#!/usr/bin/env python3
"""Second reading of EVERY inscription of the Lipi catalogue (5,679 faces): corpus_build.py plus slot rules, count attachment by
stroke style, spelled numbers inside names, and one record per multi-face object.
Writes work_data/corpus_english2.csv (one row per face + object record), work_data/odd/object_records.csv and CORPUS.md.
Values: work_data/values_master2.csv (values_master.csv + four slot-word columns, written by odd_4_values.py).

NEW RULES (on top of rules 0-10 listed at the top of corpus_build.py)
 S1 SLOT WORDS. A sign has up to four English words: short (default), short_name (inside a name), short_count (in a count line on
    goods), short_final (text-final title after a name), short_open (at the front). The slot decides the word.
 S2 COUNT ATTACHMENT BY STROKE STYLE. A run of strokes sitting between two signs goes to the neighbour that, by its own record
    over all runs of both catalogues, takes that style on that side:
    short and stacked strokes precede the counted thing, tall strokes follow a measure sign (kalam, share, pair) and precede a
    counted container (cup, chest). Adjacency counts are taken over both catalogues; ties go to the stroke-style default.
 S3 SPELLED NUMBER IN A NAME. Inside a name phrase (one ending in the jar or a closing sign) a number beside a name-word sign is part
    of a spelled word, not a count: Two-High-star, Peer-Two, One-King. Measure words keep their count (three kalam chief).
    The keeper signs counted on a seal are a title spelled with the number (Three-keeper); counted on goods they are porters.
 S4 060 away from the openers is Inner- (uḷ 'inner'); between two numbers it is 'within'. 368 text-final after a name = standard-bearer.
    824 at the front before a stroke is an opener (worth two). Ward signs 741-745 inside a name are First-/Second-/Third-ward.
 S5 OBJECT RECORD. Faces of one object are joined: who (house/person) + what (goods words) + amount (counts with a measure), written as
    one sentence per object.
GRADES as in corpus_build.py (values_master2.csv has the same strict/wide/testing/paused statuses; 152 is the one sign added).
Run: python3 corpus_build2.py   (about a minute; progress prints as it goes)"""
import sys, os, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound_v4_common import d, M as MAH, lex, parse_face, CNT
from gloss2 import WORDS
from gloss import A_VARIANTS
import pandas as pd

ROOT = '/home/antigravity/Cuuper22/ivc'
V = pd.read_csv(f'{ROOT}/work_data/values_master2.csv', dtype=str).fillna('')
READ = {s for s, st in zip(V.sign, V.status) if st in ('strict', 'wide')}
STRICT = {s for s, st in zip(V.sign, V.status) if st == 'strict'}
SHORT = dict(zip(V.sign, V.short)); SOUND = dict(zip(V.sign, V.sound))
SW = {slot: {s: w for s, w in zip(V.sign, V[col]) if w} for slot, col in (('name', 'short_name'), ('count', 'short_count'), ('final', 'short_final'), ('open', 'short_open'))}
SELECTOR = {'741': 'first ward', '742': 'second ward', '745': 'third ward'}
FISH = {'220', '226', '231', '233', '235', '236', '240', '241'}
KEEPERS = {'151', '152', '153', '154', '155', '156', '157', '158'}
UNITS = {'kalam', 'dozen', 'n loads', 'two months'}
CONTAINERS = {'700'}      # counted containers: tall strokes before them are their count even after a measure sign
MEASURE_KEEP = {'705', '706', '700', '320', '575', '540', '171', '711', '061', '480', '817', '820', '861', '176', '175'}   # counts stay counts in names
KIND = {'seal': 'seal', 'mtab': 'tablet', 'ctab': 'copper tablet', 'tag': 'tag or sealing', 'pot': 'pot', 'tool': 'tool', 'bangle': 'bangle', 'rod': 'rod', 'other': 'other'}
def damaged(x, flg): return '000' in x or 'ALT' in x or bool(flg & {'broken', 'lost', 'alt'})
def cap(w): return w[:1].upper() + w[1:]
def stype(s):
    sr = CNT[s][0]
    return 't' if sr == 'tall' else 's' if sr in ('short', 'stacked') else 'c'

