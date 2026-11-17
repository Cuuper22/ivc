# The stand letter on unicorn seals: what it is, and what the animal is

Word-free job, 2026-11-17. Sign numbers, pictures, stand letters, animals, sizes and findspots only. Scripts, run in this order, each with its predictions in its top docstring written before its numbers: `work_scripts/stand_common.py` (loader), `stand_1_photos.py`, `stand_2_cutting.py`, `stand_3_places.py`, `stand_3b_recheck.py`, `stand_3c_rescue.py`, `stand_3d_crest.py`, `stand_4_cities.py`, `stand_5_text.py`, `stand_6_animals.py`, `stand_7_buildings.py`. Tables, photo sheets and logs: `work_data/stand/`.

## Plain words

- **Unicorn seal**: the square stamp seal showing the one-horned bull. In front of its head stands a small object on a post: the **stand**. Its parts: the **upper part** (usually a box or cage with ribs; on some stones a dome or a crescent), the **lower part** or **bowl** (a cup or basin, plain or patterned with rays, fronds, lobes or hatching) and the **shaft** (the post).
- **Stand letter**: the catalogue's one-letter code after `Bull1:` (W, J, S, I, L). 950 unicorn stones carry one.
- **Stand-drawing code**: a second catalogue column (called `cult` in the catalogue), three letters: first S, R or H, second A, B or C, third N or F. On the photos below, R marks a rounded or non-cage top (dome, globe, peak, crescent) and F a fringed or rayed bowl.
- **Neck folds**: the parallel ridges cut across the bull's throat and neck. **Saddle**: the double line drawn round the shoulder and chest; on some stones it is a **heart-shaped shoulder mark**. **Collar**: a band round the throat.
- **Household reading**: the letter is chosen by the family that holds the seal. **Workshop reading**: the letter is the drawing style of the shop that cut the stone.
- **Pair**: two unicorn stones from one city. **Share**: both carry the same letter. **Dealt**: letters shuffled at random among the unicorn letter stones of the same city (sometimes also the same size third), 2,000 times; **ratio** = real count / dealt mean; **P** = share of deals at least as extreme as the real count.
- **Building**: excavation area + house (Mohenjo-daro). **Block**: house block. **Room**: building + room or grid square. **Near / far depth**: two stones of one excavation area whose depths differ by 3 ft or less / by 6 ft or more.
- **Size third**: the smallest, middle or largest third of a city's stones by face area.
- **Text kinds** (frame v2): bare name, name + closer (ends jar 740, spear 520, porter), name + title (ends with an after-jar title such as man 090 or comb 400), name + closer + title, front formula (opens with a front word 861 / 817 / 820 / 920 ...), count line (numbers + a counted thing).
- **Holder**: one person's stone, taken as text + animal + stand letter.

## What was found

1. **The stand letter is a carving style of the whole picture, and the bull's drawing shows it better than the stand does.** On 60 photos (12 per letter, drawn by seed, judged with the letter hidden), the drawn shape of the stand does not follow the letter: the best stand kind per letter covers 17 of the readable stones against 15.6 when letters are dealt (P 0.25). The bull does follow it: style (neck folds yes/no x saddle yes/no) covers 23 of 39 against 16.6 dealt (P 0.002). Neck folds: I and W 18 of 22, J and S 6 of 22 (Fisher P 0.0007). All 4 heart-shaped shoulder marks in the sample are on W stones. In the full catalogue the letter goes with the stand-drawing code (top S/R/H: V 0.243 against 0.069 dealt within city; fringed bowl F: 0.208 against 0.071; both P below 0.001) and with size (0.307 against 0.066, P below 0.001), and does not go with the boss on the back (P 0.24), the material (P 0.17), the stone's thickness for its face (P 0.45) or its wear (P 0.10). Means: the letter is a label for a whole way of drawing the beast and its stand (a folded-neck, ornate, big W style; a folded-neck, plain-bodied I style that holds every odd stand top; smooth-necked J and S). The back, the stone and its proportion follow no letter, so the letter belongs to whoever drew the picture, not to whoever shaped the blank. Opens: the letter can be replaced by a finer, photo-based style code (neck, saddle, stand top, bowl) to sort stones by hand.

