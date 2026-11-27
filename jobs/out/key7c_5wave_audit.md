# Key #7C-1 — 5-Wave 95-Sign Strictly Disjoint Meta-Analysis & Master Verification Audit (v2)

Generated directly from `work_scripts/reproduce_all_keys.py` (v2; exit code `0`, runtime `146.5s`, zero invented or hardcoded headline numbers).

## 1. Script & On-Disk Artifact Integrity (`Key #1` through `Key #7D`)

- **Scripts checked (`py_compile`):** **24/24 PASS** (`gulf3_audit_and_ventris.py`, `gulf3_key1_decipher.py`, `gulf3_redesign_lock.py`, `key2a_rebus_lock.py`, `key2a_rival_audit.py`, `key2b_ur_failaka.py`, `key2c_elamite_bridge.py`, `key3a_sound_sweep.py`, `key3b_gulf_ur3_audit.py`, `key4_master_merge.py`, `key4a_ligatures.py`, `key4b_bootstrap_wave2.py`, `key4c_sangam_epigraphy.py`, `key4d_allographs.py`, `key4e_museum_archives.py`, `key5a_big_six_strike.py`, `key5b_reader_and_network.py`, `key6a_wave4_strike.py`, `key6b_readings_key5_atlas.py`, `key7a_wave5_90pct.py`, `key7b_external_and_multiface.py`, `key7c_readings_key6_explorer.py`, `key7d_find_photos.py`, `reproduce_all_keys.py`).
- **Headline claims audited (`master_audit_table_v2.{json,csv}`):** **52/52** extracted programmatically from disk JSON/CSV artifacts (`all_artifacts_verified_on_disk = True`).
- **Honest nulls registered (`honest_null_registry_v2.csv`):** **41** documented negative/non-significant results & negative controls compiled directly from disk across Key #1 through Key #7B.
- **Unseen holdout parity:** **18/18** cleanly crosswalked tiers (`Key #4 Master` through `Key #7A`, `563` unseen intact faces) pass **both** `Unseen Token % >= Lipi Token %` and `Unseen 100%-Decoded Face % >= Lipi 100%-Decoded Face %`.

---

## 2. Invariant 1 — Exact 5-Wave Disjointness Audit (All Overlaps Caught & Stripped)

Programmatic set-intersection across all five published phonetic waves (`work_data/key2a/test_a2_matched_words.csv`, `work_data/key4b/test4b1_top30_sign_table.csv`, `work_data/key5a/trackA_per_sign_bridges.csv`, `work_data/key6a/trackA_per_sign_bridges.csv`, `work_data/key7a/trackA_wave5_per_sign_bridges.csv`) spans **106 raw sign-tests** (`12 + 30 + 13 + 24 + 27`) across **95 unique signs**.

### Exact Pairwise Intersections (All 10 Wave Pairs Audited)
- **W1 $\cap$ W2:** **1 sign (`861`)** — tested in Key #2A UltraClean-12 (outside Key #2A's 11-sign lock) and re-entered Key #4B Top-30.
- **W2 $\cap$ W3:** **5 signs (`060, 142, 240, 550, 798`)** — Big-Six bottlenecks that failed Wave-2 Key #4B (`0/5` `PhonEx`) and were re-tested with redesigned domains in Wave-3 Key #5A.
- **W2 $\cap$ W4:** **1 sign (`142`)** — #1 high-frequency holdout tested in Key #3A, Wave-2, Wave-3, and rescued in Wave-4 Key #6A.
- **W3 $\cap$ W4:** **5 signs (`142, 527, 585, 595, 692`)** — the five unresolved Key #5A holdouts re-entered into Key #6A Wave-4 Track-A (`527, 585, 595, 692` were inside Wave-3 Disjoint-8; `142` was stripped from both W2 Disjoint and W3 Disjoint).
- **ALL OTHER 6 PAIRS (`W1∩W3`, `W1∩W4`, `W1∩W5`, `W2∩W5`, `W3∩W5`, `W4∩W5`):** **0 signs (`∅`)** — confirming **Wave-5 (`27` signs) has strictly 0.00% overlap with `W1 ∪ W2 ∪ W3 ∪ W4`**, and **0.00% overlap with Key #3A's 20-sign bootstrap** (likewise `W4_disjoint19 ∩ Key3A = ∅`).

