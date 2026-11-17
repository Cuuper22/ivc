# Heads: the issuing side of the Harappa tablets

Word-free job, 2026-11-17. Sign numbers, pictures, jobs, counts and findspots only; no sign has a word here. Scripts in `work_scripts/` (each carries its predictions in the top docstring, written before its numbers): `heads_common.py` (loader and the fixed rule), `heads_1_find.py`, `heads_2_under.py`, `heads_3_parts.py`, `heads_4_names.py`, `heads_5_trenches.py`, `heads_6_copper.py`. Tables and logs in `work_data/heads/` (`h1_*` to `h6_*`, 108 KB). Each script runs in under a minute. Pair counts follow FRAME.md "How pairs are counted": one row per physical stone, chance drawn only among tablets that can carry the property, identical tablets of one trench counted as one issue.

## Plain words

- **Tablet / face / record**: a small clay plaque; one inscribed side is a face; a tablet with 2 or 3 faces is one record. **Partner faces** of a face = the other faces of the same tablet. Harappa has 1,080 clay tablets (stones, after merging duplicate rows); 747 have 2 or more faces.
- **Amount face**: only counts and measure signs. **Jar face / name**: a face holding the jar 740; the name is the signs before it. **Comb** = 400, **man** = 090. **Cups** = the count beside 700; **big measure** = 705/706 (12 cups each).
- **Heading (fixed rule, set before any number)**: a face on a Harappa tablet that is not an amount face, not lost, holds no jar and no broken sign, and stands beside at least 4 different complete partner faces. "Different" is counted on a partner key: amount faces by their reading (033-700 and 700-033 are one amount) and 706 written as 705 (one sign drawn two ways). Tier A groups by exact string; the family (the string with trailing counts, measures and front words cut off, so 413-575-335-711-033-700 becomes 413-575) is what the tables use.
- **Office line** = a heading whose partners are mostly names. **Side face** = a heading whose partners are mostly amounts and other word faces (the heading is then a name-like face without a jar).
- **Issue** = all identical tablets of one trench counted once. **Trench** = the excavator's cut. **Mound** = the letters before "Trench" (E, ET, F, AB, D). The earlier `chits_2_names.py` read "ETrench 11" as mound ET because the name begins with ET; here ETrench trenches are Mound E and "ETTrench" is mound ET. FGranery is Mound F. **Bin** = early / middle / late period (`work_data/time/`). **Moulded** = TAB:B (pressed from a mould, copies identical); **incised** = TAB:I (cut by hand).
- **Shuffle / P**: the label under test is dealt at random many thousand times inside the stated group; P = share of deals at least as extreme as the real number, in the direction stated.

## What was found

**1. The fixed rule returns 5 heading families on 50 Harappa tablets (47 issues): four office lines on 38 tablets and one side face on 13.** The 50 tablets are 6.7% of the 747 Harappa tablets with 2+ faces; the four office lines alone are 38 (5.1%). The two big headings from `chits.md` are in, with the same figures: `413-575-335-711(-033-700)` (13 tablets in the rule; 21 faces in the corpus begin 413-575, 5 more carry a broken sign in the heading) and `413-892-824` (13 tablets, 12 on complete faces). *Means*: Harappa has a handful of fixed heading lines, and they sit on one tablet in twenty. *Opens*: the ordinary name-plus-cups chit (360 amount+name records) has no heading face at all (finding 7).

| heading family | exact strings | frame-v2 shape | tablets / issues | partners | trenches | mounds | bins | moulded / incised | kind |
|---|---|---|---|---|---|---|---|---|---|
| `413-575-335-711` | 413-575-335-711-033-700; -033; bare | vertical line + trapezoid + M-shape + X-in-U (+ 3 cups) | 13 / 11 | 7 | 11 | F 5, E 5, ET 2, none 1 | middle 9, late 2, undated 2 | 13 / 0 | office line |
| `413-892` | 413-892-824; 413-892 | vertical line + bow and arrow (+ front-word 824) | 13 / 13 | 9 | 7 | E 5, F 3, AB 1, none 4 | early 4, middle 5, undated 4 | 5 / 8 | office line |
| `817-368-690` | 817-368-690; +032-700; +034-700 | front word 817 + slot 368 + after-measure 690 (+ cups) | 8 / 7 | 5 | 6 | F 3, E 2, D 1, none 2 | early 1, middle 4, undated 3 | 4 / 4 | office line |
| `415-578` | 415-578-032-824 | pitchfork + table + tall two + front-word 824 | 4 / 4 | 5 | 4 | F 2, E 2 | middle 4 | 0 / 4 | office line |
| `415-220-520` | 415-220-520 | pitchfork + fish + spear (a name closed by the spear, no jar) | 13 / 13 | 8 | 6 | F 5, E 5, D 1, none 2 | early 2, middle 7, undated 4 | 2 / 11 | side face |