2. **Each city draws in its own style, and Mohenjo-daro stones whose texts read like Harappa texts are drawn in Harappa's style.** City mixes differ: W is 65% at Harappa, 40% at Mohenjo-daro, 48% at Lothal, 42% at Kalibangan, 32% at Dholavira (chi-square 79.5, P 5e-9). It is not size: inside each size third W is still Harappa's (small 40% against 20%, P 2e-6; middle 60% against 28%, P 0.0004; big 91% against 70%, P 0.024), and it holds in the middle bin (P 9e-5) and the late bin (P 0.003). Then the outlier test: a sign-count model scores how Harappa-like each text is (the stone itself left out). The 61 Mohenjo-daro unicorn stones with the most Harappa-like texts are W 62% of the time, Harappa's own rate (65%), against 37% for the rest of Mohenjo-daro and 42% expected from their sizes; 61 stones drawn at random from Mohenjo-daro reach that only 1 time in 1,000. Means: a stone with a Harappa-type text found at Mohenjo-daro was drawn in the Harappa manner: cut in, or by a cutter from, Harappa and carried. Opens: the letter (and the finer style code) flags travelled stones; the list is `work_data/stand/city_outliers.csv` (M-1662 to M-1724 in DK-B / DK-C, M-10 and M-34 in HR-A 1I, M-672, M-673, M-224 among them).

3. **One text line is drawn in one style in every city: the sign-405 stones are W.** Of 23 unicorn stones whose text carries sign 405 (a tree variant), 22 are W, against 14.3 when letters are dealt within city and size third (P below 1 in 4,000; the only cell of 900 in the text scan below 1 in 1,000). They lie at Harappa (11), Mohenjo-daro (9), Kalibangan, Lakhanjo-daro; several are the largest seals in the corpus (H-8 4,356 mm2, H-1657 3,249, M-10 2,333). The Kalibangan / Mohenjo-daro twins K-19 and M-224 (`005-405`), judged the same hand in the twins job, belong to this set. Means: the 405 texts were cut by one shop, or one school, in the big W style, wherever their holders lived. Opens: a named workshop line to follow (405 with box 590 and jar: `590-405-740` on H-479, M-672, Lakhanjo-daro).

4. **The text does not choose the style; nothing else does either.** 180 text features (kind, after-jar title, front word, 79 fixed phrases, each sign) x 5 letters, dealt within city and size third: 1 cell at P below 0.001 (0.9 expected), 10 at P below 0.01 (9.0 expected), none at q below 0.1 (the 405 cell has q 0.23); text kind P 0.27, titles and front words together P 0.34, phrases P 0.18. Smaller leans: after-jar man 090 on S 10 against 5.1 (P 0.02) and on W 9 against 14.1 (P 0.03), the same direction as the earlier finding that "X's man" seals carry S or J on 15 of 21. Means: the cutter's style ignores what the text says, exactly as the beast does; the one exception (405) is a whole text line going to one shop.

5. **The animal: size and text length go with it, time does not, and rare beasts are spread one to a building.** Square seals, size against the median of the same city and format: zebu +25% (43 stones, P 0.010), elephant +9% (P 0.20), unicorn +1%, short-horned bull -13% (P 0.023 for that small), goat -14%, tiger -11%, inscription-only -34%. Material goes with it only through the rare faience and clay stones (V 0.127 against 0.098; steatite 86% to 100% for every beast). Time bin: chance (V 0.102 against 0.103, P 0.53). Text kind: V 0.090 against 0.070 (P 0.008): goat seals are bare names 64% (the short Banawali texts), zebu front formulas 35%, tiger name + title 19%. Inside one building, two non-unicorn beast seals occur 91 times against 118 dealt within the city (P 0.067 for that few), and when they do, the same species 13 times against 20.8 (P 0.085). Means: a building seldom holds two rare-beast seals and almost never two of one rare beast; the rare beast behaves as one holder's own mark, the unicorn as the common default. Opens: a rare beast can stand for one person in a building's set of stones.

