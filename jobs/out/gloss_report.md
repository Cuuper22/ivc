# Gloss report: sign-by-sign parse of the Indus corpus

Reading order = stored order reversed. A text is complete when it has no broken edge, no lost sign (000) and no ambiguous sign.
Roles: opener, opener-strokes, count, amount, who, house, house-marker, class, class-tail, title-phrase, cap, cap-selector, plus roles learned from the data (head, second-slot, counted-thing, fixed-ending, phrase, mark). "Fully parsed" = every sign gets a role. "Tight" = fully parsed with at most 2 who-signs and at least half the signs in template roles.

## Key findings

- Parse coverage: 2,085 of 2,162 distinct complete texts (96.4%) get a role for every sign; 1,487 (68.8%) parse tightly (at most 2 who-signs, over half the signs in template roles). Seals 96.8% / 68.5%, tablets 97.2% / 76.0%, copper tablets 100% / 60.3%, pottery 94.8% / 66.9%. Full-parse rate is nearly flat across sites (92.9% to 100%).
- The lexicon learned from other sites lifts held-out tight parsing at Mohenjo-daro from 50.8% (template only) to 61.9%, Harappa 65.4% to 73.1%, Lothal 44.3% to 62.0%, Dholavira 57.7% to 66.7%: the learned slots transfer.
- The template needs one flip. The cap 060-920 and its relatives (920, 692, 550 or 820 before 060) sit at the START of the text in reading order: 115 of 118 texts, with 741/742/745 right after 060. It is a head formula, not a closing cap. Only 22 of the 118 carry a diamond/wheel opener as well, so the cap is an alternative opener.
- Class is a closed set: 26 distinct class signs over 1,055 seal fillings, top 8 cover 84%, entropy 3.0 bits; who-slot has 384 types over 1,719 fillings (22% types/tokens, 175 seen once, 7.4 bits); house 192 types over 791 fillings (6.6 bits). Who and house behave like open-class names.
- Class goes with seal size: Kruskal-Wallis p = 2e-5 (person-class seals largest, median 738 mm2; comb 412, carrier 475 to 559, jar 645). Class does not go with animal (Cramer V 0.098, p 0.18), material (p 0.54) or site (p 0.71).
- Who-sign repeats inside Mohenjo-daro excavation houses: 19 same-house pairs share the last who-sign against 7.8 by shuffling (2.4 times, p = 0.002). The house-slot sign does not: 12 against 12.6 (p 0.60); five rescue variants (adjacent pre-class sign, jar-only seals, rare-sign sets, room level) all sit at 1.0 to 1.3 times chance. Reading under the template: the household element lives in the who slot, the house slot behaves like a recurring citywide name/office series.
- Title phrase [A-variant][806][154/158]: 21 distinct complete texts, A-variant 467 in 6, 468 in 4; 12 end on the carrier, 5 follow a jar-class segment plus a count ([name] [house] [jar] [1] [title]), so the title can be appended to a full seal text.

## 1. Coverage

Rows 5679; distinct complete texts 2162 (2284 counting each object type separately). Fully parsed: 2085 of 2162 (96.4%). Tight: 1487 (68.8%). All rows incl. broken/lost texts: 4270 of 5679 parse (75.2%).

### By object type (distinct complete texts)

| type | texts | fully parsed | % | tight | % |
|---|---|---|---|---|---|
| copper tablet | 68 | 68 | 100.0 | 41 | 60.3 |
| other | 135 | 126 | 93.3 | 82 | 60.7 |
| pottery | 154 | 146 | 94.8 | 103 | 66.9 |
| seal | 1419 | 1373 | 96.8 | 972 | 68.5 |
| tablet | 508 | 494 | 97.2 | 386 | 76.0 |

### By raw type code

| type | texts | fully parsed | % | tight % |
|---|---|---|---|---|
| BNGL | 28 | 23 | 82.1 | 35.7 |
| MISC | 34 | 34 | 100.0 | 58.8 |
| POT:T:g | 120 | 113 | 94.2 | 71.7 |
| POT:T:s | 27 | 26 | 96.3 | 51.9 |
| ROD | 18 | 16 | 88.9 | 77.8 |
| SEAL:C | 15 | 13 | 86.7 | 46.7 |
| SEAL:R | 239 | 231 | 96.7 | 69.0 |
| SEAL:S | 1148 | 1112 | 96.9 | 68.6 |
| TAB:B | 326 | 319 | 97.9 | 76.4 |
| TAB:C | 68 | 68 | 100.0 | 60.3 |
| TAB:I | 182 | 175 | 96.2 | 75.3 |
| TAG | 16 | 16 | 100.0 | 81.2 |

### By site (distinct complete texts)

| site | texts | fully parsed | % | tight % |
|---|---|---|---|---|
| Banawali | 14 | 13 | 92.9 | 64.3 |
| Chanhu-daro | 40 | 38 | 95.0 | 70.0 |
| Dholavira | 75 | 74 | 98.7 | 68.0 |
| Harappa | 756 | 729 | 96.4 | 74.7 |
| Kalibangan | 71 | 69 | 97.2 | 59.2 |
| Lothal | 74 | 70 | 94.6 | 59.5 |
| Mohenjo-daro | 1064 | 1029 | 96.7 | 66.9 |
| Nausharo | 22 | 22 | 100.0 | 68.2 |
| Unknown | 17 | 17 | 100.0 | 58.8 |

### Signs that block a full parse (77 unparsed distinct complete texts)

Block = the sign has no role in an unparsed text (texts of 3+ signs with no anchor sign). Count = unparsed texts it sits in. Shape from sign_shapes.csv.

