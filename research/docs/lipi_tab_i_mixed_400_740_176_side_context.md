# Lipi TAB:I Mixed 400-740-176 Side-Context Audit

Date: 2026-05-24

## Purpose

This artifact isolates the strongest mixed short-long `TAB:I` family from the multi-side mark validation queue:

```text
long side: +400-740-176+
short side: +700-033+ or +700-034+
```

The goal is to turn a repeated side-mark pattern into a precise validation sheet. It is not a numerical reading, metrological reading, physical side function, sign meaning, phonetic value, language identification, or translation.

## Local Artifacts

```text
data/open_prototype/tools/lipi_tab_i_mixed_400_740_176_side_context.mjs
data/open_prototype/reports/lipi_tab_i_mixed_400_740_176_side_context.csv
data/open_prototype/reports/lipi_tab_i_mixed_400_740_176_side_context_summary.json
```

Input:

```text
data/open_prototype/reports/lipi_multiside_mark_validation_queue.csv
```

## Target Definition

Rows were selected from the current T3 `lipi` planning layer when all of these were true:

- priority is `P1_mixed_short_long_core`;
- artifact type is `TAB:I`;
- the side signature contains `+400-740-176+`;
- the side signature contains either `+700-033+` or `+700-034+`.

## Result

```text
target_artifacts: 26
two_side_long1_short2: 20
two_side_short1_long2: 4
three_side_long1_double_short: 1
three_side_extra_long_text: 1
short_mark_033: 18
short_mark_034: 8
positive_horizontal_measurements: 25
positive_vertical_measurements: 25
positive_thickness_measurements: 0
horizontal_mm_positive_range: 7.6-16.5
vertical_mm_positive_range: 5.8-11.9
```

## Context Classes

| Context Class | Count | CISI IDs |
| --- | ---: | --- |
| `two_side_long1_short2` | 20 | `H-308`, `H-309`, `H-312`, `H-313`, `H-314`, `H-316`, `H-317`, `H-353`, `H-357`, `H-935`, `H-936`, `H-978`, `H-1273`, `H-1302`, `H-1303`, `H-1304`, `H-1344`, `H-1345`, `H-1346`, `H-1347` |
| `two_side_short1_long2` | 4 | `H-356`, `H-934`, `H-960`, `H-979` |
| `three_side_long1_double_short` | 1 | `H-355` |
| `three_side_extra_long_text` | 1 | `H-987` |

## Why This Matters

The older shorthand said the mixed queue contains `+400-740-176+` paired with `+700-033+` or `+700-034+`. That is true, but incomplete.

The focused sheet shows that side order is part of the problem:

- Most target artifacts have long side 1 and short side 2.
- Four target artifacts reverse that order.
- One artifact repeats the short `+700-033+` mark on two sides.
- One artifact has an additional longer text side besides the target pair.

That means later tests cannot treat the pair as a simple unordered co-occurrence. They must keep physical side relation, catalog side order, and row count separate.

## Validation Needs

Before any functional test, each target artifact needs source or image validation for:

- whether the catalog rows are distinct physical sides;
- whether side order is physical, photographic, editorial, or arbitrary;
- whether `+700-033+` and `+700-034+` are visually distinct in this family;
- whether `+400-740-176+` is stable under source-image segmentation;
- whether H-355 and H-987 are true three-side variants or catalog-entry edge cases. The follow-on [H-355 double-short-side clarification audit](h355_double_short_side_clarification_audit.md) found no object-level public image for H-355, so its duplicate `+700-033+` short rows remain pending a three-side CISI/HARP source check.
- whether the two `034` before-longer packet cases survive source checking. The follow-on [H-933/H-960 034 contrast source audit](h933_h960_034_contrast_source_audit.md) found no object-level public image for either H-933 or H-960, so the contrast remains pending a paired two-side CISI/HARP source check.
- whether the five source-dark long-side-1/short-side-2 `033` replicates survive source checking. The follow-on [H-1304/H-1344/H-1347 source-dark direct request audit](h1304_h1344_h1347_source_dark_direct_request_audit.md) found no object-level image, plate, caption, or useful text-only lead for H-1304, H-1344, H-1345, H-1346, or H-1347, so they should be acquired as a direct two-side source batch.

## Next Test

After image or stronger catalog-side validation, test whether `+700-033+` versus `+700-034+` predicts:

- side placement;
- artifact dimensions;
- longer-text family membership;
- find context;
- duplicate-family membership.

Those tests must be compared against artifact/source controls before any numerical or metrological hypothesis is admissible.

Pre-validation follow-up:

- [Lipi TAB:I mixed 400-740-176 dimension probe](lipi_tab_i_mixed_400_740_176_dimension_probe.md) runs exact side-placement and dimension checks on this sheet. It finds weak raw horizontal/aspect flags in the all-target sheet, but no corrected signal and no comparable side-placement, vertical, or area split.

## Interpretation Boundary

This audit accepts no:

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

- [Lipi multi-side mark validation queue](lipi_multiside_mark_validation_queue.md)
- [H-2218 through H-2239 series validation sheet](h2218_h2239_series_validation_sheet.md)
- [Source access requests](source_access_requests.md)
