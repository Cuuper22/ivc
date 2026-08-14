"""Batch-profile every repeated tail family after 002-861 in one pass.

Rather than auditing tails one at a time, this script picks its own unit
list: every tail that appears at least twice in the strict deduped suffix
rows, plus a fixed set of extras (255 416, 416, 698, 096, 000). For each
unit it scans the whole strict corpus for occurrences anywhere, classifies
its distribution (restricted to 002-861, mixed with independent uses, or
neither), and checks whether matched bare controls exist — inscriptions that
share the tail's preframe but end bare — including which of those controls
are already source-visible. Each unit gets an evidence role such as
restricted_tail_with_bare_controls. Writes a family summary CSV, an
occurrences CSV, and a JSON summary listing the priority units.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path.cwd()
METADATA = ROOT / "data" / "open_prototype" / "lipi" / "metadata_filtered.csv"
REPORTS = ROOT / "data" / "open_prototype" / "reports"
SUFFIX_ROWS = REPORTS / "campaign_032_002_861_suffix_split_rows.csv"
REPORTS.mkdir(parents=True, exist_ok=True)

EXTRA_UNITS = {"255 416", "416", "698", "096", "000"}
SOURCE_VISIBLE_TAILED = {"M-91", "M-240", "M-714", "M-376", "M-391", "M-1273"}
SOURCE_VISIBLE_BARE = {"H-444", "M-723", "M-1044", "M-77", "M-118", "M-15"}
UNIT_REVIEW_ORDER = ["603", "533 717", "255 416", "096", "416", "698", "000"]


def parse_tokens(text: str) -> list[str] | None:
    if not (text.startswith("+") and text.endswith("+")):
        return None
    if any(ch in text for ch in "[]()"):
        return None
    tokens = [token for token in text.strip("+").split("-") if token]
    if not tokens or not all(re.fullmatch(r"\d{3}", token) for token in tokens):
        return None
    return tokens


def load_suffix_rows() -> list[dict[str, str]]:
    with SUFFIX_ROWS.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_strict_corpus_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    seen = set()
    with METADATA.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            tokens = parse_tokens(row["text"])
            if tokens is None:
                continue
            key = (row["cisi"], row["site"], row["type"], row["symbol"], row["text"])
            if key in seen:
                continue
            seen.add(key)
            out: dict[str, object] = dict(row)
            out["_tokens"] = tokens
            rows.append(out)
    return rows


def select_units(suffix_rows: list[dict[str, str]]) -> list[str]:
    strict = [
        r
        for r in suffix_rows
        if r["scope"] == "all_002_strict_dedup" and r["tail_full"] != "<END>"
    ]
    counts = Counter(r["tail_full"] for r in strict)
    units = {tail for tail, count in counts.items() if count >= 2}
    units.update(EXTRA_UNITS)
    ordered = [unit for unit in UNIT_REVIEW_ORDER if unit in units]
    ordered.extend(sorted(unit for unit in units if unit not in UNIT_REVIEW_ORDER))
    return ordered


def find_unit_occurrences(rows: list[dict[str, object]], unit: str) -> list[dict[str, str]]:
    unit_tokens = unit.split()
    out: list[dict[str, str]] = []
    for row in rows:
        tokens = row["_tokens"]
        assert isinstance(tokens, list)
        for idx in range(0, len(tokens) - len(unit_tokens) + 1):
            if tokens[idx : idx + len(unit_tokens)] != unit_tokens:
                continue
            prev1 = tokens[idx - 1] if idx else "<START>"
            prev2 = " ".join(tokens[max(0, idx - 2) : idx]) if idx else "<START>"
            next1 = tokens[idx + len(unit_tokens)] if idx + len(unit_tokens) < len(tokens) else "<END>"
            out.append(
                {
                    "unit": unit,
                    "id": str(row["id"]),
                    "cisi": str(row["cisi"]),
                    "site": str(row["site"]),
                    "type": str(row["type"]),
                    "symbol": str(row["symbol"]),
                    "direction": str(row["dir."]),
                    "text": str(row["text"]),
                    "unit_index": str(idx),
                    "prev1": prev1,
                    "prev2": prev2,
                    "next1": next1,
                    "unit_terminal": str(next1 == "<END>").lower(),
                    "after_861": str(prev1 == "861").lower(),
                    "after_002_861": str(prev2 == "002 861").lower(),
                    "source_visible_tailed_focus": str(str(row["cisi"]) in SOURCE_VISIBLE_TAILED).lower(),
                }
            )
    return out


def short(row: dict[str, str]) -> str:
    return f"{row['cisi']} {row['text']}"


def summarize_unit(unit: str, suffix_rows: list[dict[str, str]], occurrences: list[dict[str, str]]) -> dict[str, str]:
    strict_tail_rows = [
        r
        for r in suffix_rows
        if r["scope"] == "all_002_strict_dedup" and r["tail_full"] == unit
    ]
    raw_tail_rows = [
        r
        for r in suffix_rows
        if r["scope"] == "all_002_strict_raw" and r["tail_full"] == unit
    ]
    bare_rows = [
        r
        for r in suffix_rows
        if r["scope"] == "all_002_strict_dedup" and r["tail_full"] == "<END>"
    ]
    after_002_861 = [r for r in occurrences if r["after_002_861"] == "true"]
    after_861 = [r for r in occurrences if r["after_861"] == "true"]
    non_861 = [r for r in occurrences if r["after_861"] != "true"]
    terminal = [r for r in occurrences if r["unit_terminal"] == "true"]
    source_focus = [r for r in occurrences if r["source_visible_tailed_focus"] == "true"]

    prefix_last2_keys = {r["prefix_last2"] for r in strict_tail_rows}
    prefix_last1_keys = {r["prefix_last1"] for r in strict_tail_rows}
    bare_l2 = [r for r in bare_rows if r["prefix_last2"] in prefix_last2_keys]
    bare_l1 = [r for r in bare_rows if r["prefix_last1"] in prefix_last1_keys]
    source_bare_l2 = [r for r in bare_l2 if r["cisi"] in SOURCE_VISIBLE_BARE]
    source_bare_l1 = [r for r in bare_l1 if r["cisi"] in SOURCE_VISIBLE_BARE]

    if occurrences and len(non_861) == 0 and len(after_002_861) == len(occurrences):
        distribution_class = "restricted_to_002_861_in_current_strict_layer"
    elif after_002_861 and non_861:
        distribution_class = "mixed_post_002_861_and_independent"
    elif after_861 and non_861:
        distribution_class = "mixed_after_861_and_independent"
    elif after_002_861:
        distribution_class = "post_002_861_only_in_current_scan"
    else:
        distribution_class = "not_current_post_002_861_tail"

    if bare_l2 or source_bare_l2:
        control_class = "matched_bare_controls_available"
    elif bare_l1 or source_bare_l1:
        control_class = "loose_bare_controls_available"
    else:
        control_class = "bare_controls_not_found_in_current_match"

    if distribution_class.startswith("restricted") and control_class != "bare_controls_not_found_in_current_match":
        evidence_role = "restricted_tail_with_bare_controls"
    elif "mixed" in distribution_class and control_class != "bare_controls_not_found_in_current_match":
        evidence_role = "mixed_tail_with_bare_controls"
    elif distribution_class.startswith("restricted"):
        evidence_role = "restricted_tail_control_weak"
    else:
        evidence_role = "broad_or_low_priority_distribution"

    return {
        "unit": unit,
        "strict_tail_rows_after_002_861": str(len(strict_tail_rows)),
        "raw_tail_rows_after_002_861": str(len(raw_tail_rows)),
        "occurrences_anywhere": str(len(occurrences)),
        "occurrences_after_861": str(len(after_861)),
        "occurrences_after_002_861": str(len(after_002_861)),
        "occurrences_non_861": str(len(non_861)),
        "terminal_occurrences": str(len(terminal)),
        "terminal_rate": f"{len(terminal)}/{len(occurrences)}" if occurrences else "0/0",
        "distribution_class": distribution_class,
        "prefix_last2_keys": ";".join(sorted(prefix_last2_keys)),
        "bare_prefix_last2_controls": str(len(bare_l2)),
        "source_visible_bare_prefix_last2_controls": ";".join(r["cisi"] for r in source_bare_l2),
        "bare_prefix_last1_controls": str(len(bare_l1)),
        "source_visible_bare_prefix_last1_controls": ";".join(r["cisi"] for r in source_bare_l1),
        "control_class": control_class,
        "evidence_role": evidence_role,
        "prev1_top_anywhere": ";".join(f"{k}:{v}" for k, v in Counter(r["prev1"] for r in occurrences).most_common(8)),
        "site_type_top_after_002_861": ";".join(
            f"{k}:{v}"
            for k, v in Counter(f"{r['site']}|{r['type']}|{r['symbol']}" for r in strict_tail_rows).most_common(8)
        ),
        "after_002_861_examples": ";".join(short(r) for r in after_002_861[:8]),
        "non_861_examples": ";".join(short(r) for r in non_861[:8]),
        "source_visible_tailed_examples": ";".join(short(r) for r in source_focus[:8]),
    }


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main() -> None:
    suffix_rows = load_suffix_rows()
    corpus_rows = load_strict_corpus_rows()
    units = select_units(suffix_rows)

    occurrence_rows: list[dict[str, str]] = []
    family_rows: list[dict[str, str]] = []
    for unit in units:
        occurrences = find_unit_occurrences(corpus_rows, unit)
        occurrence_rows.extend(occurrences)
        family_rows.append(summarize_unit(unit, suffix_rows, occurrences))

    family_rows.sort(
        key=lambda r: (
            UNIT_REVIEW_ORDER.index(r["unit"]) if r["unit"] in UNIT_REVIEW_ORDER else 999,
            r["unit"],
        )
    )

    family_csv = REPORTS / "campaign_032_002_861_tail_family_batch_families.csv"
    occurrence_csv = REPORTS / "campaign_032_002_861_tail_family_batch_occurrences.csv"
    summary_json = REPORTS / "campaign_032_002_861_tail_family_batch_summary.json"

    family_fields = list(family_rows[0].keys())
    occurrence_fields = list(occurrence_rows[0].keys())
    write_csv(family_csv, family_rows, family_fields)
    write_csv(occurrence_csv, occurrence_rows, occurrence_fields)

    summary = {
        "date": "2026-05-29",
        "strict_corpus_rows_scanned": len(corpus_rows),
        "tail_units": units,
        "family_rows": len(family_rows),
        "occurrence_rows": len(occurrence_rows),
        "priority_units": [
            {
                "unit": r["unit"],
                "evidence_role": r["evidence_role"],
                "distribution_class": r["distribution_class"],
                "strict_tail_rows_after_002_861": r["strict_tail_rows_after_002_861"],
                "occurrences_anywhere": r["occurrences_anywhere"],
                "source_visible_bare_prefix_last2_controls": r["source_visible_bare_prefix_last2_controls"],
            }
            for r in family_rows[:8]
        ],
        "family_csv": str(family_csv.resolve()),
        "occurrence_csv": str(occurrence_csv.resolve()),
    }
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
