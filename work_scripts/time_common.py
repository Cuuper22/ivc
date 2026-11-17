#!/usr/bin/env python3
"""Shared kit for the history job (time_*.py): puts a date on every object that can get one.

Plain words:
- PERIOD CODE: the Lipi catalogue's `time` column, which places objects on the Harappa Archaeological Research
  Project (HARP) scale. Dates from harappa.com/beas/chronology: Period 2 (Kot Diji) ca. 2800-2600 BC, 3A ca. 2600-2450,
  3B ca. 2450-2200, 3C ca. 2200-1900, Period 4 (transitional) ca. 1900-1800, Period 5 (Late Harappan) after 1800.
  The catalogue splits 3B and 3C further (3B-1, 3B-2, 3C-1 ... 3C-4) where older excavators' layers were mapped onto it.
- DATE RULES, from surest to weakest:
    A  'excavator'  Harappa objects from the 1986+ HARP digs: the period the excavators gave (phase A / B / B/C / C).
    B  'layer-map'  objects from older digs whose layer the catalogue mapped onto the HARP scale: Vats' strata I-VII at
                    Harappa (stratum I = top = latest), Mackay's Early / Intermediate / Late levels in DK-G at Mohenjo-daro,
                    Kalibangan phases; Dholavira stages placed by their own published dates (see build()).
                    Banawali and Kanmer are left undated (their site period numbers are not HARP periods).
    C  'depth-band' Mohenjo-daro objects with a depth but no level: deepest third of their own excavation area = early,
                    middle third = middle, top third = late. Deeper is older; depths are NOT compared across areas.
- BIN: early = up to and including 3B (before ca. 2200 BC); middle = 3B/C, 3C-1, 3C-2 and unsplit 3C (around and
  just after 2200); late = 3C-3, 3C-4, Period 4, Period 5 (the last stretch of the city, ca. 2100-1800 and after).
  'Period 3' with no letter is left undated.
- SHUFFLE WITHIN AREA: the bin labels are mixed only among objects of the same site and excavation area (and object
  class where the test is on one class), so a change through time cannot come from one area being dug deeper.
Import: from time_common import *
"""
import sys, os, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from measures_common import *        # d (Lipi faces, reading order), objs, M, runs, NUM, UNITS ...
import numpy as np, pandas as pd

OUTT = f'{ROOT}/work_data/time'
os.makedirs(OUTT, exist_ok=True)

RANK = {'Period 1': 0, 'Period 1B': 0, 'Period 1C': 0, 'Period 2': 0, 'Period 2A': 0, 'Period 2B': 0,
        'Period 3A': 1, 'Period 3B-1': 2, 'Period 3B-2': 3, 'Period 3B': 3,
        'Period 3B/C': 4, 'Period 3C-1': 5, 'Period 3C-2': 6, 'Period 3C': 6,
        'Period 3C-3': 7, 'Period 3C-4': 8, 'Period 4': 9, 'Period 5A': 10, 'Period 5B': 10}
def rank_bin(r):
    if r is None or (isinstance(r, float) and np.isnan(r)): return None
    return 'early' if r <= 3 else ('middle' if r <= 6 else 'late')
BINS = ['early', 'middle', 'late']
BI = {b: i for i, b in enumerate(BINS)}


def _ft(s):
    m = re.search(r'(-?\d+(\.\d+)?)\s*ft', str(s))
    if m: return abs(float(m.group(1)))
    m = re.search(r'(-?\d+(\.\d+)?)\s*m\b', str(s))
    if m and float(m.group(1)) != 0: return abs(float(m.group(1))) * 3.281
    return np.nan


