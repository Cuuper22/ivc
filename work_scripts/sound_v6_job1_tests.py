#!/usr/bin/env python3
"""Job 1, step 2: words for picture ties, each prediction written here BEFORE any of these numbers was computed.
(Step 1, sound_v6_job1_scan.py, printed only the cells at P<=0.01; none of the facts below was among them.)
Writes work_data/sound_v6/job1_tests.csv."""
from sound_v6_common import *
from scipy.stats import fisher_exact
MSEAL_PIC = {'71': 'Elep', '45': 'Gaur', '41': 'Gaur', '31': 'Zebu', '113': 'Rhin', '95': 'Tigr', '65': 'Buff', '13': 'Bull1', '11': 'Bull1', '17': 'Bull1', '14': 'Bull1'}
M['pic'] = M.fs.map(MSEAL_PIC)
PRED = [
 # (id, sign, word, DEDR, prediction text)
 ('T1', '520', 'vēḷ (pun: vēḻam "elephant", Tamil Lexicon p. 3841 sense 8)', '5544/TL', 'elephant seals carry the chief sign: on NEW-TEXT seals (second catalogue, no first-catalogue partner) whose picture code is the elephant (fs 71), 520 is on more faces than on other new-text seals with a beast'),
 ('T2', '923', 'maruppu "tusk, ivory"', '4720', 'ivory goes with the elephant on seals too: seals (both catalogues, new texts for the second) with the elephant carry 923 more than other beast seals'),
 ('T3', '255', 'mutal "chief", pun mutalai "crocodile"', '4952', 'the gharial tablets of Harappa carry 255: moulded/incised tablets showing the gharial carry 255 more than other pictured tablets of the same site'),
 ('T4', 'sets', 'copper-tablet set words', '', 'a picture brings its words to another object kind: seals showing animal A carry at least one sign of the copper-tablet text(s) whose picture is A (jar and numbers left out) more than seals with other beasts (labels shuffled among beast seals of the same site)'),
 ('T5', '341', 'kalai / māṉ "stag, deer" (the deer sign stands in for the stag picture on M-516, M-517)', '4780', 'the deer signs (341-348) go with the hill-field words: faces carrying a deer sign carry 503 or 615 more than faces overall (both catalogues)'),
 ('T6', '806', 'viḷai "produce, crop"', '5437', 'the plant picture brings produce on NEW texts too: second-catalogue miniature tablets whose partnered first-catalogue copies show a plant are not available, so: first-catalogue moulded tablets with a plant carry the load-carrier 158/154 (produce carried) more than other pictured moulded tablets of the same site'),
]
for p in PRED: print(f'[{p[0]}] {p[1]} {p[2]}: {p[4]}', flush=True)
print('---- computing ----', flush=True)
out = []
def rec(tid, ok, p, txt):
    print(f'[{tid}] -> {"yes" if ok and p <= 0.1 else "direction only" if ok else "no"}: {txt}, P {p:.3g}', flush=True)
    out.append(dict(test=tid, outcome='yes' if ok and p <= 0.1 else 'direction only' if ok else 'no', p=p, result=txt))
