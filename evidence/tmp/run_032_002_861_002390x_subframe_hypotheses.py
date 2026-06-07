from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
DOCS = ROOT / "docs"

INPUT = REPORTS / "campaign_032_002_861_002390125_branch_source_route_rows.csv"
SLUG = "campaign_032_002_861_002390x_subframe_hypotheses"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in rows:
            w.writerow({field: row.get(field, "") for field in fields})


def first_tail_sign(tail: str) -> str:
    if not tail or tail == "<END>":
        return "<END>"
    return tail.split()[0]


def tail_prefix(tail: str, n: int = 2) -> str:
    if not tail or tail == "<END>":
        return "<END>"
    parts = tail.split()
    return " ".join(parts[:n])


def source_class(tier: str) -> str:
    if tier == "source_visible_order_window_candidate":
        return "source_visible_control"
    if tier == "public_cisi_plate_context_crop_not_token_boxed":
        return "source_context_needs_token_box"
    if tier == "public_plate_route_candidate_not_panel_bound":
        return "public_route_needs_panel_binding"
    if tier == "mayig_overlap_only":
        return "mayig_only"
    if tier == "negative_control_index_hint":
        return "source_hint_needs_route"
    if tier == "unresolved_non_cisi_object":
        return "object_unresolved"
    return "unrouted"


