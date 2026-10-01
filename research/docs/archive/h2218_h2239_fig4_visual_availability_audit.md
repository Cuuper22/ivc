# H-2218 Through H-2239 Fig. 4 Visual Availability Audit

Date: 2026-05-24

## Purpose

This note records what the publicly available Fig. 4 image in Meadow and Kenoyer 2000 can and cannot support for the H-2218 through H-2239 tablet series. It exists so later steps do not treat a coarse published figure as if it were high-resolution evidence.

This is an academic source audit — a check of what a source can show. It is not OCR (machine text extraction), not image redistribution, and not a reading of any sign.

## Local Artifacts

```text
data/open_prototype/tools/lipi_h2218_fig4_visual_availability_audit.mjs
data/open_prototype/reports/lipi_h2218_h2239_fig4_visual_availability.csv
data/open_prototype/reports/lipi_h2218_h2239_fig4_visual_availability_summary.json
```

Inputs:

```text
data/open_prototype/reports/lipi_h2218_h2239_fig4_mapping.csv
data/open_prototype/reports/h2218_h2239_public_image_lead_search_summary.json
```

External source:

```text
Meadow and Kenoyer 2000, The 'Tiny Steatite Seals' (Incised Steatite Tablets) of Harappa
https://www.harappa.com/sites/default/files/pdf/Kenoyer2000_The%20Tiny%20Steatite%20Seals%20of%20Harappa.pdf
```

## Visual Check

The public PDF could not be downloaded through the local shell during this check; the request returned `403 Forbidden`. The PDF was inspected through the web viewer instead, without storing the PDF or figure image in the repository.

Web viewer page checked:

```text
page_14_inspected_in_web_viewer
```

Observed:

- Fig. 4 shows seal no. 1 plus tablet nos. 2-23.
- All 22 tablet items mapped from the local H-2218 through H-2239 sheet are present in the public figure.
- Each tablet item appears as three side panels.
- A triangular/end-profile marker appears to the right of the tablet side panels.
- The figure is coarse and not segmentation-grade — not sharp enough to split the inscriptions into individual signs.

## Coverage

```text
source_rows: 22
expected_fig4_tablet_items: 22
visible_three_side_panel_rows: 22
visible_end_profile_marker_rows: 22
rows_with_object_level_public_image_leads: 1
rows_without_object_level_public_image_leads: 21
object_level_public_image_lead_objects: H-2219
```

## What This Adds

The earlier Fig. 4 mapping established that all 22 local rows can be linked to Meadow and Kenoyer 2000 Fig. 4 item numbers and manufacturing groups. This audit adds a narrower visual-availability layer:

- Fig. 4 public coverage exists for all 22 tablet items.
- Coarse side-panel presence can be recorded for all 22.
- Coarse end-profile marker presence can be recorded for all 22.
- Object-level public A/B/C side-image leads remain available only for H-2219 in the checked RSS/blog pages.

## What It Does Not Add

The public Fig. 4 image does not support accepting:

- Sign segmentation.
- Allography (which shapes count as variants of the same sign).
- Stroke counts.
- Side orientation.
- Physical side function.
- Numerical value.
- Metrological reading.
- Commodity reading.
- Administrative reading.
- Sign meaning.
- Phonetic value.
- Language identity.
- Translation.

## Consequence

The H-2218 through H-2239 source request should now separate two image needs:

1. A higher-resolution Fig. 4 or source plate for all 22 tablets, because public Fig. 4 only gives coarse coverage.
2. Object-level side images for H-2218 and H-2220 through H-2239, because checked public A/B/C image leads exist only for H-2219.

The project can use this audit as a source-availability checkpoint. It cannot use it as image-level validation.

Follow-ups:

- [H-2218 through H-2239 Fig. 4 mapping](h2218_h2239_fig4_mapping.md)
- [H-2218 through H-2239 dimension side-order probe](h2218_h2239_dimension_side_order_probe.md)
- [H-2219 public image lead audit](h2219_public_image_lead_audit.md)
- [H-2218 through H-2239 public image-lead search](h2218_h2239_public_image_lead_search.md)
