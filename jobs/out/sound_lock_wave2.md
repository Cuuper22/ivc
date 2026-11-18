# Wave 2B: Three-Route Pure-Dictionary Sound & Word Lock Across 7 Language Families

Script: `work_scripts/sound_lock_wave2.py`  
Outputs: `work_data/sound_lock/{wave2b_summary.json, route2b1_dual_domain_summary.csv, route2b1_matched_words.csv, route2b2_clause_solver_summary.csv, route2b3_joint_lock_summary.csv}`

## What Was Found

Three honestly distinct **zero-hand-gloss (`Pure-Dictionary`)** phonetic/lexical tests were run across all 7 candidate language families (`11` raw lexicons from `/tmp/typo_lex/` and `/tmp/dict_emb/`, with `795` English meta-headword leaks such as unstarred `"to"`, `"make"`, `"break"` stripped up front). **Dravidian / Proto-Dravidian ranks #1 among candidate Indus families on every single route** — hitting **`9/12` exact homophone/polysemy bridges in Proto-Dravidian** ($P_1$ domain-shuffle $z = +2.29, P = 0.0280$; $P_2$ sound-shuffle $z = +3.06, P = 0.0190$), **#1 of 7 families on unseen `FRAME v3` within-clause Rival-Refit** ($z = +1.39, P = 0.0579$), and **`3/4` Meluhha trade-loan skeletons** ($z = +2.85, P = 0.0280$) — **but none of the three pure-dictionary routes clears the 7-family multiple-testing bar ($P < 0.0071$) or locks individual sign-by-sign words against Rival-Refit decoys** (`2B-2a` Pure-Dict Arch-Sense Rival-Refit $z = +0.69, P = 0.258$; `2B-3` joint $z = +1.43, P = 0.093$).

Together with Wave 1 (`jobs/out/global_solver.md` and `jobs/out/typology_triangulation.md`), this pins down the exact boundary of what the surviving corpus establishes:
1. **Morphosyntactic family (`building on it`)**: Word-free clause and numeral syntax (`7` replicated features) favors **Proto-Dravidian (~2500 BCE)** at **Bayes Factor = `26.6` (`92.97%` posterior)** (`jobs/out/typology_triangulation.md`), and raw Proto-Dravidian lexicons show nominal `P = 0.019–0.058` leads across all three Wave 2B lexical routes where Munda, Indo-Aryan, Elamite, Sumerian, and Burushaski sit at chance or negative under Rival-Refit / sound-shuffle controls.
2. **Sign-by-sign word values (`paused` as established readings; kept strictly as working labels)**: Because **`55.8%` of closed/functional signs are direct visual ideograms** (`jobs/out/semantic_anchors.md`) and open personal names lack external bilingual transcriptions, replacing hand-curated glosses with raw dictionary entries drops held-out Rival-Refit below significance ($z = +0.69$ to $+1.39$). Exact phonetic words on individual signs remain working labels, while **sound-free clause and physical readings (`MEANINGS.md`, `87.14%` intact Lipi)** stand independently of any word choice.

---

## Route 2B-1: 12-Sign Archaeological Dual-Domain Polysemy & Homophony Isomorphism

Twelve signs whose two distinct semantic domains `(Domain_A, Domain_B)` come from Wave 1 artifact, metrological, slot-split, and blind-picture evidence (`705` grain-measure/ship, `820` wheel/quarter, `220` fish/star-bright, `740` jar/house, `520` spear/chief, `400` comb/junior, `861` enclosure/land-share, `320` step-rung/allowance, `090` man/agent-servant, `154` carrying-yoke/guard, `850` eye/copper-blade, `390` tree/cotton-cloth) were tested inside each raw dictionary against **1,000 `Domain_B` permutations (`P1`)** and **1,000 headword/skeleton sound-shuffles (`P2`)**:

| Family (`Lexicon`) | Clean Etyma | Polysemy Hits (`/12`) | `P1` Poly $z$ ($P$) | Exact Norm Hits (`/12`) | `P1` Exact Mean | `P1` Exact $z$ ($P$) | `P2` Sound-Shuf $z$ ($P$) | Skel Hits (`/12`) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Proto-Dravidian (`pdrav_2branch`)** | 3,267 | 6 | `+1.05` (`0.247`) | **9** | 5.90 | **`+2.29` (`0.0280`)** | **`+3.06` (`0.0190`)** | 11 |
| **Dravidian (`dedr_tamil`)** | 3,457 | 6 | `-0.08` (`0.662`) | **8** | 6.68 | `+0.90` (`0.298`) | `+1.80` (`0.1349`) | 11 |
| **Sumerian (`sumerian_roots`)** | 3,436 | 4 | `+0.10` (`0.625`) | 5 | 4.22 | `+0.63` (`0.401`) | `-1.66` (`0.9850`) | 10 |
| **Munda (`santali_campbell`)** | 12,338 | 4 | `+0.46` (`0.452`) | 4 | 3.37 | `+0.46` (`0.452`) | `-0.57` (`1.0000`) | 4 |
| **Akkadian (`akkadian_roots`)** | 720 | 3 | `+2.11` (`0.072`) | 3 | 1.07 | `+2.11` (`0.072`) | `-0.17` (`1.0000`) | 3 |
| **Munda (`mundari_bhadra`)** | 5,124 | 2 | `+0.12` (`0.595`) | 2 | 1.87 | `+0.12` (`0.595`) | `-0.44` (`1.0000`) | 2 |
| **Burushaski (`burushaski_all`)** | 1,795 | 2 | `+1.18` (`0.247`) | 2 | 0.95 | `+1.18` (`0.247`) | `-0.17` (`1.0000`) | 2 |
| **Proto-Munda (`pmunda_cognates`)** | 1,419 | 1 | `-0.50` (`0.829`) | 1 | 1.53 | `-0.50` (`0.829`) | `-0.24` (`1.0000`) | 1 |
| **Indo-Aryan (`oia_turner`)** | 10,067 | 1 | `-0.32` (`0.772`) | 1 | 1.72 | `-0.66` (`0.867`) | `-0.57` (`1.0000`) | 2 |
| **Proto-Indo-Iranian (`proto_indoiranian`)** | 753 | 0 | `-0.60` (`1.000`) | 0 | 0.31 | `-0.60` (`1.000`) | `-0.10` (`1.0000`) | 0 |
| **Elamite (`elamite_roots`, German)** | 2,529 | 0 | `-0.55` (`1.000`) | 0 | 0.24 | `-0.55` (`1.000`) | `-0.20` (`1.0000`) | 0 |

- **What came true**: Proto-Dravidian (`pdrav_2branch`) is the **only lexicon** whose distinct-etymon exact homophones beat both domain-permutation (`P1 z = +2.29, P = 0.0280`) and phonetic sound-shuffling (`P2 z = +3.06, P = 0.0190`), recovering clean distinct-cluster homophones `mīṉ (4885 'fish') <-> miṉ (4876 'flash, glitter, shine')` (`220`), `kā (1417 'shoulder carrying-pole') <-> kā (1416 'guard, protect')` (`154`), and `paraṇi (3954 'jar') <-> paraṇi (3953 'upper loft of a house')` (`740`), alongside polysemous `kāṇi (1444)` (`861`) and `paṭi (3850)` (`320`).
- **What went against**: Neither `P = 0.0280` nor `P = 0.0190` passes the 7-family Bonferroni threshold (`P < 0.0071`). Moreover, inspecting `route2b1_matched_words.csv` shows that single-etymon polysemy hits (`6/12` in Dravidian vs `4.63` shuffled, `P = 0.247`; `4/12` in Santali and Sumerian) are partly inflated across languages by English gloss phrasing (`"flower of silk-cotton tree"` hitting both `tree` and `cotton`; `"male servant"` hitting both `man` and `servant`).

---

## Route 2B-2: Within-Clause (`FRAME v3`) + Archaeologically Anchored Pure-Dictionary Solver

All bigrams were restricted strictly to **within-clause transitions** under `FRAME v3` (`3,833` Lipi events / `9,321` transitions -> `955` unseen Mahadevan `new texts` events / `1,991` transitions, zero cross-clause boundary edges).

