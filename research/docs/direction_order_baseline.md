# Direction And Order Baseline

Date: 2026-05-24

## Purpose

This is the first controlled structural baseline on the open prototype clean subset.

It tests whether the sign strings have recoverable order structure under frequency, position, reversed-order, shuffled-order, and edge-sign controls. It does not test meaning, language, phonetic value, or translation.

## Local Artifacts

```text
data/open_prototype/reports/direction_order_baseline_summary.json
data/open_prototype/reports/direction_order_sequence_scores.csv
data/open_prototype/reports/direction_order_masked_predictions.csv
data/open_prototype/reports/direction_order_masked_summary.csv
```

Source gate:

```text
data/open_prototype/reports/mismatch_audit.csv
status == candidate_for_pre_crosswalk_structure_tests
```

## Corpus Build

Primary clean subset:

```text
rows: 138
tokens: 748
unique_numeric_signs: 191
site: Mohenjo-daro only
artifact_type: SEAL:S only
```

Top signs:

| Sign | Count |
| --- | ---: |
| `740` | 74 |
| `002` | 61 |
| `220` | 29 |
| `390` | 26 |
| `032` | 21 |

This is not a representative IVC corpus. It is a gated first-pass slice.

## Experiment 1: Sequence Order Likelihood

Method:

```text
leave-one-inscription-out add-one-smoothed bigram
score observed order vs reversed order
score observed order vs mean of 100 deterministic shuffles
epsilon_for_win_loss = 1e-9
```

Primary result:

| Condition | Rows longer than 1 | Observed > reversed | Reversed > observed | Ties | Observed > shuffle mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| Clean subset | 137 | 130 | 4 | 3 | 128 |
| Clean subset with `740` and `002` removed | 134 | 114 | 12 | 8 | 116 |
| Count-matched subset including 12 sensitivity rows | 149 | 142 | 4 | 3 | 139 |

Length-bucket result for the clean subset:

| Length bucket | Rows | Observed > reversed | Reversed > observed | Ties | Observed > shuffle mean |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1-3 | 24 | 21 | 2 | 1 | 20 |
| 4-5 | 50 | 47 | 2 | 1 | 46 |
| 6-8 | 55 | 54 | 0 | 1 | 54 |
| 9+ | 8 | 8 | 0 | 0 | 8 |

Edge-sign control:

Removing the two most frequent signs, `740` and `002`, weakens the signal but does not erase it.

```text
mean_actual_minus_reversed: 2.594706
median_actual_minus_reversed: 2.740320
observed_beats_reversed: 114 of 134 rows longer than one sign
observed_beats_shuffle_mean: 116 of 134 rows longer than one sign
```

Interpretation:

The order signal is not only an artifact of the two highest-frequency signs. It is weaker without them, which is expected, but it survives enough to justify stronger structural work.

## Experiment 2: Masked Sign Prediction

Method:

```text
leave-one-inscription-out masked token prediction
models: frequency, absolute-position, length-position, bidirectional-bigram
target: exact numeric sign
```

Overall result:

| Model | Masked tokens | Top-1 | Top-1 accuracy | Top-5 | Top-5 accuracy | MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Frequency | 748 | 74 | 0.098930 | 211 | 0.282086 | 0.195141 |
| Position | 748 | 119 | 0.159091 | 251 | 0.335561 | 0.244396 |
| Length-position | 748 | 113 | 0.151070 | 226 | 0.302139 | 0.232769 |
| Bidirectional bigram | 748 | 212 | 0.283422 | 363 | 0.485294 | 0.377810 |

MRR means mean reciprocal rank: a higher value means the correct sign tends to be ranked closer to the top even when it is not the top prediction.

By position class:

| Model | Position class | Tokens | Top-1 accuracy | Top-5 accuracy | MRR |
| --- | --- | ---: | ---: | ---: | ---: |
| Frequency | Initial | 137 | 0.445255 | 0.547445 | 0.491173 |
| Position | Initial | 137 | 0.445255 | 0.737226 | 0.543950 |
| Bidirectional bigram | Initial | 137 | 0.569343 | 0.744526 | 0.652841 |
| Frequency | Medial | 473 | 0.027484 | 0.281184 | 0.155597 |
| Position | Medial | 473 | 0.116279 | 0.279070 | 0.205945 |
| Bidirectional bigram | Medial | 473 | 0.270613 | 0.463002 | 0.358041 |
| Frequency | Terminal | 137 | 0.000000 | 0.021898 | 0.037023 |
| Position | Terminal | 137 | 0.021898 | 0.131387 | 0.079343 |
| Bidirectional bigram | Terminal | 137 | 0.043796 | 0.306569 | 0.173752 |

Interpretation:

The bidirectional context model beats frequency and position baselines overall. The largest useful gain is in medial positions, where frequency alone is basically blind. Initial signs are partly recoverable by position/frequency because the subset has strong initial-sign concentration. Terminal exact-sign prediction remains weak.

That terminal weakness matters. It says we should not yet pretend the model has a robust terminal grammar at exact-sign level. The next pass should test terminal classes, allograph policies, and larger authoritative corpora.

## Result

The clean subset passes a first structural-order gate:

- Observed order usually scores above reversed and shuffled order.
- The order signal survives removing `740` and `002`.
- Adding the 12 sensitivity-flag count matches does not collapse the order signal.
- Bidirectional context predicts masked signs better than frequency and position baselines.

## Counterresult

The result is narrow:

- All rows are Mohenjo-daro `SEAL:S`.
- The baseline uses `lipi` numeric signs only.
- No primary image validation has been done.
- No `P###` to `+###` sign crosswalk has been established.
- Terminal exact-sign prediction is still poor.
- No nonlinguistic comparator baseline was run for this early subset in this note; later Vector 2 structured comparators show broad predictability can be mimicked by administrative/emblem forgers.

## Interpretation Boundary

This supports an A2 structural claim on the open prototype clean subset:

```text
The gated Mohenjo-daro seal subset contains ordered sign dependencies beyond frequency and simple position baselines.
```

It does not support:

- Meaning.
- Phonetic values.
- Language identity.
- Translation.
- Corpus-wide claims about all IVC inscriptions.

## Next Falsification

The next structural target is to see whether this order signal survives:

- Manual collation of the 29 mismatch rows.
- A high-frequency sign crosswalk sample for `740`, `002`, `220`, `390`, and `032`.
- Removal or downweighting of additional edge signs.
- Allograph merge/split sensitivity.
- Comparison against emblematic and administrative nonlinguistic baselines.
- A scarcity comparator using a deciphered corpus downsampled to Indus-like inscription lengths.
