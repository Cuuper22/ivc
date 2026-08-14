"""The run matrix: which models get fitted, in what order, and under what budget.

A single fit proves nothing on a corpus this small. The matrix is the actual
experiment — the same architecture and split policy run across seeds, model
sizes, comparator corpora, null controls, and transfer arms, so that a result
can be read against what it should look like if there were nothing there.

The arms are:

- IVC at each configured model size, from random initialization;
- the comparator corpora (Linear B, SumTablets, nonwriting symbol systems) under
  the identical architecture and split policy;
- null controls, which are IVC with its sign order destroyed in two different
  ways;
- the transfer tournament, where a Transformer body pretrained on one source is
  handed to IVC. Every source gets the same optimizer-step budget and matched
  data exposure, and only the body transfers — token embeddings and task heads
  are reinitialized, because the vocabularies are unrelated.

The transfer tournament is the falsifiable part, so it runs first: if the budget
runs out, the primary comparison is the part that survives. Phase 2 spends
whatever is left on the capacity curve and the corpus calibrations.

Three things guard the results. Runs are ordered so the paired design completes
first. A wall-clock deadline derived from the hourly rate and spending ceiling
stops the work rather than overrunning the budget. And every run writes into an
immutable directory holding the resolved config, input hashes, hardware and Git
metadata, and per-row predictions, so a number can always be traced back.

`_write_matrix_analysis` applies the pre-registered gate. A `pass` there is
evidence of structural transfer between writing systems. It is not evidence of
language identity, phonetic values, or readings, and the gate output says so in
its own text.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from collections import Counter, defaultdict
from dataclasses import asdict
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import numpy as np
import torch

from .data import (
    Corpus,
    Split,
    assert_split_integrity,
    assert_source_split_integrity,
    cap_corpus_by_grouped_exposure,
    combine_corpora,
    control_collision_diagnostics,
    controlled_split,
    derived_corpus_hash,
    grouped_split,
    load_ivc,
    load_linear_b,
    load_sproat,
    load_sumtablets,
    sanitize_control_split,
)
from .evaluation import (
    continuation_probe,
    corruption_evaluation,
    directionality_evaluation,
    embedding_analysis,
    empirical_baselines,
    masked_token_evaluation,
)
from .model import SPECIAL_TOKENS, ModelSpec, SignTransformer, Vocabulary
from .training import seed_everything, train_model


def _json_write(path: Path, value) -> None:
    """Write JSON with sorted keys, so two runs produce byte-comparable files."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _csv_write(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _git_value(repo: Path, *args: str) -> str:
    """Read one piece of Git provenance, or "unavailable" if Git cannot answer."""
    try:
        return subprocess.check_output(["git", *args], cwd=repo, text=True, stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unavailable"


def _git_value_or_environment(repo: Path, environment_key: str, *args: str) -> str:
    """Keep source provenance when a remote image intentionally omits `.git`.

    The GPU container is built from copied files and has no repository inside it,
    so the launcher reads the commit locally and passes it in through the
    environment. Either way the run manifest records which source produced it.
    """
    value = _git_value(repo, *args)
    if value != "unavailable":
        return value
    return os.environ.get(environment_key, "unavailable")


def _hardware_manifest(device: torch.device) -> dict:
    """Record the machine and library versions a run executed on."""
    result = {
        "platform": platform.platform(),
        "python": sys.version,
        "torch": version("torch"),
        "numpy": version("numpy"),
        "device": str(device),
        "cuda_available": torch.cuda.is_available(),
    }
    if torch.cuda.is_available():
        result.update(
            gpu_name=torch.cuda.get_device_name(device),
            cuda_version=torch.version.cuda,
            total_gpu_memory_bytes=torch.cuda.get_device_properties(device).total_memory,
        )
    return result


def resolve_paths(config_path: Path, config: dict) -> dict:
    """Turn the config's relative paths into absolute ones, rooted at the repository.

    Configs are written relative so they read the same on a laptop and in a
    container. `IVCSLM_OUTPUT_DIR` overrides the output location, which is how
    multi-gigabyte checkpoints are kept off the Git checkout.
    """
    project_root = config_path.resolve().parents[2]
    for key in ("ivc_csv", "linear_b_inventory_csv", "sumtablets_csv", "sproat_csv"):
        candidate = Path(config["data"][key])
        if not candidate.is_absolute():
            candidate = (project_root / candidate).resolve()
        config["data"][key] = str(candidate)
    output_override = os.environ.get("IVCSLM_OUTPUT_DIR")
    output = Path(output_override or config["runtime"]["output_dir"])
    if not output.is_absolute():
        output = (project_root / "slm" / output).resolve()
    config["runtime"]["output_dir"] = str(output)
    reference_summary = config.get("matrix", {}).get("reference_baseline_summary")
    if reference_summary:
        reference_path = Path(reference_summary)
        if not reference_path.is_absolute():
            reference_path = (project_root / reference_path).resolve()
        config["matrix"]["reference_baseline_summary"] = str(reference_path)
    config["project_root"] = str(project_root)
    return config


def load_config(config_path: Path) -> dict:
    """Read a run config and resolve its paths."""
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    return resolve_paths(config_path, raw)


def load_corpora(config: dict) -> dict[str, Corpus]:
    """Load every corpus the matrix can draw on, plus the merged known-writing pool.

    Linear B is loaded with a tighter length ceiling than the others, matching
    the shape of its audited Series D rows rather than the IVC window.
    """
    data = config["data"]
    seed = config["seed"]
    corpora = {
        "ivc": load_ivc(
            Path(data["ivc_csv"]),
            data["min_length"],
            data["max_length"],
            set(data["exclude_tokens"]),
            bool(data.get("require_cisi", True)),
            set(data.get("allowed_directions", ["R/L", "L/R"])),
        ),
        "linear_b": load_linear_b(
            Path(data["linear_b_inventory_csv"]),
            data["min_length"],
            min(8, data["max_length"]),
            data["max_comparator_sequences"],
            seed,
        ),
        "sumtablets": load_sumtablets(
            Path(data["sumtablets_csv"]), data["min_length"], data["max_length"], data["max_comparator_sequences"], seed
        ),
        "nonwriting": load_sproat(
            Path(data["sproat_csv"]),
            data["min_length"],
            data["max_length"],
            data["max_comparator_sequences"],
            seed,
        ),
    }
    corpora["known_writing"] = combine_corpora(
        "known_writing",
        [corpora["linear_b"], corpora["sumtablets"]],
        data["max_comparator_sequences"],
        seed,
    )
    return corpora


def _run_id(arm_name: str, model_name: str, seed: int) -> str:
    """Name a single run by the three things that identify it: arm, size, seed."""
    return f"{arm_name}__{model_name}__seed{seed}"


def _model_spec(config: dict, name: str) -> ModelSpec:
    """Look up one configured model size by name."""
    item = next(model for model in config["models"] if model["name"] == name)
    return ModelSpec(**item)


def _load_shared_encoder(model: SignTransformer, checkpoint_path: Path, device: torch.device) -> dict:
    """Copy only the Transformer body from a pretrained checkpoint into a fresh model.

    Positional embeddings, the embedding norm, and the encoder stack come across.
    Token embeddings, the tied output bias, and both task heads do not: the
    source script and IVC share no signs, so carrying their embeddings over would
    be meaningless, and carrying the heads over would smuggle in a task the new
    arm is supposed to learn on its own.

    A missing shared parameter raises rather than silently transferring a partial
    body, since a half-transferred arm would look like a transfer result without
    being one.
    """
    state = torch.load(checkpoint_path, map_location=device, weights_only=True)["model_state"]
    current = model.state_dict()
    shared_prefixes = ("position_embedding.", "embedding_norm.", "encoder.")
    transferable = {
        key: value
        for key, value in state.items()
        if key.startswith(shared_prefixes) and key in current and current[key].shape == value.shape
    }
    expected = {key for key in current if key.startswith(shared_prefixes)}
    missing = sorted(expected - transferable.keys())
    if missing:
        raise ValueError(f"Transfer checkpoint is missing compatible shared-encoder parameters: {missing[:8]}")
    model.load_state_dict(transferable, strict=False)
    return {
        "policy": "shared_transformer_body_only_fresh_token_embeddings_and_task_heads",
        "checkpoint_path": str(checkpoint_path),
        "loaded_parameter_tensors": len(transferable),
        "loaded_parameter_count": sum(value.numel() for value in transferable.values()),
        "excluded_prefixes": ["token_embedding", "output_bias", "replacement_head", "authenticity_head"],
    }


def _canonicalize_random_shared_body(
    model: SignTransformer,
    model_spec: ModelSpec,
    max_length: int,
    seed: int,
    device: torch.device,
) -> dict:
    """Make shared-body initialization invariant to script vocabulary size.

    Random initialization draws numbers in order, so a corpus with more signs
    consumes more of the random stream and ends up with a different encoder than
    a corpus with fewer signs, at the same seed. Two arms would then differ
    before training even started.

    The fix is to build a reference model with only the special tokens in its
    vocabulary, and copy its body and auxiliary heads into every arm. All arms
    now begin from the same body no matter how large their script vocabulary is.
    """
    seed_everything(seed)
    reference = SignTransformer(len(SPECIAL_TOKENS), max_length, model_spec, 0).to(device)
    state = reference.state_dict()
    shared_prefixes = (
        "position_embedding.",
        "embedding_norm.",
        "encoder.",
        "replacement_head.",
        "authenticity_head.",
    )
    shared = {key: value for key, value in state.items() if key.startswith(shared_prefixes)}
    model.load_state_dict(shared, strict=False)
    parameter_count = sum(value.numel() for value in shared.values())
    del reference
    return {
        "shared_body_policy": "canonical_random_body_and_auxiliary_heads_independent_of_script_vocabulary",
        "canonical_seed": seed,
        "loaded_parameter_tensors": len(shared),
        "loaded_parameter_count": parameter_count,
    }


def _partition_manifest(records, group_by_record_id: dict[str, int]) -> list[dict]:
    """List a partition's records with their provenance and one-edit family.

    Written to disk so the split can be audited after the fact rather than taken
    on trust.
    """
    return [
        {
            "record_id": record.record_id,
            "source_record_ids": list(record.source_record_ids),
            "artifact_ids": list(record.artifact_ids),
            "one_edit_group": group_by_record_id[record.record_id],
        }
        for record in records
    ]


def _fresh_split(corpus: Corpus, config: dict, seed: int) -> tuple[Split, list[list[str]]]:
    """Build and verify a leakage-controlled split for one corpus at one seed.

    Forced test patterns apply to IVC only; the comparator corpora carry no
    probed sequences.
    """
    split_config = config["data"]["split"]
    forced_test_patterns = config["data"].get("forced_test_patterns", []) if corpus.name == "ivc" else []
    split = grouped_split(
        corpus.records,
        split_config["validation_fraction"],
        split_config["test_fraction"],
        seed,
        split_config["stratify_field"],
        forced_test_patterns,
    )
    assert_split_integrity(split)
    return split, forced_test_patterns


def _best_control_split(
    original: Split,
    control: str,
    seed: int,
    transform_test: bool,
    attempts: int = 32,
) -> tuple[Split, dict]:
    """Try several shuffles of a null control and keep the least damaged one.

    Shuffling can create cross-partition collisions, which then have to be
    removed, and it can leave some rows unchanged. Both weaken the control. So
    the transform is tried up to `attempts` times with different seeds and the
    attempt is chosen that drops the fewest rows and, as a tiebreak, leaves the
    fewest rows unchanged. A perfect attempt — nothing dropped, nothing unchanged
    — stops the search early.

    Every attempt's diagnostics travel with the chosen split, so the reader can
    see how much attrition the selected control actually cost.
    """
    original_by_id = {
        record.record_id: record.tokens
        for partition in (original.train, original.validation, original.test)
        for record in partition
    }
    best: tuple[tuple[int, float], Split, dict] | None = None
    errors = []
    for attempt in range(attempts):
        attempt_seed = seed + attempt * 10_000_019
        transformed = controlled_split(original, control, attempt_seed, transform_test=transform_test)
        pre_sanitize = control_collision_diagnostics(transformed)
        try:
            sanitized, diagnostics = sanitize_control_split(transformed)
        except ValueError as error:
            errors.append(str(error))
            continue
        transformed_partitions = [sanitized.train, sanitized.validation]
        if transform_test:
            transformed_partitions.append(sanitized.test)
        transformed_records = [record for partition in transformed_partitions for record in partition]
        unchanged = sum(record.tokens == original_by_id[record.record_id] for record in transformed_records)
        unchanged_share = unchanged / len(transformed_records) if transformed_records else 1.0
        removed = diagnostics["removed_train_records"] + diagnostics["removed_validation_records"]
        diagnostics.update(
            {
                "selected_attempt_0based": attempt,
                "selected_attempt_seed": attempt_seed,
                "attempts_considered": attempts,
                "pre_sanitize_exact_sequence_cross_partition_pairs": pre_sanitize[
                    "exact_sequence_cross_partition_pairs"
                ],
                "pre_sanitize_one_edit_cross_partition_components": pre_sanitize[
                    "one_edit_cross_partition_components"
                ],
                "unchanged_transformed_records": unchanged,
                "unchanged_transformed_record_share": unchanged_share,
                "test_was_transformed": transform_test,
            }
        )
        score = (removed, unchanged_share)
        if best is None or score < best[0]:
            best = (score, sanitized, diagnostics)
        if score == (0, 0.0):
            break
    if best is None:
        raise ValueError(f"No leakage-safe {control} split survived {attempts} attempts: {errors[:3]}")
    return best[1], best[2]


def _controlled_ivc_arm(
    corpus: Corpus, config: dict, seed: int, control: str, name: str
) -> tuple[Corpus, Split, dict]:
    """Build a Phase-2 null arm: shuffled fitting data, authentic held-out data.

    `transform_test=False` is the important part. The training and validation
    partitions are order-destroyed, but the test partition stays exactly as
    recorded. So the arm measures how much of the authentic held-out result can
    be reached without any real sequence order to learn from.
    """
    original, _ = _fresh_split(corpus, config, seed)
    transformed, diagnostics = _best_control_split(original, control, seed, transform_test=False)
    controlled_corpus = Corpus(
        name,
        [*transformed.train, *transformed.validation, *transformed.test],
        corpus.source_path,
        derived_corpus_hash(
            corpus.source_sha256,
            [*transformed.train, *transformed.validation, *transformed.test],
            f"{control}:partition_frozen:seed={seed}",
        ),
    )
    return controlled_corpus, transformed, diagnostics


def _shuffled_pretraining_arm(corpus: Corpus, config: dict, seed: int) -> tuple[Corpus, Split, dict]:
    """Build the shuffled transfer source exclusively from the canonical IVC training pool.

    This arm asks a specific question: does a body pretrained on IVC sign
    statistics with the order removed help IVC as much as a body pretrained on
    real writing? It is the control that separates transfer of writing-like
    structure from transfer of sign frequency.

    The source is drawn only from the canonical IVC training partition, split
    again inside itself. Canonical validation and test objects never reach this
    encoder or its early stopping, and the check afterwards raises if any of them
    did.
    """
    canonical, _ = _fresh_split(corpus, config, seed)
    split_config = config["data"]["split"]
    nested = grouped_split(
        canonical.train,
        split_config["validation_fraction"],
        split_config["test_fraction"],
        seed + 3_000_017,
        split_config["stratify_field"],
    )
    assert_split_integrity(nested)
    transformed, diagnostics = _best_control_split(
        nested, "position_slot_shuffle", seed + 4_000_037, transform_test=True
    )
    forbidden_ids = {
        record.record_id
        for record in [*canonical.validation, *canonical.test]
    }
    source_ids = {
        record.record_id
        for record in [*transformed.train, *transformed.validation, *transformed.test]
    }
    if forbidden_ids & source_ids:
        raise ValueError("Shuffled pretraining source includes canonical IVC validation/test objects")
    diagnostics.update(
        {
            "source_policy": "nested_group_split_of_canonical_ivc_train_only",
            "canonical_train_pool_records": len(canonical.train),
            "canonical_validation_test_records_excluded": len(forbidden_ids),
        }
    )
    source_corpus = Corpus(
        "ivc_position_slot_shuffle",
        [*transformed.train, *transformed.validation, *transformed.test],
        corpus.source_path,
        derived_corpus_hash(
            corpus.source_sha256,
            [*transformed.train, *transformed.validation, *transformed.test],
            f"position_slot_shuffle:nested_canonical_train_only:seed={seed}",
        ),
    )
    return source_corpus, transformed, diagnostics


def _exactly_match_transfer_train_splits(
    bundles: dict[str, tuple[Corpus, Split, dict]], seed: int
) -> dict[str, tuple[Corpus, Split, dict]]:
    """Match unique training records, tokens, and length order across transfer sources.

    Approximate exposure matching leaves an opening: one source could still get
    more or longer sequences than another, and the transfer gain would be a data
    advantage wearing a structural costume.

    So the sources are cut to a common length histogram. For every sequence
    length, each source contributes the same number of training records, chosen
    by a seeded hash of the record id. The arms then differ only in what their
    sequences are, not how many or how long. Failure to hit the target exactly
    raises, since a silently mismatched tournament is not worth running.
    """
    if not bundles:
        raise ValueError("Exact transfer exposure matching requires at least one source bundle")
    length_counts = {
        name: Counter(len(record.tokens) for record in split.train)
        for name, (_, split, _) in bundles.items()
    }
    lengths = sorted({length for counts in length_counts.values() for length in counts})
    shared_histogram = {
        length: min(counts.get(length, 0) for counts in length_counts.values())
        for length in lengths
    }
    shared_histogram = {length: count for length, count in shared_histogram.items() if count > 0}
    if not shared_histogram:
        raise ValueError("Transfer sources have no shared training-record length support")

    matched: dict[str, tuple[Corpus, Split, dict]] = {}
    expected_records = sum(shared_histogram.values())
    expected_tokens = sum(length * count for length, count in shared_histogram.items())
    for name, (corpus, split, diagnostics) in bundles.items():
        selected = []
        for length, quota in sorted(shared_histogram.items()):
            candidates = [record for record in split.train if len(record.tokens) == length]
            candidates.sort(
                key=lambda record: hashlib.sha256(
                    f"{seed}|exact-transfer-exposure|{name}|{record.record_id}".encode("utf-8")
                ).hexdigest()
            )
            selected.extend(candidates[:quota])
        selected.sort(key=lambda record: (len(record.tokens), record.record_id))
        if len(selected) != expected_records or sum(len(record.tokens) for record in selected) != expected_tokens:
            raise ValueError(f"Exact transfer exposure construction failed for {name}")
        matched_split = Split(
            selected,
            split.validation,
            split.test,
            split.group_by_record_id,
            split.forced_test_record_ids,
        )
        assert_source_split_integrity(matched_split)
        matched_diagnostics = {
            **diagnostics,
            "pre_match_source_policy": diagnostics.get("source_policy"),
            "source_policy": "source_split_frozen_then_exact_train_length_histogram_match",
            "original_train_records": len(split.train),
            "original_train_tokens": sum(len(record.tokens) for record in split.train),
            "selected_train_records": expected_records,
            "selected_train_tokens": expected_tokens,
            "shared_train_length_histogram": {
                str(length): count for length, count in sorted(shared_histogram.items())
            },
            "selection_seed": seed,
        }
        matched[name] = (corpus, matched_split, matched_diagnostics)

    signatures = {
        (
            len(split.train),
            sum(len(record.tokens) for record in split.train),
            tuple(sorted(Counter(len(record.tokens) for record in split.train).items())),
        )
        for _, split, _ in matched.values()
    }
    if len(signatures) != 1:
        raise ValueError("Transfer source train exposures are not exactly matched")
    return matched


def run_one(
    corpus: Corpus,
    model_spec: ModelSpec,
    seed: int,
    config: dict,
    output_dir: Path,
    device: torch.device,
    run_label: str | None = None,
    initial_encoder_checkpoint: Path | None = None,
    fixed_split: Split | None = None,
    control_diagnostics: dict | None = None,
    training_overrides: dict | None = None,
    deadline_monotonic: float | None = None,
    published_authentic_inventory: set[tuple[str, ...]] | None = None,
) -> dict:
    """Fit and evaluate one arm at one model size and one seed, and write it out.

    This is the unit of work the whole matrix is built from. It splits (or
    accepts a frozen split), builds the vocabulary and model, fits, then runs
    every held-out measurement and writes the predictions, manifests, and summary
    into one run directory.

    Held-out scoring is reported three ways when forced test records exist:
    ordinary test records alone (the primary number, uncontaminated by the
    sequences the probes target), all test records together, and the forced
    hypothesis families on their own.
    """
    started = time.monotonic()
    seed_everything(seed)
    split_config = config["data"]["split"]
    if fixed_split is None:
        split, forced_test_patterns = _fresh_split(corpus, config, seed)
        split_integrity_policy = "exact_sequence_one_edit_source_artifact_disjoint"
    else:
        split = fixed_split
        assert_source_split_integrity(split)
        forced_test_patterns = config["data"].get("forced_test_patterns", []) if split.forced_test_record_ids else []
        if (control_diagnostics or {}).get("source_policy") == "source_split_frozen_then_exact_train_length_histogram_match":
            split_integrity_policy = "source_partitions_frozen_then_train_exposure_length_histogram_matched"
        else:
            split_integrity_policy = "source_partitions_frozen_before_null_transform_cross_partition_null_collisions_removed"
    # The vocabulary covers the whole corpus, not just the training split. That
    # is deliberate: which signs exist is published catalogue metadata, not
    # something a model has to discover. Building the vocabulary from training
    # rows alone would score every held-out sign the training split happened to
    # miss as [UNK], which measures the split rather than the model. Context and
    # frequency information still comes only from the training split, so nothing
    # about how signs are used leaks.
    vocabulary = Vocabulary([token for record in corpus.records for token in record.tokens])
    train_token_inventory = {token for record in split.train for token in record.tokens}
    train_unseen_test = sum(token not in train_token_inventory for record in split.test for token in record.tokens)
    test_tokens = sum(len(record.tokens) for record in split.test)
    model_max_length = config["data"]["max_length"] + 3
    model = SignTransformer(len(vocabulary), model_max_length, model_spec, vocabulary.pad_id).to(device)
    canonical_body = _canonicalize_random_shared_body(model, model_spec, model_max_length, seed, device)
    initialization = {
        "policy": "random_initialization",
        "checkpoint_path": None,
        **canonical_body,
    }
    if initial_encoder_checkpoint is not None:
        initialization = {
            **_load_shared_encoder(model, initial_encoder_checkpoint, device),
            "fresh_script_specific_module_seed": seed,
            "pretransfer_random_body": canonical_body,
        }
    arm_name = run_label or corpus.name
    run_id = _run_id(arm_name, model_spec.name, seed)
    run_dir = output_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    _json_write(run_dir / "vocabulary.json", vocabulary.to_dict())
    _json_write(
        run_dir / "split_manifest.json",
        {
            "split_policy": split_config,
            "split_integrity_policy": split_integrity_policy,
            "control_collision_diagnostics": control_diagnostics,
            "forced_test_patterns": forced_test_patterns,
            "forced_test_record_ids": list(split.forced_test_record_ids),
            "train": _partition_manifest(split.train, split.group_by_record_id),
            "validation": _partition_manifest(split.validation, split.group_by_record_id),
            "test": _partition_manifest(split.test, split.group_by_record_id),
            "group_by_record_id": split.group_by_record_id,
        },
    )
    training_config = {**config["training"], **(training_overrides or {})}
    if training_config.get("max_optimizer_steps"):
        steps_per_epoch = max(1, int(np.ceil(len(split.train) / training_config["batch_size"])))
        required_epochs = int(np.ceil(training_config["max_optimizer_steps"] / steps_per_epoch))
        training_config["epochs"] = max(training_config["epochs"], required_epochs)
    authentic_inventory = {record.tokens for record in corpus.records}
    if published_authentic_inventory is not None:
        authentic_inventory |= published_authentic_inventory
    training = train_model(
        model,
        split.train,
        split.validation,
        vocabulary,
        training_config,
        seed,
        device,
        run_dir,
        deadline_monotonic,
        authentic_inventory,
    )
    forced_ids = set(split.forced_test_record_ids)
    forced_test_records = [record for record in split.test if record.record_id in forced_ids]
    ordinary_test_records = [record for record in split.test if record.record_id not in forced_ids]
    primary_test_records = ordinary_test_records or list(split.test)
    masked = masked_token_evaluation(
        model,
        primary_test_records,
        vocabulary,
        training_config["batch_size"],
        device,
        run_dir / "test_masked_predictions.csv",
        deadline_monotonic,
    )
    masked_all = masked
    masked_forced = None
    if forced_test_records:
        masked_all = masked_token_evaluation(
            model,
            split.test,
            vocabulary,
            training_config["batch_size"],
            device,
            run_dir / "test_masked_predictions_all_including_forced.csv",
            deadline_monotonic,
        )
        masked_forced = masked_token_evaluation(
            model,
            forced_test_records,
            vocabulary,
            training_config["batch_size"],
            device,
            run_dir / "test_masked_predictions_forced_hypothesis_families.csv",
            deadline_monotonic,
        )
    directionality = directionality_evaluation(
        model,
        primary_test_records,
        vocabulary,
        device,
        run_dir / "test_directionality.csv",
        authentic_inventory,
        deadline_monotonic,
    )
    corruption = corruption_evaluation(
        model,
        primary_test_records,
        vocabulary,
        device,
        run_dir / "test_corruption_ranking.csv",
        authentic_inventory,
        deadline_monotonic,
    )
    probe_rows = []
    if corpus.name.startswith("ivc"):
        probe_rows = continuation_probe(
            model,
            config["probes"]["continuation_prefixes"],
            vocabulary,
            device,
            config["probes"]["top_k"],
            run_dir / "continuation_probes.csv",
            deadline_monotonic,
        )
    embedding_analysis(
        model,
        split.train,
        vocabulary,
        config["probes"]["embedding_neighbors"],
        run_dir / "embedding_neighbors.csv",
        deadline_monotonic,
    )
    summary = {
        "run_id": run_id,
        "arm": arm_name,
        "corpus": corpus.name,
        "source_path": str(corpus.source_path),
        "source_sha256": corpus.source_sha256,
        "model": asdict(model_spec),
        "parameter_count": model.parameter_count,
        "initialization": initialization,
        "seed": seed,
        "records": {
            "total": len(corpus.records),
            "train": len(split.train),
            "validation": len(split.validation),
            "test": len(split.test),
            "ordinary_test": len(primary_test_records),
            "forced_hypothesis_test": len(forced_test_records),
        },
        "tokens": {
            "total": sum(len(record.tokens) for record in corpus.records),
            "train": sum(len(record.tokens) for record in split.train),
            "validation": sum(len(record.tokens) for record in split.validation),
            "test": sum(len(record.tokens) for record in split.test),
            "ordinary_test": sum(len(record.tokens) for record in primary_test_records),
            "forced_hypothesis_test": sum(len(record.tokens) for record in forced_test_records),
        },
        "vocabulary_size": len(vocabulary),
        "inventory_policy": "full_published_sign_inventory_context_and_frequency_train_only",
        "test_train_unseen_token_count": train_unseen_test,
        "test_train_unseen_token_share": train_unseen_test / test_tokens if test_tokens else 0.0,
        "forced_hypothesis_holdout_records": len(split.forced_test_record_ids),
        "split_integrity_policy": split_integrity_policy,
        "control_collision_diagnostics": control_diagnostics,
        "training": asdict(training),
        "training_config": training_config,
        "baselines": empirical_baselines(split.train, primary_test_records),
        "masked_token": masked,
        "masked_token_all_including_forced": masked_all,
        "masked_token_forced_hypothesis_families": masked_forced,
        "directionality": directionality,
        "corruption_ranking": corruption,
        "continuation_probe_rows": len(probe_rows),
        "elapsed_seconds": time.monotonic() - started,
    }
    # Path objects cannot be serialized to JSON; store them as text.
    summary["training"]["curve_path"] = str(summary["training"]["curve_path"])
    summary["training"]["checkpoint_path"] = str(summary["training"]["checkpoint_path"])
    summary["training"]["final_checkpoint_path"] = str(summary["training"]["final_checkpoint_path"])
    _json_write(run_dir / "summary.json", summary)
    return summary


def _matrix_row(summary: dict) -> dict:
    """Flatten one run summary into a single comparison-table row.

    `null_attrition_fraction` is carried through because a control arm that had
    to drop many rows to stay leakage-free is a weaker control, and a reader
    comparing arms needs to see that.
    """
    diagnostics = summary.get("control_collision_diagnostics") or {}
    removed = diagnostics.get("removed_train_records", 0) + diagnostics.get("removed_validation_records", 0)
    fitted_pool_before_attrition = summary["records"]["train"] + summary["records"]["validation"] + removed
    return {
        "run_id": summary["run_id"],
        "arm": summary["arm"],
        "corpus": summary["corpus"],
        "model": summary["model"]["name"],
        "seed": summary["seed"],
        "initialization": summary["initialization"]["policy"],
        "parameter_count": summary["parameter_count"],
        "optimizer_steps": summary["training"]["optimizer_steps"],
        "masked_positions_seen": summary["training"]["masked_positions_seen"],
        "total_records": summary["records"]["total"],
        "train_records": summary["records"]["train"],
        "train_tokens": summary["tokens"]["train"],
        "null_attrition_fraction": removed / fitted_pool_before_attrition if fitted_pool_before_attrition else 0.0,
        "test_records": summary["records"]["test"],
        "test_positions": summary["masked_token"]["positions"],
        "masked_nll": summary["masked_token"]["mean_negative_log_likelihood"],
        "masked_perplexity": summary["masked_token"]["perplexity"],
        "masked_top1": summary["masked_token"]["top1"],
        "masked_top5": summary["masked_token"]["top5"],
        "multiclass_brier": summary["masked_token"]["multiclass_brier"],
        "stored_order_win_share": summary["directionality"]["stored_win_share"],
        "authentic_corruption_win_share": summary["corruption_ranking"]["authentic_over_reversed_share"],
        "elapsed_seconds": summary["elapsed_seconds"],
    }


def _bootstrap_mean_interval(values: list[float], seed: int, draws: int = 10_000) -> dict:
    """Bootstrap a 95% interval around the mean of paired-seed differences.

    Resample the values with replacement many times, take each resample's mean,
    and read off the 2.5th and 97.5th percentiles. With only five planned seeds
    this interval is exploratory, and the returned note says so, so a reader does
    not treat it as a proper significance test.
    """
    if not values:
        return {"n": 0, "mean": None, "ci95_low": None, "ci95_high": None}
    array = np.asarray(values, dtype=np.float64)
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(array), size=(draws, len(array)))
    means = array[indices].mean(axis=1)
    return {
        "n": len(values),
        "mean": float(array.mean()),
        "ci95_low": float(np.quantile(means, 0.025)),
        "ci95_high": float(np.quantile(means, 0.975)),
        "note": "paired_seed_bootstrap_exploratory_with_only_five_planned_seeds",
    }


