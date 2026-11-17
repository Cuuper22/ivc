#!/usr/bin/env python3
"""Step 4: the star calendar. Do house- and room-mates share a star name? Do star names go with animals or endings?
Every distinct fish compound with its objects and cities (both catalogues).

PREDICTIONS (written before the run):
 K1  Seals from the same Mohenjo-daro room (depth within 3 ft) share a number + fish compound more than chance
     (labels shuffled among seals of the same area and 3-ft band).
 K2  Same, at house level, for any fish compound and for any fish sign at all (number or not).
 K3  Each star compound goes with its own seal animal: animal x compound is less even than chance (Cramer V, shuffled).
 K4  Star compounds go with endings: the ending (jar, jar+man, spear, porter, comb) mix differs by compound.
 K5  A calendar or clan set: the distinct number + fish compounds that recur (3+ objects) number between 4 and 12,
     and the 27/28 lunar asterisms are not all there (a clan set, not a full calendar).
Run: python3 stars_4_calendar.py -> work_data/stars/fish_compounds.csv
"""
from stars_common import *

rng3 = np.random.default_rng(17)
A = pd.concat([all_units('L'), all_units('Mu')], ignore_index=True)
A['form'] = A['style'] + A.value.astype(str)
F = A[A.nxt.isin(FISHALL)].copy(); F['compound'] = F.form + '+' + F.nxt
# plain fish signs without a number, as one-sign star words, for the table
rows = []
for comp, g in F.groupby('compound'):
    L = g[g.cat == 'L']; Mu = g[g.cat == 'Mu']
    rows.append(dict(compound=comp, objects_L=L.obj.nunique(), objects_new=Mu.obj.nunique(), distinct_texts=g.text.nunique(),
                     slots=dict(collections.Counter(g.drop_duplicates(['obj']).slot)), kinds=dict(collections.Counter(g.drop_duplicates(['obj']).kind)),
                     cities=dict(collections.Counter(g.drop_duplicates(['obj']).site).most_common()),
                     animals=dict(collections.Counter(L.drop_duplicates(['obj']).animal).most_common(4)),
                     endings=dict(collections.Counter(g.drop_duplicates(['obj']).ending).most_common()),
                     examples=' '.join(g.drop_duplicates(['obj']).cisi.head(6))))
T = pd.DataFrame(rows).sort_values(['objects_L', 'objects_new'], ascending=False)
T.to_csv(f'{OUTS}/fish_compounds.csv', index=False)
print('distinct number + fish compounds:', len(T), '| on 3+ objects:', int(((T.objects_L + T.objects_new) >= 3).sum()))
for _, r in T.iterrows():
    print(f"  {r.compound:12s} L {r.objects_L:3d} new {r.objects_new:3d} | {r.cities} | slots {r.slots} | animals {r.animals} | endings {r.endings}")

# K1/K2: house and room sharing at Mohenjo-daro (seals with a house; room from d)
room = d.groupby('obj')['room-grid'].first()
H = moh[moh.seal].copy(); H['room'] = H.index.map(room); H['rk'] = H.house + '|' + H.room.astype(str)
def comps(o):
    s = set()
    for x, P in zip(o.faces, o.parses):
        for u in units(x, P):
            if u['nxt'] in FISHALL: s.add(f"{u['style']}{u['value']}+{u['nxt']}")
    return s
H['comps'] = [comps(o) for o in H.itertuples()]
H['fish'] = H.signs.apply(lambda z: set(z) & FISHALL)
def share_test(col, key, cond_room):
    sub = H[(H.room.notna()) & (~H.room.isin(['--', '-', ''])) & H.dep.notna()] if cond_room else H[H.dep.notna()]
    keys = sub[key].values; vals = sub[col].values; dep = sub.dep.values; band = sub.band.values
    idx = np.arange(len(sub))
    def count(k):
        grp = collections.defaultdict(list)
        for i in idx: grp[k[i]].append(i)
        c = 0
        for m in grp.values():
            for a in range(len(m)):
                for b in range(a + 1, len(m)):
                    i, j = m[a], m[b]
                    if cond_room and abs(dep[i] - dep[j]) > 3: continue
                    if vals[i] & vals[j]: c += 1
        return c
    obs = count(keys); bb = collections.defaultdict(list)
    for i in idx: bb[band[i]].append(i)
    sims = []
    for _ in range(2000):
        k = keys.copy()
        for ii in bb.values():
            if len(ii) > 1: k[ii] = keys[rng3.permutation(ii)]
        sims.append(count(k))
    return obs, np.mean(sims), (1 + np.sum(np.array(sims) >= obs)) / 2001, int(sum(1 for v in vals if v))
for col, lab in (('comps', 'number + fish compound'), ('fish', 'any fish sign')):
    for key, cr, nm in (('rk', True, 'same room, depth within 3 ft'), ('house', False, 'same house')):
        o, e, p, n = share_test(col, key, cr)
        print(f'K1/K2 {lab}, {nm}: {o} pairs against {e:.2f} by chance, P {p:.3f} ({n} seals carry one)')

# K3/K4 animal and ending by compound (first catalogue seals, compounds on 4+ seals)
S = F[(F.cat == 'L') & (F.kind == 'seal')].drop_duplicates(['obj', 'compound'])
S = S.merge(objs[['animal', 'ending']].rename(columns={'ending': 'end2'}), left_on='obj', right_index=True, how='left')
top = S.compound.value_counts(); top = top[top >= 4].index
S = S[S.compound.isin(top)]
def cramer(a, b):
    t = pd.crosstab(a, b).values; n = t.sum(); e = t.sum(1, keepdims=True) * t.sum(0, keepdims=True) / n
    chi = ((t - e) ** 2 / np.where(e == 0, 1, e)).sum(); k = min(t.shape) - 1
    return np.sqrt(chi / (n * k)) if k > 0 else 0
for col, lab in (('animal_y' if 'animal_y' in S else 'animal', 'animal'), ('end2', 'ending')):
    obs = cramer(S.compound.values, S[col].values)
    sims = [cramer(rng3.permutation(S.compound.values), S[col].values) for _ in range(2000)]
    print(f'K3/K4 compound x {lab}: Cramer V {obs:.3f} against {np.mean(sims):.3f} shuffled, P {(1+np.sum(np.array(sims)>=obs))/2001:.3f} ({len(S)} seals, {len(top)} compounds)')
    print(pd.crosstab(S.compound, S[col]).to_string())
