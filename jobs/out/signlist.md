# The true sign list: how many signs the Indus script has, and what kind of writing its sign list looks like

Word-free job, 2026-11-17. Sign numbers, drawings, jobs, counts only. Scripts in `work_scripts/` (each one's rules are in its top docstring, written before its numbers; changes made after a first run are marked there as redesigns): `signlist_common.py` (loaders, copy events), `signlist_1_evidence.py` (four kinds of same-sign evidence), `signlist_eye_sheets.py` (glyph contact sheets for the eye check), `signlist_2_merge.py` (merge rule, controls, groups), `signlist_3_split.py` (splits; run plain and with `clean`), `signlist_4_marks.py` and `signlist_4b_marks_redesign.py` (base + mark families), `signlist_5_inventory.py` (inventory, growth, table), `signlist_6_yardsticks.py` (other scripts counted from raw open data; run with `python3 -I`). Tables and logs: `work_data/signlist/` (6 MB). The table asked for: `work_data/signlist/true_signs.csv`.

## Plain words

- **Catalogue sign**: one number in the first catalogue (Lipi, Wells numbering). **True sign**: a group of catalogue numbers that this job finds to be one sign drawn in different ways.
- **Use**: one occurrence of a sign. Uses are counted over **copy events**: one physical object (duplicate catalogue rows of one stone merged), and all objects of one site and one findspot with the same full text counted once (a moulded batch is one event). 5,679 faces become 4,476 copy events holding 17,034 uses of 707 catalogue numbers.
- **Swap**: two texts identical except at one place; the two signs at that place swap. **Frame**: the rest of the text around the swap; counted once however many objects carry it.
- **Neighbour similarity**: how alike the signs standing just left and just right of two signs are (each sign's left and right neighbours counted, weighted by how surprising each neighbour is, then compared by cosine: 1 = same neighbours, 0 = none shared).
- **Shape code**: the shape list (`work_data/sign_shapes.csv`) gives each catalogue number a shape code and a written description; numbers that share a code are drawn alike in that list.
- **Second catalogue**: Mahadevan 1977, 417 signs, linked to the first by the crosswalk (`work_data/lipi_mahadevan_crosswalk.csv`). It **lumps** two first-catalogue numbers when both are read as one of its numbers (in at least 25% of each one's uses).
- **Frequency band**: the eligible signs (5+ uses) split into five equal groups by how often they are used. **Deal**: an evidence label handed to another sign of the same band at random; the deal shows how many merges chance alone gives.
- **Job / class**: frame v2's 14 classes (front word, slot after it, crest = name front, name part, numbers, measure, counted thing, closer, title after the jar, place word ...), `work_data/frame/classes_v2.csv`.
- **Hapax**: a sign used once. **Chao1**: an estimate of the full sign list including signs not yet found, from how many signs were seen once and twice (observed + once² / (2 × twice)); it is a floor, not a ceiling.
- **P**: share of chance runs at least as extreme as the real figure. Small P = the real figure is not what chance gives, in the direction stated.

## What was found

**1. The script has about 650 signs in use, not 700: 59 catalogue numbers are second drawings of other signs.** Merge rule (two of the four evidence kinds agree, at least one of them a drawing kind, and no veto): 63 pairs of frequent signs merge against 3.1 when each evidence kind is dealt at random within frequency bands (max 11 in 1,000 deals, P 0.001), and against 15.2 when the deal also keeps each sign's job (max 28, P 0.001). They form 29 groups holding 76 of the 289 frequent signs; 12 rare signs join groups through drawing plus the second catalogue. The 707 numbers in use become **648 true signs** (652 with four shape-list numbers never seen in a text). What it means: about one catalogue number in twelve is a variant, and the scribes' own swaps and neighbours agree with the drawing lists on which ones. What it opens: the counted thing "porter with jars" (156) and the closers "porter" (154, 158) and title 161 are one drawn sign doing three jobs; the trees 390 and 405-407 are one counted thing; the big measure 704/705/706 is one sign (5 swap frames, neighbours, drawing and catalogue all agree).

**2. The sign list has the shape of the proto-Elamite and proto-cuneiform accounting scripts, nearly number for number, and not the shape of a syllabary or of mature cuneiform.** At the same amount of text (10,583 sign uses, the size of the open proto-Elamite non-numeral corpus; texts drawn at random, 200 draws):

| system (counted here from raw open data) | signs | used once | signs covering 50% | signs covering 95% | top 50 signs cover |
|---|---|---|---|---|---|
| **Indus, true signs (this job)** | **548** | **205** | **18.7** | **211** | **74.6%** |
| Proto-Elamite, non-numeral signs (Iran, about 3100-2900 BC) | 508 | 185 | 17.0 | 193 | 73.5% |
| Proto-cuneiform, non-numeral signs (Uruk IV-III) | 600 | 243 | 25.5 | 240 | 67.6% |
| Ur III cuneiform (Sumerian, 21st century BC) | 392 | 65 | 33.8 | 204 | 61.2% |
| Linear B syllabograms (word list, by word types, 7,408 uses) | 71 | 5 | 15 | 48 | 96.7% |

Read plainly: Indus and proto-Elamite have the same profile: a few signs carrying half of all writing (19 and 17 signs), about three quarters carried by the top 50, and a third of the list used once. Mature cuneiform at the same size has a thicker middle (34 signs for half, 61% in the top 50) and five times fewer one-off signs per use than Indus (65 against 205). A syllabary is a different animal: 71 signs, the top 50 cover 97%. What it opens: the Indus script works like the proto-scripts of its time and region: a small closed core of formula signs (fronts, slots, closers, titles, numbers, measures, counted things) plus a large open set of name and emblem signs, most of them rare.

**3. The core is closed and the names are open.** Growth (copy events in random order, 300 orders): the full list does not flatten: 380 signs after a quarter of the texts, 503 after half, 648 at the end, 23 new signs in the last tenth of texts (Heaps exponent 0.365: signs grow as tokens to the power 0.37; Ur III at the same size grows from 319 at a quarter to 429). By job: front words (11 signs), slots (5), crests (10), closers (5), after-measure signs (3), name backs (2), tall numbers (5), the tall two (1), place words (13) and measures (23) add no new sign or under one in the last tenth (closed); name parts are open (500 signs, 184 used once, 19.5 new in the last tenth, Chao1 720); counted things (40 signs, 16 once, 1.7 new), titles after the jar (13, Chao1 31) and short numbers (17, Chao1 25) are open at the edge. Because frame v2 names its small classes as fixed sign sets and files every leftover under "name part", the class split is partly built in, so it was checked with no classes at all: the share of rare true signs (5 uses or fewer) standing in each place of the text, against 4.9% over all uses: right after a front word 2.5% (2,129 uses), after a crest 2.6%, before a counted thing 2.8%, after a closer 2.9%, before a number 3.3%; after a number (the counted-thing place) 4.6%; right before a closer (the end of a name) 5.4%; text start 9.1% (3,664 uses). What it means: the places the grammar fills with fixed words take rare signs at half the general rate; the end of the name and the first sign of a text take them at or far above it. What it opens: the one-off signs are where names, emblems and one-time marks live; that is the place to look for sound values and the place where a sign list will keep growing as new seals are dug.

**4. Marks are real units on the fish, and the marked fish trades with "number + fish".** Families from the shape list: 62 bases, 176 compounds (`mark_families.csv`). Written-out test (a compound in one text, two signs in the same frame in another): 149 of 5,499 one-for-two frames of compounds hold the compound's own base, against 63.5 when each compound gets a base dealt at random (max 221 in 5,000 deals, P 0.003); non-compound signs hold a given base in 1.1% of cases. The fish family carries it: 99 of 830 frames hold the plain fish 220 against 9.1 dealt (P 0.0002). Of the 66 frames where the plain fish is the second sign, the first sign is a number in 42 (three strokes 12, tall two 11, four 6, six-stacked 5, six 4, four tall 4) and the pitchfork 415 in 10. By mark: strokes inside 52 of 1,104 against 12.1 (P 0.0004), roof (caret hat) 33 of 861 against 9.7 (P 0.010), whiskers 19 of 153 against 1.7 (P 0.015). The measure once taken for the marked fish (40 of 528 against 133 of 3,332) is reproduced and now holds for each fish mark separately. What it means: a mark drawn on the fish does the job of a sign written before the fish, mostly a number. What it opens: the fish crests are count-and-fish names written two ways; a reading of a crest as "[n] fish" can be tested on every marked fish.

**5. Splits: one catalogue sign is two lumped signs where the second catalogue already sees two; elsewhere two-profile signs are one sign with two jobs.** First catalogue sign 824 is read by the second catalogue as two numbers (284 and 267, 36% each), and its uses fall into two profiles: one ends the text after a name part, the other opens a text before the after-front slot like the front words 817/861 (which the second catalogue also reads as 267). Sign 001 (one short stroke) is read as two second-catalogue numbers (97 and 98) and also falls into two profiles. Sign 850 (simple leaf or diamond) shows the strongest two-profile behaviour of the 100 commonest signs (gain 0.95 bits per use, against 0.013 for random pooled pairs of the same size): one profile after counted things on copper tablets, one after a text start on seals.

## The merged groups (rule v2), largest first, with pictures in words

Evidence letters: a = swaps, b = neighbours, c = drawing (shape list and eye), d = second catalogue lumps them; "swaps" = swap frames. Uses are first-catalogue copy events.

| true sign | members | uses | picture in words | links |
|---|---|---|---|---|
| 156 | 153 154 155 156 158 159 161 | 198 | a person with a yoke carrying two loads; head drawn as jar handles (153-158) or as a triangle (159, 161) | 154-158 a+b+c+d (2 swaps); 154-156 b+c+d; 153-154, 153-158 b+c+d; 154-155, 153-156, 156-158, 155-158, 153-155 c+d; 154-159 b+c (eye); 159-161 c+d |
| 390 | 390 392 405 406 407 | 523 | a tree on a stem, three-pronged top (390, 392) or branched top (405-407) | 390-405 a+b+c (9 swaps); 405-407 b+c+d; 392-405, 390-406 b+c; 406-407, 405-406, 390-392 c+d |
| 630 | 630 632 634 636 642 | 100 | a tall rectangle with short ticks hanging from the top edge | 636-642 a+b+d (2 swaps); the rest c+d |
| 468 | 467 468 470 472 475 | 31 | an A-shape with a comb at its foot (the load-count sign) | 467-472, 467-468, 468-472 b+c+d; 470 and 475 by drawing and catalogue |
| 422 | 421 422 423 426 | 26 | a long base line with four upright strokes, crossed by short bars (a rake or fence) | 422-423, 422-426, 423-426 b+c+d; 421 by drawing and catalogue |
| 297 | 296 297 301 304 | 23 | prismed lines (shape code P205) | rare members by drawing and catalogue |
| 705 | 704 705 706 | 303 | a U with a long stroke standing in its gap, a dot at its foot (the big measure) | 705-706 a+b+c+d (5 swaps); 704 c+d |
| 803 | 803 806 838 | 279 | a leaf with a small tree inside it | 806-838 b+d (2 swaps); 803-838 b+c (eye) |
| 368 | 365 367 368 | 138 | a stroke with a hatched triangular wing at its middle | 365-368 c+d (1 swap); 367 by drawing and catalogue |
| 527 | 525 526 527 | 86 | a small box with horizontal bars and a line leaving two corners | 526-527 a+b+c+d (3 swaps); 525-526, 525-527 b+d |
| 070 | 070 072 515 | 70 | an upright stroke with two arms (an arrow-like person) | 070-072 b+c+d; 070-515 b+d |
| 269 | 221 267 269 | 24 | a bird pointing up between two large brackets | 221-267 b+d; 267-269 c+d |
| 861 | 817 861 | 472 | a leaf or diamond with a small diamond on top (front word) | a+c+d (10 swaps) |
| 760 | 752 760 | 171 | a U with two branches or flags at the top | b+c (eye; 1 swap) |
| 550 | 550 555 | 145 | the pincers (two triangles point to point) | b+c (1 swap) |
| 435 | 435 436 | 89 | a stroke with a diagonal at each end | b+c+d (1 swap) |
| 017 | 007 017 | 85 | seven short strokes, one row (007) or stacked (017) | b+c (1 swap) |
| 904 | 904 927 | 75 | two nested right brackets | b+c+d |
| 460 | 460 463 | 67 | three tall thin triangles | b+d (1 swap) |
| 850 | 625 850 | 64 | crosswalk glyph is a diamond; the shape list calls 625 a plain tall rectangle | b+d (no drawing support; see what went against) |
| 350 | 350 353 | 56 | a line with prongs out the top and bottom | c+d |
| 016 | 006 016 | 54 | six short strokes, one row (006) or two rows of three (016) | b+c (1 swap) |
| 745 | 745 746 | 45 | the jar with three short strokes in its mouth | c+d |
| 236 | 136 236 | 39 | 236 is the roofed fish in a cage of four strokes; 136 has no description and its glyph is a person | b+d (1 swap; eye calls them different) |
| 337 | 336 337 | 25 | an M with its legs joined by bars | b+c+d (1 swap) |
| 510 | 510 511 | 25 | a square on a stroke | c+d |
| 048 | 048 049 | 24 | seven short strokes inside brackets | b+c |
| 371 | 370 371 | 21 | a stroke broken by a ring with a dot | c+d |
| 772 | 772 773 | 19 | a U whose arms end in a double pitchfork and a tree | b+c+d |
| 101 | 101 103 | 13 | the three-headed person inside brackets | c+d |
| 626, 323, 812, 028, 578 | 626 879; 322 323; 812 814; 025 028; 578 579 | 12, 11, 11, 8, 7 | pairs with rare members, by drawing and catalogue | c+d |

The copper swap pairs: 705/706 merged; 421/422/423 merged. Near misses with one swap frame plus the same shape code, one frame short of (a): 407/408 (tree), 061/063 (reversed lambda), 005/015 (five strokes), 027/028, 352/353, 382/384 (description overlap 0.89). Taken in, the list drops by about six more signs. 904/905, 220/231/233, 176/384 and 806/831 are base and marked sign, or truly different drawings; the merge rule keeps them apart and step 4 treats the marks.

## Base + mark families (`mark_families.csv`, `mark_test.csv`, `mark_redesign.csv`)

| base | compounds (uses) | mark |
|---|---|---|
| fish 220 (459) | 231 (92) stroke inside; 233 (189) line through the body; 235 (234) roof; 240 (316) whiskers; 226 (38) four strokes at the corners; 243 (12) roof and hatching | strokes inside, roof, whiskers |
| marked fish | 232 = 231 + cage (9); 234 = 233 + cage (9); 236 = 235 + cage (26); 241 = 240 + cage (12) | cage of four short strokes |
| jar 740 (1,805) | 741 (213) one stroke in the mouth; 742-744 (60) two; 745-747 (52) three; 748 (3) four | strokes inside |
| U 700 (532) | 701, 703 short strokes inside; 704-707 long stroke (the big measure); 710 tree; 711 X; 752/760 branches | strokes inside, joined object |
| person 090 (171) | 093 stroke between legs; 097 brackets; 100 three heads (133); 104, 110-111, 125, 130, 142 ... person holding or joined to an object | joined object, brackets |
| three-headed person 100 | 101, 103 in brackets | brackets |
| leaf 790 (49) | 798 (147) with pincers; 803/806 (261) with a tree; 812-814, 825 with a hat; 832 (44) with a stroke | joined object, hat |
| seven strokes 007 | 048, 049 in brackets | brackets |
| box 590 (219) | 592 (11) in a cage | cage |
| leaf with tree 803 | 804, 807 in a cage | cage |
| double bracket 904 | 905, 928 with an added bracket | brackets |

Which marks are real units:
- **Strokes inside, roof, whiskers**: yes, by the written-out test (P 0.0004, 0.010, 0.015 against dealt bases). Each marked fish is written out elsewhere as [number or pitchfork] + plain fish.
- **Brackets**: written out no (6 of 423 frames against 5.4 dealt, P 0.36); redesign (a bracketed sign should END like its base and may START differently): right neighbours of the bracketed sign match its base, cosine 0.287 against 0.049 for dealt bases (P 0.0002), left neighbours do not (0.019 against 0.060). The bracket is a unit that changes what comes before, not after.
- **Cage**: written out no (7 of 394 against 4.4, P 0.14); redesign: left neighbours match the base (0.202 against 0.081, P 0.0012), right neighbours do not (0.019 against 0.034). The cage changes what follows. New idea run alongside (a cage as a count already written in): caged fish stand after a number 1 time in 56 uses, their uncaged bases 36 in 831 (4.3%); small, pointing the way the idea says.
- **Joined object** (person or U holding a thing): no on both tests (17 of 1,845 against 21.9; right 0.055 against 0.048, left 0.026 against 0.044). These compounds behave as signs of their own.
- **Jar strokes**: 8 of 249 jar-family frames hold the plain jar against 2.6 dealt (P 0.096); stroke signs written right before the jar are near absent (001-740 1, 002-740 1, 003-740 0, 004-740 1 bigrams), so the stroked jar is not "n strokes + jar" written out.

## The comparison table with sources

Counts as published (links), and the shape figures counted here from raw open data where a published share of uses for the top 50 signs was not found.

| system | signs (published) | source | top 50 cover (counted here, `yardsticks.csv`) |
|---|---|---|---|
| Indus, this job | 648 true signs in use (707 catalogue numbers; 417 in the second catalogue); Chao1 877 | this job | 74.5% (full corpus); 74.6% at 10,583 uses |
| Linear B | about 87 syllabic signs and over 100 ideograms, roughly 200 in all; Unicode encodes 123 ideograms | [Wikipedia: Linear B](https://en.wikipedia.org/wiki/Linear_B) | 96.7% of syllabogram uses in a 1,964-word list ([Linear B Lexicon, archive.org text](https://archive.org/download/LinearBLexicon/Linear-B-Lexicon_djvu.txt)); 71 syllabograms seen |
| Egyptian hieroglyphs | about 900 distinct signs in the Old Kingdom, 750-850 in the Middle Kingdom, around 5,000 in the Ptolemaic period | [Wikipedia: Egyptian hieroglyphs](https://en.wikipedia.org/wiki/Egyptian_hieroglyphs) | not found, not counted |
| Sumerian cuneiform | on the order of 1,000 signs, about 600 by the 24th century BC; Falkenstein 939 signs for late Uruk; Deimel 870 for Early Dynastic II | [Wikipedia: Cuneiform](https://en.wikipedia.org/wiki/Cuneiform) | Ur III: 802 signs over 5.58 million uses, top 50 59.8%; at Indus size (17,034 uses) 429 signs, top 50 60.6% ([CDLI open data](https://github.com/cdli-gh/data), readings mapped to signs with the [Nuolenna sign list](https://github.com/tosaja/Nuolenna)) |
| Proto-cuneiform | sign list 705 elements, 42 numeric | [Wikipedia: Cuneiform](https://en.wikipedia.org/wiki/Cuneiform) | Uruk IV-III non-numeral signs: 875 over 24,525 uses, top 50 67.5% (CDLI) |
| Proto-Elamite | about 1,600 texts; about 1,900 non-numerical signs, about 1,050 used once, about 300 twice, about 1,700 used 9 times or fewer | [Dahl, Proto-Elamite Sign Frequencies, CDLB 2002:1](https://cdli.earth/articles/cdlb/2002-1) | non-numeral signs with variants merged: 508 over 10,583 uses, 185 used once, top 50 73.5% (CDLI) |
| Chinese oracle bones | over 30,000 character forms, around 4,000 characters; 1,500-2,000 deciphered | [Wikipedia: Oracle bone script](https://en.wikipedia.org/wiki/Oracle_bone_script) | not found, not counted |
| Maya | around 1,000 symbols in all; 300 to 500 in use in any one period; 200 syllabic signs | [World History Encyclopedia: Maya Writing](https://www.worldhistory.org/article/655/maya-writing/) | not found, not counted |

Which kind: by size, Indus (648, about 550 at the proto-Elamite corpus size) sits with the logographic and logosyllabic systems (Ur III about 600-800, Egyptian 750-900, Maya 300-500 per period), far above any syllabary (Linear B about 87, plus logograms). By shape, it matches proto-Elamite almost exactly and proto-cuneiform closely, both accounting scripts with numerals, commodity signs and a long tail of one-off signs. How sure the comparison is with texts this short: the size-matched draws take corpus size out (every system drawn to the same 10,583 uses), so the remaining gap to Ur III (205 against 65 one-off signs) is a property of the script, not of how much survived. Text length is the one thing not matched: Indus copy events average 3.9 signs, proto-Elamite texts 6.8 non-numeral signs, Ur III texts 73 signs.

## What went against, and what was done

- **The merge rule as first asked (two of four kinds, any two) chains unrelated signs.** 70 pairs merged against 3.6 under dealt evidence, but the 5 pairs resting only on swaps + neighbours do not beat the same-job deal (5 against 2.17, P 0.074) and they chained the seated person 176, the U 760, 773, 048, 222 and the numerals 007/017 into one group of ten. Swaps and neighbours together measure "same job", not "same sign". Redesign (written into `signlist_2_merge.py` before its numbers): a merge needs a drawing kind (c or d) among its two, and (c) includes the eye check of the glyphs. Result above. The description-based numeral veto missed 003/005 and 004/005 (five strokes are described in rows); amended before any control: two stroke numerals with different shape codes never merge.
- **Two merges rest on the catalogue crosswalk against the drawing**: 625/850 (rectangle against diamond) and 136/236 (person against caged roofed fish), both b+d. 850 is also the strongest two-profile sign of the 100 commonest. Both stay in the table as the rule gave them; they are the first to recheck on photographs.
- **The split test flags 44 of the 100 commonest signs, and random pooled pairs split no more than real signs do** (median gain 0.064 bits for real signs against 0.041 for pooled pairs; pooled pairs beat the one-profile line in 58% of cases). The first run let broken edges form a profile of their own (48 flagged); the clean run drops every use touching a broken edge or lost sign (44 flagged). Most frequent signs have one profile on tablets and pots (counts, text start and end) and another on seals (inside names): one sign, two jobs. Only where the second catalogue also sees two (824, 001) is a lumped pair indicated. New idea for the next run: split by drawing, not by context: photograph the uses of 850, 824 and 001 from both profiles and sort them by eye.
- **Class closure from frame v2 is partly built in** (named small classes, leftovers filed as name parts). The no-class place test above replaces it as the evidence. The machine's own 10-state classes do not help here: they spread rare signs over every class (openers 130 signs, Chao1 195), because the machine places a rare sign by its few neighbours.

## Files

- `work_data/signlist/true_signs.csv`: every catalogue number (711): its true sign, group members, uses, true-sign uses, frame-v2 class, true-sign class, merge evidence, compound family, two-profile flag (100 commonest), shape code and description, second-catalogue readings.
- `pairs.csv` (41,616 pairs, every evidence score), `merge_pairs.csv`, `merge_groups.csv`, `merge_controls.csv`, `merge_rare_formonly.csv`, `swap_frames.csv`, `eye/` (contact sheets and `eye_judgements.csv`), `splits.csv`, `splits_clean.csv`, `mark_families.csv`, `mark_test.csv`, `mark_redesign.csv`, `one_for_two.csv`, `inventory.csv`, `growth.csv`, `growth_by_class.csv`, `slot_openness.csv`, `yardsticks.csv`, `indus_true_tokens.txt`, `log_*.txt`.
- Raw outside data for the yardsticks sits in `/tmp/cdli` and `/tmp/linb` (not in the repository; the script header says where each file comes from).
