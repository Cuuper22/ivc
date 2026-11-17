#!/usr/bin/env python3
"""Shared kit for the long-text job (long_texts_build.py, long_texts_stats.py, long_texts_fix.py).

Objects are rebuilt from the Lipi table: faces in id order (.1 .2 ...), lines inside a face split at '/',
and everything reversed into reading order (stored order = reverse of reading order, the line order too:
checked on M-314 against Mahadevan text 1400, where line 1 starts 391-99-65-67-70-211 = 820 002 235 240 231 520).
Phrases = stretches of a line cut after a closer (jar + relation, spear, porter, comb/man ending, load tag) and
before an opener.  Each phrase is parsed again with the possessive parser (gloss2.parse_face).
"""
import sys, os, re, collections
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gloss import A_VARIANTS
from gloss2 import load2, learn, parse_face, CNT, NOUN, CARRIED, RELATION, ENDINGS, WORDS
from sound_v2_tiers import V2, CLASS, TIER

ROOT = '/home/claude/ivc'
DATA = f'{ROOT}/research/data/open_prototype/lipi/metadata_filtered.csv'
OUTDIR = f'{ROOT}/work_data/long_texts'
os.makedirs(OUTDIR, exist_ok=True)

SH = pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv', dtype=str).set_index('lipi_wells_number').shape_description.to_dict()
PROF = pd.read_csv(f'{ROOT}/work_data/sound/profile.csv', dtype=str).set_index('sign')
NUMVAL = {k: v[1] for k, v in CNT.items() if v[0] != 'comb'}
PORTER = {'151', '153', '154', '155', '156', '157', '158'}
OPEN_SIGNS = {'861', '817', '820'}
CAP_HEADS = {'920', '692', '550', '820'}
CAP_SEL = {'741', '742', '745'}
FISH = {'220', '235', '240', '233', '231', '226', '236'}
RELNAME = {'090': 'manager', '400': 'junior', '679': 'seat', '001': 'one', '621': 'barred rectangle', '565': 'sign 565'}
ENDNAME = {'520': 'chief', '090': 'manager', '400': 'junior', '151': 'keeper', '153': 'keeper', '154': 'keeper', '155': 'keeper',
           '156': 'keeper', '157': 'keeper', '158': 'keeper'}


def shape_words(s):
    """Plain words for a sign picture."""
    if s == '000': return 'lost sign'
    d = SH.get(s) or ''
    d = re.split(r'[;.]', d)[0].strip()
    if s in CNT:
        ser, v = CNT[s]
        if ser == 'comb': return 'A-shape with a comb of ticks (load count)'
        return f"{v} {'full-height' if ser == 'tall' else 'short'} stroke{'s' if v > 1 else ''}" if ser != 'stacked' else f'{v} stacked strokes'
    nm = NOUN.get(s)
    base = d[:78]
    return f'{nm}: {base}' if nm and nm.lower() not in base.lower()[:20] else (base or f'sign {s}')


def num_of(s):
    ser_v = CNT.get(s)
    return None if ser_v is None or ser_v[0] == 'comb' else ser_v[1]


def snd(s):
    """Working sound or None."""
    v = V2.get(s)
    if not v or v[0] in ('?', ''): return None
    return v[0]


def gloss_en(s):
    v = V2.get(s)
    return v[1] if v else None


