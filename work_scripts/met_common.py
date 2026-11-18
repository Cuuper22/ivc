#!/usr/bin/env python3
"""met_common.py — Shared loader, deduplication, crosswalk fixes, and series-aware numeral parser
for the Metrology & Multi-Face Ledger Solver (met_01_ladder.py, met_02_multiface.py, met_03_physical.py).

Conventions enforced:
1. Dynamic ROOT path so every script reruns cleanly from any working directory.
2. Physical object deduplication (recheck_common.stone_map) + moulded copy batch deduplication
   (sense_corpus.py convention: same site + known findspot + identical sorted face texts = 1 event).
3. Crosswalk repairs for Mahadevan numerals & measures verified from mahadevan_glyphs and seal photos:
   - Lipi 056 = Mahadevan 121-121 (two 4x3 dozen blocks = 24, photo-verified on H-14, K-69, L-115);
     flags the 9 false 'unpartnered' Mahadevan twins (M4106=H-14, M7065=L-115, M8108..8115=K-69..75).
   - Mahadevan M119 (3 rows x 2 slanted strokes = 6, matching Lipi 025/027/028) separated from M105 (014 = 4).
   - Mahadevan M120 (X120, 3 rows x 3 slanted strokes = 9) mapped to 029.
   - Mahadevan M94 (X94, '| //' = 3 tall/slanted strokes after 171, matching Lipi 032-031 on M-326) and M93 ('|| /' = 3)
     mapped to tall-series value 3 ('F3s').
   - Mahadevan M115..M118, M122 mapped to their exact short/stacked/bracketed values.
4. Series-aware & phrase-boundary numeral parser:
   - Splits opener-slot locks (861/817/820/824/880/920 + 002/013) and clause-divider 001 before higher numerals.
   - Combines adjacent numeral signs additively ONLY within the same stroke-height series (F+F or S+S),
     never summing across incompatible series (e.g. 705 033 | 017 585, 001 | 034 700, 027 | 032 740).
"""
import os
import re
import sys
import json
import math
import itertools
import collections
import io
import contextlib
import numpy as np
import pandas as pd
from scipy.stats import binomtest, fisher_exact, mannwhitneyu, spearmanr, chi2_contingency

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

OUT_DIR = os.path.join(ROOT, 'work_data', 'met')
os.makedirs(OUT_DIR, exist_ok=True)

from recheck_common import stone_map, EMPTY

LIPI_CSV = os.path.join(ROOT, 'research', 'data', 'open_prototype', 'lipi', 'metadata_filtered.csv')
MAH_CSV = os.path.join(ROOT, 'work_data', 'mahadevan_parsed.csv')
CW_PAIRS_CSV = os.path.join(ROOT, 'work_data', 'crosswalk_text_pairs.csv')
SHAPES_CSV = os.path.join(ROOT, 'work_data', 'sign_shapes.csv')

MSITE = {
    'MD': 'Mohenjo-daro', 'HP': 'Harappa', 'LL': 'Lothal',
    'KB': 'Kalibangan', 'CD': 'Chanhu-daro', 'OS': 'other', 'WA': 'abroad'
}

KIND_M = {
    'seal': 'seal', 'sealing': 'tag', 'pottery graffito': 'pot',
    'bronze implement': 'tool', 'ivory/bone rod': 'rod',
    'copper tablet': 'ctab', 'miniature tablet': 'mtab', 'miscellaneous': 'other'
}

def kind_L(t):
    t = str(t)
    if t.startswith('SEAL'): return 'seal'
    if t.startswith('TAG'): return 'tag'
    if t.startswith('POT'): return 'pot'
    if t == 'IMPL': return 'tool'
    if t == 'BNGL': return 'bangle'
    if t == 'ROD': return 'rod'
    if t == 'TAB:C': return 'ctab'
    if t in ('TAB:B', 'TAB:I'): return 'mtab'
    return 'other'

def known_spot(x):
    s = str(x).strip()
    return s not in EMPTY and s != ''

def parse_dim_mm(s):
    """Parse dimension strings including ranges like '6 - 9' or '12 - 15' (returns positive midpoint or NaN)."""
    s = str(s).strip()
    if not s or s in EMPTY:
        return np.nan
    nums = [float(x) for x in re.findall(r'\d+\.?\d*', s)]
    if not nums:
        return np.nan
    # Handle '0 - 16.1' (tapered edge to center) vs '6 - 9' (sherd wall range)
    if '-' in s and len(nums) == 2:
        if nums[0] == 0 and nums[1] > 0:
            val = nums[1]
        else:
            val = 0.5 * (nums[0] + nums[1])
    else:
        val = nums[0]
    return val if val > 0 else np.nan

