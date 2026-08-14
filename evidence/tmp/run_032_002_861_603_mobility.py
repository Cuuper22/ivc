"""Mobility scan for sign 603: where does it sit, and does position vary?

This script reads the filtered corpus metadata, keeps clean strict rows (bracketed by
+ with all three-digit tokens and no damage markers), and records every position in
which 603 appears, treating M-240, M-714, and M-1273 as the source-visible witnesses.
"Mobility" means the sign shows up in more than one structural slot rather than being
frozen to a single formula position. It writes a rows CSV, a summary CSV, and a
summary JSON. The recorded decision: 603 mobility is live but not yet a value — the
positional behavior is a real research object, but no reading is accepted.
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
REPORTS.mkdir(parents=True, exist_ok=True)

SOURCE_VISIBLE = {
    "M-240",
    "M-714",
    "M-1273",
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


def joined_counts(values: list[str], topn: int = 12) -> str:
    return ";".join(f"{key}:{value}" for key, value in Counter(values).most_common(topn))


def classify_603(tokens: list[str], idx: int) -> str:
    prev2 = tokens[idx - 2 : idx] if idx >= 2 else []
    if prev2 == ["002", "861"]:
        return "post_002_861_terminal_tail"
    if idx == 1 and tokens[0] == "740" and tokens[idx + 1 : idx + 4] == ["240", "060", "692"]:
        return "independent_740_603_240_060_692_lane"
    return "independent_other"


def occurrence_rows(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        tokens = row["_tokens"]
        assert isinstance(tokens, list)
        for idx, token in enumerate(tokens):
            if token != "603":
                continue
            prev_tokens = tokens[max(0, idx - 4) : idx]
            next_tokens = tokens[idx + 1 : idx + 5]
            post_861_context = tokens[idx - 2 : idx] == ["002", "861"] if idx >= 2 else False
            before_002_861 = ""
            if post_861_context:
                before = tokens[: idx - 2]
                before_002_861 = " ".join(before[-2:]) if len(before) >= 2 else " ".join(before) if before else "<START>"
            out.append(
                {
                    "id": str(row["id"]),
                    "cisi": str(row["cisi"]),
                    "site": str(row["site"]),
                    "type": str(row["type"]),
                    "symbol": str(row["symbol"]),
                    "shape": str(row["shape"]),
                    "class": str(row["class"]),
                    "material": str(row["material"]),
                    "condition": str(row["condition"]),
                    "dir": str(row["dir."]),
                    "text_length": str(row["text length"]),
                    "text": str(row["text"]),
                    "occurrence_index_0based": str(idx),
                    "position_share": f"{idx / (len(tokens) - 1):.6f}" if len(tokens) > 1 else "0.000000",
                    "is_terminal": str(idx == len(tokens) - 1).lower(),
                    "prev1": tokens[idx - 1] if idx else "<START>",
                    "prev2": " ".join(tokens[idx - 2 : idx]) if idx >= 2 else tokens[idx - 1] if idx else "<START>",
                    "next1": tokens[idx + 1] if idx + 1 < len(tokens) else "<END>",
                    "next2": " ".join(tokens[idx + 1 : idx + 3]) if idx + 2 < len(tokens) else tokens[idx + 1] if idx + 1 < len(tokens) else "<END>",
                    "prev_window": " ".join(prev_tokens) if prev_tokens else "<START>",
                    "next_window": " ".join(next_tokens) if next_tokens else "<END>",
                    "before_002_861": before_002_861,
                    "mobility_class": classify_603(tokens, idx),
                    "source_status": "source_visible_or_routed" if str(row["cisi"]) in SOURCE_VISIBLE else "source_not_checked_in_this_campaign",
                    "register_key": "|".join([str(row["site"]), str(row["type"]), str(row["symbol"]), str(row["shape"])]),
                    "formula_key": str(row["text"]),
                }
            )
    return out


def summarize(occurrences: list[dict[str, str]], strict_rows_scanned: int) -> dict[str, object]:
    by_class = Counter(row["mobility_class"] for row in occurrences)
    post = [row for row in occurrences if row["mobility_class"] == "post_002_861_terminal_tail"]
    independent = [row for row in occurrences if row["mobility_class"] != "post_002_861_terminal_tail"]
    lane = [row for row in occurrences if row["mobility_class"] == "independent_740_603_240_060_692_lane"]
    other = [row for row in occurrences if row["mobility_class"] == "independent_other"]
    return {
        "date": "2026-05-29",
        "strict_rows_scanned": strict_rows_scanned,
        "rows_with_603_occurrence": len({row["cisi"] + "|" + row["text"] for row in occurrences}),
        "603_occurrences": len(occurrences),
        "mobility_class_counts": dict(by_class),
        "post_002_861": {
            "rows": len(post),
            "register_cells": len({row["register_key"] for row in post}),
            "prefix_before_002_861": joined_counts([row["before_002_861"] for row in post]),
            "site_type_symbol_shape": joined_counts([row["register_key"] for row in post]),
            "examples": [f"{row['cisi']} {row['text']}" for row in post],
        },
        "independent": {
            "rows": len(independent),
            "exact_formula_families": len({row["formula_key"] for row in independent}),
            "register_cells": len({row["register_key"] for row in independent}),
            "lane_740_603_240_060_692_rows": len(lane),
            "other_independent_rows": len(other),
            "site_type_symbol_shape": joined_counts([row["register_key"] for row in independent]),
            "examples": [f"{row['cisi']} {row['text']}" for row in independent],
        },
        "decision": "603_mobility_is_live_but_not_yet_a_value",
        "decision_basis": [
            "Post-861 603 is terminal in three Mohenjo-daro seal rows across three register cells.",
            "Independent 603 is dominated by one repeated Harappa TAB:B formula lane plus one weak scene/control row.",
            "The bridge is real enough to prioritize, but not clean enough to call 603 a value or translation.",
        ],
        "next_campaign": "source_layout_and_neighbor_ecology_for_603",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = load_rows()
    occurrences = occurrence_rows(rows)

    rows_csv = REPORTS / "campaign_032_002_861_603_mobility_rows.csv"
    summary_json = REPORTS / "campaign_032_002_861_603_mobility_summary.json"
    summary_csv = REPORTS / "campaign_032_002_861_603_mobility_summary.csv"

    write_csv(rows_csv, occurrences)
    payload = summarize(occurrences, len(rows))
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    flat = [
        {
            "metric": "strict_rows_scanned",
            "value": str(payload["strict_rows_scanned"]),
        },
        {
            "metric": "603_occurrences",
            "value": str(payload["603_occurrences"]),
        },
        {
            "metric": "post_002_861_rows",
            "value": str(payload["post_002_861"]["rows"]),
        },
        {
            "metric": "independent_rows",
            "value": str(payload["independent"]["rows"]),
        },
        {
            "metric": "independent_exact_formula_families",
            "value": str(payload["independent"]["exact_formula_families"]),
        },
        {
            "metric": "decision",
            "value": str(payload["decision"]),
        },
    ]
    write_csv(summary_csv, flat)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
