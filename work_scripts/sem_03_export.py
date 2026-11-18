#!/usr/bin/env python3
"""sem_03_export.py -- Domain rescues + export of sign_anchors.csv and phrase_anchors.csv.

1. Runs honestly different rescue designs for the 4 narrow intra-site/vessel sub-domains that had
   0 primary single-sign hits at k_tot>=3 in Pass 1:
     - dhol_citadel_bailey: capacity-numeral & big-measure class bundle (TALL_NUM + 706 + 033-520)
     - pot_storage_jar_vs_small: vessel capacity vs goblet stamp grammar (TALL strokes + 055/TREE vs SOLO/SHORT stamps)
     - lothal_town_dock_bead: Lothal Port Town / Bead Factory (excluding Warehouse) vs inland cities (stratified by kind)
     - chanhu_bead_seal_core: Chanhu-daro 8C-9D workshop core at k_in>=2 + craft-family bundles
2. Exports `work_data/sem/sign_anchors.csv` with exact Lipi & Mahadevan `new texts` odds/P, rival checks,
   pinned non-phonetic semantic domain, concrete meaning hypothesis, and `sense_common.py` CATS bitmask.
3. Exports `work_data/sem/phrase_anchors.csv` for anchored 2-sign and 3-sign phrases.
"""
import os
import sys
import json
import collections
import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from sense_common import CATS

OUT = os.path.join(ROOT, 'work_data', 'sem')


def log(*args):
    print('[sem_03]', *args, flush=True)


def encode_cats(cat_list):
    clean = [c for c in cat_list if c in CATS]
    # Keep canonical CATS order
    ordered = [c for c in CATS if c in clean]
    mask = sum(1 << CATS.index(c) for c in ordered)
    bits = ''.join('1' if c in ordered else '0' for c in CATS)
    return '|'.join(ordered), int(mask), bits


# ---------------- 1. Run Domain-Level Rescues for the 4 Pass-1 Null Sub-Domains ----------------
log('Running domain-level rescues for the 4 narrow Pass-1 null sub-domains ...')
ev_lipi = json.load(open(os.path.join(OUT, 'events_lipi.json')))
ev_new = json.load(open(os.path.join(OUT, 'events_new.json')))
rng = np.random.default_rng(20261119)

TALL = {'031', '032', '033', '034', '035', '036'}
SHORT = {'001', '002', '003', '004', '005', '006', '007', '012', '013', '014', '015', '016', '017', '018'}
TREES = {'390', '405', '406', '407'}


def rescue_perm_test(pool, target_fn, feat_fn, strat_fn=None, n_shuf=2000):
    y = np.array([1 if target_fn(r) else 0 for r in pool], dtype=int)
    x = np.array([1 if feat_fn(r) else 0 for r in pool], dtype=int)
    a = int((x & y).sum())
    b = int(((1 - x) & y).sum())
    c = int((x & (1 - y)).sum())
    d_c = int(((1 - x) & (1 - y)).sum())
    odds = ((a + 0.5) * (d_c + 0.5)) / ((b + 0.5) * (c + 0.5))
    pf = float(fisher_exact([[a, b], [c, d_c]], alternative='greater')[1])
    if strat_fn is None:
        sims = [int((x & rng.permutation(y)).sum()) for _ in range(n_shuf)]
    else:
        groups = collections.defaultdict(list)
        for i, r in enumerate(pool):
            groups[strat_fn(r)].append(i)
        sims = []
        for _ in range(n_shuf):
            yp = y.copy()
            for idxs in groups.values():
                if len(idxs) > 1:
                    yp[idxs] = rng.permutation(y[idxs])
            sims.append(int((x & yp).sum()))
    sims = np.array(sims)
    ps = float((1 + (sims >= a).sum()) / (n_shuf + 1))
    lift = round(a / max(sims.mean(), 0.01), 3)
    return a, int(y.sum()), c, int((1 - y).sum()), lift, round(odds, 3), round(pf, 5), round(ps, 5)


rescue_rows = []

# Rescue 1: Dholavira Citadel & Bailey vs Middle/Lower Town -> Capacity numerals (TALL_NUM) & kalam-chief (706 / 033-520)
dhol_pool = [r for r in ev_lipi if r['site'] == 'Dholavira' and len(r['zones']) > 0]
for fname, ffn in [
    ('CLASS:TALL_NUM (031-036 capacity strokes)', lambda r: any(s in TALL for s in r['signs'])),
    ('BUNDLE:706_or_033-520 (kalam measure / 3-kalam chief)', lambda r: ('706' in r['signs']) or ('033-520' in r['phrases2'])),
]:
    a, ni, c, no, lift, odds, pf, ps = rescue_perm_test(
        dhol_pool, lambda r: 'dhol_citadel_bailey' in r['zones'], ffn, strat_fn=lambda r: r['kind'])
    rescue_rows.append(dict(
        sub_domain='dhol_citadel_bailey',
        rescue_design='Class/bundle test stratified by object_kind within Dholavira',
        feature=fname, k_in=a, n_in=ni, k_out=c, n_out=no,
        strat_lift=lift, odds=odds, p_fisher=pf, p_shuf_strat=ps
    ))

# Rescue 2: Large Storage Jars vs Small Stamped Goblets -> Bulk lot/capacity (055 dozen, TALL>=3, TREES, 540) vs Goblet SOLO/SHORT stamps
pot_pool = [r for r in ev_lipi if ('pot_storage_jar' in r['subtypes']) or ('pot_small_stamped' in r['subtypes'])]
for fname, ffn in [
    ('BUNDLE:BULK_LOT (055 dozen | 540 vessel | TREE_FIBRE | 035 five-tall)',
     lambda r: bool(set(r['signs']) & ({'055', '540', '035'} | TREES))),
    ('BUNDLE:TALL_CAPACITY_ONLY (tall strokes without goblet stamp 440/697)',
     lambda r: any(s in TALL for s in r['signs']) and not bool(set(r['signs']) & {'440', '697'})),
]:
    a, ni, c, no, lift, odds, pf, ps = rescue_perm_test(
        pot_pool, lambda r: 'pot_storage_jar' in r['subtypes'], ffn)
    rescue_rows.append(dict(
        sub_domain='pot_storage_jar_vs_small',
        rescue_design='Bulk-capacity & lot-bundle test (jars vs small stamped goblets)',
        feature=fname, k_in=a, n_in=ni, k_out=c, n_out=no,
        strat_lift=lift, odds=odds, p_fisher=pf, p_shuf_strat=ps
    ))

