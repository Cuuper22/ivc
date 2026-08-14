#!/usr/bin/env python3
"""Emit the cleaned v2d manual shortlist for the directionality panel-crop repair.

After the panel-crop repair script generated hundreds of candidate crops, a
human looked at them and hand-picked 16: 4 targets, 9 negatives, and 3
reserves. This script simply records that choice in a reproducible form. Each
pick is identified by (CISI, route rank, crop method, candidate rank); the
script looks those rows up in the v2 candidates CSV, stamps them with the draft
version and the reviewer's bucket and note, and writes a shortlist CSV plus a
contact sheet for the next visual pass. It is deliberately conservative: it
claims no blind-packet denominator, only a transparent visual-QC draft that
strips the obvious label/metadata leaks before any blind review exists.
"""

from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "data" / "open_prototype" / "reports"
TMP_DIR = ROOT / "tmp" / "effective_unicity_directionality_panel_crop_repair"

SOURCE_CSV = REPORT_DIR / "effective_unicity_directionality_panel_crop_repair_v2_candidates.csv"
OUT_CSV = REPORT_DIR / "effective_unicity_directionality_panel_crop_repair_v2d_manual_shortlist_clean_draft.csv"
OUT_CONTACT_SHEET = TMP_DIR / "visual_qc_manual_shortlist_v2d_clean_draft.jpg"


SELECTIONS = [
    ("H-654", "1", "above_label_wide_darkrow_above_cluster", "20", "target", "visual draft: label-free signband candidate"),
    ("M-1310", "1", "above_label_wide_darkrow_above_cluster", "20", "target", "visual draft: label-free signband candidate"),
    ("M-1320", "1", "above_label_wide_darkrow_above_cluster", "20", "target", "visual draft: label-free signband candidate"),
    ("M-811", "1", "above_label_wide_darkrow_above_cluster", "20", "target", "visual draft: label-free signband candidate"),
    ("H-158", "1", "component_nearest_high_score", "4", "negative", "replacement for page-context draft crop; tighter label-free component"),
    ("H-665", "1", "component_nearest_high_score", "4", "negative", "replacement for leaked H-662 page-context crop; tighter component"),
    ("M-1315", "1", "component_nearest_high_score", "4", "negative", "replacement/tighter component candidate"),
    ("M-1458", "1", "component_nearest_high_score", "4", "negative", "replacement/tighter component candidate"),
    ("M-1523", "1", "component_nearest_high_score", "4", "negative", "replacement/tighter component candidate"),
    ("M-171", "1", "component_nearest_high_score", "4", "negative", "replacement/tighter component candidate"),
    ("M-365", "1", "above_label_wide_darkrow_above_cluster", "20", "negative", "visual draft: label-free signband candidate"),
    ("M-386", "1", "above_label_wide_darkrow_above_cluster", "20", "negative", "visual draft: label-free signband candidate"),
    ("M-527", "1", "component_nearest_high_score", "4", "negative", "replacement/tighter component candidate"),
    ("H-421", "1", "above_label_wide_darkrow_above_cluster", "20", "reserve", "reserve: label-free object panel, broader iconographic crop"),
    ("M-127", "1", "above_label_wide_darkrow_above_cluster", "20", "reserve", "reserve: label-free object panel, broader iconographic crop"),
    ("M-1322", "1", "above_label_wide_darkrow_above_cluster", "20", "reserve", "reserve: label-free signband/object-panel crop"),
]


def read_candidates() -> tuple[list[str], dict[tuple[str, str, str, str], list[dict[str, str]]]]:
    with SOURCE_CSV.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    index: dict[tuple[str, str, str, str], list[dict[str, str]]] = {}
    for row in rows:
        key = (row["cisi"], row["route_rank"], row["method"], row["candidate_rank"])
        index.setdefault(key, []).append(row)
    return fieldnames, index


def select_rows(fieldnames: list[str], index: dict[tuple[str, str, str, str], list[dict[str, str]]]) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    for cisi, route, method, rank, bucket, note in SELECTIONS:
        key = (cisi, route, method, rank)
        matches = index.get(key)
        if not matches:
            raise RuntimeError(f"Missing shortlist row {key}")
        row = dict(matches[0])
        row["visual_qc_selected_draft_version"] = "v2d_clean_draft_2026_05_29"
        row["manual_visual_qc_bucket"] = bucket
        row["manual_visual_qc_note"] = note
        selected.append(row)
    return selected


def write_csv(fieldnames: list[str], selected: list[dict[str, str]]) -> None:
    out_fields = fieldnames + [
        "visual_qc_selected_draft_version",
        "manual_visual_qc_bucket",
        "manual_visual_qc_note",
    ]
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=out_fields)
        writer.writeheader()
        writer.writerows(selected)


def make_contact_sheet(selected: list[dict[str, str]]) -> None:
    thumb_w, thumb_h = 420, 250
    pad = 18
    label_h = 56
    cols = 2
    rows = (len(selected) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (thumb_w + pad) + pad, rows * (thumb_h + label_h + pad) + pad), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
        small = ImageFont.truetype("arial.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
        small = ImageFont.load_default()

    for i, row in enumerate(selected):
        x = pad + (i % cols) * (thumb_w + pad)
        y = pad + (i // cols) * (thumb_h + label_h + pad)
        img_path = ROOT / row["source_crop"]
        img = Image.open(img_path).convert("RGB")
        img.thumbnail((thumb_w, thumb_h), Image.LANCZOS)
        frame = Image.new("RGB", (thumb_w, thumb_h), (245, 245, 245))
        frame.paste(img, ((thumb_w - img.width) // 2, (thumb_h - img.height) // 2))
        sheet.paste(frame, (x, y + label_h))
        label = f"{i + 1:02d} {row['manual_visual_qc_bucket'].upper()} {row['cisi']} r{row['route_rank']} c{row['candidate_rank']}"
        draw.text((x, y), label, fill=(0, 0, 0), font=font)
        draw.text((x, y + 25), row["method"][:55], fill=(55, 55, 55), font=small)
        draw.rectangle([x, y + label_h, x + thumb_w - 1, y + label_h + thumb_h - 1], outline=(180, 180, 180), width=1)

    OUT_CONTACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT_CONTACT_SHEET, quality=92)


def main() -> None:
    fieldnames, index = read_candidates()
    selected = select_rows(fieldnames, index)
    write_csv(fieldnames, selected)
    make_contact_sheet(selected)
    print(f"wrote {OUT_CSV}")
    print(f"wrote {OUT_CONTACT_SHEET}")
    print("selected 16 rows: targets=4, negatives=9, reserves=3")


if __name__ == "__main__":
    main()
