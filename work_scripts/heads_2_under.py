#!/usr/bin/env python3
"""HEADS 2: what goes under each heading (names, amounts, third faces), and do different headings issue different THINGS or to
different PEOPLE?  Predictions written 2026-11-17 BEFORE these numbers (after seeing only the partner lists of heads_1):
  P1. 413-575 goes with the big measure: at least 60% of its tablets carry 705/706 somewhere (on the heading's partner face or
      beside it); 413-892 goes with names and NO amount (at most 20% of its tablets carry any amount).
  P2. Headings differ in WHAT they issue (amount kind: none / cups / big measure) more than in TO WHOM (partner ending):
      chi-square for amount kind has P < 0.05 against partners dealt at random among the heading tablets; for ending P is larger
      than that of amount kind.
  P3. Crest classes (fish, 176, number, other) do not differ between headings (P > 0.10).
  P4. A third face is rare under headings (at most 2 of 50 tablets).
Tests: the partner attribute (ending / amount kind / crest class) is dealt at random among the heading tablets, keeping each
heading's size; statistic = sum over headings of (observed - expected)^2 / expected; P = share of 20,000 deals at least as large.
Only tablets whose partner is a full name or has an amount enter the matching test.
Outputs: work_data/heads/h2_under.csv, h2_names.csv, h2_log.txt.   Run: python3 heads_2_under.py (seconds)
"""
from heads_common import *
say = log_to(f'{HOUT}/h2_log.txt')
rng = np.random.default_rng(2)
H = harappa_stones()
HO = pd.read_csv(f'{HOUT}/h1_objects.csv', dtype=str).fillna('')
HO = HO.drop_duplicates(['obj', 'family'])
fam_order = list(pd.read_csv(f'{HOUT}/h1_headings.csv', dtype=str).family)
FISH = {'220', '231', '233', '240', '226', '222', '243'}
def crest_class(c):
    if c == '': return 'none'
    if c in FISH: return 'fish'
    if c == '176': return 'seated person 176'
    if c in NUM: return 'number'
    return 'other'
rows = []
for _, h in HO.iterrows():
    r = H.loc[h.obj if h.obj in H.index else int(h.obj)] if (h.obj in H.index or int(h.obj) in H.index) else None
    faces = [face_str(f) for f in r.faces]
    hf = h.face
    partner_idx = [j for j in range(len(faces)) if faces[j] != hf]
    names = []; amts = collections.Counter(); amts_p = collections.Counter(); ending = []; third = 'third face' if len(faces) >= 3 else ''
    for j in range(len(faces)):
        a = amount_of(r.faces[j])
        for k, v in a.items(): amts[k] += 1
        if faces[j] != hf:
            for k, v in a.items(): amts_p[k] += 1
    for j in partner_idx:
        jp = r.jars[j]
        if jp is not None:
            nm = '-'.join(jp[0]); names.append(nm); ending.append(partner_role(r.faces[j], r.types[j], jp))
        elif r.types[j] == 'name':
            names.append(faces[j]); ending.append('name no jar')
    sig = r.sig
    rows.append(dict(family=h.family, obj=h.obj, cisi=r.cisi, trench=r.trench, mound=r.mound, bin=r.bin or 'undated', moulded=r.moulded, sig=sig,
                     name='; '.join(names), crest='; '.join(sorted({n.split('-')[0] for n in names if n})), ending='; '.join(ending) if ending else 'no name',
                     crest_class=crest_class(names[0].split('-')[0]) if names else 'none',
                     big=int('big' in amts), cup=int('cup' in amts), tree=int('tree' in amts), porter=int('porter' in amts),
                     any_amount=int(bool(amts)), big_p=int('big' in amts_p), cup_p=int('cup' in amts_p), tree_p=int('tree' in amts_p), third=int(len(faces) >= 3), nfaces=len(faces),
                     amount_text=' ; '.join(amount_text(f) for f in r.faces if amount_text(f))))
U = pd.DataFrame(rows)
U['amount_kind'] = ['big measure' if b else ('cups' if c else ('tree' if t else 'none')) for b, c, t in zip(U.big, U.cup, U.tree)]
U['amount_kind_p'] = ['big measure' if b else ('cups' if c else ('tree' if t else 'none')) for b, c, t in zip(U.big_p, U.cup_p, U.tree_p)]
U['ending1'] = [e.split('; ')[0] if e else 'no name' for e in U.ending]
U['ending1'] = U.ending1.replace({'jar + other': 'jar + other', 'other title': 'jar + other'})
U.to_csv(f'{HOUT}/h2_under.csv', index=False)
say(f'heading tablets {len(U)} (rows by family; a tablet is in one family)')
say('\nPER HEADING')
for fam in fam_order:
    g = U[U.family == fam]
    nn = [n for n in g.name if n]
    say(f'\n[{fam}] tablets {len(g)}; with a name partner {sum(1 for n in g.name if n)}; distinct names {len(set(nn))}; third face {int(g.third.sum())}; any amount {int(g.any_amount.sum())}')
    say(f'   endings: {fmt_counter(collections.Counter(g.ending1))}')
    say(f'   crest classes: {fmt_counter(collections.Counter(g.crest_class))}; crests: {fmt_counter(collections.Counter(c for x in g.crest for c in x.split("; ") if c))}')
    say(f'   amount kind: {fmt_counter(collections.Counter(g.amount_kind))}; big {int(g.big.sum())} cups {int(g.cup.sum())} tree {int(g.tree.sum())} porter {int(g.porter.sum())}')
    for _, r in g.iterrows(): say(f'      {r.cisi:8s} {r.trench:14s} {r.bin:8s} {r.moulded:8s} {r.sig}  [{r.amount_text}]')

