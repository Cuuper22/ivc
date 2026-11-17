# Sound list, fourth version: kalam the measure, and the coverage push

Scripts (in `work_scripts/`, run in this order): `sound_v4_common.py` (third-pass loader plus the coverage counter and the gain table), `sound_v4_job1.py` (705/706: measure against ship), `sound_v4_job2.py` (the 25 signs, predictions A, B, C), `sound_v4_job2b.py` (rescue tests), `sound_v4_values.py` (the list and the coverage numbers), `sound_v4_cands.py` (texts that became readable), `sound_v4_readings.py` (READINGS 61-80), `sound_v4_report.py` (this file). Tables: `work_data/sound_v4/`.

Plain words used below:
- **Readable start to finish** (or "reads whole"): every sign on the face is a number, a base value (jar, man, fish, spear, comb, carriers, staff-bearer, tree, elder, cup, load comb) or a value we are **building on**. Counted on the 3,600 complete faces of the first catalogue (Lipi); "distinct texts" counts each different sign string once.
- **Building on / testing / paused**: building on = a prediction made for the word came true and we read with it; testing = no prediction has come true yet, or it could only be checked on data already looked at; paused = three different tries came up empty.
- **New texts**: the 1,183 lines of the second catalogue (Mahadevan 1977) with no partner in the first. They were never used to choose a value, so a prediction that comes true there is a prediction in the full sense.
- **fresh / seen**: fresh = the fact a prediction was checked against had not been printed while the word was chosen. Seen = it had been visible in the sign profiles printed while choosing (top neighbours, object kinds, top sites). A value that came true only on a seen fact is building on in the **wide** list and still testing in the **strict** list; both numbers are given.
- **P** = how often chance alone gives a result at least this strong (P 0.01 = once in a hundred). Small P points to the word being right; P near 1 points the other way. "yes" = right direction with P at or under 0.1.
- **Count after / before**: a number sign (short strokes or tall strokes) right after or before a sign. **Tall strokes** are the container count series, **short strokes** the series for other things.
- **Gain** of a sign: how many complete faces would become readable start to finish if that sign alone got a built-on value (counted, not guessed: faces whose only unvalued sign is this one).
- **DEDR** = Burrow and Emeneau, Dravidian Etymological Dictionary (local copy `work_data/lexicons/dedr/`), entry number. **Tamil Lexicon** = University of Madras Tamil Lexicon (1924-36), read online at dsal.uchicago.edu.

## 1. What was found

1. **705 is *kalam*, the grain measure. One word carries both readings.** Tamil *kalam* is "vessel, ship" (DEDR 1305) and also "a measure of capacity" (Tamil Lexicon p. 778, sense 10, cited from the Tolkāppiyam, the oldest Tamil grammar); the Lexicon also gives *marakkāl* = 8 *paṭi* = 1/12 *kalam* (p. 3082). DEDR 1305 itself lists only vessel, pot, ship; the measure sense is in the Tamil Lexicon. The picture fits the measure exactly: a U-shaped vessel with a stick standing in it is a measuring vessel with its levelling stick. The measure predictions came true hardest on new texts: a count follows 705 in 28 of 64 uses against 14.1% for all signs (P 8e-9), and all 28 of those counts are tall strokes, the container series, against 35% for counts overall (P 1e-13). That points straight at the measure: 705 is counted the way containers are, on texts nobody used to choose it.
2. **Where each use falls.** Every face with 705 or 706 in both catalogues (384 faces) went into a box by its own clues. Measure clues (a count after it, a grain or measure word on the face, a tablet or pot): 243 faces. Ship clues only (the sail 500 after it, a coast or foreign findspot, a trade tag): 30 faces, 14 of them the Lothal tag `705-500-...` (11 copies in the first catalogue, 3 new-text tags). Both: 16. Neither: 95 (mostly seals where 705 stands without a count). Measure wins the corpus about 8 to 1.
3. **The ship stands where it works: Lothal, uncounted, before the sail.** The ship predictions that came true are the ones about the sail and trade: sail 500 after it on new texts 3 of 64 against 0.4% (P 0.002), trade-tag words (dozen, given, sale, fish) on the same new-text face 15 of 66 against 15% (P 0.049), coast and abroad 43 of 384 against 9% (P 0.07). Where 705 is followed by the sail it is never counted. So one word, two uses: counted *kalam* = the measure (everywhere), *kalam pāy* = the ship (the Lothal tags and two Mohenjo-daro seals). The Lothal tag reading 42 stands: "by ship, first ward: one dozen fish; the house's agent". And Lothal also writes the measure: `705-320` *kalam paṭi* (two Lothal tags), `705-575` *kalam kōṭṭai* (two Lothal seals), `705-540` *kalam paṟai* (one): measure words stacked at the port.
4. **Why the count is a fixed three: "three kalam" is a grade written into titles.** On goods objects the count after *kalam* varies (pots: 2, 3, 5; other tablets: 3, 4, 5); on seals it is three 115 times out of 118 (8 of 69 not-three on goods against 3 of 118 on seals, P 0.015). On seals the chief sign 520 follows "three kalam" 54 times out of 172, against 2.0% after any sign, and seals carrying "three kalam" are bigger than seals with the same number of signs (x1.11, n 87, P 0.064). So `705-033-520` *kalam mū vēḷ* is "the three-kalam chief": a rank named by its grain allowance, the way the allowance *paṭi* gives *paṭiyāḷ* "a servant paid in grain" (DEDR 3849). The copper tablets copy it as a fixed formula too (three, 35 of 35).
5. **The coverage push: 1861 of 3,600 faces now read start to finish, up from 1222; 931 distinct texts, up from 477.** That is with every value whose prediction came true on new texts or on a fresh Lipi fact. Counting only values whose fact was fresh: 1418 faces, 608 distinct texts. Split by object: seals 697 faces of 1,540 (was 364; strict 459); goods objects 1164 of 2,060 (was 858; strict 959). On the new texts themselves: 233 of 627 complete new texts read whole (strict 178), up from 134. More than half the complete faces of the first catalogue now read.
6. **22 of the 25 top blockers got a word whose prediction came true (9 of them on fresh facts), and 705/706 came true on fresh facts in job 1.** The fresh ones: *nel* "grain" (413) lies in the Harappa tablet mound E 22 of 44 against 25% (P 0.0003); *turumpu* "threshed heap" (416) and *kutir* "granary bin" (605) lie in mound F, the granary, 15 of 27 and 6 of 9 against 34%; *vēḷāḷaṉ* "cultivator" (137) in mound E 7 of 12 against 25%; *tiṅkaḷ* "month" (900) is counted with short strokes 61 to 6 (things, not containers; P 3e-11); *kūṭumīn* "crate of fish" (226) sits at the coast and abroad 9 of 52 against 9% and takes tall (container) counts 17 to 8; *kāval* "guard" (527) stands where the possessive jar would be (jar on 7 of 63 faces against 33%, P 6e-5), so `550-527` is *vāy kāval* "gate-guard"; *aṭi* "servant" (717) shares its new-text face with a person or title sign 11 of 23 against 16% (P 0.0004); *aracu* (384) stands in the frames of its sister leaves 388/382.
7. **The web paid twice.** (a) *kalam* the measure was chosen for 705 alone, and with it the sign that follows `705-033` 15 times, 923, reads too: `706-033-923-740` on 7 copper tablets reads "three kalam, crescent-horn: of the house". (b) The Lothal measure stack *kalam paṭi* / *kalam kōṭṭai* uses three values chosen in other jobs (320, 575, 540), and the goldsmith reading of 104 (person with the seed-weight *kuṉṟi* at his foot) predicted the gold weight 645 and the seed-weight 480 on the same face: 7 of 27 against 1% (P 2e-8).
8. **Twenty more inscriptions read whole** (READINGS 61-80), all texts that read for the first time in this pass: a 29-copy Harappa store chit, a 10-copy office chit of the "chief staff" keeper, the three-kalam chief, five-kalam copper tablets, ration issues to a bondsman and a cultivator, the granary heir, the gate-guard, millet for sale.

