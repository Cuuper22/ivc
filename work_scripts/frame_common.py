#!/usr/bin/env python3
"""Shared kit for the frame-by-machine job (frame_*.py).

Everything here is FIXED before any score is computed (written 2026-11-17, before frame_classes.py / frame_predict.py ran):

DATA
  Training = the first catalogue (Lipi, 5,679 faces), reading order (stored order reversed, as gloss.load does).
  Models are trained on DISTINCT texts (identical token strings counted once), so that moulded copies of one tablet
  do not dominate. '000' (lost sign) and 'ALT' (unclear reading) are unknown tokens: never counted as signs.
  Start and end of text are counted only on faces with no broken edge and no lost or unclear sign.
  New texts = second-catalogue (Mahadevan 1977) lines with no partner in the first catalogue, complete, no lost sign,
  every sign mapped to a Lipi number (no 'X' signs), and every sign seen in training (texts with an unseen sign are
  dropped for every model alike).

HAND JOBS (the frame built by the hand parser, gloss2.parse_face roles, all Lipi faces)
  per token: opener -> OPENER; crest -> CREST; self -> PERSONAL; tag -> TAG;
             poss / relation / ending / tail / load-carried -> END (ending or title);
             counted with its count AFTER it -> MEASURE; counted with its count BEFORE it, load-crop, load-thing -> THING;
             count / load-count -> NUMBER; lost -> ignored.
  per sign: the most common token job; then three fixed overrides:
             stroke and comb count signs (gloss2.CNT) -> NUMBER; 060 -> JOINER;
             PLACE_TIME signs (below) -> PLACE (place or time word) unless their token majority is OPENER.
  PLACE_TIME is the hand frame's place/time set from the sound passes (month, day, season, town, field, hedge, land,
  quarter, paddy field, threshing floor). It is the only job the parser has no rule for.

MODELS (each gives a start vector, a sign-to-sign transition matrix and an end vector over the training vocabulary,
so scoring and gap filling run the same code for all):
  unigram      P(s) add-0.5; end = 1/(mean length + 1) share.
  bigram       Witten-Bell interpolation with the unigram (no tuning).
  class(map)   hard class map c(s): P(s_i | s_{i-1}) = P(c_i | c_{i-1}) * P(s_i | c_i); class transitions add-0.1,
               emissions add-0.5 inside the class.
  hmm          soft hidden-state model (Baum-Welch), forward probability.
  mix(map)     0.5 * bigram + 0.5 * class(map), fixed weight.
"""
import sys, os, collections, time, re
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = '/home/antigravity/Cuuper22/ivc'
OUT = f'{ROOT}/work_data/frame'
os.makedirs(OUT, exist_ok=True)
T0 = time.time()


def log(*a):
    print(f'[{time.time() - T0:7.1f}s]', *a, flush=True)


from sound_v3_common import d, M, lex, pairs, kind_L, CNT  # noqa: E402  (loads both catalogues, parses with gloss2)

UNK = {'000', 'ALT'}
JOBS = ['OPENER', 'CREST', 'PERSONAL', 'TAG', 'END', 'MEASURE', 'THING', 'PLACE', 'JOINER', 'NUMBER']
JOB_PLAIN = {'OPENER': 'opener', 'CREST': 'family crest', 'PERSONAL': 'personal name part', 'TAG': 'name tag',
             'END': 'ending or title', 'MEASURE': 'measure', 'THING': 'counted thing', 'PLACE': 'place or time word',
             'JOINER': 'joiner', 'NUMBER': 'number'}
PLACE_TIME = {'900', '904', '165', '201', '335', '503', '615', '519', '845', '061', '421', '422', '423', '424', '554'}
KIND5 = {'seal': 'seals', 'mtab': 'tablets', 'tag': 'tags and sealings', 'pot': 'pots', 'ctab': 'copper tablets'}


