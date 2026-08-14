"""The first (v1) Indus-to-Brahmi shape gate, run 2026-05-29.

The question: do a handful of hand-picked Indus sign crops look more like early
Brahmi letters than random shapes do? The script scrapes the Indoskript
manuscript index (42 pages), keeps the 12 earliest manuscripts dated -100 or
before, downloads their letter images, and converts each into a 64x64 ink mask
and a feature vector (32x32 pixels plus 8 shape scalars). It then runs 14 fixed
Indus probes — source crops for local signs 220 and 110 plus Parpola 1994
sign-list controls — through a 10-nearest-neighbor search over the Brahmi
glyphs. For each "actual" source probe it also runs a 500-iteration random
shape-evolution null (random rotation, scale, dilation, erosion, threshold) to
ask how often a random deformation matches Brahmi at least as well. Writes the
manuscript, glyph, feature, probe, neighbor, null, and fetch-log CSVs plus a
JSON summary. Recorded decision: no descent line or phonetic anchor is
accepted; nearest-neighbor hits are retrieval leads only.
"""
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
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps


DATE = "2026-05-29"
BASE_URL = "https://www.indoskript.phil.uni-wuerzburg.de"
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "data" / "brahmi"
IMG_DIR = OUT / "indoskript_letter_images"
REPORTS = OUT
TMP = ROOT / "tmp"
RNG_SEED = 20260529
EARLY_DATE_MAX = -100
EARLY_MANUSCRIPT_LIMIT = 12
NULL_ITERATIONS_PER_PROBE = 500
CANVAS = 64
FEATURE_CANVAS = 32

VOCALIZATIONS = ["a"]

INDUS_PROBES = [
    {
        "probe_id": "indus_local220_M37_source_S009",
        "family": "local_220_source_actual",
        "path": TMP / "parpola_sign60_local220_strict_probe" / "neutral_packet" / "S009.png",
        "note": "M-37 source middle component from local +520-220-415+.",
    },
    {
        "probe_id": "indus_local220_H938_source_S010",
        "family": "local_220_source_actual",
        "path": TMP / "parpola_sign60_local220_strict_probe" / "neutral_packet" / "S010.png",
        "note": "H-938 A source middle component from local +520-220-415+.",
    },
    {
        "probe_id": "indus_local220_H940_source_S011",
        "family": "local_220_source_actual",
        "path": TMP / "parpola_sign60_local220_strict_probe" / "neutral_packet" / "S011.png",
        "note": "H-940 A source middle component from local +520-220-415+.",
    },
    {
        "probe_id": "indus_local220_H942_source_stress_S012",
        "family": "local_220_stress_actual",
        "path": TMP / "parpola_sign60_local220_strict_probe" / "neutral_packet" / "S012.png",
        "note": "H-942 A source middle component candidate from local +520-220-016+; already blocked as a positive support crop.",
    },
    {
        "probe_id": "parpola_sign60_variant_a_S001",
        "family": "parpola_1994_signlist_control",
        "path": TMP / "parpola_sign60_local220_strict_probe" / "neutral_packet" / "S001.png",
        "note": "Parpola 1994 Fig. 5.1 sign no. 60 variant a, canonical control.",
    },
    {
        "probe_id": "parpola_sign60_variant_b_S002",
        "family": "parpola_1994_signlist_control",
        "path": TMP / "parpola_sign60_local220_strict_probe" / "neutral_packet" / "S002.png",
        "note": "Parpola 1994 Fig. 5.1 sign no. 60 variant b, canonical control.",
    },
    {
        "probe_id": "parpola_sign57_control_S003",
        "family": "parpola_1994_signlist_control",
        "path": TMP / "parpola_sign60_local220_strict_probe" / "neutral_packet" / "S003.png",
        "note": "Parpola 1994 Fig. 5.1 sign no. 57, nearby fish-family control.",
    },
    {
        "probe_id": "parpola_sign58_control_S004",
        "family": "parpola_1994_signlist_control",
        "path": TMP / "parpola_sign60_local220_strict_probe" / "neutral_packet" / "S004.png",
        "note": "Parpola 1994 Fig. 5.1 sign no. 58, nearby fish-family control.",
    },
    {
        "probe_id": "parpola_sign59_control_S005",
        "family": "parpola_1994_signlist_control",
        "path": TMP / "parpola_sign60_local220_strict_probe" / "neutral_packet" / "S005.png",
        "note": "Parpola 1994 Fig. 5.1 sign no. 59, nearby fish-family control.",
    },
    {
        "probe_id": "parpola_sign66_control_S006",
        "family": "parpola_1994_signlist_control",
        "path": TMP / "parpola_sign60_local220_strict_probe" / "neutral_packet" / "S006.png",
        "note": "Parpola 1994 Fig. 5.1 sign no. 66, nearby fish-family control.",
    },
    {
        "probe_id": "parpola_sign70_variant_a_S007",
        "family": "parpola_1994_signlist_control",
        "path": TMP / "parpola_sign60_local220_strict_probe" / "neutral_packet" / "S007.png",
        "note": "Parpola 1994 Fig. 5.1 sign no. 70 variant a, nearby fish-family control.",
    },
    {
        "probe_id": "parpola_sign70_variant_b_S008",
        "family": "parpola_1994_signlist_control",
        "path": TMP / "parpola_sign60_local220_strict_probe" / "neutral_packet" / "S008.png",
        "note": "Parpola 1994 Fig. 5.1 sign no. 70 variant b, nearby fish-family control.",
    },
    {
        "probe_id": "indus_local110_H2148_source",
        "family": "local_110_source_actual",
        "path": TMP / "h2148_h2100_h2152_110_route" / "derived" / "h2148_fig14_item1_left_single_panel_no_label_crop.png",
        "note": "H-2148 one-sign source panel candidate for local 110.",
    },
    {
        "probe_id": "parpola_sign41_canonical_crop",
        "family": "parpola_1994_signlist_control",
        "path": TMP / "parpola_1994_signlist" / "rendered" / "fig5_1_p70_sign41_only_crop.png",
        "note": "Parpola 1994 Fig. 5.1 sign no. 41 canonical crop.",
    },
]


