"""Split occurrences of six candidate units by what comes before them.

The question: does a unit like "603" behave differently when it follows the
002-861 pair than when it follows some other 861 or stands on its own? We read
the strict Lipi corpus (metadata_filtered.csv), keep only clean fully-numeric
inscriptions, and find every occurrence of the six units listed in UNITS. Each
occurrence gets a context class — post_002_861, post_other_861, or independent
— plus its site, artifact type, neighbors, and companion inscriptions on the
same object. We write one CSV of raw occurrences, one CSV of per-unit
summaries, and a JSON summary that also records the working research decision
for each unit (which are P1 targets, which are controls).
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path.cwd()
METADATA = ROOT / "data" / "open_prototype" / "lipi" / "metadata_filtered.csv"
REPORTS = ROOT / "data" / "open_prototype" / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

UNITS = ["603", "533 717", "255 416", "096", "416", "698"]
SOURCE_VISIBLE_POST_861 = {"M-91", "M-240", "M-714", "M-376", "M-391", "M-1273"}
SOURCE_VISIBLE_BARE = {"H-444", "M-723", "M-1044", "M-77", "M-118", "M-15"}


def parse_tokens(text: str) -> list[str] | None:
    if not (text.startswith("+") and text.endswith("+")):
        return None
    if any(ch in text for ch in "[]()"):
        return None
    tokens = [token for token in text.strip("+").split("-") if token]
    if not tokens or not all(re.fullmatch(r"\d{3}", token) for token in tokens):
        return None
    return tokens


def load_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    seen = set()
    with METADATA.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            tokens = parse_tokens(row["text"])
            if tokens is None:
                continue
            key = (row["cisi"], row["site"], row["type"], row["symbol"], row["text"])
            if key in seen:
                continue
            seen.add(key)
            out: dict[str, object] = dict(row)
            out["_tokens"] = tokens
            rows.append(out)
    return rows


def companion_rows(rows: list[dict[str, object]]) -> dict[str, list[dict[str, object]]]:
    by_cisi: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        cisi = str(row["cisi"])
        if cisi and cisi != "-":
            by_cisi[cisi].append(row)
    return by_cisi


def context_class(prev2: str, prev1: str) -> str:
    if prev2 == "002 861":
        return "post_002_861"
    if prev1 == "861":
        return "post_other_861"
    return "independent"


def find_occurrences(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    by_cisi = companion_rows(rows)
    out: list[dict[str, str]] = []
    for row in rows:
        tokens = row["_tokens"]
        assert isinstance(tokens, list)
        for unit in UNITS:
            unit_tokens = unit.split()
            for idx in range(0, len(tokens) - len(unit_tokens) + 1):
                if tokens[idx : idx + len(unit_tokens)] != unit_tokens:
                    continue
                prev1 = tokens[idx - 1] if idx else "<START>"
                prev2 = " ".join(tokens[max(0, idx - 2) : idx]) if idx else "<START>"
                next1 = tokens[idx + len(unit_tokens)] if idx + len(unit_tokens) < len(tokens) else "<END>"
                cisi = str(row["cisi"])
                companions = [
                    str(other["text"])
                    for other in by_cisi[cisi]
                    if str(other["id"]) != str(row["id"]) or str(other["text"]) != str(row["text"])
                ]
                out.append(
                    {
                        "unit": unit,
                        "context_class": context_class(prev2, prev1),
                        "id": str(row["id"]),
                        "cisi": cisi,
                        "site": str(row["site"]),
                        "type": str(row["type"]),
                        "symbol": str(row["symbol"]),
                        "material": str(row["material"]),
                        "shape": str(row["shape"]),
                        "sides": str(row["sides"]),
                        "class": str(row["class"]),
                        "direction": str(row["dir."]),
                        "text_length": str(row["text length"]),
                        "text": str(row["text"]),
                        "unit_index": str(idx),
                        "prev1": prev1,
                        "prev2": prev2,
                        "next1": next1,
                        "unit_terminal": str(next1 == "<END>").lower(),
                        "source_visible_post_861_focus": str(cisi in SOURCE_VISIBLE_POST_861).lower(),
                        "source_visible_bare_control_for_lane": str(cisi in SOURCE_VISIBLE_BARE).lower(),
                        "companion_rows": " | ".join(companions),
                    }
                )
    return out


def joined_counts(values: list[str], topn: int = 8) -> str:
    return ";".join(f"{k}:{v}" for k, v in Counter(values).most_common(topn))


def summarize(occurrences: list[dict[str, str]]) -> list[dict[str, str]]:
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in occurrences:
        groups[(row["unit"], row["context_class"])].append(row)

    summaries: list[dict[str, str]] = []
    for unit in UNITS:
        for klass in ["post_002_861", "post_other_861", "independent"]:
            rows = groups.get((unit, klass), [])
            if not rows:
                continue
            summaries.append(
                {
                    "unit": unit,
                    "context_class": klass,
                    "rows": str(len(rows)),
                    "terminal_rows": str(sum(1 for r in rows if r["unit_terminal"] == "true")),
                    "source_visible_focus_rows": str(
                        sum(1 for r in rows if r["source_visible_post_861_focus"] == "true")
                    ),
                    "site_counts": joined_counts([r["site"] for r in rows]),
                    "type_counts": joined_counts([r["type"] for r in rows]),
                    "symbol_counts": joined_counts([r["symbol"] for r in rows]),
                    "shape_counts": joined_counts([r["shape"] for r in rows]),
                    "material_counts": joined_counts([r["material"] for r in rows]),
                    "prev2_counts": joined_counts([r["prev2"] for r in rows]),
                    "next1_counts": joined_counts([r["next1"] for r in rows]),
                    "companion_patterns": joined_counts([r["companion_rows"] or "<none>" for r in rows]),
                    "examples": ";".join(f"{r['cisi']} {r['text']}" for r in rows[:8]),
                }
            )
    return summaries


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main() -> None:
    rows = load_rows()
    occurrences = find_occurrences(rows)
    summaries = summarize(occurrences)

    occ_csv = REPORTS / "campaign_032_002_861_context_split_occurrences.csv"
    summary_csv = REPORTS / "campaign_032_002_861_context_split_summary.csv"
    summary_json = REPORTS / "campaign_032_002_861_context_split_summary.json"

    write_csv(occ_csv, occurrences, list(occurrences[0].keys()))
    write_csv(summary_csv, summaries, list(summaries[0].keys()))

    by_unit = defaultdict(list)
    for row in summaries:
        by_unit[row["unit"]].append(row)

    decisions = {
        "533 717": "P1 restricted post-861 target: both current occurrences are terminal after 002-861, both are Mohenjo-daro SEAL:R with no icon, and no independent occurrence appears in the strict layer.",
        "603": "P1 mixed bridge target: three terminal post-002-861 uses on Mohenjo-daro seals, plus three repeated Harappa TAB:B independent uses in the 740-603-240-060-692 lane and one weak scene occurrence.",
        "255 416": "P2 singleton stress: one terminal post-002-861 use in the 220-032 lane, supported by source-visible bare controls but not recurrent enough to carry the parse.",
        "096": "control only: one post-002-861 ivory rod plus one independent terminal row.",
        "416": "negative/broad control: many independent uses and Harappa TAB:I post-861 rows, not a restricted suffix signal.",
        "698": "negative/broad control: terminal sign with independent uses and two post-002-861 Mohenjo-daro seal rows.",
    }

    payload = {
        "date": "2026-05-29",
        "strict_corpus_rows_scanned": len(rows),
        "units": UNITS,
        "occurrence_rows": len(occurrences),
        "summary_rows": len(summaries),
        "research_decisions": decisions,
        "unit_contexts": by_unit,
        "occurrences_csv": str(occ_csv.resolve()),
        "summary_csv": str(summary_csv.resolve()),
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
