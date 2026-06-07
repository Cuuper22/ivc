# Lipi 034 Mayig Acquisition Targets

Date: 2026-05-25

## Question

Which exact `034` rows should be acquired or crosswalked first to resolve the current Mayig/Parpola coverage gap?

The prior diagnostic showed that `034` has no exact token rows in the current 179-row Mayig overlap. This packet turns that gap into a concrete acquisition list.

## Inputs And Outputs

Inputs:

```text
data/open_prototype/lipi/metadata_filtered.csv
data/open_prototype/mayig/records_index.csv
data/open_prototype/mayig/commit.json
```

Script:

```text
data/open_prototype/tools/lipi_034_mayig_acquisition_targets.mjs
```

Outputs:

```text
data/open_prototype/reports/lipi_034_mayig_acquisition_targets.csv
data/open_prototype/reports/lipi_034_mayig_acquisition_priority_objects.csv
data/open_prototype/reports/lipi_034_mayig_acquisition_summary.json
```

## Upstream Mayig State

The local Mayig index is pinned to:

```text
repo: https://github.com/mayig/indus-valley-script-corpus
commit: ad2f1e218a34b8c33c57de0d6cb8d99272765bbb
commit message: m184
indexed records: 179
```

`git ls-remote` on 2026-05-25 returned the same head commit. So the missing `M-315+` rows are not just stale local cache; the public upstream repository currently stops before those target objects.

## Result

```text
exact 034 rows: 182
object-or-row targets: 182
P0 Mohenjo-daro 034 objects missing from current Mayig: 6
P1 H-series 034 slot controls: 21
P1 FRAME700 034 branch rows: 108
P2 Mohenjo-daro 034 row with missing/non-M CISI: 1
P3 other 034 source-coverage rows: 46
accepted decipherment claims: 0
```

## P0 Crosswalk Acquisition Targets

These are the first objects to query in any fuller Mayig/Parpola corpus or authoritative sign-list crosswalk because they are Mohenjo-daro `034` rows outside the current `m184` Mayig repository.

| Object | Text | Why It Matters |
| --- | --- | --- |
| `M-2104` | `+151-097-700-034+` | Only P0 row with adjacent `700_034`; best direct FRAME700 crosswalk target. |
| `M-315` | `+390-034-002-374-228-741+` | Mohenjo-daro `SEAL:S`, complete, direction-clean, comparable to current Mayig object type. |
| `M-1206` | `+520-220-034+` | Mohenjo-daro `SEAL:S`, complete, direction-clean; paired same-object longer row exists in the lipi layer. |
| `M-685` | `]034-204+` | Fragmentary but direct Mohenjo-daro `SEAL:S` `034` row. |
| `M-1584` | `+034+` | Single-sign Mohenjo-daro pottery row; useful only as a sign-list check, not as structural context. |
| `M-1963` | `+000-034-104+` | Mohenjo-daro rectangular seal row with uncertainty; lower priority than clean seal rows. |

There is also one Mohenjo-daro `034` row without an M-numbered CISI object in the current planning layer:

```text
source_row_id 4952.1: +034-000+
```

That row is P2 because it cannot be directly queried as an M-numbered Mayig artifact without resolving the object ID first.

## H-Series Control Lane

The H-series `+700-034+` rows remain important, but they are not the first Mayig acquisition targets. They are source-image controls for the `H-2238 +700-033+` singleton:

```text
H-2218 through H-2237, excluding H-2238, plus H-2239
```

Count:

```text
21 H-series 034 slot-control objects
```

These rows answer a different question from the P0 M-number targets:

- P0 asks for missing Parpola/Mayig coverage of exact `034` rows.
- H-series controls ask whether `H-2238 +700-033+` is visually and physically comparable to the series majority `+700-034+` side role.

## Consequence

The next `034` crosswalk move is not another source-blind statistical test.

It is one of two acquisition moves:

1. Get fuller Mayig/Parpola data for `M-2104`, `M-315`, `M-1206`, `M-685`, `M-1584`, and `M-1963`.
2. Get source images and side-label evidence for the H-series `+700-034+` controls and the paired `H-2238 +700-033+` singleton.

Until one of those happens, `034` stays crosswalk-dark.

## Boundary

Accepted decipherment claims:

```text
translations: 0
phonetic values: 0
sign meanings: 0
side functions: 0
source mappings: 0
```

No `034` Mayig/Parpola mapping, sign value, function, or reading is accepted.
