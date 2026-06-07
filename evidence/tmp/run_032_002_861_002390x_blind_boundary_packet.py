from __future__ import annotations

import csv
import json
import random
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "data" / "open_prototype" / "reports"
DOC_DIR = ROOT / "docs"
ART_DIR = ROOT / "tmp" / "blind_boundary_packet_alpha"
PANEL_DIR = ART_DIR / "blind_panels"
OVERLAY_DIR = ART_DIR / "neutral_overlay_key"
PREFIX = "blind_boundary_packet_alpha"
DATE = "2026-05-30"
SEED = 20260530
NEUTRAL_IDS = ["ALPHA", "BRAVO", "CHARLIE", "DELTA", "ECHO"]


@dataclass(frozen=True)
class Witness:
    object_key: str
    role: str
    branch: str
    local_text: str
    source_crop: Path
    source_route: str
    local_window: str
    window_box: tuple[int, int, int, int]
    token_windows: tuple[tuple[int, int], ...]
    current_status: str
    why_in_packet: str


WITNESSES = [
    Witness(
        object_key="M-119",
        role="strict_125_target",
        branch="125",
        local_text="+151-337-484-002-390-125-632-032-900-563+",
        source_crop=ROOT / "tmp" / "002390x_source_normalization" / "M119_face_A_signband.jpg",
        source_route="CISI India/Pakistan public panel crop, face A",
        local_window="positions 4-6 = 002-390-125",
        window_box=(165, 15, 380, 160),
        token_windows=((165, 225), (225, 300), (300, 380)),
        current_status="strict source-visible target, boxed-window-compatible",
        why_in_packet="cleanest target-side test for whether the local 002-390-125 window survives without labels",
    ),
    Witness(
        object_key="M-735",
        role="strict_125_target",
        branch="125",
        local_text="+740-760-235-002-390-125-195+",
        source_crop=ROOT / "tmp" / "002390x_source_normalization" / "M735_impression_a_signband.jpg",
        source_route="CISI Pakistan public panel crop, impression a",
        local_window="positions 4-6 = 002-390-125",
        window_box=(245, 15, 845, 250),
        token_windows=((245, 410), (410, 535), (535, 690), (690, 845)),
        current_status="strict source-visible target, boxed-window-compatible but crowded",
        why_in_packet="independence pressure for the target side; should fail if the crowded band only works with catalog priming",
    ),
    Witness(
        object_key="M-70",
        role="strict_non125_control",
        branch="692",
        local_text="+226-032-002-390-692+",
        source_crop=ROOT
        / "tmp"
        / "032_002_branch_tail_source_acquisition"
        / "M70_impression_a_signband_from_cisi_india_n066.png",
        source_route="CISI India public panel n066, impression a",
        local_window="positions 3-5 = 002-390-692",
        window_box=(300, 5, 900, 190),
        token_windows=((300, 455), (455, 650), (650, 900)),
        current_status="strict source-visible non-125 control, boxed-window-compatible",
        why_in_packet="tests whether the same local opener has a visually real non-target branch",
    ),
    Witness(
        object_key="M-71",
        role="strict_non125_control",
        branch="095",
        local_text="+151-279-142-002-390-095+",
        source_crop=ROOT / "tmp" / "002390x_source_normalization" / "M71_impression_a_signband.jpg",
        source_route="CISI India/Pakistan public panel crop, impression a",
        local_window="positions 4-6 = 002-390-095",
        window_box=(300, 5, 680, 250),
        token_windows=((300, 410), (410, 540), (540, 680)),
        current_status="strict source-visible non-125 control, boxed-window-compatible",
        why_in_packet="second non-target branch; important because H-1993 is still source-dark",
    ),
    Witness(
        object_key="Sktd-1",
        role="downweighted_125_candidate",
        branch="125",
        local_text="+390-004-002-390-125-820+",
        source_crop=ROOT / "tmp" / "002390x_source_normalization" / "Sktd1_impression_a_signband.jpg",
        source_route="public panel-bound crop, impression a",
        local_window="positions 3-5 = 002-390-125",
        window_box=(140, 10, 530, 190),
        token_windows=((140, 260), (260, 390), (390, 530)),
        current_status="downweighted candidate, boxed-window-compatible only",
        why_in_packet="tests whether the weaker candidate is independently segmentable or should stay out of strict counts",
    ),
]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def neutralize_panel(source: Path, neutral_id: str) -> Path:
    img = Image.open(source).convert("RGB")
    out = Image.new("RGB", (img.width, img.height + 42), "white")
    out.paste(img, (0, 42))
    draw = ImageDraw.Draw(out)
    draw.rectangle((0, 0, out.width, 41), fill=(245, 245, 245), outline=(190, 190, 190))
    draw.text((12, 10), neutral_id, fill=(0, 0, 0), font=font(20))
    path = PANEL_DIR / f"{neutral_id}.jpg"
    path.parent.mkdir(parents=True, exist_ok=True)
    out.save(path, quality=94)
    return path


