# Key #5A — The "Big Six" Bottleneck Strike + Top-15 & T6 Frontier Audit

**Script:** `work_scripts/key5a_big_six_strike.py` (rerunnable, exit 0, exact `N = 5,000` shuffles)  
**Outputs:** `work_data/key5a/` (`anatomy_31_signs.csv`, `sandwiches_t5.csv`, `trackA_7family_5000shuf.csv`, `trackA_per_sign_bridges.csv`, `trackA_sangam_sandwiches.csv`, `trackB_morpheme_table.csv`, `trackB_grammatical_and_doubles.json`, `t6_and_top15_promotions.csv`, `coverage_before_after.json`, `newly_glossed_inscriptions.csv`, `master_lexicon_after_key5a.csv`, `key5a_summary.json`)

---

## Headline Wins

1. **Intact Corpus Coverage Smashes Past 82% (`82.85%` Unseen Holdout):** Promoting **21 direct signs** from the 31 audited bottleneck/T6 targets — plus **5 verified Key 4D allographs** automatically inherited from newly locked parents (`193, 797, 195` from `798`; `436` from `435`; `160` from `161`) — expands the locked lexicon from **`114 -> 140` signs** (`+26`). Combined intact token coverage jumps from **`74.22% -> 82.17%` (`+7.95%`)**, held-out unseen Mahadevan `new texts` jump from **`75.58% -> 82.85%` (`+7.27%`)**, and **100%-decoded multi-sign (`len >= 3`) inscriptions surge by `+397` faces (`725 -> 1,122`, including `+56` unseen New faces and 302 unique newly cracked multi-sign texts up to 12 signs long)**. More than half of all intact Indus inscriptions (**`54.34%` combined / `57.73%` unseen**) are now 100% glossed sign by sign.
2. **Five of the Big Six Cracked (`240, 060, 798, 550, 440` = `774/857` tokens locked):**
   - **`240` (`297` tok, M67 4-ray fish):** `*katir-mīṉ / *cāy-mīṉ` ("rayed/shining star") — `DIRECT DEDR 1193 katir` + `PhonEx 2456/2457 cāy`.
   - **`060` (`196` tok, M123 slanting under-stroke):** `*-uḷ / *-iṉ` (locative-oblique postposition, "in/within/of") — **`94.4%` medial, `dH = +1.635` bits, `0.0%` doubling**, and a **zero-exception unseen paradigm split vs `002`** (`16:0` on place/precinct headers vs `0:29` on weight/share headers, **Fisher `P = 1.546e-12`, `100.0%` unseen accuracy; Lipi `112:6` vs `1:267`, `P = 8.799e-89`**). Unlocks the 7-city office opening **`920-060-741` (`34×`)** = `*tiṅkaḷ — *-uḷ/*-iṉ — *oru-kuṭi` ("In/Of the Month-Office: 1st House").
   - **`798` (`121` tok, M53 pincered shell/crab):** `*toṭu / *iṭukku` ("bound/grasped guild-house") — `PhonEx DEDR 3544 tōṭu <-> 3536 toṭu` + `DIRECT 444 iṭukku`; MD HR elite replication (`L OR = 2.15`, `N OR = 2.37`); triggers Pure 4D cluster `193, 797, 195`.
   - **`550` (`97` tok, M216 pinched hourglass/waist `><`):** `*nāṭu` ("district/precinct/province") — exact 2-branch `PhonEx DEDR 3584 naṭu` ("middle, centre, waist") `<-> 3638 nāṭu` ("country, district, province, locality"); opens **`BOS-550-060` (`27×`)** = `*nāṭu-uḷ` ("In the District/Precinct", cf. Chola *nāṭṭuḷ*).
   - **`440` (`63` tok, M127 sharp right-angle corner `┐`):** `*mukku` ("corner-mark / earthen goblet") — exact 2-branch `PhonEx DEDR 4898 mukku` ("corner, lane, nook") `<-> 4899 mukku` ("earthen vessel, pot, pan, cup"); stamped pre-firing onto pointed-base goblets (`Harappa F Granary`).
   - *(Big Six #5 — `142` (`83` tok) stays honestly in `testing it` as `*maṭṭam / *kōl?`: `55.4%` precede `615/617 *accu` field-plots on Mohenjo-daro copper land-allotment tablets (`L OR = 7.34`, `N OR = 22.41`), but raw DEDR hits only `DIRECT 4660 maṭṭam` with `PhonEx = 0`.)*
3. **7-Family Zero-Overlap 5,000-Shuffle Whitewash (`7/13` vs `0/13` across ALL 6 Rivals):** On the exact 13 core Top-15 lexical signs with **strictly visual-only Domain A** (programmatically verified zero shared words, zero shared 4-char stems, and zero near-synonym leaks in EN & DE, Single-Headword-Only):
   - **Proto-Dravidian (`pdrav_2branch_fixed`):** **`7/13` `PhonEx`** (null `1.22`, **`Z = +5.57, P = 0.00020`** — literal 5,000-shuffle floor), **`8/13` `PhonSt`** (`P = 0.00100`), **`6/12` Strictly-Novel `PhonEx`** (`P = 0.00040`), **`4/10` Unseen-Replicated `PhonEx`** (`P = 0.00860`).
   - **Unedited Raw Proto-Dravidian (`pdrav_2branch`, ZERO parser edits):** **`7/13` `PhonEx`** (null `0.91`, **`Z = +6.70, P = 0.00020`**), **`9/13` `PhonSt`** (`P = 0.00020`), **`6/12` Novel `PhonEx`** (`P = 0.00020`), **`4/10` Unseen-Replicated `PhonEx`** (`P = 0.00360`).
   - **ALL SIX RIVAL FAMILIES (`Munda, Indo-Aryan, Elamite, Sumerian, Akkadian, Burushaski`):** **`0/13` on `PhonEx` AND `0/13` on `PhonSt` (`P = 1.00000` for every single rival!)**.
4. **Three 100% Catalog-Proven Graphic Doubles + Stacked Numeral `013` + Copper-Tax Hatching `845` (`*vari`):**
   - **`617 == 615-615` (`*iru-accu`, `60` tok):** 15 shared `(L,R)` frames & **16 exact full-text matches** against unseen New `615-615` (**Rank `#1/150` signs, `Z = +29.26, P = 0.00020`**).
   - **`821 == 820-820` (`*iru-kāl`, `12` tok):** 5 shared frames & **5 exact full-text matches** (**Rank `#1/150`, `Z = +11.58, P = 0.00020`**; Sangam `TAM82 irukāl`).
   - **`091 == 090-090` (`*iru-āḷ`, `24` tok):** 3 shared frames & **2 exact full-text matches** (**Rank `#1/150`, `P = 0.00020`**).
   - **`013` (`*mū`, stacked short `3`, `44` tok):** `013-840 = 18/37` (**`OR = 195.7×`, Fisher `P = 5.507e-31`**), completing `013(3)–017(7)`.
   - **`845` (`*vari`, hatched `840`, `51` tok):** exact 2-branch `PhonEx DEDR 5263 vari` ("line, streak, stripe, draw") `<-> 5266 vari` ("tax, impost, duty, toll, levy"); shifts copper tablets from **`0/126 -> 29/43` (`P = 2.185e-22`)** on Lipi and **`0/19 -> 3/9` (`P = 0.0256`)** on unseen New! Cracks the 14× recurring 7-sign copper tax tablet **`806-845-061-407-850-900-740`** ("Millet-Tax Quarter — Cloth — Copper — Month-House").
   - **`435` (`*tōṭṭi`, `62` tok):** exact 2-branch `PhonEx DEDR 3547 tōṭṭi` ("elephant hook/goad") `<-> 3546 tōṭṭi` ("attendant, watchman, servant"); `87.1%` bound after `255 *mutal` (`54/62` = `*mutal-tōṭṭi` "First-Attendant", unlocking `255-435-156-400` 10× and `255-435-690-740` 5×).

---

## 1. Track A — Exact 5,000-Shuffle 7-Family Rebus Showdown (13 Core Lexical Signs)

Strictly Single-Headword-Only, zero shared words, zero shared 4-char stems, zero near-synonym leaks between visual-only Domain A and empirical Domain B (EN & DE).

| Family | Etyma | All-13 `PhonEx` (null, Z, P) | All-13 `PhonSt` (null, Z, P) | All-13 `DIR` (null, Z, P) | Novel-12 `PhonEx` (P) | Unseen-Rep `N=10` `PhonEx` (P) |
|---|---:|---:|---:|---:|---:|---:|
| **Dravidian (2-br Fixed)** | **3,411** | **7/13** (1.22, **+5.57**, **0.00020**) | **8/13** (2.73, **+3.80**, **0.00100**) | **6/13** (2.57, +2.79, **0.01220**) | **6/12 (0.00040)** | **4/10 (0.00860)** |
| **Munda** | 1,416 | 0/13 (0.00, -0.06, 1.00000) | 0/13 (0.01, -0.11, 1.00000) | 1/13 (0.30, +1.30, 0.26775) | 0/12 (1.00000) | 0/10 (1.00000) |
| **Indo-Aryan** | 6,338 | 0/13 (0.03, -0.18, 1.00000) | 0/13 (0.06, -0.24, 1.00000) | 1/13 (0.08, +3.48, 0.07658) | 0/12 (1.00000) | 0/10 (1.00000) |
| **Elamite** | 2,437 | 0/13 (0.00, -0.02, 1.00000) | 0/13 (0.00, -0.03, 1.00000) | 1/13 (0.23, +1.78, 0.22276) | 0/12 (1.00000) | 0/10 (1.00000) |
| **Sumerian** | 3,385 | 0/13 (0.44, -0.68, 1.00000) | 0/13 (0.80, -0.94, 1.00000) | 4/13 (1.06, +3.19, 0.01040) | 0/12 (1.00000) | 0/10 (1.00000) |
| **Akkadian** | 716 | 0/13 (0.00, +0.00, 1.00000) | 0/13 (0.00, +0.00, 1.00000) | 0/13 (0.08, -0.29, 1.00000) | 0/12 (1.00000) | 0/10 (1.00000) |
| **Burushaski** | 1,743 | 0/13 (0.00, -0.04, 1.00000) | 0/13 (0.00, -0.07, 1.00000) | 1/13 (0.24, +1.65, 0.22555) | 0/12 (1.00000) | 0/10 (1.00000) |
| *Audit: Dravidian RawPDrav* | 3,256 | **7/13** (0.91, **+6.70**, **0.00020**) | **9/13** (2.14, **+5.29**, **0.00020**) | **6/13** (2.34, +3.05, **0.00600**) | **6/12 (0.00020)** | **4/10 (0.00360)** |
| *Audit: Dravidian 2-Lang* | 5,095 | **8/13** (1.74, **+5.28**, **0.00040**) | **10/13** (3.84, **+4.06**, **0.00040**) | **7/13** (2.93, +3.11, **0.00400**) | **7/12 (0.00080)** | **5/10 (0.00280)** |
| *Audit: Dravidian MultiHW* | 3,411 | **8/13** (2.11, **+4.61**, **0.00020**) | **10/13** (3.95, **+3.95**, **0.00020**) | **6/13** (2.57, +2.79, **0.01220**) | **7/12 (0.00140)** | **5/10 (0.01160)** |

### Audited Track A Bridges (All 7 `PhonEx` Hits)
- **`240` (`M67` 4-ray fish):** `DEDR 2456 cāy` ("incline, slant") `<-> 2457 cāy` ("brilliance, light") + `DIRECT 1193 katir` ("ray, beam; shine, glow, abound").
- **`798` (`M53` crab/shell w/ pincers):** `DEDR 3544 tōṭu` ("shell") `<-> 3536 toṭu` ("bind, tie, build a house") + `DIRECT 444 iṭukku` ("grasp between fingers/pincers").
- **`550` (`M216` hourglass/waist `><`):** `DEDR 3584 naṭu` ("middle, centre, waist") `<-> 3638 nāṭu` ("country, district, province, locality").
- **`440` (`M127` corner/nook `┐`):** `DEDR 4898 mukku` ("corner, lane, nook") `<-> 4899 mukku` ("vessel, pot, pan, cup").
- **`435` (`M130` hooked stave/goad):** `DEDR 3547 tōṭṭi` ("elephant hook/goad, clasp") `<-> 3546 tōṭṭi` ("village watchman, attendant, servant").
- **`845` (`M376` hatched double-leaf):** `DEDR 5263 vari` ("line, streak, stripe, draw") `<-> 5266 vari` ("tax, impost, duty, toll, levy") + `PhonSt 5359 vāram` ("land-share").
- **`416` (`M173` double-stacked pitchfork):** `DEDR 1325 kavar` ("fork, branch, separate") `<-> 1326 kavar` ("seize, grasp, control") + `DIRECT 3370 tuṟai` ("branch, seaport, harbor, ford").

---

## 2. Track B — Grammatical Morpheme Classifier, Catalog Doubles & Hatching Audit

### 2A. Grammatical Lock on `060` (`*-uḷ / *-iṉ`) vs `002` (`*iru`)
Compared to the 16 locked lexical roots (mean `Med = 45.74%`, `dH = H_R - H_L = -0.678 bits`), `060` exhibits the exact closed-class postposition signature of locked linker `002`:
- **`060`**: `Init = 2.6%`, **`Med = 94.4%`**, `Fin = 3.1%`, `Dbl = 0.0%`, `H_L = 3.445 -> H_R = 5.080` (**`dH = +1.635 bits`**), `top3L = 62.8% -> top3R = 30.6%`.
- **`002` (reference linker)**: `Init = 2.2%`, **`Med = 91.2%`**, `Fin = 4.7%`, `Dbl = 0.29%`, `H_L = 4.606 -> H_R = 5.870` (**`dH = +1.265 bits`**), `top3L = 54.1% -> top3R = 23.1%`.

**Complementary Header Paradigm (`060` vs `002`):**

| Header Class | Lipi `060` | Lipi `002` | Unseen New `060` | Unseen New `002` |
|---|---:|---:|---:|---:|
| **Place / Time / Precinct (`920, 692, 550, 201`)** | **112** | 6 | **16** | **0** |
| **Weight / Share (`861, 817, 824, 880`)** | 1 | **267** | **0** | **29** |
| *Dual-meaning `820 *kāl` (quarter-unit & city-quarter)* | *21* | *73* | *3* | *11* |
| **Diagonal Accuracy / Fisher Exact P / 5,000-Shuf P** | **98.19%** | **`P = 8.799e-89` (`0.00020`)** | **100.00%** | **`P = 1.546e-12` (`0.00020`)** |

### 2B. Catalog-Proven Graphic Doubles & Stacked Numeral `013`

| Sign | Equivalence | Lipi Single | Unseen New Pair | Shared `(L,R)` Frames | Exact Full-Text Matches | Rank / 150 Signs | 5,000-Shuf `P` |
|---|---|---:|---:|---:|---:|---:|---:|
| **`617`** | **`615-615` (`*iru-accu`)** | 60 | 55 | **15** (`Z = +12.94`) | **16** (`Z = +29.26`) | **#1 / 150** | **`0.00020`** |
| **`821`** | **`820-820` (`*iru-kāl`)** | 12 | 8 | **5** (`Z = +6.44`) | **5** (`Z = +11.58`) | **#1 / 150** | **`0.00020`** |
| **`091`** | **`090-090` (`*iru-āḷ`)** | 18 | 12 | **3** (`Z = +5.12`) | **2** (`Z = +3.51`) | **#1 / 150** | **`0.00020`** |
| **`013`** | **Stacked short `3` (`*mū`)** | 40 | 4 | `013-840 = 18/37` | `OR = 195.7×` | — | **`P = 5.507e-31`** |

### 2C. Horizontal Hatching (`*vari` Tax/Levy) Copper-Tablet Shift Audit
- **`840 -> 845`**: Lipi `ctab` jumps **`0/126 -> 29/43`** (`P = 2.185e-22`), Unseen New **`0/19 -> 3/9`** (`P = 0.0256`).
- **`590 -> 595`**: Lipi `ctab` jumps **`4/217 -> 6/47`** (`P = 2.827e-03`), Unseen New **`0/42 -> 9/25`** (`P = 4.778e-05`).
- **Honest bifurcation:** `923 -> 924` (`0/9 L, 0/2 N ctab`) and `235 -> 243` (`0/12 L, 0/8 N ctab`, **100% seals**) do NOT shift to copper tablets. Hence `845` locks via its direct `PhonEx 5263/5266 vari` proof, while `595`, `924`, and `243` remain honestly in `testing it`.

---

## 3. Complete 31-Sign Audit (21 Promoted + 5 4D Inherited, 9 `testing it`, 1 Honest `null`)

| Sign | Group | Tok (L/N) | Status | Lever | Reading | Key Data Lock / Honest Reason |
|---|---|---:|---|---|---|---|
| **240** | BigSix (T6) | 297 (272/25) | **building on it** | TrackA Rebus | `*katir-mīṉ / *cāy-mīṉ` | `DIR 1193` + `PEx 2456/2457`, Harappa mtab |
| **060** | BigSix (T6) | 196 (169/27) | **building on it** | TrackB Grammar | `*-uḷ / *-iṉ` | `94.4%` med, `dH=+1.64`, unseen `16:0 vs 0:29` (`P=1.55e-12`) |
| **798** | BigSix | 121 (106/15) | **building on it** | TrackA Rebus | `*toṭu / *iṭukku` | `PEx 3544/3536` + `DIR 444`, MD HR rep; triggers 4D `193,797,195` |
| **550** | BigSix | 97 (87/10) | **building on it** | TrackA Rebus | `*nāṭu` | `PEx 3584 naṭu <-> 3638 nāṭu`; `BOS-550-060` 27× |
| **440** | BigSix | 63 (48/15) | **building on it** | TrackA Rebus | `*mukku` | `PEx 4898 mukku <-> 4899 mukku`; pre-firing goblet stamp |
| **435** | Next9 | 62 (54/8) | **building on it** | TrackA Rebus | `*tōṭṭi` | `PEx 3547/3546`; `87.1%` bound `255-435`; triggers 4D `436` |
| **617** | Next9 | 60 (60/0) | **building on it** | TrackB Double | `*iru-accu` (`2× 615`) | 16 exact full-text matches vs New `615-615` (`P=0.00020`) |
| **845** | Next9 (T6) | 51 (49/2) | **building on it** | TrackA Rebus | `*vari` | `PEx 5263/5266 vari`, `ctab 67.4% L / 33.3% N` |
| **416** | Next9 | 49 (41/8) | **building on it** | TrackA Rebus | `*iru-kavar / *tuṟai` | `PEx 1325/1326` + `DIR 3370`, `cosL=0.884` w/ `415` |
| **013** | Next9 | 44 (40/4) | **building on it** | TrackB Numeral | `*mū` (stacked `3`) | `P139` (2+1), `013-840` 18× (`OR=195.7×, P=5.5e-31`) |
| **832** | T6_Only | 44 (24/20) | **building on it** | Key4A IntStroke | `*uḷ-vaḷai / *oru-vaḷai` | `790 + 1 stroke` (`cosL=0.698, cosR=0.656`) |
| **091** | T6_Only | 24 (18/6) | **building on it** | TrackB Double | `*iru-āḷ / *iruvar` | Matches New `090-090` (`P=0.00020`), `91.7%` initial |
| **241** | T6_Only | 13 (11/2) | **building on it** | Key4A Cage | `*katir-mīṉ-[CAGE]` | `240 + 4-corner cage` (`dF400=+0.906`, strongest in corpus) |
| **161** | T6_Only | 13 (11/2) | **building on it** | Key4A RoofHat | `*oḷi-kā` | `154 + caret hat` (`M14`, `cR=0.968`, `92.3%` final); triggers 4D `160` |
| **821** | T6_Only | 12 (12/0) | **building on it** | TrackB Double | `*iru-kāl` (`2× 820`) | 5 exact full-text matches vs New `820-820` (`P=0.00020`) |
| **703** | T6_Only | 11 (8/3) | **building on it** | Key4A MultiStroke | `*mū-aḷa / *mū-akal` | `700 + 3 strokes` (`dPos=-0.612, dSeal=+0.863`, mirror of `745`) |
| **592** | T6_Only | 11 (10/1) | **building on it** | Key4A Cage | `*mūṭai-[CAGE]` | `590 + 4-corner cage` (`dF400=+0.645, cosL=0.708`) |
| **804** | T6_Only | 6 (6/0) | **building on it** | Key4A Cage | `*kampu-[CAGE]` | `803 + 4-corner cage` (`dF400=+1.000, dFin=+0.667`) |
| **159** | T6_Only | 4 (4/0) | **building on it** | Key4D PureAllo | `*oḷi-kā` | Verified Pure 4D cluster with `161` (`M14`, `cR=0.852`) |
| **242** | T6_Only | 2 (2/0) | **building on it** | Key4A Variant | `*katir-mīṉ` (var.) | Graphic variant of newly locked `240` |
| **807** | T6_Only | 2 (2/0) | **building on it** | Key4A Cage | `*kampu-[CAGE]` | `806 + 4-corner cage` (exact twin of `804`) |
| *193,797,195* | *4D Inherit* | *8 (8/0)* | **building on it** | *Key4D PureAllo* | `*toṭu / *iṭukku` | *Pure 4D cluster inherited from newly locked `798`* |
| *436* | *4D Inherit* | *15 (15/0)* | **building on it** | *Key4D Workshop* | `*tōṭṭi` | *Workshop 4D cluster inherited from newly locked `435`* |
| *160* | *4D Inherit* | *3 (3/0)* | **building on it** | *Key4D PureAllo* | `*oḷi-kā` | *Pure 4D cluster inherited from newly locked `161`* |
| **142** | BigSix | 83 (56/27) | `testing it` | Partial DIR/Sangam | `*maṭṭam / *kōl?` | `55.4%` before `615/617` (`ctab OR 7.34L/22.41N`), raw DEDR `PEx=0` |
| **585** | Next9 | 52 (43/9) | `testing it` | Partial PSt | `*kuṭai / *paḷḷi?` | Harappa AB Citadel, `90.4%` med; raw DEDR `PEx=0`, only `PSt 1663/1655` |
| **595** | Next9 (T6) | 51 (32/19) | `testing it` | HatchOp / Null DEDR | `*mūṭai-[VARI]?` | Raw DEDR `0/0/0` (visual-only); live `ctab` hatching shift (`P=4.8e-5` N) |
| **527** | Next9 | 50 (47/3) | `testing it` | Partial DIR | `*uḻalai / *katavu?` | `88%` final, `78%` after `550 *nāṭu`; raw DEDR `PEx=0`, only `DIR 683` |
| **095** | T6_Only | 28 (22/6) | `testing it` | Audit Hold | `*āḷ+[STICK]?` | Copper-tablet companion of `142/595`; awaits `142` lock |
| **175** | T6_Only | 21 (18/3) | `testing it` | Audit Hold | `*iru/*iṟai` base? | Shares left (`cL=0.91`) with `176`, diverges right (`cR=0.195`) |
| **243** | T6_Only | 15 (9/6) | `testing it` | Audit Hold | `*oḷi-mīṉ-[HATCH]?` | `100%` seals (`12L/8N`), precedes `617`; awaits hatching bifurcation |
| **924** | T6_Only | 10 (9/1) | `testing it` | Audit Hold | `*maruppu-[HATCH]?` | West trade `OR=62.6L/150.8N`; awaits hatching bifurcation |
| **063** | T6_Only | 10 (8/2) | `testing it` | Audit Hold | `*kāl?` (`M343`) | Failed Key 4A swap shuffle (`P=0.20`), `M343 != M124` |
| **692** | Next9 | 62 (56/6) | **`null`** | Honest Null | *(Precinct Opener)* | Outlined X (`M150`), `74.2%` init, takes `060` 40/62×; **`0/0/0` DEDR** |

---

## 4. Updated Master Coverage — Before (`T5 = 114`) vs After Key #5A (`140` Locked)

| Corpus Split | Stage | Signs | Covered / Total Tokens | Token % (`Δ`) | 100%-Decoded Faces (`%`, `Δ`) | 100%-Decoded `len >= 3` (`Δ`) |
|---|---|---:|---:|---:|---:|---:|
| **Lipi Intact (`3,600` faces)** | Before (`T5`) | 114 | 9,777 / 13,209 | 74.02% | 1,532 (42.56%) | 612 |
| | **After Key #5A (`+4D`)** | **140** | **10,840 / 13,209** | **82.07% (+8.05%)** | **1,937 (53.81%, +405)** | **953 (+341)** |
| | *New T6 Frontier* | *149* | *11,086 / 13,209* | *83.93%* | *2,048 (56.89%)* | *1,042* |
| **Unseen New Intact (`563` faces)** | Before (`T5`) | 114 | 1,507 / 1,994 | 75.58% | 244 (43.34%) | 113 |
| | **After Key #5A (`+4D`)** | **140** | **1,652 / 1,994** | **82.85% (+7.27%)** | **325 (57.73%, +81)** | **169 (+56)** |
| | *New T6 Frontier* | *149* | *1,726 / 1,994* | *86.56%* | *367 (65.19%)* | *204* |
| **Combined Intact (`4,163` faces)** | Before (`T5`) | 114 | 11,284 / 15,203 | 74.22% | 1,776 (42.66%) | 725 |
| | **After Key #5A (`+4D`)** | **140** | **12,492 / 15,203** | **82.17% (+7.95%)** | **2,262 (54.34%, +486)** | **1,122 (+397)** |
| | *New T6 Frontier* | *149* | *12,812 / 15,203* | *84.27%* | *2,415 (58.01%)* | *1,246* |
| **Combined All (`6,790` faces)** | Before (`T5`) | 114 | 15,742 / 23,710 | 66.39% | 2,158 (31.78%) | 803 |
| | **After Key #5A (`+4D`)** | **140** | **17,412 / 23,710** | **73.44% (+7.05%)** | **2,715 (39.99%, +557)** | **1,241 (+438)** |
| | *New T6 Frontier* | *149* | *17,862 / 23,710* | *75.34%* | *2,888 (42.53%)* | *1,374* |

---

## 5. Newly 100%-Glossed Multi-Sign Inscriptions Showcase (`+397` Faces, `len >= 3`)

Selected newly 100%-decoded seals and copper tablets from `work_data/key5a/newly_glossed_inscriptions.csv` (including held-out unseen `new texts`):

| Inscription | Faces (L/N) | Unlocked By | Sign-by-Sign Proto-Dravidian Gloss |
|---|---:|---|---|
| `806-845-061-407-850-900-740` | 14 (14/0) | `845` | `*kampu — *vari — *kāl — *kōṭi — *kaṉ — *tiṅkaḷ — *kuṭi` ("Millet-Tax Quarter — Cloth — Copper — Month-House") |
| `920-060-742-806-415-220-240-255-435-690-740` | 1 (1/0) | `060,240,435` | `*tiṅkaḷ — *-uḷ — *iru-kuṭi — *kampu — *kavar — *mīṉ — *katir-mīṉ — *mutal — *tōṭṭi — *kaṭṭu — *kuṭi` ("In Month-Office, 2nd House — Millet — Seizing-Star Rayed-Star — First-Attendant's Store-House") |
| `920-060-745-235-240-231-590-390-740` | 1 (1/0) | `060,240` | `*tiṅkaḷ — *-uḷ — *mū-kuṭi — *oḷi-mīṉ — *katir-mīṉ — *uḷ-mīṉ — *mūṭai — *tai — *kuṭi` ("In Month-Office, 3rd House — Bright/Rayed/Inner Star — Woven-Bale House") |
| `920-060-741-592` | 2 (2/0) | `060,592` | `*tiṅkaḷ — *-uḷ — *oru-kuṭi — *mūṭai-[CAGE]` ("In Month-Office, 1st House — Bale/Treasury[CAGE]") |
| `550-060-690-740` | 5 (5/0) | `060,550` | `*nāṭu — *-uḷ — *kaṭṭu — *kuṭi` ("In the District/Precinct — Store-House") |
| `550-060-806-032-220-255-435-690-176-740` | 1 (1/0) | `060,435,550` | `*nāṭu — *-uḷ — *kampu — *iru — *mīṉ — *mutal — *tōṭṭi — *kaṭṭu — *iṟai — *kuṭi` ("In the Precinct — Millet — Two Stars — First-Attendant's Store — Tribute-House") |
| `861-002-798-415-220-705-033-590-405-740` | **1 (0/1 NEW)** | `798` | `*kāṇam — *iru — *toṭu — *kavar — *mīṉ — *kalam — *mū — *mūṭai — *tai — *kuṭi` (Unseen New `428`: "Share-unit — of — Bound-Seizing-Star — 3 *kalam* — Woven-Bale House") |
| `806-415-220-320-920-255-435-690-590-390-740` | **1 (0/1 NEW)** | `435` | `*kampu — *kavar — *mīṉ — *paṭi — *tiṅkaḷ — *mutal — *tōṭṭi — *kaṭṭu — *mūṭai — *tai — *kuṭi` (Unseen New `2804`: 11-sign full reading!) |
| `415-100-740-093-435-061-550-615-615-740` / `...-617-740` | **2 (1/1 NEW)** | `435,550,617` | `*kavar — *talai — *kuṭi — *uḷ-āḷ — *tōṭṭi — *kāl — *nāṭu — *iru-accu — *kuṭi` (Lipi `3373.1` + Unseen New `898` live catalog-double twin!) |
| `615-615-002-240-233-220-520` | **2 (0/2 NEW)** | `240` | `*accu — *accu — *iru — *katir-mīṉ — *veṭi-mīṉ — *mīṉ — *vēḷ` (Unseen New `3318, 3357`: "Twin Field-Plot — of — Rayed/Dawn/Star Chief") |
| `255-435-156-400` | 10 (10/0) | `435` | `*mutal — *tōṭṭi — *kā — *cikka` ("First-Attendant — Guard — Junior") |
| `013-840-740` | 8 (8/0) | `013` | `*mū — *iṇai — *kuṭi` ("Three Joint/Paired Houses") |
| `617-892-740-400` | 5 (5/0) | `617` | `*iru-accu — *vil — *kuṭi — *cikka` ("Twin Field-Plot — Sale — House — Junior") |
| `798-240-845-061-407` | 6 (6/0) | `240,798,845` | `*toṭu — *katir-mīṉ — *vari — *kāl — *kōṭi` ("Bound Rayed-Star — Tax Quarter — Cloth") |

---

## 6. Honest Nulls & Next Rescue Targets

1. **`692` (`62` tok, M150 Outlined X) — Honest Null (`0/0/0` raw DEDR):** Functional slot is pinned (`74.2%` initial, `64.5%` takes `060 *-uḷ`, Giant Seals `OR = 5.37` -> Precinct/Assembly Opener), but zero visual cross `<->` council/office root exists in 2-branch DEDR. **Rescue plan:** Test non-X visual interpretations of M150 (e.g., *four-way junction / crossroads* `nāṟcanti`, *loom-frame*, or *salt-pan/hearth*, plus non-Dravidian trade/substrate title check).
2. **`142` (`83` tok, M25 Staff-Holder) — Honest `testing it` (`PhonEx = 0, PhonSt = 0` raw DEDR):** `55.4%` (`46/83`) immediately precede `615/617 *accu` field-plots on Mohenjo-daro copper land-allotment tablets (`L OR = 7.34, N OR = 22.41`) and `061-142` (`11/81`). Raw DEDR hits only `DIRECT 4660 maṭṭam` ("measure, rule, gauging rod"). **Rescue plan:** Test Old Tamil / Chola epigraphic *aḷavu-kōl* ("land-measuring rod") + *kōl* (`DEDR 2237`) and `095/142/595` copper-tablet sub-corpus jointly.
3. **`585` (`52` tok, M194 Roofed Pavilion), `595` (`51` tok, M252 Hatched Box), `527` (`50` tok, M254 Barred Door-Leaf) — Honest `testing it`:** None hit 2-branch `PhonEx` under strict visual-only Domain A (`585`: only `PhonSt 1663 kuṭai <-> 1655 kuṭi`; `527`: only `DIRECT 683 uḻalai`; `595`: `0/0/0` raw DEDR, but strong copper-tablet hatching shift `0/42 -> 9/25` unseen New, `P = 4.78e-5`). **Rescue plan:** Resolve the hatching bifurcation (`ctab` on `845/595` vs `100% seal` on `243/502/812`) and test `550-527` (`20×`) + `017-585-740` (`12×`) against expanded Sangam architectural/gate compound lexicons.

**Top 10 remaining unsolved signs after Key #5A:** `142 (83), 692 (62), 585 (52), 595 (51), 527 (50), 388 (44), 350 (41), 455 (39), 460 (38), 384 (38)`.
