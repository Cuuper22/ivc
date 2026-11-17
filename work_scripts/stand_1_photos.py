#!/usr/bin/env python3
"""Step 1: photo check of the stand letters.
Draw 12 unicorn seals per letter (W J S I L) by seed 20261117 from seals with a photo and catalogue
condition not 'Poor' (so the stand can be seen). Shuffle all 60 together and lay them out on numbered
sheets with the letter HIDDEN; the key goes to stand_photo_key.csv. I describe each stand blind, then unblind.
Prediction written before looking: each letter is one stand shape; W = the tall cage/brazier-like stand
with a ribbed bowl, S/J/I/L are lesser variants; the catalogue lumps at least two kinds inside W.
"""
from stand_common import *
from PIL import Image, ImageDraw, ImageFont
S = stand_seals()
u = S[(S.animal == 'unicorn') & S.stand5.isin(L5) & (S.photos != '')].copy()
u['ph'] = u.photos.str.split(';').str[0].str.strip()
u = u[u.ph.map(lambda p: os.path.exists(f'{IMG}/{p}'))]
good = u[~u.condition.isin(['Poor'])]
rng = np.random.default_rng(20261117)
pick = []
for L in L5:
    pool = good[good.stand5 == L]
    if len(pool) < 12: pool = u[u.stand5 == L]
    pick.append(pool.iloc[rng.choice(len(pool), 12, replace=False)])
P = pd.concat(pick).sample(frac=1, random_state=7).reset_index(drop=True)
P['code'] = [f'P{i+1:02d}' for i in range(len(P))]
P[['code', 'cisi', 'site', 'stand5', 'cult', 'ph', 'condition', 'area_mm2', 'building']].to_csv(f'{OUT}/stand_photo_key.csv', index=False)
cell = 520
for s in range(0, len(P), 6):
    sheet = Image.new('RGB', (cell * 3, cell * 2), 'white'); d = ImageDraw.Draw(sheet)
    for j, (_, r) in enumerate(P.iloc[s:s + 6].iterrows()):
        im = Image.open(f'{IMG}/{r.ph}').convert('RGB'); im.thumbnail((cell - 10, cell - 30))
        x, y = (j % 3) * cell, (j // 3) * cell
        sheet.paste(im, (x + 5, y + 25)); d.text((x + 8, y + 5), r.code, fill='red')
    sheet.save(f'{OUT}/stand_sheet_{s//6+1:02d}.jpg', quality=88)
log('photos', len(P), 'seals on', (len(P) + 5) // 6, 'sheets; per letter', P.stand5.value_counts().to_dict())

# Close-up sheets: the stand sits under the head, at the right side of the field in these photos.
# Crop the right 48% of the width and 22%-86% of the height (caption strip excluded), enlarge, 12 per sheet.
cw, ch = 400, 400
for s in range(0, len(P), 12):
    sheet = Image.new('RGB', (cw * 4, ch * 3), 'white'); d = ImageDraw.Draw(sheet)
    for j, (_, r) in enumerate(P.iloc[s:s + 12].iterrows()):
        im = Image.open(f'{IMG}/{r.ph}').convert('L')
        W_, H_ = im.size
        cr = im.crop((int(W_ * 0.52), int(H_ * 0.22), W_, int(H_ * 0.86)))
        cr = cr.resize((int(cr.size[0] * (ch - 30) / cr.size[1]), ch - 30), Image.LANCZOS)
        x, y = (j % 4) * cw, (j // 4) * ch
        sheet.paste(cr, (x + 5, y + 25)); d.text((x + 8, y + 5), r.code, fill=0)
    sheet.save(f'{OUT}/stand_close_{s//12+1}.jpg', quality=90)
log('close-ups', (len(P) + 11) // 12, 'sheets')

# Whole-seal sheets enlarged (the bull: neck folds, collar, shoulder/saddle outline, horn), 12 per sheet, letters still hidden.
cw, ch = 400, 420
for s in range(0, len(P), 12):
    sheet = Image.new('L', (cw * 4, ch * 3), 255); d = ImageDraw.Draw(sheet)
    for j, (_, r) in enumerate(P.iloc[s:s + 12].iterrows()):
        im = Image.open(f'{IMG}/{r.ph}').convert('L'); W_, H_ = im.size
        im = im.crop((0, 0, W_, int(H_ * 0.86)))
        f = min((cw - 10) / im.size[0], (ch - 30) / im.size[1]); im = im.resize((int(im.size[0] * f), int(im.size[1] * f)), Image.LANCZOS)
        x, y = (j % 4) * cw, (j // 4) * ch
        sheet.paste(im, (x + 5, y + 25)); d.text((x + 8, y + 5), r.code, fill=0)
    sheet.save(f'{OUT}/stand_whole_{s//12+1}.jpg', quality=90)
