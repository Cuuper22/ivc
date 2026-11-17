# Are the texts found abroad the same writing system doing the same thing?

Scripts (in `work_scripts/`, run in this order; each has its predictions in its top docstring, written before its first number): `abroad4_common.py` (loaders, the 10-fold home models, matched draws), `abroad4_01_set.py` (the set), `abroad4_02_predict.py` (how predictable), `abroad4_03_where.py` (where the difference sits, signs), `abroad4_04_repeats.py` (repeats, reversed phrases), `abroad4_05_spelling.py` (sound-spelling test), `abroad4_06_internal.py` (what foreign texts share), `abroad4_07_homekind.py` (home round seals and short-horned-bull seals), `abroad4_08_verdict.py` (per object and per shape), `abroad4_09_roundcomp.py` (what round seals are made of), `abroad4_10_roundprofile.py` (does the foreign round-seal make-up explain home round seals), `abroad4_11_twins.py` (identical or one-sign-off twins at home, after `twins.md`). Tables and logs: `work_data/abroad4/`. Date 2026-11-17. No word is attached to any sign: sign numbers, pictures, jobs and findspots only.

## Terms in plain words

- **Foreign set / abroad**: Lipi objects whose region is Persian Gulf, Mesopotamia, Iranian Plateau or Central Asia: 41 objects (the **core**). Beside them, shown separately: 7 round or cylinder seals with site "Unknown" (**unknown-site round seals**; no findspot but the overseas shape) and 9 West-Asian lines of the second catalogue with no Lipi partner (**second-catalogue-only**; two of them are probably the same seals as Lipi 3882.1 and 3898.1, read differently). **Home**: Lipi objects from the Indus region (3,437 distinct home texts). Left out of both: Lipi region "Other" squares and tablets with no site (21 faces), South India (Daimabad, 2).
- **Round seal**: catalogue type SEAL:C (circular) or SEAL:CY (cylinder). **Square seal**: SEAL:S, SEAL, SEAL:R. **Short-horned bull**: symbol Gaur (head low, trough in front).
- **Step**: two neighbouring signs in a text. **Bits per step**: how surprising the second sign of a step is to a model; 1 bit more = twice as hard to guess; lower is more predictable. A lost sign (000), an unclear sign (ALT) or a sign never seen at home cuts the text; only steps between neighbouring usable signs are scored.
- **Sign-pair model**: guesses the next sign from the sign before it, learned from home texts. **Frame v2**: guesses it from the job class of the previous sign (front word, name part, number, closer and so on), class rules learned per object kind. **Unigram**: guesses from sign frequencies alone. **Pair gain** = unigram bits minus sign-pair bits: how much the order rules help; negative = the order rules make the guess worse than frequencies alone.
- **Cross-fitted**: home texts are split into 10 folds; each home text is scored by a model that never saw it; each foreign text is scored by all 10 models and averaged. No text is scored by a model trained on it.
- **Matched home texts / 2,000 draws**: for each foreign text, a random home distinct text with the same object kind, the same number of steps and (for seals) the same animal group; repeated 2,000 times. "Control mean [a, b]" is the average over draws and the range holding 95% of draws. **P** = share of draws at least as extreme as the real value (smallest possible 0.0005). A small P means chance matching does not give the foreign value.
- **Home phrase**: one of the 136 fixed phrases of `jobs/out/phrases.md` (2 to 4 signs side by side, in one order).
- **Intact text**: complete, no lost or unclear sign, so both edges can be scored.

## What was found

