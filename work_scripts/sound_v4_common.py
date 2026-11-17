#!/usr/bin/env python3
"""Shared kit for the fourth sound pass (sound_v4_*.py): the third-pass loader (sound_v3_common) plus the
third value list, a coverage counter (faces readable start to finish with built-on values) and the gain table
(how many more faces become readable if one sign got a built-on value).
Import: from sound_v4_common import *"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound_v3_common import *
from sound_v3_values import V3, TIER3
OUT4 = f'{ROOT}/work_data/sound_v4'
os.makedirs(OUT4, exist_ok=True)
SH = pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv', dtype=str).set_index('lipi_wells_number').shape_description.to_dict()


def readable(x, T, allow=('base', 'building')):
    """a face reads start to finish: 2+ signs, nothing lost, every sign a number or a value in the allowed tiers."""
    return len(x) >= 2 and '000' not in x and 'ALT' not in x and all(a in VAL or T.get(a) in allow for a in x)


def coverage(T, allow=('base', 'building')):
    """Lipi complete faces readable start to finish, split all / seals / goods (everything but seals)."""
    sub = d[d.complete_txt]
    hit = sub.tok.apply(lambda x: readable(x, T, allow))
    out = {}
    for grp, m in [('all', np.ones(len(sub), bool)), ('seals', (sub.kind == 'seal').values), ('goods', (sub.kind != 'seal').values)]:
        h = hit.values & m
        out[grp] = dict(faces=int(h.sum()), of_faces=int(m.sum()), distinct=len(set(sub.tok[h])), of_distinct=len(set(sub.tok[m])),
                        objects=sub[h].obj.nunique())
    return out


def gains(T, allow=('base', 'building')):
    """for each sign without a built-on value: faces (and distinct texts) that it alone keeps from reading."""
    sub = d[d.complete_txt]
    g = collections.Counter(); gd = collections.defaultdict(set); gs = collections.Counter()
    for x, k in zip(sub.tok, sub.kind):
        if len(x) < 2 or '000' in x or 'ALT' in x: continue
        miss = {a for a in x if not (a in VAL or T.get(a) in allow)}
        if len(miss) == 1:
            s = miss.pop(); g[s] += 1; gd[s].add(x); gs[s] += k == 'seal'
    return g, gd, gs
