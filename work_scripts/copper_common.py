#!/usr/bin/env python3
"""Shared kit for the COPPER job (copper_*.py): the copper tablets of Mohenjo-daro read as a record system, with no word
on any sign. Written 2026-11-17 before any copper_* number was computed.

Plain words:
- OBJECT: one copper tablet. First catalogue (Lipi): one object id, one row per inscribed face. Second catalogue
  (Mahadevan 1977, 'M77'): one text number, one row per line or side; a side with no text but a picture code is
  sideline 29 and carries the picture code fs80.
- TEXT FACE: the longest inscribed face. SECOND FACE: any other inscribed face. A second face of one or two signs is a
  PICTURE-SIDE SIGN: the face where other copies carry the picture carries one sign instead.
- PICTURE: the drawing on the other side. Three independent sources, kept apart:
    cat  = the first catalogue's code (Hare, Elep, Othr ...; Othr / blank / '-' = vague);
    m77  = the second catalogue's field-symbol code fs80 (three digits: two-digit family + one sub-type digit; e.g. 147 =
           family 14, sub-type 7). Family names come from what those codes show on SEALS (01 unicorn, 03 zebu, 04 gaur,
           06 buffalo, 07 elephant, 09 tiger, 11 rhinoceros, 36 gharial) and, for families seen only on copper, from
           the photo check (eye);
    eye  = what the photograph shows, read by the lead in work_data/copper/photo_check.csv.
  The working picture of an object is eye if read, else the catalogue code if specific, else the M77 family if the
  object is matched, else unknown. No picture is ever copied from a set to its members.
- SET: copies with the same text face. ONE OBJECT COUNTED ONCE: the two catalogues re-transcribe mostly the same
  tablets, and only text, site and an area code can tie them. So the count of copies of a text is
  max(first-catalogue copies, second-catalogue copies), never their sum (the rule of twins_1_build.py). The first
  catalogue is the object list; second-catalogue objects only add copies where they exceed the first catalogue's.
  A damaged text (lost sign 000) joins a set only when its kept signs fit exactly one complete text of the same length.
- FINDSPOT: area (DK-, VSA, HR- ...), block-house (e.g. 9VII), room / grid, depth in feet. BIN: early / middle / late
  from work_data/time/time_axis.csv.
- JOB of a sign: frame v2 class (work_data/frame/classes_v2.csv). TEXT KIND of a face, from jobs only:
    'one sign'            a single sign
    'name+closer'         name signs closed by a closer (jar 740, spear 520, porters), no count after
    'record'              name + closer and a count line (number + counted thing / measure), in either order
    'name+count'          name signs and a count line, no closer
    'count line'          only numbers with counted things / measures
    'name'                name signs only, no closer, no count
  COUNT LINE = a number run next to a counted thing (THING), a measure (MEASURE) or the cup 700.
"""
import sys, os, io, contextlib, collections, re, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
with contextlib.redirect_stdout(io.StringIO()):
    from measures_common import objs, d, M, NUM, runs, ROOT
ROOT = '/home/antigravity/Cuuper22/ivc'
OUT = f'{ROOT}/work_data/copper'; os.makedirs(OUT, exist_ok=True)
IMG = f'{ROOT}/evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images'
T0 = time.time()


def say_to(path):
    f = open(path, 'w')
    def say(*a):
        s = ' '.join(str(x) for x in a); print(f'[{time.time() - T0:6.1f}s] {s}', flush=True); f.write(s + '\n'); f.flush()
    return say


C2 = pd.read_csv(f'{ROOT}/work_data/frame/classes_v2.csv', dtype=str).fillna('')
V2 = dict(zip(C2.sign, C2.v2_base))
def job(s):
    if s == '706': return 'MEASURE'      # frame v2 files 706 as a name part; the frame book reads 705/706 as one measure (FRAME 9, 11)
    return 'NUM_SHORT' if s in NUM and s not in V2 else V2.get(s, 'PERSONAL')

NUMJ = {'NUM_SHORT', 'NUM_TALL', 'NUM_NAME'}
NAMEJ = {'CREST', 'PERSONAL', 'PLACE', 'NAME_BACK', 'AFTER_M'}


def text_kind(tok):
    t = [s for s in tok]
    if len(t) == 1: return 'one sign'
    J = [job(s) for s in t]
    cnt = set()
    for i, j in enumerate(J):
        if j in NUMJ:
            for k in (i - 1, i + 1):
                if 0 <= k < len(J) and (J[k] in ('THING', 'MEASURE') or t[k] == '700'):
                    cnt |= {i, k}
    closer = [i for i, j in enumerate(J) if j == 'CLOSER']
    name = [i for i, j in enumerate(J) if i not in cnt and j in NAMEJ | {'OPEN', 'SLOT', 'TITLE'} | NUMJ | {'THING', 'MEASURE'} and j != 'CLOSER']
    if closer:
        return 'record' if cnt else 'name+closer'
    if cnt and name: return 'name+count'
    if cnt: return 'count line'
    return 'name'


