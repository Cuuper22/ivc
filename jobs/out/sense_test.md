# Sense test: does the Dravidian word on a sign, with ALL its senses, make sense with its neighbours?

Scripts `work_scripts/sense_*.py`, data and tables `work_data/sense/` (each file under 20 MB). Everything below is rerunnable: `sense_corpus.py`, `sense_build.py`, `sense_embed.py`, `sense_run.py 1000`, `sense_control_build.py`, `sense_control_run.py 1000`, `sense_onegloss.py 1000 K`, `sense_report.py`.

## What was found

1. **With every sense counted (up to 25 per word), no score version separates the real word list from same-job shuffles.** New texts, all labelled signs, shuffles that keep the number of senses (B): category overlap real 0.8347 against a chance mean of 0.8360 (P 0.569); category lift 0.0773 against 0.0755 (P 0.345); vector closeness 0.2542 against 0.2579 (P 0.612). P is the share of 1,000 shuffles that score at least as high as the real list; 0.5 is a typical shuffle, 0.05 or less would be a win. Plain shuffles (A, same class and band only) give P 0.597 / 0.374 / 0.678. On the Lipi catalogue (second number): A P 0.546 / 0.336 / 0.525. The 30 strongest-labelled signs: new texts B P 0.328 / 0.429 / 0.452; Lipi A P 0.033 (overlap) and 0.045 (vectors) but B P 0.193 and 0.107. Meaning: a real word with many senses does not fit its neighbours better than another word of the same job, band and sense count. It points to no word-level signal; the one place a P under 0.05 shows (30 strongest on Lipi, plain shuffles) vanishes once sense counts are matched.
2. **The mass run finds nothing either, and one version points the wrong way.** Each sign's label was replaced in turn by every word of its job class (36 candidates on average) with its neighbours kept. Mean percentile of the real label (1.0 best, 0.5 chance): overlap 0.448, lift 0.481, vectors 0.493; the same search on new texts with which signs sit together destroyed gives 0.496 / 0.480 / 0.506. First place: 9.3% / 7.9% / 10.2% against 11.1% by chance. Against: for category overlap the real label sits below the middle (0.448, and 0.405 among candidates with a similar number of senses).
3. **Per sign, nothing stands out.** 170 signs have at least 5 weighted objects; their z (distance from their own shuffles, in spreads, mean of 3 versions) has mean -0.01, none above +2 and none below -2 (tables below). The top of the list is dominated by measure and quantity words (vaḷḷam, pāti, kar̤añcu, kōṭṭai, nel), at z +0.7 to +1.3 — a pattern, not a result.
4. **The test can see a real signal, so the null is not blindness of the machinery.** Control: 1,519 real English sentences (human translations of Wiktionary example sentences), every word with its WordNet senses, same code. Real against sense-count-keeping shuffles: vector closeness z +16.8 (P 0.001), category lift z +2.30 (P 0.015), category overlap z +1.59 (P 0.052, borderline). Vector closeness is a strong detector; category overlap is a weak one.
5. **A surprise that opens a line: the signal is there when each word keeps only its first gloss.** Same test, each word cut to the label's own first gloss (category lift, plain shuffles, lifts learned on Lipi and applied to new texts that were not used to pick labels): new texts z +2.82 (P 0.005), Lipi z +3.77 (P 0.001). It fades as senses are added (table below) and is gone by 12 senses. Reading: the first gloss carries a category fit with the neighbours; piling on senses lets almost any pair of signs find some matching category pair, so the max-over-senses score saturates. The width of the sense list (47% of signs hit the 25 cap, with dictionary homonyms mixed in) is what kills the test's power, not the idea. Caveats: the cap was varied after seeing the null (five caps, no correction); vector closeness and category overlap show nothing at any cap, and category overlap on the first gloss alone points the wrong way (new texts z -1.20, P 0.868).

