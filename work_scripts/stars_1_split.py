#!/usr/bin/env python3
"""Step 1 and 2: number + fish, split by slot (name on a seal against count on goods), first catalogue then new texts.

PREDICTIONS (written before the run):
 P1  If number + fish inside names is a star name, the numbers before a fish in the NAME slot pile up on 3, 6 and 7:
     share of {3,6,7} among name-slot units is higher than among count-slot units.
 P2  Name-slot units avoid 1, 4, 5 and 8 (not star words) more than count-slot units do.
 P3  Count-slot numbers before a fish follow the ordinary count distribution: their value mix is closer to the mix of
     numbers before all other counted things on goods objects than the name-slot mix is.
 P4  (stroke style) name-slot numbers are written in a different form: more stacked (two rows), fewer tall strokes,
     than count-slot numbers before a fish.
Run: python3 stars_1_split.py   -> work_data/stars/units_L.csv, units_Mu.csv, printout
"""
from stars_common import *
from scipy.stats import fisher_exact, chi2_contingency

STAR = {3, 6, 7}; NONSTAR = {1, 4, 5, 8}
def test(cat, lvl, U, D):
    if True:
        F = D[D.nxt.isin(FISHALL)].copy()
        F['slot2'] = F.slot.map({'name': 'NAME', 'sealx': 'seal-other', 'count_pure': 'COUNT', 'count_named': 'COUNT'})
        print(f'\n===== catalogue {cat} ({lvl}): number units {len(U)} (deduped {len(D)}), before a fish {len(F)} =====')
        for s, g in F.groupby('slot'):
            print(f'  {s:12s} n {len(g):4d}  values {dict(sorted(collections.Counter(g.value).items()))}  styles {dict(collections.Counter(g["style"]))}')
        N = F[F.slot2 == 'NAME']; C = F[F.slot2 == 'COUNT']
        # P1
        a, b = int(N.value.isin(STAR).sum()), len(N); c_, e = int(C.value.isin(STAR).sum()), len(C)
        if b and e:
            o, p = fisher_exact([[a, b - a], [c_, e - c_]], alternative='greater')
            print(f'P1 {{3,6,7}} share: NAME {a}/{b} = {a/b:.0%}  COUNT {c_}/{e} = {c_/e:.0%}  odds {o:.2f}  P {p:.3g}')
            a2 = int(N.value.isin(NONSTAR).sum()); c2 = int(C.value.isin(NONSTAR).sum())
            o, p = fisher_exact([[a2, b - a2], [c2, e - c2]], alternative='less')
            print(f'P2 {{1,4,5,8}} share: NAME {a2}/{b} = {a2/b:.0%}  COUNT {c2}/{e} = {c2/e:.0%}  P(name fewer) {p:.3g}')
        # P3: numbers before every other thing on goods objects (count slots), deduped
        O = D[(~D.nxt.isin(FISHALL)) & D.slot.isin(['count_pure', 'count_named'])]
        vals = sorted(set(range(1, 9)))
        def mix(g): c = collections.Counter(g.value.clip(upper=8)); t = sum(c.values()); return np.array([c[v] / max(t, 1) for v in vals])
        def tvd(p, q): return 0.5 * np.abs(p - q).sum()
        print(f'P3 distance (half the summed difference) from the ordinary goods-count mix (n {len(O)}): NAME {tvd(mix(N), mix(O)):.2f}  COUNT {tvd(mix(C), mix(O)):.2f}')
        print('   ordinary goods mix', dict(zip(vals, np.round(mix(O), 2))))
        # P4 stroke style
        tab = pd.crosstab(F.slot2, F['style']); print('P4 style by slot\n', tab)
        for st in ('stacked', 'tall'):
            a = int((N['style'] == st).sum()); c_ = int((C['style'] == st).sum())
            if len(N) and len(C):
                o, p = fisher_exact([[a, len(N) - a], [c_, len(C) - c_]], alternative='greater' if st == 'stacked' else 'less')
                print(f'   {st}: NAME {a}/{len(N)}  COUNT {c_}/{len(C)}  P {p:.3g}')
        # detail: value x fish x slot
        print('  value + fish by slot:')
        for (s, v, f), g in F.groupby(['slot2', 'value', 'nxt']):
            if len(g) >= 2 or s == 'NAME': print(f'    {s:10s} {v} + {f}: {len(g)}  styles {dict(collections.Counter(g["style"]))}  e.g. {list(g.cisi[:3])}')


for cat in ('L', 'Mu'):
    U = all_units(cat); U.to_csv(f'{OUTS}/units_{cat}.csv', index=False)
    for lvl, D in (('objects', dedup(U)), ('distinct texts', distinct(U))):
        test(cat, lvl, U, D)

