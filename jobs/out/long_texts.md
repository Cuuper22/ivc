# Long texts read whole

Forty-one inscriptions (the 40 longest distinct texts plus the Dholavira signboard) parsed into phrases, read aloud with the working table (`work_data/sound_v2/values_v2.csv`, 137 signs with a sound, numbers included) and set against the corpus. Scripts: `work_scripts/long_common.py` (loader, reading order, reading), `long_texts_build.py` (pick the texts), `long_manual.py` (phrase division by hand), `long_texts_read.py` (read and mark), `long_texts_stats.py`, `long_texts_stats2.py`, `long_vessels.py`, `long_signslots.py`, `long_texts_fix.py`, `long_texts_fix2.py` (tests), `long_texts_report.py` (this file). Tables in `work_data/long_texts/`.

## What was found

1. Every one of the 41 long texts breaks into two or more phrases: 186 phrases in all (2 to 8 per text, mean 4.5), and a face of a multi-face object holds one phrase in 29 of 60 faces. Phrase kinds: 60 names, 58 count lines, 34 owner phrases ("of the X house"), 14 title phrases (X the chief / keeper / junior), 9 openings, 3 agent phrases, 2 place phrases, 1 junior, 1 load line, 1 name list, 3 signboard lines.
2. 430 of 537 signs (80%) carry a sound. Phrases marked: 76 read as sense, 73 partly (an unvalued sign sits in a slot we can name), 8 unread (one unvalued sign alone), 29 read as nonsense. 22 of the 559 sign places are lost.
3. **The nonsense is concentrated in a few sign values, not spread out.** 29 phrases are nonsense: 705 or 706 "threshing floor" with a fixed three after it (15 phrases in 15 texts), 435 "flash" (5 phrases in 5 texts), a counted jar read as "house of" (3), `176-175` "tax tax" (1) and word pairs the corpus avoids (5). Section 5 replaces them: `705/706` = a measure with a fixed "three" after it (paṭi, DEDR 3849, "measure of capacity, fixed daily allowance"), `255-435` = one title "chief of the rod" (taṭi, DEDR 3030), jar after a tall count = a counted pot.
4. **Records are a who-phrase plus a what-phrase, and one of the two repeats.** Four Lothal tags share one 8-sign agent face and differ in the other face; two Mohenjo-daro seals share a 9-sign first line and differ in the second; four Harappa tablets share `617-892-740-400` and differ in a cup count; the grain line `413-575-335-711-033-700` sits on 6 tablets under 3 different first faces.
5. **A long single-jar text is a list of name-blocks and count-lines under one "of the house".** 98 of 157 long objects have exactly one jar; the run before it cuts into blocks that recur elsewhere (`125-390` 9 lines, `002-235-240` 5, `255-435-690-740` 20, `032-220` inside a 22-line unit).
6. **Repetition inside one text is a long-text trait:** 52 of 157 long texts (33%) contain a sign twice against 75 of 1,732 texts of 3 to 5 signs (4%). The repeats are the jar (20 texts), the count strokes (`032`, `033`, `002`) and openers, i.e. repeated phrase frames.
7. Signs found only in long texts: `578` (5 uses) and `799` (4), all on five Harappa TAB:I tablets (`415-578-032-824`, `799-840-760-740`); strongly long-enriched: `711` 5.2x, `525` 5.1x, `335` 3.8x, `070` 2.9x, `413` 2.7x. They are the tablet commodity block (`413-575-335-711`) and `550-525-400`.
8. No verb found. The only sign with a fixed place between two parts is `060` (a joiner inside openers: head sign on its left in 132 of 177, jar on its right in 3 of 177). The transaction words (`892` sale, `176` tax, `550`) sit inside phrases, not between them.
9. **The signboard reads as a gate notice of quarters.** Wheel `820` (text-initial in 187 of 244 uses, "quarter" kāl) opens three phrases of the board: `820-611-388` "quarter of the [611] King", `820-850-645-031`, `821-798` "(quarter) of the Maru- (clan)". No god sign and no welcome sign in the slots; ruler (`388`, 22 of 59 uses straight before the jar) yes.

## 1. The texts and how they were picked

Source: Lipi table (`metadata_filtered.csv`), 5,679 faces on 4,694 objects, 3,614 distinct objects once copies are merged. An object is the faces `.1 .2 ...` in id order; a face is split at `/` into lines; each line is reversed into reading order, and the order of lines is reversed too (check: M-314 line 1 maps through the crosswalk to Mahadevan text 1400 line 1, `391-99-65-67-70-211` = `820-002-235-240-231-520`). Texts are ranked by legible signs (`000` lost signs not counted; they are shown). 30 distinct texts have 12 or more legible signs; 17 have exactly 11 and 10 of them are taken (ties broken by total place count including lost signs, then by the order of the table). Copies: objects with exactly the same faces are one text, listed once with a copy count. The Dholavira signboard (id 144.1, 9 signs recorded, rank 104 by length) is added as text 41.

Reading of the tables below. Sign line: `number` shape in words [sound, or the kind of word the slot says it must be]. Phrase rows: where = face and line; kind = phrase kind from the hand division; sound = the working sounds in order, `‹?›` for no value; English = structural reading, `<...>` marks an unvalued sign by its slot; mark: **reads** = every sign valued and no word pair the corpus avoids (class-bigram table `work_data/long_texts/class_bigrams.csv`, pairs seen at under 0.4 of chance with 10 or more expected); **partial** = a sign without value or a lost sign; **unread** = one unvalued sign alone; **nonsense** = an avoided pair or one of the four repaired values (reason given).

## 2. The 41 texts

### 1. M-494: TAB:B, Mohenjo-daro, DKE, Trench E-, depth -10.0 ft

24 legible signs (24 places), 3 faces, 8 phrases. Reading order: face 1: `838-798-176-740-151-697-390`; face 2: `255-070-741-150-221-840-032`; face 3: `741-904-740-820-032-017-904-415-100-921`

Signs: `838` sign 838 [eḷ] · `798` leaf-pincer: Leaf with 'pincers' coming off th [maru-] · `176` seated person: Person sitting with bent knees, [iṟai] · `740` Classic jar symbol with two horizontal handles [kuṭi] · `151` porter: Person carrying two burdens,  [kā] · `697` sign 697 [a name-end word (last 4 of 6)] · `390` Simple tree with branches at the top [maṟam] · `255` odd animal: Unknown asymmetric animal? Perhaps [mutal] · `070` A single vertical line, with two person arms [ampu] · `741` jar-dot: Classic jar symbol with two horizonta [orukuṭi] · `150` sign 150 [a name-end word (last 3 of 6)] · `221` sign 221 [a whole-name word (alone 4 of 5)] · `840` two-leaf: Two vertical leaves, slightly overla [iṇai] · `032` 2 full-height strokes [iru] · `904` Two slightly nested right parentheses [irutiṅkaḷ] · `820` Wheel with 6 spokes with even angles [kāl] · `017` 7 stacked strokes [ēḻu] · `415` Pitchfork with tines [kavar] · `100` three-headed person: Person with three heads [mutu] · `921` Left parenthesis with small semicircle against [a name-front word (first 6 of 14)]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `838-798-176-740` | owner | eḷ maru- iṟai kuṭi | of the Sesame-Descendant-Tax house | reads |
| 2 | f1l1 | `151` | title | kā | keeper | reads |
| 3 | f1l1 | `697-390` | name | ‹?› maṟam | <a name-end word (last 4 of 6)>-Warrior | partial |
| 4 | f2l1 | `255-070-741-150-221` | name | mutal ampu orukuṭi ‹?› ‹?› | Chief-Arrow-First-ward-<a name-end word (last 3 of 6)>-<a whole-name word (alone 4 of 5)> | nonsense (word-pair that the corpus avoids: TITLE>HOUSE) |
| 5 | f2l1 | `840-032` | count line | iṇai iru | pair 2 | reads |
| 6 | f3l1 | `741-904-740` | place | orukuṭi irutiṅkaḷ kuṭi | of the First-ward-Two-months house | reads |
| 7 | f3l1 | `820-032-017-904` | count line | kāl iru ēḻu irutiṅkaḷ | two quarters (kāl): seven two months | reads |
| 8 | f3l1 | `415-100-921` | name | kavar mutu ‹?› | Branch-Elder-<a name-front word (first 6 of 14)> | partial |

Three-face tablet, eight phrases. Face 1 is a normal owner phrase plus the keeper sign 151 standing straight after the jar (porter signs follow a non-final jar in 12 of 460 corpus cases). Face 3 carries a date-like pair: `904` (two months) twice and `820-032-017-904` = "two quarters, seven (units of) 904". Sister tablet M-495 differs in three places: `255` absent, `221`→`267`, final `921`→`740`; `921` stands in the jar's slot, so it is a second spelling of the ending or a second ending word.

### 2. M-495: TAB:B, Mohenjo-daro, DKG. (S), Fore Lane-, depth -16.7 ft

23 legible signs (23 places), 3 faces, 8 phrases. Reading order: face 1: `838-798-176-740-151-697-390`; face 2: `070-741-150-267-840-032`; face 3: `741-904-740-820-032-017-904-415-100-740`

Signs: `838` sign 838 [eḷ] · `798` leaf-pincer: Leaf with 'pincers' coming off th [maru-] · `176` seated person: Person sitting with bent knees, [iṟai] · `740` Classic jar symbol with two horizontal handles [kuṭi] · `151` porter: Person carrying two burdens,  [kā] · `697` sign 697 [a name-end word (last 4 of 6)] · `390` Simple tree with branches at the top [maṟam] · `070` A single vertical line, with two person arms [ampu] · `741` jar-dot: Classic jar symbol with two horizonta [orukuṭi] · `150` sign 150 [a name-end word (last 3 of 6)] · `267` Large left and right parentheses surrounding a [a name-end word (last 5 of 6)] · `840` two-leaf: Two vertical leaves, slightly overla [iṇai] · `032` 2 full-height strokes [iru] · `904` Two slightly nested right parentheses [irutiṅkaḷ] · `820` Wheel with 6 spokes with even angles [kāl] · `017` 7 stacked strokes [ēḻu] · `415` Pitchfork with tines [kavar] · `100` three-headed person: Person with three heads [mutu]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `838-798-176-740` | owner | eḷ maru- iṟai kuṭi | of the Sesame-Descendant-Tax house | reads |
| 2 | f1l1 | `151` | title | kā | keeper | reads |
| 3 | f1l1 | `697-390` | name | ‹?› maṟam | <a name-end word (last 4 of 6)>-Warrior | partial |
| 4 | f2l1 | `070-741-150-267` | name | ampu orukuṭi ‹?› ‹?› | Arrow-First-ward-<a name-end word (last 3 of 6)>-<a name-end word (last 5 of 6)> | nonsense (word-pair that the corpus avoids: TITLE>HOUSE) |
| 5 | f2l1 | `840-032` | count line | iṇai iru | pair 2 | reads |
| 6 | f3l1 | `741-904-740` | place | orukuṭi irutiṅkaḷ kuṭi | of the First-ward-Two-months house | reads |
| 7 | f3l1 | `820-032-017-904` | count line | kāl iru ēḻu irutiṅkaḷ | two quarters (kāl): seven two months | reads |
| 8 | f3l1 | `415-100-740` | owner | kavar mutu kuṭi | of the Branch-Elder house | reads |

Sister of M-494 (23 against 24 signs). Its last phrase is the template text `415-100-740` (Branch-Elder house) almost whole; M-494 ends the same frame in `921`. Frames that differ in one place: `221~267`, `921~740`, `255` present or absent: three name-end slots written with varying signs.

### 3. M-326: SEAL:S, Mohenjo-daro, DKG. (S), 6I, depth -12.4 ft

19 legible signs (22 places), 7 faces, 8 phrases, animal Bull1:S. Reading order: face 1: `920-060-741-235-904-740`; face 2: `645-003-820`; face 3: `171-032-031-171-000-000`; face 4: `000-111-390`; face 5: `840-461`; face 6: `169`; face 7: `511`

Signs: `920` leaf-paren: Right parenthesis with small leaf  [tiṅkaḷ?] · `060` ri-mark: A single small vertical line, then an [an opener word] · `741` jar-dot: Classic jar symbol with two horizonta [orukuṭi] · `235` fish-hat: Fish with a caret shaped hat [vēymīn] · `904` Two slightly nested right parentheses [irutiṅkaḷ] · `740` Classic jar symbol with two horizontal handles [kuṭi] · `645` An 'X' with no decoration [a counted thing (takes a number before it)] · `003` 3 short strokes [mū] · `820` Wheel with 6 spokes with even angles [kāl] · `171` Capital 'T' with a small leaf oriented vertica [niṟai] · `032` 2 full-height strokes [iru] · `031` 1 full-height stroke [oru] · `111` Person with U [a name-middle word (mid 5 of 10)] · `390` Simple tree with branches at the top [maṟam] · `840` two-leaf: Two vertical leaves, slightly overla [iṇai] · `461` Three short isoceles triangles, above three sh [a name-end word (last 1 of 1)] · `169` Two leaves horizontally adjacent, with a small [a whole-name word (alone 1 of 1)] · `511` Square in middle, possibly with horizontal lin [a name-front word (first 4 of 10)]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `920-060-741` | opening | tiṅkaḷ? ‹?› orukuṭi | [month-060 opening, first ward]: | partial |
| 2 | f1l1 | `235-904-740` | owner | vēymīn irutiṅkaḷ kuṭi | of the Bamboo-star-Two-months house | reads |
| 3 | f2l1 | `645-003-820` | count line | ‹?› mū kāl | <a counted thing (takes a number before it)> 3 Quarter-share | partial |
| 4 | f3l1 | `171-032-031-171-000-000` | count line | niṟai iru oru niṟai ‹?› ‹?› | weight 2 1 Weight-<lost>-<lost> | partial |
| 5 | f4l1 | `000-111-390` | name | ‹?› ‹?› maṟam | <lost>-<a name-middle word (mid 5 of 10)>-Warrior | partial |
| 6 | f5l1 | `840-461` | name | iṇai ‹?› | Pair-<a name-end word (last 1 of 1)> | partial |
| 7 | f6l1 | `169` | name | ‹?› | <a whole-name word (alone 1 of 1)> | unread |
| 8 | f7l1 | `511` | name | ‹?› | <a name-front word (first 4 of 10)> | unread |

