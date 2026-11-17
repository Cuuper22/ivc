# The eight silent signs: sounds, meanings, tests

Scripts: `work_scripts/holes_common.py` (loader), `holes_1_slots_first.py`, `holes_3_060.py` (grammar test), `holes_4_tests.py` (first tries), `holes_5_second.py` (second tries), `holes_6_slots.py`, `holes_7_retally.py`, `holes_8_retally_report.py`, `holes_9_extra.py`, `holes_dedr.py` (dictionary search), `holes_2_show.py` (print every line a sign is on). Tables and printed results in `work_data/holes/`: `slots_eight.csv` (every slot of every sign), `060_grammar.txt`, `tests_first_try.txt`, `tests_second_try.txt`, `tests_extra.txt`, `retally_phrases_final.csv` (all 186 phrases, old and new mark), `retally_by_sign.csv`, `values_eight.csv`. Predictions sit in the docstring at the top of each test script and were written before the script was first run.

Plain-words key. **Jar** = sign 740, "house of" (kuṭi), ends most texts. **Ward jar** = jar with 1, 2 or 3 dots or strokes in its mouth (741, 742, 745), first, second, third ward. **Wheel** = 820, kāl "quarter". **Cup** = 700, a measure (nāḻi). **Head sign** = month 920, outline-X 692, gate 550, wheel 820, the four words that open a text and take the joiner 060 after them. **Comb** = 400, ciṟ "junior". **DEDR** = the Burrow and Emeneau Dravidian dictionary (local copy), number given for each word. **Mahadevan number** = the second catalogue's numbering (the second, separate transcription of the inscriptions, used here as a check set). **Slot** = the place a sign takes in a text (first, middle, last, after a count, before the jar). A **pun** = choosing a word whose meaning fits the picture and whose sound does the job the slot needs.

## 1. What was found

Every sign now has a sound, a meaning and a test that came out. Two (842, 611) rest on five and six objects, so they are the thinnest.

| sign | picture | sound and meaning (DEDR) | the test that came true | what it opens |
|---|---|---|---|---|
| 060 | short upright stroke beside a hooked stroke | **uḷ** "in, within", the place ending (698) | left neighbour is a head word in 159 of 217 uses (73%, 22.5 times what these four signs are worth in all text); chains 2 of 215; reversed order 2 of 207; same kind of word on both sides 3 of 99 | every seal opener reads as an address or date: "[month / district / gate / quarter] in [ward]" |
| 692 | X drawn in outline | **nāṭu** "district, land" (3638) | with the month sign 920 on 7 lines against 2.1 expected; second catalogue 6 against 2.24 (2.7 times); never with a ward jar after it (0 of 42) | M-23 / M-234: "month one ... district-in hill-share house" |
| 525 (+526, 527) | frame with bars, one stem down | **katavu** "door" (1187) | the three drawings replace each other in 5 otherwise identical frames; 525 sits after the gate sign in 8 of 9 and before the comb in 7 of 9 | "gate-door junior" closes six E-trench tablets |
| 335 | box with a pointed M roof | **kūṭu** "bin, grain receptacle" (1883) | on tablets 21 of 34 (62% against 37%, P 0.003); 15 of its 21 tablet lines also carry the grain header 413 (71% against 1.9%) | the grain line `413-575-335-711-033-700` reads whole on 15 faces |
| 711 | U-vessel with an X across the base | **pāṉai** "pot, a measure" (4124) | on tablets 16 of 16, all Harappa; tall-stroke count after it 11 of 11 (P 1e-5); its slot is filled only by 711 (13) or the jar (1) | "grain, granary, bin, pot: three cups" |
| 842 | two overlapping leaves with four small ticks round them (Mahadevan 404) | **tuṇai** "companion, deputy" (3308) | last in the line 5 of 5; on a second line 3 of 5 against 2.1% for jar closers; chief sign in the text 3 of 5 against 15.7% (P 0.030); every measured seal above the 92nd percentile of seal size | a second line "[name], deputy" under a master's first line |
| 611 | upright pole topped by a small double box | **kuṭai** "royal umbrella", the name of a ruling house (1663) | name part: wheel on its left twice, never a name; king title or jar on its right; six uses over four sites | the board's "kāl kuṭai aracu" |
| 645 | plain X | **kuṟi** "mark, tally" (1847) | count right before it in 10 of 22; non-seal objects 16 of 22 (73% against 53%, P 0.05); in a seal frame it stands where the chief 255 stands | board's second line; counted marks on pots, rods, tablets |
| 705/706 | U-vessel with a stick | paṭi (3849) | taken as given (long_texts.md R1) | 12 nonsense phrases clear |
| 435 | slanting stick | taṭi (3030) | taken as given (R2) | 255-435 "chief of the rod" |

