# Counted things in the Indus corpus

Data: `metadata_filtered.csv`, 5,679 rows, reading order = stored order reversed, count signs as in the brief (short strokes 001-007 = 1-7 "S", stacked strokes 012-018 = 2-8 "T", full-height strokes 031-036 = 1-6 "F", A-with-comb 465-475 "A"). Scripts: `work_scripts/counted_common.py`, `counted_instances.py`, `counted_resolve.py`, `counted_table.py`, `counted_dist.py`, `counted_series.py`, `counted_world.py`, `counted_where.py`, `counted_misc.py`, `counted_commodity.py`, `counted_report_tables.py`, `counted_gloss30.py`. Tables: `work_data/counted/` (`sign_by_count.csv` full sign x count, `commodity_table.csv`, `where.csv`, `world_enrich.csv`, `instances_resolved.csv`).

## Headline

1. The corpus holds 4,012 places where a count sign touches another sign. A count between two signs belongs to one of them ("n X" or "X n"); settled by fitting each sign's pull on counts from both sides, 2,642 are owned: 1,418 "n X" (count first) and 1,224 "X n" (count after). About 45 signs carry counts at least 12 times.
2. There are two counting systems and the counted thing picks the system, not the object type. Full-height strokes count measures and made goods (cup 700: 96% full-height; box 590: 88%; jar 740: 75%; caged fish 226: 73%; the U-with-stroke 705/706: 97-98%). Short strokes count grown, living and handled things (tree 390: 62% short plus 26% stacked, rising to 6-8; woman 140: 78%; fish variants 240/235: 73-88%; leaf 803: 92%; paren 900: 100%; crop 806: 100% short or A-comb). Within seals the signs differ in full-height share at chi2 = 88 (10 dof, p = 1e-14); within tablets at chi2 = 323 (4 dof). Stacked strokes continue the short series upward: T6/T7/T8 take over where S5 ends (S6 3, S7 3 against T6 30, T7 58, T8 5).
3. Numbers do not fall off from one. Across all owned "n X" counts: F2 299, F3 216, S3 191, S2 154, F4 123, F1 107, S1 73, T7 58, S4 53, A 35, S5 33, T6 30. Full-height stops at 4 (F5 5, F6 5); short stops at 5. Each counted thing has its own preferred number, and most sit on one or two values (below).
4. The cup sign 700 is the unit of the Harappa tablets: 388 times "n cups" with n = 2, 3, 4 at 100 / 150 / 116 (and 0 at 5, 5 at 1, 3 at 6), 369 of 388 ending the face. The same 2-3-4 band is what bare numbers on pots show (122 pots whose whole text is one count: F2 41, F3 23, F4 12, F1 8, F5 6).
5. New standard tablet found: 21 three-faced steatite tablets from Harappa (area E Trench 11 for 69 of the 80 objects that carry 861-003) with faces "4 cups | 3 x 861 | 3 x 156" (20 with 034-700, 1 with 033-700; every 861 face is 003, every 156 face 003). It is a fixed three-line account: cup-measure 4, diamond-unit 3, load 3. 156 and 861 are units counted by three.
6. 806 (crop) takes counts A-comb 32, two strokes 13, one 2 of 47 owned, 62% followed by the load-carrier, and lives with the plant animal on seals (7 of 47 against 1.0% of corpus, p = 3e-7).

## 1. Sign x count table (count first, "n X")

"occ" = occurrences in corpus; "raw adj." = count sits right before it; "owned" = after settling counts shared between two neighbours. Values: S = short, T = stacked, F = full-height. Full file: `work_data/counted/sign_by_count.csv` (raw) and `instances_resolved.csv`.

