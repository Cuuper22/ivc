#!/usr/bin/env python3
"""SIZE step 3: rank order of the titles and closers.  Written 2026-11-17 before any number.

Ladder value of a sign in a group of seals = mean residual size (logA minus the baseline length + site + format fit made
on that same group) of the group's seals that carry the sign. Also the ridge weight of model (d) on all seals
(work_data/size/ladder_all.csv). Signs: the frame-v2 after-jar titles (400 090 527 621 679 565 161 241 ...) and closers
(740 520 151 154 155 158).
Stability: Spearman rank correlation of the ladder between Mohenjo-daro and Harappa, and between time bins, over the
title + closer signs with 3+ seals on both sides. Control: the same correlation for 2,000 random sets of the same number
of OTHER signs that also have 3+ seals on both sides.
Stacking: seals with two title/closer signs: does the later sign sit higher on the all-seal ladder than the earlier?

PREDICTIONS:
  R1  Ladder (all seals): man 090 and 679 high, jar 740 middle, porters 151-158 and comb 400 low.
  R2  Mohenjo-daro against Harappa: Spearman above 0.5 and above 90% of random sign sets.
  R3  Across bins (early/middle against late, middle against late): positive and above most random sets.
  R4  In stacks, the second sign is higher than the first more often than not (a title raises the holder above the
      plain closer), except 740-400, where comb is low.
"""
from size_common import *
from scipy.stats import spearmanr

S = table(); toks = list(S.tok)
TC = [s for s, v in V2.items() if v in ('TITLE', 'CLOSER')]
LA = pd.read_csv(f'{OUT}/ladder_all.csv', dtype={'sign': str}).set_index('sign')


def resid(Sub):
    Bf, _ = base_X(Sub); B = Bf.values; y = Sub.logA.values
    wb, _ = ridge_fit(B, np.zeros((len(Sub), 0)), y, 0)
    return y - ridge_pred(B, np.zeros((len(Sub), 0)), wb, np.zeros(0))


def ladder(Sub, signs=None):
    r = resid(Sub); t = list(Sub.tok)
    c = collections.Counter(s for x in t for s in set(x))
    signs = signs or list(c)
    return {s: (r[[s in x for x in t]].mean(), c[s]) for s in signs if c.get(s, 0) > 0}


rows = []
full = ladder(S)
for s in TC:
    if s not in full: continue
    row = dict(sign=s, picture=pic(s), blind=pic_book(s), job=job(s), seals=full[s][1], all_resid=full[s][0],
               ridge_weight=LA.weight.get(s, np.nan))
    for nm, sub in [('MD', S[S.siteg == 'MD']), ('HP', S[S.siteg == 'HP']), ('early', S[S.bin == 'early']),
                    ('middle', S[S.bin == 'middle']), ('late', S[S.bin == 'late'])]:
        l = ladder(sub, [s]); row[f'{nm}_resid'], row[f'{nm}_n'] = l.get(s, (np.nan, 0))
    rows.append(row)
T = pd.DataFrame(rows).sort_values('all_resid', ascending=False)
T.to_csv(f'{OUT}/titles_ladder.csv', index=False)
log('S3', 'title / closer ladder (mean residual logA; +0.10 = about 10% bigger than seals of same site, length, format):\n' +
    T[['sign', 'picture', 'job', 'seals', 'all_resid', 'ridge_weight', 'MD_resid', 'MD_n', 'HP_resid', 'HP_n', 'early_resid', 'early_n',
       'middle_resid', 'middle_n', 'late_resid', 'late_n']].round(3).to_string(index=False))

# stability with control
def compare(A, B, nmA, nmB, minn=3):
    la, lb = ladder(A), ladder(B)
    both = [s for s in la if s in lb and la[s][1] >= minn and lb[s][1] >= minn]
    tc = [s for s in both if s in TC]
    if len(tc) < 3: return dict(pair=f'{nmA} vs {nmB}', n_tc=len(tc))
    rho = spearmanr([la[s][0] for s in tc], [lb[s][0] for s in tc]).correlation
    other = [s for s in both if s not in TC]
    rr = np.random.default_rng(5); null = []
    for _ in range(2000):
        pk = list(rr.choice(other, len(tc), replace=False))
        null.append(spearmanr([la[s][0] for s in pk], [lb[s][0] for s in pk]).correlation)
    null = np.array(null)
    return dict(pair=f'{nmA} vs {nmB}', n_tc=len(tc), signs=' '.join(tc), rho=rho, null_mean=np.nanmean(null),
                share_null_ge=np.nanmean(null >= rho), all_other_rho=spearmanr([la[s][0] for s in other], [lb[s][0] for s in other]).correlation,
                n_other=len(other))
C = []
for args in [(S[S.siteg == 'MD'], S[S.siteg == 'HP'], 'Mohenjo-daro', 'Harappa'),
             (S[S.bin == 'early'], S[S.bin == 'late'], 'early', 'late'),
             (S[S.bin == 'middle'], S[S.bin == 'late'], 'middle', 'late'),
             (S[S.bin == 'early'], S[S.bin == 'middle'], 'early', 'middle'),
             (S[S.bin.isin(['early', 'middle'])], S[S.bin == 'late'], 'early+middle', 'late'),
             (S[(S.siteg == 'MD') & S.bin.isin(['early', 'middle'])], S[(S.siteg == 'MD') & (S.bin == 'late')], 'MD early+middle', 'MD late')]:
    c = compare(*args); C.append(c); log('S3', c)
pd.DataFrame(C).to_csv(f'{OUT}/titles_stability.csv', index=False)

# stacking
st = []
for t, sg in zip(toks, S.signs):
    x = [s for s in t if s in TC]
    if len(x) >= 2:
        for a, b in zip(x, x[1:]):
            if a != b: st.append((a, b, full[b][0] > full[a][0]))
ST = pd.DataFrame(st, columns=['first', 'second', 'second_higher'])
G = ST.groupby(['first', 'second']).second_higher.agg(['size', 'sum']).reset_index().sort_values('size', ascending=False)
G['first_resid'] = G['first'].map(lambda s: full[s][0]); G['second_resid'] = G['second'].map(lambda s: full[s][0])
G.to_csv(f'{OUT}/titles_stacks.csv', index=False)
log('S3', f'stacks: {len(ST)} adjacent title/closer pairs on seals; second sign higher on the ladder {int(ST.second_higher.sum())}')
log('S3', '\n' + G.round(3).to_string(index=False))
# per-seal check for jar + title: is a [..740 T] seal bigger than [..740] seals of same cell (half-free, direct)
S['res'] = resid(S)
for tt in ('090', '400', '679', '527', '565', '621', '154', '520', '151'):
    m = S[S.signs.str.contains(f'740-{tt}')]
    j = S[S.tok.map(lambda x: x[-1] == '740') ]
    if len(m): log('S3', f'740-{tt}: {len(m)} seals, mean residual {m.res.mean():+.3f} against jar-final seals {j.res.mean():+.3f} (n {len(j)})')
