"""Ask whether specific preframes before 002-861 predict which tail follows.

A preframe is the last one or two signs that come right before the 002-861
pair. This script scans the strict corpus for every 002-861 occurrence,
records its preframe and its tail (bare, 533 717, 603, or other), and then
summarizes tail choice inside seven focus last-two frames and seven focus
last-one frames. If a preframe reliably picked one tail, that would be
grammar-shaped evidence; the recorded decision is that the target last-two
frames are singletons and the last-one frames are context clues, not values.
Writes a rows CSV, a last2 summary CSV, a last1 summary CSV, and a JSON
summary with the decision.
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

FOCUS_LAST2 = {"100 176", "233 805", "740 055", "231 235", "720 175", "233 550", "415 798"}
FOCUS_LAST1 = {"176", "805", "055", "235", "175", "550", "798"}


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


def hit_row(row: dict[str, object]) -> dict[str, str] | None:
    tokens = row["_tokens"]
    assert isinstance(tokens, list)
    for idx in range(len(tokens) - 1):
        if tokens[idx : idx + 2] != ["002", "861"]:
            continue
        prefix = tokens[:idx]
        tail = tokens[idx + 2 :]
        prefix_last1 = prefix[-1] if prefix else "<START>"
        prefix_last2 = " ".join(prefix[-2:]) if len(prefix) >= 2 else prefix_last1
        tail_text = " ".join(tail) if tail else "<END>"
        return {
            "id": str(row["id"]),
            "cisi": str(row["cisi"]),
            "site": str(row["site"]),
            "type": str(row["type"]),
            "symbol": str(row["symbol"]),
            "shape": str(row["shape"]),
            "class": str(row["class"]),
            "text_length": str(row["text length"]),
            "text": str(row["text"]),
            "prefix_last1": prefix_last1,
            "prefix_last2": prefix_last2,
            "tail_after_002_861": tail_text,
            "tail_class": "bare"
            if tail_text == "<END>"
            else "target_533_717"
            if tail_text == "533 717"
            else "short_alt_603"
            if tail_text == "603"
            else "other_tail",
            "focus_last1": str(prefix_last1 in FOCUS_LAST1).lower(),
            "focus_last2": str(prefix_last2 in FOCUS_LAST2).lower(),
        }
    return None


def joined_counts(values: list[str], topn: int = 12) -> str:
    return ";".join(f"{key}:{value}" for key, value in Counter(values).most_common(topn))


def summarize(rows: list[dict[str, str]], key: str, focus_set: set[str]) -> list[dict[str, str]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row[key] in focus_set:
            groups[row[key]].append(row)
    out: list[dict[str, str]] = []
    for value in sorted(groups):
        group = groups[value]
        out.append(
            {
                "frame_type": key,
                "frame": value,
                "rows": str(len(group)),
                "tail_counts": joined_counts([row["tail_after_002_861"] for row in group]),
                "tail_class_counts": joined_counts([row["tail_class"] for row in group]),
                "site_counts": joined_counts([row["site"] for row in group]),
                "type_counts": joined_counts([row["type"] for row in group]),
                "shape_counts": joined_counts([row["shape"] for row in group]),
                "examples": ";".join(f"{row['cisi']} {row['text']}" for row in group[:10]),
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
    rows = [hit for row in load_rows() if (hit := hit_row(row)) is not None]
    last2_summary = summarize(rows, "prefix_last2", FOCUS_LAST2)
    last1_summary = summarize(rows, "prefix_last1", FOCUS_LAST1)

    rows_csv = REPORTS / "campaign_032_002_861_preframe_tail_comparison_rows.csv"
    last2_csv = REPORTS / "campaign_032_002_861_preframe_tail_comparison_last2.csv"
    last1_csv = REPORTS / "campaign_032_002_861_preframe_tail_comparison_last1.csv"
    summary_json = REPORTS / "campaign_032_002_861_preframe_tail_comparison_summary.json"

    write_csv(rows_csv, rows, list(rows[0].keys()))
    write_csv(last2_csv, last2_summary, list(last2_summary[0].keys()))
    write_csv(last1_csv, last1_summary, list(last1_summary[0].keys()))

    target_last2 = [row for row in last2_summary if row["frame"] in {"100 176", "233 805"}]
    target_last1 = [row for row in last1_summary if row["frame"] in {"176", "805"}]
    payload = {
        "date": "2026-05-29",
        "rows_with_002_861": len(rows),
        "focus_last2_frames": len(last2_summary),
        "focus_last1_frames": len(last1_summary),
        "target_last2_rows": {row["frame"]: int(row["rows"]) for row in target_last2},
        "target_last1_rows": {row["frame"]: int(row["rows"]) for row in target_last1},
        "decision": "target_last2_frames_are_singletons_last1_frames_are_context_clues_not_values",
        "decision_basis": [
            "The two target last2 frames occur as singletons in the strict 002-861 layer.",
            "The broader last1 frames give context clues but do not isolate 533-717 as a value.",
            "Preframe behavior should guide the next batch, not justify translation.",
        ],
        "outputs": {
            "rows_csv": str(rows_csv.resolve()),
            "last2_csv": str(last2_csv.resolve()),
            "last1_csv": str(last1_csv.resolve()),
        },
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
