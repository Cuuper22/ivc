#!/usr/bin/env python3
"""JOB 4: draw 30 restorations (top candidate p >= 0.5, restorations_v2.csv) that have a photo, by seed 4.
Photo match: catalogue cisi number + '_' at the start of the file name (first match, side A preferred).
Writes work_data/frame/photo_check_draw.csv and resized copies to /tmp/frame2_photos/ for looking (outside the repo)."""
import os, re, pandas as pd, numpy as np
from PIL import Image
ROOT = '/home/claude/ivc'
P = f'{ROOT}/evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images/'
files = sorted(os.listdir(P))
L = pd.read_csv(f'{ROOT}/work_data/frame/restorations_v2.csv', dtype=str)
L['p1f'] = L.p1.astype(float)
H = L[L.p1f >= 0.5].copy()


def photo(c):
    if not isinstance(c, str) or c in ('-', ''): return ''
    m = [f for f in files if re.match(re.escape(c) + r'_[aA](\.|_)', f)] or [f for f in files if f.startswith(c + '_') or f.startswith(c + '.')]
    return m[0] if m else ''


H['photo'] = H.cisi.map(photo)
W = H[H.photo != '']
print(f'restorations with p1 >= 0.5: {len(H)}; with a photo: {len(W)}')
S = W.sample(n=min(30, len(W)), random_state=4).reset_index(drop=True)
os.makedirs('/tmp/frame2_photos', exist_ok=True)
for i, r in S.iterrows():
    im = Image.open(P + r.photo).convert('RGB'); im.thumbnail((900, 900)); im.save(f'/tmp/frame2_photos/{i:02d}_{r.cisi}.jpg', quality=88)
S.drop(columns=['p1f']).to_csv(f'{ROOT}/work_data/frame/photo_check_draw.csv', index=False)
print(S[['cisi', 'site', 'object_kind', 'signs', 'position', 'cand1', 'p1', 'cand2', 'p2', 'photo']].to_string())
