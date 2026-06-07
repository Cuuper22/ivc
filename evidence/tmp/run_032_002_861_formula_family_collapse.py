import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
IN_ROWS = ROOT / "data/open_prototype/reports/campaign_032_002_861_source_normalized_tail_predictor_all_rows.csv"
OUT_DIR = ROOT / "data/open_prototype/reports"
SLUG = "campaign_032_002_861_formula_family_collapse"


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
    counts = Counter(v if v not in ("", None) else "<START>" for v in values)
    return ";".join(f"{k}:{v}" for k, v in counts.most_common())


def norm_prefix(row):
    return row.get("prefix") or "<START>"


def norm_last(row, key):
    return row.get(key) or "<START>"


def tail(row):
    return row.get("tail") or "<END>"


def source_ready(row):
    return row.get("source_status") not in ("", "source_pending_or_not_checked", None) or bool(row.get("display_image"))


def tail_len(row):
    try:
        return int(row.get("tail_len") or 0)
    except ValueError:
        return 0


def tail_class(row):
    t = tail(row)
    if t == "<END>":
        return "closure"
    n = tail_len(row)
    if n == 1:
        return "simple_single"
    if n == 2:
        return "fixed_pair"
    return "long_continuation"


def strict_identity_family_key(row):
    # Harsh enough to stop repeated local rows from pretending to be separate
    # linguistic witnesses, but not so harsh that it erases every preframe.
    return "|".join(
        [
            tail(row),
            norm_prefix(row),
            row.get("register_key") or "",
            row.get("template_key") or "",
        ]
    )


def strict_class_family_key(row):
    return "|".join(
        [
            tail_class(row),
            norm_prefix(row),
            row.get("register_key") or "",
            row.get("template_key") or "",
        ]
    )


def formula_key(row):
    return "|".join([norm_prefix(row), tail(row), row.get("register_key") or ""])


def semicolon_examples(rows, limit=10):
    return ";".join(f"{r.get('cisi')} {r.get('text')}" for r in rows[:limit])


def dominant_share(values):
    values = list(values)
    if not values:
        return ("", "0.000")
    counts = Counter(values)
    key, count = counts.most_common(1)[0]
    return (key, f"{count / len(values):.3f}")


def exact_prefix_verdict(group):
    tails = Counter(tail(r) for r in group)
    classes = Counter(tail_class(r) for r in group)
    has_closure = "<END>" in tails
    has_non_bare = any(t != "<END>" for t in tails)
    src_non_bare = sum(1 for r in group if tail(r) != "<END>" and source_ready(r))
    if len(group) < 2:
        return "singleton_not_formula_evidence"
    if has_closure and has_non_bare and src_non_bare:
        return "source_live_exact_prefix_split"
    if has_closure and has_non_bare:
        return "exact_prefix_split_source_pending"
    if not has_closure and len(tails) > 1:
        return "tail_only_template_split_no_closure_control"
    if not has_closure and len(tails) == 1:
        return "repeated_tail_formula_or_copy_family"
    if len(classes) == 1 and "closure" in classes:
        return "repeated_closure_formula_background"
    return "mixed_formula_watch"


def identity_verdict(rows):
    t = tail(rows[0])
    n = len(rows)
    src = sum(1 for r in rows if source_ready(r))
    prefixes = len({norm_prefix(r) for r in rows})
    registers = len({r.get("register_key") for r in rows})
    families = len({strict_identity_family_key(r) for r in rows})
    dom_prefix, dom_prefix_share = dominant_share(norm_prefix(r) for r in rows)
    dom_register, dom_register_share = dominant_share(r.get("register_key") for r in rows)

    if t == "<END>":
        return "background_closure_not_tail_identity"
    if n == 1:
        return "singleton_watch_not_interpretable"
    if families <= 1 or float(dom_register_share) >= 0.80 and src == 0:
        return "copy_register_template_demoted"
    if t == "603" and src >= 3 and families >= 3:
        return "post861_simple_tail_class_survives_no_value"
    if t == "533 717" and src >= 2 and families >= 2 and registers == 1:
        return "fixed_final_unit_survives_narrow_register_no_function"
    if prefixes >= 2 and families >= 2 and src:
        return "structural_watch_survives_family_collapse_no_value"
    return "acquisition_watch_before_interpretation"