## 2. Job 1 in full: 705/706 measure against ship

Predictions were written into `sound_v4_job1.py` before it ran. "seen in v3" = the same check the third pass already ran.

| test | reading | prediction | outcome | number | P | fact |
|---|---|---|---|---|---|---|
| M1 | measure | new texts: a count follows it | yes | a count right after it 28/64 = 44% against 14.1% (Mu) | 8.2e-09 | fresh |
| M2 | measure | new texts: the count after it is tall strokes | yes | counts after it: tall 28 of 28 (100%) against 35% tall for all counts (Mu) | 1.4e-13 | fresh |
| M3 | measure | new texts: grain/measure words on the same face | direction only | faces with a grain/measure word (Mu) 8/66 = 12% against 9% | 0.29 | fresh |
| M4 | measure | new texts: on miniature tablets, copper tablets, pots | no | faces on ctab/mtab/pot 5/66 = 8% against 21% for all faces, x0.4 (Mu) | 1 | fresh |
| M5 | measure | Lipi: Harappa objects with it lie in mound F (granary area) | no | Harappa objects from mound F 30/90 = 33% against 34% | 0.59 | fresh |
| M6 | measure | both catalogues: count after it varies on goods objects, fixed on seals | yes | count after it is not three: goods objects 8/69 against seals 3/118 [values by kind: ctab: 3x35; mtab: 1x3, 3x18; other: 3x1, 4x1, 5x1; pot: 2x1, 3x1, 5x1; seal: 1x1, 2x2, 3x115; tag: 2x1, 3x6] | 0.015 | fresh |
| S1 | ship | new texts: at Lothal | direction only | faces at Lothal (Mu) 8/66 = 12% against 8% | 0.12 | seen in v3 |
| S2 | ship | both catalogues: coast and abroad | yes | faces at coast/abroad sites (LM) 43/384 = 11% against 9% | 0.068 | fresh |
| S2b | ship | both catalogues: abroad only | no | faces abroad (LM) 1/384 = 0% against 1% | 0.89 | fresh |
| S3 | ship | new texts: sail 500 follows it | yes | next sign in ['500']: 3/64 = 5% against 0.4% (Mu) | 0.0017 | seen in v3 |
| S4 | ship | new texts: on sealings/tags | direction only | faces on tag 17/66 = 26% against 22% for all faces, x1.2 (Mu) | 0.27 | seen in v3 |
| S5 | ship | new texts: trade-tag words on the same face | yes | faces with a trade-tag word (Mu) 15/66 = 23% against 15% | 0.049 | fresh |
| G1 | grade | the chief 520 follows "three kalam" | yes | 520 after 705/706-033: 54/172 = 31% against 2.0% after any sign (LM) | 3.7e-48 | partly seen |
| G2 | grade | seals with "three kalam" are bigger at equal sign count | yes | seal face against seals of the same sign count x1.11 (n 87) | 0.064 | fresh |

G1 and G2 test the fixed three. G1 was partly visible while exploring (the spear after 705-033 showed in a neighbour count). G2 (size) was not.

Where every use falls (faces; L = first catalogue, Mu = new texts):

| | measure only | both | ship only | neither |
|---|---|---|---|---|
| L | 214 | 11 | 26 | 67 |
| Mu | 29 | 5 | 4 | 28 |

The 30 ship-only faces: 11 copies of the Lothal tag `705-500-741-001-055-220-740-090` and 3 new-text Lothal tags `705-500-...`, two Mohenjo-daro seals with 705/706 before the sail (`705-500-741-803-923-740`, `706-500-820-062-151`), and Dholavira and Lothal faces whose only ship clue is the findspot. The "neither" faces are mostly seals where *kalam* stands in a name without a count (`091-705-798`, `615-705-595`, `705-140`).

**The 15 long phrases, read again with *kalam* the measure** (they were nonsense under *kaḷam* "threshing floor"):

| object | signs (reading order) | sound | English | note |
|---|---|---|---|---|
| M-314 | `466-706-760-740` | *(n) kalam maka kuṭi* | n kalam: of the house of the child | the count comes before here, written with the load comb: n kalam-loads |
| K-89 | `…-002-…-705-033-…` | *… iru … kalam mū …* | … two … three kalam … | tag, broken |
| H-2584 | `705-033-095-520` | *kalam mū kōlaṉ vēḷ* | three kalam: the staff-bearer, the chief | the three-kalam grade of a staff-bearer chief |
| M-355 | `360-861-002-235-231-705-033-032-877-740` | *[360] kāṇi iru vēymīn orumīn kalam mū · iru nālkāṇi kuṭi* | holder of two shares, Bamboo-star First-star: three kalam; of the two-four-shares house |  |
| L-190 | `705-500-741-001-055-220-740-090` | *kalam pāy orukuṭi oru paṉṉiru mīn kuṭi āḷ* | by ship, first ward: one dozen fish; the house's agent | uncounted kalam before the sail: the ship |
| H-131 | `…-794-575-595-002-055-706-033-240-233-840-032-740` | *… [794] kōṭṭai paṭṭaṟai iru paṉṉiru kalam mū mīmīn vāḷai iṇai iru kuṭi* | …: great-measure, forge, two; a dozen, three kalam; of the High-star, fish, pair-two house | an inventory under a house |
| H-130 | `717-125-812-595-002-806-231-705-033-845-032-409` | *aṭi vēṭṭuvaṉ [812] paṭṭaṟai iru viḷai orumīn kalam mū cūṭu iru [409]* | the Hunter's servant: [812], forge, two; produce, First-star, three kalam; sheaf-bundles, two; [409] | an open list, no jar |
| H-774, H-1814, H-1816 | `240-705-033-550-525-400` | *mīmīn kalam mū vāy [525] ciṟ* | High-star: three kalam; Gate-[525], junior hand | face 2 is the grain line *nel kōṭṭai ūr vaḷḷam mū nāḻi*: two faces, one grain issue |
| H-1813 | `220-705-033-550-525-400` | *mīn kalam mū vāy [525] ciṟ* | Star: three kalam; Gate-[525], junior hand |  |
| M-1954 | `861-002-798-415-220-705-033-752-031-590-407-740` | *kāṇi iru maru kavar mīn kalam mū maka oru peṭṭi kiḷai kuṭi* | holder of two shares, Descendant of Branch-Star: three kalam; child-of, one; of the Chest-Kindred house |  |
| L-191 | `705-500-741-001-055-220-740-090` | *as L-190* | by ship, first ward: one dozen fish; the house's agent |  |
| M-10 | `455-267-002-806-235-706-033-032-070-061-405` | *[455] [267] iru viḷai vēymīn kalam mū iru ampu kāl kiḷai* | …two; produce, Bamboo-star, three kalam; two arrows, a quarter of the kindred |  |
| M-359 | `632-705-385-388-002-803-235-220-590-405-740` | *pal kalam [385] aracu iru il vēymīn mīn peṭṭi kiḷai kuṭi* | many kalam: [385]-Royal, two; of the house of the Bamboo-star-Star Chest-Kindred house | *pal kalam* "many kalam" with no count: an amount word in the count place |

