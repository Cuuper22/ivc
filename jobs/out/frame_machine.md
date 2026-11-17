# The frame by machine

Scripts (in `work_scripts/`, run in this order): `frame_common.py` (loaders, hand jobs, the models; every rule written at the top before any score), `frame_classes.py` (step 1), `frame_kmeans2.py` (step 1, one redesign), `frame_predict.py` (steps 2, 3, 5 and the restorations), `frame_kind_redesign.py` (step 2, one redesign), `frame_grammar.py` (step 4). Tables and logs: `work_data/frame/`. Restorations: `work_data/frame/restorations.csv`. No words are used anywhere; signs are Lipi numbers, reading order (stored order reversed).

## What was found

1. **A machine that sees only sign order finds the hand frame by itself.** A hidden-state model with 10 states, trained on the first catalogue with no parser rules, sorts the signs into classes that match the hand parser's jobs at normalised mutual information 0.266, where 1,000 shuffles of the hand labels give 0.134 on average and 0.200 at best (P 0.001); jobs dealt among signs of the same frequency give 0.139. Counted over sign uses rather than sign types it is 0.486. A second machine method (exchange clustering) gets 0.298 (0.532 over uses). What it means: the jobs (opener, crest, ending, measure, counted thing, number) are not an artefact of the hand rules; they are in the order of the signs. What it opens: the frame can now be learned, scored and extended by machine.
2. **The hand frame predicts texts it never saw, and its own decoy does not.** On 482 second-catalogue lines with no partner in the first catalogue, the hand-job grammar costs 7.661 bits per sign against 7.849 for sign frequencies alone; the same jobs dealt to the wrong signs of the same frequency cost 7.824 on average, and the best of 20 decoys 7.739. Not one decoy reaches the real frame. The real frame captures 19.6% of everything a full sign-by-sign model learns about order; the decoy captures 2.6%. The machine's own classes capture 28.5% (hidden-state) and 33.1% (exchange).
3. **The frame restores lost signs.** On 77 texts where one catalogue has a lost sign and the other has it complete, the hand-job grammar puts the true sign in its top 5 for 45.5% and top 10 for 59.7%, against 27.3% / 35.1% for a frequency-only guess and 32.5% / 42.7% for the decoy frames (best decoy 36.4% / 45.5%). Mixed half and half with the sign-pair model it gets the true sign first 32.5% of the time (frequency guess 15.6%). The job of the lost sign is right 54.5% of the time against 28.6% for always guessing the commonest job.
4. **The machine improves the frame in two places and finds two text types the hand template missed.** (a) It splits the hand "ending or title" job in two: a closing class (jar 740, spear 520, porters 151/154/158, 555) and a class that comes after the jar (comb 400, man 090, 527, 621, 679, 565). Moving 527, 621, 161, 241 into that after-jar class and 824, 880, 545, 091 into the openers raises the likelihood of the whole corpus by 0.65 to 2.54 bits per use. (b) It finds an "opener slot" class: the sign right after an opener (002, 060, 741, 742, 001, 368, 365). (c) Two text types with no name and no ending: a bare count line `[number][counted thing]` (34 seals, 17 tablets, 9 pots; e.g. `004-390`, `003-390`) and an opener with a count line `[opener][slot][number][counted thing]` (33 seals; e.g. `817-002-003-390`, `692-060-003-426`, `861-002-016-390`). The second is a second kind of seal text: an office opening followed by a quantity of goods. It is the same shape as the "2, 4, cotton" line on the Umma sealing.
5. **Restorations written for 1,971 lost or unclear signs on 1,417 damaged faces** (`restorations.csv`): predicted job, machine class and top-5 candidate signs for each.

Terms used below:
- **Bits per sign**: how many yes/no questions, on average, a model needs to guess each next sign of a text it never saw (the end of the text counted as one more symbol). Lower = the model knows more about the script's order. A drop of 1 bit = the model's guess is twice as good.
- **Unigram**: guesses each sign from how common it is, ignoring order.
- **Sign bigram**: guesses each sign from the sign right before it (smoothed with sign frequency).
- **Class grammar**: guesses the next sign's class from the class of the sign before it, then the sign from its class. With the hand jobs as classes this is "the hand frame as a grammar"; with machine classes it is the machine frame.
- **Hidden-state model (HMM)**: a model in which each sign is emitted by one of K unseen states, the states following each other with learned rates; trained by Baum-Welch (repeated re-estimation), 10 random starts, best kept.
- **Exchange clustering**: each sign is moved to whichever of K classes makes the class grammar most likely, until nothing moves.
- **Adjusted Rand index (ARI)**: how often two partitions put the same pairs of signs together, corrected so chance = 0 and identical = 1. **Normalised mutual information (NMI)**: how much knowing one partition tells you about the other, 0 = nothing, 1 = everything.
- **Decoy frame**: the hand jobs dealt to other signs of the same frequency band (10 bands by training count), 20 deals, exactly as the word decoys were dealt.
- **New texts**: second-catalogue (Mahadevan 1977) lines with no partner in the first catalogue, complete, every sign mapped to a Lipi number and seen in training. 482 lines (357 distinct), 1,681 signs.

