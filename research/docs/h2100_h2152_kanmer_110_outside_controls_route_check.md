# H-2100 / H-2152 / Kanmer `110` Outside Controls Route Check

Date: 2026-05-26

## Question

After correcting local `110` scope from three rows to six rows, can the outside controls H-2100, H-2152, and Kanmer `4881.1` be source-routed enough to compare with the H-940/H-2147/H-2148 Parpola sign-no.-41 branch?

## Result

No. They remain outside controls, but none is source-panel usable yet.

| Object | Local row | Local route hook | Checked route result | Status |
| --- | --- | --- | --- | --- |
| H-2100 | `817.2 +110[` | `H96-3179Figure 19.21` | No exact public route found in checked local/web/PDF layer | `route_dark_outside_control` |
| H-2152 | `865.1 +110[` | `H97-3327Figure 15.19` | No exact public route found in checked local/web/PDF layer | `route_dark_outside_control` |
| Kanmer `4881.1` | `+110[` | `RIHN-Indus project08- 1285` | Refined RIHN 2012 Kanmer source-holder route only; no exact public object panel | `bibliographic_route_no_object_panel` |

## Checked Sources

Local:

- `data/open_prototype/lipi/metadata_filtered.csv`
- Existing source-route docs and reports under `docs/` and `data/open_prototype/reports/`
- Existing `tmp/` source folders

Public web / downloaded PDFs:

- Kenoyer and Meadow 2010, "Inscribed Objects from Harappa Excavations 1986-2007"
  - Local PDF: `tmp/h2148_h2100_h2152_110_route/kenoyer_meadow_2010_inscribed_objects_harappa.pdf`
  - SHA256: `7a8fea92fbc7a8810ad9d47e5740a83e4896bc46facd1ec6eb7f51c329ecf2d9`
  - Exact text search did not find `H96-3179`, `H97-3327`, `3179`, or `3327`.
- Kenoyer 2000, "The Tiny Steatite Seals of Harappa"
  - Local PDF: `tmp/h2148_h2100_h2152_110_route/kenoyer2000_tiny_steatite_seals_harappa.pdf`
  - SHA256: `967ebcb058e5611de4089facba852adac418108adfc36bf793d0588ba0d8b751`
  - Text search finds nearby H97 tablet/table rows such as `H97-3343`, `H97-3346`, `H97-3352`, `H97-3301`, and others, but not `H97-3327`; it also does not find `H96-3179`.
- Exact web searches for `H96-3179`, `H97-3327`, `H2001-5142`, and `RIHN-Indus project08- 1285`.
- Kanmer bibliographic/source-holder route:
  - The better source-holder lead for local hook `RIHN-Indus project08- 1285` is the RIHN 2012 volume *Excavation at Kanmer : 2005-06--2008-09 : Kanmer Archaeological Research Project: an Indo-Japanese Collaboration*, edited by J. S. Kharakwal, Y. S. Rawat, and Toshiki Osada. CiNii records the publisher as the Indus Project, Research Institute for Humanity and Nature, Kyoto, with ISBN `9784902325720`: https://cir.nii.ac.jp/crid/1970304959869740544
  - Cambridge/Radiocarbon context confirms Kanmer was excavated over four seasons and lists Toshiki Osada at the Research Institute for Humanity and Nature: https://www.cambridge.org/core/journals/radiocarbon/article/subsistence-system-paleoecology-and-14c-chronology-at-kanmer-a-harappan-site-in-gujarat-india/79400E9EB8D5B8FEBA7E2B88E4F33E56
  - A public RIHN 2007 Indus Project report was downloaded and text-searched. It contains Kanmer/project context and pendant rows, but no exact `1285`, `08-1285`, or `project08-1285` object route:

```text
tmp/h2148_h2100_h2152_110_route/rihn_2007_indus_houkokusyo.pdf
sha256: b887ae54ebda5a0ffa39c3065c9845b61a9a576c50053b36a201a90c73448433
source: http://archives-contents.chikyu.ac.jp/1070/2007IndusHoukokusyo.pdf
```

  - This improves the source-holder route for the `project08` prefix, but no exact `RIHN-Indus project08- 1285` public object panel or table row was found in the checked public layer.

## Interpretation

These controls block a lazy `local 110 = Parpola sign no. 41` population claim, but they do not yet supply visual evidence against the branch.

Current state:

- H-940/H-2147/H-2148 remain the active Parpola sign-no.-41 branch.
- H-2148 is now source-visible and count-mapped through Kenoyer 2005 Figure 14.1.
- H-2100 and H-2152 are Harappa tablet controls with fragmentary `110` rows, but remain route-dark.
- Kanmer `4881.1` is a different site/material/type control and remains source-holder gated through the RIHN 2012 Kanmer volume route.

## Decision

Accepted:

- H-2100, H-2152, and Kanmer `4881.1` are mandatory outside controls for any local `110` crosswalk.
- No checked public source panel currently upgrades those outside controls.
- H-2152 is especially important because its companion row is `]220-415+`, close to the H-2147/H-2148 branch structure.

Rejected:

- Treating H-2100/H-2152/Kanmer as evidence for or against Parpola sign no. 41 before source images.
- Any population-level `110` identity claim.
- Any phonetic value, sign meaning, language identity, or translation.

## Next Gate

1. Search or request HARP/CISI source panels for `H96-3179Figure 19.21` and `H97-3327Figure 15.19`.
2. Inspect the RIHN 2012 *Excavation at Kanmer: 2005-06--2008-09* volume or archive table behind `RIHN-Indus project08- 1285`.
3. Once source panels exist, blind-compare outside-control `110` forms against H-940 B, H-2147's right candidate component or source-mapped panel, and H-2148's single-sign panel.