All 15 phrases now make sense as amounts: "three kalam" after a name is the holder's grade or issue; "n kalam" with the count in front (M-314, written with the load comb) is a real amount. Square brackets = a sign still without a value.

**The 11 Lothal tags** read the same as before: *kalam pāy orukuṭi oru paṉṉiru mīn kuṭi āḷ*, "by ship, first ward: one dozen fish; the house's agent". The ship is the uncounted *kalam* before the sail; nothing on those tags counts it.

## 3. Job 2: the 25 signs that blocked the most faces

Gain = complete Lipi faces that only this sign kept from reading start to finish under the third list (705 blocked 46 faces and 706 blocked 23; they are settled in job 1).

| sign | picture | faces blocked | word | English | what came true (or not) | status now |
|---|---|---|---|---|---|---|
| 240 | Fish with extra whiskers on cheeks | 131 | *mīmīn* | High-star (house crest) | A house ending on new-text seals 7/9 against 77% (direction); B another fish crest follows on new texts 15/58 against 6.5% | building (seen) |
| 233 | Fish with a horizontal line through body | 35 | *vāḷai* | scabbard-fish (a counted fish good; also a crest "Bright-star" vāḷmīn) | A vāḷmīn house ending 6/9 against 77% (against); B seal size x1.07 (direction); C vāḷai: a measure word follows on new texts 9/39 against 3.4% | building (seen) |
| 060 | A single small vertical line, then another vertical line with the bott | 29 | *-iṉ* | of (joiner after an opener) | A sites 17 against 14 (direction); B an opener stands before it on new texts 35/48 against 4.6% | building (seen) |
| 435 | Vertical line with diagonal going down from top right, diagonal going  | 28 | *kōl* | rod, sceptre: mutal kōl "chief staff", an office | taṭi: size x1.00, sites 6 against 8, land words 6/91 against 5% (all against or direction); kōl: carrier or 690 follows on new texts 9/16 against 1.1% | building (seen) |
| 407 | Simple tree with branches at the top | 27 | *kiḷai* | herd, lot (the tally word) | A herd-beast reverse 5/43 against 11% (direction); B house share 10 against 9.6 (direction); B2 last sign on copper tablets 45/77 against 21% (Lipi, seen). Not on new texts at all | testing (seen) |
| 900 | Right parenthesis (perhaps with a backward curve at the bottom) | 24 | *tiṅkaḷ* | month (counted) | A count before it on new texts 10/20 against 15.8%; B short strokes 61 to tall 6 (both catalogues) | building (fresh) |
| 416 | Pitckfork with two stacked heads | 23 | *turumpu* | heap of threshed grain | A Harappa mound F 15/27 against 34%; B opens the text on new texts 4/5; C tall counts 1 of 15 (against) | building (fresh) |
| 413 | Vertical line with small horizontal lines crossing it across the entir | 17 | *nel* | paddy, grain | A Harappa mound E 22/44 against 25%; B a measure word follows on new texts 3/3 | building (fresh) |
| 388 | Upside-down heart symbol with horizontal hatching, with vertical strok | 14 | *aracu* | pipal; royal (house name) | A house share 2 against 1.8 (direction); B jar follows on new texts 5/13 against 10.2% | building (seen) |
| 226 | Fish with four small vertical strokes around the four corners | 12 | *kūṭumīn* | crate of fish | A coast and abroad 9/52 against 9% (P 0.035); B tall counts 17 to short 8 | building (fresh) |
| 384 | Upside-down heart symbol, possibly with vertical stroke coming from bo | 12 | *aracu* | pipal; royal (house name) | A house share 0 against 0.1 (against); C frames of 388/382: 7 against 3 (P 0.054) | building (fresh) |
| 048 | Seven short vertical strokes, bracketed by parentheses | 12 | *er̤uvar* | the Seven (a body of seven) | mūṭai earlier; er̤uvar A frames of 585: 0 (against); B jar after 17/17 (Lipi only; 048 is not on new texts) | testing (seen) |
| 097 | Person with two arms and two legs, bracketed by tall vertical lines | 11 | *aṭimai* | bondsman, servant (a ration receiver) | A Harappa mound E 2/7 (direction); B a count or cup before it on new texts 4/9 against 16.5% | building (seen) |
| 717 | A cat's paw perhaps, two vertical strokes on each side, and four finge | 10 | *aṭi* | foot; servant (aṭiyāṉ) | tāḷ earlier. aṭi A: a person or title sign on the same face on new texts 11/23 against 16%; B seal smaller x1.06 (against) | building (fresh) |
| 832 | Leaf with small vertical stroke inside | 10 | *kaṇ* | eye; at, in (place word) | A sites 6 against 8 (against); B clean: a time/place word before it on new texts 3/25 against 7.2% (direction) | testing (fresh) |
| 790 | Simple leaf or diamond, possibly rotated 45 degrees | 10 | *maṇi* | bead, gem | kaṉ copper went against in v3. maṇi A bead towns 9/69 against 9% (direction); B tags on new texts 9/20 against 22% | building (seen) |
| 382 | Upside-down heart symbol, with vertical stroke coming from bottom of h | 9 | *aracu* | pipal; royal (lineage head) | A frames 3 against 3 (against); B jar after 2/20 (against); B2 maka follows 5/20 against 0.9% (both catalogues) | building (seen) |
| 605 | Tall box with horizontal hatching throughout, possibly a small handle  | 9 | *kutir* | grain bin, granary | A Harappa mound F 6/9 against 34%; B maka follows on new texts 2/3 | building (fresh) |
| 137 | Person with two arms and two legs, small leaf almost like a phallus on | 9 | *vēḷāḷaṉ* | cultivator | A Harappa mound E 7/12 against 25%; B grain/cup on the face 2/19 (against) | building (fresh) |
| 550 | The 'pincer' motif. Right-pointing isocoles triangle on left, left-poi | 9 | *vāy* | gate | A a ward jar on the face on new texts 3/27 against 7% (direction); B 060/527/555/525 follows on new texts 6/23 against 2.0% | building (seen) |
| 923 | Right parenthesis drawn in outline | 9 | *maruppu* | horn of the crescent (a counted thing before the jar) | A a count before it 17/42 against 19% (both catalogues); B month signs on the face 0/48 (against) | building (seen) |
| 877 | Diamond with four small diamonds at each vertex | 9 | *nālkāṇi* | four shares | A house share 1 against 0.3 (direction); B a count follows on new texts 5/12 against 14.1% | building (seen) |
| 104 | Person with a half-height caret coming off the right foot | 8 | *taṭṭāṉ* | goldsmith (person with the seed-weight at his foot) | kuṉṟavaṉ: frames 4 against 3, no-jar 10/26 against 33% (against); taṭṭāṉ: frames of 391 1 against 1 (against), gold/seed weight on the face 7/27 against 1% (both catalogues) | building (seen) |
| 527 | Small box with horizontal hatching, vertical lines coming from top lef | 8 | *kāval* | guard (vāy kāval "gate-guard") | A carries the jar 7/63 against 33%; B ends the text on new texts 3/3 | building (fresh) |
| 831 | Leaf with diagonal-stroke central decoration | 8 | *tiṉai* | Italian millet | A Harappa mound E 1/6 (against); B sale/price/field/grain words on the face 9/23 against 8% (both catalogues) | building (seen) |