# ---------- S2: edge statistics for count attachment (both catalogues; unambiguous runs only) ----------
EDGE_BEFORE = collections.defaultdict(collections.Counter)   # sign -> style -> runs standing first in the text right before it
EDGE_AFTER = collections.defaultdict(collections.Counter)    # sign -> style -> runs standing last in the text right after it
def _edge_fit():
    """adjacency counts over every run in both catalogues: EDGE_AFTER[t][style] = runs standing right after t, EDGE_BEFORE[t][style] = right before t.
    (Each run adds one to each neighbour; the noise is the same on both sides, the real preference shows through.)"""
    toks = list(d.tok) + list(MAH[~MAH.partnered].tok)
    for x in toks:
        n = len(x); i = 0
        while i < n:
            if x[i] in CNT:
                j = i
                while j + 1 < n and x[j + 1] in CNT: j += 1
                if not any(a in CNT and CNT[a][0] == 'comb' for a in x[i:j + 1]):
                    if i > 0 and x[i - 1] not in CNT and x[i - 1] not in ('000', 'ALT'): EDGE_AFTER[x[i - 1]][stype(x[i])] += 1
                    if j + 1 < n and x[j + 1] not in CNT and x[j + 1] not in ('000', 'ALT'): EDGE_BEFORE[x[j + 1]][stype(x[j])] += 1
                i = j + 1
            else: i += 1
_edge_fit()
_GA = collections.Counter(); _GB = collections.Counter()
for t in EDGE_AFTER: _GA.update(EDGE_AFTER[t])
for t in EDGE_BEFORE: _GB.update(EDGE_BEFORE[t])
def p_after(t, st):
    """probability that a run of style st next to sign t stands AFTER it (t then count) rather than before it, smoothed to the style's global rate"""
    ga = (_GA[st] + 1) / (_GA[st] + _GB[st] + 2)
    a, b = EDGE_AFTER[t][st], EDGE_BEFORE[t][st]
    return (a + 2 * ga) / (a + b + 2)

def side_choice(Lsign, Rsign, st_first, st_last):
    """-> 'L' or 'R'. Left neighbour takes the run if it tends to have counts after it; right neighbour takes it if it tends to have counts before it."""
    sL = p_after(Lsign, st_first); sR = 1 - p_after(Rsign, st_last)
    nL = EDGE_AFTER[Lsign][st_first] + EDGE_BEFORE[Lsign][st_first]; nR = EDGE_AFTER[Rsign][st_last] + EDGE_BEFORE[Rsign][st_last]
    if sL >= 0.8 and sR >= 0.8 and nL >= 6 and nR >= 6: return 'R' if Rsign in CONTAINERS else 'L'        # [measure] [tall count] [container]: the count belongs to the container (three cups), the measure stays a header
    if abs(sL - sR) < 1e-9: return 'R' if st_last == 's' else 'L'     # tie: short precede the thing, tall follow the measure
    return 'L' if sL > sR else 'R'

