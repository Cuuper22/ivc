#!/usr/bin/env python3
"""Shared loader and test kit for the second sound pass (sound_v2_*.py).

Objects table (Lipi), Mohenjo-daro houses with depth bands, every face parsed with gloss2,
the second catalogue (Mahadevan 1977) mapped to Lipi numbers through the crosswalk, and the
test primitives each value's prediction is run with.  Reading order = stored order reversed
(gloss.load already does it).
Import: from v2_common import *
"""
import sys, os, re, collections
import numpy as np, pandas as pd
from scipy.stats import mannwhitneyu, binomtest, fisher_exact
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gloss2 import load2, learn, parse_face, CNT

ROOT = '/home/claude/ivc'
rng = np.random.default_rng(11)
SHORT = {f'{i:03d}' for i in range(1, 8)} | {'012'} | {f'{i:03d}' for i in range(13, 19)}
TALL = {f'{i:03d}' for i in range(31, 37)}
VAL = {k: v[1] for k, v in CNT.items() if v[0] != 'comb'}
FISH = {'220', '235', '240', '233', '231', '226', '236'}
PORTER = {'151', '153', '154', '155', '156', '157', '158'}

print('[v2_common] loading Lipi faces and parsing ...', flush=True)
d = load2(); lex = learn(d)
d['obj'] = d.id.str.split('.').str[0]
d['P'] = [parse_face(x, lex) for x in d.tok]
d['R'] = [p['roles'] for p in d.P]


def _dep(s):
    m = re.search(r'-?\d+\.?\d*', str(s)); return abs(float(m.group(0))) if m else np.nan


objs = d.groupby('obj').agg(signs=('tok', lambda s: set(a for t in s for a in t)), type=('type', 'first'), site=('site', 'first'),
                            area=('area-section', 'first'), bh=('block-house', 'first'), depth=('depth', 'first'),
                            symbol=('symbol', 'first'), h=('horizontal(mm)', 'first'), v=('vertical(mm)', 'first'),
                            nfaces=('id', 'count'), faces=('tok', list), parses=('P', list), cisi=('cisi', 'first'),
                            group=('group', 'first'))
objs['seal'] = objs.type.str.startswith('SEAL')
objs['face'] = pd.to_numeric(objs.h, errors='coerce') * pd.to_numeric(objs.v, errors='coerce')
objs['animal'] = objs.symbol.str.split(':').str[0]
objs['noanimal'] = objs.symbol.isin(['-', 'None', ''])
objs['dep'] = objs.depth.map(_dep)
objs['nsign'] = objs.faces.apply(lambda fs: max(len(f) for f in fs))
# per-object name signs (all name groups on all faces) and the master name / ending of the main face
def _names(ps):
    out = []
    for p in ps:
        for g in p['names']: out.append(tuple(g))
    return out
objs['names'] = objs.parses.apply(_names)
def _ending(fs, ps):
    # seal ending as in the endings job: jar (+ man), spear, porter, comb
    for x, p in zip(fs, ps):
        if '740' in x:
            j = max(i for i, a in enumerate(x) if a == '740')
            return 'jar+man' if j + 1 < len(x) and x[j + 1] == '090' else 'jar'
        if x and x[-1] == '520': return 'spear'
        if x and x[-1] in PORTER: return 'porter'
        if x and x[-1] == '400': return 'comb'
    return 'none'
objs['ending'] = [_ending(f, p) for f, p in zip(objs.faces, objs.parses)]
objs['name'] = [tuple(p[0]['name']) if p else () for p in objs.parses]

