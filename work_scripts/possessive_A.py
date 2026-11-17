#!/usr/bin/env python3
"""Part A of the possessive model: what follows the jar, servant vs owner seals, master-servant pairs.
Writes work_data/possessive/*.csv and prints tables used in jobs/out/possessive_model.md."""
import sys, os, collections, itertools
sys.path.insert(0, '/home/claude/ivc/work_scripts')
import numpy as np, pandas as pd
from scipy import stats
from gloss2 import *
OUT = '/home/claude/ivc/work_data/possessive'; os.makedirs(OUT, exist_ok=True)
d = load2(); lex = learn(d); own = lex['owner']
d['r'] = [parse_face(x, lex, own) for x in d.tok]
d['h'] = pd.to_numeric(d['horizontal(mm)'], errors='coerce'); d['v'] = pd.to_numeric(d['vertical(mm)'], errors='coerce')
d['area'] = d.h * d.v
d.loc[(d.h <= 0) | (d.v <= 0), 'area'] = np.nan
d['obj'] = [object_id(i) for i in d['id']]
d['house'] = d['site'] + ' / ' + d['area-section'] + ' / ' + d['block-house']
d['text_s'] = ['-'.join(x) for x in d.tok]
sh = shapes()
sealish = d[(d.group != 'tablet') & (d.group != 'copper tablet')]
C = sealish[sealish.complete_txt].copy()
# one row per (site, text) so duplicate sealings do not vote many times
Cd = C.drop_duplicates(['site', 'text_s'])
P = []
def p(*a): print(*a); P.append(' '.join(str(x) for x in a))

# ---------- A1 followers
fol = []
for _, r in Cd.iterrows():
    x = r.tok; R = r.r['roles']
    for i, s in enumerate(x):
        if s == '740' and i + 1 < len(x): fol.append((x[i + 1], r))
tot_sign = collections.Counter(s for x in Cd.tok for s in set(x))
nj_last = sum(1 for x in Cd.tok for i, s in enumerate(x) if s == '740' and i == len(x) - 1)
nj = sum(1 for x in Cd.tok for s in x if s == '740')
p(f'distinct (site,text) non-tablet complete texts {len(Cd)}; jar uses {nj}; jar last {nj_last}; jar followed {len(fol)}')
rows = []
fc = collections.Counter(s for s, _ in fol)
for s, k in fc.most_common(40):
    rs = [r for t, r in fol if t == s]
    areas = [r.area for r in rs if r.area == r.area]
    an = collections.Counter(r.symbol for r in rs).most_common(3)
    st = collections.Counter(r.site for r in rs).most_common(3)
    ty = collections.Counter(r.type for r in rs).most_common(2)
    pre = collections.Counter((r.r['name'][-1] if r.r['name'] else '-') for r in rs).most_common(3)
    rows.append(dict(sign=s, label=label(s), shape=(sh.get(s) or '')[:60], after_jar=k, texts_with_sign=tot_sign[s],
                     share_after_jar=round(k / tot_sign[s], 2), median_face_mm2=round(float(np.median(areas)), 0) if areas else '',
                     n_area=len(areas), animals=';'.join(f'{a}:{b}' for a, b in an), sites=';'.join(f'{a}:{b}' for a, b in st),
                     types=';'.join(f'{a}:{b}' for a, b in ty), name_last_sign=';'.join(f'{a}:{b}' for a, b in pre)))
A1 = pd.DataFrame(rows); A1.to_csv(f'{OUT}/after_jar_signs.csv', index=False)
p(A1.head(16).to_string())
# pairs after jar
pr = collections.Counter()
for _, r in Cd.iterrows():
    x = r.tok
    for i, s in enumerate(x):
        if s == '740' and i + 2 < len(x): pr[(x[i + 1], x[i + 2])] += 1
p('pairs after jar', pr.most_common(15))
# jar then end vs follower, by object type
# ---------- A2 size
S = Cd[(Cd.type.str.startswith('SEAL'))].copy()
def cls(r):
    j = r.r['jars']
    if not j: return None
    x = r.tok
    if len(x) == j[-1] + 1: return 'of X (jar last)'
    if x[j[-1] + 1] == '090': return "X's man (jar 090)"
    if x[j[-1] + 1] == '400': return 'jar comb'
    if x[j[-1] + 1] == '679': return 'jar 679'
    if x[j[-1] + 1] == '001': return 'jar stroke'
    return 'jar other'
