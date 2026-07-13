# M-81 internal double-grid-pair segmentation gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_SEVEN_UNITS_INTERNAL_617_DOUBLE_GRID_POSITION_INDEPENDENT`.

## Question

The first three source-confirmed `617` cases placed the disputed grid pair at the beginning of normalized reading order. M-81 tests whether the same one-to-two discrepancy survives when Lipi `617` occurs internally and is followed by another sign.

## Direct evidence

- Lipi row `2608.1`: `+527-555-240-002-617-070+`, text length 6, signs 6, direction `R/L`.
- Mayig `M-81A`: `P301 P230 P062 P122 P268 P268 P217`, grapheme count 7.
- CISI 1 PDF page 70 / printed page 34 publishes `M-81 A`, `M-81 a`, and `M-81 a bis`.
- All three views show seven bounded units. The two grids have separate outer boundaries and another sign follows the pair in reading order.

The source agrees with Mayig's seven positions and rejects Lipi's six-token count as a literal structural count.

## Object-level decision

- Use source-unit count `7` for `M-81`.
- Preserve both internal grids as separate positions.
- Expand Lipi `617` to two structural grid positions on this object.
- Only the second grid is adjacent to the terminal unit represented by Lipi `070` / Mayig `P217`; Lipi `617-070` is not a literal sign-level edge.
- Do not rewrite either raw corpus or infer a sign value from the grid forms.

## Research consequence

M-81 is the fourth independent source-confirmed `617` case and the first checked case with the pair away from the initial edge. It rules out an initial-layout artifact as the explanation for the recurring discrepancy. The source-supported expansion now holds at both initial and internal positions.

Within the Lipi-Mayig overlap set, `617 -> P268 P268` is therefore a position-independent structural-normalization candidate with four direct source confirmations and no checked counterexample. M-4 is the fifth and final exact overlap case; its source check can either promote the expansion across the complete overlap cluster or expose the first exception. This does not yet authorize automatic expansion of Lipi-only `617` rows.

This gate does not establish a sign value, meaning, phonetic reading, language identification, translation, or decipherment claim.

## Preserved evidence

- `research/data/sign_crosswalk/source_panels/m081_double_grid_pair/M-81_A_a_abis_CISI1_pdf70_print34.png`, SHA-256 `89F1B2F37EEDB3D31F6624C0E51E1BA888065FCD04B829679D960415B80BDC0F`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m081.json`: `A6A173DCF40856D7DAC31C110D76E39EFDF0CF126C33B1934F50967DB3016B83`.
- Mayig `P268.json`: `34248A590A6E9508C42747CDA83871240599456F6BFE78D8E98EEB5B11E3F139`.
