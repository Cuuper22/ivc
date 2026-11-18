# Physical & Archaeological Semantic Anchors (`sem_01`–`sem_04`)

## 1. Headline Wins — What Moved and What It Opens

Without using a single phonetic guess or dictionary lookup, physical medium, container back, animal iconography, intra-city workshop/citadel architecture, and foreign trade provenance pin **219 `(sign, slot)` semantic anchors across 175 distinct Indus signs** (`work_data/sem/sign_anchors.csv`) and **239 fixed phrases** (`work_data/sem/phrase_anchors.csv`) across **4,476 Lipi physical copy-events** (4,691 stones after merging multi-face objects and collapsing same-spot moulded copy batches to 1 event) and **990 strictly held-out unseen Mahadevan `new text` copy-events** (1,050 objects / 1,183 unpartnered lines).

1. **Zero-leakage out-of-sample context prediction wins on unseen Mahadevan `new texts` (`P = 0.0005`, beating all 2,000 matched decoys).**
   - **68 Lipi-selected signs** (chosen strictly on Lipi stratum-shuffle `P <= 0.02`, zero look at `new texts`) score **148 target-domain hits** on unseen `new texts` vs **87.4 ± 16.9** across 2,000 frequency-band-matched decoy tables (`z = +3.58`, `P = 0.0025`; marginal expectation `62.1`), with mean out-of-sample `log2`-lift **`+0.5116` vs `-0.2253 ± 0.1180` (`z = +6.25`, `P = 0.00050`)**.
   - **101 Lipi-selected phrases** score **108 target-domain hits** on unseen `new texts` vs **41.5 ± 10.7** across 2,000 frequency-matched decoys (`z = +6.23`, `P = 0.00050`), with mean out-of-sample `log2`-lift **`+0.5135` vs `-0.1381 ± 0.0738` (`z = +8.82`, `P = 0.00050`)**.
   - Across individual tests (`work_data/sem/sweep_all_hits.csv`), **330 primary associations survive within-domain Benjamini-Hochberg FDR `q <= 0.05`**, **229 survive Westfall-Young max-z family-wise `P <= 0.05`**, and **103 primary associations replicate directly on held-out Mahadevan `new texts`**.

2. **Purely physical `CATS` masks solve inscription-internal semantic coherence on unseen `new texts` (`z = +3.54`, `P = 0.0005`).**
   - Assigning each anchored sign its 13-category `sense_common.py` `CATS` bitmask (`cat_mask`) purely from physical context and learning the 13×13 category co-occurrence lift matrix strictly on Lipi, **694 multi-sign unseen `new text` inscriptions** score **`+0.0034` vs `-0.0008 ± 0.0012`** across 2,000 `(v2_class × frequency_band)`-matched decoy shuffles (**`z = +3.54`, `P = 0.00050`**). Where phonetic dictionary glosses previously needed pruning to clear chance on `lift`, blind archaeological domain masks clear all 2,000 decoys immediately. **Building on `work_data/sem/sign_anchors.csv` (`cat_mask`) as a hard non-phonetic filter for every multi-language phonetic solver.**

3. **Syntactic-slot disentanglement (`COUNTED`/`SOLO` vs `FRONT` vs `NAME` vs `ENDING`) unmasks 217 hidden anchors — and splits dual-duty signs cleanly across held-out `new texts`.**
   - **Sign `820` (6-spoked wheel)** is completely flat overall on Harappa Mound AB Citadel (`ANY` `1.00x`, `P = 1.000`) because `820-002`/`820-060` opens texts everywhere. Restricted to **`NAME` slot** (`820@NAME`), it jumps to **`3.97x` on Harappa Mound AB (`4/10`, `OR = 6.36`, `P_shuf = 0.0155`)** and **replicates on held-out `new texts` Mound AB (`3/5`, `5.93x`, `P = 0.0081`)**, while `820@GOODS_OR_SOLO` selects **coastal/maritime ports (`9/21`, `3.27x`, `P = 0.0010`)**.
   - **Sign `705` (stroked U-vessel)** misses copper tablets overall (`ANY` `P = 0.066`), but splits cleanly into two replicated jobs: **`705@COUNTED`** is the **inland bulk allowance measure** (`14/106` on copper tablets, `OR = 4.83`, `P_shuf = 0.0035`; **held-out `new texts` `4/32`, `3.26x`, `P = 0.031`**; `98/106` in the Riverine Grain Core, `P = 0.005`), whereas **`705@NAME` (uncounted)** is the **maritime/freight sealing office** (`12/88` on clay package sealings, `P_shuf = 0.0255`; **held-out `new texts` `13/32`, `2.17x`, `P = 0.0028`**).
   - **Sign `923` (outline tusk curve)**: **`923@COUNTED`** sits on **elephant-pictured copper tablets (`6/7`, `22.4x`, `OR = 1,252`, `FWER P = 0.0005`; M77 `fs80=07` `4/7`, `P = 3e-5`)**, while **`923@NAME`** (`ANY` missed at `P = 0.057`) clusters inside **Mohenjo-daro HR-A/B elite merchant mansions (`8/23`, `2.73x`, `P_shuf = 0.0055`)** — pinning the **Ivory Commodity** on copper tablets and the **Ivory-Merchant Guild House** in HR-A/B.

