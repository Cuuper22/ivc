#!/usr/bin/env python3
"""LUMPS step 1: every clay lump (sealing) that carries 2+ impressions, from both catalogues, one row per impression.
Written 2026-11-17 before any lump number was counted.  Word-free: sign numbers and job classes only.

Plain words
- LUMP: one physical clay sealing.  First catalogue (Lipi): rows of tier 'sealing' (catalogue type TAG...) that share an object
  id; each row is one impression.  Moulded tablets (TAB:B) and stamped pots are NOT lumps and are left out.
  Second catalogue (Mahadevan 1977): object class 2 (sealing); one text number is one lump; sideline 10, 20, 30, 40 are its
  impressions.  Surfaces with no text at all carry no readable impression and are dropped.
- The two catalogues overlap (the same lump is in both, often transcribed differently).  A Mahadevan lump is treated as the SAME
  lump as a Lipi lump when it is at the same site and one of its impression texts near-fits an impression of that Lipi lump
  (same length, equal where both readable, at most one clash) with 3+ equal readable signs, or two of its impressions near-fit
  with 2+ equal signs.  This is loose on purpose: a doubtful Mahadevan lump is dropped, so no lump is counted twice.
  Overlapping lumps are kept once, from Lipi.  Mahadevan lumps with the same site, locus and set of impression texts (a
  batch of identical moulded lumps found together) are kept once (column batch).
- ROLE of an impression (fixed rule, written before counting; uses front_common.parse and its front-word set):
    NAME stamp : the text has a closer sign (740 520 151 154 155 158 or after-jar title) in its ending, and >= 3 signs.
    SHORT stamp: no closer, and (it starts with a front word, or it is a count line, or it has <= 3 signs), with at least
                 one readable sign.
    OTHER      : anything else (long damaged text with no closer, unreadable).
  FIELD of a name stamp = its signs up to and including the first slot sign when that is in the first three places (the heading,
  front.md); BODY = what is left before the ending; crest (FRAME definition) = first non-number sign of the BODY; crest class (frame v2 CREST class, the 11 signs 140 220 222 226 231
  233 235 240 243 803 806) = every such sign in the BODY.  Both are tested.  TAIL of a short stamp = its signs left after
  removing the front word, slot signs and number signs.
- A lump's impressions with identical text count once (the same stone pressed twice).
Writes work_data/lumps/impressions.csv and lumps.csv.
"""
import sys, os, re, collections
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
import numpy as np, pandas as pd
from front_common import load, front_set, parse, V2, NUMS, CLOSERS, TITLES, SLOT
ROOT = '/home/antigravity/Cuuper22/ivc'; OUT = f'{ROOT}/work_data/lumps'
print('loading first catalogue ...', flush=True)
D = load()
F, _, _, _ = front_set(D, say=lambda *a: None)
O = pd.read_csv(f'{ROOT}/work_data/stamps/objects.csv', dtype=str).fillna('')
O = O[O.tier == 'sealing']
cnt = O.groupby('obj').face.transform('size')
O = O[cnt >= 2]
print('Lipi lumps with 2+ impression rows:', O.obj.nunique(), flush=True)

def has_front_unit(t, F):
    # a front word followed by a slot sign at the very start, or one sign in (317-920-002)
    for i in (0, 1):
        if i + 1 < len(t) and t[i] in F and t[i + 1] in SLOT: return True
    return False

def role(t, p):
    sig = [s for s in t if s not in ('000', 'ALT') and not s.startswith('X')]
    n = len(t)
    if p['has_closer'] and n >= 3: return 'name'
    if not sig: return 'unreadable'
    if any(x in CLOSERS for x in t) and not p['has_closer']: return 'other'   # a closer sign shows but the end is lost: a damaged name stamp, left out of both roles
    if not p['has_closer'] and (p['front'] or has_front_unit(t, F) or p['is_count'] or n <= 3): return 'short'
    return 'other'

def field_body(t, p):
    # FIELD = everything up to and including the first slot sign when that sign is in the first three places (front.md, finding 1);
    # BODY = the rest before the ending.  Crest = first non-number sign of the body.
    t = list(t); k = next((i for i, s in enumerate(t[:3]) if s in SLOT), None)
    field = t[:k + 1] if k is not None else []
    rest = t[k + 1:] if k is not None else t
    j = len(rest)
    while j > 0 and (rest[j - 1] in CLOSERS or rest[j - 1] in TITLES): j -= 1
    body = rest[:j]
    crest = next((s for s in body if s not in NUMS), '')
    return '-'.join(field), '-'.join(body), crest

CREST_CLS = {x for x, c in V2.items() if c == 'CREST'}   # frame v2 CREST class: 140 220 222 226 231 233 235 240 243 803 806
def crest_cls(body): return ' '.join(x for x in body.split('-') if x in CREST_CLS)

