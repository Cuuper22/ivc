# Lipi Broader Scope Probe

Date: 2026-05-24

## Purpose

This probe asks whether the filtered `lipi` metadata can give the project a broader, claim-free working scope than the current Mayig unicorn-seal subset.

It does not use the quarantined `sanskrit`, `translation`, or `notes` columns. It does not treat `lipi` as authoritative. It only measures whether a broad T3 source can propose artifact-class, site, and direction splits for later validation against stronger sources.

## Local Artifacts

```text
data/open_prototype/tools/lipi_scope_probe.mjs
data/open_prototype/reports/lipi_scope_rows.csv
data/open_prototype/reports/lipi_scope_by_type.csv
data/open_prototype/reports/lipi_scope_by_site.csv
data/open_prototype/reports/lipi_scope_by_region.csv
data/open_prototype/reports/lipi_scope_by_type_direction.csv
data/open_prototype/reports/lipi_scope_length_by_type.csv
data/open_prototype/reports/lipi_scope_readiness_summary.csv
data/open_prototype/reports/lipi_scope_candidates_by_type.csv
data/open_prototype/reports/lipi_scope_candidates_by_site.csv
data/open_prototype/reports/lipi_scope_summary.json
```

Source file:

```text
data/open_prototype/lipi/metadata_filtered.csv
```

## Candidate Definitions

`lipi_numeric_clean_candidate` means:

- CISI-style ID present.
- Numeric text present.
- `complete = Y`.
- Direction is `R/L` or `L/R`.
- Parsed token count matches the stated text length.
- No bracketed text, slash compounds, `000` unknown signs, or question markers.

`lipi_direction_clean_candidate` means:

- CISI-style ID present.
- Numeric text present.
- Direction is `R/L` or `L/R`.
- Parsed token count matches the stated text length.
- No bracketed text or question markers.

The second bucket can include rows with `000` unknown signs or slash compounds. It is for sensitivity-style direction/order tests, not core interpretation.

## Summary Counts

```text
rows: 5679
rows_with_cisi: 5018
rows_with_numeric_text: 5679
rows_complete_Y: 3673
rows_direction_RL: 4268
rows_direction_LR: 215
rows_direction_TB: 16
rows_lipi_numeric_clean_candidates: 2887
rows_lipi_direction_clean_candidates: 3308
rows_length_matches_parsed: 5646
rows_length_disagrees_parsed: 33
rows_complex_text: 2079
rows_with_000_unknown: 1337
rows_with_slash: 118
rows_with_bracket: 1438
```

The nested readiness buckets are:

| Bucket | Rows |
| --- | ---: |
| `lipi_numeric_clean_candidate` | 2,887 |
| `lipi_direction_clean_candidate` beyond numeric-clean | 421 |
| `audit_or_scope_only` | 2,371 |

## Artifact-Type Breadth

Top raw type counts:

| Type | Rows |
| --- | ---: |
| `SEAL:S` | 1,777 |
| `TAB:B` | 1,108 |
| `TAB:I` | 952 |
| `POT:T:g` | 538 |
| `SEAL:R` | 388 |
| `TAB:C` | 230 |
| `TAG` | 172 |

Clean candidate counts by type:

| Type | Rows | Numeric Clean | Direction Clean | Audit/Scope Only |
| --- | ---: | ---: | ---: | ---: |
| `SEAL:S` | 1,777 | 1,101 | 1,276 | 501 |
| `TAB:B` | 1,108 | 705 | 803 | 305 |
| `TAB:I` | 952 | 533 | 579 | 373 |
| `SEAL:R` | 388 | 218 | 240 | 148 |
| `TAB:C` | 230 | 157 | 179 | 51 |
| `POT:T:g` | 538 | 38 | 51 | 487 |
| `TAG` | 172 | 20 | 26 | 146 |
| `ROD` | 42 | 17 | 27 | 15 |

This is enough breadth to design artifact-class split experiments. It is not enough to accept the splits as authoritative, because `lipi` remains a T3 source.

## Site Breadth

Top raw site counts:

| Site | Rows |
| --- | ---: |
| Harappa | 2,717 |
| Mohenjo-daro | 1,923 |
| Dholavira | 238 |
| Kalibangan | 212 |
| Lothal | 208 |
| Chanhu-daro | 74 |

Clean candidate counts by site:

| Site | Rows | Numeric Clean | Direction Clean | Audit/Scope Only |
| --- | ---: | ---: | ---: | ---: |
| Harappa | 2,717 | 1,430 | 1,592 | 1,125 |
| Mohenjo-daro | 1,923 | 1,217 | 1,419 | 504 |
| Lothal | 208 | 84 | 101 | 107 |
| Kalibangan | 212 | 55 | 74 | 138 |
| Chanhu-daro | 74 | 35 | 50 | 24 |
| Nausharo | 38 | 16 | 16 | 22 |

Dholavira has 238 raw rows but only 1 numeric-clean candidate under this conservative filter. That makes it a scope warning, not an absence claim.

## Interpretation

The filtered `lipi` layer gives a much broader planning surface than the Mayig open prototype:

- Multiple artifact classes are represented.
- Harappa and Mohenjo-daro both have large candidate pools.
- Tablets and sealings have enough rows for first artifact-class baselines.
- Pottery marks, tags, rods, bangles, and Dholavira-style cases mostly fall into audit/scope-only buckets under strict filters.

This means the next structural experiments can be designed as broad-corpus scouts, but any result must remain below the corpus-authority gate until cross-source or image validation is done.

The first such scout is now recorded here:

[Lipi broad order baseline](lipi_broad_order_baseline.md)

## Result

This probe supports only this claim:

```text
The filtered `lipi` dataset, with claim columns removed, can propose broader artifact-class and site splits for future structural experiments, including 2,887 strict numeric-clean candidates and 3,308 direction-clean candidates.
```

It does not support:

- Authoritative corpus statistics.
- Accepted sign segmentation.
- Accepted sign readings.
- Semantic fields.
- Phonetic values.
- Translation.

## Next Falsification

The next experiments should ask:

- Do the broad `lipi` order results survive exact-duplicate collapse and formula-family downweighting?
- Do Harappa-held-out and Mohenjo-daro-held-out baselines preserve masked-sign prediction after exact-duplicate collapse and edge-sign controls?
- Do artifact-class baselines survive after excluding `000`, brackets, and slash compounds?
- Can Dholavira and long inscriptions be treated with a separate uncertainty policy rather than forced into the short-inscription baseline?
- Which broad `lipi` splits survive cross-checking against M77/CISI/ICIT or primary images?
