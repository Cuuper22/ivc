#!/usr/bin/env python3
"""Shared kit for the measures job (measures_*.py): the ladder of Indus grain measures.

Builds on the third-pass loader (sound_v3_common -> v2_common): `d` = Lipi faces (first catalogue, tokens in
reading order), `M` = second catalogue (Mahadevan 1977) with Lipi sign numbers; M[~M.partnered] = the 1,183
"new texts" never used to choose a value.

Plain words:
- a NUMBER RUN is one or more number signs standing next to each other; its value is their sum
  (scribes write 4 as 3+1, 6 as 3+3).
- series: S = short strokes, T = stacked short strokes, F = tall (full-height) strokes, A = the A-comb load count
  (value not coded), B = row-blocks 025-029 (value unknown).
- a MEASURE sign is one of the unit words read so far (list UNITS below).
"""
import sys, os, collections, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from sound_v3_common import *          # d, M, objs, ROOT, pd, np, binomtest ...
OUTM = f'{ROOT}/work_data/measures'
os.makedirs(OUTM, exist_ok=True)

# ---- number signs: sign -> (series, value) ----
NUM = {}
for i in range(1, 8): NUM[f'{i:03d}'] = ('S', i)
NUM['012'] = ('T', 2)
for i in range(13, 19): NUM[f'{i:03d}'] = ('T', i - 10)
NUM['019'] = ('S', 9); NUM['020'] = ('S', 10)
for i in range(31, 37): NUM[f'{i:03d}'] = ('F', i - 30)
for i in range(465, 476): NUM[str(i)] = ('A', None)
for b in ('025', '026', '027', '028', '029'): NUM[b] = ('B', None)

# ---- the measure / unit words read so far (Lipi numbers) ----
UNITS = {
    '705': 'kalam', '706': 'kalam', '704': 'kalam?', '707': 'kalam?',
    '575': 'kotTai', '540': 'paRai', '320': 'paTi', '171': 'niRai',
    '700': 'cup', '703': 'cup-3?', '701': 'cup-2?',
    '711': 'pot', '335': 'bin', '605': 'granary-bin', '590': 'chest',
    '740': 'jar', '061': 'kAl(quarter)', '063': 'kAl?', '062': 'kAl?',
    '817': 'hand', '861': 'hand', '055': 'dozen', '048': 'seven-string', '049': 'seven-string?',
}
# one name per unit for grouping
UNIT_OF = {s: v.split('(')[0].rstrip('?') for s, v in UNITS.items()}
UNIT_OF.update({'705': 'kalam', '706': 'kalam', '704': 'kalam', '707': 'kalam', '703': 'cup', '701': 'cup',
                '817': 'hand', '861': 'hand', '061': 'kAl', '062': 'kAl', '063': 'kAl', '048': 'seven', '049': 'seven'})


def runs(tok):
    """number runs in a token list: list of (start, end_exclusive, value or None, series string)."""
    out = []; i = 0; n = len(tok)
    while i < n:
        if tok[i] in NUM:
            j = i
            while j < n and tok[j] in NUM: j += 1
            vals = [NUM[t][1] for t in tok[i:j]]; ser = ''.join(sorted({NUM[t][0] for t in tok[i:j]}))
            out.append((i, j, None if any(v is None for v in vals) else sum(vals), ser))
            i = j
        else:
            i += 1
    return out


def site_of_M(r):
    return r.site_l


def faces(cat='L'):
    """rows: dict(cat, obj, cisi, face_id, tok, kind, site, area, type, material, broken, sideline)"""
    out = []
    if 'L' in cat:
        for r in d.itertuples(index=False):
            out.append(dict(cat='L', cisi=r.cisi, fid=r.id, tok=tuple(r.tok), kind=r.kind, site=r.site,
                            area=getattr(r, '_4', ''), type=r.type, material=r.material,
                            broken=not r.complete_txt, text=r.text))
    if 'Mu' in cat:
        for r in M[~M.partnered].itertuples(index=False):
            out.append(dict(cat='Mu', cisi=f'M{r.textnum}', fid=f'M{r.textnum}.{r.sideline}', tok=tuple(r.tok),
                            kind=r.kind, site=r.site_l, area=str(r.fs), type=r.cls, material='',
                            broken=not r.complete_b, text=r.reading_lipi))
    return out


def area_col():
    return d['area-section']


def unit_counts(face_rows):
    """every place a number run touches a unit sign: one row per (unit sign, side)."""
    rows = []
    for f in face_rows:
        t = f['tok']; R = runs(t)
        for (a, b, v, ser) in R:
            left = t[a - 1] if a > 0 else 'START'; right = t[b] if b < len(t) else 'END'
            for side, s, other in (('before', right, left), ('after', left, right)):
                # side = where the COUNT stands relative to the unit sign: 'before' = "n UNIT", 'after' = "UNIT n"
                if s in UNITS:
                    rows.append(dict(cat=f['cat'], cisi=f['cisi'], fid=f['fid'], sign=s, unit=UNIT_OF[s], side=side,
                                     value=v, series=ser, run=' '.join(t[a:b]), other=other,
                                     other_is_unit=other in UNITS, kind=f['kind'], site=f['site'],
                                     text=' '.join(t)))
    return pd.DataFrame(rows)
