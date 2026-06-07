# 032-002-Y Source-Function Batch 1

Date: 2026-05-26

## Result

First source-function batch from the reachable Pakistan source-volume lane:

| row | role | source result |
|---|---|---|
| `M-722` | target `240-220-032-002-817` | source-visible row-level witness |
| `H-444` | non-240 `A-220-032-002-861` control | source-visible row-level witness |
| `M-1385` | outside `032-002-817` control | source-visible object, but side/local-row mapping unresolved |

This is not yet a solved source-function table. It is the first row-level check that the target/control packet is physically visible in source material.

Accepted evidence status: row-level source visibility for `M-722` and `H-444`; object-level source visibility but unresolved side mapping for `M-1385`.

Not accepted: sign segmentation, exact source/local token mapping, sign value, phonetic reading, language identity, allography, or translation.

## Data Stored

- `data/open_prototype/reports/campaign_032_002_y_source_function_batch1.csv`
- `tmp/032_002_y_source_function_batch/pakistan_source_label_context_crops_manifest.csv`
- `tmp/032_002_y_source_function_batch/M722_target_817_page083_label_context.png`
- `tmp/032_002_y_source_function_batch/H444_non240_861_page310_full_panel_context.png`
- `tmp/032_002_y_source_function_batch/M1385_outside_817_hit5_page218_label_context.png`

## Row Notes

### `M-722`

Local row:

```text
+740-585-240-220-032-002-817+
```

Source route:

```text
Pakistan pdf page 83 / Pakistan_0082.djvu / label M-722 a
```

Result:

- source image present
- one continuous signband visible
- target `002-817` row is source-visible at row level
- object condition is still poor/fragmentary, so detailed sign boxes are required before treating every token boundary as source-confirmed

### `H-444`

Local row:

```text
+241-220-032-002-861+
```

Source route:

```text
Pakistan pdf page 310 / Pakistan_0309.djvu / label H-444 A
```

Result:

- source image present
- five-sign band visible on one physical line
- strong row-level source witness for a non-240 `A-220-032-002-861` control
- detailed token boxes still required before source-confirming `032`, `002`, and `861` individually

### `M-1385`

Local row:

```text
+740-760-032-002-817+
```

Source route:

```text
Pakistan pdf page 218 / Pakistan_0217.djvu / multiple source faces A1-4, B, D, E
```

Result:

- source object present
- multiple source faces visible
- current local row cannot yet be mapped to a specific source face
- keep as outside control candidate, but do not use it as a classified `032-002-817` source witness yet

## Decision

`M-722` and `H-444` are now usable row-level source witnesses for the next source-function table.

`M-1385` is not yet usable for the functional contrast because the source face/local row bridge is unresolved.

## Next Batch

Continue the source-volume lane:

1. Crop and inspect `M-49` target non-core `002-300`.
2. Crop and inspect `M-21` outside `002-861`.
3. Crop and inspect `M-174` and `M-221` non-240 controls.
4. Add token-level boxes for `M-722` and `H-444`, targeting `032`, `002`, and Y.
5. Resolve `M-1385` side mapping before using it as an outside control.

The next decision is whether source-clean target/control rows show the same physical `032-002-Y` packet, or whether the apparent tail is partly a catalog/side-policy artifact.
