#!/usr/bin/env python3
"""FRONT job 10: do the two slot families (front word + 002, front word + 060) differ?  2026-11-17.
Prediction (written before the numbers): the 002 family is the stamping family: its texts turn up as clay impressions
more than the 060 family's (multi-stamp lumps carry 861-002 and 820-002), P < 0.05 with the family label dealt within
site; seal size, ending, animal and time do not differ.
"""
from front_common import *
say = make_logger('log_10_families.txt')
rng = np.random.default_rng(10)
D = load(); F, *_ = front_set(D, say); D = add_parse(D, F)
D['resid'] = np.nan
S0 = D[(D.kind == 'seal') & D.complete & D.area_mm2.notna()]
D.loc[S0.index, 'resid'] = size_resid(S0)
E = copy_events(D[D.first_ok & D.slot1.isin(['002', '060'])]).copy()
E['fam'] = E.slot1
E['imp'] = (E.kind == 'tag') | E.type.isin(['POT:T:s', 'POT:T:S'])
def ecls(r):
    if r.is_count: return 'count'
    if not r.has_closer: return 'none'
    return {'740': 'jar'}.get(r.endstr, 'man' if '090' in r.endstr else 'spear' if r.endstr.startswith('520') else 'other')
E['ecls'] = [ecls(r) for r in E.itertuples()]
say(f'family texts (copy events): {E.fam.value_counts().to_dict()}')
def test(nm, sub, stat, grp):
    lab = (sub.fam == '002').values
    o = stat(sub, lab); null = [stat(sub, deal_within(lab, grp(sub), rng).astype(bool)) for _ in range(3000)]
    say(f'  {nm}: 002 minus 060 = {o:+.3f}, dealt {np.mean(null):+.3f}, P high {pval_hi(null, o):.4f}, P low {pval_lo(null, o):.4f}')
    return dict(attribute=nm, diff=round(o, 3), dealt=round(np.mean(null), 3), P_high=pval_hi(null, o), P_low=pval_lo(null, o))
rows = []
rows.append(test('impression share', E, lambda s, l: s.imp.values[l].mean() - s.imp.values[~l].mean(), lambda s: s.site.values))
Ss = E[(E.kind == 'seal') & E.resid.notna()]
rows.append(test('seal size residual (mean)', Ss, lambda s, l: s.resid.values[l].mean() - s.resid.values[~l].mean(), lambda s: s.site.values))
Ec = E[E.complete]
for e in ('count', 'jar', 'man', 'spear'):
    rows.append(test(f'ending {e} share', Ec, lambda s, l, e=e: (s.ecls.values[l] == e).mean() - (s.ecls.values[~l] == e).mean(), lambda s: s.site.values))
Sa = E[(E.kind == 'seal') & (E.animal != '')]
rows.append(test('unicorn share (seals)', Sa, lambda s, l: (s.animal.values[l] == 'unicorn').mean() - (s.animal.values[~l] == 'unicorn').mean(), lambda s: s.site.values))
Mh = E[E.site.isin(['Harappa', 'Mohenjo-daro'])]
rows.append(test('Harappa share (of MD+HP)', Mh, lambda s, l: (s.site.values[l] == 'Harappa').mean() - (s.site.values[~l] == 'Harappa').mean(), lambda s: s.kind.values))
Tb = E[E.bin != '']
rows.append(test('early-bin share', Tb, lambda s, l: (s.bin.values[l] == 'early').mean() - (s.bin.values[~l] == 'early').mean(), lambda s: s.site.values))
pd.DataFrame(rows).to_csv(f'{OUTF}/f10_family_tests.csv', index=False)
say('impressions: ' + str(E.groupby('fam').imp.agg(['sum', 'size']).to_dict('index')))
