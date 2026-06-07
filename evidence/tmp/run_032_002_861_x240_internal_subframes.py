from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path.cwd()
METADATA = ROOT / "data" / "open_prototype" / "lipi" / "metadata_filtered.csv"
REPORTS = ROOT / "data" / "open_prototype" / "reports"
DOCS = ROOT / "docs"
REPORTS.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)

FRAME_PREFIXES = ("740", "690", "000")


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


def register_key(row: dict[str, object]) -> str:
    return "|".join([str(row["site"]), str(row["type"]), str(row["symbol"]), str(row["shape"])])


def joined_counts(values: list[str], topn: int = 10) -> str:
    return ";".join(f"{key}:{value}" for key, value in Counter(values).most_common(topn))


def compact_examples(rows: list[dict[str, str]], limit: int = 8) -> str:
    return ";".join(f"{row['cisi']} {row['text']}" for row in rows[:limit])


def collect(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        tokens = row["_tokens"]
        assert isinstance(tokens, list)
        for idx in range(1, len(tokens) - 1):
            if tokens[idx - 1] not in FRAME_PREFIXES or tokens[idx + 1] != "240":
                continue
            after_240 = tokens[idx + 2 :]
            out.append(
                {
                    "x_sign": tokens[idx],
                    "prefix": tokens[idx - 1],
                    "frame": f"{tokens[idx - 1]}_X_240",
                    "after_240_len": str(len(after_240)),
                    "after_240": " ".join(after_240) if after_240 else "<END>",
                    "after_240_first": after_240[0] if after_240 else "<END>",
                    "after_240_first2": " ".join(after_240[:2]) if len(after_240) >= 2 else after_240[0] if after_240 else "<END>",
                    "after_240_first3": " ".join(after_240[:3])
                    if len(after_240) >= 3
                    else " ".join(after_240) if after_240 else "<END>",
                    "cisi": str(row["cisi"]),
                    "site": str(row["site"]),
                    "type": str(row["type"]),
                    "symbol": str(row["symbol"]),
                    "shape": str(row["shape"]),
                    "material": str(row["material"]),
                    "class": str(row["class"]),
                    "condition": str(row["condition"]),
                    "dir": str(row["dir."]),
                    "text_length": str(row["text length"]),
                    "text": str(row["text"]),
                    "register_key": register_key(row),
                    "formula_key": str(row["text"]),
                }
            )
    return out


def summarize_by_after(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row["after_240_first3"]].append(row)
    out: list[dict[str, str]] = []
    for after, group in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0])):
        out.append(
            {
                "after_240_first3": after,
                "rows": str(len(group)),
                "x_signs": joined_counts([row["x_sign"] for row in group]),
                "prefixes": joined_counts([row["prefix"] for row in group]),
                "register_cells": str(len({row["register_key"] for row in group})),
                "formula_families": str(len({row["formula_key"] for row in group})),
                "examples": compact_examples(group),
            }
        )
    return out


def summarize_by_x(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[row["x_sign"]].append(row)
    out: list[dict[str, str]] = []
    for x, group in sorted(groups.items(), key=lambda item: (-len(item[1]), item[0])):
        after_counts = Counter(row["after_240_first3"] for row in group)
        out.append(
            {
                "x_sign": x,
                "rows": str(len(group)),
                "register_cells": str(len({row["register_key"] for row in group})),
                "formula_families": str(len({row["formula_key"] for row in group})),
                "prefixes": joined_counts([row["prefix"] for row in group]),
                "after_240_first3_counts": ";".join(f"{key}:{value}" for key, value in after_counts.most_common()),
                "examples": compact_examples(group),
            }
        )
    return out


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, after_summary: list[dict[str, str]], x_summary: list[dict[str, str]], rows: list[dict[str, str]]) -> None:
    exact_060_692 = [row for row in rows if row["after_240_first3"] == "060 692"]
    lines = [
        "# Campaign 032 X-Before-240 Internal Subframes",
        "",
        "Date: 2026-05-29",
        "",
        "Question: inside X-before-240, is `240-060-692` a real subframe and does it isolate the `603/636/642` slot family?",
        "",
        "Method: strict complete-token rows only; no bracketed or parenthesized readings; deduplicated by `(cisi, site, type, symbol, text)`.",
        "",
        f"X-before-240 rows: `{len(rows)}`.",
        f"`240-060-692` rows: `{len(exact_060_692)}`.",
        "",
        "## Decision",
        "",
        "`240-060-692` is a compact subframe of X-before-240. In this strict layer it contains only `603`, `636`, and `642`, making the original slot-family contrast a count-supported subframe object. This does not make any X value readable.",
        "",
        "## After-240 Subframes",
        "",
        "| after 240 | rows | X signs | prefixes | registers | formula families | examples |",
        "|---|---:|---|---|---:|---:|---|",
    ]
    for row in after_summary:
        lines.append(
            "| {after_240_first3} | {rows} | {x_signs} | {prefixes} | {register_cells} | {formula_families} | {examples} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## X Profiles",
            "",
            "| X | rows | registers | formula families | prefixes | after-240 counts | examples |",
            "|---|---:|---:|---:|---|---|---|",
        ]
    )
    for row in x_summary:
        lines.append(
            "| {x_sign} | {rows} | {register_cells} | {formula_families} | {prefixes} | {after_240_first3_counts} | {examples} |".format(
                **row
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    strict_rows = load_rows()
    rows = collect(strict_rows)
    after_summary = summarize_by_after(rows)
    x_summary = summarize_by_x(rows)

    write_csv(REPORTS / "campaign_032_002_861_x240_internal_subframes_rows.csv", rows)
    write_csv(REPORTS / "campaign_032_002_861_x240_internal_subframes_after_summary.csv", after_summary)
    write_csv(REPORTS / "campaign_032_002_861_x240_internal_subframes_x_summary.csv", x_summary)
    payload = {
        "date": "2026-05-29",
        "strict_rows_scanned": len(strict_rows),
        "x240_rows": len(rows),
        "after_240_subframes": after_summary,
        "x_profiles": x_summary,
        "decision": "240_060_692_is_compact_subframe_with_603_636_642_only_in_current_strict_layer",
    }
    (REPORTS / "campaign_032_002_861_x240_internal_subframes_summary.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    write_markdown(DOCS / "campaign_032_002_861_x240_internal_subframes.md", after_summary, x_summary, rows)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
