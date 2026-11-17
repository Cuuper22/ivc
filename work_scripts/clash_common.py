#!/usr/bin/env python3
"""Shared kit for the two clash jobs (clash_335.py, clash_527.py).

Unit tests that compare how often a sign (or a set of signs) does something against how often ANY sign does it
in the same catalogue.  Two catalogues:
  L  = the first catalogue (Lipi, 5,679 faces)
  Mu = "new texts": the 1,183 second-catalogue lines with no partner in the first (never used to choose a value)
Two units:
  faces    = every face counts (a text stamped on 22 tablets counts 22 times)
  distinct = every different sign string counts once (copies collapse)
Each test says what word A and word B predict ('high' = more often than the base rate, 'low' = less often).
The result states the number, the base rate, the one-sided P in the observed direction, and which word it points to
(P at or under 0.1) or 'direction only'.
Import: from clash_common import *"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound_v4_common import *
from scipy.stats import binomtest

OUTC = f'{ROOT}/work_data/clash'
os.makedirs(OUTC, exist_ok=True)
CNTS = set(VAL)                                   # count signs (short strokes, tall strokes, stacked)
PERSON = {'090', '400', '520', '151', '153', '154', '155', '156', '157', '158'}   # man, comb, spear, carriers

# one table of faces for both catalogues: cat, tokens, kind, site, area, parse roles
_L = pd.DataFrame(dict(cat='L', tok=d.tok.values, kind=d.kind.values, site=d.site.values, area=d['area-section'].values,
                       roles=[p['roles'] for p in d.P], obj=d.obj.values))
_m = M[~M.partnered]
_M = pd.DataFrame(dict(cat='Mu', tok=_m.tok.values, kind=_m.kind.values, site=_m.site_l.values, area='',
                       roles=[p['roles'] for p in _m.P], obj=''))
FACES = pd.concat([_L, _M], ignore_index=True)
FACES['n'] = FACES.tok.apply(len)


def _dedupe(df):
    return df.drop_duplicates('tok')


def occ_test(signs, pred, cat, unit='faces', scope='occ', sub=None):
    """pred(face_row, i) -> bool for an occurrence of a sign at index i (scope 'occ': base = the same predicate over every
    sign occurrence of every face; scope 'face': pred(face_row, None) per face, base = all faces; the sign must be on the face).
    sub: optional function(face_row)->bool restricting the faces both for the sign and for the base.
    Returns dict(k, n, base, p_high, p_low, dir)."""
    S = {signs} if isinstance(signs, str) else set(signs)
    df = FACES[FACES.cat == cat]
    if unit == 'distinct': df = _dedupe(df)
    if sub is not None: df = df[df.apply(sub, axis=1)]
    k = n = K = N = 0
    for r in df.itertuples():
        x = r.tok
        if scope == 'face':
            v = bool(pred(r, None)); N += 1; K += v
            if S & set(x): n += 1; k += v
        else:
            for i, t in enumerate(x):
                v = bool(pred(r, i)); N += 1; K += v
                if t in S: n += 1; k += v
    if n == 0 or N == 0: return dict(k=0, n=0, base=np.nan, p_high=np.nan, p_low=np.nan, dir='n/a')
    b = K / N
    ph = binomtest(k, n, b, alternative='greater').pvalue
    pl = binomtest(k, n, b, alternative='less').pvalue
    return dict(k=k, n=n, base=b, p_high=ph, p_low=pl, dir='high' if k / n > b else 'low' if k / n < b else 'equal')


def verdict(res, says):
    """says = {'A': 'high'/'low', 'B': 'high'/'low'} -> (points_to, strength)."""
    if res['n'] == 0: return ('none', 'no uses')
    dr = res['dir']
    p = res['p_high'] if dr == 'high' else res['p_low']
    who = [h for h, s in says.items() if s == dr]
    if dr == 'equal' or not who: return ('none', 'equal')
    return (who[0], 'P<=0.1' if p <= 0.1 else 'direction only')


def line(tag, label, says, res, names):
    """printable one-line result."""
    pt, st = verdict(res, says)
    if res['n'] == 0:
        return dict(test=tag, what=label, unit_cat='', k='', n=0, share='', base='', P='', points_to='no uses', strength='')
    dr = res['dir']; p = res['p_high'] if dr == 'high' else res['p_low']
    return dict(test=tag, what=label, k=res['k'], n=res['n'], share=f"{res['k'] / res['n']:.0%}", base=f"{res['base']:.1%}",
                P=f'{p:.2g}', points_to=names.get(pt, pt), strength=st)


def frames_shared(a, b_set, cats=('L', 'Mu')):
    """distinct texts: frames (previous sign, next sign) that sign(s) a share with the set b_set, against frequency-matched peers."""
    A = {a} if isinstance(a, str) else set(a)
    df = _dedupe(FACES[FACES.cat.isin(cats)])
    ctx = collections.defaultdict(set); use = collections.Counter()
    for r in df.itertuples():
        y = ('^',) + tuple(r.tok) + ('$',)
        for i in range(1, len(y) - 1):
            ctx[y[i]].add((y[i - 1], y[i + 1])); use[y[i]] += 1
    ca = set().union(*[ctx[s] for s in A])
    cb = set().union(*[ctx[s] for s in b_set - A])
    nb = sum(use[s] for s in b_set - A)
    obs = len(ca & cb)
    peers = []
    for s in use:
        if s in A or s in b_set or s in ('^', '$'): continue
        if 0.5 * nb <= use[s] <= 2 * nb: peers.append(len(ca & ctx[s]))
    k = sum(v >= obs for v in peers)
    return dict(obs=obs, median=float(np.median(peers)) if peers else np.nan, npeers=len(peers), p=(k + 1) / (len(peers) + 1))


def print_table(rows, title):
    print('\n' + title, flush=True)
    df = pd.DataFrame(rows)
    print(df.to_string(index=False), flush=True)
    return df
