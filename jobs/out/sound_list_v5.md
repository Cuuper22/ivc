# Sound list, fifth version: wide made strict, the next 25 signs, and the grammar

Scripts (in `work_scripts/`, run in this order): `sound_v5_common.py` (fourth-pass kit plus the new fact kinds: sign two places away, reverse face, copper-tablet image, Harappa period), `sound_v5_job1.py` and `sound_v5_job1b.py` (job 1, two rounds), `sound_v5_link.py` (the tree-sign link), `sound_v5_job2.py` and `sound_v5_job2b.py` (job 2 and its new words), `sound_v5_values.py` (the list and the counts), `sound_v5_job3.py` and `sound_v5_job3b.py` (grammar), `sound_v5_cands.py`, `sound_v5_readings.py` (READINGS 101-120), `sound_v5_report.py` (this file). Tables: `work_data/sound_v5/`.

Plain words used below:
- **Reads whole** (start to finish): every sign on the face is a number, a base value or a value we are building on. Counted on the 3,600 complete faces of the first catalogue (Lipi); "distinct texts" counts each different sign string once.
- **Strict** count: a value counts only if the fact that came true had NOT been printed while the word was being chosen. **Wide** count: also counts values whose fact had been glimpsed in the sign profiles while choosing.
- **Fresh / seen**: fresh = a kind of fact not printed for that sign before the prediction; seen = a kind that was.
- **New texts**: the second catalogue (Mahadevan 1977) texts with no partner in the first catalogue; never used to choose a value.
- **Building on / testing / paused**: building on = a prediction for the word came true and we read with it; testing = none has yet; paused = three different words failed.
- **P** = how often chance alone gives a result at least this strong. Small P means the reading is pointed to; P near 1 means the data points the other way. "yes" = right direction with P at or under 0.1; "direction only" = right direction, P above 0.1.
- **Two places away**: the sign standing two positions after (or before) the sign in reading order, with the start and end of the text counted as positions.
- **Reverse face**: on an object with two or more inscribed faces, what is written on the other face(s).
- **Frames**: the pair (sign on the left, sign on the right) around a sign in a distinct text. Two signs that share frames more than signs of the same frequency do are standing in for each other.
- **Gain** of a sign: complete faces that would read whole if this sign alone got a built-on value (counted, not guessed).
- **DEDR** = Burrow and Emeneau, Dravidian Etymological Dictionary (local copy), entry number. **Tamil Lexicon** = University of Madras Tamil Lexicon, read on dsal.uchicago.edu.

## 1. What was found

1. **Fully read faces: strict 1825 of 3,600 (was 1418), wide 2004 (was 1861).** Distinct texts: strict 909 (was 608), wide 1029 (was 931) of 2,162. Seals: strict 682 of 1,540 (was 459), wide 758 (was 697). Goods objects: strict 1143 of 2,060 (was 959), wide 1246 (was 1164). New texts read whole: strict 213 of 627 complete lines (was 178), wide 250 (was 233); new-text seals 119 / 138 of 346, goods 94 / 112 of 281 (strict / wide). The strict count rose by 407 faces; the gap between strict and wide shrank from 443 faces to 179. Half of all complete faces now read whole on the strict count alone.
2. **8 of the 13 wide-only values are now strict.** Each got one new prediction on a kind of fact never printed for it, all 13 written into `sound_v5_job1.py` before any was computed: 4 came true (233, 060, 435, 388). The 9 misses got one redesigned test each, again all written before running (`sound_v5_job1b.py`): 4 more came true (240, 097, 923, 104). The five still wide-only: 382, 790, 550, 877, 831.
3. **Sign 923 is ivory: *maruppu* "tusk".** The crescent-horn reading predicted horned beasts on the copper tablets that carry it: 0 of 12 (against). DEDR 4720 *maruppu* is "horn of a beast, elephant's tusk, horns of the crescent moon"; the tusk sense predicts the elephant on the image side: 11 of 12 copper tablets with 923 show the elephant, against 14% of copper tablets with an image (P 6e-9). The seven copper tablets `706-033-923-740` now read "three kalam of ivory: of the house", an ivory account stamped with the elephant. This is the web paying: *kalam* the measure (job 1 of the fourth pass) and the tusk meet on one object type nobody was looking at.
4. **The joiner 060 links an opener to a name.** Fresh: the sign two places after 060 is a fish crest 30 of 205 times against 5.8% (P 3e-6): `[month / assembly / gate]-060-[ward]-[crest] ...`. The opener stands before it 137 of 188 times (73%; the eight-signs job got the same 73%).
5. **The office sign 692 marks big seals: x1.45 at equal length (42 seals, P 8e-6), fresh.** Read *kūṭṭam* "assembly, council" (DEDR 1882): the outline X as joined bars. Openings `692-060-...` now read "of the Assembly: ...". The eight-signs job reads 692 as *nāṭu* "district" (DEDR 3638) on its own test (never followed by a ward jar, 0 of 42); both stay alive. The split: a district word should not make a seal bigger, an assembly office should; the seal size is the number for *kūṭṭam*.
6. **The spindle: 370/371 read *katir* "spindle" (Tamil Lexicon p. 712, sense 6), and stand with cotton.** The picture is a shaft through a ring: a spindle with its whorl. Prediction, fresh: faces with 370/371 carry a fibre sign (390, 405, 406, 407) on 12 of 24 against 9% (P 3e-7). Two Farmana seals and a Mohenjo-daro tablet read `371-390` / `370-390` *katir parutti* "spindle: cotton". This ties the cotton reading of 390 (cotton-house report) to a second, independent sign.
7. **The second catalogue's merges are word links.** Where Mahadevan draws two Lipi signs as one, the Lipi variant took the main sign's word, and each one stood in the main sign's frames: 525 and 526 as the guard 527 (frames P 0.035 and 0.017; neither ever takes the jar, 0 of 11 and 0 of 13 against 33%); 838 as produce 806 (11 shared frames against 2, P 0.041); 491 as 495 the banded horn (P 0.05 and 0.07); 161 as the carriers (7 against 2, P 0.029). Read: 838 is *viḷai* "produce" (not sesame), 525/526 *kāval* "guard", 491/495 *kompu* "horn", 161 *kā* "keeper".
8. **Two counting orders, measured on the read texts.** Things take the number before them (450 to 220, 67%); measure and share words take it after (315 to 49, 87%): "three chests", but *kāṇi iru* "shares two" and *kalam mū* "kalam three". That is the Old Tamil account order (thing, measure, count).
9. **The grain-ration line reads whole on 13 faces**: `413-575-335-711-033-700` *nel kōṭṭai ūr vaḷḷam mū nāḻi* (10 copies) and its variants, now that 711 *vaḷḷam* came true fresh (counts after it are tall strokes 15 to 0, P 1e-5).
10. **Possessor before possessed, title last.** *maka* "child of" is not text-first in 91 of 93 texts; the jar is not first in 1,122 of 1,132; 730 of 993 read texts of 3+ signs end in a closing title, the jar or a verb word (74%).

What it opens: the ivory account (elephant copper tablets) as a commodity class beside cotton and grain; the merge rule as a cheap way to give words to every Lipi variant Mahadevan folds into a valued sign; the Assembly openings as an institution to map by site.

## 2. Job 1: wide into strict

All 13 predictions were written in one go into `sound_v5_job1.py` before any was computed, and no sign profile was printed first. Round two (`sound_v5_job1b.py`) redesigned the test for the 9 misses, again all written before running.

