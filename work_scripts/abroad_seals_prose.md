# Seals found abroad: round seals are a different template, not a mirror-cut home text

Data: 46 objects with region Persian Gulf, Mesopotamia, Iranian Plateau, Central Asia, plus the 3 Unknown-site round seals (type SEAL:C): 23 round/cylinder seals, 15 square seals, 8 other objects (pot sherds, a prism, tags). Reading order = stored order reversed. Scripts (all in `work_scripts/`): `abroad_seals.py` (list and template fit), `abroad_orient.py`, `abroad_orient2.py`, `abroad_decide.py` (cut direction), `abroad_align.py` (round-seal alignment), `abroad_001.py` (the stroke), `abroad_report.py` (builds this file from `abroad_seals_prose.md`). Rerun any of them with `python3`.

## Findings in short

1. 15 of the 23 round seals carry a man sign (090 on 9, 091 on 6; never both), against 0 of 15 square seals and 0 of 8 other objects (Fisher P 3e-5). The round seals are a separate kind of text.
2. The man sign 090 loses its jar. At home 090 follows the jar 740 in 62 of 88 uses (it is the second closer: `[name] 740 090`). On the round seals 090 follows 740 in 0 of 9 (P 5e-5), and no round seal holds both 740 and a man sign (0 of 15). Where the jar stood, the single stroke 001 stands: `716-350-001-090` (Failaka) and `160-384-133-001-090-(lost)`.
3. The round seals keep the home order for the thing they count: count before counted (`001-090` = "1 man"), the same order the home load tags use. They do not need a flipped template; they need a template where the master slot before the man is 001, not the jar.
4. The house-crest layer is missing on round seals: 23 of the 30 commonest home name-slot signs never occur on a round seal, including all four fish crests (235, 240, 233, 231), 590, 741, 390, 705, 798, and both name-enders 760 and 100. What remains is the personal layer: 415, 220, 255, 840, 055, 550, 013. Round seals write SELF only: no house emblem, no ender tag. Their owners belonged to no Indus house.
5. Square seals abroad are home seals: 6 of 15 close in a class sign, 0 carry a man sign, 12 of the 30 commonest home name signs appear on them (240, 235, 590, 390, 798, 415, 760, 220, 255, 840, 125, 013). `590-390` sits on Kish 1971.1, Gonur 4155.1 and Altyn Depe (as `415-390`/`390`), the same name that sits on 14 home seals at 6 sites.
6. The round seals are number-heavy: 22 of 96 signs (23%) are count strokes against 5 of 51 (10%) on square seals and 16% at home. The single stroke 001 is on 9 of 23 round seals, 0 of 15 square seals (P 0.006), and in 6% of home seals. 5 of its 9 round-seal uses sit within two signs of a man sign, against 4 of 138 at home (P 3e-5); within-seal shuffling gives 3.6 expected (P 0.18), so the pull is real against home and short of proof against the geometry of 4-to-6-sign texts.
7. 091 (twin men) is abroad-specific: 6 of 110 round-seal signs (5.5%) against 0.1% at home (P 5e-9). It is first on 4 of 6 round seals (Luristan, Karzakan x2, Kalba), mid on two (Saar, an Unknown seal). It also opens the 2 complete multi-sign home seals that carry it (Mohenjo-daro `091-831-585`, Dholavira `091-500-741-240-416-840-740`). The "man first" on round seals is the way 091 behaves at home too, plus 090 on short texts.

## 1. Every text found abroad, in reading order and in words

Columns: home template = the last sign (lost signs skipped) is one of the 12 class signs (090, 151, 154, 156, 226, 400, 407, 520, 527, 617, 621, 740); flipped template = first sign is 090 or 091. Orientation column = whether the signs other than 090/091 sit where they sit at home (log-odds from a front-half/back-half profile of all home seals; positive 1 or more = home order, negative 1 or less = mirrored; man signs are left out so they cannot vote). The profile is 90% right on held-out Mohenjo-daro seals (752 of 837).
@@TABLES@@

Totals. Round: 5 fit the home template (class last), 6 fit the flipped template (man first), none fit both, 12 fit neither. Square: 6 fit home, none flipped. Other: 3 fit home.

