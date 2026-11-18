#!/usr/bin/env python3
"""STAMPS step 4: do count-line seals state the same count of the same thing as the tablets, tags and sealings found
in the same place?  Prediction (written before running): P7 yes: a count-line seal shares an exact [number][thing]
pair with a non-seal object of the same excavation area more often than when the seals' areas are dealt at random
among the city's seals; the shared pair is mostly three of tree 390 or three of porter 156.
Pairs: every number sign (v2 class NUM_SHORT / NUM_TALL / NUM_NAME) directly followed by a counted thing (THING).
Levels: same building, same area, same city.  Chance: count-line seals' findspots dealt among all seals of the same
city that have a findspot at that level (5,000 deals).
Also: same thing only (any number), to see whether it is the goods or the count that matches.
Writes work_data/stamps/countline_vs_records.csv; stdout -> log_4.txt
"""
import re, collections, time
import numpy as np, pandas as pd
ROOT = '/home/antigravity/Cuuper22/ivc'; OUT = f'{ROOT}/work_data/stamps'
T0 = time.time()
rng = np.random.default_rng(31)
D = pd.read_csv(f'{ROOT}/research/data/open_prototype/lipi/metadata_filtered.csv', dtype=str).fillna('').set_index('id')
CJ = pd.read_csv(f'{ROOT}/work_data/frame/corpus_jobs.csv', dtype=str).fillna('')
def blank(v): return str(v).strip() in ('', '-', '--', '- -')
def clean(v): return '' if blank(v) else str(v).strip().strip('-').strip()
NUMC = {'NUM_SHORT', 'NUM_TALL', 'NUM_NAME'}
rows = []
for r in CJ.itertuples():
    s = r.signs.split('-'); c = r.v2_classes.split('-')
    pairs = set(); things = set()
    if len(s) == len(c):
        for i in range(len(s) - 1):
            if c[i] in NUMC and c[i+1] == 'THING': pairs.add((s[i], s[i+1])); things.add(s[i+1])
    m = D.loc[r.face]; area, bh, rg = clean(m['area-section']), clean(m['block-house']), clean(m['room-grid'])
    building = f'{r.site}|{area}|{bh}' if area and bh else (f'{r.site}|{area}|{rg}' if area and rg else '')
    rows.append(dict(face=r.face, cisi=r.cisi, site=r.site, kind=r.object_kind, text_kind=r.text_kind, signs=r.signs,
                     area=f'{r.site}|{area}' if area else '', building=building, pairs=pairs, things=things))
A = pd.DataFrame(rows)
seals = A[A.kind == 'seals']
CLS = seals[seals.text_kind.isin(['bare count line', 'front word + count line']) & (seals.pairs.map(len) > 0)]
REC = A[A.kind != 'seals']
print(f'count-line seals with a [number][thing] pair: {len(CLS)}; non-seal faces with a pair: {(REC.pairs.map(len) > 0).sum()}')
print('pairs on count-line seals:', collections.Counter(p for ps in CLS.pairs for p in ps).most_common(12))
out = []
for lev in ['building', 'area', 'site']:
    idx_p = collections.defaultdict(set); idx_t = collections.defaultdict(set)
    for r in REC.itertuples():
        k = getattr(r, lev)
        if k: idx_p[k] |= r.pairs; idx_t[k] |= r.things
    C = CLS[CLS[lev] != '']
    def score(keys):
        hp = sum(bool(ps & idx_p.get(k, set())) for ps, k in zip(C.pairs, keys))
        ht = sum(bool({p[1] for p in ps} & idx_t.get(k, set())) for ps, k in zip(C.pairs, keys))
        return hp, ht
    rp, rt = score(C[lev].values)
    pools = {s: seals[(seals.site == s) & (seals[lev] != '')][lev].values for s in C.site.unique()}
    sp, stt = [], []
    for rep in range(5000):
        keys = [rng.choice(pools[s]) for s in C.site]
        a, b = score(keys); sp.append(a); stt.append(b)
    sp, stt = np.array(sp), np.array(stt)
    print(f'\nlevel {lev}: count-line seals with a findspot {len(C)}')
    print(f'  same [number][thing] pair on a non-seal object there: {rp} (deals {sp.mean():.2f}, P {(sp >= rp).mean():.4f})')
    print(f'  same thing (any number) there: {rt} (deals {stt.mean():.2f}, P {(stt >= rt).mean():.4f})')
    out.append(dict(level=lev, seals=len(C), same_pair=rp, same_pair_chance=round(sp.mean(), 2), P_pair=(sp >= rp).mean(),
                    same_thing=rt, same_thing_chance=round(stt.mean(), 2), P_thing=(stt >= rt).mean()))
    if lev == 'area':
        for r in C.itertuples():
            hit = r.pairs & idx_p.get(r.area, set())
            if hit:
                objs = REC[(REC.area == r.area) & REC.pairs.map(lambda ps: bool(ps & hit))]
                print(f'   {r.cisi} {r.signs} @ {r.area}: shares {sorted(hit)} with ' + ', '.join(f'{o.cisi or o.face}({o.kind}:{o.signs})' for o in objs.head(6).itertuples()) + (f' +{len(objs)-6} more' if len(objs) > 6 else ''))
pd.DataFrame(out).to_csv(f'{OUT}/countline_vs_records.csv', index=False)
print(f'done in {time.time()-T0:.0f}s')
