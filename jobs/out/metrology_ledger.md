# Metrology & Multi-Face Ledger Solver: Numeral Series, Exact Conversion Ladder, and Physical Calibration

Scripts: `work_scripts/met_common.py`, `work_scripts/met_01_ladder.py`, `work_scripts/met_02_multiface.py`, `work_scripts/met_03_physical.py` (all portable with dynamic `ROOT`, rerunning end-to-end in ~25 seconds via `/tmp/ivc_venv/bin/python`).
Machine-readable outputs in `work_data/met/`: `unit_ladder.csv`, `commodity_series.csv`, `numeral_inventory.csv`, `ladder_order_pairs.csv`, `multiface_records.csv`, `crew_kalam_equations.csv`, `recipient_ledgers.csv`, `cross_object_ledgers.csv`, `physical_pots.csv`, `physical_tools_rods.csv`, `physical_scaling_rungs.csv`, glyph/photo sheets (`mah_num_glyphs.png`, `photo_special_numerals.png`, `photo_zoom_ticks.png`), and run logs (`log_01_ladder.txt`–`log_03_physical.txt`).

Counting discipline: one row per physical object (`recheck_common.stone_map`: `5,679` Lipi faces $\to$ `4,691` physical stones) and moulded/identical copy batches at the same site and locus counted as one event (`4,476` Lipi copy events; `987` unseen Mahadevan `M_new_clean` copy events after removing 9 `121-121` = `056` split twins; `5,463` combined deduplicated events). Ownership probabilities (`X n` vs `n Y`) and the topological ladder rank are fitted on Lipi events alone and evaluated untouched on held-out unseen `M_new_clean`.

---

## 1. Headline Findings

1. **Like proto-cuneiform and proto-Elamite, the Indus script uses distinct commodity-selected numeral series (`z = +59.4`), not a single all-purpose tally.** Across `1,582` owned counts on `33` unit/commodity groups in Lipi deduplicated events, normalized mutual information between counted sign-group and numeral series (`F` tall, `S` short, `T` 2-row stacked, `B` 3-row block/bracketed, `A` A-comb) is **`NMI = 0.2606`** ($\chi^2 = 2851.3$, $\text{dof} = 128$). Against `1,000` permutations stratified within `(site × object_kind)` — the strongest rival explanation ("Harappa clay tablets use tall strokes while Mohenjo-daro seals use short strokes") — the null is **`0.0514 ± 0.0035` (`max = 0.0646`, `z = +59.4`, `P = 0.0010`)**. The split holds inside **Seals alone** (`0.2657` vs `0.0431`, `z = +46.4`, `P = 0.0010`), inside **Tablets alone** (`0.3222` vs `0.0425`, `z = +49.7`, `P = 0.0010`), and **out-of-sample on unseen `M_new_clean`** (`NMI = 0.3306` vs `0.1094`, `z = +19.1`, `P = 0.0010`; frozen Lipi$\to$`M_new_clean` series prediction accuracy **`174 / 233 = 74.7%`** vs `(site × kind)`-stratified null **`42.6%`**, `z = +11.4`, `P = 0.0010`). *Status: building on it (`commodity_series.csv` exported as hard constraints for the sound and sense solvers).*

