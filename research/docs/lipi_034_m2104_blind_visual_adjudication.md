# Lipi 034 M-2104 Blind Visual Adjudication

Date: 2026-05-25

Question:

```text
Do the two strongest public tablet-parallel crops independently show a U/pot-like unit adjacent to a four-stroke vertical group?
```

Inputs:

- `tmp/cisi_m2104_packet/crops/m478_a_inscription_crop.png`
- `tmp/cisi_m2104_packet/crops/m1425_a_inscription_crop.png`
- `tmp/cisi_m2104_packet/closeups/m478_a_u_count_closeup.png`
- `tmp/cisi_m2104_packet/closeups/m1425_a_u_count_closeup.png`

Outputs:

- `data/open_prototype/reports/lipi_034_m2104_blind_visual_adjudication.csv`
- `data/open_prototype/reports/lipi_034_m2104_blind_visual_adjudication_summary.json`

## Result

```text
adjudication rows: 8
objects adjudicated: M-478, M-1425
accepted mappings: 0
accepted decipherment claims: 0
```

Consensus:

`M-478 A` survives as the stronger public tablet-parallel witness. Three independent adjudicators saw a U/pot-like unit adjacent to a count-like group of four vertical strokes. The main caution is scan blur and possible stroke merging, but the four-stroke group is visible enough to carry the next gate.

`M-1425 A` also survives, but only provisionally. It appears to show the same broad arrangement, but the crop is blurrier and the stroke boundaries are less crisp. It is useful because it is an independent Pakistan-volume parallel, but it cannot carry the claim alone.

## What This Proves

Only this:

```text
The named tablet parallels M-478 and M-1425 contain a visually recurring adjacent-cluster pattern compatible with the proposed four-stroke side of the M-2104 test.
```

It does not prove:

```text
700-004 is a sign-list mapping.
004 means four.
034 means three.
The U/pot-like unit has an accepted value.
The M-2104 row is source-confirmed.
The object is translated.
```

## Adjudicator Summary

| Object | Verdict | Confidence | Main Caution |
| --- | --- | --- | --- |
| `M-478 A` | Survives for next gate | Medium-high | Blur could merge or split a stroke, but four strokes are independently visible. |
| `M-1425 A` | Survives provisionally | Medium-low | Stroke boundaries are less crisp; neighboring-sign contamination remains possible. |

## Next Gate

The live hypothesis advances one step, but only to a stricter test:

1. Acquire or produce higher-resolution closeups for `M-1425` and `M-480`.
2. Locate a raw source image for `M-2104`, because Parpola Fig. 1 is standardized.
3. Only then compare the target cluster against the public four-stroke parallel pattern.

Kill condition:

```text
If raw M-2104 does not show a discrete U/pot-like unit plus three vertical strokes in the corresponding position, the 700-034 side of this extraction fails even though M-478/M-1425 preserve the four-stroke parallel.
```