# ==============================================================================
# COMPLETE NUMERAL SIGN CATALOG (6 GRAPHIC / METROLOGICAL SERIES)
# ==============================================================================
# Format: token -> (series, numeric_value, label, layout_desc)
# Series codes:
#   S = Short single-row vertical strokes (discrete goods, people, small bundles 1-5, rare 6-10)
#   F = Full-height / Tall vertical strokes (capacity & weight measures, containers 1-6)
#   T = Two-row Stacked short strokes (discrete goods >=6, plus specialized 3/4/5 bundles & 'Seven' 017)
#   B = Three-row Block & Bracketed Bundle numerals (025-029 slanted blocks 6-10, 048/049=(7), 055=12, 056=24)
#   A = A-comb load-count series (465-475, monotonic foot-tick series 1..10 before crop 806/838)
#   J = Infixed Jar-mouth stroke series (741=1, 742-744=2, 745-747=3, 748=4)
NUM_CATALOG = {
    # Series S: Short single-row vertical strokes
    '001': ('S', 1, 'S1', '1 short vertical stroke'),
    '002': ('S', 2, 'S2', '2 short vertical strokes'),
    '003': ('S', 3, 'S3', '3 short vertical strokes'),
    '004': ('S', 4, 'S4', '4 short vertical strokes'),
    '005': ('S', 5, 'S5', '5 short vertical strokes'),
    '006': ('S', 6, 'S6', '6 short vertical strokes (1 row)'),
    '007': ('S', 7, 'S7', '7 short vertical strokes (1 row)'),
    '008': ('S', 8, 'S8', '8 short vertical strokes (1 row, unattested -> replaced by 018)'),
    '019': ('S', 9, 'S9', '9 short vertical strokes (1 row)'),
    '020': ('S', 10, 'S10', '10 short vertical strokes (1 row)'),
    'X115': ('S', 10, 'S10m', '10 short vertical strokes (Mahadevan M115)'),

    # Series F: Full-height / Tall vertical strokes
    '031': ('F', 1, 'F1', '1 full-height vertical stroke'),
    '032': ('F', 2, 'F2', '2 full-height vertical strokes'),
    '033': ('F', 3, 'F3', '3 full-height vertical strokes'),
    '034': ('F', 4, 'F4', '4 full-height vertical strokes'),
    '035': ('F', 5, 'F5', '5 full-height vertical strokes'),
    '036': ('F', 6, 'F6', '6 full-height vertical strokes'),
    '044': ('F', 3, 'F3h', '3 tall strokes with caret hat'),
    '045': ('F', 3, 'F3t', '3 tall strokes with side branch'),
    '046': ('F', 3, 'F3t', '3 tall strokes with side branch'),
    'X93': ('F', 3, 'F3s', '2 vertical + 1 slanted tall stroke (M93)'),
    'X94': ('F', 3, 'F3s', '1 vertical + 2 slanted tall strokes (M94 = Lipi 032-031 after 171)'),

    # Series T: Two-row Stacked short strokes
    '012': ('T', 2, 'T2', '2 stacked short strokes (1 over 1)'),
    '013': ('T', 3, 'T3', '3 stacked short strokes (2 over 1)'),
    '014': ('T', 4, 'T4', '4 stacked short strokes (2 over 2, M105)'),
    '015': ('T', 5, 'T5', '5 stacked short strokes (3 over 2)'),
    '016': ('T', 6, 'T6', '6 stacked short strokes (3 over 3)'),
    '017': ('T', 7, 'T7', '7 stacked short strokes (4 over 3)'),
    '018': ('T', 8, 'T8', '8 stacked short strokes (4 over 4)'),
    'X116': ('T', 9, 'T9', '9 stacked short strokes (5 over 4, M116)'),
    '051': ('T', 9, 'T9r', '9 stacked short strokes under roof (M117)'),
    'X117': ('T', 9, 'T9r', '9 stacked short strokes under roof (M117)'),
    'X118': ('T', 10, 'T10', '10 stacked short strokes (5 over 5, M118)'),

    # Series B: Three-row Block & Bracketed Bundle numerals
    '025': ('B', 7, 'B7', '3 rows of slanted strokes (var. 025, ~6-7)'),
    '026': ('B', 8, 'B8', '3 rows of slanted strokes (var. 026, ~8)'),
    '027': ('B', 9, 'B9', '3 rows of 3 slanted strokes = 9 (photo H-303)'),
    '028': ('B', 10, 'B10', '3 rows of slanted strokes = 10 (photo H-65)'),
    '029': ('B', 9, 'B9b', '3 rows of 3 slanted strokes = 9 (M120)'),
    'B119': ('B', 6, 'B6m', '3 rows x 2 slanted strokes = 6/block (M119 = Lipi 025/027/028)'),
    'X120': ('B', 9, 'B9m', '3 rows x 3 slanted strokes = 9 (M120 = Lipi 029)'),
    '048': ('B', 7, 'B7p', '7 stacked short strokes in parentheses (M113)'),
    '049': ('B', 7, 'B7q', '7 single-row short strokes in parentheses (M111)'),
    '055': ('B', 12, 'B12', '12 strokes: 3 rows of 4 vertical strokes (dozen, M121)'),
    '057': ('B', 12, 'B12p', '12 strokes (4x3) in parentheses (M122)'),
    'X122': ('B', 12, 'B12p', '12 strokes (4x3) in parentheses (M122)'),
    '056': ('B', 24, 'B24', '24 strokes: 3 rows of 8 vertical strokes = 2x055 (photo H-14, K-69, L-115; M 121-121)'),

    # Series A: A-comb load-count series (photo-verified monotonic foot-comb ticks)
    '465': ('A', 1, 'A1', 'A-sign plain / 1 crossbar (photo H-190, H-724)'),
    '466': ('A', 2, 'A2', 'A-sign caged by paired strokes'),
    '467': ('A', 3, 'A3', 'A-sign with 2-3 foot ticks (photo H-146, H-154)'),
    '468': ('A', 4, 'A4', 'A-sign with 4 foot teeth (photo H-152, H-27; also M178 lumped)'),
    '469': ('A', 5, 'A5', 'A-sign with 5 foot teeth (photo H-143)'),
    '470': ('A', 6, 'A6', 'A-sign with 6 foot teeth (photo H-189)'),
    '471': ('A', 7, 'A7', 'A-sign with 7 internal teeth (photo H-132)'),
    '472': ('A', 8, 'A8', 'A-sign with double-row ~8 teeth (photo H-158)'),
    '473': ('A', 8, 'A8b', 'A-sign comb variant (photo M-470)'),
    '474': ('A', 9, 'A9', 'A-sign comb variant 474'),
    '475': ('A', 10, 'A10', 'A-sign + detached 6-tooth comb (photo M-40)'),

    # Series J: Infixed Jar-mouth stroke series
    '741': ('J', 1, 'J1', 'Jar with 1 small stroke in mouth (M343)'),
    '742': ('J', 2, 'J2', 'Jar with 2 small strokes in mouth (M344)'),
    '743': ('J', 2, 'J2b', 'Jar with 2 small strokes in mouth (var.)'),
    '744': ('J', 2, 'J2c', 'Jar with 2 small strokes in mouth (var.)'),
    '745': ('J', 3, 'J3', 'Jar with 3 small strokes in mouth (M345)'),
    '746': ('J', 3, 'J3b', 'Jar with 3 small strokes in mouth (var.)'),
    '747': ('J', 3, 'J3c', 'Jar with 3 small strokes in mouth (var.)'),
    '748': ('J', 4, 'J4', 'Jar with 4 small strokes in mouth'),
}

