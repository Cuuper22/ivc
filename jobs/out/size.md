# Size: reading rank out of seal size

Word-free job, 2026-11-17. Sign numbers, pictures, jobs, sizes and findspots only. Scripts (run in order; each carries its predictions in its top docstring, written before its numbers): `work_scripts/size_common.py` (loader and models), `size_1_models.py`, `size_2_ladder.py`, `size_3_titles.py`, `size_3b_redesign.py`, `size_4_crests.py`, `size_5_marks.py`, `size_6_gaps.py`, `size_7_tablets.py`, `size_8_decide.py`. Tables and logs: `work_data/size/` (`models.csv`, `ladder_all.csv`, `ladder_top25.csv`, `ladder_heldout.csv`, `ladder_by_job.csv`, `titles_ladder.csv`, `titles_stability.csv`, `titles_stacks.csv`, `crests.csv`, `marks.csv`, `marks_twin_pairs.csv`, `gaps.csv`, `gaps_items.csv`, `gaps_restorations_changed.csv`, `tablets.csv`, `tablets_tests.csv`, `decide_splits.csv`, `log_1.txt` to `log_8.txt`).

## Plain words

- **Seal**: a carved stamp of the first catalogue (Lipi). **Face area**: catalogue width x height in mm2. **Size** below always means the natural log of face area: a difference of 0.10 is about 10% bigger. **Complete text**: no lost sign, no break flag. 1,418 complete seal faces carry a size.
- **Length**: number of signs. **Site**: Mohenjo-daro (MD), Harappa (HP), Dholavira, Lothal, Chanhu-daro, Kalibangan, other. **Format**: square beast seal, rectangular inscription-only bar, round, cylinder, other.
- **Baseline**: length + site + format. Every claim must beat it.
- **Halves**: seals split in two by TEXT (identical texts always in the same half), trained on one, scored on the other. 20 further random splits give the spread.
- **Held-out share**: the share of size variation a model explains on seals it never saw (1 = all, 0 = none).
- **Ridge weight / size weight of a sign**: how much bigger a seal is when its text carries that sign, after length, site, format and all the other signs are taken out; weights are pulled toward 0 by a penalty chosen inside the training data. +0.10 = about 10% bigger. **90% interval**: from 400 refits on texts resampled with replacement.
- **Residual size**: size minus what the baseline predicts for a seal of that site, length and format.
- **Decoys**: (i) every sign in every text swapped for a random sign of the same frequency band (each seal keeps its length and its mix of common and rare signs, loses which signs it has); (ii) the frame-v2 job labels dealt to wrong signs of the same frequency; (iii) each fixed phrase replaced by a random run of the same length and similar frequency; (iv) sizes shuffled among seals of the same site, length and format.
- **Jobs** are the frame-v2 classes (`jobs/out/frame_v2.md`): front word, after-front slot, name front (crest), name part, numbers, counted thing, closer (jar 740, spear 520, porters 151-158), after-jar title (comb 400, man 090, 527, 621, 679, 565, 161, 241).
- **Stand letter**: the catalogue letter for the stand drawn before the unicorn (W, J, S, I, L).

## What was found

1. **The text carries a real, small share of a seal's size, and it is in the signs themselves.** Held-out share of size variation: length alone 0.129, baseline 0.294, baseline + one weight per sign 0.309 (seed-0 split). Over 20 splits the per-sign model beats the baseline 20 of 20 times, by +0.018 on average. Decoys: signs swapped within frequency band give 0.292 on average, best 0.295 (0 of 20 reach 0.309); sizes shuffled within site, length and format give an extra of -0.000 (best +0.002) against the real +0.015. On seals whose text the second catalogue never had (102 faces, a fresh set): baseline 0.130, per-sign 0.147. Means: once length, city and format are fixed, which signs a text holds still moves the stone's size, and the decoys show it is sign identity, not frequency. Opens: a ranked list of size signs (below).

