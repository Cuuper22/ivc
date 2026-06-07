from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
DOCS = ROOT / "docs"

INPUT_ROWS = REPORTS / "campaign_032_002_861_source_normalized_tail_predictor_all_rows.csv"
SCORES = REPORTS / "campaign_032_002_861_220032_source_visible_contrast_packet_visual_scores.csv"
BLIND_KEY = REPORTS / "campaign_032_002_861_220032_source_visible_contrast_packet_blind_key.csv"
OUT_PREFIX = "campaign_032_002_861_220032_register_length_kill_test"
SOURCE_PENDING = {"", "source_pending_or_not_checked"}


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


def as_int(value: str) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def counter_string(counter: Counter[str]) -> str:
    return ";".join(f"{key}:{value}" for key, value in counter.most_common())


def outcome(row: dict[str, str]) -> str:
    if row["tail"] == "<END>":
        return "bare_closure"
    if row["tail"] == "603":
        return "simple_tail_603"
    if row["tail"] == "255 416":
        return "compound_tail_255_416"
    return "other_tail"


def values_by_outcome(rows: list[dict[str, Any]], field: str) -> dict[str, list[Any]]:
    out: dict[str, list[Any]] = defaultdict(list)
    for row in rows:
        value = row.get(field)
        if value not in ("", None):
            out[row["outcome"]].append(value)
    return dict(out)


def numeric_overlap(rows: list[dict[str, Any]], field: str) -> dict[str, Any]:
    by_outcome = values_by_outcome(rows, field)
    bare = [int(v) for v in by_outcome.get("bare_closure", [])]
    tailed = [int(v) for key, vals in by_outcome.items() if key != "bare_closure" for v in vals]
    if not bare or not tailed:
        return {"field": field, "testable": False}
    return {
        "field": field,
        "testable": True,
        "bare_values": ",".join(map(str, sorted(bare))),
        "tailed_values": ",".join(map(str, sorted(tailed))),
        "bare_min": min(bare),
        "bare_max": max(bare),
        "tailed_min": min(tailed),
        "tailed_max": max(tailed),
        "range_overlap": max(min(bare), min(tailed)) <= min(max(bare), max(tailed)),
        "exact_value_overlap": bool(set(bare) & set(tailed)),
    }


def summarize_feature(rows: list[dict[str, Any]], field: str) -> dict[str, Any]:
    groups = values_by_outcome(rows, field)
    return {
        "feature": field,
        "bare_closure": counter_string(Counter(groups.get("bare_closure", []))),
        "simple_tail_603": counter_string(Counter(groups.get("simple_tail_603", []))),
        "compound_tail_255_416": counter_string(Counter(groups.get("compound_tail_255_416", []))),
        "outcomes_present": ";".join(sorted(k for k, v in groups.items() if v)),
        "unique_values": len({v for vals in groups.values() for v in vals}),
    }


