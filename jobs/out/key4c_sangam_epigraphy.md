# Key #4C (Lever 3): Old Tamil Sangam & Early Tamil-Brahmi Epigraphic Lexicon Bridge

**Headline Win**: Bridging our 19 sound-locked Indus signs + numerals into a verified **Old Tamil Sangam & Tamil-Brahmi epigraphic lexicon** (86 pure-Dravidian entries strictly separated from 15 Prakrit/Sanskrit loanwords) unlocks **13 recurring attested pure-Dravidian compounds** across 18 Indus bigrams (`Lipi >= 2`, **235 Lipi texts**, **40 unseen `events_new.json` texts**, **9/13 compounds replicating on unseen texts**, **0 Prakrit/Sanskrit loan hits**) — of which **9/13 (69.2%) are absent as headwords from raw DEDR**. Across all three blind 5,000-shuffle tests — compound expansion, epigraphic syntactic formula alignment, and physical metrology ladder matching — Old Tamil / Tamil-Brahmi beats both equal-size matched controls (**Early Indo-Aryan/Prakrit Brahmi** and **Ur III Sumerian**) and random null distributions.

- **Status**: **building on it** (Lexicon bridge, 4-rung Old Tamil metrology core, and double account-order signature all lock cleanly on rerunnable data).
- **Rerunnable script**: `/home/antigravity/Cuuper22/ivc/work_scripts/key4c_sangam_epigraphy.py`
- **Generated datasets**:
  - `/home/antigravity/Cuuper22/ivc/work_data/key4c/sangam_epigraphy_lexicon.csv` (86 pure Dravidian, 40 absent from raw DEDR headwords + 15 segregated Prakrit/Sanskrit loans)
  - `/home/antigravity/Cuuper22/ivc/work_data/key4c/rival_epigraphy_lexicon.csv` (86 Early IA/Prakrit — 80 verified in local Monier-Williams — + 86 Ur III Sumerian — 60 verified in local Halloran + local CDLI ATF)
  - `/home/antigravity/Cuuper22/ivc/work_data/key4c/test4c1_compound_matches.csv`
  - `/home/antigravity/Cuuper22/ivc/work_data/key4c/epigraphic_formulas_corpus.csv`
  - `/home/antigravity/Cuuper22/ivc/work_data/key4c/test4c3_metrology_comparison.csv`
  - `/home/antigravity/Cuuper22/ivc/work_data/key4c/key4c_summary.json`

---

## 1. Summary Scorecard (All Three 5,000-Shuffle Blind Tests)

| Test | Metric | Old Tamil / Tamil-Brahmi | Early IA / Prakrit Brahmi | Ur III Sumerian (Local CDLI) | 5,000-Shuffle Null | z-score | Empirical P |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **4C-1 (Compounds)** | Recurring distinct compounds (`Lipi>=2`) | **13** (18 pairs, 9 new beyond DEDR) | 5 (7 pairs) | 1 (2 pairs) | Perm-19: `6.88 ± 2.00` | **`+3.06`** | **`0.00460`** |
| **4C-1 (Compounds)** | Recurring compounds vs random DEDR roots | **13** (`235` Lipi / `40` New) | 5 (`133` Lipi / `28` New) | 1 (`25` Lipi / `6` New) | Draw-19: `0.39 ± 0.74` | **`+16.98`** | **`0.00020`** |
| **4C-1 (Compounds)** | All compounds (`Lipi>=1`, 0 loan hits) | **15** (26 pairs, 10 new beyond DEDR) | — | — | Perm-19: `9.47 ± 2.10` / Draw: `0.46 ± 0.85` | **`+2.63`** / **`+17.04`** | **`0.01140`** / **`0.00020`** |
| **4C-2 (Syntax)** | 6-axis alignment to Indus `FRAME v3` (`1-MAE`, `dir_cos`) | **`0.8425`** (`+0.8992`, **6/6** axes) | `0.6914` (`+0.4212`, 4/6) | `0.3772` (`-0.4274`, 2/6) | Axis-flip: `0.5089 ± 0.1475` | **`+2.26`** | **`0.01560`** |
| **4C-2 (Syntax)** | Alignment gap: Tamil-Brahmi vs rivals (`1-MAE`) | — | Gap **`+0.1511`** | Gap **`+0.4698`** | Permuted labels (5,000) | **`+2.28`** / **`+4.84`** | **`0.01000`** / **`0.00020`** |
| **4C-3 (Metrology)** | Composite ladder+divisor+liter score (`/3.0`) | **`2.8874`** (`3/3` steps, `437/438` cups) | `1.0003` (`1.3304` shifted) | `1.3857` (`0/3` steps) | Random ladders: `1.2027 ± 0.3178` | **`+5.30`** | **`0.00040`** |

