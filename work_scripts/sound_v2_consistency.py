#!/usr/bin/env python3
"""Consistency of the whole: read every complete text whose signs all carry a sound (Lipi + second-catalogue
texts with no Lipi partner) and look for what a real language shows.
 A. same word, same slot: signs that share one sound (homophone signs) should share their slot profile.
 B. word order inside names: house/place words before kin and title words (head-last); count before the counted thing.
 C. endings agree: names ending in a title or kin word take the matching ending.
 D. nonsense: per sign, the share of its uses that break B; the highest are the weak values.
Writes work_data/sound_v2/consistency_*.csv and prints the numbers used in sound_list_v2.md."""
from v2_common import *
from sound_v2_tiers import V2, CLASS, TIER

OUT = f'{ROOT}/work_data/sound_v2'
texts = []
seen = set()
for x, P, st, g in faces_all('LM'):
    if not x or x in seen or '000' in x or 'ALT' in x: continue
    seen.add(x); texts.append((x, P, st, g))
allsnd = [(x, P, st, g) for x, P, st, g in texts if all(a in V2 for a in x)]
allsnd2 = [t for t in allsnd if len(t[0]) >= 2]
print(f'distinct complete texts {len(texts)}; with a sound on every sign {len(allsnd)} ({len(allsnd2)} of 2+ signs)')

# ---------- A. homophone signs share slots ----------
def slotvec(s):
    c = collections.Counter()
    for x, P, st, g in texts:
        R = P['roles']
        for i, a in enumerate(x):
            if a != s: continue
            r = R[i]
            if r in ('self', 'crest', 'tag'):
                grp = next((gg for gg in P['names'] if s in gg), [s])
                r = 'alone' if len(grp) == 1 else 'first' if grp[0] == s else 'last' if grp[-1] == s else 'mid'
                nxt = x[i + 1] if i + 1 < len(x) else '$'
                r += '>jar' if nxt == '740' else ''
            c[r] += 1
    n = sum(c.values()); return {k: v / n for k, v in c.items()}, n
def tv(a, b): return 0.5 * sum(abs(a.get(k, 0) - b.get(k, 0)) for k in set(a) | set(b))
bysound = collections.defaultdict(list)
for s, (snd, gl) in V2.items():
    if CLASS.get(s) == 'NUM' or s in ('000',): continue
    bysound[snd].append(s)
vec = {s: slotvec(s) for s in V2}
freq = {s: vec[s][1] for s in vec}
rowsA = []
pool = [s for s in V2 if freq[s] >= 5 and CLASS.get(s) != 'NUM']
for snd, ss in bysound.items():
    ss = [s for s in ss if freq[s] >= 5]
    if len(ss) < 2: continue
    for i in range(len(ss)):
        for j in range(i + 1, len(ss)):
            a, b = ss[i], ss[j]; dist = tv(vec[a][0], vec[b][0])
            peers = [tv(vec[a][0], vec[c][0]) for c in pool if c not in ss and 0.33 * freq[b] <= freq[c] <= 3 * freq[b]]
            k = sum(p <= dist for p in peers)
            rowsA.append(dict(sound=snd, a=a, b=b, n_a=freq[a], n_b=freq[b], slot_distance=round(dist, 3), peers_as_close=k, peers=len(peers), p=round((k + 1) / (len(peers) + 1), 3)))
A = pd.DataFrame(rowsA).sort_values('p'); A.to_csv(f'{OUT}/consistency_homophones.csv', index=False)
print('\nA. homophone pairs (closer slot profile than signs of the same frequency):')
print(A.to_string(index=False))
print(f'pairs with p <= 0.10: {(A.p <= 0.10).sum()} of {len(A)} (chance about {0.1 * len(A):.1f})')

