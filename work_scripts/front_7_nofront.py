#!/usr/bin/env python3
"""FRONT job 7: seals without a front.  Default or the marked case?  2026-11-17.

Compare complete seal texts with and without a front (copy events): size against matched seals (front_common.size_resid),
animal, city, time bin, ending, name length, format.  Then the ADDITION test: if the front is something put in front
of an ordinary text, the rest of a fronted text (after the front unit) should itself be attested as a whole frontless
text more often than a frontless text with its first k signs cut off (k = the length of the front unit it is matched to).

Predictions, written before the numbers:
 P1  no front is the default: 70%+ of seal texts have none; fronted and frontless seals differ in NOTHING physical
     (size, animal, city, time) beyond chance, they differ in the ending (fronted texts end in the plain jar more,
     comb less).
 P2  the front is an addition: the rest of a fronted text is a whole attested frontless text 3+ times as often as the
     cut-off control.
 P3  names behind a front have the same length as frontless names (difference under 0.2 sign).
"""
from front_common import *

say = make_logger('log_7_nofront.txt')
rng = np.random.default_rng(7)
D = load(); F, *_ = front_set(D, say); D = add_parse(D, F)
D['resid'] = np.nan
S0 = D[(D.kind == 'seal') & D.complete & D.area_mm2.notna()]
D.loc[S0.index, 'resid'] = size_resid(S0)
S = copy_events(D[(D.kind == 'seal') & D.complete]).copy()
S['hasf'] = S.front != ''
say(f'complete seal copy events {len(S)}; with a front {int(S.hasf.sum())} ({S.hasf.mean():.3f})')


def perm_diff(vals, lab, grp, stat, n=3000):
    o = stat(vals[lab]) - stat(vals[~lab])
    null = []
    for _ in range(n):
        l2 = deal_within(lab, grp, rng).astype(bool); null.append(stat(vals[l2]) - stat(vals[~l2]))
    return o, np.mean(null), pval_hi(null, o), pval_lo(null, o)


def chi(a, b):
    t = pd.crosstab(a, b).values.astype(float)
    e = t.sum(1, keepdims=True) * t.sum(0, keepdims=True) / t.sum()
    return float(((t - e) ** 2 / np.where(e > 0, e, 1)).sum())


rows = []
# size (residual already matched on site group, length, format)
X = S[S.resid.notna()]
o, m, ph, pl = perm_diff(X.resid.values, X.hasf.values, X.site.values, np.median)
rows.append(dict(attribute='size residual, median difference (front - none)', fronted=round(X[X.hasf].resid.median(), 3),
                 frontless=round(X[~X.hasf].resid.median(), 3), observed=round(o, 3), dealt=round(m, 3), P_high=ph, P_low=pl))
X2 = S[S.area_mm2.notna()]
o, m, ph, pl = perm_diff(np.log(X2.area_mm2.values), X2.hasf.values, X2.site.values, np.median)
rows.append(dict(attribute='raw log area, median difference', fronted=round(np.log(X2[X2.hasf].area_mm2).median(), 3),
                 frontless=round(np.log(X2[~X2.hasf].area_mm2).median(), 3), observed=round(o, 3), dealt=round(m, 3), P_high=ph, P_low=pl))
o, m, ph, pl = perm_diff(S.L.values.astype(float), S.hasf.values, S.site.values, np.mean)
rows.append(dict(attribute='text length, mean difference', fronted=round(S[S.hasf].L.mean(), 2), frontless=round(S[~S.hasf].L.mean(), 2),
                 observed=round(o, 2), dealt=round(m, 2), P_high=ph, P_low=pl))
NL = S[(S.name.map(len) > 0) & S.has_closer]
NL = NL.assign(nlen=NL.name.map(len).astype(float))
o, m, ph, pl = perm_diff(NL.nlen.values, NL.hasf.values, NL.site.values, np.mean)
rows.append(dict(attribute='name length (name + closer texts), mean difference', fronted=round(NL[NL.hasf].nlen.mean(), 2),
                 frontless=round(NL[~NL.hasf].nlen.mean(), 2), observed=round(o, 2), dealt=round(m, 2), P_high=ph, P_low=pl))
