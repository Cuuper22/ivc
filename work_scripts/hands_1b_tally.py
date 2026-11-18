#!/usr/bin/env python3
"""HANDS step 1b: the row-by-row judgements of the candidate photos (looked at sheets cand_sheet_01..11 and cand_verify.jpg
one by one, 2026-11-17) and the tally. Categories: a unfinished (text cut, animal field empty and smooth), b inscription-only
by design (text fills the face), c worn / broken-away, d animal cut, text field empty, e cannot tell, f hairline sketch: signs drawn in thin scratches, a few cut deep (found at the recut look, recut_sheet_1.jpg)."""
import sys; sys.path.insert(0, "/home/antigravity/Cuuper22/ivc/work_scripts")
from hands_common import *
from math import comb
J = {  # candidate cisi -> (category, note)
'Ad-7':('e','dark, animal-like shapes and signs, unreadable'),'B-19':('b','small oval and signs fill face'),'C-29':('b','text fills face, chipped'),
'C-30':('b','text fills face'),'H-98':('b','text fills face'),'H-100':('c','rough worn surface'),'H-101':('b','three signs fill face'),
'H-103':('b','two rows fill face'),'H-164':('b','wide face, text fills'),'H-533':('e','broken strip'),'H-559':('e','fragment'),
'H-569':('e','broken, text row at top'),'H-596':('b','strokes fill face'),'H-603':('e','fragment, animal-like outline at top left'),
'H-611':('e','edge view'),'H-613':('f','fine scratched hairline figures on dark stone, no cut text'),'H-656':('b','signs fill face'),'K-51':('e','animal-like drawing plus lines; catalogue says no animal'),
'K-52':('e','worn dark, ovals'),'K-53':('e','triangle seal, pictorial design'),'K-54':('e','diamond design'),'L-15':('b','text over whole face'),
'L-52':('e','two animal-like figures and lines'),'L-55':('a','text in top band, field below blank and smooth'),
'L-58':('a','text in upper 55 percent, lower field unworked, rough'),'L-59':('b','text fills face'),'L-62':('f','hairline signs and lines, one sign cut deeper'),
'L-97':('a','small text block top, lower half smooth'),'L-103':('e','worn, broken right side'),'M-682':('b','bar-like, text fills'),
'C-31':('f','hairline sign shapes on smooth dark stone, nothing cut deep'),'M-313':('b','four large signs fill face'),'M-314':('b','three rows fill face'),
'M-315':('a','one row of signs top, lower 55 percent smooth, corner broken'),'M-316':('b','large signs fill'),'M-329':('b','signs fill'),
'M-330':('b','signs fill'),'M-331':('b','two rows fill upper 75 percent'),'M-638':('e','broken pieces'),'M-1010':('e','fragment, two long strokes'),
'M-1014':('e','broken, text row on top'),'M-1057':('e','broken, text row along top edge'),'M-1137':('e','worn'),'M-1178':('b','signs fill'),
'M-1190':('e','fragment'),'M-1191':('b','two rows fill'),'M-1193':('b','text fills upper 75 percent'),'M-1195':('a','text in upper 55 percent, lower smooth'),
'M-1196':('e','fragment'),'M-1197':('b','tall strokes, lower 30 percent empty'),'M-1198':('b','single large sign centred'),
'M-1228':('f','hairline sign shapes, two signs cut deep (diamond and a stroke), rest not cut'),'M-1231':('c','faint worn text on dark'),'M-1232':('a','text in upper half, lower half smooth'),
'M-1233':('b','dense text fills'),'M-1291':('b','four signs fill'),'M-1344':('b','three big signs fill'),'M-1368':('b','signs fill upper 70 percent'),
'Sktd-2':('e','text top, rough lower with incised marks'),'L-54':('c','faint worn text, rough surface'),
# pool B (animal cut, text lost in catalogue)
'M-718':('c','fragment, text broken away'),'M-233':('c','top-left broken away, text field lost'),'H-406':('e','fragment'),'L-66':('c','animal, text worn at top'),
'M-1205':('c','dark fragment'),'H-490':('c','animal, upper part with text broken away'),'K-21':('c','animal, text field broken away'),
'L-24':('c','fragment of animal'),'M-883':('c','fragment of animal'),'M-913':('c','animal, top broken edge'),'M-1185':('c','scene, top broken'),
'K-35':('d','animal cut, text field above blank except one small triangle; one corner chipped'),'M-891':('e','fragment, back marks only')}
C = pd.read_csv(f'{OUT}/cand_list.csv', dtype=str).fillna('')
C = C.drop_duplicates('cisi').copy()
miss = set(C.cisi) - set(J); assert not miss, miss
C['cat'] = C.cisi.map(lambda c: J[c][0]); C['note'] = C.cisi.map(lambda c: J[c][1])
C[['cand','pool','cisi','site','area','house','depth_ft' if 'depth_ft' in C else 'building','animal','hmm','vmm','signs','cat','note','photo']].to_csv(f'{OUT}/unfinished_judged.csv', index=False)
A = C[C.pool == 'A']; B = C[C.pool == 'B']
print('pool A objects', len(A), A.cat.value_counts().to_dict()); print('pool B objects', len(B), B.cat.value_counts().to_dict())
print(pd.crosstab(A.site, A.cat))
# Lothal over-representation: hypergeometric P(>=k of the a-stones in Lothal)
N = len(A); K = (A.site == 'Lothal').sum(); n = (A.cat == 'a').sum(); k = ((A.cat == 'a') & (A.site == 'Lothal')).sum()
p = sum(comb(K, i) * comb(N - K, n - i) for i in range(k, min(K, n) + 1)) / comb(N, n)
print(f'Lothal: {k} of {n} a-stones; Lothal is {K} of {N} pool; P(>= {k}) = {p:.3f}')
# Mohenjo-daro: unfinished found in the same area family / same house? shuffle within site among pool objects
def fam(a): return re.sub(r'[^A-Za-z]', '', a.split()[0].split('.')[0].split('(')[0]) if a else ''
A2 = A.copy(); A2['fam'] = A2.area.map(fam)
rng = np.random.default_rng(1703)
def pairs_same(sub, lab):
    s = 0
    for site, g in sub.groupby('site'):
        v = g[lab].values; m = g.fam.values
        for i in range(len(v)):
            for j in range(i + 1, len(v)):
                if v[i] and v[j] and m[i] == m[j] and m[i] != '': s += 1
    return s
A2['isa'] = (A2.cat == 'a')
real = pairs_same(A2, 'isa')
cnt = 0; dist = []
for _ in range(5000):
    t = A2.copy(); t['isa'] = False
    for site, g in A2.groupby('site'):
        flags = g.isa.values.copy(); rng.shuffle(flags); t.loc[g.index, 'isa'] = flags
    d = pairs_same(t, 'isa'); dist.append(d); cnt += d >= real
print(f'same-area-family pairs among a-stones: real {real}, shuffled-within-site mean {np.mean(dist):.2f}, P(>=real) {cnt/5000:.3f}')
print(A[A.cat == 'a'][['cisi', 'site', 'area', 'house']].to_string())
