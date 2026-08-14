# Lipi 034 M-315 CISI 1 Source Probe

Date: 2026-05-25

This note is a source probe: a bounded check on whether a published source really shows the object we think it shows, at a quality we can work from.

Seal `M-315` matters because of a scarcity. Across our filtered corpus it is the single row carrying the sign sequence `390-034-002`. That makes it valuable and fragile at once. A whole pattern resting on one row is a pattern resting on one transcription decision, so before it can carry any weight the object itself has to be visible in print.

Question:

```text
Can M-315 move from a Kenoyer/Meadow route note into source-visible evidence for the non-terminal, non-FRAME700 034 case +390-034-002-374-228-741+?
```

Input:

- `data/open_prototype/lipi/metadata_filtered.csv`
- `tmp/cisi_xml/Corpus of Indus Seals and Inscriptions. Collections in India_djvu.xml`
- `tmp/m315_cisi1/n113_w2000.jpg`
- `tmp/m315_cisi1/n403_w2000.jpg`

Output:

- `data/open_prototype/reports/lipi_034_m315_cisi1_routes.csv`
- `data/open_prototype/reports/lipi_034_m315_cisi1_visual_inputs.csv`
- `data/open_prototype/reports/lipi_034_m315_cisi1_adjudication.csv`
- `data/open_prototype/reports/lipi_034_m315_cisi1_segmentation_scenarios.csv`
- `data/open_prototype/reports/lipi_034_m315_cisi1_summary.json`
- `data/open_prototype/reports/lipi_034_m315_390_slot_contrasts.csv`
- `data/open_prototype/reports/lipi_034_m315_390_slot_contrasts_summary.json`

## Local Object

```text
M-315 / 2833.1 / +390-034-002-374-228-741+
Mohenjo-daro, VSA, 2VIII, 432 X/18
Local excavation-idno: VS 1190395
Steatite square seal, no symbol/cult, sides=1, direction R/L
Condition good, complete, slightly chipped
Dimensions in local layer: 27.9 x 27.9 x 0 mm
```

## Result

```text
source-route rows: 10
visual input rows: 21
adjudication rows: 7
segmentation scenarios: 6
390-X-002 contrast rows: 40
sent source requests: 1
accepted object visual bindings: 1
accepted decipherment claims: 0
```

This is no longer just a bibliographic route. Internet Archive's CISI Vol. 1 scan makes printed p. 78 source-visible. The page header reads `MOHENJO-DARO 313-317 SEALS` and `no iconography; silver`, and the page visibly labels both `M-315 A` and `M-315 a`.

The data page is also source-visible. Printed p. 368 has a row readable as:

```text
M-315  1395  VS 1190  ASI 63.10.117  HU 318
```

That creates a useful reconciliation target: the local row has `VS 1190395`, while the source-visible data row appears to split `1395` and `VS 1190` into separate columns. Do not treat the local excavation string as source-perfect until this is reconciled.

## Visual Evidence

Downloaded and cropped:

- Source page: `tmp/m315_cisi1/n113_w2000.jpg`
- Data page: `tmp/m315_cisi1/n403_w2000.jpg`
- Header/context crop: `tmp/m315_cisi1/derived/m315_page78_header_context.png`
- Upper face crop: `tmp/m315_cisi1/derived/m315_upper_face_signs_close.png`
- Lower impression crop: `tmp/m315_cisi1/derived/m315_lower_impression_signs_close.png`
- Upper second-sign target: `tmp/m315_cisi1/derived/m315_upper_face_second_034_region.png`
- Lower second-sign target: `tmp/m315_cisi1/derived/m315_lower_impression_second_034_region.png`
- Data-row crop: `tmp/m315_cisi1/derived/m315_data_page_row_context.png`

Important mechanical note: Windows is case-insensitive, so early `M315_A` and `M315_a` crop names collided. The final stored evidence uses `upper_face` and `lower_impression` names to avoid overwriting the two witnesses — the two separate images of the object, each an independent piece of evidence.

## Source Route

- CISI Vol. 1 IA item: <https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan>
- CISI Vol. 1 p. 78 reader leaf: <https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India/page/n113/mode/1up>
- CISI Vol. 1 p. 78 direct raster: <https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India/page/n113_w2000.jpg>
- CISI Vol. 1 p. 368 data reader leaf: <https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India/page/n403/mode/1up>
- CISI Vol. 1 p. 368 direct raster: <https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India/page/n403_w2000.jpg>
- CISI Vol. 1 DjVu XML: <https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20India_djvu.xml>
- Kenoyer/Meadow 2010 route note: <https://www.harappa.com/sites/default/files/pdf/KenoyerMeadow%202010%20Inscribed%20Objects%20from%20Harappa.pdf>

The Kenoyer/Meadow route is now corroborated as a route, not upgraded into a reading. It pointed correctly to CISI 1 p. 78, but it still supplies typological context rather than sign segmentation.

## Slot Contrast

A slot is one position in the sign row. Holding the neighbours fixed and listing everything that ever appears in the open slot shows how unusual our row really is.

The targeted local contrast set is stored in `data/open_prototype/reports/lipi_034_m315_390_slot_contrasts.csv`.

```text
rows with prefix 390-X-002: 37
rows with prefix 390-034-002: 1
rows with prefix 390-034: 3
rows with 034 in second position: 126
```

Second-sign distribution inside `390-X-002`:

```text
003: 14
004: 10
016: 4
005: 4
017: 1
415: 1
015: 1
034: 1
869: 1
```

So M-315 is a high-value singleton: it is the only local `390-034-002` row. The only other `390-034` openings are `Ai-7 +390-034+` and `H-335 +390-034+`. This makes M-315 important, but also fragile. One bad source segmentation would create the entire `390-034-002` signal.

## Adjudication

The ruling: what this probe lets the project carry forward, and what it does not.

Accepted:

- CISI 1 p. 78 is source-visible and labels `M-315 A` and `M-315 a`.
- CISI 1 p. 368 is source-visible and has a data row for M-315.
- The no-iconography/no-animal context is real for the page group.
- The visible M-315 image has six graphic units and is testable against the local six-token row.
- M-315 is the only `390-034-002` row in the current filtered local layer.

Rejected or quarantined — quarantine means held out of downstream use until the problem is fixed:

- No numeric sign mapping is accepted from the image alone.
- No value, function, phonetic reading, language identity, or translation is accepted.
- The local `VS 1190395` string is quarantined until reconciled with source-visible `1395` and `VS 1190`.
- Direction is unresolved: the page shows both a light face and dark impression, and the local row says `R/L`.
- No-animal context is retrieval/context evidence only, not sign meaning.

## Next Gate

The gate is the next test this line of work must pass before it advances. It is a list of things to ask a source for, not a list of conclusions.

The next decisive source check is not broad scraping. It is narrow:

```text
M-315 A/a high-resolution source image or line drawing
face/impression convention
direction basis for R/L
source sign-count convention for the six visible units
whether the second visible unit is explicitly 034 or a different sign-list code
reconciliation of 1395 / VS 1190 with local VS 1190395
```

## Sent Request

```text
gmail:[redacted-msgid]
Sent to [harappa-project-email] requesting higher-resolution M-315 A/a source material, sign transcription or sign-list convention, direction basis, VS 1190/1395 reconciliation, and permission/citation terms.
```
