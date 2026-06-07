from __future__ import annotations

import csv
import json
import shutil
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
METADATA = ROOT / "data" / "open_prototype" / "lipi" / "metadata_filtered.csv"
ALL_002 = REPORTS / "campaign_032_002_post_y_all_002_rows.csv"
AFTER_032 = REPORTS / "campaign_032_002_post_y_branch_rows.csv"
OUT = ROOT / "tmp" / "032_002_861_suffix_split"

REPORTS.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

IA_ID = "TheIndusScript.TextConcordanceAndTablesIravathanMahadevan"
VOLS = {
    "india": "Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India",
    "pakistan": "Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan",
}

FOCUS_ROUTES = [
    {
        "cisi": "M-240",
        "object_id": "2763.1",
        "tail_family": "603",
        "text": "+520-240-220-032-002-861-603+",
        "scope": "after_032_and_all_002",
        "source_volume": "india",
        "leaf": 95,
        "printed_page": "60",
        "source_heading": "MOHENJO-DARO 240-242 SEALS bison",
        "panels": [],
        "route_status": "source_visible_previous_campaign",
    },
    {
        "cisi": "M-91",
        "object_id": "2618.1",
        "tail_family": "255 416",
        "text": "+740-100-798-220-032-002-861-255-416+",
        "scope": "after_032_and_all_002",
        "source_volume": "india",
        "leaf": 71,
        "printed_page": "36",
        "source_heading": "MOHENJO-DARO 89-94 SEALS unicorn IV",
        "panels": [],
        "route_status": "source_visible_previous_campaign",
    },
    {
        "cisi": "M-376",
        "object_id": "2872.1",
        "tail_family": "533 717",
        "text": "+740-100-176-002-861-533-717+",
        "scope": "all_002_only",
        "source_volume": "india",
        "leaf": 129,
        "printed_page": "94",
        "source_heading": "MOHENJO-DARO 376-381 SEALS no iconography III",
        "panels": [
            {"side": "A", "box": (105, 190, 900, 570)},
            {"side": "a", "box": (105, 640, 920, 1010)},
        ],
        "route_status": "source_visible_this_campaign",
    },
    {
        "cisi": "M-391",
        "object_id": "2887.1",
        "tail_family": "533 717",
        "text": "+405-845-686-740-793-003-233-805-002-861-533-717+",
        "scope": "all_002_only",
        "source_volume": "india",
        "leaf": 131,
        "printed_page": "96",
        "source_heading": "MOHENJO-DARO 391-396 SEALS no iconography III",
        "panels": [
            {"side": "A", "box": (105, 150, 925, 460)},
            {"side": "a", "box": (105, 540, 940, 850)},
        ],
        "route_status": "source_visible_this_campaign",
    },
    {
        "cisi": "M-714",
        "object_id": "3139.1",
        "tail_family": "603",
        "text": "+740-585-017-033-705-233-798-803-002-861-603+",
        "scope": "all_002_only",
        "source_volume": "pakistan",
        "leaf": 79,
        "printed_page": "45",
        "source_heading": "MOHENJO-DARO 712-714 SEALS unicorn III",
        "panels": [
            {"side": "A", "box": (215, 3260, 1600, 4210)},
            {"side": "a", "box": (1650, 3260, 3000, 4210)},
        ],
        "route_status": "source_visible_this_campaign",
    },
    {
        "cisi": "M-1273",
        "object_id": "3580.1",
        "tail_family": "603",
        "text": "+740-055-002-861-603+",
        "scope": "all_002_only",
        "source_volume": "pakistan",
        "leaf": 195,
        "printed_page": "161",
        "source_heading": "MOHENJO-DARO 1269-1274 SEALS no iconography II",
        "panels": [
            {"side": "A", "box": (150, 3240, 1420, 3820)},
            {"side": "a", "box": (145, 3880, 1420, 4520)},
        ],
        "route_status": "source_visible_this_campaign",
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
    if target.exists():
        return target
    with urllib.request.urlopen(direct_url(volume, leaf)) as response, target.open("wb") as handle:
        shutil.copyfileobj(response, handle)
    return target


def load_metadata() -> dict[str, dict[str, str]]:
    with METADATA.open(newline="", encoding="utf-8") as handle:
        return {row["id"]: row for row in csv.DictReader(handle)}


def load_861_rows(dedup: bool) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen = set()
    suffix = "strict_dedup" if dedup else "strict_raw"
    for path, base_scope in ((ALL_002, "all_002"), (AFTER_032, "after_032")):
        scope = f"{base_scope}_{suffix}"
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                if row.get("strict_complete_closed") != "true":
                    continue
                tokens = row["text_dedup_key"].split()
                idx_002 = int(row["idx_002"])
                if idx_002 + 1 >= len(tokens) or tokens[idx_002 + 1] != "861":
                    continue
                key = (scope, row["text_dedup_key"], row.get("site"), row.get("type"), row.get("idx_002"))
                if dedup and key in seen:
                    continue
                seen.add(key)
                prefix = tokens[:idx_002]
                tail = tokens[idx_002 + 2 :]
                out = {
                    "scope": scope,
                    "id": row["id"],
                    "cisi": row["cisi"],
                    "site": row["site"],
                    "type": row["type"],
                    "symbol": row["symbol"],
                    "frame_kind": row.get("frame_kind", ""),
                    "text": row["text"],
                    "prefix_before_002": " ".join(prefix),
                    "prefix_last1": prefix[-1] if prefix else "<START>",
                    "prefix_last2": " ".join(prefix[-2:]) if len(prefix) >= 2 else " ".join(prefix) or "<START>",
                    "idx_002": row["idx_002"],
                    "tail_len": str(len(tail)),
                    "tail_next1": tail[0] if tail else "<END>",
                    "tail_full": " ".join(tail) if tail else "<END>",
                    "terminal_861": str(not tail).lower(),
                }
                rows.append(out)
    return rows


def family_summary(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["scope"], row["tail_full"])].append(row)

    out = []
    for (scope, tail), members in sorted(grouped.items(), key=lambda kv: (kv[0][0], kv[0][1] != "<END>", -len(kv[1]), kv[0][1])):
        out.append(
            {
                "scope": scope,
                "tail_full": tail,
                "rows": str(len(members)),
                "terminal": str(tail == "<END>").lower(),
                "sites": ";".join(f"{k}:{v}" for k, v in Counter(m["site"] for m in members).most_common()),
                "types": ";".join(f"{k}:{v}" for k, v in Counter(m["type"] for m in members).most_common()),
                "symbols": ";".join(f"{k}:{v}" for k, v in Counter(m["symbol"] for m in members).most_common()),
                "prefix_last2": ";".join(f"{k}:{v}" for k, v in Counter(m["prefix_last2"] for m in members).most_common(8)),
                "examples": ";".join(f"{m['cisi']} {m['text']}" for m in members[:10]),
            }
        )
    return out


def contrast_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out = []
    for field in ("prefix_before_002", "prefix_last2", "prefix_last1"):
        grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
        for row in rows:
            grouped[(row["scope"], row[field])].append(row)
        for (scope, key), members in sorted(grouped.items()):
            terminal = [m for m in members if m["tail_full"] == "<END>"]
            continuing = [m for m in members if m["tail_full"] != "<END>"]
            if not terminal or not continuing:
                continue
            out.append(
                {
                    "scope": scope,
                    "contrast_field": field,
                    "contrast_key": key,
                    "terminal_rows": str(len(terminal)),
                    "continuing_rows": str(len(continuing)),
                    "terminal_examples": ";".join(f"{m['cisi']} {m['text']}" for m in terminal[:6]),
                    "continuing_examples": ";".join(f"{m['cisi']} {m['tail_full']} {m['text']}" for m in continuing[:6]),
                }
            )
    return out


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def crop_focus_pages() -> tuple[list[dict[str, str]], Path | None]:
    crop_rows: list[dict[str, str]] = []
    for route in FOCUS_ROUTES:
        if not route["panels"]:
            continue
        source = fetch_page(route["source_volume"], route["leaf"])
        image = Image.open(source).convert("RGB")
        for panel in route["panels"]:
            side = panel["side"]
            side_slug = "face_A" if side == "A" else "impression_a"
            box = panel["box"]
            crop = image.crop(box)
            out_path = OUT / f"{route['cisi'].replace('-', '')}_{side_slug}_cisi_{route['source_volume']}_n{route['leaf']:03d}.png"
            crop.save(out_path)
            crop_rows.append(
                {
                    "cisi": route["cisi"],
                    "object_id": route["object_id"],
                    "side": side,
                    "tail_family": route["tail_family"],
                    "text": route["text"],
                    "source_volume": route["source_volume"],
                    "leaf": str(route["leaf"]),
                    "source_image_abs": str(source.resolve()),
                    "crop_box": json.dumps(box),
                    "crop_abs": str(out_path.resolve()),
                }
            )

    if not crop_rows:
        return crop_rows, None

    try:
        font = ImageFont.truetype("arial.ttf", 22)
        small = ImageFont.truetype("arial.ttf", 16)
    except Exception:
        font = ImageFont.load_default()
        small = font

    thumbs = []
    for row in crop_rows:
        im = Image.open(row["crop_abs"]).convert("RGB")
        im.thumbnail((760, 300))
        thumbs.append((row, im.copy()))

    pad = 24
    width = 1640
    block_h = 390
    height = pad + ((len(thumbs) + 1) // 2) * block_h
    sheet = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (row, im) in enumerate(thumbs):
        col = i % 2
        x = pad + col * 810
        y = pad + (i // 2) * block_h
        draw.text((x, y), f"{row['cisi']} {row['side']}  861->{row['tail_family']}", fill=(0, 0, 0), font=font)
        draw.text((x, y + 30), row["text"], fill=(45, 45, 45), font=small)
        sheet.paste(im, (x, y + 62))

    contact = OUT / "032_002_861_suffix_split_source_contact_sheet.png"
    sheet.save(contact)
    return crop_rows, contact


def route_rows(metadata: dict[str, dict[str, str]]) -> list[dict[str, str]]:
    out = []
    for route in FOCUS_ROUTES:
        meta = metadata.get(route["object_id"], {})
        source_path = fetch_page(route["source_volume"], route["leaf"])
        out.append(
            {
                "cisi": route["cisi"],
                "object_id": route["object_id"],
                "tail_family": route["tail_family"],
                "text": route["text"],
                "scope": route["scope"],
                "route_status": route["route_status"],
                "source_volume": route["source_volume"],
                "ia_leaf": f"n{route['leaf']}",
                "printed_page": route["printed_page"],
                "source_heading": route["source_heading"],
                "reader_url": reader_url(route["source_volume"], route["leaf"]),
                "direct_image_url": direct_url(route["source_volume"], route["leaf"]),
                "source_image_abs": str(source_path.resolve()),
                "site": meta.get("site", ""),
                "area_section": meta.get("area-section", ""),
                "room_grid": meta.get("room-grid", ""),
                "excavation_idno": meta.get("excavation-idno", ""),
                "period": " ".join(p for p in (meta.get("time", ""), meta.get("period", ""), meta.get("phase", "")) if p and p != "-"),
                "depth": meta.get("depth", ""),
                "shape": meta.get("shape", ""),
                "symbol": meta.get("symbol", ""),
                "type": meta.get("type", ""),
                "direction": meta.get("dir.", ""),
            }
        )
    return out


def main() -> None:
    metadata = load_metadata()
    rows = load_861_rows(dedup=True)
    raw_rows = load_861_rows(dedup=False)
    families = family_summary(rows)
    raw_families = family_summary(raw_rows)
    contrasts = contrast_rows(rows)
    routes = route_rows(metadata)
    crop_rows, contact_sheet = crop_focus_pages()

    rows_csv = REPORTS / "campaign_032_002_861_suffix_split_rows.csv"
    raw_rows_csv = REPORTS / "campaign_032_002_861_suffix_split_raw_rows.csv"
    families_csv = REPORTS / "campaign_032_002_861_suffix_split_families.csv"
    raw_families_csv = REPORTS / "campaign_032_002_861_suffix_split_raw_families.csv"
    contrasts_csv = REPORTS / "campaign_032_002_861_suffix_split_contrasts.csv"
    routes_csv = REPORTS / "campaign_032_002_861_suffix_split_source_routes.csv"
    crops_csv = REPORTS / "campaign_032_002_861_suffix_split_source_crops.csv"
    summary_json = REPORTS / "campaign_032_002_861_suffix_split_summary.json"

    row_fields = [
        "scope",
        "id",
        "cisi",
        "site",
        "type",
        "symbol",
        "frame_kind",
        "text",
        "prefix_before_002",
        "prefix_last1",
        "prefix_last2",
        "idx_002",
        "tail_len",
        "tail_next1",
        "tail_full",
        "terminal_861",
    ]
    write_csv(rows_csv, rows, row_fields)
    write_csv(raw_rows_csv, raw_rows, row_fields)
    write_csv(families_csv, families, ["scope", "tail_full", "rows", "terminal", "sites", "types", "symbols", "prefix_last2", "examples"])
    write_csv(raw_families_csv, raw_families, ["scope", "tail_full", "rows", "terminal", "sites", "types", "symbols", "prefix_last2", "examples"])
    write_csv(
        contrasts_csv,
        contrasts,
        ["scope", "contrast_field", "contrast_key", "terminal_rows", "continuing_rows", "terminal_examples", "continuing_examples"],
    )
    write_csv(
        routes_csv,
        routes,
        [
            "cisi",
            "object_id",
            "tail_family",
            "text",
            "scope",
            "route_status",
            "source_volume",
            "ia_leaf",
            "printed_page",
            "source_heading",
            "reader_url",
            "direct_image_url",
            "source_image_abs",
            "site",
            "area_section",
            "room_grid",
            "excavation_idno",
            "period",
            "depth",
            "shape",
            "symbol",
            "type",
            "direction",
        ],
    )
    if crop_rows:
        write_csv(crops_csv, crop_rows, ["cisi", "object_id", "side", "tail_family", "text", "source_volume", "leaf", "source_image_abs", "crop_box", "crop_abs"])

    all_rows = [r for r in rows if r["scope"] == "all_002_strict_dedup"]
    after_rows = [r for r in rows if r["scope"] == "after_032_strict_dedup"]
    all_cont = [r for r in all_rows if r["tail_full"] != "<END>"]
    after_cont = [r for r in after_rows if r["tail_full"] != "<END>"]
    raw_all_rows = [r for r in raw_rows if r["scope"] == "all_002_strict_raw"]
    raw_after_rows = [r for r in raw_rows if r["scope"] == "after_032_strict_raw"]
    raw_all_cont = [r for r in raw_all_rows if r["tail_full"] != "<END>"]
    raw_after_cont = [r for r in raw_after_rows if r["tail_full"] != "<END>"]
    summary = {
        "all_002_861_rows": len(all_rows),
        "all_002_861_terminal": sum(1 for r in all_rows if r["tail_full"] == "<END>"),
        "all_002_861_continuing": len(all_cont),
        "after_032_861_rows": len(after_rows),
        "after_032_861_terminal": sum(1 for r in after_rows if r["tail_full"] == "<END>"),
        "after_032_861_continuing": len(after_cont),
        "raw_all_002_861_rows": len(raw_all_rows),
        "raw_all_002_861_terminal": sum(1 for r in raw_all_rows if r["tail_full"] == "<END>"),
        "raw_all_002_861_continuing": len(raw_all_cont),
        "raw_after_032_861_rows": len(raw_after_rows),
        "raw_after_032_861_terminal": sum(1 for r in raw_after_rows if r["tail_full"] == "<END>"),
        "raw_after_032_861_continuing": len(raw_after_cont),
        "repeated_nonterminal_families_all_002": [
            {"tail_full": row["tail_full"], "rows": int(row["rows"]), "examples": row["examples"]}
            for row in families
            if row["scope"] == "all_002_strict_dedup" and row["tail_full"] != "<END>" and int(row["rows"]) > 1
        ],
        "raw_repeated_nonterminal_families_all_002": [
            {"tail_full": row["tail_full"], "rows": int(row["rows"]), "examples": row["examples"]}
            for row in raw_families
            if row["scope"] == "all_002_strict_raw" and row["tail_full"] != "<END>" and int(row["rows"]) > 1
        ],
        "key_contrast": [
            row
            for row in contrasts
            if row["scope"] == "after_032_strict_dedup" and row["contrast_field"] == "prefix_last2" and row["contrast_key"] == "220 032"
        ],
        "rows_csv": str(rows_csv.resolve()),
        "raw_rows_csv": str(raw_rows_csv.resolve()),
        "families_csv": str(families_csv.resolve()),
        "raw_families_csv": str(raw_families_csv.resolve()),
        "contrasts_csv": str(contrasts_csv.resolve()),
        "routes_csv": str(routes_csv.resolve()),
        "crops_csv": str(crops_csv.resolve()) if crop_rows else "",
        "contact_sheet": str(contact_sheet.resolve()) if contact_sheet else "",
    }
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
