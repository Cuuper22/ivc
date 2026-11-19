# Key #6C — Publication-Ready Master Verification Audit

Generated directly from `work_scripts/reproduce_all_keys.py` (runtime: ~37s, exit code `0`, zero hardcoded headline numbers).

## 1. Script & On-Disk Artifact Integrity

- **Scripts checked (`py_compile`):** **18/18 PASS** (`gulf3_audit_and_ventris.py`, `gulf3_redesign_lock.py`, `key2a_rebus_lock.py`, `key2a_rival_audit.py`, `key2b_ur_failaka.py`, `key2c_elamite_bridge.py`, `key3a_sound_sweep.py`, `key3b_gulf_ur3_audit.py`, `key4a_ligatures.py`, `key4b_bootstrap_wave2.py`, `key4c_sangam_epigraphy.py`, `key4d_allographs.py`, `key4e_museum_archives.py`, `key4_master_merge.py`, `key5a_big_six_strike.py`, `key5b_reader_and_network.py`, `reproduce_all_keys.py`, plus `key5a` / `key4b` helper imports).
- **Headline claims audited:** **40/40** extracted programmatically from disk JSON/CSV artifacts (`all_artifacts_verified_on_disk = True`).
- **Honest nulls registered:** **30** documented negative/non-significant results compiled in `work_data/key6c/honest_null_registry.csv`.
- **Preprint manuscript:** `/home/antigravity/Cuuper22/ivc/PAPER_DRAFT.md` (**6,432 words**, 10 sections: Abstract + §§1–9, 4 verified tables, 10 cross-checked landmark inscriptions).

---

## 2. Invariant 1 — Exact 3-Wave Disjointness Audit (Discrepancy Caught)

Programmatic set-intersection across the raw sign sets on disk (`work_data/key2a/test_a2_matched_words.csv`, `work_data/key4b/test4b1_per_sign_scores.csv`, `work_data/key5a/trackA_13signs_summary.csv`) caught **6 overlapping signs** across the three published phonetic waves (`12 + 30 + 13 = 55` tests across `49` unique signs):

- **Wave-1 $\cap$ Wave-3:** `∅` (**0 signs**, 100% disjoint).
- **Wave-1 $\cap$ Wave-2:** **1 sign (`861`)** — included in Key #2A `A2c` UltraClean-12 (outside Key #2A's 11-sign core lock) and re-entered Key #4B Top-30 (`PhonSt=True`, `PhonEx=False`).
- **Wave-2 $\cap$ Wave-3:** **5 signs (`060, 142, 240, 550, 798`)** — the Big-Six bottlenecks that failed Wave-2 Key #4B (`0/5` `PhonEx`, `1/5` `PhonSt` on `798`) and were re-tested with redesigned visual/semantic domains in Wave-3 Key #5A (`240, 550, 798` subsequently locked; `060` locked via grammar; `142` remained open).
- **Cross-Key Note:** Wave-3 sign `416` also had `strictly_novel = False` with respect to Key #3A's 20-sign bootstrap.

### Resolution (Live 5,000-Shuffle Strictly Pairwise-Disjoint Rerun)
`reproduce_all_keys.py` strips all 6 overlaps and executes a fresh 5,000-shuffle 7-family `Single-Headword` permutation run on the **44 strictly pairwise-disjoint signs (`12 + 24 + 8`, 0% overlap)** and an **ultra-disjoint 43-sign set (`12 + 24 + 7`, also excluding `416`)**.

---

## 3. Invariant 2 — Combined 3-Wave 7-Family Meta-Analysis (Fisher & Stouffer)

Removing the 6 overlapping signs **strengthens** Proto-Dravidian because the 5 Wave-2 $\cap$ Wave-3 signs were Wave-2 failures (`0/5` `PhonEx`), lifting Wave-2 disjoint to `23/24` (`PhonSt`, $P = 0.00020$) and `14/24` (`PhonEx`, $P = 0.00240$).

### Table A: Strictly Pairwise-Disjoint (`12 + 24 + 8 = 44` unique signs, ZERO overlap)

