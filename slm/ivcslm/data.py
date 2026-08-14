from __future__ import annotations

import csv
import hashlib
import random
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence


IVC_PATTERN = re.compile(r"^\+(\d{3}(?:-\d{3})*)\+$")


@dataclass(frozen=True)
class Record:
    record_id: str
    tokens: tuple[str, ...]
    metadata: dict[str, str] = field(compare=False, hash=False)
    duplicate_weight: int = 1
    source_record_ids: tuple[str, ...] = field(default_factory=tuple, compare=False, hash=False)
    artifact_ids: tuple[str, ...] = field(default_factory=tuple, compare=False, hash=False)


@dataclass
class Corpus:
    name: str
    records: list[Record]
    source_path: Path
    source_sha256: str


@dataclass
class Split:
    train: list[Record]
    validation: list[Record]
    test: list[Record]
    group_by_record_id: dict[str, int]
    forced_test_record_ids: tuple[str, ...] = ()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def derived_corpus_hash(parent_sha256: str, records: Sequence[Record], policy: str) -> str:
    digest = hashlib.sha256()
    digest.update(f"parent={parent_sha256}\npolicy={policy}\n".encode("utf-8"))
    for record in sorted(records, key=lambda item: item.record_id):
        digest.update(record.record_id.encode("utf-8"))
        digest.update(b"\0")
        digest.update("\x1f".join(record.tokens).encode("utf-8"))
        digest.update(b"\0")
        digest.update("\x1f".join(record.source_record_ids).encode("utf-8"))
        digest.update(b"\0")
        digest.update("\x1f".join(record.artifact_ids).encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()


def _collapse(records: Iterable[Record]) -> list[Record]:
    grouped: dict[tuple[str, ...], list[Record]] = defaultdict(list)
    for record in records:
        grouped[record.tokens].append(record)
    collapsed: list[Record] = []
    for tokens, rows in sorted(grouped.items(), key=lambda item: (len(item[0]), item[0])):
        metadata: dict[str, str] = {}
        keys = sorted({key for row in rows for key in row.metadata})
        for key in keys:
            values = sorted({row.metadata.get(key, "") for row in rows if row.metadata.get(key, "")})
            metadata[key] = "|".join(values)
        collapsed.append(
            Record(
                record_id=rows[0].record_id,
                tokens=tokens,
                metadata=metadata,
                duplicate_weight=sum(max(1, row.duplicate_weight) for row in rows),
                source_record_ids=tuple(
                    sorted({item for row in rows for item in (row.source_record_ids or (row.record_id,))})
                ),
                artifact_ids=tuple(sorted({item for row in rows for item in row.artifact_ids if item})),
            )
        )
    return collapsed


def load_ivc(
    path: Path,
    min_length: int,
    max_length: int,
    exclude_tokens: set[str],
    require_cisi: bool = True,
    allowed_directions: set[str] | None = None,
) -> Corpus:
    records: list[Record] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            cisi = (row.get("cisi") or "").strip()
            direction = (row.get("dir.") or "").strip()
            if require_cisi and cisi in {"", "-", "--"}:
                continue
            if allowed_directions is not None and direction not in allowed_directions:
                continue
            match = IVC_PATTERN.fullmatch((row.get("text") or "").strip())
            if not match or row.get("complete") != "Y":
                continue
            tokens = tuple(match.group(1).split("-"))
            if not min_length <= len(tokens) <= max_length or any(token in exclude_tokens for token in tokens):
                continue
            try:
                stated_length = int(row.get("text length") or row.get("signs") or -1)
            except ValueError:
                continue
            if stated_length != len(tokens):
                continue
            records.append(
                Record(
                    record_id=row.get("id", ""),
                    tokens=tokens,
                    metadata={
                        "cisi": cisi,
                        "site": row.get("site", ""),
                        "region": row.get("region", ""),
                        "type": row.get("type", ""),
                        "material": row.get("material", ""),
                        "symbol": row.get("symbol", ""),
                        "cult": row.get("cult", ""),
                        "direction": direction,
                    },
                    source_record_ids=(row.get("id", ""),),
                    artifact_ids=(cisi,),
                )
            )
    return Corpus("ivc", _collapse(records), path, sha256_file(path))


def _deterministic_cap(records: list[Record], limit: int, seed: int) -> list[Record]:
    if len(records) <= limit:
        return records
    def key(record: Record) -> str:
        material = f"{seed}|{' '.join(record.tokens)}".encode("utf-8")
        return hashlib.sha256(material).hexdigest()
    return sorted(records, key=key)[:limit]


def load_linear_b(path: Path, min_length: int, max_length: int, limit: int, seed: int) -> Corpus:
    records: list[Record] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if row.get("dataset_slice") != "real_series_d_default_clean":
                continue
            if row.get("ivc_p95_length_eligible", "").lower() != "true":
                continue
            tokens = tuple(
                sign
                for word in (row.get("raw_sequence") or "").split()
                for sign in word.split("-")
                if sign
            )
            if min_length <= len(tokens) <= max_length:
                record_id = f"linear_b_{int(row['row_index_1based']):05d}"
                records.append(
                    Record(
                        record_id,
                        tokens,
                        {"site": "Linear B", "type": "Series D"},
                        1,
                        (record_id,),
                        (record_id,),
                    )
                )
    collapsed = _deterministic_cap(_collapse(records), limit, seed)
    return Corpus("linear_b", collapsed, path, sha256_file(path))


def load_sumtablets(path: Path, min_length: int, max_length: int, limit: int, seed: int) -> Corpus:
    records: list[Record] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            tokens = tuple(token for token in (row.get("tokens") or "").split() if token)
            if min_length <= len(tokens) <= max_length:
                source_tablet_ids = tuple(
                    item
                    for item in (row.get("source_tablet_ids") or row.get("first_source_tablet_id") or row.get("line_id", "")).split("|")
                    if item
                )
                records.append(
                    Record(
                        row.get("line_id", ""),
                        tokens,
                        {"site": row.get("first_period", ""), "type": row.get("first_genre", "")},
                        int(row.get("duplicate_weight") or 1),
                        (row.get("line_id", ""),),
                        source_tablet_ids,
                    )
                )
    collapsed = _deterministic_cap(_collapse(records), limit, seed)
    return Corpus("sumtablets", collapsed, path, sha256_file(path))


def load_sproat(path: Path, min_length: int, max_length: int, limit: int, seed: int) -> Corpus:
    records: list[Record] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            tokens = tuple(token.strip() for token in (row.get("tokens") or "").split("|") if token.strip())
            if not min_length <= len(tokens) <= max_length:
                continue
            record_id = row.get("sequence_id", "")
            source_ids = tuple(item for item in (row.get("source_ids") or record_id).split("|") if item)
            records.append(
                Record(
                    record_id,
                    tuple(f"{row.get('corpus', 'unknown')}::{token}" for token in tokens),
                    {"site": row.get("corpus", ""), "type": row.get("system_class", "")},
                    int(row.get("duplicate_weight") or 1),
                    source_ids,
                    source_ids,
                )
            )
    return Corpus("nonwriting", _deterministic_cap(_collapse(records), limit, seed), path, sha256_file(path))


def combine_corpora(name: str, corpora: Sequence[Corpus], limit: int, seed: int) -> Corpus:
    records: list[Record] = []
    for corpus in corpora:
        for record in corpus.records:
            records.append(
                Record(
                    f"{corpus.name}::{record.record_id}",
                    tuple(f"{corpus.name}::{token}" for token in record.tokens),
                    {**record.metadata, "source_corpus": corpus.name},
                    record.duplicate_weight,
                    tuple(f"{corpus.name}::{item}" for item in record.source_record_ids),
                    tuple(f"{corpus.name}::{item}" for item in record.artifact_ids),
                )
            )
    selected = _deterministic_cap(records, limit, seed)
    parent_hash = hashlib.sha256("|".join(corpus.source_sha256 for corpus in corpora).encode("ascii")).hexdigest()
    source_hash = derived_corpus_hash(parent_hash, selected, f"combine_corpora:{name}:limit={limit}:seed={seed}")
    return Corpus(name, selected, corpora[0].source_path, source_hash)


def cap_corpus_by_grouped_exposure(
    corpus: Corpus, target_records: int, target_tokens: int, seed: int
) -> Corpus:
    """Cap a source pool by whole leakage groups and approximate record/token exposure."""
    components = one_edit_components(corpus.records)
    ranked = sorted(
        components,
        key=lambda component: hashlib.sha256(
            f"{seed}|{'|'.join(sorted(corpus.records[index].record_id for index in component))}".encode("utf-8")
        ).hexdigest(),
    )
    selected: list[int] = []
    record_count = 0
    token_count = 0
    for component in ranked:
        component_records = len(component)
        component_tokens = sum(len(corpus.records[index].tokens) for index in component)
        exceeds_records = record_count + component_records > target_records
        exceeds_tokens = token_count + component_tokens > target_tokens
        if selected and (exceeds_records or exceeds_tokens):
            continue
        selected.extend(component)
        record_count += component_records
        token_count += component_tokens
        if record_count >= target_records or token_count >= target_tokens:
            break
    if not selected:
        raise ValueError(f"Could not select a grouped exposure pool for {corpus.name}")
    records = [corpus.records[index] for index in sorted(selected)]
    source_hash = derived_corpus_hash(
        corpus.source_sha256,
        records,
        f"grouped_exposure_cap:records={target_records}:tokens={target_tokens}:seed={seed}",
    )
    return Corpus(corpus.name, records, corpus.source_path, source_hash)


class DisjointSet:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, left: int, right: int) -> None:
        left_root, right_root = self.find(left), self.find(right)
        if left_root == right_root:
            return
        if self.rank[left_root] < self.rank[right_root]:
            left_root, right_root = right_root, left_root
        self.parent[right_root] = left_root
        if self.rank[left_root] == self.rank[right_root]:
            self.rank[left_root] += 1