### Programmatic Overlap Stripping & Zero-Overlap Assertions
Every overlapping sign is stripped programmatically (`assert len(S_i & S_j) == 0` for all 10 pairs) and evaluated via LIVE 5,000-shuffle 7-family `Single-Headword` cluster-preserving permutation runs:
1. **Primary Strictly Pairwise-Disjoint 5-Wave Set (`90` unique signs, zero overlap, excludes all prior-tested W1/W2/W3 signs from W4):**
   - `W1` (`12`): `090, 154, 220, 320, 390, 400, 520, 705, 740, 820, 850, 861`
   - `W2_disjoint24` (`24`): `W2 \ (W1 ∪ W3)`
   - `W3_disjoint8` (`8`): `440, 692, 435, 585, 595, 845, 527, 416`
   - `W4_disjoint19` (`19`): `W4 \ (W1 ∪ W2 ∪ W3)` = `388, 384, 350, 455, 460, 482, 070, 480, 335, 540, 645, 621, 630, 877, 171, 297, 831, 165, 104`
   - `W5_disjoint27` (`27`): all 27 Key #7A Fresh Wave-5 signs (`510, 890, 679, 382, 167, 190, 137, 636, 321, 315, 565, 605, 921, 065, 468, 484, 906, 130, 374, 371, 773, 267, 853, 391, 422, 347, 336`)
   - *Excluded from all 5 disjoint sets (5 signs):* `{060, 142, 240, 550, 798}` (the 5 `W2 ∩ W3` bottlenecks).
2. **Sensitivity Check 1 — Keep-`142` 5-Wave Disjoint (`91` unique signs, zero overlap across all 5 waves):** Keeps `142` in Wave-4 (`W4_keep142 = 20`) since `142` was excluded from both `W2_disjoint24` and `W3_disjoint8`.
3. **Sensitivity Check 2 — Ultra-Disjoint 5-Wave (`89` unique signs):** Additionally excludes Key #3A-overlapping sign `416` from Wave-3 (`W3_ultradisjoint7 = 7`) while excluding all prior-tested signs (including `142`) from Wave-4 (`19`).

---

## 3. Invariant 2 — Combined 5-Wave (`χ²_10`) & 4-Wave (`χ²_8`) 7-Family Meta-Analysis

### Table A: Primary 5-Wave Strictly Pairwise-Disjoint (`12 + 24 + 8 + 19 + 27 = 90` Unique Signs, `df = 10`, Live 5,000 Shuffles)

