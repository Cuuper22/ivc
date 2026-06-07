# M-381 Blind Adjudication Result

Date: 2026-05-29

Decision: failed clean-negative gate.

M-381 cannot currently be used as a clean `negative_220_032_next_not_002` source-box control from the public crop. It remains useful as an ambiguity stress packet.

## Evidence

- `data/open_prototype/reports/source_box_negative_control_v2_m381_blind_reviews.csv`
- `data/open_prototype/reports/source_box_negative_control_v2_m381_blind_review_boxes.csv`
- `data/open_prototype/reports/source_box_negative_control_v2_m381_scored_reviews.csv`
- `data/open_prototype/reports/source_box_negative_control_v2_m381_adjudication_summary.json`

## Blind Review Results

| Reviewer | Blind token count | Fusion / skip risk |
| --- | ---: | --- |
| Helmholtz | 9 | yes: boxes 7-8 and internally fused box 8 |
| Cicero | 13 | yes: boxes 10-12 and boxes 3-7 |
| Gibbs | 9 | yes: tokens 6-8 and possible token 4 dash |

Catalog token count from the answer key: 7.

Reviewers matching catalog token count: 0 / 3.

Reviewers reporting fusion risk: 3 / 3.

## Skeptic Audit

Fatal for promotion:

- No blind reviewer recovered the seven-token catalog segmentation from the source crop.
- Every blind reviewer reported a region where a cataloguer could plausibly merge or skip a boundary.
- The negative-control question requires stable visual separation before catalog alignment; the blind tokenization is unstable before that alignment.
- The crop is an enhanced public reproduction crop, not a fresh high-resolution source photograph.

Nonfatal but important:

- All reviewers agree that the signband is real and visually usable enough for ambiguity calibration.
- The panel remains worth pursuing with a sharper source image or independent plate route.

## Ledger Boundary

Accepted-claim increments: zero.

This result does not revive the retracted source-visible `032-002-Y` packet method. It strengthens the adversarial apparatus by showing that a superficially promising negative can fail under blind tokenization.
