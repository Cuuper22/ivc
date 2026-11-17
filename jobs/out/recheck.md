# Recheck of the pair-count findings, 2026-11-17

One known fault, checked wherever it could apply. The headline "seals from one room share the stand letter 38.1% against 17.2%" came from two counting errors: (1) two faces of one stone were counted as a pair of seals (such a pair always shares); (2) the chance figure dealt labels among a pool holding stones that cannot carry the label, so chance came out too low. Every finding below that counts pairs of objects found together was rerun with (a) one row per physical object, (b) the deal limited to objects that can carry the property, inside the original strata, and (c) identical copies found together counted once.

## Plain words

- **Face**: one inscribed side of an object. **Object / stone**: the physical thing. Lipi ids like 1338.1 and 1338.2 are two faces of object 1338.
- **Two catalogue rows of one stone**: decided in `work_scripts/recheck_common.py`. The two rows must share the site, the full text on every face and the excavation number, with the plate reference cut off. There must be exactly two rows under that number, and the sizes must agree within 1.0 mm. CISI numbers are never shared by two objects in this catalogue, so they cannot be used. The rule merges 3 pairs in the whole catalogue, all Harappa tablets: H-316 = H-1304, H-912 = H-1191, H-1150 = row 4409. It merges no seal. Copper tablets have their own rule (finding 15).
- **Copy event**: all objects of one site and findspot that carry the same full text, counted once (a batch of moulded tablets in one trench is one event).
- **Deal / chance**: labels shuffled at random among the objects of one stratum (site, area, depth band) 2,000 to 10,000 times. **P**: the share of deals at least as extreme as the real count. **Ratio**: real count divided by the dealt mean.
- **Stands**: the clean figure keeps the finding at about its old strength. **Weakened**: the effect keeps its direction but is smaller or no longer clear of chance. **Falls**: the clean figure is at chance.

## Table

