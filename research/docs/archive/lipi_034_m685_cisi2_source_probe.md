# Lipi 034 M-685 CISI 2 Source Probe

Date: 2026-05-25

This note is a source probe: a bounded check on whether a published volume actually shows the object we have been tracking on paper only.

The object is seal `M-685`, and it is broken. Our transcription reads `]034-204+`, where the bracket marks a break in the object — the text is missing whatever came before. A broken row is worth chasing and dangerous to lean on: the sign we care about sits right at the fracture, so we cannot know it was the first sign, or even that it survived whole.

Question:

```text
Can M-685 move from a Bhaskar S1 catalogue lead into source-visible evidence for the fragmentary 034 case ]034-204+?
```

Input:

- `data/open_prototype/lipi/metadata_filtered.csv`
- `tmp/cisi_xml/Corpus of Indus Seals and Inscriptions. Collections in Pakistan_djvu.xml`
- `tmp/m685_cisi2/n71_w2000.jpg`
- `tmp/m1206_bhaskar/S1-IndusZoomorphicIconCatalogue.pdf`

Output:

- `data/open_prototype/reports/lipi_034_m685_cisi2_routes.csv`
- `data/open_prototype/reports/lipi_034_m685_cisi2_visual_inputs.csv`
- `data/open_prototype/reports/lipi_034_m685_cisi2_adjudication.csv`
- `data/open_prototype/reports/lipi_034_m685_cisi2_segmentation_scenarios.csv`
- `data/open_prototype/reports/lipi_034_m685_cisi2_summary.json`
- `data/open_prototype/reports/lipi_034_m685_034_204_contrasts.csv`
- `data/open_prototype/reports/lipi_034_m685_034_204_contrasts_summary.json`

## Local Object

```text
M-685 / 3121.1 / ]034-204+
Mohenjo-daro, HR-
Local excavation-idno: HR 4244276
Steatite square seal, local symbol Bull1
sides=1, direction R/L
fragment, condition Poor, complete ?
```

## Result

```text
source-route rows: 7
visual input rows: 22
adjudication rows: 7
segmentation scenarios: 6
034-204 contrast rows: 33
sent source requests: 1
accepted object visual bindings: 1
accepted decipherment claims: 0
```

Internet Archive's CISI Vol. 2 scan makes printed p. 37 source-visible. The page header reads:

```text
'unicorn' II
SEALS
MOHENJO-DARO 683-686
37
```

The page visibly labels both `M-685 A` and `M-685 a`.

This upgrades M-685 from catalogue lead to source-visible object binding — meaning a published page now ties our row to a pictured object. It does not validate the numeric transcription. The local row is fragmentary, starts with a leading bracket, and the source page does not print numeric sign codes beside the image.

## Visual Evidence

Downloaded and cropped:

- Source page: `tmp/m685_cisi2/n71_w2000.jpg`
- Header/context crop: `tmp/m685_cisi2/derived/m685_page37_header_context.png`
- Full page context: `tmp/m685_cisi2/derived/m685_page37_m683_m686_context.png`
- M-685 face crop: `tmp/m685_cisi2/derived/m685_face_signs_close.png`
- M-685 impression crop: `tmp/m685_cisi2/derived/m685_impression_signs_close.png`
- First visible sign target: `tmp/m685_cisi2/derived/m685_face_left_break_034_region.png`
- Impression-side first visible sign target: `tmp/m685_cisi2/derived/m685_impression_left_break_034_region.png`
- Second sign target: `tmp/m685_cisi2/derived/m685_face_204_region.png`
- Impression-side second sign target: `tmp/m685_cisi2/derived/m685_impression_204_region.png`

## Source Route

- CISI Vol. 2 IA item: <https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan>
- CISI Vol. 2 p. 37 reader leaf: <https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n71/mode/1up>
- CISI Vol. 2 p. 37 direct raster: <https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan/page/n71_w2000.jpg>
- CISI Vol. 2 DjVu XML: <https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan_djvu.xml>
- Bhaskar S1 catalogue route: <https://storage.googleapis.com/cahcblr-pdfs/assets/ijhs/S1-IndusZoomorphicIconCatalogue.pdf>

The OCR locator is useful but not decisive: `Pakistan_0071.djvu` has an `M-685` hit at `1440,3084,1572,3044,3084`.

## Iconography Conflict

Iconography here means the animal figure carved on the seal beside the text. Three records disagree about which animal it is. That disagreement is recorded rather than resolved, because it shows our own metadata is not error-free.

The source route exposes a metadata conflict:

```text
CISI p.37 header: 'unicorn' II
Bhaskar S1: M-685, text-present checkmark, b, Unicorn
Local lipi: symbol Bull1
```

That conflict matters because local iconography metadata cannot be used as if it were source-perfect. It does not change the inscription target, but it blocks any iconography-conditioned interpretation until the source data row or a higher-resolution catalogue note explains the discrepancy.

## 034-204 Contrast

How rare this pairing is in the corpus, counted plainly.

The targeted local contrast set is stored in `data/open_prototype/reports/lipi_034_m685_034_204_contrasts.csv`.

```text
rows containing 204: 8
rows containing both 034 and 204: 1
rows with adjacent 034-204: 1
clean +034-204+ rows: 0
broken ]034-204+ rows: 1
fragmentary 034 rows: 26
Mohenjo-daro Bull fragment 034 rows: 1
```

M-685 is the only row with adjacent `034-204`, and the only row containing both tokens in the filtered corpus. That makes it useful, but the leading break makes it unsafe as a standalone semantic or functional clue.

## Adjudication

The ruling: what this probe lets the project carry forward, and what it does not.

Accepted:

- CISI Vol. 2 p. 37 is source-visible and labels `M-685 A` and `M-685 a`.
- Bhaskar S1 independently lists `M-685` as a text-present Unicorn row with marker `b`.
- The source page and Bhaskar S1 agree on Unicorn context.
- M-685 is the only `034-204` row in the filtered local layer.

Rejected or quarantined — quarantine means held out of downstream use until the problem is fixed:

- No numeric sign mapping is accepted from the image alone.
- No value, function, phonetic reading, language identity, or translation is accepted.
- The leading bracket means `034` is not accepted as initial.
- The local `Bull1` symbol is quarantined against CISI/Bhaskar Unicorn evidence.
- No source data row connecting `M-685` to `HR 4244276` was found in the current OCR pass.

## Next Gate

The gate is the next test this line of work must pass. It is a list of things to demand from a source, not a list of conclusions.

The narrow source gate is:

```text
M-685 A/a high-resolution source image or line drawing
face/impression convention
direction basis for R/L
source transcription convention for ]034-204+
whether the first visible sign is explicitly 034 or a damaged/allographic 03x
whether any lost left context is known or inferable from the source catalogue
data-row bridge to HR 4244276
iconography note resolving Unicorn versus local Bull1
```

## Sent Request

```text
gmail:[redacted-msgid]
Sent to [harappa-project-email] requesting higher-resolution M-685 A/a source material, sign transcription or sign-list convention, direction basis, HR 4244276 bridge data, iconography notes, and permission/citation terms.
```