## 1. Jobs by machine

Training: 3,499 distinct first-catalogue texts, 708 signs, 12,995 sign uses; agreement is measured on the 166 signs with 10+ uses. Hand jobs per sign: the most common job the hand parser (gloss2) gives the sign's uses, with stroke counts fixed as number, 060 as joiner, and the hand place/time set as place word (rule in `frame_common.py`).

### Class agreement with the hand jobs (`agreement.csv`)

| method | K | ARI | NMI | NMI shuffled mean / max of 1,000 | NMI band-dealt mean | NMI over uses | P |
|---|---|---|---|---|---|---|---|
| hidden-state model | 6 | 0.032 | 0.229 | 0.096 / 0.147 | 0.099 | 0.435 | 0.001 |
| hidden-state model | 8 | 0.030 | 0.249 | 0.114 / 0.182 | 0.118 | 0.473 | 0.001 |
| hidden-state model | **10** | 0.042 | **0.266** | 0.134 / 0.200 | 0.139 | **0.486** | 0.001 |
| hidden-state model | 12 | 0.030 | 0.264 | 0.146 / 0.193 | 0.156 | 0.469 | 0.001 |
| exchange clustering | 10 | 0.052 | 0.298 | 0.135 / 0.195 | 0.141 | 0.532 | 0.001 |
| exchange clustering | 12 | 0.041 | 0.307 | 0.149 / 0.210 | 0.154 | 0.546 | 0.001 |
| k-means on sign vectors, first try | 10 | -0.114 | 0.154 | 0.131 / 0.186 | 0.121 | 0.218 | 0.07 |
| k-means, redesign (10+ use signs, neighbour vectors only) | 10 | 0.022 | 0.283 | 0.136 / 0.208 | | | 0.001 |
| Ward clustering, redesign | 10 | 0.016 | 0.264 | 0.135 / 0.188 | | | 0.001 |

Every machine method except the first k-means beats every one of 1,000 shuffles at every K. The unweighted ARI stays near 0.03 to 0.05 because the hand frame puts 562 of 708 signs (most of them rare) into one "personal name part" bin, while the machines spread name signs over several classes (front, back, number-led); counted over uses the ARI is 0.28 (HMM) and 0.33 (exchange). The two machine methods agree with each other at NMI 0.48 (K = 10).

Token level: every one of 17,848 sign uses, its HMM state in its own text against the job the hand parser gave that use: NMI 0.326, shuffled 0.001 (max of 200: 0.0015).

### The ten machine classes (HMM, K = 10)

| class | uses | hand jobs of its uses | commonest signs | plain description |
|---|---|---|---|---|
| H10_9 | 1,337 | opener 59%, personal 39% | 820 861 817 920 550 692 413 824 091 | front words |
| H10_5 | 1,596 | number 59%, personal 28%, joiner 13% | 002 060 741 001 368 742 013 365 | the slot right after a front word |
| H10_6 | 2,466 | personal 65%, crest 17%, number 15% | 220 032 240 235 233 798 415 803 255 806 840 231 | name front (fish crests, with the tall two) |
| H10_2 | 1,772 | personal 53%, number 35% | 031 003 140 004 575 142 061 125 | short numbers and person signs that start a name or count |
| H10_1 | 770 | personal 64%, measure 24% | 590 705 706 017 435 440 171 845 320 711 | measures and the box |
| H10_7 | 686 | number 35%, tag 29% | 033 760 690 585 615 070 752 | what follows a measure or box (tall three, "child of" kin signs) |
| H10_3 | 1,022 | personal 49%, tag 29%, thing 16% | 390 700 405 407 617 595 156 226 165 | counted goods (trees, cup) |
| H10_4 | 897 | personal 64%, place 19%, tag 15% | 176 100 900 904 055 388 460 923 335 482 | name back (right before the closer) |
| H10_0 | 1,762 | ending 94% | 740 520 151 154 158 555 236 161 | closer |
| H10_8 | 687 | ending 68%, personal 31% | 400 090 527 621 679 565 | title after the jar |

