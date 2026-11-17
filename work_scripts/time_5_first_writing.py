#!/usr/bin/env python3
"""History job, new idea: what did the first writing say? PREDICTION written before running: objects from before
the cities (HARP Period 1-2 at Harappa, Dholavira stages I-II; ca. 3700-2600 BC) carry counts and goods signs but
not the jar 740 ("house of"): the house-name formula comes with the cities.
Also: writing after the cities (HARP Period 4-5 at Harappa, Dholavira stage VI) still carries cup counts and the jar."""
from time_common import *
from scipy.stats import fisher_exact
D['jar'] = D.faces.apply(lambda fs: any('740' in f for f in fs))
D['cnt'] = D.faces.apply(lambda fs: any(a in NUM for f in fs for a in f))
D['cup'] = D.faces.apply(lambda fs: any('700' in f for f in fs))
groups = [('before the cities (rank 0)', D['rank'] == 0), ('3A-3B', D['rank'].between(1, 3)), ('3B/C-3C-2', D['rank'].between(4, 6)),
          ('3C-3, 3C-4', D['rank'].between(7, 8)), ('after the cities (Period 4-5, Dholavira VI)', D['rank'] >= 9)]
for lab, m in groups:
    x = D[m]; print(f'{lab}: {len(x)} objects; jar {int(x.jar.sum())}; a count {int(x.cnt.sum())}; cup {int(x.cup.sum())}; sites {x.site.value_counts().to_dict()}; kinds {x.kind.value_counts().to_dict()}')
a = D[D['rank'] == 0]; b = D[D['rank'] >= 1]
for k in [None, 'seal', 'pot']:
    x = a if k is None else a[a.kind == k]; y = b if k is None else b[b.kind == k]
    print(f'jar, before cities vs later ({k or "all kinds"}): {int(x.jar.sum())}/{len(x)} against {int(y.jar.sum())}/{len(y)}; Fisher P {fisher_exact([[x.jar.sum(), len(x) - x.jar.sum()], [y.jar.sum(), len(y) - y.jar.sum()]])[1]:.2g}')
print(a[['cisi', 'site', 'kind', 'time']].assign(text=a.faces.apply(lambda f: ' | '.join('-'.join(t) for t in f))).to_string())
z = D[D['rank'] >= 9]
print(z[z.kind != 'seal'][['cisi', 'site', 'kind', 'time']].assign(text=z[z.kind != 'seal'].faces.apply(lambda f: ' | '.join('-'.join(t) for t in f))).to_string())
