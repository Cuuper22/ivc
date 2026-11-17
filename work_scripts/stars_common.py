#!/usr/bin/env python3
"""Shared kit for the star-names job (stars_*.py).

Idea under test: a number written INSIDE a name is a sound, not a count. Dravidian star names are
number + miin "star": aru-miin six-star (Pleiades), eru-miin seven-star (Great Bear), mu-miin three-star.

A "number unit" = a run of stroke signs (short-in-a-row 001-007, stacked 012-018, tall 031-036) that the
parser did not give to the opener, directly followed by one sign X (the thing the number stands on).
Its SLOT comes from the template parser (gloss2.parse_face):
  name   = on a seal, the unit sits in the run of name signs that ends in the possessive jar or a closing
           sign (spear, man, comb, porter), or on a seal with no closer at all (a bare name), and not after a jar.
  sealx  = on a seal but after the jar (or otherwise outside the name run).
  count  = on any other object (miniature tablet, copper tablet, tag, pot, tool, rod, bangle).
           count_pure = not in a name run on that object; count_named = in a name run on a goods object.
Catalogues: L = first catalogue (Lipi), Mu = second-catalogue texts with no partner in the first (new texts).
Reading order = stored order reversed (the loaders already do it).
Import: from stars_common import *
"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound_v3_common import *          # d (Lipi faces, parsed), M (second catalogue, parsed), objs, moh
from gloss2 import CNT

OUTS = f'{ROOT}/work_data/stars'
os.makedirs(OUTS, exist_ok=True)

FISHALL = {'220', '222', '226', '227', '228', '231', '232', '233', '234', '235', '236', '240', '241', '242', '243', '244'}
NUMS = {k for k, v in CNT.items() if v[0] in ('short', 'stacked', 'tall')}
STYLE = {k: v[0] for k, v in CNT.items() if k in NUMS}            # short (in a row), stacked, tall
NAMEROLES = {'crest', 'self', 'tag', 'lost', 'count', 'counted'}
WORD = {1: 'oru', 2: 'iru', 3: 'mu', 4: 'naal', 5: 'ai', 6: 'aru', 7: 'eru', 8: 'en', 9: 'tol', 10: 'patu'}


def units(x, P):
    """all number units on one face: list of dict(i, j, value, style, nxt, slot_run, postjar)."""
    R = P['roles']; n = len(x); out = []; i = 0
    jars = [q for q in range(n) if R[q] == 'poss']
    while i < n:
        if x[i] in NUMS and R[i] != 'opener':
            j = i
            while j + 1 < n and x[j + 1] in NUMS and R[j + 1] != 'opener': j += 1
            # the number that stands on the next sign is the last run of ONE stroke style (002-032-220 = 2, then tall 2 + fish);
            # an earlier run in another style is kept as 'pre' (a separate number word)
            i0 = j
            while i0 - 1 >= i and STYLE[x[i0 - 1]] == STYLE[x[j]]: i0 -= 1
            pre = '-'.join(x[i:i0])
            if j + 1 < n and x[j + 1] not in NUMS and x[j + 1] not in ('000', 'ALT'):
                val = sum(CNT[x[q]][1] for q in range(i0, j + 1))
                style = STYLE[x[j]]
                i_full = i; i = i0
                # name run: from the unit forward over name roles; what closes it?
                k = j + 1
                while k < n and R[k] in NAMEROLES: k += 1
                closer = R[k] if k < n else 'END'
                postjar = any(q < i for q in jars)
                lostnear = (i > 0 and x[i - 1] in ('000', 'ALT'))
                out.append(dict(i=i, j=j, value=val, style=style, nxt=x[j + 1], toks='-'.join(x[i:j + 1]), pre=pre,
                                closer=closer, postjar=postjar, lostnear=lostnear,
                                closed=(closer in ('poss', 'ending')), bare=(closer == 'END' and not jars and P['ending_kind'] == 'none')))
            i = j + 1
        else: i += 1
    return out


def slot_of(u, kind):
    """seal: name if the run closes in a jar/closer or the seal is a bare name; goods: count_named only if the run closes
    in a jar/closer (a named owner on a goods object), else a pure count."""
    if kind == 'seal':
        return 'name' if ((u['closed'] or u['bare']) and not u['postjar']) else 'sealx'
    return 'count_named' if (u['closed'] and not u['postjar']) else 'count_pure'


def all_units(cat='L'):
    """one row per number unit with its object, kind, site, slot. cat L or Mu."""
    rows = []
    if cat == 'L':
        it = zip(d.id, d.obj, d.cisi, d.tok, d.P, d.kind, d.site, d['area-section'], d['block-house'], d['room-grid'], d.depth, d.symbol)
        for fid, ob, cisi, x, P, k, st, ar, bh, rm, dp, sym in it:
            for u in units(x, P):
                u.update(cat='L', face=fid, obj=ob, cisi=cisi, text='-'.join(x), kind=k, site=st, area=ar, bh=bh, room=rm,
                         depth=dp, animal=str(sym).split(':')[0], slot=slot_of(u, k), ending=P['ending_kind'], rel=P['relation'] or '')
                rows.append(u)
    else:
        m = M[~M.partnered]
        for tn, x, P, k, st, sl in zip(m.textnum, m.tok, m.P, m.kind, m.site_l, m.sideline):
            for u in units(x, P):
                u.update(cat='Mu', face=f'{tn}.{sl}', obj=tn, cisi=f'M{tn}', text='-'.join(x), kind=k, site=st, area='', bh='', room='',
                         depth='', animal='', slot=slot_of(u, k), ending=P['ending_kind'], rel=P['relation'] or '')
                rows.append(u)
    return pd.DataFrame(rows)


def dedup(df):
    """one row per (object, unit position): moulded tablet copies count once per object; identical texts once per text too."""
    return df.drop_duplicates(['obj', 'i', 'toks', 'nxt'])


def distinct(df):
    """one row per distinct text and unit position (moulded copies and repeated texts count once)"""
    return df.drop_duplicates(['text', 'i', 'toks', 'nxt'])