| sign | texts blocked | shape |
|---|---|---|
| 590 | 9 | Square at bottom with vertical bar coming off top middle |
| 741 | 9 | Classic jar symbol with two horizontal handles at the top of each arm  |
| 892 | 6 | Bow and arrow |
| 140 | 5 | Person with round breasts and one raised arm |
| 440 | 5 | Rectangle, but with bottom line missing, and bottom-half of left line  |
| 550 | 5 | The 'pincer' motif. Right-pointing isocoles triangle on left, left-poi |
| 575 | 5 | Trapezoid with no bottom line, small box resting on the top middle |
| 350 | 4 | Horizontal line with multiple lines out the top, lines or U out the bo |
| 413 | 4 | Vertical line with small horizontal lines crossing it across the entir |
| 706 | 4 | U with a long vertical stroke inserted into the gap of U |
| 382 | 4 | Upside-down heart symbol, with vertical stroke coming from bottom of h |
| 820 | 4 | Wheel with 6 spokes with even angles |
| 125 | 4 | Person with bow and arrow |
| 368 | 4 | Vertical stroke with a triangular wing attached near the middle |
| 411 | 4 | Wheat shaft. Vertical stroke with upward pointing diagonal strokes on  |

Length of unparsed texts: 3 signs: 45, 4 signs: 21, 5 signs: 7, 6 signs: 3, 8 signs: 1.

### Share of all sign tokens by role (distinct complete texts)

who 25.7%, class 16.4%, count 12.1%, house 11.5%, counted-thing 4.9%, opener 4.2%, class-tail 3.6%, house-marker 3.1%, cap 3.0%, opener-strokes 3.0%, phrase 2.8%, unknown 2.6%, mark 2.3%, fixed-ending 1.5%, head 1.0%, amount 1.0%, title-phrase 0.7%, cap-selector 0.4%.

### Held-out check: lexicon learned without the test site

| test set | lexicon from | texts | fully parsed % | tight % |
|---|---|---|---|---|
| Mohenjo-daro | other sites | 1106 | 96.2 | 61.9 |
| Mohenjo-daro | nothing (template only) | 1106 | 93.8 | 50.8 |
| Harappa | other sites | 762 | 95.8 | 73.1 |
| Harappa | nothing (template only) | 762 | 95.0 | 65.4 |
| Dholavira | other sites | 78 | 98.7 | 66.7 |
| Dholavira | nothing (template only) | 78 | 97.4 | 57.7 |
| Lothal | other sites | 79 | 94.9 | 62.0 |
| Lothal | nothing (template only) | 79 | 92.4 | 44.3 |

## 2. Role of the 100 most common signs

Role = most common role of the sign over all rows (all texts, reading order); share = fraction of its occurrences in that role. Shape from the catalogue.

