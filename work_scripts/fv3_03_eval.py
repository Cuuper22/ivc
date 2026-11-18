#!/usr/bin/env python3
"""FRAME v3 — Step 3 & 4: Full Evaluation (Lipi + Unseen Mahadevan `new texts` + 20 Decoys + Order Shuffles)
and Full Corpus Clause Segmentation Export (`corpus_parsed_v3.csv`).

Runs:
  1. Strict template parse coverage on Lipi (all 3,600 intact faces, 2,855 deduplicated events, 2,162 distinct texts;
     overall, len>=2, len>=3, and per object kind) AND unseen Mahadevan `new texts` (482 Lipi-vocab lines AND all 528+
     complete mapped lines; overall, len>=2, len>=3, and per object kind), compared against:
       - 20 frequency-band-matched decoy class maps (`deal_within_bands`, seeds 500..519),
       - 20 within-line token-order shuffles (testing syntagmatic linear order with real classes intact).
  2. Next-sign cross-entropy (bits per sign) on:
       - 5-fold Lipi CV (both fixed v3 map and strictly nested out-of-fold class learning!),
       - Lipi Half-A -> Half-B (seed 2026, matching `frame2_build.py` and `frame2_kind_redesign.py`),
       - Unseen Mahadevan `new texts` (482 lines, pooled, kind-redesigned, and 0.5 mix with sign bigram),
     against `frame v1`, `frame v2`, and 20 decoys.
  3. 77-item Fill-the-Gap benchmark (`frame2_score.py` protocol) vs `frame v2` and 20 decoys.
  4. Exports `work_data/fv3/corpus_parsed_v3.csv` for every Lipi (5,679) + Mahadevan line segmented into clauses and roles.
"""
import os, sys, collections
import numpy as np, pandas as pd
from scipy.stats import norm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DYN = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
sys.path.insert(0, SCRIPT_DIR)

from frame2_common import *
from fv3_02_grammar import build_v3_classes, parse_v3, parse_v3_initial, tag_sign_roles, OUT_FV3

NDEC = 20
DECOY_SEEDS = list(range(500, 500 + NDEC))

# 1. Build/load Lipi-only v3 classes
V3_MAP, V2_MAP, MOVE_HIST = build_v3_classes(verbose=True)

T = train_texts()
vocab, idx = vocab_of(T)
C_all, CK_all = kind_counts(T, idx)
band = freq_band({s: int(C_all['uni'][idx[s]]) for s in vocab})

# Prepare evaluation text sets
intact_lipi = []
seen_ev = set(); intact_events = []
seen_txt = set(); intact_distinct = []
for idx_r, (fid, x, f, kr) in enumerate(zip(d.id, d.tok, d.flg, d.kind)):
    if not x or (set(x) & UNK) or (f & {'broken', 'lost', 'alt'}):
        continue
    k6 = kind_of(kr)
    intact_lipi.append((tuple(x), k6))
    ek = (d.site.iloc[idx_r], str(d['area-section'].iloc[idx_r]), kr, tuple(x))
    if ek not in seen_ev:
        seen_ev.add(ek); intact_events.append((tuple(x), k6))
    if tuple(x) not in seen_txt:
        seen_txt.add(tuple(x)); intact_distinct.append((tuple(x), k6))

# Unseen Mahadevan `new texts` (never used in fv3_01 or fv3_02!)
Mu = M[~M.partnered]
NEW_627 = [(tuple(x), kind_of(k)) for x, c, k in zip(Mu.tok, Mu.complete_b, Mu.kind)
           if c and x and not (set(x) & UNK)]
NEW_482 = [(x, k) for x, k in NEW_627 if not any(s.startswith('X') for s in x) and all(s in idx for s in x)]
log(f'Datasets ready: Lipi intact={len(intact_lipi)} (events={len(intact_events)}, distinct={len(intact_distinct)}); '
    f'Unseen Mahadevan new_482={len(NEW_482)}, all_complete_627={len(NEW_627)}, total_Mu={len(Mu)}')


