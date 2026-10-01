# Lipi FRAME700 Subtype Discrimination

Date: 2026-05-24

## Question

This note tests whether three sign codes that appear in the same short row are doing the same job or different ones. FRAME700 is the project's label for short inscription rows built on sign `700`, such as `+700-032+`. If `032`, `033`, and `034` were interchangeable, the objects carrying each of them should look alike; if they are different choices, the objects should differ in kind, size, or context. The question: inside short-side `+700-032+`, `+700-033+`, and `+700-034+` contexts, are `032`, `033`, and `034` interchangeable fillers, or do they occupy different object/context environments?

This is a direct functional-distributional attack. It is not a phonetic reading, sign meaning, number, measure, commodity, or translation.

## Local Artifacts

```text
data/open_prototype/tools/lipi_frame700_subtype_discrimination.mjs
data/open_prototype/reports/lipi_frame700_subtype_rows.csv
data/open_prototype/reports/lipi_frame700_subtype_predictions.csv
data/open_prototype/reports/lipi_frame700_subtype_prediction_summary.csv
data/open_prototype/reports/lipi_frame700_subtype_feature_contrasts.csv
data/open_prototype/reports/lipi_frame700_subtype_summary.json
```

Inputs:

```text
data/open_prototype/reports/lipi_short_mark_companion_context_rows.csv
data/open_prototype/reports/lipi_multiside_mark_validation_queue.csv
```

## Scope

```text
target_rows: 353
unique_artifacts: 352
h_series_rows: 22
no_h_series_rows: 331
sequence_family_keys: 287
```

Subtype counts:

| Scope | `032` | `033` | `034` |
| --- | ---: | ---: | ---: |
| All `FRAME700` subtype rows | 102 | 137 | 114 |
| Excluding H-2218 through H-2239 | 102 | 136 | 93 |

Context counts:

```text
single_longer_text: 233
all_short_or_no_longer_text: 62
single_short_no_longer_text: 53
multiple_longer_texts: 5
```

## Method

The target is the companion subtype only:

```text
032 vs 033 vs 034
```

The script preserves exact short-side order as a feature:

```text
+700-033+ is not silently merged with +033-700+
```

Prediction is leave-one-artifact-out by `cisi` — each object is predicted by a model trained without it. A stricter sequence-family leaveout also removes training rows sharing the same current sequence-family key, so the model cannot succeed by memorizing a near-identical inscription. Models are simple categorical naive Bayes so the failure modes are inspectable:

| Model | Features |
| --- | --- |
| Frequency | subtype prior only |
| Object | type, site, sides |
| Dimensions | horizontal bin, vertical bin, area bin, aspect bin, thickness bin |
| Side context | side index, `700` order, context class, side relation, longer-row count |
| Long-text family | longer-side token set, edge frame, first/last tokens, length bin |
| Combined no exact long | object, dimensions, side context, long edge/length/token-presence features |
| Combined with exact long | combined model plus exact longer-side family features |

Strict numeric parsing is used. Zero and non-positive dimensions are treated as missing; ranges are rejected.

## Prediction Result

The strongest model is dimensions, not exact long-side family.

| Scope | Leaveout | Best Model | Top-1 | Top-2 | Median Rank |
| --- | --- | --- | ---: | ---: | ---: |
| All rows | artifact | Dimensions | 0.475921 | 0.821530 | 2 |
| All rows | sequence family | Dimensions | 0.470255 | 0.815864 | 2 |
| Excluding H-series | artifact | Dimensions | 0.441088 | 0.815710 | 2 |
| Excluding H-series | sequence family | Dimensions | 0.435045 | 0.806647 | 2 |

Baseline comparison, excluding H-2218 through H-2239 with sequence-family leaveout:

| Model | Top-1 | Top-2 | `032` Top-1 | `033` Top-1 | `034` Top-1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Frequency | 0.410876 | 0.719033 | 0.000000 | 1.000000 | 0.000000 |
| Dimensions | 0.435045 | 0.806647 | 0.303922 | 0.367647 | 0.677419 |
| Object | 0.371601 | 0.752266 | 0.000000 | 0.904412 | 0.000000 |
| Long-text family | 0.287009 | 0.595166 | 0.254902 | 0.286765 | 0.322581 |
| Combined no exact long | 0.344411 | 0.782477 | 0.362745 | 0.169118 | 0.580645 |

The important point is not raw top-1. The dimension model is only modestly above the prior baseline, but it breaks the prior's fake certainty that every row is `033`. Its strongest stable branch is `034`.

## Feature Contrasts

After removing H-2218 through H-2239:

| Feature | Value | Subtype | In-Subtype | Other Subtypes | Lift |
| --- | --- | --- | ---: | ---: | ---: |
| long edge frame | `002...416` | `034` | 5/93 | 0/238 | undefined |
| horizontal bin | `h_10_13` | `034` | 20/93 | 18/238 | 2.843489 |
| long token set | `176;400;740` | `033` | 19/136 | 11/195 | 2.476604 |
| vertical bin | `v_ge_10` | `032` | 30/102 | 29/229 | 2.322515 |
| context class | `all_short_or_no_longer_text` | `034` | 18/93 | 22/238 | 2.093842 |

This does not establish a three-way grammar. It says `034` still behaves differently enough to stay alive as a broader functional subtype candidate after the H-series is removed. `033` has a repeated `+400-740-176+` longer-text association, but exact long-family prediction collapses under sequence-family leaveout, so that branch is probably copy/family-heavy until source validation says otherwise. `032` remains weaker and may be a control/residual branch — useful as a comparison case rather than a positive function.

## Current Read

The previous codebook result showed a strong but narrow H-series side-role system. This experiment attacks the broader `700 + 03x` slot.

Result:

```text
034 remains the best broad candidate for a distributional subtype.
033 has a family-heavy association with +400-740-176+.
032 is not yet functionally resolved.
Exact long-text family is not a robust predictor once sequence-family leakage is controlled.
The best surviving predictor is object dimension bins, so object/form-factor explanation remains live.
```

## Kill Conditions

- Source-grade images collapse `032/033/034` into allographs, damage, mirroring, or transcription policy.
- `+700-X+` versus `+X-700+` turns out to be only catalog/image direction convention.
- The `034` dimension/context split vanishes after source-validated side checks.
- The `033` association with `+400-740-176+` is fully explained by duplicate/copy family.
- A blocked permutation preserving type, sides, `700` order, and sequence family matches the dimension-model gain. Such a permutation is a null model: a deliberately meaningless version of the data that shows how much apparent skill chance alone produces.

Blocked-null status: executed in [Lipi FRAME700 subtype blocked null](lipi_frame700_subtype_blocked_null.md). The overall dimension-model gain is weak and nearly matched by the harshest relation-preserving null, but the `034` recall residue survives the tested blocked shuffles.

## Boundary

No numerical value, metrological reading, semantic reading, sign meaning, phonetic value, language identity, or translation is accepted from this experiment.