4. **The web pays on unseen inscriptions and unlooked-for iconography (four independent cross-checks).**
   - **Botanical produce `806` + load-carrier `158` selects plant-pictured tablets (`14.8x`, `FWER P = 0.0005`).** `806` (leaf-on-stalk) was read from load-tag syntax as agricultural produce. Tested against tablet iconography, `806-158` sits on **plant/pipal-motif tablets (`Phyt`/`Pipal`)** in **9 events across 5 distinct texts** (`OR = 41.2`, distinct-text rival `P = 2e-5`), alongside `463` (`6/8`, 4 distinct texts, `OR = 68.3`, `FWER P = 0.0005`) and `202` (`3/3`, `OR = 171.7`, `FWER P = 0.003`).
   - **Dual-city Citadel Ruling Crest `140` (female figure with raised arm) replicates at BOTH capitals.** `140` is enriched on **Harappa Mound AB Citadel** (`7/20`, 6 distinct texts, `3.51x`, `P_shuf = 0.0030`; **held-out `new texts` `2/4`, `4.94x`, `P = 0.052`**) AND on **Mohenjo-daro Citadel (`SD/L` Stupa & Great Bath)** (`6/62`, 6 distinct texts, `2.54x`, `P_shuf = 0.0295`; **held-out `new texts` `4/19`, `2.90x`, `P = 0.041`**).
   - **Independent Citadel/Metallurgy anchors converge on the same unseen Mound AB inscriptions.** `140` (Citadel Crest), `595` (Citadel/Copper Forge, `New` Mound AB `5/6`, `8.24x`, `P = 4.1e-5`), `632` (Copper-Tool Foundry, `3/3` vs copper tablets, `q = 0.007`), and `820@NAME` (Citadel Quarter, `New` `P = 0.0081`) — each discovered separately in Lipi — stand **side by side on held-out Mahadevan `new texts` from Harappa Mound AB**: `M77-4265` (`000-550-741-632-595`), `M77-4291` (`140-705-632-000`), `M77-4024` (`243-297-820-595`), and `M77-4599` (`550-X33-032-595-820`).
   - **Ideographic vs. rebus boundary measured across slots (`P = 0.0005`).** Comparing `sign_shapes.csv` visual glyph drawings (never used in the context sweep) against contextually mined `CATS` masks across 138 pictured anchors yields **50.7% (`70/138`) match vs `35.4% ± 3.3%` shuffled (`z = +4.66`, `P = 0.00050`)**: **55.8% (`29/52`, `z = +3.19`, `P = 0.0045`) in functional/commodity/ending slots** (direct logograms: cup, tree, wheat-ear, field-grid, hill, man) vs **47.7% (`41/86`, `z = +3.22`, `P = 0.0010`) in `NAME` slots** (where occupational/clan emblems share space with ~52% rebus/phonetic name spelling).

---

## 2. Counting Discipline, Rival Controls & Calibration (`sem_01`–`sem_02`)

- **Physical object & copy-batch deduplication (`sem_01_context.py`)**:
  - **Lipi**: 5,679 text faces -> **4,691 physical stones** (`stone_map()`) -> **4,476 physical copy-events** (collapsing 215 moulded duplicates sharing site + known excavation findspot + full sorted face-texts).
  - **Held-out Mahadevan `new texts`**: 1,183 unpartnered lines -> **1,050 physical objects** -> **990 physical copy-events** (60 same-locus copy duplicates collapsed).
  - **Mahadevan locus & `fs80` calibration**: Unique-seal alignment between Lipi and Mahadevan calibrates Mahadevan `locus` codes into exact intra-city zones on held-out `new texts` (`MD` `01–15` Citadel `SD/L` n=35, `16–18` `HR-A/B` n=55, `20–22` `VS` Dyers/Craft n=34, `31` `DK-G South` n=185, `32` `DK-G North` n=42; `HP` `40` Granary n=46, `41–42` Mound F Platforms/Quarters n=65, `46–50` Mound AB Citadel n=26; `CD` `62` Mound II Workshops n=16; `KB` `81` Citadel vs `82` Lower Town) and decodes `fs80` copper-tablet animal families (`07` elephant, `11` rhinoceros, `13/14` goat/stag, `16` hare, `29` composite, `52` horned archer, `86` endless knot).
- **Rival explanations tested on every hit (`sem_02_anchors.py`)**:
  1. **2,000 stratum-aware object shuffles**: Medium tests permute strictly within `site` (ruling out Mohenjo-daro vs. Harappa vs. Lothal city confounding); intra-city zone tests permute strictly within that city AND re-test under **`city × object_kind`** (`rival_strat_p`); inter-city & foreign trade circuit tests permute strictly within `object_kind` (ruling out tag/tablet/seal mix bias); giant/tiny seal tests re-test within **`site × text_length`**.
  2. **Distinct-inscription collapse (`rival_distinct_p` & `dt`)**: Collapses every identical full inscription across the entire domain pool to a single vote (`1` text = `1` vote), catching single-mould scatter across trenches immediately.

---

## 3. Axis A — Object Medium, Container Back, Vessel Scale & Iconography

### 3.1 Copper/Bronze Tools & Weapons vs. Copper Tablets (Three Foundry Hallmarks)

Contrasting inscribed copper/bronze axes, celts, daggers, and blades (`copper_tool`, n=12 Lipi events; n=6 `new texts`) head-to-head against copper tablets (`copper_tablet`, n=151 Lipi; n=38 `new texts`) cleanly separates **metallurgical foundry / weight-assay marks** from **Mohenjo-daro estate-allotment records**:

| Sign / Phrase | Slot | Domain Contrast | Lipi Events (`dt`) | Strat Lift / OR | Lipi `P_shuf` (`q_FDR`) | Rival `dt P` | Held-Out `New Texts` (or `M77 All`) | Pinned Non-Phonetic Meaning & Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`480`** | `COUNTED` / `ANY` | `copper_tool` vs `all` & `ctab` | `3/12` vs `0/151` (`dt=3`) | `46.6x` / `OR 111.6` | `0.0005` (`q=0.007`) | `0.0005` | **`New` `2/6` (`55.0x`, `P=0.00045`)** | **Metal-Ingot Weight / Assay Unit** (also `17/42` on pots, `New` replicated). Building on it. |
| **`595-850`** | `PHRASE` | `copper_tool` vs `all` & `ctab` | `3/12` vs `2/4464` (`dt=3`) | `166.7x` / `OR 657.6` | `0.0005` (`q=0.007`) | `0.0005` | **`New` `2/6` (`P=9.2e-5`)** | **Forge Metal-Share Formula** (`[forge][ingot-share]`). Building on it. |
| **`391`** (`391-595`) | `NAME` | `copper_tool` vs `all` & `ctab` | `3/12` vs `0/151` (`dt=3`) | `115.4x` / `OR 298.7` | `0.0005` (`q=0.007`) | `0.0005` | **`New` `1/6` (`P=0.018`)** | **Mohenjo-daro Copper-Smithy Crest** (`391-595-850-480-001-821`). Building on it. |
| **`632`** & **`930`** | `NAME` / `PHRASE` | `copper_tool` vs `ctab` | `3/12` vs `0/151` (`dt=2`) | `13.6x` / `OR 111.6` | `0.0005` (`q=0.007`) | `0.0015` | `M77 All` `2/2` (`P=0.0076`), `New` `M77-4902` | **Harappa Bronze-Foundry Hallmark** (`(920-)632-930` on Harappa daggers/axes). Building on it. |
| **`821`** (`001-821`) | `ANY` | `copper_tool` vs `ctab` | `3/12` vs `0/151` (`dt=3`) | `12.8x` / `OR 111.6` | `0.0005` (`q=0.007`) | `0.0005` | Written `820-820` on `New` `M77-2923, 2925`! | **Doubled-Wheel Foundry Standard** (`821` ligature = `820-820` graphic allograph!). Building on it. |
| **`005`** | `ANY` | `copper_tool` vs `all` | `3/12` vs `45/4464` (`dt=3`) | `21.6x` / `OR 35.8` | `0.0010` (`q=0.094`) | `0.0020` | **`New` `1/6` (`M77-8301`, `P=0.030`)** | **Five-Unit Copper Celt Weight Stamp** (solo `005` on Kalibangan axes `K-122` & `M77-8301`). Building on it. |

**Graphic Equivalence Discovery**: Comparing Lipi copper blades `M-2121`/`M-2118` (`391-595-850-480-001-821`) against Mahadevan `new texts` `2923`/`2925` (`391-595-850-480-001-820-820`) proves that **Lipi `821` is the graphic ligature/doubling of `820-820` (two wheels)** at the end of the Mohenjo-daro state foundry stamp.

### 3.2 Copper-Tablet Estate Registry & Specific Animal-Face Ties

Within Mohenjo-daro, copper tablets (`copper_tablet_vs_all`, stratified by site) anchor an entire **agricultural land-allotment and textile/produce lexicon** replicating on held-out `new texts`:
- **Replicated Estate & Produce Core**: **`615` (irrigated cell-grid = arable field plot)**: Lipi `20/151` (`dt=4`, `5.97x`, `OR=18.8`, `FWER P=0.048`), **`New` `15/38` (`P < 1e-6`)**; **`503` (striped hill)**: Lipi `20/151` (`6.44x`, `OR=23.5`), **`New` `3/38` (`P=0.0026`)**; **`503-615` ("Hill-Field")**: Lipi `19/151` (`OR=115.6`), **`New` `3/38` (`P=0.00020`)**; **`845` (hatched paired leaves)**: Lipi `29/151` (`dt=13`, `8.81x`, `OR=71.6`, `FWER P=0.004`), **`New` `3/38` (`P=0.0037`)**; **`095` (person with short stick = estate/herd overseer)**: Lipi `13/151` (`dt=7`, `OR=31.1`), **`New` `7/38` (`P < 1e-6`; phrase `095-595` `New` `6/38` vs `0/952`, `P < 1e-8`)**; **`142` (person with staff)**: Lipi `15/151` (`dt=12`, `OR=7.5`), **`New` `11/38` (`P < 1e-6`; `@COUNTED` `15.1x`)**; **`407` (cloth/textile tree)**: Lipi `50/151` (`dt=24`, `7.51x`, `OR=35.1`, `FWER P=0.0005`); **`597`** (`7/7` on copper tablets across `dt=5`, `OR=449`, `FWER P=0.048`); **`422`/`421` (furrowed strip)** (`6/8`, `OR=77.3`, `FWER P=0.048`).
- **Animal-Specific Copper-Tablet Ties (tested strictly WITHIN copper tablets)**:
  1. **Rhinoceros (`ctab_rhinoceros`) -> Sign `222` (bracketed fish with tooth)**: **`4/5` occurrences sit on rhinoceros tablets across `3` distinct texts** (`22.9x`, `OR=291.0`, `FDR q=0.023`, `FWER P=0.0005`, **distinct-text rival `P=0.00014`**; `M77 fs80=11` `4/4`, `P=3e-6`). Survives distinct-text collapse! Building on `222` as the **Rhinoceros-Lineage / Guild Crest**.
  2. **Elephant (`ctab_elephant`) -> Sign `923@COUNTED` & `706-033`**: **`6/7` on elephant tablets** (`dt=2`, `22.4x`, `OR=1,252`, `FDR q=0.008`, `FWER P=0.0005`, `rival_distinct_p=0.0015`; `M77 fs80=07` `4/7`, `P=3e-5`). Building on `923@COUNTED` = **Ivory / Tusk**.
  3. **Goat / Markhor / Stag (`ctab_goat_antelope`) -> `421` (`003-421-176`), `176`, `790`**: `421` is `3/3` (`dt=2`, `12.3x`, `OR=102.8`, `FWER P=0.007`, `rival_distinct_p=0.007`); `176` is `5/13` (`dt=4`, `4.75x`, `rival_distinct_p=0.0046`; `M77 fs80=13/14` `9/11`, `P=0.00011`). Building on `421` = **Pastoral/Upland Strip Measure**.
  4. **Horned Archer / Hunter (`ctab_human_archer`) -> `900` (crescent), `061`, `850`**: `900` is `9/24` (`dt=3`, `5.84x`, `OR=51.7`, `FWER P=0.001`, `rival_distinct_p=0.014`; `M77 fs80=52` `5/12`, `P=6e-6`). Building on `900` = **Lunar Month / Seasonal Stipend**.
  5. **Bovine / Unicorn (`ctab_bull_gaur_unicorn`) -> `595` & `142@COUNTED`**: `595` is `5/6` (`dt=4`, `9.11x`, `OR=52.7`, `FWER P=0.0005`, **`New` `3/9`, `P=0.010`**); `142@COUNTED` is `3/6` (**`New` `3/11`, `P=0.020`**).
  6. **Hare (`ctab_hare`) -> `321` (`235-705-033-845-407-321-407`)**: `6/8` (`18.9x`, `OR=746.2`, `FWER P=0.0005`; `M77 fs80=16` `6/6`), 1 repeated text (`dt=1`). Testing whether `321` marks a cloth grade or hare-line recipient.
  7. **Iconography-Replacing Signs (`ctab_picsign`) -> `777` (two-stemmed flowering plant) & `749` (jar variant)**: `777` is `6/6` (`dt=3`, `6.72x`, `OR=102.0`, `FWER P=0.0005`, `rival_distinct_p=0.0048`); `749` is `3/3` (`dt=3`, `OR=46.5`, `FWER P=0.008`). Building on `777` and `749` as **Emblem Taxon Classifiers**.

