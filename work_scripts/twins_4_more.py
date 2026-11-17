#!/usr/bin/env python3
"""TWINS step 4: buildings, the rival (seal format), kinds, holders, backs and wear, one holder's set of stones.
Written 2026-11-17 after step 3 (which found 0 twin pairs in one building, and twins sharing the animal 1.34 times
chance). Predictions for each part are fixed here before its numbers.

A  SAME BUILDING. Prediction: twin pairs share a building LESS often than chance (house-mates never carry one text:
   inside a house each holder has his own text). Null: building labels dealt among complete seals of the same site and
   text length (5,000 deals); also block and area.
B  RIVAL for the animal result: twins share the animal only because they share the seal FORMAT (square with a beast
   against inscription-only bar), and format goes with text length and site. Test: deal the animal among seals of the
   same site, text length AND format. Prediction: the excess survives (ratio still above 1.2).
C  KINDS. Twin rate (share of complete seals whose text is on another seal) by kind against the rate expected from text
   length alone (each seal gets the twin rate of all seals of its length). Prediction: count lines and front formulas
   twin far above their length; bare names and name + closer at or below it.
D  HOLDERS. holder = animal + stand letter. For each text: stones, distinct holders, cities, time bins; the most
   stones of one text inside one bin. Prediction: a text has a handful of stones (2-7), with distinct holders about as
   many as stones, and up to 3-4 stones of one text in one bin and several cities (several holders at once).
E  BACKS AND WEAR. Twin members against all complete seals of the same site and length: share not pierced, share with
   no boss, share in 'Poor' condition, share inscription-only. Prediction: twins carry MORE unpierced / no-boss stones
   (a replacement or unfinished copy) than chance.
F  ONE HOLDER, SEVERAL TEXTS. Pairs of seals in one building with the same animal and stand letter but different texts.
   Related = same crest (first name sign), or one sign apart (edit distance 1), or one text inside the other.
   Prediction: these pairs are related more often than pairs of house-mates with different holder marks, and more than
   texts dealt among seals of the same site.
Writes work_data/twins/{building.csv, kinds.csv, holders.csv, backs.csv, one_holder.csv}, log_4.txt.
"""
from twins_common import *
import itertools, collections
rng = np.random.default_rng(4); NR = 5000
S = pd.read_csv(f'{OUT}/seals.csv', dtype=str).fillna('')
S['n'] = S.n.astype(int)
C = S[S.complete == 'True'].drop_duplicates(['obj', 'signs']).reset_index(drop=True)
Mem = pd.read_csv(f'{OUT}/members.csv', dtype=str).fillna('')
keyM = set(zip(Mem.obj, Mem.signs))
C['in_set'] = [(o, s) in keyM for o, s in zip(C.obj, C.signs)]
C = C[(~C.signs.isin(set(Mem.signs))) | C.in_set].reset_index(drop=True)
C['stratum'] = C.site + '|' + C.n.astype(str)
pairs = [(i, j) for t, g in C[C.in_set].groupby('signs') for i, j in itertools.combinations(g.index, 2)]
I = np.array([p[0] for p in pairs]); J = np.array([p[1] for p in pairs])
def deal(col, within):
    v = C[col].values; out = v.copy()
    for _, ix in C.groupby(within).indices.items(): out[ix] = v[ix][rng.permutation(len(ix))]
    return out
def same(vals):
    a, b = vals[I], vals[J]; ok = (a != '') & (b != ''); return int(((a == b) & ok).sum()), int(ok.sum())

# ---------------- A
print('A  SAME BUILDING / BLOCK / AREA (twin pairs, both findspots known, same city)')
rowsA = []
for col in ['room', 'building', 'block', 'area_key']:
    s, n = same(C[col].values); arr = np.array([same(deal(col, 'stratum'))[0] for _ in range(NR)])
    rowsA.append(dict(level=col, pairs_with_both=n, real=s, dealt_mean=arr.mean(), P_fewer=(np.sum(arr <= s) + 1) / (NR + 1), P_more=(np.sum(arr >= s) + 1) / (NR + 1)))
