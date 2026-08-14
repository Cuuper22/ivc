# 002-390-X 3335.1 Yajnadevam provenance recheck

Date: 2026-05-31 America/Los_Angeles

Status: active source/provenance gate, not goal completion.

## Question

Does the upstream unfiltered Yajnadevam `lipi` CSV contain a source bridge for local row `3335.1`, or only the same unbound metadata plus quarantined decipherment fields?

Target:

- Row: `3335.1`
- Text: `+740-205-032-002-390-590-032+`
- Local role: highest single-object `032 -> 002-390 -> non-692/non-125` matched-gate unlock if source-bound and sequence-valid
- Current crosswalk tier: `T3_quarantined_metadata`

Accepted value, phonetics, language identity, function, sign meaning, and translation remain 0.

## Inputs And Outputs

- Runner: `data/open_prototype/tools/campaign_032_002_861_002390x_3335_yajnadevam_provenance_recheck_20260531.mjs`
- Source files: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_yajnadevam_provenance_recheck_20260531_source_files.csv`
- Schema delta: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_yajnadevam_provenance_recheck_20260531_schema_delta.csv`
- Target comparison: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_yajnadevam_provenance_recheck_20260531_target_comparison.csv`
- Row-order neighborhood: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_yajnadevam_provenance_recheck_20260531_neighbor_rows.csv`
- Chunk rows: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_yajnadevam_provenance_recheck_20260531_chunk_rows.csv`
- Decisions: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_yajnadevam_provenance_recheck_20260531_decisions.csv`
- Summary: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_yajnadevam_provenance_recheck_20260531_summary.json`

Local downloads:

- `tmp/002390x_3335_yajnadevam_provenance_20260531/inscriptions_current.csv`
- `tmp/002390x_3335_yajnadevam_provenance_20260531/inscriptions_pinned_b272ad99.csv`
- `tmp/002390x_3335_yajnadevam_provenance_20260531/github_commit_main_path.json`

## Pinned Source

The floating `main` raw CSV was pinned to the GitHub path commit before use:

| Field | Value |
|---|---|
| Commit | `b272ad99c253ba7fa1e4cd91f48cce31f6d02bf4` |
| Commit URL | `https://github.com/yajnadevam/lipi/commit/b272ad99c253ba7fa1e4cd91f48cce31f6d02bf4` |
| Pinned raw URL | `https://raw.githubusercontent.com/yajnadevam/lipi/b272ad99c253ba7fa1e4cd91f48cce31f6d02bf4/src/assets/data/inscriptions.csv` |
| Raw SHA-256 | `c02e3d7bb74cf5abb11cc94f88d8d469e6acc5d6fad4b7153c02c43428f58d98` |
| Rows / columns | `5679 / 38` |

The current `main` download, the pinned commit download, and the existing local `tmp/lipi_current_inscriptions_20260526.csv` snapshot all have the same SHA-256. In plain terms: the upstream data has not changed, so this is a stable upstream recheck, not a changed-data rescue.

## Schema Result

The unfiltered source adds exactly three columns beyond the local filtered metadata table:

- `sanskrit`
- `translation`
- `notes`

Those are the columns already quarantined in the project notes. They are recorded as observed fields only. They are not labels, values, readings, translations, language evidence, or training targets.

The metadata/sign fields for `3335.1` match the local filtered row. The bridge fields remain absent:

| Field | Value |
|---|---|
| `cisi` | `-` |
| `site` | `Unknown` |
| `excavation-idno` | `-` |
| `image_ref_id` | blank |
| `artifact_id` in crosswalk | `-` |
| `provenance_tier` in crosswalk | `T3_quarantined_metadata` |

## Row-Order Check

The row still sits in a tempting sequence:

| Row | CISI | Text |
|---|---|---|
| `3334.1` | `M-939` | `+527-550+` |
| `3335.1` | `-` | `+740-205-032-002-390-590-032+` |
| `3336.1` | `M-941` | `+000-642-240-031-002-861+` |

This is a search clue only. It does not identify `3335.1` as a missing M-number, and it does not overturn the prior M-940 rejection.

## Chunk Recheck

The pinned source preserves the same local pressure:

| Chunk | Count | Use |
|---|---:|---|
| `740-205-032-002-390-590-032` | `1` | exact target only |
| `740-205-032-002` | `2` | M-143 plus target shared-prefix family |
| `032-002-390` | `2` | M-70 plus target matched `032` lane |
| `002-390-590` | `1` | target branch plus first tail |
| `390-590-032` | `7` | formula-family adversary |

The counts are useful for acquisition triage. They do not source-bind the target.

## Decision

Status: `3335_yajnadevam_pinned_provenance_recheck_no_source_bridge_no_values`.

The upstream Yajnadevam source does not rescue `3335.1`. It confirms that:

- The row is present in a pinned upstream CSV.
- The local filtered row did not accidentally drop an object/source bridge.
- The only dropped upstream fields are the already-quarantined decipherment fields.
- `3335.1` still has no CISI object id, no site/excavation bridge, no image reference, and no authoritative source binding.
- The row-order anomaly remains acquisition pressure only.
- The `032` matched-lane gate remains blocked.

The practical lesson: stop looping on local Lipi provenance. The next path for `3335.1` is external source acquisition or replacement strict `032` witness discovery.
