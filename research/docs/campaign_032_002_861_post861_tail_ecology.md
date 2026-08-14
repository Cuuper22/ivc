# 032-002-861 Post-861 Tail Ecology

Date: 2026-05-29

This note deliberately widens the field of view. Several campaigns in a row had been squeezing one two-sign ending, `533-717`, for evidence it could not give. This note steps back and surveys everything that follows `002-861` at once — all 23 endings — then reweights them so that six copies of one stock phrase no longer outvote three genuinely different objects. The survey changes the campaign's priority: `603`, not `533-717`, is the target worth chasing. "Ecology" here means the study of which endings occur, how often, and in what company.

## Question

The previous `533-717` campaigns prevented a fake exact match, but they also made the research unit too small. This campaign resets the object:

```text
What does the full post-002-861 tail field do?
```

The target is not one sign or one pair. The target is the ecology of closures, addenda — extra material tacked on after an otherwise complete ending — subclass markers, second phrases, and source-family cells, groups of near-identical rows weighed as one piece of evidence, after `002-861`.

## Stored Outputs

```text
tmp/run_032_002_861_post861_tail_ecology.py
data/open_prototype/reports/campaign_032_002_861_post861_tail_ecology_rows.csv
data/open_prototype/reports/campaign_032_002_861_post861_tail_ecology_summary.csv
data/open_prototype/reports/campaign_032_002_861_post861_tail_ecology_priority.csv
data/open_prototype/reports/campaign_032_002_861_post861_tail_ecology_summary.json
```

Input layer. "Strict" rows have complete readings rather than partly reconstructed ones; "dedup" collapses near-duplicate rows so one object cannot be counted twice:

```text
strict complete source strings, cisi/site/type/symbol/text dedup: 4011 rows
rows carrying 002-861: 144
post-002-861 tail families: 23
```

## Ecology Classes

| ecology class | class count | interpretation |
|---|---:|---|
| bare closure background | 1 | default `002-861+` background |
| broad formula or background control | 3 | broad signs/chunks that happen to occur after `861` |
| mixed post-`861` and independent | 1 | tail also has independent formula life |
| restricted repeated cell | 1 | repeated but currently one narrow source/register-family cell |
| singleton simple tail source target | 10 | source/acquisition targets, not readings |
| singleton complex tail source target | 7 | phrase-like singletons, not suffix evidence yet |

## Main Tail Field

"Weighted cells" is the row count after near-identical rows are merged: it is the number that should carry argumentative weight, and it is often far below the raw row count.

| tail after `002-861` | rows | weighted cells | class | read |
|---|---:|---:|---|---|
| `<END>` | 113 | 58 | bare closure background | dominant background closure |
| `603` | 3 | 3 | mixed post-`861` and independent | best live bridge target |
| `533-717` | 2 | 1 | restricted repeated cell | real but one narrow source/register-family vote |
| `416` | 6 | 1 | broad formula/background control | Harappa TAB:I cell, not six grammar votes |
| `698` | 2 | 1 | broad formula/background control | small Mohenjo pair/control |
| `000` | 1 | 1 | broad formula/background control | background sign, not a post-`861` target |
| complex singletons | 7 tails | 7 | singleton source targets | phrase-like material needing recurrence or source contrast |
| simple singletons | 10 tails | 10 | singleton source targets | useful only if they connect to independent contexts |

The ranking changes the research object:

```text
603 is now the highest-payoff linguistic target.
533-717 is kept as real evidence, but not as the center of the campaign.
```

## `603` Bridge

`603` has the best translation-relevant profile in the current field:

```text
post-002-861 rows:
  M-240  +520-240-220-032-002-861-603+
  M-714  +740-585-017-033-705-233-798-803-002-861-603+
  M-1273 +740-055-002-861-603+

independent rows:
  H-1137 +740-603-240-060-692+
  H-1138 +740-603-240-060-692+
  H-1846 +740-603-240-060-692+
  -      +000-603-091-190+
```

That means `603` is not just a post-`861` ornament. It also lives in a separate Harappa TAB:B formula lane and one weak scene/control row. This makes it the first candidate for tail mobility:

```text
Does 603 behave like a lexical/classifier element that can appear after a closure and inside another formula,
or are we looking at two unrelated register templates that reuse the same sign?
```

## `533-717` Reweighted

`533-717` remains real:

```text
M-376 +740-100-176-002-861-533-717+
M-391 +405-845-686-740-793-003-233-805-002-861-533-717+
```

But the active weight is now one narrow source/register-family cell, not a broad linguistic class:

```text
two artifacts
one no-icon Mohenjo-daro SEAL:R cuboid-convex register cell
no independent occurrence in the strict layer
no unique layout discriminator
no preframe selector
```

It can return to high priority only if it escapes this cell: a third independent occurrence, a same-prefix minimal contrast, or a clear independent `533/717` phrase ecology.

## Competing Linguistic Hypotheses

| hypothesis | parse | what would promote it | what would kill it |
|---|---|---|---|
| closure plus appositional addenda | `002-861 | tail` | tails recur independently or after other closure signs | tails never leave one source/register cell |
| subclass markers | `861-tail` marks overt subclass | tail choice predicts register better than source accident | `603` and others freely behave elsewhere |
| boundary plus second phrase | `[002-861] [tail phrase]` | long tails or `603` have internal syntax elsewhere | source images show ordinary tight suffixal layout only |
| lexical/name segments | post-`861` material is noun-like content | tail signs recur in stable noun-like contexts | no substitution classes or outside lives emerge |
| source-family templates | tails are copied local templates | repeated tails collapse into catalog/plate/object families | same tail spreads across sites, registers, and left frames |

Current ranking:

```text
1. closure plus appositional addenda
2. subclass markers for narrow register-bound tails
3. boundary plus second phrase for long tails and 603
4. lexical/name segment, with 603 as the first live handle
5. source-family template for 416, 698, and maybe 533-717
```

## Falsifiers

A "falsifier" is a finding fixed in advance that would kill the claim. The linguistic-structure claim dies if these jointly hold:

```text
tail choice is predicted by register/source family
repeated tails collapse into one copied formula cell
tailing tracks row length or 861 distance from edge
tail signs have unrelated independent formula lives
source images show side breaks, large phrase breaks, or uncertain order
```

The claim survives if tails remain source-real, independently repeated, specifically attached to `861`, and not predictable from register/template mechanics.

## Decision

```text
post861_tail_ecology_replaces_single_tail_reading
```

The next campaign is not another `533-717` safety pass. It is the `603` mobility campaign:

```text
compare post-861 603:
  M-240 / M-714 / M-1273

against independent 603:
  H-1137 / H-1138 / H-1846 / scene-control row

ask:
  same sign-function or reused graph?
  appositional lexical handle or independent register template?
  do neighboring frames make 603 noun-like, classifier-like, or formula-bound?
```

No sign value, phonetic reading, language identity, or translation is accepted.
