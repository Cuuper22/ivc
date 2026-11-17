#!/usr/bin/env python3
"""HEADS 1: find every heading face by the fixed rule (see heads_common.py).  Predictions written 2026-11-17 BEFORE any number:
  P1. The rule returns 8 to 14 heading families, and the two big ones from chits.md (413-575-335-711 family; 413-892 family)
      are among them.  415-578-032-824 meets the rule only if it has 4 different partners.
  P2. Heading tablets are moulded more often than other Harappa tablets (54% of Harappa tablets are moulded), because a standing
      office repeats its line: moulded share of heading tablets >= 65%, tested against random draws of the same number of
      tablets from the same trenches.
  P3. Each heading stands in 3 or more trenches and in both mound E-type (E, ET) and mound F.
  P4. Heading partner diversity (distinct partners / objects) is NOT lower than chance: partner faces dealt at random among
      heading objects give the same ratio.  A name face is the opposite (it keeps its amount, so it has FEWER distinct partners).
      Control: the same ratio for repeated name-without-jar faces, against the same shuffle.
  P5. Headings sit in every time bin.
Outputs: work_data/heads/h1_headings.csv (one row per heading), h1_objects.csv (one row per heading-bearing tablet), h1_log.txt.
Run: python3 heads_1_find.py  (under a minute)
"""
from heads_common import *
say = log_to(f'{HOUT}/h1_log.txt')
rng = np.random.default_rng(1117)
H = harappa_stones()
say(f'Harappa stones {len(H)}; with 2+ faces {int((H.nfaces >= 2).sum())}; distinct issues {H.issue.nunique()}')
T = H[H.nfaces >= 2]

# ---- candidate face occurrences
occ = []   # (obj, face index, face string, stem, partners list)
for o, r in T.iterrows():
    fs = [face_str(f) for f in r.faces]
    for i, f in enumerate(r.faces):
        if r.types[i] in ('amount', 'lost') or r.jars[i] is not None or '000' in f: continue
        partners = [fs[j] for j in range(len(fs)) if j != i]
        keys = [pkey(r.faces[j], r.types[j]) for j in range(len(fs)) if j != i]
        roles = [partner_role(r.faces[j], r.types[j], r.jars[j]) for j in range(len(fs)) if j != i]
        occ.append(dict(obj=o, k=i, face=fs[i], stem=stem_of(f), partners=partners, keys=keys, roles=roles, complete=['000' not in p for p in partners]))
OC = pd.DataFrame(occ)
say(f'candidate face occurrences (not amount, not lost, no jar, no lost sign): {len(OC)} on {OC.obj.nunique()} tablets, {OC.face.nunique()} distinct strings')

def distinct_partners(sub):
    s = set()
    for ps, cm in zip(sub['keys'], sub.complete):
        for p, c in zip(ps, cm):
            if c: s.add(p)
    return s

def raw_partners(sub):
    s = set()
    for ps, cm in zip(sub.partners, sub.complete):
        for p, c in zip(ps, cm):
            if c: s.add(p)
    return s

# ---- tier A: exact string
A = {f: distinct_partners(g) for f, g in OC.groupby('face')}
tierA = sorted([f for f, p in A.items() if len(p) >= 4], key=lambda f: -len(OC[OC.face == f]))
say(f'TIER A (exact string, >= 4 different partners): {len(tierA)}: ' + ', '.join(tierA))

# ---- tier B: family (stem)
OC['family'] = OC.stem
B = {fam: g for fam, g in OC.groupby('family')}
tierB = {fam: g for fam, g in B.items() if len(distinct_partners(g)) >= 4}
say(f'TIER B (family, >= 4 different partners): {len(tierB)}')