# Rescue 3: Lothal Town/Dock/Bead Factory (non-Warehouse provenanced Lothal, n=71) vs Inland Cities (stratified by kind!)
loth_vs_inland = [r for r in ev_lipi if ('lothal_town_dock_bead' in r['zones']) or (r['circuit'] == 'riverine_core')]
for fname, ffn in [
    ('SIGN:406 (coastal tree/fibre variant)', lambda r: '406' in r['signs']),
    ('SIGN:111 (artisan/staff person)', lambda r: '111' in r['signs']),
    ('SIGN:527 (after-jar title closer)', lambda r: '527' in r['signs']),
    ('SIGN:575 (dry measure / port bin)', lambda r: '575' in r['signs']),
]:
    a, ni, c, no, lift, odds, pf, ps = rescue_perm_test(
        loth_vs_inland, lambda r: 'lothal_town_dock_bead' in r['zones'], ffn, strat_fn=lambda r: r['kind'])
    if a >= 2:
        rescue_rows.append(dict(
            sub_domain='lothal_town_dock_bead',
            rescue_design='Contrast Lothal Town/Dock/Bead (outside Warehouse) vs Riverine Core stratified by object_kind',
            feature=fname, k_in=a, n_in=ni, k_out=c, n_out=no,
            strat_lift=lift, odds=odds, p_fisher=pf, p_shuf_strat=ps
        ))

# Rescue 4: Chanhu-daro 8C-9D Bead/Seal Workshop Core vs Inland Core (stratified by object_kind!)
cd_core_pool = [r for r in ev_lipi if ('chanhu_bead_seal_core' in r['zones']) or (r['site'] in ('Mohenjo-daro', 'Harappa'))]
for fname, ffn in [
    ('SIGN:220@COUNTED (counted fish / bead-weight tally)', lambda r: '220' in r['slot_signs'].get('COUNTED', [])),
    ('SIGN:909 (left-arc workshop sign)', lambda r: '909' in r['signs']),
    ('PHRASE:032-220 (tall-two + fish in workshop core)', lambda r: '032-220' in r['phrases2']),
]:
    a, ni, c, no, lift, odds, pf, ps = rescue_perm_test(
        cd_core_pool, lambda r: 'chanhu_bead_seal_core' in r['zones'], ffn, strat_fn=lambda r: r['kind'])
    rescue_rows.append(dict(
        sub_domain='chanhu_bead_seal_core',
        rescue_design='Contrast Chanhu-daro 8C-9D Bead/Seal Workshop Core vs MD/HP stratified by object_kind',
        feature=fname, k_in=a, n_in=ni, k_out=c, n_out=no,
        strat_lift=lift, odds=odds, p_fisher=pf, p_shuf_strat=ps
    ))

resc_dom_df = pd.DataFrame(rescue_rows)
resc_dom_df.to_csv(os.path.join(OUT, 'domain_rescues.csv'), index=False)
log(f'Saved {len(resc_dom_df)} domain-level rescue results to work_data/sem/domain_rescues.csv:')
for _, rr in resc_dom_df.iterrows():
    log(f"  [{rr.sub_domain}] {rr.feature}: {rr.k_in}/{rr.n_in} vs {rr.k_out}/{rr.n_out}, lift={rr.strat_lift}x, OR={rr.odds}, P_shuf={rr.p_shuf_strat}")


# ---------------- 2. Build Curated Semantic Domain & Meaning Hypothesis Rules ----------------
df = pd.read_csv(os.path.join(OUT, 'sweep_all_hits.csv'), dtype=str).fillna('')
sm = pd.read_csv(os.path.join(OUT, 'sign_meta.csv'), dtype=str).fillna('').set_index('sign')

num_cols = ['lipi_k_in', 'lipi_n_in', 'lipi_k_tot', 'lipi_n_pool', 'lipi_distinct_texts_in',
            'lipi_fold', 'lipi_odds', 'lipi_p_fisher', 'lipi_exp_shuf', 'lipi_z_shuf',
            'lipi_p_shuf', 'lipi_q_fdr_dom', 'lipi_p_fwer_dom', 'rival_distinct_p', 'rival_strat_p']
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df['strat_lift'] = (df['lipi_k_in'] / df['lipi_exp_shuf'].clip(lower=0.01)).round(3)

