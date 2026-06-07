# Lipi FRAME700 034 CISI Variant Convention Probe

Date: 2026-05-25

## Question

Do the CISI volume conventions explain the messy labels that blocked `H-771`, `H-893`, `H-925`, `H-983`, and `H-353`?

## Inputs

- IA bundle: <https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan>
- CISI India OCR: `Corpus of Indus Seals and Inscriptions. Collections in India_djvu.txt`
- CISI Pakistan OCR: `Corpus of Indus Seals and Inscriptions. Collections in Pakistan_djvu.txt`
- Script: `data/open_prototype/tools/lipi_frame700_034_cisi_variant_convention_probe.mjs`
- CSV: `data/open_prototype/reports/lipi_frame700_034_cisi_variant_convention_probe.csv`
- Summary: `data/open_prototype/reports/lipi_frame700_034_cisi_variant_convention_probe_summary.json`

No page images are stored as research artifacts.

## Convention Results

The CISI introduction gives four rules that matter here:

| Rule | Source locator | Research consequence |
| --- | --- | --- |
| Original objects and impressions complement each other; the original remains the authority. Reversed prints were avoided because some seals have reversed writing. | India OCR lines `1409-1442`; Pakistan OCR lines `1857-1889` | Do not normalize direction from the current scans. |
| Capital letters normally mark sides: `A` obverse, `B` reverse, `C` upper, `D` right, `E` lower, `F` left. Three-sided prisms use `A/B/C` for principal rectangular sides. | India OCR lines `1476-1499`; Pakistan OCR lines `1934-1958` | `A/B/C` are side labels under normal CISI convention. |
| `bis`, `ter`, `quater`, and `quinquies` mark later photographs of the same side, usually in temporal order. | India OCR lines `1506-1536`; Pakistan OCR lines `1964-1973` | Do not count `bis/ter/quater` as extra physical sides by themselves. |
| Parenthesized numerals after a side letter mark same-side parts or enlargements; Arabic numerals after side letters mark separate inscriptions on one side. | India OCR lines `1501-1536`; Pakistan OCR lines `1959-1973` | This does not cleanly explain labels like `H-893 (1) A` or `H-925 (2) B`, where the number comes before the side letter. |

## Target Reconciliation

| Object | What is now reconciled | Still blocking |
| --- | --- | --- |
| `H-771` | `A bis`, `A ter`, and `A quater` are multiple photographs of side `A`, not four extra physical sides. `B` remains the distinct side-label candidate. | Which `A` photograph anchors the companion row, whether preservation changed, and whether `B` can support the local `+700-034+` row without independent subtype/direction proof. |
| `H-893` | Base `A/B` are side labels. | `H-893 (1) A/B` is not explained by the general same-side `letter (1)` convention; catalog notes must identify it before comparison. |
| `H-925` | `A bis`, `B bis`, and `A ter` are multiple photographs of sides. | `H-925 (1)/(2) A/B` remains unresolved, so this shared `033` control is still dangerous. |
| `H-983` | `A bis`, `B bis`, `B ter`, and `C bis` are same-side photograph variants. | `C` is still a real source side category, so the local two-side packet is incomplete for source comparison. |
| `H-353` | IA leaves `265` and `696` are duplicate visual locators at w1200: SHA256 `5422DE7097106AA1AEF205A067924D153321F7DD91ED1A60BC7A77D2312A4AA6`. | `C` is still a real source side category. The local two-side packet omits it. |

## Correction To Previous Gate

The previous messy-panel result stays negative, but the failure language needs tightening:

```text
Not all excess visible labels are excess physical sides.
bis/ter/quater = additional photographs of the same side.
A/B/C = side categories.
H-893 (1) A/B and H-925 (1)/(2) A/B = still unresolved object-number labels.
```

That means:

- `H-771` is less physically mismatched than first described, but still unusable as a clean `034` target until same-side photo selection and direction/subtype issues are resolved.
- `H-983` and `H-353` have genuine source-side mismatches because `C` remains a side category.
- `H-893` and `H-925` remain blocked by object-number forms that the searched general convention does not resolve.

## Consequence For Decipherment

The next linguistic experiment is still blocked. A valid `032/033/034` substitution test needs source-normalized panel nodes:

1. One node per confirmed physical side.
2. Same-side photo variants attached to that node with preservation/quality notes.
3. Unresolved numbered object forms kept separate until catalog notes identify them.
4. Only then test whether `032`, `033`, and `034` alternate in the same stable source frame.

## Claim Status

```text
accepted translations: 0
accepted phonetic values: 0
accepted sign meanings: 0
accepted side functions: 0
accepted FRAME700 subtype readings from these source conventions: 0
```