(`h1_headings.csv`, `h1_objects.csv`. One tablet, H-786, carries both `413-892-824` and `415-220-520`, so the families add to 51 rows and 50 tablets.) Every heading stands in 4 or more trenches and in both Mound E and Mound F, and every heading except 413-892 and 817-368-690 is in the middle bin or later; 413-892 alone reaches the early bin (4 tablets, all ETrench 54).

**2. Different headings issue different THINGS, and to partly different people; the crests do not differ.** Partner attributes dealt at random among the 38 office-line tablets (20,000 deals, heading sizes kept): amount kind (none / cups / big measure, read on the partner side) chi-square 41.7 against 9.3 by chance, P 0.0001; partner ending 23.8 against 12.3, P 0.017; crest class (fish / 176 / number / other) 10.3 against 12.3, P 0.62. Dropping the small `415-578` gives the same (amount 20.9 against 6.1, P 0.0001; ending P 0.020; crest P 0.36). *Means*: what a heading goes with is the amount, and that is the sharp difference; the name classes differ less, and the house emblems at the front of names do not separate the headings at all. *Opens*: the headings are lines of issue (a kind of amount), not private rolls of one crest.

| heading | tablets with a name | distinct names | name endings | crests | amounts | third face |
|---|---|---|---|---|---|---|
| `413-575` | 11 of 13 | 6 | jar only 4; name closed by the comb with no jar 4; jar + other sign 3 | 240 x3, 156 x3, 851 x2, 220, 530, 850 (fish 4) | big measure on 8 of 13 tablets (baseline 6.4%); the heading itself carries 3 cups (033-700), 3 cups on 10 of 10 tablets with the full string | 0 |
| `413-892` | 12 of 13 | 10 | comb 5 (`171-032-031-240-636-740-400` x3); name closed by the comb with no jar 3; jar only 3 | 171 x4, 415 x2, one each of 033, 229, 240, 235, 141, 924 | any amount on 1 of 13 (H-787: 3 cups with `176-740-400`); big measure on 0 | 0 |
| `817-368-690` | 8 of 8 | 6 | jar only 6, comb 2 (`679-840-032-740` x3) | 679 x3, 000, 495, 240, 171, 176 | cups written inside the heading on 2 of 8 (4 cups, 2 cups); none elsewhere | 0 |
| `415-578` | 4 of 4 | 3 | jar only 4 (`799-840-760-740` x2, `799-840-714-740`, `692-060-240-636-740`) | 799 x3, 240 | cups on 3 of 4 (3, 4, 4) | 3 of 4 |
| `415-220-520` | 0 | - | partners are 5 amount faces (4 cups x4, 2 cups x1), 7 other word faces (110 x2, 003-645-032-590 x2, 090-700, 575-869, `413-892-824`) and itself once | - | cups on 6 of 13 | 0 |

Baselines at Harappa: of 392 jar names on 2+-face tablets, jar only 52.8%, comb 37.5%, man 2.6%. The man ending appears under no heading. A third face is rare at Harappa (6.0% of 2+-face tablets) and appears under one heading only: `415-578` has it on 3 of 4 tablets, always as amount | heading | name (`034-700 | 415-578-032-824 | 799-840-760-740`), exact binomial P 0.0008. *Means*: `415-578` is the one heading that sits on the full three-part record, the amount first, the office in the middle, the name last. *Opens*: its 4 tablets lie in 4 different trenches (FTrench I, FTrench VI, ETrench 54, ETrench 11), so the full record is issued all over the city; the second catalogue's Harappa tablets are the fresh set to look for more.

