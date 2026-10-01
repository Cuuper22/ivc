# M-45 double-grid-pair segmentation gate

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_SEVEN_UNITS_THIRD_617_DOUBLE_GRID_CONFIRMATION`.

## What this is and why it exists

Five objects show the same discrepancy: Lipi, the numeric catalogue, writes one token `617` where Mayig, the `P`-code catalogue, writes the grid sign twice as `P268 P268`. Two of the five had already been checked against the plates and both showed two grids.

Two agreeing cases is a pattern worth doubting. The value of a third check lies in its ability to fail, so this note goes looking for the object that breaks the pattern. M-45 does not break it.

## Question

M-45 is the third direct test of the recurring Lipi `617` versus Mayig `P268 P268` discrepancy. Lipi stores six tokens; Mayig stores seven graphemes, meaning seven sign entries. The live question was whether the source again shows two separately bounded grids, or whether this object contradicts the emerging pair pattern.

## Direct evidence

- Lipi row `2573.1`: `+617-831-013-302-840-032+`, text length 6, signs 6, direction `R/L`.
- Mayig `M-45A`: `P268 P268 P372 P139 P205 P349 P145`, grapheme count 7.
- CISI 1 PDF page 58 / printed page 22 publishes `M-45 A` and `M-45 a`.
- Both views show seven bounded inscription units. The pair at the start of reading order is two grid forms, each with its own outer boundary.

So the Mayig pair is backed by the source here too. M-45 has seven structural units, not six.

## Object-level decision

- Use source-unit count `7` for `M-45`.
- Keep both grids as separate positions.
- Reject Lipi `617` as a literal one-unit structural count on this object.
- Write the source-confirmed prefix as `<GRID>, <GRID>, ...`. Only the second grid touches the unit that follows, so only that adjacency is real.
- Do not rewrite either raw corpus, and do not read a sign value out of the grid forms.

## Research consequence

M-45 joins M-161 and M-25 as a third independent case where one Lipi `617` corresponds to two separately bounded grids on the object and to Mayig `P268 P268`. Nothing checked so far contradicts it. The full overlap cluster holds five exact cases: `M-161`, `M-25`, `M-45`, `M-81`, and `M-4`.

For these three objects the old `compound_or_omission` question no longer blocks the count. Whether Lipi's convention is a compound token or repeat suppression, either way the object needs two positions, so the normalization is the same and the count can proceed without settling the catalogue's internal rule.

Three out of five is not a corpus rule. `617 -> P268 P268` is a strong candidate for a catalogue expansion policy, and it stays a candidate until the remaining objects are checked. M-81 is the right next test, because it puts `617` inside the sequence instead of at the start, which is where a pattern of this kind would be most likely to break.

This gate does not establish a sign value, meaning, phonetic reading, language identification, translation, or decipherment claim.

## Preserved evidence

Each file is listed with its SHA-256 hash, so a later reader can confirm the exact bytes behind this decision.

- `research/data/sign_crosswalk/source_panels/m045_double_grid_pair/M-45_A_a_CISI1_pdf58_print22.png`, SHA-256 `3B139296BE1B4DD8285DB1E48394556C2AB541C60DED8751BA4843FAA4365156`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m045.json`: `8111D98C9E2023053054901CA10F9A0B9120791999B9197F974B76133CA1E7D1`.
- Mayig `P268.json`: `34248A590A6E9508C42747CDA83871240599456F6BFE78D8E98EEB5B11E3F139`.
