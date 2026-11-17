#!/usr/bin/env python3
"""Class-bigram table over every distinct corpus line (all lines, sounded signs only) -> work_data/long_texts/class_bigrams.csv.  Used to mark a word pair as 'sense' (seen) or 'nonsense' (rare)."""
import collections
from long_cohesion import LL
from long_common import *
def cls(s):
    if s in CNT: return 'NUM'
    if not snd(s): return None
    return CLASS.get(s, '?')
B = collections.Counter(); T = collections.Counter(); S = collections.Counter()
for l in LL:
    c = [cls(s) for s in l]
    for a, b in zip(c, c[1:]):
        if a and b: B[(a, b)] += 1; T[a] += 1; S[b] += 1
tot = sum(B.values())
rows = [dict(first=a, second=b, n=n, expected=round(T[a] * S[b] / tot, 1), ratio=round(n * tot / (T[a] * S[b]), 2)) for (a, b), n in B.items()]
df = pd.DataFrame(rows).sort_values('n', ascending=False)
df.to_csv(f'{OUTDIR}/class_bigrams.csv', index=False)
if __name__ == '__main__':
    print(tot); print(df.head(30).to_string(index=False)); print(df[df.ratio < 0.4].sort_values('expected', ascending=False).head(25).to_string(index=False))
