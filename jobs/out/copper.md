# Copper: the copper tablets of Mohenjo-daro as a record system

Word-free job, 2026-11-17. Sign numbers, pictures, jobs, counts and findspots only. Scripts in `work_scripts/` (each one's predictions are in its top docstring, written before its numbers): `copper_common.py` (loader), `copper_0_sheets.py`, `copper_0b_sheets.py`, `copper_0c_sheets.py` (photo contact sheets), `copper_1_table.py` (objects and sets), `copper_2_pairs.py` and `copper_2b_shared.py` (one text, one picture), `copper_3_kinds.py` (text kinds, counted things), `copper_4_picsign.py` (picture written as a sign), `copper_5_swaps.py` (sign swaps), `copper_6_spots.py` (findspots), `copper_7_harappa_time.py` (against Harappa; time), `copper_8_settable.py` (set table), `copper_9_vocab.py` (copper's own phrases). Tables and logs in `work_data/copper/` (4.5 MB). Each script runs in under 90 seconds.

## Plain words

- **Copper tablet**: a small flat copper plaque (about 33 x 25 mm). Usually a text on one face and a drawing on the other.
- **Text face / picture face**: the inscribed side and the other side. A **picture-face sign** is a single sign cut on the side where other copies have the drawing.
- **First catalogue** (Lipi): 189 copper tablets at Mohenjo-daro, one row per face, with findspot, register number and a picture code. **Second catalogue** (Mahadevan 1977, "M77"): 135 copper tablets, its own transcription of the signs (mapped to first-catalogue numbers), an area code ("locus") and its own three-digit picture code (fs80: two-digit family plus a sub-type digit).
- **Set**: copies with the same text face. **Text family**: texts that differ in one sign, or by one sign added at the end (706-033-923-740 and 706-033-923-740-001). A damaged copy (lost sign 000) joins a family only if it fits complete texts of exactly one family.
- **Counting one object once**: the two catalogues re-transcribe mostly the same tablets and no object number ties them. So a text's copies are max(first-catalogue copies, second-catalogue copies), never the sum. The first catalogue is the object list; the second only adds copies where it has more of a text. Inside the first catalogue, the 11 rows with no CISI number have register numbers not shared with any other row, so they are separate objects.
- **Eye reading**: what the lead saw on the photographs in `evidence/.../seal_images/` (103 tablets, `work_data/copper/photo_check.csv`). "Quadruped" = an animal whose kind cannot be told; it counts as no label.
- **Jobs** (frame v2, `work_data/frame/classes_v2.csv`): closer (jar 740, spear 520, porters), number, counted thing (THING: trees 390/405/407, cup 700, porter 156), measure (705/706 big measure, and others), name signs (crest, name part, place word). 706 is filed as a name part in frame v2; here it is read with 705 as the big measure, as the frame book does.
- **Text kind**: *name+closer* (name signs shut by a closer, no count), *record* (name, closer and a count line, either order), *name+count* (name signs and a count line, no closer), *name* (name signs only), *one sign*. **Count line**: a number next to a counted thing or measure.
- **Register lot**: the excavator's running find number (DK 10141, VS 1988, HR 4337). Finds were numbered as they came out of the ground, so close numbers in one series mean close in time and place; one number is one find lot.
- **Shuffle / random deal**: the label under test is dealt at random many thousand times among the same objects; **P** = share of deals at least as extreme as the real count. Small P = the real pattern is not chance, in the direction stated.

## What was found

**1. One text carries one picture: 21 of 21 same-text pairs read by eye show the same picture, against 0.059 when pictures are dealt at random (P below 0.0001).** All 12 texts with two or more legible copies show one picture each (random 0.54). With the first catalogue's specific codes added: 175 of 191 pairs (0.916, random 0.075); in the second catalogue's independent codes: 182 of 291 (0.625, random 0.061), lower because it splits sub-types (stag set 147 on 12 and 145 on 7). *Means*: the picture is a fixed part of the record, not a choice per copy. *Opens*: the reverse is loose, and that is where the structure is (finding 2).

