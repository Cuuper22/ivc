# 032-002-Y Leave-One-Block Campaign

Date: 2026-05-26

## Result

The `A-220-032 -> 002 -> Y` signal survives removing Mohenjo-daro `SEAL:S`, but the claim narrows.

Promote:

```text
A-220-032-002-{861,820,817}
= live short continuation / closure formula
```

Demote:

```text
861/820/817 = broad script-level closure class
```

The current evidence supports a formulaic tail packet, strongest in Mohenjo-daro `SEAL:S` but not reducible to that block.

Accepted lexical values, phonetic readings, allography, language identity, and translations remain `0`.

## Data Stored

- `data/open_prototype/reports/campaign_032_002_y_selection_contrast.csv`
- `data/open_prototype/reports/campaign_032_002_y_block_summary.csv`
- `data/open_prototype/reports/campaign_032_002_y_leave_one_block_out.csv`
- `data/open_prototype/reports/campaign_032_002_y_source_manifest.csv`
- `data/open_prototype/reports/campaign_032_002_y_summary.json`

Mechanic validation: pass.

Scope:

- selection contrast rows: `12`
- block summary rows: `51`
- leave-one-block rows: `153`
- source manifest rows: `25`

## Full Contrast

Dedup units:

| outcome | A-220 | outside 032 | odds ratio |
|---|---:|---:|---:|
| `032 -> 002` | 24/55 | 16/257 | 11.66 |
| core `032-002-{861,820,817}` | 16/55 | 8/257 | 12.77 |
| core terminal tail | 14/55 | 6/257 | 14.28 |

Strict occurrences:

| outcome | A-220 | outside 032 | odds ratio |
|---|---:|---:|---:|
| `032 -> 002` | 24/57 | 18/457 | 17.74 |
| core `032-002-{861,820,817}` | 16/57 | 10/457 | 17.44 |
| core terminal tail | 14/57 | 8/457 | 18.27 |

The main function signal is still the first step: `A-220-032` makes `002` much more likely than generic `032`.

## Conditional Y Behavior

Among rows that already have `032-002`:

| outcome | A-220 dedup | outside dedup | odds ratio |
|---|---:|---:|---:|
| `Y in {861,820,817}` | 16/24 | 8/16 | 2.00 |
| Y terminal | 16/24 | 9/16 | 1.56 |
| core Y and terminal | 14/24 | 6/16 | 2.33 |

This means the big jump is from `032` into `002`. Once `032-002` exists, `861/820/817` are preferred but not exclusive.

## Mohenjo-daro SEAL:S Removal

Strict occurrences after removing Mohenjo-daro `SEAL:S`:

| outcome | A-220 | outside 032 | odds ratio |
|---|---:|---:|---:|
| `032 -> 002` | 6/28 | 12/387 | 8.52 |
| core `032-002-{861,820,817}` | 5/28 | 6/387 | 13.80 |
| core terminal tail | 5/28 | 6/387 | 13.80 |

The absolute A-220 rate drops hard, because Mohenjo-daro `SEAL:S` carries:

- 18/24 A-220 `032 -> 002` strict cases
- 11/16 A-220 core strict cases
- 9/14 A-220 core terminal strict cases

But the contrast does not collapse. The off-block A-220 rows still heavily prefer `032-002-{861,820,817}` over outside `032`.

## Block Shape

Top strict blocks:

| site/type | A-220 total | A-220 next `002` | A-220 core | outside total | outside next `002` | outside core |
|---|---:|---:|---:|---:|---:|---:|
| Mohenjo-daro `SEAL:S` | 29 | 18 | 11 | 70 | 6 | 4 |
| Harappa `SEAL:S` | 7 | 2 | 1 | 21 | 3 | 2 |
| Mohenjo-daro `SEAL:R` | 6 | 1 | 1 | 14 | 2 | 0 |
| Chanhu-daro `SEAL:S` | 2 | 2 | 2 | 16 | 1 | 1 |
| Kalibangan `SEAL:S` | 1 | 1 | 1 | 2 | 0 | 0 |

This is not a single-row accident. It is still small outside Mohenjo-daro `SEAL:S`, but it appears across more than one site/type block.

## Decision

### Keep

`A-220-032` is a continuation environment that strongly favors `002`.

### Promote Carefully

`A-220-032-002-{861,820,817}` is a live short continuation / closure packet.

### Demote

`861/820/817` as a broad script-level closure class. Outside `A-220`, those signs occur after `032-002`, but rarely enough that the broader claim is premature.

### Current Language Model

```text
A-220      = frame or domain selector
032        = hinge into continuation/tail
002        = tail-lane marker
861/820/817 = compact ending choices inside the tail packet
```

`240` mainly selects entry into `240-220-032`; it does not yet prove a distinct Y distribution after `002`.

## Source Manifest

Stored source-check manifest: `campaign_032_002_y_source_manifest.csv`.

It contains 25 rows:

- 5 target `240-220-032-002-Y` rows
- 12 non-240 `A-220-032-002-{861,820,817}` controls
- 8 outside `032-002-{861,820,817}` controls

Each row requires the same checks:

```text
same physical line
032 distinct from neighbors
002 distinct
Y distinct
direction/order policy
no break between 032-002-Y
tail continues or terminates as coded
```

P0 decision batch:

- targets: `C-65`, `M-1728`, `M-240`, `M-49`, `M-722`
- non-240 controls: `C-10`, `H-444`, `K-145`, `M-1044`, `M-174`, `M-720`, `M-91`
- outside controls: `C-60`, `H-140`, `M-1677`, `M-1045`, `M-21`, `M-1385`

## Next Campaign

Run the `032-002-Y source-function batch`.

Question:

```text
Are 861, 820, and 817 interchangeable terminal choices after 032-002,
or does each belong to a different subformula/context?
```

Do not run another sensitivity-only pass first. The next work must source-check the P0 batch and classify the rows by visual line, terminality, site/type, iconography, and immediate neighbors.

Decision rule:

- If source-clean target and control rows show the same `032-002-Y` packet and Y values move across frames, keep the closure-choice model.
- If each Y value separates by site/type/iconography/neighbors, split the Y class into separate `002-Y` branches.
- If source panels break `032-002-Y` continuity, quarantine those rows and rerun the function model.

## Bottom Line

The evidence is now strong enough to treat this as a real decipherment packet:

```text
A-220-032-002-{861,820,817}
```

Not a translation. A structural grammar target.
