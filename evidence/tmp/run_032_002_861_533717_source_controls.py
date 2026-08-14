"""Builds register-control crops for the 533-717 gate.

This script carries two inline lists: TARGETS, the objects with locally stored page
images that can be cropped now, and PENDING, the objects whose source images still
need acquisition. For each target it cuts the panel and signband crops with PIL,
hashes them, and saves them under tmp/032_002_861_533717_register_controls. It writes
a crops CSV, a pending CSV, and a summary JSON to the reports directory. The point is
to give the 533-717 comparison real same-register control images instead of catalog
rows alone; no token identity or value is accepted by this script.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path.cwd()
OUT = ROOT / "tmp" / "032_002_861_533717_register_controls"
REPORTS = ROOT / "data" / "open_prototype" / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)


TARGETS = [
    {
        "cisi": "M-355",
        "role": "cuboid_convex_other_tail_control",
        "text": "+740-877-032-033-705-231-235-002-861-360-520-919-140+",
        "page": OUT / "india_n123.jpg",
        "source_route": "CISI India IA leaf n123 / printed p.88 / Mohenjo-daro 353-355 seals no iconography I",
        "reader_url": "https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India/page/n123/mode/1up",
        "panel_boxes": [
            ("A", (520, 2290, 1935, 2725)),
            ("a", (520, 2780, 2110, 3235)),
        ],
        "status": "source_visible_this_campaign",
    },
    {
        "cisi": "M-1267",
        "role": "rectangular_bare_control",
        "text": "+416-001-740-720-175-002-861+",
        "page": OUT / "pakistan_n194.jpg",
        "source_route": "CISI Pakistan IA leaf n194 / printed p.160 / Mohenjo-daro 1264-1268 seals no iconography I, II",
        "reader_url": "https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n194/mode/1up",
        "panel_boxes": [
            ("A", (215, 3000, 1065, 3630)),
            ("a", (215, 3740, 1070, 4285)),
        ],
        "status": "source_visible_this_campaign",
    },
    {
        "cisi": "M-1273",
        "role": "rectangular_603_control",
        "text": "+740-055-002-861-603+",
        "page": OUT / "pakistan_n195.jpg",
        "source_route": "CISI Pakistan IA leaf n195 / printed p.161 / Mohenjo-daro 1269-1274 seals no iconography II",
        "reader_url": "https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n195/mode/1up",
        "panel_boxes": [
            ("A", (260, 3180, 1060, 3655)),
            ("a", (260, 3850, 1085, 4325)),
        ],
        "status": "source_visible_existing_recropped_here",
    },
]

PENDING = [
    {
        "cisi": "M-1954",
        "role": "rectangular_bare_control",
        "text": "+740-407-590-031-752-033-705-220-415-798-002-861+",
        "source_route": "not located in current public CISI India/Pakistan panel OCR pass",
        "status": "source_pending_public_dark",
    },
    {
        "cisi": "M-1973",
        "role": "rectangular_bare_control",
        "text": "+740-575-017-233-550-002-861+",
        "source_route": "not located in current public CISI India/Pakistan panel OCR pass",
        "status": "source_pending_public_dark",
    },
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def crop_target(target: dict[str, object]) -> list[dict[str, str]]:
    page = Path(target["page"])
    if not page.exists():
        raise FileNotFoundError(page)
    image = Image.open(page).convert("RGB")
    rows: list[dict[str, str]] = []
    for side, box in target["panel_boxes"]:
        crop = image.crop(box)
        side_key = "obv_A" if side == "A" else "rev_a"
        crop_path = OUT / f"{target['cisi'].replace('-', '')}_{side_key}_register_control.png"
        crop.save(crop_path)
        rows.append(
            {
                "cisi": str(target["cisi"]),
                "side": str(side),
                "side_key": side_key,
                "role": str(target["role"]),
                "text": str(target["text"]),
                "status": str(target["status"]),
                "source_route": str(target["source_route"]),
                "reader_url": str(target["reader_url"]),
                "crop_box": ",".join(str(value) for value in box),
                "page_path": str(page.resolve()),
                "page_sha256": sha(page),
                "crop_path": str(crop_path.resolve()),
                "crop_sha256": sha(crop_path),
                "crop_width": str(crop.width),
                "crop_height": str(crop.height),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def contact_sheet(rows: list[dict[str, str]]) -> Path:
    thumbs = []
    for row in rows:
        img = Image.open(row["crop_path"]).convert("RGB")
        img.thumbnail((520, 180))
        canvas = Image.new("RGB", (540, 230), "white")
        canvas.paste(img, (10, 40))
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 8), f"{row['cisi']} {row['side']} {row['role']}", fill="black")
        draw.text((10, 25), row["status"], fill="black")
        thumbs.append(canvas)
    cols = 2
    rows_n = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 540, rows_n * 230), "white")
    for idx, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((idx % cols) * 540, (idx // cols) * 230))
    out = OUT / "533717_register_source_controls_contact_sheet.png"
    sheet.save(out)
    return out


def main() -> None:
    crop_rows: list[dict[str, str]] = []
    for target in TARGETS:
        crop_rows.extend(crop_target(target))

    pending_rows = [
        {
            "cisi": row["cisi"],
            "role": row["role"],
            "text": row["text"],
            "status": row["status"],
            "source_route": row["source_route"],
        }
        for row in PENDING
    ]
    sheet = contact_sheet(crop_rows)

    crops_csv = REPORTS / "campaign_032_002_861_533717_source_controls_crops.csv"
    pending_csv = REPORTS / "campaign_032_002_861_533717_source_controls_pending.csv"
    summary_json = REPORTS / "campaign_032_002_861_533717_source_controls_summary.json"

    write_csv(crops_csv, crop_rows, list(crop_rows[0].keys()))
    write_csv(pending_csv, pending_rows, list(pending_rows[0].keys()))

    payload = {
        "date": "2026-05-29",
        "source_visible_controls": ["M-355", "M-1267", "M-1273"],
        "source_pending_controls": ["M-1954", "M-1973"],
        "evidence_effect": "Three non-533-717 no-icon SEAL:R 002-861 controls now have public source panels for layout comparison.",
        "crops_csv": str(crops_csv.resolve()),
        "pending_csv": str(pending_csv.resolve()),
        "contact_sheet": str(sheet.resolve()),
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
