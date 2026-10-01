# 032-002 Post-Y Tail Family Campaign

Date: 2026-05-28

## Question

This note tests a prediction made by the previous campaign. Signs in this corpus are numeric IDs; `Y` names whichever sign follows `002`. A "branch head" is a sign that opens further material rather than ending the row; a "closure" sign ends it. A "tail" is the material that follows `Y`; a "tail family" is a tail that recurs across independent rows rather than appearing once. "Strict dedup" means identical texts collapse to one unit of evidence, so copies cannot count twice.

If the post-`002` split is grammatical, branch-head signs should license patterned continuation material. This campaign asks whether the material after Y forms tail families or just random leftover row material.

## Inputs

- Parent rows:
  - `campaign_032_002_post_y_all_002_rows.csv`
  - `campaign_032_002_post_y_branch_rows.csv`
- Script: `tmp/run_032_002_post_y_tail_families.py`
- Current mechanic status: pending validation

Outputs:

- `data/open_prototype/reports/campaign_032_002_post_y_tail_family_summary.csv`
- `data/open_prototype/reports/campaign_032_002_post_y_tail_family_instances.csv`
- `data/open_prototype/reports/campaign_032_002_post_y_tail_next1_matrix.csv`
- `data/open_prototype/reports/campaign_032_002_post_y_tail_family_summary.json`

Mechanic validation: PASS.

## Counts

| scope | rows |
|---|---:|
| all strict dedup `002-Y` | 499 |
| adjacent strict dedup `032-002-Y` | 32 |
| continuing post-Y instances exported | 207 |

## All-002 Tail Families

Closure-heavy signs mostly close, but their continuations are not identical:

| Y | class | rows | continuing | repeated tail pressure |
|---|---|---:|---:|---|
| `817` | hard closure | 103 | 3 | no repeated full tails |
| `820` | leaky closure | 71 | 5 | `741` appears twice as next sign |
| `861` | leaky closure | 119 | 24 | `603` appears 3 times; `533-717` appears twice |

Branch-head signs continue by definition in this layer and show stronger next-sign preferences:

| Y | rows | continuing | top next signs | interpretation |
|---|---:|---:|---|---|
| `390` | 14 | 14 | `125:4`, `705:2` | real branch-head candidate; strongest recurring tail pressure |
| `368` | 11 | 11 | `260:2`, then singletons | branch-head candidate with weak recurrence |
| `031` | 9 | 9 | `892:2`, then singletons | branch-head candidate with weak recurrence |
| `220` | 9 | 9 | `455:4`, `065:3` | branch-head candidate with strong next-sign split |
| `900` | 4 | 4 | all singletons | branch-head candidate, sparse |
| `300` | 1 | 1 | `350` | target branch singleton |

The strongest all-`002` tail families right now are:

```text
002-390-125...
002-390-705
002-220-455...
002-220-065...
002-861-603
002-861-533-717
```

These are not translations. They are candidate continuation families to source-check and expand.

## Adjacent 032-002 Tail Behavior

Inside the 32 strict dedup adjacent `032-002` units:

| Y | class | rows | continuing tails |
|---|---|---:|---|
| `817` | hard closure | 4 | none |
| `820` | leaky closure | 7 | `001-440-012` once |
| `861` | leaky closure | 9 | `255-416` once; `603` once |
| `390` | branch head | 2 | `692`; `590-032` |
| `300` | branch head | 1 | `350-032-190` |
| `368` | branch head | 1 | `906-329` |
| `900` | branch head | 1 | `285` |

Result:

```text
032-002 confirms closure/branch behavior, but not yet a repeated 032-002-specific tail family.
```

The adjacent layer is too sparse. It says which rows decide the question, not yet what the post-Y material means.

## Linguistic Read

The branch-head model survives:

```text
002 - closureY               -> packet closes
002 - branchY - tail          -> packet continues
```

But the semantic layer is only beginning. The all-`002` field has recurring tail pressure after `390`, `220`, and `861`; the adjacent `032-002` subset mostly has singletons. That means the next move is not to assign values. It is to expand the branch-tail families and source-check the exact rows where branch behavior is doing work.

Current best function model:

| component | function hypothesis |
|---|---|
| `002` | tail linker / boundary before a classed exponent |
| `817` | hard closure exponent |
| `820` | closure exponent with rare extension |
| `861` | closure exponent with licensed administrative/code extension |
| `390`, `220`, `368`, `031`, `900`, `300` | branch heads into further coded material |

## Decisions

Accepted:

- Branch-head signs have non-random next-sign pressure in the all-`002` field.
- Adjacent `032-002` supports the closure/branch split, especially `817` as closure and `300/390/368/900` as continuations.
- No repeated adjacent `032-002` tail family is strong enough yet to assign a semantic field.

Rejected:

- Post-Y tails as already translated administrative codes.
- `861-603`, `820-001-440-012`, or `300-350-032-190` as known meanings.
- Any phonetic value, language identity, or sign reading.

## Next Campaign

Run a source-normalized branch-tail expansion:

1. Pull every strict row for the strongest all-`002` tail families:
   - `002-390-125`
   - `002-390-705`
   - `002-220-455`
   - `002-220-065`
   - `002-861-603`
   - `002-861-533-717`
2. Compare site/type/symbol/class distribution for each tail family.
3. Source-check the adjacent `032-002` decisive rows:
   - `M-240`: `002-861-603`
   - `M-91`: `002-861-255-416`
   - `M-1677`: `002-820-001-440-012`
   - `M-49`: `002-300-350-032-190`
   - `M-70`: `002-390-692`
   - unknown row: `002-390-590-032`
4. Test whether these tails behave like administrative subcodes, name/title expansions, or formula residue.

Pass:

- Tail families recur across independent objects and predict metadata or frame behavior better than copy-family controls — a copy family being a set of near-identical objects that really count as one witness.

Fail:

- Each tail family collapses to one plate/workshop/source family or to direction/segmentation artifacts.

First admissibility packet: `campaign_032_002_source_normalized_branch_tail_admissibility.md`. It shows that only `M-49` is currently source-boxed among the decisive adjacent continuation rows. `M-240`, `M-91`, and `M-1677` have known local source-reference routes but still need images; `M-70` needs routing; the unknown `390-590-032` row needs an object ID.
