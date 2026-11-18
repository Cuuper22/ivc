#!/usr/bin/env python3
"""SPOTS, lead 2: sign 061/820 (quarter) before sign 142 (staff-person): one office-holder per quarter of the city?

Plain words:
- OFFICE OBJECT = an undamaged object whose name, opener or ending carries sign 142 (names_all.csv, as registry_offices.py).
- HOLDER KEY = the crest of its name (first non-number sign) with the quarter signs 061/820 and 142 itself skipped, so the
  key is the family emblem of the person, not the office words. A second key keeps the registry crest unchanged.
- AREA / BLOCK = excavation area and block of the findspot. SHUFFLE = holder keys mixed among the located office objects
  of the same city, findspots fixed; P = share of shuffles at least as strong as the real count (low side).
- TIME BIN = early / middle / late from work_data/time/time_axis.csv.

PREDICTIONS (written before any number below was computed):
 (a) One holder per quarter: office objects with DIFFERENT holder keys sit in the same area (or block) less often than
     shuffled (fewer cross-holder same-area pairs), and objects with the SAME key sit in different areas less often.
     Strongest at block level at Mohenjo-daro.
 (b) The pair 061/820+142 carries a count run just before the quarter sign (first, second, third quarter) in more of its
     texts than other 061 texts do, and the ward signs 741/742/745 stand in the pair's texts more than in other texts.
 (c) A holder key that holds 142 in one time bin holds it again in another bin more often than shuffled bins.
 (d) Other signs with the same job: at least one sign beside 142 shows one-holder-per-area at P<0.05 beyond the number
     expected by chance from the number of signs tested.
Writes work_data/spots/s2_*.csv and s2_log.txt.  Run: python3 spots_2_office.py  (about 1 min; prints progress)
"""
import os, re, sys, io, contextlib, collections, random
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
random.seed(202); np.random.seed(202)
ROOT = '/home/antigravity/Cuuper22/ivc'; OUT = f'{ROOT}/work_data/spots'; os.makedirs(OUT, exist_ok=True)
LOG = open(f'{OUT}/s2_log.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n')
print('[s2] loading ...', flush=True)
with contextlib.redirect_stdout(io.StringIO()):
    from time_common import d, M, objs, NUM, runs, T
from scipy.stats import fisher_exact
A = pd.read_csv(f'{ROOT}/work_data/registry/names_all.csv', dtype=str).fillna('')
A = A[(A.damaged == 'False') & (A.goods_line == 'False')].drop_duplicates('object_id').copy()
QUART = {'061', '820'}; CNT = set(NUM)
def toks(r): return (r.opener + '-' + r.name_full + '-' + r.ending_signs).split('-')
def holder(r, skip=QUART | {'142'}):
    core = [s for s in r.name_full.split('-') if s and s not in CNT and s not in skip]
    return core[0] if core else '(none)'
A['sig'] = A.apply(toks, axis=1)
K = A[A.sig.map(lambda t: '142' in t)].copy()
K['hold'] = K.apply(holder, axis=1)
say('[s2] office objects with 142:', K.groupby('site').size().to_dict())

NSH = 5000
def cross_stats(keys, locs):
    """pairs in the same place with different keys; pairs with the same key in different places"""
    n = len(keys); same_place_diff = same_key_diff_place = 0
    for i in range(n):
        for j in range(i + 1, n):
            sp = locs[i] == locs[j]; sk = keys[i] == keys[j] and keys[i] != '(none)'
            if sp and not sk: same_place_diff += 1
            if sk and not sp: same_key_diff_place += 1
    return same_place_diff, same_key_diff_place
def run_cross(keys, locs, nsh=NSH):
    keys = list(keys); locs = list(locs)
    o1, o2 = cross_stats(keys, locs); a1 = np.zeros(nsh); a2 = np.zeros(nsh)
    for t in range(nsh):
        k2 = keys[:]; random.shuffle(k2); a1[t], a2[t] = cross_stats(k2, locs)
    return (o1, a1.mean(), (1 + (a1 <= o1).sum()) / (nsh + 1)), (o2, a2.mean(), (1 + (a2 <= o2).sum()) / (nsh + 1))

# ---------------- (a) ----------------
say('\n(a) Are the holders of 142 spread one per area/block more than chance?')
say('    cross = pairs of 142-objects in the SAME place with DIFFERENT holder (fewer = one holder per place);'
    ' apart = pairs with the SAME holder in DIFFERENT places (fewer = a holder stays in his own place)')
