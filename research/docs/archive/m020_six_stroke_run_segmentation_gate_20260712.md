# M-20 six-stroke-run segmentation gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_SIX_STROKE_RUN_REJECTS_DUPLICATION_ATOMICITY_UNRESOLVED`.

## What this is and why it exists

When a catalogue lists the same code twice in a row, there are two innocent explanations and they lead to opposite conclusions. Either the object really carries that sign twice, or somebody's transcription repeated an entry by accident. One adds a unit to the count; the other subtracts a spurious one.

M-20 is such a case, and the plate answers half of it cleanly. It rules out the transcription slip. What it does not do is tell us whether the marks form one sign or two, so this note records a partial result rather than pretending to a whole one.

## Question

Lipi, the numeric catalogue, stores seven tokens for `M-20`, with `036` sitting between `861` and `460`. Mayig, the `P`-code catalogue, stores eight graphemes and puts `P147 P147` in that slot. Mayig defines each `P147` as three adjacent full-height vertical strokes. The live question was whether the repeat means two source units that Lipi collapsed into one token, or a Mayig grapheme duplicated by accident.

## Direct evidence

- Lipi row `2548.1`: `+390-005-002-861-036-460-513+`, text length 7, signs 7.
- Mayig `M-20A`: `P086 P125 P122 P385 P147 P147 P215 P275`, grapheme count 8.
- CISI 1 PDF page 49 / printed page 13 shows both `M-20 A` and `M-20 a`.
- Between the diamond form and the three-triangle form, both published views show six full-height vertical strokes. Count them: six, not three. So all six strokes are real, and the second `P147` is not a duplicate entry for a source that only has one three-stroke group.
- Those six strokes form one continuous, evenly spaced run. Nothing encloses them and no wider gap sits in the middle, so the object does not mark a boundary after the third stroke.

## Object-level decision

- Record the graphic fact as one `SIX_VERTICAL_STROKE_RUN` region on `M-20`.
- Treat Lipi's single `036` and Mayig's `P147 P147` as two competing ways of cutting up that same visible region.
- Do not promote either Lipi's seven or Mayig's eight to a source-established structural-unit count. The plate proves six stroke elements. It does not decide between one sign unit and two.
- Do not accept a general `036 = P147 P147` rule. This gate covers one object and does not settle the sign-list conventions behind either catalogue.
- Do not rewrite either raw corpus.

## Research consequence

On M-20 the source-visible continuation after `861` is the `SIX_VERTICAL_STROKE_RUN`, then the forms Lipi calls `460` and `513`. An analysis may use Lipi's `861-036-460-513` if it labels that as catalogue-token level, or Mayig's expanded version if it labels that as Mayig-grapheme level. What it must not do is let either tokenization pass as source-grounded in a count-sensitive or sign-adjacency analysis, because the source supports neither.

This closes the duplication branch and leaves atomicity, meaning where one sign ends and the next begins, unresolved. So it does not justify moving the structural count from seven to eight. It establishes no sign value, meaning, phonetic reading, language identification, translation, or decipherment claim.

## Preserved evidence

Each file is listed with its SHA-256 hash, so a later reader can confirm the exact bytes behind this decision.

- `research/data/sign_crosswalk/source_panels/m020_six_stroke_run_segmentation/M-20_A_a_CISI1_pdf49_print13.png`, SHA-256 `47DF5B89C5E4FE01337DAAE7B79ABA3298000DE0DF13623CB0C1C8FE4B4F8994`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m020.json`: `B163F7F5C510314FD5FCC22A441E5FEDE45B4E6F1D8FD1A51408B1D8177F25AA`.
- Mayig `P147.json`: `E80F45A3DCDD5E99B90E32AF50BD8E46BD689F7B20ED633D64037FB01AC3AE03`.
