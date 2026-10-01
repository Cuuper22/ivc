# 032-002 861 Matched Terminal Controls

Date: 2026-05-28

This note checks that our interesting rows have something to be compared against. A seal that adds signs after `002-861` only tells us something if there are similar seals that do not — otherwise the addition might be normal for that kind of object and we would never know. This pass searches, for each row with a tail, for nearby rows that stop bare. Every one of them has some. That does not explain the tails; it makes them countable.

## Question

After the source-token attachment pass — the earlier work matching marks on photographs to claimed signs — the next control is whether the tail rows have nearby bare terminal `002-861` controls. "Bare" means the inscription stops right after `002-861`; a "control" is a comparison row sharing the setting but not the feature under test.

This is not a translation test. It asks whether the current tail rows are contrastive against comparable terminal rows, or whether they sit in uninformative isolated contexts.

## Stored Outputs

```text
tmp/run_032_002_861_matched_terminal_controls.py
data/open_prototype/reports/campaign_032_002_861_matched_terminal_controls_rows.csv
data/open_prototype/reports/campaign_032_002_861_matched_terminal_controls_summary.csv
data/open_prototype/reports/campaign_032_002_861_matched_terminal_controls_families.csv
data/open_prototype/reports/campaign_032_002_861_matched_terminal_controls_summary.json
```

Input layer. "Strict dedup" means near-duplicate rows are collapsed so one object cannot be counted twice:

```text
data/open_prototype/reports/campaign_032_002_861_suffix_split_rows.csv
scope = all_002_strict_dedup
rows = 119
```

## Key Control Results

"Match level" is how the comparison block was drawn: by the last sign or last two signs before `002-861`, or by the object's site, type, and icon. A "lane" is a specific left-to-right pattern of those preceding signs.

| focus | match level | matched rows | bare terminal `002-861` controls | tail rows in block | result |
|---|---|---:|---:|---:|---|
| `M-376 533-717` | prefix last sign `176` | 6 | 4 | 2 tails total | `533-717` has local bare-terminal pressure through `176-002-861` |
| `M-391 533-717` | same site/type/icon `Mohenjo-daro SEAL:R None` | 7 | 3 | 4 tails total | no-icon `SEAL:R` block contains both bare terminal and tailed rows |
| `M-91 255-416` | same site/type/icon `Mohenjo-daro SEAL:S Bull1:S` | 10 | 9 | 1 focus tail | singleton appears in a block with many bare terminal controls |
| `M-91/M-240` | prefix last two `220 032` | 6 | 4 | 2 focus tails | the `A-220-032` lane has direct bare-terminal controls |
| `M-714 603` | prefix last sign `803` | 3 | 2 | 1 focus tail | `803-002-861` has bare terminal controls plus one `603` tailed row |
| `M-1273 603` | same site/type/icon `Mohenjo-daro SEAL:R None` | 7 | 3 | 4 tails total | `603` shares the no-icon `SEAL:R` block with `533-717` and bare controls |

Family-level controls:

| tail family | match level | matched rows | bare terminal controls | focus tail rows | note |
|---|---|---:|---:|---:|---|
| `533-717` | same site/type/icon | 7 | 3 | 3 | includes `M-376`, `M-391`, and `M-1273 603` in the same broad block |
| `533-717` | prefix last sign `176/805` | 7 | 4 | 2 | the `176` branch has bare controls; `805` is not yet closely controlled |
| `603` | same site/type/icon union | 32 | 21 | 5 | broad controls exist, but this is a mixed-register family |
| `603` | prefix last two union | 8 | 4 | 4 | direct controls exist for the `220 032`, `798 803`, and `740 055` focus keys |
| `255-416` | same site/type/icon | 10 | 9 | 1 | singleton is the only focus tail inside a mostly bare-terminal block |

## Result

Every focus family has bare terminal `002-861` controls in at least one relevant matched block.

The strongest control facts are:

```text
220-032-002-861: 4 bare terminal controls vs M-91 255-416 and M-240 603
803-002-861:     2 bare terminal controls vs M-714 603
176-002-861:     4 bare terminal controls vs M-376 533-717 and L-46 392
SEAL:S Bull1:S:  9 bare terminal controls vs M-91 255-416
```

This makes the tail rows countable against a bare `002-861` background. It does not decide whether the tailed rows are addenda, subclass markers, second units, or catalog segmentation effects.

## Limits

```text
M-376 has prefix-last1 controls but no exact prefix-last2 bare control.
M-391 has same-register controls but no close prefix control yet.
M-91 is still a singleton.
603 remains mixed because it has non-861 occurrence rows in the tail-attachment scan.
Matched controls are corpus-level, not source-token checked in this campaign.
```

No sign value, phonetic reading, language identity, or translation is accepted.

## Next Test

Source-route the strongest bare controls:

```text
220-032-002-861 bare controls: H-444, M-1763, M-723, M-1044
803-002-861 bare controls: M-77, M-118
176-002-861 bare controls: M-2060, M-1880, M-1755, M-15
```

Then compare source-token layouts:

```text
bare 002-861 edge
vs
002-861-tail edge
```

The next evidence target is not a meaning. It is whether tailed rows visibly add material to an otherwise comparable terminal edge.