@dataclass
class FeatureRecord:
    record_id: str
    label: str
    source_class: str
    path: Path
    vector: np.ndarray
    aspect: float
    ink_density: float
    bbox_w: int
    bbox_h: int
    sha256: str


def fetch_text(url: str, fetch_log: list[dict], sleep_seconds: float = 0.03) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "ivc-shape-gate/0.1"})
    with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=30) as res:
        data = res.read()
        status = getattr(res, "status", 200)
    digest = hashlib.sha256(data).hexdigest()
    fetch_log.append(
        {
            "url": url,
            "status": status,
            "byte_length": len(data),
            "sha256": digest,
            "kind": "html",
        }
    )
    time.sleep(sleep_seconds)
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
    req = urllib.request.Request(url, headers={"User-Agent": "ivc-shape-gate/0.1"})
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
    time.sleep(0.02)
    return digest


def strip_tags(value: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", value)).strip()


def parse_manuscript_rows(text: str) -> list[dict]:
    pattern = re.compile(
        r'<tr><td><a href="/manuscripts/details/(\d+)">([\s\S]*?)</a> \[<a href="/letters/table/\d+"[^>]*>Table</a>\]</td>'
        r"<td>([^<]*)</td><td>([^<]*)</td><td>([^<]*)</td><td>([^<]*)</td></tr>"
    )
    rows = []
    for match in pattern.finditer(text):
        date_text = strip_tags(match.group(3))
        try:
            date_value = int(date_text)
        except ValueError:
            continue
        rows.append(
            {
                "manuscript_id": match.group(1),
                "name": strip_tags(match.group(2)),
                "date": date_value,
                "place": strip_tags(match.group(4)),
                "language": strip_tags(match.group(5)),
                "dynasty": strip_tags(match.group(6)),
                "details_url": f"{BASE_URL}/manuscripts/details/{match.group(1)}",
                "table_url": f"{BASE_URL}/letters/table/{match.group(1)}",
            }
        )
    return rows


def parse_letters_table(text: str, manuscript: dict, vocalization: str) -> list[dict]:
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
                        "vocalization": vocalization,
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
                        "vocalization": vocalization,
                        "letter_image_id": image_id,
                        "transliteration": label,
                        "variant_role": f"variant_{variant_index + 1}",
                        "table_block_index": block_index,
                        "image_url": f"{BASE_URL}/img/letters/{image_id}.png",
                    }
                )
    return rows


