#!/usr/bin/env python3
"""sense_core.py -- the scoring machinery of the sense test (numpy only).

A PROBLEM = words (each with a list of senses), units (signs; in the control, units are the words themselves), a real word for each unit,
a job class and frequency band for each unit, and texts (lists of units).  Three SENSE-SIMILARITY versions, each a number for every pair of senses:
  ov   category overlap: 1 if the two senses share at least one of the 13 categories (rule-mapped), else 0.
  lift category lift ("beats independence"): for a pair of categories (c1, c2) the log of how often units carrying c1 and units carrying c2
       sit in the same text, divided by how often independence would put them there; learned on the REAL labels of OTHER texts
       (Lipi texts split in 2 folds by object: each fold scored with lifts learned on the other fold; new texts scored with lifts learned on all Lipi).
       A pair of senses is worth the biggest lift among its category pairs (0 if either sense has no category).
  cos  meaning-vector closeness: cosine of the two sense vectors (embeddinggemma-2, vectors centred on the mean of all senses, renormalised).
TEXT SCORE (max over senses, so many-meaning words are not punished): for every sign i in a text, fit_i = the best over i's senses s of
  the average over the other signs j (carrying a different word) of the best over j's senses t of sim(s, t); text score = mean of fit_i.
  Pairs of signs that carry the same word are left out (otherwise variant signs of one word would give a free perfect match for the real list).
TOTAL SCORE = weighted mean of text scores (weights: one per physical object, split over its faces).
SHUFFLES: words dealt among signs of the same class and frequency band ('cell').  Variant B also keeps the number of senses: inside a cell, signs are
  sorted by their word's number of senses (ties random) and cut into blocks of 3; words are dealt only inside a block."""
import numpy as np, collections
CATS = ['number', 'measure', 'commodity', 'person', 'kin', 'place', 'time', 'deity', 'animal', 'plant', 'tool', 'action', 'quality']
NEG = np.float32(-1e9)