def reattach(x, R):
    """S2: re-decide which neighbour each count run belongs to. Returns a new roles list."""
    R = list(R); n = len(x); i = 0; runs = []
    while i < n:
        if R[i] == 'count' and x[i] in CNT:
            j = i
            while j + 1 < n and R[j + 1] == 'count' and x[j + 1] in CNT: j += 1
            runs.append((i, j)); i = j + 1
        else: i += 1
    ok = ('counted', 'self', 'crest', 'tag', 'ending')
    def cand(p): return 0 <= p < n and x[p] not in CNT and x[p] not in ('000', 'ALT', '741', '742', '745') and R[p] in ok
    for (i, j) in runs:
        for p in (i - 1, j + 1):
            if 0 <= p < n and R[p] == 'counted':
                R[p] = 'poss' if x[p] == '740' else 'self'
                if x[p] == '740' and p + 1 < n and R[p + 1] == 'ending': R[p + 1] = 'relation'
    taken = {}      # position -> side of the run that owns it ('left' = the run stands left of the thing)
    for (i, j) in runs:
        if any(a in CNT and CNT[a][0] == 'comb' for a in x[i:j + 1]): continue
        L = i - 1 if cand(i - 1) and taken.get(i - 1, 'left') == 'left' and (R[i - 1] != 'counted' or taken.get(i - 1) == 'left') else None
        Rr = j + 1 if cand(j + 1) and (R[j + 1] != 'counted') else None
        if L is not None and R[L] == 'counted' and taken.get(L) != 'left': L = None
        if L is None and Rr is None: continue
        if L is not None and Rr is not None: ch = side_choice(x[L], x[Rr], stype(x[i]), stype(x[j]))
        else: ch = 'L' if L is not None else 'R'
        p = L if ch == 'L' else Rr
        R[p] = 'counted'; taken[p] = 'left' if ch == 'R' else 'right'
    return R

# ---------- words ----------
def eng(s, slot=None, selector=False):
    if s == '000': return '[lost sign]'
    if s == 'ALT': return '[unclear sign]'
    if selector and s in SELECTOR: return SELECTOR[s]
    if s not in READ: return f'[{s}]'
    if slot and s in SW.get(slot, {}): return SW[slot][s]
    return SHORT[s]
def numword(v): return WORDS[v] if v is not None and v < len(WORDS) else ('n' if v is None else str(v))
def countvalue(x, idx):
    tot = 0
    for q in idx:
        ser, v = CNT[x[q]]
        if ser == 'comb': return None
        tot += v
    return tot
def plural(w):
    if w[:1].islower() and w not in UNITS and not w.endswith('s') and not w.startswith('['): return w[:-1] + 'ies' if w.endswith('y') else w + 's'
    return w

def np_piece(x, cidx, thing, order, kind):
    """a count phrase as a dict; resolved to text later (counted: 'three kalam'; spelled inside a name: 'Two-Star')"""
    return dict(x=x, cidx=cidx, thing=thing, order=order, kind=kind, v=countvalue(x, cidx), v2=None)
def np_count_text(pc):
    v, t = pc['v'], pc['thing']
    w = eng(t, 'count')
    if t in KEEPERS and pc['kind'] != 'seal': w = SW['count'].get(t, 'porter')
    num = numword(v)
    if pc['order'] == 'both':
        return f'{num} lot{"s" if (v or 0) > 1 else ""} of {numword(pc["v2"])} {plural(w) if (pc["v2"] or 0) > 1 else w}'
    if v is not None and v > 1: w = plural(w)
    return f'{num} {w}'
def np_spelled_text(pc):
    t = pc['thing']; num = cap(numword(pc['v']))
    nw = cap(eng(t, 'name'))
    if t == '060' and pc['order'] == 'both': return f'{num}-within-{cap(numword(pc["v2"]))}'
    if pc['order'] == 'both': return f'{num}-{nw}-{cap(numword(pc["v2"]))}'
    if t in KEEPERS: nw = nw.lower()
    return f'{num}-{nw}' if pc['order'] == 'before' else f'{nw}-{num}'

def name_tokens(x, idx, R, kind, slot='name'):
    toks = []
    idx = list(idx)
    for q in idx:
        s = x[q]
        if s == '390' and toks and q - 1 in idx and x[q - 1] == '590' and slot == 'name':
            toks[-1] = 'Boxed-cotton'; continue                                     # 590-390 = the house name Boxed-cotton
        if s in ('752', '760'):
            if toks: toks[-1] = 'child of ' + toks[-1]
            else: toks.append('Child of')
        else: toks.append(cap(eng(s, slot)))
    return '-'.join(toks).replace('Child of-', 'Child of ').replace('-child of ', ' child of ')

