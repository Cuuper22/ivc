#!/usr/bin/env python3
"""Step 3: every number + sign compound inside names, and number signs used as sound signs.

PREDICTIONS (written before the run):
 C1  Signs that take a number in the NAME slot take ONE fixed number form far more than the same signs do in count
     slots (a compound word, not a count). Measured as the share of each sign's single commonest form.
 C2  (ligature puns) a fish with strokes drawn INTO the sign is the same word as number + fish written out:
     - 231 (fish with one small stroke inside) = oru-miin "one-star": frames of 1 + 220 overlap frames of 231
       more than frames of other signs of 231's frequency do.
     - 226 (fish with four strokes round it) = naan-miin "asterism" (Tamil naanmiin, Kalittokai 104;
       naal 'four' ~ naal 'day, lunar asterism'): frames of 4 + 220 overlap frames of 226.
 C3  (eight = en "count, think, strength") value 8 never stands before a goods word: what follows an 8 is a name
     sign, a closer or nothing, at a higher rate than for 3 to 5.
 C4  (one = or/oru 'unique, first') in names, a single stroke before a sign is followed by the jar/closer within two
     signs more often than a single stroke in count slots.
Run: python3 stars_3_compounds.py -> work_data/stars/name_compounds.csv
"""
from stars_common import *
from gloss2 import label

rows = []
for cat in ('L', 'Mu'):
    U = distinct(all_units(cat)); U['S'] = U.slot.map({'name': 'NAME', 'sealx': 'X', 'count_pure': 'COUNT', 'count_named': 'COUNT'})
    U['form'] = U['style'] + U.value.astype(str)
    print(f'\n===== {cat}: number units on distinct texts {len(U)}; name {sum(U.S=="NAME")}, count {sum(U.S=="COUNT")}')
    for S in ('NAME', 'COUNT'):
        g = U[U.S == S]; k = n = 0
        for f, h in g.groupby('nxt'):
            if len(h) >= 4:
                c = collections.Counter(h.form); k += c.most_common(1)[0][1]; n += len(h)
        print(f'C1 {S}: signs with 4+ numbered uses: commonest form covers {k}/{n} = {k/max(n,1):.0%}')
    # table of name-slot compounds
    for f, h in U[U.S == 'NAME'].groupby('nxt'):
        c = collections.Counter(h.form); cc = U[(U.S == 'COUNT') & (U.nxt == f)]
        rows.append(dict(cat=cat, sign=f, label=label(f), name_uses=len(h), name_forms=dict(c.most_common()),
                         top_form=c.most_common(1)[0][0], top_share=round(c.most_common(1)[0][1] / len(h), 2),
                         count_uses=len(cc), count_forms=dict(collections.Counter(cc.form).most_common()),
                         sites=dict(collections.Counter(h.site).most_common()), examples=' '.join(h.cisi.head(4))))
C = pd.DataFrame(rows); C.to_csv(f'{OUTS}/name_compounds.csv', index=False)
print('\nName-slot compounds with 3+ uses (first catalogue):')
for _, r in C[(C.cat == 'L') & (C.name_uses >= 3)].sort_values('name_uses', ascending=False).iterrows():
    print(f'  {r.sign} {r.label[:22]:22s} name {r.name_uses:3d} {r.name_forms}  | count {r.count_uses} {r.count_forms}  | {r.sites}')
print('\nnew texts, name-slot compounds with 2+ uses:')
for _, r in C[(C.cat == 'Mu') & (C.name_uses >= 2)].sort_values('name_uses', ascending=False).iterrows():
    print(f'  {r.sign} {r.label[:22]:22s} name {r.name_uses:3d} {r.name_forms}  | count {r.count_uses} {r.count_forms}')

# C2 ligature frames: treat "n + 220" written out as one token, compare its frames with 231 / 226
def frames(cat):
    ctx = collections.defaultdict(set); use = collections.Counter(); seen = set()
    for x, P, st, g in faces_all(cat):
        if x in seen: continue
        seen.add(x); x = list(x)
        # merge number + plain fish into one token N<v>F (value of the last one-style run)
        y = []; i = 0
        for u in sorted(units(tuple(x), P), key=lambda u: -u['i']):
            pass
        us = {u['i']: u for u in units(tuple(x), P) if u['nxt'] == '220'}
        while i < len(x):
            if i in us: y.append(f"N{us[i]['value']}F"); i = us[i]['j'] + 2
            else: y.append(x[i]); i += 1
        y = ['^'] + y + ['$']
        for q in range(1, len(y) - 1): ctx[y[q]].add((y[q - 1], y[q + 1])); use[y[q]] += 1
    return ctx, use
for cat in ('L', 'LM'):
    ctx, use = frames(cat)
    for a, b in (('N1F', '231'), ('N4F', '226'), ('N2F', '226'), ('N3F', '226'), ('N6F', '226'), ('N4F', '220'), ('N1F', '220')):
        if use[a] < 2 or use[b] < 2: print(f'C2 {cat} {a}~{b}: too few ({use[a]}, {use[b]})'); continue
        obs = len(ctx[a] & ctx[b]); nb = use[b]
        peers = [len(ctx[a] & ctx[s]) for s in use if s not in (a, b) and 0.5 * nb <= use[s] <= 2 * nb]
        p = (1 + sum(v >= obs for v in peers)) / (len(peers) + 1)
        print(f'C2 {cat} {a} ({use[a]} uses) ~ {b} ({use[b]}): {obs} shared frames against median {np.median(peers):.0f} for {len(peers)} signs of {b}\'s frequency, P {p:.3f}; shared: {sorted(ctx[a] & ctx[b])[:6]}')

# C3 eight, C4 one
for cat in ('L', 'Mu'):
    A = distinct(all_units(cat))
    for v in (8, 7, 6, 5, 4, 3):
        g = A[A.value == v]
        nameish = g.nxt.isin(['740', '520', '090', '400', '151', '154', '156', '158']) | g.slot.isin(['name', 'count_named'])
        print(f'C3 {cat} value {v}: {len(g)} units; in a name run or before a closer {int(nameish.sum())} ({nameish.mean() if len(g) else 0:.0%}); next signs {collections.Counter(g.nxt).most_common(6)}')
    g = A[A.value == 1]
    for S in ('name', 'count_pure'):
        h = g[g.slot == S]
        print(f'C4 {cat} one-stroke units in {S}: {len(h)}; next signs {collections.Counter(h.nxt).most_common(8)}')