def _write_matrix_analysis(run_root: Path, summaries: list[dict], config: dict) -> dict:
    """Aggregate the finished runs and apply the pre-registered gate.

    Four things are produced. Per-arm averages across seeds. Transfer
    comparisons, where each pretrained arm is compared against random-init IVC on
    the same seed, so seed-to-seed noise cancels. Specificity comparisons, where
    known-writing transfer is compared against nonwriting transfer and against
    position-slot-shuffled transfer. And exposure checks, confirming that the
    pretraining sources really did see comparable amounts of data.

    The gate reports `pass` only when every one of these holds: all three
    comparisons are complete at the planned seed count, every bootstrap lower
    bound sits above zero, exposures are inside the configured tolerance, and no
    control lost more rows to attrition than the ceiling allows. Otherwise it
    reports `fail` when the evidence is complete, and `incomplete` when it is
    not — the two are distinct, and neither is rounded into the other.

    A `pass` is structural-transfer evidence. It is not evidence of language
    identity, phonetic values, or readings, and the gate carries that boundary in
    its own output.
    """
    rows = [_matrix_row(summary) for summary in summaries]
    _csv_write(run_root / "research_comparison.csv", rows)
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(row["arm"], row["model"])].append(row)
    aggregates = []
    for (arm, model), group in sorted(grouped.items()):
        aggregates.append(
            {
                "arm": arm,
                "model": model,
                "runs": len(group),
                "seeds": sorted(row["seed"] for row in group),
                "mean_masked_nll": float(np.mean([row["masked_nll"] for row in group])),
                "mean_masked_top1": float(np.mean([row["masked_top1"] for row in group])),
                "mean_masked_top5": float(np.mean([row["masked_top5"] for row in group])),
                "mean_multiclass_brier": float(np.mean([row["multiclass_brier"] for row in group])),
                "mean_stored_order_win_share": float(np.mean([row["stored_order_win_share"] for row in group])),
                "mean_authentic_corruption_win_share": float(
                    np.mean([row["authentic_corruption_win_share"] for row in group])
                ),
            }
        )
    transfer_model = config["matrix"]["transfer_model"]
    by_arm_seed = {(row["arm"], row["seed"]): row for row in rows if row["model"] == transfer_model}
    transfers = config["matrix"].get("transfers", [])
    comparisons = []
    for transfer in transfers:
        target_arm = f"ivc_transfer_{transfer}"
        paired_seeds = sorted(
            seed
            for seed in config["training"]["seeds"]
            if ("ivc", seed) in by_arm_seed and (target_arm, seed) in by_arm_seed
        )
        nll_gains = [
            by_arm_seed[("ivc", seed)]["masked_nll"] - by_arm_seed[(target_arm, seed)]["masked_nll"]
            for seed in paired_seeds
        ]
        top1_gains = [
            by_arm_seed[(target_arm, seed)]["masked_top1"] - by_arm_seed[("ivc", seed)]["masked_top1"]
            for seed in paired_seeds
        ]
        comparisons.append(
            {
                "comparison": f"{target_arm}_vs_random_ivc",
                "positive_nll_gain_favors_transfer": _bootstrap_mean_interval(nll_gains, config["seed"]),
                "positive_top1_gain_favors_transfer": _bootstrap_mean_interval(top1_gains, config["seed"] + 1),
                "paired_seeds": paired_seeds,
            }
        )
    specificity = []
    known_arm = "ivc_transfer_known_writing"
    for comparator in ("nonwriting", "ivc_position_slot_shuffle"):
        comparator_arm = f"ivc_transfer_{comparator}"
        paired_seeds = sorted(
            seed
            for seed in config["training"]["seeds"]
            if (known_arm, seed) in by_arm_seed and (comparator_arm, seed) in by_arm_seed
        )
        values = [
            by_arm_seed[(comparator_arm, seed)]["masked_nll"] - by_arm_seed[(known_arm, seed)]["masked_nll"]
            for seed in paired_seeds
        ]
        specificity.append(
            {
                "comparison": f"{known_arm}_vs_{comparator_arm}",
                "positive_nll_gain_favors_known_writing": _bootstrap_mean_interval(
                    values, config["seed"] + len(specificity) + 2
                ),
                "paired_seeds": paired_seeds,
            }
        )
    exposure_tolerance = config["matrix"].get("transfer_exposure_tolerance_fraction", 0.20)
    attrition_ceiling = config["matrix"].get("control_max_attrition_fraction", 0.15)

    def relative_spread(values: list[float]) -> float:
        """Spread between the largest and smallest value, as a share of the largest."""
        maximum = max(values) if values else 0.0
        return (maximum - min(values)) / maximum if maximum else 0.0

    exposure_checks = []
    pretrain_arms = [f"pretrain_{name}" for name in transfers]
    for seed in config["training"]["seeds"]:
        if not pretrain_arms:
            break
        source_rows = [by_arm_seed[(arm, seed)] for arm in pretrain_arms if (arm, seed) in by_arm_seed]
        if len(source_rows) != len(pretrain_arms):
            exposure_checks.append({"seed": seed, "complete": False, "within_tolerance": False})
            continue
        record_spread = relative_spread([row["train_records"] for row in source_rows])
        token_spread = relative_spread([row["train_tokens"] for row in source_rows])
        masked_spread = relative_spread([row["masked_positions_seen"] for row in source_rows])
        max_attrition = max(row["null_attrition_fraction"] for row in source_rows)
        within = (
            record_spread <= exposure_tolerance
            and token_spread <= exposure_tolerance
            and masked_spread <= exposure_tolerance
            and max_attrition <= attrition_ceiling
        )
        exposure_checks.append(
            {
                "seed": seed,
                "complete": True,
                "within_tolerance": within,
                "train_record_relative_spread": record_spread,
                "train_token_relative_spread": token_spread,
                "masked_position_relative_spread": masked_spread,
                "maximum_null_attrition_fraction": max_attrition,
                "exposure_tolerance_fraction": exposure_tolerance,
                "attrition_ceiling_fraction": attrition_ceiling,
            }
        )
    planned_seed_count = len(config["training"]["seeds"])
    known_baseline = next(
        (item for item in comparisons if item["comparison"] == f"{known_arm}_vs_random_ivc"), None
    )
    gate_inputs = (
        [known_baseline["positive_nll_gain_favors_transfer"]] if known_baseline else []
    ) + [item["positive_nll_gain_favors_known_writing"] for item in specificity]
    statistical_complete = len(gate_inputs) == 3 and all(item["n"] == planned_seed_count for item in gate_inputs)
    exposure_checks_complete = (
        len(exposure_checks) == planned_seed_count
        and all(item.get("complete") for item in exposure_checks)
    )
    exposures_within_tolerance = exposure_checks_complete and all(
        item.get("within_tolerance") for item in exposure_checks
    )
    complete = statistical_complete and exposure_checks_complete
    passed = (
        complete
        and exposures_within_tolerance
        and all(item["ci95_low"] is not None and item["ci95_low"] > 0 for item in gate_inputs)
    )
    gate = {
        "status": "pass" if passed else "fail" if complete else "incomplete",
        "criterion": (
            "Known-writing transfer must improve ordinary held-out NLL over random-init IVC, nonwriting transfer, "
            "and position-slot-shuffled transfer, with every paired-seed bootstrap lower bound above zero and all "
            "pretraining exposures/attrition inside the configured tolerances."
        ),
        "statistical_comparisons_complete": statistical_complete,
        "exposure_checks_complete": exposure_checks_complete,
        "exposures_within_tolerance": exposures_within_tolerance,
        "interpretation_boundary": "Passing is structural-transfer evidence, not evidence of language identity, values, or readings.",
    }
    analysis = {
        "aggregates": aggregates,
        "transfer_comparisons": comparisons,
        "specificity": specificity,
        "exposure_checks": exposure_checks,
        "gate": gate,
    }
    _json_write(run_root / "research_analysis.json", analysis)
    return analysis


