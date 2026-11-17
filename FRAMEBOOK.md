# FRAMEBOOK: the Indus corpus written in jobs

A word-free book of every inscription in the first catalogue (5,679 inscribed faces), built 2026-11-17 by `work_scripts/frame2_corpus.py` and `frame2_book.py`. Each sign is written as a picture-word (what it looks like) with its job after a dot. Nothing here says what any sign means or how it sounds.

## Key (half a page)

- **Sign**: one drawn character, cited by its catalogue number (740 = the jar picture). Texts are given in reading order.
- **Picture-word**: a short name for what the sign looks like: the things two or three blind describers agreed on for the matching second-catalogue drawing (`work_data/pictures/pictures_blind.csv`, through the crosswalk; two things joined by `/` when both were agreed), and otherwise a name from the catalogue shape descriptions (all stroke numbers are named by count). The sign number is always given beside the example, so variants that share a picture-word stay apart. `[jar · closer]` = the jar picture, doing the closer job. A bare `[fish]` with no job = an ordinary name sign.
- **Jobs (frame v2)**: each sign has one job, learned from where it stands, never from a meaning:
  - **front word** (`OPEN`)
  - **after-front slot** (`SLOT`)
  - **name front (crest)** (`CREST`)
  - **name part** (`PERSONAL`)
  - **tall two (in names)** (`NUM_NAME`)
  - **short number** (`NUM_SHORT`)
  - **tall number** (`NUM_TALL`)
  - **measure** (`MEASURE`)
  - **after-measure** (`AFTER_M`)
  - **counted thing** (`THING`)
  - **name back** (`NAME_BACK`)
  - **place or time word** (`PLACE`)
  - **closer** (`CLOSER`)
  - **after-jar title** (`TITLE`)
- **Object kinds**: seals (stone stamps), tablets (small incised or moulded plaques), copper tablets, tags and sealings (clay lumps pressed on goods), pots (marks on pottery), other objects.
- **Text kind**: which pattern of the grammar a whole text fits (list below).

## The grammar, in plain words

1. A text may open with a **front word** (signs 861, 817, 820, 920, 692, 550 and a few more). A front word is followed by its own **slot** sign (002, 060, 741, 742, 368, 365).
2. After the front, either a **name** or a **count line** follows.
3. A **name** is one to three signs: usually a **crest** first (a fish sign 220/231/233/235/240, or 803/806/140), then name parts, sometimes a **name back** sign just before the end. The two tall strokes (032) live inside names, mostly right before a fish.
4. A name is shut by a **closer** (740, 520, porters 151/154/158). After the jar there may be one **after-jar title** (400, 090, 527, 621, 679 and a few others). 520 and the porters never follow 740; they stand in its place.
5. A **count line** is a **number** followed by a **counted thing** (trees 390/405/407, porter with jars 156, cup 700). Short strokes count trees and porters on seals; tall strokes count cups on tablets.
6. A **measure** sign is followed by its own follower (033, 760, 690) and often by a closer.
7. A **record** (mostly copper tablets) is a whole name text followed by a count line.
8. Which job may follow which differs by object: after the closer, a title comes three times as often on tablets as on seals; pots are one or two signs; copper tablets carry records and single picture-signs.

## Text kinds: counts by object kind

| text kind | seals | tablets | copper tablets | tags and sealings | pots | other objects | all |
|---|---|---|---|---|---|---|---|
| name text | 615 | 491 | 86 | 28 | 28 | 16 | 1264 |
| loose name text | 404 | 140 | 17 | 17 | 9 | 4 | 591 |
| opener + count line | 33 | 8 | 0 | 1 | 0 | 1 | 43 |
| bare count line | 49 | 353 | 0 | 3 | 9 | 4 | 418 |
| record | 3 | 5 | 9 | 0 | 0 | 0 | 17 |
| measure line | 3 | 2 | 0 | 1 | 3 | 1 | 10 |
| title alone | 5 | 1 | 0 | 0 | 8 | 2 | 16 |
| front alone | 8 | 11 | 0 | 0 | 3 | 3 | 25 |
| one picture | 0 | 0 | 24 | 0 | 0 | 0 | 24 |
| other | 420 | 347 | 60 | 28 | 237 | 100 | 1192 |
| damaged | 750 | 702 | 34 | 184 | 338 | 71 | 2079 |

