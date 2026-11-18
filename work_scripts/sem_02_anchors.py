#!/usr/bin/env python3
"""sem_02_anchors.py -- Comprehensive Physical & Archaeological Semantic Anchor Miner.

Runs a multi-hypothesis association sweep testing:
  1. Individual signs (ANY position, >= 3 Lipi copy-events)
  2. 2-sign contiguous phrases & fixed phrases from work_data/phrases/phrase_list.csv (>= 3 Lipi copy-events)
  3. Redesign / Slot-disentangled sign occurrences (s@GOODS_OR_SOLO, s@COUNTED, s@SOLO, s@FRONT,
     s@NAME, s@NAME_CREST, s@PRE_CLOSER, s@ENDING; >= 3 Lipi copy-events)

Against 42 archaeological & physical domains across three axes:
  Axis A: Object medium, vessel/package subtype, tablet geometry, seal size, copper-tablet animal face
  Axis B: Intra-city functional zones (Harappa, Mohenjo-daro, Lothal, Dholavira, Chanhu-daro, Kalibangan)
  Axis C: Inter-city & foreign trade circuits (Coastal/Maritime, Gulf/Oman, Overland West/North,
          All Abroad, Eastern Headwaters, Riverine Grain Core)

Controls & Validation:
  - One row per physical copy-event (moulded copy batch at same findspot = 1 event).
  - 2,000 exact stratum-aware object shuffles per domain (controlling for site on medium tests,
    within-city pool on intra-city zone tests, and object_kind on inter-city circuit tests).
  - Benjamini-Hochberg FDR (within-domain & global) and Westfall-Young max-z family-wise P.
  - Strongest rival explanation test on every hit:
      * Distinct-text survival (1 vote per unique full inscription) + distinct-text count
      * Finer stratum control (city x object_kind for intra-city zones)
  - Held-out replication on unseen Mahadevan `new texts` (990 events from 1,183 unpartnered lines),
    with exact Fisher P and 2,000 stratum-aware shuffles.
"""
import os
import sys
import json
import time
import collections
import numpy as np
import pandas as pd
from scipy.stats import fisher_exact

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

OUT = os.path.join(ROOT, 'work_data', 'sem')
os.makedirs(OUT, exist_ok=True)
T0 = time.time()


def log(*args):
    print(f'[sem_02 {time.time() - T0:6.1f}s]', *args, flush=True)


# ---------------- 1. Load Copy-Event Tables ----------------
log('Loading Lipi (4,476) and held-out Mahadevan new-text (990) copy-events ...')
ev_lipi = json.load(open(os.path.join(OUT, 'events_lipi.json')))
ev_new = json.load(open(os.path.join(OUT, 'events_new.json')))
ev_mall = json.load(open(os.path.join(OUT, 'events_mah_all.json')))
sign_meta = pd.read_csv(os.path.join(OUT, 'sign_meta.csv'), dtype=str).fillna('')
shape_of = dict(zip(sign_meta.sign, sign_meta.shape_desc))
v2_of = dict(zip(sign_meta.sign, sign_meta.v2_class))

phrase_atlas = pd.read_csv(os.path.join(ROOT, 'work_data', 'phrases', 'phrase_list.csv'), dtype=str).fillna('')
fixed_phrases = set(phrase_atlas.phrase)
minor_atlas = pd.read_csv(os.path.join(ROOT, 'work_data', 'phrases', 'minor_phrases.csv'), dtype=str).fillna('')
fixed_phrases |= set(minor_atlas.phrase)

# Add Harappa pictured mtab helper tags to Lipi events
for r in ev_lipi:
    st_set = set(r['subtypes'])
    if r['kind'] == 'mtab':
        sa = r.get('seal_animal', '')
        if sa == 'Gavi':
            st_set.add('mtab_gharial')
        elif sa in ('Phyt', 'Pipal'):
            st_set.add('mtab_plant')
        elif sa == 'Fish':
            st_set.add('mtab_fish')
    if 'tag_R_jarmouth' in st_set or 'tag_W_peg' in st_set:
        st_set.add('tag_RW_jar_peg')
    r['_st'] = st_set
    r['_zn'] = set(r['zones'])

for r in ev_new:
    r['_st'] = set(r['subtypes'])
    r['_zn'] = set(r['zones'])

for r in ev_mall:
    r['_st'] = set(r['subtypes'])
    r['_zn'] = set(r['zones'])


# ---------------- 2. Build Feature Matrices (Signs, Phrases, Slot-Specific Signs) ----------------
MIN_EVENTS = 3
sign_counts = collections.Counter(s for r in ev_lipi for s in r['signs'])
p2_counts = collections.Counter(p for r in ev_lipi for p in r['phrases2'])
p3_counts = collections.Counter(p for r in ev_lipi for p in r['phrases3'] if p in fixed_phrases)

SLOTS_TO_TEST = ['GOODS_OR_SOLO', 'COUNTED', 'SOLO', 'FRONT', 'NAME', 'NAME_CREST', 'PRE_CLOSER', 'ENDING']
slot_counts = collections.Counter()
for r in ev_lipi:
    for sl in SLOTS_TO_TEST:
        for s in r['slot_signs'].get(sl, []):
            slot_counts[(s, sl)] += 1

features = []  # list of dicts: fid, ftype, sign_or_phrase, slot
for s, cnt in sorted(sign_counts.items()):
    if cnt >= MIN_EVENTS:
        features.append(dict(fid=f'SIGN:{s}', ftype='SIGN', unit=s, slot='ANY', lipi_tot=cnt))

