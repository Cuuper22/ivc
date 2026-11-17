#!/usr/bin/env python3
"""Measures, second round: the five leads left open by measures.md. Both catalogues (Lipi + the 1,183 new texts).

PREDICTIONS, written before any number below was computed:
 (a) KOTTAI 575 is the rung above the kalam, worth 6 kalam or more. Then: (a1) on any line where 575 and a counted kalam
     stand together, the kalam count is 5 or less; (a2) the count owned by 575 (after it) stays small, 1-3, like the kAl;
     (a3) the stacked seven before it (017-575, "seven kottai") is the biggest grain amount in the corpus and goes on
     seals of big houses: those seals are bigger than seals in general.
 (b) every tablet that carries a person count and a cup count multiplies to 6 or 12 (half or whole kalam):
     distinct texts hit {6, 12} far above a shuffle of cup counts across those tablets.
 (c) NIRAI 171 ("full weight") takes 5 and 3: these are the non-binary steps of the stone weight system
     (harappa.com: binary in the lower weights, decimal with fractional thirds in the higher). Prediction: nirai counts
     are only 3 and 5 (and 10s), never the binary 2, 4, 8 that dominate the cup; and a nirai line sits on account
     tablets beside a cup count (a weighed amount of grain).
 (d) a count after the "monthly allowance" phrase 320-920 never exceeds one person's month (30 paTi = 3.75 cups).
 (e) joining the faces of each multi-face tablet into one record: (e1) a number on one face repeats a number on another
     face more than shuffled; (e2) a total (one number = sum of the others, across faces) shows up more than shuffled;
     (e3) cup count on one face = kalam count on the other (monthly cups x 12 = yearly kalam) on most records with both.
Outputs: work_data/measures/m2_*.csv
"""
import collections
from measures_common import *
from time_common import T as TT
from scipy.stats import binomtest

rng2 = np.random.default_rng(5)
Mu = M[~M.partnered]

def lines(cat='LM'):
    out = []
    if 'L' in cat:
        out += [(r.obj, r.id, r.site, r.kind, tuple(r.tok)) for r in d.itertuples()]
    if 'M' in cat:
        out += [(f'M{r.textnum}', f'M{r.textnum}', r.site_l, r.kind, tuple(r.tok)) for r in Mu.itertuples()]
    return out
LN = lines()

def run_after(t, i):
    for (a, b, v, s) in runs(t):
        if a == i + 1: return v, s
    return None
def run_before(t, i):
    for (a, b, v, s) in runs(t):
        if b == i: return v, s
    return None

# ---------------- (a) kottai ----------------
print('== (a) kottai 575')
A = []
for o, f, site, kind, t in LN:
    if '575' not in t: continue
    for i, x in enumerate(t):
        if x != '575': continue
        aft = run_after(t, i); bef = run_before(t, i)
        kal = [run_after(t, j) for j, y in enumerate(t) if y in ('705', '706')]
        A.append(dict(obj=o, face=f, site=site, kind=kind, text='-'.join(t), before=bef, after=aft, kalam_counts=[k for k in kal if k]))
A = pd.DataFrame(A); A.to_csv(f'{OUTM}/m2_kottai.csv', index=False)
print('lines with 575:', len(A))
print('count after 575:', collections.Counter(x[0] for x in A.after.dropna() if x).most_common())
print('count before 575:', collections.Counter(x[0] for x in A.before.dropna() if x).most_common())
both = A[A.kalam_counts.str.len() > 0]
print('a1 lines with 575 and a counted kalam:'); print(both[['face', 'site', 'text', 'after', 'kalam_counts']].to_string())
seven = A[A.before.apply(lambda x: bool(x) and x[0] == 7)]
print(f'a3 seven-kottai lines: {len(seven)}; jar follows 575 on', sum('017-575-740' in t for t in seven.text))
fa = TT[TT.seal & TT.face_mm2.notna()]
s7 = fa[fa.faces.apply(lambda fs: any('017-575' in '-'.join(f) for f in fs))]
from scipy.stats import mannwhitneyu
if len(s7) > 2:
    print(f'a3 seven-kottai seals median face {s7.face_mm2.median():.0f} mm2 (n {len(s7)}) against all seals {fa.face_mm2.median():.0f}; '
          f'one-sided P {mannwhitneyu(s7.face_mm2, fa.face_mm2, alternative="greater").pvalue:.3f}; median signs {s7.nsign.median()} against {fa.nsign.median()}')

