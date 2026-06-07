# Lipi Short-Mark Context Orientation Audit

Date: 2026-05-24

## Purpose

This audit follows the [Lipi short-mark orientation audit](lipi_short_mark_orientation_audit.md).

It asks a narrower falsification question:

```text
When a Harappa TAB:B/TAB:I two-token 700 companion short mark is reversed, does it also change the longer-row context on the same artifact?
```

This matters because the prior audit showed that `+700-032+`, `+700-033+`, and `+700-034+` are strongly `700`-first, while reversed forms are still present. If reversed forms had a strong artifact-context association, they would become a higher-priority contrast. If not, they remain an orientation and source-validation variable.

This is still not a reading.

## Local Artifacts

```text
data/open_prototype/tools/lipi_short_mark_context_orientation_audit.mjs
data/open_prototype/reports/lipi_short_mark_context_orientation_rows.csv
data/open_prototype/reports/lipi_short_mark_context_orientation_families.csv
data/open_prototype/reports/lipi_short_mark_context_orientation_tests.csv
data/open_prototype/reports/lipi_short_mark_context_orientation_summary.json
```

Input:

```text
data/open_prototype/reports/lipi_multiside_mark_rows.csv
```

## Scope

The audit keeps only Harappa `TAB:B` and `TAB:I` short-mark rows where the row has exactly two tokens, one token is `700`, and the companion is one of `032`, `033`, or `034`.

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

The 299/54 split differs slightly from the broader orientation audit's 313/55 because this context audit keeps only the three core companions.

## Context Counts

Artifact-side context classes:

| Context Class | Rows |
| --- | ---: |
| `single_longer_text` | 233 |
| `all_short_or_no_longer_text` | 62 |
| `single_short_no_longer_text` | 53 |
| `multiple_longer_texts` | 5 |

Side relation to longer text:

| Side Relation | Rows |
| --- | ---: |
| `short_after_all_longer` | 132 |
| `no_longer_text` | 115 |
| `short_before_all_longer` | 105 |
| `short_between_longer_sides` | 1 |

## Companion Context

Core summaries:

| Companion | Order | Rows | Any Longer Text | No Longer Text |
| --- | --- | ---: | ---: | ---: |
| `032` | `700_first` | 85 | 60 | 25 |
| `032` | `700_last` | 17 | 13 | 4 |
| `033` | `700_first` | 113 | 84 | 29 |
| `033` | `700_last` | 24 | 16 | 8 |
| `034` | `700_first` | 101 | 54 | 47 |
| `034` | `700_last` | 13 | 11 | 2 |

The strongest repeated longer-row families remain planning targets, not interpretations:

| Companion | Order | Longer Side Text | Rows |
| --- | --- | --- | ---: |
| `033` | `700_first` | `1:+400-740-176+` | 15 |
| `034` | `700_first` | `1:+400-740-176+` | 7 |
| `032` | `700_first` | `2:+740-031-001-140+` | 3 |
| `033` | `700_first` | `2:+400-740-176+` | 3 |

## Tests

The audit emits 57 Fisher exact tests comparing `700_first` versus `700_last` within each companion, plus all-core descriptive checks. Tested contexts include any longer text, single/multiple longer text, short-before/after side relation, focus longer tokens, and focus longer sequences.

No context association survives Benjamini-Hochberg or Bonferroni correction.

Smallest raw P values:

| Scope | Companion | Context | Raw P | Bonferroni P | BH FDR P |
| --- | --- | --- | ---: | ---: | ---: |
| per companion | `033` | `has_long_sequence_+400-740-176+` | `0.024009` | `1.000000` | `0.741941` |
| per companion | `034` | `single_longer_text` | `0.035597` | `1.000000` | `0.741941` |
| per companion | `034` | `has_any_longer_text` | `0.039050` | `1.000000` | `0.741941` |
| all core | `032_033_034` | `has_long_sequence_+400-740-176+` | `0.063841` | `1.000000` | `0.776993` |

## Interpretation

The reversed forms do not currently show a corrected longer-context association. That means this audit does not promote `+033-700+`, `+032-700+`, or `+034-700+` to separate functional classes.

The correct consequence is narrower:

```text
Preserve exact order for image/source validation, but do not infer a function from the reversal.
```

The prior orientation audit still matters because the order imbalance is strong. This context audit adds that the imbalance is not yet explained by the available longer-row context.

## Next Evidence Step

For the source/image validation sheets:

1. Keep exact short-mark order.
2. Keep the longer-side context attached to each short mark.
3. Mark whether the artifact has no longer text, one longer text, or multiple longer texts.
4. Recheck the raw `+400-740-176+` hint only after image direction and side order are validated.

## Interpretation Boundary

This audit does not support:

- Physical side function.
- Numerical value.
- Metrological reading.
- Commodity reading.
- Administrative reading.
- Sign meaning.
- Phonetic value.
- Language identity.
- Translation.
