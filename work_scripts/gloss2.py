#!/usr/bin/env python3
"""Possessive-model glosser for Indus texts (second parser).

Reading order = stored order reversed.  A face is read as

  [opener] [name = crest + self + tag] [possessive jar 740] [relation noun]

with counts written before the thing counted ("n X"), load tags ("n loads of crop, carried"),
and multi-face tablets read as one record (one line per face).

Run:  python3 gloss2.py     -> work_data/gloss2_all.csv, work_data/gloss2_lexicon.txt, prints coverage
Import: from gloss2 import load2, learn, parse_face, sentence
"""
import sys, collections, os
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gloss import load, parse_row, OPENERS, COUNTS, A_VARIANTS, CAP_HEADS, CAP_SEL, lexicon_from, gloss_text, is_parsed

ROOT = '/home/claude/ivc'
SHAPES = f'{ROOT}/work_data/sign_shapes.csv'
RATES = f'{ROOT}/work_data/counted/owner_rates.csv'

# count signs -> (series, value)
CNT = {}
for i in range(1, 8): CNT[f'{i:03d}'] = ('short', i)
CNT['012'] = ('stacked', 2)
for i in range(13, 19): CNT[f'{i:03d}'] = ('stacked', i - 10)
for i in range(31, 37): CNT[f'{i:03d}'] = ('tall', i - 30)
for a in A_VARIANTS: CNT[a] = ('comb', 0)
CARRIED = {'154', '155', '158'}          # porter sign that follows a counted crop
RELATION = {'090', '400', '679', '621', '001', '565'}   # what can follow the possessive jar (see jobs/out/possessive_model.md)
ENDINGS = {'520', '090', '400', '151', '154', '155', '156', '158'}   # sign that can close a text with no jar
WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight']

NOUN = {
    '700': 'cup', '861': 'diamond', '817': 'diamond', '820': 'wheel', '156': 'porter', '154': 'porter', '158': 'porter',
    '155': 'porter', '151': 'porter', '153': 'porter', '806': 'crop', '803': 'leaf', '740': 'jar', '741': 'jar-dot', '742': 'jar-2dots',
    '745': 'jar-3dots', '090': 'man', '091': 'twin men', '400': 'comb', '520': 'spear', '679': 'table-X', '621': 'barred rectangle',
    '220': 'plain fish', '235': 'fish-hat', '240': 'whisker fish', '233': 'barred fish', '231': 'dotted fish', '226': 'caged fish',
    '760': 'branching-U', '100': 'three-headed person', '923': 'outline paren', '585': 'sign-585', '390': 'tree', '405': 'tree-405',
    '407': 'tree-407', '550': 'pincer', '555': 'pincer-555', '142': 'staff-bearer', '840': 'two-leaf', '705': 'U-with-stroke',
    '706': 'U-with-stroke-706', '176': 'seated person', '055': 'twelve-strokes', '798': 'leaf-pincer', '140': 'breasted person',
    '013': 'three-strokes-stack', '590': 'box', '017': 'seven-strokes', '060': 'ri-mark', '920': 'leaf-paren', '692': 'outline X',
    '125': 'bow-person', '061': 'reversed lambda', '900': 'paren', '415': 'pitchfork', '255': 'odd animal', '717': 'cat-paw',
    '460': 'three-peaks', '690': 'nested chevrons', '170': 'caged leaves', '095': 'stick-person', '097': 'bracketed person',
    '130': 'pitchfork-person', '100': 'three-headed person', '503': 'striped triangle', '575': 'trapezoid-box', '384': 'upside-down heart',
    '388': 'heart-bar', '416': 'double pitchfork', '001': 'stroke', '000': 'lost sign',
}
_shape = None


def shapes():
    global _shape
    if _shape is None:
        s = pd.read_csv(SHAPES, dtype=str)
        _shape = dict(zip(s.lipi_wells_number, s.shape_description))
    return _shape


def label(s):
    """Short plain-English name for a sign."""
    if s in NOUN: return NOUN[s]
    if s == 'ALT': return 'unclear sign'
    if s in CNT: return countlabel(s)
    d = shapes().get(s) or ''
    d = d.lower().split(',')[0].split(';')[0].split('.')[0]
    for w in ('simple ', 'classic '): d = d.replace(w, '')
    w = d.split()[:3]
    while w and w[-1] in ('with', 'a', 'of', 'the', 'on', 'in', 'and', 'or', 'at', 'to', 'an', 'no', 'one', 'two', 'bottom', 'small', 'where', 'two'): w.pop()
    d = ' '.join(w)
    return f'{d} ({s})' if d else f'sign {s}'


