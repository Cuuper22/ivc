#!/usr/bin/env python3
"""HEADS 3: the parts of a heading, and where else they occur.  Predictions written 2026-11-17 BEFORE these numbers:
  P1. 413 (the sign that starts both big headings) is a tablet sign: at least 80% of its uses are on clay tablets (the share of
      all faces on tablets is about 24%), and its neighbours 575, 335, 711, 892, 824 are likewise tablet signs (>= 60% each).
  P2. The varying part is the 'kind of issue': the tail after 413 (575-335-711 against 892-824) separates the two headings
      completely (the two tails never occur in the same face), while 413 alone is shared.
  P3. Heading signs are rare on seals: no more than 15% of the uses of 413, 575, 335, 711, 892, 824 are on seals; and at most 2
      of the heading signs are seal lead signs (front word or crest) beyond the 95th percentile of frequency-matched control signs.
  P4. 415-220-520 (the side face) is a seal name: its pitchfork-fish crest (415-220) is on seals at Harappa AND Mohenjo-daro, so this
      heading-like face ties the issuing side to a seal-holding house.  Test: 415-220 as lead on seals against matched signs.
Tie test: for sign s, S(s) = number of seal faces whose LEAD sign (first sign after taking off front word and slot) is s, or whose
front word is s.  Control: the same count for signs whose total number of uses across all faces lies within a factor 1.4 of s's
and that are not heading signs (all such signs); P = share of control signs with S >= S(s).  'Seal' = catalogue kind seal (all
cities), counted once per stone (same text on the same stone not repeated).
Outputs: work_data/heads/h3_signs.csv, h3_ties.csv, h3_pieces.csv, h3_log.txt.  Run: python3 heads_3_parts.py (seconds)
"""
from heads_common import *
say = log_to(f'{HOUT}/h3_log.txt')
with contextlib.redirect_stdout(io.StringIO()):
    O = load()
HEAD = pd.read_csv(f'{HOUT}/h1_headings.csv', dtype=str)
say('heading families:', ', '.join(HEAD.family))
PARTS = ['413', '575', '335', '711', '892', '824', '415', '578', '817', '368', '690', '220', '520', '032']
# ---- flatten all faces
F = []
for o, r in O.iterrows():
    for k, f in enumerate(r.faces):
        F.append((o, r.site, r.kind, r.type, k, tuple(f)))
F = pd.DataFrame(F, columns=['obj', 'site', 'kind', 'type', 'k', 'f'])
say(f'faces {len(F)} on {O.shape[0]} objects')
use = collections.Counter(s for f in F.f for s in f)
KINDS = ['seal', 'mtab', 'ctab', 'tag', 'pot', 'rod', 'other']
rows = []
for s in PARTS:
    m = F[[s in f for f in F.f]]
    kc = collections.Counter(m.kind); sc = collections.Counter(m.site)
    ntab = kc['mtab']; n = len(m)
    first = sum(f[0] == s for f in m.f)
    rows.append(dict(sign=s, picture=pic(s), v2=V2.get(s, 'PERSONAL'), faces=n, uses=use[s], tablets=ntab, tablet_share=round(ntab / max(n, 1), 3),
                     seals=kc['seal'], seal_share=round(kc['seal'] / max(n, 1), 3), copper=kc['ctab'], tags=kc['tag'], pots=kc['pot'], rods=kc['rod'],
                     harappa=sc['Harappa'], mohenjo=sc['Mohenjo-daro'], other_cities=n - sc['Harappa'] - sc['Mohenjo-daro'], first_sign=first))
SG = pd.DataFrame(rows); SG.to_csv(f'{HOUT}/h3_signs.csv', index=False)
say('\nTHE SIGNS OF THE HEADINGS (faces carrying the sign; all cities; base: tablets are %.1f%% of all faces, seals %.1f%%)' % (
    100 * (F.kind == 'mtab').mean(), 100 * (F.kind == 'seal').mean()))