6. **Almost every stone is its own holder.** Mohenjo-daro: 1,318 inscribed stones, 1,241 different texts, 1,299 different text + animal + letter holders. Harappa 428 / 408 / 419; Dholavira 136 / 130 / 133; Lothal 89 / 88 / 89. The biggest crests at Mohenjo-daro: 235 has 54 stones, 52 texts, 54 holders in 37 buildings; 220 49 / 46 / 48 in 31; 240 38 / 35 / 37 in 24. Means: crest families are spread over the city, one stone per holder, never piled in one house.

## Photo description table

60 unicorn stones, 12 per letter, drawn by seed 20261117 from stones with a photo and catalogue condition not "Poor"; close-ups and whole views in `work_data/stand/stand_close_*.jpg` and `stand_whole_*.jpg`, the key in `stand_photo_key.csv`, my blind notes in `stand_photo_blind.csv` and `stand_photo_bull.csv`, joined in `stand_photo_unblind.csv`.

| letter | stands seen (readable of 12) | upper part | bowl | bull | is the letter right? | finer kinds inside |
|---|---|---|---|---|---|---|
| W | 8 | tall ribbed or checker-grid cage, sometimes with concave sides; one dome (M-224) | plain cup or bowl 4, patterned (spiky fan, drooping fronds, rays) 3, a second box 1 | neck folds 8 of 10; saddle outline on most; all 4 heart-shaped shoulder marks (H-407, H-386, H-47, M-224); big stones | right as a style: ornate, folded neck, big | plain-bowl W (H-62, M-160, M-699, H-386) against fringed-bowl W (H-407, H-47, M-224) |
| J | 12 | ribbed cage 7, small box with a cross or T 3, one dome, one peak | patterned (hatched, lobed, curled, rays) 5, plain cup 4 | smooth neck 9 of 12; saddle 6; collar 2 | right as a style: smooth neck with saddle | cage + patterned bowl (M-113, M-79, M-218, M-48) against small box + plain cup (M-228, H-450, M-209) |
| S | 9 | ribbed cage 7, small box 1 | patterned (fan, banded drum) 3, plain 2, a second box under the cage 2, armed bowl 1 | smooth neck 7 of 10; saddle 6; collar 2 | right as a style: smooth neck, plainer than J | double-box stand (H-499, M-817) is a kind of its own |
| I | 11 | dome or globe 3 (all Kalibangan: K-10, K-17, K-23), crescent on an arrow 1 (M-741), peak 1 (M-214), small box 3, cage 2 | plain cup 4, patterned 3 | neck folds 10 of 12, no saddle 8 of 12; plain body | right as "the other stands": every odd stand top in the sample is I | the Kalibangan dome stand is a local kind; the crescent-arrow stand is unique |
| L | 5 | cage 3, small box 1 | plain 3, patterned 1 | 8 of 12 bulls too worn or dark to judge | not testable on these photos: 7 of 12 stands unreadable against 0 to 4 for the other letters | none seen |

Read: no letter is one stand shape. Plain-bowl and patterned-bowl stands, cage tops and box tops occur under W, J and S alike. The catalogue's stand-drawing code catches the shape (R = rounded or odd top: 4 of my 5 domes and the crescent are R; F = fringed bowl: 5 of 5 readable F stands have a patterned bowl), while the letter sorts the whole drawing, chiefly the bull's neck.

## Household against workshop: the deciding numbers

Predictions were fixed in `stand_3_places.py` before the run (household: same building far in depth shares as much as near; neighbours share little; workshop: same time beats same building).

