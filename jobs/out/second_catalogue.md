# The readings on the second catalogue (Mahadevan 1977)

Scripts: `work_scripts/mah_common.py` (loaders), `crosswalk_em.py`, `crosswalk_build.py` (crosswalk), `second_measure.py` (step 2), `second_port.py` (steps 3 and 4). Files: `work_data/lipi_mahadevan_crosswalk.csv`, `crosswalk_text_pairs.csv` (every matched text pair), `mahadevan_parsed.csv` (every Mahadevan line with its parse and gloss), `mahadevan_glyphs/` (all 417 sign pictures from indusscript.in/assets/images). Mahadevan lines are stored in reading order (the jar 342 is the last sign in 850 of 1,224 texts and first in 0, for left-to-right lines too: 30 against 0). Site comes from the text-number ranges in his codebook; object class from `inscobj`; picture from `fs80` read as field-symbol code plus one sub-type digit (13 = code 01 unicorn, sub-type 3).

## What carried over

1. The crosswalk builds itself from whole texts. 2,332 Lipi texts line up with a Mahadevan text of the same length at the same site; the matching, run with no seeds at all, returns all 14 given matches (jar 740=342, 002=99, diamond 861/817=267, wheel 820=391, cup 700=328, fish 220=59, long strokes 031-035 = 86, 87, 89, 95, 96, comb 400=176, porter 156=15). 366 pairs, 312 Lipi signs, 230 Mahadevan signs; 86% of Lipi sign occurrences and 96.6% of Mahadevan sign occurrences are covered. Seeded and seedless runs agree on the top partner for 124 of 126 Lipi signs. 167 Lipi signs have 5 or more supporting positions, 71 have 20 or more.
2. The man sign is Mahadevan 1 (picture checked: stick figure). Three-headed person 100 = 8, branching U 760 = 347, spear 520 = 211, crop 806 = 389, leaf 803 = 387, box 590 = 249, tree 390 = 162, whisker fish 240 = 67, hat fish 235 = 65, barred fish 233 = 72, dotted fish 231 = 70, cap 060 = 123, 920 = 293, jar-dot 741 = 343, table-X 679 = 139, barred rectangle 621 = 242.
3. Short strokes: Mahadevan 97/98 one, 99/100 two, 102 three, 104 four, 106 five, 108 six, 110 seven, 112 stacked seven; tall strokes 86/87/89/95/96 one to five.
4. The parser runs on Mahadevan and holds its rate: 1,721 of 1,928 distinct complete texts (89.3%) get a full role parse (Lipi, same rule, same filter: 1,948 of 2,153, 90.5%). The 383 texts with no Lipi partner at all (never seen by the crosswalk) parse at 85.4%; see section 3.
5. Both counting systems carry over with the same split (section 2e). The load tag, the jar-man possessive, the spear and porter in the jar's place, the opener, the cup counts and the front/back pairing of cup tablets are all there in the second catalogue with the same numbers within a few points.

## 1. Crosswalk (`work_data/lipi_mahadevan_crosswalk.csv`)

Method: every Lipi text without a broken edge is compared with every Mahadevan text of the same length at the same site group (Mohenjo-daro, Harappa, everything else). A pair scores the product over positions of T(m|l)/f(m), times a bonus when a repeated sign repeats in the same positions; T is re-fitted from the posterior-weighted positions, 14 rounds. A pair is kept at posterior 0.5 or more. The CSV gives each pair with: how it was found, text positions, distinct Lipi texts, objects, share of the Lipi sign's positions, positions found in the seedless run, occurrences on both sides, and the Lipi shape.

Many-to-one merges Mahadevan makes (Lipi to Mahadevan): 861 and 817 to 267 (the diamond is one sign in both); porters 153, 154, 155, 156, 157, 158 to 15 and 151 to 12; A-comb variants 467, 468, 470, 472, 475 to 178; 405, 406, 407, 409 to 169; 705 and 706 to 336. The pictures in `mahadevan_glyphs/` confirm each of 1, 15, 99, 176, 267, 328, 342, 347, 391. Pairs below 2 positions are not written. 187 Mahadevan signs, all rare (3.4% of occurrences), have no Lipi partner yet; they enter the port as unknown name-slot signs (X-numbers).

## 2. Each reading, Lipi numbers next to Mahadevan numbers

Counts are distinct complete texts (site, object class, sign string), reading order.