Three things now read that did not: the opening formula (060), the grain-ration tablets (335, 711, 525), and the signboard.

## 2. Sign by sign

### 060: the joiner. Sound uḷ "in"

Picture: a short upright stroke next to a longer stroke that hooks at the foot (shaped like the Japanese "ri"). 217 uses on 215 objects (Mahadevan 123: 193 uses).
Slots: middle 207, first 4, last 6; never first-or-last as a rule (10 of 217). Count right before it 4; count right after 36; ward jar right after 49 (after the month sign: 48 of 63, 76%; after outline-X, gate, wheel: 0 of 90 ward jars, fish names and counts instead); plain jar right after it 3. Objects: seals 175 (81% against 47% of all lines), tablets 30 (14% against 37%), tags 6, pots 3. Sites: Mohenjo-daro 114, Harappa 55, Lothal 13, Chanhu-daro 8, Dholavira 6. Left: month 63, outline-X 44, gate 26, wheel 26 (159 of 217); right: first-ward jar 36, High-star fish 15, Bamboo-star fish 10, second-ward jar 10, then counts.

The test of the genitive (-iṉ, "of") against four other grammatical words. What each says about the two sides, written first (`holes_3_060.py`), and the number:

| word | what it predicts | number | verdict |
|---|---|---|---|
| genitive -iṉ "of" | any owner noun on the left (names too), chains X-iṉ Y-iṉ Z, order not reversible | left is a fish name 2 of 217; two 060 in one line 2 of 215; reversed order 2 of 207 | order fits; owner-noun and chain parts go against. Stays alive |
| locative -uḷ "in" | a closed set of place and time words on the left, no chains, not reversible, seals as much as records | left is a head word 73% (22.5 times chance); chains 2 of 215; reversed 2 of 207; seals 81% | holds on every count. Leads |
| dative -ku "to, for" | records (tablets, tags), a count or measure on the right | seals 81% against 47%; count on the right 36 of 217 (17%) | against |
| plural -kaḷ | a countable noun on the left, often after a number | count on the left 4 of 217 | against |
| "and" -um | same kind of word on both sides, chains, reversible | same kind both sides 3 of 99; reversed 2 of 207 | against |

Second catalogue: Mahadevan 123 has the same four heads on its left in 145 of 193 uses (75%). What it means: the four heads are all places or times (month, gate, quarter, district), so the joiner is "in", and an opener is "in [place/time], [ward / name]". What it opens: 164 of its 219 uses in the older role table are openers, so the first words of most seals are an address or date line.
Rescue not needed. Genitive is kept as a second reading: the observation that splits them is a person or house name on the left of 060 (genitive allows it, locative does not); two cases in 217.

### 692: outline X. Sound nāṭu "district, land"