for _, r in SG.iterrows():
    say(f'  {r.sign} {r.picture[:34]:34s} faces {r.faces:4d} tablets {r.tablets:4d} ({100 * r.tablet_share:.0f}%) seals {r.seals:4d} ({100 * r.seal_share:.0f}%) copper {r.copper} tags {r.tags} pots {r.pots} rods {r.rods} | Harappa {r.harappa} Mohenjo {r.mohenjo} elsewhere {r.other_cities} | first sign {r.first_sign}')
# ---- P2 tails
say('\nTAILS after 413: faces starting 413-575 and faces starting 413-892 (any site)')
for pre in ('413-575', '413-892', '413'):
    m = F[[ '-'.join(f).startswith(pre) for f in F.f]]
    say(f'  faces starting {pre}: {len(m)}; kinds {fmt_counter(collections.Counter(m.kind))}; sites {fmt_counter(collections.Counter(m.site))}')
both = [f for f in F.f if '575' in f and '892' in f]
say(f'  faces with both 575 and 892: {len(both)}')
m413 = F[[ '413' in f for f in F.f]]
nxt = collections.Counter(f[f.index('413') + 1] if f.index('413') + 1 < len(f) else 'END' for f in m413.f)
say(f'  sign after 413 in all {len(m413)} faces holding 413: {fmt_counter(nxt, 12)}')
prv = collections.Counter(f[f.index('413') - 1] if f.index('413') > 0 else 'START' for f in m413.f)
say(f'  sign before 413: {fmt_counter(prv, 8)}')
say(f'  413 faces by kind: {fmt_counter(collections.Counter(m413.kind))}; by site: {fmt_counter(collections.Counter(m413.site))}')
# ---- pieces: contiguous 2- and 3-sign pieces of heading strings, where else
pieces = ['413-575', '575-335', '335-711', '413-575-335', '575-335-711', '413-575-335-711', '413-892', '892-824', '413-892-824', '415-578', '578-032', '032-824',
          '415-578-032', '578-032-824', '817-368', '368-690', '817-368-690', '415-220', '220-520', '415-220-520']
def has(f, p):
    p = p.split('-')
    return any(list(f[i:i + len(p)]) == p for i in range(len(f) - len(p) + 1))
PR = []
for p in pieces:
    m = F[[has(f, p) for f in F.f]]
    kc = collections.Counter(m.kind); sc = collections.Counter(m.site)
    PR.append(dict(piece=p, faces=len(m), objects=m.obj.nunique(), cities=m.site.nunique(), harappa=sc['Harappa'], mohenjo=sc['Mohenjo-daro'], seal=kc['seal'], tablet=kc['mtab'],
                   copper=kc['ctab'], tag=kc['tag'], pot=kc['pot'], rod=kc['rod'], other=kc['other'], sites=fmt_counter(sc)))
PR = pd.DataFrame(PR); PR.to_csv(f'{HOUT}/h3_pieces.csv', index=False)
say('\nPIECES OF HEADING STRINGS, whole corpus (face contains the piece in that order)')
for _, r in PR.iterrows():
    say(f'  {r.piece:18s} faces {r.faces:4d} objects {r.objects:4d} cities {r.cities}: seals {r.seal} tablets {r.tablet} copper {r.copper} tags {r.tag} pots {r.pot} rods {r.rod} | {r.sites}')

# ---- ties with seal lead signs
S = F[F.kind == 'seal'].copy()
S = S.drop_duplicates(['obj'])
def lead(f):
    t = list(f)
    front = ''
    if t and t[0] in OPENSLOT_OPEN: front = t[0]
    while t and t[0] in OPENSLOT: t = t[1:]
    return front, (t[0] if t else '')
