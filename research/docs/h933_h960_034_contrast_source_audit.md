# H-933/H-960 034 Contrast Source Audit

Date: 2026-05-24

## Purpose

This note checks whether public sources can settle two objects, H-933 and H-960, that are the required contrast cases for a pattern the project is testing about the signs `033` and `034`. It exists so the pattern is tested against its own counter-examples rather than only its supporting rows. It follows the [Lipi short-mark source acquisition queue](lipi_short_mark_source_acquisition_queue.md).

Question:

```text
Can public evidence validate the two `034` contrast cases, H-933 and H-960, where the short row appears before the longer `+400-740-176+` row?
```

This is a source-availability audit. It is not plate validation.

## Local Artifacts

```text
data/open_prototype/reports/h933_h960_034_contrast_source_audit.csv
data/open_prototype/reports/h933_h960_034_contrast_source_summary.json
```

## Packet Context

H-933 and H-960 are the two `034` contrast objects in the 17-object short-mark packet — the bundled list of objects whose source images the project is trying to obtain in one batch.

```text
H-933: TAB:I, 1:+034-700+|2:+400-740-176+
H-960: TAB:I, 1:+700-034+|2:+400-740-176+
```

Both are classified in the packet as:

```text
packet_priority: P1_034_before_with_400_740_176
acquisition_bucket: A_034_contrast_case
side_relation: short_before_all_longer
```

They differ internally in short-row order:

```text
H-933: 034:700_last
H-960: 034:700_first
```

That difference matters because the short-mark orientation audits already showed that `+700-034+` should not be silently collapsed with `+034-700+` before source-side direction is checked.

## Public Source Result

The existing public lead is text-only:

```text
https://indusscriptmore.blogspot.com/2012/
```

The relevant public context is a range/list mention:

```text
H-933, 936, 960, 964, 308, and 312-314 (incised)
```

It gives a bibliographic pointer, but it does not provide an object-level image, plate ID, side labels, sign segmentation, or direction basis for either H-933 or H-960.

Fresh public searches on 2026-05-24 did not find object-level public images or source-grade side views for H-933 or H-960 in the checked results. The negative result is limited to the checked public-web layer; it is not a claim that no source image exists in CISI, HARP, museum archives, libraries, or private scans.

## Why This Pair Matters

The broader planning layer has a catalog-side contrast:

```text
033: overrepresented in short_after_all_longer rows
034: underrepresented in short_after_all_longer rows
```

H-933 and H-960 are the first packet-level `034` cases where the longer row is the same high-priority context:

```text
+400-740-176+
```

That makes them the required negative/contrast pair against the `033` rows. If source images show the short-before-longer relation survives, the `033`/`034` contrast remains worth testing. If source images show catalog order, direction, segmentation, or side labels are wrong, the contrast collapses or has to be rebuilt.

The public layer cannot decide that.

## Required Evidence

The H-933/H-960 source request needs:

1. CISI, HARP, Harappa archive, museum, or library source images/plates for both objects.
2. Images or notes showing both catalog side rows for each object.
3. A source-side explanation of whether the catalog rows are distinct physical sides.
4. Side-order basis: physical, photographic, editorial, arbitrary, or unresolved.
5. Direction basis for the short rows: inscription, impression, catalog-normalized, or unresolved.
6. Independent visibility checks for `H-933 1:+034-700+` and `H-960 1:+700-034+`.
7. Visibility checks for both `+400-740-176+` longer rows.
8. Explicit preservation of the internal order difference between `+034-700+` and `+700-034+`.
9. A paired outcome: whether the `034` before-longer relation survives image-side checking in both, one, or neither object.

## Consequence

H-933 and H-960 should stay in the first acquisition batch as a paired contrast request:

```text
status: requires_CISI_HARP_two_side_source
public_object_image_leads: 0
source_validation_fields_filled: 0
```

The manual packet should not fill `catalog_rows_distinct_physical_sides`, `side_order_basis`, `short_mark_verified`, `longer_text_verified`, `sign_033_034_contrast_visible`, or `relation_survives_image_check` until source images or source-grade catalog notes are inspected.

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