# ---- object-level info
rows = []
for fam, g in tierB.items():
    for _, x in g.iterrows():
        r = H.loc[x.obj]
        rows.append(dict(family=fam, face=x.face, obj=x.obj, cisi=r.cisi, trench=r.trench, mound=r.mound, bin=r.bin or 'undated', time=r.time,
                         moulded=r.moulded, nfaces=r.nfaces, issue=r.issue, partners=' / '.join(x.partners), roles=','.join(x.roles)))
HO = pd.DataFrame(rows)
# one row per heading-bearing tablet per family (a tablet with two headings in one family counts once)
HO = HO.drop_duplicates(['family', 'obj'])
HO.to_csv(f'{HOUT}/h1_objects.csv', index=False)

tab = []
for fam, g in HO.groupby('family'):
    allp = distinct_partners(B[fam])
    iss = g.issue.nunique()
    shape = ' '.join(V2.get(s, 'PERSONAL') for s in fam.split('-'))
    rl = collections.Counter(x for r in g.roles for x in r.split(','))
    njar = sum(v for k, v in rl.items() if k.startswith('jar') or k in ('comb', 'man', 'other title', 'name no jar'))
    kind = 'office line' if njar >= 0.5 * sum(rl.values()) else 'side face'
    tab.append(dict(family=fam, kind=kind, partner_roles='; '.join(f'{k} {v}' for k, v in rl.most_common()), faces=' ; '.join(sorted(set(g.face))), pictures=' | '.join(pic(s) for s in fam.split('-')[:6]), v2_shape=shape,
                    objects=len(g), issues=iss, partners=len(allp), partner_strings=len(raw_partners(B[fam])), trenches=g.trench.nunique(), trench_list='; '.join(f'{k} {v}' for k, v in g.trench.value_counts().items()),
                    mounds='; '.join(f'{k} {v}' for k, v in g.mound.value_counts().items()),
                    bins='; '.join(f'{k} {v}' for k, v in g.bin.value_counts().items()),
                    moulded=int((g.moulded == 'moulded').sum()), incised=int((g.moulded == 'incised').sum()),
                    tierA=int(any(f in tierA for f in set(g.face)))))
HT = pd.DataFrame(tab).sort_values('objects', ascending=False)
HT.to_csv(f'{HOUT}/h1_headings.csv', index=False)
say(f'\nHEADING FAMILIES: {len(HT)} on {HO.obj.nunique()} tablets ({HO.issue.nunique()} issues)')
for _, r in HT.iterrows():
    say(f'  [{r.family}] faces {r.faces}\n      kind {r.kind} ({r.partner_roles}); shape {r.v2_shape}; objects {r.objects}, issues {r.issues}, partners {r.partners} (raw strings {r.partner_strings}), trenches {r.trenches} ({r.trench_list}); mounds {r.mounds}; bins {r.bins}; moulded {r.moulded} incised {r.incised}')

# ---- controls
Hm = T[T.moulded != ''] 
base_m = (Hm.moulded == 'moulded').mean()
HOu = HO.drop_duplicates('obj'); nh = len(HOu); mh = int((HOu.moulded == 'moulded').sum())
say(f'\nP2 moulded share: heading tablets {mh}/{nh} = {mh / nh:.3f}; all Harappa 2+-face tablets {base_m:.3f}')
# null: draw nh tablets from the same trenches in the same proportions
tr_counts = HOu.trench.value_counts()
pool = {t: Hm[Hm.trench == t].moulded.eq('moulded').values for t in tr_counts.index}
pool_all = {t: Hm[Hm.trench == t].moulded.eq('moulded').values for t in Hm.trench.unique()}
nul = []
for _ in range(4000):
    s = 0
    for t, n in tr_counts.items():
        p = pool.get(t, np.array([False]))
        s += rng.choice(p, size=n, replace=True).sum()
    nul.append(s)
