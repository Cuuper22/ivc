import csv
import json
import statistics
from pathlib import Path


ROOT = Path.cwd()
REPORTS = ROOT / "data" / "open_prototype" / "reports"
REVIEWS_CSV = REPORTS / "source_box_negative_control_v2_m381_blind_reviews.csv"
ANSWER_KEY_CSV = REPORTS / "source_box_negative_control_v2_m381_answer_key.csv"
SCORED_CSV = REPORTS / "source_box_negative_control_v2_m381_scored_reviews.csv"
SUMMARY_JSON = REPORTS / "source_box_negative_control_v2_m381_adjudication_summary.json"
RUN_DATE = "2026-05-29"


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_catalog_token_count(target_text):
    stripped = target_text.strip().strip("+")
    return len([token for token in stripped.split("-") if token])


def main():
    reviews = read_rows(REVIEWS_CSV)
    answer_key = read_rows(ANSWER_KEY_CSV)[0]
    catalog_count = parse_catalog_token_count(answer_key["target_text"])
    scored = []
    token_counts = []
    for review in reviews:
        token_count = int(review["token_count"])
        token_counts.append(token_count)
        matches_catalog_count = token_count == catalog_count
        fusion_risk = review["fusion_risk"].strip().lower() == "yes"
        scored.append(
            {
                "date": RUN_DATE,
                "packet_id": review["packet_id"],
                "reviewer": review["reviewer"],
                "blind_token_count": token_count,
                "catalog_token_count": catalog_count,
                "matches_catalog_token_count": str(matches_catalog_count).lower(),
                "fusion_risk": str(fusion_risk).lower(),
                "fusion_risk_zone": review["fusion_risk_zone"],
                "clean_negative_gate": "fail",
                "reason": (
                    "Blind token count does not match catalog count and reviewer reports fusion risk"
                    if fusion_risk and not matches_catalog_count
                    else "Review does not provide a clean source-box negative"
                ),
                "accepted_claims_increment": 0,
            }
        )

    token_counts_sorted = sorted(token_counts)
    summary = {
        "date": RUN_DATE,
        "packet_id": answer_key["packet_id"],
        "status": "failed_clean_negative_gate",
        "reviewers": len(reviews),
        "catalog_token_count": catalog_count,
        "blind_token_counts": token_counts,
        "blind_token_count_min": min(token_counts),
        "blind_token_count_median": statistics.median(token_counts),
        "blind_token_count_max": max(token_counts),
        "distinct_blind_token_counts": sorted(set(token_counts)),
        "reviewers_matching_catalog_token_count": sum(1 for n in token_counts if n == catalog_count),
        "reviewers_reporting_fusion_risk": sum(1 for row in scored if row["fusion_risk"] == "true"),
        "all_reviewers_report_fusion_risk": all(row["fusion_risk"] == "true" for row in scored),
        "all_reviewers_over_catalog_count": all(n > catalog_count for n in token_counts),
        "decision": (
            "M-381 cannot be used as a clean negative_220_032_next_not_002 control from this crop. "
            "It remains an ambiguity stress packet, not a promoted blind negative."
        ),
        "skeptic_attacks_that_break_promotion": [
            "No blind reviewer recovered the seven-token catalog segmentation from the source crop.",
            "All blind reviewers reported skip/merge risk in crowded sign regions.",
            "The critical question requires proving a stable intervening token between catalog 032 and catalog 002, but the blind visual segmentation is unstable before catalog alignment.",
            "The public crop is an enhanced reproduction crop, not a fresh high-resolution source photograph.",
        ],
        "residual_value": (
            "The panel is useful for calibrating false-positive visual packeting and for requesting a sharper source image, "
            "but not for rehabilitating the retracted source-visible 032-002-Y method."
        ),
        "accepted_claims_increment": 0,
        "files": {
            "blind_reviews": str(REVIEWS_CSV.relative_to(ROOT)).replace("\\", "/"),
            "scored_reviews": str(SCORED_CSV.relative_to(ROOT)).replace("\\", "/"),
            "answer_key": str(ANSWER_KEY_CSV.relative_to(ROOT)).replace("\\", "/"),
        },
    }

    with SCORED_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(scored[0].keys()))
        writer.writeheader()
        writer.writerows(scored)
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