| # | finding | old figure | fault present | clean figure | P | verdict |
|---|---|---|---|---|---|---|
| 1 | same-room seals share an uncommon middle sign | 5 pairs against 0.73 | neither | 5 against 0.67 (middle taken face by face: 4 against 0.68) | 0.0007 (0.007) | stands |
| 2 | different hands carved the shared sign | 24 pairs, 4 same hand | neither (0 of 70 listed pairs is one stone) | unchanged: 24, 4 | – | stands |
| 3a | same fish first among house-mates | 15 of 23 against 36% | (2) mild: deal over all seals | 15 of 23 against 40% | 0.008 | stands |
| 3b | name-slot sign repeats in houses | 19 pairs against 7.8 | neither | 19 against 7.8 (within area: 8.1) | 0.003 (0.001) | stands |
| 4 | jar + man seals beside an owner object of their crest | building 5/24 against 2.09; block 9/24 against 5.28; pooled block 11/30 against 6.35; 9 objects against 2.94 | (c): two moulded owner tablets (M-431, M-432) counted as two | 5/24 against 2.10; 9/24 against 5.30; 11/30 against 6.36; 8 objects against 2.84 | 0.046; 0.045; 0.027; 0.022 | stands |
| 5a | same-crest seals share a building | 1.43 (28 against 19.5) | (1): 2 same-crest pairs were two faces of one stone | 1.26 (24 against 19.1) | 0.16 | falls |
| 5b | same-house (top 20) seals share a building | 1.41 (23 against 16.3) | (1): face rows weighted twice | 1.31 (21 against 16.0) | 0.15 | falls |
| 5c | same-tag seals share a building | 1.11 | (1) | 1.16 (16 against 13.8) | 0.32 | stands (at chance, as before) |
| 5d | Harappa same-tag seals share a trench | 1.68 (32 against 19.1) | (1) and (c) | 1.53 (27 against 17.6) | 0.033 | weakened |
| 6a | a name keeps its own amount | 38 against 21.6 | neither (copies already merged per trench) | 38 against 21.6 | 0.003 | stands |
| 6b | same name, different amount, one trench | 9 against 3.5 | neither (2 of the 9 are one amount written in the other order) | 9 against 3.43; as amounts 7 against 2.87 | 0.011; 0.023 | stands |
| 6c | count-line seal and record with the same count in one area | 89 against 69.5 | (c): every moulded copy counted as its own record | 43 against 43.7 | 0.59 | **falls** |
| 7a | second-catalogue twins in one locus | 48 against 28.6 | (1): 10 object pairs counted twice (two identical faces); (c): batches | pairs 42 against 26.1; batches once 24 against 20.1 | 0.005; 0.15 | **falls** with batches once |
| 7b | twins close in size | 71% against 88% | neither | 71% against 88% | 0.016 | stands |
| 8 | count-line texts on impressions | 22.7% against 5.7%; 24.5% against 4.3% | neither: no seal is its own impression | 21.3% against 3.3%; 27.3% against 4.3% | 1.2e-7; 0.0005 | stands |
| 9 | rare beasts one per building (same species) | 13 against 20.8 | (2): species dealt among all seals, unicorns and bare seals included | 13 against 16.1 | 0.25 | **falls** |
| 10 | time-flat shares; earliest level 0 of 38 fish crests | 4.5/4.1/4.5%; 12.3/12.6/12.8%; 0/38 | neither (objects throughout) | 4.5/4.2/4.5%; 12.3/12.5/12.5%; 0/38 | trend P 1.0, 1.0; 0.042 | stands |
| 11 | 136 fixed phrases (8+ distinct texts) | 136 | damaged copies of one text counted as separate texts | 134 keep 8+ texts; 136 have 8+ copy events | – | stands (134) |
| 12 | frame on "482 new texts"; 77 gap texts | v2 7.536 bits, decoys 7.790, best 7.671 | repeats: 482 lines are 389 distinct (93 repeats); no catalogue double count; gap items clean | 389 distinct: v2 7.403, decoys 7.690, best 7.564, 0 of 20 reach it | – | stands |
| 13a | house-mates share the sign before the jar | 15 against 9.3 | neither | all same-house pairs: 17 against 10.7 | 0.048 | stands |
| 13b | room-mates share the number before a fish | 5 against 0.74 | (2): rooms dealt among all seals | 5 against 2.77 | 0.030 | weakened |
| 13c | Lothal warehouse: 7 texts on 15 impressions; KLB-1 2 against 7.35 | 7 against 12.96 | neither | 7 against 12.94; 2 against 7.36 | 0.0002 | stands |
| 13d | 590-390 seals in 21 houses | 22 seals, 21 houses | neither (24 faces = 24 stones) | unchanged | – | stands |
| 13e | stand letter shared by room-mates (FRAME 14) | 38.1% against 17.2% | (1) and (2) | 29.8% against 27.1% (stand job) | 0.30 | falls (already found) |
| 14a | comb-chit names: their seals end in the comb | 5 of 60 against 0.80 | (c): H-354 is an identical seal beside H-352 in one trench | 4 of 59 against 0.70 | 0.003 | stands |
| 14b | names with two endings | comb+man 4 against 17.7; jar+comb 33 against 66.1; jar+man 14 against 34.0 | (c): copies inflated chance | 4 against 12.1; 33 against 57.4; 14 against 27.5 | 0.0005 each | stands |
| 15 | copper copies in one register lot | 6 against 0.83; within 100 numbers 15 against 7.60 | (1): 3 tablets listed twice (corpus row + dig-report plate row) | 2 against 0.52; 10 against 6.42 | 0.075; 0.11 | weakened |

## Finding by finding

**1. Same-room seals share an uncommon middle sign: stands.** `findspot_room.py` already joined faces by object. It dealt room labels among seals of one excavation area and 3-ft depth band, and every seal there can hold a room label. Neither fault was present. The 5 pairs (M-1923+M-53, M-1661+M-1045, M-92+M-195, M-153+M-1112, M-723+M-937) are 10 different stones with 5 different texts. Clean run: only seals that have a middle sign (751 of 845), identical texts in a room counted once (there were none). Result: 5 against 0.67, P 0.0007. The old script joined a two-faced seal's faces into one string, so the inner ends of the faces counted as middle. With the middle taken face by face it is 4 against 0.68, P 0.007. `recheck_01_room_middle.py`, `work_data/recheck/r01_log.txt`.

