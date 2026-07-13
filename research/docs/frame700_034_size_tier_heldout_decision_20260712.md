# `FRAME700 034` held-out size-tier decision

Date: 2026-07-12 America/Los_Angeles

## Question

Does short-mark subtype `034` identify a reproducible smaller-object, numerical, metrological, or administrative-size tier beyond copied formula and object-format families?

Pre-registered target:

```text
034 versus pooled 032/033
```

The test uses one vote per artifact, requires positive horizontal and vertical measurements, holds the whole H-2218 through H-2239 series out as one source family, and holds repeated longer-text families out together. The dimension model sees only log horizontal and vertical size. It is compared with an administrative-format model, an emblem/formula model, and two matched label-shuffle nulls.

## Result

Gate: **FAIL**.

Decision: `CLOSE_034_OBJECT_SIZE_OR_METROLOGICAL_TIER_UNDER_CURRENT_LOCAL_EVIDENCE`.

| Measure | Dimension target | Administrative-format baseline | Emblem/formula baseline |
| --- | ---: | ---: | ---: |
| Eligible artifacts | 309 | 309 | 309 |
| Held-out source families | 216 | 216 | 216 |
| ROC AUC | 0.701087 | 0.643416 | 0.518200 |
| Balanced accuracy | 0.661207 | 0.606880 | 0.556579 |
| `034` recall | 0.756757 | 0.486486 | 0.774775 |

Grouped-bootstrap results:

| Quantity | 95% interval | Gate |
| --- | --- | --- |
| Dimension AUC | [0.606806, 0.789030] | passes chance floor |
| Dimension minus administrative-format AUC | [-0.010581, 0.134992] | **fails** positive-margin requirement |
| Dimension minus emblem/formula AUC | [0.057127, 0.293354] | passes |

Matched-null results:

| Null | AUC mean | AUC p95 | Null AUC >= observed |
| --- | ---: | ---: | ---: |
| Administrative-format label shuffle | 0.597158 | 0.654323 | 0.001500 |
| Emblem/copy-family label shuffle | 0.616055 | 0.662687 | 0.001000 |

The size association is therefore not imaginary. Across the full grouped sample, `034` artifacts are smaller on average and the dimension model beats both matched shuffles. Median area is 101.25 mm² for `034`, 117.15 mm² for `033`, and 146.85 mm² for `032`.

But the association does not identify a `034` tier. The cleanest family holdout is decisive:

| H-2218 through H-2239 holdout | Result |
| --- | ---: |
| Rows | 22 |
| True `034` | 21 |
| True `033` | 1 |
| `034` recall | 1.000000 |
| Non-`034` specificity | 0.000000 |
| ROC AUC | 0.476190 |

Trained without this series, the dimension model called all 22 small tablets `034`, including the `H-2238` `033` control. It recognized the series' small form factor, not the short-mark subtype.

## Interpretation

What survives:

- `034` is associated with smaller multi-side Harappa objects in the current Lipi planning layer.
- That association is stronger than random label placement under the two matched shuffles.
- Small-object format remains a useful source/corpus confound for future `034` work.

What fails:

- Size does not discriminate `034` from its `033` sibling inside the completely held-out H-series.
- The dimension model does not beat the administrative-format baseline by a positive grouped-bootstrap margin.
- No ordered quantity, numerical value, measurement unit, commodity class, or metrological tier follows.

The result closes the current “`034` means a smaller tier” route. It does not erase the separate source-visible graphic and distributional questions around `032/033/034`; it says physical size cannot currently supply their semantics.

## Raw outputs

- `research/data/open_prototype/reports/frame700_034_size_tier_heldout_20260712_summary.json`
- `research/data/open_prototype/reports/frame700_034_size_tier_heldout_20260712_predictions.csv`
- `research/data/open_prototype/reports/frame700_034_size_tier_heldout_20260712_null_iterations.csv`
- `research/data/open_prototype/tools/frame700_034_size_tier_heldout_20260712.mjs`
