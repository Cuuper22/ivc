"""Scores blind reviews of the directionality packet, v1. Reviewers saw seal
image crops under blind IDs — some primary targets, some scoring negatives,
some quarantined — and reported a visual token count, whether a single sign
band is boxable, and whether any identifying label leaked into the image.
This script joins each review CSV (CLI arguments, or the default reviews
directory) to the answer key and classifies each row: targets pass only when
boxable with the exact expected token count and no leak; scoring negatives
called boxable-with-matching-count are hard false positives. Per reviewer it
computes a yes-only and a conservative (uncertainty-counting) false-positive
rate. The packet gate fails on fewer than two reviewers, a negative
denominator below the planned floor, any hard false positive, or any target
not cleanly recovered — and even a pass adds zero accepted claims. Writes a
scored-rows CSV and a JSON summary. Superseded by the v2b scorer, which adds
synthetic sentinels and a fixed negative denominator.
"""
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path.cwd()
RUN_DATE = "2026-05-29"
PACKET_ID = "directionality_no_overlay_packet_v1"

REPORTS = ROOT / "data" / "open_prototype" / "reports"
ANSWER_KEY = REPORTS / "effective_unicity_directionality_blind_packet_answer_key.csv"
SUMMARY_IN = REPORTS / "effective_unicity_directionality_blind_packet_summary.json"
DEFAULT_REVIEW_DIR = REPORTS / "effective_unicity_directionality_blind_reviews"

OUT_ROWS = REPORTS / "effective_unicity_directionality_blind_packet_scored_rows.csv"
OUT_SUMMARY = REPORTS / "effective_unicity_directionality_blind_packet_review_summary.json"


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def norm_call(value: str) -> str:
    text = str(value or "").strip().lower()
    if text in {"yes", "y", "true", "1", "present", "boxable"}:
        return "yes"
    if text in {"no", "n", "false", "0", "absent", "not_boxable"}:
        return "no"
    if text in {"uncertain", "maybe", "ambiguous", "?", "unknown", "partial"}:
        return "uncertain"
    return text or "missing"


def numeric_count(value: str) -> int | None:
    match = re.search(r"\d+", str(value or ""))
    return int(match.group(0)) if match else None


def review_paths(argv: list[str]) -> list[Path]:
    if argv:
        return [Path(arg).resolve() for arg in argv]
    if not DEFAULT_REVIEW_DIR.exists():
        return []
    return sorted(DEFAULT_REVIEW_DIR.glob("*.csv"))


def reviewer_name(path: Path) -> str:
    return path.stem