Every check run in job 2, in the order run (A = the bold prediction, B = a better test of the same word, B2 = one more better test, C/C2 = a new word):

| stage | sign | word | prediction | outcome | number | P | fact |
|---|---|---|---|---|---|---|---|
| A | 240 | mīmīn | a house crest: names with it take the house ending (jar or jar+man) on new-text seals | direction only | names with it end in jar/jar+man 7/9 = 78% against 77% (Mu seals) | 0.66 | fresh |
| B | 240 | mīmīn | star names compound: on new texts another fish crest follows it | yes | next sign in ['220', '226', '231', '233']...: 15/58 = 26% against 6.5% (Mu) | 3.1e-06 | seen |
| A | 233 | vāḷmīn | a house crest: names with it take the house ending on new-text seals | no | names with it end in jar/jar+man 6/9 = 67% against 77% (Mu seals) | 0.87 | fresh |
| B | 233 | vāḷmīn | a great house: seals with it are bigger than seals with the same number of signs | direction only | seal face against seals of the same sign count: x1.07 (n 115) | 0.26 | fresh |
| C | 233 | vāḷai | a goods word: on new texts a measure word follows it | yes | next sign in ['171', '320', '540', '575']...: 9/39 = 23% against 3.4% (Mu) | 4.6e-06 | seen |
| A | 060 | -iṉ | a grammatical ending: it turns up at more sites than signs of its frequency | direction only | 17 sites against median 14 for 25 signs of similar frequency (LM) | 0.28 | fresh |
| B | 060 | -iṉ | on new texts the sign before it is an opener (month, office, gate, wheel) | yes | prev sign in ['550', '692', '820', '920']: 35/48 = 73% against 4.6% (Mu) | 1.8e-36 | seen |
| A | 435 | taṭi | an office: seals with it are bigger than seals with the same number of signs | no | seal face against seals of the same sign count: x1.00 (n 27) | 0.43 | fresh |
| B | 435 | taṭi | an office of the whole civilisation: more sites than signs of its frequency | no | 6 sites against median 8 for 42 signs of similar frequency (LM) | 0.9 | fresh |
| A | 407 | kiḷai | a herd word: on copper tablets the reverse animal is a herd beast (bull, buffalo, gaur, goat) more than on copper tablets overall | direction only | copper tablets whose reverse animal is a herd beast 5/43 = 12% against 11% | 0.49 | fresh |
| B | 407 | kiḷai | a lot word stands last: house-mates at Mohenjo-daro share it (a house tally) | direction only | same-house pairs 10 against 9.57 (Mohenjo-daro objects, 40 carry it, shuffled within area and 3-ft band) | 0.46 | fresh |
| A | 900 | tiṅkaḷ | months are counted: on new texts a count stands before it | yes | prev sign in ['001', '002', '003', '004']...: 10/20 = 50% against 15.8% (Mu) | 0.00038 | seen |
| B | 900 | tiṅkaḷ | months are counted like things, with short strokes (both catalogues) | yes | counts beside it: tall 6, short 61 (tall share 9% against 47% for all counts; LM) | 2.9e-11 | fresh |
| A | 416 | turumpu | a threshing-floor word: Harappa objects with it lie in mound F (granary, threshing floors) | yes | Harappa objects from area F* 15/27 = 56% against 34% | 0.017 | fresh |
| B | 416 | turumpu | a heading word: on new texts it opens the text | yes | first sign of the text 4/5 = 80% against 29% (Mu) | 0.027 | seen |
| C | 416 | turumpu | grain goes in containers: counts beside it are tall strokes (both catalogues) | no | counts beside it: tall 1, short 14 (tall share 7% against 47% for all counts; LM) | 1 | fresh |
| A | 413 | nel | grain chits: Harappa objects with it lie in mound E (the tablet mound) more than Harappa objects overall | yes | Harappa objects from area E* 22/44 = 50% against 25% | 0.00027 | fresh |
| B | 413 | nel | grain is measured: on new texts a measure word follows | yes | next sign in ['171', '320', '540', '575']...: 3/3 = 100% against 3.4% (Mu) | 3.8e-05 | seen |
| A | 388 | aracu | a house name before the jar: Mohenjo-daro house-mates share it | direction only | same-house pairs 2 against 1.84 (Mohenjo-daro objects, 22 carry it, shuffled within area and 3-ft band) | 0.54 | fresh |
| B | 388 | aracu | a house name: on new texts the jar follows it | yes | next sign in ['740']: 5/13 = 38% against 10.2% (Mu) | 0.007 | seen |
| A | 384 | aracu | a house name: Mohenjo-daro house-mates share it | no | same-house pairs 0 against 0.10 (Mohenjo-daro objects, 7 carry it, shuffled within area and 3-ft band) | 1 | fresh |
| B | 384 | aracu | a house name: on new-text seals names with it take the house ending | nan | too few cases | nan | fresh |
| C | 384 | aracu | the same word as 388: it stands in the frames of 388 and 382 | yes | 7 shared frames with ['382', '388'] against median 3 for 55 signs of the same frequency (LM, distinct texts) | 0.054 | fresh |
| A | 382 | aracu | the same word as 384/388: it stands in their frames | no | 3 shared frames with ['384', '388'] against median 3 for 52 signs of the same frequency (LM, distinct texts) | 0.53 | fresh |
| B | 382 | aracu | a house name: the jar follows it (both catalogues) | no | next sign in ['740']: 2/20 = 10% against 12.4% (LM) | 0.73 | seen |
| A | 226 | kūṭumīn | fish goods travel by water: faces with it sit at the coast and abroad (both catalogues) | yes | faces at Bala-kot/Desalpur/Dholavira/Failaka/Girs (LM) 9/52 = 17% against 9% | 0.035 | fresh |
| B | 226 | kūṭumīn | crates are counted with tall strokes (the container series) | yes | counts beside it: tall 17, short 8 (tall share 68% against 47% for all counts; LM) | 0.025 | seen |
| A | 048 | er̤uvar | the same word as the Seven maidens 585: it stands in the frames of 585 | no | 0 shared frames with ['585'] against median 0 for 62 signs of the same frequency (LM, distinct texts) | 1 | fresh |
| B | 048 | er̤uvar | a group name before the jar: the jar follows it more than chance (both catalogues) | yes | next sign in ['740']: 17/17 = 100% against 12.4% (LM) | 3.8e-16 | seen |
| A | 097 | aṭimai | a ration receiver: Harappa objects with it lie in mound E (ration chits) | direction only | Harappa objects from area E* 2/7 = 29% against 25% | 0.55 | fresh |
| B | 097 | aṭimai | a ration receiver: on new texts a cup or count stands before it | yes | prev sign in ['001', '002', '003', '004']...: 4/9 = 44% against 16.5% (Mu) | 0.046 | seen |
| A | 717 | aṭi | a servant word: on new texts a person or title sign stands on the same face | yes | faces with ['090', '095', '100', '140', '151'] beside it (Mu) 11/23 = 48% against 16% | 0.00037 | fresh |
| B | 717 | aṭi | a servant's seal is small: seals with it are smaller than seals with the same number of signs | no | seal face against seals of the same sign count: x1.06 (n 30) | 0.83 | fresh |
| A | 832 | kaṇ | a grammatical place word: more sites than signs of its frequency | no | 6 sites against median 8 for 43 signs of similar frequency (LM) | 0.81 | fresh |
| B | 832 | kaṇ | on new texts a time or place word stands before it | yes | prev sign in ['335', '503', '615', '832']...: 11/25 = 44% against 8.0% (Mu) | 1.4e-06 | fresh |
| A | 790 | maṇi | beads: faces with it sit at the bead towns (Chanhu-daro, Lothal, Dholavira) | direction only | faces at Chanhu-daro/Dholavira/Lothal (LM) 9/69 = 13% against 9% | 0.19 | fresh |
| B | 790 | maṇi | beads are goods: on new texts it sits on sealings/tags | yes | faces on tag 9/20 = 45% against 22% for all faces, x2.0 (Mu) | 0.018 | seen |
| A | 605 | kutir | a granary word: Harappa objects with it lie in mound F (granary) | yes | Harappa objects from area F* 6/9 = 67% against 34% | 0.046 | fresh |
| B | 605 | kutir | a lineage head: on new texts maka "child of" follows it | yes | next sign in ['760']: 2/3 = 67% against 1.0% (Mu) | 0.00027 | seen |
| A | 137 | vēḷāḷaṉ | a ration receiver: Harappa objects with it lie in mound E | yes | Harappa objects from area E* 7/12 = 58% against 25% | 0.014 | fresh |
| B | 137 | vēḷāḷaṉ | a cultivator gets grain: the cup 700 or a grain word on the same face (both catalogues) | no | faces with ['413', '575', '700', '806'] beside it (LM) 2/19 = 11% against 13% | 0.72 | fresh |
| A | 550 | vāy | the gate of a ward: on new texts a ward jar (741/742/745) stands on the same face | direction only | faces with ['741', '742', '745'] beside it (Mu) 3/27 = 11% against 7% | 0.33 | fresh |
| B | 550 | vāy | a gate word heads an address: on new texts the joiner 060 or the gate-guard 527/555 follows | yes | next sign in ['060', '525', '527', '555']: 6/23 = 26% against 2.0% (Mu) | 4.9e-06 | seen |
| A | 923 | maruppu | a date word after a count: a count stands before it (both catalogues) | yes | prev sign in ['001', '002', '003', '004']...: 17/42 = 40% against 19.0% (LM) | 0.001 | seen |
| B | 923 | maruppu | a date word: it shares a face with the month signs 900/904/920 more than chance (both catalogues) | no | faces with ['900', '904', '920'] beside it (LM) 0/48 = 0% against 6% | 1 | fresh |
| A | 877 | nālkāṇi | a holding: Mohenjo-daro house-mates share it | direction only | same-house pairs 1 against 0.29 (Mohenjo-daro objects, 9 carry it, shuffled within area and 3-ft band) | 0.26 | fresh |
| B | 877 | nālkāṇi | a counted holding: on new texts a count follows it | yes | next sign in ['001', '002', '003', '004']...: 5/12 = 42% against 14.1% (Mu) | 0.018 | seen |
| A | 104 | kuṉṟavaṉ | a person word: it stands in the frames of the plain man 090 and the staff-bearer 095 | direction only | 4 shared frames with ['090', '095'] against median 3 for 34 signs of the same frequency (LM, distinct texts) | 0.49 | fresh |
| B | 104 | kuṉṟavaṉ | a person word: seals with it carry no jar more than chance (a title in the possessive place) | no | faces with the jar (L) 10/26 = 38% against 33% | 0.79 | fresh |
| A | 527 | kāval | a title in the possessive place: faces with it carry the jar less than faces overall | yes | faces with the jar (L) 7/63 = 11% against 33% | 5.8e-05 | fresh |
| B | 527 | kāval | a closing title: on new texts it ends the text | yes | last sign of the text 3/3 = 100% against 29% (Mu) | 0.024 | seen |
| A | 831 | tiṉai | a crop: Harappa objects with it lie in mound E (grain chits) | no | Harappa objects from area E* 1/6 = 17% against 25% | 0.82 | fresh |
| B | 831 | tiṉai | a crop sold and grown: sale, price, field or grain words on the same face (both catalogues) | yes | faces with ['413', '615', '806', '824', '845'] beside it (LM) 9/23 = 39% against 8% | 3e-05 | seen |
| B2 | 435 | taṭi | a land measuring rod: land words (field, hill, sheaves, quarter) on the same face (both catalogues) | direction only | faces with ['061', '503', '615', '845'] beside it (LM) 6/91 = 7% against 5% | 0.34 | fresh |
| C | 435 | kōl | an office held by a person: on new texts a carrier or the bound-word 690 follows it | yes | next sign in ['154', '156', '690']: 9/16 = 56% against 1.1% (Mu) | 2.9e-14 | seen |
| B2 | 407 | kiḷai | a tally word closes the record: on copper tablets it is the last sign more than other copper-tablet signs | yes | last sign on copper tablets 45/77 = 58% against 21% for all copper-tablet sign places | 5.5e-13 | seen |
| B2 | 382 | aracu | a lineage head: maka "child of" follows it (both catalogues) | yes | next sign in ['760']: 5/20 = 25% against 0.9% (LM) | 8.3e-07 | seen |
| C | 104 | taṭṭāṉ | a goldsmith works with the smith: 104 stands in the frames of the smith 391 | no | 1 shared frames with ['391'] against median 1 for 163 signs of the same frequency (LM, distinct texts) | 0.55 | fresh |
| C2 | 104 | taṭṭāṉ | a goldsmith weighs gold: the gold weight 645 or seed-weight 480 on the same face (both catalogues) | yes | faces with ['480', '645'] beside it (LM) 7/27 = 26% against 1% | 1.9e-08 | seen |
| B | 832 | kaṇ | clean rerun: on new texts a time or place word (not 832 itself) stands before it | direction only | prev sign in ['335', '503', '615', '900']...: 3/25 = 12% against 7.2% (Mu) | 0.27 | fresh |

