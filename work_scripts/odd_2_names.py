#!/usr/bin/env python3
"""Step 2: do the number / measure words that land inside house names have a second, name-like meaning?
PREDICTIONS (written before the run; the star-names job found that a number inside a name is a spelled word, its stroke
form locked to the sign beside it):
 If sign S is a name word when it stands inside a name (and a measure/count word when it stands in a count line), then
  P1 the strokes next to S are LOCKED inside names (the commonest number form beside S covers more of its name uses than
     of its count uses), as with the fish;
  P2 house-mates (Mohenjo-daro seals of one room, within 3 ft) share S inside names more than chance;
  P3 a name use of S ends the name (jar or closer follows, or S is last) more often than a count use does;
  P4 S in names goes with a fish (star) crest on the same face more than name faces in general do (sky / star vocabulary:
     moon 904 900, the Twelve 055, Ally 690, Peer 840, Bounty 806, Throng 501).
 Name words: 904 Dark-moon (iru-tiṅkaḷ, iru = two and black as in iru-mīn), 900 Moon, 840 Peer (iṇai 'equal'), 055 the Twelve
 (paṉṉiru 'twelve', a body of twelve like 048 the Seven), 690 Ally (piṇai 'union'), 806 Bounty (viḷai 'yield'), 501 Throng
 (kumi 'multitude'), 368 Banner (koṭi), 861 Holder (kāṇiyāḷaṉ 'landholder'), 824 Worth (vilai).
Tables: work_data/odd/names_tests.csv"""
from odd_common import *
import random
random.seed(20261118)
F = faces()
SIGNS = ['904','900','840','055','690','806','501','368','861','824','156']
NAMEROLE = {'crest','self','tag'}
def slot_of(f, i):
    r = f['roles'][i]
    if r in NAMEROLE: return 'name'
    if r in ('counted','count','load-crop','load-count'): return 'count'
    return r
def adj_unit(f, i, s):
    """number run touching position i: returns list of (side, form) for runs directly left/right (stroke signs)."""
    x = f['x']; out = []
    for side, step in (('L', -1), ('R', 1)):
        j = i + step; run = []
        while 0 <= j < len(x) and x[j] in CNT: run.append(x[j]); j += step
        if run:
            if side == 'L': run = run[::-1]
            out.append((side, '+'.join(run)))
    return out
rows = []
facelist = {'L': [f for f in F if f['cat']=='L'], 'Mu': [f for f in F if f['cat']=='Mu']}
# base rates among name-slot faces
def faceinfo(f):
    x = f['x']; hasfish = bool(FISH & set(x)); return hasfish
for cat, FL in facelist.items():
    namefaces = [f for f in FL if any(r in NAMEROLE for r in f['roles'])]
    base_fish = np.mean([faceinfo(f) for f in namefaces])
    for s in SIGNS:
        nm = []; ct = []
        for f in FL:
            for i, a in enumerate(f['x']):
                if a != s: continue
                sl = slot_of(f, i)
                if sl == 'name': nm.append((f, i))
                elif sl == 'count': ct.append((f, i))
        # P3 end-of-name
        def endshare(U):
            k = 0
            for f, i in U:
                x = f['x']; nx = x[i+1] if i+1 < len(x) else '$'
                k += nx in ('740','$','090','400','520','151','154','155','156','158')
            return k, len(U)
        kn, nn = endshare(nm); kc, nc = endshare(ct)
        # P4 fish on same face
        kf = sum(faceinfo(f) for f, i in nm); 
        pf = pbin(kf, len(nm), base_fish) if nm else 1
        rows.append(dict(cat=cat, sign=s, n_name=len(nm), n_count=len(ct), end_name=f'{kn}/{nn}', end_count=f'{kc}/{nc}',
                         fish_name=f'{kf}/{len(nm)}', fish_base=round(base_fish,3), P4_p=round(pf,5)))
R = pd.DataFrame(rows); R.to_csv(f'{OUT}/names_tests.csv', index=False)
print(R.to_string())
# P1: fixed number form beside S, name vs count, pooled, label-shuffle within sign
def fixed_stat(cat):
    FL = facelist[cat]; per = {}
    for s in SIGNS:
        U = []
        for f in FL:
            for i, a in enumerate(f['x']):
                if a != s: continue
                sl = slot_of(f, i)
                if sl not in ('name','count'): continue
                for side, form in adj_unit(f, i, s): U.append((sl, side+':'+form))
        per[s] = U
    def stat(per):
        out = {}
        for lab in ('name','count'):
            top = tot = 0
            for s, U in per.items():
                c = collections.Counter(fm for sl, fm in U if sl == lab)
                if sum(c.values()) >= 1: top += c.most_common(1)[0][1]; tot += sum(c.values())
            out[lab] = (top, tot)
        return out
    o = stat(per); obs = o['name'][0]/max(o['name'][1],1) - o['count'][0]/max(o['count'][1],1)
    ge = 0; N = 3000
    for _ in range(N):
        sh = {}
        for s, U in per.items():
            labs = [sl for sl, fm in U]; random.shuffle(labs); sh[s] = [(l, fm) for l, (sl, fm) in zip(labs, U)]
        oo = stat(sh); ge += (oo['name'][0]/max(oo['name'][1],1) - oo['count'][0]/max(oo['count'][1],1)) >= obs
    return o, obs, (ge+1)/(N+1), per
for cat in ('L','Mu'):
    o, obs, p, per = fixed_stat(cat)
    print(f'\nP1 fixed number form beside the signs ({cat}): name {o["name"]} count {o["count"]}; difference {obs:+.3f}; P {p:.4f}')
    for s in SIGNS:
        for lab in ('name','count'):
            c = collections.Counter(fm for sl, fm in per[s] if sl == lab)
            if c: print(f'   {s} {lab}: {sum(c.values())} unit uses, top {c.most_common(3)}')
# P2 house-mate sharing (Mohenjo-daro)
from v2_common import house_share
print('\nP2 house-mates share the sign inside names (Mohenjo-daro seals):')
for s in SIGNS:
    r = house_share(s, 'name', nshuf=3000)
    print(f'   {s}: {r[2] if r else "too few"}  P={r[1]:.4f}' if r else f'   {s}: too few')