**2. Different hands, same sign: stands.** All 70 pairs in `jobs/photo_pairs_0.txt` to `_3.txt` were checked. None is one stone, two catalogue rows of one stone, a pair with one excavation number, or a pair with an identical text. The 24 pairs with the sign on both stones and the 4 same-hand calls stand as judged. `recheck_02_photo_pairs.py`.

**3. Name = crest + personal part + tag: stands.** (a) The fish test already kept one face per object, and no house held identical texts. When house labels are dealt only among fish-first seals (the only seals that can make a fish-fish pair), chance rises from 36% to 40%. The real rate is 15 of 23 (65%), P 0.008. (b) The who-sign table is one row per face, but no seal in it has two faces with a who-sign, so no pair is one stone. Result: 19 against 7.8 (P 0.003); dealt within excavation area, 19 against 8.1 (P 0.001). `recheck_03_name_slot.py`.

**4. The man-ending seals and their master's crest: stands.** `people.csv` and `names_all.csv` have one row per face, but no manager sits twice. The tally of owner objects counted the moulded tablets M-431 and M-432 (identical text, DK-E Trench E) as two objects. Clean results:
- Building: 5 of 24 against 2.10 (P 0.046).
- Block: 9 of 24 against 5.30 (P 0.045).
- Pooled over cities, block level: 11 of 30 against 6.36 (P 0.027).
- Owner objects of the crest in the managers' buildings: 8 against 2.84 (P 0.022); the old figure was 9 against 2.94.

`recheck_04_manager.py`.

**5. Crest and tag pairs in one building: same-crest and same-house fall; Harappa tag weakened.** `people.csv` has 1,190 rows on 1,174 stones. Fifteen stones sit there twice, and 5 of them carry one crest on both rows. Two of the 28 "same-crest pairs in one building" were one stone paired with itself. Clean results at Mohenjo-daro, one row per stone:
- Same crest: 24 against 19.1 (1.26, P 0.16).
- Top-20 houses: 21 against 16.0 (1.31, P 0.15).

Neither is clear of chance any more, so "a house is one building" loses its number. Same tag: 1.16 (P 0.32), at chance as before. At Harappa, with stones once and identical texts in one trench once, same-tag pairs share a trench 27 against 17.6 (1.53, P 0.033). `recheck_05_crest_tag_pairs.py`, `r05_table.csv`.

**6. Tablets as issue chits: two parts stand, the seal-and-record pairing falls.**
- (a) The 38 against 21.6 test already counted each (name, amount, trench) once, and objects carried their faces joined. It stands at 38 against 21.6 (P 0.003). Ten of the 38 pairs come from one text, 176-740-400 with 033-700, found in five Harappa trenches (`r06b_log.txt`).
- (b) Same name with a different amount in one trench: 9 against 3.43 (P 0.011). Two of the 9 pairs are one amount written in two orders (034-700 and 700-034). Read as one amount, it is 7 against 2.87 (P 0.023).
- (c) Count-line seal plus record (`stamps_5_more.py` P7b) counted every tablet face as a record. The 89 pairs were mostly two seals reading 033-700 / 034-700 beside 29 and 17 identical tablets in Harappa F Trench I. With stones once and identical tablets in one trench once, it is 43 against 43.7 (P 0.59). With identical seals in one trench also once, it is 28 against 28.3. **This falls.** The seals and tablets of one amount do not sit together beyond what their numbers give.

`recheck_06_tablets.py`.

**7. Twins: the locus result falls with batches counted once; the size result stands.** In the second catalogue, five two-sided objects (1412, 2220, 2339, 2505, 2508) carry the same two texts. Each pair of them was counted twice, once per face: 10 extra pair counts. With one count per object pair, it is 42 against 26.1 (P 0.005). Counting each text's batch in one locus once, as rule (c) asks, it is 24 against 20.1 (P 0.15): at chance. Of the 42 pairs, 34 sit in Mohenjo-daro locus 31, a sector that holds 505 of the city's 1,232 seals in that catalogue. Twin sizes show neither fault: 71% against 88%, P 0.016. `recheck_07_twins.py`.

