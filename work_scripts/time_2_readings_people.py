#!/usr/bin/env python3
"""History job, steps 4 and 5: the earliest and latest dated inscriptions read whole, and names that recur through time.

PREDICTIONS written before the numbers:
 R1  the earliest texts are short owner names (crest + jar) with few measure or office words; the latest carry more
     account words (kalam, cup, office opening) and more agents.
 N1  full names (2+ name signs) recur across depth bands more often than when bin labels are shuffled within area:
     names are inherited (a lineage), not one person's.
 N2  where a recurring name changes its ending between bins, the later ending is the higher one (jar -> jar+man or
     spear): a career / promotion.
Outputs: work_data/time/early_late_readings.csv, recurring_names.csv
"""
from time_common import *

CE = pd.read_csv(f'{ROOT}/work_data/corpus_english.csv', dtype=str).fillna('')
CE['obj'] = CE.object_id
G = CE.groupby('obj').agg(signs=('signs', ' | '.join), sounds=('sounds', ' | '.join), english=('english', ' '.join),
                          grade=('grade', lambda s: ','.join(sorted(set(s)))))
X = D[D.rule.isin(['A excavator', 'B layer-map'])].join(G, rsuffix='_ce')
X = X[X.grade.str.contains('whole|part') & ~X.grade.str.contains('damaged')]
X['nread'] = X.signs_ce.str.count(r'\d{3}')
pick_e = X[X['rank'] <= 3].sort_values(['rank', 'nread'], ascending=[True, False])
pick_l = X[X['rank'] >= 8].sort_values(['rank', 'nread'], ascending=[False, False])
def take(P, k=10):
    # prefer different texts and at least 2 signs
    P = P[P.nread >= 2].drop_duplicates('signs_ce'); return P.head(k)
E10, L10 = take(pick_e), take(pick_l)
cols = ['site', 'kind', 'area', 'time', 'rule', 'signs_ce', 'sounds', 'english', 'grade']
out = pd.concat([E10[cols].assign(group='earliest'), L10[cols].assign(group='latest')])
out.to_csv(f'{OUTT}/early_late_readings.csv')
print(out.to_string())

# whole-population comparison early vs late for R1 on dated objects
def fe(df, label):
    print(label, 'objects', len(df), 'kinds', df.kind.value_counts().to_dict())
fe(X[X['rank'] <= 3], 'EARLY (rank<=3)'); fe(X[X['rank'] >= 8], 'LATE (rank>=8)')

# ---------- people ----------
P = D[D.seal | D.kind.isin(['mtab', 'ctab', 'tag'])].copy()
P['nm'] = P.name.apply(lambda n: tuple(a for a in n))
P = P[P.nm.apply(lambda n: len(n) >= 2 and '000' not in n)]
grp = P.groupby('nm')
rec = []
for nm, sub in grp:
    bins = sorted(set(sub.bin), key=BI.get)
    if len(sub) < 2: continue
    rec.append(dict(name='-'.join(nm), n=len(sub), bins='/'.join(bins), nbins=len(bins), sites='/'.join(sorted(set(sub.site))),
                    kinds='/'.join(sorted(set(sub.kind))),
                    endings=' ; '.join(f'{b}:{",".join(sorted(set(sub[sub.bin == b].ending)))}' for b in bins),
                    objs=' '.join(sub.cisi.astype(str).head(12))))
R = pd.DataFrame(rec).sort_values(['nbins', 'n'], ascending=False)
R.to_csv(f'{OUTT}/recurring_names.csv', index=False)
print(R.head(40).to_string())

# N1: number of names (2+ copies) seen in 2+ bins, observed vs shuffled within stratum
def spans(df):
    g = df.groupby('nm').bin.nunique(); c = df.groupby('nm').size()
    return int(((g >= 2) & (c >= 2)).sum()), int(((g >= 3)).sum())
obs = spans(P)
rng2 = np.random.default_rng(3); null = []
for k in range(1000):
    Q = P.copy(); Q['bin'] = Q.groupby('stratum').bin.transform(lambda s: rng2.permutation(s.values))
    null.append(spans(Q))
null = np.array(null)
print(f'N1 names seen in 2+ bins: {obs[0]} against {null[:, 0].mean():.1f} shuffled (P low side {(null[:, 0] <= obs[0]).mean():.3f}, high side {(null[:, 0] >= obs[0]).mean():.3f}); in all 3 bins {obs[1]} against {null[:, 1].mean():.1f}')
# same, but excluding copies of the same text found in the same stratum (tablet batches)
P2 = P.drop_duplicates(['nm', 'stratum', 'bin'])
print('names (distinct stratum x bin finds) in 2+ bins:', spans(P2))
# N2: endings that change between bins
ch = R[R.endings.str.count(':') >= 2]
print('names in 2+ bins with ending info:'); print(ch[['name', 'n', 'sites', 'endings']].to_string())
