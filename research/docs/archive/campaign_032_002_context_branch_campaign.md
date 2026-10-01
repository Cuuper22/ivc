# 032-002 Context Branch Campaign

Date: 2026-05-28

## Question

This note widens an earlier hand-picked sample to the whole corpus, to find out whether a recurring sign sequence is really a construction. Signs in this corpus are numeric IDs. A "lane" is an analysis track — one recurring sequence followed through the data. A "register" is the object class a row sits on: site, seal type, icon, shape. `Y` names whichever sign follows `002`.

Does `A-220-032 -> 002 -> Y` behave like a grammatical construction, a generic suffix lane, a register formula, or a local catalogue artifact?

This campaign widens the unit from the curated 25-row source-function manifest to every adjacent `032-002` context in `metadata_filtered.csv`.

## Data Stored

- `data/open_prototype/reports/campaign_032_002_context_all_rows.csv`
- `data/open_prototype/reports/campaign_032_002_context_branch_summary.csv`
- `data/open_prototype/reports/campaign_032_002_context_y_by_frame.csv`
- `data/open_prototype/reports/campaign_032_002_context_prev1_y.csv`
- `data/open_prototype/reports/campaign_032_002_context_summary.json`
- `tmp/run_032_002_context_campaign.py`

Mechanic validation: PASS.

## Scope

| scope | rows |
|---|---:|
| all adjacent `032-002` rows | 50 |
| strict complete closed rows | 34 |
| strict complete closed, dedup by text/site/type | 32 |

Strict complete closed means `complete=Y`, plus-delimited, no bracket damage, no slash ambiguity, and no `000` tokens. Dedup collapses rows with the same text, site, and type into one unit of evidence, so a copied inscription cannot count twice.

## Main Result

`240-220-032` still looks like a strong selector into the `032-002` lane, but it does not control a single Y value.

Strict target rows:

| cisi | text | Y | terminal |
|---|---|---:|---|
| `M-49` | `+527-550-240-220-032-002-300-350-032-190+` | `300` | no |
| `M-722` | `+740-585-240-220-032-002-817+` | `817` | yes |
| `M-1728` | `+161-055-240-220-032-002-820+` | `820` | yes |
| `M-240` | `+520-240-220-032-002-861-603+` | `861` | no |

That kills the too-neat reading where `240-220-032` simply means "take Y = one specific ending." The better parse is:

```text
240-220-032 selects the 032-002 lane.
002 opens a branch slot.
Y is a branch head or closure choice, sometimes terminal and sometimes followed by more material.
```

## Frame Behavior

Strict dedup branch summary:

| frame | rows | terminal | continuing | Y distribution |
|---|---:|---:|---:|---|
| `target_240_220_032` | 4 | 2 | 2 | `300:1;817:1;820:1;861:1` |
| `non240_a_220_032` | 16 | 11 | 5 | `861:5;820:4;817:1;690:1;142:1;717:1;368:1;144:1;168:1` |
| `outside_032` | 12 | 6 | 6 | `861:3;817:2;820:2;390:2;892:1;252:1;900:1` |

Immediate previous sign before `032` is also not enough:

| previous sign before `032` | Y distribution in strict dedup |
|---|---|
| `220` | `861:6;820:5;817:2;300:1;690:1;142:1;717:1;368:1;144:1;168:1` |
| outside `220` | broad singleton-heavy set with recurring `861`, `817`, `820`, `390` |

So the old "core ending family" wording is too small. `861/820/817` are a high-support branch family, but the construction has a wider Y field.

## Linguistic Interpretation

The live construction is not a word-value. It is a positional grammar object:

```text
[left stem/frame] - 032 - 002 - [branch head] - [optional continuation]
```

Current function pressure:

- `032` is a hinge or subtype marker, not an ending.
- `002` is the strongest candidate for the tail-lane operator.
- `Y` is a branch head: it can close the unit (`817`, some `820/861`) or open a continuation (`300`, `861-603`, `820-001-440-012`, etc.).
- `240-220` is an entry selector into the lane, not a controller of the Y inventory.

This is closer to administrative morphology or formula grammar than to a lexical translation.

