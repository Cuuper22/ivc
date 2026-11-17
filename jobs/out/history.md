# History: the Indus texts through time, and the open measure leads

Scripts (in `work_scripts/`, rerun with `python3`, each has its predictions in its top docstring, written before it was first run): `time_common.py` (the time axis), `time_1_trends.py` (what changes, against shuffles within area), `time_2_readings_people.py` (earliest and latest readings, recurring names), `time_3_redesign.py` (redesigned tests after the flat first pass), `time_4_checks.py` (does the axis see what the excavators saw; careers; houses city by city), `time_5_first_writing.py` (writing before and after the cities), `measures2_leads.py` and `measures2_rescue.py` (the five measure leads). Tables: `work_data/time/` (`time_axis.csv`, `trends.csv`, `houses.csv`, `house_site.csv`, `dkg_levels.csv`, `first_appearance.csv`, `contrast.csv`, `early_late_readings.csv`, `recurring_names.csv`, `log_1.txt` to `log_5.txt`) and `work_data/measures/m2_*.csv`, `m2_log.txt`.

Plain words used below:
- **Bin**: early = up to the end of Harappa Period 3B (before about 2200 BC); middle = Period 3B/C, 3C-1, 3C-2 and undivided 3C (about 2200 to 2050 BC); late = 3C-3, 3C-4, Period 4 and 5 (about 2050 BC and after). Period dates from [harappa.com's chronology](https://www.harappa.com/beas/chronology): 3A ca. 2600-2450, 3B ca. 2450-2200, 3C ca. 2200-1900, Period 4 ca. 1900-1800, Period 5 after 1800.
- **Shuffle within area**: the bin labels are mixed only among objects from the same site and the same excavation area, many thousand times. P = the share of shuffles that show a trend at least as strong as the real one. A small P means time itself, not which area was dug, goes with the feature. **r** = the trend (positive = more common later).
- **Agent** = a seal ending `X jar man`, "X's man". **Fish crest** = a marked fish sign (231, 233, 235, 240, 236) first in the name, the sign of the great "star" houses. **House** (in the houses table) = the first sign of a name of two or more signs, the family element.
- **Office opening** = the three-sign start `920-060-741` (in seven cities). **Boxed-cotton** = the pair `590-390`, the trading house in nine cities.

## 1. What was found

1. **The written system was fixed from the earliest city levels to the end, and did not drift.** Across about six centuries (Harappa Period 3B to Period 4/5), measured against shuffles within area, nothing in the formula moves: agents 4.5% / 4.1% / 4.5% of seals with an ending (early / middle / late, P 1.0); fish-crest names 12.3% / 12.6% / 12.8% (P 0.89); the jar ending 74.8% / 66.4% / 68.8% (P 0.58); spear 12.6 / 12.9 / 13.1%; office opening 1.4% / 0.9% / 0.8% of all objects (P 0.45); Boxed-cotton 1.9% / 1.6% / 1.6% (P 0.87); seal text length 4.4 / 4.2 / 4.3 signs (P 0.99); star names (number + fish) 10.5 / 9.8 / 10.6% (P 0.78); a marked fish written as two signs 18.6 / 15.8 / 13.9% of fish spellings (P 0.35). In the one long dug sequence, Mackay's seven levels in DK-G at Mohenjo-daro (from about 22 ft down to about 4 ft), the same holds level by level: agents rho +0.03 (P 0.57), office -0.03 (P 0.48), fish crest +0.04 (P 0.31). What it means: the opener-name-ending grammar, the agent title, the great fish houses, the seven-city office and the cotton house were all in place in the first dated city levels and were copied unchanged for the life of the cities, like a chancery's standard form. It points toward one reading key for the whole sequence: a reading tested on 3B texts holds on 3C texts with no correction. It opens: the text formula cannot date an object; the object's form can (finding 2).
2. **The time axis sees what the excavators saw, so the flat result is not a broken clock.** At Harappa the share of seals with no animal (inscription-only seals) rises from 14 of 99 up to Period 3B/C to 33 of 98 in 3C-3 and later (within-area P 0.0018; rho +0.20 against period rank, P 0.0004). The excavators, independently, say rectangular inscription-only seals [appear only in Period 3C](https://www.harappa.com/node/2997). At Mohenjo-daro the share stays flat (21.0 / 17.9 / 18.7%, P 0.70): the inscription-only seal is a Harappa fashion of 3C.
3. **The office and the cotton house were already in several cities in the earliest bin; neither spread out from one centre.** Office opening: earliest at Mohenjo-daro M-974 (Period 3B-2, Mackay's Early level) and Harappa H-2128 (Period 3B, the excavators' own date), then Harappa, Mohenjo-daro, Dholavira and Kalibangan in the middle bin. Boxed-cotton: Harappa H-533 (3B-2) and H-1692 (3B, excavators' date) and Mohenjo-daro M-851 (3B-2) in the earliest bin. One office record survives a period change: the identical tablet `220-142-590-455 | 920-060-741-350-504` is H-2128 (Period 3B) and H-2127 (Period 3C), and Mohenjo-daro M-1757 (3C-2) carries `920-060-741-240-350-504`. The office line `350-504` ran across the 2200 BC boundary in two cities. Read: an institution founded with the cities, not grown.
4. **Names are inherited, not personal.** A full name (same crest + personal part + tag) turns up in two or more time bins on 65 names, against 65.2 when bins are shuffled within area (12 in all three bins, against 11.9). Names recur through time exactly as if time did not matter: they belong to houses that lasted, not to men who lived a few decades. 39 of 49 recurring names keep the same ending in every bin (a lineage keeps its rank). 10 change; the cleanest rises are `235-240` (Bamboo-star High-star) "man of" early, then also spearman (chief) in the middle and late bins; `705-255` (Kalam-Chief) plain "house of" early, then also "X's man" from the middle bin; `798-415-220` "house of" through, then a spearman in the late bin (section 5).
5. **The late seal is bigger.** Median seal face 713 mm2 early, 676 middle, 767 late (within-area P 0.019); the large unicorn format (stand letter W) goes 37.0% / 43.4% / 46.6% of unicorn seals (P 0.12). This went against the prediction (smaller late), which was built on the inscription-only seals.
6. **The measures (Job 2).** The "full weight" word *niṟai* (171) takes only 3 and 5, 28 of 28 counts, all in tall strokes, never the 2 and 4 that make 58% of cup counts (P 6e-12 under the cup's own count mix): its counts are the decimal and the thirds steps of the Harappan weight system, not its binary steps. On multi-face tablets joined into one record, a number on one face repeats a number on another face on 52 of 138 distinct records against 41.0 shuffled (P 0.012; on all objects 82 of 179 against 59.3, P below 0.0003): a tablet states its amount twice, once per face. Details and the leads that went against are in section 6.

## 2. The time axis

Every object in the Lipi catalogue was given a bin by one of three rules (`time_common.py`, table `work_data/time/time_axis.csv`). Of 4,694 objects, 2,666 get a bin.

| rule | what it uses | how sure | objects (early / middle / late) |
|---|---|---|---|
| A excavator | Harappa 1986+ digs (HARP): the period the excavators gave (3A, 3B, 3B/C, 3C, 4, 5) | the surest: the diggers' own phasing | 141 / 470 / 7 |
| B layer-map | Harappa: Vats' strata I-VII (stratum I = top = latest) as the catalogue mapped them (VII = 3B-1/2; VI, V = 3B/C; IV = 3C-1; III = 3C-2; II = 3C-3; I = 3C-4/4). Mohenjo-daro: Mackay's levels in DK-G (Early I = 3B-2; Intermediate III, II, I = 3B/C, 3C-1, 3C-2; Late III, II, I = 3C-3 to Period 4). Kalibangan Early / Middle / Late of period 2. Dholavira stages placed by their own dates (I-II 2650-2500 = before the cities; III 2500-2200 = early; IV 2200-2000 = middle; V 2000-1900 = late; VI 1850-1750 = Period 4), from [Wikipedia's Dholavira page](https://en.wikipedia.org/wiki/Dholavira) | order inside one dig is sure (the levels follow depth: Mackay's DK-G medians run 22.6 ft Early to 3.2 ft Late I); the match of an old dig's level to a HARP period is the catalogue's | about 105 / 948 / 551 |
| C depth-band | Mohenjo-daro objects with a depth but no level (HR, VS, DK-A to E, SD, L): deepest third of their own area = early, middle third = middle, top third = late | weakest: relative inside one area only; raw depths are never compared across areas | 156 / 145 / 208 |

Two catalogue mappings were overridden after checking the sites' own sequences: Banawali "Period II" is the whole Mature Harappan at that site (c. 2300-1700 BC, [Wikipedia](https://en.wikipedia.org/wiki/Banawali)), not HARP Period 2, so Banawali is left undated; the catalogue put Dholavira stage IV at 3B-1, but the stage's own dates are 2200-2000 BC, so it is placed in the middle bin. Kanmer's periods could not be checked and are left undated.

Bins by object kind: seals 181 / 723 / 611, tablets 118 / 606 / 98 (copper tablets 7 / 23 / 21), pots 47 / 106 / 5. The middle bin dominates at Harappa (847 of 1,147 Harappa dated objects) because the big tablet trenches (E Trench 11, F Trench I) are 3B/C. The within-area shuffle cannot use an area dug in one period only; this is why the seven-level DK-G sequence was run on its own (redesign D1).

## 3. What changes and what does not (predictions first)

The predictions as written in `time_1_trends.py` before any number: H1 agents grow; H2 fish crests grow; H3 the office opening is absent early and starts at Mohenjo-daro; H4 Boxed-cotton peaks in the middle bin and spreads from one city; H5 the short-horned bull and the ship word peak in the middle bin (the Mesopotamian trade, about 2300-2000 BC); H6 unicorn stand W rises late; H7 texts get longer; H8 seals smaller and more inscription-only late; H9 jar+man and spear rise, the 3-kalam chief rises; H10 cotton rises, copper and ivory late; H11 star names rise; H12 the two-sign fish spelling is early.

| feature (within-area shuffle) | early | middle | late | r | P | prediction |
|---|---|---|---|---|---|---|
| agents, jar + man (seals with an ending) | 4.5% (111) | 4.1% (411) | 4.5% (359) | +0.003 | 1.00 | H1 against |
| jar ending | 74.8% | 66.4% | 68.8% | -0.02 | 0.58 | |
| spear ending (chief) | 12.6% | 12.9% | 13.1% | +0.005 | 0.94 | H9 against |
| carrier ending | 6.3% | 11.9% | 9.2% | +0.005 | 0.93 | |
| comb ending (junior) | 1.8% | 4.6% | 4.5% | +0.03 | 0.44 | |
| fish crest first in name (seals) | 12.3% (154) | 12.6% (596) | 12.8% (514) | +0.005 | 0.89 | H2 against |
| office opening (all objects) | 1.4% (365) | 0.9% (1,536) | 0.8% (765) | -0.02 | 0.45 | H3 against |
| office opening (seals) | 2.2% | 1.5% | 0.8% | -0.04 | 0.11 | H3 against (falls, if anything) |
| Boxed-cotton (all objects) | 1.9% | 1.6% | 1.6% | -0.01 | 0.87 | H4 against |
| short-horned bull (seals) | 5.0% (181) | 4.3% (723) | 3.3% (611) | -0.03 | 0.19 | H5 against |
| ship `705-500` (all) | 0 of 365 | 2 of 1,536 | 1 of 765 | | 0.55 | H5 against (too few) |
| sail 500 alone (all) | 0.3% | 0.1% | 0.5% | +0.02 | 0.38 | |
| no animal (seals, all sites) | 20.4% | 17.6% | 22.4% | +0.04 | 0.12 | H8 (Harappa alone: P 0.0018, finding 2) |
| goat (seals) | 1.1% | 0.8% | 0.2% | -0.05 | 0.077 | |
| unicorn stand W | 37.0% (81) | 43.4% (316) | 46.6% (281) | +0.06 | 0.12 | H6 direction |
| unicorn stand I | 7.4% | 14.9% | 6.4% | -0.06 | 0.098 | |
| seal face (median mm2) | 713 (146) | 676 (620) | 767 (504) | +0.07 | 0.019 | H8 against (bigger late) |
| seal text length (signs) | 4.4 | 4.2 | 4.3 | 0.00 | 0.99 | H7 against |
| 3-kalam chief `705-033-520` | 0.8% | 0.7% | 1.3% | +0.02 | 0.50 | H9 direction |
| cotton 390 | 8.5% | 5.5% | 7.1% | -0.01 | 0.80 | H10 against |
| grain 413 | 2.2% | 1.6% | 0.5% | -0.05 | 0.37 | |
| copper 850 | 1.4% | 0.8% | 0.9% | -0.01 | 0.70 | H10 against |
| ivory 923 | 1.6% | 0.9% | 1.2% | -0.01 | 0.80 | H10 against |
| cup 700 | 14.5% | 19.9% | 4.4% | -0.13 | 0.18 | (follows the tablet trenches) |
| thread 405 | 1.6% | 1.7% | 2.6% | +0.03 | 0.15 | |
| kindred / cloth 407 | 2.2% | 1.8% | 3.4% | +0.04 | 0.096 | |
| star name, number + fish (seals) | 10.5% | 9.8% | 10.6% | +0.01 | 0.78 | H11 against |
| *iru-mīn* `032-220` | 2.2% | 2.1% | 3.1% | +0.03 | 0.32 | |
| marked fish as two signs | 18.6% (70) | 15.8% (284) | 13.9% (173) | -0.04 | 0.35 | H12 direction |
| barred fish written `415-220` | 13.4% | 8.2% | 9.2% | -0.03 | 0.39 | H12 direction |

The DK-G sequence at Mohenjo-daro, seals level by level (`dkg_levels.csv`; level 0 = Early I at about 22 ft, 6 = Late I at about 4 ft):

| level | seals | agents | office | Boxed-cotton | no animal | short-horned | fish crest | median mm2 |
|---|---|---|---|---|---|---|---|---|
| 0 Early I | 36 | 0/23 | 1 | 1 | 6/36 | 2 | 0/36 | 574 |
| 1 Intermediate III | 107 | 6/66 | 3 | 3 | 14/107 | 2 | 9/107 | 588 |
| 2 Intermediate II | 91 | 0/53 | 1 | 2 | 14/91 | 5 | 11/91 | 630 |
| 3 Intermediate I | 125 | 4/72 | 3 | 4 | 32/125 | 12 | 15/125 | 524 |
| 4 Late III | 142 | 6/93 | 0 | 3 | 24/142 | 7 | 13/142 | 552 |
| 5 Late II | 72 | 4/45 | 2 | 0 | 14/72 | 3 | 8/72 | 663 |
| 6 Late I | 55 | 1/31 | 1 | 0 | 14/55 | 1 | 6/55 | 524 |

Spearman against level: agents +0.03 (P 0.57), office -0.03 (P 0.48), Boxed-cotton -0.06 (P 0.14), no animal +0.06 (P 0.13), short-horned -0.005 (P 0.91), fish crest +0.04 (P 0.31), size -0.006 (P 0.88). The one thing to note by eye: the earliest DK-G level has no fish crest in 36 seals (0 of 36 against 9 to 15 in every later level). Fisher on Early I against all later DK-G seals: not run as a planned test; it is a lead (prediction: the fish-crest houses are founded after the first DK-G level; it needs more Early-level seals).

## 4. The houses through time

The 15 biggest houses (first name sign of names of 2+ signs, every object kind; `houses.csv`). Expected counts come from the base mix of all dated house names (13.1% early, 52.8% middle, 34.2% late). r and P from the shuffle within area.

| house | sign | early | middle | late | expected (e / m / l) | r | P | cities, earliest bin |
|---|---|---|---|---|---|---|---|---|
| Bamboo-star | 235 | 9 | 31 | 24 | 8.4 / 33.8 / 21.9 | +0.01 | 0.77 | Harappa, Mohenjo-daro |
| High-star | 240 | 9 | 38 | 14 | 8.0 / 32.2 / 20.8 | -0.05 | 0.26 | Dholavira, Harappa, Mohenjo-daro |
| Branch | 415 | 8 | 26 | 9 | 5.6 / 22.7 / 14.7 | -0.06 | 0.064 | Harappa, Mohenjo-daro |
| Chest | 590 | 6 | 24 | 7 | 4.8 / 19.5 / 12.6 | -0.05 | 0.030 | Harappa, Kalibangan, Mohenjo-daro |
| 803 | 803 | 2 | 19 | 15 | 4.7 / 19.0 / 12.3 | +0.04 | 0.14 | Mohenjo-daro |
| Produce | 806 | 3 | 11 | 18 | 4.2 / 16.9 / 10.9 | +0.07 | 0.025 | Mohenjo-daro |
| Lady | 140 | 6 | 16 | 10 | 4.2 / 16.9 / 10.9 | -0.02 | 0.52 | Mohenjo-daro |
| Scabbard-fish / Bright-star | 233 | 5 | 14 | 12 | 4.1 / 16.4 / 10.6 | 0.00 | 1.00 | Mohenjo-daro |
| Star (plain fish) | 220 | 2 | 16 | 8 | 3.4 / 13.7 / 8.9 | 0.00 | 0.86 | Harappa, Mohenjo-daro |
| 798 | 798 | 4 | 13 | 8 | 3.3 / 13.2 / 8.5 | -0.01 | 0.72 | Mohenjo-daro |
| Hill | 503 | 2 | 9 | 11 | 2.9 / 11.6 / 7.5 | +0.04 | 0.23 | Mohenjo-daro |
| Chief (255) | 255 | 2 | 10 | 7 | 2.5 / 10.0 / 6.5 | +0.01 | 0.85 | Mohenjo-daro |
| Ward (741) | 741 | 2 | 10 | 4 | 2.1 / 8.4 / 5.5 | -0.02 | 0.64 | Mohenjo-daro |
| Kalam | 705 | 3 | 4 | 8 | 2.0 / 7.9 / 5.1 | +0.02 | 0.54 | Mohenjo-daro |
| quarter (061) | 061 | 2 | 7 | 5 | 1.8 / 7.4 / 4.8 | 0.00 | 1.00 | Harappa, Mohenjo-daro |

- Rise: the Produce house 806 (3 → 11 → 18; P 0.025), above all at Mohenjo-daro (3 / 7 / 14). Fall: the Chest house 590 (P 0.030) and Branch 415 (P 0.064, at Harappa P 0.085). First appears only from the middle bin: First-star 231 (0 / 4 / 6; P 0.11).
- City by city (`time_4_checks.py`, within-area shuffle at each city): 803 rises at Harappa (r +0.14, P 0.017) and is flat at Mohenjo-daro (P 0.75); 415 falls at Harappa (P 0.085) and is flat at Mohenjo-daro (P 0.33). No house falls at one city while rising at the other: the prediction "a house falls at one city and rises at another" went against.
- Every one of the 15 is in both big cities by the middle bin.

## 5. People: careers and lineages

`recurring_names.csv` lists every full name found on 2+ dated objects with its bins, cities, object kinds and endings by bin.

- Names spanning time are lineages. 65 names cross two bins against 65.2 shuffled, 12 cross all three against 11.9 (counting each name once per area and bin gives the same 65 and 12, so this is not tablet batches). 39 of 49 names with endings keep the same ending in every bin.
- The long lineages (all three bins, both big cities): `415-220` Branch-star, 14 objects, spearman (chief) in every bin from 3B to late; `590-390` Boxed-cotton, 14 objects, "house of" in every bin (a carrier in the middle bin); `415-100` Branch-Elder, 12 objects; `605-760` Granary-child, 8; `235-240` Bamboo-star High-star, 7; `255-435-690` Chief-Rod-[690], 6 objects at Mohenjo-daro; `503-615-752` Hill-Field heir, 9 copper tablets at Mohenjo-daro in all three bins.
- Careers (the ending moves up across bins; read as a promotion inside the lineage, or a junior branch taking office): `235-240` agent (`jar man`) early → agent and spearman in the middle and late bins; `705-255` "house of" early → also "X's man" middle and late; `798-415-220` "house of" early and middle → also spearman late; `803-233` spearman middle → spearman and "house of" late; `415-100` "house of" early → also "X's man" in the middle bin. Moves down: `681-690` spearman early → "house of" middle; `240-233` spearman middle → "house of" late. With 10 changes against 39 constant names, a rank was mostly inherited with the name.

## 6. The earliest and the latest inscriptions read whole

Dated by rule A or B, read whole or in part, at least 2 signs, distinct texts (`early_late_readings.csv`).

Earliest:

| object | site | date (rule) | signs | sounds | English |
|---|---|---|---|---|---|
| Dholavira 4164 (seal) | Dholavira | stage I, 2650-2550 BC (B) | 104-031-002-423-001-003-423 | taṭṭāṉ oru iru [423] oru mū [423] | Goldsmith; Three [423]; Four [423]. |
| Dholavira 951 (seal) | Dholavira | stage II, 2550-2500 BC (B) | 817-002-004-390 | kāṇi iru nāl maṟam | two shares: four warriors. |
| H-1550 (pot) | Harappa | Period 2, 2800-2600 BC (A) | 700-031 | nāḻi? oru | One cup. |
| Harappa 768 (pot) | Harappa | Period 2 (A) | 893-031 | [893] oru | One [893]. |
| Harappa 969 (pot) | Harappa | Period 2 (A) | 697-031 | [697] oru | One [697]. |
| H-1547 (pot) | Harappa | Period 2 (A) | 698-034 | [698] nāl | Four [698]. |
| Kalibangan 1948 (pot) | Kalibangan | Period 3A (B) | 005-411 | ai [411] | Five [411]. |
| Harappa 265 (tablet) | Harappa | 3B-1 (B) | 176-740-400 \| 034-700 | iṟai kuṭi ciṟ \| nāl nāḻi? | Junior of the Tax house. Four cups. |
| Harappa 1309 (tablet) | Harappa | 3B-1 (B) | 605-760-740-400 | kutir maka kuṭi ciṟ | Junior of the child of Granary house. |
| M-2851 (seal) | Mohenjo-daro | 3B-2, Mackay Early (B) | 140-919-520-360-861-002-235-231-705-033-032-877-740 | ammai [919] vēḷ [360] kāṇi iru vēymīn orumīn kalam mū iru nālkāṇi kuṭi | Of the Lady-[919]-Chief-[360] two shares Bamboo-star-First-star five kalam Four shares house. |

Latest:

| object | site | date (rule) | signs | sounds | English |
|---|---|---|---|---|---|
| Harappa 1196 (seal) | Harappa | Period 5A, after 1800 BC (B) | 216-861-367-001-176-740 | [216] kāṇi [367] oru iṟai kuṭi | Of the [216]-Share one [367] Tax house. |
| Harappa 1259 (tablet) | Harappa | Period 5A (B) | 519-177-740-400 \| 032-700 | [519] [177] kuṭi ciṟ \| iru nāḻi? | Junior of the [519]-[177] house. Two cups. |
| Harappa 1270 (tablet) | Harappa | Period 5A (B) | 219-740-807-400 \| 033-700 | [219] kuṭi [807] ciṟ \| mū nāḻi? | [807] of the [219] house; Junior. Three cups. |
| Harappa 1413 (seal) | Harappa | Period 5A (B) | 503-702-002-240-176-740 | malai [702] iru mīmīn iṟai kuṭi | Of the Hill-[702] Two-High-star Tax house. |
| M 2646 (seal) | Mohenjo-daro | Period 4, Mackay Late I (B) | 563-900-032-632-125-390-002-484-337-151 | [563] tiṅkaḷ iru pal vēṭṭuvaṉ maṟam iru [484] [337] kā | [563]-Month two manies Hunter-Warrior two [484] [337], keeper. |
| M 3084 (seal) | Mohenjo-daro | Period 4 (B) | 820-140-820-812-820-001-415-220-740-679 | kāl ammai kāl [812] kāl oru kavar mīn kuṭi kaṭṭil | quarter: throne of the Lady-Quarter-[812] one quarter Branch-Star house. |
| M 2297 (seal) | Mohenjo-daro | Period 4 (B) | 705-255-435-798-002-061-142-400-740 | kalam mutal kōl maru- iru kāl kō ciṟ kuṭi | Of the Kalam-Chief-Rod-Descendant two quarters King-Junior house. |
| M 2557 (seal) | Mohenjo-daro | Period 4 (B) | 503-455-220-002-806-235-240-055-740 | malai ampu mīn iru viḷai vēymīn mīmīn paṉṉiru kuṭi | Of the Hill-Arrow-Star two produces Bamboo-star-High-star-Dozen house. |
| M 2581 (seal) | Mohenjo-daro | Period 4 (B) | 140-920-190-297-002-016-220-740-090 | ammai tiṅkaḷ? [190] [297] iru āṟu mīn kuṭi āḷ | Manager of the Lady-Month-[190]-[297] Eight-Star house. |
| M 2226 (seal) | Mohenjo-daro | Period 4 (B) | 032-632-125-190-002-617-600-390 | iru pal vēṭṭuvaṉ [190] iru ūḻiyaṉ [600] maṟam | Two manies; Hunter-[190]; Two king's servants; [600]-Warrior. |

What differs:
- **Before the cities, writing is counting.** 35 objects date before about 2600 BC (HARP Periods 1-2, Dholavira stages I-II), 31 of them pots: 20 carry a count, 4 the cup, 3 the jar. Pot marks read "one cup", "four [698]". Against later objects the jar is rarer (3 of 35 against 896 of 2,122, P 2e-5), but pot against pot the gap is not significant (2 of 31 against 17 of 108, P 0.24), and only 2 seals predate the cities, so "the house formula arrived with the cities" is a lead, not a measured fact.
- **The account outlives the city.** Harappa tablets of Period 5A (after about 1800 BC) still read `X house, junior | n cups` exactly like the 3B chits: the cup-chit carried on after the city's peak, and the share of Harappa tablets with a cup count does not fall with period (rho -0.008, P 0.83; 2 of 3 Period 5A tablets).
- **The late seals are long titled house names**: several fish crests stacked (Bamboo-star-High-star), measure words inside names (two quarters, dozen), "King-Junior", "king's servants". The earliest mature texts already hold the same pieces (M-2851, Mackay's Early level, stacks Bamboo-star-First-star and five kalam into one house name). The difference is not grammar; it is how many titles get stacked into one name.

## 7. The measure leads (Job 2)

Predictions are in the docstring of `measures2_leads.py`, written before the run. Output: `work_data/measures/m2_log.txt`.

**(a) *kōṭṭai* 575 as the rung above the *kalam* (6 *kalam* or more).** Prediction: a1 where 575 and a counted *kalam* stand together the *kalam* count is 5 or less; a2 the count after 575 stays at 1-3; a3 the stacked seven before it ("seven *kōṭṭai*") marks big houses and bigger seals.
- a1 came true on all 4 lines: `1172` and `M4271` (`575 595 002 055 706 033`: *kōṭṭai*, forge, two dozen, three *kalam*), `2593` (`575 706 001 031`: *kōṭṭai*, two *kalam*), `M1026` (`032 575 032 002 705`: two *kōṭṭai*, four *kalam*). Four lines is all the corpus has.
- a2: counts after 575 are 1 (4), 2 (4), 3, 4 and 6 (once each; the 6 is `575 031 002 003 390`, a tall 1 followed by short 2 and 3: most likely one *kōṭṭai* and then 5 for the cotton 390). Owned counts 1 to 4.
- a3 went against: 16 lines have the stacked seven before 575, 14 of them close with the jar ("of the seven-*kōṭṭai* house"), but those seals are not bigger (median 412 mm2, n 11, against 499; P 0.86). They are longer (median 6 signs against 4). Reading kept: "seven *kōṭṭai*" is a house's grade, like "three *kalam*" is a man's. If one *kōṭṭai* is 6 *kalam*, seven *kōṭṭai* is 42 *kalam*, 14 men's yearly grain at 3 *kalam* each.

**(b) person count x cup count = 6 or 12.** Prediction: every tablet. On all tablets 26 of 36 (shuffle 22.1, P 0.028); on distinct texts 8 of 14 (shuffle 6.0, P 0.19). Rescue (`measures2_rescue.py`, prediction written first): count heads only where the person sign is not itself followed by the jar (`031 176 740` is "of the one-Tax house", a name, not one person) and skip counts that belong to a *kalam*: 7 of 10 distinct texts hit 6 or 12 (shuffle 5.0, P 0.26); all tablets 25 of 31 (P 0.042). The hits: 3 hands x 4 cups = 12 (21 tablets, 3 texts); 2 women x 3 cups (H-264); 3 carriers x 2 cups (922); 2 cultivators x 3 cups (1607, 1611). The misses: `416 861 002 | 034 700` "threshed heap, two shares | four cups" (2 tablets: 8) and `033 700 | 003 861 | 003 156` (3 x 3 = 9, H-2238). The products sit on 6 and 12 for 7 of the 10 kinds of chit; the shuffle cannot separate this from chance, because cups are mostly 3 or 4 and heads mostly 2 or 3, so 6 and 12 come up often by chance.

**(c) *niṟai* 171 takes 5 and 3: the weight system.** Prediction: only 3 and 5 (and 10s), never binary 2, 4, 8. Came true: 28 of 28 counts are 5 (20) or 3 (8), all in tall strokes; the 3 is written 2 + 1 every time. Cup counts are 3 or 5 on 39.8% and 2, 4 or 8 on 58.2%; 28 of 28 on 3 or 5 has P 6e-12 under the cup mix. The weight system at harappa.com is [binary in the lower weights (1, 2, 4, 8, 16, 32 ... up to 12,800) and decimal with fractional weights in thirds in the higher](https://www.harappa.com/slide/weights); the ratio-16 weight is about 13.6 g there, and the smallest known weight [0.865 g](https://cahc.jainuniversity.ac.in/assets/ijhs/Vol55_2_2020__Art06.pdf). *Niṟai* takes exactly the two non-binary steps of that system: 5 (half of ten, the decimal step) and 3 (the thirds). Where it stands: 21 seals, 13 tablets, 2 tags, 1 pot; 3 tablets also carry a cup count (`036 700 | 171 035 415` "six cups | full five, branch"; `036 700 | 171 033 700 415`; `171 035 415 | 033 700`). On a weighed grain reading, 5 *niṟai* = 6 cups (41.6 to 44.4 kg of grain at 0.75 to 0.80 kg a litre) makes one *niṟai* about 8.3 to 8.9 kg, under the 12,800-unit top of the stone series (about 10.9 kg at 0.85 g a unit). The 3-cup tablet would make it half that; the two tablets do not agree on one size, so the gram value stays open. The repeating seal `061 171 035 740 090` ("quarter, full five, house-of, man") is a title built on the weight word.

**(d) a count after the monthly allowance `320-920` never exceeds one person's month.** Went against, once: 19 uses; only one has a count after it, H-259 `861 002 798 320 920 017 575 740 400` "two shares, [798], monthly allowance, seven *kōṭṭai*, of the house, junior": seven *kōṭṭai* is far above one person's 3.75 cups. Everywhere else the phrase is followed by the jar (10), the chief 520 (4) or 550 (2). Read: "monthly allowance" is a title inside names ("of the monthly-allowance house", "the monthly-allowance chief"), and the one counted case is a house's monthly allowance, not a man's.

**(e) multi-face tablets as one record.** 845 multi-face tablets and tags were joined into one record each, the who-face first, with the joined English (`m2_records.csv`). e1 came true: a number on one face equals a number on another face on 52 of 138 distinct records against 41.0 shuffled (P 0.012); all objects 82 of 179 against 59.3 (P below 0.0003). e2 went against: one number equals the sum of the others across faces on 1 of 15 distinct records against 3.3 shuffled (P 0.98). e3: 5 distinct records carry a *kalam* count and a cup count; the cup count equals the *kalam* count on 2 (H-774 and H-1813: "High-star / Star three-*kalam* Gate-Guard, junior. Grain, *kōṭṭai*, town, pot: three cups"). Read: a record repeats its key number across faces (a check figure), and no tablet carries a total.

## 8. What went against, and the rescues tried

- **Administration did not thicken (H1, H3, H9).** Agents 4.5 / 4.1 / 4.5%; office opening 1.4 / 0.9 / 0.8%. Rescue 1 (redesign D1): the one long sequence, DK-G level by level, where all seven levels are one dig: still flat (agents P 0.57, office P 0.48). Rescue 2 (D2, first appearances): the office and the cotton house were already in two or three cities in the earliest bin. The reading that survives: administration was born whole with the cities.
- **The Mesopotamian-trade window (H5).** Short-horned bull 5.0 / 4.3 / 3.3% (P 0.19); ship word 0 / 2 / 1 objects. Unshuffled, all sites: short-horned 9 of 181 early against 20 of 611 late (P 0.27). No middle-bin peak. The overseas seal and the ship word run through the whole sequence; the overseas trade was as old as the cities. Next: the abroad seals' own find dates in Mesopotamia and the Gulf (Akkadian, Ur III) give the window from the other end.
- **A house that falls at one city and rises at another.** None of the 15 biggest houses does: 803 rises at Harappa (P 0.017) and is flat at Mohenjo-daro; 415 falls at Harappa only.
- **Smaller late seals (H8 half).** Seals are bigger late (P 0.019). The inscription-only half came true at Harappa (P 0.0018).
- **New idea: the account moves from tablets to seals late (D4).** Went against: the share of Harappa tablets with a cup count does not fall with period (rho -0.008, P 0.83).
- **Writing before the cities (time_5).** The jar is rare before 2600 BC (3 of 35), but pots against pots it is not significant (P 0.24) and there are only 2 seals before the cities.
- **Measures:** a3 (seven-*kōṭṭai* seals not bigger, P 0.86), b (6 or 12 not above shuffle on distinct texts, P 0.19 and 0.26 after the rescue), d (one count far above a month), e2 (no totals, P 0.98).

## 9. What it opens

1. One reading key for six centuries: any value tested on 3B objects can be tested on 3C objects with no correction, so time is a free held-back set. Next: split the value list by bin and check that each value's facts hold in every bin.
2. Dating by form, not text: inscription-only seals at Harappa and the large unicorn format date a seal; the text does not.
3. Lineages: the 12 names in all three bins are the families to follow; `415-220`, `590-390` and `415-100` cover about six centuries in both big cities.
4. The weight word: *niṟai* with 3 and 5 ties the script to the stone weights. Next: find *niṟai* lines on objects found with weights (Harappa trenches with cubical weights) and look for tall 10s.
5. The earliest DK-G level has no fish crest (0 of 36 seals): test whether the star houses were founded after the first city level, with more Early-level seals from both catalogues (the second catalogue's `level` column for Mohenjo-daro is not used yet).
