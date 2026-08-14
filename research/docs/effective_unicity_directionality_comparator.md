# Effective-Unicity Directionality Comparator

Date: 2026-05-29

## What This Note Is

This note reports the main directionality comparator run. A comparator is a control corpus — or a battery of them — scored with the exact same instrument as the Indus data, so we can see where the Indus signal sits relative to known writing and known non-writing. Directionality here means the tendency of a stored sign sequence to score higher in its recorded order than reversed.

## Result

Masked-sign predictability did not distinguish Indus from real-world nonlinguistic or ambiguous symbol systems. Directionality is stronger.

Using leave-one-row-out bigram scoring — a sign-to-sign transition model that always excludes the row being scored — the script compares each stored sequence with its reversed sequence. In the harshest Indus scope, after removing rows whose first or last sign is among the ten most frequent edge signs and then collapsing near-duplicate one-edit families, stored order still beats reversed order in 0.841096 of rows. Across the current Sproat 2014 real-world comparator battery — a set of real nonlinguistic and ambiguous symbol corpora drawn from Sproat's 2014 work — the strongest nonlinguistic or ambiguous comparator is Pictish at 0.802139. Known scripts sit higher: Linear B Series D at 0.996403 and SumTablets glyph-only administrative lines at 0.935484.

Mayig P-namespace records — a second, independent transcription of many of the same objects — add a separate transcription-layer pressure test. Exact-collapsed Mayig records also show high stored-order asymmetry at 0.943750, but the harsh Mayig scope drops to 0.666667 over only 24 rows. The same-object matched overlap is no longer admissible support. In the exact-collapsed overlap, the Lipi side is high at 0.937500 with max null >= observed share 0.035000, while the Mayig side is soft at 0.929134 with max null >= observed share 0.200000. After top-10 edge removal, both overlap sides collapse: Lipi 0.363636 and Mayig 0.473684, each with max null >= observed share 1.

This is not a decipherment. It is a structural placement result: under this instrument, harshly downweighted Indus directionality is below known writing controls but above the current real-world nonlinguistic and ambiguous comparators.

## Method

For each corpus and scope:

1. Exact-collapse duplicate token sequences unless the named scope applies a stronger collapse.
2. For each row, remove that row's bigrams from the model.
3. Score the stored order and the reversed order with add-alpha-smoothed bigram likelihood.
4. Count the share of rows where stored order scores higher.
5. Run four matched null controls: global token shuffle, row-internal shuffle, length-position shuffle, and edge-frame shuffle.

Generated artifacts:

- `data/open_prototype/tools/effective_unicity_directionality_comparator.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_comparator_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_comparator.csv`
- `data/open_prototype/reports/effective_unicity_directionality_null_summary.csv`
- `data/open_prototype/reports/effective_unicity_directionality_null_iterations.csv`
- `data/open_prototype/tools/effective_unicity_directionality_skeptic_controls.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_skeptic_controls_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_skeptic_controls.csv`
- `data/open_prototype/tools/effective_unicity_directionality_block_controls.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_block_controls_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_block_controls.csv`
- `data/open_prototype/tools/effective_unicity_directionality_site_balance.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_site_balance_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_site_balance.csv`
- `data/open_prototype/tools/effective_unicity_directionality_site_profiles.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_site_profiles_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_site_profiles.csv`
- `data/open_prototype/tools/effective_unicity_directionality_policy_controls.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_policy_controls_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_policy_controls.csv`
- `data/open_prototype/tools/effective_unicity_directionality_influence_controls.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_influence_controls_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_influence_rows.csv`
- `data/open_prototype/reports/effective_unicity_directionality_influence_families.csv`
- `data/open_prototype/tools/effective_unicity_directionality_source_queue.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_source_queue_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_source_queue.csv`
- `data/open_prototype/reports/effective_unicity_directionality_source_queue_source_index.csv`
- `data/open_prototype/tools/effective_unicity_directionality_blind_packet.py`
- `data/open_prototype/tools/score_effective_unicity_directionality_blind_reviews.py`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_blind_packet_review_summary.json`
- `docs/effective_unicity_directionality_blind_packet.md`

## Primary Rows

Stored win share is the fraction of rows where the stored order beats the reversed order. Max null >= observed is the worst case across the shuffle-based null controls: the fraction of shuffled iterations that matched or beat the observed result, so small values mean the signal is hard to fake.

| Corpus / scope | Rows | Tokens | Unique tokens | Stored win share | Max null >= observed |
| --- | ---: | ---: | ---: | ---: | ---: |
| Indus exact-collapsed | 1,798 | 8,212 | 571 | 0.947720 | 0 |
| Indus edge-frame collapsed | 1,408 | 6,288 | 557 | 0.929688 | 0 |
| Indus one-edit-family collapsed | 1,098 | 6,011 | 508 | 0.953552 | 0 |
| Indus top-10-edge-removed exact-collapsed | 530 | 2,123 | 388 | 0.837736 | 0 |
| Indus top-10-edge-removed one-edit-family collapsed | 365 | 1,725 | 358 | 0.841096 | 0 |
| Mayig P exact-collapsed, length 2-8 | 160 | 842 | 174 | 0.943750 | 0.075000 |
| Mayig P top-10-edge-removed one-edit-family collapsed | 24 | 107 | 69 | 0.666667 | 0.050000 |
| Lipi side of matched Lipi/Mayig overlap | 128 | 661 | 179 | 0.937500 | 0.035000 |
| Mayig side of matched Lipi/Mayig overlap | 127 | 657 | 155 | 0.929134 | 0.200000 |
| Source-visible `861` terminal/tail probe | 12 | 87 | 36 | 1.000000 | 1 |
| Lipi side matched overlap, top-10 edge removed | 22 | 96 | 72 | 0.363636 | 1 |
| Mayig side matched overlap, top-10 edge removed | 19 | 80 | 58 | 0.473684 | 1 |
| Linear B Series D sign tokens, IVC-length cap | 278 | 1,755 | 91 | 0.996403 | 0 |
| SumTablets glyph-only line sequences | 1,798 | 8,716 | 358 | 0.935484 | 0 |
| Pictish stones | 187 | 684 | 78 | 0.802139 | 0 |
| Kudurru deity symbols | 24 | 118 | 39 | 0.666667 | 0.737500 |
| Totem poles | 246 | 1,123 | 359 | 0.654472 | 0.687500 |
| Barn stars / hex signs | 97 | 365 | 29 | 0.072165 | 1 |
| Vinca symbols | 91 | 271 | 82 | 0.384615 | 0.737500 |
| Weather icons | 4,018 | 20,090 | 16 | 0.503733 | 1 |

## Decision

Surviving candidate: the stored order of the strict Lipi working corpus has a directional asymmetry that survives exact collapse, edge-frame collapse, one-edit-family collapse, and a harsher top-edge-removal plus one-edit-family collapse. In the harshest scope, current real-world nonlinguistic and ambiguous comparators do not reach the Indus stored-win share.

Retracted support lanes — evidence tracks we previously leaned on and now withdraw: the tiny source-visible `861` terminal/tail probe and the matched Lipi/Mayig overlap rows cannot be used as independent directionality support. The `861` probe is target-selected and has max null >= observed share 1. The overlap rows fail after top-edge removal and block-conditioned edge/slot controls.

Block-control boundary: harsh Indus directionality survives `site|type|symbol` block holdout at 0.827397 with max null >= observed share 0, and a register-edge-family collapsed scope survives the same holdout at 0.835227 with max null >= observed share 0.005000. Full leave-site-out is not clean in harsh scopes: max null >= observed share 0.100000 for the one-edit collapsed scope and 0.265000 for the register-edge-family collapsed scope. Do not phrase the result as site-generalized.

Site-balance boundary: balanced Mohenjo-daro plus Harappa resampling survives, with observed median stored-win share 0.803571 and max paired null >= observed share 0.003 across 1,000 iterations. Multisite balancing does not survive: Mohenjo-daro plus Harappa plus Lothal has max paired null >= observed share 0.528, and the top-five-site design has 0.616. Do not phrase the result as pan-Indus.

Site-profile boundary: Mohenjo-daro and Harappa each carry internal directionality under within-site scoring: Mohenjo-daro stored-win share 0.816038 with max null >= observed share 0.002, and Harappa 0.741071 with max null >= observed share 0.004. Lothal is null-compatible at 0.312500 with max null >= observed share 0.988. Smaller sites are unresolved.

Direction-policy boundary: the harsh scope is overwhelmingly recorded `R/L`: 354 rows versus 11 `L/R`. Restricting to `R/L` rows preserves stored-win share at 0.838983; Mohenjo-daro `R/L` alone scores 0.813397 and Harappa `R/L` alone 0.769231. Random row-level orientation flips destroy the all-harsh signal, with null mean 0.471134 and null p95 0.526027. This supports coherent stored-order orientation in the metadata layer, but it does not validate physical source-image direction.

Influence boundary: the harsh directionality signal is not controlled by one row. The largest supportive single-row removal changes stored-win share by 0.005931, while the largest absolute row effect is adverse, L-115 at 0.010552. Coarse `site|type|symbol` family influence is larger but not decisive: `Mohenjo-daro|SEAL:R|None` is the top supportive family at 0.028975. Treat that as a source-normalization target, not as acceptance.

Source-queue boundary: the major-site harsh scope has 324 rows and pooled stored-win share 0.845679. The first acquisition queue found 223 of 324 needing a public route or source request and 94 with only non-source-grade catalogue hints; its top immediate route target, M-70 (`+226-032-002-390-692+`), failed matched-negative blind token-box promotion with maximum yes-only false-positive rate (FPR) 0.714286 and maximum conservative FPR 0.777778. The subsequent public-route probe over the 79 high-pressure source-validation targets found 38 plate-route candidates and visual triage moved four attempted target crops to no-overlay blind packets: H-654, M-1310, M-1320, and M-811. v1 failed with maximum yes-only FPR 0.333333 and maximum conservative FPR 0.666667; it had only seven packaged real scoring negatives, one leaked negative label, hard scoring-negative false positives, and unstable target token counts. v2b fixed the 12-real-negative and duplicate-hash design defects but failed because real denominator rows leaked labels, reviewer C had conservative target-like uncertainty on 2/12 real negatives, and target counts were unstable. This is acquisition progress and a useful failure report only, not an accepted source-normalized reading.

Forbidden interpretation: this proves the corpus is writing, identifies a language family, assigns sounds, or assigns meanings. Directionality is compatible with writing, administrative notation, and some emblematic ordering conventions. It becomes epigraphic evidence only when source-normalized and combined with an external anchor or a stronger discriminator.

No accepted claim count changes follow from this comparator.
