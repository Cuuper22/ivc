#!/usr/bin/env python3
"""JOB 3, step 1: picture and slot of the 30 signs (printed BEFORE any word was chosen or any prediction tested).
Prints shape, gain (faces each sign alone keeps from reading whole under the wide list), slot shares, neighbours,
object kinds, sites, time bins, pictures on the object, counts beside it, and the second-catalogue drawing.
Writes work_data/sound_v7/j3_gains.csv and j3_profiles.txt."""
from sound_v7_common import *
V, S, W = load_values()
g, gd, gs = gains(W)
SIGNS = ['592', '703', '554', '064', '136', '603', '098', '408', '621', '243', '130', '697', '776', '804', '127', '167',
         '165', '645', '236', '048', '832', '460', '222', '821', '792', '350', '027', '201', '921', '232']
pd.DataFrame([dict(sign=s, faces_gained=g.get(s, 0), distinct=len(gd.get(s, ())), seals=gs.get(s, 0), shape=SH.get(s, '')) for s in SIGNS]).to_csv(f'{OUT7}/j3_gains.csv', index=False)
out = open(f'{OUT7}/j3_profiles.txt', 'w')
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.write(s + '\n')
for s in SIGNS:
    P(f'\n=== {s}  gain {g.get(s, 0)} faces ({len(gd.get(s, ()))} distinct, {gs.get(s, 0)} seals)  status {dict(zip(V.sign, V.status)).get(s, "none")}  shape: {SH.get(s, "")}')
    pr = profile(s, 'L'); P('  Lipi:', pr); P('  new texts:', profile(s, 'Mu'))
    o = objs[objs.signs.apply(lambda z: s in z)]
    P('  bins', dict(o.bin.value_counts()), ' pictures', dict(o.pic.value_counts().head(6)), ' animals', dict(o.animal.value_counts().head(5)))
    P('  counts beside: before', collections.Counter(counts_beside(s, 'LM', 'before')).most_common(5), ' after', collections.Counter(counts_beside(s, 'LM', 'after')).most_common(5))
    texts = collections.Counter('-'.join(x) for x in d.tok if s in x)
    P('  texts:', '; '.join(f'{t} x{n}' for t, n in texts.most_common(14)))
    if s in gd: P('  texts it alone blocks:', '; '.join('-'.join(x) for x in list(gd[s])[:10]))
out.close()