def build(x, r, kind):
    """-> (english, parts) ; parts = list of (role, text) with role in who / what / amount / open"""
    R = list(r['roles']); n = len(x)
    if n >= 2 and x[0] == '824' and x[1] in CNT and kind == 'seal':          # S4: 824 before strokes at the front works like the share openers
        R[0] = 'opener'
        q = 1
        while q < n and x[q] in CNT: R[q] = 'opener'; q += 1
    if n >= 2 and x[-1] == '368' and kind == 'seal' and R[-1] in ('self', 'crest', 'tag') and x[-2] not in CNT and R[-2] in ('self', 'crest', 'tag', 'counted'):
        R[-1] = 'ending'                                                      # S4: 368 text-final after a name = standard-bearer
    R = reattach(x, R); seg = []; k = 0
    last_free = max([q for q in range(n) if R[q] not in ('opener',)] or [-1])
    while k < n:
        ro = R[k]
        if ro == 'opener':
            j = k
            while j < n and R[j] == 'opener': j += 1
            idx = list(range(k, j)); cnt = [q for q in idx if x[q] in CNT]; wd = [q for q in idx if x[q] not in CNT]
            if '060' in [x[q] for q in idx]:
                p = [x[q] for q in idx].index('060')
                head = [eng(x[q], 'count') for q in idx[:p] if x[q] not in CNT]; sel = [eng(x[q], None, True) for q in idx[p + 1:] if x[q] not in CNT]
                txt = ' '.join(head) + ' in ' + ' '.join(sel) if sel else ' '.join(head)
                if cnt and wd: txt = count_open(x, cnt, x[wd[0]]) + ' ' + txt
            elif cnt and wd: txt = count_open(x, cnt, x[wd[0]]) + (' ' + ' '.join(eng(x[q]) for q in wd[1:]) if len(wd) > 1 else '')
            else: txt = ' '.join(eng(x[q], 'count') for q in wd)
            seg.append(('open', txt)); k = j
        elif ro in ('crest', 'self', 'tag', 'lost'):
            j = k
            while j < n and R[j] in ('crest', 'self', 'tag', 'lost'): j += 1
            seg.append(('name', (k, j))); k = j
        elif ro in ('count', 'counted'):
            if ro == 'counted':
                j = k + 1
                while j < n and R[j] == 'count': j += 1
                cidx = list(range(k + 1, j))
                seg.append(('np', np_piece(x, cidx, x[k], 'after', kind)) if cidx else ('name', (k, k + 1))); k = j
            else:
                j = k
                while j < n and R[j] == 'count': j += 1
                cidx = list(range(k, j))
                if j < n and R[j] == 'counted':
                    j2 = j + 1
                    while j2 < n and R[j2] == 'count': j2 += 1       # a second run after the same thing: join (n thing m)
                    pc = np_piece(x, cidx, x[j], 'before', kind)
                    k = j + 1
                    if k < n and R[k] == 'count':                       # a second run after the same thing: n thing m
                        j2 = k
                        while j2 < n and R[j2] == 'count': j2 += 1
                        pc['v2'] = countvalue(x, list(range(k, j2))); pc['order'] = 'both'; k = j2
                    seg.append(('np', pc))
                else:
                    v = countvalue(x, cidx); seg.append(('bare', numword(v))); k = j
        elif ro == 'load-count':
            v = x[k]; c = 'n' if v in A_VARIANTS or v == '000' else WORDS[CNT[v][1]]
            seg.append(('load', f'{c} loads of {eng(x[k + 1], "count")}, carried by the {eng(x[k + 2], "count")}')); k += 3
        elif ro in ('load-crop', 'load-thing', 'load-carried'): k += 1
        elif ro == 'poss': seg.append(('poss', '')); k += 1
        elif ro == 'relation': seg.append(('rel', cap(eng(x[k], 'final')))); k += 1
        elif ro == 'ending': seg.append(('end', (k, eng(x[k], 'final')))); k += 1
        elif ro == 'tail': seg.append(('tail', eng(x[k], 'final'))); k += 1
        else: k += 1
    # keeper counted on a seal: a title (Three-keeper)
    # merge name / np pieces that sit right before a jar or an ending into one name phrase (S3)
    mg = []; i = 0
    def name_text(item, slot='name'):
        kd, v = item
        if kd == 'name':
            a, b = v; return name_tokens(x, range(a, b), R, kind, slot), 'tok'
        if kd == 'np':
            t = v['thing']
            if t in KEEPERS and kind == 'seal': return np_spelled_text(v), 'sp'
            if t in MEASURE_KEEP or v['v'] is None or t not in READ: return np_count_text(v), 'cnt'
            return np_spelled_text(v), 'sp'
        return v, 'tok'
    while i < len(seg):
        if seg[i][0] in ('name', 'np', 'bare'):
            j = i
            while j < len(seg) and seg[j][0] in ('name', 'np', 'bare'): j += 1
            if j < len(seg) and seg[j][0] in ('poss', 'end'):
                pieces = []
                for it in seg[i:j]:
                    if it[0] == 'bare': pieces.append((cap(it[1]), 'sp'))
                    else: pieces.append(name_text(it))
                txt = ''
                for q, (t, ty) in enumerate(pieces):
                    if q == 0: txt = t
                    else: txt += ('-' if ty != 'cnt' and pieces[q - 1][1] != 'cnt' else ' ') + t
                mg.append(('nm', txt))
            else:
                for it in seg[i:j]:
                    if it[0] == 'name': mg.append(('nmg' if kind != 'seal' else 'nm', name_text(it, 'count' if kind != 'seal' else 'name')[0]))
                    elif it[0] == 'bare': mg.append(('np', it[1]))
                    else:
                        v = it[1]
                        if v['thing'] in KEEPERS and kind == 'seal': mg.append(('nm', np_spelled_text(v)))
                        else: mg.append(('np', np_count_text(v)))
            i = j
        else:
            if seg[i][0] == 'end': mg.append(('end', seg[i][1][1]))
            else: mg.append(seg[i])
            i += 1
    out = []; parts = []; i = 0; opening = ''
    while i < len(mg):
        kd, t = mg[i]
        if kd == 'open': opening = t + ': '; i += 1
        elif kd == 'nm':
            if i + 1 < len(mg) and mg[i + 1][0] == 'poss':
                if i + 2 < len(mg) and mg[i + 2][0] == 'rel': s_ = f'{mg[i + 2][1]} of the {t} house'; i += 3
                else: s_ = f'Of the {t} house'; i += 2
                out.append(s_); parts.append(('who', s_))
            elif i + 1 < len(mg) and mg[i + 1][0] == 'end': s_ = f'{t}, {mg[i + 1][1]}'; out.append(s_); parts.append(('who', s_)); i += 2
            else: out.append(t); parts.append(('who', t)); i += 1
        elif kd == 'poss':
            if i + 1 < len(mg) and mg[i + 1][0] == 'rel': s_ = f'{mg[i + 1][1]} of the house'; i += 2
            else: s_ = 'Of the house'; i += 1
            out.append(s_); parts.append(('who', s_))
        elif kd == 'nmg': out.append(t); parts.append(('what', t)); i += 1
        elif kd in ('np', 'load'): out.append(cap(t)); parts.append(('amount', cap(t))); i += 1
        elif kd in ('rel', 'end', 'tail'): out.append(cap(t)); parts.append(('what', cap(t))); i += 1
        else: i += 1
    # a name that stands alone with no count and no jar on goods = what
    txt = '; '.join(out)
    if opening: txt = opening + (txt[:1].lower() + txt[1:] if txt and re.match(r'^(\w+ )?[Oo]f the ', txt) else txt)
    return (txt or '(nothing)').rstrip(': ') + '.', parts, opening