# ---- tests: do headings differ?  office lines + side face together, and the three big ones
def chisq_codes(fc, vc):
    nf, nv = fc.max() + 1, vc.max() + 1
    T = np.zeros((nf, nv)); np.add.at(T, (fc, vc), 1)
    E = np.outer(T.sum(axis=1), T.sum(axis=0)) / T.sum()
    return float(((T - E) ** 2 / np.where(E == 0, 1, E)).sum())
def deal_test(df, col, n=20000):
    fc = pd.factorize(df.family)[0]; vc = pd.factorize(df[col])[0]
    obs = chisq_codes(fc, vc); nl = [chisq_codes(fc, rng.permutation(vc)) for _ in range(n)]
    return obs, float(np.mean(nl)), pvalue_hi(nl, obs)
say('\nDO HEADINGS DIFFER?  (partner attribute dealt at random among heading tablets; keeping heading sizes)')
S = U[U.family.isin(['413-575', '413-892', '817-368-690', '415-578'])]
for label, sub in (('four office lines', S), ('three largest office lines', S[S.family.isin(['413-575', '413-892', '817-368-690'])]),
                   ('all five incl. side face 415-220-520', U)):
    say(f'  {label}: {len(sub)} tablets')
    for col in ('amount_kind', 'amount_kind_p', 'ending1', 'crest_class'):
        o, m, p = deal_test(sub, col, 8000)
        say(f'    {col:12s} chi-square {o:6.2f}  chance mean {m:5.2f}  P {p:.4f}')
# big-measure and no-amount checks
for fam in ('413-575', '413-892'):
    g = U[U.family == fam]
    say(f'  {fam}: big measure on {int(g.big.sum())} of {len(g)} tablets (partner side {int(g.big_p.sum())}; cups on partner side {int(g.cup_p.sum())}); any amount {int(g.any_amount.sum())} of {len(g)}')
# baseline: big measure and comb share on Harappa 2-face tablets
T = H[H.nfaces >= 2]
nbig = np.mean([any(k == 'big' for f in r.faces for k in amount_of(f)) for _, r in T.iterrows()])
say(f'  baseline: big measure on {100 * nbig:.1f}% of Harappa 2+-face tablets')
nm = [(j[1] or 'jar') for js in T.jars for j in js if j is not None]
say(f'  baseline: Harappa 2+-face tablet jar names: comb {100 * nm.count("400") / len(nm):.1f}%, man {100 * nm.count("090") / len(nm):.1f}%, jar only {100 * nm.count("jar") / len(nm):.1f}% of {len(nm)}')
# third faces: heading tablets with 3 faces against the Harappa 3-face rate (exact binomial)
import math
T3 = H[(H.nfaces >= 2)]; p3 = float((T3.nfaces == 3).mean()); n3 = int(U.third.sum()); nn = len(U)
pb = sum(math.comb(nn, k) * p3 ** k * (1 - p3) ** (nn - k) for k in range(n3, nn + 1))
say(f'\nthird face: {n3} of {nn} heading tablets have 3 faces ({", ".join(f + " " + str(int(g.third.sum())) for f, g in U.groupby("family"))}); Harappa rate {100 * p3:.1f}% of 2+-face tablets; exact binomial P(>= {n3}) = {pb:.5f}')
g4 = U[U.family == '415-578']; k4 = int(g4.third.sum()); n4 = len(g4)
pb4 = sum(math.comb(n4, k) * p3 ** k * (1 - p3) ** (n4 - k) for k in range(k4, n4 + 1))
say(f'415-578 alone: {k4} of {n4} tablets have 3 faces (amount | heading | name); exact binomial P(>= {k4}) at the Harappa rate = {pb4:.5f}')
# how much of the record traffic carries a heading
rec_all = int(T3.shape[0]); say(f'heading tablets {nn} of {rec_all} Harappa tablets with 2+ faces ({100 * nn / rec_all:.1f}%); office-line headings (not the side face) {int(U[U.family != "415-220-520"].shape[0])} ({100 * U[U.family != "415-220-520"].shape[0] / rec_all:.1f}%)')
# single-face tablets starting 413 / 415-578 / 817-368-690 (a heading standing alone)
one = H[H.nfaces == 1]
for pre in ('413', '415-578', '817-368-690'):
    m = [r.cisi for _, r in one.iterrows() if '-'.join(r.faces[0]).startswith(pre)]
    say(f'single-face Harappa objects whose face starts {pre}: {len(m)} {m[:8]}')
# names pooled
N = []
for _, r in U.iterrows():
    for n in [x for x in r['name'].split('; ') if x]:
        N.append(dict(family=r.family, name=n, cisi=r.cisi, trench=r.trench, mound=r.mound, ending=r.ending1, amount=r.amount_text))
N = pd.DataFrame(N); N.to_csv(f'{HOUT}/h2_names.csv', index=False)
say(f'\nnames under headings: {len(N)} name faces, {N.name.nunique()} distinct names')
say('done')