class Prob:
    def __init__(s, words, senses, emb, units, real_word, cls, band, texts, tw, tfold, lmax=10, name=''):
        """words: list of word keys; senses: dict word -> list of (phrase, cats list); emb: dict word -> array [n,D] (or None);
        units: list of unit ids; real_word: list (word key per unit); cls, band: lists per unit; texts: list of lists of unit indices;
        tw: weights; tfold: fold id per text (0,1 for cross-fit, 2 = trained on all, -1 none)."""
        s.name = name; s.words = list(words); s.widx = {w: i for i, w in enumerate(s.words)}; W = len(s.words)
        s.nsens = np.array([len(senses[w]) for w in s.words]); S = int(s.nsens.max()); s.S = S
        s.valid = np.zeros((W, S), bool); s.B = np.zeros((W, S, len(CATS)), bool)
        for i, w in enumerate(s.words):
            for k, (ph, cs) in enumerate(senses[w]):
                s.valid[i, k] = True
                for c in cs: s.B[i, k, CATS.index(c)] = True
        s.wc = s.B.any(1)                            # word-level categories
        s.E = None
        if emb is not None:
            D = next(iter(emb.values())).shape[1]; E = np.zeros((W, S, D), np.float32)
            for i, w in enumerate(s.words): E[i, :len(emb[w])] = emb[w]
            allv = E[s.valid]; mu = allv.mean(0); E = E - mu; E /= (np.linalg.norm(E, axis=2, keepdims=True) + 1e-9); E[~s.valid] = 0
            s.E = E
        s.units = list(units); U = len(s.units)
        s.real = np.array([s.widx[w] for w in real_word]); s.cls = np.array(cls); s.band = np.array(band)
        s.cell = collections.defaultdict(list)
        for u in range(U): s.cell[(s.cls[u], s.band[u])].append(u)
        # texts -> padded arrays
        L = lmax; T = len(texts); s.L = L
        X = -np.ones((T, L), int); trunc = 0
        for t, tx in enumerate(texts):
            if len(tx) > L: trunc += 1
            X[t, :min(len(tx), L)] = tx[:L]
        s.X = X; s.tw = np.array(tw, float); s.tfold = np.array(tfold); s.trunc = trunc
        s.M2 = {}
    # ---------------- similarity tables ----------------
    def lifts(s, sel):
        """category lift matrix from the texts in `sel` (bool over texts), real labels, word-level categories, different-word pairs only."""
        n = np.zeros((13, 13)); tot = 0.0; marg = np.zeros(13)
        for t in np.where(sel)[0]:
            us = [u for u in s.X[t] if u >= 0]
            for a in us:
                for b in us:
                    if a == b or s.real[a] == s.real[b]: continue
                    ca, cb = s.wc[s.real[a]], s.wc[s.real[b]]
                    w = s.tw[t]; n += w * np.outer(ca, cb); tot += w; marg += w * ca
        p = marg / max(tot, 1e-9)
        Ex = tot * np.outer(p, p)
        return np.log((n + 0.5) / (Ex + 0.5))
    def sim(s, version, Lm=None):
        W, S = len(s.words), s.S
        if version == 'cos':
            V = s.E.reshape(W * S, -1); R = V @ V.T
            R = R.reshape(W, S, W, S).astype(np.float32); R[:, :, ~s.valid] = NEG   # invalid t
            return R
        Bf = s.B.reshape(W * S, 13)
        if version == 'ov':
            R = ((Bf.astype(np.float32) @ Bf.T.astype(np.float32)) > 0).astype(np.float32).reshape(W, S, W, S)
            R[:, :, ~s.valid] = NEG; return R
        # lift
        A1 = np.full((W * S, 13), -np.inf, np.float32)
        for c1 in range(13):
            m = Bf[:, c1]
            A1[m] = np.maximum(A1[m], Lm[c1][None, :].astype(np.float32))
        R = np.full((W * S, W * S), -np.inf, np.float32)
        for c2 in range(13):
            m = Bf[:, c2]
            R[:, m] = np.maximum(R[:, m], A1[:, c2][:, None])
        R[~np.isfinite(R)] = 0
        R = R.reshape(W, S, W, S); R[:, :, ~s.valid] = NEG; return R
    def build(s, versions=('ov', 'lift', 'cos')):
        for v in versions:
            if v == 'lift':
                s.M2[v] = {}
                for f in (0, 1, 2):
                    sel = (s.tfold == f)
                    train = (s.tfold == 1 - f) if f in (0, 1) else ((s.tfold == 0) | (s.tfold == 1))
                    if not sel.any() or not train.any(): continue
                    Lm = s.lifts(train); s.M2[v][f] = np.ascontiguousarray(s.sim(v, Lm).max(3).transpose(0, 2, 1))
                    s.M2[v]['L%d' % f] = Lm
            else:
                m = np.ascontiguousarray(s.sim(v).max(3).transpose(0, 2, 1)); s.M2[v] = {f: m for f in (0, 1, 2)}
    # ---------------- scoring ----------------
    def fits(s, assign, version, rows=None):
        """assign: word index per unit. returns (fit [T,L], ok [T,L]) for all texts."""
        T, L = s.X.shape; fit = np.zeros((T, L), np.float32); ok = np.zeros((T, L), bool)
        for f, M2 in s.M2[version].items():
            if isinstance(f, str): continue
            ti = np.where(s.tfold == f)[0] if rows is None else np.intersect1d(np.where(s.tfold == f)[0], rows)
            if len(ti) == 0: continue
            X = s.X[ti]; uv = X >= 0; wi = np.where(uv, assign[np.where(uv, X, 0)], 0)
            G = M2[wi[:, :, None], wi[:, None, :], :]            # [t,i,j,s]
            pair = uv[:, :, None] & uv[:, None, :] & ~np.eye(L, dtype=bool)[None] & (wi[:, :, None] != wi[:, None, :])
            cnt = pair.sum(2)                                      # [t,i]
            num = (G * pair[..., None]).sum(2)                     # [t,i,s]
            avg = num / np.maximum(cnt, 1)[..., None]
            avg = np.where(s.valid[wi][:, :, :], avg, NEG)
            best = avg.max(2)
            fit[ti] = best; ok[ti] = cnt > 0
        return fit, ok
    def total(s, fit, ok, group=None, unit_sel=None):
        """returns (text-weighted mean of text scores) and per-unit sums."""
        tsc = (fit * ok).sum(1) / np.maximum(ok.sum(1), 1); has = ok.any(1)
        w = s.tw * has
        if group is not None: w = w * group
        tot = (tsc * w).sum() / max(w.sum(), 1e-9)
        out = {'all': tot}
        if unit_sel is not None:                                   # mean of fits of the selected signs' occurrences
            m = ok & np.isin(s.X, np.where(unit_sel)[0]); ww = s.tw[:, None] * m * (group[:, None] if group is not None else 1)
            out['sub'] = (fit * ww).sum() / max(ww.sum(), 1e-9)
        return out
    def unit_means(s, fit, ok, group):
        """per-unit weighted mean fit over the unit's occurrences in the texts of `group`."""
        U = len(s.units); m = ok & (s.X >= 0); ww = s.tw[:, None] * m * group[:, None]
        num = np.bincount(np.where(m, s.X, 0).ravel(), weights=(fit * ww).ravel(), minlength=U)
        den = np.bincount(np.where(m, s.X, 0).ravel(), weights=ww.ravel(), minlength=U)
        return num / np.maximum(den, 1e-9), den
    # ---------------- shuffles ----------------
    def shuffle(s, rng, matched=False, block=3):
        asg = s.real.copy()
        for k, us in s.cell.items():
            us = np.array(us)
            if not matched:
                asg[us] = s.real[us][rng.permutation(len(us))]
            else:
                key = s.nsens[s.real[us]] + rng.random(len(us)) * 0.5
                us = us[np.argsort(key)]; n = len(us); off = rng.integers(0, block)
                bounds = [0] + list(range(off if off > 0 else block, n, block)) + [n]
                bounds = sorted(set(b for b in bounds if 0 <= b <= n))
                if len(bounds) > 2 and bounds[-1] - bounds[-2] < 2: bounds.pop(-2)
                for a, b in zip(bounds[:-1], bounds[1:]):
                    blk = us[a:b]; asg[blk] = s.real[blk][rng.permutation(len(blk))]
        return asg
