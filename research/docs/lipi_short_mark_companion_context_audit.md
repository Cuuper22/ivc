# Lipi Short-Mark Companion Context Audit

Date: 2026-05-24

## Purpose

This note asks whether three signs that share a slot keep different company elsewhere on the same object. A short mark is a one- or two-sign row on an object that carries writing on more than one side; when the mark has two tokens and one of them is sign `700`, the other is its companion. Most such companions are `032`, `033`, or `034`. The longer row on another side of the same object is its context.

This audit follows the [Lipi short-mark orientation audit](lipi_short_mark_orientation_audit.md) and [Lipi short-mark context orientation audit](lipi_short_mark_context_orientation_audit.md).

It asks:

```text
Do the core short-mark companions 032, 033, and 034 bind to different same-artifact longer-row contexts after preserving artifact type and 700-order?
```

This matters because a future numerical, metrological, or administrative hypothesis cannot use `032`, `033`, and `034` as interchangeable short-mark labels if they behave differently against longer rows. But any such difference is still only a validation target until image direction, side order, and source-side conventions are checked.

## Local Artifacts

```text
data/open_prototype/tools/lipi_short_mark_companion_context_audit.mjs
data/open_prototype/reports/lipi_short_mark_companion_context_rows.csv
data/open_prototype/reports/lipi_short_mark_companion_context_families.csv
data/open_prototype/reports/lipi_short_mark_companion_context_tests.csv
data/open_prototype/reports/lipi_short_mark_companion_context_summary.json
```

Input:

```text
data/open_prototype/reports/lipi_multiside_mark_rows.csv
```

## Scope

The target set is the Harappa `TAB:B`/`TAB:I` rows where the short mark has exactly two tokens, one token is `700`, and the companion is `032`, `033`, or `034`.

```text
target_rows: 353
TAB:B_rows: 178
TAB:I_rows: 175
032_rows: 102
033_rows: 137
034_rows: 114
700_first: 299
700_last: 54
```

Context classes:

```text
single_longer_text: 233
all_short_or_no_longer_text: 62
single_short_no_longer_text: 53
multiple_longer_texts: 5
```

Catalog-side relation to longer text:

```text
short_after_all_longer: 132
no_longer_text: 115
short_before_all_longer: 105
short_between_longer_sides: 1
```

## Method

The audit uses two association layers:

1. One-vs-rest Fisher exact tests for each companion and context feature.
2. A deterministic blocked permutation test that shuffles companion labels within `type|700_order` blocks. That shuffle is the null model: a deliberately meaningless version of the data showing how large an apparent association chance alone produces once the blocked features are held fixed.

The blocked layer asks whether a companion-context association survives after preserving two easy confounds:

```text
artifact type: TAB:B versus TAB:I
internal order: 700_first versus 700_last
```

Permutation settings:

```text
iterations: 5000
seed: 20260524
block: type|700_order
```

The audit emits 90 tests and applies correction across the emitted tests.

## Corrected Flags

Two side-relation contrasts survive the blocked permutation layer:

| Companion | Context | Companion Share | Other Share | Fisher BH FDR | Blocked Permutation BH FDR |
| --- | --- | ---: | ---: | ---: | ---: |
| `034` | `short_after_all_longer` | 0.219298 | 0.447699 | 0.003064 | 0.035993 |
| `033` | `short_after_all_longer` | 0.489051 | 0.300926 | 0.020636 | 0.035993 |

Interpretation of the direction:

```text
033 is overrepresented when the short mark comes after all longer rows.
034 is underrepresented in that same catalog-side relation.
```

This does not establish physical side order. `short_after_all_longer` is a catalog-side relation until source images or stronger side metadata validate it.

## Raw-Only Hints

The strongest raw longer-sequence hint remains `+400-740-176+`, but it does not survive the blocked correction:

| Companion | Context | Companion Share | Other Share | Fisher BH FDR | Blocked Permutation BH FDR |
| --- | --- | ---: | ---: | ---: | ---: |
| `033` | `+400-740-176+` present in longer text | 0.145985 | 0.050926 | 0.057772 | 0.082269 |
| `032` | `+400-740-176+` present in longer text | 0.019608 | 0.115538 | 0.057772 | 0.107978 |

That makes `+400-740-176+` a validation priority, not an accepted context binding.

## Companion Summaries

| Companion | Rows | No Longer Text | Short After All Longer | Short Before All Longer | Top Longer Family |
| --- | ---: | ---: | ---: | ---: | --- |
| `032` | 102 | 29 | 40 | 33 | `2:+740-031-001-140+` in 3 rows |
| `033` | 137 | 37 | 67 | 32 | `1:+400-740-176+` in 16 rows |
| `034` | 114 | 49 | 25 | 40 | `1:+400-740-176+` in 7 rows; `2:+002-861-416+` in 4 rows |

These are not readings. They are source-validation queues.

## Interpretation

This audit strengthens one narrow point:

```text
The 033/034 contrast is not only a raw companion difference. It also has a corrected catalog-side relation difference in the current planning layer, meaning the project's unverified working data.
```

That means future plate checks should not only ask whether `033` and `034` are visually distinct. They should also ask whether the apparent `short_after_all_longer` versus `short_before_all_longer` pattern is a real physical side/order feature or a catalog artifact.

The audit does not support:

- A number.
- A measure.
- A commodity.
- A side function.
- An administrative role.
- A sign meaning.
- A phonetic value.
- A language assignment.
- A translation.

## Next Evidence Step

Update the source/image validation sheet so each core short mark carries:

1. Companion token: `032`, `033`, or `034`.
2. Exact order: `700_first` or `700_last`.
3. Catalog-side relation to longer text.
4. Longer-row sequence family.
5. Image/source direction status.
6. Whether side relation survives image validation.

Only after that can this be tested against measurements, object class, and external metrological or administrative comparators.
