# 002-390-X matched-lane replacement scout

Date: 2026-05-31 America/Los_Angeles

This note is a search report. The campaign depends on two specific objects (H-1993 and `3335.1`) that we cannot yet tie to source images. This scout asked whether any other row in our local database could stand in for either of them. The answer is no — and recording that "no" is the point, because it proves the acquisition work on those two objects is necessary, not optional.

Status: `matched_lane_replacement_scout_no_local_replacement_witness_no_values`.

## Purpose

A "lane" here is a specific left-to-right sign pattern: which sign immediately precedes the pair `002-390`, and which sign follows it. The left-context radius scan narrowed the live branch question to two immediate-predecessor lanes:

- `004 -> 002-390 -> {095,125}`
- `032 -> 002-390 -> {590,692}`

This scout asks whether local metadata contains any replacement witness for either lane. A "witness" is a database row that attests a sign sequence; a replacement witness would be another adjacent `002-390-X` row with the same immediate predecessor, preferably source-visible (its source photograph can be inspected) or at least externally bindable, so the campaign is not forced to rely only on H-1993 or `3335.1`.

Accepted value, phonetics, language identity, function, sign meaning, and translation remain 0.

## Inputs And Outputs

- Runner: `data/open_prototype/tools/campaign_032_002_861_002390x_matched_lane_replacement_scout_20260531.mjs`
- Input metadata: `data/open_prototype/lipi/metadata_filtered.csv`
- Source-tier input: `data/open_prototype/reports/campaign_032_002_861_002390x_branch_sign_ecology_20260531_002390_frames.csv`
- Lane occurrences: `data/open_prototype/reports/campaign_032_002_861_002390x_matched_lane_replacement_scout_20260531_lane_occurrences.csv`
- Lane summary: `data/open_prototype/reports/campaign_032_002_861_002390x_matched_lane_replacement_scout_20260531_lane_summary.csv`
- Replacement targets: `data/open_prototype/reports/campaign_032_002_861_002390x_matched_lane_replacement_scout_20260531_replacement_targets.csv`
- Decisions: `data/open_prototype/reports/campaign_032_002_861_002390x_matched_lane_replacement_scout_20260531_decisions.csv`
- Summary: `data/open_prototype/reports/campaign_032_002_861_002390x_matched_lane_replacement_scout_20260531_summary.json`

## Local Metadata Result

The scout found `73` local `002` occurrences whose immediate predecessor is `004` or `032`.

Only `4` of those are adjacent `002-390-X` lane rows:

| Predecessor | All local `prev -> 002` occurrences | Adjacent `002-390-X` rows | Branches | Source state | Gate |
|---|---:|---:|---|---|---|
| `004` | `22` | `2` | `095:1; 125:1` | H-1993 is route/metadata pressure; Sktd-1 is public-panel downweighted. | `branch_split_non_strict_no_replacement` |
| `032` | `51` | `2` | `590:1; 692:1` | M-70 is strict visible; `3335.1` is metadata/object blocked. | `branch_split_partly_strict_no_replacement` |

There is no additional adjacent `002-390-X` row in local metadata for either live predecessor lane.

## Replacement Targets

Because no local replacement exists, the remaining upgrade targets are necessary, not optional:

| Target | Lane | Current role | Required upgrade |
|---|---|---|---|
| H-1993 / `744.2` | `004 -> 002-390 -> 095` | Non-`125` comparator, route-only via `H96-2769 / ICIT 744`. | Bind artifact image/data row, or replace with another strict `004 -> 002-390 -> non-125` row. |
| Sktd-1 / `3875.1` | `004 -> 002-390 -> 125-820` | `125` side of the split, public side-pair visible but wrapped/not strict. | Needs strict token/order proof only after a strict comparator exists. |
| `3335.1` | `032 -> 002-390 -> 590-032` | Non-`692` side of the split, object/source blocked and formula-family pressured. | Bind object/source, or replace with another strict `032 -> 002-390` branch alternative. |

M-70 does not need replacement for the `032` lane: it is already the strict visible `032 -> 002-390 -> 692` side. The blocked side is `3335.1`.

## Post-002 Head Controls Are Not Branch Replacements

Both live predecessors have many local `prev -> 002` rows where the post-`002` head — the sign right after `002` — is not `390`:

- `004`: `817:7; 861:5; 365:2; 390:2; 820:2; 031:1; 278:1; 705:1; 933:1`
- `032`: `820:11; 861:11; 817:9; 000:4; 390:2; <END>:1; 142:1; 144:1; 168:1; 252:1; 300:1; 368:1; 415:1; 454:1; 690:1; 717:1; 880:1; 892:1; 900:1`

Those rows help the anti-template argument at post-`002` head level — they show `002` is followed by many different signs, not one fixed formula. They do not replace the missing matched branch split inside adjacent `002-390-X`.

## Web Refresh

Fresh public searches on 2026-05-31 did not add a bindable source:

- H-1993 still surfaces through Singh et al. ESM2 as `ICIT 744 (H-1993)` in the relevant sign-string neighborhood, but no artifact image/caption bridge was found.
- Searches for `H96-2769 Figure 17.07`, `H96-2769Figure 17.07`, and `ICIT 744` did not improve beyond that route.
- Exact-string searches for `740-205-032-002-390-590-032` / `3335.1` did not recover a usable public object/source bridge.

Source used for the live H-1993 route: `https://www.harappa.com/sites/default/files/pdf/43539_2023_102_MOESM2_ESM.pdf`

## Decision

Current status: `matched_lane_replacement_scout_no_local_replacement_witness_no_values`.

This result does not demote the branch-tail object. It prevents a false next step.

The next matched-lane work is:

1. External acquisition for H-1993, or a new external/public row that gives strict `004 -> 002-390 -> non-125`.
2. External/source binding for `3335.1`, or a new external/public row that gives strict `032 -> 002-390 -> non-692/non-125`.
3. Separate repeated-`705` acquisition remains useful for branch-tail ecology (the study of which signs appear around the branch tail), but it is not currently a matched-lane replacement because neither `4237.1` nor M-1825 shares predecessor `004` or `032`.

Run-control reminder: this is campaign progress inside the original moonshot decipherment goal, not a completion condition.
