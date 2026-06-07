# 032-002-Y Token-Box Scaffold v1

Date: 2026-05-28

## Result

The first token-box pass tests the hostile failure condition: whether `032`, `002`, and Y are physically distinct, adjacent signs on the same source-visible signband.

This pass uses provisional local-to-Mayig shape anchors:

| local token | provisional shape anchor | visual cue used |
|---|---|---|
| `032` | `P145 / W032 / M087` | two full-height vertical strokes |
| `002` | `P122 / W002 / M099-M100` | two adjacent half-height vertical strokes |
| `817/861` | `P385 / W817-W861 / M267` | leaf/diamond-like terminal family |
| `820` | `P378 / W820 / M391` | wheel/spoked shape |
| `300` | `P205` pressure | ray/prism branch head, not closure-family |

Stored artifacts:

- `data/open_prototype/reports/campaign_032_002_y_token_box_scaffold_v1.csv`
- `data/open_prototype/reports/campaign_032_002_y_token_box_scaffold_v1_summary.json`
- `tmp/032_002_y_token_box_scaffold_v1/token_box_scaffold_contact_sheet.png`

Status counts:

| status | rows |
|---|---:|
| candidate pass | 6 |
| candidate pass, low-res | 1 |
| candidate weak | 1 |

## Row Outcomes

| row | branch | token-box status | consequence |
|---|---|---|---|
| `M-722` | target `002-817` | candidate pass | target `817` scaffold survives |
| `H-444` | non-240 `002-861` | candidate pass | non-240 `861` scaffold survives |
| `M-49` | target `002-300...` | candidate pass | non-core target branch survives as extended, not closure |
| `M-21` | outside `002-861` | candidate pass | outside `861` scaffold survives |
| `M-375` | non-240 `002-820` | candidate pass, but edge-cropped | `820` scaffold survives provisionally; needs wider recut |
| `H-597` | outside `002-861` | candidate pass, but dark | outside Harappa `861` survives provisionally; needs stronger crop |
| `C-10` | non-240 `002-817` | candidate pass, low-res | Chanhu-daro `817` survives as pressure, not final token identity |
| `C-60` | outside `002-861` | candidate weak | row-level source witness stands; token identity needs better image |

## Interpretation

The scaffold does not kill the branch model. Across target, non-240 A-220, and outside rows, the packet is boxable as same-line adjacent material in the source-visible layer.

It also does not finish the source gate. Three rows require stronger treatment before being treated as high-confidence token-level evidence:

- `M-375`: recut wider right edge so `820/P378` is not clipped.
- `H-597`: improve dark signband contrast and rebox `032/P145` vs `002/P122`.
- `C-60`: acquire a better Plate LII / CH 2605 image before using token identity.

## Research Consequence

The next model decision can move past "is `032-002-Y` a pure catalog adjacency?" for the current scaffold, but only at candidate level. The live split remains:

```text
A-220-032 -> 002 -> Y/continuation
```

with three rival interpretations:

- Y as closure choice: strongest for `817`, plausible for `861/820`.
- Y as branch head: required for `300`, possible for extended `861/820` rows.
- Y as register/iconographic/admin code: still live because the source-clean set is seal-heavy and Bull1-heavy.

## Next Use

Use this scaffold to direct, not replace, the next source work:

1. Recut/reacquire weak scaffold rows.
2. Add `C-65`, `M-1728`, and `M-240` for missing target `861/820` evidence.
3. Add `H-140` or `M-1385` for outside `817`.
4. Add `M-1737`, `M-1677`, or `M-1045` for outside `820`.

Accepted: candidate token-box support for the source-visible scaffold.

Not accepted: final token segmentation, sign value, phonetic reading, language identity, or translation.