| first K senses kept | lift, new texts: z (P) | lift, Lipi: z (P) | vector closeness, new texts: z (P) | category overlap, new texts: z (P) |
|---|---|---|---|---|
| 1 | +2.82 (0.005) | +3.77 (0.001) | -0.36 (0.616) | -1.20 (0.868) |
| 3 | +2.67 (0.014) | +3.44 (0.002) | +0.54 (0.288) | +0.38 (0.341) |
| 6 | +2.54 (0.022) | +3.00 (0.005) | -0.42 (0.631) | -0.37 (0.641) |
| 12 | +0.69 (0.227) | +1.05 (0.175) | -0.55 (0.695) | +0.07 (0.494) |
| 25 | +0.14 (0.398) | +0.41 (0.313) | -0.54 (0.702) | -0.18 (0.612) |

(P is the share of 1,000 plain same-class-and-band shuffles at least as high as the real list. K=1 is the old one-gloss assumption.)

## What went against

- Items 1 to 3 above: full sense lists show no word-level signal in any of three versions, on new texts or Lipi.
- Category overlap on the first gloss is below chance (z -1.20 new texts); in the mass run the real label ranks below the middle (0.448).
- Vector closeness (the strongest detector in the control, z +16.8) shows nothing on the Indus list at any sense cap.
- Control power is shown on natural sentences of 1,519 texts with at most 8 senses a word; Indus texts are formulaic and the sense lists run to 25. The control proves the machinery can see topic-level meaning, not that it has the same power at Indus sizes.

## Terms

- **Sense**: one short English gloss of a word (a phrase from the dictionaries). A word's **sense list** = the label's own glosses (values_master4.csv: english, english_long), then every gloss of the same-spelled Tamil word in DEDR (Burrow and Emeneau) and in Wiktionary Tamil, then, if the label cites DEDR entry numbers, every gloss of that whole entry, at most 25 (`sense_build.py`). Words with no dictionary hit keep the label glosses. Of 195 labelled rows, 184 signs have a word (the 11 "(n) n loads" signs have none); 119 distinct words; mean 15.4 senses, median 19; 47% of signs hit the cap; 10 words have one sense.
- **Category** (13, fixed list: number, measure, commodity, person, kin, place, time, deity, animal, plant, tool, action, quality): each sense gets every category triggered by any of its first 5 content words, by keyword lists written in `sense_common.py` and, if no keyword hits, the WordNet lexicographer file of the word's first sense; a gloss starting "to " is also action. 91% of senses get at least one category. The rule is crude (one example: "creep" lands in person through WordNet's first noun sense); star and planet words are filed under time/calendar.
- **Embedding**: each sense phrase turned into a 768-number vector by google/embeddinggemma-2 (Apache 2.0; downloaded without login from huggingface.co, 744M parameters, CPU, float32, "sentence similarity" prompt). Vectors were saved once (`senses_emb.npy`, float16, 2.8 MB) and all scoring is table lookups. **Vector closeness** of two senses = cosine of their vectors after subtracting the mean vector of all senses and renormalising (raw cosines all sit near 0.72 and carry little contrast).
- **Category overlap (ov)**: two senses score 1 if they share a category, else 0.
- **Category lift (lift)**: for a pair of categories, the log of (how often signs carrying the two categories sit in one text) divided by (how often independence would put them there). Learned on real labels of other texts: Lipi split in two halves by object, each half scored with lifts learned on the other half; new texts scored with lifts learned on all Lipi. Two senses are worth the biggest lift among their category pairs (0 if either has no category). Lift above 0 = categories that go together.
- **Text score** (max over senses): for each sign in the text, its fit = the best, over its own senses, of the average over the other signs of the best match to that sign's senses; text score = mean fit. Pairs of signs carrying the same word are skipped (variant signs of one word would otherwise match perfectly in the real list only). Only signs with a word count; a text needs at least 2 signs with 2 different words.
- **Total score** = mean text score, one weight per physical object (split over its faces). One row per physical object: Lipi faces joined by object id and duplicate catalogue rows of one stone merged; moulded copies (same site, same excavation area, house and room, same full text) count once (4,691 stones become 4,476 events; unknown findspots never merge). New texts = second-catalogue texts with no Lipi partner: 1,050 objects become 990 events after copies merge (same site, locus, full text); 715 of them have a scorable text. Lipi: 3,429 scorable events. 11 texts longer than 10 labelled signs were cut at 10.
- **Shuffle A**: words dealt among signs of the same frame-v2 class (`work_data/frame/classes_v2.csv`, v2_base, 14 classes) and the same frequency band (tercile of Lipi face count among labelled signs), the old decoy rule; 174 of 184 signs can move. **Shuffle B**: also keeps the number of senses: inside each cell signs are sorted by sense count and words dealt only inside blocks of 3. The average change in sense count per sign is 7.8 under A and 2.0 under B. 1,000 shuffles each.
- **30 strongest-labelled**: status strict, a DEDR entry number given, not a number sign, top 30 by Lipi face count (pool of 55). Their score is the mean fit of those signs' occurrences (neighbours may be any labelled sign; all words are still shuffled).
- **z**: real minus shuffle mean, in shuffle spreads. 0 = typical shuffle.