def make_blind_sheet(rows: list[dict[str, object]]) -> Path:
    tile_w = 980
    label_h = 70
    gap = 16
    tiles: list[tuple[str, Image.Image]] = []
    for row in rows:
        path = Path(str(row["blind_panel_path"]))
        img = Image.open(path).convert("RGB")
        img.thumbnail((tile_w - 24, 260))
        tiles.append((str(row["neutral_id"]), img))

    total_h = sum(img.height + label_h + gap for _, img in tiles) + gap
    sheet = Image.new("RGB", (tile_w, total_h), "white")
    draw = ImageDraw.Draw(sheet)
    y = gap
    for neutral_id, img in tiles:
        draw.rectangle((0, y, tile_w, y + img.height + label_h), fill=(255, 255, 255), outline=(210, 210, 210))
        draw.text((16, y + 10), neutral_id, fill=(0, 0, 0), font=font(22))
        draw.text(
            (120, y + 13),
            "Segment visible marks and record boundaries. No object labels or expected labels are supplied.",
            fill=(50, 50, 50),
            font=font(16),
        )
        sheet.paste(img, (12, y + label_h))
        y += img.height + label_h + gap

    path = ART_DIR / f"{PREFIX}_blind_sheet.jpg"
    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, quality=94)
    return path


def make_neutral_overlay(w: Witness, neutral_id: str) -> Path:
    img = Image.open(w.source_crop).convert("RGB")
    draw = ImageDraw.Draw(img, "RGBA")
    left, top, right, bottom = w.window_box
    draw.rectangle((left, top, right, bottom), outline=(255, 0, 0, 255), width=4)
    colors = [(0, 120, 255, 95), (0, 180, 85, 95), (255, 180, 0, 95), (160, 80, 255, 95)]
    for idx, (a, b) in enumerate(w.token_windows):
        color = colors[idx % len(colors)]
        draw.rectangle((a, top, b, bottom), outline=color[:3] + (255,), fill=color, width=2)
    draw.rectangle((0, 0, min(img.width, 190), 34), fill=(255, 255, 255, 230))
    draw.text((8, 7), neutral_id, fill=(0, 0, 0), font=font(20))
    path = OVERLAY_DIR / f"{neutral_id}_overlay.jpg"
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, quality=94)
    return path