A = pd.DataFrame(rowsA); A.to_csv(f'{OUT}/building.csv', index=False); print(A.round(4).to_string(index=False))
# all seal pairs of the same text length in one building, for scale
bb = C[C.building != ''].groupby('building').size()
print(f'   buildings with 2+ complete seals: {int((bb >= 2).sum())}; seal pairs inside one building: {int((bb * (bb - 1) / 2).sum())}')

# ---------------- B
print('\nB  RIVAL: animal dealt within site x length x format')
C['strat_fmt'] = C.stratum + '|' + C.fmt
s, n = same(C.animal.values); arr = np.array([same(deal('animal', 'strat_fmt'))[0] for _ in range(NR)])
print(f'   same animal {s} of {n}; dealt {arr.mean():.1f}; ratio {s/arr.mean():.2f}; P_more {(np.sum(arr>=s)+1)/(NR+1):.4f}')
Cb = C.animal.where(~C.animal.isin(['none']), '').values
C['beast'] = Cb
s2, n2 = same(Cb); arr2 = np.array([same(deal('beast', 'strat_fmt'))[0] for _ in range(NR)])
print(f'   beast seals only: same animal {s2} of {n2}; dealt {arr2.mean():.1f}; ratio {s2/arr2.mean():.2f}; P_more {(np.sum(arr2>=s2)+1)/(NR+1):.4f}')
# second rival inside it: the unicorn is 80% of beasts; is the excess only unicorn+unicorn?
a, b = C.animal.values[I], C.animal.values[J]
nonu = (a != '') & (b != '') & ~((a == 'unicorn') & (b == 'unicorn'))
print(f'   pairs that are not unicorn+unicorn: {int(nonu.sum())}, of which same animal {int(((a == b) & nonu).sum())}: ' +
      ', '.join(f'{x}' for x in sorted(collections.Counter(a[(a == b) & nonu]).items())))
fmtsame = same(C.fmt.values); arrf = np.array([same(deal('fmt', 'stratum'))[0] for _ in range(NR)])
print(f'   same format {fmtsame[0]} of {fmtsame[1]}; dealt {arrf.mean():.1f}; ratio {fmtsame[0]/arrf.mean():.2f}; P_more {(np.sum(arrf>=fmtsame[0])+1)/(NR+1):.4f}')

# ---------------- C
print('\nC  KINDS')
C['twin'] = C.in_set
rate_L = C.groupby('n').twin.mean()
C['exp'] = C.n.map(rate_L)
P = pd.DataFrame({'kind': C.kind.values[I], 'cross_city': C.site.values[I] != C.site.values[J],
                  'b1': C.bin.values[I], 'b2': C.bin.values[J], 'g1': C.building.values[I], 'g2': C.building.values[J]})
P['cross_bin'] = (P.b1 != '') & (P.b2 != '') & (P.b1 != P.b2); P['both_bin'] = (P.b1 != '') & (P.b2 != '')
rowsC = []
for k, g in C.groupby('kind'):
    pk = P[P.kind == k]
    rowsC.append(dict(kind=k, seals=len(g), twinned=int(g.twin.sum()), twin_rate=g.twin.mean(), expected_from_length=g.exp.mean(),
                      ratio=g.twin.mean() / g.exp.mean() if g.exp.mean() else np.nan, sets=g[g.twin].signs.nunique(), pairs=len(pk),
                      cross_city=int(pk.cross_city.sum()), cross_bin=int(pk.cross_bin.sum()), dated_pairs=int(pk.both_bin.sum()),
                      mean_len=g.n.mean()))
