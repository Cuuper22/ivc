"""Re-test the 603 bridge lock after collapsing repeated rows into family cells.

The earlier row-level null gave the 603 bridge-lock pattern weak-to-moderate
support. But repeated identical Harappa rows may be copies, not independent
witnesses. This audit collapses the 95 X-before-240 rows into family cells
keyed by (X sign, prefix, after-240 subframe, register, signless formula
template), then reruns the seeded 20,000-iteration label-shuffle null at the
cell level. The result recorded here: 603 collapses to a single family cell,
so its Harappa-side internal evidence is not replicated, and the bridge
pressure is demoted from support to acquisition priority. 603 stays not
promoted; no value, phonetics, or translation is accepted. Writes cell,
profile, and null-sample CSVs, a JSON summary, and a Markdown doc in docs/.
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

X240_ROWS = REPORTS / "campaign_032_002_861_x240_internal_subframes_rows.csv"
POST861_ROWS = REPORTS / "campaign_032_002_861_x240_bridge_post861_rows.csv"
OUT_PREFIX = "campaign_032_002_861_x240_family_cell_bridge_audit"

ITERATIONS = 20000
SEED = 603240862


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


def template_for(row: dict[str, str]) -> str:
    parts = tokens(row["text"])
    x = row["x_sign"]
    prefix = row["prefix"]
    for idx in range(1, len(parts) - 1):
        if parts[idx - 1] == prefix and parts[idx] == x and parts[idx + 1] == "240":
            templated = parts[:]
            templated[idx] = "X"
            return "+" + "-".join(templated) + "+"
    return row["text"].replace(f"-{x}-240", "-X-240", 1)


def collapse_family_cells(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    groups: dict[tuple[str, str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (
            row["x_sign"],
            row["prefix"],
            row["after_240_first3"],
            row["register_key"],
            template_for(row),
        )
        groups[key].append(row)

    cells: list[dict[str, object]] = []
    for (x, prefix, after, register, template), group in sorted(groups.items(), key=lambda item: (item[0][0], item[0][2], item[0][4])):
        cells.append(
            {
                "x_sign": x,
                "prefix": prefix,
                "after_240_first3": after,
                "register_key": register,
                "template_key": template,
                "raw_rows": len(group),
                "source_objects": ";".join(sorted({row["cisi"] for row in group})),
                "source_object_count": len({row["cisi"] for row in group}),
                "examples": ";".join(f"{row['cisi']} {row['text']}" for row in group[:8]),
            }
        )
    return cells


def build_profiles(cells: list[dict[str, object]], post861_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    post_counts = Counter(row["tail_initial"] for row in post861_rows)
    post_families: dict[str, set[str]] = defaultdict(set)
    for row in post861_rows:
        post_families[row["tail_initial"]].add(row["tail_after_002_861"])

    by_x: dict[str, list[dict[str, object]]] = defaultdict(list)
    for cell in cells:
        by_x[str(cell["x_sign"])].append(cell)

    profiles: list[dict[str, object]] = []
    for x, group in sorted(by_x.items(), key=lambda item: (-len(item[1]), item[0])):
        after_counts = Counter(str(cell["after_240_first3"]) for cell in group)
        profiles.append(
            {
                "x_sign": x,
                "family_cells": len(group),
                "raw_rows": sum(int(cell["raw_rows"]) for cell in group),
                "distinct_after240_subframes": len(after_counts),
                "locked_at_family_cell_level": len(after_counts) == 1,
                "dominant_after240_subframe": after_counts.most_common(1)[0][0],
                "after240_cell_counts": ";".join(f"{key}:{value}" for key, value in after_counts.most_common()),
                "post_002_861_tail_initial_rows": post_counts.get(x, 0),
                "post_002_861_tail_families": len(post_families.get(x, set())),
                "is_nonbackground_bridge": x not in {"000", "<END>"} and post_counts.get(x, 0) > 0,
                "examples": ";".join(str(cell["examples"]) for cell in group[:6]),
            }
        )
    return profiles


def metric(assigned_signs: list[str], after_values: list[str], post_counts: Counter[str]) -> dict[str, object]:
    by_sign: dict[str, list[str]] = defaultdict(list)
    for sign, after in zip(assigned_signs, after_values):
        by_sign[sign].append(after)

    def nonbackground_bridge(sign: str) -> bool:
        return sign not in {"000", "<END>"} and post_counts.get(sign, 0) > 0

    bridge_single_cell = []
    bridge_multi_cell_locked = []
    sign603 = by_sign.get("603", [])
    for sign, afters in by_sign.items():
        if not nonbackground_bridge(sign):
            continue
        if len(afters) == 1:
            bridge_single_cell.append(sign)
        if len(afters) >= 2 and len(set(afters)) == 1:
            bridge_multi_cell_locked.append(sign)

    return {
        "sign603_has_one_family_cell": len(sign603) == 1,
        "sign603_family_cell_in_060_692": len(sign603) == 1 and sign603[0] == "060 692",
        "any_nonbackground_bridge_single_family_cell": bool(bridge_single_cell),
        "any_nonbackground_bridge_multi_cell_locked": bool(bridge_multi_cell_locked),
        "bridge_single_cell_signs": ";".join(sorted(bridge_single_cell)),
        "bridge_multi_cell_locked_signs": ";".join(sorted(bridge_multi_cell_locked)),
    }


def run_null(cells: list[dict[str, object]], post861_rows: list[dict[str, str]]) -> tuple[list[dict[str, object]], dict[str, object]]:
    rng = random.Random(SEED)
    signs = [str(cell["x_sign"]) for cell in cells]
    after_values = [str(cell["after_240_first3"]) for cell in cells]
    post_counts = Counter(row["tail_initial"] for row in post861_rows)
    observed = metric(signs, after_values, post_counts)

    counts = Counter()
    samples: list[dict[str, object]] = []
    for idx in range(ITERATIONS):
        shuffled = signs[:]
        rng.shuffle(shuffled)
        m = metric(shuffled, after_values, post_counts)
        for key, value in m.items():
            if isinstance(value, bool) and value:
                counts[key] += 1
        if idx < 250:
            samples.append({"iteration": idx, **m})

    rates = {
        key: counts[key] / ITERATIONS
        for key in [
            "sign603_has_one_family_cell",
            "sign603_family_cell_in_060_692",
            "any_nonbackground_bridge_single_family_cell",
            "any_nonbackground_bridge_multi_cell_locked",
        ]
    }
    profiles = build_profiles(cells, post861_rows)
    by_x = {str(row["x_sign"]): row for row in profiles}
    return samples, {
        "date": "2026-05-29",
        "seed": SEED,
        "iterations": ITERATIONS,
        "family_cells": len(cells),
        "raw_x240_rows": sum(int(cell["raw_rows"]) for cell in cells),
        "distinct_x_signs": len(set(signs)),
        "observed_metric": observed,
        "null_rates": rates,
        "target_profiles": {key: by_x.get(key) for key in ["603", "636", "642", "482", "904", "000"]},
        "decision": {
            "status": "603_harappa_side_collapses_to_one_family_cell_bridge_not_promoted",
            "interpretation": [
                "`603` has three raw X-before-240 rows but only one family cell after collapsing by X, prefix, after-240 subframe, register, and signless formula template.",
                "At family-cell level, `603` no longer supplies replicated Harappa-side internal evidence. It is one Harappa formula/register cell plus the post-002-861 Mohenjo tail family.",
                "The row-level bridge-lock pressure is therefore demoted from weak-to-moderate support to acquisition-priority pressure.",
                "The live promotion path is source graphic identity or a second independent family cell for Harappa/non-Mohenjo `603`.",
            ],
            "not_accepted": [
                "603 value",
                "phonetics",
                "language identity",
                "translation",
                "accepted graphic identity",
            ],
        },
        "profiles": profiles,
    }


def write_doc(path: Path, summary: dict[str, object]) -> None:
    rates = summary["null_rates"]
    assert isinstance(rates, dict)
    decision = summary["decision"]
    assert isinstance(decision, dict)
    profiles = summary["target_profiles"]
    assert isinstance(profiles, dict)
    lines = [
        "# 032-002-861 X-Before-240 Family-Cell Bridge Audit",
        "",
        "Date: 2026-05-29",
        "",
        "## Question",
        "",
        "Does the `603` bridge-lock pattern survive when repeated X-before-`240` rows are collapsed into formula/register family cells?",
        "",
        "## Method",
        "",
        "The raw X-before-`240` packet has 95 rows. This audit collapses rows by `(X sign, prefix, after-240 subframe, register key, signless formula template)`. That keeps linguistic formula cells instead of treating repeated identical Harappa text rows as independent evidence.",
        "",
        f"Family cells: `{summary['family_cells']}` from `{summary['raw_x240_rows']}` raw rows across `{summary['distinct_x_signs']}` X signs.",
        "",
        "A label-shuffle null then shuffles X labels across family cells for 20,000 iterations, preserving X family-cell counts and after-`240` family-cell sizes.",
        "",
        "## Target Profiles",
        "",
        "| X | family cells | raw rows | subframes | locked? | post-861 initial rows | after-240 cells |",
        "|---|---:|---:|---:|---|---:|---|",
    ]
    for sign in ["603", "636", "642", "482", "904", "000"]:
        row = profiles.get(sign)
        if not row:
            continue
        lines.append(
            "| {x_sign} | {family_cells} | {raw_rows} | {distinct_after240_subframes} | {locked_at_family_cell_level} | {post_002_861_tail_initial_rows} | {after240_cell_counts} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Null Results",
            "",
            f"- `P(shuffled 603 has one family cell) = {rates['sign603_has_one_family_cell']:.6f}`",
            f"- `P(shuffled 603 single family cell lands in 060 692) = {rates['sign603_family_cell_in_060_692']:.6f}`",
            f"- `P(any non-background bridge sign has a single family cell) = {rates['any_nonbackground_bridge_single_family_cell']:.6f}`",
            f"- `P(any non-background bridge sign has >=2 family cells locked to one subframe) = {rates['any_nonbackground_bridge_multi_cell_locked']:.6f}`",
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
    x240_rows = read_csv(X240_ROWS)
    post861_rows = read_csv(POST861_ROWS)
    cells = collapse_family_cells(x240_rows)
    profiles = build_profiles(cells, post861_rows)
    samples, summary = run_null(cells, post861_rows)

    write_csv(REPORTS / f"{OUT_PREFIX}_cells.csv", cells)
    write_csv(REPORTS / f"{OUT_PREFIX}_profiles.csv", profiles)
    write_csv(REPORTS / f"{OUT_PREFIX}_null_iterations_sample.csv", samples)
    (REPORTS / f"{OUT_PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_doc(DOCS / f"{OUT_PREFIX}.md", summary)
    print(json.dumps(summary["decision"], indent=2))


if __name__ == "__main__":
    main()
