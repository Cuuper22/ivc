#!/usr/bin/env python3
"""Recheck 10: the time-flat results (time_1_trends.py: agent seals 4.5 / 4.1 / 4.5%, fish-crest names 12.3 / 12.6 / 12.8%,
office opening 1.4 / 0.9 / 0.8% of all objects; Harappa inscription-only seals 14 of 99 to 33 of 98, P 0.0018) and the
earliest-level result (early_1_levels.py: fish crest first on 0 of 38 seals at the deepest Mohenjo-daro DK-G level).

Plain words: BIN = early / middle / late, from the excavators' periods or depth thirds inside an excavation area.
TREND P = bin labels shuffled inside each site x area, 5,000 times (two-sided). COPY EVENT = all objects of one site,
area and bin with the same full text, counted once.

Checks: (1) are the counts per face or per object? (time_common.objs: one row per object, faces joined; early_1:
one row per object, longest face; second-catalogue stones joined only when they do not match a first-catalogue stone);
(2) shuffle pool = dated objects of the same site x area (all eligible); (c) moulded copies inside one bin and area
swelling a share. Clean run: stones merged, copy events once.
Run: python3 recheck_10_time_early.py   (about 1-2 minutes)
"""
import sys, io, contextlib
sys.path.insert(0, '/home/claude/ivc/work_scripts')
import numpy as np, pandas as pd
from scipy.stats import fisher_exact
from recheck_common import *
say = log_to(f'{OUT}/r10_log.txt')
with contextlib.redirect_stdout(io.StringIO()):
    import time_common as tc
D = tc.D.copy()
f2s, _ = stone_map(); o2s = {k.split('.')[0]: v for k, v in f2s.items()}
D['stone'] = [o2s.get(str(i), str(i)) for i in D.index]
D['full'] = D.faces.map(lambda fs: '|'.join(sorted('-'.join(f) for f in fs)))
say(f'dated rows {len(D)}, distinct objects {D.index.nunique()}, stones {D.stone.nunique()}: rows are objects (fault 1 absent)')
S = D[D.seal].copy()
S['nm'] = S.name.apply(lambda n: [a for a in n if a != '000'])
S['fishcrest'] = S.nm.apply(lambda n: float(len(n) > 0 and n[0] in tc.MARKED)).where(S.nm.str.len() > 0)
E = S[S.ending != 'none'].copy(); E['agent'] = (E.ending == 'jar+man').astype(float)
D['office'] = D.faces.apply(lambda fs: float(tc.has_seq(fs, ('920', '060', '741'))))

def both(df, col, label):
    o = tc.shuffle_trend(df, col)
    c = df.drop_duplicates('stone').drop_duplicates(['site', 'area', 'bin', 'full'])
    oc = tc.shuffle_trend(c, col)
    say(f'  {label}\n     as run: {tc.fmt_tr(o)}\n     clean ({len(df) - len(c)} rows dropped): {tc.fmt_tr(oc)}')
    return o, oc
r = {}
r['agent'] = both(E, 'agent', 'agent seals (jar + man) among seals with an ending')
r['fish'] = both(S, 'fishcrest', 'fish crest first in the name (seals)')
r['office'] = both(D, 'office', 'office opening 920-060-741 (all objects)')
H = S[S.site == 'Harappa'].copy()
AB = pd.read_csv(f'{ROOT}/work_data/animal/animal_base.csv', dtype=str).fillna('').drop_duplicates('obj').set_index('obj')
H['noanimal'] = [float(AB.animal.get(str(i), '') == 'NONE') if AB.animal.get(str(i), '') != '' else np.nan for i in H.index]
r['harappa_noanimal'] = both(H, 'noanimal', 'Harappa seals with no animal')

say('\nearliest level (Mohenjo-daro DK-G): fish crest first, clean count (no lost sign before it)')
say('  as reported: first catalogue 0 of 36, second catalogue 0 of 36, union 0 of 38 (the union adds 2 second-catalogue stones that')
say('  matched no first-catalogue stone, so no stone is counted twice); later levels 62 of 592 / 65 of 590 / 65 of 627 (work_data/early/log_1.txt).')
for lab, a, n, b, m in (('first catalogue alone', 0, 36, 62, 592), ('union', 0, 38, 65, 627)):
    p = fisher_exact([[a, n - a], [b, m - b]])[1]
    say(f'  {lab}: {a} of {n} against {b} of {m} ({b / m:.1%}), two-sided Fisher P {p:.4f}')
import json
json.dump({k: [{kk: (vv if not isinstance(vv, tuple) else list(vv)) for kk, vv in (x or {}).items()} for x in v] for k, v in r.items()},
          open(f'{OUT}/r10.json', 'w'), default=float, indent=1)