| rank | sign | n | main role | share | second role | shape |
|---|---|---|---|---|---|---|
| 1 | 740 | 1888 | class | 69% | class-tail 31% | Classic jar symbol with two horizontal handles at the t |
| 2 | 002 | 844 | opener-strokes | 50% | count 50% | Two adjacent half-height simple vertical strokes |
| 3 | 700 | 575 | amount | 100% |  | Simple U with no other decoration |
| 4 | 032 | 574 | count | 78% | amount 22% | Two adjacent full-height vertical strokes |
| 5 | 033 | 517 | count | 64% | amount 36% | Three adjacent full-height vertical strokes |
| 6 | 400 | 499 | class | 91% | class-tail 9% | Vertical line with small horizontal lines coming off on |
| 7 | 220 | 473 | counted-thing | 81% | house 19% | Fish with no other decoration |
| 8 | 240 | 349 | who | 49% | house 23% | Fish with extra whiskers on cheeks |
| 9 | 520 | 317 | class | 83% | class-tail 17% | Isocolese triangle on top of vertical line (arrow? spea |
| 10 | 390 | 289 | class | 49% | house 24% | Simple tree with branches at the top |
| 11 | 861 | 272 | opener | 94% | who 4% | Diamond or leaf shape with a small diamond attached to  |
| 12 | 003 | 254 | count | 98% | amount 2% | Three adjacent half-height simple vertical strokes |
| 13 | 031 | 252 | count | 96% | amount 4% | One full-height vertical stroke |
| 14 | 235 | 249 | who | 59% | phrase 25% | Fish with a caret shaped hat |
| 15 | 820 | 242 | opener | 82% | cap 10% | Wheel with 6 spokes with even angles |
| 16 | 590 | 228 | who | 41% | fixed-ending 27% | Square at bottom with vertical bar coming off top middl |
| 17 | 741 | 224 | who | 58% | cap-selector 17% | Classic jar symbol with two horizontal handles at the t |
| 18 | 817 | 220 | opener | 95% | who 4% | Diamond or leaf shape with a small diamond attached to  |
| 19 | 060 | 219 | cap | 100% |  | A single small vertical line, then another vertical lin |
| 20 | 705 | 218 | who | 59% | fixed-ending 13% | U with a long vertical stroke inserted into the gap of  |
| 21 | 176 | 217 | house | 44% | who 26% | Person sitting with bent knees, four small tangent line |
| 22 | 001 | 212 | count | 100% |  | Simple, half-height vertical stroke |
| 23 | 233 | 192 | who | 52% | phrase 21% | Fish with a horizontal line through body |
| 24 | 090 | 188 | class | 69% | class-tail 31% | Person with two arms and two legs,  |
| 25 | 034 | 183 | amount | 71% | count 29% | Four adjacent full-height vertical strokes |
| 26 | 415 | 176 | who | 43% | house 18% | Pitchfork with tines |
| 27 | 920 | 152 | head | 48% | cap 43% | Right parenthesis with small leaf at middle |
| 28 | 798 | 149 | who | 34% | house 33% | Leaf with 'pincers' coming off the right, possibly with |
| 29 | 407 | 142 | class | 55% | who 16% | Simple tree with branches at the top |
| 30 | 255 | 136 | who | 52% | phrase 25% | Unknown asymmetric animal? Perhaps a fish with asymmetr |
| 31 | 806 | 135 | who | 53% | title-phrase 22% | Leaf with tree at bottom |
| 32 | 803 | 134 | counted-thing | 81% | house 19% | Leaf with tree at bottom |
| 33 | 100 | 134 | house-marker | 100% |  | Person with three heads |
| 34 | 760 | 134 | house-marker | 100% |  | U with decorated branching at top |
| 35 | 840 | 130 | who | 32% | fixed-ending 25% | Two vertical leaves, slightly overlapping |
| 36 | 550 | 122 | who | 29% | house 28% | The 'pincer' motif. Right-pointing isocoles triangle on |
| 37 | 405 | 118 | class | 39% | who 35% | Simple tree with branches at the top |
| 38 | 690 | 118 | house | 48% | who 36% | Two nested greater-than symbols, touching two nested le |
| 39 | 368 | 117 | who | 55% | class 35% | Vertical stroke with a triangular wing attached near th |
| 40 | 900 | 112 | counted-thing | 62% | house 38% | Right parenthesis (perhaps with a backward curve at the |
| 41 | 140 | 109 | who | 72% | house 10% | Person with round breasts and one raised arm |
| 42 | 156 | 106 | class | 81% | house 14% | Person carrying two burdens, jar handles for a head |
| 43 | 706 | 101 | who | 54% | fixed-ending 16% | U with a long vertical stroke inserted into the gap of  |
| 44 | 004 | 95 | count | 91% | amount 9% | Four adjacent half-height simple vertical strokes |
| 45 | 231 | 94 | who | 73% | house 19% | Fish with a small vertical stroke in the body |
| 46 | 151 | 93 | class | 86% | who 10% | Person carrying two burdens,  |
| 47 | 061 | 92 | counted-thing | 57% | house 43% | Simple lambda but reversed horizontally, and the leg ma |
| 48 | 892 | 88 | who | 45% | unknown 24% | Bow and arrow |
| 49 | 017 | 82 | house | 41% | who 37% | Seven short vertical strokes |
| 50 | 503 | 82 | counted-thing | 98% | house 2% | Tall isoceles triangle with horizontal stripes |
| 51 | 142 | 81 | house | 54% | who 32% | Person with staff |
| 52 | 575 | 80 | who | 59% | unknown 16% | Trapezoid with no bottom line, small box resting on the |
| 53 | 692 | 75 | cap | 59% | head 40% | An X but drawn in outline |
| 54 | 617 | 75 | class | 61% | who 27% | ? |
| 55 | 435 | 75 | phrase | 45% | fixed-ending 35% | Vertical line with diagonal going down from top right,  |
| 56 | 615 | 73 | house | 60% | who 25% | A grid of x by y cells |
| 57 | 904 | 64 | counted-thing | 59% | house 41% | Two slightly nested right parentheses |
| 58 | 527 | 63 | class | 83% | who 10% | Small box with horizontal hatching, vertical lines comi |
| 59 | 055 | 62 | who | 58% | house 34% | Four small vertical strokes above the same, above the s |
| 60 | 585 | 60 | house-marker | 100% |  | ? |
| 61 | 125 | 58 | who | 79% | unknown 12% | Person with bow and arrow |
| 62 | 388 | 58 | house | 45% | who 41% | Upside-down heart symbol with horizontal hatching, with |
| 63 | 440 | 58 | who | 40% | house 28% | Rectangle, but with bottom line missing, and bottom-hal |
| 64 | 416 | 57 | counted-thing | 82% | house 18% | Pitckfork with two stacked heads |
| 65 | 413 | 56 | who | 39% | unknown 38% | Vertical line with small horizontal lines crossing it a |
| 66 | 850 | 56 | who | 79% | mark 11% | Simple leaf or diamond, possibly rotated 45 degrees |
| 67 | 742 | 56 | who | 46% | mark 20% | Classic jar symbol with two horizontal handles at the t |
| 68 | 845 | 55 | who | 47% | phrase 31% | Two overlapping leaves with diagonal hatches across the |
| 69 | 717 | 54 | who | 59% | house 31% | A cat's paw perhaps, two vertical strokes on each side, |
| 70 | 752 | 53 | house-marker | 100% |  | U with decorated branching at top |
| 71 | 790 | 50 | who | 40% | class 36% | Simple leaf or diamond, possibly rotated 45 degrees |
| 72 | 013 | 49 | who | 67% | mark 14% | Two small vertical strokes over one small vertical stro |
| 73 | 005 | 49 | count | 100% |  | Five simple vertical strokes |
| 74 | 016 | 48 | counted-thing | 60% | house 40% | Six short vertical strokes |
| 75 | 595 | 48 | who | 58% | class 31% | Box with vertical stroke off top center, horizontal str |
| 76 | 350 | 47 | who | 81% | unknown 9% | Horizontal line with multiple lines out the top, lines  |
| 77 | 455 | 46 | who | 67% | mark 13% | Three triangles, one large isocoles pointing right on l |
| 78 | 154 | 45 | class | 49% | title-phrase 38% | Person carrying two burdens, jar handles for a head |
| 79 | 923 | 45 | house-marker | 100% |  | Right parenthesis drawn in outline |
| 80 | 832 | 44 | who | 50% | class 27% | Leaf with small vertical stroke inside |
| 81 | 335 | 43 | who | 49% | house 40% | M with the bottom of the legs connected by a horizontal |
| 82 | 480 | 42 | who | 67% | mark 19% | Tall, slightly narrow caret (mountain motif) |
| 83 | 482 | 41 | house-marker | 100% |  | Tall caret drawn in outline, with diamond inscribed at  |
| 84 | 630 | 40 | house | 45% | who 38% | Rectangle, taller than wide, with vertical strokes for  |
| 85 | 460 | 39 | who | 49% | house 46% | Three tall, thin isoceles triangles |
| 86 | 158 | 39 | house | 33% | title-phrase 33% | Person carrying two burdens, jar handles for a head |
| 87 | 226 | 38 | class | 71% | who 16% | Fish with four small vertical strokes around the four c |
| 88 | 070 | 37 | house | 57% | who 35% | A single vertical line, with two person arms; head may  |
| 89 | 745 | 36 | who | 64% | unknown 14% | Classic jar symbol with two horizontal handles at the t |
| 90 | 035 | 36 | count | 100% |  | Five adjacent simple tall vertical strokes |
| 91 | 384 | 33 | house-marker | 100% |  | Upside-down heart symbol, possibly with vertical stroke |
| 92 | 632 | 32 | counted-thing | 100% |  | Rectangle, taller than wide, with vertical strokes for  |
| 93 | 824 | 32 | head | 100% |  | ? |
| 94 | 501 | 31 | who | 100% |  | ? |
| 95 | 495 | 30 | who | 77% | mark 17% | ? |
| 96 | 095 | 30 | who | 73% | house 20% | Person with short stick |
| 97 | 165 | 30 | who | 47% | class 37% | A left and right paren connected only at the top, with  |
| 98 | 171 | 29 | who | 93% | unknown 3% | Capital 'T' with a small leaf oriented vertically attac |
| 99 | 645 | 28 | counted-thing | 96% | house 4% | An 'X' with no decoration |
| 100 | 463 | 28 | who | 64% | house 21% | ? |

## 3. What the parse says about the world

### 3a. Does the house sign repeat inside excavation houses at Mohenjo-daro?

Mohenjo-daro seals with a complete text and a house sign: 578.

| excavation unit | seals with unit | distinct units | same-unit pairs | pairs sharing the house sign | by shuffling (mean) | ratio | p |
|---|---|---|---|---|---|---|---|
| area-section + block-house | 463 | 198 | 862 | 12 | 12.6 | 0.95 | 0.5968 |
| area-section + block-house + room-grid | 397 | 343 | 72 | 1 | 1.1 | 0.93 | 0.6608 |
| block-house alone | 463 | 171 | 1111 | 12 | 16.4 | 0.73 | 0.8880 |

Control: the same test on the last who-sign instead of the house sign, then on the class sign.

| excavation unit | seals | units | same-unit pairs | pairs sharing | shuffle mean | ratio | p |
|---|---|---|---|---|---|---|---|
| who-sign, area-section + block-house | 284 | 153 | 300 | 19 | 7.8 | 2.44 | 0.0020 |
| class sign, area-section + block-house | 463 | 198 | 862 | 308 | 309.5 | 1.00 | 0.5195 |

Rescue tests for the house slot (the first attempt above is null).

| variant | seals | units | same-unit pairs | pairs sharing | shuffle mean | ratio | p |
|---|---|---|---|---|---|---|---|
| sign directly before the class (markers not skipped) | 463 | 198 | 862 | 18 | 14.1 | 1.27 | 0.1903 |
| jar-closed seals only, house sign | 270 | 146 | 290 | 5 | 4.9 | 1.01 | 0.5415 |
| any shared rare sign (<=100 uses) in who+house+marker slots | 463 | 198 | 862 | 10 | 10.4 | 0.97 | 0.5795 |
| any shared rare sign in who+house+marker, down to room | 397 | 343 | 72 | 1 | 0.8 | 1.29 | 0.5398 |

House sign appears 2+ times in one unit: 13 unit/sign cells. Largest:

| unit | house sign | seals | examples |
|---|---|---|---|
| DKE / Trench E- | 176 | 2 | M-155, M-330 |
| DKE / Trench E- | 240 | 2 | M-1910, M-1738 |
| DKG. (N) / 16II | 460 | 2 | M-723, M-937 |
| DKG. (N) / 18- | 390 | 2 | M-1807, M-933 |
| DKG. (N) / 18- | 920 | 2 | M-914, M-935 |
| DKG. (S) / 1I | 220 | 2 | M-1763, M-1148 |
| DKG. (S) / 1I | 717 | 2 | M-1680, M-651 |
| DKG. (S) / 1I | 920 | 2 | M-380, M-398 |
| DKG. (S) / 7I | 048 | 2 | M-159, M-895 |
| DKG. (S) / 7I | 390 | 2 | M-1911, M-278 |
| DKG. (S) / 7III | 615 | 2 | M-1803, M-269 |
| DKG. (S) / 7V | 455 | 2 | M-1789, M-1096 |

### 3b. Does the class go with seal size, animal and material?

Seals with a class sign: 1188; distinct class signs 26; top 8 cover 84.5%.

| class | seals | median area mm2 | median wide mm | median high mm | share with no animal | top animal |
|---|---|---|---|---|---|---|
| jar 740 | 562 | 645 | 26.7 | 25.0 | 19% | Bull1 (378) |
| spear 520 | 138 | 625 | 26.4 | 24.1 | 13% | Bull1 (90) |
| 390 | 83 | 645 | 26.0 | 25.4 | 10% | Bull1 (58) |
| person 090 | 52 | 738 | 27.9 | 26.9 | 8% | Bull1 (38) |
| comb 400 | 52 | 412 | 21.8 | 19.9 | 23% | Bull1 (29) |
| carrier 151 | 46 | 559 | 24.4 | 23.4 | 4% | Bull1 (38) |
| carrier 156 | 36 | 475 | 22.0 | 21.6 | 6% | Bull1 (28) |
| 527 | 35 | 567 | 26.7 | 22.9 | 26% | Bull1 (21) |
| 405 | 23 | 506 | 27.8 | 20.0 | 48% | Bull1 (12) |
| 617 | 21 | 412 | 24.9 | 17.3 | 43% | Bull1 (11) |

Seal area by class (top 6 classes, 864 seals): Kruskal-Wallis H = 29.4, p = 2e-05. Direction: classes differ in size; order above.
Class x animal (893 seals): Cramer V = 0.098, permutation p = 0.1719.
Class x material (795 seals): Cramer V = 0.083, permutation p = 0.5357.
Class x site (894 seals): Cramer V = 0.081, permutation p = 0.7291.

Class share by animal (top 6 animals; each row sums to 100% over the top 6 classes):

| animal | n | person 090 | carrier 151 | 390 | comb 400 | spear 520 | jar 740 |
|---|---|---|---|---|---|---|---|
| Bull1 | 631 | 6% | 6% | 9% | 5% | 14% | 60% |
| none | 150 | 3% | 1% | 5% | 8% | 12% | 71% |
| Gaur | 44 | 5% | 7% | 11% | 7% | 14% | 57% |
| Zebu | 25 | 12% | 4% | 8% | 0% | 28% | 48% |
| Elep | 16 | 0% | 0% | 6% | 6% | 25% | 62% |
| Rhin | 12 | 8% | 0% | 8% | 0% | 33% | 50% |
| Tigr | 9 | 11% | 0% | 0% | 22% | 0% | 67% |

Class share by material:

| material | n | person 090 | carrier 151 | 390 | comb 400 | spear 520 | jar 740 |
|---|---|---|---|---|---|---|---|
| Steatite | 770 | 5% | 5% | 8% | 6% | 15% | 61% |
| unknown | 135 | 7% | 5% | 10% | 4% | 16% | 59% |
| Faience | 12 | 8% | 8% | 17% | 8% | 8% | 50% |
| Clay | 6 | 17% | 0% | 0% | 17% | 0% | 67% |
| Terracotta | 4 | 0% | 0% | 50% | 0% | 0% | 50% |

### 3c. Do who-slots look like names and class like a closed set?

Seal texts only, distinct complete texts. Tokens = slot fillings; types = distinct signs; singletons = signs seen once in the slot; top-8 = share of tokens held by the 8 commonest signs; entropy in bits.

| slot | tokens | types | types/tokens | singleton types | top-8 share | entropy (bits) |
|---|---|---|---|---|---|---|
| who | 1719 | 384 | 0.223 | 175 | 24% | 7.37 |
| house | 791 | 192 | 0.243 | 91 | 26% | 6.60 |
| class | 1055 | 26 | 0.025 | 4 | 84% | 3.03 |
| count | 805 | 13 | 0.016 | 0 | 98% | 2.92 |
| opener | 313 | 3 | 0.010 | 0 | 100% | 1.58 |

First who-sign: 281 distinct over 874 seals, top-8 25%. Last who-sign (next to the house): 260 distinct, top-8 29%.

## 4. The 40 most completely glossed texts

Chosen from distinct complete texts of 3+ signs, fully parsed, at most 1 who-sign, scored by number of distinct template roles used; each role string used once; title-phrase texts are favoured.

**H-143** (Harappa, SEAL:R) reading order `032-877-740-001-469-806-154`  
[Two adjacent full-height vertical strokes, sign 032] (count) [Diamond with four small diamonds at each vertex, sign 877] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class-tail) [Simple, half-height vertical stroke, sign 001] (count) [A with right leg only partially formed, possib.., sign 469] (title-phrase) [Leaf with tree at bottom, sign 806] (title-phrase) [Person carrying two burdens, jar handles for a.., sign 154] (title-phrase)  
= "count 2 / house 877 / jar class / count 1 / carrier title, grade 469"

**M-371** (Mohenjo-daro, SEAL:R) reading order `467-806-154-032-384-142-617`  
[A with right leg only partially formed, possib.., sign 467] (title-phrase) [Leaf with tree at bottom, sign 806] (title-phrase) [Person carrying two burdens, jar handles for a.., sign 154] (title-phrase) [Two adjacent full-height vertical strokes, sign 032] (count) [Upside-down heart symbol, possibly with vertic.., sign 384] (house-marker) [Person with staff, sign 142] (house) [unlisted sign, sign 617] (class)  
= "carrier title, grade 467 / count 2 / house marker 384 / house 142 / class 617"

**H-158** (Harappa, SEAL:R) reading order `590-405-740-001-472-806-154`  
[Square at bottom with vertical bar coming off .., sign 590] (who) [Simple tree with branches at the top, sign 405] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class-tail) [Simple, half-height vertical stroke, sign 001] (count) [A with right leg only partially formed, possib.., sign 472] (title-phrase) [Leaf with tree at bottom, sign 806] (title-phrase) [Person carrying two burdens, jar handles for a.., sign 154] (title-phrase)  
= "person 590 / house 405 / jar class / count 1 / carrier title, grade 472"

