"""Scan for any real bridge cluster between X-before-240 and post-861, with nulls.

The earlier work fixated on 603. This scan asks the fair version of the
question: does any non-background sign form a family-cell bridge between the
two ecologies? It collapses post-002-861 tail rows into family cells the same
way the X-side audit did, scores every intersecting sign (rewarding locked
multi-cell bridges, penalizing single-cell intersections), and applies a
shape gate that demands at least two independent family cells on both sides.
Because the candidate was found by searching, the decision adversary is a
max-scan null: 20,000 seeded label shuffles within each side, plus a second
identity-remap null that breaks the cross-side sign-identity match. The
recorded decision: no bridge cluster passes the shape gate — 603 fails the
minimum recurrence rule, and the campaign should pivot away from 603-only
work. Writes tail-cell, candidate, and two null-sample CSVs, a JSON summary,
and a Markdown doc in docs/.
"""

from __future__ import annotations

import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
DOCS = ROOT / "docs"

X240_CELLS = REPORTS / "campaign_032_002_861_x240_family_cell_bridge_audit_cells.csv"
POST861_ROWS = REPORTS / "campaign_032_002_861_x240_bridge_post861_rows.csv"
OUT_PREFIX = "campaign_032_002_861_x240_post861_bridge_cluster_scan"

