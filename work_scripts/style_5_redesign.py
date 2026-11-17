#!/usr/bin/env python3
"""STYLE step 5: redesign after the travelled-stone rule found only 1 stone, plus new ideas. Written before running.

(a) Which single features carry the city signal (unicorns): V feature x city, city shuffled within size third.
    Prediction: sign_cut carries it (thin cutting more common away from Mohenjo-daro and Harappa), neck too.
(b) Thin cutting against size: thin share by size third inside each city group. Prediction: thin is not just small seals.
(c) REDESIGN of travelled stones as a continuous test: drawing-home score = naive-Bayes log ratio P(features | Harappa) /
    P(features | Mohenjo-daro) over neck, shoulder, stand_top, stand_bowl, sign_cut, spacing (each stone left out,
    add-1 smoothing, unread features skipped). Text-home score = sign-pair log ratio Harappa / Mohenjo-daro (stone left
    out, as in step 4). Spearman of the two inside Mohenjo-daro stones and inside Harappa stones; P = share of 5,000
    shuffles of the text score (within city) with rho >= real. Prediction: rho > 0 in both cities (P < 0.05 pooled).
(d) NEW IDEA 1: the Mohenjo-daro stones the stand job flagged as Harappa-like in text (city_outliers.csv) that were
    coded here: is their style mix Harappa's? Prediction: more S1 + S4 than other Mohenjo-daro stones.
(e) NEW IDEA 2: inside one catalogue letter (W), does the style mix differ by city? Prediction: yes (the letter hides
    city manners): W at Harappa is S1/S4, W at Mohenjo-daro is S2.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_common import *
from scipy.stats import spearmanr, fisher_exact
rng = np.random.default_rng(20261120); NS = 5000
S = pd.read_csv(f'{OUT}/styles_tested.csv', dtype=str).fillna('')
D = pd.read_csv(f'{OUT}/styles.csv', dtype=str).fillna('')
D['logsz'] = np.log(pd.to_numeric(D.area_mm2, errors='coerce'))
L = []
def out(*a): s = ' '.join(str(x) for x in a); print(s); L.append(s)
def cv(a, b):
    t = pd.crosstab(a, b).values.astype(float)
    if min(t.shape) < 2: return 0.0
    e = t.sum(1, keepdims=True) * t.sum(0, keepdims=True) / t.sum()
    return math.sqrt(((t - e) ** 2 / e).sum() / t.sum() / (min(t.shape) - 1))
def shuf(v, g):
    v = np.array(v, dtype=object).copy(); g = np.array(g)
    for k in set(g):
        ix = np.where(g == k)[0]; v[ix] = v[rng.permutation(ix)]
    return v
D['third'] = 'nosize'
ok = D.logsz.notna()
D.loc[ok, 'third'] = pd.qcut(D.loc[ok, 'logsz'].rank(method='first'), 3, labels=['small', 'middle', 'big']).astype(str)
FE = ['neck', 'shoulder', 'stand_top', 'stand_bowl', 'sign_cut', 'spacing']
out('== (a) single features x city (unicorns, all coded stones, city shuffled within size third)')
for f in FE:
    sub = D[D[f] != '?']; real = cv(sub[f], sub.city)
    sims = np.array([cv(sub[f], shuf(sub.city.values, sub.third.values)) for _ in range(2000)])
    out(f'{f}: n {len(sub)} V {real:.3f} against {sims.mean():.3f} (P {(sims >= real).mean():.4f})')
    out('   ' + pd.crosstab(sub.city, sub[f], normalize='index').round(2).to_string().replace('\n', '\n   '))
out('\n== (b) thin cutting by size third and city')
sub = D[(D.sign_cut != '?') & (D.third != 'nosize')].copy()
sub['cg'] = sub.city.where(sub.city.isin(['MD', 'HA']), 'small towns')
out(pd.crosstab([sub.cg], sub.third, values=(sub.sign_cut == 'thin').astype(int), aggfunc='mean').round(2).to_string())
out(pd.crosstab([sub.cg], sub.third).to_string())

out('\n== (c) drawing-home score against text-home score (Harappa vs Mohenjo-daro)')
O = objects(); O = O[O.signs.fillna('') != '']
from collections import Counter
def counts(texts):
    c = Counter(); u = Counter()
    for t in texts:
        s = ['<'] + t.split('-') + ['>']
        for a, b in zip(s, s[1:]): c[(a, b)] += 1; u[a] += 1
    return c, u
V = len(set(s for t in O.signs for s in t.split('-'))) + 2
MOD = {c: counts(O[O.city == c].signs) for c in ['MD', 'HA']}
def lp(text, city, own):
    c, u = MOD[city]; s = ['<'] + text.split('-') + ['>']; pairs = list(zip(s, s[1:])); tot = 0
    for a, b in pairs:
        cab = c[(a, b)]; ua = u[a]
        if city == own: cab -= pairs.count((a, b)); ua -= sum(1 for x, _ in pairs if x == a)
        tot += math.log((max(cab, 0) + 0.1) / (max(ua, 0) + 0.1 * V))
    return tot / len(pairs)
H = D[D.city.isin(['MD', 'HA']) & (D.signs != '')].reset_index(drop=True)
H['text_home'] = [lp(r.signs, 'HA', r.city) - lp(r.signs, 'MD', r.city) for r in H.itertuples()]
def draw_score(i):
    tot = 0; n = 0
    for f in FE:
        v = H.loc[i, f]
        if v == '?': continue
        vals = FEATURES[f]; lr = 0
        for c, sign in [('HA', 1), ('MD', -1)]:
            m = (H.city == c) & (H[f] != '?') & (H.index != i)
            k = ((H[f] == v) & m).sum(); lr += sign * math.log((k + 1) / (m.sum() + len(vals)))
        tot += lr; n += 1
    return tot if n >= 3 else np.nan
H['draw_home'] = [draw_score(i) for i in H.index]
G = H[H.draw_home.notna()]
for c in ['MD', 'HA']:
    g = G[G.city == c]; rho = spearmanr(g.draw_home, g.text_home).correlation
    sims = np.array([spearmanr(g.draw_home, rng.permutation(g.text_home.values)).correlation for _ in range(NS)])
    out(f'inside {c}: n {len(g)} rho {rho:+.3f} (P {(sims >= rho).mean():.4f})')
# pooled: within-city ranks
G = G.copy(); G['dr'] = G.groupby('city').draw_home.rank(pct=True); G['tr'] = G.groupby('city').text_home.rank(pct=True)
rho = spearmanr(G.dr, G.tr).correlation
sims = np.array([spearmanr(G.dr, shuf(G.tr.values, G.city.values).astype(float)).correlation for _ in range(NS)])
out(f'pooled within-city ranks: rho {rho:+.3f} (P {(sims >= rho).mean():.4f})')
md = G[G.city == 'MD'].sort_values('draw_home', ascending=False)
top = md.head(max(1, len(md) // 10))
out(f'MD stones with the most Harappa-like drawing (top tenth, n {len(top)}): mean text-home {top.text_home.mean():+.3f} against {md.text_home.mean():+.3f} for all MD')
out(top[['cisi', 'sty', 'letter', 'draw_home', 'text_home', 'signs']].round(3).to_string(index=False))
ha = G[G.city == 'HA'].sort_values('draw_home')
topH = ha.head(max(1, len(ha) // 10))
out(f'HA stones with the most Mohenjo-daro-like drawing (top tenth, n {len(topH)}): mean text-home {topH.text_home.mean():+.3f} against {ha.text_home.mean():+.3f} for all HA')
out(topH[['cisi', 'sty', 'letter', 'draw_home', 'text_home', 'signs']].round(3).to_string(index=False))
H.to_csv(f'{OUT}/home_scores.csv', index=False)

out('\n== (d) stand-job Harappa-like-text Mohenjo-daro stones that were coded')
CO = pd.read_csv(f'{ROOT}/work_data/stand/city_outliers.csv', dtype=str)
flag = set(CO[CO.group.str.contains('Harappa-like')].cisi)
mdS = D[(D.city == 'MD') & D.sty.isin(['S1', 'S2', 'S3', 'S4', 'S5'])]
f_ = mdS[mdS.cisi.isin(flag)]
out(f'coded flagged stones: {len(f_)}: ' + ', '.join(f'{r.cisi} {r.sty}' for r in f_.itertuples()))
out('style mix flagged: ' + str(f_.sty.value_counts().to_dict()) + ' | other MD: ' + str(mdS[~mdS.cisi.isin(flag)].sty.value_counts().to_dict()))
haS = D[(D.city == 'HA') & D.sty.isin(['S1', 'S2', 'S3', 'S4', 'S5'])]
out('HA mix: ' + str(haS.sty.value_counts().to_dict()))

out('\n== (e) style mix inside letter W (and J), by city')
for let in ['W', 'J', 'S', 'I']:
    w = D[(D.letter == let) & D.sty.isin(['S1', 'S2', 'S3', 'S4', 'S5']) & D.city.isin(['MD', 'HA'])]
    t = pd.crosstab(w.city, w.sty); out(f'letter {let}:'); out(t.to_string())
    real = cv(w.city, w.sty); sims = np.array([cv(rng.permutation(w.city.values), w.sty) for _ in range(2000)])
    out(f'  V {real:.3f} against {sims.mean():.3f} (P {(sims >= real).mean():.4f})')
open(f'{OUT}/log_5.txt', 'w').write('\n'.join(L))