| sign | shape | occ | raw adj. | owned | counts (value:n) | followed by |
|---|---|---|---|---|---|---|
| 700 | Simple U (cup) | 575 | 389 | 388 | S3:3 S4:9 T4:1 T7:1 F1:5 F2:100 F3:150 F4:116 F6:3 | END 369, comb 1 |
| 220 | Fish, plain | 473 | 144 | 103 | S1:1 S2:9 S3:18 S4:4 S6:1 T4:1 T6:12 T7:1 F1:3 F2:48 F3:4 F4:1 | other 75, jar 15, END 11 |
| 390 | Tree with branches at the top | 289 | 90 | 58 | S1:1 S3:18 S4:12 S5:4 S6:1 T6:10 T7:4 T8:1 F2:2 F3:1 F4:3 F5:1 | END 52 |
| 156 | Person carrying two burdens, jar-handle head | 106 | 51 | 49 | S3:36 S4:1 S5:2 F1:10 | END 49 |
| 806 | Leaf with tree at bottom | 135 | 58 | 47 | S1:2 S2:13 A:32 | carrier 29, other 14, END 3 |
| 861 | Diamond with small diamond on top | 272 | 36 | 36 | S2:1 S3:29 F1:3 F2:2 F6:1 | END 29 |
| 585 | (no shape listed) | 60 | 34 | 31 | T7:27 F3:4 | other 19, jar 12 |
| 900 | Right parenthesis | 112 | 34 | 27 | S1:1 S2:1 S3:12 S4:5 S5:8 | jar 14, other 8 |
| 840 | Two vertical leaves, overlapping | 130 | 31 | 25 | S2:3 T3:15 T6:2 F2:5 | jar 14, count 6 |
| 590 | Square with bar off top middle | 228 | 44 | 24 | S2:1 T7:2 F1:3 F2:15 F3:3 | other 18 |
| 240 | Fish, extra whiskers | 349 | 101 | 22 | S1:3 S2:13 F1:4 F2:2 | other 18, jar 3 |
| 407 | Tree with branches at the top | 142 | 28 | 22 | S3:1 S4:7 S5:2 T6:1 T7:1 F2:9 F3:1 | END 21 |
| 405 | Tree with branches at the top | 118 | 26 | 20 | S2:1 S3:3 S4:4 S5:6 T6:1 T7:3 T8:1 F2:1 | END 19 |
| 740 | Jar | 1888 | 109 | 20 | S4:1 S5:1 T3:1 T6:1 T7:1 F2:12 F3:2 F5:1 | END 12, comb 7 |
| 140 | Person with round breasts | 109 | 23 | 18 | S1:1 S2:6 S3:6 S5:1 T5:2 F2:2 | other 13, END 3 |
| 055 | Four strokes over four over four (12 strokes) | 62 | 20 | 16 | S1:13 F1:2 F3:1 | other 14 |
| 061 | Reversed lambda | 92 | 27 | 15 | S2:10 F1:2 F2:2 F3:1 | other 9, jar 6 |
| 226 | Fish with four strokes round it | 38 | 17 | 15 | S2:2 S3:2 F2:11 | END 10 |
| 520 | Triangle on vertical line (spear) | 317 | 67 | 15 | S1:3 T3:1 F1:5 F2:1 F3:5 | END 14 |
| 575 | Trapezoid with box on top | 80 | 17 | 15 | S1:1 T7:12 F1:2 | jar 12 |
| 803 | Leaf with tree at bottom | 134 | 38 | 13 | S1:1 S2:11 F1:1 | other 13 |
| 384 | Upside-down heart | 33 | 13 | 12 | S2:3 F1:5 F2:3 F3:1 | jar 7, carrier 3 |
| 904 | Two nested right parens | 64 | 21 | 12 | S1:3 S4:1 F2:7 F3:1 | jar 6, END 3 |
| 550 | Pincer motif | 122 | 24 | 11 | S2:1 S3:8 F3:1 A:1 | other 8 |
| 151 | Person carrying two burdens | 93 | 9 | 9 | T7:1 F1:3 F2:1 F3:4 | END 8 |
| 154 | Person carrying two burdens, jar-handle head | 45 | 9 | 9 | S3:4 S4:1 S5:1 T7:1 F1:1 F2:1 | END 8 |
| 645 | X | 28 | 10 | 9 | S1:1 S3:5 F1:2 F2:1 | other 4 |
| 142 | Person with staff | 81 | 16 | 8 | S1:3 S2:2 F1:1 F3:2 | other 6 |
| 235 | Fish with caret hat | 249 | 48 | 8 | S2:7 F3:1 | other 7 |
| 417 | Two facing pitchforks | 9 | 8 | 8 | S2:8 | other 8 |
| 422 | Long base with many verticals | 8 | 8 | 8 | S3:8 | END 6 |
| 877 | Diamond with four small diamonds | 22 | 10 | 8 | F2:8 | jar 6 |
| 760 | U with branching top | 134 | 19 | 8 | S1:4 F2:2 F3:1 F6:1 | jar 8 |

Count after the sign ("X n"), owned, with what follows the count:

| sign | shape | occ | owned | counts | after the count |
|---|---|---|---|---|---|
| 861 | Diamond opener | 272 | 177 | S2:173 S3:2 T3:2 | other 118, count 42, END 17 |
| 817 | Diamond opener | 220 | 164 | S2:155 T3:5 | other 117, count 36 |
| 820 | Six-spoke wheel opener | 242 | 139 | S2:101 S1:19 F2:10 T3:4 | other 94, count 32 |
| 705 | U with long stroke in the gap | 218 | 106 | F3:96 F1:3 S2:3 F5:2 | other 92, END 7 |
| 700 | Cup | 575 | 80 | F3:35 F2:24 F4:14 F1:4 | END 73 |
| 840 | Two leaves | 130 | 47 | F2:42 S2:3 | jar 35 |
| 706 | U with long stroke in the gap | 101 | 45 | F3:44 | other 40 |
| 405 | Tree | 118 | 32 | S2:31 | other 32 (29 of them 240) |
| 171 | T with leaf | 29 | 25 | F5:17 F2:7 | other 7, count 7 |
| 480 | Caret (mountain) | 42 | 22 | S1:12 F1:5 F2:2 | other 13 |
| 368 | Stroke with wing | 117 | 19 | S1:9 S2:8 | other 13 |
| 503 | Tall striped triangle | 82 | 19 | T7:11 S7:3 T6:3 | jar 15 |
| 905 | Nested parens with tooth | 12 | 11 | F2:9 | other 9 |

