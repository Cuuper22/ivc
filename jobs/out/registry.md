# The registry: a who's who of the Indus cities, and the tests it runs

Reading order = stored order reversed. Scripts (in `work_scripts/`, rerun with `python3` in this order): `registry_build.py` (people, every named object, houses), `registry_tests.py` (great houses, clustering, tests a to e as first written), `registry_tests2.py` (one redesign and one new idea for each test that went against), `registry_offices.py` (titles and offices, kings, the signboard name). Tables in `work_data/registry/`: `people.csv`, `houses.csv`, `names_all.csv`, `great_houses.csv`, `offices.csv`; printouts `tests.txt`, `tests2.txt`, `offices.txt`. Each test script has its predictions in its top docstring, written before it was first run. The readable book is `WHOSWHO.md` in the repository root.

Plain words used below:
- **Name** = the signs between the opener (share, quarter, office words at the front) and the ending. **Crest** = the first word-sign of the name, the family element (house-mates share it, `name_slot.md`). **Personal part** = the signs between crest and tag. **Tag** = the last sign of a name of two or more signs. For the plain fish the number in front belongs to the star word (`032+220` = *iru-mīn* "Dark-star"), so it stays in the house key. `590-390` (Boxed-cotton) is kept as one two-sign house. `705` and `706` (two drawings of *kalam*) are one house.
- **Ending** = what the person is: jar 740 "house of" (an owner), jar + man 090 "X's man" (an agent; X is the master's name and the seal goes to the master's crest), spear 520 "chief", keeper 151-161, comb 400 "junior", guard 525-527, gate + guard "gate-guard", text-final 368 "standard-bearer", 842 "deputy", jar + 679 "seat (throne)".
- **House** = all people and objects whose name starts with one crest. **Great house** = the 20 houses with the most objects naming them, among houses with at least 5 seals, title words (king, keeper, servant ...) left out.
- **Findspot**: city; area (the catalogue's excavation area); building (area + house number at Mohenjo-daro, e.g. `DKG (S) 7II`; area + grid square at Harappa and other sites); block (Mohenjo-daro: area + the block number in front of the house number, block 7 for `7II`).
- **Shuffle**: the labels in question are mixed among seals of the same city many hundred or thousand times; P = share of shuffles at least as strong as the real count. Small P = the real pattern is not chance and points the way stated. **Ratio** = real count divided by the shuffled average.

## 1. What was found

1. **"X's man" is the manager who lives in X's house.** Agents sit in a building that also holds an owner seal or tablet of their master's crest 5 of 24 times at Mohenjo-daro against 2.10 by shuffle (ratio 2.38, P 0.046); family members do it at chance (44 of 588 against 49.5). Agent seals are bigger than the owners' seals they serve: median face 718 mm2 (40 agents) against 620 for owners of the same crests (P 0.044) and 581 for all owners (P 0.016). `measured`. The prediction was the other way (agents posted away, test a); the data say the agent is housed with his master and outranks the family members by seal size. This points to the reading already in the sound list, `[crest] kuṭi āḷ` "manager of the [crest] house", the steward and head of the household, over "a servant posted out". The five cases: M-1746 and M-199 (High-star-Branch-Elder's managers) in DKG(S) 7II and DKG First Street beside High-star owners M-1726, Lipi-2388, M-2106; M-865 (Bamboo-star-High-star's manager) in DKE Trench E beside Bamboo-star owners M-1738, M-47, M-323; M-100 (Kalam-Chief's manager) in DKE Trench E beside the Kalam house's Boxed-cotton seals M-431, M-432; M-265 (Quarter-Full-weight-Five's manager) in DKG(S) 9VIII beside Quarter owner M-408. What it opens: an agent seal marks the house itself on the ground, so where an agent seal is found, the master's family lived.
2. **The kings are quarter-kings.** The quarter sign (061 or 820, *kāl*) stands right before the king sign 142 (*kō*) in 11 of its 81 uses, against 1.37 expected from how common quarter signs are (P 1.3e-7), at Harappa (6: H-1662, H-1672, H-1679, H-451, H-471, H-780) and Mohenjo-daro (5: M-1772, M-164, M-717, M-837, M-879). The same quarter sign stands before the signboard's umbrella 611 in 2 of its 6 uses (P 0.004): the Dholavira signboard itself and Lothal L-116 (`820-611`). `measured`. Read: *kāl kō* "Quarter-King", the king of one city quarter, the title the Dholavira signboard writes as "the quarter of King Umbrella" (`guess`). The prediction "one king house per city" went against (Mohenjo-daro: 22 objects with the king word, 13 different crests; Harappa 12 objects, 4 crests): a city had several kings, one per quarter, and the Quarter-King lineage name `061-142-400-740` "of the Quarter-King-Junior house" stands in both big cities (H-1679, H-451, H-780, M-879).
3. **Members of a great house live in the same buildings, not the same neighbourhoods.** Same-house pairs of seals share a building at Mohenjo-daro 23 times against 16.3 by shuffle among the top 20 houses (ratio 1.41, P 0.080); High-star 6 against 1.62 (P 0.020), Tax 3 against 0.71 (P 0.050), Bamboo-star 8 against 3.80 (P 0.069). At block and area level there is no pull (0.93 and 0.93). `measured`. A house is a household in one building, and the great houses are spread across the city, not walled into one ward.
4. **The crest is the family, the tag is not (Mohenjo-daro).** Seal pairs with the same crest share a building 28 times against 19.5 (ratio 1.43, P 0.056); pairs with the same tag but different crests 16 against 14.4 (ratio 1.11, P 0.35), as predicted (test c). `measured`. At Harappa, same-tag pairs share an excavation area 32 times against 19.1 (ratio 1.68, P 0.011): there the tag goes with the trench. `measured`; read: at Harappa the tag names the workplace (the granary trenches), a lead.
5. **A grain-named house carries grain words, a measure-named house carries measure words.** On every object carrying the house name, signs other than the crest: Bounty 806 (*viḷai* "produce") has a grain word on 22 of 133 objects against 5.7% for objects of other houses (P 1.4e-5; distinct texts 13 of 106 against 5.2%, P 0.0047); Kalam 705 (*kalam* "grain measure") has a store or measure word on 55 of 213 against 12.7% (P 6e-7; distinct texts 19% against 13.0%, P 0.013); Chest 590 (*peṭṭi*) 17% against 12.8% (P 0.063). `measured`. This counts the rest of the name too, so Bounty-Sheaf `806-845...` on 14 copper tablets is part of it: the produce house names itself with crop words and stamps crop records. Boxed-cotton went against (cotton on 5 of 71, against 5.5%).
6. **The registry.** 1,190 seals read whole (685) or nearly whole (505, at most one sign without a value) with a name, in 273 houses; 3,422 faces of every kind carry a name closed by an ending or are seal names; 439 houses in all. 41 of the seals are agents. `measured`.