2. **The comb ending marks a small-seal holder, in every city.** Comb 400 has the most negative weight of any sign: -0.185 (90% interval -0.247 to -0.114), seals 17% smaller with everything else fixed. Seals reading `[...] jar comb` (740-400) sit at residual size -0.653: about half the face of other jar-final seals of the same site, length and format (11 seals, jar-final mean -0.004, n 515). Comb seals are small at Mohenjo-daro (-0.193, 45 seals), Harappa (-0.485, 14), Chanhu-daro (-0.671, 1) and Kalibangan (-1.169, 1). A comb-final seal is smaller than a jar-final seal in 64.7% of pairs. Means: the after-jar comb is a lower holder class than the plain jar, and the stone is cut to it. It fits the guess in `MAP.md` that comb in the closing place is a junior or a craft hand, now with a measurement that never used a word. Opens: comb = the first measured rung of a rank ladder; it also matches the comb ending on ivory rods and Harappa tablets (`740-400`, `jobs/out/phrases.md`), small personal objects.

3. **The small end of the sign ladder replicates on unseen seals; the big end leans the right way.** Weights fitted on half A, checked on half B: seals carrying one of the 25 smallest signs sit above the median of their own site, length and format only 71 of 191 times (37.2%, one-sided P 0.00024); seals carrying one of the 25 biggest sit above it 68 of 124 (54.8%, P 0.16). 21 signs are above zero and 22 below with intervals clear of zero (198 signs in 4+ seals). Big-end signs: `706` (U with stroke variant, the measure line `706-033-520`) +26%, front word `692` (outlined X) +14%, barred box `595` +14%, jar variant `745`, the slot signs `368` and `742`, crest `231`, title `679` +8%. Small-end signs: comb `400`, box `590` -13%, cup `700` -12%, `495`, the place sign `061` -10%, `350`, porter `156` -9%, the office slot `741` -8% (the `920-060-741` heading), title `527` -7%, tall one `031`.

4. **Name fronts (crests) go big, goods signs go small.** Mean weight by job against 2,000 deals of job labels over the ranked signs: crests +0.025 (P 0.029 for that high), closers -0.035 (P 0.042 for that low), counted things -0.030 (P 0.050). Crest houses differ in size beyond chance: between-house spread 20.67 against 12.88 with house labels dealt within site (max 22.23, P 0.0015). The smallest houses are the goods and count signs as name fronts (cup 700 -0.507, tree 407 -0.380, open rectangle 440 -0.271, box 590 -0.231, `061` -0.227); the biggest are personal signs (garlic 371 +0.466, `706` +0.438, bracket with arc 921 +0.413, `632`, `745`). Means: a seal whose name begins with a goods sign (box, cup, tree) is a store or goods seal and is cut small; a seal whose name begins with a personal emblem is cut large.

5. **The stone's own marks carry five times what the text carries.** Held-out share over 20 splits: length 0.109, + site and format 0.285, + time bin 0.283, + signs 0.301, + stand letter, animal and material 0.400. Stone marks alone (no text) reach 0.387. Stand letter with the text taken out: W +0.248 (320 seals), J -0.007, S -0.082, L -0.147, I -0.234 (spread 23.3 against 0.77 dealt within site and format, P below 1 in 2,000). W stones are 28% bigger and I stones 21% smaller than their text predicts. Animal on square seals: zebu +0.302 (36), rhinoceros +0.120, unicorn +0.022, elephant +0.019, short-horned bull -0.149 (61), goat -0.260, inscription-only -0.386 (P below 1 in 2,000). Material: terracotta +0.453, clay +0.326, steatite +0.008, faience -0.323 (P 0.0005). With the text held fixed exactly (65 twin sets, 170 stones): a beast stone is bigger than its inscription-only twin in 27 of 39 pairs (x1.52); the zebu twins +0.394; but W stones are not bigger than their twins with other stands (6 of 16 pairs, mean gap +0.056, spread P 0.64). Means: size is set first by what kind of stone it is (beast, which beast, which material) and by the city workshop's style (stand letter); the text adds a smaller rank component on top. The stand letter differs across texts, not within one text: the workshops that draw W cut big seals for big-seal texts.

6. **Tablets are sized by their name, not by their count.** 777 clean tablets and tags with a size. With the name (every sign but the numbers) held fixed, size does not move with the count: Spearman +0.005 over 81 objects in 19 names (slope 0.0% per unit, spread P 0.82); moulded +7.8% per unit (14 objects, P 0.47), incised -0.1%, copper +4.1%. With the count held fixed, the name decides size: 79% of within-count size spread lies between names against 32% dealt (P below 1 in 2,000); incised tablets, which are not moulded, 47% against 19% (P below 1 in 2,000); copper tablets 83% against 21%. Moulded batches (38 batches, 109 tablets): within-batch variance 0.011 against 0.320 between batches. Means: a tablet's size belongs to the name it carries, exactly as a seal's size belongs to its text; the earlier "8% smaller per extra stroke" is between names (different names take different counts), not a count effect.