**2. One picture covers several texts: 8 of 13 pictures seen by eye sit with two or more text families** (5 pictures sit with one family against 0.11 when pictures are dealt at random; one of the 8, the buffalo, covers two near-variants of one text). Goat with marked body and trough: 003-421-176-100-740-790 and 231-017-585-095-520-032-407. Spotted long-necked composite: 905-032-597-142-617, 017-585-388-740, 806-235-233-705-033-585-407. Rhinoceros: 235-233-222-740, 235-220-222-740, 861-368-001-142-233-222-740 (and 503-615-740 by both catalogues' codes). Striped horned beast: 806-233-384-740, 806-233-176-740, 003-233-100-740. Different texts under one picture share a sign 4 times in 11 pairs against 0.18 by deal (P 0.028): 233 under the striped horned beast, 222 and 233 under the rhinoceros. *Means*: the picture names a class of record and the text names the line inside it; inside the rhinoceros class the ending 222-740 holds, inside the striped-beast class the fish 233. *Opens*: the picture is a heading over a group of named lines, the same shape as the Harappa heading faces over many names.

**3. Copper count lines count the big measure and the tree, not the cup.** Of copper faces with a count (every copy), the cup 700 is on 2 of 58 against 430 of 530 Harappa clay-tablet faces (P 1e-33); the big measure 705 on 20 of 58 against 10 of 530 (P 4e-15); 706 on 14 of 58 against 1 of 530 (P 2e-14); tree 407 on 12 of 58 against 2 of 530 (P 2e-11); tree 390 and porter 156, common on Harappa chits and Mohenjo-daro seals, are on 0 copper faces. Per distinct text the same: cup 1 of 17 against 32 of 72 (P 0.004), 407 5 of 17 against 2 of 72 (P 0.002). *Means*: copper tablets record a different unit from the chits: whole big measures (three of them: 705/706-033) and counted 407 lots, where the chits record cups. *Opens*: the copper count lines match the Mohenjo-daro count-line seals (705 on 49 seal faces, 706 on 20, 407 on 11), the quantity stamps of the frame book; a copper tablet and a count-line seal may be two ends of one issue.

**4. The picture can be replaced by a sign, and those signs are a class of their own: 26 of their 29 uses are on copper picture faces, against 0.016 of uses on copper at all for signs of the same rarity (max 0.138 in 10,000 draws).** Eight text families show it in the first catalogue, and the second catalogue repeats five of them with its own sign numbers on the same face (table below). The replacing signs are not drawings of the animal: 7 of the 9 are vessel or plant shapes (777, 780, 781, 782 a cup or U holding a flowering plant; 753 a U with tree handles; 749 a handled jar under a hatched caret; 841 two leaves with a tree), one is the deer 341, one (957) a jar-like shape with rungs. One sign serves several pictures: 777 stands for the horned archer on one copy and for the marked goat on four; 749 stands on the picture face of the 806-233 family and of 231-255. *Means*: the picture face holds either the record's animal or a mark from a small closed set of vessel-and-plant signs. *Opens*: the alternative to the animal is a sign of a filled vessel, so the second face is the "what kind" field of the record, written as an animal or as a vessel.

**5. Copies swap signs, and the swapped signs keep each other's company elsewhere: 7 of 9 differently-drawn swap pairs share frames (left and right neighbours) across the whole corpus above their own random pairs (P at or below 0.05), mean overlap 0.337 against 0.068.** Fourteen swap pairs (table below). Five are one sign drawn two ways by the shape list or the second catalogue (061/063, 407/408, 421/422, 422/423, 705/706). Four more are one base sign with an added mark (904/905 a tooth; 220/231/233 the plain fish, fish with a stroke, fish with a bar: all in the crest slot). Two are truly different shapes: 176/384 (seated person against upside-down heart), which also holds in the second catalogue with 5 and 6 copies, and 806/831. *Means*: the scribes treat the marked fish as the plain fish in the crest slot, and 176 and 384 as one slot filler under one picture. *Opens*: 176/384 is a pair of signs proved interchangeable by the scribes and by their neighbours (overlap 0.571 against 0.084, P 0.004).

**6. Copies were handed out across the city, with small batches kept together.** Copies of one set share one register lot 6 times against 0.83 by deal (7.2 times, P 0.0005) and lie within 100 numbers 15 times against 7.60 (P 0.013); the stag set has DK 10141, 10146, 10175, 10213, two copies in DK 3447, two in DK 5444 and HR 4337a/b; the archer set has three copies in DK 4807. But same area 196 pairs against 175.5 (P 0.20), same part of the city 303 against 317 (P 0.66), second-catalogue locus 65 against 63.4 (P 0.42): at chance. The stag set lies in 5 parts of the city (DK, HR, VS, SD, L), the archer, hare, elephant and goat sets in 3 each. Buildings with two or more copper tablets hold different sets: DK area E Trench 3 sets on 4 tablets, VS area house 1I 3 on 3, DKG First Street 3 on 3, lot DK 3447 two stag copies and one archer copy. *Means*: a set was made as a batch, some copies stayed together, most went out to many households. *Opens*: copper tablets behave as things carried by holders, not as files kept in one office.

**7. Copper tablets are the most copied texts in the script: 2.48 copies per text, against 1.45 on Harappa clay tablets and 1.52 on Mohenjo-daro clay tablets.** Count on 30.7% of copper objects against 45.4% of Harappa clay tablets; a jar name on 61.4% against 48.6%; 29 distinct jar names against 190. Copper names are not seal names: 4 of 29 copper jar names stand before a jar on a Mohenjo-daro seal (13.8%) against 20.7% for random seal names recurring on another seal; whole copper text faces are found inside a Mohenjo-daro seal face 4 of 55 times against 7 of 45 for Mohenjo-daro clay tablets; 5 of 29 copper names are on a seal of any city. The four matches (255-435-690, 503-615, 705-033-923, 773) are on unicorn or gaur seals with plain jar endings (7 of 9), not on the seals of the copper picture's animal. *Means*: the name on a copper tablet is not a seal holder's name the way the clay tablets' names are; it is the name of the line or account. *Opens*: copper texts are their own vocabulary: 134 of 162 copper tablets carry a sign pair found on no other kind of object, against 45 of 79 Mohenjo-daro clay tablets.

**8. Copper tablets run through all of Mohenjo-daro's time.** Dated: 50 of 189. Early 7 against 11.0 expected from the other objects of the same areas (P 0.09 for fewer), middle 23 against 20.9, late 20 against 18.1. The stag set itself has copies in all three bins (early 1, middle 4, late 4); the archer set middle 1, late 4; the elephant family early, middle and late. *Means*: the same texts with the same pictures were made over centuries. *Opens*: a set is a standing line, reissued, not one event.

**9. What a copper tablet is.** Reading built on: **a token of a standing entitlement or allotment, issued in batches to many holders.** The numbers that decide:

| reading | predicts | measured | standing |
|---|---|---|---|
| token of entitlement (a standing allotment line, many identical tokens handed to holders) | many identical copies; copies spread over the city; fixed amount per set; same text over a long time; names that are lines, not persons | 2.48 copies per text (up to 30); same area at chance, same lot 7.2 times chance; the amount never varies inside a set except a trailing one-stroke 001; stag set early to late; copper names on seals 13.8% against 20.7% | building on it |
| receipt (one per delivery) | texts mostly unique; amounts varying within a name | 30 identical copies of one text; no amount change inside any set | against |
| amulet (protective charm) | no counts, picture central, copies anywhere | count lines on 30.7%, measures 705/706 and tree 407; the picture can be swapped for a vessel sign, which an amulet would not need | against on counts |
| tax or tribute tally | counts of produce in measures; copies kept by the collecting office | measures 705/706 and 407 yes; but copies spread over the city and do not stay in one office | half: the counted things fit, the findspots do not |

What each reading predicts that has not been checked:
- Token: tokens are carried and handed back, so copies should be worn on the edges and found in houses and streets, not in one store; worn-edge state can be read from the photos (not done). The 30 stag copies should match the count of holders of one office in the city: compare with count-line seal impressions of 705-033 at Mohenjo-daro.
- Tally: if copper tablets are the payer's copy, the matching office record should be a count-line seal impression with the same measure (705/706-033 or 407) on a clay sealing in the same area. Test with `work_data/stamps/`.
- Amulet: should show holes or loops for wearing; the catalogue's shape field and the photos can be read for perforations (not done).
- All readings: a picture class (rhinoceros, goat, spotted composite, striped beast) should keep its sign in the other copies found later; the second catalogue's 38 extra copies and the third CISI volume objects with no photos (M-2045 to M-2050) are the fresh set.

## The table of sets

One row per text family with two or more copies (37 families; union copies shown; `work_data/copper/set_table.md`, `sets.csv`). "Eye" = photo reading (quadruped = kind not visible; sign = a sign on the picture face). Codes: first catalogue (Othr, blank and - are vague) and second catalogue (fs80; family 14 is the stag and tiger sets, 13 the goat and 806-233 sets, 16 hare, 07 elephant, 11 rhinoceros, 29 spotted composite, 52 human figure, 86 knot, 04 gaur, 06 buffalo, 01 unicorn). Register lots, buildings and bins from the first catalogue. Bins: early / middle / late.

| texts (copies first / second catalogue) | copies | kind | eye | first-cat. code | second-cat. code | picture-face sign | areas | register lots | bins |
|---|---|---|---|---|---|---|---|---|---|
| 503-615-752-740 (30/20) | 30 | name+closer | stag 4, quadruped 3 | Gaur 2 (no photo) | 147 x12, 145 x7 | - | DK 14, HRB 4, DKG 2, HRA 2, VS 2, L 1, SD 1 | DK 10141, 10146, 10175, 10213, 1023, 12001, 1365, 1798, 3409, 3447, 3447(1), 3730, 5444 x2; HR 2081, 4337a, 4337b, 5549, 6058, 723; L 456; SD 1517, 3009; VS 1988, 3320 | early 1, middle 4, late 4 |
| 806-845-061-407-850-900-740 (15/10) + damaged 1 | 16 | name+closer | horned archer 1, figure 1, sign 2 | Anth 11 | 520 x6 | 777, 780, 781, 782 one each; second cat. 362 x2, 363 x1 | DK 5, DKG 2, SD 2, DKE 2, VSA 1 | DK 10076, 1488, 3447(2), 3850, 4807 x3; DK-E 2215, 825; SD 2554, 3032; VS 1406 | middle 1, late 4 |
| 235-705-033-845-407-321-407 (14/10) | 14 | name+count | hare 3 | Hare 12 | 163 x9 | 753 x2 | DK 8, DKC 1, SD 1, VSA 1 | DK 10045, 12223, 12514, 151, 3334, 5440, 7871; DK-C 1606; DK-i 854; SD 1758; VS 2109 | early 2 |
| 706-033-923-740 (8/5); 706-033-923-740-001 (4/5); 705-033-923-740-001 (1/0) | 14 | record | elephant 4 | Elep 11 | 75 x7, 101 x1 | second text 003-422 on 1 | DK 7, VSA 3, L 1, DKE 1 | DK 11127, 12829, 5576, 5693, 9169; DK-E 2181; DK-i 167, 838; L 461; VS 1900, 2028, 888 | early 1, middle 1, late 2 |
| 806-233-384-740 (6/6); 806-233-176-740 (2/5); 806-231-176-740 (1/0); 831-233-176-740 (1/0) | 13 | name+closer | striped horned beast 2, quadruped 1 | - | 135 x7 | 749 x2; second cat. 346 x2 | DK 6, SD 1, DKG 1 | DK 10425, 10695, 3817, 4318; HR 2743; SD 1517 | late 1 |
| 231-017-585-095-520-032-407 (8/3); 220-...-407 (1/4); 220-...-408 (1/0) | 13 | record | goat 2, sign 2 | Goat 1, Buff 1 (no photo) | 139 x5 | 777 x4, 781, 782; second cat. 363 x2 | DKG 2, DK 2, HR 2, SD 1 | DK 1726, 3697, 4672, 501; HR 2676, 4337; SD 2051 | late 2 |
| 798-240-845-061-407 (7/6); ...-063-407 (1/0) | 8 | name | tiger 3, quadruped 1 | Tigr 2, Gaur 2 | 141 x3, 101 x2, 91 x1 | - | DK 3, HR 2, DKG 1 | DK 3811, 4225, 7874; DK-i 688; HR 1401, 5816 | late 1 |
| 905-032-597-142-617 (6/0); 904-... (1/0) | 7 | name+count | spotted composite 2 | Comp 2 | - | - | DK 3, DKG 1, VSA 1 | DK 10596, 3577, 4157; DK-i 417; VS 3504 | early 1, middle 1 |
| 747-717-095-595-001-142-617 (1/6) | 6 | name | - | Bull1 1 | 15 x3, 290, 950 | - | DK 1 | DK-i 803 | - |
| 003-421-176-100-740-790 (4/4) | 4 | name+closer | goat 2 | Goat 3 | 139 x3, 137 | - | DK 2, DKB 1, DKG 1 | DK 1838, 5996; DK-B 103; DK-C 153 | early 1, middle 1 |
| 235-233-222-740 (3/2); 235-220-222-740 (1/0) | 4 | name+closer | rhinoceros 2 | Rhin 2 | 111 x2 | - | DK 2, DKG 1 | DK 3694, 4532 | middle 1 |
| 091-032-001-595-001-142-617 (0/4) | 4 | name | - | - | 290 x4 | - | - | - | - |
| 017-585-388-740 (4/4) | 4 | name+closer | spotted composite 2, quadruped 2 | Comp 1 | 290 x4 | - | DK 2, DKG 1, VSA 1 | DK 10142, 4089, 4209; VS 983 | middle 1, late 1 |
| 415-220-845-407 (3/4) | 4 | name | knot 2 | Loop 3 | 860 x3 | - | DK 2, VSA 1 | DK 11287, 11499; VS 3526 | early 1 |
| 032-071-407 (2/0); second cat. 032-070-405 (0/2) | 4 | name+count | gaur 1 | Gaur 2 | 45 x2 | - | HR 1, VSA 1 | HR 4573; VS 1104 | late 1 |
| 806-235-233-705-033-585-407 (3/2) | 3 | name+count | spotted composite 1 | Comp 2 | 113 | - | VSA 2 | VS 2432, 3590 | middle 1, late 1 |
| 503-615-740 (3/3) | 3 | name+closer | sign 2 | Rhin 1 (no photo) | 113 | 341 x2; second cat. 184 x2 | VSB 1, VSA 1, DK 1 | DK 9015; VS 2590, 3500 | middle 1 |
| 233-585-407 (3/0) | 3 | name | text both faces 3 | - | - | second text 005-706 | DKE 1, DKC 1, DK 1 | DK 9152; DK-E 814 | middle 2 |
| 255-435-690-740-900-003-422 (3/1); ...-001-003-423, -424 (1+1) | 5 | name+closer | buffalo 2 | Buff 2, Gaur 1 | 65 | - | DK 1, L 1, HR 1 | DK 10311; L 982 | - |
| 705-033-032 (0/3) | 3 | name+count | - | - | - | - | - | - | - |
| 000-000-740 (3/0) | 3 | damaged | - | - | - | 749 x1 | VS 1, DK 1 | DK 3352; VS-N 83 | - |
| 798-231-705-033-904-100-740 (2/1) | 2 | record | sign 2 | - | - | 957 x2 | DKG 1, DK 1 | DK 5421; DK-i 412 | middle 1 |
| 003-700-900-165 (2/2) | 2 | name+count | text both faces 2 | - | - | second text 032-220-176-740 | DKG house 6II x2 | DK 3962, 4143 | middle 2 |
| 326-002-176-740-240-405 (2/0) | 2 | name+closer | text both faces | - | - | second text 900-165 | DK 2 | DK 4067, 4069 | - |
| 231-255-435-690-740 (2/1) | 2 | name+closer | text both faces | - | - | second text 479-749 | HR 1 | HR 4601a | - |
| 744-760-095-595-001-142-617 (2/0) | 2 | name | unicorn 2 | Bull1 2 | - | - | DK 1, DKG 1 | DK 4235; HR 2984 | middle 1 |
| other pairs: 003-233-100-740, 861-368-001-142-617, 752-740 / 773-740, 003-422-176-100-740, 231 / 231-255, 354, 806, 615-343-595, 904-032-904 | 2 each | | | | | 749 on 231-255; 035 (five tall strokes) on 773-740 | | | |

Plus 34 single-copy texts (listed in `set_table.md`). Totals: 189 first-catalogue tablets, 227 copies after the second catalogue (it adds 38 where it has more copies of a text), 90 distinct texts, 32 with two or more copies.

**Photo check.** 103 tablets read by eye in three batches: 48 chosen by a fixed rule (up to 2 per text among vague codes, then 1 per text among specific codes), 32 for texts the first batch missed, 23 aimed at sets with conflicting codes. Vague catalogue code on 73: a clear picture on 24, a sign on the picture face on 10, text on both faces on 10, too worn on 29. Specific code with a legible picture on 28: the code names another thing on 5 (M-525 Gaur is a buffalo-like beast with swept-back horns; M-567 Gaur is a tiger; M-550 Comp a striped horned beast; M-571 Comp a beast with a marked body and curled tail; M-1477 Bull shows human figures). Second-catalogue sub-type digits split one picture (147 and 145 on the stag set; 139 and 137 on the goat set), and family 14 covers both the stag and the tiger sets.

## The picture-to-sign ties

Copies of one text family where some show the picture and some carry one sign on that face (`picsign_ties.csv`). First catalogue numbers; second-catalogue numbers in brackets. "Pictures" = copies whose picture was read (eye or code).

| text family | sign on picture face (copies) | its shape | the picture it stands for (copies) | second catalogue repeats it |
|---|---|---|---|---|
| 235-705-033-845-407-321-407 | 753 (2) | U with tree-like handles, wheel inside | hare among plants (12 by code, 3 by eye; second cat. 163 on 9) | no |
| 806-845-061-407-850-900-740 | 777, 780, 781, 782 (1 each) | cup or U holding a flowering plant | horned figure with a bow (11 by code; second cat. 520 on 6) | yes: 362 (2), 363 (1), cup with plants |
| 231/220-017-585-095-520-032-407/408 | 777 (4), 781 (1), 782 (1) | cup or U holding a flowering plant | goat with marked body and trough (2 by eye; second cat. 139 on 5) | yes: 363 (2) |
| 806-233-384/176-740 family | 749 (2) | handled jar with three strokes, under a hatched caret | striped horned beast (2 by eye; second cat. 135 on 7) | yes: 346 (2), same jar shape |
| 503-615-740 | 341 (2) | deer (antlered animal) | rhinoceros on the third copy by both catalogues' codes (no photo); the near text 503-615-752-740 is the stag set (30) | yes: 184 (2) |
| 798-231-705-033-904-100-740 | 957 (2) | jar-like shape with rungs | none with a picture | second cat. reads it 255 (1) |
| 003-220-590-405-740 | 841 (1) | two leaves with a tree | none with a picture | yes: 405 (1), same shape |
| 231-255 and 231 | 749 (1) | as above | none with a picture | no |

On the rest of the corpus: the first catalogue has 777 and 780 on one unicorn seal each and every other picture-face sign only on copper; the second catalogue has 184 (the deer) on 3 seals (picture families 00 twice, 04 gaur once) and 364 on 2 unicorn seals. So the test "does the sign turn up on seals of that animal" has 0 to 1 hits per sign and cannot run. The redesign is finding 4: these signs are their own kind, 26 of 29 uses on copper picture faces against 0.016 for same-rarity signs.

## The swap pairs

Copies of one text that differ in one sign (`swaps.csv`). Frames = (left neighbour, right neighbour) pairs over all distinct first-catalogue texts; overlap = frames in common / smaller frame set; random = each sign replaced by a sign of about the same use count, 5,000 draws.

| swap | where (copies) | drawn | frame overlap | random | P |
|---|---|---|---|---|---|
| 705 / 706 | elephant: 706-033-923-740 (7), 706-...-001 (4) against 705-...-001 (1) | alike (one shape, one second-cat. sign 336) | 0.413 | 0.075 | 0.004 |
| 407 / 408 | goat: 220-...-407 (1) against 220-...-408 (1) | alike (one shape) | 0.250 | 0.079 | 0.11 |
| 061 / 063 | tiger: 798-240-845-061-407 (6) against -063- (1) | alike (one shape) | 0.250 | 0.073 | 0.10 |
| 421 / 422 | goat: 003-421-176-100-740-790 (3) against 003-422-176-100-740 (2) | alike (one shape, second cat. 190) | 0.500 | 0.035 | 0.04 |
| 422 / 423 / 424 | buffalo: -003-422 (3), -001-003-423 (1), -001-003-424 (1) | 422/423 alike; 424 no shape entry | 0.500 | 0.03 to 0.04 | 0.01 to 0.05 |
| 904 / 905 | composite: 905-032-597-142-617 (5) against 904-... (1) | one base sign, 905 adds a tooth | 0.333 | 0.081 | 0.09 |
| 220 / 231 | goat: 231-017-... (8) against 220-017-... (1); second cat. 220-... (4) against 231-... (3) | plain fish against fish with a stroke | 0.305 | 0.088 | 0.016 |
| 220 / 233 | rhinoceros: 235-233-222-740 (3) against 235-220-222-740 (1) | plain fish against fish with a bar | 0.221 | 0.075 | 0.013 |
| 231 / 233 | striped beast: 806-233-176-740 (2) against 806-231-176-740 (1) | fish with a stroke against fish with a bar | 0.288 | 0.069 | 0.012 |
| 176 / 384 | striped beast: 806-233-384-740 (3; second cat. 6) against 806-233-176-740 (2; second cat. 5) | different: seated person against upside-down heart | 0.571 | 0.084 | 0.004 |
| 806 / 831 | striped beast: 806-233-176-740 (2) against 831-233-176-740 (1) | different | 0.067 | 0.098 | 0.60 |
| 752 / 773 | 752-740 (1) against 773-740 (1) | different | 0.250 | 0.038 | 0.034 |

The unicorn texts 744-760-095-... and 747-717-095-... differ in two signs at once (744/747 jar with two or three strokes, 760/717), so they are not counted as a swap.

## What went against

- **P1.1, eye check names half the vague pictures**: 24 of 73 named; 29 too worn. Kept as a count; the worn ones are the second catalogue's job (its codes cover 96 tablets).
- **P1.3, the second catalogue adds fewer than 15 copies**: it adds 38. It has more copies than the first catalogue of 806-233-176-740 (5 against 2), 747-717-095-595-001-142-617 (6 against 1), 220-017-585-... (4 against 1) and three texts the first catalogue lacks (091-032-001-595-001-142-617 x4, 705-033-032 x3, 032-070-405 x2). Under the max rule these are added once.
- **P2.1, over 95% same picture in both sources**: holds by eye (21 of 21), 0.916 with first-catalogue codes, 0.625 with second-catalogue codes (sub-type digits split one picture).
- **P2b, different texts under one picture share signs, both sources**: first catalogue 4 of 11 pairs against 0.18 (P 0.028); second catalogue 2 of 17 against 0.225 (P 0.85). Redesign done (variant copies removed). New idea run instead: the shared sign is the swap pair itself (finding 5: 220/231/233 and 176/384 are the varying signs under one picture).
- **P3.1, name+closer is over half of copies**: 46.7% of copies, 40.6% of texts.
- **P4.3, picture-face signs on seals of their animal**: 0 to 1 seal per sign, no test possible. Redesign: the sign-class test (26 of 29 on copper picture faces). New idea: shapes (7 of 9 are vessel or plant shapes).
- **P5.2, half or more swaps drawn alike**: 5 of 14 by the shape list and the second catalogue; 9 of 14 counting one base sign with an added mark.
- **P6.1, copies together at least three times chance**: holds only at the tightest level. Same lot 7.2 times (6 against 0.83), within 100 register numbers 1.97 times (15 against 7.60), within 500 0.98 times (P 0.54), same building 2.75 times (3 against 1.09, P 0.067), same area 1.12 (P 0.20). Only the tightest level is a batch.
- **P7.2, copper names on seals as often as chit names**: 4 of 29 (13.8%) against 20.7% for random seal names recurring. Redesign: whole copper text faces inside seal faces, 4 of 55 against 7 of 45 for clay tablets. New idea: seals of any city, 5 of 29. Against three ways; paused with the reason: copper names are line names, not seal holders' names.
- **P9.1, copper phrases used nowhere else (distinct pairs)**: 81 of 138 copper pairs are found on other kinds (0.587) against 77 of 142 for Mohenjo-daro clay tablets (0.542). Redesign by object: 134 of 162 copper tablets carry a copper-only pair against 45 of 79 clay tablets, so the copies carry the copper-only phrases.
- **Codes with no photo that break one text, one picture**: the stag set's M-2045 and M-2046 (Gaur), the goat set's HR 4337 (Buff), 503-615-740's VS 3500 (Rhin, and second cat. 113), the tiger set's M-2048 (Gaur). None has a photograph here; the two photo-read Gaur codes (M-525, M-567) were wrong, so these stay open.
- **M-1477** (buffalo text 000-690-740-900-000, code Bull): the photo shows human figures with outstretched arms and a U-shaped mark, not a buffalo. Listed as an exception.
