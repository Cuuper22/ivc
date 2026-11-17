#!/usr/bin/env python3
"""Shared kit for the HANDS job (the seal cutters). Written 2026-11-17.
Photo naming rule (checked against the folder): a photo file is <object id>_<face letter>[_<scale or note>].jpg|png,
where the object id is the catalogue 'cisi' id (M-224 = Mohenjo-daro seal 224, H = Harappa, K = Kalibangan, L = Lothal,
C = Chanhu-daro, ...) and the face letter A/a is the front face (B, C ... other faces; T = tablet side). One seal can have
several files (several faces or scales); the table column 'photos' lists them. A seal "has a photo" when at least one of
its listed files exists in the folder."""
import sys, os, re, io, collections, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from PIL import Image, ImageDraw, ImageFont
ROOT = '/home/claude/ivc'
OUT = f'{ROOT}/work_data/hands'; os.makedirs(OUT, exist_ok=True)
IMG = f'{ROOT}/evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images'
FILES = set(os.listdir(IMG))

def pick_photo(photos):
    fs = [f for f in str(photos).split() if f in FILES]
    if not fs: return ''
    pref = [f for f in fs if re.search(r'_A(_|\.|$)', f)] or [f for f in fs if re.search(r'_a(_|\.|$)', f)] or fs
    return pref[0]

def load():
    S = pd.read_csv(f'{ROOT}/work_data/twins/seals.csv', dtype=str).fillna('')
    S['photo'] = S.photos.map(pick_photo)
    S['hmm_f'] = pd.to_numeric(S.hmm, errors='coerce'); S['vmm_f'] = pd.to_numeric(S.vmm, errors='coerce')
    return S

def font(sz=13):
    for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
        if os.path.exists(p): return ImageFont.truetype(p, sz)
    return ImageFont.load_default()

def sheet(items, path, cols=4, W=260, H=260, label_h=30, q=72):
    """items = list of (label, photo_file). Draw a grid with a label line over each photo."""
    rows = (len(items) + cols - 1) // cols
    im = Image.new('RGB', (cols * (W + 6), rows * (H + label_h)), 'white'); dr = ImageDraw.Draw(im); f = font(12)
    for k, (lab, fn) in enumerate(items):
        x = (k % cols) * (W + 6); y = (k // cols) * (H + label_h)
        dr.text((x + 2, y + 1), lab, fill='black', font=f)
        if fn:
            p = Image.open(f'{IMG}/{fn}').convert('RGB'); p.thumbnail((W, H)); im.paste(p, (x, y + label_h))
    im.save(path, quality=q); return path
