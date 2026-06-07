# Dholavira `4237.1` source-route recheck for `002-390-X`

Date: 2026-05-31 America/Los_Angeles

Status: active source/sign gate, not goal completion.

## Target

`4237.1` is one of the two local `705` branch witnesses inside `002-390-X`:

- Local row: `4237.1`
- Object field: `-`
- Site/type: Dholavira `SEAL:S`
- Local locus: Lower Town, `ZA-12:2-`
- Period: `5`
- Class: `SC`
- Dimensions: `27.62 x 21.31(ext) x 7.11-11.17(ext)`, normalized as `27.6 x 0 x 7.1 - 11.2`
- Local text: `+151-032-388-002-390-705+`
- Structural role: `388 -> 002-390 -> 705 -> <END>`

The question is whether this row can be source-bound strongly enough to count as a strict repeated non-`125` terminal branch.

## What Survived

The Dholavira route is not cold. It now has two separate pieces of pressure:

- A visual page-18 image/crop that looks compatible with a reverse `R/L` reading in the neighborhood of `+151-032-388-002-390-705+`.
- An OCR metadata cluster in the Bisht mirror that exposes `ZA-12:2`, `8758`, and the exact `27.62 x 21.31 x 7.11-11.17` dimension cluster matching the local row.

Those are worth keeping. They just cannot be fused.

## What Failed

The page-18 image candidate is not bound to `4237.1`.

The individual-seal details in the public OCR mirror list item `10` as Acc. No. `2118` with an inscription of 5 signs. Local `4237.1` has 6 signs and a different locus/dimension profile. That means page-18 item 10 is best treated as a visual lookalike or wrong-object route, not as strict `705` evidence.

The `8758` route is also incomplete. The OCR mirror exposes an `8758 / ZA-12:2 / 27.62 x 21.31 x 7.11-11.17` cluster, and separately an individual detail for Acc. No. `8758` with a unicorn description. But this is still text/OCR. It does not bind the visible page-18 crop to Acc. No. `8758`, and it does not independently show the six-sign sequence from a source image.

## Guard

Do not use `ICIT 4348 (Dholavira)` as a bridge. Local `4348.1` is a different Dholavira row:

- Type: `TAG`
- Text: `]740-142-000-002-861-390[`

It is a separate Dholavira clue, not evidence for `4237.1` or `002-390-705`.

## Decision

Current status:

`dholavira_8758_cluster_unbound_image_conflict`

Use Dholavira `4237.1` as:

- Yes: acquisition-hot repeated `705` target.
- Yes: metadata cluster pressure from `ZA-12:2 / 8758 / 27.62...`.
- Yes: visual-lookalike pressure from page 18 item 10.
- No: strict source-image evidence.
- No: bound token-box evidence for `705`.
- No: sign value, phonetics, function, language identity, meaning, or translation.

## Consequence for `002-390-X`

The `705` branch still has two local terminal rows:

- `M-1825`: source-dark or weak.
- `4237.1`: Dholavira OCR cluster plus lookalike image pressure, not strict.

So `705` remains the most important repeated non-`125` acquisition target, but it still contributes zero strict source-normalized counts. The positive model cannot use it as source-bound repetition yet; the adversarial model cannot erase it either, because the metadata cluster is no longer cold.

Next gate: bind Acc. No. `8758` or `ZA-12:2` to an actual image/caption of the six-sign seal, or route `M-1825` as the other `002-390-705` witness.