Number-sandwich formulas, where the count could belong to either neighbour: 405-002-240 (29 of 29 occurrences of 405-with-a-count; 405 never meets 240 without it), 840-032-740 (35), 705-033-845 (15 of 15), 706-033-923 (11 of 11), opener-002-X (about 400). They behave as fixed phrases with the number inside.

What follows counted things: cup, 156, 154/151, trees 390/405/407, 861, 520 and 226 end the text (END 95%, 100%, 89%, 90-95%, 81%, 93%, 67%). Jar 740 follows 840, 900, 904, 575, 760, 877, 384 and the stacked-7 signs 585/575/503 (jar 39-80%). The comb 400 follows counted jars (7 of 20, "032 740 400"). Carriers follow only 806 (62%) and 384 (25%). Nothing else takes a carrier.

## 2. Count distributions

- Hump, no ceiling at one: cup 2/3/4 = 100/150/116. Graded within a band, range 3 values, ceiling 4. Bare pot numbers have the same band. Pots: 122 single-count pots; full-height 91, short 26, stacked 5; tablets with one count: 33 of 35 full-height (F3 15, F4 12, F2 5).
- Wide short band starting at 3: tree 390 S3 18, S4 12, S5 4 then stacked T6 10, T7 4, T8 1. Nothing at 1 or 2 (S1 1). Tree 405: S2 1, S3 3, S4 4, S5 6, T6-8 5. Tree 407: S4 7, S5 2 and F2 9. Paren 900: S3 12, S4 5, S5 8. These count three to eight: a bundle starts at three.
- Plain fish 220 uses all three registers: F2 48, S3 18, T6 12, S2 9, S4 4 (see section 4).
- Fixed on one value (top share 80% or more, 10+ cases): 861 "three" (S3 29 of 36), 156 "three" (S3 36 of 49, plus F1 10), 585 "seven" (T7 27 of 31), 575 "seven" (T7 12 of 15), 055 "one" (S1 13 of 16), 803 "two" (S2 11 of 13), 061 "two" (S2 10 of 15), 806 (A-comb 32, S2 13), 226 "two tall" (F2 11 of 15), 877 "two tall" (F2 8 of 8), 417 "two", 422 "three" (8 of 8), 705/706 "three tall" (96 of 106; 44 of 45), 840 "two tall" (42 of 47) and "three stacked" (T3 15 of 25), 405 "two" (31 of 32), openers 861/817 "two" (98%/95%), cup-after-count F3 35.
- Fixed at seven: the stacked seven is the single favoured big number: 585 + 575 + 503 give T7 50; T7 58 in all. T6 is the other (390 10, 220 12).
- Name-like: "the seven" (T7 on 585, 575, 503) and "the three" (861, 156, 705, 706, 520/F3 5).

Two systems for two kinds of thing, as numbers: tablets are 74% full-height (451 F against 122 S and 33 T), seals 37% (224 of 609); but inside seals 900 and 806 are 0% full-height and 590 is 83%, 220 is 60%; inside tablets 861 and 156 are 3-4% full-height and the cup is 96%.

## 3. Counted things and the world

Baselines over all 5,679 objects: seals 40%, copper tablets (TAB:C) 4.1%, pots 11%, tags 4.6%, Harappa 48%, Mohenjo-daro 34%, Lothal 3.7%, Harappa mound F 16%, granary 2%, copper 4.6%, faience 11%, steatite 46%, no animal 56%. Full file `work_data/counted/where.csv`; enrichment tests `world_enrich.csv`.

| thing | n | where it lives (share of its counted objects; baseline in brackets) |
|---|---|---|
| cup 700 (count first) | 388 | tablets 97% (40% + 40% tabs), Harappa 97% (48%), faience 33% (11%), no animal 82% (56%), mound F 39% (16%), median face 116 mm2, trenches F-I 16.5% (4.2%), E-11 14% (5.8%) |
| 156 | 49 | tablets TAB:I 47%, Harappa E-11 43% (5.8%), Mohenjo DKG(S) 29% (10%), median face 99 mm2 |
| 861 (counted 3) | 36 | TAB:I 83%, Harappa 86%, E-11 67%, steatite 89%, median face 87 mm2, no animal 86% |
| 806 | 47 | seals 68%, Harappa 57%, mound F 28%, granary 5% (2%), plant symbol 15% (1.0%) |
| trees 390 | 58 | seals 76%, Mohenjo 57%, Bull1 45% (25%) |
| trees 405 / 407 | 20 / 22 | seals 75% / copper tablets 45% (4.6%), Mohenjo 73% |
| fish 220 | 103 | seals 70%, Mohenjo 51%, Bull1 45% |
| 585 | 31 | copper tablets 55% (4.1%), copper 55%, Mohenjo 74% |
| 575 | 15 | seals 73%, jar 80% after |
| 840 | 25 / 47 | Harappa 48%, tablets 44-49% |
| 590 | 24 | Harappa 58%, tablets 42%, no animal 46% |
| 055 | 16 | tags 69% (4.6%), Lothal 69% (3.7%), Lothal SRG 3GX 10 area 50% (0.5%), clay 75% |
| 740 (counted 2) | 20 | tablets 55% (36%), Harappa 65%, no animal 75% |
| 705 / 706 (+3) | 106 / 45 | Mohenjo 64% / 71%, copper tablets 16% / 24%, seals 55% / 76%, hare animal on 705 (12 of 113, 46x baseline), elephant on 706 (11 of 46, 20x) |
| 900 | 27 | seals 93%, steatite 82% |
| 520 spear (counted) | 15 | seals 47%, copper tablets 62% in the "X n" frame, Mohenjo 94% there |
| 700 (cup then count) | 80 | Harappa 90%, tablets 85%, faience 49% |

