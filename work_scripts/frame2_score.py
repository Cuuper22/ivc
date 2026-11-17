#!/usr/bin/env python3
"""FRAME v2, step 2: hand frame v1, machine classes and frame v2 side by side, each against 20 decoys.
Fixed before running (2026-11-17):

FRAMES  v1 = hand jobs (frame_common.HAND); machine = HMM K=10 classes and exchange K=10 classes (classes.csv);
        v2 base = 14 explicit classes (frame2_common.v2_of); v2 pushed = v2 base plus the classes added on the held-out
        half of the first catalogue (classes_v2.csv, frame2_build.py).
GRAMMARS each frame as a pooled class grammar (frame_common recipe) and as a kind grammar (frame2_common.class_model_kind).
DECOYS  each frame's labels dealt among signs of the same training-frequency band (frame_common.deal_within_bands,
        10 bands, seeds 500-519), scored exactly like the real frame.
TESTS   (1) bits per sign on the 482 new texts (second-catalogue lines with no partner in the first catalogue);
            share of the sign-pair model's knowledge captured = (unigram - frame) / (unigram - sign bigram).
        (2) fill-the-gap on the 77 crosswalk items (frame_predict.py item rule, training without those faces); top 1/5/10
            for the frame grammar alone and mixed 0.5/0.5 with the sign bigram. The kind of a gap item = kind of its
            first-catalogue face.
        (3) strict coverage by object kind: (a) the written patterns: v1's hand pattern on v1 jobs, v2's patterns on v2
            base classes (and the same patterns on decoy-dealt labels); (b) a learned automaton for every frame: per kind,
            the class steps (with START and END) seen 3+ times and making 2%+ of their row in the first catalogue's
            distinct clean texts of that kind; a text is covered if every step is allowed. Scored on the new texts and
            on the first catalogue's clean distinct texts.
OUTPUT  work_data/frame/v2_bits.csv, v2_gap.csv, v2_coverage.csv, v2_decoys.csv, log_v2_score.txt
"""
from frame2_common import *

NDEC = 20
c2 = pd.read_csv(f'{OUT2}/classes_v2.csv', dtype=str).fillna('')
FRAMES = collections.OrderedDict([
    ('v1 hand jobs', {s: HAND[s] for s in HAND}),
    ('machine HMM10', dict(HMM10)),
    ('machine exchange10', dict(EXCH10)),
    ('v2 base', dict(zip(c2.sign, c2.v2_base))),
    ('v2 pushed', dict(zip(c2.sign, c2.v2_pushed))),
])

T = train_texts(); vocab, idx = vocab_of(T)
C, CK = kind_counts(T, idx)
uni = unigram_model(C); big = bigram_model(C)
NEW, nMu, ncand = new_texts(idx)
log(f'new texts: {nMu} lines with no partner; {ncand} complete and mapped; {len(NEW)} with every sign seen (scored)')
band = freq_band({s: int(C['uni'][idx[s]]) for s in vocab})
u_bits = bits(FixedKind(uni), NEW, idx); b_bits = bits(FixedKind(big), NEW, idx)
log(f'unigram {u_bits:.3f}  sign bigram {b_bits:.3f} bits/sign on new texts')
share = lambda x: (u_bits - x) / (u_bits - b_bits)


def full(mp, name, pooled):
    m = class_model_kind(C, CK, {s: mp.get(s, 'PERSONAL' if name.startswith('v1') else 'UNSEEN') for s in vocab}, name, vocab, pooled_only=pooled)
    return m


# ---------------------------------------------------------------- gap items (same rule as frame_predict.py)
mah2lipi = dict(zip(M.reading_mah, M.tok))
lipikind = {}
for x, k in zip(d.tok, d.kind): lipikind.setdefault('-'.join(x), k)
items = []; seen = set()
for g, lt, mt in zip(pairs.group, pairs.lipi_text, pairs.mahadevan_text):
    L = tuple(lt.split('-')); Mt = mah2lipi.get(mt)
    if Mt is None or len(L) != len(Mt): continue
    for gapped, full_ in ((L, Mt), (Mt, L)):
        lost = [i for i, s in enumerate(gapped) if s == '000']
        if len(lost) != 1 or set(full_) & UNK or any(s.startswith('X') for s in full_): continue
        p = lost[0]
        if any(gapped[i] != full_[i] for i in range(len(L)) if i != p): continue
        key = (gapped, full_[p])
        if key in seen: continue
        seen.add(key); items.append(dict(lipi_text=lt, context=gapped, pos=p, true=full_[p], answer='-'.join(full_), kind=lipikind.get(lt, 'other')))
