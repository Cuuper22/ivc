# Mismatch Audit

Date: 2026-05-24

## Purpose

This note records a data-hygiene check. It exists because the project reads the same inscriptions from two independent catalogs, and where those two catalogs disagree about how many signs an inscription has, we cannot safely treat the row as known.

Terms first. The two catalogs are `lipi`, whose signs are numeric codes written `+###+`, and `mayig`, whose signs are Parpola-style codes written `P###`. The "overlap" is the set of inscriptions present in both. A "crosswalk" is a mapping between the two catalogs' sign codes; "pre-crosswalk" means before any such mapping is assumed. "Collation" is the manual act of checking a row against a source image or authoritative catalog entry.

This audit classifies the 29 sign-count mismatches found in the first open prototype overlap probe.

It does not resolve sign equivalence. It only decides which overlap rows are safe enough for pre-crosswalk structural tests and which rows need manual collation against source images or authoritative catalog entries.

## Local Artifacts

```text
data/open_prototype/reports/mismatch_audit.csv
data/open_prototype/reports/mismatch_summary.json
data/open_prototype/reports/mismatch_collation_queue.csv
data/open_prototype/reports/mismatch_collation_class_summary.csv
data/open_prototype/reports/mismatch_collation_summary.json
```

Inputs:

```text
data/open_prototype/reports/overlap_probe.csv
```

## Result Summary

```text
total_overlap_rows: 179
count_matches: 150
count_mismatches: 29
clean_pre_crosswalk_candidates: 138
sensitivity_flag_candidates: 12
manual_review_rows: 29
rows_with_any_flag: 28
```

The key change from the earlier overlap headline is that not all 150 count matches are equally clean. Twelve count-matching rows still contain sensitivity flags — markers that something about the row could swing a result — such as unknown signs or compound/divided signs. They can be used only in sensitivity runs, not in the clean first-pass baseline.

## Primary Categories

| Category | Rows | Meaning |
| --- | ---: | --- |
| `count_match` | 150 | Rough sign counts agree between `lipi` and `mayig`. |
| `mayig_counts_more` | 9 | `mayig` grapheme count is higher without an obvious damage/unknown flag. |
| `lipi_boundary_fragment` | 4 | `lipi` text contains boundary brackets such as `]` or `[`. |
| `lipi_unknown_zero` | 4 | `lipi` has `000` unknown signs without matching `P000` as the primary issue. |
| `shared_unknown_zero` | 4 | Both source layers show unknown/damaged placeholders. |
| `lipi_counts_more` | 4 | `lipi` sign count is higher without an obvious damage/unknown flag. |
| `mayig_unknown_p000` | 3 | `mayig` contains `P000` unknown signs as the primary issue. |
| `lipi_compound_slash` | 1 | `lipi` uses a slash compound/divided sign as the primary issue. |

## Status Classes

| Status | Rows | Allowed Use |
| --- | ---: | --- |
| `candidate_for_pre_crosswalk_structure_tests` | 138 | Clean first-pass direction/order baselines only. |
| `candidate_with_sensitivity_flag` | 12 | Include only in sensitivity runs. |
| `manual_collation_required` | 16 | Exclude until checked against primary/source catalog evidence. |
| `manual_count_disagreement` | 13 | Exclude until sign-count policy is resolved. |

## Flag Counts

Flags can overlap.

| Flag | Rows |
| --- | ---: |
| `mayig_unknown_p000` | 18 |
| `lipi_unknown_zero` | 13 |
| `lipi_compound_slash` | 7 |
| `lipi_boundary_fragment` | 4 |

## Mismatch Rows

