# Formula Variant Null Model

Date: 2026-05-24

## Purpose

This note records a null model built to attack our own formula-variant queue. A null model is a scrambled version of the data that keeps some properties and destroys the pattern under test; running it many times shows how often the pattern would appear by chance alone. If the real corpus does not beat its own scrambles, the pattern was never there.

The formula-variant queue is the review list produced by an earlier probe: near-duplicate inscriptions, shared edge frames, and rows differing in a single slot. This experiment tests whether that queue is stronger than simple corpus structure.

It does not assign sign readings, meanings, phonetics, or translations. It asks a narrower question: do near-duplicate pairs, shared edge frames, and single-slot candidates remain unusual after preserving basic properties of the 136-row strict Mayig-policy subset? Mayig policy is one of our rules for deciding which sign shapes count as the same sign.

## Local Artifacts

```text
data/open_prototype/tools/formula_variant_null_model.mjs
data/open_prototype/reports/formula_variant_null_iterations.csv
data/open_prototype/reports/formula_variant_null_summary.csv
data/open_prototype/reports/formula_variant_null_summary.json
```

Source file:

```text
data/open_prototype/reports/formula_pattern_sequences.csv
```

Dataset:

```text
policy: mayig_observed_parpola
strict_records: 136
scope: Mohenjo-daro unicorn seal rows
iterations_per_null_model: 500
seed: 20260524
```

## Null Models

### Length/Frequency Shuffle

This model preserves:

- Observed inscription lengths.
- Global sign-token frequency.

It does not preserve first-sign or last-sign positions.

### Edge-Position Preserving Shuffle

This model preserves:

- Observed inscription lengths.
- The multiset of first signs.
- The multiset of last signs.
- The multiset of interior tokens.

This is the tougher control for edge-frame results such as `P324...P385`. An edge frame is a pairing of a first sign with a last sign, with anything in between.

## Key Results

`empirical_p_ge` means the smoothed share of null runs that matched or exceeded the observed value.

| Metric | Observed | Length/Frequency Mean | Length/Frequency p95 | Length/Frequency p_ge | Edge-Preserving Mean | Edge-Preserving p95 | Edge-Preserving p_ge |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| variant pairs total | 129 | 47.044 | 63 | 0.001996 | 159.806 | 203 | 0.902196 |
| near pairs, edit distance <= 2 | 75 | 41.142 | 55.05 | 0.001996 | 98.324 | 136 | 0.894212 |
| shared edge-frame pairs | 69 | 6.614 | 12 | 0.001996 | 69.620 | 102 | 0.467066 |
| frame families | 14 | 4.876 | 8 | 0.001996 | 12.458 | 16 | 0.313373 |
| top frame rows | 10 | 2.632 | 4 | 0.001996 | 9.612 | 13 | 0.514970 |
| single-substitution pairs | 5 | 1.124 | 3 | 0.015968 | 5.770 | 11 | 0.620758 |
| slot candidate groups | 3 | 1.000 | 3 | 0.061876 | 3.060 | 5 | 0.630739 |
| exact duplicate sequence groups | 1 | 0.012 | 0 | 0.013972 | 0.172 | 1 | 0.163673 |

## Interpretation

The formula-variant signal is strong under the loose length/frequency shuffle, but it mostly disappears under the edge-position preserving shuffle.

That matters. It means many apparent formula-variant counts are explainable by stable first-sign and last-sign behavior alone. The `P324...P385` frame with 10 rows is striking under a loose null, but ordinary once the first/last position distributions are preserved: edge-preserving mean 9.612, median 10, p95 13.

The exact duplicate candidate `M-32/M-177` remains worth manual source/image validation, but the null model does not make it a semantic result. It is an audit target.

## Result

This null model supports only this claim:

```text
The strict Mayig-policy subset has stable edge-position structure that explains much of the formula-variant queue; the queue remains useful for manual duplicate and formula review, but it is not independent semantic evidence.
```

It does not support:

- Accepted duplicate interpretation.
- Accepted allograph or sign-equivalence claims.
- Semantic slots.
- Phonetic values.
- Translation.

## Consequence

Downgrade the formula-variant queue from "possible formula signal" to "edge-conditioned review queue" until it passes at least one harder test:

- Image/source validation of `M-32/M-177`.
- Broader corpus replication outside Mohenjo-daro unicorn seals.
- Artifact metadata prediction not used to construct the queue.
- Edge-preserving null models split by length and description series.
