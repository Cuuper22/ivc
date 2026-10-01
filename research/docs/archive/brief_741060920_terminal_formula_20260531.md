# 060-920 Terminal Cap / 741-060 Feeder Brief

Date: 2026-05-31  
Status: promoted candidate, metadata layer plus row-level source peek. Not accepted. No phonetic value, sign meaning, language identity, or translation is claimed.

## Claim

The cleanest structural object we currently have is the terminal cap `060-920` — a two-sign unit that closes inscriptions. The sequence `741-060` is the dominant feeder into that cap: every observed `741-060` occurrence is followed by `920`, and every such `920` ends the inscription.

This is a structural formula claim, not a decipherment. The useful reading is: `741-060` is not merely followed by a common terminal sign by chance; it appears to require `920` in this construction.

## Evidence

- Raw occurrences: `31/31` `741-060` rows are followed by `920`.
- Exact text/site/type/symbol collapse (so duplicate copies of one inscription count once): `30/30` cells still follow with `920`.
- Terminality: `31/31` `741-060-920` rows end after `920`.
- Broader cap: `060-920` has `53` raw rows and `52` exact-collapsed cells; it is terminal in `52` raw rows and `51` exact-collapsed cells.
- Feeder pressure: in exact-collapsed `060-920` rows, predecessor `741` contributes `30` cells; the next largest feeders are `742` with `7` and `745` with `3`.
- Site spread: 7 sites: Mohenjo-daro, Harappa, Dholavira, Lothal, Chanhu-daro, Kalibangan, Rakhigarhi.
- Artifact spread: mostly `SEAL:S`, but also `TAB:I`, `TAB:B`, `TAG:P`, and `TAG:R`.
- Against all other bigrams in the same metadata layer, the right-tail Fisher test for selecting `920` gives `p = 1.4692670982228672e-64`.
- In the exact-collapsed all-bigram tournament, `060-920 -> END` ranks `4` by best successor support, `740-390 -> 590` ranks `5`, and `741-060 -> 920` ranks `6`. The difference is interpretive: `740-390` has a complete-looking exception; `741-060` does not.
- In a successor-shuffle null over all bigrams with at least `30` exact cells, no run out of `5,000` produced a `30/30` exact successor formula.

## Why It Is Harder To Dismiss Than A Raw Formula Count

The obvious first objection is copying: maybe one workshop stamped the same text many times. That objection does not explain the current metadata pattern by itself. The exact text/site/type/symbol collapse reduces the set from `31` rows to `30`, not down to a local duplicate family, and the distribution crosses multiple sites and object labels.

The second objection — that this is just a local formula — is also weaker here than for exposed false positives. In the same pass, `752-615-503` looked perfect raw (`29/29`) but collapsed to two exact cells at one Mohenjo-daro `TAB:C` context. `741-060-920` does not have that failure shape.

## Source Status

A row-level visual peek checked six available source images: `C-16`, `H-89`, `K-4`, `L-28`, `M-113`, and `M-247`. The rows are real visible inscriptions and are compatible with the catalogued terminal cluster. This does not independently box `741`, `060`, or `920` — that is, it does not confirm each sign's boundaries on the object.

A blind packet has been built (a set of images with the answers sealed, so a reader must judge without knowing which rows are targets):

- Blind sheet: `tmp/blind_741060920_terminal_cluster_20260531/blind_741060920_terminal_cluster_sheet.jpg`
- Manifest: `data/open_prototype/reports/blind_741060920_terminal_cluster_20260531_manifest.csv`
- Sealed answer key: `data/open_prototype/reports/blind_741060920_terminal_cluster_20260531_answer_key.csv`

A first answer-key-blind sidecar read recovered five of the six `741-060-920` targets as the same terminal cluster at medium-low confidence or better, missed one target, and did not group the single non-`741` `060-920` diagnostic row with the targets. That initially favored the narrower visual formula.

A second blind packet directly tested non-`741` `060-920` rows against `060`-non`920` controls. The reader called all six non-`741` positives cap-like, rejected five of six controls, and marked the remaining control only as a low-confidence possible. This promotes the broader `060-920` cap as a visual candidate, not only a metadata candidate.

## Falsifier

The candidate weakens sharply if blind readers cannot distinguish the `060-920` terminal cap, or if the apparent cap is equally visible in controls without `060-920`. The narrower `741-060` feeder claim is killed in strict form by any clean source-visible `741-060` row not followed by terminal `920`, or by source review showing that the catalogued three-sign segmentation is an artifact.

## Current Bottom Line

`060-920`, with `741-060` as its dominant feeder, is the best current promoted structural candidate under strict exception-free criteria: a portable terminal cap that survives exact duplicate collapse, broad max-stat comparison, and blind visual packet tests. It is not yet an accepted claim, but it is strong enough to put in front of an epigrapher as a specific, falsifiable structural result.
