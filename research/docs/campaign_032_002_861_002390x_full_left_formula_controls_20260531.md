# 002-390-X full-left formula controls

Date: 2026-05-31 America/Los_Angeles

Status: `full_left_formula_controls_break_head_determinism_but_no_branch_promotion_no_values`.

## Purpose

This gate tests the current adversarial explanation that the `002-390-X` pattern is just a whole-left formula/template effect. The question is not whether `390-X` behaves generically after `390`; that was tested separately. The question here is whether the complete sign sequence before `002` already determines `002-390`, or whether the same left formula can feed other post-`002` heads.

Accepted value, phonetics, language identity, function, sign meaning, and translation remain 0.

## Inputs And Outputs

- Runner: `data/open_prototype/tools/campaign_032_002_861_002390x_full_left_formula_controls_20260531.mjs`
- Input metadata: `data/open_prototype/lipi/metadata_filtered.csv`
- Source-tier input for row status: `data/open_prototype/reports/campaign_032_002_861_002390x_branch_sign_ecology_20260531_002390_frames.csv`
- All `002` occurrences: `data/open_prototype/reports/campaign_032_002_861_002390x_full_left_formula_controls_20260531_all_002_occurrences.csv`
- Target controls: `data/open_prototype/reports/campaign_032_002_861_002390x_full_left_formula_controls_20260531_target_controls.csv`
- Full-left groups: `data/open_prototype/reports/campaign_032_002_861_002390x_full_left_formula_controls_20260531_full_left_groups.csv`
- Decisions: `data/open_prototype/reports/campaign_032_002_861_002390x_full_left_formula_controls_20260531_decisions.csv`
- Summary: `data/open_prototype/reports/campaign_032_002_861_002390x_full_left_formula_controls_20260531_summary.json`

## Counts

- All local `002` occurrences scanned: `851`.
- Adjacent target `002-390-X` frames: `15`.
- Exact full-left target frames with alternate post-`002` heads: `7`.
- Exact full-left groups with multiple `002-390-X` branch alternatives: `0`.
- Exact full-left singleton target frames: `4`.
- Singleton exact-prefix rows with broader last2-left alternate post-`002` heads: `4`.
- Exact full-left same-branch residue targets: `0`.

## Exact Full-Left Controls

Seven of the fifteen target rows have exact full-left controls where the same complete left sequence before `002` takes a different post-`002` head somewhere in the metadata:

| Target | Full left before `002` | Post-`002` heads in exact full-left group | Consequence |
|---|---|---|---|
| H-773 | `740 798 803` | `000:1; 390:1` | `002-390` is not forced by the full-left formula. |
| M-213 | `740 384` | `390:1; 629:1` | `002-390` is not forced by the full-left formula. |
| M-232 | `236` | `861:3; 308:1; 390:1; 820:1` | `002-390` is one branch among several after the same left. |
| M-708 | `740 061` | `817:2; 390:1; 400:1; 455:1; 575:1; 703:1` | Strong anti-determinism control. |
| M-735 | `740 760 235` | `390:1; 861:1` | The strict `125` continuation witness is not full-left deterministic for `390`. |
| 3335.1 | `740 205 032` | `252:1; 390:1` | Still object-ID blocked, but the left formula does not force `390`. |
| Sktd-1 | `390 004` | `817:4; 861:2; 031:1; 390:1; 705:1; 820:1` | The `004` lane remains a real branch batch, but Sktd-1 itself is not strict. |

This damages the adversarial claim that `002-390-X` is fully determined by whole-left formula templates. In these rows, the same complete left formula can choose another head after `002`.

## Promotion Block

The same experiment found `0` exact full-left groups with multiple `002-390-X` branch alternatives. That is the decisive brake.

The gate therefore does not yet show a matched paradigm like:

`same complete left -> 002-390-125`

against

`same complete left -> 002-390-095/692/705/...`

Without that matched branch split, the full-left result weakens one adversary but does not promote grammar, function, or sign value.

## Singleton Exact-Prefix Rows

Four target frames remain exact full-left singletons:

| Target | Full left before `002` | Branch | Status consequence |
|---|---|---|---|
| M-71 | `151 279 142` | `390-095` | Strict source-visible comparator, but no exact full-left control. |
| M-119 | `151 337 484` | `390-125` | Strict source-visible `125` witness, but no exact full-left control. |
| M-1825 | `157 031` | `390-705` | Acquisition-packeted, sign-band dark. |
| Dholavira 4237.1 | `151 032 388` | `390-705` | `8758 / ZA-12:2` acquisition-hot but unbound. |

Broader last2-left controls add pressure for H-1993, H-68, M-38, and M-70, but those controls are deliberately weaker than exact full-left controls and cannot promote the construction.

## Decision

The positive model survives in a narrower form:

`002-390-X` remains a live branch-tail ecology. Whole-left formula determinism is not enough to explain at least `7/15` target rows, and the generic `390-X` adversary already failed to explain the in-frame `125` and `095` behavior.

The adversarial model also survives:

No exact full-left group currently gives a source-controlled branch split inside `002-390-X`. Strict grammar/function promotion remains blocked until H-1993, `705`, `3335.1`, or a new row supplies a matched exact-left or strict same-predecessor branch alternative.

## Next Gate

Do not defend `125` as a value. The next useful gate is one of:

1. Bind H-1993 to test the `004 -> 002-390 -> 095` route against Sktd-1's `004 -> 002-390 -> 125 -> 820` pressure.
2. Bind Dholavira `8758 / ZA-12:2` or M-1825 to make repeated terminal `705` source-visible.
3. Find a strict exact-left or same-predecessor branch split inside `002-390-X`.
4. Keep `3335.1` out of promotion until both object/source binding and `390-590-032` formula-family collapse are solved.

Run-control reminder: this is campaign progress inside the original moonshot decipherment goal, not a completion condition.