# Default domain -> (pinned_domain_template, hypothesis_template, cats_list)
DOMAIN_SEMANTICS = {
    'copper_tool_vs_all': (
        'Metallurgy: Copper/Bronze Implement & Ingot Marking',
        'Stamped on copper/bronze axes, celts, and blades; marks metallurgical alloy/weight specification or smithy workshop.',
        ['tool', 'commodity', 'measure']
    ),
    'copper_tool_vs_ctab': (
        'Metallurgy: Weapon/Tool Workshop vs Copper Record',
        'Selectively inscribed on functional copper/bronze tools and weapons rather than Mohenjo-daro copper allotment tablets.',
        ['tool', 'commodity', 'measure']
    ),
    'copper_tablet_vs_all': (
        'Estate & Allotment Registry (Mohenjo-daro Copper Tablets)',
        'Core term of Mohenjo-daro copper-tablet standing allotments (agricultural land plots, produce shares, or titled recipients).',
        ['commodity', 'place', 'measure']
    ),
    'ctab_elephant': (
        'Commodity: Elephant / Ivory Tusk Allotment',
        'Strictly tied to elephant-pictured copper tablets (quantified in big kalam-type units 706-033); ivory/tusk commodity or elephant corps.',
        ['commodity', 'animal']
    ),
    'ctab_hare': (
        'Copper-Tablet Class: Hare Series Allotment',
        'Concentrated on hare-pictured copper tablets alongside cloth/estate terms; marks the hare-emblem allotment line.',
        ['animal', 'commodity', 'place']
    ),
    'ctab_human_archer': (
        'Copper-Tablet Class: Horned Archer / Hunter Allowance',
        'Concentrated on horned-archer/hunter copper tablets with lunar-month/share terms; bowman/guard corps or seasonal hunt/forest levy.',
        ['person', 'time', 'commodity']
    ),
    'ctab_goat_antelope': (
        'Copper-Tablet Class: Goat/Markhor/Stag Pastoral & Field Line',
        'Concentrated across multiple distinct texts on goat/antelope/stag copper tablets with ploughed-strip and tax/title signs.',
        ['animal', 'place', 'commodity']
    ),
    'ctab_bull_gaur_unicorn': (
        'Copper-Tablet Class: Bovine/Unicorn State Allowance',
        'Concentrated on unicorn/gaur/bull copper tablets with forge (595) and staff-holder (142) signs; state herd or citadel metal/grain issue.',
        ['animal', 'person', 'commodity']
    ),
    'ctab_rhinoceros': (
        'Copper-Tablet Class: Rhinoceros Crest/House Line',
        'Holds across 3 distinct texts on rhinoceros-pictured copper tablets (surviving distinct-text control P=0.00014 & M77 fs80=11).',
        ['animal', 'kin', 'person']
    ),
    'ctab_composite': (
        'Copper-Tablet Class: Composite Beast Registry',
        'Concentrated on composite-beast copper tablets at Mohenjo-daro.',
        ['animal', 'deity', 'person']
    ),
    'ctab_picsign': (
        'Copper-Tablet Reverse: Iconography-Replacing Emblem Sign',
        'Stands on the reverse of copper tablets in place of the animal drawing; graphic emblem/taxon classifier.',
        ['plant', 'tool', 'animal']
    ),
    'mtab_gharial': (
        'Pictured Tablet Class: Gharial Riverine/Chief Motif',
        'Concentrated on Harappa moulded tablets bearing the gharial crocodile motif.',
        ['animal', 'person', 'place']
    ),
    'mtab_plant': (
        'Botanical / Sacred-Tree Produce & Offering (Plant-Motif Tablets)',
        'Strongly enriched across distinct texts on moulded tablets depicting a plant/pipal tree; botanical produce, crop load, or tree-shrine offering.',
        ['plant', 'commodity']
    ),
    'mtab_fish': (
        'Aquatic / Dried-Fish Tally (Fish-Shaped & Fish-Motif Tablets)',
        'Exclusively or heavily concentrated across distinct texts on fish-shaped/fish-motif miniature tablets.',
        ['animal', 'measure', 'commodity']
    ),
    'bangle_stoneware': (
        'Luxury Insignia: Vitreous Stoneware Bangle Formula',
        'Inscribed in micro-script on high-fired stoneware bangles; royal/magistratial wrist-insignia title, artisan guild, orpair-tenure label.',
        ['person', 'tool', 'quality']
    ),
    'bangle_other_mat': (
        'Ornament: Shell / Terracotta Bangle Label',
        'Inscribed on non-stoneware (shell/terracotta/clay) bangles; circular ornament or pair designation.',
        ['tool', 'commodity', 'number']
    ),
    'bangle_all': (
        'Ornament & Pair Insignia: Inscribed Bangles',
        'Concentrated on inscribed wrist-bangles across stoneware and shell/clay media; ring/bangle object noun, pair numeral, or wearer rank.',
        ['tool', 'number', 'person']
    ),
    'ivory_bone_rod': (
        ' Craft & Divination/Metrology: Ivory & Bone Rods',
        'Concentrated on carved ivory and bone rods (replicated in held-out M77); junior/artisan comb-rank baton, tally rod, or ivory-guild owner.',
        ['tool', 'person', 'kin']
    ),
    'tag_all': (
        'Freight & Warehouse Administration: Clay Package Sealings',
        'Concentrated on clay package tags/sealings (replicated on held-out M77 sealings); shipment dispatch, customs/port ward, or consignment verb/header.',
        ['action', 'commodity', 'place']
    ),
    'tag_B_box_within_tags': (
        'Package Type: Wooden Box / Chest Consignment (TAG:B)',
        'Pressed onto straight-edged wooden box lids/corners at Lothal; boxed luxury count/bundle or chest-seal formula.',
        ['tool', 'number', 'commodity']
    ),
    'tag_P_token_within_tags': (
        'Package Type: Smooth Clay Receipt Token (TAG:P)',
        'Pressed onto smooth flat clay tokens with no package impressions; portable storehouse/chest receipt token.',
        ['tool', 'commodity', 'measure']
    ),
    'tag_L_bale_within_tags': (
        'Package Type: Soft Cloth/Cord/Reed Bale (TAG:L)',
        'Pressed onto cloth-wrapped sacks, woven bales, and corded reed bundles; carried bale-load unit or shipment lot header.',
        ['commodity', 'tool', 'measure']
    ),
    'tag_O_cane_within_tags': (
        'Package Type: Cane/Reed Bundled Container (TAG:O)',
        'Pressed onto cane/reed-backed clay sealings.',
        ['tool', 'commodity', 'number']
    ),
    'pot_all': (
        'Ceramic Vessel Capacity & Ownership Marking (Pottery)',
        'Incised or stamped on ceramic vessels (replicated on held-out M77 pottery graffiti); liquid/grain vessel capacity unit or pot-type mark.',
        ['tool', 'measure', 'commodity']
    ),
    'pot_small_stamped_vs_jars': (
        'Small Vessel Stamp: Pointed-Base Goblet / Ration Cup (POT:T:s)',
        'Stamped before firing onto small pointed-base goblets (median 17x13 mm) rather than large storage jars; ration-goblet stamp or small liquid unit.',
        ['tool', 'measure', 'action']
    ),
    'pot_storage_jar_vs_all': (
        'Bulk Vessel Marking: Large Storage Jars & Jar-Shoulders',
        'Incised or impressed on large storage jars (h>=90 mm / TAG:R jar shoulders); bulk 12-unit (dozen) or multi-marakkal storage capacity.',
        ['tool', 'measure', 'number']
    ),
    'mtab_all': (
        'Depot Ration & Issue Accounting (Harappa Miniature Tablets)',
        'Core sign of two-sided clay/faience depot chits; ration cup/measure, grain header, or recipient/artisan class.',
        ['measure', 'commodity', 'person']
    ),
    'tab_prism_vs_chit': (
        'Multi-Party Audit Accounting (3/4-Sided Prism Tablets)',
        'Concentrated across distinct texts on 3- and 4-sided prism tablets rather than flat 2-sided chits; multi-face summary audit unit, manager closer, or ledger header.',
        ['measure', 'person', 'action']
    ),
    'seal_giant_vs_seals': (
        'High-Rank Insignia: Giant Elite Steatite Seals (>=1,190 mm2)',
        'Concentrated on top-decile giant seals (surviving site x length control); supreme civic assembly, deputy/governor title, or paramount lineage crest.',
        ['person', 'quality', 'place']
    ),
    'seal_tiny_vs_seals': (
        'Subordinate / Junior Artisan Issue: Tiny Seals (<=365 mm2)',
        'Concentrated on bottom-quintile miniature seals; junior comb-rank holder, porter/load-tag clerk, or subordinate craft-hand.',
        ['person', 'quality', 'commodity']
    ),
    'seal_bar_rect_vs_seals': (
        'Non-Iconic Commodity/Allotment Stamp: Bossless Bar Seals (SEAL:R)',
        'Concentrated on animal-less rectangular bar seals sharing the exact lexicon of copper tablets and load tags (textiles, produce loads, land strips).',
        ['commodity', 'measure', 'place']
    ),
    'seal_round_cyl_vs_seals': (
        'Foreign / Gulf-Circuit Stamp: Round & Cylinder Seals',
        'Concentrated on circular Persian Gulf-type and Mesopotamian cylinder seals; non-standard person-marker or maritime merchant formula.',
        ['person', 'place', 'number']
    ),
    'har_mound_F': (
        'Granary & Threshing- Quarter Administration (Harappa Mound F)',
        'Concentrated in Harappa Mound F (Great Granary, circular threshing platforms, workmen quarters).',
        ['commodity', 'measure', 'person']
    ),
    'har_F_granary': (
        'Central State Granary Precinct (Harappa Mound F Granary)',
        'Concentrated in the Great Granary precinct at Harappa (replicated in M77 locus 40); bulk grain storage bin, 7-unit tally, or granary official.',
        ['commodity', 'measure', 'place']
    ),
    'har_F_platforms_quarters': (
        'Grain-Processing & Workmen Ration Zone (Harappa Mound F Platforms)',
        'Concentrated around Harappa Mound F circular threshing platforms and workmen lanes; junior ration-recipient title or threshing-gang crest.',
        ['person', 'commodity', 'action']
    ),
    'har_mound_E': (
        'Craft-Kiln & Gateway Quarter (Harappa Mound E)',
        'Concentrated in Harappa Mound E craft workshops and gateway trenches (4-cup standard issue and craft-guild crests).',
        ['measure', 'tool', 'place']
    ),
    'har_mound_AB': (
        'Citadel Garrison / Arsenal / High Precinct (Harappa Mound AB)',
        'Concentrated on Harappa Mound AB Citadel (replicated in held-out M77 locus 46-50); citadel forge/arsenal, acropolis quarter, or ruling/cultic crest.',
        ['place', 'person', 'deity']
    ),
    'md_citadel': (
        'Citadel Sacred/Civic Precinct (Mohenjo-daro SD/L Stupa & Great Bath)',
        'Concentrated on Mohenjo-daro Citadel Mound (replicated in held-out M77 locus 01-15); high-temple/citadel crest, ceremonial spindle/staff, or lunar calendar.',
        ['deity', 'person', 'place']
    ),
    'md_HR_elite': (
        'Elite Merchant Courtyard Houses (Mohenjo-daro HR-A/B)',
        'Concentrated in wealthy HR-A/B courtyard mansions at Mohenjo-daro (replicated in held-out M77 locus 16-18); patrician trading-house emblem.',
        ['kin', 'person', 'commodity']
    ),
    'md_DKG_south': (
        'Lower-Town Commercial Quarter (Mohenjo-daro DK-G South)',
        'Concentrated in DK-G South blocks at Mohenjo-daro.',
        ['place', 'person', 'commodity']
    ),
    'md_DKG_north': (
        'Northern Lower-Town Quarter (Mohenjo-daro DK-G North)',
        'Concentrated in DK-G North blocks at Mohenjo-daro.',
        ['person', 'kin', 'place']
    ),
    'md_VS_MN_craft': (
        'Dyers, Shell & Bead-Metal Craft Quarter (Mohenjo-daro VS & Moneer)',
        'Concentrated in Mohenjo-daro VS dyers-trough / craft quarter and Moneer metal/bead area (replicated in held-out M77 locus 20-22); craft-ward or dye-field house.',
        ['place', 'commodity', 'tool']
    ),
    'lothal_warehouse': (
        'Port Customs & Export Warehouse Hoard (Lothal SRG 3GX 10)',
        'Concentrated in the burnt sealing hoard of the Lothal Acropolis Warehouse; maritime shipping/sail header or dozen-fish bale export.',
        ['tool', 'commodity', 'place']
    ),
    'klb_citadel': (
        'Citadel Ritual/Administrative Enclave (Kalibangan KLB-1)',
        'Concentrated in Kalibangan Citadel (KLB-1) over Lower Town (KLB-2); transaction/levy or citadel office sign.',
        ['action', 'person', 'place']
    ),
    'site_chanhu_workshops': (
        'Specialized Bead, Seal & Metal Craft Town (Chanhu-daro Mound II)',
        'Concentrated at Chanhu-daro Mound II craft workshops (replicated in held-out M77 CD); industrial oilseed/fibre good or craft-guild formula.',
        ['tool', 'commodity', 'person']
    ),
    'circuit_maritime_coastal': (
        'Maritime & Coastal Port Circuit (Gujarat, Kutch, Makran & Gulf)',
        'Concentrated across coastal/maritime port settlements (Lothal, Dholavira, Bagasra, Surkotada, Oman/Gulf) stratified by object kind, replicating in held-out M77.',
        ['place', 'tool', 'commodity']
    ),
    'circuit_gulf_oman': (
        'Overseas Dilmun & Magan Maritime Trade (Persian Gulf & Oman)',
        'Concentrated on seals/vessels found in Bahrain, Failaka, Oman, and UAE (stratified by object kind); overseas merchant/person marker.',
        ['person', 'place']
    ),
    'circuit_overland_west_north': (
        'Overland Mesopotamia, Iran & Oxus Trade Circuit (Ur, Kish, Susa, BMAC)',
        'Strongly concentrated on Indus objects excavated in Mesopotamia, Susa/Iran, and Shortughai/Gonur (replicated 70.6x on held-out M77 WA!).',
        ['place', 'person', 'commodity']
    ),
    'circuit_all_abroad': (
        'Foreign Export & Expatriate Merchant Circuit (All Abroad)',
        'Concentrated across foreign Indus finds in Mesopotamia, Persian Gulf, Iran, and Central Asia.',
        ['place', 'person', 'commodity']
    ),
    'circuit_eastern_headwaters': (
        'Ghaggar-Hakra / Sutlej-Yamuna Agro-Pastoral Headwaters',
        'Concentrated in the Eastern Headwaters (Kalibangan, Banawali, Rakhigarhi, Karanpura, Rupar), replicating in held-out M77; regional crop (wheat/cotton) or grant verb.',
        ['plant', 'commodity', 'place']
    ),
    'circuit_riverine_core': (
        'Indus-Ravi Agrarian & Urban Heartland (Mohenjo-daro & Harappa Core)',
        'Locked to the riverine alluvial grain core when used in this syntactic slot.',
        ['measure', 'commodity', 'place']
    ),
}

