# 032-002-861 / 220-032 Source-Visible Contrast Packet

Date: 2026-05-29

## Question

When `220-032` immediately precedes `002-861`, does the post-`861` outcome behave like a real tail-choice contrast rather than a register artifact or a single-row accident?

## Packet

- Rows with `prefix_last2=220 032`: `7`
- Source-ready rows: `5`
- Display-image rows in blind sheet: `5`
- Tail distribution: `<END>:5;255 416:1;603:1`
- Source-ready tail distribution: `<END>:3;255 416:1;603:1`
- Blind sheet: `C:\Users\Acer\OneDrive\Documents\ivc\tmp\032_002_861_220032_source_visible_contrast_packet\campaign_032_002_861_220032_source_visible_contrast_packet_blind_sheet.png`
- Blind key: `C:\Users\Acer\OneDrive\Documents\ivc\data\open_prototype\reports\campaign_032_002_861_220032_source_visible_contrast_packet_blind_key.csv`

## Pre-Review Decision

- This is the best current source-visible minimal-contrast packet in the post-`861` field.
- It already blocks a binary reading of `220-032-002-861` as simply terminal or simply selecting `603`: the same last-two preframe reaches bare closure, `603`, and `255-416`.
- The packet is not allowed to produce sign values. It can only score visible behavior: closure, simple tail, compound tail, same-line continuity, and whether the source images actually support the catalog split.

## Human Visual Score

The sheet is semi-blind, not fully blind, because the existing overlay captions leak object/tail labels. It still supports the layout question.

- `B0B5F50 / M-1044 / <END>`: bare closure, medium confidence. Blurred, but the checked terminal-side window has no visible post-`861` addendum.
- `B1730A3 / M-91 / 255-416`: tailed continuation, high confidence. Same-line terminal-side material is visible as a longer compound tail.
- `BC6B344 / M-240 / 603`: tailed continuation, medium confidence. A single terminal-side post-`861` unit is visible; blur limits fine-form confidence.
- `BE2B253 / M-723 / <END>`: bare closure, medium confidence. Terminal-side signband is visible with no separate post-`861` material in the checked overlay.
- `BF77F3D / H-444 / <END>`: bare closure, high confidence. Cleanest bare `220-032` control in this packet.

## Result

The `220-032` split survives visual inspection as a source-visible positional contrast: the same immediate preframe reaches bare closure, a simple one-unit tail, and a longer compound tail. This is now the best post-`861` research object because it is a cluster-level language question, not a single-sign defense.

The result does not assign values to `603`, `255`, `416`, `861`, `220`, or `032`. It also does not prove source-derived token boundaries. It only says the source images support a real closure-vs-tail-vs-compound-tail contrast worth modeling.

Next linguistic gate: test whether line length, icon/register, and available terminal space explain the split as well as the post-`861` tail classes. If they do not, the object becomes a candidate grammar slot after `861`; if they do, it stays layout/register behavior.

Accepted sign values, phonetics, language identity, translations, exact source-token boundaries, and sign meanings remain 0/unaccepted.
