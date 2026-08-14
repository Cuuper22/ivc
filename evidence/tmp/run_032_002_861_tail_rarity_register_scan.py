"""Test whether rare tails after 002-861 are just artifacts of narrow registers.

The worry: a tail that always appears on one kind of object (say, Mohenjo-daro
no-icon SEAL:R seals) may mark the object class, not the language. This script
extracts every post-002-861 occurrence from the strict corpus, tags each with
its register (site, type, symbol, shape) and a family key, and flags "perfect
small register cells" — tails with three or fewer rows all in a single
register, which look clean but prove nothing. It then zooms in on the
Mohenjo-daro no-icon SEAL:R focus register to show it splits into bare,
533-717, 603, and a long tail. Writes occurrence and tail-summary CSVs for
the full field and the focus register, plus a JSON payload recording the
decision that 533-717 is a subclass/apposition candidate, not a whole-register
marker.
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

SOURCE_VISIBLE = {
    "M-355",
    "M-376",
    "M-391",
    "M-1267",
    "M-1273",
}
SOURCE_PENDING = {"M-1954", "M-1973"}


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


def tail_after_002_861(tokens: list[str]) -> tuple[int, str] | None:
    for idx in range(len(tokens) - 1):
        if tokens[idx : idx + 2] == ["002", "861"]:
            tail = tokens[idx + 2 :]
            return idx, " ".join(tail) if tail else "<END>"
    return None


def family_key(row: dict[str, str]) -> str:
    return "|".join(
        [
            row["site"],
            row["type"],
            row["symbol"],
            row["shape"],
            row["tail_after_002_861"],
            row["prefix_before_002_861_last2"],
        ]
    )


def joined_counts(values: list[str], topn: int = 10) -> str:
    return ";".join(f"{key}:{value}" for key, value in Counter(values).most_common(topn))


def make_occurrences(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        tokens = row["_tokens"]
        assert isinstance(tokens, list)
        hit = tail_after_002_861(tokens)
        if hit is None:
            continue
        idx, tail = hit
        cisi = str(row["cisi"])
        prefix = tokens[:idx]
        suffix = tokens[idx + 2 :]
        out.append(
            {
                "id": str(row["id"]),
                "cisi": cisi,
                "site": str(row["site"]),
                "type": str(row["type"]),
                "symbol": str(row["symbol"]),
                "shape": str(row["shape"]),
                "material": str(row["material"]),
                "condition": str(row["condition"]),
                "direction": str(row["dir."]),
                "text_length": str(row["text length"]),
                "text": str(row["text"]),
                "prefix_before_002_861": " ".join(prefix) if prefix else "<START>",
                "prefix_before_002_861_last1": prefix[-1] if prefix else "<START>",
                "prefix_before_002_861_last2": " ".join(prefix[-2:]) if len(prefix) >= 2 else " ".join(prefix) if prefix else "<START>",
                "tail_after_002_861": tail,
                "tail_len": str(len(suffix)),
                "terminal_after_tail": "true",
                "source_status": "source_visible" if cisi in SOURCE_VISIBLE else "source_pending_target" if cisi in SOURCE_PENDING else "source_pending_or_not_checked",
                "is_mohenjo_no_icon_seal_r": str(
                    row["site"] == "Mohenjo-daro" and row["type"] == "SEAL:R" and row["symbol"] == "None"
                ).lower(),
            }
        )
    for item in out:
        item["family_key"] = family_key(item)
    return out


def summarize_tails(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_tail: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_tail[row["tail_after_002_861"]].append(row)

    summary: list[dict[str, str]] = []
    for tail, group in sorted(by_tail.items(), key=lambda item: (-len(item[1]), item[0])):
        mohenjo_no_icon = [row for row in group if row["is_mohenjo_no_icon_seal_r"] == "true"]
        register_counts = Counter(f"{row['site']}|{row['type']}|{row['symbol']}|{row['shape']}" for row in group)
        perfect_small_cell = len(group) <= 3 and len(register_counts) == 1
        summary.append(
            {
                "tail_after_002_861": tail,
                "rows": str(len(group)),
                "source_visible_rows": str(sum(row["source_status"] == "source_visible" for row in group)),
                "family_key_count": str(len({row["family_key"] for row in group})),
                "mohenjo_no_icon_seal_r_rows": str(len(mohenjo_no_icon)),
                "perfect_small_register_cell": str(perfect_small_cell).lower(),
                "site_counts": joined_counts([row["site"] for row in group]),
                "type_counts": joined_counts([row["type"] for row in group]),
                "symbol_counts": joined_counts([row["symbol"] for row in group]),
                "shape_counts": joined_counts([row["shape"] for row in group]),
                "length_counts": joined_counts([row["text_length"] for row in group]),
                "prefix_last2_counts": joined_counts([row["prefix_before_002_861_last2"] for row in group]),
                "source_status_counts": joined_counts([row["source_status"] for row in group]),
                "examples": ";".join(f"{row['cisi']} {row['text']}" for row in group[:10]),
            }
        )
    return summary


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main() -> None:
    corpus_rows = load_rows()
    occurrences = make_occurrences(corpus_rows)
    tails = summarize_tails(occurrences)
    focus = [
        row
        for row in occurrences
        if row["site"] == "Mohenjo-daro" and row["type"] == "SEAL:R" and row["symbol"] == "None"
    ]
    focus_summary = summarize_tails(focus)
    small_cells = [row for row in tails if row["perfect_small_register_cell"] == "true"]

    rows_csv = REPORTS / "campaign_032_002_861_tail_rarity_register_scan_rows.csv"
    tail_csv = REPORTS / "campaign_032_002_861_tail_rarity_register_scan_tail_summary.csv"
    focus_csv = REPORTS / "campaign_032_002_861_tail_rarity_register_scan_focus_rows.csv"
    focus_summary_csv = REPORTS / "campaign_032_002_861_tail_rarity_register_scan_focus_summary.csv"
    summary_json = REPORTS / "campaign_032_002_861_tail_rarity_register_scan_summary.json"

    write_csv(rows_csv, occurrences, list(occurrences[0].keys()))
    write_csv(tail_csv, tails, list(tails[0].keys()))
    write_csv(focus_csv, focus, list(focus[0].keys()))
    write_csv(focus_summary_csv, focus_summary, list(focus_summary[0].keys()))

    payload = {
        "date": "2026-05-29",
        "strict_rows_scanned": len(corpus_rows),
        "rows_with_002_861": len(occurrences),
        "tail_family_count": len(tails),
        "mohenjo_no_icon_seal_r_002_861_rows": len(focus),
        "mohenjo_no_icon_seal_r_tail_distribution": {
            row["tail_after_002_861"]: int(row["rows"]) for row in focus_summary
        },
        "small_perfect_register_cells": len(small_cells),
        "533_717_decision": "narrow_to_subclass_or_apposition_candidate_not_whole_register_marker",
        "decision_basis": [
            "Mohenjo-daro no-icon SEAL:R with 002-861 splits into bare, 533-717, 603, and a long tail.",
            "M-355 is a cuboid-convex same-register hostile comparator with a different post-861 tail.",
            "M-1267 and M-1273 are now source-visible controls; M-1954 and M-1973 remain source-pending.",
            "The broad scan exposes other small perfect-looking tail/register cells, so 533-717 must survive family-blocked and source-visible contrasts before value work.",
        ],
        "outputs": {
            "rows_csv": str(rows_csv.resolve()),
            "tail_summary_csv": str(tail_csv.resolve()),
            "focus_rows_csv": str(focus_csv.resolve()),
            "focus_summary_csv": str(focus_summary_csv.resolve()),
        },
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