def count_open(x, cnt, w):
    v = countvalue(x, cnt); num = numword(v)
    word = eng(w, 'open') if w in SW['open'] else eng(w, 'count')
    if w in SW['open'] and w == '824': return f'{word} {num}'
    if v is not None and v > 1: word = plural(word)
    return f'{num} {word}'

def record_sentence(who, what, amt, opens):
    """S5: one sentence for a whole object from its who / what / amount parts"""
    def for_who(w):
        w = re.sub(r'^Of the ', 'the ', w)
        if re.match(r'^[A-Z][\w-]* of the ', w): w = 'the ' + w[:1].lower() + w[1:]
        return w
    wh = ' and '.join(for_who(w) if i == 0 or True else w for i, w in enumerate(who))
    wt = ', '.join(w.replace('-', ' ').lower() if '-' in w and ' ' not in w else w.lower() for w in what)
    am = ' and '.join(a.lower() if i else a for i, a in enumerate(amt))
    op = (', '.join(opens) + ' ') if opens else ''
    if amt:
        s_ = am + (f' of {wt}' if wt else '')
        s_ += f', for {wh}' if wh else ''
    elif who:
        s_ = (op + wh).strip(); s_ = s_[:1].upper() + s_[1:]
        s_ += f': {wt}' if wt else ''
        return s_
    else: s_ = (op + wt).strip()
    return s_[:1].upper() + s_[1:]

