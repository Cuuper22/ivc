# Lipi TAB:I Mixed 400-740-176 Dimension Probe

Date: 2026-05-24

## Purpose

This note records a statistical stress test run before any images have been checked. It exists to find out, cheaply, whether an apparent sign contrast lines up with anything physically measurable — so that later, expensive image validation knows what to look for.

The setting: `TAB:I` is a Harappa tablet type code from the catalog. The "mixed family" is a group of tablets whose long side carries the sign sequence `+400-740-176+` and whose short side carries a short mark — either `+700-033+` or `+700-034+`. Numbers like `400`, `740`, `176`, `700`, `033`, and `034` are catalog sign codes, not readings. The mixed `TAB:I` side-context sheet is the earlier note that isolated this family.

Question:

```text
Within the +400-740-176+ mixed family, does short mark +700-033+ versus +700-034+ track side placement or dimensions?
```

This is a pre-validation stress test on the T3 `lipi` planning layer — the exploratory, catalog-derived data this project computes from before image validation. It is not a numerical reading, metrological reading, physical side function, sign meaning, phonetic value, language identification, or translation.

## Local Artifacts

```text
data/open_prototype/tools/lipi_tab_i_mixed_400_740_176_dimension_probe.mjs
data/open_prototype/reports/lipi_tab_i_mixed_400_740_176_dimension_probe_rows.csv
data/open_prototype/reports/lipi_tab_i_mixed_400_740_176_dimension_probe_tests.csv
data/open_prototype/reports/lipi_tab_i_mixed_400_740_176_dimension_probe_summary.json
```

Input:

```text
data/open_prototype/reports/lipi_tab_i_mixed_400_740_176_side_context.csv
```

## Method

For `+700-033+` versus `+700-034+`, the probe tests:

- side-placement context using exact 2x2 tests;
- extra-side status using exact 2x2 tests;
- horizontal measurement using exact mean-difference permutation;
- vertical measurement using exact mean-difference permutation;
- area, computed from positive horizontal and vertical values;
- aspect ratio, computed from positive horizontal divided by positive vertical.

Zero dimensions are treated as missing.

## Result

```text
target_artifacts: 26
two_side_artifacts: 24
canonical_long1_short2_artifacts: 20
short_mark_033_artifacts: 18
short_mark_034_artifacts: 8
```

Group summaries:

```text
033 horizontal_n: 17
033 horizontal_mean: 13.735294
033 vertical_n: 17
033 vertical_mean: 6.900000
033 area_n: 16
033 area_mean: 93.510625
033 aspect_n: 16
033 aspect_mean: 2.030050

034 horizontal_n: 8
034 horizontal_mean: 11.587500
034 vertical_n: 8
034 vertical_mean: 7.612500
034 area_n: 8
034 area_mean: 86.051250
034 aspect_n: 8
034 aspect_mean: 1.607244
```

Exact exploratory tests, all target rows:

| Test | Eligible N | `033` | `034` | Exact P |
| --- | ---: | --- | --- | ---: |
| short mark predicts two-side long1-short2 | 26 | 13/18 | 7/8 | 0.627850 |
| short mark predicts extra-side case | 26 | 2/18 | 0/8 | 1.000000 |
| horizontal mean difference | 25 | 13.735294 | 11.587500 | 0.035523 |
| vertical mean difference | 25 | 6.900000 | 7.612500 | 0.204885 |
| area mean difference | 24 | 93.510625 | 86.051250 | 0.306835 |
| aspect mean difference | 24 | 2.030050 | 1.607244 | 0.041961 |

Robustness checks:

| Subset | Test | Eligible N | Exact P |
| --- | --- | ---: | ---: |
| two-side only | horizontal mean difference | 23 | 0.071042 |
| two-side only | aspect mean difference | 22 | 0.091325 |
| canonical long1-short2 only | horizontal mean difference | 19 | 0.254366 |
| canonical long1-short2 only | aspect mean difference | 18 | 0.239348 |

Multiple-test correction (Bonferroni and Benjamini-Hochberg, applied because many tests ran at once):

```text
raw_p_lte_005_tests: all_target:horizontal_value; all_target:aspect_value
bonferroni_lte_005_tests: none
bh_fdr_lte_005_tests: none
```

## Interpretation

The current planning layer shows weak raw splits for horizontal measurement and aspect ratio in the all-target sheet:

```text
horizontal_value exact p: 0.035523
aspect_value exact p: 0.041961
```

Those raw flags do not survive Bonferroni or Benjamini-Hochberg correction across the emitted tests. They also weaken when the sheet is restricted to simpler side-context subsets.

The probe does not show a comparable split for:

- two-side long1-short2 placement;
- extra-side cases;
- vertical measurement;
- area.

This is not metrological evidence. The correct use is to prioritize later image/source validation and ask whether the `033`/`034` contrast survives real side checks.

## Consequence

The mixed `TAB:I` branch now has a specific post-validation test:

1. Validate the physical side relation and sign segmentation for the 26 target artifacts.
2. Confirm whether `033` and `034` are visually distinct in this family.
3. Rerun the dimension comparison only on source-validated rows.
4. Compare any surviving split against artifact dimensions, side placement, duplicate-family membership, and find-context controls.

## Interpretation Boundary

This probe accepts no:

- Numerical value.
- Metrological reading.
- Physical side function.
- Commodity reading.
- Administrative reading.
- Sign meaning.
- Phonetic value.
- Language identity.
- Translation.

Follow-ups:

- [Lipi TAB:I mixed 400-740-176 side-context audit](lipi_tab_i_mixed_400_740_176_side_context.md)
- [Lipi multi-side mark validation queue](lipi_multiside_mark_validation_queue.md)
- [Source access requests](source_access_requests.md)