def countlabel(s):
    ser, v = CNT[s]
    return 'n' if ser == 'comb' else str(v)


def plural(noun, n):
    if n == 1 or noun.endswith(('fish', 'wheel-s')) or '(' in noun or noun.startswith('sign '): return noun
    if noun.endswith(('x', 's')): return noun + 'es'
    if noun.endswith(('man',)) and noun.split()[-1] == 'man': return noun[:-3] + 'men'
    return noun + 's'


def learn(d):
    """Learn owner rates and name-slot roles from distinct complete texts."""
    rates = pd.read_csv(RATES, dtype={'sign': str})
    occ = dict(zip(rates.sign, rates.occ))
    before = dict(zip(rates.sign, rates.owned_before))
    after = dict(zip(rates.sign, rates.owned_after))
    texts = []
    seen = set()
    for x, c in zip(d.tok, d.complete_txt):
        if c and x not in seen: seen.add(x); texts.append(x)
    names = []
    for x in texts:
        r = parse_face(x, None, (occ, before, after))
        if r['name'] and r['ending_kind'] != 'none': names.append(r['name'])
    first = collections.Counter(); last = collections.Counter(); mult = collections.Counter()
    for nm in names:
        if len(nm) >= 2:
            first[nm[0]] += 1; last[nm[-1]] += 1
            for s in nm: mult[s] += 1
    crest = {s for s, k in first.items() if k >= 8 and k / mult[s] >= 0.4 and k > last[s]}
    tag = {s for s, k in last.items() if k >= 8 and k / mult[s] >= 0.4 and k > first[s]}
    crest |= {'231', '233', '235', '240'}     # marked fish signs: house crests (jobs/out/name_slot.md)
    tag.discard('231'); tag.discard('233'); tag.discard('235'); tag.discard('240')
    both = crest & tag
    for s in both:
        (crest if first[s] >= last[s] else tag).discard(s)
    return dict(owner=(occ, before, after), crest=crest, tag=tag, first=first, last=last, mult=mult, texts=texts)


def owner_side(L, R, own):
    occ, before, after = own
    a = (after.get(L, 0) + .05) / (occ.get(L, 0) + 1)
    b = (before.get(R, 0) + .05) / (occ.get(R, 0) + 1)
    return 'L' if a > b else 'R'


