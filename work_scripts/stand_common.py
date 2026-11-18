#!/usr/bin/env python3
"""Shared kit for the STAND job (what the unicorn's stand pattern is). Written 2026-11-17.

Plain words:
- STAND LETTER: catalogue code after 'Bull1:' on unicorn seals (W, J, S, I, L): the pattern of the
  small stand drawn under the unicorn's head.
- HOUSEHOLD reading: the stand letter is chosen by the family / building that holds the seal.
- WORKSHOP reading: the stand letter is the house style of the seal-cutter's shop that made the stone.
- Loader: stand_seals() = twins_common.seals() (one row per seal face, with building, block, area,
  depth, time bin, animal, stand, material, boss, size, frame-v2 text kind) plus a few derived columns.
"""
import sys, os, time, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
ROOT = '/home/antigravity/Cuuper22/ivc'
OUT = f'{ROOT}/work_data/stand'; os.makedirs(OUT, exist_ok=True)
IMG = f'{ROOT}/evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images'
T0 = time.time()
def log(tag, *a): print(f'[{tag} {time.time()-T0:6.1f}s]', *a, flush=True)
L5 = ['W', 'J', 'S', 'I', 'L']

def stand_seals():
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        from twins_common import seals, crest_of
    S = seals()
    S['crest'] = [crest_of(s) if s else '' for s in S.signs]
    S['logsz'] = np.log(S.area_mm2)
    S['mat'] = S.material.str.lower().replace({'-': '', 'nan': ''})
    S['bossk'] = S.boss.where(~S.boss.isin(['-', '', '?']), '')
    S['thick'] = pd.to_numeric(S.thmm, errors='coerce'); S.loc[S.thick <= 0, 'thick'] = np.nan
    S['cultc'] = S.cult.where(~S.cult.isin(['-', '', '?']), '')
    return S

def perm_within(vals, strata, rng):
    out = np.array(vals, dtype=object).copy(); vals = np.array(vals, dtype=object)
    for ix in strata: out[ix] = vals[rng.permutation(ix)]
    return out

def strata_idx(keys):
    d = {}
    for i, k in enumerate(keys): d.setdefault(k, []).append(i)
    return [np.array(v) for v in d.values() if len(v) > 1]
