# Stamps: who stamped what, and where it went

Word-free job, 2026-11-17. Signs by number and picture only. Scripts: `work_scripts/stamps_1_build.py` to `stamps_7_clusters.py` (predictions in each docstring, written before the numbers). Tables and logs: `work_data/stamps/` (`objects.csv`, `impressions.csv`, `matches.csv`, `near_matches.csv`, `kinds.csv`, `roles.csv`, `multistamp.csv`, `multistamp_roles.csv`, `clusters.csv`, `city_texts.csv`, `city_links.csv`, `countline_vs_records.csv`, `backs_seen.csv`, `log_2.txt` to `log_7.txt`).

## Plain words

- **Seal**: the carved stamp (stone, sometimes other material). **Impression**: clay pressed with a seal and left on goods. **Sealing**: a lump of clay over a knot, lid, jar mouth or door, carrying one or more impressions. **Stamped pot**: a pot with a seal pressed into its wet clay.
- **Twin**: a seal whose text is the same as an impression's text. **Exact twin**: every sign the same. **Near twin**: one sign different, one sign more or fewer, or the impression's lost signs fit the seal (texts of 4+ signs, 3+ legible).
- **Same room / building / block / area**: the catalogue's findspot levels (building = Mohenjo-daro house or a grid square elsewhere; block = Mohenjo-daro block number or grid letters; area = the excavator's trench or sector).
- **Count line**: a text that is only a number and a counted thing (`003-156` three strokes + porter with jars; `003-390` three strokes + tree), sometimes after a front word. **Front word**: an opening sign like diamond 861/817, wheel 820, bracket-with-leaf 920, followed by a slot sign (002 two strokes, 060). **Agent text**: a name closed by jar 740 then man 090. **Travelling names**: `590-390(-740)` and `255-435-690(-740)`, found across many houses and cities. **Office front**: `920-060-741`.
- **Deal / shuffle**: the labels in question are dealt at random many thousand times; **P** = share of deals at least as extreme as the real count. Small P means the real pattern is not chance, in the direction stated.

## What was found

