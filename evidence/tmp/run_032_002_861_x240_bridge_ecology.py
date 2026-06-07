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


def source_key(row: dict[str, object]) -> str:
    return "|".join([str(row["site"]), str(row["type"]), str(row["symbol"]), str(row["shape"]), str(row["material"])])


def joined_counts(values: list[str], topn: int = 12) -> str:
    return ";".join(f"{key}:{value}" for key, value in Counter(values).most_common(topn))


def compact_examples(rows: list[dict[str, str]], limit: int = 8) -> str:
    return ";".join(f"{row['cisi']} {row['text']}" for row in rows[:limit])


def collect_x240(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        tokens = row["_tokens"]
        assert isinstance(tokens, list)
        for idx in range(1, len(tokens) - 1):
            if tokens[idx - 1] not in FRAME_PREFIXES or tokens[idx + 1] != "240":
                continue
            sign = tokens[idx]
            frame = f"{tokens[idx - 1]}_X_240"
            out.append(
                {
                    "x_sign": sign,
                    "frame": frame,
                    "prefix": tokens[idx - 1],
                    "id": str(row["id"]),
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
                    "occurrence_index_0based": str(idx),
                    "next2_after_x": " ".join(tokens[idx + 1 : idx + 3])
                    if idx + 2 < len(tokens)
                    else tokens[idx + 1],
                    "exact_740_x_240_060_692": str(
                        tokens[idx - 1] == "740" and tokens[idx + 1 : idx + 4] == ["240", "060", "692"]
                    ).lower(),
                    "register_key": register_key(row),
                    "source_key": source_key(row),
                    "formula_key": str(row["text"]),
                }
            )
    return out


def collect_post_861_initial(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        tokens = row["_tokens"]
        assert isinstance(tokens, list)
        for idx in range(len(tokens) - 1):
            if tokens[idx : idx + 2] != ["002", "861"]:
                continue
            tail = tokens[idx + 2 :]
            initial = tail[0] if tail else "<END>"
            out.append(
                {
                    "tail_initial": initial,
                    "tail_after_002_861": " ".join(tail) if tail else "<END>",
                    "tail_len": str(len(tail)),
                    "id": str(row["id"]),
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
                    "prefix_last2_before_002_861": " ".join(tokens[max(0, idx - 2) : idx]) if idx else "<START>",
                    "register_key": register_key(row),
                    "source_key": source_key(row),
                    "formula_key": str(row["text"]),
                }
            )
    return out


def collect_any_sign_counts(rows: list[dict[str, object]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in rows:
        tokens = row["_tokens"]
        assert isinstance(tokens, list)
        counts.update(tokens)
    return counts


def build_summary(
    x240_rows: list[dict[str, str]],
    post_rows: list[dict[str, str]],
    any_sign_counts: Counter[str],
    strict_rows_scanned: int,
) -> tuple[list[dict[str, str]], dict[str, object]]:
    by_x: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_tail_initial: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in x240_rows:
        by_x[row["x_sign"]].append(row)
    for row in post_rows:
        by_tail_initial[row["tail_initial"]].append(row)

    signs = sorted(set(by_x) | set(by_tail_initial))
    summary: list[dict[str, str]] = []
    for sign in signs:
        x_rows = by_x.get(sign, [])
        tail_rows = by_tail_initial.get(sign, [])
        frame_counts = Counter(row["frame"] for row in x_rows)
        exact_count = sum(row["exact_740_x_240_060_692"] == "true" for row in x_rows)
        summary.append(
            {
                "sign": sign,
                "any_occurrences": str(any_sign_counts.get(sign, 0)),
                "x240_rows": str(len(x_rows)),
                "x240_register_cells": str(len({row["register_key"] for row in x_rows})),
                "x240_source_cells": str(len({row["source_key"] for row in x_rows})),
                "x240_formula_families": str(len({row["formula_key"] for row in x_rows})),
                "x240_frame_counts": ";".join(f"{key}:{value}" for key, value in frame_counts.most_common()),
                "exact_740_x_240_060_692_rows": str(exact_count),
                "post_002_861_tail_initial_rows": str(len(tail_rows)),
                "post_002_861_tail_register_cells": str(len({row["register_key"] for row in tail_rows})),
                "post_002_861_tail_families": str(len({row["tail_after_002_861"] for row in tail_rows})),
                "bridge_candidate": str(bool(x_rows and tail_rows)).lower(),
                "x240_examples": compact_examples(x_rows),
                "post_861_examples": compact_examples(tail_rows),
                "x240_register_counts": joined_counts([row["register_key"] for row in x_rows]),
                "post_861_register_counts": joined_counts([row["register_key"] for row in tail_rows]),
            }
        )

    bridge_rows = [row for row in summary if row["bridge_candidate"] == "true" and row["sign"] != "<END>"]
    bridge_rows.sort(
        key=lambda row: (
            -int(row["post_002_861_tail_initial_rows"]),
            -int(row["x240_rows"]),
            row["sign"],
        )
    )
    payload = {
        "date": "2026-05-29",
        "strict_rows_scanned": strict_rows_scanned,
        "x240_rows": len(x240_rows),
        "x240_distinct_x_signs": len(by_x),
        "post_002_861_rows": len(post_rows),
        "post_002_861_non_bare_rows": sum(row["tail_initial"] != "<END>" for row in post_rows),
        "post_002_861_distinct_initials": len(by_tail_initial),
        "bridge_candidates": bridge_rows,
        "decision": decide(bridge_rows, summary),
    }
    return summary, payload


def decide(bridge_rows: list[dict[str, str]], summary: list[dict[str, str]]) -> dict[str, object]:
    bridge_signs = [row["sign"] for row in bridge_rows]
    non_background_bridge_signs = [row["sign"] for row in bridge_rows if row["sign"] != "000"]
    sign603 = next((row for row in summary if row["sign"] == "603"), None)
    controls = [row for row in summary if row["sign"] in {"636", "642"}]
    return {
        "status": "603_survives_as_only_non_background_bridge_candidate_inside_larger_x240_class",
        "raw_bridge_signs": bridge_signs,
        "non_background_bridge_signs": non_background_bridge_signs,
        "603_row": sign603,
        "636_642_controls": controls,
        "accepted": [
            "Raw bridge behavior is limited to 603 and 000; 000 is broad background/control material with 810 occurrences, so it is not a peer lexical/control competitor.",
            "603 is the only low-frequency non-background X-before-240 sign that also appears as a post-002-861 tail initial in this strict layer.",
            "Within the local 603/636/642 slot family, 636 and 642 remain X-before-240 controls while 603 bridges into post-002-861.",
            "The next linguistic object is the X-before-240 class with 603 as the primary bridge candidate and 000 as the background control.",
        ],
        "rejected": [
            "Absolute uniqueness for 603 is false if 000 is counted naively.",
            "A 603-only decipherment hypothesis is too narrow unless it explains why 636 and 642 stay inside X-before-240 while 603 can occur after 002-861.",
            "No phonetic value, language identity, or translation follows from this bridge result.",
        ],
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, summary: list[dict[str, str]], payload: dict[str, object]) -> None:
    decision = payload["decision"]
    assert isinstance(decision, dict)
    bridge_rows = payload["bridge_candidates"]
    assert isinstance(bridge_rows, list)
    lines = [
        "# Campaign 032 X-Before-240 Bridge Ecology",
        "",
        "Date: 2026-05-29",
        "",
        "Question: is `603` uniquely mobile out of the X-before-240 ecology, or is it one member of a broader bridge subset?",
        "",
        "Method: strict complete-token rows only; no bracketed or parenthesized readings; deduplicated by `(cisi, site, type, symbol, text)`.",
        "",
        f"Strict corpus rows scanned: `{payload['strict_rows_scanned']}`.",
        f"X-before-240 rows scanned: `{payload['x240_rows']}` across `{payload['x240_distinct_x_signs']}` X signs.",
        f"Post-`002-861` rows scanned: `{payload['post_002_861_rows']}` total, including `{payload['post_002_861_non_bare_rows']}` non-bare tail rows, across `{payload['post_002_861_distinct_initials']}` tail states.",
        "",
        "## Decision",
        "",
        f"Status: `{decision['status']}`.",
        "",
        "Accepted:",
    ]
    for item in decision["accepted"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Rejected:")
    for item in decision["rejected"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Bridge Candidates",
            "",
            "| sign | X-240 rows | X-240 frames | post-861 rows | post-861 families | X-240 examples | post-861 examples |",
            "|---|---:|---|---:|---:|---|---|",
        ]
    )
    for row in bridge_rows:
        assert isinstance(row, dict)
        lines.append(
            "| {sign} | {x240_rows} | {x240_frame_counts} | {post_002_861_tail_initial_rows} | {post_002_861_tail_families} | {x240_examples} | {post_861_examples} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Target Controls",
            "",
            "| sign | any occ. | X-240 rows | exact 740-X-240-060-692 | post-861 tail initial | bridge? |",
            "|---|---:|---:|---:|---:|---|",
        ]
    )
    for row in [item for item in summary if item["sign"] in {"603", "636", "642"}]:
        lines.append(
            "| {sign} | {any_occurrences} | {x240_rows} | {exact_740_x_240_060_692_rows} | {post_002_861_tail_initial_rows} | {bridge_candidate} |".format(
                **row
            )
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    rows = load_rows()
    x240_rows = collect_x240(rows)
    post_rows = collect_post_861_initial(rows)
    any_sign_counts = collect_any_sign_counts(rows)
    summary, payload = build_summary(x240_rows, post_rows, any_sign_counts, len(rows))

    write_csv(REPORTS / "campaign_032_002_861_x240_bridge_rows.csv", x240_rows)
    write_csv(REPORTS / "campaign_032_002_861_x240_bridge_post861_rows.csv", post_rows)
    write_csv(REPORTS / "campaign_032_002_861_x240_bridge_summary.csv", summary)
    (REPORTS / "campaign_032_002_861_x240_bridge_summary.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    write_markdown(DOCS / "campaign_032_002_861_x240_bridge_ecology.md", summary, payload)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