### Where machine and hand disagree (`disagreements_hmm10.csv`, `best_job_by_likelihood.csv`)

63 of the 166 signs sit in a machine class whose majority hand job differs from their own. For each, the hand-job grammar was refitted with the sign moved to the machine's job and the corpus likelihood compared (bits per use of the sign; positive = the data backs the machine).

The data backs the machine for 18 signs:
- into the after-jar title class: 621 (+2.48), 161 (+2.54), 527 (+1.64), 241 (+1.43);
- into the front words: 880 (+1.94), 824 (+1.81), 545 (+1.41), 091 (+0.65), 550 (+0.37), 360 (+0.27), 556 (+0.25);
- into the after-opener slot: 368 (+0.60), 742 (+0.59), 365 (+0.39), 741 (+0.37);
- 016 (+0.43), 630 (+0.16), 005 (+0.13).

The data backs the hand job for 45, among them all the stroke numbers that the machine files with the signs they stand beside (032 with the fish crests, 031/003/004 with persons), the crests 235, 803, 806, 140, the measures 705, 171, 480, the counted cup 700 and tree 390, the tags 100, 760, 690, 752, and the joiner 060 (-1.30). Many of these 45 are a by-product of naming a machine class by its majority job (7 of the 10 classes are mostly "personal name part" by uses): the machine's real statement for 032 is "the tall two lives inside fish names", which is the star-name finding (tall two + plain fish 65 of 73), not a claim that 032 is not a number.

## 2. Prediction on texts never used (`bits_per_sign.csv`, `bits_by_kind.csv`)

482 new lines, 1,681 signs. Controls: same lines with sign order shuffled within each line (10 shuffles); each sign replaced by a same-frequency sign (10 deals).

| model | new texts | order shuffled | same-frequency signs | no end symbol |
|---|---|---|---|---|
| unigram | 7.849 | 7.849 | 8.447 | 7.170 |
| sign bigram | **6.892** | 8.761 | 9.811 | 6.299 |
| class grammar, hand jobs | 7.661 | 8.506 | 8.955 | 6.981 |
| class grammar, HMM classes K=10 | 7.576 | 8.729 | 9.274 | 6.873 |
| class grammar, exchange K=10 | 7.532 | 8.744 | 9.372 | 6.879 |
| class grammar, k-means K=10 (first try) | 7.802 | 7.951 | 8.541 | 7.113 |
| class grammar, HMM K=6 / 8 / 12 | 7.687 / 7.607 / 7.533 | | | |
| hidden-state model K=10 (soft) | 7.574 | 9.052 | 9.762 | 6.677 |
| mix: bigram + hand jobs | 6.918 | 8.373 | 9.104 | 6.302 |
| **decoy frame, mean of 20** | 7.824 | 8.055 | | 7.136 |
| decoy frame, best of 20 | 7.739 | | | 7.056 |

What the differences mean:
- Order is real and the models see it: shuffling the order of the same signs costs the hand grammar 0.85 bits per sign, the machine grammars 1.15 to 1.21, the sign bigram 1.87.
- Share of the script's order captured by jobs alone = (unigram - class grammar) / (unigram - sign bigram): hand jobs 19.6%, HMM classes 28.5%, exchange classes 33.1%, decoy 2.6%. Ten classes hold a fifth to a third of everything a 708 x 708 sign-pair table knows about which sign follows which.
- The sign bigram (6.892) still beats every class grammar: most of the order sits in particular sign pairs (fixed phrases and names), not in the jobs.

By object kind (new lines; bits per sign):

| kind | lines | unigram | sign bigram | hand jobs | HMM classes | decoy mean |
|---|---|---|---|---|---|---|
| seals | 269 | 7.785 | 6.741 | 7.540 | 7.390 | 7.742 |
| tags and sealings | 89 | 7.747 | 6.617 | 7.497 | 7.387 | 7.678 |
| tablets | 50 | 8.082 | 8.173 | 8.047 | 8.422 | 8.211 |
| copper tablets | 22 | 8.241 | 6.983 | 8.166 | 8.247 | 8.280 |
| pots | 41 | 8.181 | 7.976 | 8.394 | 8.382 | 8.237 |

On seals and tags the frame works as above. On new tablets, copper tablets and pots the pooled class grammars do no better than the unigram (see "went against").

## 3. Fill-the-gap (`gap_test.csv`, `gap_job_test.csv`)

