#!/usr/bin/env python3
"""STEP 2, one redesign (written after the pooled class grammars did no better than the unigram on new tablets and pots).
Idea fixed before rerun: tablets and pots follow their own grammar; a grammar trained on all kinds is dominated by seals.
Redesign: class transitions (start, class-to-class, end) trained on first-catalogue texts of the SAME kind only;
sign-in-class emissions and the unigram still from all texts (small kinds are too thin for their own emissions).
Scored on the new texts of each kind; decoy = the same 20 within-band deals, trained the same way."""
from frame_common import *

T = train_texts(); vocab, idx = vocab_of(T); C = counts(T, idx)
uni = unigram_model(C)
band = freq_band({s: int(C['uni'][idx[s]]) for s in vocab})
cls = pd.read_csv(f'{OUT}/classes.csv', dtype=str).fillna('')
MAPS = {'hand jobs': {s: j for s, j in zip(cls.sign, cls.hand_job) if j}, 'hmm10': dict(zip(cls.sign, cls.hmm10))}
Mu = M[~M.partnered]
NEW = [(tuple(x), k) for x, c, k in zip(Mu.tok, Mu.complete_b, Mu.kind) if c and x and not (set(x) & UNK) and all(s in idx for s in x)]


def kind_class_model(mp, kind):
    full, info = class_model(C, mp, 'x', vocab)
    Tk = [t for t in T if t[2] == kind]
    Ck = counts(Tk, idx)
    _, ik = class_model(Ck, mp, 'k', vocab)
    cid = info['cid']; K = len(info['labs'])
    rows = np.concatenate([ik['cb'], ik['ce'][:, None]], 1) + 0.1; rows /= rows.sum(1, keepdims=True)
    cst = (ik['cs'] + 0.1) / (ik['cs'].sum() + 0.1 * K)
    em = info['em']
    return SeqModel(f'kind {kind}', cst[cid] * em, rows[:, :K][cid][:, cid] * em[None, :], rows[:, K][cid])


def sc(m, L):
    lp = sum(m.logprob([idx[s] for s in x]) for x in L); return -lp / sum(map(len, L))


out = []
for kind in ['seal', 'tag', 'mtab', 'ctab', 'pot']:
    L = [x for x, k in NEW if k == kind]
    r = dict(kind=kind, lines=len(L), unigram=sc(uni, L))
    for nm, mp in MAPS.items(): r[f'kind grammar: {nm}'] = sc(kind_class_model(mp, kind), L)
    dec = [sc(kind_class_model(deal_within_bands(MAPS['hand jobs'], band, q), kind), L) for q in range(500, 520)]
    r['kind grammar: decoy mean'] = np.mean(dec); r['kind grammar: decoy best'] = np.min(dec)
    out.append(r)
    log(f'{kind} n={len(L)}: unigram {r["unigram"]:.3f} | hand jobs {r["kind grammar: hand jobs"]:.3f} | hmm10 {r["kind grammar: hmm10"]:.3f} | decoy mean {np.mean(dec):.3f} best {np.min(dec):.3f}')
pd.DataFrame(out).to_csv(f'{OUT}/bits_by_kind_redesign.csv', index=False)
