#!/usr/bin/env python3
"""COPPER step 6: where the copies lie.

Findspot levels: BUILDING = excavation area + block-house (Mohenjo-daro house number, e.g. VSA 1I); AREA = the
excavation area (DK-, DKG, VSA, HR ...; taken from the register prefix when the area field is blank).
REGISTER LOT: the excavator's running find number (DK 10141, VS 1988, HR 4337 ...). Finds were numbered as they came out
of the ground, so two finds with close numbers in one register series came out at about the same time and place;
one number with a/b or (1)/(2) is one find lot. Series: DK (main DK area numbers), DK-i, DK-B, DK-C, DK-E, HR, VS, SD, L.
Plate suffixes in the catalogue (93.9, 103.1, CXVII:12) are stripped.
SECOND CATALOGUE LOCUS: an area code (work in jobs/out/second_catalogue.md), used as an independent check.

Tests (copies of one set against copper tablets of different sets):
 T6.1 same register lot, and register numbers within 100 of each other in one series;
 T6.2 same building, same area;
 T6.3 second catalogue: same locus;
 Control: set labels dealt at random among the copper tablets that have that kind of findspot, 10,000 deals.
 T6.4 which different sets share a lot or a building (an office holding many kinds).

Predictions written 2026-11-17 before the numbers:
 P6.1 Copies of one set share a register lot or lie within 100 numbers far more than chance (at least 3 times), so a set
      was found as a batch, a store of tokens.
 P6.2 Yet one set is also found in more than one area (the big stag, hare and archer sets in 3+ areas): batches were
      kept in several places, not all in one room.
 P6.3 Lots that hold copper tablets hold several different sets (an office holding many kinds).
Writes work_data/copper/spots_objects.csv, spots_lots.csv, log_6.txt.
"""
import sys; sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from copper_common import *
say = say_to(f'{OUT}/log_6.txt')
L = pd.read_csv(f'{OUT}/objects.csv', dtype=str).fillna('')
Mm = pd.read_csv(f'{OUT}/m77_objects.csv', dtype=str).fillna('')
exec(open(f'{ROOT}/work_scripts/copper_2_pairs.py').read().split('# ---- text families')[1].split('rng = np.random')[0])
L['fam'] = L.set_text.map(FAM).fillna(L.set_text)

def reg(e):
    e = e.strip()
    if e in ('', '-', '--') or e.startswith('-') or e == 'MD-SE': return ('', None, '')
    e = re.sub(r'CXVI+I*:\d+$', '', e).strip()
    e = re.sub(r'(93|103)\.\d+$', '', e)          # DK-G plate references (DK344793.9 = DK 3447, plate 93 no. 9)
    m = re.match(r'^(DK-[iBCE]|DK|HR|VS-N|VS|SD|L|E)\s*-?\s*(\d+)\s*([a-z]|\(\d\))?', e)
    if not m: return ('', None, '')
    ser, num, suf = m.group(1), m.group(2), m.group(3) or ''
    if ser == 'DK' and len(num) >= 7:          # DK + register number + plate reference run together (DK344793.9, DK5444818)
        num = num[:5] if num.startswith('1') else num[:4]
    return (ser, int(num), suf)
L['series'], L['regno'], L['regsuf'] = zip(*[reg(e) for e in L.exc])
def area_of(r):
    a = r.area.strip()
    if a in ('', '--'):
        return {'DK': 'DK-', 'DK-i': 'DK-', 'HR': 'HR-', 'VS': 'VS-', 'VS-N': 'VS-', 'SD': 'SD-', 'L': 'L-'}.get(r.series, '')
    return a
L['area2'] = [area_of(r) for r in L.itertuples()]
L['major'] = L.area2.str[:2].replace({'DK': 'DK', 'HR': 'HR', 'VS': 'VS', 'SD': 'SD', 'L-': 'L'})
L['building'] = [f'{r.area2}|{r.bh}' if r.bh not in ('', '--') else '' for r in L.itertuples()]
L[['cisi', 'obj', 'set_text', 'fam', 'pic', 'area2', 'major', 'building', 'room', 'ft', 'series', 'regno', 'regsuf', 'bin']].to_csv(f'{OUT}/spots_objects.csv', index=False)
say(f'copper tablets {len(L)}; with a register number {L.regno.notna().sum()}; with a building {(L.building != "").sum()}; with an area {(L.area2 != "").sum()}')

