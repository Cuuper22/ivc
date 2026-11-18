#!/usr/bin/env python3
"""COPPER step 0: photo contact sheets for the lead's own eye check of copper-tablet picture sides.
Sample (fixed before looking): up to 2 objects per distinct text among tablets whose first-catalogue picture code is
vague (Othr / blank / '-'), then 1 per text among tablets with a specific code, to check the code. 48 objects.
Each sheet row = one object, all its photos, labelled with CISI number. Writes work_data/copper/sheets/sheet_NN.jpg."""
import sys; sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from copper_common import *
from PIL import Image, ImageDraw
L = load_L(); L = L[(L.site == 'Mohenjo-daro') & (L.photos != '')]
vague = L[L.cat.isin(NOPIC)]; spec = L[~L.cat.isin(NOPIC)]
pick = []
for t, q in vague.groupby('text'): pick += list(q.cisi[:2])
pick = pick[:40]
for t, q in spec.groupby('text'):
    if len(pick) >= 48: break
    pick.append(q.cisi.iloc[0])
pick = list(dict.fromkeys(pick))
pd.DataFrame({'cisi': pick}).to_csv(f'{OUT}/photo_sample.csv', index=False)
H = 260; per = 4
for si in range(0, len(pick), per):
    rows = []
    for c in pick[si:si + per]:
        r = L[L.cisi == c].iloc[0]
        ims = []
        for f in r.photos.split('|'):
            im = Image.open(f'{IMG}/{f}').convert('RGB'); w = int(im.width * H / im.height); ims.append(im.resize((w, H)))
        W = sum(i.width for i in ims) + 10 * len(ims) + 330
        row = Image.new('RGB', (W, H + 10), 'white'); dr = ImageDraw.Draw(row)
        dr.text((5, 5), f'{c}', fill='black'); dr.text((5, 25), f'cat={r.cat_full}', fill='black'); dr.text((5, 45), r.text[:40], fill='black')
        dr.text((5, 65), f'2nd: {r.picsign} {r.second}'[:45], fill='black')
        x = 330
        for i in ims: row.paste(i, (x, 5)); x += i.width + 10
        rows.append(row)
    W = max(r.width for r in rows); S = Image.new('RGB', (W, sum(r.height for r in rows)), 'white'); y = 0
    for r in rows: S.paste(r, (0, y)); y += r.height
    S.save(f'{OUT}/sheets/sheet_{si // per:02d}.jpg', quality=85)
print(len(pick), 'objects;', (len(pick) + per - 1) // per, 'sheets')
