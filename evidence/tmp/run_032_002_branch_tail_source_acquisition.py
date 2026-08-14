"""Acquire public source images for three branch-tail seals and log the blocked ones.

Three seals with branch tails after 002 (M-240, M-91, M-70) previously had
only local reference routes — a catalog number but no viewable image. This
script downloads the three CISI India page scans that show them from the
Internet Archive at 2000px width, crops each seal's face-A and impression-a
panels plus tighter signband crops using hand-picked pixel boxes, and builds
a labeled contact sheet. Two further rows stay blocked and are recorded as
such: M-1677 needs CISI volume 3.1 or an excavation archive, and object
3335.1 cannot be routed because its corpus row has no identifying handle.
Writes a crops CSV, a routes CSV (upgraded and blocked rows together), and a
JSON summary.
"""

from __future__ import annotations

import csv
import json
import shutil
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path.cwd()
OUT = ROOT / "tmp" / "032_002_branch_tail_source_acquisition"
REPORTS = ROOT / "data" / "open_prototype" / "reports"
OUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

IA_BASE = (
    "https://archive.org/download/"
    "TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/"
    "Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India/page"
)


SOURCES = {
    66: {
        "file": OUT / "cisi_india_n066_w2000.jpg",
        "label": "CISI India IA leaf n66 / printed p.31 / Mohenjo-daro 70-72 seals",
    },
    71: {
        "file": OUT / "cisi_india_n071_w2000.jpg",
        "label": "CISI India IA leaf n71 / printed p.36 / Mohenjo-daro 89-94 seals",
    },
    95: {
        "file": OUT / "cisi_india_n095_w2000.jpg",
        "label": "CISI India IA leaf n95 / printed p.60 / Mohenjo-daro 240-242 seals",
    },
}


ROWS = [
    {
        "cisi": "M-240",
        "object_id": "2763.1",
        "text": "+520-240-220-032-002-861-603+",
        "branch_tail": "002-861-603",
        "role": "target_240_220_032 leaky-861 continuation",
        "leaf": 95,
        "source_status": "public_cisi_plate_page_found",
        "route_note": "Previous state was local source-reference route only (HR 4098324). Public CISI India leaf n95 directly shows M-240 A/a.",
        "panels": [
            ("A", (130, 180, 860, 900), (130, 180, 850, 420)),
            ("a", (1260, 170, 2020, 900), (1260, 170, 2020, 430)),
        ],
    },
    {
        "cisi": "M-91",
        "object_id": "2618.1",
        "text": "+740-100-798-220-032-002-861-255-416+",
        "branch_tail": "002-861-255-416",
        "role": "non240_a_220_032 leaky-861 continuation",
        "leaf": 71,
        "source_status": "public_cisi_plate_page_found",
        "route_note": "Previous state was local source-reference route only (DK6380429). Public CISI India leaf n71 directly shows M-91 A/a.",
        "panels": [
            ("A", (1560, 170, 2295, 840), (1560, 170, 2295, 405)),
            ("a", (1545, 900, 2300, 1615), (1545, 900, 2300, 1185)),
        ],
    },
    {
        "cisi": "M-70",
        "object_id": "2598.1",
        "text": "+226-032-002-390-692+",
        "branch_tail": "002-390-692",
        "role": "outside_032 branch-head-390 continuation",
        "leaf": 66,
        "source_status": "public_cisi_plate_page_found",
        "route_note": "Previous state was needs_source_route (HR 4076048). Public CISI India leaf n66 directly shows M-70 A/a.",
        "panels": [
            ("A", (340, 175, 1145, 920), (340, 175, 1145, 430)),
            ("a", (1305, 175, 2225, 915), (1305, 175, 2225, 430)),
        ],
    },
]

BLOCKED = [
    {
        "cisi": "M-1677",
        "object_id": "2236.1",
        "text": "+520-382-032-002-820-001-440-012+",
        "branch_tail": "002-820-001-440-012",
        "role": "outside_032 leaky-820 continuation",
        "source_status": "cisi_3_1_or_archive_required",
        "route_note": "No public CISI India/Pakistan Vol. 1/2 plate route in checked OCR/image layer. CISI 3.1 range-supports Mohenjo-daro m1660-m2132, so the next route is CISI 3.1/HARP/Harappa archive by DK11358130.",
    },
    {
        "cisi": "-",
        "object_id": "3335.1",
        "text": "+740-205-032-002-390-590-032+",
        "branch_tail": "002-390-590-032",
        "role": "outside_032 branch-head-390 continuation with later 032",
        "source_status": "blocked_until_object_id_resolved",
        "route_note": "Local metadata has no CISI object id, site, area, excavation id, or source handle. This cannot be source-routed until the corpus row is identified.",
    },
]


