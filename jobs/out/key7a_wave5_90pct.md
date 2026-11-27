# Key #7A — Wave-5 Strike Past 90% Combined Intact / 93% Unseen Holdout

**Headline win:** Locking **64 new signs** (**26 direct promotions + 38 verified Key #4D Pure/Workshop allograph cascades**, `163 -> 227` locked signs) drives **combined intact coverage (`4,163` faces, `15,203` tokens) straight past 90% — from 85.92% to 90.42% (+4.50%)**, with **2,985 intact faces (71.70%, +439 faces; 1,685 multi-sign `len >= 3`, +353)** now glossed sign by sign. On held-out **unseen `new texts` (`563` faces, `1,994` tokens)**, coverage surges from **88.31% to 93.98% (+5.67%)** — **468 of 563 (83.13%) unseen intact faces are now 100%-glossed (+88 faces, +59 multi-sign `len >= 3`)**, and even excluding the two phonetic-open structural locks (`692`, `070`), pure phonetic/metrology/operator/4D locks (`224` signs) hit **93.18% unseen** (`89.71%` combined intact).

**Fifth consecutive independent Proto-Dravidian win (strictly 0% overlap with Waves 1–4, 5,000 exact cluster-preserving shuffles):** Programmatically verified `Wave-5 Fresh (27) ∩ (Wave-1 ∪ Wave-2 ∪ Wave-3 ∪ Wave-4 ∪ Lex163 ∪ CarryOver17) == ∅`. On these 27 untouched long-tail signs, **raw uncleaned 2-branch Proto-Dravidian (`pdrav_2branch`, Single-Headword-Only)** scores **10/27 exact-consonant rebus hits** (`null 4.65`, `Z = +2.82`, **`P = 0.00760`**) and **14/27 stem hits** (`null 9.48`, `Z = +2.00`, **`P = 0.04239`**); cleaned `pdrav_2branch_fixed` replicates **10/27 `PhonEx`** (`null 5.62`, `Z = +2.15`, **`P = 0.03399`**). **All 6 rival language families collapse to 0/27 or 1/27 on `PhonEx`** (`Indo-Aryan 0/27`, `Munda 0/27`, `Elamite 0/27`, `Akkadian 0/27`, `Burushaski 0/27`, `Sumerian 1/27, Z = -0.86, P = 0.90302`).

**Key #7D photo-audit integration & holdout breakthroughs:** Direct carved-stone photograph corrections (`work_data/key7d/photo_audit_holdouts.csv`) unlocked **9 carried-over Key #6A holds/nulls** — **`621`** (`*aṟai / *paṭi`, Fixed & Raw `PhonEx` on 3-compartment chamber, +10 unseen tokens), **`297`** (10-sign nested-chevron `<<<` cluster, `cosR = 0.9773` vs `820 *kāl`, Rank 1/215, `P = 0.00020`), **`527`** (`550/555/554 *nāṭu -> 527/526`, `P = 2.53e-96`, unseen `P = 1.72e-07`, cascades `526`), **`585`** (`*paḷḷi / *kuṭai`, Harappa Mound AB + `017->585` `P = 2.72e-51`), **`095`** (`*āḷ-[BATON]`, `P = 7.18e-26`), **`384`** (`*āku / *takaṭu`, MD ctab + double `DIRECT`), **`243`** (`*katir-mīṉ-vari`, hatching jumps `615/617` from `0/292` to `8/14`, `P = 1.73e-12`, unseen `P = 6.32e-04`), plus structural locks **`692`** (`[PRECINCT-HEADER]`, `40:0` vs `1:296` paradigm, `P = 2.93e-51`, unseen `100.0%`, `P = 6.13e-09`) and **`070`** (`[ARROW-PRE-VĒḶ]`, barbed arrow `↑` before spear `520 *vēḷ`, `P = 6.45e-18`, cascades `072`). Separately, Track B proved Key #7D's **`824` two-sign conflation** (`824_init` matches `817 *kāṇam` at `cosMean = 0.9907`, Rank 1/216, `P = 0.00020`, vs `824_fin` at `0.0162`) and confirmed veined pipal leaf **`384 -> 388`** as the botanical negative control (`cL - cR = +0.050` vs `+0.489` across 5/5 true hatched pairs, `P = 0.0422`). **21 signs** stay honestly in `testing it` (12) or `null` (9) — including single-formula holds `501`, `321`, `318` — zero coverage padding.

---

## 1. Exact Before / After Coverage (`163 -> 227` Locked Signs)

Computed cleanly by `work_scripts/key7a_wave5_90pct.py` across all four canonical corpus splits (`work_data/key7a/coverage_after_key7a.json`):

| Corpus Split | Faces / Tokens | Before Key #7A (`163` locked) | Key #7A Phon/Met/4D Only (`224`, excl. `692/070`) | **After Key #7A + 4D (`227` locked)** | Delta (`163 -> 227`) | +12 `testing it` Frontier (`239`) |
|---|---|---:|---:|---:|---:|---:|
| **Lipi intact** | `3,600` / `13,209` | `85.56%` (`2,166` 100%, `1,126` len≥3) | `89.19%` (`2,466` 100%, `1,373` len≥3) | **`89.89%`** (`2,517` = `69.92%` 100%, `1,420` len≥3) | **`+4.33%` (`+351` 100%, `+294` len≥3)** | `91.63%` (`2,688` 100%) |
| **Unseen `new texts` intact** | `563` / `1,994` | `88.31%` (`380` 100%, `206` len≥3) | **`93.18%`** (`455` 100%, `253` len≥3) | **`93.98%`** (`468` = **`83.13%`** 100%, `265` len≥3) | **`+5.67%` (`+88` 100%, `+59` len≥3)** | **`95.34%`** (`483` 100%) |
| **Combined intact** | `4,163` / `15,203` | `85.92%` (`2,546` 100%, `1,332` len≥3) | `89.71%` (`2,921` 100%, `1,626` len≥3) | **`90.42%`** (`2,985` = **`71.70%`** 100%, `1,685` len≥3) | **`+4.50%` (`+439` 100%, `+353` len≥3)** | `92.12%` (`3,171` 100%) |
| **Combined all (incl. damaged)** | `6,790` / `23,710` | `77.04%` (`3,046` 100%, `1,475` len≥3) | `80.20%` (`3,457` 100%, `1,783` len≥3) | **`80.85%`** (`3,530` = `51.99%` 100%, `1,847` len≥3) | **`+3.81%` (`+484` 100%, `+372` len≥3)** | `82.33%` (`3,738` 100%) |

Unseen out-of-sample generalization again beats Lipi by **+1.34 percentage points** (`+5.67%` vs `+4.33%`), with **over 83% of all unseen intact faces** now completely glossed sign by sign.

---

## 2. Track A — Wave-5 Strictly Disjoint 7-Family Showdown (`N = 5,000` Shuffles)

### 2A. Pure Wave-5 Disjoint Fresh Set (`K = 27` Untouched Signs, 0% Overlap with Waves 1–4)
All 27 signs pass programmatic `verify_zero_overlap` (EN + DE, 0 shared words, 0 shared 4-char stems) and zero-overlap verification against `W1 ∪ W2 ∪ W3 ∪ W4 ∪ Lex163 ∪ CarryOver17`, Single-Headword-Only (`work_data/key7a/trackA_wave5_disjoint_5000shuf.csv`):

| Language Family | Lexicon (`n_etyma`) | All-27 `PhonEx` (null, `Z`, **`P`**) | All-27 `PhonSt` (null, `Z`, **`P`**) | All-27 `DIRECT` (`P`) |
|---|---:|---:|---:|---:|
| **Proto-Dravidian (Fixed, 2-br)** | `pdrav_2branch_fixed` (`3,411`) | **`10/27`** (`5.62`, `Z=+2.15`, **`0.03399`**) | `14/27` (`10.67`, `Z=+1.44`, `0.11518`) | `9/27` (`0.24035`) |
| **Audit: Dravidian Raw 2-br** | `pdrav_2branch` (`3,256`) | **`10/27`** (`4.65`, `Z=+2.82`, **`0.00760`**) | **`14/27`** (`9.48`, `Z=+2.00`, **`0.04239`**) | `9/27` (`0.17696`) |
| Sumerian | `sumerian_roots` (`3,385`) | `1/27` (`2.23`, `Z=-0.86`, `0.90302`) | `5/27` (`4.22`, `Z=+0.41`, `0.41272`) | `6/27` (`0.16617`) |
| Indo-Aryan | `oia_cognates` (`6,338`) | `0/27` (`0.21`, `Z=-0.46`, `1.00000`) | `0/27` (`0.38`, `Z=-0.63`, `1.00000`) | `2/27` (`0.22875`) |
| Munda | `pmunda_cognates` (`1,417`) | `0/27` (`0.02`, `Z=-0.15`, `1.00000`) | `0/27` (`0.07`, `Z=-0.28`, `1.00000`) | `1/27` (`0.43631`) |
| Elamite | `elamite_roots` (`2,437`) | `0/27` (`0.00`, `Z=-0.06`, `1.00000`) | `0/27` (`0.01`, `Z=-0.11`, `1.00000`) | `0/27` (`1.00000`) |
| Akkadian | `akkadian_roots` (`716`) | `0/27` (`0.01`, `Z=-0.10`, `1.00000`) | `0/27` (`0.02`, `Z=-0.15`, `1.00000`) | `4/27` (`0.01700`) |
| Burushaski | `burushaski_all` (`1,743`) | `0/27` (`0.01`, `Z=-0.10`, `1.00000`) | `0/27` (`0.02`, `Z=-0.14`, `1.00000`) | `1/27` (`0.50170`) |
| *Audit: Dravidian 2-Lang Fixed* | `pdrav_2lang_fixed` (`5,095`) | `12/27` (`7.47`, `Z=+2.12`, `0.03059`) | `16/27` (`13.65`, `Z=+1.05`, `0.20376`) | `11/27` (`0.15517`) |
| *Audit: Dravidian Multi-HW* | `pdrav_2branch_fixed` (`multi`) | `14/27` (`8.76`, `Z=+2.35`, `0.01960`) | `17/27` (`13.84`, `Z=+1.41`, `0.11558`) | `9/27` (`0.24035`) |

All 10 Wave-5 `PhonEx` hits (`890, 167, 137, 636, 605, 484, 391, 422, 347, 336`) pass **both raw uncleaned `pdrav_2branch` and cleaned `pdrav_2branch_fixed`** identically (`10/10`), while the remaining 17 long-tail signs stay honest `0` on `PhonEx`.

### 2B. Strictly Separate Photo-Verified Honest Rescue Audit (`K = 11` Carried-Over Holds/Nulls)
Run completely separately (`work_data/key7a/trackA_rescue11_audit_5000shuf.csv`) using Key #7D's direct photograph descriptions (never contaminating the Wave-5 disjoint statistics):
- Aggregate Rescue-11 is **null overall on `PhonEx`** (`Dravidian 2/11, null 2.21, P = 0.668`; `Sumerian 2/11, P = 0.114`; all other 5 families `0/11`), confirming these 11 holdouts are genuinely hard visual/substrate/structural signs rather than easy rebuses.
- Individual photo-verified wins extracted cleanly: **`621`** (`Fixed & Raw PhonEx DEDR 3850/3849 paṭi` + `DIRECT 322 aṟai`, promoted!), **`585`** (`DIRECT 4018 paḷḷi` + TIER-1 Harappa Mound AB anchor), **`384`** (`DIRECT 141 āku` & `2995 takaṭu` + TIER-1B MD ctab), **`527`** (`DIRECT 5059 meṭṭu` & `683 uḻalai` + `P = 2.53e-96` binding), and **`297`** (`DIRECT 940 oci` + `P = 0.00020` 10-sign cluster lock). `645`'s regex hit (`5264/5266 vari`) was audited and rejected as non-visual noise; `692` remained `0/0/0` phonetically.

---

## 3. Track B — Structural, Grammatical, Hatching, Deconflation & Cluster Proofs (`N = 5,000`)

All Track B results live in `work_data/key7a/trackB_structural_wave5.json`:

### 3A. Grammatical Particle / Postposition & Paradigm Audit (`070` & `692` vs Locked `060`)
| Sign / Class | Combined (`n`) | `Init% / Med% / Fin%` | `H_L / H_R` (`dH = H_R - H_L`) | Unseen New (`n`, `Med%`, `Fin%`, `dH`) | Functional Verdict |
|---|---:|---|---|---|
| **`060` (`*-uḷ/*-iṉ`, ref)** | `196` | `2.6% / 94.4% / 3.1%` | `3.445 / 5.080` (**`+1.635`**) | `n=27`, `70.4%`, `18.5%`, `+0.803` | True right-branching locative postposition |
| **`070` (`↑` barbed arrow)** | `34` | `14.7% / 85.3% / 0.0%` | `3.356 / 3.122` (`-0.234`) | `n=6`, `66.7%`, **`0.0%`**, `+0.792` | **NOT a free postposition — Pre-Spear Modifier** (`070/072 -> 520 *vēḷ`: `18/45 = 40.0%`, `OR = 28.1×`, `P = 6.45e-18`; `070|072` `P = 0.00020`, `6` swaps) |
| **`692` (hollow crossroads)** | `62` | **`74.2%`** `/ 17.7% / 4.8%` | `1.566 / 2.257` (`+0.691`) | `n=10`, `50.0%`, `0.0%`, `-1.292` | **#1 Place/Precinct Header Noun**: `692 -> 060` vs `002` = **`40:0`** vs Weight headers `1:296` (**`99.7%` acc, Fisher `P = 2.93e-51`, shuf `Z = +17.97, P = 0.00020`**); unseen New **`9:0` vs `0:29` (`100.0%` acc, `P = 6.13e-09`, shuf `P = 0.00020`)**! |

### 3B. Cross-Base Horizontal Hatching (`*vari`) 5,000-Shuffle Operator Audit & Botanical Control
Key #7D's photographs revealed that `388` has **diagonal chevron leaf-veins + twin top buds (NOT horizontal hatching)**, instantaneously explaining why `384 -> 388` had near-zero asymmetry (`cL - cR = +0.050`) while **5/5 photo-verified true horizontally hatched pairs** are strongly left-preserving, right-shifting (`mean cL - cR = +0.489` vs null `+0.159`, `Z = +1.69`, **`P = 0.04219`**):

| Pair | True Hatch? | `cosL` | `cosR` | `cL - cR` | Lipi `ctab` / `seal%` | New `ctab` / `seal%` | Register Bifurcation |
|---|---|---:|---:|---:|---|---|---|
| **`590 -> 595`** (chest) | Yes | `0.278` | `0.146` | **`+0.132`** | `4/217 -> 6/47` / `53.5% -> 68.1%` | `0/42 -> 9/25` / `50% -> 40%` | Copper-tablet tax-bundle (`post-num P = 8.55e-16`) |
| **`240 -> 243`** (roofed fish) | Yes | `0.562` | `0.031` | **`+0.531`** | `6/316 -> 0/12` / `57.0% -> 100%` | `1/57 -> 0/8` / `68.4% -> 100%` | **Seal `615/617 (*accu)` jump: `0/292 (0.0%) -> 8/14 (57.1%)`, `P = 1.73e-12`; unseen `0/23 -> 4/6 (66.7%)`, `P = 6.32e-04`!** |
| **`920 -> 924`** (crescent) | Yes | `0.453` | `0.116` | **`+0.337`** | `0/147 -> 0/9` / `70.1% -> 66.7%` | `0/39 -> 0/2` / `76.9% -> 100%` | Overland West-trade seal marker (held for `n = 10`) |
| **`480 -> 484`** (mountain caret) | Yes | `0.711` | `0.065` | **`+0.645`** | `0/42 -> 0/14` / `21.4% -> 57.1%` | `0/6 -> 0/1` / `16.7% -> 0%` | Seal granary header (`484 -> 336/337/338`, `P = 1.25e-16`) |
| **`590 -> 605`** (tall box) | Yes | `0.806` | `0.008` | **`+0.798`** | `4/217 -> 0/13` / `53.5% -> 46.2%` | `0/42 -> 0/3` / `50% -> 66.7%` | Riverine chief box (`605 -> 760`, `P = 7.28e-19`) |
| *`384 -> 388` (veined pipal)* | *No (Key 7D)* | `0.859` | `0.810` | *`+0.050`* | `5/30 -> 3/57` / `60% -> 64.9%` | `0/14 -> 0/13` / `57.1% -> 76.9%` | *Botanical negative control (veined leaf, not hatched)* |

### 3C. Key #7D Photo-Guided `824` Two-Sign Deconflation Proof (`N = 5,000` Shuffles)
Splitting Lipi `824` (`n = 25`) by Key #7D's photograph discovery confirms two completely distinct signs were merged under one catalog ID:
- **`824_init` (`n = 8`, seal-initial `824-002-...`, M267)**: matches locked **`817 *kāṇam`** at **`cosL = 0.9991`, `cosR = 0.9822`, `cosMean = 0.9907` (Rank 1/216, `Z = +3.21`, `P = 0.00020`)** and **`861 *kāṇam`** at **`cosMean = 0.9642` (Rank 2/216, `P = 0.00560`)**.
- **`824_fin` (`n = 17`, tablet-final `413-892-824`, 4-spoked wheel)**: collapses to `cosMean = 0.0162` vs `817` (`P = 0.941`) and `0.1403` vs `861` (`P = 0.850`). Whole-sign `824` stays honestly in `testing it` until split at the corpus ID level.

### 3D. Cluster, Allograph & Bigram Binding Proofs (`N = 5,000` Shuffles & Exact Fisher)
| Proof / Binding Test | Observed | Background | Odds Ratio / Metric | Exact `P` |
|---|---:|---:|---:|---:|
| **`297` 10-sign chevron cluster (`42` tok) vs `820 *kāl`** | `cosR = 0.9773` | Rank `1/215` | `Z = +4.18` | **`0.00020`** |
| **`167` vs `868` post-`*kalam` slot-twin** | `cosL=0.937, cosR=0.995` | Rank `1/215` | `cosMean = 0.966` | **`0.00020`** |
| **`527` vs `526` 4D gate-shutter pair** | `cosL=0.954, cosR=0.998` | Rank `1/215` | `cosMean = 0.976`, `4` swaps | **`0.00020`** |
| **`070` vs `072` 4D barbed-arrow pair** | `cosR=0.844, 6` swaps | Rank `1/215` | `cosMean = 0.683` | **`0.00020`** |
| **`550/555/554 (*nāṭu)` -> `527/526`** | `51/116` (`44.0%`) | `10/10,924` (`0.1%`) | **`856.3×`** (unseen `3/9` vs `0/1422`, `P=1.72e-07`) | **`2.53e-96`** |
| **`467`-cl(8, `*pārai`) -> `806 (*kampu)`** | `29/33` (`87.9%`) | `37/11,007` (`0.3%`) | **`2,149.5×`** (unseen `3/4`, `P=4.58e-07`) | **`9.40e-64`** |
| **`692` -> `060 (*-uḷ/*-iṉ)`** | `40/57` (`70.2%`) | `151/10,983` (`1.4%`) | **`168.8×`** (unseen `9/10=90.0%`, `P=1.92e-16`) | **`4.88e-59`** |
| **`017 (*ēḻ 7)` -> `585 (*paḷḷi)`** | `28/69` (`40.6%`) | `22/10,971` (`0.2%`) | **`339.9×`** | **`2.72e-51`** |
| **`890` (R-bow) -> `892 (*vil` L-bow)** | `15/19` (`79.0%`) | `55/11,021` (`0.5%`) | **`747.7×`** (unseen `7/8=87.5%`, `P=3.79e-14`) | **`8.21e-31`** |
| **`003/033 (*mū 3)` -> `422`-cl(7, `*iṟu/*pāl`)** | `24/572` (`96%` of cl!) | `1/10,468` (`0.0%`) | **`458.4×`** | **`2.10e-30`** |
| **`240 (*katir-mīṉ)` -> `636/639 (*kūṭu)`** | `16/292` (`100%` of cl!) | `0/10,748` (`0.0%`) | **`>999×`** (`636/639->740` `13/16`, `P=1.55e-09`) | **`3.82e-26`** |
| **`095` -> `520 (*vēḷ) / 595 (*mūṭai-vari)`** | `20/27` (`74.1%`) | `300/11,013` (`2.7%`) | **`102.0×`** (`585->095`, `P=6.93e-19`) | **`7.18e-26`** |
| **`510`-cl(3) -> `460 (*kaṇṇi)`** | `12/23` (`52.2%`) | `23/11,017` (`0.2%`) | **`521.5×`** (`cosL(503,510)=0.971`) | **`1.62e-25`** |
| **`704/705/706 (*kalam)` -> `167`** | `14/252` (`100%` non-init) | `0/10,788` (`0.0%`) | **`>999×`** (`705/706->868` `10/10`, `P=2.62e-17`) | **`7.28e-24`** |
| **`{002,741}` -> `048/049 (*[BRACKET]-ēḻ)`** | `19/823` (`90.5%` of cl!) | `1/10,217` (`0.0%`) | **`241.4×`** (`048/049->740` `19/21`, `P=3.52e-15`) | **`5.78e-21`** |
| **`605 (*mūṭai-vari)` -> `760 (*kuruku)`** | `10/13` (`76.9%`) | `91/11,027` (`0.8%`) | **`400.6×`** (`cosL(590,605)=0.806`) | **`7.28e-19`** |
| **`350/354 (*toṭṭi)` -> `297`-cl(10)** | `11/43` (`25.6%`) | `29/10,997` (`0.3%`) | **`130.0×`** (`297-cl->{002,820,060}` `P=1.14e-18`) | **`1.66e-18`** |
| **`347`-cl(5, `*mā` deer) -> `741 (*oru-kuṭi)`** | `11/15` (`73.3%`) | `157/11,025` (`1.4%`) | **`190.4×`** | **`9.44e-18`** |
| **`484/067 (*kō-vari)` -> `336/337/338`** | `7/15` (`46.7%`) | `13/11,025` (`0.1%`) | **`741.2×`** (`336/337/338->740` `P=9.95e-11`) | **`1.25e-16`** |
| **`772`-cl(3) -> `740 (*kuṭi)`** | `19/20` (`95.0%`) | `1,455/11,020` (`13.2%`) | **`124.9×`** (`*mīṉ->772-cl` `P=2.06e-10`) | **`3.84e-16`** |
| **`065` -> `220 (*mīṉ)`** | `10/12` (`83.3%`) | `290/11,028` (`2.6%`) | **`185.1×`** (unseen New `3/3 = 100%`) | **`1.19e-14`** |
| **`391` -> `595 (*mūṭai-vari)`** | `6/7` (`85.7%`) | `41/11,033` (`0.4%`) | **`1,608.6×`** (replicates unseen New) | **`2.98e-14`** |
| **`621` seal-exclusivity & EOS** | `27/28` seals (`96.4%`) | `21/26` EOS (`80.8%`) | **`OR = 25.8×`** (`+` Fixed & Raw `PhonEx 3850/3849`) | **`2.05e-07`** |

