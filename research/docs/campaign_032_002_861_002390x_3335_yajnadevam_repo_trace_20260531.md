# 002-390-X 3335.1 Yajnadevam repo trace

Date: 2026-05-31 America/Los_Angeles

Status: active source/provenance gate, not goal completion.

## Question

After the pinned raw-CSV check, does the upstream `yajnadevam/lipi` repository itself contain any source-generation trail, image mapping, git-history clue, or object bridge for `3335.1 / +740-205-032-002-390-590-032+`?

Accepted value, phonetics, language identity, function, sign meaning, and translation remain 0.

## Inputs And Outputs

- Runner: `data/open_prototype/tools/campaign_032_002_861_002390x_3335_yajnadevam_repo_trace_20260531.mjs`
- Source files: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_yajnadevam_repo_trace_20260531_source_files.csv`
- Target history: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_yajnadevam_repo_trace_20260531_target_history.csv`
- Image mapping: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_yajnadevam_repo_trace_20260531_image_mapping.csv`
- Occurrences: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_yajnadevam_repo_trace_20260531_occurrences.csv`
- Git history: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_yajnadevam_repo_trace_20260531_git_history.csv`
- Code paths: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_yajnadevam_repo_trace_20260531_code_paths.csv`
- Decisions: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_yajnadevam_repo_trace_20260531_decisions.csv`
- Summary: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_yajnadevam_repo_trace_20260531_summary.json`

Local clone:

- `tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo`
- HEAD: `b272ad99c253ba7fa1e4cd91f48cce31f6d02bf4`
- Repo history fetched unshallow; `main` and `experimental` remote heads inspected.

## Current Repo State

Current row:

| Field | Value |
|---|---|
| `id` | `3335.1` |
| `cisi` | `-` |
| `site` | `Unknown` |
| `excavation-idno` | `-` |
| dimensions | `29 x 29 x 0` |
| text | `+740-205-032-002-390-590-032+` |

Repo occurrence search found the target only in:

- `src/assets/data/inscriptions.csv`
- `glossing.csv`

`glossing.csv` is a derived Sanskrit-glossing layer and remains quarantined. After excluding `inscriptions.csv`, `glossing.csv`, and unrelated dictionary-line noise, there was no independent repository occurrence of `3335.1`, the exact sign string, or `sva-rava-sahana`.

## Image Mapping

The app imports `src/assets/data/seal_id_and_image_mapping.json` and renders images through `sealImages[item.cisi]`. The image-map generator builds keys from filenames like `M-940_a.jpg`, not metadata row ids.

| Key | Images | Decision |
|---|---|---|
| `3335.1` | none | no row-id image bridge |
| `-` | none | no dash-CISI fallback bridge |
| `M-939` | `M-939_a.jpg`, `M-939_1_A.jpg`, `M-939_2_A.jpg` | neighbor mapped |
| `M-940` | `M-940_a.jpg`, `M-940_a_bis.jpg` | neighbor/temptation mapped separately |
| `M-941` | `M-941_a.jpg` | neighbor mapped |

This rejects the row-order temptation again. The repository has an explicit `M-940` image key and a separate `M-940` row, so `3335.1` is not silently bridged by the missing row number between `M-939` and `M-941`.

## Git History

The exact sign string first appears in the repository at:

| Commit | Date | Subject | Decision |
|---|---|---|---|
| `0921d91d309621a292ba22bacce3f0f9c3ede929` | 2024-09-01T01:35:05-05:00 | `externalize inscriptions` | earliest repo appearance of exact text |
| `14b3421f33b1a6a38cee0d7ee54ad5669ef323dd` | 2024-09-03T20:19:27-05:00 | `auto-transliteration added` | schema migration to `3335.1` row shape |
| `92ec6a013fccc892b5063b9eada5d21b29a2a099` | 2026-01-09T23:44:29-06:00 | `L7 most` | current row blame touches Sanskrit/translation layer |

The old externalized row is useful because it preserved one source clue:

| Old field | Value |
|---|---|
| old `id` | `3335` |
| old `CISI` | blank |
| old `site` | `Unknown` |
| old `museum` | `Private collection` |
| old dimensions | `29.0 x 29.0 x 0.0` |
| old text | `+740-205-032-002-390-590-032+` |

This is not a binding source. It is an acquisition clue: ask for the private-collection object/citation behind old Lipi row `3335`, not for a generic Harappa/Mohenjo-daro catalog row.

## Decision

Status: `3335_yajnadevam_repo_history_private_collection_no_image_bridge_no_values`.

The repo trace does not rescue `3335.1`. It adds a bounded historical clue, not evidence:

- `3335.1` remains object-ID dark in current Lipi data.
- The repo image map has no `3335.1` key and no `-` fallback key.
- The app image path confirms that `cisi = -` rows cannot render an image through the normal Lipi mechanism.
- The older repo history preserves `museum = Private collection`, but no public object id, image, citation, excavation id, or source file.
- The `M-940` row-order bridge remains rejected.
- The derived Sanskrit/glossing layer remains quarantined.

Use the private-collection clue only to sharpen external acquisition. Do not promote the row, do not use the repo translation, and do not count it as a strict `032 -> 002-390` branch witness.