S['cls'] = S.apply(cls, axis=1)
S = S[S.cls.notna()]
p('\nsize by form (distinct site+text, seals with a measured face)')
sz = S.groupby('cls').agg(n=('area', 'size'), n_area=('area', lambda a: a.notna().sum()), median=('area', 'median'), q1=('area', lambda a: a.quantile(.25)), q3=('area', lambda a: a.quantile(.75)), meanlen=('tok', lambda t: np.mean([len(x) for x in t])))
p(sz.round(1).to_string())
a = S[S.cls == 'of X (jar last)'].area.dropna(); b = S[S.cls == "X's man (jar 090)"].area.dropna()
u = stats.mannwhitneyu(b, a, alternative='two-sided'); p('man vs owner area: median', b.median(), a.median(), 'n', len(b), len(a), 'MWU p', u.pvalue)
# shape: square vs round, and per side length
S['side'] = np.sqrt(S.area)
for nm, f in [('square seals', S.type == 'SEAL:S'), ('Mohenjo-daro', S.site == 'Mohenjo-daro'), ('Harappa', S.site == 'Harappa')]:
    a = S[f & (S.cls == 'of X (jar last)')].area.dropna(); b = S[f & (S.cls == "X's man (jar 090)")].area.dropna()
    if len(a) > 3 and len(b) > 3: p(nm, 'man median', round(b.median(), 0), len(b), 'owner median', round(a.median(), 0), len(a), 'MWU p', round(stats.mannwhitneyu(b, a).pvalue, 4))
# control for name length: same name length 1-3 only
for L in (1, 2, 3):
    a = S[(S.cls == 'of X (jar last)') & (S.r.map(lambda r: len(r['name'])) == L)].area.dropna(); b = S[(S.cls == "X's man (jar 090)") & (S.r.map(lambda r: len(r['name'])) == L)].area.dropna()
    if len(a) > 3 and len(b) > 3: p('name length', L, 'man', round(b.median(), 0), len(b), 'owner', round(a.median(), 0), len(a), 'p', round(stats.mannwhitneyu(b, a).pvalue, 4))
# other closers on size (no jar)
def endcls(r):
    x = r.tok; R = r.r
    if R['jars']: return None
    if R['ending_kind'] == 'ending': return {'520': 'spear', '090': 'man (no jar)', '400': 'comb (no jar)'}.get(x[-1], 'carrier' if x[-1] in ('151', '154', '155', '156', '158') else 'other')
S2 = Cd[Cd.type.str.startswith('SEAL')].copy(); S2['c2'] = S2.apply(endcls, axis=1)
p(S2[S2.c2.notna()].groupby('c2').area.agg(['size', 'median']).round(0).to_string())
# ---------- A3 master / servant pairs
def key_name(r): return tuple(r.r['name']) if r.r['name'] else None
rows_all = []
for _, r in C.iterrows():
    j = r.r['jars']
    if not j: continue
    x = r.tok; rel = r.r['relation']
    nm = key_name(r)
    if nm is None or any(s in ('000', 'ALT') for s in nm): continue
    kind = 'owner' if len(x) == j[-1] + 1 else ('servant' if rel and rel.startswith('090') else 'other-rel:' + (rel or ''))
    rows_all.append(dict(kind=kind, name=nm, cisi=r['cisi'], id=r['id'], obj=r.obj, site=r.site, house=r.house, zone=r['area-section'], text=r.text_s, type=r.type, area=r.area, sym=r.symbol))
T = pd.DataFrame(rows_all)
T.to_csv(f'{OUT}/jar_texts.csv', index=False)
p('\nname-bearing jar texts', len(T), T.kind.value_counts().to_dict())
def sameplace(a, b):
    if a.site != b.site: return 'other site'
    if a.house == b.house and a.house.split(' / ')[2] not in ('--', '', '-'): return 'same house'
    if a.zone == b.zone and a.zone not in ('--', ''): return 'same area'
    return 'same site'
