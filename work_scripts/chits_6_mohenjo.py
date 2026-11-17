#!/usr/bin/env python3
"""CHITS 6: what Mohenjo-daro has in the role Harappa's amount + name chits play.  Plus the heading faces (413 / 415-578
lines ending 824 / 876) that stand beside different names at Harappa.

Per city (Harappa, Mohenjo-daro) and object kind (clay tablet mtab, copper tablet ctab, tag, rod, pot):
objects; record kind (face types sorted); share with a cup count; share with a jar name; share with the comb ending;
picture field (symbol).  Then the 21 comb-ending objects at Mohenjo-daro listed whole, and the Harappa 'heading'
faces with every partner face.

PREDICTIONS (written before any number):
 M1 Mohenjo-daro's chit role is filled by copper tablets: a picture + a text with no cup count, many copies of one text.
 M2 the comb at Mohenjo-daro sits on rods and small tablets, not on copper tablets, and without cups.
 M3 heading faces at Harappa pair with 3+ different names and sit in several trenches: an issuing office's line.
Writes work_data/chits/c6_*.csv, c6_log.txt.
"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chits_common import *
with contextlib.redirect_stdout(io.StringIO()):
    from measures_common import objs as RAW
LOG = open(f'{OUT}/c6_log.txt', 'w'); say = say_to(LOG)
O = load(); O['symbol'] = RAW.symbol.reindex(O.index).fillna('')
O['rec'] = ['+'.join(sorted(t)) for t in O.types]
O['has_cup'] = [any('cup' in amount_of(f) for f in fs) for fs in O.faces]
O['jarname'] = [any(j is not None for j in js) for js in O.jars]
O['comb'] = [any(j is not None and j[1] == '400' for j in js) for js in O.jars]
O['man'] = [any(j is not None and j[1] == '090' for j in js) for js in O.jars]
rows = []
for site in ('Harappa', 'Mohenjo-daro'):
    for k in ('mtab', 'ctab', 'tag', 'rod', 'pot', 'seal'):
        s = O[(O.site == site) & (O.kind == k)]
        if len(s) == 0: continue
        sigs = s[s.lostfree].sig
        rows.append(dict(site=site, kind=k, objects=len(s), multi_face=int((s.nfaces >= 2).sum()), with_cup=int(s.has_cup.sum()),
                         jar_name=int(s.jarname.sum()), comb=int(s.comb.sum()), man=int(s.man.sum()),
                         with_picture=int((~s.symbol.isin(['', '-'])).sum()), distinct_texts=sigs.nunique(), lostfree=len(sigs),
                         top_records=fmt_counter(collections.Counter(s.rec), 5), top_pictures=fmt_counter(collections.Counter(s.symbol[~s.symbol.isin(['', '-'])]), 5)))
K = pd.DataFrame(rows); K.to_csv(f'{OUT}/c6_city_kinds.csv', index=False)
for _, r in K.iterrows():
    say(f'{r.site[:7]:7s} {r.kind:5s} obj {r.objects:4d} multi {r.multi_face:4d} cup {r.with_cup:4d} jar-name {r.jar_name:4d} comb {r.comb:3d} man {r.man:3d} pic {r.with_picture:4d} '
        f'texts {r.distinct_texts}/{r.lostfree} | {r.top_records} | {r.top_pictures}')

say('\nMohenjo-daro copper tablets: commonest texts (copies) and their pictures:')
M = O[(O.site == 'Mohenjo-daro') & (O.kind == 'ctab') & O.lostfree]
for sg, g in sorted(M.groupby('sig'), key=lambda x: -len(x[1]))[:15]:
    say(f'  x{len(g):2d} {sg:40s} pictures {fmt_counter(collections.Counter(g.symbol))}  areas {fmt_counter(collections.Counter(g.area), 3)}')
say('Mohenjo-daro clay tablets: commonest texts:')
M2 = O[(O.site == 'Mohenjo-daro') & (O.kind == 'mtab') & O.lostfree]
for sg, g in sorted(M2.groupby('sig'), key=lambda x: -len(x[1]))[:12]:
    say(f'  x{len(g):2d} {sg:40s} pictures {fmt_counter(collections.Counter(g.symbol))}  areas {fmt_counter(collections.Counter(g.area), 3)}')
# copies per distinct text, the two cities, tablets
for site in ('Harappa', 'Mohenjo-daro'):
    for k in ('mtab', 'ctab'):
        s = O[(O.site == site) & (O.kind == k) & O.lostfree]
        if len(s): say(f'  copies per distinct text, {site} {k}: {len(s) / s.sig.nunique():.2f} ({len(s)} objects / {s.sig.nunique()} texts)')

say('\ncomb-ending objects outside Harappa:')
C = O[O.comb & (O.site != 'Harappa')]
for _, r in C.sort_values(['site', 'kind']).iterrows():
    say(f'  {r.site[:12]:12s} {r.kind:5s} {r.cisi:8s} {r.area[:14]:14s} pic {r.symbol or "-":8s} bin {r.bin or "-":6s} {r.sig}')
C.drop(columns=['faces', 'types', 'jars']).to_csv(f'{OUT}/c6_comb_outside_harappa.csv', index=False)
# Harappa comb by kind
say('Harappa comb objects by kind: ' + fmt_counter(collections.Counter(O[O.comb & (O.site == 'Harappa')].kind)) +
    '; formats: ' + fmt_counter(collections.Counter(O[O.comb & (O.site == 'Harappa')].type)))
say('Harappa tablets with comb: with a cup count ' + str(int(O[O.comb & (O.site == 'Harappa') & (O.kind == 'mtab')].has_cup.sum())) +
    ' of ' + str(int((O.comb & (O.site == 'Harappa') & (O.kind == 'mtab')).sum())))

# heading faces
say('\nheading faces at Harappa (a face beginning 413 or 415-578, or ending 824 / 876) and their partner faces:')
rows = []
for o, r in O[O.site == 'Harappa'].iterrows():
    fs = ['-'.join(f) for f in r.faces]
    for i, f in enumerate(r.faces):
        f = list(f)
        if f and (f[0] == '413' or f[:2] == ['415', '578'] or f[-1] in ('824', '876')):
            partners = [fs[j] for j in range(len(fs)) if j != i]
            pend = []
            for j in range(len(fs)):
                if j == i: continue
                jp = r.jars[j]
                pend.append((jp[1] or 'jar') if jp is not None else ('cup' if 'cup' in amount_of(r.faces[j]) else r.types[j]))
            rows.append(dict(obj=o, cisi=r.cisi, area=r.area, bin=r.bin, type=r.type, heading=fs[i], partners=' / '.join(partners), partner_roles=','.join(pend)))
HD = pd.DataFrame(rows); HD.to_csv(f'{OUT}/c6_headings.csv', index=False)
say(f'  {len(HD)} heading faces on {HD.obj.nunique()} objects; trenches {fmt_counter(collections.Counter(HD.area.replace("", "(none)")))}')
say(f'  partner roles: {fmt_counter(collections.Counter(",".join(HD.partner_roles).split(",")))}')
for _, r in HD.sort_values('heading').iterrows():
    say(f'    {r.cisi:8s} {r.area[:14]:14s} {r.bin or "-":6s} [{r.heading}] with [{r.partners}] ({r.partner_roles})')
# comb share among names beside heading faces vs Harappa tablet names
roles = ','.join(HD.partner_roles).split(',')
jn = [x for x in roles if x not in ('cup', 'amount', 'thing', 'name', 'lost')]
say(f'  names beside heading faces: endings {fmt_counter(collections.Counter(jn))}; comb share {jn.count("400")}/{len(jn)}')
H = O[(O.site == 'Harappa') & (O.kind == 'mtab')]
allend = [j[1] or 'jar' for js in H.jars for j in js if j is not None]
say(f'  all Harappa tablet jar names: comb share {allend.count("400")}/{len(allend)}')
say('done')
