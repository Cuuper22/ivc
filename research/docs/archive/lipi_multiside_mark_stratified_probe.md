# Lipi Multi-Side Mark Stratified Probe

Date: 2026-05-24

## Purpose

This note checks whether an earlier finding is just an accident of what the corpus mostly contains. The earlier scope probe found a queue of short side marks — one- or two-sign rows on objects that carry writing on more than one side — but most of them came from Harappa tablets. Splitting the queue into strata, meaning groups defined so that site and object type are held fixed inside each one, tests whether the pattern is only that concentration. The two strata are:

- Harappa `TAB:B`
- Harappa `TAB:I`

The goal is to check whether the short side-mark queue is only a broad Harappa/tablet artifact, or whether it still has stable token behavior inside the two main tablet types.

It does not assign numerical values. It does not identify metrological signs. It does not translate. It only tests whether the short-mark review queue survives a first type-site stratification.

## Local Artifacts

```text
data/open_prototype/tools/lipi_multiside_mark_stratified_probe.mjs
data/open_prototype/reports/lipi_multiside_mark_stratified_token_counts.csv
data/open_prototype/reports/lipi_multiside_mark_stratified_pair_counts.csv
data/open_prototype/reports/lipi_multiside_mark_stratified_side_index.csv
data/open_prototype/reports/lipi_multiside_mark_stratified_summary.json
```

Input:

```text
data/open_prototype/reports/lipi_multiside_mark_rows.csv
```

## Scope Counts

| Stratum | Rows | Short Mark Rows | Longer Text Rows | Short Mark Tokens | Longer Text Tokens | Candidate Tokens |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Harappa `TAB:B` | 687 | 222 | 246 | 444 | 1011 | 6 |
| Harappa `TAB:I` | 779 | 269 | 204 | 538 | 731 | 11 |

## Token Queue

The strongest short-mark tokens inside Harappa `TAB:B` are:

| Token | Short Mark Count | Longer Text Count | Smoothed Enrichment | Main Row Side Indexes |
| --- | ---: | ---: | ---: | --- |
| `034` | 42 | 0 | 176.278409 | `1:32;2:10` |
| `700` | 189 | 23 | 16.723283 | `1:103;2:85;3:1` |
| `033` | 73 | 31 | 4.839015 | `2:40;1:33` |
| `032` | 64 | 30 | 4.385712 | `2:34;1:30` |

The strongest short-mark tokens inside Harappa `TAB:I` are:

| Token | Short Mark Count | Longer Text Count | Smoothed Enrichment | Main Row Side Indexes |
| --- | ---: | ---: | ---: | --- |
| `034` | 72 | 2 | 38.274234 | `2:40;1:31;3:1` |
| `003` | 50 | 2 | 26.659983 | `3:22;1:17;2:11` |
| `700` | 179 | 9 | 24.937296 | `2:114;1:63;3:2` |
| `033` | 68 | 5 | 16.437524 | `2:48;1:19;3:1` |
| `861` | 28 | 6 | 5.786820 | `1:17;2:11` |
| `156` | 21 | 12 | 2.270058 | `3:21` |

`700`, `034`, and `033` survive in both strata. `003`, `861`, and `156` are more specific to Harappa `TAB:I` in this pass. `032` remains common in both, but its enrichment is much weaker in Harappa `TAB:I`.

## Side Index Distribution

| Stratum | Row Side Index | Short Mark Rows | Top Tokens |
| --- | ---: | ---: | --- |
| Harappa `TAB:B` | 1 | 115 | `700:103;033:33;034:32;032:30` |
| Harappa `TAB:B` | 2 | 106 | `700:85;033:40;032:34;034:10` |
| Harappa `TAB:B` | 3 | 1 | `125:1;700:1` |
| Harappa `TAB:I` | 1 | 94 | `700:63;034:31;033:19;003:17;861:17` |
| Harappa `TAB:I` | 2 | 149 | `700:114;033:48;034:40;032:25` |
| Harappa `TAB:I` | 3 | 26 | `003:22;156:21;700:2` |

The side-index pattern is not enough to infer physical side function. It is enough to define a sharper manual validation queue: inspect whether row side index 3 in Harappa `TAB:I`, especially `003` and `156`, corresponds to a distinct artifact-side marking practice or only catalog/entry structure.

## Co-Occurrence With Longer Text Rows

Top Harappa `TAB:B` artifact-group co-occurrences:

| Short Mark Token | Longer Text Token | Artifact Groups |
| --- | --- | ---: |
| `700` | `740` | 82 |
| `700` | `400` | 61 |
| `033` | `740` | 35 |
| `032` | `400` | 24 |
| `032` | `740` | 24 |
| `033` | `400` | 24 |
| `700` | `240` | 22 |
| `034` | `740` | 20 |

Top Harappa `TAB:I` artifact-group co-occurrences:

| Short Mark Token | Longer Text Token | Artifact Groups |
| --- | --- | ---: |
| `700` | `740` | 83 |
| `700` | `400` | 63 |
| `033` | `740` | 39 |
| `700` | `176` | 37 |
| `033` | `400` | 29 |
| `034` | `740` | 24 |
| `700` | `032` | 21 |
| `034` | `400` | 19 |

These are artifact-group co-occurrences only. They do not imply syntax, quantity, ownership, commodity, measure, or translation.

## Interpretation

The broad short-mark queue survives the first serious type-site split:

```text
Harappa TAB:B and Harappa TAB:I both contain recurrent clean short-mark rows dominated by tokens 700, 034, and 033, with TAB:I adding a sharper side-index-3 queue around 003 and 156.
```

This supports a better manual validation target for E3.2 — the project's identifier for the numerical/metrological work package — than broad dimension-bin prediction.

The result does not support:

- Numerical values.
- Standardized measures.
- Metrological readings.
- Commodity readings.
- Administrative tiers.
- Physical side interpretation without image or stronger catalog validation.
- Sign meanings.
- Phonetic values.
- Language identity.
- Translation.

## Consequence

The next E3.2 work should stop treating the whole short-mark queue as one blob. Use the following validation queues:

- Harappa `TAB:B`: `700`, `034`, `033`, `032`, especially side indexes 1 and 2.
- Harappa `TAB:I`: `700`, `034`, `033`, `003`, `861`, `156`, especially side index 3 for `003` and `156`.
- Cross-text co-occurrence: `700/034/033` against longer-text `740`, `400`, `176`, and `240`.

The next evidence step is manual artifact-side or image validation. Only after that should the project test whether these marks behave like counts, measures, side labels, administrative tags, or something else.

Follow-up:

- [Lipi short-mark orientation audit](lipi_short_mark_orientation_audit.md) tests the internal order of two-token `700` short marks inside this same Harappa `TAB:B`/`TAB:I` target space. It finds a corrected imbalance for `032`, `033`, and `034`, so exact order such as `+700-033+` versus `+033-700+` must remain separate until direction and source validation are done.
