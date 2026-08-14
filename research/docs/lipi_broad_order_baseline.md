# Lipi Broad Order Baseline

Date: 2026-05-24

This note is a baseline: the first broad measurement of whether sign order in the corpus carries any real structure, run before anyone tries to interpret anything. A baseline is the number every later result has to beat.

Three terms recur below. `lipi` is our filtered planning dataset, rated T3, meaning third-tier: usable for generating ideas, never as authority. A holdout is a slice of data withheld from training and used only for testing, which is how you tell learning from memorizing. A gate is a test a claim must pass before the project builds on it.

## Purpose

This experiment asks whether the structural order signal seen in the Mayig/Mohenjo-daro unicorn-seal subset survives in a broader claim-free `lipi` planning layer.

It does not treat `lipi` as authoritative. It does not assume the `text` column is accepted reading order. It tests stored numeric sign order exactly as present in the filtered metadata.

It does not assign meanings, sign values, phonetics, language identity, or translations.

## Local Artifacts

```text
data/open_prototype/tools/lipi_broad_order_baseline.mjs
data/open_prototype/reports/lipi_broad_order_sequence_summary.csv
data/open_prototype/reports/lipi_broad_order_masked_summary.csv
data/open_prototype/reports/lipi_broad_order_holdout_summary.csv
data/open_prototype/reports/lipi_broad_order_group_inventory.csv
data/open_prototype/reports/lipi_broad_order_summary.json
```

Source file:

```text
data/open_prototype/reports/lipi_scope_rows.csv
```

## Dataset

Primary scope:

```text
scope: lipi_numeric_clean_candidate
rows: 2887
tokens: 11655
unique_signs: 571
minimum_group_rows: 50
```

Sensitivity scope:

```text
scope: lipi_direction_clean_candidate_total
rows: 3308
tokens: 13732
unique_signs: 610
```

The sensitivity scope includes the numeric-clean rows plus direction-clean rows that may contain `000` unknown signs or slash compounds. Masked-sign prediction is reported only for the stricter numeric-clean scope.

## Experiment 1: Stored Order Versus Reversed Order

The simplest possible test of whether order matters: if the signs were in no particular order, running them backwards should score about as well as running them forwards.

Method:

```text
leave-one-inscription-out add-one-smoothed bigram
score stored numeric order against reversed numeric order
```

In plain terms: for each inscription, we train a bigram model on all the other inscriptions and ask whether the stored sign order scores higher than the same signs reversed.

Overall result:

| Scope | Rows | Tokens | Stored > Reversed | Reversed > Stored | Ties | Stored Win Share |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| numeric clean | 2,887 | 11,655 | 2,748 | 131 | 8 | 0.951853 |
| direction-clean total | 3,308 | 13,732 | 3,114 | 162 | 30 | 0.941924 |

By artifact type:

| Type | Rows | Tokens | Stored Win Share | Exact Duplicate Rows | Top Sequence Count |
| --- | ---: | ---: | ---: | ---: | ---: |
| `SEAL:S` | 1,101 | 5,141 | 0.962761 | 133 | 7 |
| `SEAL:R` | 218 | 1,102 | 0.944954 | 10 | 4 |
| `TAB:I` | 533 | 1,444 | 0.951220 | 425 | 64 |
| `TAB:B` | 705 | 2,519 | 0.917730 | 491 | 53 |
| `TAB:C` | 157 | 791 | 0.980892 | 130 | 25 |

By site:

| Site | Rows | Tokens | Stored Win Share | Exact Duplicate Rows | Top Sequence Count |
| --- | ---: | ---: | ---: | ---: | ---: |
| Harappa | 1,430 | 4,871 | 0.930070 | 921 | 117 |
| Mohenjo-daro | 1,217 | 5,743 | 0.972062 | 294 | 25 |
| Lothal | 84 | 401 | 0.857143 | 25 | 11 |
| Kalibangan | 55 | 232 | 0.872727 | 8 | 8 |

## Experiment 2: Within-Split Masked Sign Prediction

Method:

```text
leave-one-inscription-out exact numeric sign prediction
models: frequency, absolute position, length-position, bidirectional context
```

In plain terms: we hide one sign at a time and ask each model to guess it exactly.

Overall result:

| Model | Top-1 Accuracy | Top-5 Accuracy | MRR |
| --- | ---: | ---: | ---: |
| Frequency | 0.106221 | 0.250193 | 0.189133 |
| Position | 0.141399 | 0.350408 | 0.248654 |
| Length-position | 0.191420 | 0.427971 | 0.307160 |
| Bidirectional context | 0.408323 | 0.665980 | 0.526717 |

Selected split results for bidirectional context:

| Split | Rows | Top-1 Accuracy | Top-5 Accuracy | MRR |
| --- | ---: | ---: | ---: | ---: |
| `SEAL:S` | 1,101 | 0.329119 | 0.581599 | 0.447490 |
| `SEAL:R` | 218 | 0.289474 | 0.543557 | 0.407504 |
| `TAB:I` | 533 | 0.504848 | 0.750693 | 0.616808 |
| `TAB:B` | 705 | 0.541088 | 0.747916 | 0.636244 |
| `TAB:C` | 157 | 0.771176 | 0.903919 | 0.828550 |
| Harappa | 1,430 | 0.452884 | 0.700267 | 0.568665 |
| Mohenjo-daro | 1,217 | 0.394045 | 0.621800 | 0.502913 |

The very high `TAB:C` within-split result is not a translation signal. `TAB:C` has 130 exact duplicate rows out of 157 rows, with a top sequence count of 25. That makes it a formula/duplication warning: a model can score well simply by having seen near-identical rows already.

The exact-duplicate collapse follow-up is recorded here:

[Lipi deduplicated order baseline](lipi_dedup_order_baseline.md)

The exact train/test sequence leakage follow-up is recorded here:

[Lipi leakage-controlled held-out baseline](lipi_leakage_control_baseline.md)

The high-frequency edge-removal follow-up is recorded here:

[Lipi high-frequency edge removal baseline](lipi_edge_removed_baseline.md)

The formula-family downweighting follow-up is recorded here:

[Lipi formula-family downweighting baseline](lipi_family_downweight_baseline.md)

## Experiment 3: Held-Out Type And Site Prediction

The hard version. Train on everything except one artifact type or one site, then predict inside the group the model has never seen. OOV share, below, is the fraction of test signs that never appeared in training at all — signs the model had no chance to learn.

Method:

```text
train on all numeric-clean rows outside a held-out type/site/region
predict exact numeric signs inside the held-out group
```

Selected held-out results for bidirectional context:

| Held-Out Split | Train Rows | Test Rows | OOV Share | Top-1 Accuracy | Top-5 Accuracy | MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| type `SEAL:S` | 1,786 | 1,101 | 0.059327 | 0.270181 | 0.499125 | 0.378844 |
| type `SEAL:R` | 2,669 | 218 | 0.027223 | 0.297641 | 0.534483 | 0.407773 |
| type `TAB:I` | 2,354 | 533 | 0.038781 | 0.398199 | 0.702909 | 0.532301 |
| type `TAB:B` | 2,182 | 705 | 0.020246 | 0.340611 | 0.614133 | 0.471291 |
| type `TAB:C` | 2,730 | 157 | 0.018963 | 0.279393 | 0.485461 | 0.377112 |
| site Harappa | 1,457 | 1,430 | 0.042702 | 0.237734 | 0.473619 | 0.351092 |
| site Mohenjo-daro | 1,670 | 1,217 | 0.049103 | 0.265018 | 0.502002 | 0.377189 |
| site Lothal | 2,803 | 84 | 0.007481 | 0.309227 | 0.518703 | 0.416491 |
| site Kalibangan | 2,832 | 55 | 0.047414 | 0.215517 | 0.448276 | 0.328516 |

Held-out bidirectional context remains above frequency, position, and length-position baselines in every reported type and site split, but it is much weaker than within-split scoring. This is the important constraint.

## Interpretation

A scout is an exploratory run meant to find where to look, not to settle anything. The broad `lipi` scout supports a real A2-style structural lead:

- Stored numeric order usually scores above reversed order across the broader filtered layer.
- Bidirectional context predicts masked signs better than frequency, position, and length-position baselines.
- The signal is visible across several artifact types and sites.
- Held-out type/site prediction remains above simpler baselines, so the result is not only same-split memorization.

But the counterresult is just as important:

- `lipi` is still a T3 source.
- Stored order is not yet accepted reading order.
- Exact duplicate rows are common: 1,355 duplicate rows out of 2,887 numeric-clean rows.
- Formula-heavy tablet classes inflate within-split masked prediction.
- Held-out performance drops sharply, especially for `SEAL:S`, Harappa, and Mohenjo-daro.
- This is still exact numeric sign prediction, not a semantic parse.

## Result

This probe supports only this claim:

```text
The filtered `lipi` numeric-clean layer contains broad stored-order dependencies that survive artifact-type and site held-out tests at the exact-sign structural level, but duplicate/formula-heavy rows inflate within-split scores and no semantic or translation claim follows.
```

It does not support:

- Accepted reading direction.
- Accepted sign segmentation.
- Sign meanings.
- Semantic slots.
- Phonetic values.
- Language identity.
- Translation.

## Next Falsification

Falsification means the next tests are chosen for their power to break this result, not to confirm it.

The next tests should ask:

- Do the same broad patterns appear in M77/CISI/ICIT or primary-image validated corpora?
- Can nonlinguistic administrative and emblematic baselines produce the same stored-order and held-out masked-sign profile?
