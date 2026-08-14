"""Build the canonical source-normalized dataset of every post-002-861 row.

This is the packet-builder the later tail scripts read from. It scans the
strict corpus for every inscription containing 002-861 and extracts one row
per occurrence with full metadata: prefix at three depths, tail and tail
bucket, register keys, template key, and physical measurements. It then
enriches each row from six earlier report CSVs — attachment verdicts,
attachment boxes, bare-edge crops, register crops, register independence, and
layout discriminator — so every row carries its source status (has the actual
image been checked?) and pixel layout numbers where they exist. On top of
that it builds a predictor table, a minimal-contrast list, a hand-selected
packet of rows worth looking at (plus external 603/636/642 controls), and
five campaign decisions. Outputs: five CSVs including the all-rows file other
scripts consume, a JSON summary, a contact-sheet PNG, and a Markdown doc.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageOps


ROOT = Path.cwd()
METADATA = ROOT / "data" / "open_prototype" / "lipi" / "metadata_filtered.csv"
REPORTS = ROOT / "data" / "open_prototype" / "reports"
DOCS = ROOT / "docs"
TMP_OUT = ROOT / "tmp" / "032_002_861_source_normalized_tail_predictor_packet"

ATTACHMENT_VERDICTS = REPORTS / "campaign_032_002_861_source_token_attachment_verdicts.csv"
ATTACHMENT_BOXES = REPORTS / "campaign_032_002_861_source_token_attachment_boxes.csv"
BARE_EDGE_CROPS = REPORTS / "campaign_032_002_861_bare_edge_source_controls_crops.csv"
REGISTER_CROPS = REPORTS / "campaign_032_002_861_533717_source_controls_crops.csv"
REGISTER_INDEPENDENCE = REPORTS / "campaign_032_002_861_533717_source_family_independence_rows.csv"
LAYOUT_DISCRIMINATOR = REPORTS / "campaign_032_002_861_533717_source_layout_discriminator_rows.csv"
EXTERNAL_603 = REPORTS / "campaign_032_002_861_603_source_normalized_slot_family.csv"

OUT_PREFIX = "campaign_032_002_861_source_normalized_tail_predictor"
FOCUS_TAILS = {"533 717", "603", "255 416", "360 520 919 140"}
NO_ICON_SEALR_POOL = {"M-1954", "M-355", "M-376", "M-391", "M-1267", "M-1273", "M-1973"}
BARE_EDGE_POOL = {"H-444", "M-723", "M-1044", "M-77", "M-118", "M-15"}


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


def parse_tokens(text: str) -> list[str] | None:
    if not (text.startswith("+") and text.endswith("+")):
        return None
    if any(ch in text for ch in "[]()"):
        return None
    tokens = [token for token in text.strip("+").split("-") if token]
    if not tokens or not all(re.fullmatch(r"\d{3}", token) for token in tokens):
        return None
    return tokens


def load_strict_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen = set()
    with METADATA.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            tokens = parse_tokens(row["text"])
            if tokens is None:
                continue
            key = (row["cisi"], row["site"], row["type"], row["symbol"], row["text"])
            if key in seen:
                continue
            seen.add(key)
            out: dict[str, Any] = dict(row)
            out["_tokens"] = tokens
            rows.append(out)
    return rows


def post861_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        tokens = row["_tokens"]
        for idx in range(len(tokens) - 1):
            if tokens[idx : idx + 2] != ["002", "861"]:
                continue
            prefix = tokens[:idx]
            tail = tokens[idx + 2 :]
            tail_text = " ".join(tail) if tail else "<END>"
            out.append(
                {
                    "id": row["id"],
                    "cisi": row["cisi"],
                    "site": row["site"],
                    "type": row["type"],
                    "symbol": row["symbol"],
                    "shape": row["shape"],
                    "cross_section": row.get("cross-section", ""),
                    "material": row["material"],
                    "condition": row["condition"],
                    "direction": row["dir."],
                    "class": row["class"],
                    "area_section": row.get("area-section", ""),
                    "block_house": row.get("block-house", ""),
                    "room_grid": row.get("room-grid", ""),
                    "excavation_idno": row.get("excavation-idno", ""),
                    "period": row.get("period", ""),
                    "phase": row.get("phase", ""),
                    "depth": row.get("depth", ""),
                    "horizontal_mm": row.get("horizontal(mm)", ""),
                    "vertical_mm": row.get("vertical(mm)", ""),
                    "thickness_mm": row.get("thickness(mm)", ""),
                    "text": row["text"],
                    "text_length": row["text length"],
                    "prefix": " ".join(prefix),
                    "prefix_len": len(prefix),
                    "prefix_last1": prefix[-1] if prefix else "<START>",
                    "prefix_last2": " ".join(prefix[-2:]) if len(prefix) >= 2 else prefix[-1] if prefix else "<START>",
                    "prefix_last3": " ".join(prefix[-3:]) if len(prefix) >= 3 else " ".join(prefix) if prefix else "<START>",
                    "tail": tail_text,
                    "tail_len": len(tail),
                    "tail_bucket": tail_bucket(tail_text),
                    "register_key": register_key(row),
                    "broad_register_key": broad_register_key(row),
                    "no_icon_sealr": row["site"] == "Mohenjo-daro" and row["type"] == "SEAL:R" and row["symbol"] == "None",
                    "mohenjo_seals_square": row["site"] == "Mohenjo-daro" and row["type"] == "SEAL:S" and row["shape"] == "square",
                    "terminal_after_tail": idx + 2 + len(tail) == len(tokens),
                    "template_key": template_key(tokens),
                }
            )
    return out


def tail_bucket(tail: str) -> str:
    if tail == "<END>":
        return "bare_closure"
    if tail == "533 717":
        return "fixed_533_717"
    if tail == "603":
        return "simple_603"
    if tail == "255 416":
        return "singleton_255_416"
    if tail == "360 520 919 140":
        return "long_360_520_919_140"
    return "other_post861_tail"


def register_key(row: dict[str, Any]) -> str:
    return "|".join(str(row.get(key, "")) for key in ["site", "type", "symbol", "shape"])


def broad_register_key(row: dict[str, Any]) -> str:
    return "|".join(str(row.get(key, "")) for key in ["site", "type", "symbol"])


def template_key(tokens: list[str]) -> str:
    out = tokens[:]
    for idx in range(len(out) - 1):
        if out[idx : idx + 2] == ["002", "861"]:
            out[idx + 2 :] = ["TAIL"] if idx + 2 < len(out) else []
            return "+" + "-".join(out) + "+"
    return "+" + "-".join(out) + "+"


def first_existing(paths: list[str]) -> str:
    for raw in paths:
        if not raw:
            continue
        path = Path(raw)
        if not path.is_absolute():
            path = ROOT / raw
        if path.exists():
            return str(path)
    return ""


def source_index() -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = defaultdict(dict)

    for row in read_csv(ATTACHMENT_VERDICTS):
        cisi = row["cisi"]
        out[cisi].update(
            {
                "source_kind": "same_line_tail_attachment_candidate",
                "source_status": row.get("attachment_verdict", ""),
                "source_quality": row.get("source_quality", ""),
                "source_route": row.get("source_route", ""),
                "source_note": row.get("observation", ""),
                "source_limit": row.get("limit", ""),
                "source_image_abs": row.get("source_image_abs", ""),
                "overlay_abs": row.get("overlay_abs", ""),
                "display_image": first_existing([row.get("overlay_abs", ""), row.get("source_image_abs", "")]),
            }
        )

    for row in read_csv(BARE_EDGE_CROPS):
        cisi = row["cisi"]
        out[cisi].update(
            {
                "source_kind": "bare_edge_control",
                "source_status": row.get("visual_status", ""),
                "source_quality": "control",
                "source_route": row.get("source_note", ""),
                "source_note": row.get("source_note", ""),
                "source_limit": "bare-edge control, not same-line tail attachment evidence",
                "source_image_abs": row.get("source_image_abs", ""),
                "overlay_abs": row.get("overlay_abs", ""),
                "display_image": first_existing([row.get("overlay_abs", ""), row.get("source_image_abs", "")]),
            }
        )

    register_seen: set[str] = set()
    for row in read_csv(REGISTER_CROPS):
        cisi = row["cisi"]
        if cisi in register_seen and not row.get("side", "").isupper():
            continue
        register_seen.add(cisi)
        previous = out.get(cisi, {})
        out[cisi].update(
            {
                "source_kind": previous.get("source_kind", "register_control_crop"),
                "source_status": previous.get("source_status", row.get("status", "")),
                "source_quality": previous.get("source_quality", "control_crop"),
                "source_route": previous.get("source_route", row.get("source_route", "")),
                "source_note": previous.get("source_note", row.get("role", "")),
                "source_limit": previous.get("source_limit", "register-control crop, not same-line attachment verdict"),
                "source_image_abs": previous.get("source_image_abs", row.get("crop_path", "")),
                "overlay_abs": previous.get("overlay_abs", ""),
                "display_image": previous.get("display_image") or first_existing([row.get("crop_path", "")]),
            }
        )

    for row in read_csv(REGISTER_INDEPENDENCE):
        cisi = row["cisi"]
        out[cisi].update(
            {
                "source_leaf": row.get("source_leaf", ""),
                "printed_page": row.get("printed_page", ""),
                "route_status": row.get("route_status", ""),
            }
        )

    return out


def layout_index() -> dict[str, dict[str, Any]]:
    by_cisi: dict[str, dict[str, Any]] = defaultdict(dict)
    boxes: dict[str, dict[str, dict[str, int]]] = defaultdict(dict)
    for row in read_csv(ATTACHMENT_BOXES):
        boxes[row["cisi"]][row["box_role"]] = {key: int(row[key]) for key in ["x1", "y1", "x2", "y2"]}
    for cisi, roles in boxes.items():
        line = roles.get("line_window")
        tail = roles.get("tail_window")
        pre = roles.get("pre_tail_window")
        if not line or not tail:
            continue
        line_width = max(1, line["x2"] - line["x1"])
        tail_width = max(0, tail["x2"] - tail["x1"])
        pre_width = max(0, pre["x2"] - pre["x1"]) if pre else ""
        by_cisi[cisi].update(
            {
                "line_width_px": line_width,
                "pre_tail_width_px": pre_width,
                "tail_width_px": tail_width,
                "tail_start_share_of_line": round((tail["x1"] - line["x1"]) / line_width, 3),
                "tail_width_share_of_line": round(tail_width / line_width, 3),
                "layout_status": "quantified_same_line_overlay",
            }
        )

    for row in read_csv(LAYOUT_DISCRIMINATOR):
        cisi = row["cisi"]
        for key in [
            "line_width_px",
            "tail_width_px",
            "tail_start_share_of_line",
            "tail_width_share_of_line",
            "layout_status",
            "layout_observation",
        ]:
            if row.get(key) and not by_cisi[cisi].get(key):
                by_cisi[cisi][key] = row[key]
    return by_cisi


def enrich(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = source_index()
    layouts = layout_index()
    bare = [row for row in rows if row["tail"] == "<END>"]
    for row in rows:
        source = sources.get(row["cisi"], {})
        layout = layouts.get(row["cisi"], {})
        row.update(
            {
                "source_kind": source.get("source_kind", "source_pending_or_not_checked"),
                "source_status": source.get("source_status", "source_pending_or_not_checked"),
                "source_quality": source.get("source_quality", ""),
                "source_route": source.get("source_route", ""),
                "source_note": source.get("source_note", ""),
                "source_limit": source.get("source_limit", ""),
                "source_leaf": source.get("source_leaf", ""),
                "printed_page": source.get("printed_page", ""),
                "route_status": source.get("route_status", ""),
                "display_image": source.get("display_image", ""),
                "same_last2_bare_count": sum(1 for b in bare if b["prefix_last2"] == row["prefix_last2"]),
                "same_last1_bare_count": sum(1 for b in bare if b["prefix_last1"] == row["prefix_last1"]),
                "same_register_bare_count": sum(1 for b in bare if b["register_key"] == row["register_key"]),
                "same_broad_register_bare_count": sum(1 for b in bare if b["broad_register_key"] == row["broad_register_key"]),
            }
        )
        row.update(layout)
    return rows


def predictor_table(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    features = [
        ("prefix_last1", "preframe_last1"),
        ("prefix_last2", "preframe_last2"),
        ("prefix_last3", "preframe_last3"),
        ("register_key", "narrow_register"),
        ("broad_register_key", "broad_register"),
        ("shape", "shape"),
        ("site", "site"),
        ("no_icon_sealr", "no_icon_sealr"),
    ]
    table: list[dict[str, Any]] = []
    for key, label in features:
        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            groups[str(row[key])].append(row)
        mixed = []
        focus_groups = []
        for value, group in groups.items():
            tails = Counter(row["tail_bucket"] for row in group)
            if len(tails) > 1:
                mixed.append((value, tails))
            if any(row["tail"] in FOCUS_TAILS for row in group):
                focus_groups.append((value, tails))
        table.append(
            {
                "predictor": label,
                "groups": len(groups),
                "mixed_tail_groups": len(mixed),
                "groups_touching_focus_tails": len(focus_groups),
                "top_focus_groups": "; ".join(
                    f"{value} -> {counter_string(tails, 5)}" for value, tails in focus_groups[:10]
                ),
                "reading_relevance": predictor_relevance(label),
            }
        )
    return table


def predictor_relevance(label: str) -> str:
    if label.startswith("preframe"):
        return "linguistic predictor candidate if it beats register/source controls"
    if "register" in label or label in {"shape", "site", "no_icon_sealr"}:
        return "register/template adversary predictor"
    return "control predictor"


def counter_string(counter: Counter, topn: int = 8) -> str:
    return ",".join(f"{key}:{value}" for key, value in counter.most_common(topn))


def minimal_contrasts(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for feature in ["prefix_last2", "prefix_last1", "register_key", "broad_register_key"]:
        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in rows:
            groups[str(row[feature])].append(row)
        for value, group in groups.items():
            tails = Counter(row["tail"] for row in group)
            if len(tails) < 2:
                continue
            if not any(tail in FOCUS_TAILS for tail in tails):
                continue
            out.append(
                {
                    "contrast_feature": feature,
                    "contrast_value": value,
                    "rows": len(group),
                    "tail_distribution": counter_string(tails, 12),
                    "source_visible_rows": sum(1 for row in group if str(row["source_kind"]) != "source_pending_or_not_checked"),
                    "examples": "; ".join(f"{row['cisi']} {row['tail']} {row['text']}" for row in group[:12]),
                    "research_use": contrast_use(feature, value, tails),
                }
            )
    out.sort(key=lambda row: (row["contrast_feature"] != "prefix_last2", -int(row["source_visible_rows"]), -int(row["rows"])))
    return out


def contrast_use(feature: str, value: str, tails: Counter) -> str:
    if feature == "prefix_last2" and value == "220 032":
        return "live minimal contrast: same last-2 preframe reaches bare, 603, and 255-416; tail choice is not decided by prefix_last2 alone"
    if feature == "prefix_last1" and value in {"176", "803", "235"}:
        return "last-1 preframe has bare controls plus a focus tail; use for source-visible closure vs addendum tests"
    if "register" in feature:
        return "tests register/template explanation against focus-tail recurrence"
    return "secondary contrast"


def packet_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_cisi = {row["cisi"]: row for row in rows}
    selected: dict[str, str] = {}
    for row in rows:
        if row["tail"] in FOCUS_TAILS:
            selected[row["cisi"]] = "focus_tail_source_visible_or_target"
        if row["cisi"] in NO_ICON_SEALR_POOL:
            selected[row["cisi"]] = selected.get(row["cisi"], "no_icon_sealr_competing_predictor_pool")
        if row["cisi"] in BARE_EDGE_POOL:
            selected[row["cisi"]] = selected.get(row["cisi"], "source_visible_bare_edge_control")
        if row["prefix_last2"] == "220 032":
            selected[row["cisi"]] = selected.get(row["cisi"], "prefix_last2_220_032_minimal_contrast")
        if row["prefix_last1"] in {"176", "803", "235"} and row["source_kind"] != "source_pending_or_not_checked":
            selected[row["cisi"]] = selected.get(row["cisi"], f"prefix_last1_{row['prefix_last1']}_source_control")

    packet = []
    for cisi, reason in selected.items():
        if cisi in by_cisi:
            row = dict(by_cisi[cisi])
            row["packet_reason"] = reason
            packet.append(row)

    for row in external_603_controls():
        packet.append(row)

    packet.sort(key=lambda row: (str(row.get("packet_reason", "")), str(row.get("cisi", ""))))
    return packet


def external_603_controls() -> list[dict[str, Any]]:
    out = []
    for row in read_csv(EXTERNAL_603):
        files = [part.strip() for part in row.get("source_files", "").split(";")]
        out.append(
            {
                "id": "",
                "cisi": row["witness"],
                "site": "Harappa",
                "type": "TAB:B/I external_x_before_240_control",
                "symbol": "None/Bult",
                "shape": "",
                "text": row["slot_text"],
                "prefix": "",
                "prefix_len": "",
                "prefix_last1": row["x_value"],
                "prefix_last2": f"{row['x_value']} 240",
                "prefix_last3": f"740 {row['x_value']} 240",
                "tail": f"external_x_before_240_{row['x_value']}",
                "tail_bucket": "external_603_636_642_control",
                "register_key": "Harappa|TAB|external_x_before_240",
                "broad_register_key": "Harappa|TAB|external",
                "source_kind": "external_x_before_240_control",
                "source_status": row["source_status"],
                "source_route": row["source_route"],
                "source_note": row["notes"],
                "display_image": first_existing(files),
                "packet_reason": "negative_external_x_before_240_control",
                "source_object_weight": row.get("source_object_weight", ""),
                "linguistic_weight": row.get("linguistic_weight", ""),
            }
        )
    return out


def campaign_decisions(rows: list[dict[str, Any]], contrasts: list[dict[str, Any]]) -> list[dict[str, str]]:
    focus = {tail: [row for row in rows if row["tail"] == tail] for tail in FOCUS_TAILS}
    return [
        {
            "object": "533 717",
            "decision": "conditional_final_unit_candidate_not_morphology",
            "reason": "two source-visible rows, independent 533 absent, but all rows stay in Mohenjo no-icon SEAL:R cuboid-convex and compete with the long tail in the same narrow field",
            "next_discriminator": "human-score separability and copy-family similarity for M-376/M-391 against M-355/M-1267/M-1273/M-1973",
        },
        {
            "object": "603",
            "decision": "recurrent_post861_tail_stable_but_no_value",
            "reason": f"{len(focus['603'])} post-861 source-visible rows across multiple Mohenjo registers; X-before-240 bridge remains parked",
            "next_discriminator": "separate post-861 mobility from Harappa X-before-240 source-family recurrence",
        },
        {
            "object": "255 416",
            "decision": "singleton_minimal_contrast_member",
            "reason": "M-91 shares prefix_last2 220 032 with bare controls and M-240/603, so this is a real contrast slot but only one row",
            "next_discriminator": "source-visible comparison of M-91 vs M-240 vs H-444/M-723/M-1044",
        },
        {
            "object": "360 520 919 140",
            "decision": "long_tail_alternative_inside_533717_register",
            "reason": "M-355 blocks the claim that no-icon cuboid-convex SEAL:R simply equals 533-717; the same narrow field can choose a different long continuation",
            "next_discriminator": "source-normalized long-tail layout: continuation after 861 vs second unit after closure",
        },
        {
            "object": "220 032 contrast cluster",
            "decision": "preframe_last2_not_sufficient",
            "reason": "prefix_last2 220 032 reaches bare closure, 603, and 255-416 in source-visible/route-visible rows",
            "next_discriminator": "test full prefix, icon/register, and layout as competing predictors for the same preframe tail split",
        },
    ]


def write_contact_sheet(packet: list[dict[str, Any]], out_path: Path) -> None:
    image_rows = [row for row in packet if row.get("display_image")]
    if not image_rows:
        return
    thumbs = []
    cell_w, cell_h = 420, 300
    for row in image_rows[:30]:
        path = Path(str(row["display_image"]))
        if not path.exists():
            continue
        try:
            img = Image.open(path).convert("RGB")
        except Exception:
            continue
        img.thumbnail((cell_w - 20, cell_h - 70))
        canvas = Image.new("RGB", (cell_w, cell_h), "white")
        canvas.paste(img, ((cell_w - img.width) // 2, 48))
        draw = ImageDraw.Draw(canvas)
        label = f"{row.get('cisi', '')} | {row.get('tail', '')}"
        reason = str(row.get("packet_reason", row.get("source_kind", "")))[:58]
        draw.text((10, 8), label[:62], fill="black")
        draw.text((10, 26), reason, fill=(70, 70, 70))
        thumbs.append(canvas)
    if not thumbs:
        return
    cols = 3
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), "white")
    for idx, thumb in enumerate(thumbs):
        sheet.paste(ImageOps.expand(thumb, border=1, fill=(180, 180, 180)), ((idx % cols) * cell_w, (idx // cols) * cell_h))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path)


def write_doc(path: Path, summary: dict[str, Any], decisions: list[dict[str, str]], contrasts: list[dict[str, Any]]) -> None:
    lines = [
        "# 032-002-861 Source-Normalized Tail Predictor Packet",
        "",
        "Date: 2026-05-29",
        "",
        "## Question",
        "",
        "Do post-`861` tails behave more like linguistic preframe-conditioned continuations, register/template addenda, source-family artifacts, or layout/space effects?",
        "",
        "## Packet",
        "",
        f"- Strict rows scanned: `{summary['strict_rows_scanned']}`",
        f"- Rows with `002-861`: `{summary['rows_with_002_861']}`",
        f"- Packet rows: `{summary['packet_rows']}`",
        f"- Contact sheet: `{summary['contact_sheet']}`",
        f"- Tail buckets: `{summary['tail_bucket_counts']}`",
        "",
        "## Main Decisions",
        "",
    ]
    for item in decisions:
        lines.append(f"- `{item['object']}`: `{item['decision']}`. {item['reason']} Next discriminator: {item['next_discriminator']}.")

    lines.extend(["", "## Minimal Contrasts", ""])
    for row in contrasts[:10]:
        lines.append(
            f"- `{row['contrast_feature']}={row['contrast_value']}`: `{row['tail_distribution']}`; source-visible rows `{row['source_visible_rows']}`. {row['research_use']}."
        )

    lines.extend(
        [
            "",
            "## Predictor Read",
            "",
            "- Preframe alone does not currently promote a reading: the live `220 032` cluster splits into bare, `603`, and `255-416`.",
            "- Register alone also does not solve the field: `533-717` is locked to no-icon cuboid-convex `SEAL:R`, but the same narrow field also has the long `360-520-919-140` tail.",
            "- Source-family copying is weakened for `533-717` by separate source leaves and metadata contexts, but not killed; this needs blind visual scoring of hand/layout similarity.",
            "- `603` is now best treated as a stable recurrent post-`861` tail class with no accepted value and no active bridge to X-before-`240`.",
            "",
            "Accepted sign values, phonetics, language identity, translations, and exact source-normalized token identities remain 0/unaccepted.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    TMP_OUT.mkdir(parents=True, exist_ok=True)
    strict_rows = load_strict_rows()
    rows = enrich(post861_rows(strict_rows))
    predictors = predictor_table(rows)
    contrasts = minimal_contrasts(rows)
    packet = packet_rows(rows)
    decisions = campaign_decisions(rows, contrasts)

    contact_sheet = TMP_OUT / f"{OUT_PREFIX}_contact_sheet.png"
    write_contact_sheet(packet, contact_sheet)

    summary = {
        "date": "2026-05-29",
        "strict_rows_scanned": len(strict_rows),
        "rows_with_002_861": len(rows),
        "packet_rows": len(packet),
        "tail_bucket_counts": counter_string(Counter(row["tail_bucket"] for row in rows), 20),
        "focus_tail_counts": counter_string(Counter(row["tail"] for row in rows if row["tail"] in FOCUS_TAILS), 20),
        "contact_sheet": str(contact_sheet),
        "predictor_table": predictors,
        "decisions": decisions,
    }

    write_csv(REPORTS / f"{OUT_PREFIX}_all_rows.csv", rows)
    write_csv(REPORTS / f"{OUT_PREFIX}_packet_rows.csv", packet)
    write_csv(REPORTS / f"{OUT_PREFIX}_predictors.csv", predictors)
    write_csv(REPORTS / f"{OUT_PREFIX}_minimal_contrasts.csv", contrasts)
    write_csv(REPORTS / f"{OUT_PREFIX}_decisions.csv", decisions)
    (REPORTS / f"{OUT_PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_doc(DOCS / f"{OUT_PREFIX}_packet.md", summary, decisions, contrasts)
    print(json.dumps({"status": "source_normalized_tail_predictor_packet_built", **summary}, indent=2))


if __name__ == "__main__":
    main()
