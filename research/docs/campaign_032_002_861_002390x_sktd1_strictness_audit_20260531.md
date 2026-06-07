# 002-390-X Sktd-1 strictness audit

Date: 2026-05-31 America/Los_Angeles

Status: active source gate, not goal completion.

## Question

Can the existing public Sktd-1 material be promoted from panel-bound pressure to strict token/order evidence for the `004 -> 002-390 -> 125 -> 820` lane?

Local row:

- Object: `Sktd-1`
- Row id: `3875.1`
- Site: Surkotada
- Local text: `+390-004-002-390-125-820+`
- Relevant lane: `004 -> 002-390 -> 125 -> 820`

No value, phonetics, language identity, function, sign meaning, or translation is accepted.

## Inputs

- Script: `data/open_prototype/tools/campaign_032_002_861_002390x_sktd1_strictness_audit_20260531.mjs`
- Evidence rows: `data/open_prototype/reports/campaign_032_002_861_002390x_sktd1_strictness_audit_20260531_evidence_rows.csv`
- Strictness tests: `data/open_prototype/reports/campaign_032_002_861_002390x_sktd1_strictness_audit_20260531_strictness_tests.csv`
- Decisions: `data/open_prototype/reports/campaign_032_002_861_002390x_sktd1_strictness_audit_20260531_decisions.csv`
- Summary: `data/open_prototype/reports/campaign_032_002_861_002390x_sktd1_strictness_audit_20260531_summary.json`

The audit consolidates the Sktd-1 side-pair recheck, the alpha blind key, token-boundary adjudication, and the source-upgrade impact scenarios. It also verifies that the five relevant image files are present and records their dimensions for reproducible visual review:

- `tmp/002390x_source_normalization/cisi_india_n397_w2000.jpg`
- `tmp/002390x_source_normalization/Sktd1_face_A_full_panel.jpg`
- `tmp/002390x_source_normalization/Sktd1_impression_a_full_panel.jpg`
- `tmp/002390x_source_normalization/Sktd1_face_A_signband.jpg`
- `tmp/002390x_source_normalization/Sktd1_impression_a_signband.jpg`

## Test Results

| Test | Result | Consequence |
|---|---|---|
| Object side-pair label visible | `pass` | CISI India leaf `n397` visibly binds `Sktd-1 A` and `Sktd-1 a` to the Surkotada row. |
| Top-band window compatible | `pass_downweighted` | The `002-390-125` window remains useful as visual pressure only. |
| Single-line full sequence | `fail_wrapped_layout` | The local six-token row is not visible as one clean source line. |
| Lower-field sign order | `fail_catalog_mediated` | The `125 -> 820` continuation order depends on catalog mediation. |
| Blind source-window preserved | `fail_boxed_compatible_only` | Existing blind/adjudication work stops at boxed-window compatibility. |
| Dual `004` split ready | `fail_not_ready` | No strict `004` matched-predecessor split can be claimed from the current public Sktd-1 panel. |

## Decision

Status: `sktd1_strictness_audit_wrapped_layout_blocks_dual004_no_values`.

Sktd-1 is source-panel side-pair visible, but not strict token/order evidence. The public plate is exhausted for promotion at this tier: full panels, top-band crops, blind-key evidence, and token-boundary adjudication all stop at boxed-window compatibility.

This matters because the source-upgrade impact audit showed that H-1993 alone does not unlock the `004` lane. The `004` lane needs both H-1993 and Sktd-1 strict, or an equivalent dual strict pair. Current Sktd-1 material does not supply that second strict side.

Accepted value, phonetics, language identity, function, sign meaning, and translation remain 0.

## Consequence

The next `004` move is not another reclassification of the same public Sktd-1 plate. It is one of:

1. Acquire H-1993 and a cleaner Sktd-1 source that explicitly fixes the wrapped order.
2. Find a replacement strict `004 -> 002-390 -> 125` witness.
3. Find a replacement strict `004 -> 002-390 -> non-125` witness that can be paired against Sktd-1 only after Sktd-1 strictness is independently solved.

Until then, the live positive model keeps `004 -> 002-390 -> 125 -> 820` only as pressure. It does not get grammar/function promotion.
