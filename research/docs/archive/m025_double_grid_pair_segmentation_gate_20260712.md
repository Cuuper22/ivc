# M-25 double-grid-pair segmentation gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_FIVE_UNITS_REJECTS_LIPI_FOUR_TOKEN_COUNT_REPEATS_617_PAIR_CONFLICT`.

## What this is and why it exists

A recurring puzzle in this corpus: Lipi, the numeric catalogue, writes one token `617`, while Mayig, the `P`-code catalogue, writes the grid sign twice, `P268 P268`, at the same spot. Five objects show it. Whichever catalogue is right about the unit count is right about every statistic built on those objects.

M-25 is the second of the five to be checked against the published plate. This note reports what the images show and, just as importantly, which part of the puzzle they leave open.

## Question

Lipi stores four tokens for `M-25`, starting with `617`. Mayig stores five graphemes, meaning five sign entries, starting with `P268 P268`, where `P268` is a grid. Three explanations were possible: the repeated grids are two separately bounded units, they are one compound that Mayig split, or the second one is an accidental duplicate entry.

## Direct evidence

- Lipi row `2553.1`: `+617-243-706-595+`, text length 4, signs 4, direction `R/L`.
- Mayig `M-25A`: `P268 P268 P050 P316 P276`, grapheme count 5.
- CISI 1 PDF page 51 / printed page 15 publishes `M-25 A`, `M-25 A bis`, and `M-25 a`.
- Each published view shows five bounded inscription units. In every usable view the grid pair has two separate outer boundaries, so the two grids are drawn as two units on the object.

That rules out the accidental duplicate. The repeated Mayig grapheme is backed by the source, and M-25 has five structural units, not four.

## Object-level decision

- Use source-unit count `5` for `M-25`.
- Keep the two grid positions separate in sign-unit analyses.
- Reject Lipi `617` as a literal single structural unit on this object.
- Classify the discrepancy as `recurrent_617_pair_macro_or_suppressed_repeat_unresolved`. The object shows two grids, but it cannot tell us why Lipi wrote one token: `617` may be a compound token covering both grids, or Lipi's convention may suppress a repeated sign. The plate cannot see a catalogue's internal rules.
- Do not accept a general `617 = P268 P268` rule, and do not rewrite either raw corpus.

## Research consequence

M-25 reproduces the M-161 result independently: one Lipi `617` sits where both Mayig and the source have two grids. The mismatch queue holds the same one-Lipi-token versus two-Mayig-grid pattern in five objects, `M-25`, `M-161`, `M-4`, `M-45`, and `M-81`, and two of them are now source-confirmed.

One consequence is easy to get wrong. Since only the second grid actually touches the unit that follows it, Lipi-level `617-243` is not a sign-level adjacency and must not be counted as one. The remaining three overlap objects are the quickest way to find out whether this expansion is a stable catalogue policy or a coincidence across a few objects.

This gate does not establish a sign value, meaning, phonetic reading, language identification, translation, or decipherment claim.

## Preserved evidence

Each file is listed with its SHA-256 hash, so a later reader can confirm the exact bytes behind this decision.

- `research/data/sign_crosswalk/source_panels/m025_double_grid_pair/M-25_A_Abis_a_CISI1_pdf51_print15.png`, SHA-256 `D5FFFD03FF979510BDF8DBEA6C9E143FBB1D6DEAA2C13A16C10DC507C7ED3035`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m025.json`: `5DCF9DE82CD08FB079A47A1F5617E405151D2A4F8ADF66F14AAF0B24D6B76FDE`.
- Mayig `P268.json`: `34248A590A6E9508C42747CDA83871240599456F6BFE78D8E98EEB5B11E3F139`.
