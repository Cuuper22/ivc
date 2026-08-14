# Effective-Unicity Directionality Site-Balance Control

Date: 2026-05-29

## Purpose

This note records a control run against the directionality candidate — the working result that Indus inscriptions score better in their recorded order than reversed. It exists because that result might be nothing but an accident of where the inscriptions come from.

The harsh directionality scope — "harsh" meaning the filtered slice built to make the result as hard to obtain as possible — is site-imbalanced. After top-10 edge removal (dropping rows whose first or last sign is one of the ten commonest) and one-edit-family collapse (counting near-identical inscriptions once), the current Lipi T3 layer, our catalog-derived working table, has 365 rows:

| Site | Rows |
| --- | ---: |
| Mohenjo-daro | 212 |
| Harappa | 112 |
| Lothal | 16 |
| Kalibangan | 7 |
| Chanhu-daro | 6 |
| Allahdino | 3 |
| Nausharo | 3 |
| Bala-kot | 2 |
| Banawali | 2 |
| Khirsara | 1 |
| Unknown | 1 |

This control asks whether the directionality signal is just raw site imbalance. It repeatedly samples equal row counts from selected sites, scores stored order versus reversed order, and compares paired null scores on the same sampled rows. A null is the same scoring run on deliberately scrambled data, so it shows how often chance alone would produce what we see. Stored-win share below is the fraction of rows where the stored order beats the reversed order.

## Result

The result is narrower than the broad directionality headline.

The Mohenjo-daro plus Harappa balanced design survives:

- cap per site: 112
- rows per iteration: 224
- iterations: 1,000
- observed median stored-win share: 0.803571
- observed p05 to p95: 0.776786 to 0.834821
- max paired null >= observed share: 0.003

Adding Lothal makes the balanced sample too small and null-compatible:

- cap per site: 16
- rows per iteration: 48
- observed median stored-win share: 0.541667
- max paired null >= observed share: 0.528

Balancing the top five sites is weaker:

- cap per site: 6
- rows per iteration: 30
- observed median stored-win share: 0.433333
- max paired null >= observed share: 0.616

## Null Controls

Each sampled iteration uses paired nulls over the same rows:

- global token shuffle,
- row-internal shuffle,
- position-slot shuffle,
- edge-frame shuffle,
- site-position shuffle,
- site-edge-interior shuffle.

For the Mohenjo-daro plus Harappa design, the strongest null pressure is site-position shuffle: paired null >= observed share 0.003. For the three-site and five-site designs, site-position shuffles reproduce or exceed the observed score often enough to block the claim.

## Decision

Promote this as a boundary on the live candidate, not as an accepted claim:

> Harsh Indus directionality is not merely raw imbalance between Mohenjo-daro and Harappa; it survives balanced resampling across those two major sites. The current data do not show a robust multisite-balanced directionality result once Lothal and smaller sites are forced into equal weight.

Forbidden wording:

- Do not say the directionality result is pan-Indus.
- Do not say it proves writing, sound, meaning, translation, or language family.
- Do not describe the multisite-balanced controls as supportive.

## Artifacts

- `data/open_prototype/tools/effective_unicity_directionality_site_balance.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_site_balance_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_site_balance.csv`
- `data/open_prototype/reports/effective_unicity_directionality_site_balance_iterations.csv`
- `data/open_prototype/reports/effective_unicity_directionality_site_balance_null_summary.csv`
