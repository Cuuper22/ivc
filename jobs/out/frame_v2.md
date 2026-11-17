# Frame v2: the grammar of the Indus texts, written out, scored against decoys

Scripts (in `work_scripts/`, run in this order): `frame2_common.py` (the v2 classes, the kind grammar, the strict patterns: all written before any v2 score), `frame2_build.py` (held-out push), `frame2_score.py` (side-by-side scoring with decoys), `frame2_kind_redesign.py` (one redesign of the kind grammar), `frame2_phrases.py` (fixed phrases), `frame2_seals.py` (the two kinds of seal), `frame2_corpus.py` and `frame2_book.py` (corpus in jobs, `FRAMEBOOK.md`), `frame2_photos.py` (photo draw), `frame2_pictures.py` (picture-words). Tables and logs: `work_data/frame/` (files named below). No words for signs anywhere: sign numbers, pictures and jobs only. Date 2026-11-17.

## What was found

1. **A 14-class written grammar now holds a third of the script's order, as much as the best machine, and beats every decoy.** Frame v2 is the hand frame plus the machine's three changes (ending split into closer and after-jar title; a slot class after the front word; numbers split into short, tall and the tall two that lives in fish names) and its two adoptions (fish signs as name fronts; trees as counted things). On the 482 new texts (never used to build anything) it costs 7.536 bits per sign against 7.849 for sign frequencies alone; its 20 decoys (the same 14 jobs dealt to the wrong signs of the same frequency) cost 7.790 on average and 7.671 at best: 0 of 20 reach it. Share of the sign-pair model's knowledge captured: **v2 32.7%** against hand v1 19.6%, machine HMM classes 28.5%, machine exchange classes 33.1%, v2 decoys 6.1%. What it means: the order the machine finds is now written down as explicit rules a person can read, and it carries over to texts no rule was built on. What it opens: v2 mixed half-and-half with the sign-pair model (6.881 bits) is the first frame mix that beats the sign-pair model alone on new texts (6.892); v1's mix did not (6.918).
2. **Pushed on the held-out half, v2 reaches 48% of the order.** Adding classes only when they lower bits on a held-out half of the first catalogue (fit on half A, score on half B; new texts never touched) took v2 from 14 to 54 classes, held-out half B from 6.153 to 5.749 bits per sign (v1 6.351, HMM 6.033). On the new texts the pushed v2 costs 7.386 bits: **48.3% of the sign-pair model's knowledge**. Almost every added class is one frequent sign given its own row (jar 740, box 590, fish 220, pitchfork 415 first): the remaining order belongs to particular signs, not to more jobs. Its decoys are strong for the same reason (mean 7.567, best 7.349, 1 of 20 beats it): a singleton class is a singleton whichever frequent sign it holds.
3. **v2 fills lost signs best of any frame.** On the 77 fill-the-gap texts the true sign is in v2's top 5 for 50.6% (pushed v2 58.4%), against v1 44.2%, HMM 41.6%, exchange 42.9%, frequency 27.3%; v2 decoys 36.0% (best 41.6%), pushed-v2 decoys 46.7% (best 55.8%): 0 of 20 decoys reach either. Mixed with the sign-pair model: top 10 74.0% (sign pairs alone 68.8%), and the pushed-by-kind mix puts the true sign first 39.0% of the time (sign pairs alone 24.7%, decoy mixes 29.6%).
4. **The strict written patterns fit more texts than v1, and dealt to the wrong signs they fit almost nothing.** First catalogue, share of distinct clean texts that fit a v2 pattern (v1 pattern in brackets; v2 decoy mean after): seals 43% (40%; 7%), tags 50% (45%; 8%), tablets 56% (46%; 7%), copper tablets 54% (34%; 23%), pots 27% (16%; 9%). New texts: seals 29% (26%; 7%), tags and sealings 33% (31%; 8%), tablets 24% (22%; 15%), copper tablets 45% (14%; 22%), pots 29% (22%; 14%). The record pattern (name, closer, then a count line) lifts copper tablets from 14% to 45% on new texts.
5. **The rest of the order lives in a few hundred fixed phrases.** On the new texts, the sign-pair model saves 934 bits over v2 inside texts; the 40 fixed pairs listed below carry 41% of that and the top 200 pairs carry 92%. The 40 fixed pairs occur 151 times in the new texts in their own order and 6 times reversed; of 172 text-pair cases where both signs are present, 151 are the adjacent pair in that order. On the first catalogue with sign order shuffled inside each text (20 shuffles), on average 1.0 pair (max 3) reaches the gain of the real 40th pair.
6. **The count-line seal is a quantity stamp whose impressions turn up on goods.** 75 undamaged seals carry a count line and nothing else: 32 as `[front word][slot][number][counted thing]`, 43 as a bare `[number][counted thing]`. The counted thing is a tree sign (390 on 41, 405 and 407 on 6 each) or the porter with jars 156 (16), the number mostly three short strokes (32), then four (13) and six stacked (12). With the jobs dealt to wrong signs, this seal kind nearly vanishes (mean 1.0 seal across 20 decoys, max 10). The text of a count-line seal is found on a clay sealing or tag **22.7% of the time (17 of 75) against 5.7% for name seals** (Fisher P 8.5e-6); 2,000 draws of non-count-line seals with the same text-length mix give 7.0% on average and none reach 22.7%. In every other measured respect (size once length is matched, animal, findspot, time, abroad) it is an ordinary seal.

