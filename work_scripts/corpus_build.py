#!/usr/bin/env python3
"""Read EVERY inscription of the Lipi catalogue (5,679 faces) through the template parser (gloss2.parse_face) and the
master value table (work_data/values_master.csv); write work_data/corpus_english.csv and CORPUS.md (repo root).

HOW THE ENGLISH IS BUILT (rules; the same signs always give the same English)
 0. Each sign has one short English word: master column `short`. Signs with status strict or wide are READ. testing,
    paused and unvalued signs are UNREAD and are printed as [sign number]. A lost sign prints as [lost sign].
 1. The parser (gloss2.parse_face) gives every sign a slot: opener, count, counted, load-count / load-crop / load-carried,
    crest, self, tag (the three parts of a NAME, in that order), poss (the jar 740), relation, ending, tail.
 2. NAME = the name signs of one group, in slot order (crest first, personal part, tag last), joined by hyphens, first
    letter of each sign capital:  High-star-Bamboo-star-Tax.
    Child-of rule: the child-of sign (752/760) after a name sign gives "child of <that sign>"  (335 760 -> "Child of town").
 2b. STAR WORD (star_names.md): a number written right before a fish sign (220 226 231 233 235 236 240 241) INSIDE a name phrase
    (one that ends in a jar or an ending) is a spelled word, not a count: <Number>-<fish>, e.g. 002 220 740 -> "Of the Two-Star house".
    A face that is only number + fish is a name too. Outside a name (a goods count) it stays a count: "two stars".
 3. COUNT PHRASE = the count run (digits add up: 003 = three; the A-comb 465-475 = "n") placed BEFORE the thing counted,
    wherever the thing stands in the text:  705 033 -> "three kalam". Plural -s (-y becomes -ies) when the number is above one and the word is a
    plain lower-case noun (not a unit: kalam, dozen).
 4. LOAD TAG  [n][produce 806][keeper] = "n loads of produce, carried by the keeper".
 5. OPENER = head word(s) + joiner 060 + selector -> "<head> in <selector>" (741 742 745 as selector = first / second / third ward);
    opener words + count -> "<count> <word>".  An opener clause ends with a colon.
 6. A run of NAME and COUNT PHRASE pieces right before the jar or an ending is one name phrase (pieces joined by spaces).
 7. JAR 740 after a name phrase = "the <NAME> house"; a relation sign after the jar names who: "<Relation> of the <NAME> house"
    (man 090 = Manager, comb 400 = Junior, other signs by their short word).  Jar with nothing before it: "Of the house".
    Jar, no relation: "Of the <NAME> house".
 8. ENDING sign with no jar (spear 520, man 090, comb 400, keepers): "<NAME>, <ending>".
 9. A name alone: the NAME.  A count phrase alone: the count phrase.  Tail signs are printed in place after a semicolon.
10. Phrases are joined with "; " and the line ends with a full stop.
GRADES  (a face gets the first that fits)
 damaged : the face has a lost sign (000), an ambiguous sign (ALT) or a broken-edge mark in the catalogue
 whole   : every sign is READ (strict or wide value)
 part    : at least one sign READ and at least one UNREAD
 none    : no sign READ
Run: python3 corpus_build.py   (about a minute; progress prints as it goes)"""
import sys, os, re, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sound_v4_common import d, lex, parse_face, CNT          # d = all 5,679 Lipi faces (with object kind), parsed with the first-pass lexicon
from gloss2 import WORDS
from gloss import A_VARIANTS
import pandas as pd

ROOT = '/home/antigravity/Cuuper22/ivc'
M = pd.read_csv(f'{ROOT}/work_data/values_master.csv', dtype=str).fillna('')
MAS = M.set_index('sign')
READ = {s for s, st in zip(M.sign, M.status) if st in ('strict', 'wide')}
STRICT = {s for s, st in zip(M.sign, M.status) if st == 'strict'}
SHORT = dict(zip(M.sign, M.short)); SOUND = dict(zip(M.sign, M.sound))
SELECTOR = {'741': 'first ward', '742': 'second ward', '745': 'third ward'}
FISH = {'220', '226', '231', '233', '235', '236', '240', '241'}
UNITS = {'kalam', 'dozen', 'n loads'}
KIND = {'seal': 'seal', 'mtab': 'tablet', 'ctab': 'copper tablet', 'tag': 'tag or sealing', 'pot': 'pot', 'tool': 'tool', 'bangle': 'bangle', 'rod': 'rod', 'other': 'other'}
# kinds of damage
def damaged(x, flg): return '000' in x or 'ALT' in x or bool(flg & {'broken', 'lost', 'alt'})


def cap(w): return w[:1].upper() + w[1:]


