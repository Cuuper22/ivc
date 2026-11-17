# Twins: what is a text, and what is a stone

Word-free job, 2026-11-17. Sign numbers, pictures, jobs, animals and findspots only. Scripts (run in this order): `work_scripts/twins_common.py` (loader), `twins_1_build.py`, `twins_2_chance.py`, `twins_3_vary.py`, `twins_4_more.py`, `twins_5_photos.py`, `twins_6_redesign.py`. Each has its predictions in its top docstring, written before its numbers. Tables and logs: `work_data/twins/` (`seals.csv`, `members.csv`, `sets.csv`, `mah_sets.csv`, `union_sets.csv`, `chance_by_length.csv`, `pairs.csv`, `vary.csv`, `building.csv`, `kinds.csv`, `holders.csv`, `backs.csv`, `one_holder.csv`, `near_twins.csv`, `photo_pairs.csv`, `photo_tally.csv`, `photo_sheet_1.jpg` to `_6.jpg`, `log_1.txt` to `log_6.txt`).

## Plain words

- **Seal**: the carved stamp. Tablets, tags, sealings and pots are left out. **Face**: one inscribed side.
- **Complete text**: a seal face with no lost sign and no break flag in the first catalogue (Lipi). 1,540 faces on 1,506 seals.
- **Twin set**: two or more different seals (different object ids) with the identical complete text, sign for sign. **Twin pair**: two stones from one twin set. **Near twin**: two texts of 3+ signs, same length, one sign different.
- **Stand letter**: the catalogue letter (W, J, S, I, L) for the stand drawn in front of the unicorn. **Holder**: animal + stand letter, the marks on the stone outside the text.
- **Format**: square seal with a beast, or the long rectangular "bar" seal with text only (inscription-only), round, cylinder.
- **Boss**: the knob on the back. Catalogue code: first letter P = pierced, N = not pierced; second letter B = boss, N = no boss.
- **Kinds of text** (from the frame-v2 job of each sign, `work_data/frame/corpus_jobs.csv`): *count line* (numbers + a counted thing, with or without a front word); *front formula* (starts with a front word such as 861/817/820/920, then a name); *name + closer* (ends in jar 740, spear 520, porter 151-158); *name + closer + title* (ends closer + after-jar title such as man 090); *name + title*; *bare name* (no closer, no title); *front alone*.
- **Dealing**: the attribute in question is shuffled at random among all complete seals of the same site and the same text length (sometimes also the same format), 2,000-5,000 times, with the twin pairs held fixed. **Ratio** = real count / dealt mean. **P** = share of deals at least as extreme as the real count in the stated direction; small P = not chance, in that direction.
- **Time bins**: early / middle / late from `work_data/time/time_axis.csv` (before about 2200 BC, about 2200-2050, after about 2050).

## What was found

1. **The seal's size belongs to the text; the animal belongs to the stone.** Two stones with the same text are close in face size: mean gap 0.537 on the log scale (faces differ by 71%) against 0.630 (88%) with size dealt among seals of the same site, length and format (P 0.016). The pull is strongest across time: twins from different time bins differ by 48% against 88% (39 pairs, P 0.004), and square beast seals alone by 60% against 83% (P 0.007). The animal does not travel with the text: among the 45 twin pairs with a beast on both stones and not both unicorns, the species matches 0 times (0.91 by chance); twins in different time bins share the animal 17 times in 42 against 16.6 dealt (ratio 1.02). Means: when a text is cut on a new stone, generations later, the stone is made to the text's size and gets a new beast. The size is a rank written into the text (it fits the earlier finding that face size follows the closing sign: person 738 mm2 > jar 645 > spear 633 > carrier 495 > comb 420). Opens: size can be predicted from a text and used as a check on a text's rank where the closer is lost.

