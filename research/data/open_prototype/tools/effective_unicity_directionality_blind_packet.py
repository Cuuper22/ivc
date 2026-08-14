"""Build the v1 blind review packet for the directionality experiment.

A blind packet is a shuffled set of anonymized inscription images that human
reviewers examine without knowing which seal each image is. Reviewers count the
visible sign tokens and flag any leaked catalogue label; if their counts match
the expected corpus counts, the crop can be promoted to a source-normalized
candidate for later sign-order work — never to a reading or translation. This
script cuts hand-picked crops from raw public CISI plate pages (avoiding the
red diagnostic route overlay), mixes seven primary targets with scoring and
quarantine negatives, shuffles them with a fixed seed, and writes the blind
images plus a crop manifest, blind manifest, answer key, review template,
contact sheet, and summary JSON under data/open_prototype/reports and
tmp/effective_unicity_directionality_blind_packet.
"""

from __future__ import annotations

import csv
import hashlib
import json
import random
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path.cwd()
RUN_DATE = "2026-05-29"
PACKET_ID = "directionality_no_overlay_packet_v1"

REPORTS = ROOT / "data" / "open_prototype" / "reports"
OUT_DIR = ROOT / "tmp" / "effective_unicity_directionality_blind_packet"
SOURCE_DIR = OUT_DIR / "source_crops"
BLIND_DIR = OUT_DIR / "blind_images"

ROUTE_STATUS = REPORTS / "effective_unicity_directionality_public_route_probe_status.csv"
TRIAGE_SUMMARY = REPORTS / "effective_unicity_directionality_route_visual_triage_summary.json"

CROP_MANIFEST = REPORTS / "effective_unicity_directionality_blind_packet_crop_manifest.csv"
BLIND_MANIFEST = REPORTS / "effective_unicity_directionality_blind_packet_manifest.csv"
ANSWER_KEY = REPORTS / "effective_unicity_directionality_blind_packet_answer_key.csv"
REVIEW_TEMPLATE = REPORTS / "effective_unicity_directionality_blind_packet_review_template.csv"
SUMMARY_JSON = REPORTS / "effective_unicity_directionality_blind_packet_summary.json"
CONTACT_SHEET = OUT_DIR / "directionality_no_overlay_blind_contact_sheet.png"

RNG_SEED = 407004001


