# M-20 six-stroke-run segmentation gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_SIX_STROKE_RUN_REJECTS_DUPLICATION_ATOMICITY_UNRESOLVED`.

## Question

Lipi stores seven tokens for `M-20`, with `036` between `861` and `460`. Mayig stores eight graphemes and places consecutive `P147 P147` in the corresponding slot. Mayig defines each `P147` as three adjacent full-height vertical strokes. The live question was whether the repeat represented two source units collapsed by Lipi or an accidentally duplicated Mayig grapheme.

## Direct evidence

- Lipi row `2548.1`: `+390-005-002-861-036-460-513+`, text length 7, signs 7.
- Mayig `M-20A`: `P086 P125 P122 P385 P147 P147 P215 P275`, grapheme count 8.
- CISI 1 PDF page 49 / printed page 13 shows both `M-20 A` and `M-20 a`.
- Between the diamond form and the three-triangle form, both published views show six full-height vertical strokes. All six strokes are therefore source-real; the second `P147` is not a transcription duplicate of a source that contains only one three-stroke group.
- The six strokes form one continuous, evenly spaced run. There is no enclosure or visibly larger middle gap that independently fixes a boundary after stroke three.

## Object-level decision

- Preserve the graphic fact as one `SIX_VERTICAL_STROKE_RUN` region on `M-20`.
- Treat Lipi's single `036` and Mayig's `P147 P147` as competing catalogue tokenizations of that same source-visible region.
- Do not promote either Lipi's seven-token count or Mayig's eight-grapheme count to a source-established structural-unit count. The source proves six stroke elements, not one versus two sign units.
- Do not accept a global `036 = P147 P147` rule. This gate is object-bound and does not resolve the sign-list conventions behind either catalogue.
- Do not rewrite either raw corpus.

## Research consequence

For M-20, the post-`861` continuation is source-visible as `SIX_VERTICAL_STROKE_RUN`, then the forms represented by Lipi `460` and `513`. Analyses may retain Lipi's `861-036-460-513` at explicitly labelled catalogue-token level, or Mayig's expanded representation at explicitly labelled Mayig-grapheme level. Count-sensitive or sign-adjacency analyses must not silently treat either tokenization as source-grounded.

This closes the duplication branch but leaves atomicity unresolved. It therefore does not justify changing the structural count from seven to eight, nor does it establish a sign value, meaning, phonetic reading, language identification, translation, or decipherment claim.

## Preserved evidence

- `research/data/sign_crosswalk/source_panels/m020_six_stroke_run_segmentation/M-20_A_a_CISI1_pdf49_print13.png`, SHA-256 `47DF5B89C5E4FE01337DAAE7B79ABA3298000DE0DF13623CB0C1C8FE4B4F8994`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m020.json`: `B163F7F5C510314FD5FCC22A441E5FEDE45B4E6F1D8FD1A51408B1D8177F25AA`.
- Mayig `P147.json`: `E80F45A3DCDD5E99B90E32AF50BD8E46BD689F7B20ED633D64037FB01AC3AE03`.
