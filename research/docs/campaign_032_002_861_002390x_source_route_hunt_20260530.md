# 032-002-861 / 002-390-X Source Route Hunt

Date: 2026-05-30

## Question

Can the missing matched alternatives be moved from source-dark into usable source evidence?

Targets:

- `H-1993`: `004 -> 002-390 -> 095`
- `M-1825`: `031 -> 002-390 -> 705`
- Dholavira `4237.1`: `388 -> 002-390 -> 705`

## Results

### H-1993

Local metadata gives:

- `H-1993`, row `744.2`
- Harappa, FTrench 37
- excavation/source pointer `H96-2769 Figure 17.07`
- text `+740-000-220-004-002-390-095+`

Web route found: a public supplementary PDF route that contains the H-1993 / ICIT 744 lead and exact sign row. This is useful, but it is not an artifact image. It upgrades H-1993 from blind search to a concrete figure target: `H96-2769 Figure 17.07`.

Public URL checked: `https://www.harappa.com/sites/default/files/pdf/43539_2023_102_MOESM2_ESM.pdf`

Extra check on 2026-05-30: the same public supplement explicitly places `ICIT 744 (H-1993)` in the relevant sign-string neighborhood. That is prior-work transcription pressure, not source-image evidence. A shell download attempt for the PDF returned `403 Forbidden`, so the usable local state is still the web-view route plus the local Lipi row.

Decision: H-1993 remains unusable for strict source-normalized 095 until the actual Figure 17.07 image is obtained.

### M-1825

Local metadata gives:

- `M-1825`, row `3992.1`
- Mohenjo-daro
- source pointer `BJ25710`
- text `+157-031-002-390-705+`

Local secondary route found:

- `C:\Users\Acer\OneDrive\Documents\ivc\tmp\m1206_bhaskar\S1-IndusZoomorphicIconCatalogue.txt`
- line 1804 lists `M-1825` as an F2 unicorn object.

This confirms object/icon-class existence in the secondary catalogue, not the inscription or sign band.

Decision: M-1825 remains source-dark for `705` branch inference.

### Dholavira 4237.1

Local metadata gives:

- row `4237.1`
- Dholavira, Lower Town, `ZA-12:2`
- Period `3C-2`
- text `+151-032-388-002-390-705+`

Downloaded source:

- `C:\Users\Acer\OneDrive\Documents\ivc\tmp\source_route_hunt_20260530\Dholavira-Bisht2015.pdf`
- Source URL: `https://www.ancientportsantiques.com/wp-content/uploads/Documents/PLACES/IndOc-Gulf/Dholavira-Bisht2015.pdf`
- rendered page: `C:\Users\Acer\OneDrive\Documents\ivc\tmp\source_route_hunt_20260530\dholavira_pages\page-018.png`
- whole candidate crop: `C:\Users\Acer\OneDrive\Documents\ivc\tmp\source_route_hunt_20260530\dholavira_page18_item10_whole.png`
- sign-band candidate crop: `C:\Users\Acer\OneDrive\Documents\ivc\tmp\source_route_hunt_20260530\dholavira_page18_item10_signband.png`

Bisht page 18 item 10 visually matches the reverse source order expected from local `+151-032-388-002-390-705+`: a terminal complex at the left, tree-like `390`, short-stroke `002`, crossed/branch sign, short-stroke sign, and final/start sign at the right under R/L policy.

Additional public OCR route:

- `https://pdfcoffee.com/excavations-at-dholavifra-1989-2005-rs-bisht-2015-pdf-free.html`
- The OCR around the seal catalogue table exposes the `ZA-12:2` locus and the exact dimension cluster `27.62 x (ext) 21.31 x 7.11 - 11.17 ext`, matching local Lipi `4237.1`.

Decision: Dholavira `4237.1` is upgraded to `source_image_candidate_unbound_metadata_cluster_found`, not strict evidence. The visual match is alive and the metadata route is stronger, but page 18 item 10 is still not explicitly bound to Lipi row `4237.1` or the matching dimensions by a report table/plate index.

### Dholavira ICIT 4348 guard

The public Singh et al. supplement also mentions `ICIT 4348 (Dholavira)` near H-1993, but local Lipi metadata shows `4348.1` is not the same object as `4237.1`:

- `4348.1`: Dholavira, clay `TAG`, poor fragment, text `]740-142-000-002-861-390[`
- `4237.1`: Dholavira Lower Town `ZA-12:2`, white square seal fragment, text `+151-032-388-002-390-705+`

Decision: `ICIT 4348` is a negative guard, not evidence for `4237.1`. Do not let the prior-work Dholavira mention bind the Bisht page 18 item 10 candidate.

## Campaign Consequence

The missing `705` branch is no longer just a cold metadata row. It now has one plausible visual route candidate from Dholavira. That matters linguistically because `705` is the repeated non-`125` terminal branch that can decide whether `125` is special or just one branch among several.

But the rule stays hard: no strict source-normalized `705` until either Dholavira page 18 item 10 is explicitly bound to `ZA-12:2` / row `4237.1` / dimensions `27.62 x 21.31 x 7.11-11.17`, or M-1825 is source-imaged.

Current status:

- `125`: live positionally, visually weakened by blind reads.
- `095`: one strict visible control (`M-71`) plus H-1993 route lead, but H-1993 still source-image-dark.
- `692`: one strict visible control (`M-70`).
- `705`: repeated in metadata, one Dholavira source-image candidate, zero strict bound source-image witnesses.

No value, phonetic reading, sign meaning, language identity, function, or translation is accepted.
