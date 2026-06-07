# Lipi Deduplicated Order Baseline

Date: 2026-05-24

## Purpose

This experiment tests whether the broad `lipi` stored-order and masked-sign signal survives exact duplicate collapse.

It follows the [Lipi broad order baseline](lipi_broad_order_baseline.md), but within every evaluated scope or split, exact duplicate numeric sign sequences are collapsed to one representative row.

It does not treat `lipi` as authoritative. It does not assume accepted reading order. It does not assign meanings, sign values, phonetics, language identity, or translations.

## Local Artifacts

```text
data/open_prototype/tools/lipi_broad_order_baseline.mjs
data/open_prototype/reports/lipi_dedup_order_sequence_summary.csv
data/open_prototype/reports/lipi_dedup_order_masked_summary.csv
data/open_prototype/reports/lipi_dedup_order_holdout_summary.csv
data/open_prototype/reports/lipi_dedup_order_group_inventory.csv
data/open_prototype/reports/lipi_dedup_order_summary.json
data/open_prototype/reports/lipi_leakage_control_holdout_summary.csv
data/open_prototype/reports/lipi_leakage_control_summary.json
```

Source file:

```text
data/open_prototype/reports/lipi_scope_rows.csv
```

Parent baseline:

```text
data/open_prototype/reports/lipi_broad_order_summary.json
```

## Collapse Policy

Exact duplicate numeric sign sequences are collapsed inside each evaluated scope or split.

This means:

- The all-corpus numeric-clean scope collapses globally.
- Type, site, and region splits collapse duplicates inside that split.
- Held-out tests collapse duplicate sequences separately in the held-out test group and the outside-training group.

Cross-split exact-sequence overlap is still reported, not removed.

## Main Comparison

| Metric | Duplicate-Weighted | Exact-Duplicate Collapsed |
| --- | ---: | ---: |
| source rows | 2,887 | 2,887 |
| evaluated rows | 2,887 | 1,798 |
| duplicate rows removed | 0 | 1,089 |
| tokens | 11,655 | 8,212 |
| unique signs | 571 | 571 |
| stored > reversed | 2,748 | 1,705 |
| reversed > stored | 131 | 84 |
| stored win share | 0.951853 | 0.948276 |
| bidirectional top-1 | 0.408323 | 0.325865 |
| bidirectional top-5 | 0.665980 | 0.567828 |
| bidirectional MRR | 0.526717 | 0.438744 |
| frequency top-1 | 0.106221 | 0.107769 |
| position top-1 | 0.141399 | 0.151120 |
| length-position top-1 | 0.191420 | 0.154652 |

Stored order barely changes after exact duplicate collapse. Exact-sign prediction drops hard, especially for the bidirectional model.

## By Artifact Type

| Type | Source Rows | Collapsed Rows | Removed | Stored Win Share | Bidirectional Top-1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| `SEAL:S` | 1,101 | 1,018 | 83 | 0.960707 | 0.333740 |
| `SEAL:R` | 218 | 212 | 6 | 0.943396 | 0.282949 |
| `TAB:I` | 533 | 173 | 360 | 0.867052 | 0.275492 |
| `TAB:B` | 705 | 312 | 393 | 0.929487 | 0.325639 |
| `TAB:C` | 157 | 53 | 104 | 0.924528 | 0.388889 |

The tablet classes lose the most rows. That confirms the previous warning: their within-split scores were heavily formula/duplicate-assisted.

## By Site

| Site | Source Rows | Collapsed Rows | Removed | Stored Win Share | Bidirectional Top-1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Harappa | 1,430 | 662 | 768 | 0.919940 | 0.307405 |
| Mohenjo-daro | 1,217 | 1,009 | 208 | 0.962339 | 0.322561 |
| Lothal | 84 | 63 | 21 | 0.809524 | 0.161290 |
| Kalibangan | 55 | 48 | 7 | 0.833333 | 0.142105 |

