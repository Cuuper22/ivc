# size_034: are 034 tablets smaller than 032/033 of the same format?

Question. Re-test the 034 size result that the 2026-07-12 decision closed on a within-series gate (H-2218..H-2239, one 033 object).

Data. 309 Harappa tablets with a short +700-03x+ face and positive horizontal and vertical size (85 / 113 / 111 for 032 / 033 / 034), from frame700_034_size_tier_heldout_20260712_predictions.csv joined to Lipi. Usable dimensions: 379 Lipi tablet objects carry such a face, 328 have positive dimensions, 309 are in the frozen file. Populated in the 309: area-section 255, period 126, phase 217, material 256 (steatite or faience), 132 of 309 are HARP-era (H-1500+).

Method. log(area) = log(h x v). One vote per near-duplicate family (identical longer text on the other face; the H-2218..H-2239 series is one family): 216 families, 228 family x format x group cells (69 for 034, 159 for 032/033). Format = tablet type x sides. Statistic: format-weighted mean difference in cell log area; 20,000 permutations of the 034 label within strata; family-bootstrap CI (5,000). Controls: permutation strata with era / material / area-section, and a cell-level OLS with family-clustered errors.

Result.
| Analysis | Area ratio 034 / other | Evidence |
|---|---|---|
| One vote per object (not family-collapsed) | 0.857 | P<0.0001 |
| Family-collapsed, format strata | 0.861 (0.79-0.93) | P 0.0005 |
| 034 vs 033 only / vs 032 only | 0.874 / 0.841 | P 0.002 / 0.001 |
| Permute within format x era / x era x material | 0.861 | P 0.0025 / 0.0022 |
| Permute within format x area-section / x era x area-section (50 / 53 strata) | 0.861 | P 0.086 / 0.073 |
| OLS +era / +era+material | 0.876 (0.80-0.96) / 0.872 (0.80-0.95) | z -2.96 / -3.11 |
| OLS +area-section (33 parameters) / +phase | 0.904 (0.82-0.997) / 0.904 (0.82-1.001) | z -2.03 / -1.94 |
| HARP era only / old era only | 0.871 (P 0.017) / 0.903 (P 0.066) | same direction |
| Without the H-2218..H-2239 series / two largest families | 0.861 / 0.860 | P 0.0004 / 0.001 |
| Within-family pairs (10 family x format pairs) | 0.877; 034 smaller in 8 of 10 | sign-flip P 0.07 |
Both dimensions shrink by about the same factor (length 0.93, width 0.93).

What it shows. 034 tablets are about 10-14% smaller in area than 032/033 of the same format, with one vote per family, and the series does not carry it. The effect holds after era and material, and shrinks to about 10% (CI touching 1) once area-section fixed effects are added; permutation inside area-section strata loses power (50 strata, P 0.07-0.09) and does not by itself reject or confirm. The July decision's own table already showed the association was real; it closed on discrimination inside one series.
What it does not show. A tier, a unit or a meaning: the difference is a shift in means with wide overlap, area-section may partly track production batch, and none of this rules out a format/series confound the metadata cannot see.
Prior work. No external source checked. Internal: research/docs/archive/frame700_034_size_tier_heldout_decision_20260712.md reports medians 101 / 117 / 147 mm2 for 034 / 033 / 032 and "the size association is real".
