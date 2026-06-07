# Lipi Formula-Family Downweighting Baseline

Date: 2026-05-24

## Purpose

This experiment asks whether the broad filtered `lipi` structural signal is mostly repeated formula families rather than a more general order signal.

It follows the [Lipi high-frequency edge removal baseline](lipi_edge_removed_baseline.md). The experiment collapses exact duplicate sequences first, then applies two formula-family downweighting policies:

- Edge-frame collapse: keep one representative per shared length, first sign, and last sign. Sequences of length 1 or 2 stay exact because their whole sequence is already edge.
- One-edit-family collapse: union exact-collapsed sequences that share a one-position wildcard frame or a one-token deletion frame, then keep one representative per connected family.

Both policies are also repeated after top-10 edge-sign removal.

This is a blunt stress test. One-edit transitive families can become very large in short-inscription corpora. That is the point of the falsifier: if the signal survives even this aggressive downweighting, then simple repeated-template explanations are incomplete. It is not an epigraphic claim that collapsed rows are the same text.

It does not treat `lipi` as authoritative. It does not assume accepted reading order. It does not assign meanings, sign values, phonetics, language identity, or translations.

## Local Artifacts

```text
data/open_prototype/tools/lipi_family_downweight_baseline.mjs
data/open_prototype/reports/lipi_family_downweight_inventory.csv
data/open_prototype/reports/lipi_family_downweight_sequence_summary.csv
data/open_prototype/reports/lipi_family_downweight_masked_summary.csv
data/open_prototype/reports/lipi_family_downweight_holdout_summary.csv
data/open_prototype/reports/lipi_family_downweight_summary.json
```

Source file:

```text
data/open_prototype/reports/lipi_scope_rows.csv
```

Parent baselines:

```text
data/open_prototype/reports/lipi_dedup_order_summary.json
data/open_prototype/reports/lipi_edge_removed_summary.json
```

Representative policy:

```text
highest exact-sequence duplicate weight, then lowest local id
```

This representative policy is deterministic only. It does not privilege the representative as more authentic.

## Family Collapse Inventory

| Policy | Input Records | Output Records | Removed | Multi-Record Families | Largest Family Records | Largest Source Weight |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| exact sequence | 1,798 | 1,798 | 0 | 0 | 1 | 117 |
| edge frame | 1,798 | 1,408 | 390 | 170 | 21 | 117 |
| one-edit family | 1,798 | 1,098 | 700 | 121 | 241 | 810 |
| top-10 edge removed, exact sequence | 1,658 | 1,658 | 0 | 0 | 1 | 43 |
| top-10 edge removed, edge frame | 1,658 | 1,550 | 108 | 74 | 6 | 43 |
| top-10 edge removed, one-edit family | 1,658 | 838 | 820 | 80 | 377 | 650 |

The one-edit policy is intentionally harsh. The largest family after top-10 edge removal contains 377 exact-collapsed records, representing 650 source rows. Treat its results as a lower-resolution stress test, not a natural cluster inventory.

## Stored Order After Family Downweighting

| Policy | Rows | Tokens | Unique Signs | Rows > 1 | Stored > Reversed | Reversed > Stored | Ties | Stored Win Share | Median Diff |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| exact sequence | 1,798 | 8,212 | 571 | 1,798 | 1,705 | 84 | 9 | 0.948276 | 9.200559 |
| edge frame | 1,408 | 6,288 | 554 | 1,408 | 1,306 | 89 | 13 | 0.927557 | 6.985179 |
| one-edit family | 1,098 | 6,011 | 509 | 1,098 | 1,046 | 39 | 13 | 0.952641 | 9.270313 |
| top-10 edge removed, exact sequence | 1,658 | 5,913 | 561 | 1,530 | 1,383 | 129 | 18 | 0.903922 | 3.912352 |
| top-10 edge removed, edge frame | 1,550 | 5,506 | 556 | 1,422 | 1,273 | 132 | 17 | 0.895218 | 3.574856 |
| top-10 edge removed, one-edit family | 838 | 3,991 | 476 | 837 | 750 | 72 | 15 | 0.896057 | 4.094345 |

Stored order survives both family downweighting policies. After top-10 edge removal and one-edit-family collapse, stored order still beats reversed order in 750 of 837 rows longer than one sign.

## Masked Sign Prediction