Picture: an X drawn as a double outline (Mahadevan 150). 75 uses on 73 objects: first in line 56 (75%), alone 3, middle 12, last 4; 060 right after it in 44. Seals 50 (35 expected), tablets 19, pots 5; Mohenjo-daro 35, Harappa 34, Lothal 3. Median seal face 921 mm2 against 605 for all seals. After 692-060: ward jar 0 of 42, fish name 13, count 5, descendant 798 3, chief 255 3. On the same line as the month 920: 7 against 2.1; with gate 550: 1 against 1.7; with wheel 820: 1 against 3.5.
First word, written first: **teru** "street" (3422). Predictions: no ward jar after it (0 of 42, true); not with the other place heads and not with the month (place heads 1 and 1 against 1.7 and 3.5, true; month 7 against 2.1, **went against**); big planned cities 0.88 or more (0.92, P 0.011, true); second catalogue first in line 70% (81%) and 123 after it 60% (70%), true. The month result split the word: a street is a place head, but a place head should not sit with the month 3.3 times as often as chance.
Second word, written first: **nāṭu** "district, land". Prediction: Mahadevan 150 and the month's partner (293) share a line at 2.0 times chance or more: 6 lines against 2.24 expected, 2.68 times. Also 692 and 920 never touch (0 adjacent in 7 lines), so they stand in different phrases. Reading: M-23 `920-001-235-220-520-692-060-482-740` = "month one, Bamboo-star Star, the chief; in the district, hill-share house". Meaning: the district is a land level between the month and the house.

### 525 (and 526, 527): the door. Sound katavu "door"

Picture: a framed box with horizontal bars and one stem down one side (all three Lipi numbers are Mahadevan 254, one sign). 525: 9 uses, all tablets (Harappa 8), five of them from Harappa E-trench 10; 8 of 9 straight after the gate 550, 7 of 9 straight before the comb 400, 2 line-final. 526: 13 uses, always last (tablets 8, seals 5). 527: 59 uses, 48 last, 50 on seals, sizes small (median face 533 mm2, seen while choosing the word, not a clean test). The three never share a line (0); they replace each other in 5 otherwise identical frames (written as a prediction of 3 or more). After the gate: 525 8 of 9, 526 5 of 13, 527 22 of 59. In Mahadevan 254 (73 uses) the gate's partner is on its left in 29 (40%), the comb's partner on its right in 4.
Word: katavu "door, door-leaf" (1187), because the picture is a door with its bar and the sign sits behind the gate word: "gate-door" = door-keeper title, "gate-door junior" = junior door-man.
Went against: "each of the three stands after the gate in 75% or more" (526 38%, 527 37%, Mahadevan 40%); "the sign before it, when it is not the gate, is a name word in 70% or more" (23 of 43 valued name-class, 53%; 13 more are unvalued signs, 4 titles, 2 counts, so unsettled). Rescue: the family test above (5 frames) shows one word in three drawings; the gate is its commonest left word, not its only one, so it is a closing title that often takes "gate" in front. The reading stands as a title; the tablet version is what is cleanest: `240-705-033-550-525-400` = "High-star: three paṭi (ration). Gate-door junior." on four E-trench tablets (H-774, H-1813, H-1814, H-1816).

### 335: box with a roof. Sound kūṭu "bin"

Picture: a square box with a pointed M-shaped roof (Mahadevan 192). 34 uses on 33 objects: middle 31, first 2, last 1. Tablets 21 (62% against 37%, binomial P 0.003), seals 11, tag 1, pot 1. Harappa 21, Mohenjo-daro 8, Kalibangan 2. Left: 575 (kōṭṭai, the great measure or store) 15 of 34 (44%), a count 4; right: 711 13, jar 9, "son-of" 760 7 (711, jar or son-of on the right in 29 of 34, 85%). Fifteen of its 21 tablet lines carry the grain header 413 (71% against 1.9% for all tablet lines, P 6e-22).
Word: kūṭu "nest, cage, receptacle for grain, dome" (1883). Predictions: on tablets above the base rate 55% (62%, true); after 575 in 40% or more (44%, true); followed by 711 or a jar kind in 70% or more (85%, true); with the grain header 70% or more (71%, true).
Went against: as a name word (335-760-740 "of the house of the son of 335") a house emblem would repeat on two or more objects at one site; none does (15 different spellings). So 335 is a middle name word that carries no house on its own. Rescue: the tablet side, which is the sign's main home, carries the test above. Rival kept: a grain name instead of the bin. Both read the line the same way.

