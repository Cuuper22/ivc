# Provisional Crosswalk Audit

Date: 2026-05-24

## Purpose

This note records a first attempt to line up two sign catalogs against each other. It exists so later work has a ranked shortlist to check by hand, rather than a whole corpus to stare at.

Terms first. The project reads the same inscriptions from two independent catalogs: `lipi`, whose signs are bare numbers like `740`, and `mayig`, whose signs are Parpola-style codes like `P324`. A "crosswalk" is a mapping between the two. It is "provisional" and "positional" because it is built only by lining the same inscription up in both catalogs and pairing signs slot by slot — no one has yet compared the shapes. An "allograph" is one sign written in two visual forms; a "merge" would be a decision that two catalog codes are really one sign.

This audit derives provisional candidates between `lipi` numeric signs such as `740` and `mayig` Parpola-style signs such as `P324`.

It is a graphemic triage artifact — a first sort by sign shape and position, meant to set priorities. It is not an accepted sign crosswalk. It does not settle exact signs, allographs, merges, splits, phonetic values, meanings, or translations.

## Local Artifacts

```text
data/open_prototype/reports/crosswalk_alignment_pairs.csv
data/open_prototype/reports/crosswalk_lipi_to_mayig_candidates.csv
data/open_prototype/reports/crosswalk_mayig_to_lipi_candidates.csv
data/open_prototype/reports/crosswalk_high_frequency_sample.csv
data/open_prototype/reports/crosswalk_collision_summary.csv
data/open_prototype/reports/crosswalk_summary.json
```

## Eligibility Rule

Only strict rows — rows that passed the earlier cleanliness checks with no warning flags — were allowed into the positional alignment:

```text
status == candidate_for_pre_crosswalk_structure_tests
lipi_dir == R/L
flags empty
```

This excludes two otherwise clean rows:

| CISI | Direction | Reason |
| --- | --- | --- |
| M-66 | BUS | Nonstandard direction handling. |
| M-137 | NR | No reliable direction for positional pairing. |

## Corpus Build

```text
eligible_records: 136
aligned_positions: 739
unique_lipi_signs: 189
unique_mayig_signs: 160
lipi_to_mayig_candidate_count: 189
mayig_to_lipi_candidate_count: 160
```

Method:

- Take same-artifact rows where `lipi` and `mayig` sign counts match.
- Pair signs by position only when direction is `R/L`.
- Count how often each `lipi` numeric sign aligns to each `mayig` `P###` sign.
- Grade consistency.
- Keep every mapping state as `uncertain`.

## Candidate Grade Counts

| Grade | Count |
| --- | ---: |
| `high_consistency_positional_candidate` | 14 |
| `medium_consistency_positional_candidate` | 21 |
| `low_consistency_positional_candidate` | 27 |
| `conflicted_positional_candidate` | 6 |
| `sparse_singleton_or_doubleton` | 121 |

The large sparse class is expected in a small corpus with a large sign inventory.

## High-Frequency Workset

These were the five high-priority signs named by the previous structural baseline.

| `lipi` sign | Top `mayig` sign | Grade | Aligned positions | Top share | Counterexamples |
| --- | --- | --- | ---: | ---: | --- |
| `740` | `P324` | `high_consistency_positional_candidate` | 73 | 1.000000 | none |
| `002` | `P122` | `high_consistency_positional_candidate` | 60 | 0.950000 | `P145:2;P300:1` |
| `220` | `P050` | `medium_consistency_positional_candidate` | 29 | 0.931034 | `P056:1;P060:1` |
| `390` | `P086` | `high_consistency_positional_candidate` | 25 | 1.000000 | none |
| `032` | `P145` | `high_consistency_positional_candidate` | 21 | 0.952381 | `P122:1` |

Interpretation:

These five signs now have review targets. They do not yet have accepted mappings.

## Possible Merge Or Allograph Clusters

Grouping `lipi` candidates by their top `mayig` sign reveals possible merge/allograph problems:

| `mayig` sign | `lipi` candidates | Aligned positions | Interpretation |
| --- | --- | ---: | --- |
| `P385` | `817`, `861` | 24 | Strong possible merge/allograph cluster. |
| `P230` | `798`, `550` | 18 | Mixed: one conflicted and one medium candidate. |
| `P364` | `803`, `806` | 15 | Possible variant or sign-list policy difference. |
| `P154` | `920`, `900` | 13 | Conflicted cluster. |
| `P316` | `705`, `706` | 12 | Possible variant or sign-list policy difference. |

The `P385` cluster is especially important because both `817` and `861` align perfectly to `P385` in this strict subset. That is not proof of an allograph merge, but it is a high-priority manual check.

## Conflicted Numeric Candidates

These require caution before any allograph policy is tested:

| `lipi` sign | Top `mayig` sign | Aligned positions | Top share | Counterexamples |
| --- | --- | ---: | ---: | --- |
| `798` | `P230` | 10 | 0.600000 | `P075:4` |
| `920` | `P154` | 7 | 0.571429 | `P160:2;P156:1` |
| `832` | `P368` | 3 | 0.666667 | `P366:1` |
| `236` | `P051` | 2 | 0.500000 | `P061:1` |
| `621` | `P092` | 2 | 0.500000 | `P265:1` |
| `844` | `P349` | 2 | 0.500000 | `P352:1` |

## Interpretation Boundary

This audit supports only this claim:

```text
The strict overlap subset yields a prioritized list of provisional positional crosswalk candidates between `lipi` numeric signs and `mayig` Parpola-style signs.
```

It does not support:

- Exact sign equivalence.
- Accepted allograph merges.
- Semantic readings.
- Linguistic readings.
- Translation.

## Next Falsification

The next graphemic work should manually validate the high-frequency workset:

```text
740 -> P324
002 -> P122
220 -> P050
390 -> P086
032 -> P145
```

Validation requires at least one additional evidence type beyond positional alignment:

- Primary image or publication plate.
- Authoritative sign-list cross-reference.
- Corpus documentation.
- Graphemic feature description.
- Stable neighbor distribution after expanding beyond the Mohenjo-daro seal subset.

The `P385` collision cluster, `817` and `861`, should be reviewed in the same pass because it may reveal an allograph policy difference between the numeric and Parpola-style systems.

