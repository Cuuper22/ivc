#!/usr/bin/env python3
"""Shared kit for the phrase atlas (phrases_*.py). Date 2026-11-17. No word is attached to any sign anywhere.

Plain words:
- PHRASE: a run of 2, 3 or 4 signs standing right next to each other, in reading order (stored order reversed by the loader).
  A lost sign ('000'), an unclear sign ('ALT') or a sign with no Lipi number ('X...') cuts a run: no phrase spans it.
- DISTINCT TEXT: identical sign strings are counted once (moulded copies, one tablet in two faces) when a phrase is counted.
- OBJECT: one physical thing (seal, tablet, tag, pot...). Atlas numbers count objects (an object carries a phrase once).
- BUILDING / BLOCK / AREA: the registry's findspot keys (registry_build.py): area = excavation area; building = area + block-house
  (Mohenjo-daro) or area + grid square (Harappa, Kalibangan); block = area + block number in front of the house number.
- BIN: early / middle / late from work_data/time/time_axis.csv (time_common.py).
- ANIMAL: the symbol before the colon (Bull1 = unicorn, Gaur = short-horned bull with head low, trough on most = the overseas seal;
  Bult = bull with table, Elep elephant ...). STAND: the letter after the colon (the stand pattern drawn in front).
- ABROAD: object found in region Persian Gulf, Mesopotamia, Iranian Plateau or Central Asia.
- V2 CLASS: the job of a sign in frame v2 (work_data/frame/classes_v2.csv, column v2_base).
"""
import sys, os, re, io, contextlib, collections, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    from time_common import d, M, objs, ROOT          # Lipi faces (reading order), second catalogue, objects
import numpy as np, pandas as pd

OUTP = f'{ROOT}/work_data/phrases'
os.makedirs(OUTP, exist_ok=True)
T0 = time.time()
def log(*a): print(f'[{time.time() - T0:7.1f}s]', *a, flush=True)

ABROAD = {'Persian Gulf', 'Mesopotamia', 'Iranian Plateau', 'Central Asia'}
SHORTHORN = 'Gaur'
C2 = pd.read_csv(f'{ROOT}/work_data/frame/classes_v2.csv', dtype=str).fillna('')
V2 = dict(zip(C2.sign, C2.v2_base))
V2_PLAIN = {'OPEN': 'front word', 'SLOT': 'slot after front', 'CREST': 'name front', 'PERSONAL': 'name part',
            'NUM_NAME': 'tall two in names', 'NUM_SHORT': 'short number', 'NUM_TALL': 'tall number', 'MEASURE': 'measure',
            'AFTER_M': 'after-measure', 'THING': 'counted thing', 'NAME_BACK': 'name back', 'PLACE': 'place/time word',
            'CLOSER': 'closer', 'TITLE': 'after-jar title', 'START': 'text start', 'END': 'text end'}
def v2c(s): return V2.get(s, 'PERSONAL')

SIGN = re.compile(r'^\d{3}$')
def is_sign(s): return bool(SIGN.match(s)) and s != '000'

def runs(tok):
    """maximal runs of real signs (no lost/unclear/X signs) inside one text."""
    out, cur = [], []
    for s in tok:
        if is_sign(s): cur.append(s)
        else:
            if cur: out.append(tuple(cur)); cur = []
    if cur: out.append(tuple(cur))
    return out

def blank(v): return v is None or str(v).strip() in ('', '-', '--', 'nan', '- -')
def clean(v): return '' if blank(v) else str(v).strip().strip('-').strip()

def build_faces():
    """one row per Lipi face with object findspot keys."""
    F = d[['id', 'obj', 'site', 'region', 'area-section', 'block-house', 'room-grid', 'symbol', 'kind', 'tok', 'flg']].copy()
    F['area'] = F['area-section'].map(clean); F['bh'] = F['block-house'].map(clean); F['grid'] = F['room-grid'].map(clean)
    return F

