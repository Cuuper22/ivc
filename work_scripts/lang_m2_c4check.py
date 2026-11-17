#!/usr/bin/env python3
"""lang_m2: test of the single strongest rival to the control-4 result.
C4 (wrong class for the same picture) beats real in Dravidian, Munda and Sumerian even at the loose distance, where real equals C1.
Rival: the wrong classes C4 can draw are the classes a picture does NOT take, and the classes many pictures take (H10_2 person /
number words) have the most keyword-carrying words in every dictionary, so C4 draws low-density classes and any real score beats it.
Check: the same C4 and C1 draws on a BASE-RATE-ADJUSTED share: for each unit, (sound-alikes carrying the class keyword / all
sound-alikes) minus (share of ALL the dictionary's words carrying that class keyword).  If the rival is right, C4's edge vanishes.
Output: work_data/lang_m2/c4check.csv"""
import sys, os, csv, time, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lang_m2_common import *
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lang_m2_score.py')).read()
exec(src.split('def matrices')[0].split('rng = ')[0])          # imports only
exec('def matrices' + src.split('def matrices')[1].split('ev_cls = collections')[0])
rng = np.random.default_rng(20261119)
NOUNS = blind_nouns(); NI = {n: i for i, n in enumerate(NOUNS)}; CI = {c: i for i, c in enumerate(CLS)}
U = list(csv.DictReader(open(f'{OUT}/units.csv', encoding='utf-8')))
real, base = {}, {}
for fam, names in FAMILIES.items():
    for n in names:
        L = Lex(n, NOUNS, []); real[n] = matrices(L, NOUNS)
        base[n] = {b: np.array([L.kwmat[:, L.kwkeys.index((c, b))].sum() for c in CLS], float) for b in BREADTHS}
        base[n]['_n'] = L.n
        print(f'[c4check {time.strftime("%H:%M:%S")}] {n} loaded', flush=True)
rows = []
for v in VARIANTS:
    units = [u for u in U if u['variant'] == v]; nU = len(units); ar = np.arange(nU)
    A = np.zeros((nU, len(NOUNS)), np.float32)
    for i, u in enumerate(units):
        for x in u['nouns'].split('|'): A[i, NI[x]] = 1
    cls = np.array([CI[u['cls']] for u in units])
    P1 = np.array([rng.permutation(cls) for _ in range(N1)])
    groups = collections.defaultdict(list)
    for i, u in enumerate(units): groups[u['nouns']].append(i)
    cfreq = np.bincount(cls, minlength=len(CLS)).astype(float)
    P4 = np.tile(cls, (N4, 1))
    for t in range(N4):
        for g in groups.values():
            avail = np.array([c for c in range(len(CLS)) if c not in set(cls[g])])
            w_ = cfreq[avail] + 1e-9; w_ = w_ / w_.sum()
            P4[t, g] = rng.choice(avail, size=len(g), replace=len(avail) < len(g), p=w_)
    for fam, names in FAMILIES.items():
        for k in KEYS:
            H = sum(real[n][k][0] for n in names); T = sum(real[n][k][1] for n in names)
            br = sum(base[n][k[1]] for n in names) / sum(base[n]['_n'] for n in names)
            UH = A @ H; UT = A @ T; ok = UT > 0
            def sc(C, adj):
                C = np.atleast_2d(C)
                with np.errstate(invalid='ignore', divide='ignore'):
                    r = np.where(ok[None, :], UH[ar[None, :], C] / UT[None, :] - (br[C] if adj else 0), 0)
                return r.sum(axis=1)
            row = dict(variant=v, family=fam, dist=k[0], breadth=k[1])
            for adj in (False, True):
                o = sc(cls, adj)[0]; c1 = sc(P1, adj); c4 = sc(P4, adj); tag = 'adj' if adj else 'raw'
                row[f'{tag}_real'] = round(o, 3)
                row[f'{tag}_c1_mean'] = round(c1.mean(), 3); row[f'{tag}_c1_P'] = round((1 + (c1 >= o - 1e-9).sum()) / (1 + N1), 4)
                row[f'{tag}_c4_mean'] = round(c4.mean(), 3); row[f'{tag}_c4_P'] = round((1 + (c4 >= o - 1e-9).sum()) / (1 + N4), 4)
            rows.append(row)
            print(v, fam, k, {x: row[x] for x in row if x.startswith('adj')}, flush=True)
with open(f'{OUT}/c4check.csv', 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('written c4check.csv')
