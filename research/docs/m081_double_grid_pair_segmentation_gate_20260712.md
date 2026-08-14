# M-81 internal double-grid-pair segmentation gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_SEVEN_UNITS_INTERNAL_617_DOUBLE_GRID_POSITION_INDEPENDENT`.

## What this is and why it exists

This is a gate: a written decision that settles one specific question against the source images, so that later analysis does not have to keep guessing. This gate covers one object, `M-81`.

Two catalogues describe the same inscriptions. Lipi is the numeric catalogue that writes signs as numbers like `617`, and each of its entries is called a token. Mayig is the Parpola-style catalogue that writes signs as `P` codes like `P268`, and each of its entries is called a grapheme. On a growing list of objects, one Lipi `617` sits where Mayig records two grid signs in a row. That is a segmentation disagreement — a disagreement about where one sign stops and the next begins — and it has to be settled object by object against the plates.

The open worry was that the pattern might be an artifact of position. On the first three objects checked, the disputed grid pair sat at the very start of the inscription, where a cataloguer might treat an opening pair as one block. M-81 is the first checked object where the pair sits in the middle.

## Question

The first three source-confirmed `617` cases placed the disputed grid pair at the beginning of normalized reading order. M-81 tests whether the same one-to-two discrepancy survives when Lipi `617` occurs internally and is followed by another sign.

## Direct evidence

Each item below is something a pinned catalogue record or a published plate actually shows.

- Lipi row `2608.1`: `+527-555-240-002-617-070+`, text length 6, signs 6, direction `R/L`.
- Mayig `M-81A`: `P301 P230 P062 P122 P268 P268 P217`, grapheme count 7.
- CISI 1 PDF page 70 / printed page 34 publishes `M-81 A`, `M-81 a`, and `M-81 a bis`.
- All three views show seven bounded units. The two grids have separate outer boundaries and another sign follows the pair in reading order.

So the source agrees with Mayig's seven positions. It rejects Lipi's six-token count as a literal structural count.

## Object-level decision

- Use source-unit count `7` for `M-81`.
- Preserve both internal grids as separate positions.
- Expand Lipi `617` to two structural grid positions on this object.
- Only the second grid is adjacent to the terminal unit represented by Lipi `070` / Mayig `P217`; Lipi `617-070` is not a literal sign-level edge.
- Do not rewrite either raw corpus or infer a sign value from the grid forms.

## Research consequence

M-81 is the fourth independent source-confirmed `617` case, and the first checked case with the pair away from the initial edge. That rules out an initial-layout artifact as the explanation for the recurring discrepancy. The source-supported expansion now holds at both initial and internal positions.

Within the Lipi-Mayig overlap set — the objects both catalogues record — `617 -> P268 P268` is therefore a position-independent structural-normalization candidate, with four direct source confirmations and no checked counterexample. M-4 is the fifth and final exact overlap case. Its source check can either promote the expansion across the complete overlap cluster or expose the first exception. None of this yet authorizes automatic expansion of Lipi-only `617` rows, meaning rows Mayig does not cover.

This gate does not establish a sign value, meaning, phonetic reading, language identification, translation, or decipherment claim.

## Preserved evidence

Each file below is listed with its SHA-256 hash, so a later reader can confirm the exact bytes this decision was made from.

- `research/data/sign_crosswalk/source_panels/m081_double_grid_pair/M-81_A_a_abis_CISI1_pdf70_print34.png`, SHA-256 `89F1B2F37EEDB3D31F6624C0E51E1BA888065FCD04B829679D960415B80BDC0F`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m081.json`: `A6A173DCF40856D7DAC31C110D76E39EFDF0CF126C33B1934F50967DB3016B83`.
- Mayig `P268.json`: `34248A590A6E9508C42747CDA83871240599456F6BFE78D8E98EEB5B11E3F139`.
