from __future__ import annotations

import csv
import hashlib
import html
import json
import math
import random
import re
import ssl
import time
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps


DATE = date.today().isoformat()
BASE_URL = "https://www.indoskript.phil.uni-wuerzburg.de"
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "data" / "brahmi"
TMP = ROOT / "tmp"
IMG_DIR = OUT / "indoskript_letter_images_v2"
TOKEN_DIR = OUT / "source_token_crops_v2"
RNG_SEED = 20260530
EARLY_DATE_MAX = -100
EARLY_MANUSCRIPT_LIMIT = 36
CANVAS = 64
FEATURE_CANVAS = 32
TOP_K = 10
NULL_ITERATIONS = 200
LABEL_NULL_ITERATIONS = 1000

ANSWER_KEY_FILES = [
    ROOT / "data" / "open_prototype" / "reports" / "campaign_002_y_branch_gap_blind_answer_key.csv",
    ROOT / "data" / "open_prototype" / "reports" / "effective_unicity_m70_blind_token_box_answer_key.csv",
    ROOT / "data" / "open_prototype" / "reports" / "effective_unicity_directionality_blind_packet_answer_key.csv",
    ROOT / "data" / "open_prototype" / "reports" / "effective_unicity_directionality_blind_packet_v2_answer_key.csv",
    ROOT / "data" / "open_prototype" / "reports" / "effective_unicity_directionality_blind_packet_v2b_answer_key.csv",
    ROOT / "data" / "open_prototype" / "reports" / "effective_unicity_directionality_blind_packet_v2c_answer_key.csv",
    ROOT / "data" / "open_prototype" / "reports" / "source_box_negative_control_v2_m381_answer_key.csv",
]

LEGACY_TOKEN_PROBES = [
    {
        "source": "legacy_token_probe",
        "cisi": "M-37",
        "sign_id": "220",
        "path": TMP / "parpola_sign60_local220_strict_probe" / "neutral_packet" / "S009.png",
        "note": "token-isolated local 220 probe from prior strict packet",
    },
    {
        "source": "legacy_token_probe",
        "cisi": "H-938",
        "sign_id": "220",
        "path": TMP / "parpola_sign60_local220_strict_probe" / "neutral_packet" / "S010.png",
        "note": "token-isolated local 220 probe from prior strict packet",
    },
    {
        "source": "legacy_token_probe",
        "cisi": "H-940",
        "sign_id": "220",
        "path": TMP / "parpola_sign60_local220_strict_probe" / "neutral_packet" / "S011.png",
        "note": "token-isolated local 220 probe from prior strict packet",
    },
    {
        "source": "legacy_token_probe",
        "cisi": "H-942",
        "sign_id": "220",
        "path": TMP / "parpola_sign60_local220_strict_probe" / "neutral_packet" / "S012.png",
        "note": "stress local 220 probe retained as hostile family member",
    },
    {
        "source": "legacy_token_probe",
        "cisi": "H-2148",
        "sign_id": "110",
        "path": TMP / "h2148_h2100_h2152_110_route" / "derived" / "h2148_fig14_item1_left_single_panel_no_label_crop.png",
        "note": "token-isolated local 110 source panel candidate",
    },
]


@dataclass
class FeatureRecord:
    record_id: str
    label: str
    source_class: str
    path: Path
    vector: np.ndarray
    mask: np.ndarray
    metrics: dict
    meta: dict


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_id(parts: list[str]) -> str:
    return hashlib.sha1("\u241f".join(parts).encode("utf-8")).hexdigest()[:16]


def fetch_text(url: str, fetch_log: list[dict]) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "ivc-brahmi-source-token-gate-v2/2026-05-29"})
    with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=30) as res:
        data = res.read()
        status = getattr(res, "status", 200)
    fetch_log.append(
        {
            "url": url,
            "status": status,
            "byte_length": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "kind": "html",
        }
    )
    time.sleep(0.02)
    return data.decode("utf-8", errors="replace")


def fetch_binary(url: str, dest: Path, fetch_log: list[dict]) -> str:
    if dest.exists() and dest.stat().st_size > 0:
        data = dest.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        fetch_log.append(
            {
                "url": url,
                "status": "cached",
                "byte_length": len(data),
                "sha256": digest,
                "kind": "image",
            }
        )
        return digest
    req = urllib.request.Request(url, headers={"User-Agent": "ivc-brahmi-source-token-gate-v2/2026-05-29"})
    with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=30) as res:
        data = res.read()
        status = getattr(res, "status", 200)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    fetch_log.append(
        {
            "url": url,
            "status": status,
            "byte_length": len(data),
            "sha256": digest,
            "kind": "image",
        }
    )
    time.sleep(0.01)
    return digest


