# Sensitivity Formula Probe

Date: 2026-05-24

## Purpose

This note records a check on the project's own exclusion rule. Twelve inscriptions were kept out of the clean working set. The question here is whether keeping them out was worth doing, or merely cautious.

Terms first. The "scaffold" is the observed tendency for certain signs to sit at the start of a row (`I`, initial) and others at the end (`T`, terminal), giving an `I...T` frame. "Sensitivity flags" mark rows with something that could swing a result: an unknown or damaged sign, or a compound sign written with a slash. The "strict subset" is the flag-free working set. `lipi` and `mayig` are the two independent sign catalogs the project reads; a "policy" is a chosen rule for turning a catalog row into a sequence of sign tokens.

This experiment stress-tests the structural and formula scaffold against the 12 count-matching rows that were excluded from the strict subset because they carry sensitivity flags.

It does not try to rescue those rows into the clean baseline. It asks whether their behavior is compatible with the strict-row scaffold, and which flags damage the scaffold most.

## Local Artifacts

```text
data/open_prototype/reports/sensitivity_formula_sequences.csv
data/open_prototype/reports/sensitivity_formula_summary.csv
data/open_prototype/reports/sensitivity_formula_by_flag.csv
data/open_prototype/reports/sensitivity_formula_summary.json
```

Source files:

```text
data/open_prototype/reports/mismatch_audit.csv
data/open_prototype/reports/structural_sign_profiles.csv
```

Input rows:

```text
candidate_with_sensitivity_flag: 12
tokens_per_policy: 84
policies_analyzed: raw_lipi_numeric, p385_merge_only, mayig_observed_parpola
```

## Tokenization Policy

The tokenization is deliberately conservative:

- Lipi slash compounds are split into separate numeric signs.
- Lipi `000` unknown groups are removed from Lipi-derived policies to match the audited `lipi_signs` count.
- Mayig `P000` unknown graphemes are preserved as `missing_profile` tokens.

This means Lipi and Mayig rows are not being forced into the same behavior. The disagreement is part of the result.

## Summary

| Policy | Rows | Tokens | Rows With Missing Profile | Missing Profile Share | I at Start | T at End | I...T Scaffold | Exact Recurrence |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `raw_lipi_numeric` | 12 | 84 | 8 | 0.130952 | 4 | 2 | 0 | 0 |
| `p385_merge_only` | 12 | 84 | 8 | 0.130952 | 4 | 2 | 0 | 0 |
| `mayig_observed_parpola` | 12 | 84 | 11 | 0.190476 | 8 | 2 | 1 | 0 |

Null controls — what the same counts look like after the signs are shuffled, so any real scaffold has to beat them:

```text
raw_lipi_numeric_I_at_start_shuffle_mean: 2.22
raw_lipi_numeric_T_at_end_shuffle_mean: 0.44
raw_lipi_numeric_I_T_scaffold_shuffle_mean: 0.09
mayig_I_at_start_shuffle_mean: 1.86
mayig_T_at_end_shuffle_mean: 0.90
mayig_I_T_scaffold_shuffle_mean: 0.33
```

## Strict Comparison

The sensitivity rows do not behave like a clean extension of the strict subset.

Strict subset:

```text
raw_lipi_numeric_I_T_scaffold: 22 of 136
mayig_observed_parpola_I_T_scaffold: 23 of 136
raw_lipi_numeric_recurrent_exact_coverage: 0.169118
mayig_observed_parpola_recurrent_exact_coverage: 0.301471
```

Sensitivity rows:

```text
raw_lipi_numeric_I_T_scaffold: 0 of 12
mayig_observed_parpola_I_T_scaffold: 1 of 12
raw_lipi_numeric_recurrent_exact_coverage: 0
mayig_observed_parpola_recurrent_exact_coverage: 0
```

The only Mayig `I...T` sensitivity row is `M-167`, with pattern `IUT`: `P324 P000 P385`. It contains an unknown `P000` in the middle, so it is not a strong formula confirmation.

## Flag Behavior

### Lipi Slash Compounds

Rows:

```text
M-165; M-23; M-67; M-68; M-79
```

Under raw Lipi-derived policies, no slash-compound row starts with an `I` class. Under Mayig, all 5 start with `I`.

This is a real cross-source disagreement. It likely reflects segmentation or ordering policy around slash compounds, not a linguistic phenomenon. These rows must stay outside the strict structural baseline until the slash notation is manually resolved.

### Lipi Unknown Zero

Rows:

```text
M-125; M-167; M-169
```

After removing `000` groups, raw Lipi-derived policies have only 1 missing-profile token across 11 analyzed tokens. The Mayig policy preserves `P000`, producing 3 missing-profile tokens across the same rows.

These rows are usable only as a sensitivity set, because unknown signs can create artificial edge scaffolds or erase them.

### Mayig Unknown P000

Rows:

```text
M-125; M-167; M-169; M-176; M-28; M-49; M-50
```

The Mayig policy has missing-profile tokens in all 7 rows with this flag. The missing-profile share is 0.225 for Mayig, compared with 0.075 for Lipi-derived policies on the same flagged group.

This shows that `P000` rows cannot be used to validate Parpola-side structural formulas.

## Result

The 12 sensitivity rows are useful as a stress test, but they do not strengthen the formula scaffold.

They support this claim:

```text
The strict gating — the rule that admits only flag-free rows — is doing real work: sensitivity-flag rows introduce missing profiles, cross-source class disagreement, and no recurrent exact formula patterns.
```

They do not support:

- Expanding the strict structural baseline.
- Accepting slash-compound segmentation.
- Validating `P000` rows.
- Semantic reading.
- Phonetic reading.
- Translation.

## Next Falsification

The next tests should ask:

- Can manual collation resolve the 5 slash-compound rows into a stable sign order?
- Does `M-167` remain an `I...T` frame after image-level handling of `P000`?
- Do the 29 count-mismatch rows show the same kinds of failure, or a different failure mode?
- Does an authoritative corpus encode slash compounds and unknown signs with more precise uncertainty markers?