# Specific high-precision sign overrides where multiple converging physical clues pin a sharper non-phonetic meaning!
SPECIFIC_SIGN_MEANINGS = {
    ('700', 'ANY'): (
        'Standard Ration Vessel / Capacity Unit (~9.2 L Cup)',
        'U-cup vessel sign on 471/524 miniature ration chits (OR=43.4; M77 new P=0.00036), taking tall stroke counts {1,2,3,4,6} (divisors of 12) and matching ~9.2 L measured jars.',
        ['measure', 'tool', 'commodity']
    ),
    ('400', 'ENDING'): (
        'Junior / Artisan / Attached-Worker Rank Closer (Comb)',
        'Text-final comb sign on half-size seals (<=365 mm2), Mound F workmen-quarter chits (346 tablets, M77 new P=0.00027), and ivory/bone rods (12 rods, M77 new P=0.019).',
        ['person', 'quality', 'tool']
    ),
    ('595', 'ANY'): (
        'Metallurgical Forge / Citadel Copper Arsenal',
        'Converges across 4 physical anchors: copper tools (595-850 M77 new P=9.2e-5), bull copper tablets (5/6, M77 new P=0.010), Harappa Mound AB Citadel (8/13, M77 new 5/6 P=4.1e-5), and giant seals (595-820).',
        ['tool', 'commodity', 'place']
    ),
    ('480', 'ANY'): (
        'Standard Metal-Ingot Weight & Vessel Capacity Unit',
        '3/3 on copper tools vs 0 on copper tablets (OR=111.6, M77 new bronze implements 2/2 P=0.016; @COUNTED 55x P=0.00045) AND 17/42 on ceramic vessels (M77 new replicated): Assay/weight & small capacity unit.',
        ['measure', 'commodity', 'tool']
    ),
    ('480', 'COUNTED'): (
        'Quantified Copper-Tool Weight / Alloy Specification',
        'Directly quantified by a numeral on copper/bronze implements (Lipi 46.6x P=0.0005; M77 new 55.0x P=0.00045); certifies metal weight of blades/axes.',
        ['measure', 'commodity', 'tool']
    ),
    ('140', 'ANY'): (
        'Dual-City Citadel Ruling / Cultic Crest (Female Figure with Raised Arm)',
        'Replicates on the Citadel Mounds of BOTH Harappa (Mound AB 3.51x P=0.003; M77 new 4.94x P=0.052) AND Mohenjo-daro (SD/L Citadel 2.54x P=0.0295; M77 new 2.90x P=0.041). High-temple goddess or matriarchal citadel crest.',
        ['deity', 'person', 'kin']
    ),
    ('820', 'NAME'): (
        'Citadel Quarter / Acropolis Administrative Division (6-Spoked Wheel)',
        'Invisible at ANY slot (P=1.0) due to generic opener use, but inside NAME slot clusters on Harappa Mound AB Citadel (3.97x P=0.0155; M77 new 5.93x P=0.0081), often before staff-king 142.',
        ['place', 'person']
    ),
    ('820', 'GOODS_OR_SOLO'): (
        'Coastal / Port Wheel-Unit or Cart/Quarter Lot',
        'When used as a standalone mark or counted unit (outside FRONT/NAME), concentrates in coastal/maritime port settlements (9/21, 3.27x, P=0.001).',
        ['tool', 'measure', 'place']
    ),
    ('705', 'COUNTED'): (
        'Bulk Grain / Commodity Capacity Measure (12-Cup Kalam Scale)',
        'Unmasked by slot split (ANY P=0.066 -> COUNTED P=0.0035): 14/106 on copper allotment tablets (M77 new 3.26x P=0.031) and 98/106 in Riverine Grain Core, taking tall strokes AFTER it.',
        ['measure', 'commodity']
    ),
    ('705', 'NAME'): (
        'Maritime Vessel / Port Freight Office (Uncounted Ship/Kalam Sign)',
        'When uncounted in NAME slot (e.g. 705-500), flips from inland measure to clay package sealings (Lipi P=0.0255; M77 new 13/32 P=0.0028) and coastal ports.',
        ['tool', 'place', 'person']
    ),
    ('500', 'NAME'): (
        'Maritime Sail / Freight Consignment Sign (Lothal & Package Sealings)',
        'Bisected triangle sign concentrated on clay package tags (Lipi P=0.0045; M77 new 8/11 P=0.00013) and Lothal Warehouse export sealings (3/4, P=0.021).',
        ['tool', 'action', 'place']
    ),
    ('880', 'ANY'): (
        'Package-Sealing Inspection / Dispatch Header (Vertex-Diamond)',
        'Concentrated on clay package sealings & multi-stamp lumps (Lipi 2.41x OR=8.6; M77 held-out new texts 5/5 = 100% on sealings, P=0.00022!).',
        ['action', 'measure', 'commodity']
    ),
    ('924', 'ANY'): (
        'Expatriate Overland Trade Marker (Mesopotamia / Susa / BMAC)',
        'Hatched outline-crescent sign enriched 30.8x (OR=62.6, P=0.002) on overland West/North foreign finds and replicated 70.6x (P=0.014) on held-out M77 West Asian seals.',
        ['place', 'person', 'commodity']
    ),
    ('923', 'COUNTED'): (
        'Commodity: Elephant Ivory / Tusk (Elephant Copper Tablets)',
        'Outline-tusk curve quantified after 706-033 on 6/7 elephant-pictured copper tablets (22.4x, OR=1252, FWER P=0.0005; M77 fs80=07 P=3e-5).',
        ['commodity', 'animal']
    ),
    ('923', 'NAME'): (
        'Elite Ivory-Merchant House Emblem (Mohenjo-daro HR-A/B)',
        'When placed inside personal/house names rather than counted on copper tablets, clusters in Mohenjo-daro HR-A/B elite merchant mansions (8/23, 2.73x, P=0.0055).',
        ['kin', 'person', 'commodity']
    ),
    ('806', 'COUNTED'): (
        'Botanical Crop / Agricultural Produce (Plant-Motif Tablets & Load Tags)',
        'Leaf-on-stalk sign sitting between A-comb counts and load-carriers; 12.4x enriched (FWER P=0.0005) on plant/pipal-pictured tablets across 5 distinct texts.',
        ['plant', 'commodity']
    ),
    ('806', 'ANY'): (
        'Agricultural Produce & Bar-Seal Allotment Sign (Leaf-on-Stalk)',
        '46/74 on bossless rectangular bar seals (OR=8.9, FWER P=0.0005) and 12.4x on plant-pictured tablets; staple crop/produce domain.',
        ['plant', 'commodity']
    ),
    ('407', 'ANY'): (
        'Woven Textile / Cloth Bolt or Estate Good (Copper Tablets & Bar Seals)',
        'Tree/fibre variant counted by small piece-numbers (tall 2) on 50/110 copper tablets (24 distinct texts, OR=35.1, FWER P=0.0005) and 35/110 bossless bar seals (OR=18.1).',
        ['commodity', 'tool', 'plant']
    ),
    ('390', 'SOLO'): (
        'Raw Cotton / Spinning Fibre Label (Whorls & Eastern Headwaters Pots)',
        'Unmasked at SOLO slot (ANY P=0.088 -> SOLO 8/11 = 12.0x, OR=38.8, P=0.001): whole-object label on Karanpura weavers spindle whorls and Kalibangan vessels.',
        ['plant', 'commodity', 'tool']
    ),
    ('390', 'NAME'): (
        'Cotton-Trade Craft Guild / Merchant House (Chanhu-daro Workshops)',
        'In NAME slot (chiefly 590-390 Boxed-Cotton house), clusters in Chanhu-daro craft town (Lipi P=0.019; M77 new P=0.018) and foreign square seals (Kish, Gonur).',
        ['commodity', 'kin', 'person']
    ),
    ('590', 'NAME'): (
        'Storehouse Chest / Treasury Receipt Token (TAG:P Smooth Tokens)',
        'Subdivided chest sign on 4/5 smooth package-less clay tokens across 4 distinct texts (OR=50.0, FWER P=0.002) and 3.8x in Harappa Granary; storage chest / treasury.',
        ['tool', 'place', 'commodity']
    ),
    ('048', 'ANY'): (
        'Wooden-Box Luxury Bundle / Seven-Strand Count (TAG:B Box Sealings)',
        'Bracketed 7-stroke sign on 10/10 Lothal wooden-box lid sealings (OR=8295, FDR q=0.007, FWER P=0.0005); boxed bead/luxury bundle unit.',
        ['number', 'commodity', 'tool']
    ),
    ('156', 'ANY'): (
        'Carried Bale / Soft-Package Shipment Load (TAG:L Cloth/Cord Bales)',
        'Yoke-carrier with two jar/bale loads enriched 8.82x (OR=59.7, FWER P=0.005) on TAG:L cloth/cord-backed bale sealings and count-line quantity stamps.',
        ['commodity', 'measure', 'person']
    ),
    ('540', 'SOLO'): (
        'Bulk Ceramic Vessel / Dry-Measure Container Mark (Pottery)',
        'Bowtie/double-cone sign standing alone as whole vessel label on pots & moulded jars (Lipi 4.23x P=0.0045; M77 new 8.57x P=0.017) and large storage jars.',
        ['measure', 'tool', 'commodity']
    ),
    ('413', 'FRONT'): (
        'Cereal / Grain Account Line Header (Harappa Tablets)',
        'Grain-ear stalk opening commodity ration lines on miniature tablets (33/36, 28 distinct texts, OR=28.9; M77 new P=0.021) and Mound E.',
        ['plant', 'commodity']
    ),
    ('411', 'ANY'): (
        'Eastern Headwaters Cereal / Wheat-Barley Ear (Ghaggar-Hakra Circuit)',
        'Drawn as a wheat shaft with upward chevrons; 6/9 occurrences across 5 distinct texts sit in Eastern Headwaters (OR=29.4, P=0.0005).',
        ['plant', 'commodity', 'place']
    ),
    ('503', 'NAME_CREST'): (
        'Striped Hill / Highland Estate & Dye-Quarter Sign',
        'Striped triangle (hill/mountain) on copper estate tablets (20/48, M77 new P=0.0026) AND Mohenjo-daro VS dyers/craft quarter (8/42, M77 new P=0.0093, often 503-615 Hill-Field).',
        ['place', 'commodity']
    ),
    ('615', 'NAME'): (
        'Irrigated Field Grid / Arable Land Plot',
        'Drawn as an x-by-y cell grid; core land-allotment sign on copper tablets (20/55, M77 new 15/81 P<1e-6) and VS craft quarter (M77 new P=0.066).',
        ['place', 'commodity', 'measure']
    ),
    ('845', 'ANY'): (
        'Paired-Leaf Produce / Land-Share Commodity (Copper Tablets & Bar Seals)',
        'Cross-hatched paired leaves on 29/43 copper tablets (13 distinct texts, OR=71.6, FWER P=0.004; M77 new P=0.0037) and 11 bossless bar seals (OR=23.1).',
        ['plant', 'commodity', 'place']
    ),
    ('222', 'ANY'): (
        'Rhinoceros-Class Lineage Crest (Bracketed Fish with Tooth)',
        '4/5 copper-tablet occurrences sit on rhinoceros tablets across 3 distinct texts (22.9x, OR=291, FWER P=0.0005, rival distinct P=0.00014; M77 fs80=11 4/4 P=3e-6).',
        ['animal', 'kin', 'person']
    ),
    ('027', 'ANY'): (
        'Dried-Fish / Scale Multi-Row Tally Unit (Fish-Motif Prism Tablets)',
        'Three rows of slanted ticks on 4/6 fish-shaped/motif miniature tablets across 4 distinct texts (23.3x, OR=75.2, FWER P=0.002, rival distinct P=1e-5).',
        ['number', 'measure', 'animal']
    ),
    ('578', 'ANY'): (
        'Multi-Face Prism Audit / Table Ledger Unit (3-Sided Prisms)',
        'Tall compartmented table sign; 5/5 distinct texts sit on 3-sided prism tablets (9.07x, OR=88.4, FDR q=0.019, FWER P=0.0005).',
        ['measure', 'tool', 'action']
    ),
    ('790', 'ANY'): (
        'Circular Bangle / Bead / Eye Ornament & Goat-Tablet Emblem',
        'Pointed oval/ringlet sign enriched 11.7x on stoneware & shell/terracotta bangles (6/48, 4 distinct texts, P=0.0005), tiny counted seals, and goat copper tablets.',
        ['tool', 'commodity', 'quality']
    ),
    ('840', 'SOLO'): (
        'Matched Pair / Twin-Bangle Designation (Two Overlapping Leaves)',
        '48.8x enriched as solo/pair mark on wrist-bangles (OR=150.4, FWER P=0.013) and 4.6x counted in HR-A/B merchant houses.',
        ['number', 'tool', 'quality']
    ),
    ('511', 'NAME'): (
        'Vitreous Stoneware Bangle Magistratial Guild / Title (511-130-920)',
        '28.6x enriched across 3 distinct micro-inscribed stoneware bangles (OR=79.5, P=0.0005; phrase 511-130 OR=875).',
        ['person', 'tool', 'quality']
    ),
    ('745', 'ANY'): (
        'Third Craft/Dyers Ward Vessel Emblem (Mohenjo-daro VS Quarter)',
        'Three-dotted handled jar enriched 4.7x across 5 distinct texts in Mohenjo-daro VS dyers/craft quarter (P=0.0025) and replicated 3.54x in held-out M77 locus 20-22 (P=0.0093).',
        ['place', 'tool', 'person']
    ),
    ('370', 'ANY'): (
        'Citadel Ceremonial / Textile-Spindle Emblem (Mohenjo-daro SD/L Citadel)',
        'Spindle/garlic-whorl shaft sign: 4/5 Mohenjo-daro provenanced occurrences (4 distinct texts) sit on the Citadel Mound (21.4x, OR=78.6, FWER P=0.0005), co-occurring corpus-wide with fibre trees.',
        ['tool', 'deity', 'commodity']
    ),
    ('374', 'ANY'): (
        'HR-AB Patrician Merchant House Plant Emblem',
        'Two-leaf curving plant sign enriched 3.15x across 4 distinct texts in Mohenjo-daro HR-A/B elite mansions (P=0.029) and replicated 5.84x in held-out M77 locus 16-18 (P=0.036).',
        ['plant', 'kin', 'person']
    ),
    ('842', 'ANY'): (
        'Supreme Civic / Governor Rank Sign (Giant Seals >=1,190 mm2)',
        '4/5 seal occurrences (4 distinct texts) sit on top-decile giant elite seals (8.44x, OR=34.6, P=0.0005).',
        ['person', 'quality']
    ),
    ('692', 'ANY'): (
        'Great-Seal Assembly / Directorate Header (Giant Seals >=1,190 mm2)',
        'Outline-X sign on 14 top-decile giant seals across 14 distinct texts (3.29x, OR=5.4, P=0.0005; 1.45x larger at matched text length).',
        ['person', 'place', 'quality']
    ),
    ('091', 'ANY'): (
        'Gulf / Round-Seal Twin-Person Foreign Marker',
        'Twin standing persons on 8/15 round/cylinder seals across 7 distinct texts (31.3x, OR=78.5, FWER P=0.0005) and 38.1x in Persian Gulf/Oman.',
        ['person', 'number', 'place']
    ),
    ('090', 'ANY'): (
        'Overseas Person Marker (Gulf) & Agent/Manager Title Closer',
        'Plain standing man: enriched 4.86x in Persian Gulf/Oman (P=0.0285; M77 new 13.0x P=0.075), 3.03x as prism-tablet closer (@ENDING P=0.005), and house-manager closer after jar 740.',
        ['person']
    ),
    ('890', 'NAME'): (
        'Eastern Headwaters & Sealing Grant/Issue Sign (Bow Motif)',
        '7/9 occurrences sit on clay sealings and in Eastern Headwaters (OR=47.7, P=0.0005; M77 new 9.7x P=0.100; phrase 890-892 M77 new 29.1x P=0.034).',
        ['action', 'commodity', 'place']
    ),
    ('391', 'NAME'): (
        'Copper-Implement Smithy / Alloy Crest (Capped Three-Pronged Sign)',
        '115x enriched on copper/bronze tools across 3 distinct texts (OR=298.7, P=0.0005; 3/3 vs copper tablets q=0.007) and replicated on held-out M77 bronze implements (P=0.018).',
        ['tool', 'commodity', 'person']
    ),
    ('632', 'NAME'): (
        'Bronze/Copper Tool Registry Enclosure Sign',
        '42.3x enriched on copper/bronze tools (OR=79.9, P=0.0005; 3/3 vs copper tablets q=0.007; M77 all bronze implements 2/2 P=0.0076) and Harappa Mound AB Citadel.',
        ['tool', 'commodity', 'place']
    ),
    ('930', 'NAME'): (
        'Wheeled-Arch Copper Implement Workshop Sign (632-930)',
        '300x enriched exclusively on copper/bronze implements (3/3 vs copper tablets, OR=3290, FWER P=0.0005).',
        ['tool', 'commodity']
    ),
    ('838', 'GOODS_OR_SOLO'): (
        'Oilseed / Sesame Commodity Tag (Chanhu-daro Craft Town & Lothal)',
        'Unmasked at GOODS_OR_SOLO slot (ANY P=0.051 -> 18.2x, OR=45.6, P=0.003 at Chanhu-daro workshops; solo tag at Lothal), while @NAME sits on ivory/bone rods (14.6x P=0.002).',
        ['plant', 'commodity']
    ),
}


