# Chits: the people of the tablets

Word-free job, 2026-11-17. Sign numbers, pictures, jobs, counts, sizes and findspots only. Scripts in `work_scripts/` (each carries its predictions in its top docstring, written before its numbers): `chits_common.py` (loader), `chits_1_titles.py`, `chits_2_names.py`, `chits_3_amounts.py`, `chits_3b_rescue.py`, `chits_4_batches.py`, `chits_5_third.py`, `chits_6_mohenjo.py`, `chits_7_time.py`. Tables and logs in `work_data/chits/` (`c1_*` to `c7_*`, `c3b_log.txt`, `objects.csv`, `jar_faces.csv`). Each script runs in under a minute.

## Plain words

- **Seal**: a carved stamp. **Tablet**: a small flat clay plaque; **moulded** (catalogue TAB:B, pressed from a mould, so copies are identical) or **incised** (TAB:I, cut by hand one at a time). **Copper tablet**: a small copper plaque, usually with a picture on one side. **Rod**: an inscribed ivory or bone stick. **Tag**: a clay lump that was pressed over a knot or lid.
- **Face**: one inscribed side. **Record**: one object with 2 or 3 faces, read as one entry.
- **Jar** = sign 740, the commonest closing sign. **After-jar sign**: the sign right after the jar. **Comb** = 400 (a vertical line with side ticks). **Man** = 090 (a plain two-armed person). Other after-jar signs (frame-v2 job "title"): 679 X with table, 565 closed X, 621 barred tall rectangle, 527 hatched box, 161 porter with diamond, 241 caged fish, and six signs used once each (170, 224, 481, 622, 686, 932).
- **Name**: the signs before the jar, with any opening word and the slot after it taken off. **Crest**: the first sign of the name.
- **Name face / amount face**: on a record, the face carrying the name, and the face carrying only number strokes and measure signs. **Cups**: the number of tall strokes beside sign 700 (a plain U). **Big measure**: sign 705/706 (a U with a long stroke through it), 12 cups each. **Porter**: 156, a person carrying two loads.
- **Chit**: a Harappa tablet whose name face ends jar + comb (740-400). **Issue**: one distinct tablet text found in one trench; identical copies in the same trench count as one issue. **Copies**: how many identical tablets one issue has.
- **Trench**: the excavator's digging area at Harappa (FTrench I, ETrench 11 ...). **Mound**: the trench's letter group (F, E, ET, D, AB).
- **Bin**: early / middle / late period (`work_data/time/time_axis.csv`). At Harappa early = Period 3B, middle = 3B/C to 3C-2, late = 3C-3 onward.
- **Seal size residual**: the log of a seal's face area minus the median for seals of the same city, text length and seal shape. 0 = typical; -0.69 = half the face.
- **Shuffle**: the label being tested (an ending, a trench, a bin) is dealt at random many thousand times inside the stated group; **P** = share of shuffles at least as extreme as the real number. Small P = the real pattern is not chance, in the direction stated.

## What was found

**1. The comb is a class of person, and the class keeps across objects.** Take the 71 distinct names on comb chits. 20 of them also stand before a jar on a seal (60 seals). 5 of those 60 seals end in the comb too, against 0.80 when seal endings are shuffled inside each city (P 0.0005). That is six times chance. Control: names from Harappa tablets ending in the jar alone keep the jar alone on their seals at chance (70 of 91 against 72.95). So the comb, unlike the plain jar, follows the person from tablet to seal. The two comb seals of the name 176 (seated person with four ticks) are H-352 and H-354. Both were found in FTrench I, and FTrench I also holds 22 of that name's 36 chits. *Means*: a comb holder's chits were kept or issued where his own small seal lay. *Opens*: the comb holder is a person with a standing class, not one entry in a ledger.

