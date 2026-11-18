#!/usr/bin/env python3
"""Shared kit for the CHITS job (chits_*.py): the people of the tablets.  Written 2026-11-17 before any chits number.

Plain words:
- OBJECT: one inscribed thing of the first catalogue (Lipi); FACE: one inscribed side, signs in reading order.
- KIND: seal, mtab (clay / faience tablet), ctab (copper tablet), tag (sealing / tag), pot, rod, other.
- JAR ENDING: a face whose last jar sign (740) is followed by nothing or by 1+ more signs.  The sign right after the
  jar is the AFTER-JAR SIGN ('' when the jar ends the face).  Frame-v2 class TITLE holds the after-jar title signs:
  comb 400, man 090, hatched box 527, barred tall rectangle 621, X-with-table 679, closed X 565, porter-with-diamond 161,
  caged fish 241 and single-use 170, 224, 481, 622, 686, 932.
- NAME: the signs before that jar, with any leading front word / after-front slot (frame-v2 OPEN, SLOT) taken off.
  CREST: the first sign of the name.  A name with a lost sign (000) is flagged 'lost'.
- FACE TYPE (as in spots_3_records.py): name (has a name job), amount (only counts and measure signs, with a count or
  cup), thing (other word-signs), lost.
- AMOUNT of a face, read with no word: for each unit sign the count run next to it (before it; if none, after it):
  cups (700), big measure (705/706), tree signs (390/405/406/407), porter (156), load-carrier (154/158).
- SEAL SIZE RESIDUAL: log face area minus the median of complete seals of the same site, length and format
  (size_common.cell_medians); 0 = typical, -0.69 = half the face.
- BIN: early / middle / late from work_data/time/time_axis.csv; TIME: the catalogue period string (Harappa 3B, 3B/C, 3C...).
"""
import sys, os, io, contextlib, collections, re, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
with contextlib.redirect_stdout(io.StringIO()):
    from measures_common import objs, NUM, UNITS, runs, ROOT
ROOT = '/home/antigravity/Cuuper22/ivc'
OUT = f'{ROOT}/work_data/chits'; os.makedirs(OUT, exist_ok=True)
T0 = time.time()

C2 = pd.read_csv(f'{ROOT}/work_data/frame/classes_v2.csv', dtype=str).fillna('')
V2 = dict(zip(C2.sign, C2.v2_base))
TITLES = sorted(s for s, c in V2.items() if c == 'TITLE')
OPENSLOT = {s for s, c in V2.items() if c in ('OPEN', 'SLOT')}
TREES = {'390', '405', '406', '407'}
SHAPES = pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv', dtype=str).fillna('')
PIC = {k: (v.split(',')[0][:40] if v else f'sign {k}') for k, v in zip(SHAPES.lipi_wells_number, SHAPES.shape_description)}
PIC.update({'400': 'comb', '090': 'man', '740': 'jar', '700': 'cup', '705': 'big measure (U with stroke)', '156': 'porter with jars',
            '176': 'seated person with four ticks', '527': 'hatched box', '621': 'barred tall rectangle', '679': 'X with table',
            '565': 'closed X', '161': 'porter with diamond', '241': 'caged whiskered fish'})
def pic(s): return PIC.get(s, f'sign {s}')

NAMEJOB = {'crest', 'poss', 'ending', 'opener', 'tag'}


def say_to(logf):
    def say(*a):
        s = ' '.join(str(x) for x in a); print(f'[{time.time() - T0:6.1f}s] {s}', flush=True); logf.write(s + '\n'); logf.flush()
    return say


def face_type(f, roles):
    t = list(f)
    if all(s == '000' for s in t): return 'lost'
    if NAMEJOB & set(roles): return 'name'
    core = [s for s in t if s != '000']
    if core and all((s in NUM or s in UNITS) for s in core) and any((s in NUM or s == '700') for s in core): return 'amount'
    return 'thing'