Harappa loses more than half its rows under exact duplicate collapse. Mohenjo-daro is much less duplicate-heavy in this filtered layer.

## Held-Out Results After Collapse

Selected bidirectional context results:

| Held-Out Split | Test Rows | Seen-In-Train Share | OOV Share | Top-1 Accuracy | Top-5 Accuracy | MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| type `SEAL:S` | 1,018 | 0.049116 | 0.061179 | 0.291057 | 0.521138 | 0.398487 |
| type `TAB:I` | 173 | 0.225434 | 0.053667 | 0.296959 | 0.525939 | 0.405583 |
| type `TAB:B` | 312 | 0.147436 | 0.025556 | 0.314097 | 0.535862 | 0.418524 |
| type `TAB:C` | 53 | 0.056604 | 0.027778 | 0.317460 | 0.551587 | 0.426328 |
| site Harappa | 662 | 0.080060 | 0.044129 | 0.276365 | 0.525056 | 0.392356 |
| site Mohenjo-daro | 1,009 | 0.057483 | 0.055226 | 0.307220 | 0.535283 | 0.413456 |
| site Lothal | 63 | 0.142857 | 0.010753 | 0.301075 | 0.534050 | 0.415476 |
| site Kalibangan | 48 | 0.270833 | 0.021053 | 0.294737 | 0.510526 | 0.400355 |

Held-out scores remain above the simple baselines, but cross-split exact-sequence overlap is not zero. Kalibangan has especially high seen-in-train sequence overlap because the split is small.

The leakage-control follow-up is recorded here:

[Lipi leakage-controlled held-out baseline](lipi_leakage_control_baseline.md)

In that follow-up, every exact numeric sign sequence that appears in the held-out test group is removed from training. The selected bidirectional top-1 scores drop only slightly: `SEAL:S` from 0.291057 to 0.283740, `TAB:B` from 0.314097 to 0.305853, Harappa from 0.276365 to 0.271129, and Mohenjo-daro from 0.307220 to 0.297402. The `test_sequence_seen_share` is 0 for all reported rows.

The high-frequency edge-removal follow-up is recorded here:

[Lipi high-frequency edge removal baseline](lipi_edge_removed_baseline.md)

In that follow-up, removing the top 10 edge signs lowers duplicate-collapsed bidirectional top-1 from 0.325865 to 0.222222, while still leaving it above frequency, position, and length-position baselines.

The formula-family downweighting follow-up is recorded here:

[Lipi formula-family downweighting baseline](lipi_family_downweight_baseline.md)

In that follow-up, edge-frame collapse lowers duplicate-collapsed bidirectional top-1 to 0.286578, while top-10 edge removal plus one-edit-family collapse leaves bidirectional top-1 at 0.224004 versus 0.070659 for frequency.

## Interpretation

The duplicate collapse separates two signals:

- Stored-order structure survives exact duplicate collapse.
- Within-split exact-sign prediction was meaningfully inflated by duplicate/formula-heavy rows.
- Held-out type/site prediction remains above simple baselines after collapse, which argues against pure duplicate memorization.
- The leakage-control follow-up shows exact train/test sequence overlap is not enough to explain the selected held-out scores.
- The edge-removal follow-up shows high-frequency edge effects are a major driver but not the whole signal.
- The formula-family follow-up shows shared edge frames and one-edit neighborhoods are not enough to erase the residual signal, though the largest one-edit families are too broad to treat as natural epigraphic clusters without manual review.

## Result

This probe supports only this claim:

```text
The broad filtered `lipi` structural signal survives exact duplicate collapse at the stored-order level and remains visible in held-out exact-sign prediction, but within-split masked prediction is substantially weakened and must be treated as duplicate/formula-sensitive.
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

The next tests should ask:

- Can a strong nonlinguistic administrative or emblematic baseline reproduce this profile?
- Does an authoritative corpus reproduce the same duplicate-collapsed behavior?
