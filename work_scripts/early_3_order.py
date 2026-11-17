#!/usr/bin/env python3
"""EARLY job, step 3: the order in which the parts of the seal-text template first appear, by dated stage, with counts.

PLAIN WORDS
- A STAGE is a rank on the history job's time axis (work_data/time/time_axis.csv, built by time_common.py): 0 = before the cities
  (Harappa Periods 1-2, Dholavira stages I-II), 1 = Harappa 3A (2600-2450 BC), 2 = 3B-1, 3 = 3B-2 (to 2200 BC; Mackay's Early I level
  at Mohenjo-daro is 3B-2), 4 = 3B/C, 5 = 3C-1, 6 = 3C-2, 7 = 3C-3 and later (3C-3, 3C-4, Period 4, Period 5).
  Dates are the harappa.com period dates (3A 2600-2450, 3B 2450-2200, 3C 2200-1900).
- Each feature is counted over the objects dated to that stage (all sites with a date), as objects with the feature / objects at the stage.
  Name features are counted over seals and tablets with a name before a jar only where stated.
- FIRST SEEN = the first stage with at least one object; FIRST SOLID = the first stage with at least 3 objects AND at least 1% of
  that stage's objects (so a lone early object does not set the order).

PREDICTIONS (written before this script was run):
 O1  The template grew in parts, in this order: number strokes and the cup first; goods signs; the jar and plain-fish "house" words;
     owner names (a name before the jar); then fish crests and the agent form `X jar man`; the office opening and the overseas bull
     last, no earlier than 3B.
 O2  So the agent form and the office opening are absent at stage 0 and 1.
 O3  If instead the template was invented once (appears complete), most features have their first solid stage inside 3A-3B-1.
Outputs: work_data/early/order_of_appearance.csv, order_first_objects.csv, log_3.txt
"""
import sys, os, io, contextlib, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    from time_common import *

OUTE = f'{ROOT}/work_data/early'
os.makedirs(OUTE, exist_ok=True)
AB = pd.read_csv(f'{ROOT}/work_data/animal/animal_base.csv', dtype=str).fillna('').drop_duplicates('obj').set_index('obj')
FISHSET = {'220', '226', '231', '233', '235', '236', '240', '241'}
Z = T[T['rank'].notna()].copy()
Z['toks'] = Z.faces.apply(lambda fs: [a for f in fs for a in f])
Z['main'] = Z.faces.apply(lambda fs: list(max(fs, key=len)) if len(fs) else [])
Z['stage'] = Z['rank'].map(lambda r: 0 if r == 0 else (1 if r == 1 else (2 if r == 2 else (3 if r == 3 else (4 if r == 4 else (5 if r == 5 else (6 if r == 6 else 7)))))))
Z['animal_grp'] = [AB.animal.get(str(o), '') for o in Z.index]


def nm(x):
    """name signs = signs before the first jar, lost signs dropped (for a text with a jar)"""
    if '740' not in x: return []
    return [a for a in x[:x.index('740')] if a not in ('000', 'ALT')]


def has(x, s): return '-'.join(s) in '-'.join(x)


def f_owner(r):    # name (1+ signs, not only counts) followed by the jar
    n = nm(r.main)
    return len([a for a in n if a not in NUM]) >= 1 and r.kind in ('seal', 'mtab', 'tag')


def f_crestfirst(r):
    n = [a for a in r.main if a not in ('000', 'ALT')]
    if r.kind != 'seal': return False
    k = n.index('740') if '740' in n else len(n)
    nn = n[:k]
    # skip leading number/opener signs (diamond, wheel, cap, strokes) to reach the first name sign
    nn = [a for a in nn if a not in NUM and a not in ('817', '861', '820', '060', '920', '741', '742', '743', '744', '745')]
    return len(nn) > 0 and nn[0] in MARKED