# T1
mu = M[~M.partnered & (M.cls == 'seal') & M.pic.notna()]
a = mu[mu.pic == 'Elep'].tok.apply(lambda x: '520' in x); b = mu[mu.pic != 'Elep'].tok.apply(lambda x: '520' in x)
p = fisher_exact([[a.sum(), len(a) - a.sum()], [b.sum(), len(b) - b.sum()]], alternative='greater')[1]
rec('T1', a.mean() > b.mean(), p, f'new-text elephant seals with 520 {a.sum()}/{len(a)} = {a.mean():.0%} against {b.sum()}/{len(b)} = {b.mean():.0%} for other new-text beast seals')
# T2
ls = objs[(objs.kind == 'seal') & objs.pic.notna()]
a1 = ls[ls.pic == 'Elep'].signs.apply(lambda z: '923' in z); b1 = ls[ls.pic != 'Elep'].signs.apply(lambda z: '923' in z)
a2 = mu[mu.pic == 'Elep'].tok.apply(lambda x: '923' in x); b2 = mu[mu.pic != 'Elep'].tok.apply(lambda x: '923' in x)
A, NA, B, NB = a1.sum() + a2.sum(), len(a1) + len(a2), b1.sum() + b2.sum(), len(b1) + len(b2)
p = fisher_exact([[A, NA - A], [B, NB - B]], alternative='greater')[1]
rec('T2', A / NA > B / NB, p, f'elephant seals with 923 {A}/{NA} = {A / NA:.1%} against {B}/{NB} = {B / NB:.1%} for other beast seals (first catalogue {a1.sum()}/{len(a1)}, new texts {a2.sum()}/{len(a2)})')
# T3
t = objs[(objs.kind == 'mtab') & objs.pic.notna()]
ok = []; obs = 0; sims = []
has = t.signs.apply(lambda z: '255' in z).values; g = (t.pic == 'Gavi').values; site = t.site.values
obs = int((has & g).sum())
for _ in range(5000):
    gg = g.copy()
    for s in set(site):
        ii = np.where(site == s)[0]; gg[ii] = rng.permutation(g[ii])
    sims.append(int((has & gg).sum()))
sims = np.array(sims); p = (np.sum(sims >= obs) + 1) / 5001
rec('T3', obs > sims.mean(), p, f'gharial tablets with 255: {obs} of {g.sum()} against {sims.mean():.2f} by shuffle (pictured tablets with 255: {has.sum()} of {len(t)})')
# T4
SETSIGN = collections.defaultdict(set)
for txt, pic in CTAB_SET.items():
    SETSIGN[pic] |= {a for a in txt.split('-') if a not in VAL and a not in ('000', '740')}
bs = objs[(objs.kind == 'seal') & objs.pic.notna() & (objs.pic.isin(set(SETSIGN)))].copy()
def score(labels):
    return int(sum(bool(z & SETSIGN[l]) for z, l in zip(bs.signs, labels)))
lab = bs.pic.values; obs = score(lab); sims = []
st = bs.site.values
for _ in range(2000):
    l = lab.copy()
    for s in set(st):
        ii = np.where(st == s)[0]; l[ii] = rng.permutation(lab[ii])
    sims.append(score(l))
sims = np.array(sims); p = (np.sum(sims >= obs) + 1) / 2001
per = {A: f'{int(sum(bool(z & SETSIGN[A]) for z in bs[bs.pic == A].signs))}/{int((bs.pic == A).sum())}' for A in sorted(set(bs.pic))}
rec('T4', obs > sims.mean(), p, f'beast seals carrying a sign of their own animal\'s copper-tablet text: {obs} against {sims.mean():.1f} by shuffle; per animal {per}')
# T5
DEER = {f'{i:03d}' for i in range(341, 349)}
rows = faces_all('LM')
allm = np.array([bool(set(x) & {'503', '615'}) for x, P, s_, g_ in rows]); sub = np.array([bool(set(x) & {'503', '615'}) for x, P, s_, g_ in rows if set(x) & DEER])
r = share(allm, sub, 'faces with a deer sign (341-348) that carry hill 503 or field 615 (LM)')
rec('T5', *r) if r else rec('T5', False, 1.0, 'too few')
# T6
t = objs[(objs.type == 'TAB:B') & objs.pic.notna()]
has = t.signs.apply(lambda z: bool(z & {'158', '154'})).values; g = (t.pic == 'Phyt').values; site = t.site.values
obs = int((has & g).sum()); sims = []
for _ in range(5000):
    gg = g.copy()
    for s in set(site):
        ii = np.where(site == s)[0]; gg[ii] = rng.permutation(g[ii])
    sims.append(int((has & gg).sum()))
sims = np.array(sims); p = (np.sum(sims >= obs) + 1) / 5001
rec('T6', obs > sims.mean(), p, f'plant moulded tablets with carrier 158/154: {obs} of {g.sum()} against {sims.mean():.2f} by shuffle (objects, copies not collapsed)')
D = pd.DataFrame(out); P = pd.DataFrame(PRED, columns=['test', 'sign', 'word', 'dedr', 'prediction'])
P.merge(D, on='test').to_csv(f'{OUT6}/job1_tests.csv', index=False)
