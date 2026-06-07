# Effective-Unicity Directionality Source Queue

Date: 2026-05-29

## Purpose

The live directionality candidate is still a metadata-layer result. The next hard gate is source-image validation: do the rows that carry the major-site stored-order signal still hold when the actual source plates, impressions, side labels, and image/impression direction are checked?

This artifact is an acquisition queue, not an accepted claim. It ranks the harsh major-site rows by directionality pressure and joins whatever local source-route hints already exist.

Scope:

- Lipi T3 metadata/sign layer.
- top-10 edge signs removed.
- one-edit families collapsed.
- Mohenjo-daro and Harappa rows only for the queue.

## Baseline

| Scope | Rows | Stored higher | Reversed higher | Ties | Stored win share |
| --- | ---: | ---: | ---: | ---: | ---: |
| all harsh | 365 | 307 | 47 | 11 | 0.841096 |
| Mohenjo-daro + Harappa | 324 | 274 | 35 | 15 | 0.845679 |
| Mohenjo-daro | 212 | 173 | 22 | 17 | 0.816038 |
| Harappa | 112 | 83 | 16 | 13 | 0.741071 |

The queue has 324 major-site rows. It scans 46 local source/provenance CSV files and builds a route index for 912 CISI identifiers. Most high-pressure rows still do not have source-grade routes.

## Queue Summary

| Priority band | Rows |
| --- | ---: |
| P0 validate high positive existing route | 1 |
| P1 acquire high positive source | 53 |
| P1 audit reversed anomaly | 35 |
| P2 validate positive support | 220 |
| P3 tie or low information | 15 |

| Source validation need | Rows |
| --- | ---: |
| find public or request source route | 223 |
| replace non-source-grade catalogue hint | 94 |
| review existing crop for visibility and token-count stress | 3 |
| blind token-box stress from existing public route | 2 |
| request or locate source image | 2 |

The most immediate usable target is `M-70`, text `+226-032-002-390-692+`, with a high positive row score and an existing public CISI plate route. The first visual pass upgrades it to row-level source-visible with a broad order-window continuation candidate. Its matched-negative blind token-box packet has now failed promotion: two reviewers produced hard target-like hits on scoring negatives, with maximum yes-only false-positive rate 0.714286 and maximum conservative false-positive-or-uncertain rate 0.777778. That row remains a source-validation target only. It does not promote any `002-Y` or directionality claim by itself.

The follow-up public CISI OCR route probe tested 79 top high-pressure rows from this queue. It found 93 OCR route rows, 39 targets with any route, 38 targets with public CISI plate-route candidates, one target with data/register route only, and 40 targets still not found in the public OCR layer. A manual visual triage of nine top route hits produced four attempted no-overlay target crops: `H-654`, `M-1310`, `M-1320`, and `M-811`. The first packet failed because the real-control denominator was too small, one scoring negative leaked a printed side annotation, scoring negatives produced hard count-boxable false positives, and target token counts were mostly unstable. A stricter v2b packet reached 12 real negatives and zero duplicate image hashes, but still failed because real denominator rows leaked labels, conservative target-like uncertainty remained in two real negatives for one reviewer, and target counts varied across reviewers. This is still acquisition and failure-discovery work only. No source-normalized token order or physical direction claim is accepted.

## Method

For each major-site harsh row, the script computes:

- stored-order versus reversed-order log probability with the tested row excluded from the bigram model,
- per-transition stored-minus-reversed difference,
- direction outcome: stored higher, reversed higher, or tie,
- leave-one-row-out delta for the pooled major-site score and the row's own site score,
- source-route hints joined by representative and family CISI identifiers.

The source join is intentionally loose and transparent. It scans local CSV files whose filenames contain source, route, crop, witness, adjudication, or manifest, then aggregates rows with a `cisi` column. The resulting source rank is only a triage score. It is not source-grade evidence.

## Decision

This queue turns the current unresolved attack into concrete work:

> Source-image validation should begin with the ranked major-site rows, not with arbitrary famous inscriptions. The local source inventory has improved after the public route probe, but the first no-overlay packet shows the crop/token-box gate is still too permissive: the four attempted target crops failed blind promotion and remain acquisition targets only.

Forbidden wording:

- Do not say this validates physical source-image direction.
- Do not say this validates a reading direction.
- Do not treat source-route hints as source-normalized sign readings.
- Do not assign signs, sounds, meanings, language family, or translations from this queue.

## Artifacts

- `data/open_prototype/tools/effective_unicity_directionality_source_queue.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_source_queue_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_source_queue.csv`
- `data/open_prototype/reports/effective_unicity_directionality_source_queue_source_index.csv`
- `docs/effective_unicity_directionality_m70_source_pilot.md`
- `docs/effective_unicity_directionality_public_route_probe.md`
- `data/open_prototype/reports/effective_unicity_directionality_m70_source_pilot.csv`
- `data/open_prototype/reports/effective_unicity_directionality_public_route_probe_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_route_visual_triage_summary.json`
- `docs/effective_unicity_m70_blind_token_box_packet.md`
- `data/open_prototype/reports/effective_unicity_m70_blind_token_box_packet_summary.json`
- `docs/effective_unicity_directionality_blind_packet.md`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_review_summary.json`
- `docs/effective_unicity_directionality_blind_packet_v2b.md`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_v2b_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_v2b_review_summary.json`
