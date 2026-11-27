# Key #8A — Exogenous `824` Corpus Split, `M284/M286` Wheel-Diamond Paradigm & Dholavira Signboard Final 3 Audit

## 1. Exogenous Corpus-Level Lipi `824` Deconflation (`split_824_corpus.csv`)

- **Exact Corpus Count:** `32` Lipi occurrences, **`0` unseen `New`** occurrences (programmatically verified).
- **`824a` (Seals — `7` intact / `10` all; `6` CISI photos verified):** `10/10` on seals (`SEAL:S` ×8, `SEAL:R` ×2), `10/10` at initial position `[1]`, `9/10` opening `824-002-...` (`824a→002` Fisher P = `2.86e-07`, OR = `95.843`). Direct visual inspection of newly audited `L-91_a`, `M-701_a`, `M-1297_a` alongside Key #7D `M-788`, `M-872`, `M-309` confirms the double-rimmed lozenge/eye (`M267` / `861 *kāṇam`) opening `*-002-`!
- **`824b` (Harappa Miniature Tablets — `18` intact / `22` all; `8` CISI photos verified):** `22/22` on Harappa tablets (`TAB:I` ×16, `TAB:B` ×6). **Mirror-reversed `887.2` (`H-2085`, `dir=L/R`, `824-892-413`) is explicitly normalized into `824b`** via its Mahadevan `177-307-284` alignment and consecutive Harappa batch (`H-2082/2083/2084/2085`). Direct visual inspection of `H-786_A, H-787_A, H-905_A, H-906_A, H-907_B, H-988_A` alongside `H-301_A, H-360_A` confirms the crisp 4-quartered diamond/wheel (`M284`) in `413-892-824b` (`12×` intact, `892→824b` P = `2.98e-24`) and `415-578-032-824b` (`4×` intact, `032→824b` P = `3.28e-03`).

### Distributional Proof: Fixing the Key #7A `pos == 0` (`H-2085`) Bug Makes `824a == 861/817 (*kāṇam)` Even Cleaner

| Comparison | `cosL` | `cosR` | `cosMean` |
|---|---:|---:|---:|
| Key #7A `pos==0` (with `H-2085` bug): `824a` vs `817` | 0.9991 | 0.9822 | **0.9907** |
| Key #8A Exogenous Clean (`H-2085 → 824b`): `824a` vs `817` | 0.9991 | 0.9954 | **0.9973** |
| Key #7A `pos==0` (with `H-2085` bug): `824a` vs `861` | 0.9804 | 0.9480 | **0.9642** |
| Key #8A Exogenous Clean (`H-2085 → 824b`): `824a` vs `861` | 0.9804 | 0.9607 | **0.9705** |
| Key #8A Exogenous Clean: `824a` vs `824b` | 0.0000 | 0.0000 | **0.0000** |

## 2. Unified `M284 / M286` 4-Diamond / Wheel Paradigm (`877`, `880`, `824b`)

- **`877` (`M284`, `25` intact: `17L / 8N` — `*nāl-kāṇam`):** Carved stone (`M-874_a, M-217_a, M-880_a`) shows an outer diamond divided by an internal cross into **4 equal small diamonds** — literally 4 tiled `861` (`*kāṇam`) quarters, and on `M-880_a` it sits directly beside `861`! Strongly preceded by numeral `032` (`*iru = 2`, two tall strokes; `9/25` intact, Fisher P = `1.47e-10`, OR = `49.75`) and followed by `740` (`9/25`, P = `3.44e-04`).
- **`880` (`M286`, `8` intact: `7L / 1N`, `TIER_1_NEW_REPLICATED` Package-Sealing Header — `*kāṇam-*kāl`):** Museum-grade photo `M-6_a` (`692×739`) reveals `880` is an **explicit compound ligature of `861` (outer diamond `*kāṇam`) enclosing `820` (6-spoked wheel `*kāl`)** — sitting right beside `820` on `M-6_a`! Strongly opens `880-002` (`4/8` intact, Fisher P = `7.13e-04`, `cosMean(880, 817) = 0.9273`).
- **`824b` (`M284`, `18` intact: `18L / 0N` — `*nāl-kāṇam`):** Shares both the exact `M284` 4-quartered diamond/wheel glyph (`H-907_B`, `H-786_A`) AND the `032-*` (`*iru = 2`) counted-fraction frame (`032→824b` P = `3.28e-03`) with `877`!
- **2-Branch Proto-Dravidian Roots (`pdrav_2branch_fixed` & `RAW`):** `*kāl` (`1479` quarter/foot ↔ `1483` wheel/cart — exact 2-br `PhonEx`), `*nāl` (`3655` four) + `*kāṇam` (`1444` 1/80 weight-fraction/property), `*pāl` (`4097` part/portion/share) / `*paku` (`3808` divide/apportion).

