# 032-002-861 603 Source Route

Date: 2026-05-29

## Question

The `603` mobility campaign found a bridge profile. This source-route pass asks which `603` rows are actually ready for source-layout comparison.

```text
post-861 side:
  M-240 / M-714 / M-1273

independent side:
  H-1137 / H-1138 / H-1846 / unknown +000-603-091-190+
```

## Post-`861` Source State

| row | route status | source |
|---|---|---|
| `M-240 +520-240-220-032-002-861-603+` | source-visible with prior source-panel crops and token/order overlay | CISI India IA leaf `n95`, printed p. 60, `MOHENJO-DARO 240-242 SEALS bison` |
| `M-714 +740-585-017-033-705-233-798-803-002-861-603+` | source-visible with prior source-panel crops and token-attachment overlay | CISI Pakistan IA leaf `n79`, printed p. 45, `MOHENJO-DARO 712-714 SEALS unicorn III` |
| `M-1273 +740-055-002-861-603+` | source-visible with prior source-panel crops and token-attachment overlay | CISI Pakistan IA leaf `n195`, printed p. 161, `MOHENJO-DARO 1269-1274 SEALS no iconography II` |

Stored local source artifacts:

```text
tmp/032_002_branch_tail_source_acquisition/M240_face_A_signband_from_cisi_india_n095.png
tmp/032_002_branch_tail_source_acquisition/M240_impression_a_signband_from_cisi_india_n095.png
tmp/032_002_branch_tail_token_order/M240_A_a_token_order_overlay.png
tmp/032_002_861_source_token_attachment/M240_603_source_token_attachment_overlay.png
tmp/032_002_861_suffix_split/M714_face_A_cisi_pakistan_n079.png
tmp/032_002_861_suffix_split/M714_impression_a_cisi_pakistan_n079.png
tmp/032_002_861_source_token_attachment/M714_603_source_token_attachment_overlay.png
tmp/032_002_861_suffix_split/M1273_face_A_cisi_pakistan_n195.png
tmp/032_002_861_suffix_split/M1273_impression_a_cisi_pakistan_n195.png
tmp/032_002_861_source_token_attachment/M1273_603_source_token_attachment_overlay.png
```

This side is ready for layout comparison at the current public-image tier.

## Independent `603` Source State

| row | local metadata hook | current route status |
|---|---|---|
| `H-1846 +740-603-240-060-692+` | `H95-2672Figure 30.13` | source-route candidate through Kenoyer and Meadow 1997 Figure 11 / Table 2, not yet a normalized sign-panel crop |
| `H-1137 +740-603-240-060-692+` | `7537824` | candidate route through Kenoyer and Meadow 1997 note that `#7537 (= Mahadevan 1977 5261)` is similar to H95-2672; not source-visible yet |
| `H-1138 +740-603-240-060-692+` | `-346` | candidate route to Vats p. 345 / Plate XCIV no. 346, but no local public crop yet |
| unknown `+000-603-091-190+` | no Cisi-style object ID | metadata-only; cannot enter source-layout comparison yet |

Kenoyer and Meadow 1997 provides the current public publication route:

```text
Figure 11.11: H95-2672, faience, tablet, 2 sides, Trench 11 surface debris.
Table 2: H95-2672 linked to Vats p. 345 / Plate XCIV no. 346, with a note that #7537 (= Mahadevan 1977 5261) is similar.
```

Local source file:

```text
tmp/h2147_source_route/kenoyer_meadow_1997_harappa.pdf
tmp/h2147_source_route/kenoyer_meadow_1997_harappa.txt
tmp/h2147_source_route/p-22.png
tmp/032_002_861_603_slot_source_normalization/H1846_H95_2672_Figure11_11_crop_v3.png
```

Public URL:

```text
https://www.harappa.com/sites/default/files/pdf/Kenoyer1997_Excavations%20at%20Harappa%201994-1995%20New%20Perspective.pdf
```

## Decision

```text
post_861_603_source_side_ready
independent_603_source_side_partly_visible_but_not_layout_ready
```

The bridge is asymmetric:

```text
Mohenjo post-861 603 side: image-backed enough for current layout comparison.
Harappa independent 603 side: H-1846/H95-2672 is now object/figure visible, but the full lane is not yet normalized into sign-panel evidence.
```

## Next Source Step

Do not claim a `603` value from the mobility result. First:

```text
1. use the H95-2672/H-1846 Figure 11.11 crop only as source-visible object evidence until side/sign mapping is checked
2. locate Vats Plate XCIV no. 346 for H-1138 and the similar #7537 route for H-1137
3. decide whether H-1137/H-1138/H-1846 are one copied tablet-family evidence unit or multiple source units
4. only then compare the graphic and layout status of 603 across post-861 and independent contexts
```

No sign value, phonetic reading, language identity, or translation is accepted.