**H-1788** (Harappa, TAB:B) reading order `861-002-470-806-154`  
[Diamond or leaf shape with a small diamond att.., sign 861] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [A with right leg only partially formed, possib.., sign 470] (title-phrase) [Leaf with tree at bottom, sign 806] (title-phrase) [Person carrying two burdens, jar handles for a.., sign 154] (title-phrase)  
= "opening mark / two / carrier title, grade 470"

**H-58** (Harappa, SEAL:S) reading order `235-231-752-740-468-806-158`  
[Fish with a caret shaped hat, sign 235] (who) [Fish with a small vertical stroke in the body, sign 231] (house) [U with decorated branching at top, sign 752] (house-marker) [Classic jar symbol with two horizontal handles.., sign 740] (class-tail) [A with right leg only partially formed, possib.., sign 468] (title-phrase) [Leaf with tree at bottom, sign 806] (title-phrase) [Person carrying two burdens, jar handles for a.., sign 158] (title-phrase)  
= "person 235 / house 231 / house marker 752 / jar class / carrier title, grade 468"

**M-1114** (Mohenjo-daro, SEAL:S) reading order `920-060-741-002-140-740`  
[Right parenthesis with small leaf at middle, sign 920] (cap) [A single small vertical line, then another ver.., sign 060] (cap) [Classic jar symbol with two horizontal handles.., sign 741] (cap-selector) [Two adjacent half-height simple vertical strokes, sign 002] (count) [Person with round breasts and one raised arm, sign 140] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class)  
= "cap 920 / cap 060 / cap selector 741 / count 2 / house 140 / jar class"

