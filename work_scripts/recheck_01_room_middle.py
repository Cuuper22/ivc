#!/usr/bin/env python3
"""Recheck 1: same-room seals at Mohenjo-daro share an uncommon middle sign, 5 pairs against 0.73
(research/extensions_20261117/findspot_room/findspot_room.py, part C, cell: middle signs, sign on <= 80 catalogue rows,
depth gap <= 3 ft, room labels shuffled within excavation area x 3-ft depth band).

Plain words: a MIDDLE sign is any sign that is not the first or last of the text. UNCOMMON = on at most 80 catalogue
rows. A PAIR = two seals found in the same room whose depths differ by 3 ft or less. CHANCE = the room labels dealt
at random among seals of the same excavation area and the same 3-ft depth band, 3,000 times.

Checks: (1) is any counted pair two faces / two rows of one stone? (2) does the pool of dealt seals hold seals that
cannot share a middle sign at all (texts of 2 signs have no middle)? (c) identical texts in one room counted once.
Clean run: one row per stone; only seals with at least one known middle sign; identical texts in a room collapsed;
for seals with two faces the middle is taken face by face (the ends of each face are ends, not middle).
Run: python3 recheck_01_room_middle.py   (about 1 minute)
"""
import sys, collections, random, re, importlib.util
import numpy as np
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from recheck_common import *
say = log_to(f'{OUT}/r01_log.txt')
spec = importlib.util.spec_from_file_location('fr', f'{ROOT}/research/extensions_20261117/findspot_room/findspot_room.py')
fr = importlib.util.module_from_spec(spec); spec.loader.exec_module(fr)
rows = fr.read_catalogue()
freq = collections.Counter()
for x in rows:
    for t in set(fr.signs_of(x['text'])):
        if t != '000': freq[t] += 1
f2s, merges = stone_map()

def build(per_face_middle, need_middle):
    objs = {}
    for x in rows:
        if x['site'] != 'Mohenjo-daro' or not x['type'].startswith('SEAL'): continue
        k = f2s[x['id']]
        o = objs.setdefault(k, dict(area=x['area-section'], house=x['block-house'], room=x['room-grid'], depth=x['depth'],
                                    cisi=x['cisi'], toks=[], mid=set(), faces=0))
        st = fr.signs_of(x['text']); o['toks'] += st; o['faces'] += 1
        if per_face_middle: o['mid'] |= set(st[1:-1]) - {'000'}
    U = []
    for o in objs.values():
        if o['house'] in fr.EMPTY or o['room'] in fr.EMPTY: continue
        st = o['toks']
        if len([t for t in st if t != '000']) < 2: continue
        d = fr.depth_ft(o['depth'])
        if d is None: continue
        if not per_face_middle: o['mid'] = set(st[1:-1]) - {'000'}
        if need_middle and not o['mid']: continue
        o['d'] = d; o['rk'] = (o['area'], o['house'], o['room']); o['text'] = '-'.join(st)
        U.append(o)
    return U

def run(U, collapse, label, nsh=3000, seed=3):
    random.seed(seed)
    if collapse:   # identical full text in one room = one event
        seen = {}; V = []
        for o in U:
            key = (o['rk'], o['text'])
            if key in seen: continue
            seen[key] = 1; V.append(o)
        say(f'   collapsing identical texts in one room removes {len(U) - len(V)} seals'); U = V
    rk = [o['rk'] for o in U]
    def count(lab):
        idx = collections.defaultdict(list)
        for i, h in enumerate(lab): idx[h].append(i)
        c = n = 0; same_obj = 0; pairs = []
        for mem in idx.values():
            for a_ in range(len(mem)):
                for b_ in range(a_ + 1, len(mem)):
                    a, b = U[mem[a_]], U[mem[b_]]
                    if abs(a['d'] - b['d']) > 3: continue
                    n += 1
                    if any(freq[t] <= 80 for t in a['mid'] & b['mid']): c += 1; pairs.append((a['cisi'], b['cisi']))
        return c, n, pairs
    obs, n, pairs = count(rk)
    strata = collections.defaultdict(list)
    for i, o in enumerate(U): strata[(o['area'], int(o['d'] // 3))].append(i)
    nl = []
    for t in range(nsh):
        p = rk[:]
        for idx in strata.values():
            sh = idx[:]; random.shuffle(sh)
            for i, j in zip(idx, sh): p[i] = rk[j]
        nl.append(count(p)[0])
    nl = np.array(nl)
    say(f'  {label}: {len(U)} seals, {n} same-room pairs within 3 ft; share an uncommon middle sign {obs} against {nl.mean():.2f} '
        f'(ratio {obs / nl.mean():.2f}, P {pvalue_hi(nl, obs):.4f})')
    return obs, nl.mean(), pvalue_hi(nl, obs), pairs, U

say('Recheck 1: same-room seals share an uncommon middle sign (old: 5 against 0.73, P 0.0010)')
say(f'stone merges in the whole catalogue (two rows = one stone): {len(merges)}, none of them a Mohenjo-daro seal: '
    f'{all(m[0] != "Mohenjo-daro" for m in merges)}')
o0 = run(build(False, False), False, 'A  original design reproduced (faces joined by object id, as the old script did)')
two = sum(o['faces'] > 1 for o in o0[4]); say(f'   seals in the pool with two inscribed faces: {two}')
say('   pairs behind the count: ' + '; '.join(f'{a}+{b}' for a, b in o0[3]))
say(f'   fault 1 (a pair that is one stone): {sum(a == b for a, b in o0[3])} of {len(o0[3])}')
o1 = run(build(False, True), True, 'B  clean: only seals that have a middle sign, identical texts in a room once')
o2 = run(build(True, True), True, 'C  clean + middle taken face by face')
import json
json.dump(dict(old=dict(obs=5, exp=0.73, p=0.0010), reproduced=o0[:3], clean=o1[:3], clean_faces=o2[:3]),
          open(f'{OUT}/r01.json', 'w'), default=float, indent=1)
say(f'OLD 5 against 0.73 | CLEAN {o1[0]} against {o1[1]:.2f}, P {o1[2]:.4f} | face-by-face {o2[0]} against {o2[1]:.2f}, P {o2[2]:.4f}')