for p, cnt in sorted(p2_counts.items()):
    if cnt >= MIN_EVENTS:
        features.append(dict(fid=f'PHRASE:{p}', ftype='PHRASE2', unit=p, slot='PHRASE', lipi_tot=cnt))

for p, cnt in sorted(p3_counts.items()):
    if cnt >= MIN_EVENTS:
        features.append(dict(fid=f'PHRASE3:{p}', ftype='PHRASE3', unit=p, slot='PHRASE', lipi_tot=cnt))

for (s, sl), cnt in sorted(slot_counts.items()):
    if cnt >= MIN_EVENTS:
        features.append(dict(fid=f'SLOT:{s}@{sl}', ftype='SLOT_SIGN', unit=s, slot=sl, lipi_tot=cnt))

f_index = {f['fid']: i for i, f in enumerate(features)}
U = len(features)
log(f'Total testable features (>={MIN_EVENTS} Lipi events): {U} '
    f'(signs={sum(f["ftype"]=="SIGN" for f in features)}, '
    f'phrases2={sum(f["ftype"]=="PHRASE2" for f in features)}, '
    f'phrases3={sum(f["ftype"]=="PHRASE3" for f in features)}, '
    f'slot_signs={sum(f["ftype"]=="SLOT_SIGN" for f in features)})')


def build_feature_matrix(evs):
    X = np.zeros((len(evs), U), dtype=np.float32)
    for row_i, r in enumerate(evs):
        for s in r['signs']:
            idx = f_index.get(f'SIGN:{s}')
            if idx is not None:
                X[row_i, idx] = 1.0
        for p in r['phrases2']:
            idx = f_index.get(f'PHRASE:{p}')
            if idx is not None:
                X[row_i, idx] = 1.0
        for p in r['phrases3']:
            idx = f_index.get(f'PHRASE3:{p}')
            if idx is not None:
                X[row_i, idx] = 1.0
        for sl in SLOTS_TO_TEST:
            for s in r['slot_signs'].get(sl, []):
                idx = f_index.get(f'SLOT:{s}@{sl}')
                if idx is not None:
                    X[row_i, idx] = 1.0
    return X


X_lipi = build_feature_matrix(ev_lipi)
X_new = build_feature_matrix(ev_new)
X_mall = build_feature_matrix(ev_mall)


