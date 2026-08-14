"""Record token-order verdicts for four branch-tail seals as boxed overlays.

The question these overlays answer: on the actual seal image, does the sign
after 002 (861, 390, or 300) really continue into a tail on the same line,
in the catalog's right-to-left reading order? The ROWS table holds the human
judgments for M-49, M-240, M-91, and M-70 — each with hand-drawn pixel boxes
marking the 032/002 transition, the Y sign, and the tail window, plus an
order verdict (all four pass), a confidence level, and an interpretive note.
The script draws the color-coded overlay PNGs, stacks them into a contact
sheet, and writes the verdicts CSV and boxes CSV that later packets cite as
the source-visible token-order evidence.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path.cwd()
OUT = ROOT / "tmp" / "032_002_branch_tail_token_order"
REPORTS = ROOT / "data" / "open_prototype" / "reports"
OUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)


COLORS = {
    "032": (230, 40, 40),
    "002": (35, 95, 255),
    "Y": (35, 170, 80),
    "tail": (210, 120, 20),
    "tail_window": (190, 90, 210),
}


ROWS = [
    {
        "cisi": "M-49",
        "side": "A",
        "text": "+527-550-240-220-032-002-300-350-032-190+",
        "branch_tail": "002-300-350-032-190",
        "source_image": ROOT / "tmp/032_002_y_source_function_batch/M49_target_300_fullpanel_a.png",
        "source_route": "CISI India IA leaf n58 / printed p.23 / Mohenjo-daro 47-49 seals",
        "source_single_line": "yes",
        "order_verdict": "pass_existing_token_box",
        "confidence": "medium",
        "family_link": "later 032 tail: 300-350-032-190",
        "interpretive_note": "Existing scaffold already boxes 032-002-300; visible material continues leftward under local R/L order and contains later 032.",
        "boxes": [
            ("032", "032", (455, 110, 530, 310)),
            ("002", "002", (385, 115, 455, 305)),
            ("300", "Y", (285, 105, 390, 310)),
            ("350-032-190 tail window", "tail_window", (95, 85, 285, 325)),
        ],
    },
    {
        "cisi": "M-240",
        "side": "A/a",
        "text": "+520-240-220-032-002-861-603+",
        "branch_tail": "002-861-603",
        "source_image": ROOT / "tmp/032_002_branch_tail_source_acquisition/M240_impression_a_signband_from_cisi_india_n095.png",
        "source_route": "CISI India IA leaf n95 / printed p.60 / Mohenjo-daro 240-242 seals",
        "source_single_line": "yes",
        "order_verdict": "pass_tail_continuation_candidate",
        "confidence": "medium",
        "family_link": "global all-002 tail family 861->603 occurs 3 times",
        "interpretive_note": "Both A and a panels show a single seven-sign band. Under the catalog R/L order, 861 is not final; 603 follows it in the same row. This is the key source-visible target 861 continuation.",
        "boxes": [
            ("032-002-861-603 order window", "tail_window", (335, 5, 755, 255)),
            ("post-861 tail side", "tail", (635, 20, 755, 250)),
            ("861 plus 002/032 transition side", "Y", (360, 20, 635, 250)),
        ],
    },
    {
        "cisi": "M-91",
        "side": "A/a",
        "text": "+740-100-798-220-032-002-861-255-416+",
        "branch_tail": "002-861-255-416",
        "source_image": ROOT / "tmp/032_002_branch_tail_source_acquisition/M91_impression_a_signband_from_cisi_india_n071.png",
        "source_route": "CISI India IA leaf n71 / printed p.36 / Mohenjo-daro 89-94 seals",
        "source_single_line": "yes",
        "order_verdict": "pass_tail_continuation_candidate_lowres",
        "confidence": "medium_low",
        "family_link": "singleton 861->255-416; supports nonterminal 861 but not a repeated tail family yet",
        "interpretive_note": "The public A/a panels show one continuous nine-sign band. The source quality is lower and the tail is not a repeated family, but it preserves 861 as nonterminal in a non-target A-220-032 frame.",
        "boxes": [
            ("032-002-861-255-416 order window", "tail_window", (105, 5, 555, 280)),
            ("post-861 tail side", "tail", (105, 20, 300, 270)),
            ("861 plus 002/032 transition side", "Y", (300, 20, 555, 270)),
        ],
    },
    {
        "cisi": "M-70",
        "side": "A/a",
        "text": "+226-032-002-390-692+",
        "branch_tail": "002-390-692",
        "source_image": ROOT / "tmp/032_002_branch_tail_source_acquisition/M70_impression_a_signband_from_cisi_india_n066.png",
        "source_route": "CISI India IA leaf n66 / printed p.31 / Mohenjo-daro 70-72 seals",
        "source_single_line": "yes",
        "order_verdict": "pass_branch_head_continuation_candidate",
        "confidence": "medium",
        "family_link": "390 branch-head family; compare next to 390->125/705 and unknown 390->590-032",
        "interpretive_note": "The public A/a panels show one continuous five-sign band. Under local R/L order, 390 is followed by 692, so 390 remains branch-head-like inside the adjacent 032-002 lane.",
        "boxes": [
            ("032-002-390-692 order window", "tail_window", (90, 5, 650, 250)),
            ("post-390 tail side", "tail", (90, 15, 250, 245)),
            ("390 plus 002/032 transition side", "Y", (250, 15, 560, 245)),
        ],
    },
]


def draw_overlay(row: dict[str, object]) -> tuple[Path, list[dict[str, object]]]:
    try:
        font = ImageFont.truetype("arial.ttf", 18)
        small = ImageFont.truetype("arial.ttf", 14)
    except Exception:
        font = ImageFont.load_default()
        small = font

    image_path = Path(row["source_image"])
    im = Image.open(image_path).convert("RGB")
    pad = 42
    canvas = Image.new("RGB", (im.width, im.height + pad), "white")
    canvas.paste(im, (0, pad))
    draw = ImageDraw.Draw(canvas)
    title = f"{row['cisi']} {row['branch_tail']} {row['order_verdict']}"
    draw.text((8, 6), title, fill=(0, 0, 0), font=small)

    box_rows = []
    for label, role, box in row["boxes"]:
        color = COLORS[role]
        x1, y1, x2, y2 = box
        shifted = (x1, y1 + pad, x2, y2 + pad)
        draw.rectangle(shifted, outline=color, width=4)
        draw.text((x1 + 3, max(0, y1 + pad - 20)), label, fill=color, font=small)
        box_rows.append(
            {
                "cisi": row["cisi"],
                "side": row["side"],
                "text": row["text"],
                "branch_tail": row["branch_tail"],
                "token_or_window": label,
                "role": role,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
            }
        )

    out = OUT / f"{str(row['cisi']).replace('-', '')}_{str(row['side']).replace('/', '_')}_token_order_overlay.png"
    canvas.save(out)
    return out, box_rows


def make_contact_sheet(overlays: list[Path]) -> Path:
    thumbs = []
    for overlay in overlays:
        im = Image.open(overlay).convert("RGB")
        im.thumbnail((980, 430))
        thumbs.append((overlay, im.copy()))
    width = 1040
    height = 24 + sum(im.height + 22 for _, im in thumbs)
    sheet = Image.new("RGB", (width, height), "white")
    y = 12
    for _, im in thumbs:
        sheet.paste(im, (20, y))
        y += im.height + 22
    out = OUT / "032_002_branch_tail_token_order_contact_sheet.png"
    sheet.save(out)
    return out


def main() -> None:
    verdict_rows = []
    box_rows = []
    overlays = []

    for row in ROWS:
        overlay, boxes = draw_overlay(row)
        overlays.append(overlay)
        box_rows.extend(boxes)
        verdict_rows.append(
            {
                "cisi": row["cisi"],
                "side": row["side"],
                "text": row["text"],
                "branch_tail": row["branch_tail"],
                "source_route": row["source_route"],
                "source_image_abs": str(Path(row["source_image"]).resolve()),
                "overlay_abs": str(overlay.resolve()),
                "source_single_line": row["source_single_line"],
                "order_verdict": row["order_verdict"],
                "confidence": row["confidence"],
                "family_link": row["family_link"],
                "interpretive_note": row["interpretive_note"],
            }
        )

    contact = make_contact_sheet(overlays)

    verdict_csv = REPORTS / "campaign_032_002_branch_tail_token_order_verdicts.csv"
    boxes_csv = REPORTS / "campaign_032_002_branch_tail_token_order_boxes.csv"
    summary_json = REPORTS / "campaign_032_002_branch_tail_token_order_summary.json"

    with verdict_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(verdict_rows[0].keys()))
        writer.writeheader()
        writer.writerows(verdict_rows)

    with boxes_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(box_rows[0].keys()))
        writer.writeheader()
        writer.writerows(box_rows)

    summary = {
        "rows": len(verdict_rows),
        "box_rows": len(box_rows),
        "pass_rows": sum(1 for row in verdict_rows if row["order_verdict"].startswith("pass")),
        "source_visible_cluster": ["M-49", "M-240", "M-91", "M-70"],
        "repeated_family_support": ["M-240 861->603", "M-70 390->692 as 390 branch-head family"],
        "singleton_support": ["M-91 861->255-416", "M-49 300->350-032-190"],
        "verdict_csv": str(verdict_csv.resolve()),
        "boxes_csv": str(boxes_csv.resolve()),
        "contact_sheet": str(contact.resolve()),
    }
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