**8. Count-line texts on impressions: stands.** No count-line or name seal is matched to an impression that is itself, another row of itself, or an object with its own excavation number. In 18 seals the match rests only on a second-catalogue sealing at the seal's own site. That could be the same object classed as a sealing by the other catalogue, so those 18 were dropped. Results:
- Clean, both catalogues: count-line 16 of 75 (21.3%) against name seals 20 of 609 (3.3%), P 1.2e-7.
- First-catalogue impressions only: 14 of 75 against 4 of 609, P 2.4e-11.
- Stamps job, one row per seal stone: 12 of 44 (27.3%) against 4.3% length-matched, P 0.0005.

The hits rest on 4 distinct impression texts (2 in the stamps table), as already said. `recheck_08_countline_impressions.py`, `r08_hits.csv`.

**9. Rare beasts avoid each other in a building: falls.** This is fault (2). `stand_6_animals.py` dealt the whole species column (unicorn and none included) among all seals of a city, which also changes how many rare-beast pairs exist (117.8 dealt against 91 real). Dealing the species only among the rare-beast stones keeps the 91 pairs fixed. Then same species is 13 against 16.1 (ratio 0.81, P 0.25), and within city and format 13 against 16.0. The companion number does hold as a lean: buildings hold fewer rare-beast pairs than chance, 91 against 117.7 (P 0.078) when species are dealt among stones with a carved animal within city and format. `recheck_09_rare_beasts.py`.

**10. Time-flat results and the earliest level: stand.** `time_common` is one row per object (2,666 dated objects), and the shuffle runs within site and area over dated objects. Stones merged and copies in one area and bin once:
- Agents: 4.5 / 4.2 / 4.5% (P 1.0).
- Fish crest first: 12.3 / 12.5 / 12.5% (P 1.0).
- Office opening on all objects: 1.4 / 0.9 / 0.8% (P 0.43).
- Harappa inscription-only seals: P 0.0032 (old 0.0018).

The earliest-level count is per object. The second catalogue adds only the 2 stones that matched no first-catalogue stone, so no stone counts twice. Result: 0 of 36 (first catalogue alone, P 0.040) and 0 of 38 (P 0.042). `recheck_10_time_early.py`.

**11. Fixed phrases: stand (134 of 136).** The rule counts distinct strings. A damaged copy of a text (one sign lost) was a separate "distinct text", and two faces of one stone could both count. Merging strings that agree wherever both are legible, and counting each stone once, 134 of 136 phrases keep 8 or more texts. 904-832 and 002-005 drop from 8 to 7. Every one of the 136 is on 8 or more copy events. The biggest losses are 740-400 (114 to 101) and 820-002 (90 to 83). `recheck_11_phrases.py`, `r11_phrases.csv`.

**12. Frame scores: stand.** The "482 new texts" are 482 lines, not distinct texts: 181 lines carry 56 strings that repeat. Counting each string once leaves 389 texts. On those, frame v2 scores 7.403 bits per sign against 7.779 for frequency alone; its 20 decoys average 7.690 and the best reaches 7.564, so none reaches the frame. Its share of what the sign-pair model knows rises from 32.7% to 36.9%. A second catalogue could re-read a first-catalogue stone with one sign different. 53 of the 482 lines (11%) have such a near-match, below the 17% that first-catalogue texts show against other stones. Dropping them as well leaves 343 lines: v2 7.606, decoy best 7.722. The 77 gap items: no answer text is used twice, and no first-catalogue text gives two items. `recheck_12_frame_newtexts.py`.

**13. Other pair counts in FRAME.md.**
- (a) The pre-jar test already joined faces and dealt only among jar-final seals. Counting all same-house pairs, it gives 17 against 10.7 (P 0.048); the old 15 against 9.3 is the other-room part of the same table and was not rerun separately. No identical texts. Stands.
- (b) Number before a fish: fault (2). Rooms were dealt among all seals of the area and band, so number-and-fish seals seldom met by chance. Dealt only among the 88 seals with a number and a fish, it is 5 against 2.77 (P 0.030). Weakened.
- (c) Lothal and KLB-1 impression clusters: no object is stamped twice with one text. 7 against 12.94 and 2 against 7.36 (both P 0.0002). Stands.
- (d) 590-390: 24 faces are 24 stones. Stands.
- (e) FRAME finding 14 still states the stand-letter figure that the stand job overturned: 29.8% against 27.1%, P 0.30 (`stand_3b_recheck.py`, not rerun here). The "fading with distance" and "independent of crest" numbers rest on the same faulty table.
- The house-mate animal figure in MAP (12.5% against 11.0%) uses the same object-joined table and location deal as finding 1. It was not rerun.

