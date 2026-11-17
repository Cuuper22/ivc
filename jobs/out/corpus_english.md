# The corpus in English, and the two clashes split

Scripts (all in `work_scripts/`): `clash_common.py`, `clash_335.py`, `clash_527.py` (job 1); `corpus_master.py`, `corpus_build.py`, `corpus_book.py`, `corpus_draw.py` (job 2). Tables: `work_data/clash/335_tests.csv`, `work_data/clash/527_tests.csv`, `work_data/values_master.csv`, `work_data/corpus_english.csv`, `work_data/corpus_draw40.csv`, `work_data/corpus_compare.json`. Book: `CORPUS.md` in the repo root.

Plain words. **Face** = one inscribed side of an object (5,679 in the Lipi catalogue). **Distinct text** = one sign string counted once however many copies. **New texts** = the 1,183 second-catalogue lines with no partner in the first, never used to choose a value. **Base rate** = how often any sign does the thing in question. **P** = how often chance alone gives a result at least that strong; small P points to the word. **Strict / wide** = values promoted on a fact nobody had seen while choosing (strict), or also on facts that had been visible (wide).

## 1. What was found

1. **527 (and 525, 526) is *kāval* "guard". Door is out.** Every test that separates the words came out for the guard and none for the door. In the first catalogue the jar is on the same face 7 of 63 times against 33% for any face (P 6e-5); 527 is the last sign 52 of 63 against 29% (P 1e-18); a count stands beside it 3 of 63 against 24% (P 4e-5); 84% of its faces are seals against 40% (P 1e-12). On new texts, which chose nothing: last sign 7 of 9 against 28% (P 0.003), seal 8 of 9 against 55% (P 0.04), jar 1 of 9, count 0 of 9, all in the guard's direction. Meaning: the sign stands in the jar's place as a class word, a person's office, not a thing. It opens: *kāval* is DEDR 1416, the same root as the keeper signs 151-158 (*kā*), so the office signs now share one dictionary entry.
2. **335 is *ūr* "town". Bin is demoted to the one Harappa grain formula.** 335 has two uses and they split cleanly (section 2.1). Outside the formula (23 distinct texts, six sites) a jar or "child of" follows it 18 times, a grain header never, a cup word once; jar or maka after it is 16 of 26 distinct texts against 9.7% (P 1e-10) and 4 of 6 on new texts against 7.9% (P 5e-4). Meaning: a name part that takes the possessive like a place name. It opens: `575-335` "Fort-town" now reads as a place on the tablets and as a name part on seals with the same word.
3. **Corpus book built.** All 5,679 faces went through the parser and the master table: **2,190 whole, 1,276 part, 2,079 damaged, 134 none.** The strict 1,418 and wide 1,861 of the fourth list reproduce to the face (section 4). `CORPUS.md` is 2,190 whole faces grouped by site and object, plus the 100 commonest part readings.
4. **40 whole faces read by hand: 25 sense, 13 odd, 2 nonsense.** Blamed signs: 904, 060, 900, 861, 752/760, 824, 501, 690/055, 368, 840.

## 2. The two clashes

### 2.1 Sign 335: *ūr* "town" against *kūṭu* "bin" (winner: *ūr*)

What each word predicts that the other does not (written into `clash_335.py` before the first run; note: I had read the first-catalogue profile in the earlier reports, so first-catalogue numbers are not clean; new texts are the clean column and hold only 6 faces with 335):

| test | town says | bin says | first catalogue, distinct texts | new texts |
|---|---|---|---|---|
| K1 count sign right beside | low | high | 4 of 26 (15%) against 25.8%, P 0.16, town | 1 of 6, town (direction) |
| K2 tall-stroke (container) count beside | low | high | 0 of 26 against 9.5%, P 0.074, town | 0 of 6, town (direction) |
| K3 face is a tablet | low | high | 13 of 26 (50%) against 25.8%, P 0.007, bin | 1 of 6, bin (direction) |
| K4 grain header 413 on the face | low | high | 7 of 26 against 0.8%, P 1e-9, bin | 1 of 6 against 0.7%, P 0.04, bin |
| K5 cup / pot / measure word on face | low | high | 7 of 26 against 10.8%, P 0.018, bin | 1 of 6, bin (direction) |
| K6 trade / price / tax word on face | high | low | 2 of 26, no preference | 0 of 6, no preference |
| K7 jar or maka right after | high | low | 16 of 26 (62%) against 9.7%, P 1e-10, town | 4 of 6 (67%) against 7.9%, P 5e-4, town |
| K8 Mohenjo-daro house-mates share it | low | high | 0 pairs against 0.08 expected, town (no house emblem) | not testable |
| K9 Harappa mound F (granary) | low | high | 8 of 29 against 34%, town direction; mound E 12 of 29 against 29% | not testable |
| K10 what fills the slot after 575 | house/place word | container word | house or ward jar 23 against container word 11 (distinct texts, both catalogues): town | included |

