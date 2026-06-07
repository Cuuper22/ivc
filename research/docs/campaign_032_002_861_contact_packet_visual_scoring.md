# 032-002-861 Contact Packet Visual Scoring

Date: 2026-05-29

## Question

When the source/contact packet is read visually, do the post-`861` tails look like attached terminal material, second units, register/workshop addenda, or bare closure controls?

## Input

- Contact sheet: `tmp/032_002_861_source_normalized_tail_predictor_packet/campaign_032_002_861_source_normalized_tail_predictor_contact_sheet.png`
- Score table: `data/open_prototype/reports/campaign_032_002_861_contact_packet_visual_scores.csv`
- Parent packet: `docs/campaign_032_002_861_source_normalized_tail_predictor_packet.md`

## Visual Decisions

- `603`: survives as a recurrent post-`861` tail class on the Mohenjo side. `M-1273` is the cleanest witness; `M-240` supports the class but is blurrier; `M-714` is same-line but crowded and downweighted for fine-form identity. This is not a value and does not revive the Harappa bridge.
- `533-717`: survives as a fixed restricted-tail candidate. `M-376` and `M-391` both preserve same-line terminal-side material, but the pair remains one narrow final-unit candidate, not a solved compound or morphology.
- `255-416`: remains a singleton minimal-contrast member. `M-91` is same-line enough to keep the contrast alive, but cannot support a repeated class by itself.
- `360-520-919-140`: becomes the strongest visual adversary to an easy `533-717` register reading. `M-355` is visibly in the same no-icon cuboid-convex `SEAL:R` lane but carries a long continuation instead of `533-717`.
- Bare controls: `H-444`, `M-723`, `M-1044`, `M-77`, `M-118`, `M-15`, and `M-1267` preserve terminal-edge behavior with no post-edge material in the checked windows. They support closure-background contrast, not values.
- Harappa external controls: `H-1138`, `H-1846`, and `H-360` are source-visible as object/band evidence, but not source-tokenized enough to accept X-slot identities or graphic identity with Mohenjo `603`.

## Decision

Status: `visual_scoring_supports_tail_classes_not_readings`.

The visual pass supports a typed post-`861` secondary zone:

- bare closure background;
- recurrent simple tail class (`603`);
- fixed restricted final unit (`533-717`);
- singleton contrast (`255-416`);
- long continuation/second-unit adversary (`360-520-919-140`).

It does not support phonetics, language identity, translations, exact sign values, or exact source-normalized `861|tail` token boundaries. The next promotion gate is not another metadata count: it is blind/semi-blind scoring of layout and copy-family similarity for `M-376/M-391` against `M-355/M-1267/M-1273` and the bare controls.
