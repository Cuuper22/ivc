#!/usr/bin/env python3
"""EARLY job, step 4: does the deepest part of the OTHER Mohenjo-daro areas lack the fish crest too?
(Redesign of the one-level result: DK-G Early I is one dig. If "fish crest first" is missing in the deepest third of other areas as well,
the pattern is the town's, not one trench's.)

PLAIN WORDS
- Areas: the first catalogue's excavation area (HR, VS, DK-A..E, SD, L ...) and the second catalogue's locus code (not 31/32).
  Inside each area (12 or more seals with a depth) seals are split into thirds by depth: deepest third = "deep", the rest = "upper".
  Depth is never compared across areas.
- Fish crest first = a marked fish sign (231/233/235/240/236) is the first name sign with no lost sign in front (the clean form).
- Shuffle P: the deep/upper labels are mixed inside each area 10,000 times; P = share of shuffles with as few deep fish-crest seals
  as the real count or fewer.

PREDICTION (written before running): the deepest third of the other areas also has a lower fish-crest share than the upper two-thirds
(the real rate is about 11%; deep rate expected about 5%), in both catalogues.
Outputs: work_data/early/areas_deep_vs_upper.csv, log_4.txt
"""
import sys, os, io, contextlib, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    from time_common import *
from scipy.stats import fisher_exact

OUTE = f'{ROOT}/work_data/early'
rng = np.random.default_rng(11)


def clean_first(x, name):
    x = list(x)
    nm = [a for a in name if a not in ('000', 'ALT')]
    if not nm or nm[0] not in MARKED: return False
    i = x.index(nm[0])
    return all(a not in ('000', 'ALT') for a in x[:i])


# first catalogue
L = T[(T.site == 'Mohenjo-daro') & (T.kind == 'seal') & T.ft.notna() & (T.ft > 0) & ~T.area.str.startswith('DKG')].copy()
L['area2'] = L.area.str.strip()
L['fish'] = [clean_first(max(fs, key=len), n) if len(fs) else False for fs, n in zip(L.faces, L['name'])]
L['named'] = L['name'].apply(lambda n: len([a for a in n if a not in ('000', 'ALT')]) > 0)
# second catalogue
m = M[(M.site == 'MD') & (M.cls == 'seal') & ~M.locus.isin(['31', '32'])].copy()
m['lv'] = m.level.astype(int); m = m[m.lv < 0]; m['ft'] = -m.lv; m['n'] = m.n.astype(int)
m = m.sort_values('n', ascending=False).drop_duplicates('textnum')
m['area2'] = 'locus ' + m.locus
m['fish'] = [clean_first(t, tuple(nm.split('-')) if nm else ()) for t, nm in zip(m.tok, m['name'])]
m['named'] = m['name'].apply(lambda n: len([a for a in n.split('-') if a not in ('000', 'ALT', '')]) > 0)


def thirds(df):
    out = []
    for a, g in df.groupby('area2'):
        if len(g) < 12 or a in ('--', ''): continue
        q = g.ft.quantile(2 / 3)
        g = g.assign(deep=g.ft >= q)
        # ties at the cut: keep deep as the deepest third by rank, not by value
        r = g.ft.rank(method='first', ascending=False)
        g['deep'] = r <= round(len(g) / 3)
        out.append(g)
    return pd.concat(out)


rows = []
for lab, df in [('first catalogue (not DK-G)', L), ('second catalogue (not loci 31, 32)', m)]:
    G = thirds(df[df.named])
    deep, up = G[G.deep], G[~G.deep]
    a, b = int(deep.fish.sum()), int(up.fish.sum())
    t = [[a, len(deep) - a], [b, len(up) - b]]
    # within-area shuffle
    groups = [np.where(G.area2.values == x)[0] for x in G.area2.unique()]
    ndeep = [int(G.deep.values[ix].sum()) for ix in groups]
    fish = G.fish.values
    null = np.empty(10000)
    for k in range(10000):
        s = 0
        for ix, nd in zip(groups, ndeep):
            s += fish[rng.choice(ix, nd, replace=False)].sum()
        null[k] = s
    p = (np.sum(null <= a) + 1) / 10001
    print(f'{lab}: {len(G)} named seals in {len(groups)} areas; deep third {a}/{len(deep)} ({100 * a / len(deep):.1f}%) fish-crest-first against upper {b}/{len(up)} ({100 * b / len(up):.1f}%); '
          f'Fisher P {fisher_exact(t)[1]:.3g}; within-area shuffle P (as few or fewer in the deep third) {p:.4f} (shuffle mean {null.mean():.1f})')
    rows.append(dict(set=lab, named=len(G), areas=len(groups), deep=len(deep), deep_fish=a, upper=len(up), upper_fish=b, fisher_p=fisher_exact(t)[1], shuffle_p=p))
    # per area
    for x, g in G.groupby('area2'):
        d_, u_ = g[g.deep], g[~g.deep]
        print(f'     {x:12s} deep {int(d_.fish.sum())}/{len(d_)} upper {int(u_.fish.sum())}/{len(u_)}')
pd.DataFrame(rows).to_csv(f'{OUTE}/areas_deep_vs_upper.csv', index=False)