## name text (1264 faces)

A name with its ending: [front word + slot]? [name signs] [closer] [title]?. The main seal text.

**Mohenjo-daro**

- `240-233-740-679` (seals, M-1720): [fish/bow · crest] [fish/leaf · crest] [jar/cup · closer] [X with table · title]

**Harappa**

- `004-783-740` (tablets, H-290): [four strokes · number] [flowering plant with three 783 · counted] [jar/cup · closer]

**Lothal**

- `861-002-235-555-527` (seals, L-89): [house · front] [two strokes · slot] [fish/bow · crest] [pincers variant] [ladder · title]

**Dholavira**

- `817-002-235-100-740` (seals, -): [house · front] [two strokes · slot] [fish/bow · crest] [man/bow · name back] [jar/cup · closer]

**Kalibangan**

- `180-740` (pots, K-104): [sign 180] [jar/cup · closer]

**Chanhu-daro**

- `055-161` (seals, C-63): [eight-stroke block] [man · title]

**Banawali**

- `061-740` (seals, B-8): [reversed lambda · place] [jar/cup · closer]

**Nausharo**

- `031-865-892-400` (pots, Ns-64): [one tall stroke · tall number] [diamond with several lines 865] [bow] [comb/ladder · title]

**Unknown**

- `817-002-061-702-740` (tablets, ?-6): [house · front] [two strokes · slot] [reversed lambda · place] [jar/cup] [jar/cup · closer]

**Allahdino**

- `235-740` (tags and sealings, -): [fish/bow · crest] [jar/cup · closer]

## loose name text (591 faces)

Holds a closer or title but breaks the strict order somewhere (a name sign after the closer, two closers, a front word inside).

**Mohenjo-daro**

- `803-861-002-705-033-482-740` (seals, M-1698): [leaf/fork · crest] [house · front] [two strokes · slot] [jar · measure] [three tall strokes · tall number] [roof · name back] [jar/cup · closer]

**Harappa**

- `400-031-384-156` (other objects, -): [comb/ladder · title] [one tall stroke · tall number] [leaf/tree] [man · counted]

**Lothal**

- `705-500-741-001-055-220-740-090` (tags and sealings, L-191): [jar · measure] [tent/house] [jar/cup · slot] [one stroke · number] [eight-stroke block] [leaf/fish · crest] [jar/cup · closer] [man · title]

**Dholavira**

- `175-742-233-798-740` (seals, -): [leaf] [jar/cup · slot] [fish/leaf · crest] [leaf/fish] [jar/cup · closer]

**Kalibangan**

- `082-132-065-220-002-231-520` (seals, K-25): [axe] [rake/man] [stroke with hook] [leaf/fish · crest] [two strokes · slot] [fish/leaf · crest] [arrow/flag · closer]

**Chanhu-daro**

- `034-287-365-002-101-740-140-840-031` (seals, C-1): [four tall strokes · tall number] [oval with several short 287 · counted] [flag/sail · slot] [two strokes · slot] [man/jar] [jar/cup · closer] [man/leaf · crest] [leaf] [one tall stroke · tall number]

**Unknown**

- `467-550-001-740-740` (seals, -): [tent/comb · number] [pincers · front] [one stroke · number] [jar/cup · closer] [jar/cup · closer]

**Nausharo**

- `920-060-742-220-520` (seals, Ns-59): [bracket with leaf · front] [hook · slot] [jar/cup · slot] [leaf/fish · crest] [arrow/flag · closer]

**Allahdino**

- `066-741-235-495-017-740` (seals, Ad-4): [tall caret with mark] [jar/cup · slot] [fish/bow · crest] [horn/bow] [seven stacked strokes · number] [jar/cup · closer]

**Desalpur**

- `740-892-002-032-394` (tags and sealings, Dlp-3): [jar/cup · closer] [bow] [two strokes · slot] [two tall strokes · name number] [simple tree with branches 394 · counted]

## opener + count line (43 faces)

A front word and its slot, then a count and a counted thing, with no name and no ending: [front][slot][number][counted thing]. The second kind of seal.

**Mohenjo-daro**