Seven-face prism: one short phrase per face. Face 1 is a dated owner phrase (`920-060-741` month, first ward, then Bamboo-star-Two-months house); faces 2 and 3 are counted lines (3 `645`; weight `171` 2 1); faces 4 to 7 are bare names (`840-461`, `169`, `511`, `000-111-390`). A roll: a heading, a holder, quantities, then names. 6 of the 19 signs have no value, all of them in faces 2 and 4 to 7.

### 4. M-314: SEAL:S, Mohenjo-daro, HRB, 1V, depth -3.0 ft

17 legible signs (17 places), 1 face, 6 phrases. Reading order: face 1 line 1: `820-002-235-240-231-520`; face 1 line 2: `466-706-760-740`; face 1 line 3: `033-809-308-125-390-817-953`

Signs: `820` Wheel with 6 spokes with even angles [kāl] · `002` 2 short strokes [iru] · `235` fish-hat: Fish with a caret shaped hat [vēymīn] · `240` whisker fish: Fish with extra whiskers on chee [mīmīn] · `231` dotted fish: Fish with a small vertical stroke [orumīn] · `520` spear: Isocolese triangle on top of vertical l [vēḷ] · `466` A-shape with a comb of ticks (load count) [(n loads)] · `706` U-with-stroke-706: U with a long vertical stro [kaḷam] · `760` branching-U: U with decorated branching at top [maka] · `740` Classic jar symbol with two horizontal handles [kuṭi] · `033` 3 full-height strokes [mū] · `809` Leaf with small dot inside [a name-middle word (mid 1 of 1)] · `308` Prismed lines like P205, but with a decoration [a name-middle word (mid 2 of 3)] · `125` bow-person: Person with bow and arrow [vēṭṭuvaṉ] · `390` Simple tree with branches at the top [maṟam] · `817` Diamond or leaf shape with a small diamond att [kāṇi] · `953` sign 953 [a name-end word (last 1 of 1)]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `820-002-235-240-231-520` | title | kāl iru vēymīn mīmīn orumīn vēḷ | two quarters (kāl): Bamboo-star-High-star-First-star, the chief | reads |
| 2 | f1l2 | `466-706` | count line | (n) kaḷam | n assembly place | nonsense (old value kaḷam "threshing floor" (usually with a fixed "three" after it)) |
| 3 | f1l2 | `760-740` | owner | maka kuṭi | of the Son/child-of house | reads |
| 4 | f1l3 | `033-809-308` | count line | mū ‹?› ‹?› | three <a name-middle word (mid 1 of 1)> <a name-middle word (mid 2 of 3)> | partial |
| 5 | f1l3 | `125-390` | name | vēṭṭuvaṉ maṟam | Hunter-Warrior | reads |
| 6 | f1l3 | `817-953` | name | kāṇi ‹?› | a share (kāṇi): <a name-end word (last 1 of 1)> | partial |

Line 1 alone is a complete seal text (wheel two, Bamboo-star-High-star-First-star, spear = chief). Lines 2 and 3 add what a short seal cannot hold: a count of `706` (written with the load-count A-sign `466`) and a child-of house, then `Hunter-Warrior` (`125-390`, a unit seen on 9 lines) and a closing pair. Shape: [title of X] [what he holds] [names].

### 5. K-89: TAG:L, Kalibangan, depth surface -

15 legible signs (23 places), 4 faces, 4 phrases, animal Bull1. Reading order: face 1: `832-360-002-362-740-090`; face 2: `000-002-000-705-033-000`; face 3: `000-390-595-002-350-001`; face 4: `000-000-000-491-000`

Signs: `832` Leaf with small vertical stroke inside [kaṇṇi] · `360` Large 'H', possibly with top points connected  [a name-front word (first 5 of 12)] · `002` 2 short strokes [iru] · `362` Trapezoid with inner rectangle [a whole-name word (alone 2 of 4)] · `740` Classic jar symbol with two horizontal handles [kuṭi] · `090` man: Person with two arms and two legs,  [āḷ] · `705` U-with-stroke: U with a long vertical stroke i [kaḷam] · `033` 3 full-height strokes [mū] · `390` Simple tree with branches at the top [maṟam] · `595` Box with vertical stroke off top center, horiz [peṭṭi] · `350` Horizontal line with multiple lines out the to [a name-front word (first 16 of 33)] · `001` 1 short stroke [oru] · `491` sign 491 [a name-front word (first 9 of 17)]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `832-360-002-362-740-090` | agent | kaṇṇi ‹?› iru ‹?› kuṭi āḷ | manager of the Tender-leaf-<a name-front word (first 5 of 12)>-Two-<a whole-name word (alone 2 of 4)> house | partial |
| 2 | f2l1 | `000-002-000-705-033-000` | count line | ‹?› iru ‹?› kaḷam mū ‹?› | <lost>-Two-<lost>-Threshing-floor-Three-<lost> | nonsense (old value kaḷam "threshing floor" (usually with a fixed "three" after it)) |
| 3 | f3l1 | `000-390-595-002-350-001` | count line | ‹?› maṟam peṭṭi iru ‹?› oru | <lost>-Warrior-Chest-Two-<a name-front word (first 16 of 33)>-One | partial |
| 4 | f4l1 | `000-000-000-491-000` | name | ‹?› ‹?› ‹?› ‹?› ‹?› | <lost>-<lost>-<lost>-<a name-front word (first 9 of 17)>-<lost> | partial |

Kalibangan tag, 8 of 23 sign places lost. The only intact phrase is the agent phrase on face 1 (manager of the Tender-leaf-360-Two-362 house). The other faces keep `705-033`, `390-595-002` (Warrior, Chest, Two): count lines, no names to hang them on.

### 6. M-1385: TAG:P, Mohenjo-daro

15 legible signs (17 places), 4 faces, 4 phrases, animal Bull1. Reading order: face 1: `817-002-032-760-740`; face 2: `817-002-032-760-740`; face 3: `817-002-032-760-740`; face 4: `000-000`

Signs: `817` Diamond or leaf shape with a small diamond att [kāṇi] · `002` 2 short strokes [iru] · `032` 2 full-height strokes [iru] · `760` branching-U: U with decorated branching at top [maka] · `740` Classic jar symbol with two horizontal handles [kuṭi]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `817-002-032-760-740` | owner | kāṇi iru iru maka kuṭi | two shares (kāṇi): two son/child of of the house | reads |
| 2 | f2l1 | `817-002-032-760-740` | owner | kāṇi iru iru maka kuṭi | two shares (kāṇi): two son/child of of the house | reads |
| 3 | f3l1 | `817-002-032-760-740` | owner | kāṇi iru iru maka kuṭi | two shares (kāṇi): two son/child of of the house | reads |
| 4 | f4l1 | `000-000` | name | ‹?› ‹?› | <lost>-<lost> | partial |

The same five-sign phrase on three faces (a tag stamped three times) and a lost fourth face: one distinct phrase, `817-002-032-760-740`. The second "two" (`032`, tall) before `760-740` is the name element Two; "two shares: the Two-Child-of house".

### 7. C-40: IMPL, Chanhu-daro, depth +9.3 ft

15 legible signs (16 places), 2 faces, 6 phrases. Reading order: face 1: `016-220-776-825-005-909-095-390`; face 2: `066-900-031-235-240-835-000-740`

