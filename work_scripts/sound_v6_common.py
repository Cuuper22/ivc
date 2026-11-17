#!/usr/bin/env python3
"""Shared kit for the sixth sound pass (sound_v6_*.py): the fifth-pass kit plus the PICTURE table.
Every Lipi object whose picture side (or picture beside the text) is known gets a picture label:
 - copper tablets (ctab): the picture of its SET (copper tablets with the same text), read by eye from the photos
   (sound_v6_sets.py lists the sets; the photo check is in jobs/out/sound_list_v6.md); a set's picture is applied to
   every copy, because the catalogue code is often vague ('Othr') or blank on copies of the same set;
 - moulded / incised tablets (mtab), seals, tags and the rest: the catalogue picture code (part before ':').
Picture labels in plain words are in PIC_EN.  Import: from sound_v6_common import *"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound_v5_common import *
OUT6 = f'{ROOT}/work_data/sound_v6'
os.makedirs(OUT6, exist_ok=True)
PIC_EN = {'Elep': 'elephant', 'Hare': 'hare', 'Tigr': 'tiger', 'Rhin': 'rhinoceros', 'Buff': 'water buffalo', 'Gaur': 'gaur (wild ox)',
          'Bull1': 'unicorn', 'Bull': 'short-horned bull', 'Bull2': 'bull (second kind)', 'Bull3': 'bull (third kind)', 'Zebu': 'zebu (humped bull)',
          'Goat': 'goat / markhor (marked body, with trough)', 'Comp': 'composite / spotted beast', 'Stag': 'branch-horned beast with trough (stag; the deer sign 341 stands in for it)',
          'Archer': 'horned figure with a bow (catalogue Anth)', 'Anth': 'human figure', 'Knot': 'endless knot (catalogue Loop)', 'Loop': 'endless knot',
          'Gavi': 'gharial / crocodile', 'Phyt': 'plant', 'Fish': 'fish', 'Mult': 'several figures', 'Scene': 'scene with figures', 'Bult': 'dotted circles / bullet motif (code Bult)',
          'Cros': 'cross', 'Xcrs': 'hatched cross', 'Pipal': 'pipal leaf', 'S590': 'box sign as picture', 'CompBull': 'composite bull', 'Swas': 'swastika', 'Maze': 'maze',
          'Tri4': 'four triangles', 'Xhch': 'hatched X', 'Crs': 'cross', 'Htgr': 'horned tiger', 'Bird': 'bird', 'Turt': 'turtle'}
# copper-tablet sets: text (reading order) -> picture, by eye (photos checked: see report)
CTAB_SET = {
 '503-615-752-740': 'Stag', '503-615-740': 'Stag', '503-752-000-740': 'Stag',
 '235-705-033-845-407-321-407': 'Hare',
 '806-845-061-407-850-900-740': 'Archer', '806-845-407-850-900-740': 'Archer', '000-000-000-407-000-900-740': 'Archer',
 '231-017-585-095-520-032-407': 'Goat', '220-017-585-095-520-032-408': 'Goat',
 '003-421-176-100-740-790': 'Goat', '003-422-176-100-740': 'Goat', '003-000-176-000-740-790': 'Goat', '003-421-176-000': 'Goat',
 '706-033-923-740': 'Elep', '706-033-923-740-001': 'Elep', '705-033-923-740-001': 'Elep',
 '798-240-845-061-407': 'Tigr', '000-000-845-061-407': 'Tigr',
 '905-032-597-142-617': 'Comp', '904-032-597-142-617': 'Comp', '905-032-597-142-000': 'Comp', '017-585-388-740': 'Comp',
 '806-235-233-705-033-585-407': 'Comp', '003-233-100-740': 'Comp', '032-220-773-740': 'Comp',
 '235-233-222-740': 'Rhin', '235-220-222-740': 'Rhin', '503-615-740x': 'Rhin',
 '255-435-690-740-900-003-422': 'Buff', '255-435-690-740-900-001-003-424': 'Buff', '255-435-690-740-900-001-003-423': 'Buff', '255-435-690-740-000': 'Buff', '000-690-740-900-000': 'Buff',
 '415-220-845-407': 'Knot',
 '032-071-407': 'Gaur', '615-343-595': 'Gaur',
 '744-760-095-595-001-142-617': 'Bull1', '747-717-095-595-001-142-617': 'Bull1', '747-717-142-595-001': 'Bull1',
}
NOPIC = {'', '-', 'Othr', 'Unknown', '?', 'None', 'X', 'T', 'Strokes', 'Box', 'T-A-T', 'Hgls'}


def picture_of(o):
    """picture label of one Lipi object (row of objs) or None."""
    if o.kind == 'ctab':
        main = max(('-'.join(x) for x in o.faces), key=len)
        return CTAB_SET.get(main)
    c = str(o.symbol).split(':')[0].split('+')[0]
    if c in NOPIC: return None
    return 'Knot' if c == 'Loop' else c


# the copper tablets whose second face is one big sign (or two) in place of a picture: no picture label for them
CT_PICSIGN = {}
for o in objs[objs.kind == 'ctab'].itertuples():
    fs = ['-'.join(x) for x in o.faces]
    if len(fs) == 2:
        a, b = sorted(fs, key=len)
        if len(a.split('-')) <= 2: CT_PICSIGN[o.Index] = (a, b)
objs['pic'] = [None if o.Index in CT_PICSIGN else picture_of(o) for o in objs.itertuples()]


def units(kinds=None):
    """one unit per distinct (site, kind, text) carrying a picture; copies of one text with one picture count once.
    Returns list of (stratum = site|kind, picture, set of signs, text)."""
    seen = set(); out = []
    for o in objs[objs.pic.notna()].itertuples():
        if kinds and o.kind not in kinds: continue
        txt = max(('-'.join(x) for x in o.faces), key=len)
        key = (o.site, o.kind, txt, o.pic)
        if key in seen: continue
        seen.add(key)
        sg = set(a for x in o.faces for a in x if a not in ('000', 'ALT') and a not in VAL)
        if sg: out.append((f'{o.site}|{o.kind}', o.pic, sg, txt))
    return out