OPENSLOT_OPEN = {s for s, c in V2.items() if c == 'OPEN'}
S['front'], S['lead'] = zip(*[lead(f) for f in S.f])
tot = pd.Series(use)
heads_signs = set(PARTS)
def S_count(s): return int(((S.lead == s) | (S.front == s)).sum())
say(f'\nSEAL TIES: seals {len(S)} (one per stone). S(s) = seals with s as crest/lead sign or front word; control = signs of similar total use')
tie = []
rngc = np.random.default_rng(3)
for s in PARTS:
    n_s = use[s]; c = tot[(tot >= n_s / 1.4) & (tot <= n_s * 1.4)].index
    c = [x for x in c if x not in heads_signs and x not in ('000',)]
    cnt = np.array([S_count(x) for x in c]); real = S_count(s)
    exp = cnt.mean() if len(cnt) else float('nan'); p = float((cnt >= real).mean()) if len(cnt) else float('nan')
    lead_n = int((S.lead == s).sum()); front_n = int((S.front == s).sum())
    tie.append(dict(sign=s, picture=pic(s), uses=n_s, seals_lead=lead_n, seals_front=front_n, S=real, control_signs=len(c), control_mean=round(exp, 2), control_max=int(cnt.max()) if len(cnt) else 0, P_ge=round(p, 3),
                    ratio=round(real / exp, 2) if exp else float('nan')))
TI = pd.DataFrame(tie); TI.to_csv(f'{HOUT}/h3_ties.csv', index=False)
for _, r in TI.iterrows():
    say(f'  {r.sign} {r.picture[:30]:30s} uses {r.uses:4d}: lead on {r.seals_lead} seals, front word on {r.seals_front}; control mean {r.control_mean} max {r.control_max} over {r.control_signs} signs; ratio {r.ratio}; P(control >= real) {r.P_ge}')
# lists of seals
for s in ('413', '415', '817', '690', '575', '892', '824'):
    m = S[(S.lead == s) | (S.front == s)]
    say(f'\n  seals with {s} as crest / front: {len(m)}')
    for o, site, f in list(zip(m.obj, m.site, m.f))[:12]:
        say(f'      {O.loc[o].cisi:8s} {site:14s} {O.loc[o].area[:14]:14s} {"-".join(f)}')
# 415-220 specifically (crest of the side face)
m = S[[ f[:2] == ('415', '220') or (len(f) > 2 and f[1:3] == ('415', '220')) for f in S.f]]
say(f'\nseals starting 415-220 (after front word): {len(m)}; sites {fmt_counter(collections.Counter(m.site))}')
m2 = S[[has(f, '415-220-520') for f in S.f]]
say(f'seals holding 415-220-520: {len(m2)}: ' + '; '.join(f'{O.loc[o].cisi} {site} {"-".join(f)}' for o, site, f in zip(m2.obj, m2.site, m2.f)))
# 415-220 on the control: how common is any 2-sign crest pair on seals
pairs = collections.Counter(f[:2] for f in S.f if len(f) >= 2)
say(f'(for scale: the commonest seal first pairs: {fmt_counter(pairs, 5)})')

# pair-level tie for the side face's crest pair 415-220 (and 220-520): matched pairs by total faces
allpairs = collections.Counter(); leadpairs = collections.Counter()
for f in F.f:
    for a, b in set(zip(f, f[1:])): allpairs[(a, b)] += 1
for f in S.f:
    t = list(f)
    while t and t[0] in OPENSLOT: t = t[1:]
    if len(t) >= 2: leadpairs[(t[0], t[1])] += 1
for pr in (('415', '220'), ('413', '575'), ('413', '892')):
    n_ = allpairs[pr]; c_ = [q for q, v in allpairs.items() if n_ / 1.4 <= v <= n_ * 1.4 and q not in (('415', '220'), ('413', '575'), ('413', '892')) and '000' not in q]
    cnt = np.array([leadpairs[q] for q in c_]); real = leadpairs[pr]
    say(f'pair {pr[0]}-{pr[1]}: faces {n_}; seal lead pair on {real} seals; control pairs {len(c_)} mean {cnt.mean():.2f} max {cnt.max()}; P(control >= real) {(cnt >= real).mean():.3f}')
say('done')
