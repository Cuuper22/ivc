# H-2147 / H-940 `110` Recrop Recheck

Date: 2026-05-26

## What This Note Is

This note asks whether looking harder at the same published pictures helps. A recut, or recrop, means going back to the highest-resolution version of a source page we can obtain and cutting a fresh, tighter image of the object, rather than reusing an earlier low-resolution crop. It is the cheapest possible upgrade: no new source, no new permission, just better pixels.

The branch under test is the proposal that our local sign `110` corresponds to Parpola's sign no. 41 — Parpola's catalog being an external sign-numbering system. Two objects, H-2147 and H-940, are the weak links in that branch, so the question is whether better crops of them settle anything.

## Question

Can public recropping improve H-2147 or H-940 enough to strengthen the local `110` / Parpola sign-no.-41 branch?

## Source Recheck

H-2147 was rechecked against the raw page image embedded in the Kenoyer/Meadow 1997 PDF, not only the earlier rendered page crop.

Stored raw page extraction:

```text
tmp/h940_higher_res_route/pdfimages_h2147_p20/p20img-000.png
sha256: fcc1bc8d7346377d6aa656c824107112ecd5817f83857c680594de3c08c2227c
dimensions: 3419 x 4413
```

New H-2147 item 17 recrops:

```text
tmp/h940_higher_res_route/derived/h2147_fig10_item17_raw_fullrow_recrop.png
tmp/h940_higher_res_route/derived/h2147_fig10_item17_face_raw_recrop.png
tmp/h940_higher_res_route/derived/h2147_fig10_item17_right_component_raw_recrop.png
tmp/h940_higher_res_route/derived/h2147_fig10_item17_left_component_raw_recrop.png
tmp/h940_higher_res_route/derived/h2147_item17_recrop_manifest.csv
```

H-940 was rechecked through the Internet Archive IIIF max image for CISI Pakistan n374.

Stored IIIF max page:

```text
tmp/h940_higher_res_route/cisi_pakistan_n374_max.jpg
sha256: 5dd6ba799bfaa40804d4aad9d3a79ab32db1210b9e4efced808c9699406bfd96
dimensions: 3258 x 4550
```

New H-940 recrops:

```text
tmp/h940_higher_res_route/derived/h940_b_panel_no_label_from_iiif_max.png
tmp/h940_higher_res_route/derived/h940_b_panel_no_label_from_iiif_max_gray_autocontrast.png
tmp/h940_higher_res_route/derived/h940_iiif_max_recrop_manifest.csv
```

Follow-up source route check: the IA JP2 archive member for the same page was also downloaded and cropped. It has the same page geometry as the IIIF max route (`3258 x 4550`) and gives no visible topology upgrade.

```text
tmp/h940_higher_res_route/ia_jp2/cisi_pakistan_0374.jp2
sha256: 352c8a84ad75ebdf36313768132a891aeff6a8c83c5a1ed6a49526ed5f753a36
dimensions: 3258 x 4550

tmp/h940_higher_res_route/derived/h940_b_panel_from_ia_jp2.png
tmp/h940_higher_res_route/derived/h940_b_panel_no_label_from_ia_jp2.png
```

## Result

No upgrade.

H-2147 is weaker than the earlier precheck wording allowed. The raw Figure 10.17 recrop shows that the relevant visible panel has at least a left vertical/U-like component plus a right branching/figure-like component. The visual attraction to H-2148 comes from the right component, not from a clean isolated single-sign panel.

So H-2147 remains object-visible, but its `110` relevance is only component-level pressure until a source-side/sign note maps the visible components to local `673.1 ]110+` or `673.2 ]220-415+`.

H-940 also does not improve. The Internet Archive IIIF max image and the IA JP2 archive member have the same pixel dimensions as the existing page route, and the fresh B-panel crops preserve the low-contrast paired/wavy vertical form problem. H-940 B still does not bind the H-2148 form at current public quality.

## Decision

Accepted:

- H-2147 remains public object-visible through `Figure 10.17 -> H95-2514`.
- H-2147 must be demoted from "candidate single-sign panel" to "candidate component within a multi-component panel."
- H-940 has no better public-resolution witness in the checked IA IIIF or JP2 routes. A witness is one published record of an object; several witnesses of the same object can disagree.
- H-2148 remains the cleanest current source-visible/count-mapped `110` branch witness.

Rejected:

- H-2147 Figure 10.17 as a clean single-sign `110` panel.
- H-2147 right component equals local `110`.
- H-940 rejoins the H-2148/H-2147 branch at current public quality.
- Local `110` equals Parpola sign no. 41.
- Any sign value, phonetic value, language identity, or translation.

## Stored Report

```text
data/open_prototype/reports/h2147_h940_110_recrop_recheck.csv
data/open_prototype/reports/h2147_h940_110_recrop_recheck_summary.json
data/open_prototype/reports/h940_ia_jp2_route_recheck.csv
data/open_prototype/reports/h940_ia_jp2_route_recheck_summary.json
```

## Next Gate

Acquire H-2147 `Figure 27.14` source-side notes and a better H-940 B source panel. If H-2147 stays multi-component and H-940 stays split, this branch becomes H-2148-led only until outside controls or source notes rescue it.
