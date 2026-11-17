#!/usr/bin/env python3
"""Control step 2 + by-kind table. HOLD bar (same as the main report): scheme S2, first catalogue, held-out bits per sign over all
texts: real split better than the unsplit frame AND rank 1 of 21 against decoys A (site and kind kept) AND decoys B (plain random);
rank = 1 + number of decoys strictly better; ties are not counted against. Also reported: same bar on new texts (when the sign occurs
there) and for scheme S1. Output: work_data/split/controls_result.csv, bykind.csv, and printed tables."""
from split_common import *
def rk(g, sch, base, col='bits_all'):
    real = g.loc[f'real_{sch}', col]; u = g.loc[base, col]
    out = dict(real=real, unsplit=u)
    for nm in 'AB':
        dv = np.array([g.loc[f'dec{nm}{j}_{sch}', col] for j in range(20)]); out[f'rank{nm}'] = 1 + int((dv < real - 1e-9).sum())
        out[f'ties{nm}'] = int((abs(dv - real) <= 1e-9).sum())
    out['hold'] = bool(real < u - 1e-9 and out['rankA'] == 1 and out['rankB'] == 1)
    return out
C = pd.read_csv(f'{SPL}/controls.csv', dtype=str)
rows = []
for grp, s, cl, occ in zip(C.group, C.sign, C.v2class, C.occurrences):
    for defn in (['mix2'] if grp == 'for824' else ['mix2', 'mix3']):
        f = f'{SPL}/test_{s}_{defn}.csv'
        if not os.path.exists(f): continue
        D = pd.read_csv(f)
        r = dict(group=grp, sign=s, v2class=cl, occ_distinct=int(occ), split=defn)
        for ho, tag in (('first catalogue 10 fold fits', 'fc'), ('new texts', 'new')):
            g = D[D.heldout == ho].set_index('name')
            r[f'occ_{tag}'] = int(g.loc['U0', 'occ_with_sign'])
            for sch, base in (('S1', 'U1'), ('S2', 'U0')):
                o = rk(g, sch, base)
                for k, v in o.items(): r[f'{tag}_{sch}_{k}'] = v
        rows.append(r)
R = pd.DataFrame(rows); R.to_csv(f'{SPL}/controls_result.csv', index=False)
for grp, defn in (('for824', 'mix2'), ('for001', 'mix2'), ('for001', 'mix3')):
    G = R[(R.group == grp) & (R.split == defn)]
    n = len(G); new_ok = G[G.occ_new > 0]
    print(f'{grp} {defn}: {n} controls run; hold on first catalogue S2: {int(G.fc_S2_hold.sum())}; hold S1: {int(G.fc_S1_hold.sum())}; '
          f'S2 hold on BOTH first catalogue and new texts (of {len(new_ok)} with the sign in new texts): {int((new_ok.fc_S2_hold & new_ok.new_S2_hold).sum())}; '
          f'S2 hold on first catalogue with rank A and B both 1 and gain>0 and >=7 of 10 fits not computed')
    print(G[['sign', 'v2class', 'occ_distinct', 'fc_S2_unsplit', 'fc_S2_real', 'fc_S2_rankA', 'fc_S2_rankB', 'fc_S2_hold', 'fc_S1_hold', 'new_S2_real', 'new_S2_unsplit', 'new_S2_rankA', 'new_S2_rankB', 'new_S2_hold']].round(4).to_string(index=False))
# by-kind grammar table for the main runs
rows = []
for s in ['850', '824', '001']:
    for tag in ('', '_left'):
        D = pd.read_csv(f'{SPL}/test_{s}{tag}.csv')
        for (sp, ho), G in D.groupby(['split', 'heldout'], sort=False):
            g = G.set_index('name')
            rows.append(dict(sign=s, split=sp, heldout='first catalogue' if ho.startswith('first') else 'new texts', occ=int(g.loc['U0', 'occ_with_sign']),
                             U0_kind=g.loc['U0k', 'bits_all'], S2_real_kind=g.loc['realk_S2', 'bits_all'], U1_kind=g.loc['U1k', 'bits_all'], S1_real_kind=g.loc['realk_S1', 'bits_all'],
                             U0_pooled=g.loc['U0', 'bits_all'], S2_real_pooled=g.loc['real_S2', 'bits_all']))
B = pd.DataFrame(rows); B['S2_gain_kind'] = B.U0_kind - B.S2_real_kind; B['S1_gain_kind'] = B.U1_kind - B.S1_real_kind; B['S2_gain_pooled'] = B.U0_pooled - B.S2_real_pooled
B.to_csv(f'{SPL}/bykind.csv', index=False); print(B.round(4).to_string(index=False))

# ---- stricter, non-degenerate bar: rank 1 against both decoy kinds, at most 1 tie in either decoy set, and real better than unsplit by 1e-4 bits/sign or more
R['fc_strict'] = (R.fc_S2_hold) & (R.fc_S2_tiesA <= 1) & (R.fc_S2_tiesB <= 1) & (R.fc_S2_unsplit - R.fc_S2_real >= 1e-4)
R['new_strict'] = (R.new_S2_hold) & (R.new_S2_tiesA <= 1) & (R.new_S2_tiesB <= 1) & (R.new_S2_unsplit - R.new_S2_real >= 1e-4) & (R.occ_new > 0)
R['fc_strict_S1'] = (R.fc_S1_hold) & (R.fc_S1_tiesA <= 1) & (R.fc_S1_tiesB <= 1) & (R.fc_S1_unsplit - R.fc_S1_real >= 1e-4)
R.to_csv(f'{SPL}/controls_result.csv', index=False)
print('\nSTRICT BAR')
for grp, defn in (('for824', 'mix2'), ('for001', 'mix2'), ('for001', 'mix3')):
    G = R[(R.group == grp) & (R.split == defn)]
    print(grp, defn, 'n', len(G), 'plain-bar hold S2 fc', int(G.fc_S2_hold.sum()), '| strict fc S2', int(G.fc_strict.sum()), list(G[G.fc_strict].sign),
          '| strict S1 fc', int(G.fc_strict_S1.sum()), '| strict S2 both sets', int((G.fc_strict & G.new_strict).sum()), list(G[G.fc_strict & G.new_strict].sign),
          '| strict S2 new only', int(G.new_strict.sum()))
    print('   all-text gain of the strict-fc holders:', [round(a - b, 4) for a, b in zip(G[G.fc_strict].fc_S2_unsplit, G[G.fc_strict].fc_S2_real)])