# Pure numeral signs that stand adjacent to counted signs (excludes J which is infixed in 740)
PURE_NUMS = {k: v for k, v in NUM_CATALOG.items() if v[0] in ('S', 'F', 'T', 'B', 'A')}

# Candidate measure, container, and counted-commodity groups
CANDIDATE_UNITS = {
    # Core capacity & grain ladder
    '413': ('grain_hdr', 'header', 'Grain header (ear/stalk)'),
    '575': ('kottai', 'measure', 'Great grain measure (trapezoid+box)'),
    '704': ('kalam', 'measure', 'Big grain measure (U+long staff, var.)'),
    '705': ('kalam', 'measure', 'Big grain measure (U+long staff)'),
    '706': ('kalam', 'measure', 'Big grain measure (U+long staff, var.)'),
    '707': ('kalam', 'measure', 'Big grain measure (U+long staff, var.)'),
    '540': ('parai', 'measure', 'Bowtie measure'),
    '711': ('vallam', 'measure', 'Sub-kalam pot measure (U with X)'),
    '700': ('cup', 'measure', 'Cup measure (marakkal, 1/12 kalam = 9.24 L)'),
    '701': ('cup', 'measure', 'Cup with 1-2 ticks'),
    '703': ('cup', 'measure', 'Cup with 3 ticks'),
    '320': ('pati', 'measure', 'Daily ration / ladder measure (1/8 cup)'),
    '321': ('pati', 'measure', 'Ration measure var. 321'),
    '323': ('pati', 'measure', 'Ration measure var. 323'),
    '061': ('quarter', 'fraction', 'Quarter (reversed lambda, 1/4)'),
    '062': ('quarter', 'fraction', 'Quarter var. 062'),
    '063': ('quarter', 'fraction', 'Quarter var. 063'),
    '064': ('half_share', 'fraction', 'Bifurcated tall stroke (half/portion)'),
    '868': ('half_share2', 'fraction', 'Half-diamond fraction'),
    # Weight & metal standards
    '171': ('nirai', 'weight', 'Weight standard (T with leaves, takes 3 & 5)'),
    '645': ('kalancu', 'weight', 'Cross weight/unit (X)'),
    '480': ('kunri', 'weight', 'Caret / seed-weight'),
    '821': ('mancadi', 'weight', 'Small weight unit on bronze tools'),
    '595': ('forge', 'craft_unit', 'Striped box with top bar (copper/forge)'),
    # Storage containers
    '605': ('granary', 'container', 'Tall hatched granary bin'),
    '335': ('bin_town', 'container', 'M-shaped bin / town'),
    '336': ('bin_town', 'container', 'M-shaped bin / town var.'),
    '590': ('chest', 'container', 'Square chest with top bar'),
    '740': ('jar', 'container', 'Handled jar (container when counted; closer otherwise)'),
    '226': ('fish_crate', 'container', 'Fish enclosed by 4 strokes (fish-crate)'),
    # Bundle numerals used as counted units
    '055': ('dozen', 'bundle', 'Dozen block (4x3 = 12)'),
    '056': ('two_dozen', 'bundle', 'Two-dozen block (8x3 = 24)'),
    '048': ('seven_bkt', 'bundle', 'Bracketed 7'),
    '049': ('seven_bkt', 'bundle', 'Bracketed 7 (1-row)'),
    # Head-count / share / opener units
    '817': ('diamond_hand', 'person_unit', 'Diamond share / hand'),
    '861': ('diamond_hand', 'person_unit', 'Diamond share / hand'),
    '820': ('wheel_qtr', 'person_unit', 'Six-spoked wheel opener / quarter'),
    '850': ('bare_diamond', 'person_unit', 'Bare diamond share'),
    '877': ('four_diamond', 'person_unit', 'Diamond with 4 small diamonds'),
    # Porters / people
    '151': ('porter', 'person_unit', 'Load-carrier (var. 151)'),
    '153': ('porter', 'person_unit', 'Load-carrier (var. 153)'),
    '154': ('porter', 'person_unit', 'Load-carrier (var. 154)'),
    '155': ('porter', 'person_unit', 'Load-carrier (var. 155)'),
    '156': ('porter', 'person_unit', 'Load-carrier / load unit (156)'),
    '158': ('porter', 'person_unit', 'Load-carrier (var. 158)'),
    '140': ('woman', 'person_unit', 'Person with breasts'),
    '142': ('staff_man', 'person_unit', 'Person with staff'),
    '176': ('seated_man', 'person_unit', 'Seated person'),
    '097': ('bondsman', 'person_unit', 'Bracketed person (ration receiver)'),
    '137': ('cultivator', 'person_unit', 'Person with leaf'),
    '090': ('man', 'person_unit', 'Plain standing person'),
    '091': ('twin_men', 'person_unit', 'Pair of standing persons'),
    # Agricultural & discrete commodities
    '806': ('crop_806', 'commodity', 'Leaf on tree (crop/produce)'),
    '838': ('crop_838', 'commodity', 'Produce / sesame variant (838)'),
    '390': ('tree_390', 'commodity', 'Branching tree (cotton/lots)'),
    '392': ('tree_390', 'commodity', 'Branching tree var. 392'),
    '405': ('tree_405', 'commodity', 'Branching tree var. 405'),
    '406': ('tree_407', 'commodity', 'Branching tree var. 406'),
    '407': ('tree_407', 'commodity', 'Branching tree var. 407 (copper tablets)'),
    '408': ('tree_407', 'commodity', 'Tree var. 408'),
    '220': ('fish_plain', 'commodity', 'Plain fish'),
    '231': ('fish_marked', 'commodity', 'Fish with dot/stroke'),
    '233': ('fish_marked', 'commodity', 'Fish with bar'),
    '235': ('fish_marked', 'commodity', 'Fish with caret roof'),
    '240': ('fish_marked', 'commodity', 'Fish with whiskers'),
    '840': ('two_leaf', 'commodity', 'Two overlapping vertical leaves'),
    '845': ('sheaves', 'commodity', 'Hatched leaf bundle'),
    '900': ('crescent_900', 'time_or_good', 'Right parenthesis (month / bolt)'),
    '904': ('double_904', 'time_or_good', 'Nested parentheses'),
    '923': ('tusk_923', 'commodity', 'Outline crescent/tusk (elephant copper)'),
    '585': ('seven_585', 'bundle_or_time', 'Sign 585 (takes stacked 7)'),
    '503': ('hill_503', 'bundle_or_time', 'Tall striped triangle (takes 7 after)'),
    '520': ('spear_520', 'closer_or_item', 'Spear closer / copper point'),
    '400': ('comb_400', 'closer_or_tally', 'Comb closer / junior'),
}

