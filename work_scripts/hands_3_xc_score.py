#!/usr/bin/env python3
"""HANDS step 2 score: join the blind judgements (work_data/hands/xc_judged_raw.txt: id|features|call, S same, N near, D different,
U cannot tell) with the key AFTER all 120 were judged; write work_data/hands/cross_city_judged.csv and the table."""
import sys; sys.path.insert(0, "/home/antigravity/Cuuper22/ivc/work_scripts")
from hands_common import *
from math import comb
K = pd.read_csv(f'{OUT}/hands_pairs_key.csv', dtype=str).fillna('')
J = pd.DataFrame([l.rstrip('\n').split('|') for l in open(f'{OUT}/xc_judged_raw.txt')], columns=['pid', 'features', 'call'])
M = K.merge(J, on='pid'); assert len(M) == 120
M['call'] = M.call.map({'S': 'same', 'N': 'near', 'D': 'different', 'U': 'cannot tell'})
M.to_csv(f'{OUT}/cross_city_judged.csv', index=False)
print(pd.crosstab(M.kind, M.call))
for k, g in M.groupby('kind'):
    dec = g[g.call != 'cannot tell']; al = dec.call.isin(['same', 'near']).sum()
    print(k, 'alike', al, 'of decided', len(dec), f'{al/len(dec):.2f}', ' of all 60:', f'{al/60:.2f}')
t = M[M.kind == 'text']; c = M[M.kind == 'control']
a1 = t.call.isin(['same', 'near']).sum(); n1 = (t.call != 'cannot tell').sum(); a2 = c.call.isin(['same', 'near']).sum(); n2 = (c.call != 'cannot tell').sum()
# permutation P: shuffle kind labels among decided pairs
d = M[M.call != 'cannot tell'].copy(); al = d.call.isin(['same', 'near']).values; kind = (d.kind == 'text').values
rng = np.random.default_rng(7); real = al[kind].mean() - al[~kind].mean(); cnt = 0
for _ in range(20000):
    p = rng.permutation(kind); cnt += (al[p].mean() - al[~p].mean()) >= real
print('diff', real, 'P(>=)', cnt / 20000)
# shared sign count in controls
print('controls: mean shared single signs', pd.to_numeric(c.shared_sign_count).mean(), ' text pairs', pd.to_numeric(t.shared_sign_count).mean())
print(t[t.call.isin(['same', 'near'])][['pid', 'a', 'b', 'site_a', 'site_b', 'shared_run', 'call']].to_string())
print(c[c.call.isin(['same', 'near'])][['pid', 'a', 'b', 'site_a', 'site_b', 'signs_a', 'signs_b', 'call']].to_string())
# is the text-pair alike driven by same-text photos? (decided text pairs by identical text)
t2 = t[t.call != 'cannot tell'].copy(); t2['full_same'] = t2.signs_a == t2.signs_b
print(pd.crosstab(t2.full_same, t2.call.isin(['same', 'near'])))
# controls same animal-photo pairs: both unicorn
for k, g in M[M.call != 'cannot tell'].groupby('kind'):
    g = g.assign(both_uni=(g.animal_a == 'unicorn') & (g.animal_b == 'unicorn'))
    print(k, g.groupby('both_uni').apply(lambda x: f"{x.call.isin(['same','near']).sum()}/{len(x)}").to_dict())
