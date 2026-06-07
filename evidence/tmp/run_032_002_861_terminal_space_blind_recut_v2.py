from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
DOCS = ROOT / "docs"
TMP_OUT = ROOT / "tmp" / "032_002_861_terminal_space_recut_v2"
SLUG = "campaign_032_002_861_terminal_space_recut_v2"

PREVIOUS_METRICS = REPORTS / "campaign_032_002_861_source_first_terminal_space_metrics.csv"
ATTACHMENT_BOXES = REPORTS / "campaign_032_002_861_source_token_attachment_boxes.csv"


RECUT_ROWS = {
    "M-355": {
        "source_image": ROOT / "tmp" / "032_002_861_533717_register_controls" / "M355_obv_A_register_control.png",
        "line_window": (35, 55, 1365, 340),
        # Tail-hidden manual measurement of the long terminal continuation zone.
        # This is a continuation window, not an exact token-boundary claim.
        "terminal_content_window": (35, 75, 560, 320),
        "box_basis": "tail_hidden_manual_recut_long_continuation_window",
        "segmentation_verdict": "same_line_long_terminal_continuation_source_visible",
        "confidence": "medium",
        "limit": "long continuation window is source-visible but exact 861|tail token boundaries remain catalog-mediated",
    },
    "M-1267": {
        "source_image": ROOT / "tmp" / "032_002_861_533717_register_controls" / "M1267_obv_A_register_control.png",
        "line_window": (0, 20, 820, 500),
        "bare_edge_window": (0, 25, 210, 315),
        "terminal_side_margin": (0, 25, 35, 315),
        "box_basis": "tail_hidden_manual_recut_bare_terminal_margin",
        "segmentation_verdict": "bare_terminal_edge_visible_low_resolution",
        "confidence": "medium_low",
        "limit": "poor source quality and uncertain terminal-side policy; measured margin is a visible same-line edge margin, not proof of total object space",
    },
}


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


def rect(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color: tuple[int, int, int], label: str) -> None:
    draw.rectangle(box, outline=color, width=4)
    draw.text((box[0] + 4, max(0, box[1] - 18)), label, fill=color)


def overlay_for(cisi: str, spec: dict[str, Any]) -> str:
    img = Image.open(spec["source_image"]).convert("RGB")
    draw = ImageDraw.Draw(img)
    rect(draw, spec["line_window"], (0, 160, 0), "line")
    if "terminal_content_window" in spec:
        rect(draw, spec["terminal_content_window"], (220, 0, 0), "terminal content")
    if "bare_edge_window" in spec:
        rect(draw, spec["bare_edge_window"], (0, 90, 220), "bare edge")
    if "terminal_side_margin" in spec:
        rect(draw, spec["terminal_side_margin"], (220, 120, 0), "post-terminal margin")
    out = TMP_OUT / f"{cisi.replace('-', '')}_terminal_recut_overlay.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return str(out)


def attachment_line_boxes() -> dict[str, tuple[int, int, int, int]]:
    out: dict[str, tuple[int, int, int, int]] = {}
    for row in read_csv(ATTACHMENT_BOXES):
        if row["box_role"] == "line_window":
            out[row["cisi"]] = tuple(int(row[key]) for key in ("x1", "y1", "x2", "y2"))
    return out