# ==============================================================================
# PART 1: STRICT PARSE COVERAGE vs 20 DECOYS & 20 ORDER SHUFFLES
# ==============================================================================
def run_parser(name, lines, mp):
    out = []
    for x, k in lines:
        cl = [mp.get(s, 'PERSONAL') for s in x]
        if name == 'v2 base':
            r = v2_type(cl, k)
        elif name == 'v3a initial':
            r = parse_v3_initial(cl, k)[0]
        elif name == 'v3 final':
            r = parse_v3(cl, k)[0]
        else:
            raise ValueError(name)
        out.append(r)
    return out


def eval_coverage_suite(grammar_name, base_map, dataset_name, lines):
    real_out = run_parser(grammar_name, lines, base_map)
    dec_maps = [deal_within_bands({s: base_map[s] for s in vocab if s in base_map}, band, q) for q in DECOY_SEEDS]
    dec_outs = [run_parser(grammar_name, lines, dm) for dm in dec_maps]

    # Within-line order shuffles (keeping REAL classes intact, testing linear syntax!)
    rng_sh = np.random.default_rng(2026)
    shuf_outs = []
    for _ in range(NDEC):
        sh_lines = [(tuple(rng_sh.permutation(list(x))), k) for x, k in lines]
        shuf_outs.append(run_parser(grammar_name, sh_lines, base_map))

    subsets = [
        ('all', lambda x, k: True),
        ('len>=2', lambda x, k: len(x) >= 2),
        ('len>=3', lambda x, k: len(x) >= 3),
        ('admin_len>=3 (no pot/other)', lambda x, k: len(x) >= 3 and k in ('seal', 'mtab', 'ctab', 'tag')),
    ] + [(f'kind:{k}', (lambda kk: lambda x, k_: k_ == kk)(k)) for k in KINDS + ['other']]

    rows = []
    for sub_name, pred in subsets:
        mask = [i for i, (x, k) in enumerate(lines) if pred(x, k)]
        if not mask:
            continue
        r_rate = float(np.mean([real_out[i] != '' for i in mask]))
        d_rates = np.array([np.mean([do[i] != '' for i in mask]) for do in dec_outs])
        s_rates = np.array([np.mean([so[i] != '' for i in mask]) for so in shuf_outs])
        dm = float(d_rates.mean()); dsd = float(d_rates.std(ddof=1)); dmax = float(d_rates.max())
        z = (r_rate - dm) / dsd if dsd > 1e-12 else np.inf
        pval = float(norm.sf(z)) if np.isfinite(z) else 0.0
        sm = float(s_rates.mean()); ssd = float(s_rates.std(ddof=1))
        zs = (r_rate - sm) / ssd if ssd > 1e-12 else np.inf
        rows.append(dict(
            grammar=grammar_name, dataset=dataset_name, subset=sub_name, n=len(mask),
            real_parse=round(r_rate, 5),
            decoy_mean=round(dm, 5), decoy_sd=round(dsd, 5), decoy_max=round(dmax, 5),
            real_minus_decoy=round(r_rate - dm, 5), z_decoy=round(z, 2), p_decoy=pval,
            decoys_ge_real=int((d_rates >= r_rate).sum()),
            order_shuf_mean=round(sm, 5), real_minus_shuf=round(r_rate - sm, 5), z_shuf=round(zs, 2)
        ))
    return rows, real_out


cov_rows = []
for gname, gmap in [('v2 base', V2_MAP), ('v3a initial', V3_MAP), ('v3 final', V3_MAP)]:
    for dname, dlines in [
        ('Lipi intact (3600)', intact_lipi),
        ('Lipi events (2855)', intact_events),
        ('Lipi distinct (2162)', intact_distinct),
        ('Unseen new_texts (482)', NEW_482),
        ('Unseen all_complete (627)', NEW_627),
    ]:
        r_sub, _ = eval_coverage_suite(gname, gmap, dname, dlines)
        cov_rows.extend(r_sub)

cov_df = pd.DataFrame(cov_rows)
cov_df.to_csv(os.path.join(OUT_FV3, 'v3_coverage_eval.csv'), index=False)

log('\n=== HEADLINE COVERAGE SUMMARY ===')
for _, r in cov_df[cov_df.subset.isin(['all', 'len>=3', 'admin_len>=3 (no pot/other)'])].iterrows():
    log(f"  {r.grammar:12s} | {r.dataset:23s} | {r.subset:27s} (n={r.n:4d}): "
        f"REAL={r.real_parse:6.2%} vs DECOY={r.decoy_mean:6.2%} (max {r.decoy_max:6.2%}, {r.decoys_ge_real}/20) "
        f"diff={r.real_minus_decoy:+6.2%} z={r.z_decoy:5.2f} P={r.p_decoy:.2e} | shuf={r.order_shuf_mean:6.2%}")

