# Lipi 034 M-1206 415 Companion Context Inventory

Date: 2026-05-26

This note counts, rather than argues. One object, `H-938`, carries two inscriptions that sit suggestively close together, and an argument was being built on it. A single suggestive object is worth nothing until you check how often the same pairing occurs elsewhere. So this note inventories every local row with the same three-sign frame and lists what else is written on the same object.

## Question

Is the `H-938` same-object `034/415` pressure an isolated cherry-picked fact, or does the local `+520-220-415+` frame — the recurring three-sign string being tracked — repeatedly appear with `034/700` companion sides?

## Inputs

Primary local input:

```text
data/open_prototype/lipi/metadata_filtered.csv
```

Generated reports:

```text
data/open_prototype/reports/lipi_034_m1206_415_companion_context_inventory.csv
data/open_prototype/reports/lipi_034_m1206_415_companion_context_inventory_summary.json
```

The scan uses exact local rows whose text is:

```text
+520-220-415+
```

It then records other local rows on the same `cisi` object.

## Result

Exact local `+520-220-415+` rows:

```text
17 rows
16 unique objects
14 rows with at least one companion local row
```

Rows with a same-object `034/700` companion:

| Object | Exact row | Companion row | Current source status | Use |
| --- | --- | --- | --- | --- |
| `H-319` | `1341.1 +520-220-415+` | `1341.2 +700-034+` | register-only in checked layer | acquisition target |
| `H-938` | `1818.1 +520-220-415+` | `1818.2 +034-700+` | source-panel audited clean | source-grade same-object pressure |
| `H-939` | `1819.2 +520-220-415+` | `1819.1 +700-034+` | source-visible same page, but not upgraded in strict review | local/source caution pressure |
| `H-1284` | `4069.1 +520-220-415+` | `4069.2 +700-034+` | route-dark in checked layer | acquisition target |

One additional row has a `032/700` companion:

```text
H-2146 841.1 +520-220-415+ | 841.2 +700-032+
```

No exact `+520-220-415+` row in this inventory has a `033/700` companion.

## Adjudication

Adjudication is the ruling on what the counts above are allowed to support. The local `034/700` companion pattern is repeated enough to matter as acquisition pressure: four of the 17 exact `+520-220-415+` rows have same-object `+700-034+` or `+034-700+` companions. After the `H-938 B` component probe, this must not be read as component-level `034/415` support. It says the local catalog pattern is worth pursuing; it does not say the `034` component matches the `415` component.

But source grade is the hard filter. Only `H-938` is currently source-panel-audited as a clean same-object pressure case. `H-939` is source-visible on the same CISI page but failed to become a secure `415` recurrence in the strict visual packet. `H-319` and `H-1284` stay acquisition targets.

## Decision

This preserves the M-1206 branch — one open line of investigation — as a sign-inventory problem, but only at the local/source-acquisition level:

```text
local +520-220-415+ sometimes co-occurs on the same object with +700-034+ / +034-700+
```

It does not prove:

```text
034 = 415
034/415 allography
034 or 415 value
function
translation
```

Next source move from this inventory:

```text
1. Keep H-938 as the only clean same-object source-grade pressure unit.
2. Recheck H-939 only as a source-visible caution case, not a promoted recurrence.
3. Acquire H-319 and H-1284 source panels before using their local companion pattern.
```
