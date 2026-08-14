# 3335.1 private-collection cluster probe

Date: 2026-05-31 America/Los_Angeles

Status: `3335_private_collection_cluster_two_rows_no_bridge_no_values`.

## Question

The Yajnadevam/Lipi repo trace found one historical clue for the `3335.1` branch-lane target: old row `3335` carried `museum = Private collection` in the first externalized CSV layer.

This probe asks a follow-up question: is that clue part of a larger source cluster — other rows from the same collection — that could identify a source holder, an image route, or a companion object for:

`3335.1 / +740-205-032-002-390-590-032+ / 29 x 29 / SEAL:S / Bull1:J / RAF`.

Accepted value, phonetics, language identity, function, sign meaning, and translation remain 0.

## Inputs And Outputs

- Runner: `data/open_prototype/tools/campaign_032_002_861_002390x_3335_private_collection_cluster_probe_20260531.mjs`
- Old source commit: `0921d91d309621a292ba22bacce3f0f9c3ede929` / `externalize inscriptions`
- Schema commit: `14b3421f33b1a6a38cee0d7ee54ad5669ef323dd` / `auto-transliteration added`
- Repo clone: `tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo`

Reports:

- `data/open_prototype/reports/campaign_032_002_861_002390x_3335_private_collection_cluster_probe_20260531_private_cluster.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_3335_private_collection_cluster_probe_20260531_image_map_keys.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_3335_private_collection_cluster_probe_20260531_repo_occurrences.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_3335_private_collection_cluster_probe_20260531_history.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_3335_private_collection_cluster_probe_20260531_decisions.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_3335_private_collection_cluster_probe_20260531_summary.json`

## Result

The old externalized CSV contains exactly two `Private collection` rows:

| Old id | Current id | Current object | Old/current site | Symbol/cult | Dimensions | Text | Image map |
|---|---|---|---|---|---|---|---|
| `3118` | `3118.1` | `-:3118.1` | `Unknown` / `Unknown` | `Gaur` / `Trough` | `21 x 21 x 0` | `+520-070-255-832-220-003-853+` | none |
| `3335` | `3335.1` | `-:3335.1` | `Unknown` / `Unknown` | `Bull1:J` / `RAF` | `29 x 29 x 0` | `+740-205-032-002-390-590-032+` | none |

The only sibling row is `3118/3118.1`. It does not help bind the target:

- It has blank old `CISI` and dash current `cisi`.
- It remains `Unknown` site in current data.
- It has no `3118`, `3118.1`, `-:3118.1`, or dash image-map key.
- It appears in the current repo only in `inscriptions.csv` and the derived quarantined `glossing.csv`.

For the target itself, checked image-map keys `3335`, `3335.1`, `-:3335.1`, and `-` all have zero mapped images.

Manual exact public searches for the target sequence, the sibling sequence, and the quarantined gloss strings produced no usable source bridge. That negative search is a guardrail only. The one piece of positive evidence is still the repo-history field `museum = Private collection` — nothing more.

## Decision

`Private collection` is now a two-row acquisition clue, not source evidence.

The result slightly sharpens the external ask:

- Ask for the private-collection source behind old Lipi row `3335`.
- Mention that old Lipi row `3118` is the only sibling in the same historical museum field, but it does not currently identify the collection.
- Do not use `3118.1` as a bridge or as independent support for `3335.1`.
- Do not use the quarantined Sanskrit/glossing layer.
- Do not count `3335.1` as a strict `032 -> 002-390 -> 590` branch witness.

Current status: `3335_private_collection_cluster_two_rows_no_bridge_no_values`.
