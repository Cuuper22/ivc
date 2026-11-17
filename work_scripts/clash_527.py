#!/usr/bin/env python3
"""CLASH 527 (+525, 526): A = kaaval "guard" (DEDR 1416, same root as the carrier sign kaa "keeper") against
B = katavu "door" (DEDR 1187).  Family F = {525, 526, 527}; tests run on F pooled and on 527 alone.

PREDICTIONS, written before this script was first run.  Honest note: I had read the first-catalogue profile (527 last in
52 of 59, after the gate 550/555/554 in 50 of 59, jar on 7 of 63 faces; 525 only on tablets, 9 of 11 before the comb 400;
no 060 after it) in eight_signs.md and sound_list_v4.md, so those numbers are not clean.  The new texts (9 faces carry
527, none carry 525 or 526) are the clean column, and small.  'high'/'low' = against what ANY sign does.
Class closers = spear 520, comb 400, man 090, carriers 151-158: the signs that stand in the jar's place and name what a person is.

 id  what is counted                                          A (guard)  B (door)
 G1  the jar 740 on the same face                              low        high     (a class sign takes the jar's place; a door is owned like any thing)
 G2  last sign of the text                                     high       low      (a class sign closes; a place/thing word is followed by ending or name)
 G3  060 (in) or a ward jar 741/742/745 right after            low        high     (a door/gate-post used as an address is followed by "in" or a ward)
 G4  a count right before or after                             low        high     (doors are counted; a guard title is not)
 G5  face is a seal (not tablet, tag, pot)                     high       low      (a person's class on his own stone; a door on tags/sealings/records)
 G6  a tag/sealing (clay sealing that was pressed on a fastening)   low  high     (door fastenings were sealed; a title is not)
 G7  the sign two places back (before the gate) is a name part in the parse (crest/self/tag), not an opener or count: high / low
     (a person is named, then his gate-guard title; an address starts with a time/place/count word)
 G8  frames (previous sign, next sign) shared with the class closers, against frequency-matched peers:  A high  B -- ; and frames
     shared with place/thing words (590 605 711 575 540 615 503 692 820 550): A low B high  (reported, one-sided P)
Decision rule as in clash_335.py.  Outputs: work_data/clash/527_tests.csv
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clash_common import *

NAMES = {'A': 'kaaval guard', 'B': 'katavu door', 'none': '-'}
GATE = {'550', '554', '555'}
NAME_ROLES = {'crest', 'self', 'tag'}
CLASS = {'520', '400', '090', '151', '153', '154', '155', '156', '157', '158'}
THING = {'590', '605', '711', '575', '540', '615', '503', '692', '820', '550'}
FAMS = {'F (525+526+527)': {'525', '526', '527'}, '527 alone': {'527'}}


def g7(r, i):
    # sign two places before the family sign, when the one right before is a gate sign
    if i is None or i < 2 or r.tok[i - 1] not in GATE: return False
    return r.roles[i - 2] in NAME_ROLES


tests = [
    ('G1', 'jar 740 on the face', lambda r, i: '740' in r.tok, 'face', dict(A='low', B='high'), None),
    ('G2', 'last sign of the text', lambda r, i: i == len(r.tok) - 1, 'occ', dict(A='high', B='low'), None),
    ('G3', '060 or ward jar right after', lambda r, i: i + 1 < len(r.tok) and r.tok[i + 1] in ('060', '741', '742', '745'), 'occ', dict(A='low', B='high'), None),
    ('G4', 'count right before/after', lambda r, i: (i > 0 and r.tok[i - 1] in CNTS) or (i + 1 < len(r.tok) and r.tok[i + 1] in CNTS), 'occ', dict(A='low', B='high'), None),
    ('G5', 'face is a seal', lambda r, i: r.kind == 'seal', 'face', dict(A='high', B='low'), None),
    ('G6', 'face is a tag / sealing', lambda r, i: r.kind == 'tag', 'face', dict(A='low', B='high'), None),
    ('G7', 'sign before the gate is a name part', g7, 'occ', dict(A='high', B='low'), lambda r: any(t in GATE for t in r.tok)),
]
rows = []
print('[clash_527] running tests ...', flush=True)
for fam, S in FAMS.items():
    for tag, lab, fn, scope, says, sub in tests:
        for cat in ('L', 'Mu'):
            for unit in ('faces', 'distinct'):
                if tag == 'G7':
                    # base for G7: every occurrence of a gate sign's follower; handle by testing the family against all followers of a gate
                    res = occ_test(S, fn, cat, unit, 'occ')
                else:
                    res = occ_test(S, fn, cat, unit, scope)
                r = line(tag, lab, says, res, NAMES); r['signs'] = fam; r['catalogue'] = cat; r['unit'] = unit
                rows.append(r)

# G8 frames
for lab, B, says in [('frames shared with class closers', CLASS, dict(A='high', B='low')), ('frames shared with place/thing words', THING, dict(A='low', B='high'))]:
    for fam, S in FAMS.items():
        f = frames_shared(S, B)
        dr = 'high' if f['obs'] > f['median'] else 'low'
        pt = [h for h, s in says.items() if s == dr]
        rows.append(dict(test='G8', what=lab, k=f['obs'], n=f['npeers'], share='', base=f"median {f['median']:.0f}", P=f"{f['p']:.2g}",
                         points_to=NAMES[pt[0]] if pt and f['p'] <= 0.1 else 'direction only' if pt else '-', strength='P<=0.1' if f['p'] <= 0.1 else 'direction only',
                         signs=fam, catalogue='L+Mu', unit='distinct'))

# extra, reported only: what follows each drawing, and the sites
for s in ('525', '526', '527'):
    nx = collections.Counter(); sites = collections.Counter(); kinds = collections.Counter()
    for r in FACES.itertuples():
        for i, t in enumerate(r.tok):
            if t == s: nx[r.tok[i + 1] if i + 1 < len(r.tok) else '$'] += 1; sites[r.site] += 1; kinds[r.kind] += 1
    print(f'{s}: next {dict(nx.most_common(5))}; kinds {dict(kinds)}; sites {dict(sites)}', flush=True)

df = pd.DataFrame(rows)
df.to_csv(f'{OUTC}/527_tests.csv', index=False)
print(df[['test', 'what', 'signs', 'catalogue', 'unit', 'k', 'n', 'share', 'base', 'P', 'points_to', 'strength']].to_string(index=False))
for fam in FAMS:
    for unit in ('distinct', 'faces'):
        t = df[(df.signs == fam) & (df.unit == unit) & (df.strength == 'P<=0.1')]
        print(f'TALLY {fam} {unit} P<=0.1:', t.groupby('points_to').size().to_dict())
    t = df[(df.signs == fam) & (df.catalogue == 'Mu') & (df.strength.isin(['P<=0.1', 'direction only']))]
    print(f'NEW TEXTS {fam} any direction:', t.groupby('points_to').size().to_dict(), flush=True)
