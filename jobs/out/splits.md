# Splitting the three double-duty signs (850, 824, 001): does it sharpen the sign-order model?

Date 2026-11-17. Word-free: sign numbers, job classes, counts only. Scripts in `work_scripts/`: `split_common.py` (kit, reuses the frame v2 class code and the v2 base classes), `split_1_contexts.py` (contexts and clustering), `split_2_test.py <sign> [left]` (refit and score against decoys), `split_3_report.py` (ranks), `split_4_describe.py`. Tables: `work_data/split/` (`contexts_<sign>.csv`, `clusters.json`, `test_<sign>.csv`, `test_<sign>_left.csv`, `ranks.csv`, `ranks_left.csv`, logs).

## What was found

1. **824 splits into two uses, and the split holds on held-out texts.** One use opens a text right before the after-front slot (10 copy events, all seals: 6 at Mohenjo-daro, 1 each at Harappa, Lothal, Dholavira and one unplaced; first sign of the text in 10 of 10, next class the slot in 10 of 10). The other closes a text after a name part (22 copy events, all Harappa tablets; last sign of the text in 20 of 22, left neighbour a name part in 13 and the tall two in 4). Clustering on neighbours finds these two groups with 1.000 agreement across five refits, and two profiles beat one on held-out occurrences by 0.699 bits per occurrence. Refitting the frame with the two uses as separate tokens lowers held-out bits per sign from 7.0598 to 7.0587 (mixture split) and 7.0583 (text-start rule) on the first catalogue, rank 1 of 21 against 20 random splits of the same sizes (plain random decoys) in every variant tried, and rank 1 against the stricter decoys that keep site and object kind (one tie at the mixture split). Inside the texts that carry 824 the gain is 7.8172 to 7.5159 bits per sign (0.30). It beat the unsplit frame in 6 to 8 of 10 held-out fits. What it means: 824 is two signs in the order model, an opener before the slot and a closer after a name. What it does not get: the second catalogue's 482 new texts contain no 824 at all, so the second held-out set cannot test it (stated as not testable, not as a pass).
2. **The two uses of 824 are the same thing as site-plus-object-kind.** Group 0 is seals, group 1 is Harappa tablets. So decoys that shuffle inside site and object kind reproduce the split almost exactly (20 of 20 ties for the kind rule), and rank against them says nothing beyond the plain random decoys. The use of 824 follows where and on what it is written as much as it follows the text.
3. **850 fails, twice.** Its clustering does not even beat one profile on held-out occurrences (two profiles minus one: -0.141 bits per occurrence; three profiles minus two: +0.137, three about equal to one). Refit on the first catalogue, every 850 split (mixture 2, mixture 3, text start, seal against other kind, and the one redesign: counting-context on the left) gains at most 0.0012 bits per sign overall in the one-sign-per-class scheme and loses in the class-joining scheme; against the site-and-kind decoys it ranks 8 to 21 of 21 (the seal-versus-other rule ties its own decoys); in the class-joining scheme it ranks 1 against plain random decoys only because those decoys are worse than the unsplit frame while the real split is also worse than it (7.0601 to 7.0617 against 7.0598), so that rank 1 is not a pass. A real and clean description exists (12 Mohenjo-daro copper tablets where 850 follows a counted thing and precedes a place word, left THING 12 of 12, right PLACE 12 of 12, against seals where it sits in a name), but it does not improve prediction on held-out texts. The redesign's single bright spot (new texts, 7 occurrences, rank 1 of 21, gain 0.0042) is not repeated on the first catalogue (rank 21 of 21, 0 of 10 fits better) and does not count.
4. **001 splits into three uses only in the class-joining scheme, with a small gain.** Three-profile groups (205 copy events): group 0, 108 events, mostly seals, after a name part or a closer and before a name part or a short number; group 1, 67 events, mostly seals, right after a front word, slot or measure and before a name part or crest; group 2, 30 events, tablets and pots, mostly Harappa, short texts (median 4 signs), at text start 30% and text end 33%. The three-way split (variants joining their best v2 class) takes first-catalogue held-out bits from 7.0598 to 7.0584, rank 1 of 21 against both decoy kinds, 8 of 10 fits better; on the 52 new-text occurrences it takes 7.5362 to 7.5248, rank 1 of 21 against both, and inside the texts carrying 001 it is 7.4820 to 7.4470. The same split with variants as their own one-sign classes does not gain (rank 21 of 21 on the first catalogue). Two-way versions are weaker (mixture 2: rank 6 against stricter decoys on the first catalogue; left-context rule: rank 2). So: a three-use 001 holds in one scheme on both held-out sets and fails in the other.
5. **Overall effect on the model is small.** Over all held-out signs (not only those in texts with the split sign) the best gains are 0.0015 bits per sign (824), 0.0014 (001, first catalogue; 0.0113 on new texts). The frame's headline gap to the sign-pair model is 0.644 bits per sign on new texts (7.536 against 6.892), so one split closes about 0.2% of it on the first catalogue and about 1.8% on new texts (001 three-way: 0.0113 / 0.644).