def grade(x, flg, readset):
    if damaged(x, flg): return 'damaged'
    rd = [s in readset for s in x]
    if all(rd): return 'whole'
    return 'part' if any(rd) else 'none'

if __name__ == '__main__':
    print(f'[corpus_build2] {len(d)} faces; {len(READ)} signs read (strict {len(STRICT)}, wide {len(READ) - len(STRICT)}); adjacency fit: {sum(sum(c.values()) for c in EDGE_BEFORE.values())} runs before a sign, {sum(sum(c.values()) for c in EDGE_AFTER.values())} runs after a sign', flush=True)
    rows = []; PARTS = {}
    for n_, (i, x, flg, ty, site, kind) in enumerate(zip(d.id, d.tok, d.flg, d.type, d.site, d.kind)):
        r = parse_face(x, lex)
        eg, parts, opening = build(x, r, kind)
        rows.append(dict(face_id=i, object_id=i.split('.')[0], site=site, object_kind=KIND.get(kind, kind), signs='-'.join(x),
                         sounds=' '.join(SOUND.get(s, f'[{s}]') if s in READ else (f'[{s}]' if s not in ('000', 'ALT') else '[lost]') for s in x),
                         english=eg, grade=grade(x, flg, READ)))
        PARTS[i] = (parts, opening)
        if (n_ + 1) % 500 == 0: print(f'  ... {n_ + 1} of {len(d)} faces read', flush=True)
    out = pd.DataFrame(rows)
    # S5 object records
    recs = []
    for oid, g in out.groupby('object_id', sort=False):
        if len(g) < 2: continue
        who = []; what = []; amt = []; opens = []
        for fid in g.face_id:
            p, op = PARTS[fid]
            if op: opens.append(op.rstrip(': '))
            for role, t in p:
                (who if role == 'who' else amt if role == 'amount' else what).append(t.rstrip('.'))
        def uniq(L): return [t for q, t in enumerate(L) if t not in L[:q]]
        who, what, amt, opens = uniq(who), uniq(what), uniq(amt), uniq(opens)
        s_ = record_sentence(who, what, amt, opens)
        grades = list(g.grade)
        recs.append(dict(object_id=oid, object_kind=g.object_kind.iloc[0], site=g.site.iloc[0], faces=len(g), signs=' / '.join(g.signs),
                         record=(s_ or '(nothing)') + '.', grade='whole' if all(q == 'whole' for q in grades) else 'damaged' if any(q == 'damaged' for q in grades) else 'part' if any(q in ('whole', 'part') for q in grades) else 'none'))
    R = pd.DataFrame(recs); R.to_csv(f'{ROOT}/work_data/odd/object_records.csv', index=False)
    out.to_csv(f'{ROOT}/work_data/corpus_english2.csv', index=False)
    gc = out.grade.value_counts()
    print('GRADES (values_master2, strict+wide):', {k: int(gc.get(k, 0)) for k in ('whole', 'part', 'damaged', 'none')}, flush=True)
    print('OBJECT RECORDS (2+ faces):', len(R), dict(R.grade.value_counts()), flush=True)
