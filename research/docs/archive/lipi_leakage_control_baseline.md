# Lipi Leakage-Controlled Held-Out Baseline

Date: 2026-05-24

## Purpose

This note records a stress test on `lipi`, the project's filtered working corpus of Indus sign sequences. Earlier baselines predicted signs in a held-out split — a group of rows, such as one artifact type or one site, kept out of training and used only for testing. The worry is leakage: if the same exact sequence appears on both sides of that boundary, the model can score well by memorizing rather than by learning structure. This experiment asks whether the duplicate-collapsed broad `lipi` held-out signal survives when exact sequence leakage is removed across the train/test boundary.

It follows the [Lipi deduplicated order baseline](lipi_dedup_order_baseline.md). For each held-out artifact type, site, or region, exact duplicate numeric sign sequences are collapsed, then any training row whose exact numeric sign sequence appears in the held-out test split is removed from training.

It does not treat `lipi` as authoritative. It does not assume accepted reading order. It does not assign meanings, sign values, phonetics, language identity, or translations.

## Local Artifacts

```text
data/open_prototype/tools/lipi_broad_order_baseline.mjs
data/open_prototype/reports/lipi_leakage_control_holdout_summary.csv
data/open_prototype/reports/lipi_leakage_control_summary.json
```

Source file:

```text
data/open_prototype/reports/lipi_scope_rows.csv
```

Parent baseline:

```text
data/open_prototype/reports/lipi_dedup_order_summary.json
```

## Leakage Policy

For each held-out split:

1. Collapse exact duplicate numeric sign sequences inside the held-out test group.
2. Collapse exact duplicate numeric sign sequences inside the outside-training group.
3. Remove from training every exact numeric sign sequence that appears in the held-out test group.
4. Train frequency, position, length-position, and bidirectional-bigram predictors on the remaining outside rows.
5. Predict exact numeric signs in the held-out group.

The resulting `test_sequence_seen_share` is `0` for every reported row.

## Selected Type Results

Bidirectional context results:

| Held-Out Type | Train Rows Before Filter | Train Rows After Filter | Test Rows | Removed Train Sequences | OOV Share | Top-1 | Top-5 | MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `SEAL:S` | 830 | 780 | 1,018 | 50 | 0.061179 | 0.283740 | 0.509350 | 0.391672 |
| `SEAL:R` | 1,606 | 1,586 | 212 | 20 | 0.027650 | 0.289401 | 0.534562 | 0.400654 |
| `TAB:I` | 1,664 | 1,625 | 173 | 39 | 0.053667 | 0.271914 | 0.504472 | 0.383626 |
| `TAB:B` | 1,532 | 1,486 | 312 | 46 | 0.030503 | 0.305853 | 0.520198 | 0.409262 |
| `TAB:C` | 1,748 | 1,745 | 53 | 3 | 0.027778 | 0.313492 | 0.543651 | 0.422939 |

Comparison against simple baselines:

| Held-Out Type | Frequency Top-1 | Position Top-1 | Length-Position Top-1 | Bidirectional Top-1 |
| --- | ---: | ---: | ---: | ---: |
| `SEAL:S` | 0.103455 | 0.150813 | 0.147358 | 0.283740 |
| `TAB:I` | 0.139535 | 0.137746 | 0.143113 | 0.271914 |
| `TAB:B` | 0.131080 | 0.144270 | 0.151690 | 0.305853 |

## Selected Site Results

Bidirectional context results:

| Held-Out Site | Train Rows Before Filter | Train Rows After Filter | Test Rows | Removed Train Sequences | OOV Share | Top-1 | Top-5 | MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Harappa | 1,189 | 1,136 | 662 | 53 | 0.044129 | 0.271129 | 0.516081 | 0.386529 |
| Mohenjo-daro | 847 | 789 | 1,009 | 58 | 0.056044 | 0.297402 | 0.526693 | 0.404760 |
| Lothal | 1,744 | 1,735 | 63 | 9 | 0.010753 | 0.301075 | 0.537634 | 0.412190 |
| Kalibangan | 1,763 | 1,750 | 48 | 13 | 0.021053 | 0.289474 | 0.505263 | 0.392634 |