OPENER_SIGNS = {'861', '817', '820', '824', '880', '920', '692', '550', '360', '297', '595'}

def repair_mah_tokens(mah_str, lipi_str):
    """Apply exact crosswalk repairs to Mahadevan token sequences while preserving alignment."""
    ms = [x for x in mah_str.split('-') if x]
    ls = [x for x in lipi_str.split('-') if x]
    if len(ms) != len(ls):
        return tuple(ls)
    out = []
    i = 0
    while i < len(ms):
        # Collapse M 121-121 -> Lipi '056' (24 = two dozen) and M 1-1 -> Lipi '091'
        if i + 1 < len(ms) and ms[i] == '121' and ms[i + 1] == '121':
            out.append('056')
            i += 2
            continue
        if i + 1 < len(ms) and ms[i] == '1' and ms[i + 1] == '1':
            out.append('091')
            i += 2
            continue
        m_tok, l_tok = ms[i], ls[i]
        if m_tok == '119':
            out.append('B119')      # 3-row slanted block (Lipi 025/027/028), NOT 014!
        elif m_tok == '120':
            out.append('029')       # 3-row x 3 slanted block = 9
        elif m_tok == '94':
            out.append('X94')       # 1 vertical + 2 slanted tall strokes = 3 (after 171)
        elif m_tok == '93':
            out.append('X93')       # 2 vertical + 1 slanted tall strokes = 3
        elif m_tok in ('115', '116', '117', '118', '122'):
            out.append(f'X{m_tok}')
        elif m_tok == '172' and l_tok == 'X172':
            out.append('417')
        else:
            out.append(l_tok)
        i += 1
    return tuple(out)