**3. The heading is built from a shared start and a varying tail; the tails never meet, and every part lives on Harappa clay tablets.** `413` starts both big headings: the sign after 413 is 575 in 21 of the 56 faces holding 413, 892 in 14, the end of the face in 10. Faces holding both 575 and 892: 0. 413 is a tablet sign (71% of its faces on tablets against 36% of all faces on tablets), and all 21 `413-575` faces and all 14 `413-892` faces are Harappa clay tablets; so are every face with `575-335`, `335-711`, `892-824`, `415-578` and `368-690` (21, 18, 12, 5, 8 faces). Sign 711 (21 faces) and 578 (5 faces) are on tablets only. Sign 892 (bow and arrow) is the only part found beyond tablets: 12 tags and 7 pots in the corpus. *Means*: the shared 413 is the office or form (the same start in two lines that go with different amounts), the tail (575-335-711 against 892-824) is what changes the line and with it the kind of issue. `413-575` goes with the big measure and 3 cups, `413-892` with names only. *Opens*: other 413 faces exist outside Harappa on 2 seals that share a start, `413-125-350-297-002-...` at Bala-kot (Blk-1) and at Nausharo (Ns-60), the only seals with 413 as lead sign.

Where else the parts occur, seals (`h3_signs.csv`, `h3_pieces.csv`, `h3_ties.csv`), against signs of the same total frequency:

| sign | faces | on tablets | on seals | seal crest or front-word count | frequency-matched signs: mean, max | P (matched >= real) |
|---|---|---|---|---|---|---|
| 413 | 56 | 40 | 9 | lead on 2 | 8.7, 38 | 0.80 |
| 575 | 80 | 27 | 47 | lead on 19 | 13.7, 41 | 0.23 |
| 335 | 43 | 29 | 11 | lead on 3 | 7.2, 21 | 0.72 |
| 711 | 21 | 21 | 0 | 0 | 3.4, 11 | 1.0 |
| 892 | 88 | 38 | 28 | lead on 8 | 15.1, 41 | 0.58 |
| 824 | 32 | 22 | 10 | front word on 10 | 4.8, 12 | 0.12 |
| 415 | 176 | 70 | 90 | lead on 29 | 26.5, 131 | 0.37 |
| 578 | 5 | 5 | 0 | 0 | 1.3, 6 | 1.0 |
| 817 | 220 | 45 | 149 | front word on 130 | 42.3, 131 | 0.067 |
| 368 | 116 | 31 | 78 | 0 | 19.4, 66 | 1.0 |
| 690 | 118 | 65 | 39 | lead on 7 | 19.4, 66 | 0.70 |
| 220 | 473 | 121 | 259 | lead on 36 | 20.5, 50 | 0.25 |
| 520 | 317 | 92 | 190 | lead on 5 | 69.3, 131 | 1.0 |
| 032 | 574 | 224 | 202 | lead on 86 | 10.7, 22 | 0.00 |

No heading sign is a seal's front word or crest beyond chance, apart from 032 (the tall two, lead on 86 seals against 10.7: a number that opens many names, not an office sign; the matched set has only 3 signs) and the weak front words 817 (generic opener of 130 seals, P 0.067) and 824 (P 0.12). So there is no tie between a heading sign and a seal-holding house or office-holder. Pair level, the side face's crest pair `415-220` heads 13 seals against 4.9 for matched pairs (P 0.154, not above chance); `415-220-520` itself is on 10 seals (8 at Mohenjo-daro, 1 Lothal) and 17 tablets (Harappa). The names under headings stand on seals no more often than ordinary Harappa tablet names: 4 of 21 against 24.3% (binomial P 0.79). *Means*: the issuing lines are not houses' own marks; they are a vocabulary of the Harappa tablet. The one exception is the pitchfork-fish pair 415-220, found on 91 faces in 6 cities and on 4 Mohenjo-daro copper tablets (finding 6). *Opens*: `415-220-520` is a person-like name (a seal crest plus the spear closer), not an office; 5 of its 13 tablets are in ETrench 11 and 11 of 13 are incised.

**4. A name keeps its heading; two names collect under two headings.** Of 23 distinct names under headings, 21 stand under one heading only. Among pairs of heading issues with the same name there are 10; 8 share the heading, against 2.61 when the heading is dealt at random among the heading issues (P 0.0008). The same test for repeated names all under one heading: 6 of 8 against 1.90 (P 0.0023). The two names under two headings:
- `176-740-400` (the commonest Harappa name, 51 objects in 14 trenches): under `413-892` with 3 cups (H-787, no findspot) and under `817-368-690` with 2 cups (H-1827, ETrench 54, Mound E). Amount differs, and both tablets are not in different mounds (one has no findspot).
- `240-636`: under `413-892` (H-2086, ETrench 54, Mound E, early, no amount) and under `415-578` (H-360, FTrench I, Mound F, middle). Two mounds, no amount to compare.

