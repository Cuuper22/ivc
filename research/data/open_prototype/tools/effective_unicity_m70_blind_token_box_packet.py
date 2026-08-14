"""Build a blind review packet for the M-70 order-window question.

We want to know whether seal M-70 really shows the sign sequence 032-002
followed by 390-692, or whether a reviewer primed by the catalog would "see"
that sequence anywhere. So we prepare a blind test: 15 sign-band crops
(already sitting in tmp/ from earlier acquisition runs) get copied under
anonymous IDs B001-B015 — two M-70 targets, three positive calibrators where
the sequence is genuinely present, and ten negatives where 002 is preceded by
something other than 032. Reviewers box every visible sign in visual order
without seeing the catalog text; only afterward is the answer key opened.
The script copies and hashes each image (trimming caption strips from two of
them), draws a two-column contact sheet, and writes the blind manifest, the
answer key, an empty review template, and a JSON summary with the promotion
thresholds. By design nothing here increments accepted claims.
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path.cwd()
RUN_DATE = "2026-05-29"
PACKET_ID = "m70_order_window_pilot_v1"
REPORTS = ROOT / "data" / "open_prototype" / "reports"
OUT_DIR = ROOT / "tmp" / "effective_unicity_m70_blind_packet"
BLIND_DIR = OUT_DIR / "blind_images"

BLIND_MANIFEST = REPORTS / "effective_unicity_m70_blind_token_box_manifest.csv"
ANSWER_KEY = REPORTS / "effective_unicity_m70_blind_token_box_answer_key.csv"
REVIEW_TEMPLATE = REPORTS / "effective_unicity_m70_blind_token_box_review_template.csv"
SUMMARY_JSON = REPORTS / "effective_unicity_m70_blind_token_box_packet_summary.json"
CONTACT_SHEET = OUT_DIR / "m70_blind_token_box_contact_sheet.png"


ITEMS = [
    {
        "blind_id": "B001",
        "cisi": "M-70",
        "text": "+226-032-002-390-692+",
        "source_image": "tmp/032_002_branch_tail_source_acquisition/M70_face_A_signband_from_cisi_india_n066.png",
        "truth_class": "target_032_002_390_692_face_order_window",
        "control_role": "primary_target_face",
        "expected_relation": "Catalog metadata has adjacent 032-002 followed by 390-692 under the current stored R/L order.",
        "source_status": "row_level_source_visible_broad_order_window_candidate",
        "admissible_use": "blind_tokenization_and_order_window_check_only",
    },
    {
        "blind_id": "B002",
        "cisi": "M-70",
        "text": "+226-032-002-390-692+",
        "source_image": "tmp/032_002_branch_tail_source_acquisition/M70_impression_a_signband_from_cisi_india_n066.png",
        "truth_class": "target_032_002_390_692_impression_order_window",
        "control_role": "primary_target_impression",
        "expected_relation": "Catalog metadata has adjacent 032-002 followed by 390-692 under the current stored R/L order.",
        "source_status": "row_level_source_visible_broad_order_window_candidate",
        "admissible_use": "blind_tokenization_and_order_window_check_only",
    },
    {
        "blind_id": "B003",
        "cisi": "M-91",
        "text": "+740-100-798-220-032-002-861-255-416+",
        "source_image": "tmp/032_002_branch_tail_source_acquisition/M91_impression_a_signband_from_cisi_india_n071.png",
        "truth_class": "positive_032_002_861_continuation_lowres",
        "control_role": "positive_calibrator_lowres",
        "expected_relation": "Catalog metadata has adjacent 032-002 followed by 861-255-416, but source quality is medium-low.",
        "source_status": "source_visible_broad_order_window_candidate_lowres",
        "admissible_use": "calibration_only",
    },
    {
        "blind_id": "B004",
        "cisi": "M-240",
        "text": "+520-240-220-032-002-861-603+",
        "source_image": "tmp/032_002_branch_tail_source_acquisition/M240_impression_a_signband_from_cisi_india_n095.png",
        "truth_class": "positive_032_002_861_603_order_window",
        "control_role": "positive_calibrator",
        "expected_relation": "Catalog metadata has adjacent 032-002 followed by 861-603; the 861->603 tail is recurrent in the all-002 family.",
        "source_status": "source_visible_broad_order_window_candidate",
        "admissible_use": "calibration_only",
    },
    {
        "blind_id": "B005",
        "cisi": "M-49",
        "text": "+527-550-240-220-032-002-300-350-032-190+",
        "source_image": "tmp/032_002_y_source_function_batch/M49_target_300_signband_closeup.png",
        "truth_class": "positive_032_002_300_continuation_existing_token_box",
        "control_role": "positive_calibrator_existing_token_box",
        "expected_relation": "Catalog metadata and earlier scaffold place 032-002-300 in a same-line source-visible window.",
        "source_status": "source_single_line_existing_token_box",
        "admissible_use": "calibration_only",
    },
    {
        "blind_id": "B006",
        "cisi": "M-77",
        "text": "+832-390-803-002-861+",
        "source_image": "tmp/m77_parpola_recurrence_gate/derived/M77_face_A_signband_strict_from_cisi_india_n68.png",
        "truth_class": "negative_002_y_prev_not_032_face",
        "control_role": "scoring_negative",
        "expected_relation": "Catalog metadata has 002 preceded by 803, not by 032; 390 occurs elsewhere in the same row.",
        "source_status": "local_image_hit_same_site_type_symbol_length",
        "admissible_use": "false_positive_scoring_control",
    },
    {
        "blind_id": "B007",
        "cisi": "M-77",
        "text": "+832-390-803-002-861+",
        "source_image": "tmp/m77_parpola_recurrence_gate/derived/M77_impression_a_signband_strict_from_cisi_india_n68.png",
        "truth_class": "negative_002_y_prev_not_032_impression",
        "control_role": "scoring_negative",
        "expected_relation": "Catalog metadata has 002 preceded by 803, not by 032; 390 occurs elsewhere in the same row.",
        "source_status": "local_image_hit_same_site_type_symbol_length",
        "admissible_use": "false_positive_scoring_control",
    },
    {
        "blind_id": "B008",
        "cisi": "M-17",
        "text": "+390-016-002-814-560+",
        "source_image": "tmp/m315_second_slot_controls/derived/expanded_first3_context_crops/M-17_impression_a_390-016-002_control_good_control.png",
        "truth_class": "negative_002_y_prev_not_032",
        "control_role": "scoring_negative",
        "expected_relation": "Catalog metadata has 002 preceded by 016, not by 032; the row begins with 390.",
        "source_status": "local_image_hit_same_site_type_symbol_length",
        "admissible_use": "false_positive_scoring_control",
    },
    {
        "blind_id": "B009",
        "cisi": "M-32",
        "text": "+390-003-002-817+",
        "source_image": "tmp/m315_second_slot_controls/derived/expanded_first3_context_crops/M-32_impression_a_390-003-002_control_good_control.png",
        "truth_class": "negative_002_y_prev_not_032_short",
        "control_role": "scoring_negative",
        "expected_relation": "Catalog metadata has 002 preceded by 003, not by 032; the row begins with 390.",
        "source_status": "local_image_hit_same_site_type_with_shorter_length",
        "admissible_use": "false_positive_scoring_control",
    },
    {
        "blind_id": "B010",
        "cisi": "M-315",
        "text": "+390-034-002-374-228-741+",
        "source_image": "tmp/m315_second_slot_controls/derived/expanded_first3_context_crops/M-315_upper_face_390-034-002_candidate_target_good.png",
        "truth_class": "negative_002_y_prev_not_032_upper_face",
        "control_role": "scoring_negative",
        "expected_relation": "Catalog metadata has 002 preceded by 034, not by 032; the row begins with 390.",
        "source_status": "local_image_hit_same_site_type",
        "admissible_use": "false_positive_scoring_control",
    },
    {
        "blind_id": "B011",
        "cisi": "M-315",
        "text": "+390-034-002-374-228-741+",
        "source_image": "tmp/m315_second_slot_controls/derived/expanded_first3_context_crops/M-315_lower_impression_390-034-002_candidate_target_good.png",
        "truth_class": "negative_002_y_prev_not_032_lower_impression",
        "control_role": "scoring_negative",
        "expected_relation": "Catalog metadata has 002 preceded by 034, not by 032; the row begins with 390.",
        "source_status": "local_image_hit_same_site_type",
        "admissible_use": "false_positive_scoring_control",
    },
    {
        "blind_id": "B012",
        "cisi": "M-1273",
        "text": "+740-055-002-861-603+",
        "source_image": "tmp/032_002_861_suffix_split/M1273_impression_a_cisi_pakistan_n195.png",
        "trim_bottom_px": 210,
        "truth_class": "negative_002_y_prev_not_032_suffix_control",
        "control_role": "scoring_negative",
        "expected_relation": "Catalog metadata has 002 preceded by 055, not by 032, followed by the 861-603 suffix lane.",
        "source_status": "local_image_hit_suffix_split_control",
        "admissible_use": "false_positive_scoring_control",
    },
    {
        "blind_id": "B013",
        "cisi": "M-376",
        "text": "+740-100-176-002-861-533-717+",
        "source_image": "tmp/032_002_861_suffix_split/M376_impression_a_cisi_india_n129.png",
        "trim_bottom_px": 36,
        "truth_class": "negative_002_y_prev_not_032_suffix_control",
        "control_role": "scoring_negative",
        "expected_relation": "Catalog metadata has 002 preceded by 176, not by 032, followed by the 861-533-717 suffix lane.",
        "source_status": "local_image_hit_suffix_split_control",
        "admissible_use": "false_positive_scoring_control",
    },
    {
        "blind_id": "B014",
        "cisi": "M-683",
        "text": "+740-798-231-002-298-460-032+",
        "source_image": "tmp/m685_cisi2/derived/m685_page37_m683_m686_context_gray_autocontrast.png",
        "truth_class": "negative_032_next_not_002_and_002_y_prev_not_032",
        "control_role": "quarantine_negative_context_crop",
        "expected_relation": "Catalog metadata has 002 away from terminal 032; context crop is not a clean signband crop.",
        "source_status": "local_context_image_hit_not_signband_boxed",
        "admissible_use": "quarantine_distractor_not_scoring",
    },
    {
        "blind_id": "B015",
        "cisi": "M-381",
        "text": "+740-055-220-032-798-002-820+",
        "source_image": "tmp/source_box_negative_control_v2/panel_crops/M-381_cisi_india_n129_plate_label_free_panel_enhanced_x2.jpg",
        "truth_class": "negative_032_not_adjacent_to_002_stress",
        "control_role": "scoring_negative",
        "expected_relation": "Catalog metadata places 798 between 032 and 002; prior blind reviews found this crop segmentation-unstable, so it is a stress control.",
        "source_status": "source_visible_ready_for_token_box_adjudication_but_prior_blind_reviews_found_unstable_segmentation",
        "admissible_use": "false_positive_scoring_control_with_instability_note",
    },
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_blind_images() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    BLIND_DIR.mkdir(parents=True, exist_ok=True)
    manifest_rows: list[dict[str, object]] = []
    key_rows: list[dict[str, object]] = []

    for item in ITEMS:
        source = ROOT / str(item["source_image"])
        if not source.exists():
            raise FileNotFoundError(source)
        transformed = bool(item.get("trim_bottom_px"))
        suffix = ".png" if transformed else source.suffix.lower()
        blind_path = BLIND_DIR / f"{item['blind_id']}{suffix}"
        if transformed:
            im = Image.open(source).convert("RGB")
            trim_bottom_px = int(item.get("trim_bottom_px", 0))
            if trim_bottom_px:
                w, h = im.size
                im = im.crop((0, 0, w, max(1, h - trim_bottom_px)))
            im.save(blind_path)
        else:
            shutil.copyfile(source, blind_path)
        image_hash = sha256_file(blind_path)

        manifest_rows.append(
            {
                "date": RUN_DATE,
                "packet_id": PACKET_ID,
                "blind_id": item["blind_id"],
                "image_path": str(blind_path.relative_to(ROOT)).replace("\\", "/"),
                "image_sha256": image_hash,
                "review_stage": "stage1_blind_tokenization",
                "review_task": "Box every visible sign token in visual order; do not use catalogue text, object ID, or expected sequence.",
                "required_output": "token_count; visual_order_note; token_boxes_json; adjacent_pair_notes; uncertainty_notes",
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
                "source_image": item["source_image"],
                "source_status": item["source_status"],
                "blind_image_sha256": image_hash,
                "accepted_claims_increment": 0,
            }
        )

    return manifest_rows, key_rows


def make_contact_sheet(manifest_rows: list[dict[str, object]]) -> None:
    try:
        font = ImageFont.truetype("arial.ttf", 18)
        small = ImageFont.truetype("arial.ttf", 14)
    except Exception:
        font = ImageFont.load_default()
        small = font

    thumbs: list[tuple[str, Image.Image]] = []
    for row in manifest_rows:
        image_path = ROOT / str(row["image_path"])
        im = Image.open(image_path).convert("RGB")
        im.thumbnail((460, 220))
        thumbs.append((str(row["blind_id"]), im.copy()))

    columns = 2
    cell_w = 510
    cell_h = 280
    rows = (len(thumbs) + columns - 1) // columns
    sheet = Image.new("RGB", (columns * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    for index, (blind_id, im) in enumerate(thumbs):
        col = index % columns
        row = index // columns
        x = col * cell_w + 20
        y = row * cell_h + 42
        draw.text((col * cell_w + 20, row * cell_h + 12), blind_id, fill=(0, 0, 0), font=font)
        sheet.paste(im, (x, y))
        draw.rectangle((x - 1, y - 1, x + im.width + 1, y + im.height + 1), outline=(180, 180, 180), width=1)

    CONTACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(CONTACT_SHEET)


def main() -> None:
    manifest_rows, key_rows = copy_blind_images()
    make_contact_sheet(manifest_rows)

    review_rows = [
        {
            "date": RUN_DATE,
            "packet_id": PACKET_ID,
            "reviewer": "",
            "blind_id": row["blind_id"],
            "stage1_visual_token_count": "",
            "stage1_visual_order_note": "",
            "stage1_token_boxes_json": "",
            "stage1_adjacent_pair_notes": "",
            "stage1_uncertainty_notes": "",
            "stage2_after_unblind_catalog_alignment": "",
            "stage2_target_relation_present_yes_no_uncertain": "",
            "stage2_confidence": "",
            "stage2_notes": "",
        }
        for row in manifest_rows
    ]

    write_csv(BLIND_MANIFEST, list(manifest_rows[0].keys()), manifest_rows)
    write_csv(ANSWER_KEY, list(key_rows[0].keys()), key_rows)
    write_csv(REVIEW_TEMPLATE, list(review_rows[0].keys()), review_rows)

    summary = {
        "date": RUN_DATE,
        "packet_id": PACKET_ID,
        "status": "blind_token_box_packet_created_no_claim_promotion",
        "counts": {
            "blind_items": len(manifest_rows),
            "primary_targets": sum(1 for row in key_rows if str(row["control_role"]).startswith("primary_target")),
            "positive_calibrators": sum(1 for row in key_rows if str(row["control_role"]).startswith("positive_calibrator")),
            "scoring_negatives": sum(1 for row in key_rows if row["control_role"] == "scoring_negative"),
            "scoring_negative_unique_cisis": len(
                {str(row["cisi"]) for row in key_rows if row["control_role"] == "scoring_negative"}
            ),
            "quarantine_negatives": sum(1 for row in key_rows if str(row["control_role"]).startswith("quarantine_negative")),
            "accepted_claims_increment": 0,
        },
        "null_question": (
            "Is M-70's broad 032-002-390-692 order window distinguishable from matched "
            "source/metadata false positives produced by the same broad-window procedure on rows "
            "with comparable site, type, length, and local-image availability but without the same "
            "catalog-slot adjacency?"
        ),
        "files": {
            "blind_manifest": str(BLIND_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
            "answer_key": str(ANSWER_KEY.relative_to(ROOT)).replace("\\", "/"),
            "review_template": str(REVIEW_TEMPLATE.relative_to(ROOT)).replace("\\", "/"),
            "contact_sheet": str(CONTACT_SHEET.relative_to(ROOT)).replace("\\", "/"),
            "blind_image_dir": str(BLIND_DIR.relative_to(ROOT)).replace("\\", "/"),
        },
        "promotion_thresholds": [
            "This packet can only promote M-70 to source-boxed order-window candidate, never to a reading, value, meaning, language ID, or accepted structural claim.",
            "Two or more independent blind reviews must recover a five-token M-70 signband on both face and impression and mark a stable adjacent-pair/order window before seeing the answer key.",
            "At least six unique scoring-negative rows must remain reviewable after blind quality screening; otherwise M-70 stays at broad order-window status.",
            "Controls must produce zero hard target-like hits. One soft ambiguous partial hit is allowed only if adjudicated as damage, cropping, or non-comparable source quality before unblinding.",
            "Quarantine negatives may diagnose reviewer behavior but cannot be counted in false-positive denominators until their source crops are packet-ready.",
        ],
        "interpretation_boundary": "No sign value, phonetic value, semantic value, physical source direction, language identification, or accepted structural claim follows from this packet.",
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