6. **Control: 824 and 001 are rarer than a typical busy sign, not unique.** Of 20 signs matched to 824 by frequency and spread over the classes, 3 pass the plain bar (rank 1 against both decoy kinds); 1 passes the stricter bar that drops empty ties; 0 pass on both held-out sets. Of 20 matched to 001, 4 (mixture 3) and 9 (mixture 2) pass the plain bar; 2 pass the strict bar on the first catalogue, 0 on both sets. 001 three-way passes both sets; 824 passes the first (and has no new-text occurrences). Two controls (798, 090) pass on the first catalogue, 798 with a bigger gain than 001's. Details in "Control" below.
7. **By-kind grammar agrees with the pooled grammar** (table below): 824 gain 0.0015, 001 three-way 0.0027 (first catalogue) and 0.0120 (new texts), 850 about zero.

## Terms

- **Bits per sign**: how many yes/no questions the model needs, on average, to guess the next sign of a text it has not seen; lower is better. Counted over all held-out texts ("all") or only over held-out texts that contain the split sign ("with sign").
- **Class / frame v2**: the 14 job classes of `jobs/out/frame_v2.md` (front word OPEN, after-front slot SLOT, name front CREST, name part PERSONAL, short number NUM_SHORT, tall number NUM_TALL, tall two NUM_NAME, measure MEASURE, after-measure AFTER_M, counted thing THING, name back NAME_BACK, place word PLACE, closer CLOSER, after-jar title TITLE). The frame guesses the next sign's class from the previous class, then the sign inside the class. The pooled class grammar (the headline one) is used.
- **Split**: sign s replaced by variants s@0, s@1 (s@2) according to a rule. **Mixture / profile / cluster**: a fitted set of K typical contexts, each occurrence going to the best-fitting one; features are the class on the left, class on the right, object kind, text-length bucket. K = 1, 2, 3 compared by likelihood on held-out occurrences (5 folds of texts).
- **Label-free held-out scoring**: on a held-out text the variants are not told; every occurrence of s may be any variant and the text probability sums over all labellings, so bits are for the original sign sequence. A split can only win by predicting order better.
- **Scheme S1**: each variant becomes its own one-sign class (compared with the unsplit frame where the sign is also its own class, "U1"). **Scheme S2**: each variant joins the v2 class (of 14) that best fits its neighbours in training texts and costs least to pick out of that class (compared with the plain unsplit v2 frame, "U0"). S2 is the primary scheme: it stays inside the 14-class frame.
- **Decoys**: 20 splits where the same sign's occurrences are divided into groups of the same sizes at random (decoys B), and 20 where the real labels are shuffled only inside the same site and object kind (decoys A, the project's chance rule). **Rank r of 21**: the real split is better than 21 - r of the 20 decoys; 1 is best; ties are not counted against it and are listed.
- **Held-out set 1**: first-catalogue distinct texts, 5 folds, two different random partitions (10 fits); the clustering is refit inside every training part; held-out texts with a sign absent from training are dropped for all models. "Occurrences" = held-out scorings (each text is held out once per partition). **Held-out set 2**: the 482 second-catalogue new texts (no partner in the first catalogue), frame fitted on the whole first catalogue.
- **Copy event**: all objects of one site and findspot with the same full text count once; one row per physical object (two catalogue rows of one stone merged). The context tables use copy events; the model training and the folds use distinct texts (each text once), which is stricter on copies.

## How the groups were found

Occurrences of each sign in distinct first-catalogue texts: 850 37, 824 19, 001 187 (copy events 53, 32, 205). Held-out log-likelihood (bits per occurrence, 5 folds of texts), higher is better:

| sign | K=1 | K=2 | K=3 | K2 minus K1 | K3 minus K2 | two-profile refit agreement |
|---|---|---|---|---|---|---|
| 850 | -9.560 | -9.701 | -9.563 | -0.141 | +0.137 | 0.962 (min 0.811) |
| 824 | -6.547 | -5.848 | -5.848 | +0.699 | 0.000 | 1.000 |
| 001 | -8.199 | -8.031 | -8.004 | +0.168 | +0.028 | 0.969 |