def parse_face(x, lex, own=None):
    """x: tuple of signs in reading order. Returns dict of roles and slots."""
    own = own or lex['owner']
    crest = lex['crest'] if lex else set()
    tag = lex['tag'] if lex else set()
    n = len(x)
    R = [None] * n
    # 1. head formula / cap (alternative opener)
    for i in range(n - 1):
        if x[i + 1] == '060' and x[i] in CAP_HEADS and R[i] is None:
            R[i] = R[i + 1] = 'opener'
            if i + 2 < n and x[i + 2] in CAP_SEL: R[i + 2] = 'opener'
    for i in range(n):
        if x[i] == '060' and R[i] is None and i == 0: R[i] = 'opener'
    # 2. load tag: [count A-comb or lost][thing][carried]
    for i in range(2, n):
        if x[i] in CARRIED and R[i] is None and R[i - 1] is None and R[i - 2] is None:
            if x[i - 2] in A_VARIANTS or x[i - 2] == '000' or (x[i - 2] in CNT and x[i - 1] == '806'):
                R[i - 2], R[i - 1], R[i] = 'load-count', 'load-crop' if x[i - 1] == '806' else 'load-thing', 'load-carried'
    # 3. opener: diamond / wheel (+ strokes) at the front
    p = 0
    while p < n and R[p] == 'opener': p += 1
    if p < n and x[p] in OPENERS and R[p] is None:
        R[p] = 'opener'
        if p + 1 < n and x[p + 1] in CNT and R[p + 1] is None: R[p + 1] = 'opener'
    # 4. counts and what they count
    i = 0
    while i < n:
        if x[i] in CNT and R[i] is None:
            j = i
            while j + 1 < n and x[j + 1] in CNT and R[j + 1] is None: j += 1
            Li = i - 1 if i > 0 and R[i - 1] is None and x[i - 1] not in CNT and x[i - 1] not in ('000', 'ALT') else None
            Ri = j + 1 if j + 1 < n and R[j + 1] is None and x[j + 1] not in CNT and x[j + 1] not in ('000', 'ALT') else None
            if Li is not None and Ri is not None: side = owner_side(x[Li], x[Ri], own)
            elif Ri is not None: side = 'R'
            elif Li is not None: side = 'L'
            else: side = None
            for k in range(i, j + 1): R[k] = 'count'
            if side == 'R': R[Ri] = 'counted'
            elif side == 'L': R[Li] = 'counted'
            i = j + 1
        else: i += 1
    # 5. jar and what follows
    jars = [i for i in range(n) if x[i] == '740' and R[i] is None]
    ending_kind = 'none'; rel = None
    if jars:
        for k, j in enumerate(jars):
            R[j] = 'poss'
        ending_kind = 'poss'
        lastj = jars[-1]
        rest = [i for i in range(lastj + 1, n) if R[i] is None]
        # relation noun = first free sign after the final jar; the rest is tail
        for q, i in enumerate(rest):
            if q == 0: R[i] = 'relation'; rel = x[i]
            elif x[i] in RELATION and R[rest[q - 1]] == 'relation': R[i] = 'relation'; rel += '+' + x[i]
            else: R[i] = 'tail'
        # a free-sign run between two jars: a second name; keep as name
    else:
        # no jar: closing noun = last free sign if it is a known closer
        free = [i for i in range(n) if R[i] is None]
        if free and x[free[-1]] in ENDINGS:
            R[free[-1]] = 'ending'; ending_kind = 'ending'; rel = x[free[-1]]
    # 6. names = free signs, grouped by the jars that cut them; crest / self / tag inside each group
    groups = []; cur = []
    for i in range(n):
        if R[i] is None: cur.append(i)
        elif R[i] == 'poss':
            if cur: groups.append(cur)
            cur = []
        elif cur and R[i] in ('relation', 'ending', 'tail', 'count', 'counted', 'load-count', 'opener') and False: pass
    if cur: groups.append(cur)
    for g in groups:
        m = len(g)
        for q, i in enumerate(g):
            s_ = x[i]
            if s_ in ('000', 'ALT'): R[i] = 'lost'
            elif m == 1: R[i] = 'self'
            elif q == 0 and s_ in crest: R[i] = 'crest'
            elif q == m - 1 and s_ in tag: R[i] = 'tag'
            else: R[i] = 'self'
    # the name that owns the relation: group just before the final jar (or the only group)
    master = None
    if jars:
        for g in groups:
            if g and g[-1] < jars[-1] and g[-1] > (jars[-2] if len(jars) > 1 else -1): master = g
    elif groups: master = groups[0]
    nm_idx = master or []
    name = [x[i] for i in nm_idx]
    names = [[x[i] for i in g] for g in groups]
    return dict(roles=R, name=name, names=names, name_idx=nm_idx, ending_kind=ending_kind, relation=rel, jars=jars)


def is_tight(x, r, lex):
    """Every sign has a grammar role, every name has at most four signs (crest + two selves + tag at the most),
    at most two names (X of Y), no unexplained tail, and the text closes in a licensed way."""
    R = r['roles']
    if 'lost' in R or 'tail' in R: return False
    if any(len(g) > 4 for g in r['names']): return False
    if len(r['jars']) > 2: return False
    if r['jars'] or r['ending_kind'] == 'ending': return True
    if not r['names']: return True            # only counted phrases / load tag / opener
    return len(x) <= 4 or any(k in R for k in ('count', 'counted', 'load-count')) and len(r['names'][0]) <= 4   # bare name, or name beside a counted phrase


def is_strict(x, r):
    """Stricter: names at most three signs (crest + self + tag), one jar at most."""
    return is_tight(x, r, None) and all(len(g) <= 3 for g in r['names']) and len(r['jars']) <= 1


def old_style_tight(R):
    """Comparison with the first parser's rule: more than half the signs in template roles (opener, count, counted,
    poss, relation, ending, load, crest, tag) and at most two free 'self' signs."""
    tmpl = sum(1 for k in R if k in ('opener', 'count', 'counted', 'poss', 'relation', 'ending', 'load-count', 'load-crop',
                                     'load-thing', 'load-carried', 'crest', 'tag'))
    selfs = sum(1 for k in R if k == 'self')
    return 'lost' not in R and selfs <= 2 and tmpl * 2 > len(R)


def template(x, r):
    R = r['roles']; out = []
    k = 0
    while k < len(x):
        role = R[k]; j = k
        if role in ('crest', 'self', 'tag', 'lost'):
            while j + 1 < len(x) and R[j + 1] in ('crest', 'self', 'tag', 'lost'): j += 1
            out.append('NAME[' + '+'.join(R[q] for q in range(k, j + 1)) + ']')
        elif role in ('count', 'counted'):
            while j + 1 < len(x) and R[j + 1] in ('count', 'counted'): j += 1
            out.append('N-THING')
        elif role.startswith('load'):
            while j + 1 < len(x) and R[j + 1].startswith('load'): j += 1
            out.append('LOAD-TAG')
        else:
            while j + 1 < len(x) and R[j + 1] == role: j += 1
            out.append({'opener': 'OPENER', 'poss': 'POSS', 'relation': 'REL', 'ending': 'END', 'tail': 'TAIL'}[role])
        k = j + 1
    return ' '.join(out)