What the numbers mean. Bin wins the tablet tests (K3 to K5) and town wins the name tests (K1, K2, K7, K8, K10). The post-hoc role split (K12, flagged post hoc in the script) shows why: the tablet tests all come from one formula. Role G, 335 right after 575: 8 distinct texts, all Harappa tablets, 413 on every one, a cup or measure word on 7. Role N, every other use: 23 distinct texts at Harappa, Mohenjo-daro, Kalibangan, Lothal, Rakhigarhi and Shikarpur, 14 seals, jar or maka right after on 18, grain header 0, cup word 1. So the grain header and cup words belong to the formula, not to 335 itself: any word between 575 and 711 on a grain chit would carry them. What belongs to 335 is what it does everywhere: it is never counted with container strokes (0 of 26), it takes jar or "child of" right after it like a name, it repeats in no house, it stands in the very slot where *kuṭi* "house, town" stands after 575 (23 against 11), and it travels to six sites, which a bin on one granary's chits does not.

Commitment: **one word carries both, and it is *ūr***. The tablet line reads *nel kōṭṭai ūr pāṉai mū nāḻi*, "grain, Fort-town, pot: three cups"; the seal uses read "of [X-]town's house / child of the town". *Kūṭu* "bin" stays as the second word (master table `alt_sound`); the one thing it explains that *ūr* does not is nothing: every bin-side test was a formula effect. Status stays strict (v3 building on); the local DEDR copy has no entry for *ūr*, so its DEDR cell is empty. Did not find a single DEDR entry carrying both "town" and "bin" (searched the local copy).

### 2.2 Sign 527 (+525, 526): *kāval* "guard" against *katavu* "door" (winner: *kāval*)

Predictions are in the docstring of `clash_527.py` (written before the first run; same note: the first-catalogue profile had been read). Family pooled = 525+526+527 (87 faces, 74 distinct texts); 527 alone gives the same directions.

| test | guard says | door says | family, first catalogue (distinct) | family, new texts (9 faces, all 527) |
|---|---|---|---|---|
| G1 jar on the face | low | high | 7 of 74 (9%) against 36%, P 1e-7, guard | 1 of 9 against 27%, P 0.25, guard (direction) |
| G2 last sign of the text | high | low | 58 of 74 (78%) against 24%, P 2e-22, guard | 7 of 9 against 25%, P 0.0014, guard |
| G3 060 or ward jar right after | low | high | 1 of 74 against 3.0%, guard (direction) | 0 of 9, guard (direction) |
| G4 count beside | low | high | 3 of 74 (4%) against 26%, P 8e-7, guard | 0 of 9 against 22%, P 0.11, guard (direction) |
| G5 face is a seal | high | low | 53 of 74 (72%) against 56%, P 0.0045, guard | 8 of 9 against 64%, P 0.11, guard (direction; faces P 0.039) |
| G6 tag / sealing | low | high | 1 of 74, guard (direction) | 1 of 9, guard (direction) |
| G7 sign before the gate is a name part | high | low | 29 of 74 (39%) | 5 of 9 (56%) |

Two honest limits: G7's P values in the table file (1e-54) are not usable, because its base rate is over all signs and is about 0.3%; quote the counts only (a person's name stands before the gate in 39% and 56%). G8 (frames shared with class closers or place words) had only 3 comparison signs of matching frequency and tells nothing; it is in the csv and ignored. G3 shows the door-as-address reading also failed its own cleanest prediction: heads of an address are followed by "in" 159 of 217 times, and 527 family 1 of 74.

What it means. The sign behaves like spear, comb and keeper: it closes the text (78%), takes the place where the jar would be (jar 9% against 36%), is never counted (4%), and sits on seals. A door would be owned, counted and followed by an ending or a ward; it is not. 525 is the tablet drawing (11 of 11 on Harappa tablets, followed by the comb *ciṟ* "junior" 9 of 11), 526 closes (13 of 13), 527 is the seal drawing: the one word *kāval*, three scribal habits. `550-525-400` reads "gate-guard, junior" on the four E-trench ration tablets. *Katavu* stays as second word (`alt_sound`) in the master.

## 3. The master table

`work_data/values_master.csv`: 149 signs. Status: 116 strict, 18 wide, 11 testing, 4 paused. Columns: sign, sound, english, dedr, status, report, alt_sound, alt_english, alt_report, short (the one-word English the corpus builder uses), note.
- Sources: values_v4.csv (the fourth pass) and values_eight.csv (eight signs). Strict = building on with a fresh fact, or a base value; wide = building on with a seen fact, or from the eight-signs report, or 525/526 (same word as 527 by the swap-frame fact).
- Beyond the two clashes, five more signs had two words in the two tables; the higher status wins, a tie goes to the fourth pass: 060 *uḷ* "in" (eight-signs report ran the grammar test; *-iṉ* "of" is alt), 692 *nāṭu* "district" (was paused), 645 *kuṟi* "mark" (alt *kar̤añcu*), 711 *pāṉai* "pot" (alt *vaḷḷam*), 435 *kōl* kept (alt *taṭi*), 705/706 *kalam* kept (alt *paṭi*). Ten signs carry an alt word in all.
- DEDR column: filled for 50 of 149 signs, only where a number written in a report matches an entry whose Tamil words contain the sound in the local DEDR copy, or where a report states it (705/706 = 1305, eight-signs table). The rest are empty on purpose; no number was guessed. 335 *ūr* has none because the local copy lacks the entry; its alt *kūṭu* is 1883 in the alt_report cell.