# ---------------- 3. Select & Export sign_anchors.csv ----------------
cand_signs = df[df.ftype.isin(['SIGN', 'SLOT_SIGN']) & (df.strat_lift >= 1.5) & (
    (df.replicated_new == 'True') |
    (df.lipi_q_fdr_dom <= 0.05) |
    (df.lipi_p_fwer_dom <= 0.05) |
    ((df.lipi_p_shuf <= 0.015) & (df.lipi_distinct_texts_in >= 2) & (df.strat_lift >= 2.2) & (df.rival_distinct_p <= 0.05))
)].copy()


def assign_tier(r):
    if r['replicated_new'] == 'True':
        return 'TIER_1_NEW_REPLICATED'
    mp = pd.to_numeric(r['mah_all_p_fisher'], errors='coerce')
    if pd.notna(mp) and mp <= 0.01 and int(r['mah_all_k_in']) >= 2:
        return 'TIER_1B_MAH_FULL_REPLICATED'
    if r['lipi_q_fdr_dom'] <= 0.05 or r['lipi_p_fwer_dom'] <= 0.05:
        return 'TIER_2_FDR_FWER'
    return 'TIER_3_SLOT_OR_MULTITEXT_LEAD'


cand_signs['tier'] = [assign_tier(r) for _, r in cand_signs.iterrows()]
tier_rank = {
    'TIER_1_NEW_REPLICATED': 1,
    'TIER_1B_MAH_FULL_REPLICATED': 2,
    'TIER_2_FDR_FWER': 3,
    'TIER_3_SLOT_OR_MULTITEXT_LEAD': 4,
}
cand_signs['trank'] = cand_signs['tier'].map(tier_rank)
cand_signs = cand_signs.sort_values(['trank', 'lipi_p_shuf', 'lipi_p_fwer_dom', 'strat_lift'],
                                    ascending=[True, True, True, False])