Comparison against simple baselines:

| Held-Out Site | Frequency Top-1 | Position Top-1 | Length-Position Top-1 | Bidirectional Top-1 |
| --- | ---: | ---: | ---: | ---: |
| Harappa | 0.117427 | 0.140613 | 0.149215 | 0.271129 |
| Mohenjo-daro | 0.105339 | 0.150747 | 0.147678 | 0.297402 |
| Lothal | 0.086022 | 0.143369 | 0.157706 | 0.301075 |
| Kalibangan | 0.110526 | 0.173684 | 0.168421 | 0.289474 |

## Comparison To Deduplicated Held-Out Baseline

| Held-Out Split | Dedup Top-1 | Leakage-Controlled Top-1 | Change |
| --- | ---: | ---: | ---: |
| type `SEAL:S` | 0.291057 | 0.283740 | -0.007317 |
| type `TAB:I` | 0.296959 | 0.271914 | -0.025045 |
| type `TAB:B` | 0.314097 | 0.305853 | -0.008244 |
| type `TAB:C` | 0.317460 | 0.313492 | -0.003968 |
| site Harappa | 0.276365 | 0.271129 | -0.005236 |
| site Mohenjo-daro | 0.307220 | 0.297402 | -0.009818 |
| site Lothal | 0.301075 | 0.301075 | 0.000000 |
| site Kalibangan | 0.294737 | 0.289474 | -0.005263 |

The strongest drop in this selected set is `TAB:I`, which is also a heavily duplicate-collapsed tablet class. The larger pattern is still clear: removing exact train/test sequence overlap weakens the held-out signal, but it does not erase it.

## Interpretation

This control narrows the leakage explanation:

- Exact cross-split sequence overlap is not the main reason the held-out bidirectional scores beat frequency, position, and length-position baselines.
- Duplicate and formula effects are still real, especially in tablet classes, because exact duplicate collapse already lowered within-split prediction substantially.
- The result remains source-tier limited: `lipi` is a filtered T3 planning layer — the project's tier label for an unverified working corpus, useful for direction but never admissible as proof — not an authoritative corpus.
- The experiment predicts exact stored numeric signs, not sign meanings or linguistic readings.

## Result

This probe supports only this claim:

```text
After exact duplicate collapse and removal of exact train/test sequence overlap, the broad filtered `lipi` held-out structural signal remains above simple baselines across selected artifact type, site, and region splits, though the result remains T3 structural scout evidence and exact-sign prediction is still formula-sensitive.
```

It does not support:

- Accepted reading direction.
- Accepted sign segmentation.
- Sign meanings.
- Semantic slots.
- Phonetic values.
- Language identity.
- Translation.

## Edge-Removal Follow-Up

The high-frequency edge-sign follow-up is recorded here:

[Lipi high-frequency edge removal baseline](lipi_edge_removed_baseline.md)

After removing the top 10 edge signs from every sequence, dropping empty rows, collapsing exact duplicate resulting sequences, and applying the same held-out leakage control, selected bidirectional scores still remain above simple baselines. The signal is much weaker, which means edge signs are a major driver and must be controlled in future broad tests.

The formula-family downweighting follow-up is recorded here:

[Lipi formula-family downweighting baseline](lipi_family_downweight_baseline.md)

That follow-up keeps selected held-out scores above simple baselines after edge-frame and one-edit-family downweighting, including when combined with top-10 edge removal.

## Next Falsification

The next tests should ask:

- Does an authoritative M77/CISI/ICIT corpus (Mahadevan 1977, the Corpus of Indus Seals and Inscriptions, or the Interactive Corpus of Indus Texts) or an image-validated corpus reproduce the same profile?
- Can nonlinguistic administrative and emblematic controls (comparison systems that carry structure without language) produce the same stored-order and held-out masked-sign profile?