# ------------------------------------------------------------------ hand jobs
def token_jobs(x, R):
    out = []
    for i, (s, r) in enumerate(zip(x, R)):
        if r == 'lost' or s in UNK: out.append(None); continue
        if r == 'opener': j = 'OPENER'
        elif r == 'crest': j = 'CREST'
        elif r == 'self': j = 'PERSONAL'
        elif r == 'tag': j = 'TAG'
        elif r in ('poss', 'relation', 'ending', 'tail', 'load-carried'): j = 'END'
        elif r in ('count', 'load-count'): j = 'NUMBER'
        elif r in ('load-crop', 'load-thing'): j = 'THING'
        elif r == 'counted':
            after = i + 1 < len(x) and R[i + 1] == 'count'
            j = 'MEASURE' if after else 'THING'
        else: j = 'PERSONAL'
        out.append(j)
    return out


def hand_jobs():
    cnt = collections.defaultdict(collections.Counter)
    for x, R in zip(d.tok, d.R):
        for s, j in zip(x, token_jobs(x, R)):
            if j: cnt[s][j] += 1
    job = {}
    for s, c in cnt.items():
        top = c.most_common(1)[0][0]
        if s in CNT: top = 'NUMBER'
        elif s == '060': top = 'JOINER'
        elif s in PLACE_TIME and top != 'OPENER': top = 'PLACE'
        job[s] = top
    return job, cnt


HAND, HAND_TOKCOUNT = hand_jobs()


# ------------------------------------------------------------------ training texts
def train_texts(exclude_ids=frozenset()):
    """distinct Lipi texts: list of (tokens, clean) where clean = start and end may be counted; plus kind of first copy."""
    seen = {}
    for i, x, f, k in zip(d.id, d.tok, d.flg, d.kind):
        if i in exclude_ids or not x: continue
        clean = not (f & {'broken', 'lost', 'alt'}) and not (set(x) & UNK)
        if x not in seen: seen[x] = (clean, k)
    return [(x, c, k) for x, (c, k) in seen.items()]


def vocab_of(texts):
    v = sorted({s for x, c, k in texts for s in x if s not in UNK})
    return v, {s: i for i, s in enumerate(v)}


def counts(texts, idx):
    V = len(idx)
    uni = np.zeros(V); big = np.zeros((V, V)); st = np.zeros(V); en = np.zeros(V); nclean = 0; ntok_clean = 0
    for x, clean, k in texts:
        ids = [idx.get(s) for s in x]
        for a in ids:
            if a is not None: uni[a] += 1
        for a, b in zip(ids, ids[1:]):
            if a is not None and b is not None: big[a, b] += 1
        if clean:
            st[ids[0]] += 1; en[ids[-1]] += 1; nclean += 1; ntok_clean += len(ids)
    return dict(uni=uni, big=big, st=st, en=en, nclean=nclean, ntok_clean=ntok_clean)


class SeqModel:
    """start (V), trans (V x V, rows sum with end to 1), end (V)."""
    def __init__(self, name, start, trans, end):
        self.name, self.start, self.trans, self.end = name, start, trans, end

    def logprob(self, ids, use_end=True):
        lp = np.log2(self.start[ids[0]])
        for a, b in zip(ids, ids[1:]): lp += np.log2(self.trans[a, b])
        if use_end: lp += np.log2(self.end[ids[-1]])
        return lp


def unigram_model(C):
    V = len(C['uni'])
    p = (C['uni'] + 0.5) / (C['uni'].sum() + 0.5 * V)
    pe = C['nclean'] / (C['ntok_clean'] + C['nclean'])
    return SeqModel('unigram', p.copy(), np.tile(p * (1 - pe), (V, 1)), np.full(V, pe))


def bigram_model(C):
    V = len(C['uni'])
    pu = (C['uni'] + 0.5) / (C['uni'].sum() + 0.5 * V)
    # end handled as an extra symbol column; follower counts include end on clean texts
    B = np.concatenate([C['big'], C['en'][:, None]], axis=1)
    pe_u = C['nclean'] / (C['ntok_clean'] + C['nclean'])
    PU = np.concatenate([pu * (1 - pe_u), [pe_u]])
    n = B.sum(1); T = (B > 0).sum(1)
    lam = np.where(n > 0, n / np.maximum(n + T, 1), 0.0)
    P = lam[:, None] * (B / np.maximum(n, 1)[:, None]) + (1 - lam)[:, None] * PU[None, :]
    st = (C['st'] + 0.5 * pu * V * 0.0 + 0.5) / (C['st'].sum() + 0.5 * V)
    stn = C['st'].sum(); stT = (C['st'] > 0).sum(); ls = stn / (stn + stT)
    st = ls * C['st'] / stn + (1 - ls) * pu
    return SeqModel('bigram', st, P[:, :V], P[:, V])