7. **What size is.** Numbers that decide (20 splits, held-out):
   - length only: 0.109 of size variation.
   - date: + time bin adds -0.002 over site and format; bin spread with text taken out is small (late +0.047, early -0.001, middle -0.030, P 0.043); twin stones in different time bins are closer in size (48%) than shuffled seals (88%) (`jobs/out/twins.md`). Not date.
   - workshop and stone kind: + stand, animal, material adds +0.100, the biggest block after format.
   - text beyond length: +0.018, real against every decoy, carried by a few rungs: comb 400 (alone +0.007, two-fifths of the text block), goods signs (box 590, cup 700, porter 156, tree 407) small, crests and personal emblems big.
   - office importance as a ladder of titles: not found (section below).
   So: size = the kind of stone (beast and workshop) first, then the holder's class read off a few signs, chiefly the comb ending (junior, about half size) and goods-headed names (stores, small). Rank of the holder is in it; a graded ladder of offices is not.

## The ladder tables

### 25 strongest "big" signs (model d on all 1,418 seals, signs in 4+ seals)

| rank | sign | picture (shape list) | picture (blind describers) | job | seals | size weight | 90% interval | % size |
|---|---|---|---|---|---|---|---|---|
| 1 | 706 | U with stroke variant | jar | name part | 41 | +0.229 | +0.137 to +0.318 | +26% |
| 2 | 692 | outlined X | outlined X | front word | 31 | +0.134 | +0.058 to +0.201 | +14% |
| 3 | 595 | barred box | box | name part | 20 | +0.127 | +0.043 to +0.196 | +14% |
| 4 | 745 | jar variant 745 | jar | name part | 12 | +0.100 | +0.038 to +0.166 | +10% |
| 5 | 368 | winged stroke | flag/sail | after-front slot | 56 | +0.098 | +0.031 to +0.160 | +10% |
| 6 | 231 | fish with stroke | fish/leaf | name front (crest) | 40 | +0.092 | +0.030 to +0.148 | +10% |
| 7 | 742 | jar variant | jar/cup | after-front slot | 24 | +0.091 | +0.026 to +0.140 | +10% |
| 8 | 354 | line with teeth variant | rake/comb | name part | 4 | +0.077 | +0.013 to +0.130 | +8% |
| 9 | 585 | sign 585 | tent | after-measure | 15 | +0.076 | +0.018 to +0.128 | +8% |
| 10 | 371 | garlic | bead/eye | name part | 7 | +0.075 | +0.015 to +0.130 | +8% |
| 11 | 679 | X with table | X with table | after-jar title | 12 | +0.075 | +0.005 to +0.140 | +8% |
| 12 | 140 | person with raised arm | man/leaf | name front (crest) | 56 | +0.074 | -0.000 to +0.146 | +8% |
| 13 | 101 | person with three heads 101 | man/jar | name part | 5 | +0.069 | +0.009 to +0.126 | +7% |
| 14 | 812 | leaf with hatched square | leaf with hatched square | name part | 7 | +0.068 | +0.013 to +0.120 | +7% |
| 15 | 703 | cup with three strokes | jar/comb | name part | 6 | +0.067 | +0.011 to +0.117 | +7% |
| 16 | 717 | paw | comb | name part | 24 | +0.066 | +0.003 to +0.147 | +7% |
| 17 | 806 | leaf on tree variant | leaf/comb | name front (crest) | 59 | +0.066 | +0.013 to +0.120 | +7% |
| 18 | 405 | tree variant 405 | rake/comb | counted thing | 41 | +0.065 | -0.013 to +0.136 | +7% |
| 19 | 500 | divided triangle | tent/house | name part | 6 | +0.061 | +0.018 to +0.105 | +6% |
| 20 | 317 | ladder | ladder | name part | 4 | +0.058 | +0.006 to +0.102 | +6% |
| 21 | 235 | capped fish | fish/bow | name front (crest) | 107 | +0.058 | -0.000 to +0.109 | +6% |
| 22 | 921 | bracket with arc | bow | name part | 11 | +0.054 | -0.009 to +0.106 | +6% |
| 23 | 773 | U with forked arm 773 | tree/jar | name part | 5 | +0.052 | +0.011 to +0.090 | +5% |
| 24 | 018 | eight stacked strokes | eight stacked strokes | short number | 4 | +0.051 | -0.004 to +0.106 | +5% |
| 25 | 125 | archer | man/bow | name part | 34 | +0.050 | -0.022 to +0.117 | +5% |

