# Key #4A (Lever 1): Diacritic, Modifier & Graphic Ligature Cracker

**Headline Win.** Unlocking graphic diacritics, Mahadevan-merged allographs, and zero-artifact Proto-Dravidian ligatures anchored to our 19 sound-locked signs adds **`36` newly `building on it` signs (`+1,585` intact tokens, `+10.31 pp`)**, driving total `building on it` token coverage across all `4,227` intact accessible faces (`15,370` tokens) from **`45.07%` → `55.38%`** and jumping 100%-glossed intact faces by **`+57.4%` (`441` → `694`, including `106` newly 100%-glossed multi-sign faces of length ≥ 3)**. On the **`627` unseen unpartnered Mahadevan intact faces** (`2,161` tokens), coverage jumps with zero shrinkage from **`42.30%` → `52.01%` (`+9.71 pp`)** and 100%-glossed faces jump **`+41.3%` (`80` → `113`)**.

Three independent 5,000-shuffle statistical locks power this jump:
1. **Three Cross-Base Grammatical Diacritic Operators Locked (`5,000` base-controlled shuffles):**
   - **`cage_4corners` (4 corner strokes, `k = 8` bases)** is a **suffixal finalizer**: `8/8 (100%)` bases jump into clause-final / pre-`400` position (**`ΔF400 = +0.7453`**, null `+0.2017 ± 0.1128`, **`z = +4.820, P = 0.0002`** — ceiling of 5,000 shuffles; `ΔFin = +0.4132`, **`P = 0.0036`**; `ΔPos = +0.2520`, **`P = 0.0056`**).
   - **`side_brackets` (enclosing parentheses/bars, `k = 6` bases)** is its exact **prefixal mirror**: it preserves RIGHT neighbors (`cosR = 0.6078`, null `0.3100`, **`z = +2.403, P = 0.0112`**) while replacing LEFT neighbors (`cosL = 0.1727`, **`asym cL − cR = −0.4351`**, null `−0.0332`, **`z = −2.662, P = 0.0054`**).
   - **`multi_stroke_inside` (`1–4` internal vertical strokes inside vessels/fish/man, `k = 10` bases)** is a **construct-state / seal-header medializer**: `10/10 (100%)` drop clause-final `F400` (`ΔF400 = −0.5521`), `10/10 (100%)` increase seal share (**`ΔSeal = +0.3641`**, null `+0.1752`, **`z = +1.938, P = 0.0488`**), `8/10` jump into pre-numeral position (**`ΔBefN = +0.1821`**, null `+0.0493`, **`z = +2.013, P = 0.0354`**), and left syntax stays anchored (**`cosL = 0.3489`**, null `0.2440`, **`z = +2.062, P = 0.0114`**).
2. **`11` Distributionally Locked Allographs of Our Core Sound-Locked Signs (`5,000` random-partner shuffles):** `705 *kalam` ↔ `706/704` (`M336`, `17` exact swaps, `P = 0.0024`), `154 *kā` ↔ `156/158/155/153` (`M15`, `P = 0.0024–0.0092`) + `151` plain porter base (`M12`, `cosR = 0.984, P = 0.0250`), and `390 *tai` ↔ `392/405/406/407` (`13` swaps `390↔405` `P = 0.0050`, `10` swaps `390↔407` `P = 0.0162`). Plus three high-frequency unsolved allograph pairs locked (`861 ≡ 817` `M267`, `419` tokens, `P = 0.0034`; `760 ≡ 752`, `151` tokens, `P = 0.0246`; `803 ≡ 806`, `234` tokens, `16` swaps, `P = 0.0088`) ready for Key #4B/4C.
3. **Zero-Artifact Proto-Dravidian DEDR Ligature & Modifier Lock (`19` independent root tests, `5,000` cluster-preserving shuffles, strict zero regex overlap, zero double-counting):**
   - **2-Branch Proto-Dravidian (`3,417` clean etyma):** **`PhonEx = 14/19`** (null `8.76 ± 2.00`, **`z = +2.620, P = 0.0068`**); **`PhonSt = 18/19`** (null `13.37 ± 1.64`, **`z = +2.819, P = 0.0026`**).
   - **2-Language Dravidian (`5,116` clean etyma):** **`PhonEx = 15/19`** (**`z = +2.166, P = 0.0246`**); **`PhonSt = 18/19`** (**`z = +2.150, P = 0.0304`**).
   - **Brand-new sound-locked ligatures & modifiers (`building on it`):** `125` (`*vil-āḷ` = `[090 *āḷ + bow]`, "merchant/trader", `53` tokens) & `892` (`*vil` = bow/sell, `DEDR 5422/5421`, individual `P = 0.0494`, `90` tokens); `255` (`*mutal` = crocodile→principal/capital, `DEDR 4952/4950`, `114` tokens); `233` (`*veṭi-mīṉ / *vāku-mīṉ` = split→dawn/bright + `*mīṉ`, `DEDR 5473/5475` & `5202/5332`, `160` tokens + `234` caged `8` tokens); `413` (`*ari` = paddy-ear→tax/cut, `DEDR 215/216/212`, `47` tokens).

