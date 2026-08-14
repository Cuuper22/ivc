# Lipi FRAME700 034 Residue Validation Packet

Date: 2026-05-25

## Question

This note is a shopping list of objects to check against source images. FRAME700 is the project's label for short inscription rows built on sign `700`, such as `+700-034+`. An earlier test shuffled labels within matched blocks of similar objects — a null model, meaning a deliberately meaningless version of the data that shows how large an apparent effect chance alone produces. Most candidate effects died against it. One residue survived — a leftover pattern the controls did not explain:

```text
700-034+ / +034-700+ behaves differently inside FRAME700 after H-2218 through H-2239 are removed.
```

The question: what exact objects should be source-checked to decide whether this is a real sign/function contrast, an object-format association, or a transcription artifact?

The result is a packet: a bundled list of objects with the specific evidence each one must supply.

## Local Artifacts

```text
data/open_prototype/tools/lipi_frame700_034_residue_validation_packet.mjs
data/open_prototype/reports/lipi_frame700_034_residue_validation_packet.csv
data/open_prototype/reports/lipi_frame700_034_residue_validation_packet_summary.json
```

Inputs:

```text
data/open_prototype/reports/lipi_frame700_subtype_rows.csv
data/open_prototype/reports/lipi_short_mark_plate_public_leads.csv
```

This packet does not use model predictions as evidence. Prediction and contrast results are used only to select rows for source validation.

## Packet Scope

```text
input_rows: 353
h_series_rows_excluded: 22
selected_packet_rows: 141
selected_unique_artifacts: 140
034 positives: 93
033 siblings: 20
032 controls: 28
```

Subtype counts after removing H-2218 through H-2239:

| Subtype | Rows |
| --- | ---: |
| `033` | 136 |
| `032` | 102 |
| `034` | 93 |

The packet includes every non-H `034` row, then adds targeted `033` and `032` comparator rows. A control below is a comparison object used to check a target.

## Top 034 Validation Targets

### 1. 034 With `+002-861-416+`

First objects:

```text
H-2094
H-2097
H-2096
H-910
H-2095
```

Why this group matters:

```text
long_edge_frames: 002...416
long_token_set: 002;416;861
034 rows: 5/93
other FRAME700 subtypes: 0/238 in the no-H contrast table
```

This is the cleanest `034`-specific companion-family signature found so far. It is not enough for meaning. It is enough to demand plates.

The internal risk is also obvious:

```text
H-2094, H-2095, H-2096 share the same sequence family.
H-2097 reverses order as +034-700+.
H-910 gives the useful opposite side relation, short after longer.
```

Support condition:

```text
034 is visible and distinct, +002-861-416+ survives segmentation, and the association is not one copied/molded local batch.
```

Kill or downgrade:

```text
034 collapses into 033/032, +034-700+ is direction normalization, +002-861-416+ is missegmented, or the group is only a copy/family cluster.
```

### 2. 034 No-Longer / Small-Object Bucket

First objects:

```text
H-307
H-947
H-952
H-1828
H-1829
H-1830
H-1831
H-1907
H-788
H-953
H-2105
H-285
```

Why this group matters:

```text
no-H 034 context counts:
single_longer_text: 63
all_short_or_no_longer_text: 18
single_short_no_longer_text: 10
multiple_longer_texts: 2
```

This bucket tests whether `034` is only a companion-family phenomenon. If these objects are genuinely all-short or no-longer, the live explanation shifts toward object format, side function, or administrative format. If the "no longer text" status is just missing imaging, the bucket is weakened.

Support condition:

```text
all sides are actually imaged or accounted for, 034 is visible, object dimensions are real, and the h_10_13/small-area association survives.
```

Kill or downgrade:

```text
missing/unpublished sides explain the no-longer status, source dimensions do not match catalog bins, or 034 is just a damaged/allographic sibling.
```

### 3. 033 Sibling Branch

First objects:

```text
H-355
H-1302
H-1303
H-233
H-309
H-316
H-353
H-357
H-935
H-978
H-1304
H-1344
H-1345
H-1346
H-1347
```

Why this group matters:

```text
033 long token set 176;400;740: 19/136
outside 033: 11/195
```

`033` is the closest sibling branch. If `033` and `034` are not visually distinct in source-grade images, the `034` residue is dead.

Special risks:

```text
H-355 has two +700-033+ catalog rows and must be checked as a physical three-side case.
H-1302 and H-1303 have direction-note leads and may expose catalog direction normalization.
```

Support condition:

```text
033 remains visually distinct from 034/032 and +400-740-176+ survives source segmentation.
```

Kill or downgrade:

```text
033/034 collapse visually, the +400-740-176+ branch is duplicate-family only, or H-355 is a catalog duplication artifact.
```

### 4. 032 Controls

First controls:

```text
H-1771
H-1772
H-1773
H-1100
H-697
```

Why this group matters:

```text
032 control family: +740-031-001-140+
large-object control family: +740-904-240-002-817+
```

`032` stops this from becoming a two-way `033` versus `034` story. If `032` behaves the same way as `034` once sources are checked, the residue becomes much weaker.

## Public Source Check

Live exact web checks on 2026-05-25 for:

```text
H-2094, H-2097, H-910, H-307
site:harappa.com H-2094/H-2097/H-910/H-307
CISI H-2094/H-2097/H-910/H-307
+002-861-416+
700-034 / 034-700
```

Result:

```text
No source-grade object page, plate image, or museum/Harappa archive page surfaced for the top 034 objects.
The top 034 group should go straight to CISI/HARP/plate acquisition.
```

One current public paper separately flags the pair `700-034` as statistically noticeable:

```text
Ruhan Khanna and Louie Merriam, "A Computational Analysis of the Indus Script: Identifying Sign Functions in Logo-Syllabic Writing Systems", International Journal of Computer Applications, Volume 187, No.64, December 2025.
URL: https://www.ijcaonline.org/archives/volume187/number64/khanna-2025-ijca-926075.pdf
```

Quarantine — the paper is walled off from the evidence chain and may not be cited as support:

```text
Useful only as a literature-search pointer that 700-034 has been noticed.
Not included in the generated packet or summary JSON.
Not accepted as a semantic, phonetic, word, logogram, language, or translation reading.
```

So the effect on this project is narrow:

```text
700-034 gets no machine-readable evidence credit from this paper.
The source-validation packet still stands or falls on object images, side order, direction, and matched controls.
```

## Manual Fields Added

Every packet row includes blanks for:

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
validation_outcome
notes
```

Allowed validation outcomes:

```text
passes_source_check
fails_short_text_order
fails_segmentation
fails_side_relation
direction_unresolved
duplicate_or_family_only
source_unavailable
```

## Current Read

The live claim is:

```text
034 is a source-validation target for a possible distributional contrast inside the FRAME700 short-side formula.
```

The current best reading is still not linguistic. It is:

```text
object/form-context residue, possibly a side-mark subtype, possibly an administrative-format distinction.
```

## Boundary

No sign meaning, numerical value, metrological reading, semantic reading, phonetic value, language identity, or translation is accepted from this packet.
