# The name slot taken apart

Reading order = stored order reversed. Data: 1,494 clean seal faces (no broken edge, no lost or ambiguous sign, every sign given a role by `gloss.py`). Of these 877 are tightly parsed, have a class sign and at least one name sign (871 different objects). All counts below are on these 877 unless stated. Scripts: `work_scripts/name_slot_build.py` (builds `work_data/name_rows.csv`), `name_slot_analysis.py` (Q1, Q2), `name_slot_analysis2.py` (Q3 to Q5), `name_slot_account.py` (house-rate tests, abroad round seals, the 25 seals), `name_slot_report.py` (this file). Raw printouts are in `jobs/out/name_slot_tabs/`.

**Name segment**, as used here: every sign between the opener block (diamond/wheel + two strokes, or the `060` cap) and the first class sign, with parser roles who, house, house-marker, fixed-ending, phrase, head, second-slot or mark. Counts, amounts and counted-things are left out. The parser's "house" role is only "the last name sign before the class", so on a one-sign name it calls the sign "house". That is why the name here is who plus house plus house-marker, not the who role alone. The who-only version is also run where it matters.

## Findings in short

1. Names are 1 sign (45%), 2 signs (33%), 3 signs (18%); 4 to 6 signs are 5%.
2. A name has a front and a back. 10 signs open names (fish signs 235, 240, 233, 231, plus 798, 806, 140, 013, 590, 017) and 15 signs close names (760, 100, 923, 585, 390, 405, 220, 550, 142 and six more). 342 of 486 multi-sign names (70%) start with one of the 10 or end with one of the 15; 105 do both.
3. The household element is the FRONT sign. Same-house seals share the first name sign (17 pairs against 11.8 by chance, P 0.053; 17 against 10.8 on the pair-type count, P 0.02); the last sign shows 11 against 8.2 (P 0.17). The clearest case is the fish: when two names in one house both start with a fish sign, it is the same fish in 15 of 23 pairs against 36% by chance (P 0.003). Each house keeps its own fish.
4. The back sign is tied to the class sign: last name sign against class has Cramer V 0.375 (P 0.0005); first name sign against class 0.263. The first name sign is tied to the animal on the seal (V 0.208, P 0.0035) and to the opener type (V 0.205, P 0.0085); the last sign is not (animal P 0.34, opener P 0.24).
5. Name-slot fillings: 23 signs cover 50%, 78 cover 80%, 209 cover 95% (289 sign types in 1,619 fillings, 136 seen once). The class slot: 1, 6 and 14 signs (24 types). The tail is long and not closing: a rarefaction curve keeps climbing and the Chao1 estimate is about 495 name-sign types. 78 signs for 80% sits in your 40 to 90 band; 209 for 95% does not. Names are a small core plus a large open set of word-signs.

## 1. Length, starters, enders, stand-alones

Name length: 1 sign: 391 (45%) ; 2 sign: 286 (33%) ; 3 sign: 155 (18%) ; 4 sign: 36 (4%) ; 5 sign: 7 (1%) ; 6 sign: 2 (0%). 552 different name segments on 877 seals.

Signs that start names of 2 or more signs (486 such names):

| sign | shape | seals |
|---|---|---|
| 235 | Fish with a caret shaped hat | 49 |
| 240 | Fish with extra whiskers on cheeks | 40 |
| 233 | Fish with a horizontal line throug | 32 |
| 590 | Square at bottom with vertical bar | 28 |
| 798 | Leaf with 'pincers' coming off the | 19 |
| 806 | Leaf with tree at bottom | 17 |
| 415 | Pitchfork with tines | 13 |
| 017 | Seven short vertical strokes | 11 |
| 140 | Person with round breasts and one  | 10 |
| 013 | Two small vertical strokes over on | 10 |
| 231 | Fish with a small vertical stroke  | 10 |
| 705 | U with a long vertical stroke inse | 9 |
| 176 | Person sitting with bent knees, fo | 8 |
| 255 | Unknown asymmetric animal? Perhaps | 8 |

Signs that end names of 2 or more signs:

| sign | shape | seals |
|---|---|---|
| 100 | Person with three heads | 42 |
| 760 | U with decorated branching at top | 39 |
| 390 | Simple tree with branches at the t | 29 |
| 923 | Right parenthesis drawn in outline | 16 |
| 220 | Fish with no other decoration | 15 |
| 585 | ? | 15 |
| 840 | Two vertical leaves, slightly over | 14 |
| 705 | U with a long vertical stroke inse | 12 |
| 176 | Person sitting with bent knees, fo | 10 |
| 550 | The 'pincer' motif. Right-pointing | 9 |
| 055 | Four small vertical strokes above  | 8 |
| 405 | Simple tree with branches at the t | 8 |
| 240 | Fish with extra whiskers on cheeks | 8 |
| 142 | Person with staff | 8 |

Signs that stand alone as a one-sign name (391 such names):

