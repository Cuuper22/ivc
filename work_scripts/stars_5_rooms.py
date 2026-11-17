#!/usr/bin/env python3
"""Step 4 redesigned (the exact-compound room test had only 1 pair to work with).

Seen after the K1 run: room-mates pair tall-two + plain fish with tall-two + caged fish twice (M-367/M-723, M-57/M-130),
and three + barred fish with three + plain fish once (M-266/M-294).
PREDICTIONS (written before this run):
 K1b The NUMBER WORD before a fish (its value), whatever the fish, is shared by room-mates (depth within 3 ft)
     more than chance: the number is the family's star-word, the fish drawing can vary.
 K1c Plain fish 220 and caged fish 226 are one star word: treating them as one, room-mates share the
     form + fish more than chance.
Chance: room labels shuffled among Mohenjo-daro seals of the same area and 3-ft depth band, 5,000 times.
"""
from stars_common import *
rng4 = np.random.default_rng(23)
room = d.groupby('obj')['room-grid'].first()
H = moh[moh.seal].copy(); H['room'] = H.index.map(room)
H = H[H.room.notna() & ~H.room.isin(['--', '-', '']) & H.dep.notna()].copy(); H['rk'] = H.house + '|' + H.room
def feats(o, how):
    s = set()
    for x, P in zip(o.faces, o.parses):
        for u in units(x, P):
            if u['nxt'] not in FISHALL: continue
            if how == 'value': s.add(u['value'])
            elif how == 'plaincaged': s.add(f"{u['style']}{u['value']}+{'P' if u['nxt'] in ('220', '226') else u['nxt']}")
            else: s.add(f"{u['style']}{u['value']}+{u['nxt']}")
    return s
for how in ('exact', 'value', 'plaincaged'):
    v = [feats(o, how) for o in H.itertuples()]; keys = H.rk.values; dep = H.dep.values; band = H.band.values
    has = [i for i in range(len(H)) if v[i]]
    def count(k):
        g = collections.defaultdict(list)
        for i in has: g[k[i]].append(i)
        c = 0; pr = []
        for m in g.values():
            for a in range(len(m)):
                for b in range(a + 1, len(m)):
                    i, j = m[a], m[b]
                    if abs(dep[i] - dep[j]) <= 3 and v[i] & v[j]: c += 1; pr.append((H.cisi.iloc[i], H.cisi.iloc[j], sorted(v[i] & v[j])))
        return c, pr
    obs, pr = count(keys); bb = collections.defaultdict(list)
    for i in range(len(H)): bb[band[i]].append(i)
    sims = []
    for _ in range(5000):
        k = keys.copy()
        for ii in bb.values():
            if len(ii) > 1: k[ii] = keys[rng4.permutation(ii)]
        sims.append(count(k)[0])
    print(f'{how}: same-room pairs {obs} against {np.mean(sims):.2f}, P {(1+np.sum(np.array(sims)>=obs))/5001:.4f} ({len(has)} seals carry a number + fish)  pairs: {pr}')