### 711: U-vessel with an X base. Sound pāṉai "pot, a measure"

Picture: a U-shaped vessel with an X across the lower part, as of a net or wicker base (Mahadevan 341). 16 uses, 16 objects, every one a Harappa tablet. Left 335 in 13; right: count 033 in 11, line end in 1. In the grain frame `413-575-335-_-count-_` the slot is filled by 711 13 times, by the jar once, lost once: nothing but a container fills it. The count after the slot is three (033) 10 times, two once.
Word: pāṉai "large earthen pot, a measure of capacity" (4124). Predictions: tall-stroke (container series) count after it 80% or more (11 of 11, P 1e-5; true); only container kinds in its slot (true); in the two lines where no cup or jar follows the count (H-1815, H-1810) the count is still tall (2 of 2, true). Caution: in the other lines the three belongs to the cup, so the 11 of 11 is partly the cup's number; the two cupless lines are the clean part.

### 842: caged pair of leaves. Sound tuṇai "companion, deputy"

Picture (Mahadevan 404, found because its neighbours on the five seals match): two overlapping leaves with four short ticks around them, the leaf-pair family 840 (iṇai "pair"). 5 uses, 5 seals (Mohenjo-daro 4, Chanhu-daro 1), last in line 5 of 5, no jar in any of the five. Left neighbours 871, 535, 374, 391, 032. Three of the five (M-23, M-234, M-626) are second lines; closers like the jar are on a second line 22 of 1,073 (2.1%). Seal faces 1,340 to 2,209 mm2 (four measured) against 605 for all seals.
First word, written first: tuṇai as "helper, junior": predicted a small seal (640 mm2 or less). **Went against**: 1,502, 1,648, 2,209, 1,340. Second try, same word, better meaning: tuṇai also "deputy, associate" (3308). Written second: 3 of 5 texts carry a chief sign (spear 520, 255, 388) elsewhere in the text against a base of 15.7% (P 0.030): M-23, M-234, M-626 yes, M-1014 and C-54 no; and every measured seal above the 75th percentile (all four above the 92nd).
Read plainly: both second-try predictions were set after the size numbers and the first lines of M-23, M-234 had been seen, so they describe the five seals; the Mahadevan table holds the same five seals (404 on 1012, 1321, 1397, 2398, 6133) and offers no separate check. What it opens: M-23 and M-234 share the master's first line (month one, Bamboo-star Star the chief, in the district a hill-share house) and differ in the second line, `368-192-871-842` and `004-099-535-842`: two different deputies of one master. Forward prediction for the next seal found with this sign: closes a second line, on a big seal, under a line with a chief sign.

### 611: pole with a double box. Sound kuṭai "umbrella", a ruling house name

Picture: an upright pole topped by a small double box (Mahadevan 256, 4 uses). Six uses on five objects: H-3 seal (Harappa, granary mound F) `...615-611-002-017-585-740` (field, 611, two, seven, maiden-of-the-seven, jar); the Dholavira board `820-611-388...`; Lothal plaque L-116 `820-611-000`; M-56 seal `840-611-550-060-235-032-877-740` (pair, 611, gate in ...); H-1076 seal `820-002-706-611-740` (two quarters, paṭi, 611, jar); a Dholavira seal `000-611`. Sites Harappa 2, Dholavira 2, Lothal 1, Mohenjo-daro 1. Seals 4 (median face 1,176 mm2), non-seal plaques 2, both opening with the wheel.
Decision: a name part, the name of a ruling house. Not a title: a title follows a name, and the left neighbours are wheel, field, pair, measure, never a name. Not a place: no site holds more than a third of its uses (2 of 6), and the Lothal plaque carries the same two opening signs as the Dholavira board. A name: it is the last name word before the jar on H-1076 and before the king title 388 on the board. Word: kuṭai "umbrella, parasol, canopy" (1663), the royal sunshade standing on its pole, so the name is "Umbrella". Predictions (not a place: 2 of 6 or less at one site, true; not a title: no name on its left, true; wheel on its left twice and king title or jar on its right, true).