| sign | shape | seals |
|---|---|---|
| 220 | Fish with no other decoration | 19 |
| 176 | Person sitting with bent knees, fo | 17 |
| 142 | Person with staff | 15 |
| 061 | Simple lambda but reversed horizon | 14 |
| 233 | Fish with a horizontal line throug | 11 |
| 016 | Six short vertical strokes | 11 |
| 900 | Right parenthesis (perhaps with a  | 9 |
| 550 | The 'pincer' motif. Right-pointing | 9 |
| 803 | Leaf with tree at bottom | 7 |
| 235 | Fish with a caret shaped hat | 7 |
| 231 | Fish with a small vertical stroke  | 7 |
| 416 | Pitckfork with two stacked heads | 7 |
| 017 | Seven short vertical strokes | 7 |
| 240 | Fish with extra whiskers on cheeks | 7 |

Signs seen 8 or more times inside 2+ sign names that sit at one end at least 75% of the time (43 signs reach 8 uses; 20 are locked; only 13 are used both first and last at 20% or more each: 717, 460, 798, 255, 705, 070, 920, 220, 706, 615 and three more):

| sign | shape | in 2+ sign names | first | middle | last |
|---|---|---|---|---|---|
| 760 | U with decorated branching at top | 39 | 0 | 0 | 39 |
| 100 | Person with three heads | 42 | 0 | 0 | 42 |
| 923 | Right parenthesis drawn in outline | 16 | 0 | 0 | 16 |
| 585 | ? | 16 | 0 | 1 | 15 |
| 405 | Simple tree with branches at the t | 9 | 0 | 1 | 8 |
| 803 | Leaf with tree at bottom | 8 | 1 | 0 | 7 |
| 752 | U with decorated branching at top | 8 | 0 | 1 | 7 |
| 550 | The 'pincer' motif. Right-pointing | 11 | 1 | 1 | 9 |
| 142 | Person with staff | 10 | 1 | 1 | 8 |
| 220 | Fish with no other decoration | 19 | 4 | 0 | 15 |
| 390 | Simple tree with branches at the t | 37 | 2 | 6 | 29 |
| 690 | Two nested greater-than symbols, t | 9 | 1 | 1 | 7 |
| 555 | The 'pincer' motif. Right-pointing | 9 | 0 | 2 | 7 |
| 388 | Upside-down heart symbol with hori | 8 | 0 | 2 | 6 |
| 482 | Tall caret drawn in outline, with  | 8 | 1 | 1 | 6 |
| 798 | Leaf with 'pincers' coming off the | 25 | 19 | 0 | 6 |
| 806 | Leaf with tree at bottom | 22 | 17 | 2 | 3 |
| 140 | Person with round breasts and one  | 13 | 10 | 2 | 1 |
| 235 | Fish with a caret shaped hat | 61 | 49 | 10 | 2 |
| 013 | Two small vertical strokes over on | 10 | 10 | 0 | 0 |

Name-enders: 760 (a U with a decorated branching top) is last in 39 of 39 two-plus-sign names and 100 (the person with three heads) in 42 of 42; they carry 81 of 486 multi-sign names (17%). 760 is followed by the jar class in 40 of 43 seals; 100 by the jar in 33 of 44 and by the plain person in 7 (this person class is the largest seal size). 100 is preceded by the pitchfork 415 in 15 of 42, by the sitting person 176 in 6, by the person 140 in 5; 760 by 440 (5), 840 (4), 605, 705, 335 (3 each). So the pitchfork-plus-three-headed-person (415-100) acts as a unit (7 seals, all Mohenjo-daro) and the fish-pitchfork-person (240-415-100) as a longer one (4 seals).

Name-starters: the four fish signs 235 (fish with a caret hat), 240 (fish with whiskers), 233 (fish with a line through the body) and 231 (fish with a small stroke) start 131 of 486 multi-sign names (27%). 235 is first in 80% of its 61 uses inside multi-sign names, 233 64%, 240 51%. 798 (leaf with pincers) and 806 (leaf on a tree) start 76% and 77% of theirs; 140 (person with round breasts) 77%; 013 (two small strokes over one) 10 of 10; 590 (square with a bar on top) 62%.

## 2. The household element

### Shared sign inside Mohenjo-daro houses (area + block-house)

355 seals in 95 houses that have 2 or more seals. Chance = labels shuffled among seals of the same area and 3-ft depth band (2,000 shuffles).

| what is shared by two seals of one house | observed | chance | ratio | P |
|---|---|---|---|---|
| any name sign (whole segment) | 55 | 44.1 | 1.25 | 0.037 |
| the same sign, first in both multi-sign names | 17 | 10.8 | 1.57 | 0.020 |
| first in one, middle in the other | 7 | 4.4 | 1.58 | 0.075 |
| the same sign, last in both | 11 | 7.7 | 1.43 | 0.117 |
| first in one, last in the other | 4 | 4.9 | 0.81 | 0.78 |
| whole name identical | 3 | 2.6 | 1.18 | 0.48 |
| a one-sign name shares with the other seal | 12 | 10.2 | 1.17 | 0.31 |

Who-role signs only (157 seals): any shared who-sign 20 against 12.1 (1.65 times, P 0.004); the same who-sign first in both 3 against 1.2 (P 0.031); whole who-name identical 9 against 4.95 (P 0.015). With the two enders 100 and 760 removed from the segment: first-first 13 against 8.0 (P 0.025), last-last 5 against 3.2 (P 0.20). Rare signs only (name-slot count 40 or less): 19 against 14.6, positions too few to split (P 0.11). At room level (area + block-house + room, 139 seals in 55 rooms) 8 pairs share a sign against 6.3; too few pairs to place the sign.

Rate form (259 multi-sign names at Mohenjo-daro with a house, 140 houses, 282 same-house pairs): same first sign 17 against 11.8 (P 0.053); same last sign 11 against 8.2 (P 0.17). Fish test: pairs where both names start with a fish sign (231/233/235/240): 23 same-house pairs; the same fish in 15 (65%) against 36% by chance, P 0.003.

Answer: the household element is the first sign of the name. The last sign repeats in houses at a smaller excess (1.35 to 1.43 times) and carries the ender function. Where a house is known, the fish sign at the front is the house.

Houses that keep their front fish (seal, name):
- DKE Trench E: 235-240 (M-1738), 235-760 (M-47), 235-415-220 (M-323), 235-240 (M-865).
- DKG (S) 1I: 240-772, 240-636, 240-220-717 (240 in front on 3 seals; a 4th, M-358, has 240 last) and 415-220-717 (717 at the back on 2 seals).
- DKG First Street: 240-637, 240-415-100 (M-199), 415-100 (M-850): the pitchfork-person unit appears with and without the 240 front.
- DKG (N) 18: 233-804 and 233-877; DKG (S) 6I: 235-240-923 and 235-904; DKG (S) 7II: 240-495-615 and 240-415-100; DKE Trench EI: 240-055 and 240-415-220; DKG (S) 8A: 240-519-760 and 240; DKG (S) 4: 140-746-142, 140-390-061 and 140.

### Names across cities

111 of the 552 distinct name segments occur on 2 or more seals; 76 on 2 or more sites; 27 multi-sign segments on 2 or more sites; 17 multi-sign segments on 3 or more seals. The 3-plus list (54 segments, 319 of 871 seals) with sites and the number of houses (Mohenjo-daro / Harappa excavation houses only):

| seals | name segment | shapes | sites (seals) | houses with a seal of it |
|---|---|---|---|---|
| 19 | 220 | Fish with no other d | id 19, obj 19, cisi 19, hmm 18, vmm 18, reading 16, room 11, depth 11, symbol 10, area 9, bh 9, roles 9, n 6, cls 5, opener 5, cls_last 5, site 4, first 3, material 3, name 3, pos 3, last 3, region 2, contiguous 2, nwho 2, tight 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 8 |
| 17 | 176 | Person sitting with  | id 17, obj 17, cisi 16, depth 15, vmm 14, reading 14, area 13, hmm 13, room 12, roles 11, bh 10, symbol 10, cls 8, cls_last 8, site 4, first 4, n 4, name 4, last 4, pos 4, opener 4, segroles 3, region 3, nwho 3, house 3, material 2, contiguous 2, tight 1, seg 1, seglen 1, has_class 1 | 9 |
| 15 | 142 | Person with staff | id 15, obj 15, hmm 14, vmm 13, cisi 12, area 12, depth 11, reading 11, bh 9, roles 8, symbol 6, room 5, site 5, opener 5, region 4, n 4, cls 4, pos 4, cls_last 4, material 2, last 2, contiguous 2, nwho 2, segroles 2, first 2, name 2, house 2, tight 1, seg 1, seglen 1, has_class 1 | 8 |
| 14 | 061 | Simple lambda but re | id 14, obj 14, cisi 14, hmm 11, depth 11, area 10, vmm 10, bh 9, room 8, reading 7, symbol 7, site 5, roles 4, opener 4, region 3, n 3, cls 3, cls_last 3, material 2, name 1, nwho 1, tight 1, contiguous 1, first 1, last 1, pos 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 8 |
| 14 | 590-390 | Square at bottom wit + Simple tree with bra | id 14, obj 14, vmm 14, hmm 14, reading 13, cisi 13, roles 12, depth 11, room 9, symbol 9, bh 8, site 6, area 6, cls 5, name 5, cls_last 5, n 5, last 5, first 5, pos 5, opener 5, region 4, material 3, segroles 3, house 2, contiguous 2, nwho 2, tight 1, seg 1, seglen 1, has_class 1 | 7 |
| 11 | 016 | Six short vertical s | id 11, obj 11, hmm 10, bh 9, cisi 9, vmm 9, area 8, depth 8, room 7, symbol 6, reading 5, site 3, region 3, material 3, roles 3, cls 3, cls_last 3, opener 3, n 2, name 1, nwho 1, tight 1, contiguous 1, first 1, last 1, pos 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 8 |
| 11 | 233 | Fish with a horizont | id 11, obj 11, cisi 11, area 10, depth 10, roles 9, reading 9, hmm 9, room 8, vmm 8, symbol 7, opener 6, pos 6, bh 5, name 5, first 5, last 4, site 4, n 4, material 3, region 3, cls 3, nwho 3, cls_last 3, contiguous 2, segroles 2, house 2, tight 1, seg 1, seglen 1, has_class 1 | 4 |
| 9 | 550 | The 'pincer' motif.  | id 9, obj 9, cisi 9, depth 9, area 7, reading 6, vmm 6, hmm 6, room 5, symbol 5, bh 4, roles 4, n 4, cls_last 4, cls 4, region 3, site 3, material 2, opener 2, name 1, nwho 1, tight 1, contiguous 1, first 1, last 1, pos 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 3 |
| 9 | 900 | Right parenthesis (p | id 9, obj 9, cisi 9, symbol 8, area 7, hmm 7, vmm 7, reading 6, roles 6, depth 6, room 5, bh 4, n 4, site 3, region 2, material 2, opener 2, tight 1, contiguous 1, first 1, last 1, nwho 1, name 1, cls_last 1, cls 1, pos 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 3 |
| 7 | 017 | Seven short vertical | id 7, obj 7, cisi 7, area 7, reading 7, vmm 7, symbol 6, hmm 6, cls 6, cls_last 6, room 5, roles 5, depth 5, bh 4, n 4, site 3, opener 3, material 2, region 2, last 2, name 2, contiguous 2, nwho 2, pos 2, first 2, tight 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 3 |
| 7 | 231 | Fish with a small ve | id 7, obj 7, cisi 7, reading 7, room 7, area 6, hmm 6, vmm 6, depth 6, roles 5, symbol 5, site 4, bh 4, n 4, cls 3, opener 3, cls_last 3, material 2, region 2, last 2, name 2, contiguous 2, nwho 2, segroles 2, first 2, pos 2, house 2, tight 1, seg 1, seglen 1, has_class 1 | 3 |
| 7 | 235 | Fish with a caret sh | id 7, obj 7, depth 7, hmm 7, vmm 7, reading 7, cisi 6, roles 6, bh 6, area 6, cls 6, cls_last 6, room 5, symbol 5, pos 4, opener 4, first 3, site 3, n 3, name 3, last 3, material 2, region 2, segroles 2, nwho 2, contiguous 2, house 2, tight 1, seg 1, seglen 1, has_class 1 | 5 |
| 7 | 240 | Fish with extra whis | id 7, obj 7, cisi 7, hmm 7, vmm 7, depth 7, room 7, reading 5, roles 5, area 5, bh 5, opener 4, last 4, first 4, name 4, n 4, segroles 3, site 3, symbol 3, pos 3, cls 3, cls_last 3, region 2, contiguous 2, house 2, nwho 2, material 1, tight 1, seg 1, seglen 1, has_class 1 | 4 |
| 7 | 415-100 | Pitchfork with tines + Person with three he | id 7, obj 7, cisi 7, vmm 7, depth 7, bh 6, hmm 6, reading 6, symbol 6, area 5, room 5, opener 5, roles 4, n 4, material 2, segroles 2, cls_last 2, contiguous 2, nwho 2, cls 2, last 2, name 2, first 2, pos 2, house 2, region 1, site 1, tight 1, seg 1, seglen 1, has_class 1 | 5 |
| 7 | 416 | Pitckfork with two s | id 7, obj 7, cisi 7, depth 7, bh 6, symbol 6, area 6, vmm 6, hmm 6, reading 4, room 4, site 3, region 3, roles 3, n 3, opener 3, cls 2, cls_last 2, material 1, name 1, nwho 1, tight 1, contiguous 1, first 1, last 1, pos 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 5 |
| 7 | 803 | Leaf with tree at bo | id 7, obj 7, cisi 7, hmm 6, vmm 6, depth 6, room 6, reading 5, symbol 5, area 5, bh 5, site 3, region 3, roles 3, cls 3, n 3, cls_last 3, material 2, contiguous 2, last 2, name 2, first 2, nwho 2, pos 2, opener 2, tight 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 4 |
| 6 | 097 | Person with two arms | id 6, obj 6, cisi 6, hmm 6, vmm 6, depth 6, bh 5, reading 5, symbol 5, area 4, room 4, roles 3, n 3, cls_last 3, cls 3, region 2, site 2, opener 2, material 1, name 1, nwho 1, tight 1, contiguous 1, first 1, last 1, pos 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 4 |
| 6 | 390 | Simple tree with bra | id 6, obj 6, cisi 6, roles 6, hmm 6, reading 6, room 5, vmm 5, cls 5, cls_last 5, depth 4, n 4, name 4, symbol 4, bh 4, pos 3, house 3, opener 3, area 3, last 3, first 3, nwho 3, site 2, segroles 2, material 2, contiguous 2, region 1, tight 1, seg 1, seglen 1, has_class 1 | 3 |
| 6 | 460 | Three tall, thin iso | id 6, obj 6, cisi 6, area 6, vmm 6, hmm 6, depth 6, reading 5, roles 5, symbol 5, bh 4, room 4, region 3, site 3, n 3, opener 3, cls 2, cls_last 2, material 1, name 1, nwho 1, tight 1, contiguous 1, first 1, last 1, pos 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 3 |
| 6 | 705 | U with a long vertic | id 6, obj 6, cisi 6, bh 6, vmm 6, depth 6, room 6, hmm 6, reading 5, roles 5, symbol 5, n 5, area 4, cls 3, segroles 3, cls_last 3, pos 2, opener 2, first 2, last 2, name 2, contiguous 2, nwho 2, house 2, material 1, region 1, site 1, tight 1, seg 1, seglen 1, has_class 1 | 6 |
| 6 | 706 | U with a long vertic | id 6, obj 6, cisi 6, area 6, vmm 6, hmm 6, depth 6, reading 5, symbol 5, roles 5, room 5, opener 4, n 4, bh 3, region 3, site 3, material 2, contiguous 2, nwho 2, last 2, pos 2, name 2, first 2, cls_last 1, cls 1, tight 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 2 |
| 6 | 840 | Two vertical leaves, | id 6, obj 6, roles 6, hmm 6, vmm 6, reading 6, symbol 6, cisi 5, bh 5, area 5, site 4, depth 4, n 4, room 3, region 3, segroles 3, opener 3, material 2, contiguous 2, cls 2, nwho 2, name 2, first 2, pos 2, cls_last 2, last 2, house 2, tight 1, seg 1, seglen 1, has_class 1 | 4 |
| 5 | 013-840 | Two small vertical s + Two vertical leaves, | id 5, obj 5, cisi 5, area 5, symbol 4, depth 4, room 4, vmm 4, hmm 4, site 3, region 3, bh 2, material 2, reading 2, roles 2, pos 2, n 2, opener 2, tight 1, first 1, contiguous 1, nwho 1, name 1, cls_last 1, cls 1, last 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 1 |
| 5 | 017-585 | Seven short vertical + ? | id 5, obj 5, cisi 5, bh 5, symbol 5, depth 5, room 5, reading 5, vmm 5, hmm 5, roles 4, area 3, n 3, opener 3, contiguous 2, segroles 2, house 2, name 2, nwho 2, last 2, pos 2, first 2, region 1, material 1, site 1, tight 1, cls 1, cls_last 1, seg 1, seglen 1, has_class 1 | 5 |
| 5 | 055 | Four small vertical  | id 5, obj 5, cisi 5, area 5, symbol 5, reading 5, hmm 4, vmm 4, roles 4, depth 4, cls_last 4, first 4, last 4, cls 4, name 4, pos 4, n 3, bh 3, room 3, site 3, nwho 3, opener 3, region 2, material 2, contiguous 2, tight 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 2 |
| 5 | 140 | Person with round br | id 5, obj 5, cisi 5, hmm 5, reading 5, cls_last 5, cls 5, vmm 4, symbol 4, roles 4, depth 4, bh 4, room 4, area 3, n 3, material 2, site 2, region 2, contiguous 2, last 2, name 2, first 2, nwho 2, segroles 2, opener 2, pos 2, house 2, tight 1, seg 1, seglen 1, has_class 1 | 3 |
| 5 | 255-435-690 | Unknown asymmetric a + Vertical line with d + Two nested greater-t | id 5, obj 5, cisi 5, hmm 5, vmm 5, depth 5, room 5, reading 4, symbol 4, area 4, bh 4, opener 4, roles 3, pos 3, n 3, name 2, site 2, region 2, contiguous 2, first 2, nwho 2, material 1, tight 1, cls_last 1, cls 1, last 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 3 |
| 4 | 140-100 | Person with round br + Person with three he | id 4, obj 4, cisi 4, hmm 4, vmm 4, depth 4, room 4, symbol 3, bh 3, area 3, region 2, site 2, reading 2, roles 2, contiguous 2, n 2, nwho 2, name 2, first 2, cls 2, last 2, cls_last 2, house 2, segroles 2, pos 2, material 1, tight 1, seg 1, opener 1, seglen 1, has_class 1 | 2 |
| 4 | 233-176 | Fish with a horizont + Person sitting with  | id 4, obj 4, cisi 4, area 4, vmm 4, hmm 4, site 3, reading 3, region 3, room 3, symbol 3, roles 3, pos 3, material 2, bh 2, depth 2, name 2, cls 2, nwho 2, cls_last 2, n 2, house 2, last 2, segroles 2, first 1, contiguous 1, tight 1, seg 1, opener 1, seglen 1, has_class 1 | 1 |
| 4 | 240-233 | Fish with extra whis + Fish with a horizont | id 4, obj 4, cisi 4, area 4, vmm 4, reading 4, depth 4, roles 4, hmm 4, bh 3, room 3, opener 3, n 3, site 2, region 2, segroles 2, symbol 2, contiguous 2, nwho 2, cls 2, last 2, name 2, first 2, pos 2, cls_last 2, house 2, material 1, tight 1, seg 1, seglen 1, has_class 1 | 2 |
| 4 | 240-415-100 | Fish with extra whis + Pitchfork with tines + Person with three he | id 4, obj 4, cisi 4, hmm 4, vmm 4, reading 4, depth 4, room 3, roles 3, area 3, bh 3, opener 3, site 2, material 2, region 2, symbol 2, name 2, cls 2, nwho 2, cls_last 2, pos 2, house 2, last 2, n 2, segroles 2, contiguous 1, tight 1, first 1, seg 1, seglen 1, has_class 1 | 2 |
| 4 | 388 | Upside-down heart sy | id 4, obj 4, cisi 4, hmm 4, vmm 4, reading 4, symbol 4, room 3, depth 3, roles 3, area 3, n 3, bh 2, site 2, region 2, material 2, cls 2, opener 2, cls_last 2, name 1, nwho 1, tight 1, contiguous 1, first 1, last 1, pos 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 1 |
| 4 | 531 | X with left points c | id 4, obj 4, cisi 4, site 4, area 4, depth 4, room 4, vmm 4, hmm 4, symbol 4, reading 3, roles 3, n 3, bh 2, region 2, segroles 2, contiguous 2, name 2, nwho 2, cls 2, last 2, cls_last 2, first 2, pos 2, opener 2, house 2, material 1, tight 1, seg 1, seglen 1, has_class 1 | 1 |
| 4 | 590-405 | Square at bottom wit + Simple tree with bra | id 4, obj 4, cisi 4, area 4, vmm 4, reading 4, depth 4, roles 4, hmm 4, site 3, n 3, opener 3, last 3, first 3, name 3, symbol 2, room 2, material 2, bh 2, region 2, nwho 2, cls 2, contiguous 2, segroles 2, cls_last 2, pos 2, tight 1, seg 1, house 1, seglen 1, has_class 1 | 1 |
| 4 | 690 | Two nested greater-t | id 4, obj 4, cisi 4, area 4, vmm 4, depth 4, room 4, hmm 4, reading 3, site 3, bh 3, roles 3, symbol 3, n 3, region 2, material 2, cls 2, opener 2, cls_last 2, name 1, nwho 1, tight 1, contiguous 1, first 1, last 1, pos 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 2 |
| 4 | 760 | U with decorated bra | id 4, obj 4, cisi 4, area 4, vmm 4, reading 4, symbol 4, roles 4, hmm 4, n 4, bh 3, depth 3, room 3, opener 3, site 2, last 2, material 2, contiguous 2, nwho 2, name 2, pos 2, first 2, region 1, cls_last 1, cls 1, tight 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 2 |
| 3 | 017-575 | Seven short vertical + Trapezoid with no bo | id 3, obj 3, cisi 3, area 3, vmm 3, symbol 3, depth 3, reading 3, roles 3, hmm 3, n 3, opener 3, region 2, bh 2, site 2, room 2, material 2, cls 2, cls_last 2, house 2, segroles 2, tight 1, contiguous 1, first 1, last 1, nwho 1, name 1, seg 1, pos 1, seglen 1, has_class 1 | 1 |
| 3 | 171 | Capital 'T' with a s | id 3, obj 3, cisi 3, bh 3, symbol 3, depth 3, room 3, vmm 3, hmm 3, site 2, region 2, area 2, reading 2, roles 2, cls 2, n 2, cls_last 2, material 1, tight 1, name 1, nwho 1, last 1, contiguous 1, first 1, opener 1, pos 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 2 |
| 3 | 231-705 | Fish with a small ve + U with a long vertic | id 3, obj 3, cisi 3, bh 3, area 3, symbol 3, depth 3, reading 3, roles 3, vmm 3, hmm 3, opener 3, material 2, pos 2, room 2, n 2, site 1, region 1, tight 1, first 1, contiguous 1, nwho 1, name 1, cls_last 1, cls 1, last 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 2 |
| 3 | 235-240 | Fish with a caret sh + Fish with extra whis | id 3, obj 3, cisi 3, hmm 3, symbol 3, depth 3, room 3, reading 3, vmm 3, roles 3, cls 3, opener 3, n 3, cls_last 3, site 2, house 2, region 2, area 2, bh 2, segroles 2, pos 2, material 1, tight 1, first 1, last 1, nwho 1, name 1, contiguous 1, seg 1, seglen 1, has_class 1 | 1 |
| 3 | 235-482 | Fish with a caret sh + Tall caret drawn in  | id 3, obj 3, cisi 3, site 3, area 3, depth 3, room 3, vmm 3, hmm 3, symbol 3, region 2, bh 2, material 1, reading 1, roles 1, tight 1, contiguous 1, nwho 1, name 1, first 1, last 1, cls 1, cls_last 1, opener 1, house 1, pos 1, seg 1, seglen 1, segroles 1, has_class 1, n 1 | 1 |
| 3 | 384 | Upside-down heart sy | id 3, obj 3, cisi 3, area 3, symbol 3, depth 3, room 3, reading 3, vmm 3, roles 3, hmm 3, opener 3, n 3, bh 2, region 2, material 2, site 2, tight 1, contiguous 1, first 1, last 1, nwho 1, name 1, cls_last 1, cls 1, pos 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 1 |
| 3 | 415-220 | Pitchfork with tines + Fish with no other d | id 3, obj 3, cisi 3, area 3, symbol 3, depth 3, room 3, reading 3, vmm 3, hmm 3, opener 3, bh 2, region 2, roles 2, site 2, n 2, material 1, tight 1, contiguous 1, first 1, last 1, nwho 1, name 1, cls_last 1, cls 1, pos 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 1 |
| 3 | 484-337 | Tall caret drawn in  + M with the bottom of | id 3, obj 3, cisi 3, bh 3, area 3, depth 3, room 3, reading 3, vmm 3, symbol 3, hmm 3, roles 3, pos 3, opener 3, region 2, name 2, site 2, contiguous 2, nwho 2, first 2, n 2, material 1, tight 1, cls_last 1, cls 1, last 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 2 |
| 3 | 519 | ? | id 3, obj 3, cisi 3, bh 3, symbol 3, depth 3, room 3, vmm 3, hmm 3, roles 2, reading 2, opener 2, n 2, area 1, region 1, material 1, site 1, tight 1, contiguous 1, first 1, last 1, nwho 1, name 1, cls_last 1, cls 1, pos 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 3 |
| 3 | 590 | Square at bottom wit | id 3, obj 3, cisi 3, bh 3, area 3, reading 3, depth 3, roles 3, hmm 3, vmm 3, name 3, last 3, house 3, site 2, region 2, n 2, symbol 2, room 2, cls 2, cls_last 2, material 1, nwho 1, contiguous 1, first 1, tight 1, pos 1, opener 1, seg 1, seglen 1, segroles 1, has_class 1 | 2 |
| 3 | 615 | A grid of x by y cel | id 3, obj 3, cisi 3, bh 3, area 3, depth 3, room 3, reading 3, vmm 3, symbol 3, hmm 3, site 2, region 2, roles 2, cls 2, n 2, cls_last 2, opener 2, material 1, name 1, nwho 1, tight 1, contiguous 1, first 1, last 1, pos 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 2 |
| 3 | 705-255 | U with a long vertic + Unknown asymmetric a | id 3, obj 3, cisi 3, bh 3, area 3, depth 3, room 3, reading 3, roles 3, vmm 3, hmm 3, pos 3, n 3, symbol 2, name 2, segroles 2, opener 2, cls 2, nwho 2, cls_last 2, house 2, last 2, region 1, material 1, site 1, contiguous 1, tight 1, first 1, seg 1, seglen 1, has_class 1 | 3 |
| 3 | 798 | Leaf with 'pincers'  | id 3, obj 3, cisi 3, bh 3, area 3, reading 3, symbol 3, roles 3, hmm 3, vmm 3, opener 3, site 2, material 2, room 2, region 2, depth 2, contiguous 2, name 2, nwho 2, cls 2, last 2, cls_last 2, first 2, n 2, house 2, pos 2, segroles 2, tight 1, seg 1, seglen 1, has_class 1 | 2 |
| 3 | 806 | Leaf with tree at bo | id 3, obj 3, cisi 3, area 3, reading 3, roles 3, depth 3, hmm 3, n 3, pos 3, cls_last 3, first 3, last 3, cls 3, name 3, segroles 2, nwho 2, material 2, vmm 2, region 2, site 2, room 2, contiguous 2, house 2, bh 1, symbol 1, tight 1, seg 1, opener 1, seglen 1, has_class 1 | 0 |
| 3 | 877 | Diamond with four sm | id 3, obj 3, cisi 3, area 3, symbol 3, depth 3, room 3, reading 3, vmm 3, hmm 3, material 2, roles 2, n 2, cls_last 2, cls 2, region 1, site 1, bh 1, tight 1, name 1, nwho 1, last 1, contiguous 1, first 1, opener 1, pos 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 0 |
| 3 | 910 | ? | id 3, obj 3, cisi 3, hmm 3, vmm 3, symbol 3, site 2, bh 2, area 2, region 2, room 2, material 2, depth 2, reading 1, roles 1, tight 1, contiguous 1, nwho 1, name 1, first 1, last 1, cls 1, cls_last 1, opener 1, house 1, pos 1, seg 1, seglen 1, segroles 1, has_class 1, n 1 | 1 |
| 3 | 923 | Right parenthesis dr | id 3, obj 3, cisi 3, bh 3, area 3, depth 3, room 3, vmm 3, hmm 3, symbol 3, region 2, site 2, reading 2, roles 2, cls 2, n 2, cls_last 2, house 2, material 1, name 1, nwho 1, tight 1, contiguous 1, first 1, last 1, pos 1, opener 1, seg 1, seglen 1, segroles 1, has_class 1 | 2 |
| 3 | 927 | Two slightly nested  | id 3, obj 3, cisi 3, bh 3, symbol 3, depth 3, room 3, reading 3, vmm 3, roles 3, hmm 3, opener 3, n 3, area 1, region 1, material 1, site 1, tight 1, contiguous 1, first 1, last 1, nwho 1, name 1, cls_last 1, cls 1, pos 1, house 1, seg 1, seglen 1, segroles 1, has_class 1 | 3 |

Reading it: single signs (220 fish, 176 sitting person, 142 person with staff, 061, 016, 233, 550, 900) are the commonest whole names on 9 to 19 seals each across 3 to 5 sites, so they are common names (or common house names), not one person. The two-sign `590-390` is on 14 seals at 6 sites including Allahdino, Chanhu-daro, Dholavira, Harappa and a Kish seal in Mesopotamia; `013-840` (5 seals) sits in Harappa, Lothal and Mohenjo-daro, three of the Mohenjo-daro seals in one house (HRB 2XII); `233-176` (4 seals) is Kalibangan, Lothal and Mohenjo-daro. `415-100` (7 seals) and `017-585` (5) are only at Mohenjo-daro; `140-100` is Harappa 2, Mohenjo-daro 2. Same whole name in different cities is therefore a feature of common names and a few fixed pairs, not rare.

## 3. Name families (names that share all but one sign)

114 families with 2 or more different fillers in the open slot; 49 with 3 or more; 30 with 4 or more. By slot: length 2 first-slot open 40, last-slot open 36; length 3 first open 14, last open 13, middle open 7. 23 different first signs begin names with 4 or more different continuations (235: 40 different continuations, 240: 31, 233: 26, 798: 19, 806: 16, 590: 12); 35 different last signs close names with 4 or more different lead-ins (760: 34, 100: 28, 923: 15, 390: 13, 220: 12, 585: 11). Fillers in brackets are seal counts. The 30 largest:

| # | frame | frame in words | fillers (seals) | n fillers | n seals |
|---|---|---|---|---|---|
| 1 | 240-* | Fish with extra whiskers + _ | 233(4), 100(2), 643(2), 772(2), 440(1), 806(1), 637(1), 055(1), 220(1), 550(1), 636(1), 176(1), 812(1), 717(1) ... | 21 | 27 |
| 2 | 235-* | Fish with a caret shaped + _ | 482(3), 240(3), 555(2), 550(2), 798(2), 840(2), 380(1), 504(1), 770(1), 388(1), 803(1), 760(1), 231(1), 904(1) ... | 17 | 25 |
| 3 | 233-* | Fish with a horizontal l + _ | 176(4), 840(2), 803(2), 760(2), 706(1), 717(1), 804(1), 388(1), 877(1), 879(1), 100(1), 923(1), 705(1), 335(1) ... | 15 | 21 |
| 4 | *-760 | _ + U with decorated branchi | 440(2), 605(2), 335(2), 233(2), 220(1), 615(1), 049(1), 019(1), 840(1), 235(1), 705(1), 742(1), 315(1), 017(1) | 14 | 18 |
| 5 | *-100 | _ + Person with three heads | 415(7), 140(4), 240(2), 176(2), 717(1), 220(1), 440(1), 798(1), 165(1), 233(1), 456(1), 235(1) | 12 | 23 |
| 6 | *-923 | _ + Right parenthesis drawn  | 220(2), 838(1), 806(1), 705(1), 803(1), 233(1), 240(1), 226(1), 013(1) | 9 | 10 |
| 7 | *-390 | _ + Simple tree with branche | 590(14), 125(2), 844(2), 072(1), 531(1), 692(1), 707(1) | 7 | 22 |
| 8 | *-705 | _ + U with a long vertical s | 231(3), 172(1), 415(1), 055(1), 176(1), 240(1), 233(1) | 7 | 9 |
| 9 | 231-* | Fish with a small vertic + _ | 705(3), 555(1), 798(1), 803(1), 440(1), 927(1), 585(1) | 7 | 9 |
| 10 | 235-240-* | Fish with a caret shaped + Fish with extra whiskers + _ | 455(2), 904(1), 923(1), 055(1), 773(1), 220(1) | 6 | 7 |
| 11 | *-142 | _ + Person with staff | 880(1), 368(1), 384(1), 013(1), 066(1), 240(1) | 6 | 6 |
| 12 | *-840 | _ + Two vertical leaves, sli | 013(5), 233(2), 235(2), 830(1), 768(1) | 5 | 11 |
| 13 | 806-* | Leaf with tree at bottom + _ | 055(1), 923(1), 235(1), 706(1), 240(1) | 5 | 5 |
| 14 | 590-* | Square at bottom with ve + _ | 390(14), 405(4), 406(1), 407(1) | 4 | 20 |
| 15 | 415-* | Pitchfork with tines + _ | 100(7), 220(3), 705(1), 717(1) | 4 | 12 |
| 16 | 017-* | Seven short vertical str + _ | 585(5), 575(3), 590(1), 760(1) | 4 | 10 |
| 17 | 013-* | Two small vertical strok + _ | 840(5), 142(1), 923(1), 016(1) | 4 | 8 |
| 18 | *-585 | _ + ? | 017(5), 798(1), 240(1), 231(1) | 4 | 8 |
| 19 | *-220 | _ + Fish with no other decor | 415(3), 368(1), 240(1), 428(1) | 4 | 6 |
| 20 | *-920 | _ + Right parenthesis with s | 322(2), 323(2), 320(1), 140(1) | 4 | 6 |
| 21 | 705-* | U with a long vertical s + _ | 255(3), 923(1), 760(1), 482(1) | 4 | 6 |
| 22 | *-460 | _ + Three tall, thin isocele | 510(2), 495(1), 615(1), 880(1) | 4 | 5 |
| 23 | 176-* | Person sitting with bent + _ | 100(2), 705(1), 337(1), 455(1) | 4 | 5 |
| 24 | *-415-220 | _ + Pitchfork with tines + Fish with no other decor | 519(2), 240(1), 235(1), 798(1) | 4 | 5 |
| 25 | *-550 | _ + The 'pincer' motif. Righ | 235(2), 240(1), 467(1), 452(1) | 4 | 5 |
| 26 | *-798 | _ + Leaf with 'pincers' comi | 235(2), 231(1), 255(1), 706(1) | 4 | 5 |
| 27 | *-055 | _ + Four small vertical stro | 806(1), 240(1), 798(1), 407(1) | 4 | 4 |
| 28 | *-904 | _ + Two slightly nested righ | 741(1), 142(1), 235(1), 690(1) | 4 | 4 |
| 29 | *-590 | _ + Square at bottom with ve | 017(1), 390(1), 575(1), 455(1) | 4 | 4 |
| 30 | 368-* | Vertical stroke with a t + _ | 480(1), 220(1), 142(1), 235(1) | 4 | 4 |

Reading it: the biggest families are a fish front with an open second slot (240-_ 21 fillers, 235-_ 17, 233-_ 15, 231-_ 7) and an open front with a fixed ender (_-760 14, _-100 12, _-923 9, _-390 7, _-705 7). Both ends are slots with a short fixed list, and the middle is where the open class lives. The fixed fish front takes any ender and any personal element; the fixed ender takes any front.

## 4. What names go with

| name part against | statistic | P (label shuffle) |
|---|---|---|
| first sign vs animal on the seal (top-25 signs) | V 0.208 | 0.0035 |
| first sign vs opener type (diamond+strokes / wheel / 060 cap / none) | V 0.205 | 0.0085 |
| first sign vs class sign | V 0.263 | 0.0005 |
| last sign vs animal | V 0.173 | 0.34 (not linked) |
| last sign vs opener type | V 0.178 | 0.24 (not linked) |
| last sign vs class sign | V 0.375 | 0.0005 |

Strongest sign-level links. With the class: 220 (plain fish) in the spear-class 24 of 38 seals against 4.4 expected; 016 (six strokes) with the tree class 390 in 12 of 15 against 0.9; 550 (pincers) with class 527 in 11 of 20 against 0.6; 760 with the jar in 40 of 43 against 21; 706 and 705 (the U with an inserted stroke) with the spear class 11 of 20 and 15 of 43. With the animal: 806 (leaf on a tree) in names on seals with no animal in 16 of 25 against 4.9 (this is the crop word of the load-tag phrase), 390 in seals with a bull 38 of 43 against 28, 741 (jar with handles) with the gaur 5 of 23 against 1.0. With the opener: 231 with the `060` cap opener 8 of 28 against 3.0; 760 with the diamond opener 14 of 43 against 8.0; 233 with the diamond 18 of 61 against 11.3. The parser fixed 760 and 100 as second-from-last by position, so their link to the jar is partly built in; the other pairs (220-spear, 016-tree, 550-527) are not.

Answer: the name has two halves. The front half goes with the animal and the opener (the group the seal belongs to). The back half goes with the class sign (rank/office). That is the same two-tier build as the household/personal split.

### Seals found abroad

41 objects in the Persian Gulf, Mesopotamia, Iranian Plateau and Central Asia: 33 seals (14 square, 18 round or cylinder). Only 8 have a parsed class plus name segment, all square seals or one round (Altyn Depe 415, Kish 590-390, Nindowari 026-760 and 255-798, Gonur Depe 285-235-125-590-390, Miri Qalat 742 and 013, Qala'at al-Bahrain 055). Their 15 name-sign fillings: 13 are signs that are common name signs at home (10 or more uses), and 026 never appears in a home name slot. So the square seals found abroad carry ordinary home names.

The round seals are a different template. Man signs: 091 (two persons side by side) is on 5 abroad objects and is the first sign of the text in 4 of them (home: 10 seals, first 7); 090 (the plain person) is the CLASS sign at home (last in 65 of 86 seals) but on 7 abroad objects it is last in only 1 and first or second in 4 (090-000-817-317, 090-405, 350-090-004-000-000, 000-090-000-001-000). 12 of the 18 round or cylinder seals carry 090 or 091; the man sign moves to the front and acts as an opener there, followed by the name signs (091-840-413-831, 091-031-455-220, 090-405).

Signs over-used on abroad seals (any slot; abroad 33 seals, home 2,257): 091 in 5 of 33 against 10 of 2,257 (P 1e-6); 090 21% against 4.0% (P 4e-4); 055 (four strokes over the same base) 12% against 1.6% (P 2e-3); 001 18% against 6.2%; 004 9% against 1.9%; the jar 740 under-used 18% against 41% (P 0.007). Signs on abroad seals never seen at home: 716, 026, 340. 055 is also a name-final sign at home (8 of 16 uses last in a name), so the Gulf seals lean on one home name element.

## 5. How many signs carry the load

Cover counts (sign types needed to reach the share of all fillings):

| slot | fillings | types | 50% | 80% | 95% | seen once |
|---|---|---|---|---|---|---|
| name slot, all name-segment signs | 1,619 | 289 | 23 | 78 | 209 | 136 (47%) |
| name slot, distinct texts only | 1,532 | 289 | 23 | 80 | 213 | 139 |
| who-role signs only | 581 | 177 | 17 | 70 | 148 | 99 (56%) |
| first sign of name | 877 | 231 | 22 | 84 | 188 | 119 |
| last sign of name | 877 | 207 | 22 | 68 | 164 | 104 |
| class slot, same seals | 851 | 24 | 1 | 6 | 14 | 2 (8%) |
| class slot, all clean seals with a class | 1,194 | 26 | 2 | 7 | 16 | 3 |
| name slot drawn down to 851 fillings | 851 | 210.7 | 22.2 | 72.9 | 168.7 | - |
| every sign in clean seal texts (context) | 6,799 | 511 | 21 | 75 | 246 | 193 |

Rarefaction of name signs: 61 types in 100 fillings, 95 in 200, 141 in 400, 204 in 800, 250 in 1,200, 289 in 1,619. No plateau. Chao1 estimate 495 name-sign types (136 seen once, 45 seen twice). The chance that the next name sign is one never seen before is 0.08 (all positions) and 0.17 (who-role only).

Reading: the class slot is a closed set of about 24 to 26 signs, as before. The name slot is not closed. 80% of fillings come from 78 signs, which is in the syllable-set range, but the last 15% needs another 131 signs and half the sign types occur once. A sound-spelled name would reuse a closed set of 40 to 90 signs for nearly everything; here 209 signs are needed for 95% and the estimated inventory is near 500. Names are a layer of about 25 position-locked signs (the 10 front signs and 15 end signs) around an open personal layer of word-signs. The core is where sounds can be pinned first, because it repeats: the fish front, 760 and 100.

## 6. The bold account

An Indus name is FRONT + SELF + TAG.

- FRONT is the household or lineage emblem. It is the first sign, drawn from about 10 signs, and in houses where we can see it, it is the same sign on every seal of the house. Four fish signs (235, 240, 233, 231) are the main series: they open 27% of multi-sign names and each Mohenjo-daro house keeps one (15 of 23 same-fish pairs). The fish is the household name the way a surname is, and the four fish are four sorts of fish-kin; 798, 806, 140, 013, 590 and 017 are other emblems of the same kind. The front goes with the animal on the seal and with the opener type, so the emblem sits inside a bigger group (the animal) and the opener tells the sort of owner.
- SELF is the personal element, one or two signs from an open set of about 500 word-signs; 47% of the sign types we see occur once. Common ones: 415 (pitchfork), 220 (plain fish), 176 (seated person), 705 and 706 (the U with an inserted stroke), 240 inside a longer name (a second fish), 840, 923. A one-sign name (45% of names) is a lone sign: of 391, 54 are one of the 10 front signs, 76 are one of the 15 end signs (220 and 142 stand alone often, 19 and 15 seals), and the other 261 are open-class signs (176, 061, 016, 900 are the commonest).
- TAG is the closing particle, a word like "son of", "of the house", or a status/title word. 760 and 100 are always last (39 of 39 and 42 of 42), 923, 585, 390, 405, 550, 142, 220 are last at 78% to 100%. The TAG agrees with the class sign (760 with the jar 40 of 43; 220 with the spear 24 of 38; 016 with the tree 12 of 15; 550 with 527 11 of 20), so TAG + class reads as one phrase, "[tag-word] of [class]", e.g. "house-of / jar".
- The full seal: [opener: sort of owner] [FRONT: emblem of the house] [SELF: person] [TAG + class: tie and rank].
- Seals abroad: square seals use the same names (13 of 15 name signs are ordinary home name signs); round seals put the man sign 090 or 091 first and the name after it: the foreign merchant's seal opens with "man" and spells a name.

What this predicts: (a) in a dated house sequence, the front sign stays and the self element changes (generations); (b) any new seal from a known house starts with that house's front; (c) names with the same SELF but different FRONT are people of one name in different houses. (d) Sounds: names of Meluhha recorded in Mesopotamian texts are the check set for the 2-sign names on the Kish, Susa, Ur and Gonur seals; the fish front should be a short word shared by the whole fish series (a fish-word clan label, Proto-Dravidian *mīn "fish" is the first candidate to run among the languages in the plan), with the TAG signs 760 and 100 as the suffix list.

### 25 seals, sign by sign

All Mohenjo-daro. House = area + block-house of the excavation record; depth in feet; animal = column symbol. HOUSEHOLD marks the front sign (22 of these 25 sit in a house where another seal of the excavation record shares that sign); SELF is written PERSONAL; ENDER is a closing particle in the TAG slot. Signs between the opener block and the class that the parser calls count or counted-thing are shown with their parser label. Exceptions are real: row 8 keeps 717 (shared with row 7) as the house sign and 240 is absent; row 14 (415-100) has no front fish and shares its pitchfork-person unit with row 13, whose front is 240; row 16 has no front.

| # | seal | house (depth) | animal | opener block | name sign by sign | class sign | whole text in reading order |
|---|---|---|---|---|---|---|---|
| 1 | M-1738 | DKE Trench E- (-6.5 ft) | Bull1:S | 692 An X but drawn in outline + 060 A single small vertical line, then another | 235 Fish with a caret shaped hat [HOUSEHOLD] ; 240 Fish with extra whiskers on cheeks [PERSONAL] | 226 Fish with four small vertical strokes arou | 692-060-235-240-226 |
| 2 | M-47 | DKE Trench E- (-3.0 ft) | Bull1:J | 861 diamond+small diamond + 002 two short strokes | 235 Fish with a caret shaped hat [HOUSEHOLD] ; 760 U with decorated branching at top [ENDER] | 740 jar | 861-002-235-760-740 |
| 3 | M-323 | DKE Trench E- (-1.0 ft) | Bull1:L | none | 235 Fish with a caret shaped hat [HOUSEHOLD] ; 415 Pitchfork with tines [PERSONAL] ; 220 Fish with no other decoration [PERSONAL] | 520 spear | 235-415-220-520 |
| 4 | M-865 | DKE Trench E- (-1.25 ft) | Bull1:W | 820 six-spoke wheel | 001 one stroke [not name: count] ; 235 Fish with a caret shaped hat [HOUSEHOLD] ; 240 Fish with extra whiskers on cheeks [PERSONAL] | 090 plain person | 820-001-235-240-740-090 |
| 5 | M-1988 | DKG. (S) 1I (-12.7 ft) | none | none | 240 Fish with extra whiskers on cheeks [HOUSEHOLD] ; 772 U where one arm has a double headed pitchf [PERSONAL] | 740 jar | 240-772-740 |
| 6 | M-228 | DKG. (S) 1I (-14.9 ft) | Bull1:J | none | 240 Fish with extra whiskers on cheeks [HOUSEHOLD] ; 636 Rectangle, taller than wide, with vertical [PERSONAL] | 740 jar | 240-636-740 |
| 7 | M-651 | DKG. (S) 1I (-17.3 ft) | Bull1:W | 820 six-spoke wheel + 002 two short strokes | 240 Fish with extra whiskers on cheeks [HOUSEHOLD] ; 220 Fish with no other decoration [PERSONAL (parser: counted-thing)] ; 717 A cat's paw perhaps, two vertical strokes  [PERSONAL] | 740 jar | 820-002-240-220-717-740 |
| 8 | M-1680 | DKG. (S) 1I (-18.1 ft) | Bull1:W | none | 415 Pitchfork with tines [PERSONAL] ; 220 Fish with no other decoration [PERSONAL (parser: counted-thing)] ; 717 A cat's paw perhaps, two vertical strokes  [HOUSEHOLD] | 740 jar | 415-220-717-740 |
| 9 | M-1977 | DKG. (S) 4- (-9.8 ft) | none | none | 140 Person with round breasts and one raised a [HOUSEHOLD] ; 746 Classic jar symbol with two horizontal han [PERSONAL] ; 142 Person with staff [PERSONAL] | 617 ? | 140-746-142-617 |
| 10 | M-708 | DKG. (S) 4- (-21.6 ft) | Bull1:W | none | 140 Person with round breasts and one raised a [HOUSEHOLD] ; 390 tree [PERSONAL] ; 002 two short strokes [not name: count] ; 061 Simple lambda but reversed horizontally, a [PERSONAL] | 740 jar | 140-390-002-061-740 |
| 11 | M-319 | DKG. (S) 4- (-9.3 ft) | Tigr | none | 032 two long strokes [not name: count] ; 220 Fish with no other decoration [not name: counted-thing] ; 240 Fish with extra whiskers on cheeks [HOUSEHOLD] ; 033 three long strokes [not name: count] ; 812 Leaf with small square hatched decoration  [PERSONAL] | 740 jar | 032-220-240-033-812-740 |
| 12 | (no CISI no.) | DKG First Street- (-18.6 ft) | Bull1:S | 861 diamond+small diamond + 002 two short strokes | 240 Fish with extra whiskers on cheeks [HOUSEHOLD] ; 637 Rectangle, taller than wide, with vertical [PERSONAL] | 740 jar | 861-002-240-637-740 |
| 13 | M-199 | DKG First Street- (-20.3 ft) | Bull1:S | 861 diamond+small diamond + 002 two short strokes | 240 Fish with extra whiskers on cheeks [HOUSEHOLD] ; 415 Pitchfork with tines [PERSONAL] ; 100 Person with three heads [ENDER] | 090 plain person | 861-002-240-415-100-740-090 |
| 14 | M-850 | DKG First Street- (-15.9 ft) | Bull1:L | 861 diamond+small diamond + 002 two short strokes | 415 Pitchfork with tines [PERSONAL] ; 100 Person with three heads [ENDER] | 740 jar | 861-002-415-100-740 |
| 15 | M-238 | DKG First Street- (-15.9 ft) | Gaur | none | 233 Fish with a horizontal line through body [HOUSEHOLD] ; 803 Leaf with tree at bottom [PERSONAL] | 740 jar | 233-803-740 |
| 16 | M-986 | DKG First Street- (-10.9 ft) | Bull1 | none | 605 Tall box with horizontal hatching througho [PERSONAL] ; 760 U with decorated branching at top [ENDER] | 740 jar | 605-760-740 |
| 17 | M-1849 | DKG. (N) 18- (-8.1 ft) | Bull1:L | none | 233 Fish with a horizontal line through body [HOUSEHOLD] ; 804 Leaf with tree at bottom, caged by four sm [PERSONAL] | 400 comb | 233-804-400 |
| 18 | M-217 | DKG. (N) 18- (-5.8 ft) | Bull1 | none | 233 Fish with a horizontal line through body [HOUSEHOLD] ; 032 two long strokes [not name: count] ; 877 Diamond with four small diamonds at each v [PERSONAL] | 740 jar | 233-032-877-740 |
| 19 | M-1726 | DKG. (S) 7II (-5.6 ft) | Bull1:W | 861 diamond+small diamond + 002 two short strokes | 240 Fish with extra whiskers on cheeks [HOUSEHOLD] ; 495 ? [PERSONAL] ; 615 A grid of x by y cells [PERSONAL] | 740 jar | 861-002-240-495-615-740 |
| 20 | M-1746 | DKG. (S) 7II (-10.8 ft) | Bull1:S | 817 diamond+small diamond + 002 two short strokes | 240 Fish with extra whiskers on cheeks [HOUSEHOLD] ; 415 Pitchfork with tines [PERSONAL] ; 100 Person with three heads [ENDER] | 090 plain person | 817-002-240-415-100-740-090 |
| 21 | M-1760 | DKG. (S) 6I (-10.6 ft) | Bull1:S | 820 six-spoke wheel + 060 A single small vertical line, then another | 235 Fish with a caret shaped hat [HOUSEHOLD] ; 240 Fish with extra whiskers on cheeks [PERSONAL] ; 923 Right parenthesis drawn in outline [ENDER] | 740 jar | 820-060-235-240-923-740 |
| 22 | M-326 | DKG. (S) 6I (-12.4 ft) | Bull1:S | 920 Right parenthesis with small leaf at middl + 060 A single small vertical line, then another + 741 Classic jar symbol with two horizontal han | 235 Fish with a caret shaped hat [HOUSEHOLD] ; 904 Two slightly nested right parentheses [PERSONAL] | 740 jar | 920-060-741-235-904-740 |
| 23 | M-1814 | DKE Trench EI (-6.0 ft) | Bull1:S | none | 240 Fish with extra whiskers on cheeks [HOUSEHOLD] ; 415 Pitchfork with tines [PERSONAL] ; 220 Fish with no other decoration [PERSONAL] | 520 spear | 240-415-220-520 |
| 24 | M-1753 | DKG. (S) 8A- (-8.4 ft) | Bull1:L | 861 diamond+small diamond + 002 two short strokes | 240 Fish with extra whiskers on cheeks [HOUSEHOLD] ; 519 ? [PERSONAL] ; 760 U with decorated branching at top [ENDER] | 740 jar | 861-002-240-519-760-740 |
| 25 | M-208 | DKG. (S) 8A- (-4.6 ft) | Bull1:J | none | 240 Fish with extra whiskers on cheeks [HOUSEHOLD] | 520 spear | 240-520 |