---

## 4. All 64 Newly Locked Signs (`building on it`, `163 -> 227`)

### 4A. 26 Direct Promotions (9 Rescued Holds/Nulls + 17 Wave-5 Fresh Locks)
| Sign | M77 | Intact (`L/N`) | Reading (`building on it`) | Lock Lever | Core Evidence |
|---|---|---:|---|---|---|
| **`692`** | M150 | `62` (`52/10`) | **`[PRECINCT-HEADER]`** *(phon. open)* | Track B Structural Place Lock | `40:0` vs `1:296` `060:002` paradigm (`P = 2.93e-51`, shuf `P = 0.00020`); unseen `9:0` vs `0:29` (`100%`, `P = 6.13e-09`). |
| **`585`** | M194 | `52` (`45/7`) | **`*paḷḷi / *kuṭai`** | Rescue TIER-1 + DIRECT + Track B | Key 7D arched pavilion/shrine; TIER-1 Harappa AB (`OR=12.8/27.2`) + `DIR 4018 paḷḷi`; `017->585` `P = 2.72e-51`. |
| **`527`** | M254 | `50` (`47/3`) | **`*uḻalai / *meṭṭu`** (`nāṭu`-gate) | Track B Compound + DIRECT | `550/555/554->527/526` `51/116` (`P = 2.53e-96`, unseen `P = 1.72e-07`), `527|526` `P = 0.00020`, `DIR 5059/683`; cascades `526`. |
| **`384`** | M326 | `38` (`24/14`) | **`*āku / *takaṭu`** | Rescue TIER-1B + Double DIRECT | Plain upright leaf (Key 7D); TIER-1B MD ctab + `DIR 141 āku` ("leaf/plate") & `2995 takaṭu` ("metal plate"). |
| **`070`** | M155 | `34` (`28/6`) | **`[ARROW-PRE-VĒḶ]`** *(phon. open)* | Track B Arrow-Pre-Vēḷ Lock | Key 7D barbed arrow `↑` beside spear `520 *vēḷ` (`18/45 = 40%`, `P = 6.45e-18`), `0.0%` fin, `070|072` `P = 0.00020`; cascades `072`. |
| **`095`** | M18 | `28` (`22/6`) | **`*āḷ-[BATON]`** | Track B Companion (`585+595`) | TIER-1 MD ctab; `585->095` `P = 6.93e-19`, `095->520/595` `20/27` (`P = 7.18e-26`, unseen replicated). |
| **`621`** | M242 | `26` (`16/10`) | **`*aṟai / *paṭi`** | Rescue Photo-7D Rebus Lock | Key 7D 3-compartment chamber: Fixed & Raw `PhonEx 3850/3849 paṭi` + `DIR 322 aṟai`; `96.4%` seals (`P = 2.05e-07`), `80.8%` EOS. |
| **`297`** | M180 | `22` (`12/10`) | **`*kōṇ / *maṭaṅku`** (chevron-share) | Track B 10-Sign Cluster + Photo-7D | Key 7D nested chevrons `<<<`; pooled 10-sign cluster `cosR=0.9773` vs `820 *kāl` (Rank 1/215, `P = 0.00020`), `350->297-cl` `P = 1.66e-18`; cascades 9 twins. |
| **`243`** | M75 | `15` (`9/6`) | **`*katir-mīṉ-vari`** | Track B Hatching Op (`240`) | `240->243` jumps `615/617` binding `0/292 (0%) -> 8/14 (57.1%)` (`P = 1.73e-12`), unseen `0/23 -> 4/6` (`P = 6.32e-04`), `100%` seals. |
| **`890`** | M304 | `19` (`11/8`) | **`*vil`** (right-bow grant) | Wave-5 Rebus + Track B | Raw & Fixed `PhonEx 5422/5421 vil`; TIER-1 Grant/Issue; `890->892` `15/19` (`P = 8.21e-31`), unseen `7/8` (`P = 3.79e-14`). |
| **`510`** | M253 | `19` (`10/9`) | **`*taṭṭam / *mālai-frame`** | Track B Compound (`460`) + DIR | `510-cl->460 (*kaṇṇi)` `12/23` (`P = 1.62e-25`, unseen replicated), `cosL(503,510)=0.971`, `DIR 3035`; cascades `511|513`. |
| **`048`** | M113 | `18` (`18/0`) | **`*[BRACKET]-ēḻ`** (7-bundle) | Track B `side_brackets` (`007`) | Key 4A `side_brackets` on locked `007 *ēḻ` (`cosR=0.747`); `19/21` before `740` (`P = 3.52e-15`) & after `{002,741}` (`P = 5.78e-21`); cascades `049`. |
| **`167`** | M321 | `16` (`16/0`) | **`*mukku / *kuntāṇi`** (`kalam`-unit) | Wave-5 Rebus + Metrology | Raw & Fixed `PhonEx 4895/4899 mukku` + `DIR 1726 kuntāṇi`; 100% Harappa mtab, `14/14` non-init after `704/705/706` (`P = 7.28e-24`). |
| **`636`** | M244 | `15` (`15/0`) | **`*kūṭu`** (M244 granary-var) | Wave-5 Rebus + Track B | Raw & Fixed `PhonEx 1883/1882 kūṭu`; `16/16` after `240` (`P = 3.82e-26`), `13/16` before `740` (`P = 1.55e-09`), `cosR(630)=0.940`; cascades `639`. |
| **`137`** | M40 | `15` (`12/3`) | **`*āḷ / *aḷ`** (ration-man) | Wave-5 Rebus + Track B | Raw & Fixed `PhonEx 399/290 āḷ↔aḷ`; `137/139->400` `8/10` (`P = 1.32e-10`); cascades `139`. |
| **`605`** | M258 | `13` (`11/2`) | **`*mūṭai-vari`** (tall box) | Wave-5 Rebus + Hatching | Raw & Fixed `PhonEx 5263/5266 vari`; `10/13` before `760` (`P = 7.28e-19`, unseen replicated), `cosL(590)=0.806`. |
| **`065`** | M125 | `13` (`10/3`) | **`[STAR-MOD]`** (`220`-prefix) | Track B Pre-Star Lock | `10/12 (83.3%)` non-final immediately precede `220 (*mīṉ)` (`OR = 185.1×, P = 1.19e-14`), unseen `3/3 (100%)`. |
| **`468`** | M178 | `12` (`8/4`) | **`*pārai`** (`806`-plough cl.) | Track B 8-Sign Cluster + DIR | `29/33 (87.9%)` across 8-sign cluster precede `806` (`OR = 2,149.5×, P = 9.40e-64`), unseen `3/4` (`P = 4.58e-07`), `DIR 4093 pārai`; cascades 7 twins. |
| **`484`** | M136 | `12` (`11/1`) | **`*kō-vari`** (hatched peak) | Wave-5 Rebus + Hatching | Raw & Fixed `PhonEx 2178/2177 kō` + `5552/5549 vai`; `cosL(480)=0.711`, `484->337` (`P = 1.25e-16`); cascades `067`. |
| **`906`** | M303 | `12` (`9/3`) | **`*kaṇṭāḷam`** (pack-bale) | Wave-5 TIER-1 + DIRECT | TIER-1 unseen-replicated Clay Package Sealings + exact 2-br `DIR 1174 kaṇṭāḷam` ("double pack-sack/pannier"). |
| **`773`** | M348 | `11` (`8/3`) | **`[MĪṈ-VESSEL]`** (`740`-cl.) | Track B 3-Sign Cluster | `19/20 (95.0%)` across cluster precede `740` (`P = 3.84e-16`, unseen replicated) & `12/20` follow `*mīṉ` (`P = 2.06e-10`); cascades `772|770`. |
| **`336`** | M193 | `10` (`9/1`) | **`*mūṭai / *tompai`** (grain-bin) | Wave-5 Rebus + 4× DIRECT | Raw & Fixed `PhonEx 4927/5037 mūṭai` + 4 `DIR` grain-bin etyma (`1192/1243/3511/4620`); `16/21` before `740` (`P = 9.95e-11`); cascades `337|338`. |
| **`391`** | M163 | `10` (`8/2`) | **`*tai-[ROOF] / *toṇṭu`** | Wave-5 Rebus + `roof_caret_hat` | Raw & Fixed `PhonEx 3496/3549 toṇṭu`; TIER-1 Copper-Implement Smithy + Key 4A `roof_caret_hat(390)`; `391->595` `6/7` (`P = 2.98e-14`, unseen replicated). |
| **`868`** | M275 | `10` (`10/0`) | **`*mukku / *kuntāṇi`** (`kalam`-unit) | Track B Metrology Twin (`167`) | TIER-1B Harappa mtab; `10/10 (100%)` follow `705/706` (`P = 2.62e-17`) & 5,000-shuf twin of `167` (`cosMean=0.966`, Rank 1, `P = 0.00020`). |
| **`422`** | M190 | `9` (`8/1`) | **`*iṟu / *pāl`** (3-comb unit) | Track B 7-Sign Metrology + Wave-5 | `24/25 (96.0%)` across 7-sign cluster follow numeral `3` (`003/033`, `P = 2.10e-30`, unseen replicated) + TIER-1B MD ctab + `PhonEx 418/521`; cascades 6 twins. |
| **`347`** | P303 | `9` (`9/0`) | **`*mā`** (deer / great) | Wave-5 Rebus + 5-Sign Cluster | Raw & Fixed `PhonEx 4780 mā` ("deer/beast") `↔ 4786 mā` ("great"); `11/15 (73.3%)` across cluster precede `741` (`P = 9.44e-18`); cascades 4 twins. |

