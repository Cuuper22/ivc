# Lipi 032 / Mayig P145 source-conflict gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_RECIPROCAL_INVERSION_BLOCKS_EXACT_MAPPING`.

Scope: `lipi_numeric:032 <-> mayig_p:P145` only.

## What this is and why it exists

Lipi and Mayig are two catalogues of the same inscriptions using different sign labels: Lipi numbers like `032`, Mayig Parpola-style codes like `P145`. A crosswalk is the table that says which label matches which. A gate is the written decision that accepts or refuses one such match after checking the source images.

This gate is the companion to the `002 / P122` gate, and the two share a culprit object. Here the question is whether `032` and `P145` are exactly the same grapheme. The gate does not decide which catalogue transcribes better, whether a record contains an error, whether either form is an allograph, meaning a variant shape counted as the same sign, or any sign meaning, reading, phonetic value, language, or translation.

## Alignment pressure

Alignment pressure is the case for the mapping: how often the two labels fall on the same position of the same object.

The pinned positional-alignment table contains `21` aligned positions involving Lipi `032`. Mayig `P145` occupies `20`, a top share of `0.952381`. The one leftover position is not a gap in the data. It is visible in the source:

| Object | CISI page | Lipi row and sequence | Mayig side and sequence | Divergent position |
| --- | --- | --- | --- | ---: |
| M-143 A | PDF 81 / printed 45 | `2670.1`: `740 205 032 002 252 840` | `M-143A`: `P324 P082 P122 P145 P170 P349` | 3: `032 / P122` |

This is worse than a single odd label. The two signs are swapped. At the very next position on the same artifact, Lipi has `002` where Mayig has `P145`. Everywhere else in the corpus that pair runs the other way: `032/P145` followed by `002/P122`. On M-143 the two Mayig codes appear in the opposite order from the two Lipi numbers, so the exception cannot be blamed on one sloppy entry.

## Source-visible review

The local complete CISI 1 PDF has SHA-256 `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`. Two labeled panels, meaning crops rendered from that PDF and kept as files, were reviewed by eye. One shows the rule, the other shows the exception:

- `research/data/sign_crosswalk/source_panels/740_P324/M-21_A_CISI1_pdf49_print13.png` supplies a source-visible dominant-policy witness. Its sixth and seventh aligned positions are Lipi `032 002` and Mayig `P145 P122`.
- `research/data/sign_crosswalk/source_panels/002_P122_conflicts/M-143_A_CISI1_pdf81_print45.png` supplies the source-visible reciprocal inversion. Its third and fourth aligned positions are Lipi `032 002` and Mayig `P122 P145`.
- `research/data/sign_crosswalk/source_panels/032_P145_conflict/manifest.csv` binds both panels, sequences, positions, hashes, and decisions.

Both panels show the complete inscription and the printed object label. That establishes that the supporting relation and the exception are both genuine same-artifact records. It does not license quietly preferring one catalogue's labels over the other's.

## Pinned Mayig evidence

Pinned means the evidence is read from one fixed commit of the Mayig repository, so the record cannot change under the decision later.

Mayig commit: `ad2f1e218a34b8c33c57de0d6cb8d99272765bbb`.

- `features/P145.json` describes two adjacent full-height simple vertical strokes and mediates the form to Wells `W032`.
- `features/P122.json` describes two adjacent half-height simple vertical strokes and mediates the form to Wells `W002`.
- The pinned M-21 record preserves the dominant sequence segment `P145 P122`.
- The pinned M-143 record preserves the inverted sequence segment `P122 P145`.

The two forms differ only in stroke height, full-height versus half-height, and Mayig records that difference deliberately. It keeps them apart; it does not lump them into one bucket.

That closes off the obvious escape route. One could try to dissolve the M-143 exception by declaring a merge, an edge where several signs collapse into one, of the form `{032,002} <-> {P145,P122}`. Do not. A merge that treats all four labels as interchangeable throws away the height distinction Mayig encodes and hides the order disagreement instead of explaining it. The separate `002/P122` gate adds a further reason: its M-140 and M-154 exceptions show the trouble is not a tidy two-sign swap that a merge could absorb.

## Decision

A 20-out-of-21 majority makes `032/P145` a useful candidate relation. Exact means no exceptions, so the one source-visible exception has to be explained rather than outvoted. Therefore:

- `mapping_state=conflict`;
- `accepted_for_analysis=false`;
- the edge may be used only to study how results shift when catalogue policy changes, or to report it openly as a candidate;
- it must not enter a conservative exact-merge vocabulary, which is reserved for edges with no exceptions;
- no two-sign merge is accepted.

Two things could revisit this. Authoritative sign-list or transcription documentation from the source side, or a reproducible visual-feature rule declared in advance that resolves M-143 while leaving both corpora intact. Editing either corpus to make the exception disappear is not such a rule.

## Claim boundary

This is a completed negative crosswalk decision: it removes a candidate rather than adding a result. It increments no accepted decipherment count and supplies no sign meaning, phonetic value, language identification, external anchor, or translation.
