from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path.cwd()
RUN_DATE = "2026-05-29"
PACKET_ID = "branch_gap_source_box_v1"

REPORTS = ROOT / "data" / "open_prototype" / "reports"
ROUTES_CSV = REPORTS / "campaign_002_y_branch_gap_public_routes.csv"
OUT_DIR = ROOT / "tmp" / "002_y_branch_gap_blind_packet"
BLIND_DIR = OUT_DIR / "blind_images"
SOURCE_CROP_DIR = OUT_DIR / "source_crops"

MANIFEST_CSV = REPORTS / "campaign_002_y_branch_gap_blind_manifest.csv"
ANSWER_KEY_CSV = REPORTS / "campaign_002_y_branch_gap_blind_answer_key.csv"
REVIEW_TEMPLATE_CSV = REPORTS / "campaign_002_y_branch_gap_blind_review_template.csv"
SUMMARY_JSON = REPORTS / "campaign_002_y_branch_gap_blind_packet_summary.json"
CONTACT_SHEET = OUT_DIR / "branch_gap_blind_contact_sheet.png"


ITEMS = [
    {
        "blind_id": "BG001",
        "cisi": "M-12",
        "text": "+740-390-590-233-002-368-202-892-371+",
        "source_enhanced": "tmp/002_y_branch_gap_public_source_acquisition/crops/M_12_cisi_india_n45_2_context_enhanced_x2.jpg",
        "crop_box_enhanced": [120, 2350, 2280, 4300],
        "truth_class": "target_002_368_continuation",
        "control_role": "primary_target_368",
        "expected_relation": "Catalog metadata has 002 followed by branch-pole sign 368 and continuation.",
        "source_status": "public_cisi_plate_route_candidate_label_free_recrop",
        "admissible_use": "blind_tokenization_and_branch_relation_check_only",
    },
    {
        "blind_id": "BG002",
        "cisi": "M-318",
        "text": "+390-003-002-031-575+",
        "source_enhanced": "tmp/002_y_branch_gap_public_source_acquisition/crops/M_318_cisi_india_n114_1_context_enhanced_x2.jpg",
        "crop_box_enhanced": [140, 200, 2320, 2250],
        "truth_class": "target_002_031_continuation_side_uncertain",
        "control_role": "primary_target_031",
        "expected_relation": "Catalog metadata has one M-318 row with 002 followed by branch-pole sign 031; same-object side mapping remains a review risk.",
        "source_status": "public_cisi_plate_route_candidate_label_free_recrop",
        "admissible_use": "blind_tokenization_and_branch_relation_check_only",
    },
    {
        "blind_id": "BG003",
        "cisi": "M-29",
        "text": "+740-055-240-235-806-002-220-455-503+",
        "source_enhanced": "tmp/002_y_branch_gap_public_source_acquisition/crops/M_29_cisi_india_n51_2_context_enhanced_x2.jpg",
        "crop_box_enhanced": [70, 2250, 2160, 4100],
        "truth_class": "target_002_220_continuation",
        "control_role": "primary_target_220",
        "expected_relation": "Catalog metadata has 002 followed by branch-pole sign 220 and continuation.",
        "source_status": "public_cisi_plate_route_candidate_label_free_recrop",
        "admissible_use": "blind_tokenization_and_branch_relation_check_only",
    },
    {
        "blind_id": "BG004",
        "cisi": "M-678",
        "text": "+740-752-006-503-236-806-002-031-502+",
        "source_enhanced": "tmp/002_y_branch_gap_public_source_acquisition/crops/M_678_cisi_pakistan_n69_2_context_enhanced_x2.jpg",
        "crop_box_enhanced": [40, 2400, 2520, 5150],
        "truth_class": "target_002_031_continuation_backup",
        "control_role": "backup_target_031",
        "expected_relation": "Catalog metadata has 002 followed by branch-pole sign 031 and continuation.",
        "source_status": "public_cisi_plate_route_candidate_label_free_recrop",
        "admissible_use": "blind_tokenization_and_branch_relation_check_only",
    },
    {
        "blind_id": "BG005",
        "cisi": "M-655",
        "text": "+740-717-233-002-220-880-689+",
        "source_enhanced": "tmp/002_y_branch_gap_public_source_acquisition/crops/M_655_cisi_pakistan_n61_2_context_enhanced_x2.jpg",
        "crop_box_enhanced": [50, 5800, 2500, 7900],
        "truth_class": "target_002_220_continuation_backup",
        "control_role": "backup_target_220",
        "expected_relation": "Catalog metadata has 002 followed by branch-pole sign 220 and continuation.",
        "source_status": "public_cisi_plate_route_candidate_label_free_recrop",
        "admissible_use": "blind_tokenization_and_branch_relation_check_only",
    },
    {
        "blind_id": "BG006",
        "cisi": "M-311",
        "text": "+401-002-368-165+",
        "source_enhanced": "tmp/002_y_branch_gap_public_source_acquisition/crops/M_311_cisi_india_n112_1_context_enhanced_x2.jpg",
        "crop_box_enhanced": [750, 3450, 1850, 4200],
        "truth_class": "target_002_368_continuation_backup",
        "control_role": "backup_target_368",
        "expected_relation": "Catalog metadata has 002 followed by branch-pole sign 368 and continuation.",
        "source_status": "public_cisi_plate_route_candidate_label_free_recrop",
        "admissible_use": "blind_tokenization_and_branch_relation_check_only",
    },
    {
        "blind_id": "BG007",
        "cisi": "M-28",
        "text": "+892-374-740-760-840-416-002-861+",
        "source_enhanced": "tmp/002_y_branch_gap_public_source_acquisition/crops/M_29_cisi_india_n51_2_context_enhanced_x2.jpg",
        "crop_box_enhanced": [70, 420, 2160, 1600],
        "truth_class": "negative_002_y_not_branch_closure_861",
        "control_role": "scoring_negative",
        "expected_relation": "Catalog metadata has 002 followed by 861, not 368/031/220.",
        "source_status": "same_page_label_free_negative_recrop",
        "admissible_use": "false_positive_scoring_control",
    },
    {
        "blind_id": "BG008",
        "cisi": "M-653",
        "text": "+679-740-235-002-861+",
        "source_enhanced": "tmp/002_y_branch_gap_public_source_acquisition/crops/M_655_cisi_pakistan_n61_2_context_enhanced_x2.jpg",
        "crop_box_enhanced": [50, 450, 2450, 2050],
        "truth_class": "negative_002_y_not_branch_closure_861",
        "control_role": "scoring_negative",
        "expected_relation": "Catalog metadata has 002 followed by 861, not 368/031/220.",
        "source_status": "same_page_label_free_negative_recrop",
        "admissible_use": "false_positive_scoring_control",
    },
    {
        "blind_id": "BG009",
        "cisi": "M-654",
        "text": "+368-000-091-031+",
        "source_enhanced": "tmp/002_y_branch_gap_public_source_acquisition/crops/M_655_cisi_pakistan_n61_2_context_enhanced_x2.jpg",
        "crop_box_enhanced": [50, 3100, 2450, 5350],
        "truth_class": "negative_contains_branch_signs_without_002_y_frame",
        "control_role": "scoring_negative",
        "expected_relation": "Catalog metadata contains branch-pole sign forms but no 002-Y branch frame.",
        "source_status": "same_page_label_free_negative_recrop",
        "admissible_use": "false_positive_scoring_control",
    },
    {
        "blind_id": "BG010",
        "cisi": "M-381",
        "text": "+740-055-220-032-798-002-820+",
        "direct_source_image": "tmp/source_box_negative_control_v2/panel_crops/M-381_cisi_india_n129_plate_label_free_panel_enhanced_x2.jpg",
        "direct_crop_box": [0, 0, 1670, 700],
        "truth_class": "negative_002_y_not_branch_closure_820_prior_unstable",
        "control_role": "scoring_negative",
        "expected_relation": "Catalog metadata has 002 followed by 820, not 368/031/220; prior blind review found segmentation unstable.",
        "source_status": "prior_blind_negative_control_instability_stress",
        "admissible_use": "false_positive_scoring_control_with_instability_note",
    },
    {
        "blind_id": "BG011",
        "cisi": "M-32",
        "text": "+390-003-002-817+",
        "direct_source_image": "tmp/m315_second_slot_controls/derived/expanded_first3_context_crops/M-32_impression_a_390-003-002_control_good_control.png",
        "truth_class": "negative_002_y_not_branch_closure_817",
        "control_role": "scoring_negative",
        "expected_relation": "Catalog metadata has 002 followed by 817, not 368/031/220.",
        "source_status": "local_image_hit_same_site_type_short_control",
        "admissible_use": "false_positive_scoring_control",
    },
    {
        "blind_id": "BG012",
        "cisi": "M-17",
        "text": "+390-016-002-814-560+",
        "direct_source_image": "tmp/m315_second_slot_controls/derived/expanded_first3_context_crops/M-17_impression_a_390-016-002_control_good_control.png",
        "truth_class": "negative_002_y_not_branch_other_y",
        "control_role": "scoring_negative",
        "expected_relation": "Catalog metadata has 002 followed by 814, not 368/031/220.",
        "source_status": "local_image_hit_same_site_type_control",
        "admissible_use": "false_positive_scoring_control",
    },
    {
        "blind_id": "BG013",
        "cisi": "H-449",
        "text": "+740-390-590-240-741-390-728+",
        "source_enhanced": "tmp/002_y_branch_gap_public_source_acquisition/crops/H_44_cisi_pakistan_n310_3_context_enhanced_x2.jpg",
        "crop_box_enhanced": [150, 2800, 1400, 3900],
        "truth_class": "quarantine_false_route_h44_prefix_trap",
        "control_role": "quarantine_negative_not_scoring",
        "expected_relation": "This is the OCR-prefix false route that formerly masqueraded as H-44; use only to diagnose route leakage.",
        "source_status": "known_false_route_quarantine",
        "admissible_use": "quarantine_route_failure_control_not_scoring",
        "allow_enhanced_fallback": True,
    },
    {
        "blind_id": "BG014",
        "cisi": "M-1427",
        "text": "+484-140-002-220-627-615-906-388+",
        "source_enhanced": "tmp/002_y_branch_gap_public_source_acquisition/crops/M_1427_cisi_pakistan_n227_1_context_enhanced_x2.jpg",
        "crop_box_enhanced": [0, 800, 2600, 1900],
        "truth_class": "quarantine_low_legibility_target_002_220",
        "control_role": "quarantine_low_quality_target_not_scoring",
        "expected_relation": "Catalog metadata has 002 followed by 220, but the public crop is side/label messy and not packet-ready.",
        "source_status": "real_route_low_legibility_quarantine",
        "admissible_use": "quarantine_legibility_control_not_scoring",
    },
]


