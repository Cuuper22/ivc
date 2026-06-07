# Structural Readiness Probe

Date: 2026-05-24

## Purpose

This probe asks whether the clean overlap subset is ready for first-pass direction/order experiments.

It does not test meaning. It does not test language. It does not test sign equivalence between `P###` and `+###`. It only tests whether the `lipi` numeric sign strings in the clean subset contain enough ordered structure to justify the next controlled baseline.

## Local Artifacts

```text
data/open_prototype/reports/clean_subset_sequences.csv
data/open_prototype/reports/order_probe_scores.csv
data/open_prototype/reports/structural_readiness_summary.json
```

Source gate:

```text
data/open_prototype/reports/mismatch_audit.csv
status == candidate_for_pre_crosswalk_structure_tests
```

## Dataset

```text
rows: 138
tokens: 748
unique_numeric_signs: 191
distinct_sequences: 138
repeated_sequence_groups: 0
unigram_entropy_bits: 6.399803
normalized_unigram_entropy: 0.844588
```

Important limitation:

```text
site_distribution: Mohenjo-daro = 138
type_distribution: SEAL:S = 138
direction_distribution: R/L = 136, BUS = 1, NR = 1
```

This is a clean subset, not a representative IVC corpus. Any result from this probe is about this gated subset only.

## Length Distribution

| Length | Rows |
| ---: | ---: |
| 5 | 32 |
| 6 | 27 |
| 3 | 18 |
| 4 | 18 |
| 7 | 15 |
| 8 | 13 |
| 2 | 6 |
| 9 | 5 |
| 10 | 2 |
| 1 | 1 |
| 13 | 1 |

The distribution is compatible with the known short-inscription constraint, but this small subset is too narrow to support corpus-wide claims.

## Frequent Signs

Top signs in the clean subset:

| Sign | Count |
| --- | ---: |
| `740` | 74 |
| `002` | 61 |
| `220` | 29 |
| `390` | 26 |
| `032` | 21 |
| `060` | 17 |
| `520` | 15 |
| `235` | 14 |
| `240` | 14 |
| `820` | 14 |

Top initial signs:

| Sign | Count |
| --- | ---: |
| `740` | 61 |
| `520` | 14 |
| `390` | 13 |
| `090` | 8 |
| `156` | 5 |

Top terminal signs:

| Sign | Count |
| --- | ---: |
| `817` | 11 |
| `861` | 10 |
| `820` | 8 |
| `692` | 7 |
| `140` | 5 |

The initial/terminal concentration is exactly why direction/order testing is worth doing. It is also exactly why shuffled baselines are mandatory.

## Held-Out Bigram Probe

Method:

```text
leave-one-out add-one-smoothed bigram over lipi numeric signs,
with start and end tokens,
epsilon_for_win_loss = 1e-9
```

For each row, the model was trained on the other 137 clean rows. The held-out sequence was scored in observed order and reversed order. For rows longer than one sign, the observed sequence was also compared against the mean score of 50 deterministic shuffles.

Result:

```text
scored_rows: 138
directional_rows_length_gt_1: 137
actual_higher_than_reversed: 130
reversed_higher_than_actual: 4
ties: 3
mean_actual_minus_reversed: 5.549892
median_actual_minus_reversed: 5.455321
shuffle_rows_length_gt_1: 137
actual_above_50_shuffle_mean: 129
actual_below_or_equal_50_shuffle_mean: 8
```

## Interpretation

The clean subset contains a strong order signal under this limited check: observed order usually scores higher than reversed order and higher than shuffled-order mean.

That is not a decipherment signal. It is a structural-readiness signal. The result says this subset is worth using for stronger direction/order experiments with explicit null models.

## Reasons Not To Overclaim

- The subset is all Mohenjo-daro `SEAL:S` rows.
- The probe uses `lipi` transcription order, not independently verified image order.
- The sign system is still numeric `+###`, not crosswalked to `mayig` `P###`.
- The model is a simple bigram with add-one smoothing.
- The shuffle check is deterministic and small, not a full null-model suite.
- No external comparator corpus has been run yet.

## Next Experiment

Run `S1.3 Direction/Order Baseline` with:

- Clean 138-row subset as the primary set.
- The 12 sensitivity-flag count matches as a separate inclusion/exclusion set.
- The 29 mismatch rows excluded.
- Reversed-order, shuffled-order, position-only, and frequency-only baselines.
- A held-out split that reports results by length bucket.

The next pass should also test whether the order signal survives after removing very frequent edge signs such as `740` and `002`.