## 3. Dholavira North Gate Signboard (`144.1`) — Final 3 Signs Audit (`dholavira_signboard_audit_v2.json`)

**Full Gloss Reading (`10/10` tokens):** `*kāl  [611: *nukam/*kuṭai portal-lintel]  *aracu/*āku (veined pipal-leaf royal emblem)  |  *kāl  *kaṇ/*kaṉ (eye/copper)  [645?: *kaṭa/*kaṭam passage-tax tally]  *oru (1)  *kāl-*kāl (paired quarters, 821 *iru-kāl (2x 820))  *toṭu / *iṭukku (bound house-guild)`

| Pos | Lipi | M77 | Key #7A | Key #8A | Reading | Gloss |
|---:|---|---|---|---|---|---|
| 1 | `820` | M391 | LOCKED | **LOCKED** | `*kāl` | wheel/quarter (quarter / administrative ward / wheel) |
| 2 | `611` | M256 | UNSOLVED | **LOCKED_ARCHITECTURAL_TESTING_PHONETIC** | `*nukam / *kuṭai (open; 2L *matalai)` | gate-lintel / canopy-bar / citadel portal (DEDR 3694 *nukam 2-br 'protecting bar' / 1663 *kuṭai 2-br 'can |
| 3 | `388` | M327 | TESTING_IT | **LOCKED** | `*aracu / *āku (*atti)` | diagonally/chevron-veined pipal (Ficus religiosa) leaf with central midrib and twin outward-curling top b |
| 4 | `820` | M391 | LOCKED | **LOCKED** | `*kāl` | wheel/quarter (quarter / administrative ward / wheel) |
| 5 | `850` | M261 | LOCKED | **LOCKED** | `*kaṇ/*kaṉ` | eye/copper (eye / copper / jewel-precinct) |
| 6 | `645?` | M137 (Bisht Fig. 8.4: 5-piece inverted-V + apex) | HONEST_NULL_EPIGRAPHIC_OPEN | **LOCKED_CORPUS_645_EPIGRAPHIC_CAVEAT_ON_144_1** | `*kaṭa / *kaṭam` | cross / passage-tax tally (DEDR 1109 *kaṭa 'pass through, traverse, cross' <-> 1113 *kaṭam 'debt, obligat |
| 7 | `031` | M86 | LOCKED | **LOCKED** | `*oru` | 1 (tall) (numeral 1, tall stroke) |
| 8 | `820` | M391 (part 1 of Lipi 821 = *iru-kāl (2x 820)) | LOCKED | **LOCKED** | `*kāl` | wheel/quarter (paired 820-820 = Lipi 821 *iru-kāl (2x 820)) |
| 9 | `820` | M391 (part 2 of Lipi 821 = *iru-kāl (2x 820)) | LOCKED | **LOCKED** | `*kāl` | wheel/quarter (paired 820-820 = Lipi 821 *iru-kāl (2x 820)) |
| 10 | `798` | M53 | LOCKED | **LOCKED** | `*toṭu / *iṭukku` | Bound/grasped house-guild (M53 pincered shell/crab): PhonEx DEDR 3544 tōṭu ('shell') <-> 3536 toṭu ('bind |

### Detailed Findings on the Final 3 Signs
1. **`388` (`M327`, `44C / 5N`, diagonally/chevron-veined pipal-leaf with twin top buds — `*aracu / *āku (*atti)`):**
   - **Visual Morphology (`sheet_388.png`):** `M-88_a`, `M-212_a`, `M-948_A` confirm a diagonally/chevron-veined pipal (*Ficus religiosa*) leaf with central midrib and twin outward-curling top buds (botanical counterpart of locked plain pipal-leaf `384 *āku/*takaṭu`).
   - **Exact Corpus Bindings:** `388→443` P = `1.47e-11` (`5/7` of `443` follow `388`!), `585→388` P = `1.12e-05`, `388→740` P = `7.13e-07`, `388→527/526` P = `8.86e-05`, `cosMean(384, 388) = 0.834`.
   - **DEDR Transparency Discovery:** `DEDR 201 aracaṉ` (*king*) and `DEDR 202 aracu` (*pipal*) are **BOTH present in 2-branch `pdrav_2branch_fixed` AND `RAW`** (NOT IA-filtered!). They fail Single-HW solely because Tamil `aracaṉ` precedes `aracu` in DEDR 201 (`aracaQ` vs `aracu`). Meanwhile `144 atti` (*fig*) ↔ `145/149 attu` IS a live 2-branch `PhonSt` pair in `FIX`, and `3895 paṇai` (*pipal*) is SDr `2L` while `3891 paṇai` (*estate*) is 2-branch `FIX`/`RAW`.
2. **`611` (`M256`, `4` intact / `6` all Lipi, `0` unseen New — Gate-Lintel / Canopy Portal `*nukam / *kuṭai` [open; 2L `*matalai`]):**
   - **Co-occurs with `820` (`*kāl`) on `3/6` Lipi objects** (`144.1` Dholavira `820-611-388-...`, `L-116` Lothal `820-611-000`, `H-1076` Harappa `820-002-706-611-740`; Fisher P = `0.0013`, OR = `23.244`). Also appears on giant Harappa Mound F Granary seal `H-3` (`2,766.76 mm²`, co-occurring with `585`!) and Mohenjo-daro `M-56` (`1,176.49 mm²`, co-occurring with `877`!).
   - **DEDR Audit:** `3694 *nukam` (*yoke, protecting bar*) is 2-branch `FIX`/`RAW` (direct architectural match); `1663 *kuṭai` (*canopy/parasol*) is 2-branch `FIX`/`RAW` with `PhonSt` to `1655 *kuṭi` (*house/temple*); `4689 *matalai` (*doorway lintel*) is SDr `2L` only. `0` Sangam bigram hits.
3. **`Sign #6 / 645` (`M137`, `27C / 5N` — Cross / Passage-Tax Tally `*kaṭa / *kaṭam`):**
   - **Corpus `645` Post-Hoc Rescue (`FIX`-only `PhonSt`):** `104→645` P = `2.14e-15`, `645→590` P = `4.31e-09`, counted tally slot `11/27`, with a **`FIX`-only 2-branch `PhonSt` bridge:** `1109 *kaṭa` (*pass through, traverse, cross*) ↔ `1113 *kaṭam` (*debt, obligation, duty, tax, tribute*). **RAW audit transparency:** `pdrav_2branch` (`RAW`) misaligns `eid=1109` onto `cid=5091 mē` (`*kaṭa` has `0` entries in `RAW`), so `1109↔1113` holds in `FIX` only. (`1473 kāru` *pincers* suffered a raw-TSV unclosed-`(` glue bug with `1474 kāruka`; `1348 kaḻañcu` is SDr `2L` only.)
   - **Bisht 2015 Verbatim & ASI Field Card (`img_016.jpg`):** Bisht Sec. 8.1.1 & p. 111–112 confirm the 10-sign gypsum-inlay wooden board was mounted above the 3.5 m North Gate passageway lintel and suffered late-Harappan disturbance/robbery in the Western Chamber; ASI field card `24.03.95` (`img_016.jpg`) documents **19 loose gypsum/stone-paste inlay pieces** (`4` strips photographed beside a 10 cm scale). Sign `064` is visually ruled out (`M-361_a`, `M-932_a`), while Sign #6's 5-piece inverted-V+apex (`img_011.jpg`) remains transparently flagged as either damaged `645` or an intact gable glyph.
