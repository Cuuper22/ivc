"""Metadata contrast between the 533 and 717 focus rows.

This script reads the focus rows from the tail-rarity register scan and compares the
two groups across a fixed list of metadata features (shape, text length, the last one
and two signs before 002-861, and source status). The question is whether plain
catalog metadata already
separates the 533 rows from the 717 rows — if it did, the contrast would be a register
artifact rather than a sign-choice contrast. It writes per-row and per-feature CSVs
plus a summary JSON. The recorded decision: metadata features do not separate 533-717
cleanly.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
FOCUS = REPORTS / "campaign_032_002_861_tail_rarity_register_scan_focus_rows.csv"


FEATURES = [
    "shape",
    "text_length",
    "prefix_before_002_861_last1",
    "prefix_before_002_861_last2",
    "source_status",
]


def load_focus() -> list[dict[str, str]]:
    with FOCUS.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def tail_class(row: dict[str, str]) -> str:
    tail = row["tail_after_002_861"]
    if tail == "533 717":
        return "target_533_717"
    if tail == "<END>":
        return "bare"
    if tail == "603":
        return "short_alt_603"
    return "long_alt_tail"


def joined_counts(values: list[str]) -> str:
    return ";".join(f"{key}:{value}" for key, value in Counter(values).most_common())


def feature_contrasts(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    targets = [row for row in rows if tail_class(row) == "target_533_717"]
    controls = [row for row in rows if tail_class(row) != "target_533_717"]
    out: list[dict[str, str]] = []
    for feature in FEATURES:
        target_values = Counter(row[feature] for row in targets)
        control_values = Counter(row[feature] for row in controls)
        for value in sorted(set(target_values) | set(control_values)):
            target_rows = [row["cisi"] for row in targets if row[feature] == value]
            control_rows = [row["cisi"] for row in controls if row[feature] == value]
            out.append(
                {
                    "feature": feature,
                    "value": value,
                    "target_rows": str(len(target_rows)),
                    "control_rows": str(len(control_rows)),
                    "target_cisis": ";".join(target_rows),
                    "control_cisis": ";".join(control_rows),
                    "contrast_status": "target_specific_singleton_or_pair"
                    if target_rows and not control_rows
                    else "hostile_shared_with_controls"
                    if target_rows and control_rows
                    else "control_only",
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
    rows = load_focus()
    for row in rows:
        row["tail_class"] = tail_class(row)

    contrasts = feature_contrasts(rows)
    target_rows = [row for row in rows if row["tail_class"] == "target_533_717"]
    control_rows = [row for row in rows if row["tail_class"] != "target_533_717"]

    focus_out = REPORTS / "campaign_032_002_861_533717_focus_contrast_rows.csv"
    contrast_out = REPORTS / "campaign_032_002_861_533717_focus_contrast_features.csv"
    summary_out = REPORTS / "campaign_032_002_861_533717_focus_contrast_summary.json"

    write_csv(focus_out, rows, list(rows[0].keys()))
    write_csv(contrast_out, contrasts, list(contrasts[0].keys()))

    payload = {
        "date": "2026-05-29",
        "focus_rows": len(rows),
        "target_rows": [row["cisi"] for row in target_rows],
        "control_rows": [row["cisi"] for row in control_rows],
        "tail_class_counts": dict(Counter(row["tail_class"] for row in rows)),
        "shape_counts_by_tail_class": {
            klass: joined_counts([row["shape"] for row in rows if row["tail_class"] == klass])
            for klass in sorted({row["tail_class"] for row in rows})
        },
        "length_counts_by_tail_class": {
            klass: joined_counts([row["text_length"] for row in rows if row["tail_class"] == klass])
            for klass in sorted({row["tail_class"] for row in rows})
        },
        "hostile_controls": [
            "M-355 shares cuboid-convex no-icon SEAL:R status with the target rows but takes long tail 360-520-919-140.",
            "M-1267 shares length 7 with M-376 but is bare after 002-861.",
            "M-1954 shares length 12 with M-391 but is bare after 002-861 and remains source-pending.",
            "M-1273 shares the same broad register but takes 603.",
        ],
        "decision": "metadata_features_do_not_separate_533_717_cleanly",
        "next_decision_question": "Use source layout and source-family independence to decide whether M-376/M-391 form a real subclass or a tiny copy/source-family cell.",
        "outputs": {
            "focus_rows_csv": str(focus_out.resolve()),
            "features_csv": str(contrast_out.resolve()),
        },
    }
    summary_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
