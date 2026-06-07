# Public CISI Routes for `002-Y` Branch-Gap Signs

Date: 2026-05-29

## Question

The `002-Y` partition source queue originally had route-level coverage for closure signs `817/820` and branch sign `390`, but not for branch signs `368`, `031`, and `220`. That made the candidate branch pole overdepend on `390`.

This note records a supplemental public-source acquisition pass for those three branch signs. It is infrastructure only.

## Method

The acquisition script reads `data/open_prototype/reports/campaign_002_y_partition_source_queue.csv`, keeps rows where:

```text
partition_class = posthoc_branch_pole
y_after_002 in 368/031/220
```

It searches public OCR from CISI India and CISI Pakistan Internet Archive page XML, constrains object IDs to the expected public CISI volume where possible, downloads the matching plate page, and crops broad context around the OCR label.

The volume constraint matters. An unconstrained OCR search falsely matched `B-1` to a side label on an unrelated Pakistan page. The current script routes `B-1` to CISI India page `n379`, where Banawali `B-1` is visible.

The label matcher also now rejects starred partial labels and split numeric suffixes. This demotes the earlier `H-44` route: the apparent hit was an OCR prefix/split-label trap from nearby `H-449`-style labels, not a clean `H-44` source route.

## Result

The target set contains 29 rows. The public route pass produced 32 route rows and 12 public CISI plate-route candidates:

| Sign | Target rows | Public route candidates | Object-ID blocked |
| --- | ---: | ---: | ---: |
| `368` | 11 | 5 | 1 |
| `031` | 9 | 4 | 1 |
| `220` | 9 | 3 | 0 |

Candidate routes:

| Sign | CISI | Public page | Text |
| --- | --- | --- | --- |
| `368` | `K-10` | CISI India `n336` | `+740-690-435-255-002-368-861-590-032-368+` |
| `368` | `B-1` | CISI India `n379` | `+090-740-220-002-368-550-821+` |
| `368` | `H-600` | CISI Pakistan `n332` | `+002-368-260+` |
| `368` | `M-12` | CISI India `n45` | `+740-390-590-233-002-368-202-892-371+` |
| `368` | `M-311` | CISI India `n112` | `+401-002-368-165+` |
| `031` | `H-389` | CISI Pakistan `n294` | `+740-405-590-235-002-031-480-625+` |
| `031` | `M-318` | CISI India `n114` | `+390-003-002-031-575+` |
| `031` | `M-678` | CISI Pakistan `n69` | `+740-752-006-503-236-806-002-031-502+` |
| `031` | `M-739` | CISI Pakistan `n87` | `+090-740-100-415-002-031-350-550-692+` |
| `220` | `M-29` | CISI India `n51` | `+740-055-240-235-806-002-220-455-503+` |
| `220` | `M-1427` | CISI Pakistan `n227` | `+484-140-002-220-627-615-906-388+` |
| `220` | `M-655` | CISI Pakistan `n61` | `+740-717-233-002-220-880-689+` |

After merging these route candidates into the source queue, the branch pole has 14 grade >= 2 route hooks instead of 2. The former route gap for `368/031/220` is closed at the route-inventory level:

| Branch sign | Rows | Terminal rows | Grade >= 2 route hooks |
| --- | ---: | ---: | ---: |
| `390` | 14 | 0 | 2 |
| `368` | 11 | 0 | 5 |
| `031` | 9 | 0 | 4 |
| `220` | 9 | 0 | 3 |

## Interpretation Boundary

These are route candidates only. They do not validate token order, physical direction, sign identity, sign meaning, phonetic value, language family, or translation.

The next gate is source-normalized proof: visual token boxing, physical side/direction checks, matched negatives, and source-family/copy review. Accepted claim count remains zero.

## Artifacts

- `data/open_prototype/tools/campaign_002_y_branch_gap_public_source_acquire.py`
- `data/open_prototype/reports/campaign_002_y_branch_gap_public_routes.csv`
- `data/open_prototype/reports/campaign_002_y_branch_gap_public_source_status.csv`
- `data/open_prototype/reports/campaign_002_y_branch_gap_public_source_summary.json`
- `tmp/002_y_branch_gap_public_source_acquisition/campaign_002_y_branch_gap_public_source_contact_sheet.jpg`
