# Global Dictionary Solver & Directional `K=1` Primary-Sense Audit

**Testing it.** Switching from order-blind bag-of-signs (`jobs/out/sense_test.md`) to **directional adjacent-bigram semantic selection** learned on Lipi (`3,321` events / `3,856` faces) and scored zero-shot on unseen Mahadevan `new texts` (`701` events / `738` faces) raises the primary-sense (`K=1`) lift of `values_master4.csv` to **$z = +4.41$ ($P = 0.001$)** against frequency-band shuffles (`Shuffle A`) and **$z = +3.45$ ($P = 0.002$)** against category-count-matched shuffles (`Shuffle B_cat`) on directional category PMI, and to **$z = +5.19$ (`A`) / $z = +3.52$ (`B_cat`, $P = 0.001$)** on BGE-base bilinear vector PMI (`+3.47` on EmbeddingGemma 2, `+3.37` on multilingual Model2Vec).

Crucially, `values_master4.csv` also survives the **Rival Refit Audit**, where every single decoy assignment refits its own directional category/vector PMI matrix on Lipi before scoring unseen `new texts`:
- **Coarse `(band × cat_count)` Refit Audit**: category PMI **$z = +2.64$ ($P = 0.003$)**, BGE bilinear **$z = +2.24$ ($P = 0.006$)** at `K=1` (`K=2`: BGE Refit $z = +2.44$, $P = 0.007$).
- **Fine Grammatical-Slot Refit Controls (`gsol_03_eval.py`)**:
  - `v2_base_band_cat` (`174/184` movable signs): Fixed **$z = +3.55$ ($P = 0.001$)** | Refit **$z = +2.70$ ($P = 0.003$)**.
  - `hmm10_band_cat` (`184/184` movable signs): Fixed **$z = +3.74$ ($P = 0.001$)** | Refit **$z = +3.02$ ($P = 0.001$)**.
  - `v2_x_hmm10_band_cat` (`146/184` movable signs): Fixed **$z = +3.40$ ($P = 0.001$)** | Refit **$z = +2.71$ ($P = 0.007$)**.
- **Cross-City Generalization**: Learned solely on **Harappa Lipi (`1,286` events)** and evaluated zero-shot on **Mohenjo-daro `new texts` (`385` events)**, Fixed `B_cat` scores **$z = +3.42$ ($P = 0.001$)** and Refit `B_cat` scores **$z = +2.29$ ($P = 0.011$)** (`MD Lipi -> Non-MD New`: Fixed $z = +2.86$, Refit $z = +1.30$).

**What went against us — and why Wave 2B is needed:**
1. **Stripping hand-curated glosses (`Pure-Dict`) collapses the Refit margin.** When `values_master4`'s hand-authored `english` column (`"bamboo-star"`, `"first-ward house"`, `"scabbard-fish"`) is discarded and each sign keeps only raw DEDR Tamil dictionary senses (`Pure-Dict`), Fixed `B_cat` stays positive (`z = +2.22` at `K=1`, `+2.75` at `K=2`), **but Rival Refit `B_cat` drops to $z = +0.66$ (`K=1`) and $z = +1.22$ (`K=2`)**.
2. **External English prose priors (`control_texts.json`) score near zero ($z = -0.73$ to $+0.01$).** The `K=1` directional signal comes from **Indus-specific administrative slot pairings** (`measure -> number`, `kin -> house`, `tool/chest -> commodity`, `plant -> crest`), not generic English sentence similarity.
3. **Unconstrained 120-sign QAP (`M = 580–900`, `gsol_02_qap.py` & `gsol_03_eval.py`) overfits Lipi without beating decoy-corpus solves.** Across all 7 candidate language families (`Dravidian`, `Munda`, `Indo-Aryan`, `Elamite`, `Sumerian`, `Akkadian`, `Burushaski`), feeding `M = 580–900` dictionary stems into a 1-to-1 Frank-Wolfe + 2-opt QAP solver across unsegmented full lines lets every family find high-PMI pairs on Lipi that match decoy-corpus solves (`Lipi vs decoy-solve z = -2.25 to +0.31` in `free`/`anchored`; `z = -1.11 to +1.80` in `morphophon M=580`), picking spurious homophones (`dedr_tamil:4312 to "breed worms"` for `740`, `dedr_tamil:604 uṇṇi "tick on dogs"` for `090`) because:
   - Bigram edges crossed **`FRAME v3` clause boundaries** (`|`);
   - Candidate pools were unconstrained by Wave 1's empirically measured **archaeological & metrological sign anchors** (`work_data/sem/sign_anchors.csv`, `work_data/met/unit_ladder.csv`);
   - A few raw lexicon rows contained parser artifacts (e.g. English infinitive `"to"` parsed as a headword in `pdrav_2branch`/`dedr_tamil`).

