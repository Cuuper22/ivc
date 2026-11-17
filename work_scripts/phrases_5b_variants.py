#!/usr/bin/env python3
"""PHRASES step 5b: do the members of a paradigm differ in where, on what, and when they are found? Written 2026-11-17 before the run.
Paradigms tested (slot signs): ward variants 920-060-{741,742,745}; front words {861,817,820}-002; after-jar titles 740-{400,090,679,565};
  measure variants {705,706}-033; counted tree 590-{390,405}-740 (tree signs); A-comb counts *-806 {467,468,472}; star numbers {032,003,016}-220.
For each paradigm, objects carrying exactly one member (objects carrying two are dropped). Statistic = chi-square of member x category (category =
city with the large five kept and the rest pooled as 'other'; object kind; time bin; animal grouped unicorn / none / other), P from 5,000
shuffles of the member labels among the carriers (so the control keeps the mix of cities, kinds and bins). Prediction: the front words and
the ward variants differ by city (variant spellings tied to place), the after-jar titles differ by kind (comb on tablets at Harappa vs man on
seals), the number slots (stars, A-comb) do not differ by city.
Output: work_data/phrases/variants.csv, log_5b.txt
"""
from phrases_common import *
LOG = open(f'{OUTP}/log_5b.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n'); LOG.flush()
rng = np.random.default_rng(55)
O = build_objects(); O = O[O.site != 'Unknown'].copy()
BIG = {'Harappa', 'Mohenjo-daro', 'Dholavira', 'Kalibangan', 'Lothal'}
O['city'] = O.site.where(O.site.isin(BIG), 'other'); O['animal3'] = np.where(O.animal == 'Bull1', 'unicorn', np.where(O.animal.isin(['none', 'blank']), 'none', 'other'))
O['bin2'] = O.bin.replace('', 'undated')
def carriers_of(p):
    out = set()
    for o, x in zip(d.obj, d.tok):
        if x and find_in(x, p): out.add(str(o))
    return out
PAR = {'ward variants 920-060-*': [('920', '060', s) for s in ('741', '742', '745')],
       'front words *-002': [(s, '002') for s in ('861', '817', '820')],
       'after-jar titles 740-*': [('740', s) for s in ('400', '090', '679', '565')],
       'measure variants *-033': [(s, '033') for s in ('705', '706')],
       'tree signs 590-*-740': [('590', s, '740') for s in ('390', '405', '407')],
       'A-comb counts *-806': [(s, '806') for s in ('467', '468', '472')],
       'star numbers *-220': [(s, '220') for s in ('032', '003', '016')]}
def chi(lbl, cat):
    tab = pd.crosstab(lbl, cat).values.astype(float); e = tab.sum(1, keepdims=True) * tab.sum(0, keepdims=True) / tab.sum()
    return float(((tab - e) ** 2 / np.where(e > 0, e, 1)).sum())
rows = []
for name, mem in PAR.items():
    C = {'-'.join(p): carriers_of(p) for p in mem}
    cnt = collections.Counter(o for s in C.values() for o in s)
    lab = {}
    for m, s in C.items():
        for o in s:
            if cnt[o] == 1 and o in O.index: lab[o] = m[len([x for x in m.split('-')]) - len(m.split('-')) :] if False else m
    idx = list(lab); L = np.array([lab[o] for o in idx]); X = O.loc[idx]
    say(f'\n{name}: carriers per member', {m: int((L == m).sum()) for m in C})
    for cat in ('city', 'kind', 'bin2', 'animal3'):
        obs = chi(L, X[cat].values); null = np.zeros(5000)
        for t in range(5000): null[t] = chi(rng.permutation(L), X[cat].values)
        P = (np.sum(null >= obs) + 1) / 5001
        tab = pd.crosstab(L, X[cat].values)
        say(f'  by {cat}: chi2 {obs:.1f}, shuffle mean {null.mean():.1f}, P {P:.4f}'); say('    ' + tab.to_string().replace('\n', '\n    '))
        rows.append(dict(paradigm=name, test=cat, chi2=round(obs, 2), null_mean=round(null.mean(), 2), P=P, carriers=len(L)))
pd.DataFrame(rows).to_csv(f'{OUTP}/variants.csv', index=False)