---

## 2. Lexicon Construction & Strict Loanword Segregation

Raw DEDR (`work_data/lexicons/dedr/dedr_entries.tsv`, 5,264 properly split entries after separating merged lines) is an etymological root dictionary: **40 of our 86 verified pure-Dravidian Old Tamil administrative, clan, astral, maritime, and metrological compounds** (`46.5%`) do **not** appear as Tamil headwords in `dedr_entries.tsv` (e.g., `mummīṉ`, `aṟumīṉ`, `eḻumīṉ`, `nāḷmīṉ`, `muttiṅkaḷ`, `aṭikkuṭi`, `ciṟukuṭi`, `mutukuṭi`, `orukuṭi`, `orutalai`, `kaḷappāy`, `paṭikkāl`, `irukāl`, `kaṇkāṇi`, `kāviti`, `kiḻāṉ`, `kuṟuṇi`, `patakku`, `tūṇi`, `paṉṉiru`).

Every entry in `sangam_epigraphy_lexicon.csv` cites an attested DEDR root ID and/or Sangam / Tamil-Brahmi / University of Madras Tamil Lexicon (DDSA) attestation. **15 Prakrit/Sanskrit loanwords attested in Tamil-Brahmi & Sangam texts** (`nikama`, `vaṇikaṉ`, `cāttu`, `paṇṭam` [merchandise < Skt. *bhāṇḍa*, distinct from native DEDR 3898 *paṇṭam* = belly], `tammam`, `amaṇaṉ`, `upācaṉ`, `atiṭṭāṉam`, `eṭṭi`, `kācu`, `paṇam`, `palam`, `kāṇam`, `kaṇi`, `catiyaputo`) are quarantined in `origin_layer = prakrit_sanskrit_loan` and excluded from all Dravidian test scoring. False homonyms (`kutikkāl` = heel `kuti+kāl` ≠ `kuṭi+kāl`; `talaikkal` = keystone `talai+kal` ≠ `talai+kāl`) were checked against the Madras Tamil Lexicon and excluded.

---

## 3. Test 4C-1: Compound-Expansion Unlock on the 19 Locked Signs + Numerals

Using **true reading-order adjacent bigrams** extracted from `faces` (not the numerically sorted `signs` array) in `events_lipi.json` (4,476 records) and unseen `events_new.json` (990 records), there are **140 recurring (`Lipi >= 2`)** and **238 total (`Lipi >= 1`)** L19/numeral bigrams. Pre-consonantal `-am` elision is restricted strictly to consonant-initial second elements (*Tolkāppiyam* sandhi), preventing spurious vowel-initial collisions.

### Attested Pure-Dravidian Compounds Unlocked (0 Prakrit/Sanskrit Loan Hits)

