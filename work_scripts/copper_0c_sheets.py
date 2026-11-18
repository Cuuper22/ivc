#!/usr/bin/env python3
"""COPPER step 0c: third photo batch, targeted after step 1: copies in sets where a catalogue code disagreed or the
picture was not yet read (stag set, goat set, tiger set, composite sets, archer set, buffalo set, hare set), and the
copies said to carry one sign on the picture face. Writes sheets/b3_NN.jpg and photo_sample3.csv."""
import sys; sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from copper_common import *
from PIL import Image, ImageDraw
L = load_L(); L = L[(L.site == 'Mohenjo-daro')]
pick = ['M-553', 'M-556', 'M-559', 'M-562', 'M-1503', 'M-1508', 'M-548', 'M-1555', 'M-1557', 'M-1476', 'M-569', 'M-1515',
        'M-1517', 'M-1534', 'M-1528', 'M-1530', 'M-602', 'M-603', 'M-1563', 'M-1550', 'M-534', 'M-535', 'M-1491']
pick = [p for p in pick if (L.cisi == p).any() and L[L.cisi == p].photos.iloc[0]]
pd.DataFrame({'cisi': pick}).to_csv(f'{OUT}/photo_sample3.csv', index=False)
H = 230; per = 4
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
    S.save(f'{OUT}/sheets/b3_{si // per:02d}.jpg', quality=85)
print(len(pick), pick)
