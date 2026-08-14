# H-2218 Through H-2239 Fig. 4 Mapping

Date: 2026-05-24

## Purpose

This note ties our local validation sheet for the H-2218 through H-2239 tablets to a published figure: Fig. 4 of Meadow and Kenoyer 2000. It exists because three different numbering systems describe the same 22 objects, and they are easy to confuse:

- local side-order signatures from `lipi`, the project's working transcription corpus — the recorded order of the inscribed sides of each tablet;
- published Fig. 4 item numbers;
- Meadow and Kenoyer's manufacturing groups — their grouping of the tablets by how they were made.

This is source control only — bookkeeping that ties local rows to published object identities. It is not a reading of any sign.

## Local Artifacts

```text
data/open_prototype/tools/lipi_h2218_fig4_mapping.mjs
data/open_prototype/reports/lipi_h2218_h2239_fig4_mapping.csv
data/open_prototype/reports/lipi_h2218_h2239_fig4_mapping_summary.json
```

Input:

```text
data/open_prototype/reports/lipi_h2218_h2239_series_validation_sheet.csv
```

External source:

```text
Meadow and Kenoyer 2000, The 'Tiny Steatite Seals' (Incised Steatite Tablets) of Harappa
https://www.harappa.com/sites/default/files/pdf/Kenoyer2000_The%20Tiny%20Steatite%20Seals%20of%20Harappa.pdf
```

## Source Anchor

Meadow and Kenoyer 2000 presents Fig. 4 as a set of a steatite seal plus incised steatite tablets from Harappa 1995-1997, Mound E, HARP Trench 11.

The figure legend groups tablet numbers:

- Fig. 4 nos. 2-7: manufacturing group 1.
- Fig. 4 nos. 8-16: manufacturing group 2.
- Fig. 4 nos. 17-23: manufacturing group 3.

The article also says that the tablets carry the same set of inscriptions, but the inscriptions do not always occur in the same sequence or orientation when the tablet is flipped. It further argues that the tablets were incised by at least three stone engravers. These are source claims to test against local side-order signatures, not translations.

## Coverage

```text
mapped_fig4_items: 22
expected_fig4_tablet_items: 22
missing_fig4_items: 0
```

## Fig. 4 Mapping

In this table, `CISI` is the object's number in the Corpus of Indus Seals and Inscriptions, and `HARP Object` is its excavation designation from the Harappa Archaeological Research Project. `Local Signature` is the side-order class from the local validation sheet: `A` is the majority side order, `B side swap` means local sides 1 and 2 appear in swapped order, and the `154` and `033` variants are the two tablets whose signature differs by one sign (`154` for `156`, and `033` for `034`).

| Fig. 4 No. | Manufacturing Group | CISI | HARP Object | Local Signature |
| ---: | --- | --- | --- | --- |
| 2 | group 1 | `H-2221` | `H97-3304/8040-01` | B side swap |
| 3 | group 1 | `H-2222` | `H97-3305/8040-02` | A |
| 4 | group 1 | `H-2220` | `H97-3312/8040-05` | A |
| 5 | group 1 | `H-2227` | `H97-3314/8040-07` | B side swap |
| 6 | group 1 | `H-2229` | `H97-3290/8010-03` | A |
| 7 | group 1 | `H-2225` | `H97-3315/8040-08` | A |
| 8 | group 2 | `H-2224` | `H97-3318/8040-12` | A |
| 9 | group 2 | `H-2235` | `H97-3333/8038-01` | B side swap |
| 10 | group 2 | `H-2219` | `H97-3317/8040-11` | A |
| 11 | group 2 | `H-2218` | `H97-3319/8040-13` | A |
| 12 | group 2 | `H-2228` | `H97-3316/8040-09` | B side swap |
| 13 | group 2 | `H-2226` | `H97-3313/8040-06` | B side swap |
| 14 | group 2 | `H-2223` | `H97-3306/8040-03` | A |
| 15 | group 2 | `H-2236` | `H97-3307/8040-04` | A |
| 16 | group 2 | `H-2239` | `H96-3046/6951-04` | A |
| 17 | group 3 | `H-2237` | `H96-3125/6937-16` | `154` variant |
| 18 | group 3 | `H-2238` | `H95-2613/6560-01` | `033` variant |
| 19 | group 3 | `H-2230` | `H97-3311/8040-10` | B side swap |
| 20 | group 3 | `H-2233` | `H97-3341/8039-10` | B side swap |
| 21 | group 3 | `H-2231` | `H97-3320/8040-14` | A |
| 22 | group 3 | `H-2234` | `H97-3322/8040-16` | A |
| 23 | group 3 | `H-2232` | `H97-3321/8040-15` | A |

## Group vs Local Signature

| Manufacturing Group | Artifact Count | Local Signature Counts |
| --- | ---: | --- |
| group 1 | 6 | A: 4; B side swap: 2 |
| group 2 | 9 | A: 6; B side swap: 3 |
| group 3 | 7 | A: 3; B side swap: 2; `154` variant: 1; `033` variant: 1 |

The source manufacturing groups do not collapse to the local side-order signature classes. Every manufacturing group contains a mix of local side-order classes or variants.

That is an important constraint. It blocks the easy story that side-order variation is simply equivalent to Meadow and Kenoyer's manufacturing groups.

## Visual Availability

The public Meadow and Kenoyer 2000 PDF includes a coarse Fig. 4 image and a readable legend. This is enough to map local rows to published figure numbers and manufacturing groups.

It is not enough to accept detailed sign segmentation (splitting an inscription into individual signs), allography (deciding which shapes are variants of the same sign), or side orientation. Detailed validation still needs higher-resolution plates, original CISI plates, or direct image access.

Follow-up visual availability audit:

- [H-2218 through H-2239 Fig. 4 visual availability audit](h2218_h2239_fig4_visual_availability_audit.md) records that the public PDF figure gives coarse three-side panel coverage and triangular/end-profile markers for all 22 mapped tablet items, while still blocking segmentation-grade use.

## Interpretation Boundary

This mapping does not support:

- Physical side function.
- Numerical value.
- Metrological reading.
- Commodity reading.
- Administrative reading.
- Sign meaning.
- Phonetic value.
- Language identity.
- Translation.

## Consequence

The next E3.2 validation step should compare three layers for each object:

1. Local `lipi` side text.
2. Meadow and Kenoyer Fig. 4 visual order.
3. Manufacturing group assignment.

Only after that can the project ask whether the side-order differences are physical orientation, cataloging convention, copying practice, or something else.

Follow-up:

- [H-2218 through H-2239 Fig. 4 visual availability audit](h2218_h2239_fig4_visual_availability_audit.md) records the public-Fig. 4 visual availability boundary for all 22 mapped tablet items.
- [H-2218 through H-2239 dimension side-order probe](h2218_h2239_dimension_side_order_probe.md) adds available object measurements as a fourth control layer. It finds that measurements track manufacturing groups more clearly than local A versus side-swap signatures.
- [H-2218 through H-2239 side-order confound probe](h2218_h2239_side_order_confound_probe.md) checks whether local A/B side order collapses to manufacturing-group distribution or published Fig. 4 sequence order. It does not find a strong manufacturing-group or sequence-order explanation, but still leaves physical side order pending image validation.
- [H-2218 through H-2239 side-role template probe](h2218_h2239_side_role_template_probe.md) records the stricter local template: every row has one `+861-003+` side, one `+700-03x+` side, and one `+15x-003+` side; the `+15x-003+` role is always local side 3.
