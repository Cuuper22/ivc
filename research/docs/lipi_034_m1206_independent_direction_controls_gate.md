# Lipi 034 M-1206 Independent Direction Controls Gate

Date: 2026-05-26

## Question

After tracing `R/L` to Lipi/Yajnadevam metadata, can independent source-visible short-mark controls tell us whether recorded `R/L` behaves coherently on the image?

## Short Answer

Yes, but only as component-coherence pressure.

The three independent source-visible controls currently in hand all behave the same way under recorded `R/L`: `700` lands on the vertical/bar component, while `032` or `033` lands on a V/leaf/loop-like component.

That strengthens the H-938/H-910 conditional negative result. It does not prove the direction field from source notes, and it does not license a sign value, allograph decision, or translation.

## Controls Checked

| Control | Local text | Recorded direction | Visible components | Under recorded direction | Use |
| --- | --- | --- | --- | --- | --- |
| `H-930 B` | `+700-032+` | `R/L` | left V/leaf; right vertical/bar group | `700` = right vertical/bar group; `032` = left V/leaf | independent clean two-panel control |
| `H-789 B` | `+033-700+` | `R/L` | left vertical/bar group; right loop/oval | `033` = right loop/oval; `700` = left vertical/bar group | independent clean two-panel control, lower scan confidence |
| `H-942 B` | `+033-700+` | `R/L` | left vertical/bar group; right V/leaf | `033` = right V/leaf; `700` = left vertical/bar group | source-visible control with side-mapping caution |

Comparison packet:

```text
data/open_prototype/reports/lipi_034_m1206_independent_direction_controls_gate.csv
data/open_prototype/reports/lipi_034_m1206_independent_direction_controls_gate_summary.json
tmp/independent_direction_controls/derived/independent_direction_controls_contact_sheet_v2.png
```

New source crops:

```text
tmp/independent_direction_controls/derived/H930_B_source_panel_v2.png
tmp/independent_direction_controls/derived/H789_B_wide2.png
```

Existing source crop reused:

```text
tmp/m1206_singleton_controls/derived/h942/H942_B_panel_labeled_from_cisi_pakistan_n374.png
```

## Consequence

This is now stronger than a naked metadata assumption:

```text
recorded R/L places 700 on the vertical/bar component in independent controls.
```

That agrees with the dependent H-938/H-910 component checks:

- `H-938 B +034-700+`, recorded `R/L`: `034` = right loop/leaf, `700` = left vertical/rake.
- `H-910 B +700-034+`, recorded `R/L`: `700` = right vertical/rake, `034` = left loop/leaf.

So the current admissible result is:

```text
direct component-level 034=415 remains negative under recorded R/L;
recorded R/L is component-coherent in current controls;
recorded R/L is still not source-grade direction proof.
```

## Not Admissible Yet

The following are not useful component/direction controls in the current checked layer:

- `H-1302` and `H-1303`: real Nature 2021 direction-note leads, but no stored source-grade panels here.
- `H-2146`: local/inventory row only in this branch.
- `H-319`: CISI register/data page only, no inscription panel.
- `H-1284`: route-dark in checked CISI 1/2 layer.
- `H-939`: source-visible but not upgraded; side/component/direction use remains blocked by prior strict review.

## Boundary

Accepted:

- H-930, H-789, and H-942 B provide source-visible component-coherence support for recorded `R/L`.
- Under that working policy, `700` behaves like the vertical/bar component in the checked short-mark controls.
- The H-938/H-910 direct `034=415` component identity rejection is strengthened as a conditional result.

Not accepted:

- Source-grade proof of reading direction.
- A global `034` versus `415` sign-identity decision.
- `034=415`, allography, value, function, language identity, or translation.

## Next Gate

Acquire one stronger independent control where both side mapping and source direction are better grounded:

1. CISI/HARP panels or notes for `H-1302` and `H-1303`, because they have a published direction/corpus-correction lead.
2. Plate-grade panels for `H-2146`, the one exact `+520-220-415+` object with a `+700-032+` companion.
3. Plate-grade panels for `H-319` and `H-1284`, because they repeat the exact `+520-220-415+ | +700-034+` pattern but currently lack source images.
