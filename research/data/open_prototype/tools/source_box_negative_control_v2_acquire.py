"""Acquires public source images for the v2 negative-control targets of the
source-box program. The five targets (M-38, M-124, M-381, H-601, H-1678)
come from a targets CSV; for each, a hand-curated route table points at
public CISI plate pages on archive.org (or, for the two Harappa rows, only
a secondary catalogue text, which is explicitly marked not source-grade).
The script downloads each plate page, scales the recorded OCR label
coordinates to the actual image size, cuts a broad context crop around the
label with the label boxed in red, and — for three hand-specified panels —
cuts a label-free panel crop plus an autocontrast 2x enhanced version.
Every artifact gets a SHA-256 hash so later steps can prove provenance.
Outputs: routes CSV, panel-crops CSV, a per-target source-status CSV that
says what each image may currently be used for (always with accepted-claims
increment 0), two contact sheets, and a JSON summary.
"""
import csv
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageDraw, ImageOps


ROOT = Path.cwd()
OUT = ROOT / "tmp" / "source_box_negative_control_v2"
PAGES = OUT / "pages"
CROPS = OUT / "crops"
PANEL_CROPS = OUT / "panel_crops"
REPORTS = ROOT / "data" / "open_prototype" / "reports"
TARGETS_CSV = REPORTS / "source_box_negative_control_v2_targets.csv"
OUT_CSV = REPORTS / "source_box_negative_control_v2_public_routes.csv"
OUT_PANEL_CSV = REPORTS / "source_box_negative_control_v2_panel_crops.csv"
OUT_STATUS_CSV = REPORTS / "source_box_negative_control_v2_source_status.csv"
OUT_JSON = REPORTS / "source_box_negative_control_v2_public_routes_summary.json"
CONTACT_SHEET = OUT / "source_box_negative_control_v2_contact_sheet.jpg"
PANEL_CONTACT_SHEET = OUT / "source_box_negative_control_v2_panel_contact_sheet.jpg"

RUN_DATE = "2026-05-29"
IA_BASE = (
    "https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/"
    "Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India/page/"
)

XML_WIDTH = 2488
XML_HEIGHT = 3476

PUBLIC_ROUTES = {
    "M-38": [
        {
            "route_id": "cisi_india_n55_plate",
            "route_kind": "public_cisi_plate_page",
            "page_index": 55,
            "page_file": "India_0055.djvu",
            "source_url": f"{IA_BASE}n55_w2000.jpg",
            "ocr_label_coords": [444, 1048, 528, 1079],
            "ocr_context": "MOHENJO-DARO 38-40 SEALS unicorn III M-38 A",
            "source_grade_status": "source_page_crop_needs_human_boxing",
        },
        {
            "route_id": "cisi_india_n405_data_register",
            "route_kind": "public_cisi_data_register",
            "page_index": 405,
            "page_file": "India_0405.djvu",
            "source_url": f"{IA_BASE}n405_w2000.jpg",
            "ocr_label_coords": [157, 2680, 209, 2700],
            "ocr_context": "data/register line containing M-38 1103 A 336",
            "source_grade_status": "data_register_not_source_panel",
        },
    ],
    "M-124": [
        {
            "route_id": "cisi_india_n139_plate",
            "route_kind": "public_cisi_plate_page",
            "page_index": 139,
            "page_file": "India_0139.djvu",
            "source_url": f"{IA_BASE}n139_w2000.jpg",
            "ocr_label_coords": [374, 1781, 477, 1809],
            "ocr_context": "MOHENJO-DARO 423-425 SEAL IMPRESSIONS on pots, on tags; OCR labels M-124 A",
            "source_grade_status": "source_page_crop_needs_human_boxing",
        },
        {
            "route_id": "cisi_india_n402_data_register",
            "route_kind": "public_cisi_data_register",
            "page_index": 402,
            "page_file": "India_0402.djvu",
            "source_url": f"{IA_BASE}n402_w2000.jpg",
            "ocr_label_coords": [135, 991, 206, 1014],
            "ocr_context": "data/register line containing M-124 1120",
            "source_grade_status": "data_register_not_source_panel",
        },
    ],
    "M-381": [
        {
            "route_id": "cisi_india_n129_plate",
            "route_kind": "public_cisi_plate_page",
            "page_index": 129,
            "page_file": "India_0129.djvu",
            "source_url": f"{IA_BASE}n129_w2000.jpg",
            "ocr_label_coords": [1832, 3217, 1929, 3248],
            "ocr_context": "MOHENJO-DARO 376-381 SEALS S3 no iconography III; OCR labels M-381 a",
            "source_grade_status": "source_page_crop_needs_human_boxing",
        },
    ],
    "H-601": [
        {
            "route_id": "bhaskar_s1_catalogue_text",
            "route_kind": "secondary_catalogue_text_only",
            "page_index": "",
            "page_file": "tmp/m1206_bhaskar/S1-IndusZoomorphicIconCatalogue.txt",
            "source_url": "local:tmp/m1206_bhaskar/S1-IndusZoomorphicIconCatalogue.txt",
            "ocr_label_coords": [],
            "ocr_context": "Bhaskar S1 catalogue line marks H-601 as F2 / Unicorn",
            "source_grade_status": "secondary_catalogue_only_not_source_grade",
        },
    ],
    "H-1678": [
        {
            "route_id": "bhaskar_s1_catalogue_text",
            "route_kind": "secondary_catalogue_text_only",
            "page_index": "",
            "page_file": "tmp/m1206_bhaskar/S1-IndusZoomorphicIconCatalogue.txt",
            "source_url": "local:tmp/m1206_bhaskar/S1-IndusZoomorphicIconCatalogue.txt",
            "ocr_label_coords": [],
            "ocr_context": "Bhaskar S1 catalogue line marks H-1678 as F2 / Unicorn",
            "source_grade_status": "secondary_catalogue_only_not_source_grade",
        },
    ],
}

