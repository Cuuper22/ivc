#!/usr/bin/env python3
"""Shared kit for the sign-split job (split_*.py), 2026-11-17. Word-free: sign numbers, classes, counts only.

Reuses the frame v2 scoring code (frame2_common: train_texts, class_model_kind, kind grammar, new_texts, v2 base classes).
Nothing here is tuned on any held-out text.

WHAT A SPLIT IS: sign s is replaced, in every occurrence, by one of its variants s@0, s@1 (s@2). Occurrences are labelled
  by a fixed rule (a two- or three-profile mixture on the neighbours, object kind and text length; or a position rule).
HOW A SPLIT IS SCORED (honest, label-free on the held-out text): the frame is refit on the training texts with the
  variants as separate tokens. On a held-out text the labels are NOT given: every occurrence of s may be any variant,
  and the text's probability is the sum over all labellings (forward algorithm). Bits per sign are for the ORIGINAL
  sign sequence, so a split can only win by making the order of signs better predicted.
GRAMMAR: the frame v2 pooled class grammar (the headline one in frame_v2.md) and the by-kind grammar.
CLASS OF A VARIANT: scheme S1 = each variant its own one-sign class. Scheme S2 = each variant joins the v2 class that best
  fits its own left and right class neighbours in the training texts (chosen on training only).
"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from frame2_common import *   # d, M, train_texts, vocab_of, kind_counts, class_model_kind, new_texts, bits, KindModel, FixedKind, c...
import numpy as np, pandas as pd

SPL = f'{ROOT}/work_data/split'
os.makedirs(SPL, exist_ok=True)
c2 = pd.read_csv(f'{OUT2}/classes_v2.csv', dtype=str).fillna('')
BASE = dict(zip(c2.sign, c2.v2_base))          # frame v2 base class of every sign (the 14 classes)
CLS = V2_CLASSES
KIND_B = {'seal': 'seal', 'tag': 'tag', 'mtab': 'tablet', 'ctab': 'copper tablet', 'pot': 'pot'}


def base_of(s):
    return BASE.get(s) or v2_of(s)


def train_with_sites():
    """distinct first-catalogue texts as in frame_common.train_texts, plus the site of the first copy."""
    seen = {}
    for i, x, f, k, st in zip(d.id, d.tok, d.flg, d.kind, d.site):
        if not x: continue
        clean = not (f & {'broken', 'lost', 'alt'}) and not (set(x) & UNK)
        if x not in seen: seen[x] = (clean, k, st)
    return [(x, c, k, st) for x, (c, k, st) in seen.items()]


# ------------------------------------------------------------------ occurrence features
LENB = lambda n: 0 if n == 1 else 1 if n == 2 else 2 if n <= 4 else 3
LEN_NAME = ['len1', 'len2', 'len3-4', 'len5+']


def feat(x, i, clean, kind):
    """(left class, right class, kind, length bucket) of the sign at i. Unknown neighbour or unproven edge -> None."""
    n = len(x)
    if i == 0: l = '^' if clean else None
    else: l = None if x[i - 1] in UNK else base_of(x[i - 1])
    if i == n - 1: r = '$' if clean else None
    else: r = None if x[i + 1] in UNK else base_of(x[i + 1])
    return (l, r, KIND_B.get(kind, 'other'), LEN_NAME[LENB(n)])


class Enc:
    """integer coding of the four features; None -> -1 (ignored in a mixture)."""
    def __init__(self):
        self.L = ['^'] + CLS; self.R = ['$'] + CLS; self.K = sorted(set(KIND_B.values())) + ['other']; self.N = LEN_NAME
        self.maps = [{v: i for i, v in enumerate(vs)} for vs in (self.L, self.R, self.K, self.N)]
        self.dims = [len(self.L), len(self.R), len(self.K), len(self.N)]
        self.names = ['left', 'right', 'kind', 'length']

    def enc(self, f):
        return [(-1 if v is None else self.maps[j][v]) for j, v in enumerate(f)]


ENC = Enc()


# ------------------------------------------------------------------ mixture of independent categorical profiles (missing allowed)
class Mix:
    def __init__(self, K, dims): self.K, self.dims = K, dims

    def _lp(self, X):
        lp = np.tile(np.log(self.pi)[None, :], (len(X), 1))
        for j, D in enumerate(self.dims):
            ok = X[:, j] >= 0
            lp[ok] += np.log(self.th[j][:, X[ok, j]]).T
        return lp

    def fit(self, X, rng, starts=6, iters=80):
        n = len(X); best = None
        for _ in range(starts if self.K > 1 else 1):
            R = rng.dirichlet(np.ones(self.K), n) if self.K > 1 else np.ones((n, 1))
            for _ in range(iters if self.K > 1 else 1):
                self.pi = R.sum(0) + 1e-9; self.pi /= self.pi.sum()
                self.th = []
                for j, D in enumerate(self.dims):
                    Mm = np.full((self.K, D), 0.5)
                    ok = X[:, j] >= 0
                    for k in range(self.K): np.add.at(Mm[k], X[ok, j], R[ok, k])
                    self.th.append(Mm / Mm.sum(1, keepdims=True))
                if self.K == 1: break
                lp = self._lp(X); m = lp.max(1, keepdims=True); R = np.exp(lp - m); R /= R.sum(1, keepdims=True)
            ll = self.loglik(X)
            if best is None or ll > best[0]: best = (ll, self.pi.copy(), [t.copy() for t in self.th])
        _, self.pi, self.th = best
        # order components by size so labels are stable
        o = np.argsort(-self.pi); self.pi = self.pi[o]; self.th = [t[o] for t in self.th]
        return self

    def loglik(self, X):
        lp = self._lp(X); m = lp.max(1, keepdims=True)
        return float((m[:, 0] + np.log(np.exp(lp - m).sum(1))).sum())

    def assign(self, X):
        return self._lp(X).argmax(1)


# ------------------------------------------------------------------ expanded vocabulary, frames, label-free scoring
def occurrences(texts, s):
    """list of (text index, position) of sign s."""
    return [(ti, i) for ti, t in enumerate(texts) for i, a in enumerate(t[0]) if a == s]


def expand(texts, s, occ, labels, ngroups):
    """texts relabelled: occurrence (ti, i) of s becomes s@label. returns new text list (same tuple shape)."""
    lab = {o: l for o, l in zip(occ, labels)}
    out = []
    for ti, t in enumerate(texts):
        x = tuple(f'{s}@{lab[(ti, i)]}' if (ti, i) in lab else a for i, a in enumerate(t[0]))
        out.append((x,) + tuple(t[1:]))
    return out


def class_bigrams(texts, cmap):
    """class bigram counts with START and END from the training texts (add-0.1 rows)."""
    labs = ['START'] + CLS + ['END']; li = {c: i for i, c in enumerate(labs)}
    B = np.zeros((len(labs), len(labs)))
    for t in texts:
        x, clean = t[0], t[1]
        cs = [cmap.get(a, 'PERSONAL') for a in x]
        for a, b in zip(cs, cs[1:]): B[li[a], li[b]] += 1
        if clean: B[0, li[cs[0]]] += 1; B[li[cs[-1]], -1] += 1
    B = B + 0.1
    return np.log(B / B.sum(1, keepdims=True)), li


def best_classes(texts, occ, labels, ngroups, s):
    """scheme S2: each variant joins the v2 class (among the 14) that best fits its own neighbours' classes, training only."""
    LB, li = class_bigrams(texts, {a: base_of(a) for t in texts for a in t[0]})
    out = []
    Nc = np.zeros(len(CLS))                      # training tokens now in each class (the sign itself left out)
    for tt in texts:
        for a in tt[0]:
            if a != s and a not in UNK: Nc[CLS.index(base_of(a))] += 1
    for g in range(ngroups):
        nv = sum(1 for l in labels if l == g)
        score = nv * np.log(nv / (Nc + nv)) if nv else np.zeros(len(CLS))   # cost of picking this variant out of its class
        for (ti, i), l in zip(occ, labels):
            if l != g: continue
            x, clean = texts[ti][0], texts[ti][1]
            lc = 'START' if i == 0 and clean else None if i == 0 or x[i - 1] in UNK else base_of(x[i - 1])
            rc = 'END' if i == len(x) - 1 and clean else None if i == len(x) - 1 or x[i + 1] in UNK else base_of(x[i + 1])
            for ci, c in enumerate(CLS):
                if lc is not None: score[ci] += LB[li[lc], li[c]]
                if rc is not None: score[ci] += LB[li[c], li[rc]]
        out.append(CLS[int(score.argmax())])
    return out


