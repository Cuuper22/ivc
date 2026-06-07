# 032-002 Branch-Tail Linguistic Model

Date: 2026-05-28

## Current Parse

The strongest working parse after the source acquisition is:

```text
[left frame]-032-002-Y(-tail)
```

`032-002` is the gateway. The sign after `002` is the branch decision. Some Y signs close the formula; others behave as heads that license more material.

This is a syntactic-value model, not a translation.

## Role Table

| sign | current role | why it matters |
|---|---|---|
| `817` | strongest closure | all-`002` strict dedup has `817` terminal in 100/103; adjacent `032-002` has 4/4 terminal |
| `820` | closure with rare extension | mostly terminal, but the decisive extension `M-1677 002-820-001-440-012` still lacks a public source panel |
| `861` | closure-capable branch with narrowed restricted-tail behavior | strict `002-861` is 95/119 terminal but has repeated strict tails; the tail-attachment scan narrows restricted post-`861` support to `533-717`, singleton `255-416`, and mixed `603`, while downgrading `416/698` as broad terminal/formula chunks |
| `390` | branch head | 0/14 terminal in all-`002`; source-visible adjacent continuation now exists in `M-70 002-390-692` |
| `300` | branch head / extended clause opener | source-boxed target `M-49 002-300-350-032-190` continues and contains later `032` |
| post-`002` `220` | branch head | all-`002` rows show recurring `220->455` and `220->065`; this is not the same role as pre-`032` `220` |

## Ranked Hypotheses

1. **Branch-selecting morphology**

   `002` marks a branch slot after `032`; Y selects a closure or complement-taking branch. This explains why Y class predicts terminality better than broad metadata and why `390/300/220` are continuation-heavy.

   Falsifier: source-clean rows where `390/300/220` are frequently terminal or where `817/820/861` take rich continuations at branch-head rates.

2. **Formula closure plus administrative extension**

   `032-002` introduces a formula close. `817/820/861` are standard closure signs, while `861/820` can take addenda and `390/300/220` open non-closing administrative continuations.

   Falsifier: post-Y continuations cluster by Y across source contexts rather than by local formula/register.

3. **Nominal classifier or role-marker system**

   `002-Y` may mark a nominal class, title, office, commodity class, or transaction role. Closure signs are compact class endings; branch heads introduce a fuller phrase.

   Falsifier: same left frame freely alternates among Y signs without corresponding continuation, object, icon, or register changes.

4. **Case/role marker after a name or title**

   `A-220-032` may be a name/title frame, `002` a linker, and Y a case-like relation marker. Closure Y signs end the phrase; branch heads require complements.

   Falsifier: continuations after `390/300/220` do not behave like complements, or the same Y appears in incompatible syntactic positions.

5. **Register/local formula only**

   Weakest serious rival. Register matters, but it does not currently explain the closure/branch split as well as Y-class behavior.

   Falsifier against register-only: matched same-register blocks where changing Y changes terminality. The current matched-terminality result already points this way.

## Next Campaigns

1. **Source-token branch cluster**

   Rows: `M-49`, `M-240`, `M-91`, `M-70`.

   Task: token-box and direction-adjudicate the source-panel crops as one cluster. Decide whether the apparent post-Y continuation survives physical order, A/a mirroring, and side-label checks.

   Status: first pass complete in `campaign_032_002_branch_tail_token_order.md`. Result: source-visible post-`002` continuation exists for `300`, `861`, and `390` branches, with broad order windows rather than final token boxes.

2. **`861` suffix split**

   Rows: `M-240`, `M-91`, `M-1273`, `M-714`, `M-376`, `M-391`.

   Test: terminal `861` versus `861-603`, `861-255-416`, and `861-533-717`. If these share a position and source behavior, `861` may be a closure that licenses suffix/addendum tails.

   Status: first campaign complete in `campaign_032_002_861_suffix_split.md`. Strict dedup `002-861` gives 119 rows, 95 terminal and 24 continuing. Strict repeated tails are `603` x3 and `533-717` x2; raw duplicate-family pressure preserves `416` x6 and `698` x2. The next test is suffix attachment: do the tails occur independently, after other closure signs, or preferentially after `861`?

   Attachment status: complete in `campaign_032_002_861_tail_attachment.md`. `533-717` is the strongest repeated restricted post-`861` tail candidate, `255-416` remains a singleton restricted-tail candidate, `603` is a mixed post-`861` tail with independent formula behavior, and `416/698` are downgraded as restricted post-`861` tails.

   Source-token status: complete in `campaign_032_002_861_source_token_attachment.md`. The six focus rows preserve same-line terminal-side candidates in public source crops, so the restricted-tail parse survives as a candidate. Exact source-normalized `861`/tail boundaries are still not accepted.

   Matched-control status: complete in `campaign_032_002_861_matched_terminal_controls.md`. The tail rows now have bare terminal `002-861` controls in relevant matched blocks, especially `220-032`, `803`, `176`, and Mohenjo-daro `SEAL:S Bull1:S`. The next distinction is visible bare edge versus visible tailed edge, not whether the tail rows have any contrast set.

   Bare-edge source-control status: complete in `campaign_032_002_861_bare_edge_source_controls.md`. Source-visible bare edges now exist for `220-032-002-861` (`H-444`, `M-723`, `M-1044`), `803-002-861` (`M-77`, `M-118`), and `176-002-861` (`M-15`). This gives the live model comparison source-visible bare rows against source-visible tailed rows. Candidate ordering remains closure plus tag/addendum, subclass marker, boundary/appended unit, then compound/artifact.

   Tail-family batch status: complete in `campaign_032_002_861_tail_family_batch.md`. `533-717` is now the best restricted post-`861` family in the current strict layer, `603` is the best mixed post-`861` and independent-formula family, `255-416` is singleton stress, and `416/698/000` are downgraded as broad formula/background material. The next decision should split `533-717` and `603`, not keep adding rows to a generic "861 continuation" bucket.

3. **`390` branch-head family**

   Rows: `M-70`, unknown `3335.1`, `M-119`, `M-38`, `M-735`, `Sktd-1`, plus `390-705` rows.

   Test: `390-692`, `390-590-032`, `390-125...`, and `390-705` as one branch-head family. The key clue is whether later `032` recurs as an internal delimiter.

4. **`820` missing-cell acquisition**

   Rows: `M-1677`, `M-1045`, `M-1728`.

   Test: whether `820` really has source-visible nonterminal uses. Without this, `820` stays a mostly-terminal closure with one metadata-only extension.

5. **Recursive `032` tail campaign**

   Rows: `M-49`, `M-119`, `M-38`, unknown `3335.1`.

   Test: later `032` inside tails is a nested delimiter/subslot, not a duplicate accident.

## Decision Rule

Upgrade to a serious syntactic value only if the source-token cluster survives:

```text
same physical line + correct order + Y-tail continuation + family recurrence
```

Downgrade if continuation dissolves into:

```text
side-label mismatch, mirror confusion, damage, duplicate-family artifact, or unrelated second-unit segmentation
```

The translation target remains zero accepted lexical values. The current win condition for this layer is controlled syntactic labels such as:

```text
002 = post-032 branch introducer
Y = closure/branch class selector
861 = closure-capable branch sign
390 = complement-taking branch head
```
