# H-940 / H-2147 / H-2148 `110` Branch Visual Precheck

Date: 2026-05-26

This note records a quick look at three image crops to see whether they show the same sign. It was run blind: the crops were stripped of their labels and shuffled into a neutral sheet, so the reviewer judged shapes without knowing which object was which. That guards against seeing a match because you expect one.

## Question

After H-2148 became source-visible, do H-2148's single-sign panel, H-940 B, and the H-2147 candidate component/panel crop form one visually coherent graphic class?

## Neutral Packet

The neutral packet is the label-stripped bundle shown to the reviewer, followed by the key that says which crop was which.

Neutral sheet:

- `tmp/h2148_h2100_h2152_110_route/derived/h940_h2147_h2148_110_branch_neutral_precheck_sheet_clean.png`
- SHA256: `01e028a53abe23b419c03e9d72c4a5a38fd8a653f92b42f5ec1002c2dbd41f11`

Unblinding key:

| Neutral ID | Object / source | Crop | SHA256 |
| --- | --- | --- | --- |
| S001 | H-2148, Kenoyer 2005 Figure 14.1 single-sign panel | `tmp/h2148_h2100_h2152_110_route/derived/h2148_fig14_item1_left_single_panel_no_label_crop.png` | `9492438a6578d36a236f8d36e7dbb09f2f106d1b4e5b2c38a18bb155b3f63b7d` |
| S002 | H-940 B source-visible local `+110+` panel, label removed | `tmp/h2148_h2100_h2152_110_route/derived/h940_b_panel_no_label_crop.png` | `48e753346e60d5e063ea129f0376ba498e1703a27b5d8053835e03fe927e2ce4` |
| S003 | H-2147 Figure 10.17 lower candidate component/panel crop | `tmp/h2148_h2100_h2152_110_route/derived/h2147_fig10_item17_lower_candidate_single_panel_crop.png` | `10c8f638e83f4701ec1291819e6dfda8b168a5841964cca845179c34cf6bd4da` |

## Reviewer Result

Decision: split.

- S001 and the right component visible in S003 are a loose visual family candidate.
- S002 is not comparable enough to bind into the same graphic class.

Concrete visual notes:

- S001 has a central vertical body with branching or limb-like strokes to the right and a compact lower crossing.
- S003 also has a vertical-stem/branching-stroke structure, but the later raw-page recrop shows this is a component inside a multi-component panel, with adjacent left vertical/U-like material. Its lower structure is heavier and more open than S001.
- S002 is low-contrast and low-resolution; it shows paired tall V/leaf-like or wavy vertical forms rather than the S001/S003 branching body structure.

Later correction:

- [H-2147 / H-940 `110` recrop recheck](h2147_h940_110_recrop_recheck.md) demotes H-2147 from "candidate single-sign panel" to "candidate component inside a multi-component panel."
- The visual-family statement therefore applies only to the H-2147 right component, not to a clean H-2147 `]110+` side.

## Decision

Accepted:

- H-2148 and the H-2147 right component are a loose source-crop visual-family candidate for the branch.
- H-940 B does not currently visually bind the class at the available crop quality.
- The branch cannot be promoted from `P0 crosswalk hypothesis` to accepted local `110` / Parpola sign-no.-41 mapping.

Rejected:

- A clean three-object visual match across H-940, H-2147, and H-2148.
- Any use of H-940 B as decisive positive support for the H-2148/H-2147 graphic form without higher-resolution imagery.
- Any use of H-2147 as a clean single-sign `110` panel without source-side/sign notes.
- Any sign value, phonetic value, language identity, or translation.

## Next Gate

1. Acquire a higher-resolution or source-original H-940 B panel.
2. Acquire H-2147 source-side labels and higher-resolution panels.
3. If H-940 B remains graphically split at better quality, test whether the Parpola branch is mixing two forms, whether local `110` is over-normalized, or whether one of the source/local side mappings is wrong.