def runvalue(x, idx):
    """Count run -> (value or None, text)"""
    vals = []
    for q in idx:
        ser, v = CNT[x[q]]
        vals.append(None if ser == 'comb' else v)
    if None in vals: return None
    return sum(vals)


def np_phrase(x, R, k):
    """Return (phrase, next index) for a counted phrase starting at k."""
    cidx = []; j = k
    while j < len(x) and R[j] == 'count': cidx.append(j); j += 1
    if j < len(x) and R[j] == 'counted':
        v = runvalue(x, cidx); noun = label(x[j])
        if v is None: return f'several {plural(noun, 2)}', j + 1
        return f'{WORDS[v] if v < len(WORDS) else v} {plural(noun, v)}', j + 1
    return None, k


def sentence(x, r):
    """Plain English reading of one face."""
    R = r['roles']; n = len(x)
    parts = []; name_done = False; lead = []
    k = 0
    cur_name = []
    def flush_name():
        nonlocal cur_name
        if not cur_name: return ''
        s = ', '.join(cur_name); cur_name = []
        return '[' + s + ']'
    pieces = []     # (kind, text)
    while k < n:
        role = R[k]
        if role == 'opener':
            j = k
            while j < n and R[j] == 'opener': j += 1
            pieces.append(('open', ' '.join(label(x[q]) if x[q] not in CNT else countlabel(x[q]) for q in range(k, j)))); k = j
        elif role in ('crest', 'self', 'tag', 'lost'):
            lab = label(x[k])
            if role == 'crest': lab += ' crest'
            elif role == 'tag': lab += ' tag'
            elif role == 'lost': lab = 'lost sign'
            if pieces and pieces[-1][0] == 'name': pieces[-1] = ('name', pieces[-1][1] + [lab])
            else: pieces.append(('name', [lab]))
            k += 1
        elif role == 'count' or role == 'counted':
            if role == 'counted':      # "X n": count after the thing
                lab = label(x[k]); q = k + 1; cidx = []
                while q < n and R[q] == 'count': cidx.append(q); q += 1
                v = runvalue(x, cidx) if cidx else None
                pieces.append(('np', f'{lab}, {WORDS[v] if v is not None and v < 9 else "n"}')); k = q
            else:
                ph, nk = np_phrase(x, R, k)
                if ph is None:
                    j = k
                    while j < n and R[j] == 'count': j += 1
                    pieces.append(('np', 'count ' + str(runvalue(x, list(range(k, j))) or 'n'))); k = j
                else: pieces.append(('np', ph)); k = nk
        elif role == 'load-count':
            v = x[k]; cnt = 'n' if v in A_VARIANTS or v == '000' else countlabel(v)
            thing = label(x[k + 1])
            lead_n = 'n' if cnt == 'n' else WORDS[int(cnt)]
            pieces.append(('np', f'{lead_n} loads of {thing}, carried')); k += 3
        elif role == 'poss': pieces.append(('poss', '')); k += 1
        elif role == 'relation': pieces.append(('rel', label(x[k]) if x[k] != '001' else 'one stroke')); k += 1
        elif role == 'ending': pieces.append(('end', label(x[k]))); k += 1
        elif role == 'tail': pieces.append(('tail', label(x[k]))); k += 1
        else: k += 1
    # merge name pieces and counted phrases that sit in one run before a jar / ending into one bracketed name
    merged = []; i = 0
    while i < len(pieces):
        if pieces[i][0] in ('name', 'np'):
            j = i
            while j < len(pieces) and pieces[j][0] in ('name', 'np'): j += 1
            run = pieces[i:j]
            if j < len(pieces) and pieces[j][0] in ('poss', 'end') and any(k == 'name' or True for k, _ in run):
                items = []
                for k_, t_ in run: items += t_ if k_ == 'name' else [t_]
                merged.append(('name', items))
            else: merged += run
            i = j
        else: merged.append(pieces[i]); i += 1
    pieces = merged
    out = []; i = 0
    while i < len(pieces):
        kind, t = pieces[i]
        if kind == 'open': out.append(f'(opening: {t})'); i += 1
        elif kind == 'name':
            nm = '[' + ', '.join(t) + ']'
            if i + 1 < len(pieces) and pieces[i + 1][0] == 'poss':
                if i + 2 < len(pieces) and pieces[i + 2][0] == 'rel':
                    out.append(f"{nm}'s {pieces[i + 2][1]}."); i += 3
                else: out.append(f'Of {nm}.'); i += 2
            elif i + 1 < len(pieces) and pieces[i + 1][0] == 'end':
                out.append(f'{nm}, {pieces[i + 1][1]}.'); i += 2
            else: out.append(f'{nm}.'); i += 1
        elif kind == 'poss':      # jar with nothing before it
            if i + 1 < len(pieces) and pieces[i + 1][0] == 'rel': out.append(f"Of-ending, {pieces[i + 1][1]}."); i += 2
            else: out.append('Of-ending.'); i += 1
        elif kind == 'np': out.append(t[0].upper() + t[1:] + '.'); i += 1
        elif kind in ('rel', 'end', 'tail'): out.append(f'Then {t}.'); i += 1
        else: i += 1
    return ' '.join(out)