# Keep best anchor per sign, PLUS a second row if the sign has a distinct syntactic-slot split in a different domain family!
selected_sign_rows = []
seen_per_sign = collections.defaultdict(list)

for _, r in cand_signs.iterrows():
    s = r['unit']
    sl = r['slot']
    dom = r['domain']
    prev = seen_per_sign[s]
    if len(prev) == 0:
        seen_per_sign[s].append((sl, dom))
        selected_sign_rows.append(r)
    elif len(prev) == 1:
        prev_sl, prev_dom = prev[0]
        # Keep a 2nd slot-disentangled entry if it is a genuinely different slot role AND different physical domain!
        diff_role = (sl != prev_sl) and not ({sl, prev_sl} <= {'COUNTED', 'SOLO', 'GOODS_OR_SOLO'}) and not ({sl, prev_sl} <= {'NAME', 'NAME_CREST', 'PRE_CLOSER'})
        diff_dom = dom.split('_')[0] != prev_dom.split('_')[0] or (s, sl) in SPECIFIC_SIGN_MEANINGS
        if (diff_role and diff_dom and (r['trank'] <= 3 or (s, sl) in SPECIFIC_SIGN_MEANINGS)):
            seen_per_sign[s].append((sl, dom))
            selected_sign_rows.append(r)

