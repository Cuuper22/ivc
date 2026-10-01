# 032-002-861 603 H-1138/H-360 Tokenization Gate

Date: 2026-05-29

This note runs the test the previous packet asked for, and the test fails to deliver. The claim under examination is that the sign the catalogue calls `603` on a Harappa tablet is the same carved shape as the sign it calls `603` at the end of a Mohenjo-daro seal. To check that, we have to know which mark on the Harappa photograph is `603` — which means tokenizing the band, cutting the inscription strip into individual signs. The public image is not good enough to do that cleanly, and neither candidate slot matches. The bridge is not killed, but it is weakened.

## Question

Can the source-visible Harappa bands — the strips of the object carrying the inscription — be tokenized enough to test whether `H-1138` catalog `603` matches the clean post-`861` `M-1273` terminal, while `H-360` catalog `636` stays visually different?

This is a candidate tokenization gate; a "gate" is a check that must pass before evidence enters the analysis. It does not accept a source-derived sign value or translation.

## Artifacts

- Candidate slot sheet: `tmp\032_002_861_603_h1138_h360_tokenization_gate\h1138_h360_candidate_slots_annotated_sheet.png`
- Candidate crop sheet: `tmp\032_002_861_603_h1138_h360_tokenization_gate\h1138_h360_m1273_candidate_crop_sheet.png`
- Manifest: `data\open_prototype\reports\campaign_032_002_861_603_h1138_h360_tokenization_gate_manifest.csv`

## Orientation Alternatives

Which visual position holds which catalogue sign depends on reading direction, and that is not settled. Both source rows are locally recorded as `R/L`, meaning right to left. Therefore two policies are kept explicit and every result is reported under both:

1. `visual_ltr_equals_catalog_order`: leftmost visual slot maps to the first catalog token.
2. `recorded_RL_means_visual_rightmost_catalog_first`: rightmost visual slot maps to the first catalog token.

Candidate X slots under these policies:

- `H-1138` / `603` under visual-LTR: ['visual_slot_2']
- `H-1138` / `603` under recorded-R/L: ['visual_slot_4']
- `H-360` / `636` under visual-LTR: ['visual_slot_2']
- `H-360` / `636` under recorded-R/L: ['visual_slot_4']

## Immediate Visual Read

Under the recorded-R/L policy, the candidate Harappa `603` in `H-1138` falls in visual slot 4, while the `H-360` `636` control falls in visual slot 4. Both are visibly different from the clean ladder/window-like `M-1273` terminal anchor in the current crop sheet. Under the visual-LTR policy, the candidate X slots fall in visual slot 2, which also does not cleanly match `M-1273`.

The key point is not that the bridge is disproven. The key point is that this public Vats crop quality and approximate slotting do not deliver the positive upgrade. The current source-tokenization gate does not prove `M-1273 terminal sign = H-1138 source-tokenized 603`.

## Decision

```text
h1138_h360_source_tokenization = candidate_only
m1273_equals_h1138_603 = not_demonstrated
h360_636_distinct_from_m1273 = plausible_but_candidate_only
cross_context_603_graphic_identity = unresolved_negative_leaning
```

## Researcher Review

Source-critical verdict:

- The positive test fails to upgrade. `M-1273` remains a clean ladder/window-like post-`861` terminal anchor, but neither candidate `H-1138` X-slot cleanly matches it under the current public crop.
- The packet does not overstate the boxes: it keeps them as candidate visual slots and preserves both orientation policies.

Linguistic update:

- The distributional bridge is unchanged: `603` still bridges the Harappa X-before-`240` class and post-`002-861` terminal position while `636/642` do not.
- The graphic bridge is weakened: candidate `H-1138` X under both orientation policies fails to confirm the `M-1273` match.
- Split-homograph/catalog-conflation — the possibility that two different carved shapes share one catalogue number — and Harappa tablet-template explanations are now promoted as live competitors.

Allowed hostile claim:

```text
603 is a distributional bridge with unresolved/negative-leaning graphic identity.
```

Not allowed:

- No final graphic kill.
- No value, phonetics, language identity, or translation.
- No accepted Harappa-to-Mohenjo graphic identity.

Reason: `H-1138` boxes are approximate, the far-left edge is clipped, orientation is not source-settled, public Vats quality is weak, and `H-1846` is still not layout-ready.

## Next Test

The bridge needs a better source image or a label-bearing source transcription for `H-1138/H-1846`. Without that, `603` remains a distributional bridge and a post-`861` terminal candidate, not a source-proven Harappa-to-Mohenjo graphic identity.

Accepted values/translations remain 0.