def parse_num_runs(tok, naive_cross_series=False):
    """Parse number runs in a token sequence (in reading order).

    Returns list of dicts:
      {'start': i, 'end': j, 'val': int, 'series': str, 'tokens': tuple, 'role': 'count'|'opener_slot'|'divider'}
    """
    n = len(tok)
    if naive_cross_series:
        out = []
        i = 0
        while i < n:
            if tok[i] in PURE_NUMS:
                j = i
                while j < n and tok[j] in PURE_NUMS:
                    j += 1
                vals = [PURE_NUMS[t][1] for t in tok[i:j]]
                ser = ''.join(sorted({PURE_NUMS[t][0] for t in tok[i:j]}))
                out.append(dict(start=i, end=j, val=sum(vals), series=ser, tokens=tuple(tok[i:j]), role='count'))
                i = j
            else:
                i += 1
        return out

    out = []
    i = 0
    while i < n:
        t = tok[i]
        if t not in PURE_NUMS:
            i += 1
            continue
        ser, val, _, _ = PURE_NUMS[t]

        # Rule 1: Opener-slot lock: opener at i-1 (especially near start of face) + 002 or 013 or 032 (for 820)
        if i > 0 and tok[i - 1] in OPENER_SIGNS and (
            t in ('002', '013') or (tok[i - 1] == '820' and t in ('001', '032'))
        ):
            out.append(dict(start=i, end=i + 1, val=val, series=ser, tokens=(t,), role='opener_slot'))
            i += 1
            continue
        # Also if 002 stands immediately before another numeral and is NOT preceded by a counted unit (broken opener `000 002 N`)
        if t == '002' and i + 1 < n and tok[i + 1] in PURE_NUMS and (i == 0 or tok[i - 1] in ('000', '741', '742', '745', '060')):
            out.append(dict(start=i, end=i + 1, val=val, series=ser, tokens=(t,), role='opener_slot'))
            i += 1
            continue

        # Rule 2: Multiplier '001 055' = '1 dozen' (12) or '002 055' (after non-opener)
        if t == '001' and i + 1 < n and tok[i + 1] == '055':
            out.append(dict(start=i, end=i + 1, val=1, series='S', tokens=('001',), role='count'))
            i += 1
            continue

        # Rule 3: Clause-divider '001' before another numeral (e.g. '740 001 468 806', '^ 001 034 700', '740 001 004 407')
        if t == '001' and i + 1 < n and tok[i + 1] in PURE_NUMS:
            nxt_ser, nxt_val, _, _ = PURE_NUMS[tok[i + 1]]
            if nxt_ser != 'S' or nxt_val > 1:
                out.append(dict(start=i, end=i + 1, val=1, series='S', tokens=('001',), role='divider'))
                i += 1
                continue

        # Rule 4: Within-series additive runs ONLY (F+F or S+S)
        if ser in ('F', 'S'):
            j = i + 1
            while j < n and tok[j] in PURE_NUMS:
                s2, v2, _, _ = PURE_NUMS[tok[j]]
                if s2 != ser:
                    break
                # Within F: allow non-increasing (033+032=5, 033+031=4, 032+031=3, 033+033=6, 032+032=4)
                # plus rare pot/tablet reversed 031+032=3 at text end/start
                prev_v = PURE_NUMS[tok[j - 1]][1]
                if ser == 'F' and (v2 <= prev_v or (prev_v == 1 and v2 == 2 and (j + 1 == n or i == 0))):
                    j += 1
                elif ser == 'S' and v2 <= prev_v and prev_v >= 2:
                    j += 1
                else:
                    break
            vals = [PURE_NUMS[x][1] for x in tok[i:j]]
            out.append(dict(start=i, end=j, val=sum(vals), series=ser, tokens=tuple(tok[i:j]), role='count'))
            i = j
        else:
            # T, B, A signs are self-contained graphic blocks (never additively chained with adjacent signs)
            out.append(dict(start=i, end=i + 1, val=val, series=ser, tokens=(t,), role='count'))
            i += 1
    return out


