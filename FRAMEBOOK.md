# FRAMEBOOK: the Indus corpus written in jobs (`FRAME v3`)

A word-free book of every inscription in the first catalogue (5,679 inscribed faces; **3,137 of 3,600 = 87.14% intact faces parsed into strict clauses**, up from 50.47% in `v2`), built by `work_scripts/fv3_02_grammar.py` and `work_scripts/reader_v3_build.py`. Each sign is written as a picture-word (what it looks like) with its grammatical job after a dot, and multi-clause boundaries are marked with `|`. Nothing here says what any sign means or how it sounds (for concrete sound-free physical and metrological meanings, see `MEANINGS.md`).

## Key (half a page)

- **Sign**: one drawn character, cited by its catalogue number (`740` = the jar picture). Texts are given in reading order, segmented into clauses (`|`) by `FRAME v3`.
- **Picture-word**: a short name for what the sign looks like from blind three-rater agreement (`work_data/pictures/pictures_blind.csv`) and catalogue shape descriptions (`work_data/sign_shapes.csv`). `[jar/cup · closer]` = the jar picture doing the closer job; a bare picture-word with no dot = an ordinary `PERSONAL` name sign.
- **Jobs (`FRAME v3` — same 14 classes, 69 Lipi-CV-validated moves)**:
  - **front word** (`OPEN`)
  - **after-front slot & clause linker** (`SLOT`)
  - **name front (crest)** (`CREST`)
  - **name part** (`PERSONAL`)
  - **tall two (in names & counts)** (`NUM_NAME`)
  - **short number** (`NUM_SHORT`)
  - **tall number** (`NUM_TALL`)
  - **measure** (`MEASURE`)
  - **after-measure** (`AFTER_M`)
  - **counted thing** (`THING`)
  - **name back** (`NAME_BACK`)
  - **place or time word** (`PLACE`)
  - **closer** (`CLOSER`)
  - **after-jar title** (`TITLE`)
- **Coverage vs. Decoys**: Strict `FRAME v3` parses **87.14%** of all 3,600 intact Lipi faces (`87.19%` on length >= 3; `88.03%` on length >= 3 administrative texts vs. `23.92%` for 20 frequency-matched decoys, `0/20`, `z = 4.53`) and **64.94%** of unseen in-vocabulary Mahadevan `new texts` (up from `29.88%` in `v2`, `0/20` decoys, `z = 3.76`).

## The grammar, in plain words

1. **Clauses and `SLOT` Linkers**: An inscription is 1, 2, or 3 clauses (`|`). Signs in `SLOT` (`002, 060, 741, 742, 368, 365`) serve both after `OPEN` front words (`920-060-741`, `861-002`) and as **postpositional subordinate-clause linkers** (`125-406-741 | 590-406-740`, where marked jar `741/742` closes the subordinate clause before final `740`).
2. **Name Clauses**: `[OPEN + SLOT*]? [CREST / PERSONAL / PLACE / MEASURE-phrase / NAME_BACK]+ [CLOSER] [TITLE]?`. `520` and porters (`151/154/158`) stand in `740`'s place; `400, 090, 527, 621, 679` follow `740` or close titled clauses.
3. **Count, Vessel, and Measure Clauses**: Discrete goods take counts before the good (`[NUM_SHORT][THING]`, e.g. `004-390`); cup `700` takes tall divisors of 12 (`032-700`, `700-033`); bulk capacity and weight units (`705, 711, 171`) take tall strokes after the unit (`705-033`, `171-035`).
4. **Compound Ledgers**: Seals, tablets, and copper plates combine `[header_clause | name_clause]`, `[name_clause | count_clause]`, `[measure_clause | open_closed_clause]`, and 3-clause administrative dockets.

## Text kinds (`FRAME v3`): counts by object kind

| text kind | seals | tablets | copper tablets | tags and sealings | pots | other objects | all |
|---|---|---|---|---|---|---|---|
| name clause | 673 | 548 | 86 | 31 | 34 | 16 | 1388 |
| count or vessel tally | 97 | 471 | 4 | 8 | 21 | 14 | 615 |
| multi-clause text | 325 | 116 | 34 | 22 | 6 | 5 | 508 |
| goods or measure clause | 81 | 55 | 38 | 2 | 13 | 7 | 196 |
| header or front clause | 60 | 46 | 0 | 2 | 9 | 6 | 123 |
| single mark or emblem | 24 | 24 | 27 | 6 | 173 | 53 | 307 |
| unparsed | 280 | 98 | 7 | 7 | 41 | 30 | 463 |
| damaged | 750 | 702 | 34 | 184 | 338 | 71 | 2079 |
| **parsed intact total** | 1260 | 1260 | 189 | 71 | 256 | 101 | **3137 / 3600 (87.14%)** |

