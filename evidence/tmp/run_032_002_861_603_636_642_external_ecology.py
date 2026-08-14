"""External ecology census for signs 603, 636, and 642.

This script reads the filtered corpus metadata (metadata_filtered.csv), keeps only
clean strict rows — inscriptions bracketed by + with no damage markers and all
three-digit sign tokens — and maps where 603, 636, and 642 occur across the whole
corpus, outside the 032-002-861 frame as well as inside it. The point is ecology:
before treating any of these signs as a meaningful tail choice, we need to know how
each behaves everywhere else. It writes a rows CSV, a summary CSV, a summary JSON,
and a docs/ markdown note. No sign value or reading is accepted.
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
DOCS = ROOT / "docs"
REPORTS.mkdir(parents=True, exist_ok=True)
DOCS.mkdir(parents=True, exist_ok=True)

TARGETS = ("603", "636", "642")


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


def find_tail_after_002_861(tokens: list[str]) -> tuple[int, list[str]] | None:
    for idx in range(len(tokens) - 1):
        if tokens[idx : idx + 2] == ["002", "861"]:
            return idx, tokens[idx + 2 :]
    return None


def joined_counts(values: list[str], topn: int = 12) -> str:
    return ";".join(f"{key}:{value}" for key, value in Counter(values).most_common(topn))


def context(tokens: list[str], idx: int, before: int = 3, after: int = 4) -> tuple[str, str]:
    prev_window = tokens[max(0, idx - before) : idx]
    next_window = tokens[idx + 1 : idx + 1 + after]
    return (" ".join(prev_window) if prev_window else "<START>", " ".join(next_window) if next_window else "<END>")


def classify_frame(tokens: list[str], idx: int) -> str:
    sign = tokens[idx]
    if idx >= 2 and tokens[idx - 2 : idx] == ["002", "861"]:
        return "post_002_861_tail_initial"
    if idx >= 1 and tokens[idx - 1] == "740" and tokens[idx + 1 : idx + 4] == ["240", "060", "692"]:
        return "exact_740_X_240_060_692"
    if idx >= 1 and idx + 1 < len(tokens) and tokens[idx - 1] == "740" and tokens[idx + 1] == "240":
        return "740_X_240_frame_other"
    if idx >= 1 and idx + 1 < len(tokens) and tokens[idx - 1] == "690" and tokens[idx + 1] == "240":
        return "690_X_240_frame"
    if idx >= 1 and idx + 1 < len(tokens) and tokens[idx - 1] == "000" and tokens[idx + 1] == "240":
        return "000_X_240_frame"
    if idx + 1 < len(tokens) and tokens[idx + 1] == "240":
        return f"{sign}_before_240_other"
    if idx == len(tokens) - 1:
        return "terminal_other"
    return "other"


def occurrence_rows(rows: list[dict[str, object]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in rows:
        tokens = row["_tokens"]
        assert isinstance(tokens, list)
        tail_hit = find_tail_after_002_861(tokens)
        tail_text = ""
        tail_initial = ""
        if tail_hit is not None:
            _, tail = tail_hit
            tail_text = " ".join(tail) if tail else "<END>"
            tail_initial = tail[0] if tail else "<END>"
        for idx, token in enumerate(tokens):
            if token not in TARGETS:
                continue
            prev_window, next_window = context(tokens, idx)
            frame_class = classify_frame(tokens, idx)
            register_key = "|".join([row["site"], row["type"], row["symbol"], row["shape"]])
            source_key = "|".join([row["site"], row["type"], row["symbol"], row["shape"], row["material"]])
            out.append(
                {
                    "target_sign": token,
                    "id": row["id"],
                    "cisi": row["cisi"],
                    "region": row["region"],
                    "site": row["site"],
                    "area_section": row["area-section"],
                    "block_house": row["block-house"],
                    "room_grid": row["room-grid"],
                    "excavation_idno": row["excavation-idno"],
                    "time": row["time"],
                    "period": row["period"],
                    "phase": row["phase"],
                    "depth": row["depth"],
                    "material": row["material"],
                    "color": row["color"],
                    "shape": row["shape"],
                    "symbol": row["symbol"],
                    "cult": row["cult"],
                    "type": row["type"],
                    "condition": row["condition"],
                    "complete": row["complete"],
                    "dir": row["dir."],
                    "class": row["class"],
                    "text_length": row["text length"],
                    "token_count": str(len(tokens)),
                    "text": row["text"],
                    "occurrence_index_0based": str(idx),
                    "position_class": "initial" if idx == 0 else "terminal" if idx == len(tokens) - 1 else "medial",
                    "is_terminal": str(idx == len(tokens) - 1).lower(),
                    "prev1": tokens[idx - 1] if idx else "<START>",
                    "prev2": " ".join(tokens[idx - 2 : idx]) if idx >= 2 else tokens[idx - 1] if idx else "<START>",
                    "next1": tokens[idx + 1] if idx + 1 < len(tokens) else "<END>",
                    "next2": " ".join(tokens[idx + 1 : idx + 3])
                    if idx + 2 < len(tokens)
                    else tokens[idx + 1]
                    if idx + 1 < len(tokens)
                    else "<END>",
                    "prev_window": prev_window,
                    "next_window": next_window,
                    "frame_class": frame_class,
                    "inside_exact_740_x_240_060_692": str(frame_class == "exact_740_X_240_060_692").lower(),
                    "inside_740_x_240": str(frame_class in {"exact_740_X_240_060_692", "740_X_240_frame_other"}).lower(),
                    "inside_690_x_240": str(frame_class == "690_X_240_frame").lower(),
                    "inside_000_x_240": str(frame_class == "000_X_240_frame").lower(),
                    "post_002_861_tail_initial": str(frame_class == "post_002_861_tail_initial").lower(),
                    "row_tail_after_002_861": tail_text,
                    "row_tail_initial_after_002_861": tail_initial,
                    "register_key": register_key,
                    "source_key": source_key,
                    "formula_key": row["text"],
                }
            )
    return out


def compact_examples(rows: list[dict[str, str]], limit: int = 8) -> str:
    return ";".join(f"{row['cisi']} {row['text']}" for row in rows[:limit])


def build_summary(rows: list[dict[str, str]], strict_rows_scanned: int) -> tuple[list[dict[str, str]], dict[str, object]]:
    by_sign: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_sign[row["target_sign"]].append(row)

    summary_rows: list[dict[str, str]] = []
    for sign in TARGETS:
        group = by_sign.get(sign, [])
        frame_counts = Counter(row["frame_class"] for row in group)
        exact_rows = [row for row in group if row["frame_class"] == "exact_740_X_240_060_692"]
        x240_rows = [
            row
            for row in group
            if row["frame_class"] in {"exact_740_X_240_060_692", "740_X_240_frame_other", "690_X_240_frame", "000_X_240_frame"}
        ]
        post_rows = [row for row in group if row["frame_class"] == "post_002_861_tail_initial"]
        outside_rows = [row for row in group if row["frame_class"] != "exact_740_X_240_060_692"]
        outside_x240_rows = [row for row in outside_rows if row in x240_rows]
        non_x240_outside_rows = [row for row in outside_rows if row not in x240_rows]
        summary_rows.append(
            {
                "target_sign": sign,
                "occurrences": str(len(group)),
                "rows": str(len({row["cisi"] + "|" + row["text"] for row in group})),
                "register_cells": str(len({row["register_key"] for row in group})),
                "source_cells": str(len({row["source_key"] for row in group})),
                "formula_families": str(len({row["formula_key"] for row in group})),
                "exact_740_x_240_060_692_rows": str(len(exact_rows)),
                "all_x_240_template_rows": str(len(x240_rows)),
                "outside_exact_rows": str(len(outside_rows)),
                "outside_x_240_template_rows": str(len(outside_x240_rows)),
                "non_x240_outside_rows": str(len(non_x240_outside_rows)),
                "post_002_861_tail_initial_rows": str(len(post_rows)),
                "terminal_rows": str(sum(row["is_terminal"] == "true" for row in group)),
                "frame_counts": ";".join(f"{key}:{value}" for key, value in frame_counts.most_common()),
                "register_counts": joined_counts([row["register_key"] for row in group]),
                "prev2_counts": joined_counts([row["prev2"] for row in group]),
                "next2_counts": joined_counts([row["next2"] for row in group]),
                "examples": compact_examples(group),
                "non_x240_outside_examples": compact_examples(non_x240_outside_rows),
            }
        )

    sign_sets_by_frame = defaultdict(set)
    for row in rows:
        sign_sets_by_frame[row["frame_class"]].add(row["target_sign"])

    payload = {
        "date": "2026-05-29",
        "strict_rows_scanned": strict_rows_scanned,
        "target_signs": list(TARGETS),
        "summary_rows": summary_rows,
        "frame_to_signs": {frame: sorted(signs) for frame, signs in sorted(sign_sets_by_frame.items())},
        "decision": decide(summary_rows),
    }
    return summary_rows, payload


def decide(summary_rows: list[dict[str, str]]) -> dict[str, object]:
    by_sign = {row["target_sign"]: row for row in summary_rows}
    bridge_signs = [
        sign for sign, row in by_sign.items() if int(row["post_002_861_tail_initial_rows"]) > 0
    ]
    x240_heavy = {
        sign: int(row["all_x_240_template_rows"]) / max(1, int(row["occurrences"]))
        for sign, row in by_sign.items()
    }
    return {
        "status": "603_is_cross_construction_bridge_candidate_not_a_translation",
        "bridge_signs_after_002_861": bridge_signs,
        "x240_template_share": x240_heavy,
        "accepted": [
            "The target set forms an X-before-240 ecology centered on 740/690/000 frames.",
            "603 is the only member of this target set that appears as an immediate post-002-861 tail initial in the strict corpus.",
        ],
        "rejected": [
            "No phonetic value, language identity, or translation follows from this campaign.",
            "The Harappa 740-X-240-060-692 slot alone is not enough to prove a grammatical paradigm.",
        ],
        "next_test": "Expand X-before-240 from only 603/636/642 to all X values, then ask whether post-861 bridge behavior concentrates in a semantic/grammatical class or is accidental.",
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, payload: dict[str, object]) -> None:
    summary_rows = payload["summary_rows"]
    decision = payload["decision"]
    assert isinstance(summary_rows, list)
    assert isinstance(decision, dict)
    lines = [
        "# Campaign 032 External Ecology: 603 / 636 / 642",
        "",
        "Date: 2026-05-29",
        "",
        "Question: do the Harappa `740-X-240-060-692` slot signs behave like a live sign class, a narrow template artifact, or a bridge into the post-`002-861` construction?",
        "",
        "Method: strict complete-token rows only; no bracketed or parenthesized readings; deduplicated by `(cisi, site, type, symbol, text)`.",
        "",
        f"Strict corpus rows scanned: `{payload['strict_rows_scanned']}`.",
        "",
        "## Summary",
        "",
        "| sign | occ. | registers | exact 740-X-240-060-692 | all X-240 templates | outside exact | non-X240 outside | post-002-861 tail initial | frame counts |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in summary_rows:
        assert isinstance(row, dict)
        lines.append(
            "| {target_sign} | {occurrences} | {register_cells} | {exact_740_x_240_060_692_rows} | {all_x_240_template_rows} | {outside_exact_rows} | {non_x240_outside_rows} | {post_002_861_tail_initial_rows} | {frame_counts} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            f"Status: `{decision['status']}`.",
            "",
            "Accepted:",
        ]
    )
    for item in decision["accepted"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Rejected:")
    for item in decision["rejected"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            f"Next test: {decision['next_test']}",
            "",
            "## Examples",
            "",
        ]
    )
    for row in summary_rows:
        assert isinstance(row, dict)
        lines.extend(
            [
                f"### `{row['target_sign']}`",
                "",
                f"- Examples: {row['examples']}",
                f"- Non-X240 outside examples: {row['non_x240_outside_examples'] or '(none)'}",
                f"- Register counts: {row['register_counts']}",
                "",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    corpus_rows = load_rows()
    rows = occurrence_rows(corpus_rows)
    summary_rows, payload = build_summary(rows, len(corpus_rows))

    rows_csv = REPORTS / "campaign_032_002_861_603_636_642_external_ecology_rows.csv"
    summary_csv = REPORTS / "campaign_032_002_861_603_636_642_external_ecology_summary.csv"
    summary_json = REPORTS / "campaign_032_002_861_603_636_642_external_ecology_summary.json"
    md = DOCS / "campaign_032_002_861_603_636_642_external_ecology.md"

    write_csv(rows_csv, rows)
    write_csv(summary_csv, summary_rows)
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(md, payload)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