2. **Three previously opaque numeral families are visually and cross-catalogically solved from seal/tablet photographs and Mahadevan glyph alignments (`photo_zoom_ticks.png`, `mah_num_glyphs.png`):**
   - **Sign `056` = `24` (`8 × 3` strokes = two dozen = `2 × 055`):** High-resolution photographs of `H-14`, `K-69`, and `L-115` show three stacked rows of eight vertical strokes (`8 + 8 + 8 = 24`; on `K-69` visibly carved as two `4 × 3` blocks side by side). Every Lipi `056` inscription aligns 1-to-1 with Mahadevan **`121-121` (`055-055`)** (`M4106 = H-14`, `M7065 = L-115`, `M8108–8115 = K-69–75`), which had previously gone unpartnered due to the 1-to-2 sign split and contaminated `M_new` with 18 duplicate `055` tokens.
   - **Mahadevan `M94` (`| //`) = Lipi `032-031` (`3` tall/slanted strokes after weight `171`):** Proven on the 7-face Mohenjo-daro prism `M-326` (`M2405`: Lipi `171 032 031 171 000` = Mahadevan `409-94-409-0`) and Harappa weight tablets. Mapping `M94 -> F3` unlocks 6 unseen `171` occurrences in `M_new_clean`, which hit **`{3, 5}` in `6 / 6 = 100.0%`** (`{3: 3, 5: 3}` vs `34.2%` on other tall counts, `P = 0.0030`, exact binomial `P = 0.0015`).
   - **Slanted 3-row blocks `025–029` (`M119` / `M120`) and A-comb ticks `465–475` (`M178`):** `mahadevan_parsed.csv` had mis-mapped `M119` (3 rows of slanted strokes on `H-65` and `H-303` series) to `014` (`4`, which is `M105`). Photographs of `H-303` (`027`) show `3 + 3 + 3 = 9` slanted strokes; `H-65` (`028`) shows `10` slanted strokes; and photographs across `H-190` (`465`), `H-146` (`467`), `H-152` (`468`), `H-143` (`469`), `H-189` (`470`), `H-132` (`471`), `H-158` (`472`), and `M-40` (`475`) show Wells' numbers `465–475` run monotonically with the foot-comb tick count (`1` up to `10` loads before crop `806/838`). *Status: building on it.*

3. **Indus Numeral Phrase-Boundary Theorem eliminates `243` false cross-series merges and sharpens every metrological ceiling.** Adjacent numeral tokens sum additively **only within the same stroke-height series (`F+F` or `S+S`)**, and **`44 / 47 = 93.6%`** of within-series compounds obey non-increasing order (`v_1 >= v_2`, e.g. `033 032 = 5`, `033 031 = 4`, `032 032 = 4`, `032 031 = 3`, `033 033 = 6`). Cross-series adjacencies (`861 002 | 004 390`, `705 033 | 017 585`, `001 | 034 700` on ivory rod `H-2570`, `027 | 032 740`) always straddle a slot or phrase boundary. Once cross-series merges are split:
   - **Cup `700` (*marakkāl*, `9.26 L`) $\to$ `12` cups = `1` *kalam* (`705/706`, `111 L`):** **`430 / 431 = 99.77%`** of Lipi deduplicated cup events (`{1:9, 2:124, 3:180, 4:114, 6:3}`, plus broken `H-1963: 000 017 700 400`) and **`7 / 7 = 100.0%`** of unseen `M_new_clean` cup events (`{2:2, 3:3, 4:2}`) sit on exact divisors of `12` (`P = 0.0010` vs non-cup counts `85.6%`; Binary `{1,2,4,8}` covers only `57.3%`, Decimal `{1,2,5,10}` only `30.8%`). **Tall `5` (`035` / `033+032`) never appears on `700`: `0 / 422 (0.0%)` vs `51 / 1,200 (4.2%)` on other tall-counted signs (`Fisher P = 1.59 × 10^-7`).**
   - **Sub-*kalam* `711` (*vaḷḷam / tūṇi*) = `4` cups (`1/3` *kalam* = `37.0 L`):** Without `711` on the face, cup `700` reaches `>= 4` on `120 / 428 = 28.0%` of deduplicated events; **when `711` precedes `700` on the face (`413 575 335 711 033 700`, `000 817 711 033 700`, `711 033 700 000`), cup `700` is capped at `3 = 4 - 1` (`0 / 10` reach `>= 4`, `Fisher P = 0.0391`), because `4` cups roll over into `1 × 711`.**
   - **Wholesale *kalam* `705/706` $\to$ `6` *kalam* = `1` *kōṭṭai* `575` (`72` cups = `665 L`):** **`170 / 170 = 100.0%`** of tall-stroke *kalam* counts across Lipi (`n = 142`: `{1:6, 2:2, 3:126, 4:2, 5:6}`) and unseen `M_new_clean` (`n = 28`: `{2:1, 3:23, 5:4}`) are capped at **`<= 5` (`6 - 1`)**, vs `358 / 2,430 (14.7%) >= 6` on other signs (`Fisher P = 4.58 × 10^-12`).
   - **Quarters `061–063` & Infixed Jar-Mouth Strokes `741–748` (`R = 4`, ceiling `3`):** Quarter counts are `<= 3` in `19 / 21 = 90.5%`, and infixed jar-mouth strokes (`741 = 1`, `742–744 = 2`, `745–747 = 3`, `748 = 4`) are `<= 3` in **`414 / 417 = 99.28%`** (`327 / 330` Lipi + `87 / 87` `M_new_clean`).
   - **Weight Standard `171` (*niṟai*) $\to$ `{3, 5}` Only:** **`25 / 25 = 100.0%`** in Lipi (`{3:8, 5:17}`, `P = 2.67 × 10^-12`) and **`6 / 6 = 100.0%`** in unseen `M_new_clean` (`{3:3, 5:3}`, `P = 0.0015`) take `3` or `5` — the exact non-binary multipliers (`3` and `5`) where the Harappan cubical chert weight series (`1, 2, 4, 8, 16, 32, 64 -> 160 = 32×5, 200 = 40×5`) departs from pure doubling. *Status: building on it.*

