from __future__ import annotations

import csv
import math
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import torch

from .batching import corruption_batch, masked_batch
from .data import Record
from .evaluation import masked_token_evaluation
from .model import SignTransformer, Vocabulary


@dataclass
class TrainResult:
    best_epoch: int
    best_validation_nll: float
    epochs_completed: int
    elapsed_seconds: float
    curve_path: Path
    checkpoint_path: Path
    final_checkpoint_path: Path
    optimizer_steps: int
    masked_positions_seen: int


def seed_everything(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.use_deterministic_algorithms(False)


def _batches(records: Sequence[Record], batch_size: int, rng: random.Random) -> list[list[Record]]:
    indices = list(range(len(records)))
    rng.shuffle(indices)
    return [[records[index] for index in indices[start : start + batch_size]] for start in range(0, len(indices), batch_size)]


def train_model(
    model: SignTransformer,
    train_records: list[Record],
    validation_records: list[Record],
    vocab: Vocabulary,
    config: dict,
    seed: int,
    device: torch.device,
    output_dir: Path,
    deadline_monotonic: float | None = None,
    published_authentic_inventory: set[tuple[str, ...]] | None = None,
) -> TrainResult:
    seed_everything(seed)
    output_dir.mkdir(parents=True, exist_ok=True)
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=config["learning_rate"],
        weight_decay=config["weight_decay"],
        betas=(0.9, 0.98),
    )
    configured_steps = config["epochs"] * math.ceil(len(train_records) / config["batch_size"])
    total_steps = max(1, min(configured_steps, int(config.get("max_optimizer_steps", configured_steps))))
    warmup_steps = max(10, int(total_steps * 0.06))

    def learning_rate(step: int) -> float:
        if step < warmup_steps:
            return config["learning_rate"] * (step + 1) / warmup_steps
        progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
        cosine = 0.5 * (1.0 + math.cos(math.pi * min(1.0, progress)))
        return config["min_learning_rate"] + (config["learning_rate"] - config["min_learning_rate"]) * cosine

    for group in optimizer.param_groups:
        group["lr"] = learning_rate(0)

    amp_enabled = bool(config.get("mixed_precision", True) and device.type == "cuda")
    scaler = torch.amp.GradScaler("cuda", enabled=amp_enabled)
    loss_function = torch.nn.CrossEntropyLoss(ignore_index=-100, label_smoothing=config.get("label_smoothing", 0.0))
    replacement_loss = torch.nn.BCEWithLogitsLoss(reduction="none")
    authenticity_loss = torch.nn.BCEWithLogitsLoss()
    rng = random.Random(seed)
    if config.get("separate_training_rng_streams", False):
        batch_rng = random.Random(seed + 1_000_003)
        mask_rng = random.Random(seed + 2_000_033)
        replacement_rng = random.Random(seed + 3_000_091)
        corruption_rng = random.Random(seed + 4_000_159)
    else:
        batch_rng = mask_rng = replacement_rng = corruption_rng = rng
    inventory_tokens = published_authentic_inventory or {record.tokens for record in train_records}
    authentic_inventory = {tuple(vocab.encode(tokens, boundaries=False)) for tokens in inventory_tokens}
    best_nll = math.inf
    best_epoch = 0
    stale_evaluations = 0
    curve: list[dict] = []
    checkpoint_path = output_dir / "best_model.pt"
    started = time.monotonic()
    global_step = 0
    total_masked_positions = 0
    epochs_completed = 0
    reached_step_limit = False

    for epoch in range(1, config["epochs"] + 1):
        model.train()
        train_loss = 0.0
        masked_positions = 0
        for records in _batches(train_records, config["batch_size"], batch_rng):
            if deadline_monotonic is not None and time.monotonic() >= deadline_monotonic:
                raise TimeoutError("Compute-budget deadline reached between optimizer steps")
            if global_step >= total_steps:
                reached_step_limit = True
                break
            batch = masked_batch(
                records,
                vocab,
                config["mask_probability"],
                config["random_token_probability"],
                config["keep_original_probability"],
                mask_rng,
                device,
                replacement_rng,
            )
            corruptions = corruption_batch(
                records, vocab, config["replacement_probability"], corruption_rng, device, authentic_inventory
            )
            optimizer.zero_grad(set_to_none=True)
            step_learning_rate = learning_rate(global_step)
            for group in optimizer.param_groups:
                group["lr"] = step_learning_rate
            with torch.autocast(device_type=device.type, dtype=torch.float16, enabled=amp_enabled):
                logits = model(batch.input_ids)
                mlm_loss = loss_function(logits.reshape(-1, logits.shape[-1]), batch.labels.reshape(-1))
                replacement_logits = model.replacement_logits(corruptions.corrupted_ids)
                valid_replacements = corruptions.replaced_labels.ne(-100)
                rtd_loss = replacement_loss(
                    replacement_logits[valid_replacements], corruptions.replaced_labels[valid_replacements]
                ).mean()
                authentic_logits = model.authenticity_logits(corruptions.authentic_ids)
                negative_logits = model.authenticity_logits(corruptions.negative_ids)
                contrastive_loss = authenticity_loss(authentic_logits, torch.ones_like(authentic_logits))
                contrastive_loss = contrastive_loss + authenticity_loss(negative_logits, torch.zeros_like(negative_logits))
                loss = (
                    mlm_loss
                    + config["replacement_loss_weight"] * rtd_loss
                    + config["authenticity_loss_weight"] * contrastive_loss
                )
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), config["gradient_clip"])
            scaler.step(optimizer)
            scaler.update()
            global_step += 1
            count = int(batch.labels.ne(-100).sum())
            train_loss += float(loss.detach()) * count
            masked_positions += count
            total_masked_positions += count
        epochs_completed = epoch
        reached_step_limit = reached_step_limit or global_step >= total_steps
        if epoch % config["eval_every"] != 0 and epoch != config["epochs"] and not reached_step_limit:
            continue
        validation = masked_token_evaluation(
            model,
            validation_records,
            vocab,
            config["batch_size"],
            device,
            output_dir / "validation_predictions_latest.csv",
            deadline_monotonic,
        )
        row = {
            "epoch": epoch,
            "global_step": global_step,
            "train_loss": train_loss / max(1, masked_positions),
            "validation_nll": validation["mean_negative_log_likelihood"],
            "validation_top1": validation["top1"],
            "validation_top5": validation["top5"],
            "learning_rate": optimizer.param_groups[0]["lr"],
            "elapsed_seconds": time.monotonic() - started,
        }
        curve.append(row)
        if validation["mean_negative_log_likelihood"] < best_nll - 1e-5:
            best_nll = validation["mean_negative_log_likelihood"]
            best_epoch = epoch
            stale_evaluations = 0
            torch.save(
                {
                    "model_state": model.state_dict(),
                    "parameter_count": model.parameter_count,
                    "best_epoch": best_epoch,
                    "best_validation_nll": best_nll,
                },
                checkpoint_path,
            )
        else:
            stale_evaluations += 1
        if stale_evaluations >= config["patience"]:
            break
        if reached_step_limit:
            break
    final_checkpoint_path = output_dir / "final_step_model.pt"
    torch.save(
        {
            "model_state": model.state_dict(),
            "parameter_count": model.parameter_count,
            "optimizer_steps": global_step,
            "masked_positions_seen": total_masked_positions,
            "checkpoint_role": "fixed_exposure_transfer_source_or_training_endpoint",
        },
        final_checkpoint_path,
    )
    state = torch.load(checkpoint_path, map_location=device, weights_only=True)
    model.load_state_dict(state["model_state"])
    curve_path = output_dir / "training_curve.csv"
    with curve_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(curve[0]))
        writer.writeheader()
        writer.writerows(curve)
    return TrainResult(
        best_epoch,
        best_nll,
        epochs_completed,
        time.monotonic() - started,
        curve_path,
        checkpoint_path,
        final_checkpoint_path,
        global_step,
        total_masked_positions,
    )
