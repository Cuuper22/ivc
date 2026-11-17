# Splitting the three double-duty signs (850, 824, 001): does it sharpen the sign-order model?

Date 2026-11-17. Word-free: sign numbers, job classes, counts only. Scripts in `work_scripts/`: `split_common.py` (kit, reuses the frame v2 class code and the v2 base classes), `split_1_contexts.py` (contexts and clustering), `split_2_test.py <sign> [left]` (refit and score against decoys), `split_3_report.py` (ranks), `split_4_describe.py`. Tables: `work_data/split/` (`contexts_<sign>.csv`, `clusters.json`, `test_<sign>.csv`, `test_<sign>_left.csv`, `ranks.csv`, `ranks_left.csv`, logs).

## What was found

1. **824 splits into two uses, and the split holds on held-out texts.** One use opens a text right before the after-front slot (10 copy events, all seals: 6 at Mohenjo-daro, 1 each at Harappa, Lothal, Dholavira and one unplaced; first sign of the text in 10 of 10, next class the slot in 10 of 10). The other closes a text after a name part (22 copy events, all Harappa tablets; last sign of the text in 20 of 22, left neighbour a name part in 13 and the tall two in 4). Clustering on neighbours finds these two groups with 1.000 agreement across five refits, and two profiles beat one on held-out occurrences by 0.699 bits per occurrence. Refitting the frame with the two uses as separate tokens lowers held-out bits per sign from 7.0598 to 7.0587 (mixture split) and 7.0583 (text-start rule) on the first catalogue, rank 1 of 21 against 20 random splits of the same sizes (plain random decoys) in every variant tried, and rank 1 against the stricter decoys that keep site and object kind (one tie at the mixture split). Inside the texts that carry 824 the gain is 7.8172 to 7.5159 bits per sign (0.30). It beat the unsplit frame in 6 to 8 of 10 held-out fits. What it means: 824 is two signs in the order model, an opener before the slot and a closer after a name. What it does not get: the second catalogue's 482 new texts contain no 824 at all, so the second held-out set cannot test it (stated as not testable, not as a pass).
2. **The two uses of 824 are the same thing as site-plus-object-kind.** Group 0 is seals, group 1 is Harappa tablets. So decoys that shuffle inside site and object kind reproduce the split almost exactly (20 of 20 ties for the kind rule), and rank against them says nothing beyond the plain random decoys. The use of 824 follows where and on what it is written as much as it follows the text.
3. **850 fails, twice.** Its clustering does not even beat one profile on held-out occurrences (two profiles minus one: -0.141 bits per occurrence; three profiles minus two: +0.137, three about equal to one). Refit on the first catalogue, every 850 split (mixture 2, mixture 3, text start, seal against other kind, and the one redesign: counting-context on the left) gains at most 0.0012 bits per sign overall in the one-sign-per-class scheme and loses in the class-joining scheme; against the site-and-kind decoys it ranks 8 to 21 of 21 (the seal-versus-other rule ties its own decoys); in the class-joining scheme it ranks 1 against plain random decoys only because those decoys are worse than the unsplit frame while the real split is also worse than it (7.0601 to 7.0617 against 7.0598), so that rank 1 is not a pass. A real and clean description exists (12 Mohenjo-daro copper tablets where 850 follows a counted thing and precedes a place word, left THING 12 of 12, right PLACE 12 of 12, against seals where it sits in a name), but it does not improve prediction on held-out texts. The redesign's single bright spot (new texts, 7 occurrences, rank 1 of 21, gain 0.0042) is not repeated on the first catalogue (rank 21 of 21, 0 of 10 fits better) and does not count.
4. **001 splits into three uses only in the class-joining scheme, with a small gain.** Three-profile groups (205 copy events): group 0, 108 events, mostly seals, after a name part or a closer and before a name part or a short number; group 1, 67 events, mostly seals, right after a front word, slot or measure and before a name part or crest; group 2, 30 events, tablets and pots, mostly Harappa, short texts (median 4 signs), at text start 30% and text end 33%. The three-way split (variants joining their best v2 class) takes first-catalogue held-out bits from 7.0598 to 7.0584, rank 1 of 21 against both decoy kinds, 8 of 10 fits better; on the 52 new-text occurrences it takes 7.5362 to 7.5248, rank 1 of 21 against both, and inside the texts carrying 001 it is 7.4820 to 7.4470. The same split with variants as their own one-sign classes does not gain (rank 21 of 21 on the first catalogue). Two-way versions are weaker (mixture 2: rank 6 against stricter decoys on the first catalogue; left-context rule: rank 2). So: a three-use 001 holds in one scheme on both held-out sets and fails in the other.
5. **Overall effect on the model is small.** Over all held-out signs (not only those in texts with the split sign) the best gains are 0.0015 bits per sign (824), 0.0014 (001, first catalogue; 0.0113 on new texts). The frame's headline gap to the sign-pair model is 0.644 bits per sign on new texts (7.536 against 6.892), so one split closes about 0.2% of it on the first catalogue and about 1.8% on new texts (001 three-way: 0.0113 / 0.644).

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
- Not run: a control that applies the same clustering to frequency-matched other signs; the by-kind grammar was scored for real splits and unsplit frames only (columns `realk_*`, `U0k`, `U1k` in the test CSVs, not tabulated here).
