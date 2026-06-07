# H-786 / H-941 Source-A Pattern Recheck

Date: 2026-05-26

## Question

```text
Do the actual source panels show a consistent side-label pattern for the target-like 415 terminal family, or is H-786/H-941 only a bookkeeping ambiguity?
```

This follows the H-786/H-941 side-mapping adjudication. The point is linguistic/source-critical: decide how much weight the source-visible panels can carry in the `034/415` terminal-family branch.

## Evidence Checked

Source crops already verified by hash and crop bounds:

```text
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H786_A_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H786_B_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H938_A_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H938_A_bis_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H938_B_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H939_A_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H939_A_bis_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H939_B_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H939_B_bis_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H940_A_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H940_B_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H941_A_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H941_A_bis_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H941_B_panel.png
tmp/m1206_m37_blind_visual_comparanda/derived/verified_panel_crops/H941_B_bis_panel.png
```

Local rows checked from:

```text
data/open_prototype/lipi/metadata_filtered.csv
data/open_prototype/reports/lipi_034_m1206_m37_415_fine_form_inputs.csv
data/open_prototype/reports/h786_h941_h938_h940_415_side_policy_gate_adjudication.csv
```

## Pattern

The target-like visual pattern is the broad three-class side:

```text
triangular/pennant-on-stem -> split-leaf/fork -> rake/vertical-bundle
```

That pattern is source-visible on:

```text
H-786 A
H-938 A / A bis
H-940 A
H-941 A / A bis
```

It is not target-grade on:

```text
H-786 B
H-938 B
H-940 B
H-941 B / B bis
```

`H-939` is the stress case. Its local exact `+520-220-415+` row is `.2`, but `H-939 B/B bis` is not target-grade. `H-939 A` has a partial target-like pattern under damage/occlusion, while local `.1` is `+700-034+`. This prevents upgrading H-939, but it also shows why row number cannot be treated as source side.

## Decision

The source-panel pattern is real enough to change the wording:

```text
H-786 A and H-941 A/A bis are not just arbitrary attractive panels.
They belong to a repeated source-A target-like pattern also seen in the clean exact-side controls H-938 A/A bis and H-940 A.
```

But the missing bridge remains:

```text
No checked source table maps H-786 A to local 1677.2.
No checked source table maps H-941 A/A bis to local 1821.2.
```

So the admissibility bins are:

```text
accepted exact-source-side 415 controls:
H-938 A/A bis
H-940 A

source-A target-like candidate exact-row reconciliations:
H-786 A
H-941 A/A bis

stress / do-not-upgrade:
H-939 A partial under damage, H-939 B/B bis not target-grade

excluded as 415 controls:
H-786 B
H-938 B
H-940 B
H-941 B/B bis
```

## Research Consequence

This strengthens the source-visible recurrence side of the `415` terminal-family pool. It makes the local row-order assumption weaker and makes source-side visual recurrence stronger.

It does not settle the branch:

- It does not prove `H-786 A = 1677.2 +520-220-415+`.
- It does not prove `H-941 A/A bis = 1821.2 +520-220-415+`.
- It does not override the H-938/H-910 component-order negative pressure against direct `034=415` under recorded `R/L`.
- It does not give `034`, `415`, or any sign a value.
- It does not translate anything.

## Next Gate

Find object-specific side/transcription notes from CISI/HARP/Mahadevan/ICIT or source-holder replies that explicitly connect:

```text
H-786 A/B -> 1677.1 / 1677.2
H-941 A/B -> 1821.1 / 1821.2
H-939 A/B -> 1819.1 / 1819.2
```

Until then, H-786 and H-941 are stronger source-side visual pressure, not accepted exact-side witnesses.
