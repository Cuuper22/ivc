# Vector 4 Targeted Context Nulls

Date: 2026-05-31

This is a replacement-branch targeted rerun for V4 context semantics. It is deliberately narrower than the broad discovery scan: it tests fixed tempting unit/context pairs against fast fixed-pair nulls. A pass here cannot promote a sign meaning by itself; a fail kills a lead cheaply.

## Artifacts

- `data/open_prototype/tools/vector4_targeted_context_nulls_20260531.mjs`
- `data/open_prototype/reports/vector4_targeted_context_nulls_20260531.csv`
- `data/open_prototype/reports/vector4_targeted_context_nulls_20260531_iterations.csv`
- `data/open_prototype/reports/vector4_targeted_context_nulls_20260531_summary.json`

Run command:

```powershell
node data\open_prototype\tools\vector4_targeted_context_nulls_20260531.mjs
```

The run used 2,000 iterations per null model and completed locally in about 40 seconds.

## Result

| Target | Collapse | Support | Observed z | Worst fixed-pair null >= observed | Worst null |
| --- | --- | ---: | ---: | ---: | --- |
| `407` / `Copper` | context-exact | 25 | 15.919522 | 1.000000 | shuffle units within site/type |
| `407` / `TAB:C` | context-exact | 25 | 16.395964 | 1.000000 | shuffle units within site/type |
| `061-845` / `Copper` | context-exact | 8 | 14.555993 | 1.000000 | shuffle units within site/type |
| `158-806` / `Phyt` | context-exact | 5 | 12.839621 | 0.000000 | shuffle contexts global |
| `154-806` / `SEAL:R|None` | context-exact | 11 | 8.896395 | 0.532000 | shuffle units within site/type |
| `400` / `TAB:B` | text-only | 94 | 11.800809 | 1.000000 | shuffle units within site/type |
| `407` / `Copper` | text-only | 14 | 10.831359 | 1.000000 | shuffle units within site/type |
| `158-806` / `Phyt` | text-only | 3 | 8.930802 | 0.007500 | shuffle units within site/type |

## Interpretation

The administrative/register-looking leads die cleanly. `407`, `061-845`, and `400` are reproduced by shuffling units within site/type, so they are not sign-meaning candidates.

The only live residue is `158-806 / Phyt`. It has fixed-pair null support in both collapse modes, but the harsh text-only support drops to `3`, below the broad scanner's minimum support threshold of `5`. That makes it a source-check queue item, not an accepted sign meaning. A future promotion would need source-image validation of the three text-collapsed witnesses, matched iconographic negatives, and a family-wise scan that keeps the signal after exact-text collapse.

## Claim-Ledger Effect

No count changes.

| Claim class | Increment |
| --- | ---: |
| translations | 0 |
| phonetic_values | 0 |
| sign_meanings | 0 |
| language_identification | 0 |
| structural_findings | 0 |
| external_anchors | 0 |