def eng(s, selector=False):
    """short English of one sign, or [number] when unread."""
    if s in ('000',): return '[lost sign]'
    if s == 'ALT': return '[unclear sign]'
    if selector and s in SELECTOR: return SELECTOR[s]
    return SHORT[s] if s in READ else f'[{s}]'


def countvalue(x, idx):
    tot = 0
    for q in idx:
        ser, v = CNT[x[q]]
        if ser == 'comb': return None
        tot += v
    return tot


def count_phrase(x, idx, thing):
    v = countvalue(x, idx)
    w = eng(thing)
    if v is None: return f'n {w}'
    num = WORDS[v] if v < len(WORDS) else str(v)
    if v > 1 and w[:1].islower() and w not in UNITS and not w.endswith('s') and not w.startswith('['): w = w[:-1] + 'ies' if w.endswith('y') else w + 's'
    return f'{num} {w}'


def fuse(x, idx, thing):
    """count + thing; for a fish sign also carries the spelled-word form after a NUL (used only inside a name, rule 2b)."""
    t = count_phrase(x, idx, thing)
    v = countvalue(x, idx)
    if thing in FISH and v is not None:
        return t + '\x00' + cap(WORDS[v] if v < len(WORDS) else str(v)) + '-' + eng(thing)
    return t


def build(x, r):
    """-> English line for one face (rules above)."""
    R = r['roles']; n = len(x); seg = []; k = 0
    while k < n:
        ro = R[k]
        if ro == 'opener':
            j = k
            while j < n and R[j] == 'opener': j += 1
            idx = list(range(k, j)); cnt = [q for q in idx if x[q] in CNT]; wd = [q for q in idx if x[q] not in CNT]
            if '060' in [x[q] for q in idx]:
                p = [x[q] for q in idx].index('060')
                head = [eng(x[q]) for q in idx[:p] if x[q] not in CNT]; sel = [eng(x[q], True) for q in idx[p + 1:] if x[q] not in CNT]
                txt = ' '.join(head) + ' in ' + ' '.join(sel) if sel else ' '.join(head)
                if cnt: txt = count_phrase(x, cnt, x[wd[0]]) + ' ' + txt if wd else txt
            elif cnt and wd: txt = count_phrase(x, cnt, x[wd[0]]) + (' ' + ' '.join(eng(x[q]) for q in wd[1:]) if len(wd) > 1 else '')
            else: txt = ' '.join(eng(x[q]) for q in wd)
            seg.append(('open', txt)); k = j
        elif ro in ('crest', 'self', 'tag', 'lost'):
            j = k
            while j < n and R[j] in ('crest', 'self', 'tag', 'lost'): j += 1
            toks = []
            for q in range(k, j):
                if x[q] in ('752', '760') and toks: toks[-1] = 'child of ' + toks[-1]
                else: toks.append(cap(eng(x[q])) if x[q] not in ('752', '760') else 'Child of')
            seg.append(('name', '-'.join(toks).replace('Child of-', 'Child of ').replace('-child of ', ' child of '))); k = j
        elif ro in ('count', 'counted'):
            # a count run (count signs only) with the counted thing right after it, or right before it ("X n")
            if ro == 'counted':
                j = k + 1
                while j < n and R[j] == 'count': j += 1
                cidx = list(range(k + 1, j))
                seg.append(('np', fuse(x, cidx, x[k]) if cidx else eng(x[k]))); k = j
            else:
                j = k
                while j < n and R[j] == 'count': j += 1
                cidx = list(range(k, j))
                if j < n and R[j] == 'counted': seg.append(('np', fuse(x, cidx, x[j]))); k = j + 1
                else:
                    v = countvalue(x, cidx); seg.append(('np', WORDS[v] if v is not None and v < len(WORDS) else 'n')); k = j
        elif ro == 'load-count':
            v = x[k]; c = 'n' if v in A_VARIANTS or v == '000' else WORDS[CNT[v][1]]
            seg.append(('np', f'{c} loads of {eng(x[k + 1])}, carried by the {eng(x[k + 2])}')); k += 3
        elif ro in ('load-crop', 'load-thing', 'load-carried'): k += 1
        elif ro == 'poss': seg.append(('poss', '')); k += 1
        elif ro == 'relation': seg.append(('rel', cap(eng(x[k])))); k += 1
        elif ro == 'ending': seg.append(('end', eng(x[k]))); k += 1
        elif ro == 'tail': seg.append(('tail', eng(x[k]))); k += 1
        else: k += 1
    if len(seg) == 1 and seg[0][0] == 'np' and '\x00' in seg[0][1]: seg = [('name', seg[0][1].split('\x00')[1])]   # rule 2b: a face that is only a star word
    # rule 6: merge runs of name / np pieces that sit right before a jar or an ending
    mg = []; i = 0
    while i < len(seg):
        if seg[i][0] in ('name', 'np'):
            j = i
            while j < len(seg) and seg[j][0] in ('name', 'np'): j += 1
            if j < len(seg) and seg[j][0] in ('poss', 'end'): mg.append(('nm', ' '.join(t.split('\x00')[-1] for _, t in seg[i:j])))
            else: mg += [(('nm' if kd == 'name' else 'np'), t.split('\x00')[0]) for kd, t in seg[i:j]]
            i = j
        else: mg.append(seg[i]); i += 1
    out = []; i = 0; opening = ''
    while i < len(mg):
        kd, t = mg[i]
        if kd == 'open': opening = t + ': '; i += 1
        elif kd == 'nm':
            if i + 1 < len(mg) and mg[i + 1][0] == 'poss':
                if i + 2 < len(mg) and mg[i + 2][0] == 'rel': out.append(f'{mg[i + 2][1]} of the {t} house'); i += 3
                else: out.append(f'Of the {t} house'); i += 2
            elif i + 1 < len(mg) and mg[i + 1][0] == 'end': out.append(f'{t}, {mg[i + 1][1]}'); i += 2
            else: out.append(t); i += 1
        elif kd == 'poss':
            if i + 1 < len(mg) and mg[i + 1][0] == 'rel': out.append(f'{mg[i + 1][1]} of the house'); i += 2
            else: out.append('Of the house'); i += 1
        elif kd == 'np': out.append(cap(t)); i += 1
        elif kd in ('rel', 'end', 'tail'): out.append(cap(t)); i += 1
        else: i += 1
    txt = '; '.join(out)
    if opening: txt = opening + (txt[:1].lower() + txt[1:] if txt else '')
    return (txt or '(nothing)').rstrip(': ') + '.'


