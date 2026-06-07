# 032-002-861 X-Before-240 Family-Cell Bridge Audit

Date: 2026-05-29

## Question

Does the `603` bridge-lock pattern survive when repeated X-before-`240` rows are collapsed into formula/register family cells?

## Method

The raw X-before-`240` packet has 95 rows. This audit collapses rows by `(X sign, prefix, after-240 subframe, register key, signless formula template)`. That keeps linguistic formula cells instead of treating repeated identical Harappa text rows as independent evidence.

Family cells: `81` from `95` raw rows across `28` X signs.

A label-shuffle null then shuffles X labels across family cells for 20,000 iterations, preserving X family-cell counts and after-`240` family-cell sizes.

## Target Profiles

| X | family cells | raw rows | subframes | locked? | post-861 initial rows | after-240 cells |
|---|---:|---:|---:|---|---:|---|
| 603 | 1 | 3 | 1 | True | 3 | 060 692:1 |
| 636 | 12 | 15 | 5 | False | 0 | <END>:6;031 032 171:2;060 692:2;066 556:1;233 235 002:1 |
| 642 | 6 | 7 | 5 | False | 0 | 060 692:2;001 692:1;031 002 861:1;204 705 621:1;<END>:1 |
| 482 | 6 | 8 | 2 | False | 0 | 002 861:5;002 944 920:1 |
| 904 | 4 | 7 | 3 | False | 0 | <END>:2;002 817:1;235:1 |
| 000 | 2 | 2 | 1 | True | 1 | <END>:2 |

## Null Results

- `P(shuffled 603 has one family cell) = 1.000000`
- `P(shuffled 603 single family cell lands in 060 692) = 0.061500`
- `P(any non-background bridge sign has a single family cell) = 1.000000`
- `P(any non-background bridge sign has >=2 family cells locked to one subframe) = 0.000000`

## Decision

Status: `603_harappa_side_collapses_to_one_family_cell_bridge_not_promoted`.

- `603` has three raw X-before-240 rows but only one family cell after collapsing by X, prefix, after-240 subframe, register, and signless formula template.
- At family-cell level, `603` no longer supplies replicated Harappa-side internal evidence. It is one Harappa formula/register cell plus the post-002-861 Mohenjo tail family.
- The row-level bridge-lock pressure is therefore demoted from weak-to-moderate support to acquisition-priority pressure.
- The live promotion path is source graphic identity or a second independent family cell for Harappa/non-Mohenjo `603`.

Accepted values, phonetics, language identity, translations, and graphic identity remain 0/unaccepted.