rowsa = []
for site in ('Mohenjo-daro', 'Harappa'):
    for kind, col in (('holder key (office words skipped)', 'hold'), ('registry crest', 'house_key')):
        for lev in ('area_key', 'block', 'building'):
            S = K[(K.site == site) & (K[lev] != '')]
            if len(S) < 4: continue
            (o1, m1, p1), (o2, m2, p2) = run_cross(S[col], S[lev])
            say(f'  {site:12s} {kind:34s} {lev:8s} n={len(S):2d} places={S[lev].nunique():2d} holders={S[col].nunique():2d} | cross {o1} vs shuffle {m1:.1f} (P low {p1:.4f}) | apart {o2} vs {m2:.1f} (P low {p2:.4f})')
            rowsa.append(dict(site=site, key=kind, level=lev, n=len(S), places=S[lev].nunique(), holders=S[col].nunique(),
                              cross=o1, cross_shuffle=round(m1, 2), cross_P=round(p1, 4), apart=o2, apart_shuffle=round(m2, 2), apart_P=round(p2, 4)))
pd.DataFrame(rowsa).to_csv(f'{OUT}/s2_a_spread.csv', index=False)
say('\n  the objects (Mohenjo-daro, then Harappa): id, area, block, building, holder key, signs')
for site in ('Mohenjo-daro', 'Harappa'):
    for _, r in K[K.site == site].sort_values(['area_key', 'block']).iterrows():
        say(f'     {r.cisi:9s} {r.kind:5s} area {r.area_key or "-":28s} block {r.block or "-":30s} holder {r.hold:6s} crest {r.house_key:8s} {r.signs}')
K[['cisi', 'object_id', 'site', 'kind', 'area_key', 'block', 'building', 'hold', 'house_key', 'bin', 'signs']].to_csv(f'{OUT}/s2_office_objects.csv', index=False)

# ---------------- (b) the pair texts ----------------
say('\n(b) Counts and wards with the pair 061/820 + 142 (both catalogues; second catalogue only the 1,183 texts with no Lipi partner)')
faces = [(r.id, r.cisi, r.site, tuple(r.tok), 'L') for r in d.itertuples()]
faces += [(f'M{r.textnum}.{r.sideline}', f'M{r.textnum}', r.site_l, tuple(r.tok), 'Mu') for r in M[~M.partnered].itertuples()]
def pair_at(t):
    return [i for i in range(len(t) - 1) if t[i] in QUART and t[i + 1] == '142']
WARDS = {'741', '742', '745'}
pairf = [f for f in faces if pair_at(f[3])]
q_not = [f for f in faces if any(s in QUART for s in f[3]) and not pair_at(f[3])]
k_not = [f for f in faces if '142' in f[3] and not pair_at(f[3])]
say(f'  texts with the pair: Lipi {sum(f[4] == "L" for f in pairf)}, second catalogue new {sum(f[4] == "Mu" for f in pairf)}; quarter-without-142 texts {len(q_not)}; 142-without-quarter-before texts {len(k_not)}')
def count_before(t, i):
    return i > 0 and t[i - 1] in CNT
def feat(fs, pairmode):
    out = collections.Counter(); n = 0
    for f in fs:
        t = f[3]
        idx = pair_at(t) if pairmode else [i for i, s in enumerate(t) if s in QUART]
        if not idx: continue
        i = idx[0]; n += 1
        if count_before(t, i): out['count right before the quarter sign'] += 1
        if i + 2 < len(t) and t[i + 2] in CNT: out['count right after 142'] += 1
        if any(s in CNT for s in t): out['any count in text'] += 1
        if WARDS & set(t): out['ward sign 741/742/745 in text'] += 1
        if '741' in t[:i]: out['741 before the quarter sign'] += 1
        if t and t[-1] == '740': out['text ends in jar'] += 1
    return n, out
npair, fp = feat(pairf, True); nq, fq = feat(q_not, False); nk, fk = feat(k_not, False)
rowsb = []
for k in ['count right before the quarter sign', 'count right after 142', 'any count in text', 'ward sign 741/742/745 in text', '741 before the quarter sign', 'text ends in jar']:
    a, b = fp[k], fq[k]
    _, p = fisher_exact([[a, npair - a], [b, nq - b]], alternative='greater')
    say(f'  {k:40s} pair texts {a} of {npair} ({a / npair:.0%}) | other quarter-sign texts {b} of {nq} ({b / nq:.0%}) | one-sided P {p:.4f}')
    rowsb.append(dict(feature=k, pair=a, pair_n=npair, quarter_other=b, quarter_other_n=nq, P=p))
