#!/usr/bin/env python3
"""Job 1, redesigns for the four tests that did not come true (one each), written before running.
Appends to work_data/sound_v6/job1_tests.csv as stage 'b'."""
from sound_v6_common import *
from scipy.stats import fisher_exact
PRED = [
 ('T1b', '520', 'vēḷ / vēḻam', 'the elephant-chief pun on the copper tablets: the elephant copper tablets (923 sets) are the only copper set with no spear; so test the other way round: sealings and tags (first catalogue, never printed for this pun) whose face carries 520 show the elephant more than other pictured sealings/tags'),
 ('T2b', '923', 'maruppu "tusk, ivory"', 'ivory is written on ivory: 923 sits on ivory/bone rods (both catalogues) more than on all faces'),
 ('T4b', 'sets', 'set words', 'leave out the unicorn (the default civic seal): seals with a special beast (tiger, rhinoceros, buffalo, elephant, gaur, goat, composite) carry a sign of their own animal\'s copper-tablet text more than seals of the other special beasts (shuffled within site)'),
 ('T5b', '341', 'kalai / māṉ', 'deer signs are record words: faces with a deer sign (341-348) sit on tablets (copper, moulded, incised) more than all faces (both catalogues)'),
]
for p in PRED: print(f'[{p[0]}] {p[1]} {p[2]}: {p[3]}', flush=True)
print('---- computing ----', flush=True)
out = []
def rec(tid, ok, p, txt):
    print(f'[{tid}] -> {"yes" if ok and p <= 0.1 else "direction only" if ok else "no"}: {txt}, P {p:.3g}', flush=True)
    out.append(dict(test=tid, outcome='yes' if ok and p <= 0.1 else 'direction only' if ok else 'no', p=p, result=txt))
t = objs[(objs.kind == 'tag') & objs.pic.notna()]
a = t[t.signs.apply(lambda z: '520' in z)].pic == 'Elep'; b = t.pic == 'Elep'
r = share(b, a, 'pictured tags/sealings with 520 that show the elephant')
rec('T1b', *r) if r else rec('T1b', False, 1.0, f'too few: pictured tags with 520 {len(a)}, elephant tags {int(b.sum())}')
r = on_kind('923', 'rod', 'LM'); rec('T2b', *r) if r else rec('T2b', False, 1.0, 'too few')
SETSIGN = collections.defaultdict(set)
for txt, pic in CTAB_SET.items(): SETSIGN[pic] |= {a for a in txt.split('-') if a not in VAL and a not in ('000', '740')}
bs = objs[(objs.kind == 'seal') & objs.pic.isin(set(SETSIGN) - {'Bull1', 'Hare'})].copy()
lab = bs.pic.values; st = bs.site.values
score = lambda L: int(sum(bool(z & SETSIGN[l]) for z, l in zip(bs.signs, L)))
obs = score(lab); sims = []
for _ in range(3000):
    l = lab.copy()
    for s in set(st):
        ii = np.where(st == s)[0]; l[ii] = rng.permutation(lab[ii])
    sims.append(score(l))
sims = np.array(sims); p = (np.sum(sims >= obs) + 1) / 3001
rec('T4b', obs > sims.mean(), p, f'special-beast seals with a sign of their own animal\'s copper text: {obs} of {len(bs)} against {sims.mean():.1f} by shuffle')
r = on_kind({f'{i:03d}' for i in range(341, 349)}, {'ctab', 'mtab'}, 'LM'); rec('T5b', *r) if r else rec('T5b', False, 1.0, 'too few')
P = pd.DataFrame(PRED, columns=['test', 'sign', 'word', 'prediction']).merge(pd.DataFrame(out), on='test')
old = pd.read_csv(f'{OUT6}/job1_tests.csv', dtype=str)
pd.concat([old[~old.test.str.endswith('b')], P]).to_csv(f'{OUT6}/job1_tests.csv', index=False)
