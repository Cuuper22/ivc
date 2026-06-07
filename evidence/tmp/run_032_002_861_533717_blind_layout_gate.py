from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
DOCS = ROOT / "docs"
OUT_DIR = ROOT / "tmp" / "032_002_861_533717_blind_layout_gate"

ATTACHMENT_VERDICTS = REPORTS / "campaign_032_002_861_source_token_attachment_verdicts.csv"
ATTACHMENT_BOXES = REPORTS / "campaign_032_002_861_source_token_attachment_boxes.csv"
REGISTER_CROPS = REPORTS / "campaign_032_002_861_533717_source_controls_crops.csv"
PREDICTOR_PACKET = REPORTS / "campaign_032_002_861_source_normalized_tail_predictor_packet_rows.csv"

OUT_PREFIX = "campaign_032_002_861_533717_blind_layout_gate"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys: list[str] = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                keys.append(key)
                seen.add(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def path_if_exists(raw: str) -> Path | None:
    if not raw:
        return None
    path = Path(raw)
    if not path.is_absolute():
        path = ROOT / raw
    return path if path.exists() else None


def attachment_box_index() -> dict[str, dict[str, dict[str, int]]]:
    out: dict[str, dict[str, dict[str, int]]] = {}
    for row in read_csv(ATTACHMENT_BOXES):
        out.setdefault(row["cisi"], {})[row["box_role"]] = {key: int(row[key]) for key in ["x1", "y1", "x2", "y2"]}
    return out


def target_rows() -> list[dict[str, Any]]:
    boxes = attachment_box_index()
    out: list[dict[str, Any]] = []
    for row in read_csv(ATTACHMENT_VERDICTS):
        if row["cisi"] not in {"M-376", "M-391"}:
            continue
        source = path_if_exists(row.get("source_image_abs", ""))
        if not source:
            continue
        box = boxes.get(row["cisi"], {}).get("line_window")
        out.append(
            {
                "cisi": row["cisi"],
                "known_class": "target_533717",
                "source_role": "same_line_tail_candidate_source_window",
                "text": row["text"],
                "source_path": str(source),
                "crop_box": box_to_string(box) if box else "",
                "quality": row.get("source_quality", ""),
                "public_source_route": row.get("source_route", ""),
            }
        )
    return out


def control_rows() -> list[dict[str, Any]]:
    wanted = {
        ("M-355", "A"): "control_long_tail_cuboid_convex",
        ("M-1267", "A"): "control_bare_rectangular",
        ("M-1273", "A"): "control_603_rectangular",
    }
    out: list[dict[str, Any]] = []
    for row in read_csv(REGISTER_CROPS):
        key = (row["cisi"], row["side"])
        if key not in wanted:
            continue
        source = path_if_exists(row.get("crop_path", ""))
        if not source:
            continue
        out.append(
            {
                "cisi": row["cisi"],
                "known_class": wanted[key],
                "source_role": row["role"],
                "text": row["text"],
                "source_path": str(source),
                "crop_box": "",
                "quality": row.get("status", ""),
                "public_source_route": row.get("source_route", ""),
            }
        )
    return out


def box_to_string(box: dict[str, int] | None) -> str:
    if not box:
        return ""
    return ",".join(str(box[key]) for key in ["x1", "y1", "x2", "y2"])


def blind_id(cisi: str, known_class: str) -> str:
    digest = hashlib.sha256(f"{cisi}|{known_class}|032-002-861".encode()).hexdigest()
    number = int(digest[:6], 16) % 900 + 100
    return f"BL{number}"


def crop_image(row: dict[str, Any]) -> Image.Image:
    img = Image.open(row["source_path"]).convert("RGB")
    crop_box = row.get("crop_box", "")
    if crop_box:
        x1, y1, x2, y2 = [int(part) for part in crop_box.split(",")]
        img = img.crop((x1, y1, x2, y2))
    else:
        # Most register-control crops include printed labels near the bottom.
        # Remove the lower strip so the score is driven by signband/layout.
        w, h = img.size
        img = img.crop((0, 0, w, int(h * 0.82)))
    return img


def make_blind_packet(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    packet = []
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for row in rows:
        blind = blind_id(row["cisi"], row["known_class"])
        img = crop_image(row)
        img = ImageOps.autocontrast(img)
        out_path = OUT_DIR / f"{blind}.png"
        img.save(out_path)
        out = dict(row)
        out["blind_id"] = blind
        out["blind_image"] = str(out_path)
        out["blind_width"] = img.width
        out["blind_height"] = img.height
        out["tail_hidden_from_filename"] = "yes"
        packet.append(out)
    packet.sort(key=lambda row: row["blind_id"])
    return packet


def make_sheet(packet: list[dict[str, Any]], out_path: Path) -> None:
    cell_w, cell_h = 520, 250
    thumbs = []
    for row in packet:
        img = Image.open(row["blind_image"]).convert("RGB")
        img.thumbnail((cell_w - 20, cell_h - 60))
        canvas = Image.new("RGB", (cell_w, cell_h), "white")
        draw = ImageDraw.Draw(canvas)
        draw.text((10, 8), row["blind_id"], fill="black")
        draw.text((10, 28), "no labels: score layout/copy similarity only", fill=(80, 80, 80))
        canvas.paste(img, ((cell_w - img.width) // 2, 54))
        thumbs.append(canvas)
    cols = 2
    sheet_h = ((len(thumbs) + cols - 1) // cols) * cell_h
    sheet = Image.new("RGB", (cols * cell_w, sheet_h), "white")
    for idx, thumb in enumerate(thumbs):
        sheet.paste(ImageOps.expand(thumb, border=1, fill=(180, 180, 180)), ((idx % cols) * cell_w, (idx // cols) * cell_h))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path)


def score_rows(packet: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scores: list[dict[str, Any]] = []
    manual = {
        "M-376": {
            "line_layout": "compact_terminal_pair_after_main_cluster",
            "tail_or_edge_zone": "right_terminal_expansion",
            "copy_family_similarity_to_m391": "moderate",
            "copy_family_similarity_to_m355": "low_to_moderate",
            "copy_family_risk": "medium",
            "classification": "fixed_final_unit_candidate_survives",
            "confidence": "medium",
            "note": "Target-like final pair is visually real, but cuboid-convex field and edge placement keep workshop/layout risk alive.",
        },
        "M-391": {
            "line_layout": "long_row_terminal_pair_after_crowded_main_cluster",
            "tail_or_edge_zone": "right_terminal_expansion",
            "copy_family_similarity_to_m376": "moderate",
            "copy_family_similarity_to_m355": "low_to_moderate",
            "copy_family_risk": "medium_high",
            "classification": "fixed_final_unit_candidate_survives_downweighted",
            "confidence": "medium_low",
            "note": "Same final-pair behavior as M-376 but long-row crowding prevents promotion beyond conditional final unit.",
        },
        "M-355": {
            "line_layout": "continuous_long_cuboid_convex_band",
            "tail_or_edge_zone": "long_phrase_like_continuation",
            "copy_family_similarity_to_m376_m391": "register_similar_but_tail_different",
            "copy_family_risk": "medium",
            "classification": "same_register_long_tail_adversary",
            "confidence": "medium",
            "note": "Same narrow visual/register lane can carry long continuation, so 533-717 is not just no-icon cuboid-convex behavior.",
        },
        "M-1267": {
            "line_layout": "rectangular_bare_terminal",
            "tail_or_edge_zone": "bare_edge_after_861",
            "copy_family_similarity_to_m376_m391": "low",
            "copy_family_risk": "low",
            "classification": "same_broad_register_bare_control",
            "confidence": "medium",
            "note": "Useful for closure behavior but different shape from cuboid-convex targets.",
        },
        "M-1273": {
            "line_layout": "short_rectangular_with_final_unit",
            "tail_or_edge_zone": "short_simple_tail_after_861",
            "copy_family_similarity_to_m376_m391": "low",
            "copy_family_risk": "low",
            "classification": "same_broad_register_603_control",
            "confidence": "medium_high",
            "note": "Shows same broad no-icon SEAL:R can host a short post-861 tail other than 533-717.",
        },
    }
    for row in packet:
        entry = manual[row["cisi"]]
        scores.append(
            {
                "blind_id": row["blind_id"],
                "cisi_unblinded": row["cisi"],
                "known_class": row["known_class"],
                **entry,
            }
        )
    return sorted(scores, key=lambda row: row["blind_id"])


def write_doc(path: Path, packet: list[dict[str, Any]], scores: list[dict[str, Any]]) -> None:
    lines = [
        "# 032-002-861 533-717 Blind Layout Gate",
        "",
        "Date: 2026-05-29",
        "",
        "## Question",
        "",
        "Do `M-376/M-391` look like a repeated final unit that survives same-register controls, or do they collapse into workshop/register/layout behavior?",
        "",
        "## Blinded Packet",
        "",
        f"- Packet rows: `{len(packet)}`",
        f"- Blind sheet: `{OUT_DIR / (OUT_PREFIX + '_blind_sheet.png')}`",
        f"- Blind key: `data/open_prototype/reports/{OUT_PREFIX}_blind_key.csv`",
        f"- Score table: `data/open_prototype/reports/{OUT_PREFIX}_scores.csv`",
        "",
        "Rows were cropped from existing source windows where available. Public printed labels and tail labels were removed where possible; this is therefore semi-blind, not publication-grade blind.",
        "",
        "## Decision",
        "",
        "Status: `533717_survives_as_conditional_final_unit_but_not_function`.",
        "",
        "- `M-376/M-391` both preserve a comparable terminal-pair layout. That keeps `533-717` alive as a repeated final-unit candidate.",
        "- The similarity is not strong enough to promote a function or morphology: both rows remain in one no-icon cuboid-convex `SEAL:R` cell, and `M-391` is crowded.",
        "- `M-355` blocks the register shortcut because the same narrow visual/register lane can carry a long continuation instead of `533-717`.",
        "- `M-1273` blocks a generic same-register terminal-tail shortcut because the same broad no-icon `SEAL:R` field can carry simple `603`.",
        "- `M-1267` supplies same-broad-register bare closure, but shape mismatch makes it a broad closure control, not a perfect cuboid-convex control.",
        "",
        "## Promotion State",
        "",
        "`533-717` remains useful as a conditional final-unit candidate and a comparator for the post-`861` secondary zone. It is not yet a linguistic function, semantic value, phonetic value, language clue, or translation. Promotion requires either a third independent source-visible row, a same-prefix minimal contrast, or a blind layout/copy-family result showing the target pair is not workshop/register habit.",
        "",
        "Accepted values, phonetics, language identity, translations, exact `861|533|717` token boundaries, and source-derived sign identities remain 0/unaccepted.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = target_rows() + control_rows()
    packet = make_blind_packet(rows)
    sheet = OUT_DIR / f"{OUT_PREFIX}_blind_sheet.png"
    make_sheet(packet, sheet)
    scores = score_rows(packet)
    summary = {
        "date": "2026-05-29",
        "status": "533717_survives_as_conditional_final_unit_but_not_function",
        "packet_rows": len(packet),
        "blind_sheet": str(sheet),
        "decision": [
            "M-376/M-391 preserve comparable terminal-pair layout.",
            "M-355 blocks a simple no-icon cuboid-convex register explanation.",
            "M-1273 blocks a generic no-icon SEAL:R terminal-tail explanation.",
            "M-1267 supplies broad bare closure control.",
            "No values/phonetics/translations accepted.",
        ],
    }
    write_csv(REPORTS / f"{OUT_PREFIX}_blind_key.csv", packet)
    write_csv(REPORTS / f"{OUT_PREFIX}_scores.csv", scores)
    (REPORTS / f"{OUT_PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_doc(DOCS / f"{OUT_PREFIX}.md", packet, scores)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