1. **Round seals abroad are a different kind of text; square seals abroad are home texts.** Sign-pair bits per step against matched home texts: round seals 9.52 against 5.74 [4.75, 6.84] (+3.79 bits, P 0.0005; 15 scorable texts, 51 steps); square seals 6.58 against 6.03 [4.73, 7.41] (+0.54, P 0.20; 11 texts, 34 steps). Frame v2 says the same: round 8.97 against 6.58 (+2.39), square 6.83 against 6.63 (+0.20, P 0.35). For round seals the order rules are worse than useless: unigram 8.32 against sign-pair 9.52 (pair gain -1.2; matched home texts +1.5). What it means: the sign-to-sign habits of the home script predict the square seals found abroad almost as well as home seals, and predict the round seals worse than guessing by frequency. What it opens: the question "same system?" splits by object shape, and the round seals are the object to explain.
2. **The split follows the round shape, not the place and not the animal.** Home round seals (15 faces; 10 have a scorable step) cost 8.15 against 5.68 [4.43, 7.12] (P 0.0005), as foreign as the foreign round ones (9.52). Home short-horned-bull seals (87 faces; 79 texts) cost 5.79 against 5.66 [5.22, 6.12] (P 0.28), square ones 5.68 against 5.66: like any home seal. Of the 14 short-horned-bull seals abroad, 13 are round. It points toward: the overseas animal is a passenger; the round seal is the carrier of the odd text, wherever it lies (a Mohenjo-daro round seal reads like an Ur one). It opens the 15 home round seals as a held-out check on any reading of the foreign ones.
3. **Home phrases are almost absent on round seals and present in home order on square seals.** Objects holding a home phrase: 6 of 41 against 14.0 for matched home texts (2.5th percentile 10, P 0.0005); round seals 1 of 18 against 8.4 (P 0.0005); square seals 4 of 15 against 4.7 (P 0.44); other objects 1 of 8 against 0.9. Phrase matches in home order: 12 on the 41 against 2.33 when the signs inside each text are shuffled (P 0.001); 8 of the 12 are on the 15 square seals (shuffled 1.32), 1 on the 18 round seals (shuffled 0.56). Reversed: 1 against 2.30 shuffled (P of more 0.91). What it means: where phrases are present abroad they are in the home order; the earlier "order reversed abroad" lead (7 against 5) is not there with the 136 phrases. The matches: Kish 1971.1 and Gonur 4155.1 both carry `590-390-740` (the name that sits on 14 home seals), Tell Umma 3884.1 and Salut 4173.1 carry `002-004`, Nindowari-damb 3858.1 carries `760-740`, Karzakan 5227.1 `455-220`, Kish 1971.1 also `003-220`, Gonur `002-235`. One reversal: Ur 3898.1 reads `004-002`.
4. **The oddness sits in the ending and the middle of round seals; the front is odd only through 091.** Intact texts only, sign-pair bits (foreign against matched home): all 19 intact, front sign 9.04 against 8.03 (+1.01, P 0.056), middle steps 8.12 against 6.28 (+1.85, P 0.002), last step 7.12 against 5.08 (+2.04, P 0.006), end-of-text event 2.06 against 1.40 (+0.66, P 0.012). Round seals (8 intact): front +2.08, middle +3.78, last +4.86, end +2.40 bits (all P 0.012 or less). Square seals (8 intact): front -0.64, middle -1.23, last +0.77, end -0.62 (none significant). Jobs: of 9 intact round seals 0 end in a closer or after-jar title against 6.3 for matched home texts (P below 0.001); 5 of 8 intact square seals do (home 4.1). Four of the 9 intact round seals start with a front-word-class sign (home 2.2), but all four start with 091 (twin men), which frame v2 files among the front words.
5. **Signs: the jar is halved, the man and stroke signs are over-used, nothing of the fish or front words is significantly missing.** Tokens of real signs in the 41: 142. Jar 740: 7 against 14.1 expected in matched home texts (P 0.0045); closer class 6.3% against 12.8% (P 0.001). Over-used abroad (matched home expectation in brackets): man 090 7 (0.78), twin men 091 5 (0.02), plain fish 220 8 (2.25), four strokes 004 5 (0.56), single stroke 001 6 (2.05), 055 5 (1.5), 924 2 (0.07), 093 2 (0.09), 095 2 (0.09); the after-jar titles 400 and 090 together 8 against 2.3 (P 0.0015). Not significant: front words 861 / 817 / 820 (0 / 2 / 1 against 2.4 / 1.6 / 1.9), marked fish crests 231 / 233 / 235 / 240 (0 / 0 / 1 / 1 against 0.8 / 2.4 / 3.6 / 3.6; P 0.07 to 0.09 each), the fish group as a whole (10 against 12.7), count strokes as a class (21 against 18.3). Of 23 signs tested for under-use only the jar is below its draws at P 0.05.
6. **Round seals are built from person signs and strokes, from a small stock, with no order rule.** 25 round seals (18 core + 7 unknown-site): 99 signs, 53 distinct. Person signs (090, 091, 093, 095) make 18.2% of their signs against 0.4% in matched home seals; stroke signs 30.3% against 17.8%; together 48.5% against 18.3% (P 0.0005 each). The 8 commonest signs cover 45.5% of tokens against 35.6% (P 0.0045). The commonest: 090 (10 seals), 001 (9), 091 (6), 055 (6), 031 (4), 220 (4). At home the 15 round seals do not share this make-up: person signs 3.6% of their signs (2 of 56), strokes 28.6%.
7. **Signs found only abroad are three.** 026 (Nindowari-damb 3858.1; three rows of slanted short strokes), 340 (Ur 3897.1; a deer facing right), 725 (unknown-site round seal 5226.1; no entry in the shape table). 2 of 142 core tokens are never-seen-at-home signs (home expectation 5.0, P lower 0.07). Rare-at-home signs (under 5 home uses, own text left out) are 12.7% of core tokens against 10.3% (P 0.15); on round seals 13.7% against 8.9% (P 0.054). Signs abroad with very few home uses: 091 (11), 093 (5), 924 (6), 095 (20), 831 (14).
8. **The sound-spelling signature is not there.** Three measures fixed in advance (`abroad4_05_spelling.py`), spelling direction in brackets. M1 flatness, entropy of pooled sign counts, bits [higher]: round seals (25) 5.25 against home 5.56 (P of higher 0.98: the round seals are LESS flat); square 5.04 against 5.14; all 41 5.87 against 5.93. M2 class regularity, frame-v2 gain over frequencies [smaller]: round -0.70 against +0.55 (P 0.0005), square +0.09 against +0.59 (P 0.035), all 41 -0.34 against +0.57. M3 share of texts (3+ signs) with a sign repeated [higher]: round 2 of 19 = 0.11 against 0.01 (P 0.02), all 41 1 of 23 against 0.04 (P 0.64). Verdict: only M2 meets the spelling direction, and the drop goes below zero (the order is anti-regular for the home rules), which a flat syllable string would not give; M1 goes the other way.