2. **Seal texts that recur are titles held by several people at once, not one man's name.** 71 twin sets in the first catalogue (187 stones), median 2 stones a text, at most 7. 32 texts have 2 or more stones in one time bin, and 15 of those have them in 2 or more cities inside that same bin. `003-156` has 4 stones in the middle bin alone; `004-390` has 3 stones in 3 cities in the middle bin; `061-740` has 3 middle-bin stones in 2 cities. One text on several stones in several cities at one time, each with its own animal (48 of 71 texts: every stone a different holder), is an office or a standard stamp issued to several holders. Names are the opposite: the biggest crest house, 235, has 56 complete name seals with 53 different texts; across Mohenjo-daro 959 complete seals carry 915 different texts.

3. **Which kinds get copied: count lines and name + closer; bare names, titled names and front formulas are one stone each.** Twin rate against the rate expected from text length alone: count line 49 of 81 seals twinned against 23.7 dealt within length (2.05 times, P 0.0005); name + closer 91 of 540 against 64.7 (1.41 times, P 0.0005); bare name 25 of 337 against 60.0 (0.42 times, P fewer 0.0005); name + title 2 of 77 against 12.1 (0.17 times, P fewer 0.0005); front formula 11 of 389 against 16.2 (0.68 times, P fewer 0.071). Means: the count line is a standard stamp (the stamps job found it is also the seal text most often pressed on goods); `[name][closer]` is a rank name (house + rank) held by several; a bare name, a titled name and a name behind a front word are personal: written for one holder.

4. **Twins sit in the same city and area, never in the same building.** 0 twin pairs in one building or room (71 pairs with buildings; 0.27 expected, so this alone has little force), 2 in one block (1.57), 18 in one area against 12.2 (P 0.072). The second catalogue (its own transcription, faces joined line by line): twin pairs in the same excavation locus 48 against 28.6 dealt within site and length (ratio 1.68, P 0.004). The stand letter follows the city: twins in one city but different buildings share it 9 of 22 against 4.9 (P 0.062), twins in different cities 5 of 29 against 5.7. Means: the holders of one title live in the same quarter of a city but in different houses, and their stones were cut by the local workshop (same stand); across cities the stand is the other city's own.

5. **One text is cut by one hand for several cities, and one unfinished copy was found.** Photos of 29 twin pairs (`photo_sheet_1-6.jpg`): same or near-same hand 8, different hand 21; same layout 24, different 5 (all 5 are a beast seal against an inscription-only bar or a cylinder). 5 of the 8 same-hand pairs are in two different cities: K-19 (Kalibangan) and M-224 (Mohenjo-daro), `005-405`, are near-identical stones (same tree, same five strokes, same unicorn, same stand W); M-404 (Mohenjo-daro bar) has the same hand again; H-62 / M-1108 and H-451 / M-879 (Harappa / Mohenjo-daro) are cut alike. **L-55 (Lothal) is an unfinished seal**: the text `233-176-740` is cut in the top band and the field below is blank, with no animal; its twin L-35, in the same city, is a finished unicorn seal (stand J). That is a second stone of the same text being made in the same town. Means: stones of one text came from one workshop and were carried out to other cities, and a holder's stone could be replaced (or a new holder's stone cut) from the same text.

## Tables

### 1. Twin sets by text length, and chance (`sets.csv`, `chance_by_length.csv`)

Token shuffle = every sign dealt at random over all text positions (keeps lengths and sign counts). Sign-pair generator = each text regrown at its own length from the seals' own sign-pair table (keeps short-range grammar, generous to chance). 300 rounds each.

| length | complete seal texts | real twin sets (seals) | token shuffle mean (max) | P | sign-pair generator mean (max) | P |
|---|---|---|---|---|---|---|
| 1 | 57 | 6 (13) | 9.5 (15) | 0.98 | 9.3 (16) | 0.98 |
| 2 | 244 | 37 (104) | 9.0 (19) | 0.003 | 25.5 (35) | 0.003 |
| 3 | 245 | 14 (36) | 0.30 (2) | 0.003 | 10.2 (18) | 0.060 |
| 4 | 241 | 11 (28) | 0.01 (1) | 0.003 | 1.7 (5) | 0.003 |
| 5 | 291 | 3 (6) | 0 (0) | 0.003 | 0.47 (3) | 0.020 |
| 6+ | 459 | 0 | 0 | | 0.05 (1) | |

