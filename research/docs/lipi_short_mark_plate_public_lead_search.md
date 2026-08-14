# Lipi Short-Mark Plate Public Lead Search

Date: 2026-05-24

## Purpose

This note records a search of public web sources for leads on 17 specific artifacts. It exists because the [Lipi short-mark plate request packet](lipi_short_mark_plate_request_packet.md) named 17 artifacts that need image or plate validation, and the cheapest first step is to check what is already public before requesting archive access.

Question:

```text
Are there public source, image, or bibliographic leads for the 17 first-pass plate-check artifacts?
```

This is source discovery only. It is not image validation: finding a page that mentions an artifact is not the same as confirming what is on the artifact.

## Local Artifacts

```text
data/open_prototype/tools/lipi_short_mark_plate_public_lead_search.mjs
data/open_prototype/reports/lipi_short_mark_plate_public_leads.csv
data/open_prototype/reports/lipi_short_mark_plate_public_lead_pages.csv
data/open_prototype/reports/lipi_short_mark_plate_public_lead_summary.json
```

Input:

```text
data/open_prototype/reports/lipi_short_mark_plate_request_packet.csv
```

## Sources Checked

The script checked 20 public endpoints:

```text
3 fixed source pages
17 Blogger Atom searches, one per packet artifact
```

Fixed pages:

```text
https://indusscriptmore.blogspot.com/2012/
https://www.nature.com/articles/s41599-021-00713-0
https://bharatkalyan97.blogspot.com/2025/08/shapes-of-tablets-convey-information.html
```

A caution about these sources. The Blogger and RSS-derived pages are claim-heavy: they assert readings and decipherments. We use them only to discover public leads — pointers to images or citations. Their readings and decipherment claims remain quarantined, meaning we do not use or trust them.

## Results

```text
packet_artifacts: 17
source_pages_checked: 20
fixed_source_pages_checked: 3
blogger_atom_queries_checked: 17
lead_rows: 31
```

Candidate image/post leads:

```text
H-233
H-1302
H-1303
```

Published direction or corpus-note leads:

```text
H-1302
H-1303
```

Text-only or bibliographic leads:

```text
H-233
H-309
H-316
H-353
H-355
H-357
H-933
H-935
H-960
H-978
```

No public lead found in the checked sources:

```text
H-1304
H-1344
H-1345
H-1346
H-1347
```

## Lead Classes

These are the labels used in the results above. Each one is deliberately weak — it says a lead exists, not that the lead is usable evidence.

`artifact_mention_with_candidate_images` means the target artifact is named on a public page or feed entry that also exposes images. It does not mean the image is a plate-grade object-side image.

`published_direction_or_corpus_note` means a published source mentions the artifact in a direction, allograph, or corpus-correction context. For this pass, that applies only to H-1302 and H-1303.

`text_only_or_bibliographic_lead` means the artifact appears in public secondary text, including range/list notation, without usable object-side imagery.

## Consequence

The plain outcome: the public search did not validate any of the 17 packet artifacts.

It did improve source targeting:

- H-233 has a claim-heavy public post with image leads, but a follow-on visual audit narrowed them to one H-233-relevant slide and one off-target H-1997 slide captured by the page-level image sweep.
- H-1302 and H-1303 have a published direction/corpus-note lead and claim-heavy copied image/post leads. A follow-on recheck confirms the Nature 2021 lead but finds the public images are not enough to bind exact object sides or fill packet fields.
- H-355 has only a text-range public lead covering `H-352-357 (incised)`. A follow-on clarification audit found no H-355 object-level public image in the checked searches, so both `+700-033+` short rows still require a three-side source check.
- H-933 and H-960 have only a text-range public lead covering `H-933, 936, 960, 964, 308, and 312-314 (incised)`. A follow-on contrast audit found no object-level public image for either object, so the `034` before-longer contrast remains wholly pending source-image validation.
- Ten artifacts have text-only or bibliographic leads in public secondary text.
- Five artifacts remain source-dark — no public trace at all — in the checked public endpoints. A follow-on direct-request audit rechecked H-1304, H-1344, H-1345, H-1346, and H-1347 with fresh public-web searches and still found no object-level image, plate, caption, or useful text-only lead, so this batch should go straight to CISI/HARP/archive access.

The plate request still needs CISI plates (the published Corpus of Indus Seals and Inscriptions), HARP/Harappa source images, or direct archive access before accepting side order, segmentation, allography, direction, or the `033`/`034` contrast.

Follow-on queue:

- [Lipi short-mark source acquisition queue](lipi_short_mark_source_acquisition_queue.md)
- [H-233 public slide visual lead audit](h233_public_slide_visual_lead_audit.md)
- [H-1302/H-1303 direction-note recheck](h1302_h1303_direction_note_recheck.md)
- [H-355 double-short-side clarification audit](h355_double_short_side_clarification_audit.md)
- [H-933/H-960 034 contrast source audit](h933_h960_034_contrast_source_audit.md)
- [H-1304/H-1344/H-1347 source-dark direct request audit](h1304_h1344_h1347_source_dark_direct_request_audit.md)

That queue ranks H-1302/H-1303 direction-note rechecks, H-355 double-short-side clarification, H-933/H-960 `034` contrast cases, and H-233 as the `TAB:B` public-image type control as the first acquisition actions.

## Interpretation Boundary

This audit does not support:

- Sign segmentation.
- Allography.
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