log('\n=== BY OBJECT KIND (v3 final vs v2 base) ===')
for dname in ['Lipi intact (3600)', 'Unseen new_texts (482)']:
    sub = cov_df[(cov_df.dataset == dname) & (cov_df.grammar.isin(['v2 base', 'v3 final'])) & (cov_df.subset.str.startswith('kind:'))]
    for _, r in sub.iterrows():
        log(f"  {r.grammar:9s} | {dname:23s} | {r.subset:11s} (n={r.n:4d}): REAL={r.real_parse:6.1%} (decoy {r.decoy_mean:5.1%}, max {r.decoy_max:5.1%})")


# ==============================================================================
# PART 2: HELD-OUT CROSS-ENTROPY (BITS PER SIGN) & NESTED CV & FILL-THE-GAP
# ==============================================================================
log('\n=== PART 2: HELD-OUT CROSS-ENTROPY (BITS PER SIGN) ===')

# 2A. 5-fold Lipi CV (both fixed class maps AND strictly nested out-of-fold class learning!)
rng_cv = np.random.default_rng(2026)
folds = rng_cv.integers(0, 5, size=len(T))


def score_5fold_map(mp):
    tot_lp = 0.0; tot_n = 0
    for f in range(5):
        tr = [t for t, fl in zip(T, folds) if fl != f]
        va = [(x, k) for (x, c, k), fl in zip(T, folds) if fl == f and c and not (set(x) & UNK)]
        tv, tidx = vocab_of(tr)
        va_f = [(x, k) for x, k in va if all(s in tidx for s in x)]
        Ctr = counts(tr, tidx)
        m, _ = class_model(Ctr, {s: mp.get(s, 'PERSONAL') for s in tv}, 'cls', tv)
        for x, k in va_f:
            ids = [tidx[s] for s in x]
            tot_lp += m.logprob(ids, True); tot_n += len(ids)
    return -tot_lp / tot_n


