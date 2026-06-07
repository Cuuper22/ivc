# Open Prototype Results

Date: 2026-05-24

## Purpose

This file records the first materialized corpus-audit result for the IVC translation research project.

The result is intentionally modest: source shape, filtered fields, and artifact-ID overlap. It does not decode or translate anything.

## Frozen Inputs

### Mayig Open Corpus

Pinned source:

```text
Repository: https://github.com/mayig/indus-valley-script-corpus
Commit: ad2f1e218a34b8c33c57de0d6cb8d99272765bbb
```

Local artifacts:

```text
data/open_prototype/mayig/commit.json
data/open_prototype/mayig/tree_manifest.csv
data/open_prototype/mayig/audit_summary.json
data/open_prototype/mayig/sample_record.json
data/open_prototype/mayig/records_index.csv
```

Observed:

- 622 total repository paths.
- 179 corpus JSON files.
- 397 feature files.
- 179 parsed side/artifact records.

### Filtered `lipi` Metadata

Source:

```text
https://raw.githubusercontent.com/yajnadevam/lipi/refs/heads/main/src/assets/data/inscriptions.csv
```

Local artifacts:

```text
data/open_prototype/lipi/metadata_filtered.csv
data/open_prototype/lipi/audit_summary.json
```

Observed:

- 5,679 rows.
- 38 original columns.
- 35 allowed columns preserved.
- 3 quarantined columns removed: `sanskrit`, `translation`, `notes`.
- 5,018 rows have non-empty/non-dash `cisi` values.

## Overlap Probe

Local artifacts:

```text
data/open_prototype/reports/overlap_probe.csv
data/open_prototype/reports/overlap_summary.json
data/open_prototype/reports/mismatch_audit.csv
data/open_prototype/reports/mismatch_summary.json
data/open_prototype/reports/mismatch_collation_queue.csv
data/open_prototype/reports/mismatch_collation_class_summary.csv
data/open_prototype/reports/mismatch_collation_summary.json
data/open_prototype/reports/clean_subset_sequences.csv
data/open_prototype/reports/order_probe_scores.csv
data/open_prototype/reports/structural_readiness_summary.json
data/open_prototype/reports/direction_order_baseline_summary.json
data/open_prototype/reports/direction_order_sequence_scores.csv
data/open_prototype/reports/direction_order_masked_predictions.csv
data/open_prototype/reports/direction_order_masked_summary.csv
data/open_prototype/reports/crosswalk_alignment_pairs.csv
data/open_prototype/reports/crosswalk_lipi_to_mayig_candidates.csv
data/open_prototype/reports/crosswalk_mayig_to_lipi_candidates.csv
data/open_prototype/reports/crosswalk_high_frequency_sample.csv
data/open_prototype/reports/crosswalk_collision_summary.csv
data/open_prototype/reports/crosswalk_summary.json
data/open_prototype/reports/sign_policy_sensitivity_summary.json
data/open_prototype/reports/sign_policy_sensitivity_sequences.csv
data/open_prototype/reports/sign_policy_sensitivity_sequence_scores.csv
data/open_prototype/reports/sign_policy_sensitivity_sequence_summary.csv
data/open_prototype/reports/sign_policy_sensitivity_masked_predictions.csv
data/open_prototype/reports/sign_policy_sensitivity_masked_summary.csv
data/open_prototype/reports/structural_sign_profiles.csv
data/open_prototype/reports/structural_priority_sign_profiles.csv
data/open_prototype/reports/structural_class_summary.csv
data/open_prototype/reports/structural_class_summary.json
data/open_prototype/reports/formula_pattern_sequences.csv
data/open_prototype/reports/formula_pattern_counts.csv
data/open_prototype/reports/formula_anchor_pairs.csv
data/open_prototype/reports/formula_class_transition_counts.csv
data/open_prototype/reports/formula_pattern_summary.csv
data/open_prototype/reports/formula_pattern_summary.json
data/open_prototype/reports/formula_variant_pairs.csv
data/open_prototype/reports/formula_variant_slot_candidates.csv
data/open_prototype/reports/formula_variant_frame_families.csv
data/open_prototype/reports/formula_variant_summary.json
data/open_prototype/reports/formula_variant_null_iterations.csv
data/open_prototype/reports/formula_variant_null_summary.csv
data/open_prototype/reports/formula_variant_null_summary.json
data/open_prototype/reports/sensitivity_formula_sequences.csv
data/open_prototype/reports/sensitivity_formula_summary.csv
data/open_prototype/reports/sensitivity_formula_by_flag.csv
data/open_prototype/reports/sensitivity_formula_summary.json
data/open_prototype/reports/metadata_scope_rows.csv
data/open_prototype/reports/metadata_scope_status_by_series.csv
data/open_prototype/reports/metadata_scope_scaffold_by_series.csv
data/open_prototype/reports/metadata_scope_top_anchor_by_series.csv
data/open_prototype/reports/metadata_scope_summary.json
data/open_prototype/reports/lipi_scope_rows.csv
data/open_prototype/reports/lipi_scope_by_type.csv
data/open_prototype/reports/lipi_scope_by_site.csv
data/open_prototype/reports/lipi_scope_by_region.csv
data/open_prototype/reports/lipi_scope_by_type_direction.csv
data/open_prototype/reports/lipi_scope_length_by_type.csv
data/open_prototype/reports/lipi_scope_readiness_summary.csv
data/open_prototype/reports/lipi_scope_candidates_by_type.csv
data/open_prototype/reports/lipi_scope_candidates_by_site.csv
data/open_prototype/reports/lipi_scope_summary.json
data/open_prototype/reports/lipi_broad_order_sequence_summary.csv
data/open_prototype/reports/lipi_broad_order_masked_summary.csv
data/open_prototype/reports/lipi_broad_order_holdout_summary.csv
data/open_prototype/reports/lipi_broad_order_group_inventory.csv
data/open_prototype/reports/lipi_broad_order_summary.json
data/open_prototype/reports/lipi_dedup_order_sequence_summary.csv
data/open_prototype/reports/lipi_dedup_order_masked_summary.csv
data/open_prototype/reports/lipi_dedup_order_holdout_summary.csv
data/open_prototype/reports/lipi_dedup_order_group_inventory.csv
data/open_prototype/reports/lipi_dedup_order_summary.json
data/open_prototype/reports/lipi_leakage_control_holdout_summary.csv
data/open_prototype/reports/lipi_leakage_control_summary.json
data/open_prototype/reports/lipi_edge_sign_inventory.csv
data/open_prototype/reports/lipi_edge_removed_sequence_summary.csv
data/open_prototype/reports/lipi_edge_removed_masked_summary.csv
data/open_prototype/reports/lipi_edge_removed_holdout_summary.csv
data/open_prototype/reports/lipi_edge_removed_summary.json
data/open_prototype/reports/lipi_family_downweight_inventory.csv
data/open_prototype/reports/lipi_family_downweight_sequence_summary.csv
data/open_prototype/reports/lipi_family_downweight_masked_summary.csv
data/open_prototype/reports/lipi_family_downweight_holdout_summary.csv
data/open_prototype/reports/lipi_family_downweight_summary.json
data/open_prototype/reports/lipi_synthetic_comparator_iterations.csv
data/open_prototype/reports/lipi_synthetic_comparator_summary.csv
data/open_prototype/reports/lipi_synthetic_comparator_summary.json
data/open_prototype/reports/lipi_structured_null_iterations.csv
data/open_prototype/reports/lipi_structured_null_summary.csv
data/open_prototype/reports/lipi_structured_null_summary.json
data/open_prototype/reports/lipi_metadata_prediction_iterations.csv
data/open_prototype/reports/lipi_metadata_prediction_summary.csv
data/open_prototype/reports/lipi_metadata_prediction_summary.json
data/open_prototype/reports/lipi_stratified_class_iterations.csv
data/open_prototype/reports/lipi_stratified_class_summary.csv
data/open_prototype/reports/lipi_stratified_class_summary.json
data/open_prototype/reports/lipi_class_robustness_inventory.csv
data/open_prototype/reports/lipi_class_robustness_results.csv
data/open_prototype/reports/lipi_class_robustness_summary.json
data/open_prototype/reports/lipi_class_field_counts.csv
data/open_prototype/reports/lipi_class_field_by_type.csv
data/open_prototype/reports/lipi_class_field_by_site.csv
data/open_prototype/reports/lipi_class_field_by_length.csv
data/open_prototype/reports/lipi_class_field_examples.csv
data/open_prototype/reports/lipi_class_field_audit_summary.json
data/open_prototype/reports/lipi_class_proxy_control_observed.csv
data/open_prototype/reports/lipi_class_proxy_control_iterations.csv
data/open_prototype/reports/lipi_class_proxy_control_summary.csv
data/open_prototype/reports/lipi_class_proxy_control_summary.json
data/open_prototype/reports/lipi_semantic_anchor_target_summary.csv
data/open_prototype/reports/lipi_semantic_anchor_label_proxy.csv
data/open_prototype/reports/lipi_semantic_anchor_dimension_bins.csv
data/open_prototype/reports/lipi_semantic_anchor_target_summary.json
data/open_prototype/reports/lipi_semantic_anchor_prediction_observed.csv
data/open_prototype/reports/lipi_semantic_anchor_prediction_iterations.csv
data/open_prototype/reports/lipi_semantic_anchor_prediction_summary.csv
data/open_prototype/reports/lipi_semantic_anchor_prediction_summary.json
data/open_prototype/reports/lipi_dimension_residue_sign_classes.csv
data/open_prototype/reports/lipi_dimension_residue_observed.csv
data/open_prototype/reports/lipi_dimension_residue_iterations.csv
data/open_prototype/reports/lipi_dimension_residue_summary.csv
data/open_prototype/reports/lipi_dimension_residue_summary.json
data/open_prototype/reports/lipi_multiside_mark_rows.csv
data/open_prototype/reports/lipi_multiside_mark_token_counts.csv
data/open_prototype/reports/lipi_multiside_mark_pair_counts.csv
data/open_prototype/reports/lipi_multiside_mark_type_summary.csv
data/open_prototype/reports/lipi_multiside_mark_summary.json
data/open_prototype/reports/lipi_multiside_mark_stratified_token_counts.csv
data/open_prototype/reports/lipi_multiside_mark_stratified_pair_counts.csv
data/open_prototype/reports/lipi_multiside_mark_stratified_side_index.csv
data/open_prototype/reports/lipi_multiside_mark_stratified_summary.json
data/open_prototype/reports/lipi_multiside_mark_validation_queue.csv
data/open_prototype/reports/lipi_multiside_mark_sequence_families.csv
data/open_prototype/reports/lipi_multiside_mark_validation_summary.json
data/open_prototype/reports/lipi_short_mark_orientation_rows.csv
data/open_prototype/reports/lipi_short_mark_orientation_companions.csv
data/open_prototype/reports/lipi_short_mark_orientation_tests.csv
data/open_prototype/reports/lipi_short_mark_orientation_summary.json
data/open_prototype/reports/lipi_short_mark_context_orientation_rows.csv
data/open_prototype/reports/lipi_short_mark_context_orientation_families.csv
data/open_prototype/reports/lipi_short_mark_context_orientation_tests.csv
data/open_prototype/reports/lipi_short_mark_context_orientation_summary.json
data/open_prototype/reports/lipi_short_mark_companion_context_rows.csv
data/open_prototype/reports/lipi_short_mark_companion_context_families.csv
data/open_prototype/reports/lipi_short_mark_companion_context_tests.csv
data/open_prototype/reports/lipi_short_mark_companion_context_summary.json
data/open_prototype/reports/lipi_short_mark_side_relation_validation_sheet.csv
data/open_prototype/reports/lipi_short_mark_side_relation_priority_summary.csv
data/open_prototype/reports/lipi_short_mark_side_relation_validation_summary.json
data/open_prototype/reports/lipi_short_mark_plate_request_packet.csv
data/open_prototype/reports/lipi_short_mark_plate_request_packet_summary.json
data/open_prototype/reports/lipi_short_mark_plate_public_leads.csv
data/open_prototype/reports/lipi_short_mark_plate_public_lead_pages.csv
data/open_prototype/reports/lipi_short_mark_plate_public_lead_summary.json
data/open_prototype/reports/lipi_short_mark_source_acquisition_queue.csv
data/open_prototype/reports/lipi_short_mark_source_acquisition_summary.json
data/open_prototype/reports/h233_public_slide_visual_lead_audit.csv
data/open_prototype/reports/h233_public_slide_visual_lead_summary.json
data/open_prototype/reports/h1302_h1303_direction_note_recheck.csv
data/open_prototype/reports/h1302_h1303_direction_note_recheck_summary.json
data/open_prototype/reports/h355_double_short_side_clarification_audit.csv
data/open_prototype/reports/h355_double_short_side_clarification_summary.json
data/open_prototype/reports/h933_h960_034_contrast_source_audit.csv
data/open_prototype/reports/h933_h960_034_contrast_source_summary.json
data/open_prototype/reports/lipi_tab_i_mixed_400_740_176_side_context.csv
data/open_prototype/reports/lipi_tab_i_mixed_400_740_176_side_context_summary.json
data/open_prototype/reports/lipi_tab_i_mixed_400_740_176_dimension_probe_rows.csv
data/open_prototype/reports/lipi_tab_i_mixed_400_740_176_dimension_probe_tests.csv
data/open_prototype/reports/lipi_tab_i_mixed_400_740_176_dimension_probe_summary.json
data/open_prototype/reports/lipi_h2218_h2239_series_validation_sheet.csv
data/open_prototype/reports/lipi_h2218_h2239_series_validation_summary.json
data/open_prototype/reports/lipi_h2218_h2239_fig4_mapping.csv
data/open_prototype/reports/lipi_h2218_h2239_fig4_mapping_summary.json
data/open_prototype/reports/lipi_h2218_h2239_fig4_visual_availability.csv
data/open_prototype/reports/lipi_h2218_h2239_fig4_visual_availability_summary.json
data/open_prototype/reports/lipi_h2218_h2239_dimension_side_order.csv
data/open_prototype/reports/lipi_h2218_h2239_dimension_side_order_class_summary.csv
data/open_prototype/reports/lipi_h2218_h2239_dimension_side_order_tests.csv
data/open_prototype/reports/lipi_h2218_h2239_dimension_side_order_summary.json
data/open_prototype/reports/lipi_h2218_h2239_side_order_confound.csv
data/open_prototype/reports/lipi_h2218_h2239_side_order_confound_tests.csv
data/open_prototype/reports/lipi_h2218_h2239_side_order_confound_summary.json
data/open_prototype/reports/lipi_h2218_h2239_side_role_templates.csv
data/open_prototype/reports/lipi_h2218_h2239_side_role_counts.csv
data/open_prototype/reports/lipi_h2218_h2239_side_role_tests.csv
data/open_prototype/reports/lipi_h2218_h2239_side_role_summary.json
data/open_prototype/reports/lipi_h2218_template_recurrence_rows.csv
data/open_prototype/reports/lipi_h2218_template_recurrence_near_matches.csv
data/open_prototype/reports/lipi_h2218_template_recurrence_summary.json
data/open_prototype/reports/h2219_public_image_leads.csv
data/open_prototype/reports/h2218_h2239_public_image_lead_search.csv
data/open_prototype/reports/h2218_h2239_public_image_lead_search_summary.json
```