Signs: `016` 6 stacked strokes [āṟu] · `220` plain fish: Fish with no other decoration [mīn] · `776` Flowering plant with three stems that meet at  [a name-end word (last 7 of 11)] · `825` Leaf with diagonal overlapping cross hatching  [a name-end word (last 2 of 4)] · `005` 5 short strokes [ai] · `909` Left parenthesis [a name-end word (last 1 of 2)] · `095` stick-person: Person with short stick [kōlaṉ] · `390` Simple tree with branches at the top [maṟam] · `066` Tall, slightly narrow caret (mountain motif),  [a name-middle word (mid 7 of 14)] · `900` Right parenthesis (perhaps with a backward cur [tiṅkaḷ] · `031` 1 full-height stroke [oru] · `235` fish-hat: Fish with a caret shaped hat [vēymīn] · `240` whisker fish: Fish with extra whiskers on chee [mīmīn] · `835` sign 835 [a name-middle word (mid 1 of 1)] · `740` Classic jar symbol with two horizontal handles [kuṭi]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `016-220` | count line | āṟu mīn | Six-Star | reads |
| 2 | f1l1 | `776-825` | name | ‹?› ‹?› | <a name-end word (last 7 of 11)>-<a name-end word (last 2 of 4)> | partial |
| 3 | f1l1 | `005-909` | count line | ai ‹?› | five <a name-end word (last 1 of 2)> | partial |
| 4 | f1l1 | `095-390` | name | kōlaṉ maṟam | Staff-bearer-Warrior | nonsense (word-pair that the corpus avoids: TITLE>SELF) |
| 5 | f2l1 | `066-900` | name | ‹?› tiṅkaḷ | <a name-middle word (mid 7 of 14)>-Month | partial |
| 6 | f2l1 | `031-235-240-835-000-740` | owner | oru vēymīn mīmīn ‹?› ‹?› kuṭi | of the One-Bamboo-star-High-star-<a name-middle word (mid 1 of 1)>-<lost> house | partial |

Impression of a seal on clay, two faces. Half the signs are unvalued (`776 825 909 066 835`); face 1 is a string of short name-like pieces with two counts (`016-220` six stars, `005-909`), face 2 ends in an ordinary owner phrase with a lost sign inside it. Reads badly mostly for want of values, not for want of structure.

### 8. H-597: SEAL:S, Harappa, FGranery, depth -12.0 ft

14 legible signs (14 places), 2 faces, 6 phrases, animal Bull1:J. Reading order: face 1: `861-002-032-070-590-390-740`; face 2: `861-002-032-070-590-390-740`

Signs: `861` Diamond or leaf shape with a small diamond att [kāṇi] · `002` 2 short strokes [iru] · `032` 2 full-height strokes [iru] · `070` A single vertical line, with two person arms [ampu] · `590` box: Square at bottom with vertical bar coming [peṭṭi] · `390` Simple tree with branches at the top [maṟam] · `740` Classic jar symbol with two horizontal handles [kuṭi]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `861-002` | opening | kāṇi iru | two shares (kāṇi): | reads |
| 2 | f1l1 | `032-070` | count line | iru ampu | two arrow | reads |
| 3 | f1l1 | `590-390-740` | owner | peṭṭi maṟam kuṭi | of the Chest-Warrior house | reads |
| 4 | f2l1 | `861-002` | opening | kāṇi iru | two shares (kāṇi): | reads |
| 5 | f2l1 | `032-070` | count line | iru ampu | two arrow | reads |
| 6 | f2l1 | `590-390-740` | owner | peṭṭi maṟam kuṭi | of the Chest-Warrior house | reads |

The same seven signs on both faces: the short-seal template exactly (two shares, two arrows, of the Chest-Warrior house), stamped twice. Every sign valued, no avoided word pair. From Harappa mound F granary, like H-180 which names the same Chest-Warrior with the keeper sign.

### 9. H-811: TAB:B, Harappa, D-, depth -4.0 ft, 2 copies in the corpus

14 legible signs (14 places), 2 faces, 6 phrases. Reading order: face 1: `491-920-002-176-740-335-740-317`; face 2: `413-575-335-740-032-700`

Signs: `491` sign 491 [a name-front word (first 9 of 17)] · `920` leaf-paren: Right parenthesis with small leaf  [tiṅkaḷ?] · `002` 2 short strokes [iru] · `176` seated person: Person sitting with bent knees, [iṟai] · `740` Classic jar symbol with two horizontal handles [kuṭi] · `335` M with the bottom of the legs connected by a h [a name-middle word (mid 23 of 40)] · `317` Two long vertical strokes, connected by multip [a whole-name word (alone 3 of 11)] · `413` Vertical line with small horizontal lines cros [katir] · `575` trapezoid-box: Trapezoid with no bottom line,  [kōṭṭai] · `032` 2 full-height strokes [iru] · `700` cup: Simple U with no other decoration [nāḻi?]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `491-920-002` | opening | ‹?› tiṅkaḷ? iru | <a name-front word (first 9 of 17)>-Month-Two | partial |
| 2 | f1l1 | `176-740` | owner | iṟai kuṭi | of the Tax house | reads |
| 3 | f1l1 | `335-740` | owner | ‹?› kuṭi | of the <a name-middle word (mid 23 of 40)> house | partial |
| 4 | f1l1 | `317` | name | ‹?› | <a whole-name word (alone 3 of 11)> | unread |
| 5 | f2l1 | `413-575-335-740` | count line | katir kōṭṭai ‹?› kuṭi | of the Grain-ear;-sun-Great-measure;-fort-<a name-middle word (mid 23 of 40)> house | partial |
| 6 | f2l1 | `032-700` | count line | iru nāḻi? | two cup measure | reads |

Tablet, two faces. Face 1: three jar phrases in a row (`176-740` Tax house, `335-740`, `491-920-002` Month-Two as a date), face 2: the grain line `413-575-335-740` and two cups. The unvalued `335` stands right before the jar in two phrases (12 jar uses in the corpus), the same slot a house word takes.

### 10. H-2584: TAG:R, Harappa

14 legible signs (14 places), 3 faces, 6 phrases. Reading order: face 1: `705-033-095-520-468-806`; face 2: `798-231-550-527`; face 3: `055-255-435-690`

Signs: `705` U-with-stroke: U with a long vertical stroke i [kaḷam] · `033` 3 full-height strokes [mū] · `095` stick-person: Person with short stick [kōlaṉ] · `520` spear: Isocolese triangle on top of vertical l [vēḷ] · `468` A-shape with a comb of ticks (load count) [(n loads)] · `806` crop: Leaf with tree at bottom [(crop)] · `798` leaf-pincer: Leaf with 'pincers' coming off th [maru-] · `231` dotted fish: Fish with a small vertical stroke [orumīn] · `550` The 'pincer' motif [vāy] · `527` Small box with horizontal hatching, vertical l [a name-end word (last 45 of 56)] · `055` twelve-strokes: Four small vertical strokes ab [paṉṉiru] · `255` odd animal: Unknown asymmetric animal? Perhaps [mutal] · `435` Vertical line with diagonal going down from to [miṉ] · `690` nested chevrons: Two nested greater-than symbo [piṇai]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `705-033` | count line | kaḷam mū | threshing floor 3 | nonsense (old value kaḷam "threshing floor" (usually with a fixed "three" after it)) |
| 2 | f1l1 | `095-520` | title | kōlaṉ vēḷ | Staff-bearer, the chief | reads |
| 3 | f1l1 | `468-806` | load line | (n) (crop) | n crop | reads |
| 4 | f2l1 | `798-231` | name | maru- orumīn | Descendant-First-star | reads |
| 5 | f2l1 | `550-527` | name | vāy ‹?› | Gate-<a name-end word (last 45 of 56)> | partial |
| 6 | f3l1 | `055-255-435-690` | name list | paṉṉiru mutal miṉ piṇai | Twelve-Chief-Flash-Bound | nonsense (old value miṉ "flash" inside a title block) |

Tag, three faces: three vessels `705-033`; staff-bearer chief (`095-520`); n crop (A-sign + `806`); Descendant-First-star; Gate-527; twelve Chief-Flash-Bound. A list of people and goods with no jar anywhere.

### 11. H-1657: SEAL:S, Harappa, FTrench 43

13 legible signs (13 places), 1 face, 6 phrases, animal Bull1:W. Reading order: face 1: `921-690-002-032-220-235-806-003-900-032-590-405-740`

Signs: `921` Left parenthesis with small semicircle against [a name-front word (first 6 of 14)] · `690` nested chevrons: Two nested greater-than symbo [piṇai] · `002` 2 short strokes [iru] · `032` 2 full-height strokes [iru] · `220` plain fish: Fish with no other decoration [mīn] · `235` fish-hat: Fish with a caret shaped hat [vēymīn] · `806` crop: Leaf with tree at bottom [(crop)] · `003` 3 short strokes [mū] · `900` Right parenthesis (perhaps with a backward cur [tiṅkaḷ] · `590` box: Square at bottom with vertical bar coming [peṭṭi] · `405` tree-405: Simple tree with branches at the top [kiḷai] · `740` Classic jar symbol with two horizontal handles [kuṭi]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `921-690` | name | ‹?› piṇai | <a name-front word (first 6 of 14)>-Bound | partial |
| 2 | f1l1 | `002-032-220` | count line | iru iru mīn | 2 Two-Star | reads |
| 3 | f1l1 | `235-806` | name | vēymīn (crop) | Bamboo-star-Crop | reads |
| 4 | f1l1 | `003-900` | count line | mū tiṅkaḷ | three month | reads |
| 5 | f1l1 | `032-590` | count line | iru peṭṭi | two chest | reads |
| 6 | f1l1 | `405-740` | owner | kiḷai kuṭi | of the Kindred house | reads |

One 13-sign run with one jar at the end. Hand division: name `921-690`; count lines `002-032-220` (two stars), `003-900` (three months), `032-590` (two chests); a name with its crop `235-806`; then the owner word `405-740` (Kindred house). A single "of the X house" carrying an inventory.

### 12. H-773: TAB:B, Harappa, FTrench IV+V, depth -6.67 ft

13 legible signs (13 places), 2 faces, 3 phrases. Reading order: face 1: `741-530-390-002-803-798-740`; face 2: `413-575-335-711-033-700`

Signs: `741` jar-dot: Classic jar symbol with two horizonta [orukuṭi] · `530` A 'Bowtie' motif, but without the vertical lin [paṟai] · `390` Simple tree with branches at the top [maṟam] · `002` 2 short strokes [iru] · `803` Leaf with tree at bottom [il] · `798` leaf-pincer: Leaf with 'pincers' coming off th [maru-] · `740` Classic jar symbol with two horizontal handles [kuṭi] · `413` Vertical line with small horizontal lines cros [katir] · `575` trapezoid-box: Trapezoid with no bottom line,  [kōṭṭai] · `335` M with the bottom of the legs connected by a h [a name-middle word (mid 23 of 40)] · `711` U with X going from side to side near the bott [a name-end word (last 13 of 18)] · `033` 3 full-height strokes [mū] · `700` cup: Simple U with no other decoration [nāḻi?]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `741-530-390` | name | orukuṭi paṟai maṟam | First-ward-Proclamation-Warrior | reads |
| 2 | f1l1 | `002-803-798-740` | owner | iru il maru- kuṭi | two house of the Descendant house | reads |
| 3 | f2l1 | `413-575-335-711-033-700` | count line | katir kōṭṭai ‹?› ‹?› mū nāḻi? | Grain-ear;-sun-Great-measure;-fort-<a name-middle word (mid 23 of 40)>-<a name-end word (last 13 of 18)>-Three-Cup-measure | partial |

Face 1 holds a name (First-ward-Proclamation-Warrior) and an owner phrase (two Houses of the Descendant house); face 2 is the Harappa grain line `413-575-335-711` + three cups, the same line as on 5 other tablets.

### 13. M-23: SEAL:S, Mohenjo-daro, DKG. (S), 1III, depth -12.4 ft

13 legible signs (13 places), 1 face, 3 phrases, animal Bull1:W. Reading order: face 1 line 1: `920-001-235-220-520-692-060-482-740`; face 1 line 2: `368-192-871-842`

Signs: `920` leaf-paren: Right parenthesis with small leaf  [tiṅkaḷ?] · `001` 1 short stroke [oru] · `235` fish-hat: Fish with a caret shaped hat [vēymīn] · `220` plain fish: Fish with no other decoration [mīn] · `520` spear: Isocolese triangle on top of vertical l [vēḷ] · `692` outline X: An X but drawn in outline [an opener word] · `060` ri-mark: A single small vertical line, then an [an opener word] · `482` Tall caret drawn in outline, with diamond insc [kōṭukāṇi] · `740` Classic jar symbol with two horizontal handles [kuṭi] · `368` Vertical stroke with a triangular wing attache [koṭi] · `192` Squashed spider, with right two legs slightly  [a name-middle word (mid 3 of 4)] · `871` Diamond with small diamond at top (and maybe e [a name-front word (first 1 of 2)] · `842` sign 842 [a name-end word (last 3 of 3)]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `920-001-235-220-520` | title | tiṅkaḷ? oru vēymīn mīn vēḷ | month 1 Bamboo-star-Star, the chief | reads |
| 2 | f1l1 | `692-060-482-740` | owner | ‹?› ‹?› kōṭukāṇi kuṭi | [X-office-060 opening]: of the Hill-share house | partial |
| 3 | f1l2 | `368-192-871-842` | name | koṭi ‹?› ‹?› ‹?› | Banner-<a name-middle word (mid 3 of 4)>-<a name-front word (first 1 of 2)>-<a name-end word (last 3 of 3)> | partial |

Two lines. Line 1 is two phrases: `920-001-235-220-520` (month one, Bamboo-star-Star, chief) and `692-060-482-740` (X-office, of the Hill-share house). Line 2 `368-192-871-842` is a bare name ending in `842`. M-234 repeats line 1 sign for sign and changes line 2.

### 14. M-38: SEAL:S, Mohenjo-daro, DKB, 2II, depth -6.0 ft

13 legible signs (13 places), 1 face, 5 phrases, animal Bull1:J. Reading order: face 1: `032-632-125-390-002-235-240-032-220-255-435-690-740`

Signs: `032` 2 full-height strokes [iru] · `632` Rectangle, taller than wide, with vertical str [pal] · `125` bow-person: Person with bow and arrow [vēṭṭuvaṉ] · `390` Simple tree with branches at the top [maṟam] · `002` 2 short strokes [iru] · `235` fish-hat: Fish with a caret shaped hat [vēymīn] · `240` whisker fish: Fish with extra whiskers on chee [mīmīn] · `220` plain fish: Fish with no other decoration [mīn] · `255` odd animal: Unknown asymmetric animal? Perhaps [mutal] · `435` Vertical line with diagonal going down from to [miṉ] · `690` nested chevrons: Two nested greater-than symbo [piṇai] · `740` Classic jar symbol with two horizontal handles [kuṭi]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `032-632` | count line | iru pal | two many | reads |
| 2 | f1l1 | `125-390` | name | vēṭṭuvaṉ maṟam | Hunter-Warrior | reads |
| 3 | f1l1 | `002-235-240` | name | iru vēymīn mīmīn | Two-Bamboo-star-High-star | reads |
| 4 | f1l1 | `032-220` | count line | iru mīn | Two-Star | reads |
| 5 | f1l1 | `255-435-690-740` | owner | mutal miṉ piṇai kuṭi | of the Chief-Flash-Bound house | nonsense (old value miṉ "flash" inside a title block) |

Thirteen signs, one jar. The run cuts into recurring blocks: `032-632`, `125-390` (9 lines elsewhere), `002-235-240` (5), `032-220` (inside a 22-line unit `002-032-220`), `255-435-690-740` (20 lines). Four name-blocks and one "of the house": read as joint owners or a list of members with one possessive. All 13 signs valued.

### 15. M-234: SEAL:S, Mohenjo-daro, DKC, 3-, depth -4.0 ft

13 legible signs (13 places), 1 face, 4 phrases, animal Gaur. Reading order: face 1 line 1: `920-001-235-220-520-692-060-482-740`; face 1 line 2: `004-099-535-842`

Signs: `920` leaf-paren: Right parenthesis with small leaf  [tiṅkaḷ?] · `001` 1 short stroke [oru] · `235` fish-hat: Fish with a caret shaped hat [vēymīn] · `220` plain fish: Fish with no other decoration [mīn] · `520` spear: Isocolese triangle on top of vertical l [vēḷ] · `692` outline X: An X but drawn in outline [an opener word] · `060` ri-mark: A single small vertical line, then an [an opener word] · `482` Tall caret drawn in outline, with diamond insc [kōṭukāṇi] · `740` Classic jar symbol with two horizontal handles [kuṭi] · `004` 4 short strokes [nāl] · `099` sign 099 [a name-middle word (mid 2 of 2)] · `535` sign 535 [a name-middle word (mid 1 of 1)] · `842` sign 842 [a name-end word (last 3 of 3)]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `920-001-235-220-520` | title | tiṅkaḷ? oru vēymīn mīn vēḷ | month 1 Bamboo-star-Star, the chief | reads |
| 2 | f1l1 | `692-060-482-740` | owner | ‹?› ‹?› kōṭukāṇi kuṭi | [X-office-060 opening]: of the Hill-share house | partial |
| 3 | f1l2 | `004-099` | count line | nāl ‹?› | four <a name-middle word (mid 2 of 2)> | partial |
| 4 | f1l2 | `535-842` | name | ‹?› ‹?› | <a name-middle word (mid 1 of 1)>-<a name-end word (last 3 of 3)> | partial |

Line 1 identical to M-23; line 2 `004-099-535-842` again ends in `842`. Two seals share a 9-sign first line and end the second line with the same rare sign: the first line is an office or institution, the second line the person.

### 16. M-331: SEAL:S, Mohenjo-daro, HRA, 2-, depth -9.0 ft

13 legible signs (13 places), 4 faces, 5 phrases. Reading order: face 1 line 1: `073-251-600`; face 1 line 2: `015-492-004`; face 2: `899-001`; face 3: `899-380-484-899`; face 4: `003`

Signs: `073` A single vertical line, with two person arms [a name-front word (first 1 of 2)] · `251` sign 251 [a name-middle word (mid 1 of 1)] · `600` Tall rectangle with no decoration [a name-end word (last 1 of 3)] · `015` 5 stacked strokes [ai] · `492` sign 492 [a counted thing (takes a number before it)] · `004` 4 short strokes [nāl] · `899` sign 899 [a name-middle word (mid 1 of 3)] · `001` 1 short stroke [oru] · `380` Upside-down heart symbol [a name-front word (first 5 of 8)] · `484` Tall caret drawn in outline, with hatching thr [a name-middle word (mid 5 of 12)] · `003` 3 short strokes [mū]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `073-251-600` | name | ‹?› ‹?› ‹?› | <a name-front word (first 1 of 2)>-<a name-middle word (mid 1 of 1)>-<a name-end word (last 1 of 3)> | partial |
| 2 | f1l2 | `015-492-004` | count line | ai ‹?› nāl | five <a counted thing (takes a number before it)> 4 | partial |
| 3 | f2l1 | `899-001` | count line | ‹?› oru | <a name-middle word (mid 1 of 3)> 1 | partial |
| 4 | f3l1 | `899-380-484-899` | name | ‹?› ‹?› ‹?› ‹?› | <a name-middle word (mid 1 of 3)>-<a name-front word (first 5 of 8)>-<a name-middle word (mid 5 of 12)>-<a name-middle word (mid 1 of 3)> | partial |
| 5 | f4l1 | `003` | count line | mū | 3 | reads |

Four faces, no jar, 9 of 13 signs unvalued; `899` stands at both ends of the face-3 phrase `899-380-484-899` (6 of 1,433 corpus lines of 4+ signs start and end on the same sign). Reads as nothing yet; structure is a list of short pieces with three counts.

### 17. M-355: SEAL:R, Mohenjo-daro, DKG. (S), 1IV, depth -20.7 ft

13 legible signs (13 places), 1 face, 5 phrases. Reading order: face 1: `140-919-520-360-861-002-235-231-705-033-032-877-740`

Signs: `140` breasted person: Person with round breasts and [ammai] · `919` sign 919 [a name-middle word (mid 2 of 2)] · `520` spear: Isocolese triangle on top of vertical l [vēḷ] · `360` Large 'H', possibly with top points connected  [a name-front word (first 5 of 12)] · `861` Diamond or leaf shape with a small diamond att [kāṇi] · `002` 2 short strokes [iru] · `235` fish-hat: Fish with a caret shaped hat [vēymīn] · `231` dotted fish: Fish with a small vertical stroke [orumīn] · `705` U-with-stroke: U with a long vertical stroke i [kaḷam] · `033` 3 full-height strokes [mū] · `032` 2 full-height strokes [iru] · `877` Diamond with four small diamonds at each verte [nālkāṇi] · `740` Classic jar symbol with two horizontal handles [kuṭi]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `140-919-520` | title | ammai ‹?› vēḷ | Mother-<a name-middle word (mid 2 of 2)>, the chief | partial |
| 2 | f1l1 | `360` | name | ‹?› | <a name-front word (first 5 of 12)> | unread |
| 3 | f1l1 | `861-002-235-231` | opening+name | kāṇi iru vēymīn orumīn | two shares (kāṇi): Bamboo-star-First-star | reads |
| 4 | f1l1 | `705-033` | count line | kaḷam mū | threshing floor 3 | nonsense (old value kaḷam "threshing floor" (usually with a fixed "three" after it)) |
| 5 | f1l1 | `032-877-740` | owner | iru nālkāṇi kuṭi | two four shares of the house | reads |

Three-part text: a title (`140-919-520`, Mother-919 the chief), a second opener inside the line (`861-002`, two shares) that starts a new owner phrase `861-002-235-231 705-033 032-877-740`. Mid-line openers: 13 of 157 long objects, 22 of 1,732 short ones.

### 18. M-626: SEAL:S, Mohenjo-daro, DKC, 5-, depth -1.5 ft

13 legible signs (13 places), 1 face, 3 phrases, animal Bull1:J. Reading order: face 1 line 1: `692-060-255-435-690-740-692-060-803-740`; face 1 line 2: `125-374-842`

Signs: `692` outline X: An X but drawn in outline [an opener word] · `060` ri-mark: A single small vertical line, then an [an opener word] · `255` odd animal: Unknown asymmetric animal? Perhaps [mutal] · `435` Vertical line with diagonal going down from to [miṉ] · `690` nested chevrons: Two nested greater-than symbo [piṇai] · `740` Classic jar symbol with two horizontal handles [kuṭi] · `803` Leaf with tree at bottom [il] · `125` bow-person: Person with bow and arrow [vēṭṭuvaṉ] · `374` Plant curving left, small leaf at top, larger  [a name-end word (last 5 of 13)] · `842` sign 842 [a name-end word (last 3 of 3)]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `692-060-255-435-690-740` | owner | ‹?› ‹?› mutal miṉ piṇai kuṭi | [X-office-060 opening]: of the Chief-Flash-Bound house | nonsense (old value miṉ "flash" inside a title block) |
| 2 | f1l1 | `692-060-803-740` | owner | ‹?› ‹?› il kuṭi | [X-office-060 opening]: of the House house | partial |
| 3 | f1l2 | `125-374-842` | name | vēṭṭuvaṉ ‹?› ‹?› | Hunter-<a name-end word (last 5 of 13)>-<a name-end word (last 3 of 3)> | partial |

Two phrases in one formula, `692-060-X-740` twice (X = Chief-Flash-Bound, then House), then a line-2 name `125-374-842` ending in `842`. M-682 has the same first line and a lost second line.

### 19. L-190: TAG, Lothal, SRG 3GX 10, depth -3.33 ft

12 legible signs (15 places), 3 faces, 5 phrases. Reading order: face 1: `705-500-741-001-055-220-740-090`; face 2: `317-920-002-000-000-000`; face 3: `880`

Signs: `705` U-with-stroke: U with a long vertical stroke i [kaḷam] · `500` Tall triangle with vertical divider, either is [a name-middle word (mid 17 of 24)] · `741` jar-dot: Classic jar symbol with two horizonta [orukuṭi] · `001` 1 short stroke [oru] · `055` twelve-strokes: Four small vertical strokes ab [paṉṉiru] · `220` plain fish: Fish with no other decoration [mīn] · `740` Classic jar symbol with two horizontal handles [kuṭi] · `090` man: Person with two arms and two legs,  [āḷ] · `317` Two long vertical strokes, connected by multip [a whole-name word (alone 3 of 11)] · `920` leaf-paren: Right parenthesis with small leaf  [tiṅkaḷ?] · `002` 2 short strokes [iru] · `880` Diamond with four small diamonds at each verte [a whole-name word (alone 5 of 9)]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `705-500-741-001` | name | kaḷam ‹?› orukuṭi oru | Threshing-floor-<a name-middle word (mid 17 of 24)>-First-ward-One | nonsense (old value kaḷam "threshing floor" (usually with a fixed "three" after it)) |
| 2 | f1l1 | `055-220-740-090` | agent | paṉṉiru mīn kuṭi āḷ | manager of the Twelve-Star house | reads |
| 3 | f2l1 | `317-920-002` | count line | ‹?› tiṅkaḷ? iru | <a whole-name word (alone 3 of 11)>-Month-Two | partial |
| 4 | f2l1 | `000-000-000` | name | ‹?› ‹?› ‹?› | <lost>-<lost>-<lost> | partial |
| 5 | f3l1 | `880` | name | ‹?› | <a whole-name word (alone 5 of 9)> | unread |

Lothal tag. Face 1 is the agent phrase `705-500-741-001-055-220-740-090` (manager of the Twelve-Star house), the same stone as on L-191, L-193 and L-197; face 2 and 3 differ: month two, `880`. The first face is the stamp, the other faces are what was attached to it.

### 20. L-211: TAG, Lothal

12 legible signs (15 places), 3 faces, 3 phrases, animal Bull. Reading order: face 1: `000-231-100-740`; face 2: `000-002-220-233-388-740`; face 3: `000-240-335-760-740`

Signs: `231` dotted fish: Fish with a small vertical stroke [orumīn] · `100` three-headed person: Person with three heads [mutu] · `740` Classic jar symbol with two horizontal handles [kuṭi] · `002` 2 short strokes [iru] · `220` plain fish: Fish with no other decoration [mīn] · `233` barred fish: Fish with a horizontal line throu [varimīn] · `388` heart-bar: Upside-down heart symbol with horiz [aracu] · `240` whisker fish: Fish with extra whiskers on chee [mīmīn] · `335` M with the bottom of the legs connected by a h [a name-middle word (mid 23 of 40)] · `760` branching-U: U with decorated branching at top [maka]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `000-231-100-740` | owner | ‹?› orumīn mutu kuṭi | of the <lost>-First-star-Elder house | partial |
| 2 | f2l1 | `000-002-220-233-388-740` | owner | ‹?› iru mīn varimīn aracu kuṭi | of the <lost>-Two-Star-Striped-star-King house | partial |
| 3 | f3l1 | `000-240-335-760-740` | owner | ‹?› mīmīn ‹?› maka kuṭi | of the <lost>-High-star-<a name-middle word (mid 23 of 40)>-Son/child-of house | partial |

Three faces, each a lost-crest name + jar: First-star-Elder, Two-Star-Striped-star-King, High-star-335-Child-of. Three owners on one tag.

### 21. H-131: SEAL:R, Harappa, AB-, depth -6.25 ft

12 legible signs (13 places), 1 face, 5 phrases. Reading order: face 1: `000-794-575-595-002-055-706-033-240-233-840-032-740`

Signs: `794` sign 794 [a name-middle word (mid 5 of 13)] · `575` trapezoid-box: Trapezoid with no bottom line,  [kōṭṭai] · `595` Box with vertical stroke off top center, horiz [peṭṭi] · `002` 2 short strokes [iru] · `055` twelve-strokes: Four small vertical strokes ab [paṉṉiru] · `706` U-with-stroke-706: U with a long vertical stro [kaḷam] · `033` 3 full-height strokes [mū] · `240` whisker fish: Fish with extra whiskers on chee [mīmīn] · `233` barred fish: Fish with a horizontal line throu [varimīn] · `840` two-leaf: Two vertical leaves, slightly overla [iṇai] · `032` 2 full-height strokes [iru] · `740` Classic jar symbol with two horizontal handles [kuṭi]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `000-794` | name | ‹?› ‹?› | <lost>-<a name-middle word (mid 5 of 13)> | partial |
| 2 | f1l1 | `575-595-002` | count line | kōṭṭai peṭṭi iru | Great-measure;-fort-Chest-Two | reads |
| 3 | f1l1 | `055-706-033` | count line | paṉṉiru kaḷam mū | Twelve-Assembly-place-Three | nonsense (old value kaḷam "threshing floor" (usually with a fixed "three" after it)) |
| 4 | f1l1 | `240-233` | name | mīmīn varimīn | High-star-Striped-star | reads |
| 5 | f1l1 | `840-032-740` | owner | iṇai iru kuṭi | pair 2 of the house | nonsense (jar read as "house of" where a tall count stands in front of it (a counted pot)) |

Thirteen signs, one jar. Goods first (great-measure, chest, two; twelve of `706`, three), then two fish and Pair-Two as the house. Inventory under a house, like H-1657.

### 22. H-130: SEAL:R, Harappa

12 legible signs (12 places), 1 face, 6 phrases. Reading order: face 1: `717-125-812-595-002-806-231-705-033-845-032-409`

Signs: `717` cat-paw: A cat's paw perhaps, two vertical str [tāḷ] · `125` bow-person: Person with bow and arrow [vēṭṭuvaṉ] · `812` Leaf with small square hatched decoration insi [a counted thing (takes a number before it)] · `595` Box with vertical stroke off top center, horiz [peṭṭi] · `002` 2 short strokes [iru] · `806` crop: Leaf with tree at bottom [(crop)] · `231` dotted fish: Fish with a small vertical stroke [orumīn] · `705` U-with-stroke: U with a long vertical stroke i [kaḷam] · `033` 3 full-height strokes [mū] · `845` Two overlapping leaves with diagonal hatches a [a name-middle word (mid 32 of 50)] · `032` 2 full-height strokes [iru] · `409` sign 409 [a counted thing (takes a number before it)]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `717-125` | name | tāḷ vēṭṭuvaṉ | Stem-Hunter | reads |
| 2 | f1l1 | `812-595` | count line | ‹?› peṭṭi | <a counted thing (takes a number before it)>-Chest | partial |
| 3 | f1l1 | `002-806` | count line | iru (crop) | two crop | reads |
| 4 | f1l1 | `231-705-033` | count line | orumīn kaḷam mū | First-star-Threshing-floor-Three | nonsense (old value kaḷam "threshing floor" (usually with a fixed "three" after it)) |
| 5 | f1l1 | `845-032` | count line | ‹?› iru | <a name-middle word (mid 32 of 50)> 2 | partial |
| 6 | f1l1 | `409` | name | ‹?› | <a counted thing (takes a number before it)> | unread |

No jar, no closer: seven short count lines (chest, crop, `231-705-033`, ...) and unvalued `812 845 409`. An open list.

### 23. H-180: TAB:B, Harappa, FGranery, depth -10.0 ft

12 legible signs (12 places), 2 faces, 2 phrases, animal Scene. Reading order: face 1: `368-330-741-590-390-151`; face 2: `368-330-741-590-390-151`

Signs: `368` Vertical stroke with a triangular wing attache [koṭi] · `330` sign 330 [a name-middle word (mid 2 of 3)] · `741` jar-dot: Classic jar symbol with two horizonta [orukuṭi] · `590` box: Square at bottom with vertical bar coming [peṭṭi] · `390` Simple tree with branches at the top [maṟam] · `151` porter: Person carrying two burdens,  [kā]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `368-330-741-590-390-151` | title | koṭi ‹?› orukuṭi peṭṭi maṟam kā | Banner-<a name-middle word (mid 2 of 3)>-First-ward-Chest-Warrior, the keeper | partial |
| 2 | f2l1 | `368-330-741-590-390-151` | title | koṭi ‹?› orukuṭi peṭṭi maṟam kā | Banner-<a name-middle word (mid 2 of 3)>-First-ward-Chest-Warrior, the keeper | partial |

The same phrase on both faces: `368-330-741-590-390-151` = Banner-330-First-ward-Chest-Warrior + keeper. Harappa mound F granary, the same Chest-Warrior name as the seal H-597.

### 24. H-774: TAB:B, Harappa, FTrench Ab, depth -4.0 ft, 3 copies in the corpus

12 legible signs (12 places), 2 faces, 4 phrases. Reading order: face 1: `240-705-033-550-525-400`; face 2: `413-575-335-711-033-700`

Signs: `240` whisker fish: Fish with extra whiskers on chee [mīmīn] · `705` U-with-stroke: U with a long vertical stroke i [kaḷam] · `033` 3 full-height strokes [mū] · `550` The 'pincer' motif [vāy] · `525` sign 525 [a name-end word (last 11 of 11)] · `400` comb: Vertical line with small horizontal line [ciṟ] · `413` Vertical line with small horizontal lines cros [katir] · `575` trapezoid-box: Trapezoid with no bottom line,  [kōṭṭai] · `335` M with the bottom of the legs connected by a h [a name-middle word (mid 23 of 40)] · `711` U with X going from side to side near the bott [a name-end word (last 13 of 18)] · `700` cup: Simple U with no other decoration [nāḻi?]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `240-705-033` | count line | mīmīn kaḷam mū | High-star-Threshing-floor-Three | nonsense (old value kaḷam "threshing floor" (usually with a fixed "three" after it)) |
| 2 | f1l1 | `550-525-400` | title | vāy ‹?› ciṟ | Gate-<a name-end word (last 11 of 11)>, the junior | partial |
| 3 | f2l1 | `413-575-335-711` | name | katir kōṭṭai ‹?› ‹?› | Grain-ear;-sun-Great-measure;-fort-<a name-middle word (mid 23 of 40)>-<a name-end word (last 13 of 18)> | partial |
| 4 | f2l1 | `033-700` | count line | mū nāḻi? | three cup measure | reads |

Tablet: face 1 = High-star + three of `705` + `550-525-400` (Gate-525, junior); face 2 = the grain line + three cups. Four tablets carry this pair (H-774, H-1813, H-1814, H-1816).

### 25. M-1688: SEAL:S, Mohenjo-daro, DKG. (N), 15IV, depth -6.3 ft

12 legible signs (12 places), 1 face, 5 phrases, animal Bull1:S. Reading order: face 1: `590-033-455-031-012-031-220-286-002-255-435-125`

Signs: `590` box: Square at bottom with vertical bar coming [peṭṭi] · `033` 3 full-height strokes [mū] · `455` Three triangles, one large isocoles pointing r [ampu] · `031` 1 full-height stroke [oru] · `012` 2 stacked strokes [iru] · `220` plain fish: Fish with no other decoration [mīn] · `286` Oval with several short strokes coming off the [a name-front word (first 1 of 2)] · `002` 2 short strokes [iru] · `255` odd animal: Unknown asymmetric animal? Perhaps [mutal] · `435` Vertical line with diagonal going down from to [miṉ] · `125` bow-person: Person with bow and arrow [vēṭṭuvaṉ]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `590-033` | count line | peṭṭi mū | chest 3 | reads |
| 2 | f1l1 | `455-031` | count line | ampu oru | arrow 1 | reads |
| 3 | f1l1 | `012-031-220` | count line | iru oru mīn | 2 One-Star | reads |
| 4 | f1l1 | `286` | name | ‹?› | <a name-front word (first 1 of 2)> | unread |
| 5 | f1l1 | `002-255-435-125` | name | iru mutal miṉ vēṭṭuvaṉ | two chief Flash-Hunter | nonsense (old value miṉ "flash" inside a title block) |

Count lines (three chests, one arrow, two-one stars) then a name `002-255-435-125`. Avoided pair: the title word `435` before the house-class `125`.

### 26. M-1954: SEAL:R, Mohenjo-daro, DKE, Trench E-, depth -9.0 ft

12 legible signs (12 places), 1 face, 5 phrases. Reading order: face 1: `861-002-798-415-220-705-033-752-031-590-407-740`

Signs: `861` Diamond or leaf shape with a small diamond att [kāṇi] · `002` 2 short strokes [iru] · `798` leaf-pincer: Leaf with 'pincers' coming off th [maru-] · `415` Pitchfork with tines [kavar] · `220` plain fish: Fish with no other decoration [mīn] · `705` U-with-stroke: U with a long vertical stroke i [kaḷam] · `033` 3 full-height strokes [mū] · `752` U with decorated branching at top [maka] · `031` 1 full-height stroke [oru] · `590` box: Square at bottom with vertical bar coming [peṭṭi] · `407` tree-407: Simple tree with branches at the top [kiḷai] · `740` Classic jar symbol with two horizontal handles [kuṭi]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `861-002` | opening | kāṇi iru | two shares (kāṇi): | reads |
| 2 | f1l1 | `798-415-220` | name | maru- kavar mīn | Descendant-Branch-Star | reads |
| 3 | f1l1 | `705-033` | count line | kaḷam mū | threshing floor 3 | nonsense (old value kaḷam "threshing floor" (usually with a fixed "three" after it)) |
| 4 | f1l1 | `752-031` | count line | maka oru | child of 1 | reads |
| 5 | f1l1 | `590-407-740` | owner | peṭṭi kiḷai kuṭi | of the Chest-Herd house | reads |

Fully valued: opener, name (Descendant-Branch-Star), three of `705`, child-of one, of the Chest-Herd house. The "three of 705" is the fixed unit seen in 15 of the 41.

### 27. M-391: SEAL:R, Mohenjo-daro, DK-

12 legible signs (12 places), 1 face, 3 phrases. Reading order: face 1: `717-533-861-002-805-233-003-793-740-686-845-405`

Signs: `717` cat-paw: A cat's paw perhaps, two vertical str [tāḷ] · `533` X with left points connected by vertical line, [a name-end word (last 2 of 2)] · `861` Diamond or leaf shape with a small diamond att [kāṇi] · `002` 2 short strokes [iru] · `805` Leaf with tree at bottom [a name-front word (first 2 of 3)] · `233` barred fish: Fish with a horizontal line throu [varimīn] · `003` 3 short strokes [mū] · `793` sign 793 [a counted thing (takes a number before it)] · `740` Classic jar symbol with two horizontal handles [kuṭi] · `686` An 'X' with vertical lines connected to each a [a word of unmeasured kind] · `845` Two overlapping leaves with diagonal hatches a [a name-middle word (mid 32 of 50)] · `405` tree-405: Simple tree with branches at the top [kiḷai]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `717-533` | name | tāḷ ‹?› | Stem-<a name-end word (last 2 of 2)> | partial |
| 2 | f1l1 | `861-002-805-233-003-793-740` | owner | kāṇi iru ‹?› varimīn mū ‹?› kuṭi | two shares (kāṇi): of the <a name-front word (first 2 of 3)>-Striped-star-Three-<a counted thing (takes a number before it)> house | partial |
| 3 | f1l1 | `686-845-405` | name | ‹?› ‹?› kiḷai | <a word of unmeasured kind>-<a name-middle word (mid 32 of 50)>-Kindred | partial |

Round seal, name, then a second opener `861-002` in mid-line starting an owner phrase, then a tail name. Five unvalued signs.

### 28. M-471: TAB:B, Mohenjo-daro, DK-

12 legible signs (12 places), 2 faces, 2 phrases. Reading order: face 1: `817-002-191-415-100-740`; face 2: `350-460-798-904-740-400`

Signs: `817` Diamond or leaf shape with a small diamond att [kāṇi] · `002` 2 short strokes [iru] · `191` sign 191 [a whole-name word (alone 1 of 2)] · `415` Pitchfork with tines [kavar] · `100` three-headed person: Person with three heads [mutu] · `740` Classic jar symbol with two horizontal handles [kuṭi] · `350` Horizontal line with multiple lines out the to [a name-front word (first 16 of 33)] · `460` three-peaks: Three tall, thin isoceles triangl [mukkōṭu] · `798` leaf-pincer: Leaf with 'pincers' coming off th [maru-] · `904` Two slightly nested right parentheses [irutiṅkaḷ] · `400` comb: Vertical line with small horizontal line [ciṟ]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `817-002-191-415-100-740` | owner | kāṇi iru ‹?› kavar mutu kuṭi | two shares (kāṇi): of the <a whole-name word (alone 1 of 2)>-Branch-Elder house | partial |
| 2 | f2l1 | `350-460-798-904-740-400` | junior | ‹?› mukkōṭu maru- irutiṅkaḷ kuṭi ciṟ | junior of the <a name-front word (first 16 of 33)>-Three-peaks-Descendant-Two-months house | partial |

Face 1 is a template seal text (two shares, [191]-Branch-Elder house). Face 2 is "[350-Three-peaks-Descendant-Two-months] house, junior": the comb ending after the jar names a second house and its junior. Two parties on one tablet.

### 29. H-1814: TAB:B, Harappa, ETrench 10W/11

12 legible signs (12 places), 2 faces, 4 phrases. Reading order: face 1: `240-705-033-550-525-400`; face 2: `413-575-335-711-033-740`

Signs: `240` whisker fish: Fish with extra whiskers on chee [mīmīn] · `705` U-with-stroke: U with a long vertical stroke i [kaḷam] · `033` 3 full-height strokes [mū] · `550` The 'pincer' motif [vāy] · `525` sign 525 [a name-end word (last 11 of 11)] · `400` comb: Vertical line with small horizontal line [ciṟ] · `413` Vertical line with small horizontal lines cros [katir] · `575` trapezoid-box: Trapezoid with no bottom line,  [kōṭṭai] · `335` M with the bottom of the legs connected by a h [a name-middle word (mid 23 of 40)] · `711` U with X going from side to side near the bott [a name-end word (last 13 of 18)] · `740` Classic jar symbol with two horizontal handles [kuṭi]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `240-705-033` | count line | mīmīn kaḷam mū | High-star-Threshing-floor-Three | nonsense (old value kaḷam "threshing floor" (usually with a fixed "three" after it)) |
| 2 | f1l1 | `550-525-400` | title | vāy ‹?› ciṟ | Gate-<a name-end word (last 11 of 11)>, the junior | partial |
| 3 | f2l1 | `413-575-335-711` | name | katir kōṭṭai ‹?› ‹?› | Grain-ear;-sun-Great-measure;-fort-<a name-middle word (mid 23 of 40)>-<a name-end word (last 13 of 18)> | partial |
| 4 | f2l1 | `033-740` | count line | mū kuṭi | three house of | nonsense (jar read as "house of" where a tall count stands in front of it (a counted pot)) |

As H-774 with the jar `740` where the cup stands at the end of face 2: `033-740` = three jars (a counted pot), not "three house of".

### 30. H-1813: TAB:B, Harappa, ETrench 10W/11

12 legible signs (12 places), 2 faces, 4 phrases. Reading order: face 1: `220-705-033-550-525-400`; face 2: `413-575-335-711-033-700`

Signs: `220` plain fish: Fish with no other decoration [mīn] · `705` U-with-stroke: U with a long vertical stroke i [kaḷam] · `033` 3 full-height strokes [mū] · `550` The 'pincer' motif [vāy] · `525` sign 525 [a name-end word (last 11 of 11)] · `400` comb: Vertical line with small horizontal line [ciṟ] · `413` Vertical line with small horizontal lines cros [katir] · `575` trapezoid-box: Trapezoid with no bottom line,  [kōṭṭai] · `335` M with the bottom of the legs connected by a h [a name-middle word (mid 23 of 40)] · `711` U with X going from side to side near the bott [a name-end word (last 13 of 18)] · `700` cup: Simple U with no other decoration [nāḻi?]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `220-705-033` | count line | mīn kaḷam mū | Star-Threshing-floor-Three | nonsense (old value kaḷam "threshing floor" (usually with a fixed "three" after it)) |
| 2 | f1l1 | `550-525-400` | title | vāy ‹?› ciṟ | Gate-<a name-end word (last 11 of 11)>, the junior | partial |
| 3 | f2l1 | `413-575-335-711` | name | katir kōṭṭai ‹?› ‹?› | Grain-ear;-sun-Great-measure;-fort-<a name-middle word (mid 23 of 40)>-<a name-end word (last 13 of 18)> | partial |
| 4 | f2l1 | `033-700` | count line | mū nāḻi? | three cup measure | reads |

As H-774 with plain fish `220` for whisker fish `240` at the front of face 1; the grain line ends in the cup.

### 31. H-1816: TAB:B, Harappa, EB

11 legible signs (12 places), 2 faces, 4 phrases. Reading order: face 1: `413-575-335-000-033-740`; face 2: `240-705-033-550-525-400`

Signs: `413` Vertical line with small horizontal lines cros [katir] · `575` trapezoid-box: Trapezoid with no bottom line,  [kōṭṭai] · `335` M with the bottom of the legs connected by a h [a name-middle word (mid 23 of 40)] · `033` 3 full-height strokes [mū] · `740` Classic jar symbol with two horizontal handles [kuṭi] · `240` whisker fish: Fish with extra whiskers on chee [mīmīn] · `705` U-with-stroke: U with a long vertical stroke i [kaḷam] · `550` The 'pincer' motif [vāy] · `525` sign 525 [a name-end word (last 11 of 11)] · `400` comb: Vertical line with small horizontal line [ciṟ]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `413-575-335-000` | name | katir kōṭṭai ‹?› ‹?› | Grain-ear;-sun-Great-measure;-fort-<a name-middle word (mid 23 of 40)>-<lost> | partial |
| 2 | f1l1 | `033-740` | count line | mū kuṭi | three house of | nonsense (jar read as "house of" where a tall count stands in front of it (a counted pot)) |
| 3 | f2l1 | `240-705-033` | count line | mīmīn kaḷam mū | High-star-Threshing-floor-Three | nonsense (old value kaḷam "threshing floor" (usually with a fixed "three" after it)) |
| 4 | f2l1 | `550-525-400` | title | vāy ‹?› ciṟ | Gate-<a name-end word (last 11 of 11)>, the junior | partial |

Faces in the other order from the three tablets above (grain line first, then the High-star line), with one sign lost in the grain line. The order of faces is not fixed by the reading.

### 32. H-278: TAB:B, Harappa, F-, depth -3.25 ft, 11 copies in the corpus

11 legible signs (11 places), 1 face, 4 phrases, animal Gavi. Reading order: face 1: `803-415-220-318-920-255-436-690-590-407-740`

Signs: `803` Leaf with tree at bottom [il] · `415` Pitchfork with tines [kavar] · `220` plain fish: Fish with no other decoration [mīn] · `318` Large 'H', possibly with top points connected  [a name-middle word (mid 13 of 13)] · `920` leaf-paren: Right parenthesis with small leaf  [tiṅkaḷ?] · `255` odd animal: Unknown asymmetric animal? Perhaps [mutal] · `436` Vertical line with diagonal going down from to [a name-middle word (mid 14 of 15)] · `690` nested chevrons: Two nested greater-than symbo [piṇai] · `590` box: Square at bottom with vertical bar coming [peṭṭi] · `407` tree-407: Simple tree with branches at the top [kiḷai] · `740` Classic jar symbol with two horizontal handles [kuṭi]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `803-415-220` | name | il kavar mīn | House-Branch-Star | reads |
| 2 | f1l1 | `318-920` | name | ‹?› tiṅkaḷ? | <a name-middle word (mid 13 of 13)>-Month | partial |
| 3 | f1l1 | `255-436-690` | name | mutal ‹?› piṇai | Chief-<a name-middle word (mid 14 of 15)>-Bound | partial |
| 4 | f1l1 | `590-407-740` | owner | peṭṭi kiḷai kuṭi | of the Chest-Herd house | reads |

Eleven identical tablets in the corpus (H-278 to 284, H-871 to 873, 291; mound F). Four blocks and a jar: House-Branch-Star, 318-Month, Chief-436-Bound, of the Chest-Herd house (`590-407-740`, also the end of M-1954).

### 33. H-612: SEAL:S, Harappa, FTrench III, depth -14.0 ft

11 legible signs (11 places), 2 faces, 3 phrases, animal Bull1:L. Reading order: face 1: `825-002-495-615-740`; face 2: `615-001-893-590-892-740`

Signs: `825` Leaf with diagonal overlapping cross hatching  [a name-end word (last 2 of 4)] · `002` 2 short strokes [iru] · `495` sign 495 [kompu] · `615` A grid of x by y cells [vayal] · `740` Classic jar symbol with two horizontal handles [kuṭi] · `001` 1 short stroke [oru] · `893` sign 893 [a counted thing (takes a number before it)] · `590` box: Square at bottom with vertical bar coming [peṭṭi] · `892` Bow and arrow [vil]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `825-002-495-615-740` | owner | ‹?› iru kompu vayal kuṭi | of the <a name-end word (last 2 of 4)>-Two-Branch-Field house | partial |
| 2 | f2l1 | `615-001-893` | count line | vayal oru ‹?› | Field-One-<a counted thing (takes a number before it)> | partial |
| 3 | f2l1 | `590-892-740` | owner | peṭṭi vil kuṭi | of the Chest-Sale house | reads |

Seal with two faces, two owner phrases (a Field house and a Chest-Sale house) and a count of the unvalued `893`.

### 34. L-191: TAG, Lothal

11 legible signs (11 places), 2 faces, 3 phrases. Reading order: face 1: `705-500-741-001-055-220-740-090`; face 2: `861-002-235`

Signs: `705` U-with-stroke: U with a long vertical stroke i [kaḷam] · `500` Tall triangle with vertical divider, either is [a name-middle word (mid 17 of 24)] · `741` jar-dot: Classic jar symbol with two horizonta [orukuṭi] · `001` 1 short stroke [oru] · `055` twelve-strokes: Four small vertical strokes ab [paṉṉiru] · `220` plain fish: Fish with no other decoration [mīn] · `740` Classic jar symbol with two horizontal handles [kuṭi] · `090` man: Person with two arms and two legs,  [āḷ] · `861` Diamond or leaf shape with a small diamond att [kāṇi] · `002` 2 short strokes [iru] · `235` fish-hat: Fish with a caret shaped hat [vēymīn]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `705-500-741-001` | name | kaḷam ‹?› orukuṭi oru | Threshing-floor-<a name-middle word (mid 17 of 24)>-First-ward-One | nonsense (old value kaḷam "threshing floor" (usually with a fixed "three" after it)) |
| 2 | f1l1 | `055-220-740-090` | agent | paṉṉiru mīn kuṭi āḷ | manager of the Twelve-Star house | reads |
| 3 | f2l1 | `861-002-235` | opening+name | kāṇi iru vēymīn | two shares (kāṇi): Bamboo-star | reads |

Same agent face as L-190; face 2 is `861-002-235` (two shares, Bamboo-star), which is a complete short text.

### 35. M-2118: IMPL, Mohenjo-daro, DKG. (S), 12AI, depth -24.4 ft

11 legible signs (11 places), 2 faces, 5 phrases. Reading order: face 1: `391-595-850-480-001-821`; face 2: `803-151-004-005-913`

Signs: `391` Three pronged tree with caret hat [a name-front word (first 6 of 8)] · `595` Box with vertical stroke off top center, horiz [peṭṭi] · `850` Simple leaf or diamond, possibly rotated 45 de [kaṇ] · `480` Tall, slightly narrow caret (mountain motif) [kuṉṟi] · `001` 1 short stroke [oru] · `821` sign 821 [a whole-name word (alone 8 of 12)] · `803` Leaf with tree at bottom [il] · `151` porter: Person carrying two burdens,  [kā] · `004` 4 short strokes [nāl] · `005` 5 short strokes [ai] · `913` sign 913 [a counted thing (takes a number before it)]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `391-595` | name | ‹?› peṭṭi | <a name-front word (first 6 of 8)>-Chest | partial |
| 2 | f1l1 | `850-480-001` | count line | kaṇ kuṉṟi oru | Eye-Seed-weight-One | reads |
| 3 | f1l1 | `821` | name | ‹?› | <a whole-name word (alone 8 of 12)> | unread |
| 4 | f2l1 | `803-151` | title | il kā | House, the keeper | reads |
| 5 | f2l1 | `004-005-913` | count line | nāl ai ‹?› | 4 five <a counted thing (takes a number before it)> | partial |

Impression, two faces: Chest, eye/seed-weight one, `821`, then House-keeper and a pair of counts. Weak values (391, 821, 913).

### 36. M-10: SEAL:S, Mohenjo-daro, HRA, 1I, depth -2.0 ft

11 legible signs (11 places), 1 face, 5 phrases, animal Bull1:W. Reading order: face 1: `455-267-002-806-235-706-033-032-070-061-405`

Signs: `455` Three triangles, one large isocoles pointing r [ampu] · `267` Large left and right parentheses surrounding a [a name-end word (last 5 of 6)] · `002` 2 short strokes [iru] · `806` crop: Leaf with tree at bottom [(crop)] · `235` fish-hat: Fish with a caret shaped hat [vēymīn] · `706` U-with-stroke-706: U with a long vertical stro [kaḷam] · `033` 3 full-height strokes [mū] · `032` 2 full-height strokes [iru] · `070` A single vertical line, with two person arms [ampu] · `061` reversed lambda: Simple lambda but reversed ho [kāl] · `405` tree-405: Simple tree with branches at the top [kiḷai]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `455-267` | name | ampu ‹?› | Arrow-<a name-end word (last 5 of 6)> | partial |
| 2 | f1l1 | `002-806` | count line | iru (crop) | two crop | reads |
| 3 | f1l1 | `235-706-033` | count line | vēymīn kaḷam mū | Bamboo-star-Assembly-place-Three | nonsense (old value kaḷam "threshing floor" (usually with a fixed "three" after it)) |
| 4 | f1l1 | `032-070` | count line | iru ampu | two arrow | reads |
| 5 | f1l1 | `061-405` | name | kāl kiḷai | Quarter-Kindred | nonsense (word-pair that the corpus avoids: OPEN>KIN) |

Eleven signs, no jar: name, two crops, Bamboo-star three of `706`, two arrows, quarter-kindred. A list of counted items.

### 37. M-359: SEAL:R, Mohenjo-daro, DKG. (S), 4-, depth -10.7 ft

11 legible signs (11 places), 1 face, 4 phrases. Reading order: face 1: `632-705-385-388-002-803-235-220-590-405-740`

Signs: `632` Rectangle, taller than wide, with vertical str [pal] · `705` U-with-stroke: U with a long vertical stroke i [kaḷam] · `385` Upside-down heart symbol, possibly with vertic [a name-middle word (mid 1 of 1)] · `388` heart-bar: Upside-down heart symbol with horiz [aracu] · `002` 2 short strokes [iru] · `803` Leaf with tree at bottom [il] · `235` fish-hat: Fish with a caret shaped hat [vēymīn] · `220` plain fish: Fish with no other decoration [mīn] · `590` box: Square at bottom with vertical bar coming [peṭṭi] · `405` tree-405: Simple tree with branches at the top [kiḷai] · `740` Classic jar symbol with two horizontal handles [kuṭi]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `632-705-385-388` | name | pal kaḷam ‹?› aracu | Many-Threshing-floor-<a name-middle word (mid 1 of 1)>-King | nonsense (old value kaḷam "threshing floor" (usually with a fixed "three" after it)) |
| 2 | f1l1 | `002-803` | count line | iru il | two house | reads |
| 3 | f1l1 | `235-220` | name | vēymīn mīn | Bamboo-star-Star | reads |
| 4 | f1l1 | `590-405-740` | owner | peṭṭi kiḷai kuṭi | of the Chest-Kindred house | reads |

Eleven signs, one jar at the end (Chest-Kindred house) after a list: Many Threshing-floor ... King, two Houses, Bamboo-star-Star.

### 38. M-369: SEAL:R, Mohenjo-daro, DKG. (S), Long Lane-, depth -23.6 ft

11 legible signs (11 places), 1 face, 3 phrases. Reading order: face 1: `920-060-742-806-415-220-240-255-435-690-740`

Signs: `920` leaf-paren: Right parenthesis with small leaf  [tiṅkaḷ?] · `060` ri-mark: A single small vertical line, then an [an opener word] · `742` jar-2dots: Classic jar symbol with two horizon [irukuṭi] · `806` crop: Leaf with tree at bottom [(crop)] · `415` Pitchfork with tines [kavar] · `220` plain fish: Fish with no other decoration [mīn] · `240` whisker fish: Fish with extra whiskers on chee [mīmīn] · `255` odd animal: Unknown asymmetric animal? Perhaps [mutal] · `435` Vertical line with diagonal going down from to [miṉ] · `690` nested chevrons: Two nested greater-than symbo [piṇai] · `740` Classic jar symbol with two horizontal handles [kuṭi]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `920-060-742` | opening | tiṅkaḷ? ‹?› irukuṭi | [month-060 opening, second ward]: | partial |
| 2 | f1l1 | `806-415-220` | name | (crop) kavar mīn | Crop-Branch-Star | reads |
| 3 | f1l1 | `240-255-435-690-740` | owner | mīmīn mutal miṉ piṇai kuṭi | of the High-star-Chief-Flash-Bound house | nonsense (old value miṉ "flash" inside a title block) |

Opening `920-060-742` (month, second ward), a crop-fish name, and the owner block High-star-Chief-Flash-Bound-jar. 10 of 11 signs have a value.

### 39. M-577: TAB:C, Mohenjo-daro, DK-

11 legible signs (11 places), 1 face, 4 phrases, animal Othr. Reading order: face 1 line 1: `495-460-365-002-004-407`; face 1 line 2: `905-032-597-142-617`

Signs: `495` sign 495 [kompu] · `460` three-peaks: Three tall, thin isoceles triangl [mukkōṭu] · `365` Vertical stroke with a triangular wing attache [a name-end word (last 8 of 17)] · `002` 2 short strokes [iru] · `004` 4 short strokes [nāl] · `407` tree-407: Simple tree with branches at the top [kiḷai] · `905` Two slightly nested right parentheses, small t [a counted thing (takes a number before it)] · `032` 2 full-height strokes [iru] · `597` sign 597 [a name-front word (first 7 of 7)] · `142` staff-bearer: Person with staff [kō] · `617` sign 617 [ūḻiyaṉ]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `495-460-365` | name | kompu mukkōṭu ‹?› | Branch-Three-peaks-<a name-end word (last 8 of 17)> | partial |
| 2 | f1l1 | `002-004-407` | count line | iru nāl kiḷai | 2 four herd | reads |
| 3 | f1l2 | `905-032` | count line | ‹?› iru | <a counted thing (takes a number before it)> 2 | partial |
| 4 | f1l2 | `597-142-617` | name | ‹?› kō ūḻiyaṉ | <a name-front word (first 7 of 7)>-King-<a name-end word (last 38 of 68)> | partial |

Copper tablet, two lines. Line 2 ends in `142-617` (King, servant), a pair of 14 lines in the corpus: "king's servant".

### 40. M-623: SEAL:S, Mohenjo-daro

11 legible signs (11 places), 1 face, 4 phrases, animal Bull1:W. Reading order: face 1: `820-530-299-002-798-415-220-176-175-760-740`

Signs: `820` Wheel with 6 spokes with even angles [kāl] · `530` A 'Bowtie' motif, but without the vertical lin [paṟai] · `299` Prismed light rays, with opposite slanting on  [a counted thing (takes a number before it)] · `002` 2 short strokes [iru] · `798` leaf-pincer: Leaf with 'pincers' coming off th [maru-] · `415` Pitchfork with tines [kavar] · `220` plain fish: Fish with no other decoration [mīn] · `176` seated person: Person sitting with bent knees, [iṟai] · `175` Person sitting with bent knees, no small tange [iṟai] · `760` branching-U: U with decorated branching at top [maka] · `740` Classic jar symbol with two horizontal handles [kuṭi]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `820-530-299` | opening | kāl paṟai ‹?› | a quarter (kāl): Proclamation-<a counted thing (takes a number before it)> | partial |
| 2 | f1l1 | `002-798-415-220` | name | iru maru- kavar mīn | two descendant Branch-Star | reads |
| 3 | f1l1 | `176-175` | count line | iṟai iṟai | Tax-Tax | nonsense (two drawings of the seated person side by side read as "tax tax") |
| 4 | f1l1 | `760-740` | owner | maka kuṭi | of the Son/child-of house | reads |

Opening (quarter, Proclamation), name, `176-175` (two drawings of the seated person side by side), child-of house.

### 41. Dholavira signboard: MISC, Dholavira, CastleCitadel, -W.Chamber

9 legible signs (9 places), 1 face, 3 phrases. Reading order: face 1: `820-611-388-820-850-645-031-821-798`

Signs: `820` Wheel with 6 spokes with even angles [kāl] · `611` Vertical line with two small boxes attached to [a name-end word (last 4 of 6)] · `388` heart-bar: Upside-down heart symbol with horiz [aracu] · `850` Simple leaf or diamond, possibly rotated 45 de [kaṇ] · `645` An 'X' with no decoration [a counted thing (takes a number before it)] · `031` 1 full-height stroke [oru] · `821` sign 821 [a whole-name word (alone 8 of 12)] · `798` leaf-pincer: Leaf with 'pincers' coming off th [maru-]

| # | where | signs | kind | sound | English | mark |
|---|---|---|---|---|---|---|
| 1 | f1l1 | `820-611-388` | phrase | kāl ‹?› aracu | a quarter (kāl): <a name-end word (last 4 of 6)>-King | partial |
| 2 | f1l1 | `820-850-645-031` | phrase | kāl kaṇ ‹?› oru | a quarter (kāl): Eye-<a counted thing (takes a number before it)>-One | nonsense (word-pair that the corpus avoids: OPEN>TRANS) |
| 3 | f1l1 | `821-798` | phrase | ‹?› maru- | <a whole-name word (alone 8 of 12)>-Descendant | partial |

The Dholavira signboard (id 144.1, gypsum, 3,000 x 370 mm, Castle, west chamber of the north gate). The record holds 9 signs; see section 6.

## 3. Phrases per text, kinds, and what reads

| # | text | signs | phrases | kinds | sense | partial | unread | nonsense | signs valued |
|---|---|---|---|---|---|---|---|---|---|
| 1 | M-494 | 24 | 8 | 3 name, 2 count line, 1 owner, 1 title, 1 place | 5 | 2 | 0 | 1 | 20/24 |
| 2 | M-495 | 23 | 8 | 2 owner, 2 name, 2 count line, 1 title, 1 place | 6 | 1 | 0 | 1 | 20/23 |
| 3 | M-326 | 19 | 8 | 4 name, 2 count line, 1 opening, 1 owner | 1 | 5 | 2 | 0 | 13/19 |
| 4 | M-314 | 17 | 6 | 2 count line, 2 name, 1 title, 1 owner | 3 | 2 | 0 | 1 | 14/17 |
| 5 | K-89 | 15 | 4 | 2 count line, 1 agent, 1 name | 0 | 3 | 0 | 1 | 11/15 |
| 6 | M-1385 | 15 | 4 | 3 owner, 1 name | 3 | 1 | 0 | 0 | 15/15 |
| 7 | C-40 | 15 | 6 | 3 name, 2 count line, 1 owner | 1 | 4 | 0 | 1 | 10/15 |
| 8 | H-597 | 14 | 6 | 2 opening, 2 count line, 2 owner | 6 | 0 | 0 | 0 | 14/14 |
| 9 | H-811 | 14 | 6 | 2 owner, 2 count line, 1 opening, 1 name | 2 | 3 | 1 | 0 | 10/14 |
| 10 | H-2584 | 14 | 6 | 2 name, 1 count line, 1 title, 1 load line, 1 name list | 3 | 1 | 0 | 2 | 13/14 |
| 11 | H-1657 | 13 | 6 | 3 count line, 2 name, 1 owner | 5 | 1 | 0 | 0 | 12/13 |
| 12 | H-773 | 13 | 3 | 1 name, 1 owner, 1 count line | 2 | 1 | 0 | 0 | 11/13 |
| 13 | M-23 | 13 | 3 | 1 title, 1 owner, 1 name | 1 | 2 | 0 | 0 | 8/13 |
| 14 | M-38 | 13 | 5 | 2 count line, 2 name, 1 owner | 4 | 0 | 0 | 1 | 13/13 |
| 15 | M-234 | 13 | 4 | 1 title, 1 owner, 1 count line, 1 name | 1 | 3 | 0 | 0 | 8/13 |
| 16 | M-331 | 13 | 5 | 3 count line, 2 name | 1 | 4 | 0 | 0 | 4/13 |
| 17 | M-355 | 13 | 5 | 1 title, 1 name, 1 opening+name, 1 count line, 1 owner | 2 | 1 | 1 | 1 | 11/13 |
| 18 | M-626 | 13 | 3 | 2 owner, 1 name | 0 | 2 | 0 | 1 | 7/13 |
| 19 | L-190 | 12 | 5 | 3 name, 1 agent, 1 count line | 1 | 2 | 1 | 1 | 9/12 |
| 20 | L-211 | 12 | 3 | 3 owner | 0 | 3 | 0 | 0 | 11/12 |
| 21 | H-131 | 12 | 5 | 2 name, 2 count line, 1 owner | 2 | 1 | 0 | 2 | 11/12 |
| 22 | H-130 | 12 | 6 | 4 count line, 2 name | 2 | 2 | 1 | 1 | 9/12 |
| 23 | H-180 | 12 | 2 | 2 title | 0 | 2 | 0 | 0 | 10/12 |
| 24 | H-774 | 12 | 4 | 2 count line, 1 title, 1 name | 1 | 2 | 0 | 1 | 9/12 |
| 25 | M-1688 | 12 | 5 | 3 count line, 2 name | 3 | 0 | 1 | 1 | 11/12 |
| 26 | M-1954 | 12 | 5 | 2 count line, 1 opening, 1 name, 1 owner | 4 | 0 | 0 | 1 | 12/12 |
| 27 | M-391 | 12 | 3 | 2 name, 1 owner | 0 | 3 | 0 | 0 | 7/12 |
| 28 | M-471 | 12 | 2 | 1 owner, 1 junior | 0 | 2 | 0 | 0 | 10/12 |
| 29 | H-1814 | 12 | 4 | 2 count line, 1 title, 1 name | 0 | 2 | 0 | 2 | 9/12 |
| 30 | H-1813 | 12 | 4 | 2 count line, 1 title, 1 name | 1 | 2 | 0 | 1 | 9/12 |
| 31 | H-1816 | 11 | 4 | 2 count line, 1 name, 1 title | 0 | 2 | 0 | 2 | 9/11 |
| 32 | H-278 | 11 | 4 | 3 name, 1 owner | 2 | 2 | 0 | 0 | 9/11 |
| 33 | H-612 | 11 | 3 | 2 owner, 1 count line | 1 | 2 | 0 | 0 | 9/11 |
| 34 | L-191 | 11 | 3 | 1 name, 1 agent, 1 opening+name | 2 | 0 | 0 | 1 | 10/11 |
| 35 | M-2118 | 11 | 5 | 2 name, 2 count line, 1 title | 2 | 2 | 1 | 0 | 8/11 |
| 36 | M-10 | 11 | 5 | 3 count line, 2 name | 2 | 1 | 0 | 2 | 10/11 |
| 37 | M-359 | 11 | 4 | 2 name, 1 count line, 1 owner | 3 | 0 | 0 | 1 | 10/11 |
| 38 | M-369 | 11 | 3 | 1 opening, 1 name, 1 owner | 1 | 1 | 0 | 1 | 10/11 |
| 39 | M-577 | 11 | 4 | 2 name, 2 count line | 1 | 3 | 0 | 0 | 8/11 |
| 40 | M-623 | 11 | 4 | 1 opening, 1 name, 1 count line, 1 owner | 2 | 1 | 0 | 1 | 10/11 |
| 41 | signboard | 9 | 3 | 3 phrase | 0 | 2 | 0 | 1 | 6/9 |

Phrase boundaries were set by hand (`long_manual.py`) from five cues, in this order of strength: (1) a closer, i.e. the jar with its relation sign, the spear, the keeper, the junior; (2) a face or line break (a face holds one phrase in 29 of 60 faces of multi-face objects); (3) a second opener (`861-002`, `692-060`, `920-060`) inside a line; (4) a unit that recurs on other objects, found with `long_cohesion.py` (blocks of 3 or more signs seen in 3 or more corpus lines); (5) a count run that starts its own counted thing. Where only cue 4 or 5 applies the phrase is a block inside a name list rather than a sentence.

## 4. What the long texts teach that short ones cannot

Corpus: 3,614 distinct objects; long = 9 or more legible signs (157), middle 6 to 8 (744), short 1 to 5 (2,705). Scripts `long_texts_stats.py`, `long_texts_stats2.py`. Measured facts first, then the reading they point to.

Measured slot facts

- S1. Jars per long object: 0 in 39, 1 in 98, 2 in 16, 3 in 4. Two or more jars: 20 of 157 long objects against 14 of 1,732 texts of 3 to 5 signs.
- S2. A jar that is not line-final: 49 of 142 jar uses in long texts (35%) against 237 of 873 in short texts (27%). After such a jar in the whole corpus (460 cases): a relation sign `090/400/679/621` 286 (62%), a porter sign 12, a new opener `692/820/861/817/920` 6 (1%), anything else 156 (34%, a second name or a count). Openers do not restart a phrase after a jar; a name does.
- S3. An opener-plus-count (`861/817/820` + `001/002/003/031/032`) in mid-line: 13 of 157 long objects (8.3%) against 22 of 1,732 short ones (1.3%). Examples: M-355, M-391.
- S4. Kind pairs in order over all 157 long objects (hand-free cut by closers): owner phrase then bare name 21, owner then owner 20, owner then count-line-with-name 12, count-line-with-name then owner 10, name then name 8, title then owner 7, name then owner 6, owner then title 4, agent phrase then name 4. A bare name follows an owner phrase 3.5 times as often as it precedes one.
- S5. Repetition inside one text: 52 of 157 long texts (33%) against 75 of 1,732 texts of 3 to 5 signs (4%). Texts with the sign twice or more: `740` 20, `032` 10, `033` 9, `002` 5, `741` 4, `368` 2, `590` 2, `390` 2, `820` 2, `692` 2, `060` 2. The same 3-sign-or-longer phrase on two or more faces of one object: M-1385 (3 faces), H-597 (2), H-180 (2).
- S6. Shared first face, different rest: the 8-sign agent face `705-500-741-001-055-220-740-090` on 4 Lothal tags (L-190 L-191 L-193 L-197) with 4 different second faces; the 9-sign first line `920-001-235-220-520-692-060-482-740` on M-23 and M-234 (second lines `368-192-871-842`, `004-099-535-842`); `617-892-740-400` on 4 Harappa tablets (H-229 H-849 H-2090 H-2089) followed by `033-700`, `700-032`, `820-060-869`, `820-001-060-869`; `255-435-156-400` on 4 tablets (H-358 H-761 H-897 H-2062).
- S7. Shared last face, different first: the grain line `413-575-335-711-033-700` on 6 objects under first faces `851-741-048-740` (3), `240-705-033-550-525-400` (2) and others; `027-032-740-400` on 4.
- S8. The ending sign `842` is line-final in 5 of 5 uses; 3 of the 5 are the second line of a seal whose first line is the office formula (`692-060` or `920-060`: M-23, M-234, M-626) and a 4th is C-54, which starts `920-060`.
- S9. `060` is a joiner: head sign on its left in 132 of 177 uses (`920` 65, `692` 45, `550` 28, `820` 26); after `920-060` a ward-number jar (`741/742/745`) follows 41 of 54 times, after `692`, `550`, `820` with `060` a ward jar follows 1 of 75 (a fish or other name sign follows); `060` before the jar directly: 3 of 177.
- S10. Counts: count before the counted thing holds across the 41 (cup `700`: count in front in 24 of 34, values 2 to 6), with one regular exception: `705` and `706` take their count after them, tall strokes, and the count is three in 65 of 69 (`705`) and 30 of 30 (`706`). `711` the same: followed by `033` in 15 of 21.
- S11. Signs found only in long texts (3+ uses, none in short): `578` (5, all five Harappa TAB:I tablets, `415-578-032-824`) and `799` (4, `799-840-760-740` and one variant, same tablets). Long-enriched against all signs with 8+ uses: `711` 5.2x, `525` 5.1x, `335` 3.8x, `070` 2.9x, `413` 2.7x, `575` 2.1x, `125` 2.1x, `850` 2.1x (`work_data/long_texts/sign_long_vs_short.csv`).
- S12. A sign opening and closing one phrase: `899-380-484-899` (M-331) is one of 6 of 1,433 corpus lines of 4+ signs that start and end on the same sign.

What these say

1. A long text is a short text with parts added, not a new kind of sentence. Of the 41, 28 contain at least one jar phrase (owner, agent or junior: name + jar + relation, the short-seal template) and 30 contain at least one count line.
2. Order between phrases. Owner phrase first, then a name (S4), and a second line that is a personal name after a first line that is an office or a house (S6, S8). The second phrase does not describe the first as "X's man, keeper of Y" in general: owner-then-title is 4 cases of 157. The pattern does occur once in full: M-494 face 1, `of the Sesame-Descendant-Tax house` + keeper `151` straight after the jar + a name. Reading on the table: second part = who handles it, name of the person handling the first.
3. A record is who + what (S6, S7). Tablets: face A = the person or house (with the junior or keeper ending), face B = the commodity and a cup count (`413-575-335-711-033-700`, `033-700`, `700-032`). Faces swap order between copies (H-1816 against H-774, H-1813, H-1814), so face order carries no meaning and the two faces are a pair, not a sequence.
4. Repeated frames inside one text (S5, S3) are list items: `692-060-X-740` twice (M-626), `817-002-032-760-740` three times (M-1385) = the same stamp on several faces; `861-002` mid-line (M-355, M-391) = a second sealed statement joined to the first.
5. Verbs and linking words. None. A linker exists, `060` (S9), and it joins an office head to the thing it governs ("month-060-first ward"). The transaction words (`892` sale, 46 uses, 22 mid-line; `176` tax; `550`) sit inside phrases next to a count, not between phrases. A verb in an account text may simply be missing, as in Linear B tablets, where the entry is name + commodity + number.
6. Counts show a second construction. Counted container words (`705`, `706`, `711`) put the number after (S10); with the number nearly always three. That is a lexical unit, "X-three", not a counting of three things.

## 5. The sign that does the damage, and a better value

The 29 nonsense phrases and the signs behind them:

| text | phrase | reason | damaging sign |
|---|---|---|---|
| M-494 | `255-070-741-150-221` | word-pair that the corpus avoids: TITLE>HOUSE | `070` |
| M-495 | `070-741-150-267` | word-pair that the corpus avoids: TITLE>HOUSE | `070` |
| M-314 | `466-706` | old value kaḷam "threshing floor" (usually with a fixed "three" after it) | `706` |
| K-89 | `000-002-000-705-033-000` | old value kaḷam "threshing floor" (usually with a fixed "three" after it) | `705` |
| C-40 | `095-390` | word-pair that the corpus avoids: TITLE>SELF | `095` |
| H-2584 | `705-033` | old value kaḷam "threshing floor" (usually with a fixed "three" after it) | `705` |
| H-2584 | `055-255-435-690` | old value miṉ "flash" inside a title block | `435` |
| M-38 | `255-435-690-740` | old value miṉ "flash" inside a title block | `435` |
| M-355 | `705-033` | old value kaḷam "threshing floor" (usually with a fixed "three" after it) | `705` |
| M-626 | `692-060-255-435-690-740` | old value miṉ "flash" inside a title block | `435` |
| L-190 | `705-500-741-001` | old value kaḷam "threshing floor" (usually with a fixed "three" after it) | `705` |
| H-131 | `055-706-033` | old value kaḷam "threshing floor" (usually with a fixed "three" after it) | `706` |
| H-131 | `840-032-740` | jar read as "house of" where a tall count stands in front of it (a counted pot) | `740` |
| H-130 | `231-705-033` | old value kaḷam "threshing floor" (usually with a fixed "three" after it) | `705` |
| H-774 | `240-705-033` | old value kaḷam "threshing floor" (usually with a fixed "three" after it) | `705` |
| M-1688 | `002-255-435-125` | old value miṉ "flash" inside a title block | `435` |
| M-1954 | `705-033` | old value kaḷam "threshing floor" (usually with a fixed "three" after it) | `705` |
| H-1814 | `240-705-033` | old value kaḷam "threshing floor" (usually with a fixed "three" after it) | `705` |
| H-1814 | `033-740` | jar read as "house of" where a tall count stands in front of it (a counted pot) | `740` |
| H-1813 | `220-705-033` | old value kaḷam "threshing floor" (usually with a fixed "three" after it) | `705` |
| H-1816 | `033-740` | jar read as "house of" where a tall count stands in front of it (a counted pot) | `740` |
| H-1816 | `240-705-033` | old value kaḷam "threshing floor" (usually with a fixed "three" after it) | `705` |
| L-191 | `705-500-741-001` | old value kaḷam "threshing floor" (usually with a fixed "three" after it) | `705` |
| M-10 | `235-706-033` | old value kaḷam "threshing floor" (usually with a fixed "three" after it) | `706` |
| M-10 | `061-405` | word-pair that the corpus avoids: OPEN>KIN | `061` |
| M-359 | `632-705-385-388` | old value kaḷam "threshing floor" (usually with a fixed "three" after it) | `705` |
| M-369 | `240-255-435-690-740` | old value miṉ "flash" inside a title block | `435` |
| M-623 | `176-175` | two drawings of the seated person side by side read as "tax tax" | `176`, `175` |
| signboard | `820-850-645-031` | word-pair that the corpus avoids: OPEN>TRANS | `820` |

Unvalued signs that spoil the most texts (number of the 41 that carry them): `335` 7, `060` 5, `711` 4, `525` 4, `692` 3, `842` 3. Values already marked paused that sit in the bad texts: `705` 12 texts, `413` 6, `435` 5, `550` 5, `706` 3, `692` 3, `388` 3.

### R1. `705`, `706` (and `711`): a measure with a fixed three, not a threshing floor

Old value: kaḷam "threshing floor" (DEDR 1376), picture word kalam "vessel" (DEDR 1305) dropped. Its own check went against (not more on records than seals: 51% against 52%). Why it reads as nonsense: "High-star, threshing floor, three" and "Bamboo-star, assembly place, three" name nothing, and the three never changes.

Measured: the two drawings are one word: `705` and `706` replace each other in 6 frames (the rest of the line identical) against 0.03 expected from their frame counts. Both take the count after them (69 of 124 uses and 30 of 67) and the count is tall-stroke (container series) in 86% of adjacent counts for `705` (73 of 85) and 82% for `706` (33 of 40), against 35% for all signs (890 of 2,511 adjacent counts), 81% for the cup `700`, 61% for the box `590`, 49% for the plain fish. The number is three in 65 of 69 (`705`) and 30 of 30 (`706`). A sign the old value could not predict.

New value from picture, slot and dictionary: the U-vessel with a stick standing in it is a measure with its striking stick, and the slot is "name, measure, three": `705/706` = *paṭi* "a weight, the ordinary measure of capacity; fixed daily allowance for food" (DEDR 3849; paṭiy-āḷ "one whose wages are paid in grain"; same word 3850 "grade, rank"). "X, mūṉṟu paṭi" = X: three paṭi, a ration. Rival kept alive: *pāṉai* "large earthen pot; a measure of capacity" (DEDR 4124), or kalam (1305). `711` (U with a cross) the same class: *pāṉai*; `711` is followed by `033` in 15 of 21 uses, tablets only.

Check on texts of 5 signs or fewer (1,879 lines, none of the 41): `705` has a tall adjacent count in 27 of 33 (82%), the count after it is three in 20 of 24; `706` tall in 12 of 16 (75%), three in 11 of 11. The value predicts both, the old one neither. Effect on the 41: of the 15 nonsense phrases, 11 are `705/706-033` count lines that now read "[X]: three paṭi" (`240-705-033` = "High-star: three paṭi", `231-705-033`, `235-706-033`, `055-706-033`, `705-033`); `466-706` in M-314 (the A-count with `706`) = "n paṭi", which the old value read as "n assembly place"; 3 (L-190, L-191, M-359) keep `705` inside a name and stay partial.

### R2. `435`: a rod, and `255-435` is one title

Old value miṉ "flash". It makes "Chief-Flash-Bound" (`255-435-690`) in M-38, M-626, M-369, M-1688 and H-2584. Measured: `435` has `255` on its left in 61 of 75 uses and `690` on its right in 38 (a porter `156` in 14); the block `255-435-690` is on 23 lines and a jar follows it in 20; `255-435-156` 2 lines. The nearest sign to `435` by neighbours is the arrow `070` (cosine 0.37, first of 77 signs), but the two never replace each other (0 frames), so `435` is a different word of the same kind, not an arrow variant.

The size test: seals with `255-435` have a median face of 838 mm2 (24 seals), with `255-435-690` 930 (18), all seals 605 (1,775). Seals with `255` and no `435`: 556 (28). The earlier result "chief seals are bigger" (684 against 600) is carried entirely by the pair.

New value: `435` = *taṭi* "stick, staff, rod, cane, measuring rod" (DEDR 3030); `255-435` = *mutal-taṭi* "head of the rod", an office (the measuring-rod holder, a surveyor-chief); `255-435-690-740` = "of the house of the head of the rod, [690]". The sound of `690` stays piṇai (bound, allied) for now. Check: the pair marks the biggest seals (838 against 605), and a title is predicted to stand in front of the jar, which it does in 20 of 23.

### R3. A jar after a tall count is a counted pot

`033-740` ends H-1814 and H-1816, read "three house of". A tall count right before the jar occurs 48 times in 1,062 jar uses (37 of them `032`); the avoided pair NUM then POSS is seen at 0.29 of chance (60 against 207). The jar is a container (kuṭam "waterpot", DEDR 1651) counted with the tall series like the cup. In H-1814 it stands where the cup stands at the end of the same line in H-774 and H-1813 (`413-575-335-711-033-[700|740]`): two writings of the counted vessel, "three cups / three jars". Check on short lines: `tall count + 740` closes 19 of 496 short lines ending in a jar (3.8%), 33 of 765 over all lines.

### R4. `413` is the commodity header, not a granary sign

The old check (granary mound F share, 20% against 34%) was the wrong place to look. Measured slot: line-first in 44 of 57 uses (77%), Harappa 44 of 57, tablets 40; next sign `575` 22, `892` 14 (sale/price), end of line 10. Reading kept (*katir* ear of grain, DEDR 1194, by the picture) but the role is a header: "grain: [575 335 711] three cups", and `413-892` = "grain, sale". Short-line check: `413` is first in 7 of 15 short lines it occurs in. The three unvalued signs after it (`575` great-measure/fort, `335`, `711`) are one block (`575-335` 21, `335-711` 18, `711-033` 15) = commodity or grade name, then the count.

### R5. `060`: a particle, sound for the slot

Not a damaging value but the commonest hole (5 of the 41, 222 uses in the corpus). Slot (S9): sits between a head sign and what it governs, never next to the jar. Proposal from the dictionary: the oblique/genitive linker *-iṉ* (the Dravidian genitive, written between head and noun), so `920-060-741` = "of the month, first ward" and `692-060-482-740` = "of the office, of the hill-share house". Check on short lines: 101 uses in lines of 2 to 5 signs, head sign on its left in 78 (77%), the ward jar to its right in 19; a particle that takes a head and a noun predicts exactly this pattern, no free-standing uses (first or last in 10 of 222 uses).

### R6. Class slips, no new value

Pair flags left over: `070-741` Arrow before First-ward (M-494, M-495): `070` stands as a name word here (arrow, a clan emblem as `455`), not a title; `095-390` staff-bearer + warrior (C-40) the same; `061-405` quarter-kindred (M-10) = `061` read as part of the name; `176-175` (M-623) two drawings of the seated person: iṟai written twice, one word.

## 6. The Dholavira signboard: what the gate said

Object: gypsum letters on a board 3,000 x 370 mm, found lying in the west guard chamber of the north gate of the Castle, fallen from above the lintel of the central passage (excavation report quoted in `evidence/tmp/source_route_hunt_20260530/Dholavira-Bisht2015.txt`). Lipi id 144.1 stores 9 signs; the published count is 10. Reading order (stored order reversed): `820-611-388-820-850-645-031-821-798`. A published Mahadevan-number string for the ten (a reader's transcription, one source) is `391 256 327 391 261 134 98 391 391 53`; the crosswalk maps 391 to 820, 256 to 611, 327 to 388, 261 to 850, 53 to 798, so five of its ten signs and the last one agree with Lipi, and the extra signs are wheels: the board has 4 wheels in 10, and Lipi's `821` is one of them.

| # | sign | picture | uses in corpus | slot elsewhere (measured) | value |
|---|---|---|---|---|---|
| 1 | `820` | six-spoke wheel | 244 | first in 187 (77%); a count of 1 to 3 follows in 138 of 139 counted cases; on the board it never has one | kāl, wheel, quarter |
| 2 | `611` | vertical line with two small boxes on top | 6 | name-end slot (last 4 of 6); on 4 seals and 2 plaques; left neighbour `820` twice, right neighbour `388` once (this board) | a proper name (word unvalued) |
| 3 | `388` | upside-down heart with bars | 59 | straight before the jar in 22 (37%), first in 17; paused value *aracu* "king, royal" | aracu, king |
| 4 | `820` | wheel | | as 1 | kāl |
| 5 | `850` | leaf or diamond on its point | 57 | right neighbour `900` month 15; left neighbour `407` herd 15; tablets 21, seals 20; Dholavira 3 | kaṇ, place, region |
| 6 | `645` | plain X | 28 | counted thing (count before it in 13 of 28); right neighbour `590` box 7 | unvalued, a counted thing |
| 7 | `031` | one tall stroke | 258 | container-series "one"; first in 99 | oru, one |
| 8 | `821` | wheel variant | 14 | first in 6; right neighbour the jar 4; left neighbour `001` 5 | kāl-type opener |
| 9 | `798` | leaf with pincers | 151 | straight before the jar 50, before `415` 23, before `240` 20; mid-name 108 | maru-, descendant, clan |

Phrase structure: the wheel is text-initial in 77% of its corpus uses and the board repeats it every three or four signs, so the wheel starts a phrase: `[820 611 388] [820 850 645 031] [(820) 821 798]`, three phrases of 3, 4 and 3 signs (Mahadevan string: `391 256 327 | 391 261 134 98 | 391 391 53`). A wheel followed by a count is the seal opener "two quarters"; none of the board's wheels has a count behind it, so here the wheel is the head word of each phrase, not an opener of a seal text.

Reading aloud: *kāl [611] aracu · kāl kaṇ [645] oru · kāl maru-*

**Commitment.** The board names a ruler and a people and divides the city in quarters: "The quarters (kāl) of King [611]; the quarter-place [645], one; the quarter of the Maru (the descendants, the clan)". The city's name is the unvalued word `611` (a rare sign, 6 uses, name slot, standing before the title `388` in the only place it meets it): "King [611]" is both the ruler and the name the gate gave the town. No god (none of its nine signs sits in a slot we have tied to a god) and no welcome (no verb, nothing between phrases). It is a statement of ownership and subdivision, put where visitors read it from outside: this city, its king, its four quarters, its clan. The plan fits: the Lipi findspot column splits Dholavira into Castle, Bailey, Middle Town and Lower Town (four parts), and four wheels stand in the ten-sign board. Evidence list: the wheel as quarter (counts of one to three, 138 of 139; seals with it smaller, 525 against 645 mm2), `388` straight before the jar in 37% of its uses (the royal house), `798` straight before the jar in 33% (the clan word), `850` right before month `900` in 15 uses.

What would move it: a transcription of the tenth sign; `611` and `645` values; a second reading of `850` (kaṇ "eye" or "place"). No image named for id 144 was found in the seal-image folder.

## Files

`work_scripts/long_common.py`, `long_cohesion.py`, `long_classgrid.py`, `long_manual.py`, `long_texts_build.py`, `long_texts_read.py`, `long_texts_stats.py`, `long_texts_stats2.py`, `long_vessels.py`, `long_signslots.py`, `long_texts_fix.py`, `long_texts_fix2.py`, `long_texts_report.py`. Data in `work_data/long_texts/` (`texts.json`, `read.json`, `class_bigrams.csv`, `sign_long_vs_short.csv`, `long_phrases_all.csv`). Rerun order: build, classgrid, read, stats, stats2, fix, fix2, report.