### 25 strongest "small" signs

| rank | sign | picture (shape list) | picture (blind describers) | job | seals | size weight | 90% interval | % size |
|---|---|---|---|---|---|---|---|---|
| 1 | 400 | comb | comb/ladder | after-jar title | 64 | -0.185 | -0.247 to -0.114 | -17% |
| 2 | 590 | box with bar | box/weight | name part | 88 | -0.143 | -0.210 to -0.069 | -13% |
| 3 | 700 | cup | cup/jar | counted thing | 13 | -0.123 | -0.197 to -0.044 | -12% |
| 4 | 495 | sign 495 | horn/bow | name part | 12 | -0.112 | -0.158 to -0.049 | -11% |
| 5 | 061 | reversed lambda | reversed lambda | place or time word | 42 | -0.104 | -0.157 to -0.035 | -10% |
| 6 | 350 | line with teeth | fork | name part | 23 | -0.098 | -0.137 to -0.044 | -9% |
| 7 | 156 | porter with jars 156 | man | counted thing | 38 | -0.094 | -0.149 to -0.020 | -9% |
| 8 | 741 | jar with mark | jar/cup | after-front slot | 107 | -0.087 | -0.133 to -0.036 | -8% |
| 9 | 804 | leaf with tree 804 | leaf/fork | name part | 5 | -0.080 | -0.142 to -0.021 | -8% |
| 10 | 527 | hatched box | ladder | after-jar title | 37 | -0.072 | -0.130 to -0.013 | -7% |
| 11 | 031 | one tall stroke | one tall stroke | tall number | 95 | -0.070 | -0.139 to -0.009 | -7% |
| 12 | 401 | sign 401 | jar/cup | name part | 5 | -0.070 | -0.123 to -0.015 | -7% |
| 13 | 455 | three triangles | three triangles | name part | 21 | -0.063 | -0.125 to +0.006 | -6% |
| 14 | 151 | porter | leaf/man | closer | 45 | -0.063 | -0.119 to +0.007 | -6% |
| 15 | 171 | T with leaf | tree | measure | 11 | -0.061 | -0.119 to +0.007 | -6% |
| 16 | 460 | three tall triangles | hill | name part | 22 | -0.060 | -0.102 to -0.009 | -6% |
| 17 | 032 | two tall strokes | two tall strokes | tall two | 133 | -0.060 | -0.121 to +0.000 | -6% |
| 18 | 760 | branched U | jar/cup | after-measure | 52 | -0.060 | -0.115 to -0.000 | -6% |
| 19 | 070 | stroke with arms | arrow/tree | name part | 23 | -0.059 | -0.102 to -0.009 | -6% |
| 20 | 844 | sign 844 | sign 844 | name part | 7 | -0.057 | -0.091 to -0.021 | -5% |
| 21 | 511 | square with lines 511 | square with lines 511 | name part | 5 | -0.054 | -0.157 to +0.030 | -5% |
| 22 | 853 | diamond with arms | spider/star | name part | 9 | -0.053 | -0.076 to -0.017 | -5% |
| 23 | 013 | three stacked strokes | three stacked strokes | short number | 23 | -0.053 | -0.121 to +0.022 | -5% |
| 24 | 550 | pincers | pincers | front word | 44 | -0.053 | -0.113 to +0.017 | -5% |
| 25 | 315 | H variant | ladder | name part | 6 | -0.053 | -0.107 to +0.009 | -5% |

Job mix: big end 14 name parts (14.1 expected), 4 crests (1.4 expected), 2 after-front slots (0.8), one each front word, after-measure, title, counted thing, short number. Small end: 12 name parts, 2 titles, 2 counted things and one each of place word, slot, tall number, closer, measure, tall two, after-measure, short number, front word. The big end is crests and personal emblems; the small end is goods (box, cup, porter, tree as measure 171), the comb title and the porter closer.

### Titles and closers (mean residual size of seals carrying the sign; ridge weight beside it)

