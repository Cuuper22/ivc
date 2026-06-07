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
RUN_DATE = "2026-05-29"
PROBE_ID = "directionality_public_route_probe_v1"

REPORTS = ROOT / "data" / "open_prototype" / "reports"
QUEUE = REPORTS / "effective_unicity_directionality_source_queue.csv"
TMP = ROOT / "tmp" / "effective_unicity_directionality_public_route_probe"
PAGES = TMP / "pages"
CROPS = TMP / "crops"

OUT_ROUTES = REPORTS / "effective_unicity_directionality_public_route_probe_routes.csv"
OUT_STATUS = REPORTS / "effective_unicity_directionality_public_route_probe_status.csv"
OUT_SUMMARY = REPORTS / "effective_unicity_directionality_public_route_probe_summary.json"
CONTACT_SHEET = TMP / "directionality_public_route_probe_contact_sheet.jpg"

TOP_N = 80

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
    "probe_id",
    "route_rank",
    "queue_rank",
    "priority_band",
    "source_validation_need",
    "direction_outcome",
    "representative_cisi",
    "family_cisis",
    "representative_lipi_id",
    "site",
    "type",
    "symbol",
    "direction",
    "text",
    "tokens",
    "diff_per_transition",
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
    "probe_id",
    "queue_rank",
    "priority_band",
    "source_validation_need",
    "direction_outcome",
    "representative_cisi",
    "family_cisis",
    "representative_lipi_id",
    "site",
    "type",
    "symbol",
    "direction",
    "text",
    "tokens",
    "diff_per_transition",
    "route_count",
    "plate_route_count",
    "data_route_count",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
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
            if raw:
                words.append({"text": raw, "norm": norm_token(raw), "box": parse_word_box(word_match.group(1))})
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
                    matches.append(
                        {
                            "volume": page["volume"],
                            "base": page["base"],
                            "page_index": page["page_index"],
                            "page_file": page["page_file"],
                            "xml_width": page["width"],
                            "xml_height": page["height"],
                            "match_text": " ".join(raw_parts),
                            "label_box_xml": [
                                min(box[0] for box in boxes),
                                min(box[1] for box in boxes),
                                max(box[2] for box in boxes),
                                max(box[3] for box in boxes),
                            ],
                        }
                    )
                    break
                if len(combined) > len(target_norm) + 4:
                    break
    return matches


def likely_expected_volume(cisi: str) -> set[str]:
    match = re.match(r"^([A-Za-z]+)-?(\d+)", cisi)
    if not match:
        return {"cisi_india", "cisi_pakistan"}
    prefix = match.group(1).upper()
    number = int(match.group(2))
    if prefix == "H":
        return {"cisi_pakistan"}
    if prefix in {"K", "B"}:
        return {"cisi_india"}
    if prefix == "M":
        if number <= 381:
            return {"cisi_india"}
        if 595 <= number <= 1659:
            return {"cisi_pakistan"}
    return {"cisi_india", "cisi_pakistan"}


def source_url(match: dict[str, object]) -> str:
    return f"{match['base']}n{int(match['page_index'])}_w2000.jpg"


def download(url: str, path: Path) -> None:
    if path.exists() and path.stat().st_size:
        return
    request = urllib.request.Request(url, headers={"User-Agent": "codex-ivc-directionality-route-probe/2026-05-29"})
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
        max(0, x1 - 560),
        max(0, y1 - 820),
        min(image_width, x2 + 720),
        min(image_height, y2 + 360),
    ]


def source_grade(match: dict[str, object], expected: set[str]) -> str:
    page_index = int(match["page_index"])
    if page_index > 390:
        return "public_cisi_late_register_or_data_route_not_source_panel"
    if match["volume"] not in expected:
        return "public_cisi_plate_route_candidate_volume_mismatch_check_needed"
    return "public_cisi_plate_route_candidate_needs_visual_review"


