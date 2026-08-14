# Lipi FRAME700 034 Source Triad Packet

Date: 2026-05-25

## Question

This note pairs each object under test with the two objects it should be compared against. FRAME700 is the project's label for short inscription rows built on sign `700`, such as `+700-034+`; the `034` work asks whether the sign codes `032`, `033`, and `034` are separate choices in the same slot. A control is a comparison object that matches the target in shape, size, site, and material, so the sign code is close to the only thing that differs; a target plus its two controls is a triad. The question: for every live non-H `034` row, what exact `033` and `032` source controls should be checked beside it?

The point is to make the next plate request contrastive:

```text
034 target -> closest 033 sibling -> closest 032 control
```

This moves the work from "034 is interesting" to "these three objects decide whether the interest is source-visible contrast, object-format, direction/allograph, or copy-family noise."

## Local Artifacts

```text
data/open_prototype/tools/lipi_frame700_034_source_triad_packet.mjs
data/open_prototype/reports/lipi_frame700_034_source_triad_packet.csv
data/open_prototype/reports/lipi_frame700_034_source_triad_packet_summary.json
```

Inputs:

```text
data/open_prototype/reports/lipi_frame700_034_matched_control_probe.csv
data/open_prototype/reports/lipi_frame700_subtype_rows.csv
data/open_prototype/lipi/metadata_filtered.csv
```

## Result

```text
triad_rows: 93
```

Counts by target bucket:

| Target bucket | Triads |
| --- | ---: |
| `E_other_034_residue` | 55 |
| `A_034_no_longer_small_object` | 13 |
| `A_034_direction_reversal` | 12 |
| `B_034_400_740_176_bridge` | 8 |
| `A_034_002_861_416_companion` | 5 |

Counts by readiness:

| Readiness | Triads |
| --- | ---: |
| `strong_two_sibling_metadata_controls` | 86 |
| `strong_032_control_only` | 4 |
| `partial_metadata_control` | 2 |
| `strong_033_control_only` | 1 |

## Top Triads

### 1. Cleanest `+002-861-416+` Representative Triad

A source hook is an identifier in our own records that can be searched for in an archive.

| Role | CISI | Row | Text | Source hook |
| --- | --- | --- | --- | --- |
| Target `034` | `H-910` | `1792.2` | `+700-034+` with `002;416;861` | `10994470` |
| `033` control | `H-916` | `1796.2` | `+700-033+` | `12516456` |
| `032` control | `H-1294` | `1061.2` | `+700-032+` | `PII-1499` |

Why this was first in the local triad packet:

```text
Both controls match strongly on object-format metadata.
It avoids the H-2094/H-2095/H-2096 repeated-family issue.
It tests whether 034 keeps a different companion/context profile under similar object conditions.
```

Source question:

```text
Do H-910, H-916, and H-1294 show visually distinct 034/033/032 signs under comparable object-format conditions, and does H-910's +002-861-416+ context remain source-real?
```

Later independent-triad auditing keeps this as the representative `+002-861-416+` branch check, but moves first archive priority to family-independent triads.

### 2. High-Value Repeated-Family Triads

| Rank | Target | `033` control | `032` control | Target hook |
| ---: | --- | --- | --- | --- |
| 2 | `H-2094 +700-034+` | `H-900 +700-033+` | `H-2173 +700-032+` | `H2001-5134`, `Figure 47.02` |
| 3 | `H-2097 +034-700+` | `H-925 +700-033+` | `H-930 +700-032+` | `H2001-5193`, `Figure 48.02` |
| 4 | `H-2096 +700-034+` | `H-924 +700-033+` | `H-930 +700-032+` | `H95-2488` |
| 5 | `H-2095 +700-034+` | `H-2125 +700-033+` | `H-1309 +700-032+` | `H90-1688`, `Figure 13.44 (d)` |

Why these still matter:

```text
They are the cleanest current 034 companion-family signal.
H-2097 tests the +034-700+ direction hazard.
H-2094/H-2095/H-2096 must be checked for copy, mold, figure, or production-family dependence before counting as independent.
```

### 3. No-Longer / Small-Object Triads

| Rank | Target | `033` control | `032` control | Target hook |
| ---: | --- | --- | --- | --- |
| 6 | `H-307 +700-034+` | `H-928 +700-033+` | `H-1156 +700-032+` | `1963` |
| 7 | `H-788 +700-034+` | `H-798 +700-033+` | `H-1836 +700-032+` | `558683` |
| 8 | `H-2105 +700-034+` | `H-929 +700-033+` | `H-2129 +700-032+` | `H95-2428`, `Figure 27.13` |
| 9 | `H-952 +700-034+` | `H-929 +700-033+` | `H-930 +700-032+` | `G257469` |
| 10 | `H-947 +700-034+` | `H-928 +700-033+` | `H-2146 +700-032+` | `8650b493` |

Why these matter:

```text
They decide whether "no longer text" is real all-short/no-longer object behavior or just missing side coverage.
If the controls are source-comparable and 034 remains distinct, object-format-only explanations weaken.
```

## What Each Triad Must Decide

Every triad carries three possible outcomes:

```text
Preserve functional contrast:
034, 033, and 032 are visually distinct; source side order/direction holds; 034 keeps different side/companion behavior under comparable object conditions.

Downgrade to object-format association:
034 is visible, but matched 033/032 controls show the same side/context behavior once source dimensions and side coverage are corrected.

Kill the residue, meaning the leftover pattern that has survived the controls run so far:
034 collapses into 033/032; order is direction normalization; longer rows are missegmented; no-longer status is missing imaging; or the contrast is only duplicate/copy family.
```

## Boundary

No sign meaning, numerical value, metrological reading, semantic reading, phonetic value, language identity, or translation is accepted from this triad packet.
