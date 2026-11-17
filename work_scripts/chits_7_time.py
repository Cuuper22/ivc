#!/usr/bin/env python3
"""CHITS 7: time.  Are the Harappa 740-400 tablets from every period or one?  Did amounts or names change?

Bins (work_data/time/time_axis.csv) at Harappa: early = Period 3B, middle = 3B/C, 3C, 3C-1, 3C-2, late = 3C-3 and after.
Controls: comb share per bin against bin labels shuffled among Harappa tablets of the same format (moulded TAB:B /
incised TAB:I) and trench; cups by bin and name overlap between bins against bins shuffled among the comb tablets.

PREDICTIONS (written before any number):
 T1 comb tablets cluster in the middle bin (3B/C to 3C) more than other Harappa tablets.
 T2 cups do not change between bins; the set of names turns over (late names mostly new).
Writes work_data/chits/c7_*.csv, c7_log.txt.
"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chits_common import *
LOG = open(f'{OUT}/c7_log.txt', 'w'); say = say_to(LOG)
O = load(); rng = np.random.default_rng(77)
H = O[(O.site == 'Harappa') & (O.kind == 'mtab')].copy()
H['comb'] = [any(j is not None and j[1] == '400' for j in js) for js in H.jars]
H['jaronly'] = [any(j is not None and j[1] == '' for j in js) for js in H.jars]
H['name'] = [next(('-'.join(j[0]) for j in js if j is not None and len(j[0]) > 0), '') for js in H.jars]
H['cups'] = [next((amount_of(f)['cup'] for f in fs if 'cup' in amount_of(f)), None) for fs in H.faces]
D = H[H.bin != '']
say(f'Harappa tablets {len(H)}, dated {len(D)}; comb tablets {int(H.comb.sum())}, dated {int(D.comb.sum())}')
rows = []
for b in ('early', 'middle', 'late'):
    s = D[D.bin == b]
    rows.append(dict(bin=b, tablets=len(s), comb=int(s.comb.sum()), comb_share=round(s.comb.mean(), 3), jar_only=int(s.jaronly.sum()),
                     periods=fmt_counter(collections.Counter(s[s.comb].time)), comb_formats=fmt_counter(collections.Counter(s[s.comb].type)),
                     comb_cups=fmt_counter(dict(sorted(collections.Counter(int(x) for x in s[s.comb].cups.dropna()).items()))),
                     jaronly_cups=fmt_counter(dict(sorted(collections.Counter(int(x) for x in s[s.jaronly].cups.dropna()).items()))),
                     comb_names=s[s.comb].name.nunique()))
TB = pd.DataFrame(rows); TB.to_csv(f'{OUT}/c7_bins.csv', index=False)
for _, r in TB.iterrows():
    say(f'  {r.bin:6s} tablets {r.tablets:4d} comb {r.comb:3d} ({r.comb_share:.1%}) jar-only {r.jar_only:3d} | comb periods {r.periods} | formats {r.comb_formats} | comb cups {r.comb_cups} | jar-only cups {r.jaronly_cups} | comb names {r.comb_names}')
# comb share per bin against shuffles within format x trench
grp = D.groupby(['type', 'area']).indices; x = D.comb.values; bins = D.bin.values
obs = {b: x[bins == b].mean() for b in ('early', 'middle', 'late')}; nul = {b: [] for b in obs}
for _ in range(4000):
    bb = bins.copy()
    for g, ix in grp.items(): bb[ix] = rng.permutation(bins[ix])
    for b in obs: nul[b].append(x[bb == b].mean())
for b in obs:
    n = np.array(nul[b]); say(f'  comb share {b}: {obs[b]:.3f} against {n.mean():.3f} with bins shuffled within format and trench (P high {(n >= obs[b]).mean():.4f}, P low {(n <= obs[b]).mean():.4f})')
# all periods strings for comb
say('  comb tablets by catalogue period: ' + fmt_counter(collections.Counter(H[H.comb].time.replace('', '(none)'))))
say('  all Harappa tablets by period:   ' + fmt_counter(collections.Counter(H.time.replace('', '(none)')), 12))
# names by bin among comb tablets
C = D[D.comb & (D.name != '')]
def overlap(df):
    s = {b: set(df[df.bin == b].name) for b in ('early', 'middle', 'late')}
    return len(s['early'] & s['middle']), len(s['middle'] & s['late']), len(s['early'] & s['late'])
o = overlap(C); nn = []
for _ in range(4000): nn.append(overlap(C.assign(bin=rng.permutation(C.bin.values))))
nn = np.array(nn)
say(f'  comb names shared early&middle {o[0]} (shuffled {nn[:, 0].mean():.2f}, P low {(nn[:, 0] <= o[0]).mean():.4f}); middle&late {o[1]} ({nn[:, 1].mean():.2f}, P low {(nn[:, 1] <= o[1]).mean():.4f}); early&late {o[2]} ({nn[:, 2].mean():.2f})')
for b in ('early', 'middle', 'late'):
    say(f'    {b}: ' + fmt_counter(collections.Counter(C[C.bin == b].name), 10))
# cups by bin, comb tablets
Cc = D[D.comb & D.cups.notna()]
def mean_by(df): return {b: df[df.bin == b].cups.mean() for b in ('early', 'middle', 'late')}
om = mean_by(Cc); spread = np.nanmax(list(om.values())) - np.nanmin(list(om.values())); ns = []
for _ in range(4000):
    m = mean_by(Cc.assign(bin=rng.permutation(Cc.bin.values))); ns.append(np.nanmax(list(m.values())) - np.nanmin(list(m.values())))
ns = np.array(ns)
say(f'  comb mean cups by bin {", ".join(f"{k} {v:.2f}" for k, v in om.items())}; spread {spread:.2f} against {ns.mean():.2f} shuffled (P {(ns >= spread).mean():.4f})')
# depth for name 176
s = H[(H.name == '176') & H.comb]
say(f'  name 176 comb tablets: {len(s)}; bins {fmt_counter(collections.Counter(s.bin.replace("", "?")))}; periods {fmt_counter(collections.Counter(s.time.replace("", "?")))}')
say('done')