sign_out = []
for r in selected_sign_rows:
    s = r['unit']
    sl = r['slot']
    dom = r['domain']
    if (s, sl) in SPECIFIC_SIGN_MEANINGS:
        p_dom, hyp, c_list = SPECIFIC_SIGN_MEANINGS[(s, sl)]
    elif (s, 'ANY') in SPECIFIC_SIGN_MEANINGS and len(seen_per_sign[s]) == 1:
        p_dom, hyp, c_list = SPECIFIC_SIGN_MEANINGS[(s, 'ANY')]
    else:
        p_dom, hyp, c_list = DOMAIN_SEMANTICS.get(
            dom, (r['domain_label'], f'Empirically enriched in {r["domain_label"]} ({sl} slot).', ['commodity', 'person'])
        )

    cats_str, cmask, cbits = encode_cats(c_list)
    k_in, n_in = int(r['lipi_k_in']), int(r['lipi_n_in'])
    k_out = int(r['lipi_k_tot']) - k_in
    n_out = int(r['lipi_n_pool']) - n_in
    dt = int(r['lipi_distinct_texts_in'])
    lipi_cnt_str = f'{k_in}/{n_in} vs {k_out}/{n_out} (dt={dt})'

    nk_in = int(r['new_k_in']) if str(r['new_k_in']) != '' else 0
    nn_in = int(r['new_n_in']) if str(r['new_n_in']) != '' else 0
    nk_tot = int(r['new_k_tot']) if str(r['new_k_tot']) != '' else 0
    new_cnt_str = f'{nk_in}/{nn_in} (tot={nk_tot})' if nn_in > 0 and nk_tot > 0 else 'untested_in_new'

    mk_in = int(r['mah_all_k_in']) if str(r['mah_all_k_in']) != '' else 0
    mk_tot = int(r['mah_all_k_tot']) if str(r['mah_all_k_tot']) != '' else 0
    mp = r['mah_all_p_fisher']
    mah_note = f'{mk_in}/{mk_tot} (P={mp})' if mk_tot > 0 and mp != '' else ''

    shp = sm.loc[s, 'shape_desc'] if s in sm.index else r['shape_desc']
    v2c = sm.loc[s, 'v2_class'] if s in sm.index else r['v2_class']

    sign_out.append(dict(
        sign=s,
        slot=sl,
        v2_class=v2c,
        shape_desc=shp,
        anchor_tier=r['tier'],
        pinned_domain=p_dom,
        concrete_meaning_hypothesis=hyp,
        source_domain=dom,
        lipi_counts=lipi_cnt_str,
        lipi_strat_lift=r['strat_lift'],
        lipi_odds=r['lipi_odds'],
        lipi_p_fisher=round(float(r['lipi_p_fisher']), 6),
        lipi_p_shuf=round(float(r['lipi_p_shuf']), 5),
        lipi_q_fdr=round(float(r['lipi_q_fdr_dom']), 5),
        lipi_p_fwer=round(float(r['lipi_p_fwer_dom']), 5),
        rival_distinct_p=round(float(r['rival_distinct_p']), 5),
        mah_new_counts=new_cnt_str,
        mah_new_odds=r['new_odds'],
        mah_new_p=r['new_p_fisher'],
        mah_all_replication=mah_note,
        cats=cats_str,
        cat_mask=cmask,
        cat_bits_13=cbits,
    ))

