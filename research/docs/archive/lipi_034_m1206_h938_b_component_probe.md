# Lipi 034 M-1206 H-938 B Component Probe

Date: 2026-05-26

This note is a probe — a quick, bounded check — that takes an argument one step further than the previous audit and finds it breaks. It was already known that one object carries both signs of interest, one on each side. That only shows the two signs sit near each other. This note asks the harder question: is the actual drawn shape behind the code `034` the same shape as the `415` controls? The answer is no.

## Question

Does the source-visible `H-938 B` companion side give component-level visual support for `034/415` allography — the claim that two codes are variants of one sign?

`H-938` is the clean same-object pressure case:

```text
H-938 A/A bis  -> local 1818.1 +520-220-415+
H-938 B        -> local 1818.2 +034-700+
```

The previous audit proved same-object proximity. This probe asks the stricter question: is the `034` component itself the vertical component that resembles the `415` controls?

## Inputs

Primary source panel:

```text
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H938_B_panel.png
```

Comparison controls:

```text
tmp/m1206_034_next_source_normalized_blind_component_control_20260526/primary_packet/N002.png
tmp/m1206_034_next_source_normalized_blind_component_control_20260526/primary_packet/N008.png
tmp/m1206_034_next_source_normalized_blind_component_control_20260526/primary_packet/N003.png
tmp/m1206_034_next_source_normalized_blind_component_control_20260526/primary_packet/N011.png
```

Contact sheet:

```text
tmp/h938_b_component_probe/h938_b_component_probe_contact_sheet.png
```

Reports:

```text
data/open_prototype/reports/lipi_034_m1206_h938_b_component_probe_crops.csv
data/open_prototype/reports/lipi_034_m1206_h938_b_component_probe_adjudication.csv
data/open_prototype/reports/lipi_034_m1206_h938_b_component_probe_summary.json
```

## Result

The result is negative for a direct component-level `034/415` match.

`H-938 B` has two visible components:

- a left vertical component;
- a right loop/cross component.

The left vertical component is the one that visually resembles the M-1206 target terminal and the `H-938 A/A bis` exact-side `415` controls.

But under the local row's `R/L` order assumption — the corpus field recording that the inscription is read right-to-left — for:

```text
+034-700+
```

the first local token, `034`, should be the rightmost visible component, not the left one. Under that assumption, the candidate `034` is the right loop/cross component, which is not close to the vertical `415` family.

## Adjudication

Adjudication is the ruling on what each observed component is allowed to support.

| Component | Visual relation to `415` family | Local-order implication | Status |
| --- | --- | --- | --- |
| `H-938 B` left vertical component | Closest B-side component to M-1206 and H-938 A/A bis `415` controls. | Candidate `700` under local `R/L` order assumption; candidate `034` only if side/order convention flips. | Not accepted as `034/415` support. |
| `H-938 B` right loop/cross component | Not close to the vertical `415` family. | Candidate `034` under local `R/L` order assumption. | Negative pressure against simple visual `034=415`. |
| `H-938 B` full signband | Source-visible companion side on the same object as exact `415` side. | Whole-side mapping is accepted; component mapping remains order-sensitive. | Same-object proximity only. |

## Consequence

This sharpens the branch.

`H-938` remains valuable because it is source-grade same-object pressure:

```text
one side: exact +520-220-415+
companion side: +034-700+
```

But it should not be used as component-level evidence that `034` visually matches `415`.

The live M-1206 explanation space remains:

- allograph/broad graphemic family;
- separate visual-family signs;
- source-side or direction artifact;
- transcription-policy split.

This probe weakens the simplest allograph story and strengthens the need for independent source-visible `034` witnesses where the component can be assigned without direction ambiguity.

## Claim Status

```text
accepted source-grade same-object proximity: yes, inherited from H-938 audit
accepted H-938 B component-level 034/415 match: no
accepted 034=415: no
accepted allograph decision: no
accepted sign value: no
accepted translation: no
```

