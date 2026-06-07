from __future__ import annotations

import csv
import hashlib
import html
import json
import random
import re
import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path.cwd()
RUN_DATE = "2026-05-29"
PACKET_ID = "directionality_no_overlay_packet_v2b_unique_target_controls"

REPORTS = ROOT / "data" / "open_prototype" / "reports"
OUT_DIR = ROOT / "tmp" / "effective_unicity_directionality_blind_packet_v2b"
SOURCE_DIR = OUT_DIR / "source_crops"
BLIND_DIR = OUT_DIR / "blind_images"

ROUTES_CSV = REPORTS / "effective_unicity_directionality_public_route_probe_routes.csv"

CROP_MANIFEST = REPORTS / "effective_unicity_directionality_blind_packet_v2b_crop_manifest.csv"
BLIND_MANIFEST = REPORTS / "effective_unicity_directionality_blind_packet_v2b_manifest.csv"
ANSWER_KEY = REPORTS / "effective_unicity_directionality_blind_packet_v2b_answer_key.csv"
REVIEW_TEMPLATE = REPORTS / "effective_unicity_directionality_blind_packet_v2b_review_template.csv"
SUMMARY_JSON = REPORTS / "effective_unicity_directionality_blind_packet_v2b_summary.json"
CONTACT_SHEET = OUT_DIR / "directionality_no_overlay_v2b_blind_contact_sheet.png"

RNG_SEED = 407004003

VOLUME_XML = {
    "cisi_india": ROOT
    / "tmp"
    / "cisi_xml"
    / "Corpus of Indus Seals and Inscriptions. Collections in India_djvu.xml",
    "cisi_pakistan": ROOT
    / "tmp"
    / "cisi_xml"
    / "Corpus of Indus Seals and Inscriptions. Collections in Pakistan_djvu.xml",
}


TARGET_SPECS = [
    {
        "cisi": "H-654",
        "source_view": "A_recut_signband",
        "role": "primary_target_recut",
        "truth_class": "tier1_directionality_candidate_recut_after_v1_overcount",
        "crop_box_xyxy": (160, 1750, 980, 2120),
        "expected_token_count": 4,
        "text": "+405-061-740-806+",
        "source_note": "Tighter H-654 recut after v1 reviewer split 4 vs 5. Single public view, so not paired-view promotion-capable alone.",
    },
    {
        "cisi": "M-1310",
        "source_view": "A_recut_signband",
        "role": "primary_target_recut",
        "truth_class": "tier1_directionality_candidate_recut_after_v1_edge_fragments",
        "crop_box_xyxy": (1060, 1495, 2115, 1790),
        "expected_token_count": 7,
        "text": "+407-004-001-740-407-590-235+",
        "source_note": "Tighter M-1310 face recut after v1 reviewer noted edge fragments and counted 8 against 7.",
    },
    {
        "cisi": "M-1320",
        "source_view": "A_diagnostic_v1_failed",
        "role": "primary_target_recut",
        "truth_class": "tier1_route_candidate_v1_target_overcount_failure",
        "crop_box_xyxy": (1810, 1225, 3025, 1540),
        "expected_token_count": 5,
        "text": "+527-555-231-240-798+",
        "source_note": "Fresh raw-page crop retained as a primary target under the forger protocol, but v1 overcount makes it a high-risk failure witness.",
    },
    {
        "cisi": "M-811",
        "source_view": "A_diagnostic_v1_failed",
        "role": "primary_target_recut",
        "truth_class": "tier1_route_candidate_v1_target_overcount_failure",
        "crop_box_xyxy": (2250, 360, 3075, 760),
        "expected_token_count": 3,
        "text": "+226-032-803+",
        "source_note": "Fresh raw-page crop retained as a primary target under the forger protocol, but v1 overcount makes it a high-risk failure witness.",
    },
]

REAL_ROUTE_NEGATIVE_CISIS = [
    "H-665",
    "M-1458",
    "M-1523",
    "M-525",
    "M-365",
    "M-527",
    "M-534",
    "M-1315",
    "M-386",
    "H-158",
    "M-171",
    "M-567",
]

