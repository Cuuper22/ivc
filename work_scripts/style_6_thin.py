#!/usr/bin/env python3
"""STYLE step 6: the sign-cutting lead (written before running).
Step 5 found thin sign cutting is the strongest city mark: 55-59% at Lothal and the small sites, 36-37% at Kalibangan and
Chanhu-daro, 17-19% at Harappa and Mohenjo-daro, inside every size third. Third way into the travelled-stone question:
use the cut as the marker.
Text score = sign-pair log-probability per transition under the SMALL-TOWN model (all seal texts of Lothal, Kalibangan,
Chanhu-daro and the other small sites) minus under the BIG-CITY model (Mohenjo-daro + Harappa), stone left out of its
own model, add-0.1 smoothing.
Predictions: (1) inside Mohenjo-daro + Harappa, thin-cut stones score more small-town-like than broad-cut stones
(P < 0.05, labels shuffled within city and size third). (2) inside the small towns, broad-cut stones score more
big-city-like than thin-cut ones. (3) thin-cut stones at the big cities carry front formulas no more than broad ones.
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_common import *
from collections import Counter
rng = np.random.default_rng(20261121); NS = 5000
D = pd.read_csv(f'{OUT}/styles.csv', dtype=str).fillna('')
D = D[(D.sign_cut != '?') & (D.signs != '')].reset_index(drop=True)
D['logsz'] = np.log(pd.to_numeric(D.area_mm2, errors='coerce'))
D['third'] = 'nosize'; ok = D.logsz.notna()
D.loc[ok, 'third'] = pd.qcut(D.loc[ok, 'logsz'].rank(method='first'), 3, labels=['s', 'm', 'b']).astype(str)
D['grp'] = np.where(D.city.isin(['MD', 'HA']), 'big', 'small')
O = objects(); O = O[O.signs.fillna('') != '']; O['grp'] = np.where(O.city.isin(['MD', 'HA']), 'big', 'small')
def counts(texts):
    c = Counter(); u = Counter()
    for t in texts:
        s = ['<'] + t.split('-') + ['>']
        for a, b in zip(s, s[1:]): c[(a, b)] += 1; u[a] += 1
    return c, u
V = len(set(s for t in O.signs for s in t.split('-'))) + 2
MOD = {g: counts(O[O.grp == g].signs) for g in ['big', 'small']}
def lp(text, g, own):
    c, u = MOD[g]; s = ['<'] + text.split('-') + ['>']; pairs = list(zip(s, s[1:])); tot = 0
    for a, b in pairs:
        cab = c[(a, b)]; ua = u[a]
        if g == own: cab -= pairs.count((a, b)); ua -= sum(1 for x, _ in pairs if x == a)
        tot += math.log((max(cab, 0) + 0.1) / (max(ua, 0) + 0.1 * V))
    return tot / len(pairs)
D['small_like'] = [lp(r.signs, 'small', r.grp) - lp(r.signs, 'big', r.grp) for r in D.itertuples()]
L = []
def out(*a): s = ' '.join(str(x) for x in a); print(s); L.append(s)
for g, want in [('big', 'thin'), ('small', 'broad')]:
    sub = D[D.grp == g].reset_index(drop=True)
    x = (sub.sign_cut == want).values; y = sub.small_like.values
    real = y[x].mean() - y[~x].mean()
    strata = (sub.city + sub.third).values; sims = []
    for _ in range(NS):
        xs = x.copy()
        for k in set(strata):
            ix = np.where(strata == k)[0]; xs[ix] = x[rng.permutation(ix)]
        sims.append(y[xs].mean() - y[~xs].mean())
    sims = np.array(sims)
    p = (sims >= real).mean() if g == 'big' else (sims <= real).mean()
    out(f'{g} cities: {want}-cut n {x.sum()} small-town-likeness {y[x].mean():+.3f} against {y[~x].mean():+.3f} for the rest (n {(~x).sum()}); gap {real:+.3f}, P {p:.4f} in the predicted direction')
    for k in ['front formula', 'count line', 'name + closer', 'bare name']:
        a = (sub.kind == k)
        out(f'   {k}: {want} {a[x].mean():.2f} against {a[~x].mean():.2f}')
big = D[D.grp == 'big']
out('\nbig-city thin-cut stones, most small-town-like texts:')
out(big[big.sign_cut == 'thin'].sort_values('small_like', ascending=False).head(12)[['cisi', 'city', 'sty', 'letter', 'small_like', 'signs', 'kind']].round(3).to_string(index=False))
D.to_csv(f'{OUT}/thin_scores.csv', index=False)
open(f'{OUT}/log_6.txt', 'w').write('\n'.join(L))