## 4. How much reads now

| list | object group | faces read whole | of | distinct texts | of | objects |
|---|---|---|---|---|---|---|
| third list | all | 1222 | 3600 | 477 | 2162 | 1052 |
| third list | seals | 364 | 1540 | 284 | 1419 | 358 |
| third list | goods | 858 | 2060 | 229 | 823 | 694 |
| fourth list, strict (fresh-based only) | all | 1418 | 3600 | 608 | 2162 | 1206 |
| fourth list, strict (fresh-based only) | seals | 459 | 1540 | 371 | 1419 | 452 |
| fourth list, strict (fresh-based only) | goods | 959 | 2060 | 277 | 823 | 754 |
| fourth list, wide | all | 1861 | 3600 | 931 | 2162 | 1572 |
| fourth list, wide | seals | 697 | 1540 | 598 | 1419 | 687 |
| fourth list, wide | goods | 1164 | 2060 | 383 | 823 | 885 |
| fourth list incl. testing | all | 2018 | 3600 | 1018 | 2162 | 1711 |
| fourth list incl. testing | seals | 749 | 1540 | 649 | 1419 | 737 |
| fourth list incl. testing | goods | 1269 | 2060 | 421 | 823 | 974 |

New texts (second catalogue, no Lipi partner, complete lines): 134 of 627 read whole under the third list; 178 under the fourth strict list; 233 under the fourth wide list (seals 71 / 94 / 125 of 346; goods 63 / 84 / 108 of 281). 454 distinct Lipi texts read whole for the first time in this pass (131 under the strict list); `work_data/sound_v4/reading_candidates.csv`.

## 5. The whole list (98 values)