EXISTING_REAL_NEGATIVE_SPECS = [
    {
        "cisi": "M-1273",
        "source_view": "impression_a_existing_hard_negative",
        "role": "external_stress_control",
        "truth_class": "m70_hard_negative_002_y_prev_not_032_suffix_control",
        "source_image": "tmp/032_002_861_suffix_split/M1273_impression_a_cisi_pakistan_n195.png",
        "trim_bottom_px": 210,
        "expected_token_count": 5,
        "text": "+740-055-002-861-603+",
        "source_note": "Existing hard negative from prior M-70 packet.",
    },
    {
        "cisi": "M-376",
        "source_view": "impression_a_existing_hard_negative",
        "role": "external_stress_control",
        "truth_class": "m70_hard_negative_002_y_prev_not_032_suffix_control",
        "source_image": "tmp/032_002_861_suffix_split/M376_impression_a_cisi_india_n129.png",
        "trim_bottom_px": 36,
        "expected_token_count": 7,
        "text": "+740-100-176-002-861-533-717+",
        "source_note": "Existing hard negative from prior M-70 packet.",
    },
    {
        "cisi": "M-381",
        "source_view": "panel_existing_stress_negative",
        "role": "external_stress_control",
        "truth_class": "existing_segmentation_instability_stress_control",
        "source_image": "tmp/source_box_negative_control_v2/panel_crops/M-381_cisi_india_n129_plate_label_free_panel_enhanced_x2.jpg",
        "trim_bottom_px": 70,
        "expected_token_count": 7,
        "text": "+740-055-220-032-798-002-820+",
        "source_note": "Existing no-overlay stress control; prior blind reviews found segmentation instability.",
    },
]

RESERVE_ROUTE_NEGATIVE_CISIS = [
    "H-659",
    "M-127",
    "M-1322",
    "H-421",
    "M-915",
    "H-611",
]


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


def token_count(text: str) -> int:
    return len([part for part in text.replace("+", "").split("-") if part.strip()])


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


def page_index_from_usemap(usemap: str) -> int:
    match = re.search(r"_(\d+)\.djvu", usemap)
    return int(match.group(1)) if match else -1


def load_page_words() -> dict[tuple[str, int], dict[str, object]]:
    pages: dict[tuple[str, int], dict[str, object]] = {}
    for volume, xml_path in VOLUME_XML.items():
        text = xml_path.read_text(encoding="utf-8", errors="ignore")
        for object_match in re.finditer(r"<OBJECT\b(?P<attrs>.*?)>(?P<body>.*?)</OBJECT>", text, flags=re.S):
            attrs = parse_attrs(object_match.group("attrs"))
            usemap = attrs.get("usemap", "")
            if not usemap:
                continue
            words = []
            for word_match in re.finditer(r'<WORD\s+coords="([^"]+)">(.*?)</WORD>', object_match.group("body"), flags=re.S):
                raw = html.unescape(re.sub(r"<.*?>", "", word_match.group(2))).strip()
                if raw:
                    words.append({"text": raw, "box": parse_word_box(word_match.group(1))})
            pages[(volume, page_index_from_usemap(usemap))] = {
                "xml_width": int(attrs.get("width", "0")),
                "xml_height": int(attrs.get("height", "0")),
                "words": words,
            }
    return pages


def parse_box(value: str) -> tuple[int, int, int, int]:
    parts = [int(part) for part in str(value).split("|") if part != ""]
    if len(parts) != 4:
        raise ValueError(f"bad box: {value}")
    x1, y1, x2, y2 = parts
    return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)