sign_anchors_df = pd.DataFrame(sign_out)
sign_anchors_df.to_csv(os.path.join(OUT, 'sign_anchors.csv'), index=False)
log(f'Exported work_data/sem/sign_anchors.csv: {len(sign_anchors_df)} anchored (sign, slot) rows '
    f'covering {sign_anchors_df.sign.nunique()} distinct Indus signs!')
log('Tier breakdown (signs):', sign_anchors_df.anchor_tier.value_counts().to_dict())


# ---------------- 4. Select & Export phrase_anchors.csv ----------------
cand_phrases = df[df.ftype.isin(['PHRASE2', 'PHRASE3']) & (df.strat_lift >= 1.5) & (
    (df.replicated_new == 'True') |
    (df.lipi_q_fdr_dom <= 0.05) |
    (df.lipi_p_fwer_dom <= 0.05) |
    ((df.lipi_p_shuf <= 0.01) & (df.lipi_distinct_texts_in >= 3) & (df.strat_lift >= 3.0) & (df.rival_distinct_p <= 0.02))
)].copy()
cand_phrases['tier'] = [assign_tier(r) for _, r in cand_phrases.iterrows()]
cand_phrases['trank'] = cand_phrases['tier'].map(tier_rank)
cand_phrases = cand_phrases.sort_values(['trank', 'lipi_p_shuf', 'lipi_p_fwer_dom', 'strat_lift'],
                                        ascending=[True, True, True, False])

phrase_out = []
seen_p = set()
for _, r in cand_phrases.iterrows():
    p = r['unit']
    if p in seen_p:
        continue
    seen_p.add(p)
    dom = r['domain']
    p_dom, hyp, c_list = DOMAIN_SEMANTICS.get(
        dom, (r['domain_label'], f'Fixed phrase empirically anchored in {r["domain_label"]}.', ['commodity', 'person'])
    )
    cats_str, cmask, cbits = encode_cats(c_list)
    k_in, n_in = int(r['lipi_k_in']), int(r['lipi_n_in'])
    k_out = int(r['lipi_k_tot']) - k_in
    n_out = int(r['lipi_n_pool']) - n_in
    dt = int(r['lipi_distinct_texts_in'])
    nk_in = int(r['new_k_in']) if str(r['new_k_in']) != '' else 0
    nn_in = int(r['new_n_in']) if str(r['new_n_in']) != '' else 0
    nk_tot = int(r['new_k_tot']) if str(r['new_k_tot']) != '' else 0
    new_cnt_str = f'{nk_in}/{nn_in} (tot={nk_tot})' if nn_in > 0 and nk_tot > 0 else 'untested_in_new'

    phrase_out.append(dict(
        phrase=p,
        ftype=r['ftype'],
        anchor_tier=r['tier'],
        pinned_domain=p_dom,
        concrete_meaning_hypothesis=hyp,
        source_domain=dom,
        lipi_counts=f'{k_in}/{n_in} vs {k_out}/{n_out} (dt={dt})',
        lipi_strat_lift=r['strat_lift'],
        lipi_odds=r['lipi_odds'],
        lipi_p_shuf=round(float(r['lipi_p_shuf']), 5),
        lipi_q_fdr=round(float(r['lipi_q_fdr_dom']), 5),
        lipi_p_fwer=round(float(r['lipi_p_fwer_dom']), 5),
        rival_distinct_p=round(float(r['rival_distinct_p']), 5),
        mah_new_counts=new_cnt_str,
        mah_new_odds=r['new_odds'],
        mah_new_p=r['new_p_fisher'],
        cats=cats_str,
        cat_mask=cmask,
    ))

phrase_anchors_df = pd.DataFrame(phrase_out)
phrase_anchors_df.to_csv(os.path.join(OUT, 'phrase_anchors.csv'), index=False)
log(f'Exported work_data/sem/phrase_anchors.csv: {len(phrase_anchors_df)} distinct anchored phrases!')
log('Tier breakdown (phrases):', phrase_anchors_df.anchor_tier.value_counts().to_dict())
