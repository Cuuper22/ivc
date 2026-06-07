# 032-002-861 / 002-390-X M-1825 Source Route Recheck

Date: 2026-05-31 America/Los_Angeles

Status: acquisition route triaged; no source-token upgrade.

## Target

Local row:

- Row: `3992.1`
- Object: `M-1825`
- Site: Mohenjo-daro
- Type: `SEAL:S`
- Symbol/cult: `Bull1` / `S`
- Shape: square
- Excavation/source pointer: `BJ25710`
- Dimensions: `17.5 x 18.5 x 0`
- Direction: `R/L`
- Text: `+157-031-002-390-705+`

The live question was whether `M-1825` can become a source-bound witness for the repeated terminal `002-390-705` branch. It cannot on the evidence found in this pass.

## Sources Checked

### Local metadata

`data/open_prototype/lipi/metadata_filtered.csv` preserves the target row as `3992.1`, object `M-1825`, with pointer `BJ25710` and text `+157-031-002-390-705+`.

### Internet Archive CISI Pakistan OCR/XML

Downloaded:

- `tmp/m1825_source_route_20260531/cisi_pakistan_djvu.txt`
- `tmp/m1825_source_route_20260531/cisi_pakistan_djvu.xml`

Archive source:

- `https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan_djvu.txt`
- `https://archive.org/download/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan/Corpus%20of%20Indus%20Seals%20and%20Inscriptions.%20Collections%20in%20Pakistan_djvu.xml`

Exact and near-exact searches were run for `M-1825`, `M 1825`, `1825`, `BJ25710`, `BJ 25710`, `25710`, and the local sequence. No clean object/pointer hit was found.

The XML page-map pass does expose the public plate sequence. The Mohenjo-daro plate headers start around IA leaf `Pakistan_0035` with `MOHENJO-DARO 595` and run through the visible plate section to about `Pakistan_0286`, where the OCR header reaches `MOHENJO-DARO 1657-1658`. No `M-1825` plate route appears in the checked IA Pakistan OCR/XML layer.

This does not prove that `M-1825` has no source image anywhere. It proves only that the public IA Pakistan OCR/XML route checked here does not bind it.

### Public web search

Exact public searches for `M-1825`, `M 1825`, `BJ25710`, `BJ 25710`, and `M-1825 CISI/Harappa/Mohenjo-daro` did not recover an artifact image or sign-band route.

The one useful public hit is the Bhaskar et al. supplemental catalogue:

- `https://cahc.jainuniversity.ac.in/assets/ijhs/S1-IndusZoomorphicIconCatalogue.pdf`

Local extracted text:

- `tmp/m1206_bhaskar/S1-IndusZoomorphicIconCatalogue.txt`

It lists `M-1825` as an `F2` unicorn object. That confirms object/icon-class presence in a secondary catalogue, not the inscription, sign order, source plate, or token boundary.

## Decision

`M-1825` is now classified as:

`m1825_ia_pakistan_absent_secondary_icon_only_no_signband`

Use it as acquisition pressure only. Do not count it as a strict source-bound `705` witness.

Consequences:

- Repeated `002-390-705` remains locally interesting but source-gated.
- `705` still has zero strict source-image witnesses in this branch gate.
- Dholavira `4237.1` / Acc. No. `8758` is now the only live repeated-`705` source-binding route in this campaign layer.
- No value, phonetics, sign meaning, function, language identity, or translation is accepted.

## Next Route

Find a source volume, museum archive, HARP entry, excavation plate, or catalogue bridge that explicitly binds `M-1825` or `BJ25710` to an image/sign band. The needed bridge is object-to-image-to-sign-band, not another icon-class list.
