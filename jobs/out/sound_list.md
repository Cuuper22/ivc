# Sound list: 89 new working values, the marked fish, the openers, names read whole

Scripts (run from `work_scripts/`, in this order): `sound_profile.py` (slots and world for every sign, `work_data/sound/profile.csv`, `top80.csv`), `sound_sheets.py` (picture sheets `work_data/sound/sheet_1..4.png`, looked at sign by sign), `sound_dedr.py` (DEDR look-up; the dictionary is kept at `work_data/lexicons/dedr/`), `sound_values.py` (the table below, with each value's prediction fixed before any check ran), `sound_checks.py` (task 5, `work_data/sound/checks.csv`), `sound_rescue.py` (second tries), `sound_fish_names.py` (fish, names spelled two ways, readable names), `sound_fishsplit.py`, `sound_readings.py` (writes `READINGS.md`), `sound_report.py` (tables). Reading order = stored order reversed.

Words in brackets are DEDR entry numbers (Burrow and Emeneau, looked up in the local copy). "mem" = from my memory, not found as a token in the local copy. Everything else in the word columns (which word goes with which sign, which pun) is my guess.

## What moved

1. **The marked fish are spelled out as [mark] + plain fish.** When a marked fish (235, 240, 233, 231, 226, 236) is swapped for two signs in an otherwise identical name, the second sign is the plain fish 220 in 40 of 528 swaps, against 133 of 3,332 for every other single sign (P 0.0004). The barred fish 233 is written `415-220` in 7 different name frames (`803-233 ~ 803-415-220` at Harappa, `240-233 ~ 240-415-220` and `235-233 ~ 235-415-220` at Mohenjo-daro). A marked fish is a compound "X-mīn" and the scribes could write it either way. This is the first measured sign of spelling inside names, and it is what the fish = *mīn* "star" reading predicts: the fish half stays, the mark becomes a word of its own.
2. **89 signs now carry a working sound.** Names read in full: 1,077 of 2,350 name tokens (46%), up from 66 (2.8%) with the first seven values and numbers; 429 distinct names. Complete faces of two or more signs with a sound on every sign: 1,759 of 3,236 (54%), up from 590 (18%).
3. **Checks: 30 of 89 predictions came true** (right direction, P 0.10 or less), 21 more went the right way without reaching that, 38 went against. Counting only the 65 checks on facts I had not already seen while choosing the word: 10 came true, 17 right direction, 38 against.
4. Fresh hits that pay: the diamond opener read as *kāṇi* "share, landed property, hereditary right" (DEDR 1444) predicts diamond seals name houses more than wheel seals: house crest opens the name on 97 of 274 diamond texts (35%) against 34 of 139 wheel texts (24%), P 0.015. The seated person 176 read as *iṟai* "tax, duty" (DEDR 521; picture *iru* "sit", 480) predicts it sits beside cup counts: on multi-face objects its face has a cup face beside it 68 of 94 times against 55% for all multi-face objects, P 0.0005. The pitchfork 415 read as *kavar* "branch (of a line)" (DEDR 1325) is shared inside Mohenjo-daro houses 26 pairs against 14.4 by chance (P 0.05). The odd animal 255 read as *mutalai* crocodile (4952) → *mutal* "chief, first" (4950) predicts bigger seals: 684 mm2 against 600 (P 0.048). The table-X 679 read as *kaṭṭil* "cot, throne" (1145), the seat of a house: its seals are 806 mm2 against 605 (P 0.03). The tree-405 *kiḷai* "kindred" (2018), the flag 368 *koṭi* "banner" (2049), the arrowheads 455 *ampu* and the pincer 555 are shared inside houses (5 vs 1.9, 11 vs 6.2, 3 vs 0.9, 2 vs 0.5).
5. **The wheel is a quarter-share.** Wheel = *kāl* "wheel" (DEDR 1483) ~ *kāl* "quarter": the wheel takes counts of 3 or less in 138 of 139 cases (2 is 111, 1 is 22, 3 is 5, one 4). With the diamond as *kāṇi* "share" and the wheel as *kāl* "quarter", the two openers are two sizes of holding, and the wheel seals are the smaller seals (525 against 645 mm2, measured in the diamond job). "Two hands" on a seal = *iru kāṇi*, "(holder of) two shares"; "wheel two" = *iru kāl*, "two quarters".
6. The cap opener `[920/692/550]-060-[jar with 1, 2 or 3 strokes]` reads as a dated or numbered opening: after the 060 mark the jar-with-strokes falls 38 / 10 / 3 for 1 / 2 / 3 strokes, the way ordinals fall. Jar + n strokes = *oru-kuṭi / iru-kuṭi / mu-kuṭi* "first / second / third house (ward)".

## 1. Sign table

Slot = roles from the possessive parser over all 5,679 faces, then position inside the name. World = commonest object group, strongest animal enrichment, strongest findspot enrichment, seal face median (all seals 646 mm2). Check = the one prediction fixed in `sound_values.py` before the run; "seen while choosing" marks the 24 checks whose fact I had already seen in the profile print-out when picking the word (they are not fresh predictions). Every check's numbers are in `work_data/sound/checks.csv`.

| sign | picture | slot (measured) | world (measured) | picture word (DEDR) | job word (DEDR) | sound | English | check | result |
|---|---|---|---|---|---|---|---|---|---|
| 235 | fish under a roof (caret hat) | crest 125; self 109; counted 15; in names first 117; mid 58; alone 41; last 18; counts 002 13; 033 1; 013 1 | seal 158; Hare 12/249 x11.2; Mohe:DK- 30/249 x1.9; seal face 745 mm2 | vēy bamboo, to thatch [5541] | vēy-mīn: the bamboo star (Old Tamil name of the asterism Punarvasu; Parpola read it so) | **vēymīn** | Bamboo-star (Punarvasu) | house-mates share it (a house/kin word repeats inside one house) | direction only: same-house pairs 38 against 37.80 by chance (Mohenjo-daro, 97 objects), P 0.441 |
| 240 | fish with whiskers | self 183; crest 132; counted 30; relation 4; in names first 135; mid 73; alone 67; last 40; counts 002 20; 031 5; 001 3; 032 2 | seal 181; Cros 7/349 x8.0; Hara:-- 64/349 x1.8; seal face 713 mm2 | mīcai whiskers [4879] | mī top, sky, height; micai sky [4841]: mī-mīn "high star" | **mīmīn** | High-star (pole star) | house-mates share it (a house/kin word repeats inside one house) | direction only: same-house pairs 55 against 47.24 by chance (Mohenjo-daro, 108 objects), P 0.231 |
| 233 | fish with a bar through the body | self 136; crest 49; counted 5; relation 2; in names mid 62; first 55; last 46; alone 22; counts 002 3; 003 1; 031 1 | seal 136; Gaur 14/192 x2.4; Mohe:DKC 10/192 x2.5; seal face 713 mm2 | vari line, stripe [5263] | vari-mīn "striped star"; vari also writing, line of a song [5263] | **varimīn** | Striped-star | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 17 against 22.06 by chance (Mohenjo-daro, 74 objects), P 0.771 |
| 231 | fish with a small stroke (dot) inside | self 52; crest 34; counted 8; in names first 31; mid 24; alone 21; last 10; counts 002 7; 003 1 | seal 63; Zebu 5/94 x4.3; Mohe:-- 7/94 x2.2; seal face 794 mm2 | puḷḷi dot, speck [4327] | puḷḷi-mīn "spot star" | **puḷḷimīn** | Spot-star | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 2 against 4.22 by chance (Mohenjo-daro, 33 objects), P 0.874 |
| 226 | fish caged by four strokes | self 22; counted 16; in names last 11; alone 10; first 1; counts 032 11; 003 2; 002 2 | seal 25; Bult 3/38 x4.7; Mohe:-- 4/38 x3.1; seal face 698 mm2 | kūṭu cage, pen, coop [1883] | kūṭu to assemble, join [1882]: kūṭu-mīn "gathered star", an asterism | **kūṭumīn** | Cluster-star | it lives on records (tablets, tags, pots, copper), not seals | no: non-seal objects 13/38 = 34% against 52% for all objects, P 0.992 |
| 236 | roofed fish caged by four strokes | self 23; counted 3; in names alone 11; last 9; mid 2; first 1; counts 002 3 | seal 15; Hara:-- 5/26 x1.9; seal face 869 mm2 | vēy + kūṭu [5541, 1883] | vēy-kūṭu-mīn, the Bamboo-star cluster | **vēykūṭumīn** | Bamboo-star cluster | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 0 against 0.17 by chance (Mohenjo-daro, 7 objects), P 1 |
| 861 | diamond with a small diamond on top | opener 173; counted 67; self 32; in names last 20; mid 10; alone 1; first 1; counts 003 29; 031 3; 032 2; 002 1 | seal 172; Elep 8/272 x1.9; Hara:ETrench 11 29/272 x2.7; seal face 676 mm2 | kāṇ to see; the lozenge is the eye [1443] | kāṇi share, land measure, landed property, hereditary right; kāṇam ancient weight [1444] | **kāṇi** | share, holding (a "hand") | diamond ("share, hereditary holding") seals name houses more than wheel seals | yes: texts whose name opens with a house crest: diamond opener 97/274 = 35%, wheel 34/139 = 24%, P 0.0152 |
| 817 | diamond, second drawing | opener 188; self 21; counted 8; tail 2; relation 1; in names last 14; mid 6; alone 1; counts 032 1 | seal 149; Elep 15/220 x4.4; Loth:-- 10/220 x2.5; seal face 673 mm2 | as 861 [1443] | kāṇi [1444] | **kāṇi** | share, holding | diamond ("share, hereditary holding") seals name houses more than wheel seals | yes: texts whose name opens with a house crest: diamond opener 97/274 = 35%, wheel 34/139 = 24%, P 0.0152 |
| 820 | six-spoke wheel | opener 186; self 31; counted 24; relation 1; in names last 16; mid 13; first 1; alone 1; counts 033 5; 001 1 | seal 176; Rhin 7/242 x4.3; Mohe:DKE 8/242 x2.1; seal face 645 mm2 | kāl wheel, cart [1483] | kāl quarter (1/4), leg (mem: not found as a token in the local DEDR copy) | **kāl** | quarter-share | the wheel never takes a count above three (quarters) | yes (seen while choosing): counts after the wheel <= 3: 138 of 139 (values [(2, 111), (1, 22), (3, 5), (4, 1)]), P 0 |
| 920 | crescent (right paren) with a leaf | opener 65; self 52; tag 24; counted 11; in names last 27; mid 27; first 18; alone 4; counts 031 1 | seal 105; Gavi 13/152 x5.2; Hara:FGranery 10/152 x2.8; seal face 686 mm2 | maruppu horns of the crescent moon [4720] | with 060: a dated opening, "in the month", (guess) | **tiṅkaḷ?** | month (head of a date formula) | the 060 + jar-with-strokes selector falls 1 > 2 > 3 (ordinals) | yes (seen while choosing): after the 060 mark: jar+1 38, jar+2 10, jar+3 3 (falls like ordinals 1st > 2nd > 3rd), P 0 |
| 590 | square box with a pole on top | self 196; counted 30; relation 2; in names mid 92; first 78; last 15; alone 11; counts 032 19; 033 4; 031 3; 017 2 | seal 117; Gavi 13/228 x3.5; Hara:FGranery 17/228 x3.2; seal face 558 mm2 | peṭṭi box, chest [4388] | paṭṭi cow-stall, sheepfold, hamlet, village [3868] | **paṭṭi** | hamlet, fold | house-mates share it (a house/kin word repeats inside one house) | direction only: same-house pairs 18 against 15.21 by chance (Mohenjo-daro, 62 objects), P 0.292 |
| 741 | handled jar with one stroke in the mouth | self 172; opener 38; counted 14; in names mid 100; last 35; first 29; alone 8; counts 003 1; 031 1 | seal 161; Gaur 13/224 x1.9; Mohe:VSA 9/224 x2.0; seal face 645 mm2 | kuṭam waterpot [1651] + oru one [1025] | kuṭi house, family, lineage, town [1655]: oru-kuṭi "first house / ward" | **orukuṭi** | first ward | house-mates share it (a house/kin word repeats inside one house) | direction only: same-house pairs 30 against 25.86 by chance (Mohenjo-daro, 80 objects), P 0.266 |
| 705 | U-vessel with a stick standing in it | counted 110; self 60; crest 48; in names first 48; mid 33; last 21; alone 6; counts 002 6; 031 3 | seal 105; Hare 12/218 x12.8; Mohe:DK- 26/218 x1.9; seal face 713 mm2 | kalam vessel, earthenware [1305] | kaḷam threshing floor, open space, assembly, place of business [1376] | **kaḷam** | threshing floor, assembly | it lives on records (tablets, tags, pots, copper), not seals | no: non-seal objects 109/213 = 51% against 52% for all objects, P 0.657 |
| 176 | person seated, knees bent | self 135; tag 77; counted 5; in names alone 90; last 68; first 32; mid 22; counts 002 3; 032 1; 031 1 | tablet 117; Bult 13/217 x3.6; Hara:FTrench I 28/217 x3.6; seal face 697 mm2 | iru to sit; irukkai seat [480] | iṟai tax on land, duty; iṟu to pay [521] | **iṟai** | tax, levy | on multi-face tablets it sits beside a cup face (a levy or weight paid in cups) | yes: two-or-more-face objects with a cup face beside the face carrying it 68/94 = 72% against 55%, P 0.000518 |
| 415 | pitchfork | self 169; counted 5; tail 1; relation 1; in names first 81; mid 74; alone 11; last 3; counts 033 2; 001 1; 031 1; 002 1 | seal 90; Gavi 13/176 x4.5; Hara:ETrench 11 13/176 x1.9; seal face 713 mm2 | kavar fork, prong [1325] | kavar to branch off; bifurcated branch [1325]: a lineage branch | **kavar** | branch (of a line) | house-mates share it (a house/kin word repeats inside one house) | yes: same-house pairs 26 against 14.37 by chance (Mohenjo-daro, 60 objects), P 0.0519 |
| 798 | leaf with pincers | self 99; tag 46; counted 4; in names first 48; last 44; mid 32; alone 21; counts 002 3; 003 1 | seal 98; Phyt 6/149 x4.0; Mohe:HRB 6/149 x1.9; seal face 742 mm2 | ilai leaf [497] (claws unread) | slot only: house front and pre-jar word; marukaṉ descendant, member of a clan [4715] | **maru-** | descendant, clan member | it stands right before the jar (a kin or house word) | yes (seen while choosing): right before the jar 48/145 = 33% against 17% for all name-slot signs, P 9.86e-07 |
| 407 | tree with ticked branches (variant) | self 105; counted 29; tail 8; in names last 57; mid 38; alone 7; first 3; counts 004 11; 032 9; 005 3; 016 2 | copper tablet 77; Hare 24/142 x39.4; Mohe:DK- 30/142 x3.3; seal face 467 mm2 | kiḷai branch (mem)  | kiḷai kindred, relations, group, herd, flock [2018] | **kiḷai** | herd, flock | it is counted with short strokes (living or grown things) | yes (seen while choosing): counts written before it: short 18, tall 10, P 0.0925 |
| 255 | odd animal: fish-bodied with legs (crocodile) | self 128; counted 7; relation 1; in names first 57; mid 45; last 22; alone 4; counts 033 2; 032 1; 001 1; 014 1 | seal 62; Gavi 11/136 x5.0; Hara:FGranery 8/136 x2.5; seal face 684 mm2 | mutalai crocodile [4952] | mutal first, chief, principal, capital [4950] | **mutal** | chief, first | seals carrying it are bigger (a high rank) | yes: seal face median 684 mm2 (n 52) against 600, P 0.0477 |
| 803 | leaf with a tree inside | crest 57; self 56; counted 18; relation 3; in names first 59; alone 20; mid 20; last 14; counts 002 15; 031 1; 001 1 | seal 97; Gavi 12/134 x5.5; Hara:FGranery 7/134 x2.2; seal face 726 mm2 | ilai leaf [497] | il house, home, place, wife [494] | **il** | house | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 7 against 12.15 by chance (Mohenjo-daro, 55 objects), P 0.901 |
| 760 | U with sprouting branches at the top | tag 99; self 23; counted 11; relation 1; in names last 88; alone 23; mid 9; first 2; counts 032 5; 001 4; 033 1; 036 1 | seal 86; Gavi 7/134 x3.2; Mohe:DKG. (N) 8/134 x2.1; seal face 742 mm2 | akai/arumpu to sprout, bud [15, 224] (picture weak) | slot: name tag before the jar; maka child, son or daughter [4616] | **maka** | son/child of | house-mates share it (a house/kin word repeats inside one house) | direction only: same-house pairs 15 against 10.75 by chance (Mohenjo-daro, 52 objects), P 0.182 |
| 840 | two overlapping leaves | counted 68; self 57; tail 5; in names mid 20; alone 15; first 11; last 11; counts 013 17; 002 6; 032 5; 016 2 | seal 57; Scene 7/130 x6.1; Mohe:HRA 5/130 x3.6; seal face 713 mm2 | iru ilai two leaves [474, 497] | iṇai union, pair, couple, to join [457] | **iṇai** | pair, partners | its texts name two parties (a pair word) | direction only: texts with two names or two jars 1/99 = 1% against 0%, P 0.303 |
| 550 | pincers (open jaws) | self 77; opener 28; counted 13; relation 4; in names first 31; mid 26; alone 11; last 9; counts 003 8; 002 3; 033 1; 467 1 | seal 68; Zebu 3/122 x2.0; Hara:FTrench IV+V 4/122 x2.0; seal face 609 mm2 | vāy mouth (mem) | vāyil gate (mem): head of the 550-060 opening = an office "the Gate" | **vāy** | gate, mouth | it lives on records (tablets, tags, pots, copper), not seals | no: non-seal objects 54/121 = 45% against 52% for all objects, P 0.963 |
| 405 | tree with ticked branches | counted 57; tag 39; self 17; tail 5; in names last 37; mid 9; alone 8; first 2; counts 004 7; 005 6; 003 4; 017 3 | seal 54; Hara:-- 39/118 x3.3; seal face 625 mm2 | kiḷai branch (mem) | kiḷai kindred, relations [2018] | **kiḷai** | kindred | house-mates share it (a house/kin word repeats inside one house) | yes: same-house pairs 5 against 1.93 by chance (Mohenjo-daro, 22 objects), P 0.0659 |
| 690 | two nested chevrons crossing | tag 73; self 40; counted 4; tail 1; in names last 75; alone 15; mid 14; first 9; counts 032 2; 004 1 | tablet 65; Gavi 13/118 x6.8; Hara:FGranery 9/118 x3.3; seal face 824 mm2 | piṇai to entwine, tie [4160] | piṇai to link, unite; pēṇ protection [4436] | **piṇai** | bound, allied | house-mates share it (a house/kin word repeats inside one house) | direction only: same-house pairs 4 against 2.89 by chance (Mohenjo-daro, 27 objects), P 0.287 |
| 368 | stroke with a triangular flag | self 64; counted 27; crest 25; relation 1; in names last 38; first 22; mid 19; alone 10; counts 005 3; 035 1; 001 1; 003 1 | seal 79; Scene 3/117 x2.9; Hara:FGranery 6/117 x2.2; seal face 756 mm2 | koṭi banner, flag [2049] | kōṭu summit, peak (same entry) ; koṭi line, lineage (guess) | **koṭi** | banner (of a line) | house-mates share it (a house/kin word repeats inside one house) | yes: same-house pairs 11 against 6.18 by chance (Mohenjo-daro, 39 objects), P 0.0989 |
| 900 | crescent (right paren) | self 43; counted 36; tag 28; relation 5; in names last 30; first 24; mid 10; alone 7; counts 003 13; 005 10; 004 5; 001 1 | seal 57; Anth 11/112 x17.1; Mohe:DK- 14/112 x2.0; seal face 524 mm2 | tiṅkaḷ moon [3213] | tiṅkaḷ month [3213] | **tiṅkaḷ** | month | its texts carry a second number (a date: month + day) | no: texts with a second count away from it 27/110 = 25% against 46%, P 1 |
| 140 | woman with breasts, arm raised | crest 46; self 33; counted 25; relation 4; tail 1; in names first 45; mid 14; last 12; alone 8; counts 003 7; 002 7; 015 2; 032 2 | seal 84; Scene 4/109 x4.1; Hara:AB- 6/109 x2.8; seal face 713 mm2 | peṇ woman (mem) | ammai mother, goddess; ammā lady, matron [183] | **ammai** | mother, lady | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 10 against 11.39 by chance (Mohenjo-daro, 53 objects), P 0.608 |
| 706 | U-vessel with a stick (elephant variant) | counted 52; self 48; tail 1; in names mid 20; first 16; last 7; alone 5; counts 002 5; 005 3; 031 2; 032 1 | seal 61; Elep 11/101 x7.0; Mohe:DK- 13/101 x2.0; seal face 930 mm2 | kalam vessel [1305] | kaḷam assembly, place of business [1376] | **kaḷam** | assembly place | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 4 against 5.67 by chance (Mohenjo-daro, 38 objects), P 0.75 |
| 061 | reversed lambda: a leg | self 50; crest 19; counted 18; relation 5; in names mid 27; first 23; alone 15; last 4; counts 002 10; 031 3; 001 2; 032 2 | seal 56; Anth 10/92 x18.9; Mohe:-- 6/92 x1.9; seal face 569 mm2 | kāl leg (mem) | kāl quarter (mem); tāḷ leg, foot, stem [3185] as rival | **kāl** | quarter | counts beside it never pass three (a quarter) | yes (seen while choosing): counts beside it <= 3: 27 of 27 (values [(2, 19), (1, 5), (3, 3)]), P 0 |
| 892 | bow and arrow | self 79; counted 6; tail 2; relation 1; in names last 34; mid 24; first 13; alone 8; counts 032 1; 031 1; 033 1 | tablet 38; Bult 6/88 x4.1; Kali:KLB-1- 9/88 x7.5; seal face 596 mm2 | vil bow; villavaṉ archer [5422] | vil to sell; vilai sale, price, value [5421] | **vil** | sale, price | it lives on records (tablets, tags, pots, copper), not seals | yes (seen while choosing): non-seal objects 60/88 = 68% against 52% for all objects, P 0.00183 |
| 503 | tall striped triangle | crest 52; counted 19; self 10; relation 1; in names first 54; mid 6; last 2; counts 002 1 | seal 38; Othr 28/82 x23.7; Mohe:DK- 15/82 x2.9; seal face 584 mm2 | malai hill, mountain [4742] | malai hill; ēḻ-malai "seven hills" with the stacked seven (guess) | **malai** | hill | house-mates share it (a house/kin word repeats inside one house) | direction only: same-house pairs 6 against 4.79 by chance (Mohenjo-daro, 35 objects), P 0.342 |
| 575 | trapezoid with a small box on top (lidded bin) | self 60; counted 20; in names mid 29; first 18; last 7; alone 6; counts 017 14; 031 2; 001 1 | seal 47; Zebu 3/80 x3.0; Hara:FGranery 4/80 x2.1; seal face 676 mm2 | kōṭṭai a measure of capacity = 21 marakkāl [2208] | kōṭṭai fort (mem) | **kōṭṭai** | great measure; fort | it lives on records (tablets, tags, pots, copper), not seals | no: non-seal objects 33/76 = 43% against 52% for all objects, P 0.952 |
| 692 | X drawn in outline | opener 44; self 28; counted 3; in names first 11; alone 9; last 5; mid 3; counts 001 1; 032 1 | seal 48; Zebu 3/75 x3.2; Mohe:DKG. (N) 5/75 x2.3; seal face 921 mm2 | slot only | head of the 692-060 opening: an office word | **?** | office (opening) | it lives on records (tablets, tags, pots, copper), not seals | no: non-seal objects 27/73 = 37% against 52% for all objects, P 0.997 |
| 617 | sign after the staff-bearer (shape not described) | self 68; counted 5; relation 2; in names last 38; first 16; alone 11; mid 3; counts 033 2; 002 1; 016 1 | seal 38; Othr 7/75 x6.5; Mohe:DK- 12/75 x2.5; seal face 524 mm2 | slot only | second half of the title kō-617 | **?** | title word | seals carrying it are bigger (a high rank) | no: seal face median 524 mm2 (n 33) against 606, P 0.813 |
| 435 | zig-zag line (lightning) | self 72; counted 3; in names mid 55; last 12; first 3; alone 2; counts 001 2 | seal 35; Bull 4/75 x5.7; Hara:FTrench I 5/75 x1.9; seal face 821 mm2 | miṉ lightning, flash [4876] | miṉ flash ~ mīṉ star [4876, 4885] | **miṉ** | flash, bright | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 1 against 2.08 by chance (Mohenjo-daro, 23 objects), P 0.853 |
| 615 | grid of cells | self 55; tag 17; counted 1; in names mid 45; last 16; alone 7; first 4; counts 016 1 | copper tablet 33; Othr 28/73 x26.6; Mohe:DK- 15/73 x3.3; seal face 524 mm2 | vayal paddy field, plots [5258] | vayal field, agricultural tract [5258] | **vayal** | field | it lives on records (tablets, tags, pots, copper), not seals | direction only (seen while choosing): non-seal objects 42/72 = 58% against 52% for all objects, P 0.183 |
| 904 | two nested crescents | self 26; tag 20; counted 15; relation 2; tail 1; in names last 18; mid 11; first 9; alone 8; counts 032 7; 001 3; 033 1; 004 1 | seal 30; Bull2 3/64 x21.6; Mohe:DK- 8/64 x2.0; seal face 621 mm2 | iru tiṅkaḷ [474, 3213] | iru-tiṅkaḷ "two months" | **irutiṅkaḷ** | two months | it lives on records (tablets, tags, pots, copper), not seals | no: non-seal objects 31/61 = 51% against 52% for all objects, P 0.642 |
| 527 | hatched box with corner strokes | self 56; tail 4; counted 2; relation 1; in names last 45; alone 6; mid 3; first 2; counts 475 1; 002 1 | seal 53; Gaur 5/63 x2.6; Mohe:DKC 3/63 x2.3; seal face 533 mm2 | slot only | second member of the fixed pair 550-527 / 555-527 | **?** | second member | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 3 against 3.98 by chance (Mohenjo-daro, 32 objects), P 0.685 |
| 055 | twelve strokes (4 over 4 over 4) | self 28; counted 17; tag 17; in names last 16; first 14; mid 8; alone 7; counts 001 13; 031 2; 033 1 | seal 41; Gaur 8/62 x4.3; Loth:SRG 3GX 10 8/62 x20.8; seal face 641 mm2 | patiṉ- ten, in teens [3918] | paṉṉiru twelve, a dozen (mem) | **paṉṉiru** | twelve | objects carrying it have no animal (a goods word, not an owner word) | direction only (seen while choosing): objects with no animal 33/61 = 54% against 51% for all objects, P 0.355 |
| 585 | stand or shrine with chevrons | counted 34; tag 17; self 9; in names last 17; mid 7; alone 2; counts 017 30; 033 4 | seal 30; Othr 4/60 x4.6; Mohe:-- 7/60 x3.4; seal face 929 mm2 | slot only (counted seven) | ēḻu + 585: a group-of-seven name, the Seven Maidens kaṉṉimār (mem) | **kaṉṉi?** | maiden (of the Seven) | it lives on records (tablets, tags, pots, copper), not seals | no: non-seal objects 30/60 = 50% against 52% for all objects, P 0.688 |
| 125 | person with bow | self 30; crest 22; counted 6; in names first 22; mid 15; last 8; alone 7; counts 001 2; 032 2; 033 1; 031 1 | seal 49; Bull1 36/58 x1.9; Hara:AB- 4/58 x3.6; seal face 745 mm2 | vēṭaṉ, vēṭṭuvaṉ hunter [5527] | vēṭṭuvar a hunting clan (mem); vēṭṭam hunting [5527] | **vēṭṭuvaṉ** | Hunter (clan) | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 0 against 1.69 by chance (Mohenjo-daro, 21 objects), P 1 |
| 388 | hatched pipal leaf on a stalk | self 35; tag 14; counted 7; tail 2; in names last 15; alone 13; first 11; mid 10; counts 031 3; 032 2; 002 2 | seal 37; Mult 3/58 x3.1; Mohe:DKG. (S) 14/58 x1.8; seal face 638 mm2 | aracu pipal, Ficus religiosa [202] | aracu kingliness, king, government; aracaṉ king [201] | **aracu** | king, royal | seals carrying it are bigger (a high rank) | direction only: seal face median 638 mm2 (n 29) against 604, P 0.375 |
| 440 | hook (backward gamma) | self 53; counted 4; tail 1; in names alone 21; mid 14; first 10; last 8; counts 012 1; 002 1; 003 1 | seal 32; Elep 4/58 x4.5; Hara:FTrench 43 7/58 x17.6; seal face 638 mm2 | alakku pole with an iron hook [237] | koḷ to receive, buy, acquire [2151] | **koḷ** | received, bought | it lives on records (tablets, tags, pots, copper), not seals | no: non-seal objects 26/58 = 45% against 52% for all objects, P 0.899 |
| 416 | double pitchfork | self 37; crest 14; counted 6; in names alone 28; first 14; mid 5; last 4; counts 001 3; 002 1 | seal 33; Hara:F- 6/57 x3.0; seal face 645 mm2 | kavar fork [1325], doubled | iru-kavar "two branches" | **irukavar** | two branches | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 0 against 1.05 by chance (Mohenjo-daro, 17 objects), P 1 |
| 413 | upright with crossbars (ear of grain) | self 53; counted 3; in names first 39; alone 5; mid 5; last 4; counts 031 1 | tablet 40; Bult 5/56 x5.3; Hara:ETrench 11 5/56 x2.2; seal face 467 mm2 | katir ear of grain, spear of grass [1194] | katir ray of light, sun; katiravaṉ sun [1193] | **katir** | grain ear; sun | at Harappa it sits in the granary mound F | no: Harappa objects from mound F 9/44 = 20% against 34% for all objects, P 0.983 |
| 850 | plain lozenge | self 48; counted 8; in names mid 17; last 14; first 10; alone 7; counts 031 2; 032 2; 001 1; 002 1 | seal 20; Anth 10/56 x31.0; Mohe:DK- 9/56 x2.5; seal face 648 mm2 | kaṇ eye (mem) | kāṇ to see [1443] | **kaṇ** | eye, sight | it lives on records (tablets, tags, pots, copper), not seals | yes (seen while choosing): non-seal objects 35/54 = 65% against 52% for all objects, P 0.0435 |
| 742 | handled jar with two strokes in the mouth | self 45; opener 9; counted 2; in names mid 20; alone 13; first 8; last 4; counts 031 1 | seal 37; Anth 6/56 x18.6; Mohe:HRB 4/56 x3.4; seal face 728 mm2 | kuṭam [1651] + iru [474] | iru-kuṭi "second ward" [1655] | **irukuṭi** | second ward | the 060 + jar-with-strokes selector falls 1 > 2 > 3 (ordinals) | yes (seen while choosing): after the 060 mark: jar+1 38, jar+2 10, jar+3 3 (falls like ordinals 1st > 2nd > 3rd), P 0 |
| 845 | two hatched overlapping leaves | self 50; tail 3; relation 1; counted 1; in names mid 32; first 16; alone 1; last 1 | copper tablet 41; Hare 12/55 x50.9; Mohe:DK- 18/55 x5.2; seal face 750 mm2 | slot only (hare tablets) | thing named on the hare copper tablets after "three" | **?** | hare-tablet word | it lives on records (tablets, tags, pots, copper), not seals | yes (seen while choosing): non-seal objects 42/55 = 76% against 52% for all objects, P 0.000214 |
| 717 | cat's paw | self 49; counted 5; in names last 14; mid 13; first 12; alone 10; counts 002 3; 032 2 | seal 39; Hara:AB- 5/54 x4.8; seal face 730 mm2 | aṭi foot, footprint [72] | aṭimai servant, devotee; aṭiyāṉ [72] | **aṭi** | servant, devotee | seals carrying it are smaller (a low rank) | no: seal face median 730 mm2 (n 30) against 600, P 0.986 |
| 752 | U with hatched sprouts (variant of 760) | tag 49; self 4; in names last 47; alone 6 | copper tablet 31; Othr 28/53 x36.6; Mohe:DK- 14/53 x4.2; seal face 663 mm2 | as 760 | maka child [4616] | **maka** | child of | house-mates share it (a house/kin word repeats inside one house) | direction only: same-house pairs 1 against 0.88 by chance (Mohenjo-daro, 15 objects), P 0.585 |
| 790 | plain lens (eye without pupil) | self 33; counted 10; relation 6; tail 1; in names first 14; alone 10; mid 5; last 4; counts 032 5; 031 1; 005 1; 001 1 | seal 19; Goat 3/50 x12.8; Hara:AB- 4/50 x4.1; seal face 376 mm2 | kaṇ eye (mem) | kaṇ eye; kāṇ see [1443] | **kaṇ** | eye | it lives on records (tablets, tags, pots, copper), not seals | yes (seen while choosing): non-seal objects 31/49 = 63% against 52% for all objects, P 0.0815 |
| 595 | striped box with a pole (variant of 590) | self 32; counted 15; tail 1; in names last 17; mid 9; first 5; alone 1 | seal 32; Gaur 3/48 x2.1; Hara:AB- 8/48 x8.6; seal face 879 mm2 | peṭṭi box [4388] | paṭṭi fold, hamlet [3868] | **paṭṭi** | fold | house-mates share it (a house/kin word repeats inside one house) | direction only: same-house pairs 3 against 1.12 by chance (Mohenjo-daro, 17 objects), P 0.106 |
| 350 | bar with shoots above and a cup below (plant in a pot) | self 33; counted 14; in names first 16; mid 15; alone 1; last 1; counts 002 5; 031 4; 001 2; 032 1 | seal 39; Gaur 5/47 x3.5; Mohe:HRB 3/47 x3.0; seal face 641 mm2 | slot only | front of a name | **?** | name front | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 1 against 1.55 by chance (Mohenjo-daro, 20 objects), P 0.754 |
| 455 | three arrowheads | self 42; counted 4; in names last 16; mid 10; first 9; alone 7; counts 033 1; 031 1 | seal 30; Gaur 3/46 x2.2; Mohe:-- 4/46 x2.6; seal face 664 mm2 | ampu arrow [178] | ampu arrow; mū-v-ampu "three arrows" as a name | **ampu** | arrow | house-mates share it (a house/kin word repeats inside one house) | yes: same-house pairs 3 against 0.86 by chance (Mohenjo-daro, 16 objects), P 0.0599 |
| 923 | crescent drawn in outline (a tusk) | self 26; tag 18; counted 1; in names alone 25; last 16; mid 2; first 1 | seal 28; Elep 12/45 x17.2; Mohe:DK- 11/45 x3.9; seal face 575 mm2 | maruppu tusk, horn, horns of the crescent moon [4720] | marukaṉ descendant, scion, member of a clan [4715] | **maru** | descendant of | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 0 against 1.84 by chance (Mohenjo-daro, 22 objects), P 1 |
| 832 | lens with a pupil: an eye | self 36; counted 6; relation 1; tail 1; in names first 13; mid 9; last 8; alone 6; counts 002 2; 003 1; 032 1; 001 1 | seal 29; Dhol:-- 3/44 x4.7; seal face 589 mm2 | kaṇ eye (mem) | kāṇ to see [1443] | **kaṇ** | eye | it lives on records (tablets, tags, pots, copper), not seals | no: non-seal objects 14/43 = 33% against 52% for all objects, P 0.997 |
| 335 | M on a box | self 40; counted 3; in names mid 23; last 9; alone 4; first 4; counts 002 2; 003 1 | tablet 29; Hara:ETrench 7/8 3/43 x17.1; seal face 641 mm2 | slot only | middle of the tablet phrase 575-335-711 | **?** | tablet word | it lives on records (tablets, tags, pots, copper), not seals | yes (seen while choosing): non-seal objects 30/41 = 73% against 52% for all objects, P 0.00524 |
| 480 | caret: a peak | counted 25; self 17; in names alone 7; mid 5; first 4; last 1; counts 003 3; 002 2 | pottery 17; Kali:KLB-1- 4/42 x7.0; seal face 506 mm2 | kuṉṟu hill [1864] | kuṉṟu hill; kuṉṟuvar mountaineers [1864] | **kuṉṟu** | hill | at Harappa it sits in the granary mound F | no: Harappa objects from mound F 2/13 = 15% against 34% for all objects, P 0.965 |
| 482 | outlined peak with a diamond | tag 23; self 16; counted 2; in names last 20; mid 8; alone 6; first 5; counts 001 1; 033 1 | tablet 19; Hara:-- 9/41 x2.2; seal face 807 mm2 | kuvaṭu mountain, peak [2049] | kōṭu summit [2049] | **kōṭu** | summit | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 0 against 0.27 by chance (Mohenjo-daro, 9 objects), P 1 |
| 630 | tall rectangle with teeth | self 39; counted 1; in names alone 16; mid 9; last 7; first 7; counts 032 1 | tablet 21; Xcrs 6/40 x247.7; Mohe:DK- 8/40 x3.2; seal face 602 mm2 | slot only (tooth: pal, mem) | pala many, several [3987] | **pal** | many | it lives on records (tablets, tags, pots, copper), not seals | yes (seen while choosing): non-seal objects 27/39 = 69% against 52% for all objects, P 0.0242 |
| 460 | three tall peaks | self 21; tag 15; counted 3; in names last 17; mid 11; alone 4; first 4; counts 031 1; 015 1; 032 1 | seal 31; Bull1 24/39 x1.9; Mohe:DK- 5/39 x2.0; seal face 625 mm2 | mū + kōṭu peak [5052, 2049] | mukkōṭu "three peaks" | **mukkōṭu** | Three-peaks | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 1 against 1.19 by chance (Mohenjo-daro, 18 objects), P 0.687 |
| 070 | upward arrow | self 17; tag 13; counted 7; in names last 11; mid 8; first 7; alone 4; counts 032 4; 002 3 | seal 28; Mohe:DKG. (S) 10/37 x2.0; seal face 645 mm2 | ampu arrow [178] | ampu (before the spear: arrow + spear) | **ampu** | arrow | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 1 against 1.14 by chance (Mohenjo-daro, 17 objects), P 0.684 |
| 745 | handled jar with three strokes in the mouth | self 30; counted 3; opener 3; in names first 17; mid 7; last 3; alone 3; counts 031 1; 001 1 | seal 21; Mohe:VSA 5/36 x6.9; seal face 930 mm2 | kuṭam [1651] + mū [5052] | mu-kuṭi "third ward" | **mukuṭi** | third ward | the 060 + jar-with-strokes selector falls 1 > 2 > 3 (ordinals) | yes (seen while choosing): after the 060 mark: jar+1 38, jar+2 10, jar+3 3 (falls like ordinals 1st > 2nd > 3rd), P 0 |
| 384 | pipal leaf on a stalk | self 20; counted 13; in names last 10; alone 7; mid 2; first 1; counts 031 5; 032 4; 002 3; 033 1 | seal 18; Othr 3/33 x6.3; Mohe:DK- 5/33 x2.4; seal face 625 mm2 | aracu pipal [202] | aracu king [201] | **aracu** | king, royal | seals carrying it are bigger (a high rank) | direction only: seal face median 625 mm2 (n 14) against 605, P 0.316 |
| 632 | tall rectangle with teeth (variant) | self 23; counted 7; relation 1; tail 1; in names first 14; mid 5; alone 3; last 1; counts 032 6; 031 1 | seal 26; Hara:AB- 3/32 x4.8; seal face 745 mm2 | as 630 | pala many [3987] | **pal** | many | house-mates share it (a house/kin word repeats inside one house) | direction only: same-house pairs 1 against 0.48 by chance (Mohenjo-daro, 11 objects), P 0.362 |
| 824 | sign after the bow (shape not described) | self 27; counted 5; in names last 15; alone 9; first 3 | tablet 22; Bult 6/32 x11.2; Hara:ETrench 11 5/32 x3.9; seal face 765 mm2 | slot only | after vil: the thing sold | **?** | thing sold | it lives on records (tablets, tags, pots, copper), not seals | yes (seen while choosing): non-seal objects 22/32 = 69% against 52% for all objects, P 0.0448 |
| 501 | striped heap with an axis | self 30; counted 1; in names alone 29; mid 1; counts 031 1 | tablet 29; Bull1 30/31 x3.0; Hara:-- 29/31 x9.3 | kumi heap, pile [1741] | kumi to heap up, accumulate [1741] | **kumi** | heap, stock | at Harappa it sits in the granary mound F | no: Harappa objects from mound F 0/30 = 0% against 34% for all objects, P 1 |
| 495 | striped horn | self 27; counted 3; in names first 17; mid 8; last 1; alone 1; counts 002 1 | seal 14; seal face 524 mm2 | kompu horn, tusk, branch [2115] | kompu branch (of a line) [2115] | **kompu** | branch | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 0 against 0.09 by chance (Mohenjo-daro, 5 objects), P 1 |
| 095 | person with a short stick | self 27; counted 3; in names alone 15; first 6; last 5; mid 1; counts 031 1 | copper tablet 14; Mohe:-- 6/30 x5.9; seal face 468 mm2 | kōl stick, staff [2237] | kōl rod, staff of office: kōlaṉ staff-bearer | **kōlaṉ** | staff-bearer | it lives on records (tablets, tags, pots, copper), not seals | yes (seen while choosing): non-seal objects 22/30 = 73% against 52% for all objects, P 0.0156 |
| 165 | two arcs joined at the top with a curl | self 27; counted 2; relation 1; in names last 11; first 6; mid 6; alone 4; counts 012 1 | seal 17; Mohe:DK- 4/30 x2.1; seal face 599 mm2 | slot only (after the month sign) | nāḷ day [3656] after tiṅkaḷ month (guess) | **nāḷ?** | day | it lives on records (tablets, tags, pots, copper), not seals | no: non-seal objects 13/30 = 43% against 52% for all objects, P 0.879 |
| 171 | T-bar with two pans: a balance | counted 25; self 4; in names mid 2; first 1; last 1 | seal 15; Bult 3/29 x6.2; Mohe:DKG. (S) 7/29 x1.8; seal face 581 mm2 | kā lever of a steelyard [1417] | niṟai fullness, to fill [3682]; weight (mem) | **niṟai** | weight, full measure | on multi-face tablets it sits beside a cup face (a levy or weight paid in cups) | no: two-or-more-face objects with a cup face beside the face carrying it 3/12 = 25% against 55%, P 0.993 |
| 645 | plain X | self 15; counted 13; in names mid 9; first 3; last 3; counts 003 5; 031 2; 032 1; 002 1 | tablet 11; Cros 7/28 x99.1; Mohe:DK- 5/28 x2.8; seal face 578 mm2 | slot only | counted three on tablets and pots | **?** | counted thing | it lives on records (tablets, tags, pots, copper), not seals | yes (seen while choosing): non-seal objects 20/26 = 77% against 52% for all objects, P 0.00901 |
| 463 | three triangles (variant of 460) | self 25; counted 2; tail 1; in names mid 12; last 8; first 3; alone 2 | seal 16; Phyt 6/28 x21.0; seal face 609 mm2 | mū + kōṭu [5052, 2049] | mukkōṭu | **mukkōṭu** | Three-peaks | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 0 against 0.28 by chance (Mohenjo-daro, 9 objects), P 1 |
| 091 | two persons side by side | self 26; counted 2; in names first 18; alone 6; mid 1; last 1; counts 031 1 | seal 15; Gaur 4/28 x4.8; Kali:KLB-1- 7/28 x18.4; seal face 997 mm2 | iraṭṭai pair, twins [474] | iruvar the two (persons) [474] | **iruvar** | the pair, partners | house-mates share it (a house/kin word repeats inside one house) | no: same-house pairs 0 against 0.08 by chance (Mohenjo-daro, 5 objects), P 1 |
| 175 | person seated, plain | self 24; counted 3; in names first 10; mid 10; alone 4; counts 002 3 | seal 13; seal face 778 mm2 | iru to sit [480] | iṟai tax, duty [521] | **iṟai** | tax | on multi-face tablets it sits beside a cup face (a levy or weight paid in cups) | direction only: two-or-more-face objects with a cup face beside the face carrying it 3/5 = 60% against 55%, P 0.599 |
| 104 | person with a caret at the foot | self 24; counted 2; in names first 14; alone 6; mid 2; last 2; counts 033 1 | seal 13; Cros 7/26 x106.7; Mohe:DK- 5/26 x3.0; seal face 485 mm2 | slot only | front of a name | **?** | name front | house-mates share it (a house/kin word repeats inside one house) | direction only: same-house pairs 1 against 0.24 by chance (Mohenjo-daro, 8 objects), P 0.213 |
| 500 | tall horn-triangle with a divider | self 24; in names mid 17; first 3; alone 2; last 2 | other 12; Loth:SRG 3GX 10 8/24 x53.7; seal face 1024 mm2 | slot only (Lothal tags) | middle of the Lothal tag formula | **?** | tag word | it lives on records (tablets, tags, pots, copper), not seals | direction only (seen while choosing): non-seal objects 16/24 = 67% against 52% for all objects, P 0.114 |
| 555 | pincers (variant of 550) | self 23; relation 1; in names mid 16; first 5; last 2 | seal 22; Mohe:DKG. (N) 3/24 x4.4; seal face 646 mm2 | vāy (mem) | vāy | **vāy** | gate | house-mates share it (a house/kin word repeats inside one house) | yes: same-house pairs 2 against 0.53 by chance (Mohenjo-daro, 12 objects), P 0.0929 |
| 540 | bow-tie: hourglass drum | self 22; in names alone 10; last 6; first 4; mid 2 | pottery 9; - 19/22 x1.9; Hara:FTrench 43 5/22 x33.1; seal face 631 mm2 | paṟai drum (mem) | paṟai to speak, proclaim; word [4031] | **paṟai** | proclamation | it lives on records (tablets, tags, pots, copper), not seals | yes (seen while choosing): non-seal objects 14/19 = 74% against 52% for all objects, P 0.0491 |
| 877 | diamond with four small diamonds | self 14; counted 8; in names first 5; alone 5; last 2; mid 2; counts 032 8 | seal 18; Mohe:DKG. (S) 6/22 x2.0; seal face 600 mm2 | kāṇ [1443], fourfold | nāl-kāṇi "four shares" (guess) | **nālkāṇi** | four shares | it stands right before the jar (a kin or house word) | no: right before the jar 1/14 = 7% against 17% for all name-slot signs, P 0.922 |
| 636 | tall rectangle with teeth (variant) | self 21; in names last 16; mid 3; first 1; alone 1 | tablet 16; Hara:-- 5/21 x2.4; seal face 740 mm2 | as 630 | pala many [3987] | **pal** | many | it lives on records (tablets, tags, pots, copper), not seals | yes (seen while choosing): non-seal objects 16/21 = 76% against 52% for all objects, P 0.0224 |
| 711 | U with an X across the base | self 18; counted 3; in names last 13; mid 4; alone 1 | tablet 21; - 21/21 x2.2; Hara:ETrench 7/8 3/21 x35.0 | slot only | end of the tablet phrase 575-335-711 + three | **?** | tablet word | it lives on records (tablets, tags, pots, copper), not seals | yes (seen while choosing): non-seal objects 21/21 = 100% against 52% for all objects, P 1.24e-06 |
| 382 | pipal leaf on a stalk (plain) | self 17; counted 3; in names first 6; last 6; mid 3; alone 2; counts 031 1; 002 1; 032 1 | tablet 12; Mult 4/20 x11.9; Mohe:DKG. (N) 3/20 x5.3; seal face 714 mm2 | aracu pipal [202] | aracu king [201] | **aracu** | king | seals carrying it are bigger (a high rank) | direction only: seal face median 714 mm2 (n 6) against 605, P 0.101 |
| 320 | stool or ladder with legs | self 18; counted 2; in names mid 12; last 3; first 3; counts 001 1 | seal 13; Bull1 13/20 x2.0; Mohe:DKG. (N) 3/20 x5.3; seal face 853 mm2 | slot only | before 920 in names | **?** | name word | house-mates share it (a house/kin word repeats inside one house) | direction only: same-house pairs 1 against 0.25 by chance (Mohenjo-daro, 9 objects), P 0.22 |
| 167 | arch with a ring at each foot | self 19; in names last 15; alone 3; first 1 | tablet 19; Mult 5/19 x15.6 | slot only | after the U-vessel on tablets | **?** | tablet word | it lives on records (tablets, tags, pots, copper), not seals | yes (seen while choosing): non-seal objects 15/15 = 100% against 52% for all objects, P 6.03e-05 |
| 679 | X-frame with a table top: a cot or seat | relation 10; self 9; in names alone 6; last 3 | seal 16; seal face 713 mm2 | kaṭṭil cot, couch, throne [1145] | kaṭṭil throne: "[name]-kuṭi kaṭṭil" = the seat of the house | **kaṭṭil** | seat, throne | seals carrying it are bigger (a high rank) | yes: seal face median 806 mm2 (n 12) against 605, P 0.0312 |
| 838 | leaf with a branching stalk (second crop) | self 17; load-thing 1; counted 1; in names first 7; mid 5; alone 4; last 1; counts 001 1 | seal 11; Mohe:DKG. (S) 6/19 x2.4; seal face 428 mm2 | eḷ sesame [854] | eḷ sesame; eṇṇey sesame oil [854]; Akkadian ellu sesame oil | **eḷ** | sesame | objects carrying it have no animal (a goods word, not an owner word) | direction only (seen while choosing): objects with no animal 11/19 = 58% against 51% for all objects, P 0.353 |
| 097 | person between two tall bars | self 18; counted 1; in names alone 11; first 5; mid 1; last 1; counts 031 1 | seal 11; Mult 4/19 x12.5; Mohe:DKG. (N) 3/19 x5.5; seal face 534 mm2 | slot only (before porter) | a guarded or enclosed person; kā guard [1416] | **kāppu?** | ward, guard | it lives on records (tablets, tags, pots, copper), not seals | no: non-seal objects 8/19 = 42% against 52% for all objects, P 0.869 |
| 530 | half bow-tie | self 16; counted 2; in names mid 6; first 4; last 3; alone 3 | seal 9; Hara:-- 5/18 x2.8; seal face 1020 mm2 | paṟai drum (mem) | paṟai [4031] | **paṟai** | proclamation | it lives on records (tablets, tags, pots, copper), not seals | no: non-seal objects 9/18 = 50% against 52% for all objects, P 0.668 |
## 2. The marked fish

| fish | uses | sites | animals | counts written before it (value:times) | next sign |
|---|---|---|---|---|---|
| 220 plain | 473 | Mohenjo-daro 200; Harappa 175; Lothal 28; Dholavira 15; Kalibangan 14 | none 206; Bull1 173 | 1:7; 2:77; 3:24; 4:8; 6:16; 7:1 | spear 66; end 63; jar 52 |
| 235 roof | 249 | Mohenjo-daro 141; Harappa 74; Dholavira 9; Chanhu-daro 7; Lothal 7 | Bull1 102; none 88; Gaur 13; Hare 12 | 1:5; 2:18; 3:2 | 240 45; 705 24; 233 23 |
| 240 whiskers | 349 | Harappa 168; Mohenjo-daro 146; Lothal 10; Chanhu-daro 8 | Bull1 153; none 130; Gaur 12 | 1:15; 2:54; 3:2 | spear 46; 233 24; jar 23 |
| 233 bar | 192 | Mohenjo-daro 112; Harappa 50; Lothal 13; Dholavira 7 | Bull1 83; none 65; Gaur 14 | 1:3; 2:12; 3:2 | spear 23; 705 20; 176 9 |
| 231 dot | 94 | Mohenjo-daro 52; Harappa 28; Dholavira 5; Kalibangan 4 | none 39; Bull1 34; Zebu 5 | 2:11; 3:1 | spear 9; 705 8; 017 8 |
| 226 four strokes round | 38 | Mohenjo-daro 23; Harappa 5; Lothal 3 | none 17; Bull1 15 | 2:13; 3:2 | end 27; comb 4 |
| 236 roof + four strokes | 26 | Mohenjo-daro 9; Harappa 8; Lothal 4 | none 12; Bull1 9 | 2:3 | end 11; comb 7 |

Readings (sound column of the table): 235 *vēy-mīn* "Bamboo star" (*vēy* bamboo, to thatch, DEDR 5541; Old Tamil name of the asterism Punarvasu, Parpola's reading, credited); 240 *mī-mīn* "High star" (*mīcai* whiskers 4879 ~ *mī, micai* top, sky 4841); 233 *vari-mīn* "Striped star" (*vari* stripe, line 5263); 231 *puḷḷi-mīn* "Spot star" (*puḷḷi* dot 4327); 226 *kūṭu-mīn* "Gathered star" (*kūṭu* cage 1883 ~ *kūṭu* to assemble 1882); 236 *vēy-kūṭu-mīn*. Plain fish with a number: *iru mīn* "Two-star", *mū mīn* "Three-star", *aṟu mīn* "Six-star" (Pleiades), *ēḻu mīn* "Seven-star" (Great Bear).

What the data says about them:
- Numbers split plain fish from marked fish. The plain fish takes 1 to 7 (6 and 7 are the Pleiades and Great Bear names); the marked fish take 1 to 3 only, and 2 by a wide margin (235 18 of 25, 240 54 of 71, 233 12 of 17, 231 11 of 12, 226 13 of 15). Reading: a marked fish is already a named star, so the only number it takes is "two", which reads as *iru* "the two / pair" of a house (two branches of the Bamboo-star house), or as the opener's pair. Plain fish + number is the star-group name itself.
- Cities: the High-star house 240 leans to Harappa (168 against 146), the Bamboo-star 235 and the Striped-star 233 to Mohenjo-daro (141 against 74; 112 against 50). Two big crests, two cities.
- Houses: by sign alone the four crests repeat inside Mohenjo-daro houses at 38 vs 37.8 (235), 55 vs 47.2 (240), 17 vs 22.1 (233), 2 vs 4.2 (231). The house signal is in the first-name position (15 of 23 same-fish pairs, name-slot job), not in any use of the sign. Rescue in hand: the split test above shows why: a cadet line writes its crest out as `kavar mīn` (415-220, "branch star") instead of the crest sign, so the crest sign alone undercounts the house.
- Animals: 235 goes with the hare (12 uses, hare is rare) and 240 with the "Cros" figure (7); both are copper-tablet animals. Bull1 carries 41% to 44% of the uses of each of the three big crests.

## 3. Openers

- Diamond 861/817 = *kāṇi* (picture: the lozenge is an eye, *kāṇ* "see", DEDR 1443; job word *kāṇi* "the fraction 1/80, a land measure, landed property, possession, hereditary right", *kāṇam* "an ancient weight", DEDR 1444). On tablets "3 diamonds" = three shares, the three men's shares beside three loads (22 of 22). On seals "diamond + 2" = *iru kāṇi*, "two shares": the seal of a holder of a two-share holding. Check: diamond seals name a house (crest first) 35% against 24% for the wheel, P 0.015.
- Wheel 820 = *kāl* (DEDR 1483 *kāl* wheel, cart) ~ *kāl* "quarter" (mem). It takes 1, 2 or 3 and nothing above (138 of 139). "Wheel two" = *iru kāl*, "two quarters": a smaller holding than two shares, on smaller seals.
- `X-060-jar+n` cap. The cap heads (920 crescent with a leaf, 692 outlined X, 550 pincers, 820 wheel) are followed by the 060 mark and then a jar with 1, 2 or 3 strokes, 38 / 10 / 3 times. Reading: 920 is a month sign (crescent; the plain crescent 900 is *tiṅkaḷ* "moon, month", DEDR 3213, counted 3 to 5 with short strokes, 34 short against 0 tall), and jar + n strokes is *n-kuṭi*, "the n-th house/ward". "920-060-741 ..." = "[month], first ward: ..." An opening like "two hands" says what the owner holds; "wheel" says it is a quarter-holding; the cap says which month or ward the seal was issued under.

## 4. Names spelled two ways, and names read whole

`work_data/sound/spell2.csv` lists every pair of names at any site that differ by one sign swapped for two (1,395 distinct names). The swaps that repeat across frames:

| one sign | written as | frames | reading |
|---|---|---|---|
| 233 barred fish | 415-220 pitchfork + plain fish | 7 | *vari-mīn* ~ *kavar mīn*: the fish half kept as *mīn* |
| 235 roofed fish | 803-233 leaf + barred fish | 5 | crest + crest |
| 233 | 235-240 | 5 | one crest for a double crest |
| 235 | 415-220 | 4 | *vēy-mīn* ~ *kavar mīn* |
| 220 plain fish | 798-240 | 3 | *mīn* ~ *maru mīmīn* |
| 233 | 240-220 whisker fish + plain fish | 3 | fish half kept |
| 240 | 415-220 | 3 | fish half kept |
| 176 seated person | 388-443 | 3 | *iṟai* ~ *aracu* + 443 |
| 100 three-headed person | 550-527 | 3 | name-ender swapped for the 550-527 pair |
| 240 | 590-405 | 3 | *mīmīn* ~ *paṭṭi kiḷai* "hamlet kindred" |

Read: the commonest swap is a crest fish for `[mark] + 220`, and the commonest mark-sign is the pitchfork 415 (*kavar* "branch"). `415-220` *kavar mīn* is "the branch of the Star (house)": a cadet line names itself by its parent house's fish written with the plain fish. Same-house pairs: 803-233 ~ 803-415-220 (Harappa), 240-233 ~ 240-415-220 (Mohenjo-daro). Names built only from signs with sounds and read aloud (full list below: 433 distinct names over complete and broken-edged texts; 429 on the complete-text count in point 2): *paṭṭi maṟam* (590-390, 16 objects, 5 sites including Kish) "Warrior of the hamlet", a village-headman type name; *kavar mutu* (415-100, 15 objects) "elder of the branch"; *mīmīn kavar mutu* (240-415-100) "elder of the branch of the High-star house"; *mutal miṉ piṇai* (255-435-690, 12) "chief bound to the Flash"; *koṭi piṇai* (368-690, 8); *vēymīn mīmīn* (235-240, 7); *tiṅkaḷ nāḷ* (900-165, 7) "month, day". Known Old Tamil name elements among them (from memory, not checked): *kō* (king, in Kōvalaṉ, Kōpperuñcōḻaṉ), *vēḷ* (Irunkōvēḷ), *mutu* (Mutukuṭumi), *maṟam* (in Maṟavar), *kiḷai*, *kuṭi* (in village and lineage names ending -kuṭi), *aracu*, *paṭṭi* (village names ending -paṭṭi, very common in Tamil Nadu today), *vēṭṭuvar* (a Tamil hunting caste).

## 5. Checks, what went against, and the rescue plan

30 of 89 came true, 21 right direction, 38 against (fresh only: 10 of 65 true, 17 direction). Against, with numbers: 803 *il* "house" is shared in houses 7 against 12.2 (below chance); 717 *aṭi* "servant" seals are bigger, 730 against 600; 900 *tiṅkaḷ* "month" texts carry a second number less often (25% against 46%); 171 *niṟai* "weight" sits beside a cup face 3 of 12 against 55%; 413 *katir* "ear of grain" sits on mound F 9 of 44 against 34%; 501 *kumi* "heap" 0 of 30 on mound F (all 29 copies are moulded tablets from one Harappa context); 233 and 231 crests not shared by sign alone; 140 *ammai* not shared in houses; 705 *kaḷam*, 550 *vāy*, 575 *kōṭṭai*, 440 *koḷ* not tablet-heavy.
Second tries run (`sound_rescue.py`): 803 read as *il* "wife, mistress of the house" (same entry 494) sits on one object with the woman sign 140 6 times against 3.1 (P 0.09): holds. 900 counted with short strokes 34 against 0: holds, but that fact was already in the counted-things job. 717 *aṭi* as "base, origin, founder" (same entry 72, which fits the big seals) gave no house sharing (1 vs 1.0); 171 house sharing 1 vs 0.6. Next for these: 717 founder → its seals sit lower (older) than house-mates; 171 → its objects sit where cubical weights were found (findspots to be pulled from the excavation reports); 413 *katir* "sun" (1193) rather than "grain" → it pairs with the moon 900.

## 6. Every name read in full (from `work_data/sound/readable_names.csv`)

| name | read | English | objects | sites | example |
|---|---|---|---|---|---|
| 176 | iṟai | tax, levy | 66 | 3 | - |
| 501-240 | kumi mīmīn | heap, stock High-star (pole star) | 29 | 1 | H-1155 |
| 220 | mīn | star | 26 | 7 | - |
| 503-615-752 | malai vayal maka | hill field child of | 26 | 1 | - |
| 415-220 | kavar mīn | branch (of a line) star | 20 | 2 | H-1284 |
| 923 | maru | descendant of | 20 | 2 | H-32 |
| 416 | irukavar | two branches | 20 | 4 | - |
| 440 | koḷ | received, bought | 19 | 2 | - |
| 240 | mīmīn | High-star (pole star) | 17 | 3 | H-1670 |
| 590-390 | paṭṭi maṟam | hamlet, fold warrior | 16 | 5 | Ad-1 |
| 061 | kāl | quarter | 15 | 5 | B-8 |
| 415-100 | kavar mutu | branch (of a line) elder | 15 | 2 | H-188 |
| 235 | vēymīn | Bamboo-star (Punarvasu) | 14 | 6 | - |
| 803 | il | house | 14 | 4 | B-19 |
| 255-435-690 | mutal miṉ piṇai | chief, first flash, bright bound, allied | 12 | 2 | H-1937 |
| 100 | mutu | elder | 12 | 4 | C-17 |
| 390 | maṟam | warrior | 11 | 5 | H-1515 |
| 840 | iṇai | pair, partners | 10 | 3 | G-8 |
| 240-636 | mīmīn pal | High-star (pole star) many | 10 | 2 | H-1178 |
| 255-435-156 | mutal miṉ kā | chief, first flash, bright keeper | 10 | 1 | - |
| 176-100 | iṟai mutu | tax, levy elder | 9 | 2 | H-1080 |
| 798 | maru- | descendant, clan member | 9 | 4 | Blk-6 |
| 540 | paṟai | proclamation | 9 | 4 | C-36 |
| 790 | kaṇ | eye | 9 | 3 | H-1149 |
| 097 | kāppu? | ward, guard | 9 | 2 | H-1860 |
| 630 | pal | many | 9 | 1 | M-1409 |
| 388 | aracu | king, royal | 9 | 3 | H-138 |
| 231-095 | puḷḷimīn kōlaṉ | Spot-star staff-bearer | 8 | 1 | - |
| 368-690 | koṭi piṇai | banner (of a line) bound, allied | 8 | 1 | H-1140 |
| 700 | nāḻi? | cup measure | 8 | 3 | - |
| 233 | varimīn | Striped-star | 8 | 4 | - |
| 226 | kūṭumīn | Cluster-star | 7 | 4 | C-79 |
| 798-415-220 | maru- kavar mīn | descendant, clan member branch (of a line) star | 7 | 2 | H-203 |
| 690 | piṇai | bound, allied | 7 | 2 | K-61 |
| 240-482 | mīmīn kōṭu | High-star (pole star) summit | 7 | 1 | H-1130 |
| 900-165 | tiṅkaḷ nāḷ? | month day | 7 | 2 | H-718 |
| 235-240 | vēymīn mīmīn | Bamboo-star (Punarvasu) High-star (pole star) | 7 | 2 | H-148 |
| 231 | puḷḷimīn | Spot-star | 7 | 4 | C-10 |
| 235-220-176 | vēymīn mīn iṟai | Bamboo-star (Punarvasu) star tax, levy | 7 | 1 | H-1130 |
| 480 | kuṉṟu | hill | 6 | 2 | Ai-2 |
| 503-615 | malai vayal | hill field | 6 | 2 | H-157 |
| 142 | kō | king | 6 | 4 | - |
| 236 | vēykūṭumīn | Bamboo-star cluster | 6 | 4 | - |
| 760 | maka | son/child of | 6 | 2 | H-1043 |
| 240-904 | mīmīn irutiṅkaḷ | High-star (pole star) two months | 5 | 1 | - |
| 240-415-100 | mīmīn kavar mutu | High-star (pole star) branch (of a line) elder | 5 | 2 | - |
| 455 | ampu | arrow | 5 | 3 | - |
| 803-233 | il varimīn | house Striped-star | 5 | 3 | C-67 |
| 900-368 | tiṅkaḷ koṭi | month banner (of a line) | 5 | 1 | H-2131 |
| 717 | aṭi | servant, devotee | 5 | 2 | H-178 |
| 240-482-752 | mīmīn kōṭu maka | High-star (pole star) summit child of | 5 | 1 | H-1793 |
| 705-255 | kaḷam mutal | threshing floor, assembly chief, first | 5 | 2 | H-1840 |
| 125 | vēṭṭuvaṉ | Hunter (clan) | 5 | 3 | C-74 |
| 742 | irukuṭi | second ward | 5 | 4 | - |
| 679 | kaṭṭil | seat, throne | 5 | 3 | C-52 |
| 384 | aracu | king, royal | 4 | 2 | K-448 |
| 413 | katir | grain ear; sun | 4 | 3 | - |
| 255-435 | mutal miṉ | chief, first flash, bright | 4 | 2 | - |
| 877 | nālkāṇi | four shares | 4 | 2 | L-222 |
| 550 | vāy | gate, mouth | 4 | 2 | - |
| 590-405 | paṭṭi kiḷai | hamlet, fold kindred | 4 | 2 | H-134 |
| 233-520 | varimīn vēḷ | Striped-star chief | 4 | 2 | H-1770 |
| 061-142-400 | kāl kō ciṟ | quarter king junior | 4 | 2 | H-1679 |
| 892 | vil | sale, price | 4 | 2 | H-1467 |
| 235-482 | vēymīn kōṭu | Bamboo-star (Punarvasu) summit | 4 | 3 | C-59 |
| 240-100 | mīmīn mutu | High-star (pole star) elder | 4 | 2 | C-51 |
| 415 | kavar | branch (of a line) | 4 | 3 | Blk-5 |
| 405 | kiḷai | kindred | 4 | 3 | C-87 |
| 590 | paṭṭi | hamlet, fold | 3 | 2 | - |
| 220-236 | mīn vēykūṭumīn | star Bamboo-star cluster | 3 | 1 | H-1124 |
| 240-176 | mīmīn iṟai | High-star (pole star) tax, levy | 3 | 2 | H-2200 |
| 156 | kā | keeper | 3 | 1 | H-1287 |
| 061-255 | kāl mutal | quarter chief, first | 3 | 1 | H-2123 |
| 175 | iṟai | tax | 3 | 2 | - |
| 440-760 | koḷ maka | received, bought son/child of | 3 | 2 | H-101 |
| 125-700 | vēṭṭuvaṉ nāḻi? | Hunter (clan) cup measure | 3 | 1 | H-1178 |
| 575 | kōṭṭai | great measure; fort | 3 | 2 | L-54 |
| 368 | koṭi | banner (of a line) | 3 | 2 | H-54 |
| 706 | kaḷam | assembly place | 3 | 2 | - |
| 240-636-690 | mīmīn pal piṇai | High-star (pole star) many bound, allied | 3 | 1 | H-1308 |
| 240-233 | mīmīn varimīn | High-star (pole star) Striped-star | 3 | 2 | H-1678 |
| 240-760 | mīmīn maka | High-star (pole star) son/child of | 3 | 1 | H-2076 |
| 850 | kaṇ | eye, sight | 3 | 3 | H-1126 |
| 407 | kiḷai | herd, flock | 3 | 2 | H-1714 |
| 832 | kaṇ | eye | 3 | 3 | H-602 |
| 235-176 | vēymīn iṟai | Bamboo-star (Punarvasu) tax, levy | 3 | 2 | H-1997 |
| 090 | āḷ | manager | 3 | 1 | H-1101 |
| 235-590-390 | vēymīn paṭṭi maṟam | Bamboo-star (Punarvasu) hamlet, fold warrior | 3 | 2 | H-1107 |
| 233-585-407 | varimīn kaṉṉi? kiḷai | Striped-star maiden (of the Seven) herd, flock | 3 | 1 | M-513 |
| 745-700 | mukuṭi nāḻi? | third ward cup measure | 3 | 1 | H-1793 |
| 091-368 | iruvar koṭi | the pair, partners banner (of a line) | 3 | 1 | H-1861 |
| 460 | mukkōṭu | Three-peaks | 3 | 2 | - |
| 503-460 | malai mukkōṭu | hill Three-peaks | 3 | 1 | M-1307 |
| 231-798-176 | puḷḷimīn maru- iṟai | Spot-star descendant, clan member tax, levy | 3 | 1 | H-171 |
| 400 | ciṟ | junior | 3 | 2 | C-15 |
| 233-176 | varimīn iṟai | Striped-star tax, levy | 3 | 2 | L-35 |
| 240-590-390 | mīmīn paṭṭi maṟam | High-star (pole star) hamlet, fold warrior | 3 | 1 | H-194 |
| 220-440-154 | mīn koḷ kā | star received, bought keeper | 2 | 1 | H-1142 |
| 520 | vēḷ | chief | 2 | 1 | H-1121 |
| 220-100 | mīn mutu | star elder | 2 | 2 | L-38 |
| 900 | tiṅkaḷ | month | 2 | 2 | K-9 |
| 390-590 | maṟam paṭṭi | warrior hamlet, fold | 2 | 2 | K-39 |
| 165 | nāḷ? | day | 2 | 2 | K-56 |
| 832-255-070 | kaṇ mutal ampu | eye chief, first arrow | 2 | 2 | H-1916 |
| 175-176-100 | iṟai iṟai mutu | tax tax, levy elder | 2 | 1 | H-741 |
| 382-760 | aracu maka | king son/child of | 2 | 1 | H-1850 |
| 061-142 | kāl kō | quarter king | 2 | 1 | M-164 |
| 798-231-904-100 | maru- puḷḷimīn irutiṅkaḷ mutu | descendant, clan member Spot-star two months elder | 2 | 1 | M-1568 |
| 235-233 | vēymīn varimīn | Bamboo-star (Punarvasu) Striped-star | 2 | 2 | H-141 |
| 920 | tiṅkaḷ? | month (head of a date formula) | 2 | 2 | - |
| 798-233-790-900 | maru- varimīn kaṇ tiṅkaḷ | descendant, clan member Striped-star eye month | 2 | 1 | M-121 |
| 482 | kōṭu | summit | 2 | 2 | L-207 |
| 615 | vayal | field | 2 | 1 | M-1596 |
| 140-850 | ammai kaṇ | mother, lady eye, sight | 2 | 1 | M-490 |
| 240-803-585 | mīmīn il kaṉṉi? | High-star (pole star) house maiden (of the Seven) | 2 | 1 | M-2030 |
| 838-798-176 | eḷ maru- iṟai | sesame descendant, clan member tax, levy | 2 | 1 | M-494 |
| 741-904 | orukuṭi irutiṅkaḷ | first ward two months | 2 | 1 | M-494 |
| 382 | aracu | king | 2 | 1 | H-1102 |
| 220-142-590-455 | mīn kō paṭṭi ampu | star king hamlet, fold arrow | 2 | 1 | H-2127 |
| 741-803 | orukuṭi il | first ward house | 2 | 2 | H-776 |
| 416-840 | irukavar iṇai | two branches pair, partners | 2 | 2 | - |
| 790-717 | kaṇ aṭi | eye servant, devotee | 2 | 1 | H-764 |
| 440-100 | koḷ mutu | received, bought elder | 2 | 1 | H-757 |
| 235-798 | vēymīn maru- | Bamboo-star (Punarvasu) descendant, clan member | 2 | 1 | M-1705 |
| 140-061 | ammai kāl | mother, lady quarter | 2 | 1 | H-1894 |
| 590-892 | paṭṭi vil | hamlet, fold sale, price | 2 | 2 | H-1691 |
| 231-176 | puḷḷimīn iṟai | Spot-star tax, levy | 2 | 1 | H-2140 |
| 540-540 | paṟai paṟai | proclamation proclamation | 2 | 1 | H-1740 |
| 220-690 | mīn piṇai | star bound, allied | 2 | 1 | H-2019 |
| 125-390 | vēṭṭuvaṉ maṟam | Hunter (clan) warrior | 2 | 2 | H-55 |
| 495-615 | kompu vayal | branch field | 2 | 2 | H-838 |
| 235-240-455 | vēymīn mīmīn ampu | Bamboo-star (Punarvasu) High-star (pole star) arrow | 2 | 1 | M-1096 |
| 153 | kā | keeper | 2 | 2 | - |
| 235-904 | vēymīn irutiṅkaḷ | Bamboo-star (Punarvasu) two months | 2 | 2 | Ad-3 |
| 220-095 | mīn kōlaṉ | star staff-bearer | 2 | 1 | M-2053 |
| 700-892 | nāḻi? vil | cup measure sale, price | 2 | 2 | C-80 |
| 140 | ammai | mother, lady | 2 | 1 | H-1677 |
| 231-255-435-690 | puḷḷimīn mutal miṉ piṇai | Spot-star chief, first flash, bright bound, allied | 2 | 1 | - |
| 904 | irutiṅkaḷ | two months | 2 | 1 | M-1137 |
| 220-240 | mīn mīmīn | star High-star (pole star) | 2 | 2 | - |
| 235-240-255-435-690 | vēymīn mīmīn mutal miṉ piṇai | Bamboo-star (Punarvasu) High-star (pole star) chief, first flash, bright bound, allied | 2 | 1 | M-377 |
| 745 | mukuṭi | third ward | 2 | 1 | M-1822 |
| 705-760 | kaḷam maka | threshing floor, assembly son/child of | 2 | 1 | M-754 |
| 803-235 | il vēymīn | house Bamboo-star (Punarvasu) | 2 | 2 | C-4 |
| 503-463 | malai mukkōṭu | hill Three-peaks | 2 | 2 | C-94 |
| 838-482 | eḷ kōṭu | sesame summit | 2 | 1 | M-2086 |
| 240-838-585 | mīmīn eḷ kaṉṉi? | High-star (pole star) sesame maiden (of the Seven) | 2 | 1 | M-1651 |
| 705-390 | kaḷam maṟam | threshing floor, assembly warrior | 2 | 2 | - |
| 416-220-760 | irukavar mīn maka | two branches star son/child of | 2 | 1 | H-1191 |
| 055 | paṉṉiru | twelve | 2 | 1 | M-18 |
| 590-407 | paṭṭi kiḷai | hamlet, fold herd, flock | 2 | 2 | Hls-1 |
| 142-400 | kō ciṟ | king junior | 2 | 2 | H-1672 |
| 233-803 | varimīn il | Striped-star house | 2 | 2 | Jk-2 |
| 705 | kaḷam | threshing floor, assembly | 2 | 2 | M-223 |
| 590-390-820 | paṭṭi maṟam kāl | hamlet, fold warrior quarter-share | 2 | 2 | - |
| 705-717-388 | kaḷam aṭi aracu | threshing floor, assembly servant, devotee king, royal | 2 | 2 | - |
| 752 | maka | child of | 2 | 1 | M-1514 |
| 240-415-220 | mīmīn kavar mīn | High-star (pole star) branch (of a line) star | 1 | 1 | M-1814 |
| 803-240-220 | il mīmīn mīn | house High-star (pole star) star | 1 | 1 | M-1716 |
| 255-070-741 | mutal ampu orukuṭi | chief, first arrow first ward | 1 | 1 | M-1780 |
| 904-415-100 | irutiṅkaḷ kavar mutu | two months branch (of a line) elder | 1 | 1 | M-495 |
| 416-255-220-798-100 | irukavar mutal mīn maru- mutu | two branches chief, first star descendant, clan member elder | 1 | 1 | M-91 |
| 255 | mutal | chief, first | 1 | 1 | M-1855 |
| 920-255 | tiṅkaḷ? mutal | month (head of a date formula) chief, first | 1 | 1 | M-146 |
| 790-390-741-590-390 | kaṇ maṟam orukuṭi paṭṭi maṟam | eye warrior first ward hamlet, fold warrior | 1 | 1 | M-131 |
| 176-741-220 | iṟai orukuṭi mīn | tax, levy first ward star | 1 | 1 | M-127 |
| 416-840-760 | irukavar iṇai maka | two branches pair, partners son/child of | 1 | 1 | M-28 |
| 368-220 | koṭi mīn | banner (of a line) star | 1 | 1 | M-1687 |
| 055-803-220 | paṉṉiru il mīn | twelve house star | 1 | 1 | M-117 |
| 235-803 | vēymīn il | Bamboo-star (Punarvasu) house | 1 | 1 | M-1845 |
| 125-861 | vēṭṭuvaṉ kāṇi | Hunter (clan) share, holding (a "hand") | 1 | 1 | M-1903 |
| 803-233-520 | il varimīn vēḷ | house Striped-star chief | 1 | 1 | M-1781 |
| 125-390-240-255-435-690 | vēṭṭuvaṉ maṟam mīmīn mutal miṉ piṇai | Hunter (clan) warrior High-star (pole star) chief, first flash, bright bound, allied | 1 | 1 | M-38 |
| 503-455-220-235-240-055 | malai ampu mīn vēymīn mīmīn paṉṉiru | hill arrow star Bamboo-star (Punarvasu) High-star (pole star) twelve | 1 | 1 | M-29 |
| 233-382 | varimīn aracu | Striped-star king | 1 | 1 | M-33 |
| 717-255-435-690 | aṭi mutal miṉ piṇai | servant, devotee chief, first flash, bright bound, allied | 1 | 1 | M-1667 |
| 235-415-220 | vēymīn kavar mīn | Bamboo-star (Punarvasu) branch (of a line) star | 1 | 1 | M-323 |
| 125-390-741-176 | vēṭṭuvaṉ maṟam orukuṭi iṟai | Hunter (clan) warrior first ward tax, levy | 1 | 1 | M-320 |
| 235-231 | vēymīn puḷḷimīn | Bamboo-star (Punarvasu) Spot-star | 1 | 1 | M-302 |
| 368-142 | koṭi kō | banner (of a line) king | 1 | 1 | M-282 |
| 820 | kāl | quarter-share | 1 | 1 | M-326 |
| 520-455-220-226 | vēḷ ampu mīn kūṭumīn | chief arrow star Cluster-star | 1 | 1 | M-147 |
| 679-630 | kaṭṭil pal | seat, throne many | 1 | 1 | M-267 |
| 632-233-235-798 | pal varimīn vēymīn maru- | many Striped-star Bamboo-star (Punarvasu) descendant, clan member | 1 | 1 | M-266 |
| 803-220-176 | il mīn iṟai | house star tax, levy | 1 | 1 | M-249 |
| 233-055-752 | varimīn paṉṉiru maka | Striped-star twelve child of | 1 | 1 | M-397 |
| 840-760 | iṇai maka | pair, partners son/child of | 1 | 1 | M-162 |
| 540-240 | paṟai mīmīn | proclamation High-star (pole star) | 1 | 1 | M-393 |
| 904-832 | irutiṅkaḷ kaṇ | two months eye | 1 | 1 | M-205 |
| 176-415-100 | iṟai kavar mutu | tax, levy branch (of a line) elder | 1 | 1 | M-595 |
| 165-100 | nāḷ? mutu | day elder | 1 | 1 | M-211 |
| 803-233-240 | il varimīn mīmīn | house Striped-star High-star (pole star) | 1 | 1 | M-236 |
| 233-235-503 | varimīn vēymīn malai | Striped-star Bamboo-star (Punarvasu) hill | 1 | 1 | M-246 |
| 798-055 | maru- paṉṉiru | descendant, clan member twelve | 1 | 1 | M-381 |
| 233-100 | varimīn mutu | Striped-star elder | 1 | 1 | M-375 |
| 590-415-100 | paṭṭi kavar mutu | hamlet, fold branch (of a line) elder | 1 | 1 | M-248 |
| 803-390-832 | il maṟam kaṇ | house warrior eye | 1 | 1 | M-77 |
| 142-157 | kō kā | king keeper | 1 | 1 | M-328 |
| 700-231 | nāḻi? puḷḷimīn | cup measure Spot-star | 1 | 1 | M-86 |
| 236-061-405 | vēykūṭumīn kāl kiḷai | Bamboo-star cluster quarter kindred | 1 | 1 | M-1978 |
| 877-061 | nālkāṇi kāl | four shares quarter | 1 | 1 | M-1818 |
| 235-240-226 | vēymīn mīmīn kūṭumīn | Bamboo-star (Punarvasu) High-star (pole star) Cluster-star | 1 | 1 | M-1738 |
| 220-798 | mīn maru- | star descendant, clan member | 1 | 1 | M-1768 |
| 798-415-220-752-407 | maru- kavar mīn maka kiḷai | descendant, clan member branch (of a line) star child of herd, flock | 1 | 1 | M-1954 |
| 861 | kāṇi | share, holding (a "hand") | 1 | 1 | M-389 |
| 235-590-407 | vēymīn paṭṭi kiḷai | Bamboo-star (Punarvasu) hamlet, fold herd, flock | 1 | 1 | M-1310 |
| 706-820-595 | kaḷam kāl paṭṭi | assembly place quarter-share fold | 1 | 1 | M-1290 |
| 091 | iruvar | the pair, partners | 1 | 1 | - |
| 390-390-390 | maṟam maṟam maṟam | warrior warrior warrior | 1 | 1 | M-2094 |
| 790-153 | kaṇ kā | eye keeper | 1 | 1 | M-1376 |
| 741-840-390 | orukuṭi iṇai maṟam | first ward pair, partners warrior | 1 | 1 | - |
| 390-368 | maṟam koṭi | warrior banner (of a line) | 1 | 1 | Ad-2 |
| 790-390 | kaṇ maṟam | eye warrior | 1 | 1 | Ns-46 |
| 632-140-706 | pal ammai kaḷam | many mother, lady assembly place | 1 | 1 | M-8 |
| 415-390 | kavar maṟam | branch (of a line) warrior | 1 | 1 | Alt-90 |
| 390-741-440 | maṟam orukuṭi koḷ | warrior first ward received, bought | 1 | 1 | M-746 |
| 803-236-140 | il vēykūṭumīn ammai | house Bamboo-star cluster mother, lady | 1 | 1 | M-726 |
| 240-585 | mīmīn kaṉṉi? | High-star (pole star) maiden (of the Seven) | 1 | 1 | M-722 |
| 140-390 | ammai maṟam | mother, lady warrior | 1 | 1 | M-708 |
| 235-590-405 | vēymīn paṭṭi kiḷai | Bamboo-star (Punarvasu) hamlet, fold kindred | 1 | 1 | M-672 |
| 231-440 | puḷḷimīn koḷ | Spot-star received, bought | 1 | 1 | M-666 |
| 055-368 | paṉṉiru koṭi | twelve banner (of a line) | 1 | 1 | M-836 |
| 900-590-390 | tiṅkaḷ paṭṭi maṟam | month hamlet, fold warrior | 1 | 1 | M-834 |
| 231-585 | puḷḷimīn kaṉṉi? | Spot-star maiden (of the Seven) | 1 | 1 | K-145 |
| 235-233-550 | vēymīn varimīn vāy | Bamboo-star (Punarvasu) Striped-star gate, mouth | 1 | 1 | M-1113 |
| 803-233-760 | il varimīn maka | house Striped-star son/child of | 1 | 1 | M-1079 |
| 095-595 | kōlaṉ paṭṭi | staff-bearer fold | 1 | 1 | M-1052 |
| 140-920-575-705-590 | ammai tiṅkaḷ? kōṭṭai kaḷam paṭṭi | mother, lady month (head of a date formula) great measure; fort threshing floor, assembly hamlet, fold | 1 | 1 | M-997 |
| 690-904 | piṇai irutiṅkaḷ | bound, allied two months | 1 | 1 | M-994 |
| 803-235-233-070 | il vēymīn varimīn ampu | house Bamboo-star (Punarvasu) Striped-star arrow | 1 | 1 | M-985 |
| 798-440-752 | maru- koḷ maka | descendant, clan member received, bought child of | 1 | 1 | M-1275 |
| 706-717-388 | kaḷam aṭi aracu | assembly place servant, devotee king, royal | 1 | 1 | M-1270 |
| 255-220-175-760 | mutal mīn iṟai maka | chief, first star tax son/child of | 1 | 1 | - |
| 233-235 | varimīn vēymīn | Striped-star Bamboo-star (Punarvasu) | 1 | 1 | M-1226 |
| 240-923 | mīmīn maru | High-star (pole star) descendant of | 1 | 1 | M-1166 |
| 140-920 | ammai tiṅkaḷ? | mother, lady month (head of a date formula) | 1 | 1 | M-1165 |
| 233-255-435-690 | varimīn mutal miṉ piṇai | Striped-star chief, first flash, bright bound, allied | 1 | 1 | M-1156 |
| 803-900 | il tiṅkaḷ | house month | 1 | 1 | - |
| 382-382-382 | aracu aracu aracu | king king king | 1 | 1 | - |
| 055-220-091 | paṉṉiru mīn iruvar | twelve star the pair, partners | 1 | 1 | - |
| 091-220 | iruvar mīn | the pair, partners star | 1 | 1 | - |
| 061-706-798 | kāl kaḷam maru- | quarter assembly place descendant, clan member | 1 | 1 | - |
| 176-455 | iṟai ampu | tax, levy arrow | 1 | 1 | M-1268 |
| 615-503-460 | vayal malai mukkōṭu | field hill Three-peaks | 1 | 1 | M-937 |
| 240-233-503 | mīmīn varimīn malai | High-star (pole star) Striped-star hill | 1 | 1 | H-1052 |
| 798-240-220 | maru- mīmīn mīn | descendant, clan member High-star (pole star) star | 1 | 1 | H-423 |
| 415-220-140 | kavar mīn ammai | branch (of a line) star mother, lady | 1 | 1 | M-412 |
| 061-407 | kāl kiḷai | quarter herd, flock | 1 | 1 | M-408 |
| 235-055 | vēymīn paṉṉiru | Bamboo-star (Punarvasu) twelve | 1 | 1 | M-399 |
| 700-415 | nāḻi? kavar | cup measure branch (of a line) | 1 | 1 | H-1881 |
| 435 | miṉ | flash, bright | 1 | 1 | H-1924 |
| 165-590 | nāḷ? paṭṭi | day hamlet, fold | 1 | 1 | M-828 |
| 165-400-255 | nāḷ? ciṟ mutal | day junior chief, first | 1 | 1 | H-1077 |
| 233-220 | varimīn mīn | Striped-star star | 1 | 1 | H-2035 |
| 240-630 | mīmīn pal | High-star (pole star) many | 1 | 1 | H-2192 |
| 832-235 | kaṇ vēymīn | eye Bamboo-star (Punarvasu) | 1 | 1 | H-2015 |
| 240-220-717 | mīmīn mīn aṭi | High-star (pole star) star servant, devotee | 1 | 1 | M-651 |
| 233-235-100 | varimīn vēymīn mutu | Striped-star Bamboo-star (Punarvasu) elder | 1 | 1 | M-647 |
| 745-235-240-055-482 | mukuṭi vēymīn mīmīn paṉṉiru kōṭu | third ward Bamboo-star (Punarvasu) High-star (pole star) twelve summit | 1 | 1 | M-638 |
| 798-240-176 | maru- mīmīn iṟai | descendant, clan member High-star (pole star) tax, levy | 1 | 1 | M-629 |
| 530-798-415-220-176-175-760 | paṟai maru- kavar mīn iṟai iṟai maka | proclamation descendant, clan member branch (of a line) star tax, levy tax son/child of | 1 | 1 | M-623 |
| 803-415-231 | il kavar puḷḷimīn | house branch (of a line) Spot-star | 1 | 1 | H-1027 |
| 803-240-233 | il mīmīn varimīn | house High-star (pole star) Striped-star | 1 | 1 | M-819 |
| 798-233-070 | maru- varimīn ampu | descendant, clan member Striped-star arrow | 1 | 1 | M-815 |
| 803-235-240-176 | il vēymīn mīmīn iṟai | house Bamboo-star (Punarvasu) High-star (pole star) tax, levy | 1 | 1 | M-814 |
| 706-140-368 | kaḷam ammai koṭi | assembly place mother, lady banner (of a line) | 1 | 1 | M-796 |
| 798-240-235-388 | maru- mīmīn vēymīn aracu | descendant, clan member High-star (pole star) Bamboo-star (Punarvasu) king, royal | 1 | 1 | M-793 |
| 803-923 | il maru | house descendant of | 1 | 1 | M-917 |
| 838-798-415-220-233-590-390 | eḷ maru- kavar mīn varimīn paṭṭi maṟam | sesame descendant, clan member branch (of a line) star Striped-star hamlet, fold warrior | 1 | 1 | M-900 |
| 368-231-520-495-590-070-892 | koṭi puḷḷimīn vēḷ kompu paṭṭi ampu vil | banner (of a line) Spot-star chief branch hamlet, fold arrow sale, price | 1 | 1 | M-894 |
| 125-390-741 | vēṭṭuvaṉ maṟam orukuṭi | Hunter (clan) warrior first ward | 1 | 1 | M-878 |
| 798-415-220-176 | maru- kavar mīn iṟai | descendant, clan member branch (of a line) star tax, levy | 1 | 1 | M-943 |
| 742-760 | irukuṭi maka | second ward son/child of | 1 | 1 | M-862 |
| 615-550 | vayal vāy | field gate, mouth | 1 | 1 | M-849 |
| 575-125-741-142 | kōṭṭai vēṭṭuvaṉ orukuṭi kō | great measure; fort Hunter (clan) first ward king | 1 | 1 | M-837 |
| 413-220-440 | katir mīn koḷ | grain ear; sun star received, bought | 1 | 1 | M-1632 |
| 235-240-220 | vēymīn mīmīn mīn | Bamboo-star (Punarvasu) High-star (pole star) star | 1 | 1 | M-962 |
| 503-460-158 | malai mukkōṭu kā | hill Three-peaks keeper | 1 | 1 | M-961 |
| 575-590 | kōṭṭai paṭṭi | great measure; fort hamlet, fold | 1 | 1 | M-960 |
| 803-236 | il vēykūṭumīn | house Bamboo-star cluster | 1 | 1 | M-959 |
| 233-923 | varimīn maru | Striped-star descendant of | 1 | 1 | M-945 |
| 220-231 | mīn puḷḷimīn | star Spot-star | 1 | 1 | M-868 |
| 382-760-382 | aracu maka aracu | king son/child of king | 1 | 1 | H-1967 |
| 717-415-100 | aṭi kavar mutu | servant, devotee branch (of a line) elder | 1 | 1 | H-2174 |
| 741-368 | orukuṭi koṭi | first ward banner (of a line) | 1 | 1 | H-1898 |
| 240-463-220-590-390 | mīmīn mukkōṭu mīn paṭṭi maṟam | High-star (pole star) Three-peaks star hamlet, fold warrior | 1 | 1 | - |
| 803-240-415-220 | il mīmīn kavar mīn | house High-star (pole star) branch (of a line) star | 1 | 1 | H-1953 |
| 220-176 | mīn iṟai | star tax, levy | 1 | 1 | H-1825 |
| 832-255-070-752 | kaṇ mutal ampu maka | eye chief, first arrow child of | 1 | 1 | H-2021 |
| 175-752 | iṟai maka | tax child of | 1 | 1 | H-2022 |
| 575-590-741-240 | kōṭṭai paṭṭi orukuṭi mīmīn | great measure; fort hamlet, fold first ward High-star (pole star) | 1 | 1 | M-1900 |
| 231-390-100 | puḷḷimīn maṟam mutu | Spot-star warrior elder | 1 | 1 | H-2197 |
| 055-255-435-690 | paṉṉiru mutal miṉ piṇai | twelve chief, first flash, bright bound, allied | 1 | 1 | H-1797 |
| 233-236 | varimīn vēykūṭumīn | Striped-star Bamboo-star cluster | 1 | 1 | H-1873 |
| 090-400 | āḷ ciṟ | manager junior | 1 | 1 | H-1906 |
| 495-817 | kompu kāṇi | branch share, holding | 1 | 1 | H-2373 |
| 235-923 | vēymīn maru | Bamboo-star (Punarvasu) descendant of | 1 | 1 | H-1903 |
| 061-760 | kāl maka | quarter son/child of | 1 | 1 | H-1975 |
| 803-233-176-435-690 | il varimīn iṟai miṉ piṇai | house Striped-star tax, levy flash, bright bound, allied | 1 | 1 | H-1842 |
| 705-630-175-100 | kaḷam pal iṟai mutu | threshing floor, assembly many tax elder | 1 | 1 | H-1839 |
| 690-158 | piṇai kā | bound, allied keeper | 1 | 1 | H-2185 |
| 741-700 | orukuṭi nāḻi? | first ward cup measure | 1 | 1 | H-2211 |
| 690-154 | piṇai kā | bound, allied keeper | 1 | 1 | H-1844 |
| 175-817 | iṟai kāṇi | tax share, holding | 1 | 1 | H-1182 |
| 798-240-231-904 | maru- mīmīn puḷḷimīn irutiṅkaḷ | descendant, clan member High-star (pole star) Spot-star two months | 1 | 1 | H-1705 |
| 142-151 | kō kā | king keeper | 1 | 1 | H-1995 |
| 482-752 | kōṭu maka | summit child of | 1 | 1 | H-47 |
| 892-798-235 | vil maru- vēymīn | sale, price descendant, clan member Bamboo-star (Punarvasu) | 1 | 1 | H-44 |
| 235-231-752 | vēymīn puḷḷimīn maka | Bamboo-star (Punarvasu) Spot-star child of | 1 | 1 | H-58 |
| 798-240-231-388 | maru- mīmīn puḷḷimīn aracu | descendant, clan member High-star (pole star) Spot-star king, royal | 1 | 1 | H-26 |
| 503-615-760 | malai vayal maka | hill field son/child of | 1 | 1 | H-13 |
| 235-240-220-803-255-435-690 | vēymīn mīmīn mīn il mutal miṉ piṇai | Bamboo-star (Punarvasu) High-star (pole star) star house chief, first flash, bright bound, allied | 1 | 1 | H-12 |
| 503-861-368 | malai kāṇi koṭi | hill share, holding (a "hand") banner (of a line) | 1 | 1 | H-139 |
| 798-231-233 | maru- puḷḷimīn varimīn | descendant, clan member Spot-star Striped-star | 1 | 1 | H-132 |
| 741-240-630 | orukuṭi mīmīn pal | first ward High-star (pole star) many | 1 | 1 | H-102 |
| 741 | orukuṭi | first ward | 1 | 1 | H-102 |
| 741-455-220 | orukuṭi ampu mīn | first ward arrow star | 1 | 1 | H-82 |
| 717-100 | aṭi mutu | servant, devotee elder | 1 | 1 | H-63 |
| 235-240-231-590-390 | vēymīn mīmīn puḷḷimīn paṭṭi maṟam | Bamboo-star (Punarvasu) High-star (pole star) Spot-star hamlet, fold warrior | 1 | 1 | H-39 |
| 240-503-070 | mīmīn malai ampu | High-star (pole star) hill arrow | 1 | 1 | M-1727 |
| 861-368 | kāṇi koṭi | share, holding (a "hand") banner (of a line) | 1 | 1 | H-1022 |
| 235-100 | vēymīn mutu | Bamboo-star (Punarvasu) elder | 1 | 1 | - |
| 850-231 | kaṇ puḷḷimīn | eye, sight Spot-star | 1 | 1 | - |
| 175-742-233-798 | iṟai irukuṭi varimīn maru- | tax second ward Striped-star descendant, clan member | 1 | 1 | - |
| 904-530-231-590-390 | irutiṅkaḷ paṟai puḷḷimīn paṭṭi maṟam | two months proclamation Spot-star hamlet, fold warrior | 1 | 1 | - |
| 530-413 | paṟai katir | proclamation grain ear; sun | 1 | 1 | H-1511 |
| 705-840 | kaḷam iṇai | threshing floor, assembly pair, partners | 1 | 1 | M-2080 |
| 097-151 | kāppu? kā | ward, guard keeper | 1 | 1 | H-1917 |
| 388-920 | aracu tiṅkaḷ? | king, royal month (head of a date formula) | 1 | 1 | M-1128 |
| 220-235 | mīn vēymīn | star Bamboo-star (Punarvasu) | 1 | 1 | - |
| 175-741-233-798 | iṟai orukuṭi varimīn maru- | tax first ward Striped-star descendant, clan member | 1 | 1 | M-786 |
| 590-407-100 | paṭṭi kiḷai mutu | hamlet, fold herd, flock elder | 1 | 1 | - |
| 407-590 | kiḷai paṭṭi | herd, flock hamlet, fold | 1 | 1 | - |
| 495-460 | kompu mukkōṭu | branch Three-peaks | 1 | 1 | - |
| 440-790-407-590 | koḷ kaṇ kiḷai paṭṭi | received, bought eye herd, flock hamlet, fold | 1 | 1 | Dlp-2 |
| 495-790 | kompu kaṇ | branch eye | 1 | 1 | C-20 |
| 240-803-233 | mīmīn il varimīn | High-star (pole star) house Striped-star | 1 | 1 | C-9 |
| 590-390-741-923 | paṭṭi maṟam orukuṭi maru | hamlet, fold warrior first ward descendant of | 1 | 1 | M-968 |
| 415-240-495-463-752 | kavar mīmīn kompu mukkōṭu maka | branch (of a line) High-star (pole star) branch Three-peaks child of | 1 | 1 | H-2021 |
| 520-382 | vēḷ aracu | chief king | 1 | 1 | - |
| 175-090-705 | iṟai āḷ kaḷam | tax manager threshing floor, assembly | 1 | 1 | M-1629 |
| 233-798 | varimīn maru- | Striped-star descendant, clan member | 1 | 1 | M-1461 |
| 590-405-100 | paṭṭi kiḷai mutu | hamlet, fold kindred elder | 1 | 1 | M-1457 |
| 920-540 | tiṅkaḷ? paṟai | month (head of a date formula) proclamation | 1 | 1 | M-1379 |
| 070 | ampu | arrow | 1 | 1 | M-1317 |
| 838-923 | eḷ maru | sesame descendant of | 1 | 1 | Grb-1 |
| 233-440 | varimīn koḷ | Striped-star received, bought | 1 | 1 | M-1894 |
| 415-803 | kavar il | branch (of a line) house | 1 | 1 | - |
| 233-555 | varimīn vāy | Striped-star gate | 1 | 1 | ?-5 |
| 900-590 | tiṅkaḷ paṭṭi | month hamlet, fold | 1 | 1 | ?-3 |
| 240-231-585 | mīmīn puḷḷimīn kaṉṉi? | High-star (pole star) Spot-star maiden (of the Seven) | 1 | 1 | - |
| 415-226 | kavar kūṭumīn | branch (of a line) Cluster-star | 1 | 1 | Rpr-1 |
| 255-798 | mutal maru- | chief, first descendant, clan member | 1 | 1 | Nd-2 |
| 550-233 | vāy varimīn | gate, mouth Striped-star | 1 | 1 | M-1973 |
| 530 | paṟai | proclamation | 1 | 1 | M-1929 |
| 455-590 | ampu paṭṭi | arrow hamlet, fold | 1 | 1 | M-1909 |
| 803-482 | il kōṭu | house summit | 1 | 1 | M-1698 |
| 235-240-923 | vēymīn mīmīn maru | Bamboo-star (Punarvasu) High-star (pole star) descendant of | 1 | 1 | M-1760 |
| 220-240-440-760 | mīn mīmīn koḷ maka | star High-star (pole star) received, bought son/child of | 1 | 1 | M-1990 |
| 240-495-615 | mīmīn kompu vayal | High-star (pole star) branch field | 1 | 1 | M-1726 |
| 235-388 | vēymīn aracu | Bamboo-star (Punarvasu) king, royal | 1 | 1 | M-1817 |
| 231-798 | puḷḷimīn maru- | Spot-star descendant, clan member | 1 | 1 | M-1804 |
| 235-240-055 | vēymīn mīmīn paṉṉiru | Bamboo-star (Punarvasu) High-star (pole star) twelve | 1 | 1 | M-1885 |
| 140-416 | ammai irukavar | mother, lady two branches | 1 | 1 | M-1741 |
| 140-900-390-741-838 | ammai tiṅkaḷ maṟam orukuṭi eḷ | mother, lady month warrior first ward sesame | 1 | 1 | M-1821 |
| 741-530-390-798 | orukuṭi paṟai maṟam maru- | first ward proclamation warrior descendant, clan member | 1 | 1 | H-773 |
| 415-220-717 | kavar mīn aṭi | branch (of a line) star servant, devotee | 1 | 1 | M-1680 |
| 832-798 | kaṇ maru- | eye descendant, clan member | 1 | 1 | M-1681 |
| 142-904 | kō irutiṅkaḷ | king two months | 1 | 1 | M-1686 |
| 803-798-415-220 | il maru- kavar mīn | house descendant, clan member branch (of a line) star | 1 | 1 | M-707 |
| 140-176 | ammai iṟai | mother, lady tax, levy | 1 | 1 | M-2098 |
| 390-090-390-176 | maṟam āḷ maṟam iṟai | warrior manager warrior tax, levy | 1 | 1 | M-1770 |
| 741-530-455-220-176-100 | orukuṭi paṟai ampu mīn iṟai mutu | first ward proclamation arrow star tax, levy elder | 1 | 1 | K-7 |
| 125-741-803-240-233 | vēṭṭuvaṉ orukuṭi il mīmīn varimīn | Hunter (clan) first ward house High-star (pole star) Striped-star | 1 | 1 | K-5 |
| 240-235 | mīmīn vēymīn | High-star (pole star) Bamboo-star (Punarvasu) | 1 | 1 | H-954 |
| 920-156-100 | tiṅkaḷ? kā mutu | month (head of a date formula) keeper elder | 1 | 1 | M-1810 |
| 745-125 | mukuṭi vēṭṭuvaṉ | third ward Hunter (clan) | 1 | 1 | M-1700 |
| 231-803 | puḷḷimīn il | Spot-star house | 1 | 1 | M-69 |
| 575-220 | kōṭṭai mīn | great measure; fort star | 1 | 1 | M-65 |
| 798-231 | maru- puḷḷimīn | descendant, clan member Spot-star | 1 | 1 | M-57 |
| 798-240-236 | maru- mīmīn vēykūṭumīn | descendant, clan member High-star (pole star) Bamboo-star cluster | 1 | 1 | M-54 |
| 798-240-705 | maru- mīmīn kaḷam | descendant, clan member High-star (pole star) threshing floor, assembly | 1 | 1 | M-50 |
| 235-760 | vēymīn maka | Bamboo-star (Punarvasu) son/child of | 1 | 1 | M-47 |
| 125-235-233-240-636 | vēṭṭuvaṉ vēymīn varimīn mīmīn pal | Hunter (clan) Bamboo-star (Punarvasu) Striped-star High-star (pole star) many | 1 | 1 | M-41 |
| 220-803 | mīn il | star house | 1 | 1 | M-1706 |
| 440-741-240-220 | koḷ orukuṭi mīmīn mīn | received, bought first ward High-star (pole star) star | 1 | 1 | M-888 |
| 892-741-235-240 | vil orukuṭi vēymīn mīmīn | sale, price first ward Bamboo-star (Punarvasu) High-star (pole star) | 1 | 1 | M-1756 |
| 590-255-435-125 | paṭṭi mutal miṉ vēṭṭuvaṉ | hamlet, fold chief, first flash, bright Hunter (clan) | 1 | 1 | M-1688 |
| 690-435-760 | piṇai miṉ maka | bound, allied flash, bright son/child of | 1 | 1 | M-2113 |
| 595-803-153 | paṭṭi il kā | fold house keeper | 1 | 1 | M-1689 |
| 415-900 | kavar tiṅkaḷ | branch (of a line) month | 1 | 1 | M-2006 |
| 455-220 | ampu mīn | arrow star | 1 | 1 | M-1749 |
| 590-820 | paṭṭi kāl | hamlet, fold quarter-share | 1 | 1 | M-1761 |
| 705-255-435-798-142-400 | kaḷam mutal miṉ maru- kō ciṟ | threshing floor, assembly chief, first flash, bright descendant, clan member king junior | 1 | 1 | M-1772 |
| 368-760 | koṭi maka | banner (of a line) son/child of | 1 | 1 | M-1717 |
| 495-463 | kompu mukkōṭu | branch Three-peaks | 1 | 1 | H-187 |
| 900-585 | tiṅkaḷ kaṉṉi? | month maiden (of the Seven) | 1 | 1 | H-472 |
| 575-861-368 | kōṭṭai kāṇi koṭi | great measure; fort share, holding (a "hand") banner (of a line) | 1 | 1 | H-458 |
| 700-742-590-390 | nāḻi? irukuṭi paṭṭi maṟam | cup measure second ward hamlet, fold warrior | 1 | 1 | H-454 |
| 240-440 | mīmīn koḷ | High-star (pole star) received, bought | 1 | 1 | H-411 |
| 741-390-368 | orukuṭi maṟam koṭi | first ward warrior banner (of a line) | 1 | 1 | H-369 |
| 090-700 | āḷ nāḻi? | manager cup measure | 1 | 1 | H-346 |
| 877-861 | nālkāṇi kāṇi | four shares share, holding (a "hand") | 1 | 1 | H-343 |
| 240-231-520 | mīmīn puḷḷimīn vēḷ | High-star (pole star) Spot-star chief | 1 | 1 | H-899 |
| 904-705 | irutiṅkaḷ kaḷam | two months threshing floor, assembly | 1 | 1 | H-717 |
| 798-240-095 | maru- mīmīn kōlaṉ | descendant, clan member High-star (pole star) staff-bearer | 1 | 1 | H-660 |
| 615-590-892 | vayal paṭṭi vil | field hamlet, fold sale, price | 1 | 1 | H-612 |
| 233-717 | varimīn aṭi | Striped-star servant, devotee | 1 | 1 | H-601 |
| 803-415-220 | il kavar mīn | house branch (of a line) star | 1 | 1 | H-592 |
| 700-741 | nāḻi? orukuṭi | cup measure first ward | 1 | 1 | H-519 |
| 790-590-405 | kaṇ paṭṭi kiḷai | eye hamlet, fold kindred | 1 | 1 | H-479 |
| 415-100-820 | kavar mutu kāl | branch (of a line) elder quarter-share | 1 | 1 | H-814 |
| 233-550 | varimīn vāy | Striped-star gate, mouth | 1 | 1 | H-791 |
| 235-717-741 | vēymīn aṭi orukuṭi | Bamboo-star (Punarvasu) servant, devotee first ward | 1 | 1 | H-328 |
| 390-817 | maṟam kāṇi | warrior share, holding | 1 | 1 | K-78 |
| 803-233-176 | il varimīn iṟai | house Striped-star tax, levy | 1 | 1 | K-62 |
| 630-741 | pal orukuṭi | many first ward | 1 | 1 | K-13 |
| 900-790-415-717 | tiṅkaḷ kaṇ kavar aṭi | month eye branch (of a line) servant, devotee | 1 | 1 | K-11 |
| 590-861-255-435-690 | paṭṭi kāṇi mutal miṉ piṇai | hamlet, fold share, holding (a "hand") chief, first flash, bright bound, allied | 1 | 1 | K-10 |
| 590-540-760 | paṭṭi paṟai maka | hamlet, fold proclamation son/child of | 1 | 1 | L-112 |
| 235-240-904 | vēymīn mīmīn irutiṅkaḷ | Bamboo-star (Punarvasu) High-star (pole star) two months | 1 | 1 | L-111 |
| 140-861 | ammai kāṇi | mother, lady share, holding (a "hand") | 1 | 1 | L-60 |
| 240-220 | mīmīn mīn | High-star (pole star) star | 1 | 1 | H-231 |
| 463 | mukkōṭu | Three-peaks | 1 | 1 | Kd-16 |
| 700-798 | nāḻi? maru- | cup measure descendant, clan member | 1 | 1 | K-90 |
| 480-142 | kuṉṟu kō | hill king | 1 | 1 | M-2063 |
| 550-390 | vāy maṟam | gate, mouth warrior | 1 | 1 | L-145 |
| 705-575 | kaḷam kōṭṭai | threshing floor, assembly great measure; fort | 1 | 1 | L-115 |
| 803-904-590-407 | il irutiṅkaḷ paṭṭi kiḷai | house two months hamlet, fold herd, flock | 1 | 1 | L-114 |
| 240-630-690 | mīmīn pal piṇai | High-star (pole star) many bound, allied | 1 | 1 | H-321 |
| 416-220 | irukavar mīn | two branches star | 1 | 1 | H-302 |
| 920-455-220-706 | tiṅkaḷ? ampu mīn kaḷam | month (head of a date formula) arrow star assembly place | 1 | 1 | H-268 |
| 368-390 | koṭi maṟam | banner (of a line) warrior | 1 | 1 | L-29 |
Forty whole inscriptions with sounds, English, sites and findspots: `READINGS.md`.