Method:

- Parse `mayig` corpus JSON side IDs.
- Strip trailing side letter from IDs such as `M-1A` to get artifact base IDs such as `M-1`.
- Match these against filtered `lipi.cisi`.
- Compare `lipi.signs` to `mayig` grapheme count.
- Mark all rows `sign_system_unmapped` because Parpola `P###` signs and numeric `+###` signs are not crosswalked.

Result:

```text
mayig_records: 179
mayig_unique_artifact_bases: 179
lipi_rows: 5679
lipi_rows_with_cisi: 5018
overlap_rows: 179
overlap_unique_cisi: 179
overlap_count_matches: 150
overlap_count_mismatches: 29
```

## Interpretation

The first overlap result is useful:

- Every parsed `mayig` record matched a filtered `lipi` row by CISI-style artifact ID.
- 150 of 179 matched by rough sign count.
- 29 records need audit before they are allowed into any structural baseline.
- The mismatch audit splits the overlap into 138 clean pre-crosswalk candidates, 12 count-matching sensitivity-flag candidates, and 29 manual-review rows.

The result is not enough to compare signs directly. Sign systems remain unmapped.

## Mismatch Collation Queue

Reference:

[Mismatch collation queue](mismatch_collation_queue.md)

The 29 count-mismatch rows were converted into a manual collation queue.

Key results:

```text
manual_review_rows: 29
P1_source_image_required: 10
P2_standard_manual_review: 12
P3_policy_check_candidate: 7
unflagged_mayig_extra: 8
unflagged_lipi_extra: 4
damaged_boundary_fragment: 4
lipi_unknown_zero_explains_count: 4
mayig_unknown_p000_explains_count: 3
ambiguous_unknown_policy_reconciles: 2
multi_sign_count_disagreement: 2
complex_manual_collation: 1
slash_compound_count_policy_reconciles: 1
```

Interpretation: the queue gives the next manual collation worklist. It does not clear any mismatch row for structural use.

## Structural Readiness Probe

Reference:

[Structural readiness probe](structural_readiness_probe.md)

The 138 clean rows were used for a narrow pre-crosswalk order check. They contain 748 numeric sign tokens, 191 unique numeric signs, and no repeated complete sequences. All 138 rows are Mohenjo-daro `SEAL:S`, so the result is not corpus-wide.

In a leave-one-out add-one-smoothed bigram probe over the clean subset, observed order scored higher than reversed order in 130 of 137 rows longer than one sign, reversed order scored higher in 4, and 3 tied under a `1e-9` epsilon. Observed order scored above the mean of 50 deterministic shuffles in 129 of 137 rows.

Interpretation: the clean subset has enough order signal to justify the next controlled direction/order baseline. It does not justify semantic, linguistic, or translation claims.

## Direction And Order Baseline

Reference:

[Direction and order baseline](direction_order_baseline.md)

The first controlled structural baseline keeps the same 138-row clean subset and compares observed order against reversed order, shuffled order, frequency-only prediction, position-only prediction, length-position prediction, and bidirectional-bigram context.

Key results:

```text
observed_order_beats_reversed: 130 of 137 rows longer than one sign
observed_order_beats_shuffle_mean: 128 of 137 rows longer than one sign
edge_removed_740_002_observed_beats_reversed: 114 of 134 rows longer than one sign
bidirectional_bigram_masked_top1_accuracy: 0.283422
frequency_masked_top1_accuracy: 0.098930
position_masked_top1_accuracy: 0.159091
```

Interpretation: the clean subset contains ordered sign dependencies beyond frequency and simple position baselines. The result remains structural only. Terminal exact-sign prediction is still weak, and all rows are Mohenjo-daro `SEAL:S`.

## Provisional Crosswalk Audit

Reference:

[Provisional crosswalk audit](provisional_crosswalk_audit.md)

The first crosswalk pass used only 136 strict rows: clean count-matched rows with `R/L` direction and no sensitivity flags. It produced 739 aligned positions, 189 `lipi` numeric signs, and 160 `mayig` Parpola-style signs.

High-frequency positional candidates:

```text
740 -> P324, 73/73
002 -> P122, 57/60 with counterexamples P145:2 and P300:1
220 -> P050, 27/29 with counterexamples P056:1 and P060:1
390 -> P086, 25/25
032 -> P145, 20/21 with counterexample P122:1
```

All mappings remain `uncertain`. This is a review queue, not an accepted crosswalk.

The audit also found possible merge/allograph clusters, especially `817` and `861` both aligning to `P385` in 12/12 cases each.

## Sign Policy Sensitivity

Reference:

[Sign policy sensitivity](sign_policy_sensitivity.md)

The sensitivity test compared raw numeric signs, an isolated `817`/`861 -> P385` merge, high-consistency provisional mappings, high+medium provisional mappings, and observed `mayig` Parpola strings on the same 136 strict rows.

Key results:

```text
raw_lipi_numeric_observed_beats_reversed: 129 of 136 rows
p385_merge_only_observed_beats_reversed: 129 of 136 rows
mayig_observed_parpola_observed_beats_reversed: 129 of 136 rows
raw_lipi_numeric_bigram_top1: 0.281461
p385_merge_only_bigram_top1: 0.307172
mayig_observed_parpola_bigram_top1: 0.319350
```

Interpretation: provisional sign policies preserve the structural order signal. The `P385` merge passes a structural screen but remains unvalidated epigraphically.

## Structural Sign Classes

Reference:

[Structural sign classes](structural_sign_classes.md)

The first positional class pass analyzed raw numeric signs, isolated `P385` merge signs, and observed `mayig` Parpola signs on the same 136 strict rows.

Key provisional classes:

```text
740/P324: dominant initial-operator candidate
002/P122: medial/core candidate
220/P050: medial/core candidate
032/P145: medial/core candidate
817/861/P385: terminal-operator candidate cluster
390/P086: distributed recurrent candidate
```

Interpretation: the strict subset contains stable positional sign behavior sufficient to define a structural hypothesis queue. It does not identify meanings.

## Formula Pattern Probe

Reference:

[Formula pattern probe](formula_pattern_probe.md)

The first formula-pattern pass mapped structural sign classes into inscription-level class patterns under raw numeric, isolated `P385` merge, and observed `mayig` Parpola policies.

Key results:

```text
raw_lipi_numeric_exact_patterns: 123
raw_lipi_numeric_recurrent_exact_coverage: 0.169118
raw_lipi_numeric_I_T_scaffold_observed: 22
raw_lipi_numeric_I_T_scaffold_reversed: 0
raw_lipi_numeric_I_T_scaffold_shuffle_mean: 1.25
mayig_observed_parpola_exact_patterns: 113
mayig_observed_parpola_recurrent_exact_coverage: 0.301471
mayig_observed_parpola_I_T_scaffold_observed: 23
mayig_observed_parpola_I_T_scaffold_reversed: 0
mayig_observed_parpola_I_T_scaffold_shuffle_mean: 1.25
top_edge_anchor_pair: 740...817/861 -> P324...P385 in 10 rows
```

Interpretation: the strict subset contains directional edge-class scaffolding, especially around the `740/P324` initial candidate and `817/861/P385` terminal candidate. Exact formula recurrence remains weak, so this is still A2 structural evidence only.

## Formula Variant Probe

Reference:

[Formula variant probe](formula_variant_probe.md)

The strict Mayig-policy formula rows were searched for near-duplicates, shared edge frames, and single-slot variants.

Key results:

```text
strict_records: 136
exact_duplicate_sequence_groups: 1
near_pairs_edit_distance_le_2: 75
single_substitution_pairs: 5
shared_edge_frame_pairs: 69
frame_families_count: 14
slot_candidate_groups: 3
top_frame_family: P324...P385 in 10 rows
exact_duplicate_candidate: M-32/M-177 = P086 P123 P122 P385
```

Interpretation: this produces a review queue for possible formula families and variable slots. It does not assign values, meanings, or translations.

## Formula Variant Null Model

Reference:

[Formula variant null model](formula_variant_null_model.md)

The Mayig-policy formula-variant queue was tested against 500 deterministic iterations of two null models: one preserving only row lengths and global sign frequency, and one preserving row lengths plus first-sign, last-sign, and interior-token distributions.

Key results:

```text
variant_pairs_observed: 129
variant_pairs_length_frequency_mean: 47.044
variant_pairs_edge_preserving_mean: 159.806
near_pairs_observed: 75
near_pairs_length_frequency_mean: 41.142
near_pairs_edge_preserving_mean: 98.324
shared_edge_pairs_observed: 69
shared_edge_pairs_length_frequency_mean: 6.614
shared_edge_pairs_edge_preserving_mean: 69.620
top_frame_rows_observed: 10
top_frame_rows_length_frequency_mean: 2.632
top_frame_rows_edge_preserving_mean: 9.612
```

Interpretation: the apparent formula-variant excess is strong under a loose length/frequency null, but mostly explained by first/last sign position under the edge-preserving null. The queue remains useful for manual review; it is not independent semantic evidence.

## Sensitivity Formula Probe

Reference:

[Sensitivity formula probe](sensitivity_formula_probe.md)

The 12 count-matching sensitivity-flag rows were tested against the same structural sign profiles.

Key results:

```text
sensitivity_rows: 12
tokens_per_policy: 84
raw_lipi_numeric_rows_with_missing_profile: 8
raw_lipi_numeric_missing_profile_share: 0.130952
raw_lipi_numeric_I_T_scaffold: 0 of 12
mayig_observed_parpola_rows_with_missing_profile: 11
mayig_observed_parpola_missing_profile_share: 0.190476
mayig_observed_parpola_I_T_scaffold: 1 of 12
exact_formula_recurrence: 0
```

Interpretation: sensitivity rows are useful stress cases, but they do not strengthen the formula scaffold. Slash compounds create cross-source disagreement, and `P000` rows cannot validate Parpola-side structural formulas.

## Metadata Scope Probe

Reference:

[Metadata scope probe](metadata_scope_probe.md)

The local Mayig descriptions were joined to the strict, sensitivity, and mismatch-gated rows.

Key results:

```text
total_mayig_records: 179
description_family_count: 1
description_family: unicorn
description_kind: seal
unicorn_IV_records: 96 of 179
strict_formula_rows: 136
unicorn_IV_strict_formula_rows: 79 of 136
```

Interpretation: the current open prototype is a Mohenjo-daro unicorn-seal subset. The structural scaffold is not yet evidence for cross-iconography, cross-artifact-class, or IVC-wide grammar.

## Lipi Broader Scope Probe

Reference:

[Lipi broader scope probe](lipi_broader_scope_probe.md)

The filtered `lipi` metadata was profiled without using the quarantined claim columns.

Key results:

```text
lipi_rows: 5679
rows_with_cisi: 5018
rows_lipi_numeric_clean_candidates: 2887
rows_lipi_direction_clean_candidates: 3308
rows_complex_text: 2079
rows_with_000_unknown: 1337
rows_with_bracket: 1438
top_types: SEAL:S 1777; TAB:B 1108; TAB:I 952; POT:T:g 538; SEAL:R 388
top_sites: Harappa 2717; Mohenjo-daro 1923; Dholavira 238; Kalibangan 212; Lothal 208
```

Interpretation: `lipi` gives a broader planning layer for artifact-class and site baselines than the Mayig unicorn-seal subset, especially for sealings, tablets, and reverse seals. It remains a T3 source, so this is experiment planning and scout analysis only.

## Lipi Broad Order Baseline

Reference:

[Lipi broad order baseline](lipi_broad_order_baseline.md)

The strict numeric-clean `lipi` planning layer was tested for stored-order structure and exact-sign masked prediction across artifact and site splits.

Key results:

```text
numeric_clean_rows: 2887
numeric_clean_tokens: 11655
unique_signs: 571
stored_order_beats_reversed: 2748 of 2887
stored_order_reversed_beats_stored: 131 of 2887
bidirectional_bigram_top1: 0.408323
frequency_top1: 0.106221
position_top1: 0.141399
length_position_top1: 0.191420
heldout_type_SEAL_S_bidirectional_top1: 0.270181
heldout_type_TAB_B_bidirectional_top1: 0.340611
heldout_site_Harappa_bidirectional_top1: 0.237734
heldout_site_Mohenjo_daro_bidirectional_top1: 0.265018
exact_duplicate_rows: 1355 of 2887
```

Interpretation: the broad filtered layer contains stored-order dependencies beyond frequency and simple position baselines, and the bidirectional context signal survives held-out artifact/site tests. However, duplicate/formula-heavy rows inflate within-split scores, especially in tablet classes. This remains T3 structural scout evidence only.

## Lipi Deduplicated Order Baseline

Reference:

[Lipi deduplicated order baseline](lipi_dedup_order_baseline.md)

The broad `lipi` order baseline was rerun after exact duplicate numeric sign sequences were collapsed within each evaluated scope or split.

Key results:

```text
source_rows: 2887
collapsed_rows: 1798
duplicate_rows_removed: 1089
stored_order_beats_reversed: 1705 of 1798
stored_order_reversed_beats_stored: 84 of 1798
bidirectional_bigram_top1: 0.325865
frequency_top1: 0.107769
position_top1: 0.151120
length_position_top1: 0.154652
heldout_type_SEAL_S_bidirectional_top1: 0.291057
heldout_type_TAB_B_bidirectional_top1: 0.314097
heldout_site_Harappa_bidirectional_top1: 0.276365
heldout_site_Mohenjo_daro_bidirectional_top1: 0.307220
```

Interpretation: exact duplicate collapse leaves stored-order structure mostly intact but substantially lowers within-split exact-sign prediction. Held-out split scores remain above simple baselines, so duplicate memorization is not the whole signal. Cross-split exact-sequence overlap still exists in this run, so the stricter leakage-control pass below is required before using held-out scores as structural evidence.

## Lipi Leakage-Controlled Held-Out Baseline

Reference:

[Lipi leakage-controlled held-out baseline](lipi_leakage_control_baseline.md)

The duplicate-collapsed held-out tests were rerun after removing from training every exact numeric sign sequence that appears in the held-out test split.

Key results:

```text
reported_holdout_rows: 48
test_sequence_seen_share: 0 for all reported rows
type_SEAL_S_bidirectional_top1: 0.283740
type_TAB_I_bidirectional_top1: 0.271914
type_TAB_B_bidirectional_top1: 0.305853
site_Harappa_bidirectional_top1: 0.271129
site_Mohenjo_daro_bidirectional_top1: 0.297402
site_Lothal_bidirectional_top1: 0.301075
site_Kalibangan_bidirectional_top1: 0.289474
```

Interpretation: removing exact train/test sequence overlap weakens the duplicate-collapsed held-out scores only slightly in the selected type and site splits. Bidirectional context remains above frequency, position, and length-position baselines, so exact cross-split sequence leakage is not enough to explain the broad structural signal. This remains T3 structural scout evidence only, not semantic or translation evidence.

## Lipi High-Frequency Edge Removal Baseline

Reference:

[Lipi high-frequency edge removal baseline](lipi_edge_removed_baseline.md)

