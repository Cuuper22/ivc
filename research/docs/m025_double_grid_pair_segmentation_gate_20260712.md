# M-25 double-grid-pair segmentation gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_FIVE_UNITS_REJECTS_LIPI_FOUR_TOKEN_COUNT_REPEATS_617_PAIR_CONFLICT`.

## Question

Lipi stores four tokens for `M-25`, beginning with `617`. Mayig stores five graphemes, beginning with consecutive `P268 P268`, where `P268` is a grid. The source question was whether the repeated grids were two bounded units, one compound split by Mayig, or a duplicated grapheme.

## Direct evidence

- Lipi row `2553.1`: `+617-243-706-595+`, text length 4, signs 4, direction `R/L`.
- Mayig `M-25A`: `P268 P268 P050 P316 P276`, grapheme count 5.
- CISI 1 PDF page 51 / printed page 15 publishes `M-25 A`, `M-25 A bis`, and `M-25 a`.
- Each published view shows five bounded inscription units. The grid pair has two separate outer boundaries in every usable view.

The repeated Mayig grapheme is therefore source-supported. M-25 has five structural units, not four.

## Object-level decision

- Use source-unit count `5` for `M-25`.
- Preserve the two grid positions separately in sign-unit analyses.
- Reject Lipi `617` as a literal single structural unit on this object.
- Classify the discrepancy as `recurrent_617_pair_macro_or_suppressed_repeat_unresolved`: the object does not distinguish a Lipi compound token spanning both grids from a policy that suppresses one repeated grid.
- Do not accept a global `617 = P268 P268` rule and do not rewrite either raw corpus.

## Research consequence

M-25 independently repeats the M-161 result: a single Lipi `617` occupies the position where Mayig and the source preserve two grids. The mismatch queue contains the same one-Lipi-token versus two-Mayig-grid pattern in five objects: `M-25`, `M-161`, `M-4`, `M-45`, and `M-81`. Two are now source-confirmed.

For M-25, only the second grid is directly adjacent to the following source unit. Lipi-level `617-243` must not be counted as a literal sign-level edge. The three remaining overlap objects are the shortest route to deciding whether this is a stable catalogue expansion policy rather than an object-local discrepancy.

This gate does not establish a sign value, meaning, phonetic reading, language identification, translation, or decipherment claim.

## Preserved evidence

- `research/data/sign_crosswalk/source_panels/m025_double_grid_pair/M-25_A_Abis_a_CISI1_pdf51_print15.png`, SHA-256 `D5FFFD03FF979510BDF8DBEA6C9E143FBB1D6DEAA2C13A16C10DC507C7ED3035`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m025.json`: `5DCF9DE82CD08FB079A47A1F5617E405151D2A4F8ADF66F14AAF0B24D6B76FDE`.
- Mayig `P268.json`: `34248A590A6E9508C42747CDA83871240599456F6BFE78D8E98EEB5B11E3F139`.