def rate(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def main() -> None:
    import sys

    key_rows = parse_csv(ANSWER_KEY)
    key_by_id = {row["blind_id"]: row for row in key_rows}
    packet_summary = json.loads(SUMMARY_IN.read_text(encoding="utf-8"))
    paths = review_paths(sys.argv[1:])

    if not paths:
        summary = {
            "date": RUN_DATE,
            "packet_id": PACKET_ID,
            "status": "not_scored_no_review_csvs_found",
            "reviewer_count": 0,
            "accepted_claims_increment": 0,
            "interpretation_boundary": "No reviews were found; no false-positive rate or promotion follows.",
        }
        OUT_SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        write_csv(
            OUT_ROWS,
            [],
            [
                "reviewer",
                "blind_id",
                "cisi",
                "source_view",
                "role",
                "expected_token_count",
                "review_token_count",
                "count_match",
                "boxable_call",
                "label_leak_call",
                "scored_outcome",
                "notes",
            ],
        )
        print(json.dumps(summary, indent=2))
        return

    scored_rows: list[dict[str, object]] = []
    reviewer_summaries: list[dict[str, object]] = []
    target_object_view_results: dict[str, list[dict[str, object]]] = defaultdict(list)

    for path in paths:
        reviewer = reviewer_name(path)
        rows = parse_csv(path)
        seen = set()
        counts = {
            "target_pass": 0,
            "target_fail": 0,
            "target_uncertain": 0,
            "scoring_negative_true_negative": 0,
            "scoring_negative_hard_false_positive": 0,
            "scoring_negative_uncertain_target_like": 0,
            "scoring_negative_label_leak_excluded": 0,
            "quarantine_rows": 0,
            "missing_rows": 0,
        }
        for review in rows:
            blind_id = review.get("blind_id", "")
            if not blind_id:
                continue
            seen.add(blind_id)
            key = key_by_id.get(blind_id)
            if not key:
                raise SystemExit(f"{path} contains unknown blind_id {blind_id}")
            role = key["role"]
            expected = int(key["expected_token_count"])
            review_count = numeric_count(review.get("stage1_visual_token_count", ""))
            count_match = review_count == expected if review_count is not None else False
            boxable = norm_call(review.get("stage1_boxable_yes_no_uncertain", ""))
            leak = norm_call(review.get("stage1_label_leak_yes_no", ""))
            notes = review.get("stage1_uncertainty_notes", "") or review.get("stage1_visual_order_note", "")
            outcome = "not_scored"
            if role == "primary_target":
                if leak == "yes":
                    outcome = "target_label_leak_fail"
                    counts["target_fail"] += 1
                elif boxable == "yes" and count_match:
                    outcome = "target_count_boxable_pass"
                    counts["target_pass"] += 1
                elif boxable == "uncertain" or review_count is None:
                    outcome = "target_uncertain"
                    counts["target_uncertain"] += 1
                else:
                    outcome = "target_fail"
                    counts["target_fail"] += 1
                target_object_view_results[f"{reviewer}:{key['cisi']}"].append(
                    {
                        "blind_id": blind_id,
                        "source_view": key["source_view"],
                        "outcome": outcome,
                        "review_token_count": review_count,
                        "expected_token_count": expected,
                        "boxable_call": boxable,
                        "label_leak_call": leak,
                    }
                )
            elif role == "scoring_negative":
                if leak == "yes":
                    outcome = "negative_label_leak_excluded"
                    counts["scoring_negative_label_leak_excluded"] += 1
                elif boxable == "yes" and count_match:
                    outcome = "hard_false_positive_count_boxable_negative"
                    counts["scoring_negative_hard_false_positive"] += 1
                elif boxable == "uncertain":
                    outcome = "uncertain_target_like_negative"
                    counts["scoring_negative_uncertain_target_like"] += 1
                else:
                    outcome = "true_negative"
                    counts["scoring_negative_true_negative"] += 1
            elif role == "quarantine_negative":
                outcome = "quarantine_not_in_fpr"
                counts["quarantine_rows"] += 1
            scored_rows.append(
                {
                    "reviewer": reviewer,
                    "blind_id": blind_id,
                    "cisi": key["cisi"],
                    "source_view": key["source_view"],
                    "role": role,
                    "expected_token_count": expected,
                    "review_token_count": "" if review_count is None else review_count,
                    "count_match": count_match,
                    "boxable_call": boxable,
                    "label_leak_call": leak,
                    "scored_outcome": outcome,
                    "notes": notes,
                }
            )
        for blind_id, key in key_by_id.items():
            if blind_id in seen:
                continue
            counts["missing_rows"] += 1
            scored_rows.append(
                {
                    "reviewer": reviewer,
                    "blind_id": blind_id,
                    "cisi": key["cisi"],
                    "source_view": key["source_view"],
                    "role": key["role"],
                    "expected_token_count": key["expected_token_count"],
                    "review_token_count": "",
                    "count_match": False,
                    "boxable_call": "missing",
                    "label_leak_call": "missing",
                    "scored_outcome": "missing_review_row",
                    "notes": "",
                }
            )
        denominator_yes_only = (
            counts["scoring_negative_hard_false_positive"]
            + counts["scoring_negative_true_negative"]
        )
        denominator_conservative = (
            counts["scoring_negative_hard_false_positive"]
            + counts["scoring_negative_true_negative"]
            + counts["scoring_negative_uncertain_target_like"]
        )
        reviewer_summaries.append(
            {
                "reviewer": reviewer,
                "review_path": str(path.relative_to(ROOT)).replace("\\", "/") if path.is_relative_to(ROOT) else str(path),
                **counts,
                "yes_only_fpr": rate(counts["scoring_negative_hard_false_positive"], denominator_yes_only),
                "conservative_fpr": rate(
                    counts["scoring_negative_hard_false_positive"]
                    + counts["scoring_negative_uncertain_target_like"],
                    denominator_conservative,
                ),
            }
        )

    failed_reasons = []
    if len(reviewer_summaries) < 2:
        failed_reasons.append("fewer_than_two_independent_reviews")
    current_negative_n = packet_summary["counts"]["scoring_negative_unique_cisis"]
    if current_negative_n < packet_summary.get("forger_control_plan", {}).get("promotion_denominator_floor", 10):
        failed_reasons.append("below_forger_real_negative_denominator_floor")
    if any(row["scoring_negative_hard_false_positive"] for row in reviewer_summaries):
        failed_reasons.append("scoring_negatives_produced_hard_count_boxable_false_positives")
    if any(row["target_fail"] or row["target_uncertain"] for row in reviewer_summaries):
        failed_reasons.append("not_all_targets_cleanly_recovered")

    summary = {
        "date": RUN_DATE,
        "packet_id": PACKET_ID,
        "status": "scored_reviews_present_not_acceptance_by_itself",
        "reviewer_count": len(reviewer_summaries),
        "reviewer_summaries": reviewer_summaries,
        "target_object_view_results": target_object_view_results,
        "max_yes_only_fpr": max(
            [row["yes_only_fpr"] for row in reviewer_summaries if row["yes_only_fpr"] is not None],
            default=None,
        ),
        "max_conservative_fpr": max(
            [row["conservative_fpr"] for row in reviewer_summaries if row["conservative_fpr"] is not None],
            default=None,
        ),
        "promotion_gate_decision": "failed_packet_gate_no_promotion" if failed_reasons else "passes_packet_gate_no_claim_increment",
        "promotion_gate_failed_reasons": failed_reasons,
        "accepted_claims_increment": 0,
        "interpretation_boundary": (
            "This review scoring only measures blind crop boxability, token-count recovery, label leakage, "
            "and false-positive behavior for selected source-normalization candidates. It cannot assign "
            "signs, sounds, meanings, language, translation, or accepted structural status."
        ),
    }

    write_csv(
        OUT_ROWS,
        scored_rows,
        [
            "reviewer",
            "blind_id",
            "cisi",
            "source_view",
            "role",
            "expected_token_count",
            "review_token_count",
            "count_match",
            "boxable_call",
            "label_leak_call",
            "scored_outcome",
            "notes",
        ],
    )
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
