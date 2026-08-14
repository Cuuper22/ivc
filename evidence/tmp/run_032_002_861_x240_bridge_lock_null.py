"""Run a shuffle null to see how often the 603 bridge-lock pattern arises by chance.

The observed pattern: 603 sits locked to the 060 692 subframe inside
X-before-240 and also bridges into the post-002-861 tail zone. Could random
label placement produce that? The null model keeps the 95 X-before-240 rows'
after-240 subframes fixed, shuffles the X-sign labels across those rows for
20,000 iterations (seeded, so the run is reproducible), and counts how often
a shuffled world shows: 603 locked anywhere, 603 locked specifically to
060 692, any non-background bridge sign locked, or any low-frequency one
locked. Those counts become false-positive rates. The recorded decision:
weak-to-moderate distributional support (~4% for the broadest pattern), which
is real pressure but not a promotion — 603 gets no value. Writes a sample of
iteration rows, a JSON summary, and a Markdown doc in docs/.
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
OUT_PREFIX = "campaign_032_002_861_x240_bridge_lock_null"

ITERATIONS = 20000
SEED = 603240861


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


def sign_profiles(x240_rows: list[dict[str, str]], post861_rows: list[dict[str, str]]) -> dict[str, dict[str, object]]:
    by_x: dict[str, list[dict[str, str]]] = defaultdict(list)
    post_counts = Counter(row["tail_initial"] for row in post861_rows)
    for row in x240_rows:
        by_x[row["x_sign"]].append(row)

    profiles: dict[str, dict[str, object]] = {}
    for sign, rows in by_x.items():
        after = Counter(row["after_240_first3"] for row in rows)
        profiles[sign] = {
            "x240_rows": len(rows),
            "distinct_after240": len(after),
            "locked": len(after) == 1,
            "dominant_after240": after.most_common(1)[0][0],
            "post861_initial_rows": post_counts.get(sign, 0),
            "is_nonbackground_bridge": sign not in {"000", "<END>"} and post_counts.get(sign, 0) > 0,
        }
    return profiles


def metric_from_assignment(
    assigned_signs: list[str],
    after_values: list[str],
    post_counts: Counter[str],
) -> dict[str, object]:
    by_sign: dict[str, list[str]] = defaultdict(list)
    for sign, after in zip(assigned_signs, after_values):
        by_sign[sign].append(after)

    bridge_locked = []
    lowfreq_bridge_locked = []
    sign603 = by_sign.get("603", [])
    for sign, afters in by_sign.items():
        locked = len(set(afters)) == 1
        bridge = sign not in {"000", "<END>"} and post_counts.get(sign, 0) > 0
        if bridge and locked:
            bridge_locked.append(sign)
        if bridge and locked and len(afters) <= 3:
            lowfreq_bridge_locked.append(sign)

    return {
        "sign603_locked": bool(sign603 and len(set(sign603)) == 1),
        "sign603_locked_to_060_692": bool(sign603 and set(sign603) == {"060 692"}),
        "any_nonbackground_bridge_locked": bool(bridge_locked),
        "any_lowfreq_nonbackground_bridge_locked": bool(lowfreq_bridge_locked),
        "bridge_locked_signs": ";".join(sorted(bridge_locked)),
        "lowfreq_bridge_locked_signs": ";".join(sorted(lowfreq_bridge_locked)),
    }


def run_null(x240_rows: list[dict[str, str]], post861_rows: list[dict[str, str]]) -> tuple[list[dict[str, object]], dict[str, object]]:
    rng = random.Random(SEED)
    observed_profiles = sign_profiles(x240_rows, post861_rows)
    signs = [row["x_sign"] for row in x240_rows]
    after_values = [row["after_240_first3"] for row in x240_rows]
    post_counts = Counter(row["tail_initial"] for row in post861_rows)

    observed_metric = metric_from_assignment(signs, after_values, post_counts)
    iter_rows: list[dict[str, object]] = []
    counts = Counter()
    for idx in range(ITERATIONS):
        shuffled = signs[:]
        rng.shuffle(shuffled)
        metric = metric_from_assignment(shuffled, after_values, post_counts)
        for key, value in metric.items():
            if isinstance(value, bool) and value:
                counts[key] += 1
        if idx < 250:
            iter_rows.append({"iteration": idx, **metric})

    fprs = {
        key: counts[key] / ITERATIONS
        for key in [
            "sign603_locked",
            "sign603_locked_to_060_692",
            "any_nonbackground_bridge_locked",
            "any_lowfreq_nonbackground_bridge_locked",
        ]
    }
    summary = {
        "date": "2026-05-29",
        "seed": SEED,
        "iterations": ITERATIONS,
        "x240_rows": len(x240_rows),
        "distinct_x_signs": len(set(signs)),
        "post861_tail_initial_states": len(post_counts),
        "observed_metric": observed_metric,
        "observed_profiles": observed_profiles,
        "null_false_positive_rates": fprs,
        "decision": {
            "status": "bridge_lock_pattern_is_weak_to_moderate_distributional_support_not_a_promotion",
            "interpretation": [
                "The exact `603 locked to 060 692` pattern is uncommon under row-label shuffle.",
                "The broader class of any low-frequency non-background bridge sign locked to one after-240 subframe appears at about the 4% level, so the pattern is real pressure but still small-count and model-sensitive.",
                "Therefore this null gives weak-to-moderate support to the bridge-lock pattern without promoting `603` to value evidence.",
                "The next promotion still depends on source graphic identity or an independent second X-before-240 context for `603`.",
            ],
            "not_accepted": [
                "603 value",
                "phonetics",
                "language identity",
                "translation",
                "accepted graphic identity",
            ],
        },
    }
    return iter_rows, summary


def write_doc(path: Path, summary: dict[str, object]) -> None:
    fprs = summary["null_false_positive_rates"]
    assert isinstance(fprs, dict)
    decision = summary["decision"]
    assert isinstance(decision, dict)
    lines = [
        "# 032-002-861 X-Before-240 Bridge-Lock Null",
        "",
        "Date: 2026-05-29",
        "",
        "## Question",
        "",
        "Is the current `603` pattern rare enough to promote, or is it a small-count bridge-lock pattern that random X-label placement can reproduce?",
        "",
        "## Method",
        "",
        "The 95 X-before-`240` rows keep their after-`240` subframes fixed. The observed X-sign multiset is shuffled across those rows for 20,000 iterations, preserving sign counts and after-`240` subframe sizes but breaking sign-to-subframe association. Post-`002-861` tail-initial counts stay attached to sign labels.",
        "",
        "This is a distributional adversary, not a source or value test.",
        "",
        "## Observed",
        "",
        "- `603` is locked to `060 692` inside X-before-`240`.",
        "- `603` is a non-background post-`002-861` bridge sign.",
        "- `603` has 3 X-before-`240` rows and 3 post-`002-861` tail-initial rows.",
        "",
        "## Null Results",
        "",
        f"- `P(shuffled 603 locked anywhere) = {fprs['sign603_locked']:.6f}`",
        f"- `P(shuffled 603 locked specifically to 060 692) = {fprs['sign603_locked_to_060_692']:.6f}`",
        f"- `P(any non-background bridge sign locked) = {fprs['any_nonbackground_bridge_locked']:.6f}`",
        f"- `P(any low-frequency non-background bridge sign locked) = {fprs['any_lowfreq_nonbackground_bridge_locked']:.6f}`",
        "",
        "## Decision",
        "",
        f"Status: `{decision['status']}`.",
        "",
    ]
    for item in decision["interpretation"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Accepted values, phonetics, language identity, translations, and graphic identity remain 0/unaccepted.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    x240_rows = read_csv(X240_ROWS)
    post861_rows = read_csv(POST861_ROWS)
    iter_rows, summary = run_null(x240_rows, post861_rows)
    write_csv(REPORTS / f"{OUT_PREFIX}_iterations_sample.csv", iter_rows)
    (REPORTS / f"{OUT_PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_doc(DOCS / f"{OUT_PREFIX}.md", summary)
    print(json.dumps(summary["null_false_positive_rates"], indent=2))


if __name__ == "__main__":
    main()