def build(texts_exp, vocab_exp_base, variants, vclass, scheme, pooled):
    """fit the frame on relabelled training texts. variants: list of tokens; vclass: their classes (S2) or None (S1)."""
    vocab = sorted({a for t in texts_exp for a in t[0] if a not in UNK}); idx = {a: i for i, a in enumerate(vocab)}
    C, CK = kind_counts(texts_exp, idx)
    cmap = {a: base_of(a) for a in vocab}
    for v, c in zip(variants, vclass if scheme == 'S2' else [f'SOLO_{v}' for v in variants]): cmap[v] = c
    m = class_model_kind(C, CK, cmap, 'split', vocab, pooled_only=pooled)
    return m, vocab, idx


def fit_plain(texts, pooled, singleton=None):
    """the unsplit frame; singleton = sign made its own one-sign class (U1)."""
    vocab, idx = vocab_of(texts); C, CK = kind_counts(texts, idx)
    cmap = {a: base_of(a) for a in vocab}
    if singleton in cmap: cmap[singleton] = f'SOLO_{singleton}'
    return class_model_kind(C, CK, cmap, 'plain', vocab, pooled_only=pooled), vocab, idx


def score_lattice(model, idx, lines, s, variants):
    """lines: (tokens, kind) of ORIGINAL signs. Occurrences of s may be any of its variants (summed over). Returns (sum log2 p, n signs)
    per line as arrays. variants=[] -> plain scoring."""
    lps = []; ns = []
    vid = [idx[v] for v in variants]
    for x, k in lines:
        m = model.get(k)
        cand = [vid if (a == s and vid) else [idx[a]] for a in x]
        al = np.array([m.start[c] for c in cand[0]])
        for t in range(1, len(x)):
            nxt = cand[t]
            al = al @ m.trans[np.ix_(cand[t - 1], nxt)]
        p = float((al * m.end[cand[-1]]).sum())
        lps.append(np.log2(p)); ns.append(len(x))
    return np.array(lps), np.array(ns)