Meaning: 824 has two separable profiles on texts it was not fitted on; 001 has a weaker two- and three-profile structure; 850's profiles do not generalise by this method.

## Held-out bits per sign, all held-out texts, S2 scheme (pooled grammar)

"A" = decoys inside site and object kind, "B" = plain random decoys; rank of 21 (ties). "Folds" = fits out of 10 where the real split beat the unsplit frame. First catalogue rows (occurrences held out: 850 48, 824 28, 001 244); new-text rows (7, 0, 52).

| sign | split | unsplit | real | A mean (best) | rank A | B mean | rank B | folds |
|---|---|---|---|---|---|---|---|---|
| 850 | mixture 2 | 7.0598 | 7.0601 | 7.0601 (7.0598) | 11 | 7.0608 | 1 | 2 |
| 850 | mixture 3 | 7.0598 | 7.0602 | 7.0601 (7.0599) | 15 | 7.0608 | 1 | 4 |
| 850 | text start | 7.0598 | 7.0600 | 7.0601 (7.0596) | 8 | 7.0608 | 1 | 4 |
| 850 | seal vs other | 7.0598 | 7.0606 | 7.0606 | 1 (20 ties) | 7.0609 | 3 | 1 |
| 850 | left counting (redesign) | 7.0598 | 7.0617 | 7.0612 (7.0608) | 21 | 7.0608 | 21 | 0 |
| 824 | mixture 2 | 7.0598 | 7.0587 | 7.0589 (7.0587) | 1 (1 tie) | 7.0596 | 1 | 6 |
| 824 | text start | 7.0598 | 7.0583 | 7.0588 (7.0584) | 1 | 7.0596 | 1 | 8 |
| 824 | seal vs other | 7.0598 | 7.0587 | 7.0587 | 1 (20 ties) | 7.0597 | 1 | 6 |
| 824 | left counting | 7.0598 | 7.0583 | 7.0591 (7.0585) | 1 | 7.0596 | 1 | 8 |
| 001 | mixture 2 | 7.0598 | 7.0593 | 7.0594 (7.0590) | 6 | 7.0597 | 1 | 5 |
| 001 | mixture 3 | 7.0598 | 7.0584 | 7.0593 (7.0590) | 1 | 7.0597 | 1 | 8 |
| 001 | text start | 7.0598 | 7.0598 | 7.0597 (7.0595) | 17 (3 ties) | 7.0596 | 17 | 3 |
| 001 | seal vs other | 7.0598 | 7.0598 | 7.0598 | 1 (20 ties, gain 0) | 7.0598 | 1 | 3 |
| 001 | left counting (redesign) | 7.0598 | 7.0591 | 7.0595 (7.0590) | 2 | 7.0597 | 2 | 7 |

New texts (second held-out set), S2:

| sign | split | unsplit | real | A mean (best) | rank A | B mean | rank B |
|---|---|---|---|---|---|---|---|
| 850 (7 occ.) | mixture 2 | 7.5362 | 7.5361 | 7.5353 (7.5335) | 15 | 7.5347 | 16 |
| 850 | mixture 3 | 7.5362 | 7.5351 | 7.5354 (7.5349) | 4 | 7.5357 | 9 |
| 850 | text start | 7.5362 | 7.5348 | 7.5347 (7.5342) | 16 | 7.5348 | 13 |
| 850 | seal vs other | 7.5362 | 7.5324 | 7.5324 | 1 (20 ties) | 7.5348 | 2 |
| 850 | left counting (redesign) | 7.5362 | 7.5320 | 7.5340 (7.5324) | 1 | 7.5358 | 1 |
| 824 (0 occ.) | all | not testable: the sign is absent from every new text | | | | | |
| 001 (52 occ.) | mixture 2 | 7.5362 | 7.5361 | 7.5361 | 1 (20 ties) | 7.5361 | 1 (20 ties) |
| 001 | mixture 3 | 7.5362 | 7.5248 | 7.5358 (7.5341) | 1 | 7.5361 | 1 |
| 001 | text start | 7.5362 | 7.5361 | 7.5361 (7.5354) | 3 (18 ties) | 7.5358 | 5 |
| 001 | left counting (redesign) | 7.5362 | 7.5341 | 7.5360 (7.5332) | 2 | 7.5361 | 1 |