Names repeated under one heading come from more than one trench in every case, from two mounds in one: `240-705-033-550-525-400` under `413-575` in ETrench 11 (E) and FTrench Ab (F), 3 cups each time; `156-924-705` ETTrench 27 and ETrench 32, 3 cups each; `851-741-048` FTrench 37 and FTrench I; `171-032-031-240-636` under `413-892` in FTrench I, VI and IV+V; `799-840-760` under `415-578` in ETrench 11 and ETrench 54 with 3 and 4 cups; `679-840-032` under `817-368-690` in FTrench VI and one with no findspot. *Means*: a name is attached to one line of issue and draws from it across the city; the amount stays the same under one heading in 3 of 4 repeated names that have a cup count on both tablets, and changes by a cup step under `415-578` (3 and 4) and across the two headings of 176 (3 and 2). *Opens*: the heading plus the name together are the stable unit, and the amount step belongs to the holder.

**5. No trench is a store for one heading; every big trench mixes. Mound F and Mound E differ in comb names and time, not in headings.** The 8 trenches with most tablets (`h5_trenches.csv`):

| trench | mound | tablets | 2-face | heading tablets (which) | distinct names / name faces | comb / man / jar only | cups: tablets, mean | big measure | moulded / incised | bins e/m/l/undated |
|---|---|---|---|---|---|---|---|---|---|---|
| ETrench 11 | E | 155 | 130 | 9 (415-220-520 5, 413-575 2, 415-578 1, 413-892 1) | 34 / 60 | 24 / 12 / 19 | 62, 3.56 | 6 | 51 / 104 | 49/66/0/40 |
| FTrench I | F | 109 | 85 | 4 (one each of the four office lines) | 33 / 68 | 43 / 0 / 24 | 66, 3.02 | 4 | 26 / 83 | 1/98/8/2 |
| F- | F | 99 | 67 | 1 (415-220-520) | 33 / 44 | 18 / 2 / 21 | 35, 2.89 | 3 | 43 / 56 | 1/94/4/0 |
| ETrench 54 | E | 67 | 46 | 7 (413-892 4, 817-368-690 2, 415-578 1) | 28 / 35 | 8 / 0 / 22 | 32, 3.22 | 5 | 46 / 21 | 27/40/0/0 |
| ETrench 10W/11 | E | 61 | 48 | 1 (413-575) | 28 / 35 | 11 / 4 / 18 | 24, 3.33 | 4 | 27 / 34 | 5/47/0/9 |
| FGranery | F | 47 | 18 | 4 (415-220-520 2, 413-575 1, 817-368-690 1) | 20 / 29 | 12 / 3 / 13 | 12, 2.50 | 0 | 36 / 11 | 0/37/10/0 |
| D- | D | 45 | 35 | 2 (817-368-690, 415-220-520) | 26 / 27 | 5 / 0 / 20 | 23, 2.70 | 4 | 21 / 24 | 0/0/0/45 |
| FTrench IV+V | F | 41 | 27 | 4 (415-220-520 2, 413-575, 413-892) | 17 / 19 | 12 / 1 / 5 | 13, 2.92 | 2 | 13 / 28 | 0/32/9/0 |
| all Harappa clay tablets | | 1,080 | 729 | 50 | 234 / 540 | 206 / 29 / 259 | 431, 3.04 | 53 | 582 / 498 | 100/576/60/344 |

No trench holds only one heading. Heading tablets are 1 to 9 per trench; the largest single-trench count of each heading is no more than a random draw of the same number of two-face tablets gives (413-575: 2 in ETTrench 27 against 3.37; 413-892: 4 in ETrench 54 against 2.73, P 0.17; 415-220-520: 5 in ETrench 11 against 3.14, P 0.088; 817-368-690: 2 against 2.05; 415-578: 1 against 1.53), and every heading uses as many trenches as chance gives or more (413-575 uses 10 trenches against 7.6). ETrench 11, the biggest trench, carries all four office lines and the side face. Mound E against Mound F (trenches with 15+ clay tablets: E 4, F 6; trench labels dealt at random, 210 possible labellings so the smallest P is about 0.01):

| measure | Mound F | Mound E | P (labels dealt) |
|---|---|---|---|
| comb share of tablets with a jar name | 0.525 (of 183) | 0.333 (of 135) | 0.064 |
| early-bin share of dated tablets | 0.012 (of 344) | 0.323 (of 251) | 0.019 |
| late-bin share of dated tablets | 0.128 | 0.000 | 0.055 |
| big measure on tablets with an amount | 0.073 | 0.119 | 0.096 |
| amount + name records, share of 2-face tablets | 0.576 | 0.422 | 0.42 |
| moulded share | 0.410 | 0.469 | 0.68 |
| heading tablets per 100 tablets | 4.6 | 5.6 | 0.72 |
| hands/loads/cups gang tablets per 100 tablets | 0 | 6.6 (20 tablets, all ETrench 11) | 0.15 |