| pairs | pairs | share | dealt (city) | ratio | P | dealt (city x size third) | ratio |
|---|---|---|---|---|---|---|---|
| same room | 104 | 31 | 28.1 | 1.10 | 0.29 | 28.6 | 1.09 |
| same building, near depth | 687 | 203 | 191.5 | 1.06 | 0.22 | 192.4 | 1.06 |
| same building, far depth | 196 | 55 | 54.2 | 1.01 | 0.48 | 56.7 | 0.97 |
| other building same block, near depth | 1,087 | 322 | 321.1 | 1.00 | 0.47 | 321.8 | 1.00 |
| other building same block, far depth | 850 | 188 | 259.0 | 0.73 | 1.00 | 251.7 | 0.75 |
| other block same area, near depth | 9,909 | 2,690 | 2,765 | 0.97 | 0.79 | 2,694 | 1.00 |
| other area, same time bin | 40,332 | 11,967 | 11,812 | 1.01 | 0.26 | 11,744 | 1.02 |
| same building, same crest | 27 | 5 | 7.3 | 0.69 | 0.89 | 9.0 | 0.56 |
| same building, different crests | 1,140 | 342 | 316.0 | 1.08 | 0.10 | 314.4 | 1.09 |
| same crest, other building, same city | 1,758 | 496 | 500.2 | 0.99 | 0.56 | 510.4 | 0.97 |

With labels cleaned (L and worn stones out, `stand_3c_rescue.py`): same building near depth 148 of 389 against 122.6 (ratio 1.21, P 0.0085); same building far depth 38 of 120 against 36.8 (1.03); other building same block near depth 0.99; other block same area near depth 0.93. The two-style axis (folded neck I + W against smooth J + S): same building 545 of 1,007 against 509.6 (1.07, P 0.022), far depth 1.02.

Same crest in different cities (`stand_3d_crest.py`, lost-sign crest removed, letters dealt within city and size third): 587 of 1,800 pairs share against 500.5 (ratio 1.17, P 0.0025). It is carried by the fish crests and 803: crest 220 (35 stones, 5 cities, W 20), 235 (32 stones, W 18), 803 (25 stones, W 15); per-crest table `work_data/stand/crest_crosscity.csv`. Inside Mohenjo-daro the same crests in other buildings are at chance (0.99). Read in the workshop frame: a great house's stones in different cities tend to come out of the same manner (W), the pattern expected if such a house had its seals cut by one school and carried them (the Harappa-type W stones at Mohenjo-daro of finding 2); read in the household frame it would be a lineage taste. This went against my fixed prediction (about 1).

Twins (identical texts on two stones): same city, other building, same letter 9 of 22 against 6.4 from the cities' letter mixes; different cities 5 of 29 against 8.4. Same-hand twin pairs (photo-judged in the twins job): 1 of 3 share the letter (K-19 / M-224, W and W; H-451 / M-879 W and J; M-187 / M-193 S and W).

What these say: the letter is not a lineage mark (same crest in other buildings 0.99; same crest in one building 0.69) and not a long-lived house mark (same building far in depth 1.01 to 1.03). Its one local pull is a house at one moment (same building, same depth, clean labels 1.21): the stones a household had cut at one time came from one hand. The wide pulls are the city (city mixes, P 5e-9, inside size thirds) and the text line (Harappa-type texts at Mohenjo-daro, the 405 line). Verdict: **the letter is a workshop style. A city's shops each had their manner; a household at one time went to one shop; a stone cut in Harappa and carried to Mohenjo-daro keeps Harappa's manner.** The household reading of the letter is paused (reason in "What went against").

## What the stand is, and what the animal is