Reading the new-text rows: where a rank 1 comes with a decoy mean equal to the unsplit value (many ties), the decoys carry no information and the row shows only that the real split moved the number; only 001 mixture 3 (gain 0.0113 against decoy means 0.0004 and 0.0001) is a clear gap. Rows with 7 occurrences (850) are too small to carry a verdict.

## Scheme S1 (variants as one-sign classes), first catalogue, all held-out texts

| sign | split | unsplit (own class) | real | rank A | rank B | folds |
|---|---|---|---|---|---|---|
| 850 | mixture 2 / 3 / text start | 7.0636 | 7.0629 / 7.0624 / 7.0629 | 15 / 15 / 11 | 19 / 9 / 19 | 7 / 5 / 7 |
| 850 | seal vs other | 7.0636 | 7.0626 | 1 (20 ties) | 4 | 7 |
| 850 | left counting (redesign) | 7.0636 | 7.0629 | 20 | 20 | 8 |
| 824 | mixture 2 | 7.0601 | 7.0594 | 1 (1 tie) | 1 | 7 |
| 824 | text start | 7.0601 | 7.0595 | 4 | 1 | 7 |
| 824 | seal vs other | 7.0601 | 7.0594 | 1 (20 ties) | 1 | 7 |
| 824 | left counting | 7.0601 | 7.0599 | 11 | 2 | 6 |
| 001 | mixture 2 / 3 / text start | 7.0449 | 7.0452 / 7.0454 / 7.0456 | 21 / 21 / 21 | 21 / 21 / 21 | 5 / 5 / 4 |
| 001 | seal vs other | 7.0449 | 7.0445 | 1 (20 ties) | 1 | 8 |
| 001 | left counting | 7.0449 | 7.0456 | 21 | 21 | 2 |

Meaning: 824 gains in both schemes; 850 gains in neither beyond what random splits of the same sizes give (a one-sign class per variant lowers bits for any split, real or random, so rank is the test and 850 sits mid-pack to last); 001 gains in S1 only on the seal-versus-other rule where the decoys tie.

## Which uses, in plain terms

- **824 (32 copy events).** Use 1: opening sign of a seal text, next class always the after-front slot (10 events, seals, text length mostly 3 or more). Use 2: closing sign of a Harappa tablet text after a name part (22 events, all tablets, all Harappa). The same sign serves as front word on seals and as last sign on tablets.
- **001 (205 copy events), three-profile version.** Use A (108): inside seal and copper-tablet texts after a name part or a closer, before a name part or a short number. Use B (67): seals, directly after a front word, slot or measure, before a name part or crest. Use C (30): short tablet and pot texts, mostly Harappa, at the start or the end of the text (30% and 33%).
- **850 (53 copy events), three-profile version, descriptive only.** 23 seal-dominated events inside long name texts (left name part, right name part or measure); 18 short texts (median 3 signs) on tablets, pots and seals at the start or end of the text; 12 Mohenjo-daro copper tablets, always after a counted thing and before a place word. None of these separations helps prediction on held-out texts.

## What went against

- 850: no split beat its decoys; its clustering failed on held-out occurrences; one redesign (counting context on the left) also failed on the first catalogue (rank 21 of 21, 0 of 10 fits better).
- 824: the groups coincide with site and object kind, so the stricter decoy gives no extra information; the second held-out set cannot test it.
- 001: the gain exists only in the class-joining scheme with three groups; every one-sign-class variant of 001 (except the tied seal-versus-other rule) ranks 21 of 21 on the first catalogue; two-group versions rank 2 to 17.
- Scale: all effects are 0.0005 to 0.0113 bits per sign over all texts.
- Control: the plain bar (rank 1 against both decoy kinds) is passed by 3 of 20 signs matched to 824 and 4 to 9 of 20 matched to 001, many with empty ties; the strict bar (added after seeing them) is passed on both held-out sets by none of the controls but the control signs 798 and 090 pass on the first catalogue and 798 gains more than 001 does. The strict bar was set after seeing the control results.

## Control: do other busy signs split just as well?

Same clustering, same label-free scoring, same 20 + 20 decoys, same folds, run on 20 control signs matched to each target by number of occurrences in distinct first-catalogue texts and spread round-robin over the 14 classes (rule fixed before any control score, `work_scripts/split_5_pick.py`; list in `work_data/split/controls.csv`). 824-matched controls (target 19 occurrences, controls 11 to 36): mixture of 2 profiles, the only mixture split 824 had. 001-matched controls (target 187, controls 108 to 346): mixture of 2 and mixture of 3. Scheme S2, pooled grammar. Scripts `split_2_test.py`, `split_6_controls.py`; results `controls_result.csv`.

