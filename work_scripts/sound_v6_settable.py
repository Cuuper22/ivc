#!/usr/bin/env python3
"""Copper-tablet sets of Mohenjo-daro under the sixth list: text, picture (set picture read from the photos, or the
single sign that stands on the picture side), copies, sounds, word glosses, and whether the set reads whole (strict / wide).
Writes work_data/sound_v6/ctab_sets_read.csv."""
from sound_v6_common import *
from sound_v6_values import V6, TIER6, STRICT6
O = objs[objs.kind == 'ctab'].copy()
O['main'] = O.faces.apply(lambda fs: max(('-'.join(x) for x in fs), key=len))
O['picsign'] = [CT_PICSIGN.get(i, ('', ''))[0] for i in O.index]
rows = []
for t, g in O.groupby('main'):
    x = t.split('-')
    pics = collections.Counter(p for p in g.pic if p); ps = collections.Counter(p for p in g.picsign if p)
    rows.append(dict(text=t, copies=len(g), picture=CTAB_SET.get(t, ''), picture_en=PIC_EN.get(CTAB_SET.get(t, ''), ''), catalogue_codes=dict(collections.Counter(g.symbol)),
                     picture_side_sign=dict(ps), cisi=' '.join(c for c in g.cisi if c != '-'),
                     sound=' '.join(V6[a][0] if a in V6 else f'[{a}]' for a in x),
                     words=' · '.join(f'{a} {V6[a][1].split(" (")[0]}' if a in V6 else f'{a} ?' for a in x),
                     strict=readable(tuple(x), STRICT6), wide=readable(tuple(x), TIER6)))
R = pd.DataFrame(rows).sort_values('copies', ascending=False)
R.to_csv(f'{OUT6}/ctab_sets_read.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 90)
print(R[R.copies >= 2][['text', 'copies', 'picture', 'picture_side_sign', 'sound', 'strict', 'wide']].to_string(index=False))
print('sets of 2+ reading whole: strict', int(R[R.copies >= 2].strict.sum()), 'wide', int(R[R.copies >= 2].wide.sum()), 'of', int((R.copies >= 2).sum()))
