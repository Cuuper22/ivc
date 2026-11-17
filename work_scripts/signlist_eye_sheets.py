#!/usr/bin/env python3
"""Contact sheets for the eye check of drawing (c): every pair with 2+ evidence kinds or a firing swap (a) or a swap in
2+ frames, both signs drawn through their rank-1 Mahadevan glyph (work_data/mahadevan_glyphs/<n>.png). Pairs whose two Lipi
signs map to ONE Mahadevan glyph are marked 'one glyph' (the eye cannot separate them there).
Output: work_data/signlist/eye/sheet_NN.png and eye_pairs.csv (the list the sheets show, in order)."""
from PIL import Image, ImageDraw
from signlist_common import *
P = pd.read_csv(f'{OUT}/pairs.csv', dtype={'a': str, 'b': str})
X = crosswalk(); X = X.sort_values('share', ascending=False)
top = {}
for l, m in zip(X.lipi, X.mahadevan): top.setdefault(l, m)
C = P[(P.n_kinds >= 2) | P.a_fire | (P.swap_frames >= 2)].copy()
C = C.sort_values(['n_kinds', 'swap_frames'], ascending=False).reset_index(drop=True)
C['glyph_a'] = C.a.map(top).fillna(''); C['glyph_b'] = C.b.map(top).fillna('')
os.makedirs(f'{OUT}/eye', exist_ok=True)
C[['a', 'b', 'glyph_a', 'glyph_b', 'n_kinds', 'swap_frames', 'drawing']].to_csv(f'{OUT}/eye/eye_pairs.csv', index_label='row')
def g(m):
    p = f'{ROOT}/work_data/mahadevan_glyphs/{m}.png'
    if not m or not os.path.exists(p): return None
    im = Image.open(p).convert('RGBA'); bg = Image.new('RGBA', im.size, 'white'); bg.alpha_composite(im)
    return bg.convert('RGB').resize((90, 90))
per = 24; cols = 4; W = 230; H = 120
for s in range(0, len(C), per):
    sub = C.iloc[s:s + per]
    sheet = Image.new('RGB', (cols * W, ((len(sub) + cols - 1) // cols) * H), 'white'); d = ImageDraw.Draw(sheet)
    for i, r in enumerate(sub.itertuples()):
        x, y = (i % cols) * W, (i // cols) * H
        for j, (sg, m) in enumerate(((r.a, r.glyph_a), (r.b, r.glyph_b))):
            im = g(m)
            if im: sheet.paste(im, (x + 10 + j * 105, y + 22))
            else: d.text((x + 20 + j * 105, y + 60), 'no glyph', fill='red')
        tag = ' ONE GLYPH' if r.glyph_a and r.glyph_a == r.glyph_b else ''
        d.text((x + 5, y + 4), f'#{r.Index} {r.a}/{r.b} M{r.glyph_a}/M{r.glyph_b}{tag}', fill='black')
        d.rectangle([x, y, x + W - 1, y + H - 1], outline='grey')
    sheet.save(f'{OUT}/eye/sheet_{s // per:02d}.png')
print(len(C), 'pairs on', (len(C) + per - 1) // per, 'sheets')
