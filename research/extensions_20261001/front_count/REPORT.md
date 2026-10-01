# front_count: does the front predict the cup + N-stroke count?

Question. On two-sided miniature tablets with cup + 2/3/4 long strokes on one face, does the text on the other face (front) predict the count?

Data. (a) Mahadevan 1977 paired objects, 85 tablets, 39 fronts (research/data/mahadevan_20260905/paired_objects.json). (b) Lipi metadata_filtered.csv: two-row TAB objects, exactly one face +700-03x+ or +03x-700+, 032/033/034 = 2/3/4 strokes. Code check: H-306 = Mahadevan 5474 (same excavation number), Lipi cup face +700-033+ matches cup + 3 strokes, other face 032 matches 2 strokes. Strict: both faces complete=Y, front has no 000 and no brackets, preservation not fragment/partly damaged: 285 objects (80/118/87 for 2/3/4; 282 Harappa), 190 fronts; cup+strokes on both faces dropped.

Method. Fronts with >1 distinct count; lookup hits (sum of modal frequency); leave-one-out hits; mutual information; chi-square. 20,000 permutations of counts, fixed seeds: unrestricted, within locus (Mahadevan), within site / era / area-section (Lipi). Cross-batch test: predict from same-front objects in a different locus / area-section, counts permuted within group.

Held-out split rule (written before the held-out score was computed). Harappa only. Fit set = CISI H-1..H-1499 (old Vats/Wheeler-era registers; objects that existed before Mahadevan 1977). Held-out = H-1500+ or excavation id H<yy>-... (HARP 1986-2007; Lipi's excavation-id format changes near H-1522; all postdate 1977). Realised gap: last fit object H-1347, first held-out H-1768. Lookup fitted on the fit set only (ties by fit-set frequency, unseen fronts -> fit-set mode 3), scored against the majority baseline and 20,000 shuffles. Limit: fit set is a Lipi-side proxy for "in Mahadevan"; a direct Mahadevan-fit test needs a Mahadevan-Lipi crosswalk the repo lacks.

Result.
| Test | Observed | Null mean | P |
|---|---|---|---|
| (a) 85 objects, unrestricted: fronts varying | 8 | 11.0 | 0.024 |
| lookup hits / MI bits / chi-square | 63 / 0.859 / 92.9 | 59.2 / 0.732 / 76.9 | 0.076 / 0.016 / 0.011 |
| leave-one-out hits | 36 | 32.5 | 0.32 |
| (a) within locus (12 strata): varying / lookup / MI / chi-square | 8 / 63 / 0.859 / 92.9 | 10.9 / 59.6 / 0.743 / 78.5 | 0.032 / 0.10 / 0.026 / 0.020 |
| (a) locus 42 only (38 obj, 16 fronts): varying / lookup / MI | 3 / 26 / 0.619 | 3.6 / 25.6 / 0.639 | 0.37 / 0.50 / 0.58 |
| (a) not locus 42 (47 obj): MI / chi-square | 1.280 / 75.8 | 1.110 / 65.0 | 0.031 / 0.031 |
| (a) without the 21-object family: MI / LOO | 1.102 / 36 | 0.978 / 25.3 | 0.051 / 0.010 |
| (a) cross-locus prediction, 55 eligible objects | 27 hits | 21.1 | 0.13 |
| (b) Lipi 285, within era x area-section (33 strata): varying / lookup / LOO / MI | 23 / 250 / 141 / 1.242 | 32.8 / 231.8 / 112.5 / 1.092 | 0.0007 / <0.0001 / 0.0002 / <0.0001 |
| (b) cross area-section, 118 eligible | 64 hits (global mode 52) | 43.5 | 0.004 |
| (b) without the 28-object family: lookup / cross-area | 233 / 47 of 90 | 217.7 / 32.0 | 0.0001 / 0.012 |
| (c) held-out, 115 objects (29/35/51), 27 with a front seen in fit | lookup 37 hits | 36.3 | 0.47 (within area 0.78, shuffled train 0.20) |
| (c) majority baseline (always 3) | 35 hits | | |
| (c) on the 27 covered objects | lookup 13, majority 11 | | |

What it shows. Mahadevan: same-front tablets differ in count less than chance (P 0.024; 0.032 within locus), but lookup accuracy is borderline and leave-one-out is null; inside locus 42 alone everything is null, with low power. Lipi: same-front tablets share a count far above chance, within site, era and area-section, without the largest family, and across area-sections. Held-out: the lookup fitted on the older tablets does not beat the majority baseline on HARP-era tablets; only 27 of 115 held-out fronts occur in the fit set, so a modest effect could be missed. Lipi-old overlaps Mahadevan's objects, so (a) and (b) are not independent replications.
What it does not show. Any meaning. Repeated fronts are mostly a few copied formulas; area-section is a coarse proxy for a production batch. The pattern is consistent with batches made together, not with a portable front-to-count rule.
Prior work. research/docs/mahadevan_crossface_constraints_20260905.md (refs 5-6) credits Priyanka 2003 and Mukhopadhyay 2023 sec. 5.8 with observing one obverse with 2-, 3- and 4-stroke reverses (the variation). Whether either reported an association or prediction test: not checked, source not held (repo has only the Nature URL in evidence/tmp/041_source_acquisition_20260611/sources_manifest.csv and no Priyanka text).