# Strictly nested out-of-fold class learning (re-learns moves inside each training fold from V2_MAP without seeing val fold!)
def nested_5fold_v3():
    tot_lp = 0.0; tot_n = 0
    labs = list(V2_CLASSES); K = len(labs)
    tgt_ids = [labs.index(c) for c in ['CLOSER', 'TITLE', 'THING', 'MEASURE', 'AFTER_M', 'OPEN', 'SLOT', 'NAME_BACK', 'CREST']]
    for f in range(5):
        tr = [t for t, fl in zip(T, folds) if fl != f]
        va = [(x, k) for (x, c, k), fl in zip(T, folds) if fl == f and c and not (set(x) & UNK)]
        tv, tidx = vocab_of(tr)
        va_f = [(x, k) for x, k in va if all(s in tidx for s in x)]
        Ctr = counts(tr, tidx)
        # Inner 4-fold split on tr to pick moves strictly inside tr!
        r_in = np.random.default_rng(100 + f)
        in_f = r_in.integers(0, 4, size=len(tr))
        in_splits = []
        for inf in range(4):
            itr = [t for t, fl in zip(tr, in_f) if fl != inf]
            iva = [t for t, fl in zip(tr, in_f) if fl == inf]
            C_i = counts(itr, tidx)
            aA, bA, sA, eA = [], [], [], []
            for x, cln, _ in itr:
                ids = [tidx[s] for s in x if s in tidx]
                if len(ids) != len(x): continue
                for p, q in zip(ids, ids[1:]): aA.append(p); bA.append(q)
                if cln: sA.append(ids[0]); eA.append(ids[-1])
            aB, bB, sB, eB = [], [], [], []
            ntokB = 0
            for x, cln, _ in iva:
                ids = [tidx[s] for s in x if s in tidx]
                if len(ids) != len(x): continue
                ntokB += len(ids)
                for p, q in zip(ids, ids[1:]): aB.append(p); bB.append(q)
                if cln: sB.append(ids[0]); eB.append(ids[-1])
            in_splits.append((C_i['uni'], np.array(aA, int), np.array(bA, int), np.array(sA, int), np.array(eA, int),
                              np.array(aB, int), np.array(bB, int), np.array(sB, int), np.array(eB, int), ntokB))

        def in_cv(z):
            tl = 0.0; tn = 0
            for uniA, aA, bA, sA, eA, aB, bB, sB, eB, ntokB in in_splits:
                nk = np.bincount(z, minlength=K); cu = np.bincount(z, uniA, K)
                em = (uniA + 0.5) / (cu[z] + 0.5 * nk[z])
                cb = np.bincount(z[aA] * K + z[bA], minlength=K * K).reshape(K, K).astype(float)
                ce = np.bincount(z[eA], minlength=K).astype(float)
                rm = np.concatenate([cb, ce[:, None]], 1) + 0.1; rm /= rm.sum(1, keepdims=True)
                cs = np.bincount(z[sA], minlength=K) + 0.1; cs /= cs.sum()
                lem = np.log2(em)
                tl += (np.log2(cs[z[sB]]) + lem[sB]).sum() + (np.log2(rm[z[aB], z[bB]]) + lem[bB]).sum() + np.log2(rm[z[eB], K]).sum()
                tn += ntokB
            return -tl / tn

        # Positional counts strictly on tr clean texts len>=2
        occ_tr = collections.Counter(); pi = collections.Counter(); pf = collections.Counter()
        pao = collections.Counter(); pan = collections.Counter(); pbn = collections.Counter()
        pbe = collections.Counter(); pae = collections.Counter(); pam = collections.Counter()
        pbs = collections.Counter(); pbt = collections.Counter()
        for x, cln, _ in tr:
            if not cln or len(x) < 2: continue
            cl = [V2_MAP.get(s, 'PERSONAL') for s in x]
            for j, s in enumerate(x):
                occ_tr[s] += 1
                if j == 0: pi[s] += 1
                if j == len(x) - 1: pf[s] += 1
                if j > 0 and cl[j-1] == 'OPEN': pao[s] += 1
                if j + 1 < len(x) and cl[j+1] == 'SLOT': pbs[s] += 1
                if j > 0 and cl[j-1] in ('NUM_SHORT', 'NUM_TALL', 'NUM_NAME'): pan[s] += 1
                if j + 1 < len(x) and cl[j+1] in ('NUM_SHORT', 'NUM_TALL', 'NUM_NAME'): pbn[s] += 1
                if j + 1 < len(x) and cl[j+1] in ('CLOSER', 'TITLE'): pbe[s] += 1
                if j > 0 and cl[j-1] in ('CLOSER', 'TITLE'): pae[s] += 1
                if j > 0 and (cl[j-1] == 'MEASURE' or x[j-1] == '706'): pam[s] += 1
                if j + 1 < len(x) and cl[j+1] == 'THING': pbt[s] += 1

        def role_ok_tr(s, orig_name, tgt_name):
            n = occ_tr[s]
            if n < 3: return False
            if orig_name != 'PERSONAL':
                if orig_name == 'PLACE' and tgt_name in ('OPEN', 'THING'): pass
                elif orig_name == 'CREST' and s in ('226', '222', '243') and tgt_name in ('CLOSER', 'TITLE', 'THING', 'NAME_BACK'): pass
                else: return False
            fi = pf[s]/n; ini = pi[s]/n
            if tgt_name == 'CLOSER': return (fi >= 0.55 and ini <= 0.25) or (fi >= 0.40 and fi + pbe[s]/n >= 0.65 and ini <= 0.20)
            if tgt_name == 'TITLE': return (fi >= 0.55 and ini <= 0.25) or (pae[s]/n >= 0.35 and fi >= 0.45) or (pam[s]/n >= 0.50 and fi >= 0.85)
            if tgt_name == 'THING': return (pan[s]/n >= 0.35 and pbn[s]/n <= 0.15) or (fi >= 0.55 and ini <= 0.22 and pan[s]/n >= 0.05)
            if tgt_name == 'MEASURE': return pbn[s]/n >= 0.45 or pbt[s]/n >= 0.45
            if tgt_name == 'AFTER_M': return pam[s]/n >= 0.35
            if tgt_name == 'OPEN': return fi <= 0.15 and (ini >= 0.65 or (ini >= 0.50 and pbs[s]/n >= 0.40))
            if tgt_name == 'SLOT': return pao[s]/n >= 0.25 and fi <= 0.20
            if tgt_name == 'NAME_BACK': return pbe[s]/n >= 0.60 and fi <= 0.18
            if tgt_name == 'CREST': return ini >= 0.45 and fi <= 0.10
            return False

        z = np.array([labs.index(V2_MAP.get(s, 'PERSONAL')) for s in tv])
        cur = in_cv(z)
        while True:
            best = (0.0, None)
            for ii, s in enumerate(tv):
                if Ctr['uni'][ii] < 4: continue
                orig_n = V2_MAP.get(s, 'PERSONAL')
                for cc in tgt_ids:
                    if cc == z[ii]: continue
                    if not role_ok_tr(s, orig_n, labs[cc]): continue
                    z2 = z.copy(); z2[ii] = cc
                    g = cur - in_cv(z2)
                    if g > best[0]: best = (g, (ii, cc))
            if best[1] is None or best[0] < 0.0002: break
            ii, cc = best[1]; z[ii] = cc; cur -= best[0]

        fold_mp = {s: labs[z[ii]] for ii, s in enumerate(tv)}
        m, _ = class_model(Ctr, fold_mp, 'nested_v3', tv)
        for x, k in va_f:
            ids = [tidx[s] for s in x]
            tot_lp += m.logprob(ids, True); tot_n += len(ids)
    return -tot_lp / tot_n