Two bars. **Plain bar** (the one asked for): real split better than the unsplit frame, rank 1 of 21 against decoys A and against decoys B on the first catalogue. **Strict bar** (added after seeing the controls, because many plain-bar passes are empty: the real split and all decoys tie because the clustering put almost every occurrence in one group): plain bar, plus at most 1 tie among the 20 decoys of each kind, plus an overall gain of at least 0.0001 bits per sign. The real 824 (mixture 2: 1 tie, gain 0.0011) and the real 001 (mixture 3: 0 ties, gain 0.0014) both pass the strict bar on the first catalogue; 001 mixture 3 also passes it on new texts (gain 0.0113).

| control group | split | controls | plain bar, first catalogue | strict bar, first catalogue | strict bar on first catalogue AND new texts | strict bar on new texts alone |
|---|---|---|---|---|---|---|
| matched to 824 | mixture 2 | 20 | 3 (158, 222, 243) | 1 (158, gain 0.0002) | 0 | 0 |
| matched to 001 | mixture 2 | 20 | 9 | 2 (090, 798) | 0 | 3 |
| matched to 001 | mixture 3 | 20 | 4 | 2 (090, 798) | 0 | 3 |

What it means: by the plain bar, 3 of 20 signs matched to 824 and 4 of 20 matched to 001 (mixture 3) pass as 824 and 001 do, so the plain bar alone is not special to them; on the strict bar 1 of 20 and 2 of 20 pass on the first catalogue and 0 of 20 pass on both sets, while 001's three-way split passes both. Direction: 824 and 001 (three-way) are rarer than a typical busy sign, but 001 is not unique: control signs 798 (a name part) and 090 (an after-jar title) pass on the first catalogue with gains 0.0089 and 0.0012 (798's gain is larger than 001's 0.0014), and neither repeats on new texts. For 824 the control count is small and its gain (0.0011) is larger than the 0.0002 of its one strict control. The class-joining scheme passes for scattered signs; with each variant as a one-sign class (S1) the first-catalogue strict bar passes for 11 of 20 (mixture 2) and 10 of 20 (mixture 3) 001-matched controls and 0 of 20 824-matched, so S1 is not a useful test of 001 (the real 001 fails it, most controls pass it).

### 824-matched controls (mixture 2, S2, pooled grammar, all held-out texts)

| sign | class | occ. | first cat. unsplit | real | rank A / B | strict hold | new texts real (unsplit) | rank A / B | strict hold |
|---|---|---|---|---|---|---|---|---|---|
| 104 | PERSONAL | 20 | 7.0598 | 7.0601 | 6 / 3 | no | 7.5364 (7.5362) | 1 / 1 | no |
| 621 | TITLE | 18 | 7.0598 | 7.0598 | 1 / 1 | no | 7.5362 (7.5362) | 1 / 1 | no |
| 752 | AFTER_M | 21 | 7.0598 | 7.0598 | 1 / 3 | no | 7.5362 (7.5362) | 1 / 1 | no |
| 845 | PLACE | 21 | 7.0598 | 7.0604 | 1 / 15 | no | 7.5446 (7.5362) | 1 / 20 | no |
| 365 | SLOT | 17 | 7.0598 | 7.0602 | 15 / 19 | no | 7.5348 (7.5362) | 12 / 3 | no |
| 171 | MEASURE | 22 | 7.0598 | 7.0598 | 1 / 1 | no | 7.5362 (7.5362) | 1 / 1 | no |
| 091 | OPEN | 16 | 7.0598 | 7.0602 | 13 / 18 | no | 7.5326 (7.5362) | 17 / 11 | no |
| 035 | NUM_TALL | 25 | 7.0598 | 7.0602 | 21 / 21 | no | 7.5363 (7.5362) | 18 / 21 | no |
| 482 | NAME_BACK | 26 | 7.0598 | 7.0602 | 1 / 20 | no | 7.5359 (7.5362) | 1 / 4 | no |
| 158 | CLOSER | 29 | 7.0598 | 7.0596 | 1 / 1 | yes | 7.5364 (7.5362) | 1 / 19 | no |
| 222 | CREST | 12 | 7.0598 | 7.0587 | 1 / 1 | plain only | 7.5330 (7.5362) | 1 / 1 | plain only |
| 406 | THING | 12 | 7.0598 | 7.0605 | 1 / 1 | no | 7.5371 (7.5362) | 1 / 1 | no |
| 013 | NUM_SHORT | 36 | 7.0598 | 7.0583 | 8 / 2 | no | 7.5369 (7.5362) | 9 / 2 | no |
| 236 | PERSONAL | 20 | 7.0598 | 7.0595 | 16 / 15 | no | 7.5376 (7.5362) | 18 / 21 | no |
| 679 | TITLE | 17 | 7.0598 | 7.0595 | 1 / 4 | no | 7.5371 (7.5362) | 1 / 19 | no |
| 519 | PLACE | 14 | 7.0598 | 7.0598 | 1 / 1 | no | 7.5362 (7.5362) | 1 / 1 | no |
| 034 | NUM_TALL | 30 | 7.0598 | 7.0610 | 21 / 21 | no | 7.5395 (7.5362) | 21 / 21 | no |
| 360 | OPEN | 11 | 7.0598 | 7.0603 | 6 / 18 | no | 7.5362 (7.5362) | 1 / 1 | no |
| 243 | CREST | 11 | 7.0598 | 7.0595 | 1 / 1 | plain only | 7.5334 (7.5362) | 1 / 1 | plain only |
| 480 | MEASURE | 33 | 7.0598 | 7.0602 | 18 / 17 | no | 7.5401 (7.5362) | 1 / 21 | no |

