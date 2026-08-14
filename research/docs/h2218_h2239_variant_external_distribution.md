# H-2218 Through H-2239 Variant External Distribution

Date: 2026-05-25

This note traces two sign variants outside the tablet series that produced them. It exists to answer a simple worry: if a variant appears on only one object in the world, it is probably a typo or damage; if it appears elsewhere, it is more likely real.

## Question

The H-series slot grammar — the hidden-side reconstruction experiment — isolated two singleton exact-text failures:

```text
H-2237: +154-003+ where the local role majority expects +156-003+
H-2238: +700-033+ where the local role majority expects +700-034+
```

This experiment asks whether those breaks are only local H-series oddities, or whether the same target variants have external distribution in the broader filtered `lipi` planning layer — the project's working transcription corpus, used for planning and not yet image-validated.

This is not a decipherment claim. It is a source-priority and variant-reality test.

## Inputs And Outputs

Input:

```text
data/open_prototype/lipi/metadata_filtered.csv
```

Script:

```text
data/open_prototype/tools/lipi_h2218_h2239_variant_external_distribution.mjs
```

Outputs:

```text
data/open_prototype/reports/lipi_h2218_h2239_variant_external_distribution_rows.csv
data/open_prototype/reports/lipi_h2218_h2239_variant_external_distribution_contexts.csv
data/open_prototype/reports/lipi_h2218_h2239_variant_external_distribution_pairs.csv
data/open_prototype/reports/lipi_h2218_h2239_variant_external_distribution_summary.json
```

Method notes:

- Scanned all 5,679 filtered metadata rows.
- Tracked target signs `033`, `034`, `154`, and `156`.
- Separated strict exact side texts from adjacent pair occurrence inside longer texts.
- Treated H-2218 through H-2239 as the local H-series under test.
- Grouped same-object companion texts by `cisi`; rows with missing `cisi` (`-`) are deliberately not merged into one artificial mega-object.

## Result

```text
metadata rows scanned: 5679
rows with any target sign: 835
accepted decipherment claims: 0
```

Strict exact text counts:

| Text | Count |
| --- | ---: |
| `+700-033+` | 125 |
| `+700-034+` | 109 |
| `+033-700+` | 32 |
| `+034-700+` | 14 |
| `+154-003+` | 2 |
| `+156-003+` | 31 |
| `+003-154+` | 0 |
| `+003-156+` | 0 |

Adjacent pair counts:

| Pair | Total Rows | Non-H-2218..H-2239 Rows | Strict Exact Rows | Strict Non-H-Series Exact Rows |
| --- | ---: | ---: | ---: | ---: |
| `700_033` | 151 | 150 | 125 | 124 |
| `700_034` | 116 | 95 | 109 | 88 |
| `033_700` | 35 | 35 | 32 | 32 |
| `034_700` | 14 | 14 | 14 | 14 |
| `154_003` | 4 | 3 | 2 | 1 |
| `156_003` | 36 | 15 | 31 | 10 |
| `003_154` | 0 | 0 | 0 | 0 |
| `003_156` | 0 | 0 | 0 | 0 |

## External Support

`H-2238` is not relying on a corpus-wide singleton. `700_033` has 151 adjacent rows, 150 outside H-2218 through H-2239, and 124 strict exact `+700-033+` rows outside the H-series. The same short mark also appears in the mixed short-long Harappa family with `+400-740-176+`, including examples such as `H-309`, `H-316`, `H-353`, `H-357`, `H-935`, `H-978`, `H-1302`, `H-1303`, `H-1304`, and `H-1344` through `H-1347`.

`H-2237` is much thinner, but not alone. The `154_003` adjacent frame appears in four rows:

| Row | Object | Site | Type | Text |
| --- | --- | --- | --- | --- |
| `794.3` | `H-2237` | Harappa | `TAB:I` | `+154-003+` |
| `810.1` | `H-1682` | Harappa | `SEAL:S` | `+154-003-617-033+` |
| `1385.1` | `H-366` | Harappa | `TAB:I` | `+154-003+` |
| `2629.1` | `M-102` | Mohenjo-daro | `SEAL:S` | `+154-003-900-545+` |

So `+154-003+` is not exclusively an H-2237 row. But the strict external support is only one non-H-series exact row, `H-366`, plus two longer-text contexts. That is enough to keep the visual distinction alive, not enough to infer a role.

## Interpretation

The slot-grammar failures are now asymmetric:

- `H-2238 +700-033+` has broad external support in the same `700` frame. It should be treated as a real variant candidate, but still source-gated inside the H-series because external `700_033` rows belong to other object families and repeated local clusters.
- `H-2237 +154-003+` has sparse but real external support. It should no longer be dismissed as a one-object catalog typo solely from distribution, but the evidence is still too thin for function. The source-image question remains central.
- `H-2237/H-2233` remains the strongest local `154/156` minimal pair because it is same group, same H-series template, same dimensions, and differs only in the `15x_003` side role.
- `H-2238/H-2230/H-2233` remains the strongest local `033/034` H-series contrast because `+861-003+` and `+156-003+` stay invariant.

## Current Boundary

This experiment upgrades neither sign into a meaning, reading, phonetic value, number, commodity, office, or side function.

It changes the research posture:

```text
033/034: broad external variant support; source validation should focus on whether the H-series slot contrast is physically real.
154/156: sparse external support; source validation should focus on diagnostic strokes and whether H-2237/H-2233 preserve a same-side role contrast.
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted side functions: 0
```
