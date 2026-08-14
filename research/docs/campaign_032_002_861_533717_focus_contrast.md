# 032-002-861 533-717 Focus Contrast

Date: 2026-05-29

This note tries to find what makes two seals special and fails to find it. M-376 and M-391 both end `002-861-533-717`. Five other seals of the same kind, from the same site, do not. If some ordinary property — shape, inscription length, image quality — sorted the two groups, `533-717` would need no linguistic explanation. This pass checks the obvious properties one by one. None of them separate the groups, which leaves the question open rather than answered.

## Question

After the tail-rarity scan, the live question became:

```text
What separates M-376/M-391 from the same-register controls?
```

A "control" is a comparison row that shares the setting but not the feature under test; "same-register" means drawn from the same coarse class of object — same site, type, and shape. This campaign tests the seven Mohenjo-daro no-icon `SEAL:R + 002-861` rows as one contrast set.

## Stored Outputs

```text
tmp/run_032_002_861_533717_focus_contrast.py
data/open_prototype/reports/campaign_032_002_861_533717_focus_contrast_rows.csv
data/open_prototype/reports/campaign_032_002_861_533717_focus_contrast_features.csv
data/open_prototype/reports/campaign_032_002_861_533717_focus_contrast_summary.json
```

## Contrast Set

| class | rows |
|---|---|
| bare `002-861` | `M-1954`, `M-1267`, `M-1973` |
| `002-861-533-717` | `M-376`, `M-391` |
| `002-861-603` | `M-1273` |
| `002-861-360-520-919-140` | `M-355` |

## Result

Simple metadata does not cleanly separate `533-717`.

Hostile overlaps — cases where a control matches the target on the property being tested, so that property cannot be doing the work:

```text
shape:
  M-376/M-391 are cuboid-convex
  but M-355 is also cuboid-convex and takes a different long tail

text length:
  M-376 length 7 overlaps bare M-1267 and M-1973
  M-391 length 12 overlaps bare M-1954

source status:
  M-376/M-391 are source-visible
  but M-355/M-1267/M-1273 are also source-visible controls
```

The only target-specific metadata features are the immediate pre-`002-861` contexts:

```text
M-376: 100-176 before 002-861
M-391: 233-805 before 002-861
```

Those are singletons. They are clues for later left-frame work, not proof of a shared `533-717` class.

## Decision

Demote again:

```text
metadata_features_do_not_separate_533_717_cleanly
```

Current status:

```text
533-717 is still a live narrow subclass/apposition candidate,
but it is not yet explained by shape, row length, broad register, or source visibility.
```

The next decisive evidence has to be source-layout or source-family independence — proof that the two rows are genuinely separate objects rather than one workshop habit copied twice. A "family cell" is such a group of near-identical rows treated as a single piece of evidence:

```text
Are M-376/M-391 two independent rows with the same clean post-861 physical tail,
or one tiny copy/source-family cell?
```

No sign value, phonetic reading, language identity, or translation is accepted.