ITERATIONS = 20000
SEED = 603240863
BACKGROUND_SIGNS = {"000", "<END>"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def tokens(text: str) -> list[str]:
    return [part for part in text.strip("+").split("-") if part]


def tail_template(row: dict[str, str]) -> str:
    parts = tokens(row["text"])
    for idx in range(len(parts) - 1):
        if parts[idx] == "002" and parts[idx + 1] == "861":
            templated = parts[:]
            if idx + 2 < len(templated):
                templated[idx + 2] = "TAIL_X"
            return "+" + "-".join(templated) + "+"
    return row.get("formula_key") or row["text"]


def collapse_post861_tail_cells(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        sign = row["tail_initial"]
        if sign == "<END>":
            continue
        key = (
            sign,
            row["prefix_last2_before_002_861"],
            row["tail_after_002_861"],
            row["register_key"],
            tail_template(row),
        )
        groups[key].append(row)

    cells: list[dict[str, object]] = []
    for (sign, preframe, tail, register, template), group in sorted(
        groups.items(), key=lambda item: (item[0][0], item[0][2], item[0][4])
    ):
        cells.append(
            {
                "tail_initial": sign,
                "prefix_last2_before_002_861": preframe,
                "tail_after_002_861": tail,
                "register_key": register,
                "template_key": template,
                "raw_rows": len(group),
                "source_objects": ";".join(sorted({row["cisi"] for row in group})),
                "source_object_count": len({row["cisi"] for row in group}),
                "examples": ";".join(f"{row['cisi']} {row['text']}" for row in group[:8]),
            }
        )
    return cells


def group_by(rows: list[dict[str, object]], key: str) -> dict[str, list[dict[str, object]]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row[key])].append(row)
    return grouped


def score_profile(
    sign: str,
    x_group: list[dict[str, object]],
    tail_group: list[dict[str, object]],
) -> dict[str, object] | None:
    if sign in BACKGROUND_SIGNS or not x_group or not tail_group:
        return None

    after_counts = Counter(str(cell["after_240_first3"]) for cell in x_group)
    dominant_after, dominant_count = after_counts.most_common(1)[0]
    x_templates = {str(cell["template_key"]) for cell in x_group}
    tail_templates = {str(cell["template_key"]) for cell in tail_group}
    registers = {str(cell["register_key"]) for cell in x_group + tail_group}
    sites = {str(cell["register_key"]).split("|", 1)[0] for cell in x_group + tail_group}

    x_family_cells = len(x_group)
    tail_family_cells = len(tail_group)
    dominant_ratio = dominant_count / x_family_cells
    locked_multi_cell_bridge_count = (
        dominant_count
        if x_family_cells >= 2 and tail_family_cells >= 2 and dominant_ratio >= 0.8
        else 0
    )
    independent_subframe_count = len(after_counts)
    independent_family_count = min(x_family_cells, tail_family_cells)
    single_cell_only_indicator = int(x_family_cells < 2 or tail_family_cells < 2)
    tail_only_or_tail_rescued_indicator = int(x_family_cells < 2)
    score = (
        10 * locked_multi_cell_bridge_count
        + 3 * independent_subframe_count
        + 2 * independent_family_count
        - 8 * single_cell_only_indicator
        - 5 * tail_only_or_tail_rescued_indicator
    )
    passes_shape_gate = (
        x_family_cells >= 2
        and tail_family_cells >= 2
        and len(x_templates | tail_templates) >= 2
        and dominant_ratio >= 0.8
        and len(registers) >= 2
    )

    return {
        "sign": sign,
        "score": score,
        "x_family_cells": x_family_cells,
        "post861_tail_family_cells": tail_family_cells,
        "dominant_after240": dominant_after,
        "dominant_after240_cells": dominant_count,
        "dominant_after240_ratio": f"{dominant_ratio:.6f}",
        "distinct_after240_subframes": independent_subframe_count,
        "x_template_count": len(x_templates),
        "post861_template_count": len(tail_templates),
        "register_count": len(registers),
        "site_count": len(sites),
        "locked_multi_cell_bridge_count": locked_multi_cell_bridge_count,
        "independent_family_count": independent_family_count,
        "single_cell_only_indicator": single_cell_only_indicator,
        "tail_only_or_tail_rescued_indicator": tail_only_or_tail_rescued_indicator,
        "passes_shape_gate": passes_shape_gate,
        "x_after240_cell_counts": ";".join(f"{key}:{value}" for key, value in after_counts.most_common()),
        "x_examples": ";".join(str(cell["examples"]) for cell in x_group[:4]),
        "post861_examples": ";".join(str(cell["examples"]) for cell in tail_group[:4]),
    }


def score_all(
    x_cells: list[dict[str, object]],
    tail_cells: list[dict[str, object]],
) -> list[dict[str, object]]:
    x_by_sign = group_by(x_cells, "x_sign")
    tail_by_sign = group_by(tail_cells, "tail_initial")
    signs = sorted(set(x_by_sign) | set(tail_by_sign))
    profiles = []
    for sign in signs:
        profile = score_profile(sign, x_by_sign.get(sign, []), tail_by_sign.get(sign, []))
        if profile:
            profiles.append(profile)
    profiles.sort(key=lambda row: (-int(row["score"]), str(row["sign"])))
    for idx, row in enumerate(profiles, start=1):
        row["observed_rank"] = idx
    return profiles


def shuffled_cells(
    rows: list[dict[str, object]],
    sign_key: str,
    rng: random.Random,
) -> list[dict[str, object]]:
    signs = [str(row[sign_key]) for row in rows]
    rng.shuffle(signs)
    out: list[dict[str, object]] = []
    for row, sign in zip(rows, signs):
        new_row = dict(row)
        new_row[sign_key] = sign
        out.append(new_row)
    return out


def run_maxt_null(
    x_cells: list[dict[str, object]],
    tail_cells: list[dict[str, object]],
    observed_profiles: list[dict[str, object]],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    rng = random.Random(SEED)
    observed_max = max((int(row["score"]) for row in observed_profiles), default=0)
    observed_top = observed_profiles[0]["sign"] if observed_profiles else ""
    observed_any_shape_pass = any(bool(row["passes_shape_gate"]) for row in observed_profiles)

    max_ge_observed = 0
    any_shape_pass_count = 0
    samples: list[dict[str, object]] = []
    for idx in range(ITERATIONS):
        sx = shuffled_cells(x_cells, "x_sign", rng)
        st = shuffled_cells(tail_cells, "tail_initial", rng)
        profiles = score_all(sx, st)
        max_score = max((int(row["score"]) for row in profiles), default=0)
        top_sign = profiles[0]["sign"] if profiles else ""
        any_shape_pass = any(bool(row["passes_shape_gate"]) for row in profiles)
        if max_score >= observed_max:
            max_ge_observed += 1
        if any_shape_pass:
            any_shape_pass_count += 1
        if idx < 250:
            samples.append(
                {
                    "iteration": idx,
                    "max_score": max_score,
                    "top_sign": top_sign,
                    "any_shape_pass": any_shape_pass,
                }
            )

    p_max = max_ge_observed / ITERATIONS
    p_any_shape = any_shape_pass_count / ITERATIONS
    for row in observed_profiles:
        row["empirical_maxT_p_for_score"] = p_max if int(row["score"]) == observed_max else None

    summary = {
        "date": "2026-05-29",
        "seed": SEED,
        "iterations": ITERATIONS,
        "x_family_cells": len(x_cells),
        "post861_tail_family_cells": len(tail_cells),
        "observed_bridge_candidates": len(observed_profiles),
        "observed_top_sign": observed_top,
        "observed_max_score": observed_max,
        "observed_any_shape_pass": observed_any_shape_pass,
        "p_maxT": p_max,
        "p_any_shape_pass": p_any_shape,
        "decision": {
            "status": "no_family_cell_bridge_cluster_promoted_from_x240_post861_scan",
            "interpretation": [
                "At family-cell level the observed nonbackground X-before-240/post-002-861 intersection has no multi-cell bridge cluster passing the shape gate.",
                "`603` remains the visible intersection sign, but its X-before-240 side is one family cell, so it fails the minimum recurrence rule before semantics or value can be discussed.",
                "The max-scan null is the relevant decision adversary because the target was found by searching for bridge-like behavior across signs.",
                "The next decipherment move is to pivot away from 603-only work unless source acquisition creates graphic identity or a second independent 603 family cell.",
            ],
            "not_accepted": [
                "603 value",
                "any X-before-240 bridge value",
                "phonetics",
                "language identity",
                "translation",
                "accepted graphic identity",
            ],
        },
    }
    return samples, summary


def remap_tail_identities(
    tail_cells: list[dict[str, object]],
    target_signs: list[str],
    rng: random.Random,
) -> list[dict[str, object]]:
    by_tail = group_by(tail_cells, "tail_initial")
    tail_signs = sorted(by_tail)
    if len(target_signs) < len(tail_signs):
        raise ValueError("target sign universe is smaller than tail sign groups")
    mapped_targets = rng.sample(target_signs, len(tail_signs))
    mapping = dict(zip(tail_signs, mapped_targets))

    out: list[dict[str, object]] = []
    for row in tail_cells:
        new_row = dict(row)
        new_row["tail_initial"] = mapping[str(row["tail_initial"])]
        out.append(new_row)
    return out


def run_identity_remap_null(
    x_cells: list[dict[str, object]],
    tail_cells: list[dict[str, object]],
    observed_profiles: list[dict[str, object]],
) -> tuple[list[dict[str, object]], dict[str, object]]:
    rng = random.Random(SEED + 1)
    observed_max = max((int(row["score"]) for row in observed_profiles), default=0)
    x_sign_universe = sorted({str(cell["x_sign"]) for cell in x_cells if str(cell["x_sign"]) not in BACKGROUND_SIGNS})

    max_ge_observed = 0
    any_shape_pass_count = 0
    samples: list[dict[str, object]] = []
    for idx in range(ITERATIONS):
        remapped_tail_cells = remap_tail_identities(tail_cells, x_sign_universe, rng)
        profiles = score_all(x_cells, remapped_tail_cells)
        max_score = max((int(row["score"]) for row in profiles), default=0)
        top_sign = profiles[0]["sign"] if profiles else ""
        any_shape_pass = any(bool(row["passes_shape_gate"]) for row in profiles)
        if max_score >= observed_max:
            max_ge_observed += 1
        if any_shape_pass:
            any_shape_pass_count += 1
        if idx < 250:
            samples.append(
                {
                    "iteration": idx,
                    "max_score": max_score,
                    "top_sign": top_sign,
                    "any_shape_pass": any_shape_pass,
                }
            )

    return samples, {
        "p_maxT": max_ge_observed / ITERATIONS,
        "p_any_shape_pass": any_shape_pass_count / ITERATIONS,
        "target_sign_universe": len(x_sign_universe),
        "tail_identity_groups": len(set(str(cell["tail_initial"]) for cell in tail_cells)),
    }


def write_doc(path: Path, summary: dict[str, object], profiles: list[dict[str, object]]) -> None:
    decision = summary["decision"]
    assert isinstance(decision, dict)
    lines = [
        "# 032-002-861 X-Before-240 / Post-861 Bridge Cluster Scan",
        "",
        "Date: 2026-05-29",
        "",
        "## Question",
        "",
        "Does any nonbackground sign form a real family-cell bridge between the X-before-`240` ecology and post-`002-861` tail-initial ecology, after correcting for the fact that the packet was searched?",
        "",
        "## Method",
        "",
        f"- Unit: family cell.",
        f"- X-before-`240` side: `{summary['x_family_cells']}` family cells from the family-cell audit.",
        f"- Post-`002-861` side: `{summary['post861_tail_family_cells']}` nonterminal tail-initial family cells.",
        "- Post-`002-861` cells collapse by `(tail initial, pre-002-861 frame, tail string, register key, signless tail template)`.",
        "- Within-side null: shuffle X labels over X-family cells and tail-initial labels over post-`002-861` tail cells for 20,000 iterations. This preserves side-specific sign frequencies and tests context placement.",
        "- Identity-remap null: remap post-`002-861` tail sign groups onto the X-before-`240` sign universe for 20,000 iterations. This breaks the cross-side sign identity match while preserving tail group sizes.",
        "",
        "A candidate must have at least two independent family cells on both sides before it can become decipherment-bearing. Single-cell intersections are logged only.",
        "",
        "## Observed Candidates",
        "",
        "| rank | sign | score | X cells | post-861 cells | dominant after-240 | shape gate | templates X/post | examples |",
        "|---:|---|---:|---:|---:|---|---|---|---|",
    ]
    for row in profiles[:12]:
        example = str(row["x_examples"]).split(";")[0]
        lines.append(
            "| {observed_rank} | {sign} | {score} | {x_family_cells} | {post861_tail_family_cells} | {dominant_after240} ({dominant_after240_cells}/{x_family_cells}) | {passes_shape_gate} | {x_template_count}/{post861_template_count} | {example} |".format(
                example=example, **row
            )
        )

    lines.extend(
        [
            "",
            "## Max-Scan Null",
            "",
            f"- Observed top sign: `{summary['observed_top_sign']}`",
            f"- Observed max score: `{summary['observed_max_score']}`",
            f"- Within-side `P(max shuffled score >= observed max score) = {summary['within_side_p_maxT']:.6f}`",
            f"- Within-side `P(any shuffled sign passes the multi-cell shape gate) = {summary['within_side_p_any_shape_pass']:.6f}`",
            f"- Identity-remap `P(max remapped score >= observed max score) = {summary['identity_remap_p_maxT']:.6f}`",
            f"- Identity-remap `P(any remapped sign passes the multi-cell shape gate) = {summary['identity_remap_p_any_shape_pass']:.6f}`",
            "",
            "## Decision",
            "",
            f"Status: `{decision['status']}`.",
            "",
        ]
    )
    for item in decision["interpretation"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Accepted values, phonetics, language identity, translations, and graphic identity remain 0/unaccepted.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    x_cells = read_csv(X240_CELLS)
    post_rows = read_csv(POST861_ROWS)
    tail_cells = collapse_post861_tail_cells(post_rows)
    profiles = score_all(x_cells, tail_cells)
    samples, summary = run_maxt_null(x_cells, tail_cells, profiles)
    identity_samples, identity_rates = run_identity_remap_null(x_cells, tail_cells, profiles)
    summary["within_side_p_maxT"] = summary.pop("p_maxT")
    summary["within_side_p_any_shape_pass"] = summary.pop("p_any_shape_pass")
    summary["identity_remap_p_maxT"] = identity_rates["p_maxT"]
    summary["identity_remap_p_any_shape_pass"] = identity_rates["p_any_shape_pass"]
    summary["identity_remap_target_sign_universe"] = identity_rates["target_sign_universe"]
    summary["identity_remap_tail_identity_groups"] = identity_rates["tail_identity_groups"]

    write_csv(REPORTS / f"{OUT_PREFIX}_post861_tail_cells.csv", tail_cells)
    write_csv(REPORTS / f"{OUT_PREFIX}_candidates.csv", profiles)
    write_csv(REPORTS / f"{OUT_PREFIX}_iterations_sample.csv", samples)
    write_csv(REPORTS / f"{OUT_PREFIX}_identity_remap_iterations_sample.csv", identity_samples)
    (REPORTS / f"{OUT_PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_doc(DOCS / f"{OUT_PREFIX}.md", summary, profiles)
    print(json.dumps(summary["decision"], indent=2))


if __name__ == "__main__":
    main()