def slot_desc(s):
    """What kind of word an unvalued sign must be, from its measured slot (profile.csv)."""
    if s in ('000', 'ALT'): return 'lost sign'
    if s not in PROF.index: return 'rare sign, slot unmeasured'
    r = PROF.loc[s]
    def parse(cell):
        c = collections.Counter()
        if isinstance(cell, str):
            for part in cell.split(';'):
                m = re.match(r'\s*(\S+)\s+(\d+)', part)
                if m: c[m.group(1)] += int(m.group(2))
        return c
    roles = parse(r['roles']); pos = parse(r['namepos']); n = max(1, sum(roles.values()))
    bits = []
    if roles.get('counted', 0) / n >= .35: bits.append('a counted thing (takes a number before it)')
    if roles.get('opener', 0) / n >= .35: bits.append('an opener word')
    if roles.get('tag', 0) / n >= .3: bits.append('a name-tag word (closes a name)')
    if roles.get('crest', 0) / n >= .3: bits.append('a house-crest word (opens a name)')
    if not bits:
        tp = sum(pos.values())
        if tp:
            top = pos.most_common(1)[0]
            where = {'first': 'name-front', 'mid': 'name-middle', 'last': 'name-end', 'alone': 'whole-name'}.get(top[0], top[0])
            bits.append(f'a {where} word ({top[0]} {top[1]} of {tp})')
        else:
            bits.append('a word of unmeasured kind')
    return bits[0] + f' [n={r["n"]}]'


# ------------------------------------------------------------------ objects, faces, lines
def build_objects():
    raw = pd.read_csv(DATA, dtype=str).fillna('')
    raw['obj'] = raw.id.str.split('.').str[0]
    raw['fno'] = raw.id.str.split('.').str[1].astype(int)
    objs = {}
    for o, g in raw.groupby('obj'):
        g = g.sort_values('fno')
        faces = []
        for _, r in g.iterrows():
            t = r.text.strip()
            broken = '[' in t or ']' in t
            t = t.strip('+[]')
            chunks = t.split('/')
            lines = []
            for ch in chunks[::-1]:
                toks = [a for a in ch.replace('[', '').replace(']', '').split('-') if a][::-1]
                lines.append(toks)
            faces.append(dict(id=r.id, lines=lines, broken=broken, dir=r['dir.'], face_type=r.type))
        r0 = g.iloc[0]
        objs[o] = dict(obj=o, cisi=r0.cisi, site=r0.site, type=r0.type, area=r0['area-section'], block=r0['block-house'], depth=r0.depth,
                       material=r0.material, animal=r0.symbol, faces=faces, h=r0['horizontal(mm)'], v=r0['vertical(mm)'])
    return objs


def obj_signature(ob):
    return tuple(tuple(tuple(l) for l in f['lines']) for f in ob['faces'])


def n_legible(ob):
    return sum(1 for f in ob['faces'] for l in f['lines'] for s in l if s != '000')


def n_total(ob):
    return sum(len(l) for f in ob['faces'] for l in f['lines'])


# ------------------------------------------------------------------ phrase segmentation
def segment(x, soft=False):
    """Cut a line (tuple of signs in reading order) into phrases.  Returns list of (start, end) half-open."""
    n = len(x); cuts = set()
    # carrier phrase: [A-comb or count] [806] [carrier]
    i = 0
    while i < n:
        s = x[i]
        # load tag closes after the carrier
        if s in CARRIED and i >= 2 and x[i - 1] == '806' and (x[i - 2] in A_VARIANTS or x[i - 2] in CNT or x[i - 2] == '000'):
            cuts.add(i + 1); cuts.add(i - 2)
        if s == '740':
            j = i + 1
            while j < n and x[j] in RELATION and not (x[j] == '001' and j + 1 < n and x[j + 1] in CNT):
                # a relation noun directly after the jar (man, comb, table-X, ...); one stroke only if it ends the line
                if x[j] == '001' and j + 1 < n: break
                j += 1
                if j - (i + 1) >= 2: break
            cuts.add(j)
            i = j; continue
        if s == '520':
            cuts.add(i + 1)
        if s in PORTER and not (i >= 2 and x[i - 1] == '806'):
            cuts.add(i + 1)
        i += 1
    # openers: diamond/wheel at a phrase start, cap X-060
    for i in range(1, n):
        if x[i] in OPEN_SIGNS and (i + 1 >= n or True):
            # an opener inside a name (a wheel as 'self') is not a boundary unless preceded by a closer cut already, or text-medial after jar
            pass
        if x[i] == '060' and x[i - 1] in CAP_HEADS and i - 1 > 0:
            cuts.add(i - 1)
    cuts = sorted(c for c in cuts if 0 < c < n)
    bounds = [0] + cuts + [n]
    hard = [(a, b) for a, b in zip(bounds, bounds[1:]) if b > a]
    if not soft: return hard
    out = []
    for a, b in hard:
        out += soft_split(x, a, b)
    return out


