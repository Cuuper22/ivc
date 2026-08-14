# Lipi 034 M-2104 M77 Identity And Segmentation Probe

Date: 2026-05-25

This note is a probe — a bounded check aimed at one question, not a finished result. It asks how much a printed, cleaned-up scholarly transcription can settle about a single object.

The object goes by several names: our local row `M-2104`, Marshall's catalogue no. `532`, excavation number `VS 875`. `034` is one of our local numeric sign labels, a transcription code rather than a reading. Segmentation is the decision about where one sign ends and the next begins. The note exists because standardized print looks like evidence about the object and mostly is not: it is a scholar's tidy drawing of the signs, one step removed from the artifact.

## Question

What does the Mahadevan/Parpola standardized text layer add to the `M-2104` / Marshall no. `532` / `VS 875` / local `034` problem?

## Result

No decipherment upgrade. Real progress, but it cuts against overconfidence.

The local `lipi` row already ties the identifiers together internally. That is a bridge — a chain of records linking identifiers to one another — but an internal one, built by us:

```text
id: 2527.1
cisi: M-2104
excavation-idno: VS 875CXIV:532
material/type: Ivory / ROD
depth: -12.0 ft
text: +151-097-700-034+
```

Mahadevan's 1977 text list adds a second localizable layer: page `0084` of the IA scan has text no. `2527`, code `100901`, and a printed standardized sign row. I downloaded the page, cropped the row, and stored the crop and overlay.

Parpola 2019 adds the prior-work explanation: `Text no. 12 (M-2104)` is described as `UIII` plus signs 15 and 1, while the tablet parallels use `UIIII` plus signs 15 and 107. That is exactly why local `+151-097-700-034+` versus `+400-097-700-004+` looked like a useful `034`/`004` count-cluster test.

But Parpola also downgrades the evidence: his Fig. 1 uses standardized signs, not the rods' actual shapes, and tells readers to check CISI photos for the actual shapes. So this is prior-work pressure, not raw artifact validation.

## Stored Outputs

- `data/open_prototype/reports/lipi_034_m2104_m77_identity_routes.csv`
- `data/open_prototype/reports/lipi_034_m2104_m77_visual_inputs.csv`
- `data/open_prototype/reports/lipi_034_m2104_m77_identity_adjudication.csv`
- `data/open_prototype/reports/lipi_034_m2104_m77_identity_summary.json`

Derived local visual files:

- `tmp/mahadevan_m77_pages/m77_0084.jp2`
- `tmp/mahadevan_m77_pages/m77_0084.png`
- `tmp/mahadevan_m77_pages/derived/m77_row2527_full.png`
- `tmp/mahadevan_m77_pages/derived/m77_row2527_full_enhanced3x.png`
- `tmp/mahadevan_m77_pages/derived/m77_row2527_signs.png`
- `tmp/mahadevan_m77_pages/derived/m77_row2527_signs_enhanced3x.png`
- `tmp/mahadevan_m77_pages/derived/m77_0084_row2527_overlay.png`

## Source Layers

| Layer | What It Gives | What It Does Not Give |
| --- | --- | --- |
| Local `lipi` row `2527.1` | Internal bridge: `M-2104`, `VS 875CXIV:532`, ivory rod, `+151-097-700-034+`. | Independent source-grade confirmation. |
| Mahadevan 1977 page `0084` | Text no. `2527`, code `100901`, printed standardized sign row. | Raw object photo, CISI object note, or Marshall alias. |
| Parpola 2019 | `M-2104` as `Text no. 12`, plus the `UIII` and signs 15/1 prior reading. | Raw shapes; Parpola explicitly points to CISI photos for those. |
| Marshall/Harappa no. `532` | `Pl. CXIV`, `VS 875`, ivory rod, five deeply incised characters. | `M-2104` identifier and a reconciliation of five characters versus four local tokens. |
| IA/IGNCA Plate CXIV | Best current public visual witness — independent image evidence — for no. `532`. | Secure exact three-stroke `034` or source-grade token boundaries. |

