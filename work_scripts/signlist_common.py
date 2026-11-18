#!/usr/bin/env python3
"""Shared kit for the sign-list job (signlist_*.py), 2026-11-17. Word-free: sign numbers, drawings, jobs, counts only.

COUNTING (FRAME.md "How pairs are counted"):
  1. One row per physical object: Lipi faces joined by object id, duplicate catalogue rows of one stone merged
     (recheck_common.stone_map).
  2. A batch of identical moulded copies counts once: all stones of one site and one findspot (area | block-house |
     room-grid, any of them filled) with the same full text (all faces) are ONE COPY EVENT. A stone with no findspot is its
     own event. Second catalogue (Mahadevan 1977): one text number = one object; same site + locus + full text = one event.
  3. Every count of sign uses, neighbours, swaps and co-occurrence below is over copy events (each event's faces once).

Reading order: corpus_jobs.csv `signs` is already in reading order. Lost sign = 000; 'ALT' and empty are not signs.
A face with a broken edge (corpus_jobs broken_edge) gives no start / end boundary and is not used for swap frames.
"""
import os, sys, re, collections, time
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recheck_common as rc

ROOT = '/home/antigravity/Cuuper22/ivc'
OUT = f'{ROOT}/work_data/signlist'; os.makedirs(OUT, exist_ok=True)
EMPTY = {'', '-', '--', '- -'}


def logger(name):
    fh = open(f'{OUT}/log_{name}.txt', 'w')
    def say(*a):
        s = f'[{name} {time.strftime("%H:%M:%S")}] ' + ' '.join(str(x) for x in a)
        print(s, flush=True); fh.write(s + '\n'); fh.flush()
    return say


def is_sign(s):
    return bool(s) and s not in ('000', 'ALT') and s.isdigit()


def load_lipi():
    """returns list of events: dict(ev, site, kind, faces=[tuple], broken=[bool], stones=[...])"""
    c = pd.read_csv(f'{ROOT}/work_data/frame/corpus_jobs.csv', dtype=str).fillna('')
    meta = rc.faces()
    f2s, _ = rc.stone_map(meta)
    fs = {}
    for fid, a, b, r in zip(meta.id, meta['area-section'], meta['block-house'], meta['room-grid']):
        parts = [x.strip() for x in (a, b, r)]
        fs[fid] = '|'.join(parts) if any(p not in EMPTY for p in parts) else ''
    stones = collections.OrderedDict()
    for face, site, kind, sig, br in zip(c.face, c.site, c.object_kind, c.signs, c.broken_edge):
        st = f2s.get(face, face.split('.')[0])
        tok = tuple(x for x in sig.split('-') if x)
        S = stones.setdefault(st, dict(stone=st, site=site, kind=kind, spot=fs.get(face, ''), faces=[], broken=[], face_ids=[]))
        if face in S['face_ids']: continue
        S['faces'].append(tok); S['broken'].append(br == 'True'); S['face_ids'].append(face)
        if not S['spot']: S['spot'] = fs.get(face, '')
    events = collections.OrderedDict()
    for st, S in stones.items():
        full = '|'.join(sorted('-'.join(f) for f in S['faces']))
        key = (S['site'], S['spot'], full) if S['spot'] else ('stone', st)
        if key in events:
            events[key]['stones'].append(st); continue
        events[key] = dict(ev=f'L{st}', site=S['site'], kind=S['kind'], faces=S['faces'], broken=S['broken'], stones=[st], cat='L')
    return list(events.values())


def load_mahadevan(numbering='lipi'):
    """second catalogue as events. numbering='lipi' -> reading_lipi tokens; 'mah' -> Mahadevan numbers (0 = lost)."""
    M = pd.read_csv(f'{ROOT}/work_data/mahadevan_parsed.csv', dtype=str).fillna('')
    objs = collections.OrderedDict()
    for tn, site, cls, loc, comp, rm, rl in zip(M.textnum, M.site, M.cls, M.locus, M.complete, M.reading_mah, M.reading_lipi):
        if numbering == 'lipi':
            tok = tuple(x for x in rl.split('-') if x)
        else:
            tok = tuple(('000' if x == '0' else 'M' + x) for x in rm.split('-') if x)
        o = objs.setdefault(tn, dict(site=site, kind=cls, locus=loc, faces=[], broken=[]))
        o['faces'].append(tok); o['broken'].append(comp != 'True')
    events = collections.OrderedDict()
    for tn, o in objs.items():
        full = '|'.join(sorted('-'.join(f) for f in o['faces']))
        key = (o['site'], o['locus'], full) if o['locus'] not in EMPTY else ('obj', tn)
        if key in events: events[key]['stones'].append(tn); continue
        events[key] = dict(ev=f'M{tn}', site=o['site'], kind=o['kind'], faces=o['faces'], broken=o['broken'], stones=[tn], cat='M')
    return list(events.values())


def uses(events):
    u = collections.Counter()
    for e in events:
        for f in e['faces']:
            for s in f:
                if is_sign(s) or s.startswith('M') and s != 'M0': u[s] += 1
    return u


def bands(u, signs, nb=5):
    """frequency band of each sign: quantile bands over the eligible signs' use counts"""
    vals = np.array([u[s] for s in signs])
    edges = np.quantile(vals, np.linspace(0, 1, nb + 1)[1:-1])
    return {s: int(np.searchsorted(edges, u[s], side='right')) for s in signs}


def shapes():
    sh = pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv', dtype=str).fillna('')
    return {r.lipi_wells_number: (r.mayig_code, r.shape_description) for r in sh.itertuples()}


def crosswalk():
    x = pd.read_csv(f'{ROOT}/work_data/lipi_mahadevan_crosswalk.csv', dtype=str)
    x['share'] = x.share_of_lipi_sign.astype(float)
    return x


def v2classes():
    c = pd.read_csv(f'{ROOT}/work_data/frame/classes_v2.csv', dtype=str).fillna('')
    return {s: k for s, k in zip(c.sign, c.v2_base) if s}


def pvalue_hi(null, obs):
    null = np.asarray(null); return float((1 + (null >= obs).sum()) / (len(null) + 1))


def bar(i, n, label, every=None):
    every = every or max(1, n // 10)
    if (i + 1) % every == 0 or i + 1 == n:
        k = int(20 * (i + 1) / n)
        print(f'    {label} [{"#" * k}{"." * (20 - k)}] {100 * (i + 1) // n}%', flush=True)
