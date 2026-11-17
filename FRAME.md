# The frame: what is measured about the Indus script without any word

Every finding below was counted from the sign catalogues with no word attached to any sign, and reruns from the script named under it. Each has four parts: the claim, the number, what the number means, the script. Dates are 2026-11-17. Part 5 onward holds the findings of the machine frame, the fixed phrases, the stamps and the records; Part 8 holds how seals were made and what the seals say about their makers; Part 9 lists what was tested and did not hold. Before Part 1, "How pairs are counted" says how every count of pairs of objects was made. For the one place where words appear, see the Labels appendix at the end.

## Terms

- **Seal**: a small stone or clay stamp with a few signs. **Tablet**: a small flat plaque of clay, stone or copper. **Tags, pots, rods**: other inscribed objects. **Face**: one inscribed side. Counts of signs and texts are by face; counts of pairs are by object (see "How pairs are counted").
- **Sign**: one drawn character, cited by catalogue number (740 is a jar picture, 220 a fish picture).
- **Lipi catalogue**: the main catalogue (5,679 faces, 2,162 distinct complete texts). Texts are stored in reverse of reading order; everything here is in reading order.
- **Second catalogue**: Mahadevan 1977, a separate transcription linked to Lipi by a 366-pair crosswalk. **New texts**: its 1,183 texts with no partner in Lipi, never used to shape any rule.
- **Crest**: the first sign of a name. **House-mates**: two seals found in the same excavated house. **Job**: the role a sign plays in the text shape.
- **Bits per sign**: how many yes/no questions, on average, a model needs to guess the next sign of a text it never saw; lower means the model knows more about the order of signs. **Sign-pair model**: a table of which sign follows which sign; it is the yardstick for "how much of the order is known".
- **Class**: a group of signs that do the same job in the text. **Decoy job-set**: the same classes with the same sizes, dealt at random to the wrong signs of the same frequency; a real frame must beat its decoys.
- **Impression**: clay pressed with a seal and left on goods. **Sealing / tag**: a lump of clay over a knot, lid, jar mouth or door, carrying impressions. **Twin**: a seal whose text is identical to an impression's text.
- **Name seal**: a seal whose text is a name closed by an ending. **Count-line seal**: a seal whose text is only a number and a counted thing, sometimes after a front word.
- **Stand**: the small object on a post drawn in front of the head of the one-horned bull on a square seal. The catalogue sorts its drawing into five letters (W, J, S, I, L); that letter is the **stand letter**. **Round seal**: a seal with a round face or a cylinder that is rolled along clay; both count as round here.
- **Findspot words**: a **building** is one excavated house (excavation area plus house); a **block** is a group of houses; a **room** is a room or grid square in a building; an **area** is a part of the dig; a **trench** is an excavation cut at Harappa; a **locus** is the excavation spot recorded in the second catalogue. **Moulded tablets**: tablets pressed from one mould, identical in text.
- `measured`: a number that comes out of the data on rerun. `guess`: something we act on without a number behind it.

## How pairs are counted

Many findings below count pairs of objects that share something (a sign, a text, a building). Three rules hold for every pair count in this file.

1. **One row per physical object.** The two faces of one stone are not a pair of seals: two faces of one stone always share their findspot and often their letters. Two catalogue rows that describe one stone are merged when they share the site, the full text on every face and the excavation number (plate reference cut off), there are exactly two rows under that number, and the sizes agree within 1.0 mm. This merges 3 pairs in the whole catalogue, all Harappa tablets (H-316 = H-1304, H-912 = H-1191, H-1150 = row 4409), and no seal.
2. **Chance is drawn only among objects that can carry the property.** The chance figure is made by shuffling the labels (rooms, houses, letters, species) at random among the objects of one stratum (same site, area and depth band), 2,000 to 10,000 times, and shuffling only among objects that can hold the label (stones that have a stand letter for a letter test, stones with a rare beast for a rare-beast test). The chance figure is the mean count over the shuffles; **P** is the share of shuffles at least as extreme as the real count; a **ratio** is the real count divided by the chance figure.
3. **A batch of identical moulded tablets found together counts once.** All objects of one site and findspot that carry the same full text are one copy event.

Every pair count in this file was rerun this way (scripts `work_scripts/recheck_01_room_middle.py` to `recheck_15_copper_lots.py`, with `recheck_common.py` and `recheck_06b_keep_pairs.py`; logs in `work_data/recheck/`; report `jobs/out/recheck.md`). Five findings did not survive and are listed in Part 9: the stand letter as a household mark; seal and tablet with the same count in one area; text twins in the same excavation spot; rare beasts one per building; same-crest and same-house seals sharing a building. Three weakened and say so where they stand: Harappa same-tag seals sharing a trench, the number before a fish shared in rooms, and copper copies in one register lot.

## Part 1. How a text is built

### 1. The template
- Claim: most seal texts run [opener] [name] [ending].
- Number: a parser gives every sign one slot and fits 68.8% of 2,162 distinct texts tightly; roles learned at other sites raise parsing on unseen Mohenjo-daro and Harappa texts by 8 to 11 points; on the second catalogue every sign gets a role in 89.3% of texts and in 85.4% of the 383 texts with no partner in Lipi.
- Means: signs keep fixed positions, and positions learned on one set of texts work on texts that were not used.
- Rerun: `work_scripts/gloss.py`, `work_scripts/gloss2.py`, `work_scripts/second_port.py`.

### 2. A name is crest + personal part + tag
- Claim: a name is up to three signs; the first is a house emblem, the last goes with the ending.
- Number: same fish variant first in a name for 15 of 23 house-mate pairs against 40% by chance (P 0.008); name-slot signs repeat inside houses 19 pairs against 7.8 (P 0.003; dealt within excavation area 8.1); class is a closed set of 26 signs tied to seal size; the name slot holds 384 different signs; a marked fish is a mark plus the plain fish (second sign plain fish in 40 of 528 swaps against 133 of 3,332).
- Means: the first sign works as a family emblem.
- Rerun: `work_scripts/name_slot_build.py`, `name_slot_analysis.py`, `name_slot_analysis2.py`, `sound_fishsplit.py`, `recheck_03_name_slot.py`.

