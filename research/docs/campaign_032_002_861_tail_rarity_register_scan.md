# 032-002-861 Tail Rarity Register Scan

Date: 2026-05-29

## Question

After `533-717` looked restricted, the danger was selection bias:

```text
pick a rare tail after seeing it, then call its tiny cell meaningful
```

This campaign scans every strict `002-861` tail family and asks whether `533-717` remains special once the whole tail field is visible.

## Stored Outputs

```text
tmp/run_032_002_861_tail_rarity_register_scan.py
data/open_prototype/reports/campaign_032_002_861_tail_rarity_register_scan_rows.csv
data/open_prototype/reports/campaign_032_002_861_tail_rarity_register_scan_tail_summary.csv
data/open_prototype/reports/campaign_032_002_861_tail_rarity_register_scan_focus_rows.csv
data/open_prototype/reports/campaign_032_002_861_tail_rarity_register_scan_focus_summary.csv
data/open_prototype/reports/campaign_032_002_861_tail_rarity_register_scan_summary.json
```

Input layer:

```text
data/open_prototype/lipi/metadata_filtered.csv
strict complete source strings, text/site/type/symbol dedup: 4011 rows
```

## Scan Result

Whole strict `002-861` field:

```text
rows with 002-861: 144
tail families after 002-861: 23
bare 002-861: 113
small perfect register cells: 20
```

Main tail counts:

| tail after `002-861` | rows | source-visible rows | Mohenjo no-icon `SEAL:R` rows | status |
|---|---:|---:|---:|---|
| `<END>` | 113 | 1 | 3 | dominant bare closure |
| `416` | 6 | 0 | 0 | broad Harappa background |
| `603` | 3 | 1 | 1 | mixed alternate short tail |
| `533-717` | 2 | 2 | 2 | live but tiny restricted cell |
| `698` | 2 | 0 | 0 | small perfect-looking cell, not enough alone |
| `360-520-919-140` | 1 | 1 | 1 | same-register hostile comparator |

Mohenjo-daro no-icon `SEAL:R + 002-861` splits as:

| tail | rows | examples |
|---|---:|---|
| `<END>` | 3 | `M-1954`, `M-1267`, `M-1973` |
| `533-717` | 2 | `M-376`, `M-391` |
| `360-520-919-140` | 1 | `M-355` |
| `603` | 1 | `M-1273` |

## Decision

Demote the broad claim.

Rejected:

```text
533-717 is the marker of no-icon SEAL:R after 002-861.
```

Still live:

```text
533-717 is a candidate narrower subclass marker or appositional tail
inside Mohenjo-daro no-icon SEAL:R + 002-861.
```

Why:

```text
M-355 is cuboid-convex and same-register but takes a different long tail.
M-1267 is same-register and source-visible but bare after 861.
M-1273 is same-register and source-visible but takes 603.
M-1954/M-1973 are same-register bare controls but remain source-pending.
```

The scan also found 20 small perfect-looking register cells. That means rarity plus tidy conditioning is not enough. `533-717` needs source-visible and family-blocked contrast, not just a low count.

## Next Test

Run a family-blocked contrast over the seven Mohenjo no-icon `SEAL:R + 002-861` rows:

```text
bare:       M-1954, M-1267, M-1973
533-717:    M-376, M-391
603:        M-1273
long tail:  M-355
```

The deciding question:

```text
What distributional property separates M-376/M-391 from the source-visible controls?
```

Candidates to test:

```text
object subtype: cuboid-convex vs rectangular
left-frame class before 002-861
distance from 861 to physical edge
copy/source-family collapse of M-376/M-391
same-register licensing of multiple post-861 tail types
```

No sign value, phonetic reading, language identity, or translation is accepted.
