# Lipi 032 / Mayig P145 source-conflict gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_RECIPROCAL_INVERSION_BLOCKS_EXACT_MAPPING`.

Scope: `lipi_numeric:032 <-> mayig_p:P145` only.

This gate decides whether the two identifiers can be used as an exact grapheme-namespace crosswalk. It does not decide which catalogue has the preferable transcription, whether a catalogue record contains an error, whether either form is an allograph, or any sign meaning, reading, phonetic value, language, or translation.

## Alignment pressure

The pinned positional-alignment table contains `21` aligned positions involving Lipi `032`. Mayig `P145` occupies `20`, for a top share of `0.952381`. The remaining position is source-visible and is not missing data:

| Object | CISI page | Lipi row and sequence | Mayig side and sequence | Divergent position |
| --- | --- | --- | --- | ---: |
| M-143 A | PDF 81 / printed 45 | `2670.1`: `740 205 032 002 252 840` | `M-143A`: `P324 P082 P122 P145 P170 P349` | 3: `032 / P122` |

This is a reciprocal local inversion rather than an isolated unknown label. At the immediately following fourth position, the same artifact has Lipi `002` where Mayig has `P145`. The dominant corpus relations would instead predict `032/P145` followed by `002/P122`.

## Source-visible review

The local complete CISI 1 PDF has SHA-256 `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`. Two labeled panels rendered from it were visually reviewed:

- `research/data/sign_crosswalk/source_panels/740_P324/M-21_A_CISI1_pdf49_print13.png` supplies a source-visible dominant-policy witness. Its sixth and seventh aligned positions are Lipi `032 002` and Mayig `P145 P122`.
- `research/data/sign_crosswalk/source_panels/002_P122_conflicts/M-143_A_CISI1_pdf81_print45.png` supplies the source-visible reciprocal inversion. Its third and fourth aligned positions are Lipi `032 002` and Mayig `P122 P145`.
- `research/data/sign_crosswalk/source_panels/032_P145_conflict/manifest.csv` binds both panels, sequences, positions, hashes, and decisions.

Both panels preserve the complete inscription and printed object label. They establish that the supporting relation and the exception are real same-artifact records. The images do not authorize silently choosing one catalogue's token labels over the other.

## Pinned Mayig evidence

Mayig commit: `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`.

- `features/P145.json` describes two adjacent full-height simple vertical strokes and mediates the form to Wells `W032`.
- `features/P122.json` describes two adjacent half-height simple vertical strokes and mediates the form to Wells `W002`.
- The pinned M-21 record preserves the dominant sequence segment `P145 P122`.
- The pinned M-143 record preserves the inverted sequence segment `P122 P145`.

The Mayig feature records distinguish the forms rather than defining one feature-bearing merge bucket. Consequently, the M-143 exception cannot be resolved by accepting an undifferentiated `{032,002} <-> {P145,P122}` merge: that would erase the encoded height distinction and the order disagreement. The M-140 and M-154 exceptions recorded by the separate `002/P122` gate also show that the uncertainty is not confined to a clean reciprocal two-sign swap.

## Decision

The 20/21 majority makes `032/P145` a useful candidate relation, but exact mapping requires the source-visible exception to be reconciled rather than outvoted. Therefore:

- `mapping_state=conflict`;
- `accepted_for_analysis=false`;
- the edge may be used only for catalogue-policy sensitivity or explicit candidate reporting;
- it must not enter a conservative exact-merge vocabulary;
- no two-sign merge is accepted.

This decision can be revisited only with authoritative source-side sign-list or transcription documentation, or a reproducible predeclared visual-feature rule that resolves M-143 while preserving both corpora rather than silently editing either one.

## Claim boundary

This is a completed negative crosswalk decision. It increments no accepted decipherment count and supplies no sign meaning, phonetic value, language identification, external anchor, or translation.
