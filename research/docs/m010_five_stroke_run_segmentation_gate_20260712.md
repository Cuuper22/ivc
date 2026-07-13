# M-10 five-stroke-run segmentation gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_FIVE_STROKE_RUN_LIPI_032_033_SPLIT_MAYIG_P151_ATOMICITY_UNRESOLVED`.

## Question

M-10 begins the `unflagged_lipi_extra` mismatch class. Lipi stores eleven tokens while Mayig stores ten graphemes. The source question was whether Lipi preserves an additional physical sign, Mayig omits one, or the catalogues segment the same graphic material differently.

## Direct evidence

- Lipi row `2539.1`: `+405-061-070-032-033-706-235-806-002-267-455+`, text length 11, signs 11, direction `R/L`.
- Mayig `M-10A`: `P086 P204 P114 P151 P316 P060 P364 P122 P067 P221`, grapheme count 10.
- The object-local alignment is `405/P086, 061/P204, 070/P114, [032+033]/P151, 706/P316, 235/P060, 806/P364, 002/P122, 267/P067, 455/P221`.
- Mayig defines `P151` as five adjacent simple tall vertical strokes. Lipi's established graphic neighborhoods make `032` the two-stroke member and `033` the three-stroke member.
- CISI 1 PDF page 45 / printed page 9 publishes inscription-bearing `M-10 A` and `M-10 a`. Both show the same five adjacent vertical strokes at the disputed position.
- The strokes form one continuous, evenly spaced, unenclosed run. No larger gap after stroke two fixes a source-visible boundary between `032` and `033`.

The source contains no extra physical glyph for Lipi and no omitted graphic material in Mayig. The count difference is a catalogue atomicity choice.

## Object-level decision

- Preserve the disputed region as `FIVE_VERTICAL_STROKE_RUN`.
- Retain Lipi `032 033` only at Lipi-token level and Mayig `P151` only at Mayig-grapheme level.
- Do not promote either Lipi's eleven-token count or Mayig's ten-grapheme count to a source-established sign-unit count for M-10.
- Do not count Lipi's internal `032-033` transition as a source-established sign adjacency.
- Keep the raw catalogues unchanged and do not infer a global compound rule from this one object.

## Research consequence

M-10 is not evidence that Mayig dropped a sign. Its ten-versus-eleven discrepancy disappears at graphic-content level: both catalogues encode the same five-stroke run, one as `P151` and the other as `032 033`. Source-grounded analyses can preserve the outer sequence as `... 070/P114, FIVE_VERTICAL_STROKE_RUN, 706/P316 ...` while excluding the internal boundary from sign-count and transition statistics.

The object has substantial corner and lower-field damage, but the five-stroke region is clear in both inscription views and is not touched by that damage. No sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is accepted.

## Preserved evidence

- `research/data/sign_crosswalk/source_panels/m010_five_stroke_run/M-10_A_a_CISI1_pdf45_print9.png`, SHA-256 `6455F4D41077EC3A4442F2D9311CAB3B3FA8DF1DDE4515AC574A68CB9F31A41E`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m010.json`: `9BA90F87A38B52A66EBAF1F5EC8C9C86CAB45BC9B234E46E833FEA39F68AE367`.
- Mayig `P151.json`: `B614599B4E078CA26E97BF07FCD192DCA6C48032703A4FECAB87F21AFCCFDD53`.
