"""Search the whole post-002-861 field for minimal contrasts worth chasing.

A minimal contrast is two inscriptions that share the same context (same exact
prefix, same last-two prefix signs, or same register) but choose different
tails after 861 — the closest thing this corpus offers to a minimal pair. We
read the 144 source-normalized tail predictor rows, find every context value
where at least two different tails appear, and rank those contrasts by whether
they are source-live (checked images on both sides). Each tail then gets a
profile and a decision class — background closure, live simple-tail cluster,
conditional fixed unit, singleton watch, or source-acquisition chore. Outputs:
tail-profile, mixed-context, and decision CSVs, a JSON summary, and a Markdown
report in docs/. All sign values and translations stay at 0/unaccepted.
"""

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
OUT_PREFIX = "campaign_032_002_861_post861_minimal_contrast_search"

FOCUS_TAILS = {"603", "533 717", "255 416", "360 520 919 140"}
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


def counter_string(counter: Counter[str], topn: int = 20) -> str:
    return ";".join(f"{key}:{value}" for key, value in counter.most_common(topn))


def examples(rows: list[dict[str, str]], limit: int = 8) -> str:
    return ";".join(f"{row['cisi']} {row['text']}" for row in rows[:limit])


def source_ready(row: dict[str, str]) -> bool:
    return row.get("source_status", "") not in SOURCE_PENDING or bool(row.get("display_image", ""))


def family_cell(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        row.get("tail", ""),
        row.get("prefix", ""),
        row.get("register_key", ""),
        row.get("template_key", ""),
    )


def unique_count(rows: list[dict[str, str]], key: str) -> int:
    return len({row.get(key, "") for row in rows})


def tail_distribution(rows: list[dict[str, str]]) -> str:
    return counter_string(Counter(row["tail"] for row in rows), 30)


def source_distribution(rows: list[dict[str, str]]) -> str:
    return counter_string(Counter(row.get("source_status", "") for row in rows), 12)


def group_by(rows: list[dict[str, str]], key: str) -> dict[str, list[dict[str, str]]]:
    out: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        out[row.get(key, "")].append(row)
    return out


