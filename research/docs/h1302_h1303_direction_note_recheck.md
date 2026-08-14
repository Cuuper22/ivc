# H-1302/H-1303 Direction-Note Recheck

Date: 2026-05-24

## Purpose

This note rechecks what published sources actually prove about two Harappa tablets, H-1302 and H-1303. Other researchers have discussed these two in connection with mirrored writing and a correction to a sign catalog. The temptation is to treat that discussion as evidence about our own catalog rows. This note tests whether it is.

It follows the [Lipi short-mark source acquisition queue](lipi_short_mark_source_acquisition_queue.md).

Question:

```text
What exactly do the public direction-note and image leads prove for H-1302 and H-1303?
```

This is a source-reconciliation audit: it compares what published notes say against what our own rows record. It is not plate validation — nobody has yet inspected a published photograph of these objects.

## Local Artifacts

```text
data/open_prototype/reports/h1302_h1303_direction_note_recheck.csv
data/open_prototype/reports/h1302_h1303_direction_note_recheck_summary.json
```

Follow-up provenance gate:

```text
docs/h1302_h1303_source_provenance_gate.md
data/open_prototype/reports/h1302_h1303_source_provenance_gate.csv
data/open_prototype/reports/h1302_h1303_source_provenance_gate_summary.json
```

## Source Leads Checked

Published direction/allograph lead:

```text
https://www.nature.com/articles/s41599-021-00713-0
```

Public image/context lead:

```text
https://bharatkalyan97.blogspot.com/2021/06/boustrophedon-form-of-writing-qoli.html
```

The public image URLs were downloaded to a temporary folder for inspection only. The images were not stored in the repository.

## Packet Context

A packet is a bundle of objects grouped for one review pass. Both artifacts are in the 17-object short-mark packet:

```text
H-1302: TAB:I, 1:+400-740-176+|2:+700-033+
H-1303: TAB:I, 1:+400-740-176+|2:+700-033+
```

The packet needs source evidence for:

```text
source image or plate ID
distinct physical side status
side-order basis
image-direction basis
short +700-033+ visibility
long +400-740-176+ visibility
whether the catalog-side relation survives image-side checking
```

## Nature 2021 Lead

The Nature 2021 allograph article — an allograph being two shapes treated as the same sign — is a real source lead. It names H-1302 and H-1303, with H-1822, in a mirrored-writing / ICIT-correction discussion after comparing against CISI.

Limit:

```text
The web text preserves the artifact IDs but not the inline sign images as numeric sign IDs.
```

Consequence:

```text
The Nature article justifies prioritizing H-1302 and H-1303 for direction-note reconciliation, but it does not fill the local packet's source-validation fields.
```

## Public Image Lead

Eight unique image URLs from the public Blogger page were checked manually.

```text
unique_image_urls_checked: 8
unlabeled_object_panel_candidates: 2
tiny_unlabeled_crops: 2
standalone_sign_icons: 2
context_or_lexical_excerpts: 2
repo_image_storage: none
```

Manual result:

- Two grayscale artifact images are plausible object-panel candidates from the mirrored-writing page context, but neither has a visible H-1302 or H-1303 label in the image.
- Two tiny grayscale crops may come from artifact panels, but they are too small and unlabeled for object assignment.
- Two images are standalone sign icons labeled 256 and 266.
- One image is a directionality/context excerpt.
- One image is a lexical excerpt.

## Consequence

The next source request for H-1302/H-1303 should ask for:

1. CISI or HARP source images for all catalog side rows of both objects.
2. The exact catalog or article-side basis for the mirrored-writing correction.
3. Captions binding the two public object-panel candidates, if they are to be used even as low-grade visual pointers.
4. Explicit reconciliation between the ICIT/Wells/Fuls direction note and the local packet rows `1:+400-740-176+|2:+700-033+`.

## Interpretation Boundary

This audit does not support:

- Local sign correction.
- Sign segmentation.
- Side order.
- Physical side function.
- Numerical value.
- Metrological reading.
- Sign meaning.
- Phonetic value.
- Language identity.
- Translation.
