# Lipi Short-Mark Dimension Stress Audit

Date: 2026-05-24

## Question

This note tests one of the few ideas about the script that physical objects can settle directly: if a sign records a size or a quantity, objects carrying it should measure differently. A short mark is a one- or two-sign row on an object that carries writing on more than one side. Blocking means the comparison is run only inside groups of objects that already match on type, site, shape, material, and side count, so that an apparent size effect cannot come from those shortcuts. The question: do recurrent multi-side short-mark tokens track object measurements after blocking obvious catalog shortcuts?

This is a direct pressure test on a possible semantic crack: short side marks could be administrative, numerical, metrological, form-factor labels, or merely catalog/type artifacts. The point is not to assign values. The point is to see whether the strongest short-mark tokens touch physical measurements strongly enough to deserve plate/source validation.

## Input

Source:

```text
data/open_prototype/lipi/metadata_filtered.csv
```

Status:

```text
T3 filtered lipi planning layer
claim columns removed
image/plate validation pending
```

`lipi` is the project's filtered working corpus of Indus sign sequences; T3 planning layer is its tier label for unverified working data, useful for direction but never admissible as proof.

Design:

- One row per CISI artifact, not one row per side.
- Include artifacts with at least one clean multi-side short-mark row.
- Test token presence in the artifact's clean short rows.
- Use physical measurements from the same artifact record: horizontal, vertical, thickness, area, and aspect.
- For each token and dimension, compare present-vs-absent mean difference.
- Permute token presence inside `type|site|shape|material|sides` blocks.
- Correct all emitted tests with Benjamini-Hochberg false discovery rate.

This avoids the fake inflation that would come from counting three sides of one tablet as three independent measurements.

## Coverage

```text
artifact_rows: 436
artifacts_with_horizontal: 398
artifacts_with_vertical: 386
artifacts_with_thickness: 117
target_tokens: 003;032;033;034;156;400;520;690;700;740;861
token_tests: 41
permutation_iterations_per_test: 5000
permutation_block: type|site|shape|material|sides
```

## Corrected Flags

Corrected measurement associations, artifact-level:

| Token | Dimension | Present Artifacts | Mean Present | Mean Absent | Permutation p | BH q |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `003` | horizontal | 29 | 11.382759 | 17.134688 | 0.000400 | 0.002343 |
| `003` | area | 29 | 81.448966 | 248.637349 | 0.000200 | 0.001367 |
| `003` | aspect | 29 | 1.608140 | 1.894241 | 0.003399 | 0.013414 |
| `034` | horizontal | 113 | 14.164602 | 17.727018 | 0.004799 | 0.016397 |
| `034` | vertical | 113 | 7.630973 | 10.369231 | 0.003599 | 0.013414 |
| `034` | area | 112 | 109.765000 | 289.187500 | 0.001800 | 0.009225 |
| `156` | horizontal | 27 | 12.492593 | 17.022911 | 0.000200 | 0.001367 |
| `156` | vertical | 26 | 7.273077 | 9.733333 | 0.000200 | 0.001367 |
| `156` | area | 26 | 86.110769 | 246.858000 | 0.000200 | 0.001367 |
| `156` | aspect | 26 | 1.608312 | 1.891776 | 0.009798 | 0.030901 |
| `740` | aspect | 10 | 1.557167 | 1.880782 | 0.016197 | 0.047434 |
| `861` | horizontal | 30 | 11.970000 | 17.102446 | 0.000200 | 0.001367 |
| `861` | area | 30 | 105.800667 | 247.009133 | 0.000200 | 0.001367 |
| `861` | aspect | 30 | 1.589059 | 1.896723 | 0.002999 | 0.013414 |

The mechanic pass rejected measurement ranges such as `3 - 3.3` instead of coercing them to the lower bound. That reduced usable artifact-level thickness values from 129 to 117. No thickness association survives correction.

## Reading The Pattern

The strongest cluster is not broad. It is concentrated around the Harappa tablet short-mark family already isolated by the multi-side work:

```text
003 / 156 / 861: smaller horizontal size, smaller area, lower aspect
034: smaller horizontal, vertical, and area
740: aspect only, with the minimum accepted present count, so it is fragile
```

The `003`, `156`, and `861` flags overlap heavily with the H-2218 through H-2239 three-side tablet role template. That matters. It means the signal could be a real object-family/form-factor association, a publication/catalog convention, a manufacturing-group effect not fully removed by the block key, or a genuine short-mark functional layer. It is not yet a metrological reading.

The `034` signal is broader: 113 present artifacts, mostly Harappa tablets with `+700-034+` or variants. That makes it a better next target than the narrow `740` aspect flag.

## H-Series Removal

Removing H-2218 through H-2239 kills all corrected dimension flags:

```text
artifact_rows_after_h_series_removed: 414
corrected_flags_after_h_series_removed: none
lowest_remaining_test: 034 area, p 0.003599, BH q 0.104371
```

So the dimension signal is not a broad metrological result. It is mainly the H-series plus a weaker `034` lead.

## Immediate Consequence

This is real movement toward the problem, but at A2/A3 boundary only — A2 and A3 being the project's evidence-strength grades, well below anything admissible as proof:

- `003`, `156`, `861`, and `034` should move up the source-validation queue.
- The next plate/image check should ask whether these marks really occupy the recorded sides and whether the dimensions are object-level measurements for the same artifacts.
- The next statistical check should split the H-2218 through H-2239 three-side series from the broader `034` tablet family so one famous series does not explain the whole result.

## Artifacts

```text
data/open_prototype/tools/lipi_short_mark_dimension_stress_audit.mjs
data/open_prototype/reports/lipi_short_mark_dimension_artifact_rows.csv
data/open_prototype/reports/lipi_short_mark_dimension_token_tests.csv
data/open_prototype/reports/lipi_short_mark_dimension_stress_summary.json
data/open_prototype/reports/lipi_short_mark_dimension_no_h_series_token_tests.csv
data/open_prototype/reports/lipi_short_mark_dimension_no_h_series_summary.json
```

## Interpretation Boundary

No numerical value, metrological reading, semantic reading, sign meaning, phonetic value, language identity, or translation is accepted from this audit.

Surviving associations are source-validation targets only.
