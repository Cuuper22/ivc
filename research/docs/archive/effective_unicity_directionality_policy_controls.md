# Effective-Unicity Directionality Policy Controls

Date: 2026-05-29

## Purpose

This note records an adversarial control — a test built to break our own result — aimed at the recorded direction field in the catalog. The live directionality candidate is the working result that Indus inscriptions score better in their stored order than reversed. That candidate might be an artifact of a corpus direction convention, meaning a cataloguing habit about which way to write the signs down, rather than evidence about the direction on the actual seal. This test asks what the metadata layer, the catalog data alone, can and cannot prove.

Scope — the filtered slice of rows this test runs on:

- top-10 edge signs removed, so the most common first and last signs cannot carry the result,
- one-edit families collapsed, so near-identical inscriptions count once,
- Lipi T3 metadata/sign layer, our catalog-derived working table,
- 365 rows.

## Direction Distribution

| Recorded direction | Rows |
| --- | ---: |
| `R/L` | 354 |
| `L/R` | 11 |

The direction field is too imbalanced to validate a physical direction policy. Almost the entire harsh corpus is recorded `R/L`.

## Result

The directionality signal is not driven by the 11 `L/R` rows. Stored-win share below is the fraction of rows where the stored order scores higher than the reversed order:

| Scope / policy | Rows | Stored win share |
| --- | ---: | ---: |
| all harsh, stored as-is | 365 | 0.841096 |
| `R/L` only, stored as-is | 354 | 0.838983 |
| Mohenjo-daro `R/L` only | 209 | 0.813397 |
| Harappa `R/L` only | 104 | 0.769231 |
| all harsh, flip only `L/R` rows | 365 | 0.813699 |
| all harsh, flip only `R/L` rows | 365 | 0.813699 |

Random row flips kill the signal. The null columns come from a null model — repeated runs on data deliberately scrambled to destroy the effect under test, here by flipping each row's orientation at random:

| Scope | Random policy | Null mean | Null p95 | Null >= stored as-is |
| --- | --- | ---: | ---: | ---: |
| all harsh | random row flips | 0.471134 | 0.526027 | 0 |
| `R/L` only | random row flips | 0.469201 | 0.528249 | 0 |
| Mohenjo-daro `R/L` only | random row flips | 0.448268 | 0.521531 | 0 |
| Harappa `R/L` only | random row flips | 0.430923 | 0.538462 | 0 |

Random site flips weaken the pooled all-harsh score, with null p95 0.816438 below stored-as-is 0.841096. Direction-label flips are mostly uninformative because `R/L` dominates the corpus.

## Decision

Promote this as a boundary on the live candidate:

> The major-site directionality signal survives after restricting to recorded `R/L` rows and is destroyed by random row-level orientation flips. The current metadata layer therefore has coherent stored-order orientation, but it does not validate physical source direction because the recorded direction field is overwhelmingly `R/L` and inherited from corpus metadata.

Forbidden wording:

- Do not say the direction field proves source-image direction.
- Do not say the result establishes the correct physical reading direction.
- Do not use this to assign signs, sounds, meanings, language family, or translations.

## Artifacts

- `data/open_prototype/tools/effective_unicity_directionality_policy_controls.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_policy_controls_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_policy_controls.csv`
- `data/open_prototype/reports/effective_unicity_directionality_policy_null_summary.csv`
- `data/open_prototype/reports/effective_unicity_directionality_policy_null_iterations.csv`