def load_corpora():
    """Load Lipi and Mahadevan with stone_map deduplication, copy-batch event deduplication, and crosswalk repairs."""
    raw_L = pd.read_csv(LIPI_CSV, dtype=str, keep_default_na=False)
    raw_L['obj'] = raw_L['id'].str.split('.').str[0]
    f2s, merges = stone_map(raw_L)
    raw_L['stone'] = raw_L['id'].map(f2s)
    raw_L['kind'] = raw_L['type'].map(kind_L)
    raw_L['broken'] = raw_L['text'].apply(lambda t: '[' in t or ']' in t or '000' in t)
    raw_L['tok'] = raw_L['text'].apply(
        lambda t: tuple('ALT' if '/' in x else x for x in t.strip('+[]').split('-')[::-1] if x)
    )
    raw_L['h_mm'] = raw_L['horizontal(mm)'].map(parse_dim_mm)
    raw_L['v_mm'] = raw_L['vertical(mm)'].map(parse_dim_mm)
    raw_L['th_mm'] = raw_L['thickness(mm)'].map(parse_dim_mm)

    # Group Lipi into physical stones
    L_stones = []
    for st, g in raw_L.groupby('stone', sort=False):
        g = g.sort_values('id')
        r0 = g.iloc[0]
        faces = list(g['tok'])
        full_sig = '|'.join(sorted('-'.join(f) for f in faces))
        if known_spot(r0['area-section']) or known_spot(r0['block-house']) or known_spot(r0.get('room-grid', '')):
            ev_key = ('L', r0['site'], r0['area-section'], r0['block-house'], r0.get('room-grid', ''), full_sig)
        else:
            ev_key = ('L_stone', st)
        L_stones.append(dict(
            cat='L', stone_id=st, cisi=r0['cisi'], site=r0['site'],
            area=r0['area-section'], bh=r0['block-house'], room=r0.get('room-grid', ''),
            type=r0['type'], kind=r0['kind'], material=r0['material'], shape=r0['shape'],
            xsec=r0['cross-section'], preservation=r0['preservation'], symbol=r0['symbol'],
            h_mm=r0['h_mm'], v_mm=r0['v_mm'], th_mm=r0['th_mm'],
            nfaces=len(faces), faces=faces, broken=any(g['broken']),
            full_sig=full_sig, ev_key=ev_key
        ))
    df_L_stones = pd.DataFrame(L_stones)
    df_L_events = df_L_stones.drop_duplicates('ev_key').reset_index(drop=True)

    # Load Mahadevan
    raw_M = pd.read_csv(MAH_CSV, dtype=str, keep_default_na=False)
    cw_pairs = pd.read_csv(CW_PAIRS_CSV, dtype=str, keep_default_na=False)
    partnered_mah = set(cw_pairs['mahadevan_text'])
    raw_M['partnered'] = raw_M['reading_mah'].isin(partnered_mah)
    # Detect 121-121 / 056 twins that missed string-length partnering (H-14, L-115, K-69..75)
    raw_M['split_twin_056'] = raw_M['reading_mah'].str.contains('121-121')
    raw_M['site_l'] = raw_M['site'].map(MSITE).fillna('other')
    raw_M['kind'] = raw_M['cls'].map(KIND_M).fillna('other')
    raw_M['broken'] = (raw_M['complete'] != 'True') | raw_M['reading_lipi'].str.contains('000')
    raw_M['tok_orig'] = raw_M['reading_lipi'].apply(lambda s: tuple(x for x in s.split('-') if x))
    raw_M['tok'] = [repair_mah_tokens(rm, rl) for rm, rl in zip(raw_M['reading_mah'], raw_M['reading_lipi'])]

    def group_mah(sub_M, tag):
        objs = []
        for tn, g in sub_M.groupby('textnum', sort=False):
            g = g.sort_values('sideline')
            r0 = g.iloc[0]
            faces = list(g['tok'])
            full_sig = '|'.join(sorted('-'.join(f) for f in faces))
            ev_key = (tag, r0['site_l'], str(r0['locus']), full_sig) if known_spot(r0['locus']) else (f'{tag}_obj', tn)
            objs.append(dict(
                cat=tag, stone_id=f'M{tn}', cisi=f'M{tn}', site=r0['site_l'],
                area=str(r0['locus']), bh='', room='',
                type=r0['cls'], kind=r0['kind'], material='', shape='',
                xsec='', preservation='', symbol=str(r0['fs']),
                h_mm=np.nan, v_mm=np.nan, th_mm=np.nan,
                nfaces=len(faces), faces=faces, broken=any(g['broken']),
                full_sig=full_sig, ev_key=ev_key,
                split_twin_056=bool(any(g['split_twin_056']))
            ))
        df_o = pd.DataFrame(objs)
        df_e = df_o.drop_duplicates('ev_key').reset_index(drop=True)
        return df_o, df_e

    df_Mall_objs, df_Mall_events = group_mah(raw_M, 'Mall')
    df_Mnew_objs, df_Mnew_events = group_mah(raw_M[~raw_M['partnered']], 'Mnew')
    df_Mnew_clean_objs, df_Mnew_clean_events = group_mah(
        raw_M[(~raw_M['partnered']) & (~raw_M['split_twin_056'])], 'Mnew_clean'
    )

    return dict(
        raw_L=raw_L, L_stones=df_L_stones, L_events=df_L_events,
        raw_M=raw_M, Mall_objs=df_Mall_objs, Mall_events=df_Mall_events,
        Mnew_objs=df_Mnew_objs, Mnew_events=df_Mnew_events,
        Mnew_clean_objs=df_Mnew_clean_objs, Mnew_clean_events=df_Mnew_clean_events,
    )