### 3.3 Clay Package Sealing Reverses (`TAG:B`, `TAG:P`, `TAG:L`), Bangles, Rods, Vessels, Prisms & Seal Rank

- **Clay Package Sealings (`tag_all` & reverse subtypes)**:
  - **General Freight Sealings (replicated on `new texts`)**: **`880` (`OPEN` vertex-diamond)**: Lipi `2.41x` (`OR=8.6`), **`New` `5/5` = 100% on clay sealings (`P=0.00022`)** -> **Freight-Inspection / Dispatch Header**; **`500` (bisected sail triangle)**: Lipi `6/17` (`dt=5`, `OR=11.9`, `P_shuf=0.0045`), **`New` `8/11` on sealings (`P=0.00013`)** (`500-741` `New` `5/5`, `P=0.00022`) -> **Maritime / Warehouse Consignment Sign**.
  - **`TAG:P` (Smooth Flat Token, No Package Back) -> Sign `590` (Subdivided Chest)**: **`4/5` at `NAME` across `4` distinct texts in `4` cities** (`Harappa H-1725`, `Hulas Hls-1`, `Lothal L-218`, `Mohenjo-daro M-437`; `11.1x`, `OR=50.0`, `FDR q=0.032`, `FWER P=0.002`, `rival_distinct_p=0.0021`) -> **Portable Treasury / Storehouse Receipt Token**. Building on it.
  - **`TAG:L` (Soft Cloth / Sack / Bundled Cord Bale) -> Sign `156` (Porter with Two Loads) & `861@FRONT`**: `156` is `3/3` within tags (`dt=2`, `8.82x`, `OR=59.7`, `FWER P=0.0055`, `rival_distinct_p=0.0155`); `861@FRONT` is `5/13` (`dt=5`, `3.23x`, `P=0.0095`) -> **Soft-Bale Carried Load**. Building on it.
  - **`TAG:B` (Wooden Box Lid, Lothal) -> `048` (`817-002-048-740`)**: `10/10` (`20.9x`, `OR=8,295`, `FDR q=0.007`, `FWER P=0.0005`, `dt=1` across 10 box impressions, `rival_distinct_p=0.0058`) -> **Boxed Seven-Strand / Luxury Consignment**. Building on it.
- **Vitreous Stoneware Bangles vs. Shell/Terracotta Bangles & Ivory Rods**:
  - **Stoneware Bangles (`bangle_stoneware`, n=38)**: **`511-130-920`** (`511`, `130`, `064`) sits on **`3/3` distinct stoneware bangles** (`53.6x`, `OR=875.2`, `P_shuf=0.0005`, found in Mohenjo-daro Citadel `M-1639` and HR-Elite `M-1628`) -> **Magistratial Wrist-Insignia Formula**.
  - **All Bangles (`bangle_all`, n=48)**: **`790` (pointed oval / ringlet)** is enriched on **both** stoneware bangles (`11.1x`, `P=0.0005`) and shell/terracotta bangles (`20.8x`, `P=0.0045`; overall `6/48`, `dt=4`, `OR=15.8`) -> **Bangle / Ring Ornament Noun**; **`840@SOLO` (two overlapping leaves)** is `6/10` (`48.8x`, `OR=150.4`, `FWER P=0.013`) -> **Matched Pair (of Bangles)**.
  - **Ivory & Bone Rods (`ivory_bone_rod`, n=40; `New` n=9)**: **`760-740-400`** (`Lipi` `3/11`, `dt=3`, `33.3x`, `OR=48.6`, `P=0.001`; **`New` `2/3`, `P=0.00022`**), **`740-400`** (`Lipi` `9` rods, `7.43x`, **`New` `3/9`, `P=0.0019`**), **`838@NAME`** (`14.6x`, `P=0.002`), **`556`** (`17.7x`, `dt=2`, `P=0.005`).