`recheck_13_other_pairs.py`.

**14. Chits: stand.** Both chit scripts keep one row per object. (a) Comb seals for comb-chit names: H-354 has the same full text as H-352 in F Trench I. Counted once, it is 4 of 59 against 0.70 (P 0.003). (b) Names with two endings: identical moulded tablets carried the same ending to many names in each deal, so chance was too high. With copies counted once:
- Comb + man: 4 against 12.1 (0.33 of chance).
- Jar + comb: 33 against 57.4 (0.58).
- Jar + man: 14 against 27.5 (0.51).

All have P 0.0005. The order is unchanged: comb and man are the most separate pair. `recheck_14_chits.py`.

**15. Copper register lots: weakened.** The copper table is one row per tablet, so two faces cannot pair. But the first catalogue lists some Mohenjo-daro copper tablets twice: once under a corpus number, and once without one, from the dig report's plates (DK344793.9 = DK 3447, plate 93 no. 9). By the stated rule (same register number, no conflicting a/b suffix, same set, sizes within 1.5 mm), three such doubles exist:
- Plate row DK 3447 (35.1 x 26.2 mm) = M-559 (35 x 25).
- M-604 (34.3 x 26.2) = M-2050 (34 x 26).
- Plate row DK 5444 (35.8 x 25.4) = M-2045 (36 x 26).

Merged, same lot is 2 against 0.52 (ratio 3.8, P 0.075) and within 100 numbers is 10 against 6.42 (P 0.11). There are no photos of M-2050, M-2045 or the plate rows in the repository, so the three identities cannot be checked against pictures here. If they are separate tablets, the old 6 against 0.83 stands. The test uses set texts, not picture codes, so the 5 of 28 wrong copper picture codes do not touch it. None of findings 1 to 14 uses a copper picture code. Finding 9 uses the catalogue's animal code on seals, a different column. `recheck_15_copper_lots.py`.

## Lines to change

MAP.md line 125, replace with:
- `measured` CORRECTED: the stand letter is not shared by room-mates beyond chance once each stone is counted once and letters are dealt only among lettered stones (29.8% against 27.1%, P 0.30; `stand_3b_recheck.py`). The old 38.1% against 17.2% counted two faces of one stone as a pair.

MAP.md line 156, replace with:
- `measured` Room-mates at Mohenjo-daro share the number word before a fish in 5 pairs against 2.77 when rooms are dealt only among the 88 seals that carry a number and a fish (P 0.030; the old 0.74 dealt rooms among all seals; `recheck_13_other_pairs.py`).

MAP.md line 240, replace with:
- `measured` Counted once per stone, same-house seal pairs share a building 1.31 times chance at Mohenjo-daro (P 0.15) and same-crest pairs 1.26 times (P 0.16): no clear pull, so "a house is one building" has no number behind it. Same-tag pairs 1.16 (P 0.32). At Harappa same-tag pairs share a trench 1.53 times (27 against 17.6, P 0.033). (`recheck_05_crest_tag_pairs.py`; the old 1.41 / 1.43 counted two faces of one stone as a pair.)

MAP.md line 305, replace with:
- `measured` Went against: seals and records with the same number and thing do not share an area beyond chance once identical tablets in one trench count once (43 against 43.7, P 0.59; the old 89 against 69.5 counted each of 29 and 17 identical F Trench I tablets separately; `recheck_06_tablets.py`).

MAP.md line 329, replace with:
- `measured` Second catalogue: twin pairs in one excavation locus 42 against 26.1 (P 0.005) counting each pair of objects once, but at chance when a batch of one text in one locus counts once (24 against 20.1, P 0.15); 34 of the 42 pairs sit in Mohenjo-daro locus 31, which holds 505 of 1,232 seals. Stand letter shared by twins in one city but different buildings 9 of 22 against 6.4 (stand job).