def fit_ownership_rates(event_df):
    """Fit EM attraction rates P(sign owns count AFTER: 'X n') and P(sign owns count BEFORE: 'n Y')
    on Lipi deduplicated events, so ambiguous 'X [num] Y' slots resolve cleanly without peeking at M_new."""
    occ = collections.Counter()
    slots = []
    face_list = []
    for r in event_df.itertuples(index=False):
        for f in r.faces:
            fi = len(face_list)
            face_list.append(f)
            for s in f:
                occ[s] += 1
            for run in parse_num_runs(f):
                if run['role'] != 'count':
                    continue
                a, b = run['start'], run['end']
                L = f[a - 1] if a > 0 and f[a - 1] not in PURE_NUMS and f[a - 1] not in ('000', 'ALT') else None
                R = f[b] if b < len(f) and f[b] not in PURE_NUMS and f[b] not in ('000', 'ALT') else None
                # note: if 001 precedes 055 ('001 055'), 055 is R (a bundle noun!) even though 055 is in PURE_NUMS
                if R is None and b < len(f) and f[b] in ('055', '056', '048', '049') and run['tokens'] in (('001',), ('002',), ('031',)):
                    R = f[b]
                slots.append((fi, run, L, R))

    w = []
    for _, _, L, R in slots:
        if L is not None and R is not None:
            w.append(0.5)
        elif L is not None:
            w.append(1.0)
        else:
            w.append(0.0)

    for _ in range(35):
        after_c = collections.defaultdict(float)
        before_c = collections.defaultdict(float)
        for (_, _, L, R), wi in zip(slots, w):
            if L is not None:
                after_c[L] += wi
            if R is not None:
                before_c[R] += (1.0 - wi)
        for idx, (_, _, L, R) in enumerate(slots):
            if L is not None and R is not None:
                pa = (after_c[L] + 0.05) / (occ[L] + 1.0)
                pb = (before_c[R] + 0.05) / (occ[R] + 1.0)
                w[idx] = pa / (pa + pb)

    after_rate = {s: (after_c[s] + 0.05) / (occ[s] + 1.0) for s in occ}
    before_rate = {s: (before_c[s] + 0.05) / (occ[s] + 1.0) for s in occ}
    return after_rate, before_rate, occ


