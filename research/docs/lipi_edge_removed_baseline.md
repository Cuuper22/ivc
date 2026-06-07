# Lipi High-Frequency Edge Removal Baseline

Date: 2026-05-24

## Purpose

This experiment asks whether the broad filtered `lipi` structural signal is mostly an artifact of high-frequency initial and terminal signs.

It follows the [Lipi deduplicated order baseline](lipi_dedup_order_baseline.md) and the [Lipi leakage-controlled held-out baseline](lipi_leakage_control_baseline.md). It ranks signs by edge count, removes the top edge signs from every strict numeric-clean sequence, drops empty rows, collapses exact duplicate resulting sequences, and reruns stored-order, masked-sign, and leakage-controlled held-out checks.

This is an artificial stress test. It does not propose removing these signs from the corpus. It asks whether the remaining interior and non-top-edge structure still carries signal.

It does not treat `lipi` as authoritative. It does not assume accepted reading order. It does not assign meanings, sign values, phonetics, language identity, or translations.

## Local Artifacts

```text
data/open_prototype/tools/lipi_edge_removed_baseline.mjs
data/open_prototype/reports/lipi_edge_sign_inventory.csv
data/open_prototype/reports/lipi_edge_removed_sequence_summary.csv
data/open_prototype/reports/lipi_edge_removed_masked_summary.csv
data/open_prototype/reports/lipi_edge_removed_holdout_summary.csv
data/open_prototype/reports/lipi_edge_removed_summary.json
```

Source file:

```text
data/open_prototype/reports/lipi_scope_rows.csv
```

Parent baselines:

```text
data/open_prototype/reports/lipi_dedup_order_summary.json
data/open_prototype/reports/lipi_leakage_control_summary.json
```

## Edge-Sign Inventory

Edge count is initial count plus terminal count in strict numeric-clean `lipi` rows.

| Rank | Sign | Total Count | Initial Count | Terminal Count | Edge Count | Edge Share |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `740` | 1,238 | 858 | 3 | 861 | 0.695477 |
| 2 | `700` | 434 | 347 | 66 | 413 | 0.951613 |
| 3 | `400` | 346 | 317 | 0 | 317 | 0.916185 |
| 4 | `520` | 229 | 194 | 1 | 195 | 0.851528 |
| 5 | `033` | 330 | 33 | 149 | 182 | 0.551515 |
| 6 | `032` | 357 | 32 | 137 | 169 | 0.473389 |
| 7 | `861` | 190 | 35 | 111 | 146 | 0.768421 |
| 8 | `817` | 152 | 1 | 139 | 140 | 0.921053 |
| 9 | `820` | 147 | 11 | 114 | 125 | 0.850340 |
| 10 | `034` | 125 | 14 | 107 | 121 | 0.968000 |

Removal policies:

```text
remove_top_2_edge_signs: 740, 700
remove_top_5_edge_signs: 740, 700, 400, 520, 033
remove_top_10_edge_signs: 740, 700, 400, 520, 033, 032, 861, 817, 820, 034
```

## Stored Order After Edge Removal

Exact duplicate sequences are collapsed after edge signs are removed.

| Policy | Evaluated Rows | Tokens | Unique Signs | Rows > 1 | Stored > Reversed | Reversed > Stored | Ties | Stored Win Share | Median Diff |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| none | 1,798 | 8,212 | 571 | 1,798 | 1,705 | 84 | 9 | 0.948276 | 9.200559 |
| top 2 removed | 1,783 | 7,239 | 569 | 1,717 | 1,588 | 116 | 13 | 0.924869 | 5.989489 |
| top 5 removed | 1,720 | 6,636 | 566 | 1,614 | 1,457 | 143 | 14 | 0.902726 | 4.616906 |
| top 10 removed | 1,658 | 5,913 | 561 | 1,530 | 1,383 | 129 | 18 | 0.903922 | 3.912352 |

The stored-order signal weakens substantially, but it does not disappear even after removing the top 10 edge signs.

## Masked Sign Prediction After Edge Removal

Exact duplicate sequences are collapsed after edge signs are removed.