cv5_v1 = score_5fold_map(HAND)
cv5_v2 = score_5fold_map(V2_MAP)
cv5_v3 = score_5fold_map(V3_MAP)
cv5_v3_nested = nested_5fold_v3()
log(f'5-fold Lipi CV (clean out-of-fold texts): v1={cv5_v1:.4f} | v2={cv5_v2:.4f} | v3={cv5_v3:.4f} | v3_strictly_nested={cv5_v3_nested:.4f} bits/sign')

# 2B. Half-A -> Half-B (exact `frame2_kind_redesign.py` protocol, seed=2026) & Unseen `new texts` (482)
rng_ab = np.random.default_rng(2026)
half = rng_ab.random(len(T)) < 0.5
TA = [t for t, h in zip(T, half) if h]
TB_clean = [(x, k) for (x, c, k), h in zip(T, half) if not h and c and not (set(x) & UNK)]
CA, CKA = kind_counts(TA, idx)

uni_m = unigram_model(C_all)
big_m = bigram_model(C_all)
u_bits = bits(FixedKind(uni_m), NEW_482, idx)
b_bits = bits(FixedKind(big_m), NEW_482, idx)
NEW_482_SEALTAG = [(x, 'seal' if k == 'tag' else k) for x, k in NEW_482]

bits_rows = []
for fn, mp in [('v1 hand jobs', HAND), ('v2 base', V2_MAP), ('v3 final', V3_MAP)]:
    mpv = {s: mp.get(s, 'PERSONAL' if fn.startswith('v1') else 'UNSEEN') for s in vocab}
    # Pooled models
    m_ab_pool = class_model_kind(CA, CKA, mpv, fn, vocab, pooled_only=True)
    hb_pool = bits(m_ab_pool, TB_clean, idx)
    m_pool = class_model_kind(C_all, CK_all, mpv, fn, vocab, pooled_only=True)
    new_pool = bits(m_pool, NEW_482, idx)
    mix_pool = bits(mix_kind(FixedKind(big_m), m_pool, 0.5, 'mix'), NEW_482, idx)

    # Kind-redesigned model (BETA chosen on Half-B from 5,20,50,200,1000; sealings->seal)
    hb_grid = {beta: bits(class_model_kind(CA, CKA, mpv, fn, vocab, beta=beta), TB_clean, idx) for beta in (5, 20, 50, 200, 1000)}
    best_beta = min(hb_grid, key=hb_grid.get)
    m_kind = class_model_kind(C_all, CK_all, mpv, fn, vocab, beta=best_beta)
    new_kind = bits(m_kind, NEW_482_SEALTAG, idx)
    mix_kind_b = bits(mix_kind(FixedKind(big_m), m_kind, 0.5, 'mix_k'), NEW_482_SEALTAG, idx)

    # 20 Decoys on Half-B and Unseen new_texts (482)
    dec_hb = []; dec_new = []; dec_mix = []
    for q in DECOY_SEEDS:
        dm = deal_within_bands({s: mp[s] for s in vocab if s in mp}, band, q)
        dmpv = {s: dm.get(s, 'UNSEEN') for s in vocab}
        dec_hb.append(bits(class_model_kind(CA, CKA, dmpv, 'dec', vocab, pooled_only=True), TB_clean, idx))
        md = class_model_kind(C_all, CK_all, dmpv, 'dec', vocab, pooled_only=True)
        dec_new.append(bits(md, NEW_482, idx))
        dec_mix.append(bits(mix_kind(FixedKind(big_m), md, 0.5, 'dmix'), NEW_482, idx))
    dec_hb = np.array(dec_hb); dec_new = np.array(dec_new); dec_mix = np.array(dec_mix)
    z_new = (dec_new.mean() - new_pool) / dec_new.std(ddof=1)

    by_k_new = {KIND_PLAIN[k]: round(bits(m_pool, [(a, kk) for a, kk in NEW_482 if kind_of(kk) == k], idx), 4)
                for k in KINDS if any(kind_of(kk) == k for _, kk in NEW_482)}

    bits_rows.append(dict(
        frame=fn, classes=len(set(mpv.values())),
        cv5_lipi=round(cv5_v1 if fn.startswith('v1') else (cv5_v2 if fn.startswith('v2') else cv5_v3), 4),
        cv5_nested=round(cv5_v3_nested, 4) if fn == 'v3 final' else np.nan,
        halfB_pooled=round(hb_pool, 4), halfB_decoy_mean=round(dec_hb.mean(), 4),
        halfB_by_kind=round(hb_grid[best_beta], 4), best_beta=best_beta,
        new_pooled=round(new_pool, 4), share_captured=round((u_bits - new_pool) / (u_bits - b_bits), 4),
        new_decoy_mean=round(dec_new.mean(), 4), new_decoy_best=round(dec_new.min(), 4),
        decoys_le_real=int((dec_new <= new_pool).sum()), z_new_bits=round(z_new, 2), p_new_bits=float(norm.sf(z_new)),
        new_by_kind_redesign=round(new_kind, 4),
        new_mix_bigram=round(mix_pool, 4), new_mix_kind_bigram=round(mix_kind_b, 4),
        new_mix_decoy_mean=round(dec_mix.mean(), 4),
        **by_k_new
    ))
    log(f"  {fn:14s}: Lipi HalfB={hb_pool:.4f} (by-kind={hb_grid[best_beta]:.4f}, dec={dec_hb.mean():.4f}) | "
        f"Unseen NEW_482={new_pool:.4f} (share={(u_bits-new_pool)/(u_bits-b_bits):.1%}, dec={dec_new.mean():.4f}, best={dec_new.min():.4f}, "
        f"{int((dec_new<=new_pool).sum())}/20, z={z_new:.2f}) | mix={mix_pool:.4f}")

