#!/usr/bin/env python3
"""Sign-by-sign glosser for Indus texts.
Reading order = stored order reversed. Roles come from the seal template
[opener][opener-strokes] [who] [house] [class] plus a lexicon learned from the data.
Run:  python3 gloss.py            -> work_data/gloss_all.csv  (+ prints coverage)
Import: from gloss import load, Lexicon, gloss_text
"""
import re, sys, collections, os
import pandas as pd

ROOT = '/home/claude/ivc'
DATA = f'{ROOT}/research/data/open_prototype/lipi/metadata_filtered.csv'
SHAPES = f'{ROOT}/work_data/sign_shapes.csv'

OPENERS = {'861', '817', '820'}
COUNTS = {f'{i:03d}' for i in list(range(1, 8)) + list(range(31, 37))}
CLOSERS = {'740', '520', '090', '400', '151', '154', '156', '158'}
A_VARIANTS = {str(i) for i in range(465, 476)}
CAP_HEADS = {'920', '692', '550', '820'}          # X-060 head formula (reading order)
CAP_SEL = {'741', '742', '745'}


def parse_row(text):
    """-> (tokens in reading order, flags)"""
    flags = set()
    if '[' in text or ']' in text: flags.add('broken')
    if '/' in text: flags.add('alt')
    t = text.strip('+[]')
    toks = t.split('-')
    toks = toks[::-1]
    out = []
    for s in toks:
        if '/' in s:
            a = s.split('/')
            nz = [x for x in a if x != '000']
            out.append('ALT')  # ambiguous reading -> unknown
        else:
            out.append(s)
    if '000' in out: flags.add('lost')
    return out, flags


class Lexicon:
    """Position statistics learned from distinct complete reading-order texts."""
    def __init__(self, texts, min_n=10):
        pos = collections.defaultdict(collections.Counter)
        prevc = collections.defaultdict(collections.Counter)
        tot = collections.Counter()
        end3 = collections.Counter()
        for x in texts:
            n = len(x)
            for i, s in enumerate(x):
                tot[s] += 1
                p = 'first' if i == 0 else 'last' if i == n - 1 else 'bl' if i == n - 2 else 'second' if i == 1 else 'in'
                pos[s][p] += 1
                if i > 0: prevc[s][x[i - 1] in COUNTS] += 1
            if n >= 3: end3[x[-3:]] += 1
            if n >= 2: end3[x[-2:]] += 1
        self.role = {}
        for s, c in tot.items():
            if c < min_n or s in COUNTS or s in OPENERS or s in CLOSERS: continue
            f = lambda k: pos[s][k] / c
            if f('last') >= 0.4: self.role[s] = 'class'            # learned extra closer
            elif c >= 15 and f('last') >= 0.25: self.role[s] = 'minor-closer'
            elif f('bl') >= 0.55: self.role[s] = 'house-marker'    # sits second-from-last
            elif f('first') >= 0.6: self.role[s] = 'head'
            elif f('second') >= 0.5: self.role[s] = 'second-slot'
            elif prevc[s][True] / max(1, prevc[s][True] + prevc[s][False]) >= 0.4: self.role[s] = 'counted-thing'
        # always-on closers: those the template names, plus learned class signs
        self.formula = {g for g, k in end3.items() if k >= 6}
        bi = collections.Counter()
        for x in texts:
            for i in range(len(x) - 1): bi[x[i:i + 2]] += 1
        self.phrases = {g for g, k in bi.items() if k >= 8}   # recurring two-sign units
        self.tot = tot


