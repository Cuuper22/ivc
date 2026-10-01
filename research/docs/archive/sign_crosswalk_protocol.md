# Sign Crosswalk Protocol

Date: 2026-05-24

## Purpose

A sign crosswalk is a table that says which sign in one catalogue corresponds to which sign in another. The project needs one because different corpora and scholars use different sign inventories, different numbering systems, and different allograph policies, meaning different rules for when two visually distinct marks count as the same sign. Sign IDs are not universal. Every cross-source mapping is therefore a research object with its own evidence and its own failure modes, not clerical cleanup.

## Source Sign Systems

### Mahadevan / M77

Role:

- Historical baseline sign list and concordance.

Current status:

- Not yet locally acquired in machine-readable form.

Risk:

- Treating M77 sign numbers as universal will erase later allograph disputes and corpus updates.

### Parpola / CISI / `mayig`

Role:

- CISI-based artifact numbering and Parpola-style sign IDs such as `P121`.
- `mayig` adds feature vectors to distinguish allographic or graphemic details.

Current status:

- Open WIP corpus available through GitHub.
- Pinned first-sprint commit exists in [corpus_freeze_manifest.md](corpus_freeze_manifest.md).

Risk:

- Parpola allograph choices may merge distinctions relevant to another analysis.

### Wells / Fuls / ICIT

Role:

- Larger sign inventory and database tooling for positional, statistical, and geographic analysis.

Current status:

- Access-gated.

Risk:

- Cannot be treated as locally verified until access is granted or published tables are reproduced.

### Numeric `+740-540-002+` Style

Role:

- Appears in ICIT examples and the filtered `lipi` CSV.

Current status:

- Useful for broad sequence analysis after quarantine.

Risk:

- It must not be assumed to map one-to-one to Parpola `P###` notation without evidence.

## Crosswalk States

Every source-to-source mapping must carry exactly one state, so that uncertainty is visible instead of implied:

| State | Meaning |
| --- | --- |
| `exact` | Same grapheme under both authorities, supported by source documentation or image check. |
| `allograph` | Same grapheme class but feature/allograph differences remain important. |
| `split` | One source sign maps to multiple signs in another source. |
| `merge` | Multiple source signs map to one sign in another source. |
| `uncertain` | Candidate mapping exists but evidence is not enough. |
| `conflict` | Sources appear to disagree. |
| `unmapped` | No mapping attempted or found. |
| `not_applicable` | Mapping does not apply to the record or source. |

## Required Evidence For A Mapping

An `exact`, `allograph`, `split`, or `merge` mapping requires at least two evidence types:

- Same artifact image.
- Same published sign-list cross-reference.
- Same corpus documentation.
- Same positional distribution across enough examples.
- Same neighbor distribution across enough examples.
- Same graphemic feature description.

Visual similarity alone can propose a mapping, but it cannot settle one.

## Crosswalk Table Schema

```text
crosswalk_id
source_a
source_a_sign
source_b
source_b_sign
mapping_state
evidence_types
evidence_refs
example_artifacts
positional_similarity
neighbor_similarity
feature_notes
allograph_policy
confidence
counterexamples
review_status
```

## Allograph Policy

No single allograph policy is allowed to dominate all experiments, because a result that only appears under one merging scheme may be an artifact of that scheme.

Every structural experiment should run at least these conditions when data permit:

1. `raw_source`: signs exactly as the source encodes them.
2. `conservative_merge`: only mappings marked `exact` or very high-confidence `allograph`.
3. `expanded_split`: preserve feature-vector distinctions where available.
4. `paper_policy`: reproduce the sign policy of a target published paper.

If a result appears only under one policy, it is a claim about that policy, not about IVC.

An accepted `merge` edge is not automatically eligible for `conservative_merge`. The July 12 P086 and P385 clusters are controlling examples: `{390,405,406,407} -> P086` and `{817,861} -> P385` may be used only in explicit Mayig-policy lanes that preserve feature vectors; raw Lipi and conservative-merge runs keep those signs distinct.

## Mayig Feature Vector Handling

For `mayig`, preserve:

- Primary grapheme ID, e.g. `P086`.
- Default features: damage, line, uncertainty.
- Source-specific features such as branching factor, branch count, or branch direction.

Do not collapse feature vectors until the experiment says why.

## Direction And Mirroring

Mirrored signs are dangerous because a mirror image can mean several very different things, and the data alone rarely says which:

- Writing direction.
- Intentional allograph.
- Artifact production process.
- Distinct grapheme.
- Annotator choice.

Direction claims and allograph claims must be evaluated together. A mirrored sign should not be merged merely because it makes the sign inventory smaller.

## Acceptance Tests

A crosswalk entry can become analysis-grade only if:

- Its evidence references are recorded.
- It has no unresolved high-impact counterexample.
- It does not depend on a proposed translation.
- It improves or preserves structural prediction under held-out testing.

## First Crosswalk Workset

Start with artifacts that appear in multiple sources:

- `mayig` Mohenjo-daro IDs such as `M-1A`.
- ICIT example `M-1088` with text `+740-540-002-820+`.
- Filtered `lipi` rows with non-empty `cisi` IDs.

The first workset should be small enough for manual inspection. The goal is to expose mapping problems early, not to pretend the whole corpus is solved.

Current first workset:

- [Provisional crosswalk audit](provisional_crosswalk_audit.md)
- [Sign policy sensitivity](sign_policy_sensitivity.md)
- 136 strict `R/L` count-matched rows.
- 739 aligned positions.
- 189 `lipi` numeric signs and 160 `mayig` Parpola-style signs.
- One mapping is analysis-grade `exact`: `740 -> P324`, supported by 73/73 aligned positions and three labeled CISI 1 source panels under the July 12 source gate.
- `002 -> P122` is source-validated as a conflict: three labeled counterexamples block exactness despite 57/60 majority support.
- `{390,405,406,407} -> P086` is source-validated as a non-injective merge for explicit Mayig-policy analysis only. The reverse lane is 25:2:1:1 and eight labeled source panels preserve the visible feature variants.
- `032 -> P145` is source-validated as a conflict: M-143 reverses the dominant adjacent `032 002 / P145 P122` policy while Mayig preserves the full-height/half-height feature distinction.
- `{817,861} -> P385` is source-validated as a feature-preserving merge for explicit Mayig-policy analysis only. Roundedness keeps 817 round and 861 angular; M-177's local-803/P385 occurrence remains a contextual conflict, not a global remapping.
- Remaining high-priority review sign: `220 -> P050` (parked for inadequate defining-detail resolution).
