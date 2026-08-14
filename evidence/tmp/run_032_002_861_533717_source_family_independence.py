"""Tests whether the 533-717 witnesses are independent artifacts or one copy family.

This script reads the filtered corpus metadata for seven focus objects (M-1954, M-355,
M-376, M-391, M-1267, M-1273, M-1973), with M-376 and M-391 as the targets. It carries
inline source routes and visual observations for each object, draws comparison
overlays with PIL into tmp/032_002_861_533717_source_family_independence, and asks
whether the two targets are independent witnesses or exact copies of one seal. It
writes a rows CSV and a summary JSON. The recorded decision: two artifact witnesses,
exact copy rejected, one narrow register family cell for linguistic weighting.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path.cwd()
METADATA = ROOT / "data" / "open_prototype" / "lipi" / "metadata_filtered.csv"
REPORTS = ROOT / "data" / "open_prototype" / "reports"
OUT = ROOT / "tmp" / "032_002_861_533717_source_family_independence"
OUT.mkdir(parents=True, exist_ok=True)

FOCUS_IDS = ["M-1954", "M-355", "M-376", "M-391", "M-1267", "M-1273", "M-1973"]
TARGET_IDS = {"M-376", "M-391"}

SOURCE_ROUTES = {
    "M-355": {
        "source_leaf": "india_n123",
        "printed_page": "88",
        "source_route": "CISI India IA leaf n123 / printed p.88 / Mohenjo-daro 353-355 seals no iconography I",
        "route_status": "public_source_visible",
    },
    "M-376": {
        "source_leaf": "india_n129",
        "printed_page": "94",
        "source_route": "CISI India IA leaf n129 / printed p.94 / Mohenjo-daro 376-381 seals no iconography III",
        "route_status": "public_source_visible",
    },
    "M-391": {
        "source_leaf": "india_n131",
        "printed_page": "96",
        "source_route": "CISI India IA leaf n131 / printed p.96 / Mohenjo-daro 391-396 seals no iconography III",
        "route_status": "public_source_visible",
    },
    "M-1267": {
        "source_leaf": "pakistan_n194",
        "printed_page": "160",
        "source_route": "CISI Pakistan IA leaf n194 / printed p.160 / Mohenjo-daro 1264-1268 seals no iconography I, II",
        "route_status": "public_source_visible",
    },
    "M-1273": {
        "source_leaf": "pakistan_n195",
        "printed_page": "161",
        "source_route": "CISI Pakistan IA leaf n195 / printed p.161 / Mohenjo-daro 1269-1274 seals no iconography II",
        "route_status": "public_source_visible",
    },
    "M-1954": {
        "source_leaf": "",
        "printed_page": "",
        "source_route": "not located in current public CISI India/Pakistan panel pass",
        "route_status": "source_pending_public_dark",
    },
    "M-1973": {
        "source_leaf": "",
        "printed_page": "",
        "source_route": "not located in current public CISI India/Pakistan panel pass",
        "route_status": "source_pending_public_dark",
    },
}

VISUALS = {
    "M-376": ROOT / "tmp" / "032_002_861_source_token_attachment" / "M376_533_717_source_token_attachment_overlay.png",
    "M-391": ROOT / "tmp" / "032_002_861_source_token_attachment" / "M391_533_717_source_token_attachment_overlay.png",
    "M-355": ROOT / "tmp" / "032_002_861_533717_register_controls" / "M355_rev_a_register_control.png",
    "M-1267": ROOT / "tmp" / "032_002_861_533717_register_controls" / "M1267_rev_a_register_control.png",
    "M-1273": ROOT / "tmp" / "032_002_861_533717_register_controls" / "M1273_rev_a_register_control.png",
}


def tail_after_002_861(text: str) -> str:
    tokens = text.strip("+").split("-")
    for idx in range(len(tokens) - 1):
        if tokens[idx : idx + 2] == ["002", "861"]:
            tail = tokens[idx + 2 :]
            return " ".join(tail) if tail else "<END>"
    return "<NO_002_861>"


def prefix_before_002_861(text: str) -> tuple[str, str]:
    tokens = text.strip("+").split("-")
    for idx in range(len(tokens) - 1):
        if tokens[idx : idx + 2] == ["002", "861"]:
            prefix = tokens[:idx]
            last1 = prefix[-1] if prefix else "<START>"
            last2 = " ".join(prefix[-2:]) if len(prefix) >= 2 else last1
            return last1, last2
    return "<NO_002_861>", "<NO_002_861>"


def tail_class(tail: str) -> str:
    if tail == "533 717":
        return "target_533_717"
    if tail == "<END>":
        return "bare"
    if tail == "603":
        return "short_alt_603"
    return "long_alt_tail"


def load_focus_rows() -> list[dict[str, str]]:
    by_cisi: dict[str, dict[str, str]] = {}
    with METADATA.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["cisi"] in FOCUS_IDS:
                by_cisi[row["cisi"]] = row

    rows: list[dict[str, str]] = []
    for cisi in FOCUS_IDS:
        row = by_cisi[cisi]
        tail = tail_after_002_861(row["text"])
        last1, last2 = prefix_before_002_861(row["text"])
        route = SOURCE_ROUTES[cisi]
        rows.append(
            {
                "cisi": cisi,
                "tail_after_002_861": tail,
                "tail_class": tail_class(tail),
                "text": row["text"],
                "text_length": row["text length"],
                "site": row["site"],
                "type": row["type"],
                "symbol": row["symbol"],
                "shape": row["shape"],
                "cross_section": row["cross-section"],
                "class": row["class"],
                "area_section": row["area-section"],
                "block_house": row["block-house"],
                "room_grid": row["room-grid"],
                "excavation_idno": row["excavation-idno"],
                "period": row["period"],
                "phase": row["phase"],
                "depth": row["depth"],
                "boss": row["boss"],
                "material": row["material"],
                "condition": row["condition"],
                "horizontal_mm": row["horizontal(mm)"],
                "vertical_mm": row["vertical(mm)"],
                "thickness_mm": row["thickness(mm)"],
                "prefix_last1": last1,
                "prefix_last2": last2,
                "source_leaf": route["source_leaf"],
                "printed_page": route["printed_page"],
                "source_route": route["source_route"],
                "route_status": route["route_status"],
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def make_visual_sheet(rows: list[dict[str, str]]) -> Path:
    cards: list[Image.Image] = []
    for row in rows:
        path = VISUALS.get(row["cisi"])
        if path and path.exists():
            img = Image.open(path).convert("RGB")
        else:
            img = Image.new("RGB", (900, 180), "white")
            draw = ImageDraw.Draw(img)
            draw.text((12, 70), "source pending public-dark", fill="black")
        img.thumbnail((760, 190))
        card = Image.new("RGB", (800, 260), "white")
        card.paste(img, (20, 55))
        draw = ImageDraw.Draw(card)
        draw.text(
            (20, 12),
            f"{row['cisi']} {row['tail_class']} len={row['text_length']} {row['shape']} {row['class']}",
            fill="black",
        )
        draw.text((20, 32), row["source_leaf"] or row["route_status"], fill="black")
        cards.append(card)
    sheet = Image.new("RGB", (800, 260 * len(cards)), "white")
    for idx, card in enumerate(cards):
        sheet.paste(card, (0, idx * 260))
    path = OUT / "533717_source_family_independence_contact_sheet.png"
    sheet.save(path)
    return path


def compare_targets(rows: list[dict[str, str]]) -> dict[str, object]:
    targets = [row for row in rows if row["cisi"] in TARGET_IDS]
    m376 = next(row for row in targets if row["cisi"] == "M-376")
    m391 = next(row for row in targets if row["cisi"] == "M-391")
    same = []
    different = []
    for field in [
        "source_leaf",
        "printed_page",
        "text",
        "text_length",
        "class",
        "area_section",
        "excavation_idno",
        "depth",
        "boss",
        "condition",
        "horizontal_mm",
        "vertical_mm",
        "prefix_last2",
    ]:
        item = {"field": field, "M-376": m376[field], "M-391": m391[field]}
        if m376[field] == m391[field]:
            same.append(item)
        else:
            different.append(item)
    return {
        "same_fields": same,
        "different_fields": different,
        "source_family_verdict": "not_exact_copy_family_under_current_metadata",
        "verdict_basis": [
            "M-376 and M-391 share broad site/type/symbol/shape/cross-section and tail.",
            "They differ in source leaf, printed page, full text, length, class, excavation identifiers, depth, boss, dimensions, and immediate pre-002-861 context.",
            "This rejects exact duplicate/copy collapse, but the pair remains one narrow source/register-family cell for linguistic weighting.",
        ],
    }


def main() -> None:
    rows = load_focus_rows()
    sheet = make_visual_sheet(rows)
    target_compare = compare_targets(rows)

    rows_csv = REPORTS / "campaign_032_002_861_533717_source_family_independence_rows.csv"
    summary_json = REPORTS / "campaign_032_002_861_533717_source_family_independence_summary.json"
    write_csv(rows_csv, rows, list(rows[0].keys()))

    payload = {
        "date": "2026-05-29",
        "focus_rows": len(rows),
        "source_visible_rows": sum(row["route_status"] == "public_source_visible" for row in rows),
        "source_pending_rows": sum(row["route_status"] != "public_source_visible" for row in rows),
        "targets": ["M-376", "M-391"],
        "controls": ["M-1954", "M-355", "M-1267", "M-1273", "M-1973"],
        "tail_classes": {row["cisi"]: row["tail_class"] for row in rows},
        "target_compare": target_compare,
        "decision": "two_artifact_witnesses_exact_copy_rejected_one_narrow_register_family_cell_for_linguistic_weighting",
        "next_question": "Do the target rows share a source-visible post-861 layout feature that same-register controls lack?",
        "outputs": {
            "rows_csv": str(rows_csv.resolve()),
            "contact_sheet": str(sheet.resolve()),
        },
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