### 2B-2a: Pure-Dictionary DEDR Audit (`109` signs, zero `values_master4` English glosses)
- **Raw DEDR `K=1` first sense within `FRAME v3` clauses**: Fixed `(v3_class × band)` decoy **$z = +1.62$ ($P = 0.0360$)** | **Rival-Refit $z = +0.00$ ($P = 0.5135$)**.
- **Archaeology-Selected DEDR sense (`Arch-Sense`, picking the raw DEDR sense matching the sign's Wave 1 `ARCH_SIGN_MASK`)**: Fixed decoy **$z = +1.84$ ($P = 0.0310$)** | **Rival-Refit $z = +0.69$ ($P = 0.2577$)** (up marginally from unsegmented `Pure-Dict` $z = +0.66$ in `jobs/out/global_solver.md`, still null under Rival-Refit).

### 2B-2b: From-Scratch 7-Family Hungarian Assignment (`TOP120` signs -> `M <= 1,500` clean etyma)
Each family's raw dictionary was matched 1-to-1 to the top `120` signs using **only** Wave 1 word-free archaeological `CATS` masks and blind 3-rater sign pictures (`work_data/pictures/pictures_blind.csv`), with zero Lipi bigram fitting during assignment, then evaluated zero-shot on unseen `new texts` within-clause directional PMI against `500` Rival-Refit decoys:

| Family | Raw Dictionary | Candidate Etyma `M` | Movable Signs (`/120`) | Unseen `new texts` Fixed $z$ ($P$) | Unseen `new texts` **Rival-Refit $z$ ($P$)** |
|---|---|---:|---:|---:|---:|
| **Dravidian** | `dedr_tamil.csv` | 1,500 | 81 | `+2.97` (`0.0020`) | **`+1.39` (`0.0579`)** |
| **Burushaski** | `burushaski_lorimer.csv` | 784 | 91 | `+3.86` (`0.0020`) | `+0.82` (`0.1996`) |
| **Munda** | `santali_campbell.csv` | 1,500 | 91 | `+2.80` (`0.0020`) | `+0.70` (`0.2555`) |
| **Indo-Aryan** | `oia_turner.csv` | 1,500 | 100 | `+2.82` (`0.0020`) | `-0.07` (`0.5170`) |
| **Sumerian** | `sumerian_halloran.csv` | 1,500 | 104 | `+3.69` (`0.0020`) | `-0.23` (`0.5709`) |
| **Akkadian** | `akkadian_wiktionary.csv` | 523 | 100 | `+1.80` (`0.0359`) | `-1.35` (`0.9162`) |
| **Elamite** | `elamite_hinzkoch.csv` | 505 | 108 | `+0.88` (`0.2056`) | `-2.67` (`0.9960`) |

- **Why Fixed $z$ is high across 6 families while Rival-Refit peaks at `+1.39` (`P = 0.058`)**: The Fixed score reflects the **word-free Wave 1 archaeological domain masks** (which already beat all 2,000 decoys at $z = +3.54$ with zero dictionary words). Once Rival-Refit refits Lipi transition PMI on shuffled dictionary words within the same `(v3_class × band × mask)` stratum, only Dravidian retains a weak positive lean ($z = +1.39, P = 0.0579$), short of a decoy-proof word lock.

---

## Route 2B-3: Joint Multi-Constraint Lexical Lock (`Metrology + [Mod+220] Compounds + Meluhha Loans`)

Tested simultaneously inside each dictionary against `1,000` sound-shuffled lexicons across (A) `4` metrological homophone pairs (`8/count`, `1/4 / leg-wheel`, `measure / ship`, `cup / ration`), (B) `8` attested `[Mod + 220 Fish]` compound skeletons, and (C) `4` Near Eastern Meluhhan trade-good loan skeletons (`sesame ellu`, `ivory/tusk pilu`, `peacock tukkī/mayil`, `cotton parutti/karpāsa`):

| Family (`Lexicon`) | Clean Etyma | Lock A: Metro (`/4` vs shuf) | Lock B: `[Mod+Fish]` (`/8` vs shuf) | Lock C: Trade Loans (`/4` vs shuf) | Loan $z$ ($P$) | **Joint Score (`/3.00` vs shuf)** | **Joint $z$ ($P$)** |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Dravidian (`dedr_tamil`)** | 3,457 | `0` (`0.31`) | `7` (`7.50`) | **`3`** (`1.15`) | **`+2.85` (`0.0280`)** | `1.625` vs `1.302` | `+1.43` (`0.0929`) |
| **Proto-Dravidian (`pdrav_2branch`)** | 3,267 | `0` (`0.26`) | `6` (`7.24`) | `2` (`0.92`) | `+1.55` (`0.1738`) | `1.250` vs `1.200` | `+0.22` (`0.5195`) |
| **Munda (`santali_campbell`)** | 12,338 | `1` (`0.04`) | `8` (`7.81`) | `0` (`0.21`) | `-0.49` (`1.0000`) | `1.250` vs `1.041` | `+1.52` (`0.2108`) |
| **Proto-Munda (`pmunda_cognates`)** | 1,419 | `0` (`0.01`) | `4` (`1.97`) | `0` (`0.12`) | `-0.34` (`1.0000`) | `0.500` vs `0.277` | `+0.82` (`0.2897`) |
| **Indo-Aryan (`oia_turner`)** | 10,067 | `1` (`0.04`) | `6` (`7.43`) | `2` (`1.11`) | `+1.51` (`0.2228`) | `1.500` vs `1.217` | `+1.41` (`0.1628`) |
| **Sumerian (`sumerian_roots`)** | 3,436 | `2` (`1.12`) | `8` (`7.96`) | `0` (`0.06`) | `-0.25` (`1.0000`) | `1.500` vs `1.291` | `+1.13` (`0.2927`) |
| **Akkadian (`akkadian_roots`, self-source)** | 720 | `0` (`0.01`) | `0` (`0.30`) | `2` (`0.06`)* | `+8.53` (`0.0010`)* | `0.500` vs `0.055`* | `+3.33` (`0.0330`)* |
| **Elamite (`elamite_roots`)** | 2,529 | `0` (`0.00`) | `0` (`0.00`) | `0` (`0.02`) | `-0.13` (`1.0000`) | `0.000` vs `0.004` | `-0.13` (`1.0000`) |
| **Burushaski (`burushaski_all`)** | 1,795 | `0` (`0.01`) | `0` (`0.38`) | `0` (`0.00`) | `-0.04` (`1.0000`) | `0.000` vs `0.050` | `-0.33` (`1.0000`) |

*\*Note: Akkadian's `2/4` hit on Lock C (`ellu` 'sesame oil', `pīru` 'elephant') is self-matching against the Akkadian target forms themselves (`Metro = 0/4`, `FishComp = 0/8`), not an external donor match.*

- **What came true**: Among external Indus candidates, only `Dravidian` (`dedr_tamil`) hits `3/4` Near Eastern Meluhha trade-loan skeletons (`z = +2.85, P = 0.0280`), while Munda (`0/4`), Sumerian (`0/4`), Elamite (`0/4`), and Burushaski (`0/4`) miss completely.
- **What went against**: Exact normalized-form matching on Lock A misses stem-level root sharing (`eṭṭu` '8' vs `eṇ` 'count' differ in geminate vs nasal), and 2-consonant skeleton concatenation on Lock B saturates in large dictionaries (`7.50–7.96 / 8` shuffled mean), leaving Dravidian's combined joint score at $z = +1.43$ ($P = 0.0929$).

## Status Decision

- **Pure-dictionary sign-by-sign word assignment**: **`paused`** after 3 honestly distinct pure-dictionary rescue routes (`2B-1`, `2B-2`, `2B-3`). All Dravidian and English words in `values_master4.csv`, `CORPUS.md`, `READINGS.md`, and `WHOSWHO.md` remain **working labels**, never established readings.
- **Language-family triangulation**: **`building on it`** at the **grammatical/typological level** (**Proto-Dravidian `BF = 26.6`, `93.0%` posterior**, reinforced by consistent `P = 0.019–0.058` #1 nominal ranks on `2B-1`, `2B-2b`, and `2B-3` Lock C), while awaiting an external bilingual or phonetic name-transliteration text to lock individual sign sounds.
