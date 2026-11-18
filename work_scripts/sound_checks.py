#!/usr/bin/env python3
"""Task 5: every new value makes one prediction (test id in sound_values.VALUES, direction fixed before the run).
Runs each test on the data on disk and writes work_data/sound/checks.csv.
"came true" = the measured direction is the predicted one and the one-sided P <= 0.10 (shuffle or exact test)."""
import sys, os, collections, random, statistics
import numpy as np, pandas as pd
from scipy.stats import mannwhitneyu, binomtest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gloss2 import load2, learn, parse_face, CNT
from sound_values import VALUES
ROOT = '/home/antigravity/Cuuper22/ivc'
rng = np.random.default_rng(7)
SHORT = {f'{i:03d}' for i in range(1, 8)} | {f'{i:03d}' for i in range(12, 19)}
TALL = {f'{i:03d}' for i in range(31, 37)}
VAL = {f'{i:03d}': i for i in range(1, 8)}; VAL.update({'012': 2}); VAL.update({f'{i:03d}': i - 10 for i in range(13, 19)}); VAL.update({f'{i:03d}': i - 30 for i in range(31, 37)})

print('stage 1/3: loading and parsing ...', flush=True)
d = load2(); lex = learn(d)
d['obj'] = d.id.str.split('.').str[0]
d['R'] = [parse_face(x, lex)['roles'] for x in d.tok]
d['P'] = [parse_face(x, lex) for x in d.tok]
objs = d.groupby('obj').agg(signs=('tok', lambda s: set(a for t in s for a in t)), type=('type', 'first'), site=('site', 'first'),
                            area=('area-section', 'first'), bh=('block-house', 'first'), symbol=('symbol', 'first'),
                            h=('horizontal(mm)', 'first'), v=('vertical(mm)', 'first'), nfaces=('id', 'count'),
                            faces=('tok', list))
objs['seal'] = objs.type.str.startswith('SEAL')
objs['face'] = pd.to_numeric(objs.h, errors='coerce') * pd.to_numeric(objs.v, errors='coerce')
objs['noanimal'] = objs.symbol.isin(['-', 'None', ''])
moh = objs[(objs.site == 'Mohenjo-daro') & ~objs.bh.isin(['--', '-', '']) & (objs.bh.str.len() > 0)].copy()
moh['house'] = moh.area + '|' + moh.bh
hc = moh.house.astype('category').cat.codes.values

def t_house(s):
    x = moh.signs.apply(lambda z: s in z).values.astype(int)
    if x.sum() < 2: return None
    def pairs(v):
        c = np.bincount(hc, weights=v); return float((c * (c - 1) / 2).sum())
    obs = pairs(x); sims = [pairs(rng.permutation(x)) for _ in range(1000)]
    e = np.mean(sims); p = (np.sum(np.array(sims) >= obs) + 1) / 1001
    return obs > e, p, f'same-house pairs {obs:.0f} against {e:.2f} by chance (Mohenjo-daro, {x.sum()} objects)'

def t_size(s, up):
    se = objs[objs.seal & (objs.face > 0)]
    a = se[se.signs.apply(lambda z: s in z)].face; b = se[~se.signs.apply(lambda z: s in z)].face
    if len(a) < 3: return None
    p = mannwhitneyu(a, b, alternative='greater' if up else 'less').pvalue
    ok = (a.median() > b.median()) if up else (a.median() < b.median())
    return ok, p, f'seal face median {a.median():.0f} mm2 (n {len(a)}) against {b.median():.0f}'

def share_test(mask_all, mask_s, label):
    base = mask_all.mean(); k = int(mask_s.sum()); n = len(mask_s)
    if n < 3: return None
    p = binomtest(k, n, base, alternative='greater').pvalue
    return k / n > base, p, f'{label} {k}/{n} = {k / n:.0%} against {base:.0%} for all objects'

