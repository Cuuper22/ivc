#!/usr/bin/env python3
"""Contact sheets of the 80 signs: Mahadevan glyph picture of each sign's crosswalk partner, labelled
'Lipi / Mahadevan'. Output: work_data/sound/sheet_1..4.png"""
import pandas as pd
from PIL import Image, ImageDraw
ROOT = '/home/claude/ivc'
d = pd.read_csv(f'{ROOT}/work_data/sound/top80.csv', dtype=str).fillna('')
T = 150
for k in range(4):
    sub = d.iloc[k * 20:(k + 1) * 20]
    im = Image.new('RGB', (5 * T, 4 * (T + 22)), 'white'); dr = ImageDraw.Draw(im)
    for j, (_, r) in enumerate(sub.iterrows()):
        x, y = (j % 5) * T, (j // 5) * (T + 22)
        try:
            g = Image.open(f'{ROOT}/work_data/mahadevan_glyphs/{r.mahadevan}.png').convert('RGBA').resize((T - 10, T - 10))
            bg = Image.new('RGBA', g.size, 'white'); bg.alpha_composite(g); im.paste(bg.convert('RGB'), (x + 5, y + 5))
        except Exception: pass
        dr.text((x + 5, y + T + 4), f"L{r['sign']} / M{r.mahadevan}", fill='black')
        dr.rectangle([x, y, x + T - 1, y + T + 21], outline='grey')
    im.save(f'{ROOT}/work_data/sound/sheet_{k + 1}.png')
print('sheets written')
