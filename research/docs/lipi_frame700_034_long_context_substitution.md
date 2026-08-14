# Lipi FRAME700 034 Long Context Substitution

Date: 2026-05-25

## Question

This note tries to break a tempting idea. FRAME700 is the project's label for short inscription rows built on sign `700`, such as `+700-034+`. Objects carrying such a short row usually also carry a longer row on another side. The tempting idea is that the sign code `034` keeps particular company on that longer side. The question: does `034` carry a stable longer-side context signal against its matched `033` and `032` controls — the closely comparable objects carrying the other two codes?

This attack is deliberately source-blind and adversarial. Inside each matched triad — a set of three objects, one per sign code — it shuffles the three longer-side contexts across the `034`, `033`, and `032` labels. That shuffle is the null model: a deliberately meaningless version of the data that shows how large an apparent effect chance alone produces. If a longer-side token or exact family is really attached to `034` in the current planning layer, it should survive this within-triad substitution pressure.

## Outputs

```text
data/open_prototype/tools/lipi_frame700_034_long_context_substitution.mjs
data/open_prototype/reports/lipi_frame700_034_long_context_token_tests.csv
data/open_prototype/reports/lipi_frame700_034_long_context_family_tests.csv
data/open_prototype/reports/lipi_frame700_034_long_context_scope_rows.csv
data/open_prototype/reports/lipi_frame700_034_long_context_substitution_summary.json
```

Inputs:

```text
data/open_prototype/reports/lipi_frame700_034_source_triad_packet.csv
data/open_prototype/reports/lipi_frame700_034_matched_contrast_stability.csv
data/open_prototype/reports/lipi_frame700_034_two_lane_source_packet.csv
```

## Method

Scopes:

| Scope | Triads |
| --- | ---: |
| `all_triads` | 93 |
| `strong_local_contrasts` | 13 |
| `independent_low_copy` | 4 |
| `two_lane_core` | 8 |
| `repeated_branch_optional` | 1 |

For each scope, the probe tests:

```text
long-side token sets
exact long-side token families
```

Null:

```text
shuffle the three longer-side contexts within each triad across 034/033/032 labels
iterations: 5000
```

Observed score:

```text
034 hits - mean(033 hits, 032 hits)
```

## Result

```text
token tests: 75
family tests: 27
corrected token tests: 0
corrected family tests: 0
accepted decipherment claims: 0
```

Top uncorrected all-triad token:

```text
candidate: 060
hit_034: 6
hit_033: 0
hit_032: 1
observed_delta: 5.5
p_ge: 0.0068
BH q: 0.077067
```

Top uncorrected all-triad exact family:

```text
candidate: 002;416;861
hit_034: 5
hit_033: 0
hit_032: 0
observed_delta: 5
p_ge: 0.0046
BH q: 0.069000
```

Neither survives correction.

## Why This Matters

The old `002;416;861` branch is visible, but it is still copy/repetition pressured:

```text
H-910   high repetition, optional repeated-branch packet
H-2094  high repetition
H-2097  high repetition
H-2096  high repetition
H-2095  high repetition
```

This keeps the old branch useful as a stress check, not as first evidence.

The `060` token is more interesting because it is not the same old branch, but it also fails correction and is mostly moderate-pressure material:

```text
H-1845
H-1138
H-1824
H-1846
H-351
H-823
```

Only `H-1824` is already in the two-lane core packet. That makes `060` a source-check note for the local contrast lane — a lane being one of the separate evidence tracks the project runs, kept apart so a result in one does not lean on the other — not a new claim.

## Consequence

This is another useful negative result. The current data do not support saying that `034` has a stable longer-side token or exact-family association.

Future long-context evidence has to pass all four gates. A gate is a checkpoint the evidence must pass before the next step is allowed:

| Gate | Requirement |
| --- | --- |
| Source link | Same physical object and side relation are source-confirmed. |
| Direction/sign safety | `034` is visually separable from `033`/`032`, and `FRAME700` order is not a mirror or drawing convention artifact. |
| Copy control | The association appears in at least two independent object/copy families. |
| Matched contrast | Matched `033`/`032` controls with comparable object format do not share the same longer-side family at comparable rates. |

Operational labels for future source coding:

```text
independent_context_evidence
object_format_context_leakage
copy_family_context_leakage
catalog_relation_unusable
sign_identity_unusable
```

The live state is narrower:

```text
034 remains a source-targeted distributional residue inside the FRAME700 tablet side-mark system.
```

A residue here is a leftover pattern that has survived the controls run so far, without being explained.

The next evidence must come from source images filling the two-lane coding sheet, not from broadening the long-context story.

Boundary:

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted language assignments: 0
accepted administrative values: 0
```
