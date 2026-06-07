# Lipi Multi-Side Mark Validation Queue

Date: 2026-05-24

## Purpose

This queue turns the stratified short-mark result into artifact-level validation work.

The question is no longer only whether short marks recur statistically. The question is which specific artifacts should be checked first against images, plates, excavation notes, or stronger catalog side metadata.

This is still not a reading. It does not assign numbers, measures, side functions, sign meanings, phonetics, language identity, or translations.

## Local Artifacts

```text
data/open_prototype/tools/lipi_multiside_mark_validation_queue.mjs
data/open_prototype/reports/lipi_multiside_mark_validation_queue.csv
data/open_prototype/reports/lipi_multiside_mark_sequence_families.csv
data/open_prototype/reports/lipi_multiside_mark_validation_summary.json
```

Inputs:

```text
data/open_prototype/reports/lipi_multiside_mark_rows.csv
data/open_prototype/lipi/metadata_filtered.csv
```

External source checked:

```text
Kenoyer and Meadow 2010, Inscribed Objects from Harappa Excavations 1986-2007
https://www.harappa.com/sites/default/files/pdf/KenoyerMeadow%202010%20Inscribed%20Objects%20from%20Harappa.pdf
```

That source reports that H-2218 through H-2239 are a group of 22 rectangular steatite tablets, triangular in section, from secondary Period 3B deposits outside the perimeter wall in Trench 11 on the east side of Mound E. It also says the use and discard reason for such tablets remain unresolved. This makes H-2218 through H-2239 a high-value validation series, not a solved semantic object.

## Priority Classes

| Priority | Meaning | Count |
| --- | --- | ---: |
| `P1_tab_i_three_side_short_series` | Harappa `TAB:I`, three-side all-short tablet series with row side index 3 carrying `003` plus `156` or `154`. | 22 |
| `P1_mixed_short_long_core` | Artifact has a core short mark and a longer text row with focus tokens such as `740`, `400`, `176`, or `240`. | 205 |
| `P2_tab_b_core_short_queue` | Harappa `TAB:B` core short-mark queue without the stronger mixed short-long condition. | 81 |
| `P2_tab_i_core_short_queue` | Harappa `TAB:I` core short-mark queue outside the three-side short-series priority. | 70 |
| `P3_other_short_mark` | Other short-mark candidate rows in the two Harappa tablet strata. | 19 |

Total artifact groups with short marks in the two strata:

```text
397
```

## Highest-Value Sequence Families

| Type | Sequence Signature | Artifact Count | Queue |
| --- | --- | ---: | --- |
| `TAB:I` | `1:+400-740-176+|2:+700-033+` | 13 | mixed short-long |
| `TAB:I` | `1:+861-003+|2:+700-034+|3:+156-003+` | 13 | three-side all-short |
| `TAB:I` | `1:+400-740-176+|2:+700-034+` | 7 | mixed short-long |
| `TAB:I` | `1:+700-034+|2:+861-003+|3:+156-003+` | 7 | three-side all-short |
| `TAB:I` | `1:+700-033+|2:+368-900+` | 4 | TAB:I core short |
| `TAB:B` | `1:+700-032+|2:+740-031-001-140+` | 3 | mixed short-long |
| `TAB:I` | `1:+700-033+|2:+400-740-176+` | 3 | mixed short-long |
| `TAB:I` | `1:+700-034+|2:+002-861-416+` | 3 | TAB:I core short |

## H-2218 Through H-2239 Series

The local queue recovers all 22 objects in the H-2218 through H-2239 series as `P1_tab_i_three_side_short_series`.

Detailed sheet:

[H-2218 through H-2239 series validation sheet](h2218_h2239_series_validation_sheet.md)

Main local signatures:

| Signature | Count | Sample Objects |
| --- | ---: | --- |
| `1:+861-003+|2:+700-034+|3:+156-003+` | 13 | `H-2218`, `H-2219`, `H-2220`, `H-2222`, `H-2223`, `H-2224`, `H-2225`, `H-2229`, `H-2231`, `H-2232`, `H-2234`, `H-2236`, `H-2239` |
| `1:+700-034+|2:+861-003+|3:+156-003+` | 7 | `H-2221`, `H-2226`, `H-2227`, `H-2228`, `H-2230`, `H-2233`, `H-2235` |
| `1:+700-034+|2:+861-003+|3:+154-003+` | 1 | `H-2237` |
| `1:+700-033+|2:+861-003+|3:+156-003+` | 1 | `H-2238` |

