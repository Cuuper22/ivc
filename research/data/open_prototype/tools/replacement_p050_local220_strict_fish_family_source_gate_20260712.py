#!/usr/bin/env python3
"""Test whether pictures of real objects earn a strict local-220 = Mayig-P050 crosswalk.

Two corpora list the same inscriptions with different sign names: the local Lipi
transcripts (sign "220") and the Mayig corpus (sign "P050", described there as
"Fish with no other decoration"). Agreement between two transcripts is not
evidence, because both could copy the same mistake, so this gate goes back to the
object images. For four pinned witnesses it re-reads the Lipi metadata, the Mayig
side record, and reports/crosswalk_alignment_pairs.csv, checks that every sequence
and every SHA-256 hash still matches the values recorded here, then cuts the
recorded token box out of the cached seal photograph and saves a raw crop, a
3x autocontrast enlargement for review, and a four-cell contact sheet.

It deliberately separates three propositions:

1. the two corpora put local 220 and Mayig P050 at the same object-side index;
2. the cached panel contains a broad fish/leaf-compatible glyph at that index;
3. the glyph is specifically the undecorated P050 type.

Only proposition 3 can promote a strict 220=P050 crosswalk, and it needs at least
three independent primary-catalog boxes with no contradiction. Outputs are a
witnesses CSV, a criteria CSV, and a summary JSON under reports/. The pinned
2026-07-12 panels are low-resolution derivative panels whose internal-decoration
state is unresolved, so the run records PARK: same-position and broad-family
pressure, no accepted crosswalk, value, phonetic reading, or translation. This is a
fixed adjudication snapshot; genuinely new evidence requires a new dated gate.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps


RUN_DATE = "2026-07-12"
PREFIX = "replacement_p050_local220_strict_fish_family_source_gate_20260712"
RESEARCH_ROOT = Path(__file__).resolve().parents[3]
REPO_ROOT = RESEARCH_ROOT.parent
REPORTS_DIR = RESEARCH_ROOT / "data" / "open_prototype" / "reports"
TOKEN_BOX_DIR = REPORTS_DIR / f"{PREFIX}_token_boxes"

LIPI_METADATA = RESEARCH_ROOT / "data" / "open_prototype" / "lipi" / "metadata_filtered.csv"
CROSSWALK_PAIRS = REPORTS_DIR / "crosswalk_alignment_pairs.csv"
MAYIG_ROOT = (
    REPO_ROOT
    / "evidence"
    / "tmp"
    / "mayig_feature_namespace_probe"
    / "repo"
    / "indus-valley-script-corpus-ad2f1e218a34b8c33c57de0d6cb8d99272765bbb"
)
P050_FEATURE = MAYIG_ROOT / "features" / "P050.json"
SOURCE_IMAGE_DIR = (
    REPO_ROOT
    / "evidence"
    / "tmp"
    / "002390x_3335_yajnadevam_repo_trace_20260531"
    / "repo"
    / "public"
    / "seal_images"
)

# These are snapshot evidence units, not a flexible image-search queue.  A new
# primary plate or a changed crop requires a new dated gate, not silent mutation.
WITNESSES: tuple[dict[str, Any], ...] = (
    {
        "neutral_id": "T001",
        "cisi": "M-37",
        "lipi_id": "2565.1",
        "mayig_side_id": "M-37A",
        "mayig_record": "corpus/m001_m099/m037.json",
        "local_sequence": ["520", "220", "415"],
        "mayig_sequence": ["P217", "P050", "P092"],
        "target_index_0based": 1,
        "source_image": "M-37_a.jpg",
        "source_sha256": "f496db9db2889e46848e714acbb9836b71f0dd7637496d19b54661f0211ab349",
        "source_dimensions": [370, 435],
        "token_box_xyxy": [78, 0, 178, 175],
        "source_route_class": "cached_derivative_panel_primary_plate_unresolved",
        "panel_view": "cached_derivative_lowercase_a",
        "mirror_relation": "unresolved_not_used_to_claim_reading_direction",
        "display_order_mapping": "token_box_visually_aligned_to_stored_transcript_order",
        "panel_token_count_state": "three_tokens_resolved",
        "target_isolation_state": "mostly_isolated_neighbor_pressure",
        "graphic_family_state": "broad_fish_leaf_compatible",
        "internal_decoration_state": "unresolved_at_cached_resolution",
        "visual_confidence": "medium",
        "contradiction_state": "none_seen",
        "visual_note": (
            "The middle glyph is source-visible and fish/leaf-compatible, but the cached panel "
            "does not resolve whether its body is genuinely undecorated."
        ),
    },
    {
        "neutral_id": "T002",
        "cisi": "M-124",
        "lipi_id": "2651.1",
        "mayig_side_id": "M-124A",
        "mayig_record": "corpus/m100_m199/m124.json",
        "local_sequence": ["740", "923", "220", "032"],
        "mayig_sequence": ["P324", "P175", "P050", "P145"],
        "target_index_0based": 2,
        "source_image": "M-124_a.jpg",
        "source_sha256": "e77930e4099d357d6cd0a25a14113f1f6777f1c4eb93e7086b1f7275656247cf",
        "source_dimensions": [330, 386],
        "token_box_xyxy": [88, 0, 154, 130],
        "source_route_class": "cached_derivative_panel_primary_plate_unresolved",
        "panel_view": "cached_derivative_lowercase_a",
        "mirror_relation": "unresolved_not_used_to_claim_reading_direction",
        "display_order_mapping": "token_box_visually_aligned_to_stored_transcript_order",
        "panel_token_count_state": "four_tokens_resolved",
        "target_isolation_state": "isolated",
        "graphic_family_state": "broad_fish_leaf_compatible",
        "internal_decoration_state": "unresolved_at_cached_resolution",
        "visual_confidence": "medium",
        "contradiction_state": "none_seen",
        "visual_note": (
            "The third glyph aligns cleanly by row position and has the expected broad outline; "
            "fine internal marks cannot be excluded from this derivative."
        ),
    },
    {
        "neutral_id": "T003",
        "cisi": "M-151",
        "lipi_id": "2678.1",
        "mayig_side_id": "M-151A",
        "mayig_record": "corpus/m100_m199/m151.json",
        "local_sequence": ["220", "065", "864"],
        "mayig_sequence": ["P050", "P201", "P393"],
        "target_index_0based": 0,
        "source_image": "M-151_a.jpg",
        "source_sha256": "3f6ad3cacb63c5791a188d2d019c98713ecef99ef0bf1f7486f137d796585901",
        "source_dimensions": [373, 411],
        "token_box_xyxy": [0, 0, 72, 145],
        "source_route_class": "cached_derivative_panel_primary_plate_unresolved",
        "panel_view": "cached_derivative_lowercase_a",
        "mirror_relation": "unresolved_not_used_to_claim_reading_direction",
        "display_order_mapping": "token_box_visually_aligned_to_stored_transcript_order",
        "panel_token_count_state": "three_tokens_resolved",
        "target_isolation_state": "mostly_isolated_edge_crop",
        "graphic_family_state": "broad_fish_leaf_compatible",
        "internal_decoration_state": "unresolved_at_cached_resolution",
        "visual_confidence": "medium_low",
        "contradiction_state": "none_seen",
        "visual_note": (
            "The first glyph is a plausible fish/leaf witness and agrees with both transcripts, "
            "but edge placement and low resolution block an undecorated-type judgment."
        ),
    },
    {
        "neutral_id": "T004",
        "cisi": "M-174",
        "lipi_id": "2699.1",
        "mayig_side_id": "M-174A",
        "mayig_record": "corpus/m100_m199/m174.json",
        "local_sequence": ["740", "923", "220", "032", "002", "820"],
        "mayig_sequence": ["P324", "P175", "P050", "P145", "P122", "P378"],
        "target_index_0based": 2,
        "source_image": "M-174_a.jpg",
        "source_sha256": "403aa87538601982f8481d2ccd5d6781ab528774d92bb1c34d7e1f4013f3388d",
        "source_dimensions": [298, 349],
        "token_box_xyxy": [52, 0, 108, 105],
        "source_route_class": "cached_derivative_panel_primary_plate_unresolved",
        "panel_view": "cached_derivative_lowercase_a",
        "mirror_relation": "unresolved_not_used_to_claim_reading_direction",
        "display_order_mapping": "token_box_visually_aligned_to_stored_transcript_order",
        "panel_token_count_state": "six_tokens_resolved",
        "target_isolation_state": "isolated_but_low_resolution",
        "graphic_family_state": "broad_fish_leaf_compatible",
        "internal_decoration_state": "unresolved_at_cached_resolution",
        "visual_confidence": "low_medium",
        "contradiction_state": "none_seen",
        "visual_note": (
            "The third glyph is positionally recoverable and broad-family compatible; the Lipi "
            "condition field is Poor and the cached pixels cannot adjudicate decoration."
        ),
    },
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def parse_local_tokens(text: str) -> list[str]:
    import re

    return re.findall(r"\d{3}", text or "")


def mayig_tokens(record: dict[str, Any]) -> list[str]:
    return [str(item["id"]) for item in record.get("graphemes", [])]


def exactly_one(rows: list[dict[str, Any]], predicate: Any, label: str) -> dict[str, Any]:
    matches = [row for row in rows if predicate(row)]
    require(len(matches) == 1, f"Expected exactly one {label}; found {len(matches)}")
    return matches[0]


def make_contact_sheet(enhanced_paths: list[tuple[str, Path]]) -> Path:
    loaded: list[tuple[str, Image.Image]] = []
    try:
        for neutral_id, image_path in enhanced_paths:
            loaded.append((neutral_id, Image.open(image_path).convert("L")))
        cell_width = max(image.width for _, image in loaded) + 32
        cell_height = max(image.height for _, image in loaded) + 58
        sheet = Image.new("L", (cell_width * 2, cell_height * 2), color=255)
        draw = ImageDraw.Draw(sheet)
        for index, (neutral_id, image) in enumerate(loaded):
            col = index % 2
            row = index // 2
            x = col * cell_width + (cell_width - image.width) // 2
            y = row * cell_height + 30
            draw.text((col * cell_width + 12, row * cell_height + 8), neutral_id, fill=0)
            sheet.paste(image, (x, y))
        output = TOKEN_BOX_DIR / f"{PREFIX}_neutral_contact_sheet.png"
        sheet.save(output)
        sheet.close()
        return output
    finally:
        for _, image in loaded:
            image.close()


def main() -> None:
    require(P050_FEATURE.exists(), f"Missing pinned Mayig feature: {P050_FEATURE}")
    require(LIPI_METADATA.exists(), f"Missing Lipi metadata: {LIPI_METADATA}")
    require(CROSSWALK_PAIRS.exists(), f"Missing crosswalk pairs: {CROSSWALK_PAIRS}")

    feature = json.loads(P050_FEATURE.read_text(encoding="utf-8"))
    require(feature.get("id") == "P050", "Pinned feature is not P050")
    require(feature.get("description") == "Fish with no other decoration", "P050 description drifted")
    require(feature.get("parpola_graphemes") == ["V177", "V517"], "P050 Parpola mapping drifted")
    require(feature.get("wells_graphemes") == ["W220"], "P050 Wells mapping drifted")
    require(feature.get("mahadevan_graphemes") == ["M059"], "P050 Mahadevan mapping drifted")

    metadata = read_csv(LIPI_METADATA)
    pairs = read_csv(CROSSWALK_PAIRS)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_BOX_DIR.mkdir(parents=True, exist_ok=True)

    witness_rows: list[dict[str, Any]] = []
    enhanced_paths: list[tuple[str, Path]] = []
    mayig_input_rows: list[dict[str, str]] = []
    image_input_rows: list[dict[str, str]] = []

    for witness in WITNESSES:
        local_row = exactly_one(
            metadata,
            lambda row, w=witness: row.get("id") == w["lipi_id"] and row.get("cisi") == w["cisi"],
            f"Lipi row {witness['lipi_id']} / {witness['cisi']}",
        )
        local_sequence = parse_local_tokens(local_row.get("text", ""))
        require(local_sequence == witness["local_sequence"], f"Local sequence drift for {witness['cisi']}")
        require(local_row.get("sides") == "1", f"Expected one-sided Lipi object for {witness['cisi']}")
        require(local_row.get("dir.") == "R/L", f"Direction metadata drift for {witness['cisi']}")

        mayig_path = MAYIG_ROOT / witness["mayig_record"]
        require(mayig_path.exists(), f"Missing Mayig record: {mayig_path}")
        mayig_records = json.loads(mayig_path.read_text(encoding="utf-8"))
        mayig_input_rows.append({"path": relative(mayig_path), "sha256": sha256_file(mayig_path)})
        mayig_record = exactly_one(
            mayig_records,
            lambda row, w=witness: row.get("id") == w["mayig_side_id"],
            f"Mayig side {witness['mayig_side_id']}",
        )
        mayig_sequence = mayig_tokens(mayig_record)
        require(mayig_sequence == witness["mayig_sequence"], f"Mayig sequence drift for {witness['cisi']}")

        index = int(witness["target_index_0based"])
        require(len(local_sequence) == len(mayig_sequence), f"Sequence length mismatch for {witness['cisi']}")
        require(local_sequence[index] == "220", f"Local target index is not 220 for {witness['cisi']}")
        require(mayig_sequence[index] == "P050", f"Mayig target index is not P050 for {witness['cisi']}")

        pair = exactly_one(
            pairs,
            lambda row, w=witness, i=index: (
                row.get("cisi") == w["cisi"]
                and row.get("lipi_id") == w["lipi_id"]
                and row.get("mayig_side_id") == w["mayig_side_id"]
                and row.get("lipi_sign") == "220"
                and row.get("mayig_sign") == "P050"
                and row.get("position_0based") == str(i)
            ),
            f"same-position crosswalk row for {witness['cisi']}",
        )
        require(
            pair.get("evidence_status") == "provisional_position_alignment_only",
            f"Crosswalk snapshot status drift for {witness['cisi']}: {pair.get('evidence_status')}",
        )

        source_image = SOURCE_IMAGE_DIR / witness["source_image"]
        require(source_image.exists(), f"Missing cached source panel: {source_image}")
        actual_hash = sha256_file(source_image)
        require(actual_hash == witness["source_sha256"], f"Source image hash drift for {witness['cisi']}")
        image_input_rows.append({"path": relative(source_image), "sha256": actual_hash})

        with Image.open(source_image) as image:
            image.load()
            require(list(image.size) == witness["source_dimensions"], f"Source dimensions drift for {witness['cisi']}")
            x1, y1, x2, y2 = [int(value) for value in witness["token_box_xyxy"]]
            require(0 <= x1 < x2 <= image.width, f"Invalid x crop box for {witness['cisi']}")
            require(0 <= y1 < y2 <= image.height, f"Invalid y crop box for {witness['cisi']}")
            crop = image.convert("RGB").crop((x1, y1, x2, y2))
            source_crop = TOKEN_BOX_DIR / f"{witness['neutral_id']}_source.png"
            crop.save(source_crop)
            enhanced = ImageOps.autocontrast(ImageOps.grayscale(crop)).resize(
                (crop.width * 3, crop.height * 3), Image.Resampling.LANCZOS
            )
            enhanced_path = TOKEN_BOX_DIR / f"{witness['neutral_id']}_review_x3.png"
            enhanced.save(enhanced_path)
            crop.close()
            enhanced.close()
            enhanced_paths.append((witness["neutral_id"], enhanced_path))

        same_position_bound = local_sequence[index] == "220" and mayig_sequence[index] == "P050"
        row_token_count_resolved = witness["panel_token_count_state"].endswith("_tokens_resolved")
        broad_family_usable = (
            same_position_bound
            and witness["graphic_family_state"] == "broad_fish_leaf_compatible"
            and witness["contradiction_state"] == "none_seen"
        )
        strict_identity_usable = (
            same_position_bound
            and witness["source_route_class"] == "primary_catalog_plate_pinned"
            and witness["target_isolation_state"] == "isolated"
            and row_token_count_resolved
            and witness["graphic_family_state"] == "plain_undecorated_fish"
            and witness["internal_decoration_state"] == "absent_visible"
            and witness["visual_confidence"] in {"high", "medium_high"}
            and witness["contradiction_state"] == "none_seen"
        )
        contradiction = witness["contradiction_state"] != "none_seen"

        witness_rows.append(
            {
                "date": RUN_DATE,
                "neutral_id": witness["neutral_id"],
                "cisi": witness["cisi"],
                "lipi_id": witness["lipi_id"],
                "mayig_side_id": witness["mayig_side_id"],
                "target_position_1based": index + 1,
                "local_sequence": " ".join(local_sequence),
                "mayig_sequence": " ".join(mayig_sequence),
                "same_position_bound": str(same_position_bound).lower(),
                "crosswalk_pair_evidence_status": pair.get("evidence_status", ""),
                "lipi_condition": local_row.get("condition", ""),
                "lipi_direction": local_row.get("dir.", ""),
                "lipi_side_count": local_row.get("sides", ""),
                "source_image": relative(source_image),
                "source_sha256": actual_hash,
                "source_dimensions": "x".join(str(value) for value in witness["source_dimensions"]),
                "token_box_xyxy": ",".join(str(value) for value in witness["token_box_xyxy"]),
                "source_crop": relative(source_crop),
                "enhanced_crop": relative(enhanced_path),
                "source_route_class": witness["source_route_class"],
                "panel_view": witness["panel_view"],
                "mirror_relation": witness["mirror_relation"],
                "display_order_mapping": witness["display_order_mapping"],
                "panel_token_count_state": witness["panel_token_count_state"],
                "row_token_count_resolved": str(row_token_count_resolved).lower(),
                "target_isolation_state": witness["target_isolation_state"],
                "graphic_family_state": witness["graphic_family_state"],
                "internal_decoration_state": witness["internal_decoration_state"],
                "visual_confidence": witness["visual_confidence"],
                "visual_note": witness["visual_note"],
                "broad_family_usable": str(broad_family_usable).lower(),
                "strict_identity_usable": str(strict_identity_usable).lower(),
                "contradiction": str(contradiction).lower(),
            }
        )

    contact_sheet = make_contact_sheet(enhanced_paths)

    same_position_count = sum(row["same_position_bound"] == "true" for row in witness_rows)
    distinct_same_position_artifacts = len(
        {row["cisi"] for row in witness_rows if row["same_position_bound"] == "true"}
    )
    broad_family_count = sum(row["broad_family_usable"] == "true" for row in witness_rows)
    strict_identity_count = sum(row["strict_identity_usable"] == "true" for row in witness_rows)
    contradiction_count = sum(row["contradiction"] == "true" for row in witness_rows)
    distinct_strict_artifacts = len(
        {row["cisi"] for row in witness_rows if row["strict_identity_usable"] == "true"}
    )

    criteria_rows = [
        {
            "outcome": "PASS",
            "criterion": "same-position object-side bindings",
            "threshold": ">=3 independent artifacts",
            "observed": distinct_same_position_artifacts,
            "satisfied": str(distinct_same_position_artifacts >= 3).lower(),
        },
        {
            "outcome": "PASS",
            "criterion": "strict source-visible P050 token boxes",
            "threshold": ">=3 independent primary-catalog boxes with isolated target and absent decoration visibly resolved",
            "observed": strict_identity_count,
            "satisfied": str(strict_identity_count >= 3 and distinct_strict_artifacts >= 3).lower(),
        },
        {
            "outcome": "PASS",
            "criterion": "contradictory strict witnesses",
            "threshold": "0",
            "observed": contradiction_count,
            "satisfied": str(contradiction_count == 0).lower(),
        },
        {
            "outcome": "PARK",
            "criterion": "source-position pressure without strict identity",
            "threshold": ">=1 same-position binding, 0 contradictions, and PASS incomplete",
            "observed": f"same_position={same_position_count}; strict={strict_identity_count}; contradictions={contradiction_count}",
            "satisfied": "pending_final_rule",
        },
        {
            "outcome": "FAIL",
            "criterion": "source contradiction or no source-bound target",
            "threshold": ">=1 contradiction or 0 same-position bindings",
            "observed": f"same_position={same_position_count}; contradictions={contradiction_count}",
            "satisfied": str(contradiction_count > 0 or same_position_count == 0).lower(),
        },
    ]

    pass_gate = (
        distinct_same_position_artifacts >= 3
        and strict_identity_count >= 3
        and distinct_strict_artifacts >= 3
        and contradiction_count == 0
    )
    fail_gate = contradiction_count > 0 or same_position_count == 0
    if fail_gate:
        outcome = "FAIL"
        status = "fail_p050_local220_source_bridge_contradicted_or_unbound"
    elif pass_gate:
        outcome = "PASS"
        status = "pass_p050_local220_strict_source_identity_earned"
    else:
        outcome = "PARK"
        status = "park_p050_local220_same_position_pressure_strict_identity_not_earned"
    criteria_rows[3]["satisfied"] = str(outcome == "PARK").lower()

    if outcome == "PASS":
        accepted_now = [
            "local Lipi 220 = Mayig P050 as a strict object-source crosswalk",
            "at least three independent primary-catalog token boxes visibly resolve the undecorated P050 type",
        ]
        not_accepted = [
            "local Lipi 220 = Parpola article sign no. 60",
            "Mayig P050 = Parpola article sign no. 60",
            "Wells W220 or Mahadevan M059 identity beyond Mayig namespace metadata",
            "fish lexical value",
            "phonetic value",
            "language identity",
            "translation",
        ]
    else:
        accepted_now = [
            "four exact Lipi/Mayig same-object same-position 220/P050 alignments are source-panel candidates",
            "the four pinned token boxes are compatible with the broad fish/leaf neighborhood",
            "the cached panels contain no observed contradiction to the candidate bridge",
        ] if outcome == "PARK" else []
        not_accepted = [
            "local Lipi 220 = Mayig P050 as a strict sign identity",
            "local Lipi 220 = Parpola article sign no. 60",
            "Mayig P050 = Parpola article sign no. 60",
            "Wells W220 or Mahadevan M059 identity beyond Mayig namespace metadata",
            "fish lexical value",
            "phonetic value",
            "language identity",
            "translation",
        ]

    witness_csv = REPORTS_DIR / f"{PREFIX}_witnesses.csv"
    criteria_csv = REPORTS_DIR / f"{PREFIX}_criteria.csv"
    summary_json = REPORTS_DIR / f"{PREFIX}_summary.json"
    write_csv(
        witness_csv,
        witness_rows,
        [
            "date",
            "neutral_id",
            "cisi",
            "lipi_id",
            "mayig_side_id",
            "target_position_1based",
            "local_sequence",
            "mayig_sequence",
            "same_position_bound",
            "crosswalk_pair_evidence_status",
            "lipi_condition",
            "lipi_direction",
            "lipi_side_count",
            "source_image",
            "source_sha256",
            "source_dimensions",
            "token_box_xyxy",
            "source_crop",
            "enhanced_crop",
            "source_route_class",
            "panel_view",
            "mirror_relation",
            "display_order_mapping",
            "panel_token_count_state",
            "row_token_count_resolved",
            "target_isolation_state",
            "graphic_family_state",
            "internal_decoration_state",
            "visual_confidence",
            "visual_note",
            "broad_family_usable",
            "strict_identity_usable",
            "contradiction",
        ],
    )
    write_csv(criteria_csv, criteria_rows, ["outcome", "criterion", "threshold", "observed", "satisfied"])

    summary = {
        "date": RUN_DATE,
        "status": status,
        "outcome": outcome,
        "research_question": (
            "Do exact same-object, same-side, same-position source token boxes earn a strict "
            "local Lipi 220 = Mayig P050 crosswalk?"
        ),
        "answer": (
            "The pinned evidence earns repeated same-position and broad fish/leaf-family pressure, "
            "but not strict identity: every panel is a low-resolution cached derivative and the "
            "absence of internal decoration is unresolved."
            if outcome == "PARK"
            else (
                "At least three independent primary-source token boxes earn the strict crosswalk."
                if outcome == "PASS"
                else "The source bridge is contradicted or cannot be bound to a visible target."
            )
        ),
        "feature": {
            "path": relative(P050_FEATURE),
            "sha256": sha256_file(P050_FEATURE),
            "id": feature["id"],
            "description": feature["description"],
            "parpola_graphemes": feature["parpola_graphemes"],
            "wells_graphemes": feature["wells_graphemes"],
            "mahadevan_graphemes": feature["mahadevan_graphemes"],
            "use_limit": "namespace metadata only; these mappings do not themselves prove sign identity",
        },
        "inputs": {
            "lipi_metadata": {"path": relative(LIPI_METADATA), "sha256": sha256_file(LIPI_METADATA)},
            "crosswalk_pairs": {"path": relative(CROSSWALK_PAIRS), "sha256": sha256_file(CROSSWALK_PAIRS)},
            "p050_feature": {"path": relative(P050_FEATURE), "sha256": sha256_file(P050_FEATURE)},
            "mayig_records": mayig_input_rows,
            "source_images": image_input_rows,
        },
        "counts": {
            "candidate_witnesses": len(witness_rows),
            "same_position_source_bound": same_position_count,
            "distinct_same_position_artifacts": distinct_same_position_artifacts,
            "broad_family_usable": broad_family_count,
            "strict_identity_usable": strict_identity_count,
            "distinct_strict_artifacts": distinct_strict_artifacts,
            "contradictions": contradiction_count,
            "accepted_crosswalks": 1 if outcome == "PASS" else 0,
            "accepted_values": 0,
            "accepted_phonetic_readings": 0,
            "accepted_translations": 0,
        },
        "criteria": criteria_rows,
        "accepted_now": accepted_now,
        "not_accepted": not_accepted,
        "blocking_evidence_gap": (
            "At least three independently pinned primary-catalog object-side panels with isolated "
            "target boxes where the body outline and absence of internal decoration are visibly "
            "resolved. A clearly decorated or position-inconsistent strict witness fails the bridge."
        ),
        "outputs": {
            "witnesses": relative(witness_csv),
            "criteria": relative(criteria_csv),
            "summary": relative(summary_json),
            "neutral_contact_sheet": relative(contact_sheet),
            "token_box_directory": relative(TOKEN_BOX_DIR),
        },
    }
    summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "outcome": outcome, "outputs": summary["outputs"]}, indent=2))


if __name__ == "__main__":
    main()
