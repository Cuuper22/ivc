# 032-002-Y Source-Function Batch 3: Chanhu-daro

Date: 2026-05-28

## Result

Mackay's public `Chanhu-Daro Excavations, 1935-36` scan gives two usable row-level witnesses and one provenance-only target.

| row | role | source status | reading impact |
|---|---|---|---|
| `C-10` | non-240 `A-220-032-002-817` | source-visible row-level witness | makes `817` portable outside the `240-220-032` target frame |
| `C-60` | outside `032-002-861` | source-visible row-level witness | adds a Chanhu-daro outside-control witness for `002-861` |
| `C-65` | target `240-220-032-002-861` | object/provenance found, public plate too dark for row use | still the highest-value target `861` row, but it cannot be counted from this scan |

Mechanic status: PASS on table/crop coherence.

## Data Stored

- `data/open_prototype/reports/campaign_032_002_y_source_function_batch3_chanhudaro.csv`
- `data/open_prototype/reports/campaign_032_002_y_source_function_current_table.csv`
- `data/open_prototype/reports/campaign_032_002_y_source_function_current_summary.csv`
- `tmp/chanhudaro_mackay_1943/chanhudaro_mackay_1943.pdf`
- `tmp/chanhudaro_mackay_1943/crops_final/chanhudaro_c10_c60_c65_crops_manifest.csv`
- `tmp/chanhudaro_mackay_1943/crops_final/chanhudaro_c10_c60_c65_contact_sheet.png`

Primary crops:

- `tmp/chanhudaro_mackay_1943/crops_final/C10_non240_817_plateLI_no29_context.png`
- `tmp/chanhudaro_mackay_1943/crops_final/C10_non240_817_plateLI_no29_signband.png`
- `tmp/chanhudaro_mackay_1943/crops_final/C60_outside_861_plateLII_no24_context.png`
- `tmp/chanhudaro_mackay_1943/crops_final/C60_outside_861_plateLII_no24_signband.png`
- `tmp/chanhudaro_mackay_1943/crops_final/C65_target_861_plateLII_no19_public_dark.png`

## Row Notes

### `C-10`

Local row:

```text
+740-231-220-032-002-817+
```

Source route:

```text
Mackay 1943 Plate LI:29 / CH 2297
```

Use:

- one-line signband visible in the public plate
- local row has one side
- `032-002-817` can now be counted as a source-visible non-240 A-220 branch

This is the first source-visible row that blocks treating `817` as a target-only or `240`-selected ending.

### `C-60`

Local row:

```text
+740-176-032-002-861+
```

Source route:

```text
Mackay 1943 Plate LII:24 / CH 2605
```

Use:

- one-line signband visible in the public plate
- local row has one side
- adds a cross-site outside-control `032-002-861` row

This makes `002-861` the best portable branch in the current source-clean layer: it appears in outside controls at Mohenjo-daro, Harappa, and Chanhu-daro, plus in a non-240 A-220 frame.

### `C-65`

Local row:

```text
+000-100-240-220-032-002-861+
```

Source route:

```text
Mackay 1943 Plate LII:19 / CH 2428
```

Use:

- object/provenance route found
- public plate face is too dark to read the row
- do not count as source-visible target `861`

This row remains critical because it would decide whether target `240-220-032` can close with `861` at Chanhu-daro. It needs a better scan/photo, not more inference from the current public plate.

## Current Source-Clean Branch Table

Count only rows with `source_visible=yes`.

| category | source-visible branches |
|---|---|
| target `240-220-032` | `817` terminal (`M-722`), `300` extended (`M-49`) |
| non-240 `A-220-032` | `861` terminal (`H-444`), `820` terminal (`M-375`), `817` terminal (`C-10`) |
| outside `032` | `861` terminal (`M-21`, `H-597`, `C-60`) |

Rows not counted:

| row | reason |
|---|---|
| `C-65` | target `861`, public plate too dark |
| `M-1385` | outside `817`, source object visible but side/local-row mapping unresolved |
| `M-174`, `M-221` | non-240 `820`, current hits are not inscription panels |

## Reading Model Update

The packet is no longer just "core endings after `032-002`." The better current model is:

```text
A-220-032 -> 002 -> branch
```

Branch behavior so far:

- `002-861`: strongest portable branch. It is source-visible outside `A-220` across three sites and also appears in a non-240 A-220 row.
- `002-820`: source-visible inside non-240 A-220 only so far. Target `820` depends on `M-1728`; outside extended `820` depends on `M-1677` or `M-1045`.
- `002-817`: now source-visible in target and non-240 A-220. Outside `817` still depends on resolving `M-1385` or acquiring `H-140`.
- `002-300...`: source-visible in target as an extended branch, not a compact terminal.

The current evidence weakens "Y is selected by `240`." Non-240 A-220 can take all three core Y values. The live question is whether Y marks a lexical/class branch, a grammatical ending class, or an object/register-conditioned formula after `002`.

## Next Discriminators

1. `M-1728`: target `002-820`, needed to test whether target can take `820`.
2. `M-240`: target extended `002-861-603`, needed to test whether `861` is branch-head plus continuation rather than an ending.
3. better `C-65`: target terminal `002-861`, needed for cross-site target `861`.
4. `H-140` or resolved `M-1385`: outside `002-817`, needed to test portability of `817` outside A-220.
5. `M-1677` or `M-1045`: outside extended `002-820`, needed to test whether `820` can head an extended branch.

## Accepted Boundary

Accepted: source-visible row-level support for `032-002-Y` in target, non-240 A-220, and outside contexts, plus a stronger branch model.

Not accepted: token-level sign boxes, exact source/local token mapping, sign values, phonetic readings, language identity, or translation.