# ---------------- 3. Define the 42 Archaeological & Physical Domains ----------------
# Each domain spec: (domain_id, axis, human_label, pool_fn, target_fn, stratum_fn, rival_stratum_fn, has_new_equiv)
DOMAINS = [
    # --- AXIS A: OBJECT MEDIUM & FUNCTION ---
    ('copper_tool_vs_all', 'A_medium', 'Copper/bronze tools & weapons (vs all)',
     lambda r: True, lambda r: 'copper_tool' in r['_st'],
     lambda r: r['site'], lambda r: r['site'], True),

    ('copper_tool_vs_ctab', 'A_medium', 'Copper tools/weapons vs Copper tablets',
     lambda r: ('copper_tool' in r['_st']) or ('copper_tablet' in r['_st']),
     lambda r: 'copper_tool' in r['_st'],
     lambda r: 'all', lambda r: 'all', True),

    ('copper_tablet_vs_all', 'A_medium', 'Copper tablets (vs same-city objects)',
     lambda r: True, lambda r: 'copper_tablet' in r['_st'],
     lambda r: r['site'], lambda r: r['site'], True),

    ('ctab_elephant', 'A_copper_animal', 'Copper tablet: Elephant face (within copper tablets)',
     lambda r: 'copper_tablet' in r['_st'], lambda r: 'ctab_elephant' in r['_st'],
     lambda r: 'ctab', lambda r: 'ctab', True),

    ('ctab_hare', 'A_copper_animal', 'Copper tablet: Hare face (within copper tablets)',
     lambda r: 'copper_tablet' in r['_st'], lambda r: 'ctab_hare' in r['_st'],
     lambda r: 'ctab', lambda r: 'ctab', True),

    ('ctab_human_archer', 'A_copper_animal', 'Copper tablet: Horned archer/hunter face (within copper tablets)',
     lambda r: 'copper_tablet' in r['_st'], lambda r: 'ctab_human_archer' in r['_st'],
     lambda r: 'ctab', lambda r: 'ctab', True),

    ('ctab_goat_antelope', 'A_copper_animal', 'Copper tablet: Goat/markhor/stag face (within copper tablets)',
     lambda r: 'copper_tablet' in r['_st'], lambda r: 'ctab_goat_antelope' in r['_st'],
     lambda r: 'ctab', lambda r: 'ctab', True),

    ('ctab_bull_gaur_unicorn', 'A_copper_animal', 'Copper tablet: Bull/gaur/unicorn face (within copper tablets)',
     lambda r: 'copper_tablet' in r['_st'],
     lambda r: ('ctab_bull_gaur' in r['_st']) or ('ctab_unicorn' in r['_st']) or ('ctab_buffalo' in r['_st']),
     lambda r: 'ctab', lambda r: 'ctab', True),

    ('ctab_rhinoceros', 'A_copper_animal', 'Copper tablet: Rhinoceros face (within copper tablets)',
     lambda r: 'copper_tablet' in r['_st'], lambda r: 'ctab_rhinoceros' in r['_st'],
     lambda r: 'ctab', lambda r: 'ctab', True),

    ('ctab_composite', 'A_copper_animal', 'Copper tablet: Composite beast face (within copper tablets)',
     lambda r: 'copper_tablet' in r['_st'], lambda r: 'ctab_composite' in r['_st'],
     lambda r: 'ctab', lambda r: 'ctab', True),

    ('ctab_picsign', 'A_copper_animal', 'Copper tablet: Single sign replacing animal face',
     lambda r: 'copper_tablet' in r['_st'], lambda r: 'ctab_picsign' in r['_st'],
     lambda r: 'ctab', lambda r: 'ctab', False),

    ('mtab_gharial', 'A_tablet_icon', 'Moulded tablet: Gharial crocodile motif (within tablets)',
     lambda r: 'mtab_all' in r['_st'], lambda r: 'mtab_gharial' in r['_st'],
     lambda r: r['site'], lambda r: r['site'], False),

    ('mtab_plant', 'A_tablet_icon', 'Moulded tablet: Plant/pipal motif (within tablets)',
     lambda r: 'mtab_all' in r['_st'], lambda r: 'mtab_plant' in r['_st'],
     lambda r: r['site'], lambda r: r['site'], False),

    ('mtab_fish', 'A_tablet_icon', 'Moulded tablet: Fish-shaped/motif tablet (within tablets)',
     lambda r: 'mtab_all' in r['_st'], lambda r: 'mtab_fish' in r['_st'],
     lambda r: r['site'], lambda r: r['site'], False),

    ('bangle_stoneware', 'A_medium', 'Stoneware bangles (vs same-city objects)',
     lambda r: True, lambda r: 'bangle_stoneware' in r['_st'],
     lambda r: r['site'], lambda r: r['site'], False),

    ('bangle_other_mat', 'A_medium', 'Shell/terracotta/clay bangles (vs same-city objects)',
     lambda r: True, lambda r: 'bangle_other_mat' in r['_st'],
     lambda r: r['site'], lambda r: r['site'], False),

    ('bangle_all', 'A_medium', 'All bangles (stoneware + shell/clay/terracotta)',
     lambda r: True, lambda r: 'bangle_all' in r['_st'],
     lambda r: r['site'], lambda r: r['site'], False),

    ('ivory_bone_rod', 'A_medium', 'Ivory & bone rods (vs same-city objects)',
     lambda r: True, lambda r: 'ivory_bone_rod' in r['_st'],
     lambda r: r['site'], lambda r: r['site'], True),

    ('tag_all', 'A_medium', 'Clay package sealings & tags (vs same-city objects)',
     lambda r: True, lambda r: 'tag_all' in r['_st'],
     lambda r: r['site'], lambda r: r['site'], True),

    ('tag_B_box_within_tags', 'A_package', 'Clay tag reverse B: Wooden box lid/chest (within tags)',
     lambda r: 'tag_all' in r['_st'], lambda r: 'tag_B_box' in r['_st'],
     lambda r: 'tag', lambda r: r['site'], False),

    ('tag_P_token_within_tags', 'A_package', 'Clay tag reverse P: Smooth clay token, no packing (within tags)',
     lambda r: 'tag_all' in r['_st'], lambda r: 'tag_P_token' in r['_st'],
     lambda r: 'tag', lambda r: r['site'], False),

    ('tag_L_bale_within_tags', 'A_package', 'Clay tag reverse L: Soft cloth/reed/cord bale package (within tags)',
     lambda r: 'tag_all' in r['_st'], lambda r: 'tag_L_bale' in r['_st'],
     lambda r: 'tag', lambda r: r['site'], False),

    ('tag_O_cane_within_tags', 'A_package', 'Clay tag reverse O: Cane/reed packing (within tags)',
     lambda r: 'tag_all' in r['_st'], lambda r: 'tag_O_cane' in r['_st'],
     lambda r: 'tag', lambda r: r['site'], False),

    ('pot_all', 'A_medium', 'Inscribed pottery vessels (vs same-city objects)',
     lambda r: True, lambda r: 'pot_all' in r['_st'],
     lambda r: r['site'], lambda r: r['site'], True),

    ('pot_storage_jar_vs_small', 'A_vessel', 'Large storage jars & jar-mouths vs Small stamped goblets',
     lambda r: ('pot_storage_jar' in r['_st']) or ('pot_small_stamped' in r['_st']),
     lambda r: 'pot_storage_jar' in r['_st'],
     lambda r: 'pot_sz', lambda r: r['site'], False),

    ('pot_small_stamped_vs_jars', 'A_vessel', 'Small stamped goblets (POT:T:s) vs Large/graffito pots',
     lambda r: 'pot_all' in r['_st'], lambda r: 'pot_small_stamped' in r['_st'],
     lambda r: r['site'], lambda r: r['site'], False),

    ('pot_storage_jar_vs_all', 'A_vessel', 'Large storage jars & jar-shoulder sealings (vs same-city objects)',
     lambda r: True, lambda r: 'pot_storage_jar' in r['_st'],
     lambda r: r['site'], lambda r: r['site'], False),

    ('mtab_all', 'A_medium', 'Miniature clay/faience tablets (vs same-city objects)',
     lambda r: True, lambda r: 'mtab_all' in r['_st'],
     lambda r: r['site'], lambda r: r['site'], True),

    ('tab_prism_vs_chit', 'A_tablet_form', '3/4-sided prism tablets vs Flat 1/2-sided chits',
     lambda r: 'mtab_all' in r['_st'], lambda r: 'tab_prism' in r['_st'],
     lambda r: r['site'], lambda r: r['site'], False),

    ('tab_chit_vs_prism', 'A_tablet_form', 'Flat 1/2-sided miniature chits vs Prisms',
     lambda r: 'mtab_all' in r['_st'], lambda r: 'tab_flat_chit' in r['_st'],
     lambda r: r['site'], lambda r: r['site'], False),

    ('seal_giant_vs_seals', 'A_seal_rank', 'Giant elite seals (>=1190 mm2, top decile) vs other seals',
     lambda r: ('seal_giant' in r['_st']) or ('seal_tiny' in r['_st']) or ('seal_all' in r['_st']),
     lambda r: 'seal_giant' in r['_st'],
     lambda r: r['site'], lambda r: f"{r['site']}|L{min(6, max((len(f) for f in r['faces']), default=0))}", False),

    ('seal_tiny_vs_seals', 'A_seal_rank', 'Tiny comb-class seals (<=365 mm2) vs other seals',
     lambda r: 'seal_all' in r['_st'], lambda r: 'seal_tiny' in r['_st'],
     lambda r: r['site'], lambda r: f"{r['site']}|L{min(6, max((len(f) for f in r['faces']), default=0))}", False),

    ('seal_bar_rect_vs_seals', 'A_seal_rank', 'Bossless rectangular bar seals (SEAL:R) vs other seals',
     lambda r: 'seal_all' in r['_st'], lambda r: 'seal_bar_rect' in r['_st'],
     lambda r: r['site'], lambda r: r['site'], False),

    ('seal_round_cyl_vs_seals', 'A_seal_rank', 'Round Gulf-type & cylinder seals vs other seals',
     lambda r: 'seal_all' in r['_st'], lambda r: 'seal_round_cyl' in r['_st'],
     lambda r: 'seal', lambda r: r['circuit'], False),

    # --- AXIS B: INTRA-CITY FUNCTIONAL ZONES ---
    ('har_mound_F', 'B_zone_harappa', 'Harappa Mound F (Granary/platforms/quarters) vs rest of Harappa',
     lambda r: r['site'] == 'Harappa' and len(r['_zn']) > 0,
     lambda r: 'har_mound_F' in r['_zn'],
     lambda r: 'Harappa', lambda r: f"Harappa|{r['kind']}", True),

    ('har_F_granary', 'B_zone_harappa', 'Harappa Great Granary (FGranery) vs rest of Harappa',
     lambda r: r['site'] == 'Harappa' and len(r['_zn']) > 0,
     lambda r: 'har_F_granary' in r['_zn'],
     lambda r: 'Harappa', lambda r: f"Harappa|{r['kind']}", True),

    ('har_F_platforms_quarters', 'B_zone_harappa', 'Harappa Mound F threshing platforms & workmen quarters vs rest',
     lambda r: r['site'] == 'Harappa' and len(r['_zn']) > 0,
     lambda r: 'har_F_platforms_quarters' in r['_zn'],
     lambda r: 'Harappa', lambda r: f"Harappa|{r['kind']}", True),

    ('har_mound_E', 'B_zone_harappa', 'Harappa Mound E (craft workshops & gateway) vs rest of Harappa',
     lambda r: r['site'] == 'Harappa' and len(r['_zn']) > 0,
     lambda r: 'har_mound_E' in r['_zn'],
     lambda r: 'Harappa', lambda r: f"Harappa|{r['kind']}", False),

    ('har_mound_AB', 'B_zone_harappa', 'Harappa Mound AB (Citadel) vs rest of Harappa',
     lambda r: r['site'] == 'Harappa' and len(r['_zn']) > 0,
     lambda r: 'har_mound_AB' in r['_zn'],
     lambda r: 'Harappa', lambda r: f"Harappa|{r['kind']}", True),

    ('md_citadel', 'B_zone_md', 'Mohenjo-daro Citadel (SD/L/Stupa/Great Bath) vs Lower Town',
     lambda r: r['site'] == 'Mohenjo-daro' and len(r['_zn']) > 0,
     lambda r: 'md_citadel' in r['_zn'],
     lambda r: 'MD', lambda r: f"MD|{r['kind']}", True),

    ('md_HR_elite', 'B_zone_md', 'Mohenjo-daro HR-A/B elite merchant houses vs rest of MD',
     lambda r: r['site'] == 'Mohenjo-daro' and len(r['_zn']) > 0,
     lambda r: 'md_HR_elite' in r['_zn'],
     lambda r: 'MD', lambda r: f"MD|{r['kind']}", True),

    ('md_DKG_south', 'B_zone_md', 'Mohenjo-daro DK-G South vs rest of MD',
     lambda r: r['site'] == 'Mohenjo-daro' and len(r['_zn']) > 0,
     lambda r: 'md_DKG_south' in r['_zn'],
     lambda r: 'MD', lambda r: f"MD|{r['kind']}", True),

    ('md_DKG_north', 'B_zone_md', 'Mohenjo-daro DK-G North vs rest of MD',
     lambda r: r['site'] == 'Mohenjo-daro' and len(r['_zn']) > 0,
     lambda r: 'md_DKG_north' in r['_zn'],
     lambda r: 'MD', lambda r: f"MD|{r['kind']}", True),

    ('md_VS_MN_craft', 'B_zone_md', 'Mohenjo-daro VS dyers/shell/metal & Moneer craft quarters vs rest',
     lambda r: r['site'] == 'Mohenjo-daro' and len(r['_zn']) > 0,
     lambda r: 'md_VS_MN_craft' in r['_zn'],
     lambda r: 'MD', lambda r: f"MD|{r['kind']}", True),

    ('lothal_warehouse', 'B_zone_lothal', 'Lothal Warehouse (SRG 3GX 10) vs Town/Dock/Acropolis/Bead factory',
     lambda r: r['site'] == 'Lothal' and len(r['_zn']) > 0,
     lambda r: 'lothal_warehouse' in r['_zn'],
     lambda r: 'Lothal', lambda r: f"Lothal|{r['kind']}", False),

    ('lothal_town_dock_bead', 'B_zone_lothal', 'Lothal Dock/Acropolis/Bead factory vs Warehouse',
     lambda r: r['site'] == 'Lothal' and len(r['_zn']) > 0,
     lambda r: 'lothal_town_dock_bead' in r['_zn'],
     lambda r: 'Lothal', lambda r: f"Lothal|{r['kind']}", False),

    ('dhol_citadel_bailey', 'B_zone_dholavira', 'Dholavira Citadel & Bailey vs Middle/Lower Town',
     lambda r: r['site'] == 'Dholavira' and len(r['_zn']) > 0,
     lambda r: 'dhol_citadel_bailey' in r['_zn'],
     lambda r: 'Dholavira', lambda r: f"Dholavira|{r['kind']}", False),

    ('dhol_middle_lower', 'B_zone_dholavira', 'Dholavira Middle & Lower Town vs Citadel/Bailey',
     lambda r: r['site'] == 'Dholavira' and len(r['_zn']) > 0,
     lambda r: ('dhol_middle_town' in r['_zn']) or ('dhol_lower_reservoir' in r['_zn']),
     lambda r: 'Dholavira', lambda r: f"Dholavira|{r['kind']}", False),

    ('chanhu_bead_seal_core', 'B_zone_chanhu', 'Chanhu-daro Mound II core bead/seal workshop (8C-9D) vs rest of CD',
     lambda r: r['site'] == 'Chanhu-daro' and len(r['_zn']) > 0,
     lambda r: 'chanhu_bead_seal_core' in r['_zn'],
     lambda r: 'Chanhu', lambda r: f"Chanhu|{r['kind']}", False),

    ('site_chanhu_workshops', 'B_zone_chanhu', 'Chanhu-daro craft town (Mound II bead/metal/seal workshops) vs core',
     lambda r: r['circuit'] != 'unknown',
     lambda r: r['site'] == 'Chanhu-daro',
     lambda r: r['kind'], lambda r: r['kind'], True),

    ('klb_citadel', 'B_zone_klb', 'Kalibangan Citadel (KLB-1) vs Lower Town (KLB-2)',
     lambda r: r['site'] == 'Kalibangan' and len(r['_zn']) > 0,
     lambda r: 'klb_citadel' in r['_zn'],
     lambda r: 'KLB', lambda r: f"KLB|{r['kind']}", True),

    # --- AXIS C: INTER-CITY & FOREIGN TRADE CIRCUITS ---
    ('circuit_maritime_coastal', 'C_circuit', 'Coastal/Maritime circuit (Lothal, Dholavira, Bagasra, Makran, Oman/Gulf)',
     lambda r: r['circuit'] != 'unknown',
     lambda r: r['circuit'] in ('coastal_home', 'gulf_oman'),
     lambda r: r['kind'], lambda r: r['kind'], True),

    ('circuit_gulf_oman', 'C_circuit', 'Overseas Gulf/Oman maritime circuit (Dilmun & Magan)',
     lambda r: r['circuit'] != 'unknown',
     lambda r: r['circuit'] == 'gulf_oman',
     lambda r: r['kind'], lambda r: r['kind'], True),

    ('circuit_overland_west_north', 'C_circuit', 'Overland West/North trade (Mesopotamia: Ur/Kish/Girsu/Umma, Susa, Shortughai/Gonur)',
     lambda r: r['circuit'] != 'unknown',
     lambda r: r['circuit'] == 'overland_west_north',
     lambda r: r['kind'], lambda r: r['kind'], True),

    ('circuit_all_abroad', 'C_circuit', 'All Foreign Finds (Gulf/Oman + Mesopotamia + Iran + BMAC)',
     lambda r: r['circuit'] != 'unknown',
     lambda r: r['circuit'] in ('gulf_oman', 'overland_west_north'),
     lambda r: r['kind'], lambda r: r['kind'], True),

    ('circuit_eastern_headwaters', 'C_circuit', 'Eastern Headwaters (Kalibangan, Banawali, Rakhigarhi, Karanpura, Rupar)',
     lambda r: r['circuit'] != 'unknown',
     lambda r: r['circuit'] == 'eastern_headwaters',
     lambda r: r['kind'], lambda r: r['kind'], True),

    ('circuit_riverine_core', 'C_circuit', 'Riverine Grain Core (Mohenjo-daro, Harappa, Chanhu-daro, Lower/Middle Indus)',
     lambda r: r['circuit'] != 'unknown',
     lambda r: r['circuit'] == 'riverine_core',
     lambda r: r['kind'], lambda r: r['kind'], True),
]