## Tables

### Core table (real list against 1000 shuffles of each kind)

P = share of shuffles scoring at least as high as the real list (so P near 0 = real list ranks at the top; near 0.5 = it is a typical shuffle; near 1 = it ranks at the bottom). "chance" column = mean of the shuffles +- one spread.

| score | texts | signs scored | real | A: chance (same class+band) | A: P | A: z | B: chance (sense count kept) | B: P | B: z | reading of B |
|---|---|---|---|---|---|---|---|---|---|---|
| category overlap | new texts (main) | all labelled | 0.8347 | 0.8400 +- 0.0301 | 0.597 | -0.18 | 0.8360 +- 0.0255 | 0.569 | -0.05 | inside chance |
| category lift | new texts (main) | all labelled | 0.0773 | 0.0756 +- 0.0102 | 0.374 | +0.17 | 0.0755 +- 0.0095 | 0.345 | +0.18 | inside chance |
| vector closeness | new texts (main) | all labelled | 0.2542 | 0.2599 +- 0.0121 | 0.678 | -0.48 | 0.2579 +- 0.0107 | 0.612 | -0.35 | inside chance |
| category overlap | new texts (main) | 30 strongest | 0.8686 | 0.8174 +- 0.0411 | 0.099 | +1.25 | 0.8431 +- 0.0397 | 0.328 | +0.64 | inside chance |
| category lift | new texts (main) | 30 strongest | 0.0750 | 0.0725 +- 0.0096 | 0.375 | +0.26 | 0.0734 +- 0.0092 | 0.429 | +0.17 | inside chance |
| vector closeness | new texts (main) | 30 strongest | 0.2575 | 0.2471 +- 0.0153 | 0.258 | +0.69 | 0.2554 +- 0.0127 | 0.452 | +0.17 | inside chance |
| category overlap | Lipi (second) | all labelled | 0.8613 | 0.8627 +- 0.0218 | 0.546 | -0.07 | 0.8598 +- 0.0185 | 0.516 | +0.08 | inside chance |
| category lift | Lipi (second) | all labelled | 0.0886 | 0.0837 +- 0.0120 | 0.336 | +0.41 | 0.0859 +- 0.0116 | 0.351 | +0.23 | inside chance |
| vector closeness | Lipi (second) | all labelled | 0.2640 | 0.2644 +- 0.0103 | 0.525 | -0.04 | 0.2609 +- 0.0089 | 0.351 | +0.35 | inside chance |
| category overlap | Lipi (second) | 30 strongest | 0.8860 | 0.8335 +- 0.0310 | 0.033 | +1.69 | 0.8598 +- 0.0297 | 0.193 | +0.88 | inside chance |
| category lift | Lipi (second) | 30 strongest | 0.0744 | 0.0766 +- 0.0094 | 0.568 | -0.24 | 0.0772 +- 0.0095 | 0.587 | -0.29 | inside chance |
| vector closeness | Lipi (second) | 30 strongest | 0.2639 | 0.2438 +- 0.0113 | 0.045 | +1.78 | 0.2535 +- 0.0085 | 0.107 | +1.22 | inside chance |


