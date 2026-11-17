# The atlas of the fixed phrases

Scripts (in `work_scripts/`, each has its predictions in its top docstring, written before it first ran): `phrases_common.py` (loaders), `phrases_1_list.py` (the list and its controls), `phrases_2_atlas.py` (the atlas), `phrases_3_kinds.py` and `phrases_3b_pooled.py` (kinds of phrase), `phrases_4_cities.py` (inter-city), `phrases_5_families.py`, `phrases_5b_variants.py`, `phrases_5c_series.py` (families, paradigms, numbered series), `phrases_6_office.py` (920-060-741), `phrases_7_minor.py` (rarer phrases), `phrases_8_time.py` (time). Tables and logs (`log_*.txt`) in `work_data/phrases/`. Date 2026-11-17. No word is attached to any sign anywhere: sign numbers, pictures, jobs and findspots only.

## Terms in plain words

- **Phrase**: 2, 3 or 4 signs that stand right next to each other. A lost or unclear sign cuts a run.
- **Fixed phrase**: a phrase that passes the rule in section 1: it turns up in 8+ different texts, almost always in one order, far more often than the signs' own frequencies would put them together.
- **Lift**: how many times more often the run occurs than chance placement by sign frequency would give. Lift 5 = five times.
- **Distinct text**: identical sign strings counted once, so moulded copies do not inflate a count. **Object**: one physical thing; an object carries a phrase once. **Carrier**: an object holding the phrase.
- **Job class**: the role of a sign in frame v2 (front word, slot after the front word, name front, name part, number, counted thing, closer, after-jar title, and so on; `work_data/frame/classes_v2.csv`).
- **Shuffle within site**: carriers replaced by random objects drawn from the same city (and, where stated, the same object kind), thousands of times. P = share of shuffles at least as extreme as the real phrase. Small P = the real pattern is not what chance gives.
- **Building / block / area**: the registry's findspot keys: area = excavation area, building = area + house (Mohenjo-daro) or grid square (Harappa), block = area + block number.
- **Bin**: early / middle / late, from `work_data/time/time_axis.csv`.
- **New texts**: the second catalogue's 889 distinct lines that have no partner in the first catalogue, never used to shape any rule.
- **Copies removed**: carriers with the identical text in the same building count once.

## 1. What was found

**1. There are 136 fixed phrases, and the same rule on order-shuffled texts finds almost none.** Rule fixed in advance: in 8+ distinct texts, in order 90%+ of the time (run against its reverse), lift 5+, on the first catalogue (3,499 distinct texts, 12,994 sign tokens); then confirmed on the new texts. Result: **99 pairs, 36 triples, 1 four-sign run (255-435-690-740)**. Control: the same rule with sign order shuffled inside every text, 20 shuffles: mean 0.45 phrases pass (max 2), against 136. On the new texts: 99 phrases were testable (the first-catalogue lift predicts 2+ occurrences), **79 confirmed (80%)**, 20 not confirmed (most are near misses: seen once, or one reversed case; 176-740 is 11 in order against 2 reversed, order 85% against the 90% bar), 37 untestable (too rare in the new texts to predict 2). 817-002 and 706-033 have 0 new-text occurrences because those signs do not appear in the new texts' numbering. 35 of the 40 fixed pairs of frame v2 pass the rule (the five that do not: 235-240, 550-525, 798-240, 798-740, 840-032). Rarer phrases (4 to 7 texts, same order and lift rule, not inside a main phrase): 277 more, against 13 on average in shuffled texts. What it means: the script has a stock of a few hundred stock phrases, a third of them tested out on fresh texts. Objects carrying at least one: 2,110 of 4,694 (45%); seals 53%, copper tablets 71%, tablets 50%, pots 8%.

By place in the text (frame v2 classes; rule in `phrases_1_list.py`): **name 42, front 39, ending 28, count line 27** (7 nested phrases included; 129 non-nested). Front = holds a front word or the slot after it (861-002, 817-002, 820-002, 920-060, 920-060-741, 692-060). Count line = holds a number or a measure (705-033, 033-520, 705-033-520). Ending = a pair ending in a closer or after-jar title (760-740, 100-740, 740-090, 740-400, 176-740). Name = the rest, including triples that end in a closer (590-390-740, 255-435-690-740, 435-690-740). Confirmation by group: front 23 of 28 testable, name 25 of 31, ending 16 of 20, count line 15 of 20.

