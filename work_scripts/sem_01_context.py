#!/usr/bin/env python3
"""sem_01_context.py -- Build unified archaeological & physical object-context tables.

Joins:
  1. Lipi (research/data/open_prototype/lipi/metadata_filtered.csv, db/ivc.sqlite, work_data/sign_shapes.csv)
  2. Mahadevan (work_data/mahadevan_parsed.csv, research/data/mahadevan_20260905/concordance_rows.csv,
     work_data/lipi_mahadevan_crosswalk.csv, work_data/crosswalk_text_pairs.csv)
  3. Sealing reverse types (work_data/stamps/objects.csv, work_data/stamps/backs_seen.csv)
  4. Copper-tablet animal faces (work_data/copper/objects.csv, work_data/copper/m77_objects.csv)
  5. Spatial/excavation coordinates & time bins (work_data/spots/s3_objects.csv, work_data/time/time_axis.csv,
     work_scripts/recheck_common.py)

Enforces strict counting discipline:
  - One row per physical object (stone_map merges multi-face & duplicate catalogue rows).
  - Moulded copy batch = 1 event (same site + same known findspot + same full text across faces = 1 event).
  - Strictly held-out Mahadevan `new texts` (1,183 unpartnered lines -> 990 physical copy-events).
"""
import os
import re
import sys
import json
import sqlite3
import io
import contextlib
import collections
import numpy as np
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

with contextlib.redirect_stdout(io.StringIO()):
    from v2_common import d as lipi_d, M as mah_M, SHORT, TALL, VAL, FISH, PORTER
from recheck_common import stone_map, EMPTY

OUT = os.path.join(ROOT, 'work_data', 'sem')
os.makedirs(OUT, exist_ok=True)


def log(*args):
    print('[sem_01]', *args, flush=True)


def clean_str(v):
    s = str(v).strip() if v is not None else ''
    return '' if s in EMPTY or s in ('nan', 'None') else s.strip('-').strip()


def known_spot(v):
    s = str(v).strip() if v is not None else ''
    return s not in EMPTY and s not in ('nan', 'None', '')


def parse_ft(s):
    m = re.search(r'(-?\d+(?:\.\d+)?)\s*ft', str(s))
    if m:
        return abs(float(m.group(1)))
    m = re.search(r'(-?\d+(?:\.\d+)?)\s*cm', str(s))
    if m:
        return abs(float(m.group(1))) / 30.48
    m = re.search(r'(-?\d+(?:\.\d+)?)\s*m\b', str(s))
    if m:
        return abs(float(m.group(1))) * 3.281
    return np.nan


# ---------------- 1. Sign metadata & Frame v2 classes ----------------
log('Loading sign metadata from SQLite, sign_shapes.csv, crosswalk, and classes_v2.csv ...')
shapes_df = pd.read_csv(os.path.join(ROOT, 'work_data', 'sign_shapes.csv'), dtype=str).fillna('')
shape_map = dict(zip(shapes_df.lipi_wells_number, shapes_df.shape_description))
mayig_map = dict(zip(shapes_df.lipi_wells_number, shapes_df.mayig_code))

cw_df = pd.read_csv(os.path.join(ROOT, 'work_data', 'lipi_mahadevan_crosswalk.csv'), dtype=str).fillna('')
cw_top = cw_df[cw_df.rank_for_lipi_sign == '1']
mah_code_map = dict(zip(cw_top.lipi, cw_top.mahadevan))

c2_df = pd.read_csv(os.path.join(ROOT, 'work_data', 'frame', 'classes_v2.csv'), dtype=str).fillna('')
v2_map = dict(zip(c2_df.sign, c2_df.v2_base))
v2_map['706'] = 'MEASURE'

con = sqlite3.connect(os.path.join(ROOT, 'db', 'ivc.sqlite'))
sql_signs = pd.read_sql("SELECT system_id, normalized_id, description FROM sign WHERE description IS NOT NULL AND description != ''", con)
p_desc_map = dict(zip(
    sql_signs[sql_signs.system_id == 'mayig_p'].normalized_id,
    sql_signs[sql_signs.system_id == 'mayig_p'].description
))
sql_wit_cnt = con.execute("SELECT count(*) FROM witness WHERE system_id='lipi_numeric'").fetchone()[0]
con.close()
log(f'SQLite verified: {sql_wit_cnt} lipi_numeric witnesses, {len(p_desc_map)} Mayig P descriptions.')

OPEN_SET = {'820', '861', '817', '920', '692', '880', '824', '545', '091', '550', '360', '556', '317', '413'}
SLOT_SET = {'002', '060', '741', '742', '745', '368', '365'}
NUM_SET = set(VAL.keys()) | SHORT | TALL | {f'{i:03d}' for i in range(465, 476)} | {'055'}
MEASURE_SET = {s for s, c in v2_map.items() if c == 'MEASURE'} | {'700', '705', '706', '711', '171', '575', '540', '320'}
CLOSER_SET = {s for s, c in v2_map.items() if c == 'CLOSER'} | {'740', '520'} | PORTER
TITLE_SET = {s for s, c in v2_map.items() if c == 'TITLE'} | {'400', '090', '679', '565', '527', '621', '161', '241'}
SIGN_RE = re.compile(r'^\d{3}$')


