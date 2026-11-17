# The language question by machine, second run: blind pictures, machine classes, homonyms kept apart

## What was found

**The Dravidian lean went away.** With pictures from blind describers, jobs from the machine's ten sign classes, and dictionaries that keep same-spelled words apart, no language family clears the bar fixed in advance, in either picture variant. The first test's lean (Dravidian cells beating outside nouns and scrambled sounds: 10 of 96, against 2 of 48 Indo-Aryan, 1 of 60 Munda, 1 of 36 Sumerian) shrank to **3 of 96 Dravidian** cells, against 2 of 60 Munda, 1 of 48 Indo-Aryan (0 with 3of3 pictures), 0 of 36 Sumerian, 0 of 24 Akkadian and Burushaski, and 2 of 24 Elamite (one cell counted twice, 3of3 pictures only). This came with a much bigger test: 172 units from 235 signs (first test: 63 units from 149 signs), and ten classes instead of a 111-of-149 "name" job.

**The single combined number per family (mean z-score against scrambled sounds over every dictionary cell) is at chance for every family.** Primary variant (3of3 + 2of3 pictures): Dravidian -0.20 (shuffle P 0.82), Munda -0.04 (0.53), Indo-Aryan -0.56 (0.97), Sumerian -0.06 (0.55), Akkadian -0.34 (0.66), Elamite +0.31 (0.16), Burushaski -0.38 (0.79). The bar was P below 0.007 (0.05 shared over seven families). Not one family points. Read plainly: in no candidate language do the names of the pictured things sound like words for their sign's slot (house, chief, clan, measure, goods) more than that language's own words would with sounds dealt at random.

**Right class against wrong class for the same picture: a positive that turned out to be the control's own tilt.** The new control 4 (same picture, a class it does not take) gave Dravidian z +2.35 (P 0.0005), Munda +0.94 (P 0.001), Sumerian +1.85 (P 0.0015). The strongest rival explanation was tested once: the classes a picture does not take are mostly the rare classes, and rare classes carry fewer keyword words in every dictionary (in DEDR Tamil, wide lists, 0.6% of words carry a "closer" keyword against 4.4% for the person/number class). With each unit's share measured against the dictionary's own rate for that class (`lang_m2_c4check.py`, same draws), the Dravidian edge vanishes in all 6 cells (P 0.66 to 0.98); one Munda cell (medium sound distance, narrow keywords: P 0.0005 against control 4, 0.022 against control 1) and one Akkadian cell (strict, wide: 0.014 / 0.025) stay. Two of 42 cells in one variant is what chance gives.

**Sign swaps: no language points.** 108 pairs of differently drawn things replace each other in two or more otherwise identical texts (3of3 + 2of3 pictures; 49 with 3of3 only). Dravidian picture names sound alike in 40 / 89 / 108 of the 108 (strict / medium / loose) against 32.0 / 84.5 / 105.4 for random sign pairs (P 0.054 / 0.17 / 0.064) and 39.4 / 89.4 / 106.9 with the pictures dealt among the swap signs (P 0.49 / 0.61 / 0.34). With 3of3 pictures: 20 / 42 / 49 of 49 against 18.8 / 41.8 / 48.8 random (P 0.42 / 0.55 / 0.82). No other family beats either swap control either.

**Step 8 did not run:** no family cleared the bar, so no candidate or decoy list was written (`lang_m2_candidates.py` checks the summary and stops).

**One thing the run measured about the controls that matters for every future rebus test.** In Dravidian the real picture words' sound-alikes carry slot keywords LESS often than scrambled sounds do (pooled family against control 3: P 0.74 to 1.0 in all 6 primary-variant share cells). Real sound-alikes of "man", "fish", "jar" are more often words of related meaning (in DEDR Tamil the strict sound-alikes of the man word include *kir̤avaṉ* "owner, master, husband" and *aṇṇaṉ* "elder brother", other person words under separate entries) than random words are. A language's sound and meaning cluster through derivation, and scrambling breaks that. So "beats scrambled sounds" is a hard bar that a true language would also struggle to pass with these dictionaries, and it pushes every family down equally.