- `817-002-005-390` (seals, M-803): [house · front] [two strokes · slot] [five strokes · number] [fork · counted]
- `861-002-003-390` (seals, M-712): [house · front] [two strokes · slot] [three strokes · number] [fork · counted]

**Harappa**

- `861-002-035-405` (tablets, H-1942): [house · front] [two strokes · slot] [five tall strokes · tall number] [rake/comb · counted]
- `817-002-004-390` (tablets, H-2003): [house · front] [two strokes · slot] [four strokes · number] [fork · counted]

**Dholavira**

- `817-002-004-390` (seals, -): [house · front] [two strokes · slot] [four strokes · number] [fork · counted]

**Banawali**

- `692-060-003-426` (seals, B-21): [outlined X · front] [hook · slot] [three strokes · number] [comb/gate · counted]

**Chanhu-daro**

- `817-002-003-390` (seals, C-66): [house · front] [two strokes · slot] [three strokes · number] [fork · counted]

**Kalibangan**

- `861-002-003-390` (tags and sealings, K-82): [house · front] [two strokes · slot] [three strokes · number] [fork · counted]

**Nausharo**

- `820-002-003-390` (seals, Ns-7): [leaf · front] [two strokes · slot] [three strokes · number] [fork · counted]

**Khirsara**

- `820-013-016-390` (seals, -): [leaf · front] [three stacked strokes · number] [six stacked strokes · number] [fork · counted]

## bare count line (418 faces)

Only a count and a counted thing: [number][counted thing]. On tablets this is the cup with tall strokes; on seals a short count with a tree or a porter.

**Harappa**

- `033-700` (tablets, H-1308): [three tall strokes · tall number] [cup/jar · counted]

**Mohenjo-daro**

- `003-156` (seals, M-1779): [three strokes · number] [man · counted]

**Kalibangan**

- `005-405` (seals, K-19): [five strokes · number] [rake/comb · counted]

**Alamgirpur**

- `017-405` (pots, Agr-3): [seven stacked strokes · number] [rake/comb · counted]

**Lothal**

- `003-156` (seals, L-42): [three strokes · number] [man · counted]

**Amri**

- `034-390` (pots, Ai-7): [four tall strokes · tall number] [fork · counted]

**Banawali**

- `004-390` (seals, B-9): [four strokes · number] [fork · counted]

**Bhirrana**

- `003-003-390` (seals, -): [three strokes · number] [three strokes · number] [fork · counted]

**Ra's al-Junayz**

- `004-405` (pots, -): [four strokes · number] [rake/comb · counted]

**Shortughai**

- `003-426` (seals, Sh-69): [three strokes · number] [comb/gate · counted]

## record (17 faces)

A name text, its closer, then a count line after it. Mostly copper tablets.

**Mohenjo-daro**

- `220-017-585-095-520-032-407` (copper tablets, M-2053): [leaf/fish · crest] [seven stacked strokes · number] [tent · after-measure] [man] [arrow/flag · closer] [two tall strokes · name number] [rake/comb · counted]
- `231-017-585-095-520-032-407` (copper tablets, M-1555): [fish/leaf · crest] [seven stacked strokes · number] [tent · after-measure] [man] [arrow/flag · closer] [two tall strokes · name number] [rake/comb · counted]
- `231-017-585-095-520-032-407` (copper tablets, M-1556): [fish/leaf · crest] [seven stacked strokes · number] [tent · after-measure] [man] [arrow/flag · closer] [two tall strokes · name number] [rake/comb · counted]
- `231-017-585-095-520-032-407` (copper tablets, M-1557): [fish/leaf · crest] [seven stacked strokes · number] [tent · after-measure] [man] [arrow/flag · closer] [two tall strokes · name number] [rake/comb · counted]
- `231-017-585-095-520-032-407` (copper tablets, M-549): [fish/leaf · crest] [seven stacked strokes · number] [tent · after-measure] [man] [arrow/flag · closer] [two tall strokes · name number] [rake/comb · counted]

**Harappa**

