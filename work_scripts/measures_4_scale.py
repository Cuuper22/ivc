#!/usr/bin/env python3
"""Steps 4-6: litres, the pay scale, why cups are never 5.

Ladder used (built in steps 1-2): 1 cup (700) = 9.24 L (Wells' three measured pots: 27.30/3, 55.56/6, 65.89/7);
1 kalam (705/706) = 12 cups; 1 tūṇi = 4 cups; 1 patakku = 2 cups; 1 paṭi (320) = 1/8 cup; kōṭṭai (575) = 21 cups.
Grain: wheat/barley about 0.75-0.8 kg per litre (bulk density); a person eats about 0.5-1 kg of grain a day.

PREDICTIONS (written before the first run).
 P1 (year/month) A kalam grade is a YEARLY allowance paid MONTHLY in cups: n kalam a year = 12n cups = n cups a
    month. On objects carrying both a kalam count and a cup count, cups = kalam number more often than chance.
 P2 (crew split) A kalam (12 cups) is split over a crew: on tablets with a person count c and a cup count k,
    c x k = 12 more often than chance.
 P3 The 3-kalam grade = one person's grain for a year: 36 cups x 9.24 L / 365 days lands in 0.5-1 kg a day.
 P4 The "monthly allowance" paṭi-month (320-920) is a sensible month for one person only if counted in many paṭi;
    1 paṭi a day x 30 = 30 paṭi = 3.75 cups a month: inside the cup band 2-4.
 P5 Never 5 cups: cup counts are the shares of a 12-cup kalam that come out whole (12/1..12/6 and 12/12):
    1, 2, 3, 4, 6, (12). 5 does not divide 12, so 5 cups is never written; 7-11 never either. Prediction: across
    every cup count in both catalogues, counts that divide 12 are 98%+.
"""
from measures_common import *
from measures_3_sums import obj_numbers
L_CUP = 9.24; KG_L = (0.75, 0.80)

on = {}
on.update(obj_numbers('L')); on.update(obj_numbers('Mu'))

# P1
rows = []
for k, v in on.items():
    ka = [r['value'] for r in v if r['unit'] == 'kalam']; cu = [r['value'] for r in v if r['unit'] == 'cup']
    if k[0] in ('-', ''): continue
    if ka and cu: rows.append((k[0], ka, cu, ' | '.join(dict.fromkeys(r['text'] for r in v))))
match = sum(any(c in ka for c in cu) for _, ka, cu, _ in rows)
allcups = collections.Counter(r['value'] for v in on.values() for r in v if r['unit'] == 'cup')
tot = sum(allcups.values())
pexp = np.mean([sum(allcups[x] for x in set(ka)) / tot for _, ka, cu, _ in rows]) if rows else 0
print(f'P1 objects with kalam and cup counts: {len(rows)}; cups = kalam number on {match}; chance per object about {pexp:.2f} '
      f'-> P {binomtest(match, len(rows), pexp, alternative="greater").pvalue:.3g}')
for r in rows: print('   ', r[0], 'kalam', r[1], 'cups', r[2], '::', r[3])
distinct = {r[3] for r in rows}
dmatch = sum(any(any(c in ka for c in cu) for (_, ka, cu, tt) in rows if tt == t) for t in distinct)
print(f'    distinct texts: {len(distinct)}; cups = kalam number on {dmatch}')

# P2
PEOPLE = {'817', '861', '156', '154', '151', '158', '140', '142', '176', '097', '137', '100', '090'}
crew = []
for cisi, g in d[d.kind == 'mtab'].groupby('cisi'):
    if cisi in ('-', ''): continue
    cups = []; ppl = []
    for t in g.tok:
        for (a, b, v, s) in runs(t):
            if not v: continue
            right = t[b] if b < len(t) else 'END'; left = t[a - 1] if a else 'START'
            if right == '700': cups.append(v)
            elif right in PEOPLE or (right == 'END' and left in PEOPLE): ppl.append((v, right if right in PEOPLE else left))
    if cups and ppl: crew.append((cisi, cups[0], ppl, ' | '.join(' '.join(t) for t in g.tok)))
