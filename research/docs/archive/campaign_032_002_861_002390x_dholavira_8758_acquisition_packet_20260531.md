# Dholavira 8758 acquisition packet

Date: 2026-05-31 America/Los_Angeles

Status: source acquisition packet, not goal completion. Follow-on source contact was sent on 2026-05-31 and is recorded in `docs/campaign_032_002_861_002390x_dholavira_8758_source_contact_20260531.md`.

## Why This Target

Dholavira `4237.1` is one of the two local `002-390-705` rows:

- `M-1825`: `031 -> 002-390 -> 705 -> <END>`, source-dark/secondary-icon-only.
- `4237.1`: `388 -> 002-390 -> 705 -> <END>`, Dholavira metadata-cluster pressure but no image binding.

Here is why the target matters. If Dholavira `4237.1` can be bound to an actual source image or caption, repeated terminal `705` becomes much more useful for testing the branch-tail model. It still would not create a value or translation, but it would move `705` from acquisition pressure toward source-normalized branch evidence.

Accepted value, phonetics, language identity, function, sign meaning, and translation remain 0.

## Target Identity

Local row:

- Row id: `4237.1`
- Object field: `-`
- Site: Dholavira
- Type: `SEAL:S`
- Locus: Lower Town, `ZA-12:2-`
- Period: `5`
- Class: `SC`
- Local dimensions: `27.62 x 21.31(ext) x 7.11-11.17(ext)`
- Local text: `+151-032-388-002-390-705+`

Source/OCR route:

- The public Bisht/PDFCoffee OCR mirror exposes an `8758 / ZA-12:2 / 27.62 x 21.31 x 7.11-11.17` cluster.
- That cluster matches the local row well enough to keep the acquisition target hot.
- The same mirror also exposes an individual `8758` catalogue detail in the National Museum section. The OCR text describes a unicorn seal, says there are "no other details," and notes the missing knob / white steatite state. This confirms `8758` is a real source-contact target, but it does not provide signs or image binding.
- It is still not a source-image binding.

## Hard Guards

Page 18 item 10:

- The page-18 item-10 crop is visually compatible with a reverse `+151-032-388-002-390-705+` neighborhood.
- But the public OCR individual-seal details list item `10` as Acc. No. `2118` with an inscription of 5 signs.
- Local `4237.1` requires 6 signs and the `8758 / ZA-12:2` metadata cluster.
- Therefore page 18 item 10 is a wrong-object/lookalike pressure route, not a binding candidate unless a direct bridge appears.

ICIT 4348:

- The Singh et al. supplement mentions `ICIT 4348 (Dholavira)`.
- Local `4348.1` is a different Dholavira `TAG` row: `]740-142-000-002-861-390[`.
- The near-frame scout reinforces this: `4348.1` is a gapped `002-861-390` row, not adjacent `002-390-705`.
- Do not use ICIT 4348 as a bridge into `4237.1`.

## Public Search Refresh

Fresh targeted searches on 2026-05-31 looped back to the Bisht/PDFCoffee route and did not find an external image/caption bridge for Acc. No. `8758`, `ZA-12:2`, or the six-sign sequence `+151-032-388-002-390-705+`. A targeted `8758 / National Museum / Dholavira` refresh found the individual `8758` remark in the same public mirror, but not an image, sign count, or source transcription.

Main public route:

- `https://pdfcoffee.com/excavations-at-dholavifra-1989-2005-rs-bisht-2015-pdf-free.html`

## Source Contact

The compact request below was sent to `[harappa-project-email]` on 2026-05-31.

- Gmail message id: `[redacted-msgid]`
- Gmail thread id: `[redacted-msgid]`
- Gmail timestamp: `2026-05-31T11:26:39`
- Send report: `data/open_prototype/reports/campaign_032_002_861_002390x_dholavira_8758_source_contact_20260531.csv`

This changes acquisition state only. It does not bind `4237.1`, prove the sign sequence, or count strict `705`.

## Compact Request Text

Subject: Narrow source check: Dholavira Acc. No. 8758 / ZA-12:2

```text
Hi,

I am trying to verify one Dholavira inscribed seal at the source-image/catalog level before using it in any structural analysis:

Acc. No. 8758 / ZA-12:2

Local row I am trying to bind:

- Dholavira row 4237.1
- locus in local metadata: Lower Town, ZA-12:2-
- dimensions: 27.62 x 21.31 x 7.11-11.17
- local sign sequence: +151-032-388-002-390-705+

The public OCR layer of Bisht 2015 exposes the 8758 / ZA-12:2 / dimension cluster, but I have not found an image or caption that binds that metadata row to the six-sign seal.

I am not asking for a decipherment claim. I only need source binding:

- image/plate/caption for Acc. No. 8758 or ZA-12:2;
- source transcription or sign count, if present;
- confirmation whether the six-sign sequence is associated with Acc. No. 8758;
- any note distinguishing it from page 18 item 10 / Acc. No. 2118, which appears to be a five-sign wrong-object/lookalike route.

Best,
Cuper
```

## Decision

Status: `dholavira_8758_source_contact_sent_awaiting_reply_no_values`.

Dholavira `4237.1` remains acquisition-hot and now has a live source-contact branch. It has stronger metadata pressure than before, but zero strict source-image count. No strict `705`, value, phonetics, language identity, function, sign meaning, or translation is accepted.
