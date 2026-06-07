# Effective-Unicity Directionality No-Overlay Blind Packet v2b

Date: 2026-05-29

## Purpose

The first no-overlay packet failed because it had too few real controls, one leaked negative label, hard false positives, and unstable target token counts. A second packet (`v2`) repaired the denominator but failed preflight because paired target views were byte-identical. This `v2b` packet removes duplicate target images and keeps the fixed 12-row real-negative denominator.

This is still a source-normalization gate only. It does not validate physical reading direction, token order, sign identity, sign meaning, language family, phonetic value, or translation.

## Packet

Packet ID: `directionality_no_overlay_packet_v2b_unique_target_controls`

| Role | Count |
| --- | ---: |
| Blind items | 23 |
| Primary target images | 4 |
| Primary target unique CISI IDs | 4 |
| Real scoring-negative images | 12 |
| Real scoring-negative unique CISI IDs | 12 |
| External stress-control images | 3 |
| Auxiliary synthetic-control images | 4 |
| Duplicate blind image hash groups | 0 |
| Accepted claim increment | 0 |

Primary target recuts: `H-654`, `M-1310`, `M-1320`, and `M-811`.

Fixed real-negative denominator: `H-158`, `H-665`, `M-1315`, `M-1458`, `M-1523`, `M-171`, `M-365`, `M-386`, `M-525`, `M-527`, `M-534`, and `M-567`.

External stress controls: `M-1273`, `M-376`, and `M-381`.

Auxiliary synthetic controls: two deliberate label-leak sentinels and two blank/non-script controls. They never count toward the real-negative denominator.

## Forger Boundary

The packet met the mechanical preflight that v1 and v2 missed:

| Gate | Status |
| --- | --- |
| At least 12 unique real routed negatives | Met |
| At least 10 real negatives after exclusions | Failed by policy, because exclusions are not allowed |
| Zero duplicate blind image hashes | Met |
| At least three blind reviewers | Met |
| Synthetic leak sentinels detected | Met |
| Synthetic blanks rejected | Met |
| Real denominator label-leak free | Failed |
| Real negatives with zero hard/uncertain target-like hits | Failed under conservative scoring |
| All targets cleanly recovered with zero variance | Failed |
| Accepted claim increment | 0 |

The fixed-denominator policy matters: real-negative leaks are not denominator exclusions. They fail the packet.

## Blind Review Result

Three blind reviews were scored against the fixed 12-row real-negative denominator.

| Reviewer | Target pass | Target fail | Target uncertain | Real true negatives | Real hard false positives | Real uncertain target-like | Real label leaks | Yes-only FPR / 12 | Conservative FPR / 12 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `reviewer_a` | 1 | 3 | 0 | 7 | 0 | 0 | 5 | 0.000000 | 0.000000 |
| `reviewer_b` | 1 | 2 | 1 | 7 | 0 | 0 | 5 | 0.000000 | 0.000000 |
| `reviewer_c` | 0 | 2 | 2 | 6 | 0 | 2 | 4 | 0.000000 | 0.166667 |

Gate decision: `failed_packet_gate_no_promotion`.

Failed reasons:

- Real-negative label leakage broke the fixed denominator. Reviewers A and B both flagged five real negatives as leaked: `H-665`, `H-158`, `M-527`, `M-1315`, and `M-171`. Reviewer C flagged four of the same five.
- Conservative real-negative target-like uncertainty appeared for reviewer C on `M-525` and `M-365`.
- Targets were not cleanly recovered. `M-1320`, `H-654`, and `M-811` failed or were uncertain across reviewers; `M-1310` passed for A/B but failed for C.
- Inter-review target counts varied for `M-1320` (`8/8/7`), `M-1310` (`7/7/6`), and `M-811` (`5/6/6`).

## Decision

Retracted promotion candidate:

> The v2b label-masked no-overlay packet promotes `H-654`, `M-1310`, `M-1320`, and `M-811` to source-normalized crop/token-order candidates.

Reason retracted: v2b fixed the duplicate-image and denominator-size defects, but it failed the adversarial packet gate. Real denominator rows still leaked catalogue/page labels, conservative target-like uncertainty remained in real negatives, and target visual token counts were unstable.

No source-normalized token order, physical direction, sign identity, sign meaning, phonetic value, language-family likelihood, translation, or accepted structural finding follows.

## Artifacts

- `data/open_prototype/tools/effective_unicity_directionality_blind_packet_v2b.py`
- `data/open_prototype/tools/score_effective_unicity_directionality_blind_reviews_v2b.py`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_v2b_crop_manifest.csv`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_v2b_manifest.csv`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_v2b_answer_key.csv`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_v2b_review_template.csv`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_v2b_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_blind_v2b_reviews/reviewer_a.csv`
- `data/open_prototype/reports/effective_unicity_directionality_blind_v2b_reviews/reviewer_b.csv`
- `data/open_prototype/reports/effective_unicity_directionality_blind_v2b_reviews/reviewer_c.csv`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_v2b_scored_rows.csv`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_v2b_review_summary.json`
- `tmp/effective_unicity_directionality_blind_packet_v2b/directionality_no_overlay_v2b_blind_contact_sheet.png`
- `tmp/effective_unicity_directionality_blind_packet_v2b/blind_images/`