def extract_owned_counts(event_df, after_rate, before_rate):
    """Extract all owned count instances from an event dataframe using frozen Lipi attraction rates."""
    rows = []
    for r in event_df.itertuples(index=False):
        for fi, f in enumerate(r.faces):
            nruns = parse_num_runs(f)
            for run in nruns:
                if run['role'] != 'count':
                    continue
                a, b = run['start'], run['end']
                L = f[a - 1] if a > 0 and f[a - 1] not in PURE_NUMS and f[a - 1] not in ('000', 'ALT') else None
                R = f[b] if b < len(f) and f[b] not in PURE_NUMS and f[b] not in ('000', 'ALT') else None
                if R is None and b < len(f) and f[b] in ('055', '056', '048', '049') and run['tokens'] in (('001',), ('002',), ('031',)):
                    R = f[b]

                if L is None and R is None:
                    owner, side, ambig = 'BARE', 'bare', False
                elif L is not None and R is None:
                    owner, side, ambig = L, 'after', False
                elif L is None and R is not None:
                    owner, side, ambig = R, 'before', False
                else:
                    ambig = True
                    pa = after_rate.get(L, 0.02)
                    pb = before_rate.get(R, 0.02)
                    if pa >= pb:
                        owner, side = L, 'after'
                    else:
                        owner, side = R, 'before'

                u_grp = CANDIDATE_UNITS[owner][0] if owner in CANDIDATE_UNITS else ('bare' if owner == 'BARE' else 'other')
                u_dom = CANDIDATE_UNITS[owner][1] if owner in CANDIDATE_UNITS else ('bare' if owner == 'BARE' else 'other')
                rows.append(dict(
                    cat=r.cat, stone_id=r.stone_id, cisi=r.cisi, site=r.site, area=r.area,
                    kind=r.kind, type=r.type, face_idx=fi, owner=owner, unit_group=u_grp,
                    domain=u_dom, side=side, ambiguous=ambig, val=run['val'], series=run['series'],
                    num_tokens=' '.join(run['tokens']), face_text=' '.join(f)
                ))
    return pd.DataFrame(rows)


if __name__ == '__main__':
    D = load_corpora()
    print(f"[met_common] Lipi: {len(D['raw_L'])} faces -> {len(D['L_stones'])} stones -> {len(D['L_events'])} copy events")
    print(f"[met_common] Mahadevan all: {len(D['raw_M'])} lines -> {len(D['Mall_objs'])} objs -> {len(D['Mall_events'])} copy events")
    print(f"[met_common] Mahadevan new (standard): {len(D['Mnew_objs'])} objs -> {len(D['Mnew_events'])} copy events")
    print(f"[met_common] Mahadevan new (056-decontaminated): {len(D['Mnew_clean_objs'])} objs -> {len(D['Mnew_clean_events'])} copy events")
    ar, br, occ = fit_ownership_rates(D['L_events'])
    oc_L = extract_owned_counts(D['L_events'], ar, br)
    oc_M = extract_owned_counts(D['Mnew_clean_events'], ar, br)
    print(f"[met_common] Owned counts: Lipi events={len(oc_L)}, M_new_clean events={len(oc_M)}")
