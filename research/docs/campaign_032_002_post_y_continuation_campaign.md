# 032-002 Post-Y Continuation Campaign

Date: 2026-05-28

## Question

This note asks what kind of thing the sign after `002` is. Signs in this corpus are numeric IDs; `Y` names whichever sign follows `002`. A row is "terminal" when it ends right after `Y`, and "continuing" when more signs follow. A "branch head" is a sign that opens further material; a "closure" sign ends the row. A "register" is the object class a row sits on — site, seal type, icon, shape. "Strict dedup" means identical texts collapse to one unit of evidence, so copies cannot count twice.

After `032-002-Y`, does `Y` behave like:

- an ending/closure class,
- a branch head that licenses a following tail,
- a register-conditioned formula filler,
- or a pure artifact of short inscriptions being near the right edge?

This campaign widens the object from the curated `032-002-Y` source-function packet to all local `002-Y` contexts, then narrows back to the 32 strict dedup adjacent `032-002` units.

## Inputs

- Corpus layer: `data/open_prototype/lipi/metadata_filtered.csv`
- Extraction script: `tmp/run_032_002_post_y_campaign.py`
- Mechanic validation: PASS

Outputs:

- `data/open_prototype/reports/campaign_032_002_post_y_all_002_rows.csv`
- `data/open_prototype/reports/campaign_032_002_post_y_branch_rows.csv`
- `data/open_prototype/reports/campaign_032_002_post_y_y_summary.csv`
- `data/open_prototype/reports/campaign_032_002_post_y_register_summary.csv`
- `data/open_prototype/reports/campaign_032_002_post_y_summary.json`

## Counts

| layer | rows |
|---|---:|
| all `002-Y` rows | 813 |
| all strict complete/closed `002-Y` rows | 576 |
| all strict text/site/type dedup `002-Y` rows | 499 |
| adjacent `032-002-Y` rows | 50 |
| adjacent strict complete/closed `032-002-Y` rows | 34 |
| adjacent strict text/site/type dedup `032-002-Y` rows | 32 |

Within the strict dedup adjacent `032-002` layer, post-Y behavior is:

| continuation class | rows |
|---|---:|
| terminal | 19 |
| one-token continuation | 8 |
| multi-token continuation | 3 |
| later `032` continuation | 2 |

## Corpus-Wide Post-002 Behavior

The all-`002` strict dedup baseline gives the crucial split.

| Y after `002` | rows | terminal | working class |
|---|---:|---:|---|
| `861` | 119 | 95/119 | closure-heavy, branch-capable |
| `817` | 103 | 100/103 | hard closure |
| `820` | 71 | 66/71 | closure-heavy |
| `390` | 14 | 0/14 | branch head |
| `368` | 11 | 0/11 | branch head |
| `031` | 9 | 0/9 | branch head |
| `220` | 9 | 0/9 | branch head |
| `824` | 6 | 6/6 | closure, small n |
| `900` | 4 | 0/4 | branch head |
| `300` | 1 | 0/1 | branch head, target-row only here |

The result is not "all signs after `002` are endings." The result is sharper: `002` is followed by a sign from a slot that splits into closure signs and continuation signs.

## Focused 032-002 Layer

Inside the 32 strict dedup adjacent `032-002` units:

| Y after `032-002` | rows | terminal | continuation examples |
|---|---:|---:|---|
| `861` | 9 | 7/9 | `861-603`, `861-255-416` |
| `820` | 7 | 6/7 | `820-001-440-012` |
| `817` | 4 | 4/4 | none |
| `390` | 2 | 0/2 | `390-692`, `390-590-032` |
| `300` | 1 | 0/1 | `300-350-032-190` |
| other singletons | 9 | mixed | unresolved residue |

Frame split:

| frame | strict dedup rows | behavior |
|---|---:|---|
| `target_240_220_032` | 4 | four Y values: `300`, `817`, `820`, `861`; two terminal, two continuing |
| `non240_a_220_032` | 16 | dominated by `861/820/817`, but with singleton branches |
| `outside_032` | 12 | `861/817/820` still present; `390` appears as a clean nonterminal branch |

This kills the old micro-model where `240-220-032` selected a specific ending. It enters the lane; it does not determine the branch.

## Register Baseline

The hostile register read is real enough to matter.

Largest matched site/type/symbol block:

```text
Mohenjo-daro / SEAL:S / Bull1:W = 8 rows, terminal 5/8
```

Matched frame/site/type blocks:

```text
target_240_220_032 @ Mohenjo-daro / SEAL:S = 4 rows, terminal 2/4
non240_a_220_032 @ Mohenjo-daro / SEAL:S = 11 rows, terminal 7/11
outside_032 @ Mohenjo-daro / SEAL:S = 5 rows, terminal 2/5
```