def soft_split(x, a, b):
    """Cut a long run (>=7 signs) at the edges of recurring corpus units (>=3 signs in >=3 lines) and before a count run
    that follows a name part and precedes its counted thing."""
    if b - a < 7: return [(a, b)]
    from long_cohesion import ngram_units
    seg = x[a:b]; cs = set()
    for k, g, c in ngram_units(seg):
        if len(g) >= 3:
            if k > 0: cs.add(k)
            if k + len(g) < len(seg): cs.add(k + len(g))
    for i in range(2, len(seg) - 1):
        if seg[i] in CNT and seg[i - 1] not in CNT and seg[i + 1] not in CNT and seg[i + 1] != '740' and seg[i - 1] != '740' and CNT[seg[i]][0] != 'comb':
            if seg[i - 1] in FISH: continue
            cs.add(i)
    cs = sorted(c for c in cs if 1 < c < len(seg) - 1 or (c == 1 and False))
    bd = [0] + cs + [len(seg)]
    pieces = [(a + p, a + q) for p, q in zip(bd, bd[1:]) if q > p]
    # merge 1-sign pieces into the following piece
    m = []
    for pc in pieces:
        if m and (m[-1][1] - m[-1][0] == 1): m[-1] = (m[-1][0], pc[1])
        else: m.append(pc)
    return m


def phrase_kind(x, P):
    """Label a phrase from its parse."""
    R = P['roles']; has = lambda r: r in R
    if has('load-count'): return 'account line (load tag: n loads of crop, carried)'
    nm = P['names']
    if len(x) <= 2 and has('opener') and not nm: return 'opening formula'
    if has('opener') and set(R) <= {'opener'}: return 'opening formula'
    if has('poss'):
        rel = P['relation']
        if rel == '090': return 'agent phrase ("X, manager of the house")'
        if rel == '400': return 'junior phrase ("X, junior")'
        if rel == '679': return 'seat phrase ("seat of X")'
        if rel: return f'owner phrase with relation sign {rel}'
        return 'owner phrase ("of X")'
    if has('ending'):
        e = P['relation']
        return {'520': 'title phrase (X the chief)', '400': 'title phrase (X the junior)', '090': 'title phrase (X the manager)'}.get(e, 'title phrase (X the keeper)')
    if (has('count') or has('counted')) and not any(r in ('self', 'crest', 'tag', 'lost') for r in R): return 'account line (counted things)'
    if has('count') or has('counted'): return 'account line with name'
    if nm: return 'name (bare, no closer)'
    return 'fragment'


# ------------------------------------------------------------------ reading
def word_en(s, role=None):
    n = num_of(s)
    if n is not None: return WORDS[n] if n < len(WORDS) else str(n)
    g = gloss_en(s)
    if g and snd(s): return g.split(',')[0].split('(')[0].strip()
    return None


