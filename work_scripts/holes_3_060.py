#!/usr/bin/env python3
"""Sign 060 (the joiner): which grammatical word is it?  Candidates and what each predicts about the two sides.
PREDICTIONS written before any number below was computed (2026-11-17):
 GEN  -iṉ (genitive/oblique, "of"): left = a noun that owns something, right = the thing owned; the left set may be any noun
       (names too), chains X-iṉ Y-iṉ Z allowed (several 060 in one line), the pair is NOT reversible (owner left, owned right);
       works on seals and records alike.
 LOC  -il (locative, "in/at"): left = a place or time noun only (closed set: month, gate, quarter, office), right = what stands
       there (ward, person); no chains; not reversible.
 DAT  -ukku (dative, "to/for"): left = receiver, right = thing given or a count; belongs to records (tablets, tags) not seals;
       a count or a measure on the right.
 PLU  -kaḷ (plural): left = a countable noun, often after a number; right = anything; 060 can stand last in a line.
 AND  -um (and, also): left and right are the same kind of word; chains common; reversible (A-060-B and B-060-A both seen);
       can stand first/last as "also".
Numbers computed below: left-neighbour closedness, class match left/right, chains, reversibility, object kinds, first/last uses,
counts left of 060, counts right, records vs seals, second catalogue repeat.
"""
import sys, collections, math
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from holes_common import *
ls = lines(True)
FISH = {'220','235','240','233','231','226','236'}
HEAD = {'920','692','550','820'}
WARD = {'741','742','745'}
NUM = set(CNT)
def cls(s):
    if s is None: return 'END'
    if s in HEAD: return 'HEAD'
    if s in WARD: return 'WARD'
    if s in FISH: return 'FISH'
    if s in NUM: return 'NUM'
    if s == '740': return 'JAR'
    if s == '000': return 'LOST'
    return 'OTHER'
out = []
U = uses('060', ls)
n = len(U); out.append(f'060 uses {n} in {len(set(ls[i]["obj"] for i,_ in U))} objects')
LC = collections.Counter(); RC = collections.Counter(); pair = collections.Counter(); lr = collections.Counter()
for i, p in U:
    t = ls[i]['toks']
    l = t[p-1] if p > 0 else None; r = t[p+1] if p < len(t)-1 else None
    LC[cls(l)] += 1; RC[cls(r)] += 1; lr[(cls(l), cls(r))] += 1
    if l and r: pair[(l, r)] += 1
out.append('left class  : ' + str(dict(LC.most_common())))
out.append('right class : ' + str(dict(RC.most_common())))
# a. baseline: how often is a random sign (anywhere) one of HEAD?
allsigns = [s for L in ls for s in L['toks']]
bh = sum(1 for s in allsigns if s in HEAD) / len(allsigns)
out.append(f'a. share of all signs that are HEAD signs {bh:.3f}; share of 060-left that are HEAD {LC["HEAD"]/n:.3f} (x{LC["HEAD"]/n/bh:.1f})')
# b. left and right class match
same = sum(v for (a, b), v in lr.items() if a == b and a not in ('END', 'OTHER', 'LOST'))
both = sum(v for (a, b), v in lr.items() if a not in ('END', 'OTHER', 'LOST') and b not in ('END', 'OTHER', 'LOST'))
out.append(f'b. both sides classed: {both}; same class on both sides {same} ({same/max(both,1):.2f})')
out.append('   left->right class table: ' + str({f'{a}>{b}': v for (a, b), v in lr.most_common(12)}))
# c. chains
ch = collections.Counter(sum(1 for s in L['toks'] if s == '060') for L in ls if '060' in L['toks'])
out.append(f'c. lines with 1,2,3 060: {dict(ch)}')
# d. reversibility
rev = 0; fwd = 0
for (a, b), v in pair.items():
    fwd += v; rev += pair.get((b, a), 0)
out.append(f'd. A-060-B tokens {fwd}; the reversed B-060-A tokens {rev}')
# e. kinds
kd = collections.Counter(kind(ls[i]['type']) for i, _ in U)
bk = collections.Counter(kind(L['type']) for L in ls)
out.append('e. object kinds: ' + ', '.join(f'{k} {v} (share {v/n:.2f} vs {bk[k]/len(ls):.2f} of all lines)' for k, v in kd.most_common(5)))
# f. first/last
pos = collections.Counter()
for i, p in U:
    m = len(ls[i]['toks']); pos['first' if p == 0 else 'last' if p == m-1 else 'inner'] += 1
out.append(f'f. position {dict(pos)}')
# g. counts left/right
out.append(f'g. count immediately left {LC["NUM"]}, right {RC["NUM"]} of {n}')
# h. the right-hand signs as classes by head
byhead = collections.defaultdict(collections.Counter)
for i, p in U:
    t = ls[i]['toks']
    if p > 0 and t[p-1] in HEAD and p < len(t)-1: byhead[t[p-1]][cls(t[p+1]) + ('' if cls(t[p+1]) != 'OTHER' else ':' + t[p+1])] += 1
for h, c in byhead.items(): out.append(f'h. after {h}-060 comes: ' + str(dict(c.most_common(8))))
# i. left neighbours that are NOT head: who?
nh = collections.Counter(ls[i]['toks'][p-1] for i, p in U if p > 0 and ls[i]['toks'][p-1] not in HEAD)
out.append('i. non-head left neighbours: ' + ', '.join(f'{k}[{snd(k) or "?"}] {v}' for k, v in nh.most_common(14)))
# j. same head, with and without 060 : what follows head when 060 is absent
for h in sorted(HEAD):
    with060 = without = 0; fol = collections.Counter()
    for L in ls:
        t = L['toks']
        for p, s in enumerate(t):
            if s == h and p < len(t)-1:
                if t[p+1] == '060': with060 += 1
                else: without += 1; fol[t[p+1]] += 1
    out.append(f'j. head {h}: followed by 060 {with060}, by something else {without}: ' + ', '.join(f'{k}[{snd(k) or "?"}] {v}' for k, v in fol.most_common(6)))
# k. second catalogue repeat: Mahadevan sign 123
M = mah_lines()
lc = collections.Counter(); rc = collections.Counter(); k = 0
for r in M:
    t = r['toks']
    for p, s in enumerate(t):
        if s == 123:
            k += 1; lc[t[p-1] if p else '^'] += 1; rc[t[p+1] if p < len(t)-1 else '$'] += 1
out.append(f'k. Mahadevan 123 (=060): {k} uses; left {lc.most_common(6)}; right {rc.most_common(8)}')
open(f'{HOLES}/060_grammar.txt', 'w').write('\n'.join(out))
print('\n'.join(out))