This is exactly the kind of series where a weak decipherment would overfit. The right next step is visual/source validation:

- Are the three catalog rows actually three physical sides?
- Is side numbering stable across the 22 tablets?
- Are the two main local signatures true sign-order variants, side-order variants, or catalog entry artifacts?
- Are `154` vs `156` and `033` vs `034` visual variants, transcription differences, or real contrasts?
- Do the dimensions and excavation contexts match the published group description?

## Mixed Short-Long Queue

The second P1 queue contains 205 artifacts where a short mark and a longer text row occur in the same artifact group.

The strongest repeated mixed families include:

| Type | Long Row | Short Row | Count |
| --- | --- | --- | ---: |
| `TAB:I` | `+400-740-176+` | `+700-033+` | 13 |
| `TAB:I` | `+400-740-176+` | `+700-034+` | 7 |
| `TAB:B` | `+740-031-001-140+` | `+700-032+` | 3 |
| `TAB:I` | `+400-740-176+` | `+700-033+` with side order reversed | 3 |
| `TAB:I` | `+740-840-013+` | `+700-033+` | 3 |

These are not syntactic claims. They are inspection targets. The validation task is to check whether the short row is genuinely a side/reverse mark attached to the longer row, and whether the repeated pair survives image-level or catalog-level source validation.

Focused follow-up:

- [Lipi TAB:I mixed 400-740-176 side-context audit](lipi_tab_i_mixed_400_740_176_side_context.md) isolates 26 target artifacts in this mixed family. It finds 20 canonical long-side-1/short-side-2 pairs, 4 reversed two-side pairs, one double-short-side case, and one three-side extra-long-text case.
- [Lipi short-mark orientation audit](lipi_short_mark_orientation_audit.md) shows that the internal order of `+700-032+`, `+700-033+`, and `+700-034+` is not balanced against the reversed forms. The validation queue should preserve exact short-row order until image direction, catalog direction, and side-order conventions are checked.
- [Lipi short-mark companion context audit](lipi_short_mark_companion_context_audit.md) shows a corrected catalog-side relation split after preserving `type|700_order`: `033` is overrepresented when the short mark comes after all longer rows, while `034` is underrepresented there. This is a plate-validation priority, not a physical side-function claim.
- [Lipi short-mark side-relation validation sheet](lipi_short_mark_side_relation_validation_sheet.md) converts that contrast into 251 row-level source-validation targets. The first source request should focus on 17 unique artifacts where the `033`/`034` relation contrast overlaps the raw `+400-740-176+` longer-context hint.

## Interpretation

The validation queue supports three research moves:

1. Treat H-2218 through H-2239 as a named three-side duplicate/copy series requiring image/source validation before any interpretation.
2. Split the E3.2 queue into all-short three-side tablets and mixed short-long tablets instead of treating all short marks as one phenomenon.
3. Prioritize repeated sequence families over isolated examples.
4. Preserve exact short-mark orientation. `+700-033+` and `+033-700+` are not interchangeable before direction and image validation.
5. Preserve companion-specific side relation. The `033`/`034` contrast should be checked against physical side order rather than collapsed into a generic `03x` class.

The queue does not support:

- Numerical values.
- Standardized measures.
- Metrological readings.
- Physical side functions.
- Commodity readings.
- Administrative readings.
- Sign meanings.
- Phonetic values.
- Language identity.
- Translation.

## Next Evidence Step

For the H-2218 through H-2239 series:

- Locate plates or images for all 22 objects.
- Verify side count, side order, sign segmentation, and visual contrast between `154`/`156` and `033`/`034`.
- Record whether the local `lipi` side order matches published plate order.

For the mixed short-long queue:

- Start with the repeated `TAB:I` family `+400-740-176+` paired with `+700-033+` or `+700-034+`.
- Start the `033`/`034` side-relation plate request with H-233, H-309, H-316, H-353, H-355, H-357, H-935, H-978, H-1302, H-1303, H-1304, H-1344, H-1345, H-1346, H-1347, H-933, and H-960.
- Verify whether the short and long rows are on distinct physical sides of the same object.
- Verify whether reversed two-token short marks are real sign-order variants, image-direction artifacts, catalog-direction artifacts, or side-order artifacts.
- Verify whether the catalog-side relation contrast for `033` versus `034` survives image-level side ordering.
- Only after image/source validation, test whether the short-row token predicts a specific long-row family better than artifact type, site, dimension, and duplicate-family controls.
