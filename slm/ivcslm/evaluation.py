from __future__ import annotations

import csv
import hashlib
import math
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Sequence

import numpy as np
import torch

from .batching import deterministic_single_mask_batches, pad_encoded
from .data import Record
from .model import SignTransformer, Vocabulary


def _check_deadline(deadline_monotonic: float | None) -> None:
    if deadline_monotonic is not None and time.monotonic() >= deadline_monotonic:
        raise TimeoutError("Compute-budget deadline reached during evaluation")


@torch.inference_mode()
def masked_token_evaluation(
    model: SignTransformer,
    records: Sequence[Record],
    vocab: Vocabulary,
    batch_size: int,
    device: torch.device,
    predictions_path: Path,
    deadline_monotonic: float | None = None,
) -> dict:
    model.eval()
    rows: list[dict] = []
    top1 = top5 = total = 0
    negative_log_likelihood = 0.0
    brier_sum = 0.0
    calibration = {level: Counter() for level in (0.80, 0.90, 0.95)}
    by_site: dict[str, Counter] = defaultdict(Counter)
    by_type: dict[str, Counter] = defaultdict(Counter)
    for input_ids, positions, targets, batch_records in deterministic_single_mask_batches(
        records, vocab, batch_size, device
    ):
        _check_deadline(deadline_monotonic)
        logits = model(input_ids)
        selected = logits[torch.arange(logits.shape[0], device=device), positions]
        sign_logits = selected[:, vocab.first_sign_id :]
        log_probs = torch.log_softmax(sign_logits, dim=-1)
        target_sign = targets - vocab.first_sign_id
        ranks = torch.argsort(sign_logits, dim=-1, descending=True)
        batch_top1 = ranks[:, 0].eq(target_sign)
        batch_top5 = ranks[:, : min(5, ranks.shape[1])].eq(target_sign.unsqueeze(1)).any(dim=1)
        nll = -log_probs[torch.arange(log_probs.shape[0], device=device), target_sign]
        top1 += int(batch_top1.sum())
        top5 += int(batch_top5.sum())
        total += len(batch_records)
        negative_log_likelihood += float(nll.sum())
        probabilities = torch.softmax(sign_logits, dim=-1)
        one_hot = torch.nn.functional.one_hot(target_sign, num_classes=probabilities.shape[1]).float()
        brier = ((probabilities - one_hot) ** 2).sum(dim=1)
        brier_sum += float(brier.sum())
        sorted_probabilities, sorted_indices = torch.sort(probabilities, dim=-1, descending=True)
        cumulative = sorted_probabilities.cumsum(dim=-1)
        for level, counts in calibration.items():
            set_sizes = cumulative.lt(level).sum(dim=-1) + 1
            in_set = torch.stack(
                [
                    sorted_indices[row, : int(set_sizes[row])].eq(target_sign[row]).any()
                    for row in range(len(batch_records))
                ]
            )
            counts["covered"] += int(in_set.sum())
            counts["set_size"] += int(set_sizes.sum())
            counts["total"] += len(batch_records)
        top_values, top_indices = probabilities.topk(min(10, probabilities.shape[1]), dim=-1)
        for index, record in enumerate(batch_records):
            site = record.metadata.get("site", "unknown")
            artifact_type = record.metadata.get("type", "unknown")
            by_site[site].update(total=1, top1=int(batch_top1[index]), top5=int(batch_top5[index]))
            by_type[artifact_type].update(total=1, top1=int(batch_top1[index]), top5=int(batch_top5[index]))
            rows.append(
                {
                    "record_id": record.record_id,
                    "site": site,
                    "type": artifact_type,
                    "sequence": " ".join(record.tokens),
                    "masked_position": int(positions[index]) - 1,
                    "target": vocab.decode_id(int(targets[index])),
                    "top1_correct": int(batch_top1[index]),
                    "top5_correct": int(batch_top5[index]),
                    "negative_log_likelihood": float(nll[index]),
                    "multiclass_brier": float(brier[index]),
                    "top_predictions": "|".join(
                        f"{vocab.decode_id(int(token_id) + vocab.first_sign_id)}:{float(value):.8f}"
                        for value, token_id in zip(top_values[index], top_indices[index])
                    ),
                }
            )
    _write_rows(predictions_path, rows)
    return {
        "positions": total,
        "top1": top1 / total if total else 0.0,
        "top5": top5 / total if total else 0.0,
        "mean_negative_log_likelihood": negative_log_likelihood / total if total else math.inf,
        "perplexity": math.exp(min(negative_log_likelihood / total, 30.0)) if total else math.inf,
        "multiclass_brier": brier_sum / total if total else math.inf,
        "prediction_sets": {
            str(level): {
                "coverage": counts["covered"] / counts["total"] if counts["total"] else 0.0,
                "mean_size": counts["set_size"] / counts["total"] if counts["total"] else 0.0,
            }
            for level, counts in calibration.items()
        },
        "by_site": _counter_metrics(by_site),
        "by_type": _counter_metrics(by_type),
    }


