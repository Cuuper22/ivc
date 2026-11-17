#!/usr/bin/env python3
"""CHITS 5: the third face.  Objects with 3+ inscribed faces: which face is the name, which the amount, what is the third.

Third face classed by its frame-v2 jobs (classes_v2.csv), no words:
  count+porter  : number + porter / load-carrier (151-158)          count+front : number + front word (003-861)
  heading line  : starts with sign 413 or 415-578 (the 'header' signs of the long account lines)
  second name   : has a jar or a crest/name job                     second amount : counts / cup / measures only
  single sign   : one sign                                           lost : all signs lost          other
The catalogue's picture field (symbol) is listed beside it (Mult = several pictures, Anth = human figure ...).

PREDICTIONS (written before any number):
 F1 most third faces are count+porter or count+front (the E11 'hands / loads / cups' set), and they go with no-jar names.
 F2 comb names never carry a third face other than a second copy of the amount.
Writes work_data/chits/c5_third.csv, c5_log.txt.
"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chits_common import *
LOG = open(f'{OUT}/c5_log.txt', 'w'); say = say_to(LOG)
with contextlib.redirect_stdout(io.StringIO()):
    from measures_common import objs as RAW
O = load()
T3 = O[O.nfaces >= 3]
say(f'objects with 3+ faces: {len(T3)}; sites {fmt_counter(collections.Counter(T3.site))}; kinds {fmt_counter(collections.Counter(T3.kind))}')
PORT = {'151', '154', '155', '156', '158', '161'}
def third_kind(f, t):
    f = list(f); core = [s for s in f if s != '000']
    if not core: return 'lost'
    if f[0] in ('413',) or f[:2] == ['415', '578']: return 'heading line'
    if t == 'amount': return 'second amount'
    if any(s in PORT for s in core) and any(s in NUM for s in core) and len(core) <= 3: return 'count+porter'
    if any(s in ('861', '817') for s in core) and any(s in NUM for s in core) and len(core) <= 3: return 'count+front'
    if '740' in core or t == 'name': return 'second name'
    if len(core) == 1: return 'single sign'
    return 'other'
rows = []
for o, r in T3.iterrows():
    fs = ['-'.join(f) for f in r.faces]
    nf = next((k for k, jp in enumerate(r.jars) if jp is not None and len(jp[0]) > 0), None)
    if nf is None: nf = next((k for k, t in enumerate(r.types) if t == 'name'), None)
    af = next((k for k, f in enumerate(r.faces) if k != nf and 'cup' in amount_of(f)), None)
    if af is None: af = next((k for k, t in enumerate(r.types) if k != nf and t == 'amount'), None)
    rest = [k for k in range(r.nfaces) if k not in (nf, af)]
    ending = ''
    if nf is not None and r.jars[nf] is not None: ending = r.jars[nf][1] or 'jar'
    elif nf is not None: ending = 'no jar'
    for k in rest:
        rows.append(dict(obj=o, cisi=r.cisi, site=r.site, kind=r.kind, area=r.area, bin=r.bin, picture=RAW.loc[o].symbol,
                         name_face=fs[nf] if nf is not None else '', ending=ending or 'no name face',
                         amount_face=fs[af] if af is not None else '', third=fs[k], third_kind=third_kind(r.faces[k], r.types[k]),
                         third_v2='-'.join(V2.get(s, 'PERSONAL') if s != '000' else 'LOST' for s in r.faces[k])))
R = pd.DataFrame(rows); R.to_csv(f'{OUT}/c5_third.csv', index=False)
R['issue'] = R.name_face + '|' + R.amount_face + '|' + R.third + '#' + R.area
say(f'third faces: {len(R)} (distinct issues {R.issue.nunique()})')
for lab, df in (('objects', R), ('issues (copies once)', R.drop_duplicates('issue'))):
    say(f'\n[{lab}] third-face kind x name ending:')
    ct = pd.crosstab(df.third_kind, df.ending); say(ct.to_string())
    ct.to_csv(f'{OUT}/c5_kind_by_ending_{"obj" if lab == "objects" else "issue"}.csv')
say('\nthird face kinds with their amount face (issues):')
D = R.drop_duplicates('issue')
for k, g in D.groupby('third_kind'):
    say(f'  {k:14s} n {len(g):3d}; amounts: {fmt_counter(collections.Counter(g.amount_face.replace("", "(none)")), 5)}; pictures: {fmt_counter(collections.Counter(g.picture.replace("", "(none)")), 4)}; sites {fmt_counter(collections.Counter(g.site), 3)}')
say('\nall issues:')
for _, r in D.sort_values(['third_kind', 'site']).iterrows():
    say(f'  {r.third_kind:13s} {r.cisi:9s} {r.site[:10]:10s} {r.area[:14]:14s} pic {r.picture or "-":6s} name [{r.name_face}] ({r.ending}) amount [{r.amount_face}] third [{r.third}]')
say('done')