### Per-sign: real word against that sign's own shuffles

170 of 184 labelled signs sit in at least 5 weighted objects (Lipi + new texts pooled); the rest are too rare to rank. For each sign: its average fit (see method) under its real word, against the 1000 sense-count-keeping shuffles (where the sign carries other words of its class and band). z is averaged over the three score versions; "beaten" is the share of shuffles its real word beats, averaged over versions (0.5 = chance).

**15 signs whose real word beats its shuffles by the most**

| sign | real word (gloss) | class | objects | senses | z (mean of 3 versions) | share of shuffles beaten |
|---|---|---|---|---|---|---|
| 711 | vaḷḷam (vaḷḷam measure) | PERSONAL | 10 | 9 | +1.33 | 0.73 |
| 064 | pāti (portion) | PERSONAL | 13 | 14 | +1.31 | 0.81 |
| 645 | kar̤añcu (gold weight) | PERSONAL | 21 | 4 | +1.20 | 0.82 |
| 575 | kōṭṭai (great measure) | PERSONAL | 77 | 17 | +0.94 | 0.78 |
| 621 | aṭai (stored) | TITLE | 18 | 25 | +0.90 | 0.78 |
| 034 | nāl (four) | NUM_TALL | 75 | 19 | +0.88 | 0.59 |
| 550 | vāy (gate) | OPEN | 122 | 25 | +0.87 | 0.72 |
| 821 | mañcāṭi (mañcāṭi weight) | PERSONAL | 12 | 5 | +0.86 | 0.73 |
| 413 | nel (grain) | PERSONAL | 38 | 17 | +0.85 | 0.71 |
| 890 | koṭu (given) | PERSONAL | 13 | 25 | +0.85 | 0.72 |
| 703 | maṉai (house-site) | PERSONAL | 14 | 25 | +0.83 | 0.67 |
| 140 | ammai (lady) | CREST | 126 | 25 | +0.83 | 0.76 |
| 717 | aṭi (servant) | PERSONAL | 70 | 25 | +0.83 | 0.76 |
| 255 | mutal (chief) | PERSONAL | 131 | 25 | +0.74 | 0.78 |
| 817 | kāṇi (share) | OPEN | 192 | 10 | +0.73 | 0.78 |

**15 signs whose real word beats its shuffles by the least (most negative)**

| sign | real word (gloss) | class | objects | senses | z (mean of 3 versions) | share of shuffles beaten |
|---|---|---|---|---|---|---|
| 005 | ai (five) | NUM_SHORT | 48 | 1 | -1.13 | 0.15 |
| 920 | tiṅkaḷ? (month) | OPEN | 171 | 4 | -1.01 | 0.08 |
| 243 | kayal (Carp) | CREST | 19 | 5 | -0.92 | 0.22 |
| 440 | koḷ (received) | PERSONAL | 55 | 25 | -0.92 | 0.22 |
| 231 | orumīn (First-star) | CREST | 106 | 1 | -0.90 | 0.22 |
| 097 | aṭimai (bondsman) | PERSONAL | 24 | 14 | -0.89 | 0.27 |
| 592 | paṭṭi (pen) | PERSONAL | 9 | 25 | -0.89 | 0.21 |
| 838 | viḷai (produce) | PERSONAL | 20 | 25 | -0.87 | 0.21 |
| 565 | maṟavaṉ (warrior) | TITLE | 13 | 10 | -0.84 | 0.20 |
| 408 | kiḷai (lot) | MEASURE | 10 | 25 | -0.74 | 0.27 |
| 927 | irutiṅkaḷ (two months) | PERSONAL | 10 | 1 | -0.72 | 0.19 |
| 900 | tiṅkaḷ (month) | PLACE | 111 | 4 | -0.72 | 0.26 |
| 336 | ūr (town) | PERSONAL | 12 | 25 | -0.71 | 0.30 |
| 405 | nūl (thread) | THING | 129 | 13 | -0.71 | 0.19 |
| 806 | viḷai (produce) | CREST | 143 | 25 | -0.71 | 0.26 |

