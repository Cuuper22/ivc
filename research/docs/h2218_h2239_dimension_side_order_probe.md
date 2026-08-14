# H-2218 Through H-2239 Dimension Side-Order Probe

Date: 2026-05-24

## Purpose

This note records a probe — a narrow, cheap experiment run to rule out a boring explanation before anyone entertains an interesting one.

A group of small Harappa tablets, H-2218 through H-2239, carry inscriptions on more than one side. Our catalog records the order of those sides, and the objects fall into two side-order signatures: a canonical pattern, called A, and a swapped one. The interesting hypothesis is that the difference means something. The boring explanation is that it tracks how big the tablets are or how they were made.

This probe follows the [H-2218 through H-2239 Fig. 4 mapping](h2218_h2239_fig4_mapping.md).

It asks a narrow control question:

```text
Do the local side-order signatures track the available object measurements?
```

The reason is simple. If the A versus side-swap split were just a size, aspect, or manufacturing artifact, it should show up before any functional hypothesis is allowed.

This is not a reading.

## Local Artifacts

```text
data/open_prototype/tools/lipi_h2218_dimension_side_order_probe.mjs
data/open_prototype/reports/lipi_h2218_h2239_dimension_side_order.csv
data/open_prototype/reports/lipi_h2218_h2239_dimension_side_order_class_summary.csv
data/open_prototype/reports/lipi_h2218_h2239_dimension_side_order_tests.csv
data/open_prototype/reports/lipi_h2218_h2239_dimension_side_order_summary.json
```

Input:

```text
data/open_prototype/reports/lipi_h2218_h2239_fig4_mapping.csv
```

## Scope

```text
source_rows: 22
canonical_signature_rows: 20
local_signature_counts: A 13; B_side_swap 7; 154_variant 1; 033_variant 1
manufacturing_group_counts: group_1 6; group_2 9; group_3 7
horizontal_mm_rows: 22
vertical_mm_rows: 22
```

The local source has zero thickness values for this series, so thickness is excluded.

## Tests

The probe computes:

- Horizontal measurement.
- Vertical measurement.
- Area as horizontal times vertical.
- Aspect as horizontal divided by vertical.

For the canonical A versus side-swap comparison, it uses exact two-sided permutation tests over all 77,520 assignments preserving group sizes. A permutation test reshuffles the group labels every possible way and asks how often chance alone produces a gap as large as the observed one.

For the three Meadow and Kenoyer manufacturing groups, it uses a deterministic 20,000-iteration label permutation over one-way F statistics. This is a descriptive size-control check, not a population claim.

## A Versus Side-Swap

| Metric | A Mean | Side-Swap Mean | Difference | Exact Permutation P |
| --- | ---: | ---: | ---: | ---: |
| `horizontal_mm` | 10.815385 | 11.214286 | 0.398901 | 0.506889 |
| `vertical_mm` | 6.946154 | 6.800000 | -0.146154 | 0.666035 |
| `area_mm2` | 76.007692 | 76.362857 | 0.355165 | 0.959494 |
| `aspect_h_over_v` | 1.557825 | 1.654008 | 0.096183 | 0.116138 |

The available measurements do not strongly separate the canonical A and side-swap local signatures.

This does not prove that side order is functional. It only blocks the easy size-only explanation in this small source-anchored series.

## Manufacturing Groups

| Metric | Group 1 Mean | Group 2 Mean | Group 3 Mean | Permutation P |
| --- | ---: | ---: | ---: | ---: |
| `horizontal_mm` | 11.816667 | 11.111111 | 9.885714 | 0.008750 |
| `vertical_mm` | 7.216667 | 6.844444 | 6.628571 | 0.286950 |
| `area_mm2` | 85.680000 | 76.633333 | 65.680000 | 0.038950 |
| `aspect_h_over_v` | 1.642514 | 1.627550 | 1.494201 | 0.039250 |

The manufacturing groups do show measurement structure, especially horizontal size, area, and aspect.

That matters because the size-control is not blind — blind here meaning unable to detect real structure at all. It can see source-level physical clustering where the published manufacturing groups suggest it should. The same measurements do not explain the A versus side-swap split.

## Interpretation

Current constraint:

```text
In the H-2218 through H-2239 series, available dimensions track manufacturing groups more clearly than they track local A versus side-swap side-order signatures.
```

This strengthens the next validation target:

1. Keep manufacturing group, measurement, and side-order signature as separate layers.
2. Validate side order from images or CISI plates before treating it as physical.
3. Require any later functional hypothesis to explain why side-order variation crosses manufacturing groups while dimensions cluster by manufacturing group.

## Interpretation Boundary

This probe does not support:

- Physical side function.
- Numerical value.
- Metrological reading.
- Commodity reading.
- Administrative reading.
- Sign meaning.
- Phonetic value.
- Language identity.
- Translation.

## Next Falsification

The next E3.2 step should compare source images or higher-resolution plates against:

- Meadow and Kenoyer Fig. 4 item order.
- Local `lipi` side order.
- Physical side adjacency on triangular-section tablets.
- Object measurements and manufacturing groups.

If side order collapses under image validation, this queue becomes a cataloging-convention study. If side order survives image validation, the next control is whether the recurrent side marks correlate with physical side position, object size, manufacturing group, find context, or longer-text neighbors.

Follow-up:

- [H-2218 through H-2239 side-order confound probe](h2218_h2239_side_order_confound_probe.md) checks whether the local A/B split is concentrated by manufacturing group or published Fig. 4 order. It weakens both explanations in the current planning layer, while still leaving physical side order pending image validation.