### 645: plain X. Sound kuṟi "mark"

Picture: a plain X (Mahadevan 137, 23 uses). 22 uses on 20 objects: seals 6, tablets 5, pots 5 (1.8 expected), rods 2, implements 2, plaques 2; Harappa 11, Mohenjo-daro 8. First 4, middle 13, last 5. Count directly before it 10 of 22 (three, short strokes, five times). Non-seal 16 of 22 (73% against 53%, P 0.05).
Slots across objects: pots `031-645` (one 645), `032-645` (two 645); rod `031-645-645-031`; tablets `003-645-032-590` twice (three 645, two chests); implement `817-002-645-017-898`; seals as a name part after a number (`255-070-741-003-645-740`, `861-368-001-645-285`, `820-003-645-510`); the Dholavira board `850-645-031`. And a fixed frame: Mahadevan sealings 1623 and 2847 open `645-070-741-150-267-840-032` where M-494 opens `255-070-741-150-221-840-032` and M-495 `070-741-150-267-840-032`, so 645 stands where the chief 255 stands.
Decision: a name part (a counted noun inside names, like "three marks"), used as a tally mark on goods; on the board it is a piece of a place name. Word: kuṟi "mark, sign" (1847). Predictions: non-seal 50% or more (73%, true); count before it 40% or more (45%, true); the 255 frame (2 Mahadevan lines, true); counts on pots 1 or 2 (31, 32, true).

## 3. The signboard in full

Sign order (published ten-sign string, reading order): wheel 611 king-title · wheel 850 645 one · wheel wheel 798. (Lipi stores nine signs and records the doubled wheel as one, 821.)

**Sounds:** kāl kuṭai aracu · kāl kaṇ kuṟi oru · kāl kāl maru-

**English:** "The quarter of King Umbrella. The quarter of the Marked Place, number one. Quarter by quarter, the Maru kin."

Word by word: kāl = quarter (the wheel, first in 187 of 244 uses); kuṭai = Umbrella, the royal house (611, section 2); aracu = king (388); kaṇ = place (eye or place, 850); kuṟi = mark (645); oru = one (031, "number one" because the one stands after a place name); kāl kāl = the wheel twice, a doubled word meaning "each quarter" (doubling of a word to say "each" is ordinary in Dravidian); maru- = descendants, kin (798, Tamil maru-makkaḷ).
Checks on it: the third line has siblings, a wheel and the kin sign together on 13 other objects including pot H-1402 `820-798-740` "quarter, kin, house" (`holes_9_extra.py`); the first line's frame wheel + a word + king title is on M-1830 `820-002-388-740` (two quarters, king, house); no verb, no god, no welcome sign, which the board's text-notice reading predicted earlier and still holds. What it says: the gate board names the king whose house governs the town, the quarter the board belongs to by its mark, and the clan that holds every quarter. Not tested beyond this: the tenth sign comes from one printed transcription.

## 4. The new phrase tally

Basis: the 186 phrases of long_texts.md, re-marked with the same rule (reads = every sign valued and no word pair the corpus avoids; partial = an unvalued or lost sign; unread = one unvalued sign alone; nonsense = an avoided pair), the ten new values in memory, and word kinds assigned to them (`holes_7_retally.py`). All 186 are in `retally_phrases_final.csv`.

| | reads | partial | unread | nonsense |
|---|---|---|---|---|
| before | 76 | 73 | 8 | 29 |
| after, the eight + paṭi + taṭi only | **111** | **58** | 8 | **9** |
| after, also counting the earlier counted-pot and "iṟai iṟai" rereads (section 5 of long_texts.md) | **115** | 58 | 8 | **5** |