def build_objects():
    """one row per object: site, kind, area, building, block, bin, animal, stand, abroad."""
    g = d.groupby('obj').agg(site=('site', 'first'), region=('region', 'first'), area=('area-section', 'first'),
                             bh=('block-house', 'first'), grid=('room-grid', 'first'), symbol=('symbol', 'first'),
                             kind=('kind', 'first'), cisi=('cisi', 'first'), typ=('type', 'first'))
    for c in ['area', 'bh', 'grid']: g[c] = g[c].map(clean)
    def bld(r):
        if not r.area: return ''
        if r.bh: return f'{r.site}|{r.area}|{r.bh}'
        if r.grid: return f'{r.site}|{r.area}|{r.grid}'
        return ''
    def blk(r):
        if not r.area: return ''
        if r.bh:
            m = re.match(r'^(\d+)', r.bh)
            return f'{r.site}|{r.area}|blk{m.group(1)}' if m else f'{r.site}|{r.area}|{r.bh}'
        if r.grid:
            m = re.match(r'^-?([A-Z]+)', r.grid)
            return f'{r.site}|{r.area}|{m.group(1)}' if m else f'{r.site}|{r.area}|{r.grid}'
        return ''
    g['building'] = g.apply(bld, axis=1); g['block'] = g.apply(blk, axis=1)
    g['area_key'] = [f'{s}|{a}' if a else '' for s, a in zip(g.site, g.area)]
    TA = pd.read_csv(f'{ROOT}/work_data/time/time_axis.csv', dtype=str).fillna('')
    g['bin'] = g.index.astype(str).map(dict(zip(TA.obj, TA.bin))).fillna('')
    sp = g.symbol.fillna('').astype(str).str.split(':', n=1)
    g['animal'] = [s[0] if s[0] not in ('', '-') else ('none' if s[0] == '' else 'blank') for s in sp]
    g['stand'] = [s[1] if len(s) > 1 else '' for s in sp]
    g['abroad'] = g.region.isin(ABROAD)
    return g

def distinct_texts():
    """first catalogue: distinct token strings -> list of run tuples."""
    seen = set(); out = []
    for x in d.tok:
        if not x or x in seen: continue
        seen.add(x); out.append(x)
    return out

def new_distinct_texts():
    """second catalogue lines with no partner in the first (never used to shape anything): distinct token strings."""
    Mu = M[~M.partnered]
    seen = set(); out = []
    for x in Mu.tok:
        if not x or x in seen: continue
        seen.add(x); out.append(x)
    return out

def count_phrases(texts, ks=(2, 3, 4)):
    """returns n_texts[k][phrase], windows[k] (number of k-windows), uni (sign token counts), N (sign tokens in runs)."""
    nt = {k: collections.Counter() for k in ks}; win = {k: 0 for k in ks}; uni = collections.Counter()
    for x in texts:
        seen = {k: set() for k in ks}
        for r in runs(x):
            for s in r: uni[s] += 1
            for k in ks:
                for i in range(len(r) - k + 1):
                    p = r[i:i + k]; win[k] += 1; seen[k].add(p)
        for k in ks:
            for p in seen[k]: nt[k][p] += 1
    return nt, win, uni, sum(uni.values())

def expected(p, uni, N, win):
    """expected number of windows of phrase p if signs were placed by frequency alone."""
    e = win
    for s in p: e *= uni[s] / N
    return e

def find_in(tok, p):
    """True if phrase p appears as adjacent signs in token tuple (no cut sign inside)."""
    k = len(p)
    for r in runs(tok):
        for i in range(len(r) - k + 1):
            if r[i:i + k] == p: return True
    return False

def positions(tok, p):
    """list of (run_index_start_in_text, at_start, at_end) for each occurrence; start/end of the whole token tuple."""
    out = []; k = len(p); i0 = 0
    # walk tokens to keep real indices
    n = len(tok); i = 0
    while i < n:
        if not is_sign(tok[i]): i += 1; continue
        j = i
        while j < n and is_sign(tok[j]): j += 1
        r = tok[i:j]
        for a in range(len(r) - k + 1):
            if tuple(r[a:a + k]) == p:
                out.append((i + a, i + a == 0, i + a + k == n))
        i = j
    return out
