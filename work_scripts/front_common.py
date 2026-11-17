#!/usr/bin/env python3
"""Shared kit for the FRONT job (front_*.py): what is the front of an Indus text?  Written 2026-11-17, before any
front_* number was computed.

Plain words
- FACE: one inscribed side (one row of the Lipi catalogue). Signs here are in READING order (work_data/frame/corpus_jobs.csv).
- STONE: one physical object; faces joined by object id, duplicate catalogue rows merged (recheck_common.stone_map).
- COPY EVENT: identical full text at the same site and the same findspot (building) counted once (clean counting rule).
- KIND of object: seal, tablet (moulded TAB:B or incised TAB:I clay/faience tablets), copper (TAB:C), tag (clay sealings
  and tags with impressions), pot, other (bangles, rods, implements ...).
- COMPLETE face: no lost sign (000), no broken edge flag, no ALT (alternative reading) mark.

FRONT WORD, fixed rule (written here before the counts):
  a sign is a front word if (a) frame v2 files it as OPEN (820 861 817 920 692 880 824 545 091 550 360 556), or
  (b) it stands first in 60% or more of its uses on complete faces AND, when first, is followed by a frame-v2 SLOT sign
      (002 060 741 742 368 365) at least 4 times and in at least half of its first-position uses.
  A text BEGINS WITH A FRONT when its first sign is a front word.
SLOT SIGNS: frame v2 SLOT = 002 060 741 742 368 365 (745 is checked separately: it is the third 'ward' variant).
FRONT UNIT of a text: the front word plus up to two slot signs right after it (920-060-741 is one unit).
NAME of a text: the signs after the front unit and before the ENDING; ENDING = the longest run at the end of the text of
  closer / after-jar title signs (frame v2 CLOSER and TITLE: 740 520 151 154 155 158 / 400 090 527 621 679 565 161 241).
  A text 'has a name and a closer' when the name is 1+ signs and the ending holds a CLOSER sign.
COUNT LINE after the front: the signs after the front unit are numbers then one counted thing (frame v2 shape).
"""
import sys, os, re, time, collections, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
with contextlib.redirect_stdout(io.StringIO()):
    from recheck_common import stone_map, faces as lipi_faces

ROOT = '/home/claude/ivc'
OUTF = f'{ROOT}/work_data/front'
os.makedirs(OUTF, exist_ok=True)
T0 = time.time()

C2 = pd.read_csv(f'{ROOT}/work_data/frame/classes_v2.csv', dtype=str).fillna('')
V2 = dict(zip(C2.sign, C2.v2_base))
V2_OPEN = {'820', '861', '817', '920', '692', '880', '824', '545', '091', '550', '360', '556'}
SLOT = {'002', '060', '741', '742', '368', '365'}
CLOSERS = {s for s, c in V2.items() if c == 'CLOSER'}
TITLES = {s for s, c in V2.items() if c == 'TITLE'}
NUMS = {s for s, c in V2.items() if c in ('NUM_SHORT', 'NUM_TALL', 'NUM_NAME')}
KMAP = {'seals': 'seal', 'tablets': 'tablet', 'copper tablets': 'copper', 'tags and sealings': 'tag', 'pots': 'pot',
        'other objects': 'other'}
KINDS = ['seal', 'tablet', 'copper', 'tag', 'pot', 'other']
SP = {'Bull1': 'unicorn', 'Gaur': 'short-horned bull', 'Zebu': 'zebu', 'Elep': 'elephant', 'Rhin': 'rhinoceros',
      'Tigr': 'tiger', 'Buff': 'buffalo', 'Goat': 'goat', 'Bull': 'bull'}


def make_logger(name):
    fh = open(f'{OUTF}/{name}', 'w')
    def say(*a):
        s = ' '.join(str(x) for x in a)
        print(f'[{time.time()-T0:6.1f}s] {s}', flush=True); fh.write(s + '\n'); fh.flush()
    return say