def build():
    g = d.groupby('obj').agg(time=('time', 'first'), phase=('phase', 'first'), period=('period', 'first'),
                             room=('room-grid', 'first'), material=('material', 'first'), shape=('shape', 'first'),
                             typ=('type', 'first'), text=('text', 'first'))
    T = objs.join(g)
    T['ft'] = T.depth.map(_ft)
    T['rank'] = T.time.map(RANK)
    T['rule'] = ''
    hp = (T.site == 'Harappa') & T['rank'].notna()
    T.loc[hp & ~T.phase.str.contains('Stratum', na=False), 'rule'] = 'A excavator'
    T.loc[T['rank'].notna() & (T.rule == ''), 'rule'] = 'B layer-map'
    # Site fixes (checked against each site's own published sequence, not the catalogue's mapping):
    # Banawali Period II = the whole Mature Harappan (c. 2300-1700 BC, Wikipedia from Bisht), so its "Period 2" code is
    # not HARP Period 2: left undated. Kanmer's own periods could not be checked: left undated.
    # Dholavira stages (Wikipedia from Bisht): I 2650-2550, II 2550-2500 (pre-urban), III 2500-2200, IV 2200-2000,
    # V 2000-1900, VI 1850-1750. The catalogue put stage IV at 3B-1; re-placed here by the stage's own dates.
    T.loc[T.site.isin(['Banawali', 'Kanmer']), ['rank', 'rule']] = [np.nan, '']
    DH = {'1': 0, '2': 0, '3': 3, '4': 5, '4/5': 6, '5': 7, '5?': 7, '5/6': 8, '6': 9}
    dh = T.site == 'Dholavira'
    T.loc[dh, 'rank'] = T.loc[dh, 'period'].str.strip().map(DH)
    T.loc[dh & T['rank'].notna(), 'rule'] = 'B layer-map'
    T.loc[dh & T['rank'].notna(), 'time'] = 'Dholavira stage ' + T.loc[dh & T['rank'].notna(), 'period'].str.strip()
    T['bin'] = T['rank'].map(rank_bin)
    # rule C: Mohenjo-daro depth tertiles inside each excavation area (areas with 12+ depths)
    md = (T.site == 'Mohenjo-daro') & T['bin'].isna() & T.ft.notna()
    for a, sub in T[md].groupby('area'):
        if len(sub) < 12 or a in ('--', ''): continue
        q1, q2 = sub.ft.quantile([1 / 3, 2 / 3])
        b = np.where(sub.ft > q2, 'early', np.where(sub.ft > q1, 'middle', 'late'))
        T.loc[sub.index, 'bin'] = b; T.loc[sub.index, 'rule'] = 'C depth-band'
    T['bi'] = T['bin'].map(BI)
    T['stratum'] = T.site + '|' + T.area.astype(str)
    T['face_mm2'] = T['face']
    return T


T = build()
D = T[T.bin.notna()].copy()           # every dated object

# ---------- per-object features used across the job ----------
MARKED = {'231', '233', '235', '240', '236'}
FISHALL = MARKED | {'220', '226'}
PORT = {'151', '153', '154', '155', '156', '157', '158'}


def rd(o):
    """main face tokens (reading order): the longest face."""
    return max(o.faces, key=len) if len(o.faces) else ()


def has_seq(fs, seq):
    s = '-'.join(seq)
    return any(s in '-'.join(f) for f in fs)


def shuffle_trend(df, col, nshuf=5000, strat='stratum', seed=7):
    """trend of a 0/1 (or numeric) column against bin index 0/1/2: correlation r, and P from shuffling the bin labels
    inside each stratum (two-sided). Returns dict with shares per bin."""
    df = df[df[col].notna()]
    y = df[col].astype(float).values; x = df.bi.values.astype(float)
    if len(df) < 6 or np.std(y) == 0 or np.std(x) == 0: return None
    r = np.corrcoef(x, y)[0, 1]
    groups = [np.where(df[strat].values == s)[0] for s in pd.unique(df[strat])]
    rng2 = np.random.default_rng(seed); null = np.empty(nshuf)
    xs = x.copy()
    for k in range(nshuf):
        for ix in groups:
            if len(ix) > 1: xs[ix] = rng2.permutation(x[ix])
        null[k] = np.corrcoef(xs, y)[0, 1] if np.std(xs) > 0 else 0
    p = (np.sum(np.abs(null) >= abs(r) - 1e-12) + 1) / (nshuf + 1)
    out = dict(n=len(df), r=r, p=p, null_sd=null.std())
    for b in BINS:
        s = df[df.bin == b][col]
        out[b] = (s.mean(), int(s.notna().sum()), float(s.sum()))
    return out


def fmt_tr(o, pct=True):
    if o is None: return 'too few'
    f = (lambda m: f'{m * 100:.1f}%') if pct else (lambda m: f'{m:.1f}')
    return (f"early {f(o['early'][0])} (n {o['early'][1]}), middle {f(o['middle'][0])} (n {o['middle'][1]}), "
            f"late {f(o['late'][0])} (n {o['late'][1]}); trend r {o['r']:+.3f}, within-area shuffle P {o['p']:.4f}")
