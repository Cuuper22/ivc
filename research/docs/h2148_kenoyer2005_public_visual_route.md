# H-2148 / H2001-5142 Kenoyer 2005 Public Visual Route

Date: 2026-05-26

## Question

Can H-2148 move from route-dark metadata into source-visible evidence for the `110` / Parpola sign-no.-41 branch?

## Result

Yes, at object and count-level side mapping. H-2148 is no longer route-dark.

Kenoyer 2005 Figure 14.1 publicly shows accession `H2001-5142`, the local hook behind H-2148. The figure table identifies it as:

- Figure item: `14.1`
- Accession: `H2001-5142`
- Lot: `11759-01`
- Artifact type: tablet, incised
- Material: fired steatite
- Shape: flat rectangular
- Context: foundation rubble

The visible source item has one single-sign panel and one three-sign panel. The local rows are exactly one single-token side and one three-token side:

- `481.2 +110+`
- `481.1 +520-220-415+`

This supports a count-level panel-to-local-row assignment:

| Source panel | Visual count | Local row assignment | Status |
| --- | --- | --- | --- |
| Figure 14.1 left panel | one sign | `481.2 +110+` | accepted as count-level row mapping |
| Figure 14.1 right panel | three signs | `481.1 +520-220-415+` | accepted as count-level row mapping |

This is stronger than H-2147 because H-2148 is complete/good in the local metadata and the source figure visibly separates the one-sign and three-sign faces.

## Source Route

Source PDF:

- Kenoyer, J. Mark. 2005. "Excavations at Harappa 2000-2001: New Insights on Chronology and City Organization"
- Public Harappa URL: `https://www.harappa.com/sites/default/files/pdf/Kenoyer2005_Excavations%20at%20Harappa%202000-2001%20New%20insights%20on.pdf`
- Local PDF: `tmp/h2148_h2100_h2152_110_route/kenoyer2005_harappa_2000_2001.pdf`
- PDF SHA256: `8539a3cba8667dc6fbd1ec77170c16d84f644dbc6854537742edcc9060cdf44f`

Rendered source page:

- Local page image: `tmp/h2148_h2100_h2152_110_route/kenoyer2005_page-17.png`
- Page image SHA256: `efe84d782e1ed3d4e464db86d3ae3a5b01294d64e34ba1d46e1324c8ee6792fd`
- Printed page visible on scan: `223`

Stored crops:

| Artifact | Path | SHA256 |
| --- | --- | --- |
| Figure 14 full crop | `tmp/h2148_h2100_h2152_110_route/derived/h2148_kenoyer2005_fig14_full_crop.png` | `56a697f990b14dcaf8f56e3fc772342aefd6bd13bec66bccc57d4691c4782dfa` |
| Figure 14 item 1 full row | `tmp/h2148_h2100_h2152_110_route/derived/h2148_kenoyer2005_fig14_item1_fullrow_recrop.png` | `b36a70f2c0e040cbcd6beb51a59409165e1d32437fa833fa042d6c01f817b5ae` |
| Left single-sign panel | `tmp/h2148_h2100_h2152_110_route/derived/h2148_kenoyer2005_fig14_item1_left_single_panel_crop.png` | `16aaea890c19c5f78cc0b332785000417ad329fc4e9d2dbaa9cff0d2a5cb9304` |
| Right three-sign panel | `tmp/h2148_h2100_h2152_110_route/derived/h2148_kenoyer2005_fig14_item1_right_three_sign_panel_strict_crop3.png` | `a6493f24869d5e082c2ae1790ec39df3953ce9460015f28a2a3e922d49b671be` |
| Figure 14 caption/table crop | `tmp/h2148_h2100_h2152_110_route/derived/h2148_kenoyer2005_fig14_caption_table_crop.png` | `49ea644b777a16787d86704938c4e3e74a57ba0396b176eab34a1408edf2be3c` |
| Figure 14.1 table row crop | `tmp/h2148_h2100_h2152_110_route/derived/h2148_kenoyer2005_fig14_table_row_14_1_recrop2.png` | `e8579a8596616a5f17e119c458255fad34904d57a0eb56b7bf0bb4dc3616eeb6` |

## What This Changes

H-2148 upgrades from `route_dark_exact_415_plus_110_candidate` to `public_visual_route_count_mapped`.

It becomes the cleanest source-visible member of the H-940/H-2147/H-2148 Parpola sign-no.-41 branch:

- H-940: source-visible `+110+` panel, but old publication/source-label route.
- H-2147: public object route, but fragmentary and row-to-panel mapping remains weaker.
- H-2148: public object route, complete/good local row, visible one-sign and three-sign faces matching the local row counts.

## What It Does Not Change

Not accepted:

- `local 110 = Parpola sign no. 41`.
- Any phonetic value, meaning, language identification, or translation.
- Any proof that the visible single sign is Parpola sign no. 41 rather than only the local-catalog `110` side.
- Any side-letter mapping, because Figure 14.1 does not label the faces as A/B or obverse/reverse.
- Any claim about H-2100, H-2152, or Kanmer `4881.1`, which remain outside controls pending route checks.

## Next Gate

1. Compare the H-2148 left single-sign panel against H-940 B and H-2147's right candidate component only after better H-940/H-2147 source quality or source-side notes are available.
2. Acquire source/sign-list notes showing whether Parpola sign no. 41 corresponds to the same visible single-sign form.
3. Route-check H-2100, H-2152, and Kanmer `4881.1` so the outside `110` controls are not ignored.
4. Ask for higher-resolution H-2148 panels if the public scan is too low-resolution for diagnostic stroke decisions.
