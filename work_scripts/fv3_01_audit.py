#!/usr/bin/env python3
"""FRAME v3 — Step 1: Systematic audit of the 3,600 intact Lipi faces (591 loose name text + 1,192 other).
Strictly uses Lipi (first catalogue `d`) ONLY; unseen Mahadevan `new texts` are NEVER touched here.
Outputs diagnostic tables to `work_data/fv3/` and detailed summary to stdout / `work_data/fv3/audit_summary.txt`.
"""
import os, sys, collections, re
import numpy as np, pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DYN = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
sys.path.insert(0, SCRIPT_DIR)
from frame2_common import *

OUT_FV3 = os.path.join(ROOT_DYN, 'work_data', 'fv3')
os.makedirs(OUT_FV3, exist_ok=True)

c2 = pd.read_csv(f'{OUT2}/classes_v2.csv', dtype=str).fillna('')
V2B = dict(zip(c2.sign, c2.v2_base))

def get_v2_kind(x, k, f):
    if not x: return 'empty'
    if set(x) & UNK or f & {'broken', 'lost', 'alt'}: return 'damaged'
    cl = [V2B.get(s, 'PERSONAL') for s in x]
    t = v2_type(cl, k)
    if t == 'count line': return 'opener + count line' if cl[0] == 'OPEN' else 'bare count line'
    if t: return t
    if 'CLOSER' in cl or 'TITLE' in cl: return 'loose name text'
    return 'other'

# Build intact Lipi dataframe
rows = []
for idx_row, (fid, x, f, k_raw) in enumerate(zip(d.id, d.tok, d.flg, d.kind)):
    k6 = kind_of(k_raw)
    tk = get_v2_kind(x, k6, f)
    intact = (tk not in ('empty', 'damaged'))
    cl = tuple(V2B.get(s, 'LOST' if s in UNK else 'PERSONAL') for s in x)
    rows.append(dict(
        face=fid,
        cisi=d.cisi.iloc[idx_row],
        site=d.site.iloc[idx_row],
        area=str(d['area-section'].iloc[idx_row]),
        raw_kind=k_raw,
        kind=k6,
        kind_plain=KIND_PLAIN.get(k6, k6),
        len=len(x),
        tok=tuple(x),
        signs='-'.join(x),
        cl=cl,
        cl_str=' '.join(cl),
        v2_kind=tk,
        intact=intact
    ))

df = pd.DataFrame(rows)
intact_df = df[df.intact].copy()
# Event deduplication: moulded copies at same site + area + kind + signs count as 1 event
intact_df['event_key'] = intact_df['site'].astype(str) + '|' + intact_df['area'] + '|' + intact_df['raw_kind'] + '|' + intact_df['signs']
events_df = intact_df.drop_duplicates('event_key').copy()
distinct_df = intact_df.drop_duplicates('signs').copy()

