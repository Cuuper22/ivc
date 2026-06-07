# H-355 Double-Short-Side Clarification Audit

Date: 2026-05-24

## Purpose

This follows the [Lipi short-mark source acquisition queue](lipi_short_mark_source_acquisition_queue.md).

Question:

```text
Can public evidence clarify whether H-355 has two distinct physical short sides carrying +700-033+, or whether the duplicate short rows are a catalog artifact?
```

This is a source-availability audit. It is not plate validation.

## Local Artifacts

```text
data/open_prototype/reports/h355_double_short_side_clarification_audit.csv
data/open_prototype/reports/h355_double_short_side_clarification_summary.json
```

## Packet Context

H-355 is the only double-short-side case in the first 17-object short-mark source acquisition packet.

```text
artifact: H-355
type: TAB:I
site: Harappa
sides: 3
row_count_in_packet: 2
raw_ids: 1374.1;1374.2;1374.3
excavation_id: 1274
dimensions_mm: 15.5 x 5.8 x 0
group_signature: 1:+400-740-176+|2:+700-033+|3:+700-033+
```

The packet rows require separate checks for both short rows:

```text
side 1: +400-740-176+
side 2: +700-033+
side 3: +700-033+
```

## Public Source Result

The existing public lead is text-only:

```text
https://indusscriptmore.blogspot.com/2012/
```

The relevant public context is a range/list mention covering `H-352-357 (incised)`. It does not provide an H-355 object-level image, a plate ID, side labels, or a way to decide whether rows 2 and 3 are two physical sides.

Fresh public searches on 2026-05-24 did not find an H-355 object-level image, plate, or source-grade side view in the checked results. The negative result is limited to the checked public-web layer; it is not a claim that no source image exists in CISI, HARP, museum archives, libraries, or private scans.

## Why H-355 Matters

H-355 is structurally different from the ordinary two-side `+400-740-176+` with `+700-033+` packet cases.

If the two `+700-033+` rows are real distinct physical sides, H-355 is evidence for deliberate repeated short-side marking on a three-side `TAB:I` object.

If they are a side-label convention, duplicate catalog entry, copied row, or other source artifact, H-355 must be removed from any physical side-repetition comparison.

Those are very different outcomes. The public layer cannot choose between them.

## Required Evidence

The H-355 source request needs:

1. A CISI, HARP, Harappa archive, museum, or library source image/plate showing all three catalog side rows.
2. Caption or catalog notes binding `1374.1`, `1374.2`, and `1374.3` to the physical object.
3. A source-side explanation of whether rows 2 and 3 are distinct physical sides.
4. Side-order basis: physical, photographic, editorial, arbitrary, or unresolved.
5. Direction basis for both short rows: inscription, impression, catalog-normalized, or unresolved.
6. Independent visibility checks for both `+700-033+` rows.
7. Visibility check for the longer `+400-740-176+` row.

## Consequence

H-355 should stay in the first acquisition batch, but with a stricter outcome gate than the ordinary two-side rows:

```text
status: requires_CISI_HARP_three_side_source
public_object_image_leads: 0
source_validation_fields_filled: 0
```

The manual packet should not fill `catalog_rows_distinct_physical_sides`, `side_order_basis`, `short_mark_verified`, `longer_text_verified`, or `relation_survives_image_check` until a three-side source is inspected.

## Interpretation Boundary

This audit does not support:

- Side relation.
- Physical side function.
- Numerical value.
- Metrological reading.
- Sign meaning.
- Phonetic value.
- Language identity.
- Translation.
