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
OUT_PREFIX = "campaign_032_002_861_533717_component_ecology"


def parse_tokens(text: str) -> list[str] | None:
    if not (text.startswith("+") and text.endswith("+")):
        return None
    if any(ch in text for ch in "[]()"):
        return None
    tokens = [token for token in text.strip("+").split("-") if token]
    if not tokens or not all(re.fullmatch(r"\d{3}", token) for token in tokens):
        return None
    return tokens


def read_rows() -> list[dict[str, object]]:
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


def reg(row: dict[str, object]) -> str:
    return "|".join(str(row.get(key, "")) for key in ["site", "type", "symbol", "shape"])


def find_unit(tokens: list[str], unit: list[str]) -> list[int]:
    return [idx for idx in range(len(tokens) - len(unit) + 1) if tokens[idx : idx + len(unit)] == unit]


def tail_after_002_861(tokens: list[str]) -> tuple[int, list[str]] | None:
    for idx in range(len(tokens) - 1):
        if tokens[idx : idx + 2] == ["002", "861"]:
            return idx, tokens[idx + 2 :]
    return None


def count_join(values: list[str], topn: int = 12) -> str:
    return ";".join(f"{key}:{value}" for key, value in Counter(values).most_common(topn))


def examples(rows: list[dict[str, object]], limit: int = 12) -> str:
    return ";".join(f"{row['cisi']} {row['text']}" for row in rows[:limit])


def component_rows(rows: list[dict[str, object]], sign: str) -> list[dict[str, object]]:
    out = []
    for row in rows:
        tokens = row["_tokens"]
        assert isinstance(tokens, list)
        for idx in find_unit(tokens, [sign]):
            in_533_717 = idx + 1 < len(tokens) and tokens[idx : idx + 2] == ["533", "717"]
            after_002_861 = idx >= 2 and tokens[idx - 2 : idx] == ["002", "861"]
            out.append(
                {
                    "sign": sign,
                    "cisi": str(row["cisi"]),
                    "site": str(row["site"]),
                    "type": str(row["type"]),
                    "symbol": str(row["symbol"]),
                    "shape": str(row["shape"]),
                    "register_key": reg(row),
                    "text": str(row["text"]),
                    "index": idx,
                    "prev2": " ".join(tokens[max(0, idx - 2) : idx]) or "<START>",
                    "next2": " ".join(tokens[idx + 1 : idx + 3]) or "<END>",
                    "terminal": idx == len(tokens) - 1,
                    "inside_533_717": in_533_717 or (idx > 0 and tokens[idx - 1 : idx + 1] == ["533", "717"]),
                    "after_002_861": after_002_861,
                }
            )
    return out


