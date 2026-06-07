# `002-Y` Branch-Gap Blind Source-Box Packet

Date: 2026-05-29

## Purpose

The public CISI route pass found route hooks for branch-pole signs `368`, `031`, and `220`. Packet `branch_gap_source_box_v1` is the next adversarial gate: hide catalogue labels and ask whether the routed source crops can actually be tokenized before any source-normalized claim is promoted.

This is a packet, not a result.

## Correction Before Packeting

The route matcher was tightened before this packet was built. OCR split labels like `H-449` into pieces that could match `H-44`; starred partial labels also produced false hits. The acquisition script now rejects starred partial labels and split numeric suffixes. As a result, `H-44` is demoted from a public route candidate to a route failure/quarantine example.

After regeneration, the branch pole has 14 grade >= 2 route hooks rather than 15. There is still no route-inventory gap:

| Sign | Public route candidates |
| --- | ---: |
| `368` | 5 |
| `031` | 4 |
| `220` | 3 |

## Packet Composition

The packet has 14 blind images:

| Role | Count | Items |
| --- | ---: | --- |
| Primary targets | 3 | `M-12` for `368`, `M-318` for `031`, `M-29` for `220` |
| Backup targets | 3 | `M-311` for `368`, `M-678` for `031`, `M-655` for `220` |
| Scoring negatives | 6 | `M-28`, `M-653`, `M-654`, `M-381`, `M-32`, `M-17` |
| Quarantine items | 2 | `H-449` false-route control, `M-1427` low-legibility real-route control |

All generated branch-gap images are label-free recrops from the original public page images, not from the red-box OCR route crops. A contact-sheet visual QA pass tightened the `M-29`, `M-654`, `H-449`, and `M-1427` crops after label leakage was detected. The answer key stores the source crop provenance and catalog text, but the blind manifest does not expose them.

## Null Question

Can public-route branch-gap crops for `002` followed by `368/031/220` be tokenized and aligned more reliably than matched negative or quarantine source crops when catalogue text and object labels are hidden?

## Promotion Boundary

Packet creation increments no claim count. The maximum future promotion, if the packet survives blind review, is `source-box adjudication candidate` for selected route rows. It cannot accept a structural claim, physical direction, sign identity, sign meaning, phonetic value, language family, or translation.

Promotion from this packet would require:

- At least two independent blind reviews with stable token counts and boxes for each primary target.
- Zero hard branch-relation hits on scoring negatives.
- Quarantine items excluded from false-positive denominators.
- No dependence on source labels, catalogue text, or post-hoc orientation choice.

## Stage-1 Blind Review Result

Three independent blind stage-1 reviews were scored after packet creation. This stage only checks visual token-count stability before unblinded catalog alignment.

Result: `not_promotable_stage1_only_no_claim_increment`.

| Reviewer | Exact count matches | Primary strict recovery | Backup strict recovery | Hard branch notes on scoring negatives |
| --- | ---: | ---: | ---: | ---: |
| `curie_review` | 2/14 | 1/3 | 0/3 | 0/6 |
| `hypatia_review` | 2/14 | 0/3 | 0/3 | 0/6 |
| `noether_review` | 1/14 | 0/3 | 0/3 | 0/6 |

Target and backup stability:

| Blind ID | CISI | Role | Catalog token count | Blind counts |
| --- | --- | --- | ---: | --- |
| `BG001` | `M-12` | primary `368` | 9 | 10, 10, 10 |
| `BG002` | `M-318` | primary `031` | 5 | 5, 6, 5 |
| `BG003` | `M-29` | primary `220` | 9 | 10, 9, 14 |
| `BG004` | `M-678` | backup `031` | 9 | 8, 9, 10 |
| `BG005` | `M-655` | backup `220` | 7 | 9, 11, 9 |
| `BG006` | `M-311` | backup `368` | 4 | 7, 12, 0 |

This is a failed promotion gate, not a failed route inventory. The strongest useful residue is diagnostic: `BG001/M-12` is visually stable at 10 blind tokens against a 9-token catalog string, suggesting a source/catalog tokenization mismatch worth separate manual audit. That audit now exists: `docs/campaign_m12_token_count_audit.md` keeps `M-12` unpromoted because Lipi and Mayig both preserve 9-token witnesses and scoring negative `BG009/M-654` reproduces stable over-counting at 1/6. `BG002/M-318` is close but not unanimous. The rest are too unstable for source-box promotion.

## Artifacts

- Builder: `data/open_prototype/tools/campaign_002_y_branch_gap_blind_packet.py`
- Summary: `data/open_prototype/reports/campaign_002_y_branch_gap_blind_packet_summary.json`
- Blind manifest: `data/open_prototype/reports/campaign_002_y_branch_gap_blind_manifest.csv`
- Answer key: `data/open_prototype/reports/campaign_002_y_branch_gap_blind_answer_key.csv`
- Review template: `data/open_prototype/reports/campaign_002_y_branch_gap_blind_review_template.csv`
- Blind reviews: `data/open_prototype/reports/campaign_002_y_branch_gap_blind_reviews/`
- Review scorer: `data/open_prototype/tools/score_campaign_002_y_branch_gap_blind_reviews.mjs`
- Review summary: `data/open_prototype/reports/campaign_002_y_branch_gap_blind_review_summary.json`
- Scored rows: `data/open_prototype/reports/campaign_002_y_branch_gap_blind_scored_rows.csv`
- M-12 follow-up audit: `docs/campaign_m12_token_count_audit.md`
- Contact sheet: `tmp/002_y_branch_gap_blind_packet/branch_gap_blind_contact_sheet.png`
- Blind image directory: `tmp/002_y_branch_gap_blind_packet/blind_images/`