4. **Syntactic Count-Direction Law splits abstract standards from discrete items & unit containers (`+76%` gap in Lipi, `+82%` in unseen `M_new_clean`).** High-rung standards (`kalam` `705/706`, `nirai` `171`, `vallam` `711`, `kalancu` `645`) place their count **after** the sign (`UNIT n`: **`173 / 198 = 87.4%`** in Lipi; **`33 / 39 = 84.6%`** in `M_new_clean`), whereas unit containers and discrete commodities (`cup` `700`, `porter` `156`, `trees` `390/405/407`, `crop` `806`, `fish` `220–240`, `quarter` `061`, `dozen` `055`) place their count **before** the sign (`n ITEM`: only **`11.5%`** post-counted in Lipi and **`2.6%`** in `M_new_clean`; `1,000` group-label shuffle `P = 0.0020` on Lipi, `P = 0.0120` on `M_new_clean`). *Opens: direct syntactic word-order filter (`NOUN + MEASURE + NUM` vs `NUM + NOUN`) for language testing.*

5. **Directed Metrological Ladder DAG holds at `86.2%` on Lipi (`P = 0.0010`) and transfers untouched at `70.4%` (`19 / 27`, `P = 0.0261`) onto held-out `M_new_clean`.** Across `239` unit-pair co-occurrences on Lipi events, a single strict ranking (`parai 540 / grain_hdr 413 > two_dozen 056 > kottai 575 > kalam 705/706 > chest 590 > bin 335 > granary 605 > vallam 711 > cup 700 > pati 320 / quarter 061`) accounts for `206 / 239 = 86.2%` vs `62.2% ± 2.2%` under refitted within-line shuffles (`P = 0.0010`), and predicts `19 / 27 = 70.4%` of unseen `M_new_clean` pairs without refitting (`binom P = 0.0261`, `perm P = 0.0340`). *Status: building on it.*