Chance is negligible from 4 signs on under both nulls; at 2 and 3 signs part of the twins are what the grammar alone would make (25.5 of 37, 10.2 of 14). Set sizes: 2 stones 44 sets, 3: 17, 4: 5, 5: 3, 6: 1, 7: 1.

Counting each stone once: inside the first catalogue a set is a set of different object ids; prism faces never pair with each other; members sharing a CISI number, an excavation number, or the same site, building, animal, stand and face size within 0.5 mm were merged into one stone (2 merged). The second catalogue (Mahadevan 1977) re-transcribes mostly the same stones: its multi-line faces were joined line by line (sideline = 10 x side + line), giving 91 sets on 238 seals (lengths 1: 3, 2: 37, 3: 21, 4: 17, 5: 7, 6: 2, 7: 3, 8: 1). The union counts, for each text and each of its seven site groups (Mohenjo-daro, Harappa, Chanhu-daro, Lothal, Kalibangan, other Indian sites, abroad), the larger of the two catalogues' counts, so a second-catalogue seal adds a stone only where that catalogue has more copies there: **124 sets, 329 stones** (`union_sets.csv`), 53 sets seen only through the second catalogue, among them the longest: `140-592-400-003-001-690-033-700` (8 signs, two Mohenjo-daro seals, loci 27 and 31, depths 5 and 18 ft) and `861-002-240-415-100-740-090` (7 signs, M-199 and two more Mohenjo-daro seals). The tables below use the first catalogue, which carries findspots, bins, stands and sizes.

### 2. The 28 twin sets of 3+ signs (first catalogue)

Columns: stones, kind, cities, buildings (MD = Mohenjo-daro, H = Harappa), depths (ft), bins, animals, stand letters, face sizes (mm2), boss codes.

