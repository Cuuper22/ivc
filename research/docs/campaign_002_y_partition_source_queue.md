# `002-Y` Partition Source-Normalization Queue

Date: 2026-05-29

## Question

The post-hoc forger-resistant result says that broad all-`002` rows split into a high-terminal pole, `817/820`, and a continuation pole, `390/368/031/220`. The next admissibility question is not whether that split is statistically sharp in the Lipi-derived metadata layer. It is whether the split can be source-normalized without depending on one convenient branch sign.

This note records the acquisition queue for that gate. It is infrastructure only.

## Method

Input rows come from `data/open_prototype/reports/campaign_032_002_post_y_all_002_rows.csv`. The script keeps only `strict_complete_closed = true`, then deduplicates by:

```text
text_dedup_key + site + type + idx_002
```

That matches the strict broad all-`002` scope used by the post-hoc partition forger. The rows are joined to `data/open_prototype/reports/effective_unicity_directionality_source_queue_source_index.csv`, then assigned source grades:

| Grade | Label | Meaning |
| ---: | --- | --- |
| 4 | `source_visible_order_window_candidate` | Existing source-visible order-window candidate in prior reports. |
| 3 | `row_level_source_visible_candidate` | Row-level source-visible candidate, not token-boxed. |
| 2 | `local_image_or_public_route_candidate` | Local crop or public route exists, but token/order work remains. |
| 1 | `source_hint_only` | Catalogue/source hint exists, no usable public/local route yet. |
| 0 | `source_dark_or_unindexed` | No current indexed source route. |

The partition is:

| Class | Signs |
| --- | --- |
| Closure pole | `817`, `820` |
| Branch pole | `390`, `368`, `031`, `220` |
| Leaky background | `861` |

`861` is deliberately kept out of the strict post-hoc pole. It remains a closure-heavy descriptive stressor from the older fixed-bin model, not closure-pole support.

## Result

The queue contains 499 strict deduplicated all-`002` rows:

| Class | Rows |
| --- | ---: |
| `posthoc_closure_pole` | 174 |
| `posthoc_branch_pole` | 43 |
| `leaky_861_descriptive_not_posthoc_pole` | 119 |
| `other_y_after_002` | 163 |

The initial pole-level source coverage was uneven, but the supplemental public CISI route pass now gives every branch-pole sign at least one grade >= 2 route hook:

| Pole sign | Rows | Terminal rows | Source grade >= 2 |
| --- | ---: | ---: | ---: |
| `817` | 103 | 100 | 2 |
| `820` | 71 | 66 | 2 |
| `390` | 14 | 0 | 2 |
| `368` | 11 | 0 | 5 |
| `031` | 9 | 0 | 4 |
| `220` | 9 | 0 | 3 |

The immediate positive is that both closure-pole signs and all four branch-pole signs now have row-level or route-level hooks. The immediate problem has changed: the branch-side route gap is no longer the blocker, but none of the new `368/031/220` route candidates is token-boxed, direction-checked, or matched-negative tested.

Top branch acquisition targets:

| Rank | Sign | CISI | Text | Current status |
| ---: | --- | --- | --- | --- |
| 1 | `390` | `M-70` | `+226-032-002-390-692+` | Grade 4 source-visible order-window candidate; blind token-box promotion failed. |
| 2 | `390` | `M-38` | `+740-690-435-255-220-032-240-235-002-390-125-632-032+` | Grade 2 public-route/local-crop candidate. |
| 3 | `031` | `M-318` | `+390-003-002-031-575+` | Supplemental public CISI route candidate; not token-boxed. |
| 4 | `220` | `M-1427` | `+484-140-002-220-627-615-906-388+` | Supplemental public CISI route candidate; low-legibility quarantine in the blind packet. |
| 5 | `220` | `M-29` | `+740-055-240-235-806-002-220-455-503+` | Supplemental public CISI route candidate; blind-packet primary target. |
| 6 | `220` | `M-655` | `+740-717-233-002-220-880-689+` | Supplemental public CISI route candidate; blind-packet backup target. |
| 7 | `368` | `H-600` | `+002-368-260+` | Supplemental public CISI route candidate; visually messy, not packet-prioritized. |
| 8 | `368` | `M-12` | `+740-390-590-233-002-368-202-892-371+` | Supplemental public CISI route candidate; blind-packet primary target. |

The earlier `H-44` route has been demoted to `source_hint_only`: manual inspection showed the public crop was an OCR prefix/split-label trap from nearby `H-449`-style labels, not a clean `H-44` route.

## Interpretation Boundary

This queue does not validate source-normalized token order, physical direction, sign identity, sign meaning, phonetic value, language family, or translation.

What it does earn is a precise next gate: a source-normalized proof of the `817/820` versus `390/368/031/220` partition now has public route hooks on both sides, including `368`, `031`, and `220`. It still needs source-visible token boxing, physical side/direction checks, source-family/copy review, and matched controls before it can leave the metadata layer.

## Artifacts

- `data/open_prototype/tools/campaign_002_y_partition_source_queue.mjs`
- `data/open_prototype/reports/campaign_002_y_partition_source_queue.csv`
- `data/open_prototype/reports/campaign_002_y_partition_source_queue_by_sign.csv`
- `data/open_prototype/reports/campaign_002_y_partition_source_queue_summary.json`
- `docs/campaign_002_y_branch_gap_public_source_acquisition.md`
- `data/open_prototype/tools/campaign_002_y_branch_gap_public_source_acquire.py`
- `data/open_prototype/reports/campaign_002_y_branch_gap_public_source_summary.json`