The broad `lipi` order tests were rerun after removing the highest-frequency edge signs from every sequence, dropping empty rows, and collapsing exact duplicate resulting sequences.

Top edge signs:

```text
top_2: 740, 700
top_5: 740, 700, 400, 520, 033
top_10: 740, 700, 400, 520, 033, 032, 861, 817, 820, 034
```

Key top-10 removal results:

```text
evaluated_rows_after_collapse: 1658 from 2887 source rows
tokens_after_top_10_removal: 5913
stored_order_beats_reversed: 1383 of 1530 rows longer than one sign
stored_order_reversed_beats_stored: 129 of 1530
stored_win_share: 0.903922
bidirectional_top1: 0.222222
frequency_top1: 0.072383
position_top1: 0.088449
length_position_top1: 0.092508
heldout_type_SEAL_S_bidirectional_top1: 0.180733
heldout_type_TAB_B_bidirectional_top1: 0.177461
heldout_site_Harappa_bidirectional_top1: 0.176140
heldout_site_Mohenjo_daro_bidirectional_top1: 0.199020
```

Interpretation: high-frequency edge signs explain a large part of the broad structural signal, but not all of it. After removing the top 10 edge signs, stored-order likelihood and leakage-controlled held-out exact-sign prediction remain above simple baselines. This is a stricter T3 structural residue, not a semantic or translation result.

## Lipi Formula-Family Downweighting Baseline

Reference:

[Lipi formula-family downweighting baseline](lipi_family_downweight_baseline.md)

The broad `lipi` structural tests were rerun after downweighting formula families. The experiment first collapses exact duplicate sequences, then applies edge-frame collapse and one-edit-family collapse. Both controls are also repeated after top-10 edge-sign removal.

Key results:

```text
edge_frame_rows: 1408 from 1798 exact-collapsed rows
edge_frame_bidirectional_top1: 0.286578
one_edit_family_rows: 1098 from 1798 exact-collapsed rows
one_edit_family_largest_family_records: 241
one_edit_family_bidirectional_top1: 0.310764
top10_edge_removed_one_edit_rows: 838 from 1658 top10-edge exact-collapsed rows
top10_edge_removed_one_edit_largest_family_records: 377
top10_edge_removed_one_edit_bidirectional_top1: 0.224004
top10_edge_removed_one_edit_frequency_top1: 0.070659
top10_edge_removed_one_edit_position_top1: 0.085192
top10_edge_removed_one_edit_length_position_top1: 0.085943
top10_edge_removed_one_edit_heldout_SEAL_S_bidirectional_top1: 0.179978
top10_edge_removed_one_edit_heldout_TAB_B_bidirectional_top1: 0.200422
top10_edge_removed_one_edit_heldout_Harappa_bidirectional_top1: 0.183817
top10_edge_removed_one_edit_heldout_Mohenjo_daro_bidirectional_top1: 0.199853
```

Interpretation: repeated formula families are not enough to explain the residual broad signal. The one-edit policy is aggressive and produces very large connected families, so it should be treated as a blunt anti-template stress test rather than a natural family inventory. Even under combined top-10 edge removal and one-edit-family collapse, bidirectional context remains above frequency, position, and length-position baselines in the selected held-out splits. This remains T3 structural scout evidence only.

## Lipi Synthetic Comparator Baseline

Reference:

[Lipi synthetic comparator baseline](lipi_synthetic_comparator_baseline.md)

The broad duplicate-collapsed `lipi` structural tests were compared against four strong synthetic nonlinguistic controls: length-frequency shuffle, edge-position shuffle, edge-frame template shuffle, and position-slot shuffle.

Key results:

```text
iterations_per_control: 5
observed_stored_win_share: 0.948276
edge_position_stored_win_share_mean: 0.936235
edge_frame_template_stored_win_share_mean: 0.938605
position_slot_stored_win_share_mean: 0.939385
observed_bidirectional_top1: 0.325865
length_frequency_bidirectional_top1_mean: 0.098096
edge_position_bidirectional_top1_mean: 0.108714
edge_frame_template_bidirectional_top1_mean: 0.124866
position_slot_bidirectional_top1_mean: 0.143747
observed_bidirectional_top5: 0.567828
position_slot_bidirectional_top5_mean: 0.312740
```

Interpretation: stored-order asymmetry is not diagnostic by itself because edge- and slot-preserving nonlinguistic controls nearly reproduce it. Simple positional metrics are also weak: the position-slot null exceeds the observed layer on length-position top-1. The residual structural signal worth testing is duplicate-collapsed bidirectional context, which remains above all four synthetic controls in this scout. This is still T3 structural evidence only, not semantic or translation evidence.

## Lipi Structured Null Comparator

Reference:

[Lipi structured null comparator](lipi_structured_null_comparator.md)

The broad duplicate-collapsed `lipi` structural tests were compared against duplicate-calibrated nonlinguistic code generators. Every structured null matches the observed unique sequence count, duplicate row share, and top sequence count before metrics are compared.

Key results:

```text
iterations_per_control: 5
calibrated_unique_sequences: 1798
calibrated_duplicate_row_share: 0.469345
observed_bidirectional_top1: 0.325865
duplicate_matched_position_slot_bidirectional_top1_mean: 0.140697
administrative_register_bidirectional_top1_mean: 0.472114
emblem_formula_bidirectional_top1_mean: 0.441719
mixed_admin_emblem_bidirectional_top1_mean: 0.416074
observed_bidirectional_top5: 0.567828
administrative_register_bidirectional_top5_mean: 0.687969
emblem_formula_bidirectional_top5_mean: 0.690550
mixed_admin_emblem_bidirectional_top5_mean: 0.662811
```

Interpretation: independent duplicate-matched position slots do not reproduce bidirectional context, but explicit nonlinguistic administrative and emblem dependencies exceed observed bidirectional masked-sign prediction. This downgrades bidirectional top-1 as standalone evidence. The next target is a harder profile: metadata prediction, artifact-class split behavior, sign-class stability, and known-script scarcity comparators.

## Lipi Metadata Prediction Probe

Reference:

[Lipi metadata prediction probe](lipi_metadata_prediction_probe.md)

The broad `lipi` numeric-clean layer was collapsed to 1,798 exact sign-sequence families. Each family received the majority label for a metadata target, then leave-one-out predictors tried to recover metadata from signs. The same evaluation was run on family-level structured nulls.

Key observed Token NB results:

```text
type_token_nb_accuracy: 0.633492
site_token_nb_accuracy: 0.654284
region_token_nb_accuracy: 0.638717
material_token_nb_accuracy: 0.736404
direction_token_nb_accuracy: 0.942158
class_token_nb_accuracy: 0.543312
class_token_nb_macro_f1: 0.474895
```

Key null comparison:

```text
type_mixed_admin_emblem_null_mean: 0.644458 vs observed 0.633492
site_mixed_admin_emblem_null_mean: 0.649731 vs observed 0.654284
region_mixed_admin_emblem_null_mean: 0.642994 vs observed 0.638717
class_position_slot_null_mean: 0.289452 vs observed 0.543312
class_admin_null_mean: 0.281791 vs observed 0.543312
class_emblem_null_mean: 0.270359 vs observed 0.543312
class_mixed_null_mean: 0.271538 vs observed 0.543312
```

Interpretation: type, site, and region prediction are confounded by artifact-type mixtures. Material and direction are dominated by majority labels. The strongest surviving metadata scout signal is inscription `class`, where observed sign-token prediction beats all structured nulls. This still remains T3 metadata evidence and may reflect cataloging conventions rather than ancient structure.

## Lipi Stratified Class Probe

Reference:

[Lipi stratified class probe](lipi_stratified_class_probe.md)

The `class` prediction result was rerun inside eligible site, artifact-type, and type-site strata. Exact sign-sequence families were used, and the same structured null controls were rerun inside each stratum.

Key results:

```text
eligible_strata: 11
min_stratum_rows: 90
min_label_rows: 12
harappa_class_token_nb: 0.519008
mohenjo_daro_class_token_nb: 0.506937
seal_r_class_token_nb: 0.534483
seal_s_class_token_nb: 0.466736
tab_b_class_token_nb: 0.520161
tab_i_class_token_nb: 0.729508
seal_s_harappa_class_token_nb: 0.386076
seal_s_mohenjo_daro_class_token_nb: 0.456681
tab_b_harappa_class_token_nb: 0.527919
tab_i_harappa_class_token_nb: 0.720339
minimum_observed_minus_null_mean_gap_for_token_nb: 0.08
null_iterations_reaching_observed_token_nb: 0 in every eligible stratum
```

Interpretation: the class signal survives within major artifact-type and site strata, including eligible type-site strata. This is the cleanest metadata scout so far, but it still depends on T3 catalog labels and does not prove that catalog classes are ancient semantic or functional classes.

## Lipi Class Robustness Probe

Reference:

[Lipi class robustness probe](lipi_class_robustness_probe.md)

The `class` prediction result was attacked with edge-sign removal and formula-family downweighting. The probe evaluates exact sequence collapse, edge-frame collapse, and one-edit-family collapse, then repeats all three after removing the top-10 edge signs.

Key results:

```text
source_rows: 2887
exact_sequence_families: 1798
top10_edge_removed_exact_families: 1658
top10_edge_removed_one_edit_families: 838
exact_sequence_token_nb_accuracy: 0.525714
exact_sequence_token_nb_macro_f1: 0.356200
top10_edge_removed_exact_token_nb_accuracy: 0.474430
top10_edge_removed_edge_frame_token_nb_accuracy: 0.476568
top10_edge_removed_one_edit_token_nb_accuracy: 0.372236
top10_edge_removed_one_edit_token_nb_macro_f1: 0.228813
top10_edge_removed_one_edit_majority_accuracy: 0.212531
top10_edge_removed_one_edit_length_accuracy: 0.374693
top10_edge_removed_one_edit_edge_frame_accuracy: 0.382064
mohenjo_daro_top10_edge_one_edit_token_nb_accuracy: 0.398438
seal_s_mohenjo_daro_top10_edge_one_edit_token_nb_accuracy: 0.405995
```