| sign | picture | job | seals | all | ridge | MD (n) | HP (n) | early (n) | middle (n) | late (n) |
|---|---|---|---|---|---|---|---|---|---|---|
| 679 | X with table | title | 12 | +0.293 | +0.075 | +0.186 (10) | +0.490 (1) | | +0.407 (2) | -0.015 (6) |
| 621 | barred tall rectangle | title | 12 | +0.055 | +0.010 | +0.062 (11) | | -0.107 (4) | +0.204 (4) | -0.025 (3) |
| 161 | porter with diamond | title | 10 | +0.042 | +0.016 | -0.034 (5) | +0.221 (3) | | +0.198 (3) | -0.122 (3) |
| 565 | closed X | title | 9 | +0.041 | +0.010 | -0.032 (7) | +0.528 (2) | +0.038 (1) | -0.022 (6) | +0.290 (2) |
| 090 | man | title | 59 | +0.004 | -0.001 | +0.013 (42) | -0.168 (10) | +0.102 (6) | -0.104 (22) | +0.139 (19) |
| 520 | spear | closer | 145 | +0.004 | -0.033 | +0.032 (97) | -0.151 (22) | -0.141 (14) | +0.040 (55) | -0.067 (40) |
| 740 | jar | closer | 644 | -0.011 | -0.031 | -0.017 (425) | -0.000 (125) | -0.024 (65) | -0.045 (224) | +0.012 (193) |
| 154 | porter with jars | closer | 26 | -0.080 | -0.047 | -0.048 (10) | -0.128 (11) | | -0.061 (7) | -0.255 (10) |
| 527 | hatched box | title | 37 | -0.091 | -0.072 | -0.177 (24) | +0.227 (5) | -0.304 (7) | -0.048 (5) | -0.138 (11) |
| 151 | porter | closer | 45 | -0.100 | -0.063 | -0.093 (28) | -0.148 (4) | +0.209 (5) | -0.153 (16) | -0.157 (8) |
| 241 | caged whiskered fish | title | 10 | -0.132 | -0.037 | -0.151 (9) | +0.070 (1) | | +0.142 (3) | -0.170 (2) |
| 158 | porter with jars 158 | closer | 5 | -0.185 | -0.021 | -0.293 (3) | +0.015 (2) | -0.077 (1) | -0.196 (4) | |
| 400 | comb | title | 64 | -0.268 | -0.185 | -0.193 (45) | -0.485 (14) | +0.227 (3) | -0.335 (31) | -0.241 (19) |

Read: three tiers. Top, few and thin: 679 (+0.29; seals `740-679` +0.300 against jar-final -0.004). Middle, flat and equal: jar 740, man 090, spear 520, 621, 565, 161 (all within ±0.06 of each other overall). Bottom: the porters 151/154/158 (-0.08 to -0.19) and comb 400 (-0.27). The "jar then man" seal is not bigger once its extra sign is counted: `740-090` seals -0.020 against jar-final -0.004 (46 seals); the earlier median gap (778 against 652 mm2) is the length.

Stacks (two title / closer signs side by side, 139 pairs): the later sign sits higher on the ladder 87 times. By pair: `740-090` higher 46 of 46, `740-679` 9 of 9, `740-565` 4 of 4, `740-621` 3 of 3, `400-740` 9 of 9, `400-520` 4 of 4; lower: `740-400` 0 of 11, `090-740` 0 of 5, `090-400` 0 of 4, `740-154` 0 of 4, `740-527` 0 of 4. Every stack that ends in comb or a porter steps down; every stack from the jar to a non-comb title steps up.

### Crest houses (6+ non-agent complete seals; mean residual size)

Biggest: 371 garlic +0.466 (6), 706 +0.438 (12), 921 bracket with arc +0.413 (6), 632 tall rectangle with strokes +0.297 (8), 745 +0.297 (6), 617 +0.251 (7), 055 eight-stroke block +0.246 (7), 405 tree variant +0.239 (7), 575 +0.203 (18), 806 leaf on tree variant +0.195 (27). Smallest: 700 cup -0.507 (10), 407 tree variant -0.380 (6), 853 -0.364 (6), 440 open rectangle -0.271 (6), 590 box -0.231 (28), 388 -0.229 (8), 061 -0.227 (23), 690 -0.214 (7), 550 -0.201 (6), 350 -0.159 (7). Fish crests sit at the middle: 231 +0.085, 220 -0.011, 235 -0.017, 240 -0.030, 233 -0.108 (median house -0.021). Full list `crests.csv`.

### Tablets (`tablets_tests.csv`)

