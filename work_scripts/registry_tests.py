#!/usr/bin/env python3
"""WHO'S WHO, step 2: rank the great houses, test where they lived, and run tests (a)-(e).

PREDICTIONS, written before any number below was computed:
 G  Members of a great house cluster: same-building and same-block pairs inside one house beat shuffles of the
    house labels among seals of the same site (locations held fixed).
 a  Agents ("X's man") sit away from their master's own building more often than family members (owner seals of
    the same house) sit away from their house's other buildings.  Away rate agents > away rate members.
 b  Goods words beside a house name match the name where the name is a trade: Boxed-cotton (590-390) objects carry
    a cotton word (390/405/370/371) outside the name more than other named goods objects; grain-named houses
    (806 Bounty, 416 Grain-heap, 605 Granary, 413 grain, 845 sheaves) carry grain words; the Chest house (590,
    not Boxed-cotton) and the Kalam house (705/706) carry store/measure words.
 c  Seal pairs that share a TAG (or a PERSONAL part) but not a crest are NOT more often neighbours than chance
    (ratio about 1), while same-crest pairs are (ratio above 1): the crest, not the tag, is the family.
 d  The same full name on a seal and on a goods object (tablet, tag, pot, copper tablet) at one city: the goods
    object sits in the seal's area more often than goods objects shuffled within the city.
 e  Names joining two crests with 690 "allied" or 407 "kindred": the two linked houses share areas and cities more
    than random pairs of houses of similar size, and more than pairs joined in one name without 690/407.
Writes work_data/registry/great_houses.csv, house_spread.csv, tests.txt.  Run: python3 registry_tests.py (~1-2 min).
"""
import os, re, collections, random, math
import pandas as pd, numpy as np
from scipy.stats import fisher_exact
random.seed(7); np.random.seed(7)
ROOT = '/home/antigravity/Cuuper22/ivc'; OUT = f'{ROOT}/work_data/registry'
LOG = open(f'{OUT}/tests.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n')

P = pd.read_csv(f'{OUT}/people.csv', dtype=str).fillna('')
A = pd.read_csv(f'{OUT}/names_all.csv', dtype=str).fillna('')
A = A[(A.damaged == 'False') & (A.goods_line == 'False')]
H = pd.read_csv(f'{OUT}/houses.csv', dtype=str).fillna('')
for c in ('seals', 'members', 'agents_kept', 'objects_all', 'goods_objects', 'n_cities'): H[c] = H[c].astype(int)
TITLES = {'142', '151', '152', '153', '154', '155', '156', '157', '158', '161', '368', '525', '526', '527', '842', '617', '717', '097', '137', '090'}
NSH = 2000

# ---------- the great houses ----------
G = H[(H.seals >= 5) & (~H.house_key.isin(TITLES))].sort_values(['objects_all', 'n_cities'], ascending=False).head(20).copy()
G['rank'] = range(1, len(G) + 1)
say('GREAT HOUSES (rank by objects naming the house; at least 5 seals; title words left out):')
say(G[['rank', 'house_key', 'english', 'sounds', 'seals', 'agents_kept', 'objects_all', 'n_cities']].to_string(index=False))
TOP = list(G.house_key)

# ---------- G: clustering inside a site ----------
def pair_counts(lab, loc):
    """same-label pairs that share loc, per label"""
    c = collections.Counter(); byloc = collections.defaultdict(list)
    for l, z in zip(lab, loc): byloc[z].append(l)
    for z, ls in byloc.items():
        cc = collections.Counter(ls)
        for l, k in cc.items(): c[l] += k * (k - 1) // 2
    return c
spread = []
say('\nG  clustering: same-house pairs sharing a building / block / area, against shuffles of house labels within site')
tot_obs = collections.Counter(); tot_null = collections.defaultdict(lambda: np.zeros(NSH))
per = {}
for site in ('Mohenjo-daro', 'Harappa'):
    for lev in ('building', 'block', 'area_key'):
        S = P[(P.city == site) & (P[lev] != '')]
        lab = list(S.house_key); loc = list(S[lev])
        obs = pair_counts(lab, loc)
        null = collections.defaultdict(list)
        for t in range(NSH):
            sh = lab[:]; random.shuffle(sh)
            c = pair_counts(sh, loc)
            for h in TOP: null[h].append(c.get(h, 0))
            null['_all_top'].append(sum(c.get(h, 0) for h in TOP))
        o_all = sum(obs.get(h, 0) for h in TOP); a = np.array(null['_all_top'])
        say(f'  {site:12s} {lev:8s} top-20 houses: {o_all} pairs against {a.mean():.2f} (ratio {o_all / max(a.mean(), 1e-9):.2f}, P {(1 + (a >= o_all).sum()) / (NSH + 1):.4f}); seals with a findspot {len(S)}')
        for h in TOP:
            a = np.array(null[h]); per[(h, site, lev)] = (obs.get(h, 0), a.mean(), (1 + (a >= obs.get(h, 0)).sum()) / (NSH + 1))

