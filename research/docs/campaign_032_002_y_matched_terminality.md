# 032-002-Y Matched Terminality Campaign

Date: 2026-05-28

## Question

This note pits our explanation against the most obvious rival one. Signs in this corpus are numeric IDs; `Y` names whichever sign follows `002`. "Terminality" is whether a row ends right after `Y`. A "register" is the object class a row sits on — site, seal type, icon, shape — and the rival explanation is that register, not grammar, decides where rows stop. "Matched" means the comparison is made inside blocks of rows that share the same register, so register cannot do the explaining.

The post-Y campaign found a strong split:

```text
closure-heavy: 817, 820, 861
continuation-heavy: 390, 368, 031, 220, 900, 300
```

This campaign asks whether that split survives a hostile register baseline. If closure is mostly caused by site/object/icon or short row habits, then `site/type/symbol` should predict terminality about as well as Y class.

## Inputs

- Parent campaign: `campaign_032_002_post_y_continuation_campaign.md`
- Extraction script: `tmp/run_032_002_y_matched_terminality.py`
- Source rows:
  - `campaign_032_002_post_y_all_002_rows.csv`
  - `campaign_032_002_post_y_branch_rows.csv`

Outputs:

- `data/open_prototype/reports/campaign_032_002_y_matched_terminality_class_summary.csv`
- `data/open_prototype/reports/campaign_032_002_y_matched_terminality_block_contrasts.csv`
- `data/open_prototype/reports/campaign_032_002_y_matched_terminality_prediction_scores.csv`
- `data/open_prototype/reports/campaign_032_002_y_matched_terminality_summary.json`

Mechanic validation: PASS.

## Method

Rows are strict complete/closed and deduped by:

```text
text_dedup_key + site + type + idx_002
```

Scopes:

| scope | rows |
|---|---:|
| all strict dedup `002-Y` | 499 |
| adjacent strict dedup `032-002-Y` | 32 |

Y classes:

| class | signs |
|---|---|
| `hard_closure` | `817` |
| `leaky_closure` | `820`, `861` |
| `branch_head` | `390`, `368`, `031`, `220`, `900`, `300` |
| `small_n_closure_like` | small terminal-looking signs kept out of the main binary contrast |
| `other` | unresolved residue |

The test uses two approaches:

1. Leave-one-out prediction of terminality using different feature sets.
2. Matched block contrasts where the same block contains at least one closure-family and one branch-family row.

Important limitation: terminality is partly a right-edge property by definition. This test does not prove semantics. It tests whether Y class carries more signal than register metadata.

## Prediction Scores

Leave-one-out means each row is predicted by a model fitted without that row, so a model cannot score well by memorizing. Accuracy is the share predicted correctly; Brier and logloss measure how well-calibrated the predicted probabilities are, and lower is better for both.

Leave-one-out scores:

| scope | model | accuracy | brier | logloss |
|---|---|---:|---:|---:|
| all `002-Y` | global | 0.611222 | 0.238581 | 0.670200 |
| all `002-Y` | `site/type/symbol` | 0.579158 | 0.248248 | 0.690585 |
| all `002-Y` | `y_binary` | 0.847695 | 0.121984 | 0.395774 |
| all `002-Y` | `y_class` | 0.885772 | 0.097554 | 0.331038 |
| adjacent `032-002-Y` | global | 0.593750 | 0.256084 | 0.706236 |
| adjacent `032-002-Y` | `site/type/symbol` | 0.531250 | 0.284136 | 0.765472 |
| adjacent `032-002-Y` | `y_binary` | 0.843750 | 0.149621 | 0.483256 |
| adjacent `032-002-Y` | `y_class` | 0.906250 | 0.106698 | 0.381811 |

Result:

```text
Y class beats register-only in both the full 002-Y field and the adjacent 032-002 subset.
```

The exact-sign model is weaker than classing because singleton and sparse signs overfit or back off badly under leave-one-out. That is good: the result is not just memorizing each sign.

## Matched Blocks

Matched closure-vs-branch blocks found:

| scope | matched blocks |
|---|---:|
| all `002-Y` | 47 |
| adjacent `032-002-Y` | 17 |

Examples:

| block | closure behavior | branch behavior | implication |
|---|---|---|---|
| Mohenjo-daro / `SEAL:S` / `Bull1:W` | closure family 38/47 terminal | branch family 0/6 terminal | same major register still separates by Y class |
| Mohenjo-daro / `SEAL:S` / `Bull1:S` | 20/22 terminal | 0/6 terminal | closure/branch split survives inside a local icon block |
| Harappa / `SEAL:S` / `Bull1:W` | 16/16 terminal | 0/3 terminal | not Mohenjo-daro-only |
| adjacent `032-002`, Mohenjo-daro / `SEAL:S` / `Bull1:W` | 4/5 terminal | 0/1 terminal | target-near lane still shows class contrast |
| adjacent `032-002`, target `240-220-032` @ Mohenjo-daro / `SEAL:S` | 2/3 terminal | 0/1 terminal | small, but aligned with the class model |

There are still sparse-cell problems. But the direction is not ambiguous: when closure-family and branch-family signs occur in the same broad register block, branch-family signs overwhelmingly continue.

## Linguistic Read

The best current parse is:

```text
A-220-032  = frame/stem extension
002        = tail linker or boundary operator
Y          = classed exponent
post-Y     = optional continuation licensed by branch-head Y
```

`002` is not the ending. It is the sign before the closure/branch choice.

`817` behaves like a hard closure exponent. `820` and `861` behave like leaky closure exponents. `390`, `368`, `031`, `220`, `900`, and `300` behave like branch heads.

This is a grammatical claim about continuation licensing. It is not a translation, not a phonetic value, and not a language-family claim.

## Hostile Constraints

Still live:

- Source-normalized direction can still overturn "terminal" if catalog order is wrong.
- `Y class` was hand-defined from the same terminality pattern being tested, so the next pass must learn classes without prelabeling or use held-out signs/blocks.
- Sparse adjacent `032-002` cells make the narrow result fragile.
- Register metadata may be too coarse; a real plate/workshop/copy family — a set of near-identical objects that really count as one witness — could still explain part of the split.
- Text length and `002` position are not independent of terminality; this campaign only beats register baselines, not all right-edge artifacts.
- Strict dedup by text/site/type does not collapse all copy families, near-duplicate formula neighborhoods, or physical source-family repetitions.

## Decisions

Accepted:

- Register-only does not explain the post-`002` terminality split in the current strict dedup layer.
- Y-class behavior is stronger than site/type/symbol behavior for predicting terminality.
- The branch-lane model has earned the next semantic test.

Rejected:

- `site/type/symbol` as sufficient explanation for the closure/branch split.
- Exact Y value as meaning.
- Any translation or phonetic reading.

## Next Campaign

Run the hard holdout first, then the semantic test. A holdout is a test run once on evidence set aside in advance, so it cannot be tuned to pass.

Hard holdout:

```text
source-boxed + family-blocked + right-edge-matched
```

Requirements:

1. Source-box rows with independently checked physical direction and terminality.
2. Collapse exact, near-duplicate, and known copy/workshop/source-family rows.
3. Match on site/type/symbol, immediate neighbors, text length, and `002` position from the right.
4. Test whether Y class still predicts closure versus continuation.

If Y class fails there, this campaign is only terminal-sign leakage. If it survives, branch grammar becomes a serious structural object.

Then run the minimal-pair branch semantics test:

```text
X-220-032-002-closureY
X-220-032-002-branchY-Z
```

The first tail-family extraction is now stored in `campaign_032_002_post_y_tail_family_campaign.md`. It finds all-`002` tail pressure after `390`, `220`, and `861`, but the adjacent `032-002` subset remains mostly singleton tails.

Tasks:

1. Find near-matched pre-`002` frames where closure and branch-head Y alternate.
2. Cluster `Z` tails after branch-head Y.
3. Test whether `Z` correlates with object/register/icon better than fixed neighbor strings.
4. Source-check the decisive continuations: `M-240`, `M-91`, `M-1677`, `M-49`, `M-70`, and the unknown `390-590-032` row.

Pass:

- Branch-head Y predicts a recurring tail family or semantic/register partition after matched frame controls.

Fail:

- Post-Y material is only row residue, copy-family continuation, or source-normalization artifact.
