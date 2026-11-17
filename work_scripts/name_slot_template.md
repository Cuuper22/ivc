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

Name length: {{LENS}}. 552 different name segments on 877 seals.

Signs that start names of 2 or more signs (486 such names):

{{STARTERS}}

Signs that end names of 2 or more signs:

{{ENDERS}}

Signs that stand alone as a one-sign name (391 such names):

{{ALONE}}

Signs seen 8 or more times inside 2+ sign names that sit at one end at least 75% of the time (43 signs reach 8 uses; 20 are locked; only 13 are used both first and last at 20% or more each: 717, 460, 798, 255, 705, 070, 920, 220, 706, 615 and three more):

{{LOCK}}

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

111 of the 552 distinct name segments occur on 2 or more seals; 76 on 2 or more sites; 27 multi-sign segments on 2 or more sites; 17 multi-sign segments on 3 or more seals. The 3-plus list ({{NBIG}} segments, 319 of 871 seals) with sites and the number of houses (Mohenjo-daro / Harappa excavation houses only):

{{BIG}}

Reading it: single signs (220 fish, 176 sitting person, 142 person with staff, 061, 016, 233, 550, 900) are the commonest whole names on 9 to 19 seals each across 3 to 5 sites, so they are common names (or common house names), not one person. The two-sign `590-390` is on 14 seals at 6 sites including Allahdino, Chanhu-daro, Dholavira, Harappa and a Kish seal in Mesopotamia; `013-840` (5 seals) sits in Harappa, Lothal and Mohenjo-daro, three of the Mohenjo-daro seals in one house (HRB 2XII); `233-176` (4 seals) is Kalibangan, Lothal and Mohenjo-daro. `415-100` (7 seals) and `017-585` (5) are only at Mohenjo-daro; `140-100` is Harappa 2, Mohenjo-daro 2. Same whole name in different cities is therefore a feature of common names and a few fixed pairs, not rare.

## 3. Name families (names that share all but one sign)

114 families with 2 or more different fillers in the open slot; 49 with 3 or more; 30 with 4 or more. By slot: length 2 first-slot open 40, last-slot open 36; length 3 first open 14, last open 13, middle open 7. 23 different first signs begin names with 4 or more different continuations (235: 40 different continuations, 240: 31, 233: 26, 798: 19, 806: 16, 590: 12); 35 different last signs close names with 4 or more different lead-ins (760: 34, 100: 28, 923: 15, 390: 13, 220: 12, 585: 11). Fillers in brackets are seal counts. The 30 largest:

{{FAMS}}

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
{{SEALS25}}