# ---------------- 4. Vectorized Permutation & Statistical Engine ----------------
N_SHUF = 2000
rng = np.random.default_rng(20261118)


def bh_fdr(pvals):
    """Benjamini-Hochberg FDR q-values for an array of p-values."""
    p = np.asarray(pvals, dtype=float)
    n = len(p)
    if n == 0:
        return p
    order = np.argsort(p)
    ranked = p[order]
    q = ranked * n / np.arange(1, n + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.clip(q, 0.0, 1.0)
    out = np.empty_like(q)
    out[order] = q
    return out


def permute_within_strata(y, strata, n_shuf, rng_obj):
    """Build (N_pool, n_shuf) float32 permutation matrix permuting binary y within strata."""
    M = len(y)
    Y_perm = np.zeros((M, n_shuf), dtype=np.float32)
    groups = collections.defaultdict(list)
    for idx, st in enumerate(strata):
        groups[st].append(idx)
    for st, idxs in groups.items():
        idxs_arr = np.array(idxs, dtype=int)
        sub_y = y[idxs_arr].astype(np.float32)
        k = int(sub_y.sum())
        m = len(idxs_arr)
        if k == 0 or k == m:
            if k == m:
                Y_perm[idxs_arr, :] = 1.0
            continue
        # Fast vectorized random argsort per stratum for 2,000 shuffles!
        noise = rng_obj.random((m, n_shuf), dtype=np.float32)
        top_k = np.argpartition(noise, k - 1, axis=0)[:k, :]
        cols = np.broadcast_to(np.arange(n_shuf)[None, :], (k, n_shuf))
        block = np.zeros((m, n_shuf), dtype=np.float32)
        block[top_k, cols] = 1.0
        Y_perm[idxs_arr, :] = block
    return Y_perm


def eval_domain_on_corpus(evs, X_mat, pool_fn, target_fn, stratum_fn, n_shuf=N_SHUF):
    """Evaluate all U features on a single corpus for one domain.
    Returns dict of arrays of length U (or None if target empty).
    """
    pool_idx = [i for i, r in enumerate(evs) if pool_fn(r)]
    if len(pool_idx) < 4:
        return None
    sub_evs = [evs[i] for i in pool_idx]
    y = np.array([1 if target_fn(r) else 0 for r in sub_evs], dtype=int)
    n_in = int(y.sum())
    n_pool = len(sub_evs)
    n_out = n_pool - n_in
    if n_in < 2 or n_out < 2:
        return None

    X_sub = X_mat[pool_idx, :]  # (n_pool, U)
    k_tot = X_sub.sum(axis=0).astype(int)
    k_in = (X_sub.T @ y.astype(np.float32)).round().astype(int)
    k_out = k_tot - k_in

    strata = [stratum_fn(r) for r in sub_evs]
    Y_perm = permute_within_strata(y, strata, n_shuf, rng)
    perm_hits = X_sub.T @ Y_perm  # (U, n_shuf)

    exp_shuf = perm_hits.mean(axis=1)
    sd_shuf = perm_hits.std(axis=1)
    z_shuf = (k_in - exp_shuf) / np.maximum(sd_shuf, 1e-6)
    p_shuf = (1.0 + (perm_hits >= (k_in[:, None] - 1e-5)).sum(axis=1)) / (n_shuf + 1.0)

    # Westfall-Young max-z family-wise P across primary signs+phrases in this domain
    prim_mask = np.array([f['ftype'] in ('SIGN', 'PHRASE2', 'PHRASE3') and k_tot[i] >= 3 for i, f in enumerate(features)])
    if prim_mask.any():
        perm_z = (perm_hits[prim_mask, :] - exp_shuf[prim_mask, None]) / np.maximum(sd_shuf[prim_mask, None], 1e-6)
        max_z_null = perm_z.max(axis=0)
        p_fwer = (1.0 + (max_z_null[None, :] >= (z_shuf[:, None] - 1e-6)).sum(axis=1)) / (n_shuf + 1.0)
    else:
        p_fwer = np.ones(U)

    # Distinct texts in target for each feature
    in_indices = np.where(y == 1)[0]
    distinct_in = np.zeros(U, dtype=int)
    for fi in np.where(k_in >= 1)[0]:
        hit_rows = in_indices[X_sub[in_indices, fi] > 0.5]
        distinct_in[fi] = len({sub_evs[r_i]['full_text'] for r_i in hit_rows})

    # Haldane-Anscombe odds ratio & fold enrichment
    # OR = ((a + 0.5)*(d + 0.5)) / ((b + 0.5)*(c + 0.5)) where a=k_in, b=n_in-k_in, c=k_out, d=n_out-k_out
    a = k_in.astype(float)
    b = (n_in - k_in).astype(float)
    c = k_out.astype(float)
    d_cnt = (n_out - k_out).astype(float)
    odds = ((a + 0.5) * (d_cnt + 0.5)) / ((b + 0.5) * (c + 0.5))
    rate_in = a / max(n_in, 1)
    rate_pool = k_tot.astype(float) / max(n_pool, 1)
    fold = np.where(rate_pool > 0, rate_in / np.maximum(rate_pool, 1e-9), 0.0)

    # Exact Fisher P for features with k_in >= 2 (fast: only a few hundred per domain)
    p_fisher = np.ones(U, dtype=float)
    for fi in np.where(k_in >= 2)[0]:
        p_fisher[fi] = fisher_exact([[int(k_in[fi]), int(n_in - k_in[fi])],
                                     [int(k_out[fi]), int(n_out - k_out[fi])]],
                                    alternative='greater')[1]

    return dict(
        n_in=n_in, n_out=n_out, n_pool=n_pool,
        k_in=k_in, k_out=k_out, k_tot=k_tot,
        distinct_in=distinct_in,
        fold=fold, odds=odds, p_fisher=p_fisher,
        exp_shuf=exp_shuf, sd_shuf=sd_shuf, z_shuf=z_shuf, p_shuf=p_shuf, p_fwer=p_fwer,
        sub_evs=sub_evs, X_sub=X_sub, y=y
    )


def eval_distinct_text_rival(sub_evs, X_sub, y, fi):
    """Rival check: collapse identical full inscriptions across the entire domain pool to 1 vote each
    (keeps target=1 if the text ever occurs in the target domain, else 0) and compute Fisher P."""
    txt_in = {}
    for idx, r in enumerate(sub_evs):
        ft = r['full_text']
        has_f = bool(X_sub[idx, fi] > 0.5)
        in_t = bool(y[idx] == 1)
        if ft not in txt_in:
            txt_in[ft] = [has_f, in_t]
        else:
            txt_in[ft][0] = txt_in[ft][0] or has_f
            txt_in[ft][1] = txt_in[ft][1] or in_t
    vals = list(txt_in.values())
    a = sum(1 for h, t in vals if h and t)
    b = sum(1 for h, t in vals if (not h) and t)
    c = sum(1 for h, t in vals if h and (not t))
    d_c = sum(1 for h, t in vals if (not h) and (not t))
    if a + b == 0 or c + d_c == 0:
        return a, a + b, 1.0
    p = fisher_exact([[a, b], [c, d_c]], alternative='greater')[1]
    return a, a + b, float(p)


# ---------------- 5. Run Full Sweep + Rival Controls + Held-Out Replication ----------------
def main():
    all_rows = []
    domain_summaries = []

    log(f'Running 2,000 stratum-aware shuffles across {len(DOMAINS)} domains ...')
    for dom_id, axis, dom_label, pool_fn, target_fn, strat_fn, rival_strat_fn, has_new in DOMAINS:
        res_L = eval_domain_on_corpus(ev_lipi, X_lipi, pool_fn, target_fn, strat_fn, n_shuf=N_SHUF)
        if res_L is None:
            log(f'  [SKIP] {dom_id}: too few target events in Lipi.')
            continue

        # Finer rival-stratum shuffle when rival_strat_fn differs
        res_rival_strat = eval_domain_on_corpus(ev_lipi, X_lipi, pool_fn, target_fn, rival_strat_fn, n_shuf=N_SHUF)

        # Held-out Mahadevan `new texts` replication (and full Mahadevan where new_texts is tiny)
        res_N = eval_domain_on_corpus(ev_new, X_new, pool_fn, target_fn, strat_fn, n_shuf=N_SHUF) if has_new else None
        res_M = eval_domain_on_corpus(ev_mall, X_mall, pool_fn, target_fn, strat_fn, n_shuf=500) if has_new else None

        # Compute within-domain BH FDR separately for primary (SIGN+PHRASE) and SLOT_SIGN features tested (k_tot >= 3)
        tested_prim = np.array([f['ftype'] in ('SIGN', 'PHRASE2', 'PHRASE3') and res_L['k_tot'][i] >= 3 for i, f in enumerate(features)])
        q_dom = np.ones(U, dtype=float)
        if tested_prim.any():
            q_dom[tested_prim] = bh_fdr(res_L['p_shuf'][tested_prim])
        tested_slot = np.array([f['ftype'] == 'SLOT_SIGN' and res_L['k_tot'][i] >= 3 for i, f in enumerate(features)])
        if tested_slot.any():
            q_dom[tested_slot] = bh_fdr(res_L['p_shuf'][tested_slot])

        n_hits_dom = 0
        n_rep_dom = 0
        for fi, f in enumerate(features):
            kt = int(res_L['k_tot'][fi])
            ki = int(res_L['k_in'][fi])
            if kt < 3 or ki < 2:
                continue
            ps = float(res_L['p_shuf'][fi])
            pf = float(res_L['p_fisher'][fi])
            if ps > 0.10 and pf > 0.05:
                continue

            # Strongest rival checks
            dt_k, dt_n, dt_p = eval_distinct_text_rival(res_L['sub_evs'], res_L['X_sub'], res_L['y'], fi)
            p_riv_strat = float(res_rival_strat['p_shuf'][fi]) if res_rival_strat is not None else ps

            # Held-out Mahadevan new-texts stats
            nk_in = nk_tot = nn_in = nn_pool = 0
            n_fold = n_odds = np.nan
            np_fish = np_shuf = np.nan
            replicated_new = False
            if res_N is not None and int(res_N['k_tot'][fi]) >= 1:
                nk_in = int(res_N['k_in'][fi])
                nk_tot = int(res_N['k_tot'][fi])
                nn_in = int(res_N['n_in'])
                nn_pool = int(res_N['n_pool'])
                n_fold = float(res_N['fold'][fi])
                n_odds = float(res_N['odds'][fi])
                nk_out = int(res_N['k_out'][fi])
                nn_out = int(res_N['n_out'])
                np_fish = float(fisher_exact([[nk_in, nn_in - nk_in], [nk_out, nn_out - nk_out]], alternative='greater')[1]) if nk_in >= 1 else 1.0
                np_shuf = float(res_N['p_shuf'][fi])
                replicated_new = (nk_in >= 1 and n_fold > 1.25 and (np_fish <= 0.10 or np_shuf <= 0.10))

            # Full Mahadevan backup stats (for rare classes like copper tools / copper animals where new_texts has <2 objects)
            mk_in = mk_tot = 0
            m_fold = mp_fish = np.nan
            if res_M is not None and int(res_M['k_tot'][fi]) >= 1:
                mk_in = int(res_M['k_in'][fi])
                mk_tot = int(res_M['k_tot'][fi])
                m_fold = float(res_M['fold'][fi])
                mk_out = int(res_M['k_out'][fi])
                mn_in, mn_out = int(res_M['n_in']), int(res_M['n_out'])
                mp_fish = float(fisher_exact([[mk_in, mn_in - mk_in], [mk_out, mn_out - mk_out]], alternative='greater')[1]) if mk_in >= 1 else 1.0

            if ps <= 0.05 and f['ftype'] != 'SLOT_SIGN':
                n_hits_dom += 1
                if replicated_new:
                    n_rep_dom += 1

            all_rows.append(dict(
                domain=dom_id,
                axis=axis,
                domain_label=dom_label,
                fid=f['fid'],
                ftype=f['ftype'],
                unit=f['unit'],
                slot=f['slot'],
                v2_class=v2_of.get(f['unit'], 'PHRASE'),
                shape_desc=shape_of.get(f['unit'], ''),
                lipi_k_in=ki,
                lipi_n_in=int(res_L['n_in']),
                lipi_k_tot=kt,
                lipi_n_pool=int(res_L['n_pool']),
                lipi_distinct_texts_in=int(res_L['distinct_in'][fi]),
                lipi_fold=round(float(res_L['fold'][fi]), 3),
                lipi_odds=round(float(res_L['odds'][fi]), 3),
                lipi_p_fisher=float(pf),
                lipi_exp_shuf=round(float(res_L['exp_shuf'][fi]), 3),
                lipi_z_shuf=round(float(res_L['z_shuf'][fi]), 3),
                lipi_p_shuf=float(ps),
                lipi_q_fdr_dom=float(q_dom[fi]),
                lipi_p_fwer_dom=float(res_L['p_fwer'][fi]),
                rival_distinct_k=dt_k,
                rival_distinct_p=round(dt_p, 5),
                rival_strat_p=round(p_riv_strat, 5),
                new_k_in=nk_in,
                new_n_in=nn_in,
                new_k_tot=nk_tot,
                new_n_pool=nn_pool,
                new_fold=round(n_fold, 3) if pd.notna(n_fold) else '',
                new_odds=round(n_odds, 3) if pd.notna(n_odds) else '',
                new_p_fisher=round(np_fish, 6) if pd.notna(np_fish) else '',
                new_p_shuf=round(np_shuf, 5) if pd.notna(np_shuf) else '',
                replicated_new=replicated_new,
                mah_all_k_in=mk_in,
                mah_all_k_tot=mk_tot,
                mah_all_fold=round(m_fold, 3) if pd.notna(m_fold) else '',
                mah_all_p_fisher=round(mp_fish, 6) if pd.notna(mp_fish) else '',
            ))

        domain_summaries.append(dict(
            domain=dom_id, axis=axis, label=dom_label,
            lipi_n_in=int(res_L['n_in']), lipi_n_pool=int(res_L['n_pool']),
            new_n_in=int(res_N['n_in']) if res_N else 0,
            primary_hits_p05=n_hits_dom,
            replicated_new_hits=n_rep_dom,
        ))

    res_df = pd.DataFrame(all_rows)
    res_df = res_df.sort_values(['lipi_p_shuf', 'lipi_z_shuf'], ascending=[True, False]).reset_index(drop=True)
    res_df.to_csv(os.path.join(OUT, 'sweep_all_hits.csv'), index=False)
    pd.DataFrame(domain_summaries).to_csv(os.path.join(OUT, 'domain_summary.csv'), index=False)

    # ---------------- 6. Detect Slot-Specific Redesign Rescues! ----------------
    any_lookup = {}
    for _, r in res_df[res_df.ftype == 'SIGN'].iterrows():
        any_lookup[(r['domain'], r['unit'])] = r

    rescues = []
    for _, r in res_df[(res_df.ftype == 'SLOT_SIGN') & (res_df.lipi_p_shuf <= 0.05)].iterrows():
        base = any_lookup.get((r['domain'], r['unit']))
        base_p = float(base['lipi_p_shuf']) if base is not None else 1.0
        base_fold = float(base['lipi_fold']) if base is not None else 1.0
        if base_p > 0.05 or float(r['lipi_fold']) >= 1.5 * base_fold:
            rescues.append(dict(
                domain=r['domain'],
                domain_label=r['domain_label'],
                sign=r['unit'],
                rescued_slot=r['slot'],
                any_p_shuf=round(base_p, 5),
                any_fold=round(base_fold, 3),
                slot_k_in=r['lipi_k_in'],
                slot_k_tot=r['lipi_k_tot'],
                slot_fold=r['lipi_fold'],
                slot_odds=r['lipi_odds'],
                slot_z_shuf=r['lipi_z_shuf'],
                slot_p_shuf=r['lipi_p_shuf'],
                new_k_in=r['new_k_in'],
                new_k_tot=r['new_k_tot'],
                new_fold=r['new_fold'],
                new_p_fisher=r['new_p_fisher'],
                replicated_new=r['replicated_new'],
            ))

    rescue_df = pd.DataFrame(rescues).sort_values(['slot_p_shuf', 'slot_z_shuf'], ascending=[True, False])
    rescue_df.to_csv(os.path.join(OUT, 'slot_redesign_rescues.csv'), index=False)

    prim = res_df[res_df.ftype.isin(['SIGN', 'PHRASE2', 'PHRASE3'])]
    log(f'Sweep complete! Saved {len(res_df)} candidate rows to work_data/sem/sweep_all_hits.csv')
    log(f'Primary (SIGN + PHRASE) hits at shuffle P <= 0.05: {(prim.lipi_p_shuf <= 0.05).sum()} '
        f'(signs={(prim[prim.ftype=="SIGN"].lipi_p_shuf <= 0.05).sum()}, '
        f'phrases={(prim[prim.ftype!="SIGN"].lipi_p_shuf <= 0.05).sum()})')
    log(f'Surviving within-domain FDR q <= 0.05: {(prim.lipi_q_fdr_dom <= 0.05).sum()} | '
        f'Westfall-Young FWER P <= 0.05: {(prim.lipi_p_fwer_dom <= 0.05).sum()}')
    log(f'Replicated on strictly held-out Mahadevan new texts: '
        f'{prim[prim.lipi_p_shuf <= 0.05].replicated_new.sum()} primary associations!')
    log(f'Slot-specific redesign rescues (unmasked when split by slot): {len(rescue_df)} '
        f'(strictly missed at ANY-slot P>0.05 -> rescued at slot P<=0.05: {(rescue_df.any_p_shuf > 0.05).sum()})')


if __name__ == '__main__':
    main()

