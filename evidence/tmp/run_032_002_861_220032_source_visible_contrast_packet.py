from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
DOCS = ROOT / "docs"
TMP_OUT = ROOT / "tmp" / "032_002_861_220032_source_visible_contrast_packet"

INPUT_ROWS = REPORTS / "campaign_032_002_861_source_normalized_tail_predictor_all_rows.csv"
OUT_PREFIX = "campaign_032_002_861_220032_source_visible_contrast_packet"
SOURCE_PENDING = {"", "source_pending_or_not_checked"}
SCORES_BY_CISI = {
    "M-1044": {
        "same_preframe_visible": "yes",
        "terminal_zone_visible": "yes",
        "post_861_material_visible": "no",
        "post_861_material_type": "bare_terminal_edge",
        "same_line_continuity": "yes",
        "closure_or_tail_score": "bare_closure",
        "confidence": "medium",
        "visual_note": "Blurred Mohenjo bare control; terminal-side window has no visible post-861 addendum in checked crop.",
    },
    "M-91": {
        "same_preframe_visible": "yes",
        "terminal_zone_visible": "yes",
        "post_861_material_visible": "yes",
        "post_861_material_type": "compound_two_unit_tail",
        "same_line_continuity": "yes",
        "closure_or_tail_score": "tailed_continuation",
        "confidence": "high",
        "visual_note": "M-91 shows same-line post-861 material occupying the terminal-side window; visually a longer compound tail than M-240.",
    },
    "M-240": {
        "same_preframe_visible": "yes",
        "terminal_zone_visible": "yes",
        "post_861_material_visible": "yes",
        "post_861_material_type": "simple_one_unit_tail",
        "same_line_continuity": "yes",
        "closure_or_tail_score": "tailed_continuation",
        "confidence": "medium",
        "visual_note": "M-240 shows a single terminal-side post-861 unit; blur/crop limits fine-form confidence but layout supports a real tail.",
    },
    "M-723": {
        "same_preframe_visible": "yes",
        "terminal_zone_visible": "yes",
        "post_861_material_visible": "no",
        "post_861_material_type": "bare_terminal_edge",
        "same_line_continuity": "yes",
        "closure_or_tail_score": "bare_closure",
        "confidence": "medium",
        "visual_note": "M-723 bare control has a terminal-side signband window but no separate post-861 material in the checked overlay.",
    },
    "H-444": {
        "same_preframe_visible": "yes",
        "terminal_zone_visible": "yes",
        "post_861_material_visible": "no",
        "post_861_material_type": "bare_terminal_edge",
        "same_line_continuity": "yes",
        "closure_or_tail_score": "bare_closure",
        "confidence": "high",
        "visual_note": "H-444 is the cleanest bare 220-032 control in this packet; the checked terminal-side region supports closure.",
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                keys.append(key)
                seen.add(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def source_ready(row: dict[str, str]) -> bool:
    return row.get("source_status", "") not in SOURCE_PENDING or bool(row.get("display_image", ""))


def counter_string(counter: Counter[str]) -> str:
    return ";".join(f"{key}:{value}" for key, value in counter.most_common())


def blind_id(row: dict[str, str]) -> str:
    seed = f"{row['cisi']}|{row['text']}|{row['tail']}"
    return "B" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:6].upper()


def image_path(row: dict[str, str]) -> Path | None:
    raw = row.get("display_image", "")
    if not raw:
        return None
    path = Path(raw)
    if not path.is_absolute():
        path = ROOT / raw
    return path if path.exists() else None


def make_rows(rows: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    target = [row for row in rows if row.get("prefix_last2") == "220 032"]
    target.sort(key=lambda row: (row["cisi"], row["text"]))

    packet: list[dict[str, Any]] = []
    key: list[dict[str, Any]] = []
    scores: list[dict[str, Any]] = []
    for row in target:
        bid = blind_id(row)
        path = image_path(row)
        packet_row = {
            "blind_id": bid,
            "has_display_image": bool(path),
            "source_ready": source_ready(row),
            "source_status": row.get("source_status", ""),
            "site": row.get("site", ""),
            "type": row.get("type", ""),
            "symbol": row.get("symbol", ""),
            "shape": row.get("shape", ""),
            "display_image": str(path) if path else "",
        }
        packet.append(packet_row)
        key.append(
            {
                **packet_row,
                "cisi": row["cisi"],
                "tail": row["tail"],
                "text": row["text"],
                "prefix": row["prefix"],
                "register_key": row["register_key"],
            }
        )
        if path:
            score = {
                "blind_id": bid,
                "same_preframe_visible": "",
                "terminal_zone_visible": "",
                "post_861_material_visible": "",
                "post_861_material_type": "",
                "same_line_continuity": "",
                "closure_or_tail_score": "",
                "confidence": "",
                "visual_note": "",
            }
            score.update(SCORES_BY_CISI.get(row["cisi"], {}))
            scores.append(score)
    packet.sort(key=lambda row: row["blind_id"])
    key.sort(key=lambda row: row["blind_id"])
    scores.sort(key=lambda row: row["blind_id"])
    return packet, key, scores


def write_sheet(packet: list[dict[str, Any]], out_path: Path) -> None:
    image_rows = [row for row in packet if row["has_display_image"]]
    cell_w, cell_h = 520, 330
    thumbs: list[Image.Image] = []
    for row in image_rows:
        path = Path(str(row["display_image"]))
        img = Image.open(path).convert("RGB")
        img.thumbnail((cell_w - 24, cell_h - 68))
        canvas = Image.new("RGB", (cell_w, cell_h), "white")
        canvas.paste(img, ((cell_w - img.width) // 2, 50))
        draw = ImageDraw.Draw(canvas)
        draw.text((12, 10), str(row["blind_id"]), fill=(0, 0, 0))
        draw.text((12, 28), f"{row['site']} | {row['type']} | {row['shape']}", fill=(70, 70, 70))
        thumbs.append(canvas)

    cols = 2
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "white")
    for idx, thumb in enumerate(thumbs):
        framed = ImageOps.expand(thumb, border=1, fill=(180, 180, 180))
        sheet.paste(framed, ((idx % cols) * cell_w, (idx // cols) * cell_h))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path)


def write_doc(path: Path, summary: dict[str, Any]) -> None:
    lines = [
        "# 032-002-861 / 220-032 Source-Visible Contrast Packet",
        "",
        "Date: 2026-05-29",
        "",
        "## Question",
        "",
        "When `220-032` immediately precedes `002-861`, does the post-`861` outcome behave like a real tail-choice contrast rather than a register artifact or a single-row accident?",
        "",
        "## Packet",
        "",
        f"- Rows with `prefix_last2=220 032`: `{summary['rows']}`",
        f"- Source-ready rows: `{summary['source_ready_rows']}`",
        f"- Display-image rows in blind sheet: `{summary['image_rows']}`",
        f"- Tail distribution: `{summary['tail_distribution']}`",
        f"- Source-ready tail distribution: `{summary['source_ready_tail_distribution']}`",
        f"- Blind sheet: `{summary['blind_sheet']}`",
        f"- Blind key: `{summary['blind_key']}`",
        "",
        "## Pre-Review Decision",
        "",
        "- This is the best current source-visible minimal-contrast packet in the post-`861` field.",
        "- It already blocks a binary reading of `220-032-002-861` as simply terminal or simply selecting `603`: the same last-two preframe reaches bare closure, `603`, and `255-416`.",
        "- The packet is not allowed to produce sign values. It can only score visible behavior: closure, simple tail, compound tail, same-line continuity, and whether the source images actually support the catalog split.",
        "",
        "## Human Visual Score",
        "",
        "The sheet is semi-blind, not fully blind, because the existing overlay captions leak object/tail labels. It still supports the layout question.",
        "",
        "- `B0B5F50 / M-1044 / <END>`: bare closure, medium confidence. Blurred, but the checked terminal-side window has no visible post-`861` addendum.",
        "- `B1730A3 / M-91 / 255-416`: tailed continuation, high confidence. Same-line terminal-side material is visible as a longer compound tail.",
        "- `BC6B344 / M-240 / 603`: tailed continuation, medium confidence. A single terminal-side post-`861` unit is visible; blur limits fine-form confidence.",
        "- `BE2B253 / M-723 / <END>`: bare closure, medium confidence. Terminal-side signband is visible with no separate post-`861` material in the checked overlay.",
        "- `BF77F3D / H-444 / <END>`: bare closure, high confidence. Cleanest bare `220-032` control in this packet.",
        "",
        "## Result",
        "",
        "The `220-032` split survives visual inspection as a source-visible positional contrast: the same immediate preframe reaches bare closure, a simple one-unit tail, and a longer compound tail. This is now the best post-`861` research object because it is a cluster-level language question, not a single-sign defense.",
        "",
        "The result does not assign values to `603`, `255`, `416`, `861`, `220`, or `032`. It also does not prove source-derived token boundaries. It only says the source images support a real closure-vs-tail-vs-compound-tail contrast worth modeling.",
        "",
        "Next linguistic gate: test whether line length, icon/register, and available terminal space explain the split as well as the post-`861` tail classes. If they do not, the object becomes a candidate grammar slot after `861`; if they do, it stays layout/register behavior.",
        "",
        "Accepted sign values, phonetics, language identity, translations, exact source-token boundaries, and sign meanings remain 0/unaccepted.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    all_rows = read_csv(INPUT_ROWS)
    packet, key, scores = make_rows(all_rows)
    if not packet:
        raise SystemExit("no prefix_last2=220 032 rows found")

    blind_sheet = TMP_OUT / f"{OUT_PREFIX}_blind_sheet.png"
    write_sheet(packet, blind_sheet)

    target_rows = [row for row in all_rows if row.get("prefix_last2") == "220 032"]
    source_rows = [row for row in target_rows if source_ready(row)]
    image_rows = [row for row in key if row["has_display_image"]]
    summary = {
        "date": "2026-05-29",
        "rows": len(target_rows),
        "source_ready_rows": len(source_rows),
        "image_rows": len(image_rows),
        "tail_distribution": counter_string(Counter(row["tail"] for row in target_rows)),
        "source_ready_tail_distribution": counter_string(Counter(row["tail"] for row in source_rows)),
        "blind_sheet": str(blind_sheet),
        "blind_key": str(REPORTS / f"{OUT_PREFIX}_blind_key.csv"),
        "visual_score_status": "semi_blind_scored_overlay_captions_leak_labels",
        "visual_result": "source_visible_positional_contrast_survives_as_closure_vs_simple_tail_vs_compound_tail",
        "visual_limits": "no sign values, no phonetics, no language identity, no translations, no exact source-token boundary acceptance",
        "source_missing_rows": [
            {"cisi": row["cisi"], "tail": row["tail"], "text": row["text"], "source_status": row["source_status"]}
            for row in target_rows
            if not source_ready(row)
        ],
    }

    write_csv(REPORTS / f"{OUT_PREFIX}_packet_rows.csv", packet)
    write_csv(REPORTS / f"{OUT_PREFIX}_blind_key.csv", key)
    write_csv(REPORTS / f"{OUT_PREFIX}_visual_scores.csv", scores)
    (REPORTS / f"{OUT_PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_doc(DOCS / f"{OUT_PREFIX}.md", summary)
    print(json.dumps({"status": "220032_source_visible_contrast_packet_built", **summary}, indent=2))


if __name__ == "__main__":
    main()
