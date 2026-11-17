#!/usr/bin/env python3
"""The missing link for the tree signs: the second catalogue (Mahadevan) draws Lipi's three branched trees
405 / 406 / 407 as one sign (M169), so 407 never shows up on the new texts.  This builds the split from raw
material: on the second-catalogue texts that have a first-catalogue partner of the same length, the Lipi partner
says which tree each M169 is; a small naive-Bayes rule learns it from what FOLLOWS the tree (next sign, sign two
after, end of text) only, so tests on the count BEFORE the tree and on the object kind stay independent of the rule.
It is checked by leave-one-out on the partnered texts, then applied to the new texts.
Import: from sound_v5_link import relabel_trees  (changes M.tok in place for unpartnered rows; returns a report)."""
import collections, math
from sound_v5_common import *
TREES = ('405', '406', '407')


def _feats(x, i):
    y = tuple(x) + ('$', '$')
    return [('n1', y[i + 1]), ('n2', y[i + 2]), ('len', min(len(x), 6))]


def _train_rows():
    rows = []
    for lt, mt in zip(pairs.lipi_text, pairs.mahadevan_text):
        L = lt.split('-'); Mm = mt.split('-')
        if len(L) != len(Mm): continue
        Lt = tuple(L)
        for i, (a, b) in enumerate(zip(L, Mm)):
            if b == '169' and a in TREES:
                rows.append((a, _feats(Lt, i), lt))
    return rows


def _fit(rows):
    cls = collections.Counter(r[0] for r in rows); fc = collections.defaultdict(collections.Counter)
    for c, f, _ in rows:
        for k in f: fc[c][k] += 1
    return cls, fc


def _pred(model, f):
    cls, fc = model; tot = sum(cls.values()); best = None
    for c in cls:
        lp = math.log(cls[c] / tot) + sum(math.log((fc[c][k] + 0.5) / (cls[c] + 1.0)) for k in f)
        if best is None or lp > best[0]: best = (lp, c)
    return best[1]


def link_check():
    rows = _train_rows(); ok = 0; n = 0; base = collections.Counter(r[0] for r in rows).most_common(1)[0][1]
    texts = sorted(set(r[2] for r in rows))
    for t in texts:
        tr = [r for r in rows if r[2] != t]; te = [r for r in rows if r[2] == t]
        m = _fit(tr)
        for c, f, _ in te: n += 1; ok += _pred(m, f) == c
    return dict(train=len(rows), texts=len(texts), loo_correct=ok, of=n, majority=base, by_class=dict(collections.Counter(r[0] for r in rows)))


def relabel_trees():
    rows = _train_rows(); m = _fit(rows); out = collections.Counter()
    idx = M.index[~M.partnered]
    newtok = []
    for j in idx:
        x = list(M.at[j, 'tok']); mt = M.at[j, 'reading_mah'].split('-')
        if len(mt) == len(x):
            for i, b in enumerate(mt):
                if b == '169':
                    x[i] = _pred(m, _feats(tuple(x), i)); out[x[i]] += 1
        newtok.append(tuple(x))
    M.loc[idx, 'tok'] = pd.Series(newtok, index=idx)
    return dict(out)


if __name__ == '__main__':
    print(link_check())