| Language Family | Mode | W1 (`12`) | W2 Disj (`24`) | W3 Disj (`8`) | Fisher $\chi^2_6$ | Fisher $P$ | Bonf-7 $P$ | Stouffer $Z_{\text{emp}}$ | Stouffer $Z_P$ |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Proto-Dravidian** | **`PhonSt`** | **9/12** (`0.0004`) | **23/24** (`0.0002`) | **5/8** (`0.0010`) | **46.50** | **$2.36 \times 10^{-8}$** | **$1.65 \times 10^{-7}$** | **+7.31** | **+5.76** |
| *Dravidian RawPDrav* | *`PhonSt`* | *9/12* (`0.0006`) | *22/24* (`0.0002`) | *5/8* (`0.0008`) | *46.13* | *$2.78 \times 10^{-8}$* | *$1.95 \times 10^{-7}$* | *+7.91* | *+5.74* |
| Indo-Aryan (OIA) | `PhonSt` | 1/12 (`0.1694`) | 2/24 (`0.1382`) | 0/8 (`1.0000`) | 7.51 | 0.2763 | **1.0000** | +2.05 | −0.97 |
| Sumerian | `PhonSt` | 3/12 (`0.1680`) | 5/24 (`0.3651`) | 0/8 (`1.0000`) | 5.58 | 0.4715 | **1.0000** | +0.75 | −1.39 |
| Elamite | `PhonSt` | 0/12 (`1.0000`) | 0/24 (`1.0000`) | 0/8 (`1.0000`) | 0.00 | 1.0000 | **1.0000** | −0.14 | −6.44 |
| Akkadian | `PhonSt` | 0/12 (`1.0000`) | 0/24 (`1.0000`) | 0/8 (`1.0000`) | 0.00 | 1.0000 | **1.0000** | −0.19 | −6.44 |
| Burushaski | `PhonSt` | 0/12 (`1.0000`) | 0/24 (`1.0000`) | 0/8 (`1.0000`) | 0.00 | 1.0000 | **1.0000** | −0.24 | −6.44 |
| Munda | `PhonSt` | 0/12 (`1.0000`) | 0/24 (`1.0000`) | 0/8 (`1.0000`) | 0.00 | 1.0000 | **1.0000** | −0.28 | −6.44 |
| **Proto-Dravidian** | **`PhonEx`** | **6/12** (`0.0038`) | **14/24** (`0.0024`) | **4/8** (`0.0002`) | **40.24** | **$4.08 \times 10^{-7}$** | **$2.85 \times 10^{-6}$** | **+7.09** | **+5.21** |
| *Dravidian RawPDrav* | *`PhonEx`* | *6/12* (`0.0016`) | *12/24* (`0.0038`) | *4/8* (`0.0004`) | *39.67* | *$5.29 \times 10^{-7}$* | *$3.70 \times 10^{-6}$* | *+7.50* | *+5.18* |
| Indo-Aryan (OIA) | `PhonEx` | 0/12 (`1.0000`) | 2/24 (`0.0574`) | 0/8 (`1.0000`) | 5.72 | 0.4558 | **1.0000** | +1.35 | −3.38 |
| Sumerian | `PhonEx` | 1/12 (`0.5693`) | 1/24 (`0.8630`) | 0/8 (`1.0000`) | 1.42 | 0.9645 | **1.0000** | −0.52 | −2.88 |
| Munda/Elamite/Akkadian/Burushaski | `PhonEx` | 0/12 | 0/24 | 0/8 | 0.00 | 1.0000 | **1.0000** | −0.16 to −0.10 | −6.44 |

### Table B: Sensitivity Regimes (Proto-Dravidian vs Best Rival)

| Regime | Mode | Proto-Dravidian Fisher $\chi^2_6$ | Fisher $P$ | Bonf-7 $P$ | Stouffer $Z_{\text{emp}}$ | Best Rival Bonf-7 $P$ |
|---|---|---:|---:|---:|---:|---:|
| **Strictly Disjoint (`12+24+8=44`)** | `PhonSt` | **46.50** | **$2.36 \times 10^{-8}$** | **$1.65 \times 10^{-7}$** | **+7.31** | 1.0000 (OIA `0.276`) |
| **Strictly Disjoint (`12+24+8=44`)** | `PhonEx` | **40.24** | **$4.08 \times 10^{-7}$** | **$2.85 \times 10^{-6}$** | **+7.09** | 1.0000 (OIA `0.456`) |
| **Ultra-Disjoint (`12+24+7=43`, excl. `416`)** | `PhonSt` | **43.28** | **$1.03 \times 10^{-7}$** | **$7.19 \times 10^{-7}$** | **+6.88** | 1.0000 (OIA `0.276`) |
| **Ultra-Disjoint (`12+24+7=43`, excl. `416`)** | `PhonEx` | **33.81** | **$7.33 \times 10^{-6}$** | **$5.13 \times 10^{-5}$** | **+6.26** | 1.0000 (OIA `0.456`) |
| Full Published Waves (`12+30+13`) | `PhonSt` | 45.11 | $4.45 \times 10^{-8}$ | $3.11 \times 10^{-7}$ | +6.71 | 1.0000 (OIA `0.290`) |
| Full Published Waves (`12+30+13`, `RawPDrav`) | `PhonSt` | 48.91 | $7.79 \times 10^{-9}$ | $5.45 \times 10^{-8}$ | +8.04 | 1.0000 (OIA `0.290`) |
| Full Published Waves (`12+30+13`) | `PhonEx` | 37.31 | $1.53 \times 10^{-6}$ | $1.07 \times 10^{-5}$ | +6.75 | 1.0000 (OIA `0.485`) |

---

## 4. Invariant 3 — Unseen Holdout Parity Audit (Subtle Quirk Caught)