say('\nNUMERIC (labels dealt within site, 3000 deals):'); say(pd.DataFrame(rows).to_string(index=False))
pd.DataFrame(rows).to_csv(f'{OUTF}/f7_numeric.csv', index=False)


def ecls(r):
    if r.is_count: return 'count line'
    if not r.has_closer: return 'no closer'
    e = r.endstr
    if e == '740': return 'jar'
    if '400' in e: return 'comb'
    if '090' in e: return 'man'
    if e.startswith('520'): return 'spear'
    if e[:3] in ('151', '154', '155', '158'): return 'porter'
    return 'other'


S['ecls'] = [ecls(r) for r in S.itertuples()]
S['anim3'] = S.animal.where(S.animal.isin(['unicorn', 'none', 'short-horned bull', 'zebu', 'elephant']), 'other')
cat = [('ending', 'ecls', 'site'), ('animal', 'anim3', 'site'), ('format', 'fmt', 'site'), ('time bin', 'bin', 'site'),
       ('city', 'siteg', 'fmt')]
rows = []
for nm, col, g in cat:
    sub = S[S[col] != '']
    o = chi(sub.hasf.values, sub[col].values)
    null = [chi(deal_within(sub.hasf.values, sub[g].values, rng), sub[col].values) for _ in range(2000)]
    tab = pd.crosstab(sub[col], sub.hasf, normalize='columns').round(3)
    rows.append(dict(attribute=nm, chi2=round(o, 1), dealt=round(np.mean(null), 1), P=pval_hi(null, o)))
    say(f'\n{nm}: chi2 {o:.1f} against {np.mean(null):.1f} dealt within {g}, P {pval_hi(null, o):.4f}')
    say(tab.rename(columns={False: 'no front', True: 'front'}).to_string())
pd.DataFrame(rows).to_csv(f'{OUTF}/f7_categorical.csv', index=False)

# ---------- the addition test
ALL = copy_events(D[D.complete])
frontless_texts = set(ALL[ALL.front == ''].signs)
fronted = ALL[(ALL.front != '') & (ALL.body.map(len) >= 1)]
hit = [('-'.join(b) in frontless_texts) for b in fronted.body]
A = np.mean(hit)
# control: frontless texts with the first k signs cut, k matched to the front-unit lengths, body length matched
klen = collections.Counter(fronted.unit.map(lambda u: len(u.split('-'))))
fl = ALL[ALL.front == '']
ctrl = []
bodies = fronted.body.map(len).values
for _ in range(20):
    hits = 0; n = 0
    for bl in bodies:
        k = rng.choice(list(klen), p=np.array(list(klen.values())) / sum(klen.values()))
        cand = fl[fl.L == bl + k]
        if not len(cand): continue
        t = cand.tok.iloc[rng.integers(len(cand))]
        rest = '-'.join(t[k:]); n += 1
        hits += rest in frontless_texts and rest != '-'.join(t)
    ctrl.append(hits / max(1, n))
say(f'\nADDITION TEST: the rest of a fronted text (after the front unit) is a whole attested frontless text in '
    f'{sum(hit)} of {len(hit)} ({A:.3f}); frontless texts of matched length with k signs cut: {np.mean(ctrl):.3f} '
    f'(20 rounds, max {np.max(ctrl):.3f}); ratio {A / max(1e-9, np.mean(ctrl)):.2f}')
# by front unit and by kind of rest
fronted = fronted.assign(hit=hit)
say('by front unit (6+ texts): ' + str(fronted.groupby('unit').hit.agg(['sum', 'size']).query('size >= 6').to_dict('index')))
say('hits by body length: ' + str(fronted.groupby(fronted.body.map(len)).hit.agg(['sum', 'size']).to_dict('index')))
# reverse: frontless name+closer texts that appear somewhere with a front put before them
fb = set('-'.join(b) for b in fronted.body)
nc = fl[(fl.name.map(len) > 0) & fl.has_closer]
say(f'frontless name + closer texts that also stand whole behind a front: {int(nc.signs.isin(fb).sum())} of {len(nc)}')
ex = fronted[fronted.hit].head(30)
say('examples: ' + '; '.join(f'{u} + {"-".join(b)}' for u, b in zip(ex.unit, ex.body)))