def overlap(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> bool:
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def scaled_word_boxes(
    page_info: dict[str, object],
    image_size: tuple[int, int],
) -> list[tuple[int, int, int, int]]:
    image_width, image_height = image_size
    xml_width = int(page_info["xml_width"]) or image_width
    xml_height = int(page_info["xml_height"]) or image_height
    sx = image_width / xml_width
    sy = image_height / xml_height
    boxes = []
    for word in page_info["words"]:
        x1, y1, x2, y2 = word["box"]
        boxes.append((round(x1 * sx), round(y1 * sy), round(x2 * sx), round(y2 * sy)))
    return boxes


def mask_ocr_words(
    image: Image.Image,
    crop_box: tuple[int, int, int, int],
    volume: str,
    page_index: int,
    page_words: dict[tuple[str, int], dict[str, object]],
) -> tuple[Image.Image, int]:
    page_info = page_words.get((volume, page_index))
    crop = image.crop(crop_box).convert("RGB")
    if not page_info:
        return crop, 0
    draw = ImageDraw.Draw(crop)
    masked = 0
    for box in scaled_word_boxes(page_info, image.size):
        if not overlap(box, crop_box):
            continue
        x1 = max(0, box[0] - crop_box[0] - 14)
        y1 = max(0, box[1] - crop_box[1] - 10)
        x2 = min(crop.width, box[2] - crop_box[0] + 14)
        y2 = min(crop.height, box[3] - crop_box[1] + 10)
        draw.rectangle((x1, y1, x2, y2), fill=(255, 255, 255))
        masked += 1
    return crop, masked


def crop_image(page_path: Path, box: tuple[int, int, int, int]) -> Image.Image:
    image = Image.open(page_path).convert("RGB")
    x1, y1, x2, y2 = box
    x1 = max(0, min(x1, image.width - 1))
    y1 = max(0, min(y1, image.height - 1))
    x2 = max(x1 + 1, min(x2, image.width))
    y2 = max(y1 + 1, min(y2, image.height))
    return image.crop((x1, y1, x2, y2))


def enhanced(image: Image.Image) -> Image.Image:
    gray = ImageOps.grayscale(image)
    gray = ImageOps.autocontrast(gray, cutoff=1)
    return gray.resize((gray.width * 2, gray.height * 2), Image.Resampling.LANCZOS)


def first_route_by_cisi() -> dict[str, dict[str, str]]:
    rows = read_csv(ROUTES_CSV)
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        if row.get("route_rank") != "1":
            continue
        if row.get("source_grade_status", "").startswith("public_cisi_plate_route_candidate"):
            result[row["representative_cisi"]] = row
    return result


def write_crop(
    spec: dict[str, object],
    crop: Image.Image,
    source_page: str,
    crop_box: tuple[int, int, int, int],
    masked_ocr_word_boxes: int,
) -> dict[str, object]:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", f"{spec['cisi']}_{spec['source_view']}").strip("_")
    source_path = SOURCE_DIR / f"{slug}_source.png"
    enhanced_path = SOURCE_DIR / f"{slug}_enhanced_x2.png"
    crop.save(source_path)
    enhanced(crop).save(enhanced_path)
    return {
        "date": RUN_DATE,
        "packet_id": PACKET_ID,
        "cisi": spec["cisi"],
        "source_view": spec["source_view"],
        "role": spec["role"],
        "truth_class": spec["truth_class"],
        "text": spec["text"],
        "expected_token_count": spec["expected_token_count"],
        "computed_token_count": token_count(str(spec["text"])),
        "source_page": source_page,
        "crop_box_xyxy": "|".join(str(v) for v in crop_box),
        "source_crop": str(source_path.relative_to(ROOT)).replace("\\", "/"),
        "enhanced_crop": str(enhanced_path.relative_to(ROOT)).replace("\\", "/"),
        "source_crop_sha256": sha256_file(source_path),
        "enhanced_crop_sha256": sha256_file(enhanced_path),
        "masked_ocr_word_boxes": masked_ocr_word_boxes,
        "source_note": spec["source_note"],
        "accepted_claims_increment": 0,
    }


def build_target_rows(routes: dict[str, dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for spec in TARGET_SPECS:
        route = routes.get(str(spec["cisi"]))
        if not route:
            raise FileNotFoundError(f"missing route for target {spec['cisi']}")
        page_path = ROOT / route["local_page_path"]
        crop = crop_image(page_path, spec["crop_box_xyxy"])
        rows.append(
            write_crop(
                spec,
                crop,
                str(page_path.relative_to(ROOT)).replace("\\", "/"),
                spec["crop_box_xyxy"],
                0,
            )
        )
    return rows


def build_route_negative_rows(
    routes: dict[str, dict[str, str]],
    page_words: dict[tuple[str, int], dict[str, object]],
) -> list[dict[str, object]]:
    rows = []
    for cisi in REAL_ROUTE_NEGATIVE_CISIS:
        route = routes.get(cisi)
        if not route:
            raise FileNotFoundError(f"missing route for negative {cisi}")
        page_path = ROOT / route["local_page_path"]
        page = Image.open(page_path).convert("RGB")
        crop_box = parse_box(route["crop_box_image_coords"])
        crop, masked = mask_ocr_words(
            page,
            crop_box,
            route["volume"],
            int(route["page_index"]),
            page_words,
        )
        spec = {
            "cisi": cisi,
            "source_view": f"{route['volume']}_n{route['page_index']}_label_masked_context",
            "role": "scoring_negative_real",
            "truth_class": "forger_recommended_routed_real_negative_label_masked_context",
            "expected_token_count": token_count(route["text"]),
            "text": route["text"],
            "source_note": (
                "Forger-recommended routed real negative. Context crop is cut from raw page, with all OCR word boxes "
                "inside the crop masked before blinding; still requires human leakage QA."
            ),
        }
        rows.append(
            write_crop(
                spec,
                crop,
                str(page_path.relative_to(ROOT)).replace("\\", "/"),
                crop_box,
                masked,
            )
        )
    return rows


def build_existing_negative_rows() -> list[dict[str, object]]:
    rows = []
    for spec in EXISTING_REAL_NEGATIVE_SPECS:
        page_path = ROOT / str(spec["source_image"])
        crop = Image.open(page_path).convert("RGB")
        trim_bottom_px = int(spec.get("trim_bottom_px", 0))
        if trim_bottom_px:
            crop = crop.crop((0, 0, crop.width, max(1, crop.height - trim_bottom_px)))
        rows.append(
            write_crop(
                spec,
                crop,
                str(page_path.relative_to(ROOT)).replace("\\", "/"),
                (0, 0, crop.width, crop.height),
                0,
            )
        )
    return rows


def synthetic_control_image(kind: str, index: int) -> Image.Image:
    image = Image.new("RGB", (760, 260), (245, 245, 245))
    draw = ImageDraw.Draw(image)
    if kind == "leak_sentinel":
        draw.rectangle((40, 48, 720, 210), fill=(225, 225, 225), outline=(80, 80, 80), width=3)
        draw.text((70, 84), f"FAKE-CISI DIRECTIONAL LEAK {index}", fill=(0, 0, 0))
        draw.text((70, 132), "M-999 A / route rank / expected count", fill=(0, 0, 0))
    elif kind == "blank_surface":
        for x in range(0, 760, 19):
            shade = 235 + ((x + index * 17) % 18)
            draw.line((x, 0, x + 120, 260), fill=(shade, shade, shade), width=2)
    else:
        raise ValueError(kind)
    return image


def build_auxiliary_control_rows() -> list[dict[str, object]]:
    rows = []
    for index in range(1, 3):
        spec = {
            "cisi": f"SYN-LEAK-{index}",
            "source_view": "synthetic_label_leak_sentinel",
            "role": "synthetic_leak_sentinel_auxiliary",
            "truth_class": "auxiliary_control_not_real_negative_denominator",
            "expected_token_count": 0,
            "text": "",
            "source_note": "Deliberate fake metadata leak sentinel. Reviewers must flag label_leak=yes; never counts toward the real-negative denominator.",
        }
        rows.append(write_crop(spec, synthetic_control_image("leak_sentinel", index), "synthetic", (0, 0, 760, 260), 0))
    for index in range(1, 3):
        spec = {
            "cisi": f"SYN-BLANK-{index}",
            "source_view": "synthetic_blank_surface_control",
            "role": "synthetic_blank_auxiliary",
            "truth_class": "auxiliary_control_not_real_negative_denominator",
            "expected_token_count": 0,
            "text": "",
            "source_note": "Synthetic blank/non-script surface. Reviewers should reject as non-boxable; never counts toward the real-negative denominator.",
        }
        rows.append(write_crop(spec, synthetic_control_image("blank_surface", index), "synthetic", (0, 0, 760, 260), 0))
    return rows


def build_blind_packet(crop_rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    BLIND_DIR.mkdir(parents=True, exist_ok=True)
    rng = random.Random(RNG_SEED)
    shuffled = list(crop_rows)
    rng.shuffle(shuffled)
    manifest_rows = []
    key_rows = []
    for index, row in enumerate(shuffled, start=1):
        blind_id = f"D2_{index:03d}"
        source = ROOT / str(row["enhanced_crop"])
        target = BLIND_DIR / f"{blind_id}.png"
        shutil.copyfile(source, target)
        image_hash = sha256_file(target)
        manifest_rows.append(
            {
                "date": RUN_DATE,
                "packet_id": PACKET_ID,
                "blind_id": blind_id,
                "image_path": str(target.relative_to(ROOT)).replace("\\", "/"),
                "image_sha256": image_hash,
                "review_stage": "stage1_blind_label_leak_and_single_signband_screen",
                "review_task": (
                    "Without catalogue text or object ID, mark label/metadata leak, whether exactly one signband is "
                    "confidently boxable, and the visible token count for that signband if boxable."
                ),
                "required_output": "token_count; single_signband_boxable_yes_no_uncertain; label_leak_yes_no; notes",
                "accepted_claims_increment": 0,
            }
        )
        key_rows.append(
            {
                "date": RUN_DATE,
                "packet_id": PACKET_ID,
                "blind_id": blind_id,
                "cisi": row["cisi"],
                "source_view": row["source_view"],
                "role": row["role"],
                "truth_class": row["truth_class"],
                "target_text": row["text"],
                "expected_token_count": row["expected_token_count"],
                "source_crop": row["source_crop"],
                "enhanced_crop": row["enhanced_crop"],
                "masked_ocr_word_boxes": row["masked_ocr_word_boxes"],
                "blind_image_sha256": image_hash,
                "source_note": row["source_note"],
                "accepted_claims_increment": 0,
            }
        )
    return manifest_rows, key_rows


def make_review_template(manifest_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "date": RUN_DATE,
            "packet_id": PACKET_ID,
            "reviewer": "",
            "blind_id": row["blind_id"],
            "stage1_visual_token_count": "",
            "stage1_single_signband_boxable_yes_no_uncertain": "",
            "stage1_label_leak_yes_no": "",
            "stage1_notes": "",
            "stage2_after_unblind_expected_count_match_yes_no_uncertain": "",
            "stage2_after_unblind_promotable_yes_no": "",
            "stage2_notes": "",
        }
        for row in manifest_rows
    ]


def make_contact_sheet(manifest_rows: list[dict[str, object]]) -> None:
    try:
        font = ImageFont.truetype("arial.ttf", 22)
    except OSError:
        font = ImageFont.load_default()
    cols = 2
    cell_w = 820
    cell_h = 500
    rows = (len(manifest_rows) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    for index, row in enumerate(manifest_rows):
        image = Image.open(ROOT / str(row["image_path"])).convert("RGB")
        image.thumbnail((cell_w - 40, cell_h - 75), Image.Resampling.LANCZOS)
        col = index % cols
        row_index = index // cols
        x = col * cell_w + 20
        y = row_index * cell_h + 58
        draw.text((col * cell_w + 20, row_index * cell_h + 20), str(row["blind_id"]), fill="black", font=font)
        sheet.paste(image, (x, y))
        draw.rectangle((x - 1, y - 1, x + image.width + 1, y + image.height + 1), outline=(180, 180, 180), width=1)
    CONTACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(CONTACT_SHEET)


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    page_words = load_page_words()
    routes = first_route_by_cisi()
    crop_rows = (
        build_target_rows(routes)
        + build_route_negative_rows(routes, page_words)
        + build_existing_negative_rows()
        + build_auxiliary_control_rows()
    )
    manifest_rows, key_rows = build_blind_packet(crop_rows)
    review_rows = make_review_template(manifest_rows)
    make_contact_sheet(manifest_rows)

    write_csv(CROP_MANIFEST, crop_rows, list(crop_rows[0].keys()))
    write_csv(BLIND_MANIFEST, manifest_rows, list(manifest_rows[0].keys()))
    write_csv(ANSWER_KEY, key_rows, list(key_rows[0].keys()))
    write_csv(REVIEW_TEMPLATE, review_rows, list(review_rows[0].keys()))

    primary_targets = [row for row in key_rows if row["role"] == "primary_target_recut"]
    real_negatives = [row for row in key_rows if row["role"] == "scoring_negative_real"]
    external_stress = [row for row in key_rows if row["role"] == "external_stress_control"]
    auxiliary_controls = [
        row for row in key_rows if str(row["role"]).startswith("synthetic_")
    ]
    image_hash_groups: dict[str, list[dict[str, object]]] = {}
    for row in key_rows:
        image_hash_groups.setdefault(str(row["blind_image_sha256"]), []).append(row)
    duplicate_hash_groups = [
        [
            {
                "blind_id": row["blind_id"],
                "cisi": row["cisi"],
                "role": row["role"],
                "source_view": row["source_view"],
            }
            for row in rows
        ]
        for rows in image_hash_groups.values()
        if len(rows) > 1
    ]

    summary = {
        "date": RUN_DATE,
        "packet_id": PACKET_ID,
        "status": "v2b_packet_created_not_scored_no_claim_promotion",
        "purpose": (
            "Repair the v2 preflight duplicate-target failure by keeping only unique primary target recuts, while retaining "
            "the fixed 12 routed real-negative denominator, label-masked raw-page context crops, and auxiliary synthetic "
            "sentinels outside the real denominator."
        ),
        "counts": {
            "blind_items": len(manifest_rows),
            "primary_target_recut_images": len(primary_targets),
            "primary_target_recut_unique_cisis": len({row["cisi"] for row in primary_targets}),
            "scoring_negative_real_images": len(real_negatives),
            "scoring_negative_real_unique_cisis": len({row["cisi"] for row in real_negatives}),
            "external_stress_control_images": len(external_stress),
            "auxiliary_synthetic_control_images": len(auxiliary_controls),
            "duplicate_blind_image_hash_groups": len(duplicate_hash_groups),
            "accepted_claims_increment": 0,
        },
        "forger_control_plan": {
            "planned_real_scoring_negative_unique_cisis": 12,
            "current_packet_real_scoring_negative_unique_cisis": len({row["cisi"] for row in real_negatives}),
            "promotion_denominator_floor": 10,
            "minimum_independent_reviewers": 3,
            "denominator_policy": "the 12 routed real negatives are fixed; if any real denominator row leaks or becomes non-comparable, the packet fails instead of recalculating FPR",
            "synthetic_controls_policy": "auxiliary only; synthetic controls never count toward the real-negative denominator",
            "duplicate_hash_policy": "any duplicate blind image hash keeps the packet at preflight failure; v2b is generated to avoid all duplicate target-image hashes",
            "status": "real-control denominator now meets the forger floor, but the packet is not reviewed and cannot promote anything yet",
        },
        "duplicate_blind_image_hash_groups": duplicate_hash_groups,
        "target_cisis": sorted({row["cisi"] for row in primary_targets}),
        "scoring_negative_real_cisis": sorted({row["cisi"] for row in real_negatives}),
        "reserve_route_negative_cisis": RESERVE_ROUTE_NEGATIVE_CISIS,
        "external_stress_control_cisis": sorted({row["cisi"] for row in external_stress}),
        "label_masking": {
            "route_context_negatives_mask_all_ocr_word_boxes_inside_crop": True,
            "total_masked_ocr_word_boxes": sum(int(row["masked_ocr_word_boxes"]) for row in crop_rows),
            "visual_leakage_still_requires_blind_review": True,
        },
        "promotion_thresholds": [
            "At least three independent blind reviews must be present.",
            "Every primary_target_recut image must be label-leak-free and have exactly one confidently boxable signband.",
            "No duplicate blind image hash is permitted in the packet.",
            "Paired target-view promotion is disabled in v2b because only unique target images are retained; any future paired-view packet must use distinct hashes and identical blind token counts.",
            "Real routed scoring negatives must produce zero hard boxable-and-count-matching hits, zero target-like uncertainty, and zero label leaks across all 12 fixed rows.",
            "If any real denominator row leaks, is missing, has duplicate unintended image hash, or becomes non-comparable, the packet fails; the denominator is not recalculated downward.",
            "Synthetic leak sentinels must be flagged by every reviewer, but synthetic controls are auxiliary and never count toward the real-negative floor.",
            "Even a passing packet can only promote a source-crop candidate for later side/direction adjudication, never a value, meaning, language, translation, or accepted structural finding.",
        ],
        "interpretation_boundary": (
            "This packet is a source-normalization control gate only. Creation of the packet validates no source order, "
            "physical direction, sign identity, sign semantics, language family, phonetic value, translation, or accepted claim."
        ),
        "outputs": {
            "crop_manifest": str(CROP_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
            "blind_manifest": str(BLIND_MANIFEST.relative_to(ROOT)).replace("\\", "/"),
            "answer_key": str(ANSWER_KEY.relative_to(ROOT)).replace("\\", "/"),
            "review_template": str(REVIEW_TEMPLATE.relative_to(ROOT)).replace("\\", "/"),
            "summary_json": str(SUMMARY_JSON.relative_to(ROOT)).replace("\\", "/"),
            "contact_sheet": str(CONTACT_SHEET.relative_to(ROOT)).replace("\\", "/"),
            "blind_image_dir": str(BLIND_DIR.relative_to(ROOT)).replace("\\", "/"),
        },
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
