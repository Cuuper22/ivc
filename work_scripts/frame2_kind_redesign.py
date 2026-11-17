#!/usr/bin/env python3
"""FRAME v2, the one redesign of the kind grammar (written 2026-11-17 after frame2_score.py showed the kind grammars
scoring WORSE than the pooled ones on the new texts, worst on tags and sealings).
Two changes, fixed before this script's numbers:
  (1) a second-catalogue 'sealing' is an impression of a seal, so it is scored with the SEAL grammar (first-catalogue
      tags are mostly goods tags: a different object).
  (2) the back-off weight BETA is chosen per frame on the held-out half B of the first catalogue (fit on half A, same
      split as frame2_build.py), from 5, 20, 50, 200, 1000; then refitted on the whole first catalogue.
Output: work_data/frame/v2_kind_redesign.csv
"""
from frame2_common import *

c2 = pd.read_csv(f'{OUT2}/classes_v2.csv', dtype=str).fillna('')
FRAMES = collections.OrderedDict([('v1 hand jobs', dict(HAND)), ('machine HMM10', dict(HMM10)), ('machine exchange10', dict(EXCH10)),
                                  ('v2 base', dict(zip(c2.sign, c2.v2_base))), ('v2 pushed', dict(zip(c2.sign, c2.v2_pushed)))])
T = train_texts(); vocab, idx = vocab_of(T)
r = np.random.default_rng(2026); half = r.random(len(T)) < 0.5
TA = [t for t, h in zip(T, half) if h]; TB = [(x, k) for (x, c, k), h in zip(T, half) if not h and c and not set(x) & UNK]
CA, CKA = kind_counts(TA, idx); C, CK = kind_counts(T, idx)
NEW, _, _ = new_texts(idx)
NEW2 = [(x, 'seal' if k == 'tag' else k) for x, k in NEW]   # second-catalogue sealings -> seal grammar
uni = unigram_model(C); big = bigram_model(C)
u = bits(FixedKind(uni), NEW, idx); b = bits(FixedKind(big), NEW, idx)
band = freq_band({s: int(C['uni'][idx[s]]) for s in vocab})
rows = []
for fn, mp in FRAMES.items():
    mpv = {s: mp.get(s, 'UNSEEN') for s in vocab}
    hb = {beta: bits(class_model_kind(CA, CKA, mpv, fn, vocab, beta=beta), TB, idx) for beta in (5, 20, 50, 200, 1000)}
    hp = bits(class_model_kind(CA, CKA, mpv, fn, vocab, pooled_only=True), TB, idx)
    beta = min(hb, key=hb.get)
    m = class_model_kind(C, CK, mpv, fn, vocab, beta=beta); x = bits(m, NEW2, idx)
    xp = bits(class_model_kind(C, CK, mpv, fn, vocab, pooled_only=True), NEW2, idx)
    dec = []
    for q in range(500, 520):
        dm = deal_within_bands({s: mp[s] for s in vocab if s in mp}, band, q)
        dec.append(bits(class_model_kind(C, CK, {s: dm.get(s, 'UNSEEN') for s in vocab}, 'decoy', vocab, beta=beta), NEW2, idx))
    dec = np.array(dec)
    by = {KIND_PLAIN[k]: bits(m, [(a, kk) for a, kk in NEW2 if kk == k], idx) for k in KINDS if any(kk == k for a, kk in NEW2)}
    byp = {KIND_PLAIN[k] + ' pooled': bits(class_model_kind(C, CK, mpv, fn, vocab, pooled_only=True), [(a, kk) for a, kk in NEW2 if kk == k], idx) for k in KINDS if any(kk == k for a, kk in NEW2)}
    rows.append(dict(frame=fn, beta=beta, heldout_by_kind=hb[beta], heldout_pooled=hp, new_by_kind=x, new_pooled=xp, share_by_kind=(u - x) / (u - b),
                     decoy_mean=dec.mean(), decoy_best=dec.min(), decoys_at_or_below=int((dec <= x).sum()), **by, **byp))
    log(f'{fn:20s} beta {beta:5d} | held-out B: by kind {hb[beta]:.3f} pooled {hp:.3f} | new texts by kind {x:.3f} (share {(u - x) / (u - b):.1%}) pooled {xp:.3f} | decoy mean {dec.mean():.3f} best {dec.min():.3f}')
    log('      ' + ' | '.join(f'{k} {v:.3f}' for k, v in {**by, **byp}.items()))
pd.DataFrame(rows).to_csv(f'{OUT2}/v2_kind_redesign.csv', index=False)
