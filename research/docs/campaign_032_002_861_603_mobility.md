# 032-002-861 603 Mobility

Date: 2026-05-29

This note asks whether one sign gets around. Most signs in the corpus sit inside a single recurring phrase and never leave it, which makes them hard to learn anything from. `603` is different: it ends Mohenjo-daro seals after `002-861` and it also fills a slot in a Harappa tablet formula. A sign that appears in two unrelated settings is worth more than one that does not — unless the two settings just happen to reuse the same shape. This note lays out both possibilities and the evidence for each.

## Question

The tail ecology campaign — the pass that surveyed what follows `002-861` — promoted `603` above `533-717` as the first translation-relevant post-`861` target. This campaign asks the actual linguistic question. "Register" below means the coarse class of object: site, type, symbol, and shape:

```text
Is 603 a mobile sign/function with a stable life across contexts,
or is it two unrelated register templates that happen to reuse the same graph?
```

## Stored Outputs

```text
tmp/run_032_002_861_603_mobility.py
data/open_prototype/reports/campaign_032_002_861_603_mobility_rows.csv
data/open_prototype/reports/campaign_032_002_861_603_mobility_summary.csv
data/open_prototype/reports/campaign_032_002_861_603_mobility_summary.json
```

Input layer. "Strict" rows have complete readings rather than partly reconstructed ones; "dedup" collapses near-duplicate rows so one object cannot be counted twice:

```text
strict complete source strings, cisi/site/type/symbol/text dedup: 4011 rows
strict rows with 603: 7
603 occurrences: 7
```

## Occurrence Classes

| class | rows | examples | current read |
|---|---:|---|---|
| post-`002-861` terminal tail | 3 | `M-240`, `M-714`, `M-1273` | tail after closure edge |
| independent `740-603-240-060-692` lane | 3 | `H-1137`, `H-1138`, `H-1846` | repeated Harappa TAB:B formula family |
| independent other | 1 | `+000-603-091-190+` | weak scene/control row |

## Post-`861` Rows

| row | text | pre-`002-861` frame | register |
|---|---|---|---|
| `M-240` | `+520-240-220-032-002-861-603+` | `220-032` | Mohenjo-daro `SEAL:S`, Gaur, square |
| `M-714` | `+740-585-017-033-705-233-798-803-002-861-603+` | `798-803` | Mohenjo-daro `SEAL:S`, Bull1:W, square |
| `M-1273` | `+740-055-002-861-603+` | `740-055` | Mohenjo-daro `SEAL:R`, no icon, rectangular |

These three rows matter because the left frames and object registers are not a single duplicate family. They still share the same behavior:

```text
002-861-603+
terminal tail
Mohenjo-daro seal register
```

## Independent Rows

| row | text | register |
|---|---|---|
| `H-1137` | `+740-603-240-060-692+` | Harappa `TAB:B`, no icon, rectangular |
| `H-1138` | `+740-603-240-060-692+` | Harappa `TAB:B`, no icon, rectangular |
| `H-1846` | `+740-603-240-060-692+` | Harappa `TAB:B`, no icon, rectangular |
| unknown | `+000-603-091-190+` | Unknown `SEAL:C`, Scene, circular |

The independent side is not four equal votes. Three of the four rows carry identical text, which makes them one "formula family" — a group of near-identical rows that must be weighed as a single piece of evidence. So the tally is:

```text
one repeated Harappa TAB:B formula family
plus one weak outside row
```

That prevents a value claim. It does not kill the bridge, because it still proves `603` is not confined to post-`861`.

## Linguistic Hypotheses For `603`

| hypothesis | what `603` would be | supporting facts | current weakness |
|---|---|---|---|
| lexical/classifier handle | noun-like or class-like element that can appear in two constructions | post-`861` plus independent lane | independent lane is mostly one formula family |
| appositional addendum | terminal note after closed `002-861` phrase | all post-`861` rows are terminal | no direct semantic contrast yet |
| boundary second phrase | separate phrase after `861`, not suffix | independent formula life makes this plausible | source spacing/boundary not yet resolved |
| register marker | Mohenjo seal tail and Harappa tablet formula share administrative role | both are administrative-looking object classes | cross-site/type difference may be too large |
| reused graphic/template | same sign reused in unrelated local templates | Harappa lane is one copied formula family | post-`861` rows are three distinct register cells |

## Decision

```text
603_mobility_is_live_but_not_yet_a_value
```

`603` is now the first live bridge target after `002-861`, but it is not a reading. It has just enough mobility to matter and enough formula/register pressure to stay dangerous.

## Next Test

Run a source-layout and neighbor-ecology campaign for `603`:

```text
post-861 side:
  M-240 / M-714 / M-1273

independent side:
  H-1137 / H-1138 / H-1846
  +000-603-091-190+
```

Decision criteria:

```text
promote if 603 keeps the same graphic identity, occupies comparable boundary/phrase positions,
and shares stable neighbor semantics beyond a single copied formula family

demote if the independent lane collapses to a copied Harappa tablet formula,
or source layout shows the post-861 use is only a boundary/appended unit with no shared behavior
```

No sign value, phonetic reading, language identity, or translation is accepted.
