#!/usr/bin/env python3
"""STYLE step 4: what the styles line up with, shops, travelled stones, twins, other animals.
Predictions are in style_1_sample.py (P2-P6), written before coding. Test rules (fixed before running):
- V = Cramer's V of a cross-table. Chance = 5,000 shuffles; P = share of shuffles with V >= real.
- Letter: stones with a letter W/J/S/I/L; letters shuffled within city.
- City: 6 city groups (MD, HA, LO, KA, CH, OT); cities shuffled within size third (thirds of all coded stones).
- Size: mean log face area per style; style shuffled within city; statistic = between-style variance of log size.
- Time: within Mohenjo-daro and within Harappa, bins shuffled within city; pooled V over the two.
- Text: style x text kind (shuffle style within city); style x each fixed phrase found on >= 5 coded stones,
  per-cell two-sided P from shuffles, Benjamini-Hochberg q over all cells.
- Travelled: home share of the stone's style <= 10% and some other main city (>= 15 coded stones) has >= 25%.
  Text score = mean log-probability per transition under the sign-pair model of the style's city minus under the home
  city's model (models from every seal text of that city, the stone left out, add-0.1 smoothing, start and end marks).
  Chance = same score for other styled stones of the same home toward the same city (draw-matched, 5,000 draws).
- Twins: share of twin / near-twin pairs with the same style; chance = partner b redrawn among styled stones of b's city.
- Other animals: per feature (neck, shoulder, sign_cut, spacing) V feature x city (MD / HA / other), city shuffled within
  species.
Main styles = S1..S5; S6-S8 (8 stones) are kept in tables, left out of V tests.
"""
import sys, os, itertools, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_common import *
rng = np.random.default_rng(20261119); NS = 5000
D = pd.read_csv(f'{OUT}/styles.csv', dtype=str).fillna('')
D['logsz'] = np.log(pd.to_numeric(D.area_mm2, errors='coerce'))
MAIN = ['S1', 'S2', 'S3', 'S4', 'S5']
S = D[D.sty.isin(MAIN)].copy().reset_index(drop=True)
L = []
def out(*a): s = ' '.join(str(x) for x in a); print(s); L.append(s)

def cv(a, b):
    t = pd.crosstab(a, b).values.astype(float)
    if t.shape[0] < 2 or t.shape[1] < 2: return 0.0
    e = t.sum(1, keepdims=True) * t.sum(0, keepdims=True) / t.sum()
    chi = ((t - e) ** 2 / np.where(e == 0, 1, e)).sum()
    return math.sqrt(chi / t.sum() / (min(t.shape) - 1))

def shuffle_within(vals, groups):
    vals = np.array(vals, dtype=object).copy(); g = np.array(groups)
    for k in set(g):
        ix = np.where(g == k)[0]; vals[ix] = vals[rng.permutation(ix)]
    return vals

def vtest(a, b, strata, which='b', label=''):
    real = cv(a, b); sims = []
    for _ in range(NS):
        if which == 'b': sims.append(cv(a, shuffle_within(b, strata)))
        else: sims.append(cv(shuffle_within(a, strata), b))
    sims = np.array(sims); p = (sims >= real).mean()
    out(f'{label}: V {real:.3f} against {sims.mean():.3f} shuffled (P {p:.4f})'); return real, sims.mean(), p

# ---------- 2. what the styles line up with
out('== Style table (all coded stones)'); out(pd.crosstab(D.sty, D.city, margins=True).to_string())
lt = S[S.letter.isin(list('WJSIL'))]
out('\n== Style x catalogue letter'); out(pd.crosstab(lt.sty, lt.letter, margins=True).to_string())
vtest(lt.sty.values, lt.letter.values, lt.city.values, 'b', 'style x letter, letters shuffled within city')
S['third'] = pd.qcut(S.logsz.rank(method='first'), 3, labels=['small', 'middle', 'big']).astype(str)
S.loc[S.logsz.isna(), 'third'] = 'nosize'
vtest(S.sty.values, S.city.values, S.third.values, 'b', 'style x city, cities shuffled within size third')
sz = S[S.logsz.notna()]
def between(st, y):
    m = y.mean(); return sum(((y[st == g].mean() - m) ** 2) * (st == g).sum() for g in set(st)) / len(y)
