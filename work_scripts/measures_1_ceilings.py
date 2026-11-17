#!/usr/bin/env python3
"""Step 1: every count that stands with a measure sign; the largest count each unit takes.

PREDICTIONS (written before the first run).
Tamil ladder (Tamil Lexicon + DEDR): 8 ollock (ār̤ākku) = 1 paṭi/nāḻi; 2 ollock = uḻakku (1/4 paṭi); uri = 1/2 paṭi;
8 paṭi = 1 marakkāl = 1 kuṟuṇi; 2 kuṟuṇi = 1 patakku; 4 marakkāl = 1 tūṇi; 12 marakkāl = 1 kalam (3 tūṇi);
kōṭṭai = 21 marakkāl; karacai = 400 marakkāl; niṟai = 100 palam (a weight).
Identify: cup 700 = marakkāl/kuṟuṇi, kalam 705/706 = 12 cups, paṭi 320 = 1/8 cup, kāl 061 = a quarter.
 T1 cup counts never reach 12 (max <= 11); if counts are named shares of a kalam they are only 1,2,3,4,6.
 T2 paṭi counts never reach 8 (max <= 7).
 T3 kāl (quarter) counts never reach 4 (max <= 3).
 T4 kalam counts are NOT capped low (a kalam is the big unit; something above 3 shows up).
Weight ladder (cubical stones 1,2,4,8,16,32,64,160,200,320,640): each written unit doubles the one below.
 W1 counts of container units sit on 1,2,4,8 for 80% or more; 3, 5, 6, 7 rare.
 W2 5 is as common as 6 (5 = 4+1 is an ordinary binary sum).
Tall strokes count containers: T5 units take tall strokes 80%+, except hand 817/861 (people: short).
"""
from measures_common import *

L = unit_counts(faces('L')); Mu = unit_counts(faces('Mu'))
U = pd.concat([L, Mu]); U.to_csv(f'{OUTM}/unit_counts.csv', index=False)

out = []
P = print
P('rows (count touching a unit sign):', len(L), 'Lipi,', len(Mu), 'new texts')
for unit, g in U.groupby('unit'):
    for side, h in g.groupby('side'):
        vals = collections.Counter(h.value.dropna().astype(int))
        ser = collections.Counter(h.series)
        own = h[~h.other_is_unit]
        ov = collections.Counter(own.value.dropna().astype(int))
        out.append(dict(unit=unit, signs=' '.join(sorted(set(h.sign))), side=side, n=len(h),
                        values=' '.join(f'{k}:{v}' for k, v in sorted(vals.items())),
                        max=max(vals) if vals else None,
                        owned_values=' '.join(f'{k}:{v}' for k, v in sorted(ov.items())),
                        series=' '.join(f'{k}:{v}' for k, v in ser.most_common()),
                        tall_share=round((h.series == 'F').mean(), 2),
                        kinds=' '.join(f'{k}:{v}' for k, v in collections.Counter(h.kind).most_common(4)),
                        sites=' '.join(f'{k}:{v}' for k, v in collections.Counter(h.site).most_common(3)),
                        new_texts=int((h.cat == 'Mu').sum())))
T = pd.DataFrame(out); T.to_csv(f'{OUTM}/ceilings.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 70)
P(T[['unit', 'signs', 'side', 'n', 'values', 'max', 'series', 'kinds', 'sites', 'new_texts']].to_string(index=False))

# --- tests of the predictions ---
def vals(unit, side=None, series=None):
    h = U[(U.unit == unit)]
    if side: h = h[h.side == side]
    if series: h = h[h.series.isin(series)]
    return collections.Counter(h.value.dropna().astype(int))

P('\nT1 cup "n cup" values:', dict(sorted(vals('cup', 'before').items())), ' "cup n":', dict(sorted(vals('cup', 'after').items())))
P('T2 paTi values:', dict(vals('paTi')), ' T3 kAl values:', dict(vals('kAl')), ' T4 kalam:', dict(vals('kalam')))
cont = U[U.unit.isin(['cup', 'kalam', 'pot', 'jar', 'kotTai', 'paRai', 'paTi', 'bin', 'chest', 'granary-bin'])].value.dropna().astype(int)
pw = cont.isin([1, 2, 4, 8]).mean()
P(f'W1 share of container counts on 1,2,4,8: {pw:.2f} (n {len(cont)}); 3:{(cont == 3).sum()} 5:{(cont == 5).sum()} 6:{(cont == 6).sum()} 7:{(cont == 7).sum()}')
for u in ['cup', 'kalam', 'jar', 'pot', 'chest', 'kotTai', 'niRai', 'hand', 'dozen', 'seven', 'kAl', 'paTi', 'paRai', 'bin']:
    h = U[U.unit == u]
    if len(h): P(f'T5 {u}: tall share {(h.series == "F").mean():.2f} of {len(h)}')