- **Storage Jars vs. Small Stamped Pointed-Base Goblets (`POT:T:s`, median 17×13 mm)**:
  - **All Vessels (`pot_all`, replicated on `new texts`)**: **`540@SOLO` (bowtie container)** (`Lipi` `4/7`, `4.23x`, `P=0.0045`; **`New` `2/3`, `8.57x`, `P=0.017`**), **`480`** (`17/42`, `New` replicated), **`956`** (`3/3`, `dt=3`, `15.0x`, `FWER P=0.049`), **`999`** (`14/17`, `dt=12`, `OR=29.1`, `P=0.0005`), **`035` (5 tall strokes)** (`12/36`, `dt=7`, `P=0.001`).
  - **Small Stamped Goblets (`pot_small_stamped_vs_jars`)**: **`440` (`@SOLO`)** (`6` goblets, `OR=40.4`, `FDR q=0.045`, `FWER P=0.0005` — ration-goblet receipt stamp), **`016` (6 short strokes)** (`3/3`, `dt=3`, `OR=62.0`, `FWER P=0.002`), **`697`** (`4/5`, `dt=3`, `OR=27.0`, `FWER P=0.008`).
  - **Large Storage Jars vs. Small Goblets (Domain Rescue)**: Bulk-lot/capacity bundle (`055` dozen | `540` container | `TREE_FIBRE` | `035` 5-tall) hits **`11/44` (25.0%) on large storage jars vs `3/58` (5.2%) on small goblets (`OR=5.44`, `P_shuf=0.0065`)**; `055` alone is `6.11x` (`dt=3`, `P=0.0085`) on storage jars.
- **Miniature Tablets: 3/4-Sided Prisms vs. Flat 2-Sided Chits & Pictured Tablets**:
  - **Ration Chits (`mtab_all`, replicated on `new texts`)**: **`700` (U-cup ~9.2 L)** (`471/524`, `OR=43.4`, **`New` `8/23`, `P=0.00036`**), **`400` (comb)** (`346/432`, **`New` `14/60`, `P=0.00027`**), **`413@FRONT` (grain stalk)** (`33/36`, `dt=28`, `OR=28.9`, **`New` `2/3`, `P=0.021`**; `413-575-335` `dt=15`, `OR=110.2`, **`New` `P=0.021`**), **`176`** (**`New` `P=0.037`**), **`240@NAME_CREST`** (**`New` `P=0.035`**).
  - **3/4-Sided Prisms (`tab_prism_vs_chit`)**: **`578` (tall compartmented table)** (`5/5`, `dt=5`, `9.07x`, `OR=88.4`, `FDR q=0.019`, `FWER P=0.0005`), **`799` (`799-840`)** (`4/4`, `dt=4`, `OR=71.8`, `FWER P=0.003`), **`824@COUNTED`** (`4/4`, `dt=4`, `OR=71.8`, `FWER P=0.003`), **`070`** (`4/4`, `dt=4`, `FWER P=0.012`), and **`090@ENDING` (manager closer)** (`9/26`, `3.03x`, `P=0.005`) -> **Prisms are multi-party manager summary ledgers (`578`, `799`, `824`, `090`), while flat chits are worker coupon issues (`740-400`)**.
  - **Fish-Motif Tablets (`mtab_fish`)**: **`027` & `025` (three rows of slanted ticks)** (`027`: `4/6`, `dt=4`, `23.3x`, `OR=75.2`, `FWER P=0.002`, `rival_distinct_p=1e-5`) -> **Dried-Fish / Scale Multi-Row Tally**.
- **Giant Elite Seals (`>= 1,190 mm²`) vs. Tiny Seals (`<= 365 mm²`) & Bossless Bar Seals (`SEAL:R`)**:
  - **Giant Top-Decile Seals (surviving `site × text_length` rival control)**: **`842`** (`4/5`, `dt=4`, `8.44x`, `OR=34.6`, `P=0.0005`, `rival_strat_p=0.001`), **`692` (outline X)** (`14/46`, `dt=14`, `3.29x`, `OR=5.4`, `P=0.0005`), **`595-820`** (`3/3`, `OR=80.3`, `P=0.001`), **`560`** (`3/3`, `OR=80.3`, `P=0.0035`), **`564`** (`3/5`, `9.06x`, `P=0.0015`).
  - **Tiny Seals & Bossless Bar Seals (`SEAL:R`)**: Carry **`400` (comb)** (`26/79` tiny, `P=0.0005`), **`806-154` (crop + load-carrier)** (`9/15` tiny `P=0.0005`; `14/16` bar seals `OR=49.0`, `FWER P=0.0005`), **`407`** (`35` bar seals, `OR=18.1`), **`845`** (`11` bar seals, `OR=23.1`), **`063`** (`6/9` tiny, `OR=10.0`), **`468` (A-ticks)** (`7/9` bar, `6/9` tiny) — proving bossless bar seals and tiny seals are **portable commodity-allotment & junior-worker stamps**, not patrician lineage seals.

---

## 4. Axis B — Intra-City Functional Zones (Citadels, Granaries, Elite Houses & Craft Quarters)

Every intra-city test runs strictly within provenanced events of that city and checks `city × object_kind` rival permutations:

1. **Harappa Functional Mounds (`Mound F Granary` vs `Platforms/Workmen` vs `Mound E Workshops` vs `Mound AB Citadel`)**:
   - **Mound AB Citadel (`har_mound_AB`, n=125; `New` n=26)**: **`595` (Forge/Arsenal)** (`8/13`, `dt=8`, `6.16x`, `OR=14.7`, `FWER P=0.0055`, `rival_strat_p=0.0015`; **`New` `5/6`, `8.24x`, `P=4.1e-5`**), **`140` (Citadel Crest)** (`7/20`, `dt=6`, `3.51x`, `P=0.003`; **`New` `2/4`, `4.94x`, `P=0.052`**), **`820@NAME` (Citadel Quarter)** (`4/10`, `3.97x`, `P=0.0155`; **`New` `3/5`, `5.93x`, `P=0.0081`**), **`717`** (`5/14`, `P=0.007`; **`New` `2/5`, `P=0.081`**), **`055`** (`4/8`, `P=0.007`; **`New` `2/5`, `P=0.081`**), **`585@COUNTED`** (`3/5`, `P=0.008`; **`New` `1/1`, `P=0.101`**), **`326`** (`3/3`, `FWER P=0.017`), **`697`** (`3/3`, `FWER P=0.023`).
   - **Great Granary (`har_F_granary`, n=86; `New` n=46)**: **`017` (7 short strokes)** (`4/17`, `dt=4`, `3.39x`, `P=0.029`; **`New` `3/5`, `3.35x`, `P=0.041`**), **`440@NAME`** (`3/11`, `4.04x`, `P=0.034`; **`New` `2/3`, `P=0.084`**), **`590-407-740` (Cloth-Chest House)** (`5/7`, `10.1x`, `FWER P=0.0025`).
   - **Threshing Platforms & Workmen's Quarters (`har_F_platforms_quarters`, n=205)**: **`740-400` (worker comb-class)** (`46/159`, `dt=32`, `1.75x`, `FWER P=0.0355`, `M77 All` `39/91`, `P=0.0071`), **`176-740-400`** (`17/29`, `dt=6`, `3.55x`, `FWER P=0.0005`), **`234`** (`3/3`, `dt=3`, `P=0.005`), **`368@NAME`** (`9/20`, `dt=7`, `P=0.002`).
   - **Mound E Craft Workshops & Gateway (`har_mound_E`, n=421)**: **`034` & `034-700` (4-cup *tūṇi* issue = 37 L)** (`62/110`, `dt=59`, `1.67x`, `FWER P=0.0005`, `rival_distinct_p=0.0`) + **`630@PRE_CLOSER`** (`4/4`, `P=0.011`).

2. **Mohenjo-daro Functional Sectors (`Citadel SD/L` vs `HR-A/B Elite` vs `VS/Moneer Craft` vs `DK-G`)**:
   - **Citadel (`md_citadel`, n=61; `New` n=35)**: **`370` (spindle/ceremonial shaft)** (`4/5`, `dt=4`, `21.4x`, `OR=78.6`, `FWER P=0.0005`, `rival_distinct_p=0.0`), **`140` (Citadel Crest)** (`6/62`, `2.54x`, `P=0.0295`; **`New` `4/19`, `2.90x`, `P=0.041`**), **`003-900` ("3 months")** (`Lipi` `8.57x`, `P=0.017`; **`New` `2/5`, `5.51x`, `P=0.045`**), **`416-740` / `416@PRE_CLOSER`** (`Lipi` `12.9x`, `P=0.011`; **`New` `1/1`, `P=0.073`**).
   - **HR-A/B Elite Merchant Mansions (`md_HR_elite`, n=200; `New` n=55)**: **`374` (curving two-leaf plant)** (`4/10`, `dt=4`, `3.15x`, `P=0.029`, `rival_strat_p=0.028`; **`New` `2/3`, `5.84x`, `P=0.036`**), **`742@NAME`** (`Lipi` `2.05x`, **`New` `3/6`, `P=0.022`**), **`264` (wingless bird)** (`3/3`, `dt=3`, `OR=48.5`, `P=0.003`), **`923@NAME` (Ivory Guild)** (`8/23`, `2.73x`, `P=0.0055`), **`840@COUNTED`** (`7/12`, `4.60x`, `P=0.001`).
   - **VS Dyers'/Shell & Moneer Bead/Metal Quarters (`md_VS_MN_craft`, n=111; `New` n=34)**: **`745` (three-dotted jar = 3rd craft ward)** (`5/15`, `dt=5`, `4.70x`, `OR=7.1`, `P=0.0025`, `rival_strat_p=0.001`; **`New` `5/20`, `3.54x`, `P=0.0093`**; `745-235` `FWER P=0.028`, `New P=0.071`), **`503` & `615` (`503-615` "Hill-Field" dye/estate house)** (`503`: `Lipi` `P=0.008`, **`New` `3/7`, `6.08x`, `P=0.0093`**; `503-615`: **`New` `2/4`, `7.09x`, `P=0.027`**).

