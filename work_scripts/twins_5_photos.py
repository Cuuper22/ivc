#!/usr/bin/env python3
"""TWINS step 5 (photo part): picture sheets of 30 twin pairs, both stones side by side, for looking by eye.
Written 2026-11-17. Pairs chosen: every twin pair where both stones have a photo, longest texts first (long texts are
the ones that cannot be chance), then by kind so every kind is in; at most 2 pairs per twin set.
For each pair the looker records: same hand (cutting style of the signs alike: stroke width, sign proportions, spacing)
or different hand; same layout (signs placed the same over the animal / in the field) or different; anything worn,
recut or unfinished. Sheets: work_data/twins/photo_sheet_*.jpg; pair list: photo_pairs.csv.
Prediction: most twin pairs from different cities are different hands with different layouts (separate stones cut
by separate carvers from one text); pairs from one building can be the same hand.
"""
from twins_common import *
from PIL import Image, ImageDraw
import itertools
P = pd.read_csv(f'{OUT}/pairs.csv', dtype=str).fillna('')
S = pd.read_csv(f'{OUT}/seals.csv', dtype=str).fillna('')
ph = dict(zip(S.cisi, S.photos))
def pick_photo(c):
    fs = [f for f in ph.get(c, '').split() if f]
    if not fs: return ''
    pref = [f for f in fs if re.search(r'_A(_|\.|$)', f)] or [f for f in fs if '_a' in f.lower()] or fs
    return pref[0]
P['pa'] = P.cisi_a.map(pick_photo); P['pb'] = P.cisi_b.map(pick_photo)
Q = P[(P.pa != '') & (P.pb != '')].copy(); Q['n'] = Q.n_a.astype(int)
Q = Q.sort_values(['n', 'signs_a'], ascending=[False, True])
chosen = []; per = collections.Counter() if False else {}
import collections
per = collections.Counter()
for r in Q.itertuples():
    if per[r.signs_a] >= 2: continue
    chosen.append(r); per[r.signs_a] += 1
    if len(chosen) >= 30: break
C = pd.DataFrame([dict(pair=k + 1, signs=r.signs_a, kind=r.kind, a=r.cisi_a, b=r.cisi_b, site_a=r.site_a, site_b=r.site_b,
                       building_a=r.building_a, building_b=r.building_b, animal_a=r.animal_a, animal_b=r.animal_b,
                       stand_a=r.stand5_a, stand_b=r.stand5_b, photo_a=r.pa, photo_b=r.pb) for k, r in enumerate(chosen)])
C.to_csv(f'{OUT}/photo_pairs.csv', index=False)
log('t5', f'pairs with both photos {len(Q)}; chosen {len(C)}')
W = 300
for s in range(0, len(C), 5):
    part = C.iloc[s:s + 5]
    sheet = Image.new('RGB', (2 * W + 20, len(part) * (W + 30)), 'white'); dr = ImageDraw.Draw(sheet)
    for k, r in enumerate(part.itertuples()):
        y = k * (W + 30)
        dr.text((5, y + 2), f'pair {r.pair}: {r.signs}  |  {r.a} ({r.site_a}, {r.animal_a}{":"+r.stand_a if r.stand_a else ""})  vs  {r.b} ({r.site_b}, {r.animal_b}{":"+r.stand_b if r.stand_b else ""})', fill='black')
        for c, f in enumerate([r.photo_a, r.photo_b]):
            im = Image.open(f'{IMG}/{f}').convert('RGB'); im.thumbnail((W, W))
            sheet.paste(im, (c * (W + 20), y + 18))
    sheet.save(f'{OUT}/photo_sheet_{s//5+1}.jpg', quality=85)
print(C[['pair', 'signs', 'kind', 'a', 'b', 'site_a', 'site_b', 'animal_a', 'animal_b', 'stand_a', 'stand_b']].to_string(index=False))