Where the picture is sharp:
- Cup: a tablet thing (97%), a Harappa thing (97%), a faience-heavy thing (33%) and in the mound F / trench I-E11 area, with small tablets (116 mm2 median) and no animal; its numbers equal pot numbers.
- The 3-line account tablet is a single Harappa trench: 69 of the 80 objects with 861-003 faces are from E Trench 11.
- The copper-tablet cluster (Mohenjo, DK area): 585 with seven (55% copper tablets), 405/407 with trees (45%), 705 and 706 with "3" (hare 12, elephant 11), 845 and 923 with "3" (raw 93% and 80% copper tablets, hare 80% and elephant 73% of the counted objects). 228 copper tablets exist; the top copper-tablet texts are `503 615 752 740` (29), `806 845 061 407 850 900 740` (14), `235 705 033 845 407 321 407` (14), `231 017 585 095 520 032 407` (8): each one is a list of numbered goods.
- Lothal tags (clay, port): the counted thing is 055 (one 055, then fish): 11 copies of `705 500 741 001 055 220 740 090`.
- Pots carry bare full-height numbers (91 of 122) and no commodity.
- Trees and seals: tree counts sit at the END of seal texts (90% of 390 cases), on the Bull1 animal (45% against 25%). The count of trees is a seal-owner property.

## 4. Fish

Fish family (220, 222, 226-228, 231-236, 240-244): 1,494 occurrences. Count right before: 374 raw, 25%; 162 owned, 10.8%. The raw S2 before fish (195 of 374) is mostly the opener's own two strokes (861/817/820-002-fish) and the 405-002-240 formula; once counts go to their owner, the numbers before fish are:

| fish | occ | owned | counts |
|---|---|---|---|
| 220 plain | 473 | 103 (22%) | F2 48, S3 18, T6 12, S2 9, S4 4, F3 4, F1 3 |
| 226 caged | 38 | 15 (39%) | F2 11, S2 2, S3 2 |
| 240 whiskers | 349 | 22 (6%) | S2 13, F1 4, S1 3, F2 2 |
| 235 hat | 249 | 8 (3%) | S2 7, F3 1 |
| 233 line | 192 | 4 | S2 3, S3 1 |
| 231 dot | 94 | 4 | S2 3, S3 1 |
| 236, 241, 243 | | 1, 2, 2 | |
| all fish | 1,494 | 162 | F2 61, S2 39, S3 22, T6 12, F1 9, F3 6, S1 5, S4 4 |

- Fish counts are pairs: F2 plus S2 is 100 of 162 (62%). One is 14 of 162 (9%), three is 28 (17%), 4 or more 18. Fish go in twos, then threes.
- Plain fish 220 takes the full-height two (47%) and the stacked six (12%); marked fish 240/235/233/231 take the short two (27 of 38 in the short series). So the marked fish variants are written with the short system, the plain fish mostly with the tall one.
- 72% of counted fish are on seals (116 of 162), 13% on pots, 10% on tags (Lothal "055 220" tags), 13% tablets. Seals: Bull1 45% of counted 220.
- Fish is followed by the jar 15% of the time (counted 220) and by 520 spear in 18 of 220's contexts; counted fish never take a carrier.
- Reading: fish is a goods item bought or issued by pairs and threes, with a six-bundle (T6) and a dozen lot at Lothal. Fish 220 is a counted good in its own right, one rung below the cup in the ration chain.

## 5. Commodity table

Count series: S short, T stacked, F tall, A comb. "n" is owned counts (count-first unless marked X n).