def one_edit_components(records: Sequence[Record]) -> list[list[int]]:
    """Connect exact-collapsed rows separated by one substitution/insertion/deletion."""
    dsu = DisjointSet(len(records))
    substitution_signatures: dict[tuple[int, int, tuple[str, ...]], int] = {}
    exact: dict[tuple[str, ...], int] = {record.tokens: index for index, record in enumerate(records)}
    for index, record in enumerate(records):
        tokens = record.tokens
        for position in range(len(tokens)):
            signature = (len(tokens), position, tokens[:position] + ("*",) + tokens[position + 1 :])
            previous = substitution_signatures.get(signature)
            if previous is None:
                substitution_signatures[signature] = index
            else:
                dsu.union(index, previous)
            shortened = tokens[:position] + tokens[position + 1 :]
            if shortened in exact:
                dsu.union(index, exact[shortened])
    artifact_owner: dict[str, int] = {}
    for index, record in enumerate(records):
        for artifact_id in record.artifact_ids:
            previous = artifact_owner.get(artifact_id)
            if previous is None:
                artifact_owner[artifact_id] = index
            else:
                dsu.union(index, previous)
    components: dict[int, list[int]] = defaultdict(list)
    for index in range(len(records)):
        components[dsu.find(index)].append(index)
    return sorted(components.values(), key=lambda values: (-len(values), values[0]))