log(f'gap items: {len(items)}')
excl_text = {it['lipi_text'] for it in items} | {it['answer'] for it in items}
excl_ids = {i for i, x in zip(d.id, d.tok) if '-'.join(x) in excl_text}
Tg = train_texts(frozenset(excl_ids)); gv, gidx = vocab_of(Tg); gC, gCK = kind_counts(Tg, gidx)
gbig = bigram_model(gC)
gband = band


def gap_score(model):
    """model: KindModel over the gap vocabulary. returns top1, top5, top10 shares."""
    h = np.zeros(3)
    for it in items:
        ids = [gidx.get(s) if s != '000' else None for s in it['context']]
        tr = gidx.get(it['true'])
        if tr is None: continue
        p = gap_posteriors(model.get(it['kind']), ids, True)[it['pos']]
        rank = int((p > p[tr]).sum()); h += [rank < 1, rank < 5, rank < 10]
    return h / len(items)


gbigK = FixedKind(gbig)
g_big = gap_score(gbigK)
g_freq = None
fo = np.argsort(-gC['uni']); fr = {gv[i]: r for r, i in enumerate(fo)}
g_freq = np.array([np.mean([fr.get(it['true'], 9999) < k for it in items]) for k in (1, 5, 10)])
log(f'gap: frequency only {g_freq.round(3)}; sign bigram {g_big.round(3)}')


# ---------------------------------------------------------------- coverage
clean_by_kind = collections.defaultdict(list); seen = set()
for x, f, k in zip(d.tok, d.flg, d.kind):
    if f & {'broken', 'lost', 'alt'} or set(x) & UNK or not x: continue
    if (x, k) in seen: continue
    seen.add((x, k)); clean_by_kind[kind_of(k)].append(x)
new_by_kind = collections.defaultdict(list)
for x, k in NEW: new_by_kind[kind_of(k)].append(x)


def automaton(mp):
    allowed = {}
    for k in KINDS + ['other']:
        T_ = clean_by_kind[k] if k != 'other' else [x for kk in clean_by_kind for x in clean_by_kind[kk]]
        tr = collections.defaultdict(collections.Counter)
        for x in T_:
            s = ['START'] + [mp.get(a, '?') for a in x] + ['END']
            for a, b in zip(s, s[1:]): tr[a][b] += 1
        allowed[k] = {(a, b) for a in tr for b, n in tr[a].items() if n >= 3 and n / sum(tr[a].values()) >= 0.02}
    return allowed


def auto_cov(mp, allowed, texts_by_kind):
    out = {}
    for k in KINDS:
        T_ = texts_by_kind[k]
        if not T_: continue
        ok = 0
        for x in T_:
            s = ['START'] + [mp.get(a, '?') for a in x] + ['END']
            ok += all((a, b) in allowed[k] for a, b in zip(s, s[1:]))
        out[k] = ok / len(T_)
    return out


def pattern_cov(frame, mp, texts_by_kind):
    out = {}
    for k in KINDS:
        T_ = texts_by_kind[k]
        if not T_: continue
        if frame == 'v1 hand jobs': ok = [v1_fits([mp.get(a, 'PERSONAL') for a in x]) for x in T_]
        else: ok = [v2_type([mp.get(a, 'PERSONAL') for a in x], k) != '' for x in T_]
        out[k] = float(np.mean(ok))
    return out


