"""Builds the one-item blind packet for seal M-381, the v2 negative control
whose panel crop reached packet-ready status. M-381 is a negative because in
its catalog text 032 is followed by 798, not directly by 002 — so a blind
reviewer boxing sign tokens on the image should not find 032 adjacent to
002. The script reads the v2 source-status CSV, refuses to run unless M-381
is marked source_visible_ready_for_token_box_adjudication, copies the panel
image to a neutral blind filename with a SHA-256 hash, and writes three
CSVs: the blind manifest (stage-1 task: box every token without using
catalog text), the answer key (kept separate; stage 2 aligns boxes to the
catalog only after tokenization is recorded), and an empty review template.
A JSON summary records the file paths and the zero accepted-claims
increment.
"""
import csv
import hashlib
import json
import shutil
from pathlib import Path


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
STATUS_CSV = REPORTS / "source_box_negative_control_v2_source_status.csv"
BLIND_MANIFEST = REPORTS / "source_box_negative_control_v2_m381_blind_manifest.csv"
ANSWER_KEY = REPORTS / "source_box_negative_control_v2_m381_answer_key.csv"
REVIEW_TEMPLATE = REPORTS / "source_box_negative_control_v2_m381_review_template.csv"
SUMMARY_JSON = REPORTS / "source_box_negative_control_v2_m381_packet_summary.json"
OUT_DIR = ROOT / "tmp" / "source_box_negative_control_v2" / "blind_packet"
RUN_DATE = "2026-05-29"
PACKET_ID = "v2_neg_001"
TARGET_CISI = "M-381"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_status_row():
    with STATUS_CSV.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["cisi"] == TARGET_CISI:
                return row
    raise RuntimeError(f"missing {TARGET_CISI} in {STATUS_CSV}")


def write_csv(path: Path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    row = load_status_row()
    if row["source_status_rank"] != "source_visible_ready_for_token_box_adjudication":
        raise RuntimeError(f"{TARGET_CISI} is not packet-ready: {row['source_status_rank']}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    source_image = ROOT / row["best_local_artifact"]
    if not source_image.exists():
        raise FileNotFoundError(source_image)

    blind_image = OUT_DIR / f"{PACKET_ID}_source_panel.jpg"
    shutil.copyfile(source_image, blind_image)
    blind_hash = sha256_file(blind_image)

    blind_manifest_rows = [
        {
            "date": RUN_DATE,
            "packet_id": PACKET_ID,
            "item_id": "blind_item_001",
            "image_path": str(blind_image.relative_to(ROOT)).replace("\\", "/"),
            "image_sha256": blind_hash,
            "review_stage": "stage1_blind_tokenization",
            "review_task": "Box every visible sign token in the signband in visual order without using catalogue text or object ID.",
            "required_output": "token_count; visual_order_note; token_boxes_json; direction_basis; uncertainty_notes",
            "admissible_use": "blind_tokenization_only",
            "accepted_claims_increment": 0,
        }
    ]
    write_csv(
        BLIND_MANIFEST,
        [
            "date",
            "packet_id",
            "item_id",
            "image_path",
            "image_sha256",
            "review_stage",
            "review_task",
            "required_output",
            "admissible_use",
            "accepted_claims_increment",
        ],
        blind_manifest_rows,
    )

    answer_key_rows = [
        {
            "date": RUN_DATE,
            "packet_id": PACKET_ID,
            "cisi": row["cisi"],
            "lipi_id": row["lipi_id"],
            "route_id": row["best_route_id"],
            "source_url": row["best_source_url"],
            "target_text": row["target_text"],
            "control_class": row["control_class"],
            "metadata_expected_negative": "032 is followed by 798, not immediately by 002",
            "stage2_gate": "Only after blind tokenization: align token boxes to the catalog sequence and decide whether 798 is source-visible between 032 and 002.",
            "source_status_sha256": sha256_file(STATUS_CSV),
            "accepted_claims_increment": 0,
        }
    ]
    write_csv(
        ANSWER_KEY,
        [
            "date",
            "packet_id",
            "cisi",
            "lipi_id",
            "route_id",
            "source_url",
            "target_text",
            "control_class",
            "metadata_expected_negative",
            "stage2_gate",
            "source_status_sha256",
            "accepted_claims_increment",
        ],
        answer_key_rows,
    )

    template_rows = [
        {
            "date": RUN_DATE,
            "packet_id": PACKET_ID,
            "reviewer": "",
            "stage1_visual_token_count": "",
            "stage1_visual_order_note": "",
            "stage1_token_boxes_json": "",
            "stage1_direction_basis": "",
            "stage1_uncertainty_notes": "",
            "stage2_catalog_alignment": "",
            "stage2_032_box_id": "",
            "stage2_002_box_id": "",
            "stage2_intervening_box_ids": "",
            "stage2_adjacent_032_002_visible": "",
            "stage2_confidence": "",
            "stage2_notes": "",
        }
    ]
    write_csv(
        REVIEW_TEMPLATE,
        [
            "date",
            "packet_id",
            "reviewer",
            "stage1_visual_token_count",
            "stage1_visual_order_note",
            "stage1_token_boxes_json",
            "stage1_direction_basis",
            "stage1_uncertainty_notes",
            "stage2_catalog_alignment",
            "stage2_032_box_id",
            "stage2_002_box_id",
            "stage2_intervening_box_ids",
            "stage2_adjacent_032_002_visible",
            "stage2_confidence",
            "stage2_notes",
        ],
        template_rows,
    )

    summary = {
        "date": RUN_DATE,
        "status": "m381_source_visible_negative_control_packet_created",
        "counts": {
            "blind_items": 1,
            "answer_key_rows": 1,
            "review_template_rows": 1,
            "accepted_claims_increment": 0,
        },
        "files": {
            "blind_manifest": str(BLIND_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
            "answer_key": str(ANSWER_KEY.relative_to(ROOT)).replace("\\", "/"),
            "review_template": str(REVIEW_TEMPLATE.relative_to(ROOT)).replace("\\", "/"),
            "blind_image": str(blind_image.relative_to(ROOT)).replace("\\", "/"),
        },
        "boundary": [
            "This packet does not promote a claim.",
            "Stage 1 is blind tokenization only.",
            "Stage 2 may compare the blind boxes to the catalog text, but only after tokenization is recorded.",
        ],
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