## Tables

### Table 1. The set (step 1; `foreign_set.csv`)

How the rows were chosen: core = the Lipi `region` column is Persian Gulf (16), Mesopotamia (11), Iranian Plateau (11) or Central Asia (3), which covers Ur, Kish, Nippur, Girsu, Tello, Tell Umma, Susa, Luristan, Tepe Yahya, Miri Qalat, Nindowari-damb, Sibri, Ornach, Murda Sang, Failaka, Bahrain (Qala'at), Saar, Karzakan, Janabiyah, Kalba, Hajar, Salut, Ra's al-Junayz, Gonur Depe, Altyn Depe, Shortughai. Unknown-site round seals are added as a second tier because the shape is the overseas shape and the catalogue gives no site. Second-catalogue-only = Mahadevan site code WA with no partner in Lipi. Kind and shape: seal round / square, tablet, pot, tag. Animal and material from the catalogue (blank = none given). "complete": Y yes, N no, ? unclear.

**Core: Lipi region is Gulf, Mesopotamia, Iran or Central Asia (41)**

| id | site | kind / shape | animal | material | complete | text (reading order) |
|---|---|---|---|---|---|---|
| 16.1 | Altyn Depe | seal / square | none | Soft stone | Y | `415-390` |
| 147.1 | Failaka | seal / round | short-horned bull | - | N | `090-000-817-317` |
| 148.1 | Failaka | seal / round | - | - | ? | `716-350-001-090` |
| 160.1 | Hajar | mtab / TAB:I | short-horned bull | - | Y | `117-617` |
| 935.1 | Ra's al-Junayz | seal / square | unicorn | Copper | N | `000` |
| 1970.1 | Kish | seal / square | unicorn | - | N | `240-643-000` |
| 1971.1 | Kish | seal / square | unicorn | - | Y | `416-840-060-003-220-590-390-740` |
| 2153.1 | Luristan | seal / round | short-horned bull | - | Y | `091-840-413-831` |
| 3858.1 | Nindowari-damb | seal / square | unicorn | - | Y | `257-060-026-760-740-066-632-220-817` |
| 3859.1 | Nindowari-damb | seal / square | unicorn | - | Y | `255-798-400` |
| 3860.1 | Nippur | seal / square | zebu | Steatite | N | `000-151` |
| 3863.1 | Qala'at al-Bahrain | seal / round | short-horned bull | Steatite | Y | `190-060-055-090-160` |
| 3864.1 | Ra's al-Junayz | pot / POT:T:g |  | Clay | N | `000-220-029-740` |
| 3865.1 | Ra's al-Junayz | pot / POT:T:g |  | Clay | Y | `004-405` |
| 3866.1 | Ra's al-Junayz | pot / POT:T:g |  | Clay | ? | `517-892-740` |
| 3874.1 | Shortughai | seal / square | rhino | Steatite | Y | `003-426` |
| 3881.1 | Susa | seal / round | short-horned bull | - | N | `000-365-090-407-604-700` |
| 3882.1 | Susa | seal / round | short-horned bull | - | Y | `924-001-319-031-055-002-150-416` |
| 3884.1 | Tell Umma | tag / TAG:L | unicorn | Clay | Y | `127-705-002-004-390` |
| 3885.1 | Tello | seal / square | tiger | - | N | `384-440-390-220-000` |
| 3886.1 | Tepe Yahya | pot / POT:T:s |  | Clay | N | `000-095-002` |
| 3897.1 | Ur | seal / round | short-horned bull | Steatite | Y | `528-220-924-340-093` |
| 3898.1 | Ur | seal / round | short-horned bull | - | Y | `415-803-001-328-004-002` |
| 3899.1 | Ur | seal / round | short-horned bull | - | N | `350-090-004-000-000` |
| 4155.1 | Gonur Depe | seal / square | elephant | Steatite | Y | `285-002-235-220-125-590-390-740` |
| 4173.1 | Salut | seal / square | short-horned bull | - | Y | `595-278-002-004-392` |
| 4174.1 | Salut | tag / TAG | elephant | - | N | `000-921` |
| 5222.1 | Girsu | seal / round | short-horned bull | - | N | `255-013-744-000-740` |
| 5225.1 | Ur | seal / round | - | - | N | `000-090-000-001-000` |
| 5227.1 | Karzakan | seal / round | short-horned bull | - | Y | `091-031-455-220` |
| 5228.1 | Karzakan | seal / round | short-horned bull | - | Y | `091-032-001-033` |
| 5229.1 | Saar | seal / round | none | - | Y | `055-220-091-001-093-031` |
| 5230.1 | Karzakan | seal / round | short-horned bull | - | Y | `ALT` |
| 5231.1 | Ur | seal / round | - | - | ? | `090-405` |
| 5232.1 | Janabiyah | seal / round | short-horned bull | - | Y | `071-031-831-055-121-099-055` |
| 5386.1 | Sibri | seal / square | none | Stone | N | `095-000` |
| 5405.1 | Ornach area | seal / square | zebu | - | N | `820-000-374-000` |
| 5442.1 | Miri Qalat | seal / square | unicorn | Steatite | Y | `742-740` |
| 5444.1 | Miri Qalat | seal / square | goat | Steatite | Y | `013-520` |
| 5551.1 | Kalba | seal / round | none | - | Y | `091` |
| 5556.1 | Murda Sang | pot / POT:T:g | - | - | N | `000` |

**Unknown site, round or cylinder seal (7)**

| id | site | kind / shape | animal | material | complete | text (reading order) |
|---|---|---|---|---|---|---|
| 3887.1 | Unknown | seal / round | other | Steatite | N | `190-091-603-000` |
| 3888.1 | Unknown | seal / round | other | Steatite | N | `032-132-000-055-090` |
| 3889.1 | Unknown | seal / round | short-horned bull | Steatite | Y | `467-550-001-740-740` |
| 5223.1 | Unknown | seal / round | short-horned bull | - | N | `160-384-133-001-090-000` |
| 5224.1 | Unknown | seal / round | short-horned bull | - | N | `000-033-220-001-032-061-000` |
| 5226.1 | Unknown | seal / round | other | - | N | `000-725-090-ALT` |
| 5557.1 | Unknown | seal / round | other | Stone | N | `000-000-139-145` |

**Second catalogue only, West Asia, no partner in Lipi (9)**

| id | site | kind / shape | animal | material | complete | text (reading order) |
|---|---|---|---|---|---|---|
| M9801 | West Asia (Mahadevan) | seal / ? |  | - | True | `416-150-001-055-X185-001-924-X57` |
| M9821 | West Asia (Mahadevan) | seal / ? |  | - | False | `000-240-632-740` |
| M9834 | West Asia (Mahadevan) | seal / ? |  | - | False | `000-243-000` |
| M9842 | West Asia (Mahadevan) | seal / ? |  | - | True | `350-151-320` |
| M9845 | West Asia (Mahadevan) | seal / ? |  | - | True | `X374` |
| M9846 | West Asia (Mahadevan) | seal / ? |  | - | True | `415-803-001-717-015` |
| M9851 | West Asia (Mahadevan) | seal / ? |  | - | True | `388-443-390-176-156` |
| M9902 | West Asia (Mahadevan) | seal / ? |  | - | True | `235-090-090-615-615` |
| M9904 | West Asia (Mahadevan) | seal / ? |  | - | True | `X11-384-X21-X21-X153` |
### Table 2. Predictability (step 2; `predict_summary.csv`, `predict_per_text.csv`)

Bits per step, foreign against matched home texts (control mean, with the range holding 95% of the 2,000 draws). Home pool for scale: 5.70 (sign pair), 6.50 (frame v2), 7.10 (unigram) per step.

| group | texts / steps | sign pair: real vs control [95% range] | diff | P real higher | frame v2: real vs control | diff | unigram: real vs control |
|---|---|---|---|---|---|---|---|
| all 41 core | 32 / 96 | 8.14 vs 5.99 [5.24, 6.81] | +2.14 | 0.0005 | 7.98 vs 6.66 | +1.32 | 7.63 vs 7.23 |
| core round seals | 15 / 51 | 9.52 vs 5.74 [4.75, 6.84] | +3.79 | 0.0005 | 8.97 vs 6.58 | +2.39 | 8.32 vs 7.21 |
| core square seals | 11 / 34 | 6.58 vs 6.03 [4.73, 7.41] | +0.54 | 0.20 | 6.83 vs 6.63 | +0.20 | 6.91 vs 7.22 |
| core non-seals (pots, tags, tablet) | 6 / 11 | 6.51 vs 6.83 [4.74, 9.02] | -0.32 | 0.60 | 6.91 vs 7.00 | -0.09 | 6.68 vs 7.21 |
| Gulf | 12 / 35 | 9.03 vs 6.20 | +2.83 | 0.0005 | 8.69 vs 6.89 | +1.81 | 8.16 vs 7.35 |
| Mesopotamia | 9 / 27 | 7.41 vs 5.86 | +1.55 | 0.013 | 7.88 vs 6.36 | +1.52 | 7.43 vs 7.04 |
| Iran | 8 / 25 | 8.88 vs 5.45 | +3.42 | 0.0005 | 7.96 vs 6.48 | +1.48 | 7.50 vs 7.09 |
| Central Asia | 3 / 9 | 4.77 vs 7.12 | -2.36 | 0.94 | 5.50 vs 7.20 | -1.70 | 6.54 vs 7.71 |
| core + unknown-site round | 38 / 113 | 8.32 vs 6.00 | +2.32 | 0.0005 | 8.11 vs 6.71 | +1.41 | 7.69 vs 7.24 |
| all round seals (core + unknown site) | 21 / 68 | 9.48 vs 5.80 | +3.68 | 0.0005 | 8.95 vs 6.68 | +2.27 | 8.25 vs 7.23 |
| + second-catalogue-only | 44 / 133 | 8.40 vs 5.94 | +2.45 | 0.0005 | 8.17 vs 6.66 | +1.51 | 7.78 vs 7.21 |
| **home** round seals | 9 / 34 | 8.28 vs 6.10 [4.67, 7.69] | +2.18 | 0.0045 | 8.19 vs 6.89 | +1.30 | 8.17 vs 7.37 |

Texts with no scorable step (lost signs, one sign, ALT) are in the object counts but not here: 9 core objects. Central Asia has 3 short texts (two are `415-390` and `003-426`, plus the 8-sign Gonur seal), so its row is not a test.

### Table 3. Where the difference sits on intact texts (step 3; `where_edges.csv`)

Sign-pair bits; foreign against matched intact home texts; "last step" = the step into the final sign; "end" = how surprising it is that the text stops there.

| group | part | foreign | home | diff | P higher |
|---|---|---|---|---|---|
| all intact (19) | front sign | 9.04 | 8.03 | +1.01 | 0.056 |
| | middle steps | 8.12 | 6.28 | +1.85 | 0.002 |
| | last step | 7.12 | 5.08 | +2.04 | 0.006 |
| | end of text | 2.06 | 1.40 | +0.66 | 0.012 |
| round (8) | front | 9.55 | 7.47 | +2.08 | 0.012 |
| | middle | 9.73 | 5.95 | +3.78 | 0.002 |
| | last step | 8.55 | 3.69 | +4.86 | 0.002 |
| | end | 3.44 | 1.04 | +2.40 | 0.002 |
| square (8) | front | 8.17 | 8.81 | -0.64 | 0.72 |
| | middle | 5.65 | 6.88 | -1.23 | 0.91 |
| | last step | 6.47 | 5.70 | +0.77 | 0.26 |
| | end | 0.95 | 1.57 | -0.62 | 0.93 |

### Table 4. Per shape, per object (step 8; `verdict_by_shape.csv`, `verdict_per_object.csv`)

"Percentile" = share of 2,000 matched home texts that cost less than the foreign text (sign-pair bits). Above the 90th: 10% expected if the object were an ordinary home text.

| shape | objects | scorable | above 90th (expected) | above 95th (expected) | holding a home phrase (matched home) |
|---|---|---|---|---|---|
| round seals | 18 | 15 | 8 (1.5) | 7 (0.75) | 1 (8.4) |
| square seals | 15 | 11 | 3 (1.1) | 1 (0.55) | 4 (4.7) |
| pots | 5 | 4 | 0 | 0 | 0 (1.0) |
| tags | 2 | 1 | 0 | 0 | 1 (0.9) |
| tablet (Hajar) | 1 | 1 | 0 | 0 | 0 (0.2) |
| all | 41 | 32 | 11 (3.2) | 8 (1.6) | 6 (14.0) |

Highest percentiles among square seals: Salut 4173.1 (1.00; short-horned bull, `595-278-002-004-392`, which does hold `002-004`), Nindowari-damb 3858.1 and Tello 3885.1 (0.95). Lowest percentiles (most home-like): Gonur Depe 4155.1 (0.08), Kish 1971.1 (0.15), Ra's al-Junayz pot 3865.1 (0.15).

### Table 5. Home seals of the foreign kind (step 7; `homekind_summary.csv`)

Controls: home square seals of the same step count whose animal is not the short-horned bull.

| group | texts | sign pair: real vs control [95% range] | P higher | frame v2: real vs control |
|---|---|---|---|---|
| home round seals | 10 | 8.15 vs 5.68 [4.43, 7.12] | 0.0005 | 8.06 vs 6.43 |
| home round seals without 090 / 091 | 9 | 8.10 vs 5.66 | 0.002 | 7.99 vs 6.42 |
| home short-horned-bull seals, all | 79 | 5.79 vs 5.66 [5.22, 6.12] | 0.28 | 6.66 vs 6.41 |
| home short-horned-bull square seals | 76 | 5.68 vs 5.66 | 0.47 | 6.58 vs 6.43 |
| foreign round seals (same controls) | 15 | 9.52 vs 5.72 | 0.0005 | 8.97 vs 6.46 |
| foreign square seals | 11 | 6.58 vs 5.77 | 0.12 | 6.83 vs 6.49 |

Where the 15 home round seals lie: Mohenjo-daro 8 (area DKE 3, DKG south 3, HRB 1, VSA 1; 53% of them against 61% of all home seals), Harappa 3, Dholavira 1, Chanhu-daro 1, Kalibangan 1, Rakhigarhi 1. The only two in one building are the two faces of one object (2419). The 87 home short-horned-bull seals: Mohenjo-daro 63 (72% against 61% of all home seals; DKG south 25), Harappa 10, Chanhu-daro 4, Dholavira 4, Kalibangan 3, Lothal 2, Nausharo 1; 8 same-building pairs against 9.7 for random seals of the same sites (P 0.65). No port, house or area carries them: they are spread like the other seals. The lead's "12 round seals at home" is 15 faces by catalogue type here; 10 of them have a scorable step.

### Table 6. Repeats, reversed phrases, shared material (steps 4 and 6)

| test | real | control | P / reading |
|---|---|---|---|
| texts (3+ signs) with a repeated sign, core 41 | 1 of 23 | 0.99 matched home | 0.65 |
| same, round seals (core + unknown site) | 2 of 19 | 0.21 | 0.012 (Janabiyah 5232.1 `055` twice; unknown-site 3889.1 `740-740` side by side) |
| same, second-catalogue-only | 2 of 6 | 0.17 | 0.009 (9902 `235-090-090-615-615`) |
| home phrase in home order, 41 core | 12 | 2.33 shuffled | 0.001 |
| home phrase reversed, 41 core | 1 | 2.30 shuffled | more: 0.91 |
| recurring pairs and triples shared by 2+ foreign objects, not home phrases, core 41 | 0 | 1.43 shuffled; 8.0 matched home | fewer than home: 0.023 |
| same, + unknown-site round | 2 (`001-090`: Failaka 148.1 and unknown 5223.1; `055-090`: Bahrain 3863.1 and unknown 3888.1) | 1.95 shuffled; 13.3 home | more than shuffled: 0.60; fewer than home: 0.021 |
| text pairs in the same region sharing such a run | 0 of 290 | region labels shuffled 0.52 | Gulf against Gulf 0 of 120; Mesopotamia 0 of 55; Iran 0 of 55; Central Asia 0 of 3 |
| unordered sign pairs in 2+ round seals (any order, any distance) | 17 | 20.6 matched home | fewer: 0.32 (`001-090` on 3 seals; `031-055` on 3) |
| same, square seals | 8 | 3.0 matched home | `220-390-740`-type name signs |
| leave-one-out: pair model trained on the other round seals only, gain over their frequencies | -0.35 bits/step (71 steps) | +1.06 matched home sets of 25 | fewer: 0.007 |
| exact home twin (same complete text on a home object), intact core texts | 0 of 19 | 1.8 matched home texts have one on another object | fewer: 0.12 |
| near twin (one sign different) | 0 of 19 | about 3 | |

Home reference for repeats (distinct clean home texts with a repeated sign): length 2: 1.2%, 3: 3.3%, 4: 1.9%, 5: 2.2%, 6: 3.4%, 7: 9.7%.

## Which of (a), (b), (c) each kind of foreign text is

- **(a) Ordinary home texts that travelled: the square seals (15), the pots, tags and the tablet.** Square seals: 6.58 against 6.03 bits (P 0.20); 3 of 11 above the 90th percentile (1.1 expected); 4 of 15 hold a home phrase (4.7 expected); phrase matches in home order 8 against 1.3 shuffled; 5 of 8 intact end in a closer or after-jar title (4.1 expected); name signs of home houses reappear (`590-390-740` at Kish and Gonur Depe). They are not copies: no foreign text has an identical or one-sign-off home twin (0 of 19; 1.8 expected for an identical twin). Pots, tags and the tablet: 6.51 against 6.83, 0 of 4 scorable pots above the 90th percentile.
- **(b) Home system with local formulas dropped, names only: nowhere.** Square seals keep their closers (5 of 8 against 4.1) and their front words are at the home rate (0 of 8 against 0.8). The one place with fewer closers is the round seals, and there the whole order is off, not only the formula. Class shares for all 41 show a name-part excess (40.9% against 33.9%, P 0.02), which comes from the round seals.
- **(c) The signs used for something else: the round seals, 18 core + 7 unknown-site, and the 15 round seals at home.** 9.52 against 5.74 bits; worse than frequencies alone (pair gain -1.2); 8 of 15 above the 90th percentile (1.5 expected), 7 above the 95th (0.75); 1 of 18 holds a home phrase (8.4 expected); 0 of 9 intact end in a closer (6.3 expected); half the signs are person signs and strokes (48.5% against 18.3%). It is not sound-spelling (entropy lower, not flatter; repeats few). It is not a second formula either: the round seals share no run of neighbouring signs (0 non-home runs in 41 core; 2 with the unknown-site ones against 13.3 in home samples) and a pair model trained on the other round seals does worse than frequencies (-0.35 against +1.06 for home). What they do share is a small stock of signs in free order: unordered pairs 17 against 20.6 in home samples.

## What went against

Predictions written in the script before each number, and what happened:

- Step 2: frame v2 gap larger than sign-pair gap for round seals: no, smaller (+2.39 against +3.79). Home round seals score like home texts: no, they score foreign (8.28 against 6.10). Redesign taken: score home round seals separately (step 7); they are foreign in kind, which turned into finding 2.
- Step 3: fish crests under-used: not significant (P 0.07 to 0.09 each; group 10 against 12.7). About five signs only abroad: three (026, 340, 725). Rare signs more common abroad: 12.7% against 10.3%, P 0.15 (round seals 13.7% against 8.9%, P 0.054, only suggestive). Front words missing: not significant (0 / 2 / 1 against 2.4 / 1.6 / 1.9). Count strokes over-used on round seals: stroke class 30.3% against 17.8% on round seals, yes.
- Step 4: repeats at least twice the home rate on all foreign texts: no (1 against 0.99); only the round seals, with unknown-site ones added, show it (2 against 0.21, small numbers).
- Step 5: M1 flatter: no, the opposite. Redesign (step 9): concentration in a few signs, 45.5% against 35.6% (P 0.0045): the signature is a small stock, the reverse of a flat spread.
- Step 6: shared runs among foreign texts: none (0 against 1.43 shuffled); Gulf with Gulf sharing: none (0 of 120). Own order rules among round seals: negative. Redesign (unordered pairs): round seals share signs at the home rate (17 against 20.6), so the sharing is of stock, not of order.
- Step 7: foreign round-seal make-up predicting home round seals: no (step 10: half-and-half model 7.70 bits per sign against 7.65 for home frequencies alone; better than 25 random home seals in the mix, 7.84, P 0.003). Home round seals carry strokes (28.6%) but almost no person signs (3.6%), so the home round seals are odd in order and make-up but not by the same signs.
- Step 8: square seals missing closers: no. Round seals 10 of 15 above the 90th: 8 of 15.
- Right as predicted: reversed home phrases not above shuffled; round seals hold no home phrase; short-horned-bull seals at home are ordinary; home round seals scatter over sites with no house repeated.

## Cautions that carry numbers

- 15 and 11 scorable round and square texts (51 and 34 steps): treated as true and growing: the second-catalogue-only lines and unknown-site seals are added in the table and point the same way (round 9.48 against 5.80 with the unknown-site ones; 8.40 against 5.94 on all 44 texts).
- The 136 home phrases were found on all first-catalogue texts including 41 foreign faces; the home matched texts therefore have a small in-sample lift on phrase presence (45.5% of home distinct texts hold one). The foreign round seals sit at 1 of 18 against 8.4, far outside that lift.
- Frame v2 files 091 among the front words; the "4 of 9 round seals begin with a front word" is 091.
- Texts with a sign never seen at home are cut at that sign (only 026, 340 and the unknown-site 725 are such signs, so the cut is small), and ALT (5230.1, `740/740`) is not scored.

## What it opens

- Two populations on foreign shores: home-style square seals bringing home names (`590-390-740` on two seals in two regions), and a round-seal stock of person signs and strokes in free order. The next measure: the round-seal stock against the 53 distinct signs, one sign at a time, by findspot (the six Gulf seals with 091 against Ur, Susa).
- The 15 round seals at home are the held-out test: any reading of the foreign round seals must also fit them, and the make-up test above says it will not fit through the person signs.
- A model for round seals that scores signs as a set (no order) and a set-size habit: tried only as the co-occurrence count here (17 pairs in 25 texts); a set model trained on the 25 foreign plus 15 home round seals with the home round seals held out is the next run.
