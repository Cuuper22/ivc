# The frame: what is measured about the Indus script without any word

Every finding below was counted from the sign catalogues with no word attached to any sign, and reruns from the script named under it. Each has four parts: the claim, the number, what the number means, the script. Dates are 2026-11-17. Part 5 onward holds the findings of the machine frame, the fixed phrases, the stamps and the records; the section after them lists what was tested and did not hold. For the one place where words appear, see the Labels appendix at the end.

## Terms

- **Seal**: a small stone or clay stamp with a few signs. **Tablet**: a small flat plaque of clay, stone or copper. **Tags, pots, rods**: other inscribed objects. **Face**: one inscribed side; this book counts faces.
- **Sign**: one drawn character, cited by catalogue number (740 is a jar picture, 220 a fish picture).
- **Lipi catalogue**: the main catalogue (5,679 faces, 2,162 distinct complete texts). Texts are stored in reverse of reading order; everything here is in reading order.
- **Second catalogue**: Mahadevan 1977, a separate transcription linked to Lipi by a 366-pair crosswalk. **New texts**: its 1,183 texts with no partner in Lipi, never used to shape any rule.
- **Crest**: the first sign of a name. **House-mates**: two seals found in the same excavated house. **Job**: the role a sign plays in the text shape.
- **Bits per sign**: how many yes/no questions, on average, a model needs to guess the next sign of a text it never saw; lower means the model knows more about the order of signs. **Sign-pair model**: a table of which sign follows which sign; it is the yardstick for "how much of the order is known".
- **Class**: a group of signs that do the same job in the text. **Decoy job-set**: the same classes with the same sizes, dealt at random to the wrong signs of the same frequency; a real frame must beat its decoys.
- **Impression**: clay pressed with a seal and left on goods. **Sealing / tag**: a lump of clay over a knot, lid, jar mouth or door, carrying impressions. **Twin**: a seal whose text is identical to an impression's text.
- **Name seal**: a seal whose text is a name closed by an ending. **Count-line seal**: a seal whose text is only a number and a counted thing, sometimes after a front word.
- `measured`: a number that comes out of the data on rerun. `guess`: something we act on without a number behind it.

## Part 1. How a text is built

### 1. The template
- Claim: most seal texts run [opener] [name] [ending].
- Number: a parser gives every sign one slot and fits 68.8% of 2,162 distinct texts tightly; roles learned at other sites raise parsing on unseen Mohenjo-daro and Harappa texts by 8 to 11 points; on the second catalogue every sign gets a role in 89.3% of texts and in 85.4% of the 383 texts with no partner in Lipi.
- Means: signs keep fixed positions, and positions learned on one set of texts work on texts that were not used.
- Rerun: `work_scripts/gloss.py`, `work_scripts/gloss2.py`, `work_scripts/second_port.py`.

### 2. A name is crest + personal part + tag
- Claim: a name is up to three signs; the first is a house emblem, the last goes with the ending.
- Number: same fish variant first in a name for 15 of 23 house-mate pairs against 36% by chance; name-slot signs repeat inside houses 19 pairs against 7.8; class is a closed set of 26 signs tied to seal size; the name slot holds 384 different signs; a marked fish is a mark plus the plain fish (second sign plain fish in 40 of 528 swaps against 133 of 3,332).
- Means: the first sign works as a family emblem.
- Rerun: `work_scripts/name_slot_build.py`, `name_slot_analysis.py`, `name_slot_analysis2.py`, `sound_fishsplit.py`.

