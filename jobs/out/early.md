# Early: before the fish houses, and before the cities

Scripts in `work_scripts/` (each has its predictions in the top docstring; rerun with `python3`): `early_1_levels.py` (levels for the second catalogue, the earliest level of the Mohenjo-daro dig), `early_2_precity.py` (writing before the cities), `early_3_order.py` (order of first appearance), `early_4_areas.py` (the same fish test in the other Mohenjo-daro areas), `early_5_carry.py` (endings, animals, stands, crest slot). Tables and logs in `work_data/early/` (`dkg_union_levels.csv`, `early_level_read.csv`, `early_level_seals.csv`, `precity_objects.csv`, `precity_stage_*.csv`, `order_of_appearance.csv`, `order_first_objects.csv`, `order_named_objects.csv`, `areas_deep_vs_upper.csv`, `log_1.txt` to `log_5.txt`).

Terms in plain words:
- **Level / DK-G Early I**: DK-G is the long dug area at Mohenjo-daro that the earlier history job used. Mackay cut it into seven levels from the bottom (Early I, about 20.5 to 30.5 ft down) to the top (Late I). Level 0 below = Early I, 1 = Intermediate III, 2 = Intermediate II, 3 = Intermediate I, 4 = Late III, 5 = Late II, 6 = Late I. Early I is dated to Harappa Period 3B-2 by the catalogue (about 2450 to 2200 BC, [harappa.com chronology](https://www.harappa.com/beas/chronology)).
- **Fish crest first**: a marked fish sign (231, 233, 235, 240, 236) is the first sign of the name, the family-crest slot. **Clean** = no lost (broken-off) sign stands in front of it, so nothing could hide a different first sign. **Any marked fish** = one of those signs anywhere in the name.
- **Agent**: a seal ending `X jar man`, "X's man". **Office opening**: the three signs `920-060-741`. **Boxed-cotton**: the pair `590-390`. **Overseas bull**: the short-horned bull seal picture, common on seals found abroad.
- **Stage**: a rank on the history job's time axis: before the cities (Harappa Periods 1 and 2, Dholavira stages I and II), then 3A (2600 to 2450 BC), 3B-1, 3B-2 (to 2200 BC), 3B/C, 3C-1, 3C-2, 3C-3 and later.
- **Fisher P**: the chance of a split at least this lopsided if the two groups were alike. Small = the groups differ. **Binomial P**: the chance of this few (or fewer) in the early group if it had the later groups' rate.

## 1. What was found

**1. The second catalogue does carry a level: it is the find depth in feet, and its locus codes 31 and 32 are the DK-G area.** Mahadevan's `level` column is a whole-number depth below the datum (0 = not recorded). On 346 seals matched by text to the first catalogue, level and the first catalogue's depth agree to the foot (r -0.98, level + depth averages -0.07 ft). Locus 31 matches DK-G South (139 matched seals) and locus 32 DK-G North (39). Cut at the first catalogue's own boundaries, the depth bands reproduce Mackay's level on 618 of 628 first-catalogue DK-G seals (98%) and Early I is exactly "20.5 ft and deeper" (36 of 36 in, 0 outside). That gives 626 second-catalogue DK-G seals a level. The second catalogue has no stratum or period field; only locus, depth, line number, object class and picture code.

**2. Most of those seals are the same stones.** By depth within 1 ft plus text alignment, 589 of the 626 are the same stone as a first-catalogue seal (94%); 150 of the 179 seals the crosswalk calls "new texts" are re-transcriptions of first-catalogue stones with a lost sign filled in or a sign read differently. Only 37 are extra stones, 2 of them at the earliest level. So the second catalogue is a second reader of the earliest level, not a second sample of it: it replicates, and the replication is the result in 3.

**3. The earliest level again has no fish crest in the first slot. Prediction E1 (written first): at most 2 extra seals with it, union rate under 4%. Number: clean fish-crest-first is 0 of 36 (first catalogue), 0 of 36 (second catalogue), 0 of 38 (union of both with the 2 extra stones), against 11.0 to 11.8% at the later levels (Fisher 0.040 / 0.042 / 0.042; binomial chance of 0 of 35 named seals at the later rate 0.0125).** Counting a fish that has a lost sign in front of it as first, the numbers are 1 of 36, 2 of 36 and 2 of 38 (5.3%, over my 4% line; the two are the same stone M-771 `000-233-690-740` and an extra stone `000-233-220-740-000`, each with a broken sign where a different first sign could stand). The count of 0 stands in both catalogues.

**4. The fish are there, in the wrong slot: they stand inside long stacked names, never first.** Prediction E4 (any marked fish also rarer at the earliest level) went against: 7 of 38 earliest seals carry a marked fish in the name (18.4%) against 143 of 757 later (18.9%, Fisher 1.0). What differs is position: among names that hold a marked fish, 0 of 7 have it clean-first at the earliest level against 65 of 120 later (54%, Fisher 0.0055); positions in the seven earliest names are 0 (behind a lost sign), 0 (same), 1, 2, 2, 3, 4. Three of the seven fish names have six or more name signs against 9 of 120 later (Fisher 0.018). The two oldest fish-house stones share a tail: M-1691 (26.9 ft) `906-741-240-255-435-690-740` and M-369 (23.6 ft) `920-060-742-806-415-220-240-255-435-690-740`, "of the ... High-star, Chief, Rod, Ally house" (240 = whiskered fish, 255-435-690 = the Chief-Rod-[690] lineage). The full tail `240-255-435-690-740` occurs only at this level (2 seals in DK-G, both Early I), while its core `255-435-690` runs on through 34 objects in all three time bins (6 early, 7 middle, 7 late, Mohenjo-daro 24, Harappa 8). Reading it points toward: the oldest visible fish house is `[High-star] Chief Rod Ally`, written behind a stack of prefixes (a ward, an office, "Bounty-Branch-Star"); the "crest leads the name" convention is a later arrangement of the same kind of name. It opens: follow `240-255-435-690` through every level; it is the first fish house with a lineage in the dig.

**5. What stands in the crest slot at the earliest level.** In the first catalogue's 36 earliest seals, 33 have a name; their 32 distinct first name signs include lady 140 (twice), plain fish 220 ("One Star"), manager 090, hill 503, quarter 061 and day 165, and 27 of the 32 also open names at later levels; 5 appear only at this level (132, 903, 495, 386, 541, one seal each). So the slot is filled by the same families that persist, not by a separate early set. In the union the scabbard-fish `233` first-slot cases are the two lost-sign ones from finding 3.

**6. Endings, animals, stand patterns (first catalogue, 36 earliest seals against 592 later).** Endings are the same mix: jar 47% against 39%, none 36% against 39%, spear 8% against 8%, porter 6% against 7%, comb 3% against 3%, agent 0 against 3.5%. The unicorn is on 56% against 59% (Fisher 0.73). What differs is the picture: rare creatures (rhino 2, buffalo 1, goat 1, other 2, unknown 1) are 7 of 36 (19%) against 25 of 592 (4.2%), Fisher 0.0013; the standard-bearing stand is on 8 of 36 (22%) against 254 of 592 (43%), Fisher 0.015; no stand 56% against 39% (0.054). The second catalogue's picture codes lean the same way, weaker (pictures other than unicorn, short-horned bull, humped bull or none: 8 of 36 against 69 of 590, Fisher 0.069; its codes count elephants and tigers as "other", which fills the later group). Reading it points toward: the written template was in place before the seal pictures were standardized; the unicorn-plus-standard format was fixed after Early I.

**7. When the fish crests arrive they arrive with the agent, not with the office or the overseas bull. Prediction E3 held.** In DK-G (union), level 0 to level 1: crest-first fish 0 of 35 named seals to 12 of 95; agent (`X jar man`) 0 of 21 jar-or-spear seals to 6 of 51. The office opening (1 seal), Boxed-cotton (1), the overseas bull (2) and the star name (3) are already on level 0. At Harappa the pair is also joint and in the first big stage: the 3B tablets hold four distinct crest-first texts (`240-760-740`, `240-636-740`, `235-242-740`, `235-240-740-090`) and four distinct agent texts (`792-740-090`, `347-741-176-740-090` on four copies, `327-740-090`, the same `235-240-740-090`). One text, `235-240 jar man`, is both an agent and a fish house. Order of first appearance is in section 2.

**8. Before the cities, 25 of 38 inscribed objects are counts, and the jar is already there.** The pre-city set is 38 objects (Harappa Periods 1 and 2: 32 pots, 2 tags; Dholavira stages I and II: 2 seals, 1 tag; Rehman Dheri 2 and Kalibangan period I 1, by the catalogue's own labels). A number stroke is on 22; with the cup 700, 25 (66%); a goods sign on 5 (wheat shaft 411 x4, grain 413, cotton tree 390; none with a jar); a house word on 5 (jar 740 on 3, plain fish 220 on 2, whiskered fish 240 on 1); 24 of 35 Harappa/Dholavira texts are one sign long; a text of 5 or more signs is only the Dholavira stage I seal. **All ten stroke signs (short 1 to 5, tall 1 to 5) are on pots.** On pots, tall strokes outnumber short 13 to 6, the container-counting style (the first catalogue's measured later rule: tall strokes for containers, short for living things). 4 pots carry the cup (3 alone, 1 as cup + one tall stroke, the "One cup" pot). Predictions P1 to P5 held (section 6).

**9. Counting is the same size before and after the cities; the house words are what is added.** Number strokes: 20 of 35 before the cities against 1,143 of 2,122 after (Fisher 0.74). Jar: 3 of 35 against 896 of 2,122 (Fisher 1.9e-5); any fish sign 2 of 35 against 528 of 2,122 (0.0053); marked fish crest 1 of 35 against 336 of 2,122 (0.033). Pots against pots the jar is 2 of 31 against 17 of 108 (0.24) and the number stroke 18 of 31 against 43 of 108 (0.10): the big rise in jar and fish comes with seals and tablets, the objects that carry names (jar on 26 of 53 3A-3B seals, 49%), not on pots. Reading it points toward: accounts first, owners' names added when sealing and tablets started. The first object with a name before the jar is a 3B-1 Harappa chit `605-760-740-400` ("Granary, child of, house, junior"); a name before the jar is on 0 of 35 pre-city objects.

**10. The jar is among the earliest signs, so "names later" is not the whole of it.** Harappa Period 1 has `000-740` (a lost sign, then the jar) and Period 2 has `740-000` on a tag and `900-740-000` ("[moon] house") on a pot. Published: [Kenoyer 2020](https://www.harappa.com/sites/default/files/pdf/Kenoyer2020%20Origin%20of%20Indus%20Script.pdf) says sign 342, "the most common script sign" later, appears in Periods 1 and 2 (342 is the first catalogue's jar 740 by the crosswalk) and is "combined with another sign (Mahadevan sign 347)" (347 = Lipi 760, "child of"). The same pair, `760-740`, is a whole text at the earliest dig level (M-1010, 22.2 ft). The same moon-plus-jar form: Harappa Period 2 pot `900-740-000` and Mohenjo-daro Early I seal M-893 `004-900-740` ("Four-Moon house"). It opens: the house-of formula is the oldest piece of the seal template, and numbers plus jar are the whole pre-city kit; names are what is put in front of the jar.

**11. The earliest seal texts are accounts first, even on seals.** The oldest seal texts in the corpus are account lines, not names: Dholavira stage I (about 2650 to 2550 BC by the repository's placement) `104-031-002-423-001-003-423`, a person sign then 1-2 and 1-3 of one counted thing [423] written twice; Dholavira stage II `817-002-004-390`, "two shares, four, cotton", the same `002-004-390` line the Umma sealing ends with (`outside_match.md`). At the earliest Mohenjo-daro level 5 of 38 seals carry the cotton tree (M-1911, M-708, M-851, M-1365 "Six cottons", M-95 "Five cottons"). The cotton lot line is as old as the oldest seal texts.

**12. The template grew in parts on top of a counting-and-jar kit, and nearly all of its parts are in the first large dated mass.** Of the 19 features tracked (section 2), 9 are first seen before the cities (number strokes, cup, goods, jar, plain fish, a marked fish on a Dholavira tag, the shares opener on a Dholavira seal, and seals with or without an animal), 3 at 3B-1 (a name before the jar, "child of", the comb) and 7 at 3B-2 (spear, crest-first fish, agent, office, cotton house, kalam, overseas bull); crest-first fish and the overseas bull become solid one stage later (3B/C), and inside the Mohenjo-daro dig crest-first fish and agents join one level above Early I. The story is in section 5.

## 2. Order of first appearance

Counts are objects with the feature / objects dated to the stage (all sites; `order_of_appearance.csv`). First seen = first stage with one object; first solid = first stage with at least 3 objects and at least 1% of the stage. Only 7 objects are dated to 3A and 3B-1 together (2 and 5), so first solid cannot fall there: the first large dated mass after the pots is 3B-2 (167 objects: Harappa 110, Mohenjo-daro 45, others).

| Feature | before cities | 3A | 3B-1 | 3B-2 | 3B/C | 3C-1 | 3C-2 | 3C-3+ | first seen | first solid |
|---|---|---|---|---|---|---|---|---|---|---|
| a number stroke | 20/35 | 1/2 | 1/5 | 90/167 | 391/683 | 145/253 | 226/455 | 289/557 | before cities | before cities |
| the cup 700 | 4/35 | 1/2 | 2/5 | 43/167 | 226/683 | 30/253 | 47/455 | 34/557 | before cities | before cities |
| a goods sign (413, 411, 390, 806) | 4/35 | 1/2 | 0/5 | 21/167 | 57/683 | 21/253 | 45/455 | 72/557 | before cities | before cities |
| the jar 740 ("house of") | 3/35 | 0/2 | 2/5 | 80/167 | 309/683 | 120/253 | 148/455 | 237/557 | before cities | before cities |
| the plain fish 220 | 2/35 | 0/2 | 0/5 | 19/167 | 57/683 | 28/253 | 55/455 | 64/557 | before cities | 3B-2 |
| a marked fish crest sign, anywhere | 1/35 | 0/2 | 0/5 | 17/167 | 92/683 | 46/253 | 76/455 | 105/557 | before cities (Dholavira tag) | 3B-2 |
| diamond + two-strokes opener (seals) | 1/2 | 0/1 | 0/2 | 8/50 | 21/205 | 21/169 | 18/231 | 48/434 | before cities (Dholavira seal) | 3B-2 |
| a name before the jar | 0/35 | 0/2 | 2/5 | 58/167 | 252/683 | 108/253 | 117/455 | 217/557 | 3B-1 | 3B-2 |
| "child of" 760-740 | 0/35 | 0/2 | 1/5 | 6/167 | 16/683 | 9/253 | 8/455 | 24/557 | 3B-1 | 3B-2 |
| comb 400 last (junior) | 0/35 | 0/2 | 2/5 | 23/167 | 158/683 | 35/253 | 28/455 | 42/557 | 3B-1 | 3B-2 |
| spear 520 last (chief, seals) | 0/2 | 0/1 | 0/2 | 4/50 | 13/205 | 15/169 | 18/231 | 31/434 | 3B-2 | 3B-2 |
| fish crest first (seals) | 0/2 | 0/1 | 0/2 | 1/50 | 15/205 | 17/169 | 25/231 | 37/434 | 3B-2 (M-771, lost sign before it) | 3B/C |
| agent `X jar man` | 0/35 | 0/2 | 0/5 | 9/167 | 21/683 | 4/253 | 8/455 | 17/557 | 3B-2 (Kalibangan K-55 seal) | 3B-2 |
| office opening `920-060-741` | 0/35 | 0/2 | 0/5 | 2/167 | 5/683 | 1/253 | 6/455 | 3/557 | 3B-2 (M-974) | 3C-2 |
| Boxed-cotton `590-390` | 0/35 | 0/2 | 0/5 | 3/167 | 8/683 | 7/253 | 6/455 | 9/557 | 3B-2 (Harappa H-533) | 3B-2 |
| kalam / ship sign 705 or 706 | 0/35 | 0/2 | 0/5 | 5/167 | 45/683 | 15/253 | 20/455 | 34/557 | 3B-2 (M-355) | 3B-2 |
| overseas short-horned bull (seals) | 0/2 | 0/1 | 0/2 | 2/50 | 6/205 | 9/169 | 13/231 | 14/434 | 3B-2 (M-1090) | 3B/C |
| seal with animal and text | 1/2 | 1/1 | 2/2 | 42/50 | 176/205 | 146/169 | 174/231 | 328/434 | before cities | 3B-2 |
| seal with text only | 1/2 | 0/1 | 0/2 | 8/50 | 29/205 | 23/169 | 57/231 | 106/434 | before cities | 3B-2 |

Read down the "first seen" column: numbers, cup, goods, jar, plain fish: before the cities. Name before the jar, "child of", comb: 3B-1 (Harappa tablets). Everything else on the list, spear, agent, office, cotton house, kalam, overseas bull, crest-first fish: 3B-2, the first stage with more than a handful of dated objects, with the crest-first fish and the overseas bull reaching a solid footing one stage later (3B/C). Against prediction O1 (office and overseas bull last): they are not last, they are in 3B-2 with the rest. O2 held (agent and office absent before 3B-2). The jar is on 80 of 167 objects at 3B-2 (48%) and on 33 to 47% at each later stage: the jar-and-name objects reach their working share in the first stage that has enough objects to count.

The same order inside one dig, DK-G at Mohenjo-daro by level (first catalogue seals plus the 2 extra stones, `dkg_union_levels.csv`; median depth in feet, "named" = seals with a name):

| Level | median ft | seals | named | crest first (clean) | any marked fish | agent | jar ending | office | Boxed-cotton | overseas bull | star name |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 Early I | 21.8 | 38 | 35 | 0 | 7 | 0 | 18 | 1 | 1 | 2 | 3 |
| 1 Intermediate III | 17.9 | 114 | 95 | 12 | 19 | 6 | 43 | 3 | 3 | 2 | 18 |
| 2 Intermediate II | 14.7 | 97 | 89 | 11 | 14 | 0 | 43 | 1 | 2 | 6 | 10 |
| 3 Intermediate I | 11.6 | 132 | 119 | 15 | 36 | 4 | 50 | 3 | 4 | 15 | 10 |
| 4 Late III | 8.4 | 153 | 136 | 13 | 24 | 6 | 72 | 0 | 3 | 7 | 16 |
| 5 Late II | 6.1 | 75 | 66 | 8 | 16 | 4 | 32 | 2 | 0 | 4 | 10 |
| 6 Late I | 4.3 | 56 | 47 | 6 | 11 | 1 | 20 | 1 | 0 | 1 | 9 |

(The "star name" column counts a number sign directly before a fish; its level-1 value of 18 compares with 3 at level 0.)

## 3. The earliest-level seals, read whole

All 38 seals at 20.5 ft and deeper in DK-G: the 36 first-catalogue Early I seals plus the 2 extra second-catalogue stones (last two rows). Sounds and English are the repository's reading rules (`corpus_english2.csv`, same rules applied to the two extra stones); `[n]` is a sign with no sound yet, `[lost]` a broken-off sign. Rows run from the deepest up (`early_level_read.csv`).

| Object | ft | Signs | Sounds | English |
|---|---|---|---|---|
| M-669 | 30.5 | 000-368-090 | [lost] koṭi āḷ | [lost sign]-Banner, manager. |
| M-1691 | 26.9 | 906-741-240-255-435-690-740 | [906] orukuṭi mīmīn mutal kōl piṇai kuṭi | Of the [906]-First-ward-High-star-Chief-Rod-Ally house. |
| M-1911 | 25.4 | 820-002-531-390-621 | kāl iru [531] parutti [621] | two quarters: [531]-Cotton-[621]. |
| M-1324 | 24.4 | 000-806-155 | [lost] viḷai kā | N loads of produce, carried by the porter. |
| M-715 | 24.0 | 000-556-741-016-220-520 | [lost] [556] orukuṭi āṟu mīn vēḷ | [lost sign]-[556]-First-ward-Six-Star, chief. |
| M-58 | 23.8 | 817-002-503-460-740 | kāṇi iru malai [460] kuṭi | two shares: of the Hill-[460] house. |
| M-201 | 23.7 | 061-151 | kāl kā | Quarter, keeper. |
| M-1273 | 23.7 | 603-861-002-055-740 | [603] kāṇi iru paṉṉiru kuṭi | Of the [603] two shares Twelve house. |
| M-1899 | 23.6 | 861-002-132-924 | kāṇi iru [132] [924] | two shares: [132]-[924]. |
| M-369 | 23.6 | 920-060-742-806-415-220-240-255-435-690-740 | tiṅkaḷ? uḷ irukuṭi viḷai kavar mīn mīmīn mutal kōl piṇai kuṭi | month in second ward: of the Bounty-Branch-Star-High-star-Chief-Rod-Ally house. |
| M-771 | 23.4 | 000-233-690-740 | [lost] vāḷai piṇai kuṭi | Of the [lost sign]-Scabbard-fish-Ally house. |
| M-1090 | 22.8 | 741-130-000-235-220-520 | orukuṭi [130] [lost] vēymīn mīn vēḷ | First-ward-[130]-[lost sign]-Bamboo-star-Star, chief. |
| M-273 | 22.6 | 386 | [386] | [386]. |
| M-732 | 22.6 | 817-002-350-400-520 | kāṇi iru [350] ciṟ vēḷ | two shares: [350]-Junior, chief. |
| M-1010 | 22.2 | 760-740 | maka kuṭi | Of the Child of house. |
| M-1028 | 22.0 | 000-798-740 | [lost] maru- kuṭi | Of the [lost sign]-Descendant house. |
| M-807 | 21.8 | 000-000-055-740 | [lost] [lost] paṉṉiru kuṭi | Of the [lost sign]-[lost sign]-Twelve house. |
| M-829 | 21.8 | 000-000-844-000 | [lost] [lost] [844] [lost] | [lost sign]-[lost sign]-[844]-[lost sign]. |
| M-1713 | 21.7 | 031-220-000-ALT-220 | oru mīn [lost] [lost] mīn | One Star; [lost sign]-[unclear sign]-Star. |
| M-708 | 21.6 | 140-390-002-061-740 | ammai parutti iru kāl kuṭi | Of the Lady-Cotton two quarters house. |
| M-1164 | 21.4 | 820-001-850-315-741 | kāl oru kāṇi [315] orukuṭi | one quarter: Share-[315]-First-ward. |
| M-1921 | 21.3 | 090-750-400 | āḷ [750] ciṟ | Manager-[750], junior. |
| M-1787 | 21.3 | 000-703-002-061-740 | [lost] [703] iru kāl kuṭi | Of the [lost sign]-[703] two quarters house. |
| M-269 | 21.3 | 495-615-740 | kompu vayal kuṭi | Of the Horn-Field house. |
| M-1367 | 21.2 | 362-861 | [362] kāṇi | [362]-Tribute. |
| M-851 | 21.1 | 817-002-590-390-740-621 | kāṇi iru peṭṭi parutti kuṭi [621] | two shares: [621] of the Boxed-cotton house. |
| M-893 | 21.1 | 004-900-740 | nāl tiṅkaḷ kuṭi | Of the Four-Moon house. |
| M-1365 | 21.0 | 016-390 | āṟu parutti | Six cottons. |
| M-95 | 20.9 | 165-111-002-003-390 | [165] [111] iru mū parutti | [165]-[111]; Five cottons. |
| M-210 | 20.9 | 903-861-368 | [903] kāṇi koṭi | [903]-Tribute, standard-bearer. |
| M-355 | 20.7 | 140-919-520-360-861-002-235-231-705-033-032-877-740 | ammai [919] vēḷ [360] kāṇi iru vēymīn orumīn kalam mū iru nālkāṇi kuṭi | Of the Lady-[919]-Chief-[360] two shares Bamboo-star-First-star five kalam Four shares house. |
| M-646 | 20.7 | 817-002-000-440-760-740 | kāṇi iru [lost] koḷ maka kuṭi | two shares: of the [lost sign] child of Received house. |
| M-1079 | 20.7 | 803-233-706-033-760-740 | il vāḷai kalam mū maka kuṭi | Of the House-Scabbard-fish three kalam Child of house. |
| M-939 | 20.6 | 550-527 | vāy kāval | Gate-Guard. |
| M-974 | 20.6 | 920-060-741-927-740 | tiṅkaḷ? uḷ orukuṭi [927] kuṭi | month in first ward: of the [927] house. |
| M-1134 | 20.6 | 541-813-595-820 | [541] [813] paṭṭaṟai kāl | [541]-[813]-Forge-Quarter. |
| Mah 2683 (second catalogue, extra stone) | 25 | 000-233-220-740-000 | [lost] vāḷai mīn kuṭi [lost] | [lost sign] of the [lost sign]-Scabbard-fish-Star house. |
| Mah 2673 (second catalogue, extra stone) | 23 | 384 | aracu | King. |

What the 38 say at a glance: 18 carry the jar (a house name), 3 end in the spear (chief), 2 in a porter, 1 in a comb, 0 in "X's man"; 5 carry the cotton tree; 2 open with the cap `920-060` (M-369, M-974) and 4 more carry a ward sign 741 inside the name (M-1691, M-715, M-1090, M-1164); 12 are one or two signs long; the deepest seal (M-669, 30.5 ft) is `[lost] banner manager`, with a man sign and no jar.

## 4. Writing before the cities: every object, and what it carries

The pre-city set (`precity_objects.csv`; first catalogue only, since the second catalogue has no period). Class: counting only = number strokes or the cup alone; goods = wheat shaft 411, grain 413 or cotton tree 390; house word = jar 740 or a fish; unnamed = a sign with no reading (698, 697, 893 have no drawing in the sign table).

| Object | Site | Kind | Date label | Signs | Class |
|---|---|---|---|---|---|
| no id | Dholavira | seal | Dholavira stage 1 | 104-031-002-423-001-003-423 | counting + unnamed sign |
| no id | Dholavira | tag | Dholavira stage 2 | 240-220-000-000-000 | house word |
| no id | Dholavira | seal | Dholavira stage 2 | 817-002-004-390 | goods sign |
| H-1522 | Harappa | pot | Period 1 | 411-411-411 | goods sign |
| no id | Harappa | pot | Period 1 | 000-740 | house word |
| no id | Harappa | pot | Period 2 | 700 | counting only |
| no id | Harappa | pot | Period 2 | 700 | counting only |
| H-1557 | Harappa | pot | Period 2 | 031 | counting only |
| no id | Harappa | pot | Period 2 | 033 | counting only |
| no id | Harappa | pot | Period 2 | 031 | counting only |
| H-1550 | Harappa | pot | Period 2 | 700-031 | counting only |
| no id | Harappa | pot | Period 2 | 413 | goods sign |
| no id | Harappa | pot | Period 2 | 000-ALT-000 | unnamed or lost only |
| no id | Harappa | pot | Period 2 | 032 | counting only |
| no id | Harappa | pot | Period 2 | 031 | counting only |
| no id | Harappa | pot | Period 2 | 035 | counting only |
| no id | Harappa | pot | Period 2 | 000-390 | goods sign |
| H-1545 | Harappa | pot | Period 2 | 893-031 | counting + unnamed sign |
| no id | Harappa | pot | Period 2 | 700 | counting only |
| no id | Harappa | pot | Period 2 | 001 | counting only |
| H-1538 | Harappa | tag | Period 2 | 740-000 | house word |
| H-1549 | Harappa | pot | Period 2 | 698 | unnamed or lost only |
| H-1544 | Harappa | pot | Period 2 | 900-740-000 | house word |
| no id | Harappa | pot | Period 2 | 698-000 | unnamed or lost only |
| no id | Harappa | pot | Period 2 | 697-031 | counting + unnamed sign |
| no id | Harappa | pot | Period 2 | ALT | unnamed or lost only |
| no id | Harappa | pot | Period 2 | 032 | counting only |
| no id | Harappa | pot | Period 2 | 003 | counting only |
| no id | Harappa | pot | Period 2 | 220 | house word |
| no id | Harappa | pot | Period 2 | 032 | counting only |
| no id | Harappa | pot | Period 2 | 004 | counting only |
| no id | Harappa | pot | Period 2 | 032 | counting only |
| no id | Harappa | pot | Period 2 | 001 | counting only |
| no id | Harappa | pot | Period 2 | 000-002 | counting only |
| H-1547 | Harappa | pot | Period 2 | 698-034 | counting + unnamed sign |
| Rhd-1 | Rahman-deri | seal | I | 031-520 | counting + unnamed sign |
| Rhd-269 | Rahman-deri | other | Early | 705 | unnamed or lost only |
| K-94 | Kalibangan | pot | Period 3A | 005-411 | goods sign |

The csv `precity_objects.csv` has the same 38 rows with the sign counts per class (`000` and `ALT` are lost or unclear signs; `700` is the cup, `740` the jar).

Sign inventory before the cities (26 different signs): all ten stroke signs (001-005, 031-035), the cup 700, the jar 740, plain fish 220, whiskered fish 240, wheat shaft 411, grain 413, cotton tree 390, and others: 698 (3), 423 (2), 104, 520, 705, 817, 900, 893, 697. The jar and the fish are the only owner-type words in the set.

What is published, to put the 38 beside the whole:
- Harappa Period 1 (Ravi phase) and Period 2 (Kot Diji phase), [Kenoyer 2020, pp. 221 to 230 and Table 2](https://www.harappa.com/sites/default/files/pdf/Kenoyer2020%20Origin%20of%20Indus%20Script.pdf): 16 post-firing graffiti from Period 1 and 175 from Period 2, of 1,218 marked sherds across all Harappa phases; graffiti of one to three signs; sign 342 in both periods. The catalogue holds 2 of the 16 (Period 1) and 30 of the 175 (Period 2) at Harappa, so its pre-city pots are about a sixth of what exists. The same paper: "Kot Diji" published one sherd with graffiti; Kalibangan has three sherds with sign 342 (and notes a later publication does not mention them, so they may be Mature); Balakot period I has "clear links" to the later script, most of all sign 342; Rehman Dheri has many marks, unquantified, and an ivory pendant with script; Nausharo and Mehrgarh marks are unquantified. It does not call any early sign a number, a count, or a goods sign; that classification is this job's. Single marks may identify a maker or batch, it says; multi-sign marks may be names.
- [harappa.com, Ravi and Kot Diji occupations](https://www.harappa.com/node/2996) and [the evolution of the script](https://www.harappa.com/blog/evolution-indus-script): Period 1 graffiti are mostly single signs, one with "three linked trident or plant shapes"; Period 2 sherds show two signs together; a Period 2 sealing with possible Early Indus script and an unfinished elephant seal blank.
- [harappa.com on Kot Dijian pre-firing marks](https://www.harappa.com/slide/kot-dijian-phase-symbols): single pre-firing potter's marks, 2800 to 2600 BC.
- Not reached: the Kenoyer and Meadow 2010 inscribed-objects paper (the harappa.com page lists a free PDF ["KenoyerMeadow 2010 Inscribed Objects from Harappa.pdf"](https://www.harappa.com/content/inscribed-objects-harappa-excavations-1986-2007) but the site refused automated downloads and the text was not retrievable; its period-by-period counts would settle the sherd tallies); any Padri inscribed sherd report (none found); the Dholavira graffiti paper (the academia page did not load); Kot Diji's own report beyond the one sherd; the Rehman Dheri sherd report (Durrani and others) beyond its title.

## 5. The story

What was written first: how many, in what, of what. Before 2600 BC, marks on pots are counts (22 of 38 carry a stroke number, all ten stroke signs; 4 the cup), a few goods names (wheat shaft, grain, cotton tree) and a few jar and fish marks; two of three jar marks are on pots with nothing else, and the jar is on a Period 1 pot. They are one sign long on 24 of 35. The number-stroke share is the same later as before (57% and 54%): counting did not grow, it stayed.

When owners' names appear: when sealing starts to carry a text. The first name before a jar is a 3B-1 Harappa tablet (`605-760-740-400`); by 3B-2 it is 58 of 167 dated objects (35%), and the share stays between 26% and 43% for the rest of the sequence (37%, 43%, 26%, 39% at the four later stages). Names are an addition to the counting kit, made with the jar, "child of" and the junior comb together.

When the great houses appear: after the first named seals, and written behind other words first. At the earliest Mohenjo-daro level a marked fish is in 18% of seals, the same share as later, but in the third to fifth place of a long stack or behind a broken sign, never clean-first (0 of 7). By the next level up (Intermediate III) the fish leads the name in 12 of 95 named seals (13%), and the agent `X jar man` stands on 6 of 43 jar seals (0 of 21 before), with the star-name (number + fish) going from 3 of 38 seals to 18 of 114. At Harappa the same pair, crest-first fish and agents, is in the 3B tablets together. The great houses were not founded as a separate institution later; their crest was moved to the front of the name, and their agents are first counted, at one step in the dig.

Whether the template was invented once or grew: it grew in two layers, and the second layer came fast. Layer one (counting kit on pots, with the jar) runs from the Ravi phase. Layer two, the seal and tablet template with name, jar, "child of", junior, chief, the share-and-quarter openers, the office prefix, the cotton house and the kalam word, is already complete in its parts at 3B-2, the first stage with more than a handful of dated objects (7 objects are dated to 3A and 3B-1 combined, so the data cannot say how long layer two took to form). Layer three, inside the dig at Mohenjo-daro, is the arrangement: crest-first names and agents appear together one level above the bottom, while the seal pictures (rare creatures 19% to 4%; the standard-bearing stand 22% to 43%) settle into the unicorn format over the same step. After that the system is flat for the remaining six levels, which is what the history job found. A plain account in one line: counted pot marks with a jar sign, then a fixed name-jar-title seal formula whose house names were still stacked, then the crest-first star houses with their agents, in a seal-picture format that was fixed at the same time.

## 6. What went against, and the rescue tried

- **E4, fish missing altogether at the earliest level: against.** 7 of 38 against 18.9% later. Rescue (new idea, position): the fish is there but stands in position 2 to 4 of long stacks, 0 of 7 clean-first against 65 of 120 later (Fisher 0.0055), three of the seven on six-sign-plus names against 9 of 120 (0.018). That came true and is finding 4.
- **E1, rate under 4%: against in its loose form.** With a lost sign in front counted as first, 2 of 38 is 5.3%; the clean form is 0 of 38. Both are given.
- **The fish gap is one trench, not the town.** Redesign (`early_4_areas.py`, the deepest third of each of the other Mohenjo-daro areas, depth never compared across areas): first catalogue deep third 19 of 118 (16.1%) against upper 33 of 238 (13.9%), shuffle P 0.77; second catalogue deep 15 of 111 (13.5%) against 36 of 221 (16.3%), shuffle P 0.31. The other areas' deep thirds are not short of fish crests. Each area's deep third is relative to that area, so it may be later in time than DK-G Early I; the claim stands for DK-G Early I only. Harappa 3B already has crest-first names (6 of 40 named objects, four distinct texts), so the absence is not shared by Harappa; whether Mackay's Early I and Harappa 3B are the same decades is the catalogue's mapping and is not independently dated.
- **The second catalogue as a second sample: against.** It is 94% the same stones; the "36 against 36" is one set read twice. Rescue: it still counts as the transcription-error check (the clean zero holds in both), and its 2 extra stones and its picture codes were run.
- **O1, office and overseas bull last: against.** Both are in 3B-2 (office on 2 of 167 objects, M-974 with the earliest named-office text; overseas bull on 2 of 50 seals, M-1090). History already found them in two or three cities at the earliest bin; the order table keeps them in the first stage.
- **Counting-first as "names later": half.** Counting is not rarer after the cities (P 0.74); and the jar is on a Period 1 pot and is the one sign Kenoyer names in both Periods. The pure form "accounts, then names" does not hold; "accounts and the jar first, names put in front of the jar next" does.
- **Pots against pots**: the jar and fish rise before-to-after is not significant (0.24, 0.68), so the strong P 1.9e-5 for the jar is an object-kind change (pots to seals and tablets), not a change inside pots.
- **Gaps, not results**: only 7 objects are dated between the last pre-city pot and 3B-2, so first-seen order inside 3A and 3B-1 is unmeasured; Dholavira stage placement and the catalogue's labels for Rehman Dheri `Rhd-1` ("period I", one + spear 520) and Kalibangan K-94 (period I, mapped to 3A) are the catalogue's and are shown flagged, not checked against the excavation reports; `Rhd-269` carries the kalam sign alone under the label "Early" and has no rank.
- **Predictions**: the 0 of 36 was already in `history.md` and the 39 deep second-catalogue texts had been printed once before the first docstring was written; the any-marked-fish count (6 of 36) was printed once before E4 was frozen. E2 held (27 of 32 first signs also lead later names); E3 held; P1 to P5 held (66% counts, 13% house words, 5 goods objects none with a jar, cup the only measure sign in the set, 24 of 35 one sign, one text of 5 or more); O2 held; O3 held in the sense that most features are first solid at 3B-2.

## 7. What it opens

1. `240-255-435-690` jar (High-star, Chief, Rod, Ally) is the oldest fish house in the dig and the only fish name with a tail seen at no other level. Take it through all seven levels and the 34 objects of `255-435-690`: where its prefix stack drops off and the crest takes the front is the date of the "crest first" change.
2. The earliest seal texts are accounts (Dholavira stages I and II; M-1365 and M-95 "cottons"; the two-shares opener on 12 of 38). A sound-value test can use the 38 as a set no value was built on: read each with the sound list and count how many whole.
3. The jar-plus-"child of" pair on the first sherds (Kenoyer's 342 + 347) is the same pair as the earliest dig seal M-1010; the Period 2 pot `900-740-000` and the seal `004-900-740` share the moon-plus-jar form. A check: every pre-city two-sign sherd against the template's first two name slots.
4. The 3A and 3B-1 gap is the next thing to fill: 7 objects. Kalibangan period I, Nausharo II, Harappa 3A seals and tablets in the Kenoyer and Meadow paper. The PDF is free; it needs to be opened in Cúper's Chrome, since harappa.com blocks scripted downloads.
5. Seal pictures: rare creatures and no-stand seals concentrate at Early I (P 0.0013, 0.015), a format-fixing date that the text formula does not give. Dating by picture can be tested in Harappa 3B seals.