## name clause (1388 faces)

A single complete name clause: `[front + slot*]? [name signs] [closer] [title]?`. Covers 1,388 intact Lipi faces.

**Mohenjo-daro**

- `820-002-176-415-100-740` (seals, M-595, `name_clause`): [leaf · front] [two strokes · slot] [comb/leaf · name back] [rake/comb] [man/bow · name back] [jar/cup · closer]

**Harappa**

- `028-032-740-400` (tablets, H-967, `name_clause`): [three rows of off-center 028 · measure] [two tall strokes · name number] [jar/cup · closer] [comb/ladder · title]

**Lothal**

- `817-002-233-740-090` (seals, L-41, `name_clause`): [house · front] [two strokes · slot] [fish/leaf · crest] [jar/cup · closer] [man · title]

**Dholavira**

- `255-220-175-760-740` (seals, -, `name_clause`): [fish/leaf] [leaf/fish · crest] [leaf] [jar/cup · after-measure] [jar/cup · closer]

**Kalibangan**

- `003-158` (pots, K-380, `name_clause`): [three strokes · number] [man · closer]

**Chanhu-daro**

- `590-390-740` (seals, C-2, `name_clause`): [box/weight · measure] [fork · counted] [jar/cup · closer]

**Nausharo**

- `495-033-740` (seals, Ns-8, `name_clause`): [horn/bow · crest] [three tall strokes · tall number] [jar/cup · closer]

**Banawali**

- `061-740` (seals, B-8, `name_clause`): [reversed lambda · place] [jar/cup · closer]

**Unknown**

- `853-003-220-832-255-070-520` (seals, -, `name_clause`): [spider/star · front] [three strokes · number] [leaf/fish · crest] [seed/leaf] [fish/leaf] [arrow/tree] [arrow/flag · closer]

**Lakhanjo-daro**

- `706-740` (tags and sealings, -, `name_clause`): [jar · measure] [jar/cup · closer]

**Allahdino**

- `235-740` (tags and sealings, -, `name_clause`): [fish/bow · crest] [jar/cup · closer]

**Rupar**

- `415-226-400` (tablets, Rpr-1, `name_clause`): [rake/comb] [fish · counted] [comb/ladder · title]

## count or vessel tally (615 faces)

A single accounting clause: `[number][counted thing]`, vessel-first capacity tallies (`[cup 700][tall strokes]`), or mirror-incised tablet counts.

**Harappa**

- `034-700` (tablets, H-363, `count_clause`): [four tall strokes · tall number] [cup/jar · counted]

**Mohenjo-daro**

- `004-408` (seals, M-749, `count_clause`): [four strokes · number] [measure 408 · measure]

**Kalibangan**

- `003-064` (other objects, K-469, `count_clause`): [three strokes · number] [tree · counted]

**Dholavira**

- `033-136` (tags and sealings, -, `count_clause`): [three tall strokes · tall number] [man/comb · counted]

**Lothal**

- `015-409` (seals, L-97, `count_clause`): [five stacked strokes · number] [rake/comb · counted]

**Alamgirpur**

- `017-405` (pots, Agr-3, `count_clause`): [seven stacked strokes · number] [rake/comb · counted]

**Banawali**

- `692-060-003-426` (seals, B-21, `count_clause`): [outlined X · front] [hook · slot] [three strokes · number] [comb/gate · counted]

**Chanhu-daro**

- `920-060-741-003-429` (seals, C-16, `count_clause`): [bracket with leaf · front] [hook · slot] [jar/cup · slot] [three strokes · number] [long horizontal at bottom 429 · counted]

**Kanmer**

- `031-136` (other objects, -, `count_clause`): [one tall stroke · tall number] [man/comb · counted]

**Nausharo**

- `820-002-003-390` (seals, Ns-7, `count_clause`): [leaf · front] [two strokes · slot] [three strokes · number] [fork · counted]

**Rakhigarhi**

- `820-032-130` (tags and sealings, Rgr-3, `count_clause`): [leaf · front] [two tall strokes · name number] [comb/rake · counted]

**Amri**

- `034-390` (pots, Ai-7, `count_clause`): [four tall strokes · tall number] [fork · counted]

## multi-clause text (508 faces)

