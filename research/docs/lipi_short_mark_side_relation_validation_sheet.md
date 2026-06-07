# Lipi Short-Mark Side-Relation Validation Sheet

Date: 2026-05-24

## Purpose

This sheet converts the corrected `033`/`034` result from the [Lipi short-mark companion context audit](lipi_short_mark_companion_context_audit.md) into concrete source-validation targets.

The research question is no longer just:

```text
Is there a statistical contrast?
```

It is now:

```text
Which artifacts must be checked in plates or images to decide whether the catalog-side contrast is real physical side/order structure?
```

This sheet is not a decipherment. It is an inspection queue.

## Local Artifacts

```text
data/open_prototype/tools/lipi_short_mark_side_relation_validation_sheet.mjs
data/open_prototype/reports/lipi_short_mark_side_relation_validation_sheet.csv
data/open_prototype/reports/lipi_short_mark_side_relation_priority_summary.csv
data/open_prototype/reports/lipi_short_mark_side_relation_validation_summary.json
```

Inputs:

```text
data/open_prototype/reports/lipi_short_mark_companion_context_rows.csv
data/open_prototype/reports/lipi_multiside_mark_validation_queue.csv
```

## Scope

Rows included:

```text
target_rows: 251
target_artifacts: 250
033_rows: 137
034_rows: 114
```

The row count is one larger than the artifact count because H-355 has two matching short rows.

Side-relation counts:

```text
short_after_all_longer: 92
short_before_all_longer: 72
no_longer_text: 86
short_between_longer_sides: 1
```

Rows with the raw `+400-740-176+` longer-context hint:

```text
raw_400_740_176_rows: 29
raw_400_740_176_artifacts: 28
```

## Priority Classes

| Priority | Rows | Artifacts | Purpose |
| --- | ---: | ---: | --- |
| `P1_033_after_with_400_740_176` | 16 | 15 | Highest-priority overlap between corrected `033` after-longer relation and raw `+400-740-176+` context. |
| `P1_034_before_with_400_740_176` | 2 | 2 | Highest-priority contrast rows where `034` appears before `+400-740-176+`. |
| `P1_033_after_corrected_relation` | 51 | 51 | Corrected `033` after-longer relation without the `+400-740-176+` raw hint. |
| `P1_034_before_contrast_relation` | 38 | 38 | `034` before-longer contrast rows without the `+400-740-176+` raw hint. |
| `P2_034_after_exception_control` | 25 | 25 | Control rows where `034` appears after longer text. |
| `P2_033_before_exception_control` | 32 | 32 | Control rows where `033` appears before longer text. |
| `P2_raw_400_740_176_context` | 1 | 1 | Raw `+400-740-176+` context row that is neither simple after nor before. |
| `P3_no_longer_text_control` | 86 | 86 | Control rows without longer text. |

## Highest Priority Artifacts

`P1_033_after_with_400_740_176`:

```text
H-233
H-309
H-316
H-353
H-355
H-357
H-935
H-978
H-1302
H-1303
H-1304
H-1344
H-1345
H-1346
H-1347
```

H-355 appears twice in the row sheet because it has two matching `+700-033+` short rows.

`P1_034_before_with_400_740_176`:

```text
H-933
H-960
```

These 17 unique artifacts are the cleanest first plate request for the `033`/`034` side-relation contrast.

Packet:

- [Lipi short-mark plate request packet](lipi_short_mark_plate_request_packet.md) converts these 17 artifacts into a manual source-validation packet with blank evidence fields and explicit outcome codes.

## Validation Questions

For each P1 row:

1. Are the catalog rows distinct physical sides?
2. Is the catalog side order physical, photographic, editorial, or arbitrary?
3. Does the source image preserve inscription direction, impression direction, or catalog-normalized direction?
4. Is the `033`/`034` visual contrast real at source resolution?
5. Is `+400-740-176+` segmented consistently?
6. Does the apparent short-after/short-before relation survive image-level side ordering?

For controls:

1. Are the exception rows real exceptions or catalog-order artifacts?
2. Are no-longer-text controls truly all-short artifacts?
3. Do `033` and `034` keep the same visual forms in controls and P1 rows?

## Interpretation

This sheet makes the next source step sharper:

```text
Check the 17 highest-priority unique artifacts first, then use the P1 non-400-740-176 rows and P2 exception rows as controls.
```

The sheet does not say `033` or `034` means anything. It says the current planning layer has a corrected catalog-side relation contrast that deserves image validation.

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