| Rank | Old Tamil Compound | Category | Indus Pair(s) | Roots | In Raw DEDR? | Lipi Texts | Unseen New Texts | DEDR / Sangam / Madras Lexicon Attestation |
| :---: | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :--- |
| 1 | **`kuṭiyāḷ`** | `house_clan` | `740-090` | `kuṭi+āḷ` | Yes (Mal. 1655) | **100** | **20** | DEDR 1655+399; U. Madras Lex. ("house-tenant, estate manager/worker") |
| 2 | **`mummīṉ`** | `astral_calendar` | `003-220` (18/2), `033-220` (3/0) | `mu+mīṉ` | **No (NEW)** | **21** | **2** | DEDR 5052+4876; Divākaram; Madras Lex. ("Three Stars / Orion *Mṛgaśīrṣa*") |
| 3 | **`irukāl`** | `metrology` | `002-061` (17/1), `032-061` (2/0), `002-820` (1/0) | `iru+kāl` | **No (NEW)** | **20** (19 rec) | **1** | DEDR 474+1479; Sangam; Madras Lex. ("two-quarters / twice / two-legged") |
| 4 | **`aṟumīṉ`** | `astral_calendar` | `016-220` (15/2), `006-220` (1/0) | `aṟu+mīṉ` | **No (NEW)** | **16** (15 rec) | **2** | DEDR 2485+4876; *Paripāṭal* 5.49; Piṅkalantai ("Pleiades / Six Stars") |
| 5 | **`aṭikkuṭi`** | `house_clan` | `717-740` | `aṭi+kuṭi` | **No (NEW)** | **16** | **3** | DEDR 72+1655; U. Madras Lex. ("original / base / subordinate household") |
| 6 | **`muttiṅkaḷ`** | `astral_calendar` | `003-900` | `mu+tiṅkaḷ` | **No (NEW)** | **14** | **6** | DEDR 5052+3213; Classical Tamil; Madras Lex. ("three months, quarter-year") |
| 7 | **`vēḷir`** *(rebus)* | `admin_title` | `520-032` (10/1), `520-002` (1/1) | `vēḷ+iru` | Yes (5545) | **11** (10 rec) | **2** | DEDR 5545; *Puṟanāṉūṟu* 24, 201; Tamil-Brahmi ("Velir lineage lords"; `032` *iru* → plural *-ir* rebus) |
| 8 | **`mukkāl`** | `metrology` | `033-820` (5/0), `033-061` (3/0), `003-820` (1/0) | `mu+kāl` | Yes (1479) | **9** (8 rec) | 0 | DEDR 5052+1479; *Tolkāppiyam*; Chola inscriptions ("three-quarters, 3/4") |
| 9 | **`orukuṭi`** | `house_clan` | `031-740` (7/0), `001-740` (1/0) | `oru+kuṭi` | **No (NEW)** | **8** (7 rec) | 0 | DEDR 990+1655; *Tirukkuṟaḷ* 1029 ("single household / lineage") |
| 10 | **`orutalai`** | `admin_title` | `001-100` (5/0), `031-100` (2/0) | `oru+talai` | **No (NEW)** | **7** | 0 | DEDR 990+3103; *Puṟanāṉūṟu*; *Tirukkuṟaḷ* 1196 ("one side, steadfast / single-headed") |
| 11 | **`kaḷappāy`** | `maritime_trade` | `705-500` | `kaḷam+pāy` | **No (NEW)** | **7** | **3** | DEDR 1376+4088; U. Madras Lex. ("threshing-floor grain mat"; cf. `kalam+pāy` ship-sail) |
| 12 | **`īraṭi`** | `admin_title` | `002-717` (4/2), `032-717` (2/0) | `iru+aṭi` | Yes (72) | **6** | **2** | DEDR 474+72; U. Madras Lex. ("two feet, double-step, couplet") |
| 13 | **`nāḷmīṉ`** *(rebus)* | `astral_calendar` | `004-220` (5/0), `034-220` (1/0) | `nāl+mīṉ` | **No (NEW)** | **6** (5 rec) | 0 | DEDR 3656+4876; *Puṟanāṉūṟu* 229; *Paṭṭiṉappālai* ("lunar asterism, day-star"; dental *nāl* / retroflex *nāḷ* rebus) |
| 14 | **`eḻumīṉ`** *(Lipi=1)* | `astral_calendar` | `017-220` | `eḻu+mīṉ` | **No (NEW)** | 1 | 0 | DEDR 910+4876; Classical Tamil ("Ursa Major / Seven Stars") |
| 15 | **`kālāḷ`** *(Lipi=1)* | `admin_title` | `820-090` | `kāl+āḷ` | Yes (1479) | 1 | 0 | DEDR 1479+399; *Puṟanāṉūṟu*; *Patiṟṟuppattu* ("foot-soldier, infantryman") |