**M-1161** (Mohenjo-daro, SEAL:S) reading order `861-002-031-233-520`  
[Diamond or leaf shape with a small diamond att.., sign 861] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [One full-height vertical stroke, sign 031] (count) [Fish with a horizontal line through body, sign 233] (house) [Isocolese triangle on top of vertical line (ar.., sign 520] (class)  
= "opening mark / two / count 1 / house 233 / spear class"

**M-1714** (Mohenjo-daro, SEAL:S) reading order `861-740-031-243-617`  
[Diamond or leaf shape with a small diamond att.., sign 861] (opener) [Classic jar symbol with two horizontal handles.., sign 740] (class-tail) [One full-height vertical stroke, sign 031] (count) [Fish with no arms, caret hat, diagonal hatchin.., sign 243] (house) [unlisted sign, sign 617] (class)  
= "opening mark / jar class / count 1 / house 243 / class 617"

**M-174** (Mohenjo-daro, SEAL:S) reading order `820-002-032-220-923-740`  
[Wheel with 6 spokes with even angles, sign 820] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Two adjacent full-height vertical strokes, sign 032] (count) [Fish with no other decoration, sign 220] (house) [Right parenthesis drawn in outline, sign 923] (house-marker) [Classic jar symbol with two horizontal handles.., sign 740] (class)  
= "opening mark / two / count 2 / house 220 / house marker 923 / jar class"

