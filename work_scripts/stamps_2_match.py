#!/usr/bin/env python3
"""STAMPS step 2: match every impression to seals, say where seal and impression lie, and what gets stamped.
Predictions, written 2026-11-17 BEFORE any number below was computed:
  P1  Most impression-to-seal exact matches are in the same city (over 70%), and most of those with both findspots
      known are in a DIFFERENT building from the seal (over 70%): the stone stays home, the stamped goods move.
  P2  Count-line seals and the office front 920-060-741 turn up as impressions more than their share of seals;
      plain name seals less.
  P3  A sealing with two or more readable stamps pairs two different kinds of stamp (name + count line, or office +
      name) in more than half the cases.
  P4  Lothal's warehouse block and Kalibangan look like receivers (many different texts and houses, few repeats);
      Mohenjo-daro DK-G looks like a house sealing its own goods (few texts, many repeats).
  P5  Shared 4+ sign texts link Mohenjo-daro and Harappa most in raw count, but against corpus sizes the over-linked
      pairs are Mohenjo-daro with the outer towns (Lothal, Kalibangan, Chanhu-daro).
Controls: (a) order shuffle: each impression's signs shuffled inside the text (200 shuffles), count matches to seals;
  (b) seal-to-seal recurrence: share of seals whose text recurs on another seal, length-matched to the impressions;
  (c) findspot shuffle: seal findspot keys (room, building, block, area) dealt at random among seals of the same city
      (2,000 deals); (d) city chance: a random seal of the same text length from the whole corpus lies in the
      impression's city with probability = that city's share of seals of that length.
Writes work_data/stamps/matches.csv, kinds.csv, multistamp.csv, clusters.csv, city_links.csv, log_2.txt (stdout).
"""
import os, sys, collections, itertools, random, time
import numpy as np, pandas as pd
ROOT = '/home/claude/ivc'; OUT = f'{ROOT}/work_data/stamps'
T0 = time.time()
def log(*a): print(f'[stamps_2 {time.time()-T0:6.1f}s]', *a, flush=True)
rng = np.random.default_rng(17); random.seed(17)

O = pd.read_csv(f'{OUT}/objects.csv', dtype=str).fillna('')
O['n'] = O.n.astype(int); O['lost'] = O.lost.astype(int); O['broken'] = O.broken == 'True'
NA = pd.read_csv(f'{ROOT}/work_data/registry/names_all.csv', dtype=str).fillna('')
CREST = dict(zip(NA.face_id, NA.house_key))
O['crest'] = O.face.map(CREST).fillna('')
CJ = pd.read_csv(f'{ROOT}/work_data/frame/corpus_jobs.csv', dtype=str).fillna('')

def kind_of(r):
    s = '-' + r.signs + '-'
    if '-920-060-741-' in s: return 'office front 920-060-741'
    if '-590-390-740-' in s or '-590-390-' in s: return 'travelling name 590-390(-740)'
    if '-255-435-690-' in s: return 'travelling name 255-435-690(-740)'
    if r.text_kind in ('bare count line', 'front word + count line'): return 'count line'
    if '-740-090-' in s: return "agent (jar + man)"
    if r.text_kind in ('name text', 'loose name', 'record'): return 'name'
    if r.text_kind == 'damaged': return 'damaged'
    return 'other'
O['skind'] = O.apply(kind_of, axis=1)

S = O[O.tier == 'seal'].copy()
I = O[O.tier.isin(['sealing', 'stamped pot'])].copy()
MT = O[O.tier == 'moulded tablet'].copy()
log(f'seals {len(S)} faces; impressions {len(I)} faces ({(I.tier=="sealing").sum()} sealing, {(I.tier=="stamped pot").sum()} stamped pot); moulded tablets {len(MT)}')
print('Impression faces by type and site:'); print(pd.crosstab(I.type, I.site).T.loc[lambda x: x.sum(1) > 0].to_string())

Sc = S[S.lost == 0]; seal_by_text = collections.defaultdict(list)
for i, r in Sc.iterrows(): seal_by_text[r.signs].append(i)
seals_all = list(S.itertuples())

def near(a, b):
    """a, b: sign lists. returns '' or the near-match type. '000'/'ALT' is a wildcard."""
    W = ('000', 'ALT')
    if len(a) == len(b):
        diff = [(x, y) for x, y in zip(a, b) if x != y]
        if not diff: return 'exact'
        wild = [d for d in diff if d[0] in W or d[1] in W]
        if len(diff) == len(wild) and len(diff) <= 2 and len(a) - len(diff) >= 2: return 'lost sign(s) fit'
        if len(diff) == 1 and len(a) >= 3: return 'one sign different'
        return ''
    if abs(len(a) - len(b)) == 1 and min(len(a), len(b)) >= 3:
        s, l = (a, b) if len(a) < len(b) else (b, a)
        for k in range(len(l)):
            if l[:k] + l[k+1:] == s: return 'one sign more or fewer'
    return ''

