#!/usr/bin/env python3
"""Step 2: each reading measured in Lipi numbers and in Mahadevan numbers.  Run: python3 second_measure.py"""
import sys, collections
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from mah_common import *

# ---- sign sets in the two numberings
LS = dict(jar={'740'}, man={'090'}, spear={'520'}, porter={'151', '153', '154', '155', '156', '158'}, carrier={'154', '155', '158'},
          diamond={'861', '817'}, wheel={'820'}, cup={'700'}, crop={'806'}, acomb={str(i) for i in range(465, 476)},
          comb={'400'}, fish={'235', '240', '233', '231'}, tag={'760', '100'}, two={'002', '013'}, cap={'060'}, cap2={'920'})
MS = dict(jar={342}, man={1}, spear={211}, porter={15, 12}, carrier={15}, diamond={267}, wheel={391}, cup={328}, crop={389}, acomb={178},
          comb={176}, fish={65, 67, 72, 70}, tag={347, 8}, two={99, 100}, cap={123}, cap2={293})
LSHORT = {'001': 1, '002': 2, '003': 3, '004': 4, '005': 5, '006': 6, '007': 7, '012': 2, '013': 3, '014': 4, '015': 5, '016': 6, '017': 7, '018': 8}
LLONG = {'031': 1, '032': 2, '033': 3, '034': 4, '035': 5, '036': 6}
MSHORT = {97: 1, 98: 1, 99: 2, 100: 2, 101: 2, 102: 3, 103: 3, 104: 4, 105: 4, 106: 5, 107: 5, 108: 6, 109: 6, 110: 7, 112: 7, 114: 8}
MLONG = {86: 1, 87: 2, 89: 3, 95: 4, 96: 5}


def lipi_texts():
    l = load_lipi()
    out = []
    for i, r in l.iterrows():
        if r.broken or not r.complete_txt: continue
        cls = {'seal': 'seal', 'tablet': 'tablet', 'pottery': 'pottery', 'copper tablet': 'copper tablet'}.get(r.group, 'other')
        out.append(dict(obj=str(r.id).split('.')[0], face=str(r.id), site=r.gsite, cls=cls, toks=tuple(r.tok)))
    return out


def mah_texts():
    m = load_mah(); out = []
    cmap = {'seal': 'seal', 'sealing': 'seal', 'miniature tablet': 'tablet', 'pottery graffito': 'pottery', 'copper tablet': 'copper tablet'}
    for i, r in m.iterrows():
        if not r.complete: continue
        out.append(dict(obj=r.textnum, face=r.textnum + '.' + r.sideline, site=r.site, cls=cmap.get(r.cls, 'other'), toks=tuple(r.toks),
                        fs=r.fs, locus=r.locus, level=r.level, rawcls=r.cls))
    return out


def distinct(texts):
    seen = {}
    for t in texts: seen.setdefault((t['site'], t['cls'], t['toks']), t)
    return list(seen.values())


def frac(a, b): return f'{a} of {b} ({100 * a / b:.0f}%)' if b else f'{a} of 0'


