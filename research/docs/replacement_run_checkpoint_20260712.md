# Replacement run checkpoint

Date: 2026-07-12 America/Los_Angeles

Authority: this checkpoint supersedes `replacement_run_checkpoint_20260531.md` for work completed on July 12 while preserving every accepted boundary from it. It does not revive any file listed in `research/data/quarantine/botched_successor_after_20260531T0104_manifest.csv`.

## Accepted state

| Claim class | Accepted count |
| --- | ---: |
| translations | 0 |
| phonetic values | 0 |
| sign meanings | 0 |
| language identification | 0 |
| external anchors | 0 |
| structural findings | 1 |

The only accepted structural finding remains the fixed `002-861 / 533-717` restricted terminal-tail result under its prior narrow wording. Nothing in this checkpoint is a reading.

## Completed annotations

### `158-806 / Phyt`

Decision: `closed_not_claim_eligible_support_below_floor_source_independence_unresolved`.

- Seven catalogue rows validate against the pinned planning corpus.
- They represent only three exact text families, below the pre-existing support floor of five.
- A two-stratum form/motif grouping is reported only as sensitivity analysis; it is not evidence of common manufacture or copying.
- No text family has a locally validated source-grade token box, and no fixed matched-iconographic-negative packet exists.
- The May 31 null was a queue trigger, never an accepted meaning. It is not rerun.

Artifacts:

- `research/docs/vector4_158806_source_family_gate_20260712.md`
- `research/data/open_prototype/reports/vector4_158806_source_family_gate_20260712_witnesses.csv`
- `research/data/open_prototype/reports/vector4_158806_source_family_gate_20260712_summary.json`

### Local `220` / Mayig `P050`

Decision: `PARK`.

- Four independent CISI artifacts have exact Lipi/Mayig same-position `220/P050` bindings.
- All four cached token boxes are compatible with the broad fish/leaf graphic neighborhood.
- Zero boxes come from an independently pinned primary-catalog panel that visibly resolves the defining “no decoration” condition.
- Accepted crosswalks, values, readings, and translations remain zero.

Artifacts:

- `research/docs/replacement_p050_local220_strict_fish_family_source_gate_20260712.md`
- `research/data/open_prototype/reports/replacement_p050_local220_strict_fish_family_source_gate_20260712_summary.json`
- `research/data/open_prototype/reports/replacement_p050_local220_strict_fish_family_source_gate_20260712_token_boxes/`

### Source annotations completed before the GPU run

| Annotation | Source-visible decision | Research consequence |
| --- | --- | --- |
| AO 22310 | Bound to De Clercq plate IX no. 83 and Louvre AO 22310; no Indus text and unknown findspot. | Contact object only, not a bilingual or external anchor. |
| 740 / P324 | Exact at 73/73 aligned positions with labeled CISI panels. | Accepted only as a Lipi-to-Mayig analysis edge. |
| 002 / P122 | Three source-visible exceptions among 60 positions. | Conflict; exact mapping rejected. |
| {390,405,406,407} / P086 | P086 merges four visibly distinct Lipi members. | Feature-preserving Mayig-policy merge only; raw Lipi stays distinct. |
| 032 / P145 | M-143 reverses the dominant 032 002 / P145 P122 pairing. | Conflict; exact mapping rejected. |
| {817,861} / P385 | Both forward lanes are exact, but roundedness distinguishes members; M-177 is a local 803/P385 collision. | Feature-preserving merge only; global 803/P364 remains conflicted. |
| P041 / Parpola 41 | Same digits refer to different signs across Parpola, Mayig, Wells, Mahadevan, and Lipi. | Namespace trap resolved; no crosswalk accepted. |
| M-77 / text no. 7 | M-35 has seven signs and M-77 five; M-37 is the complete three-sign source match. | Printed identifiers rejected; M-37 retained as an intended-reference candidate, not an author-confirmed correction. |
| M-161 | Source shows four units, including two grids, versus three Lipi tokens. | Literal Lipi count rejected; 617 remains unresolved compound-or-omission policy. |
| M-105 | Source and stored text length show seven units; signs=5 excludes two real 000 positions. | Structural count is seven; both identities remain unknown and 920/P154 stays uncertain at 4:3. |
| P000 policy: M-110, M-126, M-73 | All three flagged CISI objects show only the Lipi-counted bounded signs plus the damaged span encoded by Mayig P000. | P000 is uniformly non-sign damage metadata. M-126 and M-73 count mismatches close; M-110's complete original length remains unresolved across its lost span. |

These decisions tighten the usable corpus and crosswalk without adding a translation, value, meaning, language identification, external anchor, or accepted structural claim. The detailed panels, tables, gates, and object-level decisions remain the evidence record; this checkpoint carries only the synthesis.

## From-scratch SLM result

All 65 planned runs completed across five paired seeds. Lower negative log-likelihood (NLL) is better.