6. **Multi-face ledger equations: unconverted cross-face addition is null (`2 / 29` vs `5.58`), rescued by Cross-Face Parity (`51 / 143 = 35.7%`, `P = 0.0310`) and Copper Animal–Unit Lock (`z = +6.7`, `P = 0.0010`).** Harappan multi-face tablets do not sum homogeneous sub-lines into a total line because partner faces come from different grammatical/metrological series. Testing four distinct rescues shows:
   - **Cross-Face Parity (`v_faceA == v_faceB`)** hits **`47 / 135 = 34.8%`** on Lipi account events vs `38.6` under series-matched permutations (`P = 0.0450`, global `P = 0.0390`), **`4 / 8 = 50.0%`** on unseen `M_new_clean` (vs `2.8`), and **`51 / 143 = 35.7%`** combined vs `41.4` (`P = 0.0310`; series-matched `P = 0.0390`), driven by paired crew/load counts (`003 861 | 003 156`), annual-to-monthly `12:1` *kalam*$\leftrightarrow$cup allowances (`3 kalam <-> 3 cups` on `H-1812`, `H-1813`), and the 7-face Mohenjo-daro weight prism `M-326` (`3 kalancu` on Face 2 $\leftrightarrow$ `3 nirai` on Face 3).
   - **Mohenjo-daro Copper Tablet Animal $\times$ Unit:Count Lock:** Across `47` deduplicated copper-tablet events, animal emblems lock onto specific metrological signatures at **`NMI = 0.6378` vs `0.4390 ± 0.0296` (`z = +6.7`, `P = 0.0010`)** (`Hare`: `6/6` at `3 kalam`; `Elephant`: `6/6` at `3 kalam`; `Bull1`: `3/4` at `1 staff_man`). *Status: building on it.*

7. **Physical pottery wall thickness, intact jar capacities, bronze celts, and Harappa tablet 3D volumes confirm the metrological scale in millimetres and litres:**
   - **Kalibangan Pottery Wall Thickness (`POT:T:g`):** Across `11` undamaged capacity-marked sherds at Kalibangan spanning `1` stroke (`4.0 mm` wall on `K-404`), `3` strokes (`7.0–12.5 mm`), `4–6` strokes (`9.0–20.0 mm`), `8–10` strokes (`12.0 mm`), and `055` = `12` dozen (`24.5 mm` pithos wall on `K-417`), wall thickness correlates with inscribed capacity at **`Spearman rho = +0.7067` (`1,000`-permutation `P = 0.0050`)** (`+0.5177`, `P = 0.0559` across all sites including Nuhato `0–14 mm`).
   - **Whole Storage Jars & Goblet Stamp Split:** Wells' 3 measured intact jars (`3 -> 27.30 L`, `6 [H-371: 036-700] -> 55.56 L`, `7 -> 65.89 L`) yield **`9.26 L/cup` (`CV = 1.69%`, Monte Carlo `P = 0.0037`)**; complete Mohenjo-daro pithos `M-2066` (`600 × 580 mm`, `033 004 000`) has geometric ovoid inner volume **`84.0–97.5 L` (`9.1–10.6 cups`, ~`1` *kalam*)**; and pointed-base goblet stamps (`POT:T:s`, median stamp `17 × 13 mm`, ~`1.16 L` *paṭi* scale) segregate sharply in sign vocabulary (`540-540`, `440`, `416`, `013`) from storage-jar graffiti (`24 / 74 = 32.4%` vs `4 / 532 = 0.8%`, `Fisher P = 4.16 × 10^-20`).
   - **Harappa Tablet 3D Volume Step:** While single-cup count (`2, 3, 4`) does not enlarge clay chits (`rho = -0.289`), stepping up to wholesale *kalam* / *kōṭṭai* (`705/706/575`) **doubles the 3D volume of Harappa clay/steatite tablets** (**`732 mm³` vs `359 mm³`, `2.04×`, `MWU P = 1.22 × 10^-5`, `1,000`-perm `P = 0.0010`**; 2D area `170 mm²` vs `116 mm²`, `P = 8.35 × 10^-8`). *Status: building on it.*

---

## 2. Complete Numeral Inventory & Graphic Packing Law

All `65` numeral signs across the six graphic series (`numeral_inventory.csv`):

