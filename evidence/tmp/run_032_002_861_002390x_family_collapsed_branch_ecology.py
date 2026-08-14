"""Summarizes the 002-390-X branch ecology after collapsing exact-formula families.

This script reads the row table produced by the source-normalized contrast campaign
(campaign_032_002_861_002390x_source_normalized_contrast_rows.csv). It groups the rows
into exact-text families — rows that repeat the same full inscription count as one
family, not as independent witnesses — and then summarizes the PREV -> 002-390 -> X ->
TAIL ecology by branch and by previous sign. It writes matrix CSVs, a summary JSON, and
a docs/ markdown note. The point is to see what the branch structure still says once
copy-families can no longer inflate the counts; the recorded decision keeps 125 live
but not readable.
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
PREFIX = "campaign_032_002_861_002390x_family_collapsed_branch_ecology"
DATE = "2026-05-30"
ROWS = REPORT_DIR / "campaign_032_002_861_002390x_source_normalized_contrast_rows.csv"


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


def obj(row: dict[str, str]) -> str:
    return row["cisi"] if row["cisi"] != "-" else f"-:{row['id']}"


def family_cell(row: dict[str, str]) -> str:
    return "|".join(
        [
            row["site"],
            row["type"],
            row["symbol"],
            row["cult"],
            row["shape"],
            row["material"],
            row["prev_before_002"],
            row["next_after_390"],
            row["tail_after_next"],
        ]
    )


def signless_formula(row: dict[str, str]) -> str:
    return "|".join([row["prev_before_002"], "002-390", row["next_after_390"], row["tail_after_next"]])


def source_tier(row: dict[str, str]) -> str:
    if row.get("strict_source_visible") == "True":
        return "strict_source_visible"
    if row.get("permissive_public_panel") == "True":
        return "permissive_public_panel"
    return "source_dark_or_weak"


def main() -> None:
    rows = read_rows()
    matrix_rows = []
    for r in rows:
        matrix_rows.append(
            {
                "object": obj(r),
                "prev_before_002": r["prev_before_002"],
                "frame": "002-390",
                "branch_after_390": r["next_after_390"],
                "tail_after_branch": r["tail_after_next"],
                "terminal_after_branch": str(r["tail_after_next"] == "<END>"),
                "source_tier": source_tier(r),
                "family_cell": family_cell(r),
                "signless_formula": signless_formula(r),
                "text": r["text"],
                "site": r["site"],
                "type": r["type"],
                "symbol": r["symbol"],
                "cult": r["cult"],
            }
        )

    by_branch: dict[str, list[dict[str, object]]] = defaultdict(list)
    for r in matrix_rows:
        by_branch[str(r["branch_after_390"])].append(r)

    branch_rows = []
    for branch, group in sorted(by_branch.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        strict = [g for g in group if g["source_tier"] == "strict_source_visible"]
        permissive = [g for g in group if g["source_tier"] in {"strict_source_visible", "permissive_public_panel"}]
        terminals = [g for g in group if g["terminal_after_branch"] == "True"]
        family_cells = sorted({str(g["family_cell"]) for g in group})
        strict_family_cells = sorted({str(g["family_cell"]) for g in strict})
        strict_prev = sorted({str(g["prev_before_002"]) for g in strict})
        tails = sorted({str(g["tail_after_branch"]) for g in group})
        if branch == "125":
            verdict = "top_live_branch_but_broad_register_limited; continuation-bearing in all four local rows"
        elif branch in {"095", "692"} and strict:
            verdict = "strict_visible_non125_control; terminal in current visible rows"
        elif branch == "705":
            verdict = "repeated_non125_candidate_but_source_dark"
        else:
            verdict = "singleton_or_source_limited"
        branch_rows.append(
            {
                "branch_after_390": branch,
                "raw_rows": len(group),
                "objects": " ".join(str(g["object"]) for g in group),
                "terminal_rows": len(terminals),
                "terminal_objects": " ".join(str(g["object"]) for g in terminals),
                "tails": " | ".join(tails),
                "family_cells": len(family_cells),
                "strict_source_visible_rows": len(strict),
                "strict_source_visible_objects": " ".join(str(g["object"]) for g in strict),
                "strict_source_visible_family_cells": len(strict_family_cells),
                "strict_prev_before_002_values": " ".join(strict_prev),
                "permissive_public_rows": len(permissive),
                "permissive_public_objects": " ".join(str(g["object"]) for g in permissive),
                "verdict": verdict,
            }
        )

    prev_rows = []
    by_prev: dict[str, list[dict[str, object]]] = defaultdict(list)
    for r in matrix_rows:
        by_prev[str(r["prev_before_002"])].append(r)
    for prev, group in sorted(by_prev.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        branches = sorted({str(g["branch_after_390"]) for g in group})
        strict = [g for g in group if g["source_tier"] == "strict_source_visible"]
        prev_rows.append(
            {
                "prev_before_002": prev,
                "raw_rows": len(group),
                "branches_after_390": " ".join(branches),
                "objects": " ".join(str(g["object"]) for g in group),
                "strict_source_visible_objects": " ".join(str(g["object"]) for g in strict),
                "verdict": (
                    "live_prev_conditioner_candidate"
                    if len(group) > 1 or strict
                    else "singleton_prev_conditioner_not_promoted"
                ),
            }
        )

    decision_rows = [
        {
            "decision": "125_continuation_bearing",
            "evidence": "All four local 125 rows are nonterminal after 125; strict visible M-119/M-735 have different prev/tail families.",
            "limit": "Strict evidence remains two Mohenjo-daro square steatite SEAL:S rows; M-38 weak; Sktd-1 downweighted.",
        },
        {
            "decision": "non125_visible_controls_terminal",
            "evidence": "Strict visible M-70(692) and M-71(095) are terminal after their branch sign.",
            "limit": "They are not matched prev-frame controls against M-119/M-735.",
        },
        {
            "decision": "705_missing_repeated_control",
            "evidence": "Two local 705 rows exist and both terminal.",
            "limit": "Both are source-dark/unresolved, so 705 cannot yet decide branch ecology.",
        },
        {
            "decision": "prev_conditioning_unproven",
            "evidence": "235 links weak M-38 and strict M-735 to 125; 004 would split 095/125 if H-1993 routes.",
            "limit": "Current strict source-visible layer does not yet have matched PREV -> 002-390 -> X alternatives.",
        },
    ]

    write_csv(REPORT_DIR / f"{PREFIX}_matrix_rows.csv", matrix_rows)
    write_csv(REPORT_DIR / f"{PREFIX}_branch_summary.csv", branch_rows)
    write_csv(REPORT_DIR / f"{PREFIX}_prev_summary.csv", prev_rows)
    write_csv(REPORT_DIR / f"{PREFIX}_decisions.csv", decision_rows)

    summary = {
        "date": DATE,
        "row_count": len(matrix_rows),
        "branch_count": len(branch_rows),
        "top_branch": "125",
        "strict_visible_125_objects": ["M-119", "M-735"],
        "strict_visible_non125_objects": ["M-70", "M-71"],
        "decision": "family_collapsed_branch_ecology_keeps_125_live_but_not_readable",
        "doc": str(DOC_DIR / f"{PREFIX}.md"),
    }
    (REPORT_DIR / f"{PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    branch_lines = "\n".join(
        f"- `{r['branch_after_390']}`: raw {r['raw_rows']}, family cells {r['family_cells']}, strict visible {r['strict_source_visible_objects'] or 'none'}, tails `{r['tails']}`. {r['verdict']}"
        for r in branch_rows
    )
    prev_lines = "\n".join(
        f"- `{r['prev_before_002']}`: branches {r['branches_after_390']}; objects {r['objects']}; strict visible {r['strict_source_visible_objects'] or 'none'}"
        for r in prev_rows[:12]
    )
    decision_lines = "\n".join(
        f"- `{r['decision']}`: {r['evidence']} Limit: {r['limit']}" for r in decision_rows
    )
    text = dedent(
        f"""\
        # 032-002-861 / 002-390-X Family-Collapsed Branch Ecology

        Date: {DATE}

        ## Question

        After source route, boxed-window, and exact-family stress, what does the `PREV -> 002-390 -> X -> TAIL` ecology actually say?

        ## Result

        `125` remains the top live branch, but only as a branch-ecology object. It is not readable.

        The important contrast is behavioral: all local `125` rows continue after `125`, while the current strict visible non-`125` controls `M-70(692)` and `M-71(095)` close after the branch sign. That makes `125` look continuation-bearing. The limit is that strict `125` support is still only `M-119/M-735`, both in the broad Mohenjo-daro square steatite `SEAL:S` register.

        ## Branch Summary

        {branch_lines}

        ## Previous-Sign Summary

        {prev_lines}

        ## Decisions

        {decision_lines}

        ## Linguistic Decision

        Keep `125` live as a continuation-bearing branch candidate after `002-390`. Do not promote it to a value or function.

        The next decisive acquisition is not another `125` argument. It is source-visible matched alternatives: route `705`, route `H-1993`, and seek same-`PREV` non-`125` rows. If non-`125` branches also continue under matched source/family conditions, the continuation-bearing reading demotes.

        Accepted value, phonetics, language identity, sign meaning, and translation remain `0`.
        """
    )
    text = "\n".join(line[8:] if line.startswith("        ") else line for line in text.splitlines()) + "\n"
    doc = DOC_DIR / f"{PREFIX}.md"
    doc.write_text(text, encoding="utf-8")
    print(json.dumps({**summary, "doc": str(doc)}, indent=2))


if __name__ == "__main__":
    main()
