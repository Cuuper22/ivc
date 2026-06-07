# H-2147 Figure 10 / Figure 27 Accession Concordance

Date: 2026-05-26

## Question

Does the local hook `H95-2514Figure 27.14` contradict Meadow/Kenoyer 1997 Figure `10.17`, or are they two figure systems pointing to the same excavated object?

## Sources

- Meadow/Kenoyer 1997 public PDF: `tmp/h2147_source_route/kenoyer_meadow_1997_harappa.pdf`
- Rendered evidence pages: `tmp/h2147_source_route/p-20.png` and `tmp/h2147_source_route/p-21.png`
- Local Lipi metadata: `data/open_prototype/lipi/metadata_filtered.csv`
- Concordance table: `data/open_prototype/reports/h2147_fig10_fig27_accession_concordance.csv`
- Summary JSON: `data/open_prototype/reports/h2147_fig10_fig27_accession_concordance_summary.json`

## Method

The comparison is by excavation/accession ID, not by figure number.

Meadow/Kenoyer Figure 10 lists incised steatite tablets by public figure item and accession. Local Lipi metadata stores the same accessions in the `excavation-idno` field, usually with a different figure label appended.

One public-table row needed manual rendered-page correction:

- `10.14` is visually `H95-2417`; `pdftotext` read it as `H95-241 T`.

The same OCR problem affects the locus column:

- `pdftotext` often renders `Trench 11` as `Trench II`.
- The rendered page shows `Trench 11` for `10.17 / H95-2514`.

## Result

All 21 public Figure 10 accessions have local accession matches.

The H-2147 bridge is:

| Public source | Public accession | Local object | Local hook | Local rows |
| --- | --- | --- | --- | --- |
| Meadow/Kenoyer 1997 Figure `10.17` | `H95-2514` | `H-2147` | `H95-2514Figure 27.14` | `673.1 ]110+`; `673.2 ]220-415+` |

So the figure-number mismatch is no longer an object-identity blocker. It is a publication or figure-system difference: Meadow/Kenoyer 1997 uses Figure 10, while local Lipi metadata points to a Figure 27 series for many of the same H94/H95 incised tablet accessions.

## Decision

Accepted:

- H-2147 has an object-level public visual route.
- `Figure 10.17 -> H95-2514 -> local H-2147 / H95-2514Figure 27.14` is a valid accession bridge.

Still rejected:

- Mapping the visible upper/lower panels to `673.1` and `673.2`.
- Equating local `110` with Parpola sign no. 41.
- Treating `]220-415+` as source-side verified in the public image.
- Any `034/415` crosswalk, sign value, or translation.

## Next Gate

Find the source behind local `Figure 27.14`, or obtain Harappa/CISI/HARP side labels for H95-2514, so the visible panels can be tied to local rows `673.1` and `673.2`.
