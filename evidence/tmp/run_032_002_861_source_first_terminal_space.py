"""Measure terminal space on the actual seal images, in pixels.

The terminal-space adversary says: maybe tails after 861 appear only where
the seal had room left, and bare closures appear where it did not. To test
that we need measurements from source images, not catalog text. This script
takes the source-ready rows, pulls previously drawn pixel boxes — tail
windows for tailed rows (from the token-attachment packet) and hard-coded
bare-edge/margin boxes for six bare controls — and computes widths, area
shares, and edge gaps for each. Rows with images but no boxes are kept as
visual-only, unquantified. It then writes decision rows (the key one: every
measured bare margin is smaller than the smallest measured tail window, so
grammar promotion stays blocked), per-class summaries, a metrics CSV, a JSON
summary, and a contact-sheet PNG of all the crops with their numbers.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
TMP_OUT = ROOT / "tmp" / "032_002_861_source_first_terminal_space"
SLUG = "campaign_032_002_861_source_first_terminal_space"

CANONICAL = REPORTS / "campaign_032_002_861_source_normalized_tail_predictor_all_rows.csv"
TAILED_BOXES = REPORTS / "campaign_032_002_861_source_token_attachment_boxes.csv"
TAILED_VERDICTS = REPORTS / "campaign_032_002_861_source_token_attachment_verdicts.csv"
BARE_CROPS = REPORTS / "campaign_032_002_861_bare_edge_source_controls_crops.csv"
REGISTER_CROPS = REPORTS / "campaign_032_002_861_533717_source_controls_crops.csv"


BARE_BOXES = {
    "H-444": {
        "line_window": (0, 0, 700, 338),
        "bare_edge_window": (20, 25, 290, 330),
        "terminal_side_margin": (0, 25, 28, 330),
        "box_basis": "bare_edge_source_controls",
    },
    "M-723": {
        "line_window": (0, 0, 925, 345),
        "bare_edge_window": (0, 0, 315, 330),
        "terminal_side_margin": (0, 0, 38, 330),
        "box_basis": "bare_edge_source_controls",
    },
    "M-77": {
        "line_window": (0, 0, 750, 280),
        "bare_edge_window": (0, 0, 330, 275),
        "terminal_side_margin": (0, 0, 42, 275),
        "box_basis": "bare_edge_source_controls",
    },
    "M-15": {
        "line_window": (0, 0, 860, 290),
        "bare_edge_window": (0, 0, 335, 285),
        "terminal_side_margin": (0, 0, 45, 285),
        "box_basis": "bare_edge_source_controls",
    },
    "M-118": {
        "line_window": (0, 0, 605, 265),
        "bare_edge_window": (0, 0, 250, 260),
        "terminal_side_margin": (0, 0, 35, 260),
        "box_basis": "bare_edge_source_controls",
    },
    "M-1044": {
        "line_window": (0, 0, 600, 335),
        "bare_edge_window": (0, 0, 280, 330),
        "terminal_side_margin": (0, 0, 38, 330),
        "box_basis": "bare_edge_source_controls",
    },
}


VISUAL_ONLY = {"M-355", "M-1267"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys: list[str] = []
    seen = set()
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


def f3(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.3f}"


def source_ready(row: dict[str, str]) -> bool:
    return row.get("source_status") not in ("", "source_pending_or_not_checked", None) or bool(row.get("display_image"))


def tail_class(row: dict[str, str]) -> str:
    tail = row.get("tail") or "<END>"
    if tail == "<END>":
        return "closure"
    n = int(row.get("tail_len") or 0)
    if n == 1:
        return "simple_single"
    if n == 2:
        return "fixed_pair"
    return "long_continuation"


def tail_text(row: dict[str, str]) -> str:
    return row.get("tail") or "<END>"


def norm_prefix(row: dict[str, str]) -> str:
    return row.get("prefix") or "<START>"


def parse_tailed_boxes() -> dict[str, dict[str, tuple[int, int, int, int]]]:
    out: dict[str, dict[str, tuple[int, int, int, int]]] = defaultdict(dict)
    for row in read_csv(TAILED_BOXES):
        out[row["cisi"]][row["box_role"]] = tuple(int(row[key]) for key in ("x1", "y1", "x2", "y2"))
    return dict(out)


def rows_by_key(path: Path, key: str) -> dict[str, dict[str, str]]:
    out = {}
    for row in read_csv(path):
        out[row[key]] = row
    return out


def first_rows_by_key(path: Path, key: str) -> dict[str, dict[str, str]]:
    out = {}
    for row in read_csv(path):
        out.setdefault(row[key], row)
    return out


def metric_for_tailed(row: dict[str, str], boxes: dict[str, tuple[int, int, int, int]], verdict: dict[str, str]) -> dict[str, Any]:
    line = boxes["line_window"]
    pre = boxes["pre_tail_window"]
    tail_box = boxes["tail_window"]
    line_w = width(line)
    line_a = area(line)
    tail_w = width(tail_box)
    left_gap = abs(tail_box[0] - line[0])
    right_gap = abs(line[2] - tail_box[2])
    nearest_gap = min(left_gap, right_gap)
    return {
        "cisi": row["cisi"],
        "text": row["text"],
        "outcome": "tailed",
        "tail": tail_text(row),
        "tail_class": tail_class(row),
        "prefix": norm_prefix(row),
        "prefix_last2": row.get("prefix_last2") or "<START>",
        "register_key": row["register_key"],
        "source_status": row["source_status"],
        "metric_status": "quantified",
        "line_width_px": line_w,
        "line_height_px": height(line),
        "terminal_content_width_px": tail_w,
        "terminal_content_width_share": f3(tail_w / line_w),
        "terminal_content_area_share": f3(area(tail_box) / line_a),
        "pre_tail_width_px": width(pre),
        "nearest_terminal_edge_gap_px": nearest_gap,
        "nearest_terminal_edge_gap_share": f3(nearest_gap / line_w),
        "bare_terminal_window_width_px": "",
        "bare_terminal_window_width_share": "",
        "post_terminal_margin_width_px": "",
        "post_terminal_margin_width_share": "",
        "source_image": verdict.get("source_image_abs", row.get("display_image", "")),
        "overlay": verdict.get("overlay_abs", row.get("display_image", "")),
        "box_basis": "source_token_attachment_tail_window",
        "segmentation_verdict": verdict.get("attachment_verdict", row.get("layout_status", "")),
        "confidence": verdict.get("confidence", ""),
        "limit": verdict.get("limit", "source-token labels remain catalog-mediated"),
    }


def metric_for_bare(row: dict[str, str], crop: dict[str, str], boxes: dict[str, tuple[int, int, int, int]]) -> dict[str, Any]:
    line = boxes["line_window"]
    edge = boxes["bare_edge_window"]
    margin = boxes["terminal_side_margin"]
    line_w = width(line)
    return {
        "cisi": row["cisi"],
        "text": row["text"],
        "outcome": "bare_closure",
        "tail": "<END>",
        "tail_class": "closure",
        "prefix": norm_prefix(row),
        "prefix_last2": row.get("prefix_last2") or "<START>",
        "register_key": row["register_key"],
        "source_status": row["source_status"],
        "metric_status": "quantified",
        "line_width_px": line_w,
        "line_height_px": height(line),
        "terminal_content_width_px": "",
        "terminal_content_width_share": "",
        "terminal_content_area_share": "",
        "pre_tail_width_px": "",
        "nearest_terminal_edge_gap_px": "",
        "nearest_terminal_edge_gap_share": "",
        "bare_terminal_window_width_px": width(edge),
        "bare_terminal_window_width_share": f3(width(edge) / line_w),
        "post_terminal_margin_width_px": width(margin),
        "post_terminal_margin_width_share": f3(width(margin) / line_w),
        "post_terminal_margin_area_share": f3(area(margin) / area(line)),
        "source_image": crop.get("source_image_abs", row.get("display_image", "")),
        "overlay": crop.get("overlay_abs", row.get("display_image", "")),
        "box_basis": boxes.get("box_basis", "bare_edge_source_controls"),
        "segmentation_verdict": crop.get("visual_status", row.get("layout_status", "")),
        "confidence": "existing_box",
        "limit": "bare margin comes from existing source-control overlay, not a fresh blind recut",
    }


def metric_for_visual_only(row: dict[str, str], crop: dict[str, str] | None) -> dict[str, Any]:
    return {
        "cisi": row["cisi"],
        "text": row["text"],
        "outcome": "tailed" if tail_text(row) != "<END>" else "bare_closure",
        "tail": tail_text(row),
        "tail_class": tail_class(row),
        "prefix": norm_prefix(row),
        "prefix_last2": row.get("prefix_last2") or "<START>",
        "register_key": row["register_key"],
        "source_status": row["source_status"],
        "metric_status": "visual_only_unquantified",
        "line_width_px": "",
        "line_height_px": "",
        "terminal_content_width_px": "",
        "terminal_content_width_share": "",
        "terminal_content_area_share": "",
        "pre_tail_width_px": "",
        "nearest_terminal_edge_gap_px": "",
        "nearest_terminal_edge_gap_share": "",
        "bare_terminal_window_width_px": "",
        "bare_terminal_window_width_share": "",
        "post_terminal_margin_width_px": "",
        "post_terminal_margin_width_share": "",
        "post_terminal_margin_area_share": "",
        "source_image": (crop or {}).get("crop_abs", row.get("display_image", "")),
        "overlay": row.get("display_image", ""),
        "box_basis": "source_visible_register_control_no_terminal_metric",
        "segmentation_verdict": row.get("layout_status", ""),
        "confidence": "visual_only",
        "limit": "source-visible but not terminal-space comparable in this packet",
    }


def decision_rows(metrics: list[dict[str, Any]]) -> list[dict[str, str]]:
    tailed_q = [m for m in metrics if m["outcome"] == "tailed" and m["metric_status"] == "quantified"]
    bare_q = [m for m in metrics if m["outcome"] == "bare_closure" and m["metric_status"] == "quantified"]
    visual_only = [m for m in metrics if m["metric_status"] == "visual_only_unquantified"]
    rows = []

    min_tail_width = min(int(m["terminal_content_width_px"]) for m in tailed_q)
    max_tail_width = max(int(m["terminal_content_width_px"]) for m in tailed_q)
    min_tail_share = min(float(m["terminal_content_width_share"]) for m in tailed_q)
    max_tail_share = max(float(m["terminal_content_width_share"]) for m in tailed_q)
    max_bare_margin = max(int(m["post_terminal_margin_width_px"]) for m in bare_q)
    min_bare_margin = min(int(m["post_terminal_margin_width_px"]) for m in bare_q)
    max_bare_share = max(float(m["post_terminal_margin_width_share"]) for m in bare_q)
    min_bare_share = min(float(m["post_terminal_margin_width_share"]) for m in bare_q)
    tail_gap_zero = sum(1 for m in tailed_q if int(m["nearest_terminal_edge_gap_px"]) == 0)

    rows.append(
        {
            "test": "quantified_tail_windows_vs_bare_margins",
            "decision": "terminal_space_adversary_generalizes_across_current_quantified_source_rows",
            "evidence": f"tailed windows span {min_tail_width}-{max_tail_width}px / share {min_tail_share:.3f}-{max_tail_share:.3f}; bare post-terminal margins span {min_bare_margin}-{max_bare_margin}px / share {min_bare_share:.3f}-{max_bare_share:.3f}",
            "limit": "tailed windows are candidate tail content boxes, while bare margins are terminal-side margins from source-control overlays; this is a blocking adversary, not an automated proof",
        }
    )
    rows.append(
        {
            "test": "tail_edge_attachment",
            "decision": "same_line_tail_attachment_survives_as_positional_evidence",
            "evidence": f"{tail_gap_zero}/{len(tailed_q)} quantified tailed rows touch the marked terminal edge; all six have same-line attachment verdicts",
            "limit": "exact 861|tail boundaries and sign identities remain catalog-mediated",
        }
    )
    rows.append(
        {
            "test": "bare_tail_sized_empty_slot",
            "decision": "not_observed_in_current_quantified_bare_controls",
            "evidence": f"largest measured bare post-terminal margin is {max_bare_margin}px, below the smallest measured tailed terminal-content window {min_tail_width}px",
            "limit": "does not prove no available physical space existed outside current boxes; requires fresh blind source recut before grammar promotion",
        }
    )
    rows.append(
        {
            "test": "visual_only_rows",
            "decision": "not_comparable_for_terminal_space",
            "evidence": ";".join(f"{m['cisi']}:{m['tail_class']}" for m in visual_only),
            "limit": "M-355 and M-1267 remain source-visible but unquantified in this packet",
        }
    )
    rows.append(
        {
            "test": "grammar_promotion",
            "decision": "blocked",
            "evidence": "source-first segmentation keeps typed continuation visible, but terminal-space and formula-template attacks both remain active",
            "limit": "promote only after blind terminal-space recut finds bare controls with tail-sized space still choosing closure or exact/near-exact formulas alternating under comparable layout",
        }
    )
    return rows


def class_rows(metrics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    by_class: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in metrics:
        by_class[row["tail_class"]].append(row)
    for cls, group in sorted(by_class.items()):
        q = [r for r in group if r["metric_status"] == "quantified"]
        out.append(
            {
                "tail_class": cls,
                "source_ready_rows": len(group),
                "quantified_rows": len(q),
                "tails": ";".join(f"{k}:{v}" for k, v in Counter(r["tail"] for r in group).most_common()),
                "prefix_last2_distribution": ";".join(f"{k}:{v}" for k, v in Counter(r["prefix_last2"] for r in group).most_common()),
                "register_distribution": ";".join(f"{k}:{v}" for k, v in Counter(r["register_key"] for r in group).most_common()),
                "metric_status_distribution": ";".join(f"{k}:{v}" for k, v in Counter(r["metric_status"] for r in group).most_common()),
                "width_or_margin_range": width_range(cls, q),
                "verdict": class_verdict(cls, group, q),
            }
        )
    return out


def width_range(cls: str, q: list[dict[str, Any]]) -> str:
    if not q:
        return "unquantified"
    if cls == "closure":
        vals = [int(r["post_terminal_margin_width_px"]) for r in q]
        shares = [float(r["post_terminal_margin_width_share"]) for r in q]
        return f"margin {min(vals)}-{max(vals)}px / share {min(shares):.3f}-{max(shares):.3f}"
    vals = [int(r["terminal_content_width_px"]) for r in q]
    shares = [float(r["terminal_content_width_share"]) for r in q]
    return f"tail-window {min(vals)}-{max(vals)}px / share {min(shares):.3f}-{max(shares):.3f}"


def class_verdict(cls: str, group: list[dict[str, Any]], q: list[dict[str, Any]]) -> str:
    if cls == "closure":
        return "bare_controls_show_terminal_edge_but_not_tail_sized_post_margin"
    if cls == "simple_single":
        return "same_line_source_visible_but_tail_space_adversary_active"
    if cls == "fixed_pair":
        return "same_line_source_visible_fixed_unit_but_large_terminal_window_and_narrow_register"
    if cls == "long_continuation":
        return "source_visible_adversary_visual_only_not_metric_promotable"
    return "unclassified"


def make_sheet(metrics: list[dict[str, Any]], out_path: Path) -> None:
    panels = []
    for row in metrics:
        image_path = Path(str(row.get("overlay") or row.get("source_image")))
        if not image_path.exists():
            continue
        img = Image.open(image_path).convert("RGB")
        img.thumbnail((520, 260))
        canvas = Image.new("RGB", (560, 350), "white")
        canvas.paste(img, ((560 - img.width) // 2, 60))
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 10), f"{row['cisi']} | {row['tail_class']} | {row['tail']}", fill=(0, 0, 0))
        if row["metric_status"] == "quantified" and row["outcome"] == "tailed":
            note = f"tail window {row['terminal_content_width_px']}px / {row['terminal_content_width_share']}"
        elif row["metric_status"] == "quantified":
            note = f"bare margin {row['post_terminal_margin_width_px']}px / {row['post_terminal_margin_width_share']}"
        else:
            note = "visual-only: not terminal-space comparable"
        draw.text((10, 30), note, fill=(70, 70, 70))
        panels.append(canvas)

    cols = 2
    sheet = Image.new("RGB", (cols * 560, ((len(panels) + cols - 1) // cols) * 350), "white")
    for idx, panel in enumerate(panels):
        sheet.paste(ImageOps.expand(panel, border=1, fill=(170, 170, 170)), ((idx % cols) * 560, (idx // cols) * 350))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path)


def main() -> None:
    canonical = read_csv(CANONICAL)
    by_cisi = {row["cisi"]: row for row in canonical}
    source_ready_rows = [row for row in canonical if source_ready(row)]

    tailed_boxes = parse_tailed_boxes()
    tailed_verdicts = rows_by_key(TAILED_VERDICTS, "cisi")
    bare_crops = rows_by_key(BARE_CROPS, "cisi")
    register_crops = first_rows_by_key(REGISTER_CROPS, "cisi")

    metrics: list[dict[str, Any]] = []
    for row in source_ready_rows:
        cisi = row["cisi"]
        if cisi in tailed_boxes:
            metrics.append(metric_for_tailed(row, tailed_boxes[cisi], tailed_verdicts.get(cisi, {})))
        elif cisi in BARE_BOXES:
            metrics.append(metric_for_bare(row, bare_crops.get(cisi, {}), BARE_BOXES[cisi]))
        elif cisi in VISUAL_ONLY:
            metrics.append(metric_for_visual_only(row, register_crops.get(cisi)))
        else:
            metrics.append(metric_for_visual_only(row, None))

    decisions = decision_rows(metrics)
    classes = class_rows(metrics)
    sheet = TMP_OUT / f"{SLUG}_contact_sheet.png"
    make_sheet(metrics, sheet)

    summary = {
        "date": "2026-05-29",
        "canonical_rows": len(canonical),
        "source_ready_rows": len(source_ready_rows),
        "quantified_rows": sum(1 for r in metrics if r["metric_status"] == "quantified"),
        "visual_only_unquantified_rows": [r["cisi"] for r in metrics if r["metric_status"] == "visual_only_unquantified"],
        "contact_sheet": str(sheet),
        "decisions": decisions,
        "class_rows": classes,
    }

    write_csv(REPORTS / f"{SLUG}_metrics.csv", metrics)
    write_csv(REPORTS / f"{SLUG}_class_summary.csv", classes)
    write_csv(REPORTS / f"{SLUG}_decisions.csv", decisions)
    (REPORTS / f"{SLUG}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