Two or three complete clauses joined by `SLOT` (`002, 741, 742, 060, 368`, acting as a postpositional subordinate-clause linker / medial jar closer) or juxtaposed as `[header | name]`, `[name | count]`, or `[measure | name]`. Clause boundaries are marked with `|`.

**Mohenjo-daro**

- `235-590-407-740 | 001-004-407` (seals, M-1310, `compound:name_clause+count_clause`): [fish/bow · crest] [box/weight · measure] [rake/comb · counted] [jar/cup · closer]  |  [one stroke · number] [four strokes · number] [rake/comb · counted]

**Harappa**

- `368-330-741 | 590-390-151` (tablets, H-180, `slot_linked+name_clause`): [flag/sail · slot] [sign 330] [jar/cup · slot]  |  [box/weight · measure] [fork · counted] [leaf/man · closer]

**Lothal**

- `705-500-741 | 001-055-220-740-090` (tags and sealings, L-197, `slot_linked+name_clause`): [jar · measure] [tent/house] [jar/cup · slot]  |  [one stroke · number] [eight-stroke block] [leaf/fish · crest] [jar/cup · closer] [man · title]

**Kalibangan**

- `091-056-002 | 417-890-892` (tags and sealings, K-75, `slot_linked+tally_docket`): [jar/cup · front] [sign 056] [two strokes · slot]  |  [sign 417 · counted] [bow/shield] [bow]

**Dholavira**

- `091-500-741 | 240-416-840-740` (seals, -, `slot_linked+name_clause`): [jar/cup · front] [tent/house] [jar/cup · slot]  |  [fish/bow · crest] [comb/rake] [leaf] [jar/cup · closer]

**Chanhu-daro**

- `579-250-741 | 233-803-740` (seals, C-8, `compound:header_clause+name_clause`): [tall table 579] [fish] [jar/cup · slot]  |  [fish/leaf · crest] [leaf/fork · crest] [jar/cup · closer]

**Unknown**

- `368-572-741 | 033-033-520` (seals, -, `slot_linked+name_clause`): [flag/sail · slot] [door/arrow] [jar/cup · slot]  |  [three tall strokes · tall number] [three tall strokes · tall number] [arrow/flag · closer]

**Gola Dhoro (Bagasra)**

- `033-820 | 240-415-100-740-090` (seals, -, `compound:count_clause+name_clause`): [three tall strokes · tall number] [leaf · front]  |  [fish/bow · crest] [rake/comb] [man/bow · name back] [jar/cup · closer] [man · title]

**Nausharo**

- `840-257-741 | 001-950-031-384-740` (seals, Ns-87, `compound:header_clause+name_clause`): [leaf] [ladder/bow] [jar/cup · slot]  |  [one stroke · number] [box on top left 950] [one tall stroke · tall number] [leaf/tree · name back] [jar/cup · closer]

**Allahdino**

- `066-741 | 235-495-017-740` (seals, Ad-4, `compound:header_clause+name_clause`): [tall caret with mark] [jar/cup · slot]  |  [fish/bow · crest] [horn/bow · crest] [seven stacked strokes · number] [jar/cup · closer]

**Bala-kot**

- `413-125-350-297-002 | 003-226` (seals, Blk-1, `slot_linked+count_clause`): [comb/ladder] [man/bow] [fork] [bird] [two strokes · slot]  |  [three strokes · number] [fish · counted]

**Banawali**

- `821-550-368 | 002-220-740-090` (seals, B-1, `compound:header_clause+name_clause`): [leaf] [pincers · front] [flag/sail · slot]  |  [two strokes · slot] [leaf/fish · crest] [jar/cup · closer] [man · title]

## goods or measure clause (196 faces)

A qualified commodity or metrological unit clause (`[stem/place + counted thing]` or `[measure + tall strokes / follower]`).

**Mohenjo-daro**

- `817-002-142-617` (seals, M-1976, `goods_clause`): [house · front] [two strokes · slot] [man/arrow] [jar/cup · counted]

**Harappa**

- `415-578-032-876` (tablets, H-2214, `goods_clause`): [rake/comb] [tall table 578 · measure] [two tall strokes · name number] [sign 876 · counted]

**Lothal**

- `240-031-156` (pots, L-271, `goods_clause`): [fish/bow · crest] [one tall stroke · tall number] [man · counted]

**Dholavira**

- `019-156` (seals, -, `goods_clause`): [nine short vertical strokes 019 · measure] [man · counted]

**Kalibangan**

- `003-832-390` (pots, K-120, `goods_clause`): [three strokes · number] [seed/leaf] [fork · counted]

