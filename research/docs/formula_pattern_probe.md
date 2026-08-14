# Formula Pattern Probe

Date: 2026-05-24

## Purpose

This note records a probe — a narrow, cheap experiment run to see whether a bigger question is worth pursuing.

An earlier pass sorted signs into provisional structural classes by where they tend to sit in an inscription: openers, middles, closers, and so on. This probe asks the next question. Do those classes combine into repeated whole-inscription patterns — formulas, in the sense of a fixed shape reused across many objects?

It does not assign meaning. It does not identify grammar in a linguistic sense. It does not translate. It only tests whether the strict prototype subset — the small, tightly filtered slice of inscriptions we allow into early experiments — has repeatable class scaffolds beyond individual sign-position profiles. A scaffold here is the pattern of class codes across a whole row, such as an opener class at the start and a closer class at the end.

## Local Artifacts

```text
data/open_prototype/reports/formula_pattern_sequences.csv
data/open_prototype/reports/formula_pattern_counts.csv
data/open_prototype/reports/formula_anchor_pairs.csv
data/open_prototype/reports/formula_class_transition_counts.csv
data/open_prototype/reports/formula_pattern_summary.csv
data/open_prototype/reports/formula_pattern_summary.json
```

Source files:

```text
data/open_prototype/reports/sign_policy_sensitivity_sequences.csv
data/open_prototype/reports/structural_sign_profiles.csv
```

Dataset. A policy here is one rule for deciding which sign shapes count as the same sign; different policies merge different variants:

```text
records_per_policy: 136
tokens_per_policy: 739
policies_analyzed: raw_lipi_numeric, p385_merge_only, mayig_observed_parpola
excluded_policies: provisional_high_map, provisional_high_medium_map
```

The excluded policies have sequence outputs but no structural sign-profile table, so they are not valid inputs for class-pattern analysis.

## Class Codes

| Code | Class |
| --- | --- |
| `I` | `initial_operator_candidate` |
| `M` | `medial_core_candidate` |
| `T` | `terminal_operator_candidate` |
| `D` | `distributed_recurrent_candidate` |
| `E` | `edge_bivalent_candidate` |
| `W` | `weak_or_mixed_positional_candidate` |
| `S` | `sparse_unclassified` |

## Method

For each strict-row sequence:

1. Map each sign to its structural class under the selected policy.
2. Convert classes to compact codes.
3. Record the exact class pattern, collapsed run pattern, first and last class, and first and last sign.
4. Compare observed edge scaffolds against reversed order and 100 deterministic within-row shuffles.

The shuffle control preserves each inscription's multiset of class labels but randomizes their internal order. This is a control for whether edge scaffolds are merely caused by class abundance.

## Summary

| Policy | Exact Patterns | Recurrent Exact Coverage | Collapsed Coverage | Initial at Start | Terminal at End | I...T Scaffold | Shuffle I...T Mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `raw_lipi_numeric` | 123 | 0.169118 | 0.617647 | 87 | 33 | 22 | 1.25 |
| `p385_merge_only` | 123 | 0.169118 | 0.617647 | 87 | 33 | 22 | 1.26 |
| `mayig_observed_parpola` | 113 | 0.301471 | 0.691176 | 92 | 34 | 23 | 1.25 |

Reversed controls:

```text
raw_lipi_numeric_initial_at_start_reversed: 1
raw_lipi_numeric_terminal_at_end_reversed: 0
raw_lipi_numeric_I_T_scaffold_reversed: 0
p385_merge_only_initial_at_start_reversed: 1
p385_merge_only_terminal_at_end_reversed: 0
p385_merge_only_I_T_scaffold_reversed: 0
mayig_initial_at_start_reversed: 1
mayig_terminal_at_end_reversed: 0
mayig_I_T_scaffold_reversed: 0
```

Shuffle controls:

```text
raw_lipi_numeric_initial_at_start_shuffle_mean: 19.25
raw_lipi_numeric_terminal_at_end_shuffle_mean: 7.22
raw_lipi_numeric_I_T_scaffold_shuffle_mean: 1.25
p385_merge_only_initial_at_start_shuffle_mean: 19.90
p385_merge_only_terminal_at_end_shuffle_mean: 7.33
p385_merge_only_I_T_scaffold_shuffle_mean: 1.26
mayig_initial_at_start_shuffle_mean: 20.68
mayig_terminal_at_end_shuffle_mean: 7.69
mayig_I_T_scaffold_shuffle_mean: 1.25
```

## Pattern Result

The class scaffolds are direction-sensitive:

- `I` signs appear at the start far more often in observed order than in reversed or shuffled controls.
- `T` signs appear at the end far more often in observed order than in reversed or shuffled controls.
- Full `I...T` scaffolds appear in 22 to 23 rows, versus about 1.25 under within-row shuffling.

This supports an A2 structural claim — our claim tier for statements about structure only, never meaning: the strict subset has edge-position scaffolding that is stronger than a class-abundance artifact.

## Counterresult

Exact formula recurrence is still weak.

In raw numeric and isolated `P385` policies, only 10 exact class patterns recur, covering 0.169118 of rows. The `mayig` policy has 18 recurrent exact patterns covering 0.301471 of rows, partly because the Parpola-style inventory collapses more distinctions.

The most common exact patterns are small:

```text
raw_lipi_numeric_top_exact: IS:4; IMMMT:3; DM:2; DMMSS:2
p385_merge_only_top_exact: IS:4; IMMMT:3; DM:2; DMMSS:2
mayig_top_exact: IMMMT:4; IS:4; IMMM:3; DM:2
```

Collapsed class patterns recur more, but that is expected when long medial runs are collapsed. Collapsed recurrence is useful for triage, not for semantic interpretation.

## Anchor Pairs

The strongest edge anchor pair under the merged/Parpola policies is the same structural frame:

```text
raw_lipi_numeric: L740...L817 in 6 rows and L740...L861 in 4 rows
p385_merge_only: L740...P385 in 10 rows
mayig_observed_parpola: P324...P385 in 10 rows
```

This strengthens the priority of the `817/861 -> P385` review question, because the merge produces one repeated edge frame without changing the underlying row set.

Other repeated edge frames remain smaller:

```text
mayig_observed_parpola: P086...P385 in 4 rows
mayig_observed_parpola: P324...P256 in 3 rows
raw_lipi_numeric: L740...L692 in 3 rows
raw_lipi_numeric: L740...L820 in 3 rows
```

## Interpretation Boundary

This supports only this claim:

```text
The strict prototype subset contains directional edge-class scaffolding, especially initial-to-terminal frames involving 740/P324 and 817/861/P385.
```

It does not support:

- A translated formula.
- A semantic reading of `740`, `817`, `861`, or `P385`.
- A phonetic reading.
- An accepted sign merge.
- A corpus-wide grammar.

## Next Falsification

The next tests should ask:

- Do the `740...817/861` and `P324...P385` frames survive image-level validation?
- Do they survive the 12 sensitivity-flag count matches? First answer: not cleanly; see [Sensitivity formula probe](sensitivity_formula_probe.md).
- Do they survive manual collation of the 29 mismatch rows?
- Do they produce near-duplicate or variable-slot families? First review queue: [Formula variant probe](formula_variant_probe.md).
- Are these frames tied to iconography, artifact subtype, or duplicate behavior? The first metadata answer is that the open Mayig subset contains only unicorn seal descriptions; see [Metadata scope probe](metadata_scope_probe.md).
- Are the same frames present outside Mohenjo-daro `SEAL:S` rows in an authoritative corpus?