pd.DataFrame(rowsb).to_csv(f'{OUT}/s2_b_pair_features.csv', index=False)
base_w = np.mean([bool(WARDS & set(f[3])) for f in faces]); say(f'  all faces: ward sign in {base_w:.1%}')
say('  every pair text, in reading order:')
for f in pairf:
    t = f[3]; i = pair_at(t)[0]
    say(f'     {f[1]:9s} {f[2]:12s} {"-".join(t)}   (before quarter: {t[i - 1] if i else "START"}; after 142: {t[i + 2] if i + 2 < len(t) else "END"})')
say('  counts that precede the quarter sign, by number series:')
for f in pairf:
    t = f[3]; i = pair_at(t)[0]
    if i and t[i - 1] in NUM: say(f'     {f[1]:9s} count {t[i - 1]} = series {NUM[t[i - 1]][0]} value {NUM[t[i - 1]][1]}')

# ---------------- (c) time ----------------
say('\n(c) Does the office stay with a house across time bins?')
Kt = K[K.bin.isin(['early', 'middle', 'late'])].copy()
say(f'  142-objects with a time bin: {len(Kt)} of {len(K)}; by bin {Kt.bin.value_counts().to_dict()}')
def bin_pairs(keys, bins):
    same = diff = 0
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            if keys[i] == keys[j] and keys[i] != '(none)':
                if bins[i] == bins[j]: same += 1
                else: diff += 1
    return same, diff
rowsc = []
for col in ('hold', 'house_key'):
    keys = list(Kt[col]); bins = list(Kt.bin); sites = list(Kt.site)
    o_same, o_diff = bin_pairs(keys, bins)
    # shuffle holder keys among objects of the same site (bins fixed)
    groups = collections.defaultdict(list)
    for i, s in enumerate(sites): groups[s].append(i)
    nd = np.zeros(NSH); ns = np.zeros(NSH)
    for t in range(NSH):
        k2 = keys[:]
        for ix in groups.values():
            vals = [keys[i] for i in ix]; random.shuffle(vals)
            for i, v in zip(ix, vals): k2[i] = v
        # only same-site pairs count in the observed too, so restrict
        ns[t], nd[t] = bin_pairs([f'{sites[i]}|{k2[i]}' for i in range(len(k2))], bins)
    o_same, o_diff = bin_pairs([f'{sites[i]}|{keys[i]}' for i in range(len(keys))], bins)
    say(f'  key {col:9s}: same-holder pairs inside one site: same bin {o_same} (shuffle {ns.mean():.1f}), different bins {o_diff} (shuffle {nd.mean():.1f}; P high {(1 + (nd >= o_diff).sum()) / (NSH + 1):.4f}); same-bin P high {(1 + (ns >= o_same).sum()) / (NSH + 1):.4f}')
    rowsc.append(dict(key=col, same_bin=o_same, same_bin_shuffle=ns.mean(), diff_bin=o_diff, diff_bin_shuffle=nd.mean(), P_diff=(1 + (nd >= o_diff).sum()) / (NSH + 1)))
pd.DataFrame(rowsc).to_csv(f'{OUT}/s2_c_time.csv', index=False)
say('  holders that hold 142 in 2+ bins (site, key, bins, ids):')
for (site, h), g in Kt.groupby(['site', 'hold']):
    if len(g) >= 2 and h != '(none)':
        say(f'     {site:12s} holder {h:6s} bins {sorted(g.bin.tolist())} ids {", ".join(g.cisi)}')

# ---------------- (d) other signs behaving like 142 ----------------
say('\n(d) Other signs with 142\'s behaviour: text position and one holder per area (Mohenjo-daro + Harappa, located named objects)')
# text position profile of 142 over every face with a name
def pos_prof(sig):
    rel = []; before = collections.Counter(); after = collections.Counter(); n = 0
    for f in faces:
        t = f[3]
        for i, s in enumerate(t):
            if s == sig:
                n += 1; rel.append(i / max(len(t) - 1, 1))
                before[t[i - 1] if i else 'START'] += 1; after[t[i + 1] if i + 1 < len(t) else 'END'] += 1
    return n, (np.mean(rel) if rel else np.nan), before, after