Terms:
- **Bits per sign**: how many yes/no questions a model needs, on average, to guess each next sign of a text it never saw (the end of the text counted as one more symbol). Lower = the model knows more about order.
- **Sign-pair model (sign bigram)**: guesses each sign from the sign right before it. **Unigram**: from sign frequency alone.
- **Share captured** = (unigram bits − frame bits) / (unigram bits − sign-pair bits): how much of what the sign-pair table knows about order the frame's classes know.
- **Class grammar**: guesses the next sign's class from the previous sign's class, then the sign inside its class. **Pooled**: one table for all objects. **By kind**: one table per object kind (seals, tags and sealings, tablets, copper tablets, pots), backed off to the pooled table.
- **Decoy**: the frame's class labels dealt among signs of the same frequency band (10 bands, 20 deals, seeds 500-519), scored identically.
- **New texts**: 482 second-catalogue (Mahadevan 1977) lines with no partner in the first catalogue, complete, every sign seen in training.
- **Fill-the-gap**: 77 texts where one catalogue lost a sign that the other catalogue has; training leaves those faces out.
- **Strict pattern**: a regular expression over the class string, one per text type, written in `frame2_common.py` before scoring.
- **Gain** of a pair: the bits the sign-pair model saves over the v2 grammar on that pair across the corpus: n × log2(P_pairs(b|a) / P_v2(b|a)).

## 1. Frame v2, the grammar

Classes (`frame2_common.py`; per-sign table `work_data/frame/classes_v2.csv`):

| class | plain job | signs (commonest) |
|---|---|---|
| OPEN | front word | 820 861 817 920 550 692 824 091 880 360 556 545 |
| SLOT | after-front slot | 002 060 741 368 742 365 |
| CREST | name front | 220 240 235 233 803 140 806 231 226 222 243 |
| PERSONAL | name part | 590 798 415 176 255 840 706 575 142 617 ... (the rest) |
| NUM_NAME | tall two (in names) | 032 |
| NUM_SHORT | short number | 001 003 004 017 005 016 013 and the comb counts |
| NUM_TALL | tall number | 033 031 034 035 036 |
| MEASURE | measure | 705 480 171 408 ... |
| AFTER_M | after-measure | 760 690 585 752 |
| THING | counted thing | 390 700 405 407 156 406 426 ... |
| NAME_BACK | name back | 100 482 |
| PLACE | place or time word | 900 061 904 503 615 335 165 845 ... |
| CLOSER | closer | 740 520 151 154 158 155 |
| TITLE | after-jar title | 400 090 527 621 679 565 161 241 |

Grammar in plain words: an optional front word with its slot; then either a name (crest, name parts, optional name back) shut by a closer with an optional after-jar title, or a count line (numbers then a counted thing); a measure takes its follower; a record is a name text followed by a count line. Which class follows which is learned per object kind (`class_model_kind`).

