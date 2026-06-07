# Lipi 034 M-2104 Source Route Probe

Date: 2026-05-25

Question:

```text
Can the M-2104 Parpola crosswalk hypothesis be tested against public source images, not just prose?
```

Inputs:

- `data/open_prototype/tools/lipi_034_m2104_source_route_probe.mjs`
- Internet Archive CISI bundle:
  - `Corpus of Indus Seals and Inscriptions. Collections in India_djvu.xml`
  - `Corpus of Indus Seals and Inscriptions. Collections in Pakistan_djvu.xml`
- Parpola 2019, Fig. 1 text no. 12 and surrounding prose
- Manual visual inspection of downloaded IA page images in `tmp/cisi_m2104_packet/`

Outputs:

- `data/open_prototype/reports/lipi_034_m2104_source_route_hits.csv`
- `data/open_prototype/reports/lipi_034_m2104_source_visual_notes.csv`
- `data/open_prototype/reports/lipi_034_m2104_source_route_summary.json`

## Result

```text
route-hit rows stored: 66
manual visual-note rows stored: 10
exact OCR object hits: H-543, H-544, M-478, M-480, M-915
plate-image confirmed: H-543, H-544, M-478, M-480, M-715, M-896, M-915, M-1425
still not plate-confirmed: M-2104
accepted source mappings: 0
accepted decipherment claims: 0
```

The important change is that the tablet parallels are now visually reachable:

| Object | Source route | Status | Use |
| --- | --- | --- | --- |
| `M-478` | CISI India IA leaf `150`, printed p. 115, `Mohenjo-Daro 478-481` | Plate visible | Test `700-004` as Parpola's `UIIII` / four-pot cluster and test `400/097`. |
| `M-480` | CISI India IA leaf `150`, same plate | Plate visible | Same test as `M-478`; lower page, crop needed for sign-level work. |
| `M-1425` | CISI Pakistan IA leaf `227`, printed p. 193, `Mohenjo-Daro 1425-1428` | Plate visible | Independent tablet-parallel check for `700-004`, `400`, and `097`. |
| `H-543` | CISI Pakistan IA leaf `324`, printed p. 290 | Plate visible, broken | Control for the `097/151` signs 15/1 sequence. |
| `H-544` | CISI Pakistan IA leaf `325`, printed p. 291 | Plate visible | Cleaner control for the `097/151` signs 15/1 sequence. |
| `M-915` | CISI Pakistan IA leaf `122`, printed p. 88 | Plate visible | Named control for signs 15 and 1 at text end. |
| `M-715` | CISI Pakistan IA leaf `80`, printed p. 46 | Plate visible | Conflict-resolution image: Parpola names it, local row does not expose clean `151/097`. |
| `M-896` | CISI Pakistan IA leaf `119`, printed p. 85 | Plate visible | Conflict-resolution image: local row has `151` but not `097`. |
| `M-2104` | Parpola 2019 Fig. 1 text no. 12 | Figure/prose visible, no IA plate route found | Target remains source-gated beyond Parpola. |

## What Changed

Before this probe, the M-2104 extraction rested on Parpola's prose plus local rows:

```text
M-2104: +151-097-700-034+
M-478:  +400-097-700-004+
M-480:  +400-097-700-004+
M-1425: +400-097-700-004+
```

Now the three tablet parallels have public plate routes. That means the next test is no longer abstract:

```text
Does the visual cluster in M-478/M-480/M-1425 really show the four-stroke U/pot pattern that local lipi encodes as 700-004?

Does Parpola Fig. 1 text no. 12 really show the corresponding three-stroke U/pot pattern that local lipi encodes as 700-034?
```

If either answer is no, the live `034` extraction fails.

## Prior-Work Pressure

The CISI India introduction page reached by the M-478 route gives useful pressure for the pot-count hypothesis. It describes a U-shaped tablet sign treated as a pot, preceded by zero to four vertical strokes, and discusses M-478/M-479 as a four-pot offering context. This supports the class of visual pattern under test, but it does not validate M-2104 or any local sign mapping by itself.

## Negative Result

IA CISI OCR did not find exact `M-2104`. The bare `2104` hit appears on Pakistan leaf `479`, a register/index-like page, not a source plate for the object. So `M-2104` still depends on Parpola 2019 Fig. 1 until a direct CISI plate, rod photograph, museum image, or higher-resolution publication source is acquired.

## Boundary

Accepted translations: 0

Accepted phonetic values: 0

Accepted sign meanings: 0

Accepted source mappings: 0

Accepted sign-list mappings: 0

This artifact stores route and visual access. It does not accept `097 = sign 15`, `151 = sign 1`, `400 = sign 107`, `034 = three`, or `004 = four`. Those remain live hypotheses only.

## Next Move

1. Crop `M-478`, `M-480`, `M-1425`, and Parpola Fig. 1 text no. 12 to the inscription lanes.
2. Compare the visible stroke/U-pot cluster against local `700-004` and `700-034`.
3. Use `H-543`, `H-544`, and `M-915` as controls for the `097/151` signs 15/1 mapping.
4. Use `M-715` and `M-896` as adversarial conflict rows, not exceptions to hand-wave.

## Sources

- Parpola 2019 PDF: <https://tuhat.helsinki.fi/ws/portalfiles/portal/129602857/Parpola_A_2019_Inscriptions_incised_on_the_Harappan_bone_rods_Proceedings_of_EASAA_22.pdf>
- IA CISI bundle: <https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan>
- CISI India IA XML: <https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India_djvu.xml>
- CISI Pakistan IA XML: <https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan_djvu.xml>