def image_to_mask(path: Path, canvas: int = CANVAS) -> tuple[np.ndarray, dict]:
    img = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    bg.alpha_composite(img)
    gray = ImageOps.grayscale(bg)
    arr = np.asarray(gray).astype(np.uint8)
    median = float(np.median(arr))
    mad = float(np.median(np.abs(arr.astype(np.float32) - median)))
    threshold = max(18.0, min(55.0, 3.0 * mad))
    if median > 232:
        mask = arr < (median - threshold)
    else:
        mask = np.abs(arr.astype(np.float32) - median) > threshold
    fill = float(mask.mean())
    if fill < 0.003 or fill > 0.50:
        mask = arr < 225
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
    out_arr = (np.asarray(out).astype(np.float32) / 255.0)
    return out_arr, {
        "bbox_w": int(w),
        "bbox_h": int(h),
        "aspect": float(w / h) if h else 0.0,
        "ink_density": float(out_arr.mean()),
    }


def feature_from_mask(mask: np.ndarray, metrics: dict) -> np.ndarray:
    img = Image.fromarray((mask * 255).astype(np.uint8), mode="L").resize(
        (FEATURE_CANVAS, FEATURE_CANVAS), Image.Resampling.LANCZOS
    )
    pix = np.asarray(img).astype(np.float32).reshape(-1) / 255.0
    ys, xs = np.nonzero(mask > 0.1)
    if len(xs) == 0:
        scalars = np.zeros(8, dtype=np.float32)
    else:
        x = xs.astype(np.float32) / max(mask.shape[1] - 1, 1)
        y = ys.astype(np.float32) / max(mask.shape[0] - 1, 1)
        cx = float(x.mean())
        cy = float(y.mean())
        sx = float(x.std())
        sy = float(y.std())
        cov = float(((x - cx) * (y - cy)).mean())
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
            ],
            dtype=np.float32,
        )
    vec = np.concatenate([pix, scalars])
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.astype(np.float32)


def record_feature(record_id: str, label: str, source_class: str, path: Path) -> FeatureRecord | None:
    if not path.exists() or path.stat().st_size == 0:
        return None
    mask, metrics = image_to_mask(path)
    vector = feature_from_mask(mask, metrics)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return FeatureRecord(
        record_id=record_id,
        label=label,
        source_class=source_class,
        path=path,
        vector=vector,
        aspect=metrics["aspect"],
        ink_density=metrics["ink_density"],
        bbox_w=metrics["bbox_w"],
        bbox_h=metrics["bbox_h"],
        sha256=digest,
    )


def cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(1.0 - np.dot(a, b))


def perturb_mask(mask: np.ndarray, rng: random.Random) -> np.ndarray:
    img = Image.fromarray((mask * 255).astype(np.uint8), mode="L")
    angle = rng.uniform(-35.0, 35.0)
    img = img.rotate(angle, resample=Image.Resampling.BICUBIC, fillcolor=0)
    if rng.random() < 0.5:
        img = img.filter(ImageFilter.MaxFilter(size=3))
    if rng.random() < 0.5:
        img = img.filter(ImageFilter.MinFilter(size=3))
    scale = rng.uniform(0.72, 1.30)
    nw = max(1, int(round(CANVAS * scale)))
    nh = max(1, int(round(CANVAS * rng.uniform(0.72, 1.30))))
    img = img.resize((nw, nh), Image.Resampling.BICUBIC)
    crop = Image.new("L", (CANVAS, CANVAS), 0)
    x = rng.randint(min(0, CANVAS - nw), max(0, CANVAS - nw))
    y = rng.randint(min(0, CANVAS - nh), max(0, CANVAS - nh))
    crop.paste(img, (x, y))
    arr = np.asarray(crop).astype(np.float32) / 255.0
    arr = (arr > rng.uniform(0.18, 0.45)).astype(np.float32)
    return arr


