#!/usr/bin/env python3
"""PHRASES step 2: the atlas. For each fixed phrase of phrase_list.csv: where it is, on what, when, with which animal.
Fixed 2026-11-17 before the run.
  TOP 100 = the 100 phrases with most distinct texts among the non-nested ones (a nested run is the same unit as its longer host).
  For each phrase: carriers = objects with at least one face holding it. Columns: cities (count, list, top share), Mohenjo-daro and
  Harappa areas / blocks / buildings (objects with that findspot key known: how many, how many different, top one and its share),
  object kinds, time bins, animal and stand letter, found abroad, short-horned bull with trough, previous and next job class
  (v2 class of the sign before and after each occurrence in distinct texts; START / END at the text edge).
Output: work_data/phrases/atlas.csv (top 100), atlas_all.csv (all 136), carriers.csv (phrase, obj), log_2.txt
"""
from phrases_common import *
from frame2_pictures import pic
LOG = open(f'{OUTP}/log_2.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n'); LOG.flush()

P = pd.read_csv(f'{OUTP}/phrase_list.csv', dtype={'phrase': str}).fillna({'nested_in': ''})
O = build_objects()
O['area_n'] = O.area.map(lambda a: re.sub(r'\s*\(.*\)|\.', '', a).strip())
F = build_faces()
face_tok = list(zip(F.obj, F.tok))
say('faces', len(F), 'objects', len(O))

# carriers
car = collections.defaultdict(set)
phr = [tuple(s.split('-')) for s in P.phrase]
for o, x in face_tok:
    if not x: continue
    rs = runs(x)
    for r in rs:
        for p in phr:
            k = len(p)
            if len(r) >= k and any(r[i:i + k] == p for i in range(len(r) - k + 1)): car[p].add(o)
pd.DataFrame([(('-'.join(p)), o) for p, os_ in car.items() for o in sorted(os_)], columns=['phrase', 'obj']).to_csv(f'{OUTP}/carriers.csv', index=False)

# previous / next class over distinct texts
T = distinct_texts()
ctx = collections.defaultdict(lambda: [collections.Counter(), collections.Counter()])
for x in T:
    for p in phr:
        for (i, st, en) in positions(x, p):
            k = len(p)
            prev = 'START' if i == 0 else (v2c(x[i - 1]) if is_sign(x[i - 1]) else None)
            nxt = 'END' if i + k == len(x) else (v2c(x[i + k]) if is_sign(x[i + k]) else None)
            if prev is not None: ctx[p][0][prev] += 1
            if nxt is not None: ctx[p][1][nxt] += 1

def top(cnt, m=3):
    t = sum(cnt.values())
    return '; '.join(f'{k} {v / t:.0%}' for k, v in cnt.most_common(m)) if t else ''
def topkey(s):
    c = collections.Counter(s[s != ''])
    if not c: return '', 0, 0, 0
    k, v = c.most_common(1)[0]
    return k, v / sum(c.values()), len(c), sum(c.values())

rows = []
for r in P.itertuples():
    p = tuple(r.phrase.split('-')); S = O.loc[sorted(car[p])]
    row = dict(phrase=r.phrase, pictures=' '.join(pic(s) for s in p), classes=r.classes, group=r.group, length=r.length,
               n_texts=r.n_texts, n_objects=len(S), n_new_texts=r.new_n, new_status=r.new_status, in_order=r.in_order, lift=r.lift, nested_in=r.nested_in)
    sc = S.site.value_counts()
    row.update(n_cities=int((sc > 0).sum()), cities='; '.join(f'{k} {v}' for k, v in sc.items()), top_city=sc.index[0], top_city_share=round(sc.iloc[0] / len(S), 3))
    for tag, site in (('md', 'Mohenjo-daro'), ('h', 'Harappa')):
        X = S[S.site == site]
        row[f'{tag}_objects'] = len(X)
        for lvl, col in (('area', 'area_n'), ('block', 'block'), ('building', 'building')):
            k, sh, nd, nn = topkey(X[col])
            row[f'{tag}_{lvl}_known'] = nn; row[f'{tag}_{lvl}_distinct'] = nd; row[f'{tag}_{lvl}_top'] = k.split('|', 1)[-1]; row[f'{tag}_{lvl}_top_share'] = round(sh, 3)
    row['kinds'] = '; '.join(f'{k} {v}' for k, v in S.kind.value_counts().items())
    b = S[S.bin != ''].bin.value_counts()
    row['bins_early_mid_late'] = f"{b.get('early', 0)}/{b.get('middle', 0)}/{b.get('late', 0)}"
    row['animals'] = '; '.join(f'{k} {v}' for k, v in S.animal.value_counts().head(4).items())
    row['stands'] = '; '.join(f'{k} {v}' for k, v in S[S.stand != ''].stand.value_counts().head(4).items())
    row['abroad'] = int(S.abroad.sum()); row['shorthorn_bull'] = int((S.animal == SHORTHORN).sum())
    row['seals'] = int((S.kind == 'seal').sum())
    row['prev_class'] = top(ctx[p][0]); row['next_class'] = top(ctx[p][1])
    rows.append(row)
A = pd.DataFrame(rows)
A.to_csv(f'{OUTP}/atlas_all.csv', index=False)
top100 = A[A.nested_in == ''].sort_values(['n_texts', 'lift'], ascending=False).head(100).copy()
top100.insert(0, 'rank', range(1, len(top100) + 1))
top100.to_csv(f'{OUTP}/atlas.csv', index=False)
say('atlas rows', len(top100), ' last n_texts', top100.n_texts.iloc[-1])
say(top100[['rank', 'phrase', 'group', 'n_texts', 'n_objects', 'n_cities', 'top_city', 'top_city_share', 'kinds']].head(25).to_string())
