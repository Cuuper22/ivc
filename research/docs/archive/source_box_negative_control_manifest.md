# Source-Box Negative-Control Manifest

Date: 2026-05-29

Status update: superseded by `docs/source_box_blind_adjudication_results.md`. The blind packet created here was scored, and the source-visible `032-002-Y` candidate failed the forger gate.

## Purpose

This note records the building of a trap for the project's own claim. It exists because a reviewer looking at a blurry seal photograph can find almost anything they are hoping for, so we mix in objects that definitely lack the target and see whether the reviewer calls those too.

Terms first. A "source-box" is a box drawn on a published object photograph around the signs a reviewer thinks they see. "Source-visible" means the object exists in a published plate image, not just a catalog transcription. The claim under test concerns the sign group `032-002-Y`, where `032` and `002` are Lipi catalog sign codes and `Y` stands for whatever sign follows. A "negative control" is an object chosen because its catalog text does not contain that group. The "forger" is this project's standard adversary test — here, seeing whether the review method produces the target from material that cannot contain it. A "gate" is a recorded checkpoint that either lets a claim through or blocks it. A "manifest" is the list of which objects went into the packet.

This artifact builds the next forger gate for the source-visible `032-002-Y` packet candidate. It asks a narrower question than the catalog analysis:

Can a blinded reviewer or model be tricked into calling a same-line `032-002-Y` packet in source images whose catalog text does not contain that packet?

The script does not adjudicate sign shapes and does not compute a false-positive rate. It produces the matched negative-control manifest, copies available images into neutral filenames, and writes the truth key separately.

## Generated Files

- `data/open_prototype/tools/source_box_negative_control_manifest.mjs`
- `data/open_prototype/reports/source_box_negative_control_candidates.csv`
- `data/open_prototype/reports/source_box_negative_control_summary.json`
- `data/open_prototype/reports/source_box_blind_adjudication_packet.csv`
- `data/open_prototype/reports/source_box_blind_adjudication_key.csv`
- `tmp/source_box_blind_packet_v1/`

Run:

```powershell
node data\open_prototype\tools\source_box_negative_control_manifest.mjs 20260529 12
```

## Candidate Pool

The manifest excludes all 25 rows from the `032-002-Y` route list — the objects already traced to a real source record for the claim — and scans strict Lipi numeric-clean rows for three negative classes:

| Negative class | Candidate positions |
| --- | ---: |
| `negative_002_y_prev_not_032` | 503 |
| `negative_032_next_not_002` | 297 |
| `negative_220_032_next_not_002` | 27 |

Total negative candidate positions: 827.

Unique negative candidate CISI IDs: 761.

## Source Availability

| Availability tier | Candidate positions |
| --- | ---: |
| local image hit | 23 |
| source panel graph | 1 |
| Mayig overlap only | 74 |
| metadata only | 729 |

Local image-backed negative positions by class:

| Negative class | Local image-backed positions |
| --- | ---: |
| `negative_002_y_prev_not_032` | 19 |
| `negative_032_next_not_002` | 4 |
| `negative_220_032_next_not_002` | 0 |

The last line matters. The rarest and most valuable negative class, `220-032` not followed by `002`, exists in metadata but currently has no local image-backed controls. That is a real blocker for a fully matched source-box false-positive rate against the `A-220-032` lane — one of the separate lines of inquiry the project keeps apart so they cannot contaminate each other.

## Blind Packet v1

The packet is "blind" because the reviewer cannot tell which images are targets and which are controls; the files are "neutral" because their names carry no information. The blind packet contains 20 neutral image files:

| Truth class | Rows |
| --- | ---: |
| positive source-visible `032-002-Y` | 8 |
| `negative_002_y_prev_not_032` | 10 |
| `negative_032_next_not_002` | 2 |

The packet CSV hides catalog text and original filenames. The key CSV contains the truth labels, catalog text, and original image paths. Site/type/symbol metadata remains visible because this packet is for matched source-box review, not a fully anonymous perception experiment.

## Claim Status

This advanced the source-visible `032-002-Y` candidate from "needs a matched-negative forger" to "matched-negative forger packet exists." The packet has since been adjudicated and failed; see `docs/source_box_blind_adjudication_results.md`.

Accepted claim count remains zero.

The next acceptance gate is explicit:

1. Score `source_box_blind_adjudication_packet.csv` without reading the key.
2. Mark whether each neutral image is judged to contain a source-visible same-line `032-002-Y` packet.
3. Compare against `source_box_blind_adjudication_key.csv`.
4. Report false positives by negative class. Any nontrivial false-positive rate retracts or narrows the source-visible packet claim.
