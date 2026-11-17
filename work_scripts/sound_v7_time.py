#!/usr/bin/env python3
"""JOB 2: the time test. Predictions and rules: sound_v7_time_pred.py (written before this file ran).
Outputs: work_data/sound_v7/time_values.csv (one row per value: per-bin uses, share, base, held / failed / no data),
         time_facets.csv (sameness P per facet), time_testing.csv (rival words chosen on the early bin), time_log.txt.
Run: python3 sound_v7_time.py   (progress prints as it goes)"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound_v7_common import *
from sound_v7_time_pred import CLASS, RIVALS
from scipy.stats import chi2_contingency
V, STRICT, WIDE = load_values()
STATUS = dict(zip(V.sign, V.status))
NUM = set(VAL)
FISHC = {'220', '226', '231', '233', '235', '236', '240'}
TITLES = {'090', '400', '520', '368', '525', '526', '527', '617', '679', '717', '842'} | set(PORTER) | {'152', '161'}
CLOSE = TITLES | {'740'}
HEAD = {'920', '900', '550', '555', '820', '692'}
LOG = open(f'{OUT7}/time_log.txt', 'w')
def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n')

F = dated_faces()
log(f'[time] dated Lipi faces: {len(F)}; by bin', collections.Counter(b for _, _, _, b, _, _ in F))

def sig(cls, x, i, kind):
    """does the use of x[i] show the class signature?"""
    a = x[i]; n = len(x)
    if cls == 'NAME': return any(y in CLOSE for y in x[i + 1:])
    if cls == 'TITLE': return i == n - 1
    if cls == 'ENDING': return i == n - 1 or (i + 1 < n and x[i + 1] in TITLES)
    if cls == 'KIN': return i + 1 < n and x[i + 1] == '740'
    if cls == 'MEASURE': return i + 1 < n and x[i + 1] in NUM
    if cls == 'THING': return i > 0 and x[i - 1] in NUM
    if cls == 'OPENER': return i == 0
    if cls == 'GOODS': return kind != 'seal'
    if cls == 'KINDRED': return any(y in FISHC for y in x)
    if cls == 'JOINER': return i > 0 and x[i - 1] in HEAD
    if cls == 'LOAD': return i + 1 < n and x[i + 1] == '806'
    raise ValueError(cls)

# every use of every non-number sign, with its bin
USES = collections.defaultdict(list)        # sign -> list of (bin, x, i, kind, site)
ALLU = []                                   # (bin, x, i, kind)
for x, kind, site, b, st, o in F:
    for i, a in enumerate(x):
        if a in NUM or a in ('000', 'ALT'): continue
        USES[a].append((b, x, i, kind, site)); ALLU.append((b, x, i, kind))
CLASSES = sorted(set(CLASS.values()))
BASE = {(c, b): np.mean([sig(c, x, i, k) for bb, x, i, k in ALLU if bb == b]) for c in CLASSES for b in BINS}
for c in CLASSES: log(f'  base {c:8s}', ' '.join(f'{b} {BASE[(c, b)]:.1%}' for b in BINS))

def per_bin(s, cls):
    out = {}
    for b in BINS:
        u = [(x, i, k) for bb, x, i, k, _ in USES.get(s, []) if bb == b]
        k_ = sum(sig(cls, x, i, k) for x, i, k in u); n = len(u)
        out[b] = (k_, n, BASE[(cls, b)])
    return out
def verdict(k, n, base): return 'no data' if n < 3 else ('held' if k / n > base else 'failed')

def instead(s, b):
    """what the sign did in bin b: its commonest slot, kind and neighbours"""
    u = [(x, i, k) for bb, x, i, k, _ in USES[s] if bb == b]
    pos = collections.Counter('first' if i == 0 else 'last' if i == len(x) - 1 else 'middle' for x, i, k in u)
    nx = collections.Counter(x[i + 1] if i + 1 < len(x) else 'end' for x, i, k in u)
    pv = collections.Counter(x[i - 1] if i else 'start' for x, i, k in u)
    kd = collections.Counter(k for x, i, k in u)
    return f'slots {dict(pos)}; before it {pv.most_common(2)}; after it {nx.most_common(2)}; kinds {dict(kd)}'

rows = []
log('\n[time] values by bin (k of n show the signature, against the bin base)')
for s, cls in sorted(CLASS.items()):
    if STATUS.get(s) not in ('strict', 'wide'): continue
    pb = per_bin(s, cls)
    vs = {b: verdict(*pb[b]) for b in BINS}
    held = sum(v == 'held' for v in vs.values()); data = sum(v != 'no data' for v in vs.values())
    r = dict(sign=s, status=STATUS[s], sound=V.set_index('sign').sound[s], cls=cls, bins_with_data=data, bins_held=held)
    for b in BINS:
        k, n, base = pb[b]; r[f'{b}_k'] = k; r[f'{b}_n'] = n; r[f'{b}_base'] = round(base, 4); r[f'{b}'] = vs[b]
    r['instead'] = ' || '.join(f'{b}: {instead(s, b)}' for b in BINS if vs[b] == 'failed')
    rows.append(r)
    log(f'  {s} {cls:8s} ' + '  '.join(f'{b[0]} {pb[b][0]}/{pb[b][1]} ({vs[b]})' for b in BINS))
T = pd.DataFrame(rows); T.to_csv(f'{OUT7}/time_values.csv', index=False)
log('\n[time] SUMMARY')
for dd in (3, 2, 1, 0):
    sub = T[T.bins_with_data == dd]
    log(f'  values with data in {dd} bins: {len(sub)}; held in all of them: {int((sub.bins_held == dd).sum())}; distribution of bins held:', dict(sub.bins_held.value_counts().sort_index()))
for b in BINS:
    sub = T[T[b] != 'no data']; log(f'  bin {b}: data {len(sub)}, held {int((sub[b] == "held").sum())} ({(sub[b] == "held").mean():.0%})')
tot = T[T.bins_with_data > 0]
log(f'  all values with any data: {len(tot)}; held in every bin with data: {int((tot.bins_held == tot.bins_with_data).sum())}')

# ---- rival: shuffled classes ----
log('\n[time] RIVAL: classes shuffled among the values, 1,000 times')
rng7 = np.random.default_rng(7)
signs = list(T.sign); cls_list = list(T.cls)
cache = {}
def held_all(s, c):
    if (s, c) not in cache:
        pb = per_bin(s, c); vs = [verdict(*pb[b]) for b in BINS]
        cache[(s, c)] = (all(v != 'failed' for v in vs) and any(v == 'held' for v in vs), sum(v == 'held' for v in vs), sum(v != 'no data' for v in vs))
    return cache[(s, c)]
for s in signs:
    for c in CLASSES: held_all(s, c)
obs3 = sum(held_all(s, c)[0] for s, c in zip(signs, cls_list))
obs_full3 = sum(held_all(s, c)[1] == 3 for s, c in zip(signs, cls_list))
sims = []; sims3 = []
for _ in range(1000):
    p = rng7.permutation(cls_list)
    sims.append(sum(held_all(s, c)[0] for s, c in zip(signs, p))); sims3.append(sum(held_all(s, c)[1] == 3 for s, c in zip(signs, p)))
sims = np.array(sims); sims3 = np.array(sims3)
log(f'  held in every bin with data: real {obs3} of {len(signs)}, shuffled mean {sims.mean():.1f} (max {sims.max()}), P {(np.sum(sims >= obs3) + 1) / 1001:.4f}')
log(f'  held in all three bins: real {obs_full3}, shuffled mean {sims3.mean():.1f} (max {sims3.max()}), P {(np.sum(sims3 >= obs_full3) + 1) / 1001:.4f}')

# ---- sameness facets ----
log('\n[time] SAMENESS: slot, kind, left and right neighbour across bins (bins shuffled within site among the sign\'s uses, 2,000 times)')
def ncls(a):
    if a in ('start', 'end'): return a
    if a in NUM: return 'number'
    if a == '740': return 'jar'
    if a in FISHC: return 'crest'
    if a in TITLES: return 'title'
    return 'other'
def facet_vals(u, f):
    if f == 'slot': return ['first' if i == 0 else 'last' if i == len(x) - 1 else 'middle' for b, x, i, k, st in u]
    if f == 'kind': return [k if k in ('seal', 'mtab') else 'goods' for b, x, i, k, st in u]
    if f == 'left': return [ncls(x[i - 1] if i else 'start') for b, x, i, k, st in u]
    if f == 'right': return [ncls(x[i + 1] if i + 1 < len(x) else 'end') for b, x, i, k, st in u]
def chi(bins, vals):
    """chi-square of the bin x category table (numpy; bins and vals are integer-coded arrays)"""
    tab = np.zeros((3, vals.max() + 1)); np.add.at(tab, (bins, vals), 1)
    tab = tab[tab.sum(axis=1) > 0][:, tab.sum(axis=0) > 0]
    if tab.shape[0] < 2 or tab.shape[1] < 2: return 0.0
    e = tab.sum(axis=1, keepdims=True) * tab.sum(axis=0, keepdims=True) / tab.sum()
    return float(((tab - e) ** 2 / e).sum())
frows = []
rngf = np.random.default_rng(17)
for j, s in enumerate(signs):
    u = USES[s]; nb = collections.Counter(b for b, *_ in u)
    if sum(v >= 3 for v in nb.values()) < 2: continue
    bins = np.array([BINS.index(b) for b, *_ in u]); sites = np.array([st for *_, st in u])
    r = dict(sign=s, cls=CLASS[s], uses=len(u))
    for f in ('slot', 'kind', 'left', 'right'):
        vals = pd.factorize(pd.Series(facet_vals(u, f)))[0]; obs = chi(bins, vals)
        if obs == 0: r[f] = np.nan; continue
        ge = 0
        for _ in range(2000):
            sh = bins.copy()
            for st in set(sites):
                m = np.where(sites == st)[0]
                if len(m) > 1: sh[m] = rngf.permutation(sh[m])
            ge += chi(sh, vals) >= obs - 1e-9
        r[f] = (ge + 1) / 2001
    frows.append(r)
    if (j + 1) % 20 == 0: log(f'  ... {j + 1} of {len(signs)} values')
FT = pd.DataFrame(frows); FT.to_csv(f'{OUT7}/time_facets.csv', index=False)
for f in ('slot', 'kind', 'left', 'right'):
    col = FT[f].dropna(); log(f'  facet {f}: {len(col)} values tested, changed at P<=0.05: {int((col <= 0.05).sum())} ({(col <= 0.05).mean():.0%}); expected by chance about {0.05 * len(col):.1f}')
anych = FT[[c for c in ('slot', 'kind', 'left', 'right')]].le(0.05).any(axis=1)
log(f'  values with any facet changed at P<=0.05: {int(anych.sum())} of {len(FT)}')
log('  changed:', '; '.join(f"{r.sign} ({','.join(f for f in ('slot', 'kind', 'left', 'right') if r[f] <= 0.05)})" for _, r in FT[anych].iterrows()))

# ---- testing values: choose on the early bin, check on middle and late ----
log('\n[time] TESTING VALUES: rival words chosen on the early bin only')
trows = []
def ratio(k, n, base): return (k / n) / base if n and base else np.nan
for s, (wa, ca, wb, cb) in sorted(RIVALS.items()):
    pa = per_bin(s, ca); pbb = per_bin(s, cb)
    r = dict(sign=s, word_a=wa, class_a=ca, word_b=wb, class_b=cb)
    for b in BINS:
        r[f'{b}_n'] = pa[b][1]; r[f'{b}_a'] = f'{pa[b][0]}/{pa[b][1]} (base {pa[b][2]:.0%})'; r[f'{b}_b'] = f'{pbb[b][0]}/{pbb[b][1]} (base {pbb[b][2]:.0%})'
        r[f'{b}_ra'] = ratio(*pa[b]); r[f'{b}_rb'] = ratio(*pbb[b])
    if pa['early'][1] < 3: r['choice_early'] = 'too few early uses'
    else: r['choice_early'] = 'A' if r['early_ra'] > r['early_rb'] else 'B' if r['early_rb'] > r['early_ra'] else 'tie'
    for b in ('middle', 'late'):
        if r['choice_early'] in ('A', 'B') and pa[b][1] >= 3:
            win = 'A' if r[f'{b}_ra'] > r[f'{b}_rb'] else 'B' if r[f'{b}_rb'] > r[f'{b}_ra'] else 'tie'
            r[f'check_{b}'] = 'kept' if win == r['choice_early'] else ('tie' if win == 'tie' else 'flipped')
        else: r[f'check_{b}'] = 'no data' if pa[b][1] < 3 else ''
    # redesign (written in the predictions' spirit, run only for values the early bin cannot decide): choose on early + late (the two
    # bins that do NOT dominate), check on middle
    ea = [pa['early'][0] + pa['late'][0], pa['early'][1] + pa['late'][1]]; eb = [pbb['early'][0] + pbb['late'][0], pbb['early'][1] + pbb['late'][1]]
    basea = (pa['early'][2] * pa['early'][1] + pa['late'][2] * pa['late'][1]) / max(1, ea[1]); baseb = (pbb['early'][2] * pbb['early'][1] + pbb['late'][2] * pbb['late'][1]) / max(1, eb[1])
    if ea[1] >= 3:
        ra, rb = ratio(ea[0], ea[1], basea), ratio(eb[0], eb[1], baseb)
        r['choice_el'] = 'A' if ra > rb else 'B' if rb > ra else 'tie'
        if pa['middle'][1] >= 3 and r['choice_el'] in ('A', 'B'):
            win = 'A' if r['middle_ra'] > r['middle_rb'] else 'B' if r['middle_rb'] > r['middle_ra'] else 'tie'
            r['check_el_middle'] = 'kept' if win == r['choice_el'] else ('tie' if win == 'tie' else 'flipped')
        else: r['check_el_middle'] = 'no data'
    else: r['choice_el'] = 'too few'; r['check_el_middle'] = ''
    trows.append(r)
    log(f"  {s}: A {wa} [{ca}] / B {wb} [{cb}]  early A {r['early_a']} B {r['early_b']} -> {r['choice_early']}; middle {r['check_middle']}, late {r['check_late']}; early+late -> {r['choice_el']}, middle {r['check_el_middle']}")
TT = pd.DataFrame(trows); TT.to_csv(f'{OUT7}/time_testing.csv', index=False)
log('  early choice:', dict(TT.choice_early.value_counts()), ' middle check:', dict(TT.check_middle.value_counts()), ' late check:', dict(TT.check_late.value_counts()))
log('  early+late choice:', dict(TT.choice_el.value_counts()), ' middle check:', dict(TT.check_el_middle.value_counts()))
LOG.close()
