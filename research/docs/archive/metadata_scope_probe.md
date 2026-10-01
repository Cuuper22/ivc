# Metadata Scope Probe

Date: 2026-05-24

## Purpose

This note records a scope check on our own data. It exists because a structural finding is only as broad as the material it came from, and it is easy to forget how narrow that material is.

Terms first. A "probe" here is an exploratory pass, not accepted evidence. The "open prototype" is the small openly-licensed dataset the project computes from before touching restricted corpora. "Mayig" is one of the independent sign catalogs the project uses, and its records carry a free-text description field naming the seal's iconography.

This probe asks whether the current open prototype has enough metadata diversity to support broad structural claims.

It does not test meaning. It does not test iconographic semantics. It only checks what the local Mayig description field can and cannot support.

## Local Artifacts

```text
data/open_prototype/reports/metadata_scope_rows.csv
data/open_prototype/reports/metadata_scope_status_by_series.csv
data/open_prototype/reports/metadata_scope_scaffold_by_series.csv
data/open_prototype/reports/metadata_scope_top_anchor_by_series.csv
data/open_prototype/reports/metadata_scope_summary.json
```

Source files:

```text
data/open_prototype/mayig/records_index.csv
data/open_prototype/reports/mismatch_audit.csv
data/open_prototype/reports/formula_pattern_sequences.csv
data/open_prototype/reports/sensitivity_formula_sequences.csv
data/open_prototype/reports/mismatch_collation_queue.csv
```

## Main Scope Result

The local Mayig prototype is not iconographically diverse.

```text
total_mayig_records: 179
description_count: 5
description_family_count: 1
description_kind_count: 1
description_family: unicorn
description_kind: seal
```

The five descriptions are:

| Description | Rows |
| --- | ---: |
| `unicorn IV seal` | 96 |
| `unicorn III seal` | 45 |
| `unicorn II seal` | 19 |
| `unicorn V seal` | 10 |
| `unicorn I seal` | 9 |

This means every current structural result from the open Mayig subset is inside one description family: unicorn seals.

## Gate Behavior By Series

Each row has to pass gates — recorded checkpoints that admit or block it — before it can be used. This table shows where rows of each unicorn series ended up.

| Series | Strict Formula | Sensitivity | Manual Collation | Manual Count Disagreement | Other |
| --- | ---: | ---: | ---: | ---: | ---: |
| `I` | 6 | 0 | 0 | 3 | 0 |
| `II` | 12 | 2 | 3 | 2 | 0 |
| `III` | 31 | 4 | 6 | 3 | 1 |
| `IV` | 79 | 5 | 6 | 5 | 1 |
| `V` | 8 | 1 | 1 | 0 | 0 |

The strict formula subset is concentrated in `unicorn IV` by raw count:

```text
unicorn_IV_strict_rows: 79 of 136
```

That concentration does not prove a special `unicorn IV` structure. It mainly reflects the underlying Mayig prototype distribution, where `unicorn IV seal` has 96 of 179 rows.

## Scaffold By Series

The "scaffold" is the observed tendency for certain signs to sit at the start of a row (initial) and others at the end (terminal), giving an `I...T` frame. These counts are per sign-inventory policy — the rule chosen for deciding which sign codes count as the same sign.

For the `mayig_observed_parpola` policy:

| Series | Rows | Initial At Start | Terminal At End | I...T Scaffold |
| --- | ---: | ---: | ---: | ---: |
| `I` | 6 | 1 | 1 | 1 |
| `II` | 12 | 7 | 5 | 4 |
| `III` | 31 | 22 | 10 | 7 |
| `IV` | 79 | 57 | 17 | 11 |
| `V` | 8 | 5 | 1 | 0 |

For the raw numeric policy:

| Series | Rows | Initial At Start | Terminal At End | I...T Scaffold |
| --- | ---: | ---: | ---: | ---: |
| `I` | 6 | 1 | 1 | 1 |
| `II` | 12 | 7 | 5 | 4 |
| `III` | 31 | 20 | 10 | 6 |
| `IV` | 79 | 54 | 17 | 11 |
| `V` | 8 | 5 | 0 | 0 |

The edge scaffold is not confined to one subseries, but `unicorn IV` contributes the largest absolute count because it dominates the dataset.

## Top Anchor Pair By Series

An "edge anchor" is a specific pair of signs that recurs as the first and last sign of a row. The strongest edge anchor from the formula-pattern probe is distributed like this:

```text
mayig P324...P385:
II: 1 row
III: 2 rows
IV: 7 rows

p385_merge_only L740...P385:
II: 1 row
III: 2 rows
IV: 7 rows

raw L740...L817/L861:
II: 1 row
III: 2 rows
IV: 7 rows
```

This is useful triage for manual review, not an iconographic claim. Since there are no non-unicorn comparison rows in the Mayig prototype, the project cannot yet say whether the anchor is unicorn-specific, seal-specific, site-specific, or generally script-structural.

## Result

This probe supports only this claim:

```text
The current open prototype's structural findings are scoped to Mohenjo-daro unicorn seal rows, with heavy representation from the unicorn IV subseries.
```

It does not support:

- Cross-iconography generalization.
- Cross-artifact-class grammar.
- IVC-wide structural grammar.
- Any iconographic meaning for signs.
- Semantic reading.
- Phonetic reading.
- Translation.

## Next Falsification

The next tests should ask:

- Can an authoritative corpus add non-unicorn seals, tablets, tags, pottery marks, and long signboards?
- Does the `P324...P385` anchor survive outside unicorn seals?
- Does the structural scaffold survive outside Mohenjo-daro?
- Do description subseries correspond to catalog organization, iconographic variation, chronological grouping, or source-file batching?
- Does the gate failure rate differ by series after image-level collation?
