# 032-002 Branch-Tail Source Acquisition

Date: 2026-05-28

## Question

This note records an acquisition campaign: the work of finding published photographs for rows we previously knew only from catalog metadata. Signs in this corpus are numeric IDs. A "source route" is the traceable chain from a transcribed row back to its published page; a row is "source-visible" once that chain exists. CISI is the published photographic corpus of Indus inscriptions. A "packet" is a fixed bundle of rows assembled for one question.

The prior admissibility packet had one source-backed decisive continuation row, `M-49`, and four rows still stuck in source routing. This campaign asks:

```text
Can the decisive post-032-002 continuation rows be moved from metadata-only to public source-panel evidence?
```

## Data Stored

- Script: `tmp/run_032_002_branch_tail_source_acquisition.py`
- Route table: `data/open_prototype/reports/campaign_032_002_branch_tail_source_routes.csv`
- Crop manifest: `data/open_prototype/reports/campaign_032_002_branch_tail_source_crops.csv`
- Summary: `data/open_prototype/reports/campaign_032_002_branch_tail_source_acquisition_summary.json`
- Contact sheet: `tmp/032_002_branch_tail_source_acquisition/032_002_branch_tail_public_cisi_contact_sheet.png`

Mechanic validation: PASS. Checked Windows-safe side filenames, route counts, crop existence, distinct crop paths, and source leaf labels.

## Source Upgrades

Three decisive continuation rows are now public-CISI source-visible at row/panel level.

| row | branch-tail target | public source route | status change |
|---|---|---|---|
| `M-240` | `002-861-603` | CISI India IA leaf `n95`, printed p.60, Mohenjo-daro 240-242 seals | from local source-reference route to public source-panel route |
| `M-91` | `002-861-255-416` | CISI India IA leaf `n71`, printed p.36, Mohenjo-daro 89-94 seals | from local source-reference route to public source-panel route |
| `M-70` | `002-390-692` | CISI India IA leaf `n66`, printed p.31, Mohenjo-daro 70-72 seals | from needs source route to public source-panel route |

The script stores six panel crops: `A` and `a` for each object. Filenames use `face_A` and `impression_a` so Windows does not collapse side labels.

## What This Changes

Before this campaign, the only decisive adjacent continuation source-backed row was:

```text
M-49  002-300-350-032-190
```

The decisive source-visible set now includes:

```text
M-49   002-300-350-032-190
M-240  002-861-603
M-91   002-861-255-416
M-70   002-390-692
```

That matters linguistically. `861` is no longer just a catalog-order leaky closure in the adjacent `032-002` layer. It now has two public source-panel continuation witnesses, one in the target `240-220-032` frame and one in a non-target `A-220-032` frame. `390` also has a public source-panel continuation witness.

This does not produce a sign value or translation. It changes the grammar object from:

```text
one source-backed branch plus several metadata-only branches
```

to:

```text
multiple source-visible post-002 continuation branches requiring token-box and direction adjudication
```

A token box is a drawn rectangle claiming the exact extent of one sign on the image; direction adjudication decides which way the row reads.

## Metadata Conflict Notes

The public source-page headers expose a register warning — the register being the object class attached to a row, such as its animal icon and seal type:

| row | local icon/register | CISI page header |
|---|---|---|
| `M-240` | `Gaur` / `Trough` | `bison` |
| `M-91` | `Bull1:S` / `SAN` | `unicorn IV` |
| `M-70` | `Bull1:T` / `SAF` | `unicorn III` |

Do not let icon labels carry a linguistic claim here. They are useful as provenance/context metadata, but the next grammar test must be source-image and sign-order driven.

## Still Blocked

| row | branch-tail target | blocker |
|---|---|---|
| `M-1677` | `002-820-001-440-012` | no public CISI Vol. 1/2 plate route found; route is CISI 3.1 / HARP / Harappa archive by `DK11358130` |
| `3335.1` | `002-390-590-032` | no CISI object ID, site, source handle, or excavation number in local metadata |

The `820` continuation remains the biggest missing cell. Current source-visible evidence can support leaky `861` and branch-head `390`, but not source-normalized leaky `820`.

## Research Decision

Accepted:

- `M-240`, `M-91`, and `M-70` now have public source-panel routes and stored A/a crops.
- The post-`032-002` continuation campaign is no longer resting mostly on one `M-49` source witness.
- Source-visible branch grammar is live enough to justify token-level and direction-level adjudication across a cluster, not another one-sign detour.

Not accepted:

- token-level segmentation for the newly cropped rows
- exact local-to-source side mapping
- `861`, `390`, `603`, `255`, `416`, or `692` values
- phonetic readings, language identity, or translation

## Next Linguistic Experiment

Do not audit the packet again as the main activity. The next research unit is:

```text
Token-box and direction-adjudicate M-240, M-91, M-70, and M-49 as one branch-tail cluster.
```

Required output:

- physical order of `032-002-Y-tail` on each source panel
- whether A/a mirror the same sequence or expose side/direction ambiguity
- whether `861` behaves as a continuation-licensing sign or as a closure followed by a new unit
- whether `390` behaves like a branch-head class with terminal `692`
- whether the post-Y tails align with all-`002` tail families, especially `861->603` and `390->125/705/692`

Pass condition:

```text
At least two source-visible rows preserve a clean post-Y continuation after right-edge/direction checks, and the continuation tail belongs to a recurring family or a coherent positional slot.
```

Fail condition:

```text
The apparent continuation dissolves into side-label mismatch, damage, direction reversal, or unrelated second-unit segmentation.
```
