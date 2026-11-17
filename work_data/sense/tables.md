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