def has(s): return objs.signs.apply(lambda z: s in z)
def t_record(s): return share_test(~objs.seal, ~objs[has(s)].seal, 'non-seal objects')
def t_noanimal(s): return share_test(objs.noanimal, objs[has(s)].noanimal, 'objects with no animal')
def t_granary(s):
    H = objs[objs.site == 'Harappa']; return share_test(H.area.str.startswith('F'), H[H.signs.apply(lambda z: s in z)].area.str.startswith('F'), 'Harappa objects from mound F')

def counts_on(s, side='before'):
    out = []
    for x, R in zip(d.tok, d.R):
        for i, a in enumerate(x):
            if a == s:
                if side in ('before', 'both') and i > 0 and x[i - 1] in VAL: out.append(x[i - 1])
                if side in ('after', 'both') and i + 1 < len(x) and x[i + 1] in VAL: out.append(x[i + 1])
    return out
def t_short(s):
    c = counts_on(s); sh = sum(a in SHORT for a in c); ta = sum(a in TALL for a in c)
    if sh + ta < 3: return None
    p = binomtest(sh, sh + ta, 0.5, alternative='greater').pvalue
    return sh > ta, p, f'counts written before it: short {sh}, tall {ta}'
def t_le3(s):
    c = counts_on(s, 'both'); v = [VAL[a] for a in c]
    if len(v) < 3: return None
    k = sum(x <= 3 for x in v); return k / len(v) >= 0.95, (1.0 if k / len(v) < 0.95 else 0.0), f'counts beside it <= 3: {k} of {len(v)} (values {collections.Counter(v).most_common()})'
def t_wheel3(s):
    c = counts_on(s, 'after'); v = [VAL[a] for a in c]; k = sum(x <= 3 for x in v)
    return k / len(v) >= 0.98, (0.0 if k / len(v) >= 0.98 else 1.0), f'counts after the wheel <= 3: {k} of {len(v)} (values {collections.Counter(v).most_common()})'
def t_jar(s):
    tot = hit = 0; bt = bh = 0
    for x, R in zip(d.tok, d.R):
        for i, a in enumerate(x):
            if R[i] in ('crest', 'self', 'tag'):
                nx = x[i + 1] if i + 1 < len(x) else ''
                bt += 1; bh += nx == '740'
                if a == s: tot += 1; hit += nx == '740'
    if tot < 3: return None
    p = binomtest(hit, tot, bh / bt, alternative='greater').pvalue
    return hit / tot > bh / bt, p, f'right before the jar {hit}/{tot} = {hit / tot:.0%} against {bh / bt:.0%} for all name-slot signs'
def t_cupface(s):
    M = objs[objs.nfaces >= 2]
    other = []
    for faces in M.faces:
        fs = [set(f) for f in faces]
        sface = [i for i, f in enumerate(fs) if s in f]
        other.append(bool(sface) and any('700' in f for j, f in enumerate(fs) if j not in sface))
    other = np.array(other); hs = M.faces.apply(lambda fs: any(s in f for f in fs)).values
    base = np.array([any('700' in f for f in fs) for fs in M.faces]).mean()
    k, n = int(other[hs].sum()), int(hs.sum())
    if n < 3: return None
    p = binomtest(k, n, base, alternative='greater').pvalue
    return k / n > base, p, f'two-or-more-face objects with a cup face beside the face carrying it {k}/{n} = {k / n:.0%} against {base:.0%}'
def t_two(s):
    a = b = c = e = 0
    for x, P in zip(d.tok, d.P):
        if not P['names']: continue
        two = len(P['jars']) >= 2 or len(P['names']) >= 2
        a += 1; b += two
        if s in x: c += 1; e += two
    p = binomtest(e, c, b / a, alternative='greater').pvalue
    return e / c > b / a, p, f'texts with two names or two jars {e}/{c} = {e / c:.0%} against {b / a:.0%}'
def t_multicount(s):
    a = b = c = e = 0
    for x in d.tok:
        idx = [i for i, t in enumerate(x) if t == s]
        other = any(t in VAL and all(abs(i - j) > 1 for j in idx) for i, t in enumerate(x))
        a += 1; b += other
        if idx: c += 1; e += other
    p = binomtest(e, c, b / a, alternative='greater').pvalue
    return e / c > b / a, p, f'texts with a second count away from it {e}/{c} = {e / c:.0%} against {b / a:.0%}'