### What This Unlocks & How It Beats Controls
- **Raw DEDR alone (`Lipi >= 2`)**: 11 distinct forms (16 pairs, 212 Lipi, 31 New). **Sangam/TB epigraphy bridge**: **13 attested pure-Dravidian compounds** (18 pairs, **235 Lipi**, **40 New**), unlocking **9 recurring compounds** (`mummīṉ`, `irukāl`, `aṟumīṉ`, `aṭikkuṭi`, `muttiṅkaḷ`, `orukuṭi`, `orutalai`, `kaḷappāy`, `nāḷmīṉ`) plus `eḻumīṉ` (`Lipi=1`) that raw DEDR missed as headwords. Notice the complete Tamil astral quartet (`mummīṉ` 3-star, `nāḷmīṉ` 4/day-star, `aṟumīṉ` 6-star Pleiades, `eḻumīṉ` 7-star Ursa Major) plus household compounds (`kuṭiyāḷ`, `aṭikkuṭi`, `orukuṭi`) and calendar/quarter compounds (`muttiṅkaḷ`, `irukāl`, `mukkāl`).
- **Matched equal-size (86-term) rival controls** (even given generous multi-stem mappings per sign):
  - **Early Indo-Aryan / Prakrit**: **5 compounds** / 7 pairs / 133 Lipi / 28 New (`gṛhapati` `740-090`, `trimāsa` `003-900`, `tripāda` `033-061`/`033-820`, `dvādaśa` `002-717`/`032-717`, `cāturmāsya` `004-900`).
  - **Ur III Sumerian**: **1 compound** / 2 pairs / 25 Lipi / 6 New (`mul-mul` `235-220`/`220-235`).
- **5,000-shuffle significance**:
  - **Permuting sounds across the 19 locked signs** (numerals fixed): distinct recurring compounds = `13` vs `6.88 ± 2.00` (**`z = +3.06`, `P = 0.00460`**); recurring pairs = `18` vs `9.23 ± 2.79` (**`z = +3.14`, `P = 0.00340`**); all `Lipi>=1` compounds = `15` vs `9.47 ± 2.10` (**`z = +2.63`, `P = 0.01140`**).
  - **Equal-length root draws from clean 2-branch DEDR**: distinct recurring compounds = `13` vs `0.39 ± 0.74` (**`z = +16.98`, `P = 0.00020`**); Lipi mass = `235` vs `8.07 ± 23.65` (**`z = +9.60`, `P = 0.00040`**); unseen New mass = `40` vs `1.28 ± 4.18` (**`z = +9.25`, `P = 0.00080`**).
- **Transparent productive compounds NOT counted in the verified statistic**: Two massive `kuṭi` compounds (`100-740` *talai+kuṭi* "chief/head house" = **105 Lipi / 19 unseen New**; `176-740` *iṟai+kuṭi* "tax/lord house" = **123 Lipi / 14 unseen New**) were **excluded** from the attested Sangam lexicon because neither appears as a headword in the Madras Tamil Lexicon. Meanwhile `paṭikkāl` (*Paṭṭiṉappālai* 142) has `0` Lipi / `0` New occurrences (`320-061`/`320-820`).

---

## 4. Test 4C-2: Structural Formula Alignment (Indus `FRAME v3` vs Tamil-Brahmi vs Prakrit vs Ur III)

