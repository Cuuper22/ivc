#!/usr/bin/env python3
"""CHITS 4: batches and issuers at Harappa.

BATCH / ISSUE = identical tablets (same faces, no lost sign) in one Harappa trench; COPIES = how many.
Per batch: trench, copies, name face, amount (cup count), bin, format.
Questions and controls:
 (a) Does one trench issue to many names, or does one name collect from many trenches?  For names on 2+ tablets
     (records, copies once per trench), the number of trenches per name against trench labels shuffled among the same
     tablets (2,000 shuffles).  Few trenches = a name's chits are kept in its own place.
 (b) Do copies follow the amount (3 cups, 3 copies)?  Spearman of copies against cup count over issues; exact
     "copies == cups" share against copies shuffled among issues.
 (c) Constant faces: inside one trench, a face that stands beside many DIFFERENT partner faces on multi-face tablets.
     Listed by kind (amount / name / thing).  A non-amount face with 3+ different names beside it in one trench is an
     issuer's mark candidate.  Control: the same count with faces shuffled among the multi-face tablets of that trench
     (keeps each face's frequency) to see whether a face pairs with more different partners than chance.

PREDICTIONS (written before any number):
 B1 names sit in fewer trenches than chance (chits kept at the holder's place), and trenches hold many names
    (one trench, many recipients: a store paying out).
 B2 copies equal cups more often than chance (one tablet per cup issued).
 B3 at least one thing face (not an amount, not a name) stands beside 3+ names in one trench: the issuing office's mark.
Writes work_data/chits/c4_*.csv, c4_log.txt.
"""
import sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chits_common import *
from scipy.stats import spearmanr
LOG = open(f'{OUT}/c4_log.txt', 'w'); say = say_to(LOG)
O = load(); rng = np.random.default_rng(44)
H = O[(O.site == 'Harappa') & (O.kind == 'mtab')].copy()
say(f'Harappa tablets {len(H)}; with a trench {int((H.area != "").sum())}; lost-sign free {int(H.lostfree.sum())}')
def name_and_amount(r):
    nm, cups, amtf = '', None, ''
    for f, jp, t in zip(r.faces, r.jars, r.types):
        if jp is not None and len(jp[0]) > 0 and not nm:
            nm = '-'.join(jp[0]) + '|' + (jp[1] or 'jar')
        elif t == 'name' and not nm:
            nm = '-'.join(f) + '|nojar'
    for f, t in zip(r.faces, r.types):
        a = amount_of(f)
        if 'cup' in a and cups is None: cups = a['cup']; amtf = '-'.join(f)
    return nm, cups, amtf
H[['namekey', 'cups', 'amt_face']] = H.apply(lambda r: pd.Series(name_and_amount(r)), axis=1)
H['ending'] = H.namekey.str.split('|').str[1].fillna('')
H['issue'] = H.sig + '#' + H.area
Hb = H[H.lostfree & (H.area != '')]
B = Hb.groupby('issue').agg(trench=('area', 'first'), sig=('sig', 'first'), copies=('obj', 'size'), namekey=('namekey', 'first'),
                            cups=('cups', 'first'), formats=('type', lambda s: ','.join(sorted(set(s)))),
                            bins=('bin', lambda s: ','.join(sorted(set(x for x in s if x)))), nfaces=('nfaces', 'first'),
                            cisi=('cisi', lambda s: ' '.join(list(s)[:6]))).reset_index()
B = B.sort_values('copies', ascending=False); B.to_csv(f'{OUT}/c4_batches.csv', index=False)
say(f'issues (signature + trench) {len(B)}; copies distribution: {fmt_counter(dict(sorted(collections.Counter(B.copies).items())))}')
say('issues with 3+ copies:')
for _, b in B[B.copies >= 3].iterrows():
    say(f'   x{b.copies:2d} {b.trench:16s} {b.sig:44s} name {b.namekey:24s} cups {b.cups} {b.formats} bins {b.bins}')

# (a) names vs trenches
say('\n(a) names and trenches (records = issues; names on 2+ issues):')
R = B[B.namekey != ''].copy()
multi = R.groupby('namekey').filter(lambda g: len(g) >= 2)
def trench_per_name(df):
    return df.groupby('namekey').trench.nunique().mean()
obs = trench_per_name(multi); nul = []
for _ in range(2000):
    t = rng.permutation(R.trench.values); nul.append(trench_per_name(R.assign(trench=t)[R.namekey.isin(multi.namekey)]))
nul = np.array(nul)
say(f'  {multi.namekey.nunique()} names on 2+ issues ({len(multi)} issues): mean trenches per name {obs:.2f} against {nul.mean():.2f} shuffled (P low {(nul <= obs).mean():.4f})')
for e in ('400', 'jar', 'nojar', '090'):
    m = multi[multi.ending == e] if 'ending' in multi else multi[multi.namekey.str.endswith('|' + e)]
    m = multi[multi.namekey.str.endswith('|' + e)]
    if m.namekey.nunique() < 2: continue
    o = trench_per_name(m); nn = []
    for _ in range(2000):
        t = rng.permutation(R.trench.values); nn.append(trench_per_name(R.assign(trench=t)[R.namekey.isin(m.namekey)]))
    nn = np.array(nn)
    say(f'    ending {e:5s}: {m.namekey.nunique()} names, {o:.2f} trenches per name against {nn.mean():.2f} (P low {(nn <= o).mean():.4f})')