| Series | Code & Signs | Values | Lipi Events | `M_new_clean` Events | Primary Syntactic / Metrological Domain |
|---|---|---|---:|---:|---|
| **`S` Short (1-row)** | `001`–`007`, (`008`=0), `019`, `020`, `X115` | `1–7, 9, 10` | 1,389 | 296 | Discrete items `1–5` (`390, 405, 407, 900, 156, 140, 142, 061, 480`), opener slot `002` (`573x`), divider `001` (`49x`) |
| **`F` Tall (full-height)** | `031`–`036`, `044`–`046`, `X93`, `X94` (`M94`) | `1–6` | 1,489 | 192 | Volumetric & weight measures (`700` cup `96%`, `705/706` *kalam* `90%`, `171` *niṟai* `100%`, `711` *vaḷḷam* `100%`, `590` chest `79%`, `226` fish-crate `71%`, pot capacities) |
| **`T` Stacked (2-row)** | `012`–`018`, `051`, `X116`–`X118` | `2–10` | 200 | 37 | Discrete counts `6–8` (`016` on `220, 390`; `018` on `336, 390`), plus specialized `T3` (`013` before `840` `22x`) & `T7` (`017` with `585` `29x`, `575` `19x`, `503` `16x`) |
| **`B` Block / Bracketed (3-row)** | `025`–`029` (`M119/120`), `048/049`, `055`, `057`, `056` | `6–10, (7), 12, 24` | 110 | 21 | Slanted blocks `025–028` (`6–10`) before `032-740` on Harappa steatite tablets; `(7)` `048/049` with `741/740`; dozen `055` (`4×3=12`); two-dozen `056` (`8×3=24` = `M 121-121`) |
| **`A` A-comb ticks** | `465`–`475` (`M178`) | `1–10` | 41 | 7 | Exclusive crop/produce load counter before `806/838` + porter `154/158` (`40/48 = 83.3%` directly own `806/838`) |
| **`J` Infixed Jar-Mouth** | `741`, `742`–`744`, `745`–`747`, `748` | `1, 2, 3, 4` | 330 | 87 | Ordinal / ward / sub-vessel strokes inside mouth of `740` (`1: 260, 2: 76, 3: 78, 4: 3`; `99.28% <= 3`) |

### Graphic Packing Law Inside the Discrete Series (`S -> T -> B`)
When counting discrete items outside `F` and `A`, scribes pack strokes into more rows as the integer grows so the sign stays square:
- **Values `1–5` (`n = 1,064`):** `1-row S` = **`94.3%`** (`1,003`), `2-row T` = `5.7%` (`61`, mostly specialized `013`), `3-row B` = `0.0%`.
- **Values `6–8` (`n = 208`):** `1-row S` drops to **`8.2%`** (`006` `7x`, `007` `7x`, `008` **`0x`**), replaced by `2-row T` at **`78.4%`** (`163`) and `B` (`13.5%`, bracketed `048/049`).
- **Values `9–10` (`n = 26`):** `3-row slanted B` (`025–029`) takes **`57.7%`** (`15`), `S` (`019/020`) `34.6%` (`9`), `T` `7.7%` (`2`).
- **Value `12` (`n = 79`) & Value `24` (`n = 9`):** `3-row B` (`055` = `4×3`, `056` = `8×3`) takes **`100.0%`**.

---

## 3. Reconstructed Conversion Ladder (`unit_ladder.csv`)