Push (`v2_push_steps.csv`): 54 moves accepted, 40 classes added, held-out half B 6.153 → 5.749 bits per sign. First ten moves: 740, 590, 220, 415, 435, 255, 001, 176, 798, 840 each became its own class; later groups formed: {001, 031, 140, 845, 850, 595}, {176, 904, 388}, {706, 705}, {920, 692}, {390, 405}, {002, 742}, {503, 495, 104}.

### Side by side on the 482 new texts (`v2_bits.csv`, `v2_decoys.csv`)

| frame | classes | bits/sign | share | decoy mean | best decoy | decoys at or below | mix with sign pairs |
|---|---|---|---|---|---|---|---|
| unigram | | 7.849 | 0% | | | | |
| sign pairs | | 6.892 | 100% | | | | |
| v1 hand jobs | 10 | 7.661 | 19.6% | 7.824 | 7.739 | 0 | 6.918 |
| machine HMM10 | 10 | 7.576 | 28.5% | 7.804 | 7.714 | 0 | 6.937 |
| machine exchange10 | 10 | 7.532 | 33.1% | 7.811 | 7.744 | 0 | 6.911 |
| **v2 base** | 14 | **7.536** | **32.7%** | 7.790 | 7.671 | 0 | **6.881** |
| v2 pushed | 54 | 7.386 | 48.3% | 7.567 | 7.349 | 1 | 6.932 |

### Fill-the-gap, 77 texts (`v2_gap.csv`): true sign in top 1 / 5 / 10

| frame (pooled) | alone | decoy mean | mixed with sign pairs | decoy mixes |
|---|---|---|---|---|
| frequency only | 15.6 / 27.3 / 35.1 | | | |
| sign pairs | 24.7 / 59.7 / 68.8 | | | |
| v1 hand jobs | 23.4 / 44.2 / 59.7 | 17.0 / 32.9 / 42.0 | 32.5 / 57.1 / 70.1 | 30.0 / 55.9 |
| machine HMM10 | 28.6 / 41.6 / 48.1 | 19.0 / 33.8 / 43.4 | 31.2 / 55.8 / 66.2 | 29.6 / 57.4 |
| machine exchange10 | 32.5 / 42.9 / 50.6 | 17.7 / 33.4 / 44.0 | 31.2 / 55.8 / 64.9 | 29.5 / 56.8 |
| v2 base | 32.5 / 50.6 / 59.7 | 20.2 / 36.0 / 45.5 | 32.5 / 59.7 / 74.0 | 30.1 / 56.4 |
| v2 pushed | 33.8 / 58.4 / 70.1 | 24.5 / 46.7 / 58.4 | 33.8 / 62.3 / 72.7 | 28.2 / 57.1 |

(v1 alone reads 23.4% top 1 here against 18.2% in `frame_machine.md` because this run leaves out only the faces of the 77 main items from training, the earlier run also those of the 157-item wider set.)

### Strict patterns by object kind (`v2_coverage.csv`): share of texts fitting, real (decoy mean)

| kind | v1, first cat. | v2, first cat. | v1, new texts | v2, new texts |
|---|---|---|---|---|
| seals | 40% (6%) | 43% (7%) | 26% (6%) | 29% (7%) |
| tags and sealings | 45% (8%) | 50% (8%) | 31% (6%) | 33% (8%) |
| tablets | 46% (6%) | 56% (7%) | 22% (9%) | 24% (15%) |
| copper tablets | 34% (7%) | 54% (23%) | 14% (5%) | 45% (22%) |
| pots | 16% (7%) | 27% (9%) | 22% (8%) | 29% (14%) |

## 2. The fixed phrases (`fixed_pairs.csv`, `fixed_triples.csv`, `fixed_pairs_decoy.csv`)

The 40 sign pairs that carry the most order no v2 class explains. n = distinct first-catalogue texts; P(b|a) = how often b follows a; v2 = what the class grammar expects; new = count in the 482 new texts.

