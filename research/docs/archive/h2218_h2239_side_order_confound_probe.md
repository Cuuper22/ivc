# H-2218 Through H-2239 Side-Order Confound Probe

Date: 2026-05-24

## Purpose

This note is a probe — a narrow statistical check — for a confound: an alternative explanation that could produce the local side-order pattern without the pattern meaning anything. It follows the [H-2218 through H-2239 Fig. 4 mapping](h2218_h2239_fig4_mapping.md) and the [H-2218 through H-2239 dimension side-order probe](h2218_h2239_dimension_side_order_probe.md).

It asks a narrow source-control question:

```text
Does the local A versus side-swap split collapse to manufacturing group or published Fig. 4 sequence order?
```

This matters because Meadow and Kenoyer 2000 separates the tablets into three manufacturing groups and also presents them in a fixed figure order. A later functional hypothesis must not confuse physical side behavior with source ordering, engraver grouping, or publication layout.

This is not a reading.

## Local Artifacts

```text
data/open_prototype/tools/lipi_h2218_side_order_confound_probe.mjs
data/open_prototype/reports/lipi_h2218_h2239_side_order_confound.csv
data/open_prototype/reports/lipi_h2218_h2239_side_order_confound_tests.csv
data/open_prototype/reports/lipi_h2218_h2239_side_order_confound_summary.json
```

Input:

```text
data/open_prototype/reports/lipi_h2218_h2239_fig4_mapping.csv
```

## Scope

```text
source_rows: 22
canonical_a_b_rows: 20
coarse_signature_counts: A 13; B_side_swap 7; variant 2
canonical_signature_counts: A 13; B 7
manufacturing_group_counts: group_1 6; group_2 9; group_3 7
```

The two non-canonical rows are kept in the coarse A/B/variant blockiness check:

- `H-2237`: `154` instead of `156`.
- `H-2238`: `033` instead of `034`.

## Fig. 4 Order By Manufacturing Group

| Manufacturing Group | Fig. 4 Signature Sequence |
| --- | --- |
| group 1 | `B_side_swap A A B_side_swap A A` |
| group 2 | `A B_side_swap A A B_side_swap B_side_swap A A A` |
| group 3 | `variant variant B_side_swap B_side_swap A A A` |

These sequences show visible local blocks, especially in group 3. The point of the probe is to ask whether that blockiness is stronger than expected after the observed label counts are fixed.

## Tests

| Comparison | Scope | Statistic | Adjacent Pairs | Exact P >= Observed | Permutation Space |
| --- | --- | ---: | ---: | ---: | ---: |
| Canonical A/B group distribution chi-square | 20 canonical A/B rows | 0.073260 |  | 1.000000 | 77520 |
| Canonical Fig. 4 B-B adjacency | 20 canonical A/B rows | 2 | 18 | 0.683243 | 77520 |
| Canonical within-group B-B adjacency | 20 canonical A/B rows | 2 | 17 | 0.641447 | 77520 |
| Canonical within-group-count-conditioned B-B adjacency | 20 canonical A/B rows | 2 | 17 | 0.438889 | 12600 |
| Coarse A/B/variant within-group blockiness | all 22 rows | 10 | 19 | 0.173416 | 264600 |

## Interpretation

The canonical A/B side-order split is almost exactly spread across the three manufacturing groups:

```text
group_1: A 4; B 2
group_2: A 6; B 3
group_3: A 3; B 2
```

The exact group-distribution test returns `p >= observed = 1.000000`, so the observed split is not concentrated by manufacturing group.

The published Fig. 4 order has visible same-label blocks, but the exact sequence controls do not make those blocks unusual under fixed counts:

- B-B adjacency across canonical Fig. 4 order: `p >= observed = 0.683243`.
- B-B adjacency inside manufacturing groups: `p >= observed = 0.641447`.
- B-B adjacency after preserving each group's A/B counts: `p >= observed = 0.438889`.
- Full A/B/variant same-label blockiness inside groups: `p >= observed = 0.173416`.

This weakens two easy explanations:

1. The A/B side-order split is simply Meadow and Kenoyer manufacturing group.
2. The A/B side-order split is simply published Fig. 4 sequence order.

It does not promote side order into a physical or functional fact. It only says those two confounds do not explain the current local split in this planning layer — the local `lipi` transcription data, which is not yet image-validated.

## Consequence

The next image-validation pass should keep four layers separate for every object:

1. Local `lipi` side order.
2. Published Fig. 4 item order.
3. Meadow and Kenoyer manufacturing group.
4. Physical side order visible in plate/CISI/HARP imagery.

If image validation confirms the A/B side-order split, later functional hypotheses must explain why that split crosses manufacturing groups, does not track size, and is not just Fig. 4 ordering. If image validation collapses the split, this becomes a cataloging-convention problem.

Follow-up:

- [H-2218 through H-2239 side-role template probe](h2218_h2239_side_role_template_probe.md) sharpens A/B into a three-role template: `+15x-003+` is always local side 3, while `+861-003+` and `+700-03x+` swap across local sides 1 and 2.

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