**Strictly rerunnable pipeline:** `python3 work_scripts/key4a_ligatures.py` (~14s runtime, outputs in `work_data/key4a/`).

---

## 1. Systematic Diacritic & Ligature Catalog

We cataloged **`141` signs** across 8 core families anchored to our 19 sound-locked signs, 4 loans, and basic numerals (`work_data/key4a/key4a_catalog.csv`), integrating `work_data/sign_shapes.csv`, `work_data/signlist/{mark_families.csv, merge_groups.csv}`, `work_data/lipi_mahadevan_crosswalk.csv`, and `work_data/reader_v3/corpus_soundfree_readings.csv`:

| Family | Anchor(s) | Cataloged Signs | Key Diacritics, Allographs & Ligatures (`total_intact` across `4,227` faces) |
|---|---|---:|---|
| **Fish** | `220 *mīṉ` (`382`), `235 *oḷi-mīṉ` (`209`) | 21 | `240` whiskers (`297`), `233` crossbar (`160`), `255` gharial (`114`), `231` vert-stroke (`76`), `226` caged (`37`), `236` caged-`235` (`24`), `243` hatched-hat (`15`), `241` caged-`240` (`13`), `222` bracketed (`13`), `232`/`234` caged (`8`/`8`) |
| **Jar** | `740 *kuṭi` (`1,499`) | 11 | `741` 1-stroke (`190`), `742` 2-stroke (`43`), `745` 3-stroke (`35`), `746` M345 (`4`), `744`/`747`/`743`/`748` (`3`/`2`/`1`/`1`), `749` roofed-`745`, `751` jar+wheel |
| **Cup / Vessel** | `700` (`498`), `705 *kalam` (`183`) | 13 | `706` M336 (`76`), `704` M336 (`5`), `703` 3-stroke (`11`), `711` U+X (`13`), `760`/`752` branching-U (`102`/`49`), `710`/`712`/`753` U+tree/wheel |
| **Tree / Comb** | `390 *tai` (`254`), `400 *cikk-` (`410`) | 12 | `405` M169 (`124`), `407` M169 (`123`), `406` M169 (`8`), `392` M162 (`4`), `413` double-comb/stalk M177 (`47`), `391` roofed tree (`10`), `393`/`394` |
| **Porter / Man** | `090 *āḷ` (`163`), `154 *kā` (`38`), `100 *talai` (`108`) | 29 | `156` M15 (`105`), `151` M12 plain porter (`83`), `158` M15 (`35`), `155`/`153` M15 (`6`/`5`), `140` woman (`90`), `125` man+bow (`53`), `095` man+stick (`28`), `091` 2×man (`24`), `097` bracketed (`20`), `101`/`103` bracketed-`100` (`10`/`4`), `093` 1-stroke (`9`), `159`/`161` M14 (`4`/`13`), `142`/`144` staff/caged (`83`/`4`) |
| **Diamond / Leaf** | `850 *kaṇ/kaṉ` (`49`), `790 *vaḷai` (`57`) | 19 | `861`/`817` M267 diamond+top (`254`/`165`), `806`/`803` leaf+tree (`123`/`111`), `840` 2×leaf (`104`), `845` hatched-`840` (`51`), `832` leaf+stroke (`44`), `804`/`807` caged (`6`/`2`), `812`/`825` hatched (`8`/`5`) |
| **Moon / Crescent** | `900 *tiṅkaḷ` (`94`), `923 *maruppu` (`37`) | 8 | `920` moon+leaf (`140`), `904`/`927` 2×moon M294 (`50`/`9`), `924` hatched-`923` (`10`) |
| **Other Locked & Nums** | `820`, `061`, `176`, `500`, `520`, `320`, `892`, `590`, nums | 28 | `892` bow (`90`), `503` striped hill (`79`), `617` 2×field-grid (`60`), `595` striped furnace (`51`), `175` plain seated (`21`), `048`/`049` bracketed-7 (`18`/`4`), `821` (`12`), `592` caged-`590` (`11`), `063` (`10`) |

---

## 2. Cross-Base Distributional Operator Lock (`5,000` Shuffles)

For every recurring graphic operator, we fixed the exact base signs `b_1..b_k` and compared the real base→compound shifts against **`5,000` random draws** pairing the exact same bases with random distinct corpus signs (`n ≥ 3`). Controlling for the base signs removes ceiling/floor regression artifacts (e.g., `740` and `700` already sit near `pos ≈ 0.85`). Full per-pair data is in `work_data/key4a/key4a_operator_tests.csv` and `work_data/key4a/key4a_operator_summary.json`.

