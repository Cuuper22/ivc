#!/usr/bin/env python3
"""sense_control_run.py -- the CONTROL: real English sentences (human translations of Wiktionary example sentences for Tamil, Telugu, Kannada
words), each word with its real multi-sense WordNet entry. Same scoring code as the Indus run (sense_core.py). Real assignment (every word keeps
its own sense list) against N within-class-and-band shuffles (A) and the sense-count-keeping shuffles (B). Lift is learned on the other half
of the sentences. Output work_data/sense/results_control.json.   Usage: /tmp/senv/bin/python sense_control_run.py [N]"""
import sys, os, json, time, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from sense_core import *
D = '/home/antigravity/Cuuper22/ivc/work_data/sense'; N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
VERS = ['ov', 'lift', 'cos']
def log(*a): print(time.strftime('%H:%M:%S'), '[sense_control_run]', *a, flush=True)
SS = pd.read_csv(f'{D}/control_senses.csv').fillna(''); W = pd.read_csv(f'{D}/control_words.csv'); EM = np.load(f'{D}/control_emb.npy').astype(np.float32)
texts = json.load(open(f'{D}/control_texts.json'))
words = list(W.word); senses = {}; emb = {}
for w, g in SS.groupby('word', sort=False):
    senses[w] = [(r.phrase, [c for c in r.cats.split('|') if c]) for r in g.itertuples()]; emb[w] = EM[g.index.values]
widx = {w: i for i, w in enumerate(words)}
rng0 = np.random.default_rng(99)
tx = [[widx[w] for w in t] for t in texts]; tf = [int(rng0.integers(0, 2)) for _ in tx]
P = Prob(words, senses, emb, words, words, list(W.cls), list(W.band), tx, [1.0] * len(tx), tf, lmax=12, name='control')
log('control: words', len(words), 'texts', len(tx), 'truncated', P.trunc, 'words per cell: ', {k: len(v) for k, v in list(P.cell.items())[:6]}, '...')
P.build(VERS)
short = np.array([1.0 if len(t) <= 4 else 0.0 for t in tx]); groups = {'all': np.ones(len(tx)), 'short': short}
def run_set(asg):
    out = {}
    for v in VERS:
        fit, ok = P.fits(asg, v)
        for g, m in groups.items(): out[f'{v}|{g}'] = float(P.total(fit, ok, m)['all'])
    return out
real = run_set(P.real); log('REAL', {k: round(v, 4) for k, v in real.items()})
res = dict(N=N, real=real, n_texts=len(tx), n_short=int(short.sum()), n_words=len(words), shuf={})
for matched, tag in ((False, 'A'), (True, 'B')):
    rng = np.random.default_rng(31 + matched); rec = collections.defaultdict(list); t0 = time.time(); ds = []
    for i in range(N):
        a = P.shuffle(rng, matched=matched); ds.append(np.abs(P.nsens[a] - P.nsens[P.real]).mean())
        for k, v in run_set(a).items(): rec[k].append(v)
        if (i + 1) % 100 == 0: log(f'{tag}: {i + 1}/{N} ({time.time() - t0:.0f}s)')
    res['shuf'][tag] = dict(rec=rec, dsens=float(np.mean(ds)))
json.dump(res, open(f'{D}/results_control.json', 'w')); log('done')