n142, r142, b142, a142 = pos_prof('142')
say(f'  142: {n142} uses, mean relative position {r142:.2f}; right before it: {dict(b142.most_common(5))}; right after it: {dict(a142.most_common(5))}')
L = A[A.site.isin(['Mohenjo-daro', 'Harappa']) & (A.area_key != '')].copy()
L['sig'] = L.apply(toks, axis=1)
signs = collections.Counter(s for t in L.sig for s in set(t) if s and s not in CNT and s != '000')
cand = [s for s, c in signs.items() if c >= 6]
say(f'  signs on 6+ located named objects at the two big cities: {len(cand)}')
def holder_excl(r, s):
    core = [x for x in r.name_full.split('-') if x and x not in CNT and x != s and x not in QUART]
    return core[0] if core else '(none)'
rowsd = []
for n_, s in enumerate(cand):
    S = L[L.sig.map(lambda t: s in t)]
    out = dict(sign=s, objects=len(S))
    for lev in ('area_key', 'block'):
        S2 = S[S[lev] != '']
        if len(S2) < 6: out[lev + '_P'] = np.nan; continue
        keys = [holder_excl(r, s) for _, r in S2.iterrows()]
        locs = list(S2[lev]); sites = list(S2.site)
        pairs = [(i, j) for i in range(len(keys)) for j in range(i + 1, len(keys)) if sites[i] == sites[j]]
        def cr(k):
            return sum(1 for i, j in pairs if locs[i] == locs[j] and k[i] != k[j])
        o = cr(keys); a = np.zeros(1000)
        for t in range(1000):
            k2 = keys[:]; random.shuffle(k2); a[t] = cr(k2)
        out[lev + '_cross'] = o; out[lev + '_shuf'] = round(a.mean(), 1); out[lev + '_P'] = (1 + (a <= o).sum()) / 1001
        out['distinct_holders'] = len(set(keys)); out['places_' + lev] = len(set(locs))
    nn, rr, bb, aa = pos_prof(s); out.update(uses=nn, rel_pos=round(rr, 2), top_before=bb.most_common(1)[0][0] if bb else '', top_after=aa.most_common(1)[0][0] if aa else '')
    rowsd.append(out)
    if n_ % 25 == 0: print(f'   ... sign {n_} of {len(cand)}', flush=True)
D = pd.DataFrame(rowsd); D.to_csv(f'{OUT}/s2_d_signs.csv', index=False)
tested = D.area_key_P.notna().sum()
say(f'  signs tested at area level: {tested}; with P low <= 0.05: {(D.area_key_P <= 0.05).sum()} (chance alone gives about {0.05 * tested:.1f}); at block level tested {D.block_P.notna().sum()}, <= 0.05: {(D.block_P <= 0.05).sum()}')
good = D[(D.area_key_P <= 0.05) & (D.distinct_holders >= 4)].sort_values('area_key_P')
say('  signs with fewer cross-holder same-area pairs than shuffled (P<=0.05, 4+ different holders):')
for _, r in good.iterrows():
    say(f'     sign {r.sign}: {int(r.objects)} objects, {int(r.distinct_holders)} holders, cross {int(r.area_key_cross)} vs shuffle {r.area_key_shuf}, P {r.area_key_P:.3f}; block P {r.block_P}; mean relative position {r.rel_pos}, usually after {r.top_before}, before {r.top_after}')
say('  for comparison, sign 142 itself in the same table:')
r = D[D.sign == '142']
if len(r): r = r.iloc[0]; say(f'     142: {int(r.objects)} objects, {int(r.distinct_holders)} holders, area cross {r.area_key_cross} vs {r.area_key_shuf}, P {r.area_key_P}; block P {r.block_P}')
# signs similar in text position to 142 and with many holders
sim = D[(abs(D.rel_pos - r142) <= 0.12) & (D.distinct_holders >= 5)].sort_values('area_key_P')
say('  signs with 142\'s text position (within 0.12 of its mean relative position) and 5+ holders, best area P first:')
for _, q in sim.head(15).iterrows():
    say(f'     sign {q.sign}: {int(q.objects)} objects, {int(q.distinct_holders)} holders, rel pos {q.rel_pos}, area P {q.area_key_P}, block P {q.block_P}')
LOG.close()
