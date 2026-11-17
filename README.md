# IVC: looking for checkable structure in the Indus script

By Cúper (Yousef) Anas · [Website](https://cuuper22.github.io/ivc/) · [Cite this](CITATION.cff)

## Where the project stands (2026-11-17)

The Indus script (about 2600-1900 BCE, a few thousand short inscriptions on seals, tablets, pots and tags) has no accepted reading. This project works from the Lipi catalogue (5,679 inscription rows, 2,162 distinct complete texts; the catalogue stores each text in reverse of reading order, so every example here is printed in reading order) and tries to read real inscriptions sign by sign. Each item below says what we now read, the numbers behind it, and where to look. "Measured" means a count that comes out of the data when you rerun the script. "Working reading" means a meaning we assign and keep testing against new objects.

**1. Load tags: "n loads of crop, carried".** Measured: an A-shaped sign with a small comb of 3 to 8 ticks at its foot, then the leaf-on-a-tree sign (806), then the porter sign (a person carrying two burdens, 154 or 158). The porter follows the A-comb and leaf in 36 of 36 cases; 42 texts carry the A-comb; 11 of the 23 Harappa examples come from mound F, the granary and work-platform area. Working reading: the A-comb is a number of loads, 806 is a crop, the porter says it was carried. Files: `jobs/out/carrier_phrase.md`, `work_scripts/carrier_load.py`.

**2. Ration tablets: "3 diamonds | 4 cups | 3 loads".** Measured: 22 three-face steatite tablets, 20 of them from Harappa trench E-11, carry a count of three before the diamond sign, a count of three before the porter sign, and a cup sign with a count of four. Cups to loads is 4 to 3 in 21 of 22; the other is 3 to 3 to 3. Across the corpus the cup is counted 388 times, with 2, 3 or 4 strokes (100, 150 and 116 times; 1 or 6 strokes 8 times, 5 never), and the count is written before the cup in about 388 of 470 cases. Working reading: each tablet is one account, a delivery of cups for three diamonds (a unit of people or households) and three porters. Files: `jobs/out/counted_things.md`, `work_data/tablet_records_cup_load.csv`, `work_scripts/counted_records.py`.

**3. Seals: opener, name, possessive jar, relation.** Measured: seal texts follow one order. An opener comes first (a diamond or six-spoke wheel with two strokes, or the cap `060`). Then a name. Then the jar sign (740), which ends the text 557 times out of 743. When a sign follows the jar it is the plain man sign 54 times (54 of that sign's 73 texts), the comb 11 times, the X with a table-shaped hat (679) 10 times (10 of its 13 texts), or a tall barred rectangle (621) 5 times. The spear and the porter signs do not follow the jar (spear 0 of 152 uses, porters 2 of 47, 0 of 25 and 0 of 32 for the three kinds); they close texts that have no jar, in the jar's place. Working reading: the jar is the possessive ending, so `[name] jar` is "of [name]", the owner of the seal, and `[name] jar man` is "[name]'s man", a servant or agent. Possessor before possessed and the title after the name, with counts before counted things: the order of a head-last language. Rebuilt parser: `work_scripts/gloss2.py` assigns every sign a role in 1,957 of 2,162 distinct complete texts (90.5%) against 1,487 (68.8%) for the first parser (`work_scripts/gloss.py`); the stricter version, names of at most three signs and one jar, is 1,775 (82.1%). The new rule is looser about names, so the two numbers are not the same test; every reading is in `work_data/gloss2_all.csv` and 60 are written out in `GLOSSES.md`. Servant and master checks are in `jobs/out/possessive_model.md`: servant seals are not smaller than owner seals (median face 758 against 645 mm2), and 21 of 89 servant seals have a same-named owner seal, 9 of 70 for names of two or more signs.

**4. Names: house crest, self, tag.** Measured: a name is 1, 2 or 3 signs (45%, 33%, 18% of names). Marked fish signs open names, and when two seals from one excavated house both open with a fish it is the same fish in 15 of 23 pairs (36% by chance). Two signs always end a name: the branching U (760) last in 39 of 39, the three-headed person (100) last in 42 of 42. Seals from one Mohenjo-daro room within 3 ft of depth share an uncommon sign in the middle of the text 5 times against 0.73 by chance. Working reading: a name is a house crest, a personal sign, and a closing tag, like family name, given name and title. Files: `jobs/out/name_slot.md`, `work_scripts/name_slot.py`, `work_data/name_rows.csv`.

**5. Two counting systems.** Measured: counts are written as short half-height strokes or as tall full-height strokes, and the thing counted picks the series, not the object it sits on. Tall strokes count measures and containers (the cup 96%, the box 88%, the jar 75%); short strokes count grown or living things (the crop sign 806 100%, fish variants 73 to 88%, women 78%). Signs differ in tall-stroke share at chi-square 88 over 10 degrees of freedom (p = 1e-14). Tall counts stop at 4 and short counts at 5, with stacked strokes carrying the short series to 8. Working reading: one system counts goods measured in vessels, the other counts crops, animals and people. Files: `jobs/out/counted_things.md`, `work_data/counted/`.

**6. Seals found abroad.** Measured: on 15 round seals found in the Gulf, Mesopotamia and Iran the jar and the man sign never occur together; a single short stroke stands where the jar goes in 9 of 23 round seals. Square seals abroad carry ordinary home names. Working reading: round seals write foreign names with Indus signs. File: `jobs/out/abroad_seals.md`.

Where to go next: [MAP.md](MAP.md) lists what we believe and the live leads in order, [DIARY.md](DIARY.md) lists what was tried and when, [GLOSSES.md](GLOSSES.md) has 60 inscriptions read in plain English with object names and findspots, and [AGENTS.md](AGENTS.md) holds the working rules.

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