# ---------- spread of each great house ----------
for h in TOP:
    g = A[A.house_key == h]; sp = P[P.house_key == h]
    row = dict(house_key=h)
    for site in ('Mohenjo-daro', 'Harappa'):
        for lev in ('building', 'block', 'area_key'):
            o, e, p = per[(h, site, lev)]; row[f'{site[:3]}_{lev}'] = f'{o} vs {e:.2f} (P {p:.3f})'
    row['top_buildings'] = '; '.join(f'{k} {v}' for k, v in sp[sp.building != ''].building.value_counts().head(5).items())
    row['top_areas_all_objects'] = '; '.join(f'{k} {v}' for k, v in g[g.area_key != ''].drop_duplicates('object_id').area_key.value_counts().head(5).items())
    row['ranks'] = '; '.join(f'{k} {v}' for k, v in sp.ending.value_counts().items())
    row['kinds'] = '; '.join(f'{k} {v}' for k, v in g.drop_duplicates('object_id').kind.value_counts().items())
    row['overseas_bull'] = int((sp.animal == 'short-horned bull').sum())
    row['stand_letters'] = '; '.join(f'{k} {v}' for k, v in sp[sp.stand != ''].stand.value_counts().items())
    row['bins'] = '; '.join(f'{b} {(g.drop_duplicates("object_id").bin == b).sum()}' for b in ('early', 'middle', 'late'))
    row['agent_ids'] = '; '.join(sp[sp.master != ''].cisi)
    row['example_ids'] = '; '.join(sp.cisi.head(6))
    spread.append(row)
SP = pd.DataFrame(spread); G = G.merge(SP, on='house_key'); G.to_csv(f'{OUT}/great_houses.csv', index=False)
for h in TOP:
    o, e, p = per[(h, 'Mohenjo-daro', 'building')]; o2, e2, p2 = per[(h, 'Mohenjo-daro', 'block')]
    say(f'   {h:8s} Mohenjo-daro building {o} vs {e:.2f} (P {p:.3f}) | block {o2} vs {e2:.2f} (P {p2:.3f})')

P['name_core'] = A.set_index('face_id').name_core.reindex(P.face_id).fillna('').values
# ---------- (a) agents away from the master ----------
say('\n(a) agents vs family: is the seal found in a building / area where the house has another (owner) object?')
own = A[A.ending.map(lambda e: not e.startswith("X's man"))]
def home_sets(level, by):
    hs = collections.defaultdict(collections.Counter)
    for k, z in zip(own[by], own[level]):
        if z: hs[k][z] += 1
    return hs
for by, label in (('house_key', 'crest house'), ('name_core', 'exact master name')):
    for level in ('building', 'area_key'):
        hs = home_sets(level, by)
        ag = P[(P.master != '') & (P[level] != '')]
        mem = P[(P.master == '') & (P[level] != '')]
        a_away = a_n = 0
        for _, r in ag.iterrows():
            k = r[by] if by == 'house_key' else r.master
            homes = hs.get(k, {})
            site_has = any(z.split('|')[0] == r.city for z in homes)
            if not site_has: continue
            a_n += 1; a_away += r[level] not in homes
        m_away = m_n = 0
        for _, r in mem.iterrows():
            k = r[by]
            homes = dict(hs.get(k, {}))
            if r[level] in homes:
                homes[r[level]] -= 1          # leave this seal out
                if homes[r[level]] <= 0: del homes[r[level]]
            if not any(z.split('|')[0] == r.city for z in homes): continue
            m_n += 1; m_away += r[level] not in homes
        if a_n and m_n:
            odds, p = fisher_exact([[a_away, a_n - a_away], [m_away, m_n - m_away]], alternative='greater')
            say(f'  by {label:17s} at {level:8s}: agents away {a_away} of {a_n} ({a_away / a_n:.0%}); members away {m_away} of {m_n} ({m_away / m_n:.0%}); one-sided P {p:.3f}')
        else:
            say(f'  by {label:17s} at {level:8s}: agents usable {a_n}, members usable {m_n} (too few)')

# ---------- (b) goods words ----------
say('\n(b) goods words beside the house name (signs on the same goods object outside the name)')
GOODS = {'cotton': {'390', '405', '370', '371'},
    'grain': {'413', '416', '421', '422', '423', '424', '605', '806', '838', '831', '844', '845', '501'},
    'store/measure': {'575', '621', '590', '592', '335', '336', '700', '703', '705', '706', '711', '540', '554', '320', '321', '323', '171', '480'},
    'ivory/metal/bead': {'923', '595', '790', '645', '850'}, 'ship': {'500'}}