# --------------------------------------------------------------------- first catalogue copper tablets
NOPIC = {'', '-', 'Othr', 'Unknown', '?', 'None', 'X', 'Hgls'}
TA = pd.read_csv(f'{ROOT}/work_data/time/time_axis.csv', dtype=str).fillna('')
BIN = dict(zip(TA.obj, TA.bin))
g = d.groupby('obj').agg(room=('room-grid', 'first'), exc=('excavation-idno', 'first'), cult=('cult', 'first'),
                         time=('time', 'first'), period=('period', 'first'))
_files = os.listdir(IMG) if os.path.isdir(IMG) else []


def _ft(s):
    m = re.search(r'(-?\d+(\.\d+)?)\s*ft', str(s))
    return abs(float(m.group(1))) if m else np.nan


def load_L():
    rows = []
    for o in objs[objs.kind == 'ctab'].itertuples():
        fs = [tuple(x) for x in o.faces]
        main = max(fs, key=len)
        others = [f for f in fs if f is not main]
        picsign = [f for f in others if len(f) == 1]
        second = [f for f in others if len(f) > 1]
        code = str(o.symbol).split(':')[0].split('+')[0].strip()
        gg = g.loc[o.Index]
        ph = sorted(f for f in _files if o.cisi not in ('', '-') and f.startswith(o.cisi + '_'))
        rows.append(dict(obj=str(o.Index), cisi=o.cisi, site=o.site, text='-'.join(main), n=len(main),
                         complete='000' not in main, picsign=' / '.join('-'.join(f) for f in picsign),
                         second=' / '.join('-'.join(f) for f in second), cat=code, cat_full=str(o.symbol), cult=gg.cult,
                         area=o.area, bh=o.bh, room=gg.room, depth=o.depth, ft=_ft(o.depth), exc=gg.exc,
                         bin=BIN.get(str(o.Index), ''), time=gg.time, h=o.h, v=o.v, photos='|'.join(ph),
                         kind=text_kind(main)))
    L = pd.DataFrame(rows)
    return L


# --------------------------------------------------------------------- second catalogue copper tablets
FAMILY = {'01': 'unicorn', '03': 'zebu', '04': 'gaur', '06': 'buffalo', '07': 'elephant', '09': 'tiger', '11': 'rhinoceros',
          '36': 'gharial'}


def fam(code):
    if not code or code == '0': return ''
    c = f'{int(code):03d}'
    return c[:2]


def load_M():
    R = pd.read_csv(f'{ROOT}/research/data/mahadevan_20260905/concordance_rows.csv', dtype=str).fillna('')
    P = M.copy()
    P = P[P.cls == 'copper tablet']
    tn = set(P.textnum)
    R = R[R.textnum.isin(tn)]
    rows = []
    for t, gR in R.groupby('textnum'):
        lines = P[P.textnum == t]
        fsv = [int(x) for x in gR.fs80 if x not in ('', '0')]
        texts = [(tuple(x), bool(c), sl) for x, c, sl in zip(lines.tok, lines.complete_b, lines.sideline)]
        texts = [x for x in texts if x[0]]
        if not texts: continue
        main = max(texts, key=lambda x: len(x[0]))
        others = [x for x in texts if x is not main]
        txt = '-'.join(main[0]).replace('615-615', '617')   # the second catalogue splits 617 into two 615s
        rows.append(dict(textnum=t, text=txt, n=len(txt.split('-')), complete=main[1] and '000' not in main[0],
                         picsign=' / '.join('-'.join(x[0]) for x in others if len(x[0]) == 1),
                         second=' / '.join('-'.join(x[0]) for x in others if len(x[0]) > 1),
                         fs=(str(fsv[0]) if fsv else ''), fam=(fam(fsv[0]) if fsv else ''),
                         locus=gR.locus.iloc[0], level=gR.level.iloc[0], kind=text_kind(main[0])))
    return pd.DataFrame(rows)


def fits(dmg, full):
    a, b = dmg.split('-'), full.split('-')
    return len(a) == len(b) and all(x == '000' or x == y for x, y in zip(a, b))


def align_score(a, b):
    a, b = a.split('-'), b.split('-')
    if len(a) != len(b): return 0
    eq = {('405', '407'), ('407', '405'), ('406', '407'), ('705', '706'), ('706', '705')}
    return sum(x == y or (x, y) in eq for x, y in zip(a, b)) / len(a)


def eye_table():
    p = f'{OUT}/photo_check.csv'
    return pd.read_csv(p, dtype=str).fillna('') if os.path.exists(p) else pd.DataFrame(columns=['cisi', 'eye'])