**2. The atlas is written: `work_data/phrases/atlas.csv` (top 100 non-nested phrases by distinct texts, ranks 1 to 100, down to 9 texts), `atlas_all.csv` (all 136).** Columns: cities, areas / blocks / buildings at Mohenjo-daro and Harappa, object kinds, time bins, animal and stand letter, abroad, short-horned bull, job class before and after, new-text count. Headlines:
- The front words stand at the text edge: 861-002 starts the text in 83% of its occurrences, 817-002 96%, 820-002 93%, 920-060 98%, 920-060-741 100%. After them comes a name part (33% name part, 30% name front for 861-002).
- Ending pairs finish the text: 740-400 ends it 96% of the time, 760-740 87%, 740-090 90%.
- **740-400 is a Harappa tablet ending**: 245 objects, 219 of them tablets, 213 at Harappa (87%), 6 with a unicorn; 740-090 (jar then man) sits on seals and tablets in 9 cities.
- **Fixed phrases do not drift in time**: of the 101 phrases with 8+ dated carriers, 86 have carriers in all three bins, and 2 show a time trend at P 0.05 against 5.1 expected by chance (bin labels shuffled within excavation area, 5,000 shuffles). Same as `history.md`: the formula was fixed from the first city levels.

**3. The phrases are city-wide: no phrase is tied to one building, and almost none to one city.** (kinds in the table below; tests in `phrases_3_kinds.py`, `phrases_3b_pooled.py`, `phrases_7_minor.py`.) Shared buildings among the carriers of all 100 phrases: 146 observed against 118.0 expected by chance (Z 2.91), but **with copies removed, 108 against 111.1 (Z -0.33)**: the whole excess is identical tablets lying in the same room. The three phrases that first looked house-bound (740-400, 176-740, 415-220) lose it: P 0.34, 0.13, 0.016 with copies removed. The 277 rarer phrases, where a house phrase would hide: 74 testable, 5 shared-building carriers against 5.6 expected, 1 phrase under P 0.05 against 3.7 expected.

**4. Where phrases do lean, it is on kind of object, and it is the strongest property in the table.** Six phrases sit on non-seals far more than the cities they come from predict (non-seal share against the same-city expectation; P from 2,000 shuffles within site): 740-400 95.5% against 73.1% (P 0.0005); 752-740 82% against 39%; 235-705-033 74% against 39%; 845-407 73% against 30%; 142-617 62% against 30%; 176-740 69% against 59% (P 0.004). The same flag on random object sets of the same sizes drawn from the whole catalogue: 0.0%.

**5. The numbered slots are real, and they count different things.** Number sign right before the counted sign, over all distinct texts, against the general mix of number signs (shuffle of what follows each number, 5,000 shuffles):
- before the fish (220): the tall two (032) 56% (64 of 114), three strokes 14%, six stacked 11%; the general mix has the tall two at 23%. P 0.0002.
- before the tree signs (390, 405, 407): short strokes, mainly four (30%, 35%, 50% for the three trees), three, six, five; tall strokes 5 of 61 before 390 (8%) against 32% in the general mix. P 0.0002 (390), 0.045 (405), 0.006 (407).
- before the cup (700): tall strokes, three tall 38%, two tall 18%, four tall 15%. P 0.0014.
- before leaf-on-tree (806): the A-with-comb signs 467, 468, 472 and others: 23 of 31 (74%).
What it means: the two stroke heights are two counting series for two kinds of thing (fish count: a tall series, mostly 2; tree count: a short series 3 to 6; cup count: a tall series 1 to 4), as `MAP.md` guessed.

**6. The overseas animal does not go with many-city phrases.** (section 4 below.) Pooled over the 39 phrases found in 5+ cities, 57 short-horned-bull seals of 1,378 seal carriers against 57.7 expected from their cities (P 0.61).

**7. 920-060-741 is a shared heading over many different texts, with one repeated sub-line.** (section 6 below.)

## 2. Phrase kinds by behaviour (top 100)

Tests and flags were fixed before the run (`phrases_3_kinds.py` docstring). Counts after the redesign (copies removed from the house test):

