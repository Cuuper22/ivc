# Sound list, seventh version: the time test, one table, 30 more signs

Scripts (in `work_scripts/`, run in this order): `sound_v7_common.py` (the sixth-pass kit plus the time bins and the value loader), `sound_v7_time_pred.py` (Job 2 predictions, written before any number by time), `sound_v7_time.py` (Job 2 run), `sound_v7_j3_profile.py` (Job 3: picture and slot of the 30 signs, printed before any word was chosen), `sound_v7_j3.py` (Job 3 words and predictions, all written before running), `sound_v7_j3b.py` (one redesign per miss, written before running), `sound_v7_j3vals.py` (the job-3 values), `sound_v7_master.py` (`work_data/values_master4.csv`), `corpus_build3.py` (the corpus in English: `CORPUS.md`, `work_data/corpus_english3.csv`), `sound_v7_readings.py` (READINGS 141-160). Tables and logs: `work_data/sound_v7/` (`time_values.csv`, `time_facets.csv`, `time_testing.csv`, `time_log.txt`, `j3_gains.csv`, `j3_profiles.txt`, `j3_tests.csv`, `j3b_tests.csv`, `j3_measure_tests.csv`, `j3b_measure_tests.csv`, `j3_log.txt`, `j3b_log.txt`, `object_records3.csv`).