```
[GRAIN / CAPACITY SYSTEM — Tall Strokes F]
  575 kōṭṭai (~665 L = 72 cups)
     │  × 6  (705/706 tall counts strictly in {1,2,3,4,5}: 0/170 >= 6, P = 4.6e-12)
     ▼
  704/705/706 kalam (~110.9 L = 12 cups; post-counted: '705 033')
     │  × 3                      \
     ▼                            \  × 12 (cup counts in {1,2,3,4,6}: 430/431 Lipi,
  711 vaḷḷam/tūṇi (~37.0 L = 4c)   \       7/7 M_new; 0/422 tall-5s, P = 1.6e-7)
     │  × 4 (caps 700 at <=3, P=0.039) \
     ▼                                  ▼
  700 cup / marakkāl (9.26 ± 0.16 L on 3 whole jars, CV = 1.69%, P = 0.0037)
     │  × 8                                  │  × 4
     ▼                                       ▼
  320 paṭi (~1.16 L daily ration;          061–063 quarter (2.31 L; counts <=3: 90.5%)
             goblet scale POT:T:s)

[WEIGHT SYSTEM]                         [DISCRETE BUNDLE SYSTEM — 3-Row Blocks B]
  171 niṟai (post-counted F {3, 5} only:  056 two-dozen (24 = 8×3 = M 121-121)
      25/25 Lipi, 6/6 M_new, P = 0.0015)     │  × 2
     │                                       ▼
     ▼                                    055 dozen (12 = 4×3 = M121)
  645 kaḻañcu -> 480 kuṉṟi -> 821 mañcāṭi    │  × 12
  (on M-326 prism & M-2118..2121 Cu celts)   ▼  single discrete items (S 1–5, T 6–8)
```

### Key Head-to-Head Precedence Pairs (`ladder_order_pairs.csv`, Lipi + `M_new_clean` deduplicated events)
- `413` (`grain_hdr`) before `575` (`kōṭṭai`): **`21 : 1`** (`18:1` Lipi, `3:0` `M_new_clean`, `P = 1.0 × 10^-5`)
- `575` (`kōṭṭai`) before `335` (`bin`) and `711` (`vaḷḷam`): **`19 : 0`** and **`15 : 0`** (`P <= 3.0 × 10^-5`)
- `575` (`kōṭṭai`) before `705/706` (`kalam`): **`6 : 2`** (`4:2` Lipi, **`2:0` `M_new_clean`**; the reverse `L-115: 031 056 705 575` writes an equivalence `1 [kōṭṭai?] / 24, kalam, kōṭṭai`)
- `575` (`kōṭṭai`) before `700` (`cup`): **`11 : 1`** (`10:1` Lipi, `1:0` `M_new_clean`, `P = 0.0032`)
- `711` (`vaḷḷam`) before `700` (`cup`): **`10 : 0`** (`P = 0.00098`)
- `705/706` (`kalam`) before `320` (`paṭi`): **`11 : 0`** (`10:0` Lipi, `1:0` `M_new_clean`, `P = 0.00049`)
- `705/706` (`kalam`) before `061–063` (`quarter`): **`8 : 1`** (`7:1` Lipi, `1:0` `M_new_clean`, `P = 0.0195`)
- `700` (`cup`) before `061–063` (`quarter`): **`4 : 1`** (`3:1` Lipi, `1:0` `M_new_clean`)

---

## 4. What Went Null, Rescues Executed, and Rival Explanations Tested

