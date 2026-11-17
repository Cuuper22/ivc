#!/usr/bin/env python3
"""What long texts teach that short ones cannot: counts over distinct objects.  long = >=9 legible signs, short = <=5."""
import collections, json
from long_common import *
objs = build_objects()
sig = {}
for ob in objs.values(): sig.setdefault(obj_signature(ob), ob)
OBJ = list(sig.values())
long_ = [o for o in OBJ if n_legible(o) >= 9]; short_ = [o for o in OBJ if 1 <= n_legible(o) <= 5]; mid_ = [o for o in OBJ if 6 <= n_legible(o) <= 8]
print('distinct objects', len(OBJ), 'long', len(long_), 'mid', len(mid_), 'short', len(short_))
def signs(o): return [s for f in o['faces'] for l in f['lines'] for s in l if s != '000']
cl = collections.Counter(); cs = collections.Counter(); cm = collections.Counter()
nl = sum(len(signs(o)) for o in long_); ns = sum(len(signs(o)) for o in short_); nm = sum(len(signs(o)) for o in mid_)
for o in long_: cl.update(signs(o))
for o in short_: cs.update(signs(o))
for o in mid_: cm.update(signs(o))
print('sign tokens: long', nl, 'mid', nm, 'short', ns)
rows = []
for s in set(cl) | set(cs) | set(cm):
    a, b, m = cl[s], cs[s], cm[s]
    if a + b + m < 4: continue
    exp = (a + b + m) * nl / (nl + nm + ns)
    rows.append((s, a, m, b, round(a / exp, 2) if exp else 0))
df = pd.DataFrame(rows, columns=['sign', 'long', 'mid', 'short', 'long_enrichment']).sort_values('long', ascending=False)
df['snd'] = df.sign.map(lambda s: snd(s) or '')
df.to_csv(f'{OUTDIR}/sign_long_vs_short.csv', index=False)
only = df[(df.long >= 3) & (df.short == 0)].sort_values('long', ascending=False)
print('signs with >=3 uses in long texts and 0 in short texts:', len(only)); print(only.head(25).to_string(index=False))
print('long-enriched, >=8 uses, enrichment>=2 :'); print(df[(df.long + df.mid + df.short >= 8) & (df.long_enrichment >= 2)].head(25).to_string(index=False))
# ---- repeats inside one text
rep = collections.Counter(); rep_s = collections.Counter(); at = collections.Counter(); at_s = collections.Counter()
for o in long_:
    c = collections.Counter(signs(o))
    for s, k in c.items():
        at[s] += 1
        if k >= 2: rep[s] += 1
for o in OBJ:
    if 3 <= n_legible(o) <= 5:
        c = collections.Counter(signs(o))
        for s, k in c.items():
            at_s[s] += 1
            if k >= 2: rep_s[s] += 1
tot_rep_long = sum(1 for o in long_ if len(set(signs(o))) < len(signs(o)))
tot_rep_short = sum(1 for o in OBJ if 3 <= n_legible(o) <= 5 and len(set(signs(o))) < len(signs(o)))
nsh = sum(1 for o in OBJ if 3 <= n_legible(o) <= 5)
print(f'texts with a repeated sign: long {tot_rep_long}/{len(long_)} = {tot_rep_long/len(long_):.0%}; 3-5 sign texts {tot_rep_short}/{nsh} = {tot_rep_short/nsh:.0%}')
print('repeated in long texts (texts with sign twice+ / texts with sign):', [(s, rep[s], at[s], snd(s) or '') for s, _ in rep.most_common(14)])
# ---- phrase structure over all long objects (hard phrases)
kinds = collections.Counter(); kb = collections.Counter(); nph = collections.Counter(); first_k = collections.Counter(); last_k = collections.Counter()
jarcount = collections.Counter(); phr_rows = []
for o in long_:
    seq = []
    for fi, f in enumerate(o['faces'], 1):
        for li, line in enumerate(f['lines'], 1):
            x = tuple(line)
            for a, b in segment(x):
                p = x[a:b]; P = parse_phrase(p); k = phrase_kind(p, P).split(' (')[0]
                seq.append(k); phr_rows.append(dict(obj=o['obj'], cisi=o['cisi'], face=fi, line=li, kind=k, signs='-'.join(p)))
    nph[len(seq)] += 1
    for k in seq: kinds[k] += 1
    for a, b in zip(seq, seq[1:]): kb[(a, b)] += 1
    if seq: first_k[seq[0]] += 1; last_k[seq[-1]] += 1
    jarcount[sum(1 for s in signs(o) if s == '740')] += 1