| Policy | Model | Masked Tokens | Top-1 | Top-5 | MRR |
| --- | --- | ---: | ---: | ---: | ---: |
| none | frequency | 8,212 | 0.107769 | 0.239284 | 0.187476 |
| none | position | 8,212 | 0.151120 | 0.321603 | 0.238405 |
| none | length-position | 8,212 | 0.154652 | 0.357404 | 0.253918 |
| none | bidirectional | 8,212 | 0.325865 | 0.567828 | 0.438744 |
| top 2 removed | frequency | 7,239 | 0.062716 | 0.172261 | 0.133154 |
| top 2 removed | position | 7,239 | 0.089930 | 0.256389 | 0.177496 |
| top 2 removed | length-position | 7,239 | 0.114242 | 0.285675 | 0.204736 |
| top 2 removed | bidirectional | 7,239 | 0.278077 | 0.508772 | 0.386566 |
| top 5 removed | frequency | 6,636 | 0.068113 | 0.156872 | 0.137695 |
| top 5 removed | position | 6,636 | 0.082881 | 0.233122 | 0.167666 |
| top 5 removed | length-position | 6,636 | 0.093279 | 0.279536 | 0.185871 |
| top 5 removed | bidirectional | 6,636 | 0.249849 | 0.482520 | 0.358006 |
| top 10 removed | frequency | 5,913 | 0.072383 | 0.181803 | 0.141158 |
| top 10 removed | position | 5,913 | 0.088449 | 0.229325 | 0.171833 |
| top 10 removed | length-position | 5,913 | 0.092508 | 0.232877 | 0.174078 |
| top 10 removed | bidirectional | 5,913 | 0.222222 | 0.440724 | 0.325997 |

The bidirectional model loses about a third of its duplicate-collapsed top-1 accuracy under top-10 edge removal, from 0.325865 to 0.222222. It still remains above frequency, position, and length-position baselines.

## Leakage-Controlled Held-Out Results

These rows use exact duplicate collapse after edge removal and remove from training every exact resulting sequence that appears in the held-out test split.

Selected top-10 edge-removal results:

| Held-Out Split | Test Rows | OOV Share | Frequency Top-1 | Position Top-1 | Length-Position Top-1 | Bidirectional Top-1 | Bidirectional Top-5 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| type `SEAL:S` | 984 | 0.081682 | 0.089824 | 0.087924 | 0.079512 | 0.180733 | 0.364450 |
| type `SEAL:R` | 207 | 0.035672 | 0.057075 | 0.061831 | 0.068966 | 0.200951 | 0.423306 |
| type `TAB:I` | 153 | 0.084592 | 0.009063 | 0.045317 | 0.024169 | 0.099698 | 0.293051 |
| type `TAB:B` | 282 | 0.051813 | 0.042746 | 0.071244 | 0.075130 | 0.177461 | 0.358808 |
| site Harappa | 588 | 0.065841 | 0.053461 | 0.066967 | 0.077096 | 0.176140 | 0.370850 |
| site Mohenjo-daro | 978 | 0.074326 | 0.078410 | 0.090389 | 0.090662 | 0.199020 | 0.388511 |
| site Lothal | 61 | 0.013575 | 0.090498 | 0.099548 | 0.113122 | 0.244344 | 0.434389 |
| site Kalibangan | 45 | 0.028777 | 0.100719 | 0.107914 | 0.122302 | 0.230216 | 0.402878 |

The held-out signal also weakens but remains above the simple baselines in these selected splits. `TAB:I` is the most fragile selected artifact class after top-10 edge removal.

## Interpretation

This control separates two facts that both matter:

- High-frequency edge signs carry a large share of the broad structural signal.
- They do not explain all of it. Stored-order likelihood and bidirectional held-out exact-sign prediction remain above simple baselines after removing the top 10 edge signs.

The remaining signal is still not a reading. It is a structural residue that now needs stricter controls:

- terminal-class rather than exact-terminal prediction,
- nonlinguistic administrative and emblematic comparators,
- and reproduction on authoritative or image-validated corpora.

The formula-family downweighting follow-up is recorded here:

[Lipi formula-family downweighting baseline](lipi_family_downweight_baseline.md)

That follow-up shows the top-10 edge-removed signal also survives edge-frame and one-edit-family downweighting, though one-edit families become very large and should be treated as a blunt stress test.

## Result

This probe supports only this claim:

```text
In the filtered `lipi` numeric-clean planning layer, high-frequency edge signs explain a substantial part of the broad structural signal, but duplicate-collapsed stored-order and leakage-controlled held-out exact-sign prediction remain above simple baselines after removing the top 10 edge signs.
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

- Does terminal-class prediction remain after exact terminal signs are removed?
- Can nonlinguistic administrative or emblematic controls reproduce the same residual profile?
- Does an authoritative M77/CISI/ICIT or image-validated corpus reproduce the same profile?
