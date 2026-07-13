# M-7 bracketed three-head compound gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_NINE_COMPOUND_CLUSTERS_LIPI_101_MAYIG_DECOMPOSES_P010`.

## Question

Lipi stores nine tokens for `M-7`; Mayig stores eleven graphemes. The clean alignment localizes both extra Mayig positions to the span where Lipi uses `101` and Mayig uses `P154 P009 P154`. The source question was whether these are three separately spaced signs or visible constituents of one compound cluster.

## Direct evidence

- Lipi row `2536.1`: `+407-845-140-740-101-923-240-002-861+`, text length 9, signs 9, direction `R/L`.
- Mayig `M-7A`: `P086 P352 P011 P324 P154 P009 P154 P175 P062 P122 P385`, grapheme count 11.
- The object-local alignment is `407/P086, 845/P352, 140/P011, 740/P324, 101/[P154+P009+P154], 923/P175, 240/P062, 002/P122, 861/P385`.
- Mayig defines `P009` as a person with three heads and `P154` as a right parenthesis. Its own feature namespace also defines `P010` as a person with three heads bracketed by right parentheses and mediates it directly to Wells `W101/W103`.
- CISI 1 PDF page 42 / printed page 6 publishes `M-7 A` and `M-7 a`.
- Both views show nine compound-level inscription clusters. The two parentheses visibly flank and integrate with the three-headed figure, without inter-sign spacing around either side.

The three components are graphic constituents, not two additional source-spaced sign clusters. Mayig decomposes a compound that its own namespace can encode as `P010`.

## Object-level decision

- Use compound-level structural count `9` for `M-7`.
- Normalize Mayig positions 5-7 to one `BRACKETED_THREE_HEAD_COMPOUND` / `P010-like` cluster for sign-unit analysis.
- Retain the eleven-grapheme Mayig representation only for explicitly constituent-level analysis.
- Do not count `P154-P009` or `P009-P154` as inter-sign source adjacencies. They are internal compound relations.
- Preserve the outer source sequence as `... P324, BRACKETED_THREE_HEAD_COMPOUND, P175 ...`.
- Keep both raw catalogues unchanged.

## Research consequence

M-7 resolves the apparent two-sign surplus without inventing missing data: Lipi and Mayig operate at different decomposition levels. The source supports Lipi's nine compound-level units, while Mayig's eleven entries preserve useful internal morphology. Statistics must choose one level explicitly rather than mixing compound tokens and constituents in the same sequence model.

The object is complete and clear, so damage does not qualify this decision. No sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is accepted.

## Preserved evidence

- `research/data/sign_crosswalk/source_panels/m007_bracketed_three_head_compound/M-7_A_a_CISI1_pdf42_print6.png`, SHA-256 `75722E6F3FAF764D3586AE83B1A0A04DA4AAEB08FE9C82C0ED7CADBBF97EFEA0`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m007.json`: `B5B95510B88F08ABD23A276EBA851B60ED5416482B4418A95B1C65896A9F9DD7`.
- Mayig `P010.json`: `E321C187C9B947EBAF852697BC0B60B62402CE483D1DA16BF46BF274D1269836`.
