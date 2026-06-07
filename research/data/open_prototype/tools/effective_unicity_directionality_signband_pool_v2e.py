#!/usr/bin/env python3
"""
Build a wider signband-like crop pool from the corrected directionality route probe.

This is a preflight inventory, not a blind packet. It exists because the cleaned
v2d shortlist still mixes crop worlds: some targets are signband strips while
some controls are full object/icon panels. The v2e pool widens the candidate
universe so a later packet can pre-register a denominator from comparable
signband-like crops only.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[3]
RUN_DATE = "2026-05-29"
POOL_ID = "directionality_signband_pool_v2e_wide_route_candidates"

REPORTS = ROOT / "data" / "open_prototype" / "reports"
ROUTES_CSV = REPORTS / "effective_unicity_directionality_public_route_probe_v2_routes.csv"
OUT_DIR = ROOT / "tmp" / "effective_unicity_directionality_signband_pool_v2e"
CROP_DIR = OUT_DIR / "candidates"
CONTACT_SHEET = OUT_DIR / "directionality_signband_pool_v2e_ranked_candidates.jpg"
TARGET_CONTACT_SHEET = OUT_DIR / "directionality_signband_pool_v2e_target_candidates.jpg"

CANDIDATES_CSV = REPORTS / "effective_unicity_directionality_signband_pool_v2e_candidates.csv"
SUMMARY_JSON = REPORTS / "effective_unicity_directionality_signband_pool_v2e_summary.json"

PANEL_TOOL = ROOT / "data" / "open_prototype" / "tools" / "effective_unicity_directionality_panel_crop_repair.py"
PRIMARY_TARGET_CISIS = {"H-654", "M-1310", "M-1320", "M-811"}


EXTRA_FIELDS = [
    "signband_pool_id",
    "signband_like_score",
    "signband_like_bucket",
    "v2e_rank_within_cisi",
    "v2e_global_rank",
]


def load_panel_tool():
    spec = importlib.util.spec_from_file_location("panel_repair", PANEL_TOOL)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {PANEL_TOOL}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.CROP_DIR = CROP_DIR
    return module


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def route_sort_key(row: dict[str, str]) -> tuple[int, int, int]:
    grade_penalty = 0 if row.get("source_grade_status", "").startswith("public_cisi_plate_route_candidate") else 1
    try:
        rank = int(row.get("route_rank", "999"))
    except ValueError:
        rank = 999
    try:
        queue_rank = int(row.get("queue_rank", "9999"))
    except ValueError:
        queue_rank = 9999
    return grade_penalty, rank, queue_rank


def selected_routes(max_routes_per_cisi: int = 2) -> list[dict[str, str]]:
    by_cisi: dict[str, list[dict[str, str]]] = {}
    for row in read_csv(ROUTES_CSV):
        if not row.get("source_grade_status", "").startswith("public_cisi_plate_route_candidate"):
            continue
        if row.get("route_status") != "downloaded_and_cropped":
            continue
        by_cisi.setdefault(row["representative_cisi"], []).append(row)
    routes: list[dict[str, str]] = []
    for cisi in sorted(by_cisi):
        routes.extend(sorted(by_cisi[cisi], key=route_sort_key)[:max_routes_per_cisi])
    return routes


def signband_score(row: dict[str, object]) -> tuple[float, str]:
    width = float(row.get("crop_width") or 0)
    height = float(row.get("crop_height") or 1)
    aspect = width / max(1.0, height)
    word_overlap = int(row.get("ocr_word_overlap_count") or 0)
    label_overlap = float(row.get("label_box_overlap_fraction") or 0.0)
    dark = float(row.get("dark_pixel_fraction") or 0.0)
    method = str(row.get("method") or "")
    status = str(row.get("candidate_preflight_status") or "")
    score = 0.0
    if status == "candidate_requires_visual_label_leak_and_single_panel_preflight":
        score += 3.0
    if word_overlap == 0:
        score += 1.5
    if label_overlap == 0:
        score += 1.5
    if 1.9 <= aspect <= 5.5:
        score += 2.0
    elif 1.4 <= aspect < 1.9 or 5.5 < aspect <= 7.0:
        score += 0.7
    if 150 <= height <= 620:
        score += 1.3
    if 450 <= width <= 1600:
        score += 1.0
    if 0.18 <= dark <= 0.72:
        score += 0.8
    if "darkrow" in method:
        score += 1.0
    if method.startswith("component"):
        score += 0.4
    if method in {"above_label_wide", "below_label_wide", "around_label_without_center_label"}:
        score -= 1.3
    if word_overlap or label_overlap:
        score -= 4.0
    if aspect < 1.25:
        score -= 1.5
    if height > 780:
        score -= 1.5
    if score >= 9.0:
        bucket = "strong_signband_like_geometry_needs_visual_qc"
    elif score >= 7.0:
        bucket = "possible_signband_like_geometry_needs_visual_qc"
    elif score >= 5.0:
        bucket = "weak_or_mixed_crop_geometry"
    else:
        bucket = "reject_for_v2e_signband_pool"
    return round(score, 6), bucket


def copy_with_pool_paths(row: dict[str, object]) -> dict[str, object]:
    out = dict(row)
    for key in ("source_crop", "enhanced_crop"):
        src = ROOT / str(row[key])
        dst = CROP_DIR / src.name
        if src.resolve() != dst.resolve():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
        out[key] = str(dst.relative_to(ROOT)).replace("\\", "/")
    return out


def make_contact_sheet(rows: list[dict[str, object]], output: Path, title: str, limit: int = 72) -> None:
    selected = rows[:limit]
    if not selected:
        return
    try:
        font = ImageFont.truetype("arial.ttf", 18)
        small = ImageFont.truetype("arial.ttf", 13)
    except OSError:
        font = ImageFont.load_default()
        small = ImageFont.load_default()
    cell_w = 560
    cell_h = 430
    cols = 3
    header_h = 48
    sheet = Image.new("RGB", (cols * cell_w, header_h + ((len(selected) + cols - 1) // cols) * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    draw.text((16, 14), title, fill=(0, 0, 0), font=font)
    for index, row in enumerate(selected):
        col = index % cols
        row_index = index // cols
        x = col * cell_w + 14
        y = header_h + row_index * cell_h + 92
        tx = col * cell_w + 14
        ty = header_h + row_index * cell_h + 10
        image = Image.open(ROOT / str(row["source_crop"])).convert("RGB")
        image.thumbnail((cell_w - 28, 300), Image.Resampling.LANCZOS)
        label = f"{row['v2e_global_rank']:03d} {row['cisi']} {row['role']} r{row['route_rank']} c{row['candidate_rank']}"
        draw.text((tx, ty), label[:68], fill=(0, 0, 0), font=small)
        draw.text((tx, ty + 20), str(row["method"])[:72], fill=(40, 40, 40), font=small)
        draw.text((tx, ty + 40), f"score {row['signband_like_score']} {row['signband_like_bucket']}"[:72], fill=(80, 40, 40), font=small)
        draw.text((tx, ty + 60), str(row["match_text"])[:72], fill=(70, 70, 70), font=small)
        sheet.paste(image, (x, y))
        draw.rectangle((x - 1, y - 1, x + image.width + 1, y + image.height + 1), outline=(180, 180, 180), width=1)
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)


def main() -> None:
    CROP_DIR.mkdir(parents=True, exist_ok=True)
    panel = load_panel_tool()
    page_words = panel.load_page_words()
    routes = selected_routes(max_routes_per_cisi=2)

    generated: list[dict[str, object]] = []
    for route in routes:
        generated.extend(panel.candidates_for_route(route, page_words))

    rows = []
    by_cisi_rank: dict[str, int] = {}
    for row in generated:
        score, bucket = signband_score(row)
        out = copy_with_pool_paths(row)
        out["signband_pool_id"] = POOL_ID
        out["signband_like_score"] = score
        out["signband_like_bucket"] = bucket
        by_cisi_rank[str(out["cisi"])] = by_cisi_rank.get(str(out["cisi"]), 0) + 1
        out["v2e_rank_within_cisi"] = by_cisi_rank[str(out["cisi"])]
        rows.append(out)

    rows.sort(
        key=lambda row: (
            0 if row["cisi"] in PRIMARY_TARGET_CISIS else 1,
            -float(row["signband_like_score"]),
            int(row["queue_rank"]),
            str(row["cisi"]),
            int(row["route_rank"]),
            int(row["candidate_rank"]),
        )
    )
    for index, row in enumerate(rows, start=1):
        row["v2e_global_rank"] = index

    fields = panel.CANDIDATE_FIELDS + EXTRA_FIELDS
    write_csv(CANDIDATES_CSV, rows, fields)

    ranked_for_visual = [
        row
        for row in sorted(rows, key=lambda r: (-float(r["signband_like_score"]), int(r["queue_rank"]), str(r["cisi"])))
        if row["signband_like_bucket"] != "reject_for_v2e_signband_pool"
    ]
    make_contact_sheet(ranked_for_visual, CONTACT_SHEET, "v2e wider signband-like crop pool; visual preflight only", 72)
    make_contact_sheet([row for row in rows if row["cisi"] in PRIMARY_TARGET_CISIS], TARGET_CONTACT_SHEET, "v2e target candidate crops; visual preflight only", 48)

    by_bucket: dict[str, int] = {}
    by_role_bucket: dict[str, dict[str, int]] = {}
    cisis_by_bucket: dict[str, set[str]] = {}
    for row in rows:
        bucket = str(row["signband_like_bucket"])
        role = str(row["role"])
        by_bucket[bucket] = by_bucket.get(bucket, 0) + 1
        by_role_bucket.setdefault(role, {})[bucket] = by_role_bucket.setdefault(role, {}).get(bucket, 0) + 1
        cisis_by_bucket.setdefault(bucket, set()).add(str(row["cisi"]))

    non_target_strong_cisis = sorted(
        {
            str(row["cisi"])
            for row in rows
            if row["cisi"] not in PRIMARY_TARGET_CISIS
            and row["signband_like_bucket"] in {
                "strong_signband_like_geometry_needs_visual_qc",
                "possible_signband_like_geometry_needs_visual_qc",
            }
        }
    )
    target_strong_cisis = sorted(
        {
            str(row["cisi"])
            for row in rows
            if row["cisi"] in PRIMARY_TARGET_CISIS
            and row["signband_like_bucket"] in {
                "strong_signband_like_geometry_needs_visual_qc",
                "possible_signband_like_geometry_needs_visual_qc",
            }
        }
    )
    summary = {
        "date": RUN_DATE,
        "pool_id": POOL_ID,
        "status": "wide_signband_pool_created_for_visual_preflight_no_claim_promotion",
        "purpose": "Widen v2d beyond the mixed crop-world shortlist by ranking label-excluding public-route crop candidates for signband-like geometry before any blind packet is built.",
        "counts": {
            "public_plate_route_cisis": len({route["representative_cisi"] for route in routes}),
            "public_plate_routes_used_max_two_per_cisi": len(routes),
            "candidate_rows": len(rows),
            "primary_target_cisis_with_possible_or_strong_signband_geometry": len(target_strong_cisis),
            "non_target_cisis_with_possible_or_strong_signband_geometry": len(non_target_strong_cisis),
            "accepted_claims_increment": 0,
        },
        "by_signband_like_bucket": by_bucket,
        "by_role_bucket": by_role_bucket,
        "cisis_by_bucket": {key: sorted(value) for key, value in cisis_by_bucket.items()},
        "admissibility_gate": [
            "No v2e row is reviewer-ready from geometry alone.",
            "A future packet may pre-register only rows that pass human visual QC for no label/page cue and a comparable signband crop world.",
            "Targets and fixed real negatives must be selected from the same visual bucket and crop protocol before any blind review.",
            "Reserves may be promoted only before review and must be recorded as fixed denominator rows before scoring.",
            "This pool cannot promote physical direction, source-normalized token order, sign identity, meaning, phonetic value, language family, or translation.",
        ],
        "outputs": {
            "candidates_csv": str(CANDIDATES_CSV.relative_to(ROOT)).replace("\\", "/"),
            "summary_json": str(SUMMARY_JSON.relative_to(ROOT)).replace("\\", "/"),
            "ranked_contact_sheet": str(CONTACT_SHEET.relative_to(ROOT)).replace("\\", "/"),
            "target_contact_sheet": str(TARGET_CONTACT_SHEET.relative_to(ROOT)).replace("\\", "/"),
            "candidate_crop_dir": str(CROP_DIR.relative_to(ROOT)).replace("\\", "/"),
        },
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
