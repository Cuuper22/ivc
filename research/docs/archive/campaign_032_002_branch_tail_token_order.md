# 032-002 Branch-Tail Token/Order Adjudication

Date: 2026-05-28

## Question

This note records an adjudication pass on published photographs: for four rows, we look at the image and decide what the physical layout will and will not support. Signs in this corpus are numeric IDs. A "branch tail" is the material that follows the branch sign Y in rows shaped `032-002-Y(-tail)`. A "token box" is a rectangle claiming the exact extent of one sign on the image; the broad "order windows" used here claim only sequence, not boundaries. A row is "source-visible" when it can be checked against a published photograph.

The source acquisition upgraded `M-240`, `M-91`, and `M-70` to public source-panel rows. This campaign asks the next linguistic question:

```text
Do the source-visible rows preserve real post-Y continuation on one physical sign line?
```

The answer is yes as an order-level result, not as a final token-segmentation result.

## Data Stored

- Script: `tmp/run_032_002_branch_tail_token_order_packet.py`
- Verdicts: `data/open_prototype/reports/campaign_032_002_branch_tail_token_order_verdicts.csv`
- Box/window manifest: `data/open_prototype/reports/campaign_032_002_branch_tail_token_order_boxes.csv`
- Summary: `data/open_prototype/reports/campaign_032_002_branch_tail_token_order_summary.json`
- Contact sheet: `tmp/032_002_branch_tail_token_order/032_002_branch_tail_token_order_contact_sheet.png`

Mechanic validation: PASS.

The windows in this packet are broad order windows for low-resolution source panels. They are not final token boxes.

## Verdicts

| row | branch tail | verdict | confidence | linguistic use |
|---|---|---|---|---|
| `M-49` | `002-300-350-032-190` | pass existing token box | medium | source-backed extended `300` branch with later `032` |
| `M-240` | `002-861-603` | pass tail-continuation candidate | medium | source-visible target `861` continuation and repeated global `861->603` family |
| `M-91` | `002-861-255-416` | pass low-res tail-continuation candidate | medium-low | source-visible non-target nonterminal `861`, singleton tail |
| `M-70` | `002-390-692` | pass branch-head continuation candidate | medium | source-visible `390` branch-head behavior inside adjacent `032-002` |

## What Is Now Allowed

This packet supports:

```text
source-visible post-002 continuation exists in multiple decisive adjacent rows
```

The strongest row is `M-240`, because it is both:

- inside the target `240-220-032` frame
- part of the recurring all-`002` tail family `861->603`

`M-91` matters differently: it is not yet a recurring tail family, but it independently prevents treating `861` as strictly terminal inside `A-220-032-002`.

`M-70` matters because `390` was already branch-head-like statistically, and now has a source-visible adjacent `032-002` continuation.

## What Is Still Not Allowed

Not accepted:

- exact token segmentation from the broad windows
- exact local-to-source side mapping
- phonetic value of `861`, `390`, `300`, `603`, `255`, `416`, or `692`
- semantic translation
- `820` continuation as source-normalized, because `M-1677` remains source-gated

## Research Consequence

The active model upgrades from:

```text
branch-tail grammar is live but source-normalized continuation is mostly unproven
```

to:

```text
source-visible branch-tail continuation exists for 300, 861, and 390 branches
```

That is a real syntactic step. It means the next research unit should not be another one-sign audit. It should be a branch-family campaign:

```text
861 suffix split + 390 branch-head family + recursive 032 tails
```

## Next Experiment

### `861` Suffix Split

Rows:

```text
M-240  002-861-603
M-91   002-861-255-416
M-1273 002-861-603
M-714  002-861-603
M-376  002-861-533-717
M-391  002-861-533-717
```

Question:

```text
Is 861 a closure-capable branch sign that licenses suffix/addendum tails?
```

Pass condition:

```text
Source-visible or source-routeable rows preserve 861 followed by a same-line complement, and the complements cluster into recurring families.
```

Fail condition:

```text
The continuations dissolve into side errors, damage, duplicate-family artifacts, or unrelated second units.
```

### `390` Branch-Head Family

Rows:

```text
M-70       002-390-692
3335.1    002-390-590-032
M-119/M-38/M-735/Sktd-1 002-390-125...
M-1825 and Dholavira row 4237.1 002-390-705
```

Question:

```text
Does 390 introduce a complement slot, and does later 032 mark nested structure?
```

Pass condition:

```text
390 consistently takes following material and that material falls into stable complement families.
```

Fail condition:

```text
390 tails are object-family residue or catalog segmentation noise.
```
