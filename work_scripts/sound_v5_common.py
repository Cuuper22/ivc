#!/usr/bin/env python3
"""Shared kit for the fifth sound pass (sound_v5_*.py): the fourth-pass kit plus the fact kinds used in this pass
that earlier passes did not print: the sign two places away, the reverse face of a many-faced object,
the image on a copper tablet, and a face-level test on the two-sided tablets.
Import: from sound_v5_common import *"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound_v4_common import *
OUT5 = f'{ROOT}/work_data/sound_v5'
os.makedirs(OUT5, exist_ok=True)
CLOSE = {'740', '090', '400', '520'} | PORTER
NUMCUP = set(VAL) | {'700'}
HORNED = {'Bull1', 'Bull', 'Bull2', 'Bull3', 'Gaur', 'Zebu', 'Buff', 'Goat', 'CompBull'}


def two_away(s, t, offs=(2,), cat='LM'):
    """the sign two places after (offset +2) / before (-2) s is one of t, against how often t stands at that offset from
    any sign. '^' / '$' in t stand for the start / end of the text (padded, so a text end two places away counts)."""
    t = set(t) if not isinstance(t, str) else {t}
    k = n = K = N = 0
    for x, P, st, g in faces_all(cat):
        if '000' in x: continue
        y = ('^',) + tuple(x) + ('$',)
        for i in range(1, len(y) - 1):
            for o in offs:
                j = i + o
                if j < 0 or j >= len(y): continue
                hit = y[j] in t
                N += 1; K += hit
                if y[i] == s: n += 1; k += hit
    if n < 3: return None
    p = binomtest(k, n, K / N, alternative='greater').pvalue
    return res(k / n > K / N, p, f'sign at offset {"/".join(f"{o:+d}" for o in offs)} in {sorted(t)[:5]}{"..." if len(t) > 5 else ""}: {k}/{n} = {k / n:.0%} against {K / N:.1%} ({cat})')


def reverse_has(s, t, kinds=None):
    """on Lipi objects with 2+ faces: the face(s) other than the one carrying s hold one of t, against the same share
    for every face of 2+ face objects (each face's other faces)."""
    t = set(t)
    allm, sub = [], []
    for o in objs[objs.nfaces > 1].itertuples():
        if kinds and o.kind not in kinds: continue
        fs = o.faces
        for i, x in enumerate(fs):
            other = set(a for j, z in enumerate(fs) if j != i for a in z)
            hit = bool(other & t)
            allm.append(hit)
            if s in x and s not in other: sub.append(hit)
    return share(allm, sub, f'faces with it on 2+ face objects whose other face holds {sorted(t)[:5]}{"..." if len(t) > 5 else ""}')


def ctab_image(s, animals):
    """copper tablets carrying s show one of the given animals on the image side, against all copper tablets with an image."""
    c = objs[(objs.kind == 'ctab') & ~objs.animal.isin(['', '-', 'Othr', 'Unknown'])]
    return share(c.animal.isin(animals), c[c.signs.apply(lambda z: s in z)].animal.isin(animals), f'copper tablets with an image showing {"/".join(sorted(animals))[:40]}')


def _hp_time():
    t = d.groupby('obj').time.first(); return t


def harappa_late(s):
    """Harappa objects with s come from Period 3C (the late phase of the mature city) more than Harappa objects
    dated to a single sub-phase (3A, 3B or 3C) overall."""
    T = _hp_time()
    H = objs[(objs.site == 'Harappa')].copy(); H['time'] = T.reindex(H.index).values
    H = H[H.time.str.contains(r'3A|3B|3C', na=False) & ~H.time.str.contains('3B/C', na=False)]
    late = H.time.str.contains('3C')
    return share(late, late[H.signs.apply(lambda z: s in z)], 'Harappa objects from Period 3C')