Interpretation: edge-sign removal alone does not erase the class signal, but the harshest combined control downgrades it. Token NB remains above majority and keeps better macro-F1 than length/edge-frame controls, but its raw accuracy is matched or exceeded by length and edge-frame shortcuts in the overall harsh-control layer. Class remains the best metadata scout target, but it is not clean enough for semantic interpretation until the `class` field itself is source-audited and repeated on authoritative or image-validated data.

## Lipi Class Field Audit

Reference:

[Lipi class field audit](lipi_class_field_audit.md)

The `class` field was source-audited against the upstream `yajnadevam/lipi` repository and the local filtered layer.

Key results:

```text
repo_head_checked: b272ad99c253ba7fa1e4cd91f48cce31f6d02bf4
scanned_text_files: 67
class_definition_matches_found: 0
class_values_all_rows: 25
class_values_numeric_clean: 21
top_classes_all_rows: ?? 1341; SS 709; UC 666; SC 606; VN 355; MT 330; IT 276; SP 225; LP 212; TS 168
vn_harappa_share: 0.985915
vn_length_2_share: 0.946479
ts_length_1_share: 0.988095
pn_length_2_share: 0.849057
uc_numeric_clean_rows: 0
```

Interpretation: `lipi.class` is not currently admissible as independent semantic metadata. No upstream class-code definitions were found in the scanned repository text, the source repository makes decipherment claims, and several class labels are strongly shaped by length, site, type, or completeness. Prior class-prediction experiments remain useful as source-field stress tests, not as semantic evidence.

## Lipi Class Proxy-Control Probe

Reference:

[Lipi class proxy-control probe](lipi_class_proxy_control_probe.md)

The downgraded `class` field was tested against label filters and metadata-block label shuffles.

Key results:

```text
exact_sequence_families: 1798
iterations_per_shuffle_block: 20
all_eligible_token_nb: 0.525714
all_eligible_length_type_site_shuffle_mean: 0.254029
proxy_ge_080_removed_labels: PN
proxy_ge_080_token_nb: 0.533256
proxy_ge_080_length_type_site_shuffle_mean: 0.256564
proxy_ge_065_removed_labels: IT;LP;MS;PN;VX
proxy_ge_065_rows: 1230
proxy_ge_065_token_nb: 0.643089
proxy_ge_065_token_nb_macro_f1: 0.522030
proxy_ge_065_length_type_site_shuffle_mean: 0.322154
proxy_ge_065_length_type_site_shuffle_macro_f1_mean: 0.209834
```

Interpretation: `lipi.class` remains recoverable from exact sign tokens after simple row-metadata proxy controls. That does not rescue it as semantic evidence. Because the class codes are undefined and may be sign-derived, the survival of the signal points toward source-internal coding or circularity. Future semantic experiments should use clearer-provenance metadata targets instead.

## Lipi Semantic Anchor Target Audit

Reference:

[Lipi semantic anchor target audit](lipi_semantic_anchor_target_audit.md)

After the `class` downgrade, the next question is which clearer-provenance metadata fields can support semantic-anchor prediction experiments. The audit uses the same strict numeric-clean `lipi` layer, collapses exact duplicate numeric sign sequences, and checks label coverage plus metadata/sign proxy risk.

Key results:

```text
source_rows: 5679
numeric_clean_source_rows: 2887
exact_sequence_families: 1798
min_label_families: 30
candidate_targets: symbol; cult; material; shape; boss; type; horizontal_bin; vertical_bin; thickness_bin; area_bin; aspect_bin
symbol_eligible_families: 952
symbol_eligible_labels: 10
symbol_majority_share: 0.310924
cult_eligible_families: 783
cult_eligible_labels: 5
material_eligible_families: 1563
material_eligible_labels: 4
shape_eligible_families: 1604
shape_eligible_labels: 6
type_eligible_families: 1710
type_eligible_labels: 6
color_status: majority_dominated
```

Interpretation: the filtered `lipi` layer has enough candidate labels for iconography, cult apparatus, material, object form, artifact type, and coarse dimensions. None are clean by default. For example, some symbol labels are pure or near-pure proxies for shape or cult fields, `TAB:C` is pure `Copper`, `SEAL:S` is almost entirely square, and direction is overwhelmingly `R/L`. The next prediction experiment must therefore use blocked label-shuffle controls preserving length, type, site, material, shape, direction, and edge frame.

## Lipi Semantic Anchor Prediction Probe

Reference:

[Lipi semantic anchor prediction probe](lipi_semantic_anchor_prediction_probe.md)

The candidate semantic-anchor targets were tested with leave-one-out shortcut models and blocked label-shuffle nulls.

Key results:

```text
source_rows: 5679
numeric_clean_source_rows: 2887
exact_sequence_families: 1798
iterations_per_block: 3
symbol_token_nb: 0.276261
symbol_hard_proxy_null_mean: 0.283613
cult_token_nb: 0.605364
cult_type_null_mean: 0.610047
material_token_nb: 0.736404
material_type_null_mean: 0.736618
boss_token_nb: 0.724528
boss_type_site_null_mean: 0.736268
type_token_nb: 0.621637
type_edge_frame_null_mean: 0.620663
vertical_bin_token_nb: 0.465507
vertical_bin_edge_frame_null_mean: 0.443754
```

Interpretation: no candidate semantic-anchor target is clean enough to promote. `symbol`, `cult`, `material`, `boss`, and `thickness_bin` are matched or exceeded by their hardest Token NB nulls. `shape`, `type`, and dimension bins have only small residual gaps against edge-frame-preserved nulls, and those edge-frame nulls leave many labels unchanged because the blocks are tight. This turns the semantic-anchor work into a narrower falsification problem rather than a reading.

## Lipi Dimension Residue Stress Probe

Reference:

[Lipi dimension residue stress probe](lipi_dimension_residue_stress_probe.md)

The small dimension-bin residues from the semantic-anchor probe were attacked with fresh broad sign classes and stronger shortcut models.

Key results:

```text
source_rows: 5679
numeric_clean_source_rows: 2887
exact_sequence_families: 1798
iterations_per_block: 10
sign_classes: sparse 494; medial 34; distributed 25; initial 10; terminal 5; edge_mixed 3
horizontal_bin_token_nb: 0.444114
horizontal_bin_hard_proxy_null_mean: 0.434483
vertical_bin_token_nb: 0.465507
vertical_bin_edge_frame_null_mean: 0.449037
vertical_bin_length_type_site: 0.627098
vertical_bin_material_shape: 0.597265
thickness_bin_token_nb: 0.482227
thickness_bin_edge_frame_null_mean: 0.476896
area_bin_token_nb: 0.441875
area_bin_edge_frame_null_mean: 0.433937
aspect_bin_token_nb: 0.638871
aspect_bin_edge_frame_null_mean: 0.633668
```

Interpretation: the dimension residues are not metrological evidence. The largest remaining Token NB gap is `vertical_bin`, but simple metadata shortcuts beat sign-token prediction by a lot. `vertical_bin` Token NB is 0.465507, while length+type+site reaches 0.627098 and material+shape reaches 0.597265. The current broad metadata route is therefore blocked for size/metrology interpretation.

## Lipi Multi-Side Mark Scope Probe

Reference:

[Lipi multi-side mark scope probe](lipi_multiside_mark_scope_probe.md)

The numerical/metrological route was redirected from broad dimension prediction to multi-side artifacts with short side marks.

Key results:

```text
source_rows: 5679
rows_with_cisi: 5018
cisi_groups: 4074
multiside_or_multirow_cisi_groups: 864
multiside_rows: 1808
clean_multiside_rows: 1109
short_mark_candidate_rows: 539
long_text_candidate_rows: 558
short_mark_token_total: 1078
top_short_mark_tokens: 700 374; 033 146; 034 115; 032 105; 003 51; 861 30; 156 28
highest_enrichment_tokens: 034 31.365491; 167 18.058919; 700 14.750415; 003 6.813438; 137 6.707599; 033 6.145486
short_mark_rows_by_type: TAB:I 273; TAB:B 239; SEAL:S 10; TAB:C 5; SEAL:R 5
short_mark_rows_by_site: Harappa 497; Mohenjo-daro 40; Kalibangan 1; Unknown 1
```

Interpretation: this gives a concrete side-mark review queue. It does not assign numerical values. The queue is heavily Harappa/tablet-shaped, so the next test must stratify `TAB:I` and `TAB:B` and validate actual artifact sides or images before any metrological claim is allowed.

## Lipi Multi-Side Mark Stratified Probe

Reference:

[Lipi multi-side mark stratified probe](lipi_multiside_mark_stratified_probe.md)

The broad short-mark queue was split inside the two dominant strata: Harappa `TAB:B` and Harappa `TAB:I`.

Key results:

```text
harappa_tab_b_rows: 687
harappa_tab_b_short_mark_rows: 222
harappa_tab_b_long_text_rows: 246
harappa_tab_b_short_mark_token_total: 444
harappa_tab_b_top_by_enrichment: 034 176.278409; 700 16.723283; 033 4.839015; 032 4.385712
harappa_tab_b_side_indexes: 1 115; 2 106; 3 1
harappa_tab_i_rows: 779
harappa_tab_i_short_mark_rows: 269
harappa_tab_i_long_text_rows: 204
harappa_tab_i_short_mark_token_total: 538
harappa_tab_i_top_by_enrichment: 034 38.274234; 003 26.659983; 700 24.937296; 033 16.437524; 861 5.786820
harappa_tab_i_side_indexes: 1 94; 2 149; 3 26
```

Interpretation: the side-mark review queue survives type-site stratification. `700`, `034`, and `033` recur in both Harappa tablet strata, while `003`, `861`, and `156` are sharper in Harappa `TAB:I`; `003` and `156` concentrate in `TAB:I` row side index 3. This sharpens the manual validation queue, but it does not assign values, measures, side functions, sign meanings, or translations.

## Lipi Multi-Side Mark Validation Queue

Reference:

[Lipi multi-side mark validation queue](lipi_multiside_mark_validation_queue.md)

The stratified short-mark result was converted into artifact-level source/image validation queues.

Key results:

```text
artifact_groups_with_short_marks: 397
P1_tab_i_three_side_short_series: 22
P1_mixed_short_long_core: 205
P2_tab_b_core_short_queue: 81
P2_tab_i_core_short_queue: 70
P3_other_short_mark: 19
top_mixed_family: TAB:I 1:+400-740-176+|2:+700-033+ in 13 artifacts
top_three_side_family: TAB:I 1:+861-003+|2:+700-034+|3:+156-003+ in 13 artifacts
second_three_side_family: TAB:I 1:+700-034+|2:+861-003+|3:+156-003+ in 7 artifacts
```

External source check: Kenoyer and Meadow 2010 identifies H-2218 through H-2239 as a 22-object group of rectangular steatite tablets, triangular in section, from Period 3B secondary deposits at Harappa. That source anchor makes the H-2218 through H-2239 local queue a high-value validation target, but it does not explain the signs or tablet function.

Interpretation: the next E3.2 work should split all-short three-side tablet series from mixed short-long tablet artifacts. The validation queue does not assign numbers, measures, physical side functions, sign meanings, or translations.

## Lipi Short-Mark Orientation Audit

Reference:

[Lipi short-mark orientation audit](lipi_short_mark_orientation_audit.md)

The Harappa `TAB:B`/`TAB:I` short-mark rows were checked for internal order in two-token `700` companion marks.

Key results:

```text
target_short_mark_rows: 491
two_token_700_companion_rows: 368
core_032_033_034_rows: 353
700_first: 313
700_last: 55
032: 85 first; 17 last
033: 113 first; 24 last
034: 101 first; 13 last
corrected_orientation_flags: balance 032/033/034; type-split 032/033
```

Interpretation: `700`-companion short marks are strongly `700`-first overall, but reversed forms are present and type-conditioned for `032` and `033`. Exact order must be preserved in validation sheets; `+700-033+` cannot be silently normalized with `+033-700+`. This is an orientation control, not a numerical, metrological, semantic, or translation result.

## Lipi Short-Mark Context Orientation Audit

Reference:

[Lipi short-mark context orientation audit](lipi_short_mark_context_orientation_audit.md)

The core `032`/`033`/`034` two-token `700` short marks were checked against longer-row context on the same artifact.

Key results:

```text
target_rows: 353
TAB:B_rows: 178
TAB:I_rows: 175
700_first: 299
700_last: 54
single_longer_text: 233
no_longer_text_total: 115
short_after_all_longer: 132
short_before_all_longer: 105
emitted_tests: 57
corrected_context_flags: none
```

Smallest raw context checks:

```text
033 has +400-740-176+ longer sequence: raw p 0.024009; BH FDR 0.741941
034 single longer text: raw p 0.035597; BH FDR 0.741941
034 any longer text: raw p 0.039050; BH FDR 0.741941
```

Interpretation: reversed core `700` companion marks do not currently show a corrected longer-context association. Exact order still has to be preserved for source validation because the prior orientation audit found a strong order imbalance, but this context audit does not turn reversal into a functional, numerical, semantic, or translation contrast.

## Lipi Short-Mark Companion Context Audit

Reference:

[Lipi short-mark companion context audit](lipi_short_mark_companion_context_audit.md)

The core `032`/`033`/`034` two-token `700` companion rows were tested for same-artifact longer-row context binding. The strongest control shuffles companion labels within `type|700_order` blocks.

Key results:

```text
target_rows: 353
TAB:B_rows: 178
TAB:I_rows: 175
032_rows: 102
033_rows: 137
034_rows: 114
emitted_tests: 90
permutation_iterations: 5000
permutation_block: type|700_order
corrected_block_permutation_flags: 033 short_after_all_longer;034 short_after_all_longer
```

Corrected side-relation flags:

```text
033 short_after_all_longer: companion share 0.489051; other share 0.300926; block BH FDR 0.035993
034 short_after_all_longer: companion share 0.219298; other share 0.447699; block BH FDR 0.035993
```

Raw-only hints:

```text
033 with longer +400-740-176+: Fisher BH FDR 0.057772; block BH FDR 0.082269
032 with longer +400-740-176+: Fisher BH FDR 0.057772; block BH FDR 0.107978
```

Interpretation: the `033`/`034` contrast carries a corrected catalog-side relation difference in this planning layer. That makes it a sharper plate-validation target: source images should test whether `short_after_all_longer` is real physical side/order structure or only catalog ordering. The raw `+400-740-176+` hint remains below the acceptance line. No numerical, metrological, side-function, semantic, or translation claim is accepted.

## Lipi Short-Mark Side-Relation Validation Sheet

Reference:

[Lipi short-mark side-relation validation sheet](lipi_short_mark_side_relation_validation_sheet.md)

The corrected `033`/`034` catalog-side contrast was converted into a source-validation worklist.

Key results:

```text
target_rows: 251
target_artifacts: 250
033_rows: 137
034_rows: 114
short_after_all_longer: 92
short_before_all_longer: 72
no_longer_text: 86
raw_400_740_176_rows: 29
raw_400_740_176_artifacts: 28
```

Priority classes:

```text
P1_033_after_with_400_740_176: 16 rows, 15 artifacts
P1_034_before_with_400_740_176: 2 rows, 2 artifacts
P1_033_after_corrected_relation: 51 rows
P1_034_before_contrast_relation: 38 rows
P2_034_after_exception_control: 25 rows
P2_033_before_exception_control: 32 rows
P2_raw_400_740_176_context: 1 row
P3_no_longer_text_control: 86 rows
```

Highest priority unique artifacts:

```text
H-233, H-309, H-316, H-353, H-355, H-357, H-935, H-978, H-1302, H-1303, H-1304, H-1344, H-1345, H-1346, H-1347, H-933, H-960
```

Interpretation: this turns the corrected catalog-side relation contrast into an image/plate inspection queue. The first source request should check whether those 17 artifacts preserve the apparent `033` after-longer versus `034` before-longer split under real physical side order and image direction. No physical side function, number, measure, sign meaning, or translation is accepted.

## Lipi Short-Mark Plate Request Packet

Reference:

[Lipi short-mark plate request packet](lipi_short_mark_plate_request_packet.md)

The 17 highest-priority side-relation artifacts were converted into a manual source-validation packet with blank evidence fields.

Key results:

```text
packet_artifacts: 17
packet_rows_from_validation_sheet: 18
tier_1_033_after_with_400_740_176: 15 artifacts
tier_1_034_before_with_400_740_176: 2 artifacts
TAB:B: 1 artifact
TAB:I: 16 artifacts
duplicated_artifact_in_packet: H-355
```

Manual fields include:

```text
source_found
source_citation
image_or_plate_id
image_resolution_or_quality
catalog_rows_distinct_physical_sides
side_order_basis
image_direction_basis
short_mark_verified
longer_text_verified
sign_033_034_contrast_visible
relation_survives_image_check
validation_outcome
notes
```

Allowed outcomes:

```text
passes_source_check
fails_side_relation
fails_segmentation
fails_033_034_contrast
direction_unresolved
source_unavailable
```

Interpretation: this is now ready for manual source inspection. It is intentionally not a claim of validation; all decisive fields are blank until a plate, image, or catalog note fills them.

## Lipi Short-Mark Plate Public Lead Search

Reference:

[Lipi short-mark plate public lead search](lipi_short_mark_plate_public_lead_search.md)

The 17-artifact plate request packet was checked against public source and image leads.

Key results:

```text
packet_artifacts: 17
source_pages_checked: 20
fixed_source_pages_checked: 3
blogger_atom_queries_checked: 17
lead_rows: 31
candidate_image_or_post_leads: H-233; H-1302; H-1303
published_direction_or_corpus_notes: H-1302; H-1303
text_only_or_bibliographic_leads: H-233; H-309; H-316; H-353; H-355; H-357; H-933; H-935; H-960; H-978
no_public_lead_in_checked_sources: H-1304; H-1344; H-1345; H-1346; H-1347
```

Interpretation: this improves source targeting but validates no artifact. The H-233 and H-1302/H-1303 image/post leads are still claim-heavy secondary leads; the H-1302/H-1303 published note is a direction/corpus-correction lead, not a plate check. A later H-233 visual audit narrows the H-233 page-image URLs to one H-233-relevant slide and one off-target H-1997 slide. The packet still requires CISI plates, HARP/Harappa images, or archive access before side order, segmentation, allography, or the `033`/`034` relation can be accepted.

## Lipi Short-Mark Source Acquisition Queue

Reference:

[Lipi short-mark source acquisition queue](lipi_short_mark_source_acquisition_queue.md)

The 17-artifact packet and public lead search were converted into a source-acquisition queue.

Key results:

```text
queue_artifacts: 17
A_direction_note_recheck: 2
A_double_short_side_case: 1
A_034_contrast_case: 2
A_tab_b_type_control_with_public_image_lead: 1
B_source_dark_direct_cisi_or_harp: 5
C_replicate_033_after_case: 6
first_actions: H-1302; H-1303; H-355; H-933; H-960; H-233
source_dark_direct_requests: H-1304; H-1344; H-1345; H-1346; H-1347
```

Interpretation: this is a practical acquisition order, not a new evidential claim. It starts with the two H-1302/H-1303 direction-note rechecks, the H-355 double-short-side ambiguity, the H-933/H-960 `034` contrast cases, and H-233 as the `TAB:B` type-control with public slide leads. No side relation, physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, or translation is accepted.

## H-233 Public Slide Visual Lead Audit

Reference:

[H-233 public slide visual lead audit](h233_public_slide_visual_lead_audit.md)

The two image URLs captured from the H-233 public post were downloaded to a temporary folder and inspected manually. No image copy is stored in the repository.

Key results:

```text
candidate_images_checked: 2
h233_relevant_public_slides: 1
off_target_page_images: 1
repo_image_storage: none
```

Manual result:

```text
Slide 1: H-233-relevant public slide with tiny H-233 A/B panels.
Slide 2: H-1997 slide, not an H-233 image lead.
```

Interpretation: the public post supplies one low-grade H-233 visual pointer, not two. The relevant slide is still a secondary presentation image, so it can target a plate request but cannot fill the H-233 source-validation fields. The false positive gives a concrete rule for later public-image sweeps: image URLs from a page must be visually checked for object-level relevance before they are counted.

## H-1302/H-1303 Direction-Note Recheck

Reference:

[H-1302/H-1303 direction-note recheck](h1302_h1303_direction_note_recheck.md)