Rescue plan, from what limited this run: (1) score against cross-language cognate sets, so that the same root split across entries is one word (DEDR "Cf." links, Turner's numbered cross-references); (2) a control 3 that keeps derivational families together (deal whole DEDR cross-reference clusters, not entries); (3) narrow the units to the 26 closing and title signs where the slot meaning is measured best (the closer class has the lowest keyword density of the ten, so a real pun there would stand out most); (4) full Munda and Proto-Munda dictionaries (Santali and Mundari print no homonym numbers, so their strict match is still empty).

## Words used in this report

- **Picture noun**: the thing a sign's drawing shows, as named by at least two of three blind describers (`work_data/pictures/pictures_blind.csv`). **3of3** = all three named it; **2of3** = two did.
- **Machine class**: the class the 10-state hidden-state model gave the sign from sign order alone (`work_data/frame/classes.csv`, column hmm10), with the eight moves the frame report found backed by likelihood (621, 161, 527, 241 to the after-jar title class; 824, 880, 545, 091 to the openers). The ten classes: opener (front word), slot after an opener, front of a name (crest), number or person sign that starts a name or count, measure and box, what follows a measure, counted goods, back of a name, closer, title after the jar.
- **Unit**: signs with the same picture nouns and the same machine class count as one test.
- **Picture word**: a dictionary entry whose gloss names the thing in its first 3 words. **Sound-alike**: a word of a DIFFERENT entry within the sound distance, not itself glossed as the thing.
- **Keyword** (slot meaning): a word among the first 5 of a sound-alike's gloss from the class's list (closer: house, belonging, property, own, owner, home; title after the jar: chief, lord, servant, master, keeper, guard, ruler, headman; front of a name: clan, lineage, star, emblem, family, tribe; opener: number, share, office, place, city, town; counted goods: grain, crop, goods, cattle, cloth, load; full lists, narrow and wide, in `lang_m2_common.py`). Same lists for every language (German copies for Elamite).
- **Share** (graded score): for each unit, the share of its picture words' sound-alikes that carry its class keyword, summed over units. **Hits**: units with at least one such sound-alike.
- **Sound distance**: strict = same spelling once accents and vowel length are dropped; medium = same consonants in order; loose = consonants one apart.
- **Control 1 (C1)**: classes dealt at random among all units (2,000 times). **C2**: each picture noun swapped for a different outside drawable noun (water, rope, dog, ...; 127 of them; 2,000 times). **C3**: each dictionary's sound forms dealt at random among its entries, an entry handing its whole list of forms to another entry with as many rows (500 times). **C3row**: the first test's version, forms dealt among single rows (reported, not used in the bar). **C4**: each unit keeps its picture and gets a class that picture does not take (2,000 times).
- **P**: share of control runs scoring at least the real score. Small P = the real score is above what the control gives.
- **z-score**: (real score minus the control's mean) divided by the control's spread. 0 = what the control gives; +2 = well above it.
- **Z3 / Z1 / Z4**: the mean z-score over all of a family's dictionary cells (6 per dictionary, share score) against C3 / C1 / C4; its P comes from computing the same mean for every control run.

## How it was built (all rules in the header of `work_scripts/lang_m2_common.py`, written before the full run)

1. Dictionaries (`lang_m2_lexicons.py` -> `/tmp/lang_m2/lex/`, rebuilt by rerunning; sizes in `work_data/lang_m2/lex_sizes.csv`). **Homonyms kept apart where the source allows**: DEDR Tamil, Malayalam, Kannada, Telugu (entry numbers, as before); Monier-Williams Sanskrit (its printed homonym numbers; 12,402 normalised spellings are now shared by 2+ entries); Wiktionary Tamil, Telugu, Kannada, Akkadian, Proto-Indo-Iranian, Sumerian, Santali (etymology number and original script: Sumerian *en* "until" and *en* "lord" are two words); Halloran Sumerian (one entry per printed headword line, which is where the sign index of ePSD-style homonyms sits: *du*, *du3*, *du7* are separate; 395 shared spellings); Turner CDIAL (one entry per numbered headword line). **Not possible**: Santali Campbell, Santali Bodding vol 5, Mundari Bhadra, Elamite Hinz-Koch, Burushaski Lorimer (their OCR prints no homonym numbers; same-spelled words stay one word). ePSD2 itself is unreachable from this machine. Effect at the strict distance, wide keywords, primary variant: Sumerian Halloran now hits 81 of 172 units (0 of 63 before), Wiktionary Tamil 72 (7 of 63 before), Monier-Williams 89, Akkadian 5 (0 before); the five merged lists still hit 0.
2. Units (`lang_m2_units.py` -> `work_data/lang_m2/signs.csv`, `units.csv`). 312 Lipi signs have a rank-1 crosswalk pair (to 224 Mahadevan drawings): 152 reach a 3of3 picture, 83 a 2of3 picture, 51 an "abstract" drawing, 26 no agreement. Variant A (3of3): 152 signs, 114 units, 65 picture-noun sets. Variant B (3of3 + 2of3, the primary variant): 235 signs, 172 units, 98 noun sets, classes spread over all ten (person/number starters 30, openers 34, back of name 22, counted goods 22, front of name 18, measure and box 11, after a measure 10, after-opener slot 9, after-jar title 9, closer 7). 73 different picture nouns.
3. Scores, controls and summary (`lang_m2_score.py` -> `grid.csv`, `summary.csv`, `unit_hits.csv`, `evidence.csv` with every strict and medium picture word / sound-alike pair that carries a keyword of a class the picture takes; log `score_log.txt`). Tables by `lang_m2_tables.py` (`tables.md`).
4. **Two control changes made after a two-dictionary smoke test (DEDR Tamil, Akkadian) and before the full run**, both for reasons of construction, not of the scores, and written into the header: (a) dealing classes among units of one picture (the control 4 as first worded) cannot change the score, because those units share the same sound-alikes (control mean equalled the real score to the third decimal); control 4 became "a class the picture does not take"; (b) the row-level sound deal lets forms that DEDR repeats inside one entry loose into other entries, doubling the strict sound-alikes (Tamil picture words: 3,275 real against 6,621 dealt), so control 3 deals forms between whole entries; the row version is still reported as C3row.
5. Bar, fixed in the header: a family clears it in the primary variant when Z3 has shuffle P below 0.05/7 AND its count of cells beating all four controls is above 0.05 x cells. Only then step 8.
6. Swaps (`lang_m2_swaps.py` -> `swap_grid.csv`, `swap_pairs.csv`, `swap_log.txt`): the first test's rule unchanged (two otherwise identical texts of 3+ signs differing at one place, in 2+ frames, both catalogues), pictures from the blind list, homonym-aware dictionaries.
7. Rival check on control 4 (`lang_m2_c4check.py` -> `c4check.csv`), described above.

## Step 6 per family (the summary that cannot be cherry-picked)

Cells per family = (its dictionaries + the pooled family) x 6 grid cells x 2 scores. For one-dictionary families the pooled family is the same dictionary, so a passing cell is counted twice (the Elamite 2 is one cell). "Expected by chance" is the bound 0.05 x cells (the chance of passing the single most lenient of the four controls); passing all four by luck is rarer than that.


| variant | family | dictionaries | cells | cells beating all 4 controls (P<0.05) | expected by chance (bound) | cells beating C2 and C3 | Z3 (mean z vs C3) / P | Z1 (vs C1) / P | Z4 (vs C4) / P | clears bar |
|---|---|---|---|---|---|---|---|---|---|---|
| A_3of3 | Dravidian | 7 | 96 | 0 | 4.8 | 3 | 0.06 / 0.3852 | -0.243 / 0.8406 | 1.428 / 0.0015 | no |
| A_3of3 | Munda | 4 | 60 | 0 | 3.0 | 2 | 0.02 / 0.4251 | 0.252 / 0.1359 | 1.088 / 0.0015 | no |
| A_3of3 | Indo-Aryan | 3 | 48 | 0 | 2.4 | 0 | -0.782 / 0.998 | -0.296 / 0.8286 | 0.263 / 0.2349 | no |
| A_3of3 | Sumerian | 2 | 36 | 0 | 1.8 | 0 | -0.025 / 0.499 | 0.218 / 0.3348 | 1.293 / 0.0105 | no |
| A_3of3 | Akkadian | 1 | 24 | 0 | 1.2 | 0 | -0.272 / 0.6387 | 0.122 / 0.3748 | 0.752 / 0.1034 | no |
| A_3of3 | Elamite | 1 | 24 | 2 | 1.2 | 2 | 0.371 / 0.1277 | 0.58 / 0.1329 | 0.681 / 0.0935 | no |
| A_3of3 | Burushaski | 1 | 24 | 0 | 1.2 | 0 | -0.388 / 0.8084 | -0.089 / 0.5472 | 0.172 / 0.2914 | no |
| B_3of3+2of3 | Dravidian | 7 | 96 | 0 | 4.8 | 3 | -0.198 / 0.8244 | 0.11 / 0.3358 | 2.346 / 0.0005 | no |
| B_3of3+2of3 | Munda | 4 | 60 | 0 | 3.0 | 2 | -0.039 / 0.5289 | 0.096 / 0.3318 | 0.939 / 0.001 | no |
| B_3of3+2of3 | Indo-Aryan | 3 | 48 | 0 | 2.4 | 1 | -0.557 / 0.9681 | -0.164 / 0.6827 | 0.344 / 0.1579 | no |
| B_3of3+2of3 | Sumerian | 2 | 36 | 0 | 1.8 | 0 | -0.055 / 0.5469 | 0.255 / 0.2984 | 1.852 / 0.0015 | no |
| B_3of3+2of3 | Akkadian | 1 | 24 | 0 | 1.2 | 0 | -0.337 / 0.6647 | -0.21 / 0.6307 | 0.266 / 0.3003 | no |
| B_3of3+2of3 | Elamite | 1 | 24 | 0 | 1.2 | 0 | 0.306 / 0.1597 | 0.382 / 0.2199 | 0.479 / 0.1619 | no |
| B_3of3+2of3 | Burushaski | 1 | 24 | 0 | 1.2 | 0 | -0.377 / 0.7944 | -0.088 / 0.5567 | 0.062 / 0.4138 | no |


Cells that beat both C2 and C3 (the first test's lean measure) and cells that beat all four, listed in full:

| variant | dictionary / family | distance | keywords | score | P against C1 / C2 / C3 / C4 | all four |
|---|---|---|---|---|---|---|
| A_3of3 | dedr_malayalam | strict | wide | hits 45.0 | 0.2374 / 0.0005 / 0.024 / 0.009 | no |
| A_3of3 | dedr_kannada | medium | narrow | hits 80.0 | 0.1879 / 0.001 / 0.022 / 0.0035 | no |
| A_3of3 | kannada_wiktionary | medium | wide | hits 53.0 | 0.7206 / 0.0035 / 0.002 / 0.3593 | no |
| A_3of3 | mundari_bhadra | medium | narrow | hits 50.0 | 0.2009 / 0.0005 / 0.0319 / 0.0045 | no |
| A_3of3 | mundari_bhadra | loose | wide | hits 114.0 | 0.1829 / 0.0005 / 0.0319 / 0.0615 | no |
| A_3of3 | elamite_hinzkoch | loose | wide | share 1.198 | 0.0055 / 0.0025 / 0.0319 / 0.001 | yes |
| A_3of3 | FAMILY Elamite | loose | wide | share 1.198 | 0.0055 / 0.0025 / 0.0319 / 0.001 | yes |
| B_3of3+2of3 | dedr_malayalam | strict | wide | hits 61.0 | 0.2259 / 0.0005 / 0.014 / 0.004 | no |
| B_3of3+2of3 | kannada_wiktionary | medium | wide | hits 64.0 | 0.8501 / 0.027 / 0.002 / 0.4913 | no |
| B_3of3+2of3 | kannada_wiktionary | loose | wide | share 3.909 | 0.3948 / 0.048 / 0.022 / 0.0005 | no |
| B_3of3+2of3 | mundari_bhadra | medium | narrow | hits 67.0 | 0.1569 / 0.0005 / 0.02 / 0.0005 | no |
| B_3of3+2of3 | proto_indoiranian_wiktionary | loose | narrow | share 2.165 | 0.6042 / 0.047 / 0.022 / 0.4488 | no |
| B_3of3+2of3 | FAMILY Munda | loose | narrow | share 1.756 | 0.4953 / 0.0055 / 0.0339 / 0.002 | no |

The one cell beating all four is Elamite (Hinz-Koch, German glosses), loose distance, wide keywords, 3of3 pictures: share 1.20, P 0.0055 / 0.0025 / 0.032 / 0.001. It does not hold with 2of3 pictures added, the family's combined Z3 is +0.37 (P 0.13), and loose distance on an OCR list where only 72 of 114 units have a picture word at all is the cell most open to noise.

## Control 4 rival check (base-rate adjusted share, primary variant, family pooled)

`work_data/lang_m2/c4check.csv`. Adjusted share = each unit's keyword share minus the share of all the family's words that carry that class's keyword. The raw C4 edge in Dravidian, Munda and Sumerian disappears except in the cells named above. The raw P here comes from this check's own draws (same rule, new seed), so it differs a little from the grid.

| family | distance | keywords | raw P vs C4 | adjusted real | adjusted C1 mean / P | adjusted C4 mean / P |
|---|---|---|---|---|---|---|
| Dravidian | strict | narrow | 0.037 | -0.839 | -0.926 / 0.2504 | -0.699 / 0.8376 |
| Dravidian | strict | wide | 0.005 | -0.904 | -1.009 / 0.2794 | -0.807 / 0.6792 |
| Dravidian | medium | narrow | 0.0005 | -0.557 | -0.62 / 0.1009 | -0.513 / 0.7161 |
| Dravidian | medium | wide | 0.0005 | -0.782 | -0.866 / 0.1174 | -0.741 / 0.6612 |
| Dravidian | loose | narrow | 0.0005 | -0.457 | -0.465 / 0.3273 | -0.376 / 0.939 |
| Dravidian | loose | wide | 0.0005 | -0.649 | -0.638 / 0.6502 | -0.517 / 0.9775 |
| Munda | strict | narrow | 1.0 | -0.377 | -0.282 / 0.995 | -0.239 / 1.0 |
| Munda | strict | wide | 1.0 | -0.702 | -0.596 / 0.9885 | -0.54 / 1.0 |
| Munda | medium | narrow | 0.0005 | 0.181 | -0.082 / 0.022 | -0.193 / 0.0005 |
| Munda | medium | wide | 0.0195 | 0.088 | -0.223 / 0.044 | -0.061 / 0.1954 |
| Munda | loose | narrow | 0.0005 | 0.143 | 0.151 / 0.5707 | 0.094 / 0.079 |
| Munda | loose | wide | 0.0085 | 0.16 | 0.2 / 0.7836 | 0.213 / 0.8561 |
| Indo-Aryan | strict | narrow | 0.1484 | -0.096 | -0.201 / 0.3208 | -0.11 / 0.4238 |
| Indo-Aryan | strict | wide | 0.7916 | -0.855 | -0.477 / 0.8171 | -0.206 / 0.954 |
| Indo-Aryan | medium | narrow | 0.1494 | -0.424 | -0.468 / 0.3008 | -0.258 / 0.9735 |
| Indo-Aryan | medium | wide | 0.8136 | -0.874 | -0.767 / 0.7691 | -0.419 / 0.9975 |
| Indo-Aryan | loose | narrow | 0.002 | -0.101 | -0.113 / 0.3278 | -0.05 / 0.9715 |
| Indo-Aryan | loose | wide | 0.093 | -0.135 | -0.099 / 0.7906 | -0.028 / 0.9995 |
| Sumerian | strict | narrow | 0.063 | -1.002 | -1.124 / 0.3203 | -0.993 / 0.4868 |
| Sumerian | strict | wide | 0.2224 | -1.988 | -2.182 / 0.2999 | -1.649 / 0.8081 |
| Sumerian | medium | narrow | 0.0115 | 0.344 | 0.414 / 0.5672 | 0.186 / 0.2744 |
| Sumerian | medium | wide | 0.007 | 0.556 | 0.572 / 0.5037 | 0.381 / 0.2864 |
| Sumerian | loose | narrow | 0.015 | -0.16 | -0.093 / 0.6862 | 0.001 / 0.942 |
| Sumerian | loose | wide | 0.008 | -0.136 | -0.044 / 0.6932 | 0.051 / 0.91 |
| Akkadian | strict | narrow | 1.0 | -1.023 | -0.793 / 0.8521 | -0.594 / 1.0 |
| Akkadian | strict | wide | 0.0075 | 0.205 | -1.068 / 0.025 | -1.112 / 0.014 |
| Akkadian | medium | narrow | 0.6927 | -1.156 | -0.987 / 0.7156 | -0.747 / 0.961 |
| Akkadian | medium | wide | 0.1789 | -1.505 | -1.684 / 0.3233 | -1.352 / 0.6082 |
| Akkadian | loose | narrow | 0.8521 | -0.225 | 0.208 / 0.98 | 0.315 / 1.0 |
| Akkadian | loose | wide | 0.4078 | 0.335 | 0.882 / 0.9675 | 0.904 / 0.992 |
| Elamite | strict | narrow | 1.0 | 0.0 | 0.0 / 1.0 | 0.0 / 1.0 |
| Elamite | strict | wide | 1.0 | 0.0 | 0.0 / 1.0 | 0.0 / 1.0 |
| Elamite | medium | narrow | 0.2314 | 0.271 | 0.166 / 0.2949 | 0.149 / 0.2179 |
| Elamite | medium | wide | 0.3873 | -0.33 | -0.309 / 0.5052 | -0.3 / 0.5562 |
| Elamite | loose | narrow | 0.3423 | 0.032 | 0.015 / 0.3558 | 0.004 / 0.2814 |
| Elamite | loose | wide | 0.0635 | 0.338 | 0.25 / 0.2649 | 0.195 / 0.1179 |
| Burushaski | strict | narrow | 1.0 | 0.0 | 0.0 / 1.0 | 0.0 / 1.0 |
| Burushaski | strict | wide | 1.0 | 0.0 | 0.0 / 1.0 | 0.0 / 1.0 |
| Burushaski | medium | narrow | 1.0 | -0.574 | -0.492 / 0.8986 | -0.406 / 0.9985 |
| Burushaski | medium | wide | 0.054 | 0.443 | -0.132 / 0.2084 | -0.341 / 0.076 |
| Burushaski | loose | narrow | 0.5617 | -0.42 | -0.345 / 0.7881 | -0.257 / 0.9885 |
| Burushaski | loose | wide | 0.5747 | -0.462 | -0.299 / 0.7921 | -0.188 / 0.9765 |

## Sign swaps, full table

#### Swap pairs, A_3of3

| dictionary / family | distance | sound-alike pairs / tested | random pairs mean (sd) / P | pictures dealt mean (sd) / P |
|---|---|---|---|---|
| dedr_tamil | strict | 14/49 | 11.35 (2.97) / 0.2149 | 14.09 (3.47) / 0.5447 |
| dedr_tamil | medium | 38/49 | 36.39 (3.07) / 0.3723 | 38.85 (3.03) / 0.6857 |
| dedr_tamil | loose | 49/49 | 47.8 (1.1) / 0.2984 | 48.87 (0.36) / 0.8716 |
| dedr_malayalam | strict | 1/49 | 1.75 (1.29) / 0.8326 | 1.6 (1.28) / 0.7936 |
| dedr_malayalam | medium | 20/49 | 21.82 (3.46) / 0.7526 | 27.72 (3.66) / 0.9915 |
| dedr_malayalam | loose | 44/49 | 43.29 (2.21) / 0.4883 | 46.16 (1.94) / 0.8776 |
| dedr_kannada | strict | 2/49 | 2.05 (1.42) / 0.6092 | 1.42 (1.22) / 0.4148 |
| dedr_kannada | medium | 15/49 | 21.88 (3.41) / 0.9895 | 26.52 (3.86) / 0.999 |
| dedr_kannada | loose | 43/49 | 41.27 (2.54) / 0.3228 | 45.31 (2.13) / 0.8691 |
| dedr_telugu | strict | 0/49 | 0.29 (0.55) / 1.0 | 0.57 (0.76) / 1.0 |
| dedr_telugu | medium | 4/49 | 7.28 (2.56) / 0.951 | 8.58 (2.86) / 0.9715 |
| dedr_telugu | loose | 44/49 | 39.6 (2.71) / 0.064 | 44.82 (2.05) / 0.7636 |
| tamil_wiktionary | strict | 5/49 | 6.72 (2.35) / 0.8301 | 9.8 (2.94) / 0.972 |
| tamil_wiktionary | medium | 36/49 | 29.4 (3.49) / 0.041 | 38.0 (3.29) / 0.7821 |
| tamil_wiktionary | loose | 47/49 | 45.92 (1.73) / 0.4003 | 46.84 (1.5) / 0.6367 |
| telugu_wiktionary | strict | 0/49 | 0.07 (0.28) / 1.0 | 0.0 (0.0) / 1.0 |
| telugu_wiktionary | medium | 12/49 | 10.99 (2.88) / 0.4208 | 11.22 (3.12) / 0.4563 |
| telugu_wiktionary | loose | 39/49 | 40.16 (2.63) / 0.7466 | 41.42 (2.76) / 0.8546 |
| kannada_wiktionary | strict | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| kannada_wiktionary | medium | 3/49 | 5.66 (2.23) / 0.939 | 7.85 (2.72) / 0.989 |
| kannada_wiktionary | loose | 19/49 | 21.32 (3.47) / 0.7876 | 23.13 (3.83) / 0.8856 |
| santali_campbell | strict | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| santali_campbell | medium | 10/49 | 7.56 (2.48) / 0.2104 | 6.99 (2.55) / 0.1534 |
| santali_campbell | loose | 42/49 | 41.65 (2.48) / 0.5532 | 43.96 (2.28) / 0.8501 |
| santali_bodding5 | strict | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| santali_bodding5 | medium | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| santali_bodding5 | loose | 3/49 | 1.0 (1.01) / 0.083 | 1.83 (1.41) / 0.2689 |
| santali_wiktionary | strict | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| santali_wiktionary | medium | 1/49 | 0.06 (0.25) / 0.059 | 0.22 (0.47) / 0.1949 |
| santali_wiktionary | loose | 12/49 | 15.59 (3.32) / 0.8921 | 13.52 (3.26) / 0.7281 |
| mundari_bhadra | strict | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| mundari_bhadra | medium | 3/49 | 6.06 (2.32) / 0.953 | 4.74 (2.1) / 0.8636 |
| mundari_bhadra | loose | 32/49 | 36.12 (3.15) / 0.9225 | 39.85 (3.03) / 0.9945 |
| sanskrit_mw | strict | 2/49 | 5.25 (2.17) / 0.9675 | 2.72 (1.66) / 0.7571 |
| sanskrit_mw | medium | 20/49 | 22.28 (3.55) / 0.7731 | 22.1 (3.79) / 0.7476 |
| sanskrit_mw | loose | 45/49 | 46.33 (1.58) / 0.8646 | 46.75 (1.51) / 0.9165 |
| oia_turner | strict | 0/49 | 0.17 (0.41) / 1.0 | 0.0 (0.0) / 1.0 |
| oia_turner | medium | 0/49 | 0.99 (1.01) / 1.0 | 0.44 (0.66) / 1.0 |
| oia_turner | loose | 26/49 | 29.04 (3.39) / 0.8551 | 31.2 (3.62) / 0.9365 |
| proto_indoiranian_wiktionary | strict | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| proto_indoiranian_wiktionary | medium | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| proto_indoiranian_wiktionary | loose | 4/49 | 8.01 (2.63) / 0.9715 | 6.87 (2.56) / 0.924 |
| sumerian_halloran | strict | 1/49 | 2.96 (1.67) / 0.9585 | 0.22 (0.47) / 0.1949 |
| sumerian_halloran | medium | 11/49 | 16.81 (3.34) / 0.9765 | 14.39 (3.43) / 0.8696 |
| sumerian_halloran | loose | 35/49 | 32.61 (3.28) / 0.2919 | 35.27 (3.5) / 0.6112 |
| sumerian_wiktionary | strict | 1/49 | 1.09 (1.06) / 0.6592 | 1.02 (1.01) / 0.6437 |
| sumerian_wiktionary | medium | 8/49 | 8.82 (2.68) / 0.6687 | 9.16 (2.77) / 0.7181 |
| sumerian_wiktionary | loose | 29/49 | 28.31 (3.46) / 0.4858 | 32.08 (3.65) / 0.8396 |
| akkadian_wiktionary | strict | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| akkadian_wiktionary | medium | 0/49 | 0.09 (0.29) / 1.0 | 0.14 (0.38) / 1.0 |
| akkadian_wiktionary | loose | 11/49 | 13.71 (3.12) / 0.8521 | 13.02 (3.33) / 0.7696 |
| elamite_hinzkoch | strict | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| elamite_hinzkoch | medium | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| elamite_hinzkoch | loose | 2/49 | 2.62 (1.56) / 0.7546 | 2.36 (1.52) / 0.6862 |
| burushaski_lorimer | strict | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| burushaski_lorimer | medium | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| burushaski_lorimer | loose | 2/49 | 5.18 (2.16) / 0.97 | 4.18 (2.03) / 0.923 |
| FAMILY Dravidian | strict | 20/49 | 18.8 (3.37) / 0.4223 | 22.0 (3.8) / 0.7366 |
| FAMILY Dravidian | medium | 42/49 | 41.76 (2.49) / 0.5547 | 44.16 (2.31) / 0.8741 |
| FAMILY Dravidian | loose | 49/49 | 48.8 (0.44) / 0.8186 | 49.0 (0.0) / 1.0 |
| FAMILY Munda | strict | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| FAMILY Munda | medium | 14/49 | 11.8 (2.95) / 0.2734 | 11.95 (3.08) / 0.2984 |
| FAMILY Munda | loose | 44/49 | 44.75 (1.97) / 0.7456 | 46.06 (1.76) / 0.9195 |
| FAMILY Indo-Aryan | strict | 2/49 | 5.42 (2.19) / 0.9705 | 2.72 (1.66) / 0.7571 |
| FAMILY Indo-Aryan | medium | 20/49 | 22.39 (3.56) / 0.7841 | 22.1 (3.79) / 0.7476 |
| FAMILY Indo-Aryan | loose | 45/49 | 46.62 (1.5) / 0.9085 | 46.75 (1.51) / 0.9165 |
| FAMILY Sumerian | strict | 2/49 | 4.05 (1.93) / 0.93 | 1.24 (1.11) / 0.3583 |
| FAMILY Sumerian | medium | 17/49 | 20.87 (3.52) / 0.8956 | 20.82 (3.72) / 0.8791 |
| FAMILY Sumerian | loose | 40/49 | 35.69 (3.11) / 0.1074 | 41.18 (2.83) / 0.7256 |
| FAMILY Akkadian | strict | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| FAMILY Akkadian | medium | 0/49 | 0.09 (0.29) / 1.0 | 0.14 (0.38) / 1.0 |
| FAMILY Akkadian | loose | 11/49 | 13.71 (3.12) / 0.8521 | 13.02 (3.33) / 0.7696 |
| FAMILY Elamite | strict | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| FAMILY Elamite | medium | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| FAMILY Elamite | loose | 2/49 | 2.62 (1.56) / 0.7546 | 2.36 (1.52) / 0.6862 |
| FAMILY Burushaski | strict | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| FAMILY Burushaski | medium | 0/49 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| FAMILY Burushaski | loose | 2/49 | 5.18 (2.16) / 0.97 | 4.18 (2.03) / 0.923 |

#### Swap pairs, B_3of3+2of3

| dictionary / family | distance | sound-alike pairs / tested | random pairs mean (sd) / P | pictures dealt mean (sd) / P |
|---|---|---|---|---|
| dedr_tamil | strict | 28/108 | 19.32 (3.89) / 0.0235 | 25.12 (5.12) / 0.3083 |
| dedr_tamil | medium | 79/108 | 71.37 (4.9) / 0.071 | 78.0 (5.84) / 0.4973 |
| dedr_tamil | loose | 107/108 | 102.16 (2.4) / 0.02 | 104.46 (2.1) / 0.1514 |
| dedr_malayalam | strict | 1/108 | 3.38 (1.85) / 0.965 | 3.53 (2.02) / 0.9575 |
| dedr_malayalam | medium | 43/108 | 41.85 (4.93) / 0.4518 | 52.84 (5.97) / 0.9595 |
| dedr_malayalam | loose | 89/108 | 90.19 (3.82) / 0.6817 | 93.85 (4.51) / 0.8786 |
| dedr_kannada | strict | 2/108 | 3.54 (1.82) / 0.8736 | 2.08 (1.6) / 0.5882 |
| dedr_kannada | medium | 26/108 | 34.72 (4.93) / 0.9725 | 41.28 (6.1) / 0.997 |
| dedr_kannada | loose | 88/108 | 80.61 (4.46) / 0.0585 | 87.17 (5.16) / 0.5027 |
| dedr_telugu | strict | 0/108 | 0.27 (0.52) / 1.0 | 0.38 (0.64) / 1.0 |
| dedr_telugu | medium | 6/108 | 12.04 (3.21) / 0.9875 | 16.22 (4.29) / 0.9975 |
| dedr_telugu | loose | 84/108 | 76.18 (4.69) / 0.0595 | 84.41 (5.33) / 0.5792 |
| tamil_wiktionary | strict | 17/108 | 11.41 (3.22) / 0.067 | 18.43 (4.33) / 0.6562 |
| tamil_wiktionary | medium | 73/108 | 51.53 (5.23) / 0.0005 | 64.53 (6.3) / 0.0985 |
| tamil_wiktionary | loose | 99/108 | 96.04 (3.23) / 0.2299 | 101.36 (2.76) / 0.8566 |
| telugu_wiktionary | strict | 0/108 | 0.39 (0.62) / 1.0 | 1.01 (1.05) / 1.0 |
| telugu_wiktionary | medium | 16/108 | 18.16 (3.81) / 0.7481 | 20.67 (4.8) / 0.8526 |
| telugu_wiktionary | loose | 87/108 | 82.08 (4.47) / 0.1529 | 84.81 (5.14) / 0.3938 |
| kannada_wiktionary | strict | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| kannada_wiktionary | medium | 4/108 | 7.73 (2.75) / 0.9505 | 10.17 (3.56) / 0.985 |
| kannada_wiktionary | loose | 36/108 | 37.94 (5.02) / 0.6772 | 45.07 (6.23) / 0.936 |
| santali_campbell | strict | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| santali_campbell | medium | 16/108 | 11.48 (3.21) / 0.1074 | 12.27 (3.6) / 0.1909 |
| santali_campbell | loose | 83/108 | 76.92 (4.71) / 0.1164 | 83.03 (5.34) / 0.5587 |
| santali_bodding5 | strict | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| santali_bodding5 | medium | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| santali_bodding5 | loose | 7/108 | 2.74 (1.59) / 0.0175 | 6.69 (2.88) / 0.4903 |
| santali_wiktionary | strict | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| santali_wiktionary | medium | 1/108 | 0.08 (0.28) / 0.0775 | 0.14 (0.38) / 0.1294 |
| santali_wiktionary | loose | 22/108 | 24.25 (4.35) / 0.7301 | 28.15 (5.44) / 0.8906 |
| mundari_bhadra | strict | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| mundari_bhadra | medium | 4/108 | 7.98 (2.74) / 0.957 | 7.34 (2.85) / 0.922 |
| mundari_bhadra | loose | 72/108 | 66.76 (5.03) / 0.1689 | 76.22 (5.71) / 0.7906 |
| sanskrit_mw | strict | 4/108 | 6.87 (2.49) / 0.927 | 5.32 (2.52) / 0.7506 |
| sanskrit_mw | medium | 32/108 | 36.12 (4.94) / 0.8231 | 38.17 (5.93) / 0.8796 |
| sanskrit_mw | loose | 96/108 | 96.63 (3.22) / 0.6577 | 100.29 (3.0) / 0.93 |
| oia_turner | strict | 0/108 | 0.65 (0.8) / 1.0 | 0.24 (0.48) / 1.0 |
| oia_turner | medium | 1/108 | 2.18 (1.43) / 0.8851 | 2.22 (1.55) / 0.8871 |
| oia_turner | loose | 44/108 | 49.5 (5.29) / 0.8681 | 54.46 (6.53) / 0.958 |
| proto_indoiranian_wiktionary | strict | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| proto_indoiranian_wiktionary | medium | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| proto_indoiranian_wiktionary | loose | 4/108 | 11.48 (3.21) / 0.9975 | 9.36 (3.29) / 0.9755 |
| sumerian_halloran | strict | 1/108 | 5.81 (2.33) / 0.997 | 4.38 (2.26) / 0.981 |
| sumerian_halloran | medium | 17/108 | 28.43 (4.53) / 0.997 | 25.79 (5.38) / 0.9665 |
| sumerian_halloran | loose | 58/108 | 60.72 (5.12) / 0.7231 | 64.36 (6.46) / 0.8506 |
| sumerian_wiktionary | strict | 1/108 | 2.01 (1.43) / 0.8611 | 3.12 (1.88) / 0.941 |
| sumerian_wiktionary | medium | 14/108 | 15.61 (3.6) / 0.7106 | 19.39 (4.53) / 0.9085 |
| sumerian_wiktionary | loose | 59/108 | 53.1 (5.17) / 0.1494 | 59.57 (6.59) / 0.5607 |
| akkadian_wiktionary | strict | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| akkadian_wiktionary | medium | 1/108 | 0.38 (0.61) / 0.3123 | 0.96 (1.01) / 0.6042 |
| akkadian_wiktionary | loose | 18/108 | 22.82 (4.26) / 0.8956 | 21.13 (4.91) / 0.7691 |
| elamite_hinzkoch | strict | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| elamite_hinzkoch | medium | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| elamite_hinzkoch | loose | 4/108 | 5.09 (2.22) / 0.7436 | 3.83 (2.09) / 0.5242 |
| burushaski_lorimer | strict | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| burushaski_lorimer | medium | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| burushaski_lorimer | loose | 6/108 | 9.5 (3.0) / 0.921 | 10.32 (3.42) / 0.9325 |
| FAMILY Dravidian | strict | 40/108 | 31.98 (4.64) / 0.0535 | 39.36 (5.86) / 0.4938 |
| FAMILY Dravidian | medium | 89/108 | 84.46 (4.19) / 0.1719 | 89.44 (4.75) / 0.6082 |
| FAMILY Dravidian | loose | 108/108 | 105.36 (1.62) / 0.0635 | 106.88 (1.11) / 0.3368 |
| FAMILY Munda | strict | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| FAMILY Munda | medium | 21/108 | 17.61 (3.82) / 0.2234 | 18.17 (4.36) / 0.2939 |
| FAMILY Munda | loose | 92/108 | 86.03 (4.22) / 0.1029 | 90.74 (4.54) / 0.4468 |
| FAMILY Indo-Aryan | strict | 4/108 | 7.5 (2.58) / 0.954 | 5.56 (2.56) / 0.7796 |
| FAMILY Indo-Aryan | medium | 32/108 | 36.45 (4.94) / 0.8376 | 38.17 (5.93) / 0.8796 |
| FAMILY Indo-Aryan | loose | 96/108 | 97.36 (3.13) / 0.7406 | 100.39 (2.97) / 0.9365 |
| FAMILY Sumerian | strict | 2/108 | 7.82 (2.71) / 0.9965 | 7.51 (2.92) / 0.9935 |
| FAMILY Sumerian | medium | 27/108 | 34.78 (4.77) / 0.9655 | 36.18 (6.03) / 0.949 |
| FAMILY Sumerian | loose | 74/108 | 71.04 (4.85) / 0.3043 | 78.74 (5.6) / 0.8171 |
| FAMILY Akkadian | strict | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| FAMILY Akkadian | medium | 1/108 | 0.38 (0.61) / 0.3123 | 0.96 (1.01) / 0.6042 |
| FAMILY Akkadian | loose | 18/108 | 22.82 (4.26) / 0.8956 | 21.13 (4.91) / 0.7691 |
| FAMILY Elamite | strict | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| FAMILY Elamite | medium | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| FAMILY Elamite | loose | 4/108 | 5.09 (2.22) / 0.7436 | 3.83 (2.09) / 0.5242 |
| FAMILY Burushaski | strict | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| FAMILY Burushaski | medium | 0/108 | 0.0 (0.0) / 1.0 | 0.0 (0.0) / 1.0 |
| FAMILY Burushaski | loose | 6/108 | 9.5 (3.0) / 0.921 | 10.32 (3.42) / 0.9325 |

## Limits

- Pictures reach 235 of the 312 crosswalked signs (rank-1 pairs only); Lipi signs with no rank-1 Mahadevan partner are not in the test. Blind describers named strokes as "comb", "rake" or "fork" in places (39, 21 and 21 drawings), and these were kept, as fixed in advance: no sign was dropped by hand.
- The machine classes are learned from sign order; their keyword lists are a guess at what each class means (written once, before scoring). A class such as "back of a name" has no single English meaning, and that dilutes it.
- Glosses are English (German for Elamite) and the picture rule needs the thing named in the first 3 gloss words; words glossed only by a synonym the rule does not list are missed (73 nouns, 60 of them found in DEDR Tamil, 65 in Monier-Williams).
- Five dictionaries (both Munda sources with entries in quantity, Elamite, Burushaski, Santali Bodding) could not be split by homonym, so their strict match finds nothing; Munda's strict cells are empty for that reason, not for lack of puns.
- Sound-alikes cluster with related meanings (derivatives under separate entries), which puts real languages below scrambled sounds (C3) on this score (described above). C3 at entry level and at row level agree on this.
- 500 control-3 runs per dictionary put the smallest possible P at 0.002 for C3 and for Z3.
- Large scratch (homonym-aware dictionaries, about 20 MB, the Sanskrit table 14 MB) is in /tmp/lang_m2/lex and is rebuilt by `lang_m2_lexicons.py`.

## Full grid, every dictionary and every family

Rows marked **all 4** beat every control at P below 0.05.

#### A_3of3: share, every family and every dictionary, full grid

| dictionary / family | distance | keywords | units covered | share | C1 classes dealt mean / P | C2 outside nouns mean / P | C3 sounds dealt by entry mean / P | C4 wrong class same picture mean / P | C3row mean / P |
|---|---|---|---|---|---|---|---|---|---|
| FAMILY Dravidian | strict | narrow | 114/114 | 0.799 | 0.846 / 0.6677 | 0.809 / 0.4568 | 1.06 / 0.9501 | 0.762 / 0.3328 | 1.06 / 0.9741 |
| FAMILY Dravidian | strict | wide | 114/114 | 2.26 | 2.28 / 0.5217 | 1.96 / 0.2404 | 2.29 / 0.507 | 2.05 / 0.0955 | 2.33 / 0.5848 |
| FAMILY Dravidian | medium | narrow | 114/114 | 1.04 | 1 / 0.1174 | 1.03 / 0.4458 | 1.08 / 0.7565 | 0.858 / 0.0005 | 1.08 / 0.7505 |
| FAMILY Dravidian | medium | wide | 114/114 | 2.29 | 2.24 / 0.1804 | 2.3 / 0.4928 | 2.38 / 0.8303 | 1.98 / 0.0005 | 2.37 / 0.8024 |
| FAMILY Dravidian | loose | narrow | 114/114 | 1.08 | 1.08 / 0.3003 | 1.11 / 0.7616 | 1.12 / 0.9621 | 0.932 / 0.001 | 1.12 / 0.9661 |
| FAMILY Dravidian | loose | wide | 114/114 | 2.33 | 2.35 / 0.7696 | 2.41 / 0.937 | 2.42 / 0.996 | 2.1 / 0.0015 | 2.43 / 1.0 |
| FAMILY Munda | strict | narrow | 114/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.434 / 1.0 | 0 / 1.0 | 0.459 / 1.0 |
| FAMILY Munda | strict | wide | 114/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.939 / 1.0 | 0 / 1.0 | 1.01 / 1.0 |
| FAMILY Munda | medium | narrow | 114/114 | 1.31 | 1.05 / 0.006 | 1.08 / 0.1624 | 1.05 / 0.0878 | 0.851 / 0.0005 | 1.05 / 0.0858 |
| FAMILY Munda | medium | wide | 114/114 | 2.3 | 2.11 / 0.092 | 2.28 / 0.4023 | 2.25 / 0.4431 | 2.03 / 0.037 | 2.24 / 0.4391 |
| FAMILY Munda | loose | narrow | 114/114 | 1.09 | 1.11 / 0.8206 | 1.04 / 0.1909 | 1.06 / 0.2315 | 1.01 / 0.1099 | 1.06 / 0.2236 |
| FAMILY Munda | loose | wide | 114/114 | 2.3 | 2.32 / 0.7896 | 2.25 / 0.3078 | 2.24 / 0.1856 | 2.19 / 0.0995 | 2.24 / 0.1697 |
| FAMILY Indo-Aryan | strict | narrow | 114/114 | 1.3 | 1.29 / 0.3883 | 1.01 / 0.2034 | 1.32 / 0.4411 | 1.21 / 0.2799 | 1.32 / 0.4411 |
| FAMILY Indo-Aryan | strict | wide | 114/114 | 2.21 | 2.52 / 0.8036 | 2.53 / 0.6742 | 2.64 / 0.8483 | 2.51 / 0.7831 | 2.64 / 0.8483 |
| FAMILY Indo-Aryan | medium | narrow | 114/114 | 1.11 | 1.07 / 0.2849 | 1.12 / 0.5032 | 1.33 / 1.0 | 1.02 / 0.1439 | 1.33 / 1.0 |
| FAMILY Indo-Aryan | medium | wide | 114/114 | 2.31 | 2.4 / 0.7486 | 2.46 / 0.7836 | 2.7 / 1.0 | 2.41 / 0.7516 | 2.7 / 1.0 |
| FAMILY Indo-Aryan | loose | narrow | 114/114 | 1.23 | 1.25 / 0.8101 | 1.17 / 0.051 | 1.33 / 1.0 | 1.15 / 0.1 | 1.33 / 1.0 |
| FAMILY Indo-Aryan | loose | wide | 114/114 | 2.65 | 2.7 / 0.965 | 2.61 / 0.2364 | 2.71 / 0.996 | 2.59 / 0.3168 | 2.71 / 0.996 |
| FAMILY Sumerian | strict | narrow | 108/114 | 1.29 | 1.19 / 0.2839 | 0.868 / 0.1894 | 1.63 / 0.7844 | 1.06 / 0.1134 | 1.82 / 0.8762 |
| FAMILY Sumerian | strict | wide | 108/114 | 2.98 | 2.76 / 0.2444 | 2.83 / 0.3798 | 3.74 / 0.8383 | 2.85 / 0.3328 | 3.94 / 0.9301 |
| FAMILY Sumerian | medium | narrow | 108/114 | 1.9 | 2.02 / 0.6567 | 1.88 / 0.3793 | 1.72 / 0.1617 | 1.78 / 0.3083 | 1.86 / 0.3653 |
| FAMILY Sumerian | medium | wide | 108/114 | 4.07 | 4.29 / 0.7601 | 4.21 / 0.5162 | 3.91 / 0.2754 | 4.06 / 0.4908 | 4.05 / 0.4411 |
| FAMILY Sumerian | loose | narrow | 108/114 | 1.79 | 1.81 / 0.6082 | 1.67 / 0.2244 | 1.82 / 0.6068 | 1.65 / 0.064 | 1.87 / 0.8124 |
| FAMILY Sumerian | loose | wide | 108/114 | 3.98 | 4.12 / 0.8966 | 4.07 / 0.6257 | 4.06 / 0.6766 | 3.91 / 0.3128 | 4.09 / 0.7884 |
| FAMILY Akkadian | strict | narrow | 97/114 | 0 | 0.103 / 1.0 | 0 / 1.0 | 0.754 / 1.0 | 0.134 / 1.0 | 0.754 / 1.0 |
| FAMILY Akkadian | strict | wide | 97/114 | 1.25 | 0.428 / 0.0485 | 0 / 0.0005 | 1.35 / 0.4251 | 0.362 / 0.026 | 1.35 / 0.4251 |
| FAMILY Akkadian | medium | narrow | 97/114 | 0.675 | 0.696 / 0.4498 | 1.08 / 0.5452 | 1.3 / 0.7745 | 0.704 / 0.4513 | 1.3 / 0.7745 |
| FAMILY Akkadian | medium | wide | 97/114 | 2.14 | 1.64 / 0.081 | 1.69 / 0.2654 | 2.51 / 0.5429 | 1.44 / 0.0155 | 2.51 / 0.5429 |
| FAMILY Akkadian | loose | narrow | 97/114 | 1.57 | 1.82 / 0.8751 | 1.44 / 0.3533 | 1.66 / 0.5749 | 1.61 / 0.5917 | 1.66 / 0.5749 |
| FAMILY Akkadian | loose | wide | 97/114 | 3.55 | 3.84 / 0.8476 | 3.13 / 0.2664 | 3.31 / 0.2794 | 3.44 / 0.2929 | 3.31 / 0.2794 |
| FAMILY Elamite | strict | narrow | 72/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| FAMILY Elamite | strict | wide | 72/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.006 / 1.0 | 0 / 1.0 | 0.006 / 1.0 |
| FAMILY Elamite | medium | narrow | 72/114 | 0.238 | 0.201 / 0.3333 | 0.062 / 0.096 | 0.113 / 0.1337 | 0.213 / 0.3763 | 0.113 / 0.1337 |
| FAMILY Elamite | medium | wide | 72/114 | 0.238 | 0.227 / 0.4098 | 0.264 / 0.3548 | 0.622 / 0.6707 | 0.247 / 0.4973 | 0.622 / 0.6707 |
| FAMILY Elamite | loose | narrow | 72/114 | 0.169 | 0.142 / 0.2439 | 0.073 / 0.1114 | 0.121 / 0.1597 | 0.14 / 0.2309 | 0.121 / 0.1597 |
| FAMILY Elamite | loose | wide | 72/114 | 1.2 **all 4** | 0.91 / 0.0055 | 0.281 / 0.0025 | 0.779 / 0.0319 | 0.855 / 0.001 | 0.779 / 0.0319 |
| FAMILY Burushaski | strict | narrow | 83/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| FAMILY Burushaski | strict | wide | 83/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| FAMILY Burushaski | medium | narrow | 83/114 | 0 | 0.01 / 1.0 | 0.634 / 1.0 | 0.432 / 1.0 | 0.011 / 1.0 | 0.432 / 1.0 |
| FAMILY Burushaski | medium | wide | 83/114 | 1.15 | 0.741 / 0.2334 | 1.15 / 0.3928 | 0.887 / 0.2814 | 0.417 / 0.083 | 0.887 / 0.2814 |
| FAMILY Burushaski | loose | narrow | 83/114 | 0.305 | 0.343 / 0.6832 | 0.718 / 0.911 | 0.585 / 0.9501 | 0.32 / 0.4813 | 0.585 / 0.9501 |
| FAMILY Burushaski | loose | wide | 83/114 | 0.998 | 1.05 / 0.5842 | 1.46 / 0.7616 | 1.24 / 0.7385 | 1.01 / 0.4613 | 1.24 / 0.7385 |
| dedr_tamil | strict | narrow | 114/114 | 0.604 | 0.777 / 0.922 | 0.714 / 0.5097 | 1 / 0.978 | 0.657 / 0.6722 | 1.04 / 0.992 |
| dedr_tamil | strict | wide | 114/114 | 1.89 | 2.02 / 0.6937 | 1.49 / 0.2144 | 2.16 / 0.7505 | 1.79 / 0.3133 | 2.25 / 0.8323 |
| dedr_tamil | medium | narrow | 114/114 | 0.843 | 0.812 / 0.1699 | 0.96 / 0.6612 | 1 / 0.9741 | 0.673 / 0.0005 | 1.05 / 0.994 |
| dedr_tamil | medium | wide | 114/114 | 1.98 | 1.92 / 0.1654 | 2.08 / 0.5602 | 2.23 / 0.9741 | 1.71 / 0.001 | 2.27 / 0.982 |
| dedr_tamil | loose | narrow | 114/114 | 0.964 | 0.96 / 0.4083 | 0.951 / 0.3833 | 1.02 / 0.9641 | 0.827 / 0.0015 | 1.06 / 0.998 |
| dedr_tamil | loose | wide | 114/114 | 2.05 | 2.07 / 0.7741 | 2.06 / 0.5827 | 2.23 / 1.0 | 1.89 / 0.0145 | 2.3 / 1.0 |
| dedr_malayalam | strict | narrow | 111/114 | 1.14 | 1.24 / 0.5027 | 0.61 / 0.1184 | 0.72 / 0.1417 | 1.13 / 0.3833 | 0.726 / 0.1397 |
| dedr_malayalam | strict | wide | 111/114 | 2.96 | 2.89 / 0.4103 | 1.65 / 0.049 | 1.83 / 0.0599 | 2.55 / 0.2309 | 1.79 / 0.0539 |
| dedr_malayalam | medium | narrow | 111/114 | 1.03 | 1.14 / 0.9105 | 0.902 / 0.2499 | 0.738 / 0.0299 | 1.02 / 0.4113 | 0.729 / 0.012 |
| dedr_malayalam | medium | wide | 111/114 | 2.45 | 2.6 / 0.9105 | 2.35 / 0.3563 | 1.88 / 0.022 | 2.36 / 0.2474 | 1.84 / 0.01 |
| dedr_malayalam | loose | narrow | 111/114 | 0.862 | 0.859 / 0.4138 | 0.831 / 0.3068 | 0.735 / 0.004 | 0.794 / 0.0555 | 0.729 / 0.002 |
| dedr_malayalam | loose | wide | 111/114 | 2.15 | 2.18 / 0.8026 | 2.14 / 0.4843 | 1.87 / 0.002 | 2.03 / 0.081 | 1.85 / 0.002 |
| dedr_kannada | strict | narrow | 109/114 | 0.574 | 0.939 / 0.902 | 0.883 / 0.5382 | 0.621 / 0.499 | 1.1 / 0.9985 | 0.638 / 0.501 |
| dedr_kannada | strict | wide | 109/114 | 1.8 | 2.27 / 0.9015 | 2.36 / 0.5807 | 1.77 / 0.4192 | 2.23 / 0.93 | 1.78 / 0.4331 |
| dedr_kannada | medium | narrow | 109/114 | 0.794 | 0.737 / 0.1794 | 0.719 / 0.2939 | 0.681 / 0.1537 | 0.628 / 0.0035 | 0.667 / 0.0818 |
| dedr_kannada | medium | wide | 109/114 | 2.01 | 1.96 / 0.2934 | 2 / 0.4523 | 1.83 / 0.1916 | 1.67 / 0.0005 | 1.85 / 0.1537 |
| dedr_kannada | loose | narrow | 109/114 | 0.744 | 0.746 / 0.5312 | 0.707 / 0.2894 | 0.693 / 0.0719 | 0.665 / 0.0065 | 0.683 / 0.016 |
| dedr_kannada | loose | wide | 109/114 | 1.93 | 1.96 / 0.7831 | 1.95 / 0.5927 | 1.86 / 0.1178 | 1.79 / 0.0225 | 1.88 / 0.1437 |
| dedr_telugu | strict | narrow | 112/114 | 1.32 | 0.724 / 0.0145 | 0.759 / 0.1679 | 0.778 / 0.1537 | 0.422 / 0.0005 | 0.806 / 0.1597 |
| dedr_telugu | strict | wide | 112/114 | 3.36 | 2.66 / 0.1534 | 1.84 / 0.1084 | 1.66 / 0.0339 | 1.95 / 0.0065 | 1.78 / 0.0599 |
| dedr_telugu | medium | narrow | 112/114 | 0.898 | 0.954 / 0.6432 | 0.628 / 0.1504 | 0.857 / 0.3613 | 0.842 / 0.2884 | 0.839 / 0.3353 |
| dedr_telugu | medium | wide | 112/114 | 2.23 | 2.12 / 0.2719 | 1.8 / 0.1919 | 1.97 / 0.2196 | 1.86 / 0.0095 | 1.83 / 0.0978 |
| dedr_telugu | loose | narrow | 112/114 | 0.882 | 0.882 / 0.5082 | 0.809 / 0.2114 | 0.84 / 0.2655 | 0.738 / 0.0005 | 0.847 / 0.2216 |
| dedr_telugu | loose | wide | 112/114 | 2.06 | 2 / 0.0985 | 1.88 / 0.1539 | 1.87 / 0.0339 | 1.76 / 0.0005 | 1.86 / 0.02 |
| tamil_wiktionary | strict | narrow | 113/114 | 1.19 | 1.27 / 0.6172 | 1.04 / 0.3233 | 1.33 / 0.5828 | 1.22 / 0.5667 | 1.3 / 0.5269 |
| tamil_wiktionary | strict | wide | 113/114 | 2.2 | 2.31 / 0.6392 | 2.25 / 0.4798 | 2.85 / 0.7924 | 2.24 / 0.5572 | 2.83 / 0.8004 |
| tamil_wiktionary | medium | narrow | 113/114 | 1.25 | 1.36 / 0.8811 | 1.43 / 0.7866 | 1.36 / 0.7605 | 1.24 / 0.4713 | 1.36 / 0.7345 |
| tamil_wiktionary | medium | wide | 113/114 | 2.83 | 2.79 / 0.4018 | 2.76 / 0.3778 | 2.92 / 0.6148 | 2.41 / 0.0055 | 2.93 / 0.6347 |
| tamil_wiktionary | loose | narrow | 113/114 | 1.34 | 1.37 / 0.928 | 1.43 / 0.9765 | 1.37 / 0.7545 | 1.18 / 0.015 | 1.37 / 0.7585 |
| tamil_wiktionary | loose | wide | 113/114 | 2.73 | 2.77 / 0.8971 | 2.85 / 0.9455 | 2.95 / 1.0 | 2.4 / 0.0005 | 2.95 / 0.998 |
| telugu_wiktionary | strict | narrow | 114/114 | 1.15 | 1.32 / 0.5227 | 1.18 / 0.4178 | 1.71 / 0.7305 | 1.28 / 0.5612 | 1.7 / 0.7445 |
| telugu_wiktionary | strict | wide | 114/114 | 2.32 | 2.3 / 0.4453 | 1.96 / 0.3158 | 3.02 / 0.7186 | 1.87 / 0.2464 | 3.06 / 0.7465 |
| telugu_wiktionary | medium | narrow | 114/114 | 1.84 | 1.44 / 0.0235 | 1.71 / 0.3483 | 1.95 / 0.6228 | 1.13 / 0.0005 | 1.96 / 0.6387 |
| telugu_wiktionary | medium | wide | 114/114 | 2.96 | 2.98 / 0.4698 | 3.1 / 0.5567 | 3.46 / 0.8922 | 2.75 / 0.2889 | 3.47 / 0.8942 |
| telugu_wiktionary | loose | narrow | 114/114 | 1.72 | 1.82 / 0.912 | 1.79 / 0.7761 | 2.05 / 1.0 | 1.57 / 0.1329 | 2.05 / 1.0 |
| telugu_wiktionary | loose | wide | 114/114 | 3.15 | 3.27 / 0.947 | 3.26 / 0.7976 | 3.6 / 1.0 | 2.88 / 0.0395 | 3.6 / 1.0 |
| kannada_wiktionary | strict | narrow | 111/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.398 / 1.0 | 0 / 1.0 | 0.398 / 1.0 |
| kannada_wiktionary | strict | wide | 111/114 | 0 | 0.104 / 1.0 | 0.61 / 1.0 | 0.948 / 1.0 | 0.122 / 1.0 | 0.948 / 1.0 |
| kannada_wiktionary | medium | narrow | 111/114 | 0.96 | 0.965 / 0.4963 | 1.38 / 0.6522 | 0.736 / 0.2515 | 1.01 / 0.6317 | 0.736 / 0.2515 |
| kannada_wiktionary | medium | wide | 111/114 | 3.26 | 3.51 / 0.6982 | 2.77 / 0.2844 | 1.81 / 0.0699 | 3.08 / 0.2674 | 1.81 / 0.0699 |
| kannada_wiktionary | loose | narrow | 111/114 | 0.937 | 1.07 / 0.943 | 0.905 / 0.3963 | 0.895 / 0.3094 | 1.01 / 0.8016 | 0.895 / 0.3094 |
| kannada_wiktionary | loose | wide | 111/114 | 2.49 | 2.65 / 0.8761 | 2.29 / 0.1924 | 2.11 / 0.0679 | 2.39 / 0.2314 | 2.11 / 0.0679 |
| santali_campbell | strict | narrow | 114/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.022 / 1.0 | 0 / 1.0 | 0.022 / 1.0 |
| santali_campbell | strict | wide | 114/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.062 / 1.0 | 0 / 1.0 | 0.062 / 1.0 |
| santali_campbell | medium | narrow | 114/114 | 1.38 | 1.07 / 0.014 | 0.979 / 0.1184 | 0.957 / 0.0599 | 0.901 / 0.0005 | 0.957 / 0.0599 |
| santali_campbell | medium | wide | 114/114 | 2.24 | 1.97 / 0.1004 | 2.05 / 0.3208 | 2 / 0.2295 | 1.8 / 0.0135 | 2 / 0.2295 |
| santali_campbell | loose | narrow | 114/114 | 1.08 | 1.09 / 0.6967 | 1.03 / 0.2139 | 1.01 / 0.0818 | 0.995 / 0.0665 | 1.01 / 0.0818 |
| santali_campbell | loose | wide | 114/114 | 2.26 | 2.28 / 0.7706 | 2.17 / 0.2569 | 2.1 / 0.0459 | 2.12 / 0.04 | 2.1 / 0.0459 |
| santali_bodding5 | strict | narrow | 97/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| santali_bodding5 | strict | wide | 97/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| santali_bodding5 | medium | narrow | 97/114 | 0.094 | 0.072 / 0.2439 | 0.18 / 0.5577 | 0.451 / 0.6727 | 0.064 / 0.2039 | 0.451 / 0.6727 |
| santali_bodding5 | medium | wide | 97/114 | 0.26 | 0.305 / 0.5062 | 0.717 / 0.6817 | 0.933 / 0.7505 | 0.578 / 1.0 | 0.933 / 0.7505 |
| santali_bodding5 | loose | narrow | 97/114 | 0.511 | 0.455 / 0.1784 | 0.355 / 0.1519 | 0.614 / 0.6786 | 0.391 / 0.1459 | 0.614 / 0.6786 |
| santali_bodding5 | loose | wide | 97/114 | 1.05 | 1.12 / 0.6767 | 0.82 / 0.1864 | 1.3 / 0.8004 | 1.06 / 0.4338 | 1.3 / 0.8004 |
| santali_wiktionary | strict | narrow | 100/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.135 / 1.0 | 0 / 1.0 | 0.244 / 1.0 |
| santali_wiktionary | strict | wide | 100/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.317 / 1.0 | 0 / 1.0 | 0.481 / 1.0 |
| santali_wiktionary | medium | narrow | 100/114 | 1.17 | 0.418 / 0.044 | 0.564 / 0.1344 | 0.594 / 0.1537 | 0.17 / 0.0005 | 0.593 / 0.1457 |
| santali_wiktionary | medium | wide | 100/114 | 1.76 | 1.06 / 0.0905 | 1.01 / 0.1444 | 1.19 / 0.2116 | 0.43 / 0.0005 | 1.21 / 0.2295 |
| santali_wiktionary | loose | narrow | 100/114 | 0.533 | 0.768 / 0.9735 | 0.688 / 0.7711 | 0.823 / 0.9102 | 0.824 / 0.9905 | 0.844 / 0.9321 |
| santali_wiktionary | loose | wide | 100/114 | 1.5 | 1.81 / 0.9175 | 1.62 / 0.5982 | 1.7 / 0.6786 | 1.74 / 0.8701 | 1.72 / 0.7086 |
| mundari_bhadra | strict | narrow | 114/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.376 / 1.0 | 0 / 1.0 | 0.376 / 1.0 |
| mundari_bhadra | strict | wide | 114/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.77 / 1.0 | 0 / 1.0 | 0.77 / 1.0 |
| mundari_bhadra | medium | narrow | 114/114 | 1.19 | 1 / 0.0645 | 1.13 / 0.3498 | 1.17 / 0.4052 | 0.786 / 0.0005 | 1.17 / 0.4052 |
| mundari_bhadra | medium | wide | 114/114 | 2.56 | 2.48 / 0.3498 | 2.19 / 0.2649 | 2.55 / 0.4691 | 2.62 / 0.4983 | 2.55 / 0.4691 |
| mundari_bhadra | loose | narrow | 114/114 | 1.2 | 1.18 / 0.3813 | 1.02 / 0.0515 | 1.2 / 0.501 | 1.05 / 0.0465 | 1.2 / 0.501 |
| mundari_bhadra | loose | wide | 114/114 | 2.58 | 2.49 / 0.0985 | 2.22 / 0.0345 | 2.64 / 0.6467 | 2.39 / 0.074 | 2.64 / 0.6467 |
| sanskrit_mw | strict | narrow | 114/114 | 1.31 | 1.3 / 0.3938 | 0.997 / 0.1859 | 1.33 / 0.4371 | 1.23 / 0.2904 | 1.33 / 0.4371 |
| sanskrit_mw | strict | wide | 114/114 | 2.25 | 2.55 / 0.7896 | 2.53 / 0.6462 | 2.66 / 0.8303 | 2.51 / 0.7491 | 2.66 / 0.8303 |
| sanskrit_mw | medium | narrow | 114/114 | 1.11 | 1.08 / 0.2969 | 1.13 / 0.5117 | 1.34 / 0.998 | 1.03 / 0.1589 | 1.34 / 0.998 |
| sanskrit_mw | medium | wide | 114/114 | 2.33 | 2.38 / 0.6522 | 2.48 / 0.7746 | 2.72 / 1.0 | 2.36 / 0.5952 | 2.72 / 1.0 |
| sanskrit_mw | loose | narrow | 114/114 | 1.24 | 1.25 / 0.7606 | 1.18 / 0.0585 | 1.35 / 1.0 | 1.15 / 0.0955 | 1.35 / 1.0 |
| sanskrit_mw | loose | wide | 114/114 | 2.67 | 2.72 / 0.9385 | 2.63 / 0.2369 | 2.74 / 0.996 | 2.61 / 0.3003 | 2.74 / 0.996 |
| oia_turner | strict | narrow | 113/114 | 0.083 | 0.026 / 0.1304 | 0.719 / 0.6437 | 0.611 / 0.6786 | 0.017 / 0.0095 | 0.611 / 0.6786 |
| oia_turner | strict | wide | 113/114 | 0.083 | 0.694 / 0.6592 | 1.51 / 0.8191 | 1.39 / 0.9202 | 1.08 / 0.7881 | 1.39 / 0.9202 |
| oia_turner | medium | narrow | 113/114 | 0.583 | 0.635 / 0.5877 | 0.818 / 0.5982 | 0.789 / 0.6627 | 0.608 / 0.5697 | 0.789 / 0.6627 |
| oia_turner | medium | wide | 113/114 | 1.66 | 2.1 / 0.8036 | 1.88 / 0.5357 | 1.81 / 0.5689 | 2.19 / 0.8531 | 1.81 / 0.5689 |
| oia_turner | loose | narrow | 113/114 | 0.826 | 0.832 / 0.5307 | 0.748 / 0.1904 | 0.806 / 0.3812 | 0.734 / 0.0105 | 0.806 / 0.3812 |
| oia_turner | loose | wide | 113/114 | 1.86 | 1.87 / 0.6362 | 1.7 / 0.1634 | 1.85 / 0.4491 | 1.79 / 0.2269 | 1.85 / 0.4491 |
| proto_indoiranian_wiktionary | strict | narrow | 93/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.141 / 1.0 | 0 / 1.0 | 0.141 / 1.0 |
| proto_indoiranian_wiktionary | strict | wide | 93/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.382 / 1.0 | 0 / 1.0 | 0.382 / 1.0 |
| proto_indoiranian_wiktionary | medium | narrow | 93/114 | 0 | 0.079 / 1.0 | 0.086 / 1.0 | 0.445 / 1.0 | 0.101 / 1.0 | 0.445 / 1.0 |
| proto_indoiranian_wiktionary | medium | wide | 93/114 | 1 | 0.78 / 0.3943 | 0.928 / 0.3178 | 1.12 / 0.4012 | 0.592 / 0.1469 | 1.12 / 0.4012 |
| proto_indoiranian_wiktionary | loose | narrow | 93/114 | 1.45 | 1.54 / 0.6032 | 0.793 / 0.067 | 0.793 / 0.0319 | 1.44 / 0.4518 | 0.793 / 0.0319 |
| proto_indoiranian_wiktionary | loose | wide | 93/114 | 2.88 | 3.32 / 0.7741 | 1.79 / 0.058 | 2.02 / 0.0778 | 3.26 / 0.7801 | 2.02 / 0.0778 |
| sumerian_halloran | strict | narrow | 107/114 | 1.44 | 1.29 / 0.2474 | 0.718 / 0.0985 | 1.64 / 0.6028 | 1.16 / 0.1084 | 1.86 / 0.7924 |
| sumerian_halloran | strict | wide | 107/114 | 3.43 | 3.02 / 0.1239 | 2.26 / 0.1214 | 3.74 / 0.6008 | 3.03 / 0.1284 | 3.98 / 0.7565 |
| sumerian_halloran | medium | narrow | 107/114 | 1.98 | 1.95 / 0.4083 | 1.8 / 0.2854 | 1.78 / 0.1776 | 1.69 / 0.089 | 1.93 / 0.3733 |
| sumerian_halloran | medium | wide | 107/114 | 4.17 | 4.08 / 0.3523 | 4.06 / 0.3983 | 4 / 0.2735 | 3.78 / 0.0585 | 4.15 / 0.4331 |
| sumerian_halloran | loose | narrow | 107/114 | 1.89 | 1.97 / 0.7106 | 1.65 / 0.1129 | 1.9 / 0.519 | 1.8 / 0.2659 | 1.94 / 0.7066 |
| sumerian_halloran | loose | wide | 107/114 | 4.21 | 4.32 / 0.7411 | 4.05 / 0.3513 | 4.19 / 0.4092 | 4.08 / 0.2524 | 4.22 / 0.499 |
| sumerian_wiktionary | strict | narrow | 102/114 | 0.412 | 0.446 / 0.5697 | 0.618 / 0.4578 | 1.1 / 0.8303 | 0.313 / 0.2599 | 1.1 / 0.8343 |
| sumerian_wiktionary | strict | wide | 102/114 | 0.622 | 1.64 / 0.9315 | 2.04 / 0.8011 | 2.61 / 0.988 | 2.76 / 0.99 | 2.64 / 0.984 |
| sumerian_wiktionary | medium | narrow | 102/114 | 1.68 | 1.51 / 0.2369 | 1.57 / 0.3818 | 1.3 / 0.1397 | 1.13 / 0.001 | 1.29 / 0.1577 |
| sumerian_wiktionary | medium | wide | 102/114 | 2.93 | 2.96 / 0.5297 | 3.47 / 0.6272 | 3.04 / 0.525 | 2.58 / 0.1024 | 3.05 / 0.523 |
| sumerian_wiktionary | loose | narrow | 102/114 | 1.47 | 1.32 / 0.0965 | 1.3 / 0.2704 | 1.32 / 0.1577 | 1.17 / 0.0015 | 1.35 / 0.2016 |
| sumerian_wiktionary | loose | wide | 102/114 | 3.19 | 3.02 / 0.1359 | 2.88 / 0.2689 | 3.12 / 0.3992 | 2.76 / 0.0025 | 3.16 / 0.4571 |
| akkadian_wiktionary | strict | narrow | 97/114 | 0 | 0.103 / 1.0 | 0 / 1.0 | 0.754 / 1.0 | 0.134 / 1.0 | 0.754 / 1.0 |
| akkadian_wiktionary | strict | wide | 97/114 | 1.25 | 0.428 / 0.0485 | 0 / 0.0005 | 1.35 / 0.4251 | 0.362 / 0.026 | 1.35 / 0.4251 |
| akkadian_wiktionary | medium | narrow | 97/114 | 0.675 | 0.696 / 0.4498 | 1.08 / 0.5452 | 1.3 / 0.7745 | 0.704 / 0.4513 | 1.3 / 0.7745 |
| akkadian_wiktionary | medium | wide | 97/114 | 2.14 | 1.64 / 0.081 | 1.69 / 0.2654 | 2.51 / 0.5429 | 1.44 / 0.0155 | 2.51 / 0.5429 |
| akkadian_wiktionary | loose | narrow | 97/114 | 1.57 | 1.82 / 0.8751 | 1.44 / 0.3533 | 1.66 / 0.5749 | 1.61 / 0.5917 | 1.66 / 0.5749 |
| akkadian_wiktionary | loose | wide | 97/114 | 3.55 | 3.84 / 0.8476 | 3.13 / 0.2664 | 3.31 / 0.2794 | 3.44 / 0.2929 | 3.31 / 0.2794 |
| elamite_hinzkoch | strict | narrow | 72/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| elamite_hinzkoch | strict | wide | 72/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.006 / 1.0 | 0 / 1.0 | 0.006 / 1.0 |
| elamite_hinzkoch | medium | narrow | 72/114 | 0.238 | 0.201 / 0.3333 | 0.062 / 0.096 | 0.113 / 0.1337 | 0.213 / 0.3763 | 0.113 / 0.1337 |
| elamite_hinzkoch | medium | wide | 72/114 | 0.238 | 0.227 / 0.4098 | 0.264 / 0.3548 | 0.622 / 0.6707 | 0.247 / 0.4973 | 0.622 / 0.6707 |
| elamite_hinzkoch | loose | narrow | 72/114 | 0.169 | 0.142 / 0.2439 | 0.073 / 0.1114 | 0.121 / 0.1597 | 0.14 / 0.2309 | 0.121 / 0.1597 |
| elamite_hinzkoch | loose | wide | 72/114 | 1.2 **all 4** | 0.91 / 0.0055 | 0.281 / 0.0025 | 0.779 / 0.0319 | 0.855 / 0.001 | 0.779 / 0.0319 |
| burushaski_lorimer | strict | narrow | 83/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| burushaski_lorimer | strict | wide | 83/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| burushaski_lorimer | medium | narrow | 83/114 | 0 | 0.01 / 1.0 | 0.634 / 1.0 | 0.432 / 1.0 | 0.011 / 1.0 | 0.432 / 1.0 |
| burushaski_lorimer | medium | wide | 83/114 | 1.15 | 0.741 / 0.2334 | 1.15 / 0.3928 | 0.887 / 0.2814 | 0.417 / 0.083 | 0.887 / 0.2814 |
| burushaski_lorimer | loose | narrow | 83/114 | 0.305 | 0.343 / 0.6832 | 0.718 / 0.911 | 0.585 / 0.9501 | 0.32 / 0.4813 | 0.585 / 0.9501 |
| burushaski_lorimer | loose | wide | 83/114 | 0.998 | 1.05 / 0.5842 | 1.46 / 0.7616 | 1.24 / 0.7385 | 1.01 / 0.4613 | 1.24 / 0.7385 |

#### A_3of3: hits, every family and every dictionary, full grid

| dictionary / family | distance | keywords | units covered | hits | C1 classes dealt mean / P | C2 outside nouns mean / P | C3 sounds dealt by entry mean / P | C4 wrong class same picture mean / P | C3row mean / P |
|---|---|---|---|---|---|---|---|---|---|
| FAMILY Dravidian | strict | narrow | 114/114 | 55 | 60.6 / 0.955 | 35.4 / 0.0115 | 76.7 / 1.0 | 59.6 / 0.934 | 81 / 0.998 |
| FAMILY Dravidian | strict | wide | 114/114 | 94 | 93.2 / 0.4738 | 62.3 / 0.001 | 94.2 / 0.5609 | 90.2 / 0.1449 | 97.1 / 0.7864 |
| FAMILY Dravidian | medium | narrow | 114/114 | 108 | 108 / 0.5362 | 96.5 / 0.0125 | 109 / 0.7725 | 107 / 0.4873 | 110 / 0.8643 |
| FAMILY Dravidian | medium | wide | 114/114 | 114 | 113 / 0.2034 | 110 / 0.045 | 113 / 0.3293 | 112 / 0.0635 | 113 / 0.3373 |
| FAMILY Dravidian | loose | narrow | 114/114 | 114 | 114 / 1.0 | 114 / 0.8476 | 114 / 0.994 | 114 / 1.0 | 114 / 0.996 |
| FAMILY Dravidian | loose | wide | 114/114 | 114 | 114 / 1.0 | 114 / 0.9025 | 114 / 1.0 | 114 / 1.0 | 114 / 1.0 |
| FAMILY Munda | strict | narrow | 114/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.772 / 1.0 | 0 / 1.0 | 0.93 / 1.0 |
| FAMILY Munda | strict | wide | 114/114 | 0 | 0 / 1.0 | 0 / 1.0 | 1.63 / 1.0 | 0 / 1.0 | 1.85 / 1.0 |
| FAMILY Munda | medium | narrow | 114/114 | 69 | 70.2 / 0.6932 | 40.9 / 0.0025 | 60.2 / 0.1218 | 68.3 / 0.4843 | 60.1 / 0.1138 |
| FAMILY Munda | medium | wide | 114/114 | 86 | 87.9 / 0.7716 | 63.1 / 0.0105 | 84 / 0.4212 | 87.7 / 0.7841 | 84 / 0.4251 |
| FAMILY Munda | loose | narrow | 114/114 | 114 | 113 / 0.5667 | 108 / 0.0385 | 112 / 0.2375 | 113 / 0.5157 | 112 / 0.2275 |
| FAMILY Munda | loose | wide | 114/114 | 114 | 114 / 0.7951 | 110 / 0.1359 | 114 / 0.7246 | 114 / 0.7956 | 114 / 0.7186 |
| FAMILY Indo-Aryan | strict | narrow | 114/114 | 49 | 47.4 / 0.3808 | 20.8 / 0.0005 | 56.5 / 0.9261 | 46.7 / 0.2769 | 56.5 / 0.9261 |
| FAMILY Indo-Aryan | strict | wide | 114/114 | 67 | 67.8 / 0.6337 | 39.4 / 0.003 | 74 / 0.8882 | 65 / 0.3303 | 74 / 0.8882 |
| FAMILY Indo-Aryan | medium | narrow | 114/114 | 96 | 94 / 0.2754 | 87.2 / 0.1119 | 102 / 0.976 | 93.7 / 0.2434 | 102 / 0.976 |
| FAMILY Indo-Aryan | medium | wide | 114/114 | 104 | 103 / 0.4523 | 103 / 0.4843 | 108 / 0.982 | 103 / 0.4458 | 108 / 0.982 |
| FAMILY Indo-Aryan | loose | narrow | 114/114 | 114 | 114 / 1.0 | 113 / 0.7161 | 114 / 0.9281 | 114 / 1.0 | 114 / 0.9281 |
| FAMILY Indo-Aryan | loose | wide | 114/114 | 114 | 114 / 1.0 | 114 / 0.7896 | 114 / 0.996 | 114 / 1.0 | 114 / 0.996 |
| FAMILY Sumerian | strict | narrow | 108/114 | 35 | 35.9 / 0.6402 | 13.4 / 0.004 | 46 / 0.9681 | 31.7 / 0.1904 | 48.7 / 0.99 |
| FAMILY Sumerian | strict | wide | 108/114 | 65 | 59.1 / 0.0455 | 29.4 / 0.001 | 65.9 / 0.6108 | 58.2 / 0.007 | 69 / 0.7265 |
| FAMILY Sumerian | medium | narrow | 108/114 | 83 | 81.1 / 0.3333 | 54.4 / 0.0045 | 82 / 0.4611 | 76.7 / 0.027 | 85.5 / 0.7525 |
| FAMILY Sumerian | medium | wide | 108/114 | 96 | 95.7 / 0.5297 | 73 / 0.014 | 94.8 / 0.4371 | 95.3 / 0.4608 | 97.5 / 0.7206 |
| FAMILY Sumerian | loose | narrow | 108/114 | 104 | 103 / 0.3223 | 95.9 / 0.1984 | 103 / 0.4351 | 102 / 0.1389 | 104 / 0.5888 |
| FAMILY Sumerian | loose | wide | 108/114 | 104 | 104 / 0.7931 | 99.5 / 0.3493 | 106 / 0.8882 | 104 / 0.7661 | 106 / 0.9301 |
| FAMILY Akkadian | strict | narrow | 97/114 | 0 | 0.257 / 1.0 | 0 / 1.0 | 2.49 / 1.0 | 0.336 / 1.0 | 2.49 / 1.0 |
| FAMILY Akkadian | strict | wide | 97/114 | 3 | 1.02 / 0.06 | 0 / 0.0005 | 4.33 / 0.5689 | 0.789 / 0.027 | 4.33 / 0.5689 |
| FAMILY Akkadian | medium | narrow | 97/114 | 12 | 12.2 / 0.6047 | 4.72 / 0.077 | 14.6 / 0.7026 | 11.7 / 0.5412 | 14.6 / 0.7026 |
| FAMILY Akkadian | medium | wide | 97/114 | 26 | 22.9 / 0.093 | 6.79 / 0.002 | 22.8 / 0.3413 | 20.9 / 0.012 | 22.8 / 0.3413 |
| FAMILY Akkadian | loose | narrow | 97/114 | 65 | 65.9 / 0.6812 | 48.3 / 0.094 | 61.9 / 0.3932 | 62.9 / 0.2694 | 61.9 / 0.3932 |
| FAMILY Akkadian | loose | wide | 97/114 | 78 | 79.2 / 0.7871 | 61.4 / 0.1099 | 74.3 / 0.3812 | 77.8 / 0.5512 | 74.3 / 0.3812 |
| FAMILY Elamite | strict | narrow | 72/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| FAMILY Elamite | strict | wide | 72/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.006 / 1.0 | 0 / 1.0 | 0.006 / 1.0 |
| FAMILY Elamite | medium | narrow | 72/114 | 2 | 1.28 / 0.3658 | 0.585 / 0.1374 | 0.932 / 0.1936 | 1.29 / 0.3893 | 0.932 / 0.1936 |
| FAMILY Elamite | medium | wide | 72/114 | 2 | 1.63 / 0.5037 | 1.48 / 0.3448 | 5.28 / 0.8144 | 1.75 / 0.5687 | 5.28 / 0.8144 |
| FAMILY Elamite | loose | narrow | 72/114 | 13 | 15.7 / 0.8841 | 5.11 / 0.087 | 18.6 / 0.8263 | 17.6 / 0.975 | 18.6 / 0.8263 |
| FAMILY Elamite | loose | wide | 72/114 | 50 | 40.5 / 0.003 | 11.6 / 0.001 | 44.2 / 0.2016 | 37.4 / 0.0005 | 44.2 / 0.2016 |
| FAMILY Burushaski | strict | narrow | 83/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| FAMILY Burushaski | strict | wide | 83/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| FAMILY Burushaski | medium | narrow | 83/114 | 0 | 0.05 / 1.0 | 1.31 / 1.0 | 3.2 / 1.0 | 0.054 / 1.0 | 3.2 / 1.0 |
| FAMILY Burushaski | medium | wide | 83/114 | 3 | 2.18 / 0.3693 | 3.47 / 0.5222 | 6.14 / 0.7066 | 1.76 / 0.2514 | 6.14 / 0.7066 |
| FAMILY Burushaski | loose | narrow | 83/114 | 31 | 31.7 / 0.6817 | 24.8 / 0.2444 | 34.7 / 0.7305 | 30.5 / 0.4973 | 34.7 / 0.7305 |
| FAMILY Burushaski | loose | wide | 83/114 | 43 | 45.9 / 0.9225 | 41.2 / 0.4403 | 47.4 / 0.6806 | 47.4 / 0.994 | 47.4 / 0.6806 |
| dedr_tamil | strict | narrow | 114/114 | 39 | 45.2 / 0.971 | 16 / 0.001 | 64.2 / 0.996 | 44 / 0.957 | 69.6 / 1.0 |
| dedr_tamil | strict | wide | 114/114 | 69 | 74.9 / 0.9625 | 37.4 / 0.002 | 78.3 / 0.8822 | 73.8 / 0.9545 | 82.6 / 0.9341 |
| dedr_tamil | medium | narrow | 114/114 | 93 | 95.7 / 0.8576 | 74.7 / 0.0055 | 99.5 / 0.9341 | 95.3 / 0.8336 | 101 / 0.9701 |
| dedr_tamil | medium | wide | 114/114 | 109 | 109 / 0.5687 | 97.2 / 0.024 | 109 / 0.5749 | 109 / 0.6587 | 110 / 0.7465 |
| dedr_tamil | loose | narrow | 114/114 | 114 | 114 / 0.5977 | 111 / 0.2234 | 113 / 0.6228 | 114 / 0.5932 | 114 / 0.7645 |
| dedr_tamil | loose | wide | 114/114 | 114 | 114 / 0.8851 | 112 / 0.3823 | 114 / 0.7964 | 114 / 0.8771 | 114 / 0.9162 |
| dedr_malayalam | strict | narrow | 111/114 | 20 | 17.5 / 0.2919 | 4.86 / 0.002 | 14 / 0.1776 | 16 / 0.0995 | 15.1 / 0.2515 |
| dedr_malayalam | strict | wide | 111/114 | 45 | 41.5 / 0.2374 | 12.5 / 0.0005 | 29.9 / 0.024 | 36.1 / 0.009 | 30.8 / 0.0459 |
| dedr_malayalam | medium | narrow | 111/114 | 77 | 81.8 / 0.937 | 43.8 / 0.0005 | 71.1 / 0.2076 | 79.5 / 0.7996 | 71.9 / 0.2236 |
| dedr_malayalam | medium | wide | 111/114 | 98 | 99.2 / 0.8086 | 69.8 / 0.002 | 93.6 / 0.2096 | 97.1 / 0.4493 | 94.1 / 0.2216 |
| dedr_malayalam | loose | narrow | 111/114 | 108 | 109 / 0.9365 | 103 / 0.2104 | 109 / 0.8683 | 109 / 0.955 | 109 / 0.8703 |
| dedr_malayalam | loose | wide | 111/114 | 110 | 110 / 0.8841 | 108 / 0.3943 | 110 / 0.8982 | 110 / 0.8631 | 110 / 0.8902 |
| dedr_kannada | strict | narrow | 109/114 | 22 | 20.1 / 0.3278 | 7.7 / 0.0025 | 20.8 / 0.4671 | 19.3 / 0.2224 | 25.8 / 0.8004 |
| dedr_kannada | strict | wide | 109/114 | 40 | 40.9 / 0.6437 | 16.6 / 0.0015 | 37.2 / 0.3453 | 38.3 / 0.3623 | 42.2 / 0.6467 |
| dedr_kannada | medium | narrow | 109/114 | 80 | 76.4 / 0.1879 | 42.3 / 0.001 | 66.1 / 0.022 | 71.1 / 0.0035 | 74.6 / 0.2096 |
| dedr_kannada | medium | wide | 109/114 | 96 | 93.8 / 0.2719 | 68.7 / 0.0035 | 89.6 / 0.1357 | 89.4 / 0.01 | 96.9 / 0.6487 |
| dedr_kannada | loose | narrow | 109/114 | 106 | 107 / 0.919 | 97.6 / 0.1614 | 107 / 0.8523 | 107 / 0.9655 | 108 / 0.994 |
| dedr_kannada | loose | wide | 109/114 | 109 | 109 / 0.6877 | 101 / 0.1574 | 109 / 0.8623 | 109 / 0.6077 | 109 / 0.9681 |
| dedr_telugu | strict | narrow | 112/114 | 16 | 10.4 / 0.014 | 4.04 / 0.0145 | 12.6 / 0.3493 | 8.25 / 0.0005 | 14.9 / 0.481 |
| dedr_telugu | strict | wide | 112/114 | 25 | 21.3 / 0.1204 | 8.19 / 0.0055 | 21.3 / 0.3353 | 17.7 / 0.0025 | 26.2 / 0.6008 |
| dedr_telugu | medium | narrow | 112/114 | 52 | 50.8 / 0.4233 | 22.3 / 0.0005 | 47.1 / 0.2355 | 48.8 / 0.2334 | 52.9 / 0.5788 |
| dedr_telugu | medium | wide | 112/114 | 80 | 77.1 / 0.2529 | 43.7 / 0.0005 | 69 / 0.0798 | 73.6 / 0.035 | 74.1 / 0.1976 |
| dedr_telugu | loose | narrow | 112/114 | 100 | 103 / 0.955 | 88.1 / 0.09 | 104 / 0.8902 | 105 / 0.995 | 105 / 0.9042 |
| dedr_telugu | loose | wide | 112/114 | 110 | 109 / 0.5097 | 97.6 / 0.0445 | 111 / 0.7784 | 109 / 0.4438 | 110 / 0.6926 |
| tamil_wiktionary | strict | narrow | 113/114 | 31 | 33.6 / 0.8021 | 12.7 / 0.0005 | 33.1 / 0.6747 | 31.6 / 0.6192 | 32.8 / 0.6826 |
| tamil_wiktionary | strict | wide | 113/114 | 52 | 55.6 / 0.8756 | 25.2 / 0.0005 | 47.9 / 0.2954 | 51.9 / 0.5482 | 47.8 / 0.2695 |
| tamil_wiktionary | medium | narrow | 113/114 | 84 | 90.2 / 0.975 | 64.9 / 0.0075 | 83.3 / 0.483 | 90.2 / 0.986 | 83.2 / 0.505 |
| tamil_wiktionary | medium | wide | 113/114 | 103 | 102 / 0.5092 | 87.8 / 0.0235 | 100 / 0.3453 | 100 / 0.1629 | 100 / 0.3373 |
| tamil_wiktionary | loose | narrow | 113/114 | 112 | 112 / 0.7526 | 111 / 0.5277 | 112 / 0.7246 | 112 / 0.6862 | 112 / 0.7166 |
| tamil_wiktionary | loose | wide | 113/114 | 113 | 113 / 1.0 | 113 / 0.6747 | 113 / 0.7944 | 113 / 1.0 | 113 / 0.7345 |
| telugu_wiktionary | strict | narrow | 114/114 | 16 | 14 / 0.2629 | 3.61 / 0.0015 | 26.4 / 0.996 | 11.2 / 0.03 | 26.6 / 1.0 |
| telugu_wiktionary | strict | wide | 114/114 | 24 | 20.3 / 0.1149 | 6.16 / 0.0015 | 34.4 / 0.996 | 16.8 / 0.0035 | 34.8 / 1.0 |
| telugu_wiktionary | medium | narrow | 114/114 | 62 | 58.9 / 0.2424 | 36.2 / 0.0005 | 64.9 / 0.7026 | 55 / 0.0225 | 65.1 / 0.6986 |
| telugu_wiktionary | medium | wide | 114/114 | 74 | 74.1 / 0.5662 | 55.1 / 0.023 | 83.4 / 0.9281 | 73 / 0.4308 | 83.7 / 0.9501 |
| telugu_wiktionary | loose | narrow | 114/114 | 109 | 111 / 0.943 | 108 / 0.4988 | 110 / 0.7246 | 111 / 0.964 | 110 / 0.7525 |
| telugu_wiktionary | loose | wide | 114/114 | 111 | 112 / 0.8456 | 111 / 0.6722 | 112 / 0.8962 | 112 / 0.8286 | 112 / 0.8723 |
| kannada_wiktionary | strict | narrow | 111/114 | 0 | 0 / 1.0 | 0 / 1.0 | 1.26 / 1.0 | 0 / 1.0 | 1.26 / 1.0 |
| kannada_wiktionary | strict | wide | 111/114 | 0 | 0.104 / 1.0 | 1.06 / 1.0 | 3.03 / 1.0 | 0.122 / 1.0 | 3.03 / 1.0 |
| kannada_wiktionary | medium | narrow | 111/114 | 25 | 27.7 / 0.8196 | 13.2 / 0.0285 | 15.3 / 0.0818 | 27.7 / 0.8306 | 15.3 / 0.0818 |
| kannada_wiktionary | medium | wide | 111/114 | 53 | 54.8 / 0.7206 | 27.5 / 0.0035 | 27.8 / 0.002 | 51.2 / 0.3593 | 27.8 / 0.002 |
| kannada_wiktionary | loose | narrow | 111/114 | 83 | 87.2 / 0.9255 | 78.8 / 0.3733 | 75.9 / 0.2156 | 87 / 0.954 | 75.9 / 0.2156 |
| kannada_wiktionary | loose | wide | 111/114 | 102 | 103 / 0.7591 | 93.7 / 0.1789 | 91.7 / 0.0639 | 101 / 0.3548 | 91.7 / 0.0639 |
| santali_campbell | strict | narrow | 114/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.022 / 1.0 | 0 / 1.0 | 0.022 / 1.0 |
| santali_campbell | strict | wide | 114/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.062 / 1.0 | 0 / 1.0 | 0.062 / 1.0 |
| santali_campbell | medium | narrow | 114/114 | 51 | 51.4 / 0.5902 | 28.6 / 0.0055 | 46.4 / 0.2834 | 51.1 / 0.5817 | 46.4 / 0.2834 |
| santali_campbell | medium | wide | 114/114 | 72 | 72 / 0.5497 | 47.2 / 0.008 | 68.1 / 0.3353 | 71.7 / 0.5367 | 68.1 / 0.3353 |
| santali_campbell | loose | narrow | 114/114 | 112 | 113 / 0.8596 | 101 / 0.0285 | 108 / 0.0998 | 112 / 0.8301 | 108 / 0.0998 |
| santali_campbell | loose | wide | 114/114 | 114 | 114 / 0.6552 | 104 / 0.014 | 111 / 0.1457 | 114 / 0.6247 | 111 / 0.1457 |
| santali_bodding5 | strict | narrow | 97/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| santali_bodding5 | strict | wide | 97/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| santali_bodding5 | medium | narrow | 97/114 | 2 | 0.906 / 0.2224 | 1.67 / 0.4558 | 3.65 / 0.6427 | 0.698 / 0.1274 | 3.65 / 0.6427 |
| santali_bodding5 | medium | wide | 97/114 | 3 | 2.74 / 0.5522 | 4.01 / 0.6332 | 7.01 / 0.7944 | 3.32 / 0.7686 | 7.01 / 0.7944 |
| santali_bodding5 | loose | narrow | 97/114 | 29 | 26.6 / 0.2729 | 20.2 / 0.1444 | 43.6 / 0.9681 | 24.5 / 0.1004 | 43.6 / 0.9681 |
| santali_bodding5 | loose | wide | 97/114 | 46 | 47.5 / 0.7401 | 37.2 / 0.2529 | 61.9 / 0.9621 | 43.9 / 0.2964 | 61.9 / 0.9621 |
| santali_wiktionary | strict | narrow | 100/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.176 / 1.0 | 0 / 1.0 | 0.318 / 1.0 |
| santali_wiktionary | strict | wide | 100/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.404 / 1.0 | 0 / 1.0 | 0.602 / 1.0 |
| santali_wiktionary | medium | narrow | 100/114 | 3 | 1.46 / 0.1614 | 2.98 / 0.4633 | 4.92 / 0.5808 | 1 / 0.0525 | 4.62 / 0.5569 |
| santali_wiktionary | medium | wide | 100/114 | 11 | 9.64 / 0.3553 | 5.4 / 0.1064 | 8.89 / 0.3952 | 7.47 / 0.0575 | 8.5 / 0.3573 |
| santali_wiktionary | loose | narrow | 100/114 | 41 | 44.1 / 0.8786 | 29.8 / 0.1029 | 39.8 / 0.4531 | 47.4 / 0.981 | 39.6 / 0.4451 |
| santali_wiktionary | loose | wide | 100/114 | 65 | 67.6 / 0.8196 | 48 / 0.0535 | 54.9 / 0.0958 | 68.4 / 0.9085 | 55.3 / 0.0938 |
| mundari_bhadra | strict | narrow | 114/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.59 / 1.0 | 0 / 1.0 | 0.59 / 1.0 |
| mundari_bhadra | strict | wide | 114/114 | 0 | 0 / 1.0 | 0 / 1.0 | 1.19 / 1.0 | 0 / 1.0 | 1.19 / 1.0 |
| mundari_bhadra | medium | narrow | 114/114 | 50 | 46.6 / 0.2009 | 19.5 / 0.0005 | 35 / 0.0319 | 40.2 / 0.0045 | 35 / 0.0319 |
| mundari_bhadra | medium | wide | 114/114 | 66 | 65.9 / 0.5437 | 33.7 / 0.0005 | 56.3 / 0.1377 | 64 / 0.3338 | 56.3 / 0.1377 |
| mundari_bhadra | loose | narrow | 114/114 | 109 | 109 / 0.6362 | 87.9 / 0.0015 | 105 / 0.1657 | 109 / 0.6452 | 105 / 0.1657 |
| mundari_bhadra | loose | wide | 114/114 | 114 | 113 / 0.1829 | 97.3 / 0.0005 | 110 / 0.0319 | 112 / 0.0615 | 110 / 0.0319 |
| sanskrit_mw | strict | narrow | 114/114 | 48 | 47.1 / 0.4568 | 20.3 / 0.0015 | 55.8 / 0.9381 | 46.5 / 0.3668 | 55.8 / 0.9381 |
| sanskrit_mw | strict | wide | 114/114 | 66 | 67.5 / 0.6937 | 38.5 / 0.003 | 73 / 0.8922 | 64.8 / 0.4218 | 73 / 0.8922 |
| sanskrit_mw | medium | narrow | 114/114 | 96 | 93.8 / 0.2579 | 85.7 / 0.082 | 101 / 0.9641 | 93.6 / 0.2299 | 101 / 0.9641 |
| sanskrit_mw | medium | wide | 114/114 | 104 | 103 / 0.3803 | 102 / 0.4553 | 108 / 0.9601 | 103 / 0.3378 | 108 / 0.9601 |
| sanskrit_mw | loose | narrow | 114/114 | 114 | 114 / 1.0 | 113 / 0.7161 | 114 / 0.8623 | 114 / 1.0 | 114 / 0.8623 |
| sanskrit_mw | loose | wide | 114/114 | 114 | 114 / 1.0 | 114 / 0.7896 | 114 / 0.98 | 114 / 1.0 | 114 / 0.98 |
| oia_turner | strict | narrow | 113/114 | 1 | 0.323 / 0.2889 | 1.62 / 0.6437 | 1.81 / 0.6966 | 0.218 / 0.2089 | 1.81 / 0.6966 |
| oia_turner | strict | wide | 113/114 | 1 | 1.25 / 0.7556 | 2.87 / 0.8191 | 4.2 / 0.9301 | 1.7 / 0.8551 | 4.2 / 0.9301 |
| oia_turner | medium | narrow | 113/114 | 13 | 12.1 / 0.4363 | 8.36 / 0.1759 | 15.5 / 0.6866 | 11.3 / 0.2724 | 15.5 / 0.6866 |
| oia_turner | medium | wide | 113/114 | 23 | 24.4 / 0.7066 | 16.8 / 0.1824 | 30.4 / 0.8483 | 23.3 / 0.5942 | 30.4 / 0.8483 |
| oia_turner | loose | narrow | 113/114 | 101 | 96.8 / 0.0745 | 86.8 / 0.0405 | 104 / 0.8283 | 93.2 / 0.0015 | 104 / 0.8283 |
| oia_turner | loose | wide | 113/114 | 105 | 106 / 0.8371 | 99.4 / 0.2449 | 110 / 0.98 | 105 / 0.7481 | 110 / 0.98 |
| proto_indoiranian_wiktionary | strict | narrow | 93/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.174 / 1.0 | 0 / 1.0 | 0.174 / 1.0 |
| proto_indoiranian_wiktionary | strict | wide | 93/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.444 / 1.0 | 0 / 1.0 | 0.444 / 1.0 |
| proto_indoiranian_wiktionary | medium | narrow | 93/114 | 0 | 0.352 / 1.0 | 0.092 / 1.0 | 1.2 / 1.0 | 0.453 / 1.0 | 1.2 / 1.0 |
| proto_indoiranian_wiktionary | medium | wide | 93/114 | 2 | 2.03 / 0.6177 | 1.54 / 0.3038 | 2.75 / 0.4531 | 1.82 / 0.5877 | 2.75 / 0.4531 |
| proto_indoiranian_wiktionary | loose | narrow | 93/114 | 41 | 37.9 / 0.1929 | 19.7 / 0.0165 | 28.8 / 0.0699 | 36.4 / 0.085 | 28.8 / 0.0699 |
| proto_indoiranian_wiktionary | loose | wide | 93/114 | 52 | 49.3 / 0.2339 | 28.4 / 0.015 | 48.4 / 0.3752 | 45.9 / 0.021 | 48.4 / 0.3752 |
| sumerian_halloran | strict | narrow | 107/114 | 35 | 35.6 / 0.6107 | 11.1 / 0.0005 | 43.3 / 0.9162 | 31.4 / 0.1699 | 46.3 / 0.9721 |
| sumerian_halloran | strict | wide | 107/114 | 65 | 57.7 / 0.012 | 25 / 0.0005 | 62.7 / 0.4311 | 56.4 / 0.0005 | 65.8 / 0.5569 |
| sumerian_halloran | medium | narrow | 107/114 | 83 | 78 / 0.0615 | 48.5 / 0.0005 | 78.4 / 0.2156 | 72.8 / 0.001 | 82.6 / 0.5309 |
| sumerian_halloran | medium | wide | 107/114 | 93 | 90.6 / 0.1329 | 67.3 / 0.013 | 91.4 / 0.4052 | 89.4 / 0.0295 | 95.1 / 0.7345 |
| sumerian_halloran | loose | narrow | 107/114 | 96 | 97.5 / 0.8621 | 91.8 / 0.3993 | 101 / 0.9621 | 97.3 / 0.8516 | 103 / 0.992 |
| sumerian_halloran | loose | wide | 107/114 | 99 | 100 / 0.8656 | 95.5 / 0.4183 | 104 / 0.9701 | 100 / 0.8551 | 105 / 0.996 |
| sumerian_wiktionary | strict | narrow | 102/114 | 4 | 4.71 / 0.7426 | 2.44 / 0.2479 | 10.5 / 0.8962 | 2.93 / 0.3043 | 10.1 / 0.8842 |
| sumerian_wiktionary | strict | wide | 102/114 | 7 | 9.63 / 0.9 | 6.11 / 0.3688 | 20.1 / 0.984 | 9.46 / 0.9175 | 20.2 / 0.986 |
| sumerian_wiktionary | medium | narrow | 102/114 | 28 | 33.5 / 0.9465 | 19.1 / 0.1219 | 38.2 / 0.9541 | 29.1 / 0.6727 | 37.9 / 0.9481 |
| sumerian_wiktionary | medium | wide | 102/114 | 52 | 57.1 / 0.9295 | 33.3 / 0.037 | 57.5 / 0.7924 | 54.6 / 0.8381 | 57.4 / 0.7824 |
| sumerian_wiktionary | loose | narrow | 102/114 | 91 | 87.4 / 0.1019 | 58.8 / 0.0015 | 83 / 0.0978 | 84.3 / 0.0095 | 83.4 / 0.1018 |
| sumerian_wiktionary | loose | wide | 102/114 | 96 | 94.8 / 0.3618 | 70.6 / 0.0135 | 95 / 0.515 | 94.1 / 0.2109 | 94.8 / 0.4451 |
| akkadian_wiktionary | strict | narrow | 97/114 | 0 | 0.257 / 1.0 | 0 / 1.0 | 2.49 / 1.0 | 0.336 / 1.0 | 2.49 / 1.0 |
| akkadian_wiktionary | strict | wide | 97/114 | 3 | 1.02 / 0.06 | 0 / 0.0005 | 4.33 / 0.5689 | 0.789 / 0.027 | 4.33 / 0.5689 |
| akkadian_wiktionary | medium | narrow | 97/114 | 12 | 12.2 / 0.6047 | 4.72 / 0.077 | 14.6 / 0.7026 | 11.7 / 0.5412 | 14.6 / 0.7026 |
| akkadian_wiktionary | medium | wide | 97/114 | 26 | 22.9 / 0.093 | 6.79 / 0.002 | 22.8 / 0.3413 | 20.9 / 0.012 | 22.8 / 0.3413 |
| akkadian_wiktionary | loose | narrow | 97/114 | 65 | 65.9 / 0.6812 | 48.3 / 0.094 | 61.9 / 0.3932 | 62.9 / 0.2694 | 61.9 / 0.3932 |
| akkadian_wiktionary | loose | wide | 97/114 | 78 | 79.2 / 0.7871 | 61.4 / 0.1099 | 74.3 / 0.3812 | 77.8 / 0.5512 | 74.3 / 0.3812 |
| elamite_hinzkoch | strict | narrow | 72/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| elamite_hinzkoch | strict | wide | 72/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0.006 / 1.0 | 0 / 1.0 | 0.006 / 1.0 |
| elamite_hinzkoch | medium | narrow | 72/114 | 2 | 1.28 / 0.3658 | 0.585 / 0.1374 | 0.932 / 0.1936 | 1.29 / 0.3893 | 0.932 / 0.1936 |
| elamite_hinzkoch | medium | wide | 72/114 | 2 | 1.63 / 0.5037 | 1.48 / 0.3448 | 5.28 / 0.8144 | 1.75 / 0.5687 | 5.28 / 0.8144 |
| elamite_hinzkoch | loose | narrow | 72/114 | 13 | 15.7 / 0.8841 | 5.11 / 0.087 | 18.6 / 0.8263 | 17.6 / 0.975 | 18.6 / 0.8263 |
| elamite_hinzkoch | loose | wide | 72/114 | 50 | 40.5 / 0.003 | 11.6 / 0.001 | 44.2 / 0.2016 | 37.4 / 0.0005 | 44.2 / 0.2016 |
| burushaski_lorimer | strict | narrow | 83/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| burushaski_lorimer | strict | wide | 83/114 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| burushaski_lorimer | medium | narrow | 83/114 | 0 | 0.05 / 1.0 | 1.31 / 1.0 | 3.2 / 1.0 | 0.054 / 1.0 | 3.2 / 1.0 |
| burushaski_lorimer | medium | wide | 83/114 | 3 | 2.18 / 0.3693 | 3.47 / 0.5222 | 6.14 / 0.7066 | 1.76 / 0.2514 | 6.14 / 0.7066 |
| burushaski_lorimer | loose | narrow | 83/114 | 31 | 31.7 / 0.6817 | 24.8 / 0.2444 | 34.7 / 0.7305 | 30.5 / 0.4973 | 34.7 / 0.7305 |
| burushaski_lorimer | loose | wide | 83/114 | 43 | 45.9 / 0.9225 | 41.2 / 0.4403 | 47.4 / 0.6806 | 47.4 / 0.994 | 47.4 / 0.6806 |

#### B_3of3+2of3: share, every family and every dictionary, full grid

| dictionary / family | distance | keywords | units covered | share | C1 classes dealt mean / P | C2 outside nouns mean / P | C3 sounds dealt by entry mean / P | C4 wrong class same picture mean / P | C3row mean / P |
|---|---|---|---|---|---|---|---|---|---|
| FAMILY Dravidian | strict | narrow | 171/172 | 1.27 | 1.18 / 0.2399 | 1.28 / 0.4523 | 1.65 / 0.9601 | 1.06 / 0.0425 | 1.67 / 0.9581 |
| FAMILY Dravidian | strict | wide | 171/172 | 3.3 | 3.18 / 0.2884 | 3.03 / 0.3028 | 3.55 / 0.7365 | 2.81 / 0.007 | 3.63 / 0.8104 |
| FAMILY Dravidian | medium | narrow | 171/172 | 1.55 | 1.48 / 0.066 | 1.59 / 0.6082 | 1.7 / 0.9581 | 1.25 / 0.0005 | 1.7 / 0.9501 |
| FAMILY Dravidian | medium | wide | 171/172 | 3.42 | 3.33 / 0.0975 | 3.51 / 0.6587 | 3.69 / 0.978 | 2.89 / 0.0005 | 3.67 / 0.9721 |
| FAMILY Dravidian | loose | narrow | 171/172 | 1.65 | 1.64 / 0.2159 | 1.7 / 0.8901 | 1.76 / 0.998 | 1.39 / 0.0005 | 1.76 / 1.0 |
| FAMILY Dravidian | loose | wide | 171/172 | 3.55 | 3.56 / 0.5937 | 3.67 / 0.976 | 3.74 / 1.0 | 3.11 / 0.0005 | 3.75 / 1.0 |
| FAMILY Munda | strict | narrow | 171/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.564 / 1.0 | 0 / 1.0 | 0.613 / 1.0 |
| FAMILY Munda | strict | wide | 171/172 | 0 | 0 / 1.0 | 0 / 1.0 | 1.22 / 1.0 | 0 / 1.0 | 1.32 / 1.0 |
| FAMILY Munda | medium | narrow | 171/172 | 1.75 | 1.5 / 0.034 | 1.67 / 0.2994 | 1.62 / 0.2814 | 1.19 / 0.0005 | 1.62 / 0.2914 |
| FAMILY Munda | medium | wide | 171/172 | 3.42 | 3.12 / 0.0655 | 3.49 / 0.4828 | 3.44 / 0.489 | 2.98 / 0.016 | 3.44 / 0.505 |
| FAMILY Munda | loose | narrow | 171/172 | 1.76 | 1.76 / 0.4953 | 1.6 / 0.0055 | 1.64 / 0.0339 | 1.49 / 0.002 | 1.64 / 0.0339 |
| FAMILY Munda | loose | wide | 171/172 | 3.57 | 3.6 / 0.6897 | 3.44 / 0.1589 | 3.47 / 0.1617 | 3.3 / 0.0125 | 3.46 / 0.1437 |
| FAMILY Indo-Aryan | strict | narrow | 171/172 | 1.9 | 1.78 / 0.3013 | 1.48 / 0.1864 | 1.98 / 0.503 | 1.62 / 0.1709 | 1.98 / 0.503 |
| FAMILY Indo-Aryan | strict | wide | 171/172 | 3.32 | 3.7 / 0.8211 | 3.86 / 0.7326 | 4.05 / 0.8543 | 3.69 / 0.8081 | 4.05 / 0.8543 |
| FAMILY Indo-Aryan | medium | narrow | 171/172 | 1.61 | 1.56 / 0.2919 | 1.73 / 0.7386 | 2.03 / 1.0 | 1.51 / 0.1529 | 2.03 / 1.0 |
| FAMILY Indo-Aryan | medium | wide | 171/172 | 3.39 | 3.51 / 0.7706 | 3.79 / 0.9535 | 4.16 / 1.0 | 3.57 / 0.8421 | 4.16 / 1.0 |
| FAMILY Indo-Aryan | loose | narrow | 171/172 | 1.93 | 1.92 / 0.2779 | 1.82 / 0.041 | 2.05 / 1.0 | 1.71 / 0.003 | 2.05 / 1.0 |
| FAMILY Indo-Aryan | loose | wide | 171/172 | 4.13 | 4.17 / 0.7906 | 4.04 / 0.1424 | 4.19 / 0.9182 | 3.95 / 0.1014 | 4.19 / 0.9182 |
| FAMILY Sumerian | strict | narrow | 161/172 | 1.76 | 1.64 / 0.3148 | 1.31 / 0.2374 | 2.43 / 0.8503 | 1.35 / 0.0655 | 2.71 / 0.9142 |
| FAMILY Sumerian | strict | wide | 161/172 | 4.13 | 3.9 / 0.2769 | 4.13 / 0.4363 | 5.57 / 0.9122 | 3.86 / 0.2394 | 5.87 / 0.9741 |
| FAMILY Sumerian | medium | narrow | 161/172 | 3.17 | 3.21 / 0.5167 | 2.79 / 0.2439 | 2.64 / 0.0878 | 2.57 / 0.013 | 2.81 / 0.1497 |
| FAMILY Sumerian | medium | wide | 161/172 | 6.77 | 6.75 / 0.4653 | 6.24 / 0.2814 | 5.98 / 0.0878 | 5.95 / 0.0125 | 6.14 / 0.1018 |
| FAMILY Sumerian | loose | narrow | 161/172 | 2.72 | 2.76 / 0.5877 | 2.48 / 0.1519 | 2.78 / 0.6367 | 2.43 / 0.026 | 2.85 / 0.8323 |
| FAMILY Sumerian | loose | wide | 161/172 | 6.22 | 6.25 / 0.5347 | 6.11 / 0.4293 | 6.19 / 0.4491 | 5.72 / 0.009 | 6.24 / 0.521 |
| FAMILY Akkadian | strict | narrow | 136/172 | 0 | 0.189 / 1.0 | 0 / 1.0 | 0.934 / 1.0 | 0.27 / 1.0 | 0.934 / 1.0 |
| FAMILY Akkadian | strict | wide | 136/172 | 2.25 | 0.936 / 0.0215 | 0 / 0.0005 | 1.72 / 0.2914 | 0.678 / 0.006 | 1.72 / 0.2914 |
| FAMILY Akkadian | medium | narrow | 136/172 | 0.823 | 0.959 / 0.6647 | 1.49 / 0.6472 | 1.76 / 0.8104 | 0.985 / 0.7021 | 1.76 / 0.8104 |
| FAMILY Akkadian | medium | wide | 136/172 | 2.52 | 2.28 / 0.2854 | 2.5 / 0.3513 | 3.43 / 0.6727 | 2.14 / 0.2044 | 3.43 / 0.6727 |
| FAMILY Akkadian | loose | narrow | 136/172 | 2.07 | 2.43 / 0.947 | 2.13 / 0.5497 | 2.32 / 0.6966 | 2.28 / 0.8581 | 2.32 / 0.6966 |
| FAMILY Akkadian | loose | wide | 136/172 | 4.95 | 5.4 / 0.9205 | 4.68 / 0.3873 | 4.66 / 0.2954 | 4.89 / 0.4163 | 4.66 / 0.2954 |
| FAMILY Elamite | strict | narrow | 105/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| FAMILY Elamite | strict | wide | 105/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.006 / 1.0 | 0 / 1.0 | 0.006 / 1.0 |
| FAMILY Elamite | medium | narrow | 105/172 | 0.381 | 0.271 / 0.2864 | 0.089 / 0.06 | 0.164 / 0.1018 | 0.258 / 0.2434 | 0.164 / 0.1018 |
| FAMILY Elamite | medium | wide | 105/172 | 0.381 | 0.331 / 0.3738 | 0.362 / 0.3248 | 0.89 / 0.6567 | 0.339 / 0.3948 | 0.89 / 0.6567 |
| FAMILY Elamite | loose | narrow | 105/172 | 0.224 | 0.206 / 0.3533 | 0.1 / 0.098 | 0.182 / 0.2176 | 0.207 / 0.3423 | 0.182 / 0.2176 |
| FAMILY Elamite | loose | wide | 105/172 | 1.56 | 1.39 / 0.1219 | 0.399 / 0.001 | 1.11 / 0.0599 | 1.34 / 0.074 | 1.11 / 0.0599 |
| FAMILY Burushaski | strict | narrow | 121/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| FAMILY Burushaski | strict | wide | 121/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| FAMILY Burushaski | medium | narrow | 121/172 | 0 | 0.039 / 1.0 | 0.911 / 1.0 | 0.598 / 1.0 | 0.064 / 1.0 | 0.598 / 1.0 |
| FAMILY Burushaski | medium | wide | 121/172 | 1.65 | 0.986 / 0.1819 | 1.69 / 0.4283 | 1.19 / 0.2515 | 0.695 / 0.056 | 1.19 / 0.2515 |
| FAMILY Burushaski | loose | narrow | 121/172 | 0.465 | 0.505 / 0.6147 | 1.05 / 0.9305 | 0.865 / 0.9461 | 0.495 / 0.5662 | 0.865 / 0.9461 |
| FAMILY Burushaski | loose | wide | 121/172 | 1.42 | 1.51 / 0.6632 | 2.12 / 0.8306 | 1.82 / 0.7904 | 1.46 / 0.5742 | 1.82 / 0.7904 |
| dedr_tamil | strict | narrow | 170/172 | 0.898 | 1.05 / 0.8201 | 1.15 / 0.6197 | 1.53 / 0.986 | 0.906 / 0.4923 | 1.62 / 0.996 |
| dedr_tamil | strict | wide | 170/172 | 2.64 | 2.73 / 0.6122 | 2.32 / 0.3063 | 3.31 / 0.8842 | 2.38 / 0.1339 | 3.45 / 0.9401 |
| dedr_tamil | medium | narrow | 170/172 | 1.33 | 1.21 / 0.0165 | 1.47 / 0.6387 | 1.55 / 0.9481 | 0.981 / 0.0005 | 1.64 / 0.99 |
| dedr_tamil | medium | wide | 170/172 | 3.08 | 2.87 / 0.008 | 3.17 / 0.5352 | 3.4 / 0.9501 | 2.46 / 0.0005 | 3.51 / 0.978 |
| dedr_tamil | loose | narrow | 170/172 | 1.44 | 1.42 / 0.2309 | 1.44 / 0.5232 | 1.58 / 0.998 | 1.19 / 0.0005 | 1.65 / 1.0 |
| dedr_tamil | loose | wide | 170/172 | 3.09 | 3.1 / 0.6047 | 3.15 / 0.7231 | 3.41 / 1.0 | 2.74 / 0.0005 | 3.53 / 1.0 |
| dedr_malayalam | strict | narrow | 163/172 | 1.37 | 1.49 / 0.5022 | 0.983 / 0.2234 | 1.05 / 0.2315 | 1.44 / 0.4428 | 1.06 / 0.2595 |
| dedr_malayalam | strict | wide | 163/172 | 3.94 | 3.84 / 0.3978 | 2.51 / 0.0855 | 2.67 / 0.0798 | 3.44 / 0.2094 | 2.63 / 0.0858 |
| dedr_malayalam | medium | narrow | 163/172 | 1.46 | 1.56 / 0.8011 | 1.38 / 0.3833 | 1.12 / 0.0679 | 1.34 / 0.1254 | 1.12 / 0.0479 |
| dedr_malayalam | medium | wide | 163/172 | 3.55 | 3.64 / 0.6912 | 3.56 / 0.4443 | 2.84 / 0.0639 | 3.21 / 0.0385 | 2.76 / 0.018 |
| dedr_malayalam | loose | narrow | 163/172 | 1.29 | 1.28 / 0.4428 | 1.28 / 0.4638 | 1.13 / 0.012 | 1.16 / 0.009 | 1.12 / 0.022 |
| dedr_malayalam | loose | wide | 163/172 | 3.22 | 3.24 / 0.6377 | 3.25 / 0.5912 | 2.83 / 0.01 | 2.93 / 0.0025 | 2.8 / 0.006 |
| dedr_kannada | strict | narrow | 160/172 | 0.996 | 1.24 / 0.7541 | 1.32 / 0.5157 | 0.96 / 0.3553 | 1.34 / 0.976 | 0.971 / 0.4052 |
| dedr_kannada | strict | wide | 160/172 | 2.64 | 3.1 / 0.8466 | 3.49 / 0.6362 | 2.67 / 0.4471 | 2.85 / 0.7261 | 2.66 / 0.4491 |
| dedr_kannada | medium | narrow | 160/172 | 1.12 | 1.07 / 0.2584 | 1.13 / 0.4543 | 1.04 / 0.2974 | 0.921 / 0.0115 | 1.02 / 0.2295 |
| dedr_kannada | medium | wide | 160/172 | 2.86 | 2.88 / 0.5212 | 3.05 / 0.6287 | 2.79 / 0.3972 | 2.51 / 0.0135 | 2.81 / 0.4012 |
| dedr_kannada | loose | narrow | 160/172 | 1.11 | 1.12 / 0.6737 | 1.08 / 0.3968 | 1.06 / 0.1756 | 0.984 / 0.002 | 1.04 / 0.0539 |
| dedr_kannada | loose | wide | 160/172 | 2.86 | 2.92 / 0.8921 | 2.96 / 0.6992 | 2.82 / 0.3253 | 2.64 / 0.005 | 2.85 / 0.4132 |
| dedr_telugu | strict | narrow | 162/172 | 1.38 | 0.789 / 0.0195 | 1.15 / 0.2944 | 1.14 / 0.3074 | 0.495 / 0.0005 | 1.2 / 0.3453 |
| dedr_telugu | strict | wide | 162/172 | 4.92 | 3.5 / 0.0345 | 2.73 / 0.1059 | 2.43 / 0.0339 | 2.36 / 0.0005 | 2.63 / 0.0379 |
| dedr_telugu | medium | narrow | 162/172 | 1.3 | 1.29 / 0.4688 | 0.996 / 0.1854 | 1.27 / 0.4172 | 1.1 / 0.0675 | 1.27 / 0.4491 |
| dedr_telugu | medium | wide | 162/172 | 3.24 | 3.03 / 0.1869 | 2.8 / 0.2319 | 2.88 / 0.2116 | 2.6 / 0.001 | 2.74 / 0.1078 |
| dedr_telugu | loose | narrow | 162/172 | 1.28 | 1.31 / 0.7711 | 1.23 / 0.3473 | 1.27 / 0.4471 | 1.1 / 0.0005 | 1.29 / 0.523 |
| dedr_telugu | loose | wide | 162/172 | 3.01 | 2.99 / 0.3618 | 2.87 / 0.2844 | 2.79 / 0.0559 | 2.6 / 0.0005 | 2.8 / 0.0559 |
| tamil_wiktionary | strict | narrow | 169/172 | 1.99 | 1.76 / 0.2504 | 1.55 / 0.2224 | 2.02 / 0.475 | 1.61 / 0.053 | 2 / 0.4411 |
| tamil_wiktionary | strict | wide | 169/172 | 3.38 | 3.17 / 0.2644 | 3.44 / 0.4763 | 4.23 / 0.7705 | 3.05 / 0.1539 | 4.2 / 0.7665 |
| tamil_wiktionary | medium | narrow | 169/172 | 2.06 | 2.09 / 0.5427 | 2.23 / 0.6692 | 2.11 / 0.5289 | 1.82 / 0.059 | 2.11 / 0.515 |
| tamil_wiktionary | medium | wide | 169/172 | 4.39 | 4.29 / 0.3208 | 4.2 / 0.3013 | 4.42 / 0.525 | 3.58 / 0.0005 | 4.41 / 0.487 |
| tamil_wiktionary | loose | narrow | 169/172 | 2.08 | 2.08 / 0.5167 | 2.19 / 0.9565 | 2.14 / 0.7525 | 1.73 / 0.0005 | 2.15 / 0.7705 |
| tamil_wiktionary | loose | wide | 169/172 | 4.13 | 4.14 / 0.5452 | 4.3 / 0.9395 | 4.48 / 0.998 | 3.5 / 0.0005 | 4.48 / 0.998 |
| telugu_wiktionary | strict | narrow | 171/172 | 1.23 | 1.34 / 0.4848 | 1.79 / 0.5832 | 2.67 / 0.9042 | 1.3 / 0.4718 | 2.64 / 0.9182 |
| telugu_wiktionary | strict | wide | 171/172 | 2.54 | 2.62 / 0.4838 | 2.93 / 0.5052 | 4.51 / 0.9022 | 2.2 / 0.3068 | 4.53 / 0.9202 |
| telugu_wiktionary | medium | narrow | 171/172 | 2.47 | 2.22 / 0.1709 | 2.67 / 0.5922 | 3.25 / 0.9581 | 1.77 / 0.0005 | 3.24 / 0.9561 |
| telugu_wiktionary | medium | wide | 171/172 | 4.52 | 4.56 / 0.5087 | 4.76 / 0.5892 | 5.46 / 0.9022 | 3.98 / 0.1304 | 5.46 / 0.9142 |
| telugu_wiktionary | loose | narrow | 171/172 | 2.82 | 2.79 / 0.3763 | 2.77 / 0.3463 | 3.4 / 1.0 | 2.28 / 0.001 | 3.41 / 1.0 |
| telugu_wiktionary | loose | wide | 171/172 | 4.99 | 5 / 0.5412 | 5 / 0.5067 | 5.74 / 1.0 | 4.21 / 0.0005 | 5.74 / 1.0 |
| kannada_wiktionary | strict | narrow | 162/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.516 / 1.0 | 0 / 1.0 | 0.516 / 1.0 |
| kannada_wiktionary | strict | wide | 162/172 | 0 | 0.124 / 1.0 | 0.86 / 1.0 | 1.26 / 1.0 | 0.152 / 1.0 | 1.26 / 1.0 |
| kannada_wiktionary | medium | narrow | 162/172 | 1.18 | 1.24 / 0.6082 | 2.07 / 0.7901 | 1.06 / 0.3533 | 1.22 / 0.6007 | 1.06 / 0.3533 |
| kannada_wiktionary | medium | wide | 162/172 | 3.85 | 4.26 / 0.7881 | 4.14 / 0.5497 | 2.59 / 0.1277 | 3.7 / 0.3053 | 2.59 / 0.1277 |
| kannada_wiktionary | loose | narrow | 162/172 | 1.51 | 1.56 / 0.6242 | 1.35 / 0.1679 | 1.31 / 0.1457 | 1.34 / 0.036 | 1.31 / 0.1457 |
| kannada_wiktionary | loose | wide | 162/172 | 3.91 | 3.86 / 0.3948 | 3.41 / 0.048 | 3.06 / 0.022 | 3.28 / 0.0005 | 3.06 / 0.022 |
| santali_campbell | strict | narrow | 167/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.028 / 1.0 | 0 / 1.0 | 0.028 / 1.0 |
| santali_campbell | strict | wide | 167/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.076 / 1.0 | 0 / 1.0 | 0.076 / 1.0 |
| santali_campbell | medium | narrow | 167/172 | 1.92 | 1.55 / 0.0195 | 1.47 / 0.1454 | 1.42 / 0.0938 | 1.24 / 0.0005 | 1.42 / 0.0938 |
| santali_campbell | medium | wide | 167/172 | 3.32 | 2.92 / 0.063 | 3.06 / 0.3258 | 2.96 / 0.2315 | 2.64 / 0.0025 | 2.96 / 0.2315 |
| santali_campbell | loose | narrow | 167/172 | 1.63 | 1.63 / 0.5222 | 1.59 / 0.2839 | 1.51 / 0.0659 | 1.41 / 0.0015 | 1.51 / 0.0659 |
| santali_campbell | loose | wide | 167/172 | 3.34 | 3.36 / 0.6402 | 3.3 / 0.3933 | 3.12 / 0.0599 | 3.05 / 0.001 | 3.12 / 0.0599 |
| santali_bodding5 | strict | narrow | 135/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| santali_bodding5 | strict | wide | 135/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| santali_bodding5 | medium | narrow | 135/172 | 0.125 | 0.127 / 0.4193 | 0.279 / 0.6487 | 0.609 / 0.7605 | 0.124 / 0.4048 | 0.609 / 0.7605 |
| santali_bodding5 | medium | wide | 135/172 | 0.323 | 0.484 / 0.6257 | 1.07 / 0.7941 | 1.29 / 0.8383 | 0.753 / 1.0 | 1.29 / 0.8383 |
| santali_bodding5 | loose | narrow | 135/172 | 0.691 | 0.68 / 0.3233 | 0.55 / 0.2334 | 0.893 / 0.7745 | 0.609 / 0.2299 | 0.893 / 0.7745 |
| santali_bodding5 | loose | wide | 135/172 | 1.53 | 1.61 / 0.5917 | 1.24 / 0.2044 | 1.88 / 0.7764 | 1.45 / 0.2699 | 1.88 / 0.7764 |
| santali_wiktionary | strict | narrow | 141/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.178 / 1.0 | 0 / 1.0 | 0.32 / 1.0 |
| santali_wiktionary | strict | wide | 141/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.397 / 1.0 | 0 / 1.0 | 0.611 / 1.0 |
| santali_wiktionary | medium | narrow | 141/172 | 1.28 | 0.773 / 0.1724 | 0.786 / 0.1884 | 0.869 / 0.2335 | 0.51 / 0.047 | 0.873 / 0.2355 |
| santali_wiktionary | medium | wide | 141/172 | 1.87 | 1.49 / 0.2604 | 1.41 / 0.2639 | 1.68 / 0.3353 | 0.895 / 0.026 | 1.75 / 0.3633 |
| santali_wiktionary | loose | narrow | 141/172 | 0.966 | 1.11 / 0.8301 | 1.05 / 0.6167 | 1.22 / 0.7904 | 1.03 / 0.6867 | 1.23 / 0.7764 |
| santali_wiktionary | loose | wide | 141/172 | 2.33 | 2.53 / 0.7586 | 2.4 / 0.5292 | 2.45 / 0.5709 | 2.21 / 0.2739 | 2.44 / 0.5569 |
| mundari_bhadra | strict | narrow | 171/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.469 / 1.0 | 0 / 1.0 | 0.469 / 1.0 |
| mundari_bhadra | strict | wide | 171/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.977 / 1.0 | 0 / 1.0 | 0.977 / 1.0 |
| mundari_bhadra | medium | narrow | 171/172 | 1.61 | 1.48 / 0.2359 | 1.74 / 0.4548 | 1.78 / 0.5888 | 1.16 / 0.0255 | 1.78 / 0.5888 |
| mundari_bhadra | medium | wide | 171/172 | 3.73 | 3.65 / 0.3738 | 3.39 / 0.3133 | 3.86 / 0.523 | 3.77 / 0.4663 | 3.86 / 0.523 |
| mundari_bhadra | loose | narrow | 171/172 | 1.91 | 1.94 / 0.6457 | 1.55 / 0.01 | 1.87 / 0.3573 | 1.65 / 0.012 | 1.87 / 0.3573 |
| mundari_bhadra | loose | wide | 171/172 | 3.95 | 3.99 / 0.6502 | 3.4 / 0.0245 | 4.07 / 0.7006 | 3.82 / 0.2269 | 4.07 / 0.7006 |
| sanskrit_mw | strict | narrow | 171/172 | 1.92 | 1.8 / 0.3048 | 1.47 / 0.1769 | 1.99 / 0.491 | 1.65 / 0.1764 | 1.99 / 0.491 |
| sanskrit_mw | strict | wide | 171/172 | 3.38 | 3.74 / 0.8046 | 3.86 / 0.7056 | 4.07 / 0.8403 | 3.65 / 0.7216 | 4.07 / 0.8403 |
| sanskrit_mw | medium | narrow | 171/172 | 1.62 | 1.57 / 0.2814 | 1.74 / 0.7576 | 2.05 / 0.998 | 1.52 / 0.1669 | 2.05 / 0.998 |
| sanskrit_mw | medium | wide | 171/172 | 3.41 | 3.49 / 0.7096 | 3.83 / 0.953 | 4.2 / 1.0 | 3.53 / 0.7641 | 4.2 / 1.0 |
| sanskrit_mw | loose | narrow | 171/172 | 1.95 | 1.93 / 0.2959 | 1.83 / 0.0435 | 2.07 / 1.0 | 1.73 / 0.0035 | 2.07 / 1.0 |
| sanskrit_mw | loose | wide | 171/172 | 4.16 | 4.2 / 0.8166 | 4.08 / 0.1604 | 4.23 / 0.9301 | 3.99 / 0.1139 | 4.23 / 0.9301 |
| oia_turner | strict | narrow | 166/172 | 0.083 | 0.056 / 0.3528 | 0.945 / 0.7471 | 0.839 / 0.7585 | 0.048 / 0.2564 | 0.839 / 0.7585 |
| oia_turner | strict | wide | 166/172 | 0.083 | 1.25 / 0.9005 | 2.25 / 0.9105 | 1.97 / 0.9641 | 3.03 / 0.9885 | 1.97 / 0.9641 |
| oia_turner | medium | narrow | 166/172 | 0.877 | 0.95 / 0.5972 | 1.16 / 0.6112 | 1.15 / 0.6567 | 0.787 / 0.2939 | 1.15 / 0.6567 |
| oia_turner | medium | wide | 166/172 | 2.44 | 2.88 / 0.7836 | 2.84 / 0.6242 | 2.67 / 0.5289 | 3.01 / 0.8371 | 2.67 / 0.5289 |
| oia_turner | loose | narrow | 166/172 | 1.15 | 1.19 / 0.6087 | 1.13 / 0.3808 | 1.2 / 0.6587 | 1.11 / 0.3533 | 1.2 / 0.6587 |
| oia_turner | loose | wide | 166/172 | 2.72 | 2.81 / 0.7701 | 2.62 / 0.3138 | 2.78 / 0.6108 | 2.74 / 0.5557 | 2.78 / 0.6108 |
| proto_indoiranian_wiktionary | strict | narrow | 125/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.185 / 1.0 | 0 / 1.0 | 0.185 / 1.0 |
| proto_indoiranian_wiktionary | strict | wide | 125/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.469 / 1.0 | 0 / 1.0 | 0.469 / 1.0 |
| proto_indoiranian_wiktionary | medium | narrow | 125/172 | 0.333 | 0.181 / 0.3673 | 0.132 / 0.0985 | 0.558 / 0.3513 | 0.168 / 0.3313 | 0.558 / 0.3513 |
| proto_indoiranian_wiktionary | medium | wide | 125/172 | 1.83 | 1.15 / 0.1789 | 1.29 / 0.2574 | 1.43 / 0.2914 | 0.815 / 0.0245 | 1.43 / 0.2914 |
| proto_indoiranian_wiktionary | loose | narrow | 125/172 | 2.17 | 2.28 / 0.6042 | 1.22 / 0.047 | 1.09 / 0.022 | 2.12 / 0.4488 | 1.09 / 0.022 |
| proto_indoiranian_wiktionary | loose | wide | 125/172 | 4.36 | 4.67 / 0.6647 | 2.73 / 0.0315 | 2.81 / 0.0519 | 4.3 / 0.4408 | 2.81 / 0.0519 |
| sumerian_halloran | strict | narrow | 159/172 | 1.88 | 1.77 / 0.3338 | 1.01 / 0.0965 | 2.35 / 0.7206 | 1.52 / 0.1044 | 2.68 / 0.8663 |
| sumerian_halloran | strict | wide | 159/172 | 4.35 | 4.2 / 0.3548 | 3.27 / 0.1834 | 5.4 / 0.7824 | 4.15 / 0.3228 | 5.74 / 0.8862 |
| sumerian_halloran | medium | narrow | 159/172 | 2.95 | 2.98 / 0.5082 | 2.64 / 0.2709 | 2.65 / 0.1996 | 2.43 / 0.0185 | 2.88 / 0.3693 |
| sumerian_halloran | medium | wide | 159/172 | 6.11 | 6.07 / 0.4428 | 5.99 / 0.4228 | 6 / 0.3792 | 5.43 / 0.0175 | 6.2 / 0.501 |
| sumerian_halloran | loose | narrow | 159/172 | 2.93 | 2.96 / 0.5532 | 2.45 / 0.0495 | 2.87 / 0.3194 | 2.53 / 0.007 | 2.92 / 0.4691 |
| sumerian_halloran | loose | wide | 159/172 | 6.57 | 6.45 / 0.2934 | 6.06 / 0.1564 | 6.34 / 0.2156 | 5.75 / 0.001 | 6.36 / 0.1856 |
| sumerian_wiktionary | strict | narrow | 152/172 | 0.614 | 0.545 / 0.3453 | 0.949 / 0.5107 | 1.65 / 0.8303 | 0.292 / 0.0245 | 1.61 / 0.8164 |
| sumerian_wiktionary | strict | wide | 152/172 | 1.92 | 2.47 / 0.6957 | 3.02 / 0.6562 | 3.8 / 0.8982 | 3.76 / 0.9665 | 3.84 / 0.8723 |
| sumerian_wiktionary | medium | narrow | 152/172 | 2.44 | 2.24 / 0.2664 | 2.44 / 0.4378 | 2.03 / 0.2255 | 1.58 / 0.001 | 1.97 / 0.2036 |
| sumerian_wiktionary | medium | wide | 152/172 | 5 | 4.63 / 0.2134 | 5.23 / 0.5062 | 4.64 / 0.3214 | 3.86 / 0.0035 | 4.63 / 0.2974 |
| sumerian_wiktionary | loose | narrow | 152/172 | 2.06 | 2.01 / 0.3648 | 1.91 / 0.3398 | 2.04 / 0.4651 | 1.8 / 0.06 | 2.08 / 0.501 |
| sumerian_wiktionary | loose | wide | 152/172 | 4.74 | 4.62 / 0.3008 | 4.26 / 0.2499 | 4.79 / 0.5609 | 4.28 / 0.029 | 4.85 / 0.6347 |
| akkadian_wiktionary | strict | narrow | 136/172 | 0 | 0.189 / 1.0 | 0 / 1.0 | 0.934 / 1.0 | 0.27 / 1.0 | 0.934 / 1.0 |
| akkadian_wiktionary | strict | wide | 136/172 | 2.25 | 0.936 / 0.0215 | 0 / 0.0005 | 1.72 / 0.2914 | 0.678 / 0.006 | 1.72 / 0.2914 |
| akkadian_wiktionary | medium | narrow | 136/172 | 0.823 | 0.959 / 0.6647 | 1.49 / 0.6472 | 1.76 / 0.8104 | 0.985 / 0.7021 | 1.76 / 0.8104 |
| akkadian_wiktionary | medium | wide | 136/172 | 2.52 | 2.28 / 0.2854 | 2.5 / 0.3513 | 3.43 / 0.6727 | 2.14 / 0.2044 | 3.43 / 0.6727 |
| akkadian_wiktionary | loose | narrow | 136/172 | 2.07 | 2.43 / 0.947 | 2.13 / 0.5497 | 2.32 / 0.6966 | 2.28 / 0.8581 | 2.32 / 0.6966 |
| akkadian_wiktionary | loose | wide | 136/172 | 4.95 | 5.4 / 0.9205 | 4.68 / 0.3873 | 4.66 / 0.2954 | 4.89 / 0.4163 | 4.66 / 0.2954 |
| elamite_hinzkoch | strict | narrow | 105/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| elamite_hinzkoch | strict | wide | 105/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.006 / 1.0 | 0 / 1.0 | 0.006 / 1.0 |
| elamite_hinzkoch | medium | narrow | 105/172 | 0.381 | 0.271 / 0.2864 | 0.089 / 0.06 | 0.164 / 0.1018 | 0.258 / 0.2434 | 0.164 / 0.1018 |
| elamite_hinzkoch | medium | wide | 105/172 | 0.381 | 0.331 / 0.3738 | 0.362 / 0.3248 | 0.89 / 0.6567 | 0.339 / 0.3948 | 0.89 / 0.6567 |
| elamite_hinzkoch | loose | narrow | 105/172 | 0.224 | 0.206 / 0.3533 | 0.1 / 0.098 | 0.182 / 0.2176 | 0.207 / 0.3423 | 0.182 / 0.2176 |
| elamite_hinzkoch | loose | wide | 105/172 | 1.56 | 1.39 / 0.1219 | 0.399 / 0.001 | 1.11 / 0.0599 | 1.34 / 0.074 | 1.11 / 0.0599 |
| burushaski_lorimer | strict | narrow | 121/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| burushaski_lorimer | strict | wide | 121/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| burushaski_lorimer | medium | narrow | 121/172 | 0 | 0.039 / 1.0 | 0.911 / 1.0 | 0.598 / 1.0 | 0.064 / 1.0 | 0.598 / 1.0 |
| burushaski_lorimer | medium | wide | 121/172 | 1.65 | 0.986 / 0.1819 | 1.69 / 0.4283 | 1.19 / 0.2515 | 0.695 / 0.056 | 1.19 / 0.2515 |
| burushaski_lorimer | loose | narrow | 121/172 | 0.465 | 0.505 / 0.6147 | 1.05 / 0.9305 | 0.865 / 0.9461 | 0.495 / 0.5662 | 0.865 / 0.9461 |
| burushaski_lorimer | loose | wide | 121/172 | 1.42 | 1.51 / 0.6632 | 2.12 / 0.8306 | 1.82 / 0.7904 | 1.46 / 0.5742 | 1.82 / 0.7904 |

#### B_3of3+2of3: hits, every family and every dictionary, full grid

| dictionary / family | distance | keywords | units covered | hits | C1 classes dealt mean / P | C2 outside nouns mean / P | C3 sounds dealt by entry mean / P | C4 wrong class same picture mean / P | C3row mean / P |
|---|---|---|---|---|---|---|---|---|---|
| FAMILY Dravidian | strict | narrow | 171/172 | 77 | 79.8 / 0.7631 | 54.9 / 0.0195 | 108 / 1.0 | 77.7 / 0.5967 | 114 / 0.998 |
| FAMILY Dravidian | strict | wide | 171/172 | 136 | 133 / 0.3043 | 94.3 / 0.001 | 133 / 0.3852 | 126 / 0.0085 | 138 / 0.6387 |
| FAMILY Dravidian | medium | narrow | 171/172 | 159 | 160 / 0.6817 | 146 / 0.0305 | 162 / 0.8483 | 159 / 0.6092 | 163 / 0.9421 |
| FAMILY Dravidian | medium | wide | 171/172 | 170 | 169 / 0.4478 | 165 / 0.1 | 168 / 0.3014 | 169 / 0.3333 | 169 / 0.3653 |
| FAMILY Dravidian | loose | narrow | 171/172 | 171 | 171 / 1.0 | 172 / 0.9 | 171 / 0.99 | 171 / 1.0 | 171 / 0.994 |
| FAMILY Dravidian | loose | wide | 171/172 | 171 | 171 / 1.0 | 172 / 0.928 | 171 / 0.998 | 171 / 1.0 | 171 / 1.0 |
| FAMILY Munda | strict | narrow | 171/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.948 / 1.0 | 0 / 1.0 | 1.15 / 1.0 |
| FAMILY Munda | strict | wide | 171/172 | 0 | 0 / 1.0 | 0 / 1.0 | 2 / 1.0 | 0 / 1.0 | 2.27 / 1.0 |
| FAMILY Munda | medium | narrow | 171/172 | 99 | 98.3 / 0.4888 | 61.7 / 0.001 | 83.3 / 0.0579 | 91.2 / 0.037 | 83.2 / 0.0579 |
| FAMILY Munda | medium | wide | 171/172 | 124 | 124 / 0.5907 | 94.3 / 0.008 | 118 / 0.2774 | 122 / 0.3763 | 118 / 0.2774 |
| FAMILY Munda | loose | narrow | 171/172 | 169 | 169 / 0.7296 | 162 / 0.0955 | 167 / 0.2854 | 169 / 0.6317 | 167 / 0.2475 |
| FAMILY Munda | loose | wide | 171/172 | 171 | 171 / 0.6057 | 165 / 0.1 | 170 / 0.3872 | 170 / 0.4988 | 170 / 0.3653 |
| FAMILY Indo-Aryan | strict | narrow | 171/172 | 61 | 58.4 / 0.3223 | 30.5 / 0.002 | 75.3 / 0.982 | 56.8 / 0.1659 | 75.3 / 0.982 |
| FAMILY Indo-Aryan | strict | wide | 171/172 | 90 | 89.4 / 0.5027 | 59.2 / 0.008 | 101 / 0.9281 | 85.5 / 0.1704 | 101 / 0.9281 |
| FAMILY Indo-Aryan | medium | narrow | 171/172 | 132 | 131 / 0.4308 | 131 / 0.5067 | 145 / 0.998 | 130 / 0.3348 | 145 / 0.998 |
| FAMILY Indo-Aryan | medium | wide | 171/172 | 144 | 145 / 0.7491 | 154 / 0.95 | 157 / 1.0 | 146 / 0.8391 | 157 / 1.0 |
| FAMILY Indo-Aryan | loose | narrow | 171/172 | 171 | 170 / 0.4738 | 171 / 0.7336 | 171 / 0.6727 | 170 / 0.2779 | 171 / 0.6727 |
| FAMILY Indo-Aryan | loose | wide | 171/172 | 171 | 171 / 1.0 | 171 / 0.8156 | 171 / 0.8663 | 171 / 1.0 | 171 / 0.8663 |
| FAMILY Sumerian | strict | narrow | 161/172 | 44 | 43.5 / 0.5007 | 18.8 / 0.003 | 59 / 0.9701 | 37.2 / 0.036 | 63.7 / 0.996 |
| FAMILY Sumerian | strict | wide | 161/172 | 85 | 76 / 0.021 | 42.5 / 0.001 | 86.8 / 0.6228 | 74.2 / 0.0005 | 92 / 0.7804 |
| FAMILY Sumerian | medium | narrow | 161/172 | 111 | 113 / 0.6992 | 80.5 / 0.0145 | 114 / 0.6667 | 105 / 0.0695 | 119 / 0.8842 |
| FAMILY Sumerian | medium | wide | 161/172 | 139 | 138 / 0.4113 | 107 / 0.0135 | 135 / 0.3034 | 137 / 0.2684 | 140 / 0.6327 |
| FAMILY Sumerian | loose | narrow | 161/172 | 152 | 151 / 0.4493 | 143 / 0.2474 | 153 / 0.7066 | 150 / 0.2299 | 154 / 0.8483 |
| FAMILY Sumerian | loose | wide | 161/172 | 156 | 156 / 0.7296 | 149 / 0.2799 | 158 / 0.8543 | 156 / 0.6602 | 158 / 0.8962 |
| FAMILY Akkadian | strict | narrow | 136/172 | 0 | 0.448 / 1.0 | 0 / 1.0 | 2.86 / 1.0 | 0.628 / 1.0 | 2.86 / 1.0 |
| FAMILY Akkadian | strict | wide | 136/172 | 5 | 2.14 / 0.0395 | 0 / 0.0005 | 5.01 / 0.4571 | 1.54 / 0.01 | 5.01 / 0.4571 |
| FAMILY Akkadian | medium | narrow | 136/172 | 15 | 15.5 / 0.6417 | 6.64 / 0.0915 | 17.4 / 0.6846 | 15.3 / 0.6197 | 17.4 / 0.6846 |
| FAMILY Akkadian | medium | wide | 136/172 | 32 | 28.6 / 0.1399 | 10.1 / 0.012 | 27.9 / 0.3094 | 26.5 / 0.038 | 27.9 / 0.3094 |
| FAMILY Akkadian | loose | narrow | 136/172 | 85 | 91.3 / 0.967 | 70.8 / 0.2009 | 83.7 / 0.481 | 91.3 / 0.9765 | 83.7 / 0.481 |
| FAMILY Akkadian | loose | wide | 136/172 | 110 | 112 / 0.7996 | 91.4 / 0.1454 | 102 / 0.2575 | 111 / 0.6702 | 102 / 0.2575 |
| FAMILY Elamite | strict | narrow | 105/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| FAMILY Elamite | strict | wide | 105/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.006 / 1.0 | 0 / 1.0 | 0.006 / 1.0 |
| FAMILY Elamite | medium | narrow | 105/172 | 3 | 2.08 / 0.3388 | 0.87 / 0.1259 | 1.22 / 0.1537 | 1.99 / 0.3083 | 1.22 / 0.1537 |
| FAMILY Elamite | medium | wide | 105/172 | 3 | 2.88 / 0.5617 | 2.02 / 0.2869 | 6.74 / 0.7745 | 3.06 / 0.6172 | 6.74 / 0.7745 |
| FAMILY Elamite | loose | narrow | 105/172 | 18 | 20.9 / 0.8461 | 7.28 / 0.071 | 24.9 / 0.8124 | 23 / 0.96 | 24.9 / 0.8124 |
| FAMILY Elamite | loose | wide | 105/172 | 69 | 60.3 / 0.0205 | 17.1 / 0.0005 | 61.6 / 0.2315 | 57.4 / 0.0005 | 61.6 / 0.2315 |
| FAMILY Burushaski | strict | narrow | 121/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| FAMILY Burushaski | strict | wide | 121/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| FAMILY Burushaski | medium | narrow | 121/172 | 0 | 0.194 / 1.0 | 1.88 / 1.0 | 3.83 / 1.0 | 0.32 / 1.0 | 3.83 / 1.0 |
| FAMILY Burushaski | medium | wide | 121/172 | 4 | 2.54 / 0.2314 | 5.01 / 0.5817 | 7.34 / 0.7106 | 2.33 / 0.1874 | 7.34 / 0.7106 |
| FAMILY Burushaski | loose | narrow | 121/172 | 43 | 43.1 / 0.5637 | 37.4 / 0.3208 | 46.8 / 0.6667 | 41.6 / 0.3773 | 46.8 / 0.6667 |
| FAMILY Burushaski | loose | wide | 121/172 | 62 | 63.4 / 0.7356 | 60.6 / 0.4683 | 64.9 / 0.5968 | 64.6 / 0.8866 | 64.9 / 0.5968 |
| dedr_tamil | strict | narrow | 170/172 | 53 | 58.2 / 0.903 | 25.9 / 0.0015 | 87.9 / 1.0 | 57.6 / 0.912 | 95.8 / 1.0 |
| dedr_tamil | strict | wide | 170/172 | 99 | 104 / 0.8761 | 57.2 / 0.001 | 108 / 0.7844 | 98 / 0.4393 | 114 / 0.8902 |
| dedr_tamil | medium | narrow | 170/172 | 138 | 138 / 0.5527 | 112 / 0.0035 | 144 / 0.8144 | 135 / 0.2744 | 147 / 0.9122 |
| dedr_tamil | medium | wide | 170/172 | 164 | 161 / 0.1034 | 145 / 0.005 | 159 / 0.1018 | 161 / 0.097 | 160 / 0.1776 |
| dedr_tamil | loose | narrow | 170/172 | 170 | 170 / 0.6192 | 167 / 0.3098 | 169 / 0.3832 | 170 / 0.5912 | 169 / 0.477 |
| dedr_tamil | loose | wide | 170/172 | 170 | 170 / 0.911 | 168 / 0.4223 | 170 / 0.6986 | 170 / 0.904 | 170 / 0.8104 |
| dedr_malayalam | strict | narrow | 163/172 | 23 | 21.5 / 0.3973 | 7.8 / 0.0055 | 18.4 / 0.2635 | 20.9 / 0.2924 | 19.5 / 0.3313 |
| dedr_malayalam | strict | wide | 163/172 | 61 | 57 / 0.2259 | 19 / 0.0005 | 39.4 / 0.014 | 48.8 / 0.004 | 40.5 / 0.0279 |
| dedr_malayalam | medium | narrow | 163/172 | 109 | 112 / 0.7836 | 66.2 / 0.001 | 98.9 / 0.1497 | 107 / 0.3348 | 101 / 0.1916 |
| dedr_malayalam | medium | wide | 163/172 | 139 | 140 / 0.7021 | 104 / 0.0035 | 131 / 0.1118 | 135 / 0.1544 | 133 / 0.1816 |
| dedr_malayalam | loose | narrow | 163/172 | 158 | 159 / 0.7806 | 154 / 0.3833 | 158 / 0.5768 | 158 / 0.6787 | 158 / 0.6906 |
| dedr_malayalam | loose | wide | 163/172 | 161 | 161 / 0.8801 | 161 / 0.6257 | 161 / 0.6367 | 161 / 0.8676 | 161 / 0.7285 |
| dedr_kannada | strict | narrow | 160/172 | 26 | 24.6 / 0.3843 | 11.9 / 0.014 | 25.7 / 0.515 | 23.5 / 0.2724 | 32.5 / 0.8463 |
| dedr_kannada | strict | wide | 160/172 | 49 | 51.2 / 0.7306 | 25 / 0.009 | 48 / 0.475 | 45.8 / 0.2289 | 55.7 / 0.7984 |
| dedr_kannada | medium | narrow | 160/172 | 106 | 104 / 0.3768 | 64.3 / 0.001 | 91.5 / 0.0599 | 97.6 / 0.0245 | 105 / 0.505 |
| dedr_kannada | medium | wide | 160/172 | 135 | 133 / 0.3238 | 103 / 0.006 | 126 / 0.1357 | 130 / 0.0715 | 138 / 0.7166 |
| dedr_kannada | loose | narrow | 160/172 | 157 | 157 / 0.7191 | 147 / 0.1829 | 157 / 0.5569 | 157 / 0.7986 | 158 / 0.8683 |
| dedr_kannada | loose | wide | 160/172 | 160 | 160 / 0.6177 | 152 / 0.2174 | 159 / 0.5429 | 160 / 0.5722 | 160 / 0.6727 |
| dedr_telugu | strict | narrow | 162/172 | 17 | 12.2 / 0.0415 | 6.04 / 0.0305 | 15.5 / 0.4551 | 10.1 / 0.001 | 18.7 / 0.6228 |
| dedr_telugu | strict | wide | 162/172 | 31 | 26.7 / 0.1069 | 12.5 / 0.013 | 26.9 / 0.3393 | 22 / 0.0005 | 33.3 / 0.6248 |
| dedr_telugu | medium | narrow | 162/172 | 75 | 68.9 / 0.0915 | 34.8 / 0.0005 | 63.9 / 0.1397 | 63.1 / 0.0055 | 72.7 / 0.4172 |
| dedr_telugu | medium | wide | 162/172 | 110 | 106 / 0.2269 | 67.2 / 0.0005 | 95.3 / 0.0818 | 100 / 0.0185 | 104 / 0.2535 |
| dedr_telugu | loose | narrow | 162/172 | 147 | 151 / 0.954 | 134 / 0.1539 | 151 / 0.8224 | 153 / 0.9935 | 152 / 0.8802 |
| dedr_telugu | loose | wide | 162/172 | 159 | 159 / 0.5912 | 146 / 0.1234 | 159 / 0.6407 | 159 / 0.5432 | 159 / 0.6687 |
| tamil_wiktionary | strict | narrow | 169/172 | 46 | 42.6 / 0.2449 | 18.5 / 0.001 | 42.6 / 0.3333 | 37.9 / 0.029 | 42.3 / 0.3034 |
| tamil_wiktionary | strict | wide | 169/172 | 72 | 70 / 0.3563 | 37.6 / 0.003 | 63.8 / 0.1956 | 63.6 / 0.021 | 63.8 / 0.1776 |
| tamil_wiktionary | medium | narrow | 169/172 | 122 | 126 / 0.8896 | 98.4 / 0.0115 | 120 / 0.4012 | 125 / 0.8356 | 119 / 0.4052 |
| tamil_wiktionary | medium | wide | 169/172 | 148 | 148 / 0.5512 | 132 / 0.062 | 145 / 0.3832 | 143 / 0.0585 | 145 / 0.3613 |
| tamil_wiktionary | loose | narrow | 169/172 | 168 | 168 / 0.6202 | 167 / 0.5357 | 167 / 0.3752 | 168 / 0.6217 | 166 / 0.3513 |
| tamil_wiktionary | loose | wide | 169/172 | 169 | 169 / 1.0 | 170 / 0.7261 | 168 / 0.479 | 169 / 1.0 | 168 / 0.4251 |
| telugu_wiktionary | strict | narrow | 171/172 | 17 | 16.3 / 0.4748 | 5.49 / 0.0105 | 32.8 / 0.994 | 14.1 / 0.1714 | 32.9 / 1.0 |
| telugu_wiktionary | strict | wide | 171/172 | 27 | 25.2 / 0.3348 | 9.43 / 0.006 | 43.8 / 1.0 | 21.9 / 0.043 | 44.2 / 1.0 |
| telugu_wiktionary | medium | narrow | 171/172 | 82 | 80.1 / 0.3658 | 55.6 / 0.0045 | 92.3 / 0.9042 | 72.7 / 0.012 | 92.7 / 0.9122 |
| telugu_wiktionary | medium | wide | 171/172 | 102 | 102 / 0.5712 | 83.6 / 0.0745 | 118 / 0.98 | 98.7 / 0.2364 | 118 / 0.9741 |
| telugu_wiktionary | loose | narrow | 171/172 | 165 | 165 / 0.7236 | 163 / 0.4453 | 160 / 0.1357 | 165 / 0.5852 | 160 / 0.1457 |
| telugu_wiktionary | loose | wide | 171/172 | 168 | 168 / 0.6017 | 167 / 0.5822 | 165 / 0.1936 | 168 / 0.5337 | 165 / 0.1737 |
| kannada_wiktionary | strict | narrow | 162/172 | 0 | 0 / 1.0 | 0 / 1.0 | 1.46 / 1.0 | 0 / 1.0 | 1.46 / 1.0 |
| kannada_wiktionary | strict | wide | 162/172 | 0 | 0.124 / 1.0 | 1.52 / 1.0 | 3.53 / 1.0 | 0.152 / 1.0 | 3.53 / 1.0 |
| kannada_wiktionary | medium | narrow | 162/172 | 32 | 35.8 / 0.8596 | 19.5 / 0.059 | 18.6 / 0.0499 | 34 / 0.7551 | 18.6 / 0.0499 |
| kannada_wiktionary | medium | wide | 162/172 | 64 | 68.3 / 0.8501 | 40.5 / 0.027 | 34.7 / 0.002 | 63.4 / 0.4913 | 34.7 / 0.002 |
| kannada_wiktionary | loose | narrow | 162/172 | 123 | 126 / 0.8311 | 118 / 0.3668 | 109 / 0.1078 | 123 / 0.5687 | 109 / 0.1078 |
| kannada_wiktionary | loose | wide | 162/172 | 146 | 147 / 0.7141 | 140 / 0.3308 | 133 / 0.0639 | 143 / 0.1634 | 133 / 0.0639 |
| santali_campbell | strict | narrow | 167/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.028 / 1.0 | 0 / 1.0 | 0.028 / 1.0 |
| santali_campbell | strict | wide | 167/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.076 / 1.0 | 0 / 1.0 | 0.076 / 1.0 |
| santali_campbell | medium | narrow | 167/172 | 72 | 71.2 / 0.4838 | 42.9 / 0.0095 | 62.5 / 0.1577 | 68.5 / 0.2424 | 62.5 / 0.1577 |
| santali_campbell | medium | wide | 167/172 | 102 | 99.5 / 0.3493 | 70.3 / 0.0115 | 92.8 / 0.1976 | 101 / 0.4323 | 92.8 / 0.1976 |
| santali_campbell | loose | narrow | 167/172 | 162 | 163 / 0.7441 | 151 / 0.1009 | 156 / 0.1018 | 162 / 0.6642 | 156 / 0.1018 |
| santali_campbell | loose | wide | 167/172 | 166 | 165 / 0.4433 | 156 / 0.0825 | 161 / 0.1297 | 165 / 0.3063 | 161 / 0.1297 |
| santali_bodding5 | strict | narrow | 135/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| santali_bodding5 | strict | wide | 135/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| santali_bodding5 | medium | narrow | 135/172 | 3 | 2.2 / 0.3778 | 2.59 / 0.4398 | 5.36 / 0.7186 | 2 / 0.3173 | 5.36 / 0.7186 |
| santali_bodding5 | medium | wide | 135/172 | 5 | 5.7 / 0.7406 | 6.03 / 0.5962 | 10.2 / 0.8204 | 6.45 / 0.8901 | 10.2 / 0.8204 |
| santali_bodding5 | loose | narrow | 135/172 | 42 | 40.2 / 0.3648 | 31.5 / 0.1799 | 60.2 / 0.9581 | 37.9 / 0.1684 | 60.2 / 0.9581 |
| santali_bodding5 | loose | wide | 135/172 | 64 | 65.5 / 0.6927 | 55 / 0.3028 | 84.2 / 0.9501 | 59.9 / 0.1749 | 84.2 / 0.9501 |
| santali_wiktionary | strict | narrow | 141/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.232 / 1.0 | 0 / 1.0 | 0.414 / 1.0 |
| santali_wiktionary | strict | wide | 141/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.502 / 1.0 | 0 / 1.0 | 0.758 / 1.0 |
| santali_wiktionary | medium | narrow | 141/172 | 4 | 2.42 / 0.2144 | 4.3 / 0.5202 | 6.16 / 0.5968 | 1.86 / 0.0875 | 5.8 / 0.5888 |
| santali_wiktionary | medium | wide | 141/172 | 12 | 11.4 / 0.4723 | 7.7 / 0.1889 | 11.1 / 0.4511 | 9.21 / 0.1604 | 10.8 / 0.4132 |
| santali_wiktionary | loose | narrow | 141/172 | 57 | 60.9 / 0.8636 | 45.5 / 0.1569 | 56.1 / 0.4731 | 62.4 / 0.9275 | 55.1 / 0.4571 |
| santali_wiktionary | loose | wide | 141/172 | 89 | 91.1 / 0.7426 | 71.2 / 0.0975 | 77.6 / 0.1357 | 90.5 / 0.7321 | 77.5 / 0.1277 |
| mundari_bhadra | strict | narrow | 171/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.704 / 1.0 | 0 / 1.0 | 0.704 / 1.0 |
| mundari_bhadra | strict | wide | 171/172 | 0 | 0 / 1.0 | 0 / 1.0 | 1.45 / 1.0 | 0 / 1.0 | 1.45 / 1.0 |
| mundari_bhadra | medium | narrow | 171/172 | 67 | 62 / 0.1569 | 29.6 / 0.0005 | 46 / 0.02 | 51.7 / 0.0005 | 46 / 0.02 |
| mundari_bhadra | medium | wide | 171/172 | 93 | 92.3 / 0.4838 | 51 / 0.001 | 75.7 / 0.0878 | 85.6 / 0.0645 | 75.7 / 0.0878 |
| mundari_bhadra | loose | narrow | 171/172 | 162 | 163 / 0.7756 | 131 / 0.0005 | 153 / 0.0838 | 163 / 0.7601 | 153 / 0.0838 |
| mundari_bhadra | loose | wide | 171/172 | 168 | 168 / 0.7501 | 145 / 0.0025 | 163 / 0.1317 | 168 / 0.6847 | 163 / 0.1317 |
| sanskrit_mw | strict | narrow | 171/172 | 60 | 57.7 / 0.3478 | 29.9 / 0.001 | 74.3 / 0.982 | 56.2 / 0.2009 | 74.3 / 0.982 |
| sanskrit_mw | strict | wide | 171/172 | 89 | 88.7 / 0.5307 | 57.9 / 0.0075 | 99.7 / 0.9261 | 84.9 / 0.2054 | 99.7 / 0.9261 |
| sanskrit_mw | medium | narrow | 171/172 | 132 | 131 / 0.3963 | 129 / 0.4123 | 144 / 0.994 | 130 / 0.2929 | 144 / 0.994 |
| sanskrit_mw | medium | wide | 171/172 | 144 | 144 / 0.6887 | 154 / 0.938 | 156 / 1.0 | 145 / 0.7761 | 156 / 1.0 |
| sanskrit_mw | loose | narrow | 171/172 | 171 | 170 / 0.3963 | 171 / 0.7336 | 170 / 0.5469 | 170 / 0.2154 | 170 / 0.5469 |
| sanskrit_mw | loose | wide | 171/172 | 171 | 171 / 0.7621 | 171 / 0.8156 | 171 / 0.7824 | 171 / 0.7111 | 171 / 0.7824 |
| oia_turner | strict | narrow | 166/172 | 1 | 0.707 / 0.5307 | 2.2 / 0.7471 | 2.72 / 0.7844 | 0.603 / 0.4723 | 2.72 / 0.7844 |
| oia_turner | strict | wide | 166/172 | 1 | 2.51 / 0.945 | 4.4 / 0.9105 | 6.34 / 0.9661 | 4.47 / 0.995 | 6.34 / 0.9661 |
| oia_turner | medium | narrow | 166/172 | 21 | 20.6 / 0.5117 | 12 / 0.083 | 22.8 / 0.5968 | 18.7 / 0.2234 | 22.8 / 0.5968 |
| oia_turner | medium | wide | 166/172 | 34 | 37.2 / 0.8221 | 25.3 / 0.1704 | 43.6 / 0.8663 | 35.1 / 0.6737 | 43.6 / 0.8663 |
| oia_turner | loose | narrow | 166/172 | 137 | 131 / 0.0765 | 129 / 0.2869 | 146 / 0.9661 | 127 / 0.0025 | 146 / 0.9661 |
| oia_turner | loose | wide | 166/172 | 148 | 149 / 0.6962 | 148 / 0.5917 | 157 / 0.986 | 147 / 0.3653 | 157 / 0.986 |
| proto_indoiranian_wiktionary | strict | narrow | 125/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.22 / 1.0 | 0 / 1.0 | 0.22 / 1.0 |
| proto_indoiranian_wiktionary | strict | wide | 125/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.536 / 1.0 | 0 / 1.0 | 0.536 / 1.0 |
| proto_indoiranian_wiktionary | medium | narrow | 125/172 | 1 | 0.646 / 0.4953 | 0.137 / 0.0985 | 1.42 / 0.3892 | 0.632 / 0.4793 | 1.42 / 0.3892 |
| proto_indoiranian_wiktionary | medium | wide | 125/172 | 4 | 2.94 / 0.3423 | 2.14 / 0.1934 | 3.32 / 0.3373 | 2.4 / 0.1969 | 3.32 / 0.3373 |
| proto_indoiranian_wiktionary | loose | narrow | 125/172 | 50 | 47.3 / 0.2719 | 30.1 / 0.054 | 36.6 / 0.0918 | 45.6 / 0.1519 | 36.6 / 0.0918 |
| proto_indoiranian_wiktionary | loose | wide | 125/172 | 64 | 61.6 / 0.2989 | 43.1 / 0.06 | 62.9 / 0.483 | 58.3 / 0.067 | 62.9 / 0.483 |
| sumerian_halloran | strict | narrow | 159/172 | 44 | 43.2 / 0.4713 | 15.6 / 0.0005 | 55 / 0.9042 | 36.9 / 0.029 | 60 / 0.98 |
| sumerian_halloran | strict | wide | 159/172 | 81 | 73 / 0.0275 | 36 / 0.0015 | 81.2 / 0.5429 | 71.2 / 0.0005 | 86.6 / 0.7265 |
| sumerian_halloran | medium | narrow | 159/172 | 105 | 106 / 0.6422 | 72.3 / 0.0105 | 106 / 0.5928 | 98.6 / 0.0595 | 114 / 0.8782 |
| sumerian_halloran | medium | wide | 159/172 | 128 | 127 / 0.4023 | 98.6 / 0.0345 | 127 / 0.4451 | 126 / 0.2719 | 133 / 0.7984 |
| sumerian_halloran | loose | narrow | 159/172 | 136 | 138 / 0.8036 | 137 / 0.5802 | 147 / 0.976 | 136 / 0.5862 | 149 / 0.996 |
| sumerian_halloran | loose | wide | 159/172 | 147 | 145 / 0.2104 | 142 / 0.4018 | 153 / 0.9381 | 143 / 0.0285 | 155 / 0.984 |
| sumerian_wiktionary | strict | narrow | 152/172 | 6 | 5.63 / 0.5137 | 3.36 / 0.1814 | 12.8 / 0.8663 | 2.58 / 0.006 | 12.2 / 0.8403 |
| sumerian_wiktionary | strict | wide | 152/172 | 15 | 13.8 / 0.3948 | 8.93 / 0.1454 | 24.7 / 0.8942 | 11.6 / 0.1294 | 24.9 / 0.8982 |
| sumerian_wiktionary | medium | narrow | 152/172 | 41 | 44.3 / 0.7841 | 27.7 / 0.0745 | 50.4 / 0.8623 | 35.9 / 0.1309 | 49.5 / 0.8363 |
| sumerian_wiktionary | medium | wide | 152/172 | 77 | 77.7 / 0.6127 | 49.2 / 0.017 | 78.8 / 0.5988 | 71.4 / 0.1064 | 78.4 / 0.5589 |
| sumerian_wiktionary | loose | narrow | 152/172 | 129 | 127 / 0.2734 | 87.2 / 0.0025 | 120 / 0.1796 | 122 / 0.027 | 121 / 0.1737 |
| sumerian_wiktionary | loose | wide | 152/172 | 140 | 139 / 0.4368 | 105 / 0.012 | 140 / 0.5589 | 138 / 0.3103 | 140 / 0.5549 |
| akkadian_wiktionary | strict | narrow | 136/172 | 0 | 0.448 / 1.0 | 0 / 1.0 | 2.86 / 1.0 | 0.628 / 1.0 | 2.86 / 1.0 |
| akkadian_wiktionary | strict | wide | 136/172 | 5 | 2.14 / 0.0395 | 0 / 0.0005 | 5.01 / 0.4571 | 1.54 / 0.01 | 5.01 / 0.4571 |
| akkadian_wiktionary | medium | narrow | 136/172 | 15 | 15.5 / 0.6417 | 6.64 / 0.0915 | 17.4 / 0.6846 | 15.3 / 0.6197 | 17.4 / 0.6846 |
| akkadian_wiktionary | medium | wide | 136/172 | 32 | 28.6 / 0.1399 | 10.1 / 0.012 | 27.9 / 0.3094 | 26.5 / 0.038 | 27.9 / 0.3094 |
| akkadian_wiktionary | loose | narrow | 136/172 | 85 | 91.3 / 0.967 | 70.8 / 0.2009 | 83.7 / 0.481 | 91.3 / 0.9765 | 83.7 / 0.481 |
| akkadian_wiktionary | loose | wide | 136/172 | 110 | 112 / 0.7996 | 91.4 / 0.1454 | 102 / 0.2575 | 111 / 0.6702 | 102 / 0.2575 |
| elamite_hinzkoch | strict | narrow | 105/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| elamite_hinzkoch | strict | wide | 105/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0.006 / 1.0 | 0 / 1.0 | 0.006 / 1.0 |
| elamite_hinzkoch | medium | narrow | 105/172 | 3 | 2.08 / 0.3388 | 0.87 / 0.1259 | 1.22 / 0.1537 | 1.99 / 0.3083 | 1.22 / 0.1537 |
| elamite_hinzkoch | medium | wide | 105/172 | 3 | 2.88 / 0.5617 | 2.02 / 0.2869 | 6.74 / 0.7745 | 3.06 / 0.6172 | 6.74 / 0.7745 |
| elamite_hinzkoch | loose | narrow | 105/172 | 18 | 20.9 / 0.8461 | 7.28 / 0.071 | 24.9 / 0.8124 | 23 / 0.96 | 24.9 / 0.8124 |
| elamite_hinzkoch | loose | wide | 105/172 | 69 | 60.3 / 0.0205 | 17.1 / 0.0005 | 61.6 / 0.2315 | 57.4 / 0.0005 | 61.6 / 0.2315 |
| burushaski_lorimer | strict | narrow | 121/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| burushaski_lorimer | strict | wide | 121/172 | 0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 | 0 / 1.0 |
| burushaski_lorimer | medium | narrow | 121/172 | 0 | 0.194 / 1.0 | 1.88 / 1.0 | 3.83 / 1.0 | 0.32 / 1.0 | 3.83 / 1.0 |
| burushaski_lorimer | medium | wide | 121/172 | 4 | 2.54 / 0.2314 | 5.01 / 0.5817 | 7.34 / 0.7106 | 2.33 / 0.1874 | 7.34 / 0.7106 |
| burushaski_lorimer | loose | narrow | 121/172 | 43 | 43.1 / 0.5637 | 37.4 / 0.3208 | 46.8 / 0.6667 | 41.6 / 0.3773 | 46.8 / 0.6667 |
| burushaski_lorimer | loose | wide | 121/172 | 62 | 63.4 / 0.7356 | 60.6 / 0.4683 | 64.9 / 0.5968 | 64.6 / 0.8866 | 64.9 / 0.5968 |