def parse_csv(text: str) -> list[dict[str, str]]:
    rows = []
    reader = csv.DictReader(text.splitlines())
    for row in reader:
        rows.append(dict(row))
    return rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def route_by_enhanced_path() -> dict[str, dict[str, str]]:
    rows = parse_csv(ROUTES_CSV.read_text(encoding="utf-8"))
    return {row["local_enhanced_crop"]: row for row in rows if row.get("local_enhanced_crop")}


def enhanced_box_to_page_box(item: dict[str, object], routes: dict[str, dict[str, str]]) -> tuple[Path, tuple[int, int, int, int]]:
    enhanced = str(item["source_enhanced"])
    route = routes.get(enhanced)
    if not route:
        raise KeyError(f"No route row for {enhanced}")
    crop_box = [int(value) for value in route["crop_box_image_coords"].split("|")]
    box = [int(value) for value in item["crop_box_enhanced"]]
    x1 = crop_box[0] + box[0] // 2
    y1 = crop_box[1] + box[1] // 2
    x2 = crop_box[0] + box[2] // 2
    y2 = crop_box[1] + box[3] // 2
    return ROOT / route["local_page_path"], (x1, y1, x2, y2)


def label_free_crop(item: dict[str, object], routes: dict[str, dict[str, str]]) -> Path:
    SOURCE_CROP_DIR.mkdir(parents=True, exist_ok=True)
    out_path = SOURCE_CROP_DIR / f"{item['blind_id']}_source_crop.png"
    if item.get("direct_source_image"):
        source = ROOT / str(item["direct_source_image"])
        if not source.exists():
            raise FileNotFoundError(source)
        image = Image.open(source).convert("RGB")
        if item.get("direct_crop_box"):
            box = tuple(int(value) for value in item["direct_crop_box"])
            image = image.crop(box)
        image.save(out_path)
        return out_path

    if item.get("allow_enhanced_fallback") and str(item["source_enhanced"]) not in routes:
        source = ROOT / str(item["source_enhanced"])
        if not source.exists():
            raise FileNotFoundError(source)
        box = tuple(int(value) for value in item["crop_box_enhanced"])
        crop = Image.open(source).convert("RGB").crop(box)
        crop = ImageOps.autocontrast(ImageOps.grayscale(crop)).convert("RGB")
        crop.save(out_path)
        return out_path

    page_path, page_box = enhanced_box_to_page_box(item, routes)
    if not page_path.exists():
        raise FileNotFoundError(page_path)
    image = Image.open(page_path).convert("RGB")
    crop = image.crop(page_box)
    crop = ImageOps.autocontrast(ImageOps.grayscale(crop)).convert("RGB")
    crop = crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.LANCZOS)
    crop.save(out_path)
    return out_path


