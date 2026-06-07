# 032-002-861 Preframe Tail Comparison

Date: 2026-05-29

## Question

Since source layout did not uniquely separate `533-717`, this campaign asks whether the immediately preceding frame before `002-861` explains the tail split.

Focus frames from the seven-row same-register set:

```text
100-176 -> 533-717
233-805 -> 533-717
740-055 -> 603
231-235 -> 360-520-919-140
720-175 -> bare
233-550 -> bare
415-798 -> bare
```

## Stored Outputs

```text
tmp/run_032_002_861_preframe_tail_comparison.py
data/open_prototype/reports/campaign_032_002_861_preframe_tail_comparison_rows.csv
data/open_prototype/reports/campaign_032_002_861_preframe_tail_comparison_last2.csv
data/open_prototype/reports/campaign_032_002_861_preframe_tail_comparison_last1.csv
data/open_prototype/reports/campaign_032_002_861_preframe_tail_comparison_summary.json
```

## Last-2 Frame Result

The two `533-717` last-2 frames are singletons:

| pre-`002-861` frame | rows | tail |
|---|---:|---|
| `100-176` | 1 | `533-717` |
| `233-805` | 1 | `533-717` |

The other same-register focus frames are also mostly singleton:

| pre-`002-861` frame | rows | tail |
|---|---:|---|
| `231-235` | 1 | `360-520-919-140` |
| `233-550` | 1 | bare |
| `720-175` | 1 | bare |
| `740-055` | 1 | `603` |
| `415-798` | 2 | bare |

## Last-1 Frame Result

Broader last-1 frames do not isolate `533-717`:

| pre-`002-861` sign | rows | tail profile |
|---|---:|---|
| `176` | 6 | bare 4, `392` 1, `533-717` 1 |
| `805` | 1 | `533-717` 1 |
| `235` | 8 | bare 7, long tail 1 |
| `798` | 8 | bare 6, `216` 1, `832` 1 |
| `175` | 2 | bare 2 |
| `055` | 1 | `603` 1 |
| `550` | 1 | bare 1 |

## Decision

The preframe test does not promote `533-717` to a value or subclass marker.

What it does show:

```text
The last-2 target frames are too sparse to carry a reading.
The broader last-1 frames are useful context clues, not values.
```

Current status:

```text
533-717 remains a repeated post-861 terminal tail with two independent witnesses.
It does not yet have a demonstrated selector, value, or layout function.
```

## Next Campaign

The next productive unit should be broader than `533-717`:

```text
post-861 tail ecology:
  bare closure
  short tail 603
  pair tail 533-717
  long tail 360-520-919-140
  other rare tails
```

The research question becomes:

```text
Does 002-861 mark a closure site that can license several tail classes,
and do those tail classes behave like appositions, subclass markers, or second phrases?
```

No sign value, phonetic reading, language identity, or translation is accepted.