def _component_stratum(records: Sequence[Record], indices: Sequence[int], field: str) -> str:
    values: Counter[str] = Counter()
    for index in indices:
        for value in records[index].metadata.get(field, "").split("|"):
            if value:
                values[value] += 1
    return values.most_common(1)[0][0] if values else "unknown"


def _contains_pattern(tokens: tuple[str, ...], pattern: tuple[str, ...]) -> bool:
    width = len(pattern)
    return width > 0 and any(tokens[start : start + width] == pattern for start in range(len(tokens) - width + 1))


def grouped_split(
    records: list[Record],
    validation_fraction: float,
    test_fraction: float,
    seed: int,
    stratify_field: str,
    forced_test_patterns: Sequence[Sequence[str]] = (),
) -> Split:
    components = one_edit_components(records)
    rng = random.Random(seed)
    patterns = tuple(tuple(pattern) for pattern in forced_test_patterns if pattern)
    forced_component_ids = {
        group_id
        for group_id, component in enumerate(components)
        if any(_contains_pattern(records[index].tokens, pattern) for index in component for pattern in patterns)
    }
    strata: dict[str, list[list[int]]] = defaultdict(list)
    for group_id, component in enumerate(components):
        if group_id in forced_component_ids:
            continue
        strata[_component_stratum(records, component, stratify_field)].append(component)
    allocations: dict[int, str] = {}
    counts = Counter()
    for group_id in sorted(forced_component_ids):
        component = components[group_id]
        for index in component:
            allocations[index] = "test"
        counts["test"] += len(component)
    for stratum in sorted(strata):
        groups = strata[stratum]
        rng.shuffle(groups)
        stratum_total = sum(len(component) for component in groups)
        targets = {
            "validation": round(stratum_total * validation_fraction),
            "test": round(stratum_total * test_fraction),
        }
        targets["train"] = stratum_total - targets["validation"] - targets["test"]
        stratum_counts = Counter()
        for component in groups:
            options = ["train", "validation", "test"]
            deficits = {
                name: targets[name] - stratum_counts[name]
                for name in options
            }
            split_name = max(options, key=lambda name: (deficits[name], name == "train"))
            for index in component:
                allocations[index] = split_name
            counts[split_name] += len(component)
            stratum_counts[split_name] += len(component)
    # Guarantee all partitions exist even when a giant component dominates.
    for required in ("validation", "test"):
        if counts[required] == 0:
            candidates = [component for component in components if allocations[component[0]] == "train"]
            component = min(candidates, key=len)
            for index in component:
                allocations[index] = required
            counts["train"] -= len(component)
            counts[required] += len(component)
    buckets: dict[str, list[Record]] = defaultdict(list)
    group_by_record_id: dict[str, int] = {}
    for group_id, component in enumerate(components):
        for index in component:
            record = records[index]
            buckets[allocations[index]].append(record)
            group_by_record_id[record.record_id] = group_id
    for values in buckets.values():
        values.sort(key=lambda row: row.record_id)
    forced_test_record_ids = tuple(
        sorted(records[index].record_id for group_id in forced_component_ids for index in components[group_id])
    )
    return Split(
        buckets["train"],
        buckets["validation"],
        buckets["test"],
        group_by_record_id,
        forced_test_record_ids,
    )


