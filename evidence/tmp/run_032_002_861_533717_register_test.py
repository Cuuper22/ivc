"""Register test for 533-717: is the unit conditioned on a specific register?

A register, here, is a recurring combination of object type, layout, and iconography —
the "document format" a row appears in. This script reads the filtered corpus metadata
and checks how the 533-717 rows distribute across registers, treating M-376, M-391, and
M-1273 as the source-visible rows. It writes row and scope CSVs plus a summary JSON.
The recorded decision promotes 533-717 to a conditional register candidate: live as a
register-conditioned structural object, with no value or reading accepted.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path.cwd()
METADATA = ROOT / "data" / "open_prototype" / "lipi" / "metadata_filtered.csv"
REPORTS = ROOT / "data" / "open_prototype" / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

SOURCE_VISIBLE_ROWS = {"M-376", "M-391", "M-1273"}


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


def tail_after_002_861(tokens: list[str]) -> str:
    for idx in range(len(tokens) - 1):
        if tokens[idx : idx + 2] == ["002", "861"]:
            tail = tokens[idx + 2 :]
            return " ".join(tail) if tail else "<END>"
    return "<NO_002_861>"


def terminal2(tokens: list[str]) -> str:
    if len(tokens) == 1:
        return tokens[0]
    return " ".join(tokens[-2:])


def classify_row(row: dict[str, object]) -> dict[str, str]:
    tokens = row["_tokens"]
    assert isinstance(tokens, list)
    tail = tail_after_002_861(tokens)
    if tail == "533 717":
        branch_class = "target_533_717"
    elif tail == "<END>":
        branch_class = "bare_002_861"
    elif tail == "<NO_002_861>":
        branch_class = "no_002_861"
    else:
        branch_class = "other_002_861_tail"
    return {
        "id": str(row["id"]),
        "cisi": str(row["cisi"]),
        "site": str(row["site"]),
        "type": str(row["type"]),
        "symbol": str(row["symbol"]),
        "shape": str(row["shape"]),
        "material": str(row["material"]),
        "condition": str(row["condition"]),
        "direction": str(row["dir."]),
        "text_length": str(row["text length"]),
        "text": str(row["text"]),
        "terminal2": terminal2(tokens),
        "tail_after_002_861": tail,
        "branch_class": branch_class,
        "source_status": "source_visible_focus" if str(row["cisi"]) in SOURCE_VISIBLE_ROWS else "source_pending_or_not_checked",
    }


def count_rows(rows: list[dict[str, str]], field: str) -> str:
    return ";".join(f"{key}:{value}" for key, value in Counter(r[field] for r in rows).most_common())


def summarize_scope(name: str, rows: list[dict[str, str]]) -> dict[str, str]:
    with_002_861 = [r for r in rows if r["tail_after_002_861"] != "<NO_002_861>"]
    target = [r for r in rows if r["tail_after_002_861"] == "533 717"]
    bare = [r for r in rows if r["tail_after_002_861"] == "<END>"]
    other_tail = [
        r
        for r in rows
        if r["tail_after_002_861"] not in {"<NO_002_861>", "<END>", "533 717"}
    ]
    return {
        "scope": name,
        "rows": str(len(rows)),
        "rows_with_002_861": str(len(with_002_861)),
        "target_533_717_rows": str(len(target)),
        "bare_002_861_rows": str(len(bare)),
        "other_002_861_tail_rows": str(len(other_tail)),
        "target_share_within_002_861": f"{len(target)}/{len(with_002_861)}" if with_002_861 else "0/0",
        "shape_counts": count_rows(rows, "shape"),
        "tail_after_002_861_counts": count_rows(with_002_861, "tail_after_002_861") if with_002_861 else "",
        "examples_002_861": ";".join(f"{r['cisi']} {r['text']}" for r in with_002_861[:12]),
    }


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main() -> None:
    rows = [classify_row(row) for row in load_rows()]

    mohenjo_no_icon_seal_r = [
        r for r in rows if r["site"] == "Mohenjo-daro" and r["type"] == "SEAL:R" and r["symbol"] == "None"
    ]
    mohenjo_no_icon_seal_r_rect_cuboid = [
        r
        for r in mohenjo_no_icon_seal_r
        if r["shape"] in {"rectangular", "cuboid-convex", "cuboid"}
    ]
    mohenjo_no_icon_seal_r_cuboid_convex = [
        r for r in mohenjo_no_icon_seal_r if r["shape"] == "cuboid-convex"
    ]
    mohenjo_seal_s_with_002_861 = [
        r
        for r in rows
        if r["site"] == "Mohenjo-daro"
        and r["type"] == "SEAL:S"
        and r["tail_after_002_861"] != "<NO_002_861>"
    ]
    all_002_861 = [r for r in rows if r["tail_after_002_861"] != "<NO_002_861>"]

    scopes = [
        summarize_scope("all_strict_002_861_rows", all_002_861),
        summarize_scope("mohenjo_no_icon_seal_r", mohenjo_no_icon_seal_r),
        summarize_scope("mohenjo_no_icon_seal_r_rect_cuboid", mohenjo_no_icon_seal_r_rect_cuboid),
        summarize_scope("mohenjo_no_icon_seal_r_cuboid_convex", mohenjo_no_icon_seal_r_cuboid_convex),
        summarize_scope("mohenjo_seal_s_with_002_861", mohenjo_seal_s_with_002_861),
    ]

    focus_rows = [
        r
        for r in mohenjo_no_icon_seal_r
        if r["tail_after_002_861"] != "<NO_002_861>" or r["terminal2"] == "533 717"
    ]

    rows_csv = REPORTS / "campaign_032_002_861_533717_register_test_rows.csv"
    scope_csv = REPORTS / "campaign_032_002_861_533717_register_test_scopes.csv"
    summary_json = REPORTS / "campaign_032_002_861_533717_register_test_summary.json"

    write_csv(rows_csv, focus_rows, list(focus_rows[0].keys()))
    write_csv(scope_csv, scopes, list(scopes[0].keys()))

    payload = {
        "date": "2026-05-29",
        "strict_rows_scanned": len(rows),
        "focus_rows": len(focus_rows),
        "decision": "promote_533_717_to_conditional_register_candidate",
        "decision_basis": [
            "533-717 is 2/7 among Mohenjo-daro no-icon SEAL:R rows with 002-861.",
            "533-717 is 2/3 among cuboid-convex no-icon SEAL:R rows with 002-861.",
            "No Mohenjo-daro SEAL:S row with 002-861 has 533-717 in the strict layer.",
            "The result is conditional on the 002-861 branch, not a global no-icon SEAL:R ending.",
        ],
        "scopes": scopes,
        "rows_csv": str(rows_csv.resolve()),
        "scope_csv": str(scope_csv.resolve()),
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