## Adjudication

The ruling on each claim. Pass and fail are fixed verdicts here, not shades of opinion.

| Claim | Verdict | Reason |
| --- | --- | --- |
| Local row ties `M-2104` to `VS 875CXIV:532`. | Retain as internal bridge only. | The row is useful for source routing, but it is not an external confirmation. |
| Public layer explicitly ties `M-2104` to no. `532` / `VS 875`. | Fail. | Checked public routes split into two legs: Parpola gives `M-2104`; Marshall/Harappa gives no. `532` / `VS 875`. No public bridge found. |
| M77 text no. `2527` supports the local row lineage. | Pass for standardized text layer. | It supports why local id `2527.1` exists, not raw artifact identity or segmentation. |
| Parpola supports the `700-034` as `UIII` hypothesis. | Live hypothesis, downgraded. | It is standardized and explicitly not a raw-shape witness. |
| Marshall five characters can be ignored. | Fail. | Five Marshall characters versus four local tokens is now a primary segmentation problem. |
| `034` is validated as exactly three strokes. | Fail. | Public no. `532` crop remains three-vs-four ambiguous. |

## Consequence

`M-2104` stays live only as a quarantined candidate source route — a promising path to the object that is held out of decipherment work until it closes. It is not an accepted `034` attestation.

The actual advance is locating the compression point — the place where raw-object evidence gets flattened into standardized and then local numeric layers:

```text
raw object? -> CISI/Marshall photo and catalog note still needed
standardized text layer -> M77 text no. 2527 / Parpola text no. 12
local numeric layer -> lipi 2527.1 +151-097-700-034+
```

Follow-on CISI scope correction: the accessible CISI Pakistan Vol. 2 OCR says its Mohenjo-daro section covers `M-595` and `M-621` to `M-1659`. `M-2104` is outside that range. The only exact OCR `2104` hit in that volume is on printed p. 445, a `DATA H-989 to Rhd-156` page, not an `M-2104` object entry. I rendered and stored that false-positive page as a control.

That tells us exactly what to demand next: CISI 3.1 or later supplemental Mohenjo-daro material, or museum/archive metadata that explicitly links `M-2104`, Marshall no. `532`, and `VS 875`, plus a raw object photograph or segmentation note explaining the five-character/four-token mismatch.

## Claim Status

What this packet — one self-contained bundle of evidence and rulings — is allowed to add to the project's accepted set. The answer is nothing:

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted numerical values: 0
accepted source mappings: 0
accepted token boundaries from this packet: 0
```

## Sources

- Parpola 2019 PDF: <https://tuhat.helsinki.fi/ws/portalfiles/portal/129602857/Parpola_A_2019_Inscriptions_incised_on_the_Harappan_bone_rods_Proceedings_of_EASAA_22.pdf>
- University of Helsinki publication page: <https://researchportal.helsinki.fi/fi/publications/inscriptions-incised-on-harappan-ivorybone-rods-and-their-paralle>
- Mahadevan 1977 IA item: <https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan>
- Mahadevan page `0084` JP2: <https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/The%20Indus%20Script.%20Text%2C%20Concordance%20and%20Tables%20-Iravathan%20Mahadevan_jp2.zip/The%20Indus%20Script.%20Text%2C%20Concordance%20and%20Tables%20-Iravathan%20Mahadevan_jp2%2FThe%20Indus%20Script.%20Text%2C%20Concordance%20and%20Tables%20-Iravathan%20Mahadevan_0084.jp2>
- Harappa, Indus Cylinder Seals: <https://www.harappa.com/node/3576>
- IA/IGNCA Marshall Vol. III item: <https://archive.org/details/in.gov.ignca.48270>
- IA/IGNCA Plate CXIV IIIF image: <https://iiif.archive.org/image/iiif/3/in.gov.ignca.48270%2F48270_jp2.zip%2F48270_jp2%2F48270_0205.jp2/full/max/0/default.jpg>
