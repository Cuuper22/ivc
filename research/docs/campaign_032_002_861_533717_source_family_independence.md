# 032-002-861 533-717 Source-Family Independence

Date: 2026-05-29

## Question

The focus contrast left one live question:

```text
Are M-376/M-391 two independent witnesses for 002-861-533-717,
or one tiny source/copy-family cell?
```

This campaign tests exact copy-family collapse using current metadata, source routes, and the existing source-layout packet.

## Stored Outputs

```text
tmp/run_032_002_861_533717_source_family_independence.py
data/open_prototype/reports/campaign_032_002_861_533717_source_family_independence_rows.csv
data/open_prototype/reports/campaign_032_002_861_533717_source_family_independence_summary.json
tmp/032_002_861_533717_source_family_independence/533717_source_family_independence_contact_sheet.png
```

## Target Pair

| field | `M-376` | `M-391` |
|---|---|---|
| source leaf | India `n129`, printed p.94 | India `n131`, printed p.96 |
| source page group | Mohenjo-daro 376-381, no iconography III | Mohenjo-daro 391-396, no iconography III |
| text | `+740-100-176-002-861-533-717+` | `+405-845-686-740-793-003-233-805-002-861-533-717+` |
| length | 7 | 12 |
| local class | `IT` | `LP` |
| area / excavation | `HRA`, `HR 1574426` | `DK-`, `DK-i 60` |
| depth | `-2.5 ft` | unknown |
| boss | `P` | `PN` |
| dimensions | `39.4 x 11.4 mm` | `42 x 10 mm` |
| immediate pre-`002-861` | `100-176` | `233-805` |

## Source Layout

Existing source-token attachment verdicts:

```text
M-376: same-line candidate present, medium confidence
M-391: same-line candidate present, long row, medium-low confidence
```

Both rows preserve a same-line terminal-side `533-717` candidate in the public crops. The packet still does not accept exact source-normalized token boundaries.

## Decision

Exact duplicate/copy collapse is rejected in the current evidence layer.

The target pair shares:

```text
Mohenjo-daro
SEAL:R
no icon
cuboid-convex / plano-convex
terminal 002-861-533-717
```

But it differs on enough source-family features to preserve two artifact attestations:

```text
source leaf/page
full text
length
local class
excavation identifier
depth/boss metadata
dimensions
immediate pre-002-861 context
```

So the status becomes:

```text
two_artifact_witnesses_exact_copy_rejected_one_narrow_register_family_cell_for_linguistic_weighting
```

For linguistic weighting, however, this is still one narrow source/register-family cell:

```text
one narrow source/register-family cell for linguistic weighting
```

The semantic/function claim remains unproven:

```text
subclass_semantics_unproven
```

Why not promote farther:

```text
M-355 is same broad register and cuboid-convex but has a long alternate tail.
M-1267 is same broad register and source-visible but bare after 861.
M-1273 is same broad register and source-visible but takes 603.
M-1954/M-1973 remain source-pending bare controls.
```

## Current Reading

Accepted:

```text
M-376/M-391 are two real artifact attestations of same-line terminal 002-861-533-717 pressure.
They should count as one narrow source/register-family cell until another source-visible 533-717 row appears outside this neighborhood.
```

Not accepted:

```text
533-717 as a semantic value
533-717 as the no-icon SEAL:R register marker
533-717 as a proven subclass marker
phonetic reading
language identity
translation
```

## Next Test

The next admissible promotion needs a source-layout feature shared by `M-376/M-391` and absent in controls:

```text
post-861 spacing pattern
distance from 861 to physical edge
terminal cluster separation
same-side A/a agreement
source-normalized direction
```

If no such feature appears, `533-717` stays a real but unexplained repeated terminal tail.
