"""Looks for a source-layout feature that uniquely separates the 533-717 targets.

This script reads the source-token attachment boxes and the 533-717 source-family
independence rows, plus an inline table of qualitative layout controls. It asks
whether any measurable layout property of the visible source bands — box geometry,
spacing, band composition — discriminates the 533-717 targets from their same-register
controls. It writes a rows CSV and a summary JSON. The recorded decision: no unique
source-layout discriminator yet, so layout alone cannot currently carry the 533-717
contrast.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
BOXES = REPORTS / "campaign_032_002_861_source_token_attachment_boxes.csv"
FOCUS = REPORTS / "campaign_032_002_861_533717_source_family_independence_rows.csv"

QUALITATIVE_CONTROLS = {
    "M-355": {
        "layout_status": "same_line_long_tail_control",
        "layout_observation": "Source-visible no-icon cuboid-convex row has a continuous terminal-side long tail after 002-861; no unique 533-717-only layout feature is visible from the current crop.",
    },
    "M-1267": {
        "layout_status": "same_line_bare_edge_control",
        "layout_observation": "Source-visible no-icon rectangular row has a visible terminal edge after 002-861 without 533-717.",
    },
}


def load_focus() -> dict[str, dict[str, str]]:
    with FOCUS.open(newline="", encoding="utf-8") as handle:
        return {row["cisi"]: row for row in csv.DictReader(handle)}


def load_boxes() -> dict[str, dict[str, dict[str, int]]]:
    boxes: dict[str, dict[str, dict[str, int]]] = {}
    with BOXES.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            boxes.setdefault(row["cisi"], {})[row["box_role"]] = {
                "x1": int(row["x1"]),
                "y1": int(row["y1"]),
                "x2": int(row["x2"]),
                "y2": int(row["y2"]),
            }
    return boxes


def metric_rows(focus: dict[str, dict[str, str]], boxes: dict[str, dict[str, dict[str, int]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for cisi, by_role in boxes.items():
        if cisi not in focus or "line_window" not in by_role or "tail_window" not in by_role:
            continue
        line = by_role["line_window"]
        tail = by_role["tail_window"]
        line_width = line["x2"] - line["x1"]
        tail_width = tail["x2"] - tail["x1"]
        tail_start_share = (tail["x1"] - line["x1"]) / line_width if line_width else 0
        tail_width_share = tail_width / line_width if line_width else 0
        rows.append(
            {
                "cisi": cisi,
                "tail_class": focus[cisi]["tail_class"],
                "text": focus[cisi]["text"],
                "line_width_px": str(line_width),
                "tail_width_px": str(tail_width),
                "tail_start_share_of_line": f"{tail_start_share:.3f}",
                "tail_width_share_of_line": f"{tail_width_share:.3f}",
                "layout_status": "quantified_existing_overlay",
                "layout_observation": "tail window lies in the terminal-side part of the same source-visible line",
            }
        )
    for cisi, qualitative in QUALITATIVE_CONTROLS.items():
        row = focus[cisi]
        rows.append(
            {
                "cisi": cisi,
                "tail_class": row["tail_class"],
                "text": row["text"],
                "line_width_px": "",
                "tail_width_px": "",
                "tail_start_share_of_line": "",
                "tail_width_share_of_line": "",
                "layout_status": qualitative["layout_status"],
                "layout_observation": qualitative["layout_observation"],
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main() -> None:
    focus = load_focus()
    boxes = load_boxes()
    rows = metric_rows(focus, boxes)

    rows_out = REPORTS / "campaign_032_002_861_533717_source_layout_discriminator_rows.csv"
    summary_out = REPORTS / "campaign_032_002_861_533717_source_layout_discriminator_summary.json"
    write_csv(rows_out, rows, list(rows[0].keys()))

    target_rows = [row for row in rows if row["tail_class"] == "target_533_717"]
    quantified_controls = [row for row in rows if row["tail_class"] != "target_533_717" and row["line_width_px"]]
    payload = {
        "date": "2026-05-29",
        "rows": len(rows),
        "quantified_rows": sum(1 for row in rows if row["line_width_px"]),
        "target_tail_start_share_range": [
            min(row["tail_start_share_of_line"] for row in target_rows),
            max(row["tail_start_share_of_line"] for row in target_rows),
        ],
        "target_tail_width_share_range": [
            min(row["tail_width_share_of_line"] for row in target_rows),
            max(row["tail_width_share_of_line"] for row in target_rows),
        ],
        "quantified_control_tail_start_shares": {
            row["cisi"]: row["tail_start_share_of_line"] for row in quantified_controls
        },
        "decision": "no_unique_source_layout_discriminator_yet",
        "decision_basis": [
            "M-376 and M-391 both show same-line terminal-side 533-717 windows.",
            "M-1273 also shows same-line terminal-side post-861 material, so same-line terminal placement is not unique to 533-717.",
            "M-355 gives a source-visible cuboid-convex same-register long-tail control.",
            "M-1267 gives a source-visible same-register bare-edge control.",
        ],
        "outputs": {"rows_csv": str(rows_out.resolve())},
    }
    summary_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
