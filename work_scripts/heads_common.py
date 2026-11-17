#!/usr/bin/env python3
"""Shared kit for the HEADS job (heads_*.py): the issuing side of the Harappa tablets.  Written 2026-11-17 before any
heads number.  Word-free: sign numbers, pictures, jobs, counts, findspots.

Plain words:
- OBJECT / STONE: one physical tablet.  Catalogue rows that describe one stone are merged (recheck_common.stone_map).
- FACE: one inscribed side.  A tablet with 2 or 3 faces is one RECORD.  PARTNERS of a face = the other faces of the same tablet.
- ISSUE (copy event): all tablets of one trench with the same full text (all faces) count once (rule 3 of FRAME.md).
- JAR FACE: a face holding the jar 740 (a name ending in the jar, with any title after it).  AMOUNT FACE: only counts and
  measure signs (chits_common.face_type).  LOST: all signs broken.  A face holding a lost sign (000) is not used as a heading
  and is not counted as a distinct partner.
- HEADING (fixed rule, set before any number): a face of a Harappa tablet that
    (1) is not an amount face and not lost, (2) holds no jar (so it is not a name ending in the jar), (3) holds no lost sign,
    (4) stands on tablets beside at least 4 DIFFERENT complete partner faces.
  "Different" partner faces are counted on a PARTNER KEY (added after the first look, because 033-700 and 700-033 are one amount
  written in two orders and 705/706 are one sign drawn two ways): amount faces are keyed by their reading (cups, big measure ...),
  every other face by its sign string with 706 written as 705.  The raw-string count is shown beside it.
  Tier A groups by the exact sign string.  Tier B groups by FAMILY: a string with its trailing count / measure / front-word signs cut off (kept >= 2 signs):
  413-575-335-711-033-700 -> 413-575-335-711; 413-892-824 -> 413-892; 415-578-032-824 -> 415-578.  No other joining.
  (A first version also joined strings by sign-prefix; it fused different names such as 415-220 and 415-220-520, so it was dropped.)
  KIND of a heading (descriptive, added after the first look, applied to all alike): OFFICE LINE when at least half of its
  partner faces are jar faces (names); SIDE FACE when most partners are amount faces (the heading is then a name-like face
  without a jar that draws different amounts).
  A heading is a tier-A string or a tier-B family that meets (4).  All downstream tables use the tier-B family.
- MOUND: first letter group of the trench name (AB, ET, E, F, D ...), as in chits_2_names.py.
- Partner ROLE (of a partner face): jar only / comb 400 / man 090 / other title / jar + other sign / amount / name without jar /
  thing / lost.
Import: from heads_common import *
"""
import sys, os, io, contextlib, collections, re, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
with contextlib.redirect_stdout(io.StringIO()):
    from chits_common import *          # load, name_rows, jar_parse, ending_label, amount_of, face_type, TITLES, NUM, UNITS, pic, fmt_counter, V2
    from recheck_common import stone_map, pvalue_hi, pvalue_lo
ROOT = '/home/claude/ivc'
HOUT = f'{ROOT}/work_data/heads'; os.makedirs(HOUT, exist_ok=True)
T0 = time.time()


def log_to(path):
    fh = open(path, 'w')
    def say(*a):
        s = ' '.join(str(x) for x in a); print(f'[{time.time() - T0:6.1f}s] {s}', flush=True); fh.write(s + '\n'); fh.flush()
    return say


def mound(a):
    """mound = the letters before 'Trench' (E, ET, F, AB ...).  NOTE: chits_2_names.py read 'ETrench 11' as mound ET because the name
    starts with ET; ETrench 11 is trench 11 of Mound E, and mound ET is the 'ETTrench' series.  Here they are kept apart."""
    a = (a or '').strip()
    if not a: return ''
    if 'Trench' in a:
        m = a.split('Trench')[0]
        if m.startswith('E-ET'): return 'ET'
        return m.strip('-') or '(unknown)'
    if a.endswith('-'): return a[:-1]
    if a in ('EA', 'EB', 'EC'): return 'E'
    if a.startswith('FGran'): return 'F'      # the granary area lies on Mound F
    return a.split()[0]


def trench_name(a): return (a or '').strip() or '(none)'


def harappa_stones():
    """Harappa objects, one row per physical stone, with issue key. Returns DataFrame indexed by obj."""
    with contextlib.redirect_stdout(io.StringIO()):
        O = load()
    f2s, merges = stone_map()
    o2s = {}
    for k, v in f2s.items(): o2s[k.split('.')[0]] = v
    H = O[O.site == 'Harappa'].copy()
    H['stone'] = [o2s.get(str(o), str(o)) for o in H.obj]
    H = H[H.stone.astype(str) == H.obj.astype(str)]          # keep one object per stone (the lowest id)
    H['mound'] = H.area.map(mound)
    H['trench'] = H.area.map(trench_name)
    H['issue'] = [f'{a}||{s}' for a, s in zip(H.area, H.sig)]
    H['moulded'] = H.type.map({'TAB:B': 'moulded', 'TAB:I': 'incised'}).fillna('')
    return H


def face_str(f): return '-'.join(f)


def stem_of(f):
    """face string with trailing count / measure signs cut off (kept >= 2 signs)."""
    t = list(f)
    while len(t) > 2 and (t[-1] in NUM or t[-1] in UNITS or V2.get(t[-1]) == 'OPEN'): t = t[:-1]
    return '-'.join(t)


def partner_role(face, ty, jp):
    if jp is not None:
        a = jp[1]
        if a == '': return 'jar only'
        if a == '400': return 'comb'
        if a == '090': return 'man'
        if a in TITLES: return 'other title'
        return 'jar + other'
    if ty == 'amount': return 'amount'
    if ty == 'lost' or '000' in face: return 'lost'
    if ty == 'name': return 'name no jar'
    return 'thing'


def amount_text(face):
    """compact amount text: e.g. '3 cup', '1 big', '2 tree'."""
    a = amount_of(face)
    return ', '.join(f'{v if v is not None else "?"} {k}' for k, v in a.items())


def pkey(face, ty):
    """partner key: amount faces by their reading, other faces by string with 706 -> 705."""
    t = [('705' if x == '706' else x) for x in face]
    if ty == 'amount':
        a = amount_of(face)
        if a: return 'AMT:' + ','.join(f'{k}={v}' for k, v in sorted(a.items()))
    return '-'.join(t)