### 3. Endings
- Claim: the text closes with one of a handful of signs, and the closer belongs to the person.
- Number: the jar sign ends 557 of 743 texts; the plain man sign follows the jar 54 times (54 of that sign's 73 texts); spear, porter and comb signs stand in the jar's place (spear after jar 0 of 156 on the second catalogue); the name's last sign predicts the closer, the same name keeps it across seals, house, site, period and object type do not predict it. Median seal face by closer: person 738 mm2, jar 645, spear 633, carrier 495, comb 420. The mix of closers is the same at every site.
- Means: the ending is a property of the person, not of place or object.
- Rerun: `work_scripts/endings_build.py`, `endings_A1.py` to `endings_A6.py`, `endings_B.py`, `closers.py`.

### 4. The "jar then man" ending found in the master's building
- Claim: texts of the form [name X] jar man mark a person attached to another owner X.
- Number: these seals carry an animal 91% of the time against 78% (their larger median face, 778 mm2 against 652 for name + jar, is text length: see Part 9); the names X are fish-crest names 18 of 50 against 7 of 602 for owners; at Mohenjo-daro 5 of 24 such seals sit in a building that also holds an owner object with X's crest, against 2.10 by chance (P 0.046), family members at chance (44 of 588 against 49.5); agent seals have a larger raw median face (718 against 581 mm2, before text length is counted); goods tags are stamped by such persons 20% against 7% for seals.
- Means: the man ending marks someone who lives where the owner's objects are.
- Rerun: `work_scripts/masters_1.py` to `masters_13.py`, `possessive_A.py`, `possessive_A2.py`, `registry_tests.py`, `recheck_04_manager.py`.

### 5. Seals from one room share signs
- Claim: the middle of a seal text belongs to the household.
- Number: seals from the same room at Mohenjo-daro within 3 ft of depth share an uncommon middle sign about 7 times as often as chance (5 pairs against 0.67, P 0.0007; taking the middle face by face, 4 against 0.68, P 0.007), first and last signs no excess; across all same-house pairs of seals ending in the jar, the sign before it is shared in 17 pairs against 10.7 (P 0.048). On photographs of house-mate pairs the shared sign is on both stones in 24 pairs and cut by the same hand in 4.
- Means: different carvers wrote the same sign for the same house.
- Rerun: `work_scripts/gloss_report.py`, `pre_jar.py`, `recheck_01_room_middle.py`, `recheck_02_photo_pairs.py`, `recheck_13_other_pairs.py`; photo pairs in `jobs/out/photo_pairs_A.md`, `photo_pairs_B.md`.

### 6. The seven-city opening and the nine-city pair
- Claim: two formulas travel across houses and cities.
- Number: the opening 920-060-741 is on 38 objects in 7 cities, 24 at Mohenjo-daro (14.5 expected), 36 different names after it on 38 stones, 29 of 38 are seals (76% against 48%). The pair 590-390 is on 71 objects in 9 cities (8 named sites and one stone of unknown find place); its 22 Mohenjo-daro seals with a recorded house sit in 21 different houses (same-house pairs 1 against 1.84).
- Means: they behave as an office or trade line, not as a family name.
- Rerun: `work_scripts/travelled_1_table.py`, `travelled_2_tests.py`, `travelled_3_prefix.py`.

### 7. A fixed sign pair
- Claim: the quarter sign (061 or 820) stands right before sign 142.
- Number: 11 of 81 uses against 1.37 expected (P 1.3e-7), at both big cities; Mohenjo-daro's 22 objects with sign 142 carry 13 different crests.
- Means: one fixed phrase repeated across houses.
- Rerun: `work_scripts/registry_offices.py`.

## Part 2. Counting and measures

### 8. Two ways of counting
- Claim: short strokes and full-height strokes are separate series.
- Number: short strokes run 1 to 8 and full-height strokes 1 to 5; a two-sided tablet face is often the cup sign plus 2, 3 or 4 long strokes (107 / 157 / 123 objects; cup plus 1 stroke 4 times).
- Means: there are two counting series. `guess`: they count two kinds of thing.
- Rerun: `work_scripts/counted_common.py`, `counted_series.py`, `counted_table.py`; shapes in `work_data/sign_shapes.csv`.

### 9. Measures in twelves
- Claim: cup counts divide twelve.
- Number: 479 of 481 cup counts are 1, 2, 3, 4 or 6; the count 5 is never written (0 of 206 on the second catalogue). One cup stroke is about 9.2 litres on three measured pots; the six-stroke pot is 55.56 L and the three-stroke pot 27.30 L. Only 49% of container counts fall on 1, 2, 4, 8.
- Means: counts are whole fractions of a twelve-cup unit, and the pots are sized to match.
- Rerun: `work_scripts/measures_1_ceilings.py`, `measures_4_scale.py`.

### 10. Unit order
- Claim: units are written big before small.
- Number: lines with two or more measure signs keep their pair's usual order in 124 of 146 meetings (85%) against 69% with the unit signs shuffled inside each line (P 0.002); the quarter-unit count never reaches 4 and the largest unit never exceeds 5.
- Means: the signs sit on one ladder, as in other account scripts.
- Rerun: `work_scripts/measures_2_order.py`, `measures_1_ceilings.py`.

### 11. Ration arithmetic
- Claim: counts on ration tablets multiply and match.
- Number: 3 diamond-sign heads go with 3 load signs on 22 of 22 tablets carrying both; 3 heads x 4 cups = 12 cups on 21 tablets of one Harappa batch (trench E-11), 2 x 3 = 6 on 5 more; on account objects with two numbers they are equal on 67 of 190 against 52.2 by chance (P 0.006).
- Means: these tablets are small bookkeeping chits with consistent numbers.
- Rerun: `work_scripts/dm_A1.py` to `dm_A6.py`, `dm_B1.py` to `dm_B4.py`, `measures_3_sums.py`.

### 12. Counting before names, and before things
- Claim: an amount comes before its thing; a number inside a name is a fixed part of the name.
- Number: things take the number before them 450 to 220, measure and share words take it after 315 to 49. Inside names, tall two with the plain fish 65 of 73, short two with the marked crest fish 62 of 63 (P 1.6e-28), on new texts 14 of 16 and 17 of 17; room-mates share the number before a fish in 5 pairs against 2.77 (rooms dealt only among the 88 seals that carry a number and a fish, P 0.030; the earlier 0.74 dealt rooms among all seals, so it is weakened); numbers in names bunch on 2 (136 of 191 distinct name texts).
- Means: the number is part of the name there and an amount elsewhere.
- Rerun: `work_scripts/stars_1_split.py`, `stars_2_forms.py`, `stars_5_rooms.py`, `recheck_13_other_pairs.py`.

## Part 3. Pictures and objects

### 13. Picture-side ties on copper tablets
- Claim: the picture on a copper tablet goes with certain signs.
- Number: 11 of 12 tablets showing the elephant carry sign 923 against 14% of pictured copper tablets (P 6e-9); tablets showing the gharial carry sign 255 on 11 of 53 against 3.1 by shuffle (P 0.0002). The elephant ties come from copies of two texts and the 11 gharial tablets are copies of one text, so per distinct text the ties do not hold. On some copies the picture is written as a sign, not one sign for one picture (see 36).
- Means: picture side and sign side go together through few texts.
- Rerun: `work_scripts/sound_v5_job1.py`, `sound_v6_job1_tests.py`.

### 14. The stand letter is the cutting shop's style
- Claim: the one-letter code for the stand in front of the unicorn labels a way of drawing the whole picture; it differs by city and does not follow the household or the text.
- Number: on 60 photographs judged with the letter hidden, the stand's own drawn shape does not follow the letter (17 against 15.6 by chance) but the bull's drawing does (23 of 39 against 16.6, P 0.002); neck folds are on 18 of 22 I and W bulls against 6 of 22 J and S bulls. Each city has its own mix of letters (P 5e-9; small stones are W 40% at Harappa against 20% at Mohenjo-daro). The 61 Mohenjo-daro stones with the most Harappa-like texts are W 62% against 37% for the rest of the city (42% expected from their sizes). Of 23 unicorn stones with sign 405 in the text, 22 are W (14.3 by chance). 180 text features against the 5 letters give one cell at P below 0.001 where 0.9 were expected. Counted once per stone and dealt among lettered stones, seals from the same room share the letter 29.8% against 27.1% (104 pairs, P 0.30), and seals in the same building at about the same depth share it 1.21 times chance (P 0.0085). The species of the animal follows none of crest, first name sign, ending or area (P 0.47 to 0.91).
- Means: the letter is the drawing style of the shop that cut the stone, and the text does not choose it; the species is chosen separately and does not follow the household either. `guess`: seals were cut in city shops working to shared styles, and one text line (sign 405) went to one shop in every city. The earlier reading of the letter as a household mark is in Part 9.
- Rerun: `work_scripts/stand_1_photos.py`, `stand_3b_recheck.py`, `stand_4_cities.py`, `stand_5_text.py`, `animal_base.py`, `animal_2_assoc.py`; report `jobs/out/stand.md`.

### 15. What each kind of object holds
- Claim: object classes have their own signs.
- Number: tags (500, 417, 056, 890, 048, 055, 892), bangles (two-leaf 840, 7.9 times chance), pots (440, 480), ivory rods (comb 400 ends 29% of rods against 2.7% of seals); 91 of 122 single-count pots use tall strokes, owner on 9%; signs 503, 615, 845 sit on copper tablets 4.0, 4.7, 8.4 times chance on new texts.
- Means: object kind predicts content.
- Rerun: `work_scripts/goods_1_signs.py` to `goods_6_reads.py`, `sound_v3_c.py`.

## Part 4. Time and distance

### 16. The system is flat across time
- Claim: nothing in the frame moves with time.
- Number: 2,666 of 4,694 objects dated. Early / middle / late: agent seals 4.5 / 4.2 / 4.5%; fish-crest names 12.3 / 12.5 / 12.5%; office opening 1.4 / 0.9 / 0.8%. The axis works: inscription-only seals at Harappa 14 of 99 to 33 of 98 (P 0.0032). 87 of 122 sign jobs hold in every time bin against 39.2 with jobs shuffled (P 0.001).
- Means: one key reads about six centuries.
- Rerun: `work_scripts/time_1_trends.py` to `time_5_first_writing.py`, `sound_v7_time.py`, `recheck_10_time_early.py`.

### 17. The earliest levels
- Claim: names arrive after counting.
- Number: before the cities, 24 of 35 texts are one sign long and the jar is on 3 of 35 against 896 of 2,122 later (P 1.9e-5); earliest Mohenjo-daro level has a fish crest first in the name on 0 of 38 seals against about 11% later (P 0.042; first catalogue alone 0 of 36, P 0.040).
- Means: the system grew in layers.
- Rerun: `work_scripts/early_1_levels.py` to `early_5_carry.py`, `recheck_10_time_early.py`.

### 18. The jar drops abroad
- Claim: foreign seals follow a different ending.
- Number: jar on 11 of 57 foreign seals, 2 of 25 cylinders (P 0.005); 12 of 17 round seals found in the Gulf, Mesopotamia and Iran carry sign 090 or 091, rare at home.
- Means: abroad, the home ending is replaced.
- Rerun: `work_scripts/abroad_seals.py`, `abroad2_02_foreign.py`.

### 19. The tree-sign line at home and abroad
- Claim: a count-count-tree-sign line stands at home and on a cloth-backed sealing from Iraq.
- Number: the Umma sealing (Ashmolean 1931.120) reads `127 705 002 004 390`; a Salut seal ends `002 004 392`. At home `002-004` is followed by a tree sign in 16 of 20 places; a 4 before a tree sign is 39 of 90 places at home and 3 of 6 abroad (chance 2.8%). Tree sign 390 is counted in lots (86 of 90 counted uses at 3 or more); 407 takes a tall two on 9 of 28 places against 2 of 90 for 390 (P 3e-5). 11 of 5,610 home faces share the tail `002 004 390`, none four signs; the Dholavira stage II seal has it too.
- Means: the sign sequence recurs at home, in Oman and in Iraq.
- Rerun: `work_scripts/abroad2_05_705_390.py`, `abroad3_01_photo.py`, `abroad3_02_match.py`, `cotton_3_fibre.py`.

## Part 5. The frame found by a machine, and written as rules

### 20. A machine with no rules finds the same classes
- Claim: a 10-state sequence model trained on sign order alone, with none of the parser's rules, sorts signs into classes that line up with the hand-written jobs.
- Number: agreement with the hand jobs by sign type 0.266 (a score where 0 is no agreement and 1 is identical grouping; shuffled mean 0.134, maximum 0.200); by sign use 0.486; per use against the parser's job 0.326 (shuffled 0.001). Training: 3,499 distinct first-catalogue texts.
- Means: the job structure is in the order of the signs themselves and does not depend on how the parser was written. The machine also changes the hand frame in three places: "ending" splits into a closer (740, 520, porters) and an after-jar title (400, 090, 527, 621, 679, 565); the slot right after an opener is its own class (002, 060, 741, 742, 368); numbers are not one class (the tall two 032 sits inside fish names). It also finds text types the hand template missed: bare count lines (34 seals, 17 tablets, 9 pots), opener plus count line with no name (33 seals), a lone title sign (18 seals), and name + gate + guard on tablets with no jar. Written as a strict pattern, the hand template fits 40% of seal texts, 46% of tablets and 16% of pots.
- Rerun: `work_scripts/frame_common.py`, `frame_classes.py`, `frame_kmeans2.py`, `frame_predict.py`, `frame_grammar.py`; tables in `work_data/frame/`; report `jobs/out/frame_machine.md`.

### 21. The frame beats 20 decoy job-sets on texts never used, and restores lost signs
- Claim: hand jobs and machine classes predict the next sign better than the same classes dealt to wrong signs, on 482 new lines (389 distinct texts).
- Number: bits per sign on the 482 new lines (389 distinct texts): sign frequency only 7.849; hand jobs 7.661; hand jobs dealt to wrong signs (20 decoys) mean 7.824, best 7.739; machine classes 7.576 and 7.532; sign pairs 6.892. Share of what the sign-pair model knows about order that the classes capture: hand jobs 19.6%, machine classes 28.5% to 33.1%, decoys 2.6%. No decoy of 20 reached the real frame on any score.
- Lost-sign restoration: in 77 texts where the second catalogue has the sign that Lipi lost, the right sign is in the top 5 candidates for 45.5% with hand jobs, 27.3% by frequency and 32.5% for the decoy mean; the job of the lost sign is right 54.5% against 28.6%. Sign pairs plus jobs: right sign first for 32.5%, in the top 10 for 70.1%. Candidates for 1,971 lost signs on 1,417 damaged faces are in `work_data/frame/restorations.csv`. A photo check of 30 restorations: 5 fit the top candidate, 3 fit another sign, 22 could not be judged.
- Means: the order carried by jobs holds on texts no rule was built on, and it narrows what a lost sign can have been.
- Rerun: `work_scripts/frame_predict.py`, `frame_common.py`, `frame2_photos.py`; report `jobs/out/frame_machine.md`.

### 22. Frame v2: 14 written classes
- Claim: a frame of 14 explicit classes (the hand frame plus the machine's three changes and two additions: fish signs as name fronts, tree signs as counted things) holds about a third of the order.
- Number: on the 482 new lines (389 distinct texts), 7.536 bits per sign against 7.849 for frequencies; its 20 decoys average 7.790 and the best reaches 7.671 (0 of 20 reach it). Counted once each (389 texts): v2 7.403 against frequency 7.779, decoys mean 7.690, best 7.564 (0 of 20 reach it); v2's share of what the sign-pair model knows rises from 32.7% to 36.9%. A second-catalogue line can re-read a first-catalogue stone with one sign different; 53 of the 482 lines (11%) have such a near-match, below the 17% that first-catalogue texts show against other stones, and dropping them as well leaves 343 lines: v2 7.606, decoy best 7.722. Share of the sign-pair model's knowledge captured: v2 32.7%, v1 19.6%, machine classes 28.5% to 33.1%, v2 decoys 6.1%. Mixed with sign pairs: 6.881 bits, below sign pairs alone (6.892). Pushed on a held-out half of the first catalogue (14 to 54 classes) it reaches 48.3%; nearly every added class is one frequent sign by itself. Lost sign in the top 5: v2 50.6%, pushed 58.4%, v1 44.2%, frequency 27.3%, decoys 36.0% and 46.7%.
- Strict written patterns (one per text type, fixed before scoring) fit seals 43%, tags 50%, tablets 56%, copper tablets 54%, pots 27%; the decoys fit 7% to 23%.
- Means: the order the machine found is written as rules a person can read, and the rules carry to new texts; beyond about 14 classes the rest of the order belongs to particular signs.
- Rerun: `work_scripts/frame2_common.py`, `frame2_build.py`, `frame2_score.py`, `frame2_kind_redesign.py`, `recheck_12_frame_newtexts.py`; report `jobs/out/frame_v2.md`; the corpus written in classes is `FRAMEBOOK.md` (`frame2_corpus.py`, `frame2_book.py`).

## Part 6. Fixed phrases

### 23. 136 fixed phrases, by a rule set in advance
- Claim: the script has a stock of fixed sign pairs and triples that keep their order.
- Number: the rule was fixed before the run: 8 or more distinct texts, in order 90% or more of the time (against the reverse order), at least 5 times more often than sign frequencies give. It finds 136: 99 pairs, 36 triples, one four-sign run (255-435-690-740). Control: the same rule on texts with the sign order shuffled inside every text, 20 shuffles: 0.45 phrases pass on average (maximum 2). Confirmation on new texts: of 99 testable phrases, 79 are confirmed. In frame v2, the top 40 pairs carry 41% of what sign pairs add over v2 and the top 200 carry 92%; in new texts those 40 pairs occur 151 times in order and 6 reversed. 277 rarer phrases (4 to 7 texts) against about 13 in shuffled texts. 45% of objects carry at least one (seals 53%, copper tablets 71%, tablets 50%, pots 8%). Merging damaged copies of one text and counting each stone once, 134 of the 136 keep 8 or more texts (904-832 and 002-005 drop to 7), and all 136 have 8 or more copy events.
- By place in the text: name 42, front 39, ending 28, count line 27. 118 phrase families, 15 paradigms, 6 numbered series.
- Means: the texts are built from a stock of set phrases, and shuffling the sign order inside texts removes almost all of them (0.45 against 136).
- Rerun: `work_scripts/phrases_common.py`, `phrases_1_list.py`, `phrases_2_atlas.py`, `frame2_phrases.py`, `recheck_11_phrases.py`; report `jobs/out/phrases.md`.

### 24. The phrases do not drift in time, are not tied to buildings, and are nearly absent abroad
- Claim: the phrases are city-wide and constant over six centuries.
- Number: 86 of 101 occur in all three time bins; 2 show a trend at P 0.05 against 5.1 expected. Shared-building pairs among phrase carriers, identical tablets from one room counted once: 108 against 111.1 expected; rarer phrases 5 against 5.6. 39 phrases occur in 5 or more cities. Only 6 of 41 objects found abroad carry any of the 136, against 45% at home. 920-060-741 is a heading over many different texts: what follows it is as varied as under any other front word (94.6% distinct texts against 96.2%); no building repeats it (0 against 0.98); the unicorn is on 22 of 29 of those seals against 56% (P 0.021). Six phrases are goods phrases (740-400, 176-740, 752-740, 235-705-033, 845-407, 142-617); 740-400 is a Harappa tablet ending (245 objects, 213 at Harappa).
- Free variants: the ward-slot signs 741, 742, 745 and the front words 861, 817, 820 show no difference by city, object kind, time or animal. After the jar, signs 400 and 090 differ on everything (P 0.0002).
- Means: phrases are shared across houses, not owned by one; texts written abroad use the signs but not the home phrases.
- Rerun: `work_scripts/phrases_3_kinds.py`, `phrases_3b_pooled.py`, `phrases_4_cities.py`, `phrases_6_office.py`, `phrases_7_minor.py`, `phrases_8_time.py`.

### 25. Three ways of writing numbers, depending on what follows
- Claim: the same count is written in a different stroke form depending on the next sign.
- Number: before a fish sign the tall two (56%); before the tree signs short strokes (4, 3, 6, 5); before the cup tall strokes. Frame v2 splits numbers three ways (short, tall, and the tall two that lives in fish names). In names the stroke form is locked to the fish (see 12).
- Means: a number is read together with its neighbour, and the form carries information about the neighbour.
- Rerun: `work_scripts/phrases_5_families.py`, `phrases_5b_variants.py`, `phrases_5c_series.py`, `frame2_common.py`.

## Part 7. Seals, clay impressions and tablets

### 26. Two kinds of seal: name seals and count-line seals
- Claim: besides name seals, 75 undamaged seals carry only a count line: 32 as [front word][slot][number][counted thing], 43 as a bare [number][counted thing].
- Number: the counted things are the tree signs 390, 405, 407 and the porter-with-jars 156; the number is mostly 3. With jobs dealt to wrong signs this kind nearly vanishes (1.0 seal on average). The text of a count-line seal also appears on a clay sealing or tag 16 of 75 times (21.3%) against 20 of 609 (3.3%) for name seals (P 1.2e-7), after dropping 18 seals whose only match is a second-catalogue sealing at the seal's own site; with first-catalogue impressions only it is 14 of 75 against 4 of 609 (P 2.4e-11). The matches rest on 4 distinct impression texts. In the stamp job, one row per seal stone and matched to length against other seals: 12 of 44 (27.3%) for count-line seals against 4.3% (P 0.0005). The cup 700 never appears on them. Jar + man texts are 5.4% of impressions against 2.5% of seals (P 0.010).
- Means: count-line texts turn up on clay impressions far more often than name texts do. `guess`: a count-line seal is a quantity stamp.
- Rerun: `work_scripts/frame2_seals.py`, `stamps_4_counts.py`, `stamps_5_more.py`, `recheck_08_countline_impressions.py`; reports `jobs/out/frame_v2.md`, `jobs/out/stamps.md`.

### 27. Seals matched to their clay impressions
- Claim: the stone that made an impression is almost never among the excavated seals; the text belongs to many stones, the animal to one.
- Number: 262 tag faces and 74 stamped pots were taken as impressions. For impressions of 3 or more signs every seal with the identical text is in another city (13 of 13); at 2 or more signs 18 of 24 are in another city and none in the same building. Only 6 of 24 have a twin in their own city against 16.2% for a random seal of that length. Twin pairs carry different animals 15 times and the same animal 19 times. Shuffling signs inside texts gives 6.1 matches against 24 real.
- Multi-stamp lumps: 33 objects carry several impressions, typically a name or jar-man stamp plus a short front-word stamp (861-002 plus one sign, or 317-920-002), sometimes with a 055 stamp.
- The backs: tag subtype letters match the backs in 20 photographs: B wooden box, P plain token, L soft package (cloth, reeds, cords), R storage jar. Count lines sit on L 5 of 40 faces against 2 of 296 elsewhere (P 0.0003); jar-man texts on L 7 of 40.
- Lothal warehouse square: 7 different texts on 15 faces against 12.94 by chance (P 0.0002), one jar-man stamp 8 times, the matching seals at Mohenjo-daro. Kalibangan KLB-1: 2 texts against 7.36 (P 0.0002).
- Means: goods were stamped by senders in other cities; a transaction left two or three stamps on one lump. `guess`: a store holds a few senders each stamping many packages.
- Rerun: `work_scripts/stamps_1_build.py` to `stamps_7_clusters.py`, `recheck_13_other_pairs.py`; tables in `work_data/stamps/`.

### 28. Tablets as issue chits
- Claim: a name keeps its own amount on tablets.
- Number: 816 of 902 multi-face tablets are readable: amount + name 356 (343 at Harappa, 5 at Mohenjo-daro); name + thing 176; amount + thing 94; name + name 88. A name keeps its own amount: 38 against 21.6 (P 0.003; 10 of the 38 pairs come from one text, 176-740-400 with 033-700, found in five Harappa trenches); the same name with a different amount in one trench: 9 pairs against 3.4 (P 0.011; 7 against 2.9, P 0.023, when 034-700 and 700-034 are read as one amount). The cup ceiling holds on all 902 (1, 2, 3, 4, 6).
- Means: the tablets behave as records with a fixed amount per named line. `guess`: Harappa tablets are issue chits, a fixed amount per named recipient. The earlier pairing of seals and tablets with the same count in one area did not survive the recheck (Part 9).
- Rerun: `work_scripts/spots_3_records.py`, `spots_3b_rescue.py`, `stamps_4_counts.py`, `recheck_06_tablets.py`.

### 29. Jar + man seals near the same crest, and the quarter pair with a count
- Claim: seals of the form [crest] jar man sit near objects of the same crest, with a limit at Harappa; the pair 061/820 + 142 takes a count in front.
- Number: at Mohenjo-daro 5 of 24 share a building with an owner object of the same crest (2.10 by shuffle, P 0.046); at block level 9 of 24 against 5.30 (P 0.045); pooled over cities at block level 11 of 30 against 6.36 (P 0.027). Those buildings hold 8 same-crest objects against 2.84 (P 0.022), with the two moulded tablets M-431 and M-432 counted once. Their larger raw median face (Mohenjo-daro 778 mm2 against 629) is text length, not a size effect (Part 9). At Harappa the building test is 0 of 6; with all object kinds the mound matches 18 of 31 against 14.84 (P 0.030). They do not copy the master's stand pattern or animal (chance); they carry stand S or J on 15 of 21 against 47% of all unicorn seals (P 0.021).
- 061/820 + 142: a count (1, 2, 3) stands right before the first sign in 5 of 11 pair texts against 9% elsewhere (P 0.003); 10 of 11 end in the jar; the text 061-142-400-740 is identical on four objects in two cities.
- Means: these seals sit in the same places as their crest's other objects at Mohenjo-daro and not at Harappa; the quarter pair behaves as a numbered post.
- Rerun: `work_scripts/spots_1_manager.py`, `spots_1b_rescue.py`, `spots_2_office.py`, `registry_offices.py`, `recheck_04_manager.py`.

## Part 8. How seals were made, and what the seals say about their makers

### 30. How a seal was made
- Claim: the text was cut first and the animal added after; no building had its own cutter.
- Number: photographs exist for 1,600 of 2,290 seal faces, and about 754 panels were opened. Of 60 stones the size of an animal seal with no animal, 6 have the text cut and the animal field left smooth (L-55, L-58, L-97, M-315, M-1195, M-1232), 27 are text-only by design, 3 worn or broken, 4 hairline sketches, 20 cannot be told; one stone has the animal cut and the text field empty (K-35). Text first against animal first: 6 to 1. Lothal holds 3 of the 6, and no two share a house. Four stones carry signs drawn in thin scratches (C-31, H-613, L-62, M-1228, the last with a few signs already cut deep). Judged blind on photographs, with pair kinds looked up after all 120 were judged: pairs from different cities that share a text are alike in hand 7 of 37 (19%) against 4 of 32 (12.5%) for pairs sharing nothing (P about 0.3). At Mohenjo-daro the same hand appears for same-building pairs 8 of 35 (23%), same-area different-building pairs 7 of 31 (23%) and different-area pairs 4 of 19 (21%).
- Means: a stone was blocked out with a thin drawing of the text, the text was cut, and the animal came last; the same-hand rate does not rise with sharing a building, so cutters served a city, not a house. `guess`: seals were cut in city shops working to shared styles.
- Rerun: `work_scripts/hands_1_candidates.py`, `hands_1b_tally.py`, `hands_2_pairs.py`, `hands_3_xc_score.py`, `hands_4_md_score.py`, `hands_5_order.py`, `hands_6_relook.py`; report `jobs/out/hands.md`.

### 31. Round seals are a different kind of text
- Claim: round seals (including cylinders) carry texts built differently from square seals, at home as well as abroad.
- Number: 41 round faces on 39 objects (13 home, 18 abroad, 7 with no findspot, 1 Daimabad; 9 are cylinders). A short stroke right before a person sign (001-090, 055-090, 001-091) is in 6 of 37 round texts against 1 of 3,426 distinct non-round home texts (P 1.6e-10); among round texts with both a person sign and a stroke, 9 of 10 put them side by side (5.5 when shuffled). The man sign 090 ends the text in 2 of 10 round uses against 61 of 81 home uses; the [crest][jar][man] order is in 0 of 37. Under a sign-pair model trained on home texts, the 15 round seals found abroad cost 9.52 bits per step against 5.74 for home texts matched on kind, length and animal (range over 2,000 draws 4.75 to 6.84), and worse than sign frequencies alone (8.32); the 15 round seals found at home cost 8.15 against 5.68. Round seals hold a home phrase 1 of 18 times (8.4 expected); none of 9 intact ones ends in a closer (6.3 expected); 48.5% of their signs are person signs and strokes against 18.3% (090 seven times against 0.8; 091 five times against 0.02). Home round seals differ from foreign ones: person signs 2 of 56 signs against 18 of 97; short-horned bull 3 of 15 faces against 16 of 25; strokes alike (28.6% against 30.9%). Round texts share an ordered sign pair with a clay impression 8 of 37 times against 21.0 for matched square seals.
- Means: shape decides, not findspot or animal: the 87 home short-horned-bull seals read as ordinary (5.79 against 5.66 bits per step). The stroke + person unit is not part of the home system. `guess`: round stamps carry a unit [stroke][person] for a local record of persons with a number.
- Rerun: `work_scripts/round_01_list.py` to `round_09_unit_search.py`, `abroad4_09_roundcomp.py`, `abroad4_10_roundprofile.py`; reports `jobs/out/round_seals.md`, `jobs/out/abroad_frame.md`.

### 32. Square seals found abroad read like home seals
- Claim: square seals, pots and tags found abroad are home texts that travelled.
- Number: square seals abroad cost 6.58 bits per step against 6.03 for matched home texts (P 0.20); 4 of 15 hold a home phrase against 4.7 expected; home phrases abroad are in home order (12 matches against 2.3 shuffled; reversed 1 against 2.3); their closers stay (5 of 8 against 4.1). Kish and Gonur Depe both carry `590-390-740`. No foreign text has an identical or one-sign-off home twin (0 of 19).
- Means: the square seals found abroad follow the home sign order, with the round seals as the exception (31).
- Rerun: `work_scripts/abroad4_01_set.py` to `abroad4_11_twins.py`; report `jobs/out/abroad_frame.md`.

### 33. The same text on several stones
- Claim: stones with one text are close in size and carry animals chosen separately; how often a text is repeated depends on its kind.
- Number: 71 sets of seals with an identical complete text in the first catalogue, 124 sets (329 stones) with the second; above chance from 4 signs even against a generator that keeps short-range order (at 2 to 3 signs grammar alone gives many: 25.5 of 37; 10.2 of 14). Twin pairs sit close in size, 71% against 88% when shuffled within site, length and format (P 0.016); across time bins 48% against 88% (P 0.004). Among 45 twin pairs with a beast on both and not both unicorns, the species matches 0 times (0.91 expected); across time bins the animal is shared at chance (17 against 16.6). Twin rate by kind of text against the rate expected from length: count lines 2.05 times, name + closer 1.41, bare names 0.42, name + title 0.17, front formulas 0.68. Photographs of 29 twin pairs: 8 cut by the same or a near-same hand, 21 by different hands, 24 sharing the layout. L-55 (Lothal) is an unfinished copy of L-35: text cut, animal field blank.
- Means: size goes with the text and holds across generations, the animal is chosen fresh for each stone, and a count line is repeated more than a name. `guess`: a count line is a standard stamp, and a name + closer text is held by several people at once.
- Rerun: `work_scripts/twins_1_build.py` to `twins_6_redesign.py`, `recheck_07_twins.py`; report `jobs/out/twins.md`.

### 34. The comb ending is a small-seal class, and comb names barely meet man names
- Claim: seals ending in the comb sign are about half the size of other jar-final seals, and names that end in the comb are almost never the names that end in the man sign.
- Number: the comb sign 400 after the jar has the most negative size weight of any sign (-0.185, about 17% smaller; 90% interval -0.247 to -0.114). Seals ending `740-400` sit at residual size -0.653 against -0.004 for other jar-final seals of the same site, length and format, at Mohenjo-daro, Harappa, Chanhu-daro and Kalibangan. Comb seals are 0.48 times the face of jar-only seals; man-ending seals are the same size as jar-only. Of 71 distinct names on Harappa tablets ending `740-400`, 20 also appear on seals, and 4 of 59 of those seals end in the comb against 0.70 with seal endings shuffled inside each city, identical seals in one trench counted once (P 0.003). Names written with two different endings, identical tablets in one place counted once, against endings shuffled within city and object kind: comb + man 4 against 12.1; jar-only + comb 33 against 57.4; jar-only + man 14 against 27.5 (all P 0.0005). The seated-person sign 176 heads 22% of comb names against 3% of jar-only names; fish crests head 8% against 25%.
- Means: the comb ending marks a class of holders with half-size seals, and comb and man are different sets of people; comb and man are the most separate pair of the three. `guess`: comb persons draw ordinary cup issues from city-wide offices.
- Rerun: `work_scripts/size_2_ladder.py`, `size_8_decide.py`, `chits_1_titles.py` to `chits_7_time.py`, `recheck_14_chits.py`; reports `jobs/out/size.md`, `jobs/out/chits.md`.

### 35. Tablet size follows the name, not the count
- Claim: a tablet's size is set by the name written on it.
- Number: with the name fixed, size does not move with the count (rank correlation +0.005); with the count fixed, the name holds 79% of the size spread against 32% when names are shuffled.
- Means: tablets were made to a size for the named line, not for the amount.
- Rerun: `work_scripts/size_7_tablets.py`; report `jobs/out/size.md`.

### 36. Copper tablets as records
- Claim: a copper tablet text goes with one picture, and the copper tablets count in the big measure, not in cups.
- Number: read by eye, 21 of 21 same-text pairs show the same picture against 0.059 with pictures dealt at random, and all 12 texts with two or more legible copies have one picture each; the reverse is loose, with 8 of 13 pictures covering two or more text families. Among faces with a count, per copy: the cup sign 700 is on 2 of 58 copper faces against 430 of 530 Harappa clay tablets; the big measure 705 on 20 of 58 against 10 of 530; 706 on 14 of 58 against 1 of 530; the tree sign 407 on 12 of 58 against 2 of 530; no tree 390 and no porter 156 on copper. Eight text families have copies with one sign where the picture should be; 26 of those signs' 29 uses are on picture faces (0.016 for signs of the same rarity), and the ties are not one to one (777 stands in for the archer on 1 copy and the goat on 4). Copper names appear on Mohenjo-daro seals 4 of 29 times against 20.7% for random seal names. Copies of a set lie in the same register lot 2 pairs against 0.52 (P 0.075) once three tablets listed twice (a corpus row and a dig-report plate row) are merged, and 6 against 0.83 if those are separate tablets; the copies are not in the same area (chance).
- Means: the picture heads a class of record and the text names the line inside it; copper copies were made in batches and spread over the city; copper names are not seal names. `guess`: a copper tablet is a token of a standing allotment handed to many holders.
- Rerun: `work_scripts/copper_1_table.py` to `copper_9_vocab.py`, `recheck_15_copper_lots.py`; report `jobs/out/copper.md`.

### 37. Seal size is mostly the stone's own style
- Claim: the stone's own marks (stand letter, animal, material) carry more of a seal's size than its text does.
- Number: held-out share of size variation, mean of 20 splits: length 0.109; plus site and format 0.285; plus one weight per sign 0.301; plus stand letter, animal and material 0.400; the stone's marks alone 0.387. On one split the per-sign weights lift 0.294 to 0.309 and beat the baseline in 20 of 20 splits by +0.018 on average; signs swapped for others of the same frequency give 0.292 (best 0.295; 0 of 20 reach 0.309). W stands give a stone 28% more area than its text predicts and I stands 21% less. Inscription-only stones are smaller than their beast twins in 27 of 39 twin pairs. Seals carrying one of the 25 smallest signs sit above their median 37.2% of the time on held-out seals (71 of 191, P 0.00024); the big end leans only (54.8%, P 0.16). Crest houses differ in size more than shuffled house labels give (20.67 against 12.88, P 0.0015); goods signs as name fronts (700, 407, 440, 590) are the small houses.
- Means: seal size is mostly the kind of stone and the workshop's style, with a small rank part readable from a few signs.
- Rerun: `work_scripts/size_1_models.py`, `size_2_ladder.py`, `size_4_crests.py`, `size_5_marks.py`, `size_8_decide.py`; report `jobs/out/size.md`.

## Part 9. What was tested and did not hold

Each line gives the number and the script. These are results of the tests as run.

### The sign-by-sign words
- Four decoy results. (a) Blind decoy test: 60 signs, 30 with their accepted word and 30 with a word moved from another sign of the same job; predictions written first by two blind testers. Came true: accepted 9 of 58 (15.5%), decoy 10 of 60 (16.7%). (b) Same test with the full method (look at the data, predict, one redesign): accepted 17 of 29, decoy 19 of 30. (c) Three blind readers graded 60 whole inscriptions turned into English four ways: sense for the real word list 35% to 37%, for words dealt among signs with the same job 27%, freely dealt 10% to 17%, dealt among equally common signs 7% to 8%. (d) Forced choice, 120 inscriptions, pick the real line of four (chance 25.8%): real picked 29.2% pooled, the two same-job shuffles 34.2% and 22.2%, free shuffle 14.4%. So a wrong word of the same job passes as often as the accepted word. Scripts: `work_scripts/decoy_build.py`, `decoy_test_A.py`, `decoy_test_B.py`, `decoy_replay_A.py`, `decoy_replay_B.py`, `decoy_score.py`, `blind_build.py`, `blind_score.py`, `blind2_build.py`, `blind2_score.py`.
- A time test of the assigned jobs: of 122 values with dated uses, 87 do their job in every time bin against 39.2 with jobs shuffled; four fail in every bin (482, 575, 850, 717) (`work_scripts/sound_v7_time.py`).

### The language
- Two machine runs, 19 dictionaries in 7 families, sound-alike rule scored against controls. Run 1 (`work_scripts/lang_m_common.py`, `lang_m_score.py`): 0 of 312 cells beat all three controls at P below 0.05. Dravidian family, strict match, narrow keywords: 42 of 63 picture-and-job units match; jobs dealt at random 38.4 (P 0.045); the dictionary's sounds dealt at random 43.5 (P 0.72). The one lean (cells beating the outside-noun and scrambled-sound controls but not the job shuffle): Dravidian 10 of 96, Indo-Aryan 2 of 48, Munda 1 of 60, Sumerian 1 of 36, Akkadian, Elamite and Burushaski 0.
- Run 2, with pictures described blind (172 units from 235 signs), the machine's ten classes and dictionaries that keep same-spelled words apart (`lang_m2_common.py`, `lang_m2_score.py`, `lang_m2_swaps.py`, `lang_m2_c4check.py`): combined score per family (mean z against scrambled sounds) and shuffle P: Dravidian -0.20 (0.82), Munda -0.04 (0.53), Indo-Aryan -0.56 (0.97), Sumerian -0.06 (0.55), Akkadian -0.34 (0.66), Elamite +0.31 (0.16), Burushaski -0.38 (0.79); the bar was P below 0.007. The lean fell to 3 of 96 Dravidian cells. A first positive, right class against wrong class for the same picture (Dravidian P 0.0005), vanished once each dictionary's own rate of keyword words per class was allowed for (P 0.66 to 0.98).
- Sign swaps (pairs of differently drawn signs that replace each other): run 1 Dravidian picture names sound alike in 16 / 58 / 63 of 65 (strict / medium / loose) against 17.1 / 56.7 / 64.5 dealt at random; run 2, 40 / 89 / 108 of 108 against 39.4 / 89.4 / 106.9.
- Means: at the strength of the test, every family is at chance, and the language of the script is not identified.

### The outside match in cuneiform
- Of 585 CDLI tablets from Girsu, Lagash and Umma naming Guabba or Meluhha, 33 are sealed, 13 are Meluhha or textile texts, and all 13 seal legends are cuneiform. Foreign texts are not more lot-like than home texts (49% against 45%). The sesame sign 838 is on 0 of 69 foreign objects. No text puts a jar word on a line with Dilmun, Magan or Meluhha (918 texts). No Meluhha-tagged cloth word in 202 CDLI Meluhha texts; loan candidates 196 against 139 by shuffle (P 0.07). Scripts: `work_scripts/abroad3_04_cdli_east.py`, `abroad3_05_seals.py`, `abroad3_07_seal_legends.py`, `abroad2_14_sesame838.py`.

### One office-holder per city area; one phrase per building
- Holders of the sign pair 061/820 + 142 spread one per city area: 35 against 35.0 expected; 14 blocks against 13.6 (`work_scripts/spots_2b_spread.py`).
- A phrase belonging to one building: shared-building pairs 108 against 111.1 with copies removed; the three phrases that first looked house-bound lose it (P 0.34, 0.13, 0.016). This also cuts against "a house is one building" as a general rule (same-house seal pairs sharing a building: 1.31 times chance at Mohenjo-daro once each stone counts once, P 0.15) (`work_scripts/phrases_3_kinds.py`, `registry_tests.py`, `recheck_05_crest_tag_pairs.py`).

### Pair counts that fell in the recheck
Each entry gives the old figure, the fault, and the clean figure under the rules in "How pairs are counted".
- The stand letter as a household mark. Old: seals from the same room share the letter 38.1% against 17.2% (139 pairs, P 0.0003), fading with distance (room 1.79, block 1.27, area 1.13), independent of crest (P 0.91). Fault: two faces of one stone were counted as a pair (such a pair always shares), and letters were shuffled among all beast seals, not only stones that carry a letter. Clean: same room 29.8% against 27.1% (P 0.30); same building 29.4% against 27.4%. What remains is a lean: same building at about the same depth 1.21 times chance (P 0.0085), same building far apart in depth 1.03. Scripts `work_scripts/animal_4_pairs.py` (old), `stand_3b_recheck.py` (clean).
- Seal and tablet with the same count of the same thing in one area. Old: 89 against 69.5 (P 0.003). Fault: each of 29 and 17 identical tablets in Harappa F Trench I was counted as its own record beside two seals reading 033-700 and 034-700. Clean: 43 against 43.7 (P 0.59); with identical seals in one trench also counted once, 28 against 28.3. Scripts `stamps_5_more.py` (old), `recheck_06_tablets.py`.
- Text twins in the same excavation spot, second catalogue. Old: 48 against 28.6 (P 0.004). Fault: five two-sided objects (1412, 2220, 2339, 2505, 2508) carry the same two texts and each pair was counted once per face, 10 extra counts; and batches of one text in one locus were counted stone by stone. Clean: 42 against 26.1 (P 0.005) with each pair of objects once, and 24 against 20.1 (P 0.15) with a batch of one text in one locus counted once; 34 of the 42 pairs sit in Mohenjo-daro locus 31, which holds 505 of the 1,232 seals of that catalogue. The stand letter shared by twins in one city but different buildings is 9 of 22 against 6.4. Script `recheck_07_twins.py`.
- Rare beasts, one per building. Old: two rare-beast seals in one building are the same species 13 against 20.8 (P 0.085). Fault: species were dealt among all seals of a city, unicorn and bare seals included, which also changed how many rare-beast pairs exist (117.8 dealt against 91 real). Clean, species dealt only among rare-beast stones: 13 against 16.1 (P 0.25); within city and format 13 against 16.0. A lean stays: buildings hold fewer rare-beast pairs than chance, 91 against 117.7 (P 0.078). Scripts `stand_6_animals.py` (old), `recheck_09_rare_beasts.py`.
- Same-crest and same-house seals sharing a building. Old: same crest 1.43 times chance (28 against 19.5), top-20 houses 1.41 (23 against 16.3, P 0.08). Fault: 15 stones sit twice in the people table, and 2 of the 28 same-crest pairs were one stone paired with itself. Clean, at Mohenjo-daro: same crest 1.26 (24 against 19.1, P 0.16); top-20 houses 1.31 (21 against 16.0, P 0.15); same tag 1.16 (16 against 13.8, P 0.32). "A house is one building" has no number behind it. At Harappa, same-tag pairs share a trench 1.53 times chance (27 against 17.6, P 0.033), down from 1.68 (32 against 19.1). Script `recheck_05_crest_tag_pairs.py`.

### Other readings that did not hold
- A ladder of title signs that keeps its order across cities: on the 8 title and closer signs with 3 or more seals in both cities, the Mohenjo-daro against Harappa rank correlation of size weights is -0.10, while random sets of other signs give 0.35 (88% at or above); with 5 or more seals both sides -0.03 against 0.54; with 8 or more 0.20 against 0.69 (`work_scripts/size_3_titles.py`, `size_3b_redesign.py`).
- [Crest][jar][man] seals being bigger once length is counted: the median face gap (778 against 652 mm2) is text length; `740-090` seals sit at -0.020 against -0.004 for jar-final seals (46 seals). Also: big-seal houses having more jar + man seals, cities or impressions; size helping to restore lost signs; W as the late stand (42 / 40 / 47% early / middle / late); the earlier "8% smaller tablet per stroke" (it was a difference between names) (`size_2_ladder.py`, `size_3_titles.py`, `size_4_crests.py`, `size_7_tablets.py`).
- The short-horned bull as an overseas mark: 14 of 26 beast seals abroad against 92 of 1,575 at home (P 7e-11) is the count, but 13 of the 14 short-horned-bull seals abroad are round, and the 87 short-horned-bull seals at home read as ordinary (5.79 against 5.66 bits per step). The bull follows the round shape, not the place (`animal_7_abroad.py`, `abroad4_09_roundcomp.py`).
- "The picture on the back of a copper tablet spells a word in the text": the picture-replacing signs do not stand one for one for a picture (777 stands in for the archer on 1 copy and the goat on 4); the earlier "341 stands for the stag" rests on a near text only, and a third copy is coded rhinoceros; copper names are not seal names (three ways) (`copper_4_picsign.py`, `copper_5_swaps.py`).
- Round seals as sound-spelling: their sign frequencies are less flat, not flatter; repeats are few; they share no runs of neighbouring signs with each other (0 against 8.0) (`abroad4_10_roundprofile.py`, `round_07_verdict.py`).
- Text-sharing pairs across cities being cut by the same hand more than unrelated pairs (7 of 37 against 4 of 32, P about 0.3); a building effect on hands; guide lines or ghost signs on finished stones (none in 40); twins sitting in other cities more than chance (77 same-city against 69.0); one holder's several stones having related texts (3 against 5.0); twins carrying more unfinished or bossless stones (`hands_2_pairs.py`, `twins_4_more.py`).
- Comb-name leads: amounts marking the class (mean cups comb 2.97, jar-only 2.92); comb names keeping one amount; a trench having its own issuer's mark; names tied to one trench (2.54 trenches per name against 2.56) (`chits_3_amounts.py`, `chits_4_batches.py`).

### Other lines that went against
- Frame: for the single best guess at a lost sign the frame is no better than its decoy (18.2% against 17.3%); on new tablets and copper tablets the class grammars do not beat frequency; the sign-pair model beats every class grammar; grammars learned per object kind lose to the pooled table on new seals (7.455 against 7.374 bits) (`frame_predict.py`, `frame2_kind_redesign.py`).
- Count-line seals differing from name seals in size (once length is matched), animal, findspot, time or being abroad; the short-horned bull is rarer on them (1.3% against 4.6%) (`frame2_seals.py`).
- Stamps: the stamping stone staying in the same city as its impressions; office front and travelling names over-represented on impressions; stores receiving from many houses; city-to-city links above chance overall (13 against 16.7) (`stamps_2_match.py`, `stamps_3_cities.py`, `stamps_5_more.py`, `stamps_7_clusters.py`).
- Records and seals: amounts drifting with depth; jar-man seals copying the master's stand pattern or animal (`spots_3b_rescue.py`, `spots_1b_rescue.py`).
- Ration size following rank; total lines (one number equal to the sum of the others 10 of 70 against 14.9); batch totals in whole large units (0 of 16) (`measures_3_sums.py`, `measures_5_rank.py`).
- Administration thickening with time; a trade peak for the overseas bull (`time_3_redesign.py`).
- Numbers in names bunching on 3, 6, 7 (`stars_2_forms.py`).
- "Servant of a house-mate" and "head of his own house" for the man ending: 4 of 20 against 3.3 (`endings_A1.py` to `A6.py`).
- Animal as clan, ward or rank (`animal_2_assoc.py`).

## Appendix: labels (the only place words appear)

Every English or Dravidian word placed on a sign in `work_data/values_master4.csv`, `CORPUS.md`, `READINGS.md` and `WHOSWHO.md` is a working label for the sign's job. The decoy tests (`jobs/out/decoy_test.md`; section 'The sign-by-sign words' above) found a wrong word of the same job passes the confirming procedure as often as the accepted word (9 of 58 against 10 of 60 blind; 17 of 29 against 19 of 30 with the full method), so the exact words are not established. Labels used in this book's numbers:

| Sign | Job in this book | Label |
| --- | --- | --- |
| 740 | closing sign | "of / house of" (kuṭi) |
| 090 | sign after the jar | "man, manager" (āḷ) |
| 220 | fish crest | "star" (mīn) |
| 520 | spear, closer | "chief" (vēḷ) |
| 861 | diamond, head count | "hand" |
| 390 | tree, counted in lots | "cotton" (parutti) |
| 407 | tree, counted by piece | "cloth", then "kindred" (kiḷai) |
| 705 | measure sign | "grain measure" (kalam) |
| 142 | after the quarter sign | "king" (kō) |
| 061 / 820 | quarter sign | "quarter" (kāl) |