def main() -> None:
    missing = [str(w.source_crop) for w in WITNESSES if not w.source_crop.exists()]
    if missing:
        raise FileNotFoundError("Missing source crops: " + "; ".join(missing))

    shuffled = list(WITNESSES)
    random.Random(SEED).shuffle(shuffled)
    neutral_rows: list[dict[str, object]] = []
    key_rows: list[dict[str, object]] = []
    response_rows: list[dict[str, object]] = []
    overlay_rows: list[dict[str, object]] = []

    for idx, w in enumerate(shuffled, start=1):
        neutral_id = NEUTRAL_IDS[idx - 1]
        panel_path = neutralize_panel(w.source_crop, neutral_id)
        overlay_path = make_neutral_overlay(w, neutral_id)
        neutral_rows.append(
            {
                "neutral_id": neutral_id,
                "blind_panel_path": str(panel_path),
                "sheet_order": idx,
                "leakage_policy": "neutral_id_only_no_object_or_sign_labels",
            }
        )
        response_rows.append(
            {
                "neutral_id": neutral_id,
                "visible_mark_count": "",
                "preferred_direction_if_any": "",
                "boundary_sequence_left_to_right": "",
                "boundary_sequence_right_to_left": "",
                "candidate_repeated_cluster_ids": "",
                "confidence_0_to_3": "",
                "reject_reason_if_unsegmentable": "",
                "free_notes": "",
            }
        )
        key_rows.append(
            {
                "neutral_id": neutral_id,
                "object_key": w.object_key,
                "role": w.role,
                "branch": w.branch,
                "local_text": w.local_text,
                "source_crop": str(w.source_crop),
                "source_route": w.source_route,
                "local_window": w.local_window,
                "window_box": " ".join(map(str, w.window_box)),
                "token_windows": "; ".join(f"{a}-{b}" for a, b in w.token_windows),
                "current_status": w.current_status,
                "why_in_packet": w.why_in_packet,
                "blind_panel_path": str(panel_path),
                "neutral_overlay_path": str(overlay_path),
            }
        )
        overlay_rows.append(
            {
                "neutral_id": neutral_id,
                "neutral_overlay_path": str(overlay_path),
                "overlay_policy": "neutral_id_only; object IDs and sign labels remain in separate key CSV",
            }
        )

    blind_sheet = make_blind_sheet(neutral_rows)
    write_csv(REPORT_DIR / f"{PREFIX}_blind_manifest.csv", neutral_rows)
    write_csv(REPORT_DIR / f"{PREFIX}_response_form.csv", response_rows)
    write_csv(REPORT_DIR / f"{PREFIX}_sealed_key.csv", key_rows)
    write_csv(REPORT_DIR / f"{PREFIX}_neutral_overlay_manifest.csv", overlay_rows)

    summary = {
        "date": DATE,
        "seed": SEED,
        "neutral_count": len(neutral_rows),
        "blind_sheet": str(blind_sheet),
        "blind_manifest": str(REPORT_DIR / f"{PREFIX}_blind_manifest.csv"),
        "response_form": str(REPORT_DIR / f"{PREFIX}_response_form.csv"),
        "sealed_key": str(REPORT_DIR / f"{PREFIX}_sealed_key.csv"),
        "neutral_overlay_manifest": str(REPORT_DIR / f"{PREFIX}_neutral_overlay_manifest.csv"),
        "visible_label_policy": "blind panels and blind sheet contain neutral IDs only",
        "claim_policy": "packet is for adjudication only; it does not accept value, translation, phonetic reading, sign function, or language identity",
    }
    (REPORT_DIR / f"{PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    doc = dedent(
        f"""
        # 032-002-861 / 002-390-X Blind Boundary Packet

        Date: {DATE}

        ## Purpose

        This packet tests whether the visible sign-band segmentation survives without object IDs, target/control labels, or expected sign numbers. It is an adjudication packet, not a decipherment result.

        ## Blind Materials

        - Blind sheet: `{blind_sheet}`
        - Blind manifest: `{REPORT_DIR / f"{PREFIX}_blind_manifest.csv"}`
        - Response form: `{REPORT_DIR / f"{PREFIX}_response_form.csv"}`

        The blind sheet and individual blind panels expose only neutral IDs. Readers should segment the visible marks, record boundaries in both left-to-right and right-to-left descriptions if needed, mark repeated visual clusters across panels, and reject panels that cannot be segmented.

        ## Separated Key

        - Sealed key: `{REPORT_DIR / f"{PREFIX}_sealed_key.csv"}`
        - Neutral overlay manifest: `{REPORT_DIR / f"{PREFIX}_neutral_overlay_manifest.csv"}`
        - Neutral overlays directory: `{OVERLAY_DIR}`

        The overlays preserve neutral IDs only. Object IDs, local texts, branch labels, and roles are stored only in the sealed key CSV.

        ## Decision Rule

        The `125` branch only survives this gate if blind readers independently recover a plausible local segmentation for the two strict target panels and do not collapse the non-target controls into the same visual outcome. If the strict panels require object labels, expected sign numbers, or catalog order to become readable, then this packet demotes the visual side of the `125` branch claim.

        ## Current Status

        No value, phonetic reading, sign meaning, language identity, or translation is accepted. The packet exists to force a blind boundary decision before the campaign treats `002-390-X` as stronger than boxed-window-compatible.
        """
    ).strip()
    (DOC_DIR / f"{PREFIX}.md").write_text(doc + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
