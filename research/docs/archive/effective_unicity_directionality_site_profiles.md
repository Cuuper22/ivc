# Effective-Unicity Directionality Site Profiles

Date: 2026-05-29

## Purpose

This note breaks the directionality result apart by excavation site. Directionality is the working result that Indus inscriptions score better in their recorded order than reversed.

The site-balanced control showed that Mohenjo-daro plus Harappa survives balanced resampling, while Lothal-inclusive and top-five-site balanced designs do not. This profile asks the direct follow-up question: does each adequately sized site carry internal directionality on its own?

The scope is the harsh directionality layer — "harsh" meaning the slice filtered to make the result as hard to obtain as possible:

- top-10 edge signs removed, so the commonest first and last signs cannot carry the result,
- one-edit families collapsed, so near-identical inscriptions count once,
- Lipi T3 metadata/sign layer, our catalog-derived working table,
- minimum included site size: 10 rows.

## Result

Stored-win share is the fraction of rows where the stored order beats the reversed order. Max null >= observed is the worst case across the null controls — runs on deliberately scrambled data — giving the fraction of scrambled runs that matched or beat the real score. Small values mean the signal is hard to fake.

| Site | Rows | Stored win share | Max null >= observed |
| --- | ---: | ---: | ---: |
| Mohenjo-daro | 212 | 0.816038 | 0.002 |
| Harappa | 112 | 0.741071 | 0.004 |
| Lothal | 16 | 0.312500 | 0.988 |

Mohenjo-daro and Harappa each carry internal stored-order asymmetry under within-site leave-one-row-out scoring. Lothal does not. This explains why the Mohenjo-daro plus Harappa balanced control survives, while Lothal-inclusive balancing becomes null-compatible.

## Controls

Each site is scored against 1,000 iterations per control:

- global token shuffle,
- row-internal shuffle,
- position-slot shuffle,
- edge-frame shuffle.

The tested null is site-local: each null is generated only from that site's rows, so Mohenjo-daro cannot lend directionality to Harappa or Lothal inside this profile.

## Decision

Promote this as a live boundary:

> In the harsh current Lipi T3 layer, the directionality signal is independently visible inside Mohenjo-daro and Harappa, but not inside Lothal. Smaller sites remain unresolved because they have fewer than 10 rows in this harsh scope.

Forbidden wording:

- Do not say Lothal is non-directional as a site in general.
- Do not say the result is pan-Indus.
- Do not promote this to an accepted structural finding until source-image direction and source-family controls are complete.

## Artifacts

- `data/open_prototype/tools/effective_unicity_directionality_site_profiles.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_site_profiles_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_site_profiles.csv`
- `data/open_prototype/reports/effective_unicity_directionality_site_profiles_null_summary.csv`
- `data/open_prototype/reports/effective_unicity_directionality_site_profiles_null_iterations.csv`