# ---------------------------------------------------------------- run every frame and its decoys
rows_bits = []; rows_gap = []; rows_cov = []; rows_dec = []
gap_bits_kind = {}
for fname, mp in FRAMES.items():
    for pooled in (True, False):
        gname = f'{fname} ({"pooled" if pooled else "by kind"})'
        m = full(mp, gname, pooled); x = bits(m, NEW, idx)
        mixm = mix_kind(FixedKind(big), m, 0.5, 'mix'); xm = bits(mixm, NEW, idx)
        by = {KIND_PLAIN[k]: bits(m, [(a, kk) for a, kk in NEW if kind_of(kk) == k], idx) for k in KINDS if new_by_kind[k]}
        gm = class_model_kind(gC, gCK, {s: mp.get(s, 'UNSEEN') for s in gv}, gname, gv, pooled_only=pooled)
        gs = gap_score(gm); gsm = gap_score(mix_kind(gbigK, gm, 0.5, 'mix'))
        dec_b = []; dec_g = []; dec_gm = []
        for q in range(500, 500 + NDEC):
            dm = deal_within_bands({s: mp[s] for s in vocab if s in mp}, band, q)
            md = class_model_kind(C, CK, {s: dm.get(s, 'UNSEEN') for s in vocab}, 'decoy', vocab, pooled_only=pooled)
            dec_b.append(bits(md, NEW, idx))
            gd = class_model_kind(gC, gCK, {s: dm.get(s, 'UNSEEN') for s in gv}, 'decoy', gv, pooled_only=pooled)
            dec_g.append(gap_score(gd)); dec_gm.append(gap_score(mix_kind(gbigK, gd, 0.5, 'mix')))
            rows_dec.append(dict(grammar=gname, seed=q, bits=dec_b[-1], gap_top1=dec_g[-1][0], gap_top5=dec_g[-1][1], gap_top10=dec_g[-1][2],
                                 mix_top1=dec_gm[-1][0], mix_top5=dec_gm[-1][1]))
        dec_b = np.array(dec_b); dec_g = np.array(dec_g); dec_gm = np.array(dec_gm)
        rows_bits.append(dict(grammar=gname, classes=len(set(mp.values())), bits=x, share=share(x), decoy_mean=dec_b.mean(), decoy_best=dec_b.min(),
                              decoy_share_mean=share(dec_b.mean()), decoys_at_or_below=int((dec_b <= x).sum()), mix_with_bigram=xm, **{f'bits {k}': v for k, v in by.items()}))
        rows_gap.append(dict(grammar=gname, top1=gs[0], top5=gs[1], top10=gs[2], decoy_top1=dec_g[:, 0].mean(), decoy_top5=dec_g[:, 1].mean(), decoy_top10=dec_g[:, 2].mean(),
                             decoy_best_top5=dec_g[:, 1].max(), decoys_top5_at_or_above=int((dec_g[:, 1] >= gs[1]).sum()),
                             mix_top1=gsm[0], mix_top5=gsm[1], mix_top10=gsm[2], decoy_mix_top1=dec_gm[:, 0].mean(), decoy_mix_top5=dec_gm[:, 1].mean()))
        log(f'{gname:34s} bits {x:.3f} share {share(x):.1%} | decoy mean {dec_b.mean():.3f} best {dec_b.min():.3f} ({int((dec_b <= x).sum())} of {NDEC} at or below) | mix {xm:.3f}')
        log(f'{"":34s} gap top1/5/10 {gs.round(3)} decoy mean {dec_g.mean(0).round(3)} | mixed with bigram {gsm.round(3)} decoy-mix {dec_gm.mean(0).round(3)}')
    # coverage (kind-free definitions)
    al = automaton(mp)
    for setname, tb in (('new texts', new_by_kind), ('first catalogue', clean_by_kind)):
        ac = auto_cov(mp, al, tb); pc = pattern_cov(fname, mp, tb) if fname in ('v1 hand jobs', 'v2 base') else {}
        dac = collections.defaultdict(list); dpc = collections.defaultdict(list)
        for q in range(500, 500 + NDEC):
            dm = deal_within_bands({s: mp[s] for s in vocab if s in mp}, band, q)
            for k, v in auto_cov(dm, automaton(dm), tb).items(): dac[k].append(v)
            if pc:
                for k, v in pattern_cov(fname, dm, tb).items(): dpc[k].append(v)
        for k in ac:
            rows_cov.append(dict(frame=fname, texts=setname, kind=KIND_PLAIN[k], n=len(tb[k]), automaton=ac[k], automaton_decoy_mean=np.mean(dac[k]), automaton_decoy_max=np.max(dac[k]),
                                 pattern=pc.get(k, np.nan), pattern_decoy_mean=np.mean(dpc[k]) if dpc else np.nan, pattern_decoy_max=np.max(dpc[k]) if dpc else np.nan))
        log(f'  coverage [{setname}] ' + ' | '.join(f'{KIND_PLAIN[k]} auto {ac[k]:.0%} (decoy {np.mean(dac[k]):.0%})' + (f' pattern {pc[k]:.0%} (decoy {np.mean(dpc[k]):.0%})' if pc else '') for k in ac))

pd.DataFrame(rows_bits).to_csv(f'{OUT2}/v2_bits.csv', index=False)
G = pd.DataFrame(rows_gap)
G = pd.concat([G, pd.DataFrame([dict(grammar='frequency only', top1=g_freq[0], top5=g_freq[1], top10=g_freq[2]), dict(grammar='sign bigram', top1=g_big[0], top5=g_big[1], top10=g_big[2])])])
G.to_csv(f'{OUT2}/v2_gap.csv', index=False)
pd.DataFrame(rows_cov).to_csv(f'{OUT2}/v2_coverage.csv', index=False)
pd.DataFrame(rows_dec).to_csv(f'{OUT2}/v2_decoys.csv', index=False)
pd.DataFrame([dict(model='unigram', bits=u_bits), dict(model='sign bigram', bits=b_bits)]).to_csv(f'{OUT2}/v2_reference_bits.csv', index=False)
log('done')