hit = sum(any(c * p[0] == 12 for p in pp) for _, c, pp, _ in crew)
print(f'\nP2 tablets with a cup count and a person count: {len(crew)}; person x cups = 12 on {hit}')
for c in crew[:40]: print('   ', c[0], 'cups', c[1], 'people', c[2], '::', c[3])
dist = collections.Counter((c, tuple(p[0] for p in pp)) for _, c, pp, _ in crew)
print('    combos:', dict(dist))

# P3-P4 and the pay table
def litres(n_cup): return n_cup * L_CUP
def kgday(n_cup, days): return tuple(round(litres(n_cup) * k / days, 2) for k in KG_L)
print('\nP3 3 kalam a year = 36 cups =', round(litres(36), 1), 'L; per day kg', kgday(36, 365))
print('P4 30 paTi (1 a day) =', 30 / 8, 'cups =', round(litres(30 / 8), 1), 'L a month; kg/day', kgday(30 / 8, 30))
PAY = [
    ('three-kalam chief (705-033-520, 54 seals)', 36, 'year'),
    ('three-kalam grade + 3 cups chit (H-774, H-1811..1816, H-177)', 3, 'month'),
    ('five kalam (005-706 copper tablets M-513..515; 705-033-032 new-text copper tablets)', 60, 'year'),
    ('three kalam, crescent-horn house (706-033-923-740, 7 copper tablets)', 36, 'year'),
    ('bondsman, junior hand: 4 cups (004-700-097-400, 4 tablets)', 4, 'month'),
    ('cultivator chit (137-400, 7 copies; cup face where present)', None, 'month'),
    ('crew chit: 3 hands, 3 loads, 4 cups (21 tablets)', 4, 'month'),
    ('crew chit, 3 hands, 3 loads, 3 cups (H-2238)', 3, 'month'),
    ('six-cup issue with niRai line (H-801, H-1881)', 6, 'month'),
    ('one paTi a day for a month (320-920 "monthly allowance")', 30 / 8, 'month'),
]
print('\nPay table (cups; litres; kg grain a day for one person if the period is right):')
out = []
for who, cups, per in PAY:
    if cups is None: print(f'  {who}: no amount on the chit itself'); continue
    days = 365 if per == 'year' else 30
    out.append(dict(who=who, cups=round(cups, 2), period=per, litres=round(litres(cups), 1),
                    cups_a_month=round(cups / 12 if per == 'year' else cups, 2), kg_day=kgday(cups, days)))
    print(f'  {who}: {cups:.2f} cups/{per} = {litres(cups):.1f} L; {out[-1]["cups_a_month"]} cups a month; kg/day {kgday(cups, days)}')
pd.DataFrame(out).to_csv(f'{OUTM}/pay_scale.csv', index=False)

# cultivator chit: what is on its other faces
print('\ncultivator 137 objects (all faces):')
for cisi in d[d.tok.apply(lambda t: '137' in t)].cisi.unique():
    if cisi in ('-', ''): continue
    print('   ', cisi, ' | '.join(' '.join(t) for t in d[d.cisi == cisi].tok))
print('bondsman 097 objects (all faces):')
for cisi in d[d.tok.apply(lambda t: '097' in t)].cisi.unique():
    if cisi in ('-', ''): continue
    print('   ', cisi, ' | '.join(' '.join(t) for t in d[d.cisi == cisi].tok))

# P5
U = pd.read_csv(f'{OUTM}/unit_counts.csv')
c = U[(U.unit == 'cup')].value.dropna().astype(int)
cb = U[(U.unit == 'cup') & (U.side == 'before')].value.dropna().astype(int)
div = c.isin([1, 2, 3, 4, 6, 12]).mean()
print(f'\nP5 cup counts (both sides, both catalogues) dividing 12: {div:.3f} of {len(c)}; values {dict(collections.Counter(c))}')
# rival: binary (cup counts 1-7 under an 8-cup next unit) - predicts 5 and 7 at roughly the rate of 6 and 3
print('    5 written:', int((c == 5).sum()), ' 6 written:', int((c == 6).sum()), ' 7 written:', int((c == 7).sum()))
