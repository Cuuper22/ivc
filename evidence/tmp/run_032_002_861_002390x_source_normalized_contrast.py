"""Source-normalized contrast for the 002-390-X branch: does 125 stay alive?

This script reads the row table from the earlier 002-390-125 branch source-route pass
and re-scores every witness under source normalization — meaning each row only counts
at the strength of its actual source evidence (a visible artifact crop counts; a bare
catalog transcription does not). It carries an inline table of established source facts
and a crop list, builds a crop packet under tmp/002390x_source_normalization with PIL,
and contrasts the 125 continuation against the source-visible non-125 continuations
(692, 095, 705). It writes rows, source-route, and crop CSVs, a summary JSON, and a
docs/ markdown note. The recorded decision: source normalization upgrades 125 as a
branch object but still accepts no value.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "data" / "open_prototype" / "reports"
DOC_DIR = ROOT / "docs"
ART_DIR = ROOT / "tmp" / "002390x_source_normalization"
SOURCE_ROWS = REPORT_DIR / "campaign_032_002_861_002390125_branch_source_route_rows.csv"

PREFIX = "campaign_032_002_861_002390x_source_normalized_contrast"
DATE = "2026-05-30"


@dataclass(frozen=True)
class CropSpec:
    key: str
    cisi: str
    side: str
    source_path: Path
    full_box: tuple[int, int, int, int] | None
    signband_box: tuple[int, int, int, int] | None
    source_route: str
    source_note: str
    signband_readiness: str


CROPS = [
    CropSpec(
        "M71_face_A",
        "M-71",
        "A",
        ROOT / "tmp" / "032_002_branch_tail_source_acquisition" / "cisi_india_n066_w2000.jpg",
        (400, 1080, 1130, 1765),
        (400, 1080, 1130, 1395),
        "public_source_visible_cisi_india_n066",
        "M-71 A/a sit on the same public CISI India n66 plate as M-70; this upgrades repeated 095 from index-hint to source-visible comparator.",
        "inspectable_comparator",
    ),
    CropSpec(
        "M71_impression_a",
        "M-71",
        "a",
        ROOT / "tmp" / "032_002_branch_tail_source_acquisition" / "cisi_india_n066_w2000.jpg",
        (1530, 1090, 2220, 1775),
        (1530, 1090, 2220, 1390),
        "public_source_visible_cisi_india_n066",
        "M-71 impression crop for source-visible repeated 095 comparator.",
        "inspectable_comparator",
    ),
    CropSpec(
        "M119_face_A",
        "M-119",
        "A",
        ART_DIR / "cisi_india_n076_w2000.jpg",
        (1580, 210, 2250, 810),
        (1580, 210, 2250, 395),
        "public_source_visible_cisi_india_n076",
        "CISI India n76, printed p.41, panel labels M-117 to M-122. M-119 is now public-source-visible, not merely Mayig-overlap.",
        "inspectable_target",
    ),
    CropSpec(
        "M119_impression_a",
        "M-119",
        "a",
        ART_DIR / "cisi_india_n076_w2000.jpg",
        (1580, 950, 2240, 1530),
        (1580, 950, 2240, 1185),
        "public_source_visible_cisi_india_n076",
        "M-119 impression side. This supplies the strongest public visual route for 125 followed by 632 032.",
        "inspectable_target",
    ),
    CropSpec(
        "M735_face_A",
        "M-735",
        "A",
        ART_DIR / "cisi_pakistan_n086_w2000.jpg",
        (430, 1740, 1510, 2720),
        (430, 1740, 1510, 2080),
        "public_source_visible_cisi_pakistan_n086",
        "CISI Pakistan n86, printed p.52, panel labels M-734 to M-736. M-735 is now public-source-visible.",
        "inspectable_target",
    ),
    CropSpec(
        "M735_impression_a",
        "M-735",
        "a",
        ART_DIR / "cisi_pakistan_n086_w2000.jpg",
        (1840, 1730, 2875, 2710),
        (1840, 1730, 2875, 2100),
        "public_source_visible_cisi_pakistan_n086",
        "M-735 impression side. This is the source-visible candidate for 235 before 002-390 and 125 after it.",
        "inspectable_target",
    ),
    CropSpec(
        "Sktd1_face_A",
        "Sktd-1",
        "A",
        ART_DIR / "cisi_india_n397_w2000.jpg",
        (110, 1775, 745, 2355),
        (110, 1775, 745, 2005),
        "panel_bound_public_cisi_india_n397",
        "CISI India n397 panel-binds Sktd-1 A/a on the Surkotada row. Still weaker than M-119/M-735 because exact side and token sequence remain catalog-mediated.",
        "panel_bound_candidate",
    ),
    CropSpec(
        "Sktd1_impression_a",
        "Sktd-1",
        "a",
        ART_DIR / "cisi_india_n397_w2000.jpg",
        (860, 1775, 1540, 2370),
        (860, 1775, 1540, 2010),
        "panel_bound_public_cisi_india_n397",
        "Sktd-1 impression side. Useful for branch ecology, not yet a clean token-box proof.",
        "panel_bound_candidate",
    ),
]


SOURCE_FACTS = {
    "M-38": {
        "normalized_source_route": "public_context_low_readability_cisi_india_n055",
        "normalized_source_grade": "weak_public_context_not_token_boxable",
        "normalized_decision": "keep_as_weak_support_only",
        "strict_source_visible": False,
        "permissive_public_panel": False,
        "note": "Panel/context exists, but the source image is too faint for token-level promotion.",
    },
    "M-70": {
        "normalized_source_route": "public_source_visible_cisi_india_n066",
        "normalized_source_grade": "strict_source_visible_non125_control",
        "normalized_decision": "anchor_non125_692_control",
        "strict_source_visible": True,
        "permissive_public_panel": True,
        "note": "Source-visible 002-390-692 control already cropped from CISI India n66.",
    },
    "M-71": {
        "normalized_source_route": "public_source_visible_cisi_india_n066",
        "normalized_source_grade": "strict_source_visible_non125_comparator",
        "normalized_decision": "upgrade_repeated_095_control",
        "strict_source_visible": True,
        "permissive_public_panel": True,
        "note": "M-71 A/a are visible on CISI India n66, upgrading repeated 095 from index hint.",
    },
    "M-119": {
        "normalized_source_route": "public_source_visible_cisi_india_n076",
        "normalized_source_grade": "strict_source_visible_125_candidate",
        "normalized_decision": "upgrade_125_from_mayig_overlap",
        "strict_source_visible": True,
        "permissive_public_panel": True,
        "note": "M-119 is visible on CISI India n76, printed p.41, panel M-119 A/a.",
    },
    "M-735": {
        "normalized_source_route": "public_source_visible_cisi_pakistan_n086",
        "normalized_source_grade": "strict_source_visible_125_candidate",
        "normalized_decision": "upgrade_125_from_index_hint",
        "strict_source_visible": True,
        "permissive_public_panel": True,
        "note": "M-735 is visible on CISI Pakistan n86, printed p.52, panel M-735 A/a.",
    },
    "Sktd-1": {
        "normalized_source_route": "panel_bound_public_cisi_india_n397",
        "normalized_source_grade": "panel_bound_public_candidate",
        "normalized_decision": "upgrade_but_keep_below_strict_token_proof",
        "strict_source_visible": False,
        "permissive_public_panel": True,
        "note": "Sktd-1 is panel-bound on CISI India n397, but exact side and token sequence still need token-boxing.",
    },
    "M-1825": {
        "normalized_source_route": "still_unrouted_public_source_dark",
        "normalized_source_grade": "source_dark",
        "normalized_decision": "do_not_use_as_source_normalized_705_yet",
        "strict_source_visible": False,
        "permissive_public_panel": False,
        "note": "Direct CISI XML search did not locate M-1825 in the local India/Pakistan scans.",
    },
    "H-1993": {
        "normalized_source_route": "harappa_route_unresolved_not_public_cisi",
        "normalized_source_grade": "source_dark",
        "normalized_decision": "do_not_use_as_source_normalized_095_yet",
        "strict_source_visible": False,
        "permissive_public_panel": False,
        "note": "Likely requires Harappa figure/acquisition route, not CISI India/Pakistan page route.",
    },
    "-:3335.1": {
        "normalized_source_route": "unresolved_non_cisi_object",
        "normalized_source_grade": "source_dark",
        "normalized_decision": "do_not_use_as_source_normalized_590_yet",
        "strict_source_visible": False,
        "permissive_public_panel": False,
        "note": "No stable public label route yet.",
    },
    "-:4237.1": {
        "normalized_source_route": "dholavira_object_unresolved",
        "normalized_source_grade": "source_dark",
        "normalized_decision": "do_not_use_as_source_normalized_705_yet",
        "strict_source_visible": False,
        "permissive_public_panel": False,
        "note": "No stable public label route yet.",
    },
}


def row_key(row: dict[str, str]) -> str:
    if row["cisi"] == "-":
        return f"-:{row['id']}"
    return row["cisi"]


def read_rows() -> list[dict[str, str]]:
    with SOURCE_ROWS.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def enrich_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    enriched = []
    for row in rows:
        fact = SOURCE_FACTS.get(row_key(row), {})
        out = dict(row)
        out.update(
            {
                "normalized_source_route": fact.get("normalized_source_route", row.get("source_tier", "")),
                "normalized_source_grade": fact.get("normalized_source_grade", row.get("source_tier", "")),
                "normalized_decision": fact.get("normalized_decision", "not_revisited_in_this_contrast"),
                "normalized_note": fact.get("note", row.get("source_note", "")),
                "strict_source_visible": str(bool(fact.get("strict_source_visible", False))),
                "permissive_public_panel": str(bool(fact.get("permissive_public_panel", False))),
            }
        )
        enriched.append(out)
    return enriched


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def safe_crop(img: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    left, top, right, bottom = box
    left = max(0, min(left, img.width - 1))
    top = max(0, min(top, img.height - 1))
    right = max(left + 1, min(right, img.width))
    bottom = max(top + 1, min(bottom, img.height))
    return img.crop((left, top, right, bottom))


def make_crops() -> list[dict[str, str]]:
    ART_DIR.mkdir(parents=True, exist_ok=True)
    crop_rows: list[dict[str, str]] = []
    for spec in CROPS:
        if not spec.source_path.exists():
            crop_rows.append(
                {
                    "key": spec.key,
                    "cisi": spec.cisi,
                    "side": spec.side,
                    "source_path": str(spec.source_path),
                    "source_route": spec.source_route,
                    "source_note": spec.source_note,
                    "signband_readiness": "missing_source_image",
                    "full_panel_path": "",
                    "signband_path": "",
                }
            )
            continue
        img = Image.open(spec.source_path).convert("RGB")
        full_path = ART_DIR / f"{spec.key}_full_panel.jpg"
        signband_path = ART_DIR / f"{spec.key}_signband.jpg"
        full = safe_crop(img, spec.full_box) if spec.full_box else img.copy()
        signband = safe_crop(img, spec.signband_box) if spec.signband_box else full.copy()
        full.save(full_path, quality=92)
        signband.save(signband_path, quality=92)
        crop_rows.append(
            {
                "key": spec.key,
                "cisi": spec.cisi,
                "side": spec.side,
                "source_path": str(spec.source_path),
                "source_route": spec.source_route,
                "source_note": spec.source_note,
                "signband_readiness": spec.signband_readiness,
                "full_panel_path": str(full_path),
                "signband_path": str(signband_path),
            }
        )

    existing = [
        {
            "key": "M70_a_existing",
            "cisi": "M-70",
            "side": "a",
            "source_path": str(ROOT / "tmp" / "032_002_branch_tail_source_acquisition" / "cisi_india_n066_w2000.jpg"),
            "source_route": "public_source_visible_cisi_india_n066",
            "source_note": "Existing source-visible non-125 692 control crop from prior branch-tail acquisition.",
            "signband_readiness": "inspectable_comparator",
            "full_panel_path": str(ROOT / "tmp" / "032_002_branch_tail_source_acquisition" / "M70_impression_a_full_panel_from_cisi_india_n066.png"),
            "signband_path": str(ROOT / "tmp" / "032_002_branch_tail_source_acquisition" / "M70_impression_a_signband_from_cisi_india_n066.png"),
        },
        {
            "key": "M38_context_existing",
            "cisi": "M-38",
            "side": "context",
            "source_path": str(ROOT / "tmp" / "source_box_negative_control_v2" / "pages" / "M-38_cisi_india_n55_plate.jpg"),
            "source_route": "public_context_low_readability_cisi_india_n055",
            "source_note": "Existing public context/panel crop. It remains too faint for token-level promotion.",
            "signband_readiness": "weak_not_token_boxable",
            "full_panel_path": str(ROOT / "tmp" / "source_box_negative_control_v2" / "panel_crops" / "M-38_cisi_india_n55_plate_label_free_panel_enhanced_x2.jpg"),
            "signband_path": str(ROOT / "tmp" / "source_box_negative_control_v2" / "panel_crops" / "M-38_cisi_india_n55_plate_label_free_panel_enhanced_x2.jpg"),
        },
    ]
    crop_rows.extend(existing)
    return crop_rows


def make_contact_sheet(crop_rows: list[dict[str, str]]) -> Path:
    tiles = []
    for row in crop_rows:
        path = Path(row["signband_path"])
        if path.exists():
            img = Image.open(path).convert("RGB")
            tiles.append((row, img))

    tile_w, tile_h = 420, 260
    label_h = 76
    cols = 2
    rows_n = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tile_w, rows_n * (tile_h + label_h)), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 17)
        small = ImageFont.truetype("arial.ttf", 13)
    except OSError:
        font = ImageFont.load_default()
        small = ImageFont.load_default()

    for idx, (row, img) in enumerate(tiles):
        col = idx % cols
        r = idx // cols
        x = col * tile_w
        y = r * (tile_h + label_h)
        img.thumbnail((tile_w - 20, tile_h - 20))
        sheet.paste(img, (x + 10, y + 10))
        label = f"{row['key']} | {row['source_route']}"
        note = row["signband_readiness"]
        draw.rectangle([x, y + tile_h, x + tile_w, y + tile_h + label_h], fill=(245, 245, 245), outline=(210, 210, 210))
        draw.text((x + 10, y + tile_h + 8), label[:62], fill=(0, 0, 0), font=font)
        draw.text((x + 10, y + tile_h + 36), note[:80], fill=(40, 40, 40), font=small)

    out = ART_DIR / f"{PREFIX}_contact_sheet.jpg"
    sheet.save(out, quality=92)
    return out


def branch_contrast(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    by_branch: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_branch[row["next_after_390"]].append(row)

    contrast = []
    for branch, group in sorted(by_branch.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        members = [row_key(r) for r in group]
        strict = [row_key(r) for r in group if r["strict_source_visible"] == "True"]
        permissive = [row_key(r) for r in group if r["permissive_public_panel"] == "True"]
        terminal = [row_key(r) for r in group if r["tail_after_next"] == "<END>"]
        tails = sorted({r["tail_after_next"] for r in group})
        if branch == "125":
            decision = "live_plurality_candidate_no_value; upgraded by M-119/M-735, still not necessary because source-visible non-125 controls exist"
        elif branch in {"692", "095"}:
            decision = "source_visible_non125_control_against_125_necessity" if strict else "non125_control_needs_more_source"
        elif branch == "705":
            decision = "repeated_non125_branch_but_source_dark_in_this_pass"
        else:
            decision = "singletons_not_promoted"
        contrast.append(
            {
                "next_after_390": branch,
                "row_count": len(group),
                "members": " ".join(members),
                "terminal_members": " ".join(terminal),
                "tails_after_next": " | ".join(tails),
                "strict_source_visible_count": len(strict),
                "strict_source_visible_members": " ".join(strict),
                "permissive_public_panel_count": len(permissive),
                "permissive_public_panel_members": " ".join(permissive),
                "decision": decision,
            }
        )
    return contrast


def subframe_tests() -> list[dict[str, str]]:
    return [
        {
            "test": "235_before_002390_then_125",
            "positive_rows": "M-38 M-735",
            "source_state": "M-735 is now public-source-visible; M-38 remains weak context only",
            "interpretation": "The subframe survives as a live branch pattern through M-735, but not as a two-source proof because M-38 is unreadable at token level.",
            "avoid_distraction_rule": "Do not debate value of 125; only ask whether the local frame recurs under source visibility.",
            "next_needed": "Token-box M-735 and acquire sharper M-38 or independent 235->002-390->125 witness.",
        },
        {
            "test": "125_followed_by_632_032",
            "positive_rows": "M-119 M-38",
            "source_state": "M-119 is now public-source-visible; M-38 remains weak context only",
            "interpretation": "This is a real internal 125 subfamily candidate, but it may be one formula family rather than a general 125 function.",
            "avoid_distraction_rule": "Keep it as a formula-family contrast, not a translation claim.",
            "next_needed": "Find non-M-38/M-119 controls for 125->632 and non-125->632.",
        },
        {
            "test": "004_before_002390_split",
            "positive_rows": "H-1993 has 004->002-390->095; Sktd-1 has 004->002-390->125",
            "source_state": "Sktd-1 is panel-bound public candidate; H-1993 remains source-dark",
            "interpretation": "Potentially useful minimal split, but not interpretable until H-1993 is routed.",
            "avoid_distraction_rule": "No syntactic story from a one-sided source state.",
            "next_needed": "Route H-1993 through Harappa figure/source path.",
        },
        {
            "test": "source_visible_non125_controls",
            "positive_rows": "M-70 692; M-71 095",
            "source_state": "Both are source-visible on CISI India n66 after this pass",
            "interpretation": "This kills any necessary-125 reading for 002-390. 125 is a branch member, not a mandatory suffix.",
            "avoid_distraction_rule": "Use controls to constrain grammar immediately, not as an audit footnote.",
            "next_needed": "Add source-visible 705 or another repeated non-125 continuation.",
        },
        {
            "test": "repeated_705_branch",
            "positive_rows": "M-1825 and Dholavira 4237.1",
            "source_state": "Both are source-dark/unresolved in this pass",
            "interpretation": "Potentially important because repeated non-125 continuations would sharpen the branch ecology, but currently unusable for source-normalized inference.",
            "avoid_distraction_rule": "Do not count it as evidence until one route is visible.",
            "next_needed": "Resolve M-1825 and Dholavira image routes.",
        },
    ]


def write_markdown(
    rows: list[dict[str, str]],
    contrast: list[dict[str, object]],
    route_rows: list[dict[str, str]],
    crop_rows: list[dict[str, str]],
    subframes: list[dict[str, str]],
    contact_sheet: Path,
) -> Path:
    strict_125 = [
        r for r in rows if r["next_after_390"] == "125" and r["strict_source_visible"] == "True"
    ]
    permissive_125 = [
        r for r in rows if r["next_after_390"] == "125" and r["permissive_public_panel"] == "True"
    ]
    source_visible_non125 = [
        r for r in rows if r["next_after_390"] != "125" and r["strict_source_visible"] == "True"
    ]
    branch_lines = "\n".join(
        f"- `{c['next_after_390']}`: {c['row_count']} rows; strict source-visible {c['strict_source_visible_count']} ({c['strict_source_visible_members'] or 'none'}); decision: {c['decision']}"
        for c in contrast
    )
    route_lines = "\n".join(
        f"- `{r['cisi']}`: {r['normalized_source_grade']} via {r['normalized_source_route']}. {r['normalized_note']}"
        for r in route_rows
    )
    subframe_lines = "\n".join(
        f"- `{s['test']}`: {s['interpretation']} Source state: {s['source_state']}"
        for s in subframes
    )
    crop_lines = "\n".join(
        f"- `{r['key']}`: {r['signband_readiness']} -> `{r['signband_path']}`"
        for r in crop_rows
    )

    text = dedent(
        f"""\
        # 032-002-861 / 002-390-X Source-Normalized Contrast

        Date: {DATE}

        ## Question

        After the earlier `002-390-125` branch pass, does source normalization make `125` more alive, or does it dissolve into catalog/index noise once compared against source-visible non-`125` continuations?

        ## Result

        `125` is upgraded, but not translated.

        The prior state treated `M-119` as Mayig-only and `M-735` as an index-hint. This pass upgrades both: `M-119` is visible on CISI India `n076`, and `M-735` is visible on CISI Pakistan `n086`. `Sktd-1` is also panel-bound on CISI India `n397`, though it stays below strict token proof. `M-38` remains weak: the public context exists, but the signband is too faint for token-level promotion.

        That changes the branch from "mostly source-dark" to "source-visible plurality candidate." It still does not give a sign value. The source-visible controls `M-70` (`002-390-692`) and `M-71` (`002-390-095`) show that `002-390` can continue without `125`, so `125` cannot be a necessary continuation marker.

        Strict source-visible `125` candidates: {len(strict_125)} (`{" ".join(row_key(r) for r in strict_125) or "none"}`).

        Permissive public-panel `125` candidates: {len(permissive_125)} (`{" ".join(row_key(r) for r in permissive_125) or "none"}`).

        Strict source-visible non-`125` controls: {len(source_visible_non125)} (`{" ".join(row_key(r) for r in source_visible_non125) or "none"}`).

        Contact sheet: `{contact_sheet}`

        ## Branch Contrast

        {branch_lines}

        ## Source Route Decisions

        {route_lines}

        ## Subframe Tests

        {subframe_lines}

        ## Crop Packet

        {crop_lines}

        ## Linguistic Decision

        Keep `125` alive as a source-visible branch member inside `002-390-X`. Do not assign a value, phonetic reading, language identity, or translation.

        What changed: `125` is no longer just a catalog plurality. It now has strict public visual support through `M-119` and `M-735`, plus weaker panel-bound support through `Sktd-1`.

        What did not change: `125` is not necessary after `002-390`; `M-70` and `M-71` are source-visible non-`125` controls. The live linguistic object is therefore a branching continuation system after `002-390`, not a single suffix.

        ## Next Acquisition Targets

        1. Token-box `M-119`, `M-735`, `M-71`, `M-70`, and `Sktd-1` from the public plates.
        2. Route `H-1993` to test the `004->002-390` split against `Sktd-1`.
        3. Route `M-1825` and Dholavira `4237.1` to decide whether repeated `705` is a real non-`125` branch.
        4. Acquire a sharper `M-38` image before using it as anything stronger than weak formula-family support.

        Accepted values, phonetics, language identity, translations, exact source-token boundaries, and sign meanings remain `0`.
        """
    )
    text = "\n".join(line[8:] if line.startswith("        ") else line for line in text.splitlines()) + "\n"

    out = DOC_DIR / f"{PREFIX}.md"
    out.write_text(text, encoding="utf-8")
    return out


def main() -> None:
    rows = enrich_rows(read_rows())
    crop_rows = make_crops()
    contact_sheet = make_contact_sheet(crop_rows)

    route_rows = []
    for key, fact in SOURCE_FACTS.items():
        label = key.split(":", 1)[0] if key.startswith("-:") else key
        route_rows.append(
            {
                "cisi": label,
                "object_key": key,
                "normalized_source_route": fact["normalized_source_route"],
                "normalized_source_grade": fact["normalized_source_grade"],
                "normalized_decision": fact["normalized_decision"],
                "strict_source_visible": str(bool(fact["strict_source_visible"])),
                "permissive_public_panel": str(bool(fact["permissive_public_panel"])),
                "normalized_note": fact["note"],
            }
        )

    contrast = branch_contrast(rows)
    subframes = subframe_tests()

    write_csv(REPORT_DIR / f"{PREFIX}_rows.csv", rows)
    write_csv(REPORT_DIR / f"{PREFIX}_source_routes.csv", route_rows)
    write_csv(REPORT_DIR / f"{PREFIX}_source_crops.csv", crop_rows)
    write_csv(REPORT_DIR / f"{PREFIX}_branch_contrast.csv", contrast)
    write_csv(REPORT_DIR / f"{PREFIX}_subframe_tests.csv", subframes)

    summary = {
        "date": DATE,
        "row_count": len(rows),
        "branch_count": len({r["next_after_390"] for r in rows}),
        "strict_source_visible_125": [row_key(r) for r in rows if r["next_after_390"] == "125" and r["strict_source_visible"] == "True"],
        "permissive_public_panel_125": [row_key(r) for r in rows if r["next_after_390"] == "125" and r["permissive_public_panel"] == "True"],
        "strict_source_visible_non125_controls": [row_key(r) for r in rows if r["next_after_390"] != "125" and r["strict_source_visible"] == "True"],
        "decision": "source_normalization_upgrades_125_but_keeps_no_value",
        "contact_sheet": str(contact_sheet),
        "doc": str(DOC_DIR / f"{PREFIX}.md"),
    }
    (REPORT_DIR / f"{PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    doc = write_markdown(rows, contrast, route_rows, crop_rows, subframes, contact_sheet)

    print(json.dumps({**summary, "doc": str(doc)}, indent=2))


if __name__ == "__main__":
    main()