PANEL_CROP_SPECS = [
    {
        "cisi": "M-381",
        "route_id": "cisi_india_n129_plate",
        "context_crop": "tmp/source_box_negative_control_v2/crops/M-381_cisi_india_n129_plate_context_crop.jpg",
        "crop_box": [45, 245, 880, 640],
        "human_visual_assessment": "full signband visible; strongest source-route candidate",
        "packet_readiness": "ready_for_token_box_adjudication",
    },
    {
        "cisi": "M-124",
        "route_id": "cisi_india_n139_plate",
        "context_crop": "tmp/source_box_negative_control_v2/crops/M-124_cisi_india_n139_plate_context_crop.jpg",
        "crop_box": [285, 205, 690, 455],
        "human_visual_assessment": "pot/tag impression visible but tiny and low-contrast",
        "packet_readiness": "needs_better_image_or_manual_boxing",
    },
    {
        "cisi": "M-38",
        "route_id": "cisi_india_n55_plate",
        "context_crop": "tmp/source_box_negative_control_v2/crops/M-38_cisi_india_n55_plate_context_crop.jpg",
        "crop_box": [65, 20, 865, 585],
        "human_visual_assessment": "source panel visible but signband is not readable enough in public crop",
        "packet_readiness": "not_ready_for_blind_packet",
    },
]

PANEL_FIELDS = [
    "date",
    "cisi",
    "route_id",
    "context_crop",
    "panel_crop",
    "enhanced_panel_crop",
    "manual_crop_box_in_context",
    "sha256_panel",
    "sha256_enhanced",
    "human_visual_assessment",
    "packet_readiness",
]

STATUS_FIELDS = [
    "date",
    "priority",
    "cisi",
    "lipi_id",
    "target_text",
    "control_class",
    "best_route_id",
    "best_route_kind",
    "best_source_url",
    "best_local_artifact",
    "best_artifact_sha256",
    "source_status_rank",
    "panel_readiness",
    "current_admissible_use",
    "blocker",
    "next_action",
    "accepted_claims_increment",
]

FIELDS = [
    "date",
    "priority",
    "cisi",
    "lipi_id",
    "target_text",
    "control_class",
    "availability_tier_before",
    "route_id",
    "route_kind",
    "route_status",
    "source_grade_status",
    "source_url",
    "page_index",
    "page_file",
    "ocr_label_coords",
    "ocr_context",
    "local_page_path",
    "local_crop_path",
    "source_image_sha256",
    "crop_sha256",
    "image_width",
    "image_height",
    "crop_box_image_coords",
    "notes",
]


