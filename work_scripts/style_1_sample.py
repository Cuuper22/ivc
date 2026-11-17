#!/usr/bin/env python3
"""STYLE step 1: draw the stones, build blind contact sheets. Written 2026-11-17, before any coding.

Draws (seed 20261118):
- MAIN: 300 unicorn seals (one per object, with a photo). All photographed unicorn stones of Lothal, Kalibangan,
  Chanhu-daro and the small sites; the rest split Harappa 90 / Mohenjo-daro by catalogue letter round-robin
  (W, J, S, I, L, no letter), non-'Poor' stones first inside each letter.
- RECODE: 40 of the 300 by seed, new neutral numbers, new order, separate sheets, coded after the main pass.
- TWINS: every pair in work_data/twins/pairs.csv and near_twins.csv with both stones unicorn and both photographed;
  stones not already in MAIN get their own sheets.
- OTHER: 80 zebu, short-horned bull, elephant, rhinoceros, tiger seals with photo; all outside Mohenjo-daro, the rest
  Mohenjo-daro round-robin over species.
Sheets show only a neutral number. Keys: key_main.csv, key_recode.csv, key_twins.csv, key_other.csv (not opened while
coding).

PREDICTIONS (written before coding):
P1 Agreement: neck, shoulder, stand_top, stand_bowl, frame, spacing reach >= 75% self-agreement; eye, tail, hoof below.
P2 Styles: 4 to 6 groups. Group goes with the catalogue letter above 99% of shuffles; with city above 99% of shuffles
   dealt within size third; with size; not with time bin overall.
P3 Shops: at least one group is >= 2/3 one city (Harappa: folds + heart/outlined shoulder, big). Inside Mohenjo-daro
   the group mix differs between time bins (P < 0.05: shops drift). Group is independent of text kind and of the
   134 fixed phrases after allowing for many tests (no cell at q < 0.1).
P4 Travelled: 8-15% of coded stones are in a style rare at home (<= 10% of home stones) and common elsewhere
   (>= 25% of another city's stones). Their texts score closer to that other city than other stones of the same
   findspot do (P < 0.05). They carry [crest][jar][man] and front formulas more often than stay-at-home stones; count
   lines no more often.
P5 Twins: twin and near-twin pairs share the style group more than pairs dealt at random within city (60% vs 35%).
P6 Other animals: neck / eye / sign_cut / frame mix goes with city above 95% of shuffles.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_common import *
rng = random.Random(20261118)
O = objects()
O['letter'] = O.stand5.fillna('').replace({'': '-'})
U = O[(O.animal == 'unicorn') & (O.photo != '')].copy()
U['poor'] = U.condition.str.lower().eq('poor')

def rr_pick(df, n, key):
    groups = {}
    for k, g in df.groupby(key):
        ids = list(g.obj); rng.shuffle(ids)
        good = [i for i in ids if not df.loc[df.obj == i, 'poor'].iloc[0]]; bad = [i for i in ids if i not in good]
        groups[k] = good + bad
    out = []; keys = sorted(groups)
    while len(out) < n and any(groups.values()):
        for k in keys:
            if groups[k] and len(out) < n: out.append(groups[k].pop(0))
    return out

main = list(U[~U.city.isin(['MD', 'HA'])].obj)
main += rr_pick(U[U.city == 'HA'], 90, 'letter')
main += rr_pick(U[U.city == 'MD'], 300 - len(main), 'letter')
assert len(main) == 300 and len(set(main)) == 300

def make(objs, prefix, tag, start=1):
    objs = list(objs); rng.shuffle(objs)
    rows = []; items = []
    for k, o in enumerate(objs):
        r = O[O.obj == o].iloc[0]; lab = f'{prefix}{k + start:03d}'
        rows.append({'num': lab, 'obj': o, 'cisi': r.cisi, 'photo': r.photo}); items.append((lab, r.photo))
    pd.DataFrame(rows).to_csv(f'{OUT}/key_{tag}.csv', index=False)
    for s in range(0, len(items), 16):
        sheet(items[s:s + 16], f'{OUT}/sheet_{tag}_{s // 16 + 1:02d}.jpg', cols=4, W=360, H=360)
    return rows

make(main, 'N', 'main')
rec = rng.sample(main, 40); make(rec, 'R', 'recode')
P = pd.read_csv(f'{ROOT}/work_data/twins/pairs.csv', dtype=str).fillna('')
NT = pd.read_csv(f'{ROOT}/work_data/twins/near_twins.csv', dtype=str).fillna('')
c2o = dict(zip(O.cisi, O.obj)); uni = set(U.obj)
pairs = [('twin', a, b) for a, b in zip(P.cisi_a, P.cisi_b)] + [('near', a, b) for a, b in zip(NT.a, NT.b)]
pairs = [(k, c2o[a], c2o[b]) for k, a, b in pairs if a in c2o and b in c2o and c2o[a] in uni and c2o[b] in uni]
pd.DataFrame(pairs, columns=['kind', 'obj_a', 'obj_b']).to_csv(f'{OUT}/twin_pairs.csv', index=False)
tw_new = sorted({o for _, a, b in pairs for o in (a, b)} - set(main))
make(tw_new, 'T', 'twins')
oth = O[O.animal.isin(['zebu', 'short-horned bull', 'elephant', 'rhinoceros', 'tiger']) & (O.photo != '')]
osel = list(oth[oth.city != 'MD'].obj)
md = oth[oth.city == 'MD'].copy(); md['poor'] = md.condition.str.lower().eq('poor')
osel += rr_pick(md, 80 - len(osel), 'animal')
make(osel, 'A', 'other')
print('main', len(main), 'recode', len(rec), 'twin pairs', len(pairs), 'twin new stones', len(tw_new), 'other', len(osel))
print(U[U.obj.isin(main)].groupby(['city', 'letter']).size().unstack(fill_value=0))
