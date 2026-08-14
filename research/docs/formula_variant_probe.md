# Formula Variant Probe

Date: 2026-05-24

## Purpose

This note records a probe — a narrow, cheap experiment run to see whether a bigger question is worth pursuing. The bigger question is whether Indus inscriptions come in families: a shared shape with one part swapped, the way a form letter varies only in the name.

The probe looks for three things inside the strict formula subset, our tightly filtered slice of inscriptions: near-duplicate inscriptions, repeated edge frames (the same first sign paired with the same last sign, whatever sits between), and single-slot variants (two rows identical except at one position).

It does not assign sign values. It does not identify morphemes. It does not translate. It only creates a structural review queue for possible formula families and variable slots.

## Local Artifacts

```text
data/open_prototype/reports/formula_variant_pairs.csv
data/open_prototype/reports/formula_variant_slot_candidates.csv
data/open_prototype/reports/formula_variant_frame_families.csv
data/open_prototype/reports/formula_variant_summary.json
data/open_prototype/reports/formula_variant_null_iterations.csv
data/open_prototype/reports/formula_variant_null_summary.csv
data/open_prototype/reports/formula_variant_null_summary.json
```

Source file:

```text
data/open_prototype/reports/formula_pattern_sequences.csv
```

Dataset:

```text
policy: mayig_observed_parpola
strict_records: 136
scope: Mohenjo-daro unicorn seal rows
```

## Method

For every pair of strict Mayig-policy sequences — Mayig policy being one of our rules for deciding which sign shapes count as the same sign:

1. Compute token-level edit distance.
2. Keep pairs with edit distance <= 2.
3. Also keep pairs sharing the same first and last sign, even when the interior is more different.
4. For same-length pairs differing in exactly one sign, record the variable slot and its left/right context.
5. Group rows by shared first and last sign to identify edge-frame families.

This is a discovery queue. A first null-model screen has now been run separately. A null model is a scrambled version of the data that keeps some properties and destroys the pattern under test, so we can see how much of the queue chance alone would produce:

[Formula variant null model](formula_variant_null_model.md)

## Summary

```text
strict_records: 136
exact_duplicate_sequence_groups: 1
near_pairs_edit_distance_le_2: 75
single_substitution_pairs: 5
two_substitution_pairs: 33
single_insertion_deletion_pairs: 2
shared_edge_frame_pairs: 69
frame_families_count: 14
slot_candidate_groups: 3
```

## Exact Duplicate

One exact duplicate appears under the Mayig/Parpola policy:

```text
M-32:  P086 P123 P122 P385
M-177: P086 P123 P122 P385
```

This is a high-priority duplicate check, not a semantic reading. It must be validated against raw numeric signs, images, and source catalogs before it can support any administrative or formula claim.

## Top Edge-Frame Families

| Frame | Rows | Lengths | Series | I...T Rows |
| --- | ---: | --- | --- | ---: |
| `P324...P385` | 10 | 4;5;6;7;8 | II:1;III:2;IV:7 | 10 |
| `P086...P385` | 4 | 4;6 | III:1;IV:2;V:1 | 0 |
| `P324...P095` | 3 | 2;6;9 | IV:2;V:1 | 0 |
| `P324...P256` | 3 | 5;6 | I:1;III:1;IV:1 | 3 |
| `P324...P378` | 3 | 6;7 | III:1;IV:2 | 0 |

The `P324...P385` frame remains the strongest formula-family candidate. It spans several lengths, so it is better treated as a frame with variable interior structure than as a fixed formula.

## Single-Slot Candidates

| Context | Slot | Alternating Signs | Pair Count | Examples |
| --- | ---: | --- | ---: | --- |
| `P324 _ </s>` | 1 | `P095;P265;P368` | 3 | `M-150~M-180;M-150~M-182;M-180~M-182` |
| `P086 _ </s>` | 1 | `P123;P126` | 1 | `M-178~M-179` |
| `P324 _ P210` | 1 | `P117;P215` | 1 | `M-14~M-58` |

These are not allograph claims — an allograph being two shapes treated as the same sign. They are candidate variable slots for future testing.

## Counterresult

The variant evidence is structurally useful but weak:

- Most exact sequence recurrence is absent.
- Many near-pairs are very short strings, where accidental similarity is easier.
- Shared edge frames can be produced by common initial and terminal signs.
- The first null model shows the apparent variant-pair excess is strong under a loose length/frequency shuffle but mostly disappears when first and last sign positions are preserved.
- The top `P324...P385` frame is ordinary under the edge-position preserving null: observed 10 rows versus null mean 9.612 and median 10.
- The entire set remains scoped to unicorn seals.
- Images and authoritative sign-list validation have not been checked.

## Result

This probe supports only this claim:

```text
The strict Mayig-policy subset contains a review queue of near-duplicate sequences, edge-frame families, and single-slot variants suitable for future duplicate/formula testing.
```

After the null-model screen, the queue should be treated as edge-conditioned review material, not independent semantic evidence.

It does not support:

- Accepted duplicate interpretation.
- Allograph or sign-equivalence claims.
- Semantic slots.
- Phonetic values.
- Translation.

## Next Falsification

The next tests should ask:

- Does the exact duplicate `M-32/M-177` survive raw numeric, image, and catalog validation?
- Do the single-slot candidates remain unusual under edge-position preserving, length-split null models?
- Do the frame families survive outside unicorn seals?
- Do duplicates or near-duplicates correlate with seal imagery, findspot, or administrative context in an authoritative corpus?
- Do variable slots predict anything not used to create them?