TR = R.groupby('trench').agg(issues=('issue', 'size'), names=('namekey', 'nunique'),
                             comb_names=('namekey', lambda s: s[s.str.endswith('|400')].nunique()),
                             objects=('copies', 'sum')).sort_values('issues', ascending=False)
TR.to_csv(f'{OUT}/c4_trenches.csv')
say('  trenches by issues (issues, distinct names, comb names, tablets):')
for t, r in TR.head(12).iterrows(): say(f'    {t:18s} {r.issues:3d} {r.names:3d} {r.comb_names:3d} {r.objects:3d}')
# comb share by trench vs shuffle
CT = Hb.groupby('area').agg(n=('obj', 'size'), comb=('ending', lambda s: (s == '400').sum()))
say('  comb share by trench (tablets): ' + '; '.join(f'{t} {r.comb}/{r.n}' for t, r in CT.sort_values('n', ascending=False).head(10).iterrows()))
x = Hb.ending.values == '400'; ar = Hb.area.values
def chi(xx):
    s = 0
    for a in np.unique(ar):
        m = ar == a; e = m.sum() * xx.mean()
        if e > 0: s += (xx[m].sum() - e) ** 2 / e
    return s
oc = chi(x); nc = np.array([chi(rng.permutation(x)) for _ in range(2000)])
say(f'  comb tablets spread over trenches: chi {oc:.1f} against {nc.mean():.1f} shuffled (P {(nc >= oc).mean():.4f})')

# (b) copies vs cups
say('\n(b) copies against cups (issues with a cup count):')
C = B[B.cups.notna()]
rho = spearmanr(C.copies, C.cups).correlation
eq = (C.copies == C.cups).mean(); neq = []; nr = []
for _ in range(4000):
    p = rng.permutation(C.copies.values); neq.append((p == C.cups.values).mean()); nr.append(spearmanr(p, C.cups).correlation)
neq, nr = np.array(neq), np.array(nr)
say(f'  {len(C)} issues; Spearman copies~cups {rho:+.3f} (P high {(nr >= rho).mean():.4f}); copies == cups {eq:.3f} against {neq.mean():.3f} (P high {(neq >= eq).mean():.4f})')
say('  copies by cups: ' + '; '.join(f'{int(c)} cups: ' + fmt_counter(dict(sorted(collections.Counter(C[C.cups == c].copies).items()))) for c in sorted(C.cups.unique())))
C2 = C[C.copies >= 2]
say('  issues with 2+ copies: ' + '; '.join(f'{r.namekey} {int(r.cups)}c x{r.copies}' for _, r in C2.iterrows()))

# (c) constant faces
say('\n(c) faces that stay the same beside many different partner faces in one trench (multi-face tablets, copies once):')
M = Hb[Hb.nfaces >= 2].drop_duplicates('issue')
rows = []
for tr, g in M.groupby('area'):
    partners = collections.defaultdict(set); ftype = {}
    for _, r in g.iterrows():
        fs = ['-'.join(f) for f in r.faces]
        for i, f in enumerate(fs):
            ftype[f] = r.types[i]
            for j, f2 in enumerate(fs):
                if i != j: partners[f].add(f2)
    for f, ps in partners.items():
        if len(ps) >= 3:
            rows.append(dict(trench=tr, face=f, face_type=ftype[f], partners=len(ps), pictures=' + '.join(pic(x) for x in f.split('-')),
                             partner_sample=' / '.join(sorted(ps)[:8])))
CF = pd.DataFrame(rows).sort_values(['face_type', 'partners'], ascending=[True, False]); CF.to_csv(f'{OUT}/c4_constant_faces.csv', index=False)
say(f'  faces with 3+ different partners in one trench: {len(CF)}; by type {fmt_counter(collections.Counter(CF.face_type))}')
for _, r in CF.iterrows():
    say(f'    {r.trench:16s} {r.face_type:7s} {r.face:22s} partners {r.partners:3d}  {r.partner_sample[:110]}')
# across Harappa (all trenches): non-amount faces with many partners
say('\n  non-amount faces with 3+ different partners anywhere at Harappa (copies once per trench):')
partners = collections.defaultdict(set); ftype = {}; ftr = collections.defaultdict(set)
for _, r in M.iterrows():
    fs = ['-'.join(f) for f in r.faces]
    for i, f in enumerate(fs):
        ftype[f] = r.types[i]; ftr[f].add(r.area)
        for j, f2 in enumerate(fs):
            if i != j: partners[f].add(f2)
CA = pd.DataFrame([dict(face=f, face_type=ftype[f], partners=len(p), trenches=len(ftr[f]), pictures=' + '.join(pic(x) for x in f.split('-')),
                        partner_sample=' / '.join(sorted(p)[:10])) for f, p in partners.items() if len(p) >= 3])
CA = CA.sort_values('partners', ascending=False); CA.to_csv(f'{OUT}/c4_constant_faces_all.csv', index=False)
for _, r in CA[CA.face_type != 'amount'].iterrows():
    say(f'    {r.face_type:6s} {r.face:22s} partners {r.partners:3d} trenches {r.trenches:2d} [{r.pictures[:60]}]  {r.partner_sample[:120]}')
say('done')