def is_clean_sign(s):
    return bool(SIGN_RE.match(s)) and s != '000'


def parse_contextual_slots(tok):
    """Assign each token index on a face its syntactic slot(s) purely from structural position:
      - SOLO: single-sign face (commodity/pot mark, picture-replacing sign)
      - FRONT: opening header field/slot ([OPEN][SLOT] or [any][SLOT] at text start)
      - COUNTED: non-number sign directly quantified by a number (before it, or after a MEASURE/700),
                 excluding fixed tall/short 2 before a fish crest inside a jar-closed name
      - ENDING: text-final CLOSER or TITLE (or 740 immediately before a final TITLE)
      - NAME: name-body sign (between FRONT and ENDING, not part of a count-line),
              plus sub-tags NAME_CREST (first sign of name span) and PRE_CLOSER (immediately before CLOSER)
      - NUM: numeral token
    Returns list of primary slot strings (same length as tok) and dict slot_tag -> set of signs on this face.
    """
    L = len(tok)
    slots = ['OTHER'] * L
    tags = collections.defaultdict(set)
    if L == 0:
        return slots, tags
    if L == 1:
        s = tok[0]
        if is_clean_sign(s):
            slots[0] = 'NUM' if s in NUM_SET else 'SOLO'
            tags[slots[0]].add(s)
            if s not in NUM_SET:
                tags['GOODS_OR_SOLO'].add(s)
        return slots, tags

    # Identify FRONT span
    front_end = 0
    if L >= 3 and tok[1] in SLOT_SET:
        front_end = 2
    elif L >= 4 and tok[0] in OPEN_SET and tok[2] in SLOT_SET:
        front_end = 3
    elif tok[0] in OPEN_SET:
        front_end = 1
    for i in range(front_end):
        slots[i] = 'FRONT'

    # Identify ENDING span
    end_start = L
    if tok[L - 1] in (CLOSER_SET | TITLE_SET):
        end_start = L - 1
        if L >= 2 and tok[L - 1] in TITLE_SET and tok[L - 2] in CLOSER_SET:
            end_start = L - 2
    for i in range(end_start, L):
        if i >= front_end:
            slots[i] = 'ENDING'

    has_closer = end_start < L
    # Identify COUNTED & NUM inside body
    counted_idx = set()
    num_idx = set()
    for i in range(front_end, end_start):
        s = tok[i]
        if s in NUM_SET:
            # Check if this is 032 or 002 right before a FISH crest inside a closed name
            if has_closer and s in ('032', '002') and (i + 1 < end_start) and (tok[i + 1] in FISH):
                continue
            num_idx.add(i)

    for i in range(front_end, end_start):
        s = tok[i]
        if i in num_idx or not is_clean_sign(s):
            continue
        prev_num = (i - 1 >= front_end) and (i - 1 in num_idx)
        next_num = (i + 1 < end_start) and (i + 1 in num_idx) and (s in MEASURE_SET)
        # Also handle [NUM][MEASURE][COUNTED_THING] or [MEASURE][NUM][THING]
        if prev_num or next_num:
            counted_idx.add(i)

    for i in num_idx:
        slots[i] = 'NUM'
    for i in counted_idx:
        slots[i] = 'COUNTED'

    # Remaining body positions are NAME
    name_indices = [i for i in range(front_end, end_start) if slots[i] == 'OTHER']
    for i in name_indices:
        slots[i] = 'NAME'

    # Populate tag sets for clean signs
    for i, s in enumerate(tok):
        if not is_clean_sign(s):
            continue
        sl = slots[i]
        tags[sl].add(s)
        if sl in ('COUNTED', 'SOLO'):
            tags['GOODS_OR_SOLO'].add(s)
        if sl == 'NAME':
            if name_indices and i == name_indices[0] and has_closer:
                tags['NAME_CREST'].add(s)
            if i + 1 < L and tok[i + 1] in CLOSER_SET:
                tags['PRE_CLOSER'].add(s)
    return slots, tags


def extract_phrases_2(faces):
    """Extract all contiguous 2-sign and 3-sign clean runs across faces of an object."""
    p2, p3 = set(), set()
    for tok in faces:
        cur = []
        for s in tok:
            if is_clean_sign(s):
                cur.append(s)
            else:
                for i in range(len(cur) - 1):
                    p2.add(f'{cur[i]}-{cur[i+1]}')
                for i in range(len(cur) - 2):
                    p3.add(f'{cur[i]}-{cur[i+1]}-{cur[i+2]}')
                cur = []
        for i in range(len(cur) - 1):
            p2.add(f'{cur[i]}-{cur[i+1]}')
        for i in range(len(cur) - 2):
            p3.add(f'{cur[i]}-{cur[i+1]}-{cur[i+2]}')
    return sorted(p2), sorted(p3)