FEATS = [
    ('a number stroke (any)', lambda r: any(a in NUM for a in r.toks), None),
    ('the cup 700', lambda r: '700' in r.toks, None),
    ('a goods sign (413 / 411 / 390 / 806)', lambda r: any(a in ('413', '411', '390', '806') for a in r.toks), None),
    ('the jar 740 ("house of")', lambda r: '740' in r.toks, None),
    ('the plain fish 220', lambda r: '220' in r.toks, None),
    ('a marked fish crest sign (231/233/235/240/236), anywhere', lambda r: any(a in MARKED for a in r.toks), None),
    ('the diamond + two-strokes opener (817/861-002)', lambda r: has(r.main, ('817', '002')) or has(r.main, ('861', '002')), 'seal'),
    ('a name before the jar (owner seal or chit)', f_owner, None),
    ('"child of" 760-740', lambda r: has(r.main, ('760', '740')), None),
    ('spear 520 as the last sign (spearman)', lambda r: len(r.main) > 0 and r.main[-1] == '520', 'seal'),
    ('comb 400 as the last sign', lambda r: len(r.main) > 0 and r.main[-1] == '400', None),
    ('fish crest as the first name sign (seals)', f_crestfirst, 'seal'),
    ('the agent form X jar man (740-090)', lambda r: has(r.main, ('740', '090')), None),
    ('the office opening 920-060-741', lambda r: has(r.toks, ('920', '060', '741')), None),
    ('Boxed-cotton house 590-390', lambda r: has(r.toks, ('590', '390')), None),
    ('kalam / ship sign 705 or 706', lambda r: any(a in ('705', '706') for a in r.toks), None),
    ('the overseas short-horned bull (seals)', lambda r: r.animal_grp == 'SHORTHORN', 'seal'),
    ('a seal with an animal and a text', lambda r: r.kind == 'seal' and r.animal_grp not in ('', 'NONE'), 'seal'),
    ('a seal with text only (no animal)', lambda r: r.kind == 'seal' and r.animal_grp == 'NONE', 'seal'),
]
STAGES = ['0 before cities', '1 3A', '2 3B-1', '3 3B-2', '4 3B/C', '5 3C-1', '6 3C-2', '7 3C-3+']
base = Z.groupby('stage').size().reindex(range(8), fill_value=0)
seals = Z[Z.kind == 'seal'].groupby('stage').size().reindex(range(8), fill_value=0)
print('objects dated per stage:', dict(zip(STAGES, base.tolist())), '| seals:', seals.tolist())
rows, firsts = [], []
for lab, f, scope in FEATS:
    hit = Z[Z.apply(f, axis=1)]
    if scope == 'seal': hit = hit[hit.kind == 'seal']
    cnt = hit.groupby('stage').size().reindex(range(8), fill_value=0)
    den = seals if scope == 'seal' else base
    first_seen = next((i for i in range(8) if cnt[i] >= 1), None)
    first_solid = next((i for i in range(8) if cnt[i] >= 3 and den[i] > 0 and cnt[i] / den[i] >= 0.01), None)
    row = dict(feature=lab, **{STAGES[i]: f'{cnt[i]}/{den[i]}' for i in range(8)}, first_seen=STAGES[first_seen] if first_seen is not None else '-',
               first_solid=STAGES[first_solid] if first_solid is not None else '-', total=int(cnt.sum()))
    rows.append(row)
    if first_seen is not None:
        o = hit.sort_values('rank').iloc[0]
        firsts.append(dict(feature=lab, first_seen=STAGES[first_seen], object=o.cisi, site=o.site, kind=o.kind, dating=o.time, text=' | '.join('-'.join(t) for t in o.faces)))
O = pd.DataFrame(rows); O.to_csv(f'{OUTE}/order_of_appearance.csv', index=False)
pd.DataFrame(firsts).to_csv(f'{OUTE}/order_first_objects.csv', index=False)
print(O.to_string(index=False))
print('\nFIRST OBJECT FOR EACH FEATURE')
for r in firsts: print(f"  {r['feature'][:52]:52s} {r['first_seen']:15s} {r['site']:12s} {r['object']:8s} {r['kind']:5s} {r['text'][:60]}")

# ---- the same order inside Mohenjo-daro only (one dig sequence) and Harappa only (excavators' phasing)
for site in ['Harappa', 'Mohenjo-daro']:
    s = Z[Z.site == site]
    print(f'\n{site} ONLY: objects per stage', s.groupby('stage').size().reindex(range(8), fill_value=0).tolist())
    line = []
    for lab, f, scope in FEATS:
        hit = s[s.apply(f, axis=1)]
        if scope == 'seal': hit = hit[hit.kind == 'seal']
        cnt = hit.groupby('stage').size().reindex(range(8), fill_value=0)
        fs = next((i for i in range(8) if cnt[i] >= 1), None)
        line.append(f'{lab[:40]}: first {STAGES[fs] if fs is not None else "-"} ({cnt.tolist()})')
    print('\n'.join('  ' + l for l in line))

# ---- crest-first fish and the agent form side by side, over every object kind that has a name before the jar
print('\nCREST-FIRST FISH NAMES AND AGENTS AMONG OBJECTS WITH A NAME BEFORE THE JAR (seals, tablets, tags), by stage and site')


def crest_first_any(r):
    x = [a for a in r.main if a not in ('000', 'ALT')]
    if '740' not in x: return False
    nn = [a for a in x[:x.index('740')] if a not in NUM and a not in ('817', '861', '820', '060', '920', '741', '742', '743', '744', '745')]
    return len(nn) > 0 and nn[0] in MARKED


Zn = Z[Z.kind.isin(['seal', 'mtab', 'tag']) & Z.main.apply(lambda x: '740' in x and len(nm(x)) > 0)].copy()
Zn['crest'] = Zn.apply(crest_first_any, axis=1)
Zn['agent'] = Zn.main.apply(lambda x: has(x, ('740', '090')))
Zn['office'] = Zn.toks.apply(lambda x: has(x, ('920', '060', '741')))
Zn['short'] = Zn.animal_grp == 'SHORTHORN'
for lab, g in [('all sites', Zn), ('Harappa', Zn[Zn.site == 'Harappa']), ('Mohenjo-daro', Zn[Zn.site == 'Mohenjo-daro'])]:
    print(f'  {lab}: named objects per stage', g.groupby('stage').size().reindex(range(8), fill_value=0).tolist())
    for c in ['crest', 'agent', 'office', 'short']:
        print(f'    {c:7s}', g.groupby('stage')[c].sum().reindex(range(8), fill_value=0).astype(int).tolist())
Zn[['cisi', 'site', 'kind', 'time', 'stage', 'crest', 'agent', 'office', 'short']].assign(text=Zn.main.apply('-'.join)).to_csv(f'{OUTE}/order_named_objects.csv')