def ensure_dirs():
    PAGES.mkdir(parents=True, exist_ok=True)
    CROPS.mkdir(parents=True, exist_ok=True)
    PANEL_CROPS.mkdir(parents=True, exist_ok=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download(url: str, path: Path):
    if path.exists() and path.stat().st_size:
        return
    request = Request(url, headers={"User-Agent": "codex-ivc-source-box-v2/2026-05-29"})
    with urlopen(request, timeout=60) as response:
        data = response.read()
    path.write_bytes(data)


def scaled_label_box(coords, width, height):
    x1, y1, x2, y2 = coords
    sx = width / XML_WIDTH
    sy = height / XML_HEIGHT
    return [
        int(round(x1 * sx)),
        int(round(y1 * sy)),
        int(round(x2 * sx)),
        int(round(y2 * sy)),
    ]


def crop_box_from_label(label_box, width, height):
    x1, y1, x2, y2 = label_box
    # The seal photo usually sits above or beside its OCR label, so we grow
    # the box generously in those directions. This is a broad context crop
    # only; drawing token boxes is a later human adjudication step.
    left = max(0, x1 - 380)
    upper = max(0, y1 - 620)
    right = min(width, x2 + 440)
    lower = min(height, y2 + 180)
    return [left, upper, right, lower]


def load_targets():
    with TARGETS_CSV.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows):
    with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def make_contact_sheet(rows):
    crop_paths = [ROOT / row["local_crop_path"] for row in rows if row["local_crop_path"]]
    if not crop_paths:
        return
    thumbs = []
    for path in crop_paths:
        image = Image.open(path).convert("RGB")
        image.thumbnail((520, 420))
        canvas = Image.new("RGB", (560, 480), "white")
        canvas.paste(image, ((560 - image.width) // 2, 20))
        label = path.stem
        draw = ImageDraw.Draw(canvas)
        draw.text((20, 440), label[:80], fill=(0, 0, 0))
        thumbs.append(canvas)
    cols = 2
    rows_count = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 560, rows_count * 480), "white")
    for i, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((i % cols) * 560, (i // cols) * 480))
    sheet.save(CONTACT_SHEET, quality=92)


def make_panel_crops():
    rows = []
    for spec in PANEL_CROP_SPECS:
        source = ROOT / spec["context_crop"]
        image = Image.open(source).convert("RGB")
        panel = image.crop(spec["crop_box"])
        panel_path = PANEL_CROPS / f"{spec['cisi']}_{spec['route_id']}_label_free_panel.jpg"
        panel.save(panel_path, quality=94)
        enhanced = ImageOps.autocontrast(panel.convert("L")).resize((panel.width * 2, panel.height * 2))
        enhanced_path = PANEL_CROPS / f"{spec['cisi']}_{spec['route_id']}_label_free_panel_enhanced_x2.jpg"
        enhanced.save(enhanced_path, quality=94)
        rows.append(
            {
                "date": RUN_DATE,
                "cisi": spec["cisi"],
                "route_id": spec["route_id"],
                "context_crop": spec["context_crop"],
                "panel_crop": str(panel_path.relative_to(ROOT)).replace("\\", "/"),
                "enhanced_panel_crop": str(enhanced_path.relative_to(ROOT)).replace("\\", "/"),
                "manual_crop_box_in_context": "|".join(str(x) for x in spec["crop_box"]),
                "sha256_panel": sha256_file(panel_path),
                "sha256_enhanced": sha256_file(enhanced_path),
                "human_visual_assessment": spec["human_visual_assessment"],
                "packet_readiness": spec["packet_readiness"],
            }
        )

    with OUT_PANEL_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=PANEL_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    thumbs = []
    for row in rows:
        image = Image.open(ROOT / row["enhanced_panel_crop"]).convert("RGB")
        image.thumbnail((620, 420))
        canvas = Image.new("RGB", (660, 500), "white")
        canvas.paste(image, ((660 - image.width) // 2, 20))
        draw = ImageDraw.Draw(canvas)
        label = f"{row['cisi']} {row['human_visual_assessment']}"
        draw.text((20, 450), label[:92], fill=(0, 0, 0))
        thumbs.append(canvas)
    sheet = Image.new("RGB", (660, 500 * len(thumbs)), "white")
    for i, thumb in enumerate(thumbs):
        sheet.paste(thumb, (0, i * 500))
    sheet.save(PANEL_CONTACT_SHEET, quality=92)
    return rows


def write_source_status(targets, route_rows, panel_rows):
    route_by_cisi = {}
    for row in route_rows:
        current = route_by_cisi.get(row["cisi"])
        is_plate = row["route_kind"] == "public_cisi_plate_page"
        current_is_plate = current and current["route_kind"] == "public_cisi_plate_page"
        if current is None or (is_plate and not current_is_plate):
            route_by_cisi[row["cisi"]] = row

    panel_by_cisi = {row["cisi"]: row for row in panel_rows}
    status_rows = []
    for cisi in sorted(targets, key=lambda key: int(targets[key]["priority"])):
        target = targets[cisi]
        route = route_by_cisi.get(cisi, {})
        panel = panel_by_cisi.get(cisi, {})
        readiness = panel.get("packet_readiness", "")

        if readiness == "ready_for_token_box_adjudication":
            source_status_rank = "source_visible_ready_for_token_box_adjudication"
            current_use = "adjudication_queue_only"
            blocker = "needs token boxes around 220,032,798,002 and side/direction note before blind packet use"
            next_action = "produce token-box adjudication manifest from the enhanced panel crop"
            artifact = panel.get("enhanced_panel_crop", "")
            artifact_sha = panel.get("sha256_enhanced", "")
        elif readiness:
            source_status_rank = "public_route_visible_but_not_packet_ready"
            current_use = "source_route_inventory_only"
            blocker = panel.get("human_visual_assessment", "")
            next_action = "find a sharper source image or manually recrop from a higher-resolution plate before token boxing"
            artifact = panel.get("enhanced_panel_crop", "")
            artifact_sha = panel.get("sha256_enhanced", "")
        else:
            source_status_rank = route.get("source_grade_status", "no_route_found")
            current_use = "not_admissible"
            blocker = "no source-grade source panel in this pass"
            next_action = "locate a raw source panel or accession/plate image; secondary catalogue text is not enough"
            artifact = route.get("local_crop_path", "")
            artifact_sha = route.get("crop_sha256", "")

        status_rows.append(
            {
                "date": RUN_DATE,
                "priority": target["priority"],
                "cisi": cisi,
                "lipi_id": target["lipi_id"],
                "target_text": target["text"],
                "control_class": target["control_class"],
                "best_route_id": route.get("route_id", ""),
                "best_route_kind": route.get("route_kind", ""),
                "best_source_url": route.get("source_url", ""),
                "best_local_artifact": artifact,
                "best_artifact_sha256": artifact_sha,
                "source_status_rank": source_status_rank,
                "panel_readiness": readiness,
                "current_admissible_use": current_use,
                "blocker": blocker,
                "next_action": next_action,
                "accepted_claims_increment": 0,
            }
        )

    with OUT_STATUS_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=STATUS_FIELDS)
        writer.writeheader()
        writer.writerows(status_rows)
    return status_rows


def main():
    ensure_dirs()
    targets = {row["cisi"]: row for row in load_targets()}
    out_rows = []
    for cisi, routes in PUBLIC_ROUTES.items():
        target = targets[cisi]
        for route in routes:
            local_page = ""
            local_crop = ""
            image_sha = ""
            crop_sha = ""
            image_width = ""
            image_height = ""
            crop_box = ""
            route_status = "route_recorded"

            if route["route_kind"].startswith("public_cisi"):
                page_path = PAGES / f"{cisi}_{route['route_id']}.jpg"
                download(route["source_url"], page_path)
                image_sha = sha256_file(page_path)
                image = Image.open(page_path).convert("RGB")
                image_width, image_height = image.size
                label_box = scaled_label_box(route["ocr_label_coords"], image_width, image_height)
                crop_box = crop_box_from_label(label_box, image_width, image_height)
                crop = image.crop(crop_box)
                crop_draw = ImageDraw.Draw(crop)
                crop_draw.rectangle(
                    [
                        label_box[0] - crop_box[0],
                        label_box[1] - crop_box[1],
                        label_box[2] - crop_box[0],
                        label_box[3] - crop_box[1],
                    ],
                    outline=(255, 0, 0),
                    width=3,
                )
                crop_path = CROPS / f"{cisi}_{route['route_id']}_context_crop.jpg"
                crop.save(crop_path, quality=92)
                crop_sha = sha256_file(crop_path)
                local_page = str(page_path.relative_to(ROOT)).replace("\\", "/")
                local_crop = str(crop_path.relative_to(ROOT)).replace("\\", "/")
                route_status = "downloaded_and_cropped"

            out_rows.append(
                {
                    "date": RUN_DATE,
                    "priority": target["priority"],
                    "cisi": cisi,
                    "lipi_id": target["lipi_id"],
                    "target_text": target["text"],
                    "control_class": target["control_class"],
                    "availability_tier_before": target["availability_tier"],
                    "route_id": route["route_id"],
                    "route_kind": route["route_kind"],
                    "route_status": route_status,
                    "source_grade_status": route["source_grade_status"],
                    "source_url": route["source_url"],
                    "page_index": route["page_index"],
                    "page_file": route["page_file"],
                    "ocr_label_coords": "|".join(str(x) for x in route["ocr_label_coords"]),
                    "ocr_context": route["ocr_context"],
                    "local_page_path": local_page,
                    "local_crop_path": local_crop,
                    "source_image_sha256": image_sha,
                    "crop_sha256": crop_sha,
                    "image_width": image_width,
                    "image_height": image_height,
                    "crop_box_image_coords": "|".join(str(x) for x in crop_box) if crop_box else "",
                    "notes": "Broad source-context crop around OCR label; not token-boxed evidence.",
                }
            )

    write_csv(out_rows)
    make_contact_sheet(out_rows)
    panel_rows = make_panel_crops()
    status_rows = write_source_status(targets, out_rows, panel_rows)

    summary = {
        "date": RUN_DATE,
        "status": "source_box_negative_control_v2_public_route_acquisition",
        "counts": {
            "target_rows": len(targets),
            "route_rows": len(out_rows),
            "public_cisi_pages_downloaded": sum(1 for r in out_rows if r["route_status"] == "downloaded_and_cropped"),
            "source_page_crops_needing_human_boxing": sum(
                1 for r in out_rows if r["source_grade_status"] == "source_page_crop_needs_human_boxing"
            ),
            "secondary_catalogue_only_rows": sum(
                1 for r in out_rows if r["source_grade_status"] == "secondary_catalogue_only_not_source_grade"
            ),
            "data_register_rows": sum(
                1 for r in out_rows if r["source_grade_status"] == "data_register_not_source_panel"
            ),
            "panel_crop_rows": len(panel_rows),
            "panel_crops_ready_for_token_box_adjudication": sum(
                1 for r in panel_rows if r["packet_readiness"] == "ready_for_token_box_adjudication"
            ),
            "source_status_rows": len(status_rows),
            "accepted_crosswalk_edges": 0,
            "accepted_sign_meanings": 0,
        },
        "files": {
            "routes": str(OUT_CSV.relative_to(ROOT)).replace("\\", "/"),
            "panel_crops": str(OUT_PANEL_CSV.relative_to(ROOT)).replace("\\", "/"),
            "source_status": str(OUT_STATUS_CSV.relative_to(ROOT)).replace("\\", "/"),
            "contact_sheet": str(CONTACT_SHEET.relative_to(ROOT)).replace("\\", "/"),
            "panel_contact_sheet": str(PANEL_CONTACT_SHEET.relative_to(ROOT)).replace("\\", "/"),
            "page_dir": str(PAGES.relative_to(ROOT)).replace("\\", "/"),
            "crop_dir": str(CROPS.relative_to(ROOT)).replace("\\", "/"),
            "panel_crop_dir": str(PANEL_CROPS.relative_to(ROOT)).replace("\\", "/"),
        },
        "caveats": [
            "Downloaded crops are broad source-context crops around OCR labels, not token boxes.",
            "H-601 and H-1678 remain secondary-catalogue-only in this pass.",
            "M-38, M-124, and M-381 have public CISI routes, but still need human/token-box adjudication before entering a blind packet.",
        ],
    }
    OUT_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
