# Lipi FRAME700 034 Source Acquisition Manifest

Date: 2026-05-25

## Question

This note is the ordering and wording of the actual archive requests. FRAME700 is the project's label for short inscription rows built on sign `700`, such as `+700-034+`; the `034` residue is a leftover pattern involving sign code `034` that the controls run so far have not explained. An earlier packet — a bundled list of objects to check — names the objects. The question: what source images or plates should be acquired first, and what exact evidence must they provide?

## Local Artifacts

```text
data/open_prototype/tools/lipi_frame700_034_source_acquisition_manifest.mjs
data/open_prototype/reports/lipi_frame700_034_source_acquisition_manifest.csv
data/open_prototype/reports/lipi_frame700_034_source_acquisition_manifest_summary.json
```

Inputs:

```text
data/open_prototype/reports/lipi_frame700_034_residue_validation_packet.csv
data/open_prototype/lipi/metadata_filtered.csv
```

## Result

```text
acquisition_artifacts: 140
```

Primary buckets:

| Bucket | Artifacts |
| --- | ---: |
| `E_other_034_residue` | 55 |
| `D_032_control` | 28 |
| `C_033_400_740_176_sibling` | 19 |
| `A_034_no_longer_small_object` | 13 |
| `A_034_direction_reversal` | 12 |
| `B_034_400_740_176_bridge` | 8 |
| `A_034_002_861_416_companion` | 5 |

Source route counts:

| Route | Artifacts |
| --- | ---: |
| `direct_CISI_HARP_plate_request` | 128 |
| `use_text_lead_as_bibliographic_pointer_then_CISI_HARP_plate` | 9 |
| `verify_public_direction_lead_then_CISI_HARP_plate` | 2 |
| `inspect_public_image_pointer_then_CISI_HARP_plate` | 1 |

This is the important operational result:

```text
Most of the 034 work cannot move through public web images.
The next evidence layer is CISI/HARP/plate acquisition.
```

CISI is the Corpus of Indus Seals and Inscriptions, the standard photographic catalog of Indus objects; HARP is the Harappa Archaeological Research Project archive.

## Public Lead Update: 2026-05-25

Targeted public searches found one useful source lead for the original H-910/H-916/H-1294 triad — a triad being a set of three objects, one per sign code, matched closely enough to compare:

- `H-916`: Kenoyer 1997, [Excavations at Harappa 1994-1995](https://www.harappa.com/sites/default/files/pdf/Kenoyer1997_Excavations%20at%20Harappa%201994-1995%20New%20Perspective.pdf), Fig. `10.01`, accession `H94-2172`, table comparison to `H-916`, Vats plate `XCVI`, object `12516`. This is an image-bearing and table-bearing public lead, but it still needs reconciliation with the local hook `12516456` and row `1796.2`.
- `H-1302` and `H-1303`: Daggumati/Revesz 2021, [allograph identification article](https://www.nature.com/articles/s41599-021-00713-0), is a real direction/allograph warning because it names those tablets as mirrored-writing correction cases. It is not a plate-grade validation for the local rows.

No source-grade public object image or catalog entry was found in the targeted public layer for:

```text
H-910 / 10994470
H-1294 / PII-1499
H-2094 / H2001-5134 / Figure 47.02
H-2095 / H90-1688 / Figure 13.44 (d)
H-2096 / H95-2488
H-2097 / H2001-5193 / Figure 48.02
H-900 / 10059455/504
H-2173 / H96-3132 / Figure 20.06
H-925 / 3286512
H-930 / J30520
H-924 / 3286
H-2125 / H2000-4485 / Figure 42.03
H-1309 / 2257404
```

Exact public searches for the new independent rank-1 handles (`H-1850`, `H2001-5141`, `Figure 48.07`; `H-1842`, `H95-2416`, `Figure 26.07`; `H-1772`, `H2000-4437`, `Figure 39.05`) also returned no source-grade object-side image or plate hit. This keeps the acquisition route as archive/source request.

## First Request Batch

### 034 +002-861-416 Companion Bucket

A source hook is an identifier in our own records that can be searched for in an archive.

| Rank | CISI | Source hook | Short row | Longer row |
| ---: | --- | --- | --- | --- |
| 1 | `H-2094` | `H2001-5134`, `Figure 47.02` | `476.1:+700-034+` | `+002-861-416+` |
| 2 | `H-2097` | `H2001-5193`, `Figure 48.02` | `488.1:+034-700+` | `+002-861-416+` |
| 3 | `H-2096` | `H95-2488` | `665.1:+700-034+` | `+002-861-416+` |
| 4 | `H-910` | `10994470` | `1792.2:+700-034+` | `+002-861-416+` |
| 5 | `H-2095` | `H90-1688`, `Figure 13.44 (d)` | `518.1:+700-034+` | `+002-861-416+` |

Exact request:

```text
All sides of each object, side labels/order, image direction or impression direction, visible sign segmentation for both +700/+034 rows and +002-861-416+, object dimensions, and any source note on whether H-2094/H-2095/H-2096 are copied/molded/family-linked.
```

Preserves residue if:

```text
034 is visually distinct and the +002-861-416+ companion survives on at least one independent object outside a repeated family.
```

Kills or downgrades if:

```text
034 collapses into 033/032, +034-700+ is direction normalization, +002-861-416+ is missegmented, or the bucket is one copied local family.
```

### 034 No-Longer / Small-Object Bucket

First objects:

| Rank | CISI | Source hook | Short row |
| ---: | --- | --- | --- |
| 6 | `H-307` | `1963` | `1329.2:+700-034+` |
| 7 | `H-947` | `8650b493` | `1827.2:+700-034+` |
| 8 | `H-952` | `G257469` | `1832.2:+700-034+` |
| 9 | `H-1828` | `H97-3371`, `Figure 14.12` | `895.2:+700-034+` |
| 10 | `H-1829` | `H97-3365`, `Figure 14.13` | `890.2:+700-034+` |
| 11 | `H-1830` | `H96-3052`, `Figure 21.11` | `773.1:+700-034+` |
| 12 | `H-1831` | `H96-3051`, `Figure 21.10` | `772.1:+700-034+` |
| 13 | `H-1907` | `H96-2768`, `Figure 21.07` | `743.2:+700-034+` |

Exact request:

```text
All sides and any missing-side documentation. The source must decide whether "NO_LONGER_TEXT" means genuinely all-short/no-longer, or only incomplete image/corpus coverage.
```

Preserves residue if:

```text
Objects are complete, 034 is visible, and the small-object/no-longer pattern survives source dimensions and side checks.
```

Kills or downgrades if:

```text
No-longer status is missing imaging, catalog dimensions are shortcuts, or 034 is a damaged/allographic sibling.
```

## Required Evidence Per Object

Every request asks for:

```text
source citation or plate ID
all object sides
side labels and side order basis
inscription versus impression direction
visible 032/033/034 distinction
visible segmentation of longer-side rows
object dimensions and material/shape
copy/mold/family relation notes if present
```

## Control Request Batch

A control is a comparison object used to check a target. The first `033` sibling controls are:

| Rank | CISI | Source hook | Short row | Companion |
| ---: | --- | --- | --- | --- |
| 39 | `H-355` | `1274` | `1374.2:+700-033+`; `1374.3:+700-033+` | `+400-740-176+` |
| 40 | `H-1302` | `2366` | `4073.2:+700-033+` | `+400-740-176+` |
| 41 | `H-1303` | `2357879` | `4077.2:+700-033+` | `+400-740-176+` |
| 42 | `H-233` | `12544387` | `1260.2:+700-033+` | `+400-740-176+` |

The first `032` controls are:

| Rank | CISI | Source hook | Short row | Companion |
| ---: | --- | --- | --- | --- |
| 58 | `H-697` | `10965` | `1602.2:+700-032+` | `+740-904-240-002-817+` |
| 59 | `H-1100` | `-797` | `3959.2:+700-032+` | `+740-904-240-002-817+` |
| 61 | `H-1771` | `H2000-4375`, `Figure 36.03` | `371.1:+700-032+` | `+740-031-001-140+` |
| 62 | `H-1772` | `H2000-4437`, `Figure 39.05` | `400.1:+700-032+` | `+740-031-001-140+` |
| 63 | `H-1773` | `H2000-4392`, `Figure 37.08` | `383.1:+700-032+` | `+740-031-001-140+` |

For `H-355`, the specific request is whether the two `+700-033+` rows are two physical sides or a catalog duplication. For `H-1302` and `H-1303`, direction notes must be reconciled against the source image, not accepted from secondary discussion.

## Boundary

No sign meaning, numerical value, metrological reading, semantic reading, phonetic value, language identity, or translation is accepted from this manifest.
