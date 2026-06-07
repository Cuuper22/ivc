from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageOps


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
TMP = ROOT / "tmp" / "002_y_branch_gap_public_source_acquisition"
PAGES = TMP / "pages"
CROPS = TMP / "crops"

QUEUE = REPORTS / "campaign_002_y_partition_source_queue.csv"
OUT_ROUTES = REPORTS / "campaign_002_y_branch_gap_public_routes.csv"
OUT_STATUS = REPORTS / "campaign_002_y_branch_gap_public_source_status.csv"
OUT_SUMMARY = REPORTS / "campaign_002_y_branch_gap_public_source_summary.json"
CONTACT_SHEET = TMP / "campaign_002_y_branch_gap_public_source_contact_sheet.jpg"

RUN_DATE = "2026-05-29"
GAP_SIGNS = {"368", "031", "220"}
UNKNOWN_CISI = {"", "NA", "-", "?", "?-3"}

IA_ROOT = (
    "https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/"
)

VOLUMES = [
    {
        "volume": "cisi_india",
        "xml": ROOT
        / "tmp"
        / "cisi_xml"
        / "Corpus of Indus Seals and Inscriptions. Collections in India_djvu.xml",
        "base": IA_ROOT
        + "Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India/page/",
    },
    {
        "volume": "cisi_pakistan",
        "xml": ROOT
        / "tmp"
        / "cisi_xml"
        / "Corpus of Indus Seals and Inscriptions. Collections in Pakistan_djvu.xml",
        "base": IA_ROOT
        + "Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/",
    },
]

ROUTE_FIELDS = [
    "date",
    "route_rank",
    "priority_rank",
    "y_after_002",
    "cisi",
    "id",
    "site",
    "type",
    "symbol",
    "text",
    "volume",
    "page_index",
    "page_file",
    "source_url",
    "route_status",
    "source_grade_status",
    "match_text",
    "ocr_label_coords",
    "local_page_path",
    "local_context_crop",
    "local_enhanced_crop",
    "source_image_sha256",
    "crop_sha256",
    "enhanced_crop_sha256",
    "image_width",
    "image_height",
    "crop_box_image_coords",
    "notes",
    "accepted_claims_increment",
]

STATUS_FIELDS = [
    "date",
    "priority_rank",
    "y_after_002",
    "cisi",
    "id",
    "site",
    "type",
    "symbol",
    "text",
    "route_count",
    "best_volume",
    "best_page_index",
    "best_source_url",
    "best_local_artifact",
    "best_artifact_sha256",
    "source_status_rank",
    "current_admissible_use",
    "blocker",
    "next_action",
    "accepted_claims_increment",
]