- `413-575-335-740-032-700` (tablets, H-811): [comb/ladder] [door/jar] [cup/box · place] [jar/cup · closer] [two tall strokes · name number] [cup/jar · counted]
- `140-388-443-740-001-004-407` (seals, H-420): [man/leaf · crest] [leaf/tree] [backward capital gamma with 443] [jar/cup · closer] [one stroke · number] [four strokes · number] [rake/comb · counted]
- `390-155-004-390` (tablets, H-2186): [fork · counted] [man · closer] [four strokes · number] [fork · counted]
- `413-575-335-740-032-700` (tablets, H-2016): [comb/ladder] [door/jar] [cup/box · place] [jar/cup · closer] [two tall strokes · name number] [cup/jar · counted]
- `388-740-400-033-700` (tablets, H-1862): [leaf/tree] [jar/cup · closer] [comb/ladder · title] [three tall strokes · tall number] [cup/jar · counted]

## measure line (10 faces)

A measure sign with its follower or a number, sometimes closed: [measure][after-measure or number][closer]?

**Mohenjo-daro**

- `171-035` (pots, M-2067): [tree · measure] [five tall strokes · tall number]
- `029-032` (seals, M-1848): [three rows of off-center 029 · measure] [two tall strokes · name number]
- `905-032` (seals, M-1277): [horn/bow · measure] [two tall strokes · name number]
- `171-035` (tags and sealings, M-2036): [tree · measure] [five tall strokes · tall number]

**Harappa**

- `025-032-690` (tablets, H-2109): [three rows of off-center 025 · measure] [two tall strokes · name number] [nested chevrons · after-measure]
- `705-034` (other objects, -): [jar · measure] [four tall strokes · tall number]
- `408-003` (pots, H-1745): [measure 408 · measure] [three strokes · number]

**Dholavira**

- `408-005` (seals, -): [measure 408 · measure] [five strokes · number]
- `408-004` (tablets, -): [measure 408 · measure] [four strokes · number]

**Hissam-dheri**

- `480-001` (pots, Hd-4): [hill/roof · measure] [one stroke · number]

## title alone (16 faces)

One closer or title sign standing alone.

**Harappa**

- `740` (pots, H-1481): [jar/cup · closer]
- `090` (pots, H-1462): [man · title]
- `151` (pots, H-374): [leaf/man · closer]

**Mohenjo-daro**

- `740` (seals, M-1237): [jar/cup · closer]
- `740` (other objects, M-1647): [jar/cup · closer]

**Chanhu-daro**

- `679` (seals, C-52): [X with table · title]

**Daimabad**

- `740` (seals, Dmd-1): [jar/cup · closer]

**Lothal**

- `740` (pots, L-227): [jar/cup · closer]

**Bhirrana**

- `740` (seals, -): [jar/cup · closer]

**Lakhanjo-daro**

- `740` (tablets, -): [jar/cup · closer]

## front alone (25 faces)

A front word (with its slot) standing alone.

**Harappa**

- `820` (tablets, H-1970): [leaf · front]
- `817-002` (tablets, H-293): [house · front] [two strokes · slot]

**Banawali**

- `817-002` (seals, B-7): [house · front] [two strokes · slot]
- `817-002` (seals, B-15): [house · front] [two strokes · slot]

**Kalibangan**

- `817-002` (seals, K-27): [house · front] [two strokes · slot]
- `556` (other objects, K-464): [pincers with stroke · front]

**Mohenjo-daro**

- `820` (seals, M-1233): [leaf · front]

**Lothal**

- `550` (seals, L-106): [pincers · front]

**Nausharo**

- `861-742` (pots, Ns-78): [house · front] [jar/cup · slot]

**Kalba**

- `091` (seals, -): [jar/cup · front]

## one picture (24 faces)

One sign on a copper tablet, the sign that copies the picture on the other side.

**Mohenjo-daro**

- `777` (copper tablets, M-1555): [flowering plant with two 777]
- `354` (copper tablets, M-607): [rake/comb]
- `749` (copper tablets, M-597): [classic jar symbol with 749]
- `841` (copper tablets, M-605): [two vertical leaves 841]
- `777` (copper tablets, M-604): [flowering plant with two 777]
- `957` (copper tablets, M-1568): [sign 957]
- `035` (copper tablets, M-1465): [five tall strokes · tall number]
- `957` (copper tablets, M-606): [sign 957]
- `777` (copper tablets, M-1558): [flowering plant with two 777]
- `749` (copper tablets, M-1550): [classic jar symbol with 749]

## other (1192 faces)

Undamaged texts that fit none of the patterns above.

