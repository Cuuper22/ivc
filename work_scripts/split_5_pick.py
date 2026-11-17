#!/usr/bin/env python3
"""Control step 1: pick 20 control signs matched to 824 (19 occurrences in distinct first-catalogue texts) and 20 matched to 001 (187).
Rule fixed before any control score: eligible = signs other than 850/824/001 with a v2 class; rank by |log(count/target)|; take
signs round-robin over the v2 classes (closest match first inside each class) until 20. Output work_data/split/controls.csv"""
from split_common import *
T3 = [(x, c, k) for x, c, k in train_texts()]
cnt = collections.Counter(a for x, c, k in T3 for a in x if a not in UNK)
rows = []
for tgt, name in ((19, 'for824'), (187, 'for001')):
    el = [s for s in cnt if s not in ('850', '824', '001') and s.isdigit() and 0.5 * tgt <= cnt[s] <= 2.0 * tgt]
    by = collections.defaultdict(list)
    for s in sorted(el, key=lambda s: (abs(np.log(cnt[s] / tgt)), s)): by[base_of(s)].append(s)
    pick = []
    while len(pick) < 20 and any(by.values()):
        for c in sorted(by, key=lambda c: abs(np.log(cnt[by[c][0]] / tgt)) if by[c] else 9):
            if by[c] and len(pick) < 20: pick.append(by[c].pop(0))
    for s in pick: rows.append(dict(group=name, sign=s, v2class=base_of(s), occurrences=cnt[s]))
R = pd.DataFrame(rows); R.to_csv(f'{SPL}/controls.csv', index=False)
print(R.to_string())
print(len(el))