def decision_rows(rows: list[dict[str, Any]], feature_rows: list[dict[str, Any]], numeric_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    source_rows = [row for row in rows if row["source_ready"] == "1"]
    broad_register = next(row for row in feature_rows if row["feature"] == "type_shape")
    site = next(row for row in feature_rows if row["feature"] == "site")
    total_len = next(row for row in numeric_rows if row["field"] == "text_length_all_rows")
    source_total_len = next(row for row in numeric_rows if row["field"] == "text_length_source_ready")
    measured_layout = [row for row in source_rows if row.get("line_width_px")]
    bare_measured = [row for row in measured_layout if row["outcome"] == "bare_closure"]
    tailed_measured = [row for row in measured_layout if row["outcome"] != "bare_closure"]
    return [
        {
            "test": "broad_register",
            "decision": "fails_as_explanation",
            "evidence": f"type/shape source-ready split is {broad_register['bare_closure']} vs {broad_register['simple_tail_603']} vs {broad_register['compound_tail_255_416']}",
            "limit": "all source-ready rows are seal-square in this packet, so broad register cannot choose the tail",
        },
        {
            "test": "site",
            "decision": "fails_as_determinant",
            "evidence": f"site split is {site['bare_closure']} vs {site['simple_tail_603']} vs {site['compound_tail_255_416']}",
            "limit": "Mohenjo-daro contains bare closure, simple tail, and compound tail; Harappa only contributes one source-ready bare control here",
        },
        {
            "test": "total_text_length",
            "decision": "insufficient_as_explanation",
            "evidence": f"all rows bare lengths {total_len['bare_values']} vs tailed {total_len['tailed_values']}; source-ready bare {source_total_len['bare_values']} vs tailed {source_total_len['tailed_values']}",
            "limit": "total length partly tracks available continuation, but bare rows reach length 7/8 while tailed rows are 7/9; it is not a clean selector",
        },
        {
            "test": "fine_icon_symbol",
            "decision": "not_testable_as_general_explanation",
            "evidence": "fine symbol labels differ across the five image rows: Bull/Bull1/Bull1:W bare, Gaur for 603, Bull1:S for 255-416",
            "limit": "single rows per fine icon cannot distinguish icon function from row accident; broad Mohenjo seal-square already fails as determinant",
        },
        {
            "test": "terminal_space",
            "decision": "not_closed",
            "evidence": f"measured layout rows are {len(measured_layout)} total: {len(bare_measured)} bare and {len(tailed_measured)} tailed",
            "limit": "bare controls were visually scored but not quantified with comparable line-width/tail-space metrics, so this remains the next recut target",
        },
    ]


def write_doc(path: Path, summary: dict[str, Any], decisions: list[dict[str, str]], feature_rows: list[dict[str, Any]], numeric_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# 032-002-861 / 220-032 Register-Length Kill Test",
        "",
        "Date: 2026-05-29",
        "",
        "## Question",
        "",
        "Does broad register, fine icon label, total line length, prefix length, or measured terminal space explain the `220-032` post-`861` split before we treat it as a grammar object?",
        "",
        "## Packet",
        "",
        f"- Rows tested: `{summary['rows']}`",
        f"- Source-ready rows: `{summary['source_ready_rows']}`",
        f"- Outcomes: `{summary['outcome_distribution']}`",
        f"- Source-ready outcomes: `{summary['source_ready_outcome_distribution']}`",
        "",
        "## Decisions",
        "",
    ]
    for row in decisions:
        lines.append(f"- `{row['test']}`: `{row['decision']}`. {row['evidence']} Limit: {row['limit']}.")

    lines.extend(["", "## Feature Read", ""])
    for row in feature_rows:
        lines.append(
            f"- `{row['feature']}`: bare `{row['bare_closure']}`, `603` `{row['simple_tail_603']}`, `255-416` `{row['compound_tail_255_416']}`."
        )

    lines.extend(["", "## Numeric Read", ""])
    for row in numeric_rows:
        if not row.get("testable"):
            lines.append(f"- `{row['field']}`: not testable.")
            continue
        lines.append(
            f"- `{row['field']}`: bare `{row['bare_values']}`, tailed `{row['tailed_values']}`, range overlap `{row['range_overlap']}`, exact overlap `{row['exact_value_overlap']}`."
        )

    lines.extend(
        [
            "",
            "## Result",
            "",
            "The `220-032` split survives broad-register and total-length attacks in the current evidence layer: Mohenjo seal-square rows can be bare, simple-tailed, or compound-tailed, and total text length is not a clean selector.",
            "",
            "The kill test is not fully closed. Fine icon labels are singletons, and comparable terminal-space metrics do not yet exist for the bare controls. The next recut should quantify empty terminal margin and line occupancy for `H-444/M-723/M-1044` the same way `M-91/M-240` were quantified.",
            "",
            "Current status: `220032_split_survives_broad_register_and_length_attacks_terminal_space_unclosed`.",
            "",
            "Accepted sign values, phonetics, language identity, translations, exact source-token boundaries, and sign meanings remain 0/unaccepted.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = [row for row in read_csv(INPUT_ROWS) if row.get("prefix_last2") == "220 032"]
    if not rows:
        raise SystemExit("no prefix_last2=220 032 rows")

    score_by_blind = {row["blind_id"]: row for row in read_csv(SCORES)}
    key_by_cisi = {row["cisi"]: row for row in read_csv(BLIND_KEY)}

    out_rows: list[dict[str, Any]] = []
    for row in rows:
        key = key_by_cisi.get(row["cisi"], {})
        score = score_by_blind.get(key.get("blind_id", ""), {})
        out_rows.append(
            {
                "cisi": row["cisi"],
                "tail": row["tail"],
                "outcome": outcome(row),
                "source_ready": "1" if source_ready(row) else "0",
                "site": row["site"],
                "type": row["type"],
                "symbol": row["symbol"],
                "shape": row["shape"],
                "type_shape": f"{row['type']}|{row['shape']}",
                "site_type_shape": f"{row['site']}|{row['type']}|{row['shape']}",
                "text_length": as_int(row.get("text_length", "")),
                "prefix_len": as_int(row.get("prefix_len", "")),
                "line_width_px": row.get("line_width_px", ""),
                "pre_tail_width_px": row.get("pre_tail_width_px", ""),
                "tail_width_px": row.get("tail_width_px", ""),
                "tail_start_share_of_line": row.get("tail_start_share_of_line", ""),
                "tail_width_share_of_line": row.get("tail_width_share_of_line", ""),
                "visual_score": score.get("closure_or_tail_score", ""),
                "visual_confidence": score.get("confidence", ""),
                "text": row["text"],
            }
        )

    source_rows = [row for row in out_rows if row["source_ready"] == "1"]
    feature_rows = [
        summarize_feature(source_rows, "type_shape"),
        summarize_feature(source_rows, "site"),
        summarize_feature(source_rows, "symbol"),
        summarize_feature(source_rows, "site_type_shape"),
    ]

    numeric_rows = [
        {**numeric_overlap(out_rows, "text_length"), "field": "text_length_all_rows"},
        {**numeric_overlap(source_rows, "text_length"), "field": "text_length_source_ready"},
        {**numeric_overlap(out_rows, "prefix_len"), "field": "prefix_len_all_rows"},
        {**numeric_overlap(source_rows, "prefix_len"), "field": "prefix_len_source_ready"},
    ]
    decisions = decision_rows(out_rows, feature_rows, numeric_rows)
    summary = {
        "date": "2026-05-29",
        "rows": len(out_rows),
        "source_ready_rows": len(source_rows),
        "outcome_distribution": counter_string(Counter(row["outcome"] for row in out_rows)),
        "source_ready_outcome_distribution": counter_string(Counter(row["outcome"] for row in source_rows)),
        "status": "220032_split_survives_broad_register_and_length_attacks_terminal_space_unclosed",
        "decisions": decisions,
    }

    write_csv(REPORTS / f"{OUT_PREFIX}_rows.csv", out_rows)
    write_csv(REPORTS / f"{OUT_PREFIX}_feature_tests.csv", feature_rows)
    write_csv(REPORTS / f"{OUT_PREFIX}_numeric_tests.csv", numeric_rows)
    write_csv(REPORTS / f"{OUT_PREFIX}_decisions.csv", decisions)
    (REPORTS / f"{OUT_PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_doc(DOCS / f"{OUT_PREFIX}.md", summary, decisions, feature_rows, numeric_rows)
    print(json.dumps({"built": OUT_PREFIX, **summary}, indent=2))


if __name__ == "__main__":
    main()