| Operator (`k` pairs) | `ΔPos` (obs / null, `P`) | `ΔF400` (obs / null, `z`, `P`) | `ΔSeal` (obs / null, `P`) | `ΔBefN` (obs / null, `P`) | `cosL` (`P_gt`) | `cosR` (`P_gt`) | `cL − cR` (obs / null, `P`) | Functional Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **`cage_4corners`** (`k=8`) | **`+0.252`** / `+0.026` (**`0.0056`**) `7/8+` | **`+0.745`** / `+0.202` (**`z=+4.82, 0.0002`**) `8/8+` | `+0.085` / `−0.051` (`0.220`) | `+0.001` / `+0.054` (`0.469`) | `0.585` (`0.245`) | `0.153` (`0.451`) | `+0.432` / `+0.364` (`0.534`) | **LOCKED (`building on it`): Suffixal finalizer** (`8/8` jump to `$`/`400`) |
| **`side_brackets`** (`k=6`) | `−0.123` / `−0.190` (`0.492`) | `−0.197` / `−0.066` (`0.339`) | `−0.139` / `−0.082` (`0.638`) | `−0.024` / `+0.093` (`0.106`) | `0.173` (`0.904`) | **`0.608`** (**`0.0112`**) | **`−0.435`** / `−0.033` (**`z=−2.66, 0.0054`**) | **LOCKED (`building on it`): Prefixal / left-edge operator** (exact mirror of `cage_4corners`) |
| **`multi_stroke_inside`** (`k=10`) | `−0.415` / `−0.344` (`0.348`) `9/10−` | `−0.552` / `−0.429` (`z=−1.24, 0.216`) `10/10−` | **`+0.364`** / `+0.175` (**`z=+1.94, 0.0488`**) `10/10+` | **`+0.182`** / `+0.049` (**`z=+2.01, 0.0354`**) `8/10+` | **`0.349`** (**`0.0114`**) | `0.343` (`0.510`) | `+0.006` / `−0.105` (`0.379`) | **LOCKED (`building on it`): Construct-state / seal-header medializer** |
| **`internal_vert_stroke`** (`k=8`, 1-stroke subset) | `−0.223` / `−0.206` (`0.841`) `6/8−` | `−0.386` / `−0.257` (`0.248`) `7/8−` | `+0.294` / `+0.153` (`0.201`) `7/8+` | `+0.139` / `+0.044` (`0.161`) | `0.472` (`0.146`) | `0.390` (`0.285`) | `+0.082` / `+0.057` (`0.870`) | Same exact direction as `multi_stroke_inside` (`740→741` & `700→705/706` match identically); underpowered alone at `k=8` |
| **`doubling_graphic`** (`k=13`) | `−0.088` / `−0.065` (`0.723`) `7/13−` | `−0.024` / `+0.023` (`0.592`) | `−0.037` / `+0.045` (`0.343`) | **`+0.107`** / `−0.001` (`0.0502`) | `0.500` (`0.100`) | **`0.363`** (**`0.0144`**) | `+0.137` / `+0.199` (`0.526`) | **Split behavior (global shift null):** genuine duals (`900→904/927`, `615→617`, `790→840`) preserve `cosR` (`P=0.0144`); lexicalized pairs (`090→091`, `400→413`) diverge |
| **`horiz_hatching`** (`k=9`) | `−0.119` / `−0.087` (`0.676`) `7/9−` | `−0.156` / `+0.037` (`z=−1.81, 0.0658`) | `+0.139` / `+0.062` (`0.448`) | `+0.067` / `−0.026` (`0.146`) | `0.302` (`0.873`) | `0.129` (`0.907`) | `+0.173` / `+0.160` (`0.916`) | **Lexicalizing modifier** (both `cosL` and `cosR` sit *below* null — creates distinct lexical items like `590→595` forge, `923→924` overland) |
| **`roof_caret_hat`** (`k=4`) | `−0.198` / `−0.109` (`0.458`) `3/4−` | `−0.109` / `+0.013` (`0.467`) `4/4−` | `+0.139` / `−0.082` (`0.153`) `3/4+` | `−0.035` / `+0.035` (`0.509`) | `0.524` (`0.123`) | `0.303` (`0.614`) | `+0.221` / `+0.053` (`0.325`) | Consistent leftward/seal trend (`4/4` drop `F400`), underpowered at `k=4` |