def read_phrase(x, P):
    """(sound string, English string) for one phrase; unvalued signs appear as <slot>."""
    R = list(P['roles']); n = len(x)
    sounds = []; eng = []
    for s in x:
        if s in CNT and CNT[s][0] == 'comb': sounds.append('(n)')
        elif s == '806': sounds.append('(crop)')
        elif snd(s): sounds.append(snd(s))
        else: sounds.append('‹?›')
    # English by role
    i = 0
    FISHSET = FISH
    for q in range(n - 1):
        if R[q] == 'count' and R[q + 1] == 'counted' and x[q + 1] in FISHSET: R[q] = R[q + 1] = 'self'
    while i < n:
        s, r = x[i], R[i]
        if r == 'opener':
            j = i
            while j + 1 < n and R[j + 1] == 'opener': j += 1
            blk = x[i:j + 1]
            if blk[0] in ('861', '817', '820'):
                v = num_of(blk[1]) if len(blk) > 1 else None
                unit = ('share', 'kāṇi') if blk[0] != '820' else ('quarter', 'kāl')
                eng.append(f'{WORDS[v] if v else "a"} {unit[0]}{"s" if v and v > 1 else ""} ({unit[1]}):')
            else:
                sel = [b for b in blk if b in CAP_SEL]
                head = {'920': 'month', '692': 'X-office', '550': 'Gate', '820': 'quarter'}.get(blk[0], 'opening')
                eng.append(f'[{head}-060 opening' + (', ' + {"741": "first", "742": "second", "745": "third"}[sel[0]] + ' ward' if sel else '') + ']:')
            i = j + 1; continue
        if r == 'load-count':
            eng.append(f'n loads of crop, carried'); i += 3; continue
        if r == 'count' and i + 1 < n and R[i + 1] == 'counted':
            j = i
            while j + 1 < n and R[j + 1] == 'count': j += 1
            v = sum(num_of(x[q]) or 0 for q in range(i, j + 1)) if all(num_of(x[q]) for q in range(i, j + 1)) else None
            thing = word_en(x[j + 1]) or f'<{slot_desc(x[j + 1]).split(" [")[0]}>'
            eng.append(f'{WORDS[v] if v and v < 9 else "n"} {thing}'); i = j + 2; continue
        if r in ('crest', 'self', 'tag', 'lost'):
            j = i
            while j + 1 < n and R[j + 1] in ('crest', 'self', 'tag', 'lost', 'count', 'counted') and not (R[j + 1] in ('count', 'counted') and x[j + 1] not in FISH and False): j += 1
            grp = [(x[q], R[q]) for q in range(i, j + 1)]
            parts = []
            for a, role in grp:
                w = word_en(a)
                parts.append(w.replace(' ', '-').capitalize() if w else ('<' + slot_desc(a).split(' [')[0] + '>' if a != '000' else '<lost>'))
            nm = '-'.join(parts)
            if j + 1 < n and R[j + 1] == 'poss':
                k = j + 2; rel = []
                while k < n and R[k] == 'relation': rel.append(RELNAME.get(x[k], word_en(x[k]) or f'<{slot_desc(x[k]).split(" [")[0]}>')); k += 1
                eng.append((' '.join(rel) + ' of ' if rel else 'of ') + f'the {nm} house'); i = k; continue
            if j + 1 < n and R[j + 1] == 'ending':
                eng.append(f'{nm}, the {ENDNAME.get(x[j + 1], word_en(x[j + 1]))}'); i = j + 2; continue
            eng.append(nm); i = j + 1; continue
        if r == 'poss': eng.append('of the house'); i += 1; continue
        if r == 'ending': eng.append(ENDNAME.get(s, word_en(s) or '?')); i += 1; continue
        if r == 'relation': eng.append(RELNAME.get(s, word_en(s) or '?')); i += 1; continue
        if r == 'count': eng.append(str(num_of(s))); i += 1; continue
        eng.append(word_en(s) or f'<{slot_desc(s).split(" [")[0]}>'); i += 1
    return ' '.join(sounds), ' '.join(eng)


# ------------------------------------------------------------------ sense scoring
def name_class_pattern(nm):
    return tuple(CLASS.get(a, '?') if snd(a) else 'U' for a in nm)


ORDER_EARLY = {'HOUSE'}; ORDER_LATE = {'KIN', 'TITLE'}


def order_breaks(nm):
    """Adjacent pairs inside a name where a kin/title word precedes a house word (head-last order broken)."""
    out = []
    for a, b in zip(nm, nm[1:]):
        if CLASS.get(a) in ORDER_LATE and CLASS.get(b) in ORDER_EARLY and snd(a) and snd(b): out.append((a, b))
    return out


_lex = None


def get_lex():
    global _lex
    if _lex is None:
        d = load2(); _lex = (learn(d), d)
    return _lex


def parse_phrase(x):
    lex, _ = get_lex()
    return parse_face(tuple(x), lex)