def measure(name, texts, S, SH, LG):
    T = [t['toks'] for t in distinct(texts)]
    seal = [t['toks'] for t in distinct(texts) if t['cls'] == 'seal']
    R = {}
    # load tag
    a = c3 = cr = crc = 0; crp = crp_a = crp_s = crp_o = 0
    for t in T:
        for i in range(len(t) - 1):
            if t[i + 1] in S['crop']:
                if t[i] in S['acomb']: a += 1; c3 += (i + 2 < len(t) and t[i + 2] in S['carrier'])
                if i + 2 < len(t) and t[i + 2] in S['porter']:
                    crp += 1
                    if t[i] in S['acomb']: crp_a += 1
                    elif t[i] in SH: crp_s += 1
                    else: crp_o += 1
    R['load: A-comb then crop'] = a
    R['load: A-comb crop then carrier'] = frac(c3, a)
    R['load: crop followed by a porter sign, preceded by A-comb / short stroke / other'] = f'{crp} total: {crp_a} / {crp_s} / {crp_o}'
    # porter follows crop only after count
    # jar and what follows
    nj = last = 0; after = collections.Counter()
    for t in seal:
        for i, x in enumerate(t):
            if x in S['jar']:
                nj += 1
                if i == len(t) - 1: last += 1
                else: after[t[i + 1]] += 1
    R['jar uses (seal texts)'] = nj; R['jar is last'] = frac(last, nj)
    for nm in ('man', 'spear', 'porter', 'comb'):
        k = sum(c for x, c in after.items() if x in S[nm])
        tot = sum(1 for t in seal for x in t if x in S[nm])
        R[f'{nm}: follows jar / all uses on seals'] = frac(k, tot)
    # man after jar as share of man's texts
    mt = [t for t in seal if any(x in S['man'] for x in t)]
    mj = sum(1 for t in mt if any(t[i] in S['jar'] and i + 1 < len(t) and t[i + 1] in S['man'] for i in range(len(t) - 1)))
    R['man texts with jar+man'] = frac(mj, len(mt))
    # man abroad: round seals excluded here
    # cups
    cc = collections.Counter(); prev = collections.Counter()
    for t in T:
        for i, x in enumerate(t):
            if x in S['cup']:
                cc[LG.get(t[i - 1], 'other') if i else 'start'] += 1
    R['cup preceded by long count n'] = {str(k): v for k, v in sorted(cc.items(), key=lambda z: str(z[0]))}
    # openers
    n_open = sum(1 for t in seal if t[0] in S['diamond'] | S['wheel']); n2 = sum(1 for t in seal if len(t) > 1 and t[0] in S['diamond'] | S['wheel'] and t[1] in S['two'])
    R['seals opening diamond/wheel'] = n_open; R['  of them then two strokes'] = frac(n2, n_open)
    cap = sum(1 for t in seal if len(t) > 1 and t[0] in S['cap2'] | S['cap'] | {'692', '550'} and False)
    # counted: long vs short before each thing
    return R


def tablets(texts, S, SH, LG, MAHMODE):
    """ration tablets: objects with 2+ faces; faces '3 diamonds', '3 porters', 'n cups'."""
    byobj = collections.defaultdict(list)
    for t in texts: byobj[t['obj']].append(t)
    res = collections.Counter(); cups = collections.Counter(); three = 0; allthree = 0; ratio = collections.Counter()
    for o, fs in byobj.items():
        if len(fs) < 2 and not MAHMODE: pass
        f3d = f3p = ncup = None
        for f in fs:
            t = f['toks']
            if len(t) == 2 and t[1] in S['diamond'] and SH.get(t[0]) == 3: f3d = True
            if len(t) == 2 and t[1] in (S['porter'] - {'151'} if isinstance(next(iter(S['porter'])), str) else {15}) and SH.get(t[0]) == 3: f3p = True
            if len(t) == 2 and t[1] in S['cup'] and t[0] in LG: ncup = LG[t[0]]
        if ncup is not None and len(fs) >= 2: cups[ncup] += 1
        if f3d and f3p:
            allthree += 1
            ratio[ncup] += 1
        if f3d: res['objects with a 3-diamond face'] += 1
        if f3p: res['objects with a 3-porter face'] += 1
    res['objects with 3 diamonds + 3 porters faces'] = allthree
    res['  ...and cups face n'] = dict(ratio)
    res['multi-face objects with an "n cups" face: n'] = dict(sorted(cups.items()))
    return dict(res)


if __name__ == '__main__':
    LT, MT = lipi_texts(), mah_texts()
    for nm, T, S, SH, LG, mm in (('LIPI', LT, LS, LSHORT, LLONG, False), ('MAHADEVAN', MT, MS, MSHORT, MLONG, True)):
        print('=====', nm, 'complete lines', len(T), 'distinct', len(distinct(T)))
        for k, v in measure(nm, T, S, SH, LG).items(): print(f'  {k}: {v}')
        print('  -- tablet records')
        for k, v in tablets(T, S, SH, LG, mm).items(): print(f'  {k}: {v}')
