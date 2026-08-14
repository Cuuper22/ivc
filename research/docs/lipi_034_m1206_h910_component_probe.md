# Lipi 034 M-1206 H-910 Component Probe

Date: 2026-05-26

This note is a probe — a quick, bounded check — using one object as a mirror of another. `H-938 B` carries two signs in one order; `H-910 B` carries the same two signs in the opposite order. Comparing them tells you which drawn shape belongs to which sign code, because the shapes should swap sides if the codes do. That is a stronger test than looking at either object alone.

## Question

Does the source-visible `H-910 B` side:

```text
+700-034+
```

clarify the component assignment after the `H-938 B` probe weakened direct `034/415` support?

This is a sign-inventory and direction/order test. It is not a value or translation test.

## Inputs

Source page:

```text
CISI Pakistan IA leaf n372 / printed p. 338
HARAPPA 899-911 TABLETS incised no iconography
```

Downloaded source image:

```text
tmp/h910_component_probe/cisi_pakistan_n372_w1200.jpg
sha256: b7e45ae1441fbad5bb6ae8350c71e75a196dc6530d2801c6d4357e3a263fb610
```

Reports:

```text
data/open_prototype/reports/lipi_034_m1206_h910_component_probe_crops.csv
data/open_prototype/reports/lipi_034_m1206_h910_component_probe_adjudication.csv
data/open_prototype/reports/lipi_034_m1206_h910_component_probe_summary.json
```

Visual sheets:

```text
tmp/h910_component_probe/h910_component_probe_contact_sheet.png
tmp/h910_component_probe/h938_h910_component_order_comparison.png
```

## Result

`H-910 B` is the useful mirror-order check that `H-938 B` needed.

Visible `H-910 B` components:

- left loop/leaf component;
- right vertical/rake component.

The local row is:

```text
+700-034+
```

Under the local `R/L` assumption — the corpus field recording that the inscription is read right-to-left — the first token maps to the rightmost visible component. That gives:

| Object | Local row | Visible component assignment under `R/L` |
| --- | --- | --- |
| `H-938 B` | `+034-700+` | `034` = right loop/leaf; `700` = left vertical/rake |
| `H-910 B` | `+700-034+` | `700` = right vertical/rake; `034` = left loop/leaf |

So the two source-visible companion sides agree against the simplest `034=415` story:

```text
034 tracks the loop/leaf component.
700 tracks the vertical/rake component.
415/M-1206 target is the vertical-bundle/rake family.
```

## Consequence

This is actual negative decipherment progress. It does not just say "unclear." It pushes the live branch away from direct component-level `034/415` identity.

Accepted:

```text
H-910 is source-visible at CISI Pakistan n372 / printed p. 338.
H-910 B is a clean two-panel locator already recorded in the IA visual inspection layer.
H-910 B gives a mirror-order component check against H-938 B.
Under local R/L, H-910 and H-938 both assign 034 to the loop/leaf component, not the vertical/rake component.
```

Not accepted:

```text
034 = 415
034/415 allograph status
034 value
700 value
415 value
side function
translation
```

## Next Research Move

The next useful witness — a single source panel offered as evidence — is not another broad `034` scrape. It is a source-visible object that can test one of these two possibilities:

1. The local `R/L` mapping is correct, in which case `034` is probably not the vertical `415`-like component in FRAME700 companion sides.
2. The local direction/order mapping fails for these panels, in which case the sign equation is unresolved until source transcription notes decide the side/order convention.

Either way, `H-910` makes the direct `034/415` allograph route weaker, not stronger.