| Policy | Model | Masked Tokens | Top-1 | Top-5 | MRR |
| --- | --- | ---: | ---: | ---: | ---: |
| exact sequence | frequency | 8,212 | 0.107769 | 0.239284 | 0.187476 |
| exact sequence | position | 8,212 | 0.151120 | 0.321603 | 0.238405 |
| exact sequence | length-position | 8,212 | 0.154652 | 0.357404 | 0.253918 |
| exact sequence | bidirectional | 8,212 | 0.325865 | 0.567828 | 0.438744 |
| edge frame | frequency | 6,288 | 0.091603 | 0.218830 | 0.165149 |
| edge frame | position | 6,288 | 0.125795 | 0.273537 | 0.208294 |
| edge frame | length-position | 6,288 | 0.131997 | 0.300891 | 0.216537 |
| edge frame | bidirectional | 6,288 | 0.286578 | 0.520992 | 0.395514 |
| one-edit family | frequency | 6,011 | 0.090667 | 0.222925 | 0.172167 |
| one-edit family | position | 6,011 | 0.136583 | 0.302446 | 0.221124 |
| one-edit family | length-position | 6,011 | 0.140576 | 0.331559 | 0.233612 |
| one-edit family | bidirectional | 6,011 | 0.310764 | 0.548494 | 0.421222 |
| top-10 edge removed, exact sequence | frequency | 5,913 | 0.072383 | 0.181803 | 0.141158 |
| top-10 edge removed, exact sequence | position | 5,913 | 0.088449 | 0.229325 | 0.171833 |
| top-10 edge removed, exact sequence | length-position | 5,913 | 0.092508 | 0.232877 | 0.174078 |
| top-10 edge removed, exact sequence | bidirectional | 5,913 | 0.222222 | 0.440724 | 0.325997 |
| top-10 edge removed, edge frame | frequency | 5,506 | 0.066655 | 0.173810 | 0.134790 |
| top-10 edge removed, edge frame | position | 5,506 | 0.080821 | 0.222303 | 0.160192 |
| top-10 edge removed, edge frame | length-position | 5,506 | 0.087541 | 0.215765 | 0.163618 |
| top-10 edge removed, edge frame | bidirectional | 5,506 | 0.214312 | 0.427352 | 0.315403 |
| top-10 edge removed, one-edit family | frequency | 3,991 | 0.070659 | 0.181158 | 0.138834 |
| top-10 edge removed, one-edit family | position | 3,991 | 0.085192 | 0.238286 | 0.168645 |
| top-10 edge removed, one-edit family | length-position | 3,991 | 0.085943 | 0.225507 | 0.167395 |
| top-10 edge removed, one-edit family | bidirectional | 3,991 | 0.224004 | 0.428213 | 0.323794 |

The family controls do not erase the bidirectional signal. Edge removal remains the larger weakening factor.

## Leakage-Controlled Held-Out Results

All rows below remove exact resulting train/test sequence overlap after the family policy is applied.

Selected bidirectional top-1 scores:

| Policy | `SEAL:S` | `TAB:B` | Harappa | Mohenjo-daro |
| --- | ---: | ---: | ---: | ---: |
| exact sequence | 0.283740 | 0.305853 | 0.271129 | 0.297402 |
| edge frame | 0.242463 | 0.296539 | 0.259372 | 0.258750 |
| one-edit family | 0.290636 | 0.277778 | 0.280258 | 0.296535 |
| top-10 edge removed, exact sequence | 0.180733 | 0.177461 | 0.176140 | 0.199020 |
| top-10 edge removed, edge frame | 0.174640 | 0.170861 | 0.178114 | 0.187084 |
| top-10 edge removed, one-edit family | 0.179978 | 0.200422 | 0.183817 | 0.199853 |

Selected top-10 edge removed plus one-edit-family comparisons against simple baselines:

| Held-Out Split | Test Rows | OOV Share | Frequency Top-1 | Position Top-1 | Length-Position Top-1 | Bidirectional Top-1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| type `SEAL:S` | 571 | 0.105263 | 0.084284 | 0.080972 | 0.065145 | 0.179978 |
| type `TAB:B` | 128 | 0.063291 | 0.044304 | 0.063291 | 0.065401 | 0.200422 |
| site Harappa | 271 | 0.068602 | 0.058047 | 0.067722 | 0.079156 | 0.183817 |
| site Mohenjo-daro | 579 | 0.099559 | 0.073475 | 0.082292 | 0.082292 | 0.199853 |

Even under the harsh combined control, bidirectional context remains above simple baselines in the selected splits. The result is weaker and lower-resolution, but not gone.

## Interpretation

This control narrows the formula-repetition explanation:

- Exact duplicates are not the full explanation.
- Shared edge frames are not the full explanation.
- One-edit formula neighborhoods are not the full explanation, though the one-edit policy is so aggressive that it should be treated as a stress test rather than a clean family model.
- High-frequency edge signs remain the strongest identified driver so far.

The residual signal is still only structural. It does not imply meaning, grammar in the linguistic sense, or translation. It says the broad filtered layer has order dependencies that survive several anti-memorization controls.

## Result

This probe supports only this claim:

```text
In the filtered `lipi` numeric-clean planning layer, duplicate-collapsed stored-order and masked-sign structure survive edge-frame and one-edit-family downweighting, including after top-10 edge-sign removal, but the signal is substantially weakened and remains T3 structural scout evidence only.
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

- Can nonlinguistic administrative or emblematic controls reproduce the same residual profile?
- Does terminal-class prediction remain after exact terminal signs are removed?
- Does an authoritative M77/CISI/ICIT or image-validated corpus reproduce the same family-downweighted profile?
- Are the largest one-edit families real epigraphic formulae, data-entry artifacts, or artifacts of the collapse rule?