def make_packet() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    routes = route_by_enhanced_path()
    BLIND_DIR.mkdir(parents=True, exist_ok=True)
    manifest_rows = []
    key_rows = []

    for item in ITEMS:
        source_crop = label_free_crop(item, routes)
        blind_path = BLIND_DIR / f"{item['blind_id']}.png"
        shutil.copyfile(source_crop, blind_path)
        blind_hash = sha256_file(blind_path)
        source_hash = sha256_file(source_crop)

        manifest_rows.append(
            {
                "date": RUN_DATE,
                "packet_id": PACKET_ID,
                "blind_id": item["blind_id"],
                "image_path": str(blind_path.relative_to(ROOT)).replace("\\", "/"),
                "image_sha256": blind_hash,
                "review_stage": "stage1_blind_tokenization",
                "review_task": "Box every visible sign token in visual order without using catalogue text, object ID, expected sequence, or page labels.",
                "required_output": "token_count; visual_order_note; token_boxes_json; visible_002_y_candidate_notes; uncertainty_notes",
                "admissible_use": item["admissible_use"],
                "accepted_claims_increment": 0,
            }
        )
        key_rows.append(
            {
                "date": RUN_DATE,
                "packet_id": PACKET_ID,
                "blind_id": item["blind_id"],
                "cisi": item["cisi"],
                "target_text": item["text"],
                "truth_class": item["truth_class"],
                "control_role": item["control_role"],
                "expected_relation": item["expected_relation"],
                "source_crop": str(source_crop.relative_to(ROOT)).replace("\\", "/"),
                "source_crop_sha256": source_hash,
                "source_status": item["source_status"],
                "blind_image_sha256": blind_hash,
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
            "stage1_visual_order_note": "",
            "stage1_token_boxes_json": "",
            "stage1_visible_002_y_candidate_notes": "",
            "stage1_uncertainty_notes": "",
            "stage2_after_unblind_catalog_alignment": "",
            "stage2_branch_relation_present_yes_no_uncertain": "",
            "stage2_confidence": "",
            "stage2_notes": "",
        }
        for row in manifest_rows
    ]