**Harappa**

- `540` (pots, H-1388): [hourglass/bow]

**Mohenjo-daro**

- `550-060-235-630-794-904-832-233-630-204` (seals, M-396): [pincers · front] [hook · slot] [fish/bow · crest] [tall rectangle 630] [fish/insect] [bow · place] [seed/leaf] [fish/leaf · crest] [tall rectangle 630] [fish]

**Kalibangan**

- `920-060-741-002-140-269-036` (seals, K-4): [bracket with leaf · front] [hook · slot] [jar/cup · slot] [two strokes · slot] [man/leaf · crest] [fish/bird] [six tall strokes · tall number]

**Lothal**

- `063-032-790-700-390` (other objects, L-101): [jar/cup] [two tall strokes · name number] [leaf/seed] [cup/jar · counted] [fork · counted]

**Dholavira**

- `032-790-407-590` (seals, -): [two tall strokes · name number] [leaf/seed] [rake/comb · counted] [box/weight]

**Chanhu-daro**

- `717-575-060-844-390` (seals, C-69): [comb] [door/jar] [hook · slot] [sign 844] [fork · counted]

**Nausharo**

- `031-001` (pots, Ns-70): [one tall stroke · tall number] [one stroke · number]

**Karanpura**

- `237` (seals, -): [sign 237]

**Banawali**

- `072-308-002-236` (seals, B-17): [arrow/tree] [bird] [two strokes · slot] [fish/bow]

**Unknown**

- `900-590-368-002` (seals, ?-3): [bow/moon · place] [box/weight] [flag/sail · slot] [two strokes · slot]

## damaged (2079 faces)

A lost or unclear sign or a broken edge. Restorations are in work_data/frame/corpus_jobs.csv.

**Harappa**

- `000-000` (tablets, H-2087): [lost sign] [lost sign]  · restored: 1:923=0.00/222=0.00/760=0.00 2:740=0.14/002=0.07/400=0.03

**Mohenjo-daro**

- `000-002-241-220-000` (seals, M-305): [lost sign] [two strokes · slot] [fish/bow · title] [leaf/fish · crest] [lost sign]  · restored: 1:861=0.02/817=0.02/824=0.01 5:520=0.13/740=0.11/240=0.04

**Dholavira**

- `368` (tags and sealings, -): [flag/sail · slot]

**Kalibangan**

- `003-220-000-000` (seals, K-8): [three strokes · number] [leaf/fish · crest] [lost sign] [lost sign]  · restored: 3:740=0.10/520=0.06/176=0.06 4:740=0.40/400=0.12/520=0.06

**Lothal**

- `000-032-000-000` (tags and sealings, L-197): [lost sign] [two tall strokes · name number] [lost sign] [lost sign]  · restored: 1:025=0.04/059=0.03/027=0.03 3:220=0.24/740=0.07/590=0.06 4:740=0.14/002=0.05/520=0.05

**Chanhu-daro**

- `820-002-000-000` (seals, C-85): [leaf · front] [two strokes · slot] [lost sign] [lost sign]  · restored: 3:032=0.07/240=0.05/235=0.04 4:740=0.35/520=0.08/390=0.05

**Nausharo**

- `834-495-350-310-374-ALT-142-740` (seals, Ns-9): [leaf with small vertical 834] [horn/bow] [fork] [sign 310] [leaf] [lost sign] [man/arrow] [jar/cup · closer]  · restored: 6:002=0.18/368=0.10/001=0.08

**Unknown**

- `000-033-220-001-032-061-000` (seals, -): [lost sign] [three tall strokes · tall number] [leaf/fish · crest] [one stroke · number] [two tall strokes · name number] [reversed lambda · place] [lost sign]  · restored: 1:705=0.31/706=0.15/033=0.04 7:740=0.42/407=0.18/405=0.07

**Banawali**

- `900-484-380-900-158-000-090-906` (tablets, B-24): [bow/moon · place] [ladder/roof] [leaf/heart] [bow/moon · place] [man · closer] [lost sign] [man · title] [bow]  · restored: 6:740=0.55/400=0.30/171=0.02

**Kot-Diji**

- `000` (pots, Kd-15): [lost sign]  · restored: 1:=0.00/001=0.00/002=0.00

