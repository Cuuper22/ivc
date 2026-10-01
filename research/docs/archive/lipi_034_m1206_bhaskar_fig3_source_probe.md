# Lipi 034 M-1206 Bhaskar Fig. 3 Source Probe

Date: 2026-05-25

This note is a probe — a quick, bounded check — of one published figure that appears to show the seal M-1206. It exists because M-1206 is the only object in the local corpus carrying a particular three-sign string, and a lone object cannot be trusted until a real photograph is found. The figure turned out to be a usable lead, and also to contain a contradiction about which object it shows.

Question:

```text
Can the Bhaskar 2022 Fig. 3 public image route move M-1206 from a generic P0 034 acquisition target into a concrete source-validation packet?
```

Input:

- `data/open_prototype/lipi/metadata_filtered.csv`
- `tmp/m1206_bhaskar/Bhaskar2022_IJHS_57_3_1.pdf`
- `tmp/m1206_bhaskar/S1-IndusZoomorphicIconCatalogue.pdf`

Output:

- `data/open_prototype/reports/lipi_034_m1206_bhaskar_fig3_routes.csv`
- `data/open_prototype/reports/lipi_034_m1206_bhaskar_fig3_visual_inputs.csv`
- `data/open_prototype/reports/lipi_034_m1206_bhaskar_fig3_adjudication.csv`
- `data/open_prototype/reports/lipi_034_m1206_bhaskar_fig3_segmentation_scenarios.csv`
- `data/open_prototype/reports/lipi_034_m1206_bhaskar_fig3_summary.json`
- `data/open_prototype/reports/lipi_034_m1206_520_220_terminal_contrasts.csv`
- `data/open_prototype/reports/lipi_034_m1206_520_220_terminal_contrasts_summary.json`

## Local Object

```text
M-1206 / 3556.1 / +520-220-034+
M-1206 / 3556.2 / +740-690-435-255-002-861+
Mohenjo-daro, DKG. (S), excavation DK8186229
Steatite square seal, symbol Gaur, sides=2, direction R/L
Dimensions in local layer: 33 x 30.5 x 7-14 mm
```

## Result

```text
source-route rows: 11
visual input rows: 9
adjudication rows: 6
segmentation scenarios: 5
520-220 terminal contrast rows: 52
sent source requests: 2
accepted decipherment claims: 0
```

Bhaskar 2022 Fig. 3 is a real public image lead. The caption on article page 192 / PDF page 18 identifies the right-hand image as `M-1206` and says the images are from CISI. The local render and crops are stored under `tmp/m1206_bhaskar/derived/`.

That is not enough to accept a source mapping. The same article's running text refers to `M-2016 (Fig. 3)`, while the caption says `M-1206`. This may be a typo, but it is exactly the kind of object-number conflict that kills source-grade confidence until CISI/HARP confirms the identity.

## Visual Lead

Rendered and cropped:

- Full page: `tmp/m1206_bhaskar/page18-18.png`
- Fig. 3 context: `tmp/m1206_bhaskar/derived/m1206_fig3_caption_context.png`
- Right-hand object: `tmp/m1206_bhaskar/derived/m1206_fig3_right_full.png`
- Inscription band: `tmp/m1206_bhaskar/derived/m1206_fig3_inscription_band.png`
- Close sign crop: `tmp/m1206_bhaskar/derived/m1206_fig3_signs_close.png`

The right-hand figure visibly carries a short three-group inscription compatible with local row `3556.1 +520-220-034+`. Compatibility is not validation. The article states that all seal imagery faces as impressed, while local `M-1206` is direction `R/L`; therefore the packet preserves direction/mirroring as an unresolved source gate.

## Source Route

