#!/usr/bin/env python3
"""CHITS 3b: rescues for the results that went against in chits_3 and chits_4.

 R1 (amounts, redesign): one name, many records: is a comb name held to ONE cup count more than a jar-only name?
    Share of a name's cup records on its modal count, names with 2+ cup records, comb vs jar-only, labels shuffled.
 R2 (amounts, new idea): the big measure 705/706 on the other face: comb records against all other name records.
    Also format: moulded (TAB:B) vs incised (TAB:I) share, comb vs jar-only.
 R3 (names vs trenches, redesign): mound level (first letter of the trench: F, E, ET, D, AB, G ...) instead of trench.
 R4 (comb in FTrench I, check): the comb concentration in FTrench I with name 176 taken out.
 R5 (copies vs cups, redesign): copies counted over the whole of Harappa (signature only, trench ignored).
 R6 (copies, new idea): copies per issue by ending (comb / jar only / no jar).
PREDICTIONS (before numbers): R1 comb names more fixed (higher modal share); R2 comb never with the big measure;
R3 names sit in fewer mounds than chance; R4 survives without 176; R5 copies still do not follow cups; R6 comb issues
are copied more (a standard chit made in numbers).
Writes work_data/chits/c3b_log.txt.
"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chits_common import *
from scipy.stats import spearmanr, fisher_exact
LOG = open(f'{OUT}/c3b_log.txt', 'w'); say = say_to(LOG)
rng = np.random.default_rng(303)
R = pd.read_csv(f'{OUT}/c3_records.csv', dtype={'obj': str})
H = R[R.site == 'Harappa'].copy()
# R1
say('R1 one name, many records: share of a name\'s cup records on its modal count (names with 2+ cup records)')
C = H[H.cups.notna() & H.group.isin(['comb 740-400', 'jar only', 'name, no jar'])]
def fixedness(df, grp):
    out = {}
    for g in ('comb 740-400', 'jar only', 'name, no jar'):
        s = df[grp == g]; vals = []
        for nm, x in s.groupby('name').cups:
            if len(x) >= 2: vals.append(x.value_counts().iloc[0] / len(x))
        out[g] = (np.mean(vals) if vals else np.nan, len(vals))
    return out
ob = fixedness(C, C.group.values)
for g, (m, n) in ob.items(): say(f'  {g:16s} names {n:3d} mean modal share {m:.3f}')
# shuffle group labels by NAME (each name keeps its records, the label moves)
names = C.groupby('name').group.first(); nul = []
for _ in range(3000):
    perm = dict(zip(names.index, rng.permutation(names.values)))
    f = fixedness(C, C.name.map(perm).values); nul.append(f['comb 740-400'][0] - f['jar only'][0])
nul = np.array(nul); d = ob['comb 740-400'][0] - ob['jar only'][0]
say(f'  comb minus jar-only {d:+.3f} (P high {(nul >= d).mean():.4f}, P low {(nul <= d).mean():.4f})')
say(f'  without name 176: ' + str(fixedness(C[C.name != '176'], C[C.name != '176'].group.values)))
# R2
say('\nR2 the big measure on the other face, and the tablet format:')
A = R.copy()
for g in ('comb 740-400', 'jar only', 'man 740-090', 'other after-jar sign', 'name, no jar'):
    s = A[A.group == g]
    say(f'  {g:20s} records {len(s):4d}; with big measure {int(s.big.notna().sum()) + int(s.other_faces.fillna("").str.contains("705|706").sum() - s.big.notna().sum()) if False else int(s.other_faces.fillna("").str.contains("705|706").sum())}; '
        f'formats {fmt_counter(collections.Counter(s.type), 3)}')
cb = int(A[A.group == 'comb 740-400'].other_faces.fillna('').str.contains('705|706').sum()); cn = int((A.group == 'comb 740-400').sum())
ob_ = int(A[A.group != 'comb 740-400'].other_faces.fillna('').str.contains('705|706').sum()); on = int((A.group != 'comb 740-400').sum())
say(f'  comb {cb}/{cn} against all other name records {ob_}/{on}: Fisher P {fisher_exact([[cb, cn - cb], [ob_, on - ob_]])[1]:.4f}')
O = load(); Hm = O[(O.site == 'Harappa') & (O.kind == 'mtab')].copy()
Hm['comb'] = [any(j is not None and j[1] == '400' for j in js) for js in Hm.jars]
Hm['jaronly'] = [any(j is not None and j[1] == '' for j in js) for js in Hm.jars]
Hm['big'] = [any(('705' in f) or ('706' in f) for f in fs) for fs in Hm.faces]
for lab, m in (('comb', Hm.comb), ('jar only', Hm.jaronly & ~Hm.comb), ('neither', ~Hm.comb & ~Hm.jaronly)):
    s = Hm[m]; say(f'  Harappa tablets {lab:9s} n {len(s):4d} moulded TAB:B {int((s.type == "TAB:B").sum())} incised TAB:I {int((s.type == "TAB:I").sum())}; any 705/706 on the object {int(s.big.sum())}')
# R3 mound level
say('\nR3 names against mounds (issues; names on 2+ issues):')
B = pd.read_csv(f'{OUT}/c4_batches.csv', dtype=str).fillna('')
B = B[B.namekey != '']
def mound(a):
    a = a.strip()
    if a.startswith('AB'): return 'AB'
    if a.startswith('ET'): return 'ET'
    return a[:1]
B['mound'] = B.trench.map(mound)
multi = B.groupby('namekey').filter(lambda g: len(g) >= 2)
o = multi.groupby('namekey').mound.nunique().mean(); nn = []
for _ in range(2000):
    m = rng.permutation(B.mound.values); x = B.assign(mound=m); x = x[x.namekey.isin(multi.namekey)]
    nn.append(x.groupby('namekey').mound.nunique().mean())
nn = np.array(nn)
say(f'  {multi.namekey.nunique()} names: {o:.2f} mounds per name against {nn.mean():.2f} (P low {(nn <= o).mean():.4f}); mounds: {fmt_counter(collections.Counter(B.mound))}')
# R4
say('\nR4 comb concentration in FTrench I without name 176:')
Hb = Hm[Hm.lostfree & (Hm.area != '')].copy()
Hb['n176'] = [any(j is not None and '-'.join(j[0]) == '176' for j in js) for js in Hb.jars]
for lab, df in (('all', Hb), ('without 176', Hb[~Hb.n176])):
    x = df.comb.values; ar = df.area.values
    def chi(xx):
        s = 0
        for a in np.unique(ar):
            m = ar == a; e = m.sum() * xx.mean()
            if e > 0: s += (xx[m].sum() - e) ** 2 / e
        return s
    oc = chi(x); nc = np.array([chi(rng.permutation(x)) for _ in range(2000)])
    f1 = df[df.area == 'FTrench I']
    say(f'  {lab}: FTrench I comb {int(f1.comb.sum())}/{len(f1)} against Harappa {x.mean():.3f}; trench chi {oc:.1f} against {nc.mean():.1f} (P {(nc >= oc).mean():.4f})')
# R5 / R6 copies
say('\nR5 copies over the whole of Harappa (signature only):')
Hl = Hm[Hm.lostfree].copy()
Hl['cups'] = [next((amount_of(f)['cup'] for f in fs if 'cup' in amount_of(f)), None) for fs in Hl.faces]
Hl['end'] = ['400' if c else ('jar' if j else 'other') for c, j in zip(Hl.comb, Hl.jaronly)]
S = Hl.groupby('sig').agg(copies=('obj', 'size'), cups=('cups', 'first'), end=('end', 'first'), types=('type', lambda s: ','.join(sorted(set(s))))).reset_index()
Sc = S[S.cups.notna()]
rho = spearmanr(Sc.copies, Sc.cups).correlation; nr = np.array([spearmanr(rng.permutation(Sc.copies.values), Sc.cups).correlation for _ in range(3000)])
say(f'  {len(Sc)} signatures with cups; Spearman copies~cups {rho:+.3f} (P high {(nr >= rho).mean():.4f}); copies==cups {(Sc.copies == Sc.cups).sum()} signatures')
say('  copies by cups: ' + '; '.join(f'{int(c)}c: mean {Sc[Sc.cups == c].copies.mean():.2f} max {Sc[Sc.cups == c].copies.max()}' for c in sorted(Sc.cups.unique())))
say('\nR6 copies per signature by ending:')
for e in ('400', 'jar', 'other'):
    s = S[S.end == e]; say(f'  {e:5s} signatures {len(s):4d} objects {s.copies.sum():4d} copies per signature {s.copies.mean():.2f}; with 2+ copies {int((s.copies >= 2).sum())}; moulded-only signatures copies {s[s.types == "TAB:B"].copies.mean():.2f}')
x = S.end.values == '400'; c = S.copies.values; o = c[x].mean() - c[S.end.values == 'jar'].mean(); nn = []
for _ in range(3000):
    p = rng.permutation(S.end.values); nn.append(c[p == '400'].mean() - c[p == 'jar'].mean())
nn = np.array(nn); say(f'  comb minus jar-only copies per signature {o:+.2f} (P high {(nn >= o).mean():.4f})')
say('done')