We measured six directional syntactic axes directly on `work_data/fv3/corpus_parsed_v3.csv` (intact `Lipi` and `Mahadevan` catalogues) and compared them against attested **Tamil-Brahmi / Old Tamil** inscriptions (Mahadevan 2003 cave inscriptions + Kodumanal/Keeladi/Quseir al-Qadim/Khor Rori potsherds + Anaikoddai seal + Old Tamil/Chola accounting clauses), **Early Prakrit Brahmi** (Bharhut/Sanchi votive & guild seals + fair Arikamedu/Salihundam potsherds + Arthaśāstra/Ashokan/Sohgaura counts), and **Ur III Sumerian** extracted directly from our local CDLI ATF files (`cdli_meluhha_atf.jsonl` + `cdli_east_atf.jsonl`: **22 legible `@seal` legends** and **3,519 attested measure phrases**).

| Syntactic Axis | Indus `FRAME v3` (Lipi intact) | Indus `FRAME v3` (Mah intact) | Early Tamil-Brahmi / Old Tamil | Early Prakrit Brahmi | Ur III Sumerian (Local CDLI) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| 1. **Header / Place Initial** (`OPEN` init + `PLACE` non-final) | **78.0%** (`1074/1377`) | **78.1%** (`1050/1344`) | **100.0%** (`17/17`) | 83.3% (`15/18`) | **0.0%** (`0/22` — PN always first) |
| 2. **Modifier before Head / Genitive Final** (`CREST` < `740`) | **98.9%** (`783/792`) | **98.6%** (`710/720`) | **100.0%** (`24/24`) | 100.0% (`24/24`) | **0.0%** (`0/22` — head-initial `dumu Father`) |
| 3. **Owner before Title** (`740` < `TITLE`) | **91.5%** (`354/387`) | **92.8%** (`285/307`) | **53.3%** (`8/15`) | 43.8% (`7/16`) | 100.0% (`19/19` — `PN dub-sar`) |
| 4. **Numeral before Commodity** (`NUM` + `THING`) | **87.9%** (`632/719`) | **98.9%** (`471/476`) | **100.0%** (`5/5`) | 100.0% (`5/5`) | 72.8% (`1685/2314`) |
| 5. **Measure before Numeral** (`MEASURE` + `NUM`) | **82.6%** (`218/264`) | **84.0%** (`142/169`) | **100.0%** (`5/5` — *nel kalam mūṉṟu*) | **0.0%** (`0/5` — *catvāraḥ droṇāḥ*) | **5.7%** (`200/3519` — 94.3% `NUM+MEAS`!) |
| 6. **Short Pot Graffiti** (`<= 3` signs / owner label) | **96.3%** (`286/297`) | **86.0%** (`74/86`) | **100.0%** (`10/10` Keeladi/Kodumanal/Red Sea) | 60.0% (`3/5` Arikamedu/Salihundam) | **0.0%** (`0/5` multi-line clay ledgers) |
| **Alignment to Indus Lipi (`1 - MAE`)** | `1.0000` | — | **`0.8425`** (**6/6** direction match) | `0.6914` (4/6) | `0.3772` (2/6) |
| **Signed Directional Cosine** | `+1.0000` | — | **`+0.8992`** | `+0.4212` | **`-0.4274`** (anti-correlated) |