1. **A stamp text is not one person's stone: the same text sits on different stones in different cities, and the impressions' twin seals lie in another city.** For impressions with 3 or more signs, every exact twin seal (13 of 13 impressions) is in another city. For 2+ signs, the nearest twin is in another city for 18 of 24, in the same block for 2, and never in the same building or room. Only 6 of 24 impressions have any twin in their own city, against 16.2% for a random seal of the same length (no home pull). Where both animals are recorded, exact twin pairs carry different animals 15 times and the same animal 19 times; near twins differ 115 to 46. The ten Lothal box sealings `817-002-048-740` were stamped with an elephant seal; the same four signs are on M-895, a Mohenjo-daro seal with another animal (DK-G South, house 7I, room 13), and the first three on L-84, a small Lothal seal with no animal (I checked all three photos). Means: the text is a formula held by several stamp-holders at once (an office, a standard lot, a house name used by its agents in several towns), and the animal belongs to the stone. Second catalogue, same test (sealings outside Harappa, 3+ signs): 23 of 143 have an exact seal twin, the twin is in the same city for 6 (26%) against 32.5% by chance. It replicates. Opens: a seal text can be followed as a circuit across cities, not as one owner.
2. **Impressions match seals by sequence, not by sign content.** 24 of 131 complete impressions of 2+ signs have an exact twin seal; with the signs shuffled inside each text, 6.1 (max 12 of 200 shuffles). Their twin rate (18.3%) equals the rate at which a seal's text recurs on another seal at the same lengths (19.2%): the stamping stone itself is essentially never among the excavated seals, as expected when perhaps a few percent of stones survive.
3. **Count-line seals are the stamps that get pressed on goods; agents stamp more than they hold.** Share of each seal kind whose exact text turns up on an impression (2+ signs): count line 12 of 49 (24.5%) against 4.3% for length-matched seals of other kinds (P below 1 in 2,000); name seals 1.2% against 2.2%. Among impression faces against seal faces: agent texts (jar + man) 5.4% against 2.5% (Fisher P 0.010), front word alone 5.1% against 3.1% (P 0.064). The count stamp is held locally: `003-156` is on two sealings in Mohenjo-daro DK-G South and on four seals of the same area, one in the same block (M-919).
4. **A sealing is a two-stamp document: a name or agent stamp plus a front-word stamp.** 33 objects carry 2 to 4 impressions. Where two different roles can be read, the combinations are: agent + front word (L-190: agent `705-500-741-001-055-220-740-090` + `317-920-002-...` + `880`; L-191: same agent + `861-002-235`), travelling name + front word (L-196 `...-002-032-590-390` + `861-002`; L-202 `220-590-390-...` + `861-002-236`), travelling name + quantity (L-198 `...-055` + `...-002-032-590-390-740`), three different names on one lump (L-211: crests 231, 220-233, 240; H-2584: `705-033-095-520-468-806` + `798-231-550-527` + `055-255-435-690`). The same stamp pressed 2 to 3 times: M-1385, Rgr-3, M-426. Word-free picture of a transaction: one stamp says who (a named house or its agent, or a travelling house), a second short stamp `861-002` / `820-002` + one sign says under which office or share, and a third may state the amount (`055` the dozen sign). The short front-word stamps are exactly the opener of the name seals, cut as stamps of their own.
5. **The back tells the package, and the package goes with the stamp.** The subtype letter on tags matches what the back photos show (20 backs looked at, `backs_seen.csv`): B = wooden box (corner edge), P = plain smooth back (no package: a token), L = soft package (wrinkled cloth, bundled reeds or cords, crossing cords; the Umma sealing with its published cloth back is L), R = big storage jar (M-1383 sits on the shoulder of a jar), O = flat or cane. Count lines sit on L: 5 of 40 L faces against 2 of 296 other impressions (Fisher P 0.00033); agent texts on L 7 of 40 against 10 of 296 (P 0.0016). Plain tokens (P) carry names and offices, never a count: `920-060-741-415-100-740`, `820-002-590-390-740`, `817-002-032-760-740` three times, and the box sign 590 on 4 of 15. Boxes carry one formula (`817-002-048-740`, ten times); the big jar carries the office front (`920-060-741-031-017-575-740`). Means: quantity stamps go on bales and sacks, office and name tokens go loose, a box gets its house formula.
6. **Seals and records that state the same count of the same thing lie in the same area.** Object pairs (count-line seal, tablet or tag) in one area with the same [number][thing]: 89 against 69.5 when the records' count labels are dealt within the city (P 0.003). 75 of the 89 are Harappa FTrench I, where seals H-352 and H-354 read `033-700` (three tall strokes + cup) beside 29 tablets reading `033-700`, and H-982 `034-700` beside 17 tablets `034-700`; the rest are DK-G South (`003-156`, 5 seals and 2 sealings) and Harappa AB. A cup-count stamp also sits on a pot at Mohenjo-daro DK (M-1374 `...033-700...`). Means: in the cup-tablet trench there were seals that stamp exactly the amount written on the tablets: the stamp and the chit belong to one issue.
7. **The impression places are a few senders stamping many packages.** Distinct texts against draws of the same number of complete impressions from other places: Lothal warehouse square SRG 3GX 10, 7 texts on 15 faces against 12.96 (P below 1 in 5,000); Kalibangan KLB-1, 2 against 7.35; Harappa FTrench 43 (stamped pots), 8 against 18.2; all far fewer than chance. At Lothal one agent stamp (`705-500-741-001-055-220-740-090`, a dozen sign 055 + fish 220 house, its man) is on 8 faces there and 11 objects at Lothal in all; its stone is not among Lothal's seals, and the two Lothal warehouse texts with seal twins have them only at Mohenjo-daro. Lothal's warehouse is a receiver of repeated consignments from a few outside senders; Kalibangan KLB-1 (`091-056-002-417-890-892` seven times) and Harappa FTrench 43 (one-sign hook 440 seven times on pots) are single issuers marking their own output.

## Tables

### 1. Impressions taken (`impressions.csv`, 336 faces on 287 objects)

| tier | catalogue type | faces | why |
|---|---|---|---|
| sealing | TAG (plain) | 172 | the catalogue's sealing / tag class |
| sealing | TAG:L / P / B / O / W / C / PC / R | 40 / 15 / 10 / 6 / 6 / 4 / 5 / 4 | same, with a back-type letter |
| stamped pot | POT:T:s, POT:T:S | 73, 1 | photos M-424, M-1376, H-692, M-422 show a framed seal impression on the pot |
| left out | POT:T:p | 19 | photos Sktd-4, H-1007 show painted or incised marks, not a stamp |
| kept apart | TAB:B moulded tablets | 1,108 | the impression of a mould, not certainly a seal; not in the headline numbers |

