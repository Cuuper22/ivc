"""Count how tightly eight candidate units attach to 861 across the corpus.

For each unit in UNITS — tail candidates like 603, 533-717, 255-416, raw
duplicate-family tails 416 and 698, and three 390-branch-head controls — this
script finds every occurrence in the strict fully-numeric corpus and records
what stands immediately before and after it. The key numbers per unit: how
often it follows 861, how often it follows the full 002-861 pair, and how
often it is terminal (ends the inscription). If a unit lives almost only
after 861, it behaves like an attached tail; if it roams freely, it is a
control or background sign. Writes an occurrences CSV, a summary CSV, and a
JSON payload.
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

UNITS = [
    ("603", ("603",), "861_strict_repeated_tail"),
    ("533-717", ("533", "717"), "861_strict_repeated_tail"),
    ("255-416", ("255", "416"), "861_adjacent_singleton_tail"),
    ("416", ("416",), "861_raw_duplicate_family_tail"),
    ("698", ("698",), "861_raw_duplicate_family_tail"),
    ("125", ("125",), "390_branch_head_control"),
    ("705", ("705",), "390_branch_head_control"),
    ("692", ("692",), "390_branch_head_control"),
]


def parse_tokens(text: str) -> list[str] | None:
    if not (text.startswith("+") and text.endswith("+")):
        return None
    if any(ch in text for ch in "[]()"):
        return None
    tokens = [token for token in text.strip("+").split("-") if token]
    if not tokens or not all(re.fullmatch(r"\d{3}", token) for token in tokens):
        return None
    return tokens


def load_strict_rows() -> list[dict[str, str]]:
    rows = []
    with METADATA.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            tokens = parse_tokens(row["text"])
            if tokens is None:
                continue
            out = dict(row)
            out["_tokens"] = tokens
            rows.append(out)
    return rows


def find_occurrences(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out = []
    for unit_name, unit_tokens, unit_class in UNITS:
        unit_len = len(unit_tokens)
        for row in rows:
            tokens = row["_tokens"]
            for idx in range(0, len(tokens) - unit_len + 1):
                if tuple(tokens[idx : idx + unit_len]) != unit_tokens:
                    continue
                prev1 = tokens[idx - 1] if idx > 0 else "<START>"
                prev2 = " ".join(tokens[max(0, idx - 2) : idx]) if idx > 0 else "<START>"
                next1 = tokens[idx + unit_len] if idx + unit_len < len(tokens) else "<END>"
                out.append(
                    {
                        "unit": unit_name,
                        "unit_class": unit_class,
                        "id": row["id"],
                        "cisi": row["cisi"],
                        "site": row["site"],
                        "type": row["type"],
                        "symbol": row["symbol"],
                        "direction": row["dir."],
                        "text": row["text"],
                        "unit_index": str(idx),
                        "prev1": prev1,
                        "prev2": prev2,
                        "next1": next1,
                        "unit_terminal": str(next1 == "<END>").lower(),
                        "after_861": str(prev1 == "861").lower(),
                        "after_002_861": str(prev2 == "002 861").lower(),
                    }
                )
    return out


def summarize(occurrences: list[dict[str, str]]) -> list[dict[str, str]]:
    out = []
    for unit_name, _, unit_class in UNITS:
        rows = [row for row in occurrences if row["unit"] == unit_name]
        after_861 = [row for row in rows if row["after_861"] == "true"]
        after_002_861 = [row for row in rows if row["after_002_861"] == "true"]
        terminal = [row for row in rows if row["unit_terminal"] == "true"]
        out.append(
            {
                "unit": unit_name,
                "unit_class": unit_class,
                "occurrences": str(len(rows)),
                "after_861": str(len(after_861)),
                "after_002_861": str(len(after_002_861)),
                "terminal": str(len(terminal)),
                "terminal_rate": f"{len(terminal)}/{len(rows)}" if rows else "0/0",
                "prev1_top": ";".join(f"{k}:{v}" for k, v in Counter(row["prev1"] for row in rows).most_common(10)),
                "next1_top": ";".join(f"{k}:{v}" for k, v in Counter(row["next1"] for row in rows).most_common(10)),
                "after_861_examples": ";".join(f"{row['cisi']} {row['text']}" for row in after_861[:10]),
                "non_861_examples": ";".join(f"{row['cisi']} prev={row['prev1']} next={row['next1']} {row['text']}" for row in rows if row["after_861"] != "true")[:800],
            }
        )
    return out


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main() -> None:
    rows = load_strict_rows()
    occurrences = find_occurrences(rows)
    summary_rows = summarize(occurrences)

    occurrence_csv = REPORTS / "campaign_032_002_861_tail_attachment_occurrences.csv"
    summary_csv = REPORTS / "campaign_032_002_861_tail_attachment_summary.csv"
    summary_json = REPORTS / "campaign_032_002_861_tail_attachment_summary.json"

    write_csv(
        occurrence_csv,
        occurrences,
        [
            "unit",
            "unit_class",
            "id",
            "cisi",
            "site",
            "type",
            "symbol",
            "direction",
            "text",
            "unit_index",
            "prev1",
            "prev2",
            "next1",
            "unit_terminal",
            "after_861",
            "after_002_861",
        ],
    )
    write_csv(
        summary_csv,
        summary_rows,
        [
            "unit",
            "unit_class",
            "occurrences",
            "after_861",
            "after_002_861",
            "terminal",
            "terminal_rate",
            "prev1_top",
            "next1_top",
            "after_861_examples",
            "non_861_examples",
        ],
    )
    payload = {
        "strict_rows_scanned": len(rows),
        "units": summary_rows,
        "occurrence_csv": str(occurrence_csv.resolve()),
        "summary_csv": str(summary_csv.resolve()),
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
