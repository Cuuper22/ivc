# M-98 terminal-parenthesis omission and Lipi-extra class closure

Date: 2026-07-12 America/Los_Angeles

Decision: `SOURCE_VISIBLE_FOUR_UNITS_MAYIG_OMITS_TERMINAL_RIGHT_PARENTHESIS`.

## What this is and why it exists

This is a gate: a written decision that settles one specific question against the source images, so that later analysis does not have to keep guessing. It also closes a whole class of disagreements, because M-98 is the last unresolved object in that class.

Two catalogues describe the same inscriptions. Lipi is the numeric catalogue that writes signs as numbers like `900`, and each of its entries is called a token. Mayig is the Parpola-style catalogue that writes signs as `P` codes like `P127`, and each of its entries is called a grapheme. The `unflagged_lipi_extra` class is the set of objects where Lipi records more entries than Mayig with no flag explaining why. Each such row needs a source check before it can be used, because there are two very different explanations: Mayig might be missing real material, or the two catalogues might just be cutting the same material into units differently.

## Question

M-98 is the fourth and final `unflagged_lipi_extra` row. Lipi stores four tokens; Mayig stores three graphemes. The source question was whether Lipi's terminal `900` is a separate unit or part of the preceding seven-stroke graphic.

## Direct evidence

Each item below is something a pinned catalogue record or a published plate actually shows.

- Lipi row `2625.1`: `+740-585-017-900+`, text length 4, signs 4, direction `R/L`.
- Mayig `M-98A`: `P324 P288 P127`, grapheme count 3.
- The object-local alignment is `740/P324, 585/P288, 017/P127, 900/[missing]`.
- Mayig defines `P127` as seven short vertical strokes and mediates it to Wells `W017`. It defines `P154` as a right parenthesis and mediates it to `W900`.
- CISI 1 PDF page 73 / printed page 37 publishes `M-98 A` and `M-98 a`.
- Both views show four spatially separate units. The seven-stroke group is arranged 4+3, and a full-height curved right-parenthesis sign stands independently beyond it.

So the terminal sign is source-real and separately bounded. This is the missing-material case, not the segmentation case: Mayig omits the sign from M-98.

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

That is the useful result. The class splits evenly between atomicity policy — which catalogue treats how much material as one indivisible sign — and plain missing data. Two of four go each way. So there is no defensible rule that automatically prefers Lipi's longer count. Every mismatch has to be localized against the source, one object at a time. Combined with the completed Mayig-extra class, all twelve rows in the two `unflagged_*_extra` classes are now source-adjudicated.

This result changes structural counts and adjacencies only. No sign value, meaning, phonetic reading, language identification, translation, or decipherment claim is accepted.

## Preserved evidence

Each file below is listed with its SHA-256 hash, so a later reader can confirm the exact bytes this decision was made from.

- `research/data/sign_crosswalk/source_panels/m098_terminal_parenthesis_omission/M-98_A_a_CISI1_pdf73_print37.png`, SHA-256 `85B1D71C536DAF3EAE8C40C684D388035D4589B16EE4BBDA65379ADA5CCB58EE`.
- CISI 1 PDF SHA-256: `47A4DA4227CFB7BAA56D6A561E25797225499D0EC54F5A702A82C67AB4746D4D`.
- Mayig `m098.json`: `C11E857922E90F4284088CF8BF847184C09228EEA452C92857CC0867C3D5AAE8`.
- Mayig `P154.json`: `203EEA79DD0D49017B4F3046DAB0CF389FDA44E8C6C03D282038EC56492279EE`.
