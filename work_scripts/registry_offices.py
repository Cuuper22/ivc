#!/usr/bin/env python3
"""WHO'S WHO, step 3: the offices. Every title and office word, how many people hold it, in which cities and houses.

A person HOLDS an office when the office word is the ending of the name (chief, keeper, junior, guard, gate-guard,
standard-bearer, deputy, X's man) or stands inside the name or opener (king, king's servant, servant, cultivator,
bondsman, ward 741/742/745, assembly 692, the 7-city office opening 920-060-741, royal 384/388, umbrella 611).
Counted on people.csv (seals read whole or nearly whole) and, in a second column, on every object with an ending
(names_all.csv, undamaged).
PREDICTION (written before counting): king 142 is held by one house per city (one ruling lineage each).
Writes work_data/registry/offices.csv and offices.txt.  Run: python3 registry_offices.py (a few seconds).
"""
import collections, pandas as pd
ROOT = '/home/claude/ivc'; OUT = f'{ROOT}/work_data/registry'
P = pd.read_csv(f'{OUT}/people.csv', dtype=str).fillna('')
A = pd.read_csv(f'{OUT}/names_all.csv', dtype=str).fillna('')
A = A[(A.damaged == 'False') & (A.goods_line == 'False')]
LOG = open(f'{OUT}/offices.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s); LOG.write(s + '\n')
ENDINGS = {'chief (spearman, vēḷ 520)': lambda r: r.ending in ('chief', 'house of, chief'),
           'keeper (kā 151-161)': lambda r: 'keeper' in r.ending,
           'junior (ciṟ 400)': lambda r: 'junior' in r.ending,
           'guard (kāval 525-527)': lambda r: r.ending == 'guard',
           'gate-guard (vāy kāval 550/555 + 527)': lambda r: r.ending == 'gate-guard',
           'standard-bearer (koṭi 368, text-final)': lambda r: r.ending == 'standard-bearer',
           'deputy (tuṇai 842)': lambda r: r.ending == 'deputy',
           "agent, X's man (āḷ 090 after the jar)": lambda r: r.ending.startswith("X's man"),
           'seat / throne (kaṭṭil 679 after the jar)': lambda r: r.ending == 'house of, seat'}
INNAME = {'king (kō 142)': {'142'}, "king's servant (ūḻiyaṉ 617)": {'617'}, 'servant (aṭi 717)': {'717'},
          'cultivator (vēḷāḷaṉ 137)': {'137'}, 'bondsman (aṭimai 097/136)': {'097', '136'},
          'royal (aracu 384/388/382)': {'384', '388', '382'}, 'umbrella (kuṭai 611)': {'611'},
          'chief (mutal 255)': {'255'}, 'elder (mutu 100/101)': {'100', '101'}, 'tax (iṟai 176)': {'176'},
          'first ward (741)': {'741'}, 'second ward (742)': {'742'}, 'third ward (745)': {'745'},
          'assembly (kūṭṭam 692)': {'692'}, 'staff-bearer (kōlaṉ 095)': {'095'}, 'warrior (maṟavaṉ 565)': {'565'}}
def has_in(r, ss):
    t = (r.opener + '-' + r.name_full + '-' + r.ending_signs).split('-')
    return any(s in t for s in ss)
rows = []
for title, f in list(ENDINGS.items()) + [(k, (lambda ss: (lambda r: has_in(r, ss)))(v)) for k, v in INNAME.items()] + \
        [('7-city office opening (920-060-741)', lambda r: r.office == 'True')]:
    pm = P[P.apply(f, axis=1)]; am = A[A.apply(f, axis=1)].drop_duplicates('object_id')
    rows.append(dict(office=title, people_seals=len(pm), objects_any_kind=len(am),
                     cities='; '.join(f'{k} {v}' for k, v in am.site.value_counts().items()),
                     houses='; '.join(f'{k} {v}' for k, v in pm.house_key.value_counts().head(8).items()),
                     n_houses=pm.house_key.nunique(), example_ids='; '.join(pm.cisi.head(6))))
O = pd.DataFrame(rows); O.to_csv(f'{OUT}/offices.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 70)
say(O[['office', 'people_seals', 'objects_any_kind', 'n_houses', 'cities', 'houses']].to_string(index=False))

say('\nKING 142 by city: who holds it (every undamaged object with a name or ending)')
K = A[A.apply(lambda r: has_in(r, {'142'}), axis=1)].drop_duplicates('object_id')
for site, g in K.groupby('site'):
    say(f'  {site}: {len(g)} objects; crests: ' + '; '.join(f'{k} {v}' for k, v in g.house_key.value_counts().items()))
    for _, r in g.iterrows(): say(f'      {r.cisi:9s} {r.kind:5s} {r.signs:32s} house {r.house_key:6s} ending {r.ending}')
say('\nROYAL 384/388 by city:')
K = A[A.apply(lambda r: has_in(r, {'384', '388'}), axis=1)].drop_duplicates('object_id')
for site, g in K.groupby('site'):
    say(f'  {site}: {len(g)} objects; crests: ' + '; '.join(f'{k} {v}' for k, v in g.house_key.value_counts().items()))

say('\nDHOLAVIRA SIGNBOARD name: umbrella 611 everywhere it occurs (all faces, any state)')
import sys, io, contextlib, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    from sound_v4_common import d
E = pd.read_csv(f'{ROOT}/work_data/corpus_english2.csv', dtype=str).fillna('').set_index('face_id')
for fid, x, site, cisi, kind, area in zip(d.id, d.tok, d.site, d.cisi, d.kind, d['area-section']):
    if '611' in x:
        i = x.index('611')
        say(f'  {fid:8s} {cisi:8s} {site:12s} {kind:6s} {area:16s} {"-".join(x):40s} before 611: {x[i-1] if i else "(start)"}  after: {x[i+1] if i + 1 < len(x) else "(end)"} | {E.english.get(fid, "")}')
LOG.close()

# ---------- the "quarter king": quarter 061/820 right before a king word ----------
from scipy.stats import binomtest
LOG = open(f'{OUT}/offices.txt', 'a')
base = sum(1 for x in d.tok for s in x if s in ('061', '820')) / sum(len(x) for x in d.tok)
for k in ('142', '611', '384', '388'):
    n = sum(1 for x in d.tok for s in x if s == k)
    hit = [(c, st, '-'.join(x)) for x, c, st in zip(d.tok, d.cisi, d.site) for i, s in enumerate(x) if s == k and i > 0 and x[i - 1] in ('061', '820')]
    say(f'\nquarter (061/820) right before {k}: {len(hit)} of {n} uses; quarter signs are {base:.3f} of all signs; expected {n * base:.2f}; '
        f'P {binomtest(len(hit), n, base, alternative="greater").pvalue:.2g}')
    for h in hit: say('     ', *h)
LOG.close()
