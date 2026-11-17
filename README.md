# IVC: looking for checkable structure in the Indus script

By Cúper (Yousef) Anas · [Website](https://cuuper22.github.io/ivc/) · [Cite this](CITATION.cff)

## Where the project stands (2026-11-17)

The Indus script is the set of short inscriptions (about 2600-1900 BCE) on stamp seals, tablets, tags, pots and one large signboard from the Indus Valley civilisation, and nobody has an accepted reading of it. This repository has measured how those texts are built: a fixed shape with an opener, a name made of a house crest, a personal part and a tag, and an ending, plus a counting system with its own unit order, and every number below reruns from a script. The sign-by-sign sound values it also tried, one early Dravidian word per sign, passed a wrong word of the same job as often as the accepted word in two decoy tests, so every English or Dravidian word in this repository is a working label for what a sign does, and none is an established reading.

Words used below. A **seal** is a small stone or clay stamp carrying a few signs. A **tablet** is a small flat clay, stone or copper plaque with signs; **tags, pots and rods** are other objects that carry signs. A **sign** is one drawn character, cited by its catalogue number (for example 740 is a jar, 220 a fish). A **face** is one inscribed side of an object, and this project reads one face at a time. The **Lipi catalogue** is the main sign catalogue used here (5,679 faces, 2,162 distinct complete texts); it stores each text in reverse of reading order, so every example below is printed in reading order. The **second catalogue** is Mahadevan 1977, a separate transcription with its own sign numbering, linked to Lipi by a 366-pair crosswalk. **New texts** are the 1,183 second-catalogue texts that have no partner in the Lipi catalogue. A **crest** is the first sign of a name, shared by seals from one house. **House-mates** are two seals found in the same excavated house. A sign's **job** is the role it plays in the text shape (opener, crest, ending, measure, counted thing). A **label** is an English or Dravidian word put on a sign to say what job it seems to do; labels are written in quotation marks below. `measured` means a number that comes out of the data when the script is rerun. `guess` means a meaning we act on and keep testing. Every number below is copied from [MAP.md](MAP.md) or a report in [jobs/out/](jobs/out/).

### What is measured without any word

Each item gives the finding, its numbers and one line on what the numbers mean. The full book of these, with the script that reruns each, is [FRAME.md](FRAME.md).

- `measured` **The template.** Most seal texts run [opener] [name] [ending]. A program (`work_scripts/gloss.py`) gives every sign one slot and fits 68.8% of 2,162 distinct texts tightly; roles learned at other sites raise parsing on unseen Mohenjo-daro and Harappa texts by 8 to 11 points; on the second catalogue every sign gets a role in 89.3% of texts and in 85.4% of the 383 texts with no partner in the first catalogue. *Means:* signs hold fixed positions, and the positions learned on one set of texts work on texts that were not used.
- `measured` **Name = crest + personal part + tag.** A name is up to three signs. The first is shared by house-mates (the same fish variant in 15 of 23 pairs against 36% by chance); the last goes with the ending. Class (the office or rank sign) is a closed set of 26 signs tied to seal size; the name slot holds 384 different signs, and name-slot signs repeat inside houses (19 pairs against 7.8). A marked fish is a mark plus the plain fish: the second sign is the plain fish in 40 of 528 swaps against 133 of 3,332. *Means:* the first sign of a name works as a family emblem, and the last as part of the person.
- `measured` **Endings.** The jar sign (740) ends the text 557 of 743 times. When a sign follows the jar it is the plain man sign 54 times (54 of that sign's 73 texts), or a few others (comb, 679, 621). The spear, porter and comb signs stand in the jar's place and never follow it (spear after jar 0 of 156 on the second catalogue). The name's last sign predicts the ending, the same name keeps its ending across seals, and house, site, period and object type do not predict it. Seal size goes with the closer (median face area: person 738 mm2, jar 645, spear 633, carrier 495, comb 420), and the mix of closers is the same at every site. *Means:* the ending belongs to the person, not to the place or the object.
- `measured` **"X's man", found in the master's building.** The pattern [name X] jar man gives the biggest seals (median face 778 mm2 against 652 for [name] jar) and carries an animal 91% of the time against 78%. The names X are fish-crest names (18 of 50 against 7 of 602 for owners). At Mohenjo-daro 5 of 24 such seals sit in a building that also holds an owner object with the master's crest, against 2.10 by chance (P 0.046); family members sit there at chance (44 of 588 against 49.5). Agent seals are bigger (718 against 581 mm2), and goods tags are stamped by agents three times as often as seals are (20% against 7%). *Means:* the man ending marks a person attached to another owner's house, living where that owner's objects are.
- `measured` **Same-room seals share signs.** Seals found in the same room at Mohenjo-daro within 3 ft of depth share an uncommon sign in the middle of the text about 7 times as often as chance (5 pairs against 0.73); first and last signs show no excess. House-mates ending in the jar share the sign just before it in 15 pairs against 9.3. On photographs of house-mate pairs the shared sign is on both stones in 24 pairs and cut by the same hand in only 4. *Means:* the middle of a text belongs to the household, and different carvers wrote the same sign for the same house.
- `measured` **The seven-city opening and the nine-city pair.** A three-sign opening (920-060-741) is on 38 objects in 7 cities, 24 at Mohenjo-daro (14.5 expected), with 36 different names after it on 38 stones; 29 of the 38 are seals (76% against 48%). The pair 590-390 is on 71 objects in 9 cities (8 named sites plus one stone of unknown find place), and its 22 Mohenjo-daro seals with a recorded house sit in 21 different houses (same-house pairs 1 against 1.84 by chance). *Means:* both are formulas that travel across houses and cities, as an office or a trade line would, and are not one family's name.
- `measured` **Two ways of counting.** Short strokes run 1 to 8 and full-height strokes 1 to 5, as two separate series, and a two-sided tablet face is often the cup sign plus 2, 3 or 4 long strokes (107 / 157 / 123 objects; cup plus 1 stroke occurs 4 times). *Means:* there are two separate counting series. `guess`: they count two kinds of thing.
- `measured` **Measures in twelves, with litres.** 479 of 481 cup counts are 1, 2, 3, 4 or 6, the divisors of 12 below 12; the count 5 is never written (0 of 206 on the second catalogue). One cup stroke is about 9.2 litres on three measured pots; the six-stroke pot holds 55.56 L and the three-stroke pot 27.30 L. Only 49% of container counts fall on the weight series 1, 2, 4, 8. *Means:* the cup counts are whole fractions of a larger unit of twelve cups, and the pots are sized to match.
- `measured` **Unit order.** Lines with two or more measure signs keep a fixed order of units in 85% of meetings (124 of 146 on distinct texts) against 69% when the unit signs are shuffled inside each line (P 0.002). Quarter-unit counts run 1 to 3 and never 4; the largest unit is never above 5. *Means:* units are written big before small, as in other account scripts.
- `measured` **Ration arithmetic.** 3 diamond-sign heads and 3 load signs go together on 22 of 22 tablets that carry both (a batch of 22 steatite tablets, Harappa trench E-11); 3 heads x 4 cups = 12 cups on 21 tablets of that batch, and 2 x 3 = 6 on 5 more. On account objects with two numbers the numbers are equal on 67 of 190 against 52.2 by chance (P 0.006). *Means:* these tablets are small bookkeeping chits whose numbers multiply and match.
- `measured` **The picture-side ties.** Pictured copper tablets: 11 of 12 tablets of one text show the elephant and carry sign 923 against 14% of pictured copper tablets (P 6e-9); tablets showing the gharial carry sign 255 on 11 of 53 against 3.1 by shuffle (P 0.0002). All 11 gharial tablets are copies of one Harappa text and the elephant ties come from copies of two texts, so per distinct text the ties do not hold. On some copies the picture is written as a sign (deer sign 341 for the stag, 753 for the hare). *Means:* the picture side and the sign side of a copper tablet go together, through few texts.
- `measured` **The seal animal.** The stand drawn in front of the unicorn is shared by seals from the same room 38.1% against 17.2% by chance (139 pairs, P 0.0003), fading with distance (room 1.79, block 1.27, area 1.13) and independent of the crest (P 0.91). The species does not follow crest, first name sign, ending or area (P 0.47 to 0.91). The short-horned bull with trough is 14 of 26 beast seals abroad against 92 of 1,575 at home (P 7e-11), and all 13 round seals abroad carry it. *Means:* the stand pattern marks the household and the species marks something else, which is the exchange circuit in `guess`.
- `measured` **The system is flat across time.** 2,666 of 4,694 objects get a time bin. Agent seals are 4.5 / 4.1 / 4.5% of seals in the early, middle and late bins; fish-crest names 12.3 / 12.6 / 12.8%; the office opening 1.4 / 0.9 / 0.8%; endings, text length, star-name numbers and fish spelling are flat as well. The time axis works: inscription-only seals at Harappa go from 14 of 99 to 33 of 98 (P 0.0018), as the excavators found. *Means:* one key reads about six centuries. Before the cities, 24 of 35 texts are one sign long and the jar is on 3 of 35 against 896 of 2,122 later (P 1.9e-5).
- `measured` **Counting before names.** Things take their number before them 450 to 220; measure and share words take it after 315 to 49. Inside names the stroke form locks to the fish: tall two with the plain fish 65 of 73, short two with the marked crest fish 62 of 63 (P 1.6e-28), and 14 of 16 and 17 of 17 on new texts. Room-mates share the number before a fish in 5 pairs against 0.74; numbers in names bunch on 2 (136 of 191 distinct name texts). *Means:* a number inside a name is a fixed part of the name, and an amount outside a name comes before its thing.
- `measured` **The quarter sign before the king sign.** The quarter sign (061 or 820) stands right before sign 142 in 11 of 81 uses against 1.37 expected (P 1.3e-7), at both big cities; Mohenjo-daro's 22 objects with sign 142 carry 13 different crests. *Means:* one sign pair is a fixed title phrase, repeated across houses.
- `measured` **The cotton line, at home and on the cloth-backed sealing from Iraq.** The sealing said to be from Umma in Mesopotamia (Ashmolean 1931.120; woven cloth on the back) reads `127 705 002 004 390`; a seal from Salut in Oman ends `002 004 392`. At home `002-004` is followed by a tree sign in 16 of 20 places, and a 4 before a tree sign is 39 of 90 places at home and 3 of 6 abroad (chance 2.8%). Tree sign 390 is counted in lots (86 of 90 counted uses have a count of 3 or more); tree sign 407 takes a tall two on 9 of 28 places against 2 of 90 for 390 (P 3e-5). 11 of 5,610 home faces share the tail `002 004 390`, none shares four signs, and the Dholavira stage II seal has the same tail. `guess`: "cotton" is the label for 390 and the Umma line is a lot label on a cloth-covered object. *Means:* a count-count-tree-sign line stands at home and abroad, and the sign sequence is measured whatever word it carries.

### What each kind of object says

In word-free terms the objects fall into four kinds, and each kind has its own signs. Examples are shown as [job] sequences, with the working-label English in brackets after them (the English is a label).

- **Owner label** (most seals): [opener] [name: crest, personal part, tag] [ending]. Class signs are a closed set of 26; the name slot holds 384 signs. Seal size follows the ending.
- **Ration chit** (steatite tablets): [head count] [load count] [cup count], numbers that multiply to twelve.
- **Goods tag** (tags and sealings): [sign] [sign] [count] [goods sign] [ending]. Each class of goods object has its own signs: tags (500, 417, 056, 890, 048, 055, 892), bangles (two-leaf 840, 7.9 times chance), pots (440, 480), ivory rods (comb 400 ends 29% of rods against 2.7% of seals). Pots carry an amount (91 of 122 single-count pots use tall strokes) and an owner on 9%.
- **Land or crop record** (copper tablets): signs 503, 615 and 845 sit on copper tablets at 4.0, 4.7 and 8.4 times chance on new texts, and a count stands before 061.

Six examples (reading order):

1. Seal H-502, Harappa: `032-220-740-090` = [tall two] [fish crest] [jar ending] [man ending] (label: "manager of the Two-star house").
2. Seal M-294, Mohenjo-daro, 5 objects carry the text: `003-220-740` = [three] [fish crest] [jar ending] (label: "of the Three-star house").
3. Load tablet H-190, Harappa, 5 tablets, and the same shape on seal H-152: `465-806-158` = [A-sign with a comb of ticks, a count] [sign 806] [load-carrier sign] (label: "n loads of crop, carried"; the carrier sign follows the A-sign plus 806 in 36 of 36).
4. Ration batch H-2218 to H-2239, Harappa trench E-11: [3] [diamond sign] [3] [load sign] [4] [cup sign] (label: "3 hands, 3 loads, 4 cups, about 37 litres").
5. Lothal goods tag L-124, 11 objects: `705-500-741-001-055-220-740-090` = [sign 705] [sign 500] [sign 741] [one] [sign 055] [fish] [jar ending] [man ending] (label: "by ship, first ward: one dozen fish; the house's agent"; 500 sits at Lothal on 8 of 12 new-text uses against 8%).
6. Copper tablets, Lipi row 2275.1, 29 tablets all at Mohenjo-daro: `503-615-752-740` = [land sign 503] [land sign 615] [sign 752] [jar ending] (label: "of the house of the heir of Hill-Field").

### The decoy tests

- The sound passes gave each sign one Dravidian word and counted a word as confirmed when a prediction written from its meaning came true on facts outside the texts used to choose it.
- Test 1 (`jobs/out/decoy_test.md`): 60 signs, 30 with their accepted word and 30 with a word moved from another sign of the same job; two blind testers wrote predictions first, one run each. Came true: accepted word 9 of 58, decoy word 10 of 60 (Fisher P 1.0).
- Test 2, the full method (look at the sign's data, predict, one redesign on a miss): accepted word 17 of 29, decoy word 19 of 30; the pass rate is the same for accepted and decoy words in every job class.
- A third test (`jobs/out/blind_test.md`) showed readers four English versions of one inscription and asked for the real one: real 29.2% pooled, same-job shuffles 34.2% and 22.2% (chance 25.8%).
- *Means:* the procedure passes about six words in ten whether the word is the accepted one or a wrong one of the same job. The jobs are supported and the exact words are not, so every word is a label, and what the sound passes (`values_master4.csv`: 195 signs, 160 strict, 28 wide, 7 testing) support is the job each sign does. Any later pass on words carries decoys mixed in and reports real against decoy.

### The word list

The word list is `work_data/values_master4.csv` (195 signs), with the whole catalogue in English in [CORPUS.md](CORPUS.md) (5,679 faces), 120 inscriptions word by word in [READINGS.md](READINGS.md), and the people and houses in [WHOSWHO.md](WHOSWHO.md). Every English word and every Dravidian word in those files is a working label for a sign's job. A line there that reads "n loads of crop, carried" means a count slot, a produce-or-counted-thing sign and a carrier sign, in that order, with the order measured. Grades in CORPUS.md such as "whole" (2,190 of 5,679 faces) mean a label on every sign of the face.

### What went against

- The decoy tests above (accepted word 9 of 58 against decoy 10 of 60; 17 of 29 against 19 of 30), and the English-plausibility test (a reader cannot pick the real line from same-job shuffles; the builder's own sense rate of 73% was a third when strangers graded).
- Ration size following rank (bondsman 4 cups, three-measure holder 3); total lines (one number equal to the sum of the others 10 of 70 against 14.9 by chance); batch totals in whole large units (0 of 16).
- Administration thickening with time; a trade peak for the overseas bull.
- Name numbers bunching on 3, 6, 7 (they bunch on 2); "X's man" as servant of a house-mate or as head of his own house (first name sign matches a house-mate's 4 of 20 against 3.3 by shuffle); same name on a seal and a tablet found near each other (three tries).
- The animal as clan, ward or rank (the stand code as a house mark came in at 1.04).
- Spear seals concentrated in citadels (12 against 11.9 expected).
- Cuneiform side: of 585 CDLI tablets from Girsu, Lagash and Umma naming Guabba or Meluhha, 33 are sealed and 13 are Meluhha or textile texts, and all 13 seal legends are cuneiform; foreign texts are not more lot-like than home texts (49% against 45%).
- Four signs fail their job in every time bin (482, 575, 850, 717).

### What is open

- **The language question.** The pun test (nine pictures, a meaning each slot needs, a sound-alike rule scored against chance inside each dictionary) gave Dravidian 7 of 9 against 1.02 expected, Munda 0 of 9, Sumerian 1 of 8, Sanskrit at chance, with small numbers; it is the one language-family result left standing. It is now being rerun by machine with a built-in shuffle control, so the language result will come with its own false-alarm rate.
- **The outside match in cuneiform.** No match yet: no Meluhha-tagged cloth word in 202 CDLI Meluhha texts, no cotton word in Sumerian, no object carrying both scripts, loan candidates weak (word-shape test 196 against 139 by shuffle, P 0.07). The nearest link is the Umma sealing above. Next way in: a Guabba or Girsu wool tablet bearing a non-cuneiform seal impression, and the Ashmolean photo (Tosi counts six signs, the catalogue five). 24 CDLI seal records with no transcription need their photographs (`jobs/out/outside_match.md`).
- **The long tail.** 1,276 faces are only part read and 134 have no valued sign; multi-face tablets are read face by face, not as one record.

### Where things are

- [FRAME.md](FRAME.md): the word-free findings as a short book, each with the script that reruns it.
- [AGENTS.md](AGENTS.md): the working rules that bind everyone who works on the project.
- [MAP.md](MAP.md): what we currently believe, each line tagged `measured` or `guess`, the live leads ranked, and what each predicts next.
- [DIARY.md](DIARY.md): dated one-line entries of what was tried.
- [CORPUS.md](CORPUS.md), [READINGS.md](READINGS.md), [WHOSWHO.md](WHOSWHO.md), `work_data/values_master4.csv`: the word list (labels).
- [jobs/out/](jobs/out/): one report per line of work, holding the numbers quoted above.
- [work_scripts/](work_scripts/): the scripts that produce every number (parsers `gloss.py` and `gloss2.py`).
- Live map page: https://claude.ai/artifact/BqwVyHNfHLEoEoSvUn1Yxb (a dependency graph of the readings; private to the owner).

## Already known: cited, not claimed

Directionality of sign order (Yadav et al. 2010), hidden-sign prediction and conditional entropy (Rao et al. 2009), fish-sign diacritics (Parpola 1994), arithmetic reading of the stroke tablets (Fuls 2020), same-front/different-reverse tablets (Priyanka 2003; Mukhopadhyay 2023), and the comparison with non-linguistic controls (Sproat 2014). Full references are in [CITATION.cff](CITATION.cff); where each was re-derived is in [research/docs/README.md](research/docs/README.md).

## Reproduce

Python 3.11 and Node 22 (the database build needs Node 22.5 or later).

```sh
python -m pip install -r requirements.txt
make check audit verify db     # a few minutes, no network
make campaign                  # full four-route rerun; long; rewrites files under research/campaigns/
python research/tools/check_headline_numbers.py
```

Each extension study runs on its own: `python3 research/extensions_20261001/<study>/<script>.py`. CI ([reproduce.yml](.github/workflows/reproduce.yml)) runs the checks, the campaign and the headline-number comparison on every change under `research/`, `db/` or `docs/`.

## Layout

| Path | Contents |
| --- | --- |
| [jobs/out](jobs/out/) | Reports on each reading above: counted things, carrier phrase, name slot, glossing, seals abroad, possessive model |
| [work_scripts](work_scripts/), [work_data](work_data/) | Parsers (`gloss.py`, `gloss2.py`), analysis scripts and the tables they write |
| [research/docs](research/docs/README.md) | The 5 notes worth reading, an index, and `archive/` (422 working notes, kept as a record) |
| [research/extensions_20261001](research/extensions_20261001/README.md) | Five October 2026 tests: one script, JSON output and one-page report each |
| [research/data](research/data/) | Frozen Mahadevan concordance, the Lipi catalogue, claim ledger JSON (`claim_ledger/claims.json`) |
| [research/campaigns](research/campaigns/integrated_20260906/README.md) | The September four-route search and its completion pass |
| [research/tools](research/tools/) | Audit and check scripts |
| [research/publications](research/publications/20260907/README.md) | Index of the two paper drafts |
| [db](db/README.md) | SQLite database of the evidence, with its build script and audit report |
| [docs](docs/) | The project website source (GitHub Pages) |
| [slm](slm/README.md), [embeddings](embeddings/README.md) | Small-language-model and embedding experiments |
| `evidence/tmp` | Raw source material and working files |
| `workspace/codex` | Hooks and logs from the earlier agent setup |

One source file over GitHub's 100 MB limit is stored in chunks with a checksum manifest; see [SPLIT_FILES.md](SPLIT_FILES.md). [MERGED_BRANCH_STATE.md](MERGED_BRANCH_STATE.md) records how the two original branches were merged.
