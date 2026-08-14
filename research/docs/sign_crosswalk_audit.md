# Sign Crosswalk Audit

Date: 2026-05-29

## Verdict

This audit checks the crosswalk dataset's own hygiene: primary keys, references, evidence hashes, and counts. Passing means the scaffold is safe to build on. It says nothing about whether any mapping is true.

The provenance-tagged sign crosswalk scaffold passes dataset hygiene checks with caveats.

It is usable as infrastructure. It is not an accepted sign-list mapping, allograph table, phonetic table, semantic table, or decipherment artifact.

## Audit Artifacts

- `data/open_prototype/tools/audit_sign_crosswalk_dataset.mjs`
- `data/sign_crosswalk/audit_summary.json`
- `data/sign_crosswalk/audit_issues.csv`
- `data/sign_crosswalk/edge_pressure_summary.csv`

## Dataset Counts

| Table | Rows |
| --- | ---: |
| `sign_systems.csv` | 5 |
| `signs.csv` | 1,782 |
| `artifact_witnesses.csv` | 5,858 |
| `crosswalk_edges.csv` | 1,085 |
| `evidence_refs.csv` | 5 |
| `namespace_gates.csv` | 4 |
| `review_events.csv` | 2 |

Manifest counts match file counts.

## Hygiene Checks

| Check | Result |
| --- | ---: |
| duplicate primary keys | 0 |
| dangling sign/system/reference errors | 0 |
| evidence local-path/hash errors | 0 |
| accepted crosswalk edges | 0 |
| warning rows | 8 |

The only warnings are eight Lipi artifact witnesses with empty sign sequences:

- `lipi:364.1`
- `lipi:964.1`
- `lipi:979.1`
- `lipi:2369.1`
- `lipi:2371.1`
- `lipi:3836.1`
- `lipi:5230.1`
- `lipi:5534.1`

These are data-quality warnings, not mapping evidence.

## Crosswalk State

All 1,085 crosswalk edges have `accepted_for_analysis=false`.

Confidence distribution:

| Confidence | Edges |
| --- | ---: |
| `medium_low` | 14 |
| `low` | 21 |
| `very_low` | 154 |
| `source_metadata_only` | 896 |

Review status distribution:

| Review status | Edges |
| --- | ---: |
| `needs_image_or_authoritative_sign_list_validation` | 189 |
| `needs_primary_sign_list_validation` | 385 |
| `needs_icit_wells_validation` | 311 |
| `needs_m77_validation` | 200 |

## Highest-Pressure Edges

"Pressure" here means alignment support: how often two signs line up across sources. High pressure makes an edge worth reviewing first. It does not make the mapping true. These are the most useful review targets, not accepted mappings:

| Edge | Candidate mapping | Support | Counterexamples | Top share |
| --- | --- | ---: | ---: | ---: |
| `edge_00001` | `lipi_numeric:740 -> mayig_p:P324` | 73 | 0 | 1.000000 |
| `edge_00002` | `lipi_numeric:002 -> mayig_p:P122` | 57 | 2 | 0.950000 |
| `edge_00003` | `lipi_numeric:220 -> mayig_p:P050` | 27 | 2 | 0.931034 |
| `edge_00004` | `lipi_numeric:390 -> mayig_p:P086` | 25 | 0 | 1.000000 |
| `edge_00005` | `lipi_numeric:032 -> mayig_p:P145` | 20 | 1 | 0.952381 |
| `edge_00013` | `lipi_numeric:817 -> mayig_p:P385` | 12 | 0 | 1.000000 |
| `edge_00014` | `lipi_numeric:861 -> mayig_p:P385` | 12 | 0 | 1.000000 |

The paired `817/861 -> P385` pressure remains an allograph/source-policy question. It is not an accepted merge.

## Namespace Gates

Three namespace shortcuts remain blocked and one pressure gate remains open:

- blocked: Mayig `P041` is not automatically Parpola sign 41.
- blocked: Parpola article signs 60, 107, and 189 cannot be mapped by numeric ID shortcuts.
- blocked: Lipi `034` absence from current overlap is not falsification.
- open pressure, not accepted: Lipi `817` and `861` both align to Mayig `P385`.

## Use Boundary

Use this crosswalk to find review targets and to avoid repeating namespace mistakes. Do not use it as evidence for translations, phonetic values, sign meanings, language identification, or accepted sign equivalences.
