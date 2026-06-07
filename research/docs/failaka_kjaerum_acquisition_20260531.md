# Failaka Kjaerum 279/319 Acquisition Check

Date: 2026-05-31

Vector: V1 diffuse Meluhha bilingual source acquisition.

This is not an external-anchor claim. It is a guardrail against a tempting source-route mistake: treating any CDLI Kjaerum/Failaka record as if it were one of the two Laursen Gulf INDUS Failaka targets.

## Artifacts

- `data/meluhha/tools/build_failaka_kjaerum_acquisition_20260531.mjs`
- `data/meluhha/failaka_kjaerum_acquisition_20260531.csv`
- `data/meluhha/failaka_kjaerum_acquisition_20260531_summary.json`
- Cached CDLI JSON: `tmp/v1_external_acquisition_20260531/cdli_publication_1773730_kjaerum_failaka.json`
- Blocked DAI fetch: `tmp/v1_external_acquisition_20260531/dainst_gulf_indus_reference.pdf`
- Cached publisher/library routes:
  - `tmp/v1_external_acquisition_20260531/aarhus_university_press_failaka_kjaerum.html`
  - `tmp/v1_external_acquisition_20260531/cinii_bd0853856x_kjaerum.html`
  - `tmp/v1_external_acquisition_20260531/openlibrary_ol18985798w_failaka.html`

## What Was Re-earned

Laursen Table 1 keeps two Failaka Gulf INDUS targets live:

| Laursen no. | Reference | Current local link | Status |
| --- | --- | --- | --- |
| 12 | Kjaerum 1983 cat. no. 319 | candidate local Failaka rows `147.1/148.1`; exact row-to-cat unresolved | source-route lead only |
| 13 | Kjaerum 1983 cat. no. 279 | candidate local Failaka rows `147.1/148.1`; exact row-to-cat unresolved | source-route lead only |

The clean CDLI publication route now cached locally is publication `1773730`, `Failaka/Dilmun seals`, with four related CDLI artifacts. Their exact publication references are:

| CDLI artifact | Exact reference | Result |
| --- | --- | --- |
| `P511661` | `Failaka/Dilmun seals 168-189.` | not target `279/319` |
| `P511663` | `Failaka/Dilmun seals 162-163, No. 397` | not target `279/319` |
| `P511664` | `Failaka/Dilmun seals 158-159, No 379` | not target `279/319` |
| `P511665` | `Failaka/Dilmun seals 162-163, No 399` | not target `279/319` |

Therefore CDLI `1773730` is an adjacent Failaka/Kjaerum publication route, not an object bridge for Laursen `12` or `13`.

## Source Integrity

Input hashes:

| Input | SHA-256 |
| --- | --- |
| CDLI publication JSON | `5cb73c864926a3818500b7e15a7cf0e89758b6469d98dd6d7dc8972a9dfbf71b` |
| Gulf Type queue CSV | recorded inside `data/meluhha/failaka_kjaerum_acquisition_20260531.csv` per row |
| DAI fetch | `e8a09b86c5c019bcdc525e13c7f5042424e240a1da85d17ec6f40193f13a31fe` |

The DAI download route produced a 4,484-byte anti-bot HTML response, not a usable PDF. It cannot be cited as object evidence.

Three bibliographic/source-access routes are cached and hashed:

| Route | What it gives | Result |
| --- | --- | --- |
| Aarhus University Press | Publisher listing for `Failaka/Dilmun 1:1. The Stamp and Cylinder Seals`, 171 pages, hardback, published 1983, ISBN `87 8841 506 6` | publication route only |
| CiNii Books `BD0853856X` | Library record for the same volume, ISBN `8788415066`, 171 pages, with a University of Tsukuba holding | physical-copy route |
| Open Library `OL18985798W` | Work-level discovery route for the Failaka/Dilmun volume | bibliographic route only |

None of these exposes the actual cat. `279` or `319` catalogue/plate pages digitally.

## Decision

Accepted external anchors: `0`.

No sign value, sign meaning, language-family likelihood, translation, or external anchor is promoted.

The useful result is narrower but real: the Failaka acquisition surface is cleaner. Future V1 work must obtain the actual Kjaerum `279` and `319` catalogue/plate pages, likely through a physical-copy route, then map those pages to local rows `147.1/148.1` or reject the mapping. The CDLI `1773730` records are not allowed to stand in for that missing step.