Movement. Of the 73 partial: 19 read, 54 stay partial, none fell. Of the 29 nonsense: 16 read (strict) or 20 (with the earlier rereads), 4 became partial (K-89, L-190, L-191, M-359, where a count or a name word is still missing), the rest stay. Phrases rescued: 35, of which 21 contain one of the eight (060 in 6, 335 in 6, 711 in 4, 525/527 in 5, 692 in 4, 645 in 2, 611 and the board's doubled wheel in 2, six in all with a board phrase) and 14 turn on paṭi or taṭi alone. The 842 phrases (three) stay partial, because the signs beside it (192, 871, 535, 374) have no sound.
Examples now read: `920-060-741` "in the month, first ward"; `692-060-255-435-690-740` "in the district, the chief of the rod, ... house"; `240-705-033` "High-star: three paṭi"; `550-525-400` "gate-door junior"; `413-575-335-711-033-700` "grain, granary, bin, pot: three cups"; `645-003-820` "mark, three quarters" (mū-kāl, Tamil mukkāl "three-fourths"); `466-706` "n paṭi".
Still nonsense, strict (9): M-494 `255-070-741-150-221`, M-495 `070-741-150-267`, C-40 `095-390`, M-1688 `002-255-435-125` (title before a house word, the order the language avoids), M-10 `061-405`, and the four rereads that the earlier section 5 owns (three counted jars H-131, H-1814, H-1816 and M-623 `176-175`). With the earlier class-slip notes (070 and 095 are name words) the first three move to partial. The 58 partial are now waiting on other signs: 899 (3 phrases), 697, 921, 350, 491, 825, 500, 845, 330 (2 each), the rest one each, and 8 phrases with only a lost sign.
Judgment calls: the board's three phrases are marked reads by hand; the avoided-pair rule counts a wheel followed by a place word as nonsense because it treats the wheel as the seal opener "n quarters", while on the board it is the word "quarter" with no count (all three flagged phrases would read the same way otherwise). If those three are left to the rule (two nonsense, one partial because 821 has no value), strict reads 108, partial 59, nonsense 11.

## 5. What went against, and the rescue

| sign | what went against | number | rescue tried | result |
|---|---|---|---|---|
| 692 teru "street" | place head should not sit with the month | 7 lines against 2.1 | new word nāṭu "district" | second catalogue 6 against 2.24; no touching (0 of 7) |
| 842 tuṇai "helper" | small seal | 1,340 to 2,209 mm2 against 605 | same word, meaning deputy | 3 of 5 with a chief (P 0.030), top 8% of seal sizes; set after seeing the data, five seals, no separate check |
| 525 katavu | 526 and 527 after the gate | 5 of 13, 22 of 59 (Mahadevan 40%) | family test | one word, 5 swap frames; stays as a closing title |
| 525 katavu | name-class before it | 23 of 43 (53%) against 70% | left open | 13 of the 43 stand before unvalued signs, so unsettled |
| 335 kūṭu | house emblem repeats | 0 repeats | test the tablet side | 15 of 21 with the grain header (71% against 1.9%) |
| 060 genitive -iṉ | name on the left; chains | 2 of 217; 2 of 215 | kept alive beside uḷ | splitting observation named, uḷ leads |
| 060 dative, plural, "and" | records, counts on the left, same kind both sides | 81% seals; 4 of 217; 3 of 99 | none | dropped |
| 711 pāṉai | the count after it also belongs to the cup | most lines | two lines with no cup | 2 of 2 tall |
| marks | board's wheel and the avoided-pair rule | 2 phrases | hand override, reason given | see section 4 |

Which predictions were clean: 060, 692 (first word), 525, 335, 711 first tries, 611, 645 were fixed in the docstring before the first run. The 842 second try and the 335 grain-header test (X1) were set after the data they concern had been seen; 692's nāṭu test was set after the Lipi co-occurrence was seen, and run on the second catalogue.
Not paused: every sign has a committed word and at least one prediction that held; none needed three failed ways in.