### 4B. 38 Key #4D Verified Allograph Cascades
- **`297` (9 twins):** PureAllo `293, 295, 298, 300, 301, 304, 305` + WorkshopAllo `291, 299` (`*kōṇ / *maṭaṅku`)
- **`468` (7 twins):** PureAllo `467, 469, 470, 471, 472, 474, 475` (`*pārai`)
- **`422` (6 twins):** PureAllo `421` + WorkshopAllo `423, 426, 427, 429, 430` (`*iṟu / *pāl`)
- **`347` (4 twins):** WorkshopAllo `341, 342, 343, 345` (`*mā`)
- **`336` (2 twins):** PureAllo `337, 338` (`*mūṭai / *tompai`); **`510` (2 twins):** PureAllo `511, 513`; **`773` (2 twins):** PureAllo `770, 772`
- **Single-twin clusters (6):** PureAllo `072` (`070`), `139` (`137`), `067` (`484`), `639` (`636`); WorkshopAllo `049` (`048`), `526` (`527`)

---

## 5. Standout Newly 100%-Glossed Multi-Sign Inscriptions

Key #7A unlocks **+353 new intact `len >= 3` faces (266 unique texts, including +59 unseen `new texts` faces)** (`work_data/key7a/newly_glossed_wave5.csv`):

