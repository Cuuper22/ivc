from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path.cwd()
RUN_DATE = "2026-05-29"
AUDIT_ID = "m12_bg001_token_count_audit_v1"

REPORTS = ROOT / "data" / "open_prototype" / "reports"
TMP = ROOT / "tmp" / "m12_token_count_audit"

PAGE_N45 = ROOT / "tmp" / "002_y_branch_gap_public_source_acquisition" / "pages" / "M_12_cisi_india_n45_2.jpg"
BG001_CROP = ROOT / "tmp" / "002_y_branch_gap_blind_packet" / "source_crops" / "BG001_source_crop.png"
BG009_CROP = ROOT / "tmp" / "002_y_branch_gap_blind_packet" / "source_crops" / "BG009_source_crop.png"

ANSWER_KEY = REPORTS / "campaign_002_y_branch_gap_blind_answer_key.csv"
SCORED_ROWS = REPORTS / "campaign_002_y_branch_gap_blind_scored_rows.csv"
ARTIFACT_WITNESSES = ROOT / "data" / "sign_crosswalk" / "artifact_witnesses.csv"

OBSERVATIONS_CSV = REPORTS / "campaign_m12_token_count_audit_observations.csv"
SUMMARY_JSON = REPORTS / "campaign_m12_token_count_audit_summary.json"
CONTACT_SHEET = TMP / "m12_token_count_audit_contact_sheet.png"


