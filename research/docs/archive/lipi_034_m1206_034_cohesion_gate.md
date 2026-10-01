# Lipi 034 M-1206 034 Cohesion Gate

Date: 2026-05-26

This note is a gate — a checkpoint that evidence must pass before the project may take a further step. The question it settles is whether one object, M-1206, shows a sign shape distinct enough to stand on its own, or whether it simply looks like the neighbouring shapes it was supposed to contrast with. The test was run blind: reviewers saw label-stripped crops and did not know which object was the target.

## Question

After M-315 failed the strict blind upgrade, does M-1206 give a source-visible `034` graphic class, or does it collapse toward the broader `415` visual family?

This gate uses anonymous source-image crops. It is a graphic-class experiment, not a translation attempt.

## Inputs

The neutral packet is the label-stripped bundle shown to reviewers, followed by the key that says which crop was which.

Neutral packet:

```text
tmp/m1206_034_cohesion_gate/derived/m1206_034_cohesion_neutral_contact_sheet.png
data/open_prototype/reports/lipi_034_m1206_034_cohesion_gate_inputs.csv
data/open_prototype/reports/lipi_034_m1206_034_cohesion_gate_inputs_summary.json
```

Keyed classes, hidden from visual reviewers:

```text
C001-C003  M-1206 +520-220-034+ target views
C004-C005  M-37 +520-220-415+ same-site comparator views
C006-C008  clean or duplicate exact-side 415 controls: H-938/H-940
C009-C010  415-family candidates with source/local side-mapping conflict: H-786/H-941
C011       M-1584 +034+ pottery/graffiti singleton pressure
C012-C013  M-685 ]034-204+ fragmentary pressure
```

Mechanic check:

```text
13 CSV rows
13 neutral crops
all neutral hashes match
all dimensions match
no missing paths
no obvious source-label leak on the contact sheet
```

## Blind Reviewer Results

Two independent blind visual reviewers classified only the anonymous contact sheet.

### Shared Findings

Comparanda below are comparison pieces drawn from outside the target, used to test whether the target's shape is distinctive. Both reviewers agree:

```text
C001-C003 form a stable visual family under reversal/order change.
C004-C005 are the strongest external matches to C001-C003.
C008-C010 are also close, but more cropped/noisy or side-policy-gated.
C006-C007 are relevant but weaker.
C011-C013 are not usable as meaningful comparanda in this packet.
```

Reviewer 1 summary:

```text
C001-C003 look internally stable if mirror/order reversal is allowed. C004/C005 are closest. C008/C010/C009 are next closest. C006/C007 are weaker. C011-C013 are too degraded, cropped, or different-medium to classify confidently.
```

Reviewer 2 summary:

```text
C001-C003 are stable at the family/formula level, not exact duplicate level. C004/C005 are the strongest matches; C008/C010 also close; C009 plausible; C006/C007 weaker. C011-C013 are insufficient visual evidence.
```

## Unblinded Adjudication

Adjudication is the ruling made after the key is revealed and the blind judgements are matched back to real object names.

The M-1206 target views are internally coherent:

```text
M-1206 A+E
M-1206 A
M-1206 a
```

That is a positive source-image result. The target is not random noise or a one-crop artifact.

But the closest external matches are the `415` comparanda:

```text
M-37 A/a
H-940 A
H-941 A
H-786 A
H-938 A/A bis
```

The strongest same-site match is M-37. The strongest clean exact-side Harappa `415` control is H-940, with H-938 relevant but weaker in the blind view. H-786 and H-941 remain visually important but source/local side-mapping gated.

That means the current evidence does not support a clean terminal-substitution reading:

```text
520-220-034 versus 520-220-415
```

as a semantic contrast. The source images instead show a broad visual family spanning the M-1206 target and `415` controls.

## Decision

Accepted:

```text
M-1206 is a stable source-visible visual-family target.
M-1206 is visually close to M-37 and other 415-family panels.
The next live problem is allograph/sign-splitting/source-side-mapping/transcription-policy, not value assignment.
```

Rejected:

```text
034 has a source-validated value.
034 equals 415.
034 contrasts semantically with 415 in the 520-220-X frame.
M-1584 or M-685 confirm the same 034 graphic class.
M-315 can be used as positive 034 evidence.
```

## Status Change

Before this gate:

```text
M-1206 was the best next source-visible 034 target after M-315 failed.
```

After this gate:

```text
M-1206 is source-visible and internally stable, but its closest blind visual neighbors are 415-family panels. The 034 branch now has stronger allograph/transcription-policy or sign-splitting pressure.
```

This is progress because it removes a false reading path. The next translation-relevant step is not to assign meaning. It is to decide whether `034/415` are one visual class split by catalog policy or two signs inside the same graphic family.

## Next Gate

1. Resolve source/local side mapping for H-786 and H-941 before counting them as exact-side `415` evidence.
2. Acquire or locate source-grade M-1912 for the missing `+520-220-003+` same-site comparator.
3. Run a second blind packet after isolating the terminal components rather than whole three-sign bands.
4. Keep M-1584 and M-685 out of the positive cohesion count until better source images make them classifiable.

## Follow-on Completed

The terminal-component gate is now recorded in:

```text
docs/lipi_034_m1206_terminal_component_gate.md
```

It confirms that the whole-band result was not only prefix contamination: isolated M-1206 terminal components cluster most closely with exact-side H-938 `415` terminal controls and side-gated H-941/H-786 `415`-family candidates.

Current accepted mappings, sign values, and translations:

```text
0
```