def run_matrix(config_path: Path, scope: str = "full") -> Path:
    """Execute the whole matrix under a budget and return the run directory.

    `scope="full"` runs everything. `scope="transfer-only"` runs just the
    transfer tournament and reads its IVC baselines from a previous matrix
    summary, which is how a second GPU session extends earlier work without
    paying to refit the baselines.

    Budget handling, in order: the hourly rate must be supplied explicitly
    through the environment rather than guessed; CUDA runs refuse to fall back to
    CPU; a deadline is computed from the rate, the spending ceiling, the hard
    runtime hours, and any hours already billed, including setup time before the
    runner started. Every fit and evaluation checks that deadline. When it fires,
    the partial state is written to `runtime_guard.json` and marked as not
    transfer-eligible, because a half-trained body would break the matched-step
    comparison.

    Application-level accounting still cannot kill a failed host process, so the
    provider workspace must also carry its own hard cap.

    Setting `IVCSLM_RESUME_RUN_ROOT` continues an existing run directory. The
    stored config must match the current one exactly, so a resumed session cannot
    quietly change the experiment.
    """
    if scope not in {"full", "transfer-only"}:
        raise ValueError(f"Unknown run scope: {scope}")
    config = load_config(config_path)
    runtime = config["runtime"]
    if os.environ.get("IVCSLM_HOURLY_RATE_USD"):
        runtime["planned_hourly_rate_usd"] = float(os.environ["IVCSLM_HOURLY_RATE_USD"])
    if runtime.get("require_cuda", False) and not os.environ.get("IVCSLM_HOURLY_RATE_USD"):
        raise RuntimeError("CUDA runs require IVCSLM_HOURLY_RATE_USD set to the actual all-in provider rate.")
    started_at = datetime.now(timezone.utc)
    wall_start = time.monotonic()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if runtime.get("require_cuda", False) and device.type != "cuda":
        raise RuntimeError("This configuration requires CUDA; refusing a silent CPU fallback.")
    corpora = load_corpora(config)
    resume_root_raw = os.environ.get("IVCSLM_RESUME_RUN_ROOT", "").strip()
    run_root = (
        Path(resume_root_raw)
        if resume_root_raw
        else Path(runtime["output_dir"]) / f"{config['experiment_name']}__{started_at.strftime('%Y%m%dT%H%M%SZ')}"
    )
    if resume_root_raw:
        if not run_root.is_dir():
            raise FileNotFoundError(f"Resume root does not exist: {run_root}")
        stored_config = json.loads((run_root / "resolved_config.json").read_text(encoding="utf-8"))
        if stored_config != config:
            raise ValueError("Resume configuration differs from the immutable original configuration.")
    else:
        run_root.mkdir(parents=True, exist_ok=False)
    write_initial = (lambda *_args, **_kwargs: None) if resume_root_raw else _json_write
    resolved_hash = hashlib.sha256(json.dumps(config, sort_keys=True).encode("utf-8")).hexdigest()
    write_initial(run_root / "resolved_config.json", config)
    project_root = Path(config["project_root"])
    corpus_inventory = {
        name: {
            "records": len(corpus.records),
            "tokens": sum(len(record.tokens) for record in corpus.records),
            "unique_tokens": len({token for record in corpus.records for token in record.tokens}),
            "duplicate_weight": sum(record.duplicate_weight for record in corpus.records),
            "source_path": str(corpus.source_path),
            "source_sha256": corpus.source_sha256,
        }
        for name, corpus in corpora.items()
    }
    write_initial(
        run_root / "run_manifest.json",
        {
            "started_at_utc": started_at.isoformat(),
            "config_sha256": resolved_hash,
            "git_commit": _git_value_or_environment(
                project_root, "IVCSLM_SOURCE_COMMIT", "rev-parse", "HEAD"
            ),
            "git_branch": _git_value_or_environment(
                project_root, "IVCSLM_SOURCE_BRANCH", "branch", "--show-current"
            ),
            "git_status_porcelain": _git_value_or_environment(
                project_root, "IVCSLM_SOURCE_STATUS_PORCELAIN", "status", "--porcelain"
            ),
            "source_tree_sha256": os.environ.get("IVCSLM_SOURCE_TREE_SHA256", "unavailable"),
            "command": " ".join(sys.argv),
            "run_scope": scope,
            "hardware": _hardware_manifest(device),
            "environment": {
                key: os.environ.get(key, "")
                for key in (
                    "RUNPOD_POD_ID",
                    "MODAL_TASK_ID",
                    "CUDA_VISIBLE_DEVICES",
                    "IVCSLM_HOURLY_RATE_USD",
                    "IVCSLM_BILLED_START_UNIX",
                )
            },
            "corpora": corpus_inventory,
        },
    )
    summaries: list[dict] = (
        json.loads((run_root / "matrix_summary.json").read_text(encoding="utf-8"))
        if resume_root_raw
        else []
    )
    completed_by_key = {
        (summary["arm"], summary["model"]["name"], summary["seed"]): summary
        for summary in summaries
    }
    model_names = [item["name"] for item in config["models"]]
    matrix = config["matrix"]
    seeds = config["training"]["seeds"]
    reference_summaries: list[dict] = []
    if scope == "transfer-only":
        reference_raw = matrix.get("reference_baseline_summary")
        if not reference_raw:
            raise ValueError("transfer-only scope requires matrix.reference_baseline_summary")
        reference_path = Path(reference_raw)
        reference_rows = json.loads(reference_path.read_text(encoding="utf-8"))
        reference_summaries = [
            row
            for row in reference_rows
            if row["arm"] == "ivc"
            and row["model"]["name"] == matrix["transfer_model"]
            and row["seed"] in seeds
        ]
        if sorted(row["seed"] for row in reference_summaries) != sorted(seeds):
            raise ValueError("Reference baseline summary does not contain one matching IVC run per seed")
        write_initial(
            run_root / "reference_baselines.json",
            {
                "source_path": str(reference_path),
                "source_sha256": hashlib.sha256(reference_path.read_bytes()).hexdigest(),
                "selection": "arm=ivc;model=transfer_model;configured_seeds",
                "summaries": reference_summaries,
            },
        )
    planned_runs = (
        len(seeds) * 2 * len(matrix.get("transfers", []))
        if scope == "transfer-only"
        else len(seeds)
        * (
            len(model_names)
            + len([name for name in matrix["corpora"] if name != "ivc"])
            + len(matrix["controls"])
            + 2 * len(matrix.get("transfers", []))
        )
    )
    spendable = runtime["budget_usd"] - runtime["budget_reserve_usd"]
    rate = runtime["planned_hourly_rate_usd"]
    if runtime.get("require_cuda", False) and rate <= 0:
        raise ValueError("CUDA hourly rate must be positive for budget enforcement.")
    prior_billed_hours = float(os.environ.get("IVCSLM_PRIOR_BILLED_HOURS", "0") or 0)
    remaining_spendable = max(0.0, spendable - prior_billed_hours * rate)
    max_hours_by_cost = remaining_spendable / rate if rate > 0 else float("inf")
    allowed_hours = min(runtime["hard_runtime_hours"], max_hours_by_cost)
    billed_start_raw = os.environ.get("IVCSLM_BILLED_START_UNIX", "")
    billed_start = float(billed_start_raw) if billed_start_raw else None
    setup_hours = max(0.0, (time.time() - billed_start) / 3600) if billed_start is not None else 0.0
    remaining_hours = max(0.0, allowed_hours - setup_hours)
    deadline_monotonic = time.monotonic() + remaining_hours * 3600

    def within_budget() -> bool:
        """True while there is still paid time left to start another run."""
        return time.monotonic() < deadline_monotonic

    def summaries_for_analysis() -> list[dict]:
        """This session's runs plus any baselines imported for transfer-only scope."""
        return [*reference_summaries, *summaries]

    def execute(
        corpus: Corpus,
        model_name: str,
        seed: int,
        run_label: str | None = None,
        initial_encoder_checkpoint: Path | None = None,
        fixed_split: Split | None = None,
        control_diagnostics: dict | None = None,
        training_overrides: dict | None = None,
        published_authentic_inventory: set[tuple[str, ...]] | None = None,
    ) -> dict | None:
        """Run one cell of the matrix, or return None if it cannot be run.

        Returns None in two cases the caller treats the same way — stop this
        sequence of runs: the budget is gone, or the deadline fired mid-run. A
        cell already completed in a resumed session is returned from cache
        instead of being refitted.

        The matrix summary and analysis are rewritten after every completed cell,
        so an interrupted session still leaves a readable, consistent result.
        """
        key = (run_label or corpus.name, model_name, seed)
        if key in completed_by_key:
            return completed_by_key[key]
        if not within_budget():
            return None
        try:
            summary = run_one(
                corpus,
                _model_spec(config, model_name),
                seed,
                config,
                run_root,
                device,
                run_label,
                initial_encoder_checkpoint,
                fixed_split,
                control_diagnostics,
                training_overrides,
                deadline_monotonic,
                published_authentic_inventory,
            )
        except TimeoutError as error:
            _json_write(
                run_root / "runtime_guard.json",
                {
                    "stopped_at_utc": datetime.now(timezone.utc).isoformat(),
                    "reason": str(error),
                    "arm": run_label or corpus.name,
                    "model": model_name,
                    "seed": seed,
                    "partial_checkpoint_not_transfer_eligible": True,
                },
            )
            return None
        summaries.append(summary)
        completed_by_key[key] = summary
        _json_write(run_root / "matrix_summary.json", summaries)
        _write_matrix_analysis(run_root, summaries_for_analysis(), config)
        return summary

    transfer_model = matrix["transfer_model"]
    transfer_names = matrix.get("transfers", [])
    exact_transfer_exposure = bool(matrix.get("exact_transfer_exposure", False))
    # Phase 1 completes every seed of the falsifiable transfer tournament before
    # spending the remaining budget on capacity and corpus-calibration controls.
    # The tournament is the part that can be wrong, so it gets the compute first;
    # if the budget runs out, what survives is the primary comparison rather than
    # a collection of descriptive arms.
    #
    # The shuffled-IVC source is built first each seed because its size sets the
    # exposure target every other pretraining pool is capped down to.
    for seed in seeds:
        shuffled_source_bundle = None
        if "ivc_position_slot_shuffle" in transfer_names:
            shuffled_source_bundle = _shuffled_pretraining_arm(corpora["ivc"], config, seed)
            shuffled_records = len(shuffled_source_bundle[0].records)
            shuffled_tokens = sum(len(record.tokens) for record in shuffled_source_bundle[0].records)
        if scope == "full" and execute(corpora["ivc"], transfer_model, seed) is None:
            break
        source_bundles: dict[str, tuple[Corpus, Split | None, dict]] = {}
        for transfer_name in transfer_names:
            if transfer_name == "ivc_position_slot_shuffle":
                if shuffled_source_bundle is None:
                    raise ValueError("Shuffled transfer source bundle was not initialized")
                source_corpus, source_split, source_diagnostics = shuffled_source_bundle
            else:
                if shuffled_source_bundle is None:
                    raise ValueError("Transfer source matching requires the shuffled IVC reference arm")
                source_corpus = cap_corpus_by_grouped_exposure(
                    corpora[transfer_name], shuffled_records, shuffled_tokens, seed
                )
                source_split = _fresh_split(source_corpus, config, seed)[0] if exact_transfer_exposure else None
                source_diagnostics = {
                    "source_policy": "whole_one_edit_groups_capped_to_shuffled_ivc_source_exposure",
                    "target_records": shuffled_records,
                    "target_tokens": shuffled_tokens,
                    "selected_records": len(source_corpus.records),
                    "selected_tokens": sum(len(record.tokens) for record in source_corpus.records),
                }
            source_bundles[transfer_name] = (source_corpus, source_split, source_diagnostics)
        if exact_transfer_exposure:
            fixed_bundles = {
                name: (corpus, split, diagnostics)
                for name, (corpus, split, diagnostics) in source_bundles.items()
                if split is not None
            }
            if len(fixed_bundles) != len(source_bundles):
                raise ValueError("Exact transfer exposure requires a frozen source split for every arm")
            source_bundles = _exactly_match_transfer_train_splits(fixed_bundles, seed)

        for transfer_name in transfer_names:
            source_corpus, source_split, source_diagnostics = source_bundles[transfer_name]
            pretraining = execute(
                source_corpus,
                transfer_model,
                seed,
                run_label=f"pretrain_{transfer_name}",
                fixed_split=source_split,
                control_diagnostics=source_diagnostics,
                training_overrides={
                    "max_optimizer_steps": matrix["transfer_pretraining_steps"],
                    "patience": 1_000_000,
                    "separate_training_rng_streams": exact_transfer_exposure,
                },
                published_authentic_inventory=(
                    {record.tokens for record in corpora["ivc"].records}
                    if transfer_name == "ivc_position_slot_shuffle"
                    else {record.tokens for record in corpora[transfer_name].records}
                ),
            )
            if pretraining is None:
                break
            checkpoint = Path(pretraining["training"]["final_checkpoint_path"])
            if execute(
                corpora["ivc"],
                transfer_model,
                seed,
                run_label=f"ivc_transfer_{transfer_name}",
                initial_encoder_checkpoint=checkpoint,
            ) is None:
                break
        if not within_budget():
            break
    # Phase 2: the capacity curve, the comparator corpora, and the null controls.
    # These describe and calibrate the result rather than test it, so they run
    # only after the primary paired design has had the first claim on compute.
    if scope == "full" and within_budget():
        for seed in seeds:
            for model_name in model_names:
                if model_name != transfer_model and execute(corpora["ivc"], model_name, seed) is None:
                    break
            for corpus_name in matrix["corpora"]:
                if corpus_name != "ivc" and execute(corpora[corpus_name], matrix["comparator_model"], seed) is None:
                    break
            for control_name in matrix["controls"]:
                transform = control_name.removeprefix("ivc_")
                controlled, frozen_split, collision_diagnostics = _controlled_ivc_arm(
                    corpora["ivc"], config, seed, transform, control_name
                )
                if execute(
                    controlled,
                    matrix["control_model"],
                    seed,
                    fixed_split=frozen_split,
                    control_diagnostics=collision_diagnostics,
                    published_authentic_inventory={record.tokens for record in corpora["ivc"].records},
                ) is None:
                    break
            if not within_budget():
                break
    elapsed_hours = (time.monotonic() - wall_start) / 3600
    session_billed_hours = max(0.0, (time.time() - billed_start) / 3600) if billed_start is not None else elapsed_hours
    billed_elapsed_hours = prior_billed_hours + session_billed_hours
    analysis = _write_matrix_analysis(run_root, summaries_for_analysis(), config)
    final = {
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "completed_runs": len(summaries),
        "planned_runs": planned_runs,
        "reference_runs": len(reference_summaries),
        "run_scope": scope,
        "elapsed_hours": elapsed_hours,
        "billed_elapsed_hours_including_reported_setup": billed_elapsed_hours,
        "setup_hours_before_runner": setup_hours,
        "prior_billed_hours_conservative": prior_billed_hours,
        "resume_session": bool(resume_root_raw),
        "resume_source_tree_sha256": os.environ.get("IVCSLM_RESUME_SOURCE_TREE_SHA256", ""),
        "resume_source_status_porcelain": os.environ.get("IVCSLM_RESUME_SOURCE_STATUS_PORCELAIN", ""),
        "hourly_rate_usd": rate,
        "estimated_compute_cost_usd": billed_elapsed_hours * rate,
        "budget_ceiling_usd": runtime["budget_usd"],
        "budget_reserve_usd": runtime["budget_reserve_usd"],
        "allowed_runtime_hours": allowed_hours,
        "stopped_for_runtime_guard": len(summaries) < planned_runs,
        "research_gate": analysis["gate"],
        "run_ids": [summary["run_id"] for summary in summaries],
    }
    _json_write(run_root / "completion.json", final)
    return run_root
