# Lipi Short-Mark Source Acquisition Queue

Date: 2026-05-24

## Purpose

This note is a ranked to-do list for getting better source material. It exists because two earlier steps — the [Lipi short-mark plate request packet](lipi_short_mark_plate_request_packet.md), which named 17 artifacts needing image validation, and the [Lipi short-mark plate public lead search](lipi_short_mark_plate_public_lead_search.md), which checked public web sources for them — left the project with unequal starting points per artifact. Some artifacts have public leads; some have nothing. This queue turns that mixed picture into an ordered acquisition plan.

Question:

```text
Given the 17 first-pass plate-check artifacts and the public lead search, what source should be acquired or inspected first?
```

This is an acquisition queue only. It is not image validation.

## Local Artifacts

```text
data/open_prototype/tools/lipi_short_mark_source_acquisition_queue.mjs
data/open_prototype/reports/lipi_short_mark_source_acquisition_queue.csv
data/open_prototype/reports/lipi_short_mark_source_acquisition_summary.json
```

Inputs:

```text
data/open_prototype/reports/lipi_short_mark_plate_request_packet.csv
data/open_prototype/reports/lipi_short_mark_plate_public_leads.csv
```

## Results

The queue sorts the 17 artifacts into lettered action tiers (A first, then B, then C):

```text
queue_artifacts: 17
A_direction_note_recheck: 2
A_double_short_side_case: 1
A_034_contrast_case: 2
A_tab_b_type_control_with_public_image_lead: 1
B_source_dark_direct_cisi_or_harp: 5
C_replicate_033_after_case: 6
```

Public lead status — what the public search found for each artifact:

```text
candidate_image_plus_published_direction_note: H-1302; H-1303
candidate_public_image_or_post_lead: H-233
text_only_or_bibliographic_public_lead: H-355; H-933; H-960; H-309; H-316; H-353; H-357; H-935; H-978
no_public_lead_in_checked_sources: H-1304; H-1344; H-1345; H-1346; H-1347
```

## First Acquisition Actions

CISI is the published Corpus of Indus Seals and Inscriptions; HARP is the Harappa Archaeological Research Project. Both are plate-grade sources, unlike the public web leads.

1. H-1302 and H-1303: request plate or source images and reconcile the published direction/corpus-note lead against CISI or HARP image evidence. The follow-on [H-1302/H-1303 direction-note recheck](h1302_h1303_direction_note_recheck.md) confirms the Nature 2021 lead but leaves all packet validation fields pending.
2. H-355: request all three catalog side rows and determine whether the two short `+700-033+` rows are distinct physical sides or a catalog/duplication artifact. The follow-on [H-355 double-short-side clarification audit](h355_double_short_side_clarification_audit.md) finds no object-level public image and keeps this as a CISI/HARP three-side source request.
3. H-933 and H-960: request plate or source images for the two `034` contrast cases and check whether the before-longer relation survives image-side validation. The follow-on [H-933/H-960 034 contrast source audit](h933_h960_034_contrast_source_audit.md) finds no object-level public images and keeps them as a paired CISI/HARP two-side source request.
4. H-233: inspect the public slide leads only as acquisition pointers, then verify the `TAB:B` type-control case against a plate-grade source. The follow-on [H-233 public slide visual lead audit](h233_public_slide_visual_lead_audit.md) narrows the public post to one H-233-relevant slide and one off-target H-1997 slide.
5. H-1304, H-1344, H-1345, H-1346, and H-1347: skip broad public-search expansion for now and go straight to CISI, HARP, Harappa image archives, or library plate access. The follow-on [H-1304/H-1344/H-1347 source-dark direct request audit](h1304_h1344_h1347_source_dark_direct_request_audit.md) confirms that fresh public searches still find no object-level image, plate, caption, or useful text-only lead for the five-object batch. ("Source-dark" means no public trace at all in the checked sources.)
6. H-309, H-316, H-353, H-357, H-935, and H-978: use the text-only public lead as a bibliographic pointer while treating source-grade validation as still pending.

## Required Evidence

Each row in the queue keeps the fields needed to fill the manual packet:

```text
source citation or image/plate ID
catalog rows are distinct physical sides or source explains side convention
side order basis is physical, photographic, editorial, or arbitrary
short-mark direction basis is inscription, impression, catalog-normalized, or unresolved
short mark visible enough to check the packet row
longer text visible enough to check +400-740-176+
033/034 contrast visibility recorded
relation survives or fails after image-side check
```

## Interpretation Boundary

This queue accepts no side relation, physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, or translation.

The only admissible output is a ranked plan for acquiring or inspecting better source evidence.
