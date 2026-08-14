"""Slot-substitution test for sign 603 across structural slots.

This script reads the filtered corpus metadata, keeps clean strict rows (bracketed by
+ with all three-digit tokens and no damage markers), and builds slot tables: which
signs occupy the slots where 603 appears, and what follows in the post-tail position.
The question is whether 603 substitutes into the same slots as its comparators — a
cross-slot bridge — or whether the apparent bridge is just a shared line template
repeating itself. It writes slot, post-tail, and matrix CSVs plus a summary JSON. The
recorded decision: the 603 cross-slot bridge survives but is under template attack,
so it stays a structural candidate with no value accepted.
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


def joined_counts(values: list[str], topn: int = 12) -> str:
    return ";".join(f"{key}:{value}" for key, value in Counter(values).most_common(topn))


def tail_after_002_861(tokens: list[str]) -> list[str] | None:
    for idx in range(len(tokens) - 1):
        if tokens[idx : idx + 2] == ["002", "861"]:
            return tokens[idx + 2 :]
    return None


def row_base(row: dict[str, object]) -> dict[str, str]:
    return {
        "id": str(row["id"]),
        "cisi": str(row["cisi"]),
        "site": str(row["site"]),
        "type": str(row["type"]),
        "symbol": str(row["symbol"]),
        "shape": str(row["shape"]),
        "class": str(row["class"]),
        "material": str(row["material"]),
        "condition": str(row["condition"]),
        "text_length": str(row["text length"]),
        "text": str(row["text"]),
        "register_key": "|".join([str(row["site"]), str(row["type"]), str(row["symbol"]), str(row["shape"])]),
    }


def collect_slot_rows(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        tokens = row["_tokens"]
        assert isinstance(tokens, list)
        for idx in range(len(tokens) - 4):
            if tokens[idx] == "740" and tokens[idx + 2 : idx + 5] == ["240", "060", "692"]:
                record = row_base(row)
                record.update(
                    {
                        "slot_x": tokens[idx + 1],
                        "slot_pattern": "740-X-240-060-692",
                        "slot_index_0based": str(idx + 1),
                        "slot_position": "medial" if idx + 4 < len(tokens) - 1 else "near_terminal_formula",
                        "prev2": " ".join(tokens[max(0, idx - 1) : idx + 1]) if idx else "<START> 740",
                        "next2_after_x": " ".join(tokens[idx + 2 : idx + 4]),
                    }
                )
                out.append(record)
    return out


def collect_post_tail_rows(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        tokens = row["_tokens"]
        assert isinstance(tokens, list)
        tail = tail_after_002_861(tokens)
        if tail is None:
            continue
        record = row_base(row)
        record.update(
            {
                "tail_after_002_861": " ".join(tail) if tail else "<END>",
                "tail_len": str(len(tail)),
                "tail_initial": tail[0] if tail else "<END>",
                "tail_position": "terminal_tail" if tail else "bare_terminal",
            }
        )
        out.append(record)
    return out


def summarize(slot_rows: list[dict[str, str]], post_tail_rows: list[dict[str, str]], strict_rows_scanned: int) -> dict[str, object]:
    by_x = defaultdict(list)
    for row in slot_rows:
        by_x[row["slot_x"]].append(row)

    post_by_initial = defaultdict(list)
    for row in post_tail_rows:
        post_by_initial[row["tail_initial"]].append(row)

    slot_signs = sorted(by_x)
    rows = []
    for sign in slot_signs:
        slot_group = by_x[sign]
        post_group = post_by_initial.get(sign, [])
        rows.append(
            {
                "sign": sign,
                "slot_740_x_240_060_692_rows": len(slot_group),
                "slot_exact_text_families": len({row["text"] for row in slot_group}),
                "slot_register_cells": len({row["register_key"] for row in slot_group}),
                "post_002_861_tail_initial_rows": len(post_group),
                "post_002_861_tail_full_families": len({row["tail_after_002_861"] for row in post_group}),
                "slot_examples": [f"{row['cisi']} {row['text']}" for row in slot_group],
                "post_examples": [f"{row['cisi']} {row['text']}" for row in post_group[:8]],
            }
        )

    payload = {
        "date": "2026-05-29",
        "strict_rows_scanned": strict_rows_scanned,
        "slot_pattern": "740-X-240-060-692",
        "slot_rows": len(slot_rows),
        "slot_x_counts": dict(Counter(row["slot_x"] for row in slot_rows)),
        "slot_register_counts": joined_counts([row["register_key"] for row in slot_rows]),
        "post_002_861_rows": len(post_tail_rows),
        "post_tail_initial_counts_for_slot_signs": {sign: len(post_by_initial.get(sign, [])) for sign in slot_signs},
        "matrix_rows": rows,
        "decision": "603_cross_slot_bridge_survives_but_is_under_template_attack",
        "decision_basis": [
            "603 appears in both the post-002-861 terminal tail slot and the Harappa 740-X-240-060-692 internal slot.",
            "Other observed X-slot values should be tested as controls; if they do not occur post-861, 603 is uniquely cross-slot in this small layer.",
            "The Harappa slot itself is still a copied/formula-family risk until source-normalized.",
        ],
    }
    return payload


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = load_rows()
    slot_rows = collect_slot_rows(rows)
    post_tail_rows = collect_post_tail_rows(rows)
    payload = summarize(slot_rows, post_tail_rows, len(rows))

    slot_csv = REPORTS / "campaign_032_002_861_603_slot_substitution_slot_rows.csv"
    post_csv = REPORTS / "campaign_032_002_861_603_slot_substitution_post_tail_rows.csv"
    matrix_csv = REPORTS / "campaign_032_002_861_603_slot_substitution_matrix.csv"
    summary_json = REPORTS / "campaign_032_002_861_603_slot_substitution_summary.json"

    write_csv(slot_csv, slot_rows)
    write_csv(post_csv, post_tail_rows)
    matrix_rows = [
        {
            "sign": row["sign"],
            "slot_740_x_240_060_692_rows": str(row["slot_740_x_240_060_692_rows"]),
            "slot_exact_text_families": str(row["slot_exact_text_families"]),
            "slot_register_cells": str(row["slot_register_cells"]),
            "post_002_861_tail_initial_rows": str(row["post_002_861_tail_initial_rows"]),
            "post_002_861_tail_full_families": str(row["post_002_861_tail_full_families"]),
            "slot_examples": ";".join(row["slot_examples"]),
            "post_examples": ";".join(row["post_examples"]),
        }
        for row in payload["matrix_rows"]
    ]
    write_csv(matrix_csv, matrix_rows)
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
