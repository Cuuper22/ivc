# Lipi 034 M-2104 Raw Source Alias Route

Date: 2026-05-25

## Question

Can `M-2104` be moved beyond Parpola 2019 standardized Fig. 1 to a public raw/source-grade image route?

## Result

Yes, with a limitation.

`M-2104` now has a public raw published plate route through the local source hook:

```text
M-2104
local hook: VS 875CXIV:532 | -12.0 ft
Marshall alias: No. 532 / Pl. CXIV / VS 875
public image: Harappa cylinder-seals.jpg, no. 532 lower left
```

This breaks the previous Parpola-only bottleneck. The target side of the `034` test is no longer limited to a standardized drawing.

It does **not** accept the mapping. The Harappa image is a limited-resolution public plate reproduction, good enough to create a real visual target, not good enough to settle the stroke boundary alone.

## Stored Outputs

- `data/open_prototype/reports/lipi_034_m2104_raw_source_alias_routes.csv`
- `data/open_prototype/reports/lipi_034_m2104_raw_source_alias_summary.json`

## Evidence

| Route | Status | Evidence | Use |
| --- | --- | --- | --- |
| Local `lipi_scope_rows.csv` | Positive | `M-2104`, Mohenjo-daro, `ROD`, Ivory, `R/L`, `+151-097-700-034+` | Local target string only. |
| Local priority row | Positive | `VS 875CXIV:532 | -12.0 ft` | Alias bridge to Marshall no. 532. |
| Parpola 2019 | Positive prior, not raw | Text no. 12 is `M-2104`; Fig. 1 is standardized and actual shapes must be checked in CISI photos. | Prior-work hypothesis only. |
| Harappa `Indus Cylinder Seals` | Positive catalogue | `No. 532 (Pl. CXIV, VS 875)`, ivory, 2 in. x 0.3 in., five incised characters, Room 70 / House XXVII / VS Area. | Source-grade retrieval handle. |
| Harappa `cylinder-seals.jpg` | Positive raw public route | Plate CXIV reproduction shows no. 532 lower left. | First raw visual target for `M-2104`. |
| IA CISI OCR route | Negative | Exact `M-2104` not found; bare `2104` remains register/index noise. | Stop treating broad IA OCR search as the main route. |
| CISI 3.1 | Positive acquisition route | Bibliographic/source route with photographs, line drawings, and tablets. | Higher-resolution or updated source route, still uninspected for `M-2104`. |

## Active Requests Sent

```text
gmail:[redacted-msgid]
M-2104 source image / CISI route request to [harappa-project-email]

gmail:[redacted-msgid]
Addendum with exact Marshall alias: No. 532 / Pl. CXIV / VS 875
```

## Research Consequence

The live falsification test changes:

```text
old gate:
M-2104 target side depends on Parpola Fig. 1 standardized UIII only

new gate:
M-2104 target side can be checked against Marshall Plate CXIV no. 532,
then upgraded or rejected when a higher-resolution plate/CISI image arrives
```

If no. 532 does not visually show the expected three-stroke U/pot-side cluster corresponding to local `700-034`, the current `034` extraction fails.

If it does, the result is still only a stronger visual hypothesis until a higher-resolution source image confirms the stroke boundaries.

## Claim Status

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted numerical values: 0
accepted source mappings: 0
accepted token boundaries from this image: 0
```

## Sources

- Parpola 2019 PDF: <https://tuhat.helsinki.fi/ws/portalfiles/portal/129602857/Parpola_A_2019_Inscriptions_incised_on_the_Harappan_bone_rods_Proceedings_of_EASAA_22.pdf>
- Harappa, Indus Cylinder Seals: <https://www.harappa.com/node/3576>
- Harappa Plate CXIV image: <https://www.harappa.com/sites/default/files/styles/galleryformatter_slide/public/cylinder-seals.jpg>
- Harappa, Mohenjo-daro and the Indus Civilization: <https://www.harappa.com/content/Mohenjo-daro-and-the-Indus-Civilization>
- Harappa CISI 3.1 page: <https://www.harappa.com/content/corpus-indus-seals-and-inscriptions-vol-31>
