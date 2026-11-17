#!/usr/bin/env python3
"""Read the 41 texts phrase by phrase with the hand division in long_manual.py.  Writes work_data/long_texts/read.json"""
import json, collections
from long_common import *
from long_manual import M
bg = pd.read_csv(f'{OUTDIR}/class_bigrams.csv')
DEPLETED = {(r['first'], r['second']) for _, r in bg.iterrows() if r.ratio < 0.4 and r.expected >= 10}
def cls(s):
    if s in CNT: return 'NUM'
    return CLASS.get(s, '?') if snd(s) else None
T = json.load(open(f'{OUTDIR}/texts.json'))
out = []
for t in T:
    seq = []; marks = []
    for fi, f in enumerate(t['faces'], 1):
        for li, l in enumerate(f['lines'], 1):
            seq += [(s, fi, li) for s in l]
    flat = [s for s, _, _ in seq]
    pos = 0; phr = []
    for item in M[t['rank']]:
        sg, kind = item.split(' ', 1)
        p = sg.split('-')
        assert flat[pos:pos + len(p)] == p, (t['rank'], p, flat[pos:pos + len(p)])
        fl = {(seq[q][1], seq[q][2]) for q in range(pos, pos + len(p))}
        assert len(fl) == 1, (t['rank'], 'phrase crosses a line break', p)
        face, line = next(iter(fl))
        P = parse_phrase(p)
        sd, en = read_phrase(p, P)
        unv = [s for s in p if s != '000' and s not in CNT and s != '806' and not snd(s)]
        lost = sum(1 for s in p if s == '000')
        breaks = []
        cs = [cls(s) for s in p]
        for i in range(len(p) - 1):
            a, b = cs[i], cs[i + 1]
            if a and b and (a, b) in DEPLETED:
                # a jar after a tall count is a counted pot, not the possessive
                if b == 'POSS' and a == 'NUM' and p[i] in {f'{k:03d}' for k in range(31, 37)}: continue
                breaks.append((p[i], p[i + 1], f'{a}>{b}'))
        potjar = any(p[i] in {f'{k:03d}' for k in range(31, 37)} and p[i + 1] == '740' for i in range(len(p) - 1))
        mark = 'nonsense' if breaks else ('partial' if (unv or lost) else 'reads')
        reason = ''
        if breaks: reason = 'word-pair that the corpus avoids: ' + ', '.join(b[2] for b in breaks)
        if mark != 'unread' and any(a in p for a in ('705', '706')):
            mark = 'nonsense'; reason = 'old value kaḷam "threshing floor" (usually with a fixed "three" after it)'
        elif '435' in p:
            mark = 'nonsense'; reason = 'old value miṉ "flash" inside a title block'
        elif potjar:
            mark = 'nonsense'; reason = 'jar read as "house of" where a tall count stands in front of it (a counted pot)'
        elif p in (['176', '175'],):
            mark = 'nonsense'; reason = 'two drawings of the seated person side by side read as "tax tax"'
        if len(p) == 1 and unv: mark = 'unread'
        phr.append(dict(signs=p, kind=kind, face=face, line=line, sound=sd, english=en, unvalued=unv, lost=lost, breaks=breaks, mark=mark, reason=reason, potjar=potjar,
                        roles=P['roles']))
        pos += len(p)
    assert pos == len(flat), (t['rank'], pos, len(flat))
    t['read'] = phr
    out.append(t)
json.dump(out, open(f'{OUTDIR}/read.json', 'w'), ensure_ascii=False, indent=1)
mk = collections.Counter(p['mark'] for t in out for p in t['read'])
print(mk, 'phrases', sum(len(t['read']) for t in out))
for t in out:
    print(t['rank'], t['cisi'], [ (p['mark'][0], '-'.join(p['signs'])) for p in t['read'] if p['mark'] in ('nonsense',)], [b for p in t['read'] for b in p['breaks']])