def place_rel(i, s):
    if i.site != s.site: return 'other city'
    if i.room and i.room == s.room: return 'same room'
    if i.building and i.building == s.building: return 'same building'
    if i.block and i.block == s.block: return 'same block'
    if i.area_key and i.area_key == s.area_key: return 'same area'
    if not (i.area_key and s.area_key): return 'same city, findspot unknown'
    return 'same city, other area'

log('matching every impression against every seal ...')
rows = []
for k, (ii, ir) in enumerate(I.iterrows()):
    if k % 50 == 0: log(f'  impression {k}/{len(I)}')
    a = ir.signs.split('-')
    if ir.n == 0 or all(x in ('000', 'ALT') for x in a): continue
    rest_a = ir.restored.split('-') if ir.restored else None
    for s in seals_all:
        b = s.signs.split('-')
        t = near(a, b)
        if not t and rest_a and len(rest_a) == len(b) and rest_a == b: t = 'restored equal'
        if not t: continue
        if t == 'exact' and ir.lost: t = 'lost sign(s) fit'
        rows.append(dict(imp_face=ir.face, imp_cisi=ir.cisi, imp_type=ir.type, imp_site=ir.site, imp_area=ir.area, imp_building=ir.building,
                         imp_bin=ir.bin, imp_animal=ir.animal, imp_signs=ir.signs, n=ir.n, match=t,
                         seal_face=s.face, seal_cisi=s.cisi, seal_site=s.site, seal_area=s.area, seal_building=s.building, seal_bin=s.bin,
                         seal_animal=s.animal, seal_signs=s.signs, seal_kind=s.skind,
                         animal_agree='' if not (ir.animal and s.animal) else ('yes' if ir.animal == s.animal else 'no'),
                         place=place_rel(ir, s)))
Mt = pd.DataFrame(rows)
Mt.to_csv(f'{OUT}/matches.csv', index=False)
EX = Mt[Mt.match == 'exact']
print('\n== Matches (pairs impression-seal) by type =='); print(Mt.match.value_counts().to_string())
print(f'impressions with an exact seal twin: {EX.imp_face.nunique()} of {(I.lost == 0).sum()} complete impression faces '
      f'(texts of 2+ signs: {EX[EX.n >= 2].imp_face.nunique()} of {((I.lost == 0) & (I.n >= 2)).sum()})')
print('exact matches where both animals recorded: agree', (EX.animal_agree == 'yes').sum(), 'disagree', (EX.animal_agree == 'no').sum())

# ---- control (a): order shuffle
Ic = I[(I.lost == 0) & (I.n >= 2)]
real = sum(1 for t in Ic.signs if t in seal_by_text)
sh = []
for rep in range(200):
    c = 0
    for t in Ic.signs:
        a = t.split('-'); random.shuffle(a)
        c += '-'.join(a) in seal_by_text
    sh.append(c)
print(f'\n== Control (a) order shuffle: impressions (2+ signs, complete) whose exact text is on a seal: {real} of {len(Ic)}; '
      f'with signs shuffled inside each text {np.mean(sh):.1f} (max {max(sh)}) of 200 shuffles')
# ---- control (b): seal-to-seal recurrence, length-matched
lenmix = Ic.n.value_counts()
Sc2 = Sc[Sc.n >= 2]
cnt = collections.Counter(Sc2.signs)
rec_by_len = Sc2.groupby('n').apply(lambda g: np.mean([cnt[t] >= 2 for t in g.signs]))
exp_b = sum(lenmix.get(L, 0) * rec_by_len.get(L, 0) for L in lenmix.index) / len(Ic)
print(f'== Control (b): a seal text recurs on ANOTHER seal {exp_b*100:.1f}% of the time at the impressions\' length mix; '
      f'impressions find a seal twin {real/len(Ic)*100:.1f}%')

# ---- where: pairs, collapsed to one row per impression (closest seal)
ORDER = ['same room', 'same building', 'same block', 'same area', 'same city, other area', 'same city, findspot unknown', 'other city']
def best(g): return g.iloc[np.argmin([ORDER.index(p) for p in g.place])]
EX2 = EX[EX.n >= 2]
B1 = EX2.groupby('imp_face').apply(best).reset_index(drop=True)
print('\n== Where the nearest exact twin seal lies (one row per impression, texts of 2+ signs) ==')
print(B1.place.value_counts().reindex(ORDER).fillna(0).astype(int).to_string())
B1_3 = EX[EX.n >= 3].groupby('imp_face').apply(best).reset_index(drop=True)
print('texts of 3+ signs:'); print(B1_3.place.value_counts().reindex(ORDER).fillna(0).astype(int).to_string())
# control (d) city chance
Sn = Sc.groupby('n').site.value_counts(normalize=True)
expc = np.mean([Sn.get((r.n, r.imp_site), 0) for r in B1.itertuples()])
# for the impression, any twin seal in same city?
anyc = EX2.groupby('imp_face').apply(lambda g: (g.place != 'other city').any())
print(f'(d) impressions whose twin seals include one in the same city: {anyc.sum()} of {len(anyc)} ({anyc.mean()*100:.1f}%); '
      f'a random seal of the same length lies in that city {expc*100:.1f}% of the time')