82 building on, 11 testing, 5 paused (third list: 58 / 17 / 19 of 94). Strict list (only fresh facts promote): 69 building on, 24 testing, 5 paused. "basis" = fresh or seen for values decided in this pass. Base values (numbers, jar, man, fish, spear, comb, carriers, staff-bearer, tree, elder, cup, load comb) are not listed.

### Building on

| sign | picture | sound | English | before (v3) | basis | evidence |
|---|---|---|---|---|---|---|
| 055 | Four small vertical strokes above the same, above the same | *paṉṉiru* | dozen | building |  | A: on sealings/tags on new texts 14/31 against 22%; the fish follows it 4/40 against 3.1% |
| 060 | A single small vertical line, then another vertical line with the bott | *-iṉ* | of (joiner after an opener) | new | seen | A sites 17 against 14 (direction); B an opener stands before it on new texts 35/48 against 4.6% |
| 061 | Simple lambda but reversed horizontally, and the leg may not be quite  | *kāl* | quarter | building |  | A: copper tablets on new texts 1/10 (direction); B: a count before it on new texts 4/10 against 15.8% |
| 070 | A single vertical line, with two person arms | *ampu* | arrow | building |  |  |
| 091 | Two simple persons standing side by side | *iruvar* | the pair, partners | building |  |  |
| 095 | Person with short stick | *kōlaṉ* | staff-bearer | building |  |  |
| 097 | Person with two arms and two legs, bracketed by tall vertical lines | *aṭimai* | bondsman, servant (a ration receiver) | paused | seen | A Harappa mound E 2/7 (direction); B a count or cup before it on new texts 4/9 against 16.5% |
| 104 | Person with a half-height caret coming off the right foot | *taṭṭāṉ* | goldsmith (person with the seed-weight at his foot) | testing | seen | kuṉṟavaṉ: frames 4 against 3, no-jar 10/26 against 33% (against); taṭṭāṉ: frames of 391 1 against 1 (against), gold/seed weight on the face 7/27 against 1% (both catalogues) |
| 125 | Person with bow and arrow | *vēṭṭuvaṉ* | Hunter (clan) | building |  |  |
| 137 | Person with two arms and two legs, small leaf almost like a phallus on | *vēḷāḷaṉ* | cultivator | new | fresh | A Harappa mound E 7/12 against 25%; B grain/cup on the face 2/19 (against) |
| 140 | Person with round breasts and one raised arm | *ammai* | lady | building |  | A: opens the text on new texts 11/17 against 29% |
| 171 | Capital 'T' with a small leaf oriented vertically attached to both sid | *niṟai* | weight, full measure | building |  | A: a count after it on new texts 3/7 against 14.1% |
| 175 | Person sitting with bent knees, no small tangent lines coming off the  | *iṟai* | tax | building |  | A: miniature tablets on new texts 2/4 against 10% |
| 176 | Person sitting with bent knees, four small tangent lines coming off th | *iṟai* | tax, levy | building |  |  |
| 226 | Fish with four small vertical strokes around the four corners | *kūṭumīn* | crate of fish | paused | fresh | A coast and abroad 9/52 against 9% (P 0.035); B tall counts 17 to short 8 |
| 231 | Fish with a small vertical stroke in the body | *orumīn* | First-star | building |  |  |
| 233 | Fish with a horizontal line through body | *vāḷai* | scabbard-fish (a counted fish good; also a crest "Bright-star" vāḷmīn) | paused | seen | A vāḷmīn house ending 6/9 against 77% (against); B seal size x1.07 (direction); C vāḷai: a measure word follows on new texts 9/39 against 3.4% |
| 235 | Fish with a caret shaped hat | *vēymīn* | Bamboo-star (Punarvasu) | building |  |  |
| 240 | Fish with extra whiskers on cheeks | *mīmīn* | High-star (house crest) | testing | seen | A house ending on new-text seals 7/9 against 77% (direction); B another fish crest follows on new texts 15/58 against 6.5% |
| 255 | Unknown asymmetric animal? Perhaps a fish with asymmetric fins and leg | *mutal* | chief, first | building |  |  |
| 320 | (shape not described) | *paṭi* | ration measure, daily allowance | building |  | NEW WORD. A: the month sign 920 follows it on new texts 5/7 against 0.7% |
| 335 | M with the bottom of the legs connected by a horizontal line, and vert | *ūr* | town | building |  | NEW WORD (C). puṭṭi failed (A 1/6 tablets, B 2/6 with a number); ūr: jar or maka follows it on new texts 3/6 against 11.2% |
| 368 | Vertical stroke with a triangular wing attached near the middle | *koṭi* | banner (of a line) | building |  |  |
| 382 | Upside-down heart symbol, with vertical stroke coming from bottom of h | *aracu* | pipal; royal (lineage head) | paused | seen | A frames 3 against 3 (against); B jar after 2/20 (against); B2 maka follows 5/20 against 0.9% (both catalogues) |
| 384 | Upside-down heart symbol, possibly with vertical stroke coming from bo | *aracu* | pipal; royal (house name) | paused | fresh | A house share 0 against 0.1 (against); C frames of 388/382: 7 against 3 (P 0.054) |
| 388 | Upside-down heart symbol with horizontal hatching, with vertical strok | *aracu* | pipal; royal (house name) | paused | seen | A house share 2 against 1.8 (direction); B jar follows on new texts 5/13 against 10.2% |
| 405 | Simple tree with branches at the top | *kiḷai* | kindred | building |  |  |
| 413 | Vertical line with small horizontal lines crossing it across the entir | *nel* | paddy, grain | testing | fresh | A Harappa mound E 22/44 against 25%; B a measure word follows on new texts 3/3 |
| 415 | Pitchfork with tines | *kavar* | branch (of a line) | building |  |  |
| 416 | Pitckfork with two stacked heads | *turumpu* | heap of threshed grain | paused | fresh | A Harappa mound F 15/27 against 34%; B opens the text on new texts 4/5; C tall counts 1 of 15 (against) |
| 435 | Vertical line with diagonal going down from top right, diagonal going  | *kōl* | rod, sceptre: mutal kōl "chief staff", an office | paused | seen | taṭi: size x1.00, sites 6 against 8, land words 6/91 against 5% (all against or direction); kōl: carrier or 690 follows on new texts 9/16 against 1.1% |
| 440 | Rectangle, but with bottom line missing, and bottom-half of left line  | *koḷ* | received, bought | building |  | A against: pots on new texts 1/19 against 7%; B: Harappa on new texts 10/19 against 34% |
| 455 | Three triangles, one large isocoles pointing right on left, two small  | *ampu* | arrow | building |  |  |
| 463 | (shape not described) | *mukkōṭu* | Three-peaks | building |  |  |
| 480 | Tall, slightly narrow caret (mountain motif) | *kuṉṟi* | seed-weight | building |  |  |
| 482 | Tall caret drawn in outline, with diamond inscribed at the point | *kōṭukāṇi* | hill share | building |  |  |
| 500 | Tall triangle with vertical divider, either isocolese or more horn-sha | *pāy* | sail (ship) | building |  | NEW WORD for a building value. A: Lothal on new texts 8/12 against 8% |
| 501 | (shape not described) | *kumi* | heap, stock | building |  |  |
| 503 | Tall isoceles triangle with horizontal stripes | *malai* | hill | building |  | A: copper tablets on new texts 3/19 against 4% |
| 527 | Small box with horizontal hatching, vertical lines coming from top lef | *kāval* | guard (vāy kāval "gate-guard") | paused | fresh | A carries the jar 7/63 against 33%; B ends the text on new texts 3/3 |
| 530 | A 'Bowtie' motif, but without the vertical line connecting the right p | *paṟai* | proclamation | building |  |  |
| 540 | A 'Bowtie' motif. Or, an 'X' with vertical line connecting the left po | *paṟai* | drum; a rice measure | building |  | MEANING CHANGED to the measure (DEDR 4032). A: pots on new texts 2/7 against 7% |
| 550 | The 'pincer' motif. Right-pointing isocoles triangle on left, left-poi | *vāy* | gate | paused | seen | A a ward jar on the face on new texts 3/27 against 7% (direction); B 060/527/555/525 follows on new texts 6/23 against 2.0% |
| 555 | The 'pincer' motif. Right-pointing isocoles triangle on left, left-poi | *vāy* | gate | building |  |  |
| 575 | Trapezoid with no bottom line, small box resting on the top middle | *kōṭṭai* | great grain measure | building |  | A: a count before it on new texts 6/14 against 15.8% |
| 585 | (shape not described) | *kaṉṉi?* | maiden (of the Seven) | building |  |  |
| 590 | Square at bottom with vertical bar coming off top middle | *peṭṭi* | chest | building |  |  |
| 595 | Box with vertical stroke off top center, horizontal striping | *paṭṭaṟai* | forge, smithy | building |  | NEW WORD (C). peṭṭi: A against (counts short 19, tall 1), B copper on new texts 12/27 against 4%; paṭṭaṟai: with smith/copper/weight signs on new texts 4 against 1.4 |
| 605 | Tall box with horizontal hatching throughout, possibly a small handle  | *kutir* | grain bin, granary | new | fresh | A Harappa mound F 6/9 against 34%; B maka follows on new texts 2/3 |
| 615 | A grid of x by y cells | *vayal* | field | building |  | A: copper tablets on new texts 16/86 against 4% |
| 617 | (shape not described) | *ūḻiyaṉ* | (king's) servant | building |  | A: carries the jar 13/75 against 33% (a title in the possessive place) |
| 630 | Rectangle, taller than wide, with vertical strokes for teeth inside on | *pal* | many | building |  | A against: a number on the same object 13 against 20.2; B: frames of 632, 6 against 2 |
| 632 | Rectangle, taller than wide, with vertical strokes for teeth inside on | *pal* | many | building |  |  |
| 636 | Rectangle, taller than wide, with vertical strokes for teeth inside on | *pal* | many | building |  | A: frames of 630, 4 against 0 |
| 679 | An 'X' with a 'table' hat | *kaṭṭil* | seat, throne | building |  |  |
| 690 | Two nested greater-than symbols, touching two nested less-than symbols | *piṇai* | bound, allied | building |  | A: jar follows it on new texts 10/20 against 10.2% |
| 705 | U with a long vertical stroke inserted into the gap of U | *kalam* | grain measure (a kalam); ship where it stands uncounted before the sail 500 | testing | fresh | JOB 1. measure: count after it on new texts 28/64 against 14.1% (P 8e-9), tall 28 of 28 (P 1e-13); count varies on goods, fixed three on seals (P 0.015). ship: sail after it 3/64 (P 0.002); coast and abroad 43/384 against 9% (P 0.07) |
| 706 | U with a long vertical stroke inserted into the gap of U | *kalam* | grain measure (variant of 705) | paused | fresh | JOB 1, with 705 (the second catalogue merges 706 into 705); 706 takes three after it 45 of 46 |
| 717 | A cat's paw perhaps, two vertical strokes on each side, and four finge | *aṭi* | foot; servant (aṭiyāṉ) | testing | fresh | tāḷ earlier. aṭi A: a person or title sign on the same face on new texts 11/23 against 16%; B seal smaller x1.06 (against) |
| 741 | Classic jar symbol with two horizontal handles at the top of each arm  | *orukuṭi* | first ward | building |  |  |
| 742 | Classic jar symbol with two horizontal handles at the top of each arm  | *irukuṭi* | second ward | building |  |  |
| 745 | Classic jar symbol with two horizontal handles at the top of each arm  | *mukuṭi* | third ward | building |  |  |
| 752 | U with decorated branching at top | *maka* | child of | building |  |  |
| 760 | U with decorated branching at top | *maka* | child of | building |  | A: jar follows it on new texts 25/29 against 10.2% |
| 790 | Simple leaf or diamond, possibly rotated 45 degrees | *maṇi* | bead, gem | testing | seen | kaṉ copper went against in v3. maṇi A bead towns 9/69 against 9% (direction); B tags on new texts 9/20 against 22% |
| 798 | Leaf with 'pincers' coming off the right, possibly with small stroke l | *maru-* | descendant, clan member | building |  |  |
| 803 | Leaf with tree at bottom | *il* | house | building |  | A: a fish crest follows it on new texts 6/22 against 7.8% |
| 806 | Leaf with tree at bottom | *viḷai* | produce, ripened crop | building |  | NEW WORD for the crop. A: a load-carrier follows it on new texts 5/25 against 1.4% |
| 817 | Diamond or leaf shape with a small diamond attached to the top | *kāṇi* | share, holding | building |  |  |
| 820 | Wheel with 6 spokes with even angles | *kāl* | quarter-share | building |  |  |
| 824 | (shape not described) | *vilai* | price | building |  | NEW WORD. A: Harappa objects from mound E 11/23 against 25% |
| 831 | Leaf with diagonal-stroke central decoration | *tiṉai* | Italian millet | new | seen | A Harappa mound E 1/6 (against); B sale/price/field/grain words on the face 9/23 against 8% (both catalogues) |
| 840 | Two vertical leaves, slightly overlapping | *iṇai* | pair | building |  | A: two tall strokes follow it on new texts 7/16 against 1.7%. Second reading vaḷai "bangle" (Lipi bangles x7.9, seen) |
| 845 | Two overlapping leaves with diagonal hatches across the three midsecti | *cūṭu* | bundle of sheaves | building |  | NEW WORD. A: copper tablets on new texts 3/9 against 4% |
| 861 | Diamond or leaf shape with a small diamond attached to the top | *kāṇi* | share, holding (a "hand") | building |  |  |
| 877 | Diamond with four small diamonds at each vertex | *nālkāṇi* | four shares | testing | seen | A house share 1 against 0.3 (direction); B a count follows on new texts 5/12 against 14.1% |
| 890 | Right facing bow, i.e. a vertical stroke with a right-parenthesis full | *koṭu* | given | building |  | NEW SIGN. A: sealings/tags on new texts 7/9 against 22% |
| 892 | Bow and arrow | *vil* | sale, price | building |  |  |
| 900 | Right parenthesis (perhaps with a backward curve at the bottom) | *tiṅkaḷ* | month (counted) | paused | fresh | A count before it on new texts 10/20 against 15.8%; B short strokes 61 to tall 6 (both catalogues) |
| 904 | Two slightly nested right parentheses | *irutiṅkaḷ* | two months | building |  |  |
| 920 | Right parenthesis with small leaf at middle | *tiṅkaḷ?* | month (head of a date formula) | building |  |  |
| 923 | Right parenthesis drawn in outline | *maruppu* | horn of the crescent (a counted thing before the jar) | paused | seen | A a count before it 17/42 against 19% (both catalogues); B month signs on the face 0/48 (against) |

### Testing

| sign | picture | sound | English | before (v3) | basis | evidence |
|---|---|---|---|---|---|---|
| 048 | Seven short vertical strokes, bracketed by parentheses | *er̤uvar* | the Seven (a body of seven) | testing | seen | mūṭai earlier; er̤uvar A frames of 585: 0 (against); B jar after 17/17 (Lipi only; 048 is not on new texts) |
| 165 | A left and right paren connected only at the top, with the left paren  | *poḻutu* | sun, day | testing |  | A: with the crescent 900 on one face 10 of 33 against 0.6 (fact seen in Lipi while choosing) |
| 391 | Three pronged tree with caret hat | *kollaṉ* | smith | testing |  | NEW SIGN. A copper on new texts 1/3 (P 0.13); B both catalogues 4/13 x6.9 (Lipi tools seen) |
| 407 | Simple tree with branches at the top | *kiḷai* | herd, lot (the tally word) | testing | seen | A herd-beast reverse 5/43 against 11% (direction); B house share 10 against 9.6 (direction); B2 last sign on copper tablets 45/77 against 21% (Lipi, seen). Not on new texts at all |
| 417 | Two pitchforks with tines, facing each other vertically | *kā* | carrying pole (pole-load) | testing |  | NEW SIGN. too few for a frame test; a count before it 8/8 (seen) |
| 460 | Three tall, thin isoceles triangles | *mukkōṭu* | Three-peaks | testing |  | A: jar after it 2/11 against 10.2%; B jar or spear 2/11 (direction) |
| 645 | An 'X' with no decoration | *kar̤añcu* | a gold weight | testing |  | kaṭṭu: A count before 1/4 (direction), B with a number 2/6 against 35% (against); kar̤añcu: too few new texts with a sign after it |
| 711 | U with X going from side to side near the bottom | *vaḷḷam* | grain measure | testing |  | NEW WORD. A against: E trench 11 2/21 against 10%; B: cup on the same object 12 of 21 against 2.5 (seen) |
| 832 | Leaf with small vertical stroke inside | *kaṇ* | eye; at, in (place word) | paused | fresh | A sites 6 against 8 (against); B clean: a time/place word before it on new texts 3/25 against 7.2% (direction) |
| 838 | (shape not described) | *eḷumpu ~ eḷ* | bone ~ sesame | testing |  | A against: rods on new texts 0/5; B rods both catalogues 4/24 x22 (Lipi seen) |
| 850 | Simple leaf or diamond, possibly rotated 45 degrees | *kaṇ ~ kaṉ* | eye ~ copper | testing |  | A copper on new texts 2/13 against 4% (P 0.11); B both catalogues 20/69 x6.5 (Lipi seen) |

### Paused

| sign | picture | sound | English | before (v3) | basis | evidence |
|---|---|---|---|---|---|---|
| 167 | The 'headphones' motif. Upside down U with small cirles on each end | *?* | tablet word | paused |  | poli: mound F 3/9 against 34%, copies 10/15 against 69%; kā: carrier frames 1 against 2. Lead: closes kaḷam (705/706) tablets only |
| 236 | Fish with a caret shaped hat, caged by four small vertical strokes | *vēykūṭumīn* | Bamboo-star cluster | paused |  |  |
| 350 | Horizontal line with multiple lines out the top, lines or U out the bo | *?* | name front | paused |  |  |
| 495 | (shape not described) | *kompu* | branch | paused |  |  |
| 692 | An X but drawn in outline | *?* | office (opening) | paused |  |  |

## 6. What went against, and the rescue tried

- **705 as a record-object word**: on new texts 705 sits on tablets and pots 5 of 66 against 21% (P 0.999), and Harappa objects with it are not in the granary mound F (30 of 90 against 34%). Grain words on the same new-text face: 8 of 66 against 9% (direction only). The measure is read off the counts, not the object kind: on the new texts it lives on seals and tags. Rescue: the fixed-three grade (G1, G2) explains why a measure word sits on seals.
- **705 abroad**: 1 face of 384 at a foreign site (against 1%). The ship reading gets no foreign support; it stands at Lothal.
- **240 *mīmīn***: house ending on new-text seals 7 of 9 against 77% (no excess). Rescued by B on new texts (another fish crest follows, 15 of 58 against 6.5%), a fact visible while choosing: building on in the wide list only.
- **233**: *vāḷmīn* "Bright-star" as a crest went against (house ending 6 of 9 against 77%; size x1.07). New word *vāḷai* "scabbard-fish", a counted fish good: a measure word follows it on new texts 9 of 39 against 3.4% (seen). It now reads as goods in `806-233-384-740` and `798-240-233-320-920-740-400`.
- **435 *taṭi* "staff"**: bigger seals x1.00, sites 6 against 8, land words 6 of 91 against 5%: three misses. New word *kōl* "rod, sceptre": the carrier or 690 follows on new texts 9 of 16 against 1.1% (seen). `255-435` *mutal kōl* "chief staff" is an office.
- **407 *kiḷai***: herd-beast reverse 5 of 43 against 11%, house share 10 against 9.6: direction only. Better test: last sign on copper tablets 45 of 77 against 21% (Lipi, seen). 407 has no new texts at all (the crosswalk does not carry it), so it stays testing; it blocks 27 faces.
- **388/384/382 *aracu***: house sharing went against for 384 and 382 (0 against 0.1; frames 3 against 3; jar after 382 2 of 20). Rescue: 384 stands in the frames of its sisters (7 against 3, fresh); 382 takes *maka* after it 5 of 20 against 0.9% (seen). All three building on as one word.
- **048 *er̤uvar* "the Seven"**: no shared frames with the Seven Maidens 585 (0). The jar follows it 17 of 17, but only in the first catalogue; 048 is not on new texts. Testing.
- **832 *kaṇ* "at, in"**: sites 6 against 8 (against); a time or place word before it on new texts 3 of 25 against 7.2% (direction). The first run counted 832 standing after 832 as a hit (11 of 25); the clean rerun is the number given. Testing.
- **104**: *kuṉṟavaṉ* "hillman" went against (frames 4 against 3; jar 10 of 26 against 33%), the goldsmith *taṭṭāṉ* did not stand in the smith's frames (1 against 1) but predicted the weights on its face (7 of 27 against 1%, seen). Building on in the wide list.
- **Smaller misses inside a sign that came true elsewhere**: 416 counted with tall strokes 1 of 15 (a heap is counted as a thing, not a container); 137 with grain/cup on its face 2 of 19; 717 servant seal smaller x1.06 (it is not smaller); 923 with month signs 0 of 48 (so *maruppu* is the crescent horn as a counted thing, not a date); 550 with a ward jar 3 of 27 (direction); 790 at bead towns 9 of 69 against 9% (direction); 831 in mound E 1 of 6; 060 sites 17 against 14 (direction).

## 7. What it opens next

- **The grade system.** "Three kalam" before the chief is a grain grade. Next: every count after a measure word on seals (705, 711, 320) as a grade, against seal size and closing title; and whether *kalam* grades sit with the fish-star houses (the great houses).
- **167**, an arch with a ring at each foot, closes only *kalam* tablets (`705-167`, `167-705-031` at Chanhu-daro) and is still paused: with *kalam* now a measure it should be a measuring or issuing word. It is the next sign to give a word.
- **407** blocks 27 faces and cannot be tested on new texts: build its crosswalk entry from the second catalogue's tree signs and rerun.
- **The Harappa mounds now sort words**: grain *nel*, cultivator, ration chits in mound E; threshed heap, granary bin in mound F. A findspot map of every built-on value at Harappa is the next cheap test bed.