Photos checked by looking (23 objects): M-424, M-422, M-1376, H-692 (stamped pots: framed impression, yes); Sktd-4, H-1007 (painted or incised: excluded); K-73 (framed impression in a terracotta cake), L-211 (three overlapping impressions), K-89 (four impressions), L-206 (two impressions over a package), L-146 (impression + ridged back), L-161 (elephant seal impression, second impression arc above), M-1440, M-1383 (on a storage jar), and backs L-124, M-429, M-1427, M-427, L-168, M-426, L-220, Rgr-3, M-1391, H-830; plus backs K-69, K-80, L-162, L-190, M-1388, K-85, M-437, L-143 for the back table. Seals checked: L-84, M-895.

Findspot coverage of impressions: area 164, building 61, depth 87, date bin 100 (early 9, middle 79, late 12), animal 126.

Impression faces by site and type: Lothal 91 (TAG 70, B 10, L 6, P 3, O 1, W 1), Dholavira 76, Harappa 70 (stamped pots 51), Kalibangan 28, Mohenjo-daro 45 (stamped pots 22, P 6, O 5, C 4, L 4, W 3, R 1), Lakhanjo-daro 5, Rupar 3, abroad: Tell Umma 1, Salut 1, Tepe Yahya 1 (stamped pot).

### 2. Where the twin seal lies (exact twins, one row per impression, nearest twin)

| place of nearest twin | 2+ signs | 3+ signs |
|---|---|---|
| same room | 0 | 0 |
| same building | 0 | 0 |
| same block | 2 | 0 |
| same area | 0 | 0 |
| same city, other area | 2 | 0 |
| same city, findspot unknown | 2 | 0 |
| other city | 18 | 13 |

Findspot deal (seal findspots dealt within each city, 2,000 deals): same block 2 against 0.15 (P 0.06), same building 0 against 0.01, same area 2 against 2.28. Exact twins, listed:

| impression text | impressions (city) | twin seals | animals agree (y) / differ (n) |
|---|---|---|---|
| `003-156` | M-429, M-1388 (Mohenjo-daro DK-G S) | M-919 same block; M-838, M-1232, M-1779 same area; H-81, H-499, L-42 other city | y y y y / n n |
| `003-390` | M-2010 (Mohenjo-daro) | M-179, M-1857; H-585, H-596, K-65 | y y / n n |
| `861-002-003-390` | K-82 (Kalibangan) | M-712, M-1697 (Mohenjo-daro) | y y |
| `817-002-048-740` | L-161 to L-170 (Lothal) | M-895 (Mohenjo-daro) | n x10 |
| `705-033-520` | L-146 (Lothal) | M-122, M-1359 (Mohenjo-daro) | y |
| `017-585-740` | Rupar sealing | M-1777 (Mohenjo-daro) | y |
| `861-002` | L-133, L-196 (Lothal) | M-175 | y |
| `817-002` | Dholavira | B-5, B-7, B-15, K-27, M-825 | |
| `690-740` | H-1728 | K-61, M-176 | |
| `792-740` | M-424, M-1382 (stamped pots) | M-953 (same city) | |
| `016-220`, `032-220` | H-1086, H-1084 (stamped pots) | H-1028; Farmana | |

Near twins (4+ signs): 37 impressions; nearest twin in another city 18, same city findspot unknown 15, same city other area 3, same area 1 (M-437 `820-002-590-390-740` with M-1960). Own-city share 19 of 37 against 31.8% by chance, and 10 of the 19 are the Lothal box sealings with L-84; without them 9 of 27.

### 3. Seal kinds and impressions (`kinds.csv`, exact text, 2+ signs)

| seal kind | seals | text on an impression | share | length-matched other seals | P |
|---|---|---|---|---|---|
| count line | 49 | 12 | 24.5% | 4.3% | <0.0005 |
| name | 569 | 7 | 1.2% | 2.2% | 0.97 |
| other | 738 | 8 | 1.1% | 1.4% | 0.69 |
| damaged | 137 | 2 | 1.5% | 3.7% | 0.89 |
| agent (jar + man) | 49 | 0 | 0 | 0.1% | |
| office front 920-060-741 | 25 | 0 | 0 | 0.1% | |
| travelling 590-390 / 255-435-690 | 40 / 16 | 0 / 0 | 0 | 0.2% / 0.1% | |

