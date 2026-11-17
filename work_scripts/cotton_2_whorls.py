"""PART 2. Second whorl site. Candidate textile-tool objects in the Lipi catalogue, then does 390 (and look-alikes 405, 407) sit on them above chance?
Run: python3 cotton_2_whorls.py  (log -> cotton_out/whorl_log.txt; candidates -> cotton_out/whorl_candidates.csv)

PREDICTIONS, WRITTEN BEFORE THE RUN
 Candidate sets (a spindle whorl = a small clay or stone disc/cone weighting a hand spindle; a loom weight = a bigger clay lump/cone/disc; "other textile tool" = needle, spool etc):
   W_strict: Karanpura-style, clay/terracotta/stone objects typed MISC (the catalogue's bin for non-seal clay and stone odds and ends) -- no seal shape, no tablet shape.
   W_shape: any object whose recorded shape is conical, spherical, circular or amorph and that is NOT a seal/tablet/tag (IMPL, MISC, BEAD, MDLN).
   W_pot: none.
 If 390 is the cotton/weaving sign: on W_strict outside Karanpura, 390 (alone or first) should sit well above its 3-5% base rate: predict >= 15% of objects, i.e. >= 3x.
 405/407 (look-alike trees): if they are fibre/cloth words they should show on the same objects at lower rate; if they are copper-tablet goods (407 is 63 of 127 on copper tablets) they should be ~0 here.
 Control: 390 on bead/ivory/copper implement objects should NOT be enriched (copper tools are another craft).
"""
from cotton_common import *
f = open(f'{OUTC}/whorl_log.txt', 'w')
d = faces()
IMG = f'{ROOT}/evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/public/seal_images'
imgs = set(os.listdir(IMG))
def photos(c):
    if c in ('-', ''): return 0
    return sum(1 for x in imgs if x.startswith(c + '_') or x.startswith(c + '-bis'))
nonmetal = ~d.mat.isin(['copper', 'gold', 'silver', 'metal'])
miscs = d[(d.type == 'MISC') & nonmetal]
W_strict = miscs
W_shape = d[d['shape'].isin(['conical', 'spherical', 'circular', 'amorph']) & d.type.isin(['IMPL', 'MISC', 'BEAD', 'MDLN']) & nonmetal]
log(f, f'W_strict: non-metal MISC faces {len(W_strict)}, objects {W_strict.obj.nunique()}; sites {dict(W_strict.site.value_counts())}')
log(f, f'W_shape: {len(W_shape)} faces')
def hits(sub, sign):
    return int(sub.toks.apply(lambda t: sign in t).sum())
def alone(sub, sign): return int(sub.toks.apply(lambda t: t == [sign]).sum())
base = {s: np.mean([s in t for t in d.toks]) for s in ['390', '405', '407']}
log(f, f'base share of faces carrying: {base}')
rows = []
for name, sub in [('MISC non-metal, all', W_strict), ('MISC non-metal, not Karanpura', W_strict[W_strict.site != 'Karanpura']),
                  ('MISC non-metal, not Karanpura, not 000-only', W_strict[(W_strict.site != 'Karanpura') & W_strict.toks.apply(lambda t: any(x not in ('000',) for x in t))]),
                  ('Karanpura MISC', W_strict[W_strict.site == 'Karanpura'])]:
    n = len(sub)
    for s in ['390', '405', '407']:
        a = hits(sub, s); rest = d[~d.index.isin(sub.index)]
        r, p = fe(a, n - a, hits(rest, s), len(rest) - hits(rest, s))
        rows.append(dict(set=name, n=n, sign=s, with_sign=a, alone=alone(sub, s), ratio=round(r, 2), P=p))
        log(f, f'{name}: n {n}, {s} on {a} (alone {alone(sub, s)}): {r:.2f}x chance, P {p:.2g}')
# Karanpura-excluded with the '390 alone' dissected by site
nk = W_strict[W_strict.site != 'Karanpura']
for _, r_ in nk[nk.toks.apply(lambda t: any(s in t for s in ['390', '405', '407']))].iterrows():
    log(f, f'   MISC with tree sign: id {r_.id} cisi {r_.cisi} {r_.site} {r_.material} shape {r_["shape"]} text {"-".join(r_.toks)} photos {photos(r_.cisi)}')
pd.DataFrame(rows).to_csv(f'{OUTC}/whorl_tests.csv', index=False)
# shape set
for s in ['390', '405', '407']:
    sub = W_shape[W_shape.site != 'Karanpura']; a = hits(sub, s); rest = d[~d.index.isin(sub.index)]
    r, p = fe(a, len(sub) - a, hits(rest, s), len(rest) - hits(rest, s))
    log(f, f'W_shape not Karanpura: n {len(sub)}, {s} on {a}: {r:.2f}x, P {p:.2g}')
# Kalibangan/Harappa/other-sites clay-and-stone MISC: same test per site
for st in sorted(set(nk.site)):
    sub = nk[nk.site == st]; log(f, f'   site {st}: MISC non-metal {len(sub)}; with 390 {hits(sub,"390")}, 405 {hits(sub,"405")}, 407 {hits(sub,"407")}')
# Control: 390 on copper implements
cu = d[d.type.isin(['IMPL']) & d.mat.eq('copper')]
log(f, f'control: copper implements {len(cu)} faces, 390 on {hits(cu,"390")}, 405 on {hits(cu,"405")}, 407 on {hits(cu,"407")}')
cand = pd.concat([W_strict, W_shape]).drop_duplicates('id')
cand = cand.assign(photos=cand.cisi.apply(photos), has390=cand.toks.apply(lambda t: '390' in t), text_r=cand.toks.apply(lambda t: '-'.join(t)))
cand[['id', 'cisi', 'site', 'area-section', 'material', 'shape', 'type', 'horizontal(mm)', 'vertical(mm)', 'thickness(mm)', 'symbol', 'text_r', 'photos', 'has390']].to_csv(f'{OUTC}/whorl_candidates.csv', index=False)
log(f, f'candidates written: {len(cand)}; with photos {int((cand.photos>0).sum())}')
f.close()
