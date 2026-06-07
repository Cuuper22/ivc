# 032-002-861 Terminal-Space Recut V2

Date: 2026-05-29

## Question

After quantifying the two visual-only blockers (`M-355` and `M-1267`), does any source-visible bare closure after `002-861` show tail-sized same-line terminal opportunity?

This is still a source/layout campaign. It does not assign values, phonetics, language identity, or translations.

## Inputs

- Prior metrics: `data\open_prototype\reports\campaign_032_002_861_source_first_terminal_space_metrics.csv`
- Script: `tmp/run_032_002_861_terminal_space_blind_recut_v2.py`
- Contact sheet: `C:\Users\Acer\OneDrive\Documents\ivc\tmp\032_002_861_terminal_space_recut_v2\campaign_032_002_861_terminal_space_recut_v2_contact_sheet.png`
- Quantified rows after recut: `14` of `14`
- Newly quantified rows: `M-355`, `M-1267`

## Result

The recut strengthens the terminal-space adversary.

Tailed terminal-content windows now span `120-525px`; bare same-line post-terminal margins span `28-45px`.

The largest measured bare margin is `45px`, still below the smallest measured tailed window `120px`.

`M-355` is no longer just a visual note: it is a quantified long-continuation adversary. `M-1267` is now a quantified bare control, but it still does not provide tail-sized same-line empty terminal space.

The source review sheet hides row labels and tail classes; the metric sheet is unblinded after measurement. This is a tail-hidden manual recut, not a claim of fully independent blind epigraphy.

## Class State

| Class | Rows | Quantified | Width or margin range | Verdict |
|---|---:|---:|---|---|
| `closure` | 7 | 7 | margin 28-45px / share 0.040-0.063 | bare_controls_still_lack_tail_sized_same_line_terminal_margin |
| `fixed_pair` | 3 | 3 | tail-window 195-265px / share 0.331-0.433 | same_line_fixed_pair_survives_but_large_terminal_window_and_register_pressure_remain |
| `long_continuation` | 1 | 1 | tail-window 525-525px / share 0.395-0.395 | now_quantified_as_large_same_line_terminal_continuation_adversary |
| `simple_single` | 3 | 3 | tail-window 120-225px / share 0.177-0.286 | same_line_simple_tail_survives_but_terminal_space_adversary_remains |

## Decisions

- `visual_only_blockers_quantified`: `closed_for_M355_and_M1267_with_quality_limits`. M-355 now has a measured long continuation window; M-1267 now has a measured bare terminal margin Limit: measurements are tail-hidden manual recuts, not fully independent blind epigraphy.
- `tail_windows_vs_bare_margins_v2`: `terminal_space_adversary_strengthened`. tailed windows span 120-525px / share 0.177-0.433; bare margins span 28-45px / share 0.040-0.063 Limit: tail windows measure visible terminal content; bare margins measure same-line terminal edge margin.
- `bare_tail_sized_empty_slot`: `still_not_observed`. largest measured bare margin is 45px, below the smallest measured tailed window 120px Limit: does not prove no physical space elsewhere on the object; it blocks same-line grammar promotion from current source windows.
- `long_continuation_adversary`: `upgraded_from_visual_only_to_quantified_adversary`. M-355 window 525px / share 0.395 Limit: single long-continuation row; use as adversary, not positive grammar.
- `grammar_promotion`: `blocked`. same-line tail attachment survives, but terminal capacity still separates tailed and bare source windows Limit: promotion requires a bare closure with tail-sized same-line terminal opportunity or exact/near-exact formula alternation under comparable layout.

## Interpretation

Source-visible same-line tail attachment remains real positional evidence. But the current image layer still cannot promote a post-`861` grammar slot, because closure has not yet been observed with tail-sized same-line terminal opportunity.

The next positive gate is now very concrete: find or recut a bare closure after `002-861` with at least `120px` of same-line terminal opportunity, under matched formula/register conditions, that still chooses closure.

Accepted values, phonetics, language identity, translations, exact source-token boundaries, and sign meanings remain `0`.
