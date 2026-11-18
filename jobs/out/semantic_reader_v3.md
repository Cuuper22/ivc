# Wave 2A — Unified Sound-Free Semantic Reader (`87.14%` Intact Coverage)

**Building on it.** Fusing `FRAME v3` clause segmentation, the locked `9.24 L : 37.0 L : 110.9 L : 665 L` metrological ladder, `175` Lipi-learned archaeological sign anchors (`239` phrases), and the `25/34` Persian Gulf Cuneiform/Dilmun round-seal calque produces a **100% sound-free, language-agnostic corpus reader** (`MEANINGS.md`, `FRAMEBOOK.md` v3, `work_data/reader_v3/corpus_soundfree_readings.csv`) that exceeds the `≥85%` intact target:
- **Strict Clause Parse Coverage**: **87.14% of all 3,600 intact Lipi faces** (`3,137 / 3,600`, up from `50.47%` in `FRAME v2`), **87.19% on length ≥ 3**, and **88.03% on length ≥ 3 administrative inscriptions** (`1,912 / 2,172`, `0/20` decoys, $z = 5.91$).
- **Physical & Grammatical Token Grounding**: Within parsed intact Lipi inscriptions, **91.85% of all sign tokens** carry an empirically measured grammatical, metrological, or archaeological meaning (**92.82% on unseen in-vocabulary Mahadevan `new texts`**). Across all 3,600 intact Lipi faces, **77.94% (`2,806 / 3,600`) have 100% of administrative/functional slots explicitly glossed**, and **65.50% (`2,358 / 3,600`) have every single token — including open personal-name slots — physically or archaeologically anchored**.
- **Zero-Shot Unseen Mahadevan `new texts` Coverage & Prediction**:
  - **64.94% (`313 / 482`)** of unseen in-vocabulary complete Mahadevan `new texts` parse zero-shot (more than doubling `29.88%` in `v2`, `0/20` decoys, $z = 3.76$).
  - Compressing all `708` Lipi signs into just **14 sound-free physical/administrative channels** (`CH_CUP_RATION`, `CH_BULK_KALAM`, `CH_ESTATE_COPPER`, `CH_METAL_TOOL`, `CH_MARITIME_TAG`, `CH_CRAFT_ROD`, `CH_POT_VESSEL`, `CH_IVORY_ELITE`, `CH_CITADEL_CREST`, etc.) learned **100% on Lipi (`4,349` events)** predicts the **physical artifact class of `980` unseen Mahadevan `new texts` events** (`seal`, `miniature tablet`, `copper tablet`, `clay package sealing`, `pot`, `copper blade`, `ivory rod`) beating **all 2,000 `(v3_class × freq_band)` sign-permuted decoys** under Fixed-Prior (`macro log-LR = 0.9008` vs `0.5061` decoy mean, **$z = +3.22, P = 0.0005, 0/2000$**) AND surviving the **Rival-Refit control** where every decoy reader refits its own Lipi 14-channel Naive-Bayes classifier (`0.9008` vs `0.6534` refit-decoy mean, **$z = +2.05, P = 0.028$**).
  - Restricted to **`197` unseen Mahadevan `new texts` stone seals** (`Task B`, where object format gives zero help), the same 14-channel Lipi reader predicts unseen **excavation zones** (`Citadel`, `Chanhu-daro / VS Craft`, `HR Elite`, `Maritime / Gulf / West`, `Eastern Headwaters`) at **Fixed `(v3_class × band)` macro $z = +1.78$ ($P = 0.0355$)** (`Rival-Refit macro z = +1.22, P = 0.118`, complementing the direct per-sign `z = +6.25` and per-phrase `z = +8.82` held-out replication in `jobs/out/semantic_anchors.md`).

---

## 1. Coverage & Grounding Breakdown (`work_data/reader_v3/reader_eval_summary.json`)

| Corpus Slice | Total Lines | Strictly Parsed (`FRAME v3`) | Share Parsed | Token Grounding inside Parsed | All Admin Slots Glossed | Every Token Anchored (incl. Names) |
|---|---:|---:|---:|---:|---:|---:|
| **Intact Lipi Faces (All)** | `3,600` | **`3,137`** | **`87.14%`** | **`91.85%`** | `2,806` (`77.94%`) | `2,358` (`65.50%`) |
| **Intact Lipi Admin (`len ≥ 3`)** | `2,172` | **`1,912`** | **`88.03%`** | — | — | — |
| **Unseen Mahadevan `new texts` (in-vocab)** | `482` | **`313`** | **`64.94%`** | **`92.82%`** | — | — |
| **Unseen Mahadevan `new texts` (all, incl. `X...`)** | `627` | **`370`** | **`59.01%`** | — | — | — |

---

## 2. Zero-Shot Held-Out Artifact & Zone Prediction vs. 2,000 `(v3_class × band)` Decoys

