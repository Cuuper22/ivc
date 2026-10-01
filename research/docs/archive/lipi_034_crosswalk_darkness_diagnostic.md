# Lipi 034 Crosswalk Darkness Diagnostic

Date: 2026-05-25

This note explains an absence. When the project tried to line up its own sign numbers against published sign lists, one sign — `034` — came back with nothing. An absence can mean the sign was filtered out by a rule, or that it was never in the compared material at all. Those are very different problems, and this note works out which one it is.

## Question

Why did `034` have no clean Mayig/Parpola crosswalk candidate? A crosswalk lines up one sign-numbering system against another, sign by sign.

Possibilities:

- `034` occurs in the Mayig overlap but was filtered out by count mismatch or clean-alignment rules.
- `034` does not occur as an exact token in the current Mayig overlap layer.
- a raw text search is confusing sign `034` with object IDs such as `M-34`.

## Inputs And Outputs

Inputs:

```text
data/open_prototype/lipi/metadata_filtered.csv
data/open_prototype/reports/overlap_probe.csv
data/open_prototype/reports/crosswalk_alignment_pairs.csv
data/open_prototype/reports/crosswalk_lipi_to_mayig_candidates.csv
```

Script:

```text
data/open_prototype/tools/lipi_034_crosswalk_darkness_diagnostic.mjs
```

Outputs:

```text
data/open_prototype/reports/lipi_034_crosswalk_darkness_sign_coverage.csv
data/open_prototype/reports/lipi_034_crosswalk_darkness_rows.csv
data/open_prototype/reports/lipi_034_crosswalk_darkness_overlap_rows.csv
data/open_prototype/reports/lipi_034_crosswalk_darkness_summary.json
```

## Result

The current Mayig overlap layer is narrow:

```text
overlap rows: 179
overlap site: Mohenjo-daro only
overlap type: SEAL:S only
Mayig descriptions: unicorn I-V seals only
```

Exact token coverage:

| Lipi sign | Broad metadata rows | Overlap rows | Clean alignment rows | Candidate |
| --- | ---: | ---: | ---: | --- |
| `032` | 566 | 27 | 21 | `P145` |
| `033` | 506 | 12 | 9 | `P147` |
| `034` | 182 | 0 | 0 | none |

The raw string `034` appears once in `overlap_probe.csv`, but it is not a sign-token hit. It is an object-string hit such as `M-34`.

## Interpretation

The `034` crosswalk gap is not caused by clean-alignment filtering.

It happens earlier:

```text
exact 034 rows in broader lipi planning layer: 182
exact 034 rows in current Mayig overlap layer: 0
```

So the correct status is:

```text
coverage_absent_from_overlap_not_crosswalk_filtered
```

That means the current crosswalk cannot decide whether `034` maps to a Mayig/Parpola sign. It also cannot justify merging `034` with `033` or separating it from `033`.

## Distribution Clue

The broader `034` layer is heavily outside the current overlap:

```text
Harappa 034 rows: 166
Mohenjo-daro 034 rows: 7
TAB:I 034 rows: 91
TAB:B 034 rows: 53
POT:T:g 034 rows: 26
SEAL:S 034 rows: 4
```

The live source/crosswalk acquisition targets are therefore not just the H-series Harappa tablets. If a fuller Mayig/Parpola layer can be acquired or queried, the first Mohenjo-daro `034` candidates to check are:

```text
M-315: +390-034-002-374-228-741+
M-685: ]034-204+
M-1206: +520-220-034+
M-1584: +034+
M-1963: +000-034-104+
M-2104: +151-097-700-034+
```

These are acquisition and crosswalk targets only.

## Consequence

The previous variant crosswalk pressure result should be read more sharply:

- `154/156` is a real current crosswalk-collapse problem because both signs are present in the clean overlap and both align to `P004`.
- `033/034` is not a current crosswalk-collapse problem. `033` is present and maps to `P147`; `034` is absent from the current overlap.

This makes `034` a source-coverage and sign-list-acquisition problem before it is an allograph problem — a question of which shapes count as variants of the same sign.

## Boundary

Accepted decipherment claims:

```text
translations: 0
phonetic values: 0
sign meanings: 0
side functions: 0
source mappings: 0
```

No source-visible `034` mapping, sign value, function, or reading is accepted.
