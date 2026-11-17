#!/usr/bin/env python3
"""Recheck 13: other findings in FRAME.md that count things found together.
  (a) house-mates ending in the jar share the sign before it: 15 pairs against 9.3 (pre_jar.py; FRAME 5, MAP)
  (b) room-mates share the number before a fish: 5 pairs against 0.74 (stars_5_rooms.py; FRAME 12)
  (c) Lothal warehouse square: 7 different texts on 15 impression faces against 12.96; Kalibangan KLB-1 2 against 7.35
      (stamps_7_clusters.py; FRAME 27)
  (d) the nine-city pair 590-390: its 22 Mohenjo-daro seals in 21 houses, same-house pairs 1 against 1.84 (FRAME 6) -
      checked here for stones counted twice only.
Plain words as in the scripts named. Checks: (1) faces as objects, (2) shuffle pool, (c) copies found together.
Run: python3 recheck_13_other_pairs.py   (about 2 minutes)
"""
import sys, re, csv, collections, random, io, contextlib
sys.path.insert(0, '/home/claude/ivc/work_scripts')
import numpy as np, pandas as pd
from recheck_common import *
say = log_to(f'{OUT}/r13_log.txt')
f2s, _ = stone_map()

# ---------------- (a) pre-jar sign ----------------
say('(a) pre-jar sign shared by house-mates (old 15 against 9.3)')
random.seed(31)
r = list(csv.DictReader(open(LIPI, encoding='utf-8')))
objs = {}
for x in r:
    if x['site'] != 'Mohenjo-daro' or not x['type'].startswith('SEAL'): continue
    o = objs.setdefault(f2s[x['id']], dict(area=x['area-section'], house=x['block-house'], room=x['room-grid'], toks=[], depth=x['depth'], cisi=x['cisi'], nf=0))
    o['toks'] += re.findall(r'\d{3}', x['text']); o['nf'] += 1
def dep(s):
    m = re.search(r'(-?\d+(\.\d+)?)\s*ft', s); return float(m.group(1)) if m else None
U = []
for o in objs.values():
    t = o['toks']
    if o['house'] in ('--', '-', '') or len(t) < 3 or t[0] != '740' or t[1] == '000' or dep(o['depth']) is None: continue
    o['pre'] = t[1]; o['d'] = dep(o['depth']); o['hk'] = (o['area'], o['house']); o['text'] = '-'.join(t); U.append(o)
