#!/usr/bin/env python3
"""EARLY job, step 5: what the earliest-level seals (Mackay's DK-G Early I, 36 first-catalogue seals) carry: endings, animals, stand
patterns, and the crest slot, set beside the seven later levels.

PLAIN WORDS: ENDING = the closing role the parser gives the text (jar = "house of", jar+man = "X's man", spear = chief, comb = junior,
porter = keeper, none = no closing sign). ANIMAL = the creature on the seal's face (animal group from work_data/animal/animal_base.csv).
STAND = the pattern drawn in front of the unicorn (catalogue letters W, J, S, I, L ...). CREST SLOT = the first name sign.
PREDICTION (written before running): the earliest level has the same ending mix as later levels (the history job found endings flat),
carries the unicorn on more than half its seals, and its crest slot is filled by house signs that also occur later (plain fish, lady,
produce, hill, chest ...), not by signs found only at the earliest level.
Outputs: work_data/early/carry_by_level.csv, log_5.txt"""
import sys, os, io, contextlib, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    from time_common import *
    import corpus_build2 as cb
OUTE = f'{ROOT}/work_data/early'
AB = pd.read_csv(f'{ROOT}/work_data/animal/animal_base.csv', dtype=str).fillna('').drop_duplicates('obj').set_index('obj')
G = D[(D.site == 'Mohenjo-daro') & D.area.str.startswith('DKG') & (D.rule == 'B layer-map') & D.seal].copy()
LV = {'Early I': 0, 'Intermediate III': 1, 'Intermediate II': 2, 'Intermediate I': 3, 'Late III': 4, 'Late II': 5, 'Late I': 6, 'Late IA': 6, 'Late IB': 6}
G['lvl'] = (G.period.str.strip() + ' ' + G.phase.str.strip()).map(LV); G = G[G.lvl.notna()]
G['ag'] = [AB.animal.get(str(o), '') for o in G.index]
G['stand'] = [AB.stand.get(str(o), '') for o in G.index]
G['sym'] = [AB.symbol.get(str(o), '') for o in G.index]
G['early'] = G.lvl == 0
E0, EL = G[G.early], G[~G.early]
print(f'earliest-level seals {len(E0)}; later {len(EL)}')
for col in ['ending', 'ag', 'stand', 'shape', 'material']:
    a = E0[col].value_counts(); b = EL[col].value_counts()
    print(f'\n{col.upper()} earliest (n {len(E0)}) | later share')
    for k in sorted(set(a.index) | set(b.index), key=lambda k: -a.get(k, 0))[:10]:
        print(f'  {str(k):16s} {a.get(k, 0):3d} ({100 * a.get(k, 0) / len(E0):4.1f}%) | {b.get(k, 0):3d} ({100 * b.get(k, 0) / len(EL):4.1f}%)')
print('\nANIMAL SYMBOL CODES at the earliest level:', E0.sym.value_counts().to_dict())
fs = E0.faces.apply(lambda f: '-'.join(max(f, key=len)))
firsts = collections.Counter()
for n in E0['name']:
    nn = [a for a in n if a not in ('000', 'ALT')]
    if nn: firsts[nn[0]] += 1
SH = cb.SHORT
print('\nCREST SLOT (first name sign) at the earliest level:', [(s, SH.get(s, '?'), n) for s, n in firsts.most_common()])
later = collections.Counter()
for n in EL['name']:
    nn = [a for a in n if a not in ('000', 'ALT')]
    if nn: later[nn[0]] += 1
print('of the earliest first signs, how many also lead a name at a later level:', sum(1 for s in firsts if later.get(s, 0) > 0), 'of', len(firsts), '; only at the earliest level:', [s for s in firsts if later.get(s, 0) == 0])
# stacked tail shared by two earliest stones
for t in ('240-255-435-690-740',):
    hit = G[G.faces.apply(lambda f: t in '-'.join(max(f, key=len)))]
    print(f'\nthe tail {t}: {len(hit)} seals in DK-G; by level {hit.lvl.astype(int).value_counts().sort_index().to_dict()}')
    hit2 = T[T.faces.apply(lambda fs: any('255-435-690' in '-'.join(x) for x in fs))]
    print(f'   255-435-690 anywhere: {len(hit2)} objects, sites {hit2.site.value_counts().to_dict()}, dated bins {hit2.bin.value_counts().to_dict()}')
G.groupby('lvl').agg(n=('ending', 'size')).to_csv(f'{OUTE}/carry_by_level.csv')

# ---- tests on the first catalogue's differences, and the same animal check on the second catalogue
from scipy.stats import fisher_exact
def fp(a, n, b, m): return fisher_exact([[a, n - a], [b, m - b]])[1]
rare = {'RHINO', 'BUFFALO', 'GOAT', 'OTHER', 'UNKNOWN'}
ar, br = int(E0.ag.isin(rare).sum()), int(EL.ag.isin(rare).sum())
print(f'\nFIRST CATALOGUE: rare creatures (rhino, buffalo, goat, other, unknown): earliest {ar}/{len(E0)} against later {br}/{len(EL)}; Fisher P {fp(ar, len(E0), br, len(EL)):.3g}')
sa, sb = int((E0.stand == "standard").sum()), int((EL.stand == "standard").sum())
print(f'  the standard-bearing stand: earliest {sa}/{len(E0)} against later {sb}/{len(EL)}; Fisher P {fp(sa, len(E0), sb, len(EL)):.3g}')
m = M[(M.site == 'MD') & (M.cls == 'seal') & M.locus.isin(['31', '32'])].copy()
m['lv'] = m.level.astype(int); m = m[m.lv < 0]; m['ft'] = -m.lv; m['n'] = m.n.astype(int)
m = m.sort_values('n', ascending=False).drop_duplicates('textnum')
m['code'] = [None if str(f) in ('0', '') else str(f)[:-1].zfill(2) for f in m.fs]
m['early'] = m.ft >= 20.5
print('\nSECOND CATALOGUE, DK-G seals by picture code (earliest vs later):')
a, b = m[m.early], m[~m.early]
print('  earliest', a.code.fillna('none').value_counts().to_dict()); print('  later   ', b.code.fillna('none').value_counts().to_dict())
common = {'01', '04', '03', None}
ra, rb = int((~a.code.isin(common)).sum()), int((~b.code.isin(common)).sum())
print(f'  pictures other than unicorn (01), short-horned bull (04), humped bull (03) or none: earliest {ra}/{len(a)} against later {rb}/{len(b)}; Fisher P {fp(ra, len(a), rb, len(b)):.3g}')