def match_sort_key(match: dict[str, object], expected: set[str]) -> tuple[int, int, int]:
    plate_penalty = 0 if int(match["page_index"]) <= 390 else 1
    volume_penalty = 0 if match["volume"] in expected else 1
    return plate_penalty, volume_penalty, int(match["page_index"])


def target_rows() -> list[dict[str, str]]:
    rows = []
    for row in read_csv(QUEUE):
        rank = int(row["queue_rank"])
        if rank > TOP_N:
            continue
        if row["source_validation_need"] not in {
            "find_public_or_request_source_route",
            "replace_non_source_grade_catalogue_hint",
            "box_direction_from_existing_public_route",
            "request_or_locate_source_image",
        }:
            continue
        if not row["representative_cisi"]:
            continue
        rows.append(row)
    return rows


def build_crop(target: dict[str, str], match: dict[str, object], route_rank: int) -> dict[str, object]:
    cisi = target["representative_cisi"]
    url = source_url(match)
    slug = re.sub(
        r"[^A-Za-z0-9]+",
        "_",
        f"{target['queue_rank']}_{cisi}_{match['volume']}_n{match['page_index']}_{route_rank}",
    ).strip("_")
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
        width=4,
    )
    crop_path = CROPS / f"{slug}_context.jpg"
    enhanced_path = CROPS / f"{slug}_context_enhanced_x2.jpg"
    crop.save(crop_path, quality=92)
    gray = ImageOps.grayscale(crop)
    enhanced = ImageOps.autocontrast(gray, cutoff=1).resize((gray.width * 2, gray.height * 2), Image.Resampling.LANCZOS)
    enhanced.save(enhanced_path, quality=92)
    expected = likely_expected_volume(cisi)
    return {
        "date": RUN_DATE,
        "probe_id": PROBE_ID,
        "route_rank": route_rank,
        "queue_rank": target["queue_rank"],
        "priority_band": target["priority_band"],
        "source_validation_need": target["source_validation_need"],
        "direction_outcome": target["direction_outcome"],
        "representative_cisi": cisi,
        "family_cisis": target["family_cisis"],
        "representative_lipi_id": target["representative_lipi_id"],
        "site": target["site"],
        "type": target["type"],
        "symbol": target["symbol"],
        "direction": target["direction"],
        "text": target["text"],
        "tokens": target["tokens"],
        "diff_per_transition": target["diff_per_transition"],
        "volume": match["volume"],
        "page_index": match["page_index"],
        "page_file": match["page_file"],
        "source_url": url,
        "route_status": "downloaded_and_cropped",
        "source_grade_status": source_grade(match, expected),
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
        "crop_box_image_coords": "|".join(str(value) for value in crop_box),
        "notes": "OCR-exact route candidate only; red box marks label, not text. Needs visual source-panel review.",
        "accepted_claims_increment": 0,
    }