**2. Comb holders cut seals half the size of everyone else. The man class does not.** Comb-ending seals: residual -0.741 (11 seals) against -0.016 for 513 jar-only seals, which is x0.48 of the face (P below 1 in 4,000). Man-ending seals: -0.021 (46 seals; P 0.94, the same size as jar-only). 679 is bigger (+0.231, 8 seals, P 0.11). 565 is smaller (-0.198, 4 seals). Seals of chit names, whatever their ending, average -0.236 (50 seals) against -0.105 for the seals of jar-only tablet names. *Means*: the comb holder is the lowest seal class. The man holder is a full-size seal holder.

**3. Comb and man are different people; comb holders share names with plain jar holders.** Count the names written with two different endings, against endings shuffled inside city and object kind. Comb + man: 4 names against 17.71 (0.23 of chance). Jar-only + comb: 33 against 66.13 (0.50). Jar-only + man: 14 against 33.97 (0.41). All three fall below chance because an ending belongs to its person. The comb and man pair is the most separate of the three, about half as often as either sign shares with the plain jar. *Means*: a man holder is almost never a comb holder under the same name, but comb holders bear the same names as plain jar holders about half as often as chance. That fits **juniors or dependants of a house carrying the house's name**. Names shared both ways: 840-032, 415-100 and 220 occur with jar, comb and man; 590-390, 605-760, 240-636, 440, 717, 388, 803 and 100 occur with jar and comb (`c1_names_two_endings.csv`).

**4. The comb names have their own crests: the seated person 176 heads one in five.** Crest kinds on Harappa tablets. Comb (159 names): seated person 176 24%, fish 8%, numbers 14%, goods signs 10%. Jar-only (198): 176 5%, fish 25%. Man (26): fish 31%, 176 4%. Over all objects, 176 heads 41 of 187 comb names, 26 of 1,002 jar-only names and 2 of 98 man names. *Means*: the fish crests (the house emblems of the seal class) are thin among comb holders, and the seated person is the comb holders' own head sign. The single biggest chit name is `176-740-400`: 36 tablets, 22 of them in FTrench I, 16 seals of 176 before a jar in three cities.

