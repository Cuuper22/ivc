# Decoy test: do predictions about outside facts tell a right word from a wrong one?

You need no background beyond this page. Read it all, then do the task.

## What this is
The Indus (Harappan) script is undeciphered. A project proposes an early Dravidian word for about 150 signs. This list has 60 signs, each with a proposed word (columns `sound`, `english`, `dedr` in `test_list.csv`; `dedr` is a dictionary entry number, often blank). Some of the 60 words are the project's proposal and some are wrong on purpose: a word taken from a different sign that does the same kind of job in the texts. You are not told which. Some words on the list may well be wrong. Your job is only to report what each test shows.

## The corpus and the loader
- Lipi catalogue: about 4,000 faces (inscribed sides) on seals, tags, pots, tools, copper tablets and moulded tablets, each a sequence of sign numbers in reading order, with object kind, site, findspot, picture code and time bin.
- Second catalogue (Mahadevan): its texts with no Lipi partner are the NEW TEXTS (about 1,180). Use them as the held-out check.
- Loader to use: `work_scripts/decoy_loader.py`. Run `import sys; sys.path.insert(0, '/home/claude/ivc/work_scripts'); from decoy_loader import *`. It prints two loading lines and exposes only corpus facts (checked: it does not import any word list). Do not import any other file from `work_scripts`.
- What gives what:
  - faces: `d.tok` (one tuple of sign numbers per face), `faces_all('L')`; each sign is a 3-digit string such as `'220'`.
  - object kind: `d.kind` / `objs.kind` (seal, tag, pot, tool, bangle, rod, ctab, mtab, other); `on_kind(sign, kinds, cat)`, `off_kind`.
  - counts beside a sign: `counts_beside(sign)`, `count_series(sign, 'tall' or 'short')` (stroke style of the counts next to it), `with_count`, `prev_count`, `next_count`; `VAL` = number signs, `SHORT` / `TALL` = stroke styles.
  - picture on the other side or on the seal: `objs.pic` (picture label, plain words in `PIC_EN`), `pic_share(sign, labels)`, `animal_share`, `reverse_has(sign, signs)`.
  - findspot: `objs.site`, `objs.area`, `objs.bh` (block-house), `moh.house`, `site_share`, `harappa_area`, `moh_area`, `house_share`.
  - time bin: `objs.bin` (early / middle / late or blank), `time_share(sign, bin)`.
  - new texts: `faces_all('Mu')`, `kfaces('Mu')`; most primitives take `cat='Mu'`. `cat='L'` is Lipi, `'LM'` is both.
  - which goods or person signs share a face: `cooccur(sign, signs)`, `adjacent`, `profile(sign)`.
  - the shuffle test: `strat_shuffle_p(has, outcome, strata)` (see below).
  Primitives that use a plain binomial base rate are fine for exploring, but the verdict in this test is the shuffle test below.

## The rule (follow it in this order)
1. FIRST write one script file, for example `work_data/decoy/predictions.py`, containing for ALL 60 items, before computing anything about any of them: ONE prediction that follows from the WORD'S MEANING (the `english` and `sound` on the list, taken at face value) about a fact outside the sign's own slot. The fact must be one of: the object kind it sits on, the picture on the other side, the stroke style of counts beside it, findspot inside a city, which goods or person signs share its face, behaviour on the new texts. Write, per item: the prediction in one line, the base rate it must beat (the share among all comparable objects or faces), and the threshold fixed in advance. Do not change this file after you start computing. Do not choose a prediction because you already know how the sign behaves; choose it from the meaning alone.
2. Threshold: a prediction CAME TRUE if the direction is right AND P is below 0.05 against a shuffle within site and object kind (shuffle the sign's labels among objects of the same site and object kind, at least 5,000 shuffles, seeded; `strat_shuffle_p` does this). RIGHT DIRECTION ONLY: the direction is right but P is 0.05 or more. AGAINST: the direction is the opposite of the prediction. If there are fewer than 3 cases, write `too few` in outcome.
3. Then run all 60 and record the outcome for each. Same procedure for every item. Report what the test shows even if it looks odd.
4. Write results to `work_data/decoy/results.csv` with columns: `item, sign, prediction in one line, base rate, observed, P, outcome` (outcome is one of `came true`, `right direction only`, `against`, `too few`). Keep the header text `item,sign,prediction,base_rate,observed,P,outcome`.

## What you must NOT open
These show which words are the project's accepted ones and would spoil the test:
`work_data/values_master*.csv`, anything in `jobs/out/`, `MAP.md`, `READINGS.md`, `CORPUS.md`, `WHOSWHO.md`, `work_data/decoy/KEY_do_not_open.csv`, `work_scripts/decoy_build.py`, `work_scripts/decoy_score.py`, and every `sound_v*`, `blind*`, `corpus*` script other than `decoy_loader.py`. Also do not read `work_data/sound_v*`, `work_data/blind*`, `work_data/corpus_english*.csv`, `work_data/gloss*` or `work_data/early/`. If you open one by accident, say so in your results file header.

Print live progress as you run (item number, sign, outcome).
