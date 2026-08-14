# 032-002-861 Source-First Terminal-Space Campaign

Date: 2026-05-29

## Question

This note records a measurement campaign on the physical space at the end of inscription rows. Numbers like `861` are sign IDs; a "tail" is material that appears after `861` at the end of a row; "terminal space" is the room left on the object where a tail could physically fit. "Source-first" means we work from the published photographs, not from transcriptions.

The question: does post-`861` material behave like a real secondary inscriptional zone once source segmentation and terminal capacity are considered, or is tail/no-tail mainly layout opportunity — tails appearing simply because there was room?

This is a source-first class campaign. It does not assign values to `603`, `533-717`, `255-416`, or any other tail.

## Inputs

- Canonical universe: `data/open_prototype/reports/campaign_032_002_861_source_normalized_tail_predictor_all_rows.csv`
- Canonical rows: `144`
- Source-ready rows: `14`
- Quantified source rows in this packet: `12`
- Visual-only unquantified rows: `M-355`, `M-1267`
- Script: `tmp/run_032_002_861_source_first_terminal_space.py`
- Reports:
  - `data/open_prototype/reports/campaign_032_002_861_source_first_terminal_space_metrics.csv`
  - `data/open_prototype/reports/campaign_032_002_861_source_first_terminal_space_class_summary.csv`
  - `data/open_prototype/reports/campaign_032_002_861_source_first_terminal_space_decisions.csv`
  - `data/open_prototype/reports/campaign_032_002_861_source_first_terminal_space_summary.json`
- Contact sheet: `tmp/032_002_861_source_first_terminal_space/campaign_032_002_861_source_first_terminal_space_contact_sheet.png`

Mechanic validation: `PASS`.

## Source-First Result

The typed post-`861` zone remains visible at source level, but grammar promotion is blocked. In plain terms: the photographs still show the tail zone, but we cannot yet claim it is grammar.

The six quantified tailed rows all have same-line attachment verdicts — the tail sits on the same inscribed line as the rest of the row. Five of six touch the marked terminal edge. That keeps source-visible positional behavior alive.

But terminal-space now generalizes beyond the narrow `220-032` packet:

| Packet side | Width range | Share range |
|---|---:|---:|
| tailed terminal-content windows | `120-265px` | `0.177-0.433` |
| bare post-terminal margins | `28-45px` | `0.040-0.063` |

The largest measured bare post-terminal margin is `45px`, still below the smallest measured tailed terminal-content window, `120px`. In other words: no bare row has been shown to have tail-sized empty space that went unused.

That is not proof that layout explains the system. It is proof that grammar is not promotable from the current image layer. The current evidence is compatible with "tails appear when the physical terminal zone can carry them."

## Class-Level Evidence

| Class | Source-ready rows | Quantified | Width or margin range | Verdict |
|---|---:|---:|---|---|
| closure | 7 | 6 | margin `28-45px` / share `0.040-0.063` | terminal edge visible, no tail-sized post-margin observed |
| simple single | 3 | 3 | tail-window `120-225px` / share `0.177-0.286` | same-line source-visible, but terminal-space adversary active |
| fixed pair | 3 | 3 | tail-window `195-265px` / share `0.331-0.433` | same-line source-visible, but large terminal window and narrow-register pressure |
| long continuation | 1 | 0 | unquantified | source-visible adversary, not metric-promotable |

## What Survives

- Source-visible same-line attachment survives for the tailed rows.
- The typed secondary-zone model remains a live structural question: closure, simple single, fixed pair, and long continuation are visible categories.
- `603` remains the best simple-tail probe, not a value.
- `533-717` remains a fixed-unit comparator, not a function.
- Long continuation remains an adversary against suffix over-reading — a standing counterexample that keeps us from over-interpreting short tails.

## What Is Blocked

- Grammar-slot promotion is blocked.
- `220-032` remains positional/source-visible but not grammatical.
- `533-717` cannot be promoted beyond narrow fixed-unit comparator.
- `603` cannot be promoted beyond post-`861` simple-tail behavior.
- `M-355` and `M-1267` cannot carry terminal-space comparisons yet because they are source-visible but unquantified in this packet.

## Decisions

1. `terminal_space_adversary_generalizes_across_current_quantified_source_rows`
   - Evidence: tailed windows are `120-265px`; bare margins are `28-45px`.
   - Meaning: source-visible tail/no-tail is confounded with terminal capacity.

2. `same_line_tail_attachment_survives_as_positional_evidence`
   - Evidence: all six quantified tailed rows have same-line attachment verdicts; five touch the marked terminal edge.
   - Meaning: post-`861` material is not dismissed as random catalog residue.

3. `bare_tail_sized_empty_slot_not_observed`
   - Evidence: no quantified bare control has a measured post-terminal margin large enough for the smallest tailed window.
   - Meaning: grammar needs stronger evidence from matched terminal opportunity.

4. `visual_only_rows_not_comparable`
   - Evidence: `M-355` and `M-1267` remain source-visible but unquantified.
   - Meaning: same-register `533-717` controls still need a real source-first recut.

5. `grammar_promotion_blocked`
   - Evidence: source segmentation keeps positional behavior alive, but terminal-space and formula-template attacks both remain active.

## Next Gate

A gate is a checkpoint the work must clear before any stronger claim. The next campaign must be blind recut — re-measuring with the tail labels hidden from the scorer — not another table:

- Quantify `M-355` and `M-1267` terminal windows.
- Recut all `220-032` rows with tail labels hidden.
- Add pending source rows only if they can be measured with the same rule.
- Require at least one bare row with tail-sized available terminal space still choosing closure before grammar promotion.
- Require exact or near-exact source-visible formula alternation before treating last-k preframe behavior as grammatical.

Accepted values, phonetics, language identity, translations, exact source-token boundaries, and sign meanings remain `0`.