| text | n | kind | cities | buildings | depths | bins | animals | stands | sizes | boss |
|---|---|---|---|---|---|---|---|---|---|---|
| 820-002-003-390 | 4 | count line | Harappa, MD, Nausharo | MD DKB 5 5; MD DKG First St | 17.0 3.3 | early middle | unicorn x4 | W J S W | 778 742 529 416 | - - - PBSG |
| 005-900-740 | 4 | name + closer | Harappa, MD | MD DKG(S) 10I; MD VSA 2XVI | 12.0 9.5 | early middle | unicorn unicorn none unicorn | I J | 317 692 408 306 | - PB PBVG - |
| 013-840-740 | 4 | name + closer | Harappa, Lothal, MD | H AB P24/8; MD HRB 2XII; MD HR 05 | 7.0 6.8 3.0 7.0 | early late | none unicorn elephant unicorn | | 274 645 412 645 | PB PB - - |
| 468-806-154 | 4 | name + closer | Harappa, MD | H FTrench IV+V J12/3; MD DKG(S) 9I | 3.0 4.8 | late | none x4 | | 324 155 - 128 | - - PN - |
| 003-140-100-740 | 3 | name + closer | Harappa, MD | H AB P24/16; H AB P24/8; MD DKB 4XIV | 9.2 7.4 3.0 | late middle | unicorn unicorn zebu | W W | 412 853 1267 | PB - PB |
| 061-142-400-740 | 3 | name + closer | Harappa, MD | | 5.0 6.5 | late middle | unicorn x3 | W J W | 581 713 462 | - PB PBSG |
| 817-002-003-390 | 3 | count line | Chanhu-daro, Harappa, MD | H J Q30/14; MD DKG(S) 7II | 58.0 7.9 9.0 | late middle | unicorn x3 | W J W | 853 1011 534 | - PB PBSG |
| 817-002-004-390 | 3 | count line | Dholavira, MD | MD DKE Trench E | 4.5 9.7 | early middle | unicorn x3 | | 467 412 484 | - PB PB |
| 003-220-740 | 3 | name + closer | MD | MD HRB 1VIII | 6.0 | early | scene, none, none | | 853 213 162 | PB - - |
| 235-482-740 | 3 | name + closer | Chanhu-daro, Lothal, MD | MD HRB 2IX | 1.4 2.4 10.5 | late | unicorn x3 | W L | 524 161 807 | PB - PBSG |
| 061-171-035-740-090 | 2 | name + closer + title | Harappa, MD | H FTrench VI P10/10; MD DKG(S) 9VIII | 3.2 7.1 | late | -, zebu | | 467 225 | - PB |
| 817-002-803-233-520 | 2 | front formula | Chanhu-daro, Harappa | Chanhu Mound I; H FTrench VI P9/5 | 3.0 13.5 | late | unicorn x2 | S | 467 524 | - PBCG |
| 861-002-415-100-740 | 2 | front formula | MD | MD DKG First St | 15.9 | middle | unicorn x2 | L S | 778 - | PB PB |
| 255-435-690-740 | 2 | name + closer | MD | MD DKG(N) 22; MD HR 38 X/03 | 5.8 2.5 | late | unicorn x2 | | 824 - | PB PB |
| 817-002-005-390 | 2 | count line | MD | MD DKG First St; MD VSA 1III | 19.9 5.0 | middle | multi-headed, unicorn | | 548 713 | - PB |
| 817-002-061-740 | 2 | front formula | MD | MD DKG(S) 7III; MD HR Main St E | 19.1 2.0 | late middle | unicorn x2 | S S | 340 778 | PB PB |
| 861-002-003-390 | 2 | count line | MD | MD DKB 4IX; MD DKG(S) 8III | 5.6 5.5 | early late | unicorn x2 | W W | 1011 1049 | - PB |
| 861-002-016-390 | 2 | count line | Dholavira | Middle Town 46 x 43 | | late | none x2 | | 1190 213 | - PN |
| 920-060-741-592 | 2 | front formula | MD | MD DKG(S) 10I; MD DKG(S) 4 | 18.4 14.9 | middle | unicorn x2 | J | 571 639 | - PB |
| 003-550-617 | 2 | bare name | Harappa, MD | H FTrench IV+V; MD DKG(S) 12I | 8.2 11.0 | middle | unicorn, none | S | 524 235 | PB P |
| 233-176-740 | 2 | name + closer | Lothal | | 14.1 | | unicorn, none (L-55 unfinished) | J | 365 524 | PB PB |
| 235-798-740 | 2 | name + closer | MD | MD DKB 4XIII; MD DKC 6 | 2.5 1.5 | late | unicorn x2 | W | 467 930 | - - |
| 590-390-740 | 2 | name + closer | Allahdino, Chanhu-daro | | 0.7 9.3 | | unicorn x2 | L | 656 1228 | - PB |
| 698-861-002 | 2 | bare name | MD | MD DKE Trench E | 3.0 | late | none x2 | | 231 317 | NN NN |
| 703-615-740 | 2 | name + closer | Harappa, MD | MD DKG(S) 7VII | 6.2 16.5 | middle | buffalo, unicorn | I | 930 374 | PB - |
| 705-033-520 | 2 | name + closer | MD | MD DKG(N) 20I; MD DKG(S) 12V | 3.5 17.1 | late middle | unicorn, none | J | 795 633 | PB - |
| 706-033-520 | 2 | name + closer | Dholavira, Harappa | | | | unicorn, none | I | 900 307 | PB NN |
| 877-159-400 | 2 | name + title | MD | MD DKB 1 1; MD DKG(S) 2I | 2.0 10.2 | late middle | unicorn, none | W | 676 356 | PB - |

All 71 sets with every column: `sets.csv`.

### 3. What varies inside a twin set (`vary.csv`, `log_3.txt`, `log_4.txt`, `log_6.txt`)

Dealt within site and text length unless marked.