| kind | rule in short | how many of the top 100 | control |
|---|---|---|---|
| HOUSE: tied to one building or block | 8+ carriers with findspot, shared-building P 0.005 or less within site and object kind, copies removed, 2+ time bins | **0** (3 on the raw test: 740-400, 176-740, 415-220; all three fall away with copies removed) | pooled excess with copies removed 108 against 111.1 expected (Z -0.33); rarer phrases 5 against 5.6; random sets flagged 0.1% |
| OFFICE / spread: many cities, no tie, holder varies | 8+ carriers, 4+ cities, no building or block tie, something else beside the phrase in 8+ texts and its rest varies (rest strings distinct 0.8+) | **51** (names 16, front 15, count line 11, ending 9) | random object sets of the same size: 76% (same kind mix) to 83% (any objects) get this flag. The flag means "city-wide, not tied to a place or a building", nothing more |
| GOODS: sits on tags, pots, tablets | non-seal share 0.5+, P 0.005 or less against the same cities | **6**: 740-400, 176-740, 752-740, 235-705-033, 845-407, 142-617 | random sets: 0.0% (any objects), 5.4% (set to the phrase's own kind mix, which is circular) |
| PLACE: tied to one city or mound | top city 80%+ of carriers and P 0.005 or less against draws of the same object kinds; or one Mohenjo-daro / Harappa area holding 60%+ with P 0.005 or less | **2**: 923-740 (Mohenjo-daro 90% against 71% expected), 142-617 (90% against 72%; also goods) | random sets: 0.1% |
| none of these: found in only 2 or 3 cities, no tie | | **42** | |

Primary kind (one per phrase, goods and place joined where both): spread 51, regional (2 or 3 cities) 42, goods 5, place 1, goods and place 1, house 0. Group by kind: front 15 spread / 15 regional; names 16 spread / 12 regional / 1 goods / 1 goods+place; endings 9 spread / 9 regional / 3 goods / 1 place; count lines 11 spread / 6 regional / 1 goods.

- On P alone (any share), city ties reach P 0.005 for 6 phrases, all Mohenjo-daro: 705-033 (70% against 57% expected), 690-740 (61% against 48%), 415-100 (68% against 45%), 415-100-740 (77% against 46%), 923-740, 142-617. 23 of 100 phrases fall under 0.05 on the city test (5 expected by chance), so a mild Mohenjo-daro lean is common; a strong tie is not.
- Mound tie: one phrase, 740-400 (Harappa F Trench I, 24% of area-known carriers, P 0.002).
- Mild building clustering that survives copies removal: 415-220 (8 shared against 3.4, P 0.016), 760-740 (P 0.029), 384-740 (block P 0.014). None reaches 0.005.
- Where a house signal does exist in this project (`MAP.md`: house-mates share an uncommon middle sign), it lives in rare name-slot signs, not in these frequent phrases.

## 3. Inter-city (`phrases_4_cities.py`, `intercity.csv`)

City counts over the 136 phrases: 1 city: 1; 2: 24; 3: 44; 4: 28; 5: 14; 6: 6; 7: 6; 8: 9; 9: 2; 10: 1; 11: 1. **39 phrases are in 5+ cities (36 of the top 100)**; the widest are 861-002 (11 cities), 760-740 (10), 817-002 and 820-002 (9 and 10), 100-740, 740-090, 705-033, 176-740, 032-220, 920-060, 590-390 (8 or more).

- **Exactly one city**: one phrase, 032-740-400 (19 carriers, all Harappa tablets). Harappa is a large site (1,921 objects), not a small one. A random draw of 19 objects with the same kind mix lands all in one city 8.4% of the time, and all in small sites 0.03% of the time. Mostly one city (90%+, 2+ cities): 845-407 (24 of 26 at Mohenjo-daro). Phrases whose carriers sit mostly (50%+) at small sites (under 100 objects): 0. So a local name is not what a fixed phrase is; small sites carry the city-wide phrases.
- **Overseas animal**: pooled over the 39 many-city phrases, 57 short-horned bull seals of 1,378 seal carriers against 57.7 expected from the same cities (P 0.61); phrases in fewer than 5 cities 43 against 41.5 (P 0.41). One by one the only one under 0.05 is 220-520 (5 of 39 against 1.7, P 0.019, one of 39 tests, not corrected). Spearman correlation of city count against short-horned share over 96 phrases: 0.25 against 0.15 in shuffles, P 0.082.
- **Seals found abroad**: 41 objects came from the Gulf, Mesopotamia, Iran or Central Asia; **6 carry any of the 136 phrases (15%), against 2,104 of 4,653 home objects (45%)**. The overseas objects mostly do not use the home phrases. Phrases on them: 590-390 and 590-390-740 (2 each), 002-004 (2 of 22 carriers, P 0.016 against the 0.88% base rate), 455-220, 002-004-390, 003-220, 004-390, 002-235, 760-740 (1 each). Reads with `MAP.md`: abroad seals write something else.

## 4. Phrase families and paradigms (`phrases_5_families.py`, `families.csv`, `family_members.csv`, `variants.csv`, `series_values.csv`)

A **family** = a frame with one sign blanked (920-060-* , *-740) filled by 2+ phrases of the same length (passing phrases, plus runs of 3+ texts, order 80%+, lift 5+). **118 families**. A **paradigm** = a family whose members behave alike (the class of the sign on the slot's side of the phrase, cosine at or above the 75th percentile of random pairs of passing phrases of the same length and slot type; control 20,000 pairs): 15 paradigms. A **numbered series** = a family where 2+ filler signs are number signs making at least half its texts: 6. Predicted 20 to 60 families; got 118.

Main families (fillers with distinct-text counts; all in `families.csv`):

| frame | fillers | reading of the slot |
|---|---|---|
| *-740 | 760 (95), 100 (84), 176 (65), 690 (39), 923 (29), 585 (26), 904 (24), 752 (19) ... 31 members, 524 texts | end family: mixed first signs (21 name-part signs, 4 after-measure), not alike (cosine 0.38 against 0.65 bar): the jar closes many unrelated names, not a paradigm |
| *-002 | diamond 861 (145), diamond variant 817 (123), wheel 820 (90), then 824, 297, 365, 880 | **front-word series**: three front words before the same two strokes |
| 740-* | comb 400 (114), man 090 (84), X-with-table 679 (10), closed X 565 (7) | after-jar titles; paradigm (cosine 0.99 against 0.61) |
| 920-060-* | jar with mark 741 (36), jar variant 742 (9), jar variant 745 (3) | **ward variants**, 48 texts |
| *-220 | two tall 032 (64), pitchfork 415 (52), three strokes 003 (16), six stacked 016 (13), 455 (11) ... | **number + fish**: 4 number fillers make 55% of the texts (P 0.007 against random signs); numbered series |
| 002-*-220 | 032 (27), 016 (4), 003 (3) (+ 240, 415) | number + fish after a front slot; numbered series (number fillers 81%) |
| *-390, 002-*-390, *-405, *-407 | 004 (18), 003 (15), 016 (8), 005 (6) before the tree | **number + tree**; 002-*-390 is a numbered series (4 number fillers, 70%, P 0.00008) |
| *-806 | A-with-comb 467 (8), 468 (7), 472 (4) | **numbered series, paradigm** (cosine 0.74 against 0.65): the comb count before leaf-on-tree |
| 171-* | 035 (12), 032 (5) | measure + tall number; numbered series |
| 480-* | 001 (9), 031 (5) | numbered series (one stroke, one tall stroke) |
| *-705 | 233 (18), 235 (11), 231 (7) | three fish variants before the U-with-stroke: paradigm |
| 590-*-740 | tree 390 (39), 405 (16), 407 (6) | three tree variants between box-with-bar and jar: paradigm |
| 590-390-* | jar 740 (39), porter 151 (5) | closer slot |
| 255-* | stroke-with-diagonal 435 (42), 070 (7), 436 (4) | paradigm |
| *-002-032 / -240 / -235 / -803 / -031 / -233 / -798 | 861, 817, 820 in the same slot before 002 and the same following sign | the front-word series again: each of these frames holds the three front words, cosine 0.95 to 0.99 against 0.69 |
| 100-740-* | man 090 (12), comb 400 (7) | after-jar title after the three-headed person |
| 002-004-* | 390 (8), 407 (3) | counted thing |
| 705-* / 706 | 033 (77) / 255 (7) | |
| *-033 | 705 (77), 706 (35), 711 (5) | two measure variants before the three tall strokes |

**Which are numbered series, by the counted sign's own number mix** (`series_values.csv`): the slot before fish (tall two, three, six), before trees (four, three, six, five), before leaf-on-tree (the comb-A signs), before cup (tall strokes). In each, the varying signs are count signs of the series named: they are number-class signs in frame v2, and the mix of which number appears differs from the general number mix at P 0.0002 to 0.045. The star numbers use only 2, 3, 6 (and 455) with 1, 4, 5 nearly absent (3, 5, 3 cases against 64, 16, 13), the tree numbers favour 4 and 3.

**Do the members of a paradigm differ in where, on what and when they appear?** (chi-square of member by city, object kind, bin, animal; member labels shuffled among carriers, 5,000 shuffles; `variants.csv`):
- ward variants 741 / 742 / 745: no difference on any (city P 0.84, kind 0.47, bin 0.72, animal 0.50). Free variants of one heading. (Their next-class cosine is 0.817, a hair under the 0.836 bar, so the rule does not label them a paradigm.)
- front words 861 / 817 / 820 before 002: no difference by city (P 0.79), kind (0.24), bin (0.15); animal 0.085. Interchangeable in distribution.
- after-jar titles 740-400 / 740-090 / 679 / 565: **differ on everything**: city chi-square 147.7 against shuffle mean 14.9, kind 188.7 against 12.0, bin 48.1 against 9.0, animal 123.6 against 6.0 (all P 0.0002). Comb = Harappa tablets with no animal; man = seals and tablets in 9 cities.
- measure variants 705 / 706 before 033: differ by object kind only (706-033 on 0 tablets of 45, 11 of 45 on copper tablets; P 0.027), not by city, bin or animal.
- tree signs in 590-*-740: differ by animal (390 on unicorn seals, 405 mostly on animal-free objects, 407 on none; chi-square 42.9 against 4.1, P 0.0002), not by city, kind or bin.
- A-comb 467 / 468 / 472 and star numbers 032 / 003 / 016: no difference (A-comb by bin P 0.024, one of many tests).
Two kinds of paradigm: free variants (wards, front words, star numbers, measure variants by city) and sorted variants (comb against man; tree signs by animal).

## 5. The front formula 920-060-741 (`phrases_6_office.py`, `office_920_060_741.csv`)

38 objects in 7 cities (Mohenjo-daro 24, Harappa 6, Dholavira 2, Lothal 2, Rakhigarhi 2, Chanhu-daro 1, Kalibangan 1); 29 seals, 6 tablets, 3 tags; bins early 5, middle 14, late 6, undated 13. 34 distinct texts.

**Verdict: many different texts under one shared heading, plus one repeated sub-line.** Control for each number: random draws of 38 objects from the carriers of the commoner front formulas 861-002 (172 objects) and 820-002 (100), 5,000 draws.
- **What follows the heading is of several kinds.** A name part or crest follows on 17 + 6 objects (23 of 37 with something after it), a number (a count line) on 8 (22%), a slot or title sign on 3, the text ends on 1. Draws from 861-002 give a number-first share of 25% (P 0.71 that a draw is at least as high as the real 22%) and from 820-002 27% (P 0.84). The heading takes a count line as often as an ordinary front word does.
- **Who follows is different each time.** Distinct rests of text: 94.6% of objects against 96.2% (861-002 draws, P 0.39) and 94.9% (820-002, P 0.52). Distinct first signs after the heading: 69.4% against 66.3% and 71.8% (P 0.68, 0.35). Pairs of carriers sharing their first sign after the heading: 13 against 18.5 and 16.8 expected (P 0.84, 0.71). So holders are no more repeated than under any other front word.
- **One sub-line repeats**: the line 350-504 follows the heading on 3 objects (Harappa H-2127 and H-2128, Mohenjo-daro M-1757, in two cities and two periods; 4 objects in the whole catalogue carry 350-504, 3 with this heading). `history.md` found the same tablet text in Period 3B and 3C. This is the one case of one office line with the same words under different holders; it is 3 of 38.
- **Where in each city**: Mohenjo-daro's 24 objects span 10 areas (DKG south 8, DK 4, VSA 3, DKG north 2, DKE 2, HR 1, LC 1, DKC 1, DKB 1, DKG 1); the 22 with a house number give 22 different buildings: shared-building carriers 0 against 0.98 expected by chance. Top area share 39% (DKG), P 0.81. It is not a one-house formula, and not a one-mound formula. Against the whole catalogue it leans mildly to Mohenjo-daro (63% against 57% expected, P 0.019).
- **On what**: 24% non-seal against 39% expected at the same cities (P 0.99 that draws are this high or higher): leans to seals, as the goods flag was not met.
- **With which animal**: 22 of 29 seal carriers are unicorn seals, 76% against 56% of all seals (binomial P 0.021); one short-horned bull seal (M-247), none of the other fixed groups. Stand letters: J 7, S 5, W 3, L 2, I 1, none shown on 20 objects.
- **Fish crest after it**: 7 of 34 names start (number strokes skipped) with a fish sign, against 12.7% of seals (P 0.13): no excess.
Three slot fillers after 920-060: 741 on 38 objects, 742 on 9, 745 on 3, 740 on 2 (shared by wards of free variation, section 4).
Reading of the two sides, stated before the numbers: one office held by many predicts names almost always after the heading, alike in shape, and holders that recur; many offices under one heading predicts several kinds of text after it and holders that rarely repeat. The numbers fall on the second side: a heading shared by many different people and records, behaving like a front word, with 350-504 as the one line that recurs.

## 6. What went against, and the redesigns

- **HOUSE phrases: none.** Predicted 3 to 15 mostly names; 3 on the raw test, 0 with copies removed. Redesign one: pool across all 100 phrases and remove copies (Z -0.33). New idea: the rarer phrases (4 to 7 texts), where a house phrase should sit: 74 testable, 5 against 5.6 expected. Paused: fixed phrases are not house-bound. The house signal of `MAP.md` belongs to rare signs in the middle of names.
- **The OFFICE flag does not separate real phrases from random objects** (random sets meet it 76 to 83% of the time). It stays only as "city-wide, no tie". Redesign two (a spread test: fewer shared buildings than chance, one holder per house): 0 phrases of the 13 with enough power. The only office-like signature found is structural (920-060-741: many holders under one heading, plus 350-504).
- **One-city and small-site phrases hardly exist** (1 one-city phrase, in a large city; 0 phrases mostly at small sites). Predicted that one-city phrases would be local names at small sites: against.
- **Many-city phrases and the overseas bull**: no link (P 0.61 pooled; Spearman P 0.082). Abroad objects mostly lack the home phrases (6 of 41 against 45%).
- **Families predicted at 20 to 60; found 118**; the numbered-series prediction (3 or more) held (6). The ward variants miss the behave-alike bar by 0.019 of cosine.
- **GOODS test**: the kind-matched random sets (circular) get the goods flag 5.4% of the time; the any-object sets 0.0%. The 6 goods phrases rest on the any-object control. A first version of the number-sign test let fish signs in (they follow numbers); the table uses only the number class.
- **New-text confirmation**: 20 of 99 testable phrases not confirmed, 37 untestable (the first catalogue's lift predicts under 2). The numbering mismatch for sign 817 hides 817-002 from the new texts.
- Not run: nothing used a Colab machine; all runs fit on the local machine.

## 7. What it opens

- 740-400 as a Harappa tablet ending (213 of 245 carriers at Harappa, tablets, no animal) is the first phrase with a clear object-kind and place profile: a Harappa tablet record formula. The name part before it (50% name part) is the next thing to list.
- Two counting series are now separated by sign height and by counted thing: tall strokes count fish (stars) and cups, short strokes count trees. The A-comb counts before leaf-on-tree are a third.
- The three front words 861 / 817 / 820 are interchangeable in where they are found; a test of what separates them (what follows, name type) is the way into whether they are three words or one front slot with variant spellings. The same test fits the ward variants 741 / 742 / 745.
- 350-504 after 920-060-741: the one repeated record line; find its other holders in the second catalogue.
- The 277 rarer phrases are the candidates for names that travel as a unit within a family; they have not been atlased.

Files: `work_data/phrases/atlas.csv`, `atlas_all.csv`, `phrase_list.csv`, `phrase_shuffle_control.csv`, `carriers.csv`, `kinds.csv`, `kinds_all.csv`, `kinds_control.csv`, `kinds_pooled.csv`, `intercity.csv`, `intercity_abroad.csv`, `families.csv`, `family_members.csv`, `count_likeness.csv`, `variants.csv`, `series_values.csv`, `office_920_060_741.csv`, `minor_phrases.csv`, `minor_control.csv`, `time_trends.csv`, logs `log_1.txt` to `log_8.txt`.