def load2():
    d = load()
    return d


def object_id(i): return str(i).split('.')[0]


def main():
    d = load2()
    lex = learn(d)
    own = lex['owner']
    res = []
    for x in d.tok:
        r = parse_face(x, lex, own)
        res.append(r)
    d['tight2'] = [is_tight(x, r, lex) for x, r in zip(d.tok, res)]
    d['strict2'] = [is_strict(x, r) for x, r in zip(d.tok, res)]
    d['old_style2'] = [old_style_tight(r['roles']) for r in res]
    d['template'] = [template(x, r) for x, r in zip(d.tok, res)]
    d['gloss'] = [sentence(x, r) for x, r in zip(d.tok, res)]
    d['roles2'] = [' '.join(r['roles']) for r in res]
    d['reading'] = ['-'.join(x) for x in d.tok]
    d['name'] = ['-'.join(r['name']) for r in res]
    d['ending'] = [r['ending_kind'] for r in res]
    d['relation'] = [r['relation'] or '' for r in res]
    d['obj'] = [object_id(i) for i in d['id']]
    # old parser for comparison
    lex1 = lexicon_from(d)
    TEMPLATE = {'opener', 'opener-strokes', 'count', 'amount', 'class', 'class-tail', 'house', 'title-phrase', 'cap', 'cap-selector'}
    def tight1(r):
        return ('unknown' not in r and r.count('who') <= 2 and sum(q in TEMPLATE or q in ('house-marker',) for q in r) >= 0.5 * len(r))
    d['tight1'] = [tight1(gloss_text(x, lex1, f)) for x, f in zip(d.tok, d.flg)]
    # tablet / multi-face records: faces of one object read together
    rec = {}
    for o, g in d.groupby('obj'):
        if len(g) > 1:
            rec[o] = ' | '.join(g.gloss)
    d['record'] = [rec.get(o, '') for o in d.obj]
    out = d[['id', 'obj', 'cisi', 'site', 'type', 'reading', 'template', 'name', 'ending', 'relation', 'gloss', 'record', 'tight2', 'strict2', 'old_style2']].copy()
    out.columns = ['id', 'object', 'cisi', 'site', 'type', 'reading_order_text', 'template', 'name_signs', 'ending_kind', 'relation_sign',
                   'gloss', 'multi_face_record', 'tight', 'strict', 'tight_old_rule']
    out.to_csv(f'{ROOT}/work_data/gloss2_all.csv', index=False)
    with open(f'{ROOT}/work_data/gloss2_lexicon.txt', 'w') as f:
        f.write('crest signs (first sign of multi-sign names): ' + ' '.join(sorted(lex['crest'])) + '\n')
        f.write('tag signs (last sign of multi-sign names): ' + ' '.join(sorted(lex['tag'])) + '\n')
    c = d[d.complete_txt].drop_duplicates('tok')
    print('distinct complete texts', len(c))
    print('strict (names<=3, one jar)', int(c.strict2.sum()), round(100*c.strict2.mean(),1)); print('gloss2 tight', int(c.tight2.sum()), round(100 * c.tight2.mean(), 1), '| same-rule-as-parser-1 on gloss2 roles', round(100 * c.old_style2.mean(), 1),
          '| parser 1 tight', int(c.tight1.sum()), round(100 * c.tight1.mean(), 1))
    for g, s in c.groupby('group'):
        print(g, len(s), round(100 * s.tight2.mean(), 1), round(100 * s.tight1.mean(), 1))
    print('crests', sorted(lex['crest'])); print('tags', sorted(lex['tag']))
    return d, lex


if __name__ == '__main__':
    main()
