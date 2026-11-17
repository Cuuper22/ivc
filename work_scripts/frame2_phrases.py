#!/usr/bin/env python3
"""FRAME v2, step 3: where the order no class explains lives (the fixed phrases). Fixed before running (2026-11-17):

  Corpus: distinct first-catalogue texts. Class grammar = v2 base, pooled (the explicit 14-class grammar), and the sign
  bigram (frame_common recipe), both fitted on that corpus.
  PAIR gain = n(a,b) * log2( P_bigram(b|a) / P_v2(b|a) ): the bits the pair saves over the class grammar across the corpus.
  Pairs with n >= 4 distinct texts; top 40 by gain = the fixed pairs.
  TRIPLE gain = n(a,b,c) * log2( P_ml(b|a) P_ml(c|a,b) / (P_v2(b|a) P_v2(c|b)) ), n >= 4; top 40 = the fixed triples;
  also listed: how much of it is beyond its two pairs (n * log2 P_ml(c|a,b) / P_bigram(c|b)).
  DECOY 1: the same ranking on the corpus with sign order shuffled inside each text (20 shuffles): number of decoy pairs
  whose gain reaches the real 40th pair's gain.
  HELD-OUT CHECK on the 482 new texts: observed count of the top-40 pairs against the count expected under the v2 grammar
  (sum over each position of P_v2(b|a)); DECOY 2: the same for the top-40 pairs of each shuffled corpus.
  WHERE THE REST LIVES: on the new texts, the bigram's saving over v2 (bits) summed over tokens whose (previous, current)
  pair is among the top 40 / top 200 fixed pairs, as a share of the total saving.
Output: work_data/frame/fixed_pairs.csv, fixed_triples.csv, log_phrases.txt
"""
from frame2_common import *
from frame2_pictures import pic

c2 = pd.read_csv(f'{OUT2}/classes_v2.csv', dtype=str).fillna('')
V2B = dict(zip(c2.sign, c2.v2_base))
T = train_texts(); vocab, idx = vocab_of(T)


def fit(texts):
    C = counts(texts, idx)
    m = class_model(C, {s: V2B.get(s, 'PERSONAL') for s in vocab}, 'v2', vocab)[0]
    return C, m, bigram_model(C)


def pair_table(texts, C, m, big, nmin=4):
    n2 = collections.Counter(); n3 = collections.Counter()
    for x, c, k in texts:
        for a, b in zip(x, x[1:]):
            if a in idx and b in idx: n2[(a, b)] += 1
        for a, b, cc in zip(x, x[1:], x[2:]):
            if a in idx and b in idx and cc in idx: n3[(a, b, cc)] += 1
    rows = []
    for (a, b), n in n2.items():
        if n < nmin: continue
        i, j = idx[a], idx[b]
        rows.append(dict(a=a, b=b, n=n, p_bigram=big.trans[i, j], p_v2=m.trans[i, j], gain=n * np.log2(big.trans[i, j] / m.trans[i, j]),
                         share_of_a=n / C['uni'][i], share_of_b=n / C['uni'][j]))
    P = pd.DataFrame(rows).sort_values('gain', ascending=False)
    rows = []
    for (a, b, cc), n in n3.items():
        if n < nmin: continue
        i, j, k = idx[a], idx[b], idx[cc]
        pml_b = n2[(a, b)] / C['uni'][i]; pml_c = n / n2[(a, b)]
        rows.append(dict(a=a, b=b, c=cc, n=n, gain=n * np.log2(pml_b * pml_c / (m.trans[i, j] * m.trans[j, k])),
                         beyond_pairs=n * np.log2(pml_c / big.trans[j, k])))
    Q = pd.DataFrame(rows).sort_values('gain', ascending=False)
    return P, Q


C, m, big = fit(T)
P, Q = pair_table(T, C, m, big)
top = P.head(40).copy(); g40 = top.gain.iloc[-1]
log(f'pairs with 4+ texts: {len(P)}; 40th fixed pair gain {g40:.1f} bits')
NEW, _, _ = new_texts(idx)


def heldout(pairs_set, model):
    obs = 0; exp = 0.0
    for x, k in NEW:
        for a, b in zip(x, x[1:]):
            if (a, b) in pairs_set: obs += 1
            # expected: for each position with previous sign a such that some (a, .) is in the set
        for a, b in zip(x, x[1:]):
            for (pa, pb) in pairs_set:
                if pa == a: exp += model.trans[idx[a], idx[pb]]
    return obs, exp