**Farmana**

- `371-390` (seals, -, `goods_clause`): [bead/eye · measure] [fork · counted]

**Nausharo**

- `032-999-031` (pots, Ns-82, `measure_clause`): [two tall strokes · name number] [sign 999 · measure] [one tall stroke · tall number]

**Allahdino**

- `510-460-156` (seals, Ad-5, `goods_clause`): [square with lines] [hill] [man · counted]

**Altyn Depe**

- `415-390` (seals, Alt-90, `goods_clause`): [rake/comb] [fork · counted]

**Bakkar Buthi**

- `861-002-840-032-844-405` (pots, -, `goods_clause`): [house · front] [two strokes · slot] [leaf] [two tall strokes · name number] [sign 844 · measure] [rake/comb · counted]

**Bala-kot**

- `634-368-002-061-717-390` (seals, Blk-2, `goods_clause`): [rectangle 634 · front] [flag/sail · slot] [two strokes · slot] [reversed lambda · place] [comb] [fork · counted]

**Chanhu-daro**

- `230-156` (seals, C-21, `goods_clause`): [sign 230] [man · counted]

## header or front clause (123 faces)

An administrative header or precinct opener clause (`[front + slot + stem]`, `[front + closer/title]`, or standalone `[front + slot]`).

**Harappa**

- `698` (pots, H-1549, `front_alone`): [man/bird · front]

**Mohenjo-daro**

- `820-060-031-105` (seals, M-875, `header_clause`): [leaf · front] [hook · slot] [one tall stroke · tall number] [person with flag for 105]

**Lothal**

- `550-527` (seals, L-52, `open_closed_clause`): [pincers · front] [ladder · title]

**Kalibangan**

- `263-740-400` (tablets, K-68, `open_closed_clause`): [bird/fish · front] [jar/cup · closer] [comb/ladder · title]

**Banawali**

- `817-002` (seals, B-7, `front_alone`): [house · front] [two strokes · slot]

**Dholavira**

- `861-742-520` (seals, -, `open_closed_clause`): [house · front] [jar/cup · slot] [arrow/flag · closer]

**Nausharo**

- `794-741` (pots, Ns-86, `header_clause`): [fish/insect] [jar/cup · slot]

**Chanhu-daro**

- `920-060-031-592-031-032-842` (seals, C-54, `header_clause`): [bracket with leaf · front] [hook · slot] [one tall stroke · tall number] [weight/box · counted] [one tall stroke · tall number] [two tall strokes · name number] [sign 842]

**Unknown**

- `861-002-136` (seals, -, `header_clause`): [house · front] [two strokes · slot] [man/comb · counted]

**Bhirrana**

- `820-002-236` (seals, -, `header_clause`): [leaf · front] [two strokes · slot] [fish/bow]

**Gola Dhoro (Bagasra)**

- `861-893-140-236` (seals, -, `header_clause`): [house · front] [sign 893 · slot] [man/leaf · crest] [fish/bow]

**Kalba**

- `091` (seals, -, `front_alone`): [jar/cup · front]

## single mark or emblem (307 faces)

Single-sign vessel/tool marks, standalone titles/closers, paired crests, and single copper-tablet picture signs.

**Harappa**

- `220` (pots, H-1387, `single_mark`): [leaf/fish · crest]

**Mohenjo-daro**

- `354` (copper tablets, M-607, `one_picture`): [rake/comb]

**Kalibangan**

- `032` (pots, K-162, `single_mark`): [two tall strokes · name number]

**Dholavira**

- `032` (tags and sealings, -, `single_mark`): [two tall strokes · name number]

**Lothal**

- `740` (pots, L-227, `title_alone`): [jar/cup · closer]

**Karanpura**

- `390` (other objects, -, `single_mark`): [fork · counted]

**Nausharo**

- `031` (pots, Ns-74, `single_mark`): [one tall stroke · tall number]

**Chanhu-daro**

- `679` (seals, C-52, `title_alone`): [X with table · title]

**Banawali**

- `234` (pots, B-32, `pot_tool_mark`): [fish with a horizontal 234]

**Bhirrana**

- `006` (seals, -, `single_mark`): [six strokes · number]

**Gumla**

- `242` (pots, G-10, `pot_tool_mark`): [fish with extra whiskers 242]

**Lakhanjo-daro**

- `740` (tablets, -, `title_alone`): [jar/cup · closer]

## unparsed (463 faces)

Intact inscriptions (463 of 3,600 = 12.86%) that still fall outside strict `FRAME v3` clause rules.

