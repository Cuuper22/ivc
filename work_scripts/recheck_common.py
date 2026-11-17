"""Shared helpers for the recheck_NN_*.py scripts (2026-11-17).

Why these scripts exist: a headline result (same-room seals share the stand letter 38.1% against 17.2%) was a counting
error, for two reasons: (1) two FACES of one stone were counted as a pair of seals (such a pair always shares);
(2) the chance figure shuffled labels among a pool holding stones that cannot carry the label at all.
Each recheck script reruns one finding with:
  (a) one row per physical object: faces joined by object id (the Lipi id before the dot, e.g. 1338.1 and 1338.2 are
      one object 1338); two catalogue rows of one stone merged (rule below);
  (b) the shuffle confined to objects that can carry the property, within site and within the original design's strata;
  (c) identical moulded copies found together counted once (same site, same findspot, same full text = one event).

RULE for "two catalogue rows are the same stone" (decided from the data, see recheck_00_identity.py):
  same site, same full text on every face, and the same excavation number after the plate reference is cut off
  (e.g. "VS 3590CXVIII:2" -> "VS 3590", "H2000-5003Figure 42.06" -> "H2000-5003"); excavation numbers that are lot
  codes shared by 3+ different texts, or carry no digit, do not count; exactly two rows, and where both give a size
  the sizes agree within 1.0 mm (3+ rows under one number, e.g. Harappa G256 with 13 tablets, are a lot of copies;
  Harappa G58, 34.5 against 33 mm, and 1646, 34 against 38 mm, stay two stones). Rows with two CISI numbers can still be
  one stone (H-316 = H-1304, H-912 = H-1191: same number, findspot, text and size). CISI numbers are never shared by two objects
  in this catalogue (checked), so they cannot be used to merge.
"""
import re, collections
import numpy as np, pandas as pd

ROOT = '/home/claude/ivc'
LIPI = f'{ROOT}/research/data/open_prototype/lipi/metadata_filtered.csv'
OUT = f'{ROOT}/work_data/recheck'
EMPTY = {'', '-', '--', '- -'}


def log_to(path):
    fh = open(path, 'w')
    def say(*a):
        s = ' '.join(str(x) for x in a); print(s, flush=True); fh.write(s + '\n'); fh.flush()
    return say


def norm_exc(e):
    e = (e or '').strip()
    e = re.split(r'Figure|CX|CI|CV|CL|XC|LX', e)[0].strip()
    return e if re.search(r'\d', e) else ''


def faces():
    d = pd.read_csv(LIPI, dtype=str, keep_default_na=False)
    d['obj'] = d.id.str.split('.').str[0]
    return d


def stone_map(d=None):
    """face id -> stone id (object id, with duplicate catalogue rows merged). Returns (dict face->stone, list of merges)."""
    if d is None: d = faces()
    o = d.groupby('obj').agg(site=('site', 'first'), exc=('excavation-idno', 'first'), cisi=('cisi', 'first'),
                             sig=('text', lambda s: '|'.join(sorted(s))),
                             h=('horizontal(mm)', 'first'), v=('vertical(mm)', 'first'))
    o['h'] = pd.to_numeric(o.h, errors='coerce').fillna(0); o['v'] = pd.to_numeric(o.v, errors='coerce').fillna(0)
    o['nexc'] = o.exc.map(norm_exc)
    # lot codes: one normalised number carried by 3+ different texts at a site
    lot = o[o.nexc != ''].groupby(['site', 'nexc']).sig.nunique()
    lots = set(lot[lot >= 3].index)
    o2stone = {k: k for k in o.index}
    merges = []
    for (site, ne, sig), g in o[o.nexc != ''].groupby(['site', 'nexc', 'sig']):
        if (site, ne) in lots or len(g) != 2: continue      # 3+ rows under one number = a lot of copies, not one stone
        a, b = g.iloc[0], g.iloc[1]
        if any(x and y and abs(x - y) > 1.0 for x, y in ((a.h, b.h), (a.v, b.v))): continue   # sizes differ: two stones
        keep = sorted(g.index, key=int)[0]
        for k in g.index:
            o2stone[k] = keep
        merges.append((site, ne, sig, list(g.index)))
    f2s = {fid: o2stone[ob] for fid, ob in zip(d.id, d.obj)}
    return f2s, merges


def obj_of(face_id):
    return str(face_id).split('.')[0]


def pvalue_hi(null, obs):
    null = np.asarray(null); return float((1 + (null >= obs).sum()) / (len(null) + 1))


def pvalue_lo(null, obs):
    null = np.asarray(null); return float((1 + (null <= obs).sum()) / (len(null) + 1))


def progress(label, i, n, every=None):
    every = every or max(1, n // 4)
    if (i + 1) % every == 0 or i + 1 == n:
        print(f'    {label}: {i + 1}/{n} ({100 * (i + 1) // n}%)', flush=True)


def same_object_pairs(ids_a, ids_b):
    """how many of the listed pairs are two faces / two rows of one physical stone"""
    f2s, _ = stone_map()
    return sum(f2s.get(a, obj_of(a)) == f2s.get(b, obj_of(b)) for a, b in zip(ids_a, ids_b))
