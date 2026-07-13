# M-98 terminal-parenthesis omission and Lipi-extra class closure

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_FOUR_UNITS_MAYIG_OMITS_TERMINAL_RIGHT_PARENTHESIS`.

## Question

M-98 is the fourth and final `unflagged_lipi_extra` row. Lipi stores four tokens; Mayig stores three graphemes. The source question was whether Lipi's terminal `900` is a separate unit or part of the preceding seven-stroke graphic.

## Direct evidence

- Lipi row `2625.1`: `+740-585-017-900+`, text length 4, signs 4, direction `R/L`.
- Mayig `M-98A`: `P324 P288 P127`, grapheme count 3.
- The object-local alignment is `740/P324, 585/P288, 017/P127, 900/[missing]`.
- Mayig defines `P127` as seven short vertical strokes and mediates it to Wells `W017`. It defines `P154` as a right parenthesis and mediates it to `W900`.
- CISI 1 PDF page 73 / printed page 37 publishes `M-98 A` and `M-98 a`.
- Both views show four spatially separate units. The seven-stroke group is arranged 4+3, and a full-height curved right-parenthesis sign stands independently beyond it.

The terminal sign is source-real and separately bounded. Mayig omits it from M-98.

## Object-level decision

- Use source-unit count `4` for `M-98`.
- Normalize the Mayig representation as `P324, P288, P127, <MISSING_TERMINAL_RIGHT_PARENTHESIS>`.
- Record the missing position as `P154-like` only at object-evidence level; do not silently edit `m098.json` or promote a global `900 = P154` edge here.
- Reject Mayig `P127` as terminal on this object and reject its apparent `P127-END` source adjacency.
- Keep the raw catalogues unchanged.

## Lipi-extra class result

All four `unflagged_lipi_extra` rows are now source-adjudicated:

- `M-10`: catalogue segmentation, Lipi `032 033` versus one Mayig five-stroke run.
- `M-72`: catalogue segmentation, Lipi `003 002` versus one Mayig five-stroke run.
- `M-41`: true Mayig omission of a bounded middle fish.
- `M-98`: true Mayig omission of a bounded terminal parenthesis.

The class is evenly split between atomicity policy and missing data. There is no defensible rule to prefer Lipi's longer count automatically; each mismatch requires source localization. Combined with the completed Mayig-extra class, all twelve rows in the two `unflagged_*_extra` classes are now source-adjudicated.

This result changes structural counts and adjacencies only. No sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is accepted.

## Preserved evidence

- `research/data/sign_crosswalk/source_panels/m098_terminal_parenthesis_omission/M-98_A_a_CISI1_pdf73_print37.png`, SHA-256 `85B1D71C536DAF3EAE8C40C684D388035D4589B16EE4BBDA65379ADA5CCB58EE`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m098.json`: `C11E857922E90F4284088CF8BF847184C09228EEA452C92857CC0867C3D5AAE8`.
- Mayig `P154.json`: `203EEA79DD0D49017B4F3046DAB0CF389FDA44E8C6C03D282038EC56492279EE`.
