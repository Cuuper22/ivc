# Lipi 034 M-2104 Visual Stroke Probe

Date: 2026-05-25

Question:

```text
Do the first public crops make the M-2104 700-034 versus parallel 700-004 stroke-count hypothesis visually testable?
```

Inputs:

- Parpola 2019 Fig. 1 text no. 12 crop: `tmp/cisi_m2104_packet/crops/m2104_parpola_fig1_text12_crop.png`
- CISI India IA leaf 150 crop for `M-478 A`: `tmp/cisi_m2104_packet/crops/m478_a_inscription_crop.png`
- CISI India IA leaf 150 crop for `M-480 A`: `tmp/cisi_m2104_packet/crops/m480_a_inscription_crop.png`
- CISI Pakistan IA leaf 227 crop for `M-1425 A`: `tmp/cisi_m2104_packet/crops/m1425_a_inscription_crop.png`
- CISI India IA leaf 150 crop for `M-478 B`: `tmp/cisi_m2104_packet/crops/m478_b_scene_crop.png`

Outputs:

- `data/open_prototype/reports/lipi_034_m2104_visual_stroke_notes.csv`
- `data/open_prototype/reports/lipi_034_m2104_visual_stroke_summary.json`
- `data/open_prototype/reports/lipi_034_m2104_segmentation_targets.csv`
- `data/open_prototype/reports/lipi_034_m2104_blind_visual_adjudication.csv`
- `data/open_prototype/reports/lipi_034_m2104_blind_visual_adjudication_summary.json`
- `tmp/cisi_m2104_packet/overlays/m2104_parpola_fig1_text12_segmentation_overlay.png`
- `tmp/cisi_m2104_packet/overlays/m478_a_segmentation_overlay.png`
- `tmp/cisi_m2104_packet/overlays/m480_a_segmentation_overlay.png`
- `tmp/cisi_m2104_packet/overlays/m1425_a_segmentation_overlay.png`

## Result

```text
manual crop-note rows stored: 5
segmentation target rows stored: 15
blind adjudication rows stored: 8
objects with crops: M-2104, M-478, M-480, M-1425
accepted mappings: 0
accepted decipherment claims: 0
```

First-pass result:

The hypothesis is now visually testable, not accepted. Parpola Fig. 1 row 12 shows the standardized `M-2104` target with the `UIII` cluster. Public CISI crops for `M-478`, `M-480`, and `M-1425` show tablet inscription lanes with visible four-stroke/U-pot-like cluster regions. `M-478` and `M-1425` are the strongest immediate crops; `M-480` is usable but lower contrast.

## Live Hypothesis

```text
M-2104: +151-097-700-034+     Parpola: UIII + signs 15 and 1
M-478:  +400-097-700-004+     Parpola: UIIII + signs 15 and 107
M-480:  +400-097-700-004+     Parpola: UIIII + signs 15 and 107
M-1425: +400-097-700-004+     Parpola: UIIII + signs 15 and 107
```

If the local encoding is right, then:

```text
700-034 = UIII / three-pot cluster
700-004 = UIIII / four-pot cluster
097     = Parpola sign 15 candidate
151     = Parpola sign 1 candidate
400     = Parpola sign 107 candidate
```

## Visual Notes

| Object | Crop | First-pass observation | Status |
| --- | --- | --- | --- |
| `M-2104` | Parpola Fig. 1 row 12 | Standardized drawing shows the `UIII` target described in prose. | Keeps target alive, but still needs raw source image. |
| `M-478 A` | CISI India leaf 150 | Visible long tablet inscription with a four-parallel-stroke group adjacent to the U/pot-like tablet cluster. | Strong first parallel crop. |
| `M-480 A` | CISI India leaf 150 | Same tablet-family inscription zone visible, but crop is lower contrast and partly constrained by page placement. | Usable route, weaker crop. |
| `M-1425 A` | CISI Pakistan leaf 227 | Visible parallel tablet inscription with a clear four-parallel-stroke group and adjacent U/pot-like/tail signs. | Strong independent parallel crop. |
| `M-478 B` | CISI India leaf 150 | Iconographic scene visible on the same tablet object family. | Context support only; not sign mapping evidence. |

## Segmentation Targets

The first overlay pass marks only visual units to test. It does not accept the after-the-fact local-token assignments.

| Object | Overlay | Target boxes | Immediate use |
| --- | --- | --- | --- |
| `M-2104` | `tmp/cisi_m2104_packet/overlays/m2104_parpola_fig1_text12_segmentation_overlay.png` | `S1` candidate sign 1, `S2` candidate sign 15, `S3` U/pot, `S4` three strokes | Raw-image confirmation target; Parpola-standardized only. |
| `M-478 A` | `tmp/cisi_m2104_packet/overlays/m478_a_segmentation_overlay.png` | `S2` U/pot, `S3` four strokes, `S1/S4` adjacent sign regions | Strongest first tablet-parallel segmentation target. |
| `M-1425 A` | `tmp/cisi_m2104_packet/overlays/m1425_a_segmentation_overlay.png` | `S2` U/pot boundary, `S3` four strokes, `S1/S4` adjacent sign regions | Independent tablet-parallel segmentation target. |
| `M-480 A` | `tmp/cisi_m2104_packet/overlays/m480_a_segmentation_overlay.png` | weak `S1/S2/S3` cluster | Needs tighter crop before adjudication. |

Stored target sheet:

```text
data/open_prototype/reports/lipi_034_m2104_segmentation_targets.csv
```

## Blind Adjudication

Independent visual adjudication of the two strongest public tablet parallels gives this status:

```text
M-478 A: survives for next gate, medium-high confidence
M-1425 A: survives provisionally, medium-low confidence
accepted mappings: 0
accepted decipherment claims: 0
```

The adjudicators agree that `M-478 A` visibly carries a U/pot-like unit adjacent to a four-stroke vertical group. `M-1425 A` shows the same broad arrangement, but blur and neighboring-sign contamination keep it provisional.

Detailed artifact:

```text
docs/lipi_034_m2104_blind_visual_adjudication.md
```

## Kill Conditions

The current extraction fails if any of these happen under sign-level segmentation:

- `700-004` does not correspond to the visible four-stroke U/pot cluster in the tablet parallels.
- `700-034` does not correspond to Parpola's `UIII` cluster in `M-2104`.
- `097` is not the same visual sign slot as Parpola sign 15 across target and parallels.
- `151` and `400` do not match Parpola signs 1 and 107 in the expected object roles.
- The apparent match is caused by direction normalization, drawing regularization, or derivative sign-list circularity.

## Boundary

Accepted translations: 0

Accepted phonetic values: 0

Accepted sign meanings: 0

Accepted source mappings: 0

Accepted sign-list mappings: 0

This probe only says: the visual falsification path exists and the first crops do not immediately kill the hypothesis.

## Next Move

Run blind adjudication on the stored segmentation boxes for `M-478` and `M-1425` first. Only after those two parallel crops independently support the same four-stroke/U-pot segmentation should `M-480` and Parpola text no. 12 be used to compare against `+400-097-700-004+` and `+151-097-700-034+`.