def class_model(C, cmap, name, vocab):
    """cmap: dict sign -> class label. Signs of the vocabulary missing from cmap get their own class 'UNSEEN'."""
    V = len(vocab)
    labs = sorted({cmap.get(s, 'UNSEEN') for s in vocab})
    li = {c: i for i, c in enumerate(labs)}; K = len(labs)
    cid = np.array([li[cmap.get(s, 'UNSEEN')] for s in vocab])
    Z = np.zeros((V, K)); Z[np.arange(V), cid] = 1
    cu = C['uni'] @ Z
    cb = Z.T @ C['big'] @ Z
    ce = C['en'] @ Z; cs = C['st'] @ Z
    # emissions inside class, add-0.5
    em = (C['uni'] + 0.5) / ((cu + 0.5 * Z.sum(0))[cid])
    rows = np.concatenate([cb, ce[:, None]], axis=1) + 0.1
    rows = rows / rows.sum(1, keepdims=True)
    ctrans, cend = rows[:, :K], rows[:, K]
    cstart = (cs + 0.1) / (cs.sum() + 0.1 * K)
    trans = ctrans[cid][:, cid] * em[None, :]
    return SeqModel(name, cstart[cid] * em, trans, cend[cid]), dict(labs=labs, cid=cid, ctrans=ctrans, cend=cend, cstart=cstart, em=em, cu=cu, cb=cb, ce=ce, cs=cs)


def mix_model(a, b, w=0.5, name=None):
    return SeqModel(name or f'mix({a.name},{b.name})', w * a.start + (1 - w) * b.start, w * a.trans + (1 - w) * b.trans, w * a.end + (1 - w) * b.end)


# ------------------------------------------------------------------ hidden-state model (batched Baum-Welch)
def pad(seqs, idx):
    L = max(len(x) for x in seqs); N = len(seqs)
    O = np.full((N, L), -1); mask = np.zeros((N, L), bool)
    for n, x in enumerate(seqs):
        for t, s in enumerate(x):
            mask[n, t] = True; O[n, t] = idx.get(s, -2)   # -2 = unknown token (lost / unclear): emission 1
    return O, mask