lines_out = []
def pr(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    lines_out.append(s)

pr('=== 1. INTACT LIPI OVERVIEW ===')
pr(f'Total Lipi faces: {len(df)}, Intact faces: {len(intact_df)}, Distinct intact Events: {len(events_df)}, Distinct intact Texts: {len(distinct_df)}')
pr('\nBreakdown by v2_kind x kind (All 3,600 intact faces):')
ct = pd.crosstab(intact_df.v2_kind, intact_df.kind, margins=True)
pr(ct.to_string())

pr('\nBreakdown of `other` (1,192) and `loose name text` (591) by raw_kind:')
pr(pd.crosstab(intact_df[intact_df.v2_kind.isin(['loose name text', 'other'])].v2_kind,
               intact_df[intact_df.v2_kind.isin(['loose name text', 'other'])].raw_kind, margins=True).to_string())

pr('\nLength distribution of intact faces by parsed vs loose vs other:')
intact_df['status'] = intact_df.v2_kind.map(lambda k: k if k in ('loose name text', 'other') else 'v2_parsed')
intact_df['len_bin'] = intact_df['len'].map(lambda n: str(n) if n <= 7 else '8+')
pr(pd.crosstab([intact_df.kind, intact_df.status], intact_df.len_bin, margins=True).to_string())

# === 2. DIAGNOSE 591 LOOSE NAME TEXTS ===
pr('\n=== 2. DIAGNOSING 591 LOOSE NAME TEXTS ===')
loose = intact_df[intact_df.v2_kind == 'loose name text'].copy()

def collapse_namesigns(cl):
    NS = {'CREST', 'PERSONAL', 'NUM_NAME', 'NUM_SHORT', 'NUM_TALL', 'PLACE', 'NAME_BACK', 'MEASURE', 'AFTER_M', 'THING'}
    out = []
    for c in cl:
        lbl = 'NS' if c in NS else c
        if out and out[-1] == 'NS' and lbl == 'NS':
            continue
        out.append(lbl)
    return ' '.join(out)

loose['skeleton'] = loose.cl.map(collapse_namesigns)
pr('\nTop 40 structural skeletons in `loose name text` (NS = run of V2_NAMESIGN):')
for sk, grp in loose.groupby('skeleton'):
    pass
sk_counts = loose.groupby('skeleton').size().sort_values(ascending=False)
for sk, cnt in sk_counts.head(40).items():
    k_str = ', '.join(f'{k}:{v}' for k, v in loose[loose.skeleton == sk].kind.value_counts().items())
    ex = loose[loose.skeleton == sk].signs.iloc[0]
    pr(f'  {cnt:4d}  {sk:45s}  [{k_str}]  ex: {ex}')

# Categorize mutually-informative failure reasons for loose name text
def loose_reasons(row):
    cl = list(row.cl)
    tok = list(row.tok)
    reasons = []
    # Check OPEN not at 0
    if 'OPEN' in cl[1:]:
        reasons.append('internal_OPEN')
    # Check SLOT without preceding OPEN or double SLOT
    for i, c in enumerate(cl):
        if c == 'SLOT':
            if i == 0:
                reasons.append('initial_SLOT')
            elif cl[i-1] == 'OPEN':
                pass
            elif cl[i-1] == 'SLOT':
                reasons.append('multi_SLOT')
            else:
                reasons.append(f'mid_SLOT({tok[i]})')
    # Check CLOSER/TITLE not at end
    n = len(cl)
    end_idx = [i for i, c in enumerate(cl) if c in ('CLOSER', 'TITLE')]
    if len(end_idx) >= 2:
        # check if just CLOSER TITLE at end
        if end_idx == [n-2, n-1] and cl[n-2] == 'CLOSER' and cl[n-1] == 'TITLE':
            pass
        else:
            reasons.append(f'multi_END({",".join(cl[i]+":"+tok[i] for i in end_idx)})')
    if end_idx and end_idx[-1] < n - 1:
        after = cl[end_idx[-1]+1:]
        reasons.append(f'post_END({"_".join(after)})')
    if end_idx and end_idx[0] == 0:
        reasons.append('initial_END')
    return '; '.join(dict.fromkeys(reasons)) if reasons else 'other_loose'

loose['reason'] = loose.apply(loose_reasons, axis=1)
pr('\nTop 35 exact failure patterns in `loose name text`:')
for r_str, cnt in loose.reason.value_counts().head(35).items():
    ex = loose[loose.reason == r_str].signs.iloc[0]
    pr(f'  {cnt:4d}  {r_str:55s}  ex: {ex}')

# === 3. DIAGNOSE 1,192 OTHER FACES ===
pr('\n=== 3. DIAGNOSING 1,192 OTHER FACES ===')
oth = intact_df[intact_df.v2_kind == 'other'].copy()

def collapse_runs(cl):
    out = []
    for c in cl:
        if out and out[-1].startswith(c) and c in ('PERSONAL', 'CREST', 'NUM_SHORT', 'NUM_TALL'):
            if not out[-1].endswith('+'): out[-1] = c + '+'
        else:
            out.append(c)
    return ' '.join(out)

oth['skeleton'] = oth.cl.map(collapse_runs)
pr('\nTop 45 class skeletons in `other` across all kinds:')
for sk, cnt in oth.skeleton.value_counts().head(45).items():
    k_str = ', '.join(f'{k}:{v}' for k, v in oth[oth.skeleton == sk].kind.value_counts().items())
    ex = oth[oth.skeleton == sk].signs.iloc[0]
    pr(f'  {cnt:4d}  {sk:45s}  [{k_str}]  ex: {ex}')

for k in ['seal', 'mtab', 'ctab', 'tag', 'pot', 'other']:
    sub = oth[oth.kind == k]
    pr(f'\n--- `other` on {k} ({len(sub)} faces, len1={(sub["len"]==1).sum()}, len2={(sub["len"]==2).sum()}, len3+={(sub["len"]>=3).sum()}) ---')
    for sk, cnt in sub.skeleton.value_counts().head(15).items():
        ex = sub[sub.skeleton == sk].signs.iloc[0]
        pr(f'  {cnt:4d}  {sk:42s}  ex: {ex}')
    # Final signs on len >= 2 `other` faces of this kind
    sub2 = sub[sub['len'] >= 2]
    fin_cnt = collections.Counter(x[-1] for x in sub2.tok)
    pr(f'  Top final signs (len>=2) on {k} `other`: ' + ', '.join(f'{s}({V2B.get(s,"P")}):{n}' for s, n in fin_cnt.most_common(15)))
    init_cnt = collections.Counter(x[0] for x in sub2.tok)
    pr(f'  Top initial signs (len>=2) on {k} `other`: ' + ', '.join(f'{s}({V2B.get(s,"P")}):{n}' for s, n in init_cnt.most_common(12)))

# === 4. POSITIONAL & LIKELIHOOD PROFILE OF SIGNS IN LIPI ===
pr('\n=== 4. LIPI SIGN POSITIONAL PROFILES & 5-FOLD CV BITS-PER-SIGN CLASS MOVES ===')
T = train_texts()
vocab, idx = vocab_of(T)
V = len(vocab)

# Compute positional stats on intact distinct Lipi texts (length >= 2)
clean_distinct = [x for x, c, k in T if c and len(x) >= 2]
tot_occ = collections.Counter()
init_occ = collections.Counter()
fin_occ = collections.Counter()
after_open_occ = collections.Counter()
after_num_occ = collections.Counter()
before_num_occ = collections.Counter()
after_closer_occ = collections.Counter()
before_closer_occ = collections.Counter()

NUM_SET = {s for s in vocab if V2B.get(s) in ('NUM_SHORT', 'NUM_TALL', 'NUM_NAME')}
OPEN_SET = {s for s in vocab if V2B.get(s) == 'OPEN'}
CLOSER_SET = {s for s in vocab if V2B.get(s) == 'CLOSER'}

for x in clean_distinct:
    for i, s in enumerate(x):
        tot_occ[s] += 1
        if i == 0: init_occ[s] += 1
        if i == len(x) - 1: fin_occ[s] += 1
        if i > 0 and x[i-1] in OPEN_SET: after_open_occ[s] += 1
        if i > 0 and x[i-1] in NUM_SET: after_num_occ[s] += 1
        if i + 1 < len(x) and x[i+1] in NUM_SET: before_num_occ[s] += 1
        if i > 0 and x[i-1] in CLOSER_SET: after_closer_occ[s] += 1
        if i + 1 < len(x) and x[i+1] in CLOSER_SET: before_closer_occ[s] += 1

# 5-fold CV on T for single-sign class reassignments among the 14 v2 classes
rng = np.random.default_rng(2026)
folds = rng.integers(0, 5, size=len(T))

def prep_fold(f):
    tr = [t for t, fl in zip(T, folds) if fl != f]
    va = [t for t, fl in zip(T, folds) if fl == f]
    Ctr = counts(tr, idx)
    def flat_t(txts):
        a, b, st, en = [], [], [], []
        for x, clean, k in txts:
            ids = [idx[s] for s in x if s in idx]
            if len(ids) != len(x): continue
            for p, q in zip(ids, ids[1:]): a.append(p); b.append(q)
            if clean: st.append(ids[0]); en.append(ids[-1])
        return np.array(a, int), np.array(b, int), np.array(st, int), np.array(en, int)
    aA, bA, sA, eA = flat_t(tr)
    aB, bB, sB, eB = flat_t(va)
    ntokB = sum(len(x) for x, c, k in va if all(s in idx for s in x))
    return dict(uniA=Ctr['uni'], aA=aA, bA=bA, sA=sA, eA=eA, aB=aB, bB=bB, sB=sB, eB=eB, ntokB=ntokB)

FOLD_DATA = [prep_fold(f) for f in range(5)]

def cv5_bits(z, K):
    tot_ll = 0.0
    tot_n = 0
    for fd in FOLD_DATA:
        uniA = fd['uniA']
        nk = np.bincount(z, minlength=K); cu = np.bincount(z, uniA, K)
        em = (uniA + 0.5) / (cu[z] + 0.5 * nk[z])
        cb = np.bincount(z[fd['aA']] * K + z[fd['bA']], minlength=K * K).reshape(K, K).astype(float)
        ce = np.bincount(z[fd['eA']], minlength=K).astype(float)
        rows_m = np.concatenate([cb, ce[:, None]], 1) + 0.1
        rows_m /= rows_m.sum(1, keepdims=True)
        cs = np.bincount(z[fd['sA']], minlength=K) + 0.1
        cs /= cs.sum()
        lem = np.log2(em)
        ll = (np.log2(cs[z[fd['sB']]]) + lem[fd['sB']]).sum() + \
             (np.log2(rows_m[z[fd['aB']], z[fd['bB']]]) + lem[fd['bB']]).sum() + \
             np.log2(rows_m[z[fd['eB']], K]).sum()
        tot_ll += ll
        tot_n += fd['ntokB']
    return -tot_ll / tot_n

labs = list(V2_CLASSES)
K = len(labs)
z0 = np.array([labs.index(V2B.get(s, 'PERSONAL')) for s in vocab])
base_cv = cv5_bits(z0, K)
pr(f'5-fold Lipi CV baseline (v2_base, 14 classes): {base_cv:.5f} bits/sign')

C_all = counts(T, idx)
move_rows = []
for i, s in enumerate(vocab):
    u = int(C_all['uni'][i])
    if u < 5: continue
    cur_c = z0[i]
    best_g = 0.0
    best_c = cur_c
    gains = {}
    for c in range(K):
        if c == cur_c: continue
        z1 = z0.copy(); z1[i] = c
        g = base_cv - cv5_bits(z1, K)
        gains[labs[c]] = g
        if g > best_g:
            best_g = g
            best_c = c
    occ = tot_occ[s]
    move_rows.append(dict(
        sign=s, uses=u, occ_len2p=occ,
        v2_class=labs[cur_c],
        best_cv_class=labs[best_c],
        cv_gain_bits_per_sign=round(best_g, 6),
        cv_gain_total_bits=round(best_g * C_all['uni'].sum(), 2),
        p_init=round(init_occ[s] / occ, 3) if occ else 0.0,
        p_fin=round(fin_occ[s] / occ, 3) if occ else 0.0,
        p_after_open=round(after_open_occ[s] / occ, 3) if occ else 0.0,
        p_after_num=round(after_num_occ[s] / occ, 3) if occ else 0.0,
        p_before_num=round(before_num_occ[s] / occ, 3) if occ else 0.0,
        p_after_closer=round(after_closer_occ[s] / occ, 3) if occ else 0.0,
        p_before_closer=round(before_closer_occ[s] / occ, 3) if occ else 0.0,
    ))

mdf = pd.DataFrame(move_rows).sort_values('cv_gain_bits_per_sign', ascending=False)
mdf.to_csv(f'{OUT_FV3}/sign_cv_moves.csv', index=False)

pr('\nTop 50 single-sign class moves by 5-fold Lipi CV bits/sign gain (uses >= 5):')
pr(mdf.head(50).to_string(index=False))

pr('\nPERSONAL signs with strong final rate (p_fin >= 0.35, occ_len2p >= 8):')
p_fin_df = mdf[(mdf.v2_class == 'PERSONAL') & (mdf.p_fin >= 0.35) & (mdf.occ_len2p >= 8)].sort_values(['p_fin', 'uses'], ascending=False)
pr(p_fin_df.to_string(index=False))

pr('\nPERSONAL signs with strong initial rate (p_init >= 0.45, occ_len2p >= 8):')
p_init_df = mdf[(mdf.v2_class == 'PERSONAL') & (mdf.p_init >= 0.45) & (mdf.occ_len2p >= 8)].sort_values(['p_init', 'uses'], ascending=False)
pr(p_init_df.to_string(index=False))

pr('\nPERSONAL signs with strong after-number rate (p_after_num >= 0.35, occ_len2p >= 6):')
p_anum_df = mdf[(mdf.v2_class == 'PERSONAL') & (mdf.p_after_num >= 0.35) & (mdf.occ_len2p >= 6)].sort_values(['p_after_num', 'uses'], ascending=False)
pr(p_anum_df.to_string(index=False))

loose.to_csv(f'{OUT_FV3}/audit_loose_591.csv', index=False)
oth.to_csv(f'{OUT_FV3}/audit_other_1192.csv', index=False)
open(f'{OUT_FV3}/audit_summary.txt', 'w').write('\n'.join(lines_out) + '\n')
pr('\nAudit written to work_data/fv3/')
