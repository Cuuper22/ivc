#!/usr/bin/env python3
"""SIZE step 7: tablets and tags: does size follow the amount written or the name?  Written 2026-11-17 before any number.

Objects: first-catalogue tablets (TAB:B moulded, TAB:I incised, TAB:C copper) and tags/sealings (TAG*), one row per
object, area = catalogue width x height (mm2), logA.
COUNT of an object = value of its number signs (tall strokes 031-036 = 1-6; short strokes 001-007 = 1-7; stacked
012-018 = 2-8), summed if more than one; objects with no number sign are left out of count tests.
NAME of an object = its full sign string with the number signs removed (the rest of the record, both faces).
STRATUM = object type x site.
Tests (shuffles 2,000):
  count effect: logA minus the mean of its stratum x name group, against count; spread over counts compared with counts
                dealt within stratum x name. Direction: Spearman of the within-name residual against the count.
  name effect: logA minus the mean of its stratum x count group, spread over names (names on 2+ objects), against names
                dealt within stratum x count.
Batches: identical full texts of 2+ moulded tablets = batch; within-batch size spread vs between-batch.

PREDICTIONS:
  T1  With the name held fixed, size falls with the count (the measured 8% per stroke), i.e. Spearman negative.
  T2  With the count held fixed, the name explains size beyond the deals (P below 0.01): a tablet is made to its name's
      mould, as a seal is made to its text.
  T3  Moulded batches are tight: within-batch spread under a third of between-batch.
"""
from size_common import *
from scipy.stats import spearmanr
with contextlib.redirect_stdout(io.StringIO()):
    from sound_v4_common import d

NUMV = {f'03{i}': i for i in range(1, 7)}; NUMV.update({f'00{i}': i for i in range(1, 8)}); NUMV.update({f'01{i}': i for i in range(2, 9)})
D = d[d.type.str.startswith('TAB') | d.type.str.startswith('TAG')].copy()
D['h'] = pd.to_numeric(D['horizontal(mm)'], errors='coerce'); D['v'] = pd.to_numeric(D['vertical(mm)'], errors='coerce')
D['clean'] = D.flg.map(lambda f: not (set(f) & {'broken', 'lost', 'alt'})) & D.tok.map(lambda t: '000' not in t and 'ALT' not in t and len(t) > 0)
rows = []
for o, g in D.groupby('obj'):
    if not g.clean.all(): continue
    h, v = g.h.iloc[0], g.v.iloc[0]
    if not (h > 0 and v > 0): continue
    toks = [s for t in g.tok for s in t]
    nums = [NUMV[s] for s in toks if s in NUMV]
    name = '|'.join('-'.join(s for s in t if s not in NUMV) for t in g.tok)
    full = '|'.join('-'.join(t) for t in g.tok)
    rows.append(dict(obj=o, type=g.type.iloc[0].split(':')[0] + ':' + (g.type.iloc[0].split(':')[1] if ':' in g.type.iloc[0] else ''),
                     site=g.site.iloc[0], logA=np.log(h * v), area=h * v, count=sum(nums) if nums else np.nan, nnum=len(nums),
                     name=name, full=full, length=len(toks)))
T = pd.DataFrame(rows)
T['tg'] = T.type.str.split(':').str[0] + ':' + T.type.str.split(':').str[1].str[:1]
T['stratum'] = T.tg + '|' + T.site
log('S7', f'clean objects with a size: {len(T)}; by type: {T.tg.value_counts().to_dict()}; with a count: {int(T["count"].notna().sum())}')
T.to_csv(f'{OUT}/tablets.csv', index=False)
rr = np.random.default_rng(41)
def spread(r, lab):
    df = pd.DataFrame(dict(r=r, c=lab)); g = df.groupby('c').r.agg(['mean', 'size'])
    return (g['size'] * (g['mean'] - df.r.mean()) ** 2).sum()
