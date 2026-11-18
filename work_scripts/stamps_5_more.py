#!/usr/bin/env python3
"""STAMPS step 5: near matches (4+ signs), kind shares among impressions against seals, stamp roles on multi-stamp
sealings, tag subtypes (backs) against stamp role, and the count-line redesign.
Predictions written before running:
  P8  near twins (4+ signs, one sign off or lost) behave like exact twins: no pull to the impression's own city.
  P2b among impression faces, agent (jar + man) texts and the travelling names are a bigger share than among seals.
  P3b multi-stamp sealings with two different texts pair a name stamp with a short front-word or quantity stamp.
  P6  the box subtype (TAG:B) and cane subtype (TAG:O) carry front-word/quantity stamps; pot-mouth / round (TAG:P)
      carry name stamps.
  P7b (redesign of P7) seals and records that carry the SAME [number][thing] pair share an area more often than when
      the pair labels of the records are dealt at random among the city's records with a pair (5,000 deals).
  P7c (new idea) the count-line seal's own [number][thing] pair is found on a sealing or tag (not a tablet) of the same
      area more than chance (seal areas dealt among the city's seals).
"""
import collections, re, time
import numpy as np, pandas as pd
ROOT = '/home/antigravity/Cuuper22/ivc'; OUT = f'{ROOT}/work_data/stamps'
rng = np.random.default_rng(41); T0 = time.time()
O = pd.read_csv(f'{OUT}/objects.csv', dtype=str).fillna('')
O['n'] = O.n.astype(int); O['lost'] = O.lost.astype(int)
Mt = pd.read_csv(f'{OUT}/matches.csv', dtype=str).fillna(''); Mt['n'] = Mt.n.astype(int)
I = O[O.tier.isin(['sealing', 'stamped pot'])].copy(); S = O[O.tier == 'seal'].copy()
I[['face','cisi','obj','type','tier','site','area','house','roomgrid','building','block','room','depth_ft','bin','animal','stand','material','shape','sides','signs','n','lost','broken','text_kind','restored','photos']].to_csv(f'{OUT}/impressions.csv', index=False)
print(f'impressions.csv written: {len(I)} faces on {I.obj.nunique()} objects')
print('with area', (I.area != '').sum(), '; with building', (I.building != '').sum(), '; with depth', (I.depth_ft != '').sum(), '; with date bin', (I.bin != '').sum(), '; with animal', (I.animal != '').sum())
print('date bins:', I.bin.value_counts().to_dict())

# ---------- near matches 4+ signs
ORDER = ['same room', 'same building', 'same block', 'same area', 'same city, other area', 'same city, findspot unknown', 'other city']
NM = Mt[(Mt.n >= 4) & (Mt.match != 'exact')].copy()
NM = NM[NM.imp_signs.map(lambda t: sum(s not in ('000', 'ALT') for s in t.split('-')) >= 3)]
B = NM.groupby('imp_face').apply(lambda g: g.iloc[np.argmin([ORDER.index(p) for p in g.place])], include_groups=False).reset_index()
print(f'\n== Near twins, 4+ signs (3+ legible): {len(NM)} pairs, {B.shape[0]} impressions; nearest twin lies:')
print(B.place.value_counts().reindex(ORDER).fillna(0).astype(int).to_string())
Sc = S[S.lost == 0]; Sn = Sc.groupby('n').site.value_counts(normalize=True)
anyc = NM.groupby('imp_face').apply(lambda g: (g.place != 'other city').any(), include_groups=False)
nseal = NM.groupby('imp_face').seal_face.nunique()
# chance: each impression's near twins are k seals; chance at least one in own city = 1-(1-p)^k
exp = np.mean([1 - (1 - Sn.get((int(g.n.iloc[0]), g.imp_site.iloc[0]), 0)) ** nseal[f] for f, g in NM.groupby('imp_face')])
print(f'impressions with a near twin in their own city: {anyc.sum()} of {len(anyc)} ({anyc.mean()*100:.1f}%); chance with the same number of random same-length seals {exp*100:.1f}%')
print('near-twin pairs, animals both recorded: agree', (NM.animal_agree == 'yes').sum(), 'disagree', (NM.animal_agree == 'no').sum())
print(B[['imp_cisi', 'imp_site', 'imp_signs', 'match', 'seal_cisi', 'seal_site', 'seal_signs', 'place']].to_string(index=False))
NM.to_csv(f'{OUT}/near_matches.csv', index=False)

# ---------- roles
OPENS = {'820', '861', '817', '920', '692', '880', '824', '545', '091', '550', '360', '556'}
def role(sig, tk):
    s = '-' + sig + '-'; a = sig.split('-'); leg = [x for x in a if x not in ('000', 'ALT')]
    if not leg: return 'unreadable'
    if '-740-090-' in s: return 'agent name (jar + man)'
    if '-590-390-' in s or '-255-435-690-' in s: return 'travelling name'
    if '-920-060-741-' in s: return 'office front'
    if tk in ('bare count line', 'front word + count line') or '-055-' in s and '-740-' not in s: return 'quantity'
    if len(a) <= 3 and a[0] in OPENS and '740' not in a and '520' not in a: return 'front word only'
    if any(x in ('740', '520', '151', '154', '155', '158', '400', '527') for x in a): return 'name (closed)'
    return 'other or broken'
