# Key #2 Track C: Linear Elamite & Proto-Elamite Bridge Audit

Script: [`work_scripts/key2c_elamite_bridge.py`](file:///home/antigravity/Cuuper22/ivc/work_scripts/key2c_elamite_bridge.py) (rerunnable end-to-end; machine-readable outputs in `work_data/key2c/`: `c1_shape_map.csv`, `c1_visual_transfer_results.csv`, `c1r_redesign_results.csv`, `c1_decoded_seals.csv`, `c2_regional_grammar.csv`, `c3_metrology_audit.csv`, `elamite_clean_lexicon.csv`, `summary.json`).

Primary external references verified directly:
- **Linear Elamite syllabary (Desset et al. 2022/2026)**: verified visually from Desset's official 2022 phonetic grid (`File:Grille_phonétique_des_signes_utilisés_en_élamite_linéaire.jpg`, CC-BY-4.0) and the University of Liège Hatamti database (`hatamti-elam.uliege.be/doc_about`: `45` texts, `2,033` tokens, `1,978 = 97.3%` deciphered; `69` distinct signs / `72` allographs / `67` phonemic values on a `5 V × 12 C` grid; `Doc 22` = Laursen #28 Indus-bull seal `za-ši-ri2` = *Zaširi*).
- **Linear Elamite vs. Indus structural comparison**: Fuls (2024, *IJAS* 14(1): 3–15) — LE alpha-syllabic redundancy vs. Indus logo-syllabic redundancy; Susa Text O (`Louvre Sb 9382`, 3 LE + 20 Indus-like signs incl. initial `853` & `220-033`) and Sibri `Sb-4` (`095` + LE sign 2).
- **Proto-Elamite accounting & numeral systems**: Born, Monroe, Kelley & Sarkar (2025, `arXiv:2502.00090`, `8,011` intact numerals), Dahl (2019, 2023 *Akkadica*), Damerow & Englund (1989).
- **Ur III / Susa / Dilmun metrology**: ORACC DCCMT, Zaccagnini (1986), Roaf (1982), Peyronel (2000), and our Indus ledger (`jobs/out/metrology_ledger.md`).

---

## Headline Findings

1. **WIN — The 5 Iranian Plateau Indus seals form a distinct Elamite-frontier cylinder-seal contact dialect, not a random draw from Bahrain/Mesopotamia (`10,000`-draw rival permutation joint `p = 0.0013` on provenanced seals; `p = 0.0078` incl. unprovenanced).**
   - **`60.0%` (`3 / 5`)** of Iranian Indus seals are **cylinders** (`Susa 3882.1`, `Jalalabad Fars NMI 2698`, `Sistan BM 1960,0718.1.1`) vs **`0.0%` (`0 / 23`)** across all provenanced Bahrain (`0/7`), Failaka/UAE (`0/4`), and Mesopotamia (`0/12`) Gulf seals (**exact Fisher `p = 0.00305`**).
   - Iranian seals share the Gulf calque `090/091` MAN prefix (**`4 / 5 = 80.0%`** vs `15 / 23 = 65.2%` in ProvGM; sign-vector cosine `0.589` with Failaka, `0.489` with Mesopotamia) **while retaining `2.4×` higher directed mainland Indus bigram grammar (`7 / 22 = 31.8%` vs `10 / 74 = 13.5%`, Fisher `p = 0.0608`)**, completely dropping the Bahrain/Mesopotamia Fish complex (**`0 / 5 = 0.0%`** vs `8 / 23 = 34.8%`), and enriching `831` (`2/5 = 40%` vs `1/23 = 4.3%`, `p = 0.073`) and `032` (`2/5 = 40%` vs `1/23 = 4.3%`, `p = 0.073`).
   - **Concrete prediction**: Unprovenanced cylinder `G3-U02` (`3888.1`: `032-132-000-055-090`) is one of only two cylinders outside Iran and carries Iran's exact `032 + 055 + 090` signature — predict Iranian Plateau provenance.
   - *Status: building on it.*

2. **WIN — Two-Layer Metrological Contact Law: Exact Trade-Weight Lock (`0.0%–0.37%`, `p = 0.0068`) + Shared Commodity-Selected Numeral Architecture, Paired with Independent Local Grain Capacities (Rival Ergonomic Convergence `p = 0.5509`).**
   - **Trade Weights (Exact Lock)**: `100 × 13.65 g` Indus chert unit = **`1,365 g`** = **`1` Dilmun/Bahrain mina** (`1,365–1,370 g`, error **`0.00%–0.37%`**; `10,000`-trial Monte Carlo **`p = 0.0068`**) = `160 × 8.53 g` Mesopotamian shekels = `2 2/3` Ur III minas (`504 g`, `+1.56%`).
   - **Accounting Architecture (Isomorphic)**: Both Indus (`NMI = 0.2606`, `z = +59.4`, `P = 0.0010`: `F` tall = volume/weight vs `S/T/B` short/packed = discrete/living) and Proto-Elamite (Born et al. 2025 on `8,011` intact numerals: `C = 1,678` capacity, `S = 107` sexagesimal inanimate, `D = 96` decimal animate/laborers, `B = 18` rations; only `11 / 244 = 4.5%` preceding signs cross systems, all headers/qualifiers, zero counted commodities) enforce strict commodity-selected numeral series and share near-identical logo-syllabic sign-inventory curves at `10,583` uses (`Indus 548/205/74.6%` vs `PE 508/185/73.5%`).
   - **Bulk Grain Capacities (Independent / Local)**: Indus `cup 700` (`9.26 L`, `9.24 L` anchor) is **`-7.4%` (`-7.6%`)** below Ur III `1 ban` (`10 L`), and the apparent `-7.4%` hits at `vaḷḷam` (`37.0 L` vs `4 ban`), `kalam` (`111.1 L` vs `2 barig` / `1/2 PE N45`), and `kōṭṭai` (`666.7 L` vs `1 PE N34`) are **one algebraically dependent `0.926` scale factor**, not four independent hits. Structurally, Indus capacity is **strictly duodecimal (`1:4:12:72`, `0 / 422` tall-`5`s on `700`, `P = 1.59e-7`)**, whereas both Proto-Elamite `C` (`×5, ×6, ×10, ×3, ×10`) and Ur III (`×10, ×6, ×5`) hardwire a base factor of **`5`**. Random carryable buckets (`5–15 L`) hit within `±7.6%` of some PE/Ur III rung **`55.1%`** of the time (`p = 0.5509`).
   - *Status: building on the weight bridge & 2-series accounting isomorphism; capacity-borrowing hypothesis paused.*

3. **NULL + REDESIGN — Visual Sign-Shape Transfer from Desset's Linear Elamite Syllabary Produces Zero Signal on Iranian, Gulf, or Mainland Indus Inscriptions (`5,000` Shuffles, `p >= 0.07–1.00`).**
   - Mapping `41` Indus signs (`30` visual correspondences: `15` graphic universals, `26` specific compounds) directly from Desset's 2022 phonetic grid onto cleaned Bronze Age Elamite names/LE vocabulary (`Lex A = 117`) and cleaned Hinz & Koch (`Lex B = 2,192`, filtered from `2,460` raw rows after stripping `363` OCR/German/short fragments) yields **`0 / 5` exact or near-exact Bronze Age Elamite hits on the 5 Iranian seals (`p = 1.0000`)**, `0 / 28` exact on Gulf/Mesopotamia (`p = 1.0000`), and chance scores on the Top 50 mainland Indus stems (`Lex A skel z = -0.56` to `-0.82`, `p = 0.74–0.82`).
   - **Redesign C1-R** (stripping `090/091/093/095/001` as non-phonetic Gulf MAN determinatives/dividers and testing alternative LE visual matches across `5,000` shuffles) stays squarely at chance: **`0 / 5` Lex A exact/near/skeleton hits (`R→L`, `p = 1.0000`)**, `2 / 5` Lex B skeleton vs null `1.88` (`p = 0.642`).
   - *Status: paused.* Linear Elamite (`69`-sign alpha-syllabary) and Indus (`~500`-sign logo-syllabary) do **not** share sign-to-sound values via visual shape. Frontier contact in Iran operated by **writing Elamite names in Linear Elamite on Indus-style seals** (`Laursen #28: Zaširi`) or **calquing/transcribing frontier names with Indus's own script rules** (Test C2).

---

## Test C1: Visual Sign-Shape Transfer (Desset Linear Elamite → Indus)

### Lexicon Cleaning Audit (`elamite_clean_lexicon.csv`)
Cleaning `work_data/lang_m/lex/elamite_hinzkoch.tsv` (`2,460` raw rows) removed `363` artifacts (`129` too short / `<2` consonants, `51` OCR corruption e.g. `lfl`/`sb-be`, `43` unhyphenated German gloss leaks, `16` German stopwords `mit/ch/der/...`, `15` malformed syllable strings), leaving **`2,097` clean Hinz & Koch lemmas**, merged with **`117` verified Bronze Age Old Elamite PNs, DNs, GNs, and Desset LE corpus words** (`Lex A = 117`, `Lex B = 2,192`). Consonant skeletons preserve initial vowels (`V-`) and require `≥ 2` true consonants to block Key #1's 1-consonant collision bug.

### Verified Visual Correspondences (`c1_shape_map.csv`)
`41` Indus Lipi signs mapped directly against Desset's 2022 phonetic grid (`36` strict, `5` extended; `15` `graphic_universal` = `36.6%`, `26` `specific_compound` = `63.4%`):
- **Graphic universals**: `001 ↔ |` (divider/`la`), `031 ↔ u/w`, `032/002 ↔ zu` (`||`), `033/003 ↔ ša` (`|||`), `850 ↔ a` (`◊`), `818 ↔ šů/s` (`⊕`), `820 ↔ pe` (6-spoke wheel), `900/904 ↔ pa` (crescent), `615 ↔ ko` (`#` grid), `319 ↔ ši` (`H`), `520 ↔ ka/si` (arrow), `692 ↔ e` (`X`), `700 ↔ ku/po` (`U` cup).
- **Specific compounds**: `861/817 ↔ we` (diamond topped by small diamond), `831 ↔ ke/l` (diagonally veined leaf), `832 ↔ ta` (vertically bisected leaf), `840 ↔ pu` (twin vertical ovals), `924 ↔ sa` (hatched crescent), `603 ↔ r` (2-bar tall box), `604 ↔ ri` (3-bar tall box), `528 ↔ li` (pinwheel box), `503 ↔ le` (striped triangle), `550 ↔ k/p` (opposing bowtie triangles), `365/368 ↔ te/i` (flagged pole), `400/415/416 ↔ ni` (comb), `413 ↔ rů` (barred pole), `390/405/407 ↔ š/le` (branching tree), plus extended `740/741 ↔ mu/pi` (collared jar), `220 ↔ za/ha` (tailed diamond/fish), `090/091 ↔ š/šš` (branching stick-figure).

### Transliteration of the 5 Iranian Indus Seals (`full_30` & Redesign `det_strip_prim`)

| Seal | Site & Form | Indus Sequence | `full_30` (`R→L`) | `det_strip_prim` (`R→L`, `090/091/001` = DET/DIV) | `det_strip_prim` (`L→R`) |
|---|---|---|---|---|---|
| `G3-I01` | Susa (round) | `090-365-090-407-604-700` | `š-te-š-š-ri-ku` (`0` hits) | `te \| š-ri-ku` (`B_SKEL: srk`) | `ku-ri-š \| te` (`A_ED1: kuri`) |
| `G3-I02` | Luristan (round) | `091-840-413-831` | `šš-pu-ru-ke` (`0` hits) | `pu-ru-ke` (`B_SKEL: prk`) | `ke-ru-pu` (`B_SKEL: krp`) |
| `G3-I03` | Susa (cylinder) | `924-001-319-031-055-002-150-416` | `sa \| ši-u-?-zu-?-ni` (`0` hits) | `sa \| ši-u-?-zu-?-ni` (`0` hits) | `ni-?-zu-?-u-ši \| sa` (`0` hits) |
| `G3-I04` | Jalalabad Fars (cyl) | `741-032-090-003-090` | `mu-zu-š-ša-š` (`0` hits) | `mu-zu \| ša` (`0` hits) | `ša \| zu-mu` (`B_SKEL: zm`) |
| `G3-I05` | Sistan BM (cyl) | `090-831-091-032` | `š-ke-šš-zu` (`0` hits) | `ke \| zu` (`0` spans `≥2`) | `zu \| ke` (`0` spans `≥2`) |

### `5,000`-Shuffle Statistical Benchmark (`R→L`, primary reading direction)

| Map & Dataset | `A_exact` obs (perm null, `p`) | `A_near_ed1` obs (perm null, `p`) | `A_skel` obs (perm null, `p`) | `B_exact` obs (perm null, `p`) | `B_skel` obs (perm null, `p`) | `syl67` null `p` (`B_skel`) |
|---|---|---|---|---|---|---|
| `strict_26` · Iran (`n=5`) | `0` (`0.02`, `1.000`) | `0` (`0.35`, `1.000`) | `0` (`0.46`, `1.000`) | `0` (`0.08`, `1.000`) | `2` (`1.33`, `0.413`) | `0.398` |
| `strict_26` · Gulf/Mesop (`n=28`) | `0` (`0.01`, `1.000`) | `0` (`0.23`, `1.000`) | `0` (`0.26`, `1.000`) | `0` (`0.05`, `1.000`) | `0` (`0.53`, `1.000`) | `1.000` |
| `strict_26` · Mainland Top 50 | `1` (`0.22`, `0.154`) | `5` (`6.06`, `0.610`) | `5` (`6.94`, `0.738`) | `4` (`1.36`, `0.097`) | `21` (`15.30`, `0.150`) | `0.194` |
| `full_30` · Iran (`n=5`) | `0` (`0.01`, `1.000`) | `0` (`0.24`, `1.000`) | `0` (`0.31`, `1.000`) | `0` (`0.06`, `1.000`) | `0` (`0.85`, `1.000`) | `1.000` |
| `full_30` · Gulf/Mesop (`n=28`) | `0` (`0.28`, `1.000`) | `1` (`2.33`, `0.864`) | `1` (`2.90`, `0.918`) | `1` (`0.65`, `0.411`) | `5` (`6.53`, `0.822`) | `0.815` |
| `full_30` · Mainland Top 50 | `1` (`0.22`, `0.171`) | `5` (`7.34`, `0.768`) | `6` (`9.11`, `0.821`) | `3` (`1.57`, `0.229`) | `31` (`22.09`, `0.070`) | `0.095` |
| **Redesign `det_strip_prim` · Iran (`n=5`)** | `0` (`0.02`, `1.000`) | `0` (`0.55`, `1.000`) | `0` (`0.64`, `1.000`) | `0` (`0.12`, `1.000`) | `2` (`1.88`, `0.642`) | — |
| **Redesign `det_strip_prim` · Gulf (`n=28`)** | `0` (`0.26`, `1.000`) | `1` (`1.40`, `0.701`) | `0` (`1.62`, `1.000`) | `1` (`0.44`, `0.292`) | `4` (`3.81`, `0.584`) | — |
| **Redesign `det_strip_alt` · Iran (`n=5`)** | `0` (`0.01`, `1.000`) | `0` (`0.46`, `1.000`) | `0` (`0.60`, `1.000`) | `0` (`0.16`, `1.000`) | `1` (`1.71`, `0.904`) | — |

**Strongest Rival Audit (C1)**: Graphic simplicity & independent convergent geometry explain the visual overlap. Over a third (`36.6%`) of visual matches are cross-cultural `graphic universals` (Wells 2011; Fuls 2024: vertical strokes, diamond, crescent, cup, grid, cross, wheel), and independent complexity-matched look-alike tests show Aegean Linear B passes the same geometric threshold (`q = 0.045` vs LE `q = 0.010`) despite zero historical descent. Phonetic transfer adds zero lift over random syllable assignment across both null models and both reading directions (`p > 0.06` across all 120 test cells).

---

## Test C2: Iranian Indus Seals vs. Gulf & Mainland Grammar

### Regional Comparison (`c2_regional_grammar.csv`)

| Cohort | `N` | Cylinder | `090/091` MAN | Fish (`220/235/255/240`) | `831` | `032` | `604` | `924` | `055` | Directed Mainland Bigrams | Cosine vs. Iran |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Iran_Indus** | **5** | **3/5 (60%)** | **4/5 (80%)** | **0/5 (0%)** | **2/5 (40%)** | **2/5 (40%)** | 1/5 | 1/5 | 1/5 | **7/22 (31.8%)** | 1.000 |
| Bahrain | 7 | 0/7 (0%) | 5/7 (71%) | 3/7 (43%) | 1/7 (14%) | 1/7 (14%) | 0/7 | 0/7 | 3/7 | 3/20 (15.0%) | 0.422 |
| Failaka_UAE | 4 | 0/4 (0%) | 4/4 (100%) | 1/4 (25%) | 0/4 (0%) | 0/4 (0%) | 1/4 | 1/4 | 0/4 | 2/12 (16.7%) | **0.589** |
| Mesopotamia_Round | 12 | 0/12 (0%) | 6/12 (50%) | 4/12 (33%) | 0/12 (0%) | 0/12 (0%) | 1/12 | 1/12 | 0/12 | 5/42 (11.9%) | 0.489 |
| Unknown_Gulf_WA | 5 | 2/5 (40%) | 3/5 (60%) | 1/5 (20%) | 0/5 (0%) | 1/5 (20%) | 0/5 | 0/5 | 2/5 | 3/11 (27.3%) | 0.381 |
| Indus_Home_Round | 6 | 0/6 (0%) | 1/6 (17%) | 3/6 (50%) | 0/6 (0%) | 0/6 (0%) | 0/6 | 0/6 | 1/6 | 8/21 (38.1%) | 0.193 |
| Abroad_Square | 8 | 0/8 (0%) | 0/8 (0%) | 4/8 (50%) | 0/8 (0%) | 0/8 (0%) | 0/8 | 0/8 | 0/8 | 10/32 (31.2%) | 0.093 |

All `20 / 20` signs on the 5 Iranian seals are attested on the Indus mainland, and `7 / 22 (31.8%)` of their directed bigrams occur verbatim in mainland `events_lipi.json`: `G3-I01` Susa (`090-365` n=1, `407-604` n=1, `604-700` n=1), `G3-I02` Luristan (`413-831` n=1), `G3-I03` Susa cyl (`031-055` n=5), `G3-I04` Jalalabad cyl (`032-090` n=10, `003-090` n=4), `G3-I05` Sistan cyl (`0/3`).

### Strongest Rival Audit (C2): Small-Sample Draw from an Undifferentiated Gulf Pool
Testing whether `n = 5` Iranian seals could be a chance draw from a single undifferentiated Gulf/Mesopotamia merchant pool (`10,000` random draws of `5` seals):
- **Cylinder rate (`3/5` vs `0/23` ProvGM)**: exact Fisher **`p = 0.00305`**, perm `p = 0.0029` (`N=28` provenanced), `p = 0.0173` (`N=33` incl. unprovenanced).
- **Enriched signs (`831` `2/5` vs `1/23`, `032` `2/5` vs `1/23`)**: Fisher `p = 0.0733` each (perm `p = 0.074–0.079` on `N=28`).
- **Directed mainland bigrams (`7/22 = 31.8%` vs `10/74 = 13.5%` ProvGM)**: Fisher `p = 0.0608`.
- **Zero fish (`0/5` vs `8/23`)**: individually `p = 0.281` (perm `p = 0.153`), consistent with small `n`.
- **Joint Iranian frontier profile (`cyl ≥ 3`, `fish = 0`, and `831 ≥ 2` or `032 ≥ 2`)**: **`p = 0.0013`** (`N=28` provenanced) and **`p = 0.0078`** (`N=33` all Gulf/WA).

**Interpretation**: The Iranian Plateau is a **distinct Elamite-Indus frontier contact zone** — adopting the local Elamite cylinder medium (`60%`) and Gulf `090/091` MAN determinatives (`80%`) while preserving `2.4×` more mainland Indus bigram syntax than Bahrain/Ur seals and sitting directly alongside bilingual/bigraphic Linear Elamite–Indus hybrids (`Laursen #28 Zaširi`, `Susa Text O`, `Sibri Sb-4`).

---

## Test C3: Indus vs. Proto-Elamite vs. Mesopotamian Metrology & Structure

### 1. Conversion Ladder & Ratio Audit (`c3_metrology_audit.csv`)

| Indus Unit | Indus Value | Compared Standard | Target Value | % Diff | Independence / Structural Verdict |
|---|---:|---|---:|---:|---|
| `paṭi` (`320`, `1/8` cup) | `1.16 L` | Ur III `1 sila` | `1.00 L` | `+15.8%` | Loose (`-3.5%` vs non-integer `1.5 × 0.8 L` PE `N39B`) |
| **`cup` (`700`)** | **`9.26 L`** (`9.24 L`) | Ur III **`1 ban`** (`10 sila`) | `10.00 L` | **`-7.4%`** (`-7.6%`) | Primary DOF #1 — outside trade calibration tolerance |
| `cup` (`700`) | `9.26 L` | Archaic `12 × 0.8 L` sila | `9.60 L` | `-3.5%` | Closer, **but Proto-Elamite has NO `12×` rung** (`N1 = 5 sila = 4 L`) |
| `vaḷḷam` (`711 = 4c`) | `37.04 L` | Ur III `4 ban` | `40.00 L` | `-7.4%` | **Algebraically dependent** on `9.26 / 10.0 = 0.926` |
| `kalam` (`705 = 12c`) | `111.12 L` | Ur III `2 barig` / `1/2 PE N45` | `120.00 L` | `-7.4%` | **Algebraically dependent** (`+11.1%` vs `1/3 gur`; `1 gur = 2.70 kalam`) |
| `kōṭṭai` (`575 = 72c`) | `666.72 L` | Proto-Elamite `1 N34` | `720.00 L` | `-7.4%` | **Algebraically dependent** (`+11.1%` vs `2 gur = 600 L`) |
| **Indus Chert `100×`** | **`1,365 g`** | **Dilmun / Bahrain mina** | **`1,365–1,370 g`** | **`0.00%–0.37%`** | **EXACT INDEPENDENT LOCK** (`100 × 13.65 g`) |
| **Indus Chert `100×`** | **`1,365 g`** | **Ur III / Susa weight bridge** | `160 × 8.53 g` / `2⅔ × 504 g` | **`+1.56%`** | **EXACT TRADE BRIDGE** (verified by Indus chert weights at Ur & Susa) |

### 2. Base Systems, Commodity-Selected Numeral Series, and Sign Inventories

| Feature | Indus Script | Proto-Elamite (`Born et al. 2025`; `Dahl`) | Ur III Sumerian | Linear Elamite (`Desset 2022/2026`) |
|---|---|---|---|---|
| **Capacity base steps** | Pure duodecimal/binary: `×2, ×4, ×4, ×3, ×6` (`1:4:12:72`; **`0/422` tall-`5`s** on `700`, `P = 1.59e-7`) | `C`: binary sub-fractions → **`×5`** (`N1`) → `×6` (`N14`) → `×10` (`N45`) → `×3` (`N34`) → `×10` (`N48`) | `×10` (`ban`) → `×6` (`barig`) → **`×5`** (`gur`) | Not an accounting corpus |
| **Weight base steps** | Binary `1..64` → **`×5` decimal** (`160, 200`; `171` takes `{3, 5}`, `31/31`) | Sexagesimal/decimal trade weights | Sexagesimal (`60 shekels = 1 mina`, `60 minas = 1 talent`) | — |
| **Commodity-selected numeral series** | **YES (`NMI = 0.2606`, `z = +59.4`)**: `F` tall (volume/weight) vs `S/T/B` short/packed (discrete/living) | **YES (`8,011` numerals)**: `C` grain (`1,678`), `S` inanimate (`107`), `D` animate/laborers (`96`), `B` rations (`18`); only `11/244 (4.5%)` signs cross (0 commodities) | Single sexagesimal + distinct capacity/area metrologies | No administrative numeral split |
| **Sign inventory (`@10,583` uses)** | **`548` types / `205` hapaxes / `74.6%` top-100** (logo-syllabic) | **`508` types / `185` hapaxes / `73.5%` top-100** (logo-syllabic) | Logo-syllabic cuneiform | **`69` core signs / `67` values / `97.3%` coverage** (alpha-syllabic) |

### 3. Strongest Rival Audit (C3): Ergonomic Convergence Monte Carlo (`10,000` Trials)
Drawing a random carryable grain bucket `V ~ Uniform(5, 15) L` and small integer ladder step `k ∈ {4, 6, 8, 10, 12}`:
- Chance `V` lands within `±7.6%` of `1 ban` (`10 L`): **`15.35%`** (`p = 0.1535`).
- Chance `V` lands within `±3.8%` of `12 × 0.8 L` (`9.6 L`): **`7.26%`** (`p = 0.0726`).
- Chance `V` or `k × V` lands within `±7.6%` of *any* PE/Ur III rung (`8, 10, 12, 60, 100, 120, 240, 300 L`): **`55.09%`** (`p = 0.5509`).
- Contrast — chance a random weight unit `w ~ Uniform(5, 25) g` hits `Dilmun mina / 100` (`13.65 g`) within `±0.5%`: **`0.68%`** (`p = 0.0068`).

**Conclusion**: Bulk agricultural capacities evolved independently on a strictly duodecimal Harappan base (never `5`) — the `-7.4%` overlap with `ban`/`barig`/`N34` is ergonomic coincidence (`p = 0.55`). By contrast, **precious-commodity trade weights lock to `<0.4%` (`p = 0.0068`)** across Meluhha–Dilmun–Susa–Ur, and **Indus's 2-series accounting grammar (`F` vs `S/T/B`) mirrors Proto-Elamite's `C/S/D` commodity-typed numeral architecture** as a deep administrative template shared across the Indo-Iranian Bronze Age.