def status_for(target: dict[str, str], routes: list[dict[str, object]]) -> dict[str, object]:
    plate_routes = [
        route
        for route in routes
        if str(route["source_grade_status"]).startswith("public_cisi_plate_route_candidate")
    ]
    data_routes = [
        route
        for route in routes
        if str(route["source_grade_status"]) == "public_cisi_late_register_or_data_route_not_source_panel"
    ]
    best = sorted(plate_routes or routes, key=lambda r: (0 if r in plate_routes else 1, int(r["page_index"])))[0] if routes else None
    if not best:
        rank = "not_found_in_public_cisi_ocr_layer"
        blocker = "No exact public CISI OCR label found in accessible India/Pakistan XML for this top-ranked directionality row."
        next_action = "Try CISI 3.1, HARP, museum/archive sources, or non-OCR page-range routing."
        use = "not_admissible"
    elif plate_routes:
        rank = "public_cisi_plate_route_candidate"
        blocker = "Needs visual source-panel review, token boxing, side/direction check, and matched negatives before source-normalized evidence."
        next_action = "Review the enhanced crop/contact sheet and only then build a blind token-box packet if the signband is visible."
        use = "source_route_inventory_only"
    else:
        rank = "public_cisi_data_route_only"
        blocker = "Only late register/data OCR route found, not a source panel route."
        next_action = "Use as catalog locator only; find actual plate image before source validation."
        use = "catalog_locator_only"
    return {
        "date": RUN_DATE,
        "probe_id": PROBE_ID,
        "queue_rank": target["queue_rank"],
        "priority_band": target["priority_band"],
        "source_validation_need": target["source_validation_need"],
        "direction_outcome": target["direction_outcome"],
        "representative_cisi": target["representative_cisi"],
        "family_cisis": target["family_cisis"],
        "representative_lipi_id": target["representative_lipi_id"],
        "site": target["site"],
        "type": target["type"],
        "symbol": target["symbol"],
        "direction": target["direction"],
        "text": target["text"],
        "tokens": target["tokens"],
        "diff_per_transition": target["diff_per_transition"],
        "route_count": len(routes),
        "plate_route_count": len(plate_routes),
        "data_route_count": len(data_routes),
        "best_volume": best["volume"] if best else "",
        "best_page_index": best["page_index"] if best else "",
        "best_source_url": best["source_url"] if best else "",
        "best_local_artifact": best["local_enhanced_crop"] if best else "",
        "best_artifact_sha256": best["enhanced_crop_sha256"] if best else "",
        "source_status_rank": rank,
        "current_admissible_use": use,
        "blocker": blocker,
        "next_action": next_action,
        "accepted_claims_increment": 0,
    }