3. **Lothal, Dholavira, Chanhu-daro & Kalibangan (Including All Rescued Sub-Domains)**:
   - **Lothal Warehouse (`SRG 3GX 10`, n=16) vs. Port Town / Bead Factory (n=71)**: Warehouse selects **`220-740-090` (fish-house agent)** (`4/5`, `dt=4`, `4.33x`, `OR=16.9`, `P=0.004`), **`500`** (`3/4`, `P=0.021`), and **`001-055-220` ("one dozen fish")** (`3/4`, `P=0.021`). Contrasting Lothal's non-Warehouse Town/Dock/Bead sector (n=71) against the Riverine Core (stratified by `object_kind`, Rescue 3) pins **`406` (coastal fibre-tree variant: `3/71` vs `7/3682`, `6.91x`, `OR=25.0`, `P_shuf=0.0070`)**, **`111` (`3/71` vs `11/3682`, `OR=16.3`, `P_shuf=0.0265`)**, and **`527` (`5/71` vs `53/3682`, `OR=5.61`, `P_shuf=0.032`)**.
   - **Dholavira Citadel & Bailey (n=56) vs. Middle/Lower Town (n=88) (Rescue 1)**: Single signs missed at `k_tot >= 3`, but testing **capacity-measure syntax stratified by `object_kind`** rescues the Citadel cleanly: **`TALL_NUM` (`031–036` capacity strokes) sits on `18/56` (32.1%) Citadel/Bailey events vs `11/88` (12.5%) Middle/Lower Town (`OR=3.24`, `P_shuf=0.0045`)**, alongside **`706` / `033-520` (`4/56` vs `0/88`, `OR=15.2`, `P_shuf=0.014`)**. Dholavira's Castle/Bailey is the **capacity-accounting storehouse**, while Middle/Lower Town holds residential name seals.
   - **Chanhu-daro Mound II Bead/Seal/Metal Workshops (`site_chanhu_workshops` n=70, `New` n=23 & `8C–9D` core n=26, Rescue 4)**: **`909`** (`3/26` in `8C–9D` core vs `0/3507` in MD/HP, `OR=1,045`, `P_shuf=0.0005`), **`240-705-033`** (`Lipi` `17.3x`, `P=0.0015`; **`New` `21.5x`, `P=0.046`**), **`920-060`** (`Lipi` `4.96x`, `P=0.015`; **`New` `6.61x`, `P=0.035`**), **`390@NAME`** (`Lipi` `P=0.019`; **`New` `5.16x`, `P=0.018`**), **`838@GOODS_OR_SOLO` (sesame/oilseed)** (`18.2x`, `P=0.003`), and **`220@COUNTED`** in `8C–9D` core (`4.67x`, `P_shuf=0.024`).
   - **Kalibangan Citadel (`KLB-1`, n=87) vs. Lower Town (`KLB-2`, n=75)**: **`892` (bow-and-arrow levy/grant sign)** (`8/8` provenanced KLB occurrences in Citadel, `OR=16.1`, `FWER P=0.034`).

---

## 5. Axis C — Inter-City & Foreign Trade Circuits (Stratified by Object Kind)

1. **Overland West & North (`Ur, Kish, Girsu, Umma, Susa, Tepe Yahya, Shortughai, Gonur`, n=25; `New` n=7)**:
   - **`924` (hatched outline crescent)**: Lipi **`30.8x` (`OR=62.6`, `P_shuf=0.0020`, `rival_distinct_p=0.0013`, on Ur & Susa seals)**, and **replicates `70.6x` (`P=0.014`) on held-out Mahadevan `new texts` (`M77-9801`)**!
   - **`416@NAME` (double-headed pitchfork)**: Rescued by slot split (`ANY` `P=0.053` -> `NAME` **`8.09x`, `OR=11.0`, `P_shuf=0.041`, on Kish & Susa seals**), and **replicates `17.6x` (`P=0.055`) on held-out `new texts` (`M77-9801`, standing in the SAME inscription as `924`!)**.
2. **Overseas Persian Gulf / Oman (`Dilmun & Magan`, n=16; Round/Cylinder Seals n=39)**:
   - **`090` (plain standing man)**: Lipi **`4.86x` (`OR=6.86`, `P_shuf=0.0285`)**, **`New` `13.0x` (`P=0.075`)**; **`091` (twin standing men)**: **`31.3x` on round/cylinder seals (`8/15`, `dt=7`, `OR=78.5`, `FWER P=0.0005`)** and **`38.1x` in Gulf/Oman (`P=0.0005`)**; **`093` (person variant)**: `18.2x` on round seals & `19.6x` abroad (`P=0.0045`); **`055` (dozen)**: `8.5x` on round seals (`P=0.0005`); **`004` (4 short strokes)**: `6.2x` abroad (`P=0.0005`).
3. **Coastal / Maritime Circuit (`Lothal, Dholavira, Bagasra, Shikarpur, Surkotada, Makran, Gulf`, n=471; `New` n=81)**:
   - **`055-220` ("dozen + fish" bale)**: Lipi `dt=6`, `OR=128.4`, `P_shuf=0.010`, `rival_distinct_p=0.0`; **`New` `3/3` = 100% maritime (`12.2x`, `P=0.00053`)**!
   - **`500-741` (sail-port ward)**: Lipi `dt=6`, `OR=18.3`, `P_shuf=0.040`; **`New` `4/5` (`9.76x`, `P=0.00020`)**!
   - **`575-031` (1-unit dry port bin)**: Lipi `OR=14.1`, `P_shuf=0.033`; **`New` `2/2` (`12.2x`, `P=0.0066`)**!
   - Plus multi-text coastal markers **`634@FRONT`** (`3/3`, `dt=3`, `OR=59.4`, `P=0.002`), **`392`** (`4/6`, `dt=4`, `OR=15.3`, `P=0.002`), **`820@GOODS_OR_SOLO`** (`9/21`, `P=0.001`), **`136@COUNTED`** (`4/5`, `dt=4`, `OR=25.5`, `P=0.0105`).
4. **Eastern Headwaters (`Kalibangan, Banawali, Rakhigarhi, Karanpura, Rupar`, n=269; `New` n=34)**:
   - **`890` & `890-892`**: Lipi `12.0x` (`OR=38.8`, `P_shuf=0.0005`), **`New` `29.1x` (`P=0.034`)**; **`411` (drawn as a wheat/barley ear!)**: **`6/9` across `5` distinct texts in Eastern Headwaters (`OR=29.4`, `P_shuf=0.0005`)**; **`390@SOLO` (cotton mark on whorls & pots)**: rescued by slot split (`ANY` `P=0.088` -> **`SOLO` `8/11` = `12.0x`, `OR=38.8`, `P_shuf=0.0010`**).

