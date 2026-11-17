#!/usr/bin/env python3
"""Corpus-facts-only loader for the decoy test. Import: from decoy_loader import *

It gives the Indus corpus tables and test helpers and NOTHING about which sign has which word.
(sound_v4_common and everything built on it import the accepted word list, so this wrapper takes sound_v3_common,
which does not, and adds the picture-side table and the time bins from the later kits as plain corpus facts.)

Tables
  d      one row per face (Lipi catalogue): id, site, kind (seal / tag / pot / tool / bangle / rod / ctab / mtab / other), tok (tuple of sign
         numbers in reading order), symbol (picture code), complete_txt, group, obj (object id) ... ; 'P' / 'R' hold the template parse of the face.
  objs   one row per object: signs (set), kind, site, area, bh (block-house), nfaces, faces (list of token tuples), animal / symbol, pic (picture label), bin (time bin)
  M      second catalogue (Mahadevan); rows with partnered == False are the NEW TEXTS (no Lipi partner) -> faces_all('Mu'), kfaces('Mu')
  moh    Mohenjo-daro seal objects with a house label; moh.house, moh.band (3-ft depth band)
  VAL    number signs; SHORT / TALL stroke styles of counts; PORTER, FISH sign sets
Functions (all return None or (came_true_direction, P, text))
  faces_all(cat), kfaces(cat)                      faces; cat 'L' Lipi, 'Mu' new texts, 'LM' both
  on_kind / off_kind(s, kinds, cat)                object kind
  counts_beside(s) / count_series(s, 'tall'|'short')   counts beside a sign, and their stroke style
  with_count(s), prev_count(s), next_count(s)      counts on the face / next to it
  animal_share(s, animals), reverse_has(s, t)      picture on the seal / the other face of the object (also pic_share below)
  site_share(s, site), harappa_area, moh_area, house_share(s)   findspot (city, area, house)
  adjacent(s, t, side), cooccur(s, t), text_pos(s, 'first'|'last'), name_partner_diversity(s), multi_site(s)
  time_share(s, bin)    objects carrying s are in a time bin (early / middle / late) more than all dated objects
  pic_share(s, labels)  objects carrying s show one of the picture labels more than all objects with a picture
  profile(s)            kinds, neighbours, positions, sites of a sign
  strat_shuffle_p(has, outcome, strata)   the shuffle test of the rules: shuffles inside site|kind strata, seeded, one-sided P
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound_v3_common import *
import numpy as np, pandas as pd, collections
from scipy.stats import binomtest

# ---- picture table (copied from the sixth-pass kit; corpus facts only) ----
PIC_EN = {'Elep': 'elephant', 'Hare': 'hare', 'Tigr': 'tiger', 'Rhin': 'rhinoceros', 'Buff': 'water buffalo', 'Gaur': 'gaur (wild ox)',
          'Bull1': 'unicorn', 'Bull': 'short-horned bull', 'Bull2': 'bull (second kind)', 'Bull3': 'bull (third kind)', 'Zebu': 'zebu (humped bull)',
          'Goat': 'goat / markhor (marked body, with trough)', 'Comp': 'composite / spotted beast', 'Stag': 'branch-horned beast with trough (stag; the deer sign 341 stands in for it)',
          'Archer': 'horned figure with a bow (catalogue Anth)', 'Anth': 'human figure', 'Knot': 'endless knot (catalogue Loop)', 'Loop': 'endless knot',
          'Gavi': 'gharial / crocodile', 'Phyt': 'plant', 'Fish': 'fish', 'Mult': 'several figures', 'Scene': 'scene with figures', 'Bult': 'dotted circles / bullet motif (code Bult)',
          'Cros': 'cross', 'Xcrs': 'hatched cross', 'Pipal': 'pipal leaf', 'S590': 'box sign as picture', 'CompBull': 'composite bull', 'Swas': 'swastika', 'Maze': 'maze',
          'Tri4': 'four triangles', 'Xhch': 'hatched X', 'Crs': 'cross', 'Htgr': 'horned tiger', 'Bird': 'bird', 'Turt': 'turtle'}
# copper-tablet sets: text (reading order) -> picture, by eye (photos checked: see report)
CTAB_SET = {
 '503-615-752-740': 'Stag', '503-615-740': 'Stag', '503-752-000-740': 'Stag',
 '235-705-033-845-407-321-407': 'Hare',
 '806-845-061-407-850-900-740': 'Archer', '806-845-407-850-900-740': 'Archer', '000-000-000-407-000-900-740': 'Archer',
 '231-017-585-095-520-032-407': 'Goat', '220-017-585-095-520-032-408': 'Goat',
 '003-421-176-100-740-790': 'Goat', '003-422-176-100-740': 'Goat', '003-000-176-000-740-790': 'Goat', '003-421-176-000': 'Goat',
 '706-033-923-740': 'Elep', '706-033-923-740-001': 'Elep', '705-033-923-740-001': 'Elep',
 '798-240-845-061-407': 'Tigr', '000-000-845-061-407': 'Tigr',
 '905-032-597-142-617': 'Comp', '904-032-597-142-617': 'Comp', '905-032-597-142-000': 'Comp', '017-585-388-740': 'Comp',
 '806-235-233-705-033-585-407': 'Comp', '003-233-100-740': 'Comp', '032-220-773-740': 'Comp',
 '235-233-222-740': 'Rhin', '235-220-222-740': 'Rhin', '503-615-740x': 'Rhin',
 '255-435-690-740-900-003-422': 'Buff', '255-435-690-740-900-001-003-424': 'Buff', '255-435-690-740-900-001-003-423': 'Buff', '255-435-690-740-000': 'Buff', '000-690-740-900-000': 'Buff',
 '415-220-845-407': 'Knot',
 '032-071-407': 'Gaur', '615-343-595': 'Gaur',
 '744-760-095-595-001-142-617': 'Bull1', '747-717-095-595-001-142-617': 'Bull1', '747-717-142-595-001': 'Bull1',
}
NOPIC = {'', '-', 'Othr', 'Unknown', '?', 'None', 'X', 'T', 'Strokes', 'Box', 'T-A-T', 'Hgls'}


def picture_of(o):
    """picture label of one Lipi object (row of objs) or None."""
    if o.kind == 'ctab':
        main = max(('-'.join(x) for x in o.faces), key=len)
        return CTAB_SET.get(main)
    c = str(o.symbol).split(':')[0].split('+')[0]
    if c in NOPIC: return None
    return 'Knot' if c == 'Loop' else c


# the copper tablets whose second face is one big sign (or two) in place of a picture: no picture label for them
CT_PICSIGN = {}
for o in objs[objs.kind == 'ctab'].itertuples():
    fs = ['-'.join(x) for x in o.faces]
    if len(fs) == 2:
        a, b = sorted(fs, key=len)
        if len(a.split('-')) <= 2: CT_PICSIGN[o.Index] = (a, b)
objs['pic'] = [None if o.Index in CT_PICSIGN else picture_of(o) for o in objs.itertuples()]



# ---- time bins (work_data/time/time_axis.csv: obj, site, kind, bin early / middle / late) ----
_T = pd.read_csv(f'{ROOT}/work_data/time/time_axis.csv', dtype=str).fillna('')
BIN = dict(zip(_T.obj, _T.bin)); STRAT = dict(zip(_T.obj, _T.stratum))
d['bin'] = d.obj.map(BIN).fillna(''); d['stratum'] = d.obj.map(STRAT).fillna('')
objs['bin'] = objs.index.map(lambda o: BIN.get(o, ''))
BINS = ('early', 'middle', 'late')


def time_share(s, which):
    """objects carrying s sit in the time bin(s) `which` more than all dated objects do."""
    w = {which} if isinstance(which, str) else set(which)
    D = objs[objs.bin != '']
    return share(D.bin.isin(w), D[D.signs.apply(lambda z: s in z)].bin.isin(w), f'dated objects in {"/".join(sorted(w))}')


def pic_share(s, labels):
    """objects carrying s show one of the picture labels more than all objects that have a picture."""
    w = {labels} if isinstance(labels, str) else set(labels)
    P = objs[objs.pic.notna()]
    return share(P.pic.isin(w), P[P.signs.apply(lambda z: s in z)].pic.isin(w), f'objects with a picture showing {"/".join(sorted(w))[:40]}')


def strat_shuffle_p(has, outcome, strata, direction='greater', n=5000, seed=12345):
    """The shuffle test of the rules. has / outcome: True/False per object (or per face), strata: site|kind label per object.
    Statistic = share of `outcome` among the `has` rows. The `has` labels are shuffled among rows of the same stratum n times (seeded);
    P = (1 + shuffles at least as extreme) / (1 + n). direction 'greater' or 'less'. Returns (observed share, mean share under shuffle, P)."""
    has = np.asarray(has, bool); outcome = np.asarray(outcome, bool); strata = np.asarray(strata)
    if has.sum() < 3: return None
    g = np.random.default_rng(seed); idx = {}
    for i, s in enumerate(strata): idx.setdefault(s, []).append(i)
    idx = [np.array(v) for v in idx.values()]
    obs = outcome[has].mean(); sims = np.empty(n)
    for k in range(n):
        h = has.copy()
        for v in idx:
            if len(v) > 1: h[v] = g.permutation(has[v])
        sims[k] = outcome[h].mean() if h.any() else np.nan
    sims = sims[~np.isnan(sims)]
    hit = (sims >= obs - 1e-12).sum() if direction == 'greater' else (sims <= obs + 1e-12).sum()
    return float(obs), float(sims.mean()), float((1 + hit) / (1 + len(sims)))