| attribute | pairs | real | dealt | ratio | P |
|---|---|---|---|---|---|
| same animal, all pairs | 186 | 98 | 73.4 | 1.34 | 0.003 more |
| same animal, dealt within site x length x format | 186 | 98 | 83.8 | 1.17 | 0.044 more |
| both unicorn (site x length x format) | 191 | 88 | 71.6 | 1.23 | 0.025 more |
| same species, beast on both and not both unicorn | 45 | 0 | 0.91 | 0 | 0.38 fewer |
| same animal, different cities | 110 | 51 | 39.5 | 1.29 | 0.027 more |
| same animal, different time bins | 42 | 17 | 16.6 | 1.02 | 0.50 |
| same animal, same time bin | 51 | 27 | 19.8 | 1.36 | 0.035 more |
| same animal, bare names in different cities | 11 | 1 | 3.5 | 0.29 | 0.083 fewer |
| same stand, all unicorn pairs | 51 | 14 | 10.6 | 1.32 | 0.19 |
| same stand, same city other building | 22 | 9 | 4.9 | 1.84 | 0.062 more |
| same stand, different cities | 29 | 5 | 5.7 | 0.88 | 0.67 |
| same format | 191 | 156 | 138.1 | 1.13 | 0.015 more |
| same time bin | 94 | 52 | 42.7 | 1.22 | 0.082 more |
| same city (city dealt within length) | 191 | 77 | 69.0 | 1.12 | 0.19 |
| size gap, all (site x length x format) | 166 | 0.537 | 0.630 | 0.85 | 0.016 closer |
| size gap, different time bins | 39 | 0.395 | 0.631 | 0.63 | 0.004 closer |
| size gap, different cities | 98 | 0.580 | 0.647 | 0.90 | 0.12 closer |
| differ in animal or stand, same city other building | 76 | 42 | 47.6 | 0.88 | 0.15 fewer |
| same building / room / block / area | 71 / 28 / 71 / 114 | 0 / 0 / 2 / 18 | 0.27 / 0.03 / 1.57 / 12.2 | | area 0.072 more |
| second catalogue: same field symbol (animal) | 247 | 136 | 96.5 | 1.41 | 0.0002 more |
| second catalogue: same locus | 247 | 48 | 28.6 | 1.68 | 0.004 more |

Read: the shared-animal excess is the civic unicorn (and inscription-only bars pairing with bars), not a species carried by a holder: no rare beast ever repeats inside a set. What really stays with a text is its size (above all across generations), its format, its city quarter (locus), and inside one city its workshop's stand.

### 4. Kinds of text (`kinds.csv`)

| kind | seals | twinned | twin rate | expected from length | ratio | P | sets | pairs | cross-city pairs | cross-bin pairs / dated |
|---|---|---|---|---|---|---|---|---|---|---|
| name + closer | 540 | 91 | 16.9% | 12.0% | 1.41 | 0.0005 more | 36 | 80 | 47 | 14 / 38 |
| front formula | 389 | 11 | 2.8% | 4.2% | 0.68 | 0.071 fewer | 5 | 7 | 3 | 2 / 3 |
| bare name | 337 | 25 | 7.4% | 17.8% | 0.42 | 0.0005 fewer | 12 | 14 | 11 | 3 / 7 |
| count line | 81 | 49 | 60.5% | 29.5% | 2.05 | 0.0005 more | 14 | 79 | 46 | 19 / 38 |
| name + title | 77 | 2 | 2.6% | 15.8% | 0.17 | 0.0005 fewer | 1 | 1 | 0 | 1 / 1 |
| name + closer + title | 54 | 2 | 3.7% | 5.5% | 0.68 | 0.41 | 1 | 1 | 1 | 0 / 1 |
| front alone | 8 | 4 | 50% | 35.3% | 1.42 | | 1 | 6 | 3 | 3 / 6 |
| [crest][jar][man] | 0 complete seals | | | | | | | | | |

Copied across cities: count lines (46 cross-city pairs) and name + closer (47). Copied across time: count lines (19 of 38 dated pairs in different bins), name + closer (14 of 38). Inside one building: none of any kind. Not copied: names behind a front word, titled names, bare names.

### 5. Holders (`holders.csv`)