def make_contact_sheet(manifest_rows: list[dict[str, object]]) -> None:
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        font = ImageFont.load_default()

    thumbs = []
    for row in manifest_rows:
        image = Image.open(ROOT / str(row["image_path"])).convert("RGB")
        image.thumbnail((430, 260))
        thumbs.append((str(row["blind_id"]), image.copy()))

    columns = 2
    cell_w = 480
    cell_h = 320
    rows = (len(thumbs) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    for index, (blind_id, image) in enumerate(thumbs):
        col = index % columns
        row = index // columns
        x = col * cell_w + 24
        y = row * cell_h + 46
        draw.text((col * cell_w + 24, row * cell_h + 14), blind_id, fill=(0, 0, 0), font=font)
        sheet.paste(image, (x, y))
        draw.rectangle((x - 1, y - 1, x + image.width + 1, y + image.height + 1), outline=(180, 180, 180), width=1)

    CONTACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(CONTACT_SHEET)


def main() -> None:
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    manifest_rows, key_rows = make_packet()
    review_rows = make_review_template(manifest_rows)
    make_contact_sheet(manifest_rows)

    write_csv(MANIFEST_CSV, list(manifest_rows[0].keys()), manifest_rows)
    write_csv(ANSWER_KEY_CSV, list(key_rows[0].keys()), key_rows)
    write_csv(REVIEW_TEMPLATE_CSV, list(review_rows[0].keys()), review_rows)

    summary = {
        "date": RUN_DATE,
        "packet_id": PACKET_ID,
        "status": "blind_branch_gap_token_box_packet_created_no_claim_promotion",
        "counts": {
            "blind_items": len(manifest_rows),
            "primary_targets": sum(1 for row in key_rows if str(row["control_role"]).startswith("primary_target")),
            "backup_targets": sum(1 for row in key_rows if str(row["control_role"]).startswith("backup_target")),
            "scoring_negatives": sum(1 for row in key_rows if row["control_role"] == "scoring_negative"),
            "quarantine_items": sum(1 for row in key_rows if str(row["control_role"]).startswith("quarantine")),
            "accepted_claims_increment": 0,
        },
        "branch_targets_by_sign": {
            "031": ["M-318", "M-678"],
            "220": ["M-29", "M-655"],
            "368": ["M-12", "M-311"],
        },
        "route_failure_correction": {
            "demoted": "H-44",
            "reason": "OCR prefix/split labels such as H-449 produced false H-44 route matches before numeric-suffix rejection.",
        },
        "visual_qa": {
            "contact_sheet_checked": True,
            "label_leakage_tightened": ["BG003", "BG009", "BG013", "BG014"],
            "accepted_claims_increment": 0,
        },
        "null_question": (
            "Can public-route branch-gap crops for 002 followed by 368/031/220 be tokenized and "
            "aligned more reliably than matched negative or quarantine source crops when catalogue "
            "text and object labels are hidden?"
        ),
        "promotion_thresholds": [
            "This packet can only promote route candidates to source-box adjudication candidates; it cannot accept a structural claim.",
            "At least two independent blind reviews must produce stable token counts and boxes for each primary target before unblinding.",
            "Scoring negatives must produce zero hard branch-relation hits under the same review instructions.",
            "Quarantine items diagnose route leakage and image quality; they do not enter false-positive denominators.",
            "Any dependence on source labels, catalogue text, or post-hoc orientation choice blocks promotion.",
        ],
        "files": {
            "blind_manifest": str(MANIFEST_CSV.relative_to(ROOT)).replace("\\", "/"),
            "answer_key": str(ANSWER_KEY_CSV.relative_to(ROOT)).replace("\\", "/"),
            "review_template": str(REVIEW_TEMPLATE_CSV.relative_to(ROOT)).replace("\\", "/"),
            "contact_sheet": str(CONTACT_SHEET.relative_to(ROOT)).replace("\\", "/"),
            "blind_image_dir": str(BLIND_DIR.relative_to(ROOT)).replace("\\", "/"),
            "source_crop_dir": str(SOURCE_CROP_DIR.relative_to(ROOT)).replace("\\", "/"),
        },
        "interpretation_boundary": "No token order, physical direction, sign identity, sign meaning, phonetic value, language family, translation, or accepted structural claim follows from packet creation.",
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