**K-23** (Kalibangan, SEAL:S) reading order `033-820-002-441-740`  
[Three adjacent full-height vertical strokes, sign 033] (count) [Wheel with 6 spokes with even angles, sign 820] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [unlisted sign, sign 441] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class)  
= "count 3 / opening mark / two / house 441 / jar class"

**H-208** (Harappa, TAB:B) reading order `472-806-158-400`  
[A with right leg only partially formed, possib.., sign 472] (title-phrase) [Leaf with tree at bottom, sign 806] (title-phrase) [Person carrying two burdens, jar handles for a.., sign 158] (title-phrase) [Vertical line with small horizontal lines comi.., sign 400] (class)  
= "carrier title, grade 472 / comb class"

**H-146** (Harappa, SEAL:R) reading order `031-467-806-154`  
[One full-height vertical stroke, sign 031] (count) [A with right leg only partially formed, possib.., sign 467] (title-phrase) [Leaf with tree at bottom, sign 806] (title-phrase) [Person carrying two burdens, jar handles for a.., sign 154] (title-phrase)  
= "count 1 / carrier title, grade 467"

**C-12** (Chanhu-daro, SEAL:S) reading order `920-060-740-031-590-390-161`  
[Right parenthesis with small leaf at middle, sign 920] (cap) [A single small vertical line, then another ver.., sign 060] (cap) [Classic jar symbol with two horizontal handles.., sign 740] (class-tail) [One full-height vertical stroke, sign 031] (count) [Square at bottom with vertical bar coming off .., sign 590] (who) [Simple tree with branches at the top, sign 390] (house) [Person carrying two burdens, triangle or diamo.., sign 161] (class)  
= "cap 920 / cap 060 / jar class / count 1 / person 590 / house 390 / class 161"

**M-1737** (Mohenjo-daro, SEAL:S) reading order `820-002-032-921-072-760-740`  
[Wheel with 6 spokes with even angles, sign 820] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Two adjacent full-height vertical strokes, sign 032] (count) [Left parenthesis with small semicircle against.., sign 921] (who) [A single vertical line, with two person arms; .., sign 072] (house) [U with decorated branching at top, sign 760] (house-marker) [Classic jar symbol with two horizontal handles.., sign 740] (class)  
= "opening mark / two / count 2 / person 921 / house 072 / house marker 760 / jar class"

**M-160** (Mohenjo-daro, SEAL:S) reading order `741-820-002-031-243-151`  
[Classic jar symbol with two horizontal handles.., sign 741] (who) [Wheel with 6 spokes with even angles, sign 820] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [One full-height vertical stroke, sign 031] (count) [Fish with no arms, caret hat, diagonal hatchin.., sign 243] (house) [Person carrying two burdens, , sign 151] (class)  
= "person 741 / opening mark / two / count 1 / house 243 / carrier class"

**M-90** (Mohenjo-daro, SEAL:S) reading order `817-002-031-013-840-740`  
[Diamond or leaf shape with a small diamond att.., sign 817] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [One full-height vertical stroke, sign 031] (count) [Two small vertical strokes over one small vert.., sign 013] (who) [Two vertical leaves, slightly overlapping, sign 840] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class)  
= "opening mark / two / count 1 / person 013 / house 840 / jar class"

**M-101** (Mohenjo-daro, SEAL:S) reading order `817-002-168-740-503-390`  
[Diamond or leaf shape with a small diamond att.., sign 817] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [The 'headphones' motif. Upside down U with sma.., sign 168] (who) [Classic jar symbol with two horizontal handles.., sign 740] (class-tail) [Tall isoceles triangle with horizontal stripes, sign 503] (house) [Simple tree with branches at the top, sign 390] (class)  
= "opening mark / two / person 168 / jar class / house 503 / class 390"

**-** (Bakkar Buthi, POT:T:g) reading order `861-002-840-032-844-405`  
[Diamond or leaf shape with a small diamond att.., sign 861] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Two vertical leaves, slightly overlapping, sign 840] (who) [Two adjacent full-height vertical strokes, sign 032] (count) [unlisted sign, sign 844] (house) [Simple tree with branches at the top, sign 405] (class)  
= "opening mark / two / person 840 / count 2 / house 844 / class 405"