real = between(sz.sty.values, sz.logsz.values)
sims = np.array([between(shuffle_within(sz.sty.values, sz.city.values), sz.logsz.values) for _ in range(NS)])
out(f'style x size: between-style variance {real:.4f} against {sims.mean():.4f} (P {(sims >= real).mean():.4f})')
out('median face mm2 by style: ' + ', '.join(f'{g} {np.exp(sz[sz.sty == g].logsz).median():.0f} (n {(sz.sty == g).sum()})' for g in MAIN))
tb = S[S.bin.isin(['early', 'middle', 'late'])]
out('\n== Style x time bin'); out(pd.crosstab([tb.city, tb.bin], tb.sty).to_string())
for c in ['MD', 'HA']:
    sub = tb[tb.city == c]; vtest(sub.sty.values, sub.bin.values, sub.city.values, 'b', f'style x bin inside {c}')
vtest(tb.sty.values, tb.bin.values, tb.city.values, 'b', 'style x bin, all cities, bins shuffled within city')

# ---------- 3. text
out('\n== Style x text kind'); out(pd.crosstab(S.sty, S.kind, margins=True).to_string())
vtest(S.sty.values, S.kind.values, S.city.values, 'a', 'style x text kind, style shuffled within city')
PH = pd.read_csv(f'{ROOT}/work_data/phrases/phrase_list.csv', dtype=str)
def has(sig, ph): return ('-' + sig + '-').find('-' + ph + '-') >= 0
cells = []
sty = S.sty.values; city = S.city.values
SH = np.array([shuffle_within(sty, city) for _ in range(1000)])
for ph in PH.phrase:
    x = np.array([has(s, ph) for s in S.signs])
    if x.sum() < 5: continue
    for g in MAIN:
        real = int(((sty == g) & x).sum())
        sims = ((SH == g) & x[None, :]).sum(1)
        p = min(1.0, 2 * min((sims >= real).mean(), (sims <= real).mean()))
        cells.append((ph, g, int(x.sum()), real, sims.mean(), p))
C = pd.DataFrame(cells, columns=['phrase', 'style', 'stones_with_phrase', 'real', 'dealt', 'p'])
if len(C):
    C = C.sort_values('p'); m = len(C); C['q'] = (C.p * m / np.arange(1, m + 1))[::-1].cummin()[::-1].clip(upper=1)
    C.to_csv(f'{OUT}/phrase_cells.csv', index=False)
    out(f'phrases on >= 5 coded stones: {C.phrase.nunique()}, cells {m}, P<0.05: {(C.p < 0.05).sum()} (expected {0.05 * m:.1f}), q<0.1: {(C.q < 0.1).sum()}')
    out(C.head(8).round(3).to_string(index=False))

# ---------- 4. travelled stones
cnt = pd.crosstab(S.city, S.sty); share = cnt.div(cnt.sum(1), axis=0)
big = [c for c in ['MD', 'HA', 'LO', 'KA', 'CH'] if cnt.loc[c].sum() >= 15]
out('\n== Style shares by city (main styles)'); out(share.round(2).to_string())
def other_home(r):
    if r.city not in share.index or share.loc[r.city, r.sty] > 0.10: return ''
    cand = [(share.loc[c, r.sty], c) for c in big if c != r.city and share.loc[c, r.sty] >= 0.25]
    return max(cand)[1] if cand else ''
S['style_city'] = [other_home(r) for r in S.itertuples()]
T = S[S.style_city != '']
out(f'travelled stones: {len(T)} of {len(S)} styled ({100 * len(T) / len(S):.1f}%)')
out(T[['cisi', 'city', 'sty', 'style_city', 'letter', 'signs', 'kind']].to_string(index=False))
# sign-pair models
O = objects(); O = O[O.signs.fillna('') != '']
def counts(texts):
    from collections import Counter
    c = Counter(); u = Counter()
    for t in texts:
        s = ['<'] + t.split('-') + ['>']
        for a, b in zip(s, s[1:]): c[(a, b)] += 1; u[a] += 1
    return c, u
V = len(set(s for t in O.signs for s in t.split('-'))) + 2
MOD = {c: counts(O[O.city == c].signs) for c in ['MD', 'HA', 'LO', 'KA', 'CH', 'OT']}
def lp(text, city, leave=None):
    c, u = MOD[city]; s = ['<'] + text.split('-') + ['>']; tot = 0
    for a, b in zip(s, s[1:]):
        cab = c[(a, b)]; ua = u[a]
        if leave is not None and city == leave:
            ls = ['<'] + text.split('-') + ['>']
            cab -= sum(1 for x, y in zip(ls, ls[1:]) if (x, y) == (a, b)); ua -= sum(1 for x in ls[:-1] if x == a)
        tot += math.log((max(cab, 0) + 0.1) / (max(ua, 0) + 0.1 * V))
    return tot / (len(s) - 1)
