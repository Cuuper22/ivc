#!/usr/bin/env python3
"""Shared kit for the seventh sound pass (sound_v7_*.py): the sixth-pass kit (picture table, copper sets) plus
 - the TIME BIN of every Lipi object (work_data/time/time_axis.csv: early / middle / late, from the history job),
 - the value list read from a values_master csv (values_master4.csv once it exists, else values_master3.csv),
   turned into the tier dicts the coverage counter wants (STRICT7 = strict only; WIDE7 = strict + wide),
 - small helpers for "uses of a sign" in one bin.
Import: from sound_v7_common import *"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound_v6_common import *
OUT7 = f'{ROOT}/work_data/sound_v7'
os.makedirs(OUT7, exist_ok=True)

# ---- time bins (history job) ----
_T = pd.read_csv(f'{ROOT}/work_data/time/time_axis.csv', dtype=str).fillna('')
BIN = dict(zip(_T.obj, _T.bin))                      # obj id -> early / middle / late / '' (undated)
STRAT = dict(zip(_T.obj, _T.stratum))                # obj id -> site|area (the history job's shuffle stratum)
d['bin'] = d.obj.map(BIN).fillna('')
d['stratum'] = d.obj.map(STRAT).fillna('')
objs['bin'] = objs.index.map(lambda o: BIN.get(o, ''))
BINS = ('early', 'middle', 'late')


def load_values(path=None):
    """-> (table, STRICT dict, WIDE dict). Dicts map sign -> 'building' / 'testing' / 'paused' in the shape the
    fourth-pass coverage() and readable() functions want."""
    if path is None:
        path = f'{ROOT}/work_data/values_master4.csv'
        if not os.path.exists(path): path = f'{ROOT}/work_data/values_master3.csv'
    V = pd.read_csv(path, dtype=str).fillna('')
    S = {}; W = {}
    for s, st in zip(V.sign, V.status):
        S[s] = 'building' if st == 'strict' else ('testing' if st == 'wide' else st)
        W[s] = 'building' if st in ('strict', 'wide') else st
    return V, S, W


def dated_faces(cat='L'):
    """Lipi faces with a time bin: list of (tokens, kind, site, bin, stratum, obj)."""
    m = d[d.bin != '']
    return list(zip(m.tok, m.kind, m.site, m.bin, m.stratum, m.obj))
