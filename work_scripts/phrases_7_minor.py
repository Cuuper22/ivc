#!/usr/bin/env python3
"""PHRASES step 7 (new idea after the house test went flat): MINOR phrases, the ones too rare for the main rule. Written 2026-11-17 before the run.
Reason: a house or family phrase belongs to few objects by nature, so the 8-text rule (and the top-100 cut) favours city-wide phrases and
starves the house kind. Test: relax the count to 4-7 distinct texts, keep order >= 90% and lift >= 5, keep phrases not nested in a main phrase
(a run contained in a main phrase is left out), and run the same shared-building test with copies removed (identical text in the same building
counts once), carriers drawn within site and object kind (1,000 draws, seed 7).
  Flag HOUSE_MINOR: >= 5 carriers with building known, P <= 0.01. Pooled Z over all minor phrases and by group.
  Control A: the same minor rule on first-catalogue texts with sign order shuffled inside runs (20 shuffles): how many minor phrases pass.
  Control B: the P histogram (5% of phrases should fall under 0.05 by chance).
PREDICTION: some minor name phrases are house-bound (shared building above chance), at least 5 flagged; the pooled Z over minor names is > 2.
Output: work_data/phrases/minor_phrases.csv, minor_control.csv, log_7.txt
"""
from phrases_common import *
import random
from scipy.stats import norm
LOG = open(f'{OUTP}/log_7.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n'); LOG.flush()
rng = np.random.default_rng(7)
NMIN, NMAX, ORDER, LIFT = 4, 7, 0.90, 5.0
T = distinct_texts(); nt, win, uni, N = count_phrases(T)
main = set(tuple(s.split('-')) for s in pd.read_csv(f'{OUTP}/phrase_list.csv', dtype={'phrase': str}).phrase)
def minor(nt, win, uni, N):
    out = {}
    for k in (2, 3, 4):
        for p, n in nt[k].items():
            if n < NMIN or n > NMAX: continue
            rev = nt[k].get(p[::-1], 0) if p != p[::-1] else n
            if p == p[::-1] or n / (n + rev) < ORDER: continue
            e = expected(p, uni, N, win[k])
            if e > 0 and n / e >= LIFT: out[p] = dict(n=n, rev=rev, lift=n / e)
    return out
Mn = minor(nt, win, uni, N)
def nested_in_main(p): return any(len(q) > len(p) and any(q[i:i + len(p)] == p for i in range(len(q) - len(p) + 1)) for q in main)
Mn = {p: v for p, v in Mn.items() if not nested_in_main(p) and p not in main}
say('minor phrases (4-7 texts, order>=90%, lift>=5, not inside a main phrase):', len(Mn), {k: sum(1 for p in Mn if len(p) == k) for k in (2, 3, 4)})
# control A
ctl = []
def shuffled(texts, seed):
    r = random.Random(seed); out = []
    for x in texts:
        y = list(x); i = 0; n = len(y)
        while i < n:
            if not is_sign(y[i]): i += 1; continue
            j = i
            while j < n and is_sign(y[j]): j += 1
            seg = y[i:j]; r.shuffle(seg); y[i:j] = seg; i = j
        out.append(tuple(y))
    return out
for sd in range(800, 820):
    a, b, c_, N_ = count_phrases(shuffled(T, sd)); ctl.append(len(minor(a, b, c_, N_)))
say('control A: minor phrases passing in shuffled corpora: mean', np.mean(ctl), 'max', max(ctl))
pd.DataFrame(dict(seed=range(800, 820), minor_passing=ctl)).to_csv(f'{OUTP}/minor_control.csv', index=False)
# carriers
cand = set(Mn); car = collections.defaultdict(set)
for o, x in zip(d.obj, d.tok):
    if not x: continue
    for r in runs(x):
        for k in (2, 3, 4):
            for i in range(len(r) - k + 1):
                p = r[i:i + k]
                if p in cand: car[p].add(str(o))
O = build_objects(); O = O[O.site != 'Unknown']
O['kg'] = O.kind.where(O.kind.isin(['seal', 'mtab', 'tag', 'pot', 'ctab']), 'other')
TXT = d.groupby('obj').tok.first(); TXT.index = TXT.index.astype(str)
code = pd.factorize(O.building.where(O.building != '', None))[0]; pos = {o: i for i, o in enumerate(O.index)}
site = O.site.values; kg = O.kg.values
pool = {}
for s_ in np.unique(site):
    for k_ in np.unique(kg):
        ix = np.where((site == s_) & (kg == k_) & (code >= 0))[0]
        if len(ix): pool[(s_, k_)] = ix
D = 1000
rows = []
for p, v in Mn.items():
    S = [pos[o] for o in car[p] if o in pos]
    seen = set(); S2 = []
    for i in S:
        if code[i] < 0: S2.append(i); continue
        key = (TXT[O.index[i]], code[i])
        if key not in seen: seen.add(key); S2.append(i)
    strata = collections.defaultdict(list)
    for i in S2:
        if code[i] >= 0: strata[(site[i], kg[i])].append(code[i])
    nk = sum(len(x) for x in strata.values()); obs = sum(len(x) - len(set(x)) for x in strata.values())
    null = np.zeros(D)
    for (s_, k_), x in strata.items():
        pl = pool.get((s_, k_))
        if pl is None or len(pl) < len(x): continue
        c = code[pl]
        for t in range(D): null[t] += len(x) - len(set(rng.choice(c, len(x), replace=False).tolist()))
    P = (np.sum(null >= obs) + 1) / (D + 1) if nk >= 5 else np.nan
    cl = [v2c(s) for s in p]
    grp = 'front' if any(c in ('OPEN', 'SLOT') for c in cl) else ('count line' if any(c in ('NUM_SHORT', 'NUM_TALL', 'MEASURE') for c in cl) else ('ending' if len(p) == 2 and cl[-1] in ('CLOSER', 'TITLE') else 'name'))
    rows.append(dict(phrase='-'.join(p), group=grp, n_texts=v['n'], lift=round(v['lift'], 1), n_objects=len(S), n_after_copies=len(S2), n_bld_known=nk, shared=obs, null_mean=float(null.mean()), null_sd=float(null.std()), P=P,
                     cities=len({site[i] for i in S}), buildings='; '.join(sorted({O.building.values[i].split('|', 1)[-1] for i in S2 if code[i] >= 0}))[:120]))
R = pd.DataFrame(rows).sort_values('P'); R.to_csv(f'{OUTP}/minor_phrases.csv', index=False)
t = R[R.P.notna()]
say('tested (5+ carriers with a building):', len(t), ' P<=0.05:', int((t.P <= 0.05).sum()), '(chance', round(0.05 * len(t), 1), ') P<=0.01:', int((t.P <= 0.01).sum()), '(chance', round(0.01 * len(t), 1), ')')
for g, X in list(t.groupby('group')) + [('ALL', t)]:
    z = (X.shared - X.null_mean).sum() / np.sqrt((X.null_sd ** 2).sum()); say(f'pooled {g}: phrases {len(X)}, shared {int(X.shared.sum())}, expected {X.null_mean.sum():.1f}, Z {z:.2f}, P {1 - norm.cdf(z):.4f}')
say(t.head(15)[['phrase', 'group', 'n_texts', 'n_objects', 'n_after_copies', 'n_bld_known', 'shared', 'null_mean', 'P', 'cities', 'buildings']].to_string(index=False))