# ---------------- (b) person x cup ----------------
print('\n== (b) person count x cup count')
PEOPLE = {'817', '861', '156', '154', '151', '158', '140', '142', '176', '097', '137', '100', '090'}
recs = collections.defaultdict(list)
for o, f, site, kind, t in LN:
    if kind in ('mtab', 'ctab', 'tag', 'tablet', 'miniature tablet') or o.startswith('M') and kind != 'seal':
        recs[o].append(t)
crew = []
for o, faces in recs.items():
    cups, ppl = [], []
    for t in faces:
        for (a, b, v, s) in runs(t):
            if not v: continue
            right = t[b] if b < len(t) else 'END'; left = t[a - 1] if a else 'START'
            if right == '700': cups.append(v)
            elif right in PEOPLE: ppl.append((v, right))
            elif right == 'END' and left in PEOPLE: ppl.append((v, left))
    if cups and ppl:
        crew.append(dict(obj=o, cup=cups[0], person=ppl[0][0], who=ppl[0][1], prod=cups[0] * ppl[0][0], text=' | '.join('-'.join(t) for t in faces)))
C = pd.DataFrame(crew); C.to_csv(f'{OUTM}/m2_crew.csv', index=False)
C['hit'] = C['prod'].isin([6, 12])
Cd = C.drop_duplicates('text')
def shuf(df, n=20000):
    cu = df.cup.values; pe = df.person.values; k = []
    for _ in range(n): k.append(np.isin(rng2.permutation(cu) * pe, [6, 12]).sum())
    k = np.array(k); return k.mean(), (k >= df.hit.sum()).mean()
for lab, df in [('all tablets', C), ('distinct texts', Cd)]:
    m, p = shuf(df)
    print(f'{lab}: {df.hit.sum()} of {len(df)} multiply to 6 or 12; shuffled {m:.1f}; P {p:.4f}')
print(Cd[['obj', 'cup', 'person', 'who', 'prod', 'text']].to_string())

# ---------------- (c) nirai ----------------
print('\n== (c) nirai 171')
N = []
for o, f, site, kind, t in LN:
    for i, x in enumerate(t):
        if x == '171':
            aft = run_after(t, i); N.append(dict(obj=o, face=f, site=site, kind=kind, text='-'.join(t), after=aft[0] if aft else None, series=aft[1] if aft else None))
N = pd.DataFrame(N); N.to_csv(f'{OUTM}/m2_nirai.csv', index=False)
nc = collections.Counter(N.after.dropna().astype(int))
print('counts after 171:', nc.most_common(), ' series:', collections.Counter(N.series.dropna()).most_common())
cupc = collections.Counter()
for o, f, site, kind, t in LN:
    for i, x in enumerate(t):
        if x == '700':
            b = run_before(t, i)
            if b and b[0]: cupc[b[0]] += 1
tot = sum(cupc.values()); p35 = (cupc[3] + cupc[5]) / tot
n171 = sum(nc.values()); k35 = nc[3] + nc[5]
print(f'cup count distribution {sorted(cupc.items())}; share of 3 or 5 among cup counts {p35:.3f}')
print(f'c: nirai counts that are 3 or 5: {k35} of {n171}; P under the cup distribution {binomtest(k35, n171, p35, alternative="greater").pvalue:.2g}')
print(f'   nirai counts 2/4/8: {nc[2] + nc[4] + nc[8]}; cup counts 2/4/8 share {(cupc[2] + cupc[4] + cupc[8]) / tot:.3f}')
objs171 = set(N.obj)
withcup = [o for o in objs171 if o in recs and any('700' in t for t in recs[o])]
print(f'   objects with 171 that also carry a cup sign: {len(withcup)} of {len(objs171)}: ', {o: ' | '.join("-".join(t) for t in recs[o]) for o in withcup})
print('   kinds with 171:', collections.Counter(N.kind).most_common())

