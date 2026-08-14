# Linear B Series D Scarcity Baseline

Date: 2026-05-24

This note reports the first run of the outside yardstick. Linear B is already deciphered, so we know the right answers. Here the answers are hidden, the tablets are cut down to the short lengths the Indus corpus actually offers, and a plain structural method is asked to guess a missing sign. Whatever it scores is the honest ceiling for the same method on Indus material — a target, not a claim about Indus signs.

## Question

What can a structural method recover from a known deciphered administrative script when the known readings are hidden and the inscription lengths are forced toward the current IVC planning layer?

This is the first execution of `E5.3a Linear B Series D Scarcity Baseline`. It is a known-script comparator — a deciphered script used as a benchmark — not an IVC reading experiment.

## Source Manifest

Source:

- [Zenodo Linear B Series D record](https://zenodo.org/records/7404653)
- DOI: `10.5281/zenodo.7404653`
- Version: `1.0`
- License: `CC-BY 4.0`
- Downloaded file: `Samples.txt`
- Local file: `data/open_prototype/known_scripts/linear_b_series_d/Samples.txt`
- Bytes: `103268`
- MD5: `0c9b9190b86840c82cafdbf4f4b8c827`
- Expected MD5: `0c9b9190b86840c82cafdbf4f4b8c827`
- MD5 verified: `true`

Parsed layout:

```text
physical_lines: 3084
nonempty_lines: 3080
published_sequence_rows: 2565
real_series_d_default_clean: rows 1-513
augmented_excluded_default: rows 514-1238
duplicate_excluded_default: rows 1239-2565
gapped_test_detected_not_used: 513 rows after the blank/header section
```

The clean default uses only rows `1-513`, matching the Zenodo record's real Series D tablet sequence block. Augmented and duplicate rows are excluded unless named as stress conditions.

## Tokenization

Two hidden-reading views were produced.

```text
sign_tokens: primary view. Hyphenated transliteration sequences are split into opaque sign labels, while logograms and composite labels such as OVIS:f stay as one label.
word_tokens: sanity view. Whitespace-delimited tokens are kept whole.
```

The `sign_tokens` view is a scarcity-comparator tokenization. It is not a Linear B philological analysis and does not use known Mycenaean Greek readings as labels.

## IVC-Like Length Cap

The IVC-like cap comes from the current filtered `lipi` numeric-clean planning layer:

```text
ivc_numeric_clean_rows: 2887
ivc_length_mean: 4.037063
ivc_length_median: 4
ivc_length_p95: 8
linear_b_cap_sign_tokens: 8
linear_b_rows_after_cap: 299
```

This makes the comparator harsher than the all-length Linear B block while still preserving enough rows to measure structure.

## Main Results

Primary `sign_tokens` scorecard:

| Scope | Rows | Tokens | Unique Tokens | Exact Sequence Groups | Exact Duplicate Rows | Stored Higher Share | Frequency Top-1 | Position Top-1 | Length-Position Top-1 | Bidirectional Top-1 | Bidirectional Top-5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Real Series D, all lengths | 513 | 4202 | 100 | 490 | 40 | 0.995918 | 0.099170 | 0.127504 | 0.170738 | 0.470200 | 0.746458 |
| Real Series D, IVC p95 length cap | 299 | 1838 | 91 | 278 | 36 | 0.992806 | 0.120228 | 0.144729 | 0.156125 | 0.435897 | 0.698006 |

The all-length hidden-reading condition gives bidirectional masked-sign top-1 accuracy of `0.470200`. The IVC-like length cap lowers it to `0.435897`, still far above frequency, position-only, and length-position baselines.

## Control Results

A null model is a deliberately dumb chance model: it keeps some shallow property of the data, such as sign frequency or position, and throws the rest away. If the real method cannot beat it, the method has found nothing. Each structural control ran 50 deterministic iterations for both tokenizations and both scopes.

Primary `sign_tokens` bidirectional top-1 controls:

| Scope | Observed | Length-Frequency Null Mean | Edge-Frame Null Mean | Position-Slot Null Mean |
| --- | ---: | ---: | ---: | ---: |
| Real Series D, all lengths | 0.470200 | 0.092919 | 0.107864 | 0.136725 |
| Real Series D, IVC p95 length cap | 0.435897 | 0.110094 | 0.128736 | 0.141961 |

The bidirectional context signal remains well above the simple structural nulls.

Stored-order asymmetry is less informative. Edge-frame and position-slot controls nearly reproduce it:

```text
all_lengths_observed_stored_higher_share: 0.995918
all_lengths_edge_frame_null_mean: 0.987161
all_lengths_position_slot_null_mean: 0.989349
ivc_p95_observed_stored_higher_share: 0.992806
ivc_p95_edge_frame_null_mean: 0.977929
ivc_p95_position_slot_null_mean: 0.981705
```

That mirrors the IVC-side warning: stored order alone is a weak diagnostic if edge and slot structure can reproduce most of it.

## Source-Provided Gapped Rows

The same Zenodo file contains a testing section saying the first 513 Series D sequences were reused with synthetic gaps created by randomly removing syllables. The local parser confirms:

```text
gapped_rows: 513
gap_encoding: exact sign token "*"
asterisk_number_signs_preserved: true, e.g. *56 is not treated as a gap
rows_with_exactly_one_gap: 513
rows_with_original_gap_alignment_confirmed: 513
ivc_p95_length_cap_gapped_rows: 299
target_rows_from_exact_duplicate_sequences: 40 all lengths; 36 under p95 cap
```

This is stricter than the leave-one-token score above because the missing position is source-provided and evaluated as a held-out gap. A holdout is data kept out of training so the method must genuinely predict it rather than recall it. Two policies were run:

```text
row_leave_one_out: removes only the target row from training
sequence_leave_one_out: removes every clean-row training sequence identical to the target original sequence
```

Primary `sign_tokens` gapped held-out results:

| Scope | Holdout Policy | Gaps | Frequency Top-1 | Position Top-1 | Length-Position Top-1 | Bidirectional Top-1 | Bidirectional Top-5 | Bidirectional MRR | Median Rank |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| All 513 gapped rows | Row leave-one-out | 513 | 0.027290 | 0.093567 | 0.122807 | 0.300195 | 0.633528 | 0.454565 | 3 |
| All 513 gapped rows | Sequence leave-one-out | 513 | 0.027290 | 0.093567 | 0.116959 | 0.294347 | 0.625731 | 0.448840 | 3 |
| IVC p95 length cap | Row leave-one-out | 299 | 0.033445 | 0.090301 | 0.100334 | 0.304348 | 0.652174 | 0.464666 | 3 |
| IVC p95 length cap | Sequence leave-one-out | 299 | 0.033445 | 0.090301 | 0.090301 | 0.294314 | 0.638796 | 0.454842 | 3 |

The harsher gapped task lowers the structural ceiling from about `43.6%` top-1 under the IVC-like complete-row p95 condition to about `29.4%` top-1 under sequence-leave-one-out. The median rank stays `3`, so the model often puts the true missing sign near the top without reliably landing first.

## Ceiling Statement

Under known-script, hidden-reading, source-verified conditions, a very simple bidirectional structural method recovers about `47.0%` top-1 masked signs in the full clean Linear B Series D block and about `43.6%` top-1 after an IVC-like p95 length cap. This is a scarcity ceiling target for A2 structural recovery, not a translation target.

The source-provided gapped rows give a stricter ceiling: about `29.4%` top-1 after exact duplicate sequence removal in both all-length and IVC-like length-cap scopes. This is probably the better benchmark for future IVC missing-sign work.

For orientation only, the current broad `lipi` duplicate-collapsed T3 planning layer has bidirectional top-1 `0.325865`, and the harsh top-10-edge plus one-edit-family stress condition has `0.224004`. That comparison is not yet like-to-like because the IVC side is not source-validated and the Linear B tokenization is transliteration-derived. It only says what strong structural recovery can look like when a known administrative script is blinded.

## Artifacts

```text
data/open_prototype/tools/linear_b_series_d_scarcity_baseline.mjs
data/open_prototype/known_scripts/linear_b_series_d/Samples.txt
data/open_prototype/reports/linear_b_series_d_source_manifest.json
data/open_prototype/reports/linear_b_series_d_row_inventory.csv
data/open_prototype/reports/linear_b_series_d_length_distribution.csv
data/open_prototype/reports/linear_b_series_d_sequence_summary.csv
data/open_prototype/reports/linear_b_series_d_masked_summary.csv
data/open_prototype/reports/linear_b_series_d_position_entropy.csv
data/open_prototype/reports/linear_b_series_d_control_iterations.csv
data/open_prototype/reports/linear_b_series_d_control_summary.csv
data/open_prototype/reports/linear_b_series_d_scarcity_summary.json
data/open_prototype/reports/linear_b_series_d_gapped_alignment.csv
data/open_prototype/reports/linear_b_series_d_gapped_heldout_predictions.csv
data/open_prototype/reports/linear_b_series_d_gapped_heldout_summary.csv
data/open_prototype/reports/linear_b_series_d_gapped_heldout_summary.json
```

## Next Falsification

- Replace the transliteration-derived `sign_tokens` split with a stronger Linear B sign-ID tokenization if a citable sign-ID source can be acquired.
- Add SumTablets as the next known administrative comparator after pinning a dataset revision and hiding transliteration labels.
- Compare IVC against this ceiling only after source validation and crosswalk work remove the current T3 planning-layer caveats.

## Interpretation Boundary

This result validates no IVC sign, side relation, semantic field, numerical value, metrological reading, phonetic value, language identity, or translation.
