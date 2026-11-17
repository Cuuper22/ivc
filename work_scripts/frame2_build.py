#!/usr/bin/env python3
"""FRAME v2, step 1: the base classes (frame2_common.v2_of) and the held-out push. Fixed before running (2026-11-17):

  Split: the distinct first-catalogue texts (frame_common.train_texts) are dealt into two halves by seed 2026:
  half A (fit) and half B (held out). The new (second-catalogue) texts are NOT used here.
  Push: greedy. A candidate move takes one sign with 10+ uses in half A and puts it either into a NEW class of its own or
  into one of the classes created earlier in the push (base classes never receive signs; signs can leave them).
  The pooled class grammar (frame_common.class_model recipe: class transitions add-0.1, emissions add-0.5 within class)
  is fitted on A and scored on B in bits per sign (end of text counted on clean texts). Each round takes the single
  move that lowers B's bits most; the push stops when the best move gains less than 0.002 bits per sign, or at 60
  added classes.
  Output: work_data/frame/classes_v2.csv (sign, uses, v2 base class, v2 pushed class), work_data/frame/log_v2_push.txt
"""
from frame2_common import *

T = train_texts()
vocab, idx = vocab_of(T); V = len(vocab)
r = np.random.default_rng(2026)
half = r.random(len(T)) < 0.5
TA = [t for t, h in zip(T, half) if h]; TB = [t for t, h in zip(T, half) if not h]
log(f'distinct first-catalogue texts {len(T)}: half A {len(TA)}, half B {len(TB)}; vocabulary {V}')


def flat(texts):
    a, b, st, en = [], [], [], []
    for x, clean, k in texts:
        ids = [idx.get(s) for s in x]
        for p, q in zip(ids, ids[1:]):
            if p is not None and q is not None: a.append(p); b.append(q)
        if clean: st.append(ids[0]); en.append(ids[-1])
    return np.array(a), np.array(b), np.array(st), np.array(en)


CA = counts(TA, idx); uniA = CA['uni']
aA, bA, sA, eA = flat(TA); aB, bB, sB, eB = flat(TB)
ntokB = sum(1 for x, c, k in TB for s in x if s in idx)


def heldout_bits(z, K):
    nk = np.bincount(z, minlength=K); cu = np.bincount(z, uniA, K)
    em = (uniA + 0.5) / (cu[z] + 0.5 * nk[z])
    cb = np.bincount(z[aA] * K + z[bA], minlength=K * K).reshape(K, K).astype(float)
    ce = np.bincount(z[eA], minlength=K).astype(float)
    rows = np.concatenate([cb, ce[:, None]], 1) + 0.1; rows /= rows.sum(1, keepdims=True)
    cs = np.bincount(z[sA], minlength=K) + 0.1; cs = cs / cs.sum()
    lem = np.log2(em)
    ll = (np.log2(cs[z[sB]]) + lem[sB]).sum() + (np.log2(rows[z[aB], z[bB]]) + lem[bB]).sum() + np.log2(rows[z[eB], K]).sum()
    return -ll / ntokB


base = {s: v2_of(s) for s in vocab}
labs = list(V2_CLASSES)
z = np.array([labs.index(base[s]) for s in vocab]); K = len(labs)
b0 = heldout_bits(z, K)
# references on the same split
zu = np.zeros(V, int); log(f'held-out bits: one class (unigram-like) {heldout_bits(zu, 1):.3f}')
hand = {s: HAND.get(s, 'PERSONAL') for s in vocab}; hl = sorted(set(hand.values()))
log(f'held-out bits: v1 hand jobs {heldout_bits(np.array([hl.index(hand[s]) for s in vocab]), len(hl)):.3f}')
hm = {s: HMM10.get(s, 'UNSEEN') for s in vocab}; ml = sorted(set(hm.values()))
log(f'held-out bits: machine HMM10 classes {heldout_bits(np.array([ml.index(hm[s]) for s in vocab]), len(ml)):.3f}')
log(f'held-out bits: v2 base ({K} classes) {b0:.3f}')
cand = [i for i in range(V) if uniA[i] >= 10]
log(f'push: {len(cand)} candidate signs (10+ uses in half A)')
added = []; hist = []
cur = b0
while len(added) < 60:
    best = (0, None)
    for i in cand:
        old = z[i]
        # new class of its own
        z2 = z.copy(); z2[i] = K
        g = cur - heldout_bits(z2, K + 1)
        if g > best[0]: best = (g, (i, 'new'))
        for c in added:
            if c == old: continue
            z2 = z.copy(); z2[i] = c
            # an added class left empty is harmless (empty rows only add smoothing mass)
            g = cur - heldout_bits(z2, K)
            if g > best[0]: best = (g, (i, c))
    if best[1] is None or best[0] < 0.002: break
    i, tgt = best[1]
    frm = labs[z[i]]
    if tgt == 'new':
        labs.append(f'X{len(added) + 1:02d}'); added.append(K); z[i] = K; K += 1; to = labs[-1]
    else:
        z[i] = tgt; to = labs[tgt]
    cur -= best[0]
    hist.append(dict(step=len(hist) + 1, sign=vocab[i], from_class=frm, to_class=to, gain=round(best[0], 4), heldout_bits=round(cur, 4)))
    log(f'  step {len(hist):2d}: sign {vocab[i]} {frm} -> {to}  gain {best[0]:.4f}  held-out {cur:.3f} bits/sign  ({len(added)} added classes)')
log(f'push stopped: v2 base {b0:.3f} -> v2 pushed {cur:.3f} bits/sign on held-out half B, {len(added)} classes added')
cls2 = pd.DataFrame(dict(sign=vocab, uses=CA['uni'].astype(int) + counts(TB, idx)['uni'].astype(int),
                         v2_base=[base[s] for s in vocab], v2_pushed=[labs[z[i]] for i in range(V)],
                         hand_v1=[HAND.get(s, 'PERSONAL') for s in vocab], hmm10=[HMM10.get(s, '') for s in vocab]))
cls2.to_csv(f'{OUT2}/classes_v2.csv', index=False)
pd.DataFrame(hist).to_csv(f'{OUT2}/v2_push_steps.csv', index=False)
for c in labs[len(V2_CLASSES):]:
    log(f'  added class {c}: ' + ' '.join(cls2[cls2.v2_pushed == c].sort_values('uses', ascending=False).sign.head(15)))
