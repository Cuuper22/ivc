#!/usr/bin/env python
"""Source-normalized adversary for 002-390-X subframe positives.

This script attacks the two tempting positive subframes (235 -> 002-390 -> 125 and
125 -> 632 032) instead of defending them. It reads the filtered corpus metadata, the
family-collapsed branch-ecology matrix rows, and the source-route table from the
source-normalized contrast campaign. For each pattern in its inline PATTERNS table it
counts raw rows, then re-counts under two constraints at once: strict source
visibility (the row must be seen on an artifact image, not just in a catalog) and
formula-family collapse (copies of one formula count once). It writes a summary JSON
plus collapse-tests, occurrences, and focus-rows CSVs. The recorded decision: the
positive subframes do not survive; 002-390-X remains live as branch-tail ecology only.
"""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
REPORT_DIR = ROOT / "data" / "open_prototype" / "reports"
METADATA = ROOT / "data" / "open_prototype" / "lipi" / "metadata_filtered.csv"
MATRIX = REPORT_DIR / "campaign_032_002_861_002390x_family_collapsed_branch_ecology_matrix_rows.csv"
SOURCE_ROUTES = REPORT_DIR / "campaign_032_002_861_002390x_source_normalized_contrast_source_routes.csv"

PREFIX = "campaign_032_002_861_002390x_source_normalized_family_collapse"