## 4. Grade totals and how they compare

| grade | faces |
|---|---|
| whole | 2,190 |
| part | 1,276 |
| damaged | 2,079 |
| none | 134 |
| all | 5,679 |

Whole + part + none = 3,600 = the complete faces of the first catalogue; damaged are the other 2,079 (lost sign, unclear sign, or broken edge). Per site is in the key of `CORPUS.md` (Harappa 1,281 whole of 2,717; Mohenjo-daro 645 of 1,923; Lothal 53 of 208; Dholavira 48 of 238; Kalibangan 48 of 212).

Comparison with `sound_list_v4.md` (same rule: complete face, two signs or more, only v4 values), from `corpus_build.py`:

| set | faces | distinct texts |
|---|---|---|
| v4 strict | **1,418** | 608 |
| v4 wide | **1,861** | 931 |
| master strict only | 1,418 | 608 |
| master strict + wide | 1,926 | 971 |
| master strict + wide, one-sign faces included (this is "whole") | 2,190 | |

The strict 1,418 and wide 1,861 reproduce exactly. Our "whole" 2,190 is higher for two reasons, both counted: **264 one-sign faces** (a number, a cup, a lone jar; the fourth list required two signs) and **65 extra faces** (1,926 minus 1,861) that read only because the master adds the eight-signs values and 525/526 (060, 692, 645, 711, the guard drawings). Master strict alone adds nothing to the v4 strict 1,418 at two signs.

## 5. The 40-draw

Rules were finished and tuned on two other random draws (seeds 7 and 11) before this one. The draw: seed 20261117, 40 whole faces from the 2,190 (copies count as often as they occur), printed by `corpus_draw.py`, saved as `work_data/corpus_draw40.csv`. I read each English line as something that seal, tag, tablet or pot would say.

**Tally: 25 sense, 13 odd, 2 nonsense.**

Sense (25): 1 (938.1 "Four cups"), 3, 6, 7, 8, 9, 11, 14, 15, 16, 17, 18, 19, 22, 24, 26, 30, 31, 33, 34, 35, 36, 38, 39, 40. These are counted goods on tablets and pots, "Three keepers/shares/cups", "Junior of the Tax house", "Of the Star-Elder house", the load tag, and "Scabbard-fish-Gate-Guard".

Odd or nonsense, with the sign I think is to blame:
- 2 (280.1) and 25 (1602.1) "two shares: of the High-star-Two months house": **904** "two months" inside a house name.
- 4 (1327.1) "One share; Three.": **861** with a count on each side; the rule did not tie the 3 to the share (builder rule, not a sign).
- 5 (1370.1) **nonsense**, "three ins two houses, junior": **060** "in" used inside a text where it is not an opener's joiner (013-060-032-740-400).
- 10 (3766.1) "Of the Hill child of Field house": **752** child-of rendering (the 503-615-752-740 reading "of the house of the heir of Hill-Field" is fine; my child-of rule garbles it).
- 12 (145.1) "two shares: one King, keeper.": **382** "King" as a name part before the keeper.
- 13 (2480.1) "Second-ward house-Produce-Branch-Star-Servant-Two months-Elder": **806** "produce" and **904** inside one long name.
- 20 (3839.1) "Of the house" on a bangle: **740** alone, a lone jar has nothing to belong to.
- 21 (1138.1) "Three keepers." on a seal: **156** (keeper) counted on a seal.
- 23 (1886.1) "Of the Month-Gem-Branch-Servant house": **900** "month" in a name.
- 27 (1278.1) "Heap two kindreds High-star, chief": **501** "heap" and **405** counted.
- 28 (5576.1) **nonsense**, "Two prices; Goldsmith-Branch-Banner": **824** "price" counted on a seal.
- 29 (694.1) "Of the two pairs house": **840** "pair" counted inside a house.
- 32 (570.2) "Of the Dozen-Chief-Rod-Bound house": **055** "dozen" and **690** "bound" in a name.
- 37 (1180.1) "Hill-Share-Banner": **368** "banner" as an ending that the rule leaves bare.

Pattern: the odd ones are number or measure words standing inside house names (055, 900, 904, 824, 840, 806, 501) and 060 away from an opener. Those are the next signs to look at: they read as goods words, and the parser puts them in the name slot.

## 6. Notes on what the corpus rules do not cover
- Multi-face tablets are read face by face, not as one record.
- Copies are counted once in the book and as many times as they occur in the csv and in the draw.
