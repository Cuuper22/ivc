# 032-002-861 / 220-032 Terminal-Space Recut

Date: 2026-05-29

## Question

Do the source-visible bare `220-032-002-861` controls have a tail-sized empty terminal slot, or is terminal space a serious layout explanation for why they are bare?

## Packet

- Tailed rows measured: `2`
- Bare controls measured: `3`
- Comparison sheet: `C:\Users\Acer\OneDrive\Documents\ivc\tmp\032_002_861_220032_terminal_space_recut\campaign_032_002_861_220032_terminal_space_recut_comparison_sheet.png`

## Decisions

- `tail_window_vs_bare_margin_width`: `terminal_space_attack_survives`. smallest tailed terminal candidate width is 120px; largest bare post-terminal margin is 38px Limit: the margin boxes come from the existing bare-edge source-control overlay, not a fresh source resegmentation.
- `tail_window_vs_bare_margin_share`: `terminal_space_attack_survives`. smallest tailed terminal candidate share is 0.286; largest bare post-terminal margin share is 0.063 Limit: share compares annotated windows, not automated glyph segmentation.
- `bare_controls_have_tail_sized_empty_slot`: `no_in_current_boxes`. all three bare controls have post-terminal margin width far below both tailed terminal windows Limit: this does not prove the margin is linguistically meaningful; it blocks grammar promotion until recut/source segmentation confirms the edge.
- `grammar_slot_promotion`: `blocked_by_terminal_space_adversary`. broad register and length failed, but terminal-space now has positive support as a layout explanation Limit: the post-861 split remains a source-visible positional contrast, not a grammatical function or value.

## Metrics

- `M-91` `255 416`: line `450px`, tail window `195px`, share `0.433`, edge gap `0px`.
- `M-240` `603`: line `420px`, tail window `120px`, share `0.286`, edge gap `0px`.
- `H-444` bare: line `700px`, post-terminal margin `28px`, share `0.04`, bare terminal window `270px`.
- `M-723` bare: line `925px`, post-terminal margin `38px`, share `0.041`, bare terminal window `315px`.
- `M-1044` bare: line `600px`, post-terminal margin `38px`, share `0.063`, bare terminal window `280px`.

## Result

The terminal-space adversary is now positive, not merely pending. In the current box layer, the tailed rows have terminal candidate windows of `195px` (`M-91`) and `120px` (`M-240`), while the source-visible bare controls have only `28-38px` of marked post-terminal margin.

That does not erase the `220-032` contrast. It changes its status: the split still survives broad register and length attacks, but it cannot be promoted to grammar-slot evidence until a fresh source recut shows that the bare controls had comparable terminal space and still chose closure.

Current status: `terminal_space_adversary_blocks_220032_grammar_promotion`.

Accepted sign values, phonetics, language identity, translations, exact source-token boundaries, and sign meanings remain 0/unaccepted.
