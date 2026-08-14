# Lipi Stratified Class Probe

Date: 2026-05-24

## Purpose

This note records a follow-up prediction experiment. It exists to answer one worry: an earlier result might be an artifact of mixing different kinds of objects together.

The setup, in plain terms. `lipi` is the filtered catalog dataset this project computes from. Each inscription row carries a catalog `class` label. The earlier [Lipi metadata prediction probe](lipi_metadata_prediction_probe.md) asked whether sign sequences predict those metadata labels better than chance. It found that type, site, and region prediction are confounded by artifact-type mixtures — the apparent signal came from which kinds of objects were in the pot. But inscription `class` prediction remained above structured nulls (comparison baselines built by shuffling or recoding the data while keeping some of its structure).

This experiment asks whether that class signal survives inside strata — that is, when we hold artifact type and site fixed and predict only within each bucket.

This remains a T3 planning-layer scout: an exploratory pass over the catalog-derived planning layer, not accepted evidence. The `class` labels come from filtered `lipi`, not an authoritative corpus. The result does not assign meanings, sign values, phonetics, language identity, or translations.

## Local Artifacts

```text
data/open_prototype/tools/lipi_stratified_class_probe.mjs
data/open_prototype/reports/lipi_stratified_class_iterations.csv
data/open_prototype/reports/lipi_stratified_class_summary.csv
data/open_prototype/reports/lipi_stratified_class_summary.json
```

Source file:

```text
data/open_prototype/reports/lipi_scope_rows.csv
```

Scope:

```text
readiness_bucket = lipi_numeric_clean_candidate
source_rows = 2887
exact_sequence_families = 1798
target = class
min_stratum_rows = 90
min_label_rows = 12
iterations_per_control = 5
```

The probe collapses exact sign sequences before prediction, so duplicate inscriptions count once. Each sign-sequence family receives the majority `class`, `type`, and `site` labels from its source rows.

## Eligible Strata

A stratum is a bucket of rows sharing a site, an artifact type, or both. Type codes like `SEAL:R`, `SEAL:S`, `TAB:B`, and `TAB:I` are catalog artifact-type codes. The probe found 11 eligible strata:

```text
site: Harappa
site: Mohenjo-daro
type: SEAL:R
type: SEAL:S
type: TAB:B
type: TAB:I
type_site: SEAL:R@Mohenjo-daro
type_site: SEAL:S@Harappa
type_site: SEAL:S@Mohenjo-daro
type_site: TAB:B@Harappa
type_site: TAB:I@Harappa
```

Models — four predictors of increasing strength:

- Majority.
- Length.
- Edge frame.
- Token NB.

Controls — four structured nulls the observed result must beat:

- Duplicate-matched position slots.
- Administrative register code.
- Emblem formula code.
- Mixed admin-emblem code.

## Observed Class Prediction

Observed Token NB results:

| Stratum | Rows | Labels | Majority Share | Token NB Accuracy | Macro-F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Harappa | 605 | 10 | 0.277686 | 0.519008 | 0.361281 |
| Mohenjo-daro | 937 | 9 | 0.181430 | 0.506937 | 0.453725 |
| SEAL:R | 174 | 7 | 0.195402 | 0.534483 | 0.519803 |
| SEAL:S | 962 | 9 | 0.181913 | 0.466736 | 0.361835 |
| TAB:B | 248 | 6 | 0.298387 | 0.520161 | 0.517826 |
| TAB:I | 122 | 3 | 0.442623 | 0.729508 | 0.729142 |
| SEAL:R@Mohenjo-daro | 94 | 6 | 0.191489 | 0.457447 | 0.381449 |
| SEAL:S@Harappa | 158 | 6 | 0.215190 | 0.386076 | 0.321023 |
| SEAL:S@Mohenjo-daro | 681 | 9 | 0.209985 | 0.456681 | 0.348565 |
| TAB:B@Harappa | 197 | 5 | 0.324873 | 0.527919 | 0.558656 |
| TAB:I@Harappa | 118 | 3 | 0.432203 | 0.720339 | 0.720004 |

The result is not just majority label imbalance. Token prediction beats majority in every eligible stratum.

## Strongest Null Comparison

The mixed admin-emblem null is the hardest control from the prior metadata probe. Observed Token NB still beats it in all 11 eligible strata:

| Stratum | Observed Token NB | Mixed Null Mean | Gap |
| --- | ---: | ---: | ---: |
| Harappa | 0.519008 | 0.296198 | 0.222810 |
| Mohenjo-daro | 0.506937 | 0.256990 | 0.249947 |
| SEAL:R | 0.534483 | 0.228735 | 0.305748 |
| SEAL:S | 0.466736 | 0.247609 | 0.219127 |
| TAB:B | 0.520161 | 0.284677 | 0.235484 |
| TAB:I | 0.729508 | 0.419672 | 0.309836 |
| SEAL:R@Mohenjo-daro | 0.457447 | 0.234042 | 0.223405 |
| SEAL:S@Harappa | 0.386076 | 0.289873 | 0.096203 |
| SEAL:S@Mohenjo-daro | 0.456681 | 0.244053 | 0.212628 |
| TAB:B@Harappa | 0.527919 | 0.291371 | 0.236548 |
| TAB:I@Harappa | 0.720339 | 0.411865 | 0.308474 |

Across all four structured-null controls, the smallest observed-minus-null mean gap for Token NB is 0.08, and no null iteration reaches the observed Token NB score in any eligible stratum.

## Interpretation

This is the cleanest metadata scout so far:

- Class prediction survives within major site strata.
- Class prediction survives within major artifact-type strata.
- Class prediction survives within the eligible type-site strata.
- The result survives duplicate-matched position slots, administrative code, emblem formula code, and mixed admin-emblem code.

This does not prove semantic classes. It means the filtered `lipi` class labels track sign-token structure in a way these structured nulls do not reproduce.

The result supports only this claim:

```text
In the filtered `lipi` numeric-clean planning layer, exact-sequence-collapsed sign tokens predict catalog `class` labels above duplicate-calibrated structured nulls even within eligible site, type, and type-site strata.
```

It does not support:

- Accepted reading direction.
- Accepted sign segmentation.
- Sign meanings.
- Semantic slots.
- Phonetic values.
- Language identity.
- Translation.
- A conclusion that catalog classes are ancient functional classes.

## Next Falsification

The next tests should attack the class result directly:

- The first direct robustness attack is recorded in [Lipi class robustness probe](lipi_class_robustness_probe.md).
- Audit what the `class` labels mean in the `lipi` source.
- Repeat class prediction after removing transformed strata that fall below original eligibility thresholds.
- Repeat on an authoritative or image-validated corpus.
- Compare against known-script administrative corpora under the same class-prediction protocol.
