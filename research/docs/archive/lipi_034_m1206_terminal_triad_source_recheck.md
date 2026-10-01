# Lipi 034 M-1206 Terminal Triad Source Recheck

Date: 2026-05-25

## Question

This note records a hunt for source images. The terminal triad is a set of three seals that share the same two-sign prefix in our local transcription rows and differ only in the terminal — the final sign. The numbers (`520`, `220`, `003`, `034`, `415`) are local numeric sign labels: transcription codes, not readings.

The question: can the `M-1912 / M-1206 / M-37` terminal triad move from local-row target to source-visible evidence? A local row is an entry in our local transcription table. Source-visible means the object itself can be seen and labelled on a public source page, not just cited.

Local triad under pressure:

```text
M-1912  +520-220-003+
M-1206  +520-220-034+
M-37    +520-220-415+
```

All three local rows are Mohenjo-daro `SEAL:S`, steatite, square, class `MT`, three-sign, `R/L`, with fixed prefix `520-220`.

## Source Retrieval

### M-37

The missing M-37 source image gate — the checkpoint that was blocked for lack of a source image — is now closed at page level. CISI is the Corpus of Indus Seals and Inscriptions, the standard photographic corpus.

- CISI Vol. 1, Collections in India, IA leaf `n54`, printed p. 19.
- Header: `'unicorn' III / SEALS / MOHENJO-DARO 35-37`.
- XML object: `India_0054.djvu`.
- OCR label hits:
  - `M-37 A` at `750,3264,831,3236,3264` plus `A` at `845,3264,872,3238,3264`.
  - `M-37 a` at `1826,3264,1911,3235,3264` plus `a` at `1923,3264,1940,3245,3264`.
- Downloaded raster: `tmp/m1206_terminal_triad_source_recheck/cisi_india_n54_w2000.jpg`.

This also explains the icon-label conflict. CISI and Mayig/Bhaskar-style metadata point to unicorn, while local `lipi` says `Bull1:S`. The local icon class is not allowed to carry interpretation.

### M-1206

The M-1206 source gate is now substantially upgraded beyond Bhaskar Fig. 3.

- CISI Vol. 2, Collections in Pakistan, IA leaf `n181`, printed p. 147.
- Header: `SEALS / MOHENJO-DARO 1206`.
- XML object: `Pakistan_0181.djvu`.
- Downloaded raster: `tmp/m1206_terminal_triad_source_recheck/cisi_pakistan_n181_w2000.jpg`.
- The plate visibly labels multiple views of the same object, including `M-1206 A+E`, `M-1206 A`, `M-1206 a`, `M-1206 E`, `M-1206 e(1)`, `M-1206 B`, `M-1206 C`, `M-1206 D`, and `M-1206 F`.

This removes the previous "companion side not visible" blocker. The six-sign companion row in local `3556.2 +740-690-435-255-002-861+` is source-relevant because the CISI plate shows a long side inscription labelled `M-1206 e(1)` on the same object.

The data page also lands:

- CISI Vol. 2 IA leaf `n472`, printed p. 438, `DATA M-1120 to M-1277`.
- XML object: `Pakistan_0472.djvu`.
- OCR locator rows:
  - `M 1206 2224 DK tl<6 NMP 50.253`
  - `M 1206 1314`
- Visual row crop: `tmp/m1206_terminal_triad_source_recheck/derived/m1206_data_rows_xmlcoords.png`.

The OCR mangles `DK 8186` in the first row, so the data row is used as an object/source locator, not as a clean transcription.

### M-1912

No equivalent raw CISI 1/2 source page was found in the current public CISI 1/2 layer. M-1912 remains supported only by:

- Local row `M-1912 +520-220-003+`.
- Bhaskar S1 iconographic catalogue row marker.
- RMRL June 2025 bulletin drawing/page already stored at `tmp/m1206_bhaskar/bulletin_page15-15.png`.

M-1912 is still a comparator target, not a source-grade terminal witness. (A witness is an object whose inscription independently attests the sequence; source-grade means backed by a primary source image, not a secondary drawing or citation.)

## Visual Adjudication

What changed:

- `M-37` is no longer "overlap only"; it is page-visible in CISI Vol. 1.
- `M-1206` is no longer dependent on the Bhaskar Fig. 3 caption; it is directly page-visible in CISI Vol. 2.
- The M-1206 all-side blocker is removed because CISI shows the `e(1)` side inscription on the same object.
- The Bhaskar `M-1206` versus running-text `M-2016` conflict remains a conflict about that article's Fig. 3 wording, not a blocker against the CISI M-1206 source route.

What did not change:

- `034` still has no clean Mayig/Parpola overlap row (Mayig and Parpola are external catalogues with their own sign numbering; an overlap row would tie our local `034` to their codes).
- No numeric sign value is accepted.
- No `003/034/415` semantic contrast is accepted.
- No animal/species value is accepted.
- No phonetic value or translation is accepted.

## Terminal Slot Result

Current status:

```text
source_visible_two_of_three_terminal_triad
```

M-37 and M-1206 now have public CISI page witnesses. M-1912 remains secondary/CISI 3.1-gated.

The next real experiment is narrow:

1. Blind-label the outer signs in the source crops without using the local numeric codes.
2. Resolve whether the visible `A/a` and seal/impression directions align with local `R/L`.
3. Only then test whether `520-220-X` is visually a shared prefix with a substituted terminal.

The source images make the triad more serious, but they also raise a live warning: naive photo-order comparison can be fooled by mirror direction and side labels. The prefix must be visually aligned before the terminal contrast is allowed to mean anything.