pd.DataFrame(phr_rows).to_csv(f'{OUTDIR}/long_phrases_all.csv', index=False)
print('phrases per long text', sorted(nph.items())); print('kinds', kinds.most_common()); print('first', first_k.most_common()); print('last', last_k.most_common())
print('kind bigrams', kb.most_common(14)); print('jars per long text', sorted(jarcount.items()))
# ---- what stands between two phrases: signs just after a jar(+relation) that are not a relation sign, and are followed by something
after = collections.Counter(); before_open = collections.Counter()
for o in long_:
    for f in o['faces']:
        for l in f['lines']:
            for i, s in enumerate(l[:-1]):
                if s == '740' and i + 1 < len(l): after[l[i + 1]] += 1
print('sign right after a jar inside a long-text line:', [(s, c, snd(s) or '') for s, c in after.most_common(12)])
# medial jar frequency
mj = sum(1 for o in long_ for f in o['faces'] for l in f['lines'] for i, s in enumerate(l) if s == '740' and i < len(l) - 1)
tj = sum(1 for o in long_ for f in o['faces'] for l in f['lines'] for i, s in enumerate(l) if s == '740')
print('jars not line-final in long texts', mj, 'of', tj)
mjs = sum(1 for o in short_ for f in o['faces'] for l in f['lines'] for i, s in enumerate(l) if s == '740' and i < len(l) - 1)
tjs = sum(1 for o in short_ for f in o['faces'] for l in f['lines'] for i, s in enumerate(l) if s == '740')
print('same in short texts', mjs, 'of', tjs)
# spear mid-text
for e in ('520', '400', '090'):
    a = sum(1 for o in long_ for f in o['faces'] for l in f['lines'] for i, s in enumerate(l) if s == e and i < len(l) - 1)
    b = sum(1 for o in long_ for f in o['faces'] for l in f['lines'] for i, s in enumerate(l) if s == e)
    c = sum(1 for o in short_ for f in o['faces'] for l in f['lines'] for i, s in enumerate(l) if s == e and i < len(l) - 1)
    d = sum(1 for o in short_ for f in o['faces'] for l in f['lines'] for i, s in enumerate(l) if s == e)
    print(f'sign {e}: not line-final in long {a}/{b}; in short {c}/{d}')
# repeated phrases across objects
pc = collections.defaultdict(set)
for r in phr_rows:
    if r['signs'].count('-') >= 2: pc[r['signs']].add(r['obj'])
rp = sorted(((len(v), k) for k, v in pc.items() if len(v) >= 2), reverse=True)
print('long-text phrases (3+ signs) found on 2+ long objects:', len(rp), rp[:12])
# line / face openers
fl = collections.Counter(); ll = collections.Counter()
for o in long_:
    for f in o['faces']:
        for l in f['lines']:
            if l: fl[l[0]] += 1; ll[l[-1]] += 1
print('line-first', [(s, c) for s, c in fl.most_common(10)]); print('line-last', [(s, c) for s, c in ll.most_common(10)])
# multi-line / multi-face split
ml = sum(1 for o in long_ if len(o['faces']) > 1); ml2 = sum(1 for o in long_ if any(len(f['lines']) > 1 for f in o['faces']))
print('long objects with >1 face', ml, ' with a multi-line face', ml2, 'of', len(long_))
