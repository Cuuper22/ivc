#!/usr/bin/env python3
"""WHO'S WHO, step 2b: one redesign and one new idea for each test that went against in registry_tests.py.

PREDICTIONS, written before the numbers:
 a-redesign  Shuffle test: agents' buildings shuffled among all seals of the city. If agents are posted away, agents sit
             in a building holding an owner object of their master's crest LESS often than shuffled; members MORE.
             (Run because the first test showed agents near the master more often than members: 5 of 27 against 52 of 622.)
 a-new       READING FLIP: "X's man" = the manager living in X's house (āḷ "manager of a house"). Then agents sit with
             their master's crest above chance, and agent seals are bigger than the owner seals they serve.
 b-redesign  Goods words looked for on EVERY object carrying the house name anywhere (no ending needed), cup 700 left
             out of store words (the cup is the account unit on most tablet backs). Trade-named houses beat the rest.
 b-new       Trade-named houses (Boxed-cotton, Bounty 806, Grain-heap 416, Granary 605, Chest 590, Kalam 705/706) put a
             larger share of their objects on goods (tablets, tags, pots, copper) than star-named houses do.
 d-redesign  Only rare names (on at most 3 seals): the goods object with the same name sits in the seal's area above
             shuffled goods locations.
 d-new       Tablets with a person's name sit in the same area as OTHER tablets with that name (the issuing office)
             more than seals do with seals: a name has a desk, not a home.
 e-redesign  Link sign must stand BETWEEN the two crests (A ... 690/407 ... B); 690 and 407 are not crests themselves.
 e-new       Link names are records more than seals: the share of tablets/copper tablets among objects with a link name
             is higher than among names with two crests and no link.
Writes work_data/registry/tests2.txt.  Run: python3 registry_tests2.py (about a minute).
"""
import collections, random, re
import pandas as pd, numpy as np
from scipy.stats import fisher_exact, mannwhitneyu
random.seed(11)
ROOT = '/home/antigravity/Cuuper22/ivc'; OUT = f'{ROOT}/work_data/registry'
LOG = open(f'{OUT}/tests2.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n')
P = pd.read_csv(f'{OUT}/people.csv', dtype=str).fillna('')
A = pd.read_csv(f'{OUT}/names_all.csv', dtype=str).fillna('')
A = A[(A.damaged == 'False') & (A.goods_line == 'False')]
H = pd.read_csv(f'{OUT}/houses.csv', dtype=str).fillna(''); H['seals'] = H.seals.astype(int)
E = pd.read_csv(f'{ROOT}/work_data/corpus_english2.csv', dtype=str).fillna('')
P['name_core'] = A.set_index('face_id').name_core.reindex(P.face_id).fillna('').values
NSH = 2000

# ---------- (a) ----------
say('(a) redesign: agents and members against shuffled buildings (owner objects of the same crest as the landmark)')
own = A[~A.ending.str.startswith("X's man")]
homes = collections.defaultdict(collections.Counter)
for k, b in zip(own.house_key, own.building):
    if b: homes[k][b] += 1