Long texts almost never have an exact twin, so the role share on the impressions themselves (`roles.csv`, readable faces) is the fairer measure: agent 5.4% of impressions against 2.5% of seals (P 0.010); front word alone 5.1% against 3.1% (P 0.064); office front 1.0% against 1.2%; travelling names 1.9% against 3.0% (P 0.37); quantity 1.3% against 3.1%; closed names 29.8% against 50.0%, with broken texts 55.6% against 37.1% (impressions are worn, so the name share is pulled down by damage).

### 4. Clusters (`clusters.csv`, areas with 4+ impression faces)

| place | faces / objects | complete | different texts (chance) | most copies | crests | read |
|---|---|---|---|---|---|---|
| Lothal SRG 3GX 10 | 25 / 18 | 15 | 7 (12.96) | 8, agent `705-500-741-001-055-220-740-090` | 3 | receiver of repeated consignments; issuers' stones not at Lothal |
| Harappa FTrench 43 | 22 / 22 | 22 | 8 (18.2) | 7, hook `440` | 1 | single issuer stamping its own pots |
| Kalibangan KLB-1 | 16 / 12 | 8 | 2 (7.35) | 7, `091-056-002-417-890-892` | 1 | single issuer |
| Mohenjo-daro DK-G South | 10 / 9 | 5 | 4 (4.71) | 2, `003-156` | 1 | the count stamp at home: 12 twin seals, 4 in the same area |
| Mohenjo-daro DK | 9 / 9 | 4 | 4 (3.83) | 1 | 3 | mixed |

Lothal impressions name 5 crests (048, 220, 482, 617, 705; a sixth key is a lost sign); 3 of them (048, 220, 705) are on Lothal seals, all 5 on seals somewhere; Lothal seals carry 51 crests.

### 5. Between cities (`city_texts.csv`, `city_links.csv`): 4+ sign texts on a seal in one city and a seal or impression in another

| text | cities |
|---|---|
| `817-002-048-740` | Lothal (10 box sealings) / Mohenjo-daro M-895 |
| `861-002-003-390` | Kalibangan sealing K-82 / Mohenjo-daro M-712, M-1697 |
| `817-002-003-390` | Chanhu-daro C-66 / Harappa H-407 / Mohenjo-daro M-32 |
| `820-002-003-390` | Harappa H-1680 / Mohenjo-daro M-1729, M-1806 / Nausharo Ns-7 |
| `817-002-004-390` | Dholavira / Mohenjo-daro M-984, M-1844 |
| `817-002-803-233-520` | Chanhu-daro C-67 / Harappa H-501 |
| `003-140-100-740` | Harappa H-62, H-1032 / Mohenjo-daro M-1108 |
| `061-142-400-740` | Harappa H-451, H-1679 / Mohenjo-daro M-879 |
| `061-171-035-740-090` | Harappa H-565 / Mohenjo-daro M-265 |

City-pair links against 5,000 deals of city labels over the 1,093 complete 4+ sign faces (sizes kept): Harappa-Mohenjo-daro 5 (expected 5.59); Chanhu-daro-Harappa 2 (0.26, P 0.026, 7.6 times); Lothal-Mohenjo-daro 1 (1.95); Dholavira-Mohenjo-daro 1 (1.44); Kalibangan-Mohenjo-daro 1 (1.04); Chanhu-daro-Mohenjo-daro 1 (0.76); Nausharo-Mohenjo-daro 1 (0.38); Harappa-Nausharo 1 (0.13); Harappa-Lothal 0 (0.67). All cross-city links 13 against 16.7 (P 0.58). Five of the nine shared texts are count lines with a front word (`8xx-002-00n-390`, `861-002-003-390`) or the box formula: what crosses cities whole is the quantity formula and the house-formula stamp, not personal names.

### 6. Backs (`backs_seen.csv`, `log_6.txt`)