def jar_parse(f):
    """(name tuple, after-jar sign, rest after jar) for the LAST jar in the face, or None if no jar."""
    f = list(f)
    if '740' not in f: return None
    j = len(f) - 1 - f[::-1].index('740')
    pre = f[:j]
    while pre and pre[0] in OPENSLOT: pre = pre[1:]
    after = f[j + 1:]
    return tuple(pre), (after[0] if after else ''), tuple(after)


def ending_label(after):
    if after == '': return 'jar only'
    if after in TITLES: return after
    return 'other'


def amount_of(f):
    """dict unit -> value from the count run next to the unit sign (before it; else after it)."""
    f = list(f); out = {}
    R = runs(f)
    UN = {'700': 'cup', '705': 'big', '706': 'big', '390': 'tree', '405': 'tree', '406': 'tree', '407': 'tree',
          '156': 'porter', '154': 'carrier', '158': 'carrier'}
    for i, s in enumerate(f):
        if s not in UN: continue
        v = None
        for (a, b, val, ser) in R:
            if b == i: v = val
        if v is None:
            for (a, b, val, ser) in R:
                if a == i + 1: v = val
        out.setdefault(UN[s], v)
    return out


def load():
    """one row per object with faces, jar parses, face types, findspot, bin and sizes."""
    T = pd.read_csv(f'{ROOT}/work_data/time/time_axis.csv', dtype=str).fillna('').set_index('obj')
    rows = []
    for o, r in objs.iterrows():
        faces = [tuple(x) for x in r.faces]
        roles = [p['roles'] for p in r.parses]
        types = [face_type(f, ro) for f, ro in zip(faces, roles)]
        jp = [jar_parse(f) for f in faces]
        area = r.area if r.area not in ('--', '') else ''
        h = pd.to_numeric(r.h, errors='coerce'); v = pd.to_numeric(r.v, errors='coerce')
        rows.append(dict(obj=o, cisi=r.cisi, site=r.site, kind=r.kind, type=r.type, area=area, bh=r.bh if r.bh not in ('--',) else '',
                         dep=r.dep, animal=r.animal, nfaces=len(faces), faces=faces, types=types, jars=jp,
                         area_mm2=(h * v if (h > 0 and v > 0) else np.nan),
                         bin=T.bin.get(o, '') if o in T.index else '', time=T.time.get(o, '') if o in T.index else ''))
    O = pd.DataFrame(rows).set_index('obj', drop=False)
    O['sig'] = [' | '.join(sorted('-'.join(f) for f in fs)) for fs in O.faces]
    O['lostfree'] = [all('000' not in f for f in fs) for fs in O.faces]
    return O


def name_rows(O):
    """one row per face carrying a jar: obj, face index, name, crest, after-jar sign, ending, lost flag."""
    out = []
    for o, r in O.iterrows():
        for k, (f, jp) in enumerate(zip(r.faces, r.jars)):
            if jp is None: continue
            name, after, rest = jp
            out.append(dict(obj=o, cisi=r.cisi, site=r.site, kind=r.kind, type=r.type, area=r.area, bin=r.bin, time=r.time,
                            face=k, nfaces=r.nfaces, text='-'.join(f), name='-'.join(name), crest=(name[0] if name else ''),
                            nlen=len(name), after=after, ending=ending_label(after), rest='-'.join(rest),
                            lost=('000' in name) or len(name) == 0))
    return pd.DataFrame(out)


def seal_sizes():
    """obj -> residual size for complete seals (first face)."""
    with contextlib.redirect_stdout(io.StringIO()):
        from size_common import table, cell_medians
    S = table()
    S['res'] = S.logA.values - cell_medians(S, S.logA.values)
    return S.drop_duplicates('obj').set_index('obj')[['res', 'logA', 'area_mm2', 'siteg', 'L', 'fmt', 'signs', 'stand5', 'animal']]


def fmt_counter(c, n=None):
    return '; '.join(f'{k} {v}' for k, v in (c.most_common(n) if hasattr(c, 'most_common') else c.items()))
