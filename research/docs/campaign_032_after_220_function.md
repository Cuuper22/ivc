# 032 After 220 Function Campaign

Date: 2026-05-26

## Result

`032` after `A-220` behaves like a continuation or tail-selector position, not an ending.

The important split is:

```text
A-220-032      = tail-bearing continuation environment
outside 032    = mixed population, often terminal or in start/700/740 frames
240-220-032    = strongest selected member of the A-220-032 environment
```

This does not assign a value to `032`. It narrows what kind of slot it occupies.

Accepted lexical values, phonetic readings, allography, language identity, and translations remain `0`.

## Data Stored

- `data/open_prototype/reports/campaign_032_after_220_occurrence_rows.csv`
- `data/open_prototype/reports/campaign_032_after_220_strict_rows.csv`
- `data/open_prototype/reports/campaign_032_after_220_dedup_units.csv`
- `data/open_prototype/reports/campaign_032_after_220_category_summary.csv`
- `data/open_prototype/reports/campaign_032_after_220_tail_summary.csv`
- `data/open_prototype/reports/campaign_032_after_220_tail_metrics.csv`
- `data/open_prototype/reports/campaign_032_after_220_prev_context_summary.csv`
- `data/open_prototype/reports/campaign_032_after_220_internal_controls.csv`
- `data/open_prototype/reports/campaign_032_after_220_source_queue.csv`
- `data/open_prototype/reports/campaign_032_after_220_summary.json`

Mechanic validation: pass.

Scope:

- metadata rows: `5679`
- all parsed `032` occurrences: `588`
- strict `032` occurrences after removing bracketed damaged/open texts: `514`
- strict dedup units: `312`
- slash/allograph ambiguity retained and flagged, not excluded.

Definition note: row IDs can appear in more than one category because this is occurrence-level analysis. A row can contain more than one `032`.

## Category Summary

| category | strict occurrences | dedup units | terminal | next `002` | core `002-861/820/817` |
|---|---:|---:|---:|---:|---:|
| `target_240_220_032` | 9 | 9 | 2/9 | 5/9 | 4/9 |
| `non240_a_220_032` | 48 | 46 | 13/48 raw, 11/46 dedup | 19/48 raw, 19/46 dedup | 12/48 raw, 12/46 dedup |
| `outside_a_220_x_032` | 457 | 257 | 202/457 raw, 64/257 dedup | 18/457 raw, 16/257 dedup | 10/457 raw, 8/257 dedup |

The contrast is clear:

- `A-220-032` often continues into `002`.
- outside `A-220-X`, `032` almost never continues into `002` after dedupe.
- terminality does not distinguish target `240-220-032`; it is only 2/9 terminal.

## What Dies

### `032` as an ending after `240-220`

Rejected for now.

Only 2/9 `240-220-032` target rows are terminal after `032`. Non-`240 A-220-032` has similar terminality after dedupe, and outside `032` is more terminal in raw occurrences.

So the current claim is not:

```text
032 = ending
```

The current claim is:

```text
032 after A-220 usually sits at a hinge before a possible tail.
```

## What Survives

### 1. `032` after `A-220` is distributionally different from outside `032`

Outside `A-220-X`, `032` is dominated by start/700/740-heavy contexts:

- `<START>-<START>`: 95
- `<START>-700`: 95
- `<START>-740`: 40
- `400-740`: 16

Its top continuations are different too: terminal, `840`, `700`, `000`, `031`, and only rarely `002`.

Inside `A-220-032`, the `002` lane is prominent.

### 2. `240-220-032` is a strong selected member of the A-220-032 lane

The previous campaign already showed `240` strongly selects `032` after `220`.

This campaign adds that, once `032` is present, the target tail behavior is not unique enough to call it a separate function. It looks like a strong local member of the broader `A-220-032 -> 002-tail` pattern.

### 3. The `002` tail is now the next clue

Target `240-220-032`:

- `002-861`: `C-65`, `M-240`
- `002-820`: `M-1728`
- `002-817`: `M-722`
- `002-300...`: `M-49`

Non-`240 A-220-032` also has the same kind of lane:

- `002-861`: 5 strict cases
- `002-820`: 4 strict cases
- `002-817`: 3 strict cases

Outside `A-220-X`, those tails are rare.

## Working Function Models

### 1. Continuation / tail-selector

Best current model.

`032` after `A-220` often opens or licenses a following `002` tail. The local frame is not complete at `032`.

### 2. Classifier or subtype marker

Plausible.

`032` may classify the `A-220` unit and then allow another tail to specify subcategory, object, rank, owner, or administrative extension.

### 3. Formula component

Also plausible as a surface description.

The unit may be larger than the earlier three-sign frame:

```text
A-220-032-002-Y
```

where `Y` is often `861`, `820`, or `817`.

### 4. Closure / ending

Currently weak.

`032` can close elsewhere, but not as the main behavior after `A-220`.

## Source Queue

P0 target rows:

- `C-65`: `+000-100-240-220-032-002-861+`
- `H-1678`: `+520-233-240-220-032+`
- `M-1728`: `+161-055-240-220-032-002-820+`
- `M-49`: `+527-550-240-220-032-002-300-350-032-190+`
- `M-240`: `+520-240-220-032-002-861-603+`
- `M-319`: `+740-812-033-240-220-032+`
- `M-631`: `+520-033-706-240-220-032-368-263+`
- `M-722`: `+740-585-240-220-032-002-817+`
- `M-1265`: `+740-055-240-220-032-806+`

P0 internal controls:

- `M-1990`: `+740-760-440-240-220-002-861+`
- `M-133`: `+527-550-240-220-255-812-906-388+`
- `M-369`: `+740-690-435-255-240-220-415-806-742-060-920+`

These controls matter because they test whether local `032` is visually stable against nearby alternatives `002`, `255`, and `415` in the same `240-220-X` environment.

## Next Campaign

Run the `032-002 tail campaign`.

Contrast:

```text
240-220-032-002-Y
non-240 A-220-032-002-Y
A-220-032 terminal
outside A-220 032-002-Y
outside A-220 terminal 032
```

Decision targets:

1. Does `032-002-Y` behave consistently across A-220 frames?
2. Does `240` specifically strengthen the `032 -> 002-861/820/817` lane after site/type blocking?
3. Are `861`, `820`, and `817` interchangeable tail closures, object classes, or separate branches?
4. Are terminal `A-220-032` and tail-bearing `A-220-032-002-Y` different functions?
5. Does source imagery preserve `032`, `002`, `861`, `820`, and `817` as distinct signs in the same visual policy?

## Bottom Line

The A-220-X object has expanded again:

```text
A-220-032-002-Y
```

`240-220` selects `032`, but `032` itself usually points forward. The next decipherment-relevant object is the tail system after `032`, especially `002-861/820/817`.