### 001-matched controls, mixture 3

| sign | class | occ. | first cat. unsplit | real | rank A / B | strict hold | new texts real (unsplit) | rank A / B | strict hold |
|---|---|---|---|---|---|---|---|---|---|
| 235 | CREST | 194 | 7.0598 | 7.0602 | 11 / 21 | no | 7.5373 (7.5362) | 13 / 20 | no |
| 741 | SLOT | 199 | 7.0598 | 7.0596 | 16 / 19 | no | 7.5262 (7.5362) | 1 / 1 | yes |
| 817 | OPEN | 172 | 7.0598 | 7.0611 | 21 / 21 | no | 7.5410 (7.5362) | 21 / 21 | no |
| 590 | PERSONAL | 169 | 7.0598 | 7.0515 | 21 / 21 | no | 7.5339 (7.5362) | 21 / 21 | no |
| 705 | MEASURE | 164 | 7.0598 | 7.0598 | 1 / 1 | plain only | 7.5361 (7.5362) | 1 / 1 | plain only |
| 031 | NUM_TALL | 217 | 7.0598 | 7.0598 | 1 / 1 | no | 7.5362 (7.5362) | 1 / 1 | no |
| 520 | CLOSER | 221 | 7.0598 | 7.0597 | 21 / 5 | no | 7.5370 (7.5362) | 17 / 21 | no |
| 003 | NUM_SHORT | 156 | 7.0598 | 7.0600 | 11 / 21 | no | 7.5380 (7.5362) | 17 / 21 | no |
| 390 | THING | 226 | 7.0598 | 7.0597 | 3 / 1 | no | 7.5445 (7.5362) | 21 / 21 | no |
| 090 | TITLE | 143 | 7.0598 | 7.0586 | 1 / 1 | yes | 7.5453 (7.5362) | 21 / 21 | no |
| 100 | NAME_BACK | 110 | 7.0598 | 7.0596 | 2 / 1 | no | 7.5340 (7.5362) | 1 / 1 | yes |
| 760 | AFTER_M | 108 | 7.0598 | 7.0597 | 6 / 3 | no | 7.5361 (7.5362) | 9 / 2 | no |
| 032 | NUM_NAME | 346 | 7.0598 | 7.0598 | 1 / 1 | no | 7.5362 (7.5362) | 1 / 1 | no |
| 233 | CREST | 172 | 7.0598 | 7.0597 | 21 / 2 | no | 7.5376 (7.5362) | 21 / 21 | no |
| 060 | SLOT | 207 | 7.0598 | 7.0605 | 21 / 21 | no | 7.5362 (7.5362) | 1 / 1 | plain only |
| 861 | OPEN | 209 | 7.0598 | 7.0603 | 21 / 21 | no | 7.5344 (7.5362) | 1 / 1 | yes |
| 033 | NUM_TALL | 242 | 7.0598 | 7.0598 | 1 / 1 | plain only | 7.5361 (7.5362) | 1 / 1 | plain only |
| 798 | PERSONAL | 128 | 7.0598 | 7.0514 | 1 / 1 | yes | 7.5391 (7.5362) | 1 / 1 | no |
| 400 | TITLE | 288 | 7.0598 | 7.0597 | 8 / 2 | no | 7.5374 (7.5362) | 17 / 21 | no |
| 820 | OPEN | 213 | 7.0598 | 7.0595 | 16 / 3 | no | 7.5365 (7.5362) | 17 / 21 | no |