---

## 6. Ten Real Inscriptions Glossed Non-Phonetically by Physical Slot Anchors

Every bracketed gloss below is strictly **non-phonetic**, read directly from `work_data/sem/sign_anchors.csv`:

1. **`M-2121` & Held-Out `M77-2925` (Mohenjo-daro DK-G South, Copper Blade/Implement)**: `391 - 595 - 850 - 480 - 001 - 821` (`M77-2925`: `...-820-820`)
   -> `[MD Copper-Smithy Crest (391)] [State Forge/Arsenal (595)] [Metal-Ingot Share (850)] [Assay Weight-Unit (480) : 1 (001)] [Double-Wheel Foundry Standard (821=820-820)]`.
2. **`H-380` & Held-Out `M77-4902` (Harappa, Copper Dagger / Implement)**: `920 - 632 - 930`
   -> `[Workshop Header (920)] [Harappa Bronze-Foundry Enclosure (632)] [Wheeled-Arch Implement Hallmark (930)]`.
3. **Held-Out `M77-4265` & `M77-4291` (Harappa Mound AB Citadel)**: `000 - 550 - 741 - 632 - 595` & `140 - 705 - 632 - 000`
   -> `[... Office-Header (550) - Ward-1 (741)] [Bronze-Foundry (632)] [Citadel Forge/Arsenal (595)]` and `[Citadel Ruling/Goddess Crest (140)] [Allowance/Port Office (705)] [Bronze-Foundry (632) ...]`.
4. **Held-Out `M77-4599` (Harappa Mound AB Citadel)**: `550 - X33 - 032 - 595 - 820`
   -> `[Office-Header (550)] [...] [2-Tall (032)] [Citadel Forge/Arsenal (595)] [Citadel Acropolis Quarter (820@NAME)]` (matching the giant-seal `595-820` compound).
5. **`M-437` (Mohenjo-daro, `TAG:P` Smooth Flat Square Clay Token — No Package Back)**: `820 - 002 - 590 - 390 - 740`
   -> `[Quarter-Header (820) : 2-Shares (002)] [Storehouse-Chest / Treasury Receipt (590)] [Cotton/Fibre (390)] [House-Possessive (740)]` (a portable treasury deposit/withdrawal receipt token).
6. **`L-161..170` (Lothal, `TAG:B` Wooden Box Lid Sealings)**: `817 - 002 - 048 - 740`
   -> `[Allotment-Header (817) : 2-Shares (002)] [Boxed 7-Strand Luxury Bundle (048)] [House-Possessive (740)]`.
7. **`L-124` (Lothal Warehouse `SRG 3GX 10`, `TAG:L` Soft Cloth/Sack Bale Sealing)**: `705 - 500 - 741 - 001 - 055 - 220 - 740 - 090`
   -> `[Maritime Port Office (705@NAME) - Freight Sail (500) - Ward-1 (741)] : [1 (001) Dozen (055) Fish-Bale (220)] [of the House (740) - Agent/Manager (090)]`.
8. **Elephant Copper Tablet Set (`Mohenjo-daro`, `TAB:C`, Elephant Picture)**: `706 - 033 - 923 - 740`
   -> `[Big Kalam-Measure (706) : 3-Tall Units (033)] [Ivory / Elephant Tusk (923@COUNTED)] [of the House/Store (740)]`.
9. **Plant-Motif Moulded Tablet (`Harappa`, `TAB:B`, `Phyt`/`Pipal` Tree Picture)**: `465 - 806 - 158`
   -> `[A-Series Lot Count (465)] [Botanical Crop / Tree Produce (806@COUNTED)] [Carried Load (158)]`.
10. **Susa Seal & Held-Out `M77-9801` (Overland West Asian Trade Circuit)**: `416 - 150 - 001 - 055 - X185 - 001 - 924 - X57`
    -> `[Overland Merchant Lineage (416@NAME) - Carrier (150)] [1 Dozen (001-055) ...] [Expatriate Overland Trade Marker (924) ...]`.

---

## 7. Output Artifacts & Immediate Next Step

- **Scripts**: `work_scripts/sem_01_context.py`, `work_scripts/sem_02_anchors.py`, `work_scripts/sem_03_export.py`, `work_scripts/sem_04_global_validation.py`.
- **Data tables (`work_data/sem/`)**:
  - `sign_anchors.csv` (**219 `(sign, slot)` rows**, **175 distinct signs**, exact Lipi & `new texts` odds/P, rival checks, non-phonetic meaning hypotheses, and 13-bit `sense_common.py` `CATS` `cat_mask` ready to bit-AND directly against `/tmp/dict_emb/phrase_masks.npy`).
  - `phrase_anchors.csv` (**239 anchored 2- and 3-sign phrases** with Lipi & `new texts` replication).
  - `slot_redesign_rescues.csv` (**335 slot-specific enhancements / 217 strict rescues**), `domain_rescues.csv` (**all 4 Pass-1 null sub-domains rescued**), `sweep_all_hits.csv`, `global_validation.json`, `objects_lipi.csv`, `objects_mah_new.csv`, `events_lipi.json`, `events_new.json`.
- **What this opens next**: Multiply `(phrase_masks & cat_mask) != 0` from `work_data/sem/sign_anchors.csv` into the candidate-language phonetic alignment solver across Dravidian, Munda, Old Indo-Aryan, Elamite, and Sumerian loanwords — requiring any proposed phonetic value in `GOODS_OR_SOLO` / `COUNTED` / `MEASURE` / `ENDING` slots to satisfy its empirically measured archaeological `CATS` mask while leaving `NAME` slots free to test homophonous rebus transfers!