def _counter_metrics(values: dict[str, Counter]) -> dict[str, dict]:
    return {
        key: {
            "positions": item["total"],
            "top1": item["top1"] / item["total"] if item["total"] else 0.0,
            "top5": item["top5"] / item["total"] if item["total"] else 0.0,
        }
        for key, item in sorted(values.items())
    }


def _write_rows(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


@torch.inference_mode()
def sequence_pseudo_log_likelihood(
    model: SignTransformer, tokens: tuple[str, ...], vocab: Vocabulary, device: torch.device
) -> float:
    encoded = vocab.encode(tokens)
    masked_rows: list[list[int]] = []
    targets: list[int] = []
    positions: list[int] = []
    for position in range(1, len(encoded) - 1):
        row = list(encoded)
        targets.append(row[position])
        positions.append(position)
        row[position] = vocab.mask_id
        masked_rows.append(row)
    input_ids = pad_encoded(masked_rows, vocab.pad_id, device)
    logits = model(input_ids)
    selected = logits[torch.arange(len(positions), device=device), torch.tensor(positions, device=device)]
    log_probs = torch.log_softmax(selected[:, vocab.first_sign_id :], dim=-1)
    target_tensor = torch.tensor(targets, device=device) - vocab.first_sign_id
    return float(log_probs[torch.arange(len(targets), device=device), target_tensor].sum())


@torch.inference_mode()
def directionality_evaluation(
    model: SignTransformer,
    records: Sequence[Record],
    vocab: Vocabulary,
    device: torch.device,
    output_path: Path,
    authentic_inventory: set[tuple[str, ...]],
    deadline_monotonic: float | None = None,
) -> dict:
    model.eval()
    rows = []
    wins = ties = scored = palindromes = authentic_reverse_pairs = 0
    for record in records:
        _check_deadline(deadline_monotonic)
        reversed_tokens = tuple(reversed(record.tokens))
        if reversed_tokens == record.tokens:
            palindromes += 1
            rows.append(
                {
                    "record_id": record.record_id,
                    "site": record.metadata.get("site", ""),
                    "type": record.metadata.get("type", ""),
                    "sequence": " ".join(record.tokens),
                    "stored_pll": "",
                    "reversed_pll": "",
                    "stored_minus_reversed": "",
                    "stored_wins": "",
                    "scoring_status": "skipped_palindrome",
                }
            )
            continue
        stored = sequence_pseudo_log_likelihood(model, record.tokens, vocab, device)
        reversed_score = sequence_pseudo_log_likelihood(model, reversed_tokens, vocab, device)
        margin = stored - reversed_score
        reverse_is_authentic = reversed_tokens in authentic_inventory
        if reverse_is_authentic:
            authentic_reverse_pairs += 1
        else:
            scored += 1
            wins += int(margin > 1e-9)
            ties += int(abs(margin) <= 1e-9)
        rows.append(
            {
                "record_id": record.record_id,
                "site": record.metadata.get("site", ""),
                "type": record.metadata.get("type", ""),
                "sequence": " ".join(record.tokens),
                "stored_pll": stored,
                "reversed_pll": reversed_score,
                "stored_minus_reversed": margin,
                "stored_wins": int(margin > 1e-9),
                "scoring_status": "reported_not_gated_authentic_reverse_pair" if reverse_is_authentic else "scored",
            }
        )
    _write_rows(output_path, rows)
    return {
        "rows": len(rows),
        "scored_rows": scored,
        "skipped_palindromes": palindromes,
        "authentic_reverse_pairs_reported_not_gated": authentic_reverse_pairs,
        "stored_win_share": wins / scored if scored else 0.0,
        "tie_share": ties / scored if scored else 0.0,
        "median_margin": float(
            np.median([row["stored_minus_reversed"] for row in rows if row["scoring_status"] == "scored"])
        ) if scored else 0.0,
    }


@torch.inference_mode()
def continuation_probe(
    model: SignTransformer,
    prefixes: list[list[str]],
    vocab: Vocabulary,
    device: torch.device,
    top_k: int,
    output_path: Path,
    deadline_monotonic: float | None = None,
) -> list[dict]:
    model.eval()
    rows: list[dict] = []
    for prefix in prefixes:
        _check_deadline(deadline_monotonic)
        ids = [vocab.bos_id, *vocab.encode(prefix, boundaries=False), vocab.mask_id, vocab.eos_id]
        input_ids = torch.tensor([ids], dtype=torch.long, device=device)
        logits = model(input_ids)[0, -2, vocab.first_sign_id :]
        probabilities = torch.softmax(logits, dim=-1)
        values, indices = probabilities.topk(min(top_k, probabilities.shape[0]))
        for rank, (value, index) in enumerate(zip(values, indices), 1):
            token = vocab.decode_id(int(index) + vocab.first_sign_id)
            rows.append(
                {
                    "prefix": " ".join(prefix),
                    "rank": rank,
                    "next_token": token,
                    "probability": float(value),
                }
            )
    _write_rows(output_path, rows)
    return rows


def empirical_baselines(train: Sequence[Record], test: Sequence[Record]) -> dict:
    unigram = Counter(token for record in train for token in record.tokens)
    most_common = unigram.most_common(1)[0][0]
    top5 = {token for token, _ in unigram.most_common(5)}
    total = sum(len(record.tokens) for record in test)
    unigram_top1 = sum(token == most_common for record in test for token in record.tokens) / total
    unigram_top5 = sum(token in top5 for record in test for token in record.tokens) / total
    left: dict[str, Counter] = defaultdict(Counter)
    right: dict[str, Counter] = defaultdict(Counter)
    for record in train:
        padded = ("[BOS]",) + record.tokens + ("[EOS]",)
        for index, token in enumerate(record.tokens, 1):
            left[padded[index - 1]][token] += 1
            right[padded[index + 1]][token] += 1
    correct1 = correct5 = 0
    for record in test:
        padded = ("[BOS]",) + record.tokens + ("[EOS]",)
        for index, target in enumerate(record.tokens, 1):
            scores = Counter()
            for token in unigram:
                score = left[padded[index - 1]][token] + right[padded[index + 1]][token]
                if score > 0:
                    scores[token] = score
            ranked = sorted(scores, key=lambda token: (-scores[token], -unigram[token], token))
            if not ranked:
                ranked = sorted(unigram, key=lambda token: (-unigram[token], token))
            correct1 += int(ranked[0] == target)
            correct5 += int(target in ranked[:5])
    return {
        "unigram_top1": unigram_top1,
        "unigram_top5": unigram_top5,
        "bidirectional_bigram_top1": correct1 / total,
        "bidirectional_bigram_top5": correct5 / total,
    }


def embedding_analysis(
    model: SignTransformer,
    records: Sequence[Record],
    vocab: Vocabulary,
    neighbor_count: int,
    output_path: Path,
    deadline_monotonic: float | None = None,
) -> None:
    embeddings = model.token_embedding.weight.detach().cpu().numpy()[vocab.first_sign_id :].copy()
    embeddings /= np.linalg.norm(embeddings, axis=1, keepdims=True).clip(min=1e-12)
    position_profiles: dict[str, Counter] = defaultdict(Counter)
    for record in records:
        for index, token in enumerate(record.tokens):
            role = "initial" if index == 0 else "terminal" if index == len(record.tokens) - 1 else "medial"
            position_profiles[token][role] += 1
    rows = []
    similarities = embeddings @ embeddings.T
    for local_id, token in enumerate(vocab.tokens[vocab.first_sign_id :]):
        _check_deadline(deadline_monotonic)
        neighbors = np.argsort(-similarities[local_id])
        neighbors = [index for index in neighbors if index != local_id][:neighbor_count]
        counts = position_profiles[token]
        count = sum(counts.values())
        denominator = count or 1
        rows.append(
            {
                "token": token,
                "count": count,
                "initial_share": counts["initial"] / denominator,
                "medial_share": counts["medial"] / denominator,
                "terminal_share": counts["terminal"] / denominator,
                "neighbors": "|".join(
                    f"{vocab.tokens[index + vocab.first_sign_id]}:{similarities[local_id, index]:.6f}"
                    for index in neighbors
                ),
            }
        )
    _write_rows(output_path, rows)


@torch.inference_mode()
def corruption_evaluation(
    model: SignTransformer,
    records: Sequence[Record],
    vocab: Vocabulary,
    device: torch.device,
    output_path: Path,
    authentic_inventory: set[tuple[str, ...]],
    deadline_monotonic: float | None = None,
) -> dict:
    model.eval()
    rows: list[dict] = []
    by_corruption: dict[str, Counter] = defaultdict(Counter)
    for record in records:
        _check_deadline(deadline_monotonic)
        authentic = torch.tensor([vocab.encode(record.tokens)], dtype=torch.long, device=device)
        authentic_score = float(model.authenticity_logits(authentic)[0])
        tokens = list(record.tokens)
        corruptions: dict[str, tuple[str, ...]] = {
            "reversal": tuple(reversed(tokens)),
            "rotation": tuple(tokens[1:] + tokens[:1]),
        }
        if len(tokens) > 2:
            corruptions["edge_preserving_interior_reversal"] = tuple(
                [tokens[0], *reversed(tokens[1:-1]), tokens[-1]]
            )
        replacement_pool = [token for token in vocab.tokens[vocab.first_sign_id :] if token != tokens[0]]
        if replacement_pool:
            digest = hashlib.sha256(record.record_id.encode("utf-8")).digest()
            start = int.from_bytes(digest[:8], "big") % len(replacement_pool)
            for offset in range(len(replacement_pool)):
                replacement = replacement_pool[(start + offset) % len(replacement_pool)]
                candidate = tuple([replacement, *tokens[1:]])
                if candidate not in authentic_inventory:
                    corruptions["one_edit_substitution"] = candidate
                    break
        for corruption_type, corrupted_tokens in corruptions.items():
            if corrupted_tokens == record.tokens:
                continue
            if corrupted_tokens in authentic_inventory:
                by_corruption[corruption_type]["skipped_authentic_collision"] += 1
                continue
            corrupted = torch.tensor([vocab.encode(corrupted_tokens)], dtype=torch.long, device=device)
            corrupted_score = float(model.authenticity_logits(corrupted)[0])
            margin = authentic_score - corrupted_score
            by_corruption[corruption_type].update(total=1, wins=int(margin > 0))
            rows.append(
                {
                    "record_id": record.record_id,
                    "sequence": " ".join(record.tokens),
                    "corruption_type": corruption_type,
                    "corrupted_sequence": " ".join(corrupted_tokens),
                    "authentic_logit": authentic_score,
                    "corrupted_logit": corrupted_score,
                    "margin": margin,
                    "authentic_wins": int(margin > 0),
                }
            )
    _write_rows(output_path, rows)
    reversal = by_corruption.get("reversal", Counter())
    return {
        "rows": len(rows),
        "authentic_over_reversed_share": reversal["wins"] / reversal["total"] if reversal["total"] else 0.0,
        "by_corruption": {
            name: {
                "rows": counts["total"],
                "skipped_authentic_collisions": counts["skipped_authentic_collision"],
                "authentic_win_share": counts["wins"] / counts["total"] if counts["total"] else 0.0,
            }
            for name, counts in sorted(by_corruption.items())
        },
        "median_margin": float(np.median([row["margin"] for row in rows])) if rows else 0.0,
    }