| sign | shape | counted n | series (shares) | favoured numbers | lives | follows | boldest guess |
|---|---|---|---|---|---|---|---|
| 700 | cup | 388 (+80 X n) | F 96% | 2 /3 /4 = 100/150/116, none above 4 | Harappa tablets 97%, faience 33%, mound F 39%, tiny tablets, pot numbers same band | face end 95% | cup-measure of grain, the ration: "n cups"; ration scale of 2-4 |
| 156 | person carrying two burdens, jar-handle head | 49 | S 80%, F 20% | 3 (S3 36), 1 tall (F1 10) | Harappa E-11 tablets 43%, Mohenjo DKG(S) 29% | end 100% | a load (porter-load / basket): 3 loads a standard consignment |
| 861 | diamond with diamond on top (counted) | 36 | S 83% | 3 (29) | Harappa E-11 TAB:I 83% | end 81% | a bagged or sacked unit: 3 sacks |
| 806 | leaf with tree at bottom | 47 | S 32% / A 68% | A-comb 32, 2 strokes 13 | seals 68%, plant symbol 15%, mound F 28%, granary 5% | carrier 62% | crop / grain: "n loads of grain" |
| 220 | plain fish | 103 | F 54%, S 32%, T 14% | F2 48, S3 18, T6 12 | seals 70%, Mohenjo 51%, Lothal tags | other 73%, jar 15% | fish (dried fish), counted in 2s, 3s and sixes |
| 240 / 235 / 233 / 231 | marked fish | 22 / 8 / 4 / 4 | S 73-88% | 2 | seals 68-94% | other | grades or kinds of fish, counted in pairs |
| 226 | fish with four strokes round it | 15 | F 73% | F2 11 | seals 73% | end 67% | penned fish: "2 fish-pen" |
| 390 | tree, branching top | 58 | S 62%, T 26% | 3-5, 6-8 stacked, never 1-2 | seals 76%, Mohenjo 57%, Bull1 45% | end 90% | tree holdings (palms): 3 to 8 trees, a property count on seals |
| 405 / 407 | tree variants | 20 / 22 | S 70% / S 45%, F 45% | S3-S5 / F2 and S4 | seals 75% / copper tablets 45% | end 95% | tree variants: 407 the copper-tablet tree, counted 2 or 4 |
| 585 | (undescribed) | 31 | T 87% | 7 (27) | copper tablets 55%, Mohenjo 74% | jar 39% | "the seven": a seven-day allotment (days) |
| 575 | trapezoid with box | 15 | T 80% | 7 (12) | seals 73% | jar 80% | seven-day allotment, jar form |
| 503 (X n) | tall striped triangle | 19 | T 74% | 7 (11) | seals 58%, Harappa 53% | jar 79% | days / week: 7 then jar |
| 055 | block of 12 strokes | 16 | S 81% | 1 (13) | Lothal clay tags 69% | fish next (11 of 20 raw) | a dozen lot: "one dozen fish" |
| 840 | two overlapping leaves | 25 + 47 (X n) | T 68% before, F 91% after | 3 stacked; 2 tall after | Harappa 48%, tablets 45% | jar 56% (35 as 840-2-jar) | leafy produce packed by the jar: "2 jars of 840" |
| 740 | jar (counted) | 20 | F 75% | 2 (12) | tablets 55%, Harappa 65%, no animal 75% | end 60%, comb 35% | jar measure: 2 jars, the step above the cup |
| 590 | square with bar | 24 | F 88% | 2 (15) | Harappa 58%, tablets 42% | other 75% | storage bin / box: "2 bins" |
| 900 | right paren | 27 | S 100% | 3-5 | seals 93%, steatite 82% | jar 52% | rolled goods (cloth bolts): 3 to 5 |
| 140 / 142 / 176 | woman / staff-man / sitting man | 18 / 8 / 26 (raw 26, owned ~16) | S 78% / S 62% / S 85% | 2-3 / 1 / 2 | seals 78%, Mohenjo 61% | other | worker classes: women 2-3, overseers 1-2 |
| 520 | spear | 15 (+16 X n) | F 73% | 1 and 3 (5 and 5) | seals 47%; X n frame copper tablets 62%, Mohenjo 94% | end 93% | copper spear / arrow heads: 1 or 3 |
| 705 / 706 (X n) | U with long stroke | 106 / 45 | F 97% / 98% | 3 (96 / 44) | Mohenjo 64% / 71%; copper tablets 16% / 24%; hare / elephant | other 85% | a three-measure unit, a name with its number |
| 845 / 923 | hatched leaves / outline paren | 15 / 15 (raw) | F 100% | 3 | copper tablets 93% / 80%, Mohenjo | 407 14 / jar 15 | metal goods in threes on copper tablets (after 705/706-033) |
| 171 (X n) | T with leaf | 25 | F 100% | 5 (17), 2 (7) | seals 52% | other | five-count item |

## 6. Thirty real texts (reading order, count first; "|" separates tablet faces)

Lexicon from the table: cup = cup-measure, 156 = load, 861 counted = sack, 806 = crop, carrier = carried, jar at end = "of the jar-house" (owner ending), comb 400 = closing tally, opener-diamond-2 = opening formula.