| pair | pictures | classes | n | gain (bits) | P(b|a) | v2 | new |
|---|---|---|---|---|---|---|---|
| 255-435 | [odd animal] [stroke with diagonal] | PERSONAL > PERSONAL | 42 | 285 | 0.38 | 0.003 | 7 |
| 415-220 | [pitchfork] [fish] | PERSONAL > CREST | 52 | 247 | 0.39 | 0.014 | 4 |
| 590-390 | [box with bar] [tree] | PERSONAL > THING | 58 | 218 | 0.31 | 0.023 | 6 |
| 435-690 | [stroke with diagonal] [nested chevrons] | PERSONAL > AFTER_M | 30 | 167 | 0.45 | 0.009 | 4 |
| 706-033 | [U with stroke variant] [three tall strokes] | PERSONAL > NUM_TALL | 35 | 164 | 0.37 | 0.014 | 0 |
| 415-100 | [pitchfork] [three-headed person] | PERSONAL > NAME_BACK | 36 | 151 | 0.27 | 0.015 | 3 |
| 033-520 | [three tall strokes] [spear] | NUM_TALL > CLOSER | 48 | 144 | 0.17 | 0.021 | 4 |
| 861-002 | [diamond] [two strokes] | OPEN > SLOT | 145 | 139 | 0.69 | 0.353 | 22 |
| 060-741 | [short-tall stroke pair] [jar with mark] | SLOT > SLOT | 36 | 138 | 0.14 | 0.010 | 3 |
| 555-527 | [pincers variant] [hatched box] | PERSONAL > TITLE | 18 | 136 | 0.72 | 0.004 | 2 |
| 840-032 | [two leaves] [two tall strokes] | PERSONAL > NUM_NAME | 31 | 127 | 0.28 | 0.017 | 4 |
| 550-527 | [pincers] [hatched box] | OPEN > TITLE | 21 | 126 | 0.18 | 0.003 | 0 |
| 920-060 | [bracket with leaf] [short-tall stroke pair] | OPEN > SLOT | 63 | 121 | 0.39 | 0.102 | 6 |
| 176-740 | [sitting person with ticks] [jar] | PERSONAL > CLOSER | 65 | 120 | 0.50 | 0.139 | 8 |
| 817-002 | [diamond variant] [two strokes] | OPEN > SLOT | 123 | 118 | 0.69 | 0.353 | 0 |
| 220-520 | [fish] [spear] | CREST > CLOSER | 43 | 99 | 0.11 | 0.023 | 6 |
| 142-617 | [person with staff] [sign 617] | PERSONAL > PERSONAL | 16 | 96 | 0.22 | 0.004 | 0 |
| 032-220 | [two tall strokes] [fish] | NUM_NAME > CREST | 64 | 89 | 0.16 | 0.062 | 1 |
| 017-585 | [seven stacked strokes] [sign 585] | NUM_SHORT > AFTER_M | 19 | 89 | 0.24 | 0.009 | 0 |
| 705-033 | [U with stroke] [three tall strokes] | MEASURE > NUM_TALL | 77 | 82 | 0.41 | 0.196 | 10 |
| 692-060 | [outlined X] [short-tall stroke pair] | OPEN > SLOT | 38 | 82 | 0.46 | 0.102 | 9 |
| 017-575 | [seven stacked strokes] [trapezoid with box] | NUM_SHORT > PERSONAL | 14 | 79 | 0.17 | 0.003 | 0 |
| 798-415 | [leaf with pincers] [pitchfork] | PERSONAL > PERSONAL | 19 | 79 | 0.14 | 0.008 | 2 |
| 235-240 | [capped fish] [whiskered fish] | CREST > CREST | 36 | 77 | 0.16 | 0.036 | 2 |
| 806-154 | [leaf on tree variant] [porter with jars] | CREST > CLOSER | 15 | 75 | 0.13 | 0.004 | 0 |
| 923-740 | [outlined bracket] [jar] | PERSONAL > CLOSER | 29 | 75 | 0.84 | 0.139 | 1 |
| 320-920 | [sign 320] [bracket with leaf] | PERSONAL > OPEN | 11 | 74 | 0.55 | 0.005 | 3 |
| 590-405 | [box with bar] [tree variant 405] | PERSONAL > THING | 19 | 72 | 0.10 | 0.008 | 5 |
| 171-035 | [T with leaf] [five tall strokes] | MEASURE > NUM_TALL | 12 | 56 | 0.52 | 0.021 | 1 |
| 806-158 | [leaf on tree variant] [porter with jars 158] | CREST > CLOSER | 11 | 54 | 0.09 | 0.003 | 4 |
| 740-090 | [jar] [man] | CLOSER > TITLE | 84 | 53 | 0.08 | 0.050 | 9 |
| 845-407 | [two hatched leaves] [tree variant 407] | PLACE > THING | 10 | 52 | 0.36 | 0.010 | 0 |
| 798-740 | [leaf with pincers] [jar] | PERSONAL > CLOSER | 42 | 50 | 0.32 | 0.139 | 5 |
| 760-740 | [branched U] [jar] | AFTER_M > CLOSER | 95 | 49 | 0.87 | 0.609 | 15 |
| 467-806 | [A with comb] [leaf on tree variant] | NUM_SHORT > CREST | 8 | 48 | 0.73 | 0.012 | 0 |
| 550-525 | [pincers] [sign 525] | OPEN > PERSONAL | 6 | 47 | 0.05 | 0.000 | 0 |
| 820-001 | [wheel] [one stroke] | OPEN > NUM_SHORT | 19 | 47 | 0.08 | 0.015 | 3 |
| 798-240 | [leaf with pincers] [whiskered fish] | PERSONAL > CREST | 14 | 47 | 0.10 | 0.010 | 0 |
| 013-840 | [three stacked strokes] [two leaves] | NUM_SHORT > PERSONAL | 9 | 46 | 0.16 | 0.005 | 2 |
| 904-832 | [double bracket] [leaf with stroke] | PLACE > PERSONAL | 8 | 45 | 0.12 | 0.003 | 0 |

