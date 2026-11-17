#!/usr/bin/env python3
"""SPOTS, lead 3: multi-face objects (tablets) as records.  Uses work_data/odd/object_records.csv (902 objects, 2+ faces).

Plain words:
- FACE TYPE, from the face's own signs and parser jobs, no word values:
    name   = the face has a name job (crest / owner ending / opener / tag, e.g. 176-740-400)
    amount = the face is only count signs, measure signs (cup 700, big measure 705/706, ...) and lost signs, with a count or cup
    thing  = a face with word-signs that is neither (a counted-thing or picture-like face, e.g. 416-861-002, 615)
    lost   = every sign broken
- RECORD KIND = the face types of the object, sorted (name+amount, amount+amount, name+thing ...).
- SIGNATURE of an object = its faces, each as a sign string, sorted (copies of one tablet differ in which face is first).
- BATCH = 5+ objects with one signature (no lost signs in it) found at one site in one excavation area (trench).
- CUP COUNT = value of the number run right in front of the cup 700; BIG-MEASURE COUNT likewise for 705/706.
PREDICTIONS (written before any number below was computed):
 (a) name+amount is the main record kind (more than half of the objects with a readable type), amount+amount second;
     most at Harappa trenches E11, F-I.
 (b) Batches of identical tablets: batches within one trench share the NAME face while the AMOUNT changes more often than
     they share the amount while the name changes (an account: one holder, different quantities).
 (c) The same name face turns up with different amount faces at different depths or trenches more often than two random
     name+amount records of the same site differ in amount (an account running over time).
 (d) Cups never 5 and never above 6 on any record; records with both cups and the big measure keep to the ceiling.
Writes work_data/spots/s3_*.csv and s3_log.txt.  Run: python3 spots_3_records.py (about 1 min)
"""
import sys, os, io, contextlib, collections, random, re, itertools
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
random.seed(303); np.random.seed(303)
with contextlib.redirect_stdout(io.StringIO()):
    from measures_common import objs, NUM, UNITS, runs, ROOT
OUT = f'{ROOT}/work_data/spots'; os.makedirs(OUT, exist_ok=True)
LOG = open(f'{OUT}/s3_log.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n')
R = pd.read_csv(f'{ROOT}/work_data/odd/object_records.csv', dtype=str).fillna('')
NAMEJOB = {'crest', 'poss', 'ending', 'opener', 'tag'}
def face_type(f, roles):
    t = list(f)
    if all(s == '000' for s in t): return 'lost'
    if NAMEJOB & set(roles): return 'name'
    core = [s for s in t if s != '000']
    if all((s in NUM or s in UNITS) for s in core) and any((s in NUM or s == '700') for s in core): return 'amount'
    return 'thing'
rows = []
for _, r in R.iterrows():
    o = objs.loc[r.object_id]
    faces = [tuple(f) for f in o.faces]; roles = [p['roles'] for p in o.parses]
    types = [face_type(f, ro) for f, ro in zip(faces, roles)]
    lostfree = all('000' not in f for f in faces)
    sig = ' | '.join(sorted('-'.join(f) for f in faces))
    area = o.area if o.area not in ('--', '') else ''
    dm = re.search(r'(-?\d+(\.\d+)?)\s*(ft|m)\b', str(o.depth)); depth = None
    if dm:
        depth = abs(float(dm.group(1))) * (3.281 if dm.group(3) == 'm' else 1)
        if depth == 0: depth = None
    rows.append(dict(obj=r.object_id, site=r.site, type=o.type, kind_obj=r.object_kind, area=area, bh=o.bh, depth_ft=depth, nfaces=len(faces),
                     types='+'.join(sorted(types)), faces='|'.join('-'.join(f) for f in faces), sig=sig, lostfree=lostfree,
                     name_face='|'.join(sorted('-'.join(f) for f, t in zip(faces, types) if t == 'name')),
                     amt_face='|'.join(sorted('-'.join(f) for f, t in zip(faces, types) if t == 'amount')),
                     thing_face='|'.join(sorted('-'.join(f) for f, t in zip(faces, types) if t == 'thing')), grade=r.grade))
O = pd.DataFrame(rows); O.to_csv(f'{OUT}/s3_objects.csv', index=False)

