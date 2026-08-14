"""Rank competing hypotheses about what the post-861 tail zone is.

We read the source-normalized tail predictor rows and ask three questions.
First, which features (exact prefix, last-N prefix signs, register, site,
shape, text length) carry the most mutual information — measured in bits —
about whether a row has a tail, what class of tail, and which tail. Second,
which concrete feature-value "lanes" score highest as places to look next,
using a hand-built score that rewards source-ready non-bare rows and multiple
family cells and punishes lanes with no checked sources or a single copy
family. Third, we tabulate the four tail classes themselves. The output CSVs
(feature information, ranked lanes, tail classes, hypotheses) and the JSON
summary carry a fixed five-entry hypothesis tournament, each with its support,
next evidence, and kill gate. No readings are proposed.
"""

import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IN_ROWS = ROOT / "data/open_prototype/reports/campaign_032_002_861_source_normalized_tail_predictor_all_rows.csv"
OUT_DIR = ROOT / "data/open_prototype/reports"
SLUG = "campaign_032_002_861_post861_hypothesis_tournament"


def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def dist(values):
    counts = Counter(v if v not in ("", None) else "NULL" for v in values)
    return ";".join(f"{k}:{v}" for k, v in counts.most_common())


def entropy(labels):
    n = len(labels)
    if n == 0:
        return 0.0
    counts = Counter(labels)
    total = 0.0
    for count in counts.values():
        p = count / n
        total -= p * math.log2(p)
    return total


def mutual_information(rows, feature, label_getter):
    labels = [label_getter(r) for r in rows]
    base = entropy(labels)
    n = len(rows)
    by_value = defaultdict(list)
    for row in rows:
        by_value[row.get(feature) or "NULL"].append(row)
    conditional = 0.0
    for group in by_value.values():
        conditional += (len(group) / n) * entropy([label_getter(r) for r in group])
    return base - conditional


def source_ready(row):
    return row.get("source_status") not in ("", "source_pending_or_not_checked", None)


def family_key(row):
    return "|".join(
        row.get(k, "")
        for k in ("site", "type", "symbol", "shape", "cross_section", "material", "tail", "prefix_last2")
    )


def tail_len(row):
    try:
        return int(row.get("tail_len") or 0)
    except ValueError:
        return 0


def tail_class(row):
    tail = row.get("tail") or "<END>"
    if tail == "<END>":
        return "closure"
    length = tail_len(row)
    if length == 1:
        return "simple_single"
    if length == 2:
        return "fixed_pair"
    return "long_continuation"


def broad_tail_label(row):
    return row.get("tail") or "<END>"


def semicolon_examples(rows, limit=8):
    return ";".join(f"{r.get('cisi')} {r.get('text')}" for r in rows[:limit])


def classify_lane(feature, rows):
    tails = Counter(broad_tail_label(r) for r in rows)
    non_bare = sum(1 for r in rows if broad_tail_label(r) != "<END>")
    source_non_bare = sum(1 for r in rows if broad_tail_label(r) != "<END>" and source_ready(r))
    source_rows = sum(1 for r in rows if source_ready(r))
    family_cells = len({family_key(r) for r in rows})
    tail_classes = len({tail_class(r) for r in rows})
    source_tail_types = len({broad_tail_label(r) for r in rows if source_ready(r)})
    exactish = feature in {"prefix", "prefix_last3", "prefix_last2"}
    registerish = feature in {"register_key", "broad_register_key", "site", "symbol", "shape", "type"}

    if exactish and len(tails) > 1 and source_non_bare == 0:
        return "source_acquisition_exact_preframe_split"
    if source_non_bare and source_tail_types >= 2 and family_cells >= 3:
        return "source_live_tail_choice_field"
    if registerish and len(tails) >= 3 and non_bare >= 2:
        return "register_polysemy_field"
    if non_bare >= 2 and family_cells <= 2:
        return "copy_family_or_formula_risk"
    if non_bare == 1:
        return "singleton_contrast_watch"
    return "background_or_low_payoff"