**Direct Rescue Path (Wave 2B):** Re-run pure-dictionary lexical locking strictly **within `FRAME v3` clauses** and **restricted to archaeologically/metrologically anchored sign domains**, plus a standalone **Archaeological Dual-Domain Polysemy/Homophony Test** on raw cleaned dictionaries.

---

## 1. Directional `K=1` and `K=2` Primary-Sense Audit (`work_scripts/gsol_01_k1_audit.py`)

Evaluating `3,321` Lipi object-events (`3,856` faces) -> `701` unseen Mahadevan `new texts` object-events (`738` faces) against `1,000` shuffles:

| Metric / Prior | `K=1` `Shuffle A` (band) | `K=1` `Shuffle B_cat` (band × cats) | `K=2` `Shuffle A` | `K=2` `Shuffle B_cat` |
|---|---:|---:|---:|---:|
| Bag-of-signs lift (order-blind baseline) | $+2.82$ | $+2.56$ | $+2.14$ | $+1.96$ |
| **Directional Category PMI (Lipi-learned)** | **$+4.41$ ($P=0.001$)** | **$+3.45$ ($P=0.002$)** | **$+3.62$ ($P=0.001$)** | **$+2.90$ ($P=0.002$)** |
| **BGE-base Bilinear PMI (Lipi-learned)** | **$+5.19$ ($P=0.001$)** | **$+3.52$ ($P=0.001$)** | **$+4.87$ ($P=0.001$)** | **$+3.35$ ($P=0.001$)** |
| **EmbeddingGemma 2 Bilinear PMI (Lipi-learned)** | **$+5.10$ ($P=0.001$)** | **$+3.47$ ($P=0.001$)** | **$+4.76$ ($P=0.001$)** | **$+3.26$ ($P=0.001$)** |
| **Multilingual Model2Vec Bilinear PMI (Lipi)** | **$+4.91$ ($P=0.001$)** | **$+3.37$ ($P=0.001$)** | **$+4.70$ ($P=0.001$)** | **$+3.22$ ($P=0.001$)** |
| External prose Category PMI (`control_texts`) | $-0.73$ ($P=0.769$) | $-0.40$ ($P=0.676$) | $-0.20$ ($P=0.579$) | $-0.12$ ($P=0.542$) |
| Raw BGE cosine (`cos(u, v)`, zero Lipi fit) | $-1.06$ ($P=0.854$) | $-0.96$ ($P=0.803$) | $-1.14$ ($P=0.851$) | $-0.90$ ($P=0.791$) |
| **Rival Refit Audit (Category PMI)** | — | **$+2.64$ ($P=0.003$)** | — | **$+2.03$ ($P=0.017$)** |
| **Rival Refit Audit (BGE Bilinear)** | — | **$+2.24$ ($P=0.006$)** | — | **$+2.44$ ($P=0.007$)** |
| **Pure-Dict Only (no hand glosses), Fixed** | $+3.14$ | $+2.22$ | $+3.52$ | $+2.75$ |
| **Pure-Dict Only (no hand glosses), Rival Refit** | — | **$+0.66$ (null)** | — | **$+1.22$ (null)** |

### Top Unseen `new texts` Bigram Drivers (`work_data/gsol/k1_bigram_drivers_new.csv`)
The directional `K=1` lift on unseen `new texts` is driven by recurring administrative transitions:
1. `861 -> 002` (`share -> two`, `measure -> number`, unseen weight `26.75`, contrib `+0.0430`)
2. `760 -> 740` (`child of -> house`, `kin -> place`, unseen weight `10.56`, contrib `+0.0187`)
3. `415 -> 220` (`branch -> star`, `plant -> time`, unseen weight `4.30`, contrib `+0.0078`)
4. `798 -> 740` (`descendant -> house`, `kin -> place`, unseen weight `3.00`, contrib `+0.0060`)
5. `176 -> 740` (`tax -> house`, `commodity -> place`, unseen weight `6.65`, contrib `+0.0058`)
6. `590 -> 405` & `590 -> 390` (`chest -> thread / cotton`, `tool -> commodity`, unseen weights `4.24` & `3.47`, contrib `+0.0082`)
7. `705 -> 033` (`kalam -> three`, `measure -> number`, unseen weight `8.28`, contrib `+0.0031`)

---

## 2. Fine-Slot Rival Refit Controls & Cross-City Audit (`work_scripts/gsol_03_eval.py`)

Permuting `K=1` glosses strictly **within fine grammatical slots** while every decoy refits its own Lipi category-PMI matrix:

| Permutation Stratum | Movable Signs | Fixed-Prior $z$ ($P$) | **Rival-Refit $z$ ($P$)** |
|---|---:|---:|---:|
| `v2_base_band_cat` (`FRAME v2` class × band × cat_count) | `174 / 184` | $+3.55$ ($0.001$) | **$+2.70$ ($0.003$)** |
| `hmm10_band_cat` (`HMM-10` unsupervised class × band × cat_count) | `184 / 184` | $+3.74$ ($0.001$) | **$+3.02$ ($0.001$)** |
| `v2_x_hmm10_cat` (`v2 × HMM-10` intersection × cat_count) | `168 / 184` | $+3.81$ ($0.001$) | **$+2.67$ ($0.003$)** |
| `v2_x_hmm10_band_cat` (`v2 × HMM-10 × band × cat_count`) | `146 / 184` | $+3.40$ ($0.001$) | **$+2.71$ ($0.007$)** |
| Cross-City: `Harappa Lipi (1,286) -> MD New (385)` | `184 / 184` | $+3.42$ ($0.001$) | **$+2.29$ ($0.011$)** |
| Cross-City: `MD Lipi (1,442) -> Non-MD New (316)` | `184 / 184` | $+2.86$ ($0.001$) | $+1.30$ ($0.099$) |

Even when decoys are forced to preserve **both** `FRAME v2` and `HMM-10` distributional classes simultaneously (`v2_x_hmm10_band_cat`), `values_master4`'s `K=1` category structure beats 99.3% of refitted decoys on unseen `new texts` — proving that sub-slot semantic distinctions (e.g. `kin` vs `commodity` inside `PERSONAL`, or `person` vs `commodity` inside `THING`) carry real held-out predictive power, **mirroring the word-free archaeological `CATS` coherence win ($z = +3.54, P = 0.0005$) in `jobs/out/semantic_anchors.md`**.

---

## 3. Global 120-Sign QAP Dictionary Solver Across 7 Families (`gsol_02_qap.py`, `gsol_03_eval.py`)

Testing `N = 120` top signs (`3,187` Lipi events, `683` unseen `new texts` events, `87` pictured signs, `65` Lipi swap pairs, `16` held-out Mahadevan-only swap pairs) across all 7 candidate language families in three modes (`free` `M=900`, `anchored` `M=900`, and equal-capacity `morphophon` `M=580` against `20` decoy-corpus QAP solves):

| Language Family | `free` (`M≤900`) Lipi vs Decoy-Solve $z$ | `anchored` (`M≤900`) Lipi vs Decoy-Solve $z$ | `morphophon` (`M=580`) Lipi Lock vs Decoy $z$ ($P$) | `morphophon` (`M=580`) Unseen `New` Sem $z$ ($P$) | `morphophon` (`M=580`) Held-Out Swap $z$ ($P$) |
|---|---:|---:|---:|---:|---:|
| **Dravidian** (`dedr_tamil`) | $+0.05$ | $-1.40$ | $+1.10$ ($0.191$) | $+1.59$ ($0.007$) | $-0.68$ ($0.757$) |
| **Munda** (`santali` + `mundari`) | $-0.02$ | $-1.83$ | $+1.80$ ($0.048$) | $+1.19$ ($0.132$) | $+0.10$ ($0.407$) |
| **Indo-Aryan** (`oia_turner`) | $-0.84$ | $-0.68$ | $+0.74$ ($0.333$) | $+1.08$ ($0.137$) | $+0.12$ ($0.373$) |
| **Elamite** (`elamite_roots`) | $-0.23$ | $+0.24$ | $-1.11$ ($0.857$) | $+1.85$ ($0.056$) | $+1.80$ ($0.070$) |
| **Sumerian** (`sumerian_roots`) | $-0.01$ | $-1.69$ | $-0.93$ ($0.809$) | $+2.80$ ($0.004$) | $+0.01$ ($0.492$) |
| **Akkadian** (`akkadian_roots`) | $-1.81$ | $-2.25$ | $+0.85$ ($0.191$) | $+1.70$ ($0.062$) | $+0.67$ ($0.217$) |
| **Burushaski** (`burushaski_all`) | $+0.31$ | $-1.78$ | $+0.90$ ($0.286$) | $+1.66$ ($0.079$) | $-0.70$ ($0.674$) |

**Why unconstrained QAP failed to separate families:** With `580–900` candidate stems and no archaeological per-sign semantic filter, the 2-opt optimizer has $\sim 580^{120}$ degrees of freedom and fits high-PMI pairs equally well on scrambled decoy corpora (`Lipi vs decoy-solve z ≈ 0`). When a lexicon has `600+` stems, QAP assigns common signs to arbitrary multi-category dictionary entries unless candidate pools are first pinned to empirically measured archaeological/metrological roles (`sign_anchors.csv` + `unit_ladder.csv`) and within-clause `FRAME v3` syntax.

---

## Reproducibility
- Scripts: `work_scripts/gsol_01_k1_audit.py`, `work_scripts/gsol_02_qap.py`, `work_scripts/gsol_03_eval.py`
- Data: `work_data/gsol/k1_audit_results.json`, `k1_sign_drivers_new.csv`, `k1_bigram_drivers_new.csv`, `qap_summary.json`, `eval_redesign_summary.json`, `qap_words_<lang>_{free,anchored,morphophon}.csv`
