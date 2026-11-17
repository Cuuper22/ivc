#!/usr/bin/env python3
"""CHITS 2: names on the comb chits against names on seals.

CHIT NAME = the name (signs before the jar, front word / slot taken off, no lost sign) on a Harappa tablet ending 740-400.
For each: does the same name stand before a jar on a SEAL anywhere?  With which ending, what seal size?  Where is the
seal found against the trench of its tablets?
Controls: (a) names on Harappa tablets ending jar-only or other title, the same questions; (b) seal endings shuffled
among jar seals of the same site (4,000 shuffles) for "comb-ending seal more often than chance"; (c) seal trench
shuffled among Harappa seals with a trench for the findspot test.

PREDICTIONS (written before any number):
 Q1 roughly 60-100 distinct chit names; 10-25% of them on a seal anywhere (chits are for people who mostly had no seal).
 Q2 when a chit name has a seal, its seal ends in comb more than chance (the class is a property of the person and
    keeps across objects, as endings did in endings_A*.py), and the seal is small.
 Q3 the seal of a chit name lies in the same Harappa trench as its tablets more often than chance (the holder lived
    where his chits were issued or stored).
Writes work_data/chits/c2_*.csv, c2_log.txt.
"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chits_common import *
LOG = open(f'{OUT}/c2_log.txt', 'w'); say = say_to(LOG)
O = load(); N = name_rows(O)
SZ = seal_sizes(); N['res'] = N.obj.map(SZ.res)
rng = np.random.default_rng(22)
HT = N[(N.site == 'Harappa') & (N.kind == 'mtab') & ~N.lost & (N.name != '')]
SE = N[(N.kind == 'seal') & ~N.lost & (N.name != '')].drop_duplicates('obj')
say(f'Harappa tablet jar faces with a readable name {len(HT)}; seal jar faces {len(SE)}')
seal_by_name = SE.groupby('name')
sealnames = set(SE.name)

def profile(names, label):
    names = sorted(set(names))
    hit = [n for n in names if n in sealnames]
    S = SE[SE.name.isin(hit)]
    endc = collections.Counter(S.after.map(lambda x: x or 'jar only'))
    say(f'  {label}: {len(names)} distinct names; {len(hit)} on a seal ({len(hit) / max(len(names), 1):.0%}); seals {len(S)}; '
        f'seal endings {fmt_counter(endc)}; seal size residual mean {S.res.mean():+.3f} (n {S.res.notna().sum()})')
    return names, hit, S

say('\nQ1 / Q2: chit names and seals')
groups = {'comb chits 740-400': HT[HT.after == '400'], 'jar-only tablets': HT[HT.after == ''],
          'man tablets 740-090': HT[HT.after == '090'], 'other-title tablets': HT[~HT.after.isin(['', '400', '090'])]}
res = {}
for lab, g in groups.items(): res[lab] = profile(g.name, lab)
rows = []
for lab, (names, hit, S) in res.items():
    rows.append(dict(set=lab, distinct_names=len(names), with_seal=len(hit), seals=len(S), comb_seals=int((S.after == '400').sum()),
                     man_seals=int((S.after == '090').sum()), jar_only_seals=int((S.after == '').sum()), seal_res_mean=round(S.res.mean(), 3)))
pd.DataFrame(rows).to_csv(f'{OUT}/c2_sets.csv', index=False)

# shuffle: endings among jar seals of the same site
names, hit, S = res['comb chits 740-400']
obs = int((S.after == '400').sum())
SEi = SE.reset_index(drop=True); grp = SEi.groupby('site').indices; msk = SEi.name.isin(hit).values
nul = []
for _ in range(4000):
    a = SEi.after.values.copy()
    for g_, ix in grp.items(): a[ix] = rng.permutation(a[ix])
    nul.append(int((a[msk] == '400').sum()))
nul = np.array(nul)
say(f'  comb-ending seals among the seals of chit names: {obs} of {len(S)} against {nul.mean():.2f} with endings shuffled within site (P {(nul >= obs).mean():.4f})')
# same for the jar-only names: does a jar-only tablet name keep jar-only on its seals?
for lab in ('jar-only tablets', 'man tablets 740-090'):
    names2, hit2, S2 = res[lab]; tgt = '' if lab.startswith('jar') else '090'
    o2 = int((S2.after == tgt).sum()); msk2 = SEi.name.isin(hit2).values; n2 = []
    for _ in range(4000):
        a = SEi.after.values.copy()
        for g_, ix in grp.items(): a[ix] = rng.permutation(a[ix])
        n2.append(int((a[msk2] == tgt).sum()))
    n2 = np.array(n2)
    say(f'  {lab}: seals keeping the same ending {o2} of {len(S2)} against {n2.mean():.2f} (P {(n2 >= o2).mean():.4f})')

# Rate of having any seal: chit names vs jar-only names, matched by name length
say('\n  share of names with a seal, by name length (comb chit names / jar-only tablet names):')
cn = pd.Series(res['comb chits 740-400'][0]); jn = pd.Series(res['jar-only tablets'][0])
for L in (1, 2, 3, 4):
    a = cn[cn.str.count('-') + 1 == L]; b = jn[jn.str.count('-') + 1 == L]
    say(f'    length {L}: {a.isin(sealnames).sum()} of {len(a)} against {b.isin(sealnames).sum()} of {len(b)}')

# per-name table
T = []
CH = HT[HT.after == '400']
for nm, g in CH.groupby('name'):
    s = SE[SE.name == nm]
    T.append(dict(name=nm, pictures=' + '.join(pic(x) for x in nm.split('-')), chit_tablets=g.obj.nunique(),
                  trenches=fmt_counter(collections.Counter(g.area.replace('', '(none)'))), bins=fmt_counter(collections.Counter(g.bin.replace('', '?'))),
                  seals=len(s), seal_endings=','.join(x or 'jar' for x in s.after), seal_sites=','.join(s.site),
                  seal_areas=','.join(s.area.replace('', '?')), seal_cisi=' '.join(s.cisi), seal_res=','.join(f'{x:+.2f}' for x in s.res.dropna())))
T = pd.DataFrame(T).sort_values('chit_tablets', ascending=False); T.to_csv(f'{OUT}/c2_chit_names.csv', index=False)
say(f'\n  comb chit names: {len(T)}; tablets per name: {fmt_counter(collections.Counter(T.chit_tablets))}')
for _, r in T.head(25).iterrows():
    say(f'    {r["name"]:26s} tabs {r.chit_tablets:3d} trenches {r.trenches[:50]:50s} seals {r.seals} {r.seal_endings} {r.seal_sites} {r.seal_areas} {r.seal_res}')
say('  chit names WITH a seal:')
for _, r in T[T.seals > 0].iterrows():
    say(f'    {r["name"]:26s} tabs {r.chit_tablets:3d} [{r.trenches}] seals: {r.seal_cisi} ends {r.seal_endings} at {r.seal_sites} {r.seal_areas} res {r.seal_res}')

# Q3 findspot: seal of a chit name in the trench of its tablets
say('\nQ3 findspot of seals of chit names (Harappa seals with an area):')
HS = SE[(SE.site == 'Harappa') & (SE.area != '')]
pairs = []
for nm in T[T.seals > 0].name:
    tr = set(CH[CH.name == nm].area) - {''}
    for _, s in HS[HS.name == nm].iterrows(): pairs.append((nm, s.area, tr))
o3 = sum(a in tr for _, a, tr in pairs)
allareas = HS.area.values; n3 = []
for _ in range(4000):
    n3.append(sum(rng.choice(allareas) in tr for _, a, tr in pairs))
n3 = np.array(n3)
say(f'  {len(pairs)} Harappa seals of chit names with an area; in a trench holding that name\'s chits {o3} against {n3.mean():.2f} (P {(n3 >= o3).mean():.4f})')
for p in pairs: say(f'    {p[0]:24s} seal in {p[1]:20s} chits in {sorted(p[2])}')
# Mound level (first letter group)
def mound(a):
    a = a.strip()
    if not a: return ''
    if a.startswith('AB'): return 'AB'
    if a.startswith('ET'): return 'ET'
    return a[0]
o4 = sum(mound(a) in {mound(x) for x in tr} for _, a, tr in pairs)
n4 = np.array([sum(mound(rng.choice(allareas)) in {mound(x) for x in tr} for _, a, tr in pairs) for _ in range(4000)])
say(f'  same mound (letter group of the trench): {o4} against {n4.mean():.2f} (P {(n4 >= o4).mean():.4f})')

# the comb-ending seals of chit names: where are they against that name's chits?
say('\n  comb-ending seals of chit names and where their chits lie:')
for _, s_ in SE[SE.name.isin(hit) & (SE.after == '400')].iterrows():
    tr = collections.Counter(CH[CH.name == s_['name']].area.replace('', '(none)'))
    say(f'    {s_.cisi:8s} {s_["name"]:12s} {s_.site:12s} {s_.area or "?":14s} res {s_.res:+.2f}  chits: {fmt_counter(tr)}')
# redesign: crest-level match (the house, not the person)
say('\nredesign: house level (crest of the chit name on any seal before a jar):')
ccrest = set(CH.crest); jcrest = set(HT[HT.after == ''].crest)
for lab, cs in (('comb chit crests', ccrest), ('jar-only tablet crests', jcrest)):
    S3 = SE[SE.crest.isin(cs)]
    say(f'  {lab}: {len(cs)} crests; seals {len(S3)}; comb-ending {int((S3.after == "400").sum())} ({(S3.after == "400").mean():.1%}); '
        f'size residual {S3.res.mean():+.3f}')
say(f'  all jar seals: comb-ending {(SE.after == "400").mean():.1%}, residual {SE.res.mean():+.3f}')
say('done')
