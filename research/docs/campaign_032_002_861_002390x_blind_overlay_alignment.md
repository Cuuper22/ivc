# 032-002-861 / 002-390-X Blind Overlay Alignment

Date: 2026-05-30

## Question

After blind readers segmented the alpha panels without labels, which sealed-key windows survive when compared to the neutral overlays?

## Materials

- Blind read decision: `C:\Users\Acer\OneDrive\Documents\ivc\docs\campaign_032_002_861_002390x_alpha_blind_boundary_read.md`
- Reader consensus: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\reports\campaign_032_002_861_002390x_alpha_blind_reader_consensus.csv`
- Sealed key: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\reports\blind_boundary_packet_alpha_sealed_key.csv`
- Neutral overlays: `C:\Users\Acer\OneDrive\Documents\ivc\tmp\blind_boundary_packet_alpha\neutral_overlay_key`
- Machine-readable verdicts: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\reports\campaign_032_002_861_002390x_blind_overlay_alignment.csv`

## Alignment Verdicts

| neutral | object | branch | blind state | overlay alignment | decision |
|---|---|---:|---|---|---|
| ALPHA | M-119 | 125 | partial | Blind readers recover the vertical-bar group and later fork/comb/peaked neighborhoods, but the proposed `002-390-125` window does not emerge cleanly as a three-token sequence without overlay help. | keep as partial target only |
| ECHO | M-735 | 125 | partial | Readers see a fan/comb, peaked frame, vertical-pair, branching cluster, and sweeping terminal curve. The overlay window can be made compatible, but it is not blind-stable because dense overlap and the off-frame curve shift likely token boundaries. | keep as partial target only |
| BRAVO | M-71 | 095 | partial | Readers see paired uprights, a fork/trident, angular/roof cluster, and a cropped sweep. The non-125 branch window remains plausible, but the rightmost branch shape is partly cropped and not cleanly separated. | keep as partial control |
| DELTA | M-70 | 692 | partial | Readers independently identify the vertical-bar field and fork/trident neighborhood; this is one of the clearer internal-boundary controls, but the right angular terminal area is cropped/tangled. | keep as partial control |
| CHARLIE | Sktd-1 | 125 | partial leaning reject | Readers mark the panel as unstable or rejectable. The sealed-key window depends too much on overlay/corpus expectation. | demote from strict counts |

Independent blind-over-key comparison ranks the witnesses as:

1. `DELTA/M-70/692`: strongest partial non-`125` control.
2. `ALPHA/M-119/125`: strongest partial target.
3. `BRAVO/M-71/095`: partial non-`125` control.
4. `ECHO/M-735/125`: weak partial target.
5. `CHARLIE/Sktd-1/125`: demoted.

## Decision

No witness reaches the `blind_source_window_preserved` threshold.

The correct state is:

`catalog-guided boxed windows remain plausible; blind overlay alignment is partial; source-window proof is not achieved`.

This keeps the `002-390-X` branch ecology alive as a positional research object but blocks promotion of `125` as a visually source-proven branch member. The non-`125` controls are in the same partial visual class, so the next decisive evidence must come from source-bound matched alternatives, especially `H-1993` and `705`.

## Linguistic Consequence

The branch hypothesis now rests on a two-layer distinction:

1. Positional ecology: `125`, `095`, `692`, and `705` remain the active branch alternatives after `002-390`.
2. Visual proof: none of the current alpha witnesses independently proves the immediate local numeric window from source image alone.

This is still a language question: does `002-390` license a branch-choice slot whose next sign conditions closure versus continuation, or are the apparent branches just formula/register/copy-family residues? The blind result removes the easy visual shortcut and forces the next campaign onto matched alternatives, especially the repeated non-`125` `705` branch and the `004 -> 002-390 -> 095/125` split.

Accepted: a live positional branch-choice question.

Rejected: source-window proof, `125` function, sign value, phonetic reading, language identity, sign meaning, and translation.
