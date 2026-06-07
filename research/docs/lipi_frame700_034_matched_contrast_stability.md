# Lipi FRAME700 034 Matched Contrast Stability

Date: 2026-05-25

## Question

Which `034` matched-control triads remain local contrast candidates after requiring both `033` and `032` controls to share object, visual, and context features?

This probe separates two things that had been getting blurred:

1. Independent, low-copy source targets.
2. Strict local minimal contrasts.

They are not the same set in the current planning layer.

## Outputs

```text
data/open_prototype/tools/lipi_frame700_034_matched_contrast_stability.mjs
data/open_prototype/reports/lipi_frame700_034_matched_contrast_stability.csv
data/open_prototype/reports/lipi_frame700_034_matched_contrast_stability_summary.json
```

Inputs:

```text
data/open_prototype/reports/lipi_frame700_034_source_triad_packet.csv
data/open_prototype/reports/lipi_frame700_034_independent_triad_audit.csv
```

## Method

For each non-H-series `034` target, the probe takes the closest `033` and `032` controls from the source triad packet and asks which matched features are shared by both controls.

Core fields:

```text
object core: type, sides, site, material, shape, cross_section
visual core: h_bin, v_bin, area_bin, aspect_bin
context core: context_class, side_relation, order
```

Grades:

| Grade | Meaning in this audit |
| --- | --- |
| `A_strict_local_minimal_contrast` | object, visual, and context core all match |
| `B_visual_object_order_matched` | object and visual core match, and `700` order matches |
| `C_visual_object_matched` | object and visual core match |
| `D_object_plus_some_context` | object core matches, plus `order` or `side_relation` |
| `E_object_only` | object core matches only |
| `F_partial_or_weak` | object core does not fully match |

Copy pressure is inherited from the independent triad audit:

```text
low repetition: Tier A, target long-set count <= 1, acquisition-family count <= 1
moderate repetition: target long-set count <= 2, acquisition-family count <= 1
high repetition: everything more copy/family pressured than that
```

## Result

```text
triads: 93
strong local contrasts: 13
low-repetition strong local contrasts: 0
accepted decipherment claims: 0
```

Grade counts:

| Grade | Count |
| --- | ---: |
| `F_partial_or_weak` | 56 |
| `D_object_plus_some_context` | 21 |
| `B_visual_object_order_matched` | 7 |
| `A_strict_local_minimal_contrast` | 3 |
| `C_visual_object_matched` | 3 |
| `E_object_only` | 3 |

Copy-pressure counts:

| Copy pressure | Count |
| --- | ---: |
| `high_repetition_pressure` | 52 |
| `moderate_repetition_pressure` | 38 |
| `low_repetition_pressure` | 3 |

Long-context relation counts:

| Relation | Count |
| --- | ---: |
| `all_three_differ` | 57 |
| `same_as_both_controls` | 28 |
| `same_as_033_control` | 7 |
| `target_differs_controls_share` | 1 |

## First Independent Batch

The first low-copy archive batch remains useful, but it is not locally strict:

| Rank | Target | Controls | Grade | Copy pressure | Long context |
| ---: | --- | --- | --- | --- | --- |
| 1 | `H-1850` | `H-1842` / `H-1772` | `D_object_plus_some_context` | low | all three differ |
| 2 | `H-771` | `H-789` / `H-1123` | `D_object_plus_some_context` | low | all three differ |
| 3 | `H-1943` | `H-1940` / `H-854` | `D_object_plus_some_context` | low | all three differ |
| 4 | `H-2204` | `H-2209` / `H-2217` | `F_partial_or_weak` | moderate | all three differ |

Consequence:

This batch tests whether the `034` residue survives away from repeated long-text families. It does not test the cleanest local minimal contrasts.

## Strong Local Contrast Rows

The strict/local lane is stronger on object and visual matching, but it is repetition pressured:

| Target | Rank | Grade | Copy pressure | Controls | Long context |
| --- | ---: | --- | --- | --- | --- |
| `H-1824` | 16 | `C_visual_object_matched` | moderate | `H-1883` / `H-212` | all three differ |
| `H-893` | 17 | `A_strict_local_minimal_contrast` | moderate | `H-925` / `H-930` | all three differ |
| `H-2137` | 18 | `B_visual_object_order_matched` | moderate | `H-925` / `H-930` | all three differ |
| `H-983` | 21 | `B_visual_object_order_matched` | moderate | `H-353` / `H-2211` | all three differ |
| `H-2140` | 38 | `B_visual_object_order_matched` | high | `H-925` / `H-930` | all three differ |
| `H-2141` | 39 | `B_visual_object_order_matched` | high | `H-925` / `H-930` | all three differ |
| `H-1860` | 47 | `B_visual_object_order_matched` | high | `H-1861` / `H-1865` | same as both controls |
| `H-2102` | 48 | `B_visual_object_order_matched` | high | `H-2131` / `H-930` | same as `033` control |
| `H-910` | 50 | `A_strict_local_minimal_contrast` | high | `H-916` / `H-1294` | all three differ |
| `H-2130` | 52 | `B_visual_object_order_matched` | high | `H-2131` / `H-930` | same as `033` control |
| `H-308` | 61 | `A_strict_local_minimal_contrast` | high | `H-935` / `H-2146` | same as `033` control |
| `H-2097` | 64 | `C_visual_object_matched` | high | `H-925` / `H-930` | all three differ |
| `H-938` | 66 | `C_visual_object_matched` | high | `H-925` / `H-930` | all three differ |

Consequence:

The attractive minimal-contrast lane is not independent enough by itself. It should be used as a stress batch after, or alongside, the independent batch.

## What Changed

Before this probe, the next acquisition plan risked asking for one mixed batch and pretending it answered both independence and local contrast.

Now the plan splits:

1. Independent low-copy batch: `H-1850/H-1842/H-1772`, `H-771/H-789/H-1123`, `H-1943/H-1940/H-854`, `H-2204/H-2209/H-2217`.
2. Local minimal-contrast stress batch: `H-893/H-925/H-930`, `H-1824/H-1883/H-212`, `H-2137/H-925/H-930`, `H-983/H-353/H-2211`, with `H-910/H-916/H-1294` kept as an optional repeated-branch add-on.

The first batch attacks copy-family suspicion. The second attacks whether `034`, `033`, and `032` are visibly distinct local slot choices under close object controls.

## Boundary

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted language assignments: 0
accepted administrative values: 0
```

The live claim is still narrow:

```text
034 is a source-targeted distributional residue inside the FRAME700 tablet side-mark system.
```

This probe does not upgrade that claim. It makes the next source request less sloppy.