| CISI | `lipi` length | `lipi` signs | `mayig` signs | Diff | Category | Status |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| M-4 | 9 | 9 | 10 | 1 | `mayig_counts_more` | `manual_count_disagreement` |
| M-7 | 9 | 9 | 11 | 2 | `mayig_counts_more` | `manual_count_disagreement` |
| M-10 | 11 | 11 | 10 | -1 | `lipi_counts_more` | `manual_count_disagreement` |
| M-19 | 4+? | 2 | 3 | 1 | `lipi_boundary_fragment` | `manual_collation_required` |
| M-20 | 7 | 7 | 8 | 1 | `mayig_counts_more` | `manual_count_disagreement` |
| M-22 | 7+? | 6 | 7 | 1 | `lipi_boundary_fragment` | `manual_collation_required` |
| M-25 | 4 | 4 | 5 | 1 | `mayig_counts_more` | `manual_count_disagreement` |
| M-27 | 7 | 6 | 7 | 1 | `lipi_unknown_zero` | `manual_collation_required` |
| M-39 | 6+? | 6 | 7 | 1 | `lipi_boundary_fragment` | `manual_collation_required` |
| M-41 | 9 | 9 | 8 | -1 | `lipi_counts_more` | `manual_count_disagreement` |
| M-45 | 6 | 6 | 7 | 1 | `mayig_counts_more` | `manual_count_disagreement` |
| M-55 | 6 | 5 | 6 | 1 | `mayig_unknown_p000` | `manual_collation_required` |
| M-60 | 2 | 1 | 2 | 1 | `shared_unknown_zero` | `manual_collation_required` |
| M-61 | 7 | 6 | 7 | 1 | `lipi_unknown_zero` | `manual_collation_required` |
| M-62 | 6 | 5 | 6 | 1 | `lipi_unknown_zero` | `manual_collation_required` |
| M-72 | 7 | 7 | 6 | -1 | `lipi_counts_more` | `manual_count_disagreement` |
| M-73 | 3 | 3 | 4 | 1 | `mayig_unknown_p000` | `manual_collation_required` |
| M-81 | 6 | 6 | 7 | 1 | `mayig_counts_more` | `manual_count_disagreement` |
| M-98 | 4 | 4 | 3 | -1 | `lipi_counts_more` | `manual_count_disagreement` |
| M-105 | 7 | 5 | 7 | 2 | `lipi_unknown_zero` | `manual_collation_required` |
| M-106 | 6 | 4 | 3 | -1 | `shared_unknown_zero` | `manual_collation_required` |
| M-110 | 4 | 2 | 3 | 1 | `shared_unknown_zero` | `manual_collation_required` |
| M-111 | 6 | 6 | 7 | 1 | `mayig_counts_more` | `manual_count_disagreement` |
| M-120 | 7 | 7 | 6 | -1 | `lipi_compound_slash` | `manual_collation_required` |
| M-126 | 4 | 4 | 5 | 1 | `mayig_unknown_p000` | `manual_collation_required` |
| M-141 | 10 | 6 | 3 | -3 | `shared_unknown_zero` | `manual_collation_required` |
| M-161 | 3 | 3 | 4 | 1 | `mayig_counts_more` | `manual_count_disagreement` |
| M-162 | 5 | 5 | 6 | 1 | `mayig_counts_more` | `manual_count_disagreement` |
| M-175 | 2+? | 2 | 3 | 1 | `lipi_boundary_fragment` | `manual_collation_required` |

## Gate For Next Experiments

This is the gate — the checkpoint rows must clear before any later experiment may touch them.

The first direction/order baseline may use only the 138 rows marked:

```text
candidate_for_pre_crosswalk_structure_tests
```

The 12 count-matching rows with sensitivity flags must be run as an inclusion/exclusion sensitivity check. The 29 mismatches stay out until the project has a manual collation table for each row.

That table now exists as a queue, not as a resolution:

[Mismatch collation queue](mismatch_collation_queue.md)

Summary:

```text
P1_source_image_required: 10
P2_standard_manual_review: 12
P3_policy_check_candidate: 7
```

No mismatch row is cleared for structural use yet.

## Claim Boundary

This audit supports a corpus-readiness claim only:

```text
There is a 138-row clean overlap subset suitable for pre-crosswalk structural experiments.
```

It does not support:

- Direct sign equivalence between `P###` and `+###`.
- Semantic readings.
- Linguistic readings.
- Translation.