*Means*: Mound F (FTrench I, F-, the granary trenches) is the middle-to-late side with the comb chits; Mound E holds the earliest tablets (Period 3B), the gang tablets and the bigger share of big-measure records. The headings are spread alike on both mounds. *Opens*: the comb excess in F is mostly the name 176 in FTrench I (`chits.md`: without it P 0.80); the time difference is the cleanest E/F split and it comes from which levels were dug, so a time-matched E/F comparison is the next test.

**6. Mohenjo-daro's copper tablets and Harappa's headings do the same job in the same shape with none of the same signs.**
- No heading string appears on a copper face (0 of 5 families); 26 of 27 heading pieces (the strings and their 2-sign parts) have no copper face; signs 413, 575, 335, 711, 892, 824, 578 and 817 are on 0 of 230 copper faces. Ordinary Harappa tablet sign pairs seen 4+ times are on copper 13.4% of the time (157 pairs), heading pairs 5.6% (1 of 18).
- The one shared piece is the pitchfork-fish pair `415-220`: `415-220-845-407` on four copper tablets (M-507, M-508, M-1456, M-1457), the crest of the Harappa side face `415-220-520`.
- The picture-replacing signs 777, 780, 781, 782, 753, 749, 841, 341 (and 957) are on no heading string and no partner face of a heading tablet; 8 of the 9 occur only on Mohenjo-daro copper (777 also on one Harappa seal, H-598).
- The shape: on copper one text carries one picture (21 of 21 copy pairs) and one picture covers several texts (8 of 13 pictures); at Harappa a name keeps its heading (8 of 10 same-name pairs against 2.61) and a heading covers 3 to 10 different names. The count unit matches the same way: copper counts are the big measure and the tree (705/706 on 34 of 58 count faces against 6.4% at Harappa), and the one Harappa heading that goes with the big measure is `413-575` (8 of 13 tablets); Harappa clay-tablet objects with a three-big-measure face (705/706-033): 11, of which 5 sit beside `413-575` (the sign strings run in parallel: Harappa `235-705-033`, `240-705-033-550-525-400`; copper `235-705-033-845-407-321-407`, `706-033-923-740`).
*Means*: the Harappa heading face is doing the picture's job (a fixed face that heads a class of line, with the name face naming the line), written in signs where Mohenjo-daro uses a drawing, and the two systems do not share signs except the crest pair 415-220. *Opens*: the 5 broken-sign `413-575` faces and the 11 three-big-measure tablets are the places to look for a sign standing for `413-575` on a Mohenjo-daro clay tablet.

**7. How issuing was organised at Harappa, by these numbers.**
- Four fixed offices (heading lines), none in a copper form: `413-575` (13 tablets), `413-892` (13), `817-368-690` (8), `415-578` (4). Together 38 of 747 two-or-more-face tablets (5.1%). Two start with 413 and differ in the tail. All four stand in 4 to 11 trenches on both Mound E and Mound F, so each issued across the city; none is a trench's own store.
- What each issued: `413-575` the three-big-measure line (names such as `240-705-033-550-525-400`, `156-924-705-740-851`) with 3 cups written in the heading, every tablet moulded (13 of 13 against 8.2 for tablets of the same trenches, P 0.0002), middle and late bins; `413-892` a names-only line (1 of 13 carries an amount), 10 names, comb and jar-only, half incised, the only heading in the early bin; `817-368-690` a jar-name line with cups sometimes written in the heading, half moulded; `415-578` a three-part record (amount | heading | name) always incised, cups 3 or 4, names of crest 799 three times.
- To whom: a name keeps its heading (8 of 10 pairs against 2.61); the crest classes do not separate the headings (P 0.62); the big-measure names go to `413-575`, comb and jar-only names mix under the others; the man ending appears under none.
- Everything else is not under a heading: the ordinary chit (name plus 2 to 4 cups, 360 amount+name records, moulded or incised) carries no office face at 95% of the two-face tablets. The side face `415-220-520` is a person, with 4 cups on 4 of its 5 amount tablets, mostly incised, mostly ETrench 11 and the granary.
- Not yet checked: the second catalogue's Harappa tablets for the four office lines; the 5 broken-sign `413-575` faces and 8 more with lost partners (would raise 413-575 from 13 to 18 or more); the near-miss faces below; whether the other 695 two-face tablets carry the office inside the name (its first or last sign); wear or hand per heading; a time-matched E/F comparison; the single seal pair at Bala-kot and Nausharo sharing `413-125-350-297-002`.