moh = objs[(objs.site == 'Mohenjo-daro') & ~objs.bh.isin(['--', '-', '']) & (objs.bh.str.len() > 0)].copy()
moh['house'] = moh.area + '|' + moh.bh
moh['band'] = moh.area + '|' + (moh.dep // 3).astype(str)

# ---------------- second catalogue ----------------
print('[v2_common] loading the second catalogue ...', flush=True)
M = pd.read_csv(f'{ROOT}/work_data/mahadevan_parsed.csv', dtype=str).fillna('')
M['tok'] = M.reading_lipi.str.split('-').apply(tuple)
M['complete_b'] = M.complete == 'True'
pairs = pd.read_csv(f'{ROOT}/work_data/crosswalk_text_pairs.csv', dtype=str)
partnered = set(pairs.mahadevan_text)
M['partnered'] = M.reading_mah.isin(partnered)
M['P'] = [parse_face(x, lex) for x in M.tok]
MSITE = {'MD': 'Mohenjo-daro', 'HP': 'Harappa', 'LL': 'Lothal', 'KB': 'Kalibangan', 'CD': 'Chanhu-daro', 'OS': 'other', 'WA': 'abroad'}
M['site_l'] = M.site.map(MSITE).fillna('other')


def faces_all(cat='L'):
    """list of (tokens, parse, site, group) for every face; cat L, M (all Mahadevan) or LM (Lipi + Mahadevan with no Lipi partner)."""
    out = []
    if 'L' in cat:
        out += list(zip(d.tok, d.P, d.site, d.group))
    if cat == 'M':
        out += list(zip(M.tok, M.P, M.site_l, M.cls))
    elif 'M' in cat:
        m = M[~M.partnered]; out += list(zip(m.tok, m.P, m.site_l, m.cls))
    return out


# ---------------- primitives: each returns (ok, p, text) or None ----------------
def res(ok, p, txt): return (bool(ok), float(p), txt)


def house_share(s, where='name', pos=None, band=True, seals=True, nshuf=2000, pred=None):
    """Mohenjo-daro house-mates both carry s (in a name group; pos='first'/'last'/'prejar' narrows it).
    Chance: house labels shuffled among objects of the same area and 3-ft depth band (band=True) or among all."""
    H = moh[moh.seal] if seals else moh
    def has(o):
        if pred is not None: return pred(o)
        if where == 'any': return s in o.signs
        for g in o.names:
            if pos is None and s in g: return True
            if pos == 'first' and len(g) >= 2 and g[0] == s: return True
            if pos == 'last' and len(g) >= 2 and g[-1] == s: return True
            if pos == 'single' and g == (s,): return True
        if pos == 'prejar':
            for x in o.faces:
                for i in range(len(x) - 1):
                    if x[i] == s and x[i + 1] == '740': return True
        return False
    x = np.array([has(o) for o in H.itertuples()], dtype=int)
    if x.sum() < 2: return None
    hc = H.house.astype('category').cat.codes.values
    bands = H.band.values if band else np.zeros(len(H))
    def pairs(v):
        c = np.bincount(hc, weights=v); return float((c * (c - 1) / 2).sum())
    obs = pairs(x); sims = []
    idx_by_band = collections.defaultdict(list)
    for i, b in enumerate(bands): idx_by_band[b].append(i)
    for _ in range(nshuf):
        y = x.copy()
        for b, ii in idx_by_band.items():
            if len(ii) > 1: y[ii] = rng.permutation(x[ii])
        sims.append(pairs(y))
    e = np.mean(sims); p = (np.sum(np.array(sims) >= obs) + 1) / (nshuf + 1)
    return res(obs > e, p, f'same-house pairs {obs:.0f} against {e:.2f} (Mohenjo-daro {"seals" if seals else "objects"}, {x.sum()} carry it, shuffled within area and 3-ft band)')


def seal_size(s, up=True, adjust=True):
    """seals carrying s bigger (up) / smaller than seals with the same number of signs."""
    se = objs[objs.seal & (objs.face > 0)].copy()
    se['has'] = se.signs.apply(lambda z: s in z)
    if se.has.sum() < 4: return None
    if adjust:
        med = se.groupby('nsign').face.median(); se['rel'] = se.face / se.nsign.map(med)
        a, b = se[se.has].rel, se[~se.has].rel
        p = mannwhitneyu(a, b, alternative='greater' if up else 'less').pvalue
        ok = a.median() > 1 if up else a.median() < 1
        return res(ok, p, f'seal face against seals of the same sign count: x{a.median():.2f} (n {len(a)})')
    a, b = se[se.has].face, se[~se.has].face
    p = mannwhitneyu(a, b, alternative='greater' if up else 'less').pvalue
    return res((a.median() > b.median()) == up, p, f'seal face median {a.median():.0f} against {b.median():.0f} mm2 (n {len(a)})')


def share(mask_all, mask_s, label):
    base = float(np.mean(mask_all)); k = int(np.sum(mask_s)); n = len(mask_s)
    if n < 3: return None
    p = binomtest(k, n, base, alternative='greater').pvalue
    return res(k / n > base, p, f'{label} {k}/{n} = {k / n:.0%} against {base:.0%}')


def share_less(mask_all, mask_s, label):
    base = float(np.mean(mask_all)); k = int(np.sum(mask_s)); n = len(mask_s)
    if n < 3: return None
    p = binomtest(k, n, base, alternative='less').pvalue
    return res(k / n < base, p, f'{label} {k}/{n} = {k / n:.0%} against {base:.0%}')


def has_obj(s): return objs.signs.apply(lambda z: s in z)


def adjacent(s, t, side='next', cat='L', within_names=False):
    """how often s is directly followed (next) / preceded (prev) by any of t (set) against t's share among all neighbours."""
    t = set(t) if not isinstance(t, str) else {t}
    k = n = K = N = 0
    for x, P, site, g in faces_all(cat):
        for i, a in enumerate(x):
            j = i + 1 if side == 'next' else i - 1
            if j < 0 or j >= len(x): continue
            N += 1; K += x[j] in t
            if a == s: n += 1; k += x[j] in t
    if n < 3: return None
    p = binomtest(k, n, K / N, alternative='greater').pvalue
    return res(k / n > K / N, p, f'{side} sign in {sorted(t)[:4]}{"..." if len(t) > 4 else ""}: {k}/{n} = {k / max(n, 1):.0%} against {K / N:.1%} ({cat})')


def counts_beside(s, cat='L', side='both'):
    out = []
    for x, P, site, g in faces_all(cat):
        for i, a in enumerate(x):
            if a != s: continue
            if side in ('before', 'both') and i > 0 and x[i - 1] in VAL: out.append(x[i - 1])
            if side in ('after', 'both') and i + 1 < len(x) and x[i + 1] in VAL: out.append(x[i + 1])
    return out


def count_series(s, want='tall', cat='L', side='both'):
    c = counts_beside(s, cat, side); sh = sum(a in SHORT for a in c); ta = sum(a in TALL for a in c)
    if sh + ta < 3: return None
    # base: share of tall among all counts in the catalogue
    allc = [a for x, P, site, g in faces_all(cat) for a in x if a in VAL]
    bt = sum(a in TALL for a in allc) / max(1, sum((a in TALL) or (a in SHORT) for a in allc))
    k = ta if want == 'tall' else sh; base = bt if want == 'tall' else 1 - bt
    p = binomtest(k, sh + ta, base, alternative='greater').pvalue
    return res(k / (sh + ta) > base, p, f'counts beside it: tall {ta}, short {sh} (tall share {ta / (sh + ta):.0%} against {bt:.0%} for all counts; {cat})')


def cooccur(s, t, cat='L', unit='face'):
    """s and any of t on the same face (unit face) more often than chance (Fisher)."""
    t = set(t) if not isinstance(t, str) else {t}
    A = B = AB = N = 0
    if unit == 'object' and cat == 'L':
        rows = [o for o in objs.signs]
    else:
        rows = [set(x) for x, P, site, g in faces_all(cat)]
    for z in rows:
        a = s in z; b = bool(z & t) and not (t == {s})
        N += 1; A += a; B += b; AB += a and b
    if A < 3: return None
    p = fisher_exact([[AB, A - AB], [B - AB, N - A - B + AB]], alternative='greater')[1]
    e = A * B / N
    return res(AB > e, p, f'with {sorted(t)[:5]}{"..." if len(t) > 5 else ""} on one {unit}: {AB} of {A} against {e:.1f} expected ({cat})')


def ending_of_names(s, ending, pos=None, cat='L'):
    """names containing s (pos first/last) take the given ending more often than names in general.
    cat L uses seal objects; cat M/LM uses second-catalogue seals parsed the same way."""
    def name_end(x, P):
        if '740' in x:
            j = max(i for i, a in enumerate(x) if a == '740'); return 'jar+man' if j + 1 < len(x) and x[j + 1] == '090' else 'jar'
        if x and x[-1] == '520': return 'spear'
        if x and x[-1] in PORTER: return 'porter'
        if x and x[-1] == '400': return 'comb'
        return 'none'
    rows = []
    if 'L' in cat:
        se = objs[objs.seal]
        for nm, e in zip(se.name, se.ending): rows.append((nm, e))
    if 'M' in cat:
        m = M[(M.cls == 'seal') & ((~M.partnered) if cat == 'LM' else True)]
        for x, P in zip(m.tok, m.P): rows.append((tuple(P['name']), name_end(x, P)))
    rows = [(nm, e) for nm, e in rows if nm and e != 'none' and '000' not in nm]
    def hit(nm):
        if pos == 'first': return nm[0] == s
        if pos == 'last': return nm[-1] == s
        return s in nm
    E = set(ending) if not isinstance(ending, str) else {ending}
    base = np.mean([e in E for nm, e in rows]); sub = [e in E for nm, e in rows if hit(nm)]
    if len(sub) < 3: return None
    k = sum(sub); n = len(sub)
    p = binomtest(k, n, base, alternative='greater').pvalue
    return res(k / n > base, p, f'names with it{" " + pos if pos else ""} end in {"/".join(sorted(E))} {k}/{n} = {k / n:.0%} against {base:.0%} ({cat} seals)')


def text_pos(s, where='last', cat='L', complete=True):
    """share of s's uses that are text-final (last) / text-initial (first) against all signs."""
    k = n = K = N = 0
    for x, P, site, g in faces_all(cat):
        if not x or '000' in x: continue
        L = len(x)
        for i, a in enumerate(x):
            hit = (i == L - 1) if where == 'last' else (i == 0)
            N += 1; K += hit
            if a == s: n += 1; k += hit
    if n < 3: return None
    p = binomtest(k, n, K / N, alternative='greater').pvalue
    return res(k / n > K / N, p, f'{where} sign of the text {k}/{n} = {k / n:.0%} against {K / N:.0%} ({cat})')


def site_share(s, site, cat='L'):
    rows = faces_all(cat)
    allm = [st == site for x, P, st, g in rows]; sub = [st == site for x, P, st, g in rows if s in x]
    return share(allm, sub, f'faces at {site}')


def group_share(s, groups, cat='L'):
    groups = set(groups) if not isinstance(groups, str) else {groups}
    rows = faces_all(cat)
    allm = [g in groups for x, P, st, g in rows]; sub = [g in groups for x, P, st, g in rows if s in x]
    return share(allm, sub, f'faces on {"/".join(sorted(groups))}')


def harappa_area(s, prefix):
    H = objs[objs.site == 'Harappa']
    return share(H.area.str.startswith(prefix), H[H.signs.apply(lambda z: s in z)].area.str.startswith(prefix), f'Harappa objects from area {prefix}*')


def moh_area(s, prefix):
    H = objs[objs.site == 'Mohenjo-daro']
    return share(H.area.str.startswith(prefix), H[H.signs.apply(lambda z: s in z)].area.str.startswith(prefix), f'Mohenjo-daro objects from area {prefix}*')


def depth_rel(s, deeper=True):
    """Mohenjo-daro objects carrying s sit deeper (older) than other objects of the same area."""
    H = objs[(objs.site == 'Mohenjo-daro') & objs.dep.notna() & (objs.dep > 0)].copy()
    H['rel'] = H.dep - H.area.map(H.groupby('area').dep.median())
    a = H[H.signs.apply(lambda z: s in z)].rel; b = H[~H.signs.apply(lambda z: s in z)].rel
    if len(a) < 4: return None
    p = mannwhitneyu(a, b, alternative='greater' if deeper else 'less').pvalue
    return res((a.median() > b.median()) == deeper, p, f'depth below its area median {a.median():+.1f} ft against {b.median():+.1f} (n {len(a)})')


def animal_share(s, animals):
    animals = set(animals) if not isinstance(animals, str) else {animals}
    se = objs[objs.seal]
    return share(se.animal.isin(animals), se[se.signs.apply(lambda z: s in z)].animal.isin(animals), f'seals with animal {"/".join(sorted(animals))}')


def name_partner_diversity(s, side='after'):
    """a house/lineage element takes many different personal elements: distinct next signs inside names per use,
    against signs of similar frequency (shuffle of name contents is too slow; compare with frequency-matched signs)."""
    use = collections.Counter(); nxt = collections.defaultdict(set)
    for nm in objs.names:
        for g in nm:
            for i, a in enumerate(g):
                j = i + 1 if side == 'after' else i - 1
                if 0 <= j < len(g) and g[j] not in ('000', 'ALT'):
                    use[a] += 1; nxt[a].add(g[j])
    if use[s] < 5: return None
    ratio = len(nxt[s]) / use[s]
    peers = [len(nxt[a]) / use[a] for a in use if a != s and 0.5 * use[s] <= use[a] <= 2 * use[s]]
    k = sum(r < ratio for r in peers)
    p = 1 - k / max(1, len(peers))
    return res(ratio > np.median(peers), p, f'distinct name partners {side} it per use {ratio:.2f} ({len(nxt[s])}/{use[s]}) against median {np.median(peers):.2f} for {len(peers)} signs of similar frequency')


def multi_site(s, cat='L'):
    """a title/office word spreads over more sites than signs of the same frequency."""
    sites = collections.defaultdict(set); use = collections.Counter()
    for x, P, st, g in faces_all(cat):
        for a in set(x): sites[a].add(st); use[a] += 1
    if use[s] < 5: return None
    peers = [len(sites[a]) for a in use if a != s and 0.6 * use[s] <= use[a] <= 1.6 * use[s]]
    k = sum(v < len(sites[s]) for v in peers)
    return res(len(sites[s]) > np.median(peers), 1 - k / max(1, len(peers)), f'{len(sites[s])} sites against median {np.median(peers):.0f} for {len(peers)} signs of similar frequency ({cat})')


def custom(ok, p, txt): return res(ok, p, txt)