class HMM:
    def __init__(self, K, V, seed):
        r = np.random.default_rng(seed)
        self.K, self.V = K, V
        self.pi = r.dirichlet(np.ones(K)); self.A = r.dirichlet(np.ones(K + 1), size=K)   # last column = end
        self.B = r.dirichlet(np.ones(V) * 0.5, size=K)

    def _emit(self, O, mask):
        N, L = O.shape
        E = np.ones((N, L, self.K))
        known = O >= 0
        E[known] = self.B[:, O[known]].T
        E[~mask] = 1.0
        return E

    def forward_backward(self, O, mask, clean):
        N, L = O.shape; K = self.K; A = self.A[:, :K]; end = self.A[:, K]
        E = self._emit(O, mask); lens = mask.sum(1)
        al = np.zeros((N, L, K)); sc = np.zeros((N, L))
        a = self.pi[None, :] * E[:, 0]; s = a.sum(1); al[:, 0] = a / s[:, None]; sc[:, 0] = s
        for t in range(1, L):
            a = (al[:, t - 1] @ A) * E[:, t]
            act = mask[:, t]
            s = np.where(act, a.sum(1), 1.0)
            al[:, t] = np.where(act[:, None], a / s[:, None], al[:, t - 1]); sc[:, t] = s
        # end factor on clean texts only
        endf = np.where(clean[:, None], end[None, :], 1.0)
        last = al[np.arange(N), lens - 1]
        zend = (last * endf).sum(1)
        ll = np.log(sc).sum(1) + np.log(zend)
        be = np.zeros((N, L, K))
        be[np.arange(N), lens - 1] = endf / zend[:, None]
        for t in range(L - 2, -1, -1):
            act = mask[:, t + 1]
            b = (A @ (E[:, t + 1] * be[:, t + 1]).T).T / sc[:, t + 1][:, None]
            be[:, t] = np.where(act[:, None], b, be[:, t])
        gam = al * be; gam *= mask[:, :, None]
        return al, be, sc, E, ll, gam, endf, zend

    def fit(self, O, mask, clean, iters=150, tol=1e-4, verbose=None):
        prev = -np.inf; N, L = O.shape; K = self.K
        for it in range(iters):
            al, be, sc, E, ll, gam, endf, zend = self.forward_backward(O, mask, clean)
            tot = ll.sum()
            # xi sums
            A = self.A[:, :K]
            xi = np.zeros((K, K))
            for t in range(L - 1):
                act = mask[:, t + 1]
                if not act.any(): continue
                x = al[act, t][:, :, None] * A[None] * (E[act, t + 1] * be[act, t + 1])[:, None, :] / sc[act, t + 1][:, None, None]
                xi += x.sum(0)
            lens = mask.sum(1)
            lastg = gam[np.arange(N), lens - 1]
            endc = (lastg * clean[:, None]).sum(0)
            stayc = gam.sum((0, 1)) - 0  # total occupancy
            newA = np.concatenate([xi, endc[:, None]], 1) + 1e-3
            self.A = newA / newA.sum(1, keepdims=True)
            self.pi = gam[:, 0].sum(0) + 1e-3; self.pi /= self.pi.sum()
            Bn = np.full((K, self.V), 1e-3)
            known = (O >= 0) & mask
            np.add.at(Bn.T, O[known], gam[known])
            self.B = Bn / Bn.sum(1, keepdims=True)
            if verbose and it % 25 == 0: verbose(f'      iter {it:3d}  log-lik {tot:.1f}')
            if tot - prev < tol * abs(tot): break
            prev = tot
        return tot

    def sign_state_counts(self, O, mask, clean):
        _, _, _, _, _, gam, _, _ = self.forward_backward(O, mask, clean)
        Cn = np.zeros((self.V, self.K)); known = (O >= 0) & mask
        np.add.at(Cn, O[known], gam[known])
        return Cn

    def logprob2(self, O, mask):
        """log2 probability of complete sequences (end counted)."""
        clean = np.ones(len(O), bool)
        return self.forward_backward(O, mask, clean)[4] / np.log(2)


# ------------------------------------------------------------------ gap filling on any SeqModel
def gap_posteriors(m, ids, clean_edges):
    """ids: list of int (known) or None (lost). Returns {pos: posterior over vocab} via forward-backward on the sign chain."""
    V = len(m.start); n = len(ids)
    def ob(t):
        if ids[t] is None: return np.ones(V)
        v = np.zeros(V); v[ids[t]] = 1; return v
    st = m.start if clean_edges else np.ones(V)
    en = m.end if clean_edges else np.ones(V)
    al = [st * ob(0)]; al[0] = al[0] / al[0].sum()
    for t in range(1, n):
        a = (al[-1] @ m.trans) * ob(t); al.append(a / a.sum())
    be = [None] * n; be[-1] = en.copy()
    for t in range(n - 2, -1, -1):
        b = m.trans @ (ob(t + 1) * be[t + 1]); be[t] = b / b.sum()
    out = {}
    for t in range(n):
        if ids[t] is None:
            p = al[t] * be[t]; out[t] = p / p.sum()
    return out


def freq_band(counter, nb=10):
    """sign -> band index by training frequency (equal-sized bands over signs sorted by count, ties kept together)."""
    items = sorted(counter.items(), key=lambda kv: (kv[1], kv[0]))
    out = {}; per = len(items) / nb
    for r, (s, c) in enumerate(items): out[s] = min(int(r / per), nb - 1)
    # keep ties in one band: use the band of the first sign with that count
    first = {}
    for s, c in items: first.setdefault(c, out[s])
    return {s: first[c] for s, c in items}


def deal_within_bands(labels, band, seed):
    """move the labels among signs of the same frequency band (a decoy frame)."""
    r = np.random.default_rng(seed); out = {}
    by = collections.defaultdict(list)
    for s in labels: by[band.get(s, -1)].append(s)
    for b, ss in by.items():
        lab = [labels[s] for s in ss]; perm = r.permutation(len(ss))
        for s, q in zip(ss, perm): out[s] = lab[q]
    return out
