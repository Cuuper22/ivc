# Lipi 002 / Mayig P122 source-conflict gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_COUNTEREXAMPLES_BLOCK_EXACT_MAPPING`.

Scope: `lipi_numeric:002 <-> mayig_p:P122` only.

This gate decides whether the two identifiers can be used as an exact grapheme-namespace crosswalk. It does not decide which catalogue has the preferable segmentation, whether either sign is an allograph of another sign, or any sign meaning, reading, phonetic value, language, or translation.

## Alignment pressure

The pinned positional-alignment table contains `60` aligned positions involving Lipi `002`. Mayig `P122` occupies `57`, for a top share of `0.950000`. The three remaining positions are not missing data:

| Object | CISI page | Lipi row and sequence | Mayig side and sequence | Divergent position |
| --- | --- | --- | --- | ---: |
| M-140 A | PDF 81 / printed 45 | `2667.1`: `740 336 002 220 065 440 455` | `M-140A`: `P324 P309 P145 P050 P201 P283 P221` | 3: `002 / P145` |
| M-143 A | PDF 81 / printed 45 | `2670.1`: `740 205 032 002 252 840` | `M-143A`: `P324 P082 P122 P145 P170 P349` | 4: `002 / P145` |
| M-154 A | PDF 83 / printed 47 | `2681.1`: `520 220 621 415 002 257 898` | `M-154A`: `P217 P050 P092 P122 P300 P182 P265` | 5: `002 / P300` |

The correct counterexample total is therefore `P145:2;P300:1`, or `3`. The earlier `counterexample_count=2` field counted alternate Mayig sign types rather than counterexample positions and is corrected by this gate.

## Source-visible review

The local complete CISI 1 PDF has SHA-256 `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`. Three labeled object panels were rendered from it and visually reviewed:

- `research/data/sign_crosswalk/source_panels/002_P122_conflicts/M-140_A_CISI1_pdf81_print45.png`
- `research/data/sign_crosswalk/source_panels/002_P122_conflicts/M-143_A_CISI1_pdf81_print45.png`
- `research/data/sign_crosswalk/source_panels/002_P122_conflicts/M-154_A_CISI1_pdf83_print47.png`
- `research/data/sign_crosswalk/source_panels/002_P122_conflicts/manifest.csv`

The panels preserve the complete inscription and printed object label. They establish that these are real, source-visible same-artifact rows rather than unmatched identifiers or blank-image artifacts. They do not authorize an unrecorded choice between the Lipi and Mayig segmentations.

## Pinned Mayig evidence

Mayig commit: `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`.

- `features/P122.json` describes two adjacent half-height simple vertical strokes.
- `features/P145.json` describes two adjacent full-height simple vertical strokes.
- `features/P300.json` describes a more complex form with verticals, diagonals, tail, and triangle features.
- The pinned M-140, M-143, and M-154 records preserve the three divergent sequences above.

These records show two different kinds of conflict. M-140 and M-143 assign P145 where Lipi assigns 002; M-143 also places P122 at the preceding local-032 position. M-154 has a broader local/Mayig segmentation disagreement around `415 002` versus `P122 P300`. An exact `002=P122` rule would silently overwrite those source-policy differences.

## Decision

The majority alignment makes `002/P122` a useful candidate relation, but exact mapping requires the counterexamples to be reconciled, not outvoted. Because all three exceptions are source-visible and preserved in pinned records:

- `mapping_state=conflict`;
- `accepted_for_analysis=false`;
- the edge may be used to study catalogue-policy sensitivity only;
- it must not be used in a conservative exact-merge vocabulary.

The decision can be revisited only with authoritative source-side sign-list documentation or a reproducible, predeclared segmentation rule that explains M-140, M-143, and M-154 without silently editing either corpus.

## Claim boundary

This is a negative crosswalk decision. It increments no accepted decipherment count and supplies no sign meaning, phonetic value, language identification, external anchor, or translation.