- **The Diagnostic Double Account-Order Signature**: Indus puts numerals **before** commodities (`87.9%` Lipi, `98.9%` Mah) while putting standard capacity measures **before** numerals (`82.6%` Lipi, `84.0%` Mah) — exact Fisher reversal **`P = 7.54 × 10⁻⁹⁸` (Lipi)** and **`P = 3.47 × 10⁻¹⁰⁷` (Mahadevan)**. Old Tamil/Chola epigraphic accounting obeys this exact split (*mūṉṟu āṭu* "three sheep" vs *nel kalam mūṉṟu* "paddy, kalam 3"), whereas **both** Arthaśāstra Sanskrit/Prakrit (`catvāraḥ āḍhakāḥ droṇaḥ`) and local CDLI Ur III Sumerian (**`3,319/3,519 = 94.3%` `NUM+MEAS`**) run in the opposite direction.
- **5,000-shuffle significance**:
  - Tamil-Brahmi vs 5,000 random directional axis flips: `1-MAE = 0.8425` vs `0.5089 ± 0.1475` (**`z = +2.26`, `P = 0.01560`**); directional cosine `+0.8992` vs `-0.0147 ± 0.4050` (**`z = +2.26`, `P = 0.01560`**).
  - Exact 5,000-shuffle label-permutation gap: **Tamil-Brahmi > Prakrit-Brahmi** = **`+0.1511` (`z = +2.28`, `P = 0.01000`)** even with fair Prakrit potsherds; **Tamil-Brahmi > Ur III Sumerian** = **`+0.4698` (`z = +4.84`, `P = 0.00020`)**.

---

## 5. Test 4C-3: Metrology Ladder & Physical Scale Lock (5,000 Shuffles)

Our measured Indus capacity ladder (`work_data/met/unit_ladder.csv`) has a 4-rung core of **`1/8 paṭi (1.16 L) → ×8 cup (9.24 L) → ×4 vaḷḷam/tūṇi (37.0 L) → ×3 kalam (110.9 L)`** (plus `1/4 kāl = 2.31 L`), with **`437/438` (99.77%)** of measured Indus cup counts falling on exact divisors of `12` (`{1:9, 2:126, 3:183, 4:116, 6:3}` vs `0/438` tall-5s and only `1` seven).

| Metrology System | 4-Rung Ladder (Steps) | Step Matches (`/3`) | Cup → Super Mult | Indus Cup Divisor Compatibility (`/438`) | Mean `|log(L)|` Scale Error (Sim) | Composite Score (`/3.0`) | 5,000-Shuffle z-score | Empirical P |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Old Tamil / Chola** | `paṭi (1.3 L) → ×8 marakkāl (10.4 L) → ×4 vaḷḷam/tūṇi (41.6 L) → ×3 kalam (124.8 L)` | **`3/3`** | **`12`** | **`437/438` (99.8%)** | **`0.117`** (`0.890`) | **`2.8874`** | **`+5.30`** | **`0.00040`** |
| **Ur III Sumerian** | `sila3 (1.0 L) → ×10 ban2 (10 L) → ×6 barig (60 L) → ×5 gur (300 L)` | `0/3` | `30` | `321/438` (73.3%) | `0.427` (`0.653`) | `1.3857` | `+0.58` | `0.25555` |
| **Arthaśāstra (shifted)** | `prastha (0.75 L) → ×4 āḍhaka (3.0 L) → ×4 droṇa (12 L) → ×16 vārī (192 L)` | `1/3` | `64` | `251/438` (57.3%) | `0.858` (`0.424`) | `1.3304` | `+0.40` | `0.31434` |
| **Vedic / Arthaśāstra II.19** | `kuḍava (0.19 L) → ×4 prastha (0.75 L) → ×4 āḍhaka (3.0 L) → ×4 droṇa (12 L)` | `1/3` | `16` | `251/438` (57.3%) | `2.365` (`0.094`) | `1.0003` | `-0.64` | `0.77345` |

- **Lexical lock in DEDR**: `DEDR 5315` explicitly glosses Tamil **`vaḷḷam = "a measure of capacity = 4 marakkāls"`**, matching our exact `×4` step from `cup (9.24 L)` to `37.0 L`, while `×3` to `kalam (110.9 L)` completes the `1/8 : 1 : 4 : 12` Old Tamil capacity spine and explains why Indus cup counts forbid `5` (`0/438`) and peak on `2, 3, 4` (`425/438 = 97.0%`).
- **5,000-shuffle null** (random ancient step-factor ladders from `{2,3,4,5,6,8,10,12,16,20}` with random base volumes `[0.15, 2.5] L`): `mean = 1.2027 ± 0.3178`. Only **Old Tamil / Chola** clears the null (`z = +5.30, P = 0.00040`); both Arthaśāstra alignments and Ur III Sumerian sit squarely inside noise (`P = 0.25–0.77`).