| Sign Sequence | Corpus (`L/N`) | Newly Unlocked By | Full Sign-by-Sign Reading | Sense / Context |
|---|---:|---|---|---|
| `817-002-048-740` | `L=11, N=0` | `048` | `*kāṇam — *iru — *[BRACKET]-ēḻ — *kuṭi` | Lothal box sealings: "2-*kāṇam*, 7-strand bundle, House" |
| `231-017-585-095-520-032-407` | `L=8, N=0` | `585, 095` | `*uḷ-mīṉ — *ēḻ — *paḷḷi — *āḷ-[BATON] — *vēḷ — *iru — *kōṭi` | 8× copper tablets: "Inner-Star, 7 Citadel-Hall, Baton-Man Chief, 2 *kōṭi*" |
| `347-741-176-740-090` | `L=8, N=0` | `347` | `*mā — *oru-kuṭi — *iṟai/*iru — *kuṭi — *āḷ` | Pure Sangam formula: "Great (*mā*) — First-House — Lord — House-man" |
| `090-090-055-055-002-890-892` | `L=0, N=7` | `890` | `*āḷ — *āḷ — *paṉṉiru — *paṉṉiru — *iru — *vil — *vil` | 7× unseen Kalibangan grant sealings: paired mirror-bow sale grant (`*vil-*vil`) |
| `745-717-095-595-001-142-615-615` | `L=0, N=5` | `095` | `*mū-kuṭi — *aṭi — *āḷ-[BATON] — *mūṭai-vari — *oru — *kōl — *accu — *accu` | 5× unseen 8-sign copper tablets: "3-House base, Baton-Man, 1 taxed-bale, 1 *kōl*, double *accu*" |
| `692-060-255-435-690-740-692-060-803-740` | `L=0, N=2` | `692` | `[PRECINCT] — *-uḷ — *mutal — *tōṭṭi — *kaṭṭu — *kuṭi — [PRECINCT] — *-uḷ — *kampu — *kuṭi` | **10-sign unseen twin-clause inscription:** "In the Precinct: First Watchman Fort-House; In the Precinct: *Kampu*-House" |
| `920-001-235-220-520-692-060-482-740` | `L=0, N=2` | `692` | `*tiṅkaḷ — *oru — *oḷi-mīṉ — *mīṉ — *vēḷ — [PRECINCT] — *-uḷ — *kō — *kuṭi` | **9-sign unseen seal:** "1 Month, Bright-Star Chief, in the Precinct of the King's (*kō*) House" |
| `468-806-158-032-384-142-615-615` | `L=0, N=1` | `468, 384` | `*pārai — *kampu — *kā — *iru — *āku/*takaṭu — *kōl — *accu — *accu` | **8-sign unseen copper tablet** locking both `468` and `384 *takaṭu` |
| `391-595-850-480-001-821` / `...820-820` | `L=3, N=2` | `391` | `*tai-[ROOF] — *mūṭai-vari — *kaṇ — *tūtai — *oru — *iru-kāl` | Copper-smithy tools replicating `821 == 820-820` across Lipi & unseen New! |
| `070-615-615-002-240-555-527` | `L=0, N=1` | `070, 527` | `[ARROW-PRE-VĒḶ] — *accu — *accu — *iru — *katir-mīṉ — *nāṭu — *uḻalai/*meṭṭu` | Unseen 7-sign seal unlocking both `070` and `555-527` (`*nāṭu-meṭṭu`) |
| `220-440-615-741-243-615-615` | `L=0, N=1` | `243` | `*mīṉ — *mukku — *accu — *oru-kuṭi — *katir-mīṉ-vari — *accu — *accu` | Unseen 7-sign seal locking hatched `243 *katir-mīṉ-vari` before double `*accu` |
| `171-032-031-240-636-740-400` | `L=3, N=0` | `636` | `*tūṅku — *iru — *oru — *katir-mīṉ — *kūṭu — *kuṭi — *cikka` | Harappa depot ration tablet: "Weight-standard 2-1, Shining-Star Granary (*kūṭu*) House" |
| `255-435-690-740-900-003-422` | `L=3, N=0` | `422` | `*mutal — *tōṭṭi — *kaṭṭu — *kuṭi — *tiṅkaḷ — *mū — *iṟu/*pāl` | MD copper tablet: "First Watchman Fort-House, Month, 3 *iṟu/*pāl* units" |
| `003-900-740-621` | `L=0, N=1` | `621` | `*mū — *tiṅkaḷ — *kuṭi — *aṟai/*paṭi` | Unseen seal: "3-Month House Treasury/Chamber (*aṟai/*paṭi*)" |