def class_verdict(class_name, rows):
    src = sum(1 for r in rows if source_ready(r))
    families = len({strict_class_family_key(r) for r in rows})
    prefixes = len({norm_prefix(r) for r in rows})
    dom_prefix, dom_prefix_share = dominant_share(norm_prefix(r) for r in rows)
    dom_register, dom_register_share = dominant_share(r.get("register_key") for r in rows)

    if class_name == "closure":
        return "background_closure_state"
    if class_name == "simple_single":
        if src >= 3 and families >= 10 and float(dom_prefix_share) < 0.50:
            return "class_alive_but_empty_prefix_and_copy_family_pressure"
        return "simple_class_weak_or_template_bound"
    if class_name == "fixed_pair":
        if families >= 5 and prefixes >= 5:
            return "class_exists_as_heterogeneous_fixed_units_no_shared_value"
        return "fixed_pair_class_too_narrow"
    if class_name == "long_continuation":
        return "second_unit_adversary_not_productive_class_yet"
    return "unclassified"


def main():
    rows = read_csv(IN_ROWS)

    exact_groups = []
    by_prefix = defaultdict(list)
    for row in rows:
        by_prefix[norm_prefix(row)].append(row)
    for prefix, group in by_prefix.items():
        if len(group) < 2 and all(tail(r) == "<END>" for r in group):
            continue
        exact_groups.append(
            {
                "prefix": prefix,
                "verdict": exact_prefix_verdict(group),
                "rows": len(group),
                "family_cells": len({strict_identity_family_key(r) for r in group}),
                "source_ready_rows": sum(1 for r in group if source_ready(r)),
                "source_ready_non_bare_rows": sum(1 for r in group if tail(r) != "<END>" and source_ready(r)),
                "tail_distribution": dist(tail(r) for r in group),
                "tail_class_distribution": dist(tail_class(r) for r in group),
                "register_distribution": dist(r.get("register_key") for r in group),
                "examples": semicolon_examples(group),
            }
        )
    exact_groups.sort(
        key=lambda r: (
            r["verdict"] == "source_live_exact_prefix_split",
            r["verdict"] == "exact_prefix_split_source_pending",
            r["source_ready_non_bare_rows"],
            r["rows"],
        ),
        reverse=True,
    )

    tail_id_rows = []
    by_tail = defaultdict(list)
    for row in rows:
        by_tail[tail(row)].append(row)
    for t, group in by_tail.items():
        dom_prefix, dom_prefix_share = dominant_share(norm_prefix(r) for r in group)
        dom_register, dom_register_share = dominant_share(r.get("register_key") for r in group)
        tail_id_rows.append(
            {
                "tail": t,
                "tail_class": tail_class(group[0]),
                "verdict": identity_verdict(group),
                "rows": len(group),
                "strict_identity_family_cells": len({strict_identity_family_key(r) for r in group}),
                "exact_prefixes": len({norm_prefix(r) for r in group}),
                "registers": len({r.get("register_key") for r in group}),
                "source_ready_rows": sum(1 for r in group if source_ready(r)),
                "dominant_prefix": dom_prefix,
                "dominant_prefix_share": dom_prefix_share,
                "dominant_register": dom_register,
                "dominant_register_share": dom_register_share,
                "prefix_last2_distribution": dist(norm_last(r, "prefix_last2") for r in group),
                "examples": semicolon_examples(group),
            }
        )
    tail_id_rows.sort(
        key=lambda r: (
            r["tail"] == "<END>",
            int(r["source_ready_rows"]),
            int(r["strict_identity_family_cells"]),
            int(r["rows"]),
        ),
        reverse=True,
    )

    class_rows = []
    by_class = defaultdict(list)
    for row in rows:
        by_class[tail_class(row)].append(row)
    for cls in ["closure", "simple_single", "fixed_pair", "long_continuation"]:
        group = by_class.get(cls, [])
        dom_prefix, dom_prefix_share = dominant_share(norm_prefix(r) for r in group)
        dom_register, dom_register_share = dominant_share(r.get("register_key") for r in group)
        class_rows.append(
            {
                "tail_class": cls,
                "verdict": class_verdict(cls, group),
                "rows": len(group),
                "strict_class_family_cells": len({strict_class_family_key(r) for r in group}),
                "tail_identities": len({tail(r) for r in group}),
                "exact_prefixes": len({norm_prefix(r) for r in group}),
                "registers": len({r.get("register_key") for r in group}),
                "source_ready_rows": sum(1 for r in group if source_ready(r)),
                "dominant_prefix": dom_prefix,
                "dominant_prefix_share": dom_prefix_share,
                "dominant_register": dom_register,
                "dominant_register_share": dom_register_share,
                "tail_distribution": dist(tail(r) for r in group),
                "examples": semicolon_examples(group, 12),
            }
        )

    attack_rows = [
        {
            "attack": "whole_formula_template",
            "verdict": "blocks_optional_grammar_promotion_but_does_not_explain_field",
            "evidence": "Exact-prefix mixed evidence is scarce; strongest source-ready split remains same-last2 not exact-prefix. Empty-prefix rows form a special all-nonbare template field. Tail classes still span many prefixes and family cells.",
            "next_gate": "Cluster complete left formulas before splitting at 861; require exact or near-exact source-visible alternations before grammar promotion.",
        },
        {
            "attack": "family_collapse",
            "verdict": "demotes_empty_prefix_416_698_and_keeps_603_533717_bounded",
            "evidence": "416/698 are source-pending template/register clusters. 603 survives as three source-ready post-861 family cells; 533-717 survives as two source-ready fixed-unit cells but in one narrow register field.",
            "next_gate": "Promote only tail classes that survive source-family collapse in at least two independent preframe lanes; keep individual values at zero.",
        },
        {
            "attack": "register_label",
            "verdict": "active_adversary_not_target_lane",
            "evidence": "Register MI is lower than prefix MI but still large enough to explain local pockets. Mohenjo no-icon SEAL:R and Harappa TAB:I remain dangerous controls.",
            "next_gate": "For each ranked preframe lane, compare tail choices inside register-matched controls and after terminal-space measurement.",
        },
        {
            "attack": "terminal_space",
            "verdict": "unresolved_global_gate",
            "evidence": "220-032 is blocked by measured terminal-space asymmetry; this campaign does not remeasure images.",
            "next_gate": "Run blind terminal-space recut across source-ready ranked lanes before any grammar upgrade.",
        },
    ]

    summary = {
        "date": "2026-05-29",
        "input": str(IN_ROWS),
        "rows": len(rows),
        "non_bare_rows": sum(1 for r in rows if tail(r) != "<END>"),
        "source_ready_rows": sum(1 for r in rows if source_ready(r)),
        "exact_prefix_groups": len(exact_groups),
        "exact_prefix_groups_with_closure_and_nonbare": sum(
            1
            for group in by_prefix.values()
            if any(tail(r) == "<END>" for r in group) and any(tail(r) != "<END>" for r in group)
        ),
        "class_rows": class_rows,
        "top_exact_prefix_groups": exact_groups[:12],
        "tail_identity_rows": tail_id_rows,
        "attack_rows": attack_rows,
    }

    write_csv(
        OUT_DIR / f"{SLUG}_exact_prefix_groups.csv",
        exact_groups,
        [
            "prefix",
            "verdict",
            "rows",
            "family_cells",
            "source_ready_rows",
            "source_ready_non_bare_rows",
            "tail_distribution",
            "tail_class_distribution",
            "register_distribution",
            "examples",
        ],
    )
    write_csv(
        OUT_DIR / f"{SLUG}_tail_identity_collapse.csv",
        tail_id_rows,
        [
            "tail",
            "tail_class",
            "verdict",
            "rows",
            "strict_identity_family_cells",
            "exact_prefixes",
            "registers",
            "source_ready_rows",
            "dominant_prefix",
            "dominant_prefix_share",
            "dominant_register",
            "dominant_register_share",
            "prefix_last2_distribution",
            "examples",
        ],
    )
    write_csv(
        OUT_DIR / f"{SLUG}_tail_class_collapse.csv",
        class_rows,
        [
            "tail_class",
            "verdict",
            "rows",
            "strict_class_family_cells",
            "tail_identities",
            "exact_prefixes",
            "registers",
            "source_ready_rows",
            "dominant_prefix",
            "dominant_prefix_share",
            "dominant_register",
            "dominant_register_share",
            "tail_distribution",
            "examples",
        ],
    )
    write_csv(
        OUT_DIR / f"{SLUG}_attack_verdicts.csv",
        attack_rows,
        ["attack", "verdict", "evidence", "next_gate"],
    )
    (OUT_DIR / f"{SLUG}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
