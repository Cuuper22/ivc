#!/usr/bin/env python3
"""HEADS 5: trench by trench.  Predictions written 2026-11-17 BEFORE these numbers:
  P1. No trench is all one heading: in each of the 8 trenches with most tablets the headings that occur are at least two kinds
      or the heading tablets are under 10% of its tablets; and the largest single-trench share of each heading is not above
      what a random draw of the heading's tablets from the city's two-face tablets gives (P > 0.05 for every heading).
  P2. Mound F trenches and Mound E trenches differ: Mound E holds the hands/loads/cups gang tablets (003-156 | 003-861 | 034-700,
      ETrench 11) and more incised tablets; Mound F holds the comb chits (176-740-400 in FTrench I) and more of the
      moulded 413-575 heading.  Comb share of jar names higher in F than in E (trench-label deal P < 0.10).
  P3. The headings' time bins: all headings are in the middle bin (3B/C to 3C-2) or earlier; none is later than the middle bin
      except 413-575 which has 2 late tablets.
Tests: (a) per heading, the largest trench share against 20,000 random draws of the same number of two-face tablets with a known
trench; (b) E against F: the trench labels (E-mound / F-mound) are dealt at random among the trenches with 15+ tablets, 20,000
times, and the pooled tablet-level rate in the F group minus the E group is compared.  Copy events are not collapsed here (tablet
counts), because the question is what each trench holds, not how many separate texts.
Outputs: work_data/heads/h5_trenches.csv, h5_EF.csv, h5_log.txt.   Run: python3 heads_5_trenches.py (seconds)
"""
from heads_common import *
say = log_to(f'{HOUT}/h5_log.txt')
rng = np.random.default_rng(5)
H = harappa_stones()
HO = pd.read_csv(f'{HOUT}/h1_objects.csv', dtype=str).fillna('')
fam_of = {}
for _, r in HO.iterrows(): fam_of[str(r.obj)] = r.family
H['heading'] = [fam_of.get(str(o), '') for o in H.obj]
T = H[H.kind == 'mtab'].copy()
Tk = T[T.trench != '(none)']
say(f'Harappa clay tablets {len(T)}; with a trench {len(Tk)}; trenches {Tk.trench.nunique()}')
top = Tk.trench.value_counts().head(8).index.tolist()
say('top 8 trenches by tablets: ' + ', '.join(f'{t} {int((Tk.trench == t).sum())}' for t in top))
# per-tablet features
def feat(r):
    cups = None; big = False
    for f in r.faces:
        a = amount_of(f)
        if 'cup' in a and a['cup'] is not None: cups = a['cup']
        if 'big' in a: big = True
    ends = [(j[1] or 'jar') for j in r.jars if j is not None]
    types = r.types
    rec = ('amount' in types) and (('name' in types) or any(j is not None for j in r.jars))
    gang = r.sig == '003-156 | 003-861 | 034-700'
    return pd.Series(dict(cups=cups, big=big, comb=('400' in ends), man=('090' in ends), jaronly=('jar' in ends), anyjar=bool(ends), rec=rec, gang=gang,
                          c176=any(j is not None and j[0] and j[0][-1] == '176' and (j[1] == '400') for j in r.jars)))
F_ = T.apply(feat, axis=1); T = pd.concat([T, F_], axis=1)
T['cups'] = pd.to_numeric(T.cups, errors='coerce')
rows = []
for t in top + ['__all__']:
    g = T if t == '__all__' else T[T.trench == t]
    nm = []
    for _, r in g.iterrows():
        for f, j in zip(r.faces, r.jars):
            if j is not None: nm.append('-'.join(j[0]))
    hc = collections.Counter(x for x in g.heading if x)
    rows.append(dict(trench=t if t != '__all__' else 'all Harappa tablets', mound=mound(t) if t != '__all__' else '', tablets=len(g), two_face=int((g.nfaces >= 2).sum()),
                     heading_tablets=int((g.heading != '').sum()), headings='; '.join(f'{k} {v}' for k, v in hc.most_common()),
                     distinct_names=len(set(nm)), jar_name_faces=len(nm), comb=int(g.comb.sum()), man=int(g.man.sum()), jar_only=int((g.jaronly & ~g.comb & ~g.man).sum()),
                     with_cups=int(g.cups.notna().sum()), mean_cups=round(g.cups.mean(), 2), big_measure=int(g.big.sum()),
                     amount_name_records=int(g.rec.sum()), gang_tablets=int(g.gang.sum()), name_176_comb=int(g.c176.sum()),
                     moulded=int((g.moulded == 'moulded').sum()), incised=int((g.moulded == 'incised').sum()),
                     early=int((g.bin == 'early').sum()), middle=int((g.bin == 'middle').sum()), late=int((g.bin == 'late').sum()), undated=int((g.bin == '').sum())))
R = pd.DataFrame(rows); R.to_csv(f'{HOUT}/h5_trenches.csv', index=False)
say('\nTRENCH TABLE')
for _, r in R.iterrows():
    say(f'  {r.trench:22s} mound {r.mound or "-":3s} tablets {r.tablets:4d} 2-face {r.two_face:4d} heading {r.heading_tablets:3d} [{r.headings}] names {r.distinct_names}/{r.jar_name_faces} comb {r.comb} man {r.man} jar-only {r.jar_only} | cups {r.with_cups} mean {r.mean_cups} big {r.big_measure} records {r.amount_name_records} gang {r.gang_tablets} 176comb {r.name_176_comb} | moulded {r.moulded} incised {r.incised} | bins e/m/l/undated {r.early}/{r.middle}/{r.late}/{r.undated}')