- Article DOI: <https://doi.org/10.1007/s43539-022-00052-2>
- Harappa article page: <https://www.harappa.com/content/indus-zoomorphism-and-its-avatars>
- Harappa PDF route: <https://www.harappa.com/sites/default/files/pdf/Bhaskar2022_IJHS_57_3_1.pdf>
- Storage PDF used for local download: <https://storage.googleapis.com/cahcblr-pdfs/assets/ijhs/57_3_1.pdf>
- Supplementary S1 PDF: <https://storage.googleapis.com/cahcblr-pdfs/assets/ijhs/S1-IndusZoomorphicIconCatalogue.pdf>
- Springer S1 XLSX: <https://static-content.springer.com/esm/art%3A10.1007%2Fs43539-022-00052-2/MediaObjects/43539_2022_52_MOESM1_ESM.xlsx>

S1 extraction finds `M-1206` with a text-present marker, `P8`, `F0`, and `Bison`. This is iconographic catalogue evidence only. It is not a sign transcription and cannot license a reading of `034`.

## Terminal Contrast

The targeted local contrast set is now stored in `data/open_prototype/reports/lipi_034_m1206_520_220_terminal_contrasts.csv`.

```text
rows with prefix 520-220: 52
unique terminals after 520-220: 16
terminal 415 rows: 28
terminal 034 rows: 1
```

That means M-1206 is a singleton `520-220-034` terminal-slot target in the filtered local planning layer. This is useful because it tests `034` outside the `700-034` FRAME700 branch — the separate line of investigation into the project's `700-03x` sign frame. It is also dangerous: singleton status makes source-image confirmation mandatory, since one bad segmentation can create the entire signal.

## Adjudication

Adjudication is the ruling on what the evidence above is allowed to support. To quarantine a point is to set it aside as unusable until a named blocker clears.

Accepted:

- Public image route exists.
- Caption-level object binding exists.
- One visible face has a three-group inscription compatible with the length-3 local row.
- The S1 catalogue independently places `M-1206` in the Bhaskar zoomorphic dataset.
- The local `520-220-X` contrast set makes `034` a singleton terminal after `520-220`, with `415` as the dominant comparator terminal.

Rejected or quarantined:

- No source-grade object binding because caption `M-1206` conflicts with running-text `M-2016`.
- No source-grade side binding because the figure does not show the six-sign companion row.
- No source-grade sign segmentation because the PDF figure is a secondary CISI-derived image.
- No sign value, function, meaning, phonetic reading, or translation.

## Next Gate

Request or inspect CISI/HARP all-side source for:

```text
M-1206 / DK8186229 / CISI object image and record
all visible sides
side labels and side order
seal versus impression orientation
direction basis for R/L
source transcription for 3556.1 +520-220-034+
source transcription for 3556.2 +740-690-435-255-002-861+
object-number reconciliation for caption M-1206 versus running-text M-2016
```

If the source confirms that Fig. 3 right-hand object is M-1206 and that the visible face is row `3556.1`, the next live test is whether `034` is the terminal V/triangle-like sign under the documented orientation convention. If the source says the right-hand object is M-2016, or the side/row link fails, this entire M-1206 route gets downgraded to a false or ambiguous public lead.

## Sent Requests

```text
gmail:[redacted-msgid]
Sent to [harappa-project-email] for source-grade all-side images, CISI/HARP references, side labels/order, orientation basis, M-1206 versus M-2016 clarification, and permission/citation terms.

gmail:[redacted-msgid]
Sent to [bhaskar-email] asking whether Fig. 3 right-hand object is M-1206 or M-2016 and whether the visible inscription corresponds to +520-220-034+ or another source/caption convention.
```

## Follow-Up Author Reply

On 2026-05-26, Bhaskar replied in Gmail message `[redacted-msgid]`:

```text
Typo. The figure caption is correct. M-1206. The supplementary catalogue to my article can verify this.
```

This resolves the article-internal object-number conflict:

```text
running-text M-2016 = typo
Fig. 3 caption M-1206 = author-confirmed
```

The Bhaskar Fig. 3 route is now a stronger secondary public image lead for M-1206. It still does not provide source-grade side binding, source transcription, orientation/mirroring convention, `034` source mapping, value, or translation. The direct CISI Pakistan `n181` M-1206 source page remains the primary source-visible evidence.
