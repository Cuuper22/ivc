# Masters and institutions

Scripts (all in `work_scripts/`, rerun with `python3`): `masters_common.py` (loader, opener splitter), `masters_1.py` to `masters_13.py`. Tables in `work_data/masters/`: `census.csv` (1,443 texts with a name before the jar, every object type), `agents.csv`, `x_summary.csv`, `crest_summary.csv`, `candidate_profiles.csv`, `tablet_heads.csv`, `tags.csv`, `tag_matches.csv`. Reading order = stored order reversed. X = the signs between the opener and the jar 740. Counts are per text face (a two-faced tablet counts each face once), copies of one stone counted as separate objects unless noted. Letters after TAG are the catalogue's own subtype codes; the legend is not in the data, so the meanings below are read from shape, animal and findspot.

## Answer in one paragraph

Agents are many masters with one agent each; the institutions are the masters that were stamped over and over. 50 `X jar man` seals serve 47 different X (two X's have two or three seals). 97 `X jar man` objects of every type serve 63 X, 54 of them once. The big masters show up as piles of identical tablets, tags and copper tablets, not as piles of agent seals: 11 Lothal tags for one dozen-fish master, 29 Mohenjo-daro copper tablets for one three-sign master, 39 Harappa tablets for the seated-person office. The strongest unifying fact: masters of agents are named for fish (name ends in a fish sign on 18 of 50 `jar man` seals against 7 of 602 owner seals, p 1e-16), and a fixed three-sign office prefix `920-060-741` stamps seals, tablets and tags in 7 cities.

## 1. Every X in `X jar <noun>`

Seals only (agent seals, name complete):

| noun after the jar | seals | distinct X | X with 2+ seals | cities | median face mm2 |
|---|---|---|---|---|---|
| man 090 | 50 | 47 | 2 (`061-171-035` 3 seals, `240-415-100` 2) | Mohenjo-daro 35, Harappa 8, Lothal 2, Banawali, Kalibangan, Nausharo, Gola Dhoro, 1 unprovenanced | 738 |
| comb 400 | 11 | 10 | 1 (`176`, 2) | Mohenjo-daro 5, Harappa 4, Kalibangan, Dholavira | 240 |
| table-X 679 | 10 | 10 | 0 | Mohenjo-daro 9, Harappa 1 | 713 |
| barred rectangle 621 | 4 | 4 | 0 | Mohenjo-daro 2, Harappa, Dholavira | 748 |

All object types: man 97 objects / 63 X (54 once, 9 more than once; 6 with 3+), comb 188 / 88 (55 once, 14 with 3+), 679 10 / 10, 621 4 / 4. Full list: `agents.csv`.

Answer to "few X with many agents or many X with one each": many X with one each, on seals. The 50 man-seals split 47 ways; 10 of the 47 masters are also an owner seal somewhere. Where an X has many objects they are copies: the top three `jar man` X's are 11 Lothal tags (`705-500-741-001-055-220`), 8 Harappa tablets (`347-741-176`), 7 Mohenjo-daro tablets (`104-645-590-235-240`) = 26 of 97 objects.

Shared first sign and tag. Agent masters share a signature the owners do not.
- First sign 692 (X in outline), 545 (bowtie with a triangle), 853 (diamond with perpendicular ticks) or 683 (crossed lines with decorated tips) opens the master's name on 11 of 50 `jar man` seals (22%) against 15 of 602 owner seals (2.5%), Fisher p 6e-7. 545 and 853 each begin 3 agent names and 1 owner name.
- Last sign: plain fish 220 ends 11 of 50 agent names against 4 of 602 owner names (p 2e-10); whiskered fish 240 ends 4 against 0, sign 035 4 against 0, sign 101 3 against 0. Any fish sign last: 18 of 50 against 7 of 602 (p 1e-16).
- Reading: an agent's master is named like a fish-house, written `[outsider crest 692/545/853/683] ... [fish]`. The home houses' crests (235, 032, 803, 741 first) are not the masters' crests.

Animal. Agents of one X share the animal where the X is a real office: the three agent seals of `240-415-100` (Mohenjo-daro M-1746, M-199 and Gola Dhoro in Gujarat) all carry the Bull1:S animal; the 39 `176 jar comb` objects carry the code Bult on 11 of the 12 that show an animal, and 11 of the 127 Bult objects in the corpus are this one text. Over all seals that share an exact X, same animal 121 pairs against 127 by chance (no pull). Animals do not mark the master in general; they mark the stone.

Opener: see part 4.

## 2. The same X elsewhere

Tablets as accounts. A tablet whose first face is `X jar [man|comb]` is the who-line of an account. The X belongs to a place: for tablet heads with `jar man` or `jar comb`, the X's trench repeats at 57.5% purity against 36.2% by shuffling (max in 500 shuffles 41.8%). The cup count on the back does not follow X once the trench is held fixed (purity 0.65 against 0.62 by shuffling inside trenches, p 0.21): the count belongs to the issuing trench, the X to the office inside it.

- `176 jar comb` (seated person, jar, comb): 39 objects, 36 tablets, 24 in Harappa F Trench I (the mound F granary and working-platform area) and 38 of 39 at Harappa. Back face `033-700` (cup + 3) on 22 of 37 tablets with a counted cup, cup+4 on 10, cup+2 on 5; the rest of F Trench I is cup+3 on 31 of 67.
- `415-100 jar` account at Harappa F Granery: H-847 carries `000-690-000`, `033-700` (3 cups) and `415-100-740` on its three faces; H-799 (`415-100-820-032` / `033-700`, F Trench IV+V) and H-814 (`415-100-820-400` / `032-700`, F Trench VI) are the same pair-form.
- `347-741-176 jar man` (deer, handled jar, seated person): 8 tablets, 7 in E Trench 11, animal code Mult on all 8. E Trench 11 is the trench of the standard ration batch (3 hands, 4 cups, 3 loads); this is the only named man-office in that trench. `235-240 jar man` (caret fish, whiskered fish): tablets H-2054, H-2055 in E Trench 10W/11 and H-2019, H-2020 in E Trench 11 (back `220-032-590-690`).
- `806-235-590-405 jar comb`: 9 tablets, Harappa 8 plus Mohenjo-daro 1.

Pots and copper. X = 176 alone stands on 3 pots. The copper tablets are the largest piles of one X anywhere: 230 copper tablets exist, 229 at Mohenjo-daro.
- `503-615-752 jar`: 29 identical copper tablets (median 34 x 25 mm), 8 areas (DK 13, HRB 4, DKG(S) 2, HRA 2, VSA, VS, L), animal code Othr on 28 of 29; plus 3 of `503-615 jar`.
- `806-845-061-407-850-900 jar`: 14 copper tablets, 6 areas, animal Anth.
- `706-033-923 jar`: 11 copper tablets (+4 with a stroke 001 after), elephant on all 11, 3 areas (DK 7, VSA 3, DKE 1). Same crest as 705-033 on clay tablets at DKE Trench E (`705-033-590-390-740`, 4 tablets) and as 45 seals.
- `255-435-690`: 34 objects, Mohenjo-daro 24 (seals 20, copper 8, tablets 5, one tag), Harappa 8, Kalibangan, Rakhigarhi.

Tags. Names that stamp tags: see part 3.

Abroad. `590-390` (square with a bar on top, tree) is the one master name on seals found abroad: 73 objects in 9 cities including Kish and Gonur Depe, as X before the jar on Allahdino, Chanhu-daro, Harappa 6, Dholavira, Mohenjo-daro 3 (9 plain, 2 jar comb, 1 jar 621). It is a trading-name that travels; the round seals abroad carry none of the home masters.

Cross-city masters (objects, sites): `590-390` 71 objects, 9 sites; `840-032` 40 objects, 6 sites (Harappa 19, Mohenjo-daro 15, Dholavira 4, Lothal 2, Chanhu-daro, Bakkar Buthi); `415-100` 42 objects, 5 sites; `013-840` 17 objects, 5 sites (Allahdino, Harappa 8, Kalibangan, Lothal, Mohenjo-daro 6); `235-240` 45 objects, 4 sites.

## 3. Tags and sealings

262 TAG rows (213 objects). Kind of seal that made each tag, from the text:

| made by | rows | how it reads |
|---|---|---|
| owner `X jar` | 49 | 23 TAG, 10 TAG:B, 8 TAG:P, 5 TAG:L, 2 TAG:PC, 1 TAG:R |
| agent `X jar man` | 17 | 11 are one text at Lothal; plus 4 Dholavira, 1 Kalibangan, 1 `000-220-740-090` Lothal |
| spearman `X spear` | 12 | Lothal 4, Dholavira 4, Harappa, Banawali, Kalibangan, Tarkhanewala-dera |
| carrier `X porter` | 3 | Mohenjo-daro 2, Kalibangan 1 |
| jar + other (151, 892, 617, 803) | 5 | |
| `X comb` | 1 | |
| name or opener with no ending (mostly broken) | 143 | e.g. `861-002-236`, `817-002`, `820` |
| blank (lost signs only) | 20 | |

Tags are agent-heavy: 17 of 83 tags with a whole ending are `jar man` (20%) against 50 of about 750 seal jar texts (7%). Goods are stamped by owners (59%), then agents (20%), spearmen (14%), carriers (4%). Spear-final rate is 4.6% on tags and 7.3% on seals.

Subtypes (guess from shape, animal and findspot). TAG:B, 10 rows, all Lothal, square, elephant, one text: a bale or bundle sealing. TAG:P, 15 rows, 9 circular, Mohenjo-daro 6, Harappa 4, Lothal 3: a pot-mouth sealing (owners, 8 of 15). TAG:L, 40 rows, Kalibangan 18, Harappa 6, Lothal 6, Mohenjo-daro 4: the cord-and-lump sealing; it carries agents (7), carriers (3) and spearmen (2), the working-staff kinds. TAG:O (6) and TAG:W (6): spearman, agent, mostly bull seals; TAG:C (4, Mohenjo-daro faience, Mult animal): the faience ones; TAG:R (4): carrier and owner.

Repeated tag texts (one seal stamped several times): `705-500-741-001-055-220-740-090` 11 (Lothal), `817-002-048-740` 10 (Lothal, TAG:B), `091-056-002-417-890-892` 8 (Kalibangan, twin-men opener, no jar), `861-002-236` 3 (Lothal), `817-002-032-760-740` 3 (Mohenjo-daro TAG:P). Tags also carry account lines: `003-156` (3 porters) 2 Mohenjo-daro TAG:L tags, the same line as 29 tablets in the E-11 ration batch; `700-032` (cup + 2) on a Dholavira tag against 18 Harappa tablets.

Which names stamp goods:
- `705-500-741-001-055-220 jar man`: read as `[U with a long stroke] [horned triangle] [handled jar] one dozen fish, of [that name]'s man`: the fish dozen (055, 12 strokes) is inside the name slot, the quantity and the commodity written on the sealing. 11 tags, 8 of the 25 tags of the SRG 3GX 10 trench.
- `048 jar` (seven strokes in brackets): 10 elephant bale tags at Lothal, plus the Lothal seal L-84 `817-002-048`, Mohenjo-daro seal M-895 `817-002-048-740` and four Harappa clay tablets `851-741-048-740` / `850-741-048-740` (H-205, H-890, H-1810).
- `415-100 jar` with the `920-060-741` prefix: tag M-427 (TAG:P, DKE Trench E, Mohenjo-daro) `920-060-741-415-100-740` and Rakhigarhi tag `920-060-741-240-415-100-000` (elephant).
- `706 jar` on two Lakhanjo-daro tags `706-740` (bull) and `000-365-706-740` (2).
- Spearmen: `617-002-240-220-233-520`, `705-033-520`, `000-002-070-520` (Lothal), `002-220-520` (Banawali), `033-520` (Dholavira). `705-033-520`'s name matches 24 Mohenjo-daro seals of the 705-033 house.

Lothal: 91 tag rows (72 objects), 25 in SRG 3GX 10, the warehouse trench. Who sealed: owner `X jar` 21 rows, agent `X jar man` 12, spearman 4, porter-ending 2, jar only 2, 4 blank, 45 broken names or openers. Two repeated stones make 21 of the Lothal rows: the dozen-fish agent (11) and the elephant `048` owner (10); only 7 distinct whole-name tag texts exist there. Nothing at Lothal carries `jar comb` or `jar 679`. Lothal's own seals (94) include only 2 `jar man`: L-4 `031-575-002-233-100-740-090`, L-41 `817-002-233-740-090`. The sealing masters are outsiders to Lothal's seal corpus: `705-500-741` and `048` are not among Lothal's seal names; `048` is on Mohenjo-daro and Harappa objects.

## 4. Openers and institutions

Of 753 seals with a jar (opener recorded as none, diamond, wheel, `060-920` cap, twin men):

| role | with opener | none | cap 060-920 | diamond | wheel |
|---|---|---|---|---|---|
| owner `X jar` (602) | 154 (26%) | 448 | 21 | 80 | 52 |
| `jar man` (50) | 14 (28%) | 36 | 1 | 8 | 5 |
| `jar comb` (11) | 1 | 10 | 0 | 1 | 0 |
| other noun after jar (90) | 15 | 75 | 1 | 11 | 3 |

- Owner against agent: no split (28% against 26%, Fisher p 0.74).
- Agents of one X share the opener at chance: seals with identical X, 156 owner pairs, same opener in 88 against 89 by shuffling (max 119); with agents 300 pairs, 185 against 178.
- City: Mohenjo-daro 72% no opener, Harappa 81%, Lothal 77%, Dholavira 80%, Kalibangan 88%; the cap opens 17 of the 21 owner caps' seals at Mohenjo-daro (40 of 64 cap objects). Era: Mohenjo-daro Early / Intermediate / Late, no opener 8 of 12, 86 of 117, 84 of 116; no trend.
- So the opener type does not split owners from agents, cities or eras. The redesigned test: the opener against the first sign of the master. It does split: mutual information 0.198 against 0.062 by shuffling (p 0.002 over 391 seals); last sign, animal, and site do not (p 0.53, 0.28, 0.35). First signs: 741 (handled jar) takes the cap 12 of 18; 692 takes no opener on 19 of 19 and 003 on 14 of 14; 240 takes a count opener on 14 of 25; 032 15 of 39.
- The cap is an office prefix. 64 objects open `920-060`, and 38 of them continue with 741: `920-060-741` is a three-sign fixed opener on 38 objects in 7 cities (Mohenjo-daro 24, Harappa 6, Dholavira 2, Chanhu-daro, Kalibangan, Lothal 2, Rakhigarhi 2): 29 seals, 6 tablets, 3 tags. Reading: `920-060-741` = the office stamp ("state house"), with the personal master after it; on tags (M-427, M-1383, Rakhigarhi) it stands in front of the stamping master. The wheel and diamond are head-count openers (done in the diamond job) and ride on the master's own crest, not on the role.

## 5. The biggest masters and institutions (commit)

Sign shapes: 176 seated person with bent knees; 400 comb (vertical line with tick-lines); 740 jar; 090 man; 415 pitchfork with tines; 100 person with three heads; 240 fish with whisker cheeks; 235 fish with a caret hat; 220 plain fish; 705/706 U with a long stroke in its gap; 033 three full strokes; 923 right parenthesis in outline; 503 tall striped triangle; 615 grid of cells; 752 U with branching top; 920 right parenthesis with a small leaf; 060 stroke with a slanted tail; 741 handled jar; 590 square with a bar on top; 390 tree; 048 seven strokes in brackets; 347 deer; 055 twelve strokes in three rows.

1. The seated-person office, `176` + comb (`176-740-400`). Issued cup accounts: 36 tablets with a counted back at Harappa, 24 in F Trench I (granary and platform), cup+3 on 22 of 37; also 2 seals, the code Bult animal on 11 of its 12 animal-bearing copies. The seated person is on 217 objects, 75 seals, 10 sites. Rule: it is the accounts office of Harappa mound F, where the "junior" (comb) writes the cups.
2. The pitchfork and three-headed house, `415-100` and its `240` branch: 42 objects, 5 cities (Mohenjo-daro 29, Harappa 11, Rakhigarhi, Gola Dhoro, 1 unprovenanced): 26 seals, 15 tablets, 2 tags. Kept agents in three places: `240-415-100 jar man` at Mohenjo-daro (M-199 First Street, M-1746 DKG), Gola Dhoro in Gujarat, plus `415-100 jar man comb` at Harappa F Granery. Issued cups (H-847), stamped pot and bale goods (M-427, Rakhigarhi tag). The chain below.
3. The `705/706` house (U with a stroke): 86 name-slot objects, 7 sites: 45 seals, 11 tablets, 14 copper tablets, 13 tags, 3 pots. Copper tablets `706-033-923` (11, elephant, 3 areas), clay tablets `705-033-590-390` at DKE Trench E (4), the Lothal dozen-fish tags (11) and the spearman tag `705-033-520`, Lakhanjo-daro tags `706-740` (2). Did it all: copper issue, clay accounts, goods tags.
4. The `503-615-752` copper office: 29 identical copper tablets plus 3 `503-615`, 8 areas of Mohenjo-daro, one animal code (Othr 28 of 29). Next in size: `806-845-061-407-850-900` 14 and `706-033-923` 11. These three are the Mohenjo-daro mint of copper tokens: 54 of 230 copper tablets, three X's.
5. The Lothal warehouse stamps, `705-500-741-001-055-220 jar man` (11 tags) and `048 jar` (10 bale tags + seals at Mohenjo-daro and Lothal + 4 Harappa tablets). The only goods-stamping names with a dozen-fish count written on the tag.
6. The fish pair `235-240` (45 objects, 4 cities): `jar man` tablets at Harappa E Trench 10W/11 and E Trench 11 (the ration trench), seal M-865 at Mohenjo-daro DKE Trench E (wheel opener), and the long form `104-645-590-235-240 jar man` on 7 Mohenjo-daro tablets (X-shape + square-with-bar + pair of fish; animal Cros on all 7) and the long seal M-24. Biggest agent house by objects in the fish line.
7. The deer office `347-741-176 jar man`: 8 Harappa tablets, 7 in E Trench 11, animal Mult on all, no other object. It sits in the ration trench next to 235-240.
8. The travelling name `590-390`: 71 objects in 9 cities (Mohenjo-daro 31, Harappa 28, Lothal, Dholavira, Chanhu-daro, Allahdino, Kish, Gonur Depe); 47 seals, 20 tablets, 5 tags, 1 pot. The state or trading house that reached Mesopotamia and the Oxus.
9. The office prefix `920-060-741`: 38 objects, 7 cities, 29 seals, 6 tablets, 3 tags. A fixed stamp, not a person.
10. The twin-men tag office `091-056-002-417-890-892`: 8 identical Kalibangan tags, no jar, twin-men opener: a Kalibangan tag stamp that appears only there.

### Chain for `415-100`: account tablet, agent seal, goods tag

1. Account tablet: H-847, Harappa F Granery, faces `000-690-000`, `033-700` (3 cups), `415-100-740` ("of 415-100"). Same pairs: H-799 (F Trench IV+V, `415-100-820-032` / `033-700`), H-814 (F Trench VI, `415-100-820-400` / `032-700`). Agent-form tablets `415-100-740-090-400` ("415-100's man, junior"): H-188 (F Granery) and H-1978 (E Trench 54, animal Phyt).
2. Agent seals: `817-002-240-415-100-740-090` M-1746 (DKG South 7II) and `861-002-240-415-100-740-090` M-199 (DKG First Street), both Mohenjo-daro, both Bull1:S; the same master with Bull1:S at Gola Dhoro (Gujarat, Trench Eo 11), `033-820-240-415-100-740-090`. Owner seals of the master: M-144 `817-002-240-415-100-740`, M-1418, M-1886, M-363 and 6 others at Mohenjo-daro, H-847's twin H-1991 at Harappa.
3. Goods tag: M-427, TAG:P (pot-mouth sealing), DKE Trench E, `920-060-741-415-100-740` = office stamp + master + jar; and Rakhigarhi tag with elephant `920-060-741-240-415-100-000`.
Reading: Harappa granery books the cups to 415-100 (the who-line `415-100 jar`); his man stamps the pots; the goods tags carry the state-office prefix in front of the master's name.

## Rules added

- Masters of agents are fish-named and use outsider crests 692/545/853/683 (p 6e-7 and 1e-16).
- Tablet-head X is tied to its trench (57.5% against 36.2%); the cup count is tied to the trench, not to X.
- The cap opener is the first sign of a fixed three-sign office prefix `920-060-741` (38 objects, 7 cities).
- Opener goes with the first sign of the name (MI p 0.002), not with role, city or era.
