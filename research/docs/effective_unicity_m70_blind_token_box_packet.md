# Effective-Unicity M-70 Blind Token-Box Packet

Date: 2026-05-29

This packet is a forger gate for the M-70 source pilot. It does not promote a reading, sign value, semantic value, physical source direction, language identification, or accepted structural claim.

## Null Question

Can M-70's broad `032-002-390-692` order window be separated from matched source and metadata false positives produced by the same broad-window procedure on rows with comparable site, type, length, and local-image availability but without the same catalog-slot adjacency?

## Artifacts

- Builder: `data/open_prototype/tools/effective_unicity_m70_blind_token_box_packet.py`
- Summary: `data/open_prototype/reports/effective_unicity_m70_blind_token_box_packet_summary.json`
- Blind manifest: `data/open_prototype/reports/effective_unicity_m70_blind_token_box_manifest.csv`
- Answer key: `data/open_prototype/reports/effective_unicity_m70_blind_token_box_answer_key.csv`
- Review template: `data/open_prototype/reports/effective_unicity_m70_blind_token_box_review_template.csv`
- Review scorer: `data/open_prototype/tools/score_effective_unicity_m70_blind_token_box_reviews.mjs`
- Review summary: `data/open_prototype/reports/effective_unicity_m70_blind_token_box_review_summary.json`
- Scored review rows: `data/open_prototype/reports/effective_unicity_m70_blind_token_box_scored_rows.csv`
- Contact sheet: `tmp/effective_unicity_m70_blind_packet/m70_blind_token_box_contact_sheet.png`
- Blind image directory: `tmp/effective_unicity_m70_blind_packet/blind_images/`

## Packet Composition

- 15 blind items total.
- 2 primary M-70 target views: face and impression.
- 3 positive calibration rows: M-49, M-240, M-91.
- 9 scoring-negative images across 7 unique CISI controls: M-77, M-17, M-32, M-315, M-1273, M-376, M-381.
- 1 quarantine negative: M-683, included to diagnose reviewer behavior but excluded from false-positive denominators until source-cropped cleanly.

The control set implements the forger sidecar's matched-negative design: same broad site/type/source-availability neighborhood where possible, but without the target `032-002-390-692` catalog-slot adjacency. M-40 and M-1825 stay acquisition-gated because no local source image is available in the checked layer. M-75 is not included because the available local image is page-level and label/context leaking.

## Promotion Threshold

M-70 can move beyond broad order-window status only if all of these hold:

- Two or more independent blind reviews recover a five-token M-70 signband on both face and impression before seeing the answer key.
- Reviewers mark a stable adjacent-pair/order window for M-70 within pre-set tolerance.
- At least six unique scoring-negative rows remain reviewable after blind quality screening.
- Scoring negatives produce zero hard target-like hits.
- One soft ambiguous partial hit is allowed only if it is adjudicated as damage, cropping, or non-comparable source quality before unblinding.

Even if those pass, the maximum promotion is `source-boxed order-window candidate`. No accepted claim count changes.

## Review Results

Two independent blind reviews were scored with `data/open_prototype/tools/score_effective_unicity_m70_blind_token_box_reviews.mjs`.

| Reviewer | Target yes | Target uncertain | Scoring-negative yes | Scoring-negative no | Scoring-negative uncertain | Yes-only FPR | Conservative FPR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `avicenna_review` | 2 | 0 | 5 | 2 | 2 | 0.714286 | 0.777778 |
| `ohm_review` | 1 | 1 | 5 | 4 | 0 | 0.555556 | 0.555556 |

Gate decision: `failed_packet_gate_no_promotion`.

Reasons:

- Not all M-70 targets were strictly recovered; reviewer `ohm_review` marked the face target uncertain.
- Both reviewers produced hard target-like hits on scoring negatives.
- Maximum yes-only false-positive rate across reviewers is 0.714286.
- Maximum conservative false-positive-or-uncertain rate across reviewers is 0.777778.

Interpretation: the packet blocks promotion of M-70 beyond the prior broad order-window source-visible status. It does not falsify that M-70 is row-level source-visible, but it invalidates this blind-boxing method as support for a source-boxed order-window candidate.

## Retraction Triggers

Retract any promotion if the face/impression pairing breaks, the supposed window crosses damage, edge, label, or a second unit, blind boxes cannot separate the needed catalog slots, controls produce the same apparent hit pattern, or the result depends on choosing image orientation after metadata is visible.
