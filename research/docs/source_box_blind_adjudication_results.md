# Source-Box Blind Adjudication Results

Date: 2026-05-29

## Verdict

The blind source-box adjudication failed the `032-002-Y` source-visible packet candidate.

This does not disprove every catalog-level `032-002-Y` pattern. It does invalidate the current visual packeting method as support for the claim that the source-visible rows are secure enough to weaken the catalog-adjacency objection.

## Inputs

- Packet: `data/open_prototype/reports/source_box_blind_adjudication_packet.csv`
- Key: `data/open_prototype/reports/source_box_blind_adjudication_key.csv`
- Reviews:
  - `data/open_prototype/reports/source_box_blind_reviews/heisenberg_review.csv`
  - `data/open_prototype/reports/source_box_blind_reviews/jason_review.csv`
- Scorer: `data/open_prototype/tools/score_source_box_blind_adjudication.mjs`
- Scored rows: `data/open_prototype/reports/source_box_blind_adjudication_scored_rows.csv`
- Summary: `data/open_prototype/reports/source_box_blind_adjudication_summary.json`

## Results

| Reviewer | TP | FP | TN | FN | Uncertain positive | Uncertain negative | Yes-only FPR | Conservative negative-failure rate | Yes-only sensitivity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Heisenberg | 0 | 4 | 6 | 5 | 3 | 2 | 0.400000 | 0.500000 | 0.000000 |
| Jason | 0 | 3 | 7 | 6 | 2 | 2 | 0.300000 | 0.416667 | 0.000000 |

Definitions:

- Yes-only false-positive rate: `false_positive / (false_positive + true_negative)`.
- Conservative negative-failure rate: `(false_positive + uncertain_negative) / all negatives`.
- Yes-only sensitivity: `true_positive / (true_positive + false_negative)`.

## Failure Mode

The reviewers called no positives as confident positives. They also called three to four negatives as positives. That is the killer combination: the visual features used for packet recognition are not specific enough, while the actual positive packet images are not recoverable under blind review.

Common false-positive negatives:

- `SBP1_006` / `M-32`, catalog `+390-003-002-817+`
- `SBP1_020` / `M-17`, catalog `+390-016-002-814-560+`

Additional false positives:

- `SBP1_003` / `C-3`, catalog `+740-016-002-920-317+` for one reviewer
- `SBP1_011` / `M-77`, catalog `+832-390-803-002-861+` for one reviewer
- `SBP1_018` / `C-1`, catalog `+031-840-140-740-101-002-365-287-034+` for one reviewer

## Claim Consequence

The ledger must not accept the source-visible `032-002-Y` packet claim.

The honest conclusion is:

The current source-image packeting process can generate visually plausible `032-002-Y` calls in negative controls at rates comparable to or worse than its recovery of positives. The method is invalid for claim acceptance until rebuilt with better source crops, a pre-registered sign-shape guide, and local image-backed `220-032` not followed by `002` controls.

Accepted claim count remains zero.