def ensure_dirs() -> None:
    PAGES.mkdir(parents=True, exist_ok=True)
    CROPS.mkdir(parents=True, exist_ok=True)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm_token(value: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", value.upper())


def page_index_from_usemap(usemap: str) -> int:
    match = re.search(r"_(\d+)\.djvu", usemap)
    return int(match.group(1)) if match else -1


def parse_attrs(text: str) -> dict[str, str]:
    return {key: html.unescape(value) for key, value in re.findall(r'(\w+)="([^"]*)"', text)}


def parse_word_box(coords: str) -> tuple[int, int, int, int]:
    values = [int(v) for v in coords.split(",") if v.strip()]
    if len(values) == 4:
        x1, y1, x2, y2 = values
        return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
    if len(values) >= 5:
        x1 = min(values[0], values[2])
        x2 = max(values[0], values[2])
        ys = values[1:]
        return x1, min(ys), x2, max(ys)
    raise ValueError(f"Unsupported WORD coords: {coords}")


def parse_volume_pages(volume: dict[str, object]) -> list[dict[str, object]]:
    text = Path(volume["xml"]).read_text(encoding="utf-8", errors="ignore")
    pages = []
    for object_match in re.finditer(r"<OBJECT\b(?P<attrs>.*?)>(?P<body>.*?)</OBJECT>", text, flags=re.S):
        attrs = parse_attrs(object_match.group("attrs"))
        usemap = attrs.get("usemap", "")
        if not usemap:
            continue
        words = []
        for word_match in re.finditer(r'<WORD\s+coords="([^"]+)">(.*?)</WORD>', object_match.group("body"), flags=re.S):
            raw = html.unescape(re.sub(r"<.*?>", "", word_match.group(2))).strip()
            if not raw:
                continue
            words.append(
                {
                    "text": raw,
                    "norm": norm_token(raw),
                    "box": parse_word_box(word_match.group(1)),
                }
            )
        pages.append(
            {
                "volume": volume["volume"],
                "base": volume["base"],
                "page_index": page_index_from_usemap(usemap),
                "page_file": usemap,
                "width": int(attrs.get("width", "0")),
                "height": int(attrs.get("height", "0")),
                "words": words,
            }
        )
    return pages


def clean_exact_label_match(raw_parts: list[str], words: list[dict[str, object]], end_index: int) -> bool:
    raw_text = " ".join(raw_parts)
    if "*" in raw_text:
        return False
    next_word = words[end_index + 1]["norm"] if end_index + 1 < len(words) else ""
    if next_word[:1].isdigit():
        return False
    return True


def find_label_matches(target: str, pages: list[dict[str, object]]) -> list[dict[str, object]]:
    target_norm = norm_token(target)
    matches = []
    for page in pages:
        words = page["words"]
        for i in range(len(words)):
            combined = ""
            raw_parts = []
            boxes = []
            for j in range(i, min(i + 4, len(words))):
                combined += words[j]["norm"]
                raw_parts.append(words[j]["text"])
                boxes.append(words[j]["box"])
                if combined == target_norm and clean_exact_label_match(raw_parts, words, j):
                    x1 = min(box[0] for box in boxes)
                    y1 = min(box[1] for box in boxes)
                    x2 = max(box[2] for box in boxes)
                    y2 = max(box[3] for box in boxes)
                    matches.append(
                        {
                            "volume": page["volume"],
                            "base": page["base"],
                            "page_index": page["page_index"],
                            "page_file": page["page_file"],
                            "xml_width": page["width"],
                            "xml_height": page["height"],
                            "match_text": " ".join(raw_parts),
                            "label_box_xml": [x1, y1, x2, y2],
                        }
                    )
                    break
                if len(combined) > len(target_norm) + 4:
                    break
    return matches


def expected_volumes(cisi: str) -> set[str]:
    match = re.match(r"^([A-Za-z]+)-?(\d+)", cisi)
    if not match:
        return {"cisi_india", "cisi_pakistan"}
    prefix = match.group(1).upper()
    number = int(match.group(2))
    if prefix == "H":
        return {"cisi_pakistan"}
    if prefix in {"K", "B"}:
        return {"cisi_india"}
    if prefix == "BLK":
        return {"cisi_pakistan"}
    if prefix == "M":
        if number <= 381:
            return {"cisi_india"}
        if 595 <= number <= 1659:
            return {"cisi_pakistan"}
        return set()
    return {"cisi_india", "cisi_pakistan"}


def match_score(match: dict[str, object]) -> tuple[int, int]:
    page_index = int(match["page_index"])
    # In both public CISI 1/2 scans, the late pages are mostly registers/data.
    likely_plate = 1 if 20 <= page_index <= 390 else 0
    return (-likely_plate, page_index)


def source_url(match: dict[str, object]) -> str:
    return f"{match['base']}n{int(match['page_index'])}_w2000.jpg"


def download(url: str, path: Path) -> None:
    if path.exists() and path.stat().st_size:
        return
    request = urllib.request.Request(url, headers={"User-Agent": "codex-ivc-002-y-branch-gap/2026-05-29"})
    with urllib.request.urlopen(request, timeout=90) as response:
        path.write_bytes(response.read())


def scale_box(label_box: list[int], xml_width: int, xml_height: int, image_width: int, image_height: int) -> list[int]:
    sx = image_width / xml_width if xml_width else 1
    sy = image_height / xml_height if xml_height else 1
    x1, y1, x2, y2 = label_box
    return [round(x1 * sx), round(y1 * sy), round(x2 * sx), round(y2 * sy)]


def context_crop_box(label_box: list[int], image_width: int, image_height: int) -> list[int]:
    x1, y1, x2, y2 = label_box
    return [
        max(0, x1 - 520),
        max(0, y1 - 760),
        min(image_width, x2 + 620),
        min(image_height, y2 + 260),
    ]


def build_crop(target: dict[str, str], match: dict[str, object], route_rank: int) -> dict[str, object]:
    url = source_url(match)
    slug = re.sub(r"[^A-Za-z0-9]+", "_", f"{target['cisi']}_{match['volume']}_n{match['page_index']}_{route_rank}").strip("_")
    page_path = PAGES / f"{slug}.jpg"
    download(url, page_path)
    image_sha = sha256_file(page_path)
    image = Image.open(page_path).convert("RGB")
    image_width, image_height = image.size
    label_box = scale_box(
        match["label_box_xml"],
        int(match["xml_width"]),
        int(match["xml_height"]),
        image_width,
        image_height,
    )
    crop_box = context_crop_box(label_box, image_width, image_height)
    crop = image.crop(crop_box)
    draw = ImageDraw.Draw(crop)
    draw.rectangle(
        [
            label_box[0] - crop_box[0],
            label_box[1] - crop_box[1],
            label_box[2] - crop_box[0],
            label_box[3] - crop_box[1],
        ],
        outline=(255, 0, 0),
        width=3,
    )
    crop_path = CROPS / f"{slug}_context.jpg"
    crop.save(crop_path, quality=92)
    enhanced = ImageOps.autocontrast(crop.convert("L")).resize((crop.width * 2, crop.height * 2))
    enhanced_path = CROPS / f"{slug}_context_enhanced_x2.jpg"
    enhanced.save(enhanced_path, quality=92)

    source_grade_status = (
        "public_cisi_plate_route_candidate_needs_visual_token_boxing"
        if 20 <= int(match["page_index"]) <= 390
        else "public_cisi_late_register_or_data_route_not_source_panel"
    )
    return {
        "date": RUN_DATE,
        "route_rank": route_rank,
        "priority_rank": target["rank"],
        "y_after_002": target["y_after_002"],
        "cisi": target["cisi"],
        "id": target["id"],
        "site": target["site"],
        "type": target["type"],
        "symbol": target["symbol"],
        "text": target["text"],
        "volume": match["volume"],
        "page_index": match["page_index"],
        "page_file": match["page_file"],
        "source_url": url,
        "route_status": "downloaded_and_cropped",
        "source_grade_status": source_grade_status,
        "match_text": match["match_text"],
        "ocr_label_coords": "|".join(str(v) for v in match["label_box_xml"]),
        "local_page_path": str(page_path.relative_to(ROOT)).replace("\\", "/"),
        "local_context_crop": str(crop_path.relative_to(ROOT)).replace("\\", "/"),
        "local_enhanced_crop": str(enhanced_path.relative_to(ROOT)).replace("\\", "/"),
        "source_image_sha256": image_sha,
        "crop_sha256": sha256_file(crop_path),
        "enhanced_crop_sha256": sha256_file(enhanced_path),
        "image_width": image_width,
        "image_height": image_height,
        "crop_box_image_coords": "|".join(str(v) for v in crop_box),
        "notes": "OCR-label public page route and broad context crop only; not token-boxed, not physical direction, not sign identity.",
        "accepted_claims_increment": 0,
    }


def target_rows() -> list[dict[str, str]]:
    rows = []
    for row in parse_csv(QUEUE):
        if row["partition_class"] != "posthoc_branch_pole":
            continue
        if row["y_after_002"] not in GAP_SIGNS:
            continue
        row["cisi"] = row["cisi"].strip()
        rows.append(row)
    return rows


def status_for(target: dict[str, str], routes: list[dict[str, object]]) -> dict[str, object]:
    if target["cisi"] in UNKNOWN_CISI:
        return {
            "date": RUN_DATE,
            "priority_rank": target["rank"],
            "y_after_002": target["y_after_002"],
            "cisi": target["cisi"],
            "id": target["id"],
            "site": target["site"],
            "type": target["type"],
            "symbol": target["symbol"],
            "text": target["text"],
            "route_count": 0,
            "best_volume": "",
            "best_page_index": "",
            "best_source_url": "",
            "best_local_artifact": "",
            "best_artifact_sha256": "",
            "source_status_rank": "blocked_until_object_id_resolved",
            "current_admissible_use": "not_admissible",
            "blocker": "No stable public CISI object id in this row.",
            "next_action": "Resolve object identity before source routing.",
            "accepted_claims_increment": 0,
        }
    if not routes:
        return {
            "date": RUN_DATE,
            "priority_rank": target["rank"],
            "y_after_002": target["y_after_002"],
            "cisi": target["cisi"],
            "id": target["id"],
            "site": target["site"],
            "type": target["type"],
            "symbol": target["symbol"],
            "text": target["text"],
            "route_count": 0,
            "best_volume": "",
            "best_page_index": "",
            "best_source_url": "",
            "best_local_artifact": "",
            "best_artifact_sha256": "",
            "source_status_rank": "not_found_in_public_cisi_ocr_layer",
            "current_admissible_use": "not_admissible",
            "blocker": "No exact public CISI OCR label found in accessible India/Pakistan XML.",
            "next_action": "Try CISI 3.1, HARP, museum/archive, or non-OCR page-range routing.",
            "accepted_claims_increment": 0,
        }

    best = sorted(routes, key=lambda r: (0 if "plate_route" in r["source_grade_status"] else 1, int(r["page_index"])))[0]
    is_plate = "plate_route" in best["source_grade_status"]
    return {
        "date": RUN_DATE,
        "priority_rank": target["rank"],
        "y_after_002": target["y_after_002"],
        "cisi": target["cisi"],
        "id": target["id"],
        "site": target["site"],
        "type": target["type"],
        "symbol": target["symbol"],
        "text": target["text"],
        "route_count": len(routes),
        "best_volume": best["volume"],
        "best_page_index": best["page_index"],
        "best_source_url": best["source_url"],
        "best_local_artifact": best["local_enhanced_crop"],
        "best_artifact_sha256": best["enhanced_crop_sha256"],
        "source_status_rank": "public_cisi_plate_route_candidate" if is_plate else "public_cisi_route_not_source_panel",
        "current_admissible_use": "source_route_inventory_only",
        "blocker": "Needs visual source-panel review, token boxing, side/direction check, and matched negatives before source-normalized evidence.",
        "next_action": "Review enhanced crop and build a blind token-box packet only if the signband is actually visible.",
        "accepted_claims_increment": 0,
    }


def make_contact_sheet(status_rows: list[dict[str, object]]) -> None:
    ready = [row for row in status_rows if row["best_local_artifact"]]
    if not ready:
        return
    thumbs = []
    for row in ready:
        artifact = ROOT / str(row["best_local_artifact"])
        image = Image.open(artifact).convert("RGB")
        image.thumbnail((620, 420))
        canvas = Image.new("RGB", (680, 520), "white")
        canvas.paste(image, ((680 - image.width) // 2, 20))
        draw = ImageDraw.Draw(canvas)
        draw.text((20, 450), f"{row['cisi']} y={row['y_after_002']} {row['best_volume']} n{row['best_page_index']}", fill=(0, 0, 0))
        draw.text((20, 475), str(row["text"])[:90], fill=(30, 30, 30))
        thumbs.append(canvas)
    cols = 2
    sheet = Image.new("RGB", (cols * 680, ((len(thumbs) + cols - 1) // cols) * 520), "white")
    for i, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((i % cols) * 680, (i // cols) * 520))
    sheet.save(CONTACT_SHEET, quality=92)


def main() -> None:
    ensure_dirs()
    targets = target_rows()
    pages = []
    for volume in VOLUMES:
        pages.extend(parse_volume_pages(volume))

    routes_by_cisi: dict[str, list[dict[str, object]]] = {}
    route_rows = []
    for target in targets:
        if target["cisi"] in UNKNOWN_CISI:
            routes_by_cisi[target["cisi"]] = []
            continue
        allowed_volumes = expected_volumes(target["cisi"])
        matches = [
            match
            for match in find_label_matches(target["cisi"], pages)
            if match["volume"] in allowed_volumes
        ]
        matches = sorted(matches, key=match_score)[:3]
        built_routes = []
        for route_rank, match in enumerate(matches, start=1):
            try:
                built = build_crop(target, match, route_rank)
            except Exception as exc:
                built = {
                    "date": RUN_DATE,
                    "route_rank": route_rank,
                    "priority_rank": target["rank"],
                    "y_after_002": target["y_after_002"],
                    "cisi": target["cisi"],
                    "id": target["id"],
                    "site": target["site"],
                    "type": target["type"],
                    "symbol": target["symbol"],
                    "text": target["text"],
                    "volume": match["volume"],
                    "page_index": match["page_index"],
                    "page_file": match["page_file"],
                    "source_url": source_url(match),
                    "route_status": f"download_failed:{type(exc).__name__}",
                    "source_grade_status": "route_failed_not_source_grade",
                    "match_text": match["match_text"],
                    "ocr_label_coords": "|".join(str(v) for v in match["label_box_xml"]),
                    "local_page_path": "",
                    "local_context_crop": "",
                    "local_enhanced_crop": "",
                    "source_image_sha256": "",
                    "crop_sha256": "",
                    "enhanced_crop_sha256": "",
                    "image_width": "",
                    "image_height": "",
                    "crop_box_image_coords": "",
                    "notes": str(exc),
                    "accepted_claims_increment": 0,
                }
            route_rows.append(built)
            if built["route_status"] == "downloaded_and_cropped":
                built_routes.append(built)
        routes_by_cisi[target["cisi"]] = built_routes

    status_rows = [status_for(target, routes_by_cisi.get(target["cisi"], [])) for target in targets]
    make_contact_sheet(status_rows)

    write_csv(OUT_ROUTES, route_rows, ROUTE_FIELDS)
    write_csv(OUT_STATUS, status_rows, STATUS_FIELDS)

    by_sign: dict[str, dict[str, int]] = {}
    for target in targets:
        rec = by_sign.setdefault(target["y_after_002"], {"target_rows": 0, "route_candidates": 0, "object_id_blocked": 0})
        rec["target_rows"] += 1
    for status in status_rows:
        rec = by_sign[status["y_after_002"]]
        if status["source_status_rank"] == "public_cisi_plate_route_candidate":
            rec["route_candidates"] += 1
        if status["source_status_rank"] == "blocked_until_object_id_resolved":
            rec["object_id_blocked"] += 1

    summary = {
        "date": RUN_DATE,
        "purpose": "Public CISI OCR/page-route acquisition for branch-pole gap signs in the broad all-002 post-hoc partition.",
        "scope": "Rows from campaign_002_y_partition_source_queue.csv with partition_class=posthoc_branch_pole and y_after_002 in 368/031/220.",
        "counts": {
            "target_rows": len(targets),
            "route_rows": len(route_rows),
            "public_cisi_plate_route_candidates": sum(
                1 for row in status_rows if row["source_status_rank"] == "public_cisi_plate_route_candidate"
            ),
            "not_found_or_blocked": sum(
                1 for row in status_rows if row["source_status_rank"] != "public_cisi_plate_route_candidate"
            ),
            "accepted_claims_increment": 0,
        },
        "by_sign": by_sign,
        "interpretation_boundary": "These are source-route candidates only. They do not validate source-normalized token order, physical direction, sign identity, sign meaning, phonetic value, language family, or translation.",
        "files": {
            "routes_csv": str(OUT_ROUTES.relative_to(ROOT)).replace("\\", "/"),
            "status_csv": str(OUT_STATUS.relative_to(ROOT)).replace("\\", "/"),
            "summary_json": str(OUT_SUMMARY.relative_to(ROOT)).replace("\\", "/"),
            "contact_sheet": str(CONTACT_SHEET.relative_to(ROOT)).replace("\\", "/") if CONTACT_SHEET.exists() else "",
            "page_dir": str(PAGES.relative_to(ROOT)).replace("\\", "/"),
            "crop_dir": str(CROPS.relative_to(ROOT)).replace("\\", "/"),
        },
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