K = pd.DataFrame(rowsC).sort_values('seals', ascending=False); K.to_csv(f'{OUT}/kinds.csv', index=False)
print(K.round(3).to_string(index=False))
# P for each kind's twin rate: deal kind labels within length
for k in ['count line', 'front formula', 'name + closer', 'bare name', 'name + title', 'name + closer + title']:
    real = int(C[C.kind == k].twin.sum()); arr = []
    kv = C.kind.values; tw = C.twin.values
    for _ in range(2000):
        d_ = deal('kind', 'n'); arr.append(int(tw[d_ == k].sum()))
    arr = np.array(arr)
    print(f'   {k:24s} twinned {real} vs dealt within length {arr.mean():.1f}; P_more {(np.sum(arr>=real)+1)/2001:.4f}; P_fewer {(np.sum(arr<=real)+1)/2001:.4f}')

# ---------------- D
print('\nD  HOLDERS')
rowsD = []
M = C[C.in_set]
for t, g in M.groupby('signs'):
    hold = g.animal + ':' + g.stand5
    known = hold[g.animal != '']
    perbin = g[g.bin != ''].groupby('bin').size()
    rowsD.append(dict(signs=t, kind=g.kind.iloc[0], length=g.n.iloc[0], stones=len(g), holders_known=len(known), distinct_holders=known.nunique(),
                      cities=g.site.nunique(), bins=' '.join(sorted(g.bin[g.bin != '']).__iter__()), max_in_one_bin=int(perbin.max()) if len(perbin) else 0,
                      cities_in_that_bin=int(g[g.bin == perbin.idxmax()].site.nunique()) if len(perbin) else 0))
D = pd.DataFrame(rowsD).sort_values('stones', ascending=False); D.to_csv(f'{OUT}/holders.csv', index=False)
print(D.head(25).to_string(index=False))
print(f'   texts {len(D)}; stones per text median {D.stones.median()}, max {D.stones.max()}; distinct holders = holders known in {int((D.distinct_holders == D.holders_known).sum())} of {len(D)}')
print(f'   texts with 2+ stones in ONE time bin: {int((D.max_in_one_bin >= 2).sum())}; of those in 2+ cities in that bin: {int((D.cities_in_that_bin >= 2).sum())}')
print('   by kind: ' + '; '.join(f'{k}: {len(g)} texts, {g.stones.sum()} stones, mean {g.stones.mean():.2f}' for k, g in D.groupby('kind')))
C['crest'] = C.signs.map(crest_of)
cr = C[C.kind.isin(['name + closer', 'name + closer + title', 'front formula', 'bare name'])].groupby('crest').agg(stones=('obj', 'size'), texts=('signs', 'nunique'), cities=('site', 'nunique'))
cr = cr.sort_values('stones', ascending=False)
print('   crest houses (complete name seals): stones / distinct texts, top 12:\n' + cr.head(12).to_string())
print('   per city: ' + '; '.join(f'{c}: {len(g)} stones, {g.signs.nunique()} texts' for c, g in C.groupby('site') if len(g) >= 40))

# ---------------- E
print('\nE  BACKS AND WEAR (twin members against all complete seals of the same site and length)')
C['unpierced'] = np.where(C.pierced == '', '', np.where(C.pierced == 'not pierced', 'y', 'n'))
C['noboss'] = np.where(C.knob == '', '', np.where(C.knob == 'no boss', 'y', 'n'))
C['poor'] = np.where(C.condition.str.lower().isin(['poor']), 'y', np.where(C.condition.str.lower().isin(['good', 'fair', 'fine']), 'n', ''))
C['textonly'] = np.where(C.animal == '', '', np.where(C.animal == 'none', 'y', 'n'))
rowsE = []
for col in ['unpierced', 'noboss', 'poor', 'textonly']:
    v = C[col].values; tw = C.twin.values
    def stat(vv): ok = (vv != '') & tw; return int(((vv == 'y') & ok).sum()), int(ok.sum())
    s, n = stat(v); arr = np.array([stat(deal(col, 'stratum'))[0] for _ in range(NR)])
    rowsE.append(dict(feature=col, twins_known=n, twins_yes=s, dealt_mean=arr.mean(), P_more=(np.sum(arr >= s) + 1) / (NR + 1), P_fewer=(np.sum(arr <= s) + 1) / (NR + 1),
                      all_seals_share=float((C[col] == 'y').sum() / max(1, (C[col] != '').sum()))))