**Mohenjo-daro**

- `016-405-001-255-324` (seals, M-416, `unparsed`): [six stacked strokes · number] [rake/comb · counted] [one stroke · number] [fish/leaf] [h with two horizontal 324]

**Harappa**

- `033-812-125-354-304-001` (seals, H-642, `unparsed`): [three tall strokes · tall number] [leaf with hatched square] [man/bow] [rake/comb] [bird · measure] [one stroke · number]

**Kalibangan**

- `906-055` (seals, K-30, `unparsed`): [bow] [eight-stroke block]

**Dholavira**

- `817-013-104-820-031` (seals, -, `unparsed`): [house · front] [three stacked strokes · number] [man/hill] [leaf · front] [one tall stroke · tall number]

**Lothal**

- `406-390-892-104` (seals, L-37, `unparsed`): [rake/comb · counted] [fork · counted] [bow] [man/hill]

**Chanhu-daro**

- `034-287-365-002-101-740-140-840-031` (seals, C-1, `unparsed`): [four tall strokes · tall number] [oval with several short 287 · counted] [flag/sail · slot] [two strokes · slot] [man/jar · name back] [jar/cup · closer] [man/leaf · crest] [leaf] [one tall stroke · tall number]

**Nausharo**

- `031-645` (pots, Ns-69, `unparsed`): [one tall stroke · tall number] [X]

**Banawali**

- `072-308-002-236` (seals, B-17, `unparsed`): [arrow/tree] [bird] [two strokes · slot] [fish/bow]

**Desalpur**

- `740-892-002-032-394` (tags and sealings, Dlp-3, `unparsed`): [jar/cup · closer] [bow] [two strokes · slot] [two tall strokes · name number] [simple tree with branches 394 · counted]

**Unknown**

- `741-298-002-136` (seals, -, `unparsed`): [jar/cup · slot] [bird] [two strokes · slot] [man/comb · counted]

**Allahdino**

- `013-840-740-170-072` (seals, Ad-6, `unparsed`): [three stacked strokes · number] [leaf] [jar/cup · closer] [two leaves horizontally adjacent 170 · title] [arrow/tree]

**Kot-Diji**

- `095-033` (pots, Kd-9, `unparsed`): [man] [three tall strokes · tall number]

## damaged (2079 faces)

Inscriptions with lost (`000`), unclear (`ALT`), or broken signs (2,079 faces).

**Harappa**

- `740-400` (tablets, H-1927, `damaged`): [jar/cup · closer] [comb/ladder · title]

**Mohenjo-daro**

- `233-705-033-807-388-740` (seals, M-1328, `damaged`): [fish/leaf · crest] [jar · measure] [three tall strokes · tall number] [leaf with tree at 807] [leaf/tree] [jar/cup · closer]

**Dholavira**

- `000-000` (tags and sealings, -, `damaged`): [lost sign] [lost sign]

**Kalibangan**

- `861-002-460-000-740` (tags and sealings, K-88, `damaged`): [house · front] [two strokes · slot] [hill] [lost sign] [jar/cup · closer]

**Lothal**

- `000-000-000-544` (seals, L-104, `damaged`): [lost sign] [lost sign] [lost sign] [sign 544]

**Chanhu-daro**

- `500-031-002-221-740-ALT-521-817` (seals, C-6, `damaged`): [tent/house] [one tall stroke · tall number] [two strokes · slot] [fish/bird] [jar/cup · closer] [lost sign] [anchor/tree] [house · front]

**Nausharo**

- `000-413-090-740` (pots, Ns-65, `damaged`): [lost sign] [comb/ladder] [man · title] [jar/cup · closer]

**Unknown**

- `000-033-220-001-032-061-000` (seals, -, `damaged`): [lost sign] [three tall strokes · tall number] [leaf/fish · crest] [one stroke · number] [two tall strokes · name number] [reversed lambda · place] [lost sign]

**Banawali**

- `031-220-368-000-220-000` (seals, -, `damaged`): [one tall stroke · tall number] [leaf/fish · crest] [flag/sail · slot] [lost sign] [leaf/fish · crest] [lost sign]

**Kot-Diji**

- `151` (pots, Kd-12, `damaged`): [leaf/man · closer]

**Rakhigarhi**

- `000-520-400` (tablets, -, `damaged`): [lost sign] [arrow/flag · closer] [comb/ladder · title]

**Lakhanjo-daro**

- `678` (pots, -, `damaged`): [an 'x' with a 678]