# ---------- B. order inside names ----------
ORDER_EARLY = {'HOUSE'}; ORDER_LATE = {'KIN', 'TITLE'}
pairs = collections.Counter(); viol = collections.Counter(); uses = collections.Counter(); good = collections.Counter()
for x, P, st, g in allsnd2:
    for nm in P['names']:
        for s in nm: uses[s] += 1
        for i in range(len(nm) - 1):
            a, b = nm[i], nm[i + 1]; ca, cb = CLASS.get(a), CLASS.get(b)
            pairs[(ca, cb)] += 1
            if ca in ORDER_LATE and cb in ORDER_EARLY: viol[a] += 1; viol[b] += 1
            if ca in ORDER_EARLY and cb in ORDER_LATE: good[a] += 1; good[b] += 1
hl = pairs[('HOUSE', 'KIN')] + pairs[('HOUSE', 'TITLE')]; lh = pairs[('KIN', 'HOUSE')] + pairs[('TITLE', 'HOUSE')]
print(f'\nB. inside names: house/place before kin/title {hl}, kin/title before house/place {lh}')
cp = pd.DataFrame([dict(first=a, second=b, n=n) for (a, b), n in pairs.most_common()]); cp.to_csv(f'{OUT}/consistency_class_pairs.csv', index=False)
print(cp.head(16).to_string(index=False))
# count before counted thing, for goods words
cb_ = ca_ = 0; gviol = collections.Counter(); guse = collections.Counter()
for x, P, st, g in allsnd2:
    for i, a in enumerate(x):
        if CLASS.get(a) != 'GOODS': continue
        guse[a] += 1
        before = i > 0 and x[i - 1] in VAL; after = i + 1 < len(x) and x[i + 1] in VAL
        if before: cb_ += 1
        if after and not before: ca_ += 1; gviol[a] += 1
print(f'goods words: count written before {cb_}, only after {ca_}')

# ---------- C. endings agree ----------
def endk(x):
    if '740' in x:
        j = max(i for i, a in enumerate(x) if a == '740'); return 'jar+man' if j + 1 < len(x) and x[j + 1] == '090' else 'jar'
    if x[-1] == '520': return 'spear'
    if x[-1] in PORTER: return 'porter'
    if x[-1] == '400': return 'comb'
    return 'none'
E = collections.defaultdict(collections.Counter)
for x, P, st, g in texts:
    nm = P['name']
    if not nm or any(a not in V2 for a in nm): continue
    E[CLASS.get(nm[-1])][endk(x)] += 1
Etab = pd.DataFrame(E).fillna(0).astype(int).T; Etab.to_csv(f'{OUT}/consistency_endings.csv')
print('\nC. last name sign class against ending (all complete texts whose name has sounds):'); print(Etab.to_string())

# ---------- D. nonsense per sign ----------
rows = []
for s in V2:
    u = uses[s] + guse[s]
    if u < 5: continue
    v = viol[s] + gviol[s]
    rows.append(dict(sign=s, sound=V2[s][0], english=V2[s][1], cls=CLASS.get(s), tier=TIER.get(s), uses_in_sounded_names=u, order_breaks=v, rate=round(v / u, 3), good_orders=good[s]))
D = pd.DataFrame(rows).sort_values(['rate', 'order_breaks'], ascending=False); D.to_csv(f'{OUT}/consistency_nonsense.csv', index=False)
print('\nD. signs whose readings break the order most:'); print(D.head(15).to_string(index=False))

# top recurring element pairs inside names, read aloud
bi = collections.Counter()
for x, P, st, g in allsnd2:
    for nm in P['names']:
        for i in range(len(nm) - 1): bi[(nm[i], nm[i + 1])] += 1
B = pd.DataFrame([dict(pair=f'{a}-{b}', read=f'{V2[a][0]} {V2[b][0]}', english=f'{V2[a][1]} + {V2[b][1]}', classes=f'{CLASS.get(a)}-{CLASS.get(b)}', texts=n) for (a, b), n in bi.most_common(40)])
B.to_csv(f'{OUT}/consistency_name_pairs.csv', index=False); print('\nname pairs:'); print(B.head(25).to_string(index=False))