# ---------------- (a) kinds ----------------
say('(a) What kinds of record are there?  (902 multi-face objects)')
K = O.types.value_counts()
say('  kinds, all sites:', '; '.join(f'{k} {v}' for k, v in K.head(12).items()))
readable = O[~O.types.str.contains('lost')]
say(f'  with no wholly-lost face: {len(readable)}; kinds:', '; '.join(f'{k} {v}' for k, v in readable.types.value_counts().head(8).items()))
two = O[O.nfaces == 2]
say(f'  two-face objects {len(two)}: ' + '; '.join(f'{k} {v} ({v / len(two):.0%})' for k, v in two.types.value_counts().head(8).items()))
by_site = pd.crosstab(O.site, O.types); by_site.to_csv(f'{OUT}/s3_a_kind_by_site.csv')
say('  by site (top kinds):')
for s in by_site.index:
    row = by_site.loc[s]; row = row[row > 0].sort_values(ascending=False)
    say(f'     {s:14s} {int(row.sum()):4d}  ' + '; '.join(f'{k} {v}' for k, v in row.head(5).items()))
Ot = O.copy(); Ot['trench'] = Ot.site + '|' + Ot.area.where(Ot.area != '', '(no area)')
by_tr = pd.crosstab(Ot.trench, Ot.types); by_tr['total'] = by_tr.sum(axis=1); by_tr = by_tr.sort_values('total', ascending=False)
by_tr.to_csv(f'{OUT}/s3_a_kind_by_trench.csv')
say('  by trench (top 14 by objects; main kinds):')
for t in by_tr.index[:14]:
    row = by_tr.loc[t].drop('total'); row = row[row > 0].sort_values(ascending=False)
    say(f'     {t:34s} {int(by_tr.loc[t, "total"]):4d}  ' + '; '.join(f'{k} {v}' for k, v in row.head(4).items()))
# object type: moulded vs incised
say('  by object format (TAB:B moulded miniature, TAB:I incised miniature, TAB:C copper):', '; '.join(f'{t}: ' + ', '.join(f'{k} {v}' for k, v in O[O.type == t].types.value_counts().head(3).items()) for t in ('TAB:B', 'TAB:I', 'TAB:C')))

# ---------------- (b) batches ----------------
say('\n(b) Batches: 5+ identical tablets (same faces, no lost sign) in one site + trench')
Ob = O[O.lostfree & (O.area != '')].copy()
Ob['place'] = Ob.site + '|' + Ob.area
g = Ob.groupby(['place', 'sig'])
B = g.agg(copies=('obj', 'size'), types=('types', 'first'), name_face=('name_face', 'first'), amt_face=('amt_face', 'first'),
          thing_face=('thing_face', 'first'), formats=('type', lambda s: ','.join(sorted(set(s)))),
          depth_min=('depth_ft', 'min'), depth_max=('depth_ft', 'max'), objs=('obj', lambda s: ' '.join(s))).reset_index()
B5 = B[B.copies >= 5].sort_values('copies', ascending=False)
B.to_csv(f'{OUT}/s3_b_all_signatures.csv', index=False); B5.to_csv(f'{OUT}/s3_b_batches5.csv', index=False)
say(f'  batches of 5+: {len(B5)}, holding {int(B5.copies.sum())} objects; of 3+: {(B.copies >= 3).sum()}')
for _, b in B5.iterrows():
    say(f'     {b.place:30s} x{b.copies:3d} {b.types:14s} {b.sig:50s} formats {b.formats}')
# pairs of batches in one trench
def rel(b1, b2):
    ns = b1.name_face == b2.name_face and b1.name_face != ''; as_ = b1.amt_face == b2.amt_face and b1.amt_face != ''
    ts = b1.thing_face == b2.thing_face and b1.thing_face != ''
    return ns, as_, ts
