# The language question by machine: rebus test with no hand-picked words

## What was found

**No language beats its controls.** Run with every choice fixed in code, across 19 dictionaries in 7 language families, 3 sound distances, 2 keyword breadths and 3 controls, not one cell (0 of 312: 19 dictionaries plus 7 families, times 6 cells, times 2 scores) beats all three controls at P below 0.05. The rebus principle as tested here (the word for the pictured thing sounds like a word whose meaning fits the sign's job) does not single out Dravidian, Munda, Indo-Aryan, Sumerian, Akkadian, Elamite or Burushaski. This goes against the earlier pun test (Dravidian 7 of 9 against about 1 expected): the machine finds the same Tamil pairs that test used (fish *mīṉ* ~ *mīṉ* "star" on a crest sign, spear *vēl* ~ *vēḷ* "chief" on an ending sign, both at the strictest sound match), but a Tamil dictionary with its sounds dealt at random among its words, or with the jobs dealt at random among the signs, gives as many such pairs. At the family level, strict match, narrow keywords: Dravidian 42 of 63 picture-job units hit; jobs dealt at random give 38.4 (P 0.045); sounds dealt at random give 43.5 (P 0.72). What that means: the Dravidian hit rate is what the density of short look-alike words in DEDR produces by itself.

**The one pattern that leans one way: Dravidian picture words sound like "job words" in general, not like their own sign's job.** 14 cells beat controls 2 and 3 but not control 1; 10 of them are Dravidian (DEDR Tamil, Malayalam, Kannada, Telugu; Wiktionary Tamil and Kannada): 10 of 96 Dravidian cells, against 2 of 48 Indo-Aryan, 1 of 60 Munda, 1 of 36 Sumerian and 0 for Akkadian, Elamite, Burushaski. In those cells the real picture words, with their real sounds, have more sound-alikes carrying title / name / measure / crest meanings than outside nouns do (control 2) and than scrambled sounds do (control 3), but the match to the sign's OWN job is no better than a random deal of jobs (control 1). Example: DEDR Tamil, strict match, wide keywords: share 3.19 against 1.22 for outside nouns (P 0.001) and 1.51 for scrambled sounds (P 0.005), but 2.51 for jobs dealt at random (P 0.13). Read plainly: in Dravidian the names of the pictured things (man, fish, tree, leaf, jar, bow) sit among homophones that mean chief, son, star, measure more often than chance; which of those meanings goes with which sign is not shown. Control 1 has little power here, because the parser puts 111 of the 149 pictured signs (35 of 63 units) in the personal-name job, so dealing jobs at random mostly moves name to name.

**Sound-alike swap pairs: no language points.** 291 sign pairs swap in two or more otherwise identical texts; 65 of them pair two differently drawn things with pictures. Dravidian picture names are sound-alikes in 16 / 58 / 63 of the 65 (strict / medium / loose) against 17.1 / 56.7 / 64.5 when the pictures are dealt at random (P 0.64 / 0.44 / 0.98). The only cell that beats both swap controls is Munda at medium (21 against 13.3 random pairs, P 0.014, and 12.7 pictures dealt, P 0.028), and reading its matches shows they are not picture names: a Santali "fish basket" word against a "leaf bag" word, and an OCR-damaged Mundari "male servant" word against a fish-catching verb.

Rescue plan, straight from what limited this run (detail at the end): (1) more pictures: 194 of 498 signs had no thing-word in their description (the comb 400 is one; it is described only as "vertical line with small horizontal lines"); a description pass over the glyph images in `work_data/mahadevan_glyphs/` would add them; (2) jobs that split the name slot (crest / self / tag inside the name are measured, but most pictured signs land in plain "name"); (3) dictionaries that keep homonyms apart (in the flat word lists, words spelled alike are one entry, so the strict match finds nothing in 11 of the 19 dictionaries); (4) Proto-Dravidian reconstructions and full Munda dictionaries.

## Words used in this report

- **Picture noun**: the thing a sign's drawing shows (fish, man, jar, tree), taken by rule from the shape description.
- **Job**: what the sign does in a text, from the template parser (opener, crest, name, tag, title/ending, measure, counted thing, time).
- **Unit**: signs with the same picture nouns and the same job count as one test (fifty different "person" signs in the name job are one test, not fifty). 149 pictured signs with a job make 63 units.
- **Picture word**: a dictionary word whose gloss names the thing in its first 3 words.
- **Sound-alike**: another dictionary word (different entry) within the sound distance of a picture word, not itself glossed as the same thing.
- **Hit**: a unit for which some sound-alike has a gloss (first 5 words) containing a keyword of the unit's job.
- **Share**: for each unit, the share of all its sound-alikes that carry a keyword of its job; summed over units. This is the score with power: the hit count saturates once sound-alikes are many.
- **Sound distance**: strict = same spelling once accents, dots and vowel length are dropped; medium = same consonants in the same order (vowels free); loose = consonants differ by one (one changed, added or dropped).
- **Keyword breadth**: narrow and wide lists of meanings a word of that job could have, written once, the same for every language (German copies for the German-glossed Elamite dictionary).
- **Control 1**: jobs dealt at random among the units, 2,000 times (does the right job match better than a wrong one?).
- **Control 2**: every picture noun swapped for an outside concrete noun (water, stone, dog, ...), 2,000 times (do the real pictures do better than any drawable things?).
- **Control 3**: the dictionary's sound forms dealt at random among its words, 200 times (keeps the exact density of look-alikes and the gloss habits, cuts every real tie between sound and meaning). A consistent swap of consonant letters, the version first named, leaves every look-alike relation unchanged and so would measure nothing; this replaces it.
- **P**: share of control runs scoring at least the real score. Small P = the real score is above what the control gives.

## How it was built (all choices fixed in code before scoring)

1. Pictures (`work_scripts/lang_m_pictures.py` -> `work_data/lang_m/pictures.csv`): first sentence of each shape description plus quoted names and "(arrow? spear?)" asides, matched against a fixed list of drawable things; head shapes ("jar handles for a head") are not things; "leaf or diamond" alternatives and "Unknown" are dropped; number signs dropped. 261 of 498 signs get a picture; 38 different things. No word list from the repository was opened for this step.
2. Jobs (`lang_m_jobs.py` -> `jobs.csv`): roles from `gloss2.parse_face` over 6,862 faces (first catalogue + second-catalogue texts with no partner); counted signs split by the stroke series beside them (tall -> measure, short -> counted thing, stacked -> time). 149 pictured signs have a job: name 111, counted 14, measure 10, title 7, tag 3, crest 2, opener 2. The parser has no place slot, so no sign is a place word.
3. Dictionaries (`lang_m_lexicons.py` -> `work_data/lang_m/lex/`): DEDR cut into its Tamil, Malayalam, Kannada and Telugu parts (two words are different words only when they sit in different DEDR entries); Wiktionary Tamil, Telugu, Kannada, Akkadian and Proto-Indo-Iranian fetched from kaikki.org (2026-11-17, `work_data/lang_m/raw/`); the rest from `work_data/lexicons/tsv/`. Sizes (words / entries): DEDR Tamil 12,801 / 3,043; DEDR Malayalam 7,149 / 2,405; DEDR Kannada 10,342 / 2,651; DEDR Telugu 7,892 / 2,354; Wiktionary Tamil 10,240; Telugu 15,968; Kannada 2,391; Santali Campbell 11,104; Santali Bodding vol 5 1,830; Santali Wiktionary 774; Mundari Bhadra 4,875; Monier-Williams Sanskrit 187,327; Turner Old Indo-Aryan 7,079; Proto-Indo-Iranian 754; Sumerian Halloran 3,078; Sumerian Wiktionary 998; Akkadian 720; Elamite Hinz-Koch 2,460; Burushaski Lorimer 1,322. Not to be had as free word lists: Proto-Dravidian reconstructions (not in kaikki; DEDR prints none), full Bodding, Berger's Burushaski.
4. Score and controls (`lang_m_score.py` -> `grid.csv`, `evidence.csv` with every picture word / sound-alike pair, `signhits.csv`); keyword lists and rules in `lang_m_common.py`; tables by `lang_m_tables.py`.
5. One redesign, made after the first trial run and before any language comparison was read: the first version (any gloss mentioning the thing in its first 6 words, keyword anywhere in 12 words, every sign counted separately) hit 103 to 149 of 149 signs in both Tamil and Sanskrit with every control at the same level, so it had no power. The windows were tightened, signs grouped into units and the share score added, the same for every language.

## The full grid

The family score pools the family's dictionaries (a unit hits if it hits in any; shares pool the counts).

### Share score, every family, full grid

| family | distance | keywords | units with a picture word | share | control 1 (jobs dealt) mean / P | control 2 (outside nouns) mean / P | control 3 (sounds dealt) mean / P |
|---|---|---|---|---|---|---|---|
| Dravidian | strict | narrow | 63/63 | 0.61 | 0.54 / 0.136 | 0.39 / 0.05 | 0.63 / 0.512 |
| Dravidian | strict | wide | 63/63 | 1.82 | 1.74 / 0.286 | 1.51 / 0.155 | 1.84 / 0.463 |
| Dravidian | medium | narrow | 63/63 | 0.64 | 0.60 / 0.177 | 0.67 / 0.659 | 0.65 / 0.517 |
| Dravidian | medium | wide | 63/63 | 1.88 | 1.87 / 0.449 | 1.89 / 0.492 | 1.96 / 0.652 |
| Dravidian | loose | narrow | 63/63 | 0.69 | 0.70 / 0.526 | 0.67 / 0.06 | 0.64 / 0.005 |
| Dravidian | loose | wide | 63/63 | 1.99 | 2.00 / 0.745 | 1.98 / 0.424 | 2.00 / 0.622 |
| Munda | strict | narrow | 63/63 | 0.00 | 0.00 / 1 | 0.00 / 1 | 0.31 / 1 |
| Munda | strict | wide | 63/63 | 0.00 | 0.00 / 1 | 0.00 / 1 | 0.68 / 1 |
| Munda | medium | narrow | 63/63 | 0.46 | 0.46 / 0.476 | 0.39 / 0.245 | 0.57 / 0.716 |
| Munda | medium | wide | 63/63 | 1.68 | 1.86 / 0.789 | 1.51 / 0.237 | 1.90 / 0.771 |
| Munda | loose | narrow | 63/63 | 0.56 | 0.57 / 0.742 | 0.59 / 0.848 | 0.56 / 0.428 |
| Munda | loose | wide | 63/63 | 1.90 | 1.96 / 0.977 | 1.96 / 0.811 | 1.94 / 0.677 |
| Indo-Aryan | strict | narrow | 63/63 | 0.72 | 0.62 / 0.089 | 0.81 / 0.603 | 0.85 / 0.642 |
| Indo-Aryan | strict | wide | 63/63 | 1.81 | 1.75 / 0.338 | 2.02 / 0.666 | 1.86 / 0.517 |
| Indo-Aryan | medium | narrow | 63/63 | 0.72 | 0.74 / 0.654 | 0.79 / 0.799 | 0.84 / 0.95 |
| Indo-Aryan | medium | wide | 63/63 | 2.34 | 2.18 / 0.426 | 1.93 / 0.002 | 1.86 / 0.01 |
| Indo-Aryan | loose | narrow | 63/63 | 0.94 | 0.95 / 0.678 | 0.94 / 0.466 | 0.85 / 0.04 |
| Indo-Aryan | loose | wide | 63/63 | 2.09 | 2.12 / 0.904 | 2.12 / 0.827 | 1.88 / 0.015 |
| Sumerian | strict | narrow | 57/63 | 0.62 | 0.62 / 0.528 | 0.44 / 0.22 | 0.52 / 0.333 |
| Sumerian | strict | wide | 57/63 | 0.88 | 0.78 / 0.383 | 0.69 / 0.272 | 1.21 / 0.562 |
| Sumerian | medium | narrow | 57/63 | 1.01 | 1.00 / 0.473 | 1.18 / 0.653 | 1.15 / 0.627 |
| Sumerian | medium | wide | 57/63 | 3.03 | 2.86 / 0.25 | 3.24 / 0.567 | 2.76 / 0.234 |
| Sumerian | loose | narrow | 57/63 | 1.19 | 1.16 / 0.267 | 1.33 / 0.893 | 1.26 / 0.716 |
| Sumerian | loose | wide | 57/63 | 2.91 | 2.84 / 0.166 | 3.08 / 0.779 | 3.12 / 0.851 |
| Akkadian | strict | narrow | 50/63 | 0.00 | 0.00 / 1 | 0.00 / 1 | 0.38 / 1 |
| Akkadian | strict | wide | 50/63 | 0.00 | 0.07 / 1 | 0.00 / 1 | 1.28 / 1 |
| Akkadian | medium | narrow | 50/63 | 1.11 | 0.83 / 0.199 | 0.88 / 0.295 | 0.75 / 0.214 |
| Akkadian | medium | wide | 50/63 | 2.08 | 1.90 / 0.31 | 1.70 / 0.323 | 2.16 / 0.473 |
| Akkadian | loose | narrow | 50/63 | 0.97 | 0.92 / 0.283 | 1.13 / 0.723 | 0.95 / 0.418 |
| Akkadian | loose | wide | 50/63 | 2.82 | 2.62 / 0.17 | 2.72 / 0.411 | 2.66 / 0.289 |
| Elamite | strict | narrow | 21/63 | 0.00 | 0.00 / 1 | 0.00 / 1 | 0.00 / 1 |
| Elamite | strict | wide | 21/63 | 0.00 | 0.00 / 1 | 0.00 / 1 | 0.05 / 1 |
| Elamite | medium | narrow | 21/63 | 0.20 | 0.03 / 0.154 | 0.00 / 0.001 | 0.16 / 0.264 |
| Elamite | medium | wide | 21/63 | 0.20 | 0.04 / 0.21 | 0.01 / 0.032 | 0.48 / 0.597 |
| Elamite | loose | narrow | 21/63 | 0.29 | 0.25 / 0.149 | 0.16 / 0.106 | 0.21 / 0.139 |
| Elamite | loose | wide | 21/63 | 0.51 | 0.40 / 0.053 | 0.53 / 0.456 | 0.54 / 0.612 |
| Burushaski | strict | narrow | 41/63 | 0.00 | 0.00 / 1 | 0.00 / 1 | 0.00 / 1 |
| Burushaski | strict | wide | 41/63 | 0.00 | 0.00 / 1 | 0.00 / 1 | 0.00 / 1 |
| Burushaski | medium | narrow | 41/63 | 1.15 | 0.44 / 0.127 | 0.55 / 0.111 | 0.20 / 0.035 |
| Burushaski | medium | wide | 41/63 | 1.15 | 0.54 / 0.204 | 0.73 / 0.194 | 0.67 / 0.229 |
| Burushaski | loose | narrow | 41/63 | 0.30 | 0.28 / 0.332 | 0.37 / 0.622 | 0.29 / 0.388 |
| Burushaski | loose | wide | 41/63 | 0.97 | 0.90 / 0.165 | 1.16 / 0.555 | 0.85 / 0.269 |

### Hit count, every family, full grid

| family | distance | keywords | hits | control 1 mean (sd) / P | control 2 mean (sd) / P | control 3 mean (sd) / P |
|---|---|---|---|---|---|---|
| Dravidian | strict | narrow | 42 | 38.4 (1.9) / 0.044 | 20.0 (5.6) / 0.001 | 43.5 (3.6) / 0.716 |
| Dravidian | strict | wide | 50 | 48.7 (1.9) / 0.342 | 37.4 (5.1) / 0.003 | 50.8 (2.6) / 0.707 |
| Dravidian | medium | narrow | 59 | 58.6 (1.3) / 0.535 | 57.6 (2.4) / 0.379 | 58.4 (1.7) / 0.473 |
| Dravidian | medium | wide | 62 | 62.3 (0.5) / 0.979 | 62.5 (0.7) / 0.907 | 61.6 (1.0) / 0.607 |
| Dravidian | loose | narrow | 63 | 63.0 (0.0) / 1 | 63.0 (0.0) / 1 | 62.9 (0.3) / 0.93 |
| Dravidian | loose | wide | 63 | 63.0 (0.0) / 1 | 63.0 (0.0) / 1 | 63.0 (0.2) / 0.97 |
| Munda | strict | narrow | 0 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 | 0.5 (1.6) / 1 |
| Munda | strict | wide | 0 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 | 1.2 (2.4) / 1 |
| Munda | medium | narrow | 40 | 42.3 (2.1) / 0.901 | 21.8 (5.5) / 0.002 | 35.3 (4.2) / 0.154 |
| Munda | medium | wide | 49 | 51.0 (1.6) / 0.938 | 40.5 (4.8) / 0.042 | 48.8 (2.9) / 0.537 |
| Munda | loose | narrow | 62 | 62.1 (0.8) / 0.795 | 60.6 (2.1) / 0.413 | 61.5 (1.1) / 0.537 |
| Munda | loose | wide | 63 | 62.9 (0.4) / 0.864 | 62.0 (1.4) / 0.512 | 62.4 (0.7) / 0.522 |
| Indo-Aryan | strict | narrow | 28 | 26.1 (1.8) / 0.229 | 15.5 (4.7) / 0.009 | 31.4 (3.5) / 0.905 |
| Indo-Aryan | strict | wide | 40 | 39.1 (1.9) / 0.416 | 28.3 (5.2) / 0.013 | 40.9 (3.2) / 0.687 |
| Indo-Aryan | medium | narrow | 53 | 53.1 (1.8) / 0.637 | 52.6 (3.5) / 0.537 | 57.0 (1.9) / 0.98 |
| Indo-Aryan | medium | wide | 59 | 59.6 (1.3) / 0.802 | 59.0 (2.2) / 0.632 | 60.1 (1.2) / 0.895 |
| Indo-Aryan | loose | narrow | 63 | 63.0 (0.0) / 1 | 62.8 (0.5) / 0.879 | 62.5 (0.5) / 0.547 |
| Indo-Aryan | loose | wide | 63 | 63.0 (0.0) / 1 | 63.0 (0.0) / 1 | 62.6 (0.5) / 0.582 |
| Sumerian | strict | narrow | 2 | 1.6 (0.9) / 0.538 | 1.0 (1.6) / 0.201 | 5.0 (4.6) / 0.741 |
| Sumerian | strict | wide | 3 | 2.8 (0.9) / 0.648 | 2.3 (2.5) / 0.358 | 10.4 (5.7) / 0.91 |
| Sumerian | medium | narrow | 32 | 30.5 (1.9) / 0.313 | 25.5 (6.2) / 0.177 | 34.7 (3.5) / 0.811 |
| Sumerian | medium | wide | 41 | 40.0 (1.9) / 0.39 | 37.4 (6.1) / 0.327 | 43.1 (2.7) / 0.851 |
| Sumerian | loose | narrow | 51 | 51.4 (1.3) / 0.761 | 55.4 (4.1) / 0.88 | 53.5 (2.0) / 0.905 |
| Sumerian | loose | wide | 54 | 54.1 (0.3) / 1 | 57.0 (3.9) / 0.832 | 54.7 (1.9) / 0.746 |
| Akkadian | strict | narrow | 0 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 | 0.9 (2.1) / 1 |
| Akkadian | strict | wide | 0 | 0.1 (0.4) / 1 | 0.0 (0.0) / 1 | 2.6 (3.5) / 1 |
| Akkadian | medium | narrow | 10 | 7.5 (1.9) / 0.138 | 2.3 (2.3) / 0.028 | 9.5 (5.4) / 0.488 |
| Akkadian | medium | wide | 21 | 19.4 (1.7) / 0.261 | 5.2 (3.5) / 0.001 | 18.1 (4.8) / 0.323 |
| Akkadian | loose | narrow | 41 | 41.2 (1.4) / 0.691 | 33.7 (6.9) / 0.176 | 36.9 (3.5) / 0.174 |
| Akkadian | loose | wide | 44 | 43.7 (1.1) / 0.602 | 40.6 (6.7) / 0.365 | 42.2 (3.1) / 0.373 |
| Elamite | strict | narrow | 0 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 |
| Elamite | strict | wide | 0 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 | 0.1 (0.7) / 1 |
| Elamite | medium | narrow | 1 | 0.2 (0.4) / 0.154 | 0.0 (0.0) / 0.001 | 1.6 (2.4) / 0.567 |
| Elamite | medium | wide | 1 | 0.2 (0.4) / 0.21 | 0.1 (0.2) / 0.061 | 4.8 (4.8) / 0.776 |
| Elamite | loose | narrow | 15 | 15.5 (1.5) / 0.743 | 9.1 (5.4) / 0.155 | 15.4 (2.9) / 0.702 |
| Elamite | loose | wide | 18 | 17.5 (1.5) / 0.515 | 13.5 (6.6) / 0.248 | 19.0 (1.6) / 0.791 |
| Burushaski | strict | narrow | 0 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 |
| Burushaski | strict | wide | 0 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 |
| Burushaski | medium | narrow | 3 | 1.7 (1.1) / 0.23 | 2.0 (2.0) / 0.302 | 1.7 (3.0) / 0.169 |
| Burushaski | medium | wide | 3 | 2.5 (1.3) / 0.471 | 2.9 (2.5) / 0.469 | 4.7 (4.7) / 0.567 |
| Burushaski | loose | narrow | 28 | 27.0 (1.3) / 0.35 | 18.0 (6.1) / 0.074 | 22.9 (4.8) / 0.179 |
| Burushaski | loose | wide | 32 | 31.6 (1.2) / 0.537 | 27.5 (7.3) / 0.307 | 30.7 (3.9) / 0.428 |

### Every dictionary, share score (P against controls 1 / 2 / 3), cells: strict-narrow, strict-wide, medium-narrow, medium-wide, loose-narrow, loose-wide

| dictionary | words / entries | units covered | s-n | s-w | m-n | m-w | l-n | l-w |
|---|---|---|---|---|---|---|---|---|
| dedr_tamil | 12801 / 3043 | 60 | 0.67 (0.005/0.026/0.343) | 3.19 (0.134/0.001/0.005) | 0.54 (0.384/0.549/0.905) | 1.50 (0.606/0.629/0.95) | 0.61 (0.572/0.834/0.826) | 1.63 (0.615/0.909/1) |
| dedr_malayalam | 7149 / 2405 | 54 | 0.86 (0.701/0.024/0.095) | 2.64 (0.466/0.072/0.005) | 0.87 (0.266/0.372/0.005) | 1.89 (0.346/0.674/0.01) | 0.64 (0.352/0.899/0.005) | 1.59 (0.25/0.971/0.005) |
| dedr_kannada | 10342 / 2651 | 61 | 0.46 (0.135/0.268/0.333) | 2.42 (0.292/0.253/0.045) | 0.64 (0.654/0.21/0.075) | 2.01 (0.75/0.115/0.015) | 0.61 (0.554/0.017/0.005) | 1.74 (0.903/0.122/0.005) |
| dedr_telugu | 7892 / 2354 | 59 | 0.58 (0.226/0.107/0.378) | 1.17 (0.084/0.13/0.647) | 0.64 (0.367/0.667/0.343) | 1.85 (0.396/0.619/0.209) | 0.65 (0.824/0.239/0.134) | 2.03 (0.333/0.028/0.01) |
| tamil_wiktionary | 10240 / 10240 | 63 | 0.40 (0.392/0.479/0.453) | 0.59 (0.685/0.77/0.846) | 0.83 (0.194/0.206/0.055) | 2.65 (0.09/0.315/0.015) | 0.65 (0.25/0.406/0.224) | 2.08 (0.414/0.712/0.07) |
| telugu_wiktionary | 15968 / 15968 | 63 | 0.91 (0.199/0.153/0.239) | 0.95 (0.153/0.706/0.985) | 0.85 (0.101/0.545/0.279) | 2.32 (0.326/0.947/0.985) | 0.85 (0.213/0.545/0.298) | 3.00 (0.601/0.662/1) |
| kannada_wiktionary | 2391 / 2391 | 55 | 0.00 (1/1/1) | 0.00 (1/1/1) | 0.79 (0.42/0.381/0.194) | 2.64 (0.277/0.227/0.05) | 0.99 (0.155/0.017/0.02) | 2.27 (0.5/0.006/0.035) |
| santali_campbell | 11104 / 11104 | 61 | 0.00 (1/1/1) | 0.00 (1/1/1) | 0.40 (0.915/0.352/0.642) | 2.04 (0.567/0.034/0.174) | 0.55 (0.74/0.787/0.244) | 1.92 (0.977/0.773/0.343) |
| santali_bodding5 | 1830 / 1830 | 54 | 0.00 (1/1/1) | 0.00 (1/1/1) | 0.06 (0.253/0.556/0.567) | 0.26 (0.05/0.926/0.816) | 0.35 (0.839/0.113/0.353) | 1.12 (0.481/0.103/0.716) |
| santali_wiktionary | 774 / 774 | 52 | 0.00 (1/1/1) | 0.00 (1/1/1) | 0.83 (0.29/0.001/0.129) | 1.12 (0.34/0.102/0.378) | 0.39 (0.268/0.318/0.348) | 1.25 (0.271/0.147/0.458) |
| mundari_bhadra | 4875 / 4875 | 62 | 0.00 (1/1/1) | 0.00 (1/1/1) | 0.65 (0.098/0.086/0.358) | 1.70 (0.368/0.116/0.522) | 0.54 (0.632/0.606/0.895) | 1.69 (0.787/0.294/0.965) |
| sanskrit_mw | 187327 / 187327 | 63 | 0.73 (0.089/0.502/0.617) | 1.82 (0.332/0.554/0.507) | 0.73 (0.597/0.683/0.925) | 2.36 (0.386/0.003/0.01) | 0.94 (0.636/0.519/0.04) | 2.08 (0.862/0.864/0.015) |
| oia_turner | 7079 / 7079 | 62 | 0.00 (1/1/1) | 0.50 (0.812/0.883/0.582) | 1.47 (0.554/0.315/0.065) | 2.23 (0.72/0.591/0.298) | 0.80 (0.692/0.073/0.075) | 2.23 (0.943/0.15/0.065) |
| proto_indoiranian_wiktionary | 754 / 754 | 52 | 0.00 (1/1/1) | 0.00 (1/1/1) | 1.00 (0.287/0.254/0.209) | 2.25 (0.325/0.059/0.189) | 1.27 (0.432/0.427/0.373) | 2.45 (0.874/0.3/0.463) |
| sumerian_halloran | 3078 / 3078 | 55 | 0.00 (1/1/1) | 0.00 (1/1/1) | 1.13 (0.541/0.582/0.597) | 4.73 (0.148/0.044/0.01) | 1.23 (0.473/0.744/0.731) | 3.08 (0.316/0.506/0.811) |
| sumerian_wiktionary | 998 / 998 | 45 | 0.62 (0.528/0.22/0.333) | 0.88 (0.383/0.272/0.562) | 0.48 (0.342/0.733/0.776) | 1.40 (0.152/0.737/0.552) | 0.65 (0.225/0.79/0.731) | 1.82 (0.092/0.33/0.149) |
| akkadian_wiktionary | 720 / 720 | 50 | 0.00 (1/1/1) | 0.00 (1/1/1) | 1.11 (0.199/0.295/0.214) | 2.08 (0.31/0.323/0.473) | 0.97 (0.283/0.723/0.418) | 2.82 (0.17/0.411/0.289) |
| elamite_hinzkoch | 2460 / 2460 | 21 | 0.00 (1/1/1) | 0.00 (1/1/1) | 0.20 (0.154/0.001/0.264) | 0.20 (0.21/0.032/0.597) | 0.29 (0.149/0.106/0.139) | 0.51 (0.053/0.456/0.612) |
| burushaski_lorimer | 1322 / 1322 | 41 | 0.00 (1/1/1) | 0.00 (1/1/1) | 1.15 (0.127/0.111/0.035) | 1.15 (0.204/0.194/0.229) | 0.30 (0.332/0.622/0.388) | 0.97 (0.165/0.555/0.269) |

### Swap pairs (65 pairs of differently drawn things), sound-alike picture names

| family | distance | sound-alike pairs | random pairs mean (sd) / P | pictures dealt mean (sd) / P |
|---|---|---|---|---|
| Dravidian | strict | 16 | 19.8 (3.73) / 0.879 | 17.14 (4.3) / 0.644 |
| Dravidian | medium | 58 | 52.91 (3.16) / 0.066 | 56.67 (3.42) / 0.443 |
| Dravidian | loose | 63 | 63.55 (1.2) / 0.823 | 64.47 (0.76) / 0.978 |
| Munda | strict | 0 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 |
| Munda | medium | 21 | 13.26 (3.12) / 0.014 | 12.68 (3.81) / 0.028 |
| Munda | loose | 57 | 51.32 (3.36) / 0.056 | 55.44 (3.86) / 0.434 |
| Indo-Aryan | strict | 3 | 7.41 (2.59) / 0.981 | 2.89 (1.9) / 0.531 |
| Indo-Aryan | medium | 35 | 33.14 (4.03) / 0.362 | 30.68 (5.36) / 0.232 |
| Indo-Aryan | loose | 60 | 60.15 (2.09) / 0.638 | 61.3 (2.2) / 0.809 |
| Sumerian | strict | 0 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 |
| Sumerian | medium | 11 | 7.94 (2.58) / 0.164 | 10.93 (3.31) / 0.544 |
| Sumerian | loose | 50 | 36.09 (4.0) / 0.001 | 43.08 (5.49) / 0.106 |
| Akkadian | strict | 0 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 |
| Akkadian | medium | 1 | 1.03 (1.0) / 0.654 | 1.6 (1.37) / 0.779 |
| Akkadian | loose | 17 | 18.19 (3.6) / 0.669 | 16.36 (4.65) / 0.467 |
| Elamite | strict | 0 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 |
| Elamite | medium | 0 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 |
| Elamite | loose | 0 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 |
| Burushaski | strict | 0 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 |
| Burushaski | medium | 0 | 0.0 (0.0) / 1 | 0.0 (0.0) / 1 |
| Burushaski | loose | 6 | 9.72 (2.82) / 0.946 | 7.71 (3.01) / 0.755 |

Listed swap pairs from `sound_list_v6.md` as found by the frame rule: 220/231 swap in 6 frames, 705/706 in 6; 904/905, 407/408 and 423/424 in 1 each (below the 2-frame cut); the other 421-424 pairs in none. All pairs: `work_data/lang_m/swap_pairs.csv` (291 pairs in 2+ frames; 25 of the pictured ones are the same thing drawn two ways and were left out as drawing variants). Script: `work_scripts/lang_m_swaps.py`.

## Candidates

None listed: no language shows a clear excess, so per the brief no sign is put forward. The pairs the machine finds are all in `work_data/lang_m/evidence.csv` (for Tamil they include the earlier *mīṉ* fish ~ *mīṉ* star and *vēl* spear ~ *vēḷ* chief), with the control saying as many would turn up with sounds dealt at random.

## Limits

- Pictures: 261 of 498 signs; the rule depends on the words of the shape descriptions. Signs drawn as something the describer did not name (comb, cup, the A-comb) are missing.
- Jobs are lopsided: 35 of 63 units are "name", which leaves control 1 little to shuffle and dilutes any job-specific effect. The name slot has measured inner parts (crest, self, tag) that most pictured signs are not assigned to.
- Flat word lists merge words spelled alike into one entry, so at the strict distance a homophone can only be found where the printed spellings differ; 11 of 19 dictionaries score 0 at strict-narrow for that reason, not for lack of puns. DEDR keeps homonyms apart, which is why it is the one source with strict hits in quantity.
- OCR noise in the Santali, Mundari, Sumerian (Halloran) and Elamite lists; Elamite has a picture word for only 21 of 63 units and Burushaski for 41.
- With 312 cells, about 16 would pass any one control at P below 0.05 by luck. 16 cells pass two of three (14 of them controls 2 and 3, which both look at the real picture words' sound neighbourhood and so are not independent of each other); none passes all three.
- What would be needed for power: pictures for the 194 undescribed-as-thing signs, a job split finer than "name", homonym-aware dictionaries for Munda, Indo-Aryan and Sumerian (Bodding vols 1-6, ePSD2, Turner's full CDIAL with homonym numbers), and Proto-Dravidian reconstructions.