## 2. The great houses

Objects = every undamaged object naming the house (seals, tablets, copper tablets, tags, pots; moulded copies count each). Building pull = same-house seal pairs in one Mohenjo-daro building against shuffles. Goods = commonest goods words on the house's goods objects outside its name (from `houses.csv`; the cup 700 is the account unit on tablet backs).

| rank | house | crest | sounds | seals | agents kept | objects | cities | ranks held (seals) | overseas bull | main areas | building pull (MD) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | High-star | 240 | *mīmīn* | 39 | 3 | 119 | 7 | house of 19, chief 7, X's man 3, seat 2 | 2 | MD DKG(S) 15, Harappa F Trench I 10 | 6 vs 1.62 (P 0.020) |
| 2 | Bamboo-star | 235 | *vēymīn* | 61 | 2 | 100 | 8 | house of 34, gate-guard 8, chief 7 | 3 | MD DKG(S) 14, DK 9, HR-B 7 | 8 vs 3.80 (P 0.069) |
| 3 | Tax | 176 | *iṟai* | 26 | 1 | 88 | 5 | house of 16, keeper 2, junior 2 | 1 | Harappa F Trench I 25 | 3 vs 0.71 (P 0.050) |
| 4 | Kalam | 705/706 | *kalam* | 30 | 1 | 69 | 7 | house of 12, chief 7, keeper 3 | 0 | MD DKG(S) 11, Lothal SRG 3GX 10 8 | 1 vs 1.61 |
| 5 | Home | 803 | *il* | 38 | 0 | 63 | 9 | house of 18, chief 10 | 4 | MD DKG(S) 11, Harappa F Granary 7 | 0 vs 1.45 |
| 6 | Bounty | 806 | *viḷai* | 27 | 0 | 61 | 3 | house of 14, chief 5 | 0 | MD DKG(S) 13, DK 10 | 0 vs 0.85 |
| 7 | Hill | 503 | *malai* | 16 | 0 | 60 | 3 | house of 13 | 0 | MD DK 14, DKG(S) 9 | 0 vs 0.29 |
| 8 | Branch | 415 | *kavar* | 23 | 0 | 56 | 10 | house of 8, chief 6 | 2 | MD DKG(S) 7, Harappa E Trench 11 6 | 1 vs 0.87 |
| 9 | Star | 220 | *mīn* | 20 | 0 | 56 | 7 | house of 5, chief 5, keeper 2 | 0 | MD DKG(S) 11 | 0 vs 0.34 |
| 10 | Lady | 140 | *ammai* | 31 | 2 | 50 | 5 | house of 10, X's man 2 | 0 | MD DKG(S) 13, HR-B 4 | 2 vs 1.07 |
| 11 | Chief | 255 | *mutal* | 11 | 0 | 45 | 7 | house of 7 | 1 | Harappa F Trench I 4, E Trench 10W/11 4 | 0 vs 0.21 |
| 12 | Bright-star (scabbard-fish) | 233 | *vāḷai* | 29 | 2 | 44 | 5 | house of 18, chief 5, X's man 2 | 4 | MD DKC 5, DKG(S) 4 | 1 vs 1.15 |
| 13 | Descendant (Maru) | 798 | *maru-* | 23 | 0 | 40 | 5 | house of 12, chief 4, seat 2 | 0 | MD DKG(S) 7 | 0 vs 0.51 |
| 14 | Peer | 840 | *iṇai* | 17 | 1 | 37 | 6 | house of 11 | 1 | Harappa F Trench I 4, MD DKG(S) 4 | 0 vs 0.44 |
| 15 | First-star | 231 | *orumīn* | 15 | 0 | 34 | 3 | house of 6, chief 4 | 1 | MD DKG(S) 4, HR 3, DKC 3 | 0 vs 0.32 |
| 16 | Quarter | 061 | *kāl* | 24 | 3 | 33 | 7 | house of 15, keeper 4, X's man 3 | 1 | MD DKG(S) 10 | 1 vs 0.53 |
| 17 | Moon | 900 | *tiṅkaḷ* | 19 | 1 | 29 | 6 | house of 13 | 1 | Harappa F Trench I 4, MD DKG(S) 4 | 0 vs 0.08 |
| 18 | Dark-star | 032+220 | *iru-mīn* | 17 | 1 | 25 | 6 | house of 10, chief 2 | 0 | MD DKG(S) 6 | 0 vs 0.13 |
| 19 | Chest | 590 | *peṭṭi* | 17 | 0 | 24 | 6 | house of 10 | 1 | MD DKG(S) 5 | 0 vs 0.17 |
| 20 | Gate | 550 | *vāy* | 14 | 0 | 24 | 5 | gate-guard 4, house of 3 | 2 | MD DKG(S) 5 | 0 vs 0.12 |
| (24) | Boxed-cotton | 590-390 | *peṭṭi-parutti* | 15 | 0 | 22 | 6 | house of 7, keeper 2 | 0 | Harappa F Granary, E Trench 11 | |