def score(r, toward): return lp(r.signs, toward, r.city) - lp(r.signs, r.city, r.city)
S['ok_text'] = S.signs.str.len() > 0
if len(T):
    real = np.mean([score(r, r.style_city) for r in T.itertuples() if r.signs])
    pool = {}
    for r in T.itertuples():
        pool.setdefault((r.city, r.style_city), [])
    for (h, s_), _ in pool.items():
        pool[(h, s_)] = [score(r, s_) for r in S[(S.city == h) & (S.style_city == '') & S.ok_text].itertuples()]
    keys = [(r.city, r.style_city) for r in T.itertuples() if r.signs]
    sims = np.array([np.mean([rng.choice(pool[k]) for k in keys]) for _ in range(NS)])
    out(f'text pull toward the style city: travelled {real:.3f} against {sims.mean():.3f} for stay-at-home stones of the same homes (P {(sims >= real).mean():.4f})')
    for r in T.itertuples():
        if r.signs: out(f'  {r.cisi} {r.city}->{r.style_city} score {score(r, r.style_city):+.3f}')
    jm = S.signs.str.endswith('740-090'); ff = S.kind == 'front formula'; cl = S.kind == 'count line'
    from scipy.stats import fisher_exact
    tr = S.style_city != ''
    for nm, x in [('[crest][jar][man] (ends 740-090)', jm), ('front formula', ff), ('count line', cl)]:
        a = int((x & tr).sum()); b = int(tr.sum()); c_ = int((x & ~tr).sum()); d = int((~tr).sum())
        out(f'{nm}: travelled {a}/{b} against stay {c_}/{d} (Fisher P {fisher_exact([[a, b - a], [c_, d - c_]])[1]:.3f})')
S.to_csv(f'{OUT}/styles_tested.csv', index=False)

# ---------- 5. twins
P = pd.read_csv(f'{OUT}/twin_pairs.csv', dtype=str)
st = dict(zip(D.obj, D.sty)); ct = dict(zip(D.obj, D.city))
P = P[P.obj_a.map(st).fillna('').ne('') & P.obj_b.map(st).fillna('').ne('')]
by_city = {c: list(D[(D.city == c) & (D.sty != '')].obj) for c in D.city.unique()}
for kind in ['twin', 'near', 'all']:
    Q = P if kind == 'all' else P[P.kind == kind]
    if not len(Q): continue
    real = np.mean([st[a] == st[b] for a, b in zip(Q.obj_a, Q.obj_b)])
    cand = [np.array([st[o] for o in by_city[ct[b]] if o != a]) for a, b in zip(Q.obj_a, Q.obj_b)]
    sa = np.array([st[a] for a in Q.obj_a])
    draws = np.array([c[rng.integers(0, len(c), NS)] for c in cand])
    sims = (draws == sa[:, None]).mean(0)
    out(f'{kind} pairs same style: {real * len(Q):.0f} of {len(Q)} ({100 * real:.0f}%) against {100 * sims.mean():.0f}% dealt within city (P {(sims >= real).mean():.4f})')
P.assign(sa=P.obj_a.map(st), sb=P.obj_b.map(st), ca=P.obj_a.map(ct), cb=P.obj_b.map(ct),
         ida=P.obj_a.map(dict(zip(D.obj, D.cisi))), idb=P.obj_b.map(dict(zip(D.obj, D.cisi)))).to_csv(f'{OUT}/twin_styles.csv', index=False)

# ---------- 6. other animals
A = pd.read_csv(f'{OUT}/codes_other.csv', dtype=str).merge(pd.read_csv(f'{OUT}/key_other.csv', dtype=str)[['num', 'obj', 'cisi']], on='num')
O2 = objects(); O2['obj'] = O2.obj.astype(str); A = A.merge(O2[['obj', 'city', 'animal']], on='obj')
A['c3'] = A.city.where(A.city.isin(['MD', 'HA']), 'other')
A.to_csv(f'{OUT}/other_coded.csv', index=False)
out('\n== Other animals: coded per city'); out(pd.crosstab(A.animal, A.c3).to_string())
for f in ['neck', 'shoulder', 'sign_cut', 'spacing']:
    sub = A[A[f] != '?']; out(pd.crosstab(sub.c3, sub[f]).to_string())
    vtest(sub[f].values, sub.c3.values, sub.animal.values, 'b', f'other animals {f} x city, city shuffled within species')
# unicorn sign_cut x city for comparison
sub = D[D.sign_cut != '?']; out(pd.crosstab(sub.city, sub.sign_cut).to_string())
open(f'{OUT}/log_4.txt', 'w').write('\n'.join(L))
