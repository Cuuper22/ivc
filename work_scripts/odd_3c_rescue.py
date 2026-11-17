#!/usr/bin/env python3
"""Step 2b: second readings for the signs whose name-sense went against (368, 861, 824) and the 060 / keeper rules.
PREDICTIONS (written before the run)
 368 banner: if 368 is a TITLE that closes a name (standard-bearer, like the spear), it is text-final far above the base rate and the
     jar is rarer in those texts than in seals in general (a title takes the jar's place).
 861 holding: if 861 away from the front is a land-holding word, faces with it carry land words (503 hill, 615 field, 845 sheaf-bundle,
     692 district, 482 hill-share) more than other faces, and sit on copper tablets (the land records).
 824 worth: 824 at the front before a stroke (seals) works like the share openers 861/817/820: the sign after the stroke is a name sign that
     also follows those openers.
 060 inner: 060 away from the openers is a name prefix: the next sign is a fish or a number far above the base rate.
 keepers: a keeper with a count before it ends the text (title) on seals; on goods it is a head-count of porters.
"""
from odd_common import *
F = faces()
LAND = {'503','615','845','692','482'}
def share(k, n, base, alt='greater'): return f'{k}/{n} = {k/n:.0%} against {base:.1%}, P {pbin(k, n, base, alt):.2g}' if n else 'none'
for cat in ('L', 'Mu', 'ALL'):
    FL = [f for f in F if cat == 'ALL' or f['cat'] == cat]
    # 368
    seals = [f for f in FL if f['kind'] == 'seal' and len(f['x']) >= 2]
    last_all = np.mean([1.0 / len(f['x']) for f in seals])      # expected chance that a given sign is last
    n368 = sum(f['x'].count('368') for f in seals); k368 = sum(f['x'][-1] == '368' for f in seals)
    jar_base = np.mean(['740' in f['x'] for f in seals])
    f368 = [f for f in seals if f['x'][-1] == '368']
    kj = sum('740' in f['x'] for f in f368)
    # 861 away from front
    na = [(f, i) for f in FL for i, a in enumerate(f['x']) if a == '861' and i > 0]
    land_base = np.mean([bool(LAND & set(f['x'])) for f in FL]); kl = sum(bool(LAND & set(f['x'])) for f, i in na)
    ct_base = np.mean([f['kind'] == 'ctab' for f in FL]); kc = sum(f['kind'] == 'ctab' for f, i in na)
    # 824 front + stroke vs 861/817/820 openers
    def after_open(op):
        c = collections.Counter()
        for f in FL:
            x = f['x']
            if len(x) >= 3 and x[0] == op and x[1] in CNT: c[x[2]] += 1
        return c
    c824 = after_open('824'); cop = sum((after_open(o) for o in ('861','817','820')), collections.Counter())
    n824 = sum(c824.values()); k824 = sum(v for s, v in c824.items() if cop.get(s, 0) >= 2)
    # control: random seal's third sign in cop set
    ctl = np.mean([f['x'][2] in {s for s, v in cop.items() if v >= 2} for f in seals if len(f['x']) >= 3])
    # 060
    nx = [(f['x'][i+1] if i+1 < len(f['x']) else '$') for f in FL for i, a in enumerate(f['x']) if a == '060' and f['roles'][i] in ('crest','self','tag')]
    base_nx = np.mean([(f['x'][i+1] in FISH or f['x'][i+1] in CNT) for f in FL for i in range(len(f['x'])-1)])
    kf = sum(a in FISH or a in CNT for a in nx)
    # keepers
    KEEP = {'151','152','153','154','155','156','157','158'}
    ck = [(f, i) for f in FL for i, a in enumerate(f['x']) if a in KEEP and i > 0 and f['x'][i-1] in CNT]
    kfin = sum(i == len(f['x']) - 1 for f, i in ck)
    kseal = sum(f['kind'] == 'seal' for f, i in ck)
    print(f'--- {cat} ---')
    print(f' 368 text-final on seals: {share(k368, n368, last_all)} (base = chance a given sign is last)')
    print(f' 368-final seals carrying the jar: {share(kj, len(f368), jar_base, 'less')}  (expected FEWER if a title replaces the jar)')
    print(f' 861 away from the front, land word on the face: {share(kl, len(na), land_base)}; on copper tablets: {share(kc, len(na), ct_base)}')
    print(f' 824 front + stroke, then a sign that follows the share openers: {k824}/{n824} against {ctl:.0%} of seals; (824 at front: {n824})')
    print(f' 060 away from openers, next is fish or number: {share(kf, len(nx), base_nx)}')
    print(f' count + keeper: {len(ck)} uses; text-final {kfin}; on seals {kseal}')
