#!/usr/bin/env python3
"""sense_onegloss.py N K -- same test but every word keeps ONLY its first K senses (K=1: the old one-gloss assumption; label glosses come first in each list). Same texts, folds, shuffles A (class+band).
Original docstring: sense_run.py -- runs the whole sense test and writes work_data/sense/results.json (+ csv tables).
Steps: (1) load signs, senses, embeddings, objects; (2) real scores; (3) N_SHUF shuffles of each kind (A: same class and band; B: also same
number of senses); (4) per-sign real-vs-shuffle; (5) mass run: every candidate word allowed for the sign's job class, real vs scrambled corpus;
(6) the control (English sentences with WordNet senses), same code.
Usage: /tmp/senv/bin/python sense_run.py [N_SHUF]   (background job; progress lines print as it goes)"""
import sys, os, json, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from sense_core import *
ROOT = '/home/antigravity/Cuuper22/ivc'; D = f'{ROOT}/work_data/sense'
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
K = int(sys.argv[2]) if len(sys.argv) > 2 else 1   # keep only each word's first K senses
VERS = ['ov', 'lift', 'cos']
def log(*a): print(time.strftime('%H:%M:%S'), '[sense_run]', *a, flush=True)
T0 = time.time()
# ------------------------------------------------------------------ Indus problem
S = pd.read_csv(f'{D}/signs.csv', dtype={'sign': str}).fillna(''); SS = pd.read_csv(f'{D}/senses.csv').fillna('')
EM = np.load(f'{D}/senses_emb.npy').astype(np.float32)
words = sorted(S.word.unique()); senses = {}; emb = {}
for w, g in SS.groupby('word', sort=False):
    senses[w] = [(r.phrase, [c for c in r.cats.split('|') if c]) for r in g.itertuples()][:K]   # first K senses only (label glosses come first)
    emb[w] = EM[g.index.values][:K]
sidx = {s: i for i, s in enumerate(S.sign)}
rng0 = np.random.default_rng(20261117)
def make_texts(evfile, fold_mode):
    ev = json.load(open(f'{D}/{evfile}')); agg = collections.defaultdict(float); n_ev = 0; n_txt = 0
    for e in ev:
        fold = int(rng0.integers(0, 2)) if fold_mode == 'cross' else 2
        faces = []
        for f in e['faces']:
            us = list(dict.fromkeys(sidx[x] for x in f if x in sidx))
            if len(us) >= 2 and len({S.word.iloc[u] for u in us}) >= 2: faces.append(us)
        if not faces: continue
        n_ev += 1
        for us in faces: agg[(fold, tuple(sorted(us)))] += 1 / len(faces); n_txt += 1
    log(evfile, 'events with a scorable text', n_ev, 'face-texts', n_txt, 'distinct texts', len(agg))
    return agg
A1 = make_texts('events_lipi.json', 'cross'); A2 = make_texts('events_new.json', 'new')
keys = list(A1) + list(A2)
texts = [list(k[1]) for k in keys]; tw = [(A1.get(k) or A2.get(k)) for k in keys]; tf = [k[0] for k in keys]
P = Prob(words, senses, emb, list(S.sign), list(S.word), list(S.cls), list(S.band), texts, tw, tf, lmax=10, name='indus')
log('Indus problem: words', len(P.words), 'max senses', P.S, 'texts', len(texts), 'texts truncated at 10 signs', P.trunc)
grp_new = (P.tfold == 2).astype(float); grp_lip = (P.tfold < 2).astype(float)
log('weights: new texts', grp_new @ P.tw, 'Lipi', grp_lip @ P.tw)
P.build(VERS); log('similarity tables built', f'{time.time() - T0:.0f}s')
# strongest 30: status strict, DEDR number given, not a number sign class, ranked by Lipi faces
cand = S[(S.status == 'strict') & (S.dedr != '') & (~S.cls.str.startswith('NUM'))].sort_values('faces', ascending=False)
strong = list(cand.head(30).sign); log('strongest-labelled pool', len(cand), 'taken', len(strong))
sub30 = np.isin(P.units, strong)
def run_set(P, groups, sub, asg, vers=VERS):
    out = {}; um = {}
    for v in vers:
        fit, ok = P.fits(asg, v)
        for gname, g in groups.items():
            r = P.total(fit, ok, g, sub)
            out[(v, gname, 'all')] = r['all']
            if sub is not None: out[(v, gname, 'sub')] = r['sub']
        um[v] = P.unit_means(fit, ok, groups['all'] if 'all' in groups else list(groups.values())[0])
    return out, um
groups = {'new': grp_new, 'lipi': grp_lip, 'all': np.ones(len(P.tw))}
real, real_um = run_set(P, groups, sub30, P.real)
for k, v in real.items(): log('REAL', k, round(float(v), 5))

rng = np.random.default_rng(4242); rec = collections.defaultdict(list)
for i in range(N):
    a = P.shuffle(rng, matched=False); o, _ = run_set(P, groups, sub30, a)
    for k, v in o.items(): rec['|'.join(k)].append(float(v))
    if (i + 1) % 100 == 0: log(f'one-gloss shuffles {i + 1}/{N}')
out = {}
for k, v in real.items():
    kk = '|'.join(k); a = np.array(rec[kk]); out[kk] = dict(real=float(v), chance=float(a.mean()), sd=float(a.std()), P=float((1 + (a >= v).sum()) / (len(a) + 1)), z=float((v - a.mean()) / a.std()))
json.dump(out, open(f'{D}/results_cap{K}.json', 'w')); log('done')
