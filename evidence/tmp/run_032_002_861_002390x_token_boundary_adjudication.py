from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "data" / "open_prototype" / "reports"
DOC_DIR = ROOT / "docs"
ART_DIR = ROOT / "tmp" / "002390x_token_boundary_adjudication"
PREFIX = "campaign_032_002_861_002390x_token_boundary_adjudication"
DATE = "2026-05-30"


FEATURES = {
    "002": "two adjacent half-height simple vertical strokes",
    "390": "simple tree with branches at the top",
    "125": "person with bow and arrow",
    "095": "person with short stick",
    "692": "outlined X",
    "235": "unscored preceding-frame sign in this packet",
}


@dataclass(frozen=True)
class Witness:
    neutral_id: str
    object_key: str
    role: str
    branch: str
    local_text: str
    best_crop: Path
    side_policy: str
    local_window: str
    expected_shapes: str
    window_box: tuple[int, int, int, int]
    token_boxes: str
    sign_count_visible: str
    boundary_verdict: str
    identity_verdict: str
    confidence: str
    adversary: str
    consequence: str


WITNESSES = [
    Witness(
        "N001",
        "M-119",
        "strict_125_target",
        "125",
        "+151-337-484-002-390-125-632-032-900-563+",
        ROOT / "tmp" / "002390x_source_normalization" / "M119_face_A_signband.jpg",
        "catalog/Mayig-compatible; source side-order still explicit-policy mediated",
        "positions 4-6 = 002-390-125; positions 6-8 = 125-632-032",
        "002 two short verticals -> 390 tree -> 125 archer/person-with-bow",
        (165, 15, 380, 160),
        "approx token windows: 165-225, 225-300, 300-380",
        "ten-sign band visible enough for window test",
        "boxed_window_compatible",
        "shape_match_plausible_not_source_derived_numeric_proof",
        "medium_high",
        "side/order and local numeric identity remain catalog/Mayig mediated; source image itself supplies separability, not a standalone reading",
        "keeps M-119 as strict target if M-735 also passes; no value accepted",
    ),
    Witness(
        "N002",
        "M-735",
        "strict_125_target",
        "125",
        "+740-760-235-002-390-125-195+",
        ROOT / "tmp" / "002390x_source_normalization" / "M735_impression_a_signband.jpg",
        "local R/L sequence compared against the clearer impression crop under explicit direction policy",
        "positions 3-6 = 235-002-390-125; positions 4-6 = 002-390-125",
        "235 precedes the same 002 two-strokes -> 390 tree -> 125 archer/person-with-bow window",
        (245, 15, 845, 250),
        "approx token windows: 245-410, 410-535, 535-690, 690-845",
        "seven-sign band visible; target region is crowded but separable",
        "boxed_window_compatible",
        "shape_match_plausible_but_less_secure_than_M119",
        "medium",
        "no Mayig independent row found; side/order and exact identity depend on local/corpus alignment",
        "keeps 235->002-390->125 as live only if family independence survives",
    ),
    Witness(
        "N003",
        "M-70",
        "strict_non125_control",
        "692",
        "+226-032-002-390-692+",
        ROOT / "tmp" / "032_002_branch_tail_source_acquisition" / "M70_impression_a_signband_from_cisi_india_n066.png",
        "Mayig/local-compatible source-visible control",
        "positions 3-5 = 002-390-692",
        "002 two short verticals -> 390 tree -> 692 outlined X",
        (300, 5, 900, 190),
        "approx token windows: 300-455, 455-650, 650-900",
        "five-sign band visible; terminal control window clear enough",
        "boxed_window_compatible",
        "shape_match_plausible_control",
        "medium_high",
        "single-branch control only; does not by itself establish repeated non-125 ecology",
        "blocks necessary-125 if paired with M-71 and if target windows hold",
    ),
    Witness(
        "N004",
        "M-71",
        "strict_non125_control",
        "095",
        "+151-279-142-002-390-095+",
        ROOT / "tmp" / "002390x_source_normalization" / "M71_impression_a_signband.jpg",
        "Mayig/local-compatible source-visible control",
        "positions 4-6 = 002-390-095",
        "002 two short verticals -> 390 tree -> 095 person-with-short-stick",
        (300, 5, 680, 250),
        "approx token windows: 300-410, 410-540, 540-680",
        "six-sign band visible; left edge crowding but target/control end readable enough",
        "boxed_window_compatible",
        "shape_match_plausible_control",
        "medium",
        "H-1993 still source-dark, so repeated 095 is not fully source-normalized",
        "adds second strict non-125 control and strengthens branch plurality",
    ),
    Witness(
        "N005",
        "Sktd-1",
        "downweighted_125_candidate",
        "125",
        "+390-004-002-390-125-820+",
        ROOT / "tmp" / "002390x_source_normalization" / "Sktd1_impression_a_signband.jpg",
        "panel-bound public candidate; exact side/order weaker than M-119/M-735",
        "positions 3-5 = 002-390-125",
        "002 two short verticals -> 390 tree -> 125 archer/person-with-bow",
        (140, 10, 530, 190),
        "approx token windows: 140-260, 260-390, 390-530",
        "six-sign band visible but blurrier; panel/source side caution remains",
        "boxed_window_compatible_downweighted",
        "shape_match_possible_not_strict",
        "low_medium",
        "site/register difference and side identity may be doing the work; H-1993 is absent on the 004->002-390->095 side",
        "cannot count equally with M-119/M-735 until side/token identity is explicit",
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


def draw_overlay(w: Witness) -> Path:
    img = Image.open(w.best_crop).convert("RGB")
    draw = ImageDraw.Draw(img, "RGBA")
    left, top, right, bottom = w.window_box
    draw.rectangle((left, top, right, bottom), outline=(255, 0, 0, 255), width=4)
    # Draw approximate token separators inside the window.
    coords = []
    raw = w.token_boxes.split(":", 1)[-1].strip()
    for chunk in raw.split(","):
        chunk = chunk.strip()
        if "-" not in chunk:
            continue
        a, b = chunk.split("-", 1)
        try:
            coords.append((int(a), int(b)))
        except ValueError:
            pass
    colors = [(0, 120, 255, 120), (0, 200, 80, 120), (255, 180, 0, 120), (160, 80, 255, 120)]
    for idx, (a, b) in enumerate(coords):
        draw.rectangle((a, top, b, bottom), outline=colors[idx % len(colors)][:3] + (255,), fill=colors[idx % len(colors)], width=2)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    draw.rectangle((0, 0, min(img.width, 360), 28), fill=(255, 255, 255, 220))
    draw.text((5, 5), f"{w.neutral_id} {w.object_key} {w.branch}", fill=(0, 0, 0), font=font)
    out = ART_DIR / f"{w.neutral_id}_{w.object_key.replace('-', '').replace(' ', '_')}_boxed.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, quality=92)
    return out


def make_contact_sheet(paths: list[tuple[Witness, Path]]) -> Path:
    tile_w, image_h, label_h = 620, 260, 105
    cols = 1
    sheet = Image.new("RGB", (tile_w, len(paths) * (image_h + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
        small = ImageFont.truetype("arial.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
        small = ImageFont.load_default()
    for idx, (w, path) in enumerate(paths):
        img = Image.open(path).convert("RGB")
        img.thumbnail((tile_w - 20, image_h - 20))
        y = idx * (image_h + label_h)
        sheet.paste(img, (10, y + 10))
        draw.rectangle((0, y + image_h, tile_w, y + image_h + label_h), fill=(245, 245, 245), outline=(210, 210, 210))
        draw.text((10, y + image_h + 8), f"{w.neutral_id} | {w.object_key} | {w.role} | {w.boundary_verdict}", fill=(0, 0, 0), font=font)
        draw.text((10, y + image_h + 38), w.expected_shapes[:86], fill=(20, 20, 20), font=small)
        draw.text((10, y + image_h + 64), f"confidence={w.confidence}; consequence={w.consequence}"[:100], fill=(20, 20, 20), font=small)
    out = ART_DIR / f"{PREFIX}_boxed_contact_sheet.jpg"
    sheet.save(out, quality=92)
    return out


def main() -> None:
    overlays = [(w, draw_overlay(w)) for w in WITNESSES]
    contact = make_contact_sheet(overlays)
    rows = []
    for w, overlay in overlays:
        d = w.__dict__.copy()
        d["best_crop"] = str(w.best_crop)
        d["window_box"] = " ".join(map(str, w.window_box))
        d["boxed_overlay"] = str(overlay)
        rows.append(d)
    write_csv(REPORT_DIR / f"{PREFIX}_adjudication_rows.csv", rows)
    feature_rows = [{"local_sign": k, "shape_description": v} for k, v in FEATURES.items()]
    write_csv(REPORT_DIR / f"{PREFIX}_feature_reference.csv", feature_rows)

    decisions = [
        {
            "decision": "strict_target_windows_boxed_compatible",
            "members": "M-119 M-735",
            "verdict": "both are compatible with separable boxed windows, but not yet blind source-preserved numeric readings",
        },
        {
            "decision": "strict_control_windows_boxed_compatible",
            "members": "M-70 M-71",
            "verdict": "both are compatible with separable non-125 windows, blocking necessary-125 only under current side/order policy",
        },
        {
            "decision": "sktd_downweighted_only",
            "members": "Sktd-1",
            "verdict": "usable as panel-bound pressure, not equal-weight strict support",
        },
        {
            "decision": "branch_contrast_state",
            "members": "002-390-X",
            "verdict": "upgrades to boxed-window-compatible branch contrast; no value/translation accepted",
        },
    ]
    write_csv(REPORT_DIR / f"{PREFIX}_decisions.csv", decisions)

    summary = {
        "date": DATE,
        "strict_125_targets_boxed_compatible": ["M-119", "M-735"],
        "strict_non125_controls_boxed_compatible": ["M-70", "M-71"],
        "downweighted_candidate": ["Sktd-1"],
        "decision": "boxed_window_compatible_branch_contrast_no_values",
        "contact_sheet": str(contact),
        "doc": str(DOC_DIR / f"{PREFIX}.md"),
    }
    (REPORT_DIR / f"{PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    feature_lines = "\n".join(f"- `{k}`: {v}" for k, v in FEATURES.items() if k != "235")
    witness_lines = "\n".join(
        f"- `{w.object_key}` ({w.role}): {w.boundary_verdict}; {w.identity_verdict}; confidence `{w.confidence}`. Consequence: {w.consequence}"
        for w in WITNESSES
    )
    adversary_lines = "\n".join(f"- `{w.object_key}`: {w.adversary}" for w in WITNESSES)
    text = dedent(
        f"""\
        # 032-002-861 / 002-390-X Token-Boundary Adjudication

        Date: {DATE}

        ## Question

        Are the visible source bands compatible with the immediate `002-390-X` windows for strict `125` targets and strict non-`125` controls under explicit side/order policy?

        ## Shape Reference

        This pass compares visible bands against sign-shape descriptions, not only catalog numbers:

        {feature_lines}

        ## Result

        The strict source-visible `125` targets `M-119` and `M-735` are compatible with separable boxed windows for `002-390-125` under explicit side/order policy. The strict non-`125` controls `M-70` and `M-71` are also compatible with boxed windows for `002-390-692` and `002-390-095`.

        This upgrades the live object to a boxed-window-compatible `002-390-X` branch contrast. It is not yet a blind source-preserved branch proof. It still does not accept a numeric value, phonetic reading, language identity, sign meaning, or translation.

        Boxed contact sheet: `{contact}`

        ## Witness Verdicts

        {witness_lines}

        ## Active Adversaries

        {adversary_lines}

        ## Linguistic Decision

        `125` survives the immediate boxed-window compatibility gate. It is not demoted by this visual pass alone.

        The next danger is side/order blindness, independence, and formula-family collapse. If blind adjudication rejects the boundaries, if `M-119` and `M-735` reduce to one family/source habit, or if `125` occurs only inside closed longer formulas, then `125` demotes even though the current boxes are visually plausible.

        Current status: `002-390-X` is a boxed-window-compatible branch contrast. `125` is a live branch member, not a reading.
        """
    )
    text = "\n".join(line[8:] if line.startswith("        ") else line for line in text.splitlines()) + "\n"
    doc = DOC_DIR / f"{PREFIX}.md"
    doc.write_text(text, encoding="utf-8")
    print(json.dumps({**summary, "doc": str(doc)}, indent=2))


if __name__ == "__main__":
    main()