def controlled_split(split: Split, control: str, seed: int, transform_test: bool = True) -> Split:
    """Apply a null transformation independently inside each frozen partition."""
    transformed = Split(
        apply_control(split.train, control, seed),
        apply_control(split.validation, control, seed + 1_000_003),
        apply_control(split.test, control, seed + 2_000_003) if transform_test else list(split.test),
        dict(split.group_by_record_id),
        split.forced_test_record_ids,
    )
    original_ids = [
        {record.record_id for record in partition}
        for partition in (split.train, split.validation, split.test)
    ]
    transformed_ids = [
        {record.record_id for record in partition}
        for partition in (transformed.train, transformed.validation, transformed.test)
    ]
    if original_ids != transformed_ids:
        raise ValueError("Control transformation changed frozen partition membership")
    original_artifacts = {
        record.record_id: record.artifact_ids
        for partition in (split.train, split.validation, split.test)
        for record in partition
    }
    for partition in (transformed.train, transformed.validation, transformed.test):
        for record in partition:
            if record.artifact_ids != original_artifacts[record.record_id]:
                raise ValueError("Control transformation changed source-artifact membership")
    return transformed


def control_collision_diagnostics(split: Split) -> dict[str, int | str]:
    partitions = (split.train, split.validation, split.test)
    token_sets = [{record.tokens for record in rows} for rows in partitions]
    exact_pairs = (
        len(token_sets[0] & token_sets[1])
        + len(token_sets[0] & token_sets[2])
        + len(token_sets[1] & token_sets[2])
    )
    labelled = [
        (partition_id, record)
        for partition_id, rows in enumerate(partitions)
        for record in rows
    ]
    components = one_edit_components([record for _, record in labelled])
    cross_partition_components = sum(
        len({labelled[index][0] for index in component}) > 1
        for component in components
    )
    return {
        "exact_sequence_cross_partition_pairs": exact_pairs,
        "one_edit_cross_partition_components": cross_partition_components,
        "note": "Original source families remain frozen; this diagnostic is used before and after collision removal.",
    }