### 001-matched controls, mixture 2

| sign | class | occ. | first cat. unsplit | real | rank A / B | strict hold | new texts real (unsplit) | rank A / B | strict hold |
|---|---|---|---|---|---|---|---|---|---|
| 235 | CREST | 194 | 7.0598 | 7.0598 | 1 / 1 | plain only | 7.5362 (7.5362) | 1 / 1 | no |
| 741 | SLOT | 199 | 7.0598 | 7.0600 | 21 / 21 | no | 7.5256 (7.5362) | 1 / 1 | yes |
| 817 | OPEN | 172 | 7.0598 | 7.0612 | 21 / 21 | no | 7.5399 (7.5362) | 21 / 21 | no |
| 590 | PERSONAL | 169 | 7.0598 | 7.0507 | 20 / 21 | no | 7.5292 (7.5362) | 21 / 21 | no |
| 705 | MEASURE | 164 | 7.0598 | 7.0598 | 1 / 1 | plain only | 7.5361 (7.5362) | 1 / 1 | plain only |
| 031 | NUM_TALL | 217 | 7.0598 | 7.0598 | 1 / 1 | no | 7.5362 (7.5362) | 1 / 1 | no |
| 520 | CLOSER | 221 | 7.0598 | 7.0606 | 21 / 21 | no | 7.5362 (7.5362) | 2 / 1 | no |
| 003 | NUM_SHORT | 156 | 7.0598 | 7.0598 | 1 / 1 | plain only | 7.5362 (7.5362) | 1 / 1 | no |
| 390 | THING | 226 | 7.0598 | 7.0598 | 1 / 1 | plain only | 7.5362 (7.5362) | 1 / 1 | plain only |
| 090 | TITLE | 143 | 7.0598 | 7.0582 | 1 / 1 | yes | 7.5447 (7.5362) | 21 / 21 | no |
| 100 | NAME_BACK | 110 | 7.0598 | 7.0596 | 2 / 1 | no | 7.5340 (7.5362) | 1 / 1 | yes |
| 760 | AFTER_M | 108 | 7.0598 | 7.0602 | 21 / 21 | no | 7.5361 (7.5362) | 9 / 2 | no |
| 032 | NUM_NAME | 346 | 7.0598 | 7.0598 | 1 / 1 | no | 7.5362 (7.5362) | 1 / 1 | no |
| 233 | CREST | 172 | 7.0598 | 7.0598 | 21 / 21 | no | 7.5362 (7.5362) | 1 / 1 | no |
| 060 | SLOT | 207 | 7.0598 | 7.0598 | 1 / 1 | plain only | 7.5362 (7.5362) | 1 / 1 | plain only |
| 861 | OPEN | 209 | 7.0598 | 7.0601 | 21 / 21 | no | 7.5361 (7.5362) | 1 / 1 | plain only |
| 033 | NUM_TALL | 242 | 7.0598 | 7.0598 | 1 / 1 | plain only | 7.5362 (7.5362) | 1 / 1 | plain only |
| 798 | PERSONAL | 128 | 7.0598 | 7.0509 | 1 / 1 | yes | 7.5397 (7.5362) | 2 / 1 | no |
| 400 | TITLE | 288 | 7.0598 | 7.0598 | 1 / 1 | plain only | 7.5362 (7.5362) | 1 / 1 | no |
| 820 | OPEN | 213 | 7.0598 | 7.0611 | 21 / 21 | no | 7.5339 (7.5362) | 1 / 1 | yes |

## By-kind grammar (class transitions learned per object kind, backed off to the pooled table)

Bits per sign over all held-out texts with the by-kind grammar for the real split and the unsplit frame; decoys were scored with the pooled grammar only, so no rank exists for this grammar. Gain = unsplit minus real (positive = split helps). Note the by-kind grammar alone is worse than the pooled one on the new texts (7.6636 against 7.5362 unsplit), as already in `frame_v2.md`.