The Nature 2021 direction/allograph lead and public Blogger image set for H-1302/H-1303 were checked as source-reconciliation evidence.

Key results:

```text
published_direction_source: Nature 2021
packet_objects: H-1302; H-1303
public_image_urls_checked: 8
unlabeled_object_panel_candidates: 2
tiny_unlabeled_crops: 2
standalone_sign_icons: 2
context_or_lexical_excerpts: 2
source_validation_fields_filled: 0
```

Interpretation: the Nature article is a real direction/corpus-correction lead because it names H-1302 and H-1303 in a mirrored-writing / ICIT-correction discussion after CISI comparison. It does not resolve the local packet rows because the inline signs are not available as numeric sign IDs through text extraction. The public image set has possible object-panel candidates but no visible object labels, so it remains acquisition targeting only.

## H-355 Double-Short-Side Clarification Audit

Reference:

[H-355 double-short-side clarification audit](h355_double_short_side_clarification_audit.md)

The only double-short-side case in the 17-artifact packet was checked against its public text lead and fresh public-web searches.

Key results:

```text
packet_object: H-355
catalog_rows: 3
short_rows_to_check: 2
public_text_only_leads: 1
public_object_image_leads: 0
source_validation_fields_filled: 0
status: requires_CISI_HARP_three_side_source
```

Interpretation: H-355 remains a high-priority source request because it is the only packet object with `1:+400-740-176+|2:+700-033+|3:+700-033+`. The checked public layer gives only the Indus Script & More range/list mention `H-352-357 (incised)` and no object-level H-355 image. Both `+700-033+` rows must be checked independently against a three-side source before the duplicate short rows can be treated as physical repetition.

## H-933/H-960 034 Contrast Source Audit

Reference:

[H-933/H-960 034 contrast source audit](h933_h960_034_contrast_source_audit.md)

The two `034` contrast cases in the 17-artifact packet were checked against their public text lead and fresh public-web searches.

Key results:

```text
packet_objects: H-933; H-960
H-933_signature: 1:+034-700+|2:+400-740-176+
H-960_signature: 1:+700-034+|2:+400-740-176+
public_text_only_leads: 2
public_object_image_leads: 0
source_validation_fields_filled: 0
status: requires_CISI_HARP_two_side_source
```

Interpretation: H-933 and H-960 remain the required `034` contrast pair against the `033` after-longer packet rows, but the checked public layer gives only the Indus Script & More range/list mention `H-933, 936, 960, 964, 308, and 312-314 (incised)` and no object-level images. The pair needs a source-grade two-side check before the `034` before-longer contrast can be treated as physical side/order evidence.

## H-1304/H-1344/H-1347 Source-Dark Direct Request Audit

Reference:

[H-1304/H-1344/H-1347 source-dark direct request audit](h1304_h1344_h1347_source_dark_direct_request_audit.md)

The five source-dark `033` after-longer packet objects were checked against the existing no-lead layer and fresh public-web searches.

Key results:

```text
packet_objects: H-1304; H-1344; H-1345; H-1346; H-1347
common_signature: 1:+400-740-176+|2:+700-033+
public_text_only_leads: 0
public_object_image_leads: 0
source_validation_fields_filled: 0
status: requires_CISI_HARP_two_side_source_batch
```

Interpretation: these five objects are not public-lead cases; they are the repeated source-dark control batch for the `033` after-longer relation. Fresh public searches found no object-level image, plate, caption, or useful text-only lead, so the next action is direct CISI/HARP/archive acquisition for both catalog rows of each object. No side relation, sign segmentation, function, value, or reading is accepted.

## Known-Script Scarcity Comparator Acquisition Audit

Reference:

[Known-script scarcity comparator acquisition audit](known_script_scarcity_comparator_acquisition_audit.md)

The current public source state for Coptic SCRIPTORIUM, Linear B Series D, and SumTablets was checked to decide which known deciphered system should become the first artificial-scarcity comparator.

Key results:

```text
first_comparator_to_run: Linear B Series D
linear_b_clean_real_rows: 513
linear_b_augmented_rows_excluded_by_default: 725
linear_b_duplicate_rows_excluded_by_default: 1327
coptic_role: continuity_upper_bound
sumtablets_role: large_administrative_comparator_after_revision_pin
ivc_source_validation_fields_filled: 0
next_experiment: E5.3a Linear B Series D Scarcity Baseline
```

Interpretation: the first known-script comparator should be Linear B Series D because it is small, open, deciphered, administrative, and sequence-based. Coptic is too rich to be the first IVC-like comparator but is exactly the right continuity upper bound for the Egyptian question. SumTablets is the later large administrative comparator, but it needs a pinned dataset revision and hidden transliteration labels. This audit validates no IVC sign, side relation, semantic field, language identity, or translation.

## Linear B Series D Scarcity Baseline

Reference:

[Linear B Series D scarcity baseline](linear_b_series_d_scarcity_baseline.md)

The first known-script scarcity comparator was executed on the Zenodo Linear B Series D `Samples.txt` source.

Key results:

```text
source_md5_verified: true
real_series_d_default_rows: 513
augmented_rows_excluded_by_default: 725
duplicate_rows_excluded_by_default: 1327
gapped_test_rows_detected_not_used: 513
ivc_p95_length_cap_sign_tokens: 8
sign_all_rows: 513
sign_all_bidirectional_top1: 0.470200
sign_all_bidirectional_top5: 0.746458
sign_all_position_slot_null_bidirectional_top1_mean: 0.136725
sign_p95_rows: 299
sign_p95_bidirectional_top1: 0.435897
sign_p95_bidirectional_top5: 0.698006
sign_p95_position_slot_null_bidirectional_top1_mean: 0.141961
gapped_rows: 513
gapped_rows_exactly_one_gap: 513
gapped_sequence_loo_all_bidirectional_top1: 0.294347
gapped_sequence_loo_all_bidirectional_top5: 0.625731
gapped_sequence_loo_p95_bidirectional_top1: 0.294314
gapped_sequence_loo_p95_bidirectional_top5: 0.638796
gapped_sequence_loo_median_rank: 3
ivc_validation_fields_filled: 0
```

Interpretation: under a hidden-reading known-script condition, a simple bidirectional structural method recovers roughly 47.0 percent top-1 masked signs in the full clean Linear B block and 43.6 percent after an IVC-like p95 length cap. The source-provided gapped rows are harsher: after removing every identical original sequence from training, top-1 is about 29.4 percent, top-5 is about 62.6 to 63.9 percent, and median rank is 3. This becomes the first concrete A2 scarcity ceiling. It does not make the current IVC score a translation score, and it validates no IVC sign, side relation, semantic field, language identity, or translation.

## Lipi TAB:I Mixed 400-740-176 Side-Context Audit

Reference:

[Lipi TAB:I mixed 400-740-176 side-context audit](lipi_tab_i_mixed_400_740_176_side_context.md)

The strongest mixed short-long `TAB:I` family was isolated from the validation queue: artifacts where `+400-740-176+` occurs with short `+700-033+` or `+700-034+`.

Key results:

```text
target_artifacts: 26
two_side_long1_short2: 20
two_side_short1_long2: 4
three_side_long1_double_short: 1
three_side_extra_long_text: 1
short_mark_033: 18
short_mark_034: 8
positive_horizontal_measurements: 25
positive_vertical_measurements: 25
positive_thickness_measurements: 0
```

Interpretation: the pair recurrence is real enough to become a priority validation sheet, but not simple enough to treat as unordered co-occurrence. Side order, row count, the `033`/`034` contrast, and the H-355/H-987 edge cases must be validated from images or stronger catalog-side metadata before any functional test.

## Lipi TAB:I Mixed 400-740-176 Dimension Probe

Reference:

[Lipi TAB:I mixed 400-740-176 dimension probe](lipi_tab_i_mixed_400_740_176_dimension_probe.md)

The 26-artifact mixed `TAB:I` sheet was tested for pre-validation associations between short-mark class and side placement or dimensions.

Key results:

```text
target_artifacts: 26
short_mark_033_artifacts: 18
short_mark_034_artifacts: 8
short_mark_predicts_two_side_long1_short2_p: 0.627850
short_mark_predicts_extra_side_case_p: 1.000000
horizontal_mean_difference_p: 0.035523
vertical_mean_difference_p: 0.204885
area_mean_difference_p: 0.306835
aspect_mean_difference_p: 0.041961
bonferroni_lte_005_tests: none
bh_fdr_lte_005_tests: none
canonical_long1_short2_horizontal_p: 0.254366
canonical_long1_short2_aspect_p: 0.239348
```

Interpretation: `+700-033+` versus `+700-034+` has weak raw all-target horizontal and aspect flags in the current T3 planning layer, but no emitted test survives Bonferroni or Benjamini-Hochberg correction, and the canonical long-side-1/short-side-2 subset weakens the same checks. This is not metrological evidence. It is a reason to prioritize source validation and rerun only on image-validated rows.

## H-2218 Through H-2239 Series Validation Sheet

Reference:

[H-2218 through H-2239 series validation sheet](h2218_h2239_series_validation_sheet.md)

The H-2218 through H-2239 tablet series was isolated into a source-anchored validation sheet.

Key results:

```text
expected_series_size: 22
local_rows_found: 22
all_series_ids_present: true
source_figure_count: 22
main_signature_A: 13
side1_side2_swapped_signature: 7
H-2237_variant: 154 instead of 156 on side 3
H-2238_variant: 033 instead of 034 on side 1
plate_check_status: pending for all rows
```

Interpretation: this is the cleanest first image-validation target in E3.2. It binds local rows to HARP object IDs and figure references, but no physical side function, numerical value, metrological reading, sign meaning, or translation is accepted.

## H-2218 Through H-2239 Fig. 4 Mapping

Reference:

[H-2218 through H-2239 Fig. 4 mapping](h2218_h2239_fig4_mapping.md)

The H-2218 through H-2239 local rows were mapped to Meadow and Kenoyer 2000 Fig. 4 item numbers and manufacturing groups.

Key results:

```text
mapped_fig4_items: 22
missing_fig4_items: 0
group_1_local_signatures: A 4; side_swap 2
group_2_local_signatures: A 6; side_swap 3
group_3_local_signatures: A 3; side_swap 2; 154_variant 1; 033_variant 1
```