pd.DataFrame(bits_rows).to_csv(os.path.join(OUT_FV3, 'v3_bits_eval.csv'), index=False)

# 2C. 77-item Fill-the-Gap evaluation (`frame2_score.py` exact protocol)
mah2lipi = dict(zip(M.reading_mah, M.tok))
lipikind = {}
for x, k in zip(d.tok, d.kind): lipikind.setdefault('-'.join(x), k)
gap_items = []; seen_g = set()
for g, lt, mt in zip(pairs.group, pairs.lipi_text, pairs.mahadevan_text):
    L = tuple(lt.split('-')); Mt = mah2lipi.get(mt)
    if Mt is None or len(L) != len(Mt): continue
    for gapped, full_ in ((L, Mt), (Mt, L)):
        lost = [i for i, s in enumerate(gapped) if s == '000']
        if len(lost) != 1 or set(full_) & UNK or any(s.startswith('X') for s in full_): continue
        p = lost[0]
        if any(gapped[i] != full_[i] for i in range(len(L)) if i != p): continue
        key = (gapped, full_[p])
        if key in seen_g: continue
        seen_g.add(key); gap_items.append(dict(lipi_text=lt, context=gapped, pos=p, true=full_[p], answer='-'.join(full_), kind=lipikind.get(lt, 'other')))