say('\n  pairs of DIFFERENT signatures inside one trench (3+ copies each, name+amount records): share the name, share the amount, share both-or-neither')
def pair_table(Bset, label):
    Bn = Bset[(Bset.types == 'amount+name') & (Bset.name_face != '') & (Bset.amt_face != '')].reset_index(drop=True)
    nm_ = pd.factorize(Bn.name_face)[0]; am_ = pd.factorize(Bn.amt_face)[0]
    site_ = pd.factorize(Bn.place.str.split('|').str[0])[0]; pl_ = pd.factorize(Bn.place)[0]
    n = len(Bn)
    NS = (nm_[:, None] == nm_[None, :]); AS = (am_[:, None] == am_[None, :]); iu = np.triu_indices(n, 1)
    kinds = {'name_same_amount_differs': NS & ~AS, 'amount_same_name_differs': AS & ~NS, 'neither': ~NS & ~AS}
    def counts(pl):
        same = (pl[:, None] == pl[None, :])[iu]
        return {k: int((m[iu] & same).sum()) for k, m in kinds.items()}
    obs = counts(pl_); nul = {k: [] for k in kinds}
    rng = np.random.default_rng(3)
    for t in range(3000):
        p2 = pl_.copy()
        for s_ in np.unique(site_):
            ix = np.where(site_ == s_)[0]; p2[ix] = rng.permutation(pl_[ix])
        c = counts(p2)
        for k in kinds: nul[k].append(c[k])
    say(f'  {label}: {n} name+amount signatures in {Bn.place.nunique()} trenches')
    for k in kinds:
        a = np.array(nul[k]); say(f'     {k:26s} {obs[k]:4d} pairs in one trench; trench labels shuffled within site: {a.mean():.1f}  (P high {(1 + (a >= obs[k]).sum()) / 3001:.4f}, P low {(1 + (a <= obs[k]).sum()) / 3001:.4f})')
    return Bn
pair_table(B[B.copies >= 5], 'batches of 5+')
pair_table(B[B.copies >= 3], 'batches of 3+')
pair_table(B, 'every signature (1+ copies)')

# ---------------- (c) accounts over time ----------------
say('\n(c) Same name face with different amount faces: an account running over time?')
N = O[(O.types == 'amount+name') & O.lostfree & (O.name_face != '') & (O.amt_face != '')].copy()
N['place'] = N.site + '|' + N.area.where(N.area != '', '(no area)')
say(f'  name+amount records with no lost sign: {len(N)}; distinct name faces {N.name_face.nunique()}')
nm = N.groupby('name_face')
multi = [(n, g) for n, g in nm if len(g) >= 2]
say(f'  name faces on 2+ records: {len(multi)}; with 2+ different amounts: {sum(g.amt_face.nunique() >= 2 for _, g in multi)}')
# pair statistic: for pairs of records with the same name, how often the amounts differ; baseline = random pairs of records, same site
def pairs_same_name(df):
    same = diff = 0
    for n, g in df.groupby('name_face'):
        a = list(g.amt_face)
        for i in range(len(a)):
            for j in range(i + 1, len(a)):
                if a[i] == a[j]: same += 1
                else: diff += 1
    return same, diff
s0, d0 = pairs_same_name(N)
# shuffle amounts among records of the same site (name stays)
nl = []
for t in range(1000):
    X = N.copy()
    for s, ix in X.groupby('site').groups.items():
        X.loc[ix, 'amt_face'] = list(X.loc[ix, 'amt_face'].sample(frac=1, random_state=int(np.random.randint(1e9))))
    nl.append(pairs_same_name(X)[0])
nl = np.array(nl)
say(f'  pairs with one name: amount identical {s0}, amount differs {d0}; amounts shuffled within site gives identical {nl.mean():.1f} (P high {(1 + (nl >= s0).sum()) / 1001:.4f}: small P = a name keeps ITS amount more than chance)')
# depth / trench structure among same-name pairs
rowsc = []
for n, g in multi:
    for (i, a), (j, b) in itertools.combinations(list(g.iterrows()), 2):
        if a.amt_face == b.amt_face and a.sig == b.sig: kind = 'identical copy'
        else: kind = 'amount differs' if a.amt_face != b.amt_face else 'same'
        dd = abs(a.depth_ft - b.depth_ft) if pd.notna(a.depth_ft) and pd.notna(b.depth_ft) else np.nan
        rowsc.append(dict(name=n, a=a.obj, b=b.obj, same_trench=a.place == b.place, amt_a=a.amt_face, amt_b=b.amt_face, kind=kind, dd=dd, site_a=a.site, site_b=b.site))