## What went against, and the rescue tried

- **The rule returns 5 families, not the 8 to 14 predicted (P1 of `heads_1`).** Redesign: lower the bar to exactly 3 different partners (`h1_log.txt`): `003-156` (21 tablets, the nameless hands/loads/cups gang tablet), `255-435-156-400` (10 tablets, beside the measure line `590-705/706-868` 8 times), `590-705-868` (5), `137-400`, `091-368`, `125-700`, `144`, `255-435-156`, `681-690`. New idea, followed: `590-705-868` and `255-435-156-400` are a second big-measure pair of faces beside names closed by the comb (`550-525-400`, the same name tail as under `413-575`). They are a candidate sixth heading line, left out because they miss the fixed rule (when 705/706 and cup spellings are merged their partners fall to 3). Earlier, the raw-string rule gave 9 families; merging 033-700 with 700-033 and 705 with 706 removed `255-435-156-400` and `137-400`.
- **Moulded is not the mark of headings (P2).** All heading tablets: 23 moulded of 50 against 27.1 for tablets of the same trenches (P of fewer 0.13). Redesign, per family: `413-575` 13 of 13 moulded (chance 8.2, P 0.0002), `415-220-520` 2 of 13 (chance 5.6, P fewer 0.028), `415-578` 0 of 4 (chance 1.8, P fewer 0.06), `413-892` 5 of 13 (chance 7.5) and `817-368-690` 4 of 8 (chance 4.7) at chance. The format splits by heading, not by the class "heading".
- **Partner diversity (P4).** `413-575` has fewer different partners than a random deal gives (6 for 10 tablets against 9.3, P 0.005): the same big-measure names return. `413-892` is at chance (9 against 10.2, P 0.21), `415-220-520` slightly under (9 against 12.7, P 0.014), `817-368-690` under (4 against 5.8, P 0.031). Repeated jar-name faces are far lower (17 against 36.4 for 2 faces). So `413-892` is the heading that behaves like a free list; `413-575` behaves like a standing list.
- **No tie between a heading sign and a house or office-holder** (finding 3). Sign level: 0 of 14 heading signs beyond chance except the number 032 and the weak openers 817 (P 0.067) and 824 (P 0.12). Pair level: `415-220` P 0.154. Names under headings on seals: 4 of 21 against 24.3%. Redesign (pair level) and new idea (via names) both came out at chance; the tie line is paused on the sign-level evidence, with `415-220` kept as the one live link (it is on Mohenjo-daro copper).
- **Name under several headings is rare, not common** (prediction P2 of `heads_4` expected more than chance): 2 names against 6.1 by chance (P of fewer 0.002). The result is the opposite of a pooled store: a name stays with its line.
- **Mound E against F** shows no heading difference (P 0.72) and the comb, early-bin, late-bin and big-measure differences are at P 0.02 to 0.10 with only 210 possible labellings. Time is mixed in (E is the early side). Redesign (time-matched comparison) not yet run.
- **The `chits.md` figure of 49 heading faces on 49 objects in 17 trenches** was a looser screen (any face beginning 413 or 415-578 or ending 824/876); the fixed rule gives 5 families. The facts that carried over are the two big lines and the absence of a trench-owned mark.
- **A choice made after the first look**: partner "different" counted on the partner key (amounts by reading, 706 as 705), and no prefix-union of families (an early version fused 415-220 with 415-220-520 and 255-435 with 255-435-156-400). Both are written in `heads_common.py`.
- **`415-220-520` is not an office** under the rule's own wording (a name ending in the spear is not a name ending in the jar, so it enters). It is kept in the tables and labelled a side face.

## Files

`work_scripts/heads_common.py`, `heads_1_find.py` ... `heads_6_copper.py`; `work_data/heads/h1_headings.csv`, `h1_objects.csv`, `h2_under.csv`, `h2_names.csv`, `h3_signs.csv`, `h3_pieces.csv`, `h3_ties.csv`, `h4_names.csv`, `h5_trenches.csv`, `h5_EF.csv`, `h6_copper.csv`, and the logs `h1_log.txt` to `h6_log.txt`.