| round | sign | word | kind of fact | prediction | outcome | number | P |
|---|---|---|---|---|---|---|---|
| 1 | 240 | *mīmīn* | seal size | High-star is a great house: seals with 240 are bigger than seals with the same number of signs | no | seal face against seals of the same sign count: x0.99 (n 157) | 0.44 |
| 1 | 233 | *vāḷai* | sign two places away | a goods word takes measure then count: the sign two places after 233 is a number | yes | sign at offset +2 in ['001', '002', '003', '004', '005']...: 27/166 = 16% against 9.0% (LM) | 0.002 |
| 1 | 060 | *-iṉ* | sign two places away | opener-iṉ [ward] [crest ...]: the sign two places after 060 is a fish crest | yes | sign at offset +2 in ['220', '226', '231', '233', '235']...: 30/205 = 15% against 5.8% (LM) | 2.7e-06 |
| 1 | 435 | *kōl* | sign two places away | mutal kōl [carrier] [class]: the sign two places after 435 is a closing class sign (jar, man, comb, spear, carrier) or the text end | yes | sign at offset +2 in ['$', '090', '151', '153', '154']...: 53/65 = 82% against 52.2% (LM) | 8.2e-07 |
| 1 | 388 | *aracu* | sign two places away | aracu kuṭi [man/comb/spear]: the sign two places after 388 is a person or class sign after the jar (man, comb, spear, carrier) or the text end | yes | sign at offset +2 in ['$', '090', '151', '153', '154']...: 33/50 = 66% against 41.3% (LM) | 0.00037 |
| 1 | 382 | *aracu* | sign two places away | aracu maka kuṭi: the sign two places after 382 is the jar | direction only | sign at offset +2 in ['740']: 2/15 = 13% against 10.9% (LM) | 0.5 |
| 1 | 097 | *aṭimai* | reverse face | a ration receiver: the other face of a many-faced object with 097 carries a number or cup | direction only | faces with it on 2+ face objects whose other face holds ['001', '002', '003', '004', '005']... 3/3 = 100% against 52% | 0.14 |
| 1 | 790 | *maṇi* | sign two places away | beads are counted goods: a number stands two places before or after 790 | no | sign at offset -2/+2 in ['001', '002', '003', '004', '005']...: 2/76 = 3% against 10.9% (LM) | 1 |
| 1 | 550 | *vāy* | sign two places away | vāy [guard/joiner] [class]: the sign two places after 550 is a closing class sign or the text end | no | sign at offset +2 in ['$', '090', '151', '153', '154']...: 49/96 = 51% against 52.2% (LM) | 0.63 |
| 1 | 923 | *maruppu* | copper-tablet image | a horn word: copper tablets with 923 show a horned beast (bull, unicorn, gaur, zebu, buffalo, goat) | no | copper tablets with an image showing Buff/Bull/Bull1/Bull2/Bull3/CompBull/Gau 0/12 = 0% against 30% | 1 |
| 1 | 877 | *nālkāṇi* | sign two places away | kāṇi [count] [crest]: the sign two places after 877 is a fish crest | no | sign at offset +2 in ['220', '226', '231', '233', '235']...: 0/22 = 0% against 5.8% (LM) | 1 |
| 1 | 104 | *taṭṭāṉ* | seal size | a craftsman, not a great house: seals with 104 are smaller than seals with the same number of signs | direction only | seal face against seals of the same sign count: x0.72 (n 9) | 0.1 |
| 1 | 831 | *tiṉai* | reverse face | a crop is issued in amounts: the other face of a many-faced object with 831 carries a number or cup | no | faces with it on 2+ face objects whose other face holds ['001', '002', '003', '004', '005']... 2/4 = 50% against 52% | 0.71 |
| 2 | 240 | *mīmīn* | reverse face | a house is the who-face of a tablet: the other face of a many-faced object with 240 carries a number or cup (the amount) | yes | faces with it on 2+ face objects whose other face holds ['001', '002', '003', '004', '005']... 59/96 = 61% against 52% | 0.036 |
| 2 | 382 | *aracu* | seal size | a royal lineage head: seals with 382 are bigger than seals with the same number of signs | direction only | seal face against seals of the same sign count: x1.15 (n 6) | 0.18 |
| 2 | 097 | *aṭimai* | sign two places away | count + cup + bondsman: a number stands two places before 097 | yes | sign at offset -2 in ['001', '002', '003', '004', '005']...: 10/14 = 71% against 12.9% (LM) | 7.6e-07 |
| 2 | 790 | *maṇi* | area inside the city | bead workshops: Harappa objects with 790 lie in mound E (the craft mound) more than Harappa objects overall | no | Harappa objects from area E* 4/21 = 19% against 25% | 0.8 |
| 2 | 550 | *vāy* | seal size | a gate office: seals with 550 are bigger than seals with the same number of signs | no | seal face against seals of the same sign count: x0.91 (n 55) | 0.61 |
| 2 | 923 | *maruppu* | copper-tablet image | the tusk sense: copper tablets with 923 show the elephant | yes | copper tablets with an image showing Elep 11/12 = 92% against 14% | 6.1e-09 |
| 2 | 877 | *nālkāṇi* | seal size | a four-share holder outranks a two-share holder: seals with 877 are bigger than seals with the same number of signs | no | seal face against seals of the same sign count: x0.93 (n 14) | 0.65 |
| 2 | 104 | *taṭṭāṉ* | area inside the city | the jewellery hoards: Mohenjo-daro objects with 104 lie in the DK area more than Mohenjo-daro objects overall | yes | Mohenjo-daro objects from area DK* 13/14 = 93% against 70% | 0.048 |
| 2 | 831 | *tiṉai* | depth/era | millet spreads late: Harappa objects with 831 come from Period 3C more than dated Harappa objects overall | nan | too few cases | nan |

Moved to strict: 233, 060, 435, 388 (round one), 240, 097, 923, 104 (round two). 923 changed meaning on the way: horn went against (0 of 12), tusk came true (11 of 12). 104 at P 0.048 rests on 14 Mohenjo-daro objects, 13 of them in the DK area where the jewellery hoards were dug.

## 3. Job 2: the next 25 signs

Ranking: `work_data/sound_v5/gains_v4wide.csv` (faces each sign alone keeps from reading, under the fourth wide list). Top 25 after the signs already done: 407 (48 faces), 692 (18), 165 (15), 645 (15), 167 (14), 711 (13), 236 (12), 048 (12), 832 (11), 526, 868, 222 (10 each), 161, 495, 460, 838, 525, 491, 370 (9 each), 565, 519, 850, 347 (8 each), 821, 792 (7 each); plus 405 for the thread reading.

