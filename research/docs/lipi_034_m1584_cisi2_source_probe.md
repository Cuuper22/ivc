# Lipi 034 M-1584 CISI 2 Source Probe

Date: 2026-05-25

Question:

```text
Can M-1584 move from public-dark P0 target to source-visible evidence for the exact single-sign local row +034+?
```

Input:

- `data/open_prototype/lipi/metadata_filtered.csv`
- `tmp/cisi_xml/Corpus of Indus Seals and Inscriptions. Collections in Pakistan_djvu.txt`
- `tmp/m1584_cisi2/n266_w2000.jpg`
- `tmp/m1584_cisi2/n474_w2000.jpg`

Output:

- `data/open_prototype/reports/lipi_034_m1584_cisi2_routes.csv`
- `data/open_prototype/reports/lipi_034_m1584_cisi2_visual_inputs.csv`
- `data/open_prototype/reports/lipi_034_m1584_cisi2_adjudication.csv`
- `data/open_prototype/reports/lipi_034_m1584_cisi2_segmentation_scenarios.csv`
- `data/open_prototype/reports/lipi_034_m1584_cisi2_summary.json`
- `data/open_prototype/reports/lipi_034_m1584_single_sign_contrasts.csv`
- `data/open_prototype/reports/lipi_034_m1584_single_sign_contrasts_summary.json`

## Local Object

```text
M-1584 / 3807.1 / +034+
Mohenjo-daro, Lower Indus
Clay pottery/graffiti row: POT:T:g
sides=1, direction NR, class NU
fragment, condition Poor, complete Y
```

## Result

```text
source-route rows: 6
visual input rows: 9
adjudication rows: 6
segmentation scenarios: 6
single-sign contrast rows: 23
sent source requests: 1
accepted object visual bindings: 1
accepted decipherment claims: 0
```

CISI Vol. 2 printed p. 232 / Internet Archive leaf `n266` makes M-1584 source-visible. The page header reads:

```text
MOHENJO-DARO 1579-1587
GRAFFITI on pottery, rim
```

The page visibly labels the target:

```text
M-1584 A (50 %)
```

This upgrades M-1584 from public-source-dark to source-visible object binding. It does not validate the numeric transcription `034`. The public image shows the pottery fragment and marks, but the inspected source layer does not print a clean sign-code mapping beside the image.

## Visual Evidence

Downloaded and cropped:

- Source page: `tmp/m1584_cisi2/n266_w2000.jpg`
- Page header crop: `tmp/m1584_cisi2/derived/n266_page_header_crop.jpg`
- M-1584 object and label crop: `tmp/m1584_cisi2/derived/n266_m1584_object_label_crop.jpg`
- M-1584 rim-mark context crop: `tmp/m1584_cisi2/derived/n266_m1584_true_sign_context_2x.png`
- M-1584 rim-mark close crop: `tmp/m1584_cisi2/derived/n266_m1584_true_sign_close_2x.png`
- Data page: `tmp/m1584_cisi2/n474_w2000.jpg`
- Data row context crop: `tmp/m1584_cisi2/derived/n474_m1578_m1586_data_crop_2x.png`
- Boundary pages: `tmp/m1584_cisi2/n265_w2000.jpg`, `tmp/m1584_cisi2/n267_w2000.jpg`

The close crop includes the neighboring `M-1582 A+E` printed label above the object. That label belongs to the neighboring source panel and must not be used as M-1584 metadata.

## Source Route

- CISI Vol. 2 IA item: <https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan>
- CISI Vol. 2 p. 232 reader leaf: <https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n266/mode/1up>
- CISI Vol. 2 p. 232 direct raster: <https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n266_w2000.jpg>
- CISI Vol. 2 p. 440 reader leaf: <https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n474/mode/1up>
- CISI Vol. 2 p. 440 direct raster: <https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n474_w2000.jpg>
- CISI Vol. 2 DjVu XML: <https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan_djvu.xml>

The OCR locator is useful only as a page pointer. It captures the range page and neighboring labels, but misses or mangles the exact `M-1584` label. Manual page inspection is decisive here.

## Data Page

CISI Vol. 2 printed p. 440 / IA leaf `n474` is the data page for `M-1437 to M-1611`.

The M-1584 row is visible but blurred. Conservative extraction:

```text
M-1584
2911
middle field unreadable / ???
LF?
D&K, p. 567-N5
```

This confirms a source-row route but should not be overcoded. The local `lipi` row has no excavation ID, so the source-data row is a reconciliation target rather than a solved bridge.

## Single-Sign Contrast

The targeted contrast set is stored in `data/open_prototype/reports/lipi_034_m1584_single_sign_contrasts.csv`.

```text
rows containing 034: 182
exact +034+ rows: 11
single-sign rows containing 034: 32
damaged or bracketed single-034 rows: 21
exact +034+ pottery/clay rows: 9
Lower Indus exact +034+ rows: 2
Mohenjo-daro exact +034+ rows: 1
```

Exact bounded singleton controls:

```text
032: 47 exact bounded rows
033: 25 exact bounded rows
034: 11 exact bounded rows
004: 6 exact bounded rows
700: 11 exact bounded rows
002: 12 exact bounded rows
```

M-1584 is one of two Lower Indus exact `+034+` rows, the other being `Ns-72` at Nausharo. Most exact `+034+` rows are pottery/clay and `NR/NU`, so the immediate pressure is potmark/graffiti behavior, not line-text syntax.

## Adjudication

Accepted:

- CISI Vol. 2 p. 232 is source-visible and labels `M-1584 A (50 %)`.
- The source page classifies the panel as Mohenjo-daro graffiti on pottery rim.
- The local object class `POT:T:g`, material `Clay`, and fragmentary/poor condition agree with the source-page visual context.
- M-1584 can now be used as a source-targeted `034` graphic-pressure object.

Rejected or quarantined:

- No numeric source mapping to sign `034` is accepted from the public image alone.
- No standalone linguistic value is accepted from `+034+`.
- No phonetic value, morpheme, commodity, number, administrative function, or translation is accepted.
- Complete-singleton status remains source-gated because the object is a fragment and the source photo is `50 %`.
- The p. 440 data row is too blurred for confident full-field extraction.

## Sent Request

```text
gmail:19e6014217a8eeaa
Sent to harappa@gmail.com requesting higher-resolution M-1584 A source material, data-row confirmation, transcription/sign-list convention, direction or image convention, complete-single-mark status, and permission/citation terms.
```

## Next Gate

The next evidence gate is:

```text
high-resolution M-1584 A image or line drawing
source transcription or sign-list bridge for +034+
confirmation that the visible mark is a complete bounded single mark
confirmation that no adjacent signs are lost at fragment edges
full p. 440 data-row fields and source-reference bridge
comparison against source-visible exact +034+, +033+, and +032+ singletons
```

If the high-resolution source shows a bounded single mark and the source transcription independently treats it as `034`, M-1584 becomes a real graphic singleton witness. If it shows edge loss, ambiguous scratches, or a different sign convention, M-1584 stays only an object-visible pottery/graffiti target.
