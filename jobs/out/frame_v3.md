# FRAME v3 — Word-Free Clause Grammar & Corpus Segmentation

**Building on it.** Strict, word-free clause parsing now covers **87.14% of all 3,600 intact Lipi faces** (`3,137 / 3,600`, up from `50.47%` in `FRAME v2`), **87.19% of intact Lipi inscriptions of length ≥ 3** (`1,973 / 2,263`, up from `49.93%`), and **88.03% of length ≥ 3 administrative inscriptions** (`seals, miniature tablets, copper tablets, and clay tags`, `1,912 / 2,172`), while **0 of 20 frequency-band-matched decoy class maps** come within 38 percentage points (`29.46%` decoy mean overall, `+57.68` pp, $z = 5.91$, $P = 1.74 \times 10^{-9}$; `23.92%` decoy mean on length ≥ 3, `+63.26` pp, $z = 4.53$, $P = 2.93 \times 10^{-6}$).

Applied with zero retuning to **held-out unseen Mahadevan `new texts`** (`482` complete lines whose signs are in the Lipi training vocabulary, never touched during audit, class refinement, or rule design), `FRAME v3` **more than doubles `FRAME v2` strict parse coverage from 29.88% (`144 / 482`) to 64.94% (`313 / 482`)**, beating all 20 decoys (`34.61%` mean, `53.32%` max, `0/20`, `+30.33` pp, $z = 3.76$, $P = 8.41 \times 10^{-5}$) and 20 within-line token-order shuffles (`38.87%`). On unseen `new texts` of **length ≥ 3** (`n = 290`), coverage jumps from **33.10%** (`v2`) to **64.83%** (`v3`) against a **22.93%** decoy mean (`+41.90` pp, $z = 3.52$, $P = 2.14 \times 10^{-4}$, `0/20`) and **24.31%** order-shuffle mean. Across all **627 complete unpartnered Mahadevan inscriptions** (including 145 lines carrying rare Mahadevan-only `X...` signs defaulted to `PERSONAL`), `FRAME v3` parses **59.01%** (`61.62%` on length ≥ 3, vs. `22.20%` decoy mean, `+39.43` pp, $z = 3.59$, `0/20`).

Keeping the **exact same 14 explicit multi-sign classes** as `FRAME v2` (zero singleton classes), 69 role-consistent Lipi-CV-validated sign moves lower held-out next-sign cross-entropy across every split:
- **5-fold Lipi CV**: **6.8445 bits/sign** (**6.8847 bits/sign** under strictly nested out-of-fold class learning where moves are re-learned inside each 4-fold training split) vs. `FRAME v2` **6.9456** and `FRAME v1` **7.1735 bits/sign**.
- **Lipi Half-A → Half-B** (`seed = 2026`): **7.0772 bits/sign** pooled (**7.0430 bits/sign** by object kind) vs. `FRAME v2` **7.1752** (`7.1434` by kind), `FRAME v1` **7.4032**, and 20-decoy mean **7.7044 bits/sign** (`0/20`).
- **Unseen Mahadevan `new texts` (`482` lines)**: **7.5313 bits/sign** (**33.2% of bigram order captured** — beating `FRAME v2` `7.5362`, machine `exchange10` `7.5321`, and `HMM10` `7.5757`!), against 20-decoy mean **7.7924** and best decoy **7.6871 bits/sign** (`0/20`, $z = 5.76$, $P = 4.30 \times 10^{-9}$). On unseen seals (`n = 269`), cross-entropy drops from `7.3739` (`v2`) to **7.3413 bits/sign**.
- **77-item Fill-the-Gap Restoration**: `FRAME v3` alone reaches **51.9% Top-5** (up from `50.6%` in `v2`, vs. `36.4%` decoy mean), and mixed 50/50 with the sign bigram reaches **59.7% Top-5 / 74.0% Top-10**.

