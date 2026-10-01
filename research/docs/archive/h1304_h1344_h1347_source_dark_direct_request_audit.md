# H-1304/H-1344/H-1347 Source-Dark Direct Request Audit

Date: 2026-05-24

## What This Note Is

This note decides how to chase images for five Harappa tablets that the open web does not show. Source-dark means exactly that: we have catalog rows for the object, but no published photograph we can reach. Until an object has a picture, its catalog row cannot be checked against reality.

The five sit in the same packet — a bundle of objects grouped for one review pass — because they carry the same two-row inscription. The note asks whether more web searching is worth the effort, or whether the batch should go straight to the institutions that hold the plates.

## Question

For the five source-dark `033` packet objects H-1304, H-1344, H-1345, H-1346, and H-1347, is there enough public evidence to keep searching the open web, or should the batch go straight to CISI, HARP, Harappa image archives, library plates, or direct archive access?

## Local Packet Context

All five objects share the same local packet signature:

```text
type: TAB:I
site: Harappa
packet_priority: P1_033_after_with_400_740_176
acquisition_bucket: B_source_dark_direct_cisi_or_harp
public_lead_status: no_public_lead_in_checked_sources
signature: 1:+400-740-176+|2:+700-033+
short row: 2:+700-033+
short order: 033:700_first
side relation in catalog layer: short_after_all_longer
```

Artifact details:

| Artifact | Raw IDs | Excavation ID | Dimensions mm | Material | Shape | Local rows |
| --- | --- | --- | --- | --- | --- | --- |
| H-1304 | 5470.1;5470.2 | 2480 | 14.5 x 0 x 0 | - | oval | `1:+400-740-176+`; `2:+700-033+` |
| H-1344 | 4085.1;4085.2 | -752 | 14 x 8 x 0 | - | prism | `1:+400-740-176+`; `2:+700-033+` |
| H-1345 | 4086.1;4086.2 | 3509902 | 14.5 x 6.4 x 0 | Steatite | prism | `1:+400-740-176+`; `2:+700-033+` |
| H-1346 | 4087.1;4087.2 | 2894900 | 10.2 x 6.4 x 0 | Steatite | prism | `1:+400-740-176+`; `2:+700-033+` |
| H-1347 | 4088.1;4088.2 | 1262896 | 0 x 7.6 x 0 | Steatite | prism | `1:+400-740-176+`; `2:+700-033+` |

The zero measurements and the odd H-1344 excavation ID are not interpreted. They are source-check flags.

## Public Search Result

The earlier packet-level public lead search checked 20 public endpoints: three fixed pages plus one Blogger Atom query per packet artifact. It found no checked-source public lead for H-1304, H-1344, H-1345, H-1346, or H-1347.

Fresh public-web searches on 2026-05-24 checked exact object IDs, object IDs with `Indus`/`Harappa`/`tablet`, object IDs with `+700-033+` and `400-740-176`, and site-limited searches against Indus Script & More and Bharatkalyan97. They did not surface object-level images, plate IDs, captions, source-grade side views, or even useful text-only leads for this five-object batch.

That negative result is limited to the checked public-web layer. It is not evidence that no source image exists in CISI, HARP, museum archives, library scans, or private research files.

## Why This Batch Matters

These five objects are not valuable because public leads exist. They are valuable because they are repeated source-dark instances of the same local `TAB:I` packet, `TAB:I` being an incised tablet class:

```text
1:+400-740-176+
2:+700-033+
```

They are the control batch for asking whether the `033` after-longer relation survives beyond publicly visible or text-mentioned cases. If they are skipped, the visible evidence layer becomes too dependent on objects that happen to have public pages. If they are acquired as a batch, the relation can be checked against repeated, less-public examples.

## Direct Source Request

For each object, the source request needs:

1. Plate or source image for both catalog rows.
2. Source citation, plate ID, image ID, or archive reference.
3. Confirmation that the two catalog rows are distinct physical sides, or a source explanation of the side convention.
4. Side-order basis: physical, photographic, editorial, arbitrary, or unresolved.
5. Direction basis for the short row: inscription order, impression order, catalog-normalized order, or unresolved.
6. Visibility of `2:+700-033+`.
7. Visibility and segmentation of `+400-740-176+`.
8. Visual check that the relevant sign is `033`, not `034`.
9. A recorded outcome for whether the catalog relation survives, fails, or remains unresolved after image-side check.
10. Dimension and shape recheck, especially all zero dimensions and the H-1344 excavation ID.

## Decision

Stop broad public-search expansion for this batch. The next useful action is direct source acquisition:

```text
status: requires_CISI_HARP_two_side_source_batch
public_object_image_leads: 0
public_text_only_leads: 0
source_validation_fields_filled: 0
```

## Interpretation Boundary

This audit accepts no side relation, physical side function, numerical value, metrological reading, sign meaning, phonetic value, language identity, or translation.

The only admissible output is a sharper direct-source request for five repeated source-dark packet objects.
