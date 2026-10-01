# M-72 five-stroke-run segmentation gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_FIVE_STROKE_RUN_LIPI_003_002_SPLIT_MAYIG_P125_ATOMICITY_UNRESOLVED`.

## What this is and why it exists

This is a gate: a written decision that settles one specific question against the source images, so that later analysis does not have to keep guessing. This gate covers one object, `M-72`.

Two catalogues describe the same inscriptions. Lipi is the numeric catalogue that writes signs as numbers like `003`, and each of its entries is called a token. Mayig is the Parpola-style catalogue that writes signs as `P` codes like `P125`, and each of its entries is called a grapheme. The two catalogues give `M-72` different lengths, and that has to be settled before either row can be used.

The disagreement is about segmentation — where one sign stops and the next begins. Nobody disputes what is cut into the object. The dispute is how many signs that same material counts as.

## Question

Lipi stores seven tokens for `M-72`; Mayig stores six graphemes. Lining the two rows up position by position leaves exactly one place where they differ: Lipi `003 002` against Mayig `P125`. So the question to put to the source images was whether Mayig omitted a sign, or grouped the same stroke material differently.

## Direct evidence

Each item below is something a pinned catalogue record or a published plate actually shows.

- Lipi row `2600.1`: `+740-255-705-140-003-002-861+`, text length 7, signs 7, direction `R/L`.
- Mayig `M-72A`: `P324 P073 P316 P011 P125 P385`, grapheme count 6.
- The object-local alignment is `740/P324, 255/P073, 705/P316, 140/P011, [003+002]/P125, 861/P385`.
- Mayig defines `P125` as five simple vertical strokes. Its feature metadata separately describes the three-stroke and two-stroke neighborhoods represented by `P123/W003` and `P122/W002`.
- CISI 1 PDF page 67 / printed page 31 publishes inscription-bearing `M-72 A` and `M-72 a`.
- Both views show the same five adjacent short vertical strokes between the person form and the terminal diamond/leaf form. There is no fracture, enclosure, or larger gap that fixes a boundary after stroke three.

So the source has no missing Mayig glyph. Lipi segments the run as three strokes plus two; Mayig groups all five together.

## Object-level decision

The safe move is to record what the object shows and refuse to pick a winner between the two catalogues:

- Preserve the disputed region as `FIVE_SHORT_VERTICAL_STROKE_RUN`.
- Retain Lipi `003 002` only at Lipi-token level and Mayig `P125` only at Mayig-grapheme level.
- Do not promote either Lipi's seven-token count or Mayig's six-grapheme count to a source-established sign-unit count for M-72.
- Do not count Lipi's internal `003-002` transition as source-established sign adjacency.
- Keep both raw catalogues unchanged and do not infer a global compound rule from this object.

## Research consequence

Atomicity is the question of what counts as one indivisible sign. M-72 repeats M-10's catalogue-atomicity failure with the split reversed: `3+2` strokes versus one five-stroke grapheme. Source-grounded analysis can still keep the outer sequence as `... 140/P011, FIVE_SHORT_VERTICAL_STROKE_RUN, 861/P385 ...`, while leaving the internal Lipi boundary out of structural-count and transition statistics.

The catalogue marks the object `Poor`, and `M-72 A` is abraded, but the five-stroke run stays visible in both inscription views and is clearest on `M-72 a`. No sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is accepted.

## Preserved evidence

Each file below is listed with its SHA-256 hash, so a later reader can confirm the exact bytes this decision was made from.

- `research/data/sign_crosswalk/source_panels/m072_five_stroke_run/M-72_A_a_CISI1_pdf67_print31.png`, SHA-256 `596252CCE64F457870B56D6466F176EAFCAD0F97603D44EDDD546FBBFA01E916`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m072.json`: `5AA9D73971D45CBF2FB95DB0C6D7594AF28BA8B430A147D1C219259D99CB91E1`.
- Mayig `P125.json`: `DDDC125A43043ABDBC4BFA6477CE27DB69FD7B14B165EEA70391478B7EA8D76A`.