---

## 6. Honest Holds, Honest Nulls & Top 15 Remaining Unsolved Frontier

Zero coverage padding — **21 audited signs** remain strictly withheld:
- **12 Honest `testing it` holds:**
  - *Single-formula holds (3):* **`501`** (`30` tok — Key 7D photo twin of `500 *pāy`, 29/30 one Harappa tablet), **`321`** (`15` tok — 14/15 one Hare ctab), **`318`** (`12` tok — 11/12 one Gharial mtab).
  - *Deconflation split hold (1):* **`824`** (`25` tok — proved split `824_init == 817/861` `P = 0.00020` vs `824_fin` 4-wheel; awaits corpus ID split).
  - *Botanical / partial / low-N holds (8):* **`388`** (`44` tok, Key 7D veined pipal leaf, `cosMean=0.834, P=0.0152` vs `384`), **`455`** (`39` tok, winged butterfly/knot, `DIR 4921`), **`877`** (`25` tok), **`679`** (`18` tok, roofed X, `740->679 P=6.14e-15`, `PhonEx=0`), **`382`** (`17` tok, stemmed pipal), **`921`** (`13` tok, `921->070/072 P=7.07e-13`, `DIR 3213`), **`924`** (`10` tok, hatched crescent, `n=10`), **`063`** (`10` tok, fails `061` swap gate).