## Competing Models

### H1: Branch-Slot Grammar

`032-002` creates a grammatical branch slot. The Y signs are branch heads, not simple endings.

Support:

- target `240-220-032` accepts four different Y values in four strict rows.
- outside rows reuse `861`, `817`, and `820`.
- terminality splits by Y/context, not by the mere presence of `002`.

Next test:

- classify post-Y continuation types by Y across all strict rows.

### H2: Register Formula

Y choice tracks site, object type, iconography, or administrative register.

Support:

- source-clean rows are still seal-heavy and Bull1-heavy.
- `M-375` puts `820` on `SEAL:R`, which may mark register behavior.
- singleton Y values after `A-220-032` are mostly Mohenjo-daro seals.

Next test:

- compare Y choice inside matched site/type/icon blocks, especially Mohenjo-daro `SEAL:S` versus non-square and non-Mohenjo rows.

### H3: Name/Title Morphology

The left frame is a stem/name/title, and `032-002-Y` supplies office, rank, clan, or title morphology.

Support:

- left contexts vary while the right lane recurs.
- `Y` is diverse enough to behave like a title/rank slot rather than a fixed phrase.

Next test:

- group by `prev3_frame` and test whether near-identical stems select stable or contrastive Y values.

### H4: Catalogue/Source Artifact

The construction may be inflated by normalized order, damaged rows, copied families, or source-side ambiguity.

Support:

- target `820` (`M-1728`) and target extended `861` (`M-240`) are not yet source-clean — that is, not yet checked against a published photograph.
- outside `817/820` still depends on `H-140`, `M-1385`, `M-1737`, or `M-1677` source work.

Next test:

- source-box target `M-1728/M-240`, outside `H-140/M-1737/M-1677`, and the singleton other-Y A-220 rows.

## Researcher Review

Model-builder read:

- best current model is branch-selecting morphology: `032` is a hinge, `002` is a linker or boundary marker, and Y is a branch exponent.
- `817` is currently the cleanest closure candidate.
- `820` and `861` behave as closure/branch heads because both can take continuation in some rows.
- `300` is not an ending in this packet; it opens a longer target branch.

Hostile read:

- strongest rival is register-conditioned administrative formula, not morphology.
- strict target rows are all Mohenjo-daro `SEAL:S`, so target behavior is still site/type vulnerable.
- target Y scatter (`300/817/820/861`) blocks any claim that `240-220-032` controls a semantic ending.
- singleton Y values are not noise until source-boxed; they may be branch codes.

Prior-work pressure:

- sequence statistics justify syntax/function claims only, not readings.
- `002` should be treated first as a positional operator, not a lexical sign.
- stroke/numerical pressure is real but unproven because the current packet is seal-heavy.
- `817/861` must be tested collapsed and split because provisional crosswalk pressure — uncertainty in the mapping between catalog sign numbers and actual graphic shapes — makes them possible allographs or variants.

## Decision

The current model is upgraded from:

```text
A-220-032-002-{861,820,817} = compact ending family
```

to:

```text
A-220-032 enters a 032-002 branch lane.
861/820/817 are the best-supported compact branches.
300 and several singleton Y values prove the lane is broader than the compact family.
```

Accepted: `032-002` is a real constructional target with branch behavior in the current corpus layer.

Rejected: any translation, any Y value, any claim that `240-220-032` determines one ending, and any claim that `{861,820,817}` exhausts the construction.

## Next Experiments

1. Source-box target `M-1728` and `M-240` because they decide whether target `820` and target extended `861` are real physical rows.
2. Source-box outside `H-140`, `M-1737`, and `M-1677` because they decide whether `817/820` are portable outside the `A-220` frame.
3. Run a post-Y continuation campaign: compare what follows `300`, `861`, `820`, `817`, `390`, and singleton branches.
4. Run an other-Y A-220 campaign over `M-1686`, `M-130`, `M-1159`, `M-36`, `H-1657`, and `M-1667` to decide whether the singleton Y values are real branches or damaged/source-policy noise.
5. Build matched site/type/icon mini-sets before interpreting any branch as morphology.