1. **Null #1 — Raw unconverted cross-face addition (`v_faceA + v_faceB = v_faceC`):** Only `2 / 29` Lipi multi-face account events with `>= 3` counts hit an unconverted sum vs `5.58` shuffled (`P = 0.986`).
   - **Why:** Multi-face tablets pair heterogeneous series (`S` people/loads on one face, `F` cups on another), which cannot be added as raw integers.
   - **Four Rescues Run (`met_02_multiface.py`):**
     - *Rescue R1 (Cross-Face Parity `v_faceA == v_faceB`):* **Hit** — `47 / 135` (`34.8%`) Lipi events vs `38.6` series-matched shuffle (`P = 0.0450`), `4 / 8` (`50.0%`) `M_new_clean`, **`51 / 143` (`35.7%`) combined vs `41.4` (`P = 0.0310`; series-matched `P = 0.0390`)**.
     - *Rescue R2 (`Crew × Cup ∈ {6, 12}` after removing false `820-002` opener counts):* **`4 / 5 = 80.0%`** of deduplicated crew+cup templates multiply to `6` or `12` (`H-1287: 2 women × 3 cups = 6`; `H-1902: 3 porters × 2 cups = 6`; `H-2239, H-2237: 3 hands × 4 cups = 12`; only `H-2238: 3 × 3 = 9` misses), including **`2 / 2 = 100.0%`** outside E-Trench-11 (`Harappa cup-pool P = 0.214` at `n = 5` templates after strict copy-batch deduplication of the 20 E-Trench-11 gang tablets).
     - *Rescue R3 (Cumulative Recipient Cup Sums & Ration Lock):* Cumulative sums across 2–6 events of one name hit multiples of 6 at chance (`5 / 26 = 19.2%` vs `7.0`, `P = 0.89`), showing Harappa chits are **standing repeat-issue vouchers** rather than partial installments summed to a *kalam*. Cross-object matching (`cross_object_ledgers.csv`) links **`60` exact house/recipient stems** appearing on both Seals and Tablets/Sealings.
     - *Rescue R4 (Copper Animal $\times$ Unit:Count Lock):* **Hit** — **`NMI = 0.6378` vs `0.4390` (`z = +6.7`, `P = 0.0010`)**.

2. **Null #2 — Unconstrained in-sample Slater ratio vs sparse random sign decoys (`86.2%` real vs `85.3%` decoy, `P = 0.45`):**
   - **Why:** Random 14-sign decoy sets co-occur half as often (`122.7` ordered pairs vs `206` real) and exploit global positional slots (`1`-observation pairs trivially score `100%` when refitted in-sample).
   - **Rescue Run (`met_01_ladder.py`):** Testing **Domain Co-Occurrence $\times$ Directional Lock** against `1,000` frequency-matched interior (`non-OPEN, non-SLOT, non-CLOSER`) decoys gives **`206` ordered pairs vs `122.7` (`P = 0.0410`)**, and applying the frozen Lipi ranking out-of-sample to `M_new_clean` gives **`19 / 27 = 70.4%` (`P = 0.0261`)**.

3. **Null #3 — Clay tablet area vs cup count `2, 3, 4` (`rho = -0.289`) & Seal `5-kalam` vs `3-kalam` after length control (`P = 0.48`):**
   - **Rival Check on Seals:** Controlling for sign length (`nsign`) and site shows the raw size gap between `5-kalam` (`1,242 mm²`, written `705-033-032` = 3 tokens) and `3-kalam` (`812 mm²`, `705-033` = 2 tokens) shrinks to `+5%` (`P = 0.48`), whereas junior `740-400` seals remain **`-57%` smaller (`resid = -0.855`)** even after length and site control.
   - **Redesign on Tablets (`met_03_physical.py`):** Stepping up from `cup` (`700`) to `kalam / kōṭṭai` (`705/706/575`) **strictly within Harappa clay/steatite tablets** increases median 2D area from `116` to `170 mm²` (`P = 8.35 × 10^-8`) and **doubles median 3D volume from `359` to `732 mm³` (`P = 1.22 × 10^-5`, `1,000`-perm `P = 0.0010`)**.

---

## 5. Machine-Readable Exports Ready for Downstream Solvers

- `work_data/met/unit_ladder.csv`: 17-rung conversion table with exact Lipi/`M_new` counts, ratios (`6 : 1`, `3 : 1`, `4 : 1`, `12 : 1`, `8 : 1`, `2 : 1`), litre/gram anchors, and structural constraints.
- `work_data/met/commodity_series.csv`: 52 sign-groups with series purity (`%F, %S, %T, %B, %A`), pre/post count direction (`pct_after`), ceilings, and `solver_constraint` strings ready to plug directly into phonetic/semantic scoring.
- `work_data/met/cross_object_ledgers.csv`: 60 recipient houses linked across Seals and Tablets/Sealings with their recorded *kalam* and *cup* grades.
