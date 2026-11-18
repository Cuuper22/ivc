#!/usr/bin/env python3
"""sense_corpus.py -- builds the list of PHYSICAL OBJECTS (events) used by the sense test.

Plain words: one row per physical object; identical moulded copies found together count once.
  Lipi catalogue (first): faces joined by object id, duplicate catalogue rows of one stone merged (recheck_common.stone_map);
      copy event = same site + same excavation area + same house + same room + same full text on every face (only when the findspot
      is known: area, house or room not blank/'--'); an unknown findspot is never merged.
  New texts (second catalogue, Mahadevan 1977, texts with no Lipi partner): object = text number; copy event = same site + same
      locus + same full text on every face (locus must be known).
Output: work_data/sense/events_lipi.json, events_new.json : list of {"key", "site", "kind", "faces": [[sign,...], ...]} (one per event).
Run: python3 sense_corpus.py"""
import sys, os, json, collections, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    from sound_v3_common import d, M
from recheck_common import stone_map, EMPTY
ROOT = '/home/antigravity/Cuuper22/ivc'; OUT = f'{ROOT}/work_data/sense'; os.makedirs(OUT, exist_ok=True)
def log(*a): print('[sense_corpus]', *a, flush=True)
def known(x): return str(x).strip() not in EMPTY and str(x).strip() != ''

# ---- Lipi ----
f2s, merges = stone_map()
d['stone'] = d.id.map(f2s)
raw = d.copy()
stones = {}
for st, g in d.groupby('stone', sort=False):
    g = g.sort_values('id')
    first = g.iloc[0]
    stones[st] = dict(site=first.site, kind=first.kind, area=first['area-section'], bh=first['block-house'], room=first.get('room-grid', ''),
                      faces=[list(t) for t in g.tok])
log('Lipi faces', len(d), 'stones', len(stones))
ev = {}
nmerge = 0
for st, s in stones.items():
    full = '|'.join(sorted('-'.join(f) for f in s['faces']))
    if known(s['area']) or known(s['bh']) or known(s['room']):
        key = ('L', s['site'], s['area'], s['bh'], s['room'], full)
    else:
        key = ('L', 'stone', st)
    if key in ev: nmerge += 1; continue
    ev[key] = dict(key=str(key), site=s['site'], kind=s['kind'], faces=s['faces'])
log('Lipi physical objects (stones)', len(stones), '-> copy events', len(ev), '(moulded copies merged:', nmerge, ')')
json.dump(list(ev.values()), open(f'{OUT}/events_lipi.json', 'w'))
# ---- new texts ----
m = M[~M.partnered].copy()
evn = {}; nobj = 0; nm = 0
for tn, g in m.groupby('textnum', sort=False):
    nobj += 1
    g = g.sort_values('sideline'); first = g.iloc[0]
    faces = [list(t) for t in g.tok]
    full = '|'.join(sorted('-'.join(f) for f in faces))
    key = ('M', first.site_l, str(first.locus), full) if known(first.locus) else ('M', 'obj', tn)
    if key in evn: nm += 1; continue
    evn[key] = dict(key=str(key), site=first.site_l, kind=first.kind, faces=faces)
log('new-text physical objects', nobj, '-> copy events', len(evn), '(copies merged:', nm, ')')
json.dump(list(evn.values()), open(f'{OUT}/events_new.json', 'w'))
