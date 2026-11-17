#!/usr/bin/env python3
"""More facts on long texts: shared first lines, signs only in long texts, what follows a jar, phrase counts of the 41."""
import collections, json
from long_cohesion import LL
from long_common import *
objs = build_objects()
# shared first line/face, different later part
sig = {}
for o in objs.values(): sig.setdefault(obj_signature(o), o)
by_first = collections.defaultdict(list)
for o in sig.values():
    units = [tuple(l) for f in o['faces'] for l in f['lines']]
    if len(units) >= 2 and len(units[0]) >= 4: by_first[units[0]].append((o['cisi'] or o['obj'], units[1:]))
print('A. objects sharing a first line/face of 4+ signs but differing after it:')
for k, v in sorted(by_first.items(), key=lambda kv: -len(kv[1])):
    if len(v) >= 2 and len({tuple(x[1]) for x in v}) >= 2:
        print('  ', '-'.join(k), len(v), [(c, ['-'.join(u) for u in rest]) for c, rest in v][:5])
# shared last line
by_last = collections.defaultdict(list)
for o in sig.values():
    units = [tuple(l) for f in o['faces'] for l in f['lines']]
    if len(units) >= 2 and len(units[-1]) >= 4: by_last[units[-1]].append((o['cisi'] or o['obj'], units[:-1]))
print('   shared LAST line, different before:', [( '-'.join(k), len(v)) for k, v in by_last.items() if len(v) >= 2 and len({tuple(x[1]) for x in v}) >= 2][:6])
# signs only in long texts: contexts
for s in ('578', '799'):
    for o in sig.values():
        for f in o['faces']:
            for l in f['lines']:
                if s in l: print('B.', s, o['cisi'], o['site'], o['type'], '-'.join(l))
# after a jar (not line-final) in all objects: next sign classes
nxt = collections.Counter(); N = 0
for o in sig.values():
    for f in o['faces']:
        for l in f['lines']:
            for i, s in enumerate(l[:-1]):
                if s == '740': N += 1; nxt[l[i + 1]] += 1
opener = sum(nxt[x] for x in ('692', '820', '861', '817', '920'))
print(f'C. jar followed by something in the same line: {N}; relation signs 090/400/679/621: {sum(nxt[x] for x in ("090","400","679","621"))}; a new opener (692/820/861/817/920): {opener}; porter: {sum(nxt[x] for x in PORTER)}; other:', N - opener - sum(nxt[x] for x in ("090","400","679","621")) - sum(nxt[x] for x in PORTER))
# phrases per text in the manual division
from long_manual import M
kinds = collections.Counter(); per = collections.Counter()
for r, items in M.items():
    per[len(items)] += 1
    for it in items: kinds[it.split(' ', 1)[1]] += 1
print('D. manual phrases per text:', sorted(per.items()), 'total', sum(per.values()), 'kinds', kinds.most_common())
# TRANS class signs in the 41
T = json.load(open(f'{OUTDIR}/read.json'))
tr = collections.Counter()
for t in T:
    for p in t['read']:
        for s in p['signs']:
            if CLASS.get(s) == 'TRANS' and snd(s): tr[(s, snd(s))] += 1
print('E. TRANS words in the 41:', tr.most_common())
# 000 lost-sign share
print('F. lost signs in 41:', sum(p['lost'] for t in T for p in t['read']), 'of', sum(len(p['signs']) for t in T for p in t['read']))
# multi-face objects: phrases per face in the 41 with >1 face
faceph = collections.Counter()
for t in T:
    if len(t['faces']) > 1:
        c = collections.Counter(p['face'] for p in t['read'])
        for f, n in c.items(): faceph[n] += 1
print('G. phrases per face on multi-face objects among the 41:', sorted(faceph.items()))
# identical phrase repeated on several faces of one object
rep = 0
for t in T:
    ph = ['-'.join(p['signs']) for p in t['read'] if len(p['signs']) >= 3]
    if len(ph) != len(set(ph)): rep += 1; print('   repeated phrase in one text:', t['cisi'], [x for x in set(ph) if ph.count(x) > 1])