Reading "text + animal + stand = one stone = one holder": 71 texts, median 2 stones, max 7; in 48 of 71 texts every stone with a known animal is a different holder. Most stones: `003-156` 7 stones, 6 holders, 3 cities, 4 in the middle bin; `016-390` 6 / 5 / 2 cities, early to late; `003-390` 5 / 5 / 3 cities; `031-156` 5 / 4; `061-740` 5 / 4 / 4 cities, 3 in the middle bin; `013-840-740` 4 / 3 / 3 cities, early and late; `005-900-740` 4 / 4; `468-806-154` 4 stones, all inscription-only bars (the counted load tag of MAP), Harappa and Mohenjo-daro, all late. Count lines average 3.5 stones a text, name + closer 2.5, bare names 2.1.

Six centuries is about 24 generations of 25 years. A text whose stones were one holder at a time would show its surviving stones spread over the bins with one per bin; instead 32 texts have 2+ stones inside one bin and 15 of them in 2+ cities inside that bin. Several holders at once.

Crest houses (complete name seals): 235 has 56 stones / 53 texts in 7 cities; 220 53 / 49; 240 41 / 39; 803 38 / 35; 741 35 / 34; 061 26 / 16 (the quarter sign, with the quarter-king lineage `061-142-400-740` and `061-740` recurring). Per city: Mohenjo-daro 959 stones / 915 texts, Harappa 270 / 260, Dholavira 67 / 65, Lothal 57 / 56.

### 6. Backs, wear, and the photo tally

Backs and wear, twin members against all complete seals of the same site and length (`backs.csv`): not pierced 6 of 122 against 5.8 dealt; no boss 8 of 117 against 12.9 (P fewer 0.052); poor condition 59 of 187 against 52.7 (P more 0.12); inscription-only 34 of 183 against 36.1. Twin members with no boss or not pierced: Dmd-1 `740`, H-681 `468-806-154`, M-329 and M-330 `698-861-002` (both NN, one building, DKE Trench E), M-410 `220`, M-1195 `176-740`, M-1222 `416-151`, Dholavira `706-033-520` (NN), Dholavira `861-002-016-390`, Rhd-1 `031-520`.

Photo tally, 30 pairs drawn longest text first, at most 2 per set (`photo_pairs.csv`, `photo_tally.csv`; I looked at every sheet):

| | same city | different cities | all |
|---|---|---|---|
| same or near-same hand | 3 | 5 | 8 |
| different hand | 9 | 12 | 21 |
| same layout | 10 | 14 | 24 |
| different layout | 2 | 3 | 5 |

Same-hand pairs: H-62 / M-1108 (`003-140-100-740`, unicorn / zebu), H-451 / M-879 (`061-142-400-740`), H-49 / M-401 (`003-550-617`, unicorn / bar), L-35 / L-55 (`233-176-740`, L-55 unfinished), M-874 / M-1305 (`877-159-400`, unicorn / bar), M-187 / M-193 (`005-156`), K-19 / M-224 and K-19 / M-404 (`005-405`). Hand against animal: the same-hand pairs share the animal 3 of 8, the different-hand pairs 10 of 21: a carver cut the same text with a different beast. Pair 19 (M-329 / M-330) left out: M-330 is two-sided and its photo shows its other face. Worn or broken in the sample: H-565, M-850, M-950, M-1443, H-71. Recut: none seen. Unfinished: L-55.

### 7. One holder, several texts (`one_holder.csv`, `near_twins.csv`)

