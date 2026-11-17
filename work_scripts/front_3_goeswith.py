#!/usr/bin/env python3
"""FRONT job 3: what each front goes with.  2026-11-17.

For each front word (and for 'no front'): endings, count line or name, crests, seal size against matched seals (same
site group, length, format), share found as clay impressions (tags and stamped pots), Harappa against Mohenjo-daro,
animal. Unit = copy events. Front FAMILIES (from front_1): the 002 family = front word followed by 002 (817 861 824 880
820); the 060 family = front word followed by 060 (920 692 550 201 820). 820 is in both by its slot.

Control (dealt labels): the front-word label dealt among front-initial copy events of the same site and object kind,
5,000 deals; statistic = chi-square of front word x attribute.  A real difference between front words beats the deals.

Predictions, written before the numbers:
 P1  the front words are NOT free variants of one another: endings differ by front word beyond dealing (P < 0.01),
     with the 060 family (920 692 550) taking the man ending 090 and the spear more than the 002 family.
 P2  two kinds of front: the 002 family heads count lines (count-line share 5%+), the 060 family heads names only
     (count-line share under 3%).
 P3  fronted seals are bigger than matched frontless seals; the 060 family the biggest.
 P4  the 002 family is pressed on clay (impression share) more than the 060 family (multi-stamp lumps carry 861-002).
"""
from front_common import *

say = make_logger('log_3_goeswith.txt')
rng = np.random.default_rng(3)
D = load(); F, *_ = front_set(D, say); D = add_parse(D, F)
D['resid'] = np.nan
S = D[(D.kind == 'seal') & D.complete & D.area_mm2.notna()]
D.loc[S.index, 'resid'] = size_resid(S)
E = copy_events(D[D.first_ok]).copy()
E['impression'] = (E.kind == 'tag') | (E.type.str.startswith('POT:T:s') | (E.type == 'POT:T:S'))
FISH = {'220', '231', '233', '240', '226', '222', '243', '235'}


def end_cls(r):
    if r.is_count: return 'count line'
    if not len(r.name) and not r.ending: return 'front only'
    e = r.endstr
    if not r.has_closer:
        return 'title, no closer' if e else 'no ending'
    if e == '740': return 'jar'
    if e.startswith('740-400') or e == '740-400': return 'jar+comb 400'
    if e.startswith('740-090'): return 'jar+man 090'
    if e.startswith('740-'): return 'jar+other title'
    if e.startswith('520'): return 'spear 520'
    if e[:3] in ('151', '154', '155', '158'): return 'porter'
    return 'other closer'


def crest_cls(c):
    if not c: return '-'
    if c in FISH: return 'fish'
    if c == '176': return '176'
    if c in ('590', '415', '255', '798', '840'): return c
    return 'other'


E['ecls'] = [end_cls(r) for r in E.itertuples()]
E['ccls'] = E.crest.map(crest_cls)
E['family'] = [('002' if r.slot1 == '002' else '060' if r.slot1 == '060' else 'other slot' if r.slot1 else 'no slot')
               if r.front else 'none' for r in E.itertuples()]
E['fw'] = E.front.where(E.front != '', 'none')
E['comp'] = E.complete

MAINF = ['817', '861', '820', '920', '692', '550', '091', '824']
rows = []
for f in MAINF + ['none']:
    g = E[E.fw == f]; gc = g[g.comp]
    sz = g[(g.kind == 'seal')].resid.dropna()
    rows.append(dict(front=f, events=len(g), complete=len(gc),
                     count_line=round((gc.ecls == 'count line').mean(), 3),
                     jar=round((gc.ecls == 'jar').mean(), 3), jar_comb=round((gc.ecls == 'jar+comb 400').mean(), 3),
                     jar_man=round((gc.ecls == 'jar+man 090').mean(), 3), spear=round((gc.ecls == 'spear 520').mean(), 3),
                     porter=round((gc.ecls == 'porter').mean(), 3),
                     fish_crest=round((gc[gc.ccls != '-'].ccls == 'fish').mean(), 3),
                     seals_sized=len(sz), size_resid_median=round(sz.median(), 3) if len(sz) else '',
                     size_resid_mean=round(sz.mean(), 3) if len(sz) else '',
                     impression_share=round(g.impression.mean(), 3),
                     seal_share=round((g.kind == 'seal').mean(), 3), tablet_share=round((g.kind == 'tablet').mean(), 3),
                     MD=int((g.site == 'Mohenjo-daro').sum()), HP=int((g.site == 'Harappa').sum()),
                     HP_share_of_MD_HP=round((g.site == 'Harappa').sum() / max(1, g.site.isin(['Harappa', 'Mohenjo-daro']).sum()), 3),
                     unicorn_of_seals=round((g[(g.kind == 'seal') & (g.animal != '')].animal == 'unicorn').mean(), 3)))
T = pd.DataFrame(rows); T.to_csv(f'{OUTF}/f3_by_front.csv', index=False)
say('\nBY FRONT WORD (copy events; shares among complete texts):'); say(T.to_string(index=False))