- **The stand letter** = the hand or shop that drew the picture. Numbers that decide: bull style follows the letter (23 of 39 against 16.6, P 0.002) while the stand shape does not (P 0.25); city mixes differ inside every size third (P 2e-6 to 0.024); Harappa-like texts at Mohenjo-daro carry Harappa's W rate (62% against 37%, P 0.001); the 405 text line is W in every city (22 of 23); same building across generations at chance (1.01).
- **The animal** = the holder's own mark, chosen per stone. The unicorn is the common default (1,248 of 1,651 stones with a beast or scene in the corpus); a rare beast is spread one per building (91 rare-beast pairs in a building against 118), is never repeated on the identical text (0 of 45 in the twins job), and goes with size (zebu +25%) and text length (goats on short bare names), not with time (P 0.53), crest, ending or area.
- **The stand drawing itself** (the catalogue's second code: cage or rounded top, plain or fringed bowl) is a detail inside a shop's style; the rounded and odd tops cluster in I and at Kalibangan.

## The 40 Mohenjo-daro buildings with the most seals

Class rule fixed before the run (`stand_7_buildings.py`): HOUSEHOLD = more same-crest pairs than random draws of the same size from the city (P at or below 0.10) and species at or above chance; OFFICE = crests at chance and count lines + front formulas above chance (P at or below 0.10); SHOP = one letter above chance (P at or below 0.10) with crests at chance; ORDINARY = none. At P 0.10 about 4 buildings per class are expected by chance alone.

Result: 29 ORDINARY, 5 SHOP, 3 OFFICE, 3 HOUSEHOLD. Pooled over the 40: same-crest pairs 40 against 34.0 for same-size random draws (ratio 1.18); same-letter pairs 281 against 227.4 (ratio 1.24, draws not matched on unicorn share or depth).

| building | seals | depth span ft | crests | commonest crest | same-crest pairs (draws) | species (draws) | animals | letters | count line + front share | class |
|---|---|---|---|---|---|---|---|---|---|---|
| DKG First Street | 34 | 16.9 | 26 | 390 | 3 (5.3) | 7 (6.8) | unicorn 24, none 2, short-horned 2, zebu 2, tiger, multi-headed, scene | W 7 S 3 J 2 L 2 I 1 | 0.35 | ORDINARY |
| DKE Trench E | 34 | 8.0 | 21 | 235 | 9 (5.2) | 6 (6.8) | unicorn 24, none 4, rhinoceros, bull, zebu, elephant | J 9 W 6 S 4 I 2 L 1 | 0.50 | OFFICE |
| DKG(N) 18 | 26 | 6.6 | 21 | 233 | 3 (3.1) | 6 (5.9) | unicorn 19, elephant 2, short-horned, zebu, none, composite | J 7 L 4 S 3 W 2 I 1 | 0.19 | ORDINARY |
| DKG(S) 1I | 25 | 12.2 | 18 | 240 | 6 (2.7) | 6 (5.8) | unicorn 13, none 7, zebu, elephant, composite bull, goat | W 8 J 2 I 1 | 0.28 | HOUSEHOLD (W-heavy too, letter P 0.017) |
| DKG(S) Crooked Lane | 17 | 12.4 | 16 | 798 | 1 (1.3) | 2 (4.7) | unicorn 9, none 8 | S 3 I 2 J 2 W 1 | 0.35 | ORDINARY |
| DKG(S) 7V | 17 | 15.2 | 15 | 260 | 0 (1.2) | 5 (4.8) | unicorn 10, none 4, plant-beast, bull, short-horned | W 7 I 1 J 1 S 1 | 0.12 | SHOP (W) |
| DKG(S) Loop Lane | 15 | 12.5 | 11 | 156 | 1 (1.0) | 4 (4.5) | unicorn 10, none 3, zebu, short-horned | J 4 S 3 I 1 W 1 | 0.20 | ORDINARY |
| DKG(S) 1III | 15 | 11.6 | 14 | 415 | 1 (1.0) | 3 (4.5) | unicorn 11, none 3, other | W 5 L 2 J 1 I 1 S 1 | 0.53 | OFFICE |
| DKG(S) 7III | 14 | 17.0 | 9 | 503 | 0 (0.8) | 6 (4.3) | unicorn 6, none 3, bull 2, short-horned, buffalo, composite bull | W 2 I 1 S 1 J 1 | 0.14 | ORDINARY |
| DKG(S) 8III | 14 | 8.6 | 10 | 390 | 0 (0.8) | 5 (4.4) | unicorn 9, none 2, short-horned, rhinoceros, bull | J 4 W 2 S 1 | 0.14 | ORDINARY |
| DKG(S) 4 | 14 | 14.5 | 11 | 220 | 4 (0.8) | 4 (4.4) | unicorn 10, none 2, buffalo, tiger | W 3 S 2 J 1 I 1 | 0.29 | HOUSEHOLD |
| DKG(S) 7I | 14 | 22.2 | 11 | 175 | 0 (0.8) | 3 (4.3) | unicorn 11, rhinoceros, elephant | W 3 L 2 S 2 I 1 | 0.21 | ORDINARY |
| DKG(S) 12V | 14 | 11.4 | 9 | 140 | 4 (0.8) | 6 (4.3) | unicorn 8, none 2, short-horned, zebu, elephant, bull | J 2 L 1 S 1 W 1 I 1 | 0.36 | HOUSEHOLD |
| DKG(S) 9VIII | 14 | 10.6 | 10 | 061 | 1 (0.9) | 5 (4.3) | unicorn 8, none 2, zebu 2, composite, gharial | W 3 S 2 J 2 I 1 | 0.36 | ORDINARY |
| DKC 8 | 13 | 7.5 | 11 | 877 | 0 (0.7) | 7 (4.1) | unicorn 5, none 3, bull, tiger, composite, short-horned, zebu | J 1 S 1 W 1 | 0.23 | ORDINARY (7 species, most varied) |
| DKG(S) 10I | 11 | 7.3 | 10 | 235 | 0 (0.5) | 3 (3.8) | unicorn 9, bull, elephant | J 4 W 4 S 1 | 0.27 | ORDINARY |
| DKC 12 | 10 | 4.5 | 7 | 235 | 1 (0.4) | 3 (3.6) | unicorn 7, elephant 2, none | W 4 S 1 J 1 | 0.40 | ORDINARY |
| DKG(S) 7II | 10 | 14.5 | 6 | 240 | 1 (0.4) | 3 (3.7) | unicorn 8, short-horned, none | W 3 J 2 S 1 L 1 | 0.40 | ORDINARY |
| DKG(S) Long Lane | 10 | 15.8 | 6 | 503 | 1 (0.4) | 5 (3.7) | none 4, unicorn 3, zebu, goat, short-horned | W 1 J 1 | 0.30 | ORDINARY |
| HRA 1I | 10 | 9.3 | 9 | 240 | 0 (0.4) | 2 (3.7) | unicorn 6, none 4 | W 5 J 1 | 0.10 | SHOP (W; M-10, M-34, sign 405, median 930 mm2) |
| DKC 10 | 10 | 4.0 | 8 | 070 | 0 (0.4) | 3 (3.6) | unicorn 6, short-horned, none | S 3 I 1 W 1 J 1 | 0.20 | ORDINARY |
| DKG(S) 9VII | 10 | 9.8 | 6 | 416 | 0 (0.4) | 4 (3.6) | unicorn 4, none 3, short-horned 2, tiger | S 1 I 1 | 0.20 | ORDINARY |
| DKC 11 | 9 | 7.5 | 8 | 806 | 0 (0.3) | 3 (3.4) | none 4, unicorn 3, zebu | I 1 J 1 L 1 | 0.00 | ORDINARY |
| DKG(S) 9IX | 9 | 3.6 | 9 | 527 | 0 (0.3) | 4 (3.4) | unicorn 5, none 2, bull, short-horned | W 4 J 1 | 0.33 | SHOP (W) |
| DKG(S) 7VIII | 9 | 14.5 | 8 | 220 | 1 (0.3) | 2 (3.4) | unicorn 8, none | J 4 S 2 I 1 | 0.22 | ORDINARY |
| DKG(S) 10III | 9 | 17.7 | 5 | 176 | 1 (0.3) | 3 (3.5) | unicorn 4, none 4, short-horned | W 2 J 2 | 0.33 | ORDINARY |
| DKG(S) 1IV | 9 | 14.4 | 8 | 705 | 0 (0.3) | 3 (3.5) | unicorn 6, none 2, scene | W 2 I 1 S 1 | 0.00 | ORDINARY |
| DKD Trench D | 8 | 5.0 | 8 | 279 | 0 (0.3) | 2 (3.3) | unicorn 6, none 2 | W 4 S 1 | 0.00 | SHOP (W, median 869 mm2) |
| DKG(S) 9I | 8 | 10.1 | 8 | 698 | 0 (0.3) | 3 (3.3) | none 4, unicorn 3, buffalo | S 2 L 1 | 0.25 | ORDINARY |
| DKG(N) 22 | 8 | 5.7 | 6 | 921 | 0 (0.3) | 2 (3.2) | unicorn 6, bull | W 2 J 1 S 1 | 0.50 | ORDINARY |
| DKG(S) 10IV | 8 | 9.8 | 6 | 097 | 0 (0.3) | 3 (3.3) | unicorn 5, none 2, elephant | I 1 J 1 S 1 | 0.12 | ORDINARY |
| DKG(S) 3VI | 8 | 9.6 | 6 | 458 | 0 (0.2) | 3 (3.2) | unicorn 5, none 2, short-horned | J 2 I 1 | 0.62 | OFFICE |
| DKG(S) 7IX | 8 | 10.3 | 7 | 235 | 1 (0.3) | 3 (3.3) | unicorn 6, zebu, none | J 2 S 1 W 1 | 0.50 | ORDINARY |
| VSA 2VIII | 8 | 3.0 | 7 | 741 | 1 (0.3) | 3 (3.2) | unicorn 5, none, zebu | W 4 | 0.25 | SHOP (W 4 of 4, median 1,354 mm2) |
| DKG(S) 9III | 7 | 15.4 | 7 | 503 | 0 (0.2) | 3 (3.0) | none 3, unicorn 2, short-horned 2 | J 1 W 1 | 0.14 | ORDINARY |
| DKG(S) 1VI | 7 | 15.0 | 7 | 220 | 0 (0.2) | 3 (3.0) | unicorn 5, none, composite bull | J 1 W 1 I 1 S 1 | 0.43 | ORDINARY |
| DKG(S) 9AV | 7 | 11.3 | 6 | 803 | 0 (0.2) | 6 (3.0) | none 2, scene, tiger, other, zebu, unicorn | none | 0.14 | ORDINARY (6 species in 7 stones) |
| DKE Trench EII | 7 | 6.5 | 4 | 350 | 0 (0.2) | 3 (3.0) | unicorn 5, plant-beast, zebu | J 1 L 1 | 0.43 | ORDINARY |
| VSA 2XVI | 7 | 8.0 | 7 | 803 | 0 (0.2) | 2 (3.0) | unicorn 5, none 2 | W 2 S 1 I 1 J 1 | 0.14 | ORDINARY |
| DKG(N) 13III | 6 | 4.7 | 3 | 235 | 0 (0.2) | 4 (2.8) | unicorn 2, elephant 2, rhinoceros, triple-beast | W 1 | 0.17 | ORDINARY |

What they look like: the big buildings are mixed sets of single holders. A building's stones span 4 to 22 ft of depth (several generations), carry 3 to 26 different crests, and almost never two stones of one text; three buildings hold a family (DKG(S) 1I, DKG(S) 4, DKG(S) 12V: 4 to 6 same-crest pairs against under 3), and five hold mostly big W stones (DKG(S) 7V, HR-A 1I, DKG(S) 9IX, DK-D Trench D, VS-A 2VIII), which in the workshop reading are buildings whose holders had their seals cut in the big-W manner (median face 869 to 1,354 mm2 in three of them). None looks like an office in the sense "varied texts, one stand": the three OFFICE buildings are mixed in letter. Full table: `work_data/stand/buildings_md40.csv`.

## What went against

- **The old house-mate result for the letter does not survive a correct count.** The earlier figure "same room 38.1% against 17.2%" (animal job, `animal_4_pairs.py`) came from two faults: the table had one row per FACE, so two faces of one stone were counted as a pair that always shares; and the letters were dealt among all beast seals, so dealt letter pairs often received a blank. Reproduced: 38.8% against 21.6%. Counted once per stone and dealt only among letter stones: same room 29.8% against 27.1% (104 pairs, ratio 1.10, P 0.30); same building 29.4% against 27.4% (P 0.13) (`stand_3b_recheck.py`). The distance fade (room 1.79, block 1.27, area 1.13) and "independent of crest" rested on the same table. Redesign 1 (clean labels, depth window): same building near depth 1.21 (P 0.0085), far depth 1.03, so a same-time household pull is left and a lasting house mark is not. Redesign 2 (new idea, the folds / smooth axis): building 1.07 (P 0.022). The household reading of the letter is paused: three ways in (room, cleaned building + depth, style axis) give at most a same-time pull of 1.07 to 1.21, which the workshop reading also predicts (one household, one shop, one moment).
- The twins-job figure "same city other building share 9 of 22 against 4.9" used a low chance figure; against the cities' own letter mixes it is 9 against 6.4.
- My committed prediction that neighbours at the same depth share as much as house-mates went against: other building, same block, near depth 1.00 (and 0.99 on clean labels). The workshop is a city-wide manner and a text line, not a neighbourhood.
- Same-hand twins share the letter only 1 of 3 (prediction was 4 or more of the same-hand unicorn pairs; there are only 3). Rescue: the hand judged in the twins job is the hand of the TEXT; the beast can be drawn by another hand in the same shop. Next test: judge the beast's hand separately on the same pairs.
- The text-home score is partly a W detector: inside Harappa its upper half is W 71% against 59% for its lower half. Inside Mohenjo-daro (outside the top tenth) it has no pull at all (Spearman -0.005), so the top-tenth jump to 62% is not just a W-text effect, but part of it may be.
- Animal avoidance in a building is a lean, not a clean number: same rare species 13 against 20.8 (P 0.085); species counted per building are at chance (358 against 359). Same crest and same building share the animal more than chance, not less (48 of 73 against 40.2): family members did not pick different beasts; they mostly took the unicorn.
- Thickness goes with the letter only through size (proportion P 0.45).
- Same crest across cities shares the letter 1.17 (P 0.0025), against my prediction of about 1; it is the one number the household (lineage) reading can claim. Rescue in the workshop frame (above): the fish houses' W stones are the travelled Harappa-manner stones. Split test: photo-compare the W stones of crests 220 and 235 at Mohenjo-daro with Harappa W stones; a lineage taste predicts W in each city's own manner, a travelled school predicts Harappa's manner (heart-shaped shoulder, fringed bowl) at both.
- Building classes are at the chance level (about 4 per class expected at P 0.10): 5 SHOP, 3 OFFICE, 3 HOUSEHOLD.

## What each reading predicts that has not been checked

- Workshop: a photo-based style code (neck folds, saddle, stand top, bowl, horn curve) should sort stones more finely than the letter, and stones of one fine style should cluster in time (one cutter's working life, about one depth band) and in a city, but not in one building over generations. A cutter's hand on the beast should repeat across texts; the same-hand twin pairs should be rejudged on the beast alone.
- Workshop: the 405 W stones should share fine traits (same neck-fold count, same stand) across Harappa, Mohenjo-daro and Kalibangan.
- Workshop: the Harappa-type W stones at Mohenjo-daro (M-1662 to M-1724, M-10, M-34) should look like Harappa W stones in photos (heart-shaped shoulder, fringed bowl) more than like Mohenjo-daro W stones.
- Household (paused): if any house mark exists on the stone it should be found in the fine style code within one depth band of one building; the 1.21 same-time pull is the only ground left for it.
- Animal: if a rare beast is a holder's personal mark, the same holder's other objects (tags stamped with his seal) should never show a different beast with the same text; impressions with a rare beast should trace to one stone.