C = pd.DataFrame(rowsc); C.to_csv(f'{OUT}/s3_c_same_name_pairs.csv', index=False)
Cd = C[C.kind == 'amount differs']
say(f'  same-name pairs {len(C)}: different amount {len(Cd)}, same amount {len(C) - len(Cd)}; of the differing pairs {int(Cd.same_trench.sum())} are in the same trench, {int((~Cd.same_trench).sum())} in different trenches/sites; with both depths known {int(Cd.dd.notna().sum())}, median depth gap {Cd.dd.median():.1f} ft')
say('  name faces with several amounts (all records, sorted by number of distinct amounts):')
for n, g in sorted(multi, key=lambda x: -x[1].amt_face.nunique())[:14]:
    if g.amt_face.nunique() < 2: break
    say(f'     {n:30s} {len(g)} records, {g.amt_face.nunique()} amounts [{"; ".join(f"{k} x{v}" for k, v in g.amt_face.value_counts().items())}] in {g.place.nunique()} trenches, depths {sorted(g.depth_ft.dropna().round(1).tolist())}')
# depth test: within the same name AND trench, do amounts change with depth?
rowsd = []
for n, g in multi:
    for pl, gg in g.groupby('place'):
        gg = gg[gg.depth_ft.notna()]
        if len(gg) >= 2 and gg.amt_face.nunique() >= 2:
            rowsd.append((n, pl, [(round(r.depth_ft, 1), r.amt_face) for _, r in gg.sort_values('depth_ft').iterrows()]))
say(f'  name + trench groups where the amount changes and depths are known: {len(rowsd)}')
for n, pl, lst in rowsd[:12]: say(f'     {n:28s} {pl:28s} {lst}')

# ---------------- (d) measures ----------------
say('\n(d) Cups and the big measure (12 cups = 1 big measure, 705/706): ceiling check')
def unit_counts(tok, unit_set):
    out = []
    for (a, b, v, ser) in runs(list(tok)):
        if b < len(tok) and tok[b] in unit_set and v is not None: out.append(v)
    return out
rec = []
for _, r in O.iterrows():
    o = objs.loc[r.obj]; cups = []; big = []
    for f in o.faces:
        cups += unit_counts(f, {'700'}); big += unit_counts(f, {'705', '706'})
    rec.append(dict(obj=r.obj, site=r.site, cups=cups, big=big, sig=r.sig))
Rr = pd.DataFrame(rec)
cupvals = collections.Counter(v for c in Rr.cups for v in c)
say('  cup counts on the 902 records (count run right before 700):', dict(sorted(cupvals.items())))
bad = Rr[Rr.cups.map(lambda c: any(v == 5 or v > 6 for v in c))]
say(f'  records breaking the cup rule (a count of 5, or above 6): {len(bad)}')
for _, r in bad.iterrows(): say(f'     object {r.obj} {r.site}: cups {r.cups}  {r.sig}')
both = Rr[(Rr.cups.map(len) > 0) & (Rr.big.map(len) > 0)]
say(f'  records with both a cup count and a big-measure count: {len(both)}')
for _, r in both.iterrows(): say(f'     object {r.obj} {r.site}: cups {r.cups}, big {r.big}  {r.sig}')
# also run over every object in the catalogue (ceiling is the same claim, wider)
allc = collections.Counter(); badall = []
for o_, o in objs.iterrows():
    for f in o.faces:
        for v in unit_counts(f, {'700'}):
            allc[v] += 1
            if v == 5 or v > 6: badall.append((o_, o.site, '-'.join(f)))
say('  all objects in the catalogue, cup counts:', dict(sorted(allc.items())), f'; breaking the rule: {len(badall)}')
for b in badall[:20]: say('     ', b)
# cup + big on one FACE or one object anywhere, with the number runs
both_all = []
for o_, o in objs.iterrows():
    cs = []; bs = []
    for f in o.faces: cs += unit_counts(f, {'700'}); bs += unit_counts(f, {'705', '706'})
    if cs and bs: both_all.append((o_, o.site, cs, bs, [ '-'.join(f) for f in o.faces]))
say(f'  all objects with a cup count AND a big-measure count: {len(both_all)}')
for b in both_all[:25]: say('     ', b)
pd.DataFrame(rec).to_csv(f'{OUT}/s3_d_cups.csv', index=False)
LOG.close()