**The `dir.` column.** It does not flip anything. Home seals marked L/R keep the same stored order as R/L ones (16 of 16 L/R home seals with 3 or more signs score as home order; 1,456 of 1,566 R/L). Abroad, the 2 round seals marked L/R (Qala'at al-Bahrain `190-060-055-090-160`, Janabiyah) both score home order (+2.7, +1.1); the 3 L/R square seals (Altyn Depe, Miri Qalat x2) read as home texts in reading order (`415-390`, `742-740`, `013-520`). Cut direction does not explain the man sign: all 6 round seals where 090/091 comes first are marked R/L, NR or unmarked, like the home seals, and the one L/R round seal with a man sign (Qala'at al-Bahrain) has it fourth.

**Decision per round seal** (orientation from non-man signs, margin 1.0): home order 7 (Failaka `090-000-817-317`, Qala'at al-Bahrain, Unknown `467-550-001-740-740`, Ur `528-220-924-340-093`, Girsu, Karzakan `091-032-001-033`, Janabiyah); mirrored 5 (Luristan `091-840-413-831` reads `831-413-840-091`; Susa `000-365-090-407-604-700` reads `700-604-407-090-365-000`; Unknown `160-384-133-001-090-000` reads `000-090-001-133-384-160`; Unknown `000-033-220-001-032-061-000`; Unknown `000-725-090-000-002`); 11 stay open (short or lost). So 5 of 12 decided round seals look catalogued in the opposite direction against 2 of 12 square seals; the round seals' reading direction is noisy in the catalogue, and a mirror is what makes Luristan and Failaka's man sign a closer. Reading order is therefore not settled for 17 round seals; the stats above that do not depend on direction (items 1, 2, 4, 6) hold either way, and item 7's "first" counts depend on it.

## 2. Round seals lined up

Signs on round seals against home (round share / home share, Fisher P): 090 9.4% / 1.0% (6e-7), 001 9.4% / 1.5% (2e-5), 091 6.3% / 0.10% (5e-9), 055 5.2% / 0.38% (5e-5), 160 (carrier-with-diamond-head) 2 uses / 2 at home, 924 2 / 4, 093 (man with a stroke between the legs) 2 / 5, 831 2 / 9, 190 2 / 9. Signs on round seals seen 0 to 3 times at home: 716, 160, 604, 319, 150, 603, 528, 340 (a deer), 328, 744, 133, 725, 071, 121, 099. Used mostly abroad: 090, 001, 091, 055, 160, 093, 924, 831, 190.

Shared pieces in shared positions:
- 091 first or at the head of its seal: `091-031-455-220`, `091-032-001-033`, `091-840-413-831`; `091` alone (Kalba). Second sign after 091 is a count stroke in 2 of 3 (031, 032).
- `001-090` adjacent on 2 seals; `350` right before 090 (stroke between) on 2 (Failaka `716-350-001-090`, Ur `350-090-004-...`).
- `740-740` doubled on 2 seals (Karzakan `740-740`, Unknown `467-550-001-740-740`); no man sign on either.
- Pairs in order on 3 seals: `031 ... 055`; on 2 seals each: `001 ... 090`, `350 ... 090`, `001 ... 031`, `001 ... 002`, `001 ... 740`, `467 ... 740`, `550 ... 740`, `220 ... 093`, `091 ... 031`, `091 ... 001`, `071 ... 055`, `831 ... 055`.
- A fixed frame `[man] [X] [stroke] [Y]` is on one seal only: `091-032-001-033` (twin-men, 2, 1, 3). The robust frame is `[name signs] [001] [090]`: Failaka, the Unknown `160-384-133-001-090`, and (mirrored) the Saar and Ur seals with a man sign beside 001. 

**What 001 separates.** In 9 of 9 round-seal uses 001 is interior (never first or last once lost signs are ignored, except the damaged `000-090-000-001-000`), and it splits the text into two blocks: `716-350 | 001 | 090`, `160-384-133 | 001 | 090`, `467-550 | 001 | 740-740`, `415-803 | 001 | 328-004-002`, `924 | 001 | 319-031-055-002-150-416`, `055-220-091 | 001 | 093-031`, `091-032 | 001 | 033`, `033-220 | 001 | 032-061`. The right block holds a man sign in 2, counts in 6 of 9. At home 001 does the same job: it follows the jar in 18 of 138 uses, follows the wheel opener in 17, and separates `[name + class]` from the `[A-count] 806 [carrier]` title phrase (H-143, H-158). Reading: 001 is a count of one and the boundary between the identity block and the counted block. `033-220 | 001 | 032-061` reads as an inventory in home grammar (3 fish, 1, 2 of 061); `415-803 | 001 | 328-004-002` reads as `[name: 415 803] 1 [328] 4 2`.

## 3. Matching the Gulf, Mesopotamian and Elamite legend formulas

What the sources give (web search, 2026-11-17): Old Babylonian and Larsa-period seals run owner's name, father's name, then the god or king served ("Waqrum, son of Shamash-nasir, servant of Nimintabba"; the Smithsonian Ancient Near East seal collection); Sargonic royal-service seals run "royal name, personal name, his servant"; Ur III seals change the slot after the name with the career (father's name replaced by office). Dilmun's own legend, quoted from Laursen's article in a Harappa.com review: "Palace of Rimum, servant of Inzak of Agarum", with Rimum, Yagli-El and Sumu-lel (18th to 16th century BC) calling themselves servants of Inzak of Agarum (Wikipedia, Agarum). The Gulf-type circular seals appear at Qala'at al-Bahrain with the city wall of about 2050 BC and spread from Babylonia to Gujarat (Harappa.com, Tilmun article). The cuneiform side in this repository holds Sargonic "Shu-ilishu, interpreter of Meluhha" (`eme-bal Me-luh-ha`) and Ur III Girsu "Ur-Lamma, son of Meluhha" (`dumu Me-luh-ha`) in `research/data/meluhha/cuneiform_seed_attestations.csv`.

The shape of these formulas is `[Name] [relation: servant / son / man] [master: god, king, father, land]` for Akkadian and Sumerian legends, and `[head: palace of / servant of] [Name]` inside a genitive chain: Sumerian `ir3 dInzak` and Akkadian `warad Sin` put the head noun first, the way Amorite names (Abdi-X, Warad-X) are built.

**Committed match: the Gulf round seal is "Name, servant of Master" with the Indus word order, and the master slot is where the jar stands at home.**

| slot of `PN, servant of DN` (Akkadian/Dilmun) | Indus home seal | Indus round seal abroad |
|---|---|---|
| PN | name block: FRONT crest + SELF + TAG (a house name) | SELF only: 1 to 3 personal signs (415, 220, 255, 840, 055, 550, 013 and rare signs 716, 350, 160-384-133) |
| servant (ARAD / ìr) | 090 plain man, last | 090 plain man (9 seals), 091 twin men (6 seals) |
| DN / master (the one served) | 740 jar, right before the man (62 of 88) | 001 (one stroke) right before the man on 2 seals; 740 absent from every seal with a man (0 of 15) |
| "palace of" / opener | diamond, wheel, `060-920` cap | 190 (spider) first on 2 round seals (Qala'at al-Bahrain, one Unknown seal), 160 carrier first on 1 |
| father/place after the man | title phrase `[A-count] 806 [carrier]` after 001 | `1 [328-004-002]`, `1 [032-061]`: a count block after 001 |

The order is the point. Akkadian and Sumerian put the relation word before the master (`servant | Inzak`), Indus home puts it after (`Inzak | servant`, i.e. `jar | man`), because the Indus language is head-final. A Dilmun-facing seal in Mesopotamian order would read `[servant][master][name]`, and that is what the 091-first seals are: `091 | 840-413-831`, `091 | 031-455-220`: twin-men as the head noun "servant(s) of", the name signs after it as the genitive. So the 6 round seals with 091 first are Akkadian-order legends written in Indus signs (head noun first), and the 090-last seals are home-order legends (head noun last). The same signs, two word orders, one meaning slot: both orders exist on Gulf seals because the Gulf merchants lived between an Indus-speaking and a Semitic/Sumerian-speaking customer. The 091 sign is "men / servants (of)" at the head, 090 is "man / servant" at the foot.

**Predictions for the other round seals** (rerunnable on every new Gulf-type reading):
1. A round seal that carries 091 has no 740 and no 090 (true on 6 of 6; 0 of 15 man seals hold a 740).
2. A round seal with a man sign and a count stroke has the stroke adjacent to the man (001 within 2 of a man sign: 5 of 9 against 4 of 138 at home).
3. After 091 comes a count or a rare sign, never a house crest (fish, 590, 741): true on 3 of 3 complete 091-first seals (031, 032, 840).
4. New Dilmun-type circular seals from Failaka and Bahrain (Laursen's queue rows 6-27) will show 090 or 091 on about two thirds of the round ones (15 of 23 here), and a fish crest on fewer than 1 in 20.
5. A bilingual round seal (Indus + cuneiform) will have the cuneiform `ARAD/ìr` or `dumu` next to the man sign; the Ur seal `3898.1` is not one (the bridge audit found Indus only) so test on Kjaerum 279/319 when the plate is obtained.
6. Gulf names should be Amorite or Sumerian names ending in a DN, so the SELF signs after 091 must be shared with the man's own seal group: 831 follows 091 at home (Mohenjo-daro `091-831-585`) and ends the Luristan seal and sits in Janabiyah: predict 831 recurs next to 091 or 090 on the next Gulf seal.

## 4. Reading the candidate meanings back at home

If 090 = servant/man and 740 = master/institution, a home seal `[name] 740 090` reads "name, (servant) of the jar-house, man". Home counts: 740 precedes 090 in 62 of 88; three of the 25 seals sign-by-sign in `name_slot.md` close this way (`861-002-240-415-100-740-090`, `817-002-240-415-100-740-090`, `820-001-235-240-740-090`) and read as "[opener] [FRONT 240][SELF 415][TAG 100] of-jar man". The 090 closer is the largest-seal class (median face 738 mm2, class table in `gloss_report.md`), which fits "man (of)" as a rank word at the top of the seal-size scale. The same assignment gives a reading for the home twin-man 091 openers: Dholavira `091-500-741-240-416-840-740`: "[men-of] 500 / 741 / 240-416-840 / jar" and Mohenjo-daro `091-831-585`: "men of 831, 585". This makes sense as an opener: 091 begins the text as the head noun, the genitive after it. 001 as "one" fits the home load tag `[name] 740 001 [A-n] 806 [carrier]` as "one [n loads of crop carried]" in the same slot. The 090/091 reading breaks nothing at home. It does not add a sound.

## 5. Home word order against the languages of the region

Home order: name first, class / title after (`[name] [class]`), count before the counted thing (`2 fish`, `A-n 806`, `001-090`), master before servant (`740 090`).

| family | title after name? | number before noun? | master before servant? (genitive order) | fits home order |
|---|---|---|---|---|
| Dravidian (Proto-Dravidian, Brahui, Tamil) | yes (caste/title follows the name: Tamil `Raman Pillai`) | yes | yes (genitive before head) | yes on all three |
| Munda (Santali, Mundari) | yes (clan/title follows) | yes | yes | yes on all three |
| Elamite | yes (`PN sunkik`, "PN king") | numerals in administrative lists come first | yes (possessor before possessed, head-final) | yes |
| Indo-Aryan, Vedic Sanskrit | no, title mostly before name (`raja Dasaratha`); Prakrit inscriptions put it after | number before noun | free (compounds put the first member first) | partial |
| Sumerian | yes (`Gudea ensi2 Lagas`) | no in grammar (noun-numeral), yes in accounts (`3 udu`) | no: possessed before possessor (`ir3 dInzak`) | no on the genitive, yes on title and account numbers |
| Akkadian, Amorite (Semitic) | yes (`PN eme-bal Meluhha`) | yes for cardinals | no: head before genitive (`warad Sin`, `mar PN`) | no on the genitive |

Dravidian, Munda and Elamite all keep title-after-name, number-before-noun and master-before-servant; Semitic and Sumerian break the third (head-initial genitive); Vedic Sanskrit breaks the first. This is a typological table from memory of the grammars; it is a filter, not a proof. The reading above predicts the same filter: the round Gulf seals that put 091 first are written in the order the Mesopotamian customer would parse, the 090-last seals in the home order, and the square Gulf seals keep home names, so the home language is on the Dravidian/Munda/Elamite side of the table. Sounds start from the SELF names on the Gulf seals: 415, 220, 255, 840, 055, 550, 013 are the signs to run against Amorite and Meluhhan name lists (the cuneiform lists in `research/data/meluhha/`).