Interpretation: Meadow and Kenoyer's manufacturing groups do not collapse to the local side-order signature classes. Every manufacturing group contains mixed local signatures or variants. This is a constraint on later functional hypotheses, not evidence for a reading.

## H-2218 Through H-2239 Fig. 4 Visual Availability Audit

Reference:

[H-2218 through H-2239 Fig. 4 visual availability audit](h2218_h2239_fig4_visual_availability_audit.md)

The public Meadow and Kenoyer 2000 Fig. 4 image was inspected as a visual-availability source. The PDF could not be stored locally through the shell because direct download returned `403 Forbidden`; the figure was checked through the web viewer instead.

Key results:

```text
source_rows: 22
expected_fig4_tablet_items: 22
visible_three_side_panel_rows: 22
visible_end_profile_marker_rows: 22
rows_with_object_level_public_image_leads: 1
rows_without_object_level_public_image_leads: 21
object_level_public_image_lead_objects: H-2219
```

Interpretation: public Fig. 4 coverage exists for all 22 tablet items at a coarse level. This supports source coverage, figure-item presence, and plate-request targeting, but it does not support sign segmentation, allography, stroke counts, side orientation, function, meaning, or translation.

## H-2218 Through H-2239 Dimension Side-Order Probe

Reference:

[H-2218 through H-2239 dimension side-order probe](h2218_h2239_dimension_side_order_probe.md)

The H-2218 through H-2239 local signatures were compared against available measurements and Meadow/Kenoyer manufacturing groups.

Key results:

```text
source_rows: 22
canonical_signature_rows: 20
horizontal_mm_rows: 22
vertical_mm_rows: 22
A_vs_side_swap_horizontal_p: 0.506889
A_vs_side_swap_vertical_p: 0.666035
A_vs_side_swap_area_p: 0.959494
A_vs_side_swap_aspect_p: 0.116138
manufacturing_group_horizontal_p: 0.008750
manufacturing_group_area_p: 0.038950
manufacturing_group_aspect_p: 0.039250
```

Interpretation: available measurements track manufacturing groups more clearly than they track the local A versus side-swap split. This blocks a simple size-only explanation of A versus side-swap, but it does not prove physical side function, numerical value, metrological reading, sign meaning, or translation.

## H-2218 Through H-2239 Side-Order Confound Probe

Reference:

[H-2218 through H-2239 side-order confound probe](h2218_h2239_side_order_confound_probe.md)

The H-2218 through H-2239 local A/B side-order split was checked against manufacturing-group concentration and published Fig. 4 sequence-order blockiness.

Key results:

```text
source_rows: 22
canonical_a_b_rows: 20
coarse_signature_counts: A 13; B_side_swap 7; variant 2
canonical_group_distribution_p_ge_observed: 1.000000
canonical_fig4_bb_adjacency_p_ge_observed: 0.683243
canonical_within_group_bb_adjacency_p_ge_observed: 0.641447
canonical_within_group_count_conditioned_bb_adjacency_p_ge_observed: 0.438889
coarse_signature_within_group_blockiness_p_ge_observed: 0.173416
```

Interpretation: the A/B split is not concentrated by manufacturing group, and visible same-label blocks in Fig. 4 are not strong under exact order nulls. This weakens manufacturing-group and publication-order explanations for the current local split, but it does not accept physical side order, side function, numerical value, sign meaning, or translation.

## H-2218 Through H-2239 Side-Role Template Probe

Reference:

[H-2218 through H-2239 side-role template probe](h2218_h2239_side_role_template_probe.md)

The H-2218 through H-2239 local side texts were reduced to three recurrent role families: `+861-003+`, `+700-03x+`, and `+15x-003+`.

Key results:

```text
source_rows: 22
complete_three_role_inventory_rows: 22
side3_role_15x_003_rows: 22
template_861_700_15x_rows: 13
template_700_861_15x_rows: 9
role_700_03x_exact_texts: +700-034+ 21; +700-033+ 1
role_15x_003_exact_texts: +156-003+ 21; +154-003+ 1
rowwise_role_permutation_p_ge_observed: 3.186635545325e-11
```

Interpretation: all 22 rows fit one `+861-003+` side, one `+700-03x+` side, and one `+15x-003+` side. The `+15x-003+` role is always local side 3, while the other two roles swap between local sides 1 and 2. This creates a sharper image-validation target, but it does not accept physical side order, side function, numerical value, sign meaning, or translation.

## H-2218 Through H-2239 Template Recurrence Audit

Reference:

[H-2218 through H-2239 template recurrence audit](h2218_h2239_template_recurrence_audit.md)

The H-series side-role template was searched across the full 397-row multi-side mark validation queue.

Key results:

```text
validation_queue_rows: 397
h_series_rows: 22
non_h_series_rows: 375
strict_complete_h_inventory_rows: 22
strict_complete_h_inventory_non_h_rows: 0
unordered_complete_h_inventory_rows: 22
unordered_complete_h_inventory_non_h_rows: 0
non_h_near_match_rows: 0
```

Interpretation: the complete H-series three-role template occurs only inside H-2218 through H-2239 in the current validation queue. No non-H artifact group has even two of the three H-series role families under strict or unordered checks. This blocks generalizing the H-series template to the broader side-mark queue, while still leaving the H-series itself pending image validation.

## H-2219 Public Image Lead Audit

Reference:

[H-2219 public image lead audit](h2219_public_image_lead_audit.md)

Three public low-resolution image leads labeled `h2219A`, `h2219B`, and `h2219C` were found in an RSS mirror of a blog page.

Key results:

```text
public_image_leads: 3
linked_object: H-2219 / H97-3317 / Meadow and Kenoyer 2000 Fig. 4 no. 10
image_sizes_px: 97x57; 99x49; 98x58
local_side_order: +861-003+; +700-034+; +156-003+
source_tier: T4 image lead only
```

Interpretation: the images are roughly compatible with the local H-2219 three-side order, but they are thumbnail-grade and come from a claim-heavy secondary page. They are useful for source targeting, not for accepting sign segmentation, side orientation, function, meaning, or translation.

## H-2218 Through H-2239 Public Image-Lead Search

Reference:

[H-2218 through H-2239 public image-lead search](h2218_h2239_public_image_lead_search.md)

The H-2219 image-lead search was widened to the full H-2218 through H-2239 tablet series.

Key results:

```text
source_pages_checked: 5
target_objects: 22
target_labels: 66
image_lead_rows: 12
text_only_target_mentions: 5
unique_public_labels_found: h2219A; h2219B; h2219C
unique_cisi_candidates_found: H-2219
missing_cisi_candidates: 21 of 22
```

Interpretation: across the checked public RSS/blog pages, object-level A/B/C image URLs were found only for H-2219. The remaining H-2218 and H-2220 through H-2239 objects still need CISI plates, higher-resolution HARP images, or direct archive access before side order, segmentation, allography, or side orientation can be accepted.

## Mismatch Audit

Reference:

[Mismatch audit](mismatch_audit.md)

Observed mismatch/sensitivity patterns include `000` unknown signs, `P000` unknown graphemes, bracketed fragments, slash compounds, and source-level sign-count policy disagreements.

These are not annoyances. They are the exact places a bogus decipherment can hide. The first structural baseline is therefore gated to the 138 clean rows. The 12 flagged count-matches must be used only for sensitivity checks, and the 29 mismatches require manual collation.

## Next Falsification Target

Target:

```text
S1.2 Overlap Audit
```

Claim to test:

```text
The 138 clean overlap records are safe enough for first-pass direction/order experiments without semantic interpretation.
```

Failure conditions:

- Manual inspection finds systematic sign-count agreement hiding incompatible sign segmentation.
- The count-matched set is biased toward a single artifact type or sign formula.
- Direction metadata disagrees across sources.
- Mismatches cluster around signs or object types central to the structural baseline.

Required next evidence:

- Distribution of clean, sensitivity-flagged, and mismatched records by object type, direction, sign length, and iconography.
- A manual audit of the 29 mismatches.
- Manual image or sign-list validation of the high-frequency crosswalk workset.
- Manual validation of the `817`/`861 -> P385` possible merge/allograph cluster.
- Test whether provisional structural classes survive sensitivity rows, mismatch collation, and larger corpora.
- Known deciphered administrative corpora under Indus-like scarcity.
- Metadata-prediction tests against structured nonlinguistic controls.
- Artifact-class and site-held-out tests against structured nonlinguistic controls.
- Class-prediction controls within artifact type and site.
- Find an external definition for the `class` codes, if one exists in CISI, ICIT, Mahadevan, or another catalog source.
- Remove near-pure length/site/type proxy class labels and rerun class prediction.
- Run proxy-blocked semantic-anchor prediction for `symbol`, `cult`, `material`, `shape`, `type`, and dimension bins.
- Rerun the weakest possible semantic-anchor residues with stricter sign-class blocks, especially `vertical_bin` and `horizontal_bin`.
- Test numerical signs directly against measurements and reverse-side marks rather than broad all-sign dimension bins.
- Validate the artifact-level multi-side short-mark queue, especially H-2218 through H-2239 and the mixed `TAB:I` family `+400-740-176+` paired with `+700-033+` or `+700-034+`.
- Acquire or inspect the first six short-mark source-action artifacts from the source acquisition queue: H-1302, H-1303, H-355, H-933, H-960, and H-233.
- Upgrade `E5.3a Linear B Series D Scarcity Baseline` with a stronger sign-ID tokenization if a citable source can be acquired, then replicate the stricter source-provided gapped test on SumTablets after revision pinning and transliteration-label hiding.
- Repeat metadata prediction on an authoritative or image-validated corpus.
- Known-script scarcity comparators with artificial catalog classes.

## Translation Status

No translation claim is admissible from this result.

Current maximum confidence layer:

```text
Corpus layer: partial open-prototype audit
Graphemic layer: provisional positional crosswalk candidates only
Structural layer: A2 narrow Mayig overlap subset plus T3 broad Lipi scout controls
Semantic layer: target-gate only; no semantic reading admissible
Linguistic layer: not admissible
Translation layer: not admissible
```
