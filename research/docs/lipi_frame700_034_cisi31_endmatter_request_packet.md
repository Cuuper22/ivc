# Lipi FRAME700 034 CISI 3.1 End-Matter Request Packet

Date: 2026-05-25

## Question

What exactly should be requested from CISI 3.1/end matter, HARP, or archive notes before the current `032/033/034` panel graph can be used as linguistic evidence?

This is a source-acquisition packet. It is not a decipherment claim.

## Inputs

- Local filtered metadata: `data/open_prototype/lipi/metadata_filtered.csv`
- Neighbor pressure result: `docs/lipi_frame700_034_neighbor_family_pressure.md`
- CISI 3.1 route recheck: `docs/lipi_frame700_034_cisi31_route_recheck.md`
- Script: `data/open_prototype/tools/lipi_frame700_034_cisi31_endmatter_request_packet.mjs`
- CSV: `data/open_prototype/reports/lipi_frame700_034_cisi31_endmatter_request_packet.csv`
- Summary: `data/open_prototype/reports/lipi_frame700_034_cisi31_endmatter_request_packet_summary.json`
- Team review: `docs/lipi_frame700_034_cisi31_request_team_review.md`

## Result

```text
request rows: 48
unique requested objects: 47
P0 rows: 7
P1 rows: 19
P2 rows: 22
core target rows: 9
exact-family comparator rows: 17
local-neighborhood comparator rows: 22
accepted readings: 0
```

## P0 Core Requests

| Object | Why it is P0 |
| --- | --- |
| `H-771` | Needs `A/A bis/A ter/A quater` same-side photo selection plus `B` resolved. |
| `H-1123` | Not page-addressable in the checked IA CISI vol. 1/2 OCR route; needs source-grade all-side labels. |
| `H-893` | Needs the meaning of `H-893 (1) A/B` resolved before any local row can be mapped to a source panel. |
| `H-925` | Needs `H-925 (1)/(2) A/B` and `bis/ter` witnesses resolved, with exact-family pressure carried. |
| `H-983` | Needs the source `C` side and B/C witnesses classified before the local two-row packet can be trusted. |
| `H-353` | Needs source `C` policy resolved inside the repeated `+400-740-176+ / +700-033+` family. |
| `H-2211` | Needs CISI 3.1/archive side labels and direction basis before acting as a `032` control. |

`H-789` and `H-930` are kept as P1 calibration controls, not solved readings.

## Family Rows

Exact-family comparanda are now explicit request rows, not prose:

```text
H-925 exact family comparanda: H-326; H-924
H-353 exact family comparanda: H-233; H-309; H-316; H-352; H-354; H-357; H-935; H-978; H-1302; H-1303; H-1304; H-1344; H-1345; H-1346; H-1347
```

Local-neighborhood comparanda are also explicit:

```text
H-771 neighborhood: H-766; H-768; H-770; H-776
H-893 neighborhood: H-891; H-892; H-894; H-895
H-983 neighborhood: H-978; H-979; H-980; H-982; H-984; H-985; H-987; H-988
H-2211 neighborhood: H-2206; H-2207; H-2208; H-2209; H-2213; H-2214
```

`H-978` appears twice: as an exact-family comparator for `H-353` and as a neighborhood comparator for `H-983`. That makes it a cross-pressure object, not a validation point.

## Fields Requested For Every Row

```text
CISI 3.1 end-matter row
excavation number
museum or owner
source of photograph
all side labels
all photo/impression labels
side-order basis
image or impression direction
copy/mold/duplicate/family notes
condition and preservation notes
material/shape/dimensions
findspot/period/phase/stratum/depth
```

## Decision Rule

A row can enter a source-normalized substitution test only after the source evidence answers the specific blocker for that row. Family and neighborhood rows do not create evidence by repetition; they are contamination controls.

If the source material shows that a local two-row packet suppresses a side, mixes a copy family, or collapses non-comparable source panels, the relevant `032/033/034` contrast must be downgraded or killed.

The team review adds the hard guardrail: CISI 3.1/end matter can stabilize object identity, side labels, photograph sources, and family pressure, but it does not validate the contrast unless it also gives source-visible sign separation, row-to-side mapping, direction control, and copy-family independence.

## Claim Status

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted side functions: 0
accepted source mappings from this packet: 0
```