Items: crosswalk text pairs where one side has exactly one lost sign and the other side has the same text complete, same length, every other position equal: 77 distinct items (57 lost in the first catalogue, 20 lost in the second). A wider set allows one other mismatch: 157 items. Training for this test leaves out the 515 first-catalogue faces whose text is a test text or its completed answer.

Main set (77 items): true sign in top 1 / top 5 / top 10.

| model | top 1 | top 5 | top 10 |
|---|---|---|---|
| frequency only | 15.6% | 27.3% | 35.1% |
| class grammar, hand jobs | 18.2% | 45.5% | 59.7% |
| class grammar, HMM K=10 | 23.4% | 40.3% | 48.1% |
| class grammar, exchange K=10 | 26.0% | 44.2% | 50.6% |
| hidden-state model K=10 (soft) | 19.5% | 48.1% | 55.8% |
| sign bigram | 24.7% | **57.1%** | 68.8% |
| mix: bigram + hand jobs | **32.5%** | 54.5% | **70.1%** |
| mix: bigram + HMM classes | 31.2% | 55.8% | 63.6% |
| decoy frame, mean of 20 | 17.3% | 32.5% | 42.7% |
| decoy frame, best of 20 | 15.6% | 36.4% | 45.5% |

Wider set (157 items): frequency 12.7 / 28.0 / 38.9; hand jobs 15.3 / 38.9 / 49.0; mix bigram + hand 26.1 / 48.4 / 58.6; decoy mean 14.8 / 30.6 / 40.5.

Job of the lost sign (main set): hand-job grammar right 54.5% against 28.6% for always guessing the commonest job; HMM classes 45.5% against 23.4%; exchange classes 46.8% against 20.8%. The sign bigram's guesses, read as hand jobs, are right 55.8%.

Restorations (`work_data/frame/restorations.csv`): the model with the best top-5 on the main set (rule fixed in advance: sign bigram) gives the top-5 candidates; the predicted job comes from the hand-job grammar and the machine class from the HMM-class grammar. 1,971 lost or unclear signs on 1,417 of the 2,079 damaged faces (the other 662 are broken at an edge with no lost sign inside). Predicted jobs: personal name part 1,569, ending or title 277, number 74, opener 51. The top candidate has probability 0.5 or more for 7.6% of them; example: `861-002-032-220-240-100-[lost]` → jar 740 at 0.94.

## 4. The template as a grammar (`grammar.txt`, `grammar_summary.csv`)

Machine classes (HMM K=10) as named in section 1. Distinct clean first-catalogue texts. "A → B 66%" = 66% of the time the class after A is B; END = the text ends.

**Seals** (1,419 texts, mean 4.7 signs). Start: front word 38%, number/person 21%, name front 19%.
front word → after-opener slot 66% · after-opener slot → name front 41%, number/person 21% · name front → name front 33%, closer 20%, name back 13%, measure 11% · number/person → counted goods 30%, number/person 14%, name front 11% · name back → closer 64% · measure → after-measure 38%, counted goods 21% · after-measure → closer 57% · counted goods → END 44%, after-opener slot 23% · closer → END 79%, after-jar title 12% · after-jar title → END 77%.

**Tablets** (508). Start: name front 31%, front word 20%, number/person 20%. closer → END 54%, **after-jar title 39%** (seals 12%) · after-jar title → END 86% · front word → after-opener slot 42%, END 14% (a front word alone) · name back → closer 64%.

**Tags and sealings** (42). Start: front word 38%. front word → after-opener slot 72% · closer → END 88%. Commonest: measure + after-measure + closer (`705-033-520`, `445-760-740`).

**Pots** (154, mean 2.05 signs). Start: number/person 34%. Almost every class is followed by END 36 to 88%. One-sign texts: a number (13), a name front (7), a title (7), counted goods (6), a front word (5).

**Copper tablets** (68). Start: name front 43%. name front → measure 33%, name front 28%, name back 20% · measure → after-measure 54% · number/person → counted goods 55% · counted goods → END 67%. A record formula: `[name front][measure][after-measure]…[closer][number][counted goods]`, e.g. `220-017-585-095-520-032-407`, `255-435-690-740-900-001-003-423`: a name with its ending, then a count line after it.

