# Lipi 154/156 Comparanda Packet

Date: 2026-05-25

## Question

In the H-series slot grammar, `H-2237` stands alone: it is the only H-2218 through H-2239 object with `+154-003+` where the role majority has `+156-003+`.

The external-distribution audit then showed that `154_003` is sparse but not unique:

```text
H-2237: +154-003+
H-366: +154-003+
H-1682: +154-003-617-033+
M-102: +154-003-900-545+
```

This packet asks what those external rows actually buy us. Do they produce real comparanda for the H-2237 slot question, or only a weak allograph/source-validation warning?

## Inputs And Outputs

Inputs:

```text
data/open_prototype/lipi/metadata_filtered.csv
data/open_prototype/reports/crosswalk_alignment_pairs.csv
data/open_prototype/reports/crosswalk_lipi_to_mayig_candidates.csv
data/open_prototype/reports/overlap_probe.csv
```

Script:

```text
data/open_prototype/tools/lipi_154_156_comparanda_packet.mjs
```

Outputs:

```text
data/open_prototype/reports/lipi_154_156_comparanda_rows.csv
data/open_prototype/reports/lipi_154_156_ranked_controls.csv
data/open_prototype/reports/lipi_154_156_crosswalk_pressure.csv
data/open_prototype/reports/lipi_154_156_comparanda_summary.json
```

## Distribution

```text
packet rows: 40
154_003 rows: 4
156_003 rows: 36
accepted decipherment claims: 0
```

Scope counts:

| Scope | Rows |
| --- | ---: |
| `h_series_singleton_variant` | 1 |
| `h_series_majority_156_003` | 21 |
| `external_strict_154_003` | 1 |
| `external_strict_156_003` | 10 |
| `external_longer_154_003` | 2 |
| `external_longer_156_003` | 5 |

External `154_003` objects:

| Object | Text | Site | Type | Shape | Class | Current Use |
| --- | --- | --- | --- | --- | --- | --- |
| `H-366` | `+154-003+` | Harappa | `TAB:I` | cuboid | `AN` | strict external exact support |
| `H-1682` | `+154-003-617-033+` | Harappa | `SEAL:S` | square | `SC` | longer prefix-frame support |
| `M-102` | `+154-003-900-545+` | Mohenjo-daro | `SEAL:S` | square | `SS` | longer prefix-frame support plus Mayig overlap |

## Ranked Controls

Best current `156_003` controls for each `154_003` row:

| Target | Best Control | Why It Ranks |
| --- | --- | --- |
| `H-2237 +154-003+` | `H-2233 +156-003+` | Same H-series scope, same site/type/shape/material/class/direction/sign count, and two invariant companion side texts. |
| `H-366 +154-003+` | `H-2230 +156-003+` | Same site/type/material/direction/sign count/id-prefix/token length, but this is not independent of the H-series. |
| `H-366 +154-003+` non-H-series only | `H-288 +156-003+` | Same site/type/direction/sign count/id-prefix/token length, but shape/material/class are weaker. |
| `M-102 +154-003-900-545+` | `M-132 +156-003-545+` | Same site/type/shape/material/class/direction/id-prefix and shares suffix token `545` after `003`. |
| `H-1682 +154-003-617-033+` | `H-81 +156-003+` | Same site/type/shape/direction/id-prefix, but not a close text-length or suffix control. |

Interpretation:

- `H-2237/H-2233` remains the cleanest 154/156 contrast. The external packet does not beat it.
- `H-366` is valuable because it is the only strict external `+154-003+` row, but its best non-H-series control is weaker than the H-series controls.
- `M-102/M-132` is the most interesting external longer-text pair because it shares a later token after `003`; it is not the same kind of two-token side-role contrast.
- `H-1682` keeps the prefix-frame alive but does not currently provide a tight control.

## Crosswalk Pressure

The overlap/crosswalk layer creates a serious caution:

```text
lipi 154 -> Mayig/Parpola P004 alignments: 1
lipi 156 -> Mayig/Parpola P004 alignments: 5
```

Observed position alignments:

| Artifact | Lipi | Mayig/Parpola | Context |
| --- | --- | --- | --- |
| `M-102` | `154` | `P004` | `<s> 154 003` aligns to `<s> P004 P123` |
| `M-80` | `156` | `P004` | `<s> 156 003` aligns to `<s> P004 P123` |
| `M-93` | `156` | `P004` | `<s> 156 003` aligns to `<s> P004 P123` |
| `M-132` | `156` | `P004` | `<s> 156 003` aligns to `<s> P004 P123` |
| `M-96` | `156` | `P004` | `<s> 156 004` aligns to `<s> P004 P124` |
| `M-97` | `156` | `P004` | `<s> 156 435` aligns to `<s> P004 P188` |

This does not prove `154` and `156` are the same sign. It proves the opposite of what a lazy argument would want: the H-2237 contrast is now under allograph/crosswalk pressure and has to survive source images.

## Current Research Consequence

The honest state is:

```text
154/156 visual distinction: alive but source-gated
154/156 slot-function contrast: not accepted
154/156 allograph/crosswalk collapse: active competing explanation
strongest local test: H-2237 vs H-2233
best external strict support: H-366
best external longer-text pressure pair: M-102 vs M-132
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted side functions: 0
```

## Next Source Questions

1. `H-2237/H-2233`: are `154` and `156` visually distinct on the same H-series physical side role while `+700-034+` and `+861-003+` stay invariant?
2. `H-366`: is the strict external `+154-003+` source-visible, and does it visually match the H-2237 `154` form?
3. `M-102/M-132`: does the `M-102` source image really carry the form transcribed as `154`, while `M-132` carries `156`, even though the Mayig/Parpola overlap maps both to `P004`?
4. `H-1682`: is the longer `154_003` prefix real, or does the longer seal context expose a different segmentation/allograph convention?

Any failure in these source checks downgrades the 154/156 branch to catalog/sign-list variation until stronger evidence appears.