The 40 strongest fixed triples (gain over the class grammar; "beyond pairs" = bits the third sign saves over the pair model, i.e. how much the triple is a unit of its own):

| triple | pictures | n | gain | beyond pairs | new |
|---|---|---|---|---|---|
| 255-435-690 | [odd animal] [stroke with diagonal] [nested chevrons] | 27 | 351 | 14 | 4 |
| 920-060-741 | [bracket with leaf] [short-tall stroke pair] [jar with mark] | 36 | 290 | 73 | 3 |
| 590-390-740 | [box with bar] [tree] [jar] | 39 | 240 | 69 | 5 |
| 435-690-740 | [stroke with diagonal] [nested chevrons] [jar] | 27 | 173 | 24 | 3 |
| 840-032-740 | [two leaves] [two tall strokes] [jar] | 24 | 168 | 62 | 2 |
| 705-033-520 | [U with stroke] [three tall strokes] [spear] | 29 | 157 | 33 | 4 |
| 798-415-220 | [leaf with pincers] [pitchfork] [fish] | 15 | 150 | 15 | 2 |
| 706-033-520 | [U with stroke variant] [three tall strokes] [spear] | 15 | 139 | 20 | 0 |
| 017-575-740 | [seven stacked strokes] [trapezoid with box] [jar] | 14 | 124 | 31 | 0 |
| 415-100-740 | [pitchfork] [three-headed person] [jar] | 27 | 122 | -3 | 3 |
| 413-575-335 | [ear with crossbars] [trapezoid with box] [joined M] | 7 | 109 | 26 | 1 |
| 590-405-740 | [box with bar] [tree variant 405] [jar] | 16 | 104 | 28 | 4 |
| 415-220-520 | [pitchfork] [fish] [spear] | 12 | 98 | 12 | 0 |
| 002-032-220 | [two strokes] [two tall strokes] [fish] | 27 | 92 | 49 | 0 |
| 575-335-711 | [trapezoid with box] [joined M] [u with x going 711] | 5 | 84 | 10 | 0 |
| 920-060-742 | [bracket with leaf] [short-tall stroke pair] [jar variant] | 9 | 73 | 17 | 1 |
| 233-705-033 | [barred fish] [U with stroke] [three tall strokes] | 17 | 72 | 20 | 2 |
| 001-142-617 | [one stroke] [person with staff] [sign 617] | 6 | 69 | 10 | 0 |
| 017-585-740 | [seven stacked strokes] [sign 585] [jar] | 13 | 67 | 5 | 0 |
| 320-920-740 | [sign 320] [bracket with leaf] [jar] | 6 | 67 | 16 | 2 |
| 832-255-070 | [leaf with stroke] [odd animal] [stroke with arms] | 5 | 65 | 20 | 0 |
| 468-806-154 | [A with comb] [leaf on tree variant] [porter with jars] | 4 | 54 | 9 | 0 |
| 550-525-400 | [pincers] [sign 525] [comb] | 4 | 53 | 0 | 0 |
| 467-806-154 | [A with comb] [leaf on tree variant] [porter with jars] | 4 | 53 | 8 | 0 |
| 240-415-100 | [whiskered fish] [pitchfork] [three-headed person] | 7 | 53 | 10 | 0 |
| 171-035-130 | [T with leaf] [five tall strokes] [person with pitchfork] | 4 | 53 | 3 | 0 |
| 032-597-142 | [two tall strokes] [sign 597] [person with staff] | 4 | 53 | 1 | 0 |
| 455-220-002 | [three triangles] [fish] [two strokes] | 5 | 49 | 18 | 0 |
| 350-460-798 | [line with teeth] [three tall triangles] [leaf with pincers] | 4 | 49 | 11 | 1 |
| 142-400-740 | [person with staff] [comb] [jar] | 7 | 49 | 26 | 0 |
| 002-590-390 | [two strokes] [box with bar] [tree] | 9 | 49 | 15 | 0 |
| 013-840-740 | [three stacked strokes] [two leaves] [jar] | 6 | 48 | 13 | 0 |
| 055-255-435 | [eight-stroke block] [odd animal] [stroke with diagonal] | 4 | 47 | 6 | 0 |
| 233-320-920 | [barred fish] [sign 320] [bracket with leaf] | 4 | 46 | 2 | 2 |
| 032-877-740 | [two tall strokes] [diamond with four diamonds] [jar] | 7 | 46 | 9 | 1 |
| 806-158-400 | [leaf on tree variant] [porter with jars 158] [comb] | 6 | 46 | 2 | 0 |
| 240-636-740 | [whiskered fish] [rectangle 636] [jar] | 6 | 44 | 1 | 0 |
| 032-590-390 | [two tall strokes] [box with bar] [tree] | 7 | 43 | 3 | 1 |
| 503-017-740 | [striped triangle] [seven stacked strokes] [jar] | 5 | 43 | 13 | 1 |
| 233-706-033 | [barred fish] [U with stroke variant] [three tall strokes] | 5 | 41 | 7 | 0 |

