#!/usr/bin/env python3
"""Preflight check: can the v2e crop pool support a homogeneous blind packet?

This is a gate, not a packet — it decides whether a packet could be built, and
promotes nothing. v2d failed because it mixed signband strips with object/icon
panels and because its advertised fixed denominator was 9 controls, not the
promised 12. v2e widened the crop universe; v2f asks the narrower question:
can v2e supply matched signband strips without moving the goalposts?

The script reads the v2e candidate CSV and runs two lanes. The strict lane
keeps only v2e crops that already look like compact signband strips (aspect
ratio 2.0-5.5, height 120-520 px, width 450-1700 px, zero OCR-word and label
overlap). The derived lane cuts a fresh top strip out of each wide crop by
finding the darkest horizontal band in the upper 62% of the image. For each
lane it picks the best candidate per CISI, checks the four primary targets are
present, checks the 12 fixed real negatives are present, and flags source-page
collisions and duplicate image hashes. It writes two candidate CSVs, three
contact sheets, and a summary JSON whose status is hardwired to "failed
preflight": the strict lane lacks the targets, and the derived lane is
acquisition-only until human visual QC and pre-registered forger nulls exist.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[3]
RUN_DATE = "2026-05-29"
PREFLIGHT_ID = "directionality_homogeneous_signband_packet_v2f_preflight"

REPORTS = ROOT / "data" / "open_prototype" / "reports"
V2E_CSV = REPORTS / "effective_unicity_directionality_signband_pool_v2e_candidates.csv"

OUT_DIR = ROOT / "tmp" / "effective_unicity_directionality_homogeneous_packet_v2f"
STRICT_CONTACT = OUT_DIR / "directionality_homogeneous_packet_v2f_strict_reuse_contact_sheet.jpg"
DERIVED_CONTACT = OUT_DIR / "directionality_homogeneous_packet_v2f_derived_top_strip_contact_sheet.jpg"
TARGET_CONTACT = OUT_DIR / "directionality_homogeneous_packet_v2f_target_gate_contact_sheet.jpg"
DERIVED_CROP_DIR = OUT_DIR / "derived_top_strips"

STRICT_CSV = REPORTS / "effective_unicity_directionality_homogeneous_packet_v2f_strict_reuse_candidates.csv"
DERIVED_CSV = REPORTS / "effective_unicity_directionality_homogeneous_packet_v2f_derived_top_strip_candidates.csv"
SUMMARY_JSON = REPORTS / "effective_unicity_directionality_homogeneous_packet_v2f_preflight_summary.json"

PRIMARY_TARGET_CISIS = {"H-654", "M-1310", "M-1320", "M-811"}

ORIGINAL_FIXED_REAL_NEGATIVE_CISIS = {
    "H-665",
    "M-1458",
    "M-1523",
    "M-525",
    "M-365",
    "M-527",
    "M-534",
    "M-1315",
    "M-386",
    "H-158",
    "M-171",
    "M-567",
}

STRICT_EXTRA_FIELDS = [
    "v2f_preflight_id",
    "v2f_lane",
    "v2f_candidate_status",
    "v2f_gate_notes",
    "accepted_claims_increment",
]

DERIVED_EXTRA_FIELDS = [
    "v2f_preflight_id",
    "v2f_lane",
    "v2f_source_crop",
    "v2f_source_crop_sha256",
    "v2f_derived_crop",
    "v2f_derived_crop_sha256",
    "v2f_derived_crop_box_xyxy",
    "v2f_derived_width",
    "v2f_derived_height",
    "v2f_derived_aspect_ratio",
    "v2f_derived_dark_pixel_fraction",
    "v2f_derived_strip_score",
    "v2f_candidate_status",
    "v2f_gate_notes",
    "accepted_claims_increment",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def to_float(row: dict[str, Any], key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key) or default)
    except (TypeError, ValueError):
        return default


def to_int(row: dict[str, Any], key: str, default: int = 0) -> int:
    try:
        return int(float(row.get(key) or default))
    except (TypeError, ValueError):
        return default


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dark_fraction(image: Image.Image) -> float:
    arr = np.asarray(ImageOps.grayscale(image))
    return round(float((arr < 215).mean()), 6)


def slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")


def strict_reuse_gate(row: dict[str, str]) -> tuple[bool, str]:
    if row.get("candidate_preflight_status") != "candidate_requires_visual_label_leak_and_single_panel_preflight":
        return False, "mechanical_preflight_failed"
    if row.get("signband_like_bucket") not in {
        "strong_signband_like_geometry_needs_visual_qc",
        "possible_signband_like_geometry_needs_visual_qc",
    }:
        return False, "not_strong_or_possible_signband_geometry"
    if to_int(row, "ocr_word_overlap_count") != 0:
        return False, "ocr_word_overlap"
    if to_float(row, "label_box_overlap_fraction") != 0.0:
        return False, "label_box_overlap"
    aspect = to_float(row, "crop_aspect_ratio")
    height = to_float(row, "crop_height")
    width = to_float(row, "crop_width")
    if not (2.0 <= aspect <= 5.5):
        return False, "aspect_outside_compact_signband_range"
    if not (120 <= height <= 520):
        return False, "height_outside_compact_signband_range"
    if not (450 <= width <= 1700):
        return False, "width_outside_compact_signband_range"
    return True, "strict_reuse_candidate_requires_human_visual_qc"


def candidate_sort_key(row: dict[str, Any]) -> tuple[int, float, int, int, str]:
    bucket_rank = {
        "strong_signband_like_geometry_needs_visual_qc": 0,
        "possible_signband_like_geometry_needs_visual_qc": 1,
        "weak_or_mixed_crop_geometry": 2,
        "reject_for_v2e_signband_pool": 3,
    }.get(str(row.get("signband_like_bucket")), 9)
    return (
        bucket_rank,
        -to_float(row, "signband_like_score"),
        to_int(row, "route_rank", 999),
        to_int(row, "candidate_rank", 999),
        str(row.get("source_crop", "")),
    )


def best_by_cisi(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["cisi"])].append(row)
    return {cisi: sorted(candidates, key=candidate_sort_key)[0] for cisi, candidates in grouped.items()}


def source_page_collisions(
    selected: dict[str, dict[str, Any]],
    target_cisis: set[str] = PRIMARY_TARGET_CISIS,
) -> list[dict[str, str]]:
    targets = {
        cisi: row
        for cisi, row in selected.items()
        if cisi in target_cisis
    }
    collisions = []
    for target_cisi, target in targets.items():
        target_page = str(target.get("source_page_sha256") or target.get("source_page"))
        for cisi, row in selected.items():
            if cisi in target_cisis:
                continue
            page = str(row.get("source_page_sha256") or row.get("source_page"))
            if page and page == target_page:
                collisions.append(
                    {
                        "target_cisi": target_cisi,
                        "control_cisi": cisi,
                        "source_page": str(row.get("source_page")),
                        "source_page_sha256": str(row.get("source_page_sha256")),
                    }
                )
    return collisions


def duplicate_hash_groups(rows: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        value = str(row.get(key) or "")
        if value:
            groups[value].append(row)
    out = []
    for digest, members in groups.items():
        cisis = sorted({str(member.get("cisi")) for member in members})
        if len(cisis) > 1:
            out.append(
                {
                    "sha256": digest,
                    "cisis": cisis,
                    "rows": len(members),
                }
            )
    return out


def smooth(values: np.ndarray, window: int = 13) -> np.ndarray:
    if len(values) < window:
        return values
    kernel = np.ones(window) / window
    return np.convolve(values, kernel, mode="same")


def active_clusters(active: np.ndarray, allowed_gap: int = 18) -> list[tuple[int, int]]:
    clusters: list[tuple[int, int]] = []
    start: int | None = None
    last = -1
    for index, is_active in enumerate(active.tolist()):
        if is_active:
            if start is None:
                start = index
            last = index
        elif start is not None and index - last > allowed_gap:
            clusters.append((start, last + 1))
            start = None
    if start is not None:
        clusters.append((start, last + 1))
    return clusters


def derive_top_strip(row: dict[str, str]) -> dict[str, Any] | None:
    source_path = ROOT / row["source_crop"]
    image = Image.open(source_path).convert("RGB")
    gray = ImageOps.grayscale(image)
    arr = np.asarray(gray)
    dark = arr < 215
    height, width = dark.shape
    upper_limit = max(120, min(height, int(height * 0.62)))
    row_fraction = smooth(dark[:upper_limit].mean(axis=1), window=15)
    threshold = max(0.014, float(np.quantile(row_fraction, 0.58)))
    clusters = active_clusters(row_fraction > threshold, allowed_gap=20)

    candidates = []
    for y1, y2 in clusters:
        if y2 - y1 < 45:
            continue
        sub = dark[y1:y2, :]
        col_fraction = smooth(sub.mean(axis=0), window=21)
        col_threshold = max(0.006, float(np.quantile(col_fraction, 0.52)))
        xs = np.nonzero(col_fraction > col_threshold)[0]
        if not len(xs):
            continue
        x1 = int(xs.min())
        x2 = int(xs.max()) + 1
        if x2 - x1 < 260:
            continue
        pad_x = max(18, int(width * 0.015))
        pad_y = max(14, int((y2 - y1) * 0.08))
        box = (
            max(0, x1 - pad_x),
            max(0, y1 - pad_y),
            min(width, x2 + pad_x),
            min(height, y2 + pad_y),
        )
        bw = box[2] - box[0]
        bh = box[3] - box[1]
        aspect = bw / max(1, bh)
        dark_area = int(sub[:, x1:x2].sum())
        vertical_bonus = 1.0 - min(1.0, ((box[1] + box[3]) / 2.0) / max(1.0, height))
        score = dark_area * max(0.15, aspect) * vertical_bonus / max(1, bh)
        candidates.append((score, box))

    if not candidates:
        return None
    _, box = sorted(candidates, key=lambda item: -item[0])[0]
    crop = image.crop(box).convert("RGB")
    bw, bh = crop.size
    aspect = bw / max(1, bh)
    status = "derived_top_strip_candidate_requires_human_visual_qc"
    notes = []
    if not (1.85 <= aspect <= 6.2):
        status = "derived_top_strip_mechanical_reject"
        notes.append("aspect_outside_derived_strip_range")
    if not (95 <= bh <= 570):
        status = "derived_top_strip_mechanical_reject"
        notes.append("height_outside_derived_strip_range")
    if bw < 320:
        status = "derived_top_strip_mechanical_reject"
        notes.append("width_too_small")

    DERIVED_CROP_DIR.mkdir(parents=True, exist_ok=True)
    output_name = (
        f"{slug(str(row['cisi']))}_r{row['route_rank']}_c{row['candidate_rank']}_"
        f"{slug(str(row['method']))}_derived_top_strip.png"
    )
    output_path = DERIVED_CROP_DIR / output_name
    crop.save(output_path)
    return {
        "box": box,
        "path": output_path,
        "sha256": sha256_file(output_path),
        "width": bw,
        "height": bh,
        "aspect": round(aspect, 6),
        "dark_fraction": dark_fraction(crop),
        "score": round(float(sorted(candidates, key=lambda item: -item[0])[0][0]), 6),
        "status": status,
        "notes": ";".join(notes) if notes else "derived from v2e source crop; acquisition-only until human visual preflight confirms no icon/context leakage",
    }


def make_contact_sheet(rows: list[dict[str, Any]], output: Path, title: str, image_key: str, limit: int = 48) -> None:
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
    cell_h = 390
    cols = 3
    header_h = 48
    rows_needed = (len(selected) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, header_h + rows_needed * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    draw.text((16, 14), title, fill=(0, 0, 0), font=font)
    for index, row in enumerate(selected):
        col = index % cols
        row_index = index // cols
        x = col * cell_w + 14
        y = header_h + row_index * cell_h + 82
        tx = col * cell_w + 14
        ty = header_h + row_index * cell_h + 10
        path_value = row.get(image_key) or row.get("source_crop")
        path = ROOT / str(path_value)
        image = Image.open(path).convert("RGB")
        image.thumbnail((cell_w - 28, 270), Image.Resampling.LANCZOS)
        label = f"{index + 1:02d} {row['cisi']} {row['role']} r{row['route_rank']} c{row['candidate_rank']}"
        draw.text((tx, ty), label[:68], fill=(0, 0, 0), font=small)
        draw.text((tx, ty + 20), str(row["method"])[:72], fill=(40, 40, 40), font=small)
        draw.text((tx, ty + 40), str(row.get("v2f_candidate_status", ""))[:72], fill=(80, 40, 40), font=small)
        draw.text((tx, ty + 60), f"score {row.get('signband_like_score', '')} {row.get('signband_like_bucket', '')}"[:72], fill=(70, 70, 70), font=small)
        sheet.paste(image, (x, y))
        draw.rectangle((x - 1, y - 1, x + image.width + 1, y + image.height + 1), outline=(180, 180, 180), width=1)
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)


def summarize_lane(rows: list[dict[str, Any]], selected: dict[str, dict[str, Any]], hash_key: str) -> dict[str, Any]:
    target_available = sorted(set(selected) & PRIMARY_TARGET_CISIS)
    fixed_negative_available = sorted(set(selected) & ORIGINAL_FIXED_REAL_NEGATIVE_CISIS)
    non_target_available = sorted(cisi for cisi in selected if cisi not in PRIMARY_TARGET_CISIS)
    return {
        "candidate_rows": len(rows),
        "unique_cisis": len(selected),
        "target_available": target_available,
        "target_missing": sorted(PRIMARY_TARGET_CISIS - set(target_available)),
        "fixed_real_negative_unique_count": len(fixed_negative_available),
        "fixed_real_negative_available": fixed_negative_available,
        "all_non_target_unique_count": len(non_target_available),
        "all_non_target_available": non_target_available,
        "target_control_source_page_collisions": source_page_collisions(selected),
        "exact_duplicate_hash_groups": duplicate_hash_groups(list(selected.values()), hash_key),
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    v2e_rows = read_csv(V2E_CSV)

    strict_rows: list[dict[str, Any]] = []
    rejected_strict_reasons: dict[str, int] = defaultdict(int)
    for row in v2e_rows:
        passed, reason = strict_reuse_gate(row)
        if not passed:
            rejected_strict_reasons[reason] += 1
            continue
        out = dict(row)
        out.update(
            {
                "v2f_preflight_id": PREFLIGHT_ID,
                "v2f_lane": "strict_v2e_reuse_compact_signband_strip",
                "v2f_candidate_status": "strict_reuse_candidate_requires_human_visual_qc",
                "v2f_gate_notes": reason,
                "accepted_claims_increment": 0,
            }
        )
        strict_rows.append(out)

    strict_selected = best_by_cisi(strict_rows)
    strict_selected_rows = sorted(strict_selected.values(), key=lambda row: (0 if row["cisi"] in PRIMARY_TARGET_CISIS else 1, str(row["cisi"])))

    derived_rows: list[dict[str, Any]] = []
    derived_attempts = 0
    derived_failures: dict[str, int] = defaultdict(int)
    for row in v2e_rows:
        if row.get("candidate_preflight_status") != "candidate_requires_visual_label_leak_and_single_panel_preflight":
            continue
        if to_int(row, "ocr_word_overlap_count") != 0 or to_float(row, "label_box_overlap_fraction") != 0.0:
            continue
        if to_float(row, "crop_width") < 450 or to_float(row, "crop_height") < 240:
            continue
        if row.get("signband_like_bucket") == "reject_for_v2e_signband_pool":
            continue
        derived_attempts += 1
        derived = derive_top_strip(row)
        if not derived:
            derived_failures["no_active_top_strip_cluster"] += 1
            continue
        if derived["status"] != "derived_top_strip_candidate_requires_human_visual_qc":
            derived_failures[derived["notes"]] += 1
            continue
        out = dict(row)
        out.update(
            {
                "v2f_preflight_id": PREFLIGHT_ID,
                "v2f_lane": "derived_top_strip_acquisition_not_blind_packet",
                "v2f_source_crop": row["source_crop"],
                "v2f_source_crop_sha256": row["source_crop_sha256"],
                "v2f_derived_crop": str(derived["path"].relative_to(ROOT)).replace("\\", "/"),
                "v2f_derived_crop_sha256": derived["sha256"],
                "v2f_derived_crop_box_xyxy": "|".join(str(int(value)) for value in derived["box"]),
                "v2f_derived_width": derived["width"],
                "v2f_derived_height": derived["height"],
                "v2f_derived_aspect_ratio": derived["aspect"],
                "v2f_derived_dark_pixel_fraction": derived["dark_fraction"],
                "v2f_derived_strip_score": derived["score"],
                "v2f_candidate_status": derived["status"],
                "v2f_gate_notes": derived["notes"],
                "accepted_claims_increment": 0,
            }
        )
        derived_rows.append(out)

    derived_selected = best_by_cisi(derived_rows)
    derived_selected_rows = sorted(
        derived_selected.values(),
        key=lambda row: (0 if row["cisi"] in PRIMARY_TARGET_CISIS else 1, str(row["cisi"])),
    )

    v2e_fields = list(v2e_rows[0].keys()) if v2e_rows else []
    write_csv(STRICT_CSV, strict_rows, v2e_fields + [field for field in STRICT_EXTRA_FIELDS if field not in v2e_fields])
    write_csv(DERIVED_CSV, derived_rows, v2e_fields + [field for field in DERIVED_EXTRA_FIELDS if field not in v2e_fields])

    make_contact_sheet(strict_selected_rows, STRICT_CONTACT, "v2f strict reuse gate: best candidate per CISI", "source_crop")
    make_contact_sheet(derived_selected_rows, DERIVED_CONTACT, "v2f derived top-strip gate: best candidate per CISI", "v2f_derived_crop")
    target_rows = [
        row for row in derived_selected_rows if row["cisi"] in PRIMARY_TARGET_CISIS
    ] + [
        row for row in strict_selected_rows if row["cisi"] in PRIMARY_TARGET_CISIS
    ]
    make_contact_sheet(target_rows, TARGET_CONTACT, "v2f target availability gate: derived first, strict second", "v2f_derived_crop" if target_rows and "v2f_derived_crop" in target_rows[0] else "source_crop")

    strict_summary = summarize_lane(strict_rows, strict_selected, "source_crop_sha256")
    derived_summary = summarize_lane(derived_rows, derived_selected, "v2f_derived_crop_sha256")

    strict_can_form_fixed_packet = (
        not strict_summary["target_missing"]
        and strict_summary["fixed_real_negative_unique_count"] >= 12
        and not strict_summary["target_control_source_page_collisions"]
        and not strict_summary["exact_duplicate_hash_groups"]
    )
    derived_can_form_acquisition_packet = (
        not derived_summary["target_missing"]
        and derived_summary["all_non_target_unique_count"] >= 12
        and not derived_summary["target_control_source_page_collisions"]
        and not derived_summary["exact_duplicate_hash_groups"]
    )

    status = "failed_preflight_no_blind_packet_promoted"
    automatic_fail_gates = []
    if strict_summary["target_missing"]:
        automatic_fail_gates.append("strict_reuse_lane_missing_target_cisis")
    if strict_summary["fixed_real_negative_unique_count"] < 12:
        automatic_fail_gates.append("strict_reuse_lane_has_fewer_than_12_original_fixed_real_negatives")
    if strict_summary["target_control_source_page_collisions"]:
        automatic_fail_gates.append("strict_reuse_lane_has_target_control_source_page_collisions")
    if derived_summary["target_control_source_page_collisions"]:
        automatic_fail_gates.append("derived_lane_has_target_control_source_page_collisions")
    if derived_can_form_acquisition_packet:
        automatic_fail_gates.append("derived_lane_is_acquisition_only_not_a_blind_packet_until_visual_qc_and_forger_nulls")

    summary = {
        "date": RUN_DATE,
        "preflight_id": PREFLIGHT_ID,
        "input_v2e_candidates_csv": str(V2E_CSV.relative_to(ROOT)).replace("\\", "/"),
        "status": status,
        "accepted_claims_increment": 0,
        "strict_can_form_fixed_packet": strict_can_form_fixed_packet,
        "derived_can_form_acquisition_packet_before_visual_review": derived_can_form_acquisition_packet,
        "automatic_fail_gates": automatic_fail_gates,
        "strict_reuse_lane": strict_summary,
        "strict_reject_reason_counts": dict(sorted(rejected_strict_reasons.items())),
        "derived_top_strip_lane": derived_summary | {
            "attempted_source_rows": derived_attempts,
            "mechanical_failure_counts": dict(sorted(derived_failures.items())),
        },
        "output_artifacts": {
            "strict_candidates_csv": str(STRICT_CSV.relative_to(ROOT)).replace("\\", "/"),
            "derived_candidates_csv": str(DERIVED_CSV.relative_to(ROOT)).replace("\\", "/"),
            "strict_contact_sheet": str(STRICT_CONTACT.relative_to(ROOT)).replace("\\", "/"),
            "derived_contact_sheet": str(DERIVED_CONTACT.relative_to(ROOT)).replace("\\", "/"),
            "target_contact_sheet": str(TARGET_CONTACT.relative_to(ROOT)).replace("\\", "/"),
        },
        "no_promotion_reason": (
            "The strict v2e reuse lane cannot form the claimed packet because it lacks all four compact target "
            "signbands and has fewer than 12 original fixed real negatives. The derived top-strip lane is useful "
            "crop-acquisition infrastructure, but it is not a blind packet: it still requires human visual preflight, "
            "pre-registered forger/null packets, and a fresh fixed denominator before any directionality claim can be tested."
        ),
        "next_gate_requirements": [
            "Human visual review must mark each selected derived strip as no label, no page-context sliver, exactly one comparable signband, and no icon/object cue dominating the crop.",
            "A fixed denominator of at least 12 real non-target CISIs must be pre-registered before any reviewer sees randomized packets.",
            "A matched synthetic forger set must include planted directionality, planted non-linguistic emblem/order structure, and frequency-matched noise at the same packet size.",
            "Reviewer true-positive and false-positive rates must be reported before any accepted claim ledger increment.",
        ],
        "minimum_future_v2f_forger_requirements": {
            "required_blind_reviewers": 3,
            "fixed_denominators": {
                "real_signband_negative_unique_cisis": {
                    "minimum": 12,
                    "rule": "Fixed before review; no reserve promotion after packet creation; same crop world as targets."
                },
                "real_nonlinguistic_null_unique_source_crops": {
                    "minimum": 12,
                    "rule": "Source-real icon-only, animal-only, blank/damaged/non-script bands matched for dimensions, contrast, and page quality."
                },
                "synthetic_null_rows": {
                    "minimum": 32,
                    "families": {
                        "matched_texture_noise": 8,
                        "asemic_stroke_bands": 8,
                        "mirror_or_reversal_controls": 8,
                        "shuffled_token_or_collage_controls": 8
                    },
                    "rule": "Generated from a fixed seed and manifest before review."
                }
            },
            "sentinel_rows": {
                "denominator_inclusion": "auxiliary_only_never_denominator",
                "families": [
                    "deliberate_label_leak_sentinels",
                    "blank_or_near_blank_sentinels",
                    "duplicate_image_sentinels"
                ]
            },
            "fpr_threshold": {
                "yes_only_false_positive_rate": 0,
                "conservative_false_positive_or_uncertain_rate": 0,
                "applies_to": [
                    "real_signband_negatives",
                    "real_nonlinguistic_nulls",
                    "synthetic_nulls"
                ],
                "note": "With these small denominators, one hard or uncertain null hit fails the apparatus."
            },
            "automatic_pre_review_fail_gates": [
                "reviewer_visible_filename_manifest_contact_sheet_or_order_reveals_cisi_role_source_page_route_rank_match_text_target_status_score_or_crop_method",
                "exact_duplicate_blind_image_hash_or_unregistered_near_duplicate_cluster",
                "target_control_crop_world_mismatch",
                "denominator_below_floor",
                "reserve_row_promoted_after_packet_creation",
                "visible_label_page_or_source_cue_in_denominator_row",
                "target_only_source_family_or_page_style_not_balanced_by_fixed_real_negatives",
                "synthetic_or_null_row_generated_or_selected_after_review_starts",
                "fewer_than_three_independent_blind_reviewers"
            ],
            "automatic_review_fail_gates": [
                "any_real_denominator_row_leaks_label_or_source_cue_without_downward_denominator_recalculation",
                "any_hard_or_uncertain_target_like_or_directional_call_on_real_signband_negative",
                "any_hard_or_uncertain_target_like_or_directional_call_on_real_nonlinguistic_null",
                "any_hard_or_uncertain_target_like_or_directional_call_on_synthetic_null",
                "leak_sentinels_not_flagged_by_every_reviewer",
                "blank_or_noise_sentinels_not_rejected",
                "targets_not_all_strictly_recovered",
                "paired_target_views_have_nonzero_token_count_or_direction_variance",
                "mirrored_or_reversed_controls_receive_same_claimed_directionality_as_targets",
                "result_depends_on_choosing_orientation_after_metadata_is_visible"
            ]
        },
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
