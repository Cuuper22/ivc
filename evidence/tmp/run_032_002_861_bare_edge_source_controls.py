from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path.cwd()
OUT = ROOT / "tmp" / "032_002_861_bare_edge_source_controls"
REPORTS = ROOT / "data" / "open_prototype" / "reports"
OUT.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

IA_ID = "TheIndusScript.TextConcordanceAndTablesIravathanMahadevan"
VOLS = {
    "india": "Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India",
    "pakistan": "Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan",
}

ALL_CONTROL_ROWS = [
    {
        "cisi": "H-444",
        "family": "220-032-002-861",
        "text": "+241-220-032-002-861+",
        "match_pressure": "bare control for M-91 255-416 and M-240 603",
        "route_status": "source_visible_existing",
        "source_route": "CISI Pakistan IA leaf n309 / printed p.275? / prior source-function packet page 310",
        "source_image": ROOT / "tmp/032_002_y_source_function_batch/H444_non240_861_signband_closeup.png",
        "panel_image": ROOT / "tmp/032_002_y_source_function_batch/H444_non240_861_page310_full_panel_context.png",
        "line_window": (0, 0, 700, 338),
        "bare_edge_window": (20, 25, 290, 330),
        "terminal_side_margin": (0, 25, 28, 330),
        "visual_status": "bare_terminal_edge_visible",
        "source_note": "Existing token-box scaffold places the terminal-side 002-861 candidate in a broad left edge window.",
        "evidence_note": "220-032 bare edge against two tailed 220-032 rows.",
    },
    {
        "cisi": "M-723",
        "family": "220-032-002-861",
        "text": "+740-460-510-235-220-032-002-861+",
        "match_pressure": "bare control for M-91 255-416 and M-240 603",
        "route_status": "source_visible_this_campaign",
        "source_route": "CISI Pakistan IA leaf n82 / printed p.48 / Mohenjo-daro 722-725 seals unicorn III",
        "volume": "pakistan",
        "leaf": 82,
        "page_box": (370, 1110, 1325, 1810),
        "signband_box": (390, 1110, 1315, 1455),
        "line_window": (0, 0, 925, 345),
        "bare_edge_window": (0, 0, 315, 330),
        "terminal_side_margin": (0, 0, 38, 330),
        "visual_status": "bare_terminal_edge_visible",
        "source_note": "A-side crop gives a same-line top signband with no visible post-edge material on the terminal side.",
        "evidence_note": "Second public 220-032 bare edge, same broad lane as M-91 and M-240.",
    },
    {
        "cisi": "M-77",
        "family": "803-002-861",
        "text": "+832-390-803-002-861+",
        "match_pressure": "bare control for M-714 603",
        "route_status": "source_visible_existing",
        "source_route": "CISI India IA leaf n68 / M-77 source gate",
        "source_image": ROOT / "tmp/m77_parpola_recurrence_gate/derived/M77_impression_a_signband_v3_from_cisi_india_n68.png",
        "panel_image": ROOT / "tmp/m77_parpola_recurrence_gate/derived/M77_impression_a_panel_v3_from_cisi_india_n68.png",
        "line_window": (0, 0, 750, 280),
        "bare_edge_window": (0, 0, 330, 275),
        "terminal_side_margin": (0, 0, 42, 275),
        "visual_status": "bare_terminal_edge_visible",
        "source_note": "Existing M-77 packet gives a public CISI source signband for the 803-002-861 bare control.",
        "evidence_note": "Direct public 803 bare edge against M-714 803-002-861-603.",
    },
    {
        "cisi": "M-15",
        "family": "176-002-861",
        "text": "+090-740-176-002-861+",
        "match_pressure": "bare control for M-376 533-717",
        "route_status": "source_visible_this_campaign",
        "source_route": "CISI India IA leaf n46 / printed p.11 / Mohenjo-daro 13-15 seals unicorn II",
        "volume": "india",
        "leaf": 46,
        "page_box": (70, 2375, 930, 3235),
        "signband_box": (70, 2375, 930, 2665),
        "line_window": (0, 0, 860, 290),
        "bare_edge_window": (0, 0, 335, 285),
        "terminal_side_margin": (0, 0, 45, 285),
        "visual_status": "bare_terminal_edge_visible",
        "source_note": "A-side crop gives a same-line top signband; icon heading differs from local symbol, so it is used for line/edge behavior only.",
        "evidence_note": "Direct public 176 bare edge against M-376 176-002-861-533-717.",
    },
    {
        "cisi": "M-118",
        "family": "803-002-861",
        "text": "+740-772-033-705-233-803-002-861+",
        "match_pressure": "bare control for M-714 603",
        "route_status": "source_visible_this_campaign",
        "source_route": "CISI India IA leaf n76 / printed p.41 / Mohenjo-daro 117-122 seals unicorn IV",
        "volume": "india",
        "leaf": 76,
        "page_box": (710, 850, 1340, 1480),
        "signband_box": (720, 870, 1325, 1135),
        "line_window": (0, 0, 605, 265),
        "bare_edge_window": (0, 0, 250, 260),
        "terminal_side_margin": (0, 0, 35, 260),
        "visual_status": "bare_terminal_edge_visible",
        "source_note": "Impression-side crop gives a source-visible 803-002-861 control in the same broad lane as M-714.",
        "evidence_note": "Second public 803 bare edge target, paired with M-77 for M-714.",
    },
    {
        "cisi": "M-1044",
        "family": "220-032-002-861",
        "text": "+520-220-032-002-861+",
        "match_pressure": "bare control for M-91 255-416 and M-240 603",
        "route_status": "source_visible_this_campaign",
        "source_route": "CISI Pakistan IA leaf n138 / printed p.104 / Mohenjo-daro 1043-1050 seals broken bovids IV-V",
        "volume": "pakistan",
        "leaf": 138,
        "page_box": (1660, 190, 2260, 810),
        "signband_box": (1660, 300, 2260, 635),
        "line_window": (0, 0, 600, 335),
        "bare_edge_window": (0, 0, 280, 330),
        "terminal_side_margin": (0, 0, 38, 330),
        "visual_status": "bare_terminal_edge_visible",
        "source_note": "A-side crop gives a short 220-032-002-861 source control; object is fragmentary but label and line are visible.",
        "evidence_note": "Short 220-032 bare control against M-91 and M-240.",
    },
    {
        "cisi": "M-1763",
        "family": "220-032-002-861",
        "text": "+416-001-565-740-220-032-002-861+",
        "match_pressure": "bare control for M-91 255-416 and M-240 603",
        "route_status": "route_pending_panel_or_cisi_3_1",
        "source_route": "local CISI Pakistan OCR has data/register pressure, not a usable panel hit",
    },
    {
        "cisi": "M-1880",
        "family": "176-002-861",
        "text": "+151-176-002-861+",
        "match_pressure": "bare control for M-376 533-717",
        "route_status": "route_pending_panel_or_cisi_3_1",
        "source_route": "not found in local public CISI 1/2 panel OCR pass",
    },
    {
        "cisi": "M-1755",
        "family": "176-002-861",
        "text": "+740-176-002-861+",
        "match_pressure": "bare control for M-376 533-717",
        "route_status": "route_pending_panel_or_cisi_3_1",
        "source_route": "local CISI Pakistan OCR has data/register pressure, not a usable panel hit",
    },
    {
        "cisi": "M-2060",
        "family": "176-002-861",
        "text": "+740-176-002-861+",
        "match_pressure": "bare control for M-376 533-717",
        "route_status": "route_pending_panel_or_cisi_3_1",
        "source_route": "not found in local public CISI 1/2 panel OCR pass",
    },
]


