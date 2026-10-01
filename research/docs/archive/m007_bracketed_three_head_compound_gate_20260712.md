# M-7 bracketed three-head compound gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_NINE_COMPOUND_CLUSTERS_LIPI_101_MAYIG_DECOMPOSES_P010`.

## What this is and why it exists

Two catalogues can count the same inscription differently without either being wrong. They may simply be describing it at different levels of detail. One writes a compound sign as a single unit; the other writes its parts. Both are accurate, and averaging them is meaningless.

That is what happens on M-7. Lipi, the numeric catalogue, records nine tokens. Mayig, the `P`-code catalogue, records eleven. The gap is entirely at one spot, where Lipi has `101` and Mayig has three codes, `P154 P009 P154`. This note decides which count the object itself supports.

## Question

Lipi stores nine tokens for `M-7`; Mayig stores eleven graphemes, meaning eleven sign entries. Everything else aligns cleanly, so both extra Mayig positions sit in the span where Lipi uses `101` and Mayig uses `P154 P009 P154`. The source question was whether those are three separately spaced signs or three visible parts of one compound cluster.

## Direct evidence

- Lipi row `2536.1`: `+407-845-140-740-101-923-240-002-861+`, text length 9, signs 9, direction `R/L`.
- Mayig `M-7A`: `P086 P352 P011 P324 P154 P009 P154 P175 P062 P122 P385`, grapheme count 11.
- The object-local alignment is `407/P086, 845/P352, 140/P011, 740/P324, 101/[P154+P009+P154], 923/P175, 240/P062, 002/P122, 861/P385`.
- Mayig defines `P009` as a person with three heads and `P154` as a right parenthesis. The decisive detail is that Mayig's own namespace already has a code for the whole thing: `P010` is a person with three heads bracketed by right parentheses, mediated directly to Wells `W101/W103`.
- CISI 1 PDF page 42 / printed page 6 publishes `M-7 A` and `M-7 a`.
- Both views show nine clusters at compound level. The two parentheses flank the three-headed figure and read as part of it, with no gap on either side of the kind that separates one sign from the next.

So the three components are parts of one graphic, not two extra signs spaced out on the object. Mayig has taken apart a compound that its own catalogue could have written as `P010`.

## Object-level decision

- Use compound-level structural count `9` for `M-7`.
- For sign-unit analysis, fold Mayig positions 5-7 into one cluster: `BRACKETED_THREE_HEAD_COMPOUND`, the `P010-like` form.
- Keep the eleven-grapheme Mayig version only for analysis that is explicitly about sign constituents.
- Do not count `P154-P009` or `P009-P154` as adjacencies between signs. They are relations inside one sign.
- Write the outer source sequence as `... P324, BRACKETED_THREE_HEAD_COMPOUND, P175 ...`.
- Leave both raw catalogues unchanged.

## Research consequence

The apparent two-sign surplus dissolves without anyone inventing missing data. Lipi and Mayig were describing the same marks at different levels. The source backs Lipi's nine compound-level units, and Mayig's eleven entries are still worth having, because they record how the compound is built.

The rule that follows is about hygiene. A sequence model must pick one level and say which, because mixing compound tokens and their constituents in one stream produces counts that correspond to nothing on any object.

The object is complete and clearly preserved, so damage plays no part in this decision. No sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is accepted.

## Preserved evidence

Each file is listed with its SHA-256 hash, so a later reader can confirm the exact bytes behind this decision.

- `research/data/sign_crosswalk/source_panels/m007_bracketed_three_head_compound/M-7_A_a_CISI1_pdf42_print6.png`, SHA-256 `75722E6F3FAF764D3586AE83B1A0A04DA4AAEB08FE9C82C0ED7CADBBF97EFEA0`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m007.json`: `B5B95510B88F08ABD23A276EBA851B60ED5416482B4418A95B1C65896A9F9DD7`.
- Mayig `P010.json`: `E321C187C9B947EBAF852697BC0B60B62402CE483D1DA16BF46BF274D1269836`.
