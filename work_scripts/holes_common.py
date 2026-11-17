#!/usr/bin/env python3
"""Shared kit for the eight-signs job (holes_*.py).  Uses long_common.build_objects (Lipi table, reading order) and
the Mahadevan second catalogue through the crosswalk.  A 'line' = one line of one face of one object, in reading order."""
import sys, os, collections, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pandas as pd
import long_common as LC
from long_common import build_objects, SH, snd, gloss_en, CNT
ROOT = '/home/claude/ivc'
HOLES = f'{ROOT}/work_data/holes'
os.makedirs(HOLES, exist_ok=True)
EIGHT = ['060', '335', '711', '525', '692', '842', '611', '645']
_O = None


def objs():
    global _O
    if _O is None: _O = build_objects()
    return _O


def lines(distinct=True):
    """list of dict(obj,cisi,site,type,area,animal,material,face,line,toks,nlines,fid). distinct: drop exact-copy objects."""
    seen = set(); out = []
    for o, ob in objs().items():
        if distinct:
            sig = LC.obj_signature(ob)
            if sig in seen: continue
            seen.add(sig)
        for fi, f in enumerate(ob['faces']):
            for li, l in enumerate(f['lines']):
                out.append(dict(obj=o, cisi=ob['cisi'], site=ob['site'], type=ob['type'], area=ob['area'], block=ob['block'],
                                animal=ob['animal'], material=ob['material'], face=fi + 1, line=li + 1, toks=tuple(l),
                                nfaces=len(ob['faces']), ftype=f['face_type']))
    return out


def kind(t):
    return (t or '').split(':')[0]


def uses(sign, ls):
    """each occurrence: (line index, position)"""
    r = []
    for i, L in enumerate(ls):
        for p, s in enumerate(L['toks']):
            if s == sign: r.append((i, p))
    return r


def mah_lines():
    sys.path.insert(0, ROOT + '/work_scripts')
    import mah_common as M
    return M.load_mah().to_dict('records')
