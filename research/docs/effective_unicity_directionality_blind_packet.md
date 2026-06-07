# Effective-Unicity Directionality No-Overlay Blind Packet

Date: 2026-05-29

## Purpose

The public route probe produced four route-probe targets selected for a failed attempted source-normalization gate: `H-654`, `M-1310`, `M-1320`, and `M-811`. This packet tested whether those routed source panels remained cleanly boxable after removing route overlays and mixing them with real source controls.

This is a source-normalization gate only. It does not validate physical reading direction, token order, sign identity, sign meaning, language family, phonetic value, or translation.

## Packet

Packet ID: `directionality_no_overlay_packet_v1`

| Role | Count |
| --- | ---: |
| Blind items | 15 |
| Primary target images | 7 |
| Primary target unique CISI IDs | 4 |
| Scoring negative images | 7 |
| Packaged scoring negative unique CISI IDs | 7 |
| Effective scorable unique CISI IDs after label exclusion | 6 |
| Quarantine negative images | 1 |
| Accepted claim increment | 0 |

Targets:

| CISI | Expected catalog text |
| --- | --- |
| `H-654` | `+405-061-740-806+` |
| `M-1310` | `+407-004-001-740-407-590-235+` |
| `M-1320` | `+527-555-231-240-798+` |
| `M-811` | `+226-032-803+` |

Scoring negatives: `H-665`, `M-1273`, `M-1458`, `M-1523`, `M-376`, `M-381`, `M-525`.

Quarantine negative: `H-152`.

## Forger Boundary

The forger target was stricter than this packet achieved: 12 unique real controls were planned, with a promotion floor of 10. The packet packaged seven unique real controls, and after the `D006/M-525` label leak only six unique controls were effectively scorable. It was underpowered for promotion before review began. It can still expose leakage, overcounting, and false-positive behavior.

Promotion thresholds before review:

| Requirement | Status |
| --- | --- |
| At least two independent blind reviews | Met |
| Every target view label-leak-free and cleanly boxable | Failed |
| Paired target views agree in visual token count where paired views exist | Failed |
| Real scoring negative denominator >= 10 unique CISI IDs | Failed |
| Zero hard count-boxable hits on scoring negatives | Failed |
| Accepted claim increment | 0 |

## Blind Review Result

Two blind reviews were scored.

Denominator accounting is deliberately explicit: the packet contained seven unique scoring-negative CISI controls, but `D006/M-525` leaked a printed side annotation and is not scorable. The effective unique real-negative denominator after label exclusion is six. Yes-only denominators were 3 for `blind_review_a` and 4 for `blind_review_b`; conservative denominators were 6 for each reviewer.

| Reviewer | Target pass | Target fail | Target uncertain | True negatives | Hard false positives | Uncertain negative hits | Label-leak negatives excluded | Yes-only FPR | Conservative FPR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `blind_review_a` | 0 | 7 | 0 | 2 | 1 | 3 | 1 | 0.333333 | 0.666667 |
| `blind_review_b` | 1 | 4 | 2 | 3 | 1 | 2 | 1 | 0.250000 | 0.500000 |

Gate decision: `failed_packet_gate_no_promotion`.

Failed reasons:

- Below the forger real-negative denominator floor: seven packaged unique scoring negatives instead of at least ten, with only six effectively scorable after label leakage.
- `D006/M-525` leaked a printed side annotation and was excluded from the negative denominator for both reviewers.
- Scoring negatives produced hard count-boxable false positives: `D015/M-381` for `blind_review_a`, `D009/H-665` for `blind_review_b`.
- Targets were not cleanly recovered. `M-811`, `M-1320`, and `H-654` were overcounted by at least one reviewer; `M-1310` was uncertain for `blind_review_b`.

## Skeptic Attacks

The packet failed the attacks it was supposed to survive:

| Attack | Result |
| --- | --- |
| Label leakage | Broke on `D006/M-525`; printed side annotation visible. |
| Matched-negative false positives | Broke; two reviewers produced hard count-boxable scoring-negative hits. |
| Target token-count stability | Broke; targets were mostly overcounted or uncertain. |
| Real-control denominator | Broke; seven packaged unique real scoring negatives, only six effectively scorable after label leakage. |
| Physical direction/source side | Not tested; this packet only tests blind crop boxability and token-count recovery. |

## Decision

Retracted promotion candidate:

> The H-654/M-1310/M-1320/M-811 no-overlay blind packet promotes those route-probe targets to source-normalized crop/token-order candidates.

Reason retracted: the packet failed its own gate and the forger's denominator floor. It remains useful as a crop-QA and control-design failure report.

No source-normalized token order, physical direction, sign identity, sign meaning, phonetic value, language-family likelihood, translation, or accepted structural finding follows.

## Artifacts

- `data/open_prototype/tools/effective_unicity_directionality_blind_packet.py`
- `data/open_prototype/tools/score_effective_unicity_directionality_blind_reviews.py`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_crop_manifest.csv`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_manifest.csv`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_answer_key.csv`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_review_template.csv`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_blind_reviews/blind_review_a.csv`
- `data/open_prototype/reports/effective_unicity_directionality_blind_reviews/blind_review_b.csv`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_scored_rows.csv`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_review_summary.json`
- `tmp/effective_unicity_directionality_blind_packet/directionality_no_overlay_blind_contact_sheet.png`
- `tmp/effective_unicity_directionality_blind_packet/blind_images/`
