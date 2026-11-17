# The ladder of Indus grain measures

Scripts (in `work_scripts/`, run in this order; each has its predictions written in its top docstring before it was first run): `measures_common.py` (loader: number runs, the unit list), `measures_1_ceilings.py` (every count beside every measure sign), `measures_2_order.py` (order of units on a line; run once plain and once with `distinct`), `measures_3_sums.py` (do the numbers on one object add up), `measures_3b_rescue.py` (rescue tests for the sums), `measures_4_scale.py` (litres, pay scale, why never 5 cups), `measures_5_rank.py` (rescue for the pay-scale order). Tables: `work_data/measures/` (`unit_counts.csv` every count beside a unit, `ceilings.csv`, `order_pairs.csv`, `order_pairs_distinct.csv`, `sum_hits.csv`, `multi_number_objects.csv`, `batch_totals.csv`, `pay_scale.csv`).

Plain words used below:
- **Unit / measure sign**: a sign read as a measure word: cup 700, *kalam* 705/706 (the big grain measure), *kōṭṭai* 575 (great grain measure), *paṭi* 320 (daily ration measure), *kāl* 061 (quarter), *paṟai* 540, *niṟai* 171 ("full", a weight word), pot 711, bin 335, granary bin 605, chest 590, dozen 055, seven-string 048, hand 817/861.
- **Count / number run**: one or more stroke signs side by side; the value is their sum (scribes write 5 as 3+2, `033 032`).
- **Tall strokes** = the container counting series; **short strokes** = the series for people, living things, produce.
- **Ceiling**: the largest count a unit ever takes. In a real measure system the count of a small unit stops just below the number that makes one of the next unit up.
- **Two catalogues**: Lipi (first catalogue, 5,679 faces) and the 1,183 "new texts" of the second catalogue (Mahadevan 1977) with no partner in the first.
- **P** = how often chance alone gives a result at least this strong. Small P points to the reading being right.
- **Tamil ladder** (looked up today in the Tamil Lexicon at dsal.uchicago.edu and the local DEDR, Burrow and Emeneau's Dravidian Etymological Dictionary): 1 *ceviṭu* = 1/5 *ār̤ākku* (ollock); 8 ollock = 1 *paṭi* / *nāḻi* (DEDR 3849, 397; TL); *uḻakku* = 2 ollock = 1/4 *paṭi* (DEDR 681); *uri* = 1/2 *paṭi* (TL p. 441); 8 *paṭi* = 1 *marakkāl* = 1 *kuṟuṇi* (TL p. 3082, p. 1054); 2 *kuṟuṇi* = 1 *patakku* (TL); 4 *marakkāl* = 1 *tūṇi* (TL); 12 *marakkāl* = 1 *kalam* (TL p. 3082); *kōṭṭai* = 21 *marakkāl* (DEDR 2208; TL); *karacai* = 400 *marakkāl* (DEDR 1261). *Paṭi* is also "a fixed daily allowance for food" and *paṭiy-āḷ* "a servant paid in grain" (DEDR 3849).

## 1. What was found

1. **The cup is the *marakkāl* and twelve cups make a *kalam*. Cup counts are the whole shares of a twelve.** Every cup count in both catalogues: 1 (11), 2 (127), 3 (193), 4 (145), 6 (3), 5 (1), 7 (1). The counts that divide 12 are 479 of 481 (99.6%). The one "5" is the ivory rod H-2570 `001 034 700`, the one "7" is the broken tablet H-1963 `000 017 700 400` (stacked seven, the "Seven" formula). Six is written three times while five is written at most once; any smooth run of counts from a 2-3-4 hump puts more fives than sixes. This is the fingerprint: 1, 2, 3, 4, 6 cups are 1/12, 1/6, 1/4, 1/3, 1/2 of a *kalam*, and in Tamil 2 cups is a *patakku*, 4 cups a *tūṇi*. It points to the twelve-based Tamil ladder and away from the weight ladder (section 2).
2. **Units are written big before small, like every deciphered account script.** Lines that hold two or more measure signs keep their pair's usual order in 124 of 146 meetings on distinct texts (85%) against 69% when the unit signs are shuffled inside each line (P 0.002; with copies counted 89% against 62%). The order alone gives the ladder: grain header 413 > *kōṭṭai* 575 > *kalam* 705/706 > chest, bin, *kāl* > pot 711 > cup 700. Tamil sizes predict the same order: bigger first in 27 of 37 Tamil-ranked meetings on distinct texts (P 0.008). The order ladder and the ceiling ladder agree.
3. **The quarter *kāl* 061 never counts four.** Owned counts before it are 1, 2 and 3; none at 4 or above (the one 8 is the opener `861 002` plus a stacked six). Three quarters is the most a quarter can count before it makes a whole.
4. **The *kalam* tops out at five.** Counts after 705/706: 3 (159 of 187), 5 (written `033 032` or tall 5: 11, plus `005 706` on three copper tablets), 4 (`033 031`, `033 001`), 1. Nothing above 5 that belongs to the *kalam* (the 10s are `033 017 585`, "three *kalam*" followed by the "Seven" formula). The rung above the *kalam* is at least 6 *kalam*.
5. **One *paṭi* a day for a month is the cup band.** 1 *paṭi* = 1/8 cup = 1.16 L; thirty days = 3.75 cups = 34.6 L = 0.87 to 0.92 kg of grain a day. The tablets issue 3 or 4 cups (193 and 145 of 481 counts). The cup count on a ration chit is one person's month of daily *paṭi*. The bondsman (097) gets 4 cups on all 7 objects that give him an amount; the cultivator (137) gets 3 or 4 (H-1858, H-1859, H-976, H-702: 3; H-2105, H-215, H-2102: 4).
6. **Three *kalam* a year is one person's grain.** 3 *kalam* = 36 cups = 332.6 L = 0.68 to 0.73 kg a day for 365 days, inside the 0.5 to 1 kg a person eats. The "three-*kalam* chief" (705-033-520, 45 of the 83 three-*kalam* seals) is named by a one-man yearly grain allowance. On the 3-*kalam* chit `240 705 033 550 525 400 | 413 575 335 711 033 700` the monthly issue is 3 cups: 3 cups x 12 months = 3 *kalam*.
7. **Numbers on account objects repeat each other more than chance.** On account objects (tablets, copper tablets, tags, pots) carrying exactly two numbers, the two are equal on 67 of 190 against 52.2 shuffled (P 0.006). The commonest equal pair is "3 *kalam* | 3 cups" (5 objects).
8. **Wells' measured pots sit on the ladder.** The six-stroke pot (55.56 L) is half a *kalam* (6 cups = 55.4 L); the three-stroke pot (27.30 L) a quarter *kalam*.

What it opens: every count beside a measure sign can now be turned into litres and person-days, the ration chits read as monthly issues, and the *kalam* grades on seals read as yearly allowances.

## 2. Step 1: ceilings

Predictions in `measures_1_ceilings.py`: Tamil ladder T1 cups never reach 12, and only 1, 2, 3, 4, 6 if they are shares of a *kalam*; T2 *paṭi* never reaches 8; T3 *kāl* never reaches 4; T4 *kalam* not capped low. Weight ladder W1 container counts on 1, 2, 4, 8 for 80%+; W2 five as common as six.

Every count touching a unit sign: 1,382 places in Lipi, 176 in the new texts (`ceilings.csv`; raw adjacency, so a count between two signs is listed under both).

| unit | sign | count side | n | values (count:times) | ceiling | series | lives |
|---|---|---|---|---|---|---|---|
| cup | 700 (703) | before | 397 | 1:4 2:102 3:157 4:129 5:1 6:3 7:1 | 4 (6 rare; 5, 7 one each, both explained above) | tall 96% | tablets 378, Harappa 379 |
| cup | 700 | after | 84 | 1:7 2:25 3:36 4:16 | 4 | tall | tablets 68 |
| *kalam* | 705/706 | after | 187 | 1:3 2:4 3:159 4:3 5:11 6:1 10:4 | 5 (the 10s are 3 + the "Seven" formula; the 6 is a tree count) | tall 94% | seals 118, copper tablets 35 |
| *kalam* | 705/706 | before | 33 | mostly 2 from the opener `861 002` | - | short | seals |
| *kōṭṭai* | 575 | before | 23 | 7:16 (stacked seven, the "Seven" formula) 9:2 | - | stacked | seals |
| *kōṭṭai* | 575 | after | 11 | 1:4 2:4 3:1 4:1 6:1 | 3 owned (1, 2, 1+2) | mixed | Lothal 4 |
| *kāl* | 061/062/063 | before | 32 | 1:5 2:21 3:5 8:1 | 3 (the 8 is opener + six) | short | seals |
| *niṟai* | 171 | after | 28 | 3:8 (always written 2+1) 5:20 | 5 | tall 100% | seals 15, tablets 10 |
| pot | 711 | after | 15 | 3:15 | 3 (the cup's three) | tall | Harappa tablets |
| jar | 740 | before | 126 | 2:59 7:22 5:9 3:8 | - | tall 58% | tablets, seals |
| chest | 590 | before | 51 | 1:5 2:27 3:13 4:4 7:2 | 4 | tall 67% | seals, tablets |
| hand | 817/861 | after / before | 405 / 38 | 2 opener / 3:29 | 3 on tablets | short 97% | |
| dozen | 055 | before | 31 | 1:20 2:6 | 2 | short | Lothal tags |
| *paṭi* | 320 | both | 3 | 1, 2, 2 | - | | |
| *paṟai* | 540 | both | 4 | 2 | - | | |

Tests:
- T1 came true: cup counts divide 12 in 479 of 481; maximum 6.
- T2 could not run: *paṭi* is counted three times in the whole corpus (1, 2, 2). Its own amount is carried by the cup instead (section 5).
- T3 came true: *kāl* 1, 2, 3, never 4.
- T4 came true: *kalam* takes 3, 4 and 5.
- W1 went against: 49% of container counts sit on 1, 2, 4, 8 (n 971), and 3 is the commonest value (402).
- W2 went against: five is written once with the cup, six three times.
- Tall strokes for containers: cup 96%, pot 100%, *kalam* 83% (94% on the count-after side), *niṟai* 97%; the hand 3%. *Kōṭṭai* 18% because its "before" count is the stacked "Seven" formula.

The data fit the twelve-based ladder. The binary weight ladder (1, 2, 4, 8, 16, 32, 64, then 160, 200, 320, 640) does not describe the capacity counts: weights double, grain measures go by twelfths.

## 3. Step 2: order of units on a line

Predictions in `measures_2_order.py` (O1 bigger first in 80%+ of Tamil-ranked meetings; O2 pairs keep one order in 80%+; O3 the order ladder matches the Tamil sizes). Full table `order_pairs_distinct.csv`.

| pair (distinct texts) | first | second | n | usual order |
|---|---|---|---|---|
| grain 413 / *kōṭṭai* | 10 | 1 | 11 | grain first (P 0.012) |
| *kōṭṭai* / bin 335 | 8 | 0 | 8 | *kōṭṭai* first (P 0.008) |
| grain / bin | 8 | 0 | 8 | grain first |
| *kōṭṭai* / *kalam* | 6 | 3 | 9 | *kōṭṭai* first |
| *kalam* / *kāl* | 7 | 1 | 8 | *kalam* first (P 0.07) |
| bin / pot 711 | 5 | 0 | 5 | bin first |
| *kōṭṭai* / pot | 5 | 0 | 5 | |
| cup / *kāl* | 4 | 1 | 5 | cup first |
| pot / cup | 3 | 0 | 3 | pot first |
| *kalam* / *paṭi* | 3 | 0 | 3 | *kalam* first |
| *kōṭṭai* / cup | 3 | 1 | 4 | |
| *kalam* / chest 590 | 16 | 8 | 24 | *kalam* first (P 0.15) |

- O2: 14 of 21 pairs that meet 3+ times keep one order 80%+ (with copies 15 of 21).
- Kept share overall: 85% against 69.4% +- 2.5% under shuffling, P 0.002 (95 lines with 2+ different units). With copies: 89% against 62%.
- O1: bigger first in 27 of 37 Tamil-ranked meetings (73%, P 0.008); with copies 37 of 47 (79%, P 1e-4). Just under the 80% written.
- O3, the ladder from order alone: grain header (+0.80) > *kōṭṭai* (+0.27) > *kalam* (+0.20) > dozen (+0.14) > *paṟai* (0) > *paṭi* (-0.20), *niṟai* (-0.20) > chest (-0.31) > granary bin, cup, bin, *kāl* (-0.33 to -0.36) > pot (-0.67). Big containers and big measures first, cup and pot last. Tamil order *kōṭṭai* > *kalam* > cup > *kāl* matches the four signs that the Tamil ladder sizes.
- The standard grain line `413 575 335 711 033 700` (15 faces) is one line written strictly big to small: grain, *kōṭṭai*, bin, pot, 3 cups.
- Jar 740 comes after every unit (chest 143 to 4, *kalam* 115 to 2, *kāl* 66 to 12): it closes the line as "house of", outside the ladder. The hand opener comes before every unit (*kalam* 30 to 3).

## 4. Step 3: sums

Predictions in `measures_3_sums.py`: S1 a total line (one number = sum of the others) more than shuffled; S2 converted sums in cup units; S3 the 4 cups of the crew chit is a per-crew issue; S4 products.

- S1 went against: on 70 objects with 3 or more numbers, one is the sum of the rest on 10, against 14.9 when numbers are shuffled between objects (P 0.95). The ten (`sum_hits.csv`) are mostly seals where the numbers are parts of names.
- S2 went against: 15 objects mix ladder units; converted to cups none gives a total (`3 kalam | 3 cups` = 36 and 3; `2 kōṭṭai, 4 kalam` on M1026 = 42 and 48).
- S4 went against: 0 products against 4.1 shuffled.

Rescue 1 (better test, `measures_3b_rescue.py` R1): Indus accounts are one-line chits, not ledgers with total lines, so look for repetition instead of addition, on account objects only. Two-number account objects: the two numbers are equal on 67 of 190 against 52.2 shuffled (P 0.006). Equal pairs: 3 *kalam* | 3 cups x5, 2 cups | 2 jars x4, 3 two-leaf | 3 cups x3, 2 sitting-men | 2 cups x2, 2 cups | 2 quarters x2. On account objects with 3+ numbers (36), one sum relation.

Rescue 2 (new idea, R2): batches of chits sharing one front with different cup counts should total whole *kalam*. 16 batches; totals 89, 83, 16, 14, 16, 16, 8, 8, 9, 6, 7, 7, 9, 11, 11, 9; multiples of 12: 0 of 16 (chance 1.3). Went against: the cup issues of one office are not drawn so as to empty whole *kalam*.

Crew arithmetic (`measures_4_scale.py` P2): 35 tablets carry a cup count and a person count. Person count x cups = 12 on 21 (the one batch: 3 hands x 4 cups). All products: 12 (21 tablets), 6 (3 cups x 2 women H-1287; 3 cups x 2 cultivators H-702, H-706; 2 cups x 3 carriers H-1902, H-2139), 8 (4 cups x the opener "2 shares" `416 861 002`, 4 tablets), 4 (4 x 1; 2 x 2), 9 (H-2238, 3 x 3), 3. Products that make a whole or half *kalam*: 26 of 35 tablets, 4 of 8 different combinations. Read: a crew chit issues one *kalam* to a crew of three, 4 cups each (the old reading "4 cups for the crew" becomes "4 cups a head"; both stay alive).

The working sums, with the arithmetic:
- H-2218 to H-2239 (21 tablets): 3 hands x 4 cups = 12 cups = 1 *kalam* = 110.9 L.
- H-1287, H-702, H-706, H-1902, H-2139: 2 x 3 = 3 x 2 = 6 cups = half a *kalam* = 55.4 L (the size of Wells' six-stroke pot, 55.56 L).
- H-774, H-1811, H-1812, H-1813 (4 objects; with H-369 5): 3 *kalam* a year = 36 cups = 12 months x 3 cups; the chit's cup line is 3.

## 5. Step 4: litres

Anchor: Wells' three measured inscribed pots, three long strokes 27.30 L, six 55.56 L, seven 65.89 L, so 9.10 / 9.26 / 9.41 L a stroke, 9.24 L on average ([varnam.org summary](https://www.varnam.org/2009/12/03/the-harappan-volumetric-system/); the [History News Network report](https://www.historynewsnetwork.org/article/120459) gives the 3:6:7 ratio and ties the marks to the tablets). One cup = 9.24 L.

| rung | sign | in cups | litres | grain (kg, at 0.75-0.80 kg/L) | evidence |
|---|---|---|---|---|---|
| *uḻakku* (quarter *paṭi*) | - | 1/32 | 0.29 | 0.22-0.23 | Tamil only |
| *paṭi* (day's ration) | 320 | 1/8 | 1.16 | 0.87-0.92 | Tamil; 320-920 "monthly allowance" |
| *kāl* (quarter, of the next unit) | 061 | 1/4 of its unit | - | - | counts 1-3, never 4 |
| cup = *marakkāl* / *kuṟuṇi* | 700 | 1 | 9.24 | 6.9-7.4 | Wells' pots; counts divide 12 |
| *patakku* | `032 700` | 2 | 18.5 | 13.9-14.8 | 127 counts |
| quarter *kalam* | `033 700` | 3 | 27.7 | 20.8-22.2 | 193 counts; Wells' 3-stroke pot 27.30 L |
| *tūṇi* | `034 700` | 4 | 37.0 | 27.7-29.6 | 145 counts; crew and bondsman chits |
| half *kalam* | `036 700` | 6 | 55.4 | 41.6-44.4 | 3 counts; Wells' 6-stroke pot 55.56 L |
| *kalam* | 705/706 | 12 | 110.9 | 83-89 | counted 1, 3, 4, 5 |
| 3 *kalam* | `705 033` | 36 | 332.6 | 249-266 | the grade on 83 seals |
| 5 *kalam* | `005 706`, `705 033 032` | 60 | 554.4 | 416-444 | copper tablets, 4 big seals |
| *kōṭṭai* | 575 | 21 by the Tamil Lexicon | 194 | 146-155 | Tamil only; Indus *kalam* ceiling of 5 says the rung above is 6+ *kalam* |

Wells' seven-stroke pot (65.89 L) is 7 cups: a pot marked with its own capacity, not a named rung. The pot capacities 3 and 6 are the quarter and half *kalam*.

Searched for other measured vessels (broad queries on Indus vessel capacities, ration bowls, Lothal measures): nothing beyond Wells' three pots came back with litres. The catalogue's size columns for pots (78 rows with a width) give the size of the inscribed sherd or graffito, not the pot's volume, so they cannot test litres.

## 6. Step 5: the pay scale

Grain at 0.75-0.80 kg a litre; a person eats about 0.5-1 kg of grain a day. `pay_scale.csv`.

| who (text) | amount as written | cups a month | litres a month | kg a day for one person |
|---|---|---|---|---|
| the three-*kalam* chief `705 033 520` (45 seals; 83 three-*kalam* seals) | 3 *kalam* a year | 3 | 27.7 | 0.68-0.73 |
| three-*kalam* holder's chit `240 705 033 550 525 400 \| 413 575 335 711 033 700` (H-774, H-1811, H-1812, H-1813) | 3 *kalam*; 3 cups | 3 | 27.7 | 0.69-0.74 |
| crescent-horn house `706 033 923 740` (7 copper tablets) | 3 *kalam* a year | 3 | 27.7 | 0.68-0.73 |
| five *kalam* `005 706` (M-513, M-514, M-515), `705 033 032` (3 new-text copper tablets), 4 seals | 5 *kalam* a year | 5 | 46.2 | 1.14-1.22 |
| bondsman, junior hand `004 700 097 400` (M-478, M-479, M-480, M-1425; also H-1917, H-1860, M-2104) | 4 cups | 4 | 37.0 | 0.92-0.99 |
| cultivator `137 400` with a cup face (H-1858, H-1859, H-976, H-702: 3; H-2105, H-215, H-2102: 4) | 3 or 4 cups | 3.4 average | 31.7 | 0.79-0.85 |
| crew chit: 3 hands, 3 loads, 4 cups (21 tablets) | 4 cups a head, 1 *kalam* for the crew | 4 a head | 37.0 | 0.92-0.99 |
| crew chit H-2238: 3 hands, 3 loads, 3 cups | 3 cups | 3 | 27.7 | 0.69-0.74 |
| six-cup issue with a *niṟai* line (H-801 `036 700 \| 171 035 415`, H-1881 `036 700 \| 171 033 700 415`) | 6 cups | 6 | 55.4 | 1.39-1.48 (two people: 0.69-0.74 each) |
| monthly allowance `320 920` (one *paṭi* a day) | 30 *paṭi* | 3.75 | 34.6 | 0.87-0.92 |

The monthly allowance is a sensible month for one person: 30 *paṭi* = 34.6 L = 26 to 28 kg of grain. Every issue on the chits, 3 to 4 cups, is one adult's month. Six cups is two adults' month (or a household of a working man and a dependant). Three *kalam* a year is one adult for a year at 0.7 kg a day.

The order of amounts against rank went against: the bondsman's 4 cups a month is above the three-*kalam* chief's 3 cups a month (36 cups a year) and level with or above the cultivator's 3 to 4. Rations do not rise with rank.

Rescue (`measures_5_rank.py`, prediction written first: rank lives in the *kalam* count, not in the monthly cups): seals naming 5 *kalam* are bigger than seals naming 3 *kalam*, which are bigger than seals in general. Median face: 5 *kalam* 1,127 mm2 (n 4: M-10 2,333; M-677 1,243; M-1155 1,011; M-355 827, all four above the 3-*kalam* median, about P 0.06), 3 *kalam* 785 mm2 (n 76), all seals 605. After the count the 3-*kalam* seals take the chief 520 (45 of 83); the 5-*kalam* seals take something else (070 twice, 877, 335). Read: the monthly cup chit is subsistence for whoever works (heavier work, more grain: the bondsman's full *tūṇi*); rank is written in *kalam* a year on the seal, and only the holders at 3 *kalam* (one man's ration) and 5 *kalam* appear. The 5-*kalam* seals are also longer (median 11 signs against 6), which by itself makes a seal bigger; the size test does not separate the two.

## 7. Step 6: why cups are never 5

The ladder's reason: a cup count on a chit is a share of a *kalam* (12 cups) that comes out whole. Twelve splits into 12, 6, 4, 3, 2 and 1 cups; it does not split into fives, so "5 cups" is never written, and neither are 7 to 11. The crew chits show the split happening: 3 hands x 4 cups = 12; 2 x 3 = 3 x 2 = 6 (section 4).

Test (prediction P5, written first: counts dividing 12 are 98%+): 479 of 481 cup counts divide 12 (99.6%). The rival, an eight-cup next unit (binary, from the stone weights), allows 1 to 7 and predicts fives and sevens at the rate of threes and sixes: fives 1, sevens 1 against threes 193, sixes 3.

The five that people needed lives elsewhere: *niṟai* 171 takes tall 5 in 20 of 28 counts (and 3, always written 2+1, in 8); five *kalam* is written `033 032` or `005 706`. A yearly 5 *kalam* would be 5 cups a month, which is never written: a 5-*kalam* holder is not paid by monthly cup chits.

## 8. What went against, and the rescues

- Weight ladder for capacities: 49% of container counts on 1, 2, 4, 8 (80% predicted); five nearly absent. Not rescued: weights and grain measures are two systems.
- Total lines (S1, S2, S4): sums 10 of 70 against 14.9 shuffled; converted sums 0 of 15; products 0 against 4.1. Rescue R1 came true (equal numbers 67 against 52.2, P 0.006); rescue R2 went against (0 of 16 batch totals in whole *kalam*). Indus accounts are single-entry chits; totals, if kept, were on something that did not survive.
- Pay order: bondsman 4 cups > three-*kalam* holder 3 cups a month. Rescue: rank is in the *kalam* count on seals (5-*kalam* seals 1,127 mm2 against 785, n 4, about P 0.06, confounded with length).
- *Kalam* number = monthly cups (P1, a guess built in this job): 5 of 8 objects, 3 of 6 distinct texts (P 0.066 by objects). Two texts give 1 *kalam* with 3 cups (H-177 `817 002 031 706 151 033 700`, H-846 `705 031 100 740 400 | 033 700`), one gives 3 *kalam* with 2 cups (H-2139). Alive beside the rival that 3 cups is a fixed issue whatever the grade.
- *Paṭi* 320 is almost never counted (3 counts), so its 1/8-cup size rests on the Tamil Lexicon and the month arithmetic, not on an Indus ceiling.

## 9. Next tests this opens

1. The rung above the *kalam*: every line with *kōṭṭai* 575 and a *kalam* count (M1026 `032 575 032 002 705`: 2 *kōṭṭai*, 4 *kalam*) predicts *kalam* counts below the *kōṭṭai* ratio; collect all *kōṭṭai* counts after it (1, 2, 3 so far) and read the *kōṭṭai* as 6 or more *kalam*.
2. *Niṟai* 171 with tall 5 heads the two 6-cup tablets: test whether *niṟai* 5 is "5 *kalam* full" (a yearly total) by looking for *niṟai* lines on objects with *kalam* counts.
3. Wells' pots: any further whole Harappan pot with tall strokes predicts a volume of strokes x 9.24 L; the six-stroke and three-stroke sizes should be the commonest jar capacities.
4. Crew chits: every tablet with a person count and a cup count predicts a product of 6 or 12.
