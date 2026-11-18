#!/usr/bin/env python3
"""COPPER step 0b: second photo batch. The first sample (copper_0_sheets.py) was cut at 40 vague objects in text order
and so missed the texts late in the sort (the big stag set among them). Batch 2: up to 2 objects per distinct text not
yet looked at, any catalogue code, texts with most copies first. Writes sheets/b2_NN.jpg and photo_sample2.csv."""
import sys; sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from copper_common import *
from PIL import Image, ImageDraw
L = load_L(); L = L[(L.site == 'Mohenjo-daro')]
done = set(pd.read_csv(f'{OUT}/photo_sample.csv').cisi)
seen_txt = set(L[L.cisi.isin(done)].text)
P = L[(L.photos != '') & ~L.cisi.isin(done) & ~L.text.isin(seen_txt)]
order = P.text.value_counts().index
pick = []
for t in order:
    pick += list(P[P.text == t].cisi[:2])
pick = pick[:32]
pd.DataFrame({'cisi': pick}).to_csv(f'{OUT}/photo_sample2.csv', index=False)
H = 240; per = 4
for si in range(0, len(pick), per):
    rows = []
    for c in pick[si:si + per]:
        r = L[L.cisi == c].iloc[0]; ims = []
        for f in r.photos.split('|'):
            im = Image.open(f'{IMG}/{f}').convert('RGB'); w = int(im.width * H / im.height); ims.append(im.resize((w, H)))
        W = sum(i.width for i in ims) + 10 * len(ims) + 330
        row = Image.new('RGB', (W, H + 10), 'white'); dr = ImageDraw.Draw(row)
        dr.text((5, 5), c, fill='black'); dr.text((5, 25), f'cat={r.cat_full}', fill='black'); dr.text((5, 45), r.text[:40], fill='black')
        dr.text((5, 65), f'2nd: {r.picsign} {r.second}'[:45], fill='black')
        x = 330
        for i in ims: row.paste(i, (x, 5)); x += i.width + 10
        rows.append(row)
    W = max(r.width for r in rows); S = Image.new('RGB', (W, sum(r.height for r in rows)), 'white'); y = 0
    for r in rows: S.paste(r, (0, y)); y += r.height
    S.save(f'{OUT}/sheets/b2_{si // per:02d}.jpg', quality=85)
print(len(pick), pick)