def anim(sym):
    sym = str(sym).strip()
    if sym in ('', 'None', 'nan'): return 'none'
    if sym in ('-', '?', 'Unknown'): return ''
    return SP.get(sym.split(':', 1)[0], sym.split(':', 1)[0])


def load():
    """one row per face, every face of the first catalogue."""
    c = pd.read_csv(f'{ROOT}/work_data/frame/corpus_jobs.csv', dtype=str, keep_default_na=False)
    L = lipi_faces().set_index('id')
    f2s, _ = stone_map(L.reset_index())
    D = c[['face', 'cisi', 'site', 'object_kind', 'signs', 'v2_classes', 'broken_edge', 'text_kind']].copy()
    D['kind'] = D.object_kind.map(KMAP).fillna('other')
    D['obj'] = D.face.str.split('.').str[0]
    D['stone'] = D.face.map(f2s)
    for col, src in (('type', 'type'), ('symbol', 'symbol'), ('area', 'area-section'), ('bh', 'block-house'),
                     ('room', 'room-grid'), ('sides', 'sides'), ('shape', 'shape')):
        D[col] = D.face.map(L[src])
    h = pd.to_numeric(D.face.map(L['horizontal(mm)']), errors='coerce')
    v = pd.to_numeric(D.face.map(L['vertical(mm)']), errors='coerce')
    D['area_mm2'] = h * v
    D.loc[~(D.area_mm2 > 0), 'area_mm2'] = np.nan
    D['animal'] = D.symbol.map(anim)
    D['fmt'] = D.type.map(lambda t: {'SEAL:S': 'square', 'SEAL:R': 'rectangular', 'SEAL:C': 'round',
                                     'SEAL:CY': 'cylinder'}.get(t, 'other'))
    # findspot building: stamps/objects.csv where it has one, else site|area|block-house
    O = pd.read_csv(f'{ROOT}/work_data/stamps/objects.csv', dtype=str, keep_default_na=False).set_index('face')
    ob = D.face.map(O['building']).fillna('')
    def bkey(r, b):
        if b: return f'{r.site}|{b}'
        a = r.area if r.area not in ('', '--', '-') else ''
        bh = r.bh if r.bh not in ('', '--', '-') else ''
        rm = r.room if r.room not in ('', '--', '-') else ''
        if a and (bh or rm): return f'{r.site}|{a}|{bh or rm}'
        return ''
    D['building'] = [bkey(r, b) for r, b in zip(D.itertuples(), ob)]
    D['areakey'] = [f'{s}|{a}' if a not in ('', '--', '-') else '' for s, a in zip(D.site, D.area)]
    TA = pd.read_csv(f'{ROOT}/work_data/time/time_axis.csv', dtype=str, keep_default_na=False).set_index('obj')
    D['bin'] = D.obj.map(TA['bin']).fillna('')
    D['tok'] = D.signs.map(lambda s: tuple(s.split('-')) if s else ())
    D['complete'] = [(bool(t) and '000' not in t and not any(x.startswith('X') or x == 'ALT' for x in t)
                      and be == 'False') for t, be in zip(D.tok, D.broken_edge)]
    D['first_ok'] = [bool(t) and t[0] not in ('000', 'ALT') and not t[0].startswith('X') for t in D.tok]
    D['siteg'] = D.site.map({'Mohenjo-daro': 'MD', 'Harappa': 'HP'}).fillna('other')
    return D.reset_index(drop=True)


def front_set(D, say=print):
    """the fixed rule in the docstring."""
    C = D[D.complete]
    uses = collections.Counter(); first = collections.Counter(); fslot = collections.Counter()
    for t in C.tok:
        for s in set(t): uses[s] += 1
        first[t[0]] += 1
        if len(t) > 1 and t[1] in SLOT: fslot[t[0]] += 1
    F = set(V2_OPEN); added = []
    for s in uses:
        if s in F or s in SLOT: continue
        if first[s] >= 0.6 * uses[s] and fslot[s] >= 4 and fslot[s] >= 0.5 * first[s]:
            F.add(s); added.append((s, uses[s], first[s], fslot[s]))
    say(f'front words by rule: v2 OPEN {sorted(V2_OPEN)}; added by position {added}')
    return F, uses, first, fslot


