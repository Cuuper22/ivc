# M-381 Blind Adjudication Result

Date: 2026-05-29

This note records what happened when three reviewers looked at one seal photograph without being told what was on it, and why that killed a control we wanted to use.

Terms first. M-381 is a Mohenjo-daro artifact. A "source-box" is a box drawn on a published object photograph around each sign a reviewer can see; "tokenization" is the act of drawing those boxes, one per sign. "Blind" means the reviewer had the image only, with no catalog text or object identity. "Adjudication" is the scored decision that follows. A "negative control" is an object picked because its catalog text lacks the pattern under test — useful only if the image can actually show that absence. Numbers like `220`, `032`, and `002` are Lipi catalog sign codes, not readings. A "gate" is a recorded checkpoint that either lets a claim through or blocks it.

Decision: failed clean-negative gate.

M-381 cannot currently be used as a clean `negative_220_032_next_not_002` source-box control from the public crop. It remains useful as an ambiguity stress packet — material for measuring how uncertain reviewers get, rather than for settling a claim.

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

A skeptic audit is a deliberate attempt to argue the result down. "Promotion" would mean moving this object to a stronger status in the project's ledger.

Fatal for promotion:

- No blind reviewer recovered the seven-token catalog segmentation from the source crop.
- Every blind reviewer reported a region where a cataloguer could plausibly merge or skip a boundary.
- The negative-control question requires stable visual separation before catalog alignment; the blind tokenization is unstable before that alignment.
- The crop is an enhanced public reproduction crop, not a fresh high-resolution source photograph.

Nonfatal but important:

- All reviewers agree that the signband — the strip of the photograph holding the inscription — is real and visually usable enough for ambiguity calibration.
- The panel remains worth pursuing with a sharper source image or independent plate route.

## Ledger Boundary

The ledger is the project's running record of accepted findings.

Accepted-claim increments: zero.

This result does not revive the retracted source-visible `032-002-Y` packet method. It strengthens the adversarial apparatus by showing that a superficially promising negative can fail under blind tokenization.
