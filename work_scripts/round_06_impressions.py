#!/usr/bin/env python3
"""ROUND SEALS, step 6: do round-seal texts share a whole text or a sign pair with any clay impression (work_data/stamps/impressions.csv, 336 faces, home sites)?
Written 2026-11-17. No word on any sign. Round texts: the 41 faces (the Daimabad seal included; it has one sign). Impression texts: reading order, as stored.
Measures: (1) same complete text (all signs, same order); (2) an ordered adjacent pair (two usable signs side by side, same order) found in an impression;
(3) the same pair in either order. CONTROL: for each round text a length-matched home square-seal text (same token count), 2,000 draws; pair-sharing counted the same way.
Also: which abroad vs home round texts. PREDICTION (written now): round seals share no whole text with an impression and fewer ordered pairs than square seals do
(impressions are home administrative objects; the round texts are not home phrases): round pair-sharing texts <= 40% of the square draw mean.
Output: work_data/round/impressions_shared.csv, log_6.txt
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abroad4_common import *
OUTR = f'{ROOT}/work_data/round'
RL = pd.read_csv(f'{OUTR}/round_list.csv', dtype=str)
im = pd.read_csv(f'{ROOT}/work_data/stamps/impressions.csv', dtype=str).fillna('')
IT = [tuple(s.split('-')) for s in im.signs if s]
ipairs = set(); iunord = set(); ifull = set(IT)
for t in IT:
    for a, b in zip(t, t[1:]):
        if real(a) and real(b): ipairs.add((a, b)); iunord.add(frozenset((a, b)))
print('impression texts', len(IT), 'ordered pairs', len(ipairs))
def P(t): return [(a, b) for a, b in zip(t, t[1:]) if real(a) and real(b)]
def share(t):
    ps = P(t)
    return dict(full=int(t in ifull and len(t) >= 2 and all(real(s) for s in t)), ordered=int(any(p in ipairs for p in ps)), either=int(any(frozenset(p) in iunord for p in ps)),
                n_ordered=sum(p in ipairs for p in ps))
rt = {r.id: tuple(d.set_index('id').loc[r.id, 'tok']) for r in RL.itertuples()}
rt2 = {i: t for i, t in rt.items() if len(t) >= 2}
rows = []
for i, t in rt2.items():
    s = share(t); s.update(id=i, tier=RL.set_index('id').tier[i], text='-'.join(t)); rows.append(s)
R = pd.DataFrame(rows); R.to_csv(f'{OUTR}/impressions_shared.csv', index=False)
print('round texts with 2+ tokens:', len(R)); print(R[['full', 'ordered', 'either']].sum())
print(R[R.ordered > 0][['id', 'tier', 'text', 'n_ordered']])
# which impressions hold the shared pairs
for i in R[R.ordered > 0].id:
    t = rt[i]
    for p in P(t):
        if p in ipairs:
            hits = [(f, s, site) for f, s, site in zip(im.face, im.signs, im.site) if s and any((a, b) == p for a, b in zip(s.split('-'), s.split('-')[1:]))]
            print(i, '-'.join(p), 'in', len(hits), 'impressions e.g.', hits[:3])
# control
sq = F[(F.tier == 'home') & (F.kind == 'seal') & (~F['round'])]
pool = collections.defaultdict(list)
for x in set(sq.tok):
    if len(x) >= 2: pool[len(x)].append(x)
rng = np.random.default_rng(66)
ctrl = {k: [] for k in ('full', 'ordered', 'either')}
for _ in range(2000):
    tot = {k: 0 for k in ctrl}
    for t in rt2.values():
        c = pool[min(len(t), max(pool))]; s = share(c[rng.integers(len(c))])
        for k in tot: tot[k] += s[k]
    for k in ctrl: ctrl[k].append(tot[k])
for k in ctrl:
    a = np.array(ctrl[k]); print(k, 'round real', int(R[k].sum()), 'square matched mean %.2f' % a.mean(), 'range', np.percentile(a, [2.5, 97.5]), 'P round lower %.4f' % ((np.sum(a <= R[k].sum()) + 1) / 2001))