say(f'  seals {len(U)} (faces were already joined by object in the old script; two-faced among them: {sum(o["nf"] > 1 for o in U)})')
def prejar(U, label, nsh=3000):
    hk = [o['hk'] for o in U]
    def count(hk):
        idx = collections.defaultdict(list)
        for i, h in enumerate(hk): idx[h].append(i)
        c = n = 0
        for mem in idx.values():
            for a in range(len(mem)):
                for b in range(a + 1, len(mem)):
                    i, j = mem[a], mem[b]
                    if abs(U[i]['d'] - U[j]['d']) > 5: continue
                    n += 1; c += U[i]['pre'] == U[j]['pre']
        return c, n
    obs, n = count(hk)
    strata = collections.defaultdict(list)
    for i, o in enumerate(U): strata[(o['area'], int(o['d'] // 3))].append(i)
    nl = []
    for t in range(nsh):
        ph = hk[:]
        for idx in strata.values():
            sh = idx[:]; random.shuffle(sh)
            for i, j in zip(idx, sh): ph[i] = hk[j]
        nl.append(count(ph)[0])
    nl = np.array(nl)
    say(f'  {label}: {len(U)} seals, {n} same-house pairs within 5 ft; same pre-jar sign {obs} against {nl.mean():.2f} (ratio {obs / nl.mean():.2f}, P {pvalue_hi(nl, obs):.4f})')
    return obs, nl.mean(), pvalue_hi(nl, obs)
a0 = prejar(U, 'A  stones (as the old design)')
seen = set(); Uc = []
for o in U:
    k = (o['hk'], o['text'])
    if k in seen: continue
    seen.add(k); Uc.append(o)
a1 = prejar(Uc, f'B  clean: identical texts in one house once ({len(U) - len(Uc)} removed)')

# ---------------- (b) number before a fish ----------------
say('\n(b) room-mates share the number before a fish (old 5 against 0.74)')
with contextlib.redirect_stdout(io.StringIO()):
    from stars_common import d as sd, moh, units, FISHALL
room = sd.groupby('obj')['room-grid'].first()
H = moh[moh.seal].copy(); H['room'] = H.index.map(room)
H = H[H.room.notna() & ~H.room.isin(['--', '-', '']) & H.dep.notna()].copy(); H['rk'] = H.house + '|' + H.room
H['stone'] = [f2s.get(f'{i}.1', str(i)) for i in H.index]
H['full'] = H.faces.map(lambda fs: '|'.join(sorted('-'.join(f) for f in fs)))
rng4 = np.random.default_rng(23)
def stars(H, label, eligible_only):
    H = H.reset_index(drop=True)
    v = []
    for o in H.itertuples():
        s = set()
        for x, P in zip(o.faces, o.parses):
            for u in units(x, P):
                if u['nxt'] in FISHALL: s.add(u['value'])
        v.append(s)
    keys = H.rk.values; dep_ = H.dep.values; band = H.band.values
    has = [i for i in range(len(H)) if v[i]]
    def count(k):
        g = collections.defaultdict(list)
        for i in has: g[k[i]].append(i)
        c = 0
        for m in g.values():
            for a in range(len(m)):
                for b in range(a + 1, len(m)):
                    i, j = m[a], m[b]
                    if abs(dep_[i] - dep_[j]) <= 3 and v[i] & v[j]: c += 1
        return c
    obs = count(keys); bb = collections.defaultdict(list)
    pool = has if eligible_only else range(len(H))
    for i in pool: bb[band[i]].append(i)
    sims = []
    for _ in range(5000):
        k = keys.copy()
        for ii in bb.values():
            if len(ii) > 1: k[ii] = keys[rng4.permutation(ii)]
        sims.append(count(k))
    sims = np.array(sims)
    say(f'  {label}: {len(has)} seals with a number + fish; same-room pairs sharing the number {obs} against {sims.mean():.2f} (P {pvalue_hi(sims, obs):.4f})')
    return obs, sims.mean(), pvalue_hi(sims, obs)
b0 = stars(H, 'A  as run (rooms dealt among all seals of the area x 3-ft band)', False)
Hc = H.drop_duplicates('stone').drop_duplicates(['rk', 'full'])
b1 = stars(Hc, f'B  clean: stones, identical texts in a room once ({len(H) - len(Hc)} removed), rooms dealt only among number + fish seals', True)

# ---------------- (c) impression clusters ----------------
say('\n(c) distinct stamped texts in one place (old: Lothal 7 on 15 faces against 12.96; KLB-1 2 against 7.35)')
I = pd.read_csv(f'{ROOT}/work_data/stamps/impressions.csv', dtype=str).fillna(''); I['lost'] = I.lost.astype(int)
C = I[(I.lost == 0) & (I.area != '')].copy()
C['stone'] = C.face.map(f2s)
rng = np.random.default_rng(53)
def clusters(C, label):
    out = {}
    for (site, area) in [('Lothal', 'SRG 3GX 10'), ('Kalibangan', 'KLB-1')]:
        g = C[(C.site == site) & (C.area == area)]; rest = C[~((C.site == site) & (C.area == area))].signs.values
        k = len(g); real = g.signs.nunique()
        dr = np.array([len(set(rng.choice(rest, k, replace=False))) for _ in range(5000)])
        say(f'  {label} {site} {area}: {k} stampings on {g.stone.nunique()} objects, {real} different texts; draws {dr.mean():.2f} (P fewer-or-equal {pvalue_lo(dr, real):.4f})')
        out[site] = (k, real, dr.mean(), pvalue_lo(dr, real))
    return out
c0 = clusters(C, 'A  as run (one per face)')
c1 = clusters(C.drop_duplicates(['stone', 'signs']), 'B  clean (one object stamped twice with one text = one stamping)')

# ---------------- (d) 590-390 ----------------
say('\n(d) 590-390 seals at Mohenjo-daro: stones counted twice?')
d = faces(); d['stone'] = d.id.map(f2s)
m = d[(d.site == 'Mohenjo-daro') & d.type.str.startswith('SEAL') & d.text.str.contains('390-590')]
say(f'  faces {len(m)}, objects {m.obj.nunique()}, stones {m.stone.nunique()}; houses {m[~m["block-house"].isin(list(EMPTY))].groupby(["area-section", "block-house"]).ngroups}')
import json
json.dump(dict(prejar=[a0, a1], stars=[b0, b1], clusters=[c0, c1]), open(f'{OUT}/r13.json', 'w'), default=float, indent=1)