def tail(t, p):
    return tuple(s for s in t if s not in F and s not in SLOT and s not in NUMS and s not in ('000', 'ALT') and not s.startswith('X'))

rows = []
for r in O.itertuples():
    t = tuple(r.signs.split('-')); p = parse(t, F)
    rows.append(dict(cat='Lipi', lump='L1:' + r.obj, label=r.cisi, site=r.site, spot=r.area or r.building, depth=r.depth_ft,
                     imp=int(r.face.split('.')[1]), text='-'.join(t), animal=r.animal, role=role(t, p),
                     front='-'.join((p['front'],) + p['slots']) if p['front'] else '', name='-'.join(p['name']),
                     ending='-'.join(p['ending']), field=field_body(t, p)[0], body=field_body(t, p)[1], crest=field_body(t, p)[2], crest_cls=crest_cls(field_body(t, p)[1]),
                     tail='-'.join(tail(t, p)), restored=r.restored))
M = pd.read_csv(f'{ROOT}/work_data/mahadevan_parsed.csv', dtype=str).fillna('')
M = M[M.cls == 'sealing']
raw = pd.read_csv(f'{ROOT}/research/data/mahadevan_20260905/concordance_rows.csv', dtype=str).fillna('')
raw = raw[raw.inscobj == '2']
nlines = raw.groupby('textnum').size()
sitemap = {'MD': 'Mohenjo-daro', 'HP': 'Harappa', 'CD': 'Chanhu-daro', 'LL': 'Lothal', 'KB': 'Kalibangan', 'OS': 'Other', 'WA': 'West Asia'}
for r in M.itertuples():
    t = tuple(r.reading_lipi.split('-')); p = parse(t, F)
    rows.append(dict(cat='Mah', lump='M2:' + r.textnum, label='Mah' + r.textnum, site=sitemap[r.site], spot=f'locus {r.locus}',
                     depth=r.level, imp=int(r.sideline), text='-'.join(t), animal=('fs' + r.fs) if r.fs != '0' else '',
                     role=role(t, p), front='-'.join((p['front'],) + p['slots']) if p['front'] else '', name='-'.join(p['name']),
                     ending='-'.join(p['ending']), field=field_body(t, p)[0], body=field_body(t, p)[1], crest=field_body(t, p)[2], crest_cls=crest_cls(field_body(t, p)[1]),
                     tail='-'.join(tail(t, p)), restored=''))
I = pd.DataFrame(rows)
# keep lumps with 2+ impression rows
I = I[I.groupby('lump').imp.transform('size') >= 2].copy()

def wild(x): return x in ('000', 'ALT') or x.startswith('X')

def near(a, b):
    """same length; equal where both readable; at most 1 clash; returns number of equal readable signs or -1."""
    a = a.split('-'); b = b.split('-')
    if len(a) != len(b): return -1
    eq = clash = 0
    for x, y in zip(a, b):
        if wild(x) or wild(y): continue
        if x == y: eq += 1
        else: clash += 1
    return eq if clash <= 1 and eq >= 1 else -1

Lp = {k: g for k, g in I[I.cat == 'Lipi'].groupby('lump')}
Mh = {k: g for k, g in I[I.cat == 'Mah'].groupby('lump')}
dup = {}
for mk, mg in Mh.items():
    best = None
    for lk, lg in Lp.items():
        if lg.site.iloc[0] != mg.site.iloc[0] and mg.site.iloc[0] != 'Other': continue   # Mahadevan's 'Other' covers Rupar etc.
        used = set(); strong = 0; hits = 0
        for t in mg.text:
            cand = [(near(t, u), j) for j, u in zip(lg.index, lg.text) if j not in used]
            cand = [c for c in cand if c[0] >= 2]
            if cand:
                k, j = max(cand); used.add(j); hits += 1; strong += k >= 3
        ok = strong >= 1 or hits >= 2   # loose on purpose: when in doubt a Mahadevan lump is treated as a Lipi lump and counted once
        if ok and (best is None or (hits, strong) > best[0]): best = ((hits, strong), lk)
    if best: dup[mk] = best[1]
print('Mahadevan lumps that are also in Lipi:', len(dup), 'of', len(Mh), flush=True)
for mk, lk in dup.items():
    print('  ', Mh[mk].label.iloc[0], '=', Lp[lk].label.iloc[0], '|', ' / '.join(Mh[mk].text), '||', ' / '.join(Lp[lk].text))
I['dup_of'] = I.lump.map(dup).fillna('')
sets = I.groupby('lump').apply(lambda g: '|'.join(sorted(set(g.text))), include_groups=False)
meta = I.groupby('lump')[['site', 'spot']].first()
I['batch'] = I.lump.map(lambda k: f"{meta.site[k]}~{meta.spot[k]}~{sets[k]}")
I.to_csv(f'{OUT}/impressions.csv', index=False)
print(I.groupby('cat').lump.nunique().to_string())
print(I.role.value_counts().to_string())
