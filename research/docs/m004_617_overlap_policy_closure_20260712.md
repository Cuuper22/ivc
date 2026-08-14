# M-4 and Lipi 617 overlap-policy closure

Date: 2026-07-12 America/Los_Angeles

Decision: `COMPLETE_OVERLAP_617_EXPANDS_TO_TWO_SOURCE_GRID_POSITIONS_5_OF_5`.

## What this is and why it exists

Five objects share the same odd pattern. At one position the Lipi catalogue, which writes signs as numbers, records a single token `617`. At the same position the Mayig catalogue, which writes signs as `P` codes, records the same grid sign twice in a row: `P268 P268`. So Mayig always counts one unit more than Lipi on these objects.

Somebody has to be right about how many things are on the seal, because sign counts feed every later statistic. This note checks M-4, the fifth and last of the five, against the published plate. With it the whole group is settled.

## Question

M-4 is the fifth and final Lipi-Mayig overlap row in which one Lipi `617` corresponds to consecutive Mayig `P268 P268`. The source check decides whether the expansion to two positions holds across the complete cluster, or whether M-4 is its first exception.

## M-4 direct evidence

- Lipi row `2533.1`: `+298-465-033-705-231-002-564-617-033+`, text length 9, signs 9, direction `R/L`.
- Mayig `M-4A`: `P205 P186 P147 P316 P056 P122 P237 P268 P268 P147`, grapheme count 10.
- CISI 1 PDF page 39 / printed page 3 publishes inscription-bearing `M-4 A` and `M-4 a`, plus non-inscription boss/profile views `B`, `C`, and `D`.
- Both inscription views show ten bounded units. The two grids have their own separate enclosing borders, so they are two units on the object, not one unit drawn twice.
- Nothing else on the object could explain the count gap instead. Lipi's two `033` positions line up with Mayig's two `P147` positions, and once `617` is expanded every remaining position matches one-for-one in order.

M-4 therefore has ten structural units, not nine.

## Complete-overlap result

The five exact `617` overlap rows are `M-161`, `M-25`, `M-45`, `M-81`, and `M-4`. With M-4 done, all five have been checked against the source, and they agree:

- Every Lipi row contains one `617` where Mayig contains consecutive `P268 P268`.
- Every Mayig row has exactly one more grapheme than Lipi.
- Every source panel shows two separately bounded grids and the Mayig structural count.
- The pattern holds with the pair initially and internally, including cases with a following sign.
- Checked counterexamples: `0/5`.

## Accepted normalization policy

- On these five objects, expand Lipi `617` into two source positions: `<GRID>, <GRID>`.
- Use source counts `4` for M-161, `5` for M-25, `7` for M-45, `7` for M-81, and `10` for M-4.
- Where a unit follows the pair, only the second grid touches it. An analysis that treats `617` as one sign is describing a Lipi token, not a source adjacency, and must say so.
- This settles the structural count without settling the earlier `compound_or_omission` question. Lipi might be writing one compound token for two grids, or suppressing a repeat. Either way the object needs two positions, so the count no longer waits on that answer.
- Leave the raw Lipi and Mayig records unchanged. The expansion happens in analysis, not in the corpus.

The accepted scope is exactly these five overlap rows. It is not a standing rule for Lipi rows that Mayig does not cover, not a claim that every grid variant is the same sign, and not a semantic or phonetic crosswalk. Any object outside the overlap set needs its own source check.

## Queue consequence

All eight `unflagged_mayig_extra` rows now have source-level adjudications: `M-111`, `M-161`, `M-162`, `M-20`, `M-25`, `M-4`, `M-45`, and `M-81`. Seven ended with a larger structural count established from the source. M-20 is the exception: it rules out accidental duplication but leaves the one-versus-two sign question unresolved. The next live mismatch class starts at `M-10`, where the extra token belongs to Lipi rather than Mayig.

No sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is accepted.

## Preserved evidence

Each file is listed with its SHA-256 hash, so a later reader can confirm the exact bytes behind this decision.

- `research/data/sign_crosswalk/source_panels/m004_double_grid_pair/M-4_A_a_CISI1_pdf39_print3.png`, SHA-256 `AA8CE1500F310D96133BCD811F1BA9E7E948AEB2D379849E9E9AC312360CB19E`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m004.json`: `493D870B78853AED03030EDB2474EA178F2912EB27E74E4AC9D9AB9468CC1E21`.
- Mayig `P268.json`: `34248A590A6E9508C42747CDA83871240599456F6BFE78D8E98EEB5B11E3F139`.
