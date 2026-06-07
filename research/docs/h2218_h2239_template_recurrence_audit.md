# H-2218 Through H-2239 Template Recurrence Audit

Date: 2026-05-24

## Purpose

This audit follows the [H-2218 through H-2239 side-role template probe](h2218_h2239_side_role_template_probe.md).

It asks whether the H-series three-role template is isolated or part of a wider side-mark pattern:

```text
Does the complete H-2218 through H-2239 side-role template recur elsewhere in the 397-row validation queue?
```

This matters for the decipherment program because the next interpretation branch changes depending on the answer:

- If the template recurs outside the H-series, it becomes a broader structural hypothesis.
- If the template is isolated, it is more likely a copied-object, source-series, or catalog-side problem until image validation says otherwise.

This is not a reading.

## Local Artifacts

```text
data/open_prototype/tools/lipi_h2218_template_recurrence_audit.mjs
data/open_prototype/reports/lipi_h2218_template_recurrence_rows.csv
data/open_prototype/reports/lipi_h2218_template_recurrence_near_matches.csv
data/open_prototype/reports/lipi_h2218_template_recurrence_summary.json
```

Input:

```text
data/open_prototype/reports/lipi_multiside_mark_validation_queue.csv
```

## Method

The audit scans all 397 artifact groups in the multi-side validation queue.

It checks two role policies:

| Policy | Meaning |
| --- | --- |
| strict | Exact local strings: `+861-003+`, `+700-033+` or `+700-034+`, and `+154-003+` or `+156-003+`. |
| unordered | Same two-token sets regardless of order, for example `+033-700+` is treated as a near `role_700_03x` form. |

It then records:

- complete three-role inventory matches,
- exact H-template matches,
- and non-H near matches with at least two H-series role families.

## Result

```text
validation_queue_rows: 397
h_series_rows: 22
non_h_series_rows: 375
strict_complete_h_inventory_rows: 22
strict_complete_h_inventory_non_h_rows: 0
unordered_complete_h_inventory_rows: 22
unordered_complete_h_inventory_non_h_rows: 0
non_h_near_match_rows: 0
```

Template class counts:

| Template Class | Strict Count | Unordered Count |
| --- | ---: | ---: |
| `template_861_700_15x` | 13 | 13 |
| `template_700_861_15x` | 9 | 9 |

The strict and unordered policies give the same complete-template result: all complete matches are exactly the H-2218 through H-2239 series.

No non-H artifact group has even two of the three H-series role families under either policy.

## Interpretation

The current validation queue does not support generalizing the H-series template to the broader multi-side short-mark queue.

That makes the H-series more series-specific:

```text
H-2218 through H-2239 = source-anchored copied/related tablet-series problem
broader short-mark queue = separate validation problem
```

This does not prove that the H-series template is nonlinguistic, copied, administrative, metrological, or functional. It only blocks a premature generalization from the 22-object series to the wider queue.

## Consequence

The next plate/image request should keep two branches separate:

1. H-2218 through H-2239: validate the isolated three-role side template.
2. Mixed short-long and TAB:B/TAB:I core queues: validate their own side-mark structures without importing the H-series template.

If future source data finds the same three-role template outside H-2218 through H-2239, this audit should be rerun.

## Interpretation Boundary

This audit does not support:

- Physical side function.
- Numerical value.
- Metrological reading.
- Commodity reading.
- Administrative reading.
- Sign meaning.
- Phonetic value.
- Language identity.
- Translation.