def t_ord(s):
    c = collections.Counter()
    for x in d.tok:
        for i in range(len(x) - 1):
            if x[i] == '060' and x[i + 1] in ('741', '742', '745'): c[x[i + 1]] += 1
    ok = c['741'] > c['742'] > c['745']
    return ok, (0.0 if ok else 1.0), f'after the 060 mark: jar+1 {c["741"]}, jar+2 {c["742"]}, jar+3 {c["745"]} (falls like ordinals 1st > 2nd > 3rd)'
def t_crest(s):
    g = collections.defaultdict(lambda: [0, 0])
    for x, P in zip(d.tok, d.P):
        R = P['roles']
        if not x or len(x) < 3: continue
        op = '820' if x[0] == '820' else 'D' if x[0] in ('861', '817') else None
        if op is None or not P['names']: continue
        g[op][0] += 1; g[op][1] += 'crest' in R
    (n1, k1), (n2, k2) = g['D'], g['820']
    from scipy.stats import fisher_exact
    p = fisher_exact([[k1, n1 - k1], [k2, n2 - k2]], alternative='greater')[1]
    return k1 / n1 > k2 / n2, p, f'texts whose name opens with a house crest: diamond opener {k1}/{n1} = {k1 / n1:.0%}, wheel {k2}/{n2} = {k2 / n2:.0%}'

TESTS = {'H': t_house, 'SU': lambda s: t_size(s, True), 'SD': lambda s: t_size(s, False), 'R': t_record, 'NA': t_noanimal,
         'G': t_granary, 'CS': t_short, 'LE3': t_le3, 'WHEEL3': t_wheel3, 'J': t_jar, 'CUPFACE': t_cupface, 'TWO': t_two,
         'MULTICOUNT': t_multicount, 'ORD': t_ord, 'CREST': t_crest}
WHAT = {'H': 'house-mates share it (a house/kin word repeats inside one house)', 'SU': 'seals carrying it are bigger (a high rank)',
        'SD': 'seals carrying it are smaller (a low rank)', 'R': 'it lives on records (tablets, tags, pots, copper), not seals',
        'NA': 'objects carrying it have no animal (a goods word, not an owner word)', 'G': 'at Harappa it sits in the granary mound F',
        'CS': 'it is counted with short strokes (living or grown things)', 'LE3': 'counts beside it never pass three (a quarter)',
        'WHEEL3': 'the wheel never takes a count above three (quarters)', 'J': 'it stands right before the jar (a kin or house word)',
        'CUPFACE': 'on multi-face tablets it sits beside a cup face (a levy or weight paid in cups)',
        'TWO': 'its texts name two parties (a pair word)', 'MULTICOUNT': 'its texts carry a second number (a date: month + day)',
        'ORD': 'the 060 + jar-with-strokes selector falls 1 > 2 > 3 (ordinals)', 'CREST': 'diamond ("share, hereditary holding") seals name houses more than wheel seals'}

print('stage 2/3: running', len(VALUES), 'checks ...', flush=True)
rows = []
for k, (s, pic, pw, jw, snd, gl, kind, t) in enumerate(VALUES):
    r = TESTS[t](s)
    if r is None: rows.append(dict(sign=s, sound=snd, test=t, prediction=WHAT[t], result='too few cases', came_true='n/a', p='')); continue
    ok, p, txt = r
    rows.append(dict(sign=s, sound=snd, test=t, prediction=WHAT[t], result=txt, came_true='yes' if ok and p <= 0.10 else 'direction only' if ok else 'no', p=f'{p:.3g}'))
    if (k + 1) % 10 == 0: print(f'   {k + 1}/{len(VALUES)} checks done', flush=True)
out = pd.DataFrame(rows); out.to_csv(f'{ROOT}/work_data/sound/checks.csv', index=False)
print('stage 3/3:', out.came_true.value_counts().to_dict())
