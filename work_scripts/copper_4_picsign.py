#!/usr/bin/env python3
"""COPPER step 4: the picture written as a sign.

A TIE is a set (one text family) where some copies show a picture on the second face and others carry one sign there.
Each tie: the sign (first catalogue number; second catalogue number where it has its own), the picture it stands for,
copies each way in each catalogue.
Then the rest of the corpus: (a) where else does each picture-face sign occur (object kinds, pictures on those objects);
(b) is a picture-face sign a sign of its own kind? Share of its uses that are on copper picture faces, against signs of
the same total use count dealt at random (every sign with the same number of uses in the first catalogue).

Predictions written 2026-11-17 before the numbers:
 P4.1 At least 6 ties in the first catalogue, and the second catalogue repeats at least 3 of them with its own sign
      numbers on the picture face of the same text.
 P4.2 The picture-face signs are nearly never used in running text: over 80% of their uses are on copper picture
      faces, against under 10% for signs of the same rarity.
 P4.3 Where a picture-face sign does occur on a seal, the seal shows the animal it stands for more than chance
      (expected to be too few to test; then the rescue is P4.2 and the shapes).
Writes work_data/copper/picsign_ties.csv, picsign_elsewhere.csv, log_4.txt.
"""
import sys; sys.path.insert(0, '/home/claude/ivc/work_scripts')
from copper_common import *
say = say_to(f'{OUT}/log_4.txt')
L = pd.read_csv(f'{OUT}/objects.csv', dtype=str).fillna('')
Mm = pd.read_csv(f'{OUT}/m77_objects.csv', dtype=str).fillna('')
exec(open(f'{ROOT}/work_scripts/copper_2_pairs.py').read().split('# ---- text families')[1].split('rng = np.random')[0])
rows = []
for f, ts in sorted(collections.defaultdict(list, {k: [t for t in FAM if FAM[t] == k] for k in set(FAM.values())}).items()):
    a = L[L.set_text.isin(ts)]; b = Mm[Mm.set_text.isin(ts)]
    ps = collections.Counter(p for p in a.picsign if p) + collections.Counter(p for p in a[a.eye_group == 'sign'].eye.str.extract(r'sign (\d+)')[0].dropna() if p not in set(a.picsign))
    psM = collections.Counter(p for p in b.picsign if p)
    if not ps and not psM: continue
    pics = collections.Counter(p for p, s in zip(a.pic, a.pic_src) if s in ('eye', 'catalogue') and p not in ('quadruped',))
    picM = collections.Counter(x for x in b.fs if x)
    rows.append(dict(family=f, texts=' | '.join(sorted(set(a.set_text) | set(b.set_text))),
                     picture_face_signs_L=dict(ps), picture_face_signs_M77=dict(psM), pictures_L=dict(pics), pictures_M77_codes=dict(picM),
                     copies_L=len(a), copies_M77=len(b)))
T = pd.DataFrame(rows); T.to_csv(f'{OUT}/picsign_ties.csv', index=False)
say(f'families with a sign on the picture face: {len(T)}')
for r in T.itertuples():
    say(f'  {r.texts}: signs L {r.picture_face_signs_L} M77 {r.picture_face_signs_M77}; pictures L {r.pictures_L} M77 {r.pictures_M77_codes}; copies L {r.copies_L} M77 {r.copies_M77}')

# ---------------- (a) where else the picture-face signs occur (first catalogue)
PF = sorted(({p for p in L.picsign if p} | {'749', '479'}) - set(NUM))   # a lone number on that face (035) is a count, not a picture sign
ob = objs.copy(); ob['code'] = ob.symbol.astype(str).str.split(':').str[0]
pf_faces = collections.Counter()   # uses on copper picture faces
for r in L.itertuples():
    if r.picsign: pf_faces[r.picsign] += 1
    if r.second == '479-749': pf_faces['479'] += 1; pf_faces['749'] += 1
use = collections.Counter(); where = collections.defaultdict(collections.Counter)
for o in ob.itertuples():
    for fc in o.faces:
        for s in fc:
            use[s] += 1
            where[s][(o.kind, o.code)] += 1
rows = []
for s in PF:
    rows.append(dict(sign=s, uses=use[s], on_copper_picture_face=pf_faces[s], elsewhere={f'{k[0]}:{k[1] or "none"}': v for k, v in where[s].items()}))
E = pd.DataFrame(rows); E.to_csv(f'{OUT}/picsign_elsewhere.csv', index=False)
say('picture-face signs, first catalogue, all uses:'); [say(f'  {r.sign}: uses {r.uses}, on copper picture faces {r.on_copper_picture_face}, by object:picture {r.elsewhere}') for r in E.itertuples()]

# ---------------- (b) picture-face signs as a kind of their own: share of uses on copper tablets vs same-use signs
share_pf = sum(min(pf_faces[s], use[s]) for s in PF) / sum(use[s] for s in PF)
ctab_use = collections.Counter()
for o in ob[ob.kind == 'ctab'].itertuples():
    for fc in o.faces:
        for s in fc: ctab_use[s] += 1
pool = collections.defaultdict(list)
for s, n in use.items():
    if s in PF or s in ('000', 'ALT'): continue
    pool[n].append(s)
rng = np.random.default_rng(3)
sims = []
for _ in range(10000):
    tot = cu = 0
    for s in PF:
        n = use[s]; c = pool.get(n) or pool[min(pool, key=lambda k: abs(k - n))]
        x = c[rng.integers(len(c))]; tot += use[x]; cu += ctab_use[x]
    sims.append(cu / tot)
sims = np.array(sims)
say(f'P4.2 share of uses of the {len(PF)} picture-face signs that are on copper picture faces: {share_pf:.3f}; '
    f'same-use random signs: share of their uses on copper tablets at all, mean {sims.mean():.3f}, max {sims.max():.3f}')

# ---------------- (c) second catalogue: the picture-face signs on seals and the seal's picture code
R = pd.read_csv(f'{ROOT}/research/data/mahadevan_20260905/concordance_rows.csv', dtype=str).fillna('')
Scols = [f'S{i}' for i in range(1, 15)]
fsT = R.groupby('textnum').fs80.apply(lambda s: max([int(x) for x in s if x] + [0]))
clsT = R.groupby('textnum').inscobj.first()
MPF = sorted({p.lstrip('X') for p in Mm.picsign if p})
seal_fam = collections.Counter(f'{fsT[t]:03d}'[:2] for t in clsT.index if clsT[t] == '1')
nseal = sum(seal_fam.values())
for sg in MPF:
    hit = R[R[Scols].apply(lambda r: any(x.lstrip('*') == sg for x in r), axis=1)].textnum.unique()
    seals = [t for t in hit if clsT[t] == '1']
    fams = collections.Counter(f'{fsT[t]:03d}'[:2] for t in seals)
    cop = [t for t in hit if clsT[t] == '5']
    say(f'  second catalogue sign {sg}: objects {len(hit)} (copper {len(cop)}, seals {len(seals)}); seal picture families {dict(fams)}; '
        + '; '.join(f'family {k}: {v} seals against {len(seals) * seal_fam[k] / nseal:.3f} expected' for k, v in fams.items()))