# ---------------- (d) monthly allowance ----------------
print('\n== (d) after 320-920')
Dm = []
for o, f, site, kind, t in LN:
    s = '-'.join(t)
    for i in range(len(t) - 1):
        if t[i] == '320' and t[i + 1] == '920':
            nxt = t[i + 2:i + 5]
            aft = run_after(t, i + 1)
            Dm.append(dict(obj=o, face=f, site=site, kind=kind, text=s, next='-'.join(nxt), count=aft[0] if aft else None,
                           unit_after=t[i + 2 + (runs(t[i + 2:])[0][1] if aft else 0)] if aft and i + 2 + runs(t[i + 2:])[0][1] < len(t) else ''))
Dm = pd.DataFrame(Dm); Dm.to_csv(f'{OUTM}/m2_month.csv', index=False)
print(Dm[['face', 'site', 'kind', 'text', 'next', 'count', 'unit_after']].to_string())
print('what follows the phrase:', collections.Counter(Dm.next.str.split('-').str[0]).most_common())

# ---------------- (e) joined multi-face records ----------------
print('\n== (e) multi-face tablets as one record')
CE = pd.read_csv(f'{ROOT}/work_data/corpus_english.csv', dtype=str).fillna('')
MF = objs[(objs.nfaces > 1) & objs.kind.isin(['mtab', 'ctab', 'tag'])]
rows = []
for o, r in MF.iterrows():
    nums = []
    for fi, t in enumerate(r.faces):
        for (a, b, v, s) in runs(t):
            if v: nums.append((fi, v, t[b] if b < len(t) else 'END', t[a - 1] if a else 'START'))
    eng = CE[CE.object_id == o].sort_values('face_id')
    # one record: who-face first (the face without a cup count), amount face second
    order = sorted(range(len(r.faces)), key=lambda i: any(x == '700' for x in r.faces[i]))
    ce_by = dict(zip(eng.face_id.str.split('.').str[1].astype(int) - 1, eng.english))
    rec_en = ' '.join(ce_by.get(i, '') for i in order)
    rows.append(dict(obj=o, cisi=r.cisi, site=r.site, kind=r.kind, area=r.area, nf=r.nfaces,
                     text=' | '.join('-'.join(r.faces[i]) for i in order), english=rec_en, nums=nums))
R = pd.DataFrame(rows)
R[['obj', 'cisi', 'site', 'kind', 'area', 'nf', 'text', 'english']].to_csv(f'{OUTM}/m2_records.csv', index=False)
print('multi-face account objects:', len(R))
def cross_rep(nl):
    a = [v for f, v, _, _ in nl]; fs = [f for f, v, _, _ in nl]
    return any(a[i] == a[j] and fs[i] != fs[j] for i in range(len(a)) for j in range(i + 1, len(a)))
def cross_sum(nl):
    if len(nl) < 3: return False
    a = [v for _, v, _, _ in nl]
    return any(2 * a[i] == sum(a) for i in range(len(a)))
def kal_cup(nl):
    ka = [v for f, v, u, l in nl if l in ('705', '706')]; cu = [v for f, v, u, l in nl if u == '700']
    return (bool(ka and cu), bool(ka and cu and set(ka) & set(cu)))
for name, fn in [('e1 cross-face repeat', cross_rep), ('e2 total across faces', cross_sum)]:
    for lab, df in [('objects', R), ('distinct records', R.drop_duplicates('text'))]:
        el = df[df.nums.str.len() >= (2 if name.startswith('e1') else 3)]
        obs = sum(fn(n) for n in el.nums)
        pool = [x for n in el.nums for x in n]; vals = [x[1] for x in pool]
        nul = []
        for _ in range(3000):
            pv = rng2.permutation(vals); k = 0; out = 0
            for n in el.nums:
                nn = [(f, pv[k + j], u, l) for j, (f, v, u, l) in enumerate(n)]; k += len(n); out += fn(nn)
            nul.append(out)
        nul = np.array(nul)
        print(f'{name} ({lab}): {obs} of {len(el)} against {nul.mean():.1f} shuffled, P {(nul >= obs).mean():.4f}')
kc = [kal_cup(n) for n in R.drop_duplicates('text').nums]
print(f'e3 distinct records with a kalam count and a cup count: {sum(a for a, b in kc)}; cup count = kalam count on {sum(b for a, b in kc)}')
print(R.drop_duplicates('text')[[kal_cup(n)[0] for n in R.drop_duplicates('text').nums]][['cisi', 'text', 'english']].to_string())
