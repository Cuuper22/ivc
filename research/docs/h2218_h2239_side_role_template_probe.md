# H-2218 Through H-2239 Side-Role Template Probe

Date: 2026-05-24

## Purpose

This probe follows the [H-2218 through H-2239 series validation sheet](h2218_h2239_series_validation_sheet.md), [Fig. 4 mapping](h2218_h2239_fig4_mapping.md), and [side-order confound probe](h2218_h2239_side_order_confound_probe.md).

It asks a narrower question than A versus side-swap:

```text
Do the 22 local rows fit a stable three-role side template?
```

The point is to separate local catalog-side structure from meaning. A stable side-role template is useful because it tells the image-validation pass exactly what to falsify. It is not a physical side function, sign value, or translation.

## Local Artifacts

```text
data/open_prototype/tools/lipi_h2218_side_role_template_probe.mjs
data/open_prototype/reports/lipi_h2218_h2239_side_role_templates.csv
data/open_prototype/reports/lipi_h2218_h2239_side_role_counts.csv
data/open_prototype/reports/lipi_h2218_h2239_side_role_tests.csv
data/open_prototype/reports/lipi_h2218_h2239_side_role_summary.json
```

Input:

```text
data/open_prototype/reports/lipi_h2218_h2239_fig4_mapping.csv
```

## Role Families

The probe uses only local sign-string shape:

| Role Family | Local Texts |
| --- | --- |
| `role_861_003` | `+861-003+` |
| `role_700_03x` | `+700-034+`, `+700-033+` |
| `role_15x_003` | `+156-003+`, `+154-003+` |

These names are bookkeeping labels only. They do not assign meaning.

## Result

```text
source_rows: 22
complete_three_role_inventory_rows: 22
side3_role_15x_003_rows: 22
two_template_fit_rows: 22
```

Role counts by local side:

| Local Side | `role_861_003` | `role_700_03x` | `role_15x_003` |
| --- | ---: | ---: | ---: |
| side 1 | 13 | 9 | 0 |
| side 2 | 9 | 13 | 0 |
| side 3 | 0 | 0 | 22 |

Template classes:

| Template Class | Count |
| --- | ---: |
| `template_861_700_15x` | 13 |
| `template_700_861_15x` | 9 |

Exact text counts by role:

| Role | Exact Text | Count |
| --- | --- | ---: |
| `role_861_003` | `+861-003+` | 22 |
| `role_700_03x` | `+700-034+` | 21 |
| `role_700_03x` | `+700-033+` | 1 |
| `role_15x_003` | `+156-003+` | 21 |
| `role_15x_003` | `+154-003+` | 1 |

## Variant Localization

| Object | Fig. 4 No. | Group | Local Side | Variant Text | Role | Template |
| --- | ---: | --- | ---: | --- | --- | --- |
| `H-2237` | 17 | group 3 | 3 | `+154-003+` | `role_15x_003` | `template_700_861_15x` |
| `H-2238` | 18 | group 3 | 1 | `+700-033+` | `role_700_03x` | `template_700_861_15x` |

Both single-object variants sit inside the `template_700_861_15x` side-role order. That does not make them related; it only makes them a sharper image-validation target.

## Rowwise Role-Permutation Checks

If each object is treated as one `role_861_003`, one `role_700_03x`, and one `role_15x_003` side with random local side positions, then:

| Check | Observed | Eligible N | Rowwise Null | Exact P >= Observed |
| --- | ---: | ---: | --- | ---: |
| `role_15x_003_fixed_on_side_3` | 22 | 22 | one of three role positions per object | `3.186635545325e-11` |
| `two_template_fit_861_700_15x_or_700_861_15x` | 22 | 22 | two of six role permutations per object | `3.186635545325e-11` |

These p values are not promoted as population statistics. They are a compact way to state that the local catalog-side template is extremely structured under a rowwise role-shuffle sanity check.

## Interpretation

The current local layer is not just:

```text
A versus B
```

It is more specifically:

```text
template_861_700_15x: +861-003+ | +700-03x+ | +15x-003+
template_700_861_15x: +700-03x+ | +861-003+ | +15x-003+
```

The `role_15x_003` side is stable as local side 3 in all 22 rows. The `role_861_003` and `role_700_03x` sides swap between local side 1 and local side 2.

This sharpens the plate question:

```text
Is local side 3 a real repeated physical side position, a catalog convention, an image ordering convention, or a transcription artifact?
```

## Consequence

The next image-validation pass should record, for each object:

1. Whether `role_15x_003` is truly on the same physical side position across the series.
2. Whether `role_861_003` and `role_700_03x` physically swap or only swap in catalog order.
3. Whether the H-2237 `154`/`156` variant and H-2238 `033`/`034` variant are visually real.
4. Whether any physical side adjacency explains the two local templates.

Follow-up:

- [H-2218 through H-2239 template recurrence audit](h2218_h2239_template_recurrence_audit.md) checks the complete three-role template against all 397 validation-queue rows. It finds no non-H complete or near recurrence, so the template stays series-specific until new source evidence expands it.

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
