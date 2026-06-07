# Lipi FRAME700 034 Matched-Control Probe

Date: 2026-05-25

## Question

Can the live `034` rows be tested against close `033` and `032` controls under current object metadata, or is the residue still only object-format confounding?

This is not a translation experiment. It is a source-prioritization experiment:

```text
If close metadata controls exist, source images can test a functional contrast.
If close controls do not exist, object-format explanation remains dominant.
```

## Local Artifacts

```text
data/open_prototype/tools/lipi_frame700_034_matched_control_probe.mjs
data/open_prototype/reports/lipi_frame700_034_matched_control_probe.csv
data/open_prototype/reports/lipi_frame700_034_matched_control_probe_summary.json
```

Inputs:

```text
data/open_prototype/reports/lipi_frame700_subtype_rows.csv
data/open_prototype/reports/lipi_frame700_034_source_acquisition_manifest.csv
data/open_prototype/lipi/metadata_filtered.csv
```

## Method

Scope:

```text
non-H FRAME700 rows only
target rows: all 93 non-H 034 rows
candidate 033 rows: 136
candidate 032 rows: 102
```

For each `034` row, the script finds the closest `033` and closest `032` row by weighted metadata/context matching:

```text
type, sides, site
material, shape, cross-section, symbol
area/section, period/phase, excavation prefix
horizontal bin, vertical bin, area bin, aspect bin
context class, side relation, 700 order
long-token set
```

The score is not evidence of meaning. It is a triage score for whether a source-visible contrast can be tested without changing too many object variables at once.

## Result

Readiness counts:

| Readiness | Rows |
| --- | ---: |
| `strong_two_sibling_metadata_controls` | 86 |
| `strong_032_control_only` | 4 |
| `partial_metadata_control` | 2 |
| `strong_033_control_only` | 1 |

Bucket summary:

| Bucket | Rows | Readiness |
| --- | ---: | --- |
| `A_034_002_861_416_companion` | 5 | 4 strong two-sibling, 1 strong 032-only |
| `A_034_no_longer_small_object` | 13 | 13 strong two-sibling |
| `A_034_direction_reversal` | 12 | 12 strong two-sibling |
| `B_034_400_740_176_bridge` | 8 | 8 strong two-sibling |
| `E_other_034_residue` | 55 | 49 strong two-sibling, 3 strong 032-only, 2 partial, 1 strong 033-only |

## Consequence

This is the first result in this branch that actively weakens the lazy objection:

```text
"Maybe 034 only looks special because it appears on different kinds of objects."
```

The objection is not dead. Source images still decide. But current metadata does contain many close `033` and `032` controls. That means the next plate work can test source-visible contrast instead of only asking whether `034` belongs to small tablets.

## Top Source-Ready 034 Companion Contrasts

For the `+002-861-416+` bucket:

| 034 target | Best 033 control | Best 032 control | Readiness |
| --- | --- | --- | --- |
| `H-910` | `H-916` score 35 | `H-1294` score 35 | strong two-sibling |
| `H-2094` | `H-900` score 33 | `H-2173` score 33 | strong two-sibling |
| `H-2097` | `H-925` score 32 | `H-930` score 32 | strong two-sibling |
| `H-2096` | `H-924` score 28 | `H-930` score 28 | strong two-sibling |
| `H-2095` | `H-2125` score 27 | `H-1309` score 25 | strong 032-only |

Interpretation:

```text
H-910 is the cleanest representative target inside the +002-861-416 branch because it has strong 033 and 032 object-format controls.
H-2094 and H-2097 are still high priority, but H-2094/H-2095/H-2096 family repetition must be checked before treating them as independent.
H-2097 is crucial for the +034-700+ direction-risk branch.
```

Later independent-triad auditing demotes this whole branch for first archive priority because the target long-side context repeats five times. It should still get one representative source check, but independent triads now come first.

## Support And Kill Logic

Supports functional contrast if:

```text
Source-grade images show 034, 033, and 032 are visually distinct on close object-format controls, and the 034 target still differs in side/companion context after direction and family checks.
```

Downgrades to object-format association if:

```text
034 remains visually real but matched controls show the same side/context behavior once source-side order and dimensions are verified.
```

Kills the residue if:

```text
034 collapses visually into 033/032, row order is only direction normalization, no-longer rows have missing sides, or +002-861-416+ is one copied family.
```

## Boundary

No sign meaning, numerical value, metrological reading, semantic reading, phonetic value, language identity, or translation is accepted from this probe.
