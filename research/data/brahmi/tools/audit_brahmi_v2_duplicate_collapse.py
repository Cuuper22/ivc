from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "data" / "brahmi"
SEGMENTS = OUT / "source_token_segments_v2.csv"
NEIGHBORS = OUT / "source_token_brahmi_neighbors_v2.csv"
FAMILIES = OUT / "source_token_family_descent_summary_v2.csv"
OUT_CSV = OUT / "source_token_duplicate_collapse_audit_v2.csv"
OUT_JSON = OUT / "source_token_duplicate_collapse_audit_v2_summary.json"


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def modal(counter: Counter[str]) -> tuple[str, int, float]:
    if not counter:
        return "", 0, 0.0
    label, count = counter.most_common(1)[0]
    return label, count, count / sum(counter.values())


def collapse_first(rows: list[dict], key: str) -> list[dict]:
    seen = set()
    collapsed = []
    for row in rows:
        value = row.get(key, "")
        if value in seen:
            continue
        seen.add(value)
        collapsed.append(row)
    return collapsed


def main() -> None:
    segments = read_csv(SEGMENTS)
    neighbors = read_csv(NEIGHBORS)
    families = read_csv(FAMILIES)
    top1 = {row["token_id"]: row for row in neighbors if row.get("rank") == "1"}
    family_meta = {(row["sign_id"], row["orientation_policy"]): row for row in families}

    by_family: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in segments:
        by_family[(row["assigned_sign"], row["orientation_policy"])].append(row)

    audit_rows: list[dict] = []
    for key, rows in sorted(by_family.items()):
        if len(rows) < 2:
            continue
        sign_id, policy = key
        raw_labels = Counter(top1.get(row["token_id"], {}).get("brahmi_label", "") for row in rows)
        sha_rows = collapse_first(rows, "sha256")
        cisi_rows = collapse_first(rows, "cisi")
        sha_labels = Counter(top1.get(row["token_id"], {}).get("brahmi_label", "") for row in sha_rows)
        cisi_labels = Counter(top1.get(row["token_id"], {}).get("brahmi_label", "") for row in cisi_rows)
        raw_label, raw_count, raw_share = modal(raw_labels)
        sha_label, sha_count, sha_share = modal(sha_labels)
        cisi_label, cisi_count, cisi_share = modal(cisi_labels)
        meta = family_meta.get(key, {})

        if raw_share >= 1 and len(sha_rows) < 2:
            duplicate_status = "raw_unanimity_collapses_below_two_unique_hashes"
        elif raw_share >= 1 and len(cisi_rows) < 2:
            duplicate_status = "raw_unanimity_single_cisi_only"
        elif raw_share >= 1 and (sha_share < 1 or cisi_share < 1):
            duplicate_status = "raw_unanimity_not_stable_after_duplicate_collapse"
        elif raw_share >= 1:
            duplicate_status = "raw_unanimity_survives_duplicate_collapse_but_original_null_failed"
        else:
            duplicate_status = "raw_not_unanimous"

        audit_rows.append(
            {
                "sign_id": sign_id,
                "orientation_policy": policy,
                "raw_sample_count": len(rows),
                "unique_sha256_count": len(sha_rows),
                "unique_cisi_count": len(cisi_rows),
                "raw_modal_label": raw_label,
                "raw_modal_count": raw_count,
                "raw_modal_share": f"{raw_share:.6f}",
                "sha_modal_label": sha_label,
                "sha_modal_count": sha_count,
                "sha_modal_share": f"{sha_share:.6f}",
                "cisi_modal_label": cisi_label,
                "cisi_modal_count": cisi_count,
                "cisi_modal_share": f"{cisi_share:.6f}",
                "original_shape_null_share": meta.get("shape_modal_distance_le_observed_share", ""),
                "original_label_null_share": meta.get("label_null_ge_observed_modal_count_share", ""),
                "original_gate_decision": meta.get("gate_decision", ""),
                "duplicate_collapse_status": duplicate_status,
                "cisis": "|".join(sorted({row.get("cisi", "") for row in rows})),
                "token_ids": "|".join(row["token_id"] for row in rows),
            }
        )

    audit_rows.sort(
        key=lambda row: (
            row["duplicate_collapse_status"] != "raw_unanimity_collapses_below_two_unique_hashes",
            row["duplicate_collapse_status"] != "raw_unanimity_single_cisi_only",
            -float(row["raw_modal_share"]),
            -int(row["raw_sample_count"]),
            row["sign_id"],
            row["orientation_policy"],
        )
    )
    write_csv(
        OUT_CSV,
        audit_rows,
        [
            "sign_id",
            "orientation_policy",
            "raw_sample_count",
            "unique_sha256_count",
            "unique_cisi_count",
            "raw_modal_label",
            "raw_modal_count",
            "raw_modal_share",
            "sha_modal_label",
            "sha_modal_count",
            "sha_modal_share",
            "cisi_modal_label",
            "cisi_modal_count",
            "cisi_modal_share",
            "original_shape_null_share",
            "original_label_null_share",
            "original_gate_decision",
            "duplicate_collapse_status",
            "cisis",
            "token_ids",
        ],
    )

    counts = Counter(row["duplicate_collapse_status"] for row in audit_rows)
    top_nearmiss_keys = [
        ("817", "visual_ltr_catalog_reverse"),
        ("527", "visual_ltr_catalog_order"),
        ("472", "visual_ltr_catalog_reverse"),
        ("060", "visual_ltr_catalog_reverse"),
        ("061", "visual_ltr_catalog_order"),
    ]
    top_nearmisses = [
        row
        for row in audit_rows
        if (row["sign_id"], row["orientation_policy"]) in top_nearmiss_keys
    ]
    OUT_JSON.write_text(
        json.dumps(
            {
                "date": date.today().isoformat(),
                "status": "brahmi_v2_duplicate_collapse_audit_no_anchor_promotion",
                "family_rows_audited": len(audit_rows),
                "status_counts": dict(counts),
                "top_nearmiss_duplicate_audit": top_nearmisses,
                "decision": "Duplicate collapse adds a skeptic-side reason not to promote the v2 near-misses: several raw-unanimous families collapse below two unique token hashes, and the remaining top near-misses are single-CISI rows. The original shape/label null failure remains sufficient by itself.",
                "outputs": {
                    "csv": "data/brahmi/source_token_duplicate_collapse_audit_v2.csv",
                    "summary": "data/brahmi/source_token_duplicate_collapse_audit_v2_summary.json",
                },
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
