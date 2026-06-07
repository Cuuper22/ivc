# Lipi Synthetic Comparator Baseline

Date: 2026-05-29

## Purpose

This experiment asks whether the broad filtered `lipi` structural results can be reproduced by strong nonlinguistic synthetic controls.

The control systems are intentionally hostile. They preserve the obvious confounds before asking whether the observed `lipi_numeric_clean_candidate` layer still has extra structure:

- Length-frequency shuffle: preserves row lengths and global numeric sign frequencies.
- Edge-position shuffle: preserves row lengths, singleton signs, first-sign pool, last-sign pool, and interior-sign pool.
- Edge-frame template shuffle: preserves each row length plus exact first and last signs; only interiors are shuffled.
- Position-slot shuffle: preserves each row length and every length-position token multiset.

This is a comparator scout, not a decipherment. It does not treat `lipi` as authoritative. It does not assume accepted reading order. It does not assign meanings, sign values, phonetics, language identity, or translations.

## Local Artifacts

```text
data/open_prototype/tools/lipi_synthetic_comparator_baseline.mjs
data/open_prototype/reports/lipi_synthetic_comparator_iterations.csv
data/open_prototype/reports/lipi_synthetic_comparator_summary.csv
data/open_prototype/reports/lipi_synthetic_comparator_summary.json
```

Source file:

```text
data/open_prototype/reports/lipi_scope_rows.csv
```

Scope:

```text
readiness_bucket = lipi_numeric_clean_candidate
source_rows = 2883
source_tokens = 11645
iterations_per_control = 20
seed_base = 20260524
```

The masked-sign evaluation uses exact duplicate collapse before scoring. It reports top-1 and top-5 accuracy for frequency, position, length-position, and bidirectional context.

## Observed Baseline

The observed duplicate-collapsed `lipi_numeric_clean_candidate` layer has:

```text
source_rows: 2883
unique_sequences: 1798
exact_duplicate_rows: 1351
exact_duplicate_row_share: 0.468609
top_sequence_count: 117
collapsed_tokens: 8212
stored_higher_share: 0.948276
frequency_top1: 0.107769
position_top1: 0.151120
length_position_top1: 0.154652
bidirectional_top1: 0.325865
bidirectional_top5: 0.567828
```

## Synthetic Null Results

Means below are over 20 deterministic iterations per control.

| Control | Duplicate Row Share | Top Sequence Count | Stored Win Share | Bidirectional Top-1 | Bidirectional Top-5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| observed `lipi` | 0.468609 | 117 | 0.948276 | 0.325865 | 0.567828 |
| length-frequency shuffle | 0.063857 | 9.5 | 0.494735 | 0.097481 | 0.227814 |
| edge-position shuffle | 0.132830 | 15.45 | 0.936035 | 0.109609 | 0.296928 |
| edge-frame template shuffle | 0.240375 | 117.0 | 0.939348 | 0.126095 | 0.301071 |
| position-slot shuffle | 0.179934 | 48.55 | 0.940100 | 0.144034 | 0.312283 |

The edge-position, edge-frame, and position-slot controls nearly reproduce the stored-order win share. That means stored order by itself is not strong enough to distinguish the `lipi` layer from a rigid nonlinguistic positional system.

The same controls do not reproduce bidirectional masked-sign prediction. The strongest tested null for bidirectional top-1 is the position-slot shuffle at 0.144034, while observed is 0.325865. None of the 80 synthetic iterations across all controls reached the observed bidirectional top-1 or top-5 score.

## Simple Model Comparison

| Control | Frequency Top-1 | Position Top-1 | Length-Position Top-1 | Bidirectional Top-1 |
| --- | ---: | ---: | ---: | ---: |
| observed `lipi` | 0.107769 | 0.151120 | 0.154652 | 0.325865 |
| length-frequency shuffle | 0.101745 | 0.101443 | 0.097227 | 0.097481 |
| edge-position shuffle | 0.097785 | 0.110074 | 0.115842 | 0.109609 |
| edge-frame template shuffle | 0.113770 | 0.127205 | 0.134435 | 0.126095 |
| position-slot shuffle | 0.108443 | 0.146333 | 0.173527 | 0.144034 |

The position-slot null beats the observed layer on length-position top-1. That is the expected warning label: simple positional predictability is not enough. The current residual worth testing is specifically contextual prediction after exact-duplicate collapse, edge removal, formula-family downweighting, and synthetic nonlinguistic controls.

## Interpretation

This comparator tightens the evidence:

- Stored-order asymmetry is heavily explained by edge and position constraints.
- Exact duplicate mass remains higher in the observed layer than in these synthetic controls, except that the edge-frame template preserves a top length-2 sequence count of 117.
- Frequency and simple positional prediction are not diagnostic. A slot-preserving nonlinguistic system can match or exceed simple positional metrics.
- Bidirectional masked-sign prediction remains substantially above these four synthetic controls.

The result supports only this claim:

```text
In the filtered `lipi` numeric-clean planning layer, duplicate-collapsed bidirectional context predicts held-out signs better than four strong synthetic nonlinguistic controls that preserve length, frequency, edge position, edge frames, or length-position slots. Stored-order asymmetry alone is not diagnostic because edge/slot controls nearly reproduce it.
```

It does not support:

- Accepted reading direction.
- Accepted sign segmentation.
- Sign meanings.
- Semantic slots.
- Phonetic values.
- Language identity.
- Translation.

## Limits

- `lipi` remains a T3 planning source.
- The current run uses 20 deterministic iterations per control, enough for the simple-shuffle boundary but not a final benchmark.
- The controls are statistical generators, not archaeologically realistic emblem or administrative systems.
- No image-level validation is present.
- No result here can move a claim into the semantic, linguistic, or translation layer.

## Next Falsification

Follow-up completed:

- [Lipi structured null comparator](lipi_structured_null_comparator.md) added duplicate-calibrated administrative and emblem formula generators.

The next comparator should now be less artificial:

- Run the same metrics on known deciphered administrative corpora under Indus-like downsampling.
- Reproduce this comparator on an authoritative M77/CISI/ICIT or image-validated corpus.
