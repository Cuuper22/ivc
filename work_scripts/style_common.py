#!/usr/bin/env python3
"""Shared kit for the STYLE job (a photo-made cutting-style code for seals). Written 2026-11-17.

Plain words:
- STYLE CODE: a short list of drawing habits read off a seal photo (neck, shoulder, horn, eye, ...), each with 2 to 4
  values. Fixed in FEATURES below BEFORE any stone of the sample was coded. '?' = cannot be read on the photo.
- Neutral number: a contact-sheet label like N017. The key (number -> catalogue id) lives in work_data/style/key_*.csv
  and is not opened until all coding of that sheet set is written down.
- One row per physical object (catalogue 'obj'); the face shown is the front face photo.

FEATURES (fixed first; unicorn seals; values in order):
  neck      : plain | folds (many thin parallel ridges across throat and neck) | bands (2-4 broad collar bands)
  shoulder  : plain | outlined (double line round shoulder / chest, the 'saddle') | heart (heart-shaped shoulder mark)
  horn      : single (one smooth curve) | double (S-curve or forward hook at tip) | ribbed (cross ribs along horn)
  eye       : dot | almond (long eye with lids) | ringed (round eye with a ring)
  tail      : down (hangs) | up (curves up or out) | tuft (marked tuft at end)
  hoof      : plain (leg ends plain) | marked (hoof split, cut line or knob at foot)
  stand_top : cage (tall box with ribs / grid) | box (small low box) | round (dome, globe, peak, crescent) | none
  stand_bowl: plain (plain cup or basin) | patterned (rays, fringe, hatching, lobes) | box (a second box below)
  shaft     : plain (single post) | marked (knobs, ribs, double line)
  sign_cut  : thin (fine narrow strokes) | broad (wide rounded strokes) | drilled (round drilled ends on strokes)
  frame     : yes (border line round the field) | no
  spacing   : tight (text touches or nearly touches the animal's back / horn) | gap (clear band between text and back)
Other-animal sheet uses neck, shoulder, eye, sign_cut, frame, spacing only.
"""
import sys, os, re, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from PIL import Image, ImageDraw, ImageFont
ROOT = '/home/antigravity/Cuuper22/ivc'
OUT = f'{ROOT}/work_data/style'; os.makedirs(OUT, exist_ok=True)
IMG = f'{ROOT}/evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images'
FILES = set(os.listdir(IMG))
FEATURES = {
    'neck': ['plain', 'folds', 'bands'], 'shoulder': ['plain', 'outlined', 'heart'],
    'horn': ['single', 'double', 'ribbed'], 'eye': ['dot', 'almond', 'ringed'],
    'tail': ['down', 'up', 'tuft'], 'hoof': ['plain', 'marked'],
    'stand_top': ['cage', 'box', 'round', 'none'], 'stand_bowl': ['plain', 'patterned', 'box'],
    'shaft': ['plain', 'marked'], 'sign_cut': ['thin', 'broad', 'drilled'],
    'frame': ['yes', 'no'], 'spacing': ['tight', 'gap']}
CITY6 = {'Mohenjo-daro': 'MD', 'Harappa': 'HA', 'Lothal': 'LO', 'Kalibangan': 'KA', 'Chanhu-daro': 'CH'}

def pick_photo(photos):
    fs = [f for f in str(photos).split() if f in FILES]
    if not fs: return ''
    pref = [f for f in fs if re.search(r'_A(_|\.|$)', f)] or [f for f in fs if re.search(r'_a(_|\.|$)', f)] or fs
    return pref[0]

def objects():
    """One row per physical object, with the front-face photo."""
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()):
        from stand_common import stand_seals
    S = stand_seals()
    S['photo'] = S.photos.map(pick_photo)
    S = S.sort_values(['obj', 'face'])
    O = S.groupby('obj').agg({c: 'first' for c in S.columns if c not in ('obj',)}).reset_index()
    ph = S[S.photo != ''].groupby('obj').photo.first()
    O['photo'] = O.obj.map(ph).fillna('')
    O['city'] = O.site.map(CITY6).fillna('OT')
    return O

def font(sz=22):
    p = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
    return ImageFont.truetype(p, sz) if os.path.exists(p) else ImageFont.load_default()

def crop_caption(p):
    """Cut away the printed catalogue caption (e.g. 'H-69 a') under the seal, so the sheet stays blind.
    Keep the longest run of rows where at least 25% of pixels are not near-white; then trim near-white columns."""
    a = np.asarray(p.convert('L')).astype(float)
    dark = (a < 200).mean(1) > 0.25
    best = (0, 0); st = None
    for i, d in enumerate(list(dark) + [False]):
        if d and st is None: st = i
        if not d and st is not None:
            if i - st > best[1] - best[0]: best = (st, i)
            st = None
    if best[1] - best[0] < a.shape[0] * 0.3: return p
    a2 = a[best[0]:best[1]]; cols = np.where((a2 < 200).mean(0) > 0.25)[0]
    x0, x1 = (cols.min(), cols.max() + 1) if len(cols) else (0, a.shape[1])
    return p.crop((x0, best[0], x1, best[1]))

def sheet(items, path, cols=4, W=390, H=390, label_h=30, q=68):
    rows = (len(items) + cols - 1) // cols
    im = Image.new('RGB', (cols * (W + 8), rows * (H + label_h)), 'white'); dr = ImageDraw.Draw(im); f = font()
    for k, (lab, fn) in enumerate(items):
        x = (k % cols) * (W + 8); y = (k // cols) * (H + label_h)
        dr.text((x + 4, y + 2), lab, fill='red', font=f)
        if fn:
            p = crop_caption(Image.open(f'{IMG}/{fn}').convert('RGB')); p.thumbnail((W, H), Image.LANCZOS)
            if p.size[0] < W * 0.8 and p.size[1] < H * 0.8:
                s = min(W / p.size[0], H / p.size[1]); p = p.resize((int(p.size[0] * s), int(p.size[1] * s)), Image.LANCZOS)
            im.paste(p, (x, y + label_h))
    im.save(path, quality=q); return path
