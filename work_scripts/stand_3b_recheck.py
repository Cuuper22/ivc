#!/usr/bin/env python3
"""Step 2b-check: rerun the old 'same room shares the letter 38.1% against 17.2%' (animal_4_pairs.py) with the
letters dealt ONLY among unicorn seals that carry a letter.

Why: the old script dealt the letter column among ALL beast seals of a stratum (non-unicorns carry a blank there), so
a dealt pair of letter seals often received blanks; that lowers the chance figure below the true letter-mix chance.
Second fix: the old table had one row per FACE, so two faces of one stone made a pair that always shares.
PREDICTION (fixed first): with the proper deal the chance rises to about 28% and the room excess shrinks; if the
real share stays near 38% the room effect stands (ratio about 1.35), if it is near 30% it was the null.
"""
import sys; sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from animal_common import *
rng = np.random.default_rng(5)
d = b[(b.g == 'UNI') & b.stand_sfx.isin(['W', 'J', 'S', 'I', 'L'])].copy().reset_index(drop=True)
print('faces', len(d), 'objects', d.obj.nunique())
FACES = d.copy()
d = d.drop_duplicates('obj').reset_index(drop=True)   # one row per stone: two faces of one stone are not a pair
d['szb'] = pd.qcut(d.face.fillna(d.face.median()), 3, labels=False).astype(str)
lab = pd.Categorical(d.stand_sfx).codes
def pairs(key):
    P = []
    for v, ix in d.groupby(key).groups.items():
        if v == '' or len(ix) > 40: continue
        ix = list(ix); P += [(i, j) for a, i in enumerate(ix) for j in ix[a + 1:]]
    return np.array(P)
d['house'] = np.where(d['block-house'].isin(['--', '-', '']), '', d.site + '|' + d['area-section'] + '|' + d['block-house'])
for strat_name, sk in [('site', d.site2), ('site x shape x size third (old strata)', d.site2 + '|' + d['shape'] + '|' + d.szb)]:
    st = strata_idx(sk.values)
    for key in ['room_key', 'house']:
        P = pairs(key); obs = (lab[P[:, 0]] == lab[P[:, 1]]).mean(); null = []
        for _ in range(2000):
            p = lab.copy()
            for ix in st: p[ix] = lab[rng.permutation(ix)]
            null.append((p[P[:, 0]] == p[P[:, 1]]).mean())
        null = np.array(null)
        print(f'{key:9s} strata {strat_name:40s} pairs {len(P)} same {obs*100:.1f}% chance {null.mean()*100:.1f}% ratio {obs/null.mean():.2f} P {(1+(null>=obs).sum())/2001:.4f}', flush=True)
# the old null, reproduced: letter column dealt among all beast seals
d2 = b[(b.g != '') & (b.g != 'NONE')].copy().reset_index(drop=True)
d2['L'] = np.where((d2.g == 'UNI') & (d2.stand_sfx != ''), d2.stand_sfx, '')
d2['szb'] = pd.qcut(d2.face.fillna(d2.face.median()), 3, labels=False).astype(str)
st = strata_idx((d2.site2 + '|' + d2['shape'] + '|' + d2.szb).values)
lab2 = pd.Categorical(d2.L.where(d2.L != '', '~')).codes; ok = (d2.L != '').values
P = []
for v, ix in d2.groupby('room_key').groups.items():
    if v == '' or len(ix) > 40: continue
    ix = list(ix); P += [(i, j) for a, i in enumerate(ix) for j in ix[a + 1:]]
P = np.array(P); P = P[ok[P[:, 0]] & ok[P[:, 1]]]
obs = (lab2[P[:, 0]] == lab2[P[:, 1]]).mean(); null = []
for _ in range(1000):
    p = lab2.copy()
    for ix in st: p[ix] = lab2[rng.permutation(ix)]
    null.append((p[P[:, 0]] == p[P[:, 1]]).mean())
print(f'OLD NULL reproduced: pairs {len(P)} same {obs*100:.1f}% chance {np.mean(null)*100:.1f}%')