def gloss_text(x, lex, flags=frozenset()):
    """x: tuple of sign strings in reading order -> list of roles."""
    n = len(x)
    R = [None] * n
    i0 = 0
    # 1. head formula: [920|692|550|820] 060 [741/742/745]
    for i in range(n - 1):
        if x[i + 1] == '060' and x[i] in CAP_HEADS and R[i] is None:
            R[i] = 'cap'; R[i + 1] = 'cap'
            if i + 2 < n and x[i + 2] in CAP_SEL: R[i + 2] = 'cap-selector'
    for i in range(n):
        if x[i] == '060' and R[i] is None: R[i] = 'cap'
        if x[i] in CAP_SEL and R[i] is None and i > 0 and x[i - 1] == '060': R[i] = 'cap-selector'
    # 2. title phrase [A][806][154/158]
    for i in range(n - 2):
        if x[i] in A_VARIANTS and x[i + 1] == '806' and x[i + 2] in ('154', '158'):
            R[i] = R[i + 1] = R[i + 2] = 'title-phrase'
    # 3. opener + strokes
    for i in range(n):
        if x[i] in OPENERS and R[i] is None and i <= 1 + (1 if R[0] == 'cap' else 0) + 1:
            R[i] = 'opener'
            if i + 1 < n and x[i + 1] == '002' and R[i + 1] is None: R[i + 1] = 'opener-strokes'
    # 4. amount (cup + count either side) and counts
    for i in range(n):
        if x[i] == '700' and R[i] is None:
            R[i] = 'amount'
            for j in (i - 1, i + 1):
                if 0 <= j < n and x[j] in COUNTS and R[j] is None: R[j] = 'amount'
    for i in range(n):
        if x[i] in COUNTS and R[i] is None: R[i] = 'count'
    # 5. class: last sign if closer (template or learned)
    last = n - 1
    if R[last] is None and (x[last] in CLOSERS or lex.role.get(x[last]) == 'class'):
        R[last] = 'class'
    # stray closers elsewhere (e.g. 740 followed by a tail): class-in-middle
    for i in range(n - 1):
        if R[i] is None and x[i] in {'740', '520', '090', '400'}:
            R[i] = 'class-tail'     # class sign followed by a tail (title/count/extra)
    # 6. house marker / house: scan left from class
    anchor = None
    for i in range(n - 1, -1, -1):
        if R[i] in ('class', 'class-tail'): anchor = i; break
    if anchor is not None:
        j = anchor - 1
        while j >= 0 and R[j] is None and lex.role.get(x[j]) == 'house-marker':
            R[j] = 'house-marker'; j -= 1
        if j >= 0 and R[j] is None: R[j] = 'house'
    # 7. other learned roles
    for i in range(n):
        if R[i] is None:
            lr = lex.role.get(x[i])
            if lr == 'house-marker': R[i] = 'house-marker'
            elif lr in ('head', 'second-slot', 'counted-thing'): R[i] = lr
    # 8. fixed endings (>=6 distinct texts share this 2- or 3-sign tail)
    if n >= 3 and tuple(x[-3:]) in lex.formula:
        for i in range(n - 3, n):
            if R[i] is None: R[i] = 'fixed-ending'
    elif n >= 2 and tuple(x[-2:]) in lex.formula:
        for i in range(n - 2, n):
            if R[i] is None: R[i] = 'fixed-ending'
    # 8b. recurring two-sign units (>=8 distinct texts)
    for i in range(n - 1):
        if tuple(x[i:i + 2]) in lex.phrases and R[i] is None and R[i + 1] is None:
            R[i] = R[i + 1] = 'phrase'
    # 8c. minor closers in last place
    if R[last] is None and lex.role.get(x[last]) == 'minor-closer': R[last] = 'class'
    # 9. who: leftover signs, only if the text has an anchor
    anchors = any(r in ('opener', 'opener-strokes', 'class', 'class-tail', 'count', 'amount', 'title-phrase',
                        'cap', 'house', 'house-marker', 'fixed-ending') for r in R)
    for i in range(n):
        if R[i] is None:
            if x[i] in ('000', 'ALT'): R[i] = 'unknown'
            elif anchors: R[i] = 'who'
            elif n <= 2: R[i] = 'mark'          # short unanchored text: a bare name or mark
            else: R[i] = 'unknown'
    return R


def load():
    d = pd.read_csv(DATA, dtype=str).fillna('')
    toks, flg = [], []
    for t in d.text:
        a, f = parse_row(t); toks.append(tuple(a)); flg.append(f)
    d['tok'] = toks; d['flg'] = flg
    d['complete_txt'] = [not (f & {'broken', 'alt', 'lost'}) for f in flg]
    tg = []
    for t in d.type:
        tg.append('seal' if t.startswith('SEAL') else 'copper tablet' if t == 'TAB:C' else 'tablet' if t.startswith('TAB') else
                  'pottery' if t.startswith('POT') else 'other')
    d['group'] = tg
    return d


def lexicon_from(d):
    seen, T = set(), []
    for x, c in zip(d.tok, d.complete_txt):
        if c and x not in seen: seen.add(x); T.append(x)
    return Lexicon(T)


def is_parsed(R):
    return 'unknown' not in R


if __name__ == '__main__':
    d = load(); lex = lexicon_from(d)
    d['roles'] = [gloss_text(x, lex, f) for x, f in zip(d.tok, d.flg)]
    d['parsed'] = [is_parsed(r) for r in d.roles]
    d['reading'] = ['-'.join(x) for x in d.tok]
    d['rolestr'] = [' '.join(r) for r in d.roles]
    out = d[['id', 'cisi', 'site', 'type', 'reading', 'rolestr', 'parsed']].copy()
    out['parsed'] = out.parsed.map({True: 'yes', False: 'no'})
    out.columns = ['id', 'cisi', 'site', 'type', 'reading_order_text', 'role_string', 'fully_parsed']
    out.to_csv(f'{ROOT}/work_data/gloss_all.csv', index=False)
    print('rows', len(out), 'parsed rows', int(d.parsed.sum()))
