#!/usr/bin/env python3
"""HANDS step 3 score: join blind judgements (md_judged_raw.txt: id|features|call) with the key AFTER all 180 were judged."""
import sys; sys.path.insert(0, "/home/antigravity/Cuuper22/ivc/work_scripts")
from hands_common import *
K = pd.read_csv(f'{OUT}/hands_md_key.csv', dtype=str).fillna('')
J = pd.DataFrame([l.rstrip('\n').split('|') for l in open(f'{OUT}/md_judged_raw.txt')], columns=['pid', 'features', 'call'])
M = K.merge(J, on='pid'); assert len(M) == 180
M['call'] = M.call.map({'S': 'same', 'N': 'near', 'D': 'different', 'U': 'cannot tell'})
M.to_csv(f'{OUT}/md_judged.csv', index=False)
print(pd.crosstab(M.kind, M.call))
rng = np.random.default_rng(11)
for k, g in M.groupby('kind'):
    d = g[g.call != 'cannot tell']; al = d.call.isin(['same', 'near']).sum()
    print(k, f'alike {al} of decided {len(d)} = {al/len(d):.2f}; of all 60 = {al/60:.2f}; same-text pairs {int((g.same_text=="True").sum())}')
d = M[M.call != 'cannot tell'].copy(); d['al'] = d.call.isin(['same', 'near'])
from scipy.stats import fisher_exact
def cmp(k1, k2):
    a = d[d.kind == k1].al; b = d[d.kind == k2].al
    print(k1, 'vs', k2, fisher_exact([[a.sum(), len(a)-a.sum()], [b.sum(), len(b)-b.sum()]], alternative='greater')[1])
cmp('same_building', 'diff_building_same_area'); cmp('same_building', 'diff_area'); cmp('diff_building_same_area', 'diff_area')
x = d.assign(sb=d.kind == 'same_building')
print('alike excluding identical-text pairs:'); print(d[d.same_text != 'True'].groupby('kind').al.agg(['sum', 'count']))
print(d[d.al][['pid', 'a', 'b', 'kind', 'bld_a', 'bld_b', 'call']].to_string())
# building-level: same-building alike pairs by building
print(d[(d.kind == 'same_building')].groupby('bld_a').al.agg(['sum', 'count']).query('count>0').to_string())
# decided pairs: both-unicorn
u = d[(d.animal_a == 'unicorn') & (d.animal_b == 'unicorn')]
print('both unicorn', u.groupby('kind').al.agg(['sum', 'count']))
