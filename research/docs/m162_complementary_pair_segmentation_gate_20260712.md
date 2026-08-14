# M-162 complementary-pair segmentation gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_SIX_UNITS_SUPPORT_PROBABLE_LIPI_UNIT_OMISSION_BEFORE_552_NOT_MAYIG_DUPLICATION`.

## What this is and why it exists

This is a gate: a written decision that settles one specific question against the source images, so that later analysis does not have to keep guessing. This gate covers one object, `M-162`.

Two catalogues describe the same inscriptions. Lipi is the numeric catalogue that writes signs as numbers like `552`, and each of its entries is called a token. Mayig is the Parpola-style catalogue that writes signs as `P` codes like `P230`, and each of its entries is called a grapheme. Mayig records one more unit here than Lipi does, and the surplus has to be explained before either row can be counted.

The earlier objects of this kind involved a repeated Mayig grapheme, which invites the easy explanation that the catalogue duplicated a line by accident. M-162 does not offer that escape: the two Mayig units in question are different signs. So the question becomes which catalogue is short, and where.

## Question

Lipi stores five tokens for `M-162`; Mayig stores six. Unlike M-111 and M-161, the Mayig sequence contains no repeated grapheme. The discrepancy is localized to one Lipi `552` position versus adjacent Mayig `P230 P234`.

## Direct evidence

Each item below is something a pinned catalogue record or a published plate actually shows.

- Lipi row `2688.1`: `+740-760-840-552-003+`, text length 5, signs 5.
- Mayig `M-162A`: `P324 P332 P349 P230 P234 P123`, grapheme count 6.
- CISI 1 PDF page 85 / printed page 49 shows both `M-162 A` and `M-162 a`.
- Both published views show six separately bounded inscription units. The middle pair corresponding to `P230 P234` consists of two distinct complementary graphics with separate boundaries.

So Mayig's extra unit is source-visible. It is not duplicated transcription, and it is not one bounded graphic that Mayig chose to split into components.

## M-126 discriminator

A discriminator is a second object that tells two otherwise equal explanations apart. Here the two explanations are that Lipi dropped a unit, or that Lipi's `552` is a macro token standing for both forms at once. `M-126` decides between them, because it carries the same adjacent Mayig pair `P230 P234`. After its non-counting `P000` damage event is separated out, that row has four source-visible signs, and Lipi supplies two positions across the pair: `520-552`.

So on M-126 Lipi does use two tokens for this pair. On `M-162` the same Mayig pair is source-visible as two units, but Lipi supplies only `552`. A missing Lipi unit before `552` — probably the object-local counterpart of M-126's `520` — is therefore more plausible than a stable Lipi `552` macro spanning both forms.

The inference is object-bound and comparative. It does not accept global `520/P230` or `552/P234` edges, and it does not authorize rewriting the raw Lipi row.

## Normalization and research consequence

- Structural source-unit count for `M-162` is `6`, not `5`.
- For source-unit models, normalize the middle as `840, <MISSING_LIPI_UNIT probable_520>, 552, 003`, or use the pinned Mayig six-unit sequence while retaining namespace provenance.
- Do not treat Lipi `840-552` as a direct sign-level adjacency on this object; one source unit intervenes.
- `M-162` may re-enter source-count and order analyses only with the missing unit restored as an explicit unresolved position.
- The M-161 control remains `unresolved_compound_or_omission_policy`; M-162 is narrower because M-126 supplies an external object-level pair discriminator.

No sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is added.

## Preserved evidence

Each file below is listed with its SHA-256 hash, so a later reader can confirm the exact bytes this decision was made from.

- `research/data/sign_crosswalk/source_panels/m162_complementary_pair/M-162_A_a_CISI1_pdf85_print49.png`, SHA-256 `1D0834C57AA40BAB713956BBC950106AC0CC0F32274C9DBE2D01F937BD7BACEC`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m162.json`: `855FD84AE42047B0F3423D80BE526D03AD3C615089634A2E59AC758529F02FC7`.
- Mayig `P230.json`: `3D1E79DA98AB14E6266582A282767BE6B595784603565658FD166D4B15133B7F`.
- Mayig `P234.json`: `C0FC2C18ED93ECEBAACBBBB89BF1C9449FB7A0C380EA5AA3C0626A1C6544DFCF`.