a. Load tag (`A-comb, crop, porter`).
- Lipi `465-475 + 806 + 154/158`: A-comb then crop 25, porter after the crop 24 of 25. Mahadevan `178 + 389 + 15`: A-comb then crop 15, porter after 14 of 15.
- The porter after the crop stands after an A-comb 24 of 24 in Lipi, 14 of 14 in Mahadevan; after a short stroke or anything else 0 and 0. Porter only after the count holds.
- The 11 A-variants are one sign: Mahadevan draws them as one sign (178).

b. Ration tablets.
- Cup counts on two-face tablets (long stroke + cup): Lipi 2, 3, 4 = 71, 104, 100, one 1, two 6, never 5. Mahadevan: 2, 3, 4 = 62, 96, 47, one 1, never 5 (0 of 206).
- Three diamonds / three porters / four cups: Lipi 22 objects with 3-diamond and 3-porter faces, 21 with cup+4. Mahadevan has no such object (3-diamond faces 0, `102 15` faces 2, both paired with a plain fish `59`). The batch is the Harappa E-trench-11 tablets excavated 1986 on (Lipi H-2218 to H-2239), which Mahadevan (Vats 1940 for Harappa) does not hold. This reading cannot be measured in the second catalogue.
- The cup count follows the findspot in both: Mahadevan Harappa locus 42 gives cup 2/3/4 = 15/38/19, locus 53 gives 11/11/1.
- Front against back: `176-740-400` (Mahadevan `48 342 176`) goes with cup+3 in 21 of 32 in Lipi and 23 of 36 in Mahadevan (cup+4 in 11, cup+2 in 2). `171 59 211` goes with cup+4 in 3 of 3.

c. Jar possessive and the man sign (seal texts).
- Jar is the last sign: Lipi 541 of 673 texts (80%), Mahadevan 603 of 793 (76%).
- Man follows the jar: 48 of 65 uses (74%) in Lipi, 53 of 72 (74%) in Mahadevan. Texts with the man sign that carry jar + man: 75% and 79%.
- Round seals abroad (Mahadevan West Asian finds, 18 lines): man sign 1 in 3 texts, jar and man together 0; the single stroke is present; too few lines to say more.

d. Spear and porter stand in the jar's place.
- Spear after a jar: 0 of 149 (Lipi), 0 of 156 (Mahadevan). Porters after a jar: 2 of 113 and 7 of 124 (the 7 are mostly the jar-porter 12). The spear is the last sign in 132 and 134 texts.

e. Names, and the two counting systems.
- Names of 2+ signs (through the crosswalk, same parser): open with a fish crest 154 of 816 (19%) Lipi, 157 of 792 (20%) Mahadevan. The four fish crests are four different signs in Mahadevan too (65, 67, 70, 72). Tag 760 is last in its name 55 of 64 (Lipi), 63 of 71 (Mahadevan); three-headed person 100 last 61 of 75 and 59 of 73.
- Tall strokes count containers; short strokes count living things. Short / tall counts directly before the sign. Cup: Lipi 6 / 26, Mahadevan 0 / 24. Jar: 11 / 47 and 12 / 34. Box: 9 / 18 and 7 / 11. Tree: 63 / 5 and 47 / 5. Whisker fish: 38 / 7 and 39 / 5. Crop: 17 / 1 and 19 / 1. Woman: 15 / 2 and 16 / 0. Plain fish splits both ways in both (43 / 54 and 47 / 53).

f. Openers.
- Seals that open with the diamond or wheel: 290, then two strokes in 228 (79%) in Lipi; 306 and 241 (79%) in Mahadevan. After the diamond Mahadevan has 99 (two) 234 times, 402 (vertical-stroke crest) 23. The wheel takes one stroke (97/98) 18 times and tall two (87) 6 times: the wheel counts one and tall two, as in Lipi.
- Cap `920-060`: Mahadevan `293 123` occurs 51 times, text-initial in 51 of 51 (Lipi 115 of 118), and `123 293` once.

## 3. The parser on Mahadevan (`second_port.py`)

Each Mahadevan line is turned into Lipi numbers through the inverse crosswalk (porter 15 becomes the load-carrier 158 after a crop and 156 elsewhere; unmapped signs become unknown name-slot signs) and run through `gloss2.parse_face` with the lexicon learned on Lipi.

Distinct complete texts of 2+ signs: 1,928; full role parse 1,721 (89.3%), tight names 1,546 (80.2% strict). Lipi on the same rule: 90.5%.

