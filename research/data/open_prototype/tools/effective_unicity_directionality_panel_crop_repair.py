"""Generate label-free object-panel crop candidates for the blind packet series.

This is the repair step after v2c failed visual preflight: masking OCR words on
a page-context crop was not enough, because the crop itself still showed page
layout. The fix attempted here is to find the seal's object panel and crop only
it, keeping catalogue labels and OCR text outside the crop box entirely rather
than painting over them. For each focus CISI (4 primary targets, 12 fixed real
negatives, 6 reserves), the script takes up to three plate routes from the v2
public route probe CSV, locates the printed catalogue label via the DjVu OCR
coordinates, and proposes crops three ways: fixed boxes above/below/around the
label, horizontal dark-row clusters inside those boxes, and dark connected
components found near the label (with text regions masked out of the search).
Component crops are clipped away from any overlapping text box. Every candidate
gets a mechanical preflight status — any label-box or OCR-word overlap is an
automatic fail — and is written to a candidates CSV, two contact sheets, and a
summary JSON. This is a preflight inventory only; a human must still review
every crop before it can enter a blind packet, and nothing here promotes a
claim.
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import math
import re
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path.cwd()
RUN_DATE = "2026-05-29"
REPAIR_ID = "directionality_panel_crop_repair_v2_clean_component_clips"

REPORTS = ROOT / "data" / "open_prototype" / "reports"
ROUTES_CSV = REPORTS / "effective_unicity_directionality_public_route_probe_v2_routes.csv"

OUT_DIR = ROOT / "tmp" / "effective_unicity_directionality_panel_crop_repair"
CROP_DIR = OUT_DIR / "candidates_v2"
CONTACT_ALL = OUT_DIR / "directionality_panel_crop_repair_v2_all_candidates.jpg"
CONTACT_BEST = OUT_DIR / "directionality_panel_crop_repair_v2_best_candidates.jpg"

CANDIDATES_CSV = REPORTS / "effective_unicity_directionality_panel_crop_repair_v2_candidates.csv"
SUMMARY_JSON = REPORTS / "effective_unicity_directionality_panel_crop_repair_v2_summary.json"

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

PRIMARY_TARGET_CISIS = {"H-654", "M-1310", "M-1320", "M-811"}

REAL_ROUTE_NEGATIVE_CISIS = {
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
}

RESERVE_ROUTE_NEGATIVE_CISIS = {
    "H-659",
    "M-127",
    "M-1322",
    "H-421",
    "M-915",
    "H-611",
}

FOCUS_CISIS = PRIMARY_TARGET_CISIS | REAL_ROUTE_NEGATIVE_CISIS | RESERVE_ROUTE_NEGATIVE_CISIS

CANDIDATE_FIELDS = [
    "date",
    "repair_id",
    "cisi",
    "role",
    "crop_kind",
    "crop_stage",
    "control_subtype",
    "denominator_group",
    "denominator_inclusion",
    "match_set_id",
    "matched_target_cisi",
    "match_basis",
    "source_family_key",
    "near_duplicate_group_id",
    "route_rank",
    "queue_rank",
    "volume",
    "page_index",
    "source_url",
    "match_text",
    "source_grade_status",
    "source_page",
    "source_page_sha256",
    "parent_crop_sha256",
    "image_width",
    "image_height",
    "xml_width",
    "xml_height",
    "ocr_label_coords_xml",
    "label_box_image_coords",
    "label_box_width",
    "label_box_height",
    "label_match_compactness_status",
    "method",
    "candidate_rank",
    "crop_box_xyxy",
    "crop_width",
    "crop_height",
    "crop_aspect_ratio",
    "dark_pixel_fraction",
    "component_area_downsampled",
    "component_bbox_image_coords",
    "component_centroid_image_coords",
    "component_score",
    "ocr_word_overlap_count",
    "label_box_overlap_fraction",
    "label_exclusion_status",
    "candidate_preflight_status",
    "source_crop",
    "enhanced_crop",
    "source_crop_sha256",
    "enhanced_crop_sha256",
    "notes",
    "accepted_claims_increment",
]


def ensure_dirs() -> None:
    CROP_DIR.mkdir(parents=True, exist_ok=True)


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


def parse_attrs(text: str) -> dict[str, str]:
    return {key: html.unescape(value) for key, value in re.findall(r'(\w+)="([^"]*)"', text)}


def parse_word_box(coords: str) -> tuple[int, int, int, int]:
    values = [int(v) for v in coords.split(",") if v.strip()]
    if len(values) == 4:
        x1, y1, x2, y2 = values
        return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
    if len(values) == 5:
        x1, y1, x2, y2 = values[:4]
        return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
    if len(values) > 5 and len(values) % 2 == 0:
        xs = values[0::2]
        ys = values[1::2]
        return min(xs), min(ys), max(xs), max(ys)
    if len(values) > 5:
        x1, y1, x2, y2 = values[:4]
        return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
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


def clamp_box(box: tuple[int, int, int, int], width: int, height: int) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = box
    x1 = max(0, min(x1, width - 1))
    y1 = max(0, min(y1, height - 1))
    x2 = max(x1 + 1, min(x2, width))
    y2 = max(y1 + 1, min(y2, height))
    return x1, y1, x2, y2


def expand_box(
    box: tuple[int, int, int, int],
    pad_x: int,
    pad_y: int,
    width: int,
    height: int,
) -> tuple[int, int, int, int]:
    x1, y1, x2, y2 = box
    return clamp_box((x1 - pad_x, y1 - pad_y, x2 + pad_x, y2 + pad_y), width, height)


def box_str(box: tuple[int, int, int, int] | None) -> str:
    if box is None:
        return ""
    return "|".join(str(int(value)) for value in box)


def scale_box(
    box: tuple[int, int, int, int],
    xml_width: int,
    xml_height: int,
    image_width: int,
    image_height: int,
) -> tuple[int, int, int, int]:
    sx = image_width / xml_width if xml_width else 1.0
    sy = image_height / xml_height if xml_height else 1.0
    x1, y1, x2, y2 = box
    return (
        round(x1 * sx),
        round(y1 * sy),
        round(x2 * sx),
        round(y2 * sy),
    )


def overlap_area(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> int:
    x1 = max(a[0], b[0])
    y1 = max(a[1], b[1])
    x2 = min(a[2], b[2])
    y2 = min(a[3], b[3])
    if x2 <= x1 or y2 <= y1:
        return 0
    return (x2 - x1) * (y2 - y1)


def box_area(box: tuple[int, int, int, int]) -> int:
    return max(0, box[2] - box[0]) * max(0, box[3] - box[1])


def scaled_word_boxes(
    page_info: dict[str, object] | None,
    image_size: tuple[int, int],
) -> list[tuple[int, int, int, int]]:
    if not page_info:
        return []
    image_width, image_height = image_size
    xml_width = int(page_info["xml_width"]) or image_width
    xml_height = int(page_info["xml_height"]) or image_height
    return [
        scale_box(word["box"], xml_width, xml_height, image_width, image_height)
        for word in page_info["words"]
    ]


def compactness_status(label_box: tuple[int, int, int, int]) -> str:
    width = label_box[2] - label_box[0]
    height = label_box[3] - label_box[1]
    if width <= 0 or height <= 0:
        return "invalid_label_box"
    if height > 95:
        return "noncompact_vertical_label_match_reject_for_blind_source"
    if width > 360:
        return "wide_label_match_check_before_blind_source"
    return "compact_label_match_candidate"


def role_for_cisi(cisi: str) -> str:
    if cisi in PRIMARY_TARGET_CISIS:
        return "primary_target_route_candidate"
    if cisi in REAL_ROUTE_NEGATIVE_CISIS:
        return "real_route_negative_candidate"
    if cisi in RESERVE_ROUTE_NEGATIVE_CISIS:
        return "reserve_route_negative_candidate"
    return "unplanned_focus_candidate"


def control_subtype_for_cisi(cisi: str) -> str:
    if cisi in PRIMARY_TARGET_CISIS:
        return "directionality_target_candidate"
    if cisi in REAL_ROUTE_NEGATIVE_CISIS:
        return "fixed_real_object_panel_negative"
    if cisi in RESERVE_ROUTE_NEGATIVE_CISIS:
        return "reserve_real_object_panel_negative"
    return "unplanned_candidate"


def denominator_group_for_cisi(cisi: str) -> str:
    if cisi in REAL_ROUTE_NEGATIVE_CISIS:
        return "fixed_real_route_negative_denominator"
    if cisi in PRIMARY_TARGET_CISIS:
        return "primary_target_not_denominator"
    if cisi in RESERVE_ROUTE_NEGATIVE_CISIS:
        return "reserve_not_denominator"
    return "not_denominator"


def denominator_inclusion_for_cisi(cisi: str) -> str:
    if cisi in REAL_ROUTE_NEGATIVE_CISIS:
        return "candidate_for_fixed_denominator_after_visual_preflight"
    return "excluded_from_real_negative_denominator"


def crop_enhanced(image: Image.Image) -> Image.Image:
    gray = ImageOps.grayscale(image)
    gray = ImageOps.autocontrast(gray, cutoff=1)
    return gray.resize((gray.width * 2, gray.height * 2), Image.Resampling.LANCZOS)


def downsample_max(mask: np.ndarray, factor: int) -> np.ndarray:
    height, width = mask.shape
    new_h = max(1, height // factor)
    new_w = max(1, width // factor)
    trimmed = mask[: new_h * factor, : new_w * factor]
    return trimmed.reshape(new_h, factor, new_w, factor).max(axis=(1, 3))


def dilate(mask: np.ndarray, radius: int) -> np.ndarray:
    if radius <= 0:
        return mask
    height, width = mask.shape
    out = np.zeros_like(mask, dtype=bool)
    for dy in range(-radius, radius + 1):
        y_src_1 = max(0, -dy)
        y_src_2 = min(height, height - dy)
        y_dst_1 = max(0, dy)
        y_dst_2 = min(height, height + dy)
        for dx in range(-radius, radius + 1):
            if dx * dx + dy * dy > radius * radius:
                continue
            x_src_1 = max(0, -dx)
            x_src_2 = min(width, width - dx)
            x_dst_1 = max(0, dx)
            x_dst_2 = min(width, width + dx)
            out[y_dst_1:y_dst_2, x_dst_1:x_dst_2] |= mask[y_src_1:y_src_2, x_src_1:x_src_2]
    return out


def connected_components(mask: np.ndarray) -> list[dict[str, object]]:
    height, width = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    components: list[dict[str, object]] = []
    ys, xs = np.nonzero(mask)
    starts = list(zip(xs.tolist(), ys.tolist()))
    for sx, sy in starts:
        if visited[sy, sx] or not mask[sy, sx]:
            continue
        queue: deque[tuple[int, int]] = deque([(sx, sy)])
        visited[sy, sx] = True
        min_x = max_x = sx
        min_y = max_y = sy
        area = 0
        sum_x = 0
        sum_y = 0
        while queue:
            x, y = queue.popleft()
            area += 1
            sum_x += x
            sum_y += y
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if nx < 0 or nx >= width or ny < 0 or ny >= height:
                    continue
                if visited[ny, nx] or not mask[ny, nx]:
                    continue
                visited[ny, nx] = True
                queue.append((nx, ny))
        components.append(
            {
                "bbox": (min_x, min_y, max_x + 1, max_y + 1),
                "area": area,
                "centroid": (sum_x / area, sum_y / area),
            }
        )
    return components


def text_mask_for_search(
    page_image: Image.Image,
    search_box: tuple[int, int, int, int],
    word_boxes: list[tuple[int, int, int, int]],
    label_box: tuple[int, int, int, int],
) -> np.ndarray:
    sx1, sy1, sx2, sy2 = search_box
    mask = np.zeros((sy2 - sy1, sx2 - sx1), dtype=bool)
    for box in word_boxes + [label_box]:
        if overlap_area(box, search_box) == 0:
            continue
        x1, y1, x2, y2 = expand_box(box, 70, 50, page_image.width, page_image.height)
        x1 = max(sx1, x1) - sx1
        y1 = max(sy1, y1) - sy1
        x2 = min(sx2, x2) - sx1
        y2 = min(sy2, y2) - sy1
        if x2 > x1 and y2 > y1:
            mask[y1:y2, x1:x2] = True
    return mask


def component_candidates(
    page_image: Image.Image,
    search_box: tuple[int, int, int, int],
    word_boxes: list[tuple[int, int, int, int]],
    label_box: tuple[int, int, int, int],
) -> list[dict[str, object]]:
    sx1, sy1, sx2, sy2 = search_box
    crop = page_image.crop(search_box).convert("L")
    arr = np.asarray(crop)
    dark = arr < 215
    dark &= ~text_mask_for_search(page_image, search_box, word_boxes, label_box)
    coarse_factor = 4
    coarse = downsample_max(dark, coarse_factor)
    coarse = dilate(coarse, radius=8)
    comps = connected_components(coarse)
    label_cx = (label_box[0] + label_box[2]) / 2.0
    label_cy = (label_box[1] + label_box[3]) / 2.0
    rows = []
    for comp in comps:
        bx1, by1, bx2, by2 = comp["bbox"]
        full_box = clamp_box(
            (
                sx1 + bx1 * coarse_factor,
                sy1 + by1 * coarse_factor,
                sx1 + bx2 * coarse_factor,
                sy1 + by2 * coarse_factor,
            ),
            page_image.width,
            page_image.height,
        )
        width = full_box[2] - full_box[0]
        height = full_box[3] - full_box[1]
        if width < 80 or height < 60:
            continue
        if int(comp["area"]) < 80:
            continue
        cx = sx1 + float(comp["centroid"][0]) * coarse_factor
        cy = sy1 + float(comp["centroid"][1]) * coarse_factor
        distance = math.hypot(cx - label_cx, cy - label_cy)
        score = int(comp["area"]) * 1000.0 / (1.0 + distance)
        rows.append(
            {
                "box": expand_box(full_box, 45, 45, page_image.width, page_image.height),
                "raw_component_box": full_box,
                "area": int(comp["area"]),
                "centroid": (round(cx), round(cy)),
                "score": round(score, 6),
                "position": "above" if cy < label_cy else "below",
            }
        )
    return sorted(rows, key=lambda row: (-float(row["score"]), -int(row["area"])))


def fixed_relative_boxes(
    label_box: tuple[int, int, int, int],
    image_size: tuple[int, int],
) -> list[dict[str, object]]:
    width, height = image_size
    lx1, ly1, lx2, ly2 = label_box
    cx = (lx1 + lx2) // 2
    label_w = max(1, lx2 - lx1)
    half_w = max(520, min(900, label_w // 2 + 560))
    boxes = [
        {
            "method": "above_label_wide",
            "box": clamp_box((cx - half_w, ly1 - 980, cx + half_w, ly1 - 70), width, height),
        },
        {
            "method": "below_label_wide",
            "box": clamp_box((cx - half_w, ly2 + 70, cx + half_w, ly2 + 980), width, height),
        },
        {
            "method": "around_label_without_center_label",
            "box": clamp_box((cx - half_w, ly1 - 560, cx + half_w, ly2 + 560), width, height),
        },
    ]
    return boxes


def dark_fraction(image: Image.Image) -> float:
    arr = np.asarray(ImageOps.grayscale(image))
    return round(float((arr < 215).mean()), 6)


def overlap_word_count(box: tuple[int, int, int, int], word_boxes: list[tuple[int, int, int, int]]) -> int:
    return sum(1 for word_box in word_boxes if overlap_area(box, word_box) > 0)


def horizontal_overlap_fraction(
    a: tuple[int, int, int, int],
    b: tuple[int, int, int, int],
) -> float:
    overlap = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    return overlap / max(1, min(a[2] - a[0], b[2] - b[0]))


def vertical_overlap_fraction(
    a: tuple[int, int, int, int],
    b: tuple[int, int, int, int],
) -> float:
    overlap = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    return overlap / max(1, min(a[3] - a[1], b[3] - b[1]))


def clip_component_box_away_from_text(
    component_box: tuple[int, int, int, int],
    label_box: tuple[int, int, int, int],
    word_boxes: list[tuple[int, int, int, int]],
    image_width: int,
    image_height: int,
) -> tuple[int, int, int, int]:
    crop = expand_box(component_box, 32, 22, image_width, image_height)
    text_boxes = word_boxes + [label_box]
    for _ in range(4):
        changed = False
        overlaps = [text_box for text_box in text_boxes if overlap_area(crop, text_box) > 0]
        for text_box in overlaps:
            h_frac = horizontal_overlap_fraction(crop, text_box)
            v_frac = vertical_overlap_fraction(crop, text_box)
            if h_frac >= 0.08:
                if text_box[1] >= component_box[3] - 18:
                    new_bottom = max(crop[1] + 1, text_box[1] - 10)
                    if new_bottom < crop[3]:
                        crop = (crop[0], crop[1], crop[2], new_bottom)
                        changed = True
                        continue
                if text_box[3] <= component_box[1] + 18:
                    new_top = min(crop[3] - 1, text_box[3] + 10)
                    if new_top > crop[1]:
                        crop = (crop[0], new_top, crop[2], crop[3])
                        changed = True
                        continue
            if v_frac >= 0.08:
                if text_box[0] >= component_box[2] - 18:
                    new_right = max(crop[0] + 1, text_box[0] - 10)
                    if new_right < crop[2]:
                        crop = (crop[0], crop[1], new_right, crop[3])
                        changed = True
                        continue
                if text_box[2] <= component_box[0] + 18:
                    new_left = min(crop[2] - 1, text_box[2] + 10)
                    if new_left > crop[0]:
                        crop = (new_left, crop[1], crop[2], crop[3])
                        changed = True
                        continue
        if not changed:
            break
    return clamp_box(crop, image_width, image_height)


def horizontal_dark_cluster_candidates(
    page_image: Image.Image,
    base_box: tuple[int, int, int, int],
    word_boxes: list[tuple[int, int, int, int]],
    label_box: tuple[int, int, int, int],
    method_prefix: str,
) -> list[dict[str, object]]:
    bx1, by1, bx2, by2 = base_box
    crop = page_image.crop(base_box).convert("L")
    arr = np.asarray(crop)
    dark = arr < 215
    mask = text_mask_for_search(page_image, base_box, word_boxes, label_box)
    dark &= ~mask
    row_fraction = dark.mean(axis=1)
    active = row_fraction > 0.012
    clusters: list[tuple[int, int]] = []
    start: int | None = None
    last_active = -1
    allowed_gap = 10
    for index, is_active in enumerate(active.tolist()):
        if is_active:
            if start is None:
                start = index
            last_active = index
        elif start is not None and index - last_active > allowed_gap:
            clusters.append((start, last_active + 1))
            start = None
    if start is not None:
        clusters.append((start, last_active + 1))

    label_cy = (label_box[1] + label_box[3]) / 2.0
    rows = []
    for y1, y2 in clusters:
        if y2 - y1 < 80:
            continue
        sub = dark[y1:y2, :]
        col_fraction = sub.mean(axis=0)
        cols = np.nonzero(col_fraction > 0.008)[0]
        if not len(cols):
            continue
        x1 = int(cols.min())
        x2 = int(cols.max()) + 1
        if x2 - x1 < 220:
            continue
        cluster_box = clamp_box((bx1 + x1, by1 + y1, bx1 + x2, by1 + y2), page_image.width, page_image.height)
        clean_box = clip_component_box_away_from_text(cluster_box, label_box, word_boxes, page_image.width, page_image.height)
        if clean_box[2] - clean_box[0] < 180 or clean_box[3] - clean_box[1] < 70:
            continue
        cy = (clean_box[1] + clean_box[3]) / 2.0
        position = "above" if cy < label_cy else "below"
        dark_area = int(sub[:, x1:x2].sum())
        score = dark_area * 1000.0 / (1.0 + abs(cy - label_cy))
        rows.append(
            {
                "method": f"{method_prefix}_{position}_cluster",
                "box": clean_box,
                "raw_component_box": cluster_box,
                "area": dark_area,
                "centroid": (round((clean_box[0] + clean_box[2]) / 2), round(cy)),
                "score": round(score, 6),
                "position": position,
            }
        )
    return sorted(rows, key=lambda row: (-float(row["score"]), -int(row["area"])))


def write_candidate(
    route: dict[str, str],
    page_image: Image.Image,
    page_sha: str,
    page_info: dict[str, object] | None,
    word_boxes: list[tuple[int, int, int, int]],
    label_box: tuple[int, int, int, int],
    label_compactness: str,
    method: str,
    candidate_rank: int,
    crop_box: tuple[int, int, int, int],
    component: dict[str, object] | None,
) -> dict[str, object]:
    cisi = route["representative_cisi"]
    crop_box = clamp_box(crop_box, page_image.width, page_image.height)
    crop = page_image.crop(crop_box).convert("RGB")
    enhanced = crop_enhanced(crop)
    slug = re.sub(
        r"[^A-Za-z0-9]+",
        "_",
        f"{cisi}_{route['volume']}_n{route['page_index']}_r{route['route_rank']}_{candidate_rank}_{method}",
    ).strip("_")
    source_path = CROP_DIR / f"{slug}_source.png"
    enhanced_path = CROP_DIR / f"{slug}_enhanced_x2.png"
    crop.save(source_path)
    enhanced.save(enhanced_path)
    label_overlap = overlap_area(crop_box, label_box) / max(1, box_area(label_box))
    label_status = "label_box_excluded" if label_overlap == 0 else "label_box_overlaps_crop_preflight_fail"
    word_overlap_count = overlap_word_count(crop_box, word_boxes)
    if label_compactness.startswith("noncompact"):
        preflight = "route_label_match_noncompact_preflight_fail"
    elif label_status != "label_box_excluded":
        preflight = "label_box_overlap_preflight_fail"
    elif word_overlap_count:
        preflight = "ocr_word_overlap_preflight_fail"
    else:
        preflight = "candidate_requires_visual_label_leak_and_single_panel_preflight"
    crop_w = crop_box[2] - crop_box[0]
    crop_h = crop_box[3] - crop_box[1]
    component_box = component.get("raw_component_box") if component else None
    centroid = component.get("centroid") if component else None
    return {
        "date": RUN_DATE,
        "repair_id": REPAIR_ID,
        "cisi": cisi,
        "role": role_for_cisi(cisi),
        "crop_kind": "object_panel_candidate",
        "crop_stage": "panel_crop_repair_v2_preflight_inventory",
        "control_subtype": control_subtype_for_cisi(cisi),
        "denominator_group": denominator_group_for_cisi(cisi),
        "denominator_inclusion": denominator_inclusion_for_cisi(cisi),
        "match_set_id": f"{cisi}|{route['volume']}|n{route['page_index']}|r{route['route_rank']}",
        "matched_target_cisi": cisi if cisi in PRIMARY_TARGET_CISIS else "",
        "match_basis": "public_cisi_ocr_label_route_then_label_excluded_component_or_relative_panel_crop",
        "source_family_key": f"{route.get('site', '')}|{route.get('type', '')}|{route.get('symbol', '')}|{route['volume']}|n{route['page_index']}",
        "near_duplicate_group_id": "",
        "route_rank": route["route_rank"],
        "queue_rank": route["queue_rank"],
        "volume": route["volume"],
        "page_index": route["page_index"],
        "source_url": route["source_url"],
        "match_text": route["match_text"],
        "source_grade_status": route["source_grade_status"],
        "source_page": route["local_page_path"],
        "source_page_sha256": page_sha,
        "parent_crop_sha256": route.get("enhanced_crop_sha256", ""),
        "image_width": page_image.width,
        "image_height": page_image.height,
        "xml_width": page_info["xml_width"] if page_info else "",
        "xml_height": page_info["xml_height"] if page_info else "",
        "ocr_label_coords_xml": route["ocr_label_coords"],
        "label_box_image_coords": box_str(label_box),
        "label_box_width": label_box[2] - label_box[0],
        "label_box_height": label_box[3] - label_box[1],
        "label_match_compactness_status": label_compactness,
        "method": method,
        "candidate_rank": candidate_rank,
        "crop_box_xyxy": box_str(crop_box),
        "crop_width": crop_w,
        "crop_height": crop_h,
        "crop_aspect_ratio": round(crop_w / max(1, crop_h), 6),
        "dark_pixel_fraction": dark_fraction(crop),
        "component_area_downsampled": component["area"] if component else "",
        "component_bbox_image_coords": box_str(component_box) if component_box else "",
        "component_centroid_image_coords": "|".join(str(value) for value in centroid) if centroid else "",
        "component_score": component["score"] if component else "",
        "ocr_word_overlap_count": word_overlap_count,
        "label_box_overlap_fraction": round(label_overlap, 6),
        "label_exclusion_status": label_status,
        "candidate_preflight_status": preflight,
        "source_crop": str(source_path.relative_to(ROOT)).replace("\\", "/"),
        "enhanced_crop": str(enhanced_path.relative_to(ROOT)).replace("\\", "/"),
        "source_crop_sha256": sha256_file(source_path),
        "enhanced_crop_sha256": sha256_file(enhanced_path),
        "notes": (
            "Object-panel repair candidate only. It is not a blind packet row until visual preflight confirms no catalogue "
            "label, exactly one comparable object/signband, and no source-selection leakage."
        ),
        "accepted_claims_increment": 0,
    }


def candidates_for_route(
    route: dict[str, str],
    page_words: dict[tuple[str, int], dict[str, object]],
) -> list[dict[str, object]]:
    page_path = ROOT / route["local_page_path"]
    page_image = Image.open(page_path).convert("RGB")
    page_sha = sha256_file(page_path)
    page_info = page_words.get((route["volume"], int(route["page_index"])))
    xml_label = parse_box(route["ocr_label_coords"])
    if page_info:
        label_box = scale_box(
            xml_label,
            int(page_info["xml_width"]),
            int(page_info["xml_height"]),
            page_image.width,
            page_image.height,
        )
    else:
        label_box = xml_label
    label_box = clamp_box(label_box, page_image.width, page_image.height)
    word_boxes = scaled_word_boxes(page_info, page_image.size)
    label_compactness = compactness_status(label_box)
    rows: list[dict[str, object]] = []

    fixed = fixed_relative_boxes(label_box, page_image.size)
    for rank, candidate in enumerate(fixed, start=1):
        rows.append(
            write_candidate(
                route,
                page_image,
                page_sha,
                page_info,
                word_boxes,
                label_box,
                label_compactness,
                candidate["method"],
                rank,
                candidate["box"],
                None,
            )
        )
    cluster_offset = 20
    for fixed_candidate in fixed[:2]:
        clusters = horizontal_dark_cluster_candidates(
            page_image,
            fixed_candidate["box"],
            word_boxes,
            label_box,
            f"{fixed_candidate['method']}_darkrow",
        )
        for cluster in clusters[:4]:
            rows.append(
                write_candidate(
                    route,
                    page_image,
                    page_sha,
                    page_info,
                    word_boxes,
                    label_box,
                    label_compactness,
                    cluster["method"],
                    cluster_offset,
                    cluster["box"],
                    cluster,
                )
            )
            cluster_offset += 1

    search_box = expand_box(label_box, 1150, 1300, page_image.width, page_image.height)
    components = component_candidates(page_image, search_box, word_boxes, label_box)
    selected_components: list[tuple[str, dict[str, object]]] = []
    if components:
        selected_components.append(("component_nearest_high_score", components[0]))
        above = [component for component in components if component["position"] == "above"]
        below = [component for component in components if component["position"] == "below"]
        if above:
            selected_components.append(("component_above_high_score", above[0]))
        if below:
            selected_components.append(("component_below_high_score", below[0]))
        largest = sorted(components, key=lambda component: -int(component["area"]))[0]
        selected_components.append(("component_largest_in_search", largest))

    seen_component_methods: set[tuple[str, str]] = set()
    for offset, (method, component) in enumerate(selected_components, start=4):
        clipped_box = clip_component_box_away_from_text(
            component["raw_component_box"],
            label_box,
            word_boxes,
            page_image.width,
            page_image.height,
        )
        key = (method, box_str(clipped_box))
        if key in seen_component_methods:
            continue
        seen_component_methods.add(key)
        rows.append(
            write_candidate(
                route,
                page_image,
                page_sha,
                page_info,
                word_boxes,
                label_box,
                label_compactness,
                method,
                offset,
                clipped_box,
                component,
            )
        )
    return rows


def route_sort_key(row: dict[str, str]) -> tuple[int, int, int]:
    compact_penalty = 0
    try:
        label_box = parse_box(row["ocr_label_coords"])
        compact_penalty = 1 if (label_box[3] - label_box[1]) > 120 else 0
    except Exception:
        compact_penalty = 2
    grade_penalty = 0 if row["source_grade_status"].startswith("public_cisi_plate_route_candidate") else 1
    return grade_penalty, compact_penalty, int(row["route_rank"])


def focus_routes() -> list[dict[str, str]]:
    by_cisi: dict[str, list[dict[str, str]]] = {}
    for row in read_csv(ROUTES_CSV):
        cisi = row["representative_cisi"]
        if cisi not in FOCUS_CISIS:
            continue
        if not row["source_grade_status"].startswith("public_cisi_plate_route_candidate"):
            continue
        if row["route_status"] != "downloaded_and_cropped":
            continue
        by_cisi.setdefault(cisi, []).append(row)
    routes = []
    for cisi in sorted(by_cisi):
        rows = sorted(by_cisi[cisi], key=route_sort_key)
        routes.extend(rows[:3])
    return routes


def make_contact_sheet(rows: list[dict[str, object]], output: Path, max_items: int, title: str) -> None:
    selected = rows[:max_items]
    if not selected:
        return
    try:
        font = ImageFont.truetype("arial.ttf", 18)
        small = ImageFont.truetype("arial.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
        small = ImageFont.load_default()
    cell_w = 560
    cell_h = 500
    cols = 3
    header_h = 44
    sheet = Image.new(
        "RGB",
        (cols * cell_w, header_h + ((len(selected) + cols - 1) // cols) * cell_h),
        "white",
    )
    draw = ImageDraw.Draw(sheet)
    draw.text((16, 12), title, fill=(0, 0, 0), font=font)
    for index, row in enumerate(selected):
        image = Image.open(ROOT / str(row["enhanced_crop"])).convert("RGB")
        image.thumbnail((cell_w - 28, 340), Image.Resampling.LANCZOS)
        col = index % cols
        row_index = index // cols
        x = col * cell_w + 14
        y = header_h + row_index * cell_h + 120
        tx = col * cell_w + 14
        ty = header_h + row_index * cell_h + 12
        label = (
            f"{row['cisi']} {row['role'].replace('_candidate', '')} "
            f"r{row['route_rank']} {row['method']}"
        )
        draw.text((tx, ty), label[:64], fill=(0, 0, 0), font=small)
        draw.text(
            (tx, ty + 22),
            f"label {row['label_exclusion_status']} words {row['ocr_word_overlap_count']} dark {row['dark_pixel_fraction']}",
            fill=(30, 30, 30),
            font=small,
        )
        draw.text((tx, ty + 44), str(row["candidate_preflight_status"])[:70], fill=(95, 40, 40), font=small)
        draw.text((tx, ty + 66), str(row["match_text"])[:70], fill=(70, 70, 70), font=small)
        sheet.paste(image, (x, y))
        draw.rectangle((x - 1, y - 1, x + image.width + 1, y + image.height + 1), outline=(180, 180, 180), width=1)
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)


def best_candidate_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    usable = [
        row
        for row in rows
        if row["candidate_preflight_status"] == "candidate_requires_visual_label_leak_and_single_panel_preflight"
    ]
    method_priority = {
        "component_nearest_high_score": 0,
        "component_above_high_score": 1,
        "component_below_high_score": 2,
        "component_largest_in_search": 3,
        "above_label_wide_darkrow_above_cluster": 4,
        "below_label_wide_darkrow_below_cluster": 5,
        "above_label_wide_darkrow_below_cluster": 6,
        "below_label_wide_darkrow_above_cluster": 7,
        "above_label_wide": 8,
        "below_label_wide": 9,
        "around_label_without_center_label": 10,
    }
    result = []
    for cisi in sorted({row["cisi"] for row in rows}):
        cisi_rows = [row for row in usable if row["cisi"] == cisi]
        if not cisi_rows:
            cisi_rows = [row for row in rows if row["cisi"] == cisi]
        cisi_rows = sorted(
            cisi_rows,
            key=lambda row: (
                0 if row["candidate_preflight_status"] == "candidate_requires_visual_label_leak_and_single_panel_preflight" else 1,
                0 if str(row["method"]).startswith("component") else 1,
                int(row["ocr_word_overlap_count"]),
                method_priority.get(str(row["method"]), 99),
                -float(row["component_score"] or 0),
            ),
        )
        result.append(cisi_rows[0])
    return result


def main() -> None:
    ensure_dirs()
    page_words = load_page_words()
    rows: list[dict[str, object]] = []
    routes = focus_routes()
    for route in routes:
        rows.extend(candidates_for_route(route, page_words))
    write_csv(CANDIDATES_CSV, rows, CANDIDATE_FIELDS)
    best_rows = best_candidate_rows(rows)
    sorted_all = sorted(
        rows,
        key=lambda row: (
            row["role"],
            row["cisi"],
            int(row["route_rank"]),
            int(row["candidate_rank"]),
        ),
    )
    make_contact_sheet(sorted_all, CONTACT_ALL, 90, "Directionality object-panel repair candidates; visual preflight only")
    make_contact_sheet(best_rows, CONTACT_BEST, 40, "Best candidate per CISI by automatic heuristic; not reviewer-ready")

    by_role: dict[str, int] = {}
    by_status: dict[str, int] = {}
    by_cisi: dict[str, int] = {}
    for row in rows:
        by_role[str(row["role"])] = by_role.get(str(row["role"]), 0) + 1
        by_status[str(row["candidate_preflight_status"])] = by_status.get(str(row["candidate_preflight_status"]), 0) + 1
        by_cisi[str(row["cisi"])] = by_cisi.get(str(row["cisi"]), 0) + 1
    best_by_role: dict[str, int] = {}
    for row in best_rows:
        best_by_role[str(row["role"])] = best_by_role.get(str(row["role"]), 0) + 1

    summary = {
        "date": RUN_DATE,
        "repair_id": REPAIR_ID,
        "status": "candidate_panel_crops_created_for_visual_preflight_no_claim_promotion",
        "purpose": (
            "Repair the v2c failure mode by replacing masked page-context crops with explicit object-panel crop candidates, "
            "clipping component crops away from OCR text, and recording crop-world/denominator fields. This is a preflight "
            "inventory, not a blind packet."
        ),
        "root_cause_reconstructed": [
            "v2b leaked source labels in real negatives.",
            "v2c fixed the DjVu five-coordinate OCR parser and padded masks, but the underlying crop was still page context.",
            "A second route hazard remains: OCR label matches can be non-compact if words from different page positions are stitched together.",
            "The repair therefore emits crop candidates only when their label box and all OCR word boxes are excluded, and records compactness/word-overlap/crop-world fields for hostile review.",
        ],
        "counts": {
            "focus_cisis_requested": len(FOCUS_CISIS),
            "focus_cisis_with_plate_routes": len({route["representative_cisi"] for route in routes}),
            "plate_routes_used_max_three_per_cisi": len(routes),
            "candidate_rows": len(rows),
            "best_candidate_rows": len(best_rows),
            "best_candidate_rows_preflight_geometry_clean": sum(
                1
                for row in best_rows
                if row["candidate_preflight_status"] == "candidate_requires_visual_label_leak_and_single_panel_preflight"
            ),
            "accepted_claims_increment": 0,
        },
        "by_role": by_role,
        "best_by_role": best_by_role,
        "by_preflight_status": by_status,
        "candidate_rows_by_cisi": by_cisi,
        "admissibility_gate": [
            "No row is reviewer-ready from this script alone.",
            "A future blind packet may use only rows whose crop geometrically excludes OCR text, visibly excludes catalogue labels, and contains exactly one comparable object/signband.",
            "Targets and fixed real negatives must use the same crop_kind/crop_stage and comparable crop dimensions; target signband strips cannot be mixed with negative page panels.",
            "The fixed real-negative denominator must remain at least 12 unique CISIs, with no duplicate image hashes, no label leak, and no target-like uncertainty.",
            "If visual preflight cannot produce 4 targets and 12 real negatives under those constraints, the directionality packet remains retracted/preflight-failed.",
        ],
        "outputs": {
            "candidates_csv": str(CANDIDATES_CSV.relative_to(ROOT)).replace("\\", "/"),
            "summary_json": str(SUMMARY_JSON.relative_to(ROOT)).replace("\\", "/"),
            "all_candidates_contact_sheet": str(CONTACT_ALL.relative_to(ROOT)).replace("\\", "/"),
            "best_candidates_contact_sheet": str(CONTACT_BEST.relative_to(ROOT)).replace("\\", "/"),
            "candidate_crop_dir": str(CROP_DIR.relative_to(ROOT)).replace("\\", "/"),
        },
        "interpretation_boundary": (
            "The artifacts validate no source directionality, sign identity, sign meaning, language family, phonetic value, "
            "translation, or structural claim. They only expose candidate crop geometry for the forger/skeptic gate."
        ),
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