**5. Comb holders draw the same cups as everyone else.** Neither prediction held (section "What went against"). Harappa records with a cup count, mean cups: comb 2.97 (98 records), jar-only 2.92 (99), man 3.20 (5), name with no jar 2.95 (109); comb minus jar-only P 0.67. The cup mix is the same shape in every class: about 1 in 4 records at 2 cups, a bit under half at 3, 1 in 4 at 4. *Means*: the amount is set by the name (`spots.md`: a name keeps its own amount), not by the class. The comb class gets an ordinary monthly issue. Comb holders are less held to one amount than other names (share of a name's records on its usual count 0.63 against 0.76, P 0.08, 11 against 16 names). One thing does separate the comb: **comb records never carry the big measure** (0 of 150 against 26 of 541 other name records, Fisher P 0.0026). But jar-only records hardly carry it either (2 of 247); 21 of the 26 are names with no jar. The big-measure records belong to the measure-holding names themselves, such as `705-033-...` (three big measures).

**6. Comb chits are hand-cut more than the others.** Harappa comb tablets: incised 113, moulded 95 (54% incised). Jar-only tablets: incised 104, moulded 155 (40%). Fisher P 0.0028. Copies per text: comb 1.54, jar-only 1.36 (P 0.24). *Means*: a comb chit is more often written by hand for the one occasion. The plain-jar chits are more often pressed from a mould, which is the form of a standing, repeated issue.

**7. The issuing side: every trench pays out to many names, every name draws from several trenches, and the one fixed office face sits across the whole city.**
- One trench, many names. ETrench 11: 56 issues to 49 names. F-: 50 to 48. FTrench I: 45 to 42. ETrench 54: 41 to 40 (`c4_trenches.csv`). Nearly every issue in a trench goes to a different name.
- One name, many trenches. 72 names on 2+ issues sit in 2.54 trenches each, against 2.56 with trenches shuffled (P 0.36). At mound level: 1.86 against 1.93 (P 0.16). A name's chits are found wherever the chits of the city were dropped or stored. Names are not tied to a place.
- The comb is concentrated in FTrench I: 39 of 86 tablets there against 22% across Harappa (trench test P 0.0025). All of that comes from the name 176. Without 176, 17 of 64 (P 0.80).
- No trench has its own issuer's mark. 35 faces stand beside 3+ different partner faces inside one trench: 31 are amount faces (`034-700`, `033-700` ...) and 4 are names. At city level, a small set of **heading faces** stand beside many different names (`c6_headings.csv`, 49 faces on 49 objects in 17 trenches):
  - `413-575-335-711-033-700`, and the same line shortened or varied: 21 objects. It goes with names that carry the big measure: `240-705-033-550-525-400` (5 objects), `220-705-033-550-525-400`, `000-705-033-550-525`, `156-924-705-740-851` (3), and with `851-741-048-740` / `850-741-048-740` (4).
  - `413-892-824` (and `413-892`): 14 objects, beside 12 different partner faces in 7 trenches. 5 of the 14 partners end in the comb (`171-032-031-240-636-740-400` 3 times, `033-700-176-740-400`, `141-740-400`).
  - `415-578-032-824/876`: 5 objects in 5 trenches, beside one name (`799-840-760-740` / `799-840-714-740`) 4 times with 3 or 4 cups, and once beside `692-060-240-636-740`.
  These are the **offices of the issuing side**, written as a third face or as the second face: lines that open with 413 (a vertical line crossed by short lines) or 415-578 and close with 824/876. A name drew from them, and the same office line turns up in many trenches.
- Copies do not follow cups. Spearman +0.069 over 253 issues (P 0.12); copies equal cups in 2.8% against 1.9% by chance. City-wide: +0.043 (P 0.24). The batches are uneven: 20 copies of the no-name `003-156 | 003-861 | 034-700` (ETrench 11), 13 and 7 copies of `176-740-400` at 3 and 4 cups (FTrench I), 7 of `347-741-176-740-090` (ETrench 11), 7 of a 12-sign jar name (FGranery).

**8. The third face.** 70 objects carry 3+ faces (Harappa 46, Mohenjo-daro 13, Lothal 6, Kalibangan 3). After name and amount are taken out, the 87 distinct third faces sort as: second name 20, other 22, single sign 17, lost 15, second amount 5, heading line 4, count + porter 4 (`c5_kind_by_ending_issue.csv`). The "hands / loads / cups" tablet of ETrench 11 (`003-156 | 003-861 | 034-700`, 20 copies) has **no name face at all**: three porters, three of the front-word diamond 861, four cups. So the big ETrench 11 batch is an issue to an unnamed work gang, the one place where recipients appear as a group. Only 2 comb issues have a third face: H-355 repeats its amount `033-700`, and H-987 carries `817-365-690`. The heading lines (`415-578-032-824/876`) are third faces only beside the name `799-840-...-740`.

**9. Mohenjo-daro does the chit's job with copper tablets: one picture, one text, many copies, no amount.** Harappa clay tablets: 1,083, of which 500 (46%) carry a cup count, 208 carry the comb and 340 are amount + name records. Mohenjo-daro clay tablets: 112, of which 7 carry cups and 7 the comb. Mohenjo-daro copper tablets: 189, of which 2 carry cups and **0 carry the comb or the man**; 116 carry a jar name and 131 a picture. Copies per distinct text: Mohenjo-daro copper 2.48 (164 objects, 66 texts), Harappa clay 1.45, Mohenjo-daro clay 1.52. Leading copper texts: `503-615-752-740` x29 (the picture field reads "other" on 28), `235-705-033-845-407-321-407` x12 (hare), `806-845-061-407-850-900-740` x10 (human figure), `706-033-923-740` x7 (elephant). At Mohenjo-daro the comb sits on **rods**: 9 of 32 rods, against 5 of 1,318 seals. *Means*: Harappa issued per person and per amount on clay. Mohenjo-daro issued the same text, with a picture, to many hands on copper, with no amount written. The comb class at Mohenjo-daro carried rods. Kalibangan has comb tablets with cups (`032-700 | 263-740-400`) and comb pots, and so follows Harappa.

**10. The comb chit runs through every period at Harappa at the same share.** Comb share of dated Harappa tablets: early 18 of 100 (18.0%, chance 17.0%), middle 124 of 579 (21.4%, chance 21.8%), late 16 of 60 (26.7%, chance 25.1%). Chance here means bins shuffled inside format and trench (all P above 0.34). By period: 3B 16, 3B-1 2, 3B/C 95, 3C-1 17, 3C-2 6, 3C 6, 3C-3 11, 3C-4 3, 4 1, 5A 1. Mean cups by bin: 2.86 / 3.11 / 2.50 (spread P 0.15). The names turn over. Early and middle share 4 names against 6.59 shuffled (P 0.09), and the late names are almost all new (16 names, 8 shared with the middle bin). Name 176 is a middle-bin holder: 28 of its 31 dated chits are middle, 27 in Period 3B/C. *Means*: the comb class is an institution of the whole Harappa sequence. The people in it change, and the amounts do not.

## What the comb class is

Numbers that decide between the four readings:

| reading | predicts | measured | verdict |
|---|---|---|---|
| ration recipients as a group (workers on fixed rations) | one amount for all comb records | modal cup share 0.47 comb against 0.43 jar-only (P 0.29); the one group issue with no name (E11 porters) carries no comb | against |
| lower grade drawing less | fewer cups, no big measure | 2.97 against 2.92 cups (P 0.67); big measure 0 of 150 against 2 of 247 for jar-only | against on cups |
| juniors / dependants of houses | small seals; names shared with jar holders; own crest; the class follows the person | seal x0.48 (P < 0.00025); jar + comb names 0.50 of chance against comb + man 0.23; seated-person crest 22% against 3%; comb seals for chit names 5 against 0.80 (P 0.0005) | **building on it** |
| a title / office | holders in many cities, a fixed few names, big or equal seals | 87 names, 213 of 245 objects at Harappa, half-size seals | against |

**The comb class is a dependent class of persons attached to named houses.** They are written with the house's name plus the comb, and they hold half-size seals or none. They drew ordinary monthly cup issues, on chits that were more often cut by hand, from the same city-wide stores that paid everyone. The issuing ran through city-wide offices, not through each house. Every trench pays out to dozens of names, and a name draws from any trench. The only fixed faces beside many names are the heading lines `413-575-335-711(-033-700)`, `413-892-824` and `415-578-032-824/876`. The first goes with holders of three big measures, the other two with ordinary names including comb holders. The man class is a separate class: full-size seals, many cities, fish crests, and almost never the same name as a comb holder (4 names against 17.7). That fits the agent who lives in the master's building (`spots.md`), next to a comb junior who lives on issues.

What each reading predicts that has not been checked:
- Juniors of houses: at Mohenjo-daro, a comb rod or comb seal should lie in the same building or block as a jar-only seal of the same crest more often than chance (same test as the manager test in `spots.md`, run on the 21 comb objects there). The comb holder should also never hold the bigger stand letters (W).
- Dependants on issues: the incised comb chits of one name should cluster in depth, one hand-cut issue at a time, while moulded jar-only chits should spread through depth.
- Office headings: every name beside `413-892-824` should be an ordinary-size name, and every name beside `413-575-335-711` should carry the big measure. That holds on the objects listed. The second catalogue's Harappa tablets are the fresh set for it.
- Rations as a group: the porter / front-word / cup tablets with no name (E11) are the group issue. They should never carry a comb, and none of the 20 does. Look for other nameless count + porter tablets in the second catalogue.

## Tables

### After-jar signs (`c1_titles.csv`)

| after jar | picture | objects | seals | tablets | copper | tags | pots | rods | cities | Harappa / Mohenjo-daro | seal size residual (n) | names | top crests |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| nothing | jar only | 1281 | 723 | 315 | 98 | 48 | 83 | 3 | 36 | 439 / 633 | -0.016 (513) | 658 | 240, 503, 235, 032, 806, 803 |
| 400 | comb | 245 | 11 | 219 | 0 | 0 | 6 | 9 | 7 | 213 / 21 | -0.741 (11) | 87 | 176 (41), 240, 798, 806, 503, 617 |
| 090 | man | 117 | 57 | 41 | 0 | 16 | 2 | 1 | 9 | 41 / 49 | -0.021 (46) | 63 | 705 (13), 347, 104, 235 |
| 679 | X with table | 9 | 9 | 0 | 0 | 0 | 0 | 0 | 2 | 1 / 8 | +0.231 (8) | 9 | 240, 798 |
| 565 | closed X | 8 | 6 | 2 | 0 | 0 | 0 | 0 | 2 | 2 / 6 | -0.198 (4) | 5 | 231 |
| 621 | barred tall rectangle | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 3 | 1 / 2 | +0.077 (3) | 4 | |
| 527, 161, 170, 224, 481, 622, 686, 932 | | 1 each | | | | | | | | | | | |
| any other sign | | 168 | 88 | 40 | 19 | 9 | 11 | 1 | 11 | 59 / 76 | +0.032 (53) | 81 | |

527, 621 and 161 are mostly used elsewhere in the text, not after the jar (527 1 object, 621 4, 161 1).

### Chit names and their seals (`c2_sets.csv`, `c2_chit_names.csv`)

| Harappa tablet names ending | distinct names | on a seal | seals | comb-ending seals | seal size residual |
|---|---|---|---|---|---|
| jar + comb (chits) | 71 | 20 (28%) | 60 | 5 (0.80 by chance, P 0.0005) | -0.236 |
| jar only | 116 | 29 (25%) | 91 | 4 | -0.105 |
| jar + man | 14 | 6 (43%) | 29 | 4 | -0.145 |
| jar + other title | 15 | 5 (33%) | 25 | 2 | -0.074 |

Chit names by number of tablets: 44 names on 1, 13 on 2, 8 on 3, 3 on 5, and one each on 6, 8 and 36 (176).

### Cups by class (`c3_distributions.csv`; Harappa, one row per object)

| name ends | records | with cups | 1 | 2 | 3 | 4 | mean | share on the usual count | big measure | no amount face |
|---|---|---|---|---|---|---|---|---|---|---|
| jar + comb | 147 | 98 | 1 | 26 | 46 | 25 | 2.97 | 0.47 | 0 | 35 |
| jar + man | 10 | 5 | | 1 | 2 | 2 | 3.20 | 0.40 | 0 | 5 |
| jar only | 192 | 99 | 2 | 29 | 43 | 25 | 2.92 | 0.43 | 2 | 77 |
| jar + other sign | 26 | 19 | | 4 | 7 | 8 | 3.21 | 0.42 | 0 | 5 |
| name with no jar | 192 | 109 | | 37 | 40 | 32 | 2.95 | 0.37 | 2 (13 more with an uncounted 705) | 57 |

With identical copies in one trench counted once: comb 2.89, jar-only 2.93 (P 0.40). One vote per name: comb names 2 cups 22, 3 cups 19, 4 cups 9; jar-only names 22 / 32 / 19.

### Issues at Harappa with 3+ copies (`c4_batches.csv`)

| copies | trench | text | name ending | cups | format | bin |
|---|---|---|---|---|---|---|
| 20 | ETrench 11 | `003-156 \| 003-861 \| 034-700` | no name | 4 | incised | early, middle |
| 13 | FTrench I | `033-700 \| 176-740-400` | comb | 3 | moulded, incised | middle |
| 7 | FTrench I | `034-700 \| 176-740-400` | comb | 4 | incised | middle |
| 7 | ETrench 11 | `347-741-176-740-090` | man | - | moulded | early, middle |
| 7 | FGranery | `803-415-220-318-920-255-436-690-590-407-740` | jar | - | moulded | middle, late |
| 5 | FTrench I | `605-760-740-400` | comb | - | incised | early, middle |
| 4 | ETrench 11 | `034-700 \| 176-156` | no jar | 4 | moulded | middle |
| 3 | ETrench 11 | `820` | - | - | moulded, incised | early |
| 3 | FTrench I | `013-840-740 \| 033-700` | jar | 3 | incised | middle |
| 3 | FTrench I | `033-700 \| 900-368` | - | 3 | incised | middle |

### Two cities (`c6_city_kinds.csv`)

| city, kind | objects | with cups | jar name | comb | man | picture | copies per text |
|---|---|---|---|---|---|---|---|
| Harappa clay tablets | 1083 | 500 | 526 | 208 | 29 | 318 | 1.45 |
| Harappa seals | 428 | 11 | 175 | 4 | 11 | 292 | |
| Mohenjo-daro clay tablets | 112 | 7 | 73 | 7 | 12 | 70 | 1.52 |
| Mohenjo-daro copper tablets | 189 | 2 | 116 | 0 | 0 | 131 | 2.48 |
| Mohenjo-daro rods | 32 | 1 | 12 | 9 | 0 | 2 | |
| Mohenjo-daro seals | 1318 | 7 | 572 | 5 | 37 | 1029 | |

### Comb by period at Harappa (`c7_bins.csv`)

| bin | tablets | comb | share | chance | comb cups (2/3/4) | comb names |
|---|---|---|---|---|---|---|
| early (3B) | 100 | 18 | 18.0% | 17.0% | 3 / 2 / 2 | 13 |
| middle (3B/C to 3C-2) | 579 | 124 | 21.4% | 21.8% | 11 / 31 / 20 (+1 at 1) | 59 |
| late (3C-3 on) | 60 | 16 | 26.7% | 25.1% | 4 / 4 / 0 | 16 |

## What went against

- **Amounts do not mark the class** (predictions A1 and A2). Comb names draw the same cups as jar-only names (2.97 against 2.92, P 0.67), and the comb mix is no more uniform (usual-count share 0.47 against 0.43, P 0.29; with copies counted once 0.41 against 0.42). Redesign: per name, whether a comb name stays on one amount. It goes the other way: comb names vary more (0.63 against 0.76, P 0.08). New idea: tablet format. That one paid: comb chits are hand-cut more often (P 0.0028). The amount line is closed for class. Amount belongs to the name.
- **Copies do not follow cups** (B2). Spearman +0.069 (P 0.12) in trenches, +0.043 (P 0.24) across the city. Redesign: done (city-wide). New idea: copies by class. Comb 1.54 against jar-only 1.36 copies per text (P 0.24), no difference. Paused after two ways in. Batches are made by the issuer's mould, not by the amount.
- **Names are not tied to a trench or a mound** (B1, Q3). 2.54 trenches per name against 2.56 (P 0.36); 1.86 mounds against 1.93 (P 0.16). The seal of a chit name lies in the trench of its chits 2 times of 13 against 2.09; same mound 7 against 7.46. Redesign: mound level, done. New idea: the comb seals in particular. Both Harappa comb seals of 176 lie in FTrench I with 22 of its 36 chits, but that is one name. Kept as a lead for the Mohenjo-daro comb rods (the junior-of-house test above).
- **No trench has its own issuer's mark** (B3). Constant faces inside a trench are amount faces (31 of 35). The office lines exist at city level only (finding 7).
- **The FTrench I comb cluster is one name**: without 176, 17 of 64 (P 0.80).
- **The comb does not cluster in time** (T1): its share is at chance in every bin (P 0.34 to 0.75).
- **A comb seal for chit names is rare in absolute terms**: 5 of 60 seals; 40 of the 60 end in the jar alone. A comb holder who owns a seal mostly cut it with the plain jar, or the names belong to more than one person of a house.
- A name made only of lost signs (`000`) is left in the time table's name lists and in the name-overlap test (`chits_7_time.py`). It adds at most one shared name to each pair of bins, so the overlap counts above are upper bounds.
