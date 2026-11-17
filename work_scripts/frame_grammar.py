#!/usr/bin/env python3
"""STEP 4. The template as a grammar, by object kind. Fixed before running (2026-11-17):

  Classes = HMM K=10 machine classes (frame_classes.py), hard map. Texts = distinct clean first-catalogue texts (no lost
  sign, no broken edge) of each kind: seals, tablets (incised / moulded), tags and sealings, pots, copper tablets.
  Per kind: start rates, transition rates P(next class | class) including END, every transition with rate >= 10% and
  3+ cases listed; the commonest whole class sequences with their coverage.
  Hand template on the same texts, written as a pattern over hand jobs:
      [OPENER (NUMBER|JOINER)?]? [CREST? (PERSONAL|PLACE|THING|NUMBER)* TAG?] [END END?]
    with at least one name sign and the END block required (a seal-style text). Texts that do not fit are
    grouped by their machine class sequence: the commonest groups are candidate text types the hand template missed.
"""
from frame_common import *

cls = pd.read_csv(f'{OUT}/classes.csv', dtype=str).fillna('')
MC = dict(zip(cls.sign, cls.hmm10)); HJ = dict(zip(cls.sign, cls.hand_job))
uses = dict(zip(cls.sign, cls.uses_distinct_texts.astype(int)))
# class names from data: dominant hand job by uses + top signs
names = {}
for c in sorted(set(MC.values())):
    mem = sorted([s for s in MC if MC[s] == c], key=lambda s: -uses[s])
    jc = collections.Counter()
    for s in mem: jc[HJ.get(s, '?')] += uses[s]
    tot = sum(jc.values())
    names[c] = f'{c} ({", ".join(f"{j} {v / tot:.0%}" for j, v in jc.most_common(2))}; signs {" ".join(mem[:6])})'
for c, n in names.items(): log(n)

seen = set(); texts = collections.defaultdict(list)
for x, f, k in zip(d.tok, d.flg, d.kind):
    if f & {'broken', 'lost', 'alt'} or set(x) & UNK or not x: continue
    if (x, k) in seen: continue
    seen.add((x, k)); texts[k].append(x)
import re as _re
HAND_RE = _re.compile(r'^(OPENER( NUMBER| JOINER)? )?(CREST )?((PERSONAL|PLACE|THING|NUMBER) )*(TAG )?END( END)?$')

out = open(f'{OUT}/grammar.txt', 'w')
def w(s=''):
    print(s); out.write(s + '\n')
summary = []
for k, kname in KIND5.items():
    T = texts[k]
    seqs = [tuple(MC[s] for s in x) for x in T]
    st = collections.Counter(s[0] for s in seqs); tr = collections.defaultdict(collections.Counter)
    for s in seqs:
        for a, b in zip(s, s[1:]): tr[a][b] += 1
        tr[s[-1]]['END'] += 1
    w(f'\n=== {kname}: {len(T)} distinct clean texts, mean length {np.mean([len(x) for x in T]):.2f} ===')
    w('starts: ' + ', '.join(f'{c} {v / len(T):.0%}' for c, v in st.most_common(5)))
    for a in sorted(tr, key=lambda a: -sum(tr[a].values())):
        n = sum(tr[a].values())
        if n < 5: continue
        w(f'  after {a} (n={n}): ' + ', '.join(f'{b} {v / n:.0%} ({v})' for b, v in tr[a].most_common() if v / n >= 0.10 and v >= 3))
    cs = collections.Counter(seqs)
    w('commonest whole sequences:')
    for s, v in cs.most_common(10):
        ex = [x for x, q in zip(T, seqs) if q == s][:2]
        w(f'  {v:4d} ({v / len(T):.1%})  {" ".join(c.split("_")[1] for c in s)}   e.g. {" | ".join("-".join(e) for e in ex)}')
    hj = [' '.join(HJ.get(a, 'PERSONAL') for a in x) for x in T]
    fit = [bool(HAND_RE.match(h)) for h in hj]
    w(f'hand template [opener][crest+personal+tag][ending] fits {sum(fit)} of {len(T)} ({np.mean(fit):.0%})')
    miss = collections.Counter(q for q, f_ in zip(seqs, fit) if not f_)
    misshand = collections.Counter(h for h, f_ in zip(hj, fit) if not f_)
    w('texts the hand template misses, commonest machine sequences:')
    for s, v in miss.most_common(8):
        ex = [x for x, q, f_ in zip(T, seqs, fit) if q == s and not f_][:3]
        w(f'  {v:4d}  {" ".join(c.split("_")[1] for c in s)}   e.g. {" | ".join("-".join(e) for e in ex)}')
    w('same, as hand-job strings:')
    for h, v in misshand.most_common(8): w(f'  {v:4d}  {h}')
    summary.append(dict(kind=kname, texts=len(T), hand_template_fits=sum(fit), share=np.mean(fit),
                        top_missed_machine=' '.join(c.split('_')[1] for c in miss.most_common(1)[0][0]) if miss else ''))
w('\nclass names:')
for c, n in names.items(): w('  ' + n)
pd.DataFrame(summary).to_csv(f'{OUT}/grammar_summary.csv', index=False)
out.close()