owners = T[T.kind == 'owner']; servants = T[T.kind == 'servant']
by_name = collections.defaultdict(list)
for _, r in owners.iterrows(): by_name[r['name']].append(r)
pairs = []
for _, s in servants.iterrows():
    for o in by_name.get(s['name'], []):
        if o.text == s.text.split('-740')[0] + '-740' or True:
            pairs.append(dict(level='exact', name='-'.join(s['name']), servant_cisi=s.cisi, servant_site=s.site, servant_house=s.house, servant_text=s.text,
                              owner_cisi=o.cisi, owner_site=o.site, owner_house=o.house, owner_text=o.text, place=sameplace(s, o)))
Pp = pd.DataFrame(pairs)
# looser: last two signs of name equal (self + tag), name length >= 2, excluding exact
by2 = collections.defaultdict(list)
for _, r in owners.iterrows():
    if len(r['name']) >= 2: by2[r['name'][-2:]].append(r)
pairs2 = []
for _, s in servants.iterrows():
    if len(s['name']) < 2: continue
    for o in by2.get(s['name'][-2:], []):
        if o['name'] != s['name']:
            pairs2.append(dict(level='last-two-signs', name='-'.join(s['name']), servant_cisi=s.cisi, servant_site=s.site, servant_house=s.house, servant_text=s.text,
                               owner_cisi=o.cisi, owner_site=o.site, owner_house=o.house, owner_text=o.text, place=sameplace(s, o)))
Pp2 = pd.DataFrame(pairs2)
allp = pd.concat([Pp, Pp2]); allp.to_csv(f'{OUT}/master_servant_pairs.csv', index=False)
p('servants (named, complete)', len(servants), 'owners', len(owners))
p('exact-name pairs', len(Pp), 'distinct servants matched', Pp.servant_cisi.nunique() if len(Pp) else 0, 'place', Pp.place.value_counts().to_dict() if len(Pp) else {})
p('last-two pairs', len(Pp2), 'place', Pp2.place.value_counts().to_dict() if len(Pp2) else {})
# baseline: owners matched to other owners, same exact-name rate; servants matched to other servants
def rate(src, pool):
    hit = 0; hit_same = 0
    cnt = collections.defaultdict(list)
    for _, r in pool.iterrows(): cnt[r['name']].append(r)
    for _, s in src.iterrows():
        m = [o for o in cnt.get(s['name'], []) if o.text != s.text and not (o.site == s.site and o.cisi == s.cisi)]
        if m: hit += 1
        if any(o.site == s.site for o in m): hit_same += 1
    return hit, hit_same, len(src)
p('servant name also an owner seal elsewhere (any site, same site, n):', rate(servants, owners))
p('owner name also on another owner seal (any, same site, n):', rate(owners, owners))
p('servant name also on another servant seal:', rate(servants, servants))
# multi-sign names only (single-sign names repeat by chance)
ms = servants[servants.name.map(len) >= 2]; mo = owners[owners.name.map(len) >= 2]
p('multi-sign: servant->owner', rate(ms, mo), 'owner->owner', rate(mo, mo))
# randomized baseline: shuffle names among owners, test same-site exact match
rng = np.random.default_rng(3)
nm = list(owners['name'])
def cnt_hits(names_src, srcs, pool_names, pool_sites):
    ps = collections.defaultdict(set)
    for n_, s_ in zip(pool_names, pool_sites): ps[n_].add(s_)
    return sum(1 for n_, s_ in zip(names_src, srcs) if s_ in ps.get(n_, ()))
real = cnt_hits(list(servants.name), list(servants.site), nm, list(owners.site))
null = []
for _ in range(300):
    sh_names = rng.permutation(list(map(str, owners.name)))
    ow_sites = list(owners.site)
    ps = collections.defaultdict(set)
    for n_, s_ in zip(sh_names, ow_sites): ps[n_].add(s_)
    null.append(sum(1 for n_, s_ in zip(map(str, servants.name), servants.site) if s_ in ps.get(n_, ())))
p('same-site exact servant/owner matches real', real, 'null (owner names shuffled over owner sites) mean', round(np.mean(null), 1), 'max', max(null))
with open(f'{OUT}/report_numbers.txt', 'w') as f: f.write('\n'.join(P))