Read plainly: the fixed phrases are of four sorts. Front formulas (`861-002`, `817-002`, `920-060-741`, `692-060`, `920-060-742`, `820-001`); fixed name units that travel whole (`255-435-690-740`, `590-390-740`, `415-220`, `415-100-740`, `798-415-220`, `840-032-740`, `017-575-740`, `142-617`); measure lines (`705-033-520`, `706-033-520`, `171-035`, `233-705-033`); and fixed endings (`760-740` 87% of the time, `923-740` 84%, `176-740` 50%, `555-527` 72%, `740-090`). The triples with large "beyond pairs" values (`920-060-741` 72.5, `590-390-740` 69.5, `840-032-740` 62.2, `002-032-220` 48.9) are three-sign units: their third sign is fixed by the first, not just by the second.

## 3. The two kinds of seal (`seal_kinds.csv`, `seal_kind_tests.csv`, `seal_things.csv`, `seal_length_matched_draws.csv`)

Split of the 2,238 seal objects by v2 classes: damaged 740, name seal 609, loose name (has a closer or title but breaks order) 402, other 395, **bare count line 43, front word + count line 32**, front alone 6, title alone 5, name + count 3, measure line 3.

Predictions were written in the script before the numbers. Count-line seals (75) against name seals (609):

| prediction | count-line | name seals | test | verdict |
|---|---|---|---|---|
| (a) smaller | median 477 mm2 | 576 mm2 | Mann-Whitney P 0.14; length-matched draws 485 mm2 | against: the size gap is the text length |
| (a) no animal more often | 18.7% | 19.9% | P 0.88 | against |
| (a) round or cylinder more often | 1 of 75 | 1 of 609 | P 0.21 | against (62 square, 12 rectangle, 1 cylinder) |
| (b) short-horned bull more often | 1 of 75 (1.3%) | 28 of 609 (4.6%) | P 0.36 | against |
| (c) ports and store areas more often | 7 of 52 classed (13.5%) | 63 of 446 (14.1%) | P 1.0 | against |
| (d) same text on a sealing or tag | **17 of 75 (22.7%)** | 35 of 609 (5.7%) | P 8.5e-6; length-matched draws 7.0%, 0 of 2,000 reach | **came true** |
| (e) earlier | early bin 7 of 54 (13.0%) | 49 of 435 (11.3%) | P 0.65 | against |
| (f) abroad more often | 1 of 75 | 2 of 609 | P 0.30 | against |

