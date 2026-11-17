#!/usr/bin/env python3
"""HEADS 4: does one name collect under more than one heading, from more than one mound, and with the same amount?
Predictions written 2026-11-17 BEFORE these numbers:
  P1. Most names under headings stand under ONE heading: at least 80% of the distinct names.
  P2. Yet more names stand under two or more headings than a random dealing of the heading labels among the heading tablets
      gives (the headings are all offices of one city): observed 2 to 4 names, chance below 1.  The shared names are comb or
      repeated names (176-740-400 is the most repeated Harappa name).
  P3. A name that stands under two headings stands in two mounds (ET and F), as the two headings are city-wide.
  P4. The amount under the two headings is NOT the same (a name keeps its amount only inside one account).
Method: name = the signs before the jar (front word and slot taken off; a leading count + measure run such as 033-700 taken off); for a name face without a jar the whole face. Tablets in
one copy event (same trench, same full text) count once.  Chance: the heading label is dealt at random among the heading tablets
that carry a name (each heading keeps its number of tablets), 20,000 deals; statistic = names under >= 2 headings.
Outputs: work_data/heads/h4_names.csv, h4_log.txt.   Run: python3 heads_4_names.py (seconds)
"""
from heads_common import *
say = log_to(f'{HOUT}/h4_log.txt')
rng = np.random.default_rng(4)
H = harappa_stones()
U = pd.read_csv(f'{HOUT}/h2_under.csv', dtype=str).fillna('')
U = U[U.name != ''].copy()
def strip_amount(n):
    t = n.split('-')
    for i, x in enumerate(t):
        if x in ('700', '705', '706') and i + 1 < len(t) and all(y in NUM or y in ('700', '705', '706') for y in t[:i + 1]): return '-'.join(t[i + 1:])
    return n
U['name1'] = [strip_amount(n.split('; ')[0]) for n in U.name]
U['obj'] = U.obj.astype(str)
# one row per issue
U['issue'] = [H.loc[H.index[H.obj.astype(str) == o][0]].issue for o in U.obj]
U = U.drop_duplicates(['family', 'issue', 'name1'])
say(f'heading issues with a name partner: {len(U)}; distinct names {U.name1.nunique()}; families {U.family.nunique()}')
# amount of each issue
def cups_of(o):
    r = H.loc[H.index[H.obj.astype(str) == o][0]]; v = []
    for f in r.faces:
        a = amount_of(f)
        if 'cup' in a: v.append(a['cup'])
    return v
byname = collections.defaultdict(list)
for _, r in U.iterrows(): byname[r.name1].append(r)
multi = {n: v for n, v in byname.items() if len({x.family for x in v}) >= 2}
under1 = sum(1 for v in byname.values() if len({x.family for x in v}) == 1)
say(f'names under exactly one heading: {under1} of {len(byname)} ({100 * under1 / len(byname):.0f}%); under 2+ headings: {len(multi)}')
obs = len(multi)
fams = U.family.values; names = U.name1.values
nl = []
for _ in range(20000):
    f = rng.permutation(fams); d = collections.defaultdict(set)
    for n, ff in zip(names, f): d[n].add(ff)
    nl.append(sum(1 for s in d.values() if len(s) >= 2))
nl = np.array(nl)
say(f'names under 2+ headings: observed {obs}, chance {nl.mean():.2f} (max {nl.max()}); P(chance <= observed) {pvalue_lo(nl, obs):.4f}')
# repeated names (any repeat) under the same heading
rep = {n: v for n, v in byname.items() if len(v) >= 2}
sameh = sum(1 for v in rep.values() if len({x.family for x in v}) == 1)
say(f'names on 2+ heading issues: {len(rep)}; of these under one heading only {sameh}, under several {len(multi)}')
# same-heading repeats against chance
nl2 = []
for _ in range(20000):
    f = rng.permutation(fams); d = collections.defaultdict(list)
    for n, ff in zip(names, f): d[n].append(ff)
    nl2.append(sum(1 for v in d.values() if len(v) >= 2 and len(set(v)) == 1))
