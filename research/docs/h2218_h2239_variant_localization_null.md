# H-2218 Through H-2239 Variant Localization Null

Date: 2026-05-25

## Question

Are the two singleton H-series variants distributed like broad sign-function evidence, or are they localized in the same manufacturing/template/figure stratum?

This is a direct falsification pressure test on the attractive H-series story. If the `033/034` and `154/156` variants are clustered inside one local batch, then workshop, copy, or template-local behavior stays a dangerous explanation.

## Outputs

```text
data/open_prototype/tools/lipi_h2218_h2239_variant_localization_null.mjs
data/open_prototype/reports/lipi_h2218_h2239_variant_localization_objects.csv
data/open_prototype/reports/lipi_h2218_h2239_variant_localization_tests.csv
data/open_prototype/reports/lipi_h2218_h2239_variant_localization_summary.json
```

Inputs:

```text
data/open_prototype/reports/lipi_h2218_h2239_fig4_mapping.csv
data/open_prototype/reports/lipi_h2218_h2239_side_role_templates.csv
data/open_prototype/reports/lipi_h2218_h2239_minimal_contrast_packet.csv
```

## Result

```text
object rows: 22
singleton variant objects: H-2237; H-2238
singleton variant slots: H-2237 role_15x_003; H-2238 role_700_03x
unordered pair nulls: 231
accepted decipherment claims: 0
```

Exact pair-localization checks:

| Test | Null hits | Total pairs | Exact probability |
| --- | ---: | ---: | ---: |
| Same manufacturing group | 72 | 231 | 0.311688 |
| Both in group 3 | 21 | 231 | 0.090909 |
| Same role-template class | 114 | 231 | 0.493506 |
| Both in `template_700_861_15x` | 36 | 231 | 0.155844 |
| Both in group 3 and `template_700_861_15x` | 6 | 231 | 0.025974 |
| Adjacent in Fig. 4 order | 21 | 231 | 0.090909 |
| Adjacent in Fig. 4 order within group 3 | 6 | 231 | 0.025974 |
| Adjacent in Fig. 4 order within group 3 and `template_700_861_15x` | 3 | 231 | 0.012987 |

## Object-Level Consequence

The two variants are:

| Object | Fig. 4 no. | Group | Template | Variant slot | Same group/template controls | Exact-dimension controls |
| --- | ---: | --- | --- | --- | ---: | ---: |
| `H-2237` | 17 | group 3 | `template_700_861_15x` | `role_15x_003`: `+154-003+` | 2 | 1 |
| `H-2238` | 18 | group 3 | `template_700_861_15x` | `role_700_03x`: `+700-033+` | 2 | 0 |

This is the annoying but useful answer: the variants are exactly where a controlled-slot story wants them, but also exactly where a batch/workshop/template-local confound wants them.

## Research Consequence

The H-series minimal contrasts stay live because both variants still sit in controlled slots with local controls:

```text
H-2237: +700-034+ | +861-003+ | +154-003+
H-2233/H-2230 controls: +700-034+ | +861-003+ | +156-003+

H-2238: +700-033+ | +861-003+ | +156-003+
H-2230/H-2233 controls: +700-034+ | +861-003+ | +156-003+
```

But the localization result blocks a broad sign-function upgrade. The next source test has to ask whether this is a real paradigmatic contrast on the same physical side roles or just a group-3/template-local workshop variant.

Minimum source gate:

1. Source images must confirm the same physical side roles for `H-2237`, `H-2238`, `H-2230`, and `H-2233`.
2. `154/156` and `033/034` must be visually separable at diagnostic stroke level.
3. Group-3 controls must be checked together, not as isolated pretty pairs.
4. Manufacturing/workshop notes must be treated as active confounds, not background context.

## Claim Status

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted side functions: 0
accepted H-series slot values from this test: 0
```
