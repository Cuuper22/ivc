# M-4 and Lipi 617 overlap-policy closure

Date: 2026-07-12 America/Los_Angeles

Decision: `COMPLETE_OVERLAP_617_EXPANDS_TO_TWO_SOURCE_GRID_POSITIONS_5_OF_5`.

## Question

M-4 is the fifth and final Lipi-Mayig overlap row in which one Lipi `617` corresponds to consecutive Mayig `P268 P268`. The source check decides whether the expansion holds across the complete overlap cluster or meets its first exception.

## M-4 direct evidence

- Lipi row `2533.1`: `+298-465-033-705-231-002-564-617-033+`, text length 9, signs 9, direction `R/L`.
- Mayig `M-4A`: `P205 P186 P147 P316 P056 P122 P237 P268 P268 P147`, grapheme count 10.
- CISI 1 PDF page 39 / printed page 3 publishes inscription-bearing `M-4 A` and `M-4 a`, plus non-inscription boss/profile views `B`, `C`, and `D`.
- Both inscription views show ten bounded units. The two grids have distinct enclosing borders.
- No second count discrepancy competes with this explanation: Lipi's two `033` positions correspond to Mayig's two `P147` positions, and after expanding `617` the remaining positions align one-for-one in order.

M-4 therefore has ten structural units, not nine.

## Complete-overlap result

The five exact `617` overlap rows are `M-161`, `M-25`, `M-45`, `M-81`, and `M-4`.

- Every Lipi row contains one `617` where Mayig contains consecutive `P268 P268`.
- Every Mayig row has exactly one more grapheme than Lipi.
- Every source panel shows two separately bounded grids and the Mayig structural count.
- The pattern holds with the pair initially and internally, including cases with a following sign.
- Checked counterexamples: `0/5`.

## Accepted normalization policy

- For these five overlap objects, expand Lipi `617` to two source positions: `<GRID>, <GRID>`.
- Use source counts `4` for M-161, `5` for M-25, `7` for M-45, `7` for M-81, and `10` for M-4.
- Only the second grid is adjacent to the following source unit where one exists. Catalogue edges that treat `617` as one sign must remain explicitly Lipi-token-level.
- This supersedes the earlier object-local `compound_or_omission` uncertainty for structural normalization: either internal catalogue mechanism produces the same empirically required two-position expansion.
- Keep the raw Lipi and Mayig records unchanged.

The accepted scope is the complete five-row overlap cluster. It is not an automatic rule for Lipi-only `617` rows, a claim that every grid variant is identical, or a semantic/phonetic crosswalk. Transfer beyond the overlap set still requires source checks.

## Queue consequence

All eight `unflagged_mayig_extra` rows are now source-adjudicated: `M-111`, `M-161`, `M-162`, `M-20`, `M-25`, `M-4`, `M-45`, and `M-81`. Seven have a source-established larger structural count; M-20 instead closes accidental duplication while retaining one-versus-two sign atomicity as unresolved. The next live mismatch class begins with `M-10`, where Lipi rather than Mayig has the extra token.

No sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is accepted.

## Preserved evidence

- `research/data/sign_crosswalk/source_panels/m004_double_grid_pair/M-4_A_a_CISI1_pdf39_print3.png`, SHA-256 `AA8CE1500F310D96133BCD811F1BA9E7E948AEB2D379849E9E9AC312360CB19E`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m004.json`: `493D870B78853AED03030EDB2474EA178F2912EB27E74E4AC9D9AB9468CC1E21`.
- Mayig `P268.json`: `34248A590A6E9508C42747CDA83871240599456F6BFE78D8E98EEB5B11E3F139`.