### 3. Endings
- Claim: the text closes with one of a handful of signs, and the closer belongs to the person.
- Number: the jar sign ends 557 of 743 texts; the plain man sign follows the jar 54 times (54 of that sign's 73 texts); spear, porter and comb signs stand in the jar's place (spear after jar 0 of 156 on the second catalogue); the name's last sign predicts the closer, the same name keeps it across seals, house, site, period and object type do not predict it. Median seal face by closer: person 738 mm2, jar 645, spear 633, carrier 495, comb 420. The mix of closers is the same at every site.
- Means: the ending is a property of the person, not of place or object.
- Rerun: `work_scripts/endings_build.py`, `endings_A1.py` to `endings_A6.py`, `endings_B.py`, `closers.py`.

### 4. The "jar then man" ending found in the master's building
- Claim: texts of the form [name X] jar man mark a person attached to another owner X.
- Number: these seals are the biggest (median face 778 mm2 against 652 for name + jar) and carry an animal 91% of the time against 78%; the names X are fish-crest names 18 of 50 against 7 of 602 for owners; at Mohenjo-daro 5 of 24 such seals sit in a building that also holds an owner object with X's crest, against 2.10 by chance (P 0.046), family members at chance (44 of 588 against 49.5); agent seals are bigger (718 against 581 mm2); goods tags are stamped by such persons 20% against 7% for seals.
- Means: the man ending marks someone who lives where the owner's objects are.
- Rerun: `work_scripts/masters_1.py` to `masters_13.py`, `possessive_A.py`, `possessive_A2.py`, `registry_tests.py`.

### 5. Seals from one room share signs
- Claim: the middle of a seal text belongs to the household.
- Number: seals from the same room at Mohenjo-daro within 3 ft of depth share an uncommon middle sign about 7 times as often as chance (5 pairs against 0.73), first and last signs no excess; house-mates ending in the jar share the sign before it in 15 pairs against 9.3. On photographs of house-mate pairs the shared sign is on both stones in 24 pairs and cut by the same hand in 4.
- Means: different carvers wrote the same sign for the same house.
- Rerun: `work_scripts/gloss_report.py`, `pre_jar.py`; photo pairs in `jobs/out/photo_pairs_A.md`, `photo_pairs_B.md`.

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
- Number: things take the number before them 450 to 220, measure and share words take it after 315 to 49. Inside names, tall two with the plain fish 65 of 73, short two with the marked crest fish 62 of 63 (P 1.6e-28), on new texts 14 of 16 and 17 of 17; room-mates share the number before a fish in 5 pairs against 0.74; numbers in names bunch on 2 (136 of 191 distinct name texts).
- Means: the number is part of the name there and an amount elsewhere.
- Rerun: `work_scripts/stars_1_split.py`, `stars_2_forms.py`, `stars_5_rooms.py`.

## Part 3. Pictures and objects

### 13. Picture-side ties on copper tablets
- Claim: the picture on a copper tablet goes with certain signs.
- Number: 11 of 12 tablets showing the elephant carry sign 923 against 14% of pictured copper tablets (P 6e-9); tablets showing the gharial carry sign 255 on 11 of 53 against 3.1 by shuffle (P 0.0002). The elephant ties come from copies of two texts and the 11 gharial tablets are copies of one text, so per distinct text the ties do not hold. On some copies the picture is written as a sign (deer sign 341, hare sign 753).
- Means: picture side and sign side go together through few texts.
- Rerun: `work_scripts/sound_v5_job1.py`, `sound_v6_job1_tests.py`.

### 14. The seal animal
- Claim: the stand in front of the unicorn marks the household; the species does not.
- Number: stand shared by same-room seals 38.1% against 17.2% (139 pairs, P 0.0003), fading with distance (room 1.79, block 1.27, area 1.13), independent of crest (P 0.91); species follows none of crest, first name sign, ending, area (P 0.47 to 0.91); short-horned bull with trough 14 of 26 beast seals abroad against 92 of 1,575 at home (P 7e-11), and all 13 round seals abroad.
- Means: a seal carries separate household and circuit marks.
- Rerun: `work_scripts/animal_base.py`, `animal_2_assoc.py` to `animal_7_abroad.py`.

### 15. What each kind of object holds
- Claim: object classes have their own signs.
- Number: tags (500, 417, 056, 890, 048, 055, 892), bangles (two-leaf 840, 7.9 times chance), pots (440, 480), ivory rods (comb 400 ends 29% of rods against 2.7% of seals); 91 of 122 single-count pots use tall strokes, owner on 9%; signs 503, 615, 845 sit on copper tablets 4.0, 4.7, 8.4 times chance on new texts.
- Means: object kind predicts content.
- Rerun: `work_scripts/goods_1_signs.py` to `goods_6_reads.py`, `sound_v3_c.py`.

## Part 4. Time and distance

### 16. The system is flat across time
- Claim: nothing in the frame moves with time.
- Number: 2,666 of 4,694 objects dated. Early / middle / late: agent seals 4.5 / 4.1 / 4.5%; fish-crest names 12.3 / 12.6 / 12.8%; office opening 1.4 / 0.9 / 0.8%. The axis works: inscription-only seals at Harappa 14 of 99 to 33 of 98 (P 0.0018). 87 of 122 sign jobs hold in every time bin against 39.2 with jobs shuffled (P 0.001).
- Means: one key reads about six centuries.
- Rerun: `work_scripts/time_1_trends.py` to `time_5_first_writing.py`, `sound_v7_time.py`.

### 17. The earliest levels
- Claim: names arrive after counting.
- Number: before the cities, 24 of 35 texts are one sign long and the jar is on 3 of 35 against 896 of 2,122 later (P 1.9e-5); earliest Mohenjo-daro level has a fish crest first in the name on 0 of 38 seals against about 11% later (P 0.0125).
- Means: the system grew in layers.
- Rerun: `work_scripts/early_1_levels.py` to `early_5_carry.py`.

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
- Claim: hand jobs and machine classes predict the next sign better than the same classes dealt to wrong signs, on 482 new texts.
- Number: bits per sign on the 482 new texts: sign frequency only 7.849; hand jobs 7.661; hand jobs dealt to wrong signs (20 decoys) mean 7.824, best 7.739; machine classes 7.576 and 7.532; sign pairs 6.892. Share of what the sign-pair model knows about order that the classes capture: hand jobs 19.6%, machine classes 28.5% to 33.1%, decoys 2.6%. No decoy of 20 reached the real frame on any score.
- Lost-sign restoration: in 77 texts where the second catalogue has the sign that Lipi lost, the right sign is in the top 5 candidates for 45.5% with hand jobs, 27.3% by frequency and 32.5% for the decoy mean; the job of the lost sign is right 54.5% against 28.6%. Sign pairs plus jobs: right sign first for 32.5%, in the top 10 for 70.1%. Candidates for 1,971 lost signs on 1,417 damaged faces are in `work_data/frame/restorations.csv`. A photo check of 30 restorations: 5 fit the top candidate, 3 fit another sign, 22 could not be judged.
- Means: the order carried by jobs holds on texts no rule was built on, and it narrows what a lost sign can have been.
- Rerun: `work_scripts/frame_predict.py`, `frame_common.py`, `frame2_photos.py`; report `jobs/out/frame_machine.md`.

### 22. Frame v2: 14 written classes
- Claim: a frame of 14 explicit classes (the hand frame plus the machine's three changes and two additions: fish signs as name fronts, tree signs as counted things) holds about a third of the order.
- Number: on the 482 new texts, 7.536 bits per sign against 7.849 for frequencies; its 20 decoys average 7.790 and the best reaches 7.671 (0 of 20 reach it). Share of the sign-pair model's knowledge captured: v2 32.7%, v1 19.6%, machine classes 28.5% to 33.1%, v2 decoys 6.1%. Mixed with sign pairs: 6.881 bits, below sign pairs alone (6.892). Pushed on a held-out half of the first catalogue (14 to 54 classes) it reaches 48.3%; nearly every added class is one frequent sign by itself. Lost sign in the top 5: v2 50.6%, pushed 58.4%, v1 44.2%, frequency 27.3%, decoys 36.0% and 46.7%.
- Strict written patterns (one per text type, fixed before scoring) fit seals 43%, tags 50%, tablets 56%, copper tablets 54%, pots 27%; the decoys fit 7% to 23%.
- Means: the order the machine found is written as rules a person can read, and the rules carry to new texts; beyond about 14 classes the rest of the order belongs to particular signs.
- Rerun: `work_scripts/frame2_common.py`, `frame2_build.py`, `frame2_score.py`, `frame2_kind_redesign.py`; report `jobs/out/frame_v2.md`; the corpus written in classes is `FRAMEBOOK.md` (`frame2_corpus.py`, `frame2_book.py`).

## Part 6. Fixed phrases

### 23. 136 fixed phrases, by a rule set in advance
- Claim: the script has a stock of fixed sign pairs and triples that keep their order.
- Number: the rule was fixed before the run: 8 or more distinct texts, in order 90% or more of the time (against the reverse order), at least 5 times more often than sign frequencies give. It finds 136: 99 pairs, 36 triples, one four-sign run (255-435-690-740). Control: the same rule on texts with the sign order shuffled inside every text, 20 shuffles: 0.45 phrases pass on average (maximum 2). Confirmation on new texts: of 99 testable phrases, 79 are confirmed. In frame v2, the top 40 pairs carry 41% of what sign pairs add over v2 and the top 200 carry 92%; in new texts those 40 pairs occur 151 times in order and 6 reversed. 277 rarer phrases (4 to 7 texts) against about 13 in shuffled texts. 45% of objects carry at least one (seals 53%, copper tablets 71%, tablets 50%, pots 8%).
- By place in the text: name 42, front 39, ending 28, count line 27. 118 phrase families, 15 paradigms, 6 numbered series.
- Means: the texts are built from a stock of set phrases, and shuffling the sign order inside texts removes almost all of them (0.45 against 136).
- Rerun: `work_scripts/phrases_common.py`, `phrases_1_list.py`, `phrases_2_atlas.py`, `frame2_phrases.py`; report `jobs/out/phrases.md`.

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
- Number: the counted things are the tree signs 390, 405, 407 and the porter-with-jars 156; the number is mostly 3. With jobs dealt to wrong signs this kind nearly vanishes (1.0 seal on average). The text of a count-line seal also appears on a clay sealing or tag 17 of 75 times (22.7%) against 5.7% for the 609 name seals (P 8.5e-6; none of 2,000 length-matched draws reaches it; it rests on about five distinct sealings). In the stamp job, matched to length against other seals: 24.5% for count-line seals against 4.3%; name seals 1.2%. The cup 700 never appears on them. Jar + man texts are 5.4% of impressions against 2.5% of seals (P 0.010).
- Means: count-line texts turn up on clay impressions far more often than name texts do. `guess`: a count-line seal is a quantity stamp.
- Rerun: `work_scripts/frame2_seals.py`, `stamps_4_counts.py`, `stamps_5_more.py`; reports `jobs/out/frame_v2.md`, `jobs/out/stamps.md`.

### 27. Seals matched to their clay impressions
- Claim: the stone that made an impression is almost never among the excavated seals; the text belongs to many stones, the animal to one.
- Number: 262 tag faces and 74 stamped pots were taken as impressions. For impressions of 3 or more signs every seal with the identical text is in another city (13 of 13); at 2 or more signs 18 of 24 are in another city and none in the same building. Only 6 of 24 have a twin in their own city against 16.2% for a random seal of that length. Twin pairs carry different animals 15 times and the same animal 19 times. Shuffling signs inside texts gives 6.1 matches against 24 real.
- Multi-stamp lumps: 33 objects carry several impressions, typically a name or jar-man stamp plus a short front-word stamp (861-002 plus one sign, or 317-920-002), sometimes with a 055 stamp.
- The backs: tag subtype letters match the backs in 20 photographs: B wooden box, P plain token, L soft package (cloth, reeds, cords), R storage jar. Count lines sit on L 5 of 40 faces against 2 of 296 elsewhere (P 0.0003); jar-man texts on L 7 of 40.
- Lothal warehouse square: 7 different texts on 15 faces against 12.96 by chance, one jar-man stamp 8 times, the matching seals at Mohenjo-daro. Kalibangan KLB-1: 2 texts against 7.35.
- Means: goods were stamped by senders in other cities; a transaction left two or three stamps on one lump. `guess`: a store holds a few senders each stamping many packages.
- Rerun: `work_scripts/stamps_1_build.py` to `stamps_7_clusters.py`; tables in `work_data/stamps/`.

### 28. Tablets as issue chits
- Claim: a name keeps its own amount, and seals and tablets in one area carry the same count of the same thing.
- Number: 816 of 902 multi-face tablets are readable: amount + name 356 (343 at Harappa, 5 at Mohenjo-daro); name + thing 176; amount + thing 94; name + name 88. A name keeps its own amount: 38 against 21.6 (P 0.003); the same name with a different amount in one trench: 9 pairs against 3.5 (P 0.011). The cup ceiling holds on all 902 (1, 2, 3, 4, 6). Seal and tablet pairs in one area with the same number and thing: 89 against 69.5 (P 0.003), mostly Harappa F Trench I (seals 033-700 and 034-700 beside 29 and 17 tablets with the same text).
- Means: the tablets behave as records with a fixed amount per named line. `guess`: Harappa tablets are issue chits, a fixed amount per named recipient.
- Rerun: `work_scripts/spots_3_records.py`, `spots_3b_rescue.py`, `stamps_4_counts.py`.

### 29. Jar + man seals near the same crest, and the quarter pair with a count
- Claim: seals of the form [crest] jar man sit near objects of the same crest, with a limit at Harappa; the pair 061/820 + 142 takes a count in front.
- Number: at Mohenjo-daro 5 of 24 share a building with an owner object of the same crest (2.09 by shuffle, P 0.044); at block level 9 of 24 against 5.28; pooled over cities at block level 11 of 30 against 6.35 (P 0.024). Those buildings hold 9 same-crest objects against 2.94. These seals are bigger (Mohenjo-daro median 778 mm2 against 629). At Harappa the building test is 0 of 6; with all object kinds the mound matches 18 of 31 against 14.84 (P 0.030). They do not copy the master's stand pattern or animal (chance); they carry stand S or J on 15 of 21 against 47% of all unicorn seals (P 0.021).
- 061/820 + 142: a count (1, 2, 3) stands right before the first sign in 5 of 11 pair texts against 9% elsewhere (P 0.003); 10 of 11 end in the jar; the text 061-142-400-740 is identical on four objects in two cities.
- Means: these seals sit in the same places as their crest's other objects at Mohenjo-daro and not at Harappa; the quarter pair behaves as a numbered post.
- Rerun: `work_scripts/spots_1_manager.py`, `spots_1b_rescue.py`, `spots_2_office.py`, `registry_offices.py`.

## Part 8. What was tested and did not hold

Each line gives the number and the script. These are results of the tests as run.

### The sign-by-sign words
- Four decoy results. (a) Blind decoy test: 60 signs, 30 with their accepted word and 30 with a word moved from another sign of the same job; predictions written first by two blind testers. Came true: accepted 9 of 58 (15.5%), decoy 10 of 60 (16.7%). (b) Same test with the full method (look at the data, predict, one redesign): accepted 17 of 29, decoy 19 of 30. (c) Three blind readers graded 60 whole inscriptions turned into English four ways: sense for the real word list 35% to 37%, for words dealt among signs with the same job 27%, freely dealt 10% to 17%, dealt among equally common signs 7% to 8%. (d) Forced choice, 120 inscriptions, pick the real line of four (chance 25.8%): real picked 29.2% pooled, the two same-job shuffles 34.2% and 22.2%, free shuffle 14.4%. So a wrong word of the same job passes as often as the accepted word. Scripts: `work_scripts/decoy_build.py`, `decoy_test_A.py`, `decoy_test_B.py`, `decoy_replay_A.py`, `decoy_replay_B.py`, `decoy_score.py`, `blind_build.py`, `blind_score.py`, `blind2_build.py`, `blind2_score.py`.
- A time test of the assigned jobs: of 122 values with dated uses, 87 do their job in every time bin against 39.2 with jobs shuffled; four fail in every bin (482, 575, 850, 717) (`work_scripts/sound_v7_time.py`).

### The language
- Two machine runs, 19 dictionaries in 7 families, sound-alike rule scored against controls. Run 1 (`work_scripts/lang_m_common.py`, `lang_m_score.py`): 0 of 312 cells beat all three controls at P below 0.05. Dravidian family, strict match, narrow keywords: 42 of 63 picture-and-job units hit; jobs dealt at random 38.4 (P 0.045); the dictionary's sounds dealt at random 43.5 (P 0.72). The one lean (cells beating the outside-noun and scrambled-sound controls but not the job shuffle): Dravidian 10 of 96, Indo-Aryan 2 of 48, Munda 1 of 60, Sumerian 1 of 36, Akkadian, Elamite and Burushaski 0.
- Run 2, with pictures described blind (172 units from 235 signs), the machine's ten classes and dictionaries that keep same-spelled words apart (`lang_m2_common.py`, `lang_m2_score.py`, `lang_m2_swaps.py`, `lang_m2_c4check.py`): combined score per family (mean z against scrambled sounds) and shuffle P: Dravidian -0.20 (0.82), Munda -0.04 (0.53), Indo-Aryan -0.56 (0.97), Sumerian -0.06 (0.55), Akkadian -0.34 (0.66), Elamite +0.31 (0.16), Burushaski -0.38 (0.79); the bar was P below 0.007. The lean fell to 3 of 96 Dravidian cells. A first positive, right class against wrong class for the same picture (Dravidian P 0.0005), vanished once each dictionary's own rate of keyword words per class was allowed for (P 0.66 to 0.98).
- Sign swaps (pairs of differently drawn signs that replace each other): run 1 Dravidian picture names sound alike in 16 / 58 / 63 of 65 (strict / medium / loose) against 17.1 / 56.7 / 64.5 dealt at random; run 2, 40 / 89 / 108 of 108 against 39.4 / 89.4 / 106.9.
- Means: at the strength of the test, every family is at chance, and the language of the script is not identified.

### The outside match in cuneiform
- Of 585 CDLI tablets from Girsu, Lagash and Umma naming Guabba or Meluhha, 33 are sealed, 13 are Meluhha or textile texts, and all 13 seal legends are cuneiform. Foreign texts are not more lot-like than home texts (49% against 45%). The sesame sign 838 is on 0 of 69 foreign objects. No text puts a jar word on a line with Dilmun, Magan or Meluhha (918 texts). No Meluhha-tagged cloth word in 202 CDLI Meluhha texts; loan candidates 196 against 139 by shuffle (P 0.07). Scripts: `work_scripts/abroad3_04_cdli_east.py`, `abroad3_05_seals.py`, `abroad3_07_seal_legends.py`, `abroad2_14_sesame838.py`.

### One office-holder per city area; one phrase per building
- Holders of the sign pair 061/820 + 142 spread one per city area: 35 against 35.0 expected; 14 blocks against 13.6 (`work_scripts/spots_2b_spread.py`).
- A phrase belonging to one building: shared-building pairs 108 against 111.1 with copies removed; the three phrases that first looked house-bound lose it (P 0.34, 0.13, 0.016). This also cuts against "a house is one building" as a general rule (same-house seal pairs sharing a building: 1.41 times chance at Mohenjo-daro, P 0.08) (`work_scripts/phrases_3_kinds.py`, `registry_tests.py`).

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