# ---------------- 2. Spatial & Trade Circuit Classifiers ----------------
COASTAL_HOME_SITES = {
    'Lothal', 'Dholavira', 'Gola Dhoro (Bagasra)', 'Shikarpur', 'Kanmer', 'Surkotada',
    'Desalpur', 'Khirsara', 'Rodji', 'Pabumath', 'Juna Khatiya', 'Bala-kot',
    'Sutkagen-dor', 'Sotka-koh', 'Miri Qalat'
}
GULF_OMAN_SITES = {
    "Ra's al-Junayz", 'Salut', 'Karzakan', "Qala'at al-Bahrain", 'Saar',
    'Janabiyah', 'Hajar', 'Failaka', 'Kalba'
}
OVERLAND_WEST_NORTH_SITES = {
    'Shortughai', 'Gonur Depe', 'Altyn Depe', 'Susa', 'Tepe Yahya', 'Luristan',
    'Ur', 'Kish', 'Girsu', 'Tello', 'Tell Umma', 'Nippur', 'Sibri', 'Nindowari-damb',
    'Ornach area', 'Murda Sang'
}
EASTERN_HEADWATERS_SITES = {
    'Kalibangan', 'Banawali', 'Rakhigarhi', 'Farmana', 'Bhirrana', 'Karanpura',
    'Rupar', 'Alamgirpur', 'Chandigarh', 'Hulas', 'Baror', 'Tarkhanewala-dera', 'Tigrana'
}
RIVERINE_CORE_SITES = {
    'Mohenjo-daro', 'Harappa', 'Chanhu-daro', 'Lakhanjo-daro', 'Allahdino', 'Kot-Diji',
    'Amri', 'Nausharo', 'Ganweriwala', 'Nuhato', 'Naru-Waro-dharo', 'Gumla',
    'Rahman-deri', 'Hissam-dheri', 'Lohumjo-daro', 'Jhukar', 'Pirak', 'Bakkar Buthi',
    'Gharo Bhiro', 'Wattoowala', 'Rajanpur', 'Rappwala Ther', 'Guddal A', 'Derawar Ther'
}


def classify_circuit(site, region=''):
    if site in GULF_OMAN_SITES or region == 'Persian Gulf':
        return 'gulf_oman'
    if site in OVERLAND_WEST_NORTH_SITES or region in ('Mesopotamia', 'Iranian Plateau', 'Central Asia'):
        return 'overland_west_north'
    if site in COASTAL_HOME_SITES or region == 'Gujarat/Kutch':
        return 'coastal_home'
    if site in EASTERN_HEADWATERS_SITES or region == 'Eastern Headwaters':
        return 'eastern_headwaters'
    if site in RIVERINE_CORE_SITES or region in ('Lower Indus', 'Inter-Riverine', 'Upper Indus'):
        return 'riverine_core'
    return 'unknown'


def classify_lipi_zone(site, area_raw, bh_raw, rg_raw):
    """Map intra-city excavation coordinates to functional archaeological zones."""
    a = str(area_raw).strip()
    rg = str(rg_raw).strip()
    zones = []
    if site == 'Harappa':
        if a in ('', '--', '-'):
            return zones
        if a.startswith('F'):
            zones.append('har_mound_F')
            if 'Gran' in a:
                zones.append('har_F_granary')
            elif a in ('FTrench I', 'FTrench IV+V'):
                zones.append('har_F_platforms_quarters')
        elif a.startswith('E'):
            zones.append('har_mound_E')
        elif a.startswith('AB'):
            zones.append('har_mound_AB')
        elif a[0] in ('D', 'G', 'H', 'J'):
            zones.append('har_area_DGH')
    elif site == 'Mohenjo-daro':
        if a in ('', '--', '-'):
            return zones
        if a.startswith('SD') or a.startswith('L'):
            zones.append('md_citadel')
        elif a.startswith('HR'):
            zones.append('md_HR_elite')
        elif a == 'DKG. (S)':
            zones.append('md_DKG_south')
        elif a == 'DKG. (N)':
            zones.append('md_DKG_north')
        elif a.startswith('VS') or a.startswith('MN'):
            zones.append('md_VS_MN_craft')
            if a.startswith('VS'):
                zones.append('md_VS_dyers')
            if a.startswith('MN'):
                zones.append('md_MN_moneer')
        elif a.startswith('DK'):
            zones.append('md_DK_other')
    elif site == 'Lothal':
        if '3GX 10' in a or 'GX 10' in a or '3FX 10' in a or 'GX 10' in rg:
            zones.append('lothal_warehouse')
        elif a not in ('', '--', '-'):
            zones.append('lothal_town_dock_bead')
            if a.startswith('SRG 2E') or a.startswith('SRG 2C') or a.startswith('SRG 1'):
                zones.append('lothal_bead_lower')
            elif a.startswith('SRG 2B') or a.startswith('SRG 3') or a.startswith('SRG 2A'):
                zones.append('lothal_acropolis_res')
    elif site == 'Dholavira':
        al = a.lower()
        if 'castle' in al or 'bailey' in al or 'citadel' in al:
            zones.append('dhol_citadel_bailey')
        elif 'middle town' in al:
            zones.append('dhol_middle_town')
        elif 'lower town' in al or 'reservoir' in al or 'annexe' in al:
            zones.append('dhol_lower_reservoir')
    elif site == 'Chanhu-daro':
        if 'Mound I-' in a or '12/K' in rg or '13/J' in rg:
            zones.append('chanhu_mound1')
        elif 'Mound II' in a or any(sq in rg for sq in ('6/F', '7/C', '7/E', '7/F', '8/B', '8/C', '8/D', '8/E', '8/F', '9/C', '9/D', '9/E', '10/E', '10/F')):
            zones.append('chanhu_mound2_workshops')
            if any(sq in rg for sq in ('8/C', '8/D', '9/C', '9/D')):
                zones.append('chanhu_bead_seal_core')
    elif site == 'Kalibangan':
        if 'KLB-1' in a:
            zones.append('klb_citadel')
        elif 'KLB-2' in a:
            zones.append('klb_lower_town')
    return zones