def contrast_rows(rows: list[dict[str, str]], feature: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for value, group in group_by(rows, feature).items():
        tails = {row["tail"] for row in group}
        if len(tails) < 2:
            continue
        non_bare = [row for row in group if row["tail"] != "<END>"]
        source_rows = [row for row in group if source_ready(row)]
        source_non_bare = [row for row in non_bare if source_ready(row)]
        focus_hits = sorted({row["tail"] for row in group if row["tail"] in FOCUS_TAILS})
        exact_source_live = len(source_rows) > 0 and len({row["tail"] for row in source_rows}) > 1
        out.append(
            {
                "feature": feature,
                "value": value if value else "<EMPTY>",
                "rows": len(group),
                "non_bare_rows": len(non_bare),
                "family_cells": len({family_cell(row) for row in group}),
                "tail_types": len(tails),
                "tail_distribution": tail_distribution(group),
                "source_ready_rows": len(source_rows),
                "source_ready_tail_distribution": tail_distribution(source_rows) if source_rows else "",
                "source_ready_non_bare_rows": len(source_non_bare),
                "focus_tails_present": ";".join(focus_hits),
                "source_live_split": exact_source_live,
                "register_distribution": counter_string(Counter(row.get("register_key", "") for row in group), 8),
                "site_distribution": counter_string(Counter(row.get("site", "") for row in group), 8),
                "examples": examples(group, 12),
            }
        )
    out.sort(
        key=lambda row: (
            int(not row["source_live_split"]),
            -int(row["source_ready_rows"]),
            -int(row["tail_types"]),
            -int(row["rows"]),
            str(row["feature"]),
            str(row["value"]),
        )
    )
    return out


def all_contrasts(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    contrasts: list[dict[str, Any]] = []
    for feature in ["prefix", "prefix_last3", "prefix_last2", "prefix_last1", "register_key", "broad_register_key"]:
        for row in contrast_rows(rows, feature):
            contrasts.append(row)
    contrasts.sort(
        key=lambda row: (
            int(not row["source_live_split"]),
            -int(row["source_ready_rows"]),
            -int(row["tail_types"]),
            -int(row["family_cells"]),
            -int(row["rows"]),
        )
    )
    return contrasts


def contrast_membership(contrasts: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for contrast in contrasts:
        tails = Counter(part.split(":")[0] for part in str(contrast["tail_distribution"]).split(";") if part)
        for tail in tails:
            if contrast["feature"] == "prefix":
                out[tail]["exact_prefix_contrasts"] += 1
            elif contrast["feature"] in {"prefix_last3", "prefix_last2", "prefix_last1"}:
                out[tail]["preframe_contrasts"] += 1
            elif contrast["feature"] in {"register_key", "broad_register_key"}:
                out[tail]["register_contrasts"] += 1
            if contrast["source_live_split"]:
                out[tail]["source_live_contrasts"] += 1
    return out


def classify_tail(tail: str, rows: list[dict[str, str]], memberships: dict[str, dict[str, int]]) -> tuple[str, str, int]:
    source_rows = [row for row in rows if source_ready(row)]
    cells = len({family_cell(row) for row in rows})
    exact = memberships[tail]["exact_prefix_contrasts"]
    preframe = memberships[tail]["preframe_contrasts"]
    register = memberships[tail]["register_contrasts"]
    live = memberships[tail]["source_live_contrasts"]
    score = len(rows) + 2 * cells + 3 * len(source_rows) + 2 * live + exact + preframe + register

    if tail == "<END>":
        return "background_closure", "dominant closure state; not a sign value", score
    if tail == "603":
        return (
            "top_live_simple_tail_cluster",
            "three source-ready post-861 rows, participates in the source-ready 220-032 split, and is not explained by one exact prefix",
            score,
        )
    if tail == "255 416":
        return (
            "source_ready_minimal_contrast_singleton",
            "one source-ready row in the 220-032 contrast cluster; important because it blocks a binary bare-vs-603 reading",
            score,
        )
    if tail == "533 717":
        return (
            "conditional_fixed_final_unit",
            "two source-ready rows and a fixed pair, but no exact-prefix or same-last2 contrast; lives mainly in a register split",
            score,
        )
    if tail == "360 520 919 140":
        return (
            "source_ready_long_continuation_adversary",
            "one source-ready same-register long continuation that prevents treating no-icon cuboid-convex SEAL:R as the 533-717 function",
            score,
        )
    if len(rows) >= 2 and not source_rows:
        return (
            "source_acquisition_cluster_not_linguistic_yet",
            "count-supported but source-pending; do not promote until at least one source image and family-cell check exist",
            score,
        )
    if len(rows) == 1 and source_rows:
        return "source_ready_singleton_watch", "source-ready singleton; usable as an adversary or control, not a value", score
    return "metadata_singleton_watch", "single metadata row; source-route before interpretation", score


def tail_profiles(rows: list[dict[str, str]], contrasts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    memberships = contrast_membership(contrasts)
    out: list[dict[str, Any]] = []
    for tail, group in group_by(rows, "tail").items():
        source_rows = [row for row in group if source_ready(row)]
        decision, reason, score = classify_tail(tail, group, memberships)
        out.append(
            {
                "tail": tail,
                "decision_class": decision,
                "research_reason": reason,
                "rank_score": score,
                "rows": len(group),
                "family_cells": len({family_cell(row) for row in group}),
                "source_ready_rows": len(source_rows),
                "source_ready_examples": examples(source_rows, 8),
                "prefix_last2_distribution": counter_string(Counter(row.get("prefix_last2", "") for row in group), 12),
                "register_distribution": counter_string(Counter(row.get("register_key", "") for row in group), 10),
                "site_distribution": counter_string(Counter(row.get("site", "") for row in group), 10),
                "source_distribution": source_distribution(group),
                "exact_prefix_contrasts": memberships[tail]["exact_prefix_contrasts"],
                "preframe_contrasts": memberships[tail]["preframe_contrasts"],
                "register_contrasts": memberships[tail]["register_contrasts"],
                "source_live_contrasts": memberships[tail]["source_live_contrasts"],
                "examples": examples(group, 12),
            }
        )
    out.sort(
        key=lambda row: (
            row["decision_class"] == "background_closure",
            -int(row["source_ready_rows"]),
            -int(row["rank_score"]),
            -int(row["family_cells"]),
            str(row["tail"]),
        )
    )
    return out


def live_decision_rows(rows: list[dict[str, str]], profiles: list[dict[str, Any]], contrasts: list[dict[str, Any]]) -> list[dict[str, str]]:
    by_tail = {row["tail"]: row for row in profiles}
    top_contrast = next((row for row in contrasts if row["feature"] == "prefix_last2" and row["value"] == "220 032"), None)
    register_contrast = next(
        (row for row in contrasts if row["feature"] == "broad_register_key" and row["value"] == "Mohenjo-daro|SEAL:R|None"),
        None,
    )
    exact_prefix_390 = next((row for row in contrasts if row["feature"] == "prefix" and row["value"] == "390 004"), None)
    exact_prefix_empty = next((row for row in contrasts if row["feature"] == "prefix" and row["value"] == "<EMPTY>"), None)

    return [
        {
            "object": "post-861 tail-choice system",
            "decision": "alive_as_positional_linguistic_question_not_translation",
            "evidence": "144 rows after 002-861 split into dominant closure plus simple tails, fixed pair, long continuation, and source-pending artifact classes",
            "next_action": "model typed continuations after 861 as closure/simple/fixed-pair/long, then test against matched source-visible contexts",
        },
        {
            "object": "prefix_last2=220 032",
            "decision": "best_source_visible_minimal_contrast_cluster",
            "evidence": top_contrast["tail_distribution"] if top_contrast else "missing",
            "next_action": "run source-visible side-by-side epigraphic packet for M-240/603, M-91/255-416, and bare 220-032 controls; do not infer values",
        },
        {
            "object": "603",
            "decision": by_tail.get("603", {}).get("decision_class", "missing"),
            "evidence": by_tail.get("603", {}).get("research_reason", "missing"),
            "next_action": "treat as recurrent post-861 simple-tail class; compare internal tail ecology before reopening the Harappa bridge",
        },
        {
            "object": "255 416",
            "decision": by_tail.get("255 416", {}).get("decision_class", "missing"),
            "evidence": by_tail.get("255 416", {}).get("research_reason", "missing"),
            "next_action": "use as third-arm contrast in 220-032; source-route more 255/416 contexts before assigning function",
        },
        {
            "object": "533 717",
            "decision": by_tail.get("533 717", {}).get("decision_class", "missing"),
            "evidence": by_tail.get("533 717", {}).get("research_reason", "missing"),
            "next_action": "keep as conditional fixed final-unit comparator, not the center of the next campaign",
        },
        {
            "object": "Mohenjo no-icon SEAL:R register",
            "decision": "register_does_not_determine_tail",
            "evidence": register_contrast["tail_distribution"] if register_contrast else "missing",
            "next_action": "use register split as an adversarial control against all 533-717 functional claims",
        },
        {
            "object": "exact_prefix=390 004",
            "decision": "high_value_source_acquisition_exact_prefix_split",
            "evidence": exact_prefix_390["tail_distribution"] if exact_prefix_390 else "missing",
            "next_action": "source-route H-55 and the bare 390-004 control if this branch becomes the next acquisition target",
        },
        {
            "object": "empty-prefix 416/698/096 cluster",
            "decision": "repeated_but_not_interpretable_before_source_images",
            "evidence": exact_prefix_empty["tail_distribution"] if exact_prefix_empty else "missing",
            "next_action": "quarantine as object/type/formula acquisition, not grammar, until source panels show comparable signbands",
        },
    ]


def write_doc(path: Path, summary: dict[str, Any], decisions: list[dict[str, str]], profiles: list[dict[str, Any]], contrasts: list[dict[str, Any]]) -> None:
    lines = [
        "# 032-002-861 Post-861 Minimal-Contrast Search",
        "",
        "Date: 2026-05-29",
        "",
        "## Question",
        "",
        "Across the whole 144-row post-`002-861` field, which tails gain real decipherment pressure from repetition, minimal contrast, and source-visible context, and which are just metadata/source-acquisition chores?",
        "",
        "## Corpus Slice",
        "",
        f"- Input rows: `{summary['rows']}` from `{INPUT_ROWS}`",
        f"- Non-bare tail rows: `{summary['non_bare_rows']}`",
        f"- Tail distribution: `{summary['tail_distribution']}`",
        f"- Source-ready rows: `{summary['source_ready_rows']}`",
        f"- Exact-prefix mixed groups: `{summary['exact_prefix_mixed_groups']}`",
        f"- Source-live mixed groups: `{summary['source_live_mixed_groups']}`",
        "",
        "## Decisions",
        "",
    ]
    for row in decisions:
        lines.append(f"- `{row['object']}`: `{row['decision']}`. Evidence: {row['evidence']}. Next: {row['next_action']}.")

    lines.extend(["", "## Ranked Tail Objects", ""])
    for row in profiles:
        if row["tail"] == "<END>":
            continue
        lines.append(
            f"- `{row['tail']}`: `{row['decision_class']}`; rows `{row['rows']}`, family cells `{row['family_cells']}`, source-ready `{row['source_ready_rows']}`. {row['research_reason']}"
        )

    lines.extend(["", "## Strongest Mixed Contexts", ""])
    for row in contrasts[:12]:
        live = "source-live" if row["source_live_split"] else "metadata/source-pending"
        lines.append(
            f"- `{row['feature']}={row['value']}` ({live}): rows `{row['rows']}`, tails `{row['tail_distribution']}`, source-ready `{row['source_ready_rows']}`."
        )

    lines.extend(
        [
            "",
            "## Linguistic Read",
            "",
            "- The research object is now a typed tail-choice system after `861`: closure, simple terminal sign, fixed terminal pair, singleton compound tail, and long continuation.",
            "- The strongest live contrast is not another `533-717` micro-audit. It is the `220 032` preframe split: bare closure versus `603` versus `255-416`, with source-ready witnesses already in hand.",
            "- `603` is the best current source-visible simple-tail class on the Mohenjo post-`861` side, but its Harappa bridge remains parked; keep those questions separate.",
            "- `533-717` remains useful as a conditional fixed final-unit comparator, but it has no exact-prefix or same-last2 minimal contrast and should not monopolize the next campaign.",
            "- `416` and `698` are count-supported but source-pending empty-prefix clusters; they are acquisition targets, not readings.",
            "",
            "Accepted sign values, phonetics, language identity, translations, exact `861|tail` source-token boundaries, and sign meanings remain 0/unaccepted.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = read_csv(INPUT_ROWS)
    if not rows:
        raise SystemExit(f"no rows read from {INPUT_ROWS}")

    for row in rows:
        row["source_ready"] = "1" if source_ready(row) else "0"
        row["family_cell"] = "|".join(family_cell(row))

    contrasts = all_contrasts(rows)
    profiles = tail_profiles(rows, contrasts)
    decisions = live_decision_rows(rows, profiles, contrasts)

    exact_prefix_mixed = [row for row in contrasts if row["feature"] == "prefix"]
    source_live = [row for row in contrasts if row["source_live_split"]]
    non_bare = [row for row in rows if row["tail"] != "<END>"]
    source_ready_rows = [row for row in rows if source_ready(row)]

    summary = {
        "date": "2026-05-29",
        "rows": len(rows),
        "non_bare_rows": len(non_bare),
        "source_ready_rows": len(source_ready_rows),
        "tail_distribution": tail_distribution(rows),
        "exact_prefix_mixed_groups": len(exact_prefix_mixed),
        "source_live_mixed_groups": len(source_live),
        "top_source_live_contrasts": source_live[:10],
        "top_profiles": profiles[:12],
        "decisions": decisions,
    }

    write_csv(REPORTS / f"{OUT_PREFIX}_tail_profiles.csv", profiles)
    write_csv(REPORTS / f"{OUT_PREFIX}_mixed_contexts.csv", contrasts)
    write_csv(REPORTS / f"{OUT_PREFIX}_decisions.csv", decisions)
    (REPORTS / f"{OUT_PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_doc(DOCS / f"{OUT_PREFIX}.md", summary, decisions, profiles, contrasts)
    print(json.dumps({"status": "post861_minimal_contrast_search_built", **summary}, indent=2))


if __name__ == "__main__":
    main()