# control (c): findspot shuffle within city, levels room/building/block/area, over all exact pairs (2+ signs)
lev = ['room', 'building', 'block', 'area_key']
Sx = S.copy()
def count_levels(Sx):
    loc = Sx.set_index('face')[lev]
    res = {}
    for L in lev:
        c = 0
        for f, g in EX2.groupby('imp_face'):
            iv = I.loc[I.face == f, L].iloc[0]
            if not iv: continue
            if any(loc.at[sf, L] == iv for sf in g.seal_face): c += 1
        res[L] = c
    return res
realL = count_levels(S)
shL = collections.defaultdict(list)
log('findspot shuffle (2,000 deals) ...')
for rep in range(2000):
    Sx = S.copy()
    for site, idx in S.groupby('site').groups.items():
        perm = rng.permutation(len(idx))
        Sx.loc[idx, lev] = S.loc[idx, lev].values[perm]
    r_ = count_levels(Sx)
    for L in lev: shL[L].append(r_[L])
    if rep % 500 == 0: log(f'  deal {rep}')
print('\n== (c) Impressions with an exact twin seal at the same findspot level, real against seal findspots shuffled within city ==')
for L in lev:
    a = np.array(shL[L]); print(f'  {L:9s} real {realL[L]}  shuffled mean {a.mean():.2f}  P(shuffle >= real) {(a >= realL[L]).mean():.4f}')

# ---- what gets stamped (P2): seal kinds, share whose text appears on an impression (exact, 2+ signs)
imp_texts = set(Ic.signs)
S2 = Sc[Sc.n >= 2].copy(); S2['on_imp'] = S2.signs.isin(imp_texts)
tab = S2.groupby('skind').agg(seals=('face', 'size'), on_impression=('on_imp', 'sum'))
tab['share'] = (tab.on_impression / tab.seals * 100).round(1)
# length-matched draws: for each kind, draw seals of other kinds with same length mix
exp_k = {}
for k, g in S2.groupby('skind'):
    others = S2[S2.skind != k]; by_len = {L: gg.on_imp.values for L, gg in others.groupby('n')}
    draws = []
    for rep in range(2000):
        v = 0
        for L, c in g.n.value_counts().items():
            pool = by_len.get(L)
            if pool is None or len(pool) == 0: continue
            v += rng.choice(pool, c).sum()
        draws.append(v / len(g) * 100)
    draws = np.array(draws); exp_k[k] = (draws.mean(), (draws >= tab.at[k, 'share']).mean())
tab['length_matched_other_seals_%'] = [round(exp_k[k][0], 1) for k in tab.index]
tab['P_draws_ge'] = [round(exp_k[k][1], 4) for k in tab.index]
tab.to_csv(f'{OUT}/kinds.csv')
print('\n== Which seal kinds turn up as impressions (exact text, 2+ signs) =='); print(tab.sort_values('share', ascending=False).to_string())
print('\nImpression faces by text kind (their own text):'); print(I.skind.value_counts().to_string())

# ---- multi-stamp sealings (P3)
ms = []
for obj, g in I.groupby('obj'):
    if len(g) < 2: continue
    rd = g[~g.signs.str.fullmatch(r'(000|ALT)(-(000|ALT))*')]
    ms.append(dict(obj=obj, cisi=g.cisi.iloc[0], type=g.type.iloc[0], site=g.site.iloc[0], area=g.area.iloc[0], stamps=len(g),
                   readable=len(rd), texts=' | '.join(g.signs), kinds=' | '.join(g.skind), animals=' | '.join(a or '-' for a in g.animal),
                   distinct_texts=g[g.lost == 0].signs.nunique() if (g.lost == 0).any() else 0,
                   distinct_kinds=len(set(k for k in rd.skind if k not in ('damaged',)))))
MS = pd.DataFrame(ms); MS.to_csv(f'{OUT}/multistamp.csv', index=False)
print(f'\n== Multi-stamp objects: {len(MS)} =='); print(MS.to_string(index=False))

# ---- clusters (P4)
cl = []
for (site, area), g in I[I.area != ''].groupby(['site', 'area']):
    if len(g) < 4: continue
    gc = g[g.lost == 0]; vc = gc.signs.value_counts()
    cr = g.crest[g.crest != '']
    tw = EX2[EX2.imp_face.isin(g.face)]
    cl.append(dict(site=site, area=area, impressions=len(g), objects=g.obj.nunique(), complete=len(gc), distinct_texts=gc.signs.nunique(),
                   most_copies=int(vc.iloc[0]) if len(vc) else 0, top_text=vc.index[0] if len(vc) else '', crests=cr.nunique(),
                   kinds=', '.join(f'{k} {v}' for k, v in g.skind.value_counts().items()),
                   twin_seals=tw.seal_face.nunique(), twin_seals_same_area=tw[tw.place.isin(ORDER[:4])].seal_face.nunique(),
                   twin_seals_other_city=tw[tw.place == 'other city'].seal_face.nunique()))
CL = pd.DataFrame(cl).sort_values('impressions', ascending=False); CL.to_csv(f'{OUT}/clusters.csv', index=False)
print('\n== Clusters (areas with 4+ impression faces) =='); print(CL.to_string(index=False))
log('done step 2')
