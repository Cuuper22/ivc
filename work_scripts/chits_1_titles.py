#!/usr/bin/env python3
"""CHITS 1: the after-jar signs side by side (comb 400, man 090, and every other frame-v2 TITLE sign after the jar).

For each after-jar sign: objects by kind (seal, tablet, tag, pot ...), cities, seal size residual against jar-only
seals of the same site, length and format, crests before the jar, distinct names, and names that turn up with two
different after-jar endings (a person changing class, or two people of one house in different classes).
Control: after-jar labels shuffled among jar faces of the same site and object kind (2,000 shuffles).

PREDICTIONS (written before any number):
 P1 comb 400 lives on Harappa tablets and is the smallest seal class; man 090 lives on seals in many cities and is
    jar-only size or bigger.  Every other title is mostly seals at Mohenjo-daro.
 P2 Crests before comb are goods / count signs (box 590, tree, cup) and the seated person 176 more than before man;
    fish crests stand before man more than before comb.
 P3 Names shared between two endings are FEWER than shuffled for comb vs man (the two are different people), but a
    name shared between jar-only and comb is MORE than shuffled (the comb holder is a junior of a jar-only house).
Writes work_data/chits/c1_*.csv, c1_log.txt.  Run: python3 chits_1_titles.py
"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chits_common import *
LOG = open(f'{OUT}/c1_log.txt', 'w'); say = say_to(LOG)
say('loading objects ...')
O = load(); N = name_rows(O)
O.drop(columns=['faces', 'types', 'jars']).to_csv(f'{OUT}/objects.csv', index=False)
N.to_csv(f'{OUT}/jar_faces.csv', index=False)
say(f'objects {len(O)}, faces with a jar {len(N)}; after-jar signs:', fmt_counter(collections.Counter(N.after), 25))
SZ = seal_sizes()
N['res'] = N.obj.map(SZ.res)
# one row per object (an object with two jar faces counts once per ending)
NO = N.drop_duplicates(['obj', 'after'])
jar_only_res = NO[(NO.kind == 'seal') & (NO.after == '')].res.dropna()
say(f'jar-only seals with size {len(jar_only_res)}, mean residual {jar_only_res.mean():+.3f}')
rows = []
for t in ['', '400', '090'] + [s for s in TITLES if s not in ('400', '090')] + ['other']:
    sub = NO[NO.after == t] if t != 'other' else NO[NO.ending == 'other']
    if len(sub) == 0: continue
    k = collections.Counter(sub.kind); c = collections.Counter(sub.site)
    r = sub[sub.kind == 'seal'].res.dropna()
    names = sub[~sub.lost].name
    rows.append(dict(after=t or 'jar only', picture=pic(t) if t not in ('', 'other') else t or 'nothing', objects=len(sub),
                     seals=k['seal'], tablets=k['mtab'], copper=k['ctab'], tags=k['tag'], pots=k['pot'], rods=k['rod'], other=len(sub) - k['seal'] - k['mtab'] - k['ctab'] - k['tag'] - k['pot'] - k['rod'],
                     cities=len(c), Harappa=c['Harappa'], Mohenjo=c['Mohenjo-daro'], top_cities=fmt_counter(c, 4),
                     seals_sized=len(r), seal_res_mean=round(r.mean(), 3) if len(r) else np.nan,
                     seal_res_median=round(r.median(), 3) if len(r) else np.nan,
                     distinct_names=names.nunique(), top_crests=fmt_counter(collections.Counter(sub[~sub.lost].crest), 6),
                     bins=fmt_counter(collections.Counter(sub[sub.bin != ''].bin))))
TT = pd.DataFrame(rows); TT.to_csv(f'{OUT}/c1_titles.csv', index=False)
say('\nper after-jar sign:')
for _, r in TT.iterrows():
    say(f"  {r.after:8s} {r.picture[:22]:22s} obj {r.objects:4d} seal {r.seals:3d} tab {r.tablets:3d} cu {r.copper:2d} tag {r.tags:2d} pot {r.pots:2d} rod {r.rods:2d} | "
        f"cities {r.cities} ({r.top_cities}) | seal res {r.seal_res_mean} (n {r.seals_sized}) | names {r.distinct_names} | crests {r.top_crests} | bins {r.bins}")

# size test: comb seals vs jar-only, shuffle within site x format cell is already in the residual; permutation of labels
say('\nseal size against jar-only seals (residual already removes site, length, format); label shuffle P:')
rng = np.random.default_rng(11)
J = NO[(NO.kind == 'seal') & NO.res.notna()]
for t in ['400', '090', '527', '621', '679', '565', '161', '241']:
    a = J[J.after == t].res.values; b = J[J.after == ''].res.values
    if len(a) < 2: continue
    allv = np.concatenate([a, b]); obs = a.mean() - b.mean(); cnt = 0
    for _ in range(4000):
        p = rng.permutation(allv); d_ = p[:len(a)].mean() - p[len(a):].mean()
        cnt += (abs(d_) >= abs(obs))
    say(f'  {t}: n {len(a)}, mean {a.mean():+.3f} vs jar-only {b.mean():+.3f}, gap {obs:+.3f} (x{np.exp(obs):.2f} face), two-sided P {cnt / 4000:.4f}')

# crest groups before the jar, per ending
say('\ncrest kind before the jar, comb vs man vs jar-only (all objects, name not lost):')
FISH = {'220', '231', '233', '235', '240', '226', '222', '243'}
GOODS = {'590', '390', '405', '406', '407', '700', '440', '156', '705', '706', '335', '605'}
def ckind(c):
    if c in FISH: return 'fish'
    if c in GOODS: return 'goods/measure'
    if c == '176': return '176 seated person'
    if c in NUM: return 'number'
    return 'other'
CK = []
for t in ['', '400', '090']:
    sub = NO[(NO.after == t) & ~NO.lost]
    cc = collections.Counter(sub.crest.map(ckind))
    for k, v in cc.items(): CK.append(dict(after=t or 'jar only', crest_kind=k, n=v, share=round(v / len(sub), 3)))
    say(f'  {t or "jar only":8s} n {len(sub)}: ' + '; '.join(f'{k} {v} ({v / len(sub):.0%})' for k, v in cc.most_common()))
pd.DataFrame(CK).to_csv(f'{OUT}/c1_crest_kinds.csv', index=False)
# same within Harappa tablets only (object kind fixed)
for t in ['', '400', '090']:
    sub = NO[(NO.after == t) & ~NO.lost & (NO.site == 'Harappa') & (NO.kind == 'mtab')]
    cc = collections.Counter(sub.crest.map(ckind))
    say(f'  Harappa tablets {t or "jar only":8s} n {len(sub)}: ' + '; '.join(f'{k} {v} ({v / max(len(sub), 1):.0%})' for k, v in cc.most_common()))

# shared names across endings
say('\nnames carried with two different after-jar endings (jar only counts as an ending); shuffle within site x kind:')
NN = NO[~NO.lost & (NO.name != '')].reset_index(drop=True)
def shared(df):
    g = df.groupby('name').after.apply(set)
    out = collections.Counter()
    for s in g:
        s = sorted(s)
        for i in range(len(s)):
            for j in range(i + 1, len(s)): out[(s[i] or 'jar', s[j] or 'jar')] += 1
    return out
obs = shared(NN)
keys = [k for k, v in obs.most_common(12)] + [('090', '400')]
keys = list(dict.fromkeys(keys))
null = {k: [] for k in keys}
grp = NN.groupby(['site', 'kind']).indices
for it in range(2000):
    a = NN.after.values.copy()
    for g_, ix in grp.items(): a[ix] = rng.permutation(a[ix])
    s = shared(NN.assign(after=a))
    for k in keys: null[k].append(s.get(k, 0))
SH = []
for k in keys:
    nv = np.array(null[k]); o = obs.get(k, 0)
    SH.append(dict(pair=f'{k[0]}+{k[1]}', names_shared=o, shuffled_mean=round(nv.mean(), 2), P_high=round((nv >= o).mean(), 4), P_low=round((nv <= o).mean(), 4)))
    say(f'  {k[0]:4s} + {k[1]:4s}: {o} names against {nv.mean():.2f} shuffled (P high {(nv >= o).mean():.4f}, P low {(nv <= o).mean():.4f})')
pd.DataFrame(SH).to_csv(f'{OUT}/c1_shared_names.csv', index=False)
# list the comb names that also appear with man or jar-only
g = NN.groupby('name').agg(endings=('after', lambda s: ','.join(sorted({x or 'jar' for x in s}))), n=('obj', 'size'),
                            sites=('site', lambda s: ','.join(sorted(set(s)))), kinds=('kind', lambda s: ','.join(sorted(set(s)))),
                            cisi=('cisi', lambda s: ' '.join(list(s)[:8])))
gm = g[g.endings.str.contains(',') & g.endings.str.contains('400|090')]
gm.to_csv(f'{OUT}/c1_names_two_endings.csv')
say('\nnames with comb or man and another ending:')
for nm, r in gm.sort_values('n', ascending=False).iterrows():
    say(f'  {nm:28s} {r.endings:14s} n {r.n:3d} {r.sites:30s} {r.kinds:18s} {r.cisi}')
say('done')