I['role'] = [role(s, t) for s, t in zip(I.signs, I.text_kind)]; S['role'] = [role(s, t) for s, t in zip(S.signs, S.text_kind)]
tab = pd.DataFrame({'impression_faces': I.role.value_counts(), 'seal_faces': S.role.value_counts()}).fillna(0).astype(int)
tab['imp_%'] = (tab.impression_faces / tab.impression_faces.sum() * 100).round(1); tab['seal_%'] = (tab.seal_faces / tab.seal_faces.sum() * 100).round(1)
r_i = I[I.role != 'unreadable']; r_s = S[S.role != 'unreadable']
tab['imp_%_readable'] = (tab.impression_faces / len(r_i) * 100).round(1); tab['seal_%_readable'] = (tab.seal_faces / len(r_s) * 100).round(1)
# role share with impressions counted once per object+text (moulded/repeat stamps collapse)
Iu = I.drop_duplicates(['site', 'signs'])
tab['imp_distinct_texts'] = Iu.role.value_counts().reindex(tab.index).fillna(0).astype(int)
from math import comb
from scipy.stats import fisher_exact
tab['fisher_P_imp_vs_seal'] = [fisher_exact([[tab.at[k, 'impression_faces'], len(r_i) - tab.at[k, 'impression_faces']], [tab.at[k, 'seal_faces'], len(r_s) - tab.at[k, 'seal_faces']]])[1] if k != 'unreadable' else np.nan for k in tab.index]
tab.to_csv(f'{OUT}/roles.csv')
print('\n== Stamp role: impressions against seals =='); print(tab.to_string())
print('by site, impression roles:'); print(pd.crosstab(I.site, I.role).loc[lambda x: x.sum(1) >= 5].to_string())

# ---------- multi-stamp combos
rows = []
for obj, g in I.groupby('obj'):
    if len(g) < 2: continue
    rr = [r for r in g.role if r != 'unreadable']
    rows.append(dict(obj=obj, cisi=g.cisi.iloc[0], site=g.site.iloc[0], type=g.type.iloc[0], stamps=len(g),
                     roles=' + '.join(sorted(rr)), texts=' | '.join(g.signs),
                     same_stamp_repeated=g[g.lost == 0].signs.duplicated().any(),
                     combo=' + '.join(sorted(set(rr))) if len(set(rr)) >= 2 else ('one role: ' + rr[0] if rr else 'unreadable')))
MS = pd.DataFrame(rows); MS.to_csv(f'{OUT}/multistamp_roles.csv', index=False)
print('\n== Multi-stamp objects: combinations of stamp roles =='); print(MS.combo.value_counts().to_string())
print(MS[['cisi', 'site', 'type', 'stamps', 'roles', 'texts']].to_string(index=False))

# ---------- subtype (back) against role
print('\n== Tag subtype against stamp role (faces) =='); print(pd.crosstab(I.type, I.role).to_string())
print('subtype against site:'); print(pd.crosstab(I.type, I.site).loc[:, lambda x: x.sum() > 0].to_string())

# ---------- count lines: redesign P7b and new idea P7c
D = pd.read_csv(f'{ROOT}/research/data/open_prototype/lipi/metadata_filtered.csv', dtype=str).fillna('').set_index('id')
CJ = pd.read_csv(f'{ROOT}/work_data/frame/corpus_jobs.csv', dtype=str).fillna('')
def clean(v): v = str(v).strip(); return '' if v in ('', '-', '--', '- -') else v.strip('-').strip()
NUMC = {'NUM_SHORT', 'NUM_TALL', 'NUM_NAME'}; rec = []
for r in CJ.itertuples():
    s = r.signs.split('-'); c = r.v2_classes.split('-')
    if len(s) != len(c): continue
    ps = {(s[i], s[i+1]) for i in range(len(s) - 1) if c[i] in NUMC and c[i+1] == 'THING'}
    if not ps: continue
    a = clean(D.at[r.face, 'area-section'])
    rec.append(dict(face=r.face, cisi=r.cisi, site=r.site, kind=r.object_kind, tk=r.text_kind, area=a, pairs=ps))
R = pd.DataFrame(rec); R = R[R.area != '']
CLS = R[(R.kind == 'seals') & R.tk.isin(['bare count line', 'front word + count line'])]
REC = R[R.kind != 'seals']
def colo(rec_pairs):
    c = 0
    for s in CLS.itertuples():
        for p, a, site in zip(rec_pairs, REC.area, REC.site):
            if site == s.site and a == s.area and (s.pairs & p): c += 1
    return c
real = colo(list(REC.pairs))
sh = []
for rep in range(2000):
    newp = list(REC.pairs)
    for site, idx in REC.reset_index(drop=True).groupby('site').groups.items():
        idx = list(idx); perm = rng.permutation(idx)
        vals = [REC.pairs.iloc[i] for i in perm]
        for i, v in zip(idx, vals): newp[i] = v
    sh.append(colo(newp))
sh = np.array(sh)
print(f'\n== P7b: (count-line seal, record) object pairs in the same area with the same [number][thing]: {real}; '
      f'record pair labels dealt within city: {sh.mean():.1f}, P(deal >= real) {(sh >= real).mean():.4f}')
TG = REC[REC.kind == 'tags and sealings']
seals_all = O[O.tier == 'seal']
pools = {s: seals_all[(seals_all.site == s) & (seals_all.area != '')].area.values for s in CLS.site.unique()}
def hit(areas):
    return sum(any((p & s.pairs) and t.site == s.site and t.area == a for t, p in zip(TG.itertuples(), TG.pairs)) for s, a in zip(CLS.itertuples(), areas))
real_c = hit(list(CLS.area)); shc = np.array([hit([rng.choice(pools[s]) for s in CLS.site]) for _ in range(2000)])
print(f'== P7c: count-line seals whose pair is on a sealing or tag of the same area: {real_c} of {len(CLS)}; areas dealt: {shc.mean():.2f}, P {(shc >= real_c).mean():.4f}')
print(f'done {time.time()-T0:.0f}s')