def recut_metric(previous: dict[str, str], cisi: str, spec: dict[str, Any]) -> dict[str, Any]:
    line = spec["line_window"]
    line_w = width(line)
    out: dict[str, Any] = dict(previous)
    out["metric_status"] = "quantified_tail_hidden_recut"
    out["line_width_px"] = line_w
    out["line_height_px"] = height(line)
    out["source_image"] = str(spec["source_image"])
    out["overlay"] = overlay_for(cisi, spec)
    out["box_basis"] = spec["box_basis"]
    out["segmentation_verdict"] = spec["segmentation_verdict"]
    out["confidence"] = spec["confidence"]
    out["limit"] = spec["limit"]
    if "terminal_content_window" in spec:
        tail = spec["terminal_content_window"]
        left_gap = abs(tail[0] - line[0])
        right_gap = abs(line[2] - tail[2])
        nearest_gap = min(left_gap, right_gap)
        out["terminal_content_width_px"] = width(tail)
        out["terminal_content_width_share"] = f3(width(tail) / line_w)
        out["terminal_content_area_share"] = f3(area(tail) / area(line))
        out["pre_tail_width_px"] = ""
        out["nearest_terminal_edge_gap_px"] = nearest_gap
        out["nearest_terminal_edge_gap_share"] = f3(nearest_gap / line_w)
        out["bare_terminal_window_width_px"] = ""
        out["bare_terminal_window_width_share"] = ""
        out["post_terminal_margin_width_px"] = ""
        out["post_terminal_margin_width_share"] = ""
        out["post_terminal_margin_area_share"] = ""
    else:
        edge = spec["bare_edge_window"]
        margin = spec["terminal_side_margin"]
        out["terminal_content_width_px"] = ""
        out["terminal_content_width_share"] = ""
        out["terminal_content_area_share"] = ""
        out["pre_tail_width_px"] = ""
        out["nearest_terminal_edge_gap_px"] = ""
        out["nearest_terminal_edge_gap_share"] = ""
        out["bare_terminal_window_width_px"] = width(edge)
        out["bare_terminal_window_width_share"] = f3(width(edge) / line_w)
        out["post_terminal_margin_width_px"] = width(margin)
        out["post_terminal_margin_width_share"] = f3(width(margin) / line_w)
        out["post_terminal_margin_area_share"] = f3(area(margin) / area(line))
    return out


def numeric(rows: list[dict[str, Any]], field: str) -> list[float]:
    values = []
    for row in rows:
        raw = row.get(field, "")
        if raw not in ("", None):
            values.append(float(raw))
    return values


def rng(values: list[float], suffix: str = "") -> str:
    if not values:
        return ""
    if all(value.is_integer() for value in values):
        return f"{int(min(values))}-{int(max(values))}{suffix}"
    return f"{min(values):.3f}-{max(values):.3f}{suffix}"


