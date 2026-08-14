# Lipi FRAME700 034 IA CISI Page Locator

Date: 2026-05-25

## Question

This note is a lookup table telling us which catalog page to open for each object under study. FRAME700 is the project's label for short inscription rows built on sign `700`, such as `+700-032+`; the `034` packet is the bundle of objects gathered to test whether the sign codes `032`, `033`, and `034` are separate choices in the same slot. An earlier route audit — a check of which published sources actually reach each object — found nine of those packet objects with OCR hits in the Internet Archive (IA) scans of CISI, the Corpus of Indus Seals and Inscriptions, the standard photographic catalog of Indus objects. The question: where are those hits at page level?

This is a source-acquisition artifact, not a source-image validation artifact. It says where to look, not what the images show.

## Local Artifacts

```text
data/open_prototype/tools/lipi_frame700_034_ia_cisi_page_locator.mjs
data/open_prototype/reports/lipi_frame700_034_ia_cisi_page_locator.csv
data/open_prototype/reports/lipi_frame700_034_ia_cisi_page_locator_summary.json
```

Inputs:

```text
data/open_prototype/reports/lipi_frame700_034_source_route_audit.csv
Internet Archive DjVu XML for CISI Collections in India
Internet Archive DjVu XML for CISI Collections in Pakistan
```

Source files:

- https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India_djvu.xml
- https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan_djvu.xml

## Result

```text
IA route objects input: 9
located objects: 9
missing after positive route: 0
page locator rows: 11
total OCR hits: 27
accepted decipherment claims: 0
```

Located objects. In the packet role column, a target is an object the test is about, and a control is a comparison object used to check the target.

| Object | Priority | Packet role | IA volume | Leaves | Hit count | Immediate use |
| --- | --- | --- | --- | --- | ---: | --- |
| `H-212` | core | `032` control | CISI Collections in India | `406`, `837` | 4 | Reconcile duplicated OCR pages, then inspect plate/source visibility. |
| `H-353` | core | `033` control | CISI Collections in India | `265`, `696` | 4 | Reconcile duplicated OCR pages, then inspect plate/source visibility. |
| `H-771` | core | `034` target | CISI Collections in Pakistan | `358` | 4 | First independent-batch IA source page. |
| `H-789` | core | `033` control | CISI Collections in Pakistan | `359` | 2 | Same independent batch as `H-771`. |
| `H-893` | core | `034` target | CISI Collections in Pakistan | `371` | 3 | First local-contrast stress target page. |
| `H-925` | core | `033` control | CISI Collections in Pakistan | `373` | 7 | Shared local-contrast control; high page density means side variants/copies must be separated carefully. |
| `H-930` | core | `032` control | CISI Collections in Pakistan | `374` | 1 | Local-contrast control page. |
| `H-983` | core | `034` target | CISI Collections in Pakistan | `377` | 1 | Second local-contrast target page. |
| `H-910` | optional | `034` target | CISI Collections in Pakistan | `372` | 1 | Optional repeated-branch check only. |

## Page Queue

Open these first:

```text
CISI Pakistan leaf 358: H-771
CISI Pakistan leaf 359: H-789
CISI Pakistan leaf 371: H-893
CISI Pakistan leaf 373: H-925
CISI Pakistan leaf 374: H-930
CISI Pakistan leaf 377: H-983
CISI India leaf 265 and 696: H-353 duplicate-locator pair
CISI India leaf 406 and 837: H-212 duplicate-locator pair
CISI Pakistan leaf 372: optional H-910
```

The CSV stores direct IA reader URLs and page-image URLs for each row.

## Consequence

The source route is now operational for part of the packet:

```text
H-771 / H-789 can be inspected as the first independent low-copy IA pair.
H-893 / H-925 / H-930 can be inspected as the first local minimal-contrast IA triad.
H-983 / H-353 can start the second visual-object local lane, with H-2211 still on CISI 3.1 route.
```

A lane is one of the separate evidence tracks the project runs, kept apart so a result in one does not lean on the other.

This creates the first page-addressable source inspection queue for `034`.

## Follow-up Visual Pass

The located pages have now been manually inspected in [Lipi FRAME700 034 IA CISI visual inspection](lipi_frame700_034_ia_cisi_visual_inspection.md).

```text
visual plate objects: 8
data-register-only objects: 1
source panel count matches local side count: 3
source panel count exceeds local side count: 5
accepted decipherment claims: 0
```

The cleanest two-panel locators are `H-789`, `H-930`, and optional `H-910`. The source pages expose immediate side-count or variant hazards for `H-771`, `H-893`, `H-925`, `H-983`, and `H-353`.

## Boundary

OCR page location is not sign validation.

This locator cannot decide:

- whether the listed page image truly shows the packet side,
- whether `032`, `033`, and `034` are visually separable,
- whether side labels are physical, editorial, or photographic,
- whether recorded direction is inscription direction or impression direction,
- whether any object belongs to a copy or mold family,
- any meaning, number, phonetic value, administrative function, language, or translation.

It only tells us where to look next.
