# Mismatch Collation Queue

Date: 2026-05-24

## Purpose

This note is a worklist. It names the inscriptions someone has to check by hand, and says what to look for in each one.

Why it exists: the project reads the same inscriptions from two independent catalogs — `lipi`, whose signs are numeric codes, and `mayig`, whose signs are Parpola-style `P###` codes. For 29 inscriptions the two catalogs disagree about how many signs are present. "Collation" is the manual act of settling such a disagreement against a source image or an authoritative catalog entry. Until that happens, those rows stay out of every experiment.

This document turns the 29 count-mismatch rows from the overlap audit into a manual collation queue.

It does not resolve the mismatches. It classifies the likely failure mode, records simple count-policy checks, and assigns a review priority before any row can be admitted into structural experiments.

## Local Artifacts

```text
data/open_prototype/reports/mismatch_collation_queue.csv
data/open_prototype/reports/mismatch_collation_class_summary.csv
data/open_prototype/reports/mismatch_collation_summary.json
```

Source file:

```text
data/open_prototype/reports/mismatch_audit.csv
```

Input rows:

```text
manual_review_rows: 29
manual_count_disagreement: 13
manual_collation_required: 16
```

## Review Priorities

| Priority | Rows | Meaning |
| --- | ---: | --- |
| `P1_source_image_required` | 10 | Damaged boundary, multi-sign disagreement, ambiguous unknown policy, or complex unknown mismatch. |
| `P2_standard_manual_review` | 12 | Unflagged count disagreement that needs source-level segmentation review. |
| `P3_policy_check_candidate` | 7 | Count can be reconciled by one explicit policy, but still needs confirmation. |

No row is cleared by this queue. A `P3` label means the row has a plausible count-policy explanation, not that the explanation is accepted.

## Failure-Mode Classes

| Class | Rows | Examples |
| --- | ---: | --- |
| `unflagged_mayig_extra` | 8 | `M-111;M-161;M-162;M-20;M-25;M-4;M-45;M-81` |
| `damaged_boundary_fragment` | 4 | `M-175;M-19;M-22;M-39` |
| `lipi_unknown_zero_explains_count` | 4 | `M-105;M-27;M-61;M-62` |
| `unflagged_lipi_extra` | 4 | `M-10;M-41;M-72;M-98` |
| `mayig_unknown_p000_explains_count` | 3 | `M-110;M-126;M-73` |
| `ambiguous_unknown_policy_reconciles` | 2 | `M-55;M-60` |
| `multi_sign_count_disagreement` | 2 | `M-141;M-7` |
| `complex_manual_collation` | 1 | `M-106` |
| `slash_compound_count_policy_reconciles` | 1 | `M-120` |

## Count-Policy Checks

Simple policy checks found:

```text
drop_mayig_P000: 9 rows
count_lipi_000_as_sign: 7 rows
treat_lipi_slash_compound_as_one_sign: 1 row
```

These are diagnostic only. They are not accepted corrections.

The two ambiguous rows are important:

```text
M-55
M-60
```

For both, either counting Lipi `000` or dropping Mayig `P000` reconciles the count. That ambiguity is exactly why source images or authoritative catalog notes are required before choosing either policy.

## Unflagged Extra-Sign Rows

The unflagged Mayig-extra group is the largest unresolved class:

```text
M-111; M-161; M-162; M-20; M-25; M-4; M-45; M-81
```

Several of these contain repeated Mayig graphemes — the same sign code appearing twice in one inscription:

```text
M-111: P378:2, consecutive P378
M-161: P268:2, consecutive P268
M-20: P147:2, consecutive P147
M-25: P268:2, consecutive P268
M-4: P147:2 and P268:2, consecutive P268
M-45: P268:2, consecutive P268
M-81: P268:2, consecutive P268
```

This pattern could reflect real repeated signs, segmentation splits, or source-layer transcription conventions. It cannot be resolved statistically from the current open data.

## High-Risk Rows

Rows requiring source-image or catalog collation before any reuse:

```text
M-105
M-106
M-141
M-175
M-19
M-22
M-39
M-55
M-60
M-7
```

Reasons:

- Boundary fragments can hide missing signs.
- Multi-sign disagreements cannot be repaired by a one-sign policy.
- Ambiguous unknown-policy rows would require choosing between source layers.
- Complex unknown rows do not have a clean count-policy explanation.

## Result

The mismatch rows remain excluded from structural baselines.

This queue supports only this claim:

```text
The 29 count-mismatch rows now have a concrete manual collation worklist with failure-mode classes and review priorities.
```

It does not support:

- Adding any mismatch row to the clean subset.
- Accepting any count-policy correction.
- Sign equivalence.
- Semantic reading.
- Phonetic reading.
- Translation.

## Next Falsification

The next tests should ask:

- Can the 7 `P3` policy-check candidates be resolved against images or authoritative catalog entries?
- Are the repeated Mayig graphemes in the 8 unflagged Mayig-extra rows real repeated signs or segmentation artifacts?
- Does the source catalog treat Lipi slash compounds as one sign, two signs, or a ligature?
- Do the 10 `P1` rows reveal systematic damage conventions that should be encoded in the corpus schema?