G2K = {s: k for k, v in GOODS.items() for s in v}
d_tok = pd.read_csv(f'{ROOT}/work_data/corpus_english2.csv', dtype=str).fillna('')
d_tok = d_tok[~d_tok.face_id.str.startswith('obj')] if 'face_id' in d_tok else d_tok
objtok = collections.defaultdict(list)
for o, s in zip(d_tok.object_id, d_tok.signs):
    objtok[o] += [t for t in s.split('-') if t]
GO = A[A.kind != 'seal'].drop_duplicates('object_id').copy()
def cats(r):
    toks = list(objtok.get(r.object_id, []))
    for s in r.name_full.split('-'):
        if s in toks: toks.remove(s)
    return {G2K[s] for s in toks if s in G2K}
GO['cats'] = GO.apply(cats, axis=1)
GO['text'] = GO.object_id.map(lambda o: '-'.join(objtok.get(o, [])))
TESTS = [('Boxed-cotton', {'590-390'}, 'cotton'), ('grain-named', {'806', '416', '605', '413', '845', '844', '838'}, 'grain'),
         ('Chest', {'590'}, 'store/measure'), ('Kalam', {'705'}, 'store/measure'), ('Cotton (390 as crest)', {'390'}, 'cotton')]
for unit in ('objects', 'distinct texts'):
    D = GO if unit == 'objects' else GO.drop_duplicates(['text', 'site'])
    for nm, keys, cat in TESTS:
        inh = D[D.house_key.isin(keys)]; out = D[~D.house_key.isin(keys)]
        a = sum(cat in c for c in inh.cats); b = sum(cat in c for c in out.cats)
        if len(inh):
            odds, p = fisher_exact([[a, len(inh) - a], [b, len(out) - b]], alternative='greater')
            say(f'  [{unit}] {nm:22s} {cat:14s}: {a} of {len(inh)} ({a / len(inh):.0%}) against {b} of {len(out)} ({b / len(out):.1%}); one-sided P {p:.4f}')
say('  what each grain/cotton/chest house object carries (distinct texts):')
for nm, keys, cat in TESTS[:4]:
    for _, r in GO[GO.house_key.isin(keys)].drop_duplicates(['text', 'site']).head(12).iterrows():
        say(f'     {nm:12s} {r.cisi:10s} {r.kind:5s} {r.site:12s} {r.text:40s} cats={sorted(r.cats)}')