1. H-1138 (Harappa, faience tablet): face 1 `692 060 240 603 740` = [X-outline] [060] fish-whisker [tall-hatched] of-jar-house. Face 2 `034 700` = 4 cups. Account: for the fish-whisker jar-house, 4 cups.
2. H-1312 (Harappa E-F Trench I, steatite tablet, depth -15 ft): face 1 `032 001 904 031 740` = 2, [1 x nested-paren], 1, of-jar-house. Face 2 `032 700` = 2 cups.
3. H-1121 (Harappa F Trench III, faience tablet, -16.2 ft): `000 817 711 033 700` = [lost] opener, [U-with-X], 3 cups.
4. H-903 (Harappa F Trench I, steatite tablet, -15 ft): `817 368 690 034 700` = opener, [wing-stroke], [nested arrows], 4 cups.
5. M-480 (Mohenjo-daro DK, clay tablet, multi-animal): `004 700 097 400` = 4 cups, the bracketed man, closing tally. Cup tablet at Mohenjo, 4 cups to a man.
6. H-1977 (Harappa E-ETT 10E, clay tablet): `840 032 740` = two-leaf produce, 2, jar: "2 jars of the two-leaf goods".
7. H-2184 (Harappa E Trench 11, steatite tablet): `015 032 740 400` = 5, 2 jars, tally: a five-lot and two jars, counted.
8. H-967 (Harappa F Trench VI, steatite tablet): `028 032 740 400` = [slanted-row block], 2 jars, tally.
9. H-1979 (Harappa F Trench 41C, clay tablet, plant): `467 806 158 740` = n(comb-A) crop carried, of-jar-house: "n loads of grain carried; of the jar-house".
10. M-1986 (Mohenjo DKG(S) 9I, steatite seal, -4.8 ft): `468 806 154` = n loads of crop, carried (the whole seal).
11. H-1709 (Harappa E Trench 7/8, steatite seal): `470 838 158` = n of [838], carried: 838 sits in the crop slot, a second carried commodity.
12. H-2229 (Harappa, steatite tablet, three faces): `003 861 | 034 700 | 003 156` = 3 sacks | 4 cups | 3 loads.
13. H-2238 (Harappa E Trench 10W/11, steatite, three faces): `033 700 | 003 861 | 003 156` = 3 cups | 3 sacks | 3 loads.
14. M-1557 (Mohenjo copper tablet): `231 017 585 095 520 032 407` = fish-dot, 7 x [585], the short-stick man, spear, 2 x tree-407: a metal-tablet list: seven-day item, spear, two trees.
15. M-1485 (Mohenjo DK copper tablet, elephant): `706 033 923 740` = [U-staff x 3], outline-paren, of-jar-house.
16. M-1568 (Mohenjo DK copper tablet): `798 231 705 033 904 100 740` = leaf-pincer, fish-dot, [U-staff x 3], nested-paren, three-headed man, of-jar-house.
17. M-581 (Mohenjo DK copper tablet, other animal): `017 585 388 740` = 7 x [585], [heart-hatched], of-jar-house: "seven-day allotment for the heart-hatched jar-house".
18. M-1524 (Mohenjo VSA copper tablet, -4.4 ft): `806 235 233 705 033 585 407` = crop, fish-hat, fish-line, [U-staff x 3], [585], tree-407: crop and fish goods, then three, then tree.
19. M-550 (Mohenjo DK copper tablet, composite animal): `003 233 100 740` = 3 x fish-line, three-headed man, of-jar-house: three line-fish to the three-headed man's jar-house.
20. L-169 (Lothal clay tag, elephant; same text on L-163, L-165, L-170): `817 002 048 740` = opener-2, [seven-in-parens], of-jar-house.
21. L-190 (Lothal SRG 3GX 10 clay tag, -3.3 ft; also L-197): `705 500 741 001 055 220 740 090` = U-staff, horn-triangle, jar-dot, 1 x [dozen block], fish, of-jar-house, man: "a dozen-lot of fish, belonging to the jar-house of the man".
22. L-143 (Lothal tag, Bull1): `920 060 004 220 388 740` = paren-leaf, 060, 4 x fish, [heart-hatched], of-jar-house: four fish.
23. L-220 (Lothal SRG 2BX 4 tag, bull): `861 013 100` = opener-3(stacked), three-headed man.
24. M-860 (Mohenjo DK seal, Bull1:S): `240 705 033 520` = fish-whisker, [U-staff x 3], spear.
25. M-1269 (Mohenjo DK seal): `235 240 706 033 520` = fish-hat, fish-whisker, [U-staff x 3], spear: both marked fish then the three-unit, spear.
26. H-1673 (Harappa F Trench 43 seal, Bull1:W): `104 004 405` = [foot-caret man], 4 x tree-405.
27. M-958 (Mohenjo DKG(S) Low Lane, -11.1 ft, Bull1:J): `590 003 900 002 240 772 740` = bin, 3 x paren, 2 x fish-whisker, [U-with-fork-and-tree], of-jar-house: bin; 3 rolled goods; 2 fish; of the jar-house.
28. M-1880 (Mohenjo DKB 3VII, -8 ft, gaur): `861 002 176 151` = opener-2, sitting man, porter: a porter whose name begins with the sitting man.
29. M-380 (Mohenjo DKG(S) 1I, -13.9 ft): `322 920 740 001 003 137` = [H-bars], paren-leaf, of-jar-house, 1, 3 x [man with leaf]: "of the jar-house; one; three leaf-men".
30. H-149 (Harappa F-, steatite seal, 41.9 mm, no animal): `820 002 220 630 794 706 033 061 405` = wheel opener-2, fish, [630], [794], [U-staff x 3], lambda, tree-405: a fish and a three-unit then tree.

