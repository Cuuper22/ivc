# 032-002-Y Source-Function Batch 2

Date: 2026-05-26

## Result

Second source-volume batch adds four usable row-level witnesses and rejects two false source-image upgrades.

Usable source-visible rows:

| row | role | status |
|---|---|---|
| `M-49` | target non-core `240-220-032-002-300...` | source-visible row-level witness |
| `M-21` | outside `032-002-861` control | source-visible row-level witness |
| `M-375` | non-240 `A-220-032-002-820` control | source-visible row-level witness |
| `H-597` | outside `032-002-861` control | source-visible row-level witness |

Rejected as source-function witnesses for now:

| row | reason |
|---|---|
| `M-174` | OCR hit points to data/register rows, not an inscription panel |
| `M-221` | OCR hit points to prose/context page, not an inscription panel |

Accepted evidence status: row-level source visibility now exists for target, non-240 A-220, and outside-control rows across `Y=861`, `Y=820`, `Y=817`, and non-core `Y=300`.

Not accepted: token-level segmentation, exact source/local sign mapping, sign value, phonetic reading, language identity, allography, or translation.

## Data Stored

- `data/open_prototype/reports/campaign_032_002_y_source_function_batch2.csv`
- `tmp/032_002_y_source_function_batch/source_volume_batch2_label_context_crops_manifest.csv`
- `tmp/032_002_y_source_function_batch/m49_m21_fullpanel_recrops_manifest.csv`
- `tmp/032_002_y_source_function_batch/source_volume_batch2_contact_sheet.png`

Primary crop files:

- `tmp/032_002_y_source_function_batch/M49_target_300_fullpanel_a.png`
- `tmp/032_002_y_source_function_batch/M21_outside_861_fullpanel_a.png`
- `tmp/032_002_y_source_function_batch/M375_non240_820_hit2_india_0128_label_context.png`
- `tmp/032_002_y_source_function_batch/H597_outside_861_pakistan_0331_label_context.png`

## Row Notes

### `M-49`

Local row:

```text
+527-550-240-220-032-002-300-350-032-190+
```

Source route:

```text
India page n58 / India_0058.djvu / labels M-49 A and M-49 a
```

Result:

- source image present
- one continuous signband visible
- row is poor but source-visible
- target contrast row because it has `240-220-032-002` with non-core `Y=300` and an extended tail

This row matters because it tests whether `240-220-032-002` requires the core `861/820/817` ending or can branch into a different compound/tail.

### `M-21`

Local row:

```text
+350-001-740-362-692-032-002-861+
```

Source route:

```text
India page n48 / India_0048.djvu / labels M-21 A and M-21 a
```

Result:

- source image present
- one continuous signband visible
- outside-control `032-002-861` row is source-visible at row level

This row matters because it proves `032-002-861` is not exclusive to `A-220`.

### `M-375`

Local row:

```text
+740-100-233-220-032-002-820+
```

Source route:

```text
India page n128 / India_0128.djvu / labels M-375 A and M-375 a
```

Result:

- source image present
- one continuous signband visible
- non-240 `A-220-032-002-820` row is source-visible at row level
- object type is `SEAL:R`, giving a register contrast against square seal rows

This row matters because it gives a source-visible `Y=820` non-240 A-220 control outside the dominant square-seal shape.

### `H-597`

Local row:

```text
+740-390-590-070-032-002-861+
```

Source route:

```text
Pakistan pdf page 332 / Pakistan_0331.djvu / labels H-597 C and H-597 c
```

Result:

- source image present
- one continuous signband visible
- outside-control `032-002-861` row is source-visible at row level
- local has two identical text rows, reducing side-mapping risk for row-level use

This row matters because it gives a Harappa outside-control witness for the same `032-002-861` packet.

### `M-174`

Local row:

```text
+740-923-220-032-002-820+
```

Result:

- current OCR hit is not a source-image panel
- source-function status remains pending

### `M-221`

Local row:

```text
+740-760-335-220-032-002-820+
```

Result:

- current OCR hit is not a source-image panel
- source-function status remains pending

## Running Source-Function Table

Source-visible row-level witnesses so far:

| row | category | Y | source status |
|---|---|---:|---|
| `M-722` | target `240-220-032` | `817` | visible |
| `M-49` | target `240-220-032` | `300` | visible |
| `H-444` | non-240 `A-220-032` | `861` | visible |
| `M-375` | non-240 `A-220-032` | `820` | visible |
| `M-21` | outside `032` | `861` | visible |
| `H-597` | outside `032` | `861` | visible |

Side-gated or not yet usable:

| row | issue |
|---|---|
| `M-1385` | source object visible, local-row side mapping unresolved |
| `M-174` | data/register hit only |
| `M-221` | prose/context hit only |

## Decision

The source layer now supports the existence of the `032-002-Y` packet in target, non-240 A-220, and outside-control contexts.

The current source-visible evidence still does not decide whether `861`, `820`, and `817` are interchangeable terminal choices or separate `002-Y` branches. It does show that the packet itself is not only a catalog artifact.

## Next Batch

1. Add token-level boxes for `M-722`, `M-49`, `H-444`, `M-375`, `M-21`, and `H-597`.
2. Continue with Chanhu-daro rows `C-65`, `C-10`, and `C-60`.
3. Resolve local source-reference target rows `M-1728` and `M-240`.
4. Keep `M-174`, `M-221`, and `M-1385` out of source-function counts until real panel mapping exists.

The next decision is no longer whether the packet exists. It is whether source-clean `Y` choices pattern by frame, object type, iconography, or neighbor context.