# ---------- (c) tag/personal without crest ----------
say('\n(c) pairs of seals in one city: share building / area, against locations shuffled within site')
def pairstats(S, level, rel):
    idx = list(range(len(S))); hk = list(S.house_key); tg = list(S.tag); ps = list(S.personal); loc = list(S[level])
    pairs = []
    for i in idx:
        for j in idx[i + 1:]:
            if rel == 'crest' and hk[i] == hk[j]: pairs.append((i, j))
            elif rel == 'tag' and tg[i] and tg[i] == tg[j] and hk[i] != hk[j]: pairs.append((i, j))
            elif rel == 'personal' and ps[i] and ps[i] == ps[j] and hk[i] != hk[j]: pairs.append((i, j))
    obs = sum(loc[i] == loc[j] for i, j in pairs)
    nl = []
    for t in range(NSH // 2):
        sh = loc[:]; random.shuffle(sh); nl.append(sum(sh[i] == sh[j] for i, j in pairs))
    a = np.array(nl); return len(pairs), obs, a.mean(), (1 + (a >= obs).sum()) / (len(a) + 1)
for site in ('Mohenjo-daro', 'Harappa'):
    for level in ('building', 'area_key'):
        S = P[(P.city == site) & (P[level] != '')].reset_index(drop=True)
        for rel in ('crest', 'tag', 'personal'):
            n, o, e, p = pairstats(S, level, rel)
            say(f'  {site:12s} {level:8s} same {rel:8s}{" (different crest)" if rel != "crest" else "                  "}: {n} pairs, {o} share against {e:.2f} (ratio {o / max(e, 1e-9):.2f}, P {p:.4f})')

# ---------- (d) seal and goods object with the same full name ----------
say('\n(d) same full name on a seal and on a goods object in one city: same area / same building?')
SE = A[(A.kind == 'seal')]; GD = A[A.kind != 'seal'].drop_duplicates('object_id')
for level in ('area_key', 'building', 'block'):
    res = []
    for site in ('Mohenjo-daro', 'Harappa'):
        gs = GD[(GD.site == site) & (GD[level] != '')].reset_index(drop=True)
        ss = SE[(SE.site == site) & (SE[level] != '')]
        if not len(gs): continue
        byname = collections.defaultdict(list)
        for i, nmc in enumerate(gs.name_core): byname[nmc].append(i)
        units = [(r[level], byname[r.name_core]) for _, r in ss.iterrows() if r.name_core in byname]
        loc = list(gs[level])
        obs = sum(any(loc[i] == z for i in ii) for z, ii in units)
        nl = []
        for t in range(NSH // 2):
            sh = loc[:]; random.shuffle(sh); nl.append(sum(any(sh[i] == z for i in ii) for z, ii in units))
        res.append((site, len(units), obs, np.mean(nl), (1 + (np.array(nl) >= obs).sum()) / (len(nl) + 1)))
    for site, n, o, e, p in res:
        say(f'  {site:12s} {level:8s}: {n} seals whose full name is on a goods object in the same city; goods object in the same {level}: {o} against {e:.2f} (ratio {o / max(e, 1e-9):.2f}, P {p:.4f})')

# ---------- (e) allied / kindred ----------
say('\n(e) names joining two crests with 690 "allied" or 407 "kindred"')
CRESTS = set(H[(H.seals >= 5) & (~H.house_key.isin(TITLES))].house_key) - {'590-390'}
def crest_signs(core):
    t = core.split('-'); out = []
    for s in t:
        s2 = '705' if s == '706' else s
        if s2 in CRESTS and s2 not in out: out.append(s2)
    return out
link = collections.Counter(); plain = collections.Counter(); link_ids = collections.defaultdict(set)
for _, r in A.drop_duplicates('object_id').iterrows():
    t = r.name_core.split('-'); cs = crest_signs(r.name_core)
    if len(cs) < 2: continue
    pr = tuple(sorted((cs[0], cs[-1])))
    if '690' in t or '407' in t: link[pr] += 1; link_ids[pr].add(r.cisi)
    else: plain[pr] += 1
say(f'  linked crest pairs (690/407): {len(link)} distinct, {sum(link.values())} objects; plain two-crest pairs: {len(plain)} distinct')
for pr, n in link.most_common(): say(f'     {pr} {n} objects: {", ".join(sorted(link_ids[pr])[:6])}')
# co-location of members of two houses
mem = P[P.area_key != '']
area_of = collections.defaultdict(collections.Counter); city_of = collections.defaultdict(set); bld_of = collections.defaultdict(collections.Counter)
for k, z, b, c in zip(mem.house_key, mem.area_key, mem.building, mem.city): area_of[k][z] += 1; city_of[k].add(c); bld_of[k][b] += 1 if b else 0
for k, c in zip(A.house_key, A.site): city_of[k].add(c)
def share(a, b, of):
    A_, B_ = of.get(a, {}), of.get(b, {})
    na, nb = sum(A_.values()), sum(B_.values())
    if not na or not nb: return None
    return sum(A_[z] * B_.get(z, 0) for z in A_ if z) / (na * nb)
def jac(a, b):
    x, y = city_of.get(a, set()), city_of.get(b, set())
    return len(x & y) / len(x | y) if x | y else None
pool = [k for k in CRESTS if sum(area_of[k].values()) >= 2]
rnd = [(a, b) for i, a in enumerate(pool) for b in pool[i + 1:]]
for nm, of in (('area', area_of), ('building', bld_of)):
    for lab, C in (('linked 690/407', link), ('two crests, no link', plain)):
        v = [share(a, b, of) for a, b in C if share(a, b, of) is not None]
        r = [share(a, b, of) for a, b in rnd if share(a, b, of) is not None]
        if v:
            # permutation: mean of v against means of random draws of the same size from all crest pairs
            m = np.mean(v); draws = np.array([np.mean(random.sample(r, len(v))) for _ in range(NSH)])
            say(f'  {lab:20s} same {nm:8s} share of member pairs: {m:.4f} over {len(v)} house pairs; random pairs {draws.mean():.4f} (ratio {m / draws.mean():.2f}, P {(1 + (draws >= m).sum()) / (NSH + 1):.4f})')
for lab, C in (('linked 690/407', link), ('two crests, no link', plain)):
    v = [jac(a, b) for a, b in C if jac(a, b) is not None]; r = [jac(a, b) for a, b in rnd if jac(a, b) is not None]
    m = np.mean(v); draws = np.array([np.mean(random.sample(r, len(v))) for _ in range(NSH)])
    say(f'  {lab:20s} city overlap (shared cities / all cities): {m:.3f} over {len(v)} pairs; random {draws.mean():.3f} (ratio {m / draws.mean():.2f}, P {(1 + (draws >= m).sum()) / (NSH + 1):.4f})')
LOG.close()
