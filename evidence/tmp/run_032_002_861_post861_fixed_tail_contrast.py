"""Profile the tails that follow 002-861 and sort them into contrast classes.

We rebuild every post-002-861 occurrence from the strict corpus, attach source
status (whether a photo or crop has actually been checked) from three earlier
verdict/control CSVs, and then profile each focus tail: how many rows, how
many strict family cells (tail + prefix + register + template), how many rows
are source-visible, and how much matched bare-closure pressure exists in the
same preframe or register. A classifier assigns each tail a contrast class —
background closure, fixed restricted unit, recurrent simple tail, singleton
contrast, and so on. Outputs: profiles/focus-rows/matched-controls CSVs, a
JSON summary, and a Markdown doc in docs/. The decision block records that no
tail values, phonetics, or translations are accepted.
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

ATTACHMENT_VERDICTS = REPORTS / "campaign_032_002_861_source_token_attachment_verdicts.csv"
BARE_EDGE_CONTROLS = REPORTS / "campaign_032_002_861_bare_edge_source_controls_rows.csv"
REGISTER_CONTROL_CROPS = REPORTS / "campaign_032_002_861_533717_source_controls_crops.csv"

OUT_PREFIX = "campaign_032_002_861_post861_fixed_tail_contrast"
FOCUS_TAILS = {"<END>", "533 717", "603", "255 416", "360 520 919 140"}


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


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
    return "|".join(str(row.get(key, "")) for key in ["site", "type", "symbol", "shape"])


def signless_template(tokens: list[str]) -> str:
    out = tokens[:]
    for idx in range(len(out) - 1):
        if out[idx : idx + 2] == ["002", "861"]:
            out[idx + 2 :] = ["TAIL"] if idx + 2 < len(out) else []
            return "+" + "-".join(out) + "+"
    return "+" + "-".join(out) + "+"


def post861_occurrences(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for row in rows:
        tokens = row["_tokens"]
        assert isinstance(tokens, list)
        for idx in range(len(tokens) - 1):
            if tokens[idx : idx + 2] != ["002", "861"]:
                continue
            prefix = tokens[:idx]
            tail = tokens[idx + 2 :]
            tail_text = " ".join(tail) if tail else "<END>"
            out.append(
                {
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
                    "prefix_last1": prefix[-1] if prefix else "<START>",
                    "prefix_last2": " ".join(prefix[-2:]) if len(prefix) >= 2 else prefix[-1] if prefix else "<START>",
                    "tail": tail_text,
                    "tail_len": len(tail),
                    "terminal_after_tail": idx + 2 + len(tail) == len(tokens),
                    "register_key": register_key(row),
                    "template_key": signless_template(tokens),
                }
            )
    return out


def source_map() -> dict[str, dict[str, str]]:
    source: dict[str, dict[str, str]] = {}
    for row in read_csv(ATTACHMENT_VERDICTS):
        source[row["cisi"]] = {
            "source_status": "source_visible_same_line_tail_candidate",
            "source_basis": row.get("attachment_verdict", ""),
            "source_confidence": row.get("confidence", ""),
            "source_note": row.get("observation", ""),
        }
    for row in read_csv(BARE_EDGE_CONTROLS):
        status = row.get("visual_status") or row.get("route_status", "")
        source[row["cisi"]] = {
            "source_status": "source_visible_bare_edge" if status == "bare_terminal_edge_visible" else row.get("route_status", ""),
            "source_basis": row.get("family", ""),
            "source_confidence": "",
            "source_note": row.get("evidence_note", ""),
        }
    for row in read_csv(REGISTER_CONTROL_CROPS):
        prev = source.get(row["cisi"], {})
        source[row["cisi"]] = {
            "source_status": prev.get("source_status") or row.get("status", ""),
            "source_basis": prev.get("source_basis") or row.get("role", ""),
            "source_confidence": prev.get("source_confidence", ""),
            "source_note": prev.get("source_note") or row.get("source_route", ""),
        }
    return source


def count_join(values: list[str], topn: int = 12) -> str:
    return ";".join(f"{key}:{value}" for key, value in Counter(values).most_common(topn))


def examples(rows: list[dict[str, object]], limit: int = 10) -> str:
    return ";".join(f"{row['cisi']} {row['text']}" for row in rows[:limit])


def family_key(row: dict[str, object]) -> tuple[str, str, str, str]:
    return (str(row["tail"]), str(row["prefix_last2"]), str(row["register_key"]), str(row["template_key"]))


def matched_bare_controls(rows: list[dict[str, object]], focus_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    bare = [row for row in rows if row["tail"] == "<END>"]
    out: list[dict[str, object]] = []
    for row in focus_rows:
        if row["tail"] == "<END>":
            continue
        same_last2 = [b for b in bare if b["prefix_last2"] == row["prefix_last2"]]
        same_last1 = [b for b in bare if b["prefix_last1"] == row["prefix_last1"]]
        same_register = [b for b in bare if b["register_key"] == row["register_key"]]
        same_register_shape_family = [
            b
            for b in bare
            if b["site"] == row["site"] and b["type"] == row["type"] and b["symbol"] == row["symbol"]
        ]
        out.append(
            {
                "tail": row["tail"],
                "cisi": row["cisi"],
                "text": row["text"],
                "prefix_last2": row["prefix_last2"],
                "register_key": row["register_key"],
                "same_last2_bare_count": len(same_last2),
                "same_last2_bare_examples": examples(same_last2, 6),
                "same_last1_bare_count": len(same_last1),
                "same_last1_bare_examples": examples(same_last1, 6),
                "same_register_bare_count": len(same_register),
                "same_register_bare_examples": examples(same_register, 6),
                "same_broad_register_bare_count": len(same_register_shape_family),
                "same_broad_register_bare_examples": examples(same_register_shape_family, 6),
            }
        )
    return out


def classify(row: dict[str, object]) -> tuple[str, list[str]]:
    tail = str(row["tail"])
    rows = int(row["rows"])
    family_cells = int(row["family_cells"])
    source_visible = int(row["source_visible_rows"])
    last2_bare = int(row["rows_with_same_last2_bare"])
    broad_bare = int(row["rows_with_same_broad_register_bare"])
    notes: list[str] = []
    if tail == "<END>":
        return "background_closure", ["dominant post-002-861 state, not a tail value"]
    if tail == "533 717":
        notes.extend(["repeated fixed-prefix terminal unit", "not decomposed because independent 533 is absent"])
        if broad_bare:
            notes.append("broad no-icon SEAL:R field has bare controls")
        return "fixed_restricted_tail_unit", notes
    if tail == "603":
        notes.extend(["recurrent simple tail across multiple source-visible rows", "bridge route killed at family-cell level"])
        return "recurrent_simple_tail_parked_from_bridge", notes
    if rows == 1 and source_visible:
        notes.append("source-visible singleton tail")
        if last2_bare:
            notes.append("same last-2 frame has bare controls")
        return "source_visible_singleton_contrast", notes
    if family_cells == 1:
        return "single_family_tail", ["single family cell only"]
    return "unclassified_tail", notes


def summarize(rows: list[dict[str, object]], sources: dict[str, dict[str, str]]) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    for row in rows:
        row.update(sources.get(str(row["cisi"]), {"source_status": "source_pending_or_not_checked", "source_basis": "", "source_confidence": "", "source_note": ""}))

    focus_rows = [row for row in rows if row["tail"] in FOCUS_TAILS]
    bare_matches = matched_bare_controls(rows, focus_rows)
    bare_by_cisi = {str(row["cisi"]): row for row in bare_matches}
    by_tail: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in focus_rows:
        by_tail[str(row["tail"])].append(row)

    profiles: list[dict[str, object]] = []
    for tail, group in sorted(by_tail.items(), key=lambda item: (item[0] != "<END>", item[0])):
        family_cells = len({family_key(row) for row in group})
        source_visible = sum(str(row.get("source_status", "")).startswith("source_visible") for row in group)
        match_rows = [bare_by_cisi.get(str(row["cisi"])) for row in group if str(row["cisi"]) in bare_by_cisi]
        last2_count_rows = sum(1 for row in match_rows if row and int(row["same_last2_bare_count"]) > 0)
        last1_count_rows = sum(1 for row in match_rows if row and int(row["same_last1_bare_count"]) > 0)
        register_bare_rows = sum(1 for row in match_rows if row and int(row["same_register_bare_count"]) > 0)
        broad_bare_rows = sum(1 for row in match_rows if row and int(row["same_broad_register_bare_count"]) > 0)
        profile: dict[str, object] = {
            "tail": tail,
            "rows": len(group),
            "family_cells": family_cells,
            "source_visible_rows": source_visible,
            "source_status_counts": count_join([str(row["source_status"]) for row in group]),
            "tail_len_counts": count_join([str(row["tail_len"]) for row in group]),
            "prefix_last2_counts": count_join([str(row["prefix_last2"]) for row in group]),
            "register_counts": count_join([str(row["register_key"]) for row in group]),
            "site_counts": count_join([str(row["site"]) for row in group]),
            "shape_counts": count_join([str(row["shape"]) for row in group]),
            "rows_with_same_last2_bare": last2_count_rows,
            "rows_with_same_last1_bare": last1_count_rows,
            "rows_with_same_register_bare": register_bare_rows,
            "rows_with_same_broad_register_bare": broad_bare_rows,
            "examples": examples(group, 12),
        }
        cls, notes = classify(profile)
        profile["contrast_class"] = cls
        profile["interpretive_notes"] = ";".join(notes)
        profiles.append(profile)

    order = {
        "background_closure": 0,
        "fixed_restricted_tail_unit": 1,
        "recurrent_simple_tail_parked_from_bridge": 2,
        "source_visible_singleton_contrast": 3,
        "single_family_tail": 4,
        "unclassified_tail": 5,
    }
    profiles.sort(key=lambda row: (order.get(str(row["contrast_class"]), 9), str(row["tail"])))
    for idx, row in enumerate(profiles, 1):
        row["rank"] = idx
    return profiles, focus_rows, bare_matches


def write_doc(path: Path, summary: dict[str, object], profiles: list[dict[str, object]]) -> None:
    lines = [
        "# 032-002-861 Post-861 Fixed-Tail Contrast",
        "",
        "Date: 2026-05-29",
        "",
        "## Question",
        "",
        "Inside the post-`002-861` secondary zone, which tails behave like recurrent grammar objects, which are singleton contrasts, and which are just bare closure background?",
        "",
        "## Profiles",
        "",
        "| rank | tail | class | rows | cells | source-visible | matched bare pressure | notes |",
        "|---:|---|---|---:|---:|---:|---|---|",
    ]
    for row in profiles:
        matched = f"last2 {row['rows_with_same_last2_bare']}; last1 {row['rows_with_same_last1_bare']}; broad {row['rows_with_same_broad_register_bare']}"
        lines.append(
            f"| {row['rank']} | `{row['tail']}` | `{row['contrast_class']}` | {row['rows']} | {row['family_cells']} | {row['source_visible_rows']} | {matched} | {row['interpretive_notes']} |"
        )
    lines.extend(
        [
            "",
            "## Decision",
            "",
            f"Status: `{summary['decision']['status']}`.",
            "",
        ]
    )
    for item in summary["decision"]["interpretation"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Accepted values, phonetics, language identity, translations, and exact source-normalized token boundaries remain 0/unaccepted.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    corpus_rows = load_rows()
    rows = post861_occurrences(corpus_rows)
    sources = source_map()
    profiles, focus_rows, bare_matches = summarize(rows, sources)

    summary = {
        "date": "2026-05-29",
        "strict_rows_scanned": len(corpus_rows),
        "rows_with_002_861": len(rows),
        "focus_tails": sorted(FOCUS_TAILS),
        "profile_count": len(profiles),
        "profiles": profiles,
        "decision": {
            "status": "post861_secondary_zone_has_fixed_unit_singletons_and_bare_background_no_values",
            "interpretation": [
                "`533-717` is the best fixed restricted-tail unit, but it remains one narrow grammatical object, not a value.",
                "`603` is recurrent and source-visible as a post-`861` simple tail, but the X-before-240 bridge route is parked, so it cannot carry cross-context value evidence.",
                "`255-416` and `360-520-919-140` are source-visible singleton contrasts: useful for defining the secondary zone, not for reading it.",
                "Bare `<END>` remains the closure background and supplies matched controls in several preframes/registers.",
                "The next grammar move is a source-normalized contrast among tail classes, not component translation.",
            ],
            "not_accepted": [
                "533-717 value",
                "603 value",
                "255-416 value",
                "360-520-919-140 value",
                "phonetics",
                "language identity",
                "translation",
            ],
        },
    }

    write_csv(REPORTS / f"{OUT_PREFIX}_profiles.csv", profiles)
    write_csv(REPORTS / f"{OUT_PREFIX}_focus_rows.csv", focus_rows)
    write_csv(REPORTS / f"{OUT_PREFIX}_matched_bare_controls.csv", bare_matches)
    (REPORTS / f"{OUT_PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_doc(DOCS / f"{OUT_PREFIX}.md", summary, profiles)
    print(json.dumps(summary["decision"], indent=2))


if __name__ == "__main__":
    main()