nul = np.array(nul)
say(f'  same trenches, same number: chance {nul.mean():.1f} moulded of {nh}; P(real >= chance) {pvalue_hi(nul, mh):.4f}; P(real <= chance) {pvalue_lo(nul, mh):.4f}')
# per issue (copy events) too
HI = HOu.drop_duplicates('issue'); ni = len(HI); mi = int((HI.moulded == 'moulded').sum())
say(f'  counting issues once: moulded {mi}/{ni} = {mi / ni:.3f}')

# P4 diversity: distinct partners / objects vs shuffle of partner faces among all two-face tablets
say('\nP4 partner diversity: distinct partners per object, real vs partner faces dealt at random (4000 deals) among all 2-face Harappa tablets')
two = T[T.nfaces == 2]
def diversity_test(label, faces_list, repeats_min=5):
    # for each repeated face string with >= repeats_min tablets: real distinct partners (complete) vs null
    res = []
    D = OC[OC.face.isin(faces_list)]
    allp = [p for ps in two.faces for p in [face_str(f) for f in ps]]
    for f in faces_list:
        g = D[(D.face == f) & (D.partners.map(len) == 1)]
        if len(g) < repeats_min: continue
        real = len({p[0] for p in g.partners})
        nl = [len({rng.choice(allp) for _ in range(len(g))}) for _ in range(1500)]
        res.append((f, len(g), real, float(np.mean(nl)), pvalue_lo(nl, real)))
    return res
heads_faces = sorted(set(HO.face))
for f, n, real, nl, p in diversity_test('heads', heads_faces, 5):
    say(f'  heading face {f:32s} tablets {n:3d} distinct partners {real:3d} chance {nl:5.1f} (P fewer {p:.3f})')
# control: every repeated face on 2-face tablets that is NOT a heading: names with a jar (they keep their amount) and amount faces
allocc = collections.defaultdict(list)
for o, r in two.iterrows():
    fs = [face_str(f) for f in r.faces]
    for i in (0, 1):
        allocc[fs[i]].append(fs[1 - i])
allp = [p for ps in two.faces for p in [face_str(f) for f in ps]]
jarfaces = {face_str(f) for ps, js in zip(two.faces, two.jars) for f, j in zip(ps, js) if j is not None}
amt = {face_str(f) for ps, ts in zip(two.faces, two.types) for f, t in zip(ps, ts) if t == 'amount'}
for label, S in (('jar-name faces', jarfaces), ('amount faces', amt)):
    tr = tn = 0; k = 0; below = 0
    for f, ps in allocc.items():
        if f not in S or len(ps) < 8 or '000' in f: continue
        real = len(set(ps)); nl = [len({rng.choice(allp) for _ in range(len(ps))}) for _ in range(600)]
        tr += real; tn += float(np.mean(nl)); k += 1; below += pvalue_lo(nl, real) <= 0.05
    say(f'  control {label}: {k} repeated faces (8+ tablets): distinct partners {tr} against chance {tn:.1f}; {below} of {k} individually below chance at P <= 0.05')

# per-family moulded test (trench-matched deal) and near misses
say('\nper heading family: moulded count against tablets of the same trenches (4000 deals)')
for fam, g in HO.groupby('family'):
    g = g.drop_duplicates('obj'); n = len(g); m = int((g.moulded == 'moulded').sum()); trc = g.trench.value_counts(); nl = []
    for _ in range(4000):
        t = 0
        for tn, c in trc.items():
            p_ = pool_all.get(tn, np.array([False])); t += rng.choice(p_, size=c, replace=True).sum()
        nl.append(t)
    nl = np.array(nl)
    say(f'  {fam:18s} moulded {m} of {n}; chance {nl.mean():.1f}; P(more) {pvalue_hi(nl, m):.4f}; P(fewer) {pvalue_lo(nl, m):.4f}')
say('\nnear misses: families with exactly 3 different partners (not headings by the rule)')
for fam, g in B.items():
    if len(distinct_partners(g)) == 3:
        say(f'  [{fam}] tablets {g.obj.nunique()} partners {sorted(distinct_partners(g))}')
say('done')
