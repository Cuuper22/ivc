# M-10 five-stroke-run segmentation gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_FIVE_STROKE_RUN_LIPI_032_033_SPLIT_MAYIG_P151_ATOMICITY_UNRESOLVED`.

## What this is and why it exists

Suppose an inscription has five vertical strokes in a row. Is that one sign, or two signs of two strokes and three strokes? The strokes are a fact. The grouping is a decision, and different catalogues make it differently.

M-10 is the first object in the class where Lipi, the numeric catalogue, has more tokens than Mayig, the `P`-code catalogue. That is the opposite of the earlier cases, so the natural suspicion is that Mayig dropped a sign. This note checks the plate and finds something less alarming: both catalogues see the same marks and cut them into units differently. The count difference is real, and it is not a missing sign.

## Question

M-10 begins the `unflagged_lipi_extra` mismatch class, the group of objects where Lipi holds the extra token. Lipi stores eleven tokens; Mayig stores ten graphemes, meaning ten sign entries. Three explanations were possible: Lipi preserves a physical sign that Mayig lost, Mayig omitted one, or the two catalogues divide the same marks differently.

## Direct evidence

- Lipi row `2539.1`: `+405-061-070-032-033-706-235-806-002-267-455+`, text length 11, signs 11, direction `R/L`.
- Mayig `M-10A`: `P086 P204 P114 P151 P316 P060 P364 P122 P067 P221`, grapheme count 10.
- The object-local alignment is `405/P086, 061/P204, 070/P114, [032+033]/P151, 706/P316, 235/P060, 806/P364, 002/P122, 267/P067, 455/P221`.
- Mayig defines `P151` as five adjacent simple tall vertical strokes. Lipi's established graphic neighborhoods make `032` the two-stroke member and `033` the three-stroke member.
- CISI 1 PDF page 45 / printed page 9 publishes inscription-bearing `M-10 A` and `M-10 a`. Both show the same five adjacent vertical strokes at the disputed position.
- The strokes form one continuous, evenly spaced run with nothing enclosing it. There is no wider gap after the second stroke, so the source itself does not mark a boundary between `032` and `033`.

That settles two of the three explanations. Lipi has no extra physical mark behind its extra token, and Mayig has left nothing out. Atomicity means where a catalogue decides one sign ends and the next begins, and the count difference is purely that choice.

## Object-level decision

- Record the disputed region as `FIVE_VERTICAL_STROKE_RUN`, which is what the object actually shows.
- Keep Lipi `032 033` as a Lipi-token-level fact and Mayig `P151` as a Mayig-grapheme-level fact. Neither is a fact about the seal.
- Do not treat either Lipi's eleven or Mayig's ten as the source-established sign-unit count for M-10. The source does not supply one.
- Do not count Lipi's internal `032-033` transition as a sign adjacency. No boundary is visible there.
- Leave the raw catalogues unchanged, and do not turn one object into a general compound rule.

## Research consequence

M-10 is not evidence that Mayig dropped a sign. Look at graphic content rather than token counts and the ten-versus-eleven gap disappears: both catalogues encode the same five strokes, Mayig as `P151` and Lipi as `032 033`.

Analysis can still use the object. Keep the outer sequence as `... 070/P114, FIVE_VERTICAL_STROKE_RUN, 706/P316 ...` and leave the internal boundary out of sign-count and transition statistics. The parts that are source-grounded stay usable; only the invented boundary is excluded.

The object has substantial damage at a corner and in the lower field. The five-stroke region is clear in both inscription views and the damage does not reach it, so it does not qualify this decision. No sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is accepted.

## Preserved evidence

Each file is listed with its SHA-256 hash, so a later reader can confirm the exact bytes behind this decision.

- `research/data/sign_crosswalk/source_panels/m010_five_stroke_run/M-10_A_a_CISI1_pdf45_print9.png`, SHA-256 `6455F4D41077EC3A4442F2D9311CAB3B3FA8DF1DDE4515AC574A68CB9F31A41E`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m010.json`: `9BA90F87A38B52A66EBAF1F5EC8C9C86CAB45BC9B234E46E833FEA39F68AE367`.
- Mayig `P151.json`: `B614599B4E078CA26E97BF07FCD192DCA6C48032703A4FECAB87F21AFCCFDD53`.