| Language Family (Single-HW) | W1 (`12`) | W2 Disj (`24`) | W3 Disj (`8`) | W4 Disj (`19`) | W5 Disj (`27`) | Fisher $\chi^2_{10}$ | Fisher $P$ | Bonf-7 $P$ | Stouffer $Z_{\text{emp}}$ | Stouffer $Z_P$ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Mode A: `PhonSt` (Phonemic Stem Match, 90 strictly disjoint signs)** | | | | | | | | | | |
| **Proto-Dravidian (2-br Fixed)** | **9/12** (`0.0004`) | **23/24** (`0.0002`) | **5/8** (`0.0010`) | **14/19** (`0.0002`) | **14/27** (`0.1090`) | **67.97** | **$1.09 \times 10^{-10}$** | **$7.66 \times 10^{-10}$** | **+8.17** | **+6.60** |
| *Dravidian RawPDrav (audit)* | *9/12* (`0.0006`) | *22/24* (`0.0002`) | *5/8* (`0.0008`) | *12/19* (`0.0008`) | *14/27* (`0.0402`) | *66.82* | *$1.81 \times 10^{-10}$* | *$1.27 \times 10^{-9}$* | *+8.69* | *+6.64* |
| Indo-Aryan (OIA) | 1/12 (`0.1694`) | 2/24 (`0.1382`) | 0/8 (`1.0000`) | 2/19 (`0.0076`) | 0/27 (`1.0000`) | 17.27 | 0.0686 | **0.4803** | +3.58 | −1.33 |
| Sumerian | 3/12 (`0.1680`) | 5/24 (`0.3651`) | 0/8 (`1.0000`) | 0/19 (`1.0000`) | 5/27 (`0.4239`) | 7.30 | 0.6969 | **1.0000** | +0.26 | −2.66 |
| Munda | 0/12 (`1.0000`) | 0/24 (`1.0000`) | 0/8 (`1.0000`) | 0/19 (`1.0000`) | 0/27 (`1.0000`) | 0.00 | 1.0000 | **1.0000** | −0.42 | −8.32 |
| Elamite | 0/12 (`1.0000`) | 0/24 (`1.0000`) | 0/8 (`1.0000`) | 0/19 (`1.0000`) | 0/27 (`1.0000`) | 0.00 | 1.0000 | **1.0000** | −0.18 | −8.32 |
| Akkadian | 0/12 (`1.0000`) | 0/24 (`1.0000`) | 0/8 (`1.0000`) | 0/19 (`1.0000`) | 0/27 (`1.0000`) | 0.00 | 1.0000 | **1.0000** | −0.21 | −8.32 |
| Burushaski | 0/12 (`1.0000`) | 0/24 (`1.0000`) | 0/8 (`1.0000`) | 0/19 (`1.0000`) | 0/27 (`1.0000`) | 0.00 | 1.0000 | **1.0000** | −0.29 | −8.32 |
| **Mode B: `PhonEx` (Exact Phonemic Homophony, 90 strictly disjoint signs)** | | | | | | | | | | |
| **Proto-Dravidian (2-br Fixed)** | **6/12** (`0.0038`) | **14/24** (`0.0024`) | **4/8** (`0.0002`) | **7/19** (`0.0112`) | **10/27** (`0.0324`) | **56.09** | **$1.98 \times 10^{-8}$** | **$1.38 \times 10^{-7}$** | **+7.71** | **+5.89** |
| *Dravidian RawPDrav (audit)* | *6/12* (`0.0016`) | *12/24* (`0.0038`) | *4/8* (`0.0004`) | *6/19* (`0.0194`) | *10/27* (`0.0092`) | *56.93* | *$1.37 \times 10^{-8}$* | *$9.61 \times 10^{-8}$* | *+8.28* | *+5.99* |
| Indo-Aryan (OIA) | 0/12 (`1.0000`) | 2/24 (`0.0574`) | 0/8 (`1.0000`) | 1/19 (`0.0692`) | 0/27 (`1.0000`) | 11.06 | 0.3531 | **1.0000** | +2.41 | −3.62 |
| Sumerian | 1/12 (`0.5693`) | 1/24 (`0.8630`) | 0/8 (`1.0000`) | 0/19 (`1.0000`) | 1/27 (`0.9002`) | 1.63 | 0.9985 | **1.0000** | −1.10 | −4.47 |
| Munda | 0/12 (`1.0000`) | 0/24 (`1.0000`) | 0/8 (`1.0000`) | 0/19 (`1.0000`) | 0/27 (`1.0000`) | 0.00 | 1.0000 | **1.0000** | −0.24 | −8.32 |
| Elamite | 0/12 (`1.0000`) | 0/24 (`1.0000`) | 0/8 (`1.0000`) | 0/19 (`1.0000`) | 0/27 (`1.0000`) | 0.00 | 1.0000 | **1.0000** | −0.12 | −8.32 |
| Akkadian | 0/12 (`1.0000`) | 0/24 (`1.0000`) | 0/8 (`1.0000`) | 0/19 (`1.0000`) | 0/27 (`1.0000`) | 0.00 | 1.0000 | **1.0000** | −0.15 | −8.32 |
| Burushaski | 0/12 (`1.0000`) | 0/24 (`1.0000`) | 0/8 (`1.0000`) | 0/19 (`1.0000`) | 0/27 (`1.0000`) | 0.00 | 1.0000 | **1.0000** | −0.18 | −8.32 |

### Table B: Sensitivity Regimes Across 3-Wave (`df=6`), 4-Wave (`df=8`), and 5-Wave (`df=10`)