| Question | Five-seed result | Decision |
| --- | --- | --- |
| IVC capacity: micro, 886,850 parameters | NLL 4.1165; top-1 25.45% | Best IVC NLL in every paired seed. |
| IVC capacity: small, 6,537,794 parameters | NLL 4.1946; top-1 24.68% | Worse than micro; no scale-up signal. |
| IVC capacity: medium, 18,123,074 parameters | NLL 4.3120; top-1 23.85% | Worse again; 1B escalation is not scientifically justified. |
| Authentic IVC vs row-internal shuffle, small | Authentic gains 0.3665 NLL and 6.05 top-1 points; stored-order win share 0.883 vs 0.470. | Real order/co-occurrence structure survives grouped holdout. |
| Authentic IVC vs position-slot shuffle, small | Authentic gains 0.6492 NLL and 12.86 top-1 points. | Structure is not reducible to position marginals. |
| Known-writing transfer vs random IVC | NLL gain +0.0909, 95% paired bootstrap CI [0.0659, 0.1159]. | Transfer helps. |
| Known-writing vs nonwriting transfer | Specificity gain +0.0191, CI [-0.0087, 0.0444]. | No writing-specific advantage established. |
| Known-writing vs position-shuffled-IVC transfer | Specificity gain +0.0429, CI [0.0046, 0.0821]. | Known writing beats this shuffled source, but not the nonwriting comparator. |
| Exposure matching | Max record spread 12.74%; token spread 29.01%; masked-position spread 24.61%; tolerance 20%. | Exposure gate fails despite zero attrition. |
| Known-script calibration | Linear B: NLL 2.7466, top-1 40.02%; SumTablets: NLL 4.5013, top-1 15.50%. | Calibration only; cross-corpus absolute scores do not identify language status. |
| Pre-registered transfer gate | Statistical comparisons complete; exposure checks complete; specificity and exposure requirements not met. | **FAIL**. |

Interpretation: the model finds reproducible sequential structure in the IVC corpus, because authentic sequences beat both matched corruption controls. That is a structural result, not a linguistic identification. The transfer benefit is not writing-specific: nonwriting pretraining produces a statistically compatible gain, while exposure imbalance also violates the pre-registered design. The capacity curve points in the opposite direction from scaling: the 0.89M model beats the 6.54M and 18.12M models on held-out NLL in all five seeds, so a 1B run would spend compute without answering the live research question.

Raw outputs are preserved in `research/data/slm/ivc_from_scratch_scaling_20260712/`: the full 65-run matrix, per-run comparison table, aggregate analysis, completion/cost record, resolved configuration, and hardware/input manifest.

## Directionality closure

Decision: `CLOSED_PHYSICAL_DIRECTION_PROMOTION_RETAIN_STORED_ORDER_STRUCTURE`.

- Meadow and Kenoyer's matched seal/tablet case identifies `H96-2796/6876-01`, local `H-1682`, as left-to-right on the physical intaglio seal while the matching non-impressing tablets are assumed right-to-left.
- Lipi records `R/L` for `H-1682` and for all 66 sides of H-2218 through H-2239. The field therefore does not uniformly encode physical as-pictured orientation across those media.
- `H-1682` is inside the harsh 365-row directionality scope and favors stored order, so this is an internal semantic counterexample rather than an unrelated source objection.
- Removing it changes stored-win share only from 0.841096 to 0.840659. The stored-order structural result survives; physical reading direction does not follow from it.
- A larger negative-image denominator cannot fix an unlabeled orientation construct. The failed packet lane is closed rather than expanded.

Detailed decision: `research/docs/effective_unicity_directionality_physical_orientation_closure_20260712.md`.

## `FRAME700 034` size-tier falsification

Decision: `CLOSE_034_OBJECT_SIZE_OR_METROLOGICAL_TIER_UNDER_CURRENT_LOCAL_EVIDENCE`.

- The pre-registered test used 309 measured artifacts in 216 held-out source/formula groups, with the entire H-2218 through H-2239 series held out together.
- Dimensions predict `034` above chance: grouped AUC 0.701087, bootstrap 95% interval [0.606806, 0.789030]. Both matched administrative-format and emblem/copy-family label shuffles rarely reach the observed AUC, at 0.001500 and 0.001000.
- The size model does not beat the administrative-format baseline by a positive bootstrap margin: AUC difference interval [-0.010581, 0.134992].
- On the clean H-series holdout, the model calls all 22 small tablets `034`, including the one true `033`: `034` recall 1.000000, non-`034` specificity 0, AUC 0.476190.
- The surviving association is small-tablet form factor, not a subtype-specific numerical or metrological tier. No value, unit, quantity, commodity, or meaning is accepted.

Detailed decision: `research/docs/frame700_034_size_tier_heldout_decision_20260712.md`.

## `603` cross-context graphic closure

Decision: `CLOSED_CROSS_CONTEXT_603_GRAPHIC_IDENTITY_NOT_SOURCE_SUPPORTED`.

- M-240, M-714, and M-1273 preserve a recurrent rectangular ladder/window-like post-`861` terminal class in the source panels.
- H-1138 and H-1846 preserve the five-unit Harappa `740-X-240-060-692` formula, but local `603` can only be visual unit 2 or 4 under forward/reversed order. Neither candidate is the Mohenjo window.
- H-1846 has a window-like edge unit, but it maps to local `740` or `692`, not `603`, under the two linear orientations. Making it `603` would require rejecting the stored sequence/order and therefore still kills the current bridge.
- The shared Lipi number is catalog-mediated, not source-visible cross-context identity. Keep the Mohenjo tail class and Harappa internal-slot candidate separate; do not use the Harappa rows to interpret the Mohenjo tail.
- No raw corpus number is rewritten and no value, function, phonetic reading, language, or translation is accepted.

Detailed decision: `research/docs/campaign_032_002_861_603_cross_context_graphic_closure_20260712.md`.

## Next executable order

1. Adjudicate the next unresolved `lipi_unknown_zero_explains_count` object, M-27, against both CISI views: test whether its Lipi `000` is a bounded source sign, an uncertainty code, or lost material.

## Parked lanes

The paid/contact/physical-source rows listed in `replacement_live_action_register_20260712.md` remain parked. No message was sent and no source was purchased. Language-family, rebus, proper-name, phonetic, and translation lanes remain closed because no bilingual or secure external reading constraint exists.
