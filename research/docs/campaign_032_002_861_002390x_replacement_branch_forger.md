# 002-390-X Replacement Branch Forger

Date: 2026-05-31 America/Los_Angeles.

This is a replacement-run adversarial check for the source-normalized `002-390-X` lane. It does not use the quarantined `campaign_032_002_861_002390x_source_normalized_family_collapse` artifact.

## Inputs

- `data/open_prototype/reports/campaign_032_002_861_002390x_source_normalized_contrast_rows.csv`
- Input SHA-256: `f796bc663f906c83e114d207914e5b81702adb528aeedbbd191d613658f0773f`

Outputs:

- `data/open_prototype/tools/campaign_032_002_861_002390x_replacement_branch_forger.mjs`
- `data/open_prototype/reports/campaign_032_002_861_002390x_replacement_branch_forger_observed_branches.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_replacement_branch_forger_nulls.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_replacement_branch_forger_summary.json`

## Observed Pattern

In the 15-row `002-390-X` layer, `125` is the top branch:

| Branch | Raw rows | Continuation rows | Terminal rows | Strict source-visible rows | Strict source-visible objects |
| --- | ---: | ---: | ---: | ---: | --- |
| `125` | 4 | 4 | 0 | 2 | `M-119 M-735` |
| `095` | 2 | 0 | 2 | 1 | `M-71` |
| `705` | 2 | 0 | 2 | 0 |  |
| `692` | 1 | 0 | 1 | 1 | `M-70` |

The target branch survives exact formula collapse between `M-119` and `M-735`: they differ in full text, preceding sign before `002`, tail after `125`, symbol/cult, condition, and source route. It does not survive broad register collapse: both strict objects are Mohenjo-daro square steatite `SEAL:S` rows.

## Null Tests

The event tested was: target branch `125` has at least four raw rows, at least two strict source-visible rows, and no terminal rows after the branch.

| Null model | Iterations | Target event FPR | Discovery event FPR |
| --- | ---: | ---: | ---: |
| Shuffle branch labels across all rows | 50,000 | 0.004360 | 0.004360 |
| Shuffle within terminal/continuing status | 50,000 | 0.397360 | 0.397360 |
| Shuffle within strict-source-visible versus non-strict rows | 50,000 | 0.017660 | 0.017660 |
| Shuffle within site/type buckets | 50,000 | 0.012460 | 0.012460 |
| Shuffle within site/type/terminal buckets | 50,000 | 1.000000 | 1.000000 |

The broad-register-independent event has observed value false because the strict `125` pair is one broad register cell; it therefore cannot be promoted by any null model here.

## Decision

`002-390-125` is a live source-normalized structural candidate, not an accepted claim.

The reason is specific: the pattern is interesting under weak all-row shuffles, but the continuation-only part is not surprising once terminal status is preserved, and source/site-constrained nulls are too close to or above the adversarial threshold. The candidate needs a sharper gate: blind token-boxing of `M-119` and `M-735` plus matched source-visible controls, then a family/source-register null that no longer treats terminal continuation as free evidence.

Claim-ledger increment: 0.