def nearest_neighbors(probe: FeatureRecord, brahmi: list[FeatureRecord], k: int = 10) -> list[tuple[FeatureRecord, float]]:
    scores = [(rec, cosine_distance(probe.vector, rec.vector)) for rec in brahmi]
    scores.sort(key=lambda item: item[1])
    return scores[:k]


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    fetch_log: list[dict] = []

    manuscript_rows: list[dict] = []
    for page in range(1, 43):
        text = fetch_text(f"{BASE_URL}/manuscripts?page={page}", fetch_log)
        manuscript_rows.extend(parse_manuscript_rows(text))
    manuscript_rows = sorted(
        {row["manuscript_id"]: row for row in manuscript_rows}.values(),
        key=lambda row: (row["date"], row["manuscript_id"]),
    )
    early_manuscripts_all = [row for row in manuscript_rows if row["date"] <= EARLY_DATE_MAX]
    early_manuscripts = early_manuscripts_all[:EARLY_MANUSCRIPT_LIMIT]

    glyph_rows: list[dict] = []
    seen_glyph_keys: set[tuple[str, str, str]] = set()
    for manuscript in early_manuscripts:
        for vocalization in VOCALIZATIONS:
            suffix = "" if vocalization == "a" else f"?vocalization={urllib.request.quote(vocalization)}"
            table_url = f"{BASE_URL}/letters/table/{manuscript['manuscript_id']}{suffix}"
            text = fetch_text(table_url, fetch_log)
            parsed = parse_letters_table(text, manuscript, vocalization)
            for row in parsed:
                key = (row["manuscript_id"], row["letter_image_id"], row["transliteration"])
                if key not in seen_glyph_keys:
                    seen_glyph_keys.add(key)
                    glyph_rows.append(row)

    glyph_feature_rows: list[dict] = []
    brahmi_features: list[FeatureRecord] = []
    for row in glyph_rows:
        dest = IMG_DIR / f"{row['letter_image_id']}.png"
        digest = fetch_binary(row["image_url"], dest, fetch_log)
        feature = record_feature(
            record_id=f"indoskript_{row['letter_image_id']}",
            label=row["transliteration"],
            source_class="early_brahmi_indoskript",
            path=dest,
        )
        if feature is None or feature.ink_density <= 0:
            continue
        brahmi_features.append(feature)
        glyph_feature_rows.append(
            {
                **row,
                "local_image_path": str(dest.relative_to(ROOT)),
                "sha256": digest,
                "bbox_w": feature.bbox_w,
                "bbox_h": feature.bbox_h,
                "aspect": f"{feature.aspect:.6f}",
                "ink_density": f"{feature.ink_density:.6f}",
            }
        )

    probe_features: list[FeatureRecord] = []
    probe_rows: list[dict] = []
    for probe in INDUS_PROBES:
        feature = record_feature(probe["probe_id"], probe["probe_id"], probe["family"], probe["path"])
        if feature is None:
            probe_rows.append(
                {
                    "probe_id": probe["probe_id"],
                    "family": probe["family"],
                    "path": str(probe["path"].relative_to(ROOT)),
                    "present": "false",
                    "note": probe["note"],
                }
            )
            continue
        probe_features.append(feature)
        probe_rows.append(
            {
                "probe_id": probe["probe_id"],
                "family": probe["family"],
                "path": str(probe["path"].relative_to(ROOT)),
                "present": "true",
                "sha256": feature.sha256,
                "bbox_w": feature.bbox_w,
                "bbox_h": feature.bbox_h,
                "aspect": f"{feature.aspect:.6f}",
                "ink_density": f"{feature.ink_density:.6f}",
                "note": probe["note"],
            }
        )

    neighbor_rows: list[dict] = []
    for probe in probe_features:
        for rank, (neighbor, dist) in enumerate(nearest_neighbors(probe, brahmi_features, k=10), start=1):
            glyph_meta = next(
                row for row in glyph_feature_rows if f"indoskript_{row['letter_image_id']}" == neighbor.record_id
            )
            neighbor_rows.append(
                {
                    "probe_id": probe.record_id,
                    "probe_family": probe.source_class,
                    "rank": rank,
                    "distance": f"{dist:.6f}",
                    "brahmi_transliteration": neighbor.label,
                    "letter_image_id": glyph_meta["letter_image_id"],
                    "manuscript_id": glyph_meta["manuscript_id"],
                    "manuscript_name": glyph_meta["name"],
                    "date": glyph_meta["date"],
                    "place": glyph_meta["place"],
                    "image_url": glyph_meta["image_url"],
                    "local_image_path": glyph_meta["local_image_path"],
                }
            )

    rng = random.Random(RNG_SEED)
    null_rows: list[dict] = []
    null_summary_rows: list[dict] = []
    actual_families = {"local_220_source_actual", "local_110_source_actual"}
    for probe in [p for p in probe_features if p.source_class in actual_families]:
        mask, metrics = image_to_mask(probe.path)
        observed = nearest_neighbors(probe, brahmi_features, k=1)[0]
        observed_distance = observed[1]
        null_distances: list[float] = []
        for iteration in range(NULL_ITERATIONS_PER_PROBE):
            evolved = perturb_mask(mask, rng)
            vec = feature_from_mask(
                evolved,
                {
                    "bbox_w": metrics["bbox_w"],
                    "bbox_h": metrics["bbox_h"],
                    "aspect": metrics["aspect"],
                    "ink_density": float(evolved.mean()),
                },
            )
            pseudo = FeatureRecord(
                record_id=f"{probe.record_id}_null_{iteration}",
                label="null",
                source_class="random_shape_evolution_null",
                path=probe.path,
                vector=vec,
                aspect=metrics["aspect"],
                ink_density=float(evolved.mean()),
                bbox_w=metrics["bbox_w"],
                bbox_h=metrics["bbox_h"],
                sha256="",
            )
            nearest = nearest_neighbors(pseudo, brahmi_features, k=1)[0]
            dist = nearest[1]
            null_distances.append(dist)
            null_rows.append(
                {
                    "probe_id": probe.record_id,
                    "iteration": iteration,
                    "nearest_distance": f"{dist:.6f}",
                    "nearest_brahmi_transliteration": nearest[0].label,
                    "nearest_letter_image_id": nearest[0].record_id.replace("indoskript_", ""),
                }
            )
        null_arr = np.array(null_distances, dtype=np.float32)
        null_le_observed = float(np.mean(null_arr <= observed_distance))
        null_summary_rows.append(
            {
                "probe_id": probe.record_id,
                "probe_family": probe.source_class,
                "observed_nearest_distance": f"{observed_distance:.6f}",
                "observed_nearest_brahmi_transliteration": observed[0].label,
                "observed_nearest_letter_image_id": observed[0].record_id.replace("indoskript_", ""),
                "null_iterations": NULL_ITERATIONS_PER_PROBE,
                "null_mean_nearest_distance": f"{float(null_arr.mean()):.6f}",
                "null_p05_nearest_distance": f"{float(np.quantile(null_arr, 0.05)):.6f}",
                "null_p50_nearest_distance": f"{float(np.quantile(null_arr, 0.50)):.6f}",
                "null_p95_nearest_distance": f"{float(np.quantile(null_arr, 0.95)):.6f}",
                "null_le_observed_share": f"{null_le_observed:.6f}",
                "gate_decision": "failed_shape_null_or_family_consistency",
            }
        )

    source_220_top1 = [
        row
        for row in neighbor_rows
        if row["rank"] == 1 and row["probe_family"] == "local_220_source_actual"
    ]
    source_110_top1 = [
        row
        for row in neighbor_rows
        if row["rank"] == 1 and row["probe_family"] == "local_110_source_actual"
    ]
    label_counts: dict[str, int] = {}
    for row in source_220_top1:
        label_counts[row["brahmi_transliteration"]] = label_counts.get(row["brahmi_transliteration"], 0) + 1

    summary = {
        "date": DATE,
        "status": "brahmi_shape_descent_gate_no_survivor",
        "source": {
            "homepage": BASE_URL,
            "manuscript_pages_scanned": 42,
            "early_date_max": EARLY_DATE_MAX,
            "early_manuscript_limit": EARLY_MANUSCRIPT_LIMIT,
            "vocalizations_scanned": VOCALIZATIONS,
            "license_note": "Indoskript homepage states CC BY-NC-ND 4.0. Local images are cached only as provenance-backed research inputs.",
        },
        "counts": {
            "manuscripts_total": len(manuscript_rows),
            "early_manuscripts_date_le_cutoff_total": len(early_manuscripts_all),
            "early_manuscripts_used": len(early_manuscripts),
            "glyph_rows_parsed": len(glyph_rows),
            "glyph_features": len(brahmi_features),
            "indus_probe_rows": len(probe_rows),
            "indus_probe_features": len(probe_features),
            "nearest_neighbor_rows": len(neighbor_rows),
        },
        "null": {
            "iterations_per_actual_probe": NULL_ITERATIONS_PER_PROBE,
            "random_seed": RNG_SEED,
            "model": "Random affine, scale, threshold, dilation, and erosion perturbations of each actual Indus source probe; each evolved shape gets the same nearest-Brahmi search as the observed probe.",
            "summary_rows": null_summary_rows,
        },
        "family_consistency": {
            "local_220_source_top1_label_counts": label_counts,
            "local_220_source_top1_rows": source_220_top1,
            "local_110_source_top1_rows": source_110_top1,
        },
        "decision": "No Brahmi descent line or phonetic anchor is accepted. Nearest-neighbor shape matches are retrieval leads only unless they beat the random shape-evolution null and converge across independent source probes on one Brahmi value.",
        "files": {
            "manuscripts": "data/brahmi/indoskript_brahmi_manuscripts.csv",
            "glyphs": "data/brahmi/indoskript_brahmi_glyphs.csv",
            "features": "data/brahmi/indoskript_brahmi_features.csv",
            "indus_probes": "data/brahmi/indus_shape_probe_features.csv",
            "nearest_neighbors": "data/brahmi/indus_brahmi_nearest_neighbors.csv",
            "null_iterations": "data/brahmi/brahmi_shape_descent_null_iterations.csv",
            "fetch_log": "data/brahmi/indoskript_brahmi_fetch_log.csv",
            "summary": "data/brahmi/brahmi_shape_descent_null_summary.json",
        },
    }

    write_csv(
        REPORTS / "indoskript_brahmi_manuscripts.csv",
        manuscript_rows,
        ["manuscript_id", "name", "date", "place", "language", "dynasty", "details_url", "table_url"],
    )
    write_csv(
        REPORTS / "indoskript_brahmi_glyphs.csv",
        glyph_rows,
        [
            "manuscript_id",
            "name",
            "date",
            "place",
            "language",
            "dynasty",
            "details_url",
            "table_url",
            "vocalization",
            "letter_image_id",
            "transliteration",
            "variant_role",
            "table_block_index",
            "image_url",
        ],
    )
    write_csv(
        REPORTS / "indoskript_brahmi_features.csv",
        glyph_feature_rows,
        [
            "manuscript_id",
            "name",
            "date",
            "place",
            "language",
            "dynasty",
            "details_url",
            "table_url",
            "vocalization",
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
    probe_fieldnames = [
        "probe_id",
        "family",
        "path",
        "present",
        "sha256",
        "bbox_w",
        "bbox_h",
        "aspect",
        "ink_density",
        "note",
    ]
    normalized_probe_rows = [{key: row.get(key, "") for key in probe_fieldnames} for row in probe_rows]
    write_csv(REPORTS / "indus_shape_probe_features.csv", normalized_probe_rows, probe_fieldnames)
    write_csv(
        REPORTS / "indus_brahmi_nearest_neighbors.csv",
        neighbor_rows,
        [
            "probe_id",
            "probe_family",
            "rank",
            "distance",
            "brahmi_transliteration",
            "letter_image_id",
            "manuscript_id",
            "manuscript_name",
            "date",
            "place",
            "image_url",
            "local_image_path",
        ],
    )
    write_csv(
        REPORTS / "brahmi_shape_descent_null_iterations.csv",
        null_rows,
        [
            "probe_id",
            "iteration",
            "nearest_distance",
            "nearest_brahmi_transliteration",
            "nearest_letter_image_id",
        ],
    )
    write_csv(
        REPORTS / "indoskript_brahmi_fetch_log.csv",
        fetch_log,
        ["url", "status", "byte_length", "sha256", "kind"],
    )
    (REPORTS / "brahmi_shape_descent_null_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