| site | texts | parsed | % |
|---|---|---|---|
| Mohenjo-daro | 1,110 | 970 | 87.4 |
| Harappa | 560 | 521 | 93.0 |
| Chanhu-daro | 66 | 61 | 92.4 |
| Lothal | 91 | 84 | 92.3 |
| Kalibangan | 67 | 59 | 88.1 |
| other sites | 21 | 17 | 81.0 |
| West Asian finds | 13 | 9 | 69.2 |

| object class | texts | parsed | % |
|---|---|---|---|
| seal | 1,397 | 1,217 | 87.1 |
| sealing | 265 | 247 | 93.2 |
| miniature tablet | 133 | 132 | 99.2 |
| pottery graffito | 53 | 52 | 98.1 |
| copper tablet | 37 | 31 | 83.8 |
| ivory/bone rod | 18 | 18 | 100 |
| bronze implement | 12 | 11 | 91.7 |
| miscellaneous | 13 | 13 | 100 |

Texts that have a Lipi partner: 1,545, 90.2%. Texts with no Lipi partner (383, objects the Lipi side never saw): 327 parse, 85.4%; by site Mohenjo-daro 82.1% (223 texts), Harappa 92.2% (102), Lothal 95.7% (23), Kalibangan 90.9% (11), Chanhu-daro 80.0% (15). Untight texts: 30 of 207 fail on a lost or tail sign, 37 of 207 carry an unmapped sign. The template stands on objects it was not built from at 85.4% overall (80% to 96% by site).

## 4. What Mahadevan has that Lipi lacks

- Picture code. Seal texts with a picture: 1,241, of which 910 unicorn (code 01), 76 short-horned bull (04), 50 humped bull (03), 32 elephant (07). Class (relation) sign against picture: chi2 40.4 against 31.6 by shuffling, p 0.18 (n 248): no link, as in Lipi (Cramér V 0.098, p 0.18). In the table the spear closes 81 of the 197 unicorn seals shown and 7 of 15 short-horned bull seals; the man 40 and 2. First name sign against picture: chi2 359.7 against 307.1, p 0.053 (n 554), the same direction as Lipi (first sign with animal, V 0.208, p 0.0035), weaker because 73% of picture-coded seals carry the unicorn.
- Locus and level. Mahadevan's locus is a code with 59 values over all sites (median 6 texts, maximum 290), not a house or room. Pairs of seals at one site and locus within 3 ft of level sharing the first name sign: 442 of 24,734 against 448 by shuffling; last name sign 577 against 548 (max 628 in 100 shuffles). At the same level: first sign 120 of 6,285 pairs against 113.7, last sign 163 against 143. House-mates share the last name sign slightly more often than chance (1.1 to 1.3 times) and the first name sign not at all. Room-level sharing (Lipi: 5 pairs against 0.73) cannot be tested here.

## 5. Where it comes out differently, and the adjusted reading

1. Comb after the jar. Lipi: 10 of 66 comb uses on seals follow the jar (15%); Mahadevan 46 of 144 (32%). The comb is the last sign in 114 Mahadevan seal texts. Adjusted reading: after the jar come two nouns of about equal rank, the man (53) and the comb (46). The comb is the second head noun in the same slot as the man, not only a rod-size tag; the earlier statement that the comb after the jar marks the smallest seals stands for Lipi sizes and has no size column in Mahadevan to test.
2. The porters. Mahadevan has one porter sign (15) for Lipi 153 to 158 and a separate 12 for 151. The 156 = three-strokes porter, 154/158 = leaf-tree porter split is a Lipi drawing split. Adjusted reading: one porter word; the choice between the three-count and the crop-count frames is made by the sign before it (3 strokes or A-comb + crop), which is what the data show: 15 after a crop only after the A-comb, 14 of 14.
3. The 4:3 standard tablet is absent. Mahadevan Harappa tablets peak at cup+3 (96 of 205), where the E-trench-11 batch in Lipi peaks at cup+4. The adjusted reading: cup+4 is the count of one batch; cup+3 is the common count of the Vats-excavated tablets; counts follow the trench in both catalogues.
4. Picture and first name sign: weaker in Mahadevan (p 0.053 against 0.0035). Adjusted: the link holds in direction; the 910-unicorn majority leaves only about 330 informative seals.
5. Locus is an area code. The house-mate tests need Lipi's block-house field; the second catalogue gives only a weak same-area excess for the last name sign.
