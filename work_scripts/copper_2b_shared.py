#!/usr/bin/env python3
"""COPPER step 2b: when one picture goes with several different texts, do those texts share signs?

Unit: a distinct complete copper text with a picture label (its majority label). Pairs of texts with the same picture
against pairs with different pictures: share of pairs that have at least one sign in common, leaving out the jar 740,
number signs and lost signs. Control: picture labels dealt at random among the texts, 10,000 deals.
Two label sources, kept apart: A (eye, else first-catalogue specific code; unclear quadruped left out) and B (second
catalogue field-symbol family: the first two of its three digits).

Prediction written 2026-11-17 before the numbers:
 P2b.1 Same-picture text pairs share a sign at least twice as often as different-picture pairs, in both sources, P < 0.01.
 P2b.2 The shared signs are name signs (frame v2 CREST / PERSONAL / AFTER_M), not counted things or measures.
Writes work_data/copper/shared_pairs.csv and log_2b.txt.
"""
import sys; sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from copper_common import *
say = say_to(f'{OUT}/log_2b.txt')
L = pd.read_csv(f'{OUT}/objects.csv', dtype=str).fillna('')
Mm = pd.read_csv(f'{OUT}/m77_objects.csv', dtype=str).fillna('')
SKIP = {'740', '000'} | set(NUM)
A = L[(L.pic_src.isin(['eye', 'catalogue'])) & ~L.pic.isin({'quadruped', ''}) & ~L.text.str.contains('000')]
B = Mm[(Mm.fs != '') & ~Mm.text.str.contains('000') & ~Mm.text.str.contains('X')].copy(); B['pic'] = B.fs.str.zfill(3).str[:2]
rng = np.random.default_rng(11)
rows = []
for nm, D, col in (('A', A, 'text'), ('B', B, 'text')):
    lab = D.groupby(col).pic.agg(lambda s: collections.Counter(s).most_common(1)[0][0])
    T = list(lab.index); P = np.array(lab.values)
    S = [set(t.split('-')) - SKIP for t in T]
    share = np.array([[len(S[i] & S[j]) > 0 for j in range(len(T))] for i in range(len(T))])
    iu = np.triu_indices(len(T), 1)
    def rate(P):
        same = (P[:, None] == P[None, :])[iu]; sh = share[iu]
        return sh[same].mean(), sh[~same].mean(), same.sum()
    rs, rd, ns = rate(P)
    sims = np.array([rate(rng.permutation(P))[0] for _ in range(10000)])
    say(f'[{nm}] texts {len(T)}, pictures {len(set(P))}; same-picture pairs {ns}: share a sign {rs:.3f}; '
        f'different-picture pairs {rd:.3f}; random deals same-picture mean {sims.mean():.3f}; P {np.mean(sims >= rs):.4f}')
    # redesign written after the first run: copies that are variants of one text (half or more of their signs in
    # common) are left out, so only pairs of genuinely different texts count
    W = [set(t.split('-')) for t in T]
    var = np.array([[len(W[i] & W[j]) / len(W[i] | W[j]) >= 0.5 for j in range(len(T))] for i in range(len(T))])
    keep = ~var[iu]
    def rate2(P):
        same = (P[:, None] == P[None, :])[iu][keep]; sh = share[iu][keep]
        return (sh[same].mean() if same.any() else 0), sh[~same].mean(), same.sum(), sh[same].sum()
    r2, d2, n2, k2 = rate2(P)
    s2 = np.array([rate2(rng.permutation(P))[0] for _ in range(10000)])
    say(f'    different texts only: same-picture pairs {n2}, sharing a sign {k2} ({r2:.3f}); different-picture {d2:.3f}; '
        f'random mean {s2.mean():.3f}; P {np.mean(s2 >= r2):.4f}')
    for i, j in zip(*iu):
        if P[i] == P[j]:
            common = sorted(S[i] & S[j])
            rows.append(dict(source=nm, picture=P[i], text_a=T[i], text_b=T[j], shared=' '.join(common),
                             jobs=' '.join(job(s) for s in common)))
X = pd.DataFrame(rows); X.to_csv(f'{OUT}/shared_pairs.csv', index=False)
for r in X.itertuples(): say(f'   [{r.source}] {r.picture}: {r.text_a} | {r.text_b} -> shared {r.shared or "-"} ({r.jobs})')
jc = collections.Counter(j for js in X.jobs for j in js.split())
say('jobs of shared signs:', dict(jc))
