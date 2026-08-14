# Lipi FRAME700 034 Independent Source Lead Audit

Date: 2026-05-25

## Scope

This note records the first attempt to find published evidence for a new batch of objects. FRAME700 is the project's label for short inscription rows built on sign `700`, such as `+700-034+`; the `034` work asks whether the sign codes `032`, `033`, and `034` are separate choices in the same slot. This batch is called independent because its objects do not overlap the earlier batch, so a result here would not lean on that one. The objects are grouped in triads — sets of three, one per sign code:

```text
H-1850 / H-1842 / H-1772
H-771 / H-789 / H-1123
H-1943 / H-1940 / H-854
H-2204 / H-2209 / H-2217
```

The purpose is source acquisition, not decipherment. No reading, language assignment, sign meaning, phonetic value, number value, metrological value, or translation is accepted here.

## Machine-Readable Outputs

```text
data/open_prototype/reports/lipi_frame700_034_independent_source_leads.csv
data/open_prototype/reports/lipi_frame700_034_independent_source_leads_summary.json
data/open_prototype/reports/lipi_frame700_034_source_coding_sheet_template.csv
```

## Result

```text
objects_checked: 12
source_grade_public_row_hits: 0
public_object_leads: 1
secondary_bibliographic_pointers: 1
objects_still_requiring_CISI_HARP_or_archive_images: 12
accepted_decipherment_claims: 0
source_coding_sheet_rows: 25
```

Source-grade means an image or plate entry good enough to check signs against, rather than a mention. The useful hit is `H-2204` via the local hook `H95-2482` — a hook being an identifier in our own records that can be searched for elsewhere.

That hit is not enough to validate the local row. It is an object-level source lead and a reconciliation target.

There is also one secondary bibliographic pointer for `H-1943`, but it is not a source image. The Indus Dictionary Project page points to `H-1943 C` in CISI 3.1 page 266 and then makes interpretive claims. Only the CISI page pointer is useful; the interpretive layer gets zero evidence credit.

## Public Lead Found

### H-2204 / H95-2482

Local metadata:

```text
CISI: H-2204
Local source hook: H95-2482; Figure 27.06
Local rows: 659.1:+700-034+; 659.2:+400-740-032-027+
Local dimensions: 19 x 7.3 x 0
Local material/shape: Steatite / prism / triangular
```

Public source 1:

- [Harappa.com, Recent Indus Discoveries and Highlights from Excavations at Harappa 1998-2000](https://www.harappa.com/node/3000)
- Figure list item: `H95-2482/4419-05`
- Description: incised steatite tablet, Period `3B/3C`

Public source 2:

- [Meadow and Kenoyer 1997, Excavations at Harappa 1994-1995](https://www.harappa.com/sites/default/files/pdf/Kenoyer1997_Excavations%20at%20Harappa%201994-1995%20New%20Perspective.pdf)
- Figure `10.07`
- Accession `H95-2482`
- Excavation unit `4419-05`
- Object class: incised tablet
- Dimensions in the public table layer: `19 x 7.3 x 3.5`
- Public table layer associates the object with `3` incised sides.

Reconciliation problem:

```text
Local row packet says H95-2482 / Figure 27.06, 19 x 7.3 x 0, and two local rows.
Public sources say H95-2482/4419-05, Figure 4 item 4 or Figure 10.07, 19 x 7.3 x 3.5, and three incised sides.
```

Current status:

```text
H-2204 has a real object-level source lead.
H-2204 does not yet have public row-level confirmation.
The exact source images or plates are still needed before using this as evidence for +700-034+.
```

## Checked With No Source-Grade Public Hit

The checked public layer did not yield source-grade object-side images or plate entries for:

```text
H-1850 / H2001-5141 / Figure 48.07
H-1842 / H95-2416 / Figure 26.07
H-1772 / H2000-4437 / Figure 39.05
H-771 / 657678
H-789 / 12549604
H-1123 / 9015360
H-1940 / H2001-5072 / Figure 44.05
H-854 / 10010647
H-2209 / H95-2423
H-2217 / H95-2521 / Figure 27.09
```

This is not proof that no source exists. It means public web search did not supply the required source-grade image or plate layer. These remain archive/CISI/HARP requests.

`H-1943` is excluded from the above no-pointer list because it has a secondary CISI-page pointer:

```text
H-1943 C / CISI 3.1 page 266
```

That pointer does not validate the local row.

## Why This Matters

The first independent batch is now evidence-led:

1. The first three triads remain pure source requests.
2. The fourth triad has one real public object hook, but it exposes a thickness/side-count mismatch that must be resolved rather than smoothed over.
3. No public source in this pass lets us claim that `034`, `033`, and `032` are visually distinct under source-image inspection.

## Required Next Evidence

For all 12 objects:

```text
all sides or all available source plates
source plate/page/image identifier
side labels and side order basis
inscription versus impression direction
visible 032/033/034 contrast
visible segmentation of the companion rows
object dimensions, material, shape, condition, and find context
copy, mold, or family relation notes if present
```

## Boundary

This audit changes the source-acquisition state, not the decipherment state.

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted language assignments: 0
```
