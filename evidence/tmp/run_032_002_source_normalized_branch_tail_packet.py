import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()
REPORTS = ROOT / "data/open_prototype/reports"
TAIL_INSTANCES = REPORTS / "campaign_032_002_post_y_tail_family_instances.csv"
SOURCE_ROUTE = REPORTS / "campaign_032_002_y_source_route_probe.csv"
SOURCE_CURRENT = REPORTS / "campaign_032_002_y_source_function_current_table.csv"
TOKEN_BOXES = REPORTS / "campaign_032_002_y_token_box_scaffold_v1.csv"

DECISIVE_CISI = {"M-49", "M-70", "M-91", "M-1677", "M-240", "-"}
TAIL_FAMILIES = {
    ("390", "125"),
    ("390", "705"),
    ("220", "455"),
    ("220", "065"),
    ("861", "603"),
    ("861", "533"),
}


def load_csv(path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def by_cisi(rows):
    out = {}
    for r in rows:
        cisi = r.get("cisi", "")
        if cisi and cisi not in out:
            out[cisi] = r
    return out


def token_box_index(rows):
    out = {}
    for r in rows:
        cisi = r.get("cisi", "")
        if not cisi:
            continue
        out.setdefault(cisi, {"rows": 0, "statuses": Counter(), "overlays": set(), "notes": set()})
        out[cisi]["rows"] += 1
        out[cisi]["statuses"][r.get("status", "")] += 1
        if r.get("overlay_image"):
            out[cisi]["overlays"].add(r["overlay_image"])
        if r.get("note"):
            out[cisi]["notes"].add(r["note"])
    return out


def source_status(cisi, source_current, source_route, token_boxes):
    current = source_current.get(cisi)
    route = source_route.get(cisi)
    boxes = token_boxes.get(cisi)
    if current and current.get("source_visible") == "yes":
        base = "source_visible_row_level"
    elif route and route.get("route_status"):
        base = route["route_status"]
    elif cisi == "-":
        base = "no_object_id"
    elif not cisi:
        base = "missing_cisi"
    else:
        base = "not_routed_in_current_packet"

    if boxes:
        box_status = ";".join(f"{k}:{v}" for k, v in boxes["statuses"].most_common())
        overlay = ";".join(sorted(boxes["overlays"]))
        note = " | ".join(sorted(boxes["notes"]))
    else:
        box_status = "none"
        overlay = ""
        note = ""

    if base == "source_visible_row_level" and boxes:
        admissibility = "source_boxed_candidate"
    elif base == "source_visible_row_level":
        admissibility = "source_visible_needs_token_boxes"
    elif base == "local_source_reference_route":
        admissibility = "source_route_known_needs_image"
    elif base == "source_volume_ocr_hit":
        admissibility = "source_volume_route_needs_crop_or_existing_check"
    elif base == "no_object_id":
        admissibility = "blocked_until_object_id_resolved"
    else:
        admissibility = "needs_source_route"

    return {
        "source_status": base,
        "admissibility": admissibility,
        "token_box_status": box_status,
        "token_box_overlay": overlay,
        "token_box_note": note,
        "source_page": current.get("source_page", "") if current else "",
        "source_crop": current.get("crop_file", "") if current else "",
        "route_next_action": route.get("next_action", "") if route else "",
        "route_required_checks": route.get("required_source_checks", "") if route else "",
        "excavation_idno": route.get("excavation_idno", "") if route else "",
    }


def main():
    tail_rows = load_csv(TAIL_INSTANCES)
    source_current = by_cisi(load_csv(SOURCE_CURRENT))
    source_route = by_cisi(load_csv(SOURCE_ROUTE))
    token_boxes = token_box_index(load_csv(TOKEN_BOXES))

    decisive = []
    family = []
    for r in tail_rows:
        is_after = r.get("scope") == "after_032_strict_dedup"
        is_decisive = is_after and r.get("cisi") in DECISIVE_CISI
        is_family = r.get("scope") == "all_002_strict_dedup" and (r.get("y_after_002"), r.get("tail_next1")) in TAIL_FAMILIES
        if not (is_decisive or is_family):
            continue
        status = source_status(r.get("cisi", ""), source_current, source_route, token_boxes)
        item = {
            "packet_role": "decisive_adjacent" if is_decisive else "all_002_tail_family",
            "scope": r.get("scope", ""),
            "id": r.get("id", ""),
            "cisi": r.get("cisi", ""),
            "site": r.get("site", ""),
            "type": r.get("type", ""),
            "symbol": r.get("symbol", ""),
            "frame_kind": r.get("frame_kind", ""),
            "text": r.get("text", ""),
            "idx_002": r.get("idx_002", ""),
            "y_after_002": r.get("y_after_002", ""),
            "y_class": r.get("y_class", ""),
            "tail_full": r.get("tail_full", ""),
            "tail_next1": r.get("tail_next1", ""),
            "tail_len": r.get("tail_len", ""),
            "tail_has_032": r.get("tail_has_032", ""),
            **status,
        }
        if is_decisive:
            decisive.append(item)
        if is_family:
            item2 = dict(item)
            item2["packet_role"] = "all_002_tail_family"
            family.append(item2)

    fields = [
        "packet_role",
        "scope",
        "id",
        "cisi",
        "site",
        "type",
        "symbol",
        "frame_kind",
        "text",
        "idx_002",
        "y_after_002",
        "y_class",
        "tail_next1",
        "tail_full",
        "tail_len",
        "tail_has_032",
        "source_status",
        "admissibility",
        "token_box_status",
        "source_page",
        "source_crop",
        "token_box_overlay",
        "excavation_idno",
        "route_next_action",
        "route_required_checks",
        "token_box_note",
    ]

    decisive_path = REPORTS / "campaign_032_002_source_normalized_branch_tail_decisive_rows.csv"
    family_path = REPORTS / "campaign_032_002_source_normalized_branch_tail_family_rows.csv"
    summary_path = REPORTS / "campaign_032_002_source_normalized_branch_tail_summary.json"
    for path, rows in [(decisive_path, decisive), (family_path, family)]:
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for row in sorted(rows, key=lambda x: (x["packet_role"], x["y_after_002"], x["tail_next1"], x["cisi"], x["id"])):
                w.writerow({k: row.get(k, "") for k in fields})

    summary = {
        "decisive_rows": len(decisive),
        "family_rows": len(family),
        "decisive_admissibility_counts": dict(Counter(r["admissibility"] for r in decisive)),
        "family_admissibility_counts": dict(Counter(r["admissibility"] for r in family)),
        "family_counts": dict(Counter(f"{r['y_after_002']}->{r['tail_next1']}" for r in family)),
        "decisive_path": str(decisive_path.resolve()),
        "family_path": str(family_path.resolve()),
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