### Key Structural Mechanism: `740 → 741` vs `700 → 705`
The parallel between the Jar (`740→741`) and Cup (`700→705/706`) families is exact and dramatic:
- **`740` (`n=1,499`) → `741` (`n=190`)**: `pos 0.880 → 0.357 (Δ=−0.524)`, `Fin 68.6% → 3.2%`, `F400 82.3% → 3.7% (Δ=−0.786)`, `Seal 54.2% → 73.2% (+18.9%)`, `BefN 2.0% → 26.3% (+24.3%)`.
- **`700` (`n=498`) → `705` (`n=183`) / `706` (`n=76`)**: `pos 0.789 → 0.349/0.336 (Δ=−0.440/−0.453)`, `Fin 74.3% → 1.6%/6.6%`, `F400 76.9% → 3.3%/9.2% (Δ=−0.736/−0.677)`, `Seal 4.6% → 52.5%/60.5% (+47.8%/+55.9%)`, `BefN 14.7% → 54.1%/52.6% (+39.4%/+38.0%)`.
- The exact same shift repeats on `740→742/745/746`, `700→703`, `220→231`, `790→832`, and `090→093` (`10/10` drop `F400`, `10/10` rise on seals). Inserting vertical stroke(s) converts a clause-final vessel/base sign into an **internal construct-state / head-of-quantity noun on seals** (`*uḷ-kuṭi / *oru-kuṭi`, `*iru-kuṭi`, `*mū-kuṭi`, `*kalam` before numerals).
- **Adjacent corpus doubling (`X-X`, `k=11` recurring signs with `n≥4`)**: mirrors `doubling_graphic` (`mean ΔPos = −0.182`, `cosL = 0.485`, `cosR = 0.425`): `090-090` (`n=12`) collapses from `pos=0.761` to clause-initial `0.111` just like graphic `091` (`pos=0.037`), while `615-615` (`n=55`) jumps to `pos=0.703, F400=0.636` just like graphic `617` (`pos=0.717, F400=0.667`)!

---

## 3. Distributional Allograph Identity Lock (`5,000` Shuffles)

We tested `24` candidate allograph/base pairs against `5,000` random partner draws from the intact sign pool (`n ≥ 4`), measuring left/right neighbor cosine (`cosL`, `cosR`, `cosMean`), exact `X_Y` frame swaps, positional delta `|ΔPos|`, and Mahadevan M77 / MaYIG concordance (`work_data/key4a/key4a_allograph_tests.csv`).

### A. Locked Allographs (`building on it` — `11` signs, `+574` intact tokens)

| Pair (`base ~ variant`) | `n_a / n_b` | M77 | `|ΔPos|` | `cosL` | `cosR` (`P`) | `cosMean` (`P`) | Exact Swaps (`P`) | Status & Notes |
|---|---:|---|---:|---:|---:|---:|---:|---|
| **`705 ~ 706`** (`*kalam`) | `183 / 76` | `336 / 336` | `0.013` | `0.918` | `0.974` (`0.0064`) | **`0.946` (`0.0024`)** | **`17` (`0.0024`)** | **`building on it`**: identical (`R:'033'` 51% vs 51%) |
| **`705 ~ 704`** (`*kalam`) | `183 / 5` | `336 / 336` | `0.082` | `0.631` | `0.103` (`0.0534`) | `0.367` (`0.4359`) | `2` (`0.2154`) | **`building on it`**: same M336 & shares rare `R:167` (2/5), `255` (1/5) |
| **`154 ~ 158`** (`*kā`) | `38 / 35` | `15 / 15` | `0.124` | `0.919` | `0.884` (`0.1844`) | **`0.901` (`0.0024`)** | **`6` (`0.0042`)** | **`building on it`**: M15 closer (`806-154/158`) |
| **`154 ~ 156`** (`*kā`) | `38 / 105` | `15 / 15` | `0.038` | `0.237` | **`0.998` (`0.0074`)** | **`0.617` (`0.0092`)** | **`5` (`0.0100`)** | **`building on it`**: M15 (`003-156` literal yoke-load) |
| **`154 ~ 155`** (`*kā`) | `38 / 6` | `15 / 15` | `0.265` | `0.678` | `0.841` (`0.1920`) | **`0.760` (`0.0076`)** | `2` (`0.0624`) | **`building on it`**: M15 |
| **`154 ~ 153`** (`*kā`) | `38 / 5` | `15 / 15` | `0.004` | `0.026` | **`0.999` (`0.0036`)** | **`0.512` (`0.0446`)** | `1` (`0.2510`) | **`building on it`**: M15 |
| **`154 ~ 151`** (`*kā` base) | `38 / 83` | `15 / 12` | `0.002` | `0.009` | **`0.984` (`0.0250`)** | `0.497` (`0.0550`) | `1` (`0.2616`) | **`building on it`**: M12 plain porter base (`pos 0.91`, `F400 89%`, `seal 67%`) |
| **`390 ~ 392`** (`*tai`) | `254 / 4` | `162 / 162` | `0.190` | `0.678` | `0.805` (`0.2272`) | **`0.742` (`0.0116`)** | `2` (`0.3075`) | **`building on it`**: M162 |
| **`390 ~ 405`** (`*tai`) | `254 / 124` | `162 / 169` | `0.096` | `0.674` | `0.898` (`0.1608`) | **`0.786` (`0.0050`)** | **`13` (`0.0082`)** | **`building on it`**: MaYIG-merged; `590-390` (61×) / `590-405` (29×) |
| **`390 ~ 406`** (`*tai`) | `254 / 8` | `162 / 169` | `0.056` | `0.609` | `0.897` (`0.1710`) | **`0.753` (`0.0074`)** | `5` (`0.0684`) | **`building on it`**: M169 = `405` |
| **`390 ~ 407`** (`*tai`) | `254 / 123` | `162 / 169` | `0.092` | `0.442` | **`0.942` (`0.0252`)** | **`0.692` (`0.0162`)** | **`10` (`0.0184`)** | **`building on it`**: M169 (`11` swaps w/ `405`, `P=0.0060`); note medium split (`407` is 61% copper tablets vs `390` 76% seals) |

