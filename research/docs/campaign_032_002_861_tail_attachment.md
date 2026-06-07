# 032-002 861 Tail-Attachment Campaign

Date: 2026-05-28

## Question

Do the apparent post-`861` tails behave like material restricted to `861`, or are they ordinary chunks that happen to follow `861` in a few rows?

This campaign tests the live suffix-split tails:

```text
603
533-717
255-416
416
698
```

and compares them against branch-head controls from the `390` family:

```text
125
705
692
```

## Stored Outputs

```text
tmp/run_032_002_861_tail_attachment.py
data/open_prototype/reports/campaign_032_002_861_tail_attachment_occurrences.csv
data/open_prototype/reports/campaign_032_002_861_tail_attachment_summary.csv
data/open_prototype/reports/campaign_032_002_861_tail_attachment_summary.json
```

The scan covers 4,135 strict closed rows from `metadata_filtered.csv`.

## Result

| unit | total occurrences | after `861` | after `002-861` | terminal | read |
|---|---:|---:|---:|---:|---|
| `603` | 7 | 3 | 3 | 3 | post-`861` occurrence set, but also has a separate repeated `740-603-240...` profile |
| `533-717` | 2 | 2 | 2 | 2 | strongest repeated restricted post-`861` tail candidate |
| `255-416` | 1 | 1 | 1 | 1 | singleton restricted post-`861` tail candidate, tied to `M-91` |
| `416` | 46 | 6 | 6 | 29 | widespread terminal sign/chunk; `002-861-416` is a Harappa exact-formula family |
| `698` | 10 | 2 | 2 | 10 | terminal everywhere; `002-861-698` is a small Mohenjo-daro pair |
| `125` | 50 | 2 | 1 | 15 | not a clean `861` tail; more important as branch-head/control material |
| `705` | 174 | 0 | 0 | 48 | not post-`861`; strong independent/formula sign |
| `692` | 58 | 0 | 0 | 47 | not post-`861`; independent terminal/control sign |

## Distributional Consequence

The scan separates the tail candidates into three evidence tiers:

### Restricted Post-`861` Candidates

```text
861-533-717
861-255-416
```

Both are terminal in every strict occurrence and have no non-`861` occurrences in this scan. `533-717` is the strongest repeated candidate because it appears twice; `255-416` remains a singleton.

### Mixed Tail / Independent Unit

```text
861-603
```

`603` is not exclusive to `861`: it occurs 7 times, 3 after `861`. The non-`861` cases are mainly the repeated formula `740-603-240-060-692`. The data support a post-`861` occurrence family, but not exclusivity.

### Duplicate-Family / Terminal Chunk Pressure

```text
861-416
861-698
```

`416` and `698` are not restricted to post-`861`. `416` occurs widely and is often terminal; `698` is terminal in all 10 strict occurrences. The `002-861-416` and `002-861-698` rows matter as formula families, not as restricted post-`861` evidence.

## Current Working State

The working state is now narrower:

```text
002-861            = high-terminality row family from the prior campaign
002-861-533-717    = repeated restricted terminal continuation candidate
002-861-255-416    = singleton restricted terminal continuation candidate
002-861-603        = terminal continuation candidate using a sign that also appears in another formula lane
```

This upgrades the suffix-split campaign from "there are tails" to "some tails are restricted to post-`861` in this scan, while others are broader terminal/formula material."

## Next Working Inputs

Use in the next source-token pass:

```text
533-717 = strongest current repeated post-861 restricted-tail candidate
255-416 = post-861 restricted-tail singleton
603 = post-861 candidate with separate repeated non-861 profile
```

Do not use as restricted post-`861` evidence yet:

```text
416 / 698
```

They stay in the corpus as broader repeated/terminal occurrences, not as clean restricted-tail evidence.

No sign value, phonetic reading, language identity, or translation is accepted.

## Next Test

Do a source-token attachment pass only on rows that can change the model:

```text
M-376 / M-391: is 533-717 physically separated after 861?
M-91: is 255-416 physically separated after 861?
M-240 / M-714 / M-1273: is 603 separated after 861, and does it occupy the same final slot?
```

Then compare `861-533-717` against the `390` branch-head families. If `533-717` remains restricted to `861`, it becomes the next source-token test target in this branch.
