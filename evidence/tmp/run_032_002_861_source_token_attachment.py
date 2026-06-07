from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path.cwd()
OUT = ROOT / "tmp" / "032_002_861_source_token_attachment"
REPORTS = ROOT / "data" / "open_prototype" / "reports"
OUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)


COLORS = {
    "line_window": (180, 70, 210),
    "pre_tail_window": (35, 160, 80),
    "tail_window": (220, 125, 25),
}


ROWS = [
    {
        "cisi": "M-376",
        "object_id": "2872.1",
        "witness": "a",
        "tail_family": "533-717",
        "text": "+740-100-176-002-861-533-717+",
        "source_route": "CISI India IA leaf n129 / printed p.94 / Mohenjo-daro 376-381 seals",
        "source_image": ROOT / "tmp/032_002_861_suffix_split/M376_impression_a_cisi_india_n129.png",
        "line_window": (75, 35, 805, 270),
        "pre_tail_window": (330, 45, 540, 260),
        "tail_window": (540, 45, 805, 260),
        "source_quality": "medium",
        "attachment_verdict": "same_line_candidate_present",
        "confidence": "medium",
        "observation": "A/a witnesses show one continuous row; the terminal-side candidate cluster is visually separated from the preceding cluster, with no obvious fusion or side split.",
        "limit": "Exact 861/533/717 boundaries remain catalog-mediated; this is not a source-normalized sign identification.",
    },
    {
        "cisi": "M-391",
        "object_id": "2887.1",
        "witness": "a",
        "tail_family": "533-717",
        "text": "+405-845-686-740-793-003-233-805-002-861-533-717+",
        "source_route": "CISI India IA leaf n131 / printed p.96 / Mohenjo-daro 391-396 seals",
        "source_image": ROOT / "tmp/032_002_861_suffix_split/M391_impression_a_cisi_india_n131.png",
        "line_window": (25, 80, 825, 245),
        "pre_tail_window": (350, 85, 560, 240),
        "tail_window": (560, 85, 825, 240),
        "source_quality": "medium_low",
        "attachment_verdict": "same_line_candidate_present_long_row",
        "confidence": "medium_low",
        "observation": "The source row is long but continuous; terminal-side material remains on the same line and is graphically discrete from the preceding cluster.",
        "limit": "Long-row crowding and scan blur block a stronger token-boundary claim.",
    },
    {
        "cisi": "M-91",
        "object_id": "2618.1",
        "witness": "a",
        "tail_family": "255-416",
        "text": "+740-100-798-220-032-002-861-255-416+",
        "source_route": "CISI India IA leaf n71 / printed p.36 / Mohenjo-daro 89-94 seals",
        "source_image": ROOT / "tmp/032_002_branch_tail_source_acquisition/M91_impression_a_signband_from_cisi_india_n071.png",
        "line_window": (105, 5, 555, 280),
        "pre_tail_window": (300, 20, 555, 270),
        "tail_window": (105, 20, 300, 270),
        "source_quality": "low_medium",
        "attachment_verdict": "same_line_singleton_candidate_present",
        "confidence": "medium_low",
        "observation": "One continuous signband is visible; the singleton terminal-side window remains attached to the same line under the previous order adjudication.",
        "limit": "This is a singleton and the public crop is low resolution; it cannot carry a repeated-tail model by itself.",
    },
    {
        "cisi": "M-240",
        "object_id": "2763.1",
        "witness": "a",
        "tail_family": "603",
        "text": "+520-240-220-032-002-861-603+",
        "source_route": "CISI India IA leaf n95 / printed p.60 / Mohenjo-daro 240-242 seals",
        "source_image": ROOT / "tmp/032_002_branch_tail_source_acquisition/M240_impression_a_signband_from_cisi_india_n095.png",
        "line_window": (335, 5, 755, 255),
        "pre_tail_window": (360, 20, 635, 250),
        "tail_window": (635, 20, 755, 250),
        "source_quality": "medium",
        "attachment_verdict": "same_line_candidate_present",
        "confidence": "medium",
        "observation": "The prior order window shows one seven-sign band; the terminal-side candidate is visually separated from the preceding window on the same row.",
        "limit": "The crop supports attachment/continuity, not exact sign identity or direction policy.",
    },
    {
        "cisi": "M-714",
        "object_id": "3139.1",
        "witness": "a",
        "tail_family": "603",
        "text": "+740-585-017-033-705-233-798-803-002-861-603+",
        "source_route": "CISI Pakistan IA leaf n79 / printed p.45 / Mohenjo-daro 712-714 seals",
        "source_image": ROOT / "tmp/032_002_861_suffix_split/M714_impression_a_cisi_pakistan_n079.png",
        "line_window": (40, 0, 1310, 245),
        "pre_tail_window": (860, 5, 1110, 235),
        "tail_window": (1110, 5, 1335, 235),
        "source_quality": "medium_low",
        "attachment_verdict": "same_line_candidate_present_crowded",
        "confidence": "medium_low",
        "observation": "The top signband is continuous and the terminal-side candidate remains on the same line, but the row is crowded and partly low-contrast.",
        "limit": "Good enough to keep the 603 row in the source-visible set; not good enough to accept exact 861/603 boundaries.",
    },
    {
        "cisi": "M-1273",
        "object_id": "3580.1",
        "witness": "a",
        "tail_family": "603",
        "text": "+740-055-002-861-603+",
        "source_route": "CISI Pakistan IA leaf n195 / printed p.161 / Mohenjo-daro 1269-1274 seals",
        "source_image": ROOT / "tmp/032_002_861_suffix_split/M1273_impression_a_cisi_pakistan_n195.png",
        "line_window": (40, 45, 1230, 445),
        "pre_tail_window": (760, 55, 1010, 430),
        "tail_window": (1010, 55, 1230, 430),
        "source_quality": "high",
        "attachment_verdict": "same_line_candidate_present_strongest_603",
        "confidence": "medium_high",
        "observation": "Short five-sign row with crisp separated graphic units; the terminal-side candidate is on the same line and not visibly fused to the preceding cluster.",
        "limit": "Still catalog-mediated for exact token labels, but this is the strongest public source witness for the 603 tail set.",
    },
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def font(size: int):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()


def draw_overlay(row: dict[str, object]) -> tuple[Path, list[dict[str, object]]]:
    image_path = Path(row["source_image"])
    im = Image.open(image_path).convert("RGB")
    title_font = font(18)
    label_font = font(14)
    pad = 54
    canvas = Image.new("RGB", (im.width, im.height + pad), "white")
    canvas.paste(im, (0, pad))
    draw = ImageDraw.Draw(canvas)
    title = f"{row['cisi']} {row['tail_family']} {row['attachment_verdict']}"
    draw.text((8, 8), title, fill=(0, 0, 0), font=title_font)
    draw.text((8, 31), "purple=line  green=pre-tail/861-side  orange=tail candidate", fill=(60, 60, 60), font=label_font)

    box_rows = []
    for field, role_label in [
        ("line_window", "line_window"),
        ("pre_tail_window", "pre_tail_window"),
        ("tail_window", "tail_window"),
    ]:
        box = row[field]
        color = COLORS[field]
        x1, y1, x2, y2 = box
        shifted = (x1, y1 + pad, x2, y2 + pad)
        draw.rectangle(shifted, outline=color, width=4)
        draw.text((x1 + 3, max(0, y1 + pad - 18)), role_label, fill=color, font=label_font)
        box_rows.append(
            {
                "cisi": row["cisi"],
                "object_id": row["object_id"],
                "witness": row["witness"],
                "tail_family": row["tail_family"],
                "text": row["text"],
                "box_role": field,
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2,
            }
        )

    out = OUT / f"{str(row['cisi']).replace('-', '')}_{row['tail_family'].replace('-', '_')}_source_token_attachment_overlay.png"
    canvas.save(out)
    return out, box_rows


def make_contact_sheet(overlays: list[Path]) -> Path:
    thumbs = []
    for overlay in overlays:
        im = Image.open(overlay).convert("RGB")
        im.thumbnail((1080, 430))
        thumbs.append(im.copy())
    width = 1140
    height = 20 + sum(im.height + 20 for im in thumbs)
    sheet = Image.new("RGB", (width, height), "white")
    y = 10
    for im in thumbs:
        sheet.paste(im, (20, y))
        y += im.height + 20
    out = OUT / "032_002_861_source_token_attachment_contact_sheet.png"
    sheet.save(out)
    return out


def main() -> None:
    verdict_rows = []
    box_rows = []
    overlays = []

    for row in ROWS:
        image_path = Path(row["source_image"])
        with Image.open(image_path) as im:
            width, height = im.size
        overlay, boxes = draw_overlay(row)
        overlays.append(overlay)
        box_rows.extend(boxes)
        verdict_rows.append(
            {
                "cisi": row["cisi"],
                "object_id": row["object_id"],
                "witness": row["witness"],
                "tail_family": row["tail_family"],
                "text": row["text"],
                "source_route": row["source_route"],
                "source_image_abs": str(image_path.resolve()),
                "source_sha256": sha256(image_path),
                "source_width": width,
                "source_height": height,
                "overlay_abs": str(overlay.resolve()),
                "source_quality": row["source_quality"],
                "attachment_verdict": row["attachment_verdict"],
                "confidence": row["confidence"],
                "observation": row["observation"],
                "limit": row["limit"],
            }
        )

    contact = make_contact_sheet(overlays)

    verdict_csv = REPORTS / "campaign_032_002_861_source_token_attachment_verdicts.csv"
    boxes_csv = REPORTS / "campaign_032_002_861_source_token_attachment_boxes.csv"
    summary_json = REPORTS / "campaign_032_002_861_source_token_attachment_summary.json"

    with verdict_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(verdict_rows[0].keys()))
        writer.writeheader()
        writer.writerows(verdict_rows)

    with boxes_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(box_rows[0].keys()))
        writer.writeheader()
        writer.writerows(box_rows)

    by_tail: dict[str, list[str]] = {}
    for row in verdict_rows:
        by_tail.setdefault(str(row["tail_family"]), []).append(str(row["cisi"]))

    summary = {
        "campaign": "032-002 861 source-token attachment",
        "rows": len(verdict_rows),
        "box_rows": len(box_rows),
        "tail_families": by_tail,
        "same_line_candidate_rows": len(verdict_rows),
        "strongest_public_witnesses": {
            "533-717": ["M-376", "M-391"],
            "255-416": ["M-91 singleton, low-resolution"],
            "603": ["M-1273 strongest", "M-240 medium", "M-714 medium-low"],
        },
        "source_observations": [
            "six focus rows have source-visible same-line terminal-side candidate windows",
            "no public crop in this packet shows an obvious side split or graphic fusion in the marked windows",
        ],
        "not_accepted": [
            "exact source-normalized 861/tail token boundaries",
            "sign values",
            "phonetic readings",
            "language identity",
            "translation",
        ],
        "verdict_csv": str(verdict_csv.resolve()),
        "boxes_csv": str(boxes_csv.resolve()),
        "contact_sheet": str(contact.resolve()),
    }
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
