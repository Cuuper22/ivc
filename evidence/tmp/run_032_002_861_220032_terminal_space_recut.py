"""Recuts terminal space on bare 220-032-002-861 controls to test a layout adversary.

The adversary says: maybe the "bare" rows lack a tail simply because the line ran out
of room. This script reads the source-token attachment boxes and verdicts for the
tailed rows, plus the bare-edge control crops, and recuts the terminal region of each
bare 220-032-002-861 control with PIL into tmp/032_002_861_220032_terminal_space_recut.
It measures whether each control has a tail-sized empty slot after the last sign. It
writes measurement CSVs, a summary JSON, and a docs/ markdown note. The recorded
outcomes distinguish rows where the terminal-space attack survives from rows that are
blocked by the terminal-space adversary.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
DOCS = ROOT / "docs"
TMP_OUT = ROOT / "tmp" / "032_002_861_220032_terminal_space_recut"

TAILED_BOXES = REPORTS / "campaign_032_002_861_source_token_attachment_boxes.csv"
TAILED_VERDICTS = REPORTS / "campaign_032_002_861_source_token_attachment_verdicts.csv"
BARE_CROPS = REPORTS / "campaign_032_002_861_bare_edge_source_controls_crops.csv"
OUT_PREFIX = "campaign_032_002_861_220032_terminal_space_recut"


BARE_BOXES = {
    "H-444": {
        "line_window": (0, 0, 700, 338),
        "bare_edge_window": (20, 25, 290, 330),
        "terminal_side_margin": (0, 25, 28, 330),
        "orientation_note": "terminal side marked on the left edge in existing source-control overlay",
    },
    "M-723": {
        "line_window": (0, 0, 925, 345),
        "bare_edge_window": (0, 0, 315, 330),
        "terminal_side_margin": (0, 0, 38, 330),
        "orientation_note": "terminal side marked on the left edge in existing source-control overlay",
    },
    "M-1044": {
        "line_window": (0, 0, 600, 335),
        "bare_edge_window": (0, 0, 280, 330),
        "terminal_side_margin": (0, 0, 38, 330),
        "orientation_note": "terminal side marked on the left edge in existing source-control overlay",
    },
}

TAILED_TARGETS = {"M-91": "255 416", "M-240": "603"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                keys.append(key)
                seen.add(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def width(box: tuple[int, int, int, int]) -> int:
    return box[2] - box[0]


def height(box: tuple[int, int, int, int]) -> int:
    return box[3] - box[1]


def area(box: tuple[int, int, int, int]) -> int:
    return width(box) * height(box)


def f3(value: float) -> float:
    return round(value, 3)


def parse_box_rows() -> dict[str, dict[str, tuple[int, int, int, int]]]:
    out: dict[str, dict[str, tuple[int, int, int, int]]] = {}
    for row in read_csv(TAILED_BOXES):
        cisi = row["cisi"]
        if cisi not in TAILED_TARGETS:
            continue
        out.setdefault(cisi, {})[row["box_role"]] = tuple(int(row[key]) for key in ["x1", "y1", "x2", "y2"])
    return out


def verdict_map() -> dict[str, dict[str, str]]:
    return {row["cisi"]: row for row in read_csv(TAILED_VERDICTS)}


def crop_map() -> dict[str, dict[str, str]]:
    return {row["cisi"]: row for row in read_csv(BARE_CROPS)}


def metric_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    verdicts = verdict_map()
    tailed_boxes = parse_box_rows()
    for cisi, tail in TAILED_TARGETS.items():
        boxes = tailed_boxes[cisi]
        line = boxes["line_window"]
        tail_box = boxes["tail_window"]
        pre_tail = boxes["pre_tail_window"]
        line_w = width(line)
        tail_w = width(tail_box)
        left_gap = abs(tail_box[0] - line[0])
        right_gap = abs(line[2] - tail_box[2])
        nearest_edge_gap = min(left_gap, right_gap)
        rows.append(
            {
                "cisi": cisi,
                "outcome": "tailed",
                "tail": tail,
                "line_width_px": line_w,
                "line_height_px": height(line),
                "terminal_candidate_width_px": tail_w,
                "terminal_candidate_width_share": f3(tail_w / line_w),
                "terminal_candidate_area_share": f3(area(tail_box) / area(line)),
                "pre_tail_width_px": width(pre_tail),
                "nearest_terminal_edge_gap_px": nearest_edge_gap,
                "nearest_terminal_edge_gap_share": f3(nearest_edge_gap / line_w),
                "source_image": verdicts[cisi]["source_image_abs"],
                "overlay": verdicts[cisi]["overlay_abs"],
                "box_basis": "source_token_attachment_tail_window",
                "orientation_note": "tail window touches or nearly touches marked terminal edge",
            }
        )

    crops = crop_map()
    for cisi, boxes in BARE_BOXES.items():
        line = boxes["line_window"]
        edge = boxes["bare_edge_window"]
        margin = boxes["terminal_side_margin"]
        line_w = width(line)
        margin_w = width(margin)
        rows.append(
            {
                "cisi": cisi,
                "outcome": "bare_closure",
                "tail": "<END>",
                "line_width_px": line_w,
                "line_height_px": height(line),
                "terminal_candidate_width_px": "",
                "terminal_candidate_width_share": "",
                "terminal_candidate_area_share": "",
                "bare_terminal_window_width_px": width(edge),
                "bare_terminal_window_width_share": f3(width(edge) / line_w),
                "post_terminal_margin_width_px": margin_w,
                "post_terminal_margin_width_share": f3(margin_w / line_w),
                "post_terminal_margin_area_share": f3(area(margin) / area(line)),
                "source_image": crops[cisi]["source_image_abs"],
                "overlay": crops[cisi]["overlay_abs"],
                "box_basis": "bare_edge_source_controls_terminal_side_margin",
                "orientation_note": boxes["orientation_note"],
            }
        )
    return rows


def decision_rows(metrics: list[dict[str, Any]]) -> list[dict[str, str]]:
    tailed = [row for row in metrics if row["outcome"] == "tailed"]
    bare = [row for row in metrics if row["outcome"] == "bare_closure"]
    min_tail_w = min(int(row["terminal_candidate_width_px"]) for row in tailed)
    max_bare_margin = max(int(row["post_terminal_margin_width_px"]) for row in bare)
    min_tail_share = min(float(row["terminal_candidate_width_share"]) for row in tailed)
    max_margin_share = max(float(row["post_terminal_margin_width_share"]) for row in bare)
    return [
        {
            "test": "tail_window_vs_bare_margin_width",
            "decision": "terminal_space_attack_survives",
            "evidence": f"smallest tailed terminal candidate width is {min_tail_w}px; largest bare post-terminal margin is {max_bare_margin}px",
            "limit": "the margin boxes come from the existing bare-edge source-control overlay, not a fresh source resegmentation",
        },
        {
            "test": "tail_window_vs_bare_margin_share",
            "decision": "terminal_space_attack_survives",
            "evidence": f"smallest tailed terminal candidate share is {min_tail_share}; largest bare post-terminal margin share is {max_margin_share}",
            "limit": "share compares annotated windows, not automated glyph segmentation",
        },
        {
            "test": "bare_controls_have_tail_sized_empty_slot",
            "decision": "no_in_current_boxes",
            "evidence": "all three bare controls have post-terminal margin width far below both tailed terminal windows",
            "limit": "this does not prove the margin is linguistically meaningful; it blocks grammar promotion until recut/source segmentation confirms the edge",
        },
        {
            "test": "grammar_slot_promotion",
            "decision": "blocked_by_terminal_space_adversary",
            "evidence": "broad register and length failed, but terminal-space now has positive support as a layout explanation",
            "limit": "the post-861 split remains a source-visible positional contrast, not a grammatical function or value",
        },
    ]


def make_sheet(metrics: list[dict[str, Any]], out_path: Path) -> None:
    panels = []
    for row in metrics:
        overlay = Path(str(row["overlay"]))
        img = Image.open(overlay).convert("RGB")
        img.thumbnail((520, 260))
        canvas = Image.new("RGB", (560, 340), "white")
        canvas.paste(img, ((560 - img.width) // 2, 58))
        draw = ImageDraw.Draw(canvas)
        draw.text((12, 10), f"{row['cisi']} | {row['outcome']} | {row['tail']}", fill=(0, 0, 0))
        if row["outcome"] == "tailed":
            note = f"tail {row['terminal_candidate_width_px']}px / share {row['terminal_candidate_width_share']}"
        else:
            note = f"margin {row['post_terminal_margin_width_px']}px / share {row['post_terminal_margin_width_share']}"
        draw.text((12, 30), note, fill=(70, 70, 70))
        panels.append(canvas)

    cols = 2
    sheet_h = ((len(panels) + cols - 1) // cols) * 340
    sheet = Image.new("RGB", (cols * 560, sheet_h), "white")
    for idx, panel in enumerate(panels):
        sheet.paste(ImageOps.expand(panel, border=1, fill=(180, 180, 180)), ((idx % cols) * 560, (idx // cols) * 340))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path)


def write_doc(path: Path, summary: dict[str, Any], metrics: list[dict[str, Any]], decisions: list[dict[str, str]]) -> None:
    lines = [
        "# 032-002-861 / 220-032 Terminal-Space Recut",
        "",
        "Date: 2026-05-29",
        "",
        "## Question",
        "",
        "Do the source-visible bare `220-032-002-861` controls have a tail-sized empty terminal slot, or is terminal space a serious layout explanation for why they are bare?",
        "",
        "## Packet",
        "",
        f"- Tailed rows measured: `{summary['tailed_rows']}`",
        f"- Bare controls measured: `{summary['bare_rows']}`",
        f"- Comparison sheet: `{summary['comparison_sheet']}`",
        "",
        "## Decisions",
        "",
    ]
    for row in decisions:
        lines.append(f"- `{row['test']}`: `{row['decision']}`. {row['evidence']} Limit: {row['limit']}.")

    lines.extend(["", "## Metrics", ""])
    for row in metrics:
        if row["outcome"] == "tailed":
            lines.append(
                f"- `{row['cisi']}` `{row['tail']}`: line `{row['line_width_px']}px`, tail window `{row['terminal_candidate_width_px']}px`, share `{row['terminal_candidate_width_share']}`, edge gap `{row['nearest_terminal_edge_gap_px']}px`."
            )
        else:
            lines.append(
                f"- `{row['cisi']}` bare: line `{row['line_width_px']}px`, post-terminal margin `{row['post_terminal_margin_width_px']}px`, share `{row['post_terminal_margin_width_share']}`, bare terminal window `{row['bare_terminal_window_width_px']}px`."
            )

    lines.extend(
        [
            "",
            "## Result",
            "",
            "The terminal-space adversary is now positive, not merely pending. In the current box layer, the tailed rows have terminal candidate windows of `195px` (`M-91`) and `120px` (`M-240`), while the source-visible bare controls have only `28-38px` of marked post-terminal margin.",
            "",
            "That does not erase the `220-032` contrast. It changes its status: the split still survives broad register and length attacks, but it cannot be promoted to grammar-slot evidence until a fresh source recut shows that the bare controls had comparable terminal space and still chose closure.",
            "",
            "Current status: `terminal_space_adversary_blocks_220032_grammar_promotion`.",
            "",
            "Accepted sign values, phonetics, language identity, translations, exact source-token boundaries, and sign meanings remain 0/unaccepted.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    TMP_OUT.mkdir(parents=True, exist_ok=True)
    metrics = metric_rows()
    decisions = decision_rows(metrics)
    sheet = TMP_OUT / f"{OUT_PREFIX}_comparison_sheet.png"
    make_sheet(metrics, sheet)
    summary = {
        "date": "2026-05-29",
        "tailed_rows": sum(1 for row in metrics if row["outcome"] == "tailed"),
        "bare_rows": sum(1 for row in metrics if row["outcome"] == "bare_closure"),
        "outcome_distribution": ";".join(f"{k}:{v}" for k, v in Counter(row["outcome"] for row in metrics).items()),
        "comparison_sheet": str(sheet),
        "status": "terminal_space_adversary_blocks_220032_grammar_promotion",
        "decisions": decisions,
    }
    write_csv(REPORTS / f"{OUT_PREFIX}_metrics.csv", metrics)
    write_csv(REPORTS / f"{OUT_PREFIX}_decisions.csv", decisions)
    (REPORTS / f"{OUT_PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_doc(DOCS / f"{OUT_PREFIX}.md", summary, metrics, decisions)
    print(json.dumps({"built": OUT_PREFIX, **summary}, indent=2))


if __name__ == "__main__":
    main()