def lane_score(feature, rows):
    tails = Counter(broad_tail_label(r) for r in rows)
    non_bare = sum(1 for r in rows if broad_tail_label(r) != "<END>")
    source_non_bare = sum(1 for r in rows if broad_tail_label(r) != "<END>" and source_ready(r))
    family_cells = len({family_key(r) for r in rows})
    tail_classes = len({tail_class(r) for r in rows})
    sites = len({r.get("site") for r in rows})
    registers = len({r.get("register_key") for r in rows})
    score = 0
    score += min(len(rows), 20)
    score += 5 * min(source_non_bare, 4)
    score += 3 * min(non_bare, 5)
    score += 4 * (len(tails) - 1)
    score += 3 * (tail_classes - 1)
    score += 2 * min(family_cells, 5)
    if sites > 1:
        score += 2
    if registers > 1:
        score += 2
    if feature == "prefix":
        score += 3
    if feature in {"prefix_last2", "prefix_last3"}:
        score += 2
    if source_non_bare == 0:
        score -= 10
    if non_bare and family_cells <= 1:
        score -= 8
    return score


def main():
    rows = read_csv(IN_ROWS)
    predictor_features = [
        "prefix",
        "prefix_last3",
        "prefix_last2",
        "prefix_last1",
        "register_key",
        "broad_register_key",
        "site",
        "type",
        "symbol",
        "shape",
        "text_length",
        "prefix_len",
    ]
    lane_features = [
        "prefix",
        "prefix_last3",
        "prefix_last2",
        "prefix_last1",
    ]

    feature_rows = []
    for feature in predictor_features:
        feature_rows.append(
            {
                "feature": feature,
                "nonbare_mi_bits": f"{mutual_information(rows, feature, lambda r: 'nonbare' if broad_tail_label(r) != '<END>' else 'closure'):.6f}",
                "tail_class_mi_bits": f"{mutual_information(rows, feature, tail_class):.6f}",
                "tail_identity_mi_bits": f"{mutual_information(rows, feature, broad_tail_label):.6f}",
            }
        )
    feature_rows.sort(key=lambda r: float(r["tail_class_mi_bits"]), reverse=True)

    lanes = []
    for feature in lane_features:
        groups = defaultdict(list)
        for row in rows:
            groups[row.get(feature) or "NULL"].append(row)
        for value, group in groups.items():
            non_bare = [r for r in group if broad_tail_label(r) != "<END>"]
            if len(group) < 2 or not non_bare:
                continue
            tails = Counter(broad_tail_label(r) for r in group)
            if len(tails) == 1 and "<END>" not in tails:
                # Pure non-bare clusters matter only if they repeat beyond one family.
                if len({family_key(r) for r in group}) < 2:
                    continue
            lanes.append(
                {
                    "score": lane_score(feature, group),
                    "lane_class": classify_lane(feature, group),
                    "feature": feature,
                    "value": value,
                    "rows": len(group),
                    "non_bare_rows": len(non_bare),
                    "family_cells": len({family_key(r) for r in group}),
                    "source_ready_rows": sum(1 for r in group if source_ready(r)),
                    "source_ready_non_bare_rows": sum(1 for r in non_bare if source_ready(r)),
                    "tail_distribution": dist(broad_tail_label(r) for r in group),
                    "tail_class_distribution": dist(tail_class(r) for r in group),
                    "register_distribution": dist(r.get("register_key") for r in group),
                    "site_distribution": dist(r.get("site") for r in group),
                    "examples": semicolon_examples(group, 10),
                }
            )
    lanes.sort(key=lambda r: (r["score"], r["source_ready_non_bare_rows"], r["non_bare_rows"]), reverse=True)

    class_rows = []
    for cls in ("closure", "simple_single", "fixed_pair", "long_continuation"):
        group = [r for r in rows if tail_class(r) == cls]
        class_rows.append(
            {
                "tail_class": cls,
                "rows": len(group),
                "family_cells": len({family_key(r) for r in group}),
                "source_ready_rows": sum(1 for r in group if source_ready(r)),
                "tail_distribution": dist(broad_tail_label(r) for r in group),
                "register_distribution": dist(r.get("register_key") for r in group),
                "prefix_last2_distribution": dist(r.get("prefix_last2") for r in group),
                "examples": semicolon_examples(group, 12),
            }
        )

    hypotheses = [
        {
            "rank": 1,
            "hypothesis": "post_861_secondary_zone_is_typed_not_one_suffix",
            "support": "Closure dominates, but non-bare rows split into simple singles, fixed pairs, and long continuations across multiple context lanes.",
            "best_next_evidence": "Compare tail class, not tail identity, against prefix/register features and against other post-002 branch signs.",
            "kill_gate": "If every source-live non-bare row is explained by terminal margin, side-order, or one copied source/register family, treat the zone as graphic/catalog residue.",
        },
        {
            "rank": 2,
            "hypothesis": "long_continuations_are_second_phrases_or_formula_continuations",
            "support": "Long tails recur as a type but not as one repeated sign value; they are adversaries to suffix readings.",
            "best_next_evidence": "Run source-visible line/spacing checks on long-tail rows and ask whether they begin a visually separate phrase after 861.",
            "kill_gate": "If long tails are all broken signbands or unrelated surface residue, remove them from grammatical continuation counts.",
        },
        {
            "rank": 3,
            "hypothesis": "fixed_pair_final_units_exist_but_are_narrow_cells",
            "support": "533-717 is fixed and source-ready but trapped in a small no-icon Mohenjo SEAL:R cell.",
            "best_next_evidence": "Search for another fixed pair with independent cells or a third 533-717 witness before assigning function.",
            "kill_gate": "If no third independent row or same-prefix contrast appears, keep fixed pairs as local formulas, not translatable morphemes.",
        },
        {
            "rank": 4,
            "hypothesis": "simple_single_tails_are_live_as_tail_class_not_values",
            "support": "603 has three source-ready post-861 rows, while other simple tails are mostly source-pending or formula-bound.",
            "best_next_evidence": "Find another source-ready simple-single tail with two independent cells, or compare simple-single behavior across post-002 branch signs.",
            "kill_gate": "If simple singles collapse to one family each after source normalization, they are acquisition priorities only.",
        },
        {
            "rank": 5,
            "hypothesis": "exact_preframe_tail_choice_is_the_best_route_to_reading_probability",
            "support": "Exact/same-prefix splits are rare but are the closest thing to minimal pairs.",
            "best_next_evidence": "Batch all exact and same-last2 splits together; do not spend a full work unit on one sign unless it changes the class model.",
            "kill_gate": "If source routing shows exact splits are cross-site/copy artifacts with no visual comparability, demote them.",
        },
    ]

    write_csv(
        OUT_DIR / f"{SLUG}_feature_information.csv",
        feature_rows,
        ["feature", "nonbare_mi_bits", "tail_class_mi_bits", "tail_identity_mi_bits"],
    )
    write_csv(
        OUT_DIR / f"{SLUG}_ranked_lanes.csv",
        lanes,
        [
            "score",
            "lane_class",
            "feature",
            "value",
            "rows",
            "non_bare_rows",
            "family_cells",
            "source_ready_rows",
            "source_ready_non_bare_rows",
            "tail_distribution",
            "tail_class_distribution",
            "register_distribution",
            "site_distribution",
            "examples",
        ],
    )
    write_csv(
        OUT_DIR / f"{SLUG}_tail_classes.csv",
        class_rows,
        [
            "tail_class",
            "rows",
            "family_cells",
            "source_ready_rows",
            "tail_distribution",
            "register_distribution",
            "prefix_last2_distribution",
            "examples",
        ],
    )
    write_csv(
        OUT_DIR / f"{SLUG}_hypotheses.csv",
        hypotheses,
        ["rank", "hypothesis", "support", "best_next_evidence", "kill_gate"],
    )

    summary = {
        "date": "2026-05-29",
        "input": str(IN_ROWS),
        "rows": len(rows),
        "non_bare_rows": sum(1 for r in rows if broad_tail_label(r) != "<END>"),
        "source_ready_rows": sum(1 for r in rows if source_ready(r)),
        "tail_class_distribution": dist(tail_class(r) for r in rows),
        "top_feature_by_tail_class_mi": feature_rows[:6],
        "top_lanes": lanes[:12],
        "hypotheses": hypotheses,
    }
    (OUT_DIR / f"{SLUG}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
