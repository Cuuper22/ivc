# Directionality Route-Conditioned Control

Date: 2026-05-29

Status: failed promotion. Accepted claim increment: 0.

This note records a gate — a pass/fail test a result must clear before it can be promoted. The gate asks a tempting question: does the Vector 2 directionality candidate, the working result that Indus inscriptions score better in their stored order than reversed, get stronger when we keep only the rows we can actually see published photographs of? A route is a concrete path from a catalog row to a published image; here, a plate in the public CISI volumes (the Corpus of Indus Seals and Inscriptions, the primary published photographic record).

The gate uses the frozen public-route probe universe rather than the later manual crop triage:

```text
probe_id = directionality_public_route_probe_v1
priority_band in {P1_acquire_high_positive_source, P1_audit_reversed_anomaly}
queue_rank <= 80
```

That universe has 79 rows: 38 public CISI plate-route candidates and 41 rows not found in the public CISI OCR layer. This is still not source-normalized token evidence; it is a route-availability audit.

## Result

Stored-win share is the fraction of rows where the stored order scores higher than the reversed order.

| Subset | Rows | Stored wins | Reversed wins | Stored-win share |
| --- | ---: | ---: | ---: | ---: |
| Major-site harsh baseline | 324 | 274 | 35 | 0.845679 |
| Frozen top-79 route-probe universe | 79 | 53 | 26 | 0.670886 |
| Public-route rows | 38 | 26 | 12 | 0.684211 |
| No-public-route rows | 41 | 27 | 14 | 0.658537 |
| Public-route rows, source-page collapsed | 32 | 20 | 12 | 0.625000 |
| Public-route rows, `site|type|symbol|direction` collapsed | 21 | 13 | 8 | 0.619048 |
| Public-route rows, `site|type|material|symbol|direction` collapsed | 23 | 15 | 8 | 0.652174 |
| v2e possible/strong signband-like rows | 31 | 23 | 8 | 0.741935 |
| v2e possible/strong, page collapsed | 26 | 18 | 8 | 0.692308 |
| v2e possible/strong, `site|type|symbol|direction` collapsed | 17 | 11 | 6 | 0.647059 |
| v2e possible/strong, `site|type|material|symbol|direction` collapsed | 19 | 13 | 6 | 0.684211 |

Route availability does not rescue the source-normalization objection. The route subset starts below the 0.70 promotion threshold and weakens after source-page and source-register collapse. The v2e signband-like geometry slice briefly rises to 0.741935, but falls below threshold after page/source-register collapse.

## Nulls

A null is a run on deliberately scrambled data, used to see how often chance alone reproduces the observed result. The route-label null shuffles which rows are treated as public-route rows while preserving labels inside matched blocks. Four blocking policies were run for 5,000 iterations:

- `priority_band`
- `priority_band|site`
- `priority_band|site|type`
- `priority_band|site|type|symbol|direction|length_bin`

All four reproduce or exceed the observed public-route stored-win share and the observed route-minus-no-route difference with null >= observed share 1. The observed route share is only 0.684211 versus no-route share 0.658537, a difference of 0.025674.

## Decision

Decision: `failed_promotion_route_conditioned_subset_not_source_normalized_evidence`.

Fail reasons:

- public-route stored-win share below 0.70
- page-collapsed public-route share below 0.70
- source-register-collapsed public-route share below 0.70
- source-convention-collapsed public-route share below 0.70
- v2e source-register and source-convention collapsed shares below 0.70
- matched route-label nulls reproduce or exceed the observed route share

This kills a tempting shortcut: public route visibility is not source-normalized directionality evidence. It remains useful acquisition infrastructure, not a claim.

Main artifacts:

- `data/open_prototype/tools/effective_unicity_directionality_route_conditioned_control.mjs`
- `data/open_prototype/reports/effective_unicity_directionality_route_conditioned_control_summary.json`
- `data/open_prototype/reports/effective_unicity_directionality_route_conditioned_control.csv`
- `data/open_prototype/reports/effective_unicity_directionality_route_conditioned_null_summary.csv`
- `data/open_prototype/reports/effective_unicity_directionality_route_conditioned_null_iterations.csv`
