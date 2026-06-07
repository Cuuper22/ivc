# Lipi Dimension Residue Stress Probe

Date: 2026-05-24

## Purpose

This probe follows the [Lipi semantic anchor prediction probe](lipi_semantic_anchor_prediction_probe.md). That probe left only tiny dimension-bin residues, especially `vertical_bin`, after blocked semantic-anchor nulls.

This stress probe asks whether those residues survive broader sign-role controls and stronger metadata shortcuts.

It does not test metrology. It does not assign sign meanings, semantic slots, phonetic values, language identity, or translations. Dimension bins are catalog measurements from a T3 planning source.

## Local Artifacts

```text
data/open_prototype/tools/lipi_dimension_residue_stress_probe.mjs
data/open_prototype/reports/lipi_dimension_residue_sign_classes.csv
data/open_prototype/reports/lipi_dimension_residue_observed.csv
data/open_prototype/reports/lipi_dimension_residue_iterations.csv
data/open_prototype/reports/lipi_dimension_residue_summary.csv
data/open_prototype/reports/lipi_dimension_residue_summary.json
```

Source file:

```text
data/open_prototype/lipi/metadata_filtered.csv
```

Scope:

```text
source_rows: 5679
numeric_clean_source_rows: 2887
exact_sequence_families: 1798
min_label_families: 30
min_sign_tokens_for_class: 20
iterations_per_block: 10
```

## Broad Sign Classes

Unlike the earlier structural-class work on the narrow Mayig overlap, this probe derives fresh broad sign classes from the 1,798 exact-sequence-collapsed `lipi` families.

Sign classes are positional only:

- `initial`
- `medial`
- `terminal`
- `single`
- `edge_mixed`
- `distributed`
- `sparse`

Observed broad class counts:

| Class | Signs |
| --- | ---: |
| `sparse` | 494 |
| `medial` | 34 |
| `distributed` | 25 |
| `initial` | 10 |
| `terminal` | 5 |
| `edge_mixed` | 3 |

These classes are not semantic. They are controls for broad sign-position behavior.

## Models And Blocks

Targets:

```text
horizontal_bin
vertical_bin
thickness_bin
area_bin
aspect_bin
```

Observed shortcut models:

- Majority.
- Length+type+site.
- Material+shape.
- Exact edge frame.
- Broad edge-class frame.
- Hard proxy: length+type+site+material+shape+direction.
- Hard proxy plus edge-class frame.
- Token NB over exact sign tokens.

Label-shuffle blocks:

- Global.
- Exact edge frame.
- Broad edge-class frame.
- Hard proxy.
- Hard proxy plus edge-class frame.

## Observed Shortcut Results

| Target | Majority | Length+Type+Site | Material+Shape | Edge-Class Frame | Hard Proxy | Token NB |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `horizontal_bin` | 0.398930 | 0.485731 | 0.471463 | 0.477408 | 0.488704 | 0.444114 |
| `vertical_bin` | 0.356122 | 0.627098 | 0.597265 | 0.413300 | 0.533250 | 0.465507 |
| `thickness_bin` | 0.436019 | 0.554502 | 0.531991 | 0.426540 | 0.546209 | 0.482227 |
| `area_bin` | 0.373750 | 0.588125 | 0.555000 | 0.432500 | 0.506250 | 0.441875 |
| `aspect_bin` | 0.618182 | 0.828213 | 0.838245 | 0.605016 | 0.786207 | 0.638871 |

Plain metadata shortcuts beat Token NB for every dimension target. That blocks any metrological interpretation from the current T3 metadata layer.

## Hardest Token NB Nulls

| Target | Hardest Block | Observed Token NB | Null Mean | Gap | Macro-F1 Gap | Unchanged Label Share |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `horizontal_bin` | hard proxy | 0.444114 | 0.434483 | 0.009631 | -0.000453 | 0.591201 |
| `vertical_bin` | edge frame | 0.465507 | 0.449037 | 0.016470 | 0.013710 | 0.864512 |
| `thickness_bin` | edge frame | 0.482227 | 0.476896 | 0.005332 | 0.003540 | 0.900000 |
| `area_bin` | edge frame | 0.441875 | 0.433937 | 0.007938 | 0.011411 | 0.865750 |
| `aspect_bin` | edge frame | 0.638871 | 0.633668 | 0.005204 | 0.010594 | 0.899624 |

The largest remaining Token NB gap is `vertical_bin`, at 0.016470 accuracy over the exact edge-frame null. But the observed Token NB is still much weaker than length+type+site at 0.627098 and material+shape at 0.597265.

The edge-frame nulls also leave high unchanged-label shares. That means the exact edge frame is too tight to act as the only final control, but the broader edge-class blocks do not rescue the result because metadata shortcuts already outperform sign-token prediction.

## Interpretation

This stress probe downgrades the dimension residue:

```text
The filtered `lipi` dimension-bin signal is better explained by artifact class, site, material, shape, direction, and edge-frame structure than by independent sign-token evidence.
```

The result supports only this claim:

```text
Dimension-bin prediction can be measured in the T3 planning layer, but no dimension target currently survives controls strongly enough for metrological or semantic interpretation.
```

It does not support:

- Metrological readings.
- Quantity or measure values.
- Commodity readings.
- Artifact-size semantics.
- Semantic slots.
- Sign values.
- Phonetic values.
- Language identity.
- Translation.

## Next Falsification

The next path should not be more broad dimension-bin prediction. Better next tests:

- Run artifact-type-specific dimension probes inside `SEAL:S`, `TAB:B`, and `TAB:I`, where object form is less wildly mixed.
- Replace catalog dimensions with image-validated measurements if available.
- Test numerical signs directly against measurements and reverse-side marks, instead of asking all signs to predict coarse bins.
- Repeat on an authoritative or image-validated corpus before treating any dimension association as evidence.

Follow-up:

- [Lipi multi-side mark scope probe](lipi_multiside_mark_scope_probe.md) starts that direct route by isolating short side-mark candidates in multi-side or multi-row artifacts.
