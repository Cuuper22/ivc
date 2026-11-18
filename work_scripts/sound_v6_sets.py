#!/usr/bin/env python3
"""Copper-tablet sets: Mohenjo-daro copper tablets grouped by the text on the text side (reading order),
with the catalogue picture code, the other face (when the picture side is a single big sign), and photo files.
Writes work_data/sound_v6/ctab_objects.csv and ctab_sets.csv."""
import os, collections, pandas as pd
ROOT = '/home/antigravity/Cuuper22/ivc'
IMG = f'{ROOT}/evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images'
files = os.listdir(IMG)
import sys; sys.path.insert(0, f'{ROOT}/work_scripts')
from gloss import load
d = load(); d['obj'] = d.id.str.split('.').str[0]
c = d[d.type == 'TAB:C']
rows = []
for o, g in c.groupby('obj', sort=False):
    faces = ['-'.join(x) for x in g.tok]
    # text side = longest face; picture-sign side = a one-sign face
    main = max(faces, key=lambda f: len(f))
    other = [f for f in faces if f != main]
    cisi = g.cisi.iloc[0]
    ph = sorted(f for f in files if cisi != '-' and f.startswith(cisi + '_'))
    rows.append(dict(obj=o, cisi=cisi, site=g.site.iloc[0], code=g.symbol.iloc[0], cult=g.cult.iloc[0], text=main,
                     other_face=' / '.join(other), complete=all(g.complete_txt), photos=' '.join(ph)))
O = pd.DataFrame(rows)
O.to_csv(f'{ROOT}/work_data/sound_v6/ctab_objects.csv', index=False)
S = O.groupby('text').agg(n=('obj', 'count'), cisi=('cisi', lambda s: ' '.join(s)), codes=('code', lambda s: dict(collections.Counter(s))),
                          other=('other_face', lambda s: dict(collections.Counter(s)))).sort_values('n', ascending=False)
S.to_csv(f'{ROOT}/work_data/sound_v6/ctab_sets.csv')
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 120)
print(S[S.n >= 2].to_string())