| subtype | what the back photos show | stamps on it |
|---|---|---|
| B | box corner and lid edge (L-162, L-168) | `817-002-048-740` x10 |
| P | smooth flat back, no package (H-830, L-220, M-427, M-437) | names and offices only: `920-060-741-415-100-740`, `820-002-590-390-740`, `817-002-032-760-740` x3, `803-233-032-904-740`, 590 on 4 of 15 |
| L | cloth or sack wrinkles (K-80), bundled reeds or cords (K-85), crossing cords (M-1388, M-429), lump (L-124); the Umma sealing | count lines 5 of 40, agents 7 of 40 |
| R | shoulder of a big storage jar (M-1383) | `920-060-741-031-017-575-740` office front |
| W | flat (M-426); broad channel over a rod or peg (Rgr-3) | `820-032-130` x2 |
| O | flat (M-1391), ridged cane (L-146), bobbin lump (M-1427) | `705-033-520` measure line, `003-390` |
| plain TAG | long cord or stick groove (L-190), striated folds (L-143) | agents 9, names 45 |

### 7. Count-line seals against tablets and tags (`countline_vs_records.csv`)

| level | count-line seals | same [number][thing] on a record there | chance (seal findspots dealt in city) | P |
|---|---|---|---|---|
| building | 35 | 1 | 0.74 | 0.56 |
| area | 42 | 10 | 8.06 | 0.20 |
| redesign: object pairs, record labels dealt in city | | 89 | 69.5 | 0.003 |
| new idea: on a sealing or tag of the same area | 42 | 5 | 3.10 | 0.16 |

## What went against

- **P1 (stone at home, goods move within the city)**: the twins are in other cities (18 of 24; 13 of 13 at 3+ signs), not in the same city. Redesign: near twins (37 impressions): own city 19 of 37 against 31.8%, but 10 of those are one case (Lothal box sealings with L-84); without it 9 of 27, at chance. New idea, run: the second catalogue gives the same answer (6 of 23 same city against 32.5%). Reading kept: the twin is a fellow holder of the formula, not the stamping stone; the stone that made an impression is not in the excavated set. Next: match on carving detail (sign shapes and spacing in the photos) to find the one stone that made a given impression.
- **P2 for the office front and the travelling names**: no excess among impressions (office front 1.0% against 1.2%; travelling names 1.9% against 3.0%, P 0.37). Redesign (role share on impressions rather than exact twins) is the table above; it moved agents and front words, not these two.
- **P3 (more than half of multi-stamp sealings pair two kinds)**: 15 of 32 readable multi-stamp objects carry two or more roles, just under half; 8 more carry closed names only (some of those are the same stamp repeated).
- **P4 (Lothal and Kalibangan as receivers from many houses)**: both hold far fewer different texts than chance (7 against 12.96; 2 against 7.35). Redesign run (distinct-text draws) gave this; new idea run (crests on Lothal impressions against Lothal seals): 3 of 5 crests are on Lothal seals, the issuing texts with twins are at Mohenjo-daro. Lothal reads as a receiver of a few repeated senders, Kalibangan as one issuer.
- **P5 (outer towns over-linked to Mohenjo-daro)**: Lothal-Mohenjo-daro 1 against 1.95, Kalibangan 1 against 1.04; only Chanhu-daro-Harappa stands out (2 against 0.26). Total cross-city links at chance (13 against 16.7). The sample of 4+ sign shared texts is 9; the redesign is the second catalogue's sealings (table 2 replication) and the next new idea is near twins between cities.
- **P7 (count-line seals match records in the same room or area)**: building 1 against 0.74, area 10 against 8.06 (P 0.20). The redesign (object pairs, record labels dealt) came true (89 against 69.5, P 0.003), carried by Harappa FTrench I cup seals; the new idea (sealings and tags only) 5 against 3.10, P 0.16.
- Near-match rules without a length floor gave 1,158 pairs, mostly short texts with lost signs; only the 4+ sign near twins are used above.

## What it opens

- The transaction picture for reading: [who: name or agent stamp] + [office or share: `861-002` / `820-002` + one sign] + [how much: count stamp or 055], pressed on a bale, box or jar, matched at the store by tablets with the same count (FTrench I). Test next: do the one-sign tails of the short front-word stamps (`861-002-235`, `861-002-236`, `820-002-220-234`) match the crest of the name stamp beside them on the same lump.
- Formula texts held in several cities with different animals: list every text on 3+ stones and test whether the animal follows the city (local holder) or the text.
- The stamp-to-stone search on photographs (carving detail) for the Lothal dozen-agent stamp and the elephant box stamp.