for site in ('Mohenjo-daro', 'all cities'):
    S = P[(P.building != '')] if site == 'all cities' else P[(P.building != '') & (P.city == site)]
    blds = list(S.building); cities = list(S.city)
    for grp, sub in (('agents', S[S.master != '']), ('members', S[S.master == ''])):
        def hit(k, b, self_out):
            h = homes.get(k, {}); c = h.get(b, 0) - (1 if self_out else 0)
            return c > 0
        obs = sum(hit(k, b, grp == 'members') for k, b in zip(sub.house_key, sub.building))
        bycity = collections.defaultdict(list)
        for b, c in zip(blds, cities): bycity[c].append(b)
        nl = []
        for t in range(NSH // 4):
            nl.append(sum(hit(k, random.choice(bycity[c]), False) for k, c in zip(sub.house_key, sub.city)))
        a = np.array(nl)
        say(f'  {site:12s} {grp:8s}: {obs} of {len(sub)} sit in a building with an owner object of their crest; shuffled {a.mean():.2f} '
            f'(ratio {obs / max(a.mean(), 1e-9):.2f}, P high {(1 + (a >= obs).sum()) / (len(a) + 1):.4f}, P low {(1 + (a <= obs).sum()) / (len(a) + 1):.4f})')
say('  agents found in a building that also holds an owner object of their crest:')
for _, r in P[(P.master != '') & (P.building != '')].iterrows():
    if homes.get(r.house_key, {}).get(r.building, 0) > 0:
        mates = own[(own.house_key == r.house_key) & (own.building == r.building)]
        say(f'     {r.cisi:8s} {r.building:34s} {r.signs:32s} | owners there: ' + ', '.join(f'{m.cisi} {m.signs}' for _, m in mates.iterrows()))
say('(a) new idea: are agent seals bigger than owner seals of the same crest? (face area mm2, same city)')
P['area_mm2'] = pd.to_numeric(P.hmm, errors='coerce') * pd.to_numeric(P.vmm, errors='coerce')
ag = P[(P.master != '') & (P.area_mm2 > 0)]; ow = P[(P.master == '') & (P.area_mm2 > 0) & (P.house_key.isin(set(ag.house_key)))]
ow_all = P[(P.master == '') & (P.area_mm2 > 0)]
say(f'  agents median {ag.area_mm2.median():.0f} mm2 (n {len(ag)}); owners of the same crests {ow.area_mm2.median():.0f} (n {len(ow)}), '
    f'P {mannwhitneyu(ag.area_mm2, ow.area_mm2, alternative="greater").pvalue:.4f}; all owners {ow_all.area_mm2.median():.0f} (P {mannwhitneyu(ag.area_mm2, ow_all.area_mm2, alternative="greater").pvalue:.4f})')

# ---------- (b) ----------
say('\n(b) redesign: every object carrying the house name anywhere; cup 700 left out of store words')
GO = {'cotton': {'390', '405', '370', '371'}, 'grain': {'413', '416', '421', '422', '423', '424', '605', '806', '838', '831', '844', '845'},
      'store/measure': {'575', '621', '590', '592', '335', '336', '703', '705', '706', '711', '540', '554', '320', '321', '323', '171', '480'}}
objtok = collections.defaultdict(list); objkind = {}; objsite = {}
for o, s, k, st in zip(E.object_id, E.signs, E.object_kind, E.site):
    objtok[o] += [t for t in s.split('-') if t]; objkind[o] = k; objsite[o] = st
def find(o, pat):
    t = objtok[o]; n = len(pat)
    return [i for i in range(len(t) - n + 1) if t[i:i + n] == pat]
HOUSES = {'Boxed-cotton': (['590', '390'], 'cotton', None), 'Bounty 806': (['806'], 'grain', None), 'Grain-heap 416': (['416'], 'grain', None),
          'Granary 605': (['605'], 'grain', None), 'Chest 590 (not +390)': (['590'], 'store/measure', '390'), 'Kalam 705': (['705'], 'store/measure', None),
          'Kalam 706': (['706'], 'store/measure', None)}
NAMESIGNS = set(H[H.seals >= 5].house_key) - set(GO['grain']) - set(GO['cotton']) - set(GO['store/measure'])
for nm, (pat, cat, notnext) in HOUSES.items():
    for unit in ('objects', 'distinct texts'):
        inh = []; seen = set()
        for o in objtok:
            hits = find(o, pat)
            if notnext: hits = [i for i in hits if not (i + 1 < len(objtok[o]) and objtok[o][i + 1] == notnext)]
            if not hits: continue
            key = ('-'.join(objtok[o]), objsite[o]) if unit == 'distinct texts' else o
            if key in seen: continue
            seen.add(key)
            t = list(objtok[o]); i = hits[0]; del t[i:i + len(pat)]
            inh.append(any(s in GO[cat] for s in t))
        base = []; seen = set()   # objects that carry some other house crest and not this one
        for o in objtok:
            if find(o, pat[:1]): continue
            if not any(s in NAMESIGNS for s in objtok[o]): continue
            key = ('-'.join(objtok[o]), objsite[o]) if unit == 'distinct texts' else o
            if key in seen: continue
            seen.add(key); base.append(any(s in GO[cat] for s in objtok[o]))
        a, n = sum(inh), len(inh); b, m = sum(base), len(base)
        p = fisher_exact([[a, n - a], [b, m - b]], alternative='greater')[1]
        say(f'  [{unit:14s}] {nm:22s} {cat:13s}: {a} of {n} ({a / max(n, 1):.0%}) against {b} of {m} ({b / max(m, 1):.1%}), one-sided P {p:.4g}')
say('(b) new idea: share of a house\'s objects that are goods objects (not seals)')
trade = {'590-390', '806', '416', '605', '590', '705'}; star = {'220', '231', '233', '235', '240', '032+220', '003+220', '016+220'}
for lab, ks in (('trade-named', trade), ('star-named', star)):
    g = A[A.house_key.isin(ks)].drop_duplicates('object_id')
    say(f'  {lab}: {(g.kind != "seal").sum()} goods of {len(g)} objects ({(g.kind != "seal").mean():.0%}); distinct goods texts {g[g.kind != "seal"].drop_duplicates(["signs", "site"]).shape[0]}')
gt = A[A.house_key.isin(trade)].drop_duplicates('object_id'); gs = A[A.house_key.isin(star)].drop_duplicates('object_id')
a, n, b, m = (gt.kind != 'seal').sum(), len(gt), (gs.kind != 'seal').sum(), len(gs)
say(f'  Fisher one-sided P {fisher_exact([[a, n - a], [b, m - b]], alternative="greater")[1]:.4g}')
gt2 = gt.drop_duplicates(['signs', 'site']); gs2 = gs.drop_duplicates(['signs', 'site'])
a, n, b, m = (gt2.kind != 'seal').sum(), len(gt2), (gs2.kind != 'seal').sum(), len(gs2)
say(f'  distinct texts: trade {a} of {n} ({a / n:.0%}) against star {b} of {m} ({b / m:.0%}); P {fisher_exact([[a, n - a], [b, m - b]], alternative="greater")[1]:.4g}')

# ---------- (d) ----------
say('\n(d) redesign: rare names only (full name on at most 3 seals)')
SE = A[A.kind == 'seal']; GD = A[A.kind != 'seal'].drop_duplicates('object_id')
nseal = SE.name_core.value_counts()
for level in ('area_key', 'block'):
    for site in ('Mohenjo-daro', 'Harappa'):
        gs_ = GD[(GD.site == site) & (GD[level] != '')].reset_index(drop=True)
        ss = SE[(SE.site == site) & (SE[level] != '') & (SE.name_core.map(nseal) <= 3)]
        byname = collections.defaultdict(list)
        for i, nmc in enumerate(gs_.name_core): byname[nmc].append(i)
        units = [(r[level], byname[r.name_core]) for _, r in ss.iterrows() if r.name_core in byname]
        loc = list(gs_[level]); obs = sum(any(loc[i] == z for i in ii) for z, ii in units)
        nl = []
        for t in range(NSH // 2):
            sh = loc[:]; random.shuffle(sh); nl.append(sum(any(sh[i] == z for i in ii) for z, ii in units))
        a = np.array(nl)
        say(f'  {site:12s} {level:8s}: {len(units)} rare-name seals with a goods twin; same {level}: {obs} against {a.mean():.2f} (ratio {obs / max(a.mean(), 1e-9):.2f}, P {(1 + (a >= obs).sum()) / (len(a) + 1):.4f})')
say('(d) new idea: does a name have a desk? pairs of DIFFERENT objects with one full name in one city, sharing an area, against shuffled areas')
for site in ('Mohenjo-daro', 'Harappa'):
    for lab, D in (('tablet-tablet', A[A.kind.isin(['mtab', 'ctab'])]), ('seal-seal', SE)):
        D = D[(D.site == site) & (D.area_key != '')].drop_duplicates('object_id').reset_index(drop=True)
        D = D.drop_duplicates(['signs', 'area_key'])     # moulded copies in one area count once
        names = list(D.name_core); loc = list(D.area_key); sg = list(D.signs)
        idx = collections.defaultdict(list)
        for i, nmc in enumerate(names): idx[nmc].append(i)
        pairs = [(i, j) for v in idx.values() for a_ in range(len(v)) for i, j in [(v[a_], b_) for b_ in v[a_ + 1:]] if sg[i] != sg[j]]   # different texts only: copies cannot make a pair
        obs = sum(loc[i] == loc[j] for i, j in pairs); nl = []
        for t in range(NSH // 2):
            sh = loc[:]; random.shuffle(sh); nl.append(sum(sh[i] == sh[j] for i, j in pairs))
        a = np.array(nl)
        say(f'  {site:12s} {lab:13s}: {len(pairs)} same-name pairs (different texts), same area {obs} against {a.mean():.2f} (ratio {obs / max(a.mean(), 1e-9):.2f}, P {(1 + (a >= obs).sum()) / (len(a) + 1):.4f})')

# ---------- (e) ----------
say('\n(e) redesign: the link sign stands between two crests')
CRESTS = set(H[(H.seals >= 5)].house_key) - {'690', '407', '590-390', '142', '156', '151', '368', '527', '617', '717'}
CRESTS = {('705' if c == '706' else c) for c in CRESTS if '+' not in c}
link = collections.Counter(); lids = collections.defaultdict(set); plain = collections.Counter(); kinds = {'link': collections.Counter(), 'plain': collections.Counter()}
for _, r in A.drop_duplicates('object_id').iterrows():
    t = ['705' if s == '706' else s for s in r.name_core.split('-')]
    pos = [i for i, s in enumerate(t) if s in CRESTS]
    if len(pos) < 2: continue
    lk = [i for i, s in enumerate(t) if s in ('690', '407')]
    between = [(i, j) for i in pos for j in pos if i < j and t[i] != t[j] and any(i < q < j for q in lk)]
    if between:
        i, j = between[0]; pr = tuple(sorted((t[i], t[j]))); link[pr] += 1; lids[pr].add(r.cisi); kinds['link'][r.kind] += 1
    elif not lk:
        pr = tuple(sorted((t[pos[0]], t[pos[-1]])))
        if pr[0] != pr[1]: plain[pr] += 1; kinds['plain'][r.kind] += 1
say(f'  linked pairs: {len(link)} distinct over {sum(link.values())} objects')
for pr, n in link.most_common(): say(f'     {pr} {n}: {", ".join(sorted(lids[pr])[:6])}')
mem = P[P.area_key != '']
area_of = collections.defaultdict(collections.Counter); city_of = collections.defaultdict(set)
for k, z in zip(mem.house_key, mem.area_key): area_of[k][z] += 1
for k, c in zip(A.house_key, A.site): city_of[k].add(c)
def share(a, b):
    A_, B_ = area_of.get(a, {}), area_of.get(b, {}); na, nb = sum(A_.values()), sum(B_.values())
    return None if not na or not nb else sum(A_[z] * B_.get(z, 0) for z in A_) / (na * nb)
def jac(a, b):
    x, y = city_of.get(a, set()), city_of.get(b, set()); return len(x & y) / len(x | y) if x | y else None
pool = sorted(CRESTS); rnd = [(a, b) for i, a in enumerate(pool) for b in pool[i + 1:]]
for nm, f in (('same area', share), ('city overlap', jac)):
    for lab, C in (('linked', link), ('plain two-crest', plain)):
        v = [f(a, b) for a, b in C if f(a, b) is not None]; r = [f(a, b) for a, b in rnd if f(a, b) is not None]
        if len(v) and len(r) >= len(v):
            m = np.mean(v); dr = np.array([np.mean(random.sample(r, len(v))) for _ in range(NSH)])
            say(f'  {lab:16s} {nm:12s}: {m:.4f} over {len(v)} pairs; random crest pairs {dr.mean():.4f} (ratio {m / dr.mean():.2f}, P {(1 + (dr >= m).sum()) / (NSH + 1):.4f})')
say('(e) new idea: object kinds of link names against plain two-crest names')
for k in ('link', 'plain'): say(f'  {k}: ' + ', '.join(f'{a} {b}' for a, b in kinds[k].most_common()))
lt = sum(v for k, v in kinds['link'].items() if k in ('mtab', 'ctab')); ln = sum(kinds['link'].values())
pt = sum(v for k, v in kinds['plain'].items() if k in ('mtab', 'ctab')); pn = sum(kinds['plain'].values())
say(f'  tablets: link {lt} of {ln} ({lt / max(ln, 1):.0%}) against plain {pt} of {pn} ({pt / max(pn, 1):.0%}); one-sided P {fisher_exact([[lt, ln - lt], [pt, pn - pt]], alternative="greater")[1]:.4g}')
LOG.close()
