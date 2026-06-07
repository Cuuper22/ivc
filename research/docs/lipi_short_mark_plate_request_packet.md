# Lipi Short-Mark Plate Request Packet

Date: 2026-05-24

## Purpose

This packet turns the [Lipi short-mark side-relation validation sheet](lipi_short_mark_side_relation_validation_sheet.md) into a first manual plate request.

The packet is deliberately narrow:

```text
17 artifacts where the corrected 033/034 catalog-side relation contrast overlaps the raw +400-740-176+ longer-context hint.
```

It is designed for source/image inspection. It does not ask anyone to translate the signs.

## Local Artifacts

```text
data/open_prototype/tools/lipi_short_mark_plate_request_packet.mjs
data/open_prototype/reports/lipi_short_mark_plate_request_packet.csv
data/open_prototype/reports/lipi_short_mark_plate_request_packet_summary.json
```

Input:

```text
data/open_prototype/reports/lipi_short_mark_side_relation_validation_sheet.csv
```

## Packet Scope

```text
packet_artifacts: 17
packet_rows_from_validation_sheet: 18
tier_1_033_after_with_400_740_176: 15 artifacts
tier_1_034_before_with_400_740_176: 2 artifacts
TAB:B: 1 artifact
TAB:I: 16 artifacts
duplicated_artifact_in_packet: H-355
```

H-355 appears once as an artifact in this packet but covers two matching source rows.

## Artifact List

`tier_1_033_after_with_400_740_176`:

```text
H-233
H-309
H-316
H-353
H-355
H-357
H-935
H-978
H-1302
H-1303
H-1304
H-1344
H-1345
H-1346
H-1347
```

`tier_1_034_before_with_400_740_176`:

```text
H-933
H-960
```

## Manual Fields

The packet pre-fills artifact context and leaves evidence fields blank:

```text
source_found
source_citation
image_or_plate_id
image_resolution_or_quality
catalog_rows_distinct_physical_sides
side_order_basis
image_direction_basis
short_mark_verified
longer_text_verified
sign_033_034_contrast_visible
relation_survives_image_check
validation_outcome
notes
```

These fields are blank because the current planning layer cannot answer them. They must be filled only from images, plates, catalog notes, or direct source records.

## Allowed Outcomes

Use one of these values in `validation_outcome`:

| Outcome | Meaning |
| --- | --- |
| `passes_source_check` | Source image/catalog confirms distinct sides, direction basis, visible short mark, visible longer text, and the side relation. |
| `fails_side_relation` | Signs may be visible, but the apparent catalog-side relation does not survive source side order. |
| `fails_segmentation` | The local sign segmentation or row grouping is wrong or unresolved. |
| `fails_033_034_contrast` | The apparent `033`/`034` contrast is not visible or cannot be accepted at source resolution. |
| `direction_unresolved` | The artifact is visible, but inscription/impression/catalog direction cannot be resolved. |
| `source_unavailable` | No adequate source image, plate, or catalog note is available. |

## Pass Standard

An artifact can only get `passes_source_check` if all of these are true:

1. The relevant catalog rows are visible or documented.
2. The rows are confirmed as distinct physical sides, or the source explicitly explains the side convention.
3. The short mark is visible enough to verify `033` or `034`.
4. The longer text is visible enough to verify `+400-740-176+`.
5. The side relation survives after accounting for image direction and side order.

If any item fails, the packet should preserve the failure reason instead of smoothing it into a positive result.

## Interpretation Boundary

This packet does not support:

- Physical side function.
- Numerical value.
- Metrological reading.
- Commodity reading.
- Administrative reading.
- Sign meaning.
- Phonetic value.
- Language identity.
- Translation.

## Public Lead Follow-Up

[Lipi short-mark plate public lead search](lipi_short_mark_plate_public_lead_search.md) checked 20 public endpoints for this packet. It found candidate image/post leads for H-233, H-1302, and H-1303; text-only or bibliographic leads for ten artifacts; and no public lead in the checked sources for H-1304, H-1344, H-1345, H-1346, and H-1347.

None of those leads fills the manual validation fields above. They only sharpen source acquisition.
