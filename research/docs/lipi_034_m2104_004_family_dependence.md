# Lipi 034 M-2104 004 Family Dependence

Date: 2026-05-25

Question:

```text
How many independent evidence units does the +400-097-700-004 comparator side actually provide for the M-2104 count-compound hypothesis?
```

## Result

The `004` side is source-visible, but the naive count of four rows is wrong.

```text
Naive rows:       M-478, M-479, M-480, M-1425 = 4
Evidence units:   {M-478/M-479/M-480}, {M-1425} = 2
```

The India group is one tight tablet-family unit. M-1425 is a provisional second recurrence, not a settled independent proof.

## Sources Checked

Stored source crops:

- `tmp/cisi_m2104_packet/family_dependence/cisi_india_n19_tablet_duplicates_moulds_crop.png`
- `tmp/cisi_m2104_packet/family_dependence/cisi_india_n150_m478_m480_plate_family_crop.png`
- `tmp/cisi_m2104_packet/family_dependence/cisi_india_n835_m476_m481_data_rows_crop.png`
- `tmp/cisi_m2104_packet/family_dependence/cisi_pakistan_n227_m1425_plate_crop.png`

Stored reports:

- `data/open_prototype/reports/lipi_034_m2104_004_family_dependence_objects.csv`
- `data/open_prototype/reports/lipi_034_m2104_004_family_dependence_weights.csv`
- `data/open_prototype/reports/lipi_034_m2104_004_family_dependence_summary.json`

## Why The Row Count Drops

CISI's own introduction warns that tablets often occur as identical duplicates, are sometimes mass-produced in moulds, and can be found in close groups. The same introduction then discusses `M-478/M-479` together as the relevant four-plus-U tablet case.

That makes `M-478/M-479/M-480` useful, but dangerous. They are:

- same CISI India plate cluster, leaf `n150`
- same object class: `TAB:B`
- same material: clay
- same direction: `R/L`
- same full local text: `+400-097-700-004+`
- adjacent catalogue family: `M-478/M-479/M-480`
- visually close formula-family tablets

So they are one evidence unit, not three.

## Object-Level Result

| Object | Status | Weight |
| --- | --- | --- |
| `M-478` | strongest public India crop; survives first blind visual gate | family-primary witness |
| `M-479` | source-visible local extra; paired with M-478 in CISI introduction | family-support witness |
| `M-480` | same-plate same-formula witness, weaker crop | family-support witness |
| `M-1425` | separate Pakistan-volume plate, survives provisionally | provisional independent recurrence |

This keeps the M-2104 contrast alive:

```text
M-2104: +151-097-700-034+
004 side: one strong India family unit + one provisional Pakistan recurrence
```

It also blocks exaggeration:

```text
Do not say: four independent 004 witnesses.
Say: two adjudicated 004-side evidence units, one of them provisional.
```

## Current Adjudication

Accepted:

- `M-478/M-479/M-480` are source-visible family-level witnesses for the `700-004` visual test.
- `M-1425` is a provisional second visual recurrence.
- The M-2104 count-compound hypothesis still survives as a source-targeted candidate.

Rejected or quarantined:

- No `004 = four` mapping is accepted.
- No `034 = three` mapping is accepted.
- No `700` role or value is accepted.
- No translation is accepted.
- The India same-plate family cannot be counted as three independent votes.

## Next Gate

The next actual test is a blinded segmentation/weighting pass with this unit policy:

```text
EU_004_INDIA_478_479_480 = 1 family-level unit
EU_004_PAKISTAN_1425     = 1 provisional unit
EU_034_TARGET_2104       = 1 source-gated target unit
```

The hypothesis dies if M-2104 fails exact three-stroke segmentation or if M-1425 collapses into the same copy family as the India tablets.