def fetch_leaf(leaf: int) -> None:
    target = SOURCES[leaf]["file"]
    if target.exists():
        return
    url = f"{IA_BASE}/n{leaf}_w2000.jpg"
    with urllib.request.urlopen(url) as response, target.open("wb") as handle:
        shutil.copyfileobj(response, handle)


def crop(path: Path, box: tuple[int, int, int, int], out_path: Path) -> None:
    im = Image.open(path).convert("RGB")
    im.crop(box).save(out_path)


def draw_contact_sheet(crop_rows: list[dict[str, str]]) -> Path:
    try:
        font = ImageFont.truetype("arial.ttf", 22)
        small = ImageFont.truetype("arial.ttf", 16)
    except Exception:
        font = ImageFont.load_default()
        small = font

    panels = []
    for row in crop_rows:
        im = Image.open(row["full_panel_crop_abs"]).convert("RGB")
        im.thumbnail((560, 440))
        panels.append((row, im.copy()))

    width = 1200
    pad = 24
    y = pad
    blocks = []
    for row, im in panels:
        block_h = im.height + 86
        blocks.append((row, im, y, block_h))
        y += block_h + pad

    sheet = Image.new("RGB", (width, y + pad), "white")
    draw = ImageDraw.Draw(sheet)
    for row, im, y0, _ in blocks:
        title = f"{row['cisi']} {row['side']}  {row['branch_tail']}  {row['source_leaf']}"
        draw.text((pad, y0), title, fill=(0, 0, 0), font=font)
        draw.text((pad, y0 + 30), row["text"], fill=(40, 40, 40), font=small)
        sheet.paste(im, (pad, y0 + 60))

    out = OUT / "032_002_branch_tail_public_cisi_contact_sheet.png"
    sheet.save(out)
    return out


def main() -> None:
    for leaf in SOURCES:
        fetch_leaf(leaf)

    crop_rows: list[dict[str, str]] = []
    route_rows: list[dict[str, str]] = []
    for row in ROWS:
        source = SOURCES[row["leaf"]]
        route_rows.append(
            {
                "cisi": row["cisi"],
                "object_id": row["object_id"],
                "text": row["text"],
                "branch_tail": row["branch_tail"],
                "role": row["role"],
                "source_status": row["source_status"],
                "source_leaf": source["label"],
                "source_image_abs": str(source["file"].resolve()),
                "route_note": row["route_note"],
            }
        )
        for side, full_box, signband_box in row["panels"]:
            side_slug = "face_A" if side == "A" else "impression_a"
            full_out = OUT / f"{row['cisi'].replace('-', '')}_{side_slug}_full_panel_from_cisi_india_n{row['leaf']:03d}.png"
            band_out = OUT / f"{row['cisi'].replace('-', '')}_{side_slug}_signband_from_cisi_india_n{row['leaf']:03d}.png"
            crop(source["file"], full_box, full_out)
            crop(source["file"], signband_box, band_out)
            crop_rows.append(
                {
                    "cisi": row["cisi"],
                    "object_id": row["object_id"],
                    "side": side,
                    "text": row["text"],
                    "branch_tail": row["branch_tail"],
                    "role": row["role"],
                    "source_leaf": source["label"],
                    "source_image_abs": str(source["file"].resolve()),
                    "full_panel_box": json.dumps(full_box),
                    "signband_box": json.dumps(signband_box),
                    "full_panel_crop_abs": str(full_out.resolve()),
                    "signband_crop_abs": str(band_out.resolve()),
                    "route_note": row["route_note"],
                }
            )

    for row in BLOCKED:
        route_rows.append(
            {
                "cisi": row["cisi"],
                "object_id": row["object_id"],
                "text": row["text"],
                "branch_tail": row["branch_tail"],
                "role": row["role"],
                "source_status": row["source_status"],
                "source_leaf": "",
                "source_image_abs": "",
                "route_note": row["route_note"],
            }
        )

    contact_sheet = draw_contact_sheet(crop_rows)

    crop_csv = REPORTS / "campaign_032_002_branch_tail_source_crops.csv"
    route_csv = REPORTS / "campaign_032_002_branch_tail_source_routes.csv"
    summary_json = REPORTS / "campaign_032_002_branch_tail_source_acquisition_summary.json"

    with crop_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(crop_rows[0].keys()))
        writer.writeheader()
        writer.writerows(crop_rows)

    with route_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(route_rows[0].keys()))
        writer.writeheader()
        writer.writerows(route_rows)

    summary = {
        "source_visible_public_cisi_rows": 3,
        "source_visible_public_cisi_crops": len(crop_rows),
        "newly_upgraded_rows": ["M-240", "M-91", "M-70"],
        "still_blocked_rows": ["M-1677", "3335.1"],
        "route_csv": str(route_csv.resolve()),
        "crop_csv": str(crop_csv.resolve()),
        "contact_sheet": str(contact_sheet.resolve()),
    }
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
