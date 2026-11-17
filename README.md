# IVC: looking for checkable structure in the Indus script

By Cúper (Yousef) Anas · [Website](https://cuuper22.github.io/ivc/) · [Cite this](CITATION.cff)

## Where the project stands (2026-11-17)

The Indus script is a set of short inscriptions (about 2600-1900 BCE) on stamp seals, clay and copper tablets, pots, tags and one large signboard from the Indus Valley civilisation, and nobody has an accepted reading of it. This repository reads the inscriptions sign by sign: it assigns each sign a slot in a fixed text shape, guesses an early Dravidian word for each sign, and checks every guess against objects that were not used to pick it. The claim is a web of tentative readings that hold together: 2,190 of the 5,679 inscribed faces in the working catalogue now read in English from start to finish under those guesses, and the guesses keep predicting facts on texts they were not built from.

Words used below. A **seal** is a small stone or clay stamp carrying a few signs. A **tablet** is a small flat clay, stone or copper plaque with signs; **tags, pots and rods** are other objects that carry signs. A **sign** is one drawn character; signs are cited by their catalogue number (for example 740 is a jar). A **face** is one inscribed side of an object, and this project reads one face at a time. The **Lipi catalogue** is the main sign catalogue used here (5,679 faces, 2,162 distinct complete texts); it stores each text in reverse of reading order, so every example below is printed in reading order. The **second catalogue** is Mahadevan 1977, a separate transcription with its own sign numbering, linked to Lipi by a 366-pair crosswalk. **New texts** are the 1,183 second-catalogue texts that have no partner in the Lipi catalogue and were never used to choose a sound value, so a prediction that holds on them is a real test. `measured` means a number that comes out of the data when the script is rerun. `guess` means a meaning we act on and keep testing. Every number below is copied from [MAP.md](MAP.md) or a report in [jobs/out/](jobs/out/).

### The numbers

- `measured` **Grades of all 5,679 faces** ([CORPUS.md](CORPUS.md), `work_data/corpus_english.csv`): whole 2,190, part 1,276, damaged 2,079, none 134. *Whole* means every sign on the face has a sound value we build on and nothing is lost. *Part* means some signs read and the rest show as a bracketed number. *Damaged* means the face has a lost, unclear or broken sign. *None* means no sign on the face has a value. Whole is the share of faces the English covers end to end.
- `measured` **Strict and wide, on the 3,600 complete faces of the Lipi catalogue** (`jobs/out/sound_list_v5.md`): strict 1,825 faces (909 distinct texts) read fully, wide 2,004 (1,029 distinct texts); one pass earlier (`jobs/out/sound_list_v4.md`) it was strict 1,418, wide 1,861. *Strict* counts only sound values whose confirming fact had not been seen while the word was chosen; *wide* also counts values that were confirmed on new-text facts glimpsed while choosing. The 2,190 above is higher because it also counts 264 one-sign faces and 65 faces opened by the eight-signs values.
- `measured` **Draw by eye** (`jobs/out/corpus_english.md`): 40 whole faces drawn by a seeded random draw and read by a person: 25 make sense, 13 are odd, 2 are nonsense. This is the check on whether the rule-built English is sensible; the odd ones are mostly number or measure words sitting inside house names.
- `measured` **Sound values**: `work_data/values_master.csv` lists 149 signs: 116 strict (number signs included), 18 wide, 11 testing, 4 paused.

### How a text is built

- `measured` The **template** is the order most seal texts follow: [opener] [name] [ending]. A program (the template parser, `work_scripts/gloss.py`) gives every sign one slot; it parses 68.8% of 2,162 distinct texts tightly, and roles learned at other sites raise parsing on unseen Mohenjo-daro and Harappa texts by 8 to 11 points. On the second catalogue it gives every sign a role in 89.3% of its texts, and in 85.4% of the 383 texts that have no partner in the first catalogue.
- `measured` A **name** is up to three signs: a **crest**, a personal part, and a tag. The crest is a house or clan emblem and is the first sign; when two seals from one excavated house both open with a fish crest it is the same fish in 15 of 23 pairs against 36% by chance. The last sign goes with the ending. Class (the office or rank) is a closed set of 26 signs tied to seal size; the name slot holds 384 different signs.
- `measured` **Endings**: the jar sign (740) ends the text 557 of 743 times. When a sign follows the jar it is the plain man sign 54 times (54 of that sign's 73 texts), or a few others (comb, X-with-table 679, barred rectangle 621). Spear, porter and comb signs stand in the jar's place and never follow it (spear 0 of 156 on the second catalogue). The ending belongs to the person: the name's last sign predicts it and the same name keeps it across seals.
- `guess` The jar is the possessive "house of" (*kuṭi*), so `[name] jar` is "of [name]". Spear = chief (*vēḷ*), comb = junior (*ciṟ*), load-carrier = keeper (*kā*), each saying what the named person is.
- `guess` **"X's man"**: `[X] jar man` is "X's man" (*āḷ*), an agent or officer of an outside master or institution X. Two earlier versions (servant of a house-mate, head of his own house) went against seal sizes and crests. The masters are fish-named: 18 of 50 against 7 of 602 for owners.
- `guess` Order is possessor before possessed, title after name, count before the counted thing, which is the order of a head-last language.

### What the texts say

Each line gives the object id, the signs in reading order, the sounds, and the English. Every reading is a `guess` built on `measured` slots; the English is a reading under working guesses, not a translation. Full lists with word-by-word glosses: [READINGS.md](READINGS.md) and [CORPUS.md](CORPUS.md).

1. Seal H-502 (Harappa): `032-220-740-090`, *iru mīn kuṭi āḷ*, "manager of the Two-star house".
2. Seal M-294 (Mohenjo-daro; 5 objects carry the text): `003-220-740`, *mum-mīn kuṭi*, "of the Three-star house".
3. Kish seal (found in Mesopotamia): `416-840-060-003-220-590-390-740`, *turumpu iṇai -iṉ mum-mīn peṭṭi parutti kuṭi*, "threshed heap, a pair, of the Three-star boxed-cotton house".
4. Seal C-12 (Chanhu-daro): `920-060-740-031-590-390-161`, *tiṅkaḷ -iṉ kuṭi oru peṭṭi parutti kā*, "in the month: of the house, one boxed-cotton keeper".
5. Load tablet H-190 (Harappa; 5 tablets), and the same shape on seal H-152: `465-806-158`, *(n) (crop) kā*, "n loads of crop, carried".
6. Tablet H-2024 (Harappa; 8 copies): `347-741-176-740-090`, *kalai orukuṭi iṟai kuṭi āḷ*, "the Stag of the first ward: agent of the Tax house".
7. Tablet H-252 (Harappa; 29 copies): `501-405-002-240-520`, *kumi kiḷai iru mīmīn vēḷ*, "stock of the kindred, two: High-star the chief".
8. Ration tablets, batch H-2218 to H-2239 (22 steatite tablets, Harappa trench E-11): three diamonds, three loads, four cups. `measured`: 3 diamonds = 3 loads on 22 of 22 tablets carrying both; one cup stroke is about 9.2 litres on three measured pots. `guess`: the diamond is "hand", a head counted for work, and the tablet is a gang leader's chit for 3 hands, 3 loads, 4 cups (about 37 litres).
9. Pot M-1379 (Mohenjo-daro): `920-540-740`, *tiṅkaḷ paṟai kuṭi*, "the month's paṟai (drum) measure, of the house". Pot H-1740 (Harappa; 2 pots): `540-540`, *paṟai paṟai*, "two drum-measures of grain".
10. Copper tablets, Lipi row 2275.1 (29 tablets, all Mohenjo-daro): `503-615-752-740`, *malai vayal maka kuṭi*, "of the house of the heir of Hill-Field". Copper tablets M-1482 (7 tablets): `706-033-923-740`, *kalam mū maruppu kuṭi*, "three kalam (a grain measure), the crescent-horn: of the house".
11. Lothal goods tags, L-124 (11 objects): `705-500-741-001-055-220-740-090`, *kalam pāy orukuṭi oru paṉṉiru mīn kuṭi āḷ*, "by ship, first ward: one dozen fish; the house's agent".
12. Dholavira signboard (catalogue id 144.1, gypsum, about 3,000 mm long, over the north gate): *kāl kuṭai aracu · kāl kaṇ kuṟi oru · kāl kāl maru-*, "the quarter of King Umbrella; the quarter of the Marked Place, number one; quarter by quarter, the Maru kin". The wheel sign *kāl* "quarter" starts all three phrases (a wheel is text-initial 187 of 244 times). The catalogue records 9 signs; the 10-sign string in print traces to one blog comment.

### Why the language is read as early Dravidian

- `measured` **The pun test** ([jobs/out/rival_languages.md](jobs/out/rival_languages.md)): nine pictures, each with a meaning the slot it sits in needs (a fish in the slot where "star" fits, a jar where "house of" fits), and a sound-alike rule: does the language have a word that sounds like the picture's name and means what the slot needs? The same rule, same slots, and chance measured inside each dictionary: Dravidian 7 of 9 (1.02 expected), Munda 0 of 9, Sumerian 1 of 8, Sanskrit at chance. Burushaski and Elamite word lists were too small to run. Earlier, 9 of 12 slot pairs worked fully only in Dravidian, and Sumerian and Elamite word order does not fit the measured order.
- `measured` **Predictions that came true on new texts** (never used to choose the values):
  1. On the second catalogue: load tag 14 of 14, man after jar 74%, spear after jar 0 of 156, cup never counted five (0 of 206).
  2. Month sign 920 follows ladder 320 in 5 of 7 new-text uses against 0.7% by chance (P 3e-10).
  3. Land words sit on copper tablets: 503 at 4.0 times chance, 615 on 16 of 86 at 4.7 times, 845 at 8.4 times.
  4. The sail sign 500 sits at Lothal on 8 of 12 new-text uses against 8%; the pair 705-500 is 3 of 64 against 0.4%.
  5. A count follows sign 705 in 28 of 64 new-text uses against 14.1% (P 8e-9), all 28 in tall strokes (P 1e-13).
  6. Sign 527 is the last sign of the text on 7 of 9 new texts against 28%.
  7. Sign 335 is followed by a jar or "child of" on 4 of 6 new texts against 7.9%.
  8. Inside names the stroke form locks to the fish: 14 of 16 and 17 of 17 on new texts (62 of 63 and 65 of 73 on the main catalogue, P 1.6e-28). The box sign 590 takes tall container strokes on new texts 8 to 3.
- `measured` Of the 25 most useful signs given words in the fourth pass, 22 had their prediction come true, 9 of them on unseen facts.

### What went against

Each is a `measured` result against a reading; the rescue plan for each is in the report named.

- The eye sign as copper: 790 on new-text copper 0 of 20, and 832 likewise; the excess is 850 alone (`jobs/out/sound_list_v3.md`).
- Sesame 838 on tags and pots: 1 of 19; as bone, 0 of 5 new-text rods (`jobs/out/goods.md`, `sound_list_v3.md`).
- Crop sign 806 with the cup: 0 of 133; fish 220 as a coast sign (`jobs/out/goods.md`).
- Cotton 390 on ivory rods: 1.0 times chance; the spindle-whorl check came in at P 0.011 where below 1e-6 was predicted; no second whorl site (2 of 71 clay or stone objects outside Karanpura; 5 whorl-shaped objects with photos carry no 390) (`jobs/out/beads_cotton.md`, `cotton_house.md`).
- "Chest-guard" for 590-390: box plus a keeper sign is 2 of 209 box places (`jobs/out/cotton_house.md`).
- Measure reading of 705: not on tablets or pots beyond chance on new texts (5 of 66 against 21%); not in Harappa mound F (30 of 90 against 34%); 1 of 384 faces abroad (`jobs/out/sound_list_v4.md`).
- The animal as clan, ward or rank, and the catalogue's cult-stand code as a house mark (1.04) (`jobs/out/animals.md`).
- Name numbers bunching on 3, 6, 7 (they bunch on 2: 136 of 191 distinct name texts), name numbers following the 28 lunar-mansion star counts, strokes drawn inside a fish as a written number, and same-house sharing of exact compounds (`jobs/out/star_names.md`).
- Sign 060 as dative, plural or "and"; 525/526/527 all standing after the gate sign in 75% or more of uses (38%, 37%, 40%) (`jobs/out/eight_signs.md`).
- "X's man" as servant of a house-mate or as head of his own house: the first name sign matches a house-mate's in 4 of 20 against 3.3 by shuffle (`jobs/out/endings_heads.md`).
- Spear seals concentrated in citadels: 12 against 11.9 expected; person-with-staff seals larger: 572 against 618 mm2 (`jobs/out/language_candidates.md`).
- Of the 89 second-list sound values, 38 went against at first (including 803 "house", 717 "servant", 900 "month", 171 "weight", 413 "grain"); after second tries the list sorts as 34 building on, 37 testing, 18 paused (`jobs/out/sound_list_v2.md`).

### What is still open

- `measured` **The outside match in cuneiform.** No match yet: no Meluhha-tagged cloth word in 202 CDLI Meluhha texts, no cotton word in Sumerian, no object carrying both scripts, loan candidates weak (word-shape test 196 against 139 by shuffle, P 0.07). The nearest link is a sealing said to be from Umma (Ashmolean 1931.120) whose back carries a cloth impression and whose text ends `002 004 390` ("2, 4, tree sign", a cotton lot line; `002-004` is followed by a tree sign in 16 of 20 places at home). Next way in: a Guabba or Girsu wool tablet bearing a non-cuneiform seal impression, and the Ashmolean photo (Tosi counts six signs, the catalogue five) (`jobs/out/outside_match.md`).
- `guess` **Clashes still alive.** Box-tree pair 590-390 as "boxed cotton" (*peṭṭi parutti*); 335 "town" (*ūr*) against "bin" (*kūṭu*) for the one Harappa grain formula; 527 "guard" against "door"; 060 "in" (*uḷ*) against the genitive; tree sign 405 "thread" is the weakest value (failed 2 of 4); 838 sesame against bone, alive for rods only; the Dholavira "Marked Place" and "King Umbrella" words rest on 6 uses or fewer.
- `measured` **Signs blamed for odd readings** in the 40-face draw: 904, 900, 824, 840, 055, 690, 806, 501, 368, keeper counts, 861, and 060 away from an opener. They read as goods words that the parser puts in the name slot.
- `measured` **The long tail.** 1,276 faces are only part read and 134 have no valued sign (CORPUS.md shows each unvalued sign as a bracketed number). Multi-face tablets are read face by face, not as one record, and some counts attach to the wrong neighbour. Signs 407 and 048 are missing from the new texts and need a crosswalk link to be tested; 167 closes only kalam tablets.

### Where things are

- [AGENTS.md](AGENTS.md): the working rules that bind everyone who works on the project.
- [MAP.md](MAP.md): what we currently believe, each line tagged `measured` or `guess`, the live leads ranked, and what each predicts next.
- [DIARY.md](DIARY.md): dated one-line entries of what was tried.
- [READINGS.md](READINGS.md): 120 inscriptions read whole, word by word, with object ids and findspots.
- [CORPUS.md](CORPUS.md): all 5,679 faces read in English by rule, with the key and the grade counts by site.
- `work_data/values_master.csv`: the sound value of every valued sign with its status, report and alternative reading.
- [jobs/out/](jobs/out/): one report per line of work, holding the numbers quoted above.
- [work_scripts/](work_scripts/): the scripts that produce every number (parsers `gloss.py` and `gloss2.py`, corpus builder `corpus_build.py`).
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