---

## 6. Honest Limits & Next Leads Opened

1. **Test 4C-1 Lipi/New token-mass under pure 19-sign permutation**: While distinct recurring compounds (`13` vs `6.88`, `P = 0.00460`) and pairs (`18` vs `9.23`, `P = 0.00340`) clear 5,000 permutations cleanly, raw Lipi token mass (`235` vs `123.01 ± 82.43`, `z = +1.36, P = 0.09658`) and New mass (`40` vs `20.73 ± 13.49`, `z = +1.43, P = 0.10278`) have high permutation variance because `740-090` (`kuṭiyāḷ`, 100 Lipi / 20 New) dominates total mass whenever `kuṭi`/`āḷ` land on any high-frequency slot. Under equal-length DEDR draws, both Lipi mass (`z = +9.60, P = 0.00040`) and New mass (`z = +9.25, P = 0.00080`) clear overwhelmingly.
2. **Two phonetic-rebus matches in Test 4C-1**: `004-220` (`nāl` "four" + `mīṉ` "star" → `nāḷmīṉ` "day-star/lunar asterism") crosses dental *l* / retroflex *ḷ*, and `520-032` (`vēḷ` + `iru` "two" → `vēḷir`) uses numeral `iru` as plural *-ir*. Even excluding both, **11/13** recurring pure-Dravidian compounds (8 absent from raw DEDR, 8/11 in unseen New) hold on exact segmental sandhi — still >2× generous multi-stem Indo-Aryan (`5`) and 11× Ur III (`1`).
3. **Top-rung metrology divergence (`kōṭṭai`)**: While the 4-rung core (`paṭi 1/8 : cup 1 : vaḷḷam/tūṇi 4 : kalam 12` plus `1/4 kāl`) matches Old Tamil in step ratios (`3/3`) and liter scale (`~12%`), the Indus 5th rung is `6 kalam = 72 cups (665.3 L)`, whereas medieval South Tamil `kōṭṭai` (`DEDR 2208`) is `21 marakkāl` (varying 16–24 regionally). Thus the 5th-rung top multiplier is a regional/historical divergence and is **paused** as a ratio lock while the 4-rung core is **building on it**.
4. **Shared South Asian SOV substrate in Test 4C-2**: Prakrit-Brahmi shares 4/6 general South Asian head-final axes with Indus (`header_init`, `mod_before_gen`, `num_before_comm`, and some short potsherds). What cleanly separates Tamil-Brahmi/Old Tamil from Prakrit-Brahmi (`P = 0.01000`) is the **post-measure numeral accounting syntax** (`meas_before_num`: 100% Old Tamil / 82.6–84.0% Indus vs 0% Arthaśāstra Prakrit/Sanskrit) and the uniform secular owner-label potsherd tradition (Keeladi/Kodumanal/Red Sea).
5. **Next lead opened**: Test the 9 newly unlocked Sangam compounds — especially `aṭikkuṭi` (`717-740`), `kaḷappāy` (`705-500`), `muttiṅkaḷ` (`003-900`), and the astral quartet (`mummīṉ`, `nāḷmīṉ`, `aṟumīṉ`, `eḻumīṉ`) — against **site, object-type, and motif co-occurrence** (e.g., do `kaḷappāy` and `aṭikkuṭi` concentrate on maritime/trade seals vs rationing tablets, and do `100-740` *talai+kuṭi* and `176-740` *iṟai+kuṭi* split by administrative tier?).