- **9 Honest `null` (0/0/0 on clean visual-only DEDR):** **`645`** (`27` tok, plain X / tongs), **`190`** (`16` tok, spider/crab), **`315`** (`14` tok, H-portal), **`565`** (`14` tok, X-pincers), **`130`** (`12` tok, pitchfork-man), **`374`** (`11` tok, curved plant), **`371`** (`11` tok, garlic/bulb), **`267`** (`11` tok, bracketed bird), **`853`** (`11` tok, spiked diamond).

**Top 15 remaining unsolved signs after Key #7A** (`work_data/key7a/key7a_summary.json`):
`388 (44), 455 (39), 501 (30), 645 (27), 824 (25), 877 (25), 679 (18), 382 (17), 838 (16), 190 (16), 321 (15), 136 (15), 315 (14), 565 (14), 921 (13)`.

---

## 7. Deliverables on Disk (Reruns Cleanly, Exit 0, Zero Git Commits)
- Script: `work_scripts/key7a_wave5_90pct.py`
- Data directory: `work_data/key7a/`
  - `anatomy_wave5.csv` (`47` audited targets), `sandwiches_163.csv`
  - `trackA_wave5_disjoint_5000shuf.csv` (27 strictly untouched Wave-5 signs, 7 primary families + 3 Dravidian ablations, 5,000 shuffles), `trackA_wave5_per_sign_bridges.csv`
  - `trackA_rescue11_audit_5000shuf.csv` (strictly separate 11-sign Key 7D photo-verified rescue audit, 5,000 shuffles), `trackA_rescue11_per_sign_bridges.csv`
  - `trackB_structural_wave5.json` (`070`/`692` grammar & paradigm, 5-pair hatching operator + `384->388` botanical negative control, `824` deconflation split, `297` 10-sign chevron cluster, `621` seal-final audit, 35 Fisher binding proofs)
  - `promotions_wave5.csv` (`47` decisions), `master_lexicon_after_key7a.csv` (`227` locked signs)
  - `coverage_after_key7a.json`, `newly_glossed_wave5.csv` (`266` unique `len >= 3` texts, `353` faces), `key7a_summary.json`
- Report: `jobs/out/key7a_wave5_90pct.md`