Spread of z over the 170 signs: mean -0.01, share with z above 0: 0.47, share with z above 2: 0.00, below -2: 0.00. A sign list with no signal would give a mean near 0 and about 2.5% beyond +2 and 2.5% beyond -2 by chance alone.


### Mass run (every candidate word of the pool tried in place of each sign's label, new texts)

rank percentile: 1.0 = the real label is the best candidate, 0.5 = middle (chance), 0.0 = worst. "scrambled" = the same search on new texts where which signs sit together has been destroyed (every sign occurrence dealt out again at random, same text lengths and sign totals; mean of 10 scrambles). Ties share places.

| score | pool | candidates per sign | signs | real: mean percentile | scrambled: mean percentile | real: first place | chance first | scrambled first | real: top 10% | chance | scrambled top 10% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| category overlap | class | 36 (all candidates) | 108 | 0.448 | 0.496 | 0.093 | 0.111 | 0.103 | 0.123 | 0.169 | 0.157 |
| category overlap | class | 12 (candidates within 3 senses of the real word) | 108 | 0.405 | 0.444 | 0.277 | 0.297 | 0.278 | 0.296 | 0.323 | 0.307 |
| category overlap | all | 119 (all candidates) | 108 | 0.471 | 0.507 | 0.004 | 0.008 | 0.005 | 0.072 | 0.101 | 0.095 |
| category overlap | all | 37 (candidates within 3 senses of the real word) | 108 | 0.464 | 0.498 | 0.015 | 0.035 | 0.040 | 0.079 | 0.117 | 0.117 |
| category lift | class | 36 (all candidates) | 108 | 0.481 | 0.480 | 0.079 | 0.111 | 0.093 | 0.128 | 0.169 | 0.134 |
| category lift | class | 12 (candidates within 3 senses of the real word) | 108 | 0.430 | 0.431 | 0.272 | 0.297 | 0.279 | 0.301 | 0.323 | 0.304 |
| category lift | all | 119 (all candidates) | 108 | 0.501 | 0.485 | 0.003 | 0.008 | 0.005 | 0.068 | 0.101 | 0.068 |
| category lift | all | 37 (candidates within 3 senses of the real word) | 108 | 0.490 | 0.478 | 0.030 | 0.035 | 0.028 | 0.080 | 0.117 | 0.080 |
| vector closeness | class | 36 (all candidates) | 108 | 0.493 | 0.506 | 0.102 | 0.111 | 0.111 | 0.148 | 0.169 | 0.171 |
| vector closeness | class | 12 (candidates within 3 senses of the real word) | 108 | 0.451 | 0.492 | 0.259 | 0.297 | 0.326 | 0.287 | 0.323 | 0.356 |
| vector closeness | all | 119 (all candidates) | 108 | 0.501 | 0.517 | 0.000 | 0.008 | 0.008 | 0.065 | 0.101 | 0.093 |
| vector closeness | all | 37 (candidates within 3 senses of the real word) | 108 | 0.518 | 0.528 | 0.019 | 0.035 | 0.026 | 0.083 | 0.117 | 0.110 |


