# 032-002-861 533-717 Component Ecology

Date: 2026-05-29

This note asks whether the two-sign ending `533-717` is one thing or two. If `533` and `717` each led their own lives elsewhere in the corpus, the pair would look like a phrase built from parts. If they only ever appear together, it is more likely a single frozen unit. The counting is simple and the answer is lopsided, so the note tells the next pass to stop trying to read the halves separately.

## Question

Does `533-717` behave like a decomposable phrase with independent component ecology — each sign appearing on its own elsewhere, in its own range of contexts — or like a fixed terminal two-sign unit after `002-861`?

## Result

"Strict" rows are those with complete source strings after deduplication. Counts follow:

- Strict rows scanned: `4011`
- `533-717` adjacent occurrences: `2`
- Independent `533` occurrences outside `533-717`: `0`
- Independent `717` occurrences outside `533-717`: `37`
- Broad no-icon `SEAL:R` `002-861` rows checked: `7`
- Narrow cuboid-convex no-icon `SEAL:R` `002-861` rows checked: `3`

## Register Tail Fields

A "register" is a coarse class of object defined by site, type, and shape; the "tail field" is the set of endings that class actually takes.

- Broad no-icon `SEAL:R`: `<END>:3;533 717:2;360 520 919 140:1;603:1`
- Narrow cuboid-convex no-icon `SEAL:R`: `533 717:2;360 520 919 140:1`

## Decision

Status: `533_717_fixed_terminal_unit_not_decomposed_value`.

- `533-717` remains the only fixed-prefix repeated terminal tail after `002-861`, but this scan does not promote its internal components to independent values.
- The pair should be treated as a fixed two-sign restricted-tail unit for the next grammar pass, not as separately readable `533` plus `717`.
- The broad no-icon SEAL:R field still contains bare closure, `603`, and a long tail, so `533-717` is not the marker of that whole branch.
- Inside the narrower cuboid-convex no-icon SEAL:R field, `533-717` competes with the long tail `360-520-919-140`; that is narrower pressure, not a value.
- The next useful question is source-normalized contrast between fixed-tail units inside the post-`002-861` secondary zone, not a component-level translation of `533` or `717`.

Accepted values, phonetics, language identity, translations, and exact source-normalized token boundaries remain 0/unaccepted.
