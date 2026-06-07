# Lipi Variant Crosswalk Pressure

Date: 2026-05-25

## Question

Do the candidate singleton variant pairs from the H-series survive or collapse when checked against the independent Mayig/Parpola positional crosswalk layer?

This is a pressure test, not a decipherment. It asks whether the current crosswalk makes the live variants look like:

- distinct signs in a second sign system,
- allographs or sign-list splits,
- or source-dark cases where the overlap layer cannot decide.

## Inputs And Outputs

Inputs:

```text
data/open_prototype/reports/crosswalk_alignment_pairs.csv
data/open_prototype/reports/crosswalk_lipi_to_mayig_candidates.csv
data/open_prototype/reports/crosswalk_mayig_to_lipi_candidates.csv
data/open_prototype/reports/overlap_probe.csv
```

Script:

```text
data/open_prototype/tools/lipi_variant_crosswalk_pressure.mjs
```

Outputs:

```text
data/open_prototype/reports/lipi_variant_crosswalk_pressure_signs.csv
data/open_prototype/reports/lipi_variant_crosswalk_pressure_alignments.csv
data/open_prototype/reports/lipi_variant_crosswalk_pressure_pairs.csv
data/open_prototype/reports/lipi_variant_crosswalk_pressure_summary.json
```

## Sign-Level Result

| Lipi sign | Clean aligned rows | Top Mayig/Parpola sign | Reverse pressure | Status |
| --- | ---: | --- | --- | --- |
| `032` | 21 | `P145` | `P145 -> 032` at 20/22, runner-up `002` | FRAME700 control |
| `033` | 9 | `P147` | `P147 -> 033` at 9/9 | crosswalk-supported |
| `034` | 0 | none | none | crosswalk-dark |
| `154` | 1 | `P004` | `P004 -> 156` top, `154` runner-up | sparse collapse pressure |
| `156` | 5 | `P004` | `P004 -> 156` top, `154` runner-up | active collapse pressure |

## Pair-Level Result

### `154/156`

The current overlap layer aligns both signs to `P004`:

```text
154 -> P004: 1 aligned position
156 -> P004: 5 aligned positions
reverse P004 -> 156: 5/6, runner-up 154: 1/6
```

This creates active allograph or sign-list-collapse pressure. It does not prove `154` and `156` are visually identical, but it prevents using `H-2237 +154-003+` versus `H-2233 +156-003+` as functional evidence until source images show a diagnostic visual distinction.

Current status:

```text
collapse_pressure_active_not_proven
```

### `033/034`

This is not the same pattern. `033` is cleanly supported:

```text
033 -> P147: 9/9 aligned positions
P147 -> 033: 9/9 aligned positions
```

But `034` has no clean aligned positions and no candidate row in the current crosswalk candidate file.

Current status:

```text
033_crosswalk_supported_034_unobserved_in_overlap
```

That means `034` is not currently collapsed with `033` by this layer. It is crosswalk-dark. The next question is source coverage and sign-list mapping, not a lazy allograph merge.

### `032/033/034`

The FRAME700 family now has a sharper split:

```text
032 -> P145
033 -> P147
034 -> no clean overlap candidate
```

Current status:

```text
frame700_crosswalk_differentiates_032_033_034_unobserved
```

This supports keeping `032` and `033` separate in the clean overlap layer, while keeping `034` unresolved.

## Research Consequence

The two H-series singleton failures are no longer one generic "variant" problem.

`H-2237` asks whether `154/156` survive a strong `P004` collapse pressure. The image check must decide if `154` and `156` are source-visible diagnostic variants or only a catalog/sign-list split.

`H-2238` asks whether `033/034` can be source-validated when the clean crosswalk supports `033 -> P147` but gives no clean `034` mapping. The source request must not assume either collapse or distinction for `034` from the overlap layer alone.

Follow-up diagnostic:

The [034 crosswalk darkness diagnostic](lipi_034_crosswalk_darkness_diagnostic.md) shows that `034` is absent upstream of candidate generation: the broader filtered `lipi` layer has 182 exact `034` rows, but the current 179-row Mayig overlap has zero exact `034` token rows. So the `033/034` branch needs more coverage or authoritative sign-list mapping before the crosswalk can adjudicate it.

## Boundary

Accepted decipherment claims:

```text
translations: 0
phonetic values: 0
sign meanings: 0
side functions: 0
source mappings: 0
```

The crosswalk remains provisional positional alignment only. It can create pressure, route source requests, and kill sloppy assumptions. It cannot authorize a reading.