def parse(t, F):
    """returns dict: front, slots, name (tuple), ending (tuple), body (all after front unit)."""
    t = tuple(t)
    front, slots, i = '', (), 0
    if t and t[0] in F:
        front = t[0]; i = 1
        while i < len(t) and t[i] in SLOT and len(slots) < 2:
            slots += (t[i],); i += 1
    body = t[i:]
    j = len(body)
    while j > 0 and (body[j - 1] in CLOSERS or body[j - 1] in TITLES): j -= 1
    name, ending = body[:j], body[j:]
    is_count = len(body) >= 2 and V2.get(body[-1]) == 'THING' and all(s in NUMS for s in body[:-1])
    return dict(front=front, slots=slots, unit='-'.join((front,) + slots) if front else '', body=body,
                name=name, ending=ending, has_closer=any(s in CLOSERS for s in ending), is_count=is_count)


def add_parse(D, F):
    P = [parse(t, F) for t in D.tok]
    for k in ('front', 'slots', 'unit', 'body', 'name', 'ending', 'has_closer', 'is_count'):
        D[k] = [p[k] for p in P]
    D['slot1'] = [s[0] if s else '' for s in D.slots]
    D['slotstr'] = ['-'.join(s) for s in D.slots]
    D['namestr'] = ['-'.join(n) for n in D.name]
    D['endstr'] = ['-'.join(e) for e in D.ending]
    D['crest'] = [next((s for s in n if s not in NUMS), '') for n in D.name]
    D['L'] = D.tok.map(len)
    return D


def copy_events(D):
    """one row per copy event: same site, same building (or same stone when no building), same full text."""
    key = [f'{s}|{b or "stone:" + st}|{x}' for s, b, st, x in zip(D.site, D.building, D.stone, D.signs)]
    D = D.assign(ckey=key)
    return D.drop_duplicates('ckey')


def size_resid(S):
    """seals: log face area minus the median log area of seals of the same site group, text length (cap 8) and format,
    leaving the seal itself out (cells under 4 seals fall back to site group + format)."""
    S = S.copy(); S['logA'] = np.log(S.area_mm2); S['Lc'] = S.L.clip(upper=8)
    out = np.full(len(S), np.nan)
    g1 = S.groupby(['siteg', 'Lc', 'fmt']).logA; g2 = S.groupby(['siteg', 'fmt']).logA
    cell1 = {k: v.dropna().values for k, v in g1}; cell2 = {k: v.dropna().values for k, v in g2}
    for i, r in enumerate(S.itertuples()):
        if np.isnan(r.logA): continue
        v = cell1.get((r.siteg, r.Lc, r.fmt), np.array([]))
        if len(v) < 5: v = cell2.get((r.siteg, r.fmt), np.array([]))
        v = list(v);
        try: v.remove(r.logA)
        except ValueError: pass
        if len(v) >= 3: out[i] = r.logA - np.median(v)
    return out


def pval_hi(null, obs):
    null = np.asarray(null); return float((1 + (null >= obs).sum()) / (len(null) + 1))


def pval_lo(null, obs):
    null = np.asarray(null); return float((1 + (null <= obs).sum()) / (len(null) + 1))


def deal_within(labels, groups, rng):
    """shuffle labels inside each group (arrays)."""
    labels = np.asarray(labels, dtype=object).copy(); groups = np.asarray(groups)
    out = labels.copy()
    for g in np.unique(groups):
        ix = np.where(groups == g)[0]
        out[ix] = labels[rng.permutation(ix)]
    return out
