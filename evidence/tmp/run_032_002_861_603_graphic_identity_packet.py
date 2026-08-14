"""Graphic-identity packet for sign 603 across two different contexts.

Catalog transcriptions can call two different-looking marks by the same number, so
"graphic identity" — same actual drawn shape — has to be checked on images. This
script carries an inline list of source bands: the source-visible post-002-861 603
windows and the Harappa 740-603-240-060-692 bands. With PIL it cuts each band into
deliberately equal-width visual slices (explicitly not accepted token boxes), hashes
the images, and assembles a comparison packet under
tmp/032_002_861_603_graphic_identity_packet. It writes packet CSVs, a summary JSON,
and a docs/ markdown note. The recorded decision: cross-context 603 graphic identity
is unresolved — the bridge between the two contexts is still catalog-mediated.
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path.cwd()
OUT = ROOT / "tmp" / "032_002_861_603_graphic_identity_packet"
REPORTS = ROOT / "data" / "open_prototype" / "reports"
OUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)


POST861 = [
    {
        "item_id": "M240_post861_tail_window",
        "object": "M-240",
        "role": "post861_603_tail_candidate_window",
        "text": "+520-240-220-032-002-861-603+",
        "source": ROOT / "tmp/032_002_branch_tail_source_acquisition/M240_impression_a_signband_from_cisi_india_n095.png",
        "box": (635, 20, 755, 250),
        "source_note": "CISI India IA leaf n95 / printed p.60; existing source-token attachment tail window.",
        "token_assignment": "catalog_mediated_tail_window_not_exact_box",
        "quality": "medium",
        "notes": "Terminal-side window is visually separated but blurred and narrow.",
    },
    {
        "item_id": "M714_post861_terminal_broad_rescue_window",
        "object": "M-714",
        "role": "post861_603_terminal_broad_rescue_window",
        "text": "+740-585-017-033-705-233-798-803-002-861-603+",
        "source": ROOT / "tmp/032_002_861_suffix_split/M714_impression_a_cisi_pakistan_n079.png",
        "box": (1060, 0, 1185, 235),
        "source_note": "CISI Pakistan IA leaf n79 / printed p.45; broad rescue crop because the earlier attachment tail window split the terminal graphic.",
        "token_assignment": "broad_terminal_region_not_exact_box",
        "quality": "low_for_identity",
        "notes": "Crowded row; this broad region preserves the likely terminal ladder-like graphic but is not an exact 861/603 boundary.",
    },
    {
        "item_id": "M1273_post861_tail_window",
        "object": "M-1273",
        "role": "post861_603_tail_candidate_window",
        "text": "+740-055-002-861-603+",
        "source": ROOT / "tmp/032_002_861_suffix_split/M1273_impression_a_cisi_pakistan_n195.png",
        "box": (1010, 55, 1230, 430),
        "source_note": "CISI Pakistan IA leaf n195 / printed p.161; existing source-token attachment tail window.",
        "token_assignment": "catalog_mediated_tail_window_not_exact_box",
        "quality": "high",
        "notes": "Strongest public source witness for the post-861 603 tail window.",
    },
]


SOURCE_BANDS = [
    {
        "object": "H-1138",
        "role": "harappa_603_source_band_unassigned",
        "text": "+740-603-240-060-692+",
        "source": ROOT / "tmp/032_002_861_603_slot_source_normalization/H1138_Vats_Plate_XCIV_346_crop_tight.png",
        "source_note": "Vats Plate XCIV no.346 tight upper signband crop.",
        "quality": "medium_low",
        "slice_count": 5,
        "slice_box": (0, 55, 290, 165),
        "notes": "Source-visible band, but local five-sign sequence has not been retokenized from the image.",
    },
    {
        "object": "H-1846",
        "role": "harappa_603_source_context_unassigned",
        "text": "+740-603-240-060-692+",
        "source": ROOT / "tmp/032_002_861_603_slot_source_normalization/H1846_H95_2672_Figure11_11_crop_v3.png",
        "source_note": "Kenoyer and Meadow 1997 Figure 11.11 / H95-2672 crop.",
        "quality": "object_visible_layout_not_ready",
        "slice_count": 0,
        "slice_box": None,
        "notes": "Useful as object/panel visibility only in this packet; not enough for a source-derived 603 crop.",
    },
    {
        "object": "H-360",
        "role": "harappa_636_source_band_control_unassigned",
        "text": "+740-636-240-060-692+",
        "source": ROOT / "tmp/032_002_861_603_slot_source_normalization/H360_Vats_Plate_XCVIII_584_signband_crop.png",
        "source_note": "Vats Plate XCVIII no.584 signband crop.",
        "quality": "low_medium",
        "slice_count": 5,
        "slice_box": (0, 80, 600, 150),
        "notes": "Source-visible 636 control band; local sequence has not been retokenized from the image.",
    },
]


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


def crop(path: Path, box: tuple[int, int, int, int], out: Path) -> tuple[int, int]:
    with Image.open(path) as im:
        im = im.convert("RGB")
        x1, y1, x2, y2 = box
        x1 = max(0, min(im.width, x1))
        x2 = max(0, min(im.width, x2))
        y1 = max(0, min(im.height, y1))
        y2 = max(0, min(im.height, y2))
        region = im.crop((x1, y1, x2, y2))
        region.save(out)
        return region.size


def copy_context(path: Path, out: Path, max_width: int = 760) -> tuple[int, int]:
    with Image.open(path) as im:
        im = im.convert("RGB")
        if im.width > max_width:
            h = int(im.height * (max_width / im.width))
            im = im.resize((max_width, h))
        im.save(out)
        return im.size


def make_slices(row: dict[str, object], manifest: list[dict[str, object]]) -> None:
    source = Path(row["source"])
    object_id = str(row["object"]).replace("-", "")
    role = str(row["role"])
    with Image.open(source) as im:
        im = im.convert("RGB")
        full_out = OUT / f"{object_id}_{role}_full_band.png"
        im.save(full_out)
        manifest.append(
            {
                "item_id": full_out.stem,
                "object": row["object"],
                "role": role,
                "text": row["text"],
                "source_path": str(source),
                "source_sha256": sha256(source),
                "crop_path": str(full_out),
                "crop_width": im.width,
                "crop_height": im.height,
                "source_note": row["source_note"],
                "token_assignment": "none_source_band_only",
                "quality": row["quality"],
                "notes": row["notes"],
            }
        )

        slice_count = int(row["slice_count"])
        if slice_count <= 0:
            return

        slice_box = row.get("slice_box")
        slice_image = im
        if slice_box:
            sx1, sy1, sx2, sy2 = slice_box
            slice_image = im.crop((sx1, sy1, sx2, sy2))

        # These are deliberately equal-width visual slices, not accepted token boxes.
        for idx in range(slice_count):
            x1 = round(slice_image.width * idx / slice_count)
            x2 = round(slice_image.width * (idx + 1) / slice_count)
            out = OUT / f"{object_id}_{role}_visual_slice_{idx + 1:02d}.png"
            slice_image.crop((x1, 0, x2, slice_image.height)).save(out)
            manifest.append(
                {
                    "item_id": out.stem,
                    "object": row["object"],
                    "role": f"{role}_visual_slice",
                    "text": row["text"],
                    "source_path": str(source),
                    "source_sha256": sha256(source),
                    "crop_path": str(out),
                    "crop_width": x2 - x1,
                    "crop_height": slice_image.height,
                    "source_note": row["source_note"],
                    "token_assignment": "rough_equal_width_slice_not_token_identity",
                    "quality": row["quality"],
                    "notes": "Orientation and token assignment are not accepted; slice is for visual comparison only.",
                }
            )


def make_contact_sheet(manifest: list[dict[str, object]]) -> Path:
    title_font = font(22)
    label_font = font(15)
    rows = []
    for item in manifest:
        if item["role"].endswith("_visual_slice"):
            continue
        path = Path(str(item["crop_path"]))
        im = Image.open(path).convert("RGB")
        im.thumbnail((420, 220))
        tile = Image.new("RGB", (470, 290), "white")
        tile.paste(im, (20, 54))
        draw = ImageDraw.Draw(tile)
        draw.text((12, 8), str(item["object"]), fill=(0, 0, 0), font=title_font)
        draw.text((12, 34), str(item["role"])[:55], fill=(70, 70, 70), font=label_font)
        rows.append(tile)

    cols = 2
    width = cols * 470 + 30
    height = ((len(rows) + cols - 1) // cols) * 290 + 30
    sheet = Image.new("RGB", (width, height), "white")
    for idx, tile in enumerate(rows):
        x = 15 + (idx % cols) * 470
        y = 15 + (idx // cols) * 290
        sheet.paste(tile, (x, y))
    out = OUT / "032_002_861_603_graphic_identity_contact_sheet.png"
    sheet.save(out)
    return out


def make_slice_sheet(manifest: list[dict[str, object]]) -> Path:
    title_font = font(18)
    label_font = font(13)
    slice_items = [item for item in manifest if str(item["role"]).endswith("_visual_slice")]
    tiles = []
    for item in slice_items:
        path = Path(str(item["crop_path"]))
        im = Image.open(path).convert("RGB")
        im.thumbnail((150, 190))
        tile = Image.new("RGB", (190, 245), "white")
        tile.paste(im, (20, 44))
        draw = ImageDraw.Draw(tile)
        label = str(item["item_id"]).split("_visual_slice_")[-1]
        draw.text((10, 8), str(item["object"]), fill=(0, 0, 0), font=title_font)
        draw.text((10, 29), f"visual slice {label}", fill=(70, 70, 70), font=label_font)
        tiles.append(tile)

    cols = 5
    width = cols * 190 + 20
    height = ((len(tiles) + cols - 1) // cols) * 245 + 20
    sheet = Image.new("RGB", (width, height), "white")
    for idx, tile in enumerate(tiles):
        x = 10 + (idx % cols) * 190
        y = 10 + (idx // cols) * 245
        sheet.paste(tile, (x, y))
    out = OUT / "032_002_861_603_graphic_identity_slice_sheet.png"
    sheet.save(out)
    return out


def write_doc(manifest: list[dict[str, object]], contact: Path, slices: Path) -> Path:
    doc = ROOT / "docs" / "campaign_032_002_861_603_graphic_identity_packet.md"
    rows_csv = REPORTS / "campaign_032_002_861_603_graphic_identity_packet_manifest.csv"
    summary_json = REPORTS / "campaign_032_002_861_603_graphic_identity_packet_summary.json"
    lines = [
        "# 032-002-861 603 Graphic Identity Packet",
        "",
        "Date: 2026-05-29",
        "",
        "## Question",
        "",
        "Do the source-visible post-`002-861` `603` windows and the Harappa `740-603-240-060-692` source bands currently support the same graphic sign, or is the bridge still catalog-mediated?",
        "",
        "This packet is visual source comparison. It is not a sign value, phonetic reading, language identity claim, or translation.",
        "",
        "## Packet",
        "",
        f"- Contact sheet: `{contact.relative_to(ROOT)}`",
        f"- Rough visual slice sheet: `{slices.relative_to(ROOT)}`",
        f"- Manifest: `{rows_csv.relative_to(ROOT)}`",
        "",
        "Included source-visible post-`861` tail windows:",
        "",
        "- `M-240`: medium-quality terminal-side `603` candidate window.",
        "- `M-714`: low-confidence broad rescue terminal region because the previous tail window split the terminal graphic.",
        "- `M-1273`: strongest public terminal-side `603` candidate window.",
        "",
        "Included Harappa source bands:",
        "",
        "- `H-1138`: Vats Plate XCIV no.346 source-visible five-sign band, sliced only as rough visual positions.",
        "- `H-1846`: Kenoyer/Meadow H95-2672 object/panel crop, layout-not-ready for an exact source-derived `603` crop.",
        "- `H-360`: Vats Plate XCVIII no.584 `636` source-visible control band, sliced only as rough visual positions.",
        "",
        "## Visual Decision",
        "",
        "The post-`861` side is usable as source-visible terminal-region evidence, with `M-1273` the strongest, `M-240` compatible but blurred, and `M-714` demoted to a broad rescue region rather than a clean tail crop.",
        "",
        "The Harappa side is not yet usable as exact source-derived `603` token evidence. `H-1138` contains a visible five-sign band and has rough equal-width slices that can be inspected visually, but orientation and token assignment are still unaccepted. `H-1846` remains object/figure visible but not layout-ready. `H-360` is useful as a visible `636` control band, but its X-slot sign is also not source-tokenized yet.",
        "",
        "Current classification:",
        "",
        "```text",
        "post_861_603_windows = source_visible_candidate_windows",
        "harappa_603_bands = source_visible_but_token_unassigned",
        "cross_context_603_graphic_identity = unresolved",
        "```",
        "",
        "## Linguistic Consequence",
        "",
        "`603` remains the live low-frequency bridge candidate because the distributional contrast still exists. But the bridge is not yet source-proven at the graphic-identity level. The next promotion requires source-tokenizing at least `H-1138` against `H-360`, then rechecking whether the candidate Harappa `603` unit is the same broad graphic class as the post-`861` terminal windows. `M-714` should not be used as fine-form evidence unless a better crop or higher-resolution source image cleanly separates the terminal sign.",
        "",
        "Accepted values/translations remain 0.",
    ]
    doc.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return doc


def main() -> None:
    manifest: list[dict[str, object]] = []

    for row in POST861:
        source = Path(row["source"])
        out = OUT / f"{row['item_id']}.png"
        width, height = crop(source, row["box"], out)
        manifest.append(
            {
                "item_id": row["item_id"],
                "object": row["object"],
                "role": row["role"],
                "text": row["text"],
                "source_path": str(source),
                "source_sha256": sha256(source),
                "crop_path": str(out),
                "crop_width": width,
                "crop_height": height,
                "source_note": row["source_note"],
                "token_assignment": row["token_assignment"],
                "quality": row["quality"],
                "notes": row["notes"],
            }
        )

    for row in SOURCE_BANDS:
        make_slices(row, manifest)

    manifest_csv = REPORTS / "campaign_032_002_861_603_graphic_identity_packet_manifest.csv"
    with manifest_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest[0].keys()))
        writer.writeheader()
        writer.writerows(manifest)

    contact = make_contact_sheet(manifest)
    slices = make_slice_sheet(manifest)
    doc = write_doc(manifest, contact, slices)

    summary = {
        "date": "2026-05-29",
        "campaign": "032-002-861 603 graphic identity packet",
        "manifest_rows": len(manifest),
        "post861_tail_windows": 3,
        "harappa_603_source_bands": ["H-1138", "H-1846"],
        "harappa_636_control_bands": ["H-360"],
        "decision": "cross_context_603_graphic_identity_unresolved",
        "contact_sheet": str(contact.resolve()),
        "slice_sheet": str(slices.resolve()),
        "manifest_csv": str(manifest_csv.resolve()),
        "doc": str(doc.resolve()),
        "not_accepted": ["603 value", "phonetic reading", "language identity", "translation"],
    }
    summary_json = REPORTS / "campaign_032_002_861_603_graphic_identity_packet_summary.json"
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