The frequency-band decoys produced 3 or more count-line seals in only 2 of 20 deals (the kind belongs to the real jobs), so the decoy for each difference was redesigned once as a length-matched draw from undamaged non-count-line seals (2,000 draws); results in the table.

Where they are: Mohenjo-daro 45, Harappa 14, Dholavira 4, Kalibangan 3, Banawali 2, Lothal 2, and one each at Khirsara, Chanhu-daro, Nausharo, Bhirrana, Shortughai (Central Asia). Front words on them: diamond + two strokes (861-002) 8, its variant 817-002 8, wheel + two strokes 6, outlined X + stroke pair 2. The texts that recur on sealings are `003-156`, `003-390`, `004-390` and `861-002-003-390` (on Lipi tags TAG:L / TAG:O at Mohenjo-daro DK-G and Kalibangan, and on second-catalogue sealings at Mohenjo-daro, Harappa and Kalibangan; some second-catalogue lines are the same objects as Lipi tags).

The things counted on count-line seals: tree 390 (41 uses), porter with jars 156 (16), tree variants 407 (6) and 405 (6), then 426 (3) and three singles. 92% of these uses are signs that are themselves counted on tablets, copper tablets or tags (a sign right after a number there at least twice: 390 14 times, 156 26, 407 13, 405 7); for the sign after a number on name seals the share is 82%. The big counted thing on tablets, the cup 700 (385 times), never appears on a count-line seal: seals count trees and porter-loads, tablets count cups.

**What a count-line seal is**: a stamp that states a quantity of one kind of goods, three (sometimes four or six) tree-units or porter-loads, optionally under an office front word (diamond, wheel, bracket-with-leaf + slot), with no owner's name. It is pressed onto goods about four times as often as a name seal of the same length. It is the same shape as the count line on the Umma sealing (`... 002 004 390`) and the tail of copper-tablet records. Building on: a standard-lot stamp, the seal used to certify a load rather than a person. It fits the issue-chit reading of the tablets (`jobs/out/spots.md`): if tablets record what a named person draws, the count-line seal is the matching mark on the lot itself; next test: do the counts on count-line seals (mostly 3) match the counts on tablets and tags from the same rooms.

## 4. Restorations checked on photographs (`photo_check.csv`)

Restorations: `work_data/frame/restorations_v2.csv` (1,971 lost or unclear signs on 1,417 faces; model = sign pairs + pushed v2 classes, 0.5/0.5, the best mixed model by top 5 on the gap test). 101 have the top candidate at probability 0.5 or more; 57 of those have a photo; 30 drawn by seed 4; I looked at each photo.