## 6b. Whole tablets as accounts (cup + diamond + load)

Scripts `work_scripts/counted_records.py` (faces grouped by cisi; 787 multi-face tablets, 736 two-face, 51 three-face; fronts file `work_data/counted/tablet_fronts.csv`). One face = one line: count + thing.

Claims, with numbers:
1. One tablet says 3 loads / 3 diamonds / 4 cups. 22 three-face tablets carry `003 861` and `003 156` (or `003 154`) faces; 21 of them have cup+4 (`034 700`), 1 has cup+3 (H-2238, `033 700`). Cups per load is 4 for 3 in 21 of 22; the exception is 3 for 3. 20 of the 22 are from E Trench 11 (steatite). Their cisi: H-2218 to H-2236 (19 numbers), H-2237 (with 154), H-2238, H-2239.
2. Counted-diamond faces: `003 861` occurs on 29 tablets. 21 pair with cup+4, 1 with cup+3, 7 have no cup face and sit beside an owner front (H-2119 `416 740`, H-2123 `061 255 740`, H-2190 `327 740 090`, H-921 `061 255 740`, H-922 and H-923 `031 520`, H-1882 `820 002`). So a diamond-3 face is the alternative to a cup face on a two-face tablet: "owner front | 3 diamonds".
3. Whole-tablet statistics, cup+4 tablets (130 non-cup faces on 106 tablets): 42 open with 003 (all `003 861` 21, `003 156` 20, `003 154` 1), 25 close with 156 (20 are `003 156`), 21 close with 861. Counting every non-cup face that opens with 003 and sits on a cup tablet: 42 of 45 have cup+4 (the other three: H-2238 twice with cup+3, H-854 with cup+2). Faces ending in 156: 25 of 32 (cup+4), faces ending in 861: 21 of 22.
4. Cup+2 and cup+3 tablets pair with a different front. Their fronts end in the comb 400 or the jar 740 in 63 of 92 (68%) and 82 of 124 (66%) cases, against 47 of 130 (36%) for cup+4; they end in 156 or 861 in 2 of 92 and 3 of 124, against 46 of 130 (35%). Cup+3 fronts open with the sitting man 176 in 22 of 124 (18%) against 6 of 92 (7%) for cup+2 and 14 of 130 (11%) for cup+4. Cup count follows the trench: E Trench 11 gives cup+4 60 of 73 (82%), F Trench I gives cup+4 15 of 57 (26%) and cup+3 28; chi2 = 93, 14 dof, p = 1e-13. Steatite goes 4 (82) and 3 (58); faience goes 2 / 3 / 4 evenly (39 / 39 / 30).
5. So there are two kinds of tablet. The E-11 cup+4 kind is a standard consignment: a fixed 4 cups for 3 + 3 units (fronts 2 signs long: 60 of 130). The F-trench cup+2 / cup+3 kind is an owner record: a long front (3 to 4 signs in 147 of 216) naming a jar-house or comb-closed person, plus a variable cup count of 2 or 3.
6. The diamond as a counted thing: 861 is counted in 36 "n X" cases: 29 are `003 861` tablet faces (TAB:I, steatite, Harappa 86%, E-11 67%, median face 87 mm2, no animal 86%) and 7 are other. After it, always END (81%). It is never counted by two on tablets: the "two" belongs to the seal-opener use (861 + 002 in 177 cases, 98% two, on seals 71%, Mohenjo 53%). In the counted-by-three use it equals the load count in every tablet that carries both (22 of 22 equal, 3 = 3). Boldest reading: the diamond is a person-unit, a household or worker-hand, counted on the same footing as the porter-load (156 is a person carrying two burdens); the tablet issues 4 cups for 3 hands and 3 porters. The seal opener "diamond + 2" is then "two hands / a pair of households" heading every seal text.

Records glossed (reading order, one line per face, `|` between faces; cup = cup-measure ration, load = porter, diamond = hand):

