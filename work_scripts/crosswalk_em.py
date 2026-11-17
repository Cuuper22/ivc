#!/usr/bin/env python3
"""Lipi -> Mahadevan sign crosswalk by matching whole texts (EM over text pairs of equal length at one site group).

Run: python3 crosswalk_em.py [--noseed]   -> work_data/crosswalk_em_raw.pkl (pair table, text matches) and printed progress.
Each Lipi text (distinct sign string, no broken edge) is compared with every Mahadevan text of the same length at the same
site group. A pair's score is the product over positions of T(m|l)/f(m), times a bonus when repeated signs line up
(position i equals position j in both texts). T is re-estimated from the posterior-weighted positions, seeded with the
known matches. Output: for every Lipi sign its Mahadevan partner(s) with position support.
"""
import sys, os, pickle, math, collections, time
import numpy as np
sys.path.insert(0, '/home/claude/ivc/work_scripts')
from mah_common import *

SEEDS = {'740': 342, '002': 99, '861': 267, '817': 267, '820': 391, '700': 328, '220': 59,
         '031': 86, '032': 87, '033': 89, '034': 95, '035': 96, '400': 176, '156': 15}
GROUP = lambda s: s if s in ('MD', 'HP') else 'MINOR'


def prep():
    l = load_lipi(); m = load_mah()
    lt = {}   # (group, tuple) -> list of row indices
    for i, (t, b, gs) in enumerate(zip(l.tok, l.broken, l.gsite)):
        if b or len(t) < 2: continue
        t = tuple(None if x in ('000', 'ALT', '999', '') else x for x in t)
        lt.setdefault((GROUP(gs), t), []).append(i)
    mt = {}
    for i, (t, s) in enumerate(zip(m.toks, m.site)):
        if len(t) < 2: continue
        t = tuple(None if x == 0 else x for x in t)
        mt.setdefault((GROUP(s), t), []).append(i)
    return l, m, lt, mt


def run(use_seeds=True, iters=14, verbose=True):
    l, m, lt, mt = prep()
    lsigns = sorted({x for (_, t) in lt for x in t if x is not None}); lix = {s: i for i, s in enumerate(lsigns)}
    msigns = sorted({x for (_, t) in mt for x in t if x is not None} | set(range(1, 418))); mix = {s: i for i, s in enumerate(msigns)}
    nL, nM = len(lsigns), len(msigns)
    f = np.ones(nM)
    for (_, t) in mt:
        for x in t:
            if x is not None: f[mix[x]] += 1
    f /= f.sum()
    seed = np.zeros((nL, nM))
    if use_seeds:
        for a, b in SEEDS.items():
            if a in lix: seed[lix[a], mix[b]] = 1
    # arrays per (group, n)
    blocks = {}
    for (g, t) in lt: blocks.setdefault((g, len(t)), [[], []])[0].append(t)
    for (g, t) in mt: blocks.setdefault((g, len(t)), [[], []])[1].append(t)
    pre = {}
    for k, (A, B) in blocks.items():
        if not A or not B: continue
        a = np.array([[lix[x] if x is not None else -1 for x in t] for t in A])
        b = np.array([[mix[x] if x is not None else -1 for x in t] for t in B])
        pre[k] = (A, B, a, b)
    alpha, seedw = 0.3, 40.0
    T = seed * seedw + alpha * f[None, :]
    T /= T.sum(1, keepdims=True)
    logpi, logc = 0.0, math.log(0.4)
    for it in range(iters):
        R = np.log(T / f[None, :])
        C = np.zeros((nL, nM)); tot_post = 0.0; ntext = 0
        results = {}
        for k, (A, B, a, b) in pre.items():
            na, nb = len(A), len(B); n = k[1]
            logS = np.zeros((na, nb))
            for i in range(n):
                ai, bi = a[:, i], b[:, i]
                valid = (ai >= 0)[:, None] & (bi >= 0)[None, :]
                v = R[np.maximum(ai, 0)[:, None], np.maximum(bi, 0)[None, :]]
                logS += np.where(valid, v, 0.0)
            for i in range(n):
                for j in range(i + 1, n):
                    va = (a[:, i] >= 0) & (a[:, j] >= 0); vb = (b[:, i] >= 0) & (b[:, j] >= 0)
                    ea = va & (a[:, i] == a[:, j]); eb = vb & (b[:, i] == b[:, j])
                    na_ = va & ~ea; nb_ = vb & ~eb
                    bonus = np.zeros((na, nb))
                    bonus += np.where(ea[:, None] & eb[None, :], math.log(6), 0)
                    bonus += np.where(ea[:, None] & nb_[None, :], math.log(0.05), 0)
                    bonus += np.where(na_[:, None] & eb[None, :], math.log(0.4), 0)
                    logS += bonus
            lg = logS + math.log(0.6 / nb)
            mx = np.maximum(lg.max(1, keepdims=True), logc)
            den = np.exp(lg - mx).sum(1, keepdims=True) + np.exp(logc - mx)
            P = np.exp(lg - mx) / den
            results[k] = P
            ia, ib = np.nonzero(P > 1e-3)
            for x, y in zip(ia, ib):
                w = P[x, y]
                for i in range(n):
                    if a[x, i] >= 0 and b[y, i] >= 0: C[a[x, i], b[y, i]] += w
            tot_post += P.sum(); ntext += na
        T = C + seed * seedw + alpha * f[None, :]
        T /= T.sum(1, keepdims=True)
        if verbose: print(f'iter {it}: expected matched Lipi texts {tot_post:.0f} of {ntext}', flush=True)
    out = dict(lsigns=lsigns, msigns=msigns, T=T, lt=lt, mt=mt, pre={k: (v[0], v[1]) for k, v in pre.items()}, P=results, C=C)
    return out


if __name__ == '__main__':
    noseed = '--noseed' in sys.argv
    t0 = time.time()
    out = run(use_seeds=not noseed)
    pickle.dump(out, open(f'/home/claude/ivc/work_data/crosswalk_em_raw{"_noseed" if noseed else ""}.pkl', 'wb'))
    print('done', round(time.time() - t0), 's')
