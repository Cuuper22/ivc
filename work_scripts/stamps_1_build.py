#!/usr/bin/env python3
"""STAMPS step 1: every impression and every seal in the first catalogue (Lipi), with findspot, date bin, animal, text,
text kind (frame v2) and photo files.  Written 2026-11-17 before any match was counted.

Plain words:
- SEAL: the stone (or other) stamp itself.  Catalogue type starting SEAL (SEAL, SEAL:S square, SEAL:R rectangular,
  SEAL:C circular, SEAL:CY cylinder, SEAL:L).
- IMPRESSION: clay pressed with a seal and left on goods.  Taken as:
    tier 'sealing'  : every catalogue row whose type starts TAG (plain TAG and the subtypes B, C, L, O, P, PC, R, W).
                      The catalogue has no legend; B = wooden box and O = cane packing are pinned by two Lothal anchors
                      (L-161..L-170 box sealings, L-146 cane-backed) found earlier (jobs/out/beads_cotton.md).
    tier 'stamped pot': POT:T:s rows (photos M-424, M-1376, H-692, M-422 show a framed seal impression on the pot).
    tier 'moulded tablet': TAB:B (bas-relief tablets made in a mould).  Kept as a separate tier: the impression of a
                      mould, not certainly of a seal.  Every headline number is given for the first two tiers.
- Findspot keys follow registry_build.py: building = site|area|block-house (or site|area|room-grid where there is no
  house); block = site|area|block number (or grid letters); room = building|room-grid.
- Date bin: work_data/time/time_axis.csv (early / middle / late).
Writes work_data/stamps/objects.csv (one row per face of a seal or impression).
"""
import sys, os, re, io, contextlib, glob, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
T0 = time.time()
def log(*a): print(f'[stamps_1 {time.time()-T0:6.1f}s]', *a, flush=True)
log('loading the catalogue (gloss parser) ...')
with contextlib.redirect_stdout(io.StringIO()):
    from sound_v4_common import d
import pandas as pd, numpy as np
ROOT = '/home/antigravity/Cuuper22/ivc'; OUT = f'{ROOT}/work_data/stamps'; os.makedirs(OUT, exist_ok=True)
IMG = f'{ROOT}/evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images'

def blank(v): return str(v).strip() in ('', '-', '--', '- -')
def clean(v): return '' if blank(v) else str(v).strip().strip('-').strip()
def ft(s):
    m = re.search(r'(-?\d+(\.\d+)?)\s*ft', str(s))
    if m: return abs(float(m.group(1)))
    m = re.search(r'(-?\d+(\.\d+)?)\s*cm', str(s))
    if m: return abs(float(m.group(1))) / 30.48
    m = re.search(r'(-?\d+(\.\d+)?)\s*m\b', str(s))
    if m: return abs(float(m.group(1))) * 3.281
    return np.nan

def tier(t):
    if t.startswith('SEAL'): return 'seal'
    if t.startswith('TAG'): return 'sealing'
    if t in ('POT:T:s', 'POT:T:S'): return 'stamped pot'   # POT:T:p dropped: photos (Sktd-4, H-1007) show painted or incised marks, not stamps
    if t == 'TAB:B': return 'moulded tablet'
    return ''

SPECIES = {'Bull1': 'unicorn', 'Gaur': 'short-horned bull', 'Zebu': 'zebu', 'Elep': 'elephant', 'Rhin': 'rhinoceros',
           'Tigr': 'tiger', 'Buff': 'buffalo', 'Goat': 'goat', 'Bull': 'bull'}
TA = pd.read_csv(f'{ROOT}/work_data/time/time_axis.csv', dtype=str).fillna('')
TBIN = dict(zip(TA.obj, TA.bin))
CJ = pd.read_csv(f'{ROOT}/work_data/frame/corpus_jobs.csv', dtype=str).fillna('').set_index('face')

log('indexing photos ...')
photos = {}
for f in os.listdir(IMG):
    m = re.match(r'^([A-Za-z]+-\d+)', f)
    if m: photos.setdefault(m.group(1), []).append(f)

rows = []
for _, r in d.iterrows():
    tr = tier(r.type)
    if not tr: continue
    x = list(r.tok)
    flg = r.flg
    sym = str(r.symbol).strip()
    sp = sym.split(':', 1) if sym not in ('', '-') else ['']
    animal = SPECIES.get(sp[0], sp[0]) if sp[0] else ''
    area, bh, rg = clean(r['area-section']), clean(r['block-house']), clean(r['room-grid'])
    site = r.site
    building = f'{site}|{area}|{bh}' if area and bh else (f'{site}|{area}|{rg}' if area and rg else '')
    if area and bh:
        m = re.match(r'^(\d+)', bh); block = f'{site}|{area}|blk{m.group(1)}' if m else f'{site}|{area}|{bh}'
    elif area and rg:
        m = re.match(r'^-?([A-Z]+)', rg); block = f'{site}|{area}|{m.group(1)}' if m else f'{site}|{area}|{rg}'
    else: block = ''
    room = f'{building}|{rg}' if building and rg and rg != building.split('|')[-1] else ''
    cj = CJ.loc[r.id] if r.id in CJ.index else None
    cis = str(r.cisi).strip()
    rows.append(dict(face=r.id, obj=r.obj, cisi=cis, type=r.type, tier=tr, site=site, area=area, house=bh, roomgrid=rg,
                     area_key=f'{site}|{area}' if area else '', building=building, block=block, room=room,
                     depth_ft=ft(r.depth), bin=TBIN.get(r.obj, ''), animal=animal, stand=sp[1] if len(sp) > 1 else '',
                     material=r.material, shape=r.shape, sides=r.sides, hmm=r['horizontal(mm)'], vmm=r['vertical(mm)'],
                     signs='-'.join(x), n=len(x), lost=sum(s in ('000', 'ALT') for s in x),
                     broken=bool(flg & {'broken'}) if isinstance(flg, (set, frozenset)) else ('broken' in str(flg)),
                     text_kind=cj.text_kind if cj is not None else '', v2=cj.v2_classes if cj is not None else '',
                     restored=cj.restored_signs if cj is not None else '',
                     photos=' '.join(sorted(photos.get(cis, []))) if cis not in ('', '-') else ''))
O = pd.DataFrame(rows)
O.to_csv(f'{OUT}/objects.csv', index=False)
log(f'wrote objects.csv: {len(O)} faces')
print(O.groupby('tier').agg(faces=('face', 'size'), objects=('obj', 'nunique'), with_photo=('photos', lambda s: (s != '').sum())).to_string())
print(pd.crosstab(O[O.tier != 'seal'].type, O[O.tier != 'seal'].photos != '').to_string())