MAP.md line 357, replace "5 of those seals end in the comb against 0.80 with seal endings shuffled inside each city (P 0.0005)" with:
"4 of 59 seals end in the comb against 0.70 with seal endings shuffled inside each city, identical seals in one trench counted once (P 0.003)"

MAP.md line 358, replace "comb + man 4 against 17.7; jar-only + comb 33 against 66.1; jar-only + man 14 against 34.0" with:
"identical tablets in one place counted once: comb + man 4 against 12.1; jar-only + comb 33 against 57.4; jar-only + man 14 against 27.5 (all P 0.0005)"

MAP.md line 369, replace "rare beasts are spread about one per building (same species in one building 13 against 20.8, P 0.085)" with:
"a building holds fewer rare-beast seals than chance (91 pairs against 117.7, P 0.078), but two rare beasts in one building are the same species at chance (13 against 16.1, P 0.25, species dealt only among rare-beast stones)"

MAP.md line 385, replace "Copies of a set lie in the same register lot 6 pairs against 0.83 (P 0.0005)" with:
"Copies of a set lie in the same register lot 2 pairs against 0.52 (P 0.075) once three tablets listed twice (corpus row + dig-report plate row) are merged; 6 against 0.83 if those are separate tablets"

MAP.md line 268 ("On 482 new texts") and line 291 ("on 482 new texts"), replace the phrase with "On 482 new lines (389 distinct texts; counted once: frame v2 7.403 bits against decoy best 7.564, 0 of 20)".

FRAME.md line 90, replace "room-mates share the number before a fish in 5 pairs against 0.74" with:
"room-mates share the number before a fish in 5 pairs against 2.77 (rooms dealt only among number-and-fish seals, P 0.030)"

FRAME.md line 104, replace "stand shared by same-room seals 38.1% against 17.2% (139 pairs, P 0.0003), fading with distance (room 1.79, block 1.27, area 1.13), independent of crest (P 0.91);" with:
"stand letter shared by same-room seals 29.8% against 27.1% once stones are counted once and letters dealt among lettered stones (104 pairs, P 0.30; same building at the same depth 1.21, P 0.0085);"
and line 102's claim "the stand in front of the unicorn marks the household" with "the stand letter is a carving style; the species does not follow the household either".

FRAME.md line 203, replace "Seal and tablet pairs in one area with the same number and thing: 89 against 69.5 (P 0.003), mostly Harappa F Trench I (seals 033-700 and 034-700 beside 29 and 17 tablets with the same text)." with:
"Seal and tablet pairs in one area with the same number and thing: 43 against 43.7 (P 0.59) once identical tablets in one trench count once; the old 89 against 69.5 counted the 29 and 17 identical F Trench I tablets one by one."
and in the same line "9 pairs against 3.5 (P 0.011)" with "9 pairs against 3.4 (P 0.011; 7 against 2.9, P 0.023, when 034-700 and 700-034 are read as one amount)".

FRAME.md line 233, replace "(same-house seal pairs sharing a building: 1.41 times chance at Mohenjo-daro, P 0.08)" with "(same-house seal pairs sharing a building: 1.31 times chance at Mohenjo-daro once each stone counts once, P 0.15)".

FRAME.md lines 149, 150 and 157, replace "482 new texts" with "482 new lines (389 distinct texts)", and add to line 157: "Counted once each: v2 7.403 against frequency 7.779, decoys mean 7.690, best 7.564 (0 of 20 reach it)."

FRAME.md finding 23 (Part 6): add "Merging damaged copies of one text and counting each stone once, 134 of the 136 keep 8+ texts (904-832 and 002-005 drop to 7)."

FRAME.md finding 4 and 29: no number changes needed. Optionally change "those buildings hold 9 same-crest objects against 2.94" to "8 against 2.84 with the two moulded M-431/M-432 counted once (P 0.022)".

## Files

Scripts: `work_scripts/recheck_common.py`, `recheck_01_room_middle.py` to `recheck_15_copper_lots.py`, `recheck_06b_keep_pairs.py`. Logs and tables: `work_data/recheck/` (132 KB). No existing script or report was edited.
