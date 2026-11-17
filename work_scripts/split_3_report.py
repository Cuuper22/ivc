#!/usr/bin/env python3
"""Split step 3: ranks of each real split among its 20+20 decoys, from work_data/split/test_<sign>.csv. Prints tables."""
from split_common import *
rows = []
import sys
TAG = sys.argv[1] if len(sys.argv) > 1 else ''
for s in ['850', '824', '001']:
    if not os.path.exists(f'{SPL}/test_{s}{TAG}.csv'): continue
    D = pd.read_csv(f'{SPL}/test_{s}{TAG}.csv')
    for (sp, ho), G in D.groupby(['split', 'heldout'], sort=False):
        g = G.set_index('name')
        for sch, base in (('S1', 'U1'), ('S2', 'U0')):
            for col in ('bits_all', 'bits_with_sign'):
                real = g.loc[f'real_{sch}', col]; b = g.loc[base, col]
                r = dict(sign=s, split=sp, heldout=ho, scheme=sch, measure=col, unsplit=b, real=real, gain=b - real)
                for nm in 'AB':
                    dv = np.array([g.loc[f'dec{nm}{j}_{sch}', col] for j in range(20)])
                    r[f'dec{nm}_mean'] = dv.mean(); r[f'dec{nm}_best'] = dv.min(); r[f'rank{nm}'] = 1 + int((dv < real - 1e-9).sum()); r[f'ties{nm}'] = int((abs(dv - real) <= 1e-9).sum())
                    r[f'dec{nm}_mean_gain'] = b - dv.mean()
                if ho == 'first catalogue 10 fold fits':
                    r['folds_beat'] = int(g.loc[f'real_{sch}', f'folds_real_beats_base_{sch}']); r['occ'] = int(g.loc['U0', 'occ_with_sign'])
                else: r['occ'] = int(g.loc['U0', 'occ_with_sign'])
                rows.append(r)
R = pd.DataFrame(rows); R.to_csv(f'{SPL}/ranks{TAG}.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30)
print(R[R.measure == 'bits_all'].round(4).to_string())
print(R[R.measure == 'bits_with_sign'].round(4).to_string())