### B. Locked Unsolved Allograph Pairs (`testing it`) & Honest Non-Locks
- **Unsolved allograph merges locked (`testing it`, ready for Key #4B/4C):**
  - **`861 ≡ 817`** (`M267/267`, `254 + 165 = 419` tokens): `cosL = 0.980`, `cosR = 0.972`, **`cosMean = 0.976 (P = 0.0034)`**, `6` swaps (`P = 0.0126`). Distinct from `850` (`M261`).
  - **`760 ≡ 752`** (`M347/358`, `102 + 49 = 151` tokens): `cosR = 0.999 (P = 0.0110)`, **`cosMean = 0.574 (P = 0.0246)`**, `8` swaps (`P = 0.0166`), `|ΔPos| = 0.003`.
  - **`803 ≡ 806`** (`M387/389`, `111 + 123 = 234` tokens): `cosL = 0.919`, **`16` exact swaps (`P = 0.0088`)**, `|ΔPos| = 0.043`.
  - **`904 ≡ 927`** (`M294/294`, `50 + 9 = 59` tokens): **`cosMean = 0.860 (P = 0.0038)`**, `6` swaps (`P = 0.0410`), and `900 ~ 904` (`cosR = 0.905, P = 0.0490`) confirms `*iru-tiṅkaḷ` ("2 months").
  - **`745 ≡ 746`** (`M345/345`, `35 + 4 = 39` tokens): `cosL = 0.825`, **`cosMean = 0.594 (P = 0.0298)`**.
- **Honest Non-Locks caught by 5,000 shuffles (kept out of `building on it` → `testing it`):**
  - **`061 vs 063`**: Crosswalk maps `063` to `M343` (NOT `M124/125`), `cosMean = 0.406 (P = 0.1994)`, `2` swaps (`P = 0.1530`).
  - **`820 vs 821`**: Same M391 (`cosL = 0.770`), but `cosR = 0.239 (P = 0.3635)`, `cosMean = 0.504 (P = 0.2907)`, `|ΔPos| = 0.311` (`n = 12`).
  - **`176 vs 175`**: `cosL = 0.910` (`^`, `002`), **but `cosR = 0.195 (P = 0.3371)`** (`176` goes 71% before `740`, `175` does not). This is structural information: `175` is NOT a free allograph of `176`; the 4 back-strokes on `176` shift its right-hand collocation onto `740`!
  - **`154 vs 161` (`M15/14`)**: `cosR = 0.968 (P = 0.0758)`, `0` swaps (`P = 1.0`).

---

## 4. Zero-Artifact Proto-Dravidian DEDR Ligature & Modifier Lock (`5,000` Shuffles)

Reusing the exact zero-artifact `dedr_entries.tsv` parser and `InMemoryLex` from `key2a_rebus_lock.py` and `key3a_sound_sweep.py` (with automated strict zero-overlap assertion between every visual regex `rxA` and domain regex `rxB`, and deduplicating `125/892` into ONE single independent root test so `*vil` is never double-counted), we ran **`5,000` exact cluster-preserving sound shuffles** across **`19` independent ligature/modifier targets** (`work_data/key4a/key4a_dedr_ligatures.csv`, `work_data/key4a/key4a_dedr_summary.json`):

| DEDR Filter | Test Mode | Real Hits | Null Mean ± SD (`5,000` shuf) | `z` | Empirical `P` |
|---|---|---:|---:|---:|---:|
| **2-Branch Proto-Dravidian** (`3,417` etyma) | **`PhonEx` (distinct cluster)** | **`14 / 19`** | `8.76 ± 2.00` | **`+2.620`** | **`0.0068`** |
| **2-Branch Proto-Dravidian** (`3,417` etyma) | **`PhonSt` (distinct cluster)** | **`18 / 19`** | `13.37 ± 1.64` | **`+2.819`** | **`0.0026`** |
| **2-Branch Proto-Dravidian** (`3,417` etyma) | `AscEx` (distinct cluster) | `14 / 19` | `11.46 ± 1.81` | `+1.400` | `0.1252` |
| **2-Branch Proto-Dravidian** (`3,417` etyma) | `DirectPoly` (domain-perm) | `15 / 19` | `12.10 ± 1.80` | `+1.611` | `0.0890` |
| **2-Language Dravidian** (`5,116` etyma) | **`PhonEx` (distinct cluster)** | **`15 / 19`** | `11.02 ± 1.84` | **`+2.166`** | **`0.0246`** |
| **2-Language Dravidian** (`5,116` etyma) | **`PhonSt` (distinct cluster)** | **`18 / 19`** | `15.15 ± 1.32` | **`+2.150`** | **`0.0304`** |

### Per-Sign Audited DEDR Ligature & Modifier Table

| Sign(s) | Intact Tok | Visual Decomposition | Candidate Proto-Dravidian Reading | Audited Zero-Artifact DEDR Bridge(s) (`2-branch` unless noted) | `2-br` `Ex`/`St` (`p_Ex`) | Status |
|---|---:|---|---|---|---:|---|
| **`125` + `892`** | `53 + 90` | `125 = [090 *āḷ + 892 bow]`; `892` = bow & arrow (`M307`) | **`*vil-āḷ` ("merchant") / `*vil` ("sale/bow")** | **`DEDR 5422 *vil`** ('bow, archer') ↔ **`DEDR 5421 *vil`** ('to sell, sale, price') `[2-br PhonEx]` | `1`/`1` (**`0.0494`**) | **`building on it`** |
| **`255`** | `114` | Gharial/crocodile (`M51`, Mound F granary tablets) | **`*mutal` ("principal / capital / first-issue")** | **`DEDR 4952 *mutalai`** ('crocodile', only 10 reptile etyma) ↔ **`DEDR 4950 *mutal`** ('first, principal, capital') `[2-br PhonSt]` | `0`/`1` (`p_St=0.1474`) | **`building on it`** |
| **`233` (+`234`)** | `160 (+8)` | `220 *mīṉ` + horizontal dividing crossbar | **`*veṭi-mīṉ` / `*vāku-mīṉ` ("dawn/bright star")** | **`DEDR 5473 *veṭi`** ('split, crack') ↔ **`5475 *veṭi`** ('dawn, break of day') `[2-br PhonEx]`; **`5202 *vaku`** ('divide') ↔ **`5332 *vāku`** ('brightness') `[2-br PhonEx]` | `1`/`1` (`0.3745`) | **`building on it`** |
| **`231`** | `76` | `220 *mīṉ` + 1 internal vertical stroke | **`*uḷ-mīṉ` / `*iṟai-mīṉ`** | Operator-locked `internal_vert_stroke`; **`DEDR 528 *iṟai`** ('inside') ↔ **`527 *iṟai`** ('great, chief') `[2-br PhonEx]`; `DEDR 7 *akam` `[DIRECT]` | `1`/`1` (`0.2458`) | **`building on it`** |
| **`226`** | `37` | `220 *mīṉ` + 4 corner strokes (`cage_4corners`) | **`*mīṉ-kūṭu` / `*mīṉ-[CAGE]`** | Operator-locked `8/8` finalizer (`P=0.0002`); **`DEDR 1883 *kūṭu`** ('cage') ↔ **`1655 *kuṭi`** ('house') `[2-br PhonSt]`; `3485 *toṭṭi` ('enclosure') ↔ `3546 *tōṭṭi` ('guard') `[2-br PhonEx]` | `1`/`1` (`0.2969`) | **`building on it`** |
| **`741` (–`748`)** | `190 (+89)` | `740 *kuṭi` + 1–4 internal strokes | **`*uḷ-kuṭi` / `*oru-kuṭi` (`*iru`/`*mū`/`*nāl-kuṭi`)** | Operator-locked `10/10` construct-state medializer (`dSeal P=0.0488, dBefN P=0.0354`) + `DEDR 698 *uḷ` / `990 *oru` + `1655 *kuṭi` | `1`/`1` (`0.8358`) | **`building on it`** |
| **`413`** | `47` | Double-sided cereal stalk (`M177`, precedes `575` grain measure) | **`*ari` ("ear of paddy / grain-tax")** | **`DEDR 215 *ari`** ('ear of paddy, rice, husked grain') ↔ **`DEDR 216 *ari`** ('tax, duty') & **`212 *ari`** ('cut, reap') `[2-br PhonEx]` | `1`/`1` (`0.7514`) | **`building on it`** |
| `240` | `297` | `220 *mīṉ` + oblique cheek-whiskers / fins | `*cāy-mīṉ` / `*ciṟai-mīṉ`? | `DEDR 2456 *cāy` ('incline/slant') ↔ `2457 *cāy` ('brilliance') `[2-br PhonEx]`; `2591 *ciṟai` ('wing') ↔ `2589 *ciṟa` ('eminent') `[2-lg PhonSt]` | `1`/`1` (`0.3101`) | `testing it` |
| `140` | `90` | Woman with round breasts & raised arm (`M17`) | `*ammā` / `*il` | `DEDR 183 *ammā` ('mother, matron, lady, goddess') `[DIRECT]`; `494 *il` ('wife/house') `[DIRECT]` | `1`/`1` (`0.5705`) | `testing it` |
| `595` | `51` | Striped furnace / box+bar (citadel forge) | `*aṭu` / `*kaṉal` | `DEDR 76 *aṭu` ('oven, furnace, melt') `[DIRECT]`; `1406 *kaṉal` ('fire, burn') `[DIRECT]` | `1`/`1` (`0.4005`) | `testing it` |
| `503` | `79` | Horizontally striped hill/slope (`M204`) | `*vāram` / `*karai` | `DEDR 5360 *vāram` ('mountain slope') ↔ `5359 *vāram` ('land rent, crop share') `[2-lg PhonEx]` | `1`/`1` (`0.5815`) | `testing it` |
| `095` | `28` | `090 *āḷ` + short stick/hammer (copper tablets) | `*koṭṭu-āḷ` / `*aṟai-āḷ`? | `DEDR 2063 *koṭṭu` ('hammer/beat') `[DIRECT]`; `1417/1416 *kā` duplicates `154` | `1`/`1` (`0.4493`) | `testing it` |
| `920` | `140` | `900 *tiṅkaḷ` + leaf at middle (office opener) | `*tiṅkaḷ-[il]`? | Compositional `[900 *tiṅkaḷ + leaf]`; `DEDR 3213 *tiṅkaḷ` `[DIRECT]` | `0`/`0` (`1.0000`) | `testing it` |
| `861` (`≡817`) | `254+165` | Diamond + small diamond at top (`M267`) | `*alaku` / `*ucci`? | Multiple rivals (`DEDR 237/238 *alaku` `[2-lg]`, `579 *ucci`); M267 merge locked (`P=0.0034`) | `0`/`1` (`p_St=0.9350`) | `testing it` |
| `840` | `104` | Doubled overlapping leaf (`2× 790`, `cosL=0.815`) | `*2× vaḷai`? | Distributional pair of `790`; no unique single-root DEDR rebus beyond `*vaḷai` | `1`/`1` (`0.7329`) | `testing it` |
| `832` | `44` | `790` leaf + 1 internal stroke (`M375`) | `*uḷ-vaḷai` / `*eḷ-uḷ`? | Obeys `internal_vert_stroke` (`ΔF400=−0.14, ΔSeal=+0.16`); `DEDR 215/216` overlaps `413` | `1`/`1` (`0.7115`) | `testing it` |
| `803` (`≡806`) | `111+123` | Leaf + `390` tree (`M387/389`, `16` swaps) | `*il-tai`? | Graphic ligature `[leaf + 390]`; `497 ilai` ↔ `494 il` fails 3-char stem cutoff | `0`/`1` (`p_St=0.7145`) | `testing it` |
| `700` | `498` | Plain U cup (~9.24 L, base of `705 *kalam`) | `*akal` / `*aḷ`? | High shuffle baseline (`0.782`) due to multiple broad vessel↔measure roots | `0`/`1` (`p_St=0.7822`) | `testing it` |
| **`391`** | `10` | `390 *tai` + roof/caret hat (smithy copper) | **null** | Broad baseline (`null_rate = 0.783`); zero clean Proto-Dravidian tree-roof↔smithy rebus | `1`/`1` (`0.7834`) | **`null`** |

---

## 5. Exact Token & 100%-Face Coverage Jump (`4,227` Intact Faces)

Every tier below is strictly disjoint (`work_data/key4a/key4a_coverage.json`, `work_data/key4a/key4a_coverage_breakdown.csv`):

| Coverage Tier | Signs | Lipi Intact (`3,600` faces, `13,209` tok) | Unseen M77 Intact (`627` faces, `2,161` tok) | **Combined Intact (`4,227` faces, `15,370` tok)** | **100%-Glossed Faces (Combined)** |
|---|---:|---:|---:|---:|---:|
| `01` Key #2A Locked | 11 | `2,997` (`22.69%`) | `486` (`22.49%`) | `3,483` (`22.66%`) | `96` (`2.27%`) |
| `02` Key #3A Locked | 19 | `3,690` (`27.94%`) | `573` (`26.52%`) | `4,263` (`27.74%`) | `185` (`4.38%`) |
| `03` Baseline (`19` + `4` loans + `10` basic nums) | 33 | `6,013` (`45.52%`) | `914` (`42.30%`) | **`6,927` (`45.07%`)** | **`441` (`10.43%`)** |
| `04` + Key #4A Allographs (`building on it`: `+11`) | 44 | `6,530` (`49.44%`) | `971` (`44.93%`) | `7,501` (`48.80%`, `+3.73 pp`) | `549` (`12.99%`, `+108`) |
| `05` + Key #4A Operators (`building on it`: `+19`) | 63 | `6,980` (`52.84%`) | `1,060` (`49.05%`) | `8,040` (`52.31%`, `+3.51 pp`) | `635` (`15.02%`, `+86`) |
| **`06` + Key #4A ALL `building on it` (`+36` total)** | **69** | **`7,388` (`55.93%`, `+10.41 pp`)** | **`1,124` (`52.01%`, `+9.71 pp`)** | **`8,512` (`55.38%`, `+10.31 pp`)** | **`694` (`16.42%`, `+253` / `+57.4%`)** |
| `07` + Key #4A `testing it` (`+31` more) | 100 | `9,478` (`71.75%`) | `1,387` (`64.18%`) | `10,865` (`70.69%`, `+15.31 pp`) | `1,535` (`36.31%`, `+841`) |

### Real Newly 100%-Glossed Multi-Sign Inscriptions (`building on it` only)

| Object | Site & Kind | Sign Sequence | Sign-by-Sign Gloss (`building on it`) |
|---|---|---|---|
| **Lipi `2068.1`** (also `2069.1`) | Lothal, sealing | `705-500-741-001-055-220-740-090` | `*kalam *pāy *uḷ-kuṭi *oru *paṉṉiru *mīṉ *kuṭi *āḷ` ("Ship-sail, inner-house 1×12, Star-house manager") |
| **Lipi `2838.1`** | Mohenjo-daro, seal | `125-390-741-176-740` | `*vil-āḷ *tai *uḷ-kuṭi *iṟai *kuṭi` ("Merchant/trader, weaver/craftsman, inner-house tax-house") |
| **Lipi `2871.1`** | Mohenjo-daro, seal | `820-002-032-220-233-100-740` | `*kāl *iru *iru *mīṉ *veṭi-mīṉ *talai *kuṭi` ("Quarter 2-2, Star / Dawn-Star, Chief House") |
| **Lipi `3551.1`** | Mohenjo-daro, seal | `176-704-255-740` | `*iṟai *kalam *mutal *kuṭi` ("Tax-measure, principal/capital house") |
| **Lipi `643.1`** | Harappa, tablet | `032-255-740` | `*iru *mutal *kuṭi` ("2 principal-issue, house") |
| **Lipi `8.1`** | Allahdino, seal | `235-705-033-904-740` | `*oḷi-mīṉ *kalam *mū *iru-tiṅkaḷ *kuṭi` ("Bright-Star, 3 measures, 2 months, House") |
| **Unseen `M3218`** | Lothal, seal | `390-741-032-226` | `*tai *uḷ-kuṭi *iru *mīṉ-[CAGE]` ("Weaver/craftsman, inner-house, 2 Star-enclosure") |
| **Lipi `127.1`** | Dholavira, seal | `032-892-151` | `*iru *vil *kā` ("2 trade/sale guard") |

---

## 6. Honest Nulls & Next Targets

1. **`doubling_graphic` global positional shift = null** (`ΔPos = −0.088, P = 0.723`; `ΔF400 = −0.024, P = 0.592`) because graphic doubling splits into two distinct processes: grammatical duals (`900→904/927`, `615→617`, `790→840`, driving `cosR P = 0.0144`) vs lexicalized signs (`090→091`, `400→413`, `850→861`).
2. **`horiz_hatching` is a lexicalizing modifier, not an inflectional operator** (`cosL = 0.302` and `cosR = 0.129` both fall below random null).
3. **`391` (`[390 + caret hat]`, smithy copper) = null** for a standalone Proto-Dravidian rebus (`null_rate = 0.783`, zero clean tree-roof↔smithy root).
4. **Three candidate allographs failed 5,000-shuffle verification** and were kept in `testing it`: `063` (`M343 ≠ M124`, `P = 0.199`), `821` (`|ΔPos| = 0.311, P = 0.291`), and `175` (uncaged base of `176`, `cosL = 0.910` but `cosR = 0.195, P = 0.214`).
5. **Highest-leverage remaining `testing it` prizes for Key #4B/4C:** cracking just FOUR sign-groups — **`700`** (`498` tokens), **`861 ≡ 817`** (`419` tokens, already merged at `P = 0.0034`), **`240`** (`297` tokens), and **`803 ≡ 806`** (`234` tokens, `16` swaps) — adds **`+1,448` intact tokens (`+9.42 pp`)**, pushing `building on it` coverage past **`64.8%`**!