**M-706** (Mohenjo-daro, SEAL:S) reading order `031-861-002-240-773-740`  
[One full-height vertical stroke, sign 031] (count) [Diamond or leaf shape with a small diamond att.., sign 861] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Fish with extra whiskers on cheeks, sign 240] (who) [U where one arm has a double headed pitchfork,.., sign 773] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class)  
= "count 1 / opening mark / two / person 240 / house 773 / jar class"

**M-1974** (Mohenjo-daro, SEAL:R) reading order `820-002-521-400-031-064`  
[Wheel with 6 spokes with even angles, sign 820] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Pitckfork with two vertical tines on ends, one.., sign 521] (house) [Vertical line with small horizontal lines comi.., sign 400] (class-tail) [One full-height vertical stroke, sign 031] (count) [Singly, symetrically bifurcated tall vertical .., sign 064] (who)  
= "opening mark / two / house 521 / comb class / count 1 / person 064"

**M-1957** (Mohenjo-daro, SEAL:R) reading order `820-013-474-806-154`  
[Wheel with 6 spokes with even angles, sign 820] (opener) [Two small vertical strokes over one small vert.., sign 013] (who) [A with right leg only partially formed, possib.., sign 474] (title-phrase) [Leaf with tree at bottom, sign 806] (title-phrase) [Person carrying two burdens, jar handles for a.., sign 154] (title-phrase)  
= "opening mark / person 013 / carrier title, grade 474"

**M-1383** (Mohenjo-daro, TAG:R) reading order `920-060-741-031-017-575-740`  
[Right parenthesis with small leaf at middle, sign 920] (cap) [A single small vertical line, then another ver.., sign 060] (cap) [Classic jar symbol with two horizontal handles.., sign 741] (cap-selector) [One full-height vertical stroke, sign 031] (count) [Seven short vertical strokes, sign 017] (fixed-ending) [Trapezoid with no bottom line, small box resti.., sign 575] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class)  
= "cap 920 / cap 060 / cap selector 741 / count 1 / fixed-ending 017 / house 575 / jar class"

**M-221** (Mohenjo-daro, SEAL:S) reading order `820-002-032-220-335-760-740`  
[Wheel with 6 spokes with even angles, sign 820] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Two adjacent full-height vertical strokes, sign 032] (count) [Fish with no other decoration, sign 220] (counted-thing) [M with the bottom of the legs connected by a h.., sign 335] (house) [U with decorated branching at top, sign 760] (house-marker) [Classic jar symbol with two horizontal handles.., sign 740] (class)  
= "opening mark / two / count 2 / counted-thing 220 / house 335 / house marker 760 / jar class"

**M-384** (Mohenjo-daro, SEAL:R) reading order `820-002-803-003-900-740`  
[Wheel with 6 spokes with even angles, sign 820] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Leaf with tree at bottom, sign 803] (counted-thing) [Three adjacent half-height simple vertical str.., sign 003] (count) [Right parenthesis (perhaps with a backward cur.., sign 900] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class)  
= "opening mark / two / counted-thing 803 / count 3 / house 900 / jar class"

**C-10** (Chanhu-daro, SEAL:S) reading order `817-002-032-220-231-740`  
[Diamond or leaf shape with a small diamond att.., sign 817] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Two adjacent full-height vertical strokes, sign 032] (count) [Fish with no other decoration, sign 220] (counted-thing) [Fish with a small vertical stroke in the body, sign 231] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class)  
= "opening mark / two / count 2 / counted-thing 220 / house 231 / jar class"

**M-1763** (Mohenjo-daro, SEAL:S) reading order `861-002-032-220-740-565-001-416`  
[Diamond or leaf shape with a small diamond att.., sign 861] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Two adjacent full-height vertical strokes, sign 032] (count) [Fish with no other decoration, sign 220] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class-tail) [X with vertical connection on left two tips, r.., sign 565] (who) [Simple, half-height vertical stroke, sign 001] (count) [Pitckfork with two stacked heads, sign 416] (counted-thing)  
= "opening mark / two / count 2 / house 220 / jar class / person 565 / count 1 / counted-thing 416"

**M-21** (Mohenjo-daro, SEAL:S) reading order `861-002-032-692-362-740-001-350`  
[Diamond or leaf shape with a small diamond att.., sign 861] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Two adjacent full-height vertical strokes, sign 032] (count) [An X but drawn in outline, sign 692] (head) [Trapezoid with inner rectangle, sign 362] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class-tail) [Simple, half-height vertical stroke, sign 001] (count) [Horizontal line with multiple lines out the to.., sign 350] (who)  
= "opening mark / two / count 2 / head 692 / house 362 / jar class / count 1 / person 350"

**M-1728** (Mohenjo-daro, SEAL:S) reading order `820-002-032-220-240-055-161`  
[Wheel with 6 spokes with even angles, sign 820] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Two adjacent full-height vertical strokes, sign 032] (count) [Fish with no other decoration, sign 220] (counted-thing) [Fish with extra whiskers on cheeks, sign 240] (who) [Four small vertical strokes above the same, ab.., sign 055] (house) [Person carrying two burdens, triangle or diamo.., sign 161] (class)  
= "opening mark / two / count 2 / counted-thing 220 / person 240 / house 055 / class 161"

**M-1346** (Mohenjo-daro, SEAL:R) reading order `820-002-803-233-032-861-740`  
[Wheel with 6 spokes with even angles, sign 820] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Leaf with tree at bottom, sign 803] (counted-thing) [Fish with a horizontal line through body, sign 233] (who) [Two adjacent full-height vertical strokes, sign 032] (count) [Diamond or leaf shape with a small diamond att.., sign 861] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class)  
= "opening mark / two / counted-thing 803 / person 233 / count 2 / house 861 / jar class"