E = pd.DataFrame(rowsE); E.to_csv(f'{OUT}/backs.csv', index=False); print(E.round(4).to_string(index=False))
odd = M[(M.pierced == 'not pierced') | (M.knob == 'no boss')]
print('   twin members with no boss or not pierced:\n' + odd[['cisi', 'signs', 'site', 'building', 'animal', 'stand5', 'boss', 'condition', 'fmt']].to_string(index=False))

# ---------------- F
print('\nF  ONE HOLDER, SEVERAL TEXTS')
def lev(a, b):
    a, b = a.split('-'), b.split('-'); dp = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, len(b) + 1):
            cur = dp[j]; dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + (a[i - 1] != b[j - 1])); prev = cur
    return dp[-1]
def related(a, b):
    if a == b: return 'same text'
    ca, cb = crest_of(a), crest_of(b)
    if lev(a, b) == 1: return 'one sign apart'
    if ('-' + a + '-') in ('-' + b + '-') or ('-' + b + '-') in ('-' + a + '-'): return 'one inside the other'
    if ca and ca == cb: return 'same crest'
    return ''
A2 = S[(S.signs != '') & (S.lost == '0') & (S.building != '')].drop_duplicates(['obj', 'signs']).reset_index(drop=True)
same_h, other_h = [], []
for b, g in A2.groupby('building'):
    for i, j in itertools.combinations(g.index, 2):
        if A2.obj[i] == A2.obj[j]: continue
        r = related(A2.signs[i], A2.signs[j])
        if A2.animal[i] == '' or A2.animal[j] == '': continue
        hs = A2.animal[i] == A2.animal[j] and A2.stand5[i] == A2.stand5[j] and A2.animal[i] == 'unicorn' and A2.stand5[i] != ''
        hd = A2.animal[i] != A2.animal[j] or (A2.stand5[i] != '' and A2.stand5[j] != '' and A2.stand5[i] != A2.stand5[j])
        row = (i, j, r)
        if hs: same_h.append(row)
        elif hd: other_h.append(row)
def share(rows): return sum(1 for _, _, r in rows if r and r != 'same text'), len(rows)
sh, nh = share(same_h); so, no = share(other_h)
print(f'   house-mate pairs (complete text, unicorn with the same stand letter): {nh}; related {sh} ({sh/max(nh,1):.1%})')
print(f'   house-mate pairs with a different animal or stand letter: {no}; related {so} ({so/max(no,1):.1%})')
# null: texts dealt among seals of the same site
sig = A2.signs.values.copy(); site_ix = A2.groupby('site').indices
arr = []
for _ in range(2000):
    v = sig.copy()
    for _, ix in site_ix.items(): v[ix] = sig[ix][rng.permutation(len(ix))]
    arr.append(sum(1 for i, j, _ in same_h if (lambda r: r and r != 'same text')(related(v[i], v[j]))))
arr = np.array(arr)
print(f'   same-holder pairs related: {sh} vs texts dealt within site {arr.mean():.2f}; ratio {sh/arr.mean() if arr.mean() else float("nan"):.2f}; P_more {(np.sum(arr>=sh)+1)/2001:.4f}')
F = pd.DataFrame([dict(building=A2.building[i], a=A2.cisi[i], b=A2.cisi[j], text_a=A2.signs[i], text_b=A2.signs[j], holder=f'{A2.animal[i]}:{A2.stand5[i]}', relation=r) for i, j, r in same_h])
F.to_csv(f'{OUT}/one_holder.csv', index=False)
print(F[F.relation != ''].to_string(index=False))
print('   relation counts, same holder: ' + str(collections.Counter(r for _, _, r in same_h)) + '\n   relation counts, other holder: ' + str(collections.Counter(r for _, _, r in other_h)))
