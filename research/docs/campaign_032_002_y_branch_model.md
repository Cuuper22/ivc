# 032-002-Y Branch Model

Date: 2026-05-28

## Current Parse

The working parse is:

```text
A-220-032 -> 002 -> Y / continuation
```

Read it this way. `032` after `A-220` is not an ending; it frequently opens a tail lane — a stretch of signs that finishes the inscription. `002` is the current best marker of that tail lane. And the sign after `002`, which we call Y, is no longer one interchangeable "ending" bucket. It behaves like a branch choice: which Y you get changes what can happen next.

Corpus-wide context update: `campaign_032_002_context_branch_campaign.md` widens the unit to all adjacent `032-002` rows. It finds 50 adjacent rows, 34 strict complete rows, and 32 strict text/site/type dedup units. Strict `target_240_220_032` has four rows and four Y values (`300`, `817`, `820`, `861`), so `240-220-032` selects entry into the `032-002` lane but does not select one ending. The model below should now be read as branch-lane grammar, not as a compact `861/820/817` ending-only hypothesis.

Post-Y continuation update: `campaign_032_002_post_y_continuation_campaign.md` tests what happens after `002-Y` across 813 all-`002` rows and 499 strict dedup units, then narrows to 32 strict dedup adjacent `032-002` units. The result splits the Y slot into two kinds of sign: closure-heavy signs, which end the inscription, and branch heads, which keep it going. `817` is the cleanest closure (`100/103` terminal in all strict dedup `002-Y`, `4/4` after adjacent `032-002`); `820` is closure-heavy (`66/71`, `6/7`); `861` is closure-heavy but branch-capable (`95/119`, `7/9`). By contrast, `390`, `368`, `031`, `220`, `900`, and `300` are continuation-heavy in the all-`002` baseline. The branch model is now:

```text
[left frame]-032-002-[closure or branch head]-[optional continuation]
```

The next falsifier is not another source audit. It is a matched register and length-position test: the Y class must predict terminality better than site/type/symbol/text-length baselines, or the closure/branch grammar collapses into register and inscription-length behavior.

Matched terminality update: `campaign_032_002_y_matched_terminality.md` runs that test. In leave-one-out prediction, all-`002` `y_class` scores 0.885772 accuracy, 0.097554 Brier, and 0.331038 logloss, while `site/type/symbol` scores 0.579158, 0.248248, and 0.690585. Inside adjacent `032-002`, `y_class` scores 0.906250, 0.106698, and 0.381811, while `site/type/symbol` scores 0.531250, 0.284136, and 0.765472. Matched closure-vs-branch blocks exist in 47 all-`002` blocks and 17 adjacent `032-002` blocks. So the Y class beats the register baseline, and the branch grammar stays alive against the current register-only attack. The next falsifier is now source-normalized direction and tail-family semantics, not broad register metadata.

Tail-family update: `campaign_032_002_post_y_tail_family_campaign.md` extracts what actually follows Y. In the all-`002` field, branch-head candidates show repeated next-tail pressure: `390 -> 125/705`, `220 -> 455/065`, and leaky `861 -> 603/533-717`. In the adjacent `032-002` field, the decisive continuations are still mostly singletons: `M-240 861-603`, `M-91 861-255-416`, `M-1677 820-001-440-012`, `M-49 300-350-032-190`, and `M-70 390-692`. So the branch taxonomy has content to chase, but adjacent `032-002` semantics are not repeated enough for a value.

## Source-Clean Evidence

Rows counted here require `source_visible=yes` in the current source-function table — meaning a source image confirms the row at row level.

| branch | source-clean rows | current behavior |
|---|---|---|
| `002-861` | `H-444`, `M-21`, `H-597`, `C-60` | most portable branch; appears in non-240 A-220 and outside controls across Harappa, Mohenjo-daro, Chanhu-daro |
| `002-820` | `M-375` | source-visible in non-240 A-220 only so far |
| `002-817` | `M-722`, `C-10` | source-visible in target and non-240 A-220 |
| `002-300...` | `M-49` | target extended branch; proves target `240-220-032-002` can continue outside the core set |