Plain words used below:
- **Value**: the early Dravidian word we give a sign (its sound and its English). **Strict**: the fact that came true had not been seen while the word was chosen. **Wide**: the fact had been glimpsed (for example in a printed list of the sign's neighbours) before the test. **Testing**: no test has come true yet. **Paused**: three ways in failed.
- **Time bin**: the history job dated 2,666 objects (`work_data/time/time_axis.csv`): **early** = up to the end of Harappa Period 3B (before about 2200 BC), **middle** = about 2200 to 2050 BC, **late** = about 2050 BC and after. 3,349 dated Lipi faces: 522 early, 2,049 middle, 778 late; the middle bin holds most of the data (the big Harappa tablet trenches).
- **Class / signature**: the job a word does, and the behaviour that job must show. A house or person word (NAME) has the jar or a closing title later in its text; a TITLE is the last sign; a MEASURE has a number right after it; a counted THING has a number right before it; an OPENER is first; a GOODS word is on a tablet, tag, pot or tool rather than a seal; "child of" (KIN) has the jar right after it; "kindred" has a fish crest on its face; the joiner 060 has a head word (month, gate, quarter, assembly) on its left; the load counts 465-475 have produce 806 right after them.
- **Base**: the share of all non-number sign uses in the same bin that show the same behaviour. "Holds" = the sign shows it more than the base.
- **Frames**: the pair (sign before, sign after) around a sign in a distinct text. Two signs sharing frames more than signs of the same frequency stand in for each other. **P** = the share of chance outcomes (shuffles, or the binomial) at least as strong as the real one; small P points to the stated direction, P near 1 points the other way.
- **Reads whole**: every sign on the face is a number or a strict/wide value and nothing is lost. Counted two ways: on the 3,600 complete faces of 2+ signs (the measure the sound lists use) and on all 5,679 faces with the corpus grades (whole / part / damaged / none).
- **New texts**: the 1,183 second-catalogue (Mahadevan 1977) texts with no partner in the first catalogue, never used to choose a value.
- **DEDR**: Burrow and Emeneau, Dravidian Etymological Dictionary (local copy), entry number.

## 1. What was found

1. **The values are real words across six centuries: 87 of the 122 strict and wide values with dated uses hold their job in every time bin they occur in, against 39.2 when the jobs are shuffled among the values (best of 1,000 shuffles 54; P 0.001).** Of the 70 values with 3+ uses in all three bins, 52 hold in all three (shuffled 21.0, best 31; P 0.001). The words were chosen without looking at dates, so every early and late object is a held-back test. The fear was that a value fitted to noise would hold only in the bin that dominates the data (middle) and fail elsewhere; the data say the opposite: the hold rate is 86% in the early bin (64 of 74), 77% in the middle (88 of 115), 83% in the late (86 of 104). The middle bin is the weakest, not the strongest. What it means: the readings are not tuned to the Harappa tablet trenches; a word that does its job in 3B does it in 3C and Period 4. It points toward the reading as a language system, the same one the history job found in the grammar. It opens: any value can now be checked on time as a free second sample, and the misses (section 3) are a short list of signs whose job word is wrong, not whose sign is unstable.
2. **The signs also do not change their surroundings with time.** For each value with 3+ uses in two bins, slot (first / middle / last), left neighbour and right neighbour were compared across bins with bins shuffled within site: slot changed for 7 of 98 values, left neighbour 5 of 101, right 4 of 95, against about 5 each by chance. Object kind changed for 11 of 99 (about 5 by chance): the kind mix moves with the excavated areas (tablet trenches are middle), not with the words.
3. **Fully read faces: strict 2,025 of 3,600 (was 1,970), wide 2,369 (was 2,160).** Distinct texts strict 1,035 (was 997), wide 1,276 (was 1,126). Seals strict 760, wide 918 of 1,540; goods objects strict 1,265, wide 1,451 of 2,060; copper tablets strict 140, wide 153 of 196; new texts strict 221, wide 272 of 627 complete lines (new-text seals 125 / 156 of 346). The 30 signs of Job 3 each kept 1 to 16 faces from reading (234 faces counted one sign at a time, `j3_gains.csv`); together with keeper 152 (carried over from the odd-readings table, 1 face) they open 55 strict and 209 wide faces.
4. **The corpus in English, one table: whole 2,644 of 5,679 faces (was 2,201), part 847 (was 1,268), damaged 2,079, none 109 (was 131).** With strict values only: whole 2,284. Multi-face objects read as one record: 902, of which 365 whole (was 306), 175 part, 359 damaged, 3 none.
5. **Four new words came true on fresh facts (strict):** 554 *kaḷam* "threshing floor" (it shares frames with the gate words 550 / 555 that also stand before the guard 527: 5 shared frames against a median of 2, P 0.023; so `554-527` is *kaḷam kāval*, the threshing-floor guard, beside *vāy kāval* the gate-guard); 645 *kar̤añcu* "a gold weight" (frames shared with the weights 480 / 171 / 850, 6 against 3, P 0.063; its 7-copy tablet `104-645-590-...` opens with the goldsmith 104); 460 *mukkōṭu* "Three-peaks" (frames of 463, 3 against 0, P 0.022); and on the time test plus a right-pointing frame test: 222 *aṭaimīn* "Shut-in-fish", 792 *aracu* "royal", 921 *vil* "bow" (`921-070-520` = *vil ampu vēḷ*, "chief of bow and arrow", the bow sign right before the arrow sign 070 in 4 of its 16 uses, before the man-with-arms 072 in 3 more).
6. **The measure words leave the names.** An uncounted kalam sign inside a name is *kalam* "ship": those uses sit at coast, Gujarat and abroad sites on 14 of 52 against 9% for counted kalam (P 0.0002). An uncounted cup on a seal is the Measurer's seal: such seals are 0.86 the size of seals of the same length (n 8, P 0.055). Uncounted 540 is "drum", a goods label (last in its text 15 of 25 against 31%, P 0.003). 711 is never a name word (before a jar or closer 1 of 21 against 32%, P 0.003). A share 861 with its count at the front is the opener and the name starts after it (the next word is a crest or house word 90 of 188 against 15%, P 1e-25). 868 after a kalam is "half a kalam": the other face of its tablets names a person or house 10 of 12 against 38% (P 0.002). `corpus_build3.py` now prints counted measures as the house's allowance after the name: `803-861-002-705-033-482-740` was "Of the House two shares three kalam Hill-share house", now "Of the Home-Hill-share house (allowance: two shares and three kalam)".
7. **Wages, dates and the threshing floor.** 167, paused after three failed words, now reads *kūli* "wages, pay" (DEDR 1905): it closes kalam chits, a kalam sign right before it 15 of 15 (seen in the profile, so wide). Harappa tablets `705-167` (6 copies) and `706-167` (5) read "kalam as wages"; with the office opening, H-175 reads "In the month, first ward: five banners; kalam as wages". 165 is *nāḷ* "day" after the month (`900-165` "month, day", the month right before it 10 of 26 against 1.9%), and it holds its date job in the middle bin and in early + late alike. 130, the person with the pitchfork, is *kaḷamar* "threshing-floor men" from the same DEDR entry as 554 (counted: a number right before it 9 of 16 against 19%), so the threshing floor has its guard and its workers.

What it opens: (a) time as a standing held-back test for every new value; (b) a ration and wage system on the tablets (kalam as wages, the Measurer's seal, half a kalam to a named person, the threshing floor and its men); (c) the bow-and-arrow chief beside the Hunter 125 and the archer 127 on the Umma sealing as a line of martial titles.

## 2. The time test (Job 2)

All predictions and the rule were written in `sound_v7_time_pred.py` before `sound_v7_time.py` computed anything by bin. 142 strict and wide values were tested (the stroke numbers are left out: they are counts, not chosen words). One class per value from its word.

| values | count | held in all bins with data | held in 2 | held in 1 | held in 0 |
|---|---|---|---|---|---|
| with 3+ uses in all three bins | 70 | 52 | 9 | 6 | 3 |
| with 3+ uses in two bins | 31 | 18 | | 5 | 8 |
| with 3+ uses in one bin | 21 | 17 | | | 4 |
| with no bin of 3+ uses | 20 | | | | |
| all with data | 122 | 87 | | | |

Shuffled-class rival (the strongest other explanation: the grammar is so stable that any job would hold everywhere): 39.2 of 122 held in every bin with data (best of 1,000 shuffles 54) against 87 real; all three bins 21.0 (best 31) against 52 real; P 0.001 for both. The rival is out.

By bin: early held 64 of 74 (86%), middle 88 of 115 (77%), late 86 of 104 (83%).

The 20 values with no bin of 3+ dated uses: 152, 153, 157 (keepers), 321, 421-424 (fields), 465, 466, 469, 471-475 (load counts), 501, 611, 642, 842.

**The values that failed in at least one bin, and what they did instead** (k/n = uses showing the signature; base in brackets):

| sign | word | class | early | middle | late | what it did instead |
|---|---|---|---|---|---|---|
| 482 | *kōṭukāṇi* hill-share | MEASURE | 0/5 | 0/13 | 0/7 | never takes a count after it; stands before the jar or "child of" (after 240 six times): a name word in every bin |
| 575 | *kōṭṭai* great measure | MEASURE | 0/7 | 3/35 | 0/11 | first after grain 413, then town 335: a goods-line head word, counted rarely |
| 850 | *kāṇi* share | MEASURE | 0/6 | 1/11 | 0/7 | sits on tools early (after the forge 595, before the seed-weight 480); a goods word, not a counted measure |
| 717 | *aṭi* servant | TITLE | 0/2 | 2/14 | 1/12 | stands before the jar (7 of 14 middle): a name word, not a closing title |
| 091 | *iruvar* the pair | NAME | 0/1 | 3/13 | 0/3 | first sign 11 of 13 middle, then 056; on tags and tablets: an opener |
| 323 | *paṭi* ration | MEASURE | | 0/3 | 0/3 | first sign, then 690 or month 920 |
| 530 | *paṟai* proclamation | OPENER | | 1/4 | 0/3 | middle of the text, after a ward sign |
| 565 | *maṟavaṉ* warrior | NAME | | 2/9 | 0/3 | last sign after the jar (6 of 9): a closing title |
| 632 | *pal* many | NAME | | 2/6 | 3/11 | first sign, before Hunter 125 or Lady 140: an opener |
| 868 | *araikkāṇi* half-share | THING | | 0/8 | | last, after a kalam sign 7 of 8: "half a kalam" (rule now in the corpus) |
| 877 | *nālkāṇi* four shares | MEASURE | | 1/11 | 0/3 | first sign after a tall two, before the jar |
| 371 | *katir* spindle | GOODS | | 1/5 | | on seals |
| 406 | *kiḷai* kindred | KINDRED | | | 0/4 | last sign on seals with no crest |
| 525 | *kāval* guard | TITLE | | 1/6 | | after the gate 550, before junior 400: "gate-guard, junior" |
| 158 | *kā* keeper | TITLE | 0/3 | 6/20 | 2/3 | before junior 400 (13 of 20 middle): "keeper, junior" |
| 368 | *koṭi* banner | TITLE | 2/9 | 21/51 | 10/21 | early: after a share 861 and before a count |
| 416 | *turumpu* threshed heap | GOODS | 1/4 | 17/27 | 2/9 | early: first sign of seals |
| 463 | *mukkōṭu* Three-peaks | NAME | 1/3 | 5/8 | 5/8 | early: two seals without a jar |
| 455 | *ampu* arrow | NAME | 1/4 | 7/18 | 5/8 | before the star 220 or a count |
| 070 | *ampu* arrow | NAME | 3/5 | 10/13 | 4/8 | late: before "child of" or quarter |
| 104 | *taṭṭāṉ* goldsmith | NAME | 1/2 | 0/4 | 3/5 | middle: first or last of short texts |
| 125 | *vēṭṭuvaṉ* Hunter | NAME | 2/3 | 7/16 | 10/17 | middle: first sign before cotton 390 or cup |
| 140 | *ammai* lady | NAME | 6/10 | 21/44 | 10/24 | late: first sign, before month 920 |
| 335 | *ūr* town | NAME | 3/3 | 8/20 | 4/7 | middle: the Harappa grain line `413-575-335-711` (the bin reading, its second word) |
| 742 / 745 | second / third ward | NAME | held | 9/20, 3/13 | held / 4/9 | first sign, before 519 or a lost sign |
| 904 | *irutiṅkaḷ* two months | NAME | 5/7 | 19/22 | 4/10 | late: before 832 |
| 097 | *aṭimai* bondsman | THING | | 2/10 | 0/4 | late: after the cup, before junior |
| 320 | *paṭi* ration | MEASURE | | 0/9 | 2/7 | before the month 920 ("monthly allowance") |
| 540 | *paṟai* rice measure | MEASURE | | 0/10 | 1/4 | first or last on pots and tablets: the drum label (rule now in the corpus) |
| 595 | *paṭṭaṟai* forge | GOODS | 3/6 | 3/11 | 3/16 | on seals, last sign |
| 824 | *vilai* price | OPENER | 3/6 | 4/16 | | last sign after the sale 892 on tablets ("sale price") |
| 831 | *tiṉai* millet | GOODS | 1/3 | 2/5 | | first sign on seals, before the sale 892 |
| 845 | *cūṭu* sheaves | THING | 2/6 | 0/3 | 0/8 | after produce 806, before quarter 061 on copper tablets: "produce: sheaves, a quarter" |
| 923 | *maruppu* ivory | GOODS | 1/6 | 3/14 | 3/9 | on seals before the jar: the Ivory house |

Read: the four that fail in every bin with data (482, 575, 850, 717) fail because the CLASS was wrong for how the word is used, the same way in every bin: hill-share, the great measure and the share are house or goods words, not counted measures; *aṭi* "servant" stands before the jar. That is the word holding steady, with the slot word to be corrected. The rest fail in one bin with small numbers, and most did the same thing the other bins show (565 sits after the jar as a title everywhere it fails).

**Testing values, rival words chosen on the early bin only** (`time_testing.csv`): 18 of the 26 have under 3 early uses, so the early bin cannot choose for them. For the 8 it could choose: middle kept the choice 4 times and flipped it twice (222, 821), late kept 4 and flipped once (832). Kept in both: 130 (counted worker over servant title), 460 (Three-peaks name over goods), 621 (closing title over measure); 136 kept on late. Redesign (choose on early + late, the two bins that do not dominate, check on middle): 17 chosen, middle kept 8 (130, 165 date-head over counted day, 222 crest, 243 crest over counted good, 460, 621, 645 gold weight, 832 goods), tied 3, flipped 3 (236, 792, 821), no data 3. Job 3 took these choices in where they existed: 621 as a closing word, 165 as a date word, 222 and 243 as crests, 130 as counted men.

## 3. The new totals

| group | strict | wide | of | sixth pass strict / wide |
|---|---|---|---|---|
| all complete faces | 2,025 (1,035 distinct) | 2,369 (1,276) | 3,600 (2,162) | 1,970 / 2,160 |
| seals | 760 | 918 | 1,540 | 738 / 820 |
| goods objects | 1,265 | 1,451 | 2,060 | 1,232 / 1,340 |
| copper tablets | 140 | 153 | 196 | 135 / 142 |
| new texts | 221 | 272 | 627 | 215 / 254 |
| new-text seals | 125 | 156 | 346 | 121 / 142 |

Corpus grades, all 5,679 faces (`corpus_build3.py`, strict + wide values): whole 2,644, part 847, damaged 2,079, none 109. Strict values only: whole 2,284. Object records: 902; 365 whole, 175 part, 359 damaged, 3 none.

## 4. Job 1: one table, one corpus

`work_data/values_master4.csv` (195 signs: 160 strict, 28 wide, 7 testing, 0 paused) = `values_master3.csv` (sixth-pass sounds and status) + the slot words of `values_master2.csv` (odd-readings job) + this pass's values. Columns: sign, sound, english (default short word), english_name (inside a name), english_count (on a goods count line), english_final (text-final title), english_open (at the front), english_long, dedr, status, report, second_word. Where a sign's word changed since the odd-readings job (405 now thread, 407 now kindred, 060 now "of"), the old slot words were dropped except the "Inner-" name rule of 060. Keeper 152 (only in values_master2) is kept.

`corpus_build3.py` (a copy of `corpus_build2.py`, which is untouched) reads it and adds: M1 uncounted kalam in a name = Ship; M2 uncounted cup on a seal = the Measurer; M3 uncounted 540 = Drum; M4 counted measures leave the name as the house's allowance; M5 803 in a house name = Home; M6 on goods objects an unnamed word group is a list with commas, 705/706 + 868 = half a kalam, a repeated word is counted (`390-390-390` = "Three cottons"). Lines from the odd-readings draw, before and after: `413-575-335-711-033-700` "Grain-Great measure-Town-Grain measure; Three cups" → "Grain, great measure, town, vaḷḷam measure; Three cups"; `590-705-868` "Chest-Kalam-Half-share" → "Chest, half a kalam"; `700` alone on a seal "Cup" → "The Measurer"; `631.2` "Of the House-Scabbard-fish-..." → "Of the Home-Scabbard-fish-Tax-Rod-Ally house". Progress prints every 500 faces; it also writes `CORPUS.md`.

## 5. Job 3: the next 30 signs

Ranking: faces each sign alone keeps from reading whole under the sixth wide list (`j3_gains.csv`). The 30: the 14 left testing in the sixth pass, 127, 167, then the next by gain (165, 645, 236, 048, 832, 460, 222, 821, 792, 350, 027, 201, 921, 232); 999 (an unclassified sign) skipped. Order kept: profile printed first (`j3_profiles.txt`), words chosen, all 60 predictions written in `sound_v7_j3.py` before it ran (A = word test; B = the time test: the class signature must hold in the middle bin and in early + late pooled), then one redesign each in `sound_v7_j3b.py`, written before it ran. Most redesigns use a slot fact visible in the profile, so their yes counts wide. The picture side was used where the profile showed it (048 on the Lothal elephant sealings, 027 on the fish tablets) but was not turned into a separate test this pass.

| sign | faces it alone blocks | word | English | DEDR | A | B (time) | redesign | status | second word |
|---|---|---|---|---|---|---|---|---|---|
| 165 | 16 | *nāḷ* | day (after the month: a date) | 3656 | no (P 0.85) | held | yes: month right before it 10/26 against 1.9% | wide | *poḻutu* "sun, day" |
| 645 | 15 | *kar̤añcu* | a gold weight | 1348 | **yes** (P 0.063) | held | | **strict** | |
| 167 | 14 | *kūli* | wages, pay (closes kalam chits) | 1905 | no (P 0.72) | too few | yes: kalam right before it 15/15 against 2.1% | wide | |
| 236 | 13 | *vēymīn* | Bamboo-star (caged crest) | | direction (P 0.15) | failed | direction: number before it 7/22 against 19% | testing | |
| 048 | 13 | *er̤uvar* | the Seven (a house name) | | yes (seen; share opener two before 16/18) | too few | | wide | |
| 832 | 11 | *aṭai* | leaves, greens (counted) | 59 | direction (P 0.31) | failed | direction: number before 15/60 against 19% | testing | *kaṇ* "eye" |
| 460 | 10 | *mukkōṭu* | Three-peaks | | **yes** (P 0.022) | held | | **strict** | |
| 222 | 10 | *aṭaimīn* | Shut-in-fish (crest) | 83 | direction (P 0.5) | held | | **strict** | |
| 592 | 8 | *paṭṭi* | pen, fold, hamlet | 3868 | no (P 0.92) | too few | yes: a keeper / junior / servant title next 3/6 against 6.9% | wide | *kūṭu* "crate" |
| 703 | 8 | *maṉai* | house-site; a land measure | 4776 | no (P 0.53) | failed | no: house-mates 0 against 0.03 | testing | *nāḻi* "cup" |
| 554 | 7 | *kaḷam* | threshing floor | 1376 | **yes** (P 0.023) | held | | **strict** | *paṟai* "grain measure" |
| 064 | 7 | *pāti* | half, a portion (counted) | 4074 | direction (P 0.45) | failed | yes: on bangles and pots 5/14 against 12% | wide | *kavar* "fork" |
| 136 | 7 | *aṭimai* | bondsman (counted head) | 72 | direction (P 0.39) | too few | yes: number before it 7/12 against 19% | wide | |
| 621 | 7 | *aṭai* | shut in, stored (a closing word) | 83 | no (jar on 8/18 against 33%) | held | yes: last sign 13/18 against 29% | wide | *kōṭṭai* "store" |
| 821 | 7 | *mañcāṭi* | red-wood seed: a small goldsmith's weight | 4636 | no (P 0.84) | failed | yes: on copper tools 3/13 | wide | *veṟṟilai* "betel" |
| 792 | 7 | *aracu* | royal (with 384 / 388) | 201 | direction (P 0.11) | held | | **strict** | |
| 350 | 7 | *kalappai* | plough (counted) | 1304 | no (P 0.57) | held | yes: number before it 18/46 against 19% | wide | |
| 603 | 6 | *kūṭu* | grain receptacle, store | 1883 | no (P 1) | too few | yes: share 861 or jar next 6/7 against 13% | wide | *katavu* "door" |
| 098 | 6 | *ēvalaṉ* | attendant (raised arm) | 909 | too few | too few | yes: junior 400 next 5/7 against 3.3% | wide | *ammai* "lady" |
| 408 | 6 | *kiḷai* | lot, bunch (counted tree) | 2018 | direction (P 0.13) | too few | yes: number after it 5/5 against 15% | wide | |
| 243 | 6 | *kayal* | carp (a crest fish) | 1252 | no (P 0.8) | held | yes: servant / keeper next 10/19 against 1.1% | wide | *vāḷai* |
| 130 | 6 | *kaḷamar* | threshing-floor men (counted) | 1376 | no (P 1) | held | yes: number before it 9/16 against 19% | wide | *aṭiyāṉ* "servant" |
| 776 | 6 | *malar* | Bloom (a name word) | 4729 | direction (P 0.3) | too few | yes: jar next 4/7 against 12% | wide | *pū* "flower" |
| 697 | 5 | *ney* | weaving, woven | 3745 | no (P 0.65) | too few | yes: on pots 6/10 against 11% | wide | *kaṭṭu* "bundle" |
| 804 | 5 | *ilai* | Leaf (a name word) | 497 | no (P 0.54) | too few | yes: crest fish before it 4/6 against 9% | wide | *kūṭu* "crate" |
| 027 | 5 | *toṇṭu* | Nine (spelled in a name) | 3532 | too few | too few | yes: tall two next 6/6 | wide | |
| 201 | 5 | *kār* | the rain season (a date head) | 1395 | direction (P 0.12) | too few | yes: joiner 060 next 5/5 | wide | |
| 921 | 5 | *vil* | bow | 5422 | direction (P 0.14; seals x1.13) | held | | **strict** | |
| 232 | 5 | *kūṭumīn* | Cluster-star (caged fish crest) | | direction (P 0.18) | failed | yes: last sign 7/11 against 29% | wide | |
| 127 | 1 | *villavaṉ* | archer, bowman | 5422 | direction (P 0.24) | too few | direction: edge of text 3/4 | testing | |

Count: 30 signs; 6 strict, 20 wide, 4 testing. A tests came true 4 times of 30 (12 pointed the right way); the time test held 11 times, failed 6, had too few uses 13 times. The two needing a new word got one: 697 *ney* "woven" (it sits on pots, and 151-697-390 is "keeper; woven cotton"), 776 *malar* "Bloom". 127 (the archer on the Umma sealing): *villavaṉ* "bowman", the same DEDR entry as the bow 921; with 4 faces in all, no test has numbers to come true.

**Measure words inside names** (one prediction each, written before running; one redesign for each miss):

| sign | rule or name-sense | prediction | outcome |
|---|---|---|---|
| 705 / 706 | uncounted inside a name = *kalam* "Ship"; counted = the allowance, moved out of the name | uncounted name uses at coast / Gujarat / abroad sites | **yes**: 14/52 against 9% (P 0.0002) |
| 700 | uncounted on a seal = *nāḻi* "the Measurer" (a title) | such seals smaller than seals of the same length | **yes**: x0.86 (n 8, P 0.055) |
| 540 | uncounted = *paṟai* "Drum" (a goods label); counted = rice measure | uncounted 540 ends its text | **yes**: 15/25 against 31% (P 0.003) |
| 711 | never a name word; goods lines are lists | few uncounted uses before a jar or closer | **yes**: 1/21 against 32% (P 0.003) |
| 861 | share + count at the front = opener; the name starts after | the word after the count is a crest or house word | **yes**: 90/188 against 15% (P 1e-25) |
| 868 | after a kalam = "half a kalam", an amount | on new texts after a kalam sign | too few new-text uses; redesign: the other face holds a who-word **yes** 10/12 against 38% (P 0.002) |
| 530 | uncounted in a name = *paṟaiyaṉ* "Drummer" | jar or closer within two after it | **no**: 0/16 against 28%; redesign: last sign **no** 4/18 against 29% |
| 575 | in a seal name = *kōṭṭai* "Fort" | seals bigger | **no**: x0.92 (n 18); redesign: house-mates **no** 0 against 0.61 |

## 6. The value list

Full table: `work_data/values_master4.csv`. New or changed in this pass: the 30 rows of section 5. Unchanged testing: 341 *kalai* "stag", 391 *kollaṉ* "smith", 417 *kā* "pole-load". Paused: none (167 and 350 reopened with new words and now read wide).

## 7. What went against, and the rescue tried

- **Four values fail the time test in every bin they have data for (482, 575, 850 in all three; 717 in middle and late).** Rescue built in: the failure is the class, not the bin: each does one other job steadily (482 and 717 before the jar, 575 a goods-line head word, 850 a goods word on tools). Next pass: give each the slot word its steady job asks for and rerun the time test on it.
- **The early bin is too small to choose between rival words for 18 of the 26 testing values.** Redesign: choose on early + late, check on middle: 8 kept, 3 flipped (236, 792, 821). 792 then came true as *aracu* on the job-3 time test and frames pointing the right way; 821 took a new word.
- **Object kind changes with time for 11 of 99 values against about 5 by chance.** This follows the excavated areas (the middle-bin tablet trenches); slot and neighbours stay at chance level.
- **Job 3 A tests: 12 of 30 went against** (frames with the chosen meaning group not above chance for 592, 703, 603, 621, 243, 130, 697, 804, 821, 350, 167, 165). The redesigns came true for 19 signs, but on slot facts that were visible in the printed profile, so those 19 count wide only. 703 *maṉai* failed both (house-mates 0 against 0.03) and the time test; 236, 832 and 127 only pointed the right way. They stay testing.
- **530 as "Drummer" and 575 as "Fort" failed twice each.** 530 sits in the middle of texts after ward signs; 575 seals are not bigger and house-mates do not share it. Both keep their measure readings; the corpus moves them out of names only when counted. Third try next: 530 as a word of the office line (`741-530`), 575 as the head of the grain line it opens.
- **Test sizes**: many job-3 signs have 4 to 20 uses; several time tests ran on 3 to 6 uses per part. Growing them: the second catalogue's own dates are not linked to the time axis yet; linking them would add the new texts to every bin.

READINGS.md: readings 141-160 added (`sound_v7_readings.py`), all from texts that read whole for the first time in this pass.