# (a) single-heading concentration per heading
say('\n(a) is any heading concentrated in one trench?  largest single-trench count against random draws of the same number of two-face tablets with a trench')
pool = Tk[Tk.nfaces >= 2].trench.values
for fam, g in H[H.heading != ''].groupby('heading'):
    gk = g[g.trench != '(none)']; n = len(gk)
    if n == 0: continue
    top1 = gk.trench.value_counts().iloc[0]; nm = gk.trench.value_counts().index[0]
    nl = np.array([pd.Series(rng.choice(pool, size=n)).value_counts().iloc[0] for _ in range(20000)])
    nd = np.array([len(set(rng.choice(pool, size=n))) for _ in range(20000)])
    say(f'  {fam:12s} tablets with a trench {n}: most in one trench = {top1} ({nm}); chance {nl.mean():.2f}; P(>=) {pvalue_hi(nl, top1):.4f}; trenches used {gk.trench.nunique()} against {nd.mean():.1f} (P fewer {pvalue_lo(nd, gk.trench.nunique()):.3f})')
# headings per trench
say('\nheadings per trench (all trenches with 1+ heading tablet):')
hh = H[(H.heading != '') & (H.trench != '(none)')].groupby('trench').heading.agg(lambda s: '; '.join(f'{k} {v}' for k, v in collections.Counter(s).most_common()))
for t, v in hh.items():
    say(f'  {t:16s} tablets {int((Tk.trench == t).sum()):4d}  {v}')
nonum = H[(H.heading != '')].trench.eq('(none)').sum()
say(f'  heading tablets with no trench recorded: {nonum} of {int((H.heading != "").sum())}')

# (b) E against F
say('\n(b) MOUND E AGAINST MOUND F  (trenches with 15+ clay tablets)')
cnt = Tk.groupby('trench').size(); big_t = [t for t in cnt.index if cnt[t] >= 15]
grp = {t: mound(t) for t in big_t}
EF = [t for t in big_t if grp[t] in ('E', 'F')]
say('  trenches: ' + ', '.join(f'{t} ({grp[t]}, {cnt[t]})' for t in EF))
TT = T[T.trench.isin(EF)].copy()
def rate(col, mask=None, num=None):
    pass
measures = {
    'comb share of jar-name tablets': (lambda g: g.comb.sum(), lambda g: g.anyjar.sum()),
    'moulded share': (lambda g: (g.moulded == 'moulded').sum(), lambda g: (g.moulded != '').sum()),
    'big measure on tablets with an amount': (lambda g: g.big.sum(), lambda g: (g.big | g.cups.notna()).sum()),
    'amount + name records share': (lambda g: g.rec.sum(), lambda g: (g.nfaces >= 2).sum()),
    'gang tablets (003-156 | 003-861 | 034-700) per 100 tablets': (lambda g: g.gang.sum() * 100, lambda g: len(g)),
    'heading tablets per 100 tablets': (lambda g: (g.heading != '').sum() * 100, lambda g: len(g)),
    'early-bin share of dated': (lambda g: (g.bin == 'early').sum(), lambda g: (g.bin != '').sum()),
    'late-bin share of dated': (lambda g: (g.bin == 'late').sum(), lambda g: (g.bin != '').sum()),
}
by_t = {t: TT[TT.trench == t] for t in EF}
nums = {k: np.array([f[0](by_t[t]) for t in EF], float) for k, f in measures.items()}
dens = {k: np.array([f[1](by_t[t]) for t in EF], float) for k, f in measures.items()}
isF = np.array([grp[t] == 'F' for t in EF])
out = []
for k in measures:
    def diff(mask):
        a = nums[k][mask].sum() / max(dens[k][mask].sum(), 1); b = nums[k][~mask].sum() / max(dens[k][~mask].sum(), 1); return a - b
    obs = diff(isF); nl = []
    for _ in range(20000):
        nl.append(diff(rng.permutation(isF)))
    nl = np.array(nl)
    f_ = nums[k][isF].sum() / max(dens[k][isF].sum(), 1); e_ = nums[k][~isF].sum() / max(dens[k][~isF].sum(), 1)
    out.append(dict(measure=k, F=round(f_, 3), E=round(e_, 3), diff=round(obs, 3), P_two_sided=round(float((1 + (np.abs(nl) >= abs(obs)).sum()) / (len(nl) + 1)), 4),
                    denomF=int(dens[k][isF].sum()), denomE=int(dens[k][~isF].sum())))
    say(f'  {k:60s} F {f_:.3f} (of {int(dens[k][isF].sum())})  E {e_:.3f} (of {int(dens[k][~isF].sum())})  diff {obs:+.3f}  P(two-sided, trench labels dealt) {out[-1]["P_two_sided"]}')
pd.DataFrame(out).to_csv(f'{HOUT}/h5_EF.csv', index=False)
import math
say(f'  ways to label {len(EF)} trenches with {int(isF.sum())} F: {math.comb(len(EF), int(isF.sum()))}, so the smallest possible two-sided P is about {2 / math.comb(len(EF), int(isF.sum())):.3f}')
say('done')
