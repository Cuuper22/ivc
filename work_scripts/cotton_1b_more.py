"""PART 1 continued. Predictions (written first):
 A: 390 is a keeper word -> 390 outside the box pair should sit in the same name slot (jar after it) and be uncounted.
 B: 390 is a goods word -> outside the pair it is counted in lots and almost never takes the jar; inside the pair it is carried into the name slot by the box.
 Both-true prediction (house named for its trade): jar-after 390 in pair >> jar-after 390 elsewhere, AND counts elsewhere in lots.
 Lothal (warehouse): the pair on tags should carry a count in front and often no jar (a goods use).
"""
from cotton_common import *
f = open(f'{OUTC}/split_log2.txt', 'w')
d = faces(); T = d.toks.tolist(); NUMS = {k for k, v in CNT.items() if v[0] != 'A'}
inpair = []; outpair = []
for k, t in enumerate(T):
    for j, x in enumerate(t):
        if x != '390': continue
        jar = j + 1 < len(t) and t[j + 1] == JAR
        (inpair if (j > 0 and t[j - 1] == '590') else outpair).append((k, j, jar))
a = sum(x[2] for x in inpair); b = len(inpair) - a; c = sum(x[2] for x in outpair); e = len(outpair) - c
r, p = fe(a, b, c, e)
log(f, f'390 followed by the jar: in the box pair {a}/{len(inpair)} ({a/len(inpair):.2f}); elsewhere {c}/{len(outpair)} ({c/len(outpair):.3f}); ratio {r:.1f}, one-sided P {p:.1e}')
cnt_out = sum(1 for k, j, _ in outpair if j > 0 and T[k][j - 1] in NUMS)
log(f, f'390 elsewhere with a count right before: {cnt_out}/{len(outpair)} ({cnt_out/len(outpair):.2f}); in the pair the count stands before the BOX instead: {sum(1 for k,j,_ in inpair if j>1 and T[k][j-2] in NUMS)}/{len(inpair)}')
# tree variants 405, 407 same pair/elsewhere contrast
for s in ['405', '407']:
    ip = []; op = []
    for k, t in enumerate(T):
        for j, x in enumerate(t):
            if x != s: continue
            jar = j + 1 < len(t) and t[j + 1] == JAR
            cn = j > 0 and t[j - 1] in NUMS
            (ip if (j > 0 and t[j - 1] == '590') else op).append((jar, cn))
    log(f, f'{s}: in box pair n {len(ip)}, jar after {np.mean([x[0] for x in ip]):.2f}, counted {np.mean([x[1] for x in ip]):.2f} | elsewhere n {len(op)}, jar after {np.mean([x[0] for x in op]):.2f}, counted {np.mean([x[1] for x in op]):.2f}')
# what comes before an uncounted, unboxed 390 (if a keeper title: goods words or house words)
pv = collections.Counter(T[k][j - 1] for k, j, _ in outpair if j > 0 and T[k][j - 1] not in NUMS and T[k][j - 1] != '590')
log(f, 'sign before an uncounted 390 outside the pair: ' + str(pv.most_common(12)))
# counted-value distribution of 390 vs other counted nouns: share of count>=3
def cshare(sign):
    v = [CNT[T[k][j - 1]][1] for k, t in enumerate(T) for j, x in enumerate(t) if x == sign and j > 0 and T[k][j - 1] in NUMS]
    return (len(v), np.mean([u >= 3 for u in v])) if v else (0, np.nan)
for s in ['390', '405', '407', '220', '806', '590']:
    n, sh = cshare(s); log(f, f'count>=3 share before {s}: {sh:.2f} over {n} counted uses')
# Lothal
log(f, '\nLothal warehouse tags: formula check')
L = d[(d.site == 'Lothal') & (d.cls == 'tag')]
pairL = L[L.toks.apply(lambda t: has_pair(t, '590', '390') != [])]
log(f, f'Lothal tags {len(L)}; carrying the pair {len(pairL)}; with 002-032 right before the box: {sum(1 for t in pairL.toks if "002-032-590" in "-".join(t))}')
others = L[L.toks.apply(lambda t: '002-032' in '-'.join(t))]
log(f, f'Lothal tags with 002-032 anywhere: {len(others)} (of which with pair {sum(1 for t in others.toks if has_pair(t,"590","390"))}); texts: ' + '; '.join('-'.join(t) for t in others.toks))
r, p = fe(len(pairL), len(L) - len(pairL), len(d[d.cls == 'tag']) - len(L) and sum(1 for t in d[(d.cls == 'tag') & (d.site != 'Lothal')].toks if has_pair(t, '590', '390')), len(d[(d.cls == 'tag') & (d.site != 'Lothal')]))
log(f, f'pair on Lothal tags vs tags elsewhere: ratio {r:.1f}, P {p:.3f}')
# seals vs goods objects: share of pair faces on goods-class objects
goods = d.cls.isin(['tag', 'pot']); n_pair = np.array([bool(has_pair(t, '590', '390')) for t in T])
log(f, f'pair on tags+pots: {int((goods&n_pair).sum())} of {int(n_pair.sum())} ({(goods&n_pair).sum()/n_pair.sum():.2f}) against {goods.mean():.2f} of the corpus')
f.close()
