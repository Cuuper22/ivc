# 002-390-X left-context radius scan

Date: 2026-05-31 America/Los_Angeles

Status: `left_context_radius_scan_immediate_splits_source_blocked_no_values`.

## Purpose

The source-tiered predecessor gate tested immediate predecessor only. The full-left formula gate tested complete left formula. This scan fills the gap between them by grouping the same `15` adjacent `002-390-X` frames by left-context suffix radius:

- radius `1`: immediate predecessor before `002`
- radius `2`: last two signs before `002`
- ...
- radius `8`: longest left suffix present in the target set

The question is where branch alternatives actually exist. A decipherment-useful paradigm would look like this: at some matched left-context radius, the same context takes different branch signs, and that split survives source control.

Accepted value, phonetics, language identity, function, sign meaning, and translation remain 0.

## Inputs And Outputs

- Runner: `data/open_prototype/tools/campaign_032_002_861_002390x_left_context_radius_scan_20260531.mjs`
- Input: `data/open_prototype/reports/campaign_032_002_861_002390x_full_left_formula_controls_20260531_target_controls.csv`
- Target/radius rows: `data/open_prototype/reports/campaign_032_002_861_002390x_left_context_radius_scan_20260531_target_radius_rows.csv`
- Radius groups: `data/open_prototype/reports/campaign_032_002_861_002390x_left_context_radius_scan_20260531_groups.csv`
- Radius summary: `data/open_prototype/reports/campaign_032_002_861_002390x_left_context_radius_scan_20260531_radius_summary.csv`
- Decisions: `data/open_prototype/reports/campaign_032_002_861_002390x_left_context_radius_scan_20260531_decisions.csv`
- Summary: `data/open_prototype/reports/campaign_032_002_861_002390x_left_context_radius_scan_20260531_summary.json`

## Result

Across the `15` adjacent `002-390-X` frames:

| Radius | Groups | Multirow groups | Branch-split groups | Strict branch-split groups |
|---:|---:|---:|---:|---:|
| 1 | 12 | 3 | 2 | 0 |
| 2 | 14 | 0 | 0 | 0 |
| 3 | 9 | 0 | 0 | 0 |
| 4 | 3 | 0 | 0 | 0 |
| 5 | 1 | 0 | 0 | 0 |
| 6 | 1 | 0 | 0 | 0 |
| 7 | 1 | 0 | 0 | 0 |
| 8 | 1 | 0 | 0 | 0 |

Branch alternatives exist only at radius `1`, the immediate predecessor before `002`. Widen the left context to last2 or beyond and they vanish.

## The Two Split Lanes

| Immediate predecessor | Branches | Source state | Decision |
|---|---|---|---|
| `004` | `095:1; 125:1` | H-1993 is route/metadata pressure; Sktd-1 is public-panel downweighted. | Non-strict split only. Bind H-1993 before promotion. |
| `032` | `590:1; 692:1` | M-70 is strict visible; `3335.1` is metadata/object blocked. | Partly strict split, blocked by `3335.1`. |

The `235` group is not a branch split:

| Immediate predecessor | Branches | Source state | Decision |
|---|---|---|---|
| `235` | `125:2` | M-38 is metadata/weak; M-735 is strict visible. | Same-branch tail split, not branch alternation. |

## Interpretation

This scan sharpens the model fight:

- The positive model keeps the immediate-predecessor branch-tail ecology alive. The only branch alternatives are exactly the already-live `004` and `032` lanes.
- The adversarial model keeps the grammar/function promotion block. There are `0` strict source-visible branch-split groups across all radii, and no branch split survives once context is widened to radius `2`.
- The full-left result remains useful but limited: it weakens deterministic-template collapse for post-`002` head choice, while this radius scan confirms it does not rescue a matched `002-390-X` branch paradigm.

## Decision

Current status: `left_context_radius_scan_immediate_splits_source_blocked_no_values`.

The live object remains:

`immediate predecessor -> 002-390 -> branch sign -> tail behavior`

The decisive rows are still:

- `004`: H-1993 `095` versus Sktd-1 `125`, blocked because H-1993 lacks image binding and Sktd-1 is wrapped/not strict.
- `032`: M-70 `692` versus `3335.1` `590-032`, blocked because `3335.1` lacks object/source binding and is formula-family pressured.
- `235`: M-38/M-735 same `125` branch, useful only for tail-subframe stress.

## Next Gate

This result prioritizes acquisition and replacement witnesses:

1. Bind H-1993 or find another strict `004 -> 002-390 -> non-125` row.
2. Bind `3335.1` or find another strict `032 -> 002-390 -> non-692/non-125` branch alternative.
3. Bind Dholavira `8758 / ZA-12:2` or M-1825 only if the goal is repeated `705` source control; neither currently creates a matched radius split.
4. Keep searching for source-bound terminal `125` or continuing non-`125` inside true `002-390-X`, but do not convert the current pattern into a value or function.

Run-control reminder: this is campaign progress inside the original moonshot decipherment goal, not a completion condition.