def post861_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out = []
    for row in rows:
        tokens = row["_tokens"]
        assert isinstance(tokens, list)
        hit = tail_after_002_861(tokens)
        if hit is None:
            continue
        idx, tail = hit
        prefix = tokens[:idx]
        out.append(
            {
                "cisi": str(row["cisi"]),
                "site": str(row["site"]),
                "type": str(row["type"]),
                "symbol": str(row["symbol"]),
                "shape": str(row["shape"]),
                "register_key": reg(row),
                "text": str(row["text"]),
                "prefix_last1": prefix[-1] if prefix else "<START>",
                "prefix_last2": " ".join(prefix[-2:]) if len(prefix) >= 2 else prefix[-1] if prefix else "<START>",
                "tail": " ".join(tail) if tail else "<END>",
                "tail_len": len(tail),
            }
        )
    return out


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_doc(path: Path, summary: dict[str, object]) -> None:
    lines = [
        "# 032-002-861 533-717 Component Ecology",
        "",
        "Date: 2026-05-29",
        "",
        "## Question",
        "",
        "Does `533-717` behave like a decomposable phrase with independent component ecology, or like a fixed terminal two-sign unit after `002-861`?",
        "",
        "## Result",
        "",
        f"- Strict rows scanned: `{summary['strict_rows_scanned']}`",
        f"- `533-717` adjacent occurrences: `{summary['unit_533_717_occurrences']}`",
        f"- Independent `533` occurrences outside `533-717`: `{summary['independent_533_occurrences']}`",
        f"- Independent `717` occurrences outside `533-717`: `{summary['independent_717_occurrences']}`",
        f"- Broad no-icon `SEAL:R` `002-861` rows checked: `{summary['broad_register_002_861_rows']}`",
        f"- Narrow cuboid-convex no-icon `SEAL:R` `002-861` rows checked: `{summary['narrow_register_002_861_rows']}`",
        "",
        "## Register Tail Fields",
        "",
        f"- Broad no-icon `SEAL:R`: `{summary['broad_register_tail_counts']}`",
        f"- Narrow cuboid-convex no-icon `SEAL:R`: `{summary['narrow_register_tail_counts']}`",
        "",
        "## Decision",
        "",
        f"Status: `{summary['decision']['status']}`.",
        "",
    ]
    for item in summary["decision"]["interpretation"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Accepted values, phonetics, language identity, translations, and exact source-normalized token boundaries remain 0/unaccepted.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = read_rows()
    comp533 = component_rows(rows, "533")
    comp717 = component_rows(rows, "717")
    unit_rows = []
    for row in rows:
        tokens = row["_tokens"]
        assert isinstance(tokens, list)
        if find_unit(tokens, ["533", "717"]):
            unit_rows.append(row)

    independent533 = [row for row in comp533 if not row["inside_533_717"]]
    independent717 = [row for row in comp717 if not row["inside_533_717"]]

    post_rows = post861_rows(rows)
    broad_register = [
        row
        for row in post_rows
        if row["site"] == "Mohenjo-daro" and row["type"] == "SEAL:R" and row["symbol"] == "None"
    ]
    narrow_register_key = "Mohenjo-daro|SEAL:R|None|cuboid-convex"
    narrow_register = [row for row in post_rows if row["register_key"] == narrow_register_key]

    component_summary = [
        {
            "object": "533",
            "occurrences": len(comp533),
            "independent_occurrences": len(independent533),
            "register_counts": count_join([str(row["register_key"]) for row in independent533]),
            "prev2_counts": count_join([str(row["prev2"]) for row in independent533]),
            "next2_counts": count_join([str(row["next2"]) for row in independent533]),
            "examples": examples(independent533),
        },
        {
            "object": "717",
            "occurrences": len(comp717),
            "independent_occurrences": len(independent717),
            "register_counts": count_join([str(row["register_key"]) for row in independent717]),
            "prev2_counts": count_join([str(row["prev2"]) for row in independent717]),
            "next2_counts": count_join([str(row["next2"]) for row in independent717]),
            "examples": examples(independent717),
        },
        {
            "object": "533 717",
            "occurrences": len(unit_rows),
            "independent_occurrences": 0,
            "register_counts": count_join([reg(row) for row in unit_rows]),
            "prev2_counts": count_join([" ".join(row["_tokens"][max(0, find_unit(row["_tokens"], ["533", "717"])[0] - 2) : find_unit(row["_tokens"], ["533", "717"])[0]]) for row in unit_rows]),  # type: ignore[index]
            "next2_counts": "<END>",
            "examples": examples(unit_rows),
        },
    ]

    summary = {
        "date": "2026-05-29",
        "strict_rows_scanned": len(rows),
        "unit_533_717_occurrences": len(unit_rows),
        "unit_533_717_examples": examples(unit_rows),
        "independent_533_occurrences": len(independent533),
        "independent_533_examples": examples(independent533),
        "independent_717_occurrences": len(independent717),
        "independent_717_examples": examples(independent717),
        "broad_register_key": "Mohenjo-daro|SEAL:R|None|*",
        "broad_register_002_861_rows": len(broad_register),
        "broad_register_tail_counts": count_join([str(row["tail"]) for row in broad_register]),
        "broad_register_examples": examples(
            [row for row in broad_register if row["tail"] in {"<END>", "533 717", "603", "360 520 919 140"}]
        ),
        "narrow_register_key": narrow_register_key,
        "narrow_register_002_861_rows": len(narrow_register),
        "narrow_register_tail_counts": count_join([str(row["tail"]) for row in narrow_register]),
        "narrow_register_examples": examples(narrow_register),
        "decision": {
            "status": "533_717_fixed_terminal_unit_not_decomposed_value",
            "interpretation": [
                "`533-717` remains the only fixed-prefix repeated terminal tail after `002-861`, but this scan does not promote its internal components to independent values.",
                "The pair should be treated as a fixed two-sign restricted-tail unit for the next grammar pass, not as separately readable `533` plus `717`.",
                "The broad no-icon SEAL:R field still contains bare closure, `603`, and a long tail, so `533-717` is not the marker of that whole branch.",
                "Inside the narrower cuboid-convex no-icon SEAL:R field, `533-717` competes with the long tail `360-520-919-140`; that is narrower pressure, not a value.",
                "The next useful question is source-normalized contrast between fixed-tail units inside the post-`002-861` secondary zone, not a component-level translation of `533` or `717`.",
            ],
            "not_accepted": [
                "533 value",
                "717 value",
                "533-717 semantic value",
                "phonetics",
                "language identity",
                "translation",
            ],
        },
    }

    write_csv(REPORTS / f"{OUT_PREFIX}_components.csv", comp533 + comp717)
    write_csv(REPORTS / f"{OUT_PREFIX}_component_summary.csv", component_summary)
    write_csv(REPORTS / f"{OUT_PREFIX}_broad_register_rows.csv", broad_register)
    write_csv(REPORTS / f"{OUT_PREFIX}_narrow_register_rows.csv", narrow_register)
    (REPORTS / f"{OUT_PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_doc(DOCS / f"{OUT_PREFIX}.md", summary)
    print(json.dumps(summary["decision"], indent=2))


if __name__ == "__main__":
    main()