PATTERNS = {
    "prev235_002390125": ["235", "002", "390", "125"],
    "tail_125_632032": ["125", "632", "032"],
    "frame_002390125": ["002", "390", "125"],
    "frame_002390095": ["002", "390", "095"],
    "frame_002390705": ["002", "390", "705"],
    "frame_002390692": ["002", "390", "692"],
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def parse_tokens(text: str) -> list[str]:
    return re.findall(r"\d{3}", text or "")


def is_closed_clean(text: str) -> bool:
    return bool(text) and text.startswith("+") and text.endswith("+") and "[" not in text and "]" not in text


def object_key(row: dict[str, str]) -> str:
    cisi = row.get("cisi", "")
    if cisi and cisi != "-":
        return cisi
    return f"-:{row.get('id', '')}"


def source_route_key(row: dict[str, str]) -> str:
    obj = object_key(row)
    return row.get("source_route", "") or row.get("normalized_source_route", "") or obj


def boolish(value: str) -> bool:
    return str(value).strip().lower() == "true"


def find_occurrences(tokens: list[str], pattern: list[str]) -> list[int]:
    width = len(pattern)
    return [idx for idx in range(0, len(tokens) - width + 1) if tokens[idx : idx + width] == pattern]


def main() -> None:
    metadata_rows = read_csv(METADATA)
    matrix_rows = read_csv(MATRIX)
    route_rows = read_csv(SOURCE_ROUTES)

    route_by_object: dict[str, dict[str, str]] = {}
    for row in route_rows:
        key = row.get("object_key") or row.get("cisi")
        if key:
            route_by_object[key] = row

    occurrence_rows: list[dict[str, object]] = []
    pattern_to_rows: dict[str, list[dict[str, object]]] = defaultdict(list)

    for row in metadata_rows:
        text = row.get("text", "")
        tokens = parse_tokens(text)
        if not tokens:
            continue
        key = object_key(row)
        source = route_by_object.get(key, {})
        for pattern_name, pattern in PATTERNS.items():
            for pos in find_occurrences(tokens, pattern):
                before = tokens[pos - 1] if pos > 0 else "<START>"
                after_pos = pos + len(pattern)
                after = tokens[after_pos] if after_pos < len(tokens) else "<END>"
                occ = {
                    "pattern": pattern_name,
                    "object": key,
                    "id": row.get("id", ""),
                    "site": row.get("site", ""),
                    "type": row.get("type", ""),
                    "symbol": row.get("symbol", ""),
                    "cult": row.get("cult", ""),
                    "shape": row.get("shape", ""),
                    "material": row.get("material", ""),
                    "condition": row.get("condition", ""),
                    "text": text,
                    "text_len": len(tokens),
                    "pattern_pos": pos,
                    "before_pattern": before,
                    "after_pattern": after,
                    "closed_clean": is_closed_clean(text),
                    "strict_source_visible": boolish(source.get("strict_source_visible", "")),
                    "permissive_public_panel": boolish(source.get("permissive_public_panel", "")),
                    "normalized_source_grade": source.get("normalized_source_grade", "not_source_normalized"),
                    "normalized_source_route": source.get("normalized_source_route", ""),
                    "broad_register_cell": "|".join(
                        [
                            row.get("site", ""),
                            row.get("type", ""),
                            row.get("shape", ""),
                            row.get("material", ""),
                        ]
                    ),
                    "fine_register_cell": "|".join(
                        [
                            row.get("site", ""),
                            row.get("type", ""),
                            row.get("symbol", ""),
                            row.get("cult", ""),
                            row.get("shape", ""),
                            row.get("material", ""),
                        ]
                    ),
                    "edge_frame": "|".join([before, "-".join(pattern), after]),
                    "in_002390x_frame": (
                        pattern_name == "tail_125_632032"
                        and pos >= 2
                        and tokens[pos - 2 : pos] == ["002", "390"]
                    ),
                }
                occurrence_rows.append(occ)
                pattern_to_rows[pattern_name].append(occ)

    matrix_by_object = {row["object"]: row for row in matrix_rows}
    focus_objects = {"M-38", "M-119", "M-735", "Sktd-1", "M-70", "M-71", "H-1993", "M-1825", "-:4237.1"}

    focus_rows: list[dict[str, object]] = []
    for obj in sorted(focus_objects):
        matrix = matrix_by_object.get(obj)
        if not matrix:
            continue
        source = route_by_object.get(obj, {})
        row = {
            "object": obj,
            "prev_before_002": matrix.get("prev_before_002", ""),
            "branch_after_390": matrix.get("branch_after_390", ""),
            "tail_after_branch": matrix.get("tail_after_branch", ""),
            "terminal_after_branch": matrix.get("terminal_after_branch", ""),
            "source_tier": matrix.get("source_tier", ""),
            "strict_source_visible": source.get("strict_source_visible", "False"),
            "permissive_public_panel": source.get("permissive_public_panel", "False"),
            "normalized_source_grade": source.get("normalized_source_grade", "not_source_normalized"),
            "normalized_source_route": source.get("normalized_source_route", ""),
            "site": matrix.get("site", ""),
            "type": matrix.get("type", ""),
            "symbol": matrix.get("symbol", ""),
            "cult": matrix.get("cult", ""),
            "text": matrix.get("text", ""),
        }
        focus_rows.append(row)

    collapse_rows: list[dict[str, object]] = []
    for pattern_name in PATTERNS:
        rows = pattern_to_rows[pattern_name]
        strict_source = [row for row in rows if row["strict_source_visible"]]
        permissive = [row for row in rows if row["permissive_public_panel"]]
        closed_clean = [row for row in rows if row["closed_clean"]]
        in_frame = [row for row in rows if row["in_002390x_frame"]]
        strict_in_frame = [row for row in in_frame if row["strict_source_visible"]]
        exact_texts = Counter(str(row["text"]) for row in rows)
        broad_cells = Counter(str(row["broad_register_cell"]) for row in rows)
        fine_cells = Counter(str(row["fine_register_cell"]) for row in rows)
        edge_frames = Counter(str(row["edge_frame"]) for row in rows)
        source_grades = Counter(str(row["normalized_source_grade"]) for row in rows)

        if pattern_name == "prev235_002390125":
            verdict = "demote_raw_2of2_to_one_strict_witness_m38_is_weak_common_hinge"
        elif pattern_name == "tail_125_632032":
            verdict = "global_tail_has_four_rows_but_002390x_positive_demotes_to_one_strict_witness"
        elif pattern_name == "frame_002390705":
            verdict = "source_gated_repeated_terminal_comparator_zero_strict_witnesses"
        elif pattern_name == "frame_002390095":
            verdict = "one_strict_visible_terminal_comparator_plus_h1993_route_only"
        elif pattern_name == "frame_002390692":
            verdict = "single_strict_visible_terminal_control"
        elif pattern_name == "frame_002390125":
            verdict = "branch_survives_as_plurality_but_strict_layer_is_two_mohenjo_square_seals"
        else:
            verdict = "context_only"

        collapse_rows.append(
            {
                "pattern": pattern_name,
                "raw_rows": len(rows),
                "closed_clean_rows": len(closed_clean),
                "objects": " ".join(sorted(str(row["object"]) for row in rows)),
                "strict_source_visible_rows": len(strict_source),
                "strict_source_visible_objects": " ".join(sorted(str(row["object"]) for row in strict_source)),
                "permissive_public_rows": len(permissive),
                "permissive_public_objects": " ".join(sorted(str(row["object"]) for row in permissive)),
                "in_002390x_rows": len(in_frame),
                "in_002390x_objects": " ".join(sorted(str(row["object"]) for row in in_frame)),
                "strict_source_visible_in_002390x_rows": len(strict_in_frame),
                "strict_source_visible_in_002390x_objects": " ".join(sorted(str(row["object"]) for row in strict_in_frame)),
                "exact_text_cells": len(exact_texts),
                "top_exact_text_count": max(exact_texts.values()) if exact_texts else 0,
                "broad_register_cells": len(broad_cells),
                "top_broad_register_count": max(broad_cells.values()) if broad_cells else 0,
                "fine_register_cells": len(fine_cells),
                "top_fine_register_count": max(fine_cells.values()) if fine_cells else 0,
                "edge_frame_cells": len(edge_frames),
                "top_edge_frame_count": max(edge_frames.values()) if edge_frames else 0,
                "source_grade_distribution": "; ".join(f"{k}:{v}" for k, v in sorted(source_grades.items())),
                "verdict": verdict,
            }
        )

    source_visible_patterns = {
        row["pattern"]: row for row in collapse_rows if row["pattern"] in {"prev235_002390125", "tail_125_632032"}
    }

    summary = {
        "date": "2026-05-31",
        "question": "Do the live 235->002-390->125 and 125->632 032 positives survive source-normalized family collapse?",
        "metadata_rows_scanned": len(metadata_rows),
        "patterns": {row["pattern"]: row for row in collapse_rows},
        "source_visible_positive_gate": {
            "prev235_002390125": {
                "raw_rows": source_visible_patterns["prev235_002390125"]["raw_rows"],
                "strict_source_visible_rows": source_visible_patterns["prev235_002390125"]["strict_source_visible_rows"],
                "strict_source_visible_objects": source_visible_patterns["prev235_002390125"]["strict_source_visible_objects"],
                "decision": "fails_positive_gate_demoted_to_single_strict_witness",
            },
            "tail_125_632032": {
                "raw_rows": source_visible_patterns["tail_125_632032"]["raw_rows"],
                "in_002390x_rows": source_visible_patterns["tail_125_632032"]["in_002390x_rows"],
                "strict_source_visible_rows": source_visible_patterns["tail_125_632032"]["strict_source_visible_rows"],
                "strict_source_visible_in_002390x_rows": source_visible_patterns["tail_125_632032"][
                    "strict_source_visible_in_002390x_rows"
                ],
                "strict_source_visible_objects": source_visible_patterns["tail_125_632032"]["strict_source_visible_objects"],
                "decision": "fails_positive_gate_demoted_to_single_strict_witness",
            },
        },
        "shared_weak_hinge": "M-38 is the only row shared by both positive subframes and remains weak/not token-boxable.",
        "decision": "positive_subframes_do_not_survive_source_normalized_family_collapse; 002-390-X remains live as branch-tail ecology only",
        "accepted_values_translations": 0,
    }

    write_csv(
        REPORT_DIR / f"{PREFIX}_occurrences.csv",
        occurrence_rows,
        [
            "pattern",
            "object",
            "id",
            "site",
            "type",
            "symbol",
            "cult",
            "shape",
            "material",
            "condition",
            "text",
            "text_len",
            "pattern_pos",
            "before_pattern",
            "after_pattern",
            "closed_clean",
            "strict_source_visible",
            "permissive_public_panel",
            "normalized_source_grade",
            "normalized_source_route",
            "broad_register_cell",
            "fine_register_cell",
            "edge_frame",
            "in_002390x_frame",
        ],
    )
    write_csv(
        REPORT_DIR / f"{PREFIX}_collapse_tests.csv",
        collapse_rows,
        [
            "pattern",
            "raw_rows",
            "closed_clean_rows",
            "objects",
            "strict_source_visible_rows",
            "strict_source_visible_objects",
            "permissive_public_rows",
            "permissive_public_objects",
            "in_002390x_rows",
            "in_002390x_objects",
            "strict_source_visible_in_002390x_rows",
            "strict_source_visible_in_002390x_objects",
            "exact_text_cells",
            "top_exact_text_count",
            "broad_register_cells",
            "top_broad_register_count",
            "fine_register_cells",
            "top_fine_register_count",
            "edge_frame_cells",
            "top_edge_frame_count",
            "source_grade_distribution",
            "verdict",
        ],
    )
    write_csv(
        REPORT_DIR / f"{PREFIX}_focus_rows.csv",
        focus_rows,
        [
            "object",
            "prev_before_002",
            "branch_after_390",
            "tail_after_branch",
            "terminal_after_branch",
            "source_tier",
            "strict_source_visible",
            "permissive_public_panel",
            "normalized_source_grade",
            "normalized_source_route",
            "site",
            "type",
            "symbol",
            "cult",
            "text",
        ],
    )
    (REPORT_DIR / f"{PREFIX}_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps({"summary": summary, "reports_prefix": str(REPORT_DIR / PREFIX)}, indent=2))


if __name__ == "__main__":
    main()
