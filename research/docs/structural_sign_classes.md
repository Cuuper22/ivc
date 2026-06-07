# Structural Sign Classes

Date: 2026-05-24

## Purpose

This experiment converts the order signal into provisional structural sign classes.

It does not assign meaning. It does not identify phonetic values. It does not translate. It only asks which signs behave like initial operators, medial/core signs, terminal operators, distributed recurrent signs, or sparse unclassified signs in the strict prototype subset.

## Local Artifacts

```text
data/open_prototype/reports/structural_sign_profiles.csv
data/open_prototype/reports/structural_priority_sign_profiles.csv
data/open_prototype/reports/structural_class_summary.csv
data/open_prototype/reports/structural_class_summary.json
```

Source file:

```text
data/open_prototype/reports/sign_policy_sensitivity_sequences.csv
```

Dataset:

```text
eligible_records: 136
tokens: 739
policies_analyzed: raw_lipi_numeric, p385_merge_only, mayig_observed_parpola
```

## Classification Rules

Minimum evidence threshold:

```text
token_count >= 5
```

Rules:

| Class | Rule |
| --- | --- |
| `initial_operator_candidate` | Token count >= 5, initial share >= 0.6, terminal share <= 0.2. |
| `terminal_operator_candidate` | Token count >= 5, terminal share >= 0.6, initial share <= 0.2. |
| `medial_core_candidate` | Token count >= 5, medial share >= 0.75. |
| `edge_bivalent_candidate` | Token count >= 5, initial+terminal share >= 0.65, both initial and terminal >= 0.2. |
| `distributed_recurrent_candidate` | Token count >= 10 and no position share >= 0.6. |
| `sparse_unclassified` | Token count < 5. |

These are mechanical structural labels. They are meant to produce a review queue, not to settle grammar.

## Class Counts

| Policy | Sparse | Medial/core | Initial | Terminal | Distributed | Weak/mixed |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `raw_lipi_numeric` | 149 | 25 | 4 | 4 | 2 | 5 |
| `p385_merge_only` | 149 | 25 | 4 | 3 | 2 | 5 |
| `mayig_observed_parpola` | 122 | 26 | 5 | 3 | 2 | 2 |

The `mayig` policy has fewer sparse signs because the Parpola-style inventory collapses more numeric distinctions.

## Priority Structural Profiles

### Initial Candidates

| Policy | Sign | Tokens | Initial | Medial | Terminal | Class |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `raw_lipi_numeric` | `L740` | 73 | 0.821918 | 0.178082 | 0.000000 | `initial_operator_candidate` |
| `mayig_observed_parpola` | `P324` | 76 | 0.789474 | 0.210526 | 0.000000 | `initial_operator_candidate` |
| `mayig_observed_parpola` | `P217` | 15 | 0.933333 | 0.000000 | 0.066667 | `initial_operator_candidate` |
| `mayig_observed_parpola` | `P013` | 8 | 1.000000 | 0.000000 | 0.000000 | `initial_operator_candidate` |

Interpretation:

`740/P324` is the dominant initial-operator candidate in this subset. It is not exclusively initial, so the counterevidence is the roughly 0.18 to 0.21 medial share.

### Medial/Core Candidates

| Policy | Sign | Tokens | Initial | Medial | Terminal | Class |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `raw_lipi_numeric` | `L002` | 60 | 0.000000 | 1.000000 | 0.000000 | `medial_core_candidate` |
| `mayig_observed_parpola` | `P122` | 59 | 0.000000 | 1.000000 | 0.000000 | `medial_core_candidate` |
| `raw_lipi_numeric` | `L220` | 29 | 0.034483 | 0.965517 | 0.000000 | `medial_core_candidate` |
| `mayig_observed_parpola` | `P050` | 27 | 0.037037 | 0.962963 | 0.000000 | `medial_core_candidate` |
| `raw_lipi_numeric` | `L032` | 21 | 0.000000 | 0.904762 | 0.095238 | `medial_core_candidate` |
| `mayig_observed_parpola` | `P145` | 22 | 0.000000 | 0.909091 | 0.090909 | `medial_core_candidate` |

Interpretation:

`002/P122`, `220/P050`, and `032/P145` are strong medial/core candidates. This supports using them in future formula-structure tests, but not semantic assignment.

### Terminal Candidates

| Policy | Sign | Tokens | Initial | Medial | Terminal | Class |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `raw_lipi_numeric` | `L817` | 12 | 0.000000 | 0.083333 | 0.916667 | `terminal_operator_candidate` |
| `raw_lipi_numeric` | `L861` | 12 | 0.000000 | 0.166667 | 0.833333 | `terminal_operator_candidate` |
| `p385_merge_only` | `P385` | 24 | 0.000000 | 0.125000 | 0.875000 | `terminal_operator_candidate` |
| `mayig_observed_parpola` | `P385` | 25 | 0.000000 | 0.120000 | 0.880000 | `terminal_operator_candidate` |
| `mayig_observed_parpola` | `P256` | 9 | 0.000000 | 0.222222 | 0.777778 | `terminal_operator_candidate` |
| `mayig_observed_parpola` | `P011` | 8 | 0.000000 | 0.375000 | 0.625000 | `terminal_operator_candidate` |

Interpretation:

The `817`/`861 -> P385` cluster is structurally coherent as a terminal candidate. This strengthens the review priority for that allograph/merge question. It still does not validate the merge.

### Distributed Recurrent Candidates

| Policy | Sign | Tokens | Initial | Medial | Terminal | Class |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `raw_lipi_numeric` | `L390` | 25 | 0.520000 | 0.440000 | 0.040000 | `distributed_recurrent_candidate` |
| `mayig_observed_parpola` | `P086` | 29 | 0.517241 | 0.448276 | 0.034483 | `distributed_recurrent_candidate` |
| `raw_lipi_numeric` | `L820` | 14 | 0.142857 | 0.285714 | 0.571429 | `distributed_recurrent_candidate` |
| `mayig_observed_parpola` | `P378` | 14 | 0.142857 | 0.285714 | 0.571429 | `distributed_recurrent_candidate` |

Interpretation:

`390/P086` is not a simple initial or medial sign despite being frequent. It may be doing something more flexible, or this subset may be mixing contexts that need finer structural separation. This sign deserves caution before semantic interpretation.

## Result

The strict subset yields a first structural grammar scaffold:

- A dominant initial candidate: `740/P324`.
- Strong medial/core candidates: `002/P122`, `220/P050`, `032/P145`.
- A coherent terminal candidate cluster: `817/861/P385`.
- A distributed recurrent sign: `390/P086`.

## Counterresult

The scaffold is narrow and mechanical:

- It is based only on Mohenjo-daro seal rows in the strict subset.
- It uses position only, with neighbor summaries as supporting context.
- It does not include images.
- It does not include an authoritative accepted crosswalk.
- It does not test artifact classes beyond `SEAL:S`.
- It does not assign meanings.

## Interpretation Boundary

This supports only this claim:

```text
The strict prototype subset contains stable positional sign behavior sufficient to define provisional structural classes.
```

It does not support:

- Semantic categories.
- Linguistic readings.
- Phonetic readings.
- Accepted allograph policy.
- Translation.

## Next Falsification

The next tests should ask:

- Do these classes survive the 12 sensitivity-flag count matches?
- Do they survive manual collation of the 29 mismatch rows?
- Do they survive an authoritative corpus beyond the open `mayig` subset?
- Do they predict held-out neighbors better than frequency alone?
- Do they predict iconography, artifact class, or duplicate behavior without overfitting?