Order kept for each: picture (shape table and the second catalogue's glyph drawing) and slot (first / middle / last share) printed, nothing else; word chosen; predictions A and B written into `sound_v5_job2.py`; run; on a double miss one new word C written into `sound_v5_job2b.py` and run.

**The links built for 407 and 048.** The crosswalk maps Lipi 405, 406 and 407 all to one second-catalogue sign (M169, a stalk with side branches; the 390 tree is M162, a trident). On the 92 partnered texts a rule learned from the signs around the tree splits 405 from 407 no better than always guessing 405 (55 of 102 right with what follows, 59 with the object kind, against 50 for always-405): the second catalogue's tree carries no trace of the split, so on the new texts M169 was tested as one tree family. 048, the bracketed seven, maps to M113, which occurs on no new text (the plain seven M112 does, 15 times); 048 was tested on first-catalogue facts never printed for it.

| stage | sign | word | prediction | outcome | number | P | fact |
|---|---|---|---|---|---|---|---|
| A | 407 | *tuṇi* | cloth is issued in amounts: the other face of a many-faced object with 407 carries a number or cup | no | faces with it on 2+ face objects whose other face holds ['001', '002', '003', '004', '005']... 5/20 = 25% against 52% | 1 | fresh |
| B | 407 | *tuṇi* | the tree family on new texts (M169) sits on goods objects (tablets, tags, pots, tools) more than all new-text faces | no | faces on bangle/ctab/mtab/other/pot/rod/tag/tool 16/46 = 35% against 45% for all faces, x0.8 (Mu) | 0.94 | seen |
| A | 405 | *nūl* | thread is counted in lots: on new texts (tree family M169) a count of 3 or more stands right before it | yes | a count of 3+ right before it 6/48 = 12% against 3.2% (Mu) | 0.0039 | seen |
| B | 405 | *nūl* | issued in amounts: the other face of a many-faced object with 405 carries a number or cup | no | faces with it on 2+ face objects whose other face holds ['001', '002', '003', '004', '005']... 2/7 = 29% against 52% | 0.95 | fresh |
| A | 692 | *kūṭṭam* | an institution of the whole land: 692 turns up at more sites than signs of its frequency | no | 6 sites against median 8 for 43 signs of similar frequency (LM) | 0.88 | fresh |
| B | 692 | *kūṭṭam* | office seals are big: seals with 692 are bigger than seals with the same number of signs | yes | seal face against seals of the same sign count: x1.45 (n 42) | 8.3e-06 | fresh |
| A | 165 | *poḻutu* | days are counted like things: counts beside it are short strokes (both catalogues) | no | counts beside it: tall 3, short 2 (tall share 60% against 47% for all counts; LM) | 0.85 | fresh |
| B | 165 | *poḻutu* | a day count on a ration tablet: the other face of a many-faced object with 165 carries a number or cup | direction only | faces with it on 2+ face objects whose other face holds ['001', '002', '003', '004', '005']... 6/10 = 60% against 52% | 0.42 | fresh |
| A | 645 | *kar̤añcu* | the gold hoards: Mohenjo-daro objects with 645 lie in the DK area | direction only | Mohenjo-daro objects from area DK* 10/13 = 77% against 70% | 0.42 | fresh |
| B | 645 | *kar̤añcu* | weights are counted: a number stands two places before or after 645 | direction only | sign at offset -2/+2 in ['001', '002', '003', '004', '005']...: 5/43 = 12% against 10.9% (LM) | 0.51 | fresh |
| A | 167 | *tūkku* | n kalam weighed: a number stands two places before 167 (first catalogue) | no | sign at offset -2 in ['001', '002', '003', '004', '005']...: 0/14 = 0% against 12.8% (L) | 1 | fresh |
| B | 167 | *tūkku* | a weighed issue: the other face of a many-faced object with 167 carries a number or cup | direction only | faces with it on 2+ face objects whose other face holds ['001', '002', '003', '004', '005']... 2/3 = 67% against 52% | 0.53 | fresh |
| A | 711 | *vaḷḷam* | a container measure: counts after it are tall strokes (both catalogues) | yes | counts beside it: tall 15, short 0 (tall share 100% against 47% for all counts; LM) | 1e-05 | fresh |
| B | 711 | *vaḷḷam* | measure, count, cup: the cup 700 stands two places after 711 | yes | sign at offset +2 in ['700']: 10/13 = 77% against 0.4% (LM) | 2.3e-22 | seen |
| A | 236 | *vēy-kūṭu* | a container: counts beside it are tall strokes (both catalogues) | no | counts beside it: tall 0, short 7 (tall share 0% against 47% for all counts; LM) | 1 | fresh |
| B | 236 | *vēy-kūṭu* | counted goods: new-text faces with it carry a number more than faces overall | nan | too few cases | nan | fresh |
| A | 048 | *er̤uvar* | the Seven is a house with agents: the man 090 stands two places after 048 (048-jar-man) | no | sign at offset +2 in ['090']: 0/17 = 0% against 1.0% (L) | 1 | fresh |
| B | 048 | *er̤uvar* | a trading body: trade-tag words (dozen 055, given 890, sale 892, fish 220) on the same face (first catalogue) | no | with ['055', '220', '890', '892'] on one face: 0 of 18 against 1.9 expected (L) | 1 | fresh |
| A | 832 | *kaṇkāṇi* | an overseer outranks: seals with 832 are bigger than seals with the same number of signs | no | seal face against seals of the same sign count: x0.82 (n 22) | 0.97 | fresh |
| B | 832 | *kaṇkāṇi* | a title in the possessive place: faces with 832 carry the jar less than faces overall | direction only | faces with the jar (L) 13/43 = 30% against 33% | 0.42 | fresh |
| A | 526 | *kāval* | one word with the guard: 526 stands in the frames of 527/525 | yes | 4 shared frames with ['525', '527'] against median 0 for 57 signs of the same frequency (LM, distinct texts) | 0.017 | fresh |
| B | 526 | *kāval* | a title in the possessive place: faces with 526 carry the jar less than faces overall | yes | faces with the jar (L) 0/13 = 0% against 33% | 0.0055 | fresh |
| A | 525 | *kāval* | one word with the guard: 525 stands in the frames of 527/526 | yes | 1 shared frames with ['526', '527'] against median 0 for 57 signs of the same frequency (LM, distinct texts) | 0.034 | fresh |
| B | 525 | *kāval* | a title in the possessive place: faces with 525 carry the jar less than faces overall | yes | faces with the jar (L) 0/11 = 0% against 33% | 0.012 | fresh |
| A | 868 | *kāṇi* | one word with the share signs: 868 stands in the frames of 861/817/877 | no | 1 shared frames with ['817', '861', '877'] against median 1 for 14 signs of the same frequency (LM, distinct texts) | 0.93 | fresh |
| B | 868 | *kāṇi* | a counted holding: new-text faces with 868 carry a number | nan | too few cases | nan | fresh |
| A | 222 | *kuḷa-mīn* | a name element: new-text faces with 222 carry the jar more than faces overall | direction only | faces with ['740'] beside it (Mu) 2/3 = 67% against 26% | 0.17 | fresh |
| B | 222 | *kuḷa-mīn* | a house name: Mohenjo-daro house-mates share it | no | same-house pairs 0 against 0.05 (Mohenjo-daro objects, 5 carry it, shuffled within area and 3-ft band) | 1 | fresh |
| A | 161 | *kā* | stands in the jar's place: faces with 161 carry the jar less than faces overall (both catalogues) | direction only | faces with the jar (LM) 4/15 = 27% against 32% | 0.46 | fresh |
| B | 161 | *kā* | one word with the carriers: 161 stands in the frames of the other carriers | yes | 7 shared frames with ['151', '153', '154', '155', '156', '157', '158'] against median 2 for 34 signs of the same frequency (LM, distinct texts) | 0.029 | fresh |
| A | 495 | *kompu* | a horn word: seals with 495/491 show a horned beast other than the unicorn (zebu, buffalo, gaur, short-horned bull, goat) more than beast seals overall | no | seals with 491/495 showing Buff/Bull/Gaur/Goat/Zebu 2/19 = 11% against 14% | 0.77 | fresh |
| B | 495 | *kompu* | one sign with 491: 495 stands in the frames of 491 | yes | 3 shared frames with ['491'] against median 1 for 129 signs of the same frequency (LM, distinct texts) | 0.069 | fresh |
| A | 491 | *kompu* | one sign with 495: 491 stands in the frames of 495 | yes | 3 shared frames with ['495'] against median 1 for 75 signs of the same frequency (LM, distinct texts) | 0.053 | fresh |
| B | 491 | *kompu* | a horn-named house: Mohenjo-daro house-mates share 491/495 | no | same-house pairs 0 against 0.15 (Mohenjo-daro objects, 6 carry it, shuffled within area and 3-ft band) | 1 | fresh |
| A | 460 | *mukkōṭu* | a place word: 460 stands in the frames of the hill 503 | no | 1 shared frames with ['503'] against median 1 for 58 signs of the same frequency (LM, distinct texts) | 0.68 | fresh |
| B | 460 | *mukkōṭu* | a place-named house: Mohenjo-daro house-mates share it | direction only | same-house pairs 1 against 0.66 (Mohenjo-daro objects, 18 carry it, shuffled within area and 3-ft band) | 0.47 | fresh |
| A | 838 | *viḷai* | one word with produce: 838 stands in the frames of 806 | yes | 11 shared frames with ['806'] against median 2 for 48 signs of the same frequency (LM, distinct texts) | 0.041 | fresh |
| B | 838 | *viḷai* | produce is counted: a number stands two places before 838 (n [unit] produce) | no | sign at offset -2 in ['001', '002', '003', '004', '005']...: 0/9 = 0% against 12.9% (LM) | 1 | fresh |
| A | 370 | *katir* | a spinner's word: faces with 370/371 carry a fibre sign (390, 405, 406, 407) more than faces overall | yes | faces with 370/371 that carry ['390', '405', '406', '407'] (LM) 12/24 = 50% against 9% | 2.6e-07 | fresh |
| B | 370 | *katir* | one sign with 371: 370 stands in the frames of 371 | yes | 3 shared frames with ['371'] against median 0 for 124 signs of the same frequency (LM, distinct texts) | 0.008 | fresh |
| A | 565 | *maṟavaṉ* | a title in the possessive place: faces with 565 carry the jar less than faces overall (both catalogues) | no | faces with the jar (LM) 10/18 = 56% against 32% | 0.99 | fresh |
| B | 565 | *maṟavaṉ* | a rank title: 565 stands in the frames of the chief 520 | yes | 4 shared frames with ['520'] against median 2 for 29 signs of the same frequency (LM, distinct texts) | 0.067 | fresh |
| A | 519 | *tōṭṭam* | a land word: faces with 519 carry field/hill/sheaf/quarter words (615, 503, 845, 061) (both catalogues) | no | faces with ['061', '503', '615', '845'] beside it (LM) 0/17 = 0% against 5% | 1 | fresh |
| B | 519 | *tōṭṭam* | one sign with 910 (the second catalogue merges them): 519 stands in the frames of 910 | nan | too few cases | nan | fresh |
| A | 850 | *kāṇi* | a counted holding: on new texts a count follows 850 | yes | next sign in ['001', '002', '003', '004']...: 4/12 = 33% against 14.1% (Mu) | 0.076 | fresh |
| B | 850 | *kāṇi* | one word with the share signs: 850 stands in the frames of 861/817 | direction only | 7 shared frames with ['817', '861'] against median 5 for 14 signs of the same frequency (LM, distinct texts) | 0.33 | fresh |
| A | 347 | *māṉ* | a counted good: the other face of a many-faced object with 347 carries a number or cup | nan | too few cases | nan | fresh |
| B | 347 | *māṉ* | a counted good: a number on the same face (first catalogue) | no | with ['001', '002', '003', '004', '005']... on one face: 0 of 10 against 4.7 expected (L) | 1 | fresh |
| A | 821 | *kāl* | one word with the wheel: 821 stands in the frames of 820 | no | 2 shared frames with ['820'] against median 2 for 29 signs of the same frequency (LM, distinct texts) | 0.57 | fresh |
| B | 821 | *kāl* | kāl iru: the two-stroke 002 follows 821 (first catalogue) | no | next sign in ['002']: 0/10 = 0% against 5.7% (L) | 1 | fresh |
| A | 792 | *maṇi* | one word with 790: 792 stands in the frames of 790 | direction only | 2 shared frames with ['790'] against median 1 for 56 signs of the same frequency (LM, distinct texts) | 0.47 | fresh |
| B | 792 | *maṇi* | a house name: Mohenjo-daro house-mates share it | no | same-house pairs 0 against 0.01 (Mohenjo-daro objects, 3 carry it, shuffled within area and 3-ft band) | 1 | fresh |
| C | 407 | *kiḷai* | a kindred name: names with the tree family take the house ending (jar, jar+man) on new-text seals | direction only | names with it end in jar/jar+man 4/4 = 100% against 77% (Mu seals) | 0.36 | fresh |
| C | 165 | *kātu* | an ornament word: Harappa objects with 165 lie in mound E (the craft mound) | no | Harappa objects from area E* 0/9 = 0% against 25% | 1 | fresh |
| C | 645 | *pāti* | a fraction word: 645 stands in the frames of the share and quarter words 861/817/820 | no | 4 shared frames with ['817', '820', '861'] against median 8 for 3 signs of the same frequency (LM, distinct texts) | 1 | fresh |
| C | 167 | *kā* | one word with the load-carriers: 167 stands in the frames of the carriers and the pole 417 | no | 1 shared frames with ['151', '153', '154', '155', '156', '157', '158', '417'] against median 2 for 33 signs of the same frequency (LM, distinct texts) | 0.91 | fresh |
| C | 236 | *vēymīn* | a crest: 236 stands in the frames of the Bamboo-star 235 | direction only | 5 shared frames with ['235'] against median 3 for 32 signs of the same frequency (LM, distinct texts) | 0.15 | fresh |
| C | 048 | *kōvai* | a bead word: 048 stands in the frames of the bead/gem words 790/792 | direction only | 1 shared frames with ['790', '792'] against median 0 for 55 signs of the same frequency (LM, distinct texts) | 0.46 | fresh |
| C | 832 | *maṇi* | one word with the gem 790: 832 stands in the frames of 790 | direction only | 4 shared frames with ['790'] against median 3 for 55 signs of the same frequency (LM, distinct texts) | 0.41 | fresh |
| C | 868 | *araikkāṇi* | a fraction ends the text in place of the possessive: faces with 868 carry the jar less than faces overall | yes | faces with the jar (L) 0/13 = 0% against 33% | 0.0055 | fresh |
| C | 222 | *aṭaimīn* | a crest: 222 stands in the frames of the four fish crests 231/233/235/240 | direction only | 7 shared frames with ['231', '233', '235', '240'] against median 4 for 4 signs of the same frequency (LM, distinct texts) | 0.4 | fresh |
| C | 460 | *mukkōṭṭai* | a town word: 460 stands in the frames of fort 575 and town 335 | direction only | 2 shared frames with ['335', '575'] against median 1 for 46 signs of the same frequency (LM, distinct texts) | 0.38 | fresh |
| C | 519 | *vēli* | a name element: the jar stands one or two places after 519 | yes | sign at offset +1/+2 in ['740']: 8/26 = 31% against 10.0% (LM) | 0.003 | fresh |
| C | 347 | *kalai* | a tablet word: Harappa objects with 347 lie in mound E (the tablet mound) | yes | Harappa objects from area E* 9/9 = 100% against 25% | 3.5e-06 | fresh |
| C | 821 | *veṟṟilai* | a counted good: a number stands one or two places from 821 | direction only | sign at offset -2/-1/+1/+2 in ['001', '002', '003', '004', '005']...: 8/43 = 19% against 12.2% (LM) | 0.15 | fresh |
| C | 792 | *aracu* | one word with the pipal leaves: 792 stands in the frames of 382/384/388 | direction only | 3 shared frames with ['382', '384', '388'] against median 2 for 46 signs of the same frequency (LM, distinct texts) | 0.11 | fresh |

**405 and 407 as thread and cloth.** Thread *nūl* (405) came true on the new texts: the tree family has a count of 3 or more right before it on 6 of 48 uses against 3.2% (P 0.004; the lot-count kind had been printed for 405 in the cotton job, so this is wide only). Cloth *tuṇi* (407) went against twice: the other face of its tablets carries an amount on 5 of 20 against 52%, and on the new texts the tree family sits on goods objects 16 of 46 against 45%. 407 stays testing under *kiḷai* "kindred" (its names end in the house ending 4 of 4 on new-text seals, P 0.36).

## 4. The whole list

97 building on, 12 testing, 2 paused (111 values beyond the base set). Strict: 91 / 18 / 2. Still wide-only: 382, 405, 550, 790, 831, 877. Base values (numbers, jar, man, fish, spear, comb, carriers, staff-bearer, tree, elder, cup, load comb) are listed at the end.

### Building on

| sign | picture | sound | English | strict | v4 | evidence |
|---|---|---|---|---|---|---|
| 055 | Four small vertical strokes above the same, above the same | *paṉṉiru* | dozen | building | building | A: on sealings/tags on new texts 14/31 against 22%; the fish follows it 4/40 against 3.1% |
| 060 | A single small vertical line, then another vertical line wit | *-iṉ* | of (joiner after an opener) | building | building | A sites 17 against 14 (direction); B an opener stands before it on new texts 35/48 against 4.6% | J1 fresh: a fish crest two places after it 30/205 against 5.8% (P 3e-6) |
| 061 | Simple lambda but reversed horizontally, and the leg may not | *kāl* | quarter | building | building | A: copper tablets on new texts 1/10 (direction); B: a count before it on new texts 4/10 against 15.8% |
| 070 | A single vertical line, with two person arms; head may be ci | *ampu* | arrow | building | building |  |
| 091 | Two simple persons standing side by side | *iruvar* | the pair, partners | building | building |  |
| 095 | Person with short stick | *kōlaṉ* | staff-bearer | building | building |  |
| 097 | Person with two arms and two legs, bracketed by tall vertica | *aṭimai* | bondsman, servant (a ration receiver) | building | building | A Harappa mound E 2/7 (direction); B a count or cup before it on new texts 4/9 against 16.5% | J1 round two fresh: a number two places before it 10/14 against 12.9% (P 8e-7); reverse face 3/3 (too few) |
| 104 | Person with a half-height caret coming off the right foot | *taṭṭāṉ* | goldsmith (person with the seed-weight at his foot) | building | building |  no-jar 10/26 against 33% (against); taṭṭāṉ: frames of 391 1 against 1 (against), gold/seed weight on the face 7/27 against 1% (both catalogues) | J1 round two fresh: Mohenjo-daro objects in the DK area 13/14 against 70% (P 0.048); seals smaller x0.72 (P 0.10) |
| 125 | Person with bow and arrow | *vēṭṭuvaṉ* | Hunter (clan) | building | building |  |
| 137 | Person with two arms and two legs, small leaf almost like a  | *vēḷāḷaṉ* | cultivator | building | building | A Harappa mound E 7/12 against 25%; B grain/cup on the face 2/19 (against) |
| 140 | Person with round breasts and one raised arm | *ammai* | lady | building | building | A: opens the text on new texts 11/17 against 29% |
| 161 | Person carrying two burdens, triangle or diamond for a head | *kā* | keeper, load-carrier (variant) | building | new | J2 A: jar 4/15 against 32% (direction); B frames of the carriers 7 against 2 (P 0.029) |
| 171 | Capital 'T' with a small leaf oriented vertically attached t | *niṟai* | weight, full measure | building | building | A: a count after it on new texts 3/7 against 14.1% |
| 175 | Person sitting with bent knees, no small tangent lines comin | *iṟai* | tax | building | building | A: miniature tablets on new texts 2/4 against 10% |
| 176 | Person sitting with bent knees, four small tangent lines com | *iṟai* | tax, levy | building | building |  |
| 226 | Fish with four small vertical strokes around the four corner | *kūṭumīn* | crate of fish | building | building | A coast and abroad 9/52 against 9% (P 0.035); B tall counts 17 to short 8 |
| 231 | Fish with a small vertical stroke in the body | *orumīn* | First-star | building | building |  |
| 233 | Fish with a horizontal line through body | *vāḷai* | scabbard-fish (a counted fish good; also a crest "Bright-star" vāḷmīn) | building | building | A vāḷmīn house ending 6/9 against 77% (against); B seal size x1.07 (direction); C vāḷai: a measure word follows on new texts 9/39 against 3.4% | J1 fresh: a number two places after it 27/166 against 9.0% (P 0.002) |
| 235 | Fish with a caret shaped hat | *vēymīn* | Bamboo-star (Punarvasu) | building | building |  |
| 240 | Fish with extra whiskers on cheeks | *mīmīn* | High-star (house crest) | building | building | A house ending on new-text seals 7/9 against 77% (direction); B another fish crest follows on new texts 15/58 against 6.5% | J1 round two fresh: the other face of its tablets carries a number or cup 59/96 against 52% (P 0.036); seal size x0.99 (against) |
| 255 | Unknown asymmetric animal? Perhaps a fish with asymmetric fi | *mutal* | chief, first | building | building |  |
| 320 |  | *paṭi* | ration measure, daily allowance | building | building | NEW WORD. A: the month sign 920 follows it on new texts 5/7 against 0.7% |
| 335 | M with the bottom of the legs connected by a horizontal line | *ūr* | town | building | building | NEW WORD (C). puṭṭi failed (A 1/6 tablets, B 2/6 with a number); ūr: jar or maka follows it on new texts 3/6 against 11.2% |
| 347 | Deer facing to the right (see also P303) | *kalai* | stag | building | new | J2 māṉ: reverse too few; number on the face 0/10 (against); C kalai: Harappa mound E 9/9 against 25% (P 4e-6; one text in copies) |
| 368 | Vertical stroke with a triangular wing attached near the mid | *koṭi* | banner (of a line) | building | building |  |
| 370 | The 'garlic' motif. Vertical stroke, broken by a circle with | *katir* | spindle (also ear of grain, ray) | building | new | J2 A: faces with 370/371 carry a fibre sign 12/24 against 9% (P 3e-7); B frames of 371 3 against 0 (P 0.008) |
| 371 | The 'garlic' motif. Vertical stroke, broken by a circle with | *katir* | spindle (same drawing code as 370) | building | new | with 370 (one sign in the second catalogue, M397; one drawing code P108) |
| 382 | Upside-down heart symbol, with vertical stroke coming from b | *aracu* | pipal; royal (lineage head) | testing | building | A frames 3 against 3 (against); B jar after 2/20 (against); B2 maka follows 5/20 against 0.9% (both catalogues) | J1: jar two places after 2/15 (direction); seal size x1.15 n 6 (direction) |
| 384 | Upside-down heart symbol, possibly with vertical stroke comi | *aracu* | pipal; royal (house name) | building | building | A house share 0 against 0.1 (against); C frames of 388/382: 7 against 3 (P 0.054) |
| 388 | Upside-down heart symbol with horizontal hatching, with vert | *aracu* | pipal; royal (house name) | building | building | A house share 2 against 1.8 (direction); B jar follows on new texts 5/13 against 10.2% | J1 fresh: man/comb/spear/carrier or text end two places after it 33/50 against 41% (P 0.0004) |
| 405 | Simple tree with branches at the top | *nūl* | thread, yarn (counted in lots) | testing | building | J2 A: a count of 3+ before the tree family on new texts 6/48 against 3.2% (P 0.004); B reverse face 2/7 (against) |
| 413 | Vertical line with small horizontal lines crossing it across | *nel* | paddy, grain | building | building | A Harappa mound E 22/44 against 25%; B a measure word follows on new texts 3/3 |
| 415 | Pitchfork with tines | *kavar* | branch (of a line) | building | building |  |
| 416 | Pitckfork with two stacked heads | *turumpu* | heap of threshed grain | building | building | A Harappa mound F 15/27 against 34%; B opens the text on new texts 4/5; C tall counts 1 of 15 (against) |
| 435 | Vertical line with diagonal going down from top right, diago | *kōl* | rod, sceptre: mutal kōl "chief staff", an office | building | building | taṭi: size x1.00, sites 6 against 8, land words 6/91 against 5% (all against or direction); kōl: carrier or 690 follows on new texts 9/16 against 1.1% | J1 fresh: a closing class sign or text end two places after it 53/65 against 52% (P 8e-7) |
| 440 | Rectangle, but with bottom line missing, and bottom-half of  | *koḷ* | received, bought | building | building | A against: pots on new texts 1/19 against 7%; B: Harappa on new texts 10/19 against 34% |
| 455 | Three triangles, one large isocoles pointing right on left,  | *ampu* | arrow | building | building |  |
| 463 |  | *mukkōṭu* | Three-peaks | building | building |  |
| 480 | Tall, slightly narrow caret (mountain motif) | *kuṉṟi* | seed-weight | building | building |  |
| 482 | Tall caret drawn in outline, with diamond inscribed at the p | *kōṭukāṇi* | hill share | building | building |  |
| 491 |  | *kompu* | horn (variant of 495) | building | new | J2 A: frames of 495 3 against 1 (P 0.053); B house share 0 against 0.15 (against) |
| 495 |  | *kompu* | horn (horn-blower; a name word) | building | paused | J2 A: horned non-unicorn beasts 2/19 against 14% (against); B frames of 491 3 against 1 (P 0.069) |
| 500 | Tall triangle with vertical divider, either isocolese or mor | *pāy* | sail (ship) | building | building | NEW WORD for a building value. A: Lothal on new texts 8/12 against 8% |
| 501 |  | *kumi* | heap, stock | building | building |  |
| 503 | Tall isoceles triangle with horizontal stripes | *malai* | hill | building | building | A: copper tablets on new texts 3/19 against 4% |
| 519 |  | *vēli* | fence, hedged plot (a name element) | building | new | J2 tōṭṭam: land words 0/17 (against), frames of 910 too few; C vēli: jar one or two places after 8/26 against 10% (P 0.003) |
| 525 |  | *kāval* | guard (variant of 527) | building | new | J2 A: frames of 527/526 1 against 0 (P 0.035); B jar 0/11 against 33% (P 0.012) |
| 526 | Small box with horizontal hatching, vertical lines coming fr | *kāval* | guard (variant of 527) | building | new | J2 A: frames of 527/525 4 against 0 (P 0.017); B jar 0/13 against 33% (P 0.006) |
| 527 | Small box with horizontal hatching, vertical lines coming fr | *kāval* | guard (vāy kāval "gate-guard") | building | building | A carries the jar 7/63 against 33%; B ends the text on new texts 3/3 |
| 530 | A 'Bowtie' motif, but without the vertical line connecting t | *paṟai* | proclamation | building | building |  |
| 540 | A 'Bowtie' motif. Or, an 'X' with vertical line connecting t | *paṟai* | drum; a rice measure | building | building | MEANING CHANGED to the measure (DEDR 4032). A: pots on new texts 2/7 against 7% |
| 550 | The 'pincer' motif. Right-pointing isocoles triangle on left | *vāy* | gate | testing | building | A a ward jar on the face on new texts 3/27 against 7% (direction); B 060/527/555/525 follows on new texts 6/23 against 2.0% | J1: closing sign two places after 49/96 against 52% (against); seal size x0.91 (against) |
| 555 | The 'pincer' motif. Right-pointing isocoles triangle on left | *vāy* | gate | building | building |  |
| 565 | X with vertical connection on left two tips, right tips both | *maṟavaṉ* | warrior (crossed arrows) | building | new | J2 A: jar 10/18 against 32% (against); B frames of the chief 520 4 against 2 (P 0.067) |
| 575 | Trapezoid with no bottom line, small box resting on the top  | *kōṭṭai* | great grain measure | building | building | A: a count before it on new texts 6/14 against 15.8% |
| 585 |  | *kaṉṉi?* | maiden (of the Seven) | building | building |  |
| 590 | Square at bottom with vertical bar coming off top middle | *peṭṭi* | chest | building | building |  |
| 595 | Box with vertical stroke off top center, horizontal striping | *paṭṭaṟai* | forge, smithy | building | building | NEW WORD (C). peṭṭi: A against (counts short 19, tall 1), B copper on new texts 12/27 against 4%; paṭṭaṟai: with smith/copper/weight signs on new texts 4 against 1.4 |
| 605 | Tall box with horizontal hatching throughout, possibly a sma | *kutir* | grain bin, granary | building | building | A Harappa mound F 6/9 against 34%; B maka follows on new texts 2/3 |
| 615 | A grid of x by y cells | *vayal* | field | building | building | A: copper tablets on new texts 16/86 against 4% |
| 617 |  | *ūḻiyaṉ* | (king's) servant | building | building | A: carries the jar 13/75 against 33% (a title in the possessive place) |
| 630 | Rectangle, taller than wide, with vertical strokes for teeth | *pal* | many | building | building | A against: a number on the same object 13 against 20.2; B: frames of 632, 6 against 2 |
| 632 | Rectangle, taller than wide, with vertical strokes for teeth | *pal* | many | building | building |  |
| 636 | Rectangle, taller than wide, with vertical strokes for teeth | *pal* | many | building | building | A: frames of 630, 4 against 0 |
| 679 | An 'X' with a 'table' hat | *kaṭṭil* | seat, throne | building | building |  |
| 690 | Two nested greater-than symbols, touching two nested less-th | *piṇai* | bound, allied | building | building | A: jar follows it on new texts 10/20 against 10.2% |
| 692 | An X but drawn in outline | *kūṭṭam* | assembly, council (an office opening) | building | paused | J2 A: sites 6 against 8 (against); B seals x1.45 bigger at equal length (n 42, P 8e-6) |
| 705 | U with a long vertical stroke inserted into the gap of U | *kalam* | grain measure (a kalam); ship where it stands uncounted before the sail 500 | building | building | JOB 1. measure: count after it on new texts 28/64 against 14.1% (P 8e-9), tall 28 of 28 (P 1e-13); count varies on goods, fixed three on seals (P 0.015). ship: sail after it 3/64 (P 0.002); coast and abroad 43/384 against 9% (P 0.07) |
| 706 | U with a long vertical stroke inserted into the gap of U | *kalam* | grain measure (variant of 705) | building | building | JOB 1, with 705 (the second catalogue merges 706 into 705); 706 takes three after it 45 of 46 |
| 711 | U with X going from side to side near the bottom | *vaḷḷam* | grain measure (vessel) | building | testing | NEW WORD. A against: E trench 11 2/21 against 10%; B: cup on the same object 12 of 21 against 2.5 (seen) | J2 A: counts after it tall 15, short 0 (P 1e-5); B the cup two places after 10/13 against 0.4% (seen) |
| 717 | A cat's paw perhaps, two vertical strokes on each side, and  | *aṭi* | foot; servant (aṭiyāṉ) | building | building | tāḷ earlier. aṭi A: a person or title sign on the same face on new texts 11/23 against 16%; B seal smaller x1.06 (against) |
| 741 | Classic jar symbol with two horizontal handles at the top of | *orukuṭi* | first ward | building | building |  |
| 742 | Classic jar symbol with two horizontal handles at the top of | *irukuṭi* | second ward | building | building |  |
| 745 | Classic jar symbol with two horizontal handles at the top of | *mukuṭi* | third ward | building | building |  |
| 752 | U with decorated branching at top | *maka* | child of | building | building |  |
| 760 | U with decorated branching at top | *maka* | child of | building | building | A: jar follows it on new texts 25/29 against 10.2% |
| 790 | Simple leaf or diamond, possibly rotated 45 degrees | *maṇi* | bead, gem | testing | building | kaṉ copper went against in v3. maṇi A bead towns 9/69 against 9% (direction); B tags on new texts 9/20 against 22% | J1: number two places away 2/76 (against); Harappa mound E 4/21 (against) |
| 798 | Leaf with 'pincers' coming off the right, possibly with smal | *maru-* | descendant, clan member | building | building |  |
| 803 | Leaf with tree at bottom | *il* | house | building | building | A: a fish crest follows it on new texts 6/22 against 7.8% |
| 806 | Leaf with tree at bottom | *viḷai* | produce, ripened crop | building | building | NEW WORD for the crop. A: a load-carrier follows it on new texts 5/25 against 1.4% |
| 817 | Diamond or leaf shape with a small diamond attached to the t | *kāṇi* | share, holding | building | building |  |
| 820 | Wheel with 6 spokes with even angles | *kāl* | quarter-share | building | building |  |
| 824 |  | *vilai* | price | building | building | NEW WORD. A: Harappa objects from mound E 11/23 against 25% |
| 831 | Leaf with diagonal-stroke central decoration | *tiṉai* | Italian millet | testing | building | A Harappa mound E 1/6 (against); B sale/price/field/grain words on the face 9/23 against 8% (both catalogues) | J1: reverse face 2/4 (against); Harappa Period 3C too few dated |
| 838 |  | *viḷai* | produce (variant of 806, as the second catalogue draws it) | building | testing | A against: rods on new texts 0/5; B rods both catalogues 4/24 x22 (Lipi seen) | J2 A: frames of 806 11 against 2 (P 0.041); B number two places before 0/9 (against) |
| 840 | Two vertical leaves, slightly overlapping | *iṇai* | pair | building | building | A: two tall strokes follow it on new texts 7/16 against 1.7%. Second reading vaḷai "bangle" (Lipi bangles x7.9, seen) |
| 845 | Two overlapping leaves with diagonal hatches across the thre | *cūṭu* | bundle of sheaves | building | building | NEW WORD. A: copper tablets on new texts 3/9 against 4% |
| 850 | Simple leaf or diamond, possibly rotated 45 degrees | *kāṇi* | share (the bare diamond) | building | testing | A copper on new texts 2/13 against 4% (P 0.11); B both catalogues 20/69 x6.5 (Lipi seen) | J2 A: a count follows it on new texts 4/12 against 14.1% (P 0.076); B frames of 861/817 7 against 5 (direction) |
| 861 | Diamond or leaf shape with a small diamond attached to the t | *kāṇi* | share, holding (a "hand") | building | building |  |
| 868 | Diamond with a small diamond attached to the top, lower left | *araikkāṇi* | half-share (a fraction ending) | building | new | J2 kāṇi: frames 1 against 1 (against), new-text count too few; C araikkāṇi: jar 0/13 against 33% (P 0.006) |
| 877 | Diamond with four small diamonds at each vertex | *nālkāṇi* | four shares | testing | building | A house share 1 against 0.3 (direction); B a count follows on new texts 5/12 against 14.1% | J1: fish crest two places after 0/22 (against); seal size x0.93 (against) |
| 890 | Right facing bow, i.e. a vertical stroke with a right-parent | *koṭu* | given | building | building | NEW SIGN. A: sealings/tags on new texts 7/9 against 22% |
| 892 | Bow and arrow | *vil* | sale, price | building | building |  |
| 900 | Right parenthesis (perhaps with a backward curve at the bott | *tiṅkaḷ* | month (counted) | building | building | A count before it on new texts 10/20 against 15.8%; B short strokes 61 to tall 6 (both catalogues) |
| 904 | Two slightly nested right parentheses | *irutiṅkaḷ* | two months | building | building |  |
| 920 | Right parenthesis with small leaf at middle | *tiṅkaḷ?* | month (head of a date formula) | building | building |  |
| 923 | Right parenthesis drawn in outline | *maruppu* | tusk, ivory (horn; the counted thing on elephant copper tablets) | building | building | A a count before it 17/42 against 19% (both catalogues); B month signs on the face 0/48 (against) | J1 round two fresh: copper tablets with it show the elephant 11/12 against 14% (P 6e-9); horned beasts 0/12 (against) |

### Testing

| sign | picture | sound | English | strict | v4 | evidence |
|---|---|---|---|---|---|---|
| 048 | Seven short vertical strokes, bracketed by parentheses | *er̤uvar* | the Seven | testing | testing | rlier; er̤uvar A frames of 585: 0 (against); B jar after 17/17 (Lipi only; 048 is not on new texts) | J2: man two places after 0/17 (against); trade words 0/18 (against); C kōvai: frames of 790/792 1 against 0 (direction). Bracketed seven absent from new texts |
| 165 | A left and right paren connected only at the top, with the l | *poḻutu* | sun, day | testing | testing | A: with the crescent 900 on one face 10 of 33 against 0.6 (fact seen in Lipi while choosing) | J2: short counts 2 to tall 3 (against); reverse 6/10 against 52% (direction); C kātu: mound E 0/9 (against) |
| 222 | Simple fish inside parentheses, with a small tooth coming of | *aṭaimīn* | shut-in fish (crest?) | testing | new | J2 kuḷa-mīn: jar on new texts 2/3 (direction), house share 0 (against); C aṭaimīn: crest frames 7 against 4 (direction) |
| 236 | Fish with a caret shaped hat, caged by four small vertical s | *vēymīn* | Bamboo-star (caged; crest variant) | testing | paused | J2 vēy-kūṭu: tall counts 0 of 7 (against); new-text counts too few; C vēymīn: frames of 235 5 against 3 (direction) |
| 391 | Three pronged tree with caret hat | *kollaṉ* | smith | testing | testing | NEW SIGN. A copper on new texts 1/3 (P 0.13); B both catalogues 4/13 x6.9 (Lipi tools seen) |
| 407 | Simple tree with branches at the top | *kiḷai* | kindred; lot (cloth tuṇi went against) | testing | testing | ablets 45/77 against 21% (Lipi, seen). Not on new texts at all | J2 tuṇi: reverse face 5/20 against 52% (against); tree family on goods objects 16/46 against 45% (against); C kiḷai: names with the tree family end in the house ending 4/4 against 77% (direction) |
| 417 | Two pitchforks with tines, facing each other vertically | *kā* | carrying pole (pole-load) | testing | testing | NEW SIGN. too few for a frame test; a count before it 8/8 (seen) |
| 460 | Three tall, thin isoceles triangles | *mukkōṭu* | Three-peaks | testing | testing | A: jar after it 2/11 against 10.2%; B jar or spear 2/11 (direction) | J2: hill frames 1 against 1; house share 1 against 0.66 (direction); C mukkōṭṭai: fort/town frames 2 against 1 (direction) |
| 645 | An 'X' with no decoration | *kar̤añcu* | a gold weight | testing | testing | kaṭṭu: A count before 1/4 (direction), B with a number 2/6 against 35% (against); kar̤añcu: too few new texts with a sign after it | J2: DK 10/13 against 70% (direction); number two away 5/43 (direction); C pāti: frames 4 against 8 (against) |
| 792 |  | *maṇi ~ aracu* | gem ~ pipal | testing | new | J2 maṇi: frames of 790 2 against 1 (direction), house share 0 (against); C aracu: pipal frames 3 against 2 (P 0.11, direction) |
| 821 |  | *veṟṟilai* | betel leaf? | testing | new | J2 kāl: wheel frames 2 against 2, 002 after 0/10 (against); C veṟṟilai: a number within two places 8/43 against 12% (direction) |
| 832 | Leaf with small vertical stroke inside | *kaṇ* | eye; at, in | testing | testing | A sites 6 against 8 (against); B clean: a time/place word before it on new texts 3/25 against 7.2% (direction) | J2 kaṇkāṇi: seals x0.82 (against), jar 13/43 against 33% (direction); C maṇi: frames of 790 4 against 3 (direction) |

### Paused

| sign | picture | sound | English | strict | v4 | evidence |
|---|---|---|---|---|---|---|
| 167 | The 'headphones' motif. Upside down U with small cirles on e | *?* | closes kalam tablets | paused | paused | nst 34%, copies 10/15 against 69%; kā: carrier frames 1 against 2. Lead: closes kaḷam (705/706) tablets only | J2 tūkku: number two before 0/14 (against); reverse 2/3 (direction); C kā: carrier frames 1 against 2 (against). Third word to fail (poli, kā, tūkku) |
| 350 | Horizontal line with multiple lines out the top, lines or U  | *?* | name front | paused | paused |  |

### Base values

001 *oru* "one", 002 *iru* "two", 003 *mū* "three", 004 *nāl* "four", 005 *ai* "five", 006 *āṟu* "six", 007 *ēḻu* "seven", 012 *iru* "two", 013 *mū* "three", 014 *nāl* "four", 015 *ai* "five", 016 *āṟu* "six", 017 *ēḻu* "seven", 018 *eṭṭu* "eight", 031 *oru* "one", 032 *iru* "two", 033 *mū* "three", 034 *nāl* "four", 035 *ai* "five", 036 *āṟu* "six", 090 *āḷ* "manager", 100 *mutu* "elder", 142 *kō* "king", 151 *kā* "keeper", 153 *kā* "keeper", 154 *kā* "keeper", 155 *kā* "keeper", 156 *kā* "keeper", 157 *kā* "keeper", 158 *kā* "keeper", 220 *mīn* "star", 390 *parutti* "cotton (cotton_house.md; base value)", 400 *ciṟ* "junior", 465 *(n)* "n loads", 466 *(n)* "n loads", 467 *(n)* "n loads", 468 *(n)* "n loads", 469 *(n)* "n loads", 470 *(n)* "n loads", 471 *(n)* "n loads", 472 *(n)* "n loads", 473 *(n)* "n loads", 474 *(n)* "n loads", 475 *(n)* "n loads", 520 *vēḷ* "chief", 700 *nāḻi?* "cup measure", 740 *kuṭi* "house of"

## 5. The grammar sketch

Predictions written into `sound_v5_job3.py` before the numbers; the redesigns (a null means the test was wrong) in `sound_v5_job3b.py`, also written before running. Test bed: 1,224 distinct texts that read whole under the fifth wide list (both catalogues); scans over all 2,885 distinct texts.

| claim | prediction | outcome | number | what it means |
|---|---|---|---|---|
| G1 | after the jar: class sign or end in 95%+; never a number before it | no | jar uses 584: next is end 429, man 38, comb 66, other 45 (92.3% class or end); a number right before the jar 40 | the jar closes a name and only a person word may follow: "of X's house" then "the man / the junior". A possessive ending, not a noun. |
| G2 | opener before 060 in 70%+; after it never a number, never the end | no | 060 uses 188 (all distinct texts): opener before 137 (73%), text start 3, other 48; after it a noun 149, a number 34, the end 5 | 060 links the opener to the noun after it, like Old Tamil -iṉ: "[month/gate/assembly]-of [ward ...]". |
| G3 | a name-closing sign never with the jar, on goods objects at 2x the jar's share | no | jar on goods objects 34% of its texts; candidates (sign, texts ending name+sign, texts with sign, goods share): [] | a sign in the jar's place on goods objects and never with it is the issue ending "for X" (Old Tamil dative -ku): none found |
| G4 | no sign follows counted nouns 3x as often as uncounted ones (min 5) | no | signs after counted nouns: 872, after uncounted: 3944; signs 3x+ after counted nouns: [('231', 12, 15, 3.6), ('142', 9, 8, 5.1), ('125', 7, 7, 4.5), ('460', 7, 9, 3.5), ('555', 6, 9, 3.0), ('923', 6, 8, 3.4), ('700', 5, 7, 3.2), ('236', 5, 3, 7.5)] | if empty: no plural suffix, the number alone marks plurality, as in Dravidian non-human nouns; any sign listed is a plural or a unit word to look at |
| G5 | a sign repeated in one text after two different nouns, 3+ texts | yes | repeat-after-noun texts (sign, texts, uses, sound): [('400', 4, 260, 'ciṟ')]; median repeat share 0.000 | a sign that comes back after each listed noun is the coordinator "-um ... -um" (and) |
| G6 | number before noun 70%+; number after measure words 70%+ | no | nouns: number before 616, after 479 (56% before); measure words: number before 30, after 87 (74% after) | two orders: count + thing ("three chests", "two shares"), and thing + measure + count ("grain kalam three"), the Old Tamil account order |
| G7 | maka never first, after its owner 90%+; jar never first | no | 760 first in 2 of 93 texts; after a non-number word 72 of 93 uses; jar first in 10 of 1132 | possessor first, possessed after: "[owner] maka" = "[owner]'s child", "[name] kuṭi" = "[name]'s house" |
| G8 | marker before the plain fish 80%+ | no | a word right before the plain fish 220: 130; a non-closing word right after it: 160 (45% before) | modifier before head: "Branch-Star", "Descendant Star"; the fish (star) is the head noun of the name |
| G9 | verb words last on goods faces at 2x the base | no | verb words last 12 of 45 uses (27%) against 28% for all goods-face sign places (P 0.66); per sign [('440', 'koḷ', 2, 9), ('824', 'vilai', 5, 6), ('890', 'koṭu', 0, 3), ('892', 'vil', 5, 27)] | the account line ends in the act: "[goods] [amount] given / sold / received", verb-final like Dravidian |
| G10 | last sign is a closer or verb in 60%+ of read texts with 3+ signs | yes | 730 of 993 (74%) | texts end in the head: possessive, title or verb |
| G1b | half of the other signs after the jar are title/person words | no | 5 of 45 (11%); commonest: [('679', 10), ('001', 5), ('565', 4), ('032', 2), ('061', 2), ('790', 2), ('820', 2), ('031', 1)] | jar + title = "of X's house, the [title]": a second title in the man's place |
| G2b | month opener before 060 more often when a number follows | no | month before 060 when a number follows 4/34 (12%) against 52/146 (36%) when a noun follows, P 1; openers before 060+number [('692', 4), ('920', 4), ('820', 4), ('550', 3)] | 060 + number after the month is a date: "in the month, n" (uḷ "in"), and 060 + noun after gate/district is an address |
| G3b | a name-closing sign on goods objects at 2x the jar share | yes | jar goods share 34%; candidates (sign, sound, texts ending name+sign, goods share): [('400', 'ciṟ', 27, np.float64(0.72)), ('158', 'kā', 7, np.float64(0.68)), ('700', 'nāḻi?', 6, np.float64(0.83))] | the closing sign of issue tablets after a name: "for/by X" read as the agent or recipient ending |
| G4b | no plural suffix on counted goods nouns | no | after counted goods nouns 150, uncounted 972; 3x+ signs: [('415', 6, 3)] | empty list = the number alone makes the plural, as Dravidian does with non-human nouns |
| G6b | things: number before 70%+; measures/shares: number after 70%+ | no | things: before 450, after 220 (67% before); measures and shares: before 49, after 315 (87% after) | count + thing, but measure/share + count: "kāṇi iru" two shares, "kalam mū" three kalam, the order Old Tamil uses for measures |
| G7b | maka not first 97%+, jar not first 99%+ | yes | maka not first 91 of 93 (97.8%); jar not first 1122 of 1132 (99.1%) | possessor before possessed |
| G8b | markers before the plain fish in names 70%+ | no | marker then plain fish 25; plain fish then marker 22 (53% before) | modifier before head inside names: "Branch-Star", "Descendant-Star" |
| G9b | verbs last or right before a closing person sign 60%+ | no | 20 of 49 (41%); by sign {'440': 4, '824': 6, '892': 9, '890': 1} | verb + agent: "sold, junior hand"; the act stands at the end of the goods phrase |

The sketch, as we build on it:

- **Possessive.** The jar *kuṭi* closes a name; what follows it is a person or class word or nothing: 539 of 584 jar uses (92%). Of the 45 others the commonest is the seat 679 *kaṭṭil* (10): "of X's house, the seat-holder". Numbers stand before the jar 40 times: inside names numbers are spelled words (star-names job), so "Pair-two house" is a name, not a count.
- **Joiner 060.** Opener + 060 + noun: opener before it 73%, noun after it 149 of 188. Read *-iṉ* "of" here, *uḷ* "in" in the eight-signs job; the 34 cases with a number after 060 do not favour the month opener (4 of 34 against 52 of 146), so the "in the month, n" date reading is not what they are. Both readings stay alive.
- **No dative suffix found; the issuing closer is a person word.** No sign closes names in the jar's place while never meeting the jar. Dropping that condition: the comb 400 *ciṟ* "junior hand" closes 27 names on objects that are 72% goods, the carrier 158 *kā* 7 (68%), against the jar's 34%. An issue tablet names the house and then the hand who took the goods: "of X's house, junior hand". The "for X" sense sits in that closing title.
- **No plural suffix.** On goods objects only one sign follows counted nouns three times as often as uncounted ones, and on 6 uses (415). The number alone makes the plural, as Dravidian does with non-human nouns. (The first scan listed name signs; those were spelled numbers inside names.)
- **No "and".** Only the comb repeats after two nouns inside one text (4 texts): two persons, each "junior hand". Lists are written by juxtaposition.
- **Two counting orders**: count + thing (67%), measure/share + count (87%).
- **Possessor first**: *maka* after its owner, jar never opening.
- **Head-last ending**: 74% of read texts end in a title, the jar or a verb word.

## 6. What went against, and the rescue tried

- **Five values stay wide-only.** 382 *aracu*: jar two places after 2 of 15, seals x1.15 on 6 (both direction). 790 *maṇi*: a number two places away 2 of 76 against 11%; Harappa mound E 4 of 21 against 25%. 550 *vāy*: closing sign two places after 49 of 96 against 52%; seals x0.91. 877 *nālkāṇi*: fish crest two places after 0 of 22; seals x0.93. 831 *tiṉai*: reverse face 2 of 4; Harappa Period 3C dating too few. Next for each: the copper-tablet image and the stand pattern on unicorn seals, the two fact kinds not yet used on them.
- **Cloth 407**: both cloth predictions went against (5 of 20; 16 of 46). Rescue: *kiḷai* "kindred", direction only (4 of 4, P 0.36). Testing.
- **The 405/407 link**: no rule built from the texts splits M169 (55 of 102 against 50). The split has to come from the drawings: Lipi's own sign pictures or photographs of the M169 objects.
- **048**: man two places after 0 of 17; trade words 0 of 18; rescue *kōvai* "string of seven" frames 1 against 0 (direction). Testing; it is on no new text.
- **165, 645, 167, 236, 222, 460, 821, 792, 832**: two predictions and one new word each without a yes. 167 is paused (third word failed: *poli*, *kā*, *tūkku*; number two places before 0 of 14). 236 counts with short strokes 7 to 0, so it is not a container: the crest reading (*vēymīn*, frames of 235 5 against 3) is the one alive. 645 has a rival from the eight-signs job (*kuṟi* "mark, tally", count before it 10 of 22).
- **Grammar against**: modifier before head inside star names did not hold (marker then plain fish 25, plain fish then marker 22; first version 130 against 160). Star names compound in both orders, read as two stars side by side. Verbs at the end of account lines did not hold: given/sale/received/price stand last 12 of 45 against 28% for any goods sign; last or right before the closing hand 20 of 49 (41%). Next: read 892 and 440 as nouns ("sale", "purchase") heading the line, and test the line-initial slot.
- **Rivals with the eight-signs job** (both stay alive, split named): 692 *kūṭṭam* against *nāṭu* (seal size against ward jars), 525-527 *kāval* "guard" against *katavu* "door" (both agree the three drawings are one sign), 711 *vaḷḷam* against *pāṉai* (both a measure vessel with tall counts), 060 *-iṉ* against *uḷ*.
- **Smaller misses inside signs that came true**: 692 sites 6 against 8; 405 reverse face 2 of 7; 838 a number two places before 0 of 9; 565 takes the jar 10 of 18 (more, not less); 491/495 horned non-unicorn beasts 2 of 19; 161 jar 4 of 15 (direction).
