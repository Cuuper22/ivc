#!/usr/bin/env python3
"""FRONT job 2: the same name with a front and without one, or with two different fronts.  2026-11-17.

Name = the signs between the front unit and the ending (front_common); only complete faces whose ending holds a closer.
Unit = copy events (same site, same findspot, same text = once).
Control: the front unit (or 'none') dealt at random among texts of the same name length and the same site, 2,000 deals;
the names stay where they are.

Predictions, written before the numbers:
 P1  the front is a title or office, added to a person's name on some stones and not on others: names that occur both
     with and without a front come to at least 60% of what dealing gives (a name part would give near 0).
     Bold version, the one I bet on: AT chance (ratio 0.8-1.2): the front is free of the name.
 P2  two different front words on one name are rarer than dealing gives (ratio < 0.6): a person holds one front, if any.
 P3  where a name has a fronted and a frontless copy, the fronted one is on a seal and the frontless one is ALSO a seal
     more often than not (same kind of object), and the two are in different buildings (a title on some of a man's
     seals, not a store copy).
 P4  the fronted seal of a pair is larger than its frontless twin once length is matched (a title stone is a bigger stone).
"""
from front_common import *

say = make_logger('log_2_withwithout.txt')
rng = np.random.default_rng(2)
D = load(); F, *_ = front_set(D, say); D = add_parse(D, F)
D['resid'] = np.nan
S = D[(D.kind == 'seal') & D.complete & D.area_mm2.notna()]
D.loc[S.index, 'resid'] = size_resid(S)
N = D[D.complete & (D.name.map(len) > 0) & D.has_closer].copy()
N = copy_events(N)
N['nlen'] = N.name.map(len)
say(f'copy events with a name and a closer: {len(N)}; with a front {int((N.front != "").sum())}')


def stats(names, units):
    by = collections.defaultdict(set)
    for n, u in zip(names, units): by[n].add(u)
    both = sum(1 for s in by.values() if '' in s and len(s) > 1)
    two = sum(1 for s in by.values() if len({u.split('-')[0] for u in s if u}) >= 2)
    twounit = sum(1 for s in by.values() if len({u for u in s if u}) >= 2)
    return both, two, twounit


def run(sub, tag, key, bykind=False):
    names = sub[key].values; units = sub.unit.values
    grp = (sub.nlen.astype(str) + '|' + sub.site + ('|' + sub.kind if bykind else '')).values
    ob = stats(names, units)
    null = np.array([stats(names, deal_within(units, grp, rng)) for _ in range(2000)])
    say(f'\n[{tag}] texts {len(sub)}, distinct names {sub[key].nunique()}, fronted texts {int((sub.unit != "").sum())}')
    for i, lab in enumerate(['names with AND without a front', 'names with two different front WORDS',
                             'names with two different front UNITS (word+slot)']):
        say(f'  {lab}: {ob[i]} against {null[:, i].mean():.2f} dealt (ratio {ob[i]/max(1e-9, null[:, i].mean()):.2f}; '
            f'P low {pval_lo(null[:, i], ob[i]):.4f}, P high {pval_hi(null[:, i], ob[i]):.4f})')
    return ob, null


res = {}
res['all'] = run(N, 'all names', 'namestr')
res['len2'] = run(N[N.nlen >= 2], 'names of 2+ signs', 'namestr')
N['name_end'] = N.namestr + '|' + N.endstr
res['ne'] = run(N, 'name + same ending', 'name_end')
res['seal'] = run(N[N.kind == 'seal'], 'seals only', 'namestr')
res['all_kind'] = run(N, 'all names, dealt within length + site + object kind (redesign)', 'namestr', True)
res['len2_kind'] = run(N[N.nlen >= 2], 'names of 2+ signs, dealt within length + site + kind', 'namestr', True)
res['seal_len2'] = run(N[(N.kind == 'seal') & (N.nlen >= 2)], 'seals only, names of 2+ signs', 'namestr')
pd.DataFrame([dict(test=k, both=v[0][0], both_dealt=round(v[1][:, 0].mean(), 2), two_words=v[0][1],
                   two_words_dealt=round(v[1][:, 1].mean(), 2), two_units=v[0][2], two_units_dealt=round(v[1][:, 2].mean(), 2),
                   P_both_low=pval_lo(v[1][:, 0], v[0][0]), P_both_high=pval_hi(v[1][:, 0], v[0][0]),
                   P_two_low=pval_lo(v[1][:, 1], v[0][1]))
              for k, v in res.items()]).to_csv(f'{OUTF}/f2_tests.csv', index=False)

