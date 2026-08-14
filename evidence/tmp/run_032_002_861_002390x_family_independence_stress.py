"""Stress-tests whether the strict 125 witnesses are really independent of each other.

This script reads the source-normalized contrast rows for the 002-390-X branch and
focuses on the four 125 witnesses (M-38, M-119, M-735, Sktd-1), with M-119 and M-735 as
the strict source-visible pair. It asks whether the strict pair collapses into a single
formula or source family — if two witnesses are just copies of one formula, they count
as one piece of evidence, not two. It compares exact formulas, broad register, and the
known bridge risks (M-38 is the shared weak hinge), then writes a summary JSON and a
docs/ markdown note. The recorded outcome: the strict pair survives exact-formula
collapse but still shares a broad register, so it is medium confidence, not proof.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "data" / "open_prototype" / "reports"
DOC_DIR = ROOT / "docs"
PREFIX = "campaign_032_002_861_002390x_family_independence_stress"
DATE = "2026-05-30"
ROWS = REPORT_DIR / "campaign_032_002_861_002390x_source_normalized_contrast_rows.csv"


TARGETS = {"M-38", "M-119", "M-735", "Sktd-1"}
STRICT_TARGETS = {"M-119", "M-735"}


def read_rows() -> list[dict[str, str]]:
    with ROWS.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def key(row: dict[str, str]) -> str:
    return row["cisi"] if row["cisi"] != "-" else row["id"]


def main() -> None:
    rows = read_rows()
    target_rows = [r for r in rows if key(r) in TARGETS]
    strict_rows = [r for r in target_rows if key(r) in STRICT_TARGETS]

    compare_rows = []
    for r in target_rows:
        compare_rows.append(
            {
                "object": key(r),
                "strict_source_visible": r["strict_source_visible"],
                "permissive_public_panel": r["permissive_public_panel"],
                "site": r["site"],
                "type": r["type"],
                "symbol": r["symbol"],
                "cult": r["cult"],
                "shape": r["shape"],
                "material": r["material"],
                "condition": r["condition"],
                "text": r["text"],
                "text_len": r["text_len"],
                "prev_before_002": r["prev_before_002"],
                "next_after_390": r["next_after_390"],
                "tail_after_next": r["tail_after_next"],
                "normalized_source_grade": r["normalized_source_grade"],
                "family_role": (
                    "strict_independent_candidate"
                    if key(r) in STRICT_TARGETS
                    else "weak_bridge_or_downweighted_candidate"
                ),
            }
        )

    dimensions = [
        "site",
        "type",
        "symbol",
        "cult",
        "shape",
        "material",
        "condition",
        "text",
        "text_len",
        "prev_before_002",
        "tail_after_next",
        "normalized_source_grade",
    ]
    strict_dimension_rows = []
    for dim in dimensions:
        vals = defaultdict(list)
        for r in strict_rows:
            vals[r[dim]].append(key(r))
        strict_dimension_rows.append(
            {
                "dimension": dim,
                "distinct_values": len(vals),
                "values": " | ".join(f"{v}: {' '.join(members)}" for v, members in vals.items()),
                "collapse_effect": "collapses_strict_targets" if len(vals) == 1 else "separates_strict_targets",
            }
        )

    bridge_rows = [
        {
            "bridge": "M-38 links two subframes but is weak",
            "evidence": "M-38 shares prev_before_002=235 with M-735 and tail_after_next starts 632 032 with M-119",
            "risk": "M-38 can make the pattern look cleaner than the strict source-visible layer permits",
            "decision": "do_not_use_M38_as_strict_independence_bridge",
        },
        {
            "bridge": "M-119/M-735 strict pair",
            "evidence": "different full texts, different prev_before_002, different tails, different symbol/cult, different source routes",
            "risk": "same broad site/type/shape/material Mohenjo-daro seal register",
            "decision": "two strict candidate families at medium confidence, not final proof",
        },
        {
            "bridge": "Sktd-1 outside-site pressure",
            "evidence": "Surkotada panel-bound candidate with different prev_before_002 and tail",
            "risk": "not strict source-token proof and different site/register may explain behavior",
            "decision": "downweighted external pressure only",
        },
    ]

    decisions = [
        {
            "decision": "strict_125_not_single_exact_formula",
            "verdict": "M-119 and M-735 do not collapse by full text, preceding frame, tail, symbol/cult, or source route.",
        },
        {
            "decision": "broad_register_still_shared",
            "verdict": "Both strict targets are Mohenjo-daro square steatite SEAL:S rows, so broad register independence is not proven.",
        },
        {
            "decision": "M38_quarantine",
            "verdict": "M-38 remains useful as weak triangulation but cannot carry strict subframe independence.",
        },
        {
            "decision": "next_gate",
            "verdict": "Find either a third strict source-visible 125 branch family or source-visible non-125 matched frames; do not promote 125 to value.",
        },
    ]

    write_csv(REPORT_DIR / f"{PREFIX}_target_rows.csv", compare_rows)
    write_csv(REPORT_DIR / f"{PREFIX}_strict_dimension_collapse.csv", strict_dimension_rows)
    write_csv(REPORT_DIR / f"{PREFIX}_bridge_risks.csv", bridge_rows)
    write_csv(REPORT_DIR / f"{PREFIX}_decisions.csv", decisions)

    summary = {
        "date": DATE,
        "strict_targets": [key(r) for r in strict_rows],
        "strict_target_count": len(strict_rows),
        "strict_pair_exact_text_collapse": False,
        "strict_pair_prev_tail_collapse": False,
        "strict_pair_broad_register_shared": True,
        "decision": "strict_pair_survives_exact_formula_collapse_but_broad_register_shared",
        "doc": str(DOC_DIR / f"{PREFIX}.md"),
    }
    (REPORT_DIR / f"{PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    dim_lines = "\n".join(
        f"- `{r['dimension']}`: {r['collapse_effect']}; {r['values']}" for r in strict_dimension_rows
    )
    bridge_lines = "\n".join(
        f"- {r['bridge']}: {r['decision']}. Risk: {r['risk']}" for r in bridge_rows
    )
    decision_lines = "\n".join(f"- `{r['decision']}`: {r['verdict']}" for r in decisions)
    text = dedent(
        f"""\
        # 032-002-861 / 002-390-X Family-Independence Stress

        Date: {DATE}

        ## Question

        Do strict `125` witnesses `M-119` and `M-735` collapse into one formula/source family after the source-window gate?

        ## Result

        They do not collapse as one exact formula. They remain two strict candidate families at medium confidence.

        The positive side: `M-119` and `M-735` differ by full text, previous sign before `002`, post-`125` tail, symbol/cult label, source route, and condition. `M-119` tests the `125->632 032` subframe; `M-735` tests the `235->002-390->125` subframe.

        The negative side: both are still Mohenjo-daro square steatite `SEAL:S` rows. That shared broad register blocks any claim that `125` is independently established across the script.

        ## Strict Pair Dimensions

        {dim_lines}

        ## Bridge Risks

        {bridge_lines}

        ## Decisions

        {decision_lines}

        ## Linguistic Decision

        `125` survives exact-formula collapse between the two strict source-visible witnesses, but remains broad-register limited. The next upgrade requires either a third strict source-visible `125` branch family or a source-visible matched non-`125` frame that clarifies what the branch slot is doing.

        Accepted value, phonetics, language identity, and translation remain `0`.
        """
    )
    text = "\n".join(line[8:] if line.startswith("        ") else line for line in text.splitlines()) + "\n"
    doc = DOC_DIR / f"{PREFIX}.md"
    doc.write_text(text, encoding="utf-8")
    print(json.dumps({**summary, "doc": str(doc)}, indent=2))


if __name__ == "__main__":
    main()