1. H-2229 (Harappa E Trench 11, steatite, 10 x 6 mm, three faces): 3 diamonds | 4 cups | 3 loads. Record: ration of 4 cups for 3 hands and 3 porters. Same line for H-2218 to H-2236 (19 tablets), H-2239 and H-2237 (last face `003 154`).
2. H-2238 (Harappa E Trench 10W/11, steatite): 3 cups | 3 diamonds | 3 loads. The one 3:3:3 record.
3. H-2237 (E Trench 11, steatite): 4 cups | 3 diamonds | 3 [154-load]. 154 is the stamp form of the load carrier; same record.
4. H-2119 (Harappa E Trench 11, steatite): 3 diamonds | [416] of-jar-house. Owner front, then a 3-hand line; no cup line.
5. H-2123 (Harappa E Trench 11): [061] [255] of-jar-house | 3 diamonds. Owner (lambda, animal-fish) with 3 hands.
6. H-2190 (Harappa E Trench 11): [327] of-jar-house, man | 3 diamonds.
7. H-921 (Harappa F Trench IV+V): 3 diamonds | [061] [255] of-jar-house. The same owner text as H-2123, on a tablet from the F mound.
8. H-922 and H-923 (Harappa F- and F Trench I): 3 diamonds | 1(tall) spear. Hands 3, spear 1.
9. H-1882 (Harappa E-): opener-2 | 3 diamonds. Opener-2 front, then 3 hands.
10. H-854 (Harappa): front `003 335 740 400` = 3 [335] of-jar-house, tally; cup+2. The one 003-opening front with a cup count that is not 4.
11. H-2215 (Harappa E Trench 54, steatite): 3 cups | load | [lost]. Cup+3 with a bare load line (1 load).
12. H-1354 (Harappa F Trench VI, steatite, three faces): [415 pitchfork] [578] 2(tall) [824] | [799] two-leaf-840 [714] of-jar-house | 4 cups. Two owner fronts and a cup+4 line: same text on H-2246 (4 cups), H-2213 and H-2214 (3 cups; `799 840 760 740` and `415 578 032 824/876`). Four tablets share one two-front record with cup count 3 or 4: a standing delivery written for two parties.
13. H-1947 (Harappa E Trench 11, faience, three faces): 3 cups | 1(tall) [lost] of-jar-house | [630] of-jar-house. 3 cups against two jar-house lines.
14. H-847 (Harappa F Granery, faience): [690] | 3 cups | [415] [three-headed man] of-jar-house. Cup+3 in the granary area, owner front with the three-headed man.
15. H-987 (Harappa F Trench IV+V, faience): opener [365] [690] | 3 cups | sitting man [176] of-jar-house, tally. Sitting-man owner, cup+3.
16. H-355 (Harappa): sitting man of-jar-house tally | 3 cups | 3 cups. The same 3-cup line twice: a double issue.
17. H-358 (Harappa F Trench VI, steatite): [255] [435] load, tally | 4 cups | [lost] jar-house. Front ends in the load carrier without a number; cup+4.
18. H-2217 (Harappa E Trench 10W/11): 2 cups | 2(tall) [854] tally | [360] [257]. Cup+2 with a tally-closed front.
19. H-1353 (Harappa D-, steatite): [617] [lost] [480] staff-man [lost] | cup then 2 (`700 032`, cup written first) | [lost] cup. A cup+2 record in cup-first writing.
20. H-1946 (Harappa E Trench 10W/11, faience): 4 cups (written with the stacked four, `014 700`) | [144] | archer + cup (`125 700`, no number). Two cup lines, one numbered 4, one for the archer.
21. H-196 (Harappa F Trench III, faience): [072] jar [590 bin] [407 tree] | [706] [167] | 1(short) three-headed man cup 2(tall). A record of bin and tree property with a cup line.
22. M-1400 (Mohenjo DKG(S), clay): 2(opener) [368] of-jar-house [lost] [871] | [lost] cup [705] | [382]. Mohenjo cup record, cup first.
23. M-486 (Mohenjo HRB, clay): fish-hat spear | [lost] [255] | [615] of-jar-house, man. Three faces of fish and spear with an owner.
24. M-487 (Mohenjo DKG(S), clay): fish-hat spear | [lost] [165] [255] [435] | [lost] of-jar-house, man. Same record, longer second face.
25. M-1430 (Mohenjo DKG(S), clay): [384] jar | [384] jar | [384] jar. One text three times.
26. M-494 and M-495 (Mohenjo DKE / DKG(S), clay): face 1 `838 798 176 740 151 697 390` = [838] [leaf-pincer] sitting-man of-jar-house porter [697] tree-A (identical on both tablets); face 2 `255 070 741 150 221 840 032` / `070 741 150 267 840 032` = ... jar-dot ... two-leaf 2(tall); face 3 a long jar line. Two long three-face records sharing face 1; the second faces both end `840 032` (two-leaf, 2).

Next test this opens: other tablets in E Trench 11 with the standard line carry cup+4 (60 of 73 do); an E-11 tablet with cup+3 or cup+2 should have a different diamond or load count in its other faces.

## 7. What the counted things are

- Counted things split in three: measures (cup, jar, bin: full-height, tablets, Harappa, F2-F4), bundled units with a fixed number (load 3, sack 3, seven 7, dozen, the three-unit 705/706), and grown or worked goods with a number range (trees 3-8, fish 2-3 and 6, crop A-comb, rolled goods 3-5).
- The tablet is a ration or issue chit: cup count variable, other lines fixed at three.
- The seal carries the property counts: trees at the end, fish in the middle, crop loads at the end.
- The copper-tablet class (Mohenjo) is a goods list: seven, three, two on metal.
- Next tests it predicts: other tablet faces in E Trench 11 write `003 861` / `003 156` with the cup count 3 or 4 only; 838 and the other signs filling the crop slot between A-comb and carrier are further commodities; Lothal tags with 055 carry fish.