# ---------- the cases
rows = []
for n, g in N.groupby('namestr'):
    if not ((g.unit == '').any() and (g.unit != '').any()) and g[g.unit != ''].front.nunique() < 2: continue
    for r in g.itertuples():
        rows.append(dict(name=n, nlen=r.nlen, front=r.unit or '-', text=r.signs, kind=r.kind, site=r.site,
                         building=r.building, bin=r.bin, animal=r.animal, area_mm2=r.area_mm2,
                         size_resid=round(r.resid, 3) if r.resid == r.resid else '', cisi=r.cisi, face=r.face))
C = pd.DataFrame(rows); C.to_csv(f'{OUTF}/f2_cases.csv', index=False)
say(f'\nCASES written: {C.name.nunique()} names, {len(C)} texts (f2_cases.csv). Names of 2+ signs:')
say(C[C.nlen >= 2].drop(columns=['face']).to_string(index=False))

# ---------- inside the with/without cases: object kind, city, building, size, animal
pairs = []
for n, g in N.groupby('namestr'):
    a = g[g.unit != '']; b = g[g.unit == '']
    for x in a.itertuples():
        for y in b.itertuples():
            pairs.append(dict(name=n, nlen=x.nlen, fk=x.kind, nk=y.kind, same_site=x.site == y.site,
                              same_bld=bool(x.building) and x.building == y.building,
                              fr=x.resid, nr=y.resid, fa=x.animal, na=y.animal, same_end=x.endstr == y.endstr))
P = pd.DataFrame(pairs)
P.to_csv(f'{OUTF}/f2_pairs.csv', index=False)
say(f'\nwith/without pairs: {len(P)} (names {P.name.nunique()})')
say('object kinds (fronted -> frontless):'); say(pd.crosstab(P.fk, P.nk).to_string())
say(f'same city {P.same_site.mean():.2f}; same building {int(P.same_bld.sum())}; same ending {P.same_end.mean():.2f}')
ss = P[(P.fk == 'seal') & (P.nk == 'seal')].dropna(subset=['fr', 'nr'])
if len(ss):
    dlt = (ss.fr - ss.nr).values
    flips = [np.mean(dlt * rng.choice([-1, 1], len(dlt))) for _ in range(5000)]
    say(f'seal-seal pairs with sizes {len(ss)}: fronted minus frontless residual size mean {dlt.mean():+.3f}, '
        f'fronted larger in {int((dlt > 0).sum())}; sign-flip P (larger) {pval_hi(flips, dlt.mean()):.4f}')
an = P[(P.fk == 'seal') & (P.nk == 'seal') & (P.fa != '') & (P.na != '')]
say(f'seal-seal pairs with both animals known {len(an)}: same animal {int((an.fa == an.na).sum())}')
# base rate: same-name seal pairs (both frontless) same animal
base = []
for n, g in N[(N.kind == 'seal') & (N.unit == '') & (N.animal != '')].groupby('namestr'):
    a = g.animal.values
    for i in range(len(a)):
        for j in range(i + 1, len(a)): base.append(a[i] == a[j])
say(f'base: same-name frontless seal pairs same animal {np.mean(base):.2f} of {len(base)}')
