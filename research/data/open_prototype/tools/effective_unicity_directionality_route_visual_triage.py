"""Record the manual visual triage of the v1 public route candidates.

After the v1 route probe found candidate CISI plate pages, a human looked at
nine of the route crops and judged each one: is the seal's source panel
actually visible, is the signband legible, and is the crop clean enough to
feed a blind token-boxing packet? This script encodes those judgments (keyed
by queue rank in MANUAL_REVIEWS) and merges them with the probe's status CSV.
Every row gets an admissibility tier from tier 1 (ready as a blind-packet
candidate — H-654, M-1310, M-1320, M-811) down to tier 6 (no public route at
all); routes not manually reviewed default to tier 4 unreviewed. It writes a
triage CSV, a summary JSON with tier counts and the immediate candidates, and
a contact sheet of the reviewed crops with the reviewer's notes. The triage
selects candidates only; it validates no token order, direction, or meaning,
and the accepted-claims counter stays at zero.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageOps


ROOT = Path.cwd()
RUN_DATE = "2026-05-29"
TRIAGE_ID = "directionality_route_visual_triage_v1"

REPORTS = ROOT / "data" / "open_prototype" / "reports"
TMP = ROOT / "tmp" / "effective_unicity_directionality_public_route_probe"

STATUS_CSV = REPORTS / "effective_unicity_directionality_public_route_probe_status.csv"

OUT_CSV = REPORTS / "effective_unicity_directionality_route_visual_triage.csv"
OUT_JSON = REPORTS / "effective_unicity_directionality_route_visual_triage_summary.json"
CONTACT_SHEET = TMP / "directionality_route_visual_triage_reviewed_contact_sheet.jpg"

ACCEPTED_CLAIMS_INCREMENT = 0

FIELDS = [
    "date",
    "triage_id",
    "queue_rank",
    "representative_cisi",
    "site",
    "type",
    "text",
    "diff_per_transition",
    "route_count",
    "plate_route_count",
    "data_route_count",
    "source_status_rank",
    "best_volume",
    "best_page_index",
    "best_source_url",
    "best_local_artifact",
    "best_artifact_sha256",
    "visual_review_status",
    "admissibility_tier",
    "signband_visible",
    "immediate_blind_packet_candidate",
    "manual_visual_note",
    "next_gate",
    "skeptic_boundary",
    "forger_boundary",
    "accepted_claims_increment",
]


MANUAL_REVIEWS = {
    "4": {
        "visual_review_status": "source_panel_visible_weak_partial",
        "admissibility_tier": "tier_2_source_panel_visible_needs_recrop_or_quality_gate",
        "signband_visible": "partial",
        "immediate_blind_packet_candidate": "no",
        "manual_visual_note": (
            "H-665 A source panel is visible in the OCR route crop, but the signband is dark, partly "
            "cut by the route crop, and weaker than the M-1320/M-811/M-1310/H-654 candidates."
        ),
        "next_gate": "Make a no-overlay source-panel crop from the page image before any token boxing.",
    },
    "5": {
        "visual_review_status": "low_legibility_tablet_route",
        "admissibility_tier": "tier_3_route_only_low_legibility",
        "signband_visible": "uncertain",
        "immediate_blind_packet_candidate": "no",
        "manual_visual_note": (
            "M-1458 is a real page route, but the tablet-like source image is dark/low-legibility at "
            "this public resolution."
        ),
        "next_gate": "Seek higher-quality source image or defer behind clearer candidates.",
    },
    "9": {
        "visual_review_status": "source_panel_visible_candidate",
        "admissibility_tier": "tier_1_ready_for_blind_token_boxing_candidate",
        "signband_visible": "yes",
        "immediate_blind_packet_candidate": "yes",
        "manual_visual_note": (
            "H-654 A is visible with a compact sign sequence; neighboring labels are present, so it "
            "needs a clean no-overlay panel crop before blind token boxing."
        ),
        "next_gate": "Generate no-overlay source-panel crop and include as a positive in the blind token-box packet.",
    },
    "10": {
        "visual_review_status": "source_panel_visible_candidate_needs_no_overlay_recrop",
        "admissibility_tier": "tier_1_ready_for_blind_token_boxing_candidate",
        "signband_visible": "yes",
        "immediate_blind_packet_candidate": "yes",
        "manual_visual_note": (
            "M-1310 A is visible and promising, but the route-label box overlay crosses the useful "
            "view. The underlying page image, not the overlay crop, must be used for boxing."
        ),
        "next_gate": "Generate no-overlay source-panel crop from the page image and blind-box it with matched negatives.",
    },
    "11": {
        "visual_review_status": "source_panel_visible_candidate",
        "admissibility_tier": "tier_1_ready_for_blind_token_boxing_candidate",
        "signband_visible": "yes",
        "immediate_blind_packet_candidate": "yes",
        "manual_visual_note": (
            "M-1320 A is clearly routed to a visible source panel with a legible signband at public "
            "resolution."
        ),
        "next_gate": "Generate no-overlay source-panel crop and include as a positive in the blind token-box packet.",
    },
    "15": {
        "visual_review_status": "source_panel_visible_candidate",
        "admissibility_tier": "tier_1_ready_for_blind_token_boxing_candidate",
        "signband_visible": "yes",
        "immediate_blind_packet_candidate": "yes",
        "manual_visual_note": (
            "M-811 A is routed to a visible source panel; signband and object context are legible "
            "enough for blind token-box adjudication."
        ),
        "next_gate": "Generate no-overlay source-panel crop and include as a positive in the blind token-box packet.",
    },
    "16": {
        "visual_review_status": "low_legibility_tablet_route",
        "admissibility_tier": "tier_3_route_only_low_legibility",
        "signband_visible": "uncertain",
        "immediate_blind_packet_candidate": "no",
        "manual_visual_note": (
            "M-1523 is a page route, but the tablet-like source panel is dark/low-legibility in the "
            "public crop."
        ),
        "next_gate": "Seek higher-quality source image or defer behind clearer candidates.",
    },
    "17": {
        "visual_review_status": "source_panel_visible_volume_mismatch_gate",
        "admissibility_tier": "tier_2_source_panel_visible_needs_recrop_or_quality_gate",
        "signband_visible": "yes",
        "immediate_blind_packet_candidate": "no",
        "manual_visual_note": (
            "H-152 A is visibly routed to a source panel with a legible signband, but the public route "
            "is in the India volume while the row metadata is Harappa. Keep the volume/provenance gate."
        ),
        "next_gate": "Resolve volume/provenance mismatch before adding to any positive blind packet.",
    },
    "27": {
        "visual_review_status": "source_panel_visible_but_low_legibility_complex_tablet",
        "admissibility_tier": "tier_2_source_panel_visible_needs_recrop_or_quality_gate",
        "signband_visible": "partial",
        "immediate_blind_packet_candidate": "no",
        "manual_visual_note": (
            "M-525 has visible routed source panels, but the tablet sides and crop geometry make it "
            "less clean than the tier-1 candidates."
        ),
        "next_gate": "Make side-specific no-overlay crops before considering blind token boxing.",
    },
}

DEFAULT_PLATE_REVIEW = {
    "visual_review_status": "not_yet_visual_reviewed",
    "admissibility_tier": "tier_4_plate_route_unreviewed",
    "signband_visible": "unreviewed",
    "immediate_blind_packet_candidate": "no",
    "manual_visual_note": "Public OCR route exists, but this route was not manually visually triaged in this pass.",
    "next_gate": "Manual visual source-panel review before any token-box packet.",
}

DATA_ONLY_REVIEW = {
    "visual_review_status": "data_or_register_route_only",
    "admissibility_tier": "tier_5_catalog_locator_only",
    "signband_visible": "no",
    "immediate_blind_packet_candidate": "no",
    "manual_visual_note": "Only a late register/data route was found; no source-panel route is available here.",
    "next_gate": "Use as catalog locator only; find actual plate/source image.",
}

NOT_FOUND_REVIEW = {
    "visual_review_status": "not_found_in_public_cisi_ocr_layer",
    "admissibility_tier": "tier_6_no_public_route",
    "signband_visible": "no",
    "immediate_blind_packet_candidate": "no",
    "manual_visual_note": "No exact public CISI OCR route was found in the accessible India/Pakistan XML layer.",
    "next_gate": "Try CISI 3.1, HARP, museum/archive sources, or non-OCR page-range routing.",
}

SKEPTIC_BOUNDARY = (
    "Visual route triage cannot validate source-normalized token order, physical direction, sign "
    "identity, meaning, phonetic value, language family, or translation."
)

FORGER_BOUNDARY = (
    "No forger pass has been run on visual admissibility tiers. These tiers only select candidates for "
    "the next blind token-boxing/control packet; accepted claims remain zero."
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    if not path.exists():
        return ""
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def review_for(row: dict[str, str]) -> dict[str, str]:
    rank = row["queue_rank"]
    if rank in MANUAL_REVIEWS:
        return MANUAL_REVIEWS[rank]
    status = row["source_status_rank"]
    if status == "public_cisi_plate_route_candidate":
        return DEFAULT_PLATE_REVIEW
    if status == "public_cisi_data_route_only":
        return DATA_ONLY_REVIEW
    return NOT_FOUND_REVIEW


def row_to_output(row: dict[str, str]) -> dict[str, str]:
    review = review_for(row)
    artifact = row.get("best_local_artifact", "")
    artifact_path = ROOT / artifact if artifact else None
    return {
        "date": RUN_DATE,
        "triage_id": TRIAGE_ID,
        "queue_rank": row["queue_rank"],
        "representative_cisi": row["representative_cisi"],
        "site": row["site"],
        "type": row["type"],
        "text": row["text"],
        "diff_per_transition": row["diff_per_transition"],
        "route_count": row["route_count"],
        "plate_route_count": row["plate_route_count"],
        "data_route_count": row["data_route_count"],
        "source_status_rank": row["source_status_rank"],
        "best_volume": row["best_volume"],
        "best_page_index": row["best_page_index"],
        "best_source_url": row["best_source_url"],
        "best_local_artifact": artifact,
        "best_artifact_sha256": sha256_file(artifact_path) if artifact_path else "",
        "visual_review_status": review["visual_review_status"],
        "admissibility_tier": review["admissibility_tier"],
        "signband_visible": review["signband_visible"],
        "immediate_blind_packet_candidate": review["immediate_blind_packet_candidate"],
        "manual_visual_note": review["manual_visual_note"],
        "next_gate": review["next_gate"],
        "skeptic_boundary": SKEPTIC_BOUNDARY,
        "forger_boundary": FORGER_BOUNDARY,
        "accepted_claims_increment": str(ACCEPTED_CLAIMS_INCREMENT),
    }


def fit_image(path: Path, width: int, height: int) -> Image.Image:
    image = Image.open(path).convert("RGB")
    image.thumbnail((width, height), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (width, height), "white")
    x = (width - image.width) // 2
    y = (height - image.height) // 2
    canvas.paste(image, (x, y))
    return canvas


def draw_multiline(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fill: str = "black") -> int:
    x, y = xy
    line_height = 18
    for line in wrap(text, width=58):
        draw.text((x, y), line, fill=fill)
        y += line_height
    return y


def make_contact_sheet(rows: list[dict[str, str]]) -> str:
    reviewed = [
        row
        for row in rows
        if row["queue_rank"] in MANUAL_REVIEWS and row["best_local_artifact"]
    ]
    if not reviewed:
        return ""

    tile_w = 760
    image_h = 440
    caption_h = 170
    cols = 2
    rows_needed = (len(reviewed) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tile_w, rows_needed * (image_h + caption_h)), "white")
    draw = ImageDraw.Draw(sheet)

    for index, row in enumerate(reviewed):
        x = (index % cols) * tile_w
        y = (index // cols) * (image_h + caption_h)
        artifact = ROOT / row["best_local_artifact"]
        if artifact.exists():
            image = fit_image(artifact, tile_w - 20, image_h - 20)
            sheet.paste(image, (x + 10, y + 10))
        draw.rectangle((x, y, x + tile_w - 1, y + image_h + caption_h - 1), outline="black")
        caption_y = y + image_h + 8
        title = (
            f"rank {row['queue_rank']} | {row['representative_cisi']} | "
            f"{row['visual_review_status']}"
        )
        draw.text((x + 12, caption_y), title, fill="black")
        caption_y += 22
        draw.text(
            (x + 12, caption_y),
            f"tier: {row['admissibility_tier']} | immediate: {row['immediate_blind_packet_candidate']}",
            fill="black",
        )
        caption_y += 22
        draw_multiline(draw, (x + 12, caption_y), row["manual_visual_note"])

    CONTACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    sheet = ImageOps.exif_transpose(sheet)
    sheet.save(CONTACT_SHEET, quality=92)
    return str(CONTACT_SHEET.relative_to(ROOT)).replace("\\", "/")


def main() -> None:
    source_rows = read_csv(STATUS_CSV)
    rows = [row_to_output(row) for row in source_rows]
    write_csv(OUT_CSV, rows)
    contact_sheet = make_contact_sheet(rows)

    by_tier = Counter(row["admissibility_tier"] for row in rows)
    by_review_status = Counter(row["visual_review_status"] for row in rows)
    immediate_candidates = [
        {
            "queue_rank": row["queue_rank"],
            "representative_cisi": row["representative_cisi"],
            "site": row["site"],
            "type": row["type"],
            "text": row["text"],
            "diff_per_transition": row["diff_per_transition"],
            "best_volume": row["best_volume"],
            "best_page_index": row["best_page_index"],
            "best_local_artifact": row["best_local_artifact"],
            "next_gate": row["next_gate"],
        }
        for row in rows
        if row["immediate_blind_packet_candidate"] == "yes"
    ]

    summary = {
        "date": RUN_DATE,
        "triage_id": TRIAGE_ID,
        "purpose": (
            "Manual visual admissibility triage for public CISI OCR route candidates feeding the "
            "effective-unicity directionality source-normalization queue."
        ),
        "inputs": {
            "status_csv": str(STATUS_CSV.relative_to(ROOT)).replace("\\", "/"),
        },
        "counts": {
            "target_rows": len(rows),
            "public_plate_route_candidates": sum(
                1 for row in rows if row["source_status_rank"] == "public_cisi_plate_route_candidate"
            ),
            "manually_visual_reviewed": len(MANUAL_REVIEWS),
            "immediate_blind_packet_candidates": len(immediate_candidates),
            "accepted_claims_increment": ACCEPTED_CLAIMS_INCREMENT,
        },
        "by_admissibility_tier": dict(sorted(by_tier.items())),
        "by_visual_review_status": dict(sorted(by_review_status.items())),
        "immediate_candidates": immediate_candidates,
        "interpretation_boundary": SKEPTIC_BOUNDARY,
        "forger_boundary": FORGER_BOUNDARY,
        "outputs": {
            "triage_csv": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
            "summary_json": str(OUT_JSON.relative_to(ROOT)).replace("\\", "/"),
            "reviewed_contact_sheet": contact_sheet,
        },
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["counts"], indent=2))


if __name__ == "__main__":
    main()
