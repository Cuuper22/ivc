# Lipi 002 / Mayig P122 source-conflict gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_COUNTEREXAMPLES_BLOCK_EXACT_MAPPING`.

Scope: `lipi_numeric:002 <-> mayig_p:P122` only.

## What this is and why it exists

Two catalogues describe the same inscriptions with different sign numbers. Lipi uses numbers like `002`; Mayig uses Parpola-style codes like `P122`. To combine them you need a crosswalk, a table saying which sign in one catalogue is which sign in the other. A gate is the written decision that either accepts one such edge or refuses it, based on the source images.

This gate asks one narrow question: can `002` and `P122` be treated as exactly the same grapheme, so that either label can stand for the other? It does not decide which catalogue segments the inscriptions better. It does not decide whether either sign is an allograph of another, meaning a variant shape counted as the same sign. And it settles no sign meaning, reading, phonetic value, language, or translation.

## Alignment pressure

Alignment pressure is the case for the mapping: how often the two labels actually land on the same position of the same object.

The pinned positional-alignment table contains `60` aligned positions involving Lipi `002`. Mayig `P122` occupies `57` of them, a top share of `0.950000`. That is a strong majority. But the three leftover positions are not gaps or unmatched records. Each one is a place where Mayig positively records a different sign:

| Object | CISI page | Lipi row and sequence | Mayig side and sequence | Divergent position |
| --- | --- | --- | --- | ---: |
| M-140 A | PDF 81 / printed 45 | `2667.1`: `740 336 002 220 065 440 455` | `M-140A`: `P324 P309 P145 P050 P201 P283 P221` | 3: `002 / P145` |
| M-143 A | PDF 81 / printed 45 | `2670.1`: `740 205 032 002 252 840` | `M-143A`: `P324 P082 P122 P145 P170 P349` | 4: `002 / P145` |
| M-154 A | PDF 83 / printed 47 | `2681.1`: `520 220 621 415 002 257 898` | `M-154A`: `P217 P050 P092 P122 P300 P182 P265` | 5: `002 / P300` |

So the correct counterexample total is `P145:2;P300:1`, which is `3`. The earlier record said `counterexample_count=2`. That field had counted how many distinct Mayig sign types appeared, not how many positions conflicted. This gate corrects it.

## Source-visible review

Records can disagree for boring reasons: a mismatched object ID, a blank image, a clerical slip. Looking at the plates rules those out.

The local complete CISI 1 PDF has SHA-256 `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`. Three labeled object panels, meaning crops rendered from that PDF and saved as files, were reviewed by eye:

- `research/data/sign_crosswalk/source_panels/002_P122_conflicts/M-140_A_CISI1_pdf81_print45.png`
- `research/data/sign_crosswalk/source_panels/002_P122_conflicts/M-143_A_CISI1_pdf81_print45.png`
- `research/data/sign_crosswalk/source_panels/002_P122_conflicts/M-154_A_CISI1_pdf83_print47.png`
- `research/data/sign_crosswalk/source_panels/002_P122_conflicts/manifest.csv`

Each panel shows the complete inscription and the printed object label. That confirms these are genuine same-artifact rows, not mismatched identifiers or blank images. What the panels cannot do is pick a winner. They do not license quietly preferring the Lipi segmentation over the Mayig one, or the reverse.

## Pinned Mayig evidence

Pinned means the evidence is read from one fixed commit of the Mayig repository, so the record cannot shift under the decision later.

Mayig commit: `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`.

- `features/P122.json` describes two adjacent half-height simple vertical strokes.
- `features/P145.json` describes two adjacent full-height simple vertical strokes.
- `features/P300.json` describes a more complex form with verticals, diagonals, tail, and triangle features.
- The pinned M-140, M-143, and M-154 records preserve the three divergent sequences above.

Note that P122 and P145 differ only in stroke height. Mayig treats that height difference as worth encoding, which is why these are not simply interchangeable.

The three exceptions are not all the same kind of problem. M-140 and M-143 put P145 where Lipi puts 002. M-143 goes further and puts P122 at the preceding position, where Lipi has `032`, so the two labels are swapped rather than merely disagreeing. M-154 is a wider segmentation disagreement around `415 002` versus `P122 P300`. An exact `002=P122` rule would paper over all three of these catalogue-policy differences without recording that it had done so.

## Decision

A 57-out-of-60 majority makes `002/P122` a useful candidate relation. It does not make it exact. Exactness means no exceptions, so the three counterexamples would have to be explained, not outvoted. All three are visible in the source and preserved in pinned records, so they cannot be set aside. Therefore:

- `mapping_state=conflict`;
- `accepted_for_analysis=false`;
- the edge may be used only to study how results shift when catalogue policy changes;
- it must not enter a conservative exact-merge vocabulary, which is reserved for edges with no exceptions.

Two things could revisit this. Authoritative sign-list documentation from the source side, or a reproducible segmentation rule declared in advance that accounts for M-140, M-143, and M-154 without quietly editing either corpus. Choosing one catalogue's labels after the fact is not such a rule.

## Claim boundary

This is a negative crosswalk decision: it removes a candidate rather than adding a result. It increments no accepted decipherment count and supplies no sign meaning, phonetic value, language identification, external anchor, or translation.
