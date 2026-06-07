# H-2147 / H95-2514 Public Visual Route

Date: 2026-05-26

## Question

Does the Meadow/Kenoyer 1997 public PDF provide enough visual evidence to upgrade H-2147 from route-only to source-visible, and does that decide the Parpola sign no. 41 / local `110` question?

## Source

Downloaded source:

- `tmp/h2147_source_route/kenoyer_meadow_1997_harappa.pdf`
- SHA256: `4CE604F7ED11D247A6AB88E49DA946D00CDC1B2787B3DD2C58B327C95A7A51D3`

Public URL:

- `https://www.harappa.com/sites/default/files/pdf/Kenoyer1997_Excavations%20at%20Harappa%201994-1995%20New%20Perspective.pdf`

Rendered pages:

- `tmp/h2147_source_route/p-20.png`: printed p. 158, Figure 10.
- `tmp/h2147_source_route/p-21.png`: printed p. 159, Figure 10 continuation table.

Stored crops:

- `tmp/h2147_source_route/h2147_h95_2514_fig10_item17_context_crop.png`
- `tmp/h2147_source_route/h2147_h95_2514_fig10_item17_crop.png`
- `tmp/h2147_source_route/h2147_h95_2514_fig10_17_table_row_full_crop.png`

## Visual And Table Findings

Figure 10 item 17 is visible on printed p. 158. The first rendered crop seemed to show two visible inscription panels for item 17:

- An upper panel with a longer inscription field.
- A lower panel with a central/right anthropomorphic/kneeling-pot-like sign area.

Correction from the later raw-page recrop:

- The lower visible item 17 panel is not a clean single-sign panel.
- It has at least a left vertical/U-like component plus a right branching/figure-like component.
- The visual similarity to H-2148 comes from that right component only.
- Therefore H-2147 is component-level pressure, not a panel-level `110` witness.

See [H-2147 / H-940 `110` recrop recheck](h2147_h940_110_recrop_recheck.md).

The continuation table on printed p. 159 maps:

- Figure item: `10.17`
- Accession: `H95-2514`
- Excavation unit: `4461-04`
- Artifact: tablet, incised, 2 sides
- Material: fired steatite
- Locus: Trench 11, dump

This upgrades H-2147 from route-only to public visual route for the H95-2514 object.

Follow-up accession concordance:

- Meadow/Kenoyer 1997 Figure `10.17` maps to accession `H95-2514`.
- Local Lipi metadata maps `H95-2514Figure 27.14` to H-2147 rows `673.1` and `673.2`.
- A broader Figure 10 / local figure concordance matched all 21 public Figure 10 accessions to local accessions. This makes `10.17` versus `27.14` a figure-system difference, not an object-identity contradiction.
- The rendered table, not OCR, is the basis for `Trench 11`; `pdftotext` misreads several `Trench 11` entries as `Trench II`.

## What It Does Not Decide

This does not identify local `110` as Parpola sign no. 41.

Blocking reasons:

- The accession bridge resolves object identity, but not source-side mapping: `Figure 10.17 -> H95-2514 -> H95-2514Figure 27.14`.
- Local rows are fragmentary: `673.1 ]110+` and `673.2 ]220-415+`.
- The public PDF does not assign local Mahadevan/Lipi row numbers to the two visible panels.
- The public PDF does not give local numeric sign IDs.
- The visible lower panel makes Parpola's sign-no.-41 clue inspectable only at component level, but source-side labels and source sign notes are still missing.

## Decision

H-2147 status is upgraded to:

- `public_visual_route_no_local_mapping`

It is not upgraded to:

- `source_grade_side_mapping`
- `local_110_equals_parpola_41`
- `034/415 crosswalk evidence`
- `sign value`
- `translation`

## Next Gate

Ask Harappa/CISI/HARP source holders to reconcile:

- The source behind local `Figure 27.14`, so the publication figure system can be cited directly.
- Which visible panel is obverse/reverse.
- Which visible panel corresponds to `673.1 ]110+` and `673.2 ]220-415+`.
- Whether the right branching/figure-like component, rather than the whole panel, is the source basis for Parpola sign no. 41.
- Whether the fragmentary signs are complete enough for any crosswalk use.