Source-visible target `240-220-032` currently has:

```text
817 terminal: M-722
300 extended: M-49
```

It does not yet have source-visible target `820` or `861`. That is the main weakness in the target-frame story.

## Scaffold Token-Box Gate

The first token-box pass — checking whether the catalog's signs are physically distinct, boxable units on the object — is stored in `campaign_032_002_y_token_box_scaffold_v1.md`.

Result:

- six anchor rows are boxable as candidate same-line `032/002/Y` packets
- `C-10` is boxable but low-resolution
- `C-60` is weak at token level, though still row-level source-visible

This means the current scaffold does not die as a catalog-adjacency artifact. It still needs stronger token-level work before sign identity is accepted.

## Hypotheses Ranked

### H1: Tail-Lane Marker Plus Closure/Branch Choice

The idea: `002` is the main operator after `A-220-032`; `Y` usually closes the packet, but some Y values can open continuation branches. This best fits the current row behavior because:

- non-240 A-220 has source-visible `861`, `820`, and `817`
- outside controls have strong source-visible `861`
- the target has a source-visible extended `300` branch
- terminal and extended tails both occur after `002`
- all-`002` baseline behavior separates closure-heavy `817/820/861` from continuation-heavy `390/368/031/220/900/300`

Hostile constraint: the hard signal is `A-220-032 -> 002`, not "Y morphology." Conditional on already having `032-002`, the difference between A-220 and outside contexts is much smaller. Therefore the Y claim must be won by branch behavior, source-visible terminality, and controls, not by the first `002` enrichment alone.

Prediction:

- `M-240` should show `002-861-603` as a real extended branch, not a damaged terminal.
- `M-1677` or `M-1045` should show `002-820...` as real outside extended branches if `820` can behave like `861`.
- resolving `M-1385` or `H-140` should show whether `817` is portable outside A-220.
- `002-300` should remain nonterminal if `300` is branch material rather than a closure choice.

Kill condition:

- target/source-visible rows fail for `820/861`, and outside/non-240 rows collapse under better images or side labels.

### H2: Grammatical Ending Class

The idea: `861/820/817` are different compact endings after `002`, with `300` as a separate extended construction.

Current pressure for this model: campaign dedup rows with `032-002-Y` make `817` terminal in all counted cases, while `861` and `820` are terminal-heavy but leaky. In the broader corpus after `002`, the same signs are also heavily terminal by the current metadata layer. This supports closure behavior but does not yet prove grammar.

Prediction:

- core `861/820/817` should mostly terminate after source-visible token boxes.
- extended rows such as `M-240` and `M-1677` should reveal segmentation problems or a second construction boundary after `Y`.
- `817` should almost never continue after source-clean `032-002-817`.

Kill condition:

- `M-240` and outside `820` rows show clean continuation after `Y`, making "ending class" too narrow.

### H3: Object/Register Formula

The idea: the Y split may track site, object type, iconography, or administrative register rather than grammar.

Current pressure:

- outside `861` is cross-site, so it is not just one local plate family
- `M-375` gives `820` on a cuboid-convex seal, which may be register-relevant
- `C-10` puts `817` in Chanhu-daro non-240 A-220, reducing a pure Mohenjo-daro explanation
- the current source-clean set is still seal-heavy and Bull1-heavy, so register and iconography remain serious rival explanations

Prediction:

- `Y` should correlate with object type, symbol/cult, or site after adding source-clean controls.
- if non-iconographic `SEAL:R` rows keep selecting `820` while Bull1 square seals prefer `861/817/300`, the branch model becomes a register formula — unless the same split appears within matched icon/type blocks.

Kill condition:

- the same Y branch appears across unlike sites/types/icons while different Y branches appear within matched register blocks.

### H4: Personal Name or Title Morphology

The idea: `A-220-032-002-Y` may be a name/title formula, with `Y` selecting title/rank/clan/office endings.