def strip_tags(value: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", value)).strip()


def parse_letters_table(text: str, manuscript: dict) -> list[dict]:
    rows: list[dict] = []
    block_re = re.compile(r'<div class="letter-card-table"[\s\S]*?</div> <!-- letter-card -->')
    primary_re = re.compile(
        r'<img src="/img/letters/(\d+)\.png" class="letter-card-image-img" alt="">[\s\S]*?<strong>([\s\S]*?)</strong>'
    )
    variant_re = re.compile(
        r'<img src="/img/letters/(\d+)\.png" class="letter-card-image-img" alt=""><br/><span[^>]*>([\s\S]*?)</span>'
    )
    for block_index, block_match in enumerate(block_re.finditer(text)):
        block = block_match.group(0)
        primary = primary_re.search(block)
        if primary:
            image_id = primary.group(1)
            label = strip_tags(primary.group(2))
            if label and image_id != "0":
                rows.append(
                    {
                        **manuscript,
                        "letter_image_id": image_id,
                        "transliteration": label,
                        "variant_role": "primary",
                        "table_block_index": block_index,
                        "image_url": f"{BASE_URL}/img/letters/{image_id}.png",
                    }
                )
        for variant_index, variant in enumerate(variant_re.finditer(block)):
            image_id = variant.group(1)
            label = strip_tags(variant.group(2))
            if label and image_id != "0":
                rows.append(
                    {
                        **manuscript,
                        "letter_image_id": image_id,
                        "transliteration": label,
                        "variant_role": f"variant_{variant_index + 1}",
                        "table_block_index": block_index,
                        "image_url": f"{BASE_URL}/img/letters/{image_id}.png",
                    }
                )
    return rows


def parse_signs(text: str) -> list[str]:
    return re.findall(r"\d{3}", text or "")


def open_gray(path: Path) -> np.ndarray:
    img = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    bg.alpha_composite(img)
    return np.asarray(ImageOps.grayscale(bg)).astype(np.uint8)


def otsu_threshold(arr: np.ndarray) -> int:
    hist = np.bincount(arr.reshape(-1), minlength=256).astype(np.float64)
    total = arr.size
    sum_total = float(np.dot(np.arange(256), hist))
    sum_b = 0.0
    w_b = 0.0
    best = 127
    best_var = -1.0
    for t in range(256):
        w_b += hist[t]
        if w_b <= 0:
            continue
        w_f = total - w_b
        if w_f <= 0:
            break
        sum_b += t * hist[t]
        m_b = sum_b / w_b
        m_f = (sum_total - sum_b) / w_f
        between = w_b * w_f * (m_b - m_f) ** 2
        if between > best_var:
            best_var = between
            best = t
    return best


def raw_mask(path: Path) -> tuple[np.ndarray, np.ndarray, dict]:
    arr = open_gray(path)
    median = float(np.median(arr))
    mad = float(np.median(np.abs(arr.astype(np.float32) - median)))
    threshold = max(18.0, min(60.0, 3.0 * mad))
    if median > 228:
        mask = arr < (median - threshold)
    else:
        otsu = otsu_threshold(arr)
        dark = arr < otsu
        light = arr > otsu
        mask = dark if dark.mean() < light.mean() else light
    fill = float(mask.mean())
    if fill < 0.003 or fill > 0.55:
        otsu = otsu_threshold(arr)
        dark = arr < otsu
        light = arr > otsu
        mask = dark if dark.mean() < light.mean() else light
    coords = np.argwhere(mask)
    metrics = {
        "bbox_w": 0,
        "bbox_h": 0,
        "aspect": 0.0,
        "ink_density_raw": fill,
    }
    if coords.size:
        y0, x0 = coords.min(axis=0)
        y1, x1 = coords.max(axis=0) + 1
        metrics.update(
            {
                "bbox_w": int(x1 - x0),
                "bbox_h": int(y1 - y0),
                "aspect": float((x1 - x0) / max(y1 - y0, 1)),
                "bbox": [int(x0), int(y0), int(x1), int(y1)],
            }
        )
    return arr, mask.astype(bool), metrics


def normalized_mask_from_mask(mask: np.ndarray, canvas: int = CANVAS) -> tuple[np.ndarray, dict]:
    coords = np.argwhere(mask)
    if coords.size == 0:
        return np.zeros((canvas, canvas), dtype=np.float32), {
            "bbox_w": 0,
            "bbox_h": 0,
            "aspect": 0.0,
            "ink_density": 0.0,
        }
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1
    crop = mask[y0:y1, x0:x1].astype(np.uint8) * 255
    pil = Image.fromarray(crop, mode="L")
    w, h = pil.size
    scale = min((canvas - 8) / max(w, 1), (canvas - 8) / max(h, 1))
    nw = max(1, int(round(w * scale)))
    nh = max(1, int(round(h * scale)))
    pil = pil.resize((nw, nh), Image.Resampling.LANCZOS)
    out = Image.new("L", (canvas, canvas), 0)
    out.paste(pil, ((canvas - nw) // 2, (canvas - nh) // 2))
    out_arr = np.asarray(out).astype(np.float32) / 255.0
    return out_arr, {
        "bbox_w": int(w),
        "bbox_h": int(h),
        "aspect": float(w / h) if h else 0.0,
        "ink_density": float(out_arr.mean()),
    }


def image_to_mask(path: Path) -> tuple[np.ndarray, dict]:
    _, mask, _ = raw_mask(path)
    return normalized_mask_from_mask(mask)


def feature_from_mask(mask: np.ndarray, metrics: dict) -> np.ndarray:
    img = Image.fromarray((mask * 255).astype(np.uint8), mode="L").resize(
        (FEATURE_CANVAS, FEATURE_CANVAS), Image.Resampling.LANCZOS
    )
    pix = np.asarray(img).astype(np.float32).reshape(-1) / 255.0
    ys, xs = np.nonzero(mask > 0.1)
    if len(xs) == 0:
        scalars = np.zeros(18, dtype=np.float32)
    else:
        x = xs.astype(np.float32) / max(mask.shape[1] - 1, 1)
        y = ys.astype(np.float32) / max(mask.shape[0] - 1, 1)
        cx = float(x.mean())
        cy = float(y.mean())
        sx = float(x.std())
        sy = float(y.std())
        cov = float(((x - cx) * (y - cy)).mean())
        row_profile = mask.mean(axis=1)
        col_profile = mask.mean(axis=0)
        row_bins = np.array_split(row_profile, 4)
        col_bins = np.array_split(col_profile, 4)
        scalars = np.array(
            [
                metrics["aspect"] / 4.0,
                metrics["ink_density"] * 4.0,
                cx,
                cy,
                sx,
                sy,
                cov,
                math.log1p(metrics["bbox_w"] * metrics["bbox_h"]) / 10.0,
                *[float(b.mean()) * 4.0 for b in row_bins],
                *[float(b.mean()) * 4.0 for b in col_bins],
                float((mask[:, : mask.shape[1] // 2].mean() - mask[:, mask.shape[1] // 2 :].mean()) * 4.0),
                float((mask[: mask.shape[0] // 2, :].mean() - mask[mask.shape[0] // 2 :, :].mean()) * 4.0),
            ],
            dtype=np.float32,
        )
    vec = np.concatenate([pix, scalars])
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.astype(np.float32)


def record_feature(record_id: str, label: str, source_class: str, path: Path, meta: dict | None = None) -> FeatureRecord | None:
    if not path.exists() or path.stat().st_size == 0:
        return None
    mask, metrics = image_to_mask(path)
    if metrics["ink_density"] <= 0:
        return None
    return FeatureRecord(
        record_id=record_id,
        label=label,
        source_class=source_class,
        path=path,
        vector=feature_from_mask(mask, metrics),
        mask=mask,
        metrics=metrics,
        meta=meta or {},
    )


def crop_token(raw_arr: np.ndarray, raw_mask_arr: np.ndarray, x0: int, x1: int, dest: Path) -> tuple[np.ndarray, dict]:
    submask = raw_mask_arr[:, x0:x1]
    coords = np.argwhere(submask)
    if coords.size == 0:
        dest.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(raw_arr[:, x0:x1]).save(dest)
        return np.zeros((CANVAS, CANVAS), dtype=np.float32), {"bbox_w": 0, "bbox_h": 0, "aspect": 0.0, "ink_density": 0.0}
    y0, sx0 = coords.min(axis=0)
    y1, sx1 = coords.max(axis=0) + 1
    pad = 3
    y0 = max(0, int(y0) - pad)
    y1 = min(raw_arr.shape[0], int(y1) + pad)
    abs_x0 = max(0, x0 + int(sx0) - pad)
    abs_x1 = min(raw_arr.shape[1], x0 + int(sx1) + pad)
    token_arr = raw_arr[y0:y1, abs_x0:abs_x1]
    token_mask = raw_mask_arr[y0:y1, abs_x0:abs_x1]
    dest.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(token_arr).save(dest)
    return normalized_mask_from_mask(token_mask)


def segment_source_crop(path: Path, expected_count: int) -> tuple[str, list[tuple[int, int]], dict]:
    if expected_count <= 0 or not path.exists():
        return "missing_or_zero_expected", [], {}
    raw_arr, mask, metrics = raw_mask(path)
    coords = np.argwhere(mask)
    if coords.size == 0:
        return "no_ink", [], metrics
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1
    x0 = max(0, int(x0) - 2)
    x1 = min(mask.shape[1], int(x1) + 2)
    cropped = mask[:, x0:x1]
    proj = cropped.sum(axis=0).astype(np.float32)
    if len(proj) < expected_count * 3:
        return "too_narrow", [], metrics
    smooth = np.convolve(proj, np.ones(5, dtype=np.float32) / 5.0, mode="same")
    low = max(1.0, float(np.percentile(smooth[smooth > 0], 18)) if np.any(smooth > 0) else 1.0)
    blank = smooth <= low
    gaps: list[tuple[int, int, int]] = []
    start = None
    for i, is_blank in enumerate(blank):
        if is_blank and start is None:
            start = i
        elif not is_blank and start is not None:
            if i - start >= max(2, int(round(cropped.shape[1] * 0.008))):
                gaps.append((start, i, i - start))
            start = None
    if start is not None and len(blank) - start >= 2:
        gaps.append((start, len(blank), len(blank) - start))
    internal_gaps = [
        gap for gap in gaps
        if gap[0] > cropped.shape[1] * 0.02 and gap[1] < cropped.shape[1] * 0.98
    ]
    if len(internal_gaps) < expected_count - 1:
        return "not_enough_projection_gaps", [], {**metrics, "gap_count": len(internal_gaps)}
    cuts = sorted(((a + b) // 2 for a, b, _ in sorted(internal_gaps, key=lambda g: g[2], reverse=True)[: expected_count - 1]))
    bounds = [0, *cuts, cropped.shape[1]]
    segments = []
    for i in range(len(bounds) - 1):
        a = bounds[i]
        b = bounds[i + 1]
        if b - a < 3:
            return "degenerate_segment", [], {**metrics, "gap_count": len(internal_gaps)}
        segment_mask = cropped[:, a:b]
        if segment_mask.mean() < 0.001:
            return "empty_segment", [], {**metrics, "gap_count": len(internal_gaps)}
        segments.append((x0 + a, x0 + b))
    return "exact_projection_gap_count", segments, {**metrics, "gap_count": len(internal_gaps)}


def nearest_neighbors(probe: FeatureRecord, brahmi: list[FeatureRecord], k: int = TOP_K) -> list[tuple[FeatureRecord, float]]:
    scores = [(rec, float(1.0 - np.dot(probe.vector, rec.vector))) for rec in brahmi]
    scores.sort(key=lambda item: item[1])
    return scores[:k]


def distance_to_label(probe_vec: np.ndarray, brahmi_by_label: dict[str, list[FeatureRecord]], label: str) -> float:
    records = brahmi_by_label.get(label, [])
    if not records:
        return 9.0
    return min(float(1.0 - np.dot(probe_vec, rec.vector)) for rec in records)


def perturb_mask(mask: np.ndarray, rng: random.Random) -> np.ndarray:
    img = Image.fromarray((mask * 255).astype(np.uint8), mode="L")
    angle = rng.uniform(-45.0, 45.0)
    img = img.rotate(angle, resample=Image.Resampling.BICUBIC, fillcolor=0)
    if rng.random() < 0.50:
        img = img.filter(ImageFilter.MaxFilter(size=3))
    if rng.random() < 0.50:
        img = img.filter(ImageFilter.MinFilter(size=3))
    sx = rng.uniform(0.62, 1.42)
    sy = rng.uniform(0.62, 1.42)
    nw = max(1, int(round(CANVAS * sx)))
    nh = max(1, int(round(CANVAS * sy)))
    img = img.resize((nw, nh), Image.Resampling.BICUBIC)
    crop = Image.new("L", (CANVAS, CANVAS), 0)
    x = rng.randint(min(0, CANVAS - nw), max(0, CANVAS - nw))
    y = rng.randint(min(0, CANVAS - nh), max(0, CANVAS - nh))
    crop.paste(img, (x, y))
    arr = np.asarray(crop).astype(np.float32) / 255.0
    return (arr > rng.uniform(0.15, 0.48)).astype(np.float32)


def build_brahmi_features(fetch_log: list[dict]) -> tuple[list[dict], list[FeatureRecord]]:
    manuscript_rows = read_csv(OUT / "indoskript_brahmi_manuscripts.csv")
    if not manuscript_rows:
        raise RuntimeError("Missing indoskript_brahmi_manuscripts.csv; run the first gate before v2.")
    for row in manuscript_rows:
        row["date"] = int(row["date"])
    early = sorted([row for row in manuscript_rows if int(row["date"]) <= EARLY_DATE_MAX], key=lambda row: (int(row["date"]), row["manuscript_id"]))
    early = early[:EARLY_MANUSCRIPT_LIMIT]
    glyph_rows: list[dict] = []
    seen = set()
    for manuscript in early:
        url = f"{BASE_URL}/letters/table/{manuscript['manuscript_id']}"
        text = fetch_text(url, fetch_log)
        for row in parse_letters_table(text, manuscript):
            key = (row["manuscript_id"], row["letter_image_id"], row["transliteration"])
            if key in seen:
                continue
            seen.add(key)
            glyph_rows.append(row)
    print(f"[brahmi-v2] parsed {len(glyph_rows)} early Brahmi glyph rows from {len(early)} manuscripts", flush=True)
    features: list[FeatureRecord] = []
    out_rows: list[dict] = []
    for index, row in enumerate(glyph_rows, start=1):
        if index == 1 or index % 100 == 0 or index == len(glyph_rows):
            print(f"[brahmi-v2] feature extraction {index}/{len(glyph_rows)}", flush=True)
        dest = IMG_DIR / f"{row['letter_image_id']}.png"
        digest = fetch_binary(row["image_url"], dest, fetch_log)
        feature = record_feature(
            record_id=(
                f"brahmi_v2_{row['manuscript_id']}_{row['letter_image_id']}_"
                f"{stable_id([row['transliteration'], row['variant_role'], str(row['table_block_index'])])}"
            ),
            label=row["transliteration"],
            source_class="early_brahmi_indoskript_v2",
            path=dest,
            meta=row,
        )
        if feature is None:
            continue
        features.append(feature)
        out_rows.append(
            {
                **row,
                "local_image_path": rel(dest),
                "sha256": digest,
                "bbox_w": feature.metrics["bbox_w"],
                "bbox_h": feature.metrics["bbox_h"],
                "aspect": f"{feature.metrics['aspect']:.6f}",
                "ink_density": f"{feature.metrics['ink_density']:.6f}",
            }
        )
    write_csv(
        OUT / "indoskript_brahmi_features_v2.csv",
        out_rows,
        [
            "manuscript_id",
            "name",
            "date",
            "place",
            "language",
            "dynasty",
            "details_url",
            "table_url",
            "letter_image_id",
            "transliteration",
            "variant_role",
            "table_block_index",
            "image_url",
            "local_image_path",
            "sha256",
            "bbox_w",
            "bbox_h",
            "aspect",
            "ink_density",
        ],
    )
    return out_rows, features


def source_rows_from_answer_keys() -> list[dict]:
    rows: list[dict] = []
    for key_path in ANSWER_KEY_FILES:
        for row in read_csv(key_path):
            target_text = row.get("target_text", "")
            signs = parse_signs(target_text)
            source_path_text = row.get("source_crop") or row.get("source_image") or ""
            if not signs or not source_path_text:
                continue
            if "synthetic" in row.get("role", "").lower() or "synthetic" in row.get("truth_class", "").lower():
                continue
            source_path = ROOT / source_path_text
            rows.append(
                {
                    "answer_key": rel(key_path),
                    "packet_id": row.get("packet_id", ""),
                    "blind_id": row.get("blind_id", ""),
                    "cisi": row.get("cisi", ""),
                    "role": row.get("role") or row.get("control_role", ""),
                    "truth_class": row.get("truth_class", ""),
                    "target_text": target_text,
                    "signs": signs,
                    "expected_count": int(row.get("expected_token_count") or len(signs)),
                    "source_path": source_path,
                    "source_status": row.get("source_status", ""),
                    "source_note": row.get("source_note") or row.get("expected_relation", ""),
                }
            )
    return rows


def build_source_tokens() -> tuple[list[dict], list[FeatureRecord], list[dict]]:
    TOKEN_DIR.mkdir(parents=True, exist_ok=True)
    source_rows = source_rows_from_answer_keys()
    segment_rows: list[dict] = []
    token_features: list[FeatureRecord] = []
    inventory_rows: list[dict] = []

    for src in source_rows:
        signs = src["signs"]
        status, segments, metrics = segment_source_crop(src["source_path"], src["expected_count"])
        inventory_rows.append(
            {
                "source_id": stable_id([src["answer_key"], src["blind_id"], src["target_text"], rel(src["source_path"])]),
                "answer_key": src["answer_key"],
                "packet_id": src["packet_id"],
                "blind_id": src["blind_id"],
                "cisi": src["cisi"],
                "role": src["role"],
                "truth_class": src["truth_class"],
                "target_text": src["target_text"],
                "expected_count": src["expected_count"],
                "catalog_sign_count": len(signs),
                "source_path": rel(src["source_path"]),
                "source_exists": src["source_path"].exists(),
                "segmentation_status": status,
                "segment_count": len(segments),
                "gap_count": metrics.get("gap_count", ""),
                "source_status": src["source_status"],
                "source_note": src["source_note"],
            }
        )
        if status != "exact_projection_gap_count" or len(segments) != len(signs):
            continue
        raw_arr, mask, _ = raw_mask(src["source_path"])
        for visual_index, (x0, x1) in enumerate(segments):
            token_crop = TOKEN_DIR / f"{src['cisi'].replace('-', '_')}_{src['blind_id']}_{visual_index + 1}_{stable_id([rel(src['source_path']), str(visual_index)])}.png"
            token_mask, token_metrics = crop_token(raw_arr, mask, x0, x1, token_crop)
            for policy, assigned_sign in [
                ("visual_ltr_catalog_order", signs[visual_index]),
                ("visual_ltr_catalog_reverse", list(reversed(signs))[visual_index]),
            ]:
                token_id = f"tok_{stable_id([src['packet_id'], src['blind_id'], str(visual_index), policy, assigned_sign])}"
                vector = feature_from_mask(token_mask, token_metrics)
                feature = FeatureRecord(
                    record_id=token_id,
                    label=assigned_sign,
                    source_class=f"source_token_{policy}",
                    path=token_crop,
                    vector=vector,
                    mask=token_mask,
                    metrics=token_metrics,
                    meta={
                        **src,
                        "visual_index": visual_index + 1,
                        "orientation_policy": policy,
                        "assigned_sign": assigned_sign,
                        "token_crop": rel(token_crop),
                    },
                )
                token_features.append(feature)
                segment_rows.append(
                    {
                        "token_id": token_id,
                        "packet_id": src["packet_id"],
                        "blind_id": src["blind_id"],
                        "cisi": src["cisi"],
                        "role": src["role"],
                        "truth_class": src["truth_class"],
                        "orientation_policy": policy,
                        "visual_index": visual_index + 1,
                        "assigned_sign": assigned_sign,
                        "target_text": src["target_text"],
                        "source_path": rel(src["source_path"]),
                        "token_crop": rel(token_crop),
                        "x0": x0,
                        "x1": x1,
                        "bbox_w": token_metrics["bbox_w"],
                        "bbox_h": token_metrics["bbox_h"],
                        "aspect": f"{token_metrics['aspect']:.6f}",
                        "ink_density": f"{token_metrics['ink_density']:.6f}",
                        "sha256": sha256_file(token_crop),
                        "admissibility": "projection_exact_count_unverified_token_identity",
                    }
                )

    for legacy in LEGACY_TOKEN_PROBES:
        feature = record_feature(
            f"legacy_{stable_id([legacy['cisi'], legacy['sign_id'], rel(legacy['path'])])}",
            legacy["sign_id"],
            "legacy_token_probe",
            legacy["path"],
            meta={
                "packet_id": "legacy_token_probe",
                "blind_id": legacy["cisi"],
                "cisi": legacy["cisi"],
                "role": "legacy_token_isolated_actual",
                "truth_class": "prior_actual_source_probe",
                "target_text": legacy["sign_id"],
                "visual_index": 1,
                "orientation_policy": "legacy_token_isolated",
                "assigned_sign": legacy["sign_id"],
                "source_note": legacy["note"],
            },
        )
        if feature is None:
            continue
        token_features.append(feature)
        segment_rows.append(
            {
                "token_id": feature.record_id,
                "packet_id": "legacy_token_probe",
                "blind_id": legacy["cisi"],
                "cisi": legacy["cisi"],
                "role": "legacy_token_isolated_actual",
                "truth_class": "prior_actual_source_probe",
                "orientation_policy": "legacy_token_isolated",
                "visual_index": 1,
                "assigned_sign": legacy["sign_id"],
                "target_text": legacy["sign_id"],
                "source_path": rel(legacy["path"]),
                "token_crop": rel(legacy["path"]),
                "x0": "",
                "x1": "",
                "bbox_w": feature.metrics["bbox_w"],
                "bbox_h": feature.metrics["bbox_h"],
                "aspect": f"{feature.metrics['aspect']:.6f}",
                "ink_density": f"{feature.metrics['ink_density']:.6f}",
                "sha256": sha256_file(legacy["path"]),
                "admissibility": "legacy_token_isolated_actual_probe",
            }
        )
    return inventory_rows, token_features, segment_rows


def summarize_families(token_features: list[FeatureRecord], neighbor_by_token: dict[str, list[tuple[FeatureRecord, float]]]) -> list[dict]:
    groups: dict[tuple[str, str], list[FeatureRecord]] = defaultdict(list)
    for feature in token_features:
        key = (feature.label, feature.meta.get("orientation_policy", ""))
        groups[key].append(feature)
    rows: list[dict] = []
    for (sign_id, policy), features in sorted(groups.items()):
        if len(features) < 2:
            continue
        top_labels = [neighbor_by_token[f.record_id][0][0].label for f in features if neighbor_by_token.get(f.record_id)]
        top_distances = [neighbor_by_token[f.record_id][0][1] for f in features if neighbor_by_token.get(f.record_id)]
        if not top_labels:
            continue
        counts = Counter(top_labels)
        modal_label, modal_count = counts.most_common(1)[0]
        modal_distances = [
            neighbor_by_token[f.record_id][0][1]
            for f in features
            if neighbor_by_token.get(f.record_id) and neighbor_by_token[f.record_id][0][0].label == modal_label
        ]
        rows.append(
            {
                "family_id": f"family_{stable_id([sign_id, policy])}",
                "sign_id": sign_id,
                "orientation_policy": policy,
                "sample_count": len(features),
                "cisis": "|".join(sorted(set(str(f.meta.get("cisi", "")) for f in features))),
                "token_ids": "|".join(f.record_id for f in features),
                "top1_label_counts": json.dumps(dict(counts), ensure_ascii=False, sort_keys=True),
                "modal_brahmi_label": modal_label,
                "modal_count": modal_count,
                "modal_share": f"{modal_count / len(features):.6f}",
                "mean_top1_distance": f"{float(np.mean(top_distances)):.6f}",
                "max_top1_distance": f"{float(np.max(top_distances)):.6f}",
                "mean_modal_distance": f"{float(np.mean(modal_distances)):.6f}" if modal_distances else "",
                "candidate_status": "needs_nulls",
            }
        )
    rows.sort(key=lambda row: (-int(row["modal_count"]), -int(row["sample_count"]), float(row["mean_top1_distance"])))
    return rows


def run_nulls(
    family_rows: list[dict],
    token_features: list[FeatureRecord],
    neighbor_by_token: dict[str, list[tuple[FeatureRecord, float]]],
    brahmi: list[FeatureRecord],
) -> tuple[list[dict], list[dict], list[dict]]:
    rng = random.Random(RNG_SEED)
    token_by_id = {feature.record_id: feature for feature in token_features}
    brahmi_by_label: dict[str, list[FeatureRecord]] = defaultdict(list)
    for rec in brahmi:
        brahmi_by_label[rec.label].append(rec)
    labels = [rec.label for rec in brahmi]
    brahmi_index_by_record_id = {rec.record_id: i for i, rec in enumerate(brahmi)}
    family_null_rows: list[dict] = []
    shape_null_rows: list[dict] = []
    label_null_rows: list[dict] = []

    for family in family_rows:
        token_ids = family["token_ids"].split("|")
        features = [token_by_id[token_id] for token_id in token_ids if token_id in token_by_id]
        modal_label = family["modal_brahmi_label"]
        observed_modal_count = int(family["modal_count"])
        observed_modal_share = float(family["modal_share"])
        observed_distances = [distance_to_label(feature.vector, brahmi_by_label, modal_label) for feature in features]
        observed_mean = float(np.mean(observed_distances))
        null_better = 0
        same_label_hits = 0
        total_shape = 0
        for feature in features:
            for iteration in range(NULL_ITERATIONS):
                perturbed = perturb_mask(feature.mask, rng)
                metrics = {
                    "aspect": feature.metrics.get("aspect", 0.0),
                    "ink_density": float(perturbed.mean()),
                    "bbox_w": feature.metrics.get("bbox_w", 0),
                    "bbox_h": feature.metrics.get("bbox_h", 0),
                }
                vec = feature_from_mask(perturbed, metrics)
                scores = [(rec, float(1.0 - np.dot(vec, rec.vector))) for rec in brahmi]
                scores.sort(key=lambda item: item[1])
                nearest_label = scores[0][0].label
                nearest_distance = scores[0][1]
                modal_distance = distance_to_label(vec, brahmi_by_label, modal_label)
                if modal_distance <= observed_mean:
                    null_better += 1
                if nearest_label == modal_label:
                    same_label_hits += 1
                total_shape += 1
                if iteration < 20:
                    shape_null_rows.append(
                        {
                            "family_id": family["family_id"],
                            "sign_id": family["sign_id"],
                            "orientation_policy": family["orientation_policy"],
                            "token_id": feature.record_id,
                            "iteration": iteration,
                            "modal_brahmi_label": modal_label,
                            "nearest_label": nearest_label,
                            "nearest_distance": f"{nearest_distance:.6f}",
                            "modal_distance": f"{modal_distance:.6f}",
                            "observed_family_mean_modal_distance": f"{observed_mean:.6f}",
                            "modal_distance_le_observed_mean": modal_distance <= observed_mean,
                        }
                    )
        label_null_ge = 0
        observed_top_glyph_indexes = [
            brahmi_index_by_record_id[neighbor_by_token[feature.record_id][0][0].record_id]
            for feature in features
            if neighbor_by_token.get(feature.record_id)
        ]
        for iteration in range(LABEL_NULL_ITERATIONS):
            shuffled = labels[:]
            rng.shuffle(shuffled)
            null_labels = [shuffled[idx] for idx in observed_top_glyph_indexes]
            if not null_labels:
                continue
            modal = Counter(null_labels).most_common(1)[0][1]
            if modal >= observed_modal_count:
                label_null_ge += 1
            if iteration < 50:
                label_null_rows.append(
                    {
                        "family_id": family["family_id"],
                        "iteration": iteration,
                        "observed_modal_count": observed_modal_count,
                        "null_modal_count": modal,
                        "null_ge_observed": modal >= observed_modal_count,
                    }
                )
        shape_modal_distance_le_observed_share = null_better / max(total_shape, 1)
        shape_nearest_same_modal_share = same_label_hits / max(total_shape, 1)
        label_null_ge_share = label_null_ge / LABEL_NULL_ITERATIONS
        if (
            len(features) >= 2
            and observed_modal_share >= 1.0
            and shape_modal_distance_le_observed_share <= 0.01
            and label_null_ge_share <= 0.01
        ):
            gate = "candidate_only_requires_manual_visual_descent_review"
        else:
            gate = "failed_shape_or_label_null"
        family_null_rows.append(
            {
                **family,
                "observed_mean_modal_distance": f"{observed_mean:.6f}",
                "shape_null_iterations": total_shape,
                "shape_modal_distance_le_observed_share": f"{shape_modal_distance_le_observed_share:.6f}",
                "shape_nearest_same_modal_share": f"{shape_nearest_same_modal_share:.6f}",
                "label_null_iterations": LABEL_NULL_ITERATIONS,
                "label_null_ge_observed_modal_count_share": f"{label_null_ge_share:.6f}",
                "gate_decision": gate,
                "accepted_phonetic_anchor": "false",
            }
        )
    return family_null_rows, shape_null_rows, label_null_rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fetch_log: list[dict] = []
    brahmi_rows, brahmi_features = build_brahmi_features(fetch_log)
    print(f"[brahmi-v2] retained {len(brahmi_features)} Brahmi features", flush=True)
    inventory_rows, token_features, segment_rows = build_source_tokens()
    print(f"[brahmi-v2] retained {len(token_features)} source-token features from {len(segment_rows)} segment rows", flush=True)

    neighbor_rows: list[dict] = []
    neighbor_by_token: dict[str, list[tuple[FeatureRecord, float]]] = {}
    for feature in token_features:
        neighbors = nearest_neighbors(feature, brahmi_features, TOP_K)
        neighbor_by_token[feature.record_id] = neighbors
        for rank, (brahmi, distance) in enumerate(neighbors, start=1):
            neighbor_rows.append(
                {
                    "token_id": feature.record_id,
                    "sign_id": feature.label,
                    "orientation_policy": feature.meta.get("orientation_policy", ""),
                    "cisi": feature.meta.get("cisi", ""),
                    "token_crop": rel(feature.path),
                    "rank": rank,
                    "distance": f"{distance:.6f}",
                    "brahmi_label": brahmi.label,
                    "brahmi_record_id": brahmi.record_id,
                    "brahmi_letter_image_id": brahmi.meta.get("letter_image_id", ""),
                    "brahmi_manuscript_id": brahmi.meta.get("manuscript_id", ""),
                    "brahmi_manuscript_name": brahmi.meta.get("name", ""),
                    "brahmi_date": brahmi.meta.get("date", ""),
                    "brahmi_place": brahmi.meta.get("place", ""),
                    "brahmi_image_url": brahmi.meta.get("image_url", ""),
                    "brahmi_local_image_path": rel(brahmi.path),
                }
            )

    family_rows = summarize_families(token_features, neighbor_by_token)
    print(f"[brahmi-v2] testing {len(family_rows)} sign/orientation families with >=2 samples", flush=True)
    family_null_rows, shape_null_rows, label_null_rows = run_nulls(family_rows, token_features, neighbor_by_token, brahmi_features)

    write_csv(
        OUT / "source_token_descent_inventory_v2.csv",
        inventory_rows,
        [
            "source_id",
            "answer_key",
            "packet_id",
            "blind_id",
            "cisi",
            "role",
            "truth_class",
            "target_text",
            "expected_count",
            "catalog_sign_count",
            "source_path",
            "source_exists",
            "segmentation_status",
            "segment_count",
            "gap_count",
            "source_status",
            "source_note",
        ],
    )
    write_csv(
        OUT / "source_token_segments_v2.csv",
        segment_rows,
        [
            "token_id",
            "packet_id",
            "blind_id",
            "cisi",
            "role",
            "truth_class",
            "orientation_policy",
            "visual_index",
            "assigned_sign",
            "target_text",
            "source_path",
            "token_crop",
            "x0",
            "x1",
            "bbox_w",
            "bbox_h",
            "aspect",
            "ink_density",
            "sha256",
            "admissibility",
        ],
    )
    write_csv(
        OUT / "source_token_brahmi_neighbors_v2.csv",
        neighbor_rows,
        [
            "token_id",
            "sign_id",
            "orientation_policy",
            "cisi",
            "token_crop",
            "rank",
            "distance",
            "brahmi_label",
            "brahmi_record_id",
            "brahmi_letter_image_id",
            "brahmi_manuscript_id",
            "brahmi_manuscript_name",
            "brahmi_date",
            "brahmi_place",
            "brahmi_image_url",
            "brahmi_local_image_path",
        ],
    )
    write_csv(
        OUT / "source_token_family_descent_summary_v2.csv",
        family_null_rows,
        [
            "family_id",
            "sign_id",
            "orientation_policy",
            "sample_count",
            "cisis",
            "token_ids",
            "top1_label_counts",
            "modal_brahmi_label",
            "modal_count",
            "modal_share",
            "mean_top1_distance",
            "max_top1_distance",
            "mean_modal_distance",
            "candidate_status",
            "observed_mean_modal_distance",
            "shape_null_iterations",
            "shape_modal_distance_le_observed_share",
            "shape_nearest_same_modal_share",
            "label_null_iterations",
            "label_null_ge_observed_modal_count_share",
            "gate_decision",
            "accepted_phonetic_anchor",
        ],
    )
    write_csv(
        OUT / "source_token_shape_null_iterations_v2.csv",
        shape_null_rows,
        [
            "family_id",
            "sign_id",
            "orientation_policy",
            "token_id",
            "iteration",
            "modal_brahmi_label",
            "nearest_label",
            "nearest_distance",
            "modal_distance",
            "observed_family_mean_modal_distance",
            "modal_distance_le_observed_mean",
        ],
    )
    write_csv(
        OUT / "source_token_label_null_iterations_v2.csv",
        label_null_rows,
        [
            "family_id",
            "iteration",
            "observed_modal_count",
            "null_modal_count",
            "null_ge_observed",
        ],
    )
    write_csv(
        OUT / "source_token_descent_fetch_log_v2.csv",
        fetch_log,
        ["url", "status", "byte_length", "sha256", "kind"],
    )

    accepted = [row for row in family_null_rows if row["gate_decision"] == "candidate_only_requires_manual_visual_descent_review"]
    summary = {
        "date": DATE,
        "status": "source_token_brahmi_descent_v2_no_accepted_anchor" if not accepted else "source_token_brahmi_descent_v2_candidate_only",
        "source": {
            "indoskript_homepage": BASE_URL,
            "early_date_max": EARLY_DATE_MAX,
            "early_manuscript_limit": EARLY_MANUSCRIPT_LIMIT,
            "answer_keys": [rel(path) for path in ANSWER_KEY_FILES],
            "segmentation_policy": "projection-gap tokenization only; rows whose visual gaps do not recover the exact catalog token count are rejected before Brahmi comparison.",
        },
        "counts": {
            "brahmi_feature_rows": len(brahmi_rows),
            "brahmi_features": len(brahmi_features),
            "source_answer_key_rows": len(inventory_rows),
            "source_rows_exact_projection_count": sum(1 for row in inventory_rows if row["segmentation_status"] == "exact_projection_gap_count"),
            "source_token_feature_records": len(token_features),
            "source_token_segment_rows": len(segment_rows),
            "family_rows_with_ge_2_samples": len(family_rows),
            "family_null_rows": len(family_null_rows),
            "candidate_only_rows": len(accepted),
            "accepted_phonetic_anchors": 0,
        },
        "nulls": {
            "shape_iterations_per_token_family_sample": NULL_ITERATIONS,
            "label_null_iterations_per_family": LABEL_NULL_ITERATIONS,
            "survival_rule": ">=2 samples, 100% modal Brahmi label agreement, shape null <=0.01, label null <=0.01, then still candidate-only pending manual visual descent review.",
        },
        "candidate_only_rows": accepted,
        "decision": "No Brahmi-derived phonetic anchor is accepted. Any candidate-only row is explicitly blocked from the claim ledger until source tokenization and visual descent are manually reviewed with matched negatives.",
        "outputs": {
            "inventory": "data/brahmi/source_token_descent_inventory_v2.csv",
            "segments": "data/brahmi/source_token_segments_v2.csv",
            "neighbors": "data/brahmi/source_token_brahmi_neighbors_v2.csv",
            "family_summary": "data/brahmi/source_token_family_descent_summary_v2.csv",
            "shape_null_iterations": "data/brahmi/source_token_shape_null_iterations_v2.csv",
            "label_null_iterations": "data/brahmi/source_token_label_null_iterations_v2.csv",
            "fetch_log": "data/brahmi/source_token_descent_fetch_log_v2.csv",
        },
    }
    (OUT / "source_token_brahmi_descent_v2_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
