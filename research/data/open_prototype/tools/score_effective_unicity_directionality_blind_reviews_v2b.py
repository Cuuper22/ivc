"""Scores blind reviews of the directionality packet, v2b (unique-target
controls). The packet mixes recut target images with 12 real scoring
negatives, external stress controls, synthetic leak sentinels, and synthetic
blanks, all under blind IDs. Reviewers report, per image: a visual token
count, whether a single sign band is boxable, and whether any label leaked
into the image. This script reads each review CSV (from the CLI arguments or
the default reviews directory), joins it to the answer key, and classifies
every row into a pass/fail/uncertain outcome by role. The packet gate is
strict: it fails on fewer than three reviewers, any missing or duplicate
row, any false positive or target-like uncertainty on a real negative, any
undetected leak sentinel, any accepted blank, or any disagreement between
reviewers on a target's token count. Even a clean pass increments accepted
claims by zero — this stage measures reviewer reliability, not truth. Writes
a scored-rows CSV and a JSON summary.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path.cwd()
RUN_DATE = "2026-05-29"
PACKET_ID = "directionality_no_overlay_packet_v2b_unique_target_controls"

REPORTS = ROOT / "data" / "open_prototype" / "reports"
ANSWER_KEY = REPORTS / "effective_unicity_directionality_blind_packet_v2b_answer_key.csv"
SUMMARY_IN = REPORTS / "effective_unicity_directionality_blind_packet_v2b_summary.json"
DEFAULT_REVIEW_DIR = REPORTS / "effective_unicity_directionality_blind_v2b_reviews"

OUT_ROWS = REPORTS / "effective_unicity_directionality_blind_packet_v2b_scored_rows.csv"
OUT_SUMMARY = REPORTS / "effective_unicity_directionality_blind_packet_v2b_review_summary.json"


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
    if text in {"no", "n", "false", "0", "absent", "not_boxable", "not boxable"}:
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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def review_boxable(review: dict[str, str]) -> str:
    return norm_call(
        review.get("stage1_single_signband_boxable_yes_no_uncertain", "")
        or review.get("stage1_boxable_yes_no_uncertain", "")
    )


def review_notes(review: dict[str, str]) -> str:
    return (
        review.get("stage1_notes", "")
        or review.get("stage1_uncertainty_notes", "")
        or review.get("stage1_visual_order_note", "")
    )


def empty_outputs(status: str) -> None:
    summary = {
        "date": RUN_DATE,
        "packet_id": PACKET_ID,
        "status": status,
        "reviewer_count": 0,
        "accepted_claims_increment": 0,
        "interpretation_boundary": "No review set was scored; no false-positive rate or promotion follows.",
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


def main() -> None:
    key_rows = parse_csv(ANSWER_KEY)
    key_by_id = {row["blind_id"]: row for row in key_rows}
    packet_summary = json.loads(SUMMARY_IN.read_text(encoding="utf-8"))
    paths = review_paths(sys.argv[1:])

    if not paths:
        empty_outputs("not_scored_no_review_csvs_found")
        return

    expected_real_negative_ids = {
        row["blind_id"] for row in key_rows if row["role"] == "scoring_negative_real"
    }
    expected_target_ids = {
        row["blind_id"] for row in key_rows if row["role"] == "primary_target_recut"
    }
    expected_leak_sentinels = {
        row["blind_id"] for row in key_rows if row["role"] == "synthetic_leak_sentinel_auxiliary"
    }
    expected_blank_controls = {
        row["blind_id"] for row in key_rows if row["role"] == "synthetic_blank_auxiliary"
    }
    fixed_real_denominator = len(expected_real_negative_ids)

    scored_rows: list[dict[str, object]] = []
    reviewer_summaries: list[dict[str, object]] = []
    target_counts_by_cisi: dict[str, list[dict[str, object]]] = defaultdict(list)
    duplicate_review_rows: list[dict[str, str]] = []

    for path in paths:
        reviewer = reviewer_name(path)
        rows = parse_csv(path)
        seen: set[str] = set()
        counts = {
            "target_pass": 0,
            "target_fail": 0,
            "target_uncertain": 0,
            "real_negative_true_negative": 0,
            "real_negative_hard_false_positive": 0,
            "real_negative_uncertain_target_like": 0,
            "real_negative_label_leak": 0,
            "external_stress_true_negative": 0,
            "external_stress_hard_false_positive": 0,
            "external_stress_uncertain": 0,
            "synthetic_leak_sentinel_pass": 0,
            "synthetic_leak_sentinel_fail": 0,
            "synthetic_blank_pass": 0,
            "synthetic_blank_fail": 0,
            "missing_rows": 0,
            "unknown_rows": 0,
            "duplicate_rows": 0,
        }

        for review in rows:
            blind_id = review.get("blind_id", "").strip()
            if not blind_id:
                continue
            if blind_id in seen:
                counts["duplicate_rows"] += 1
                duplicate_review_rows.append({"reviewer": reviewer, "blind_id": blind_id})
                continue
            seen.add(blind_id)

            key = key_by_id.get(blind_id)
            if not key:
                counts["unknown_rows"] += 1
                continue

            role = key["role"]
            expected = int(key["expected_token_count"])
            review_count = numeric_count(review.get("stage1_visual_token_count", ""))
            count_match = review_count == expected if review_count is not None else False
            boxable = review_boxable(review)
            leak = norm_call(review.get("stage1_label_leak_yes_no", ""))
            notes = review_notes(review)
            outcome = "not_scored"

            if role == "primary_target_recut":
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
                target_counts_by_cisi[key["cisi"]].append(
                    {
                        "reviewer": reviewer,
                        "blind_id": blind_id,
                        "review_token_count": review_count,
                        "expected_token_count": expected,
                        "boxable_call": boxable,
                        "label_leak_call": leak,
                        "outcome": outcome,
                    }
                )
            elif role == "scoring_negative_real":
                if leak == "yes":
                    outcome = "real_negative_label_leak_packet_fail"
                    counts["real_negative_label_leak"] += 1
                elif boxable == "yes" and count_match:
                    outcome = "real_negative_hard_false_positive"
                    counts["real_negative_hard_false_positive"] += 1
                elif boxable == "uncertain":
                    outcome = "real_negative_uncertain_target_like_packet_fail"
                    counts["real_negative_uncertain_target_like"] += 1
                else:
                    outcome = "real_negative_true_negative"
                    counts["real_negative_true_negative"] += 1
            elif role == "external_stress_control":
                if boxable == "yes" and count_match:
                    outcome = "external_stress_hard_false_positive_not_denominator"
                    counts["external_stress_hard_false_positive"] += 1
                elif boxable == "uncertain":
                    outcome = "external_stress_uncertain_not_denominator"
                    counts["external_stress_uncertain"] += 1
                else:
                    outcome = "external_stress_true_negative_not_denominator"
                    counts["external_stress_true_negative"] += 1
            elif role == "synthetic_leak_sentinel_auxiliary":
                if leak == "yes":
                    outcome = "synthetic_leak_sentinel_pass"
                    counts["synthetic_leak_sentinel_pass"] += 1
                else:
                    outcome = "synthetic_leak_sentinel_fail_packet_fail"
                    counts["synthetic_leak_sentinel_fail"] += 1
            elif role == "synthetic_blank_auxiliary":
                if leak != "yes" and boxable == "no":
                    outcome = "synthetic_blank_pass"
                    counts["synthetic_blank_pass"] += 1
                else:
                    outcome = "synthetic_blank_fail_packet_fail"
                    counts["synthetic_blank_fail"] += 1

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
                    "scored_outcome": "missing_review_row_packet_fail",
                    "notes": "",
                }
            )

        missing_real_negative_rows = len(expected_real_negative_ids - seen)
        missing_target_rows = len(expected_target_ids - seen)
        missing_leak_sentinels = len(expected_leak_sentinels - seen)
        missing_blank_controls = len(expected_blank_controls - seen)

        reviewer_summaries.append(
            {
                "reviewer": reviewer,
                "review_path": rel(path),
                **counts,
                "fixed_real_negative_denominator": fixed_real_denominator,
                "missing_real_negative_rows": missing_real_negative_rows,
                "missing_target_rows": missing_target_rows,
                "missing_synthetic_leak_sentinels": missing_leak_sentinels,
                "missing_synthetic_blank_controls": missing_blank_controls,
                "yes_only_fpr_fixed_denominator": rate(
                    counts["real_negative_hard_false_positive"], fixed_real_denominator
                ),
                "conservative_fpr_fixed_denominator": rate(
                    counts["real_negative_hard_false_positive"]
                    + counts["real_negative_uncertain_target_like"],
                    fixed_real_denominator,
                ),
            }
        )

    failed_reasons: list[str] = []
    if len(reviewer_summaries) < 3:
        failed_reasons.append("fewer_than_three_independent_reviews")
    if packet_summary["counts"].get("duplicate_blind_image_hash_groups", 0):
        failed_reasons.append("duplicate_blind_image_hash_groups_present")
    if fixed_real_denominator != 12:
        failed_reasons.append("fixed_real_negative_denominator_not_12")
    if packet_summary["counts"].get("scoring_negative_real_unique_cisis") != 12:
        failed_reasons.append("packet_real_negative_unique_cisis_not_12")
    if any(row["missing_rows"] for row in reviewer_summaries):
        failed_reasons.append("missing_review_rows")
    if any(row["unknown_rows"] for row in reviewer_summaries):
        failed_reasons.append("unknown_review_rows")
    if any(row["duplicate_rows"] for row in reviewer_summaries):
        failed_reasons.append("duplicate_review_rows")
    if any(row["real_negative_label_leak"] for row in reviewer_summaries):
        failed_reasons.append("real_negative_label_leak_packet_fail")
    if any(row["missing_real_negative_rows"] for row in reviewer_summaries):
        failed_reasons.append("missing_real_negative_rows_packet_fail")
    if any(row["real_negative_hard_false_positive"] for row in reviewer_summaries):
        failed_reasons.append("real_negative_hard_false_positive")
    if any(row["real_negative_uncertain_target_like"] for row in reviewer_summaries):
        failed_reasons.append("real_negative_uncertain_target_like")
    if any(row["target_fail"] or row["target_uncertain"] for row in reviewer_summaries):
        failed_reasons.append("not_all_targets_cleanly_recovered")
    if any(row["synthetic_leak_sentinel_fail"] for row in reviewer_summaries):
        failed_reasons.append("synthetic_leak_sentinel_not_detected")
    if any(row["missing_synthetic_leak_sentinels"] for row in reviewer_summaries):
        failed_reasons.append("missing_synthetic_leak_sentinel_rows")
    if any(row["synthetic_blank_fail"] for row in reviewer_summaries):
        failed_reasons.append("synthetic_blank_control_not_rejected")
    if any(row["missing_synthetic_blank_controls"] for row in reviewer_summaries):
        failed_reasons.append("missing_synthetic_blank_rows")

    target_variance_failures: dict[str, list[object]] = {}
    for cisi, rows in target_counts_by_cisi.items():
        observed = [row["review_token_count"] for row in rows]
        if len(observed) != len(reviewer_summaries) or len(set(observed)) != 1:
            target_variance_failures[cisi] = observed
    if target_variance_failures:
        failed_reasons.append("inter_reviewer_target_count_variance_nonzero")

    summary = {
        "date": RUN_DATE,
        "packet_id": PACKET_ID,
        "status": "scored_reviews_present_not_acceptance_by_itself",
        "reviewer_count": len(reviewer_summaries),
        "reviewer_summaries": reviewer_summaries,
        "target_counts_by_cisi": target_counts_by_cisi,
        "target_variance_failures": target_variance_failures,
        "duplicate_review_rows": duplicate_review_rows,
        "fixed_real_negative_denominator": fixed_real_denominator,
        "max_yes_only_fpr_fixed_denominator": max(
            [
                row["yes_only_fpr_fixed_denominator"]
                for row in reviewer_summaries
                if row["yes_only_fpr_fixed_denominator"] is not None
            ],
            default=None,
        ),
        "max_conservative_fpr_fixed_denominator": max(
            [
                row["conservative_fpr_fixed_denominator"]
                for row in reviewer_summaries
                if row["conservative_fpr_fixed_denominator"] is not None
            ],
            default=None,
        ),
        "promotion_gate_decision": (
            "failed_packet_gate_no_promotion"
            if failed_reasons
            else "passes_packet_gate_no_claim_increment"
        ),
        "promotion_gate_failed_reasons": failed_reasons,
        "accepted_claims_increment": 0,
        "interpretation_boundary": (
            "This scorer only measures blind image boxability, target token-count stability, label leakage, "
            "and false-positive behavior under a fixed 12-real-negative denominator. It cannot assign signs, "
            "sounds, meanings, language, translation, source direction, or accepted structural status."
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