toppairs = set(zip(top.a, top.b))
obs, exp = heldout(toppairs, m)
log(f'new texts: the 40 fixed pairs occur {obs} times against {exp:.1f} expected under the v2 grammar ({obs / exp:.1f} times)')
rng = np.random.default_rng(77); dec = []
for q in range(20):
    Ts = [(tuple(rng.permutation(list(x))), c, k) for x, c, k in T]
    Cs, ms, bs = fit(Ts)
    Ps, _ = pair_table(Ts, Cs, ms, bs)
    ds = set(zip(Ps.head(40).a, Ps.head(40).b))
    o, e = heldout(ds, m)
    dec.append(dict(shuffle=q, pairs_reaching_real_40th=int((Ps.gain >= g40).sum()), top_gain=Ps.gain.iloc[0], new_obs=o, new_exp=e))
D = pd.DataFrame(dec)
log(f'DECOY order-shuffled corpora: pairs reaching the real 40th gain: mean {D.pairs_reaching_real_40th.mean():.1f}, max {D.pairs_reaching_real_40th.max()}; '
    f'their top-40 pairs on new texts: {D.new_obs.mean():.1f} observed against {D.new_exp.mean():.1f} expected under the real v2 grammar ({(D.new_obs / D.new_exp).mean():.2f} times)')
# where the rest lives
tot = 0.0; in40 = 0.0; in200 = 0.0; top200 = set(zip(P.head(200).a, P.head(200).b))
for x, k in NEW:
    ids = [idx[s] for s in x]
    for a, b in zip(x, x[1:]):
        g = np.log2(big.trans[idx[a], idx[b]] / m.trans[idx[a], idx[b]])
        tot += g; in40 += g * ((a, b) in toppairs); in200 += g * ((a, b) in top200)
log(f'new texts: bigram saving over v2 inside texts {tot:.0f} bits; top-40 pairs carry {in40:.0f} ({in40 / tot:.0%}), top-200 pairs {in200:.0f} ({in200 / tot:.0%})')
top['picture'] = [f'[{pic(a)}] [{pic(b)}]' for a, b in zip(top.a, top.b)]
top['classes'] = [f'{V2B.get(a)} > {V2B.get(b)}' for a, b in zip(top.a, top.b)]
top['new_text_count'] = [sum(1 for x, k in NEW for p, q in zip(x, x[1:]) if (p, q) == (a, b)) for a, b in zip(top.a, top.b)]
top.to_csv(f'{OUT2}/fixed_pairs.csv', index=False)
t3 = Q.head(40).copy()
t3['picture'] = [f'[{pic(a)}] [{pic(b)}] [{pic(c)}]' for a, b, c in zip(t3.a, t3.b, t3.c)]
t3['classes'] = [f'{V2B.get(a)} > {V2B.get(b)} > {V2B.get(c)}' for a, b, c in zip(t3.a, t3.b, t3.c)]
t3['new_text_count'] = [sum(1 for x, k in NEW for p, q, r in zip(x, x[1:], x[2:]) if (p, q, r) == (a, b, c)) for a, b, c in zip(t3.a, t3.b, t3.c)]
t3.to_csv(f'{OUT2}/fixed_triples.csv', index=False)
D.to_csv(f'{OUT2}/fixed_pairs_decoy.csv', index=False)
for r in top.itertuples(): log(f'  pair {r.a}-{r.b} n={r.n} gain {r.gain:.1f}  P(b|a) {r.p_bigram:.2f} vs v2 {r.p_v2:.3f}  new {r.new_text_count}  {r.picture}  {r.classes}')
for r in t3.itertuples(): log(f'  triple {r.a}-{r.b}-{r.c} n={r.n} gain {r.gain:.1f} beyond pairs {r.beyond_pairs:.1f} new {r.new_text_count}  {r.picture}')
# ORDER DECOY on new texts (added after the shuffled-corpus check matched the real ratio): for the 40 fixed pairs,
# count (a,b) against the reversed (b,a), and texts that hold both signs at all.
cn = collections.Counter()
for x, k in NEW:
    for a, b in zip(x, x[1:]): cn[(a, b)] += 1
fw = sum(cn[(a, b)] for a, b in zip(top.a, top.b)); rv = sum(cn[(b, a)] for a, b in zip(top.a, top.b))
both = sum(1 for x, k in NEW for a, b in zip(top.a, top.b) if a in x and b in x)
log(f'new texts, order check: fixed pairs in their order {fw}, reversed {rv}; text-pair incidences holding both signs {both}')
