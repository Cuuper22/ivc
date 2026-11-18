#!/usr/bin/env python3
"""Contact sheets of object photos for looking at the picture side by eye.
usage: python3 sound_v6_sheet.py OUT.jpg CISI_FILE_STEM [...]   (file stems as in the photo folder, e.g. M-552_B)"""
import sys, os
from PIL import Image, ImageDraw
IMG = '/home/antigravity/Cuuper22/ivc/evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images'
out, stems = sys.argv[1], sys.argv[2:]
H = 200; ims = []
for s in stems:
    f = next((os.path.join(IMG, x) for x in sorted(os.listdir(IMG)) if x.startswith(s + '.') or x == s), None)
    if not f: print('missing', s); continue
    i = Image.open(f).convert('RGB'); i = i.resize((max(1, int(i.width * H / i.height)), H)); ims.append((s, i))
cols = 4; W = 330
rows = (len(ims) + cols - 1) // cols
c = Image.new('RGB', (cols * W, rows * (H + 18)), 'white'); dr = ImageDraw.Draw(c)
for k, (s, i) in enumerate(ims):
    x, y = (k % cols) * W, (k // cols) * (H + 18)
    c.paste(i.crop((0, 0, min(i.width, W - 6), H)), (x, y + 16)); dr.text((x + 2, y + 2), s, fill='red')
c.save(out); print(out, c.size)
