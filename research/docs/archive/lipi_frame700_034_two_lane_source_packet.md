# Lipi FRAME700 034 Two-Lane Source Packet

Date: 2026-05-25

## Question

This note turns an earlier finding into a concrete, ordered list of objects to request. FRAME700 is the project's label for short inscription rows built on sign `700`, such as `+700-034+`; the `034` candidate is the idea that sign code `034` behaves as a distinct choice in that slot. A packet is a bundled list of objects with the specific evidence each must supply. The question: what exact source packet follows from the matched-contrast stability result?

The answer is not one bigger pile. The current `034` candidate now needs two separate source lanes — separate evidence tracks, kept apart so a result in one does not lean on the other:

1. An independent low-copy lane that tests escape from copy-family pressure — the risk that objects in a set carry the same inscription because they are copies of one another, so counting them separately would double-count one act of writing.
2. A local contrast lane that tests the best `034` / `033` / `032` object-matched rows.

## Outputs

```text
data/open_prototype/tools/lipi_frame700_034_two_lane_source_packet.mjs
data/open_prototype/reports/lipi_frame700_034_two_lane_source_packet.csv
data/open_prototype/reports/lipi_frame700_034_two_lane_source_coding_sheet.csv
data/open_prototype/reports/lipi_frame700_034_two_lane_source_packet_summary.json
```

## Packet Size

```text
core triads: 8
optional triads: 1
participant rows: 27
core unique objects: 22
optional unique objects: 3
all unique objects: 25
row-level coding rows: 51
accepted decipherment claims: 0
```

Lane rows:

| Lane | Participant rows |
| --- | ---: |
| `independent_low_copy` | 12 |
| `local_contrast_stress` | 12 |
| `repeated_branch_check` | 3 |

Hook quality — a hook being an identifier in our own records that can be searched for in an archive:

| Hook grade | Count |
| --- | ---: |
| `catalog_or_archive_handle` | 15 |
| `excavation_plus_figure_hook` | 11 |
| `excavation_hook` | 1 |

## Core Objects

```text
H-212
H-353
H-771
H-789
H-854
H-893
H-925
H-930
H-983
H-1123
H-1772
H-1824
H-1842
H-1850
H-1883
H-1940
H-1943
H-2137
H-2204
H-2209
H-2211
H-2217
```

Optional repeated-branch objects:

```text
H-910
H-916
H-1294
```

## Required Source Decisions

Every row in the coding sheet has blank fields for:

```text
object identity
side distinctness
source side count
side order basis
direction basis
mirror status
FRAME700 visibility
source companion read
subtype separability
diagnostic strokes visible
allograph risk
source formula order
companion visibility
longer-row visibility
catalog/source agreement
duplicate or copy note
independent attestation
research decision
```

Source-grade means:

```text
object, side, row, direction, and sign contrast are source-visible and match the packet role
```

Downgrade means:

```text
source supports the object but leaves row, side, direction, or contrast unresolved
```

Kill means:

```text
wrong object, wrong row, invisible sign, collapsed contrast, failed side assignment, or unrecoverable duplicate/copy risk
```

## Consequence

The next serious move is not another broad corpus statistic. It is filling this packet from CISI (the Corpus of Indus Seals and Inscriptions, the standard photographic catalog), HARP (the Harappa Archaeological Research Project archive), Harappa archive images, library plates, or direct archive access.

The current `034` claim remains:

```text
034 is a source-targeted distributional residue inside the FRAME700 tablet side-mark system.
```

A residue is a leftover pattern that has survived the controls run so far, without being explained. This packet does not upgrade it. It defines the exact source evidence needed to kill, downgrade, or preserve it.