| set | count with name fixed: objects / names, Spearman, P | name with count fixed: objects / names, between-name share against dealt, P |
|---|---|---|
| all tablets and tags | 81 / 19, +0.005, P 0.63 | 174 / 51, 0.789 against 0.315, P < 0.0005 |
| moulded TAB:B | 14 / 6, +0.325, P 0.93 | 42 / 19, 0.934 against 0.403, P < 0.0005 |
| incised TAB:I | 57 / 12, -0.059, P 0.35 | 83 / 18, 0.473 against 0.185, P < 0.0005 |
| copper TAB:C | 10 / 1, +0.142, P 0.69 | 49 / 14, 0.828 against 0.214, P < 0.0005 |

## What went against

- **Frame-v2 job classes and fixed phrases add nothing as yes/no columns.** Held-out: classes 0.294 (= baseline 0.294; class decoys 0.294, best 0.311); phrases 0.287 (phrase decoys 0.287); 20-split means 0.285 and 0.287 against baseline 0.285. Almost every seal has the same classes present, so presence carries nothing; the job effect shows up only through the per-sign weights (crests up, closers and goods down, finding 4). Next: class COUNTS and the ending sign as a category.
- **No graded ladder of titles across cities.** Mohenjo-daro against Harappa, title and closer signs with 3+ seals both sides (8 signs): Spearman -0.10, while random sets of other signs give 0.35 (88% of them at or above). Redesign with 5+ seals both sides: -0.03 against 0.54; 8+ both sides: 0.20 against 0.69. Across time: early vs late -0.29, middle vs late +0.45 (40% of random sets at or above); inside Mohenjo-daro, early+middle vs late +0.64 (8% of random sets at or above: stable inside one city over time). The disagreements are 527 (MD -0.18, HP +0.23), man 090 (+0.01 / -0.17) and spear 520 (+0.03 / -0.15). Rescue plan: the one rung that holds in every city is comb 400; next test is the porter rung (151/154/158) city by city with all object kinds, and 527 split by its fixed phrase `555-527` / `550-527` (front-word use) against its after-jar use.
- **Big-seal houses do not have more agents, cities or impressions.** House size against agents per seal Spearman -0.245 (P 0.96 for positive), agents -0.213, cities -0.049, impressions per seal +0.012, impressions -0.009; beyond what each house's object count gives: cities +0.110 (P 0.22), impressions +0.071 (P 0.31), agents -0.067. Fish crests sit at the median, not above. The houses that keep agents (853, 061, 550, 350, 233) are on the small side. Rescue: the agent pattern points the other way: houses named as masters may be offices whose own seals are small stores seals; next test is house size against the masters list of `masters_*.py` directly, and the size of the agent seal against the size of its master's own seals.
- **Size does not help restore a lost sign.** 31 of the 77 gap texts are seals with a size. Sign model alone top-1 / top-5 / top-10: 41.9% / 67.7% / 77.4%; with the per-sign size term 29.0% / 67.7% / 80.6%; with sizes dealt among those seals 38.1% / 69.7% / 78.1%. Redesign (job-level size weight, applied only to the sign model's top 10): 38.7% / 67.7% / 80.6% against dealt 39.5% / 62.7% / 73.7%: top-5 and top-10 above the dealt control, top-1 below the sign model alone. New idea run: size alone tells a comb-final from a jar-final seal in 64.7% of pairs (49 against 515), so size is worth using only where the lost sign is the ending. On 476 restorations of seals with a size, the size term changes the top choice in 26 (`gaps_restorations_changed.csv`).
- **Prediction misses**: the big end of the ladder replicates only weakly on half B (54.8%, P 0.16); W is not "the late format" (W share early 42%, middle 40%, late 47%); W twins are not bigger than their other-stand twins (6 of 16); counts on tablets do not shrink tablets with the name fixed.
- **Second catalogue**: 0 of its new texts carry a size (it has no measurement field). Stand-in used: the 102 first-catalogue seals whose text has no second-catalogue partner (baseline 0.130, per-sign 0.147).

## Next

1. Use the comb rung: list every seal and tablet ending `740-400` with its findspot, house and animal; test whether comb holders share houses with jar holders of the same name (junior of a house).
2. Goods-headed names (box 590, cup 700, tree 407, porter 156): test whether their small seals sit in stores areas (Harappa granary area, DK-G) more than the jar-headed names of the same length.
3. Stand letter as workshop: map W / J / S / I / L by city and building, and test whether each workshop cut its own size band.