Tally: **fits the top candidate 5**, fits a different sign 3, cannot be judged 22.
- Fits: M-79 and M-120 (the jar 740 at the end of the line, both clearly visible), H-579 (chevron traces at the broken end: 690, completing the fixed phrase 255-435-690), M-300 (two short strokes after the wheel: 002), H-847 (a tall jar outline at the end; small photo).
- Fits another sign, none of the top 3: M-258 (a roofed three-stroke sign where 033 was proposed), M-310 (a U on a stem, not the jar), M-295 (no two strokes beside the diamond; the signs are scattered round a scene).
- Cannot be judged: text area broken off (H-83, L-17), photo too small or worn (H-234, H-365, H-725, H-836, H-840, H-744, H-953, H-562, M-1116, M-434, M-1477, M-970, M-531, M-843, M-636), photo strings not matching the catalogue (M-1498, M-492), wrong side or wrong object in the photo file (H-571, L-212 file shows L-272), lost places inside a worn zone (H-639).

Of the 8 that could be judged, 5 fit the top candidate. All three misses are on seals where the catalogue marks the place unclear rather than lost, and the actual sign is a rarer one the model never offered.

## Corpus in jobs and the book

- `work_data/frame/corpus_jobs.csv`: all 5,679 faces: sign numbers, v2 class and pushed class of each sign, picture-words, text kind, broken edge, restorations (`position:candidate=probability/...`, top 3), the restored string and the text kind after restoring. Text kinds: damaged 2,079, name text 1,264, other 1,192, loose name 591, bare count line 418 (353 of them tablets: cup + tall strokes), front word + count line 43, front alone 25, one picture 24, record 17, title alone 16, measure line 10. Restoring the lost signs moves 641 damaged faces into a kind (264 name texts, 198 loose names, 116 other, 34 title alone, 14 bare count lines, the rest smaller).
- `FRAMEBOOK.md` (repo root): picture-words from the blind describers (`work_data/pictures/pictures_blind.csv`, 312 first-catalogue signs mapped through the crosswalk) with shape names for the rest; the key, the grammar in plain words, the kind-by-object table, and 10 examples of each text kind by site as picture-words with jobs, e.g. `817-002-005-390`: [house · front] [two strokes · slot] [five strokes · number] [fork · counted] (the blind describers saw the diamond as a house and the tree as a fork).

## What went against

- **The kind grammar loses on new texts.** Transitions learned per object kind cost more bits than the pooled table for every frame (v2 7.664 against 7.536), worst on tags and sealings (7.95 against 7.37). One redesign (`frame2_kind_redesign.py`: second-catalogue sealings scored with the seal grammar, the back-off weight chosen on the held-out half of the first catalogue: 50, or 200 for pushed v2): it now wins on held-out first-catalogue texts (v2 7.143 against 7.175) and on new tablets (8.118 against 8.173), copper tablets (7.812 against 8.085) and pots (8.099 against 8.499), but still loses on new seals (7.455 against 7.374), so the pooled table stays the headline. Next: seal transitions pooled, kind transitions for the other objects, chosen on the held-out half.
- **Pushed v2 against its decoys**: one decoy of 20 beats it in bits (7.349 against 7.386). The push mostly makes frequent signs into one-sign classes, and a one-sign class works whichever frequent sign it holds. The pushed classes measure how much order is sign-specific (the fixed phrases), not a better set of jobs.
- **The learned automaton coverage** (allowed class steps seen 3+ times) gives decoys equal or higher coverage on seals and tablets for every frame (v2 seals 74% against decoy 76%): it rewards loose grammars and does not separate real from decoy. The written patterns do.
- **Seals with a count line differ from name seals in none of size (once length is matched), animal, findspot, period or being abroad.** The short-horned bull prediction went the other way (1.3% against 4.6%). Rescue: the count-line seal is an ordinary seal of an ordinary household used for a different act (stamping a lot); test next whether house-mates of count-line seals hold tablets or tags with the same count and thing.
- **Photo check**: 22 of 30 photos too small, worn or mismatched to judge; 3 of the 8 judged show a sign the model did not offer.
- **The held-out ratio of the fixed pairs**: the top 40 pairs from order-shuffled corpora also turn up in the new texts above the v2 expectation (4.8 times against 3.6 for the real pairs), because signs that sit in the same texts keep doing so. The order check (151 in order against 6 reversed) is what shows the pairs are fixed in order.