def grade(x, flg, readset):
    if damaged(x, flg): return 'damaged'
    rd = [s in readset for s in x]
    if all(rd): return 'whole'
    return 'part' if any(rd) else 'none'


if __name__ == '__main__':
    print(f'[corpus_build] {len(d)} faces; {len(READ)} signs read (strict {len(STRICT)}, wide {len(READ) - len(STRICT)})', flush=True)
    rows = []
    for n_, (i, x, flg, ty, site, kind) in enumerate(zip(d.id, d.tok, d.flg, d.type, d.site, d.kind)):
        r = parse_face(x, lex)
        g = grade(x, flg, READ)
        rows.append(dict(face_id=i, object_id=i.split('.')[0], site=site, object_kind=KIND.get(kind, kind), signs='-'.join(x),
                         sounds=' '.join(SOUND.get(s, f'[{s}]') if s in READ else (f'[{s}]' if s not in ('000', 'ALT') else '[lost]') for s in x),
                         english=build(x, r), grade=g))
        if (n_ + 1) % 500 == 0: print(f'  ... {n_ + 1} of {len(d)} faces read', flush=True)
    out = pd.DataFrame(rows)
    out.to_csv(f'{ROOT}/work_data/corpus_english.csv', index=False)
    gc = out.grade.value_counts()
    print('GRADES (master table, strict+wide):', {k: int(gc.get(k, 0)) for k in ('whole', 'part', 'damaged', 'none')}, flush=True)
    # comparison with sound_list_v4.md: the same rule it used (2+ signs, complete face, v4 values only)
    V4 = pd.read_csv(f'{ROOT}/work_data/sound_v4/values_v4.csv', dtype=str)
    v4_wide = set(V4.sign[V4.tier_v4.isin(['base', 'building'])]); v4_strict = set(V4.sign[(V4.tier_v4 == 'base') | ((V4.tier_v4 == 'building') & (V4.basis != 'seen'))])
    cmp_ = {}
    for nm, S in [('v4 strict', v4_strict), ('v4 wide', v4_wide), ('master strict', STRICT), ('master strict+wide', READ)]:
        w = [len(x) >= 2 and not damaged(x, f) and all(s in S for s in x) for x, f in zip(d.tok, d.flg)]
        w1 = [not damaged(x, f) and all(s in S for s in x) for x, f in zip(d.tok, d.flg)]
        cmp_[nm] = (sum(w), len({x for x, ok in zip(d.tok, w) if ok}), sum(w1))
    print('COMPARISON whole faces (2+ signs) / distinct texts / incl. one-sign faces:', cmp_, flush=True)
    pd.Series({k: v for k, v in cmp_.items()}).to_json(f'{ROOT}/work_data/corpus_compare.json')
