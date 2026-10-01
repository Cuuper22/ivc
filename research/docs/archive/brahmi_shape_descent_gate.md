# Brahmi Shape-Descent Gate

Date: 2026-05-29

This note records the first direct attempt at the descendant-script back door. The idea: if Brahmi descended from the Indus script, an Indus sign shape might survive into an early Brahmi glyph whose phonetic value we know. So we compare actual local Indus source/canonical shape probes against early Brahmi glyphs, and then try to kill every visual match with a random shape-evolution null.

The expanded source-token gate is recorded separately in `docs/brahmi_source_token_descent_gate_v2.md`. It scales this attempt from 457 early Brahmi glyphs and four actual source probes to 1,342 early Brahmi glyphs and 611 source-token features; it also yields zero candidate-only rows and zero accepted anchors.

It produces no accepted descent line and no phonetic value.

## Source Surface

Indoskript was used as the Brahmi-side source:

- Homepage: `https://www.indoskript.phil.uni-wuerzburg.de/`
- Manuscript index: `https://www.indoskript.phil.uni-wuerzburg.de/manuscripts`
- Letter table route: `https://www.indoskript.phil.uni-wuerzburg.de/letters/table/<manuscript_id>`

The scraper parsed all 42 manuscript-index pages, found 399 manuscript rows, and selected the first 12 early manuscripts at date <= -100 for the first controlled run. Those 12 tables yielded 457 Brahmi glyph rows and 457 usable glyph features. This is intentionally a bounded first gate, not a complete Brahmi corpus.

## Indus Probes

The Indus side used 14 local probes:

- Actual local `220` source crops: `S009/M-37`, `S010/H-938`, `S011/H-940`.
- Blocked/stress local `220` crop: `S012/H-942`.
- Parpola 1994 fish-family controls: signs 57, 58, 59, 60, 66, and 70 variants.
- Actual local `110` source crop: `H-2148`.
- Parpola 1994 sign 41 canonical crop.

Keep in mind the actual source probes are not clean vector glyphs. They are seal/source-photo crops, so the mask extraction uses background-adaptive thresholding rather than treating gray background as ink.

## Forger / Null

For each actual Indus source probe, the forger generated 500 random shape-evolution variants by applying affine rotation, scale changes, threshold changes, dilation, and erosion. Each evolved shape was sent through the same nearest-Brahmi retrieval as the real source probe.

A proposed descent line must clear both gates:

1. Family consistency: independent source probes for the same local sign converge on the same Brahmi value.
2. Shape null: random evolved shapes should rarely match Brahmi as well as the observed source probe.

## Results

| Probe | Top Brahmi neighbor | Observed distance | Null <= observed share | Decision |
| --- | --- | ---: | ---: | --- |
| `M-37` local `220` | `kaṃ` | 0.345068 | 0.576000 | failed |
| `H-938` local `220` | `o` | 0.525419 | 0.438000 | failed |
| `H-940` local `220` | `ka` | 0.476909 | 0.656000 | failed |
| `H-2148` local `110` | `a` | 0.470080 | 0.666000 | failed |

The earlier tempting behavior vanished once the source-photo masking was repaired. Under the corrected mask, local `220` does not converge on one Brahmi value, and random shape evolutions equal or beat the observed nearest distances too often to trust any single match.

## Decision

No morphological descent line survives. No Brahmi-derived phonetic value is accepted.

Useful residue:

- The Indoskript acquisition route now exists and is provenance logged.
- The local `220` and `110` probes now have a repeatable nearest-neighbor plus null harness.
- The next real swing should use hand-verified, token-isolated source crops or full segmentation rather than broad source-photo component crops.