def class_summary(metrics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in metrics:
        grouped[row["tail_class"]].append(row)
    out = []
    for klass, rows in sorted(grouped.items()):
        tails = Counter(row["tail"] for row in rows)
        statuses = Counter(row["metric_status"] for row in rows)
        tail_widths = numeric(rows, "terminal_content_width_px")
        tail_shares = numeric(rows, "terminal_content_width_share")
        bare_margins = numeric(rows, "post_terminal_margin_width_px")
        bare_shares = numeric(rows, "post_terminal_margin_width_share")
        if tail_widths:
            measure = f"tail-window {rng(tail_widths, 'px')} / share {rng(tail_shares)}"
        elif bare_margins:
            measure = f"margin {rng(bare_margins, 'px')} / share {rng(bare_shares)}"
        else:
            measure = "unquantified"
        if klass == "long_continuation":
            verdict = "now_quantified_as_large_same_line_terminal_continuation_adversary"
        elif klass == "closure":
            verdict = "bare_controls_still_lack_tail_sized_same_line_terminal_margin"
        elif klass == "fixed_pair":
            verdict = "same_line_fixed_pair_survives_but_large_terminal_window_and_register_pressure_remain"
        else:
            verdict = "same_line_simple_tail_survives_but_terminal_space_adversary_remains"
        out.append(
            {
                "tail_class": klass,
                "rows": len(rows),
                "quantified_rows": sum(1 for row in rows if row["metric_status"].startswith("quantified")),
                "tails": ";".join(f"{tail}:{count}" for tail, count in sorted(tails.items())),
                "metric_status_distribution": ";".join(f"{status}:{count}" for status, count in sorted(statuses.items())),
                "width_or_margin_range": measure,
                "verdict": verdict,
            }
        )
    return out


def decisions(metrics: list[dict[str, Any]]) -> list[dict[str, str]]:
    tailed = [row for row in metrics if row["tail"] != "<END>" and row.get("terminal_content_width_px")]
    bare = [row for row in metrics if row["tail"] == "<END>" and row.get("post_terminal_margin_width_px")]
    min_tail = min(int(float(row["terminal_content_width_px"])) for row in tailed)
    max_tail = max(int(float(row["terminal_content_width_px"])) for row in tailed)
    min_tail_share = min(float(row["terminal_content_width_share"]) for row in tailed)
    max_tail_share = max(float(row["terminal_content_width_share"]) for row in tailed)
    max_bare = max(int(float(row["post_terminal_margin_width_px"])) for row in bare)
    min_bare = min(int(float(row["post_terminal_margin_width_px"])) for row in bare)
    min_bare_share = min(float(row["post_terminal_margin_width_share"]) for row in bare)
    max_bare_share = max(float(row["post_terminal_margin_width_share"]) for row in bare)
    long_rows = [row for row in metrics if row["tail_class"] == "long_continuation"]
    return [
        {
            "test": "visual_only_blockers_quantified",
            "decision": "closed_for_M355_and_M1267_with_quality_limits",
            "evidence": "M-355 now has a measured long continuation window; M-1267 now has a measured bare terminal margin",
            "limit": "measurements are tail-hidden manual recuts, not fully independent blind epigraphy",
        },
        {
            "test": "tail_windows_vs_bare_margins_v2",
            "decision": "terminal_space_adversary_strengthened",
            "evidence": f"tailed windows span {min_tail}-{max_tail}px / share {min_tail_share:.3f}-{max_tail_share:.3f}; bare margins span {min_bare}-{max_bare}px / share {min_bare_share:.3f}-{max_bare_share:.3f}",
            "limit": "tail windows measure visible terminal content; bare margins measure same-line terminal edge margin",
        },
        {
            "test": "bare_tail_sized_empty_slot",
            "decision": "still_not_observed",
            "evidence": f"largest measured bare margin is {max_bare}px, below the smallest measured tailed window {min_tail}px",
            "limit": "does not prove no physical space elsewhere on the object; it blocks same-line grammar promotion from current source windows",
        },
        {
            "test": "long_continuation_adversary",
            "decision": "upgraded_from_visual_only_to_quantified_adversary",
            "evidence": "; ".join(f"{row['cisi']} window {row['terminal_content_width_px']}px / share {row['terminal_content_width_share']}" for row in long_rows),
            "limit": "single long-continuation row; use as adversary, not positive grammar",
        },
        {
            "test": "grammar_promotion",
            "decision": "blocked",
            "evidence": "same-line tail attachment survives, but terminal capacity still separates tailed and bare source windows",
            "limit": "promotion requires a bare closure with tail-sized same-line terminal opportunity or exact/near-exact formula alternation under comparable layout",
        },
    ]


def make_contact_sheet(metrics: list[dict[str, Any]], out_path: Path) -> None:
    rows = [row for row in metrics if row["cisi"] in {"M-355", "M-1267", "M-376", "M-391", "M-1273", "M-240", "M-91"}]
    thumbs = []
    cell_w, cell_h = 560, 300
    for row in rows:
        source = row.get("overlay") or row.get("source_image")
        img = Image.open(source).convert("RGB")
        img = ImageOps.autocontrast(img)
        img.thumbnail((cell_w - 20, cell_h - 72))
        canvas = Image.new("RGB", (cell_w, cell_h), "white")
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 8), f"{row['cisi']} | {row['tail_class']} | {row['tail']}", fill="black")
        if row["tail"] == "<END>":
            metric = f"bare margin {row.get('post_terminal_margin_width_px','')}px / {row.get('post_terminal_margin_width_share','')}"
        else:
            metric = f"terminal window {row.get('terminal_content_width_px','')}px / {row.get('terminal_content_width_share','')}"
        draw.text((10, 28), metric, fill=(70, 70, 70))
        draw.text((10, 48), row.get("box_basis", ""), fill=(110, 70, 0))
        canvas.paste(img, ((cell_w - img.width) // 2, 68))
        thumbs.append(canvas)
    cols = 2
    sheet = Image.new("RGB", (cols * cell_w, ((len(thumbs) + cols - 1) // cols) * cell_h), "white")
    for idx, thumb in enumerate(thumbs):
        sheet.paste(ImageOps.expand(thumb, border=1, fill=(180, 180, 180)), ((idx % cols) * cell_w, (idx // cols) * cell_h))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path)


def blind_id(cisi: str) -> str:
    digest = hashlib.sha256(f"{cisi}|terminal-space-recut-v2".encode()).hexdigest()
    return f"TH{int(digest[:8], 16) % 900 + 100}"


def make_tail_hidden_source_sheet(metrics: list[dict[str, Any]], out_path: Path) -> list[dict[str, Any]]:
    rows = [row for row in metrics if row["cisi"] in {"M-355", "M-1267", "M-376", "M-391", "M-1273", "M-240", "M-91"}]
    line_boxes = attachment_line_boxes()
    packet = []
    thumbs = []
    cell_w, cell_h = 560, 250
    for row in rows:
        source = row.get("source_image")
        img = Image.open(source).convert("RGB")
        if row["cisi"] in RECUT_ROWS:
            img = img.crop(RECUT_ROWS[row["cisi"]]["line_window"])
        elif row["cisi"] in line_boxes:
            img = img.crop(line_boxes[row["cisi"]])
        img = ImageOps.autocontrast(img)
        img.thumbnail((cell_w - 20, cell_h - 52))
        bid = blind_id(row["cisi"])
        canvas = Image.new("RGB", (cell_w, cell_h), "white")
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 8), bid, fill="black")
        draw.text((10, 28), "source crop only; labels and tail class hidden", fill=(70, 70, 70))
        canvas.paste(img, ((cell_w - img.width) // 2, 52))
        thumbs.append(canvas)
        packet.append(
            {
                "blind_id": bid,
                "cisi": row["cisi"],
                "tail_class": row["tail_class"],
                "tail": row["tail"],
                "source_image": row["source_image"],
            }
        )
    cols = 2
    sheet = Image.new("RGB", (cols * cell_w, ((len(thumbs) + cols - 1) // cols) * cell_h), "white")
    for idx, thumb in enumerate(thumbs):
        sheet.paste(ImageOps.expand(thumb, border=1, fill=(180, 180, 180)), ((idx % cols) * cell_w, (idx // cols) * cell_h))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path)
    return packet


def write_doc(metrics: list[dict[str, Any]], summary_rows: list[dict[str, Any]], decision_rows: list[dict[str, str]], contact_sheet: Path) -> None:
    tailed = [row for row in metrics if row["tail"] != "<END>" and row.get("terminal_content_width_px")]
    bare = [row for row in metrics if row["tail"] == "<END>" and row.get("post_terminal_margin_width_px")]
    min_tail = min(int(float(row["terminal_content_width_px"])) for row in tailed)
    max_tail = max(int(float(row["terminal_content_width_px"])) for row in tailed)
    min_bare = min(int(float(row["post_terminal_margin_width_px"])) for row in bare)
    max_bare = max(int(float(row["post_terminal_margin_width_px"])) for row in bare)
    lines = [
        "# 032-002-861 Terminal-Space Recut V2",
        "",
        "Date: 2026-05-29",
        "",
        "## Question",
        "",
        "After quantifying the two visual-only blockers (`M-355` and `M-1267`), does any source-visible bare closure after `002-861` show tail-sized same-line terminal opportunity?",
        "",
        "This is still a source/layout campaign. It does not assign values, phonetics, language identity, or translations.",
        "",
        "## Inputs",
        "",
        f"- Prior metrics: `{PREVIOUS_METRICS.relative_to(ROOT)}`",
        f"- Script: `tmp/run_032_002_861_terminal_space_blind_recut_v2.py`",
        f"- Contact sheet: `{contact_sheet}`",
        f"- Quantified rows after recut: `{sum(1 for row in metrics if row['metric_status'].startswith('quantified'))}` of `{len(metrics)}`",
        "- Newly quantified rows: `M-355`, `M-1267`",
        "",
        "## Result",
        "",
        "The recut strengthens the terminal-space adversary.",
        "",
        f"Tailed terminal-content windows now span `{min_tail}-{max_tail}px`; bare same-line post-terminal margins span `{min_bare}-{max_bare}px`.",
        "",
        f"The largest measured bare margin is `{max_bare}px`, still below the smallest measured tailed window `{min_tail}px`.",
        "",
        "`M-355` is no longer just a visual note: it is a quantified long-continuation adversary. `M-1267` is now a quantified bare control, but it still does not provide tail-sized same-line empty terminal space.",
        "",
        "The source review sheet hides row labels and tail classes; the metric sheet is unblinded after measurement. This is a tail-hidden manual recut, not a claim of fully independent blind epigraphy.",
        "",
        "## Class State",
        "",
        "| Class | Rows | Quantified | Width or margin range | Verdict |",
        "|---|---:|---:|---|---|",
    ]
    for row in summary_rows:
        lines.append(f"| `{row['tail_class']}` | {row['rows']} | {row['quantified_rows']} | {row['width_or_margin_range']} | {row['verdict']} |")
    lines += [
        "",
        "## Decisions",
        "",
    ]
    for row in decision_rows:
        lines.append(f"- `{row['test']}`: `{row['decision']}`. {row['evidence']} Limit: {row['limit']}.")
    lines += [
        "",
        "## Interpretation",
        "",
        "Source-visible same-line tail attachment remains real positional evidence. But the current image layer still cannot promote a post-`861` grammar slot, because closure has not yet been observed with tail-sized same-line terminal opportunity.",
        "",
        "The next positive gate is now very concrete: find or recut a bare closure after `002-861` with at least `120px` of same-line terminal opportunity, under matched formula/register conditions, that still chooses closure.",
        "",
        "Accepted values, phonetics, language identity, translations, exact source-token boundaries, and sign meanings remain `0`.",
        "",
    ]
    (DOCS / f"{SLUG}.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    previous = read_csv(PREVIOUS_METRICS)
    metrics: list[dict[str, Any]] = []
    previous_by_cisi = {row["cisi"]: row for row in previous}
    for row in previous:
        if row["cisi"] in RECUT_ROWS:
            metrics.append(recut_metric(row, row["cisi"], RECUT_ROWS[row["cisi"]]))
        else:
            metrics.append(dict(row))
    summary_rows = class_summary(metrics)
    decision_rows = decisions(metrics)
    contact_sheet = TMP_OUT / f"{SLUG}_contact_sheet.png"
    tail_hidden_sheet = TMP_OUT / f"{SLUG}_tail_hidden_source_sheet.png"
    make_contact_sheet(metrics, contact_sheet)
    blind_key = make_tail_hidden_source_sheet(metrics, tail_hidden_sheet)
    write_csv(REPORTS / f"{SLUG}_metrics.csv", metrics)
    write_csv(REPORTS / f"{SLUG}_class_summary.csv", summary_rows)
    write_csv(REPORTS / f"{SLUG}_decisions.csv", decision_rows)
    write_csv(REPORTS / f"{SLUG}_tail_hidden_key.csv", blind_key)
    summary = {
        "date": "2026-05-29",
        "source_rows": len(metrics),
        "quantified_rows": sum(1 for row in metrics if row["metric_status"].startswith("quantified")),
        "newly_quantified_rows": sorted(RECUT_ROWS),
        "contact_sheet": str(contact_sheet),
        "tail_hidden_source_sheet": str(tail_hidden_sheet),
        "decisions": decision_rows,
        "class_rows": summary_rows,
    }
    (REPORTS / f"{SLUG}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_doc(metrics, summary_rows, decision_rows, contact_sheet)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
