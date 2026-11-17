"""PART 2 rescue. The MISC bin gave 390 on 2 of 71 outside Karanpura (against the >=3x predicted).
Rescue 1 (better test): the tool may be catalogued as something other than MISC. Look at material instead: terracotta (the fired-clay craft) vs all, outside Karanpura; and every whole-text '390' / '405' / '407' object.
Prediction: if 390 marks the weavers' trade, terracotta objects (cheap fired copies and craft pieces) carry it above 2x chance outside Karanpura; 390-alone objects sit on non-seal objects.
Rescue 2 (new idea): the textile-linked signs may sit on terracotta SEALS and tags of weaving towns (Kalibangan, Nausharo, Nuhato): test 390/405/407 on terracotta seals vs steatite seals.
"""
from cotton_common import *
f = open(f'{OUTC}/whorl_log2.txt', 'w')
d = faces()
terr = d.mat.isin(['terracotta']) & (d.site != 'Karanpura')
for s in ['390', '405', '407']:
    h = d.toks.apply(lambda t: s in t)
    a = int((terr & h).sum()); n = int(terr.sum()); c = int((~terr & h).sum()); m = int((~terr).sum())
    r, p = fe(a, n - a, c, m - c)
    log(f, f'terracotta (not Karanpura) n {n}: {s} on {a} ({a/n:.3f}) vs {c/m:.3f} elsewhere: {r:.2f}x, P {p:.3g}')
clay = d.mat.isin(['terracotta', 'clay', 'ceramic']) & (d.site != 'Karanpura')
for s in ['390']:
    h = d.toks.apply(lambda t: s in t)
    a = int((clay & h).sum()); n = int(clay.sum()); c = int((~clay & h).sum()); m = int((~clay).sum())
    r, p = fe(a, n - a, c, m - c); log(f, f'all fired/unfired clay (not Karanpura) n {n}: {s} on {a}: {r:.2f}x P {p:.3g}')
# terracotta seals vs steatite seals
seal = d.cls == 'seal'
for s in ['390', '405', '407']:
    h = d.toks.apply(lambda t: s in t)
    ts = seal & d.mat.eq('terracotta'); ss = seal & d.mat.str.startswith('steatite')
    log(f, f'seals: terracotta {int((ts&h).sum())}/{int(ts.sum())} vs steatite {int((ss&h).sum())}/{int(ss.sum())} carry {s}: ' + str(fe(int((ts&h).sum()), int(ts.sum() - (ts&h).sum()), int((ss&h).sum()), int(ss.sum() - (ss&h).sum()))))
# by site: terracotta carrying 390
tt = d[(d.mat == 'terracotta') & d.toks.apply(lambda t: '390' in t)]
log(f, 'terracotta faces with 390: ' + '; '.join(f'{r.cisi if r.cisi!="-" else r.id}|{r.site}|{r.type}|{"-".join(r.toks)}' for _, r in tt.iterrows()))
# whole-text 390 / 405 / 407 objects
for s in ['390', '405', '407']:
    w = d[d.toks.apply(lambda t: t == [s])]
    log(f, f'whole-text {s}: {len(w)} faces; by site {dict(w.site.value_counts())}; by type {dict(w.type.value_counts())}; materials {dict(w.mat.value_counts())}')
    if s == '390':
        for _, r in w.iterrows(): log(f, f'    id {r.id} {r.site} {r.type} {r.material} {r["shape"]} {r["area-section"]}')
# who else is single-sign on Karanpura-like classes: whole-text 390 share of single-sign non-seal misc/other
f.close()