def direct_url(volume: str, leaf: int) -> str:
    return f"https://archive.org/download/{IA_ID}/{VOLS[volume]}/page/n{leaf}_w2000.jpg"


def reader_url(volume: str, leaf: int) -> str:
    return f"https://archive.org/details/{IA_ID}/{VOLS[volume]}/page/n{leaf}/mode/1up"


def page_path(volume: str, leaf: int) -> Path:
    return OUT / f"cisi_{volume}_n{leaf:03d}_w2000.jpg"


def fetch_page(volume: str, leaf: int) -> Path:
    target = page_path(volume, leaf)
    if not target.exists():
        raise FileNotFoundError(f"source page must already exist locally: {target}")
    return target


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def font(size: int):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        return ImageFont.load_default()


def materialize_source_image(row: dict[str, object]) -> tuple[Path | None, Path | None]:
    if "source_image" in row:
        return Path(row["source_image"]), Path(row["panel_image"]) if row.get("panel_image") else None

    if row.get("route_status") != "source_visible_this_campaign":
        return None, None

    volume = str(row["volume"])
    leaf = int(row["leaf"])
    page = fetch_page(volume, leaf)
    image = Image.open(page).convert("RGB")

    panel = image.crop(row["page_box"])
    panel_out = OUT / f"{row['cisi'].replace('-', '')}_panel_cisi_{volume}_n{leaf:03d}.png"
    panel.save(panel_out)

    signband = image.crop(row["signband_box"])
    signband_out = OUT / f"{row['cisi'].replace('-', '')}_signband_cisi_{volume}_n{leaf:03d}.png"
    signband.save(signband_out)
    return signband_out, panel_out


