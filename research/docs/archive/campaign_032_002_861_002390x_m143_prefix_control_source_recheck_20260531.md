# `032-002-861` / `002-390-X` M-143 Prefix-Control Source Recheck

Date: 2026-05-31

This note records one narrow check inside the `032-002-861` / `002-390-X` campaign. The check asks whether seal M-143 can serve as a control object for the campaign's real target. A "control" here means a seal that shares part of the target's sign sequence, so the two can be compared. Before we can use M-143 that way, it must be "source-bound" — tied to an actual photograph of a source publication page, not just to a transcription in our database.

Status: active source-control gate, not goal completion. (A "gate" is a check that must pass before evidence is allowed into the analysis.)

Current status string: `m143_prefix_control_source_panel_found_not_3335_bridge_no_values`

## Question

After the `3335.1` acquisition packet, M-143 was the live local control because it shares the exact left prefix `740-205-032-002` with the target row but then branches away from it:

- M-143: `+740-205-032-002-252-840+`
- `3335.1`: `+740-205-032-002-390-590-032+`

The question was simple: is M-143 still source-dark (no source page bound to it), or can it be source-bound well enough to serve as a prefix-family control while `3335.1` remains unbound?

## Source Route

The "source route" is the chain of pointers that leads from our database row to a real published image. The local CISI India OCR route resolves M-143 to page object `India_0080.djvu`, with a duplicated OCR block at `India_0511.djvu`. The public archive leaf is:

`https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India/page/n80_w2000.jpg`

Local source page:

`tmp/002390x_m143_prefix_control_20260531/cisi_india_n080_w2000.jpg`

Printed header on the page:

`'unicorn' IV / SEALS MOHENJO-DARO 139-144 / 45`

The page visibly contains both `M-143 A` and `M-143 a`. The source panel and signband (the strip of the seal that carries the inscription) are visible. But this audit does not perform blind numeric token-box adjudication — the stricter step where sign boundaries are judged from the image alone, without looking at the claimed reading.

## Crops

Source-derived crops:

- `tmp/002390x_m143_prefix_control_20260531/derived/M143_face_A_full_panel_label_x2.jpg`
- `tmp/002390x_m143_prefix_control_20260531/derived/M143_face_A_signband_x2.jpg`
- `tmp/002390x_m143_prefix_control_20260531/derived/M143_impression_a_full_panel_label_x2.jpg`
- `tmp/002390x_m143_prefix_control_20260531/derived/M143_impression_a_signband_x2.jpg`

## Local Transcription State

Our local metadata file, `data/open_prototype/lipi/metadata_filtered.csv`, gives M-143 as:

| field | value |
|---|---|
| row | `2670.1` |
| object | `M-143` |
| site | `Mohenjo-daro` |
| type | `SEAL:S` |
| symbol | `Bull1:J` |
| cult | `RAF` |
| material | `Steatite` |
| shape | `square` |
| direction | `R/L` |
| dimensions | `23.9 x 24.1 x 7.6` mm |
| text | `+740-205-032-002-252-840+` |

The crosswalk — the table that links independent transcription systems to the same object — has two relevant witness rows (a "witness" is one independent record of the object's sign sequence):

- `mayig:M-143A`: `P324 P082 P122 P145 P170 P349`, `T2_open_wip`.
- `lipi:2670.1`: `740 205 032 002 252 840`, `T3_quarantined_metadata`.

This is enough for source-route control context. It is not enough, by itself, to promote a strict numeric reading.

## Shared-Prefix Split

The full shared prefix `740-205-032-002` has two local rows in this gate:

| row | object | branch after `002` | continuation | source state |
|---|---|---|---|---|
| `2670.1` | `M-143` | `252` | `252 840` | `public_cisi_india_n80_panel_visible` |
| `3335.1` | `-` | `390` | `390 590 032` | `metadata_only_unbound` |

This makes `3335.1` a better-controlled target: we now have a bound neighbor that shares its prefix but not its branch. If `3335.1` is ever acquired, it must be checked as a shared-prefix branch against M-143 and the wider `390-590-032` formula family. Until then, M-143 does not bind the target.

## Decisions

1. `m143_source_panel_found`: archive leaf `n80` source-binds the M-143 panel route.
2. `m143_not_3335_identity_bridge`: M-143 branches to `252-840`, while `3335.1` claims `390-590-032`. The two are not the same object, so M-143 cannot stand in for `3335.1`.
3. `numeric_token_strictness_not_claimed_here`: source panels and signbands are visible, but no blind numeric token-box adjudication is accepted from this audit.
4. `no_reading_no_value_no_translation`: accepted value, phonetics, language identity, function, sign meaning, and translation remain `0`.

## Generated Artifacts

Runner:

`data/open_prototype/tools/campaign_032_002_861_002390x_m143_prefix_control_source_recheck_20260531.mjs`

Reports:

- `data/open_prototype/reports/campaign_032_002_861_002390x_m143_prefix_control_source_recheck_20260531_source_route.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_m143_prefix_control_source_recheck_20260531_files.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_m143_prefix_control_source_recheck_20260531_metadata.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_m143_prefix_control_source_recheck_20260531_shared_prefix_rows.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_m143_prefix_control_source_recheck_20260531_witness_rows.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_m143_prefix_control_source_recheck_20260531_decisions.csv`
- `data/open_prototype/reports/campaign_032_002_861_002390x_m143_prefix_control_source_recheck_20260531_summary.json`

## Run-Control Note

This closes one source-control question inside the active `032-002-861` / `002-390-X` campaign. It is not a decipherment result and not a goal-completion condition.
