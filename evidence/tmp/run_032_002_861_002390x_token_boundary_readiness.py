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
ART_DIR = ROOT / "tmp" / "002390x_token_boundary_readiness"
SOURCE_ROWS = REPORT_DIR / "campaign_032_002_861_002390x_source_normalized_contrast_rows.csv"
SOURCE_CROPS = REPORT_DIR / "campaign_032_002_861_002390x_source_normalized_contrast_source_crops.csv"
PREFIX = "campaign_032_002_861_002390x_token_boundary_readiness"
DATE = "2026-05-30"


@dataclass(frozen=True)
class Readiness:
    object_key: str
    local_text: str
    branch_after_390: str
    source_state: str
    visible_witnesses: str
    catalog_window: str
    readiness: str
    use_now: str
    risk: str
    demotion_trigger: str
    next_action: str


READINESS = [
    Readiness(
        "M-119",
        "+151-337-484-002-390-125-632-032-900-563+",
        "125",
        "strict_public_source_visible",
        "M119_face_A_signband.jpg; M119_impression_a_signband.jpg",
        "catalog positions 4-6 = 002-390-125; also tests 125->632-032",
        "token_box_ready_high",
        "yes_target",
        "source-local side/order still catalog-mediated; face/impression must be boxed without assuming Mayig/local sequence is source-derived",
        "If neither public side preserves a separable 002-390-125 window followed by the expected post-125 cluster under any explicit direction policy, demote M-119 from strict 125 support to source-visible object only.",
        "Blind token-box both sides; compare boxed unit count/order against local and Mayig only after boxing.",
    ),
    Readiness(
        "M-735",
        "+740-760-235-002-390-125-195+",
        "125",
        "strict_public_source_visible",
        "M735_face_A_signband.jpg; M735_impression_a_signband.jpg",
        "catalog positions 4-6 = 002-390-125; tests 235->002-390->125",
        "token_box_ready_high",
        "yes_target",
        "panel is readable but source/local side mapping is not independently proven in this packet",
        "If the visible band cannot support a separable 235->002-390->125 sequence under explicit side/order policy, demote the 235 subframe to one weak M-38-led clue.",
        "Blind token-box both sides and score the 235-before-frame and 125-after-frame windows separately.",
    ),
    Readiness(
        "Sktd-1",
        "+390-004-002-390-125-820+",
        "125",
        "panel_bound_public_candidate",
        "Sktd1_face_A_signband.jpg; Sktd1_impression_a_signband.jpg",
        "catalog positions 3-5 = 002-390-125; also tests 004->002-390 split",
        "token_box_ready_medium",
        "yes_but_downweighted",
        "panel-bound, but exact side and token sequence remain weaker than M-119/M-735; site/register difference may be doing the work",
        "If side/token boxing fails or the apparent window is not separable, keep Sktd-1 out of strict 125 counts and use only as acquisition pressure.",
        "Box as a panel-bound candidate; do not let it count equally with M-119/M-735 until side identity is explicit.",
    ),
    Readiness(
        "M-71",
        "+151-279-142-002-390-095+",
        "095",
        "strict_public_source_visible",
        "M71_face_A_signband.jpg; M71_impression_a_signband.jpg",
        "catalog positions 4-6 = 002-390-095",
        "token_box_ready_high",
        "yes_control",
        "it is one source-visible 095 control; H-1993 is still needed to make repeated 095 source-normalized",
        "If boxed source order does not preserve 002-390-095, repeated 095 drops back to source-dark H-1993 only.",
        "Blind token-box both sides as the immediate non-125 comparator against M-119/M-735.",
    ),
    Readiness(
        "M-70",
        "+226-032-002-390-692+",
        "692",
        "strict_public_source_visible",
        "M70_impression_a_signband_from_cisi_india_n066.png",
        "catalog positions 3-5 = 002-390-692",
        "token_box_ready_high",
        "yes_control",
        "single 692 control, but already decisive against necessary-125 if token boxing holds",
        "If source boxing fails to preserve 002-390-692, the strongest non-125 control weakens and M-71 must carry the control side.",
        "Keep as primary non-125 control and measure terminal closure/spacing in the same boxing pass.",
    ),
    Readiness(
        "M-38",
        "+740-690-435-255-220-032-240-235-002-390-125-632-032+",
        "125",
        "weak_public_context_not_token_boxable",
        "M-38_cisi_india_n55_plate_label_free_panel_enhanced_x2.jpg",
        "catalog positions 9-11 = 002-390-125; tests both 235-before and 125->632-032",
        "not_ready",
        "no",
        "public context exists, but the signband is too faint for token-level promotion",
        "No demotion needed: it is already weak. It must not be counted as strict source evidence until a sharper source appears.",
        "Acquire sharper image or leave it as weak formula-family pressure only.",
    ),
    Readiness(
        "H-1993",
        "+740-000-220-004-002-390-095+",
        "095",
        "source_dark",
        "",
        "catalog positions 5-7 = 002-390-095; would test 004->002-390 split",
        "not_ready",
        "no",
        "no public route in current packet",
        "If no route appears, 004-before split remains one-sided through Sktd-1 only.",
        "Route Harappa figure/source path before any linguistic use.",
    ),
    Readiness(
        "M-1825",
        "+157-031-002-390-705+",
        "705",
        "source_dark",
        "",
        "catalog positions 3-5 = 002-390-705",
        "not_ready",
        "no",
        "direct public CISI route not found in this pass",
        "Without M-1825 or Dholavira route, repeated 705 is not source-normalized evidence.",
        "Find CISI 3.1/HARP/archive route or keep 705 out.",
    ),
    Readiness(
        "Dholavira 4237.1",
        "+151-032-388-002-390-705+",
        "705",
        "source_dark",
        "",
        "catalog positions 4-6 = 002-390-705",
        "not_ready",
        "no",
        "object route unresolved",
        "Without this or M-1825, 705 remains unusable as repeated non-125 comparator.",
        "Resolve object/source route before counting.",
    ),
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


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


def crop_lookup() -> dict[str, list[dict[str, str]]]:
    out: dict[str, list[dict[str, str]]] = {}
    if not SOURCE_CROPS.exists():
        return out
    for row in read_csv(SOURCE_CROPS):
        out.setdefault(row["cisi"], []).append(row)
    return out


def make_contact_sheet(lookup: dict[str, list[dict[str, str]]]) -> Path:
    ART_DIR.mkdir(parents=True, exist_ok=True)
    tiles: list[tuple[Readiness, Path]] = []
    for r in READINESS:
        for crop in lookup.get(r.object_key, []):
            path = Path(crop.get("signband_path", ""))
            if path.exists():
                tiles.append((r, path))

    extra_paths = [
        (r, Path(ROOT / "tmp" / "032_002_branch_tail_source_acquisition" / "M70_impression_a_signband_from_cisi_india_n066.png"))
        for r in READINESS
        if r.object_key == "M-70"
    ]
    for r, p in extra_paths:
        if p.exists() and all(p != existing for _, existing in tiles):
            tiles.append((r, p))

    tile_w, image_h, label_h = 520, 220, 110
    cols = 2
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tile_w, rows * (image_h + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 17)
        small = ImageFont.truetype("arial.ttf", 13)
    except OSError:
        font = ImageFont.load_default()
        small = ImageFont.load_default()

    for idx, (r, path) in enumerate(tiles):
        img = Image.open(path).convert("RGB")
        img.thumbnail((tile_w - 20, image_h - 20))
        x = (idx % cols) * tile_w
        y = (idx // cols) * (image_h + label_h)
        sheet.paste(img, (x + 10, y + 10))
        draw.rectangle([x, y + image_h, x + tile_w, y + image_h + label_h], fill=(245, 245, 245), outline=(210, 210, 210))
        title = f"{r.object_key} | {r.branch_after_390} | {r.readiness}"
        draw.text((x + 10, y + image_h + 8), title[:70], fill=(0, 0, 0), font=font)
        draw.text((x + 10, y + image_h + 36), r.catalog_window[:82], fill=(30, 30, 30), font=small)
        draw.text((x + 10, y + image_h + 60), f"use_now={r.use_now}"[:82], fill=(30, 30, 30), font=small)

    out = ART_DIR / f"{PREFIX}_contact_sheet.jpg"
    sheet.save(out, quality=92)
    return out


def main() -> None:
    contrast_rows = read_csv(SOURCE_ROWS)
    branch_counts: dict[str, int] = {}
    for row in contrast_rows:
        branch_counts[row["next_after_390"]] = branch_counts.get(row["next_after_390"], 0) + 1

    lookup = crop_lookup()
    contact = make_contact_sheet(lookup)

    readiness_rows = [r.__dict__ for r in READINESS]
    decision_rows = [
        {
            "decision": "token_box_ready_targets",
            "members": "M-119 M-735",
            "meaning": "Strict source-visible 125 candidates ready for blind token-boundary judgment; still no value.",
        },
        {
            "decision": "token_box_ready_controls",
            "members": "M-70 M-71",
            "meaning": "Strict source-visible non-125 controls that block necessary-125 readings if their boxes hold.",
        },
        {
            "decision": "panel_bound_downweighted_target",
            "members": "Sktd-1",
            "meaning": "Useful for the 004-before split only after side/token identity is boxed.",
        },
        {
            "decision": "not_ready_exclusions",
            "members": "M-38 H-1993 M-1825 Dholavira_4237.1",
            "meaning": "Do not count as strict source-token evidence in the next inference.",
        },
    ]

    write_csv(REPORT_DIR / f"{PREFIX}_readiness_rows.csv", readiness_rows)
    write_csv(REPORT_DIR / f"{PREFIX}_decisions.csv", decision_rows)

    summary = {
        "date": DATE,
        "source_rows": len(contrast_rows),
        "branch_counts": branch_counts,
        "strict_token_box_ready_125_targets": ["M-119", "M-735"],
        "strict_token_box_ready_non125_controls": ["M-70", "M-71"],
        "panel_bound_downweighted_targets": ["Sktd-1"],
        "not_ready": ["M-38", "H-1993", "M-1825", "Dholavira 4237.1"],
        "decision": "token_boundary_readiness_defined_no_values",
        "contact_sheet": str(contact),
    }
    (REPORT_DIR / f"{PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    readylines = "\n".join(
        f"- `{r.object_key}`: {r.readiness}; {r.catalog_window}. Risk: {r.risk}"
        for r in READINESS
    )
    demotion = "\n".join(
        f"- `{r.object_key}`: {r.demotion_trigger}"
        for r in READINESS
        if r.use_now != "no"
    )
    text = dedent(
        f"""\
        # 032-002-861 / 002-390-X Token-Boundary Readiness

        Date: {DATE}

        ## Question

        Which `002-390-X` witnesses are ready for source-token boundary judgment, and what would demote `125` if the visible source bands do not preserve the catalog window?

        ## Result

        The next inference unit is a token-boundary packet, not a value assignment.

        Strict target rows ready for blind token boxing: `M-119` and `M-735`.

        Strict non-`125` controls ready for the same treatment: `M-70` and `M-71`.

        Downweighted public-panel target: `Sktd-1`.

        Excluded from strict source-token inference for now: `M-38`, `H-1993`, `M-1825`, and Dholavira `4237.1`.

        Contact sheet: `{contact}`

        ## Readiness Rows

        {readylines}

        ## Demotion Triggers

        {demotion}

        ## Linguistic Decision

        If `M-119` and `M-735` both preserve separable `002-390-125` windows under explicit side/order policies, while `M-70` and `M-71` preserve separable non-`125` windows, then the live object upgrades to a source-tokenized `002-390-X` branch contrast. That still gives no phonetic value, meaning, language identity, or translation.

        If either target fails source-token boxing, `125` drops back toward formula-family pressure. If both fail, `125` is demoted from live source-visible branch evidence to catalog/source-route pressure only.

        The forbidden shortcut is to read `125`. The permitted question is whether source-visible inscriptions preserve a real branch slot after `002-390`.
        """
    )
    text = "\n".join(line[8:] if line.startswith("        ") else line for line in text.splitlines()) + "\n"
    doc = DOC_DIR / f"{PREFIX}.md"
    doc.write_text(text, encoding="utf-8")
    print(json.dumps({**summary, "doc": str(doc)}, indent=2))


if __name__ == "__main__":
    main()
