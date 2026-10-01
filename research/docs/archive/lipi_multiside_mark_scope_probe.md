# Lipi Multi-Side Mark Scope Probe

Date: 2026-05-24

## Purpose

This note starts the search for possible number or measure signs, but from the safe end. `lipi` is the project's filtered working corpus of Indus sign sequences; calling it a planning layer means it is unverified working data, good for deciding where to look and never usable as proof. Instead of guessing which signs are numerals from sign IDs, this probe asks whether that layer contains multi-side artifacts with short side marks that can become a review queue — a list of specific rows for a human to check against images.

It does not assign numerical values. It does not identify metrological signs. It does not translate. It only separates short side-mark candidates from longer text rows and reports enrichment patterns that need manual image/source validation.

## Local Artifacts

```text
data/open_prototype/tools/lipi_multiside_mark_scope_probe.mjs
data/open_prototype/reports/lipi_multiside_mark_rows.csv
data/open_prototype/reports/lipi_multiside_mark_token_counts.csv
data/open_prototype/reports/lipi_multiside_mark_pair_counts.csv
data/open_prototype/reports/lipi_multiside_mark_type_summary.csv
data/open_prototype/reports/lipi_multiside_mark_summary.json
```

Source file:

```text
data/open_prototype/lipi/metadata_filtered.csv
```

## Definitions

`multi-side or multi-row group` means a CISI artifact group with either multiple rows or a `sides` value above 1.

`clean side row` means:

- Numeric text is present.
- `complete = Y`.
- Direction is `R/L`, `L/R`, or `T/B`.
- Parsed token count matches stated text length.
- No `000` unknown signs.
- No question markers, brackets, or slash compounds.

`short mark candidate` means:

- Clean side row.
- Artifact has at least two sides or multiple rows.
- Parsed token count is 1 or 2.

This is only a working definition. It does not prove a row is a reverse mark or a number.

## Scope Counts

```text
source_rows: 5679
rows_with_cisi: 5018
cisi_groups: 4074
multiside_or_multirow_cisi_groups: 864
multiside_rows: 1808
clean_multiside_rows: 1109
short_mark_candidate_rows: 539
long_text_candidate_rows: 558
short_mark_token_total: 1078
non_short_token_total: 3022
enriched_short_mark_tokens: 19
```

Most short mark candidates are tablets:

| Type | Multi-Side Rows | Short Mark Rows | Long Text Rows | Multi-Side Artifacts |
| --- | ---: | ---: | ---: | ---: |
| `TAB:I` | 787 | 273 | 208 | 376 |
| `TAB:B` | 762 | 239 | 271 | 373 |
| `SEAL:S` | 65 | 10 | 24 | 25 |
| `TAB:C` | 76 | 5 | 34 | 38 |
| `SEAL:R` | 16 | 5 | 8 | 8 |

Most short mark rows are Harappa:

```text
Harappa: 497
Mohenjo-daro: 40
Kalibangan: 1
Unknown: 1
```

This concentration is a major caveat.

## Short Mark Token Queue

The strongest short-mark tokens by count and enrichment are:

| Token | Short Mark Count | Non-Short Count | Smoothed Enrichment | Main Types | Main Sites |
| --- | ---: | ---: | ---: | --- | --- |
| `700` | 374 | 65 | 14.750415 | `TAB:B`, `TAB:I` | Harappa |
| `033` | 146 | 61 | 6.145486 | `TAB:B`, `TAB:I` | Harappa |
| `034` | 115 | 9 | 31.365491 | `TAB:I`, `TAB:B` | Harappa |
| `032` | 105 | 98 | 2.763185 | `TAB:B`, `TAB:I` | Harappa |
| `003` | 51 | 19 | 6.813438 | `TAB:I` | Harappa |
| `861` | 30 | 29 | 2.667298 | `TAB:I` | Harappa |
| `156` | 28 | 20 | 3.586615 | `TAB:I`, `TAB:B` | Harappa |

The highest enrichment tokens among those with at least five short-mark occurrences are:

```text
034: 31.365491
167: 18.058919
700: 14.750415
003: 6.813438
137: 6.707599
033: 6.145486
```

The depletion queue is also useful. `740` appears only 15 times in short marks but 367 times in non-short multi-side text. That makes it a likely longer-text operator in this subset rather than a short side-mark token.

## Co-Occurrence With Longer Text Rows

The strongest artifact-level co-occurrences between short-mark tokens and longer text tokens are:

| Short Mark Token | Longer Text Token | Artifact Groups |
| --- | --- | ---: |
| `700` | `740` | 170 |
| `700` | `400` | 127 |
| `033` | `740` | 76 |
| `033` | `400` | 55 |
| `700` | `176` | 47 |
| `034` | `740` | 45 |
| `032` | `740` | 43 |
| `032` | `400` | 37 |
| `700` | `240` | 33 |
| `034` | `400` | 30 |

These are artifact-group co-occurrences only. They do not imply syntax, quantity, ownership, or translation.

## Interpretation

The probe supports this claim:

```text
The filtered `lipi` planning layer contains a concrete multi-side short-mark queue, dominated by Harappa tablets, with recurrent side-mark tokens such as `700`, `034`, `033`, `032`, and `003`.
```

The result does not support:

- Numerical values.
- Standardized measures.
- Metrological readings.
- Commodity readings.
- Administrative tiers.
- Reverse-side interpretation without side/image validation.
- Sign meanings.
- Phonetic values.
- Language identity.
- Translation.

## Consequence

This is now the better E3.2 path — E3.2 being the project's identifier for the numerical/metrological work package — than broad dimension-bin prediction.

The next numerical/metrological work should:

- Validate whether the short rows are true side/reverse marks using images or stronger catalog side metadata.
- Use the stratified Harappa `TAB:B` and `TAB:I` queue in [Lipi multi-side mark stratified probe](lipi_multiside_mark_stratified_probe.md).
- Test whether `700`, `034`, `033`, `032`, and `003` predict artifact-side count, row side index, long-text token classes, or measurements after type/site controls.
- Compare the short-mark behavior against known administrative token systems and known ancient multi-side tablets under artificial scarcity.
