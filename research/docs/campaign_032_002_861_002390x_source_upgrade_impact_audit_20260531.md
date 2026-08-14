# 002-390-X source-upgrade impact audit

Date: 2026-05-31 America/Los_Angeles

This note is a planning exercise. Several seals in the campaign are blocked because we have no photograph of them. Chasing them all costs time, so this audit asks, one seal at a time: if we did get that photograph tomorrow, what would it actually buy us? The answer reorders the acquisition queue, and it is not the order the backlog suggests.

Status: `source_upgrade_impact_audit_3335_single_unlock_004_dual_upgrade_705_ecology_no_values`.

## Purpose

A "lane" is a specific left-to-right pattern: which sign comes right before `002-390`, and which sign follows it. A "matched" lane is one where two rows share that preceding sign, so their branches can be compared fairly. A "witness" is a database row that attests a sign sequence. The matched-lane replacement scout showed that the surviving local matched lanes have no backup witness:

- `004`: H-1993 / Sktd-1
- `032`: M-70 / `3335.1`

This audit asks what would actually change if a blocked row became strict source-visible — that is, if its reading could be checked against an inspectable source photograph. It is a counterfactual acquisition-priority gate (a "gate" being a check that must pass before evidence enters the analysis), not evidence that any row has been upgraded.

Accepted value, phonetics, language identity, function, sign meaning, and translation remain 0.

## Inputs And Outputs

- Runner: `data/open_prototype/tools/campaign_032_002_861_002390x_source_upgrade_impact_audit_20260531.mjs`
- Input: `data/open_prototype/reports/campaign_032_002_861_002390x_branch_sign_ecology_20260531_002390_frames.csv`
- Scenario summary: `data/open_prototype/reports/campaign_032_002_861_002390x_source_upgrade_impact_audit_20260531_scenario_summary.csv`
- Strict predecessor groups: `data/open_prototype/reports/campaign_032_002_861_002390x_source_upgrade_impact_audit_20260531_strict_prev_groups.csv`
- Strict branch summary: `data/open_prototype/reports/campaign_032_002_861_002390x_source_upgrade_impact_audit_20260531_strict_branch_summary.csv`
- Decisions: `data/open_prototype/reports/campaign_032_002_861_002390x_source_upgrade_impact_audit_20260531_decisions.csv`
- Summary: `data/open_prototype/reports/campaign_032_002_861_002390x_source_upgrade_impact_audit_20260531_summary.json`

## Main Result

The acquisition priority is not what a simple reading of the backlog suggests. In the table below, "ecology" means the study of which signs appear around the branch point — useful background pressure, but weaker than a matched split.

| Hypothetical source upgrade | Strict matched predecessor split unlocked? | Other effect | Decision |
|---|---:|---|---|
| H-1993 only | `0` | Adds strict `004 -> 002-390 -> 095`, but Sktd-1 remains non-strict. | Necessary but insufficient for strict `004`. |
| Sktd-1 only | `0` | Expands strict `125` continuation set to `3`. | Still lacks strict non-`125` comparator in `004`. |
| H-1993 + Sktd-1 | `1`: `004:095/125` | Expands strict `125` continuation set. | Full `004` gate requires dual strict sides under current inventory. |
| `3335.1` only | `1`: `032:590/692` | Creates strict non-`125` continuing exception `590 -> 032`. | Highest single-object matched-gate unlock, because M-70 is already strict. |
| M-1825 only | `0` | One strict terminal `705`. | Ecology only. |
| Dholavira `4237.1` only | `0` | One strict terminal `705`. | Ecology only. |
| M-1825 + Dholavira `4237.1` | `0` | Repeated strict terminal `705` pair. | Strong ecology, not matched-lane proof. |
| M-38 | `0` | Expands strict `125` continuation set; makes `235` a strict same-branch tail split with M-735. | Tail-subframe stress, not branch split. |
| H-773 | `0` | Creates strict non-`125` continuing exception `530 -> 741`. | Adversarial polarity test, not matched-lane proof. |

## Decisions

### H-1993 Alone Is Not Enough

Binding H-1993 would produce a strict `004 -> 002-390 -> 095` side, but the other known `004` branch, Sktd-1 `004 -> 002-390 -> 125-820`, remains wrapped/public-panel downweighted. Under the current strict-gate rule, H-1993 alone gives `0` strict matched predecessor splits.

This corrects the campaign wording: H-1993 is necessary for the `004` lane, but not sufficient unless Sktd-1 also becomes strict or a new strict `004 -> 002-390 -> 125` witness appears.

### `3335.1` Is The Highest Single-Object Matched-Gate Unlock

If `3335.1` were source-bound and its sign sequence were validated, it would pair with already-strict M-70:

- M-70: `032 -> 002-390 -> 692 -> <END>`
- `3335.1`: `032 -> 002-390 -> 590 -> 032`

That would create a strict `032` matched-predecessor branch split. It would also create a strict non-`125` continuing exception, which is a hard adversarial test for the current closure/continuation polarity.

This still would not be a reading. `3335.1` would then need to survive object/source binding, token-order proof, and the existing `390-590-032` formula-family pressure.

### `705` Is Ecology, Not Matched-Lane Proof

If both M-1825 and Dholavira `4237.1` became strict, the campaign would gain a repeated strict terminal `705` pair:

- M-1825: `031 -> 002-390 -> 705 -> <END>`
- Dholavira `4237.1`: `388 -> 002-390 -> 705 -> <END>`

That would strongly improve branch-tail ecology, but it would not create a matched predecessor split because the predecessors differ and neither is `004` or `032`.

### H-773 Is An Adversarial Polarity Test

If H-773 target side became strict, it would create a strict non-`125` continuing exception:

- H-773: `803 -> 002-390 -> 530 -> 741`

That would attack the lazy version of the polarity model. It would not unlock matched-lane proof.

### M-38 Is Tail-Subframe Stress

If M-38 became strict, it would pair with M-735 under predecessor `235`, but both rows choose branch `125`:

- M-38: `235 -> 002-390 -> 125 -> 632 032`
- M-735: `235 -> 002-390 -> 125 -> 195`

This would improve strict evidence for `125` continuation and tail-subframe variation, not branch alternation.

## Priority Change

For matched-branch proof, the ranked acquisition logic is now:

1. `3335.1` or an equivalent strict `032 -> 002-390 -> non-692/non-125` row, because it is a single-object matched-gate unlock with M-70 already strict.
2. H-1993 plus Sktd-1 strict token/order proof, or an equivalent dual strict `004` pair.
3. M-1825 + Dholavira `4237.1` for repeated `705` ecology.
4. H-773 as a polarity adversary.
5. M-38 as tail-subframe stress.

Run-control reminder: this is campaign progress inside the original moonshot decipherment goal, not a completion condition.