**What this opens:** All **9,252 inscriptions** across both catalogues (`5,679` Lipi faces + `3,573` Mahadevan lines in `work_data/fv3/corpus_parsed_v3.csv`) are now explicitly segmented into individual clauses (`clause_1 | clause_2 | ...`) and within-clause grammatical roles (`clause_opener`, `header_slot`, `clause_linker`, `name_crest`, `name_stem`, `pre_closer_stem`, `clause_closer`, `clause_title`, `measure_unit`, `quantifier`, `counted_commodity`). Downstream lexical and phonetic solvers no longer treat multi-clause seals or copper tablets as monolithic names: subordinate headers, commodity counts, and owner/official name clauses can now be aligned and glossed clause by clause.

---

## 1. Forensic Diagnosis of the 1,783 Unparsed Intact Lipi Faces (`fv3_01_audit.py`)

Auditing Lipi (`d`) alone showed why `FRAME v2` stopped at `1,817 / 3,600` (`50.47%`), leaving **591 `loose name text`** and **1,192 `other`** intact faces unparsed:

1. **`SLOT` (`002, 060, 741, 742, 368, 365`) is a Postpositional Clause Linker / Medial Closer (260+ `loose name text` + 67 `other` faces).**
   `FRAME v2` permitted `SLOT` only once after an `OPEN` word (`OPEN SLOT?`). In Lipi:
   - Double-slot headers (`920-060-741`, `920-060-742`, `817-368-060`, `260-368-002`) occur on **22+ intact faces** (`OPEN SLOT SLOT NS+ CLOSER`).
   - Medial `002`, `741`, `742`, `060`, and `368` link a front phrase or commodity clause directly to a main closed clause (`NS+ SLOT NS+ CLOSER (TITLE)?` = **213 faces** in `loose name text` alone!). Crucially, **`741` and `742` (marked variants of the `740` jar) function as medial/subordinate clause closers** parallel to final `740`: e.g. `125-406-741 | 590-406-740`, `728-390-741 | 240-590-390-740`, and `066-741 | 235-495-017-740`.
2. **Multi-Clause / Compound Inscriptions (~250 `loose name text` + ~90 `other` faces).**
   Long seals, miniature tablets, and copper tablets juxtapose two or three complete clauses:
   - `[Name Clause] + [Name Clause]`: e.g. `032-877-740 | 001-468-806-154`, `440-740-400 | 840-712`.
   - `[Goods / Measure Clause] + [Name Clause]` and `[Name Clause] + [Goods / Count Clause]`: e.g. `072-740 | 590-407`, `240-705-033 | 550-525-400`, `235-705-033-845-407 | 321-407` (`14` copper tablets).
   - `[Prefix] + [OPEN-headed Clause]`: e.g. `803-415-220-318 | 920-255-436-690-590-407-740` (`11` tablets), `317 | 920-002-016-740`, plus direct `OPEN + CLOSER/TITLE` clauses (`550-527`, `861-740-400`, `920-740`) and stacked closing complexes (`740-090-400`, `400-740`, `740-151`).
3. **Qualified Commodity Clauses, Vessel Tallies, and Mirror-Incised Tablets (~390 `other` faces).**
   - **173 intact faces** end in `THING` (`390, 405, 407, 156, 700`) preceded by a place, measure, crest, or short stem rather than bare strokes (`798-240-845-061-407`, `415-390`, `510-460-156`, `820-060-142-156`).
   - **68 miniature tablets and pots** write vessel-first capacity tallies (`700-033` ×32, `700-032` ×18, `700-034` ×14, `700-031` ×2, `700-032-032` ×2).
   - **29 miniature tablets** write counted house/unit `003-861` (`NUM_SHORT + OPEN`), and **20 miniature tablets/bangles** are mirror-incised left-to-right with `OPEN` at the right edge (`413-892-824` ×11 vs. normal `824-892-413`; `415-578-032-824` ×4).
   - **254 single-sign shorthand marks** on pots, tablets, tools, and seals denote standalone numerals, vessels, measures, or potter's emblems (`032` ×47, `031` ×43, `033` ×24, `700` ×12, `002` ×12, `390` ×11).
