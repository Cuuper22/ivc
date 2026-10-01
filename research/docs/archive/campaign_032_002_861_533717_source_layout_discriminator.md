# 032-002-861 533-717 Source Layout Discriminator

Date: 2026-05-29

This note looks for a physical fingerprint and does not find one. If M-376 and M-391 laid out their `533-717` ending in some measurable way that other seals of the same class never do, that would be evidence the ending is a real unit. This pass measures where the tail sits on the line and how wide it is, then checks the controls. A control does the same thing, so the fingerprint is not unique. The note ends by telling the campaign to stop working this small group and look elsewhere.

## Question

After exact copy-family collapse was rejected — the earlier finding that the two rows are not near-copies of one another — the next promotion gate was:

```text
Do M-376/M-391 share a visible post-861 layout behavior that same-register controls lack?
```

## Stored Outputs

```text
tmp/run_032_002_861_533717_source_layout_discriminator.py
data/open_prototype/reports/campaign_032_002_861_533717_source_layout_discriminator_rows.csv
data/open_prototype/reports/campaign_032_002_861_533717_source_layout_discriminator_summary.json
```

## Quantified Existing Overlay Rows

Measurements are in pixels on the marked-up source crops. "Tail start share" is how far along the line the tail begins, as a fraction of line width; "tail width share" is the fraction of the line the tail occupies.

| row | tail | line width | tail width | tail start share | tail width share |
|---|---|---:|---:|---:|---:|
| `M-376` | `533-717` | 730 | 265 | 0.637 | 0.363 |
| `M-391` | `533-717` | 800 | 265 | 0.669 | 0.331 |
| `M-1273` | `603` | 1190 | 220 | 0.815 | 0.185 |

Qualitative controls — same-class comparison rows judged by eye rather than measured. "Same-register" means the same coarse class of object by site, type, and shape:

```text
M-355: source-visible cuboid-convex same-register row with long post-861 tail.
M-1267: source-visible same-register row with bare terminal 002-861 edge.
```

## Decision

No unique source-layout discriminator yet.

What survives:

```text
M-376/M-391 both show same-line terminal-side 533-717 windows.
```

What blocks promotion:

```text
M-1273 also has same-line terminal-side post-861 material.
M-355 has same-register cuboid-convex long-tail behavior.
M-1267 has same-register bare-edge behavior.
```

So same-line terminal placement is not enough to assign function. `533-717` remains a real repeated terminal tail with two independent witnesses, but it is not yet a deciphered subclass marker.

## Updated Status

Accepted:

```text
two real artifact attestations for same-line terminal 002-861-533-717 pressure
one narrow source/register-family cell for linguistic weighting
```

Rejected for now:

```text
unique source-layout marker
metadata-defined subclass
register-wide marker
semantic value
phonetic value
translation
```

## Next Test

Do not keep squeezing this tiny cell. Move laterally:

```text
compare 533-717 against the broader post-861 tail inventory
and against left-frame families before 002-861
```

The immediate candidate is a branch-family comparison:

```text
100-176 -> 002-861-533-717
233-805 -> 002-861-533-717
740-055 -> 002-861-603
231-235 -> 002-861-360-520-919-140
720-175 / 233-550 / 415-798 -> bare 002-861
```

No sign value, phonetic reading, language identity, or translation is accepted.
