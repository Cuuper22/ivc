# Lipi Short-Mark Orientation Audit

Date: 2026-05-24

## Purpose

This note records a bookkeeping check on sign order. It exists because a later hypothesis could go badly wrong if we quietly treated two reversed sign pairs as the same thing.

First, the terms. A "short mark" is a very short catalog row — one or two signs — flagged as a short-mark candidate on a Harappa tablet. `TAB:B` and `TAB:I` are two Harappa tablet type codes from the catalog. Numbers like `700`, `032`, `033`, and `034` are catalog sign codes, not readings. A "companion mark" is the other sign in a two-sign row that contains sign `700`.

This audit follows the [Lipi multi-side mark stratified probe](lipi_multiside_mark_stratified_probe.md) and [multi-side mark validation queue](lipi_multiside_mark_validation_queue.md).

It asks a narrow orientation-control question:

```text
Inside Harappa TAB:B and TAB:I short marks, do two-token 700 companion marks keep a stable internal order?
```

Why this matters: a future side-mark or metrological hypothesis cannot treat `+700-033+` (sign `700` first) and `+033-700+` (sign `700` last) as interchangeable until direction, mirroring, catalog order, and image orientation have been checked.

This is not a reading.

## Local Artifacts

```text
data/open_prototype/tools/lipi_short_mark_orientation_audit.mjs
data/open_prototype/reports/lipi_short_mark_orientation_rows.csv
data/open_prototype/reports/lipi_short_mark_orientation_companions.csv
data/open_prototype/reports/lipi_short_mark_orientation_tests.csv
data/open_prototype/reports/lipi_short_mark_orientation_summary.json
```

Input:

```text
data/open_prototype/reports/lipi_multiside_mark_rows.csv
```

## Scope

```text
target_short_mark_rows: 491
TAB:B_short_mark_rows: 222
TAB:I_short_mark_rows: 269
two_token_700_companion_rows: 368
core_032_033_034_rows: 353
```

Target rows are Harappa `TAB:B` and `TAB:I` rows flagged as short-mark candidates.

The audit focuses on two-token rows where one token is `700`.

## Main Counts

Two-token `700` companion rows:

```text
700_first: 313
700_last: 55
```

Core companions:

| Companion | Rows | `700` First | `700` Last | First Share |
| --- | ---: | ---: | ---: | ---: |
| `032` | 102 | 85 | 17 | 0.833333 |
| `033` | 137 | 113 | 24 | 0.824818 |
| `034` | 114 | 101 | 13 | 0.885965 |

## Type Split

| Companion | TAB:I `700` First | TAB:I `700` Last | TAB:B `700` First | TAB:B `700` Last |
| --- | ---: | ---: | ---: | ---: |
| `032` | 37 | 2 | 48 | 15 |
| `033` | 60 | 4 | 53 | 20 |
| `034` | 64 | 8 | 37 | 5 |

## Tests

The audit emits exact tests. Because it runs many tests at once, it applies two standard multiple-testing corrections across all emitted tests: Bonferroni and Benjamini-Hochberg.

Corrected orientation flags — the tests that still stand after correction:

```text
orientation_balance_binomial_700_first_vs_last: 032, 033, 034
type_orientation_assoc_fisher_TAB_I_vs_TAB_B: 032, 033
```

Key emitted tests:

| Test | Companion | Raw P | Bonferroni P | BH FDR P |
| --- | --- | ---: | ---: | ---: |
| `700_first` vs `700_last` | `032` | `4.698103109444e-12` | `5.637723731333e-11` | `1.879241243778e-11` |
| `700_first` vs `700_last` | `033` | `5.247371793292e-15` | `6.296846151951e-14` | `3.148423075975e-14` |
| `700_first` vs `700_last` | `034` | `4.774037347033e-18` | `5.728844816439e-17` | `5.728844816439e-17` |
| TAB:I vs TAB:B orientation | `032` | `0.014463` | `0.173561` | `0.034712` |
| TAB:I vs TAB:B orientation | `033` | `0.001323` | `0.015871` | `0.003968` |
| TAB:I vs TAB:B orientation | `034` | `1.000000` | `1.000000` | `1.000000` |

Side-index orientation checks did not survive correction.

Follow-up context check:

- [Lipi short-mark context orientation audit](lipi_short_mark_context_orientation_audit.md) tests whether reversed core `700` companion marks also carry distinct longer-row contexts. No longer-context association survives correction in that pass.

## Interpretation

The local short-mark queue has a strong internal-order asymmetry:

```text
700-companion marks are usually written with 700 first.
```

But the reversed forms are real enough in the planning layer — the catalog-derived data we work from before any image validation — to block careless normalization:

```text
+700-033+ cannot be silently merged with +033-700+.
+700-032+ cannot be silently merged with +032-700+.
+700-034+ cannot be silently merged with +034-700+.
```

The type split matters: `032` and `033` show corrected TAB:I versus TAB:B orientation differences, while `034` does not in this pass.

The context follow-up matters too: reversal is not yet explained by, or promoted to, a longer-row functional contrast.

This is an orientation and catalog-control result. It does not make `700`, `032`, `033`, or `034` numerical, metrological, phonetic, semantic, or linguistic signs.

## Consequence

The next side-mark validation sheets should preserve:

1. Exact short-mark order.
2. Unordered companion pair.
3. Artifact type.
4. Side index.
5. Catalog/image direction.
6. Whether the source image is mirrored, rotated, or copied from a seal impression.

Only after that can the project decide whether reversed short marks are physical orientation, scribal/copy variation, catalog convention, allography, or separate signs.

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