out = []
for label, sub in [('all tablets and tags', T), ('moulded tablets TAB:B', T[T.tg == 'TAB:B']), ('incised tablets TAB:I', T[T.tg == 'TAB:I']),
                   ('copper tablets TAB:C', T[T.tg == 'TAB:C'])]:
    C = sub[sub['count'].notna()].copy()
    # count effect within stratum x name
    C['nk'] = C.stratum + '#' + C.name
    multi = C.groupby('nk')['count'].transform('nunique') >= 2
    Cn = C[multi].reset_index(drop=True)
    if len(Cn) >= 6:
        r = (Cn.logA - Cn.groupby('nk').logA.transform('mean')).values
        rho = spearmanr(r, Cn['count']).correlation
        real = spread(r, Cn['count'].values); groups = list(Cn.groupby('nk').indices.values()); null = []; nr = []
        for _ in range(2000):
            lab = Cn['count'].values.copy()
            for ix in groups: lab[ix] = lab[rr.permutation(ix)]
            null.append(spread(r, lab)); nr.append(spearmanr(r, lab).correlation)
        pc = np.mean(np.array(null) >= real); pr = np.mean(np.array(nr) <= rho)
        slope = np.polyfit(Cn['count'], r, 1)[0]
        log('S7', f'{label}: COUNT with name fixed: {len(Cn)} objects in {Cn.nk.nunique()} names; Spearman {rho:+.3f} (P negative {pr:.4f}); '
                  f'slope {slope:+.3f} logA per unit ({(np.exp(slope)-1)*100:+.1f}%); spread P {pc:.4f}')
        out.append(dict(set=label, test='count, name fixed', objects=len(Cn), groups=Cn.nk.nunique(), spearman=rho, P_dir=pr, slope=slope, P_spread=pc))
        # by count means
        log('S7', '   mean within-name residual by count: ' + ', '.join(f'{int(k)}: {v:+.3f} (n {n})' for k, (v, n) in Cn.assign(r=r).groupby('count').r.agg(['mean', 'size']).iterrows()))
    # name effect within stratum x count
    C['ck'] = C.stratum + '#' + C['count'].astype(str)
    nm = C.groupby(['ck', 'name'])['logA'].transform('size') >= 2
    Cc = C[nm & (C.groupby('ck').name.transform('nunique') >= 2)].reset_index(drop=True)
    if len(Cc) >= 6:
        Cc = Cc[Cc.groupby('ck').name.transform('nunique') >= 2].reset_index(drop=True)
        r = (Cc.logA - Cc.groupby('ck').logA.transform('mean')).values
        real = spread(r, Cc.name.values); groups = list(Cc.groupby('ck').indices.values()); null = []
        for _ in range(2000):
            lab = Cc.name.values.copy()
            for ix in groups: lab[ix] = lab[rr.permutation(ix)]
            null.append(spread(r, lab))
        pn = np.mean(np.array(null) >= real)
        share = real / (r ** 2).sum()
        log('S7', f'{label}: NAME with count fixed: {len(Cc)} objects, {Cc.name.nunique()} names; share of within-count spread between names {share:.3f} '
                  f'(dealt {np.mean(null)/(r**2).sum():.3f}); P {pn:.4f}')
        out.append(dict(set=label, test='name, count fixed', objects=len(Cc), groups=Cc.name.nunique(), share=share, share_dealt=np.mean(null) / (r ** 2).sum(), P_spread=pn))
# batches: identical full texts, moulded
Bt = T[T.tg == 'TAB:B']; Bt = Bt[Bt.groupby(['site', 'full'])['logA'].transform('size') >= 2]
w = (Bt.logA - Bt.groupby(['site', 'full']).logA.transform('mean')).var(); b = Bt.groupby(['site', 'full']).logA.mean().var()
log('S7', f'moulded batches (identical text, 2+ tablets): {Bt.groupby(["site","full"]).ngroups} batches, {len(Bt)} tablets; within-batch variance {w:.4f}, between-batch variance of means {b:.4f}')
out.append(dict(set='moulded batches', test='within vs between variance', objects=len(Bt), groups=Bt.groupby(['site', 'full']).ngroups, share=w / b))
pd.DataFrame(out).to_csv(f'{OUT}/tablets_tests.csv', index=False)
