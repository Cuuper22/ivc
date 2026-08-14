# `FRAME700 034` held-out size-tier decision

Date: 2026-07-12 America/Los_Angeles

## What this is and why it exists

`032`, `033`, and `034` are short marks made of vertical strokes, and they differ mainly in how many strokes there are. A natural guess is that they are quantities. If so, the objects carrying them might sort by physical size, and `034` would mark a distinct tier of smaller objects. This note tests that guess and reports that it fails.

The test is held out, which means the model is trained on some objects and then judged only on objects it never saw. That matters because the corpus is full of near-duplicates. Many Harappa tablets were copied from the same formula and made in the same format, so a model can score well by recognizing a batch of similar objects rather than by learning anything about the mark. Holding whole families out is what separates those two explanations.

## Question

Does short-mark subtype `034` identify a reproducible smaller-object, numerical, metrological, or administrative-size tier beyond copied formula and object-format families?

Pre-registered target, meaning the comparison was fixed in advance so the result could not be chosen after seeing the numbers:

```text
034 versus pooled 032/033
```

The test counts one vote per artifact, so a heavily duplicated object cannot vote many times. It requires positive horizontal and vertical measurements. It holds the whole H-2218 through H-2239 series out together as one source family, and likewise holds repeated longer-text families out together. The dimension model is deliberately blinkered: it sees only log horizontal and vertical size, nothing else. It is scored against an administrative-format model, an emblem/formula model, and two matched nulls built by shuffling the labels, which show what a given score looks like when the labels carry no information at all.

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

ROC AUC is the chance that the model ranks a true `034` artifact above a non-`034` one; 0.5 is coin-flip.

Grouped-bootstrap results, where the resampling is done by source family rather than by artifact so that copied objects cannot inflate the apparent precision:

| Quantity | 95% interval | Gate |
| --- | --- | --- |
| Dimension AUC | [0.606806, 0.789030] | passes chance floor |
| Dimension minus administrative-format AUC | [-0.010581, 0.134992] | **fails** positive-margin requirement |
| Dimension minus emblem/formula AUC | [0.057127, 0.293354] | passes |

The second row is the one that decides the gate. The interval for the dimension model's margin over the administrative-format baseline includes zero, so a margin of zero cannot be ruled out.

Matched-null results, where labels are shuffled and the model is rerun to show what score pure chance produces:

| Null | AUC mean | AUC p95 | Null AUC >= observed |
| --- | ---: | ---: | ---: |
| Administrative-format label shuffle | 0.597158 | 0.654323 | 0.001500 |
| Emblem/copy-family label shuffle | 0.616055 | 0.662687 | 0.001000 |

So the size association is real. Across the full grouped sample, `034` artifacts are smaller on average, and the dimension model beats both matched shuffles. Median area is 101.25 mm² for `034`, 117.15 mm² for `033`, and 146.85 mm² for `032`.

Being real is not the same as being a tier. A tier would have to tell `034` apart from its neighbours, and the cleanest held-out family shows it does not:

| H-2218 through H-2239 holdout | Result |
| --- | ---: |
| Rows | 22 |
| True `034` | 21 |
| True `033` | 1 |
| `034` recall | 1.000000 |
| Non-`034` specificity | 0.000000 |
| ROC AUC | 0.476190 |

Read that column carefully. Trained without ever seeing this series, the dimension model called all 22 small tablets `034`, including `H-2238`, which is a `033`. Recall of 1.000000 with specificity of 0.000000 is what a model looks like when it says yes to everything. It recognized the series' small form factor. It did not recognize the short-mark subtype.

## Interpretation

What survives:

- `034` is associated with smaller multi-side Harappa objects in the current Lipi planning layer.
- That association is stronger than random label placement under the two matched shuffles.
- Small-object format remains a useful source/corpus confound for future `034` work.

What fails:

- Size does not discriminate `034` from its `033` sibling inside the completely held-out H-series.
- The dimension model does not beat the administrative-format baseline by a positive grouped-bootstrap margin.
- No ordered quantity, numerical value, measurement unit, commodity class, or metrological tier follows.

This closes the current route in which `034` means a smaller tier. It leaves the separate source-visible graphic and distributional questions about `032/033/034` untouched. The narrow finding is that physical size cannot supply the meaning of those marks on the evidence available now.

## Raw outputs

- `research/data/open_prototype/reports/frame700_034_size_tier_heldout_20260712_summary.json`
- `research/data/open_prototype/reports/frame700_034_size_tier_heldout_20260712_predictions.csv`
- `research/data/open_prototype/reports/frame700_034_size_tier_heldout_20260712_null_iterations.csv`
- `research/data/open_prototype/tools/frame700_034_size_tier_heldout_20260712.mjs`