4. **Catalogue-Adjacent Functional Signs Defaulted to `PERSONAL` in `v2` (69 Lipi-CV-validated moves).**
   `FRAME v2` missed sibling variants whose Lipi positional profile and 5-fold CV likelihood gain unambiguously place them in closed functional classes:
   - **`MEASURE` (+10 moves)**: `706` (`[U with stroke variant]`, sibling of `705`, `51.5%` immediately before numerals, **+0.01095 bits/sign** #1 CV gain), `590` (`[box with bar]`, **+0.00374**), `844`, `371`, `711` (`100%` before `033-700` count clause), `999` (`75%` before numerals), `272`, `321`, `746`, `019`.
   - **`NAME_BACK` (+19 moves, `67%–100%` immediately before `CLOSER/TITLE`)**: `176` (`66.7%` pre-ending, **+0.00669**), `923` (`93.3%`, **+0.00546**), `336` (`88.9%`), `772` (`100%`), `773` (`100%`), `636` (`78.6%`), `101` (`87.5%`), `222` (`100%`), `337` (`88.9%`), `927` (`88.9%`), `642` (`80%`), `384` (`66.7%`), `048` (`90%`), `177` (`100%`), `443` (`100%`), `531`, `637`, `912`, `067`, `229`.
   - **`THING` (+9 moves)**: `226` (`64%` final, `52%` after numerals, **+0.00467**), `617` (`64.3%` final across 60 intact faces, **+0.00080**), `064` (`77.8%` final, **+0.00183**), `422` & `423` (`100%` and `83.3%` after `NUM_SHORT`, siblings of `426`), `215`, `592`, `136` (`80%` final), `130`.
   - **`CLOSER` (+4 moves) & `TITLE` (+6 moves)**: `526` (`100%` final, sibling of `527`), `153` (`80%` final, porter sibling of `151/154`), `804` (`100%` final or pre-title), `159`; `401` (`80%` final, comb sibling of `400`), `697`, `600`, and post-measure finals `167` (`84.6%` final), `868` (`100%` final), `200` (`100%` final).
   - **`OPEN` (+13 moves, `67%–100%` clause-initial, typically before `SLOT`)**: `201` (`100%` initial in `201-060-...`), `347` (`8/9` in `347+SLOT`), `263` (`263-365`), `634` (`634-368`), `853` (`90%` initial), `146` (`146-742`), `260` (`260-368-002`), `345`, `922`, `698`, `502`, `910`, `370`.

---

## 2. Step-3 Tightening Redesign (`v3a initial` → `v3 final`) & Rival Tests

Our first broad multi-clause grammar (`v3a initial`) included unconstrained boustrophedon reversal on all object kinds, bare `OPEN + NS{1,2}` without `SLOT`, `PERSONAL` inside `MEASURE` followers, and `NUM + PERSONAL` capacity marks. While `v3a initial` hit **89.50%** on Lipi (`69.30%` on unseen `new texts`), per-rule decoy ablation revealed that those four permissive branches let decoy mean rise to **40.95%**.

In `v3 final` (`fv3_02_grammar.py`), we eliminated unconstrained boustrophedon, required explicit `SLOT{1,2}` on `header_clause`, removed `PERSONAL` as a `MEASURE` follower, and restricted 2- and 3-clause compounds to boundary-anchored clauses (`CLOSER/TITLE`, `THING`, `MEASURE + NUM/AFTER_M`, `OPEN + SLOT`). Decoy mean dropped by **11.49 percentage points** (`40.95% → 29.46%`) while real Lipi coverage held above **87.1%** across both all faces and length ≥ 3, raising decoy separation from `+48.55` pp ($z = 5.26$) to **`+57.68` pp ($z = 5.91$)**.

### Table 1 — Strict Parse Coverage: Real vs. 20 Frequency-Band Decoys & 20 Order Shuffles

| Grammar | Dataset | Subset | $N$ | Real Parse | Decoy Mean (SD) | Decoy Max | Real − Decoy | $z$ (Decoy) | $P$-value | Decoys ≥ Real | Order-Shuf Mean |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `v2 base` | Lipi intact | All | 3,600 | 50.47% | 7.96% (6.24%) | 20.86% | +42.51% | 6.82 | 4.65e-12 | 0 / 20 | 16.78% |
| `v2 base` | Lipi intact | Length ≥ 3 | 2,263 | 49.93% | 6.25% (8.00%) | 21.56% | +43.69% | 5.46 | 2.37e-08 | 0 / 20 | 8.78% |
| `v2 base` | Unseen `new texts` | All | 482 | 29.88% | 9.35% (4.87%) | 20.75% | +20.53% | 4.22 | 1.24e-05 | 0 / 20 | 12.47% |
| `v2 base` | Unseen `new texts` | Length ≥ 3 | 290 | 33.10% | 5.43% (6.34%) | 19.31% | +27.67% | 4.36 | 6.45e-06 | 0 / 20 | 7.10% |
| `v3a initial` | Lipi intact | All | 3,600 | 89.50% | 40.95% (9.22%) | 59.61% | +48.55% | 5.26 | 7.23e-08 | 0 / 20 | 59.85% |
| `v3a initial` | Unseen `new texts` | All | 482 | 69.30% | 41.18% (6.65%) | 57.26% | +28.11% | 4.23 | 1.19e-05 | 0 / 20 | 48.54% |
| **`v3 final`** | **Lipi intact** | **All** | **3,600** | **87.14%** | **29.46% (9.76%)** | **49.03%** | **+57.68%** | **5.91** | **1.74e-09** | **0 / 20** | **46.47%** |
| **`v3 final`** | **Lipi intact** | **Length ≥ 3** | **2,263** | **87.19%** | **23.92% (13.97%)** | **53.20%** | **+63.26%** | **4.53** | **2.93e-06** | **0 / 20** | **29.53%** |
| **`v3 final`** | **Lipi intact** | **Admin len ≥ 3 (no pot/other)** | **2,172** | **88.03%** | **23.83% (14.26%)** | **53.91%** | **+64.20%** | **4.50** | **3.35e-06** | **0 / 20** | **29.18%** |
| **`v3 final`** | **Lipi events (dedup)** | **All** | **2,855** | **84.17%** | **29.04% (10.77%)** | **50.68%** | **+55.13%** | **5.12** | **1.49e-07** | **0 / 20** | **39.50%** |
| **`v3 final`** | **Lipi events (dedup)** | **Length ≥ 3** | **2,003** | **85.62%** | **23.64% (13.81%)** | **51.97%** | **+61.98%** | **4.49** | **3.62e-06** | **0 / 20** | **28.34%** |
| **`v3 final`** | **Lipi distinct texts** | **Length ≥ 3** | **1,705** | **83.34%** | **23.31% (13.59%)** | **50.09%** | **+60.04%** | **4.42** | **4.98e-06** | **0 / 20** | **26.60%** |
| **`v3 final`** | **Unseen `new texts`** | **All** | **482** | **64.94%** | **34.61% (8.06%)** | **53.32%** | **+30.33%** | **3.76** | **8.41e-05** | **0 / 20** | **38.87%** |
| **`v3 final`** | **Unseen `new texts`** | **Length ≥ 3** | **290** | **64.83%** | **22.93% (11.90%)** | **48.28%** | **+41.90%** | **3.52** | **2.14e-04** | **0 / 20** | **24.31%** |
| **`v3 final`** | **Unseen `new texts`** | **Admin len ≥ 3 (no pot/other)** | **276** | **64.85%** | **22.39% (11.86%)** | **47.46%** | **+42.46%** | **3.58** | **1.73e-04** | **0 / 20** | **23.50%** |
| **`v3 final`** | **Unseen all complete** | **All (incl. Mah-only `X` signs)** | **627** | **59.01%** | **32.03% (7.22%)** | **48.01%** | **+26.98%** | **3.74** | **9.10e-05** | **0 / 20** | **35.53%** |
| **`v3 final`** | **Unseen all complete** | **Length ≥ 3** | **357** | **61.62%** | **22.20% (10.99%)** | **44.82%** | **+39.43%** | **3.59** | **1.66e-04** | **0 / 20** | **23.50%** |

### Table 2 — Coverage by Object Kind (`FRAME v2` vs. `FRAME v3`)

| Object Kind | Lipi $N$ | Lipi `v2` | Lipi `v3` | Lipi `v3` Decoy Mean | Unseen `new` $N$ | Unseen `v2` | Unseen `v3` | Unseen `v3` Decoy Mean |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Seals | 1,540 | 46.5% | **81.8%** | 23.6% | 269 | 29.4% | **66.2%** | 27.4% |
| Tags & sealings | 78 | 42.3% | **91.0%** | 31.0% | 89 | 32.6% | **56.2%** | 31.3% |
| Miniature tablets | 1,358 | 64.1% | **92.8%** | 24.5% | 50 | 24.0% | **64.0%** | 44.0% |
| Copper tablets | 196 | 60.7% | **96.4%** | 29.4% | 22 | 45.5% | **59.1%** | 33.6% |
| Pots | 297 | 17.2% | **86.2%** | 71.0% | 41 | 29.3% | **78.0%** | 70.1% |
| Other (tools/bangles/rods) | 131 | 20.6% | **77.1%** | 54.8% | 11 | 18.2% | **72.7%** | 64.1% |

---

## 3. Held-Out Next-Sign Cross-Entropy & Fill-the-Gap (`fv3_03_eval.py`)

### Table 3 — Held-Out Next-Sign Cross-Entropy (Bits per Sign; Lower Is Better)

| Model | Classes | Lipi 5-Fold CV | Lipi Nested 5-Fold CV | Lipi Half-B Pooled | Lipi Half-B By-Kind | Unseen `new` (482) Pooled | Share of Bigram Gain | Unseen Decoy Mean (Best) | Decoys ≤ Real | $z$ ($P$-value) | Unseen Seals | Mix w/ Bigram |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Unigram | 1 | — | — | — | — | 7.8489 | 0.0% | — | — | — | — | — |
| Sign bigram | 417 | — | — | — | — | 6.8918 | 100.0% | — | — | — | — | — |
| `v1 hand jobs` | 10 | 7.1735 | — | 7.4032 | 7.3741 | 7.6614 | 19.6% | 7.8239 (7.7390) | 0 / 20 | 3.70 (1.1e-4) | 7.5401 | 6.9182 |
| `v2 base` | 14 | 6.9456 | — | 7.1752 | 7.1434 | 7.5362 | 32.7% | 7.7904 (7.6715) | 0 / 20 | 5.10 (1.7e-7) | 7.3739 | 6.8805 |
| **`v3 final`** | **14** | **6.8445** | **6.8847** | **7.0772** | **7.0430** | **7.5313** | **33.2%** | **7.7924 (7.6871)** | **0 / 20** | **5.76 (4.3e-9)** | **7.3413** | **6.8833** |

---

## 4. Major Clause Templates & Real Segmented Inscriptions (`v3_clause_breakdown.csv`)

| Clause Pattern (`FRAME v3`) | Lipi Intact | Share | Unseen Mah. Complete | Segmented Lipi Example | Segmented Unseen Mahadevan Example |
|---|---:|---:|---:|---|---|
| `name_clause` | 1,388 | 38.6% | 146 | `235-740` | `861-002-X153-X153-415-220-520` |
| `count_clause` | 527 | 14.6% | 2 | `017-410` | `001-550` |
| `single_mark` | 191 | 5.3% | 59 | `007` | `705` |
| `goods_clause` | 160 | 4.4% | 22 | `510-460-156` | `615-615-745-235-X158-405` |
| `compound:header_clause+name_clause` | 119 | 3.3% | 11 | `066-741 \| 235-495-017-740` | `031-X55-861-002 \| 055-233-705-033-520` |
| `header_clause` | 70 | 1.9% | 10 | `820-002-236` | `861-002-717-705-892` |
| `slot_linked+name_clause` | 70 | 1.9% | 5 | `741-298-002 \| 717-140-740` | `032-575-032-002 \| 705-760-740` |
| `vessel_tally` | 68 | 1.9% | 0 | `700-033` | — |
| `pot_tool_mark` | 63 | 1.8% | 13 | `234` | `X69` |
| `compound:goods_clause+name_clause` | 52 | 1.4% | 0 | `125-406 \| 741-590-406-740` | — |
| `front_alone` | 32 | 0.9% | 10 | `817-002` | `820` |
| `prefix+open_closed_clause` | 29 | 0.8% | 3 | `031 \| 920-400-740` | `031 \| 698-151` |
| `compound:name_clause+name_clause` | 27 | 0.8% | 2 | `001-900-165-400 \| 255-400` | `095-740 \| 176-740-090` |
| `measure_clause` | 25 | 0.7% | 5 | `032-999-031` | `705-033-032` |
| `one_picture` / `title_alone` / `open_closed` | 68 | 1.9% | 41 | `782` / `679` / `698-400` | `X363` / `740` / `920-740` |
| `prefix+name_clause` | 21 | 0.6% | 1 | `803-415-220-318 \| 920-255-436-690-590-407-740` | `806-415-220-320 \| 920-255-435-690-590-390-740` |
| `mirror_tablet_open` | 20 | 0.6% | 0 | `415-578-032-824` | — |
| `compound:name_clause+count/goods` | 29 | 0.8% | 5 | `413-575-335-740 \| 032-700` | `838-798-176-740-151 \| 700-700-700-390` |
| Other 2- and 3-clause compounds | 178 | 4.9% | 35 | `817-002-806 \| 235-233-555-527 \| 061-405` | `717-X309-861-002 \| 806-233-003-900-790-900-740 \| X145-845-405` |
| **Total Parsed (`FRAME v3`)** | **3,137** | **87.14%** | **370 / 627** (`313 / 482` = **64.94%**) | | |

---

## 5. Artifacts & Reproducibility

- **Scripts**:
  - `work_scripts/fv3_01_audit.py` — Lipi-only structural audit of the 591 `loose name text` and 1,192 `other` faces + single-sign 5-fold CV profile scan.
  - `work_scripts/fv3_02_grammar.py` — Lipi 5-fold CV role-consistent class learner + `parse_v3` / `parse_v3_initial` clause segmenters and per-sign role tagger.
  - `work_scripts/fv3_03_eval.py` — Full coverage, 20-decoy, 20-order-shuffle, nested 5-fold CV, Half-B, unseen `new texts` cross-entropy, 77-gap evaluation, and 9,252-row corpus export.
- **Data (`work_data/fv3/`)**:
  - `classes_v3.csv` — 417+ Lipi signs with `v2_base`, `v3_class`, counts, and positional rates.
  - `cv_class_moves.csv` — Sequential 5-fold Lipi CV gains for all 69 role-consistent class moves.
  - `corpus_parsed_v3.csv` — Every Lipi (`5,679`) and Mahadevan (`3,573`) inscription segmented into clauses and sign roles.
  - `v3_coverage_eval.csv`, `v3_bits_eval.csv`, `v3_gap_eval.csv`, `v3_clause_breakdown.csv` — Complete evaluation tables.
