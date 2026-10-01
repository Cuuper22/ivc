# H-2218 Through H-2239 Minimal Contrast Packet

Date: 2026-05-25

This note builds a packet of minimal-contrast candidates: pairs of tablets whose three inscribed sides match exactly except for one sign in one slot. Such pairs matter because a one-sign difference between otherwise identical objects is the closest thing this corpus offers to a controlled experiment on sign function.

## Question

Inside the H-2218 through H-2239 three-side tablet series, do the two single-object variants form real minimal-contrast candidates rather than loose curiosities?

This is an attempt to find controlled sign-function evidence. It is not a translation.

## Inputs

- Side-role template probe: `docs/h2218_h2239_side_role_template_probe.md`
- Fig. 4 mapping: `data/open_prototype/reports/lipi_h2218_h2239_fig4_mapping.csv`
- Side-role rows: `data/open_prototype/reports/lipi_h2218_h2239_side_role_templates.csv`
- Script: `data/open_prototype/tools/lipi_h2218_h2239_minimal_contrast_packet.mjs`
- CSV: `data/open_prototype/reports/lipi_h2218_h2239_minimal_contrast_packet.csv`
- Summary: `data/open_prototype/reports/lipi_h2218_h2239_minimal_contrast_summary.json`
- Team review: `docs/h2218_h2239_minimal_contrast_team_review.md`

## Result

```text
variant targets: 2
contrast rows: 4
same-group/same-template/single-slot controls: 4
exact-dimension single-slot controls: 1
accepted readings: 0
```

## Minimal Contrast Candidates

| Target | Control | Contrast | Why it matters |
| --- | --- | --- | --- |
| `H-2237` | `H-2233` | side 3 `+154-003+` versus `+156-003+` | Same manufacturing group, same side-role template, same dimensions `10 x 6.5`, same invariant sides `+700-034+` and `+861-003+`. This is the cleanest local minimal pair found so far. |
| `H-2237` | `H-2230` | side 3 `+154-003+` versus `+156-003+` | Same group and template, one-slot difference, but vertical size differs by `0.7 mm`. |
| `H-2238` | `H-2230` | side 1 `+700-033+` versus `+700-034+` | Same group and template, one-slot difference, closest Fig. 4 neighbor, invariant sides `+861-003+` and `+156-003+`. |
| `H-2238` | `H-2233` | side 1 `+700-033+` versus `+700-034+` | Same group and template, one-slot difference, second local control. |

## Research Consequence

This is the narrowest local contrast so far:

```text
H-2237 / H-2233:
+700-034+ | +861-003+ | +154-003+
+700-034+ | +861-003+ | +156-003+
```

If source images confirm same physical side role, direction basis, and diagnostic stroke separation, then `154/156` becomes a serious side-role value contrast candidate inside this tablet batch. That still would not give a phonetic value, sign meaning, number, commodity, or translation.

The second contrast is:

```text
H-2238 / H-2230:
+700-033+ | +861-003+ | +156-003+
+700-034+ | +861-003+ | +156-003+
```

If source images validate it, `033/034` becomes a batch-internal subtype contrast within FRAME700 — the project's name for the `700-03x` sign frame — in the same side-role environment. That would strengthen the broader `034` line because it is no longer only a cross-object metadata pattern; it has a same-series, same-template, single-slot case.

The team review keeps the two variants separate: `H-2237` tests `154/156` in the `15x-003` slot, while `H-2238` tests `033/034` in the `700-03x` slot. They are not one paired contrast unless source evidence gives a reason to link the two slots.

## Source Gate

For these rows, the plate request must verify:

1. The target and control are correctly aligned to the same Fig. 4/HARP objects.
2. The differing side is the same physical side role, not just local side numbering.
3. The invariant sides are genuinely invariant in the images.
4. The diagnostic strokes separating `154/156` or `033/034` are visible.
5. Direction and impression/object orientation are recorded.
6. Damage, retouching, or catalog normalization is not creating the difference.

## Claim Status

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted numerical values: 0
accepted side functions: 0
accepted source mappings from this packet: 0
```
