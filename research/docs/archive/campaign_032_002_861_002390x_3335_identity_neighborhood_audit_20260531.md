# 3335.1 identity-neighborhood audit for `002-390-X`

Date: 2026-05-31 America/Los_Angeles

Status: `3335_identity_neighborhood_no_local_bridge_external_source_required_no_values`.

## Purpose

The source-upgrade impact audit made `3335.1` the highest single-object matched-gate unlock: if it were source-bound and sequence-valid, it would pair with already-strict M-70 to create a strict `032 -> 002-390 -> {590,692}` branch split.

This audit asks a cheaper question first: can local metadata alone triangulate `3335.1` before we go hunting for an external source? It checks every local route we have — exact duplicate, row-order identity, formula-family source rows, no-object metadata siblings, `RAF` context, and same-profile source candidates.

Accepted value, phonetics, language identity, function, sign meaning, and translation remain 0.

## Inputs And Outputs

- Runner: `data/open_prototype/tools/campaign_032_002_861_002390x_3335_identity_neighborhood_audit_20260531.mjs`
- Input metadata: `data/open_prototype/lipi/metadata_filtered.csv`
- Target profile: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_identity_neighborhood_audit_20260531_target_profile.csv`
- Row-order neighborhood: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_identity_neighborhood_audit_20260531_row_order_neighborhood.csv`
- Exact/chunk matches: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_identity_neighborhood_audit_20260531_exact_and_chunk_matches.csv`
- No-object similar rows: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_identity_neighborhood_audit_20260531_no_object_similar_rows.csv`
- All similarity candidates: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_identity_neighborhood_audit_20260531_all_similarity_candidates.csv`
- `RAF` rows: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_identity_neighborhood_audit_20260531_raf_rows.csv`
- Same metadata profile: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_identity_neighborhood_audit_20260531_same_metadata_profile.csv`
- Decisions: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_identity_neighborhood_audit_20260531_decisions.csv`
- Summary: `data/open_prototype/reports/campaign_032_002_861_002390x_3335_identity_neighborhood_audit_20260531_summary.json`

## Target Profile

| Field | Value |
|---|---|
| Row | `3335.1` |
| Object | `-:3335.1` |
| Region/site | Other / Unknown |
| Type | `SEAL:S` |
| Symbol/cult | `Bull1:J` / `RAF` |
| Material/shape | unknown / square |
| Dimensions | `29 x 29 x 0` |
| Text | `+740-205-032-002-390-590-032+` |
| Structural role | `032 -> 002-390 -> 590 -> 032` |

## Results

| Test | Count/result | Decision |
|---|---:|---|
| Exact text rows | `1`, the target itself | No duplicate replacement. |
| Rows containing `390-590-032` | `7` | Real formula-family pressure, not identity. |
| Rows containing `032-002-390` | `2` | Only M-70 and `3335.1` carry the live `032` branch lane. |
| No-object rows in corpus | `661` | Large unresolved field; not usable by itself. |
| No-object rows passing similarity threshold | `8` | None supplies the target chunk except `3335.1`. |
| `RAF` rows | `57` | Context clue only. |
| `RAF` no-object rows | `3` | Still no source bridge. |
| Same type/symbol/cult/shape rows | `28` | Metadata profile is not unique and does not bind text. |

## Row-Order Check

The local row-order neighborhood still places `3335.1` between known Mohenjo-daro objects:

- `3334.1 / M-939`: `+527-550+`
- `3335.1 / -`: `+740-205-032-002-390-590-032+`
- `3336.1 / M-941`: `+000-642-240-031-002-861+`

The earlier `M-940` bridge remains rejected because `M-940` is already a separate local row and source-visible on the CISI Pakistan page checked in the previous gate. No alternate row-order neighbor supplies the target sequence or a usable object bridge.

## Chunk-Family Check

The seven `390-590-032` rows remain:

| Row | Object | Site | Text | Role |
|---|---|---|---|---|
| `2081.1` | L-139 | Lothal | `]390-590-032-002-880[` | chunk before `002` |
| `2116.1` | L-196 | Lothal | `]390-590-032-002-000[` | chunk before `002` |
| `2118.2` | L-198 | Lothal | `+740-390-590-032-002-000[` | chunk before `002` |
| `2448.1` | M-1739 | Mohenjo-daro | `+740-390-590-032-060-201+` | non-frame continuation |
| `3169.1` | M-746 | Mohenjo-daro | `+740-440-220-032-741-390-590-032+` | source-visible non-frame control |
| `3335.1` | unknown | Unknown | `+740-205-032-002-390-590-032+` | target |
| `3359.1` | M-965 | Mohenjo-daro | `+740-390-590-032-741-527+` | source-visible non-frame control |

This strengthens the formula-family warning. The chunk is real and it travels across objects and sites — which is exactly why it cannot identify `3335.1`.

## Public Refresh

Fresh public searches on 2026-05-31 for the exact target string and narrow variants did not recover a usable Harappa, Archive, source-plate, object, or museum bridge:

- `+740-205-032-002-390-590-032`
- `740-205-032-002-390-590-032 Indus`
- `3335.1 740-205 Indus`
- `390-590-032 M-746 M-965`
- `site:harappa.com 740-205-032-002-390-590-032`
- `site:archive.org 740-205-032-002-390-590-032`

## Decision

Current status: `3335_identity_neighborhood_no_local_bridge_external_source_required_no_values`.

Use `3335.1` as:

- Yes: the highest single-object acquisition target for matched `032` branch proof.
- Yes: a raw local continuing non-`125` pressure row.
- Yes: a formula-family danger marker because `390-590-032` appears across Lothal tags and Mohenjo-daro seals.
- No: a source-bound witness.
- No: a local duplicate of another object.
- No: an inferred M-number from row order.
- No: a grammar/function/value/translation result.

## Next Gate

The local routes are exhausted: `3335.1` now needs external source acquisition, not more local triangulation. The useful next moves are:

1. Find the source that produced cisi-less row `3335.1` or its original sign-list context.
2. Search for a strict replacement row with `032 -> 002-390 -> non-692/non-125`.
3. Keep `390-590-032` formula-family collapse active if `3335.1` ever becomes source-bound.

Run-control reminder: this is campaign progress inside the original moonshot decipherment goal, not a completion condition.