rng = np.random.default_rng(9)
def pair_test(D, close, label, within=None, n=10000):
    D = D.reset_index(drop=True); fam = D.fam.values
    idx = list(itertools.combinations(range(len(D)), 2))
    if within is not None: idx = [(i, j) for i, j in idx if D[within][i] == D[within][j]]
    if not idx: say(f'{label}: no pairs'); return
    I = np.array([i for i, _ in idx]); J = np.array([j for _, j in idx])
    cl = np.array([close(D.iloc[i], D.iloc[j]) for i, j in idx])
    def stat(f):
        same = f[I] == f[J]
        return cl[same].sum(), same.sum(), cl[~same].mean() if (~same).any() else 0
    s, ns, other = stat(fam)
    groups = D[within].values if within is not None else np.zeros(len(D))
    sims = []
    for _ in range(n):
        f = fam.copy()
        for g in set(groups):
            m = np.where(groups == g)[0]; f[m] = rng.permutation(f[m])
        sims.append(stat(f)[0])
    sims = np.array(sims)
    say(f'{label}: same-set pairs {ns}, close {s} ({s / max(ns, 1):.3f}); different-set pairs close {other:.3f}; '
        f'random deals mean {sims.mean():.2f}; ratio {s / max(sims.mean(), 1e-9):.2f}; P {np.mean(sims >= s):.4f}')

R = L[L.regno.notna()].copy()
pair_test(R, lambda a, b: a.series == b.series and a.regno == b.regno, 'T6.1a same register lot (one number)', within='series')
pair_test(R, lambda a, b: a.series == b.series and abs(a.regno - b.regno) <= 100, 'T6.1b register numbers within 100', within='series')
pair_test(R, lambda a, b: a.series == b.series and abs(a.regno - b.regno) <= 500, 'T6.1c register numbers within 500', within='series')
B = L[L.building != ''].copy()
pair_test(B, lambda a, b: a.building == b.building, 'T6.2a same building (area + house), among tablets with a building', within='major')
A = L[L.area2 != ''].copy()
pair_test(A, lambda a, b: a.area2 == b.area2, 'T6.2b same area')
pair_test(A, lambda a, b: a.major == b.major, 'T6.2c same part of the city (DK / HR / VS / SD / L)')
M2 = Mm.copy(); M2['fam'] = M2.set_text.map(FAM).fillna(M2.set_text)
pair_test(M2, lambda a, b: a.locus == b.locus, 'T6.3 second catalogue: same locus')

# ---- each set: spread
rows = []
for f, g in L.groupby('fam'):
    if len(g) < 2: continue
    rows.append(dict(family=f, copies=len(g), areas=dict(collections.Counter(x for x in g.area2 if x)),
                     parts=len(set(x for x in g.major if x)), buildings=dict(collections.Counter(x for x in g.building if x)),
                     lots=sorted(f'{s} {int(n)}{x}' for s, n, x in zip(g.series, g.regno, g.regsuf) if s),
                     m77_loci=dict(collections.Counter(Mm[Mm.set_text.map(FAM).fillna(Mm.set_text) == f].locus))))
SP = pd.DataFrame(rows).sort_values('copies', ascending=False); SP.to_csv(f'{OUT}/spots_sets.csv', index=False)
for r in SP.itertuples(): say(f'  {r.family} x{r.copies}: parts {r.parts}; areas {r.areas}; buildings {r.buildings}; lots {r.lots}; loci {r.m77_loci}')

# ---- T6.4 lots and buildings with several sets
rows = []
for key, g in list(R.groupby(['series', 'regno'])) + [(('building', b), g) for b, g in B.groupby('building')]:
    if len(g) < 2: continue
    rows.append(dict(where=f'{key[0]} {key[1]}', objects=len(g), sets=len(set(g.fam)),
                     what='; '.join(f'{r.cisi or r.obj}:{r.set_text}:{r.pic}' for r in g.itertuples())))
LT = pd.DataFrame(rows); LT.to_csv(f'{OUT}/spots_lots.csv', index=False)
say('lots / buildings holding 2+ copper tablets:')
for r in LT.itertuples(): say(f'  {r.where}: {r.objects} tablets, {r.sets} sets: {r.what}')
