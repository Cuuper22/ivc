# 002-390-X re-earned family collapse

Date: 2026-05-31 America/Los_Angeles

This note redoes an analysis from scratch. An earlier "family collapse" run — a pass that groups the `002-390-X` rows into families and tests whether any subpattern deserves promotion — was quarantined, meaning its outputs were sealed off and may not be cited. "Re-earned" means every number here was recomputed from clean inputs without touching the quarantined material. The result: the two tempting subpattern claims are demoted, not promoted.

Status: `reearned_family_collapse_demotes_subframes_no_values`.

## Boundary

This is the clean replacement for the quarantined post-cutoff `campaign_032_002_861_002390x_source_normalized_family_collapse` artifact. The quarantined script and reports were not imported, read, or cited as settled evidence.

Inputs:

- Re-earned frame table: `data/open_prototype/reports/campaign_032_002_861_002390x_branch_sign_ecology_20260531_002390_frames.csv`
- Local metadata: `data/open_prototype/lipi/metadata_filtered.csv`
- Runner: `data/open_prototype/tools/campaign_032_002_861_002390x_reearned_family_collapse_20260531.mjs`

Accepted value, phonetics, language identity, function, sign meaning, and translation remain 0.

## Outputs

- `data/open_prototype/reports/campaign_032_002_861_002390x_reearned_family_collapse_20260531_frames.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_reearned_family_collapse_20260531_branch_summary.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_reearned_family_collapse_20260531_prev235_rows.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_reearned_family_collapse_20260531_tail_125632032_rows.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_reearned_family_collapse_20260531_decisions.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_reearned_family_collapse_20260531_summary.json`

## Main Counts

In this table, a "frame" is one occurrence of `002-390` plus its neighboring signs, and "strict" means the row's reading is backed by an inspectable source image.

| Gate | Result | Consequence |
|---|---:|---|
| Adjacent `002-390-X` frames | 15 | Same live frame set as the replacement branch ecology run. |
| Branch signs | 10 | Branch diversity remains structural pressure only. |
| `235 -> 002-390 -> 125` rows | 2 raw / 2 family cells / 1 strict | One strict witness plus one weak/non-strict witness cannot promote a subframe. |
| Global `125-632-032` rows | 4 | Tail-family pressure expands beyond the frame. |
| In-frame `125-632-032` rows | 2 raw / 1 strict | The in-frame tail is not independently proven. |
| Repeated `002-390-705` rows | 2 raw / 0 strict | Dholavira and M-1825 are contact-pending acquisition branches only. |

## Decisions

1. `235_002390125_subframe_demoted`: `M-38` and `M-735` are the two raw rows, but only `M-735` is strict-visible.
2. `125_632_032_tail_family_pressure`: `125-632-032` occurs in `M-1692`, `M-38`, `M-119`, and `M-1188`; only `M-38/M-119` are inside `002-390-125`, and only `M-119` is strict in-frame.
3. `705_repeated_branch_contacts_pending_zero_strict`: Dholavira `4237.1` and `M-1825` are both request-sent, but neither is source-bound.
4. `strict_family_core_unmatched`: strict rows preserve branch-tail polarity but still have no strict same-predecessor branch split — no pair of source-backed rows that share the sign before `002` yet diverge after `390`.

## Decision

The positive branch-tail ecology remains alive, but the two tempting subframe claims are demoted rather than promoted. The adversarial copied/formula-family model — the rival explanation that these sequences are copies of one formula rather than productive structure — still survives, because the clean strict layer has polarity without a matched predecessor split, and because `125-632-032` spreads outside the in-frame pair.

Current status: `reearned_family_collapse_demotes_subframes_no_values`.