def annotate(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in rows:
        tail = row["tail_after_next"]
        next_after = row["next_after_390"]
        prev = row["prev_before_002"]
        prefix2 = tail_prefix(tail, 2)
        out.append(
            {
                **row,
                "source_class": source_class(row["source_tier"]),
                "first_tail_after_next": first_tail_sign(tail),
                "subframe_002390x": f"002-390-{next_after}",
                "prev_to_next_frame": f"{prev}->002-390->{next_after}",
                "next_tail_frame": f"{next_after}->{tail}",
                "next_tail_prefix2_frame": f"{next_after}->{prefix2}",
                "is_terminal_after_next": tail == "<END>",
                "is_125_632032_lane": next_after == "125" and tail.startswith("632 032"),
                "is_prev235_125_lane": prev == "235" and next_after == "125",
            }
        )
    return out


def grouped(rows: list[dict[str, object]], key: str) -> list[dict[str, object]]:
    buckets: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        buckets[str(row[key])].append(row)
    out: list[dict[str, object]] = []
    for value, items in sorted(buckets.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        nexts = Counter(str(r["next_after_390"]) for r in items)
        tails = Counter(str(r["tail_after_next"]) for r in items)
        source = Counter(str(r["source_class"]) for r in items)
        sites = Counter(str(r["site"]) for r in items)
        out.append(
            {
                key: value,
                "rows": len(items),
                "next_distribution": ";".join(f"{k}:{v}" for k, v in sorted(nexts.items())),
                "tail_distribution": ";".join(f"{k}:{v}" for k, v in sorted(tails.items())),
                "source_classes": ";".join(f"{k}:{v}" for k, v in sorted(source.items())),
                "sites": ";".join(f"{k}:{v}" for k, v in sorted(sites.items())),
                "cisis": ";".join(str(r["cisi"]) for r in items),
                "decision": group_decision(key, value, items),
            }
        )
    return out


def group_decision(key: str, value: str, items: list[dict[str, object]]) -> str:
    if key == "prev_before_002" and value == "235" and len(items) == 2:
        return "live_prev_conditioned_125_lane_source_weak"
    if key == "next_tail_prefix2_frame" and value == "125->632 032" and len(items) == 2:
        return "live_125_632032_subframe_same_site_symbol_lane"
    if key == "next_after_390" and value == "125":
        return "largest_raw_next_group_but_source_weak_and_nonterminal"
    if key == "next_after_390" and value in {"095", "705"} and len(items) == 2:
        return "repeated_terminal_non125_comparator_source_needed"
    if key == "next_after_390" and value == "692":
        return "source_visible_non125_control"
    return "context_or_singleton_control"


def hypotheses(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    prev235 = [r for r in rows if r["prev_before_002"] == "235"]
    tail632032 = [r for r in rows if r["next_after_390"] == "125" and str(r["tail_after_next"]).startswith("632 032")]
    source_visible_non125 = [r for r in rows if r["next_after_390"] != "125" and r["source_class"] == "source_visible_control"]
    repeated_non125 = [r for r in grouped(rows, "next_after_390") if r["next_after_390"] in {"095", "705"}]
    return [
        {
            "rank": 1,
            "hypothesis": "prev-conditioned branch selection",
            "evidence_for": "`235->002-390->125` occurs in 2/2 local rows; both are Mohenjo-daro seals and both continue after 125.",
            "evidence_against": "both rows are source-hint/context only, and two rows can be a formula/copy-family accident.",
            "fastest_next_test": "token-box M-38 and route M-735; then search source-visible `235-002-390-X` near-misses and non-125 controls.",
            "current_status": "alive_source_weak",
            "rows": len(prev235),
            "cisis": ";".join(str(r["cisi"]) for r in prev235),
        },
        {
            "rank": 2,
            "hypothesis": "`125-632-032` is a subframe after `002-390`",
            "evidence_for": "M-38 and M-119 share `002-390-125-632-032`; both are Mohenjo-daro square `SEAL:S` Bull1/SAN rows.",
            "evidence_against": "M-119 is Mayig-only here, M-38 is only a context crop, and M-119 has extra `900-563` after the shared material.",
            "fastest_next_test": "route M-119 and token-box M-38; compare against all `632-032` occurrences outside `002-390-125`.",
            "current_status": "alive_but_source_gated",
            "rows": len(tail632032),
            "cisis": ";".join(str(r["cisi"]) for r in tail632032),
        },
        {
            "rank": 3,
            "hypothesis": "`125` is just one member of a broader `002-390-X` branch-choice slot",
            "evidence_for": "`002-390-X` has 15 rows and 10 next signs; `125` is largest at 4 but not dominant.",
            "evidence_against": "current source visibility is uneven; source-visible M-70 proves non-125 continuation, but most comparators remain source-hint only.",
            "fastest_next_test": "source-normalize repeated `095` and `705` comparators before giving any special status to `125`.",
            "current_status": "best_current_null_sensitive_model",
            "rows": len(rows),
            "cisis": ";".join(str(r["cisi"]) for r in rows),
        },
        {
            "rank": 4,
            "hypothesis": "source/register mirage",
            "evidence_for": "only M-70 is source-visible at order-window quality; 125 rows are source-weak, and Sktd-1 is not panel-bound.",
            "evidence_against": "the internal `235` and `632-032` clustering gives a real linguistic target if source routes survive.",
            "fastest_next_test": "kill or promote by source-normalizing M-38/M-735/M-119 against M-70, `095`, and `705`.",
            "current_status": "active_adversary",
            "rows": len(source_visible_non125) + len(repeated_non125),
            "cisis": ";".join(str(r["cisi"]) for r in source_visible_non125),
        },
    ]


def write_doc(summary: dict[str, object], hypo_rows: list[dict[str, object]]) -> Path:
    doc = DOCS / f"{SLUG}.md"
    ranked = "\n".join(
        f"{row['rank']}. `{row['hypothesis']}`: {row['current_status']}. For: {row['evidence_for']} Against: {row['evidence_against']} Next: {row['fastest_next_test']}"
        for row in hypo_rows
    )
    doc.write_text(
        f"""# 032-002-861 / 002-390-X Subframe Hypotheses

Date: 2026-05-29

## Question

Inside the `002-390-X` branch, is `125` behaving like a structural continuation choice, a subframe opener, or a source/register mirage?

## Result

No value, phonetics, language identity, or translation is promoted.

The new linguistic object is not `125` alone. It is the internal contrast among `002-390-X` rows, especially two subframes:

- `235->002-390->125`: `2/2` local rows with previous sign `235` choose `125`.
- `002-390-125-632-032`: `2` rows share the `125-632-032` continuation, both Mohenjo-daro square `SEAL:S` Bull1/SAN rows.

These are real structural hypotheses, but both are source-weak. The source-visible non-`125` control remains `M-70 +226-032-002-390-692+`, so `125` cannot be treated as necessary after `002-390`.

## Ranked Hypotheses

{ranked}

## Decision

Promote `002-390-X` subframe analysis as the next batch. Do not promote `125` as a suffix, value, or translation unit.

Next source-normalized campaign: token-box `M-38`; route `M-119` and `M-735`; panel-bind Sktd-1; source-route repeated non-`125` comparators `095` and `705`; keep `M-70` as the source-visible non-`125` control.

Accepted values, phonetics, language identity, translations, exact source-token boundaries, and sign meanings remain `0`.
""",
        encoding="utf-8",
    )
    return doc


def main() -> None:
    rows = annotate(read_csv(INPUT))
    by_prev = grouped(rows, "prev_before_002")
    by_next = grouped(rows, "next_after_390")
    by_next_tail = grouped(rows, "next_tail_frame")
    by_next_tail_prefix = grouped(rows, "next_tail_prefix2_frame")
    hypo_rows = hypotheses(rows)
    summary = {
        "date": "2026-05-29",
        "question": "Rank structural hypotheses inside 002-390-X without accepting values.",
        "rows": len(rows),
        "next_after_390_values": len({r["next_after_390"] for r in rows}),
        "prev235_rows": len([r for r in rows if r["is_prev235_125_lane"]]),
        "tail_125_632032_rows": len([r for r in rows if r["is_125_632032_lane"]]),
        "source_visible_non125_control": "M-70 +226-032-002-390-692+",
        "decision": "promote_002390x_subframe_hypotheses_source_normalize_next_no_values",
        "accepted_values_translations": 0,
    }
    doc = write_doc(summary, hypo_rows)
    write_csv(
        REPORTS / f"{SLUG}_rows.csv",
        rows,
        [
            "cisi",
            "id",
            "site",
            "type",
            "symbol",
            "text",
            "text_len",
            "prev_before_002",
            "next_after_390",
            "tail_after_next",
            "source_tier",
            "source_class",
            "first_tail_after_next",
            "subframe_002390x",
            "prev_to_next_frame",
            "next_tail_frame",
            "next_tail_prefix2_frame",
            "is_terminal_after_next",
            "is_125_632032_lane",
            "is_prev235_125_lane",
        ],
    )
    write_csv(
        REPORTS / f"{SLUG}_by_prev_before_002.csv",
        by_prev,
        ["prev_before_002", "rows", "next_distribution", "tail_distribution", "source_classes", "sites", "cisis", "decision"],
    )
    write_csv(
        REPORTS / f"{SLUG}_by_next_after_390.csv",
        by_next,
        ["next_after_390", "rows", "next_distribution", "tail_distribution", "source_classes", "sites", "cisis", "decision"],
    )
    write_csv(
        REPORTS / f"{SLUG}_by_next_tail_frame.csv",
        by_next_tail,
        ["next_tail_frame", "rows", "next_distribution", "tail_distribution", "source_classes", "sites", "cisis", "decision"],
    )
    write_csv(
        REPORTS / f"{SLUG}_by_next_tail_prefix2_frame.csv",
        by_next_tail_prefix,
        ["next_tail_prefix2_frame", "rows", "next_distribution", "tail_distribution", "source_classes", "sites", "cisis", "decision"],
    )
    write_csv(
        REPORTS / f"{SLUG}_hypotheses.csv",
        hypo_rows,
        ["rank", "hypothesis", "evidence_for", "evidence_against", "fastest_next_test", "current_status", "rows", "cisis"],
    )
    (REPORTS / f"{SLUG}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps({"doc": str(doc), "summary": summary}, indent=2))


if __name__ == "__main__":
    main()