- **Cleanly Crosswalked Tiers (Key #4 Master `T0–T6` + Key #5A `T5_Before–T6`, `563` unseen intact faces): 11/11 PASS (`100%`)**
  - Every tier strictly satisfies `Unseen Token % >= Lipi Token %` (margin **`+0.22` to `+4.46 pp`**) and `Unseen 100%-Decoded % >= Lipi 100%-Decoded %` (margin **`+0.39` to `+8.30 pp`**).
  - Final Locked 140-sign Lexicon: **82.85% unseen** vs **82.07% Lipi** (`+0.78 pp`; combined **82.17%**); **57.73%** unseen vs **53.81%** Lipi 100%-decoded faces (combined **2,262 / 4,163 = 54.34%**).
- **Subtle Pre-Filter Discrepancy Caught in Key #3A:** Key #3A evaluated the raw `627`-face unseen set before Key #4 Master removed 64 faces containing unmapped Mahadevan-only `X` tokens. Those `X` tokens inflated Key #3A's unseen token denominator, producing slight negative diffs on two raw tiers (`Locked-11`: `22.49%` vs `22.69%`, `-0.20 pp`; `11+Loans+BNums`: `38.27%` vs `40.28%`, `-2.01 pp`), even while 100%-decoded unseen face share already beat Lipi (`10.37%` vs `7.22%`, `+3.15 pp`). Removing the 64 unmapped-`X` faces flips Key #3A (`T0_Baseline_K3A`) immediately to positive (`45.79%` vs `45.57%`, `+0.22 pp`).

---

## 5. Invariant 4 — Honest Null Registry (`30` Documented Nulls)

All **30** documented nulls/negative controls across Keys #1–#5B are logged in `work_data/key6c/honest_null_registry.csv`, including:
- Key #1: 5-language Gulf pictographic acrophony null ($P = 0.46–1.00$).
- Key #2A: Auto-Tier1 unfiltered 51-sign null ($P = 0.629$); strict 10-word Near-East loanword standalone null ($P = 0.528$).
- Key #2B: DKG.(S) `415-220` null ($P = 0.849$); `803-415` collapsed unique-matrix power null ($P = 0.121$).
- Key #2C: Linear Elamite visual-transfer phonetic null (`0` exact hits, $P = 0.266–1.00$); Proto-Elamite/Ur III capacity ladder coincidence null ($P = 0.551$).
- Key #3A: Within-11 exact bigram permutation null ($P = 0.767$); sign `850` unseen copper null (`0/13`, $P = 1.00$).
- Key #3B: Post-flip Gulf `MAN → Deity` ordering null ($P = 0.212 / 0.499$); 6 foreign Ur III Meluhhan PN phonetic null (`0` hits, $P = 1.00$).
- Key #4A: Three non-uniform diacritic operators (`internal_vert_stroke` $P = 0.841$, `roof_caret_hat` $P = 0.458$, `horiz_hatching` $P = 0.676$).
- Key #4B: Raw DEDR 1-blank sandwich null ($P = 0.770$).
- Key #4C: Within-19 Sangam token-mass permutation null ($P = 0.097$ Lipi / $0.103$ unseen).
- Key #4D: 67 catalogued visual `FALSE_MERGER` pairs (negative control degrades perplexity `5.3654 → 5.3858` bps).
- Key #4E: Expanded 11 foreign Meluhhan PNs (`0/7` families, Dravidian $P = 0.848$) & 21 trade words (`0/7`, $P = 0.408$); pooled Eastern Frontier bigrams ($P = 0.136$).
- Key #5A: Sign `692` honest null (`0` DEDR bridges); hatched `924`/`243` copper-tablet null (`0/9`, `0/12`, $P = 1.00$); open bottlenecks `142, 692, 585, 595, 527`.
- Key #5B: Stamp-seals-only city $\chi^2$ null ($P = 0.529$); trade vs star-clan travel breadth null ($P = 0.343–0.999$); 6 Mohenjo-daro room/house spatial pairings outside `Numeral + Star` clans ($P = 0.164–0.943$).

---

## 6. Additional Cross-File Metadata Catch

- `work_data/key5a/newly_glossed_inscriptions.csv` stores `mahadevan_parsed.csv` row indices rather than `objects_mah_new.csv` `textnum` values (for example, index `1527` maps to a different inscription than `objects_mah_new.csv` textnum `1527`). All landmark inscriptions in `PAPER_DRAFT.md` Table 3 were cross-verified directly against `objects_lipi.csv` and `work_data/key5b/decoded_1776_corpus.csv` (using verified unseen seal `Mahadevan 1559 / M-3160`).

---

## 7. Deliverables Verified on Disk

- `work_scripts/reproduce_all_keys.py`
- `work_data/key6c/master_audit_table.json`
- `work_data/key6c/master_audit_table.csv`
- `work_data/key6c/combined_3wave_meta_stats.json`
- `work_data/key6c/honest_null_registry.csv`
- `PAPER_DRAFT.md`
- `jobs/out/key6c_publication_audit.md`
