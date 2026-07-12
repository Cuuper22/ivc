from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Sequence

import torch

from .data import Record
from .model import Vocabulary


@dataclass
class Batch:
    input_ids: torch.Tensor
    labels: torch.Tensor
    record_ids: list[str]


@dataclass
class CorruptionBatch:
    corrupted_ids: torch.Tensor
    replaced_labels: torch.Tensor
    authentic_ids: torch.Tensor
    negative_ids: torch.Tensor


def pad_encoded(encoded: list[list[int]], pad_id: int, device: torch.device) -> torch.Tensor:
    width = max(len(row) for row in encoded)
    tensor = torch.full((len(encoded), width), pad_id, dtype=torch.long, device=device)
    for index, row in enumerate(encoded):
        tensor[index, : len(row)] = torch.tensor(row, dtype=torch.long, device=device)
    return tensor


def masked_batch(
    records: Sequence[Record],
    vocab: Vocabulary,
    mask_probability: float,
    random_token_probability: float,
    keep_original_probability: float,
    rng: random.Random,
    device: torch.device,
) -> Batch:
    encoded = [vocab.encode(record.tokens) for record in records]
    input_ids = pad_encoded(encoded, vocab.pad_id, device)
    labels = torch.full_like(input_ids, -100)
    sign_ids = list(range(vocab.first_sign_id, len(vocab)))
    for row_index, row in enumerate(encoded):
        candidate_positions = list(range(1, len(row) - 1))
        chosen = [position for position in candidate_positions if rng.random() < mask_probability]
        if not chosen:
            chosen = [rng.choice(candidate_positions)]
        for position in chosen:
            labels[row_index, position] = input_ids[row_index, position]
            draw = rng.random()
            if draw < keep_original_probability:
                continue
            if draw < keep_original_probability + random_token_probability:
                input_ids[row_index, position] = rng.choice(sign_ids)
            else:
                input_ids[row_index, position] = vocab.mask_id
    return Batch(input_ids, labels, [record.record_id for record in records])


def corruption_batch(
    records: Sequence[Record],
    vocab: Vocabulary,
    replacement_probability: float,
    rng: random.Random,
    device: torch.device,
    authentic_inventory: set[tuple[int, ...]],
) -> CorruptionBatch:
    authentic = [vocab.encode(record.tokens) for record in records]
    corrupted = [list(row) for row in authentic]
    replacement_labels: list[list[float]] = []
    sign_ids = list(range(vocab.first_sign_id, len(vocab)))
    for row in corrupted:
        labels = [0.0] * len(row)
        candidate_positions = list(range(1, len(row) - 1))
        chosen = [position for position in candidate_positions if rng.random() < replacement_probability]
        if not chosen:
            chosen = [rng.choice(candidate_positions)]
        for position in chosen:
            original = row[position]
            replacement = rng.choice(sign_ids)
            while replacement == original and len(sign_ids) > 1:
                replacement = rng.choice(sign_ids)
            row[position] = replacement
            labels[position] = 1.0
        replacement_labels.append(labels)
    negative: list[list[int]] = []
    for row in authentic:
        signs = list(row[1:-1])
        candidates: list[list[int]] = []
        candidates.append(list(reversed(signs)))
        if len(signs) > 2:
            candidates.append([signs[0], *reversed(signs[1:-1]), signs[-1]])
        if len(signs) > 1:
            candidates.append(signs[1:] + signs[:1])
        shuffled = list(signs)
        rng.shuffle(shuffled)
        candidates.append(shuffled)
        rng.shuffle(candidates)
        changed = next(
            (
                candidate
                for candidate in candidates
                if candidate != signs and tuple(candidate) not in authentic_inventory
            ),
            None,
        )
        if changed is None:
            search_positions = list(range(len(signs)))
            rng.shuffle(search_positions)
            search_signs = list(sign_ids)
            rng.shuffle(search_signs)
            for position in search_positions:
                for replacement in search_signs:
                    candidate = list(signs)
                    candidate[position] = replacement
                    if candidate != signs and tuple(candidate) not in authentic_inventory:
                        changed = candidate
                        break
                if changed is not None:
                    break
        if changed is None:
            raise ValueError("Could not construct a corruption outside the authentic training inventory")
        negative.append([vocab.bos_id, *changed, vocab.eos_id])
    corrupted_tensor = pad_encoded(corrupted, vocab.pad_id, device)
    label_tensor = torch.full(corrupted_tensor.shape, -100.0, dtype=torch.float32, device=device)
    for index, labels in enumerate(replacement_labels):
        label_tensor[index, : len(labels)] = torch.tensor(labels, dtype=torch.float32, device=device)
    return CorruptionBatch(
        corrupted_tensor,
        label_tensor,
        pad_encoded(authentic, vocab.pad_id, device),
        pad_encoded(negative, vocab.pad_id, device),
    )


def deterministic_single_mask_batches(
    records: Sequence[Record], vocab: Vocabulary, batch_size: int, device: torch.device
):
    examples: list[tuple[list[int], int, int, Record]] = []
    for record in records:
        encoded = vocab.encode(record.tokens)
        for position in range(1, len(encoded) - 1):
            row = list(encoded)
            target = row[position]
            row[position] = vocab.mask_id
            examples.append((row, position, target, record))
    for start in range(0, len(examples), batch_size):
        chunk = examples[start : start + batch_size]
        yield (
            pad_encoded([item[0] for item in chunk], vocab.pad_id, device),
            torch.tensor([item[1] for item in chunk], dtype=torch.long, device=device),
            torch.tensor([item[2] for item in chunk], dtype=torch.long, device=device),
            [item[3] for item in chunk],
        )
