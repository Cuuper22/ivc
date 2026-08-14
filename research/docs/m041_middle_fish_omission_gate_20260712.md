# M-41 middle-fish omission gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_NINE_UNITS_MAYIG_OMITS_MIDDLE_FISH_POSITION`.

## What this is and why it exists

Most count mismatches in this corpus turn out to be bookkeeping: two catalogues cutting the same marks into units differently. M-41 is the exception. Here a sign is genuinely present on the object and genuinely absent from one catalogue.

That distinction matters because the two cases call for opposite responses. A segmentation difference should be left alone and labeled. A real omission has to be repaired in analysis, or every transition statistic across that span will join two signs that never touched.

## Question

Lipi, the numeric catalogue, stores nine tokens for `M-41`; Mayig, the `P`-code catalogue, stores eight graphemes. Lining the two up on this object puts the whole difference in one span: Lipi's `240-233-235` against Mayig's `P062-P060`. The source question was whether Lipi split one compound fish form into pieces, or Mayig omitted a middle sign that stands on its own.

## Direct evidence

- Lipi row `2569.1`: `+740-636-240-233-235-002-405-125-820+`, text length 9, signs 9, direction `R/L`.
- Mayig `M-41A`: `P324 P270 P062 P060 P122 P086 P035 P378`, grapheme count 8.
- The aligned sequence is `740/P324, 636/P270, 240/P062, 233/[missing], 235/P060, 002/P122, 405/P086, 125/P035, 820/P378`.
- Mayig describes `P058` as a fish with a horizontal line through its body. The existing 233/P058 concordance has 13 aligned supporting positions and no recorded counterexample. That edge is still unaccepted as a global mapping, so it is a hint about what the missing sign looks like, not an identification of it.
- CISI 1 PDF page 57 / printed page 21 publishes `M-41 A` and `M-41 a`.
- Both views show nine bounded inscription units. Across the disputed span they show three separate fish-family signs, and the middle fish has its own boundary, sitting between the forms Mayig calls `P062` and `P060`.

So the middle sign is on the object and separately bounded. Mayig omits one grapheme position on M-41.

## Object-level decision

- Use source-unit count `9` for `M-41`.
- Write the normalized span as `P062, <MISSING_MAYIG_MIDDLE_FISH>, P060`, so the gap is explicit rather than closed over.
- Note the missing position as `P058-like` at the level of this object's evidence only. Do not edit `m041.json`, and do not use this to promote a global `233 = P058` rule.
- Reject Mayig's direct `P062-P060` transition on M-41. A sign stands between them, so it is not a source adjacency.
- Keep Lipi `240-233-235` as the catalogue path that preserves the correct source count for this object.

## Research consequence

M-41 is the first checked `unflagged_lipi_extra` row where Lipi's extra token corresponds to a real unit on the object rather than to a segmentation convention. Count-sensitive analyses should use nine positions, and transition statistics must put the omitted middle fish back between Mayig `P062` and `P060`. This is a missing-data correction applied in analysis. It interprets nothing.

No sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is accepted.

## Preserved evidence

Each file is listed with its SHA-256 hash, so a later reader can confirm the exact bytes behind this decision.

- `research/data/sign_crosswalk/source_panels/m041_middle_fish_omission/M-41_A_a_CISI1_pdf57_print21.png`, SHA-256 `6271DFD711AF975834B63F1AFF3328C9E7057762BB8C67E6A75B9A3F6D5A840D`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m041.json`: `A296D1C2A202FECA2F104067C115872204BDE73C79EB80F0B9A18551B4B2C93D`.
- Mayig `P058.json`: `D5D2AB6451FA581DE4A707D9E46B1798F9A054B3528D39B0122C540213DD1AA3`.
