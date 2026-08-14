"""Find matched bare-terminal controls for six focus inscriptions with tails.

The focus rows (FOCUS_CISI) each carry a tail after 002-861. To know whether a
tail means anything, we need controls: inscriptions that end bare at 861 but
otherwise look the same. This script reads the suffix-split rows CSV and, for
each focus row, pulls every match at four levels of strictness — same
site/type/symbol, that plus the last prefix sign, same last-two prefix signs,
and same last-one prefix sign. It counts how many matches are bare terminals,
other focus tails, or other tails, and does the same per tail family (533 717,
603, 255 416). It writes a detail CSV, a per-focus summary CSV, a per-family
CSV, and a JSON summary with hand-picked key results.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
ROWS_IN = REPORTS / "campaign_032_002_861_suffix_split_rows.csv"

FOCUS_CISI = {"M-376", "M-391", "M-91", "M-240", "M-714", "M-1273"}

MATCH_LEVELS = [
    "site_type_symbol",
    "site_type_symbol_prefix_last1",
    "prefix_last2",
    "prefix_last1",
]


def read_rows() -> list[dict[str, str]]:
    with ROWS_IN.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return [r for r in rows if r["scope"] == "all_002_strict_dedup"]


def row_key(row: dict[str, str], level: str) -> str:
    if level == "site_type_symbol":
        return "|".join([row["site"], row["type"], row["symbol"]])
    if level == "site_type_symbol_prefix_last1":
        return "|".join([row["site"], row["type"], row["symbol"], row["prefix_last1"]])
    if level == "prefix_last2":
        return row["prefix_last2"]
    if level == "prefix_last1":
        return row["prefix_last1"]
    raise ValueError(level)


def row_class(row: dict[str, str]) -> str:
    if row["cisi"] in FOCUS_CISI:
        return "focus_tail"
    if row["terminal_861"].lower() == "true" and row["tail_len"] == "0":
        return "bare_terminal_002_861"
    if row["tail_len"] != "0":
        return f"other_tail_{row['tail_full'].replace(' ', '-')}"
    return "other"


def short(row: dict[str, str]) -> str:
    return f"{row['cisi']} {row['tail_full']} {row['text']}"


def main() -> None:
    rows = read_rows()
    focus = [r for r in rows if r["cisi"] in FOCUS_CISI]

    detail_rows: list[dict[str, str]] = []
    summary_rows: list[dict[str, str]] = []

    for f in focus:
        for level in MATCH_LEVELS:
            key = row_key(f, level)
            matches = [r for r in rows if row_key(r, level) == key]
            bare = [r for r in matches if row_class(r) == "bare_terminal_002_861"]
            focus_matches = [r for r in matches if r["cisi"] in FOCUS_CISI]
            other_tails = [r for r in matches if r["tail_len"] != "0" and r["cisi"] not in FOCUS_CISI]
            for m in matches:
                detail_rows.append(
                    {
                        "focus_cisi": f["cisi"],
                        "focus_tail": f["tail_full"],
                        "focus_text": f["text"],
                        "match_level": level,
                        "match_key": key,
                        "match_cisi": m["cisi"],
                        "match_id": m["id"],
                        "match_class": row_class(m),
                        "site": m["site"],
                        "type": m["type"],
                        "symbol": m["symbol"],
                        "prefix_last1": m["prefix_last1"],
                        "prefix_last2": m["prefix_last2"],
                        "tail_len": m["tail_len"],
                        "tail_full": m["tail_full"],
                        "terminal_861": m["terminal_861"],
                        "text": m["text"],
                    }
                )
            summary_rows.append(
                {
                    "focus_cisi": f["cisi"],
                    "focus_tail": f["tail_full"],
                    "focus_prefix_last1": f["prefix_last1"],
                    "focus_prefix_last2": f["prefix_last2"],
                    "focus_site_type_symbol": row_key(f, "site_type_symbol"),
                    "match_level": level,
                    "match_key": key,
                    "matched_rows": str(len(matches)),
                    "bare_terminal_controls": str(len(bare)),
                    "focus_tail_rows_in_block": str(len(focus_matches)),
                    "other_tail_rows_in_block": str(len(other_tails)),
                    "bare_terminal_examples": ";".join(short(r) for r in bare[:8]),
                    "focus_tail_examples": ";".join(short(r) for r in focus_matches[:8]),
                    "other_tail_examples": ";".join(short(r) for r in other_tails[:8]),
                }
            )

    family_rows: list[dict[str, str]] = []
    for family in ["533 717", "603", "255 416"]:
        members = [r for r in focus if r["tail_full"] == family]
        if not members:
            continue
        for level in ["site_type_symbol", "prefix_last2", "prefix_last1"]:
            keys = sorted({row_key(r, level) for r in members})
            matches = [r for r in rows if row_key(r, level) in keys]
            bare = [r for r in matches if row_class(r) == "bare_terminal_002_861"]
            focus_matches = [r for r in matches if r["cisi"] in FOCUS_CISI]
            other_tails = [r for r in matches if r["tail_len"] != "0" and r["cisi"] not in FOCUS_CISI]
            family_rows.append(
                {
                    "tail_family": family,
                    "match_level": level,
                    "match_keys": ";".join(keys),
                    "matched_rows": str(len(matches)),
                    "bare_terminal_controls": str(len(bare)),
                    "focus_tail_rows_in_block": str(len(focus_matches)),
                    "other_tail_rows_in_block": str(len(other_tails)),
                    "bare_terminal_examples": ";".join(short(r) for r in bare[:10]),
                    "focus_tail_examples": ";".join(short(r) for r in focus_matches[:10]),
                    "other_tail_examples": ";".join(short(r) for r in other_tails[:10]),
                }
            )

    detail_path = REPORTS / "campaign_032_002_861_matched_terminal_controls_rows.csv"
    summary_path = REPORTS / "campaign_032_002_861_matched_terminal_controls_summary.csv"
    family_path = REPORTS / "campaign_032_002_861_matched_terminal_controls_families.csv"
    json_path = REPORTS / "campaign_032_002_861_matched_terminal_controls_summary.json"

    with detail_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(detail_rows[0].keys()))
        writer.writeheader()
        writer.writerows(detail_rows)

    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    with family_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(family_rows[0].keys()))
        writer.writeheader()
        writer.writerows(family_rows)

    def find_summary(focus_cisi: str, level: str) -> dict[str, str]:
        return next(r for r in summary_rows if r["focus_cisi"] == focus_cisi and r["match_level"] == level)

    key_results = {
        "M-376_prefix_last1_176": find_summary("M-376", "prefix_last1"),
        "M-391_site_type_symbol": find_summary("M-391", "site_type_symbol"),
        "M-91_prefix_last2_220_032": find_summary("M-91", "prefix_last2"),
        "M-240_prefix_last2_220_032": find_summary("M-240", "prefix_last2"),
        "M-714_prefix_last1_803": find_summary("M-714", "prefix_last1"),
        "M-1273_site_type_symbol": find_summary("M-1273", "site_type_symbol"),
    }

    summary = {
        "input_rows": len(rows),
        "focus_rows": [r["cisi"] for r in focus],
        "match_levels": MATCH_LEVELS,
        "detail_rows": len(detail_rows),
        "summary_rows": len(summary_rows),
        "family_rows": len(family_rows),
        "key_results": key_results,
        "detail_csv": str(detail_path.resolve()),
        "summary_csv": str(summary_path.resolve()),
        "family_csv": str(family_path.resolve()),
    }
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