# families
rows = []
for f in ['002', '060', 'other slot', 'no slot', 'none']:
    g = E[E.family == f]; gc = g[g.comp]; sz = g[g.kind == 'seal'].resid.dropna()
    rows.append(dict(family=f, events=len(g), complete=len(gc), count_line=round((gc.ecls == 'count line').mean(), 3),
                     jar_man=round((gc.ecls == 'jar+man 090').mean(), 3), jar_comb=round((gc.ecls == 'jar+comb 400').mean(), 3),
                     spear=round((gc.ecls == 'spear 520').mean(), 3), size_resid_median=round(sz.median(), 3) if len(sz) else '',
                     seals_sized=len(sz), impression_share=round(g.impression.mean(), 3),
                     HP_share=round((g.site == 'Harappa').sum() / max(1, g.site.isin(['Harappa', 'Mohenjo-daro']).sum()), 3)))
TF = pd.DataFrame(rows); TF.to_csv(f'{OUTF}/f3_by_family.csv', index=False)
say('\nBY FAMILY (slot after the front word):'); say(TF.to_string(index=False))

# ending table
say('\nending class by front word (complete copy events):')
et = pd.crosstab(E[E.comp].fw, E[E.comp].ecls); say(et.to_string()); et.to_csv(f'{OUTF}/f3_endings.csv')


# ---------- dealt-label control
def chi(a, b):
    t = pd.crosstab(a, b).values.astype(float)
    if t.shape[0] < 2 or t.shape[1] < 2: return 0.0
    e = t.sum(1, keepdims=True) * t.sum(0, keepdims=True) / t.sum()
    return float(((t - e) ** 2 / np.where(e > 0, e, 1)).sum())


X = E[E.fw.isin(MAINF)].copy()
Xc = X[X.comp]
tests = [('ending class', Xc, 'ecls', (Xc.site + Xc.kind).values),
         ('count line vs not', Xc, Xc.ecls.eq('count line').map(str).name if False else None, None),
         ('crest class', Xc[Xc.ccls != '-'], 'ccls', None),
         ('impression or not', X, 'impression', None),
         ('Harappa vs Mohenjo-daro', X[X.site.isin(['Harappa', 'Mohenjo-daro'])], 'site', None),
         ('object kind', X, 'kind', None),
         ('time bin', X[X.bin != ''], 'bin', None),
         ('animal (seals)', X[(X.kind == 'seal') & (X.animal != '')], 'animal', None)]
Xc = Xc.assign(isc=Xc.ecls.eq('count line'))
tests[1] = ('count line vs not', Xc, 'isc', None)
rows = []
for nm, sub, col, _ in tests:
    if nm in ('Harappa vs Mohenjo-daro',): grp = sub.kind.values
    elif nm == 'object kind': grp = sub.site.values
    else: grp = (sub.site + '|' + sub.kind).values
    if nm == 'animal (seals)':
        a = sub.animal.where(sub.animal.isin(['unicorn', 'none']), 'other').values
    else:
        a = sub[col].astype(str).values
    o = chi(sub.fw.values, a)
    null = [chi(deal_within(sub.fw.values, grp, rng), a) for _ in range(3000)]
    rows.append(dict(attribute=nm, n=len(sub), chi2=round(o, 1), dealt_mean=round(np.mean(null), 1),
                     dealt_95=round(np.percentile(null, 95), 1), P=round(pval_hi(null, o), 4)))
    say(f'  {nm}: chi2 {o:.1f} against dealt mean {np.mean(null):.1f} (95th {np.percentile(null, 95):.1f}), P {pval_hi(null, o):.4f}, n {len(sub)}')
pd.DataFrame(rows).to_csv(f'{OUTF}/f3_dealt_tests.csv', index=False)

# family test: count-line share 002 vs 060
g2 = E[(E.family == '002') & E.comp]; g6 = E[(E.family == '060') & E.comp]
a2, a6 = int((g2.ecls == 'count line').sum()), int((g6.ecls == 'count line').sum())
from math import comb
say(f'\ncount lines: 002 family {a2} of {len(g2)}, 060 family {a6} of {len(g6)}')
lab = np.r_[np.ones(len(g2)), np.zeros(len(g6))]; val = np.r_[(g2.ecls == 'count line').values, (g6.ecls == 'count line').values]
null = [val[rng.permutation(len(val))][:len(g2)].sum() for _ in range(10000)]
say(f'  family label dealt: 002-family count lines dealt mean {np.mean(null):.2f}, P(>= {a2}) {pval_hi(null, a2):.4f}')
# size: fronted vs frontless, then family vs family
sz_f = E[(E.kind == 'seal') & (E.fw != 'none')].resid.dropna(); sz_n = E[(E.kind == 'seal') & (E.fw == 'none')].resid.dropna()
v = np.r_[sz_f.values, sz_n.values]
null = [np.median(v[rng.permutation(len(v))][:len(sz_f)]) - np.median(v[len(sz_f):]) for _ in range(1)]
dd = []
for _ in range(5000):
    p = rng.permutation(len(v)); dd.append(np.median(v[p[:len(sz_f)]]) - np.median(v[p[len(sz_f):]]))
obs = sz_f.median() - sz_n.median()
say(f'\nseal size residual: fronted median {sz_f.median():+.3f} (n {len(sz_f)}), frontless {sz_n.median():+.3f} (n {len(sz_n)}); '
    f'difference {obs:+.3f}, labels dealt P(>=) {pval_hi(dd, obs):.4f}')
for fam in ('002', '060'):
    s = E[(E.kind == 'seal') & (E.family == fam)].resid.dropna()
    say(f'  family {fam}: median residual {s.median():+.3f}, mean {s.mean():+.3f}, n {len(s)}')