# Each crop box is in raw page-image pixels (x1, y1, x2, y2), not route-context
# coordinates. The boxes were chosen by hand on the public CISI page scans to
# dodge the red diagnostic route overlay and, where the scan allows, the printed
# object labels.
CROP_SPECS = [
    {
        "cisi": "H-654",
        "source_view": "A_signband",
        "role": "primary_target",
        "truth_class": "tier1_directionality_candidate_harappa_four_token",
        "crop_box_xyxy": (130, 1690, 1120, 2150),
        "expected_token_count": 4,
        "text": "+405-061-740-806+",
        "source_note": "H-654 A signband from CISI Pakistan n342; compact four-token tier-1 route candidate.",
    },
    {
        "cisi": "M-1310",
        "source_view": "A_signband",
        "role": "primary_target",
        "truth_class": "tier1_directionality_candidate_mohenjo_daro_seven_token_face",
        "crop_box_xyxy": (965, 1490, 2310, 1790),
        "expected_token_count": 7,
        "text": "+407-004-001-740-407-590-235+",
        "source_note": "M-1310 A source band from CISI Pakistan n202; route label is excluded.",
    },
    {
        "cisi": "M-1310",
        "source_view": "a_signband",
        "role": "primary_target",
        "truth_class": "tier1_directionality_candidate_mohenjo_daro_seven_token_impression",
        "crop_box_xyxy": (955, 2080, 2315, 2375),
        "expected_token_count": 7,
        "text": "+407-004-001-740-407-590-235+",
        "source_note": "M-1310 impression band from CISI Pakistan n202; paired with the A crop for side/order stress.",
    },
    {
        "cisi": "M-1320",
        "source_view": "A_signband",
        "role": "primary_target",
        "truth_class": "tier1_directionality_candidate_mohenjo_daro_five_token_face",
        "crop_box_xyxy": (1810, 1225, 3025, 1540),
        "expected_token_count": 5,
        "text": "+527-555-231-240-798+",
        "source_note": "M-1320 A band from CISI Pakistan n203; visually strong tier-1 route candidate.",
    },
    {
        "cisi": "M-1320",
        "source_view": "a_signband",
        "role": "primary_target",
        "truth_class": "tier1_directionality_candidate_mohenjo_daro_five_token_impression",
        "crop_box_xyxy": (1785, 1760, 3065, 2155),
        "expected_token_count": 5,
        "text": "+527-555-231-240-798+",
        "source_note": "M-1320 lower impression band from CISI Pakistan n203; cropped as a paired order check.",
    },
    {
        "cisi": "M-811",
        "source_view": "A_signband",
        "role": "primary_target",
        "truth_class": "tier1_directionality_candidate_mohenjo_daro_three_token_face",
        "crop_box_xyxy": (2250, 360, 3075, 760),
        "expected_token_count": 3,
        "text": "+226-032-803+",
        "source_note": "M-811 A signband and upper field from CISI Pakistan n104; label excluded.",
    },
    {
        "cisi": "M-811",
        "source_view": "a_signband",
        "role": "primary_target",
        "truth_class": "tier1_directionality_candidate_mohenjo_daro_three_token_impression",
        "crop_box_xyxy": (2250, 1435, 3090, 1780),
        "expected_token_count": 3,
        "text": "+226-032-803+",
        "source_note": "M-811 lower impression band from CISI Pakistan n104; cropped as paired target evidence.",
    },
    {
        "cisi": "H-665",
        "source_view": "A_signband",
        "role": "scoring_negative",
        "truth_class": "tier2_weak_partial_route_control",
        "crop_box_xyxy": (2390, 3140, 3240, 3525),
        "expected_token_count": 4,
        "text": "+407-004-060-692+",
        "source_note": "H-665 A weak/partial source panel from CISI Pakistan n343; tests whether weak route crops look falsely clean.",
    },
    {
        "cisi": "M-1458",
        "source_view": "A_tablet_panel",
        "role": "scoring_negative",
        "truth_class": "tier3_low_legibility_tablet_control",
        "crop_box_xyxy": (1090, 2440, 2160, 3110),
        "expected_token_count": 5,
        "text": "+407-004-001-617-142+",
        "source_note": "M-1458 tablet panel from CISI Pakistan n234; low-legibility control.",
    },
    {
        "cisi": "M-1523",
        "source_view": "A_tablet_panel",
        "role": "scoring_negative",
        "truth_class": "tier3_low_legibility_tablet_control",
        "crop_box_xyxy": (230, 2340, 1535, 3150),
        "expected_token_count": 7,
        "text": "+407-585-033-705-233-235-806+",
        "source_note": "M-1523 A tablet panel from CISI Pakistan n253; dark low-legibility control.",
    },
    {
        "cisi": "M-525",
        "source_view": "B_side_panel",
        "role": "scoring_negative",
        "truth_class": "tier2_complex_side_geometry_control",
        "crop_box_xyxy": (2295, 3150, 3135, 3820),
        "expected_token_count": 8,
        "text": "+423-003-001-900-740-690-435-255+",
        "source_note": "M-525 side panel from CISI Pakistan n40; complex geometry and label-adjacent trap.",
    },
    {
        "cisi": "H-152",
        "source_view": "A_signband",
        "role": "quarantine_negative",
        "truth_class": "volume_provenance_mismatch_control",
        "crop_box_xyxy": (905, 240, 1510, 500),
        "expected_token_count": 3,
        "text": "+154-806-468+",
        "source_note": "H-152 A is visually readable but route volume/provenance is mismatched; quarantine only.",
    },
    {
        "cisi": "M-1273",
        "source_view": "impression_a_existing_hard_negative",
        "role": "scoring_negative",
        "truth_class": "m70_hard_negative_002_y_prev_not_032_suffix_control",
        "source_image": "tmp/032_002_861_suffix_split/M1273_impression_a_cisi_pakistan_n195.png",
        "trim_bottom_px": 210,
        "expected_token_count": 5,
        "text": "+740-055-002-861-603+",
        "source_note": "Existing M-70 hard negative; prior reviewers produced target-like false positives.",
    },
    {
        "cisi": "M-376",
        "source_view": "impression_a_existing_hard_negative",
        "role": "scoring_negative",
        "truth_class": "m70_hard_negative_002_y_prev_not_032_suffix_control",
        "source_image": "tmp/032_002_861_suffix_split/M376_impression_a_cisi_india_n129.png",
        "trim_bottom_px": 36,
        "expected_token_count": 7,
        "text": "+740-100-176-002-861-533-717+",
        "source_note": "Existing M-70 hard negative; prior reviewers produced target-like false positives.",
    },
    {
        "cisi": "M-381",
        "source_view": "panel_existing_stress_negative",
        "role": "scoring_negative",
        "truth_class": "existing_segmentation_instability_stress_control",
        "source_image": "tmp/source_box_negative_control_v2/panel_crops/M-381_cisi_india_n129_plate_label_free_panel_enhanced_x2.jpg",
        "trim_bottom_px": 70,
        "expected_token_count": 7,
        "text": "+740-055-220-032-798-002-820+",
        "source_note": "Existing no-overlay stress control; prior blind reviews found segmentation instability.",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def route_lookup() -> dict[str, dict[str, str]]:
    rows = read_csv(ROUTE_STATUS)
    return {
        row["representative_cisi"]: row
        for row in rows
        if row.get("representative_cisi")
    }


def route_row_lookup() -> dict[str, dict[str, str]]:
    rows = read_csv(REPORTS / "effective_unicity_directionality_public_route_probe_routes.csv")
    first_routes: dict[str, dict[str, str]] = {}
    for row in rows:
        if row.get("route_rank") != "1":
            continue
        first_routes[row["representative_cisi"]] = row
    return first_routes


def fallback_route(cisi: str) -> dict[str, str]:
    return {
        "site": "",
        "type": "",
        "direction": "",
        "diff_per_transition": "",
        "queue_rank": "",
    }


def crop_image(page_path: Path, box: tuple[int, int, int, int]) -> Image.Image:
    image = Image.open(page_path).convert("RGB")
    x1, y1, x2, y2 = box
    x1 = max(0, min(x1, image.width - 1))
    y1 = max(0, min(y1, image.height - 1))
    x2 = max(x1 + 1, min(x2, image.width))
    y2 = max(y1 + 1, min(y2, image.height))
    return image.crop((x1, y1, x2, y2))


def enhanced(image: Image.Image) -> Image.Image:
    gray = ImageOps.grayscale(image)
    gray = ImageOps.autocontrast(gray, cutoff=1)
    return gray.resize((gray.width * 2, gray.height * 2), Image.Resampling.LANCZOS)


def token_count(text: str) -> int:
    return len([part for part in text.replace("+", "").split("-") if part.strip()])


def build_source_crops() -> list[dict[str, object]]:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    routes = route_lookup()
    route_rows = route_row_lookup()
    rows: list[dict[str, object]] = []
    for spec in CROP_SPECS:
        route = routes.get(spec["cisi"], fallback_route(spec["cisi"]))
        if "source_image" in spec:
            page_path = ROOT / str(spec["source_image"])
            if not page_path.exists():
                raise FileNotFoundError(page_path)
            crop = Image.open(page_path).convert("RGB")
            trim_bottom_px = int(spec.get("trim_bottom_px", 0))
            if trim_bottom_px:
                crop = crop.crop((0, 0, crop.width, max(1, crop.height - trim_bottom_px)))
            crop_box = (0, 0, crop.width, crop.height)
        else:
            route_row = route_rows.get(spec["cisi"])
            page_path = ROOT / route_row["local_page_path"] if route_row else Path("__missing_page__")
            if not page_path.exists():
                matching_route_rows = [
                    row
                    for row in read_csv(REPORTS / "effective_unicity_directionality_public_route_probe_routes.csv")
                    if row["representative_cisi"] == spec["cisi"] and row["route_rank"] == "1"
                ]
                if matching_route_rows:
                    page_path = ROOT / matching_route_rows[0]["local_page_path"]
            if not page_path.exists():
                raise FileNotFoundError(f"raw page for {spec['cisi']}: {page_path}")
            crop_box = spec["crop_box_xyxy"]
            crop = crop_image(page_path, crop_box)
        slug = f"{spec['cisi'].replace('-', '_')}_{spec['source_view']}"
        source_path = SOURCE_DIR / f"{slug}_source.png"
        enhanced_path = SOURCE_DIR / f"{slug}_enhanced_x2.png"
        crop.save(source_path)
        enhanced(crop).save(enhanced_path)
        rows.append(
            {
                "date": RUN_DATE,
                "packet_id": PACKET_ID,
                "cisi": spec["cisi"],
                "source_view": spec["source_view"],
                "role": spec["role"],
                "truth_class": spec["truth_class"],
                "text": spec["text"],
                "expected_token_count": spec["expected_token_count"],
                "computed_token_count": token_count(spec["text"]),
                "site": route["site"],
                "type": route["type"],
                "direction": route["direction"],
                "diff_per_transition": route["diff_per_transition"],
                "route_queue_rank": route["queue_rank"],
                "source_page": str(page_path.relative_to(ROOT)).replace("\\", "/"),
                "crop_box_xyxy": "|".join(str(v) for v in crop_box),
                "source_crop": str(source_path.relative_to(ROOT)).replace("\\", "/"),
                "enhanced_crop": str(enhanced_path.relative_to(ROOT)).replace("\\", "/"),
                "source_crop_sha256": sha256_file(source_path),
                "enhanced_crop_sha256": sha256_file(enhanced_path),
                "source_note": spec["source_note"],
                "label_leak_precheck": "designed_label_free_needs_visual_verification",
                "accepted_claims_increment": 0,
            }
        )
    return rows


def build_blind_packet(crop_rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    BLIND_DIR.mkdir(parents=True, exist_ok=True)
    rng = random.Random(RNG_SEED)
    shuffled = list(crop_rows)
    rng.shuffle(shuffled)
    manifest_rows: list[dict[str, object]] = []
    key_rows: list[dict[str, object]] = []
    for index, row in enumerate(shuffled, start=1):
        blind_id = f"D{index:03d}"
        source = ROOT / str(row["enhanced_crop"])
        target = BLIND_DIR / f"{blind_id}.png"
        shutil.copyfile(source, target)
        image_hash = sha256_file(target)
        manifest_rows.append(
            {
                "date": RUN_DATE,
                "packet_id": PACKET_ID,
                "blind_id": blind_id,
                "image_path": str(target.relative_to(ROOT)).replace("\\", "/"),
                "image_sha256": image_hash,
                "review_stage": "stage1_blind_source_visibility_and_token_boxing",
                "review_task": (
                    "Without catalogue text or object ID, count visible sign tokens, mark whether a "
                    "single signband is confidently boxable, and note any label/metadata leak."
                ),
                "required_output": (
                    "token_count; boxable_yes_no_uncertain; label_leak_yes_no; "
                    "visual_order_note; uncertainty_notes"
                ),
                "accepted_claims_increment": 0,
            }
        )
        key_rows.append(
            {
                "date": RUN_DATE,
                "packet_id": PACKET_ID,
                "blind_id": blind_id,
                "cisi": row["cisi"],
                "source_view": row["source_view"],
                "role": row["role"],
                "truth_class": row["truth_class"],
                "target_text": row["text"],
                "expected_token_count": row["expected_token_count"],
                "site": row["site"],
                "type": row["type"],
                "direction": row["direction"],
                "source_crop": row["source_crop"],
                "enhanced_crop": row["enhanced_crop"],
                "blind_image_sha256": image_hash,
                "source_note": row["source_note"],
                "accepted_claims_increment": 0,
            }
        )
    return manifest_rows, key_rows


def make_review_template(manifest_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "date": RUN_DATE,
            "packet_id": PACKET_ID,
            "reviewer": "",
            "blind_id": row["blind_id"],
            "stage1_visual_token_count": "",
            "stage1_boxable_yes_no_uncertain": "",
            "stage1_label_leak_yes_no": "",
            "stage1_visual_order_note": "",
            "stage1_uncertainty_notes": "",
            "stage1_token_boxes_json_optional": "",
            "stage2_after_unblind_expected_count_match_yes_no_uncertain": "",
            "stage2_after_unblind_promotable_yes_no": "",
            "stage2_notes": "",
        }
        for row in manifest_rows
    ]


def make_contact_sheet(manifest_rows: list[dict[str, object]]) -> None:
    try:
        font = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    cols = 2
    cell_w = 780
    cell_h = 470
    rows = (len(manifest_rows) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    for index, row in enumerate(manifest_rows):
        image = Image.open(ROOT / str(row["image_path"])).convert("RGB")
        image.thumbnail((cell_w - 40, cell_h - 70), Image.Resampling.LANCZOS)
        col = index % cols
        row_index = index // cols
        x = col * cell_w + 20
        y = row_index * cell_h + 52
        draw.text((col * cell_w + 20, row_index * cell_h + 18), str(row["blind_id"]), fill="black", font=font)
        sheet.paste(image, (x, y))
        draw.rectangle((x - 1, y - 1, x + image.width + 1, y + image.height + 1), outline=(180, 180, 180), width=1)
    CONTACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(CONTACT_SHEET)


def main() -> None:
    crop_rows = build_source_crops()
    manifest_rows, key_rows = build_blind_packet(crop_rows)
    review_rows = make_review_template(manifest_rows)
    make_contact_sheet(manifest_rows)

    write_csv(CROP_MANIFEST, crop_rows, list(crop_rows[0].keys()))
    write_csv(BLIND_MANIFEST, manifest_rows, list(manifest_rows[0].keys()))
    write_csv(ANSWER_KEY, key_rows, list(key_rows[0].keys()))
    write_csv(REVIEW_TEMPLATE, review_rows, list(review_rows[0].keys()))

    primary_targets = [row for row in key_rows if row["role"] == "primary_target"]
    scoring_negatives = [row for row in key_rows if row["role"] == "scoring_negative"]
    quarantine_negatives = [row for row in key_rows if row["role"] == "quarantine_negative"]
    triage = json.loads(TRIAGE_SUMMARY.read_text(encoding="utf-8"))
    summary = {
        "date": RUN_DATE,
        "packet_id": PACKET_ID,
        "status": "blind_packet_created_not_scored_no_claim_promotion",
        "inputs": {
            "route_status_csv": str(ROUTE_STATUS.relative_to(ROOT)).replace("\\", "/"),
            "route_visual_triage_summary": str(TRIAGE_SUMMARY.relative_to(ROOT)).replace("\\", "/"),
            "triage_id": triage.get("triage_id", ""),
        },
        "counts": {
            "blind_items": len(manifest_rows),
            "primary_target_images": len(primary_targets),
            "primary_target_unique_cisis": len({row["cisi"] for row in primary_targets}),
            "scoring_negative_images": len(scoring_negatives),
            "scoring_negative_unique_cisis": len({row["cisi"] for row in scoring_negatives}),
            "quarantine_negative_images": len(quarantine_negatives),
            "accepted_claims_increment": 0,
        },
        "forger_control_plan": {
            "planned_real_scoring_negative_unique_cisis": 12,
            "current_packet_real_scoring_negative_unique_cisis": len({row["cisi"] for row in scoring_negatives}),
            "promotion_denominator_floor": 10,
            "status": (
                "current packet is below the forger's preferred real-control denominator; it is usable for "
                "blind QA and failure discovery, not for promotion"
            ),
        },
        "target_cisis": sorted({row["cisi"] for row in primary_targets}),
        "scoring_negative_cisis": sorted({row["cisi"] for row in scoring_negatives}),
        "quarantine_negative_cisis": sorted({row["cisi"] for row in quarantine_negatives}),
        "forger_question": (
            "Do the four visually triaged tier-1 public-route candidates remain distinguishable as "
            "clean, label-free, source-boxable signbands when mixed with weak/low-legibility/complex "
            "route controls cut by the same no-overlay procedure?"
        ),
        "promotion_thresholds": [
            "Two or more independent blind reviews must mark every primary-target image as label-leak-free and boxable or explicitly identify any non-comparable target view before scoring.",
            "For any candidate object to move beyond acquisition inventory, both available paired views must have matching visual token count under blind review; H-654 has only one current public view and therefore cannot pass a paired-view promotion in this packet.",
            "Scoring negatives must produce zero hard boxable-and-count-matching hits under the same review rubric; quarantine negatives are excluded from false-positive denominators.",
            "Even a passing packet can promote only to source-normalized crop candidate for further sign-order adjudication, never to sign value, phonetic value, meaning, language family, translation, or an accepted structural finding.",
        ],
        "interpretation_boundary": (
            "This packet is a source-normalization gate only. It does not validate physical direction, "
            "token order, sign identity, sign semantics, language family, phonetic value, or translation."
        ),
        "outputs": {
            "crop_manifest": str(CROP_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
            "blind_manifest": str(BLIND_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
            "answer_key": str(ANSWER_KEY.relative_to(ROOT)).replace("\\", "/"),
            "review_template": str(REVIEW_TEMPLATE.relative_to(ROOT)).replace("\\", "/"),
            "summary_json": str(SUMMARY_JSON.relative_to(ROOT)).replace("\\", "/"),
            "contact_sheet": str(CONTACT_SHEET.relative_to(ROOT)).replace("\\", "/"),
            "blind_image_dir": str(BLIND_DIR.relative_to(ROOT)).replace("\\", "/"),
        },
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