Prediction:

- left context before `A-220` should carry name-like variation while the right branch stays formulaic.
- exact or near-exact left contexts should recur with different Y values only in controlled substitutions.
- stems such as `231-220-032`, `233-220-032`, `241-220-032`, or `520-220-032` should show stable Y preferences if Y is morphology attached to a stem.

Kill condition:

- Y tracks object/register better than local string morphology, or extended branches behave like administrative clauses rather than name endings.

### H5: Administrative/Metrological Tail

Prior work gives real pressure toward administrative or metrological structure, not toward a readable lexical phrase. The filtered prior-work pressure is:

- `220` has fish/commodity/metrology pressure, but our current rows are seals/formula lanes rather than direct offering-pot contexts.
- `032` and `002` have stroke/numeral/operator pressure, but the current packet is syntactic, not arithmetic.
- `817/861` may be allographic or variant-sensitive, because both collapse to `P385/M267` in the current provisional crosswalk while Wells separates them as `W817/W861`.
- `820/P378` has no accepted standalone value; keep it as a distinct branch until alternation with `817/861` is source-visible.

Prediction:

- post-Y material should pattern by branch if this is administrative coding: `861`, `820`, `817`, and `300` should license different continuations.
- if `817/861` are allographs, they should substitute under matched site/type/source-quality controls rather than split by function.

Kill condition:

- source-clean token boxes show the apparent stroke/operator lane is an artifact of normalized order, or the Y branches show no controlled continuation behavior after matched controls.

## Next Batch

Run the next campaign in this order:

1. Tail-family semantics test: cluster post-Y material after `861`, `820`, `390`, `300`, and singletons to see whether continuations are licensed chunks, administrative codes, semantic fields, or random row residue.
2. Minimal-pair branch test: find near-matched pre-`002` frames where closure-family and branch-family Y alternate.
3. Source-check decisive continuation rows: `M-240`, `M-91`, `M-1677`, `M-49`, and the two `390` continuations.

Then run the source-campaign queue:

1. Token-box the current source-visible scaffold: `M-722`, `H-444`, `M-375`, `C-10`, `M-21`, `C-60`, `H-597`, `M-49`. This tests whether `032`, `002`, and Y are physically distinct, consecutive, same-line signs rather than catalog-normalized adjacency.
2. Better `C-65` target `002-861`: fills cross-site target `861`.
3. `M-1728` target `002-820`: fills the missing target `820` branch.
4. `M-240` target `002-861-603`: tests whether `861` can continue.
5. `K-145` non-240 A-220 `002-820`: tests `820` outside the Mohenjo-daro block.
6. `H-140` or resolved `M-1385` outside `002-817`: tests outside portability of `817`.
7. `M-1737` outside terminal `002-820`: tests whether outside `820` has a compact branch too.
8. `M-1677` or `M-1045` outside `002-820...`: tests outside/extended `820`.
9. `M-91` non-240 A-220 `002-861-255-416`: tests nonterminal `861` outside the target frame.
10. `M-720` non-240 A-220 `002-817`: pairs against the `923-220...820` family and tests `817` stability.
11. Other-Y A-220 rows such as `M-636`, `M-1686`, `M-130`, `M-1159`, `M-36`, `H-1657`, and `M-1667`: tests whether `{861,820,817}` is special or only a visible subset of a broader `002-Y` field.
12. Negative controls: A-220-032 rows without `002`, and outside `032` rows without `002`, matched by site/type where possible.

Hard kill result: if token boxes on the anchor scaffold fail to show `032-002-Y` as distinct consecutive signs on the same physical line across target, non-240 A-220, and outside rows, the current model dies. The statistical version dies if off-Mohenjo and non-square-seal source-clean rows lose both multi-site and multi-Y support after quarantine.

The research question for the next batch is not "does the packet exist?" It exists in the source-clean layer. The question is whether Y is a branch selector, an ending class, a register formula, or a name/title component.
