# Effective-Unicity Directionality M-70 Source Pilot

Date: 2026-05-29

## Purpose

This note records the first source-image pass from the directionality source queue — the ranked list of seals whose published photographs we want to inspect before any reading-direction claim is allowed to stand. Up to this point the directionality work lived entirely in catalog metadata. This pass checks the top-ranked seal, queue rank 1, M-70, against its actual published plate. It promotes no sign reading.

Queue row:

- CISI: `M-70`
- Lipi row: `2598.1`
- Site: Mohenjo-daro
- Type: `SEAL:S`
- Symbol: `Bull1:T`
- Catalog text: `+226-032-002-390-692+`
- Metadata direction: `R/L`
- Queue priority: `P0_validate_high_positive_existing_route`

## Source Material

Route — the concrete path from our catalog row to a published image:

- CISI India IA leaf `n66`, printed page 31, Mohenjo-daro 70-72 seals. CISI is the Corpus of Indus Seals and Inscriptions, the primary published photographic record; IA is the Internet Archive scan of it.

Local crops inspected:

| Crop | SHA-256 |
| --- | --- |
| `tmp/032_002_branch_tail_source_acquisition/M70_face_A_signband_from_cisi_india_n066.png` | `3F9E0553A46A78DDC3BFA51E03CD39F09E77485DA586B7CF346147E668211218` |
| `tmp/032_002_branch_tail_source_acquisition/M70_impression_a_signband_from_cisi_india_n066.png` | `8AECC8B6C7FC8708134FC638A95736F1D6737CCD4A9A2F07207F72B1A3D75696` |
| `tmp/032_002_branch_tail_source_acquisition/M70_face_A_full_panel_from_cisi_india_n066.png` | `6AA79DACD1EA66697FB7042ED299EAE964B3386DD012ABE6A450D9A2ECBEFA15` |
| `tmp/032_002_branch_tail_source_acquisition/M70_impression_a_full_panel_from_cisi_india_n066.png` | `2172C5F4BE359DFCDE3D1A751B8BAE625D829482F18D71658FAA514A3A1016FB` |
| `tmp/032_002_branch_tail_token_order/M70_A_a_token_order_overlay.png` | `A96FB11A300EED3094D2E2B0206408F85D480CD332859F17591EB54A5334A634` |

## Human Visual Read

The public CISI crop visibly contains a single signband — the horizontal strip of signs — above the animal on the seal face, and a matching band on the impression. The face and impression are mirror counterparts, as expected for a seal and its impression.

The existing broad order-window packet — a bundle of crops in which reviewers mark where a span of signs sits — marks the `032-002-390-692` span and records `pass_branch_head_continuation_candidate` at medium confidence. Branch head here means the sign that opens this branch of the sequence grammar. That is stronger than route-only visibility, but weaker than exact token boxing: drawing a box around each individual sign.

The band was suitable for a blind token-boxing stress test — blind meaning the reviewers cannot see the catalog answers — and that test has now been scored. The matched-negative packet failed its promotion gate. A matched-negative packet plants decoy crops that should yield nothing, and the gate is the pass/fail rule the packet has to clear. Two independent reviewers recovered target-like structure in M-70, but they also produced hard target-like hits on scoring negatives, the planted decoys. The maximum yes-only false-positive rate was 0.714286, and the maximum conservative false-positive-or-uncertain rate was 0.777778.

## Decision

Keep M-70 inside the source queue as:

> row-level source-visible public CISI pair with a broad order-window continuation candidate; the first matched-negative blind token-box packet failed promotion to source-boxed order-window status.

No accepted claim count changes. This does not validate physical source-image direction, sign identity, sign meaning, phonetic value, language family, or translation.

Next action:

1. Do not reuse this broad visual-boxing packet as positive evidence.
2. Build a stricter source-box protocol with lower-control false positives before attempting another M-70 promotion.
3. Keep M-70 useful as a source-validation target, not as an accepted token or direction claim.

## Artifacts

- `data/open_prototype/reports/effective_unicity_directionality_m70_source_pilot.csv`
- `data/open_prototype/reports/campaign_032_002_branch_tail_token_order_verdicts.csv`
- `data/open_prototype/reports/campaign_032_002_branch_tail_token_order_boxes.csv`
- `docs/effective_unicity_m70_blind_token_box_packet.md`
- `data/open_prototype/reports/effective_unicity_m70_blind_token_box_packet_summary.json`
- `data/open_prototype/reports/effective_unicity_m70_blind_token_box_review_summary.json`
