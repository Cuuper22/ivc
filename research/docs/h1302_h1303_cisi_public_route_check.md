# H-1302/H-1303 CISI Public Route Check

Date: 2026-05-26

## What This Note Is

This note records a route check on two Harappa objects, H-1302 and H-1303. A route is a concrete path from one of our catalog rows to a published photograph of the same object; a route check asks whether a particular published volume actually contains that photograph, before anyone spends time reading it.

The volume tested is the public Internet Archive scan of CISI Pakistan — CISI being the Corpus of Indus Seals and Inscriptions, the primary published photographic record. A source panel is the plate image of the object itself, the thing we need in order to check our catalog row against reality.

## Question

```text
Can the public Internet Archive CISI Pakistan volume supply H-1302/H-1303 source panels?
```

## Artifacts

```text
data/open_prototype/reports/h1302_h1303_cisi_public_route_check.csv
data/open_prototype/reports/h1302_h1303_cisi_public_route_check_summary.json
data/open_prototype/reports/h1302_h1303_source_request_log.csv
data/open_prototype/reports/h1302_h1303_source_request_log_summary.json
```

Source/context files:

```text
tmp/cisi_pakistan_ocr/pakistan_djvu.xml
tmp/h1302_h1303_cisi_public_route_check/derived/cisi_pakistan_contents_page-006.png
tmp/h1302_h1303_cisi_public_route_check/derived/cisi_pakistan_harappa_range_crop.png
```

## Result

The public CISI Pakistan volume is not the H-1302/H-1303 source-panel route.

The volume contents page scopes the Harappa black-and-white photograph section to `H-266` through `H-1019`, with gaps noted on the page. The two target objects are `H-1302` and `H-1303`, so they fall outside that public volume's Harappa photograph range.

The OCR check found no exact target hits for:

```text
H-1302
H1302
H-1303
H1303
```

Bare `1302` and `1303` hits do occur, but they are Mohenjo-daro `M-1302/M-1303` homonyms, index/data noise, or unrelated numeric strings. They cannot be used for Harappa `H-1302/H-1303`.

## Decision

Stop spending time on public CISI Pakistan vol. 2 for these two objects. The next route is:

1. CISI 3.1 or equivalent supplemental Harappa material.
2. HARP object/photo records.
3. ICIT/Wells/Fuls rows or notes for the exact correction claim.
4. Source-holder request with the Nature citation and local row IDs.

## Follow-Up Source Request

The source-holder request has now been sent:

```text
gmail:[redacted-msgid]
recipient: [harappa-project-email]
subject: Source image request: H-1302 and H-1303 Harappa tablets
```

The request asks for source panels, plate/catalog references, side labels, side-order basis, row-convention basis, direction/orientation basis, the bridge from the Daggumati/Revesz correction note to local `+700-033+`, and damage/copy/family notes. A copy family is a group of objects carrying the same inscription, which matters because a repeated text can otherwise look like independent evidence.

## Boundary

This route check validates no source panel, no side order, no image direction, no `+700-033+` row, no sign correction, no value, and no translation.
