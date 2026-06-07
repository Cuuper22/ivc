# H-2218 Through H-2239 Series Validation Sheet

Date: 2026-05-24

## Purpose

This sheet isolates the H-2218 through H-2239 tablet series from the broader multi-side mark validation queue.

The purpose is source control, not interpretation. Each row ties the local `lipi` transcription to the HARP object designation, published figure reference, local dimensions, local side texts, and the exact manual checks still required before any functional experiment.

## Local Artifacts

```text
data/open_prototype/tools/lipi_h2218_series_validation_sheet.mjs
data/open_prototype/reports/lipi_h2218_h2239_series_validation_sheet.csv
data/open_prototype/reports/lipi_h2218_h2239_series_validation_summary.json
```

Input:

```text
data/open_prototype/reports/lipi_multiside_mark_validation_queue.csv
```

External source:

```text
Kenoyer and Meadow 2010, Inscribed Objects from Harappa Excavations 1986-2007
https://www.harappa.com/sites/default/files/pdf/KenoyerMeadow%202010%20Inscribed%20Objects%20from%20Harappa.pdf
```

## Source Anchor

Kenoyer and Meadow 2010 identifies H-2218 through H-2239 as a 22-object group of rectangular steatite tablets, triangular in section, from Period 3B secondary deposits outside the perimeter wall in Trench 11 on the east side of Mound E.

The same source leaves the use and discard reason of these tablets unresolved. That matters: the series is a strong validation target, not a solved administrative, numerical, or semantic class.

Related figure mapping:

[H-2218 through H-2239 Fig. 4 mapping](h2218_h2239_fig4_mapping.md)

Meadow and Kenoyer 2000 provides the public Fig. 4 visual and manufacturing group legend for this series.

## Coverage

```text
expected_series_size: 22
local_rows_found: 22
all_series_ids_present: true
source_figure_count: 22
missing_source_figures: 0
priority: P1_tab_i_three_side_short_series for all 22 rows
```

## Local Signature Classes

| Local Signature | Count | Objects |
| --- | ---: | --- |
| `1:+861-003+|2:+700-034+|3:+156-003+` | 13 | `H-2218`, `H-2219`, `H-2220`, `H-2222`, `H-2223`, `H-2224`, `H-2225`, `H-2229`, `H-2231`, `H-2232`, `H-2234`, `H-2236`, `H-2239` |
| `1:+700-034+|2:+861-003+|3:+156-003+` | 7 | `H-2221`, `H-2226`, `H-2227`, `H-2228`, `H-2230`, `H-2233`, `H-2235` |
| `1:+700-034+|2:+861-003+|3:+154-003+` | 1 | `H-2237` |
| `1:+700-033+|2:+861-003+|3:+156-003+` | 1 | `H-2238` |

The first two classes may be true side-order variants, catalog side-order variants, or entry artifacts. The sheet marks them as pending.

The two single-object variants are the most important visual checks:

- `H-2237`: side 3 has `154-003` instead of `156-003`.
- `H-2238`: side 1 has `700-033` instead of `700-034`.

Follow-up side-role probe:

- [H-2218 through H-2239 side-role template probe](h2218_h2239_side_role_template_probe.md) shows that all 22 rows fit one `+861-003+` side, one `+700-03x+` side, and one `+15x-003+` side. The `+15x-003+` role is always local side 3, while the other two roles swap across local sides 1 and 2. This sharpens the plate check without accepting physical side order or meaning.

## Plate And Figure Map

| CISI | HARP Object | Published Figure | Local Signature Class |
| --- | --- | --- | --- |
| `H-2218` | `H97-3319` | `Figure 12.11` | main signature A |
| `H-2219` | `H97-3317` | `Figure 12.10` | main signature A |
| `H-2220` | `H97-3312` | `Figure 12.04` | main signature A |
| `H-2221` | `H97-3304` | `Figure 12.02` | side-1/side-2 swapped |
| `H-2222` | `H97-3305` | `Figure 12.03` | main signature A |
| `H-2223` | `H97-3306` | `Figure 12.14` | main signature A |
| `H-2224` | `H97-3318` | `Figure 12.08` | main signature A |
| `H-2225` | `H97-3315` | `Figure 12.07` | main signature A |
| `H-2226` | `H97-3313` | `Figure 12.13` | side-1/side-2 swapped |
| `H-2227` | `H97-3314` | `Figure 12.05` | side-1/side-2 swapped |
| `H-2228` | `H97-3316` | `Figure 12.12` | side-1/side-2 swapped |
| `H-2229` | `H97-3290` | `Figure 12.06` | main signature A |
| `H-2230` | `H97-3311` | `Figure 12.19` | side-1/side-2 swapped |
| `H-2231` | `H97-3320` | `Figure 12.21` | main signature A |
| `H-2232` | `H97-3321` | `Figure 12.23` | main signature A |
| `H-2233` | `H97-3341` | `Figure 12.20` | side-1/side-2 swapped |
| `H-2234` | `H97-3322` | `Figure 12.22` | main signature A |
| `H-2235` | `H97-3333` | `Figure 12.09` | side-1/side-2 swapped |
| `H-2236` | `H97-3307` | `Figure 12.15` | main signature A |
| `H-2237` | `H96-3125` | `Figure 12.17` | `154` instead of `156` |
| `H-2238` | `H95-2613` | `Figure 12.18` | `033` instead of `034` |
| `H-2239` | `H96-3046` | `Figure 12.16` | main signature A |

## Manual Validation Protocol

For each object:

1. Locate the published figure or plate image.
2. Verify the object is part of the H-2218 through H-2239 series.
3. Verify that the three local rows correspond to three physical sides.
4. Record whether local side 1, side 2, and side 3 match the published orientation.
5. Check whether `154` vs `156` on H-2237 is a real visual contrast, allograph issue, or transcription issue.
6. Check whether `033` vs `034` on H-2238 is a real visual contrast, allograph issue, or transcription issue.
7. Record whether the repeated signatures are incised copies, molded duplicates, catalog regularization, or something else, if the source image permits that judgment.

## Interpretation Boundary

This sheet does not support:

- Physical side function.
- Numerical value.
- Metrological reading.
- Commodity reading.
- Administrative reading.
- Sign meaning.
- Phonetic value.
- Language identity.
- Translation.

## Consequence

This is now the cleanest first image-validation target in E3.2.

If plate checks confirm the side count, side order, and two visual variants, then the next experiment can ask whether the H-2218 through H-2239 series behaves like:

- copied administrative tags,
- side-indexed formula tablets,
- numerical or metrological mark systems,
- nonlinguistic emblem/token systems,
- or a mixed text-and-mark system.

Those are future hypotheses. The current state is only a source-anchored validation sheet.