def sanitize_control_split(split: Split) -> tuple[Split, dict]:
    """Remove lower-priority null rows until train/validation/test are one-edit disjoint.

    Test membership is preserved. If a null component touches test, its train and
    validation rows are removed; otherwise validation rows are removed when a
    component also touches train. This makes the null weaker rather than allowing
    transformed held-out strings to leak into fitting or checkpoint selection.
    """
    partitions = (split.train, split.validation, split.test)
    labelled = [
        (partition_id, record)
        for partition_id, rows in enumerate(partitions)
        for record in rows
    ]
    components = one_edit_components([record for _, record in labelled])
    drop_ids: set[str] = set()
    spanning_components = 0
    for component in components:
        present = {labelled[index][0] for index in component}
        if len(present) <= 1:
            continue
        spanning_components += 1
        if 2 in present:
            drop_partitions = {0, 1}
        else:
            drop_partitions = {1}
        drop_ids.update(
            labelled[index][1].record_id
            for index in component
            if labelled[index][0] in drop_partitions
        )
    sanitized = Split(
        [record for record in split.train if record.record_id not in drop_ids],
        [record for record in split.validation if record.record_id not in drop_ids],
        list(split.test),
        dict(split.group_by_record_id),
        split.forced_test_record_ids,
    )
    assert_source_split_integrity(sanitized)
    after = control_collision_diagnostics(sanitized)
    if after["exact_sequence_cross_partition_pairs"] or after["one_edit_cross_partition_components"]:
        raise ValueError("Null-world collision sanitization did not produce disjoint partitions")
    if not sanitized.train or not sanitized.validation or not sanitized.test:
        raise ValueError("Null-world collision sanitization emptied a required partition")
    diagnostics = {
        "pre_sanitize_spanning_components": spanning_components,
        "removed_train_records": len(split.train) - len(sanitized.train),
        "removed_validation_records": len(split.validation) - len(sanitized.validation),
        "removed_test_records": 0,
        "retained_test_records": len(sanitized.test),
        "post_sanitize_exact_sequence_cross_partition_pairs": after["exact_sequence_cross_partition_pairs"],
        "post_sanitize_one_edit_cross_partition_components": after["one_edit_cross_partition_components"],
        "policy": "preserve_test_drop_colliding_train_then_validation_components",
    }
    return sanitized, diagnostics


def _nonidentity_shuffle(values: list[str], rng: random.Random) -> list[str]:
    if len(values) < 2 or len(set(values)) < 2:
        return list(values)
    original = list(values)
    for _ in range(32):
        candidate = list(values)
        rng.shuffle(candidate)
        if candidate != original:
            return candidate
    rotations = [original[offset:] + original[:offset] for offset in range(1, len(original))]
    alternatives = [candidate for candidate in rotations if candidate != original]
    if alternatives:
        return rng.choice(alternatives)
    return list(reversed(original))


def apply_control(records: list[Record], control: str, seed: int) -> list[Record]:
    rng = random.Random(seed)
    if control == "row_internal_shuffle":
        output = []
        for record in records:
            tokens = _nonidentity_shuffle(list(record.tokens), rng)
            output.append(
                Record(
                    record.record_id,
                    tuple(tokens),
                    record.metadata,
                    record.duplicate_weight,
                    record.source_record_ids,
                    record.artifact_ids,
                )
            )
        return output
    if control == "position_slot_shuffle":
        by_length: dict[int, list[Record]] = defaultdict(list)
        for record in records:
            by_length[len(record.tokens)].append(record)
        output: list[Record] = []
        for length, rows in sorted(by_length.items()):
            columns = [[record.tokens[position] for record in rows] for position in range(length)]
            columns = [_nonidentity_shuffle(column, rng) for column in columns]
            for row_index, record in enumerate(rows):
                tokens = tuple(columns[position][row_index] for position in range(length))
                output.append(
                    Record(
                        record.record_id,
                        tokens,
                        record.metadata,
                        record.duplicate_weight,
                        record.source_record_ids,
                        record.artifact_ids,
                    )
                )
        return output
    raise ValueError(f"Unknown control: {control}")


def assert_source_split_integrity(split: Split) -> None:
    partitions = [split.train, split.validation, split.test]
    id_sets = [{record.record_id for record in rows} for rows in partitions]
    if id_sets[0] & id_sets[1] or id_sets[0] & id_sets[2] or id_sets[1] & id_sets[2]:
        raise ValueError("Record leakage across split partitions")
    groups = [
        {split.group_by_record_id[record.record_id] for record in rows}
        for rows in partitions
    ]
    if groups[0] & groups[1] or groups[0] & groups[2] or groups[1] & groups[2]:
        raise ValueError("One-edit family leakage across split partitions")
    artifacts = [{artifact for record in rows for artifact in record.artifact_ids} for rows in partitions]
    if artifacts[0] & artifacts[1] or artifacts[0] & artifacts[2] or artifacts[1] & artifacts[2]:
        raise ValueError("Catalogue object/source tablet leakage across split partitions")


def assert_split_integrity(split: Split) -> None:
    assert_source_split_integrity(split)
    partitions = [split.train, split.validation, split.test]
    token_sets = [{record.tokens for record in rows} for rows in partitions]
    if token_sets[0] & token_sets[1] or token_sets[0] & token_sets[2] or token_sets[1] & token_sets[2]:
        raise ValueError("Exact sequence leakage across split partitions")
