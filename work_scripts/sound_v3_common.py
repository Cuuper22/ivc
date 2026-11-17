#!/usr/bin/env python3
"""Shared kit for the third sound pass (sound_v3_*.py): the v2 loader plus the object-kind anchor
(what an inscription is written on) for both catalogues, and a sign profile printer.
Kinds: seal, tag (clay tags and sealings), pot, tool (copper/bronze implements), bangle, rod (ivory/bone),
ctab (copper tablet), mtab (moulded/incised miniature tablets), other.
Import: from sound_v3_common import *"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from v2_common import *
OUT3 = f'{ROOT}/work_data/sound_v3'
os.makedirs(OUT3, exist_ok=True)


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


KIND_M = {'seal': 'seal', 'sealing': 'tag', 'pottery graffito': 'pot', 'bronze implement': 'tool', 'ivory/bone rod': 'rod',
          'copper tablet': 'ctab', 'miniature tablet': 'mtab', 'miscellaneous': 'other'}
d['kind'] = d.type.map(kind_L)
M['kind'] = M.cls.map(KIND_M).fillna('other')
objs['kind'] = objs.type.map(kind_L)


def kfaces(cat='L'):
    """(tokens, kind, site) for each face. L = Lipi, Mu = second-catalogue texts with no Lipi partner (never used to choose)."""
    out = []
    if 'L' in cat: out += list(zip(d.tok, d.kind, d.site))
    if 'Mu' in cat or cat == 'LM':
        m = M[~M.partnered]; out += list(zip(m.tok, m.kind, m.site_l))
    return out


def on_kind(s, kinds, cat='Mu', label=None):
    """faces carrying s (any of s if a set) sit on the given object kinds more than all faces do."""
    S = {s} if isinstance(s, str) else set(s); K = {kinds} if isinstance(kinds, str) else set(kinds)
    rows = kfaces(cat)
    allm = np.array([k in K for x, k, st in rows]); sub = np.array([k in K for x, k, st in rows if S & set(x)])
    if len(sub) < 3: return None
    k = int(sub.sum()); n = len(sub); base = allm.mean()
    p = binomtest(k, n, base, alternative='greater').pvalue
    return res(k / n > base, p, f'faces on {"/".join(sorted(K))} {k}/{n} = {k / n:.0%} against {base:.0%} for all faces, x{(k / n) / base:.1f} ({cat})')


def off_kind(s, kinds, cat='Mu'):
    """faces carrying s avoid the given kinds (fewer than all faces)."""
    S = {s} if isinstance(s, str) else set(s); K = {kinds} if isinstance(kinds, str) else set(kinds)
    rows = kfaces(cat)
    allm = np.array([k in K for x, k, st in rows]); sub = np.array([k in K for x, k, st in rows if S & set(x)])
    if len(sub) < 3: return None
    k = int(sub.sum()); n = len(sub); base = allm.mean()
    p = binomtest(k, n, base, alternative='less').pvalue
    return res(k / n < base, p, f'faces on {"/".join(sorted(K))} {k}/{n} = {k / n:.0%} against {base:.0%} (should be fewer; {cat})')


def next_in(s, t, cat='Mu', side='next'):
    return adjacent(s, t, side, 'Mu' if cat == 'Mu' else cat)


def never_before_jar(s, cat='Mu'):
    """a goods/unit word should not close a name: share of s's uses right before the jar is under the name-slot base."""
    k = n = K = N = 0
    for x, P, st, g in faces_all(cat):
        for i, a in enumerate(x[:-1]):
            N += 1; K += x[i + 1] == '740'
            if a == s: n += 1; k += x[i + 1] == '740'
    if n < 3: return None
    p = binomtest(k, n, K / N, alternative='less').pvalue
    return res(k / n < K / N, p, f'right before the jar {k}/{n} = {k / n:.0%} against {K / N:.0%} for all signs (should be fewer; {cat})')


def with_count(s, cat='Mu'):
    """faces with s carry a number sign more than faces overall."""
    rows = faces_all(cat)
    allm = np.array([any(a in VAL for a in x) for x, P, st, g in rows]); sub = np.array([any(a in VAL for a in x) for x, P, st, g in rows if s in x])
    return share(allm, sub, f'faces with a number ({cat})') if len(sub) >= 3 else None


def profile(s, cat='L'):
    pv = collections.Counter(); nx = collections.Counter(); kinds = collections.Counter(); pos = collections.Counter(); sites = collections.Counter()
    for x, k, st in kfaces(cat):
        if s not in x: continue
        kinds[k] += 1; sites[st] += 1
        for i, a in enumerate(x):
            if a != s: continue
            pv[x[i - 1] if i else '^'] += 1; nx[x[i + 1] if i + 1 < len(x) else '$'] += 1
            pos['first' if i == 0 else 'last' if i == len(x) - 1 else 'mid'] += 1
    return dict(kinds=kinds.most_common(6), prev=pv.most_common(6), next=nx.most_common(6), pos=dict(pos), sites=sites.most_common(4))


def run(tag, sign, word, pred, fn):
    try: r = fn()
    except Exception as e: r = None; print('   error', e)
    if r is None: out = ('n/a', np.nan, 'too few cases')
    else:
        ok, p, txt = r
        out = ('yes' if ok and p <= 0.1 else 'direction only' if ok else 'no', p, txt)
    print(f'[{tag}] {sign} {word}: {pred}\n      -> {out[0]}: {out[2]}, P {out[1]:.3g}', flush=True)
    return dict(stage=tag, sign=sign, word=word, prediction=pred, outcome=out[0], p=out[1], result=out[2])


def frame_swap(a, b, cat='LM'):
    """a and b stand in the same frames (same sign before and after) more than b and signs of b's frequency do."""
    ctx = collections.defaultdict(set); use = collections.Counter(); seen = set()
    for x, P, st, g in faces_all(cat):
        if x in seen: continue
        seen.add(x); y = ('^',) + tuple(x) + ('$',)
        for i in range(1, len(y) - 1):
            ctx[y[i]].add((y[i - 1], y[i + 1])); use[y[i]] += 1
    bs = set(b) if not isinstance(b, str) else {b}
    cb = set().union(*[ctx[s] for s in bs]); nb = sum(use[s] for s in bs)
    if use[a] < 3 or nb < 3: return None
    obs = len(ctx[a] & cb)
    peers = [len(ctx[a] & ctx[s]) for s in use if s not in bs and s != a and 0.5 * nb <= use[s] <= 2 * nb]
    k = sum(v >= obs for v in peers)
    return res(obs > np.median(peers), (k + 1) / (len(peers) + 1), f'{obs} shared frames with {sorted(bs)} against median {np.median(peers):.0f} for {len(peers)} signs of the same frequency ({cat}, distinct texts)')


def no_jar(s, cat='L'):
    """faces with s carry the jar 740 less often than faces overall (a title or goods word in place of the possessive)."""
    rows = faces_all(cat)
    allm = np.array(['740' in x for x, P, st, g in rows]); sub = np.array(['740' in x for x, P, st, g in rows if s in x])
    return share_less(allm, sub, f'faces with the jar ({cat})') if len(sub) >= 3 else None


def prev_count(s, cat='Mu'): return adjacent(s, set(VAL), 'prev', cat)
def next_count(s, cat='Mu'): return adjacent(s, set(VAL), 'next', cat)
