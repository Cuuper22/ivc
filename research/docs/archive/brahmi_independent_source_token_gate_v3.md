# Brahmi Independent Source-Token Gate v3

Date: 2026-05-30

This gate tests the most basic skeptic objection to the v2 Brahmi back-door run. The objection is simple: an apparent family agreement means little if it comes from the same crop counted twice or from a single object. So before any visual descent claim is shown to reviewers, we ask whether the agreement survives duplicate collapse and object independence.

It does not. All 83 v2 families are blocked before review.

## Artifacts

- `data/brahmi/tools/build_brahmi_independent_source_token_gate_v3.mjs`
- `data/brahmi/brahmi_independent_source_token_gate_v3.csv`
- `data/brahmi/brahmi_independent_source_token_gate_v3_summary.json`

Inputs:

- `data/brahmi/source_token_family_descent_summary_v2.csv`
- `data/brahmi/source_token_duplicate_collapse_audit_v2.csv`
- `data/brahmi/source_token_segments_v2.csv`

## Rule

A sign/orientation family is eligible for a future blind visual packet only if it has:

- at least 3 unique token hashes,
- at least 3 unique CISI objects,
- at least 3 unique source paths,
- unanimity after token-hash and CISI collapse,
- unchanged modal label after collapse,
- original shape-null share <= 0.01,
- original label-null share <= 0.01.

Note what passing would mean: not an accepted phonetic value, only permission to build a future blind panel with matched Brahmi negatives from the same date/manuscript band and comparable image geometry.

## Result

| Measure | Value |
| --- | ---: |
| Input family rows | 83 |
| Blocked before review | 83 |
| Review-packet eligible rows | 0 |
| Candidate-only rows | 0 |
| Accepted phonetic anchors | 0 |

Blocked-reason counts:

| Reason | Count |
| --- | ---: |
| shape null above 0.01 | 83 |
| label null above 0.01 | 72 |
| fewer than 3 unique CISIs | 58 |
| not unanimous after duplicate collapse | 53 |
| fewer than 3 unique token hashes | 36 |
| modal label changes after collapse | 23 |
| fewer than 3 unique source paths | 22 |

The v2 headline near-misses are all blocked:

| Sign | v2 label after collapse | Independence failure |
| --- | --- | --- |
| `817` | `dhya` / `dha` | 1 unique hash, 1 CISI |
| `527` | `ra` / `o` | 2 unique hashes, 1 CISI |
| `472` | `ra` | 1 unique hash, 1 CISI |
| `060` | `ka` / `ra` | 1 unique hash, 1 CISI |
| `061` | `ra` / `o` | 2 unique hashes, 1 CISI |

## Decision

Retracted as a descendant-script phonetic anchor. The v3 gate promotes no candidate to visual review and accepts no phonetic value.

What the gate still buys us: v3 stops repeated crops and one-object clusters from turning into visual-descent stories. The next valid Brahmi swing must either acquire more independent source-token witnesses or move to a real-token impostor forger that samples matched Indus token crops from other signs.
