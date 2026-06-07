# Lipi 034 M-1206 M-37 Terminal Recut Gate

Date: 2026-05-26

## Question

Can the contaminated `M-37` terminal-component controls from the M-1206 terminal gate be cleaned enough to promote `M-37 +520-220-415+` into a clean same-site `415` control?

This matters because `M-37` is the same-site, same-object-type, same-material, same-shape comparator for `M-1206 +520-220-034+`. If `M-37` can be made clean, it becomes the best same-site `415` control. It still does not automatically become the closest visual match to M-1206; that is a separate graphic judgment.

## Inputs

Source-level M-37 images:

```text
tmp/m1206_terminal_triad_source_recheck/cisi_india_n54_w2000.jpg
tmp/m1206_terminal_triad_source_recheck/derived/m37_A_signband_v2.png
tmp/m1206_terminal_triad_source_recheck/derived/dotnet_m37_bottom_right_a.png
```

Previous terminal crops:

```text
tmp/m1206_034_terminal_component_gate/derived/T004.png
tmp/m1206_034_terminal_component_gate/derived/T005.png
```

New recut packet:

```text
tmp/m1206_m37_terminal_recut_gate/derived/m37_terminal_recut_contact_sheet.png
data/open_prototype/reports/lipi_034_m1206_m37_terminal_recut_inputs.csv
```

## Recut Results

The old terminal crops used the same box from broad signband crops:

```text
T004/T005 crop box: x=500, y=20, w=250, h=190
```

Those boxes included visible adjacent animal/horn relief, which made them unsafe as clean isolated terminal controls.

New candidate crops were cut directly from the source-level M-37 views. The useful candidates are:

| Candidate | Effect |
| --- | --- |
| `M37_A_terminal_strict_core_from_signband.png` | Best M-37 control. Removes the major right-hand curved contaminant while preserving the diagnostic top rake/comb and central descending stem. |
| `M37_A_terminal_minimal_core_from_signband.png` | Cleanest isolation check, but slightly too tight to be the primary comparison crop because it suppresses context. |
| `M37_a_terminal_strict_core_from_full.png` | Useful mirror-side corroboration, but not as clean as the source-signband strict crop. |
| `M37_a_terminal_minimal_core_from_full.png` | Low-contamination mirror-side check, but context-poor. |

## Visual Adjudication

The strict signband recut promotes M-37 out of the old contaminated-control bucket.

What is now clearer:

```text
M-37 terminal form is a comb/rake with a horizontal top bar and a central stem.
The old T004/T005 contamination exaggerated the uncertainty, but the comb/rake profile is not purely an artifact of the horn intrusion.
The primary recut `M37_A_terminal_strict_core_from_signband.png` is clean enough to function as the same-site isolated `415` terminal control.
```

What remains blocking:

```text
M-37 still reads as a heavier comb/rake-with-stem subform.
It is not the closest visual neighbor to the M-1206 034 terminal bundle.
The closest vertical-bundle comparanda for M-1206 remain H-938 T006/T007; H-940 T008 stays weaker.
```

## Decision

M-37 improves from:

```text
same-site 415 pressure but crop-contaminated
```

to:

```text
clean isolated same-site 415 terminal control, but as a comb/rake subform rather than the closest M-1206 match
```

This matters. It means the same local `415` label currently covers at least two source-visible terminal profiles in this branch:

```text
H-938/H-940: vertical-bundle profile
M-37: comb/rake-with-stem profile
```

That increases sign-inventory pressure. It can support either:

```text
local 415 is a broad graphemic/transcription bin
or
M-37 and H-938/H-940 are different fine forms/subtypes inside a larger 415 family
```

It does not prove:

```text
034 = 415
M-37 terminal equals the M-1206 terminal
any sign value
any translation
```

## Effect On The M-1206 Allograph Decision Gate

Keep:

```text
H-938 A/A bis = strongest clean exact-source-side 415 control
H-940 A = secondary clean exact-source-side 415 control
```

Update:

```text
M-37 A strict signband recut = clean isolated same-site 415 terminal control
M-37 still belongs to a comb/rake subform, not the closest M-1206 vertical-bundle match
```

Next useful work:

```text
Acquire higher-resolution M-37 source imagery or a source transcription note.
Use M-37 as the clean same-site 415 subtype/fine-form control in the next blind component packet.
Do not let M-37 carry the whole allograph claim by itself.
```

Accepted mappings, sign values, and translations remain:

```text
0
```