So register does not disappear. But it also does not explain the whole split, because the same `Y` classes show consistent corpus-wide post-`002` terminality behavior:

- `817`, `820`, and `861` are closure-heavy in the full `002-Y` baseline.
- `390`, `368`, `031`, `220`, `900`, and `300` are continuation-heavy.
- In the same broad Mohenjo-daro seal register, both terminal and continuing post-Y outcomes occur.

## Working Linguistic Model

Current parse:

```text
[left frame] - 032 - 002 - Y - [optional continuation]
```

`032` marks entry into a tail lane when it follows `A-220`. `002` is the stronger boundary/operator sign. `Y` is not a single ending; it is a branch choice whose members fall into at least two classes:

| class | members | interpretation |
|---|---|---|
| hard closure | `817` | closes the `032-002` packet almost always |
| leaky closure | `820`, `861` | closes often, but can license controlled extensions |
| branch heads | `390`, `368`, `031`, `220`, `900`, `300`, likely several singletons | open further material after `002` |

This is a language-relevant result because it is about positional behavior and continuation licensing. It is not a translation and not a sign value.

## Competing Reads

### H1: Ending Class With Branch Leakage

Best current read.

`817/820/861` are a closure family, with `817` the cleanest closure. `861` and `820` are not pure endings; they can carry an extension tail. Under this read, `002` is a right-edge/tail-lane operator and Y chooses the ending or branch subtype.

Prediction:

- `817` remains terminal after source-clean checks.
- `861-603` and `861-255-416` are real licensed extensions, not damage.
- `820-001-440-012` is either a real extension or a separable second construction.

### H2: Register Formula

Serious rival.

Short Mohenjo-daro square-seal strings may terminate after common formula fillers, while longer rows continue for register reasons. This can fake an ending class.

Falsifier:

- Within matched site/type/symbol/text-length blocks, `817/820/861` must still predict terminality better than length and register.

### H3: Length / Right-Edge Artifact

Also serious.

Most inscriptions are short. Any sign after `032-002` is often near the end. Terminality alone is cheap.

Falsifier:

- Compare each `Y` against length-position matched signs after `002`, not against the whole corpus.
- If `817/820/861` do not beat that baseline, closure grammar collapses.

### H4: Administrative Code Tail

Live semantic direction.

The continuation material after branch heads looks bounded and code-like. This favors an administrative or classification formula over a full free-text phrase.

Prediction:

- post-Y tails recur as stable chunks by Y class.
- `861` extensions should share a tail family if it is an administrative code rather than random leftover text.

## Decisions

Accepted:

- `032-002` is a branch-lane construction in the current corpus layer.
- `002-Y` splits into closure-heavy and continuation-heavy post-slot classes.
- `817` is currently the strongest closure sign after `002`.
- `861` and `820` are closure-heavy but not pure endings.
- `390`, `368`, `031`, `220`, `900`, and `300` are current continuation/branch-head candidates after `002`.

Rejected:

- `240-220-032` controls one Y value.
- `861/820/817` are interchangeable endings.
- all signs after `002` are endings.
- any lexical value, phonetic value, language identity, or translation.

## Next Campaign

Matched-register terminality has now been run in `campaign_032_002_y_matched_terminality.md`. Result: Y class beats register-only baselines in both the 499-row all-`002` strict dedup layer and the 32-row adjacent `032-002` strict dedup layer. The next campaign is therefore semantic/branch-tail, not another generic register check.

Run a minimal-pair branch semantics test:

1. Restrict to strict dedup `002-Y` rows.
2. Find near-matched pre-`002` frames where closure-family and branch-family Y alternate.
3. Cluster tails after branch-head Y.
4. Test whether those tails track object/register/icon, neighbor formula, or a recurring code-like semantic class.
5. Source-check the decisive continuations: `M-240`, `M-91`, `M-1677`, `M-49`, `M-70`, and the unknown `390-590-032` row.

Pass:

- branch-head Y predicts a recurring tail family or semantic/register partition after matched frame controls.

Fail:

- post-Y material is only row residue, copy-family continuation, or source-normalization artifact.

Immediate source rows for interpretation:

- `M-240`: target `002-861-603`
- `M-91`: non-target `002-861-255-416`
- `M-1677`: outside `002-820-001-440-012`
- `M-49`: target `002-300-350-032-190`
- `M-70` and unknown row: `002-390...`

These decide whether the leaky closure and branch-head classes are real grammar or catalog-normalized row tails.
