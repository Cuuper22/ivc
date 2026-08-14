# Lipi 034 M-1206 Terminal Component Gate

Date: 2026-05-26

## Question

This note records a blind-review gate — a decision checkpoint the evidence must pass before any claim moves forward. The numbers in strings like `520-220-034` are local numeric sign labels — transcription codes, not readings.

The previous M-1206 cohesion gate used whole three-sign bands: crops of the full inscription strip. That was useful, but whole bands could match mostly because they share the `520-220` prefix, the first two signs.

This gate isolates the apparent terminal components — crops of the final sign alone. The question is narrower:

```text
Does the M-1206 terminal component visually stay separate from the 415 terminal controls, or does it cluster with them?
```

This is still graphic-class research only. It is not a value, reading, function, language, or translation test.

## Inputs

The neutral packet is the anonymized bundle given to blind reviewers: label-free crops plus a private key that stays hidden until adjudication.

Neutral packet:

```text
tmp/m1206_034_terminal_component_gate/derived/m1206_034_terminal_component_neutral_contact_sheet.png
data/open_prototype/reports/lipi_034_m1206_terminal_component_gate_inputs.csv
data/open_prototype/reports/lipi_034_m1206_terminal_component_gate_inputs_summary.json
```

Private key:

```text
T001-T003  M-1206 apparent terminal components from +520-220-034+
T004-T005  M-37 apparent terminal/rake components from +520-220-415+
T006-T008  H-938/H-940 exact-side 415 terminal controls
T009-T010  H-786/H-941 side-gated 415-family terminal candidates
T011-T016  prefix/nonterminal distractors
```

Mechanic check:

```text
16 CSV rows
16 neutral crops
all paths exist
all hashes match
all dimensions match
no duplicate IDs
no source-label leak on contact sheet
crop boxes are within base crop dimensions
```

Mechanical caveat:

```text
T004/T005 include adjacent curved material, so M-37 remains a useful same-site pressure case but not the cleanest isolated terminal control.
```

## Blind Reviewer Results

Two blind reviewers classified only the anonymous terminal-component sheet. Neither knew which object any crop came from.

### Reviewer A

```text
T001-T003 form a stable cluster, with T002-T003 as the core pair and T001 as a looser member.
Closest T004-T010: T006, T007, T010.
Secondary/partial: T004, T005, T009.
Weakest: T008.
T011-T016 are distractors/nonterminal forms.
Terminal isolation strengthens the upright-rib match and exposes that some previous broad matches were driven by adjacent curved material.
```

### Reviewer B

```text
T001-T003 cohere visually; T002-T003 are tightest, T001 is plausible but less secure.
Nearest neighbors: T006-T007 first, then T010/T009.
T004-T005 are a separate comb-like subcluster because of the heavy top band and curved stroke.
T008 is weaker.
T011-T016 are mostly distractors; T015 is a superficial near miss but outside the cluster.
```

## Unblinded Adjudication

Adjudication is the judgment made after the private key is opened and the crop identities come back into view.

The target terminal result:

```text
T002-T003 = M-1206 apparent terminal component, tight blind pair
T001      = M-1206 apparent terminal component, weaker but plausible member
```

The closest external terminal controls:

```text
T006-T007 = H-938 A/A bis exact-side 415 controls
T010      = H-941 A side-gated 415-family candidate
T009      = H-786 A side-gated 415-family candidate, weaker
```

The M-37 same-site controls:

```text
T004-T005 = related comb-like subcluster, but contaminated by adjacent curved material
```

The distractors:

```text
T011-T016 = rejected as nonterminal/prefix classes by both reviewers
```

## Decision

Accepted:

```text
M-1206 has a stable apparent terminal component at the visual level.
The closest clean external terminal controls are H-938 A/A bis exact-side 415 components.
The terminal-level comparison strengthens 034/415 graphic-family pressure.
The shared whole-band prefix alone does not explain the previous broad match.
```

Not accepted:

```text
034 equals 415.
034 has a value.
415 has a value.
034 and 415 are proven allographs.
M-37 gives a clean isolated terminal match.
H-786 or H-941 count as exact-side 415 evidence before side mapping is resolved.
Any translation.
```

## Status Change

Before this gate:

```text
Whole-band M-1206 looked closest to 415-family panels, but prefix similarity could be responsible.
```

After this gate:

```text
The isolated M-1206 terminal component still clusters closest to exact-side H-938 415 controls and side-gated H-941/H-786 415-family candidates.
```

This is a stronger result than the whole-band gate. It moves this branch of the investigation away from a clean `034` terminal contrast and toward a real sign-inventory problem — a question about how many distinct signs there are:

```text
034/415 may be allographs, source-side mapping variants, transcription-policy splits, or neighboring signs within one graphic family.
```

The project still cannot choose among those explanations without side-policy and source-image closure.

## Next Gate

1. Resolve H-938/H-940/H-786/H-941 side-label policy against CISI/HARP/Mahadevan source tables.
2. Acquire source-grade M-1912 to add the missing `+520-220-003+` same-site terminal control.
3. Recut T004/T005 from higher-resolution or less contaminated M-37 source images if possible.
4. Add independent `520-220-034` or exact `034` source-visible targets only after their components are classifiable.

Current accepted mappings, sign values, and translations:

```text
0
```