Against the hand template `[opener][name = crest + personal + tag][ending]`, written as a strict pattern over the hand jobs: fits 40% of seal texts, 46% of tablets, 45% of tags, 34% of copper tablets, 16% of pots.
- **Where they match**: front word → slot → name front → … → name back → closer → END is the backbone on seals, and the machine finds each piece: openers, crest-led names, name-back signs that sit right before the closer (64%), the jar as closer, a title after the jar.
- **Where the machine differs**: (1) the ending is two slots, closer then title, and the title slot is three times as common on tablets as on seals (39% against 12%); (2) the after-opener slot is its own class (002, 060, 741, 742, 368, 365); (3) numbers are not one class: the tall two lives inside fish names, short numbers and person signs start names or count lines, the tall three follows measures; (4) a measure takes its own follower class (tall three, kin signs).
- **Text types the hand template missed**:
  1. Bare count line `[number][counted goods]`: 34 seals, 17 tablets, 9 pots, 2 tags (`004-390`, `003-390`, `230-156`, `034-700`).
  2. Front word + count line, no name, no ending: 33 seals, 6 tablets, 1 tag (`817-002-003-390`, `861-002-016-390`, `692-060-003-426`, `550-060-003-390`). A second kind of seal text.
  3. A title sign alone: 18 seals (`411`, `679`, `047`, `147`), 7 pots, 4 tablets.
  4. One picture-sign on copper tablets: 9 texts (`782`, `780`, `341`), the signs that copy the picture side.
  5. Name + gate + guard with no jar on tablets: `220-550-525`, `233-550-526`, `233-550-527`.
  6. The copper-tablet record: name, ending, then a count line.

## 5. Decoy control on the frame itself

| test | real hand frame | decoy mean of 20 | best decoy | decoys at or above real |
|---|---|---|---|---|
| bits per sign, new texts (lower better) | 7.661 | 7.824 | 7.739 | 0 of 20 |
| share of bigram gain captured | 19.6% | 2.6% | 11.5% | 0 of 20 |
| cost of shuffling order (bits) | 0.85 | 0.23 | | |
| gap test top 5 | 45.5% | 32.5% | 36.4% | 0 of 20 |
| gap test top 10 | 59.7% | 42.7% | 45.5% (of the best top-5 decoy) | |
| gap test top 1 | 18.2% | 17.3% | 15.6% (of the best top-5 decoy) | |
| job of the lost sign: gain over guessing the commonest job | +25.9 points (54.5 against 28.6) | +5.3 points (55.6 against 50.3) | | |

The real frame beats its own decoy on every order and fill test, by about the width of the whole decoy spread. Meaning: the jobs belong to the signs they were given; dealt to other signs of the same frequency they lose nearly all their predictive power on texts never used.

## What went against

- **k-means first try at chance**: NMI 0.154 against shuffled 0.131 (P 0.07), one giant cluster. Redesign (fit on the 166 signs with 10+ uses, neighbour vectors only): 0.283 against shuffled max 0.208, and its clusters repeat the HMM's (front words; after-opener slot 002 060 741 742 001; after-jar titles 400 090 151 621 679 565; closer 740 520 154 158).
- **Tablets, copper tablets and pots in the new texts**: the pooled class grammars do no better than the unigram (tablets 8.05 against 8.08; pots 8.39 against 8.18). One redesign (`frame_kind_redesign.py`, class transitions learned on the same kind only): pots hand frame 7.899 against unigram 8.181 and decoy mean 8.065 (best decoy 7.854); copper tablets 7.817 against 8.241, decoy mean 8.189 but best decoy 7.488 (22 lines); tablets 8.040 against 8.082, decoy mean 8.099, best 7.760; tags fell to 7.899 (only 42 training tags). So on pots the kind grammar beats the decoy mean, on tablets the frame still carries nothing measurable over 50 new lines.
- **Top-1 gap fill**: the hand frame alone (18.2%) is no better than its decoy (17.3%) at the single best guess; its gain is in the top 5 and top 10.
- **Job accuracy on its own**: the decoy frame's raw job accuracy (55.6%) equals the real one (54.5%) because decoy dealing piles frequent signs into the commonest decoy job (its baseline is 50.3%); only the gain over baseline separates them.
- **The sign bigram beats every class grammar** in bits (6.89 against 7.53 to 7.66): jobs carry a fifth to a third of the order, sign pairs the rest.
- **Disagreements**: the likelihood backs the machine on 18 of 63 disagreeing signs, the hand job on 45.
- **Restorations are spread**: the top candidate reaches probability 0.5 on 7.6% of the 1,971 lost signs.

Rescue plan, one line each: kind-specific grammar with kind-specific emissions trained on both catalogues' partnered texts (more tablet data); a trigram class grammar for tablets (their formula runs across three or more slots); feed the machine's two-slot ending and after-opener slot back into the hand parser and rerun steps 2, 3, 5.