# ---------------- 3. Build Lipi Physical Objects & Copy Events ----------------
log('Building Lipi physical objects (stone_map) and merging stamps, copper animals, and spots ...')
raw_meta = pd.read_csv(os.path.join(ROOT, 'research', 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv'),
                       dtype=str, keep_default_na=False)
meta_by_id = raw_meta.set_index('id').to_dict(orient='index')

f2s, merges = stone_map()
lipi_d = lipi_d.copy()
lipi_d['stone'] = lipi_d.id.map(f2s)

# Load auxiliary tables
copper_obj = pd.read_csv(os.path.join(ROOT, 'work_data', 'copper', 'objects.csv'), dtype=str).fillna('')
copper_by_obj = copper_obj.set_index('obj').to_dict(orient='index')
copper_by_cisi = {r['cisi']: r for _, r in copper_obj.iterrows() if r['cisi'] not in ('', '-')}

backs_df = pd.read_csv(os.path.join(ROOT, 'work_data', 'stamps', 'backs_seen.csv'), dtype=str).fillna('')
backs_by_cisi = dict(zip(backs_df.cisi, backs_df.back))

ta_df = pd.read_csv(os.path.join(ROOT, 'work_data', 'time', 'time_axis.csv'), dtype=str).fillna('')
tbin_by_obj = dict(zip(ta_df.obj, ta_df.bin))


def norm_copper_animal(pic_str, cat_str=''):
    p = str(pic_str).strip().lower()
    if not p:
        c = str(cat_str).strip()
        cmap = {'Hare': 'hare', 'Elep': 'elephant', 'Anth': 'human_archer', 'Comp': 'composite',
                'Gaur': 'bull_gaur', 'Goat': 'goat_antelope', 'Loop': 'knot', 'Bull1': 'unicorn',
                'Rhin': 'rhinoceros', 'Tigr': 'tiger', 'Bull': 'bull_gaur', 'Buff': 'buffalo'}
        return cmap.get(c, '')
    if p.startswith('sign '):
        return 'picsign'
    if 'no picture' in p:
        return 'two_sided_text'
    if 'elephant' in p:
        return 'elephant'
    if 'hare' in p:
        return 'hare'
    if 'human' in p or 'archer' in p:
        return 'human_archer'
    if 'goat' in p or 'stag' in p or 'striped horned' in p:
        return 'goat_antelope'
    if 'rhino' in p:
        return 'rhinoceros'
    if 'gaur' in p or 'bull' in p:
        return 'bull_gaur'
    if 'unicorn' in p:
        return 'unicorn'
    if 'buffalo' in p:
        return 'buffalo'
    if 'tiger' in p:
        return 'tiger'
    if 'composite' in p or 'marked-body' in p:
        return 'composite'
    if 'knot' in p or 'loop' in p:
        return 'knot'
    if 'gharial' in p or 'croc' in p:
        return 'gharial'
    return 'other_quadruped'


def kind_lipi(t):
    t = str(t)
    if t.startswith('SEAL'):
        return 'seal'
    if t.startswith('TAG'):
        return 'tag'
    if t.startswith('PO'):
        return 'pot'
    if t == 'IMPL':
        return 'tool'
    if t == 'BNGL':
        return 'bangle'
    if t == 'ROD':
        return 'rod'
    if t == 'TAB:C':
        return 'ctab'
    if t in ('TAB:B', 'TAB:I'):
        return 'mtab'
    return 'other'


lipi_stones = []
for st, g in lipi_d.groupby('stone', sort=False):
    g = g.sort_values('id')
    first_id = g.iloc[0].id
    m = meta_by_id[first_id]
    site = m['site']
    region = m['region']
    typ = m['type']
    knd = kind_lipi(typ)
    mat = m['material'].strip()
    shp = m['shape'].strip()
    sides = m['sides'].strip()
    cisi = m['cisi'].strip()
    area_raw = m['area-section']
    bh_raw = m['block-house']
    rg_raw = m['room-grid']
    h_mm = pd.to_numeric(m['horizontal(mm)'], errors='coerce')
    v_mm = pd.to_numeric(m['vertical(mm)'], errors='coerce')
    th_mm = pd.to_numeric(m['thickness(mm)'], errors='coerce')
    area_mm2 = float(h_mm * v_mm) if (pd.notna(h_mm) and pd.notna(v_mm) and h_mm > 0 and v_mm > 0) else np.nan

    faces = [list(t) for t in g.tok]
    full_sig = '|'.join(sorted('-'.join(f) for f in faces))

    # Copper animal lookup
    c_rec = copper_by_obj.get(str(st)) or copper_by_cisi.get(cisi)
    ctab_anim = ''
    ctab_picsign = ''
    if knd == 'ctab':
        if c_rec:
            ctab_anim = norm_copper_animal(c_rec.get('pic', ''), c_rec.get('cat', ''))
            ctab_picsign = c_rec.get('picsign', '')
        else:
            ctab_anim = norm_copper_animal('', m['symbol'].split(':')[0])

    # Tag reverse subtype
    tag_rev = ''
    if knd == 'tag':
        tag_rev = typ.split(':', 1)[1] if ':' in typ else 'PLAIN'
    back_note = backs_by_cisi.get(cisi, '')

    # Intra-city zones & trade circuit
    zones = classify_lipi_zone(site, area_raw, bh_raw, rg_raw)
    circuit = classify_circuit(site, region)

    # Medium & function subtype flags
    subtypes = []
    if knd == 'tool' and mat.lower() in ('copper', 'bronze', 'metal'):
        subtypes.append('copper_tool')
    if knd == 'ctab':
        subtypes.append('copper_tablet')
        if ctab_anim:
            subtypes.append(f'ctab_{ctab_anim}')
    if knd == 'bangle':
        subtypes.append('bangle_all')
        if mat.lower() == 'stoneware':
            subtypes.append('bangle_stoneware')
        else:
            subtypes.append('bangle_other_mat')
    if knd == 'rod':
        subtypes.append('ivory_bone_rod')
    if knd == 'tag':
        subtypes.append('tag_all')
        if tag_rev == 'B':
            subtypes.append('tag_B_box')
        elif tag_rev in ('P', 'PC'):
            subtypes.append('tag_P_token')
        elif tag_rev == 'L':
            subtypes.append('tag_L_bale')
        elif tag_rev == 'R':
            subtypes.append('tag_R_jarmouth')
        elif tag_rev == 'O':
            subtypes.append('tag_O_cane')
        elif tag_rev == 'W':
            subtypes.append('tag_W_peg')
    if knd == 'pot' or tag_rev == 'R':
        if knd == 'pot':
            subtypes.append('pot_all')
        if typ in ('POT:T:s', 'POT:T:S'):
            subtypes.append('pot_small_stamped')
        if tag_rev == 'R' or typ == 'POT:M' or (knd == 'pot' and ((pd.notna(h_mm) and h_mm >= 90) or (pd.notna(v_mm) and v_mm >= 80) or (pd.notna(th_mm) and th_mm >= 10))):
            subtypes.append('pot_storage_jar')
        if typ in ('POT:T:g', 'POsT:T:g'):
            subtypes.append('pot_graffito')
        if typ == 'POT:T:p':
            subtypes.append('pot_painted')
    if knd == 'mtab':
        subtypes.append('mtab_all')
        if shp in ('prism', 'triangular') or sides in ('3', '4'):
            subtypes.append('tab_prism')
        else:
            subtypes.append('tab_flat_chit')
        if typ == 'TAB:B':
            subtypes.append('tab_moulded')
        elif typ == 'TAB:I':
            subtypes.append('tab_incised')
    if knd == 'seal':
        subtypes.append('seal_all')
        if typ in ('SEAL:C', 'SEAL:CY'):
            subtypes.append('seal_round_cyl')
        if typ == 'SEAL:R':
            subtypes.append('seal_bar_rect')
        if pd.notna(area_mm2):
            if area_mm2 >= 1190.0:
                subtypes.append('seal_giant')
            elif area_mm2 <= 365.0:
                subtypes.append('seal_tiny')

    # Contextual slots & 2-sign phrases across all faces of this object
    obj_slot_signs = collections.defaultdict(set)
    face_slots_list = []
    all_clean_signs = set()
    for f in faces:
        sl_list, tg = parse_contextual_slots(f)
        face_slots_list.append(sl_list)
        for s in f:
            if is_clean_sign(s):
                all_clean_signs.add(s)
        for k_sl, sset in tg.items():
            obj_slot_signs[k_sl] |= sset
    p2, p3 = extract_phrases_2(faces)

    # Copy-event key (exact sense_corpus.py convention!)
    if known_spot(area_raw) or known_spot(bh_raw) or known_spot(rg_raw):
        ev_key = ('L', site, area_raw, bh_raw, rg_raw, full_sig)
    else:
        ev_key = ('L', 'stone', str(st))

    sym_parts = m['symbol'].strip().split(':', 1) if m['symbol'].strip() not in ('', '-') else ['']
    seal_anim = sym_parts[0]
    stand_code = sym_parts[1] if len(sym_parts) > 1 else ''

    lipi_stones.append(dict(
        stone_id=str(st),
        cisi=cisi,
        site=site,
        region=region,
        circuit=circuit,
        area_raw=area_raw,
        bh_raw=bh_raw,
        rg_raw=rg_raw,
        zones='|'.join(zones),
        type_raw=typ,
        kind=knd,
        material=mat,
        shape=shp,
        sides=sides,
        area_mm2=round(area_mm2, 2) if pd.notna(area_mm2) else '',
        depth_ft=round(parse_ft(m['depth']), 2) if pd.notna(parse_ft(m['depth'])) else '',
        time_bin=tbin_by_obj.get(str(st), ''),
        seal_animal=seal_anim,
        stand_code=stand_code,
        tag_reverse=tag_rev,
        back_note=back_note,
        ctab_animal=ctab_anim,
        ctab_picsign=ctab_picsign,
        subtypes='|'.join(subtypes),
        n_faces=len(faces),
        full_text=full_sig,
        signs='|'.join(sorted(all_clean_signs)),
        phrases2='|'.join(p2),
        phrases3='|'.join(p3),
        ev_key=str(ev_key),
        _faces=faces,
        _face_slots=face_slots_list,
        _slot_signs={k: sorted(v) for k, v in obj_slot_signs.items()},
        _zones_list=zones,
        _subtypes_list=subtypes,
        _p2=p2,
        _p3=p3,
        _signs=sorted(all_clean_signs),
    ))

# Deduplicate moulded copy batches -> 1 event representative
ev_seen = {}
ev_counts = collections.Counter(r['ev_key'] for r in lipi_stones)
lipi_events = []
for r in lipi_stones:
    ek = r['ev_key']
    r['batch_size'] = ev_counts[ek]
    if ek not in ev_seen:
        ev_seen[ek] = r['stone_id']
        r['is_event_rep'] = True
        lipi_events.append(r)
    else:
        r['is_event_rep'] = False
    r['event_id'] = ev_seen[ek]

log(f'Lipi physical stones: {len(lipi_stones)} -> copy-events: {len(lipi_events)} '
    f'(moulded batch duplicates collapsed: {len(lipi_stones) - len(lipi_events)}, duplicate row merges: {len(merges)})')


# ---------------- 4. Calibrate & Build Mahadevan Physical Objects & New-Text Events ----------------
log('Building Mahadevan physical objects & held-out new-text events ...')
cr_df = pd.read_csv(os.path.join(ROOT, 'research', 'data', 'mahadevan_20260905', 'concordance_rows.csv'),
                    dtype=str, keep_default_na=False)
fs_by_tn = {}
for tn, g in cr_df.groupby('textnum'):
    fsv = [x for x in g.fs80 if x not in ('', '0')]
    fs_by_tn[tn] = fsv[0] if fsv else ''

M77_CTAB_FAM = {
    '01': 'unicorn', '03': 'bull_gaur', '04': 'bull_gaur', '06': 'buffalo',
    '07': 'elephant', '09': 'tiger', '10': 'tiger', '11': 'rhinoceros',
    '13': 'goat_antelope', '14': 'goat_antelope', '16': 'hare',
    '29': 'composite', '36': 'gharial', '52': 'human_archer', '86': 'knot'
}

KIND_MAH = {
    'seal': 'seal', 'sealing': 'tag', 'pottery graffito': 'pot',
    'bronze implement': 'tool', 'ivory/bone rod': 'rod',
    'copper tablet': 'ctab', 'miniature tablet': 'mtab', 'miscellaneous': 'other'
}


def classify_mah_site_and_circuit(site_code, tn_str):
    tn = int(tn_str)
    if site_code == 'MD':
        return 'Mohenjo-daro', 'riverine_core'
    if site_code == 'HP':
        return 'Harappa', 'riverine_core'
    if site_code == 'CD':
        return 'Chanhu-daro', 'riverine_core'
    if site_code == 'LL':
        return 'Lothal', 'coastal_home'
    if site_code == 'KB':
        return 'Kalibangan', 'eastern_headwaters'
    if site_code == 'WA':
        # 9801..9852 = Mesopotamia / Susa / Iran; 9901..9905 = Persian Gulf (Bahrain / Failaka)
        if tn >= 9900:
            return 'Persian Gulf (WA)', 'gulf_oman'
        return 'Mesopotamia/Iran (WA)', 'overland_west_north'
    # OS (9001..9701): prefix calibration verified against Lipi & Mahadevan 1977 Table 1
    prefix = tn // 10
    if prefix in (902, 906, 913, 914, 915):  # Rupar, Alamgirpur, Banawali, Bara, Chandigarh
        return f'OS_{prefix}', 'eastern_headwaters'
    if prefix in (908, 909, 910, 911, 912, 920):  # Bala-kot, Surkotada, Desalpur, Pabumath, Dholavira, Rangpur/Rojdi
        return f'OS_{prefix}', 'coastal_home'
    if prefix in (900, 901, 903, 904, 905, 907):  # Amri, Kot-Diji, Lohumjo-daro, Jhukar, Allahdino, Gumla/Nindowari
        return f'OS_{prefix}', 'riverine_core'
    return f'OS_{prefix}', 'unknown'


def classify_mah_zone(site_code, locus_str):
    loc = str(locus_str).strip()
    zones = []
    if not loc or not loc.isdigit():
        return zones
    li = int(loc)
    if site_code == 'MD':
        if 1 <= li <= 15:
            zones.append('md_citadel')
        elif li in (16, 17, 18):
            zones.append('md_HR_elite')
        elif li == 31:
            zones.append('md_DKG_south')
        elif li == 32:
            zones.append('md_DKG_north')
        elif li in (20, 21, 22):
            zones.append('md_VS_MN_craft')
            zones.append('md_VS_dyers')
        elif li in (23, 24, 25, 26, 27, 28, 30, 33, 34, 35, 36, 38):
            zones.append('md_DK_other')
    elif site_code == 'HP':
        if 40 <= li <= 45 or li in (51, 55):
            zones.append('har_mound_F')
            if li == 40:
                zones.append('har_F_granary')
            elif li in (41, 42):
                zones.append('har_F_platforms_quarters')
        elif 46 <= li <= 50:
            zones.append('har_mound_AB')
        elif li in (53, 56, 57, 58):
            zones.append('har_area_DGH')
    elif site_code == 'KB':
        if li == 81:
            zones.append('klb_citadel')
        elif li == 82:
            zones.append('klb_lower_town')
    elif site_code == 'CD':
        if li == 61:
            zones.append('chanhu_mound1')
        elif li == 62:
            zones.append('chanhu_mound2_workshops')
    return zones


def build_mah_subset(df_sub, only_new=True):
    """Build physical object rows and copy-events from Mahadevan lines."""
    objs_out = []
    for tn, g in df_sub.groupby('textnum', sort=False):
        g = g.sort_values('sideline')
        first = g.iloc[0]
        site_code = first.site
        site_std = first.site_l
        sub_site, circuit = classify_mah_site_and_circuit(site_code, str(tn))
        knd = KIND_MAH.get(first.cls, 'other')
        locus = str(first.locus).strip()
        zones = classify_mah_zone(site_code, locus)

        faces = [list(t) for t in g.tok]
        full_sig = '|'.join(sorted('-'.join(f) for f in faces))

        # Copper animal via fs80
        fsc = fs_by_tn.get(str(tn), '')
        ctab_anim = ''
        if knd == 'ctab' and fsc and fsc != '0':
            fam2 = f'{int(fsc):03d}'[:2]
            ctab_anim = M77_CTAB_FAM.get(fam2, '')

        subtypes = []
        if knd == 'tool':
            subtypes.append('copper_tool')
        if knd == 'ctab':
            subtypes.append('copper_tablet')
            if ctab_anim:
                subtypes.append(f'ctab_{ctab_anim}')
        if knd == 'rod':
            subtypes.append('ivory_bone_rod')
        if knd == 'tag':
            subtypes.append('tag_all')
        if knd == 'pot':
            subtypes.append('pot_all')
            subtypes.append('pot_graffito')
        if knd == 'mtab':
            subtypes.append('mtab_all')
        if knd == 'seal':
            subtypes.append('seal_all')

        obj_slot_signs = collections.defaultdict(set)
        face_slots_list = []
        all_clean_signs = set()
        for f in faces:
            sl_list, tg = parse_contextual_slots(f)
            face_slots_list.append(sl_list)
            for s in f:
                if is_clean_sign(s):
                    all_clean_signs.add(s)
            for k_sl, sset in tg.items():
                obj_slot_signs[k_sl] |= sset
        p2, p3 = extract_phrases_2(faces)

        ev_key = ('M', site_std, locus, full_sig) if known_spot(locus) else ('M', 'obj', str(tn))
        objs_out.append(dict(
            textnum=str(tn),
            site_code=site_code,
            site=site_std,
            sub_site=sub_site,
            circuit=circuit,
            locus=locus,
            level=str(first.level),
            zones='|'.join(zones),
            cls_raw=first.cls,
            kind=knd,
            fs80=fsc,
            ctab_animal=ctab_anim,
            subtypes='|'.join(subtypes),
            n_faces=len(faces),
            full_text=full_sig,
            signs='|'.join(sorted(all_clean_signs)),
            phrases2='|'.join(p2),
            phrases3='|'.join(p3),
            ev_key=str(ev_key),
            is_new_only=bool(only_new),
            _faces=faces,
            _face_slots=face_slots_list,
            _slot_signs={k: sorted(v) for k, v in obj_slot_signs.items()},
            _zones_list=zones,
            _subtypes_list=subtypes,
            _p2=p2,
            _p3=p3,
            _signs=sorted(all_clean_signs),
        ))

    seen = {}
    cnts = collections.Counter(r['ev_key'] for r in objs_out)
    evs = []
    for r in objs_out:
        ek = r['ev_key']
        r['batch_size'] = cnts[ek]
        if ek not in seen:
            seen[ek] = r['textnum']
            r['is_event_rep'] = True
            evs.append(r)
        else:
            r['is_event_rep'] = False
        r['event_id'] = seen[ek]
    return objs_out, evs


mah_new_df = mah_M[~mah_M.partnered].copy()
mah_new_objs, mah_new_events = build_mah_subset(mah_new_df, only_new=True)
mah_all_objs, mah_all_events = build_mah_subset(mah_M.copy(), only_new=False)
log(f'Mahadevan held-out new texts: {len(mah_new_df)} lines -> {len(mah_new_objs)} objects -> {len(mah_new_events)} copy-events '
    f'(moulded batch duplicates collapsed: {len(mah_new_objs) - len(mah_new_events)})')
log(f'Mahadevan full corpus: {len(mah_M)} lines -> {len(mah_all_objs)} objects -> {len(mah_all_events)} copy-events')


# ---------------- 5. Save CSVs & Event JSONs ----------------
def strip_private(rows):
    return [{k: v for k, v in r.items() if not k.startswith('_')} for r in rows]


pd.DataFrame(strip_private(lipi_stones)).to_csv(os.path.join(OUT, 'objects_lipi.csv'), index=False)
pd.DataFrame(strip_private(mah_new_objs)).to_csv(os.path.join(OUT, 'objects_mah_new.csv'), index=False)
pd.DataFrame(strip_private(mah_all_objs)).to_csv(os.path.join(OUT, 'objects_mah_all.csv'), index=False)


def serialize_events(evs, id_col):
    out = []
    for r in evs:
        out.append(dict(
            id=r[id_col],
            cisi=r.get('cisi', ''),
            site=r['site'],
            circuit=r['circuit'],
            kind=r['kind'],
            zones=r['_zones_list'],
            subtypes=r['_subtypes_list'],
            ctab_animal=r['ctab_animal'],
            tag_reverse=r.get('tag_reverse', ''),
            seal_animal=r.get('seal_animal', ''),
            time_bin=r.get('time_bin', ''),
            full_text=r['full_text'],
            faces=r['_faces'],
            face_slots=r['_face_slots'],
            signs=r['_signs'],
            slot_signs=r['_slot_signs'],
            phrases2=r['_p2'],
            phrases3=r['_p3'],
            batch_size=r['batch_size'],
        ))
    return out


with open(os.path.join(OUT, 'events_lipi.json'), 'w') as fh:
    json.dump(serialize_events(lipi_events, 'stone_id'), fh)
with open(os.path.join(OUT, 'events_new.json'), 'w') as fh:
    json.dump(serialize_events(mah_new_events, 'textnum'), fh)
with open(os.path.join(OUT, 'events_mah_all.json'), 'w') as fh:
    json.dump(serialize_events(mah_all_events, 'textnum'), fh)

# Build sign_meta.csv with event counts across Lipi and New texts
lipi_sign_cnt = collections.Counter()
new_sign_cnt = collections.Counter()
lipi_slot_cnt = collections.defaultdict(collections.Counter)
for r in lipi_events:
    for s in r['_signs']:
        lipi_sign_cnt[s] += 1
    for sl, ss in r['_slot_signs'].items():
        for s in ss:
            lipi_slot_cnt[s][sl] += 1
for r in mah_new_events:
    for s in r['_signs']:
        new_sign_cnt[s] += 1

all_signs = sorted(set(lipi_sign_cnt.keys()) | set(new_sign_cnt.keys()) | set(shape_map.keys()))
smeta_rows = []
for s in all_signs:
    if not is_clean_sign(s):
        continue
    pc = mayig_map.get(s, '')
    sc = lipi_slot_cnt[s]
    dom_slot = sc.most_common(1)[0][0] if sc else v2_map.get(s, 'PERSONAL')
    smeta_rows.append(dict(
        sign=s,
        v2_class=v2_map.get(s, 'PERSONAL'),
        dominant_ctx_slot=dom_slot,
        mayig_p=pc,
        mahadevan_m=mah_code_map.get(s, ''),
        shape_desc=shape_map.get(s, '') or p_desc_map.get(pc, ''),
        lipi_events=lipi_sign_cnt[s],
        new_events=new_sign_cnt[s],
        n_solo=sc['SOLO'],
        n_counted=sc['COUNTED'],
        n_front=sc['FRONT'],
        n_name=sc['NAME'],
        n_crest=sc['NAME_CREST'],
        n_pre_closer=sc['PRE_CLOSER'],
        n_ending=sc['ENDING'],
    ))
pd.DataFrame(smeta_rows).to_csv(os.path.join(OUT, 'sign_meta.csv'), index=False)

# Summary breakdown print
log('--- Context Summary (Lipi 4,476 events vs Held-Out New Texts 990 events) ---')
log('Lipi circuits:', dict(collections.Counter(r['circuit'] for r in lipi_events)))
log('New  circuits:', dict(collections.Counter(r['circuit'] for r in mah_new_events)))
log('Lipi subtypes:', dict(collections.Counter(st for r in lipi_events for st in r['_subtypes_list']).most_common(22)))
log('Lipi zones   :', dict(collections.Counter(z for r in lipi_events for z in r['_zones_list']).most_common(20)))
log('New  zones   :', dict(collections.Counter(z for r in mah_new_events for z in r['_zones_list']).most_common(15)))
log('Done writing work_data/sem/ context tables.')