excl_text = {it['lipi_text'] for it in gap_items} | {it['answer'] for it in gap_items}
excl_ids = {i for i, x in zip(d.id, d.tok) if '-'.join(x) in excl_text}
Tg = train_texts(frozenset(excl_ids)); gv, gidx = vocab_of(Tg); gC, gCK = kind_counts(Tg, gidx)
gbigK = FixedKind(bigram_model(gC))


def gap_score(model):
    h = np.zeros(3)
    for it in gap_items:
        ids = [gidx.get(s) if s != '000' else None for s in it['context']]
        tr = gidx.get(it['true'])
        if tr is None: continue
        p = gap_posteriors(model.get(it['kind']), ids, True)[it['pos']]
        rank = int((p > p[tr]).sum()); h += [rank < 1, rank < 5, rank < 10]
    return h / len(gap_items)


gap_rows = []
for fn, mp in [('v2 base', V2_MAP), ('v3 final', V3_MAP)]:
    gm = class_model_kind(gC, gCK, {s: mp.get(s, 'UNSEEN') for s in gv}, fn, gv, pooled_only=True)
    gs = gap_score(gm); gsm = gap_score(mix_kind(gbigK, gm, 0.5, 'mix'))
    dg = np.array([gap_score(class_model_kind(gC, gCK, {s: deal_within_bands({k: mp[k] for k in vocab if k in mp}, band, q).get(s, 'UNSEEN') for s in gv}, 'd', gv, pooled_only=True)) for q in DECOY_SEEDS])
    gap_rows.append(dict(frame=fn, top1=round(gs[0], 4), top5=round(gs[1], 4), top10=round(gs[2], 4),
                         decoy_top1=round(dg[:, 0].mean(), 4), decoy_top5=round(dg[:, 1].mean(), 4),
                         mix_top1=round(gsm[0], 4), mix_top5=round(gsm[1], 4), mix_top10=round(gsm[2], 4)))
    log(f"  Gap-77 {fn:10s}: alone top1/5/10 = {gs[0]:.1%}/{gs[1]:.1%}/{gs[2]:.1%} (decoy {dg[:,0].mean():.1%}/{dg[:,1].mean():.1%}) | "
        f"mix = {gsm[0]:.1%}/{gsm[1]:.1%}/{gsm[2]:.1%}")
pd.DataFrame(gap_rows).to_csv(os.path.join(OUT_FV3, 'v3_gap_eval.csv'), index=False)


# ==============================================================================
# PART 3: EXPORT FULL SEGMENTED CORPUS (`corpus_parsed_v3.csv`)
# ==============================================================================
log('\n=== PART 3: EXPORTING FULL CORPUS CLAUSE SEGMENTATION (Lipi + Mahadevan) ===')
out_corpus = []

# 3A. All 5,679 Lipi faces
for idx_r, (fid, x, f, kr) in enumerate(zip(d.id, d.tok, d.flg, d.kind)):
    k6 = kind_of(kr)
    intact = bool(x) and not (set(x) & UNK) and not (f & {'broken', 'lost', 'alt'})
    cl2 = [V2_MAP.get(s, 'LOST' if s in UNK else 'PERSONAL') for s in x]
    cl3 = [V3_MAP.get(s, 'LOST' if s in UNK else 'PERSONAL') for s in x]
    if intact:
        p2 = v2_type(cl2, k6) or ('loose name text' if ('CLOSER' in cl2 or 'TITLE' in cl2) else 'other')
        p3, segs = parse_v3(cl3, k6)
        roles = tag_sign_roles(cl3, segs)
    else:
        p2 = 'damaged' if x else 'empty'
        p3, segs = ('damaged' if x else 'empty'), []
        roles = ['damaged' if s in UNK else f'frag:{c.lower()}' for s, c in zip(x, cl3)]

    seg_str = ' | '.join('-'.join(x[a:b]) for a, b, _ in segs) if segs else ''
    ctype_str = ' + '.join(t for _, _, t in segs) if segs else ''
    out_corpus.append(dict(
        catalogue='Lipi',
        id=str(fid),
        ref_id=str(d.cisi.iloc[idx_r]),
        site=str(d.site.iloc[idx_r]),
        object_kind=KIND_PLAIN.get(k6, k6),
        partnered=True,
        intact=intact,
        length=len(x),
        signs='-'.join(x),
        v2_classes='-'.join(cl2),
        v3_classes='-'.join(cl3),
        v2_pattern=p2,
        v3_pattern=p3 if p3 else 'unparsed',
        parsed_v3=bool(intact and p3 != ''),
        clause_count=len(segs),
        clauses_segmented=seg_str,
        clause_types=ctype_str,
        sign_roles=' '.join(roles)
    ))