**H-597** (Harappa, SEAL:S) reading order `861-002-032-070-590-390-740`  
[Diamond or leaf shape with a small diamond att.., sign 861] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Two adjacent full-height vertical strokes, sign 032] (count) [A single vertical line, with two person arms; .., sign 070] (who) [Square at bottom with vertical bar coming off .., sign 590] (fixed-ending) [Simple tree with branches at the top, sign 390] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class)  
= "opening mark / two / count 2 / person 070 / fixed-ending 590 / house 390 / jar class"

**M-1267** (Mohenjo-daro, SEAL:R) reading order `861-002-175-720-740-001-416`  
[Diamond or leaf shape with a small diamond att.., sign 861] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Person sitting with bent knees, no small tange.., sign 175] (who) [unlisted sign, sign 720] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class-tail) [Simple, half-height vertical stroke, sign 001] (count) [Pitckfork with two stacked heads, sign 416] (counted-thing)  
= "opening mark / two / person 175 / house 720 / jar class / count 1 / counted-thing 416"

**M-86** (Mohenjo-daro, SEAL:S) reading order `700-820-002-231-705-033-520`  
[Simple U with no other decoration, sign 700] (amount) [Wheel with 6 spokes with even angles, sign 820] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Fish with a small vertical stroke in the body, sign 231] (who) [U with a long vertical stroke inserted into th.., sign 705] (fixed-ending) [Three adjacent full-height vertical strokes, sign 033] (count) [Isocolese triangle on top of vertical line (ar.., sign 520] (class)  
= "amount / opening mark / two / person 231 / fixed-ending 705 / count 3 / spear class"

**M-381** (Mohenjo-daro, SEAL:R) reading order `820-002-798-032-220-055-740`  
[Wheel with 6 spokes with even angles, sign 820] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Leaf with 'pincers' coming off the right, poss.., sign 798] (who) [Two adjacent full-height vertical strokes, sign 032] (count) [Fish with no other decoration, sign 220] (counted-thing) [Four small vertical strokes above the same, ab.., sign 055] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class)  
= "opening mark / two / person 798 / count 2 / counted-thing 220 / house 055 / jar class"

**M-240** (Mohenjo-daro, SEAL:S) reading order `603-861-002-032-220-240-520`  
[Tall rectangle with two horizontal hatches goi.., sign 603] (who) [Diamond or leaf shape with a small diamond att.., sign 861] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Two adjacent full-height vertical strokes, sign 032] (count) [Fish with no other decoration, sign 220] (counted-thing) [Fish with extra whiskers on cheeks, sign 240] (house) [Isocolese triangle on top of vertical line (ar.., sign 520] (class)  
= "person 603 / opening mark / two / count 2 / counted-thing 220 / house 240 / spear class"

**Rgr-1** (Rakhigarhi, SEAL:S) reading order `920-060-741-335-760-740`  
[Right parenthesis with small leaf at middle, sign 920] (cap) [A single small vertical line, then another ver.., sign 060] (cap) [Classic jar symbol with two horizontal handles.., sign 741] (cap-selector) [M with the bottom of the legs connected by a h.., sign 335] (house) [U with decorated branching at top, sign 760] (house-marker) [Classic jar symbol with two horizontal handles.., sign 740] (class)  
= "cap 920 / cap 060 / cap selector 741 / house 335 / house marker 760 / jar class"

**H-134** (Harappa, SEAL:R) reading order `861-002-003-220-590-405-740`  
[Diamond or leaf shape with a small diamond att.., sign 861] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Three adjacent half-height simple vertical str.., sign 003] (count) [Fish with no other decoration, sign 220] (counted-thing) [Square at bottom with vertical bar coming off .., sign 590] (fixed-ending) [Simple tree with branches at the top, sign 405] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class)  
= "opening mark / two / count 3 / counted-thing 220 / fixed-ending 590 / house 405 / jar class"

**L-217** (Lothal, TAB:B) reading order `920-060-741-821-740`  
[Right parenthesis with small leaf at middle, sign 920] (cap) [A single small vertical line, then another ver.., sign 060] (cap) [Classic jar symbol with two horizontal handles.., sign 741] (cap-selector) [unlisted sign, sign 821] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class)  
= "cap 920 / cap 060 / cap selector 741 / house 821 / jar class"

**M-59** (Mohenjo-daro, SEAL:S) reading order `920-060-742-003-368`  
[Right parenthesis with small leaf at middle, sign 920] (cap) [A single small vertical line, then another ver.., sign 060] (cap) [Classic jar symbol with two horizontal handles.., sign 742] (cap-selector) [Three adjacent half-height simple vertical str.., sign 003] (count) [Vertical stroke with a triangular wing attache.., sign 368] (class)  
= "cap 920 / cap 060 / cap selector 742 / count 3 / class 368"

**H-1198** (Harappa, TAB:I) reading order `820-031-001-061-740`  
[Wheel with 6 spokes with even angles, sign 820] (opener) [One full-height vertical stroke, sign 031] (count) [Simple, half-height vertical stroke, sign 001] (count) [Simple lambda but reversed horizontally, and t.., sign 061] (house) [Classic jar symbol with two horizontal handles.., sign 740] (class)  
= "opening mark / count 1 / count 1 / house 061 / jar class"

**M-1299** (Mohenjo-daro, SEAL:R) reading order `817-002-233-705-033-550-527`  
[Diamond or leaf shape with a small diamond att.., sign 817] (opener) [Two adjacent half-height simple vertical strokes, sign 002] (opener-strokes) [Fish with a horizontal line through body, sign 233] (phrase) [U with a long vertical stroke inserted into th.., sign 705] (phrase) [Three adjacent full-height vertical strokes, sign 033] (count) [The 'pincer' motif. Right-pointing isocoles tr.., sign 550] (house) [Small box with horizontal hatching, vertical l.., sign 527] (class)  
= "opening mark / two / phrase 233 / phrase 705 / count 3 / house 550 / class 527"
