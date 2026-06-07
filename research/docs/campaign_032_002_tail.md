# 032-002 Tail Campaign

Date: 2026-05-26

## Result

The live construction is:

```text
A-220-032 -> 002 -> Y
```

The strongest current claim is not that `240` has its own tail meaning. It is that `A-220-032` opens a continuation lane into `002`, and `861/820/817` form the main compact ending family inside that lane.

Best current parse:

```text
A-220-032        = continuation / subtype hinge
002              = tail-lane marker after that hinge
861/820/817      = preferred short-tail ending set after 032-002
```

Accepted lexical values, phonetic readings, allography, language identity, and translations remain `0`.

## Data Stored

- `data/open_prototype/reports/campaign_032_002_tail_units.csv`
- `data/open_prototype/reports/campaign_032_002_tail_strict_rows.csv`
- `data/open_prototype/reports/campaign_032_002_tail_dedup_units.csv`
- `data/open_prototype/reports/campaign_032_002_tail_category_summary.csv`
- `data/open_prototype/reports/campaign_032_002_tail_y_distribution.csv`
- `data/open_prototype/reports/campaign_032_002_tail_target_vs_non240_contrast.csv`
- `data/open_prototype/reports/campaign_032_002_tail_block_contrast.csv`
- `data/open_prototype/reports/campaign_032_002_tail_source_queue.csv`
- `data/open_prototype/reports/campaign_032_002_tail_summary.json`

Mechanic validation: pass.

Scope:

- strict `032` occurrence rows inherited from the previous campaign: `514`
- strict frame/text dedup units inherited from the previous campaign: `312`
- total exported tail units: `826 = 514 strict + 312 dedup`
- source queue rows: `64`

Definition note: `core tail` means `032-002-Y` with `Y in {861, 820, 817}`. `core terminal tail` means that `Y` is the final sign in the tail.

## Category Summary

Dedup units:

| category | n | terminal at `032` | next `002` | core `002-861/820/817` | core terminal |
|---|---:|---:|---:|---:|---:|
| `target_240_220_032` | 9 | 2/9 | 5/9 | 4/9 | 3/9 |
| `non240_a_220_032` | 46 | 11/46 | 19/46 | 12/46 | 11/46 |
| `outside_a_220_x_032` | 257 | 64/257 | 16/257 | 8/257 | 6/257 |

Combined `A-220-032` versus outside `032`:

| outcome | A-220-032 | outside 032 | odds ratio |
|---|---:|---:|---:|
| next `002` | 24/55 | 16/257 | 11.66 |
| core `002-861/820/817` | 16/55 | 8/257 | 12.77 |
| core terminal tail | 14/55 | 6/257 | 14.28 |

This is the main signal. Generic `032` does not behave like `A-220-032`.

## Target Versus Non-240 A-220

Dedup contrast:

| outcome | `240-220-032` | non-240 `A-220-032` | odds ratio |
|---|---:|---:|---:|
| next `002` | 5/9 | 19/46 | 1.78 |
| core `002-861/820/817` | 4/9 | 12/46 | 2.27 |
| `002-Y` terminal | 3/9 | 13/46 | 1.27 |
| core terminal | 3/9 | 11/46 | 1.59 |

`240` leans harder into the tail lane, but the clean functional split is not target-specific. The shared `A-220-032` environment carries the larger signal.

Matched block check:

| site/type | target next `002` | target core | non-240 next `002` | non-240 core |
|---|---:|---:|---:|---:|
| Mohenjo-daro `SEAL:S` | 4/6 | 3/6 | 14/23 | 8/23 |
| Chanhu-daro `SEAL:S` | 1/1 | 1/1 | 1/1 | 1/1 |
| Harappa `SEAL:S` | 0/1 | 0/1 | 2/6 | 1/6 |
| Mohenjo-daro `SEAL:R` | 0/1 | 0/1 | 1/5 | 1/5 |

So `240` is still a strong entry selector for `032` after `220`, but the post-`032` behavior is mostly a broader `A-220-032` construction.

## Y Distribution

Dedup `032-002-Y` cases:

| category | `861` | `820` | `817` | other Y |
|---|---:|---:|---:|---:|
| `target_240_220_032` | 2 | 1 | 1 | 1 |
| `non240_a_220_032` | 5 | 4 | 3 | 7 |
| `outside_a_220_x_032` | 3 | 3 | 2 | 8 |

`861/820/817` are not unique to `A-220-032`, but they concentrate there because `A-220-032` much more often enters the `002` lane. Once `032-002` exists, these three are a preferred compact family, not yet separable into meanings.

## Working Function Models

### 1. Chained tail construction

Best current model.

`A-220-032` is a stem/frame or subtype hinge. `002` opens the tail lane. `861/820/817` occupy a restricted ending slot.

### 2. `240` as entry selector, not tail controller

Also strong.

The previous campaign showed `240` strongly selects `032` after `220`. This campaign shows that after `032`, the tail behavior is shared with other `A-220-032` frames. So `240` mostly gets the inscription into the construction.

### 3. Separate `002-Y` branches

Still live.

`002-861`, `002-820`, and `002-817` may be three separate short compounds rather than one interchangeable ending class. The counts are balanced enough to keep this alive.

### 4. Mohenjo-daro `SEAL:S` formula habit

Strongest countermodel.

The main target block is Mohenjo-daro `SEAL:S`, and non-240 controls in that same block also use `002` often. This could be a local seal formula family rather than a system-wide grammatical rule.

## What Dies

### `032` as the ending after `240-220`

Already rejected by the previous campaign and reinforced here.

Only 2/9 target rows stop at `032`; 5/9 continue immediately into `002`.

### `240` as a proven selector of a distinct Y value

Not supported yet.

The target has `861=2`, `820=1`, `817=1`, and non-core `300=1`. That is a small sample and does not separate `240` from the broader `A-220-032` population.

### `861/820/817` as translated values

Not supported.

They are a structural ending set for now, not meanings.

## Source Queue

P0 target witnesses:

- `C-65`: `+000-100-240-220-032-002-861+`
- `M-240`: `+520-240-220-032-002-861-603+`
- `M-1728`: `+161-055-240-220-032-002-820+`
- `M-722`: `+740-585-240-220-032-002-817+`
- `M-49`: `+527-550-240-220-032-002-300-350-032-190+`

P0 non-240 A-220 controls:

- `C-10`: `+740-231-220-032-002-817+`
- `H-444`: `+241-220-032-002-861+`
- `K-145`: `+740-585-231-220-032-002-820+`
- `M-1044`: `+520-220-032-002-861+`
- `M-174`: `+740-923-220-032-002-820+`
- `M-720`: `+000-740-923-220-032-002-817+`
- `M-91`: `+740-100-798-220-032-002-861-255-416+`

P0 outside controls:

- `H-140`: `+740-384-032-002-817+`
- `M-1385`: `+740-760-032-002-817+`
- `M-1677`: `+520-382-032-002-820-001-440-012+`
- `M-1045`: `+740-100-415-070-032-002-820-000+`
- `M-21`: `+350-001-740-362-692-032-002-861+`
- `C-60`: `+740-176-032-002-861+`

## Next Campaign

Run the `032-002-Y source and leave-one-block campaign`.

Decision tests:

1. Compare all strict dedup `032-002-Y` rows, not only `A-220`.
2. Split `A-220-032-002-Y` versus outside `032-002-Y`.
3. Score `Y in {861, 820, 817}`, immediate close after `Y`, and individual `861`, `820`, `817`.
4. Block by site/type and run leave-one-block-out without Mohenjo-daro `SEAL:S`.
5. Source-check the P0 target/control rows to confirm `032`, `002`, and `Y` are visually distinct and same-line.

Decision rule:

- If `A-220` still elevates `032-002` and compact core terminal tails after removing Mohenjo-daro `SEAL:S`, promote `A-220-032-002-Y` to a real formulaic continuation/closure packet.
- If only `032 -> 002` survives, keep `002` as the live function and demote `861/820/817` to preferred fillers.
- If source images break the segmentation or line order, quarantine the affected rows before any function claim.

## Bottom Line

The research object has moved from one sign to a construction:

```text
A-220-032-002-Y
```

The live function is a tail-bearing construction after `A-220`, not a translation. The next fork is whether `861/820/817` are a true closure class or just the most common fillers in a broader `002-Y` tail slot.