def make_contact_sheet(status_rows: list[dict[str, object]]) -> None:
    rows = [row for row in status_rows if row["source_status_rank"] == "public_cisi_plate_route_candidate"]
    if not rows:
        return
    thumbs = []
    for row in rows[:24]:
        artifact = ROOT / str(row["best_local_artifact"])
        image = Image.open(artifact).convert("RGB")
        image.thumbnail((640, 420), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (700, 540), "white")
        canvas.paste(image, ((700 - image.width) // 2, 20))
        draw = ImageDraw.Draw(canvas)
        draw.text((20, 455), f"rank {row['queue_rank']} {row['representative_cisi']} {row['site']} {row['type']}", fill=(0, 0, 0))
        draw.text((20, 480), f"{row['best_volume']} n{row['best_page_index']} diff {row['diff_per_transition']}", fill=(0, 0, 0))
        draw.text((20, 505), str(row["text"])[:95], fill=(30, 30, 30))
        thumbs.append(canvas)
    cols = 2
    sheet = Image.new("RGB", (cols * 700, ((len(thumbs) + cols - 1) // cols) * 540), "white")
    for i, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((i % cols) * 700, (i // cols) * 540))
    sheet.save(CONTACT_SHEET, quality=92)


def main() -> None:
    ensure_dirs()
    targets = target_rows()
    pages: list[dict[str, object]] = []
    for volume in VOLUMES:
        pages.extend(parse_volume_pages(volume))

    routes_by_cisi: dict[str, list[dict[str, object]]] = {}
    route_rows: list[dict[str, object]] = []
    for target in targets:
        cisi = target["representative_cisi"]
        expected = likely_expected_volume(cisi)
        matches = sorted(find_label_matches(cisi, pages), key=lambda match: match_sort_key(match, expected))[:4]
        built_routes = []
        for route_rank, match in enumerate(matches, start=1):
            try:
                built = build_crop(target, match, route_rank)
            except Exception as exc:
                built = {field: "" for field in ROUTE_FIELDS}
                built.update(
                    {
                        "date": RUN_DATE,
                        "probe_id": PROBE_ID,
                        "route_rank": route_rank,
                        "queue_rank": target["queue_rank"],
                        "priority_band": target["priority_band"],
                        "source_validation_need": target["source_validation_need"],
                        "direction_outcome": target["direction_outcome"],
                        "representative_cisi": cisi,
                        "family_cisis": target["family_cisis"],
                        "representative_lipi_id": target["representative_lipi_id"],
                        "site": target["site"],
                        "type": target["type"],
                        "symbol": target["symbol"],
                        "direction": target["direction"],
                        "text": target["text"],
                        "tokens": target["tokens"],
                        "diff_per_transition": target["diff_per_transition"],
                        "volume": match["volume"],
                        "page_index": match["page_index"],
                        "page_file": match["page_file"],
                        "source_url": source_url(match),
                        "route_status": f"download_failed:{type(exc).__name__}",
                        "source_grade_status": "route_failed_not_source_grade",
                        "match_text": match["match_text"],
                        "ocr_label_coords": "|".join(str(v) for v in match["label_box_xml"]),
                        "notes": str(exc),
                        "accepted_claims_increment": 0,
                    }
                )
            route_rows.append(built)
            if built["route_status"] == "downloaded_and_cropped":
                built_routes.append(built)
        routes_by_cisi[cisi] = built_routes

    status_rows = [status_for(target, routes_by_cisi.get(target["representative_cisi"], [])) for target in targets]
    make_contact_sheet(status_rows)

    write_csv(OUT_ROUTES, route_rows, ROUTE_FIELDS)
    write_csv(OUT_STATUS, status_rows, STATUS_FIELDS)

    by_priority: dict[str, int] = {}
    by_status: dict[str, int] = {}
    for row in status_rows:
        by_priority[row["priority_band"]] = by_priority.get(row["priority_band"], 0) + 1
        by_status[row["source_status_rank"]] = by_status.get(row["source_status_rank"], 0) + 1

    top_plate_rows = [
        {
            "queue_rank": row["queue_rank"],
            "cisi": row["representative_cisi"],
            "site": row["site"],
            "type": row["type"],
            "text": row["text"],
            "diff_per_transition": row["diff_per_transition"],
            "best_volume": row["best_volume"],
            "best_page_index": row["best_page_index"],
            "best_local_artifact": row["best_local_artifact"],
        }
        for row in status_rows
        if row["source_status_rank"] == "public_cisi_plate_route_candidate"
    ][:15]

    summary = {
        "date": RUN_DATE,
        "probe_id": PROBE_ID,
        "purpose": f"Public CISI OCR/page-route probe for the top {TOP_N} harsh directionality source-queue rows.",
        "target_selection": {
            "source_queue": str(QUEUE.relative_to(ROOT)).replace("\\", "/"),
            "top_n": TOP_N,
            "included_source_validation_needs": [
                "find_public_or_request_source_route",
                "replace_non_source_grade_catalogue_hint",
                "box_direction_from_existing_public_route",
                "request_or_locate_source_image",
            ],
        },
        "counts": {
            "target_rows": len(targets),
            "route_rows": len(route_rows),
            "targets_with_any_route": sum(1 for row in status_rows if int(row["route_count"]) > 0),
            "targets_with_plate_route_candidate": sum(
                1 for row in status_rows if row["source_status_rank"] == "public_cisi_plate_route_candidate"
            ),
            "targets_with_data_route_only": sum(
                1 for row in status_rows if row["source_status_rank"] == "public_cisi_data_route_only"
            ),
            "targets_not_found": sum(
                1 for row in status_rows if row["source_status_rank"] == "not_found_in_public_cisi_ocr_layer"
            ),
            "accepted_claims_increment": 0,
        },
        "by_priority_band": by_priority,
        "by_source_status": by_status,
        "top_plate_route_candidates": top_plate_rows,
        "interpretation_boundary": "These are route candidates only. They do not validate source-normalized token order, physical direction, sign identity, sign meaning, phonetic value, language family, or translation.",
        "skeptic_notes": [
            "Exact OCR labels reject starred partial labels and split numeric suffix traps.",
            "Page-route crops show the OCR label context, not validated sign boxes.",
            "Volume mismatches and late register/data pages are retained but explicitly demoted.",
            "Every candidate still needs human visual source-panel review and matched-negative blind token-boxing.",
        ],
        "outputs": {
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
