"""Tokenization gate for the Harappa bands of H-1138 and H-360.

This script works on the stored Harappa source bands and tries to tokenize them —
split the visible band into separate sign-sized windows — with PIL enhancement and
explicit orientation policies (for right-to-left metadata, the visual rightmost sign
is catalog-first). The question: can the bands be tokenized well enough to test
whether the H-1138 catalog 603 matches the clean post-861 terminal on M-1273, while
the H-360 catalog 636 stays visually different? It writes gate CSVs, hashed crops
under tmp/032_002_861_603_h1138_h360_tokenization_gate, a summary JSON, and a docs/
markdown note. The recorded decision: cross-context 603 graphic identity stays
unresolved and negative-leaning; nothing is accepted.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps


ROOT = Path.cwd()
OUT = ROOT / "tmp" / "032_002_861_603_h1138_h360_tokenization_gate"
REPORTS = ROOT / "data" / "open_prototype" / "reports"
OUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)


SOURCES = [
    {
        "object": "H-1138",
        "expected_text": "+740-603-240-060-692+",
        "x_value": "603",
        "source": ROOT / "tmp/032_002_861_603_slot_source_normalization/H1138_Vats_Plate_XCIV_346_crop_tight.png",
        "source_note": "Vats Plate XCIV no.346 tight upper signband crop",
        "boxes": {
            "visual_slot_1_left": (46, 58, 91, 171),
            "visual_slot_2": (88, 58, 136, 171),
            "visual_slot_3": (132, 58, 184, 171),
            "visual_slot_4": (181, 58, 231, 171),
            "visual_slot_5_right": (226, 58, 286, 171),
        },
        "notes": "The far-left edge is clipped; five slots are approximate visual units, not accepted sign boundaries.",
    },
    {
        "object": "H-360",
        "expected_text": "+740-636-240-060-692+",
        "x_value": "636",
        "source": ROOT / "tmp/032_002_861_603_slot_source_normalization/H360_Vats_Plate_XCVIII_584_signband_crop.png",
        "source_note": "Vats Plate XCVIII no.584 signband crop",
        "boxes": {
            "visual_slot_1_left": (245, 78, 319, 149),
            "visual_slot_2": (318, 78, 390, 149),
            "visual_slot_3": (390, 78, 458, 149),
            "visual_slot_4": (458, 78, 524, 149),
            "visual_slot_5_right": (524, 78, 599, 149),
        },
        "notes": "The central 5-sign band is cropped from a wider row; boundaries are approximate visual units.",
    },
]

POST861_ANCHOR = {
    "object": "M-1273",
    "role": "post861_clean_603_anchor",
    "expected_text": "+740-055-002-861-603+",
    "source": ROOT / "tmp/032_002_861_603_graphic_identity_packet/M1273_post861_tail_window.png",
    "source_note": "CISI Pakistan n195 terminal candidate window from prior graphic-identity packet",
}


def font(size: int):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def enhanced(im: Image.Image) -> Image.Image:
    gray = ImageOps.grayscale(im)
    gray = ImageEnhance.Contrast(gray).enhance(1.8)
    gray = ImageEnhance.Sharpness(gray).enhance(2.0)
    return ImageOps.colorize(gray, black="black", white="white").convert("RGB")


def crop_box(source: Path, box: tuple[int, int, int, int], out: Path, scale: int = 4) -> tuple[int, int]:
    with Image.open(source) as im:
        im = im.convert("RGB")
        region = im.crop(box)
        region = enhanced(region)
        region = region.resize((region.width * scale, region.height * scale))
        region.save(out)
        return region.size


def draw_annotated_source(row: dict[str, object]) -> Path:
    source = Path(row["source"])
    with Image.open(source) as im:
        im = enhanced(im.convert("RGB"))
        scale = 3
        im = im.resize((im.width * scale, im.height * scale))
        pad = 58
        canvas = Image.new("RGB", (im.width, im.height + pad), "white")
        canvas.paste(im, (0, pad))
        draw = ImageDraw.Draw(canvas)
        draw.text((8, 8), f"{row['object']} candidate visual slots", fill=(0, 0, 0), font=font(22))
        draw.text((8, 34), "candidate boxes only; not accepted source tokenization", fill=(80, 80, 80), font=font(14))
        colors = [(220, 40, 40), (30, 120, 220), (20, 150, 70), (180, 100, 20), (135, 60, 190)]
        for idx, (slot, box) in enumerate(row["boxes"].items(), start=1):
            x1, y1, x2, y2 = box
            shifted = (x1 * scale, y1 * scale + pad, x2 * scale, y2 * scale + pad)
            color = colors[(idx - 1) % len(colors)]
            draw.rectangle(shifted, outline=color, width=5)
            draw.text((x1 * scale + 4, y1 * scale + pad - 22), str(idx), fill=color, font=font(22))
        out = OUT / f"{str(row['object']).replace('-', '')}_candidate_slots_annotated.png"
        canvas.save(out)
        return out


def make_manifest() -> tuple[list[dict[str, object]], list[Path]]:
    rows: list[dict[str, object]] = []
    images: list[Path] = []

    for source_row in SOURCES:
        annotated = draw_annotated_source(source_row)
        images.append(annotated)
        source = Path(source_row["source"])
        for idx, (slot, box) in enumerate(source_row["boxes"].items(), start=1):
            out = OUT / f"{str(source_row['object']).replace('-', '')}_{slot}.png"
            width, height = crop_box(source, box, out)

            # Both orientation policies are explicit. For R/L metadata, visual rightmost is catalog first.
            ltr_tokens = source_row["expected_text"].strip("+").split("-")
            rtl_tokens = list(reversed(ltr_tokens))
            ltr_token = ltr_tokens[idx - 1]
            rtl_token = rtl_tokens[idx - 1]
            rows.append(
                {
                    "object": source_row["object"],
                    "expected_text": source_row["expected_text"],
                    "x_value": source_row["x_value"],
                    "slot": slot,
                    "visual_position_left_to_right": idx,
                    "source_path": str(source),
                    "source_sha256": sha256(source),
                    "crop_path": str(out),
                    "crop_width": width,
                    "crop_height": height,
                    "candidate_token_if_visual_ltr_equals_catalog_order": ltr_token,
                    "candidate_token_if_recorded_RL_means_visual_rightmost_catalog_first": rtl_token,
                    "is_x_slot_under_ltr_policy": str(ltr_token == source_row["x_value"]).lower(),
                    "is_x_slot_under_rl_policy": str(rtl_token == source_row["x_value"]).lower(),
                    "source_note": source_row["source_note"],
                    "status": "candidate_visual_slot_not_accepted_token_box",
                    "notes": source_row["notes"],
                }
            )
            images.append(out)

    anchor_source = Path(POST861_ANCHOR["source"])
    anchor_out = OUT / "M1273_post861_clean_603_anchor_enhanced.png"
    with Image.open(anchor_source) as im:
        im = enhanced(im.convert("RGB"))
        im = im.resize((im.width * 2, im.height * 2))
        im.save(anchor_out)
    rows.append(
        {
            "object": POST861_ANCHOR["object"],
            "expected_text": POST861_ANCHOR["expected_text"],
            "x_value": "603",
            "slot": POST861_ANCHOR["role"],
            "visual_position_left_to_right": "",
            "source_path": str(anchor_source),
            "source_sha256": sha256(anchor_source),
            "crop_path": str(anchor_out),
            "crop_width": im.width,
            "crop_height": im.height,
            "candidate_token_if_visual_ltr_equals_catalog_order": "603",
            "candidate_token_if_recorded_RL_means_visual_rightmost_catalog_first": "603",
            "is_x_slot_under_ltr_policy": "true",
            "is_x_slot_under_rl_policy": "true",
            "source_note": POST861_ANCHOR["source_note"],
            "status": "post861_anchor_from_prior_packet",
            "notes": "Cleanest available post-861 terminal 603 anchor.",
        }
    )
    images.append(anchor_out)
    return rows, images


def tile_for(path: Path, label: str, size: tuple[int, int] = (360, 310)) -> Image.Image:
    im = Image.open(path).convert("RGB")
    im.thumbnail((size[0] - 24, size[1] - 62))
    tile = Image.new("RGB", size, "white")
    tile.paste(im, (12, 50))
    draw = ImageDraw.Draw(tile)
    draw.text((10, 8), label[:42], fill=(0, 0, 0), font=font(16))
    return tile


def make_sheets(rows: list[dict[str, object]], images: list[Path]) -> tuple[Path, Path]:
    annotated = [p for p in images if p.name.endswith("_annotated.png")]
    crops = [Path(str(row["crop_path"])) for row in rows]

    tiles = [tile_for(p, p.stem, (620, 430)) for p in annotated]
    sheet = Image.new("RGB", (660, 20 + len(tiles) * 440), "white")
    y = 10
    for tile in tiles:
        sheet.paste(tile, (20, y))
        y += 440
    annotated_out = OUT / "h1138_h360_candidate_slots_annotated_sheet.png"
    sheet.save(annotated_out)

    crop_tiles = [tile_for(p, p.stem, (260, 265)) for p in crops]
    cols = 4
    crop_sheet = Image.new("RGB", (cols * 260 + 20, ((len(crop_tiles) + cols - 1) // cols) * 265 + 20), "white")
    for idx, tile in enumerate(crop_tiles):
        crop_sheet.paste(tile, (10 + (idx % cols) * 260, 10 + (idx // cols) * 265))
    crop_out = OUT / "h1138_h360_m1273_candidate_crop_sheet.png"
    crop_sheet.save(crop_out)
    return annotated_out, crop_out


def write_doc(rows: list[dict[str, object]], annotated: Path, crop_sheet: Path) -> Path:
    doc = ROOT / "docs" / "campaign_032_002_861_603_h1138_h360_tokenization_gate.md"
    manifest = REPORTS / "campaign_032_002_861_603_h1138_h360_tokenization_gate_manifest.csv"
    h1138_x_ltr = [r for r in rows if r["object"] == "H-1138" and r["is_x_slot_under_ltr_policy"] == "true"]
    h1138_x_rl = [r for r in rows if r["object"] == "H-1138" and r["is_x_slot_under_rl_policy"] == "true"]
    h360_x_ltr = [r for r in rows if r["object"] == "H-360" and r["is_x_slot_under_ltr_policy"] == "true"]
    h360_x_rl = [r for r in rows if r["object"] == "H-360" and r["is_x_slot_under_rl_policy"] == "true"]
    lines = [
        "# 032-002-861 603 H-1138/H-360 Tokenization Gate",
        "",
        "Date: 2026-05-29",
        "",
        "## Question",
        "",
        "Can the source-visible Harappa bands be tokenized enough to test whether `H-1138` catalog `603` matches the clean post-`861` `M-1273` terminal, while `H-360` catalog `636` stays visually different?",
        "",
        "This is a candidate tokenization gate. It does not accept a source-derived sign value or translation.",
        "",
        "## Artifacts",
        "",
        f"- Candidate slot sheet: `{annotated.relative_to(ROOT)}`",
        f"- Candidate crop sheet: `{crop_sheet.relative_to(ROOT)}`",
        f"- Manifest: `{manifest.relative_to(ROOT)}`",
        "",
        "## Orientation Alternatives",
        "",
        "Both source rows are locally recorded as `R/L`. Therefore two policies are kept explicit:",
        "",
        "1. `visual_ltr_equals_catalog_order`: leftmost visual slot maps to the first catalog token.",
        "2. `recorded_RL_means_visual_rightmost_catalog_first`: rightmost visual slot maps to the first catalog token.",
        "",
        "Candidate X slots under these policies:",
        "",
        f"- `H-1138` / `603` under visual-LTR: {[r['slot'] for r in h1138_x_ltr]}",
        f"- `H-1138` / `603` under recorded-R/L: {[r['slot'] for r in h1138_x_rl]}",
        f"- `H-360` / `636` under visual-LTR: {[r['slot'] for r in h360_x_ltr]}",
        f"- `H-360` / `636` under recorded-R/L: {[r['slot'] for r in h360_x_rl]}",
        "",
        "## Immediate Visual Read",
        "",
        "Under the recorded-R/L policy, the candidate Harappa `603` in `H-1138` falls in visual slot 4, while the `H-360` `636` control falls in visual slot 4. Both are visibly different from the clean ladder/window-like `M-1273` terminal anchor in the current crop sheet. Under the visual-LTR policy, the candidate X slots fall in visual slot 2, which also does not cleanly match `M-1273`.",
        "",
        "The key point is not that the bridge is disproven. The key point is that this public Vats crop quality and approximate slotting do not deliver the positive upgrade. The current source-tokenization gate does not prove `M-1273 terminal sign = H-1138 source-tokenized 603`.",
        "",
        "## Decision",
        "",
        "```text",
        "h1138_h360_source_tokenization = candidate_only",
        "m1273_equals_h1138_603 = not_demonstrated",
        "h360_636_distinct_from_m1273 = plausible_but_candidate_only",
        "cross_context_603_graphic_identity = unresolved_negative_leaning",
        "```",
        "",
        "## Researcher Review",
        "",
        "Source-critical verdict:",
        "",
        "- The positive test fails to upgrade. `M-1273` remains a clean ladder/window-like post-`861` terminal anchor, but neither candidate `H-1138` X-slot cleanly matches it under the current public crop.",
        "- The packet does not overstate the boxes: it keeps them as candidate visual slots and preserves both orientation policies.",
        "",
        "Linguistic update:",
        "",
        "- The distributional bridge is unchanged: `603` still bridges the Harappa X-before-`240` class and post-`002-861` terminal position while `636/642` do not.",
        "- The graphic bridge is weakened: candidate `H-1138` X under both orientation policies fails to confirm the `M-1273` match.",
        "- Split-homograph/catalog-conflation and Harappa tablet-template explanations are now promoted as live competitors.",
        "",
        "Allowed hostile claim:",
        "",
        "```text",
        "603 is a distributional bridge with unresolved/negative-leaning graphic identity.",
        "```",
        "",
        "Not allowed:",
        "",
        "- No final graphic kill.",
        "- No value, phonetics, language identity, or translation.",
        "- No accepted Harappa-to-Mohenjo graphic identity.",
        "",
        "Reason: `H-1138` boxes are approximate, the far-left edge is clipped, orientation is not source-settled, public Vats quality is weak, and `H-1846` is still not layout-ready.",
        "",
        "## Next Test",
        "",
        "The bridge needs a better source image or a label-bearing source transcription for `H-1138/H-1846`. Without that, `603` remains a distributional bridge and a post-`861` terminal candidate, not a source-proven Harappa-to-Mohenjo graphic identity.",
        "",
        "Accepted values/translations remain 0.",
    ]
    doc.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return doc


def main() -> None:
    rows, images = make_manifest()
    manifest = REPORTS / "campaign_032_002_861_603_h1138_h360_tokenization_gate_manifest.csv"
    with manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    annotated, crop_sheet = make_sheets(rows, images)
    doc = write_doc(rows, annotated, crop_sheet)
    summary = {
        "date": "2026-05-29",
        "campaign": "032-002-861 603 H-1138/H-360 tokenization gate",
        "manifest_rows": len(rows),
        "decision": "cross_context_603_graphic_identity_unresolved_negative_leaning",
        "bridge_status": "distributional_alive_graphically_weakened",
        "positive_upgrade": "not_demonstrated",
        "annotated_sheet": str(annotated.resolve()),
        "crop_sheet": str(crop_sheet.resolve()),
        "manifest_csv": str(manifest.resolve()),
        "doc": str(doc.resolve()),
        "not_accepted": ["603 value", "phonetic reading", "language identity", "translation"],
    }
    summary_path = REPORTS / "campaign_032_002_861_603_h1138_h360_tokenization_gate_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
