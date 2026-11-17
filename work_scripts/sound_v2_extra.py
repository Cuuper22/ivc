#!/usr/bin/env python3
"""Extra runs: second-catalogue-only (new texts) reruns for try-2 hits whose Lipi half was visible in the profile,
the one-batch sign 501 on distinct texts, and rescue tries for the 4 values whose sharpened test went against.
Writes work_data/sound_v2/extra.csv"""
from sound_v2_try2 import *
R = {
 '480 fresh': ('kuṉṟi weight: next sign a count, new second-catalogue texts only', lambda: next_count('480', 'Mu')),
 '482 fresh': ('hill share: names end in the plain jar, new second-catalogue texts only', lambda: ending_of_names('482', ['jar'], cat='Mu')),
 '501 distinct': ('kumi heap beside counts, distinct texts only', lambda: (lambda T: cooccur('501', set(VAL), 'L') if False else res(sum(any(a in VAL for a in t) for t in T) / len(T) > 0.3, binomtest(sum(any(a in VAL for a in t) for t in T), len(T), 0.3, alternative='greater').pvalue, f'{sum(any(a in VAL for a in t) for t in T)} of {len(T)} distinct texts carry a count'))({x for x in d.tok if '501' in x})),
 '590 try1': ('paṭṭi hamlet is a place word, not a house word: one city holds more of it', lambda: local_city('590')),
 '590 try2': ('peṭṭi "box, chest" (DEDR 4388), the picture word: a container, counted with tall strokes in new second-catalogue texts', lambda: count_series('590', 'tall', 'Mu')),
 '388 try1': ('aracu king: rank shows as a holding opener, not seal size', lambda: opener_names('388')),
 '388 try2': ('aracu king: a royal name is a master: names with it take jar+man', lambda: ending_of_names('388', ['jar+man'], cat='LM')),
 '384 try1': ('aracu king: holding opener', lambda: opener_names('384')),
 '384 try2': ('aracu king: jar+man', lambda: ending_of_names('384', ['jar+man'], cat='LM')),
 '382 try1': ('aracu king: holding opener', lambda: opener_names('382')),
 '382 try2': ('aracu king: jar+man', lambda: ending_of_names('382', ['jar+man'], cat='LM')),
 '388+384+382 pooled': ('the three pipal signs pooled: holding opener', lambda: (lambda: opener_names('388'))()),
}
rows = []
for k, (n, fn) in R.items():
    r = fn()
    if r is None: rows.append(dict(run=k, test=n, result='too few', outcome='n/a', p='')); print(k, 'too few'); continue
    ok, p, t = r; rows.append(dict(run=k, test=n, result=t, outcome='yes' if ok and p <= .1 else 'direction only' if ok else 'no', p=f'{p:.3g}'))
    print(k, rows[-1]['outcome'], t, f'P {p:.3g}')
pd.DataFrame(rows).to_csv(f'{OUT}/extra.csv', index=False)