Boxed-cotton is added because the brief names it; with an ending required it ranks 24th (masters.md counted 71 objects carrying the pair in any position). Full columns (all areas, buildings, stand letters, date bins, object ids, agents' ids) in `great_houses.csv` and `houses.csv`.

What the table says (`measured` unless marked):
- The fish-star houses (High-star, Bamboo-star, Bright-star, First-star, Star, Dark-star) are 6 of the 20 and keep 8 of the 17 agents the top 20 keep. Every great house is in both Mohenjo-daro and Harappa, and all have objects in all three date bins.
- The houses split into two kinds by what carries their name. Seal houses: Bamboo-star (68 seals of 100 objects), Home, Lady, Bright-star. Record houses, named mostly on tablets and copper tablets: Tax (55 tablets of 88, 25 in Harappa F Trench I), Hill (32 copper tablets of 60: the `503-615-752` copper office), Bounty (21 copper tablets), Chief (24 tablets), High-star (64 tablets). `guess`: the record houses are the ones that ran stores.
- Kalam is the Lothal warehouse house: 15 tags, 8 of them in SRG 3GX 10, the warehouse trench (the dozen-fish agent tag `705-500-741-001-055-220-740-090`).
- Gate-guard is the Bamboo-star rank: 8 of the 25 gate-guards in the registry are Bamboo-star.
- Seal size and stand letter: the large-format stand W leads in High-star (13 of 28 letters), Bamboo-star (18 of 35), Home (13 of 23) and Descendant (9 of 11).

## 3. The tests, each with the prediction written first

| test | prediction | result | way |
|---|---|---|---|
| G clustering | same-house pairs share a building / block above shuffle | building 23 vs 16.3 (1.41, P 0.080); block 48 vs 51.8 (0.93); area 0.93; Harappa area 1.16 (P 0.28) | building: with; block, area: against |
| a agents away | agents away from the master's building more than members | agents away 22 of 27 (81%) against members 570 of 622 (92%), P 0.98 the predicted way | against (agents are closer) |
| a redesign | shuffle test, agents' buildings shuffled within city | MD agents 5 of 24 with their crest's owners vs 2.10 (2.38, P 0.046); members 44 vs 49.5 (0.89) | the opposite of the prediction, and strong |
| a new idea | agent = house manager: bigger seals | 718 vs 620 mm2 (P 0.044), vs all owners 581 (P 0.016) | with |
| b goods words | trade-named houses carry their goods outside the name (ending-closed goods objects) | Boxed-cotton 0 of 6; grain houses 0 of 49; Chest 0 of 5; Kalam 5 of 33 vs 39.5% | against |
| b redesign | any object with the house name, cup left out | Bounty grain 17% vs 5.7% (P 1.4e-5); Kalam store 26% vs 12.7% (P 6e-7); Chest 17% vs 12.8% (P 0.063); Boxed-cotton 7% vs 5.5% (P 0.36); Grain-heap 2% vs 7.3%; Granary 0 of 15 | with for Bounty, Kalam, Chest; against for cotton, Grain-heap, Granary |
| b new idea | trade houses put more objects on goods than star houses | 43% vs 41% (P 0.30); distinct texts 26% vs 29% | against |
| c crest not tag | same crest pairs neighbours, same tag (different crest) at chance | MD building: crest 1.43 (P 0.056), tag 1.11 (P 0.35), personal part 2.00 (3 vs 1.5, P 0.20); Harappa area: tag 1.68 (P 0.011) | with at Mohenjo-daro; against at Harappa |
| d seal and tablet | goods object with the seal's full name in the seal's area | MD 22 vs 17.4 (1.26, P 0.16); Harappa 11 vs 11.3 (0.98); building and block at chance | against |
| d redesign | rare names only (on 3 seals or fewer) | MD 4 vs 2.58 (1.55, P 0.24); Harappa 0 vs 1.43 | against |
| d new idea | a name has a desk: different texts with one name in one area | Harappa tablets 18 vs 13.0 (1.39, P 0.12); MD tablets 1 vs 1.72; seals 0.84 and 0.67 | against (Harappa tablets lean with) |
| e allied / kindred | linked houses share areas and cities | first build (690 counted as a crest by mistake): area 0.83, city 1.05 | against |
| e redesign | link sign between two crests | 5 linked pairs on 30 objects; area 1.05 (P 0.41); city overlap 0.563 vs 0.423 (1.33, P 0.042) | cities: with; areas: against |
| e new idea | link names are records, not seals | tablets 26 of 30 (87%) vs 193 of 771 (25%), P 7e-12 | with, but 26 are two moulded texts |
| offices | one king house per city | Mohenjo-daro 13 crests on 22 king objects; Harappa 4 on 12 | against; the quarter-king finding instead |

## 4. The offices (from `offices.csv`)

People = seals in the registry; objects = every undamaged named object of any kind.

| office | sound | people | objects | cities (objects) | houses holding it most (people) |
|---|---|---|---|---|---|
| chief (spear 520) | *vēḷ* | 114 | 222 | MD 104, Harappa 88, Dholavira 9, Lothal 5, 9 more | Home 10, Kalam 7, High-star 7, Bamboo-star 7, Branch 6 (49 houses) |
| keeper (151-161) | *kā* | 62 | 100 | MD 46, Harappa 35, Dholavira 7 | King 5, Quarter 4, Kalam 3, Bondsman 3, Grain-heap 3 |
| junior (comb 400) | *ciṟ* | 45 | 349 | Harappa 280, MD 59 | 41 houses |
| agent, X's man | *āḷ* | 41 | 96 | MD 44, Harappa 34, Lothal 13 | High-star 3, Quarter 3, 853 3, Bright-star 2, Lady 2, Bamboo-star 2 |
| gate-guard (550/555 + 527) | *vāy kāval* | 25 | 42 | MD 24, Harappa 13, Lothal 5 | Bamboo-star 8, Gate 4 |
| guard (525-527) | *kāval* | 6 | 12 | MD 5, Harappa 4 | |
| standard-bearer (368 last) | *koṭi* | 15 | 26 | Harappa 13, MD 11 | 14 houses, Hunter 2 |
| seat / throne (jar + 679) | *kaṭṭil* | 10 | 9 | MD 8, Harappa 1 | High-star 2, Descendant 2, Great-measure 2 |
| deputy (842) | *tuṇai* | 1 | 2 | Chanhu-daro, MD | |
| king (142) | *kō* | 28 | 39 | MD 22, Harappa 12, Dholavira 3, Lothal 1 | the King name itself 13, Quarter 6 |
| king's servant (617) | *ūḻiyaṉ* | 25 | 39 | MD 24, Harappa 13 | 617 7, King 5, Gate 3 |
| servant (717) | *aṭi* | 23 | 39 | MD 18, Harappa 14 | |
| bondsman (097/136) | *aṭimai* | 10 | 22 | MD 14, Harappa 6 | |
| cultivator (137) | *vēḷāḷaṉ* | 0 | 8 | Harappa 7, MD 1 | only on goods objects |
| royal (384/388/382) | *aracu* | 30 | 66 | MD 34, Harappa 23, Dholavira 4 | the royal name itself 11, Kalam 3 |
| chief (255) | *mutal* | 37 | 98 | Harappa 46, MD 43 | |
| elder (100/101) | *mutu* | 53 | 100 | MD 57, Harappa 34 | Branch 8, High-star 6 |
| tax (176) | *iṟai* | 51 | 175 | Harappa 103, MD 58 | |
| first ward (741) | *orukuṭi* | 87 | 160 | 12 cities | 57 houses |
| second ward (742) | *irukuṭi* | 23 | 27 | MD 18, Harappa 5 | |
| third ward (745) | *mukuṭi* | 12 | 22 | MD 13, Harappa 8 | |
| assembly (692) | *kūṭṭam* | 29 | 48 | MD 23, Harappa 22 | 17 houses |
| 7-city office opening 920-060-741 | | 21 | 27 | MD 18, Harappa 2, Lothal 2, Dholavira 2, 3 more | 19 different houses |

Read (`guess` on `measured` counts): chief is the common rank of the great houses (49 houses hold it); junior is the rank that writes the Harappa tablets (280 of its 349 objects); gate-guard belongs to Bamboo-star; the 7-city office is held by people of 19 different houses, so it is an office open to many families, not one house's property. **The Dholavira signboard's name** (umbrella 611, 6 uses): the signboard and Lothal L-116 write it as "quarter: Umbrella" (Gujarat both); at Harappa it sits in the Kalam house (H-1076 `820-002-706-611-740`, "of the Kalam-Umbrella house") and in a Field name (H-3, F Granary, `703-615-611-002-017-585-740`); at Mohenjo-daro after Peer (M-56). No single house holds it; the nearest is the Kalam house (`measured` placements, `guess` reading).

## 5. What went against, and the rescues

- **Agents posted away (a): against.** Agents were away from their master's building less often than members (81% against 92%). Rescue 1 (redesign, shuffle within city) turned it into a finding: agents sit with their crest's owners 2.38 times chance (P 0.046). Rescue 2 (new idea, the agent is the house manager) came true on size (P 0.016). The "posted out servant" reading is paused at the building level; "manager of the house" goes up.
- **Goods words (b): against as first built, half rescued.** Ending-closed goods objects carry almost no goods words outside the name (0 of 49 grain-house objects). Redesign: any object with the name, cup left out: Bounty and Kalam carry their goods (P 1.4e-5, 6e-7), Chest leans (P 0.06); Boxed-cotton, Grain-heap and Granary do not. New idea (trade houses do more paperwork) went against (43% vs 41%). Boxed-cotton stays read as cotton from the earlier jobs; its own objects say nothing more here.
- **Same name on seal and tablet (d): against three times** (all objects, rare names, the "desk" idea). Paused for now; reason in one line: names are inherited across six centuries (`history.md`), so a seal and a tablet with one name are two holders of a family name, not one man's seal and his receipt. The Harappa tablets lean towards a desk (1.39, P 0.12); next way in: the same name and the same cup count on two tablets.
- **Allied and kindred (e): areas against, cities with.** The first build counted 690 itself as a crest (bug, fixed in the redesign). With the link between two crests there are only 5 linked pairs on 30 objects (the Bounty-Share copper tablets `806-845-061-407-850-900`, 15; the Harappa tablet `803-415-220-318-920-255-436-690-590-407-740`, 11; three seals). Linked houses share cities 1.33 times chance (P 0.042), not areas. Read: an alliance joined houses of different cities, written on records. Grow the sample: the second catalogue.
- **Clustering at block and area level: against** (0.93). A house is one building, not a quarter of the city.
- **Tag at Harappa: against** test c (same-tag pairs share a trench 1.68, P 0.011). Kept as a lead: at Harappa the tag marks the work trench.
- **One king per city: against.** Replaced by the quarter-king finding (section 1.2).

## 6. What it opens

- Agent seals are house markers: map every agent seal's building as the seat of its master's family (5 placed now).
- Quarter-kings: list every `061/820 + 142/611` text with its findspot; the prediction is one Quarter-King name per excavation area, and the Dholavira signboard's quarter in the Castle.
- Bounty and Kalam as trade houses: their copper tablets and tags are their own stock records; Bounty-Sheaf `806-845` on 14 copper tablets is the produce house's crop record.
