# The frame: what is measured about the Indus script without any word

Every finding below was counted from the sign catalogues with no word attached to any sign, and reruns from the script named under it. Each has four parts: the claim, the number, what the number means, the script. Dates are 2026-11-17. For the one place where words appear, see the Labels appendix at the end.

## Terms

- **Seal**: a small stone or clay stamp with a few signs. **Tablet**: a small flat plaque of clay, stone or copper. **Tags, pots, rods**: other inscribed objects. **Face**: one inscribed side; this book counts faces.
- **Sign**: one drawn character, cited by catalogue number (740 is a jar picture, 220 a fish picture).
- **Lipi catalogue**: the main catalogue (5,679 faces, 2,162 distinct complete texts). Texts are stored in reverse of reading order; everything here is in reading order.
- **Second catalogue**: Mahadevan 1977, a separate transcription linked to Lipi by a 366-pair crosswalk. **New texts**: its 1,183 texts with no partner in Lipi, never used to shape any rule.
- **Crest**: the first sign of a name. **House-mates**: two seals found in the same excavated house. **Job**: the role a sign plays in the text shape.
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

## Part 5. What went against, with no word involved
- Ration size following rank; total lines (one number equal to the sum of the others 10 of 70 against 14.9); batch totals in whole large units (0 of 16) (`work_scripts/measures_3_sums.py`, `measures_5_rank.py`).
- Administration thickening with time; a trade peak for the overseas bull (`work_scripts/time_3_redesign.py`).
- Numbers in names bunching on 3, 6, 7 (`work_scripts/stars_2_forms.py`).
- "Servant of a house-mate" and "head of his own house" for the man ending: 4 of 20 against 3.3 (`work_scripts/endings_A1.py` to `A6.py`).
- Animal as clan, ward or rank (`work_scripts/animal_2_assoc.py`).
- Cuneiform match: 13 sealed Meluhha or textile tablets all have cuneiform legends (`work_scripts/abroad3_07_seal_legends.py`).

## Appendix: labels (the only place words appear)

Every English or Dravidian word placed on a sign in `work_data/values_master4.csv`, `CORPUS.md`, `READINGS.md` and `WHOSWHO.md` is a working label for the sign's job. Two decoy tests (`jobs/out/decoy_test.md`) found a wrong word of the same job passes the confirming procedure as often as the accepted word (9 of 58 against 10 of 60 blind; 17 of 29 against 19 of 30 with the full method), so the exact words are not established. Labels used in this book's numbers:

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