# 3B. All Mahadevan lines (`M`)
for idx_m, row_m in M.iterrows():
    x = tuple(row_m['tok']) if row_m['tok'] else ()
    kr = str(row_m['kind'])
    k6 = kind_of(kr)
    comp = bool(row_m['complete_b']) and bool(x) and not (set(x) & UNK)
    cl2 = [V2_MAP.get(s, 'LOST' if s in UNK else 'PERSONAL') for s in x]
    cl3 = [V3_MAP.get(s, 'LOST' if s in UNK else 'PERSONAL') for s in x]
    if comp:
        p2 = v2_type(cl2, k6) or ('loose name text' if ('CLOSER' in cl2 or 'TITLE' in cl2) else 'other')
        p3, segs = parse_v3(cl3, k6)
        roles = tag_sign_roles(cl3, segs)
    else:
        p2 = 'damaged'
        p3, segs = 'damaged', []
        roles = ['damaged' if s in UNK else f'frag:{c.lower()}' for s, c in zip(x, cl3)]

    seg_str = ' | '.join('-'.join(x[a:b]) for a, b, _ in segs) if segs else ''
    ctype_str = ' + '.join(t for _, _, t in segs) if segs else ''
    out_corpus.append(dict(
        catalogue='Mahadevan',
        id=str(row_m.get('id', idx_m)),
        ref_id=str(row_m.get('reading_mah', '')),
        site=str(row_m.get('site_l', '')),
        object_kind=KIND_PLAIN.get(k6, k6),
        partnered=bool(row_m['partnered']),
        intact=comp,
        length=len(x),
        signs='-'.join(x),
        v2_classes='-'.join(cl2),
        v3_classes='-'.join(cl3),
        v2_pattern=p2,
        v3_pattern=p3 if p3 else 'unparsed',
        parsed_v3=bool(comp and p3 != ''),
        clause_count=len(segs),
        clauses_segmented=seg_str,
        clause_types=ctype_str,
        sign_roles=' '.join(roles)
    ))

corp_df = pd.DataFrame(out_corpus)
corp_path = os.path.join(OUT_FV3, 'corpus_parsed_v3.csv')
corp_df.to_csv(corp_path, index=False)
log(f'Wrote {corp_path}: {len(corp_df)} total rows ({(corp_df.catalogue=="Lipi").sum()} Lipi, {(corp_df.catalogue=="Mahadevan").sum()} Mahadevan)')

# Export clause-pattern summary table with Lipi + Unseen New examples
lipi_int_df = corp_df[(corp_df.catalogue == 'Lipi') & corp_df.intact]
mu_int_df = corp_df[(corp_df.catalogue == 'Mahadevan') & (~corp_df.partnered) & corp_df.intact]
pat_rows = []
for pat, grp in lipi_int_df.groupby('v3_pattern'):
    mu_sub = mu_int_df[mu_int_df.v3_pattern == pat]
    ex_l = grp.clauses_segmented.iloc[0] if grp.clauses_segmented.iloc[0] else grp.signs.iloc[0]
    ex_m = (mu_sub.clauses_segmented.iloc[0] if mu_sub.clauses_segmented.iloc[0] else mu_sub.signs.iloc[0]) if len(mu_sub) else ''
    pat_rows.append(dict(
        v3_pattern=pat,
        lipi_intact_faces=len(grp),
        lipi_share=round(len(grp) / len(lipi_int_df), 4),
        unseen_mah_complete=len(mu_sub),
        example_lipi=ex_l,
        example_unseen_mah=ex_m
    ))
pd.DataFrame(pat_rows).sort_values('lipi_intact_faces', ascending=False).to_csv(
    os.path.join(OUT_FV3, 'v3_clause_breakdown.csv'), index=False)
