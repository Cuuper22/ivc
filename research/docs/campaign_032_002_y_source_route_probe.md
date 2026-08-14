# 032-002-Y Source Route Probe

Date: 2026-05-26

This note is a plan, not a finding. Before we can check rows against photographs, we have to know how to reach each photograph. A "source route" is that chain: from a transcribed row to a published page or plate. This probe sorts 25 rows by which kind of route they need, so the acquisition work can proceed in order instead of by guesswork. Signs in this corpus are numeric IDs; `Y` names whichever sign follows `002`; a "lane" is one such analysis track. CISI is the published photographic corpus of Indus inscriptions.

## Result

The 25-row `032-002-Y` source-function manifest now has a concrete acquisition route split.

Route summary:

| route | rows | objects |
|---|---:|---|
| source-volume OCR hit | 9 | `H-444`, `M-375`, `M-174`, `M-221`, `H-597`, `M-21`, `M-1385`, `M-49`, `M-722` |
| Chanhu-daro plate route | 3 | `C-10`, `C-60`, `C-65` |
| local source-reference route | 11 | `M-1044`, `M-1763`, `M-1788`, `M-720`, `M-723`, `M-91`, `M-1045`, `M-1677`, `M-1737`, `M-1728`, `M-240` |
| direct route needed | 2 | `K-145`, `H-140` |

Mechanic validation: pass.

Accepted evidence status: route planning only. This does not validate a source image, sign segmentation, side order, sign value, phonetic reading, or translation.

## Data Stored

- `data/open_prototype/reports/campaign_032_002_y_source_route_probe.csv`
- `data/open_prototype/reports/campaign_032_002_y_source_route_summary.csv`
- `data/open_prototype/reports/campaign_032_002_y_source_route_summary.json`

## Definition Corrections

Two extraction traps were corrected before accepting the route table.

1. Image filename matching now uses exact CISI tokens with non-alphanumeric boundaries, allowing hyphen/underscore variation. This prevents `M-91` from matching `M-918` image crops and `M-21` from matching `M-2104`.
2. OCR counting now uses exact token boundaries and counts only unique CISI India/Pakistan source-volume files. Mahadevan text concordance hits are recorded separately and do not make a row source-visible.

Checked exact OCR counts:

- `H-444`: 2
- `H-597`: 2
- `M-1385`: 10
- `M-722`: 2
- `M-91`: 0
- `M-21`: 8

## Source-Function Implication

The next work can stop hunting blindly. It should split into four lanes:

### Lane 1: source-volume OCR hits

Use the existing CISI source-volume OCR route to locate page images, crop the target panel, and record label/side.

Priority target/control rows:

- `M-722`: target `+740-585-240-220-032-002-817+`
- `M-49`: target non-core `+527-550-240-220-032-002-300-350-032-190+`
- `M-21`: outside core `+350-001-740-362-692-032-002-861+`
- `M-1385`: outside core `+740-760-032-002-817+`
- `H-444`: non-240 core `+241-220-032-002-861+`

### Lane 2: Chanhu-daro plate routes

The local source references already name exact plate hooks:

- `C-65`: `CH 2428 Pl. LII:19`, target `002-861`
- `C-60`: `CH 2605 Pl. LII:24`, outside core `002-861`
- `C-10`: `CH 2297 Pl. LI:29`, non-240 core `002-817`

These are cross-site high-value rows because they test whether the packet exists outside Mohenjo-daro.

### Lane 3: local source-reference routes

Resolve source references such as `HR`, `DK`, `DK-E`, and `DK-C` identifiers to plates/archive images.

Highest value:

- `M-1728`: target `+161-055-240-220-032-002-820+`, `DK-E 1585079`
- `M-240`: target extended `+520-240-220-032-002-861-603+`, `HR 4098324`
- `M-1044`: non-240 core `+520-220-032-002-861+`, `HR 4399551`
- `M-1677`: outside extended core `+520-382-032-002-820-001-440-012+`, `DK11358130`

### Lane 4: direct route needed

These remain direct request/archive rows:

- `K-145`: non-240 core `+740-585-231-220-032-002-820+`
- `H-140`: outside core `+740-384-032-002-817+`

## Next Campaign

Run the `032-002-Y source-function batch` with route lanes in this order:

1. Crop and inspect source-volume OCR hit rows.
2. Acquire/check Chanhu-daro plate rows.
3. Resolve local source-reference rows.
4. Request direct-route rows only after the first three lanes produce a source-classification table.

For each row, record:

```text
source image present
same physical line
032 distinct
002 distinct
Y distinct
direction/order status
tail ends or continues
iconography
site/type/register
neighbor context before A-220 or before 032
```

Decision target:

```text
Are 861, 820, and 817 interchangeable terminal choices after 032-002,
or separate source-visible subformula branches?
```