| Regime | Mode | Drav $\chi^2_{\text{df}}$ | Drav Fisher $P$ | Drav Bonf-7 $P$ | Drav $Z_{\text{emp}}$ | RawPDrav $P$ | Best Rival Bonf-7 $P$ |
|---|---|---:|---:|---:|---:|---:|---:|
| **5-Wave Strictly Disjoint (`12+24+8+19+27 = 90`)** | **`PhonSt`** | **67.97** (`df=10`) | **$1.09 \times 10^{-10}$** | **$7.66 \times 10^{-10}$** | **+8.17** | $1.81 \times 10^{-10}$ | 0.4803 (OIA) |
| **5-Wave Strictly Disjoint (`12+24+8+19+27 = 90`)** | **`PhonEx`** | **56.09** (`df=10`) | **$1.98 \times 10^{-8}$** | **$1.38 \times 10^{-7}$** | **+7.71** | **$1.37 \times 10^{-8}$** | **1.0000** (OIA) |
| **5-Wave Keep-`142` Disjoint (`12+24+8+20+27 = 91`)** | `PhonSt` | 67.97 (`df=10`) | $1.09 \times 10^{-10}$ | $7.66 \times 10^{-10}$ | +8.25 | $5.31 \times 10^{-11}$ | 0.5243 (OIA) |
| **5-Wave Keep-`142` Disjoint (`12+24+8+20+27 = 91`)** | `PhonEx` | 58.05 (`df=10`) | $8.46 \times 10^{-9}$ | $5.92 \times 10^{-8}$ | +7.91 | $5.67 \times 10^{-9}$ | 1.0000 (OIA) |
| **5-Wave Ultra-Disjoint (`12+24+7+19+27 = 89`, excl. `416`)** | `PhonSt` | 64.75 (`df=10`) | $4.53 \times 10^{-10}$ | $3.17 \times 10^{-9}$ | +7.84 | $4.78 \times 10^{-10}$ | 0.4803 (OIA) |
| **5-Wave Ultra-Disjoint (`12+24+7+19+27 = 89`, excl. `416`)** | `PhonEx` | 49.65 (`df=10`) | $3.10 \times 10^{-7}$ | $2.17 \times 10^{-6}$ | +7.07 | $9.08 \times 10^{-8}$ | 1.0000 (OIA) |
| Full Published Waves (`12+30+13+24+27`, `95` unique) | `PhonSt` | 66.47 (`df=10`) | $2.12 \times 10^{-10}$ | $1.48 \times 10^{-9}$ | +8.01 | $1.62 \times 10^{-11}$ | 0.6207 (OIA) |
| Full Published Waves (`12+30+13+24+27`, `95` unique) | `PhonEx` | 57.22 (`df=10`) | $1.21 \times 10^{-8}$ | $8.49 \times 10^{-8}$ | +7.81 | $1.98 \times 10^{-9}$ | 1.0000 (OIA) |
| **4-Wave Strictly Disjoint (`12+24+8+19 = 63`)** | `PhonSt` | 63.53 (`df=8`) | $9.41 \times 10^{-11}$ | $6.59 \times 10^{-10}$ | +8.41 | $3.90 \times 10^{-10}$ | 0.1920 (OIA) |
| **4-Wave Strictly Disjoint (`12+24+8+19 = 63`)** | `PhonEx` | 49.23 (`df=8`) | $5.75 \times 10^{-8}$ | $4.02 \times 10^{-7}$ | +7.55 | $1.20 \times 10^{-7}$ | 1.0000 (OIA) |
| 4-Wave Keep-`142` Disjoint (`12+24+8+20 = 64`) | `PhonSt` | 63.53 (`df=8`) | $9.41 \times 10^{-11}$ | $6.59 \times 10^{-10}$ | +8.50 | $1.11 \times 10^{-10}$ | 0.2125 (OIA) |
| 4-Wave Keep-`142` Disjoint (`12+24+8+20 = 64`) | `PhonEx` | 51.19 (`df=8`) | $2.41 \times 10^{-8}$ | $1.69 \times 10^{-7}$ | +7.77 | $4.89 \times 10^{-8}$ | 1.0000 (OIA) |
| 3-Wave Strictly Disjoint (`12+24+8 = 44`, Key #6C baseline) | `PhonSt` | 46.50 (`df=6`) | $2.36 \times 10^{-8}$ | $1.65 \times 10^{-7}$ | +7.31 | $2.78 \times 10^{-8}$ | 1.0000 (OIA) |
| 3-Wave Strictly Disjoint (`12+24+8 = 44`, Key #6C baseline) | `PhonEx` | 40.24 (`df=6`) | $4.08 \times 10^{-7}$ | $2.85 \times 10^{-6}$ | +7.09 | $5.29 \times 10^{-7}$ | 1.0000 (OIA) |

**Key takeaway:** Stripping ALL overlaps across all 5 waves leaves Proto-Dravidian's combined signal **stronger than or virtually identical to** the raw published waves (`PhonSt` $P = 1.09 \times 10^{-10}$ vs $2.12 \times 10^{-10}$; `PhonEx` $P = 1.98 \times 10^{-8}$, `RawPDrav` $P = 1.37 \times 10^{-8}$), with **all six rival language families remaining non-significant** after 7-family Bonferroni correction (`OIA Bonf-7 P = 0.4803` on `PhonSt` and `1.0000` on `PhonEx`; all 5 other rivals `Bonf-7 P = 1.0000` on both modes).

---

## 4. Invariant 3 — Unseen Holdout Parity (`Key #4 Master` through `Key #7A`)

Across all **18/18** cleanly crosswalked tiers (`563` unseen intact faces vs `3,600` Lipi intact faces):
- **Key #6A Locked (`163` signs):** Lipi `85.56%` vs Unseen **`88.31%`** (`+2.75 pp`); combined intact **`85.92%`** (`2,546/4,163 = 61.16%` 100%-decoded; unseen `380/563 = 67.50%`).
- **Key #7A Phon/Met/4D-Only (`224` signs, excl. `692`/`070`):** Lipi `89.19%` vs Unseen **`93.18%`** (`+3.99 pp`); combined intact **`89.71%`**.
- **Key #7A Locked (`227` signs):** Lipi `89.89%` vs Unseen **`93.98%`** (`+4.09 pp`); combined intact **`90.42%`** (`2,985/4,163 = 71.70%` 100%-decoded; unseen **`468/563 = 83.13%`**!).
- **Key #7A + `testing it` Frontier (`239` signs):** Lipi `91.63%` vs Unseen **`95.34%`** (`+3.71 pp`); unseen 100%-decoded **`85.79%`**.

---

## 5. Invariant 4 — Expanded Honest Null Registry v2 (`41` Documented Nulls)

`work_data/key7c/honest_null_registry_v2.csv` preserves all **30** Key #1–#5B nulls and adds **11** new Key #6A–#7B nulls/negative controls extracted directly from disk:
- **Key #6A (2 entries):** 4 strict visual-only DEDR nulls (`070, 455, 645, 692`) + 13 withheld holds & 0 remaining catalog doubles; 4 failed Track-B allograph swap controls (`061/063`, `861/824`, `550/554`, `384/388`).
- **Key #6B (2 entries):** Seals-only 9×7 city $\chi^2$ null (`n = 1,749`, $\chi^2 = 35.77, P = 0.6585$); 13/13 individual Key #5A roles length+site seal-area nulls ($P \ge 0.116$, showing `255-435`'s `990 mm²` raw median is explained by its 8-sign length).
- **Key #7A (2 entries):** Wave-5 `pdrav_2branch_fixed` `PhonSt` (`14/27`, $P = 0.115$ disk / $0.109$ live, while `RawPDrav` passes at $P = 0.0424$ / $0.0402$ and `PhonEx` passes on both) & separate Photo-Verified Rescue-11 aggregate null (`Dravidian PhonEx 2/11, P = 0.668`); 9 strict nulls (`130, 190, 267, 315, 371, 374, 565, 645, 853`), 12 withheld holds (incl. single-formula `501, 321, 318`), `824_fin` 4-wheel null vs `817` (`P = 0.941`), and `384 -> 388` botanical negative control (`cL-cR = +0.050`).
- **Key #7B (5 entries):** Waves 2–4 `>=1 outside K4C-35` within-lexicon permutation word count (`P = 0.1054`), Prakrit 30-loan negative control (`0/30`), & Ur III Sumerian word count (`P = 0.9240`); 5/23 Wave-4 blind object/site nulls + 15/18 Wave-4 seal-area nulls (plus `350`/`495` significantly smaller); Multi-face Commodity $\to$ Unit/Cups (`P = 0.1586 / 0.2843`); Multi-face Rank $\to$ Cup Ration (`H = 3.38, P = 0.4877`, flat ~3-cup standard allowance); Multi-face Cross-Face Numeral Equality (`P = 0.0548` dedup / `0.4197` raw) & `n1 × n2 == 12` (`P = 0.9972` dedup / `0.1554` raw).

---

## 6. Deliverables Verified on Disk

- `work_scripts/reproduce_all_keys.py` (v2, exit 0)
- `work_data/key7c/combined_5wave_meta_stats.json`
- `work_data/key7c/master_audit_table_v2.json`
- `work_data/key7c/master_audit_table_v2.csv`
- `work_data/key7c/honest_null_registry_v2.csv`
- `jobs/out/key7c_5wave_audit.md`
- `PAPER_DRAFT.md` (upgraded to full Key #1–#7D coverage)
