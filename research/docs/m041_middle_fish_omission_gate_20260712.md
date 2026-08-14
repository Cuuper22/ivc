# M-41 middle-fish omission gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_NINE_UNITS_MAYIG_OMITS_MIDDLE_FISH_POSITION`.

## Question

Lipi stores nine tokens for `M-41`; Mayig stores eight graphemes. The object-local alignment localizes the difference to Lipi `240-233-235` against Mayig `P062-P060`. The source question was whether Lipi split one compound fish form or Mayig omitted a separately bounded middle sign.

## Direct evidence

- Lipi row `2569.1`: `+740-636-240-233-235-002-405-125-820+`, text length 9, signs 9, direction `R/L`.
- Mayig `M-41A`: `P324 P270 P062 P060 P122 P086 P035 P378`, grapheme count 8.
- The aligned sequence is `740/P324, 636/P270, 240/P062, 233/[missing], 235/P060, 002/P122, 405/P086, 125/P035, 820/P378`.
- Mayig describes `P058` as a fish with a horizontal line through its body. The existing 233/P058 concordance has 13 aligned supporting positions and no recorded counterexample, although the global edge remains unaccepted.
- CISI 1 PDF page 57 / printed page 21 publishes `M-41 A` and `M-41 a`.
- Both views show nine bounded inscription units. At the disputed span they show three separate fish-family signs, including a bounded middle fish between the forms represented by Mayig `P062` and `P060`.

The middle sign is source-real and separately bounded. Mayig omits one grapheme position on M-41.

## Object-level decision

- Use source-unit count `9` for `M-41`.
- Preserve the normalized span as `P062, <MISSING_MAYIG_MIDDLE_FISH>, P060`.
- Record the missing position as `P058-like` only at object-evidence level; do not silently edit `m041.json` or promote a global `233 = P058` rule here.
- Reject Mayig's direct `P062-P060` transition on M-41 as a literal source adjacency.
- Retain Lipi `240-233-235` as the source-count-preserving catalogue path for this object.

## Research consequence

M-41 is the first checked `unflagged_lipi_extra` row where the extra Lipi token is an actual source unit rather than a segmentation convention. Count-sensitive analyses should use nine positions, and transition statistics must insert the omitted middle fish between Mayig `P062` and `P060`. This is a concrete missing-data correction at analysis level, not a semantic interpretation.

No sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is accepted.

## Preserved evidence

- `research/data/sign_crosswalk/source_panels/m041_middle_fish_omission/M-41_A_a_CISI1_pdf57_print21.png`, SHA-256 `6271DFD711AF975834B63F1AFF3328C9E7057762BB8C67E6A75B9A3F6D5A840D`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m041.json`: `A296D1C2A202FECA2F104067C115872204BDE73C79EB80F0B9A18551B4B2C93D`.
- Mayig `P058.json`: `D5D2AB6451FA581DE4A707D9E46B1798F9A054B3528D39B0122C540213DD1AA3`.