CROPS = [
    {
        "crop_id": "m12_face_A_panel",
        "side_label": "M-12 A",
        "crop_kind": "source_panel",
        "path": "m12_face_A_panel_source.png",
        "box": (70, 2140, 1195, 3325),
        "note": "CISI India leaf n45 lower-left source panel labelled M-12 A.",
    },
    {
        "crop_id": "m12_face_A_signband",
        "side_label": "M-12 A",
        "crop_kind": "signband_closeup",
        "path": "m12_face_A_signband_source.png",
        "box": (75, 2140, 1185, 2680),
        "note": "Label-free signband crop from M-12 A.",
    },
    {
        "crop_id": "m12_impression_a_panel",
        "side_label": "M-12 a",
        "crop_kind": "source_panel",
        "path": "m12_impression_a_panel_source.png",
        "box": (1230, 2140, 2340, 3325),
        "note": "CISI India leaf n45 lower-right source panel labelled M-12 a.",
    },
    {
        "crop_id": "m12_impression_a_signband",
        "side_label": "M-12 a",
        "crop_kind": "signband_closeup",
        "path": "m12_impression_a_signband_source.png",
        "box": (1240, 2140, 2335, 2680),
        "note": "Label-free signband crop from M-12 a; this is the source side used for BG001.",
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


def token_count_from_lipi_text(text: str) -> int:
    clean = text.replace("+", "").replace("[", "").replace("]", "")
    return len([part for part in clean.split("-") if part.strip()])


def token_count_from_space_sequence(text: str) -> int:
    return len([part for part in text.split() if part.strip()])


def enhance(image: Image.Image) -> Image.Image:
    gray = ImageOps.grayscale(image)
    gray = ImageOps.autocontrast(gray, cutoff=1)
    return ImageOps.invert(gray).resize((gray.width * 2, gray.height * 2), Image.Resampling.LANCZOS)


def create_crops() -> list[dict[str, object]]:
    TMP.mkdir(parents=True, exist_ok=True)
    page = Image.open(PAGE_N45).convert("RGB")
    rows: list[dict[str, object]] = []
    for spec in CROPS:
        crop = page.crop(spec["box"])
        source_path = TMP / str(spec["path"])
        enhanced_path = TMP / str(spec["path"]).replace("_source.png", "_enhanced_x2.png")
        crop.save(source_path)
        enhance(crop).save(enhanced_path)
        rows.append(
            {
                "crop_id": spec["crop_id"],
                "side_label": spec["side_label"],
                "crop_kind": spec["crop_kind"],
                "source_page": str(PAGE_N45.relative_to(ROOT)).replace("\\", "/"),
                "crop_box_xyxy": "|".join(str(v) for v in spec["box"]),
                "crop_path": str(source_path.relative_to(ROOT)).replace("\\", "/"),
                "enhanced_crop_path": str(enhanced_path.relative_to(ROOT)).replace("\\", "/"),
                "crop_sha256": sha256_file(source_path),
                "enhanced_crop_sha256": sha256_file(enhanced_path),
                "note": spec["note"],
            }
        )
    return rows


def blind_count_profile() -> tuple[list[dict[str, object]], dict[str, object]]:
    scored = read_csv(SCORED_ROWS)
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in scored:
        grouped[row["blind_id"]].append(row)

    profiles = []
    for blind_id, rows in sorted(grouped.items()):
        counts = [int(row["review_token_count"]) for row in rows if row["review_token_count"].isdigit()]
        expected = int(rows[0]["expected_token_count"])
        all_numeric = len(counts) == len(rows)
        all_same = all_numeric and len(set(counts)) == 1
        same_mismatch = all_same and counts[0] != expected
        profiles.append(
            {
                "blind_id": blind_id,
                "cisi": rows[0]["cisi"],
                "role_class": rows[0]["role_class"],
                "expected_token_count": expected,
                "reviewed_numeric_counts": counts,
                "all_numeric_counts_same": all_same,
                "stable_count_mismatch": same_mismatch,
                "all_reviewers_marked_uncertain": all(row["review_count_uncertain"].lower() == "true" for row in rows),
                "notes": " | ".join(row["notes"] for row in rows if row.get("notes")),
            }
        )

    scoring_negatives = [row for row in profiles if row["role_class"] == "scoring_negative"]
    stable_negative_mismatches = [row for row in scoring_negatives if row["stable_count_mismatch"]]
    summary = {
        "scoring_negative_rows": len(scoring_negatives),
        "stable_count_mismatch_scoring_negatives": len(stable_negative_mismatches),
        "stable_count_mismatch_scoring_negative_rate": (
            len(stable_negative_mismatches) / len(scoring_negatives) if scoring_negatives else None
        ),
        "stable_mismatch_rows": [
            {
                "blind_id": row["blind_id"],
                "cisi": row["cisi"],
                "role_class": row["role_class"],
                "expected_token_count": row["expected_token_count"],
                "reviewed_numeric_counts": row["reviewed_numeric_counts"],
                "all_reviewers_marked_uncertain": row["all_reviewers_marked_uncertain"],
            }
            for row in profiles
            if row["stable_count_mismatch"]
        ],
    }
    return profiles, summary


def m12_catalog_witnesses() -> list[dict[str, object]]:
    rows = []
    for row in read_csv(ARTIFACT_WITNESSES):
        if row["artifact_id"] != "M-12":
            continue
        sequence = row["sign_sequence"]
        count = token_count_from_space_sequence(sequence)
        rows.append(
            {
                "witness_id": row["witness_id"],
                "system_id": row["system_id"],
                "row_id": row["row_id"],
                "side_id": row["side_id"],
                "sequence": sequence,
                "token_count": count,
                "direction": row["direction"],
                "provenance_tier": row["provenance_tier"],
            }
        )
    return rows


def create_contact_sheet(crop_rows: list[dict[str, object]], profiles: list[dict[str, object]]) -> None:
    sheet_items = [
        ("M-12 A panel", TMP / "m12_face_A_panel_source.png"),
        ("M-12 A signband", TMP / "m12_face_A_signband_enhanced_x2.png"),
        ("M-12 a panel", TMP / "m12_impression_a_panel_source.png"),
        ("M-12 a signband", TMP / "m12_impression_a_signband_enhanced_x2.png"),
        ("BG001 blind crop", BG001_CROP),
        ("BG009 scoring-negative crop", BG009_CROP),
    ]
    thumbs = []
    for label, path in sheet_items:
        image = Image.open(path).convert("RGB")
        image.thumbnail((520, 360), Image.Resampling.LANCZOS)
        thumbs.append((label, path, image.copy()))

    width = 1100
    row_height = 500
    height = row_height * 3
    sheet = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 22)
        small = ImageFont.truetype("arial.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
        small = ImageFont.load_default()

    bg001 = next(row for row in profiles if row["blind_id"] == "BG001")
    bg009 = next(row for row in profiles if row["blind_id"] == "BG009")
    captions = {
        "BG001 blind crop": f"BG001/M-12: catalog {bg001['expected_token_count']}, blind {bg001['reviewed_numeric_counts']}",
        "BG009 scoring-negative crop": f"BG009/M-654: catalog {bg009['expected_token_count']}, blind {bg009['reviewed_numeric_counts']}",
    }

    for idx, (label, path, image) in enumerate(thumbs):
        col = idx % 2
        row = idx // 2
        x = col * 550 + 20
        y = row * row_height + 20
        draw.text((x, y), label, fill="black", font=font)
        caption = captions.get(label, str(path.relative_to(ROOT)).replace("\\", "/"))
        draw.text((x, y + 28), caption, fill="black", font=small)
        sheet.paste(image, (x, y + 56))
        draw.rectangle((x, y + 56, x + image.width, y + 56 + image.height), outline="black", width=1)

    CONTACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(CONTACT_SHEET)


def main() -> None:
    crop_rows = create_crops()
    profiles, blind_summary = blind_count_profile()
    catalog_witnesses = m12_catalog_witnesses()
    create_contact_sheet(crop_rows, profiles)

    answer_key = {row["blind_id"]: row for row in read_csv(ANSWER_KEY)}
    bg001_key = answer_key["BG001"]
    lipi_text = bg001_key["target_text"]
    lipi_catalog_count = token_count_from_lipi_text(lipi_text)

    observation_rows: list[dict[str, object]] = []
    for row in crop_rows:
        observation_rows.append(
            {
                "date": RUN_DATE,
                "audit_id": AUDIT_ID,
                "cisi": "M-12",
                "artifact_side": row["side_label"],
                "crop_kind": row["crop_kind"],
                "source_page": row["source_page"],
                "crop_box_xyxy": row["crop_box_xyxy"],
                "crop_path": row["crop_path"],
                "enhanced_crop_path": row["enhanced_crop_path"],
                "crop_sha256": row["crop_sha256"],
                "catalog_sequence": lipi_text,
                "catalog_token_count": lipi_catalog_count,
                "blind_review_counts": "10|10|10" if row["side_label"] == "M-12 a" else "",
                "packet_false_positive_control": "BG009 scoring negative has the same stable over-count pattern",
                "status": "source_crop_audit_artifact_only_no_claim_increment",
                "accepted_claims_increment": 0,
                "note": row["note"],
            }
        )

    write_csv(
        OBSERVATIONS_CSV,
        observation_rows,
        [
            "date",
            "audit_id",
            "cisi",
            "artifact_side",
            "crop_kind",
            "source_page",
            "crop_box_xyxy",
            "crop_path",
            "enhanced_crop_path",
            "crop_sha256",
            "catalog_sequence",
            "catalog_token_count",
            "blind_review_counts",
            "packet_false_positive_control",
            "status",
            "accepted_claims_increment",
            "note",
        ],
    )

    summary = {
        "date": RUN_DATE,
        "audit_id": AUDIT_ID,
        "status": "audit_lead_not_claim",
        "cisi": "M-12",
        "catalog_text": lipi_text,
        "catalog_token_count": lipi_catalog_count,
        "catalog_witnesses": catalog_witnesses,
        "source_crops": crop_rows,
        "blind_count_profile_summary": blind_summary,
        "forger_boundary": (
            "A stable blind token-count mismatch has an observed packet false-positive control: "
            "BG009/M-654 is a scoring negative with stable 6-versus-4 over-counting. "
            "Therefore BG001/M-12 cannot be promoted as a catalog-correction or tokenization claim."
        ),
        "skeptic_attacks_logged": [
            "case-insensitive output filename collision in the first ad hoc crop pass; corrected with case-safe names",
            "same-packet scoring negative BG009 reproduces stable over-counting",
            "all BG001 reviewers marked the token count uncertain",
            "M-12 has both Lipi and Mayig catalog witnesses at nine tokens; neither source is source-box proof",
            "public CISI plate has face/impression relief and animal-head overlap that can create extra visual units",
        ],
        "decision": "Keep BG001/M-12 as a source/catalog tokenization audit target. Do not increment any accepted claim count.",
        "accepted_claims_increment": 0,
        "outputs": {
            "observations_csv": str(OBSERVATIONS_CSV.relative_to(ROOT)).replace("\\", "/"),
            "summary_json": str(SUMMARY_JSON.relative_to(ROOT)).replace("\\", "/"),
            "contact_sheet": str(CONTACT_SHEET.relative_to(ROOT)).replace("\\", "/"),
        },
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