House-mate pairs (one building, complete text) with the same unicorn stand letter: 269; texts related (same crest, one sign apart, or one inside the other) 3 (1.1%), against 5.0 with texts dealt within site (P more 0.87); house-mates with different holder marks 43 of 1,982 (2.2%). The three: M-1822 / M-9 (`745-171-032-031` / `745-311-031`, W); M-1779 / M-1810 (`003-156` / `920-156-002-003-140-100-740`, J); DKG First Street `861-002-240-637-740` / M-199 `861-002-240-415-100-740-090` (S: a High-star house owner and the High-star house's agent, in the building the registry already placed them). Redesign, sharing any name sign: 27 of 269 against 19.8 (ratio 1.36, P 0.086); other-holder house-mates 157 against 146.0 (1.08).

Near twins (420 pairs, 3+ signs, one sign apart): same block 7 against 3.43 (P 0.061), same building 2 against 1.12, same city 203 against 179.7 (P 0.076); same animal 215 of 398 against 171.6 (ratio 1.25, P 0.004); same stand 34 against 35.6. The differing sign is a personal name sign 152 times, a front word 65, a short number 64, a crest 39, a closer 17.

## What it all says, plainly

- **Count line** (`003-156`, `016-390`, `820-002-003-390`): a standard quantity stamp. Twinned at twice its length's rate, up to 7 stones, several in one bin and in several cities, same size across generations. Not a person: an issue stamp held by every store-keeper of that issue.
- **Name + closer** (`061-740`, `005-900-740`, `003-140-100-740`, `061-142-400-740`): a rank name, a house plus its rank, held at once by several holders in several cities, each on his own stone with his own beast; the stone is cut to the rank's size and the size holds over generations. An office of a house.
- **Bare name, name + title, front formula**: personal. Twinned at 0.17-0.68 of the length rate; inside one crest house almost every stone has its own text (235: 53 texts on 56 stones).
- **The animal**: the stone's own mark, not the text's. Rare beasts never repeat inside a set; across generations the beast is chosen anew. The unicorn excess inside sets is the civic default of the seals that carry office texts.
- **The stand letter**: the city workshop's mark: shared by twins in one city (9 of 22 against 4.9), not across cities.
- **A stone** = text (office or name) + size (the text's rank) + beast and stand (the holder and the workshop that cut it).

## What went against

- **(a) Twins in one building differ in animal or stand more than chance**: no twin pair is in one building at all (0 against 0.27), so the test had no pairs. Redesign with near twins: 2 in one building against 1.12; same-city other-building twins differ in animal or stand 42 of 76 against 47.6 (fewer, not more). Against as framed. New idea run instead: the holders of one text live in one quarter (second-catalogue locus 48 against 28.6, P 0.004).
- **(c) committed guess, count lines share the animal less across cities (a local office)**: against. Count lines in different cities share the animal 26 of 46 against 17.3 (1.50, P 0.038). Rescue: it is all unicorn-with-unicorn; dealt within format the general excess falls to 1.17 and no non-unicorn species repeats (0 of 45), so the "same holder travelling" reading gets nothing either.
- **P0 (no animal sharing)**: against as a raw number (98 against 73.4); explained by the unicorn and format, as above.
- **P-city (twins in other cities more than chance)**: against for seal-seal pairs: same city 77 of 191 against 69.0 (P 0.19). The stamps result (impression twins in other cities, 13 of 13) is about where stamped goods went, not where twin stones lie.
- **Twins carry more unfinished or bossless stones (a replacement being made)**: against in the catalogue columns: no boss 8 against 12.9 (P fewer 0.052), not pierced 6 against 5.8. One unfinished copy found by eye (L-55).
- **One holder's set of stones shows related texts**: against on crest, edit distance and containment (3 against 5.0); the name-sign redesign leans with (27 against 19.8, P 0.086). Next way in: holder = stand letter + seal size band + building, and compare against the masters list (the one hit is an owner and his own agent).
- **No twin of 6+ signs in the first catalogue's strict set** (459 texts); the second catalogue has 6 sets of 6-8 signs at Mohenjo-daro and Harappa. Long personal texts are one stone each; the long twins there are worth a photo check (Mahadevan 1527 / 2604, `140-592-400 | 003-001-690-033-700`).

## Next

1. Predict face size from text (closer + kind + length) and test on held-out seals; then use it on broken seals.
2. Photo-check every cross-city same-hand pair and every second-catalogue long twin; find the workshop (K-19 / M-224 / M-404 hand).
3. Look at every inscription-only seal with a blank field like L-55: a list of unfinished stones and their twins.