Where the scramble keeps sign order out of it: the scores ignore sign order entirely (a text is a bag of signs), so "scrambling order inside each text" would change nothing. The luck baseline therefore scrambles which signs sit together (every sign occurrence of the new texts dealt out again at random; same text lengths and sign totals), 10 times. The candidate pool of each sign = the words of the labelled signs of its job class (also tried: all 119 words), not the whole dictionary.

### Control (English sentences, WordNet senses)

1519 sentences (1243 with 4 or fewer content words), 1122 words, 1000 shuffles of each kind.

| score | sentences | real | A: chance | A: P | A: z | B: chance | B: P | B: z |
|---|---|---|---|---|---|---|---|---|
| category overlap | all | 0.7599 | 0.7268 +- 0.0128 | 0.005 | +2.58 | 0.7465 +- 0.0084 | 0.052 | +1.59 |
| category lift | all | 0.0721 | 0.0642 +- 0.0026 | 0.004 | +3.08 | 0.0666 +- 0.0024 | 0.015 | +2.30 |
| vector closeness | all | 0.2085 | 0.1580 +- 0.0028 | 0.001 | +18.10 | 0.1686 +- 0.0024 | 0.001 | +16.83 |
| category overlap | 4 words or fewer | 0.7674 | 0.7332 +- 0.0144 | 0.010 | +2.38 | 0.7535 +- 0.0096 | 0.074 | +1.44 |
| category lift | 4 words or fewer | 0.0739 | 0.0646 +- 0.0028 | 0.003 | +3.25 | 0.0674 +- 0.0027 | 0.012 | +2.38 |
| vector closeness | 4 words or fewer | 0.2189 | 0.1643 +- 0.0033 | 0.001 | +16.67 | 0.1755 +- 0.0028 | 0.001 | +15.49 |
Control details: units are English words (reduced to base form, stop words dropped, words found in at least 2 sentences, so a swap means something); job class = part of speech, band = tercile of sentence count; lift learned on the other random half of the sentences; a word's senses are its first 8 WordNet senses.

## Next

- **Full-dictionary table.** After the same cleaning, the Tamil dictionary files hold: DEDR Tamil 34,312 sense phrases (14,851 distinct) over 9,350 words; Wiktionary Tamil 43,693 (22,779 distinct) over 10,240 words. Together about 78,000 phrases and at most 37,600 distinct ones (the overlap between the two is not counted). The Malayalam, Kannada and Telugu parts of DEDR add 13,517, 25,274 and 18,340 phrases. The present table holds 1,832 senses (119 words). At the stock speed measured here (1,597 phrases in 130 s) the 37,600 distinct Tamil phrases take roughly 50 minutes; the full mass run over every dictionary sense per sign would use that table directly.
- **Model conversion.** The weights downloaded here are `google/embeddinggemma-2`, the same repository the fast runtime README names, as safetensors (`EmbeddingGemma2Model`), fetched without a licence gate. By the README they convert with `tools/convert_hf_to_gguf.py ... --outtype bf16`. I did not run the conversion or the runtime, so that is untested.
- **Live lead.** Category lift on the label's first few senses is the version that sees something (K=1 to 6, P 0.005 to 0.022 on new texts). Next: rank senses (label glosses first, homonyms from other DEDR entries down-weighted) instead of a flat max, learn lifts from the dictionary-wide sense table rather than 13 hand categories, and re-run the mass run on the first-gloss version where the search has something to find.

## Rerun notes

Scripts that embed or read WordNet ran in a Python environment at `/tmp/senv` (torch CPU, transformers, sentence-transformers, nltk) with the model at `/tmp/hfm/eg2` and the WordNet files at `/tmp/nltk_data/corpora/wordnet` (from nltk_data on GitHub); these live in /tmp and must be recreated to re-embed or rebuild categories. The saved tables (`senses.csv` with categories, `senses_emb.npy`, `control_*`) let `sense_run.py`, `sense_control_run.py`, `sense_onegloss.py` and `sense_report.py` rerun without them (numpy and pandas only).
