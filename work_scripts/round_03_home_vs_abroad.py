#!/usr/bin/env python3
"""ROUND SEALS, step 3: home round seals against foreign round seals. Written 2026-11-17. No word on any sign.
Home = round_list tier 'home' (15 faces, 13 objects); Foreign = tiers 'abroad' + 'unknown site' (25 faces); Daimabad (South India) left out of both.
PREDICTION (written now): the two groups differ in make-up: person signs 3.6% of signs at home against ~18% abroad (Fisher P < 0.01);
stroke share is alike (28.6% vs 30%); home round seals carry the home animals (unicorn, composite, none) more than the short-horned bull,
foreign ones the bull (14 of 18+). Home round seals sit in the same few Mohenjo-daro areas as other seals (no special house).
Output: work_data/round/home_vs_abroad.csv, log_3.txt
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abroad4_common import *
from scipy.stats import fisher_exact
OUTR = f'{ROOT}/work_data/round'
L = pd.read_csv(f'{OUTR}/round_list.csv', dtype=str).fillna('')
PERSON = {'090', '091', '093', '095'}
STROKES = {s for s in GV if V2CLASS.get(s) in ('NUM_SHORT', 'NUM_TALL', 'NUM_NAME')} | {'001', '002', '003', '004', '005', '031', '032', '033', '055', '013'}
L['grp'] = L.tier.map({'home': 'home', 'abroad': 'foreign', 'unknown site': 'foreign'})
L = L[L.grp.isin(['home', 'foreign'])]
def toks(t): return [s for s in t.split('-') if real(s) and s in GIDX]
out = []
def fish(name, a, na, b, nb):
    o, p = fisher_exact([[a, na - a], [b, nb - b]])
    out.append(dict(measure=name, home=f'{a}/{na}', foreign=f'{b}/{nb}', home_pct=round(100 * a / max(na, 1), 1), foreign_pct=round(100 * b / max(nb, 1), 1), fisher_P_two_sided=round(p, 4)))
H = L[L.grp == 'home']; Fo = L[L.grp == 'foreign']
def tally(D, S): n = sum(len(toks(t)) for t in D.text); k = sum(s in S for t in D.text for s in toks(t)); return k, n
for nm, S in [('person signs (090 091 093 095), share of signs', PERSON), ('stroke signs, share of signs', STROKES), ('the man 090 alone', {'090'}), ('twin men 091 alone', {'091'})]:
    a, na = tally(H, S); b, nb = tally(Fo, S); fish(nm, a, na, b, nb)
def hasany(D, S): return sum(any(s in S for s in toks(t)) for t in D.text), len(D)
for nm, S in [('texts holding a person sign', PERSON), ('texts holding a stroke sign', STROKES)]:
    a, na = hasany(H, S); b, nb = hasany(Fo, S); fish(nm, a, na, b, nb)
fish('short-horned bull on the seal', (H.animal == 'SHORTHORN').sum(), len(H), (Fo.animal == 'SHORTHORN').sum(), len(Fo))
fish('pierced / boss recorded as P', H.pierced.eq('pierced').sum(), len(H), Fo.pierced.eq('pierced').sum(), len(Fo))
fish('cylinder (type SEAL:CY)', (H.type == 'SEAL:CY').sum(), len(H), (Fo.type == 'SEAL:CY').sum(), len(Fo))
fish('steatite recorded', (H.material == 'Steatite').sum(), len(H), (Fo.material == 'Steatite').sum(), len(Fo))
fish('lost or unclear sign in text', H.text.str.contains('000|ALT').sum(), len(H), Fo.text.str.contains('000|ALT').sum(), len(Fo))
R = pd.DataFrame(out); R.to_csv(f'{OUTR}/home_vs_abroad.csv', index=False); print(R.to_string())
print('\nanimal'); print(pd.crosstab(L.grp, L.animal))
print('\nmaterial'); print(pd.crosstab(L.grp, L.material))
print('\nboss'); print(pd.crosstab(L.grp, L.boss_code))
print('\nnumber of usable signs per text'); print(L.assign(n=L.text.map(lambda t: len(toks(t)))).groupby('grp').n.describe())
print('\nhome sites'); print(H.groupby(['site', 'area', 'house', 'bin']).size())
print('\nforeign sites'); print(Fo.groupby(['site']).size().sort_values(ascending=False))
# do the home round seals sit in the same areas as other home seals? share Mohenjo
hs = F[(F.tier == 'home') & (F.kind == 'seal')]
print('home seals at Mohenjo-daro: %.1f%% ; home round at Mohenjo-daro %d of %d faces' % (100 * (hs.site == 'Mohenjo-daro').mean(), (H.site == 'Mohenjo-daro').sum(), len(H)))
print('home seals by bin:'); print(pd.read_csv(f'{ROOT}/work_data/frame/seal_kinds.csv', dtype=str).query("abroad=='False'").bin.value_counts(normalize=True).round(3))
print('home round by bin:'); print(H.bin.value_counts())
# per-sign: signs of foreign round seals found on home round seals
hs_signs = set(s for t in H.text for s in toks(t)); fs_signs = set(s for t in Fo.text for s in toks(t))
print('home round signs', len(hs_signs), 'foreign round signs', len(fs_signs), 'shared', sorted(hs_signs & fs_signs))
print('shared pairs (adjacent, any order):')
def adjp(t):
    z = t.split('-'); return {frozenset((a, b)) for a, b in zip(z, z[1:]) if real(a) and real(b)}
hp = set().union(*[adjp(t) for t in H.text]); fp = set().union(*[adjp(t) for t in Fo.text]); print(hp & fp)