def draw_overlay(row: dict[str, object], source_image: Path) -> Path:
    im = Image.open(source_image).convert("RGB")
    pad = 66
    canvas = Image.new("RGB", (im.width, im.height + pad), "white")
    canvas.paste(im, (0, pad))
    draw = ImageDraw.Draw(canvas)
    title_font = font(18)
    label_font = font(14)
    draw.text((8, 8), f"{row['cisi']} {row['family']} bare edge control", fill=(0, 0, 0), font=title_font)
    draw.text((8, 32), "purple=line  green=bare terminal-side window  gray=terminal-side margin", fill=(55, 55, 55), font=label_font)

    boxes = [
        ("line_window", (165, 75, 210)),
        ("bare_edge_window", (20, 150, 70)),
        ("terminal_side_margin", (120, 120, 120)),
    ]
    for field, color in boxes:
        x1, y1, x2, y2 = row[field]
        shifted = (x1, y1 + pad, x2, y2 + pad)
        draw.rectangle(shifted, outline=color, width=4)
        label_y = y1 + pad + 6 if y1 < 24 else max(0, y1 + pad - 18)
        draw.text((x1 + 3, label_y), field, fill=color, font=label_font)

    out = OUT / f"{row['cisi'].replace('-', '')}_bare_edge_overlay.png"
    canvas.save(out)
    return out


def make_contact_sheet(overlays: list[Path]) -> Path:
    thumbs = []
    for path in overlays:
        im = Image.open(path).convert("RGB")
        im.thumbnail((1080, 430))
        thumbs.append(im.copy())
    width = 1140
    height = 20 + sum(im.height + 18 for im in thumbs)
    sheet = Image.new("RGB", (width, height), "white")
    y = 10
    for im in thumbs:
        sheet.paste(im, (20, y))
        y += im.height + 18
    out = OUT / "032_002_861_bare_edge_source_controls_contact_sheet.png"
    sheet.save(out)
    return out


def main() -> None:
    control_rows: list[dict[str, str]] = []
    crop_rows: list[dict[str, str]] = []
    overlays: list[Path] = []

    for row in ALL_CONTROL_ROWS:
        source_image, panel_image = materialize_source_image(row)
        overlay = None
        width = height = ""
        source_hash = ""
        if source_image is not None:
            overlay = draw_overlay(row, source_image)
            overlays.append(overlay)
            with Image.open(source_image) as im:
                width, height = map(str, im.size)
            source_hash = sha256(source_image)
            crop_rows.append(
                {
                    "cisi": str(row["cisi"]),
                    "family": str(row["family"]),
                    "source_image_abs": str(source_image.resolve()),
                    "source_sha256": source_hash,
                    "source_width": width,
                    "source_height": height,
                    "panel_image_abs": str(panel_image.resolve()) if panel_image else "",
                    "overlay_abs": str(overlay.resolve()),
                    "visual_status": str(row["visual_status"]),
                    "source_note": str(row["source_note"]),
                }
            )

        reader = ""
        direct = ""
        if "volume" in row:
            reader = reader_url(str(row["volume"]), int(row["leaf"]))
            direct = direct_url(str(row["volume"]), int(row["leaf"]))
        control_rows.append(
            {
                "cisi": str(row["cisi"]),
                "family": str(row["family"]),
                "text": str(row["text"]),
                "match_pressure": str(row["match_pressure"]),
                "route_status": str(row["route_status"]),
                "source_route": str(row["source_route"]),
                "reader_url": reader,
                "direct_image_url": direct,
                "source_image_abs": str(source_image.resolve()) if source_image else "",
                "source_sha256": source_hash,
                "overlay_abs": str(overlay.resolve()) if overlay else "",
                "visual_status": str(row.get("visual_status", "")),
                "evidence_note": str(row.get("evidence_note", "")),
            }
        )

    contact = make_contact_sheet(overlays)

    controls_csv = REPORTS / "campaign_032_002_861_bare_edge_source_controls_rows.csv"
    crops_csv = REPORTS / "campaign_032_002_861_bare_edge_source_controls_crops.csv"
    summary_json = REPORTS / "campaign_032_002_861_bare_edge_source_controls_summary.json"

    with controls_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(control_rows[0].keys()))
        writer.writeheader()
        writer.writerows(control_rows)

    with crops_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(crop_rows[0].keys()))
        writer.writeheader()
        writer.writerows(crop_rows)

    visible = [r for r in control_rows if r["route_status"].startswith("source_visible")]
    visible_by_family: dict[str, list[str]] = {}
    for row in visible:
        visible_by_family.setdefault(row["family"], []).append(row["cisi"])

    summary = {
        "date": "2026-05-29",
        "question": "Do matched bare terminal 002-861 controls have visible source edges for comparison against same-line tailed 002-861 rows?",
        "control_rows": len(control_rows),
        "source_visible_controls": len(visible),
        "route_pending_controls": len(control_rows) - len(visible),
        "source_visible_by_family": visible_by_family,
        "best_controls_now": ["H-444", "M-723", "M-1044", "M-77", "M-118", "M-15"],
        "evidence_effect": "The tailed rows now have source-visible bare-edge controls in the 220-032, 803, and 176 matched lanes.",
        "not_accepted": [
            "exact source-normalized 861/002 boundaries for every control",
            "addendum vs subclass vs apposition choice",
            "sign values",
            "phonetics",
            "language identity",
            "translation",
        ],
        "controls_csv": str(controls_csv.resolve()),
        "crops_csv": str(crops_csv.resolve()),
        "contact_sheet": str(contact.resolve()),
    }
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
