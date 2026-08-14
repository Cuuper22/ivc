"""Map the ecology of every tail that follows 002-861 in the strict corpus.

Instead of studying one tail at a time, this script takes every clean
inscription containing 002-861, extracts whatever follows the pair, and asks
of each tail family: how often does it appear here, how often does it appear
elsewhere in the corpus independently of 002-861, and how many distinct
register cells (site|type|symbol|shape) does it span? Each tail gets an
ecology class — bare closure background, mixed post-861-and-independent,
restricted repeated cell, singleton source target, or broad control — and a
priority rank for source acquisition. A manual override table keeps 533 717
weighted as one linguistic cell. Outputs: per-occurrence rows, per-tail
summary, priority ranking (three CSVs), and a JSON payload with the decision
that tail ecology replaces any single-tail reading.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path.cwd()
METADATA = ROOT / "data" / "open_prototype" / "lipi" / "metadata_filtered.csv"
REPORTS = ROOT / "data" / "open_prototype" / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

SOURCE_VISIBLE = {
    "M-355",
    "M-376",
    "M-391",
    "M-1267",
    "M-1273",
    "M-15",
    "M-77",
    "M-118",
    "M-723",
    "M-1044",
    "H-444",
}
SOURCE_PENDING_TARGET = {"M-1954", "M-1973"}
MANUAL_LINGUISTIC_WEIGHT_CELLS = {
    "533 717": 1,
}


def parse_tokens(text: str) -> list[str] | None:
    if not (text.startswith("+") and text.endswith("+")):
        return None
    if any(ch in text for ch in "[]()"):
        return None
    tokens = [token for token in text.strip("+").split("-") if token]
    if not tokens or not all(re.fullmatch(r"\d{3}", token) for token in tokens):
        return None
    return tokens


def load_rows() -> list[dict[str, object]]:
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


def tail_after_002_861(tokens: list[str]) -> tuple[int, list[str]] | None:
    for idx in range(len(tokens) - 1):
        if tokens[idx : idx + 2] == ["002", "861"]:
            return idx, tokens[idx + 2 :]
    return None


def occurrence_rows(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        tokens = row["_tokens"]
        assert isinstance(tokens, list)
        hit = tail_after_002_861(tokens)
        if hit is None:
            continue
        idx, tail = hit
        prefix = tokens[:idx]
        tail_text = " ".join(tail) if tail else "<END>"
        cisi = str(row["cisi"])
        register_key = "|".join([str(row["site"]), str(row["type"]), str(row["symbol"]), str(row["shape"])])
        out.append(
            {
                "id": str(row["id"]),
                "cisi": cisi,
                "site": str(row["site"]),
                "type": str(row["type"]),
                "symbol": str(row["symbol"]),
                "shape": str(row["shape"]),
                "class": str(row["class"]),
                "material": str(row["material"]),
                "condition": str(row["condition"]),
                "text_length": str(row["text length"]),
                "text": str(row["text"]),
                "prefix_last1": prefix[-1] if prefix else "<START>",
                "prefix_last2": " ".join(prefix[-2:]) if len(prefix) >= 2 else prefix[-1] if prefix else "<START>",
                "tail_after_002_861": tail_text,
                "tail_len": str(len(tail)),
                "tail_terminal": "true",
                "register_key": register_key,
                "source_status": "source_visible"
                if cisi in SOURCE_VISIBLE
                else "source_pending_target"
                if cisi in SOURCE_PENDING_TARGET
                else "source_pending_or_not_checked",
            }
        )
    return out


def contains_unit(tokens: list[str], unit: list[str]) -> list[int]:
    return [idx for idx in range(len(tokens) - len(unit) + 1) if tokens[idx : idx + len(unit)] == unit]


def independent_profile(rows: list[dict[str, object]], tail: str) -> dict[str, str]:
    if tail == "<END>":
        return {
            "occurs_anywhere": "",
            "independent_occurrences": "",
            "independent_registers": "",
            "independent_examples": "",
        }
    unit = tail.split()
    anywhere = []
    independent = []
    for row in rows:
        tokens = row["_tokens"]
        assert isinstance(tokens, list)
        for idx in contains_unit(tokens, unit):
            prev2 = tokens[idx - 2 : idx] if idx >= 2 else []
            hit_is_after_002_861 = prev2 == ["002", "861"]
            record = {
                "cisi": str(row["cisi"]),
                "site": str(row["site"]),
                "type": str(row["type"]),
                "symbol": str(row["symbol"]),
                "shape": str(row["shape"]),
                "text": str(row["text"]),
                "terminal": str(idx + len(unit) == len(tokens)).lower(),
            }
            anywhere.append(record)
            if not hit_is_after_002_861:
                independent.append(record)
    return {
        "occurs_anywhere": str(len(anywhere)),
        "independent_occurrences": str(len(independent)),
        "independent_registers": joined_counts(
            [f"{r['site']}|{r['type']}|{r['symbol']}|{r['shape']}" for r in independent], topn=8
        ),
        "independent_examples": ";".join(f"{r['cisi']} {r['text']}" for r in independent[:8]),
    }


def joined_counts(values: list[str], topn: int = 10) -> str:
    return ";".join(f"{key}:{value}" for key, value in Counter(values).most_common(topn))


def classify_tail(tail: str, group: list[dict[str, str]], independent_count: int, register_cells: int) -> str:
    rows = len(group)
    tail_len = int(group[0]["tail_len"])
    if tail == "<END>":
        return "bare_closure_background"
    if tail in {"416", "698", "000"} and independent_count > rows:
        return "broad_formula_or_background_control"
    if rows >= 2 and independent_count == 0 and register_cells <= 2:
        return "restricted_repeated_cell"
    if rows >= 2 and independent_count > 0:
        return "mixed_post861_and_independent"
    if tail_len > 1:
        return "singleton_complex_tail_source_target"
    return "singleton_simple_tail_source_target"


def summarize(rows: list[dict[str, str]], corpus_rows: list[dict[str, object]]) -> list[dict[str, str]]:
    by_tail: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_tail[row["tail_after_002_861"]].append(row)
    out: list[dict[str, str]] = []
    for tail, group in sorted(by_tail.items(), key=lambda item: (-len(item[1]), item[0])):
        register_cells = len({row["register_key"] for row in group})
        profile = independent_profile(corpus_rows, tail)
        independent_count = int(profile["independent_occurrences"] or 0)
        linguistic_weight_cells = MANUAL_LINGUISTIC_WEIGHT_CELLS.get(tail, register_cells)
        out.append(
            {
                "tail_after_002_861": tail,
                "rows": str(len(group)),
                "register_cells": str(register_cells),
                "linguistic_weight_cells": str(linguistic_weight_cells),
                "tail_len": group[0]["tail_len"],
                "source_visible_rows": str(sum(row["source_status"] == "source_visible" for row in group)),
                "source_pending_target_rows": str(sum(row["source_status"] == "source_pending_target" for row in group)),
                "site_counts": joined_counts([row["site"] for row in group]),
                "type_counts": joined_counts([row["type"] for row in group]),
                "symbol_counts": joined_counts([row["symbol"] for row in group]),
                "shape_counts": joined_counts([row["shape"] for row in group]),
                "class_counts": joined_counts([row["class"] for row in group]),
                "prefix_last2_counts": joined_counts([row["prefix_last2"] for row in group]),
                "tail_ecology_class": classify_tail(tail, group, independent_count, register_cells),
                **profile,
                "examples": ";".join(f"{row['cisi']} {row['text']}" for row in group[:10]),
            }
        )
    return out


def priority(summary: list[dict[str, str]]) -> list[dict[str, str]]:
    rank = {
        "mixed_post861_and_independent": 1,
        "restricted_repeated_cell": 2,
        "singleton_complex_tail_source_target": 3,
        "singleton_simple_tail_source_target": 4,
        "broad_formula_or_background_control": 5,
        "bare_closure_background": 6,
    }
    rows = [row for row in summary if row["tail_after_002_861"] != "<END>"]
    rows.sort(key=lambda row: (rank[row["tail_ecology_class"]], -int(row["rows"]), row["tail_after_002_861"]))
    for idx, row in enumerate(rows, 1):
        row["priority_rank"] = str(idx)
    return rows


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main() -> None:
    corpus_rows = load_rows()
    rows = occurrence_rows(corpus_rows)
    summary = summarize(rows, corpus_rows)
    priorities = priority([dict(row) for row in summary])

    rows_csv = REPORTS / "campaign_032_002_861_post861_tail_ecology_rows.csv"
    summary_csv = REPORTS / "campaign_032_002_861_post861_tail_ecology_summary.csv"
    priority_csv = REPORTS / "campaign_032_002_861_post861_tail_ecology_priority.csv"
    summary_json = REPORTS / "campaign_032_002_861_post861_tail_ecology_summary.json"

    write_csv(rows_csv, rows, list(rows[0].keys()))
    write_csv(summary_csv, summary, list(summary[0].keys()))
    write_csv(priority_csv, priorities, list(priorities[0].keys()))

    class_counts = Counter(row["tail_ecology_class"] for row in summary)
    payload = {
        "date": "2026-05-29",
        "strict_rows_scanned": len(corpus_rows),
        "rows_with_002_861": len(rows),
        "tail_families": len(summary),
        "tail_ecology_class_counts": dict(class_counts),
        "top_priority_tails": [
            {
                "tail": row["tail_after_002_861"],
                "class": row["tail_ecology_class"],
                "rows": int(row["rows"]),
                "linguistic_weight_cells": int(row["linguistic_weight_cells"]),
            }
            for row in priorities[:10]
        ],
        "decision": "post861_tail_ecology_replaces_single_tail_reading",
        "decision_basis": [
            "Bare 002-861 is the dominant background closure.",
            "Post-861 continuations split into mixed independent tails, restricted repeated cells, singleton source targets, and broad/background controls.",
            "533-717 is real but linguistically weighted as one narrow source/register-family cell.",
            "603 is currently the best mixed tail because it has post-861 rows and independent formula life.",
        ],
        "outputs": {
            "rows_csv": str(rows_csv.resolve()),
            "summary_csv": str(summary_csv.resolve()),
            "priority_csv": str(priority_csv.resolve()),
        },
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