say(f'repeated names all under ONE heading: observed {sameh}, chance {np.mean(nl2):.2f}; P(>=) {pvalue_hi(nl2, sameh):.4f}')
rows = []
say('\nNAMES UNDER 2+ HEADINGS')
for n, v in multi.items():
    say(f'  name [{n}]')
    for x in v:
        c = cups_of(x.obj)
        say(f'      under {x.family:12s} {x.cisi:8s} {x.trench:14s} mound {x.mound or "?":3s} bin {x.bin:8s} cups {c}  sig {x.sig}')
        rows.append(dict(name=n, family=x.family, cisi=x.cisi, trench=x.trench, mound=x.mound, bin=x.bin, cups=c, sig=x.sig))
    mounds = {x.mound for x in v if x.mound}; 
    say(f'      mounds {sorted(mounds)}; headings {sorted({x.family for x in v})}')
pd.DataFrame(rows).to_csv(f'{HOUT}/h4_names.csv', index=False)
# repeated names under one heading: mounds
say('\nNAMES REPEATED UNDER ONE HEADING (2+ issues)')
for n, v in rep.items():
    if n in multi: continue
    say(f'  [{n}] under {v[0].family}: {len(v)} issues; trenches {sorted({x.trench for x in v})}; mounds {sorted({x.mound for x in v if x.mound})}; cups {[cups_of(x.obj) for x in v]}')
# (leading count + unit run, e.g. 033-700-176, is taken off the name in both places)
# the same names on the rest of Harappa tablets (not under these headings)
hn = set(byname)
N = name_rows(load()) if False else None
rest = H[(H.nfaces >= 1)]
other = collections.defaultdict(list)
for o, r in rest.iterrows():
    for f, jp in zip(r.faces, r.jars):
        if jp is None: continue
        nm = strip_amount('-'.join(jp[0]))
        if nm in hn: other[nm].append((r.cisi, r.trench, r.mound, amount_of(f).get('cup'), r.sig))
say('\nWHERE ELSE THE HEADING NAMES STAND (all Harappa jar faces with that name; tablets of any kind)')
for n in sorted(hn, key=lambda x: -len(other.get(x, []))):
    ot = other.get(n, [])
    say(f'  [{n}] under headings {sorted({x.family for x in byname[n]})}; Harappa objects with this name {len(ot)}; trenches {len({t[1] for t in ot})}; mounds {len({t[2] for t in ot if t[2]})}')
# summary: of names under headings, how many stand on other Harappa objects at all
say(f'\nheading names that stand on another Harappa object: {sum(1 for n in hn if len(other.get(n, [])) >= 2)} of {len(hn)}')
# ---- new idea for the tie question: do the names under headings stand on seals (the houses behind the tablets)?
with contextlib.redirect_stdout(io.StringIO()):
    NR = name_rows(load())
NR['n1'] = [strip_amount(n) for n in NR.name]
seal_names = set(NR[(NR.kind == 'seal') & ~NR.lost & (NR.n1 != '')].n1)
tab_names = NR[(NR.site == 'Harappa') & (NR.kind == 'mtab') & ~NR.lost & (NR.n1 != '')]
base = tab_names.drop_duplicates('n1').n1.map(lambda x: x in seal_names)
hn_ok = [n for n in hn if n and '000' not in n]
hits = [n for n in hn_ok if n in seal_names]
import math
pbase = float(base.mean()); k = len(hits); nn = len(hn_ok)
pb = sum(math.comb(nn, j) * pbase ** j * (1 - pbase) ** (nn - j) for j in range(k, nn + 1))
say(f'\nTIE VIA NAMES: heading names that also stand before a jar on a seal (any city): {k} of {nn}; all Harappa tablet names {100 * pbase:.1f}% ({int(base.sum())} of {len(base)}); exact binomial P(>= {k}) {pb:.4f}')
for n in hits: say(f'   {n}: seals ' + ', '.join(sorted(set(f"{r.cisi}" for r in NR[(NR.kind == "seal") & (NR.n1 == n)].itertuples()))[:6]))
by_h = collections.defaultdict(list)
for n, v in byname.items():
    for x in v: by_h[x.family].append(n)
for f, ns in by_h.items():
    ns = sorted(set(n for n in ns if '000' not in n)); say(f'   {f:12s}: {sum(n in seal_names for n in ns)} of {len(ns)} names on seals')
say('done')