| sign | split | held-out set | occ. | S2 unsplit (kind) | S2 real (kind) | S2 gain, kind | S2 gain, pooled | S1 gain, kind |
|---|---|---|---|---|---|---|---|---|
| 850 | mix2 | first catalogue | 48 | 7.0595 | 7.0594 | +0.0001 | -0.0003 | +0.0004 |
| 850 | mix2 | new texts | 7 | 7.6636 | 7.6636 | +0.0000 | +0.0000 | +0.0006 |
| 850 | mix3 | first catalogue | 48 | 7.0595 | 7.0595 | -0.0001 | -0.0004 | +0.0010 |
| 850 | mix3 | new texts | 7 | 7.6636 | 7.6893 | -0.0257 | +0.0010 | -0.0004 |
| 850 | pos | first catalogue | 48 | 7.0595 | 7.0596 | -0.0001 | -0.0002 | +0.0012 |
| 850 | pos | new texts | 7 | 7.6636 | 7.6621 | +0.0015 | +0.0014 | -0.0003 |
| 850 | kind | first catalogue | 48 | 7.0595 | 7.0590 | +0.0004 | -0.0008 | +0.0009 |
| 850 | kind | new texts | 7 | 7.6636 | 7.6841 | -0.0205 | +0.0038 | -0.0015 |
| 850 | left | first catalogue | 48 | 7.0595 | 7.0590 | +0.0004 | -0.0019 | +0.0008 |
| 850 | left | new texts | 7 | 7.6636 | 7.6887 | -0.0251 | +0.0042 | +0.0024 |
| 824 | mix2 | first catalogue | 28 | 7.0595 | 7.0579 | +0.0015 | +0.0011 | +0.0006 |
| 824 | mix2 | new texts | 0 | 7.6636 | 7.6634 | +0.0001 | +0.0008 | -0.0000 |
| 824 | pos | first catalogue | 28 | 7.0595 | 7.0584 | +0.0011 | +0.0015 | -0.0000 |
| 824 | pos | new texts | 0 | 7.6636 | 7.6645 | -0.0009 | -0.0011 | -0.0000 |
| 824 | kind | first catalogue | 28 | 7.0595 | 7.0580 | +0.0014 | +0.0011 | +0.0006 |
| 824 | kind | new texts | 0 | 7.6636 | 7.6634 | +0.0001 | +0.0008 | -0.0000 |
| 824 | left | first catalogue | 28 | 7.0595 | 7.0581 | +0.0014 | +0.0015 | -0.0002 |
| 824 | left | new texts | 0 | 7.6636 | 7.6639 | -0.0003 | -0.0008 | -0.0000 |
| 001 | mix2 | first catalogue | 244 | 7.0595 | 7.0576 | +0.0019 | +0.0005 | -0.0013 |
| 001 | mix2 | new texts | 52 | 7.6636 | 7.6635 | +0.0000 | +0.0000 | -0.0019 |
| 001 | mix3 | first catalogue | 244 | 7.0595 | 7.0567 | +0.0027 | +0.0014 | -0.0033 |
| 001 | mix3 | new texts | 52 | 7.6636 | 7.6516 | +0.0120 | +0.0113 | -0.0250 |
| 001 | pos | first catalogue | 244 | 7.0595 | 7.0595 | -0.0000 | -0.0000 | -0.0010 |
| 001 | pos | new texts | 52 | 7.6636 | 7.6635 | +0.0000 | +0.0000 | +0.0012 |
| 001 | kind | first catalogue | 244 | 7.0595 | 7.0596 | -0.0002 | +0.0000 | -0.0003 |
| 001 | kind | new texts | 52 | 7.6636 | 7.6635 | +0.0000 | +0.0000 | -0.0007 |
| 001 | left | first catalogue | 244 | 7.0595 | 7.0579 | +0.0016 | +0.0007 | -0.0010 |
| 001 | left | new texts | 52 | 7.6636 | 7.6596 | +0.0040 | +0.0021 | -0.0022 |

Meaning: the by-kind grammar gives the same picture as the pooled one. 824 gains 0.0011 to 0.0015 on the first catalogue (pooled 0.0011 to 0.0015); 001 three-way gains 0.0027 on the first catalogue and 0.0120 on new texts (pooled 0.0014 and 0.0113); 850 gains between -0.0001 and +0.0004 on the first catalogue and loses 0.02 to 0.03 on new texts for three of its five splits. The one-sign-class scheme (S1) with the by-kind grammar is negative for all five 001 splits on the first catalogue (-0.0003 to -0.0033), i.e. it agrees with the pooled result that S1 does not help 001.