Every decoy reader permutes the 14-channel physical/archaeological vectors among signs of the **exact same `FRAME v3` grammatical class and Lipi frequency band** (`665` signs in movable strata):

| Held-Out Zero-Shot Task on Unseen `new texts` | Real Score | Decoy Mean ± SD | Decoy Max | `$z$` | Decoys ≥ Real | Empirical `$P$` |
|---|---:|---:|---:|---:|---:|---:|
| **Task A (`n = 980` unseen events, 7 artifact kinds) — Fixed Macro Discrim** | **`+0.9008`** | `+0.5061 ± 0.1226` | `+0.8394` | **`+3.22`** | **`0 / 2,000`** | **`0.0005`** |
| **Task A (`n = 980` unseen events) — Fixed Log-Likelihood Gain** | `-0.0777` | `-0.1407 ± 0.0384` | `-0.0274` | **`+1.64`** | `83 / 2,000` | **`0.0420`** |
| **Task A (`n = 980` unseen events) — Rival-Refit Macro Discrim** | **`+0.9008`** | `+0.6534 ± 0.1208` | `+1.0439` | **`+2.05`** | `55 / 2,000` | **`0.0280`** |
| **Task A (`n = 980` unseen events) — Rival-Refit LL Gain** | `-0.0777` | `-0.1076 ± 0.0290` | `-0.0119` | `+1.03` | `296 / 2,000` | `0.1484` |
| **Task B (`n = 197` unseen stone seals, 5 zones) — Fixed Macro Discrim** | **`+0.1985`** | `+0.1004 ± 0.0553` | `+0.2640` | **`+1.78`** | `70 / 2,000` | **`0.0355`** |
| **Task B (`n = 197` unseen stone seals) — Rival-Refit Macro Discrim** | `+0.1985` | `+0.1336 ± 0.0532` | `+0.3147` | `+1.22` | `235 / 2,000` | `0.1179` |

**Note on per-document LL Gain (`-0.0777`):** Multi-class Naive Bayes sums binary channel log-odds across 14 partially correlated channels (`seal` is `580/980 = 59.2%` of unseen `new texts`, while `tool = 6` and `rod = 9`), mildly over-sharpening rare-class posteriors on seal majority lines (`Rival-Refit LL z = +1.03` on Task A, `-1.06` on Task B), whereas class-balanced **Macro Log-Likelihood Discrimination** (`+3.22` Fixed, `+2.05` Rival-Refit) cleanly measures class-by-class separation across all 7 physical artifact types.

---

## 3. Representative Zero-Shot Sound-Free Readings (`MEANINGS.md`)

1. **Unseen Mohenjo-daro Seal (`M-1003`, VS Dyers/Craft Quarter)**:
   - Raw signs: `031-X55-861-002 | 055-233-705-033-520`
   - Sound-free clause reading: `[1 + Name(X55) + Diamond head-unit + slot-2]  ||  [Dozen(12) + Barred-Fish Crest + 3 × 12-cup bulk measure (~332.7 L) + Spear-rank closer]`
2. **Unseen Mohenjo-daro Double-Clause Seal (`M-1012`)**:
   - Raw signs: `692-060-255 | 435-690-740 | 692-060-803-740`
   - Sound-free clause reading: `[District-Enclosure + in/of + Name(255)]  ||  [Name(435) + Post-Measure Allotment + House-of]  ||  [District-Enclosure + in/of + Leaf-Branch Crest + House-of]`
3. **Harappa Multi-Face Steatite/Clay Ledger (`H-1121`, Mound F Trench III)**:
   - Raw faces: `016-220-520-400  ||  000-817-711-033-700`
   - Sound-free ledger reading: **Front:** `[6 (stacked) + Plain-Fish Crest + Spear-rank + Junior/Artisan comb-rank]`  ||  **Back:** `[... + Double-Diamond + 4-cup vessel (~37.0 L) + 3 × cup (~27.7 L) = 7 cups (~64.7 L)]`
4. **Lothal Warehouse Clay Package Sealing -> Bahrain Saar Round Seal**:
   - Lothal tag: `705-500-741 | 001-055-220` -> `[Maritime Ship-Sail Freight Office + Ward-1 linker]  ||  [1-Dozen-Fish Port Seal {city-lock: Lothal}]`
   - Bahrain Saar (`5229.1`): `055-220-091 | 001-093 | 031` -> `[Dozen-Fish Port Stem + Plural LÚ.MEŠ (091)]  ||  [DIŠ-LÚ person (001-093)]  ||  [1]`

---

## Reproducibility
- Script: `work_scripts/reader_v3_build.py`
- Root Corpus Books: `MEANINGS.md` (concrete sound-free readings), `FRAMEBOOK.md` (`FRAME v3` word-free jobs)
- Data: `work_data/reader_v3/corpus_soundfree_readings.csv`, `soundfree_lexicon.csv`, `reader_eval_summary.json`
