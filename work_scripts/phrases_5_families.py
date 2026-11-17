#!/usr/bin/env python3
"""PHRASES step 5: phrase families and paradigms. Fixed 2026-11-17 before the run.
  FRAME = a phrase with one slot blanked: e.g. 920-060-* (slot 3), *-740 (slot 1), 861-*. MEMBERS = the passing phrases (phrase_list.csv)
  that fit the frame, plus EXTENDED members: any run of the same length with 3+ distinct texts, in order >= 80%, lift >= 5 that fits a frame
  that has at least one passing member. FAMILY = a frame with 2+ members (at least one passing).
  PARADIGM = a family whose members behave alike: mean cosine of the members' context profiles ON THE SIDE OF THE SLOT (slot first: the class
  of the sign before the phrase; slot last: the class of the sign after it; slot inside: both) at or above the 75th percentile of the same
  cosine between random pairs of passing phrases of the same length and slot type (control: 20,000 random pairs). (The first run compared both
  sides, which makes *-740 families look alike because they share 740; redesign before the second run.) Filler classes are listed, not required.
  NUMBER FILLERS of a family = its filler signs whose v2 class is a number class (NUM_SHORT, NUM_TALL, NUM_NAME). Redesign after the first
  run (the context-profile cosine to the count signs lets fish signs in, because fish follow numbers): the cosine is kept only as a second
  list, 'count_like_not_number' = non-number-class fillers at or above the 90th percentile of the cosine (sign's class-before and class-after
  profile against the pooled profile of the count signs, itself left out, signs with 15+ uses).
  NUMBERED SERIES = a family with 2+ number fillers that make up at least half of the family's texts, or a paradigm whose fillers are all
  number fillers. Control: P(at least that many number fillers) if each filler were a random sign (binomial, base = share of number-class
  signs among the distinct signs of the corpus with 3+ uses).
  Also reported: whether the fillers are consecutive stroke numbers (sign shapes 001-007 short strokes, 031-036 tall).
PREDICTIONS: F1 20-60 families. F0 (new) number+thing families (*-390, *-405, *-407) and number+fish (*-220) show up as numbered series. F2 the ward variants 741 / 742 (/ 745) after 920-060 form a family; their filler signs (jar variants) are one class.
  F3 at least 3 numbered series (count-sign slots after a front word, e.g. 861-002-* / 820-002-*; before a counted thing). F4 end-sign
  families (*-740, *-520) have mixed first signs (not paradigms).
Output: work_data/phrases/families.csv, family_members.csv, count_likeness.csv, log_5.txt
"""
from phrases_common import *
LOG = open(f'{OUTP}/log_5.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n'); LOG.flush()
rng = np.random.default_rng(5)
from frame2_pictures import pic
P = pd.read_csv(f'{OUTP}/phrase_list.csv', dtype={'phrase': str})
T = distinct_texts(); nt, win, uni, N = count_phrases(T)
passing = {tuple(s.split('-')): r for s, r in zip(P.phrase, P.itertuples())}
def frames_of(p): return [(p[:j] + ('*',) + p[j + 1:], j) for j in range(len(p))]
pf = collections.defaultdict(list)
for p in passing:
    for f, j in frames_of(p): pf[f].append(p)
# extended
mem = collections.defaultdict(dict)   # frame -> {phrase: (n, passing)}
for f, ps in pf.items():
    for p in ps: mem[f][p] = (nt[len(p)][p], True)
for k in (2, 3, 4):
    for p, n in nt[k].items():
        if n < 3 or p in passing: continue
        rev = nt[k].get(p[::-1], 0) if p != p[::-1] else n
        if n / (n + rev) < 0.8: continue
        if n / expected(p, uni, N, win[k]) < 5: continue
        for f, j in frames_of(p):
            if f in pf: mem[f][p] = (n, False)
fam = {f: m for f, m in mem.items() if len(m) >= 2}
say('frames with a passing member', len(pf), ' families (2+ members):', len(fam))
# context profiles
CL = ['START', 'END'] + [c for c in V2_PLAIN if c not in ('START', 'END')]
ci = {c: i for i, c in enumerate(CL)}
def outside(p):
    v = np.zeros(2 * len(CL)); k = len(p)
    for x in T:
        for (i, st, en) in positions(x, p):
            prev = 'START' if i == 0 else (v2c(x[i - 1]) if is_sign(x[i - 1]) else None)
            nxt = 'END' if i + k == len(x) else (v2c(x[i + k]) if is_sign(x[i + k]) else None)
            if prev: v[ci[prev]] += 1
            if nxt: v[len(CL) + ci[nxt]] += 1
    return v
def side(v, j, k):
    """keep only the half(s) of the outside profile on the slot side."""
    w = v.copy(); L = len(CL)
    if j == 0 and k > 1: w[L:] = 0          # slot first: keep the 'before' half
    elif j == k - 1 and k > 1: w[:L] = 0    # slot last: keep the 'after' half
    return w
def cos(a, b):
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    return float(a @ b / (na * nb)) if na and nb else 0.0
ctx = {}
def cx(p):
    if p not in ctx: ctx[p] = outside(p)
    return ctx[p]
# control for member similarity
allp = list(passing)
bylen = collections.defaultdict(list)
for p in allp: bylen[len(p)].append(p)
ctl = {}
for k, lst in bylen.items():
    if len(lst) < 3: continue
    for typ in ('first', 'last', 'inner'):
        if typ == 'inner' and k == 2: continue
        j = {'first': 0, 'last': k - 1, 'inner': 1}[typ]; ctl[(k, typ)] = []
        for _ in range(20000):
            a, b = rng.choice(len(lst), 2, replace=False); ctl[(k, typ)].append(cos(side(cx(lst[a]), j, k), side(cx(lst[b]), j, k)))
q75 = {k: float(np.percentile(v, 75)) for k, v in ctl.items() if v}; med = {k: float(np.median(v)) for k, v in ctl.items() if v}
say('control: random pairs of passing phrases, cosine median / 75th pct by length:', {k: (round(med[k], 2), round(q75[k], 2)) for k in q75})
# sign context profile for count-likeness
sprof = collections.defaultdict(lambda: np.zeros(2 * len(CL))); suse = collections.Counter()
for x in T:
    for r in runs(x):
        pass
    n = len(x)
    for i, s in enumerate(x):
        if not is_sign(s): continue
        suse[s] += 1
        prev = 'START' if i == 0 else (v2c(x[i - 1]) if is_sign(x[i - 1]) else None)
        nxt = 'END' if i + 1 == n else (v2c(x[i + 1]) if is_sign(x[i + 1]) else None)
        if prev: sprof[s][ci[prev]] += 1
        if nxt: sprof[s][len(CL) + ci[nxt]] += 1
NUMC = {'NUM_SHORT', 'NUM_TALL', 'NUM_NAME'}
numsigns = [s for s in suse if v2c(s) in NUMC and suse[s] >= 5]
cent = sum(sprof[s] for s in numsigns)
def countlike(s):
    c = cent - sprof[s] if s in numsigns else cent
    return cos(sprof[s], c)
big = [s for s in suse if suse[s] >= 15]
CLK = pd.DataFrame([dict(sign=s, uses=suse[s], v2=v2c(s), count_like=countlike(s)) for s in big])
CLK['pct'] = CLK.count_like.rank(pct=True)
p75c = float(np.percentile(CLK.count_like, 75)); p90c = float(np.percentile(CLK.count_like, 90)); CLK.to_csv(f'{OUTP}/count_likeness.csv', index=False)
say(f'count-likeness: {len(big)} signs with 15+ uses; 75th percentile cosine {p75c:.3f}; number-class signs median {CLK[CLK.v2.isin(NUMC)].count_like.median():.3f} vs others {CLK[~CLK.v2.isin(NUMC)].count_like.median():.3f}')
cdict = dict(zip(CLK.sign, CLK.count_like))
voc3 = [s for s in suse if suse[s] >= 3]; BASE_NUM = sum(1 for s in voc3 if v2c(s) in NUMC) / len(voc3); say('base share of number-class signs among distinct signs with 3+ uses:', round(BASE_NUM, 3))
SHORT = [f'{i:03d}' for i in range(1, 8)]; TALL = [f'{i:03d}' for i in range(31, 37)]
rows = []; mrows = []
for f, m in fam.items():
    k = len(f); j = f.index('*')
    fill = {p[j]: m[p][0] for p in m}
    members = sorted(m, key=lambda p: -m[p][0])
    classes = collections.Counter(v2c(s) for s in fill)
    cs = [cos(side(cx(a), j, k), side(cx(b), j, k)) for i, a in enumerate(members) for b in members[i + 1:]]
    mcos = float(np.mean(cs)) if cs else np.nan
    oneclass = len(classes) == 1
    typ = 'first' if j == 0 else ('last' if j == k - 1 else 'inner'); alike = mcos >= q75.get((k, typ), 1.0)
    numeric = all(v2c(s) in NUMC for s in fill)
    numf = [s for s in fill if v2c(s) in NUMC]
    likeother = [s for s in fill if v2c(s) not in NUMC and cdict.get(s, 0) >= p90c]
    numtexts = sum(fill[s] for s in numf); share_num = numtexts / sum(fill.values())
    from scipy.stats import binom
    p_num = 1 - binom.cdf(len(numf) - 1, len(fill), BASE_NUM) if numf else 1.0
    cl_like = [cdict.get(s) for s in fill if s in cdict]
    countlike_all = len(cl_like) == len(fill) and all(c >= p75c for c in cl_like)
    stroke_consec = all(s in SHORT or s in TALL for s in fill)
    rows.append(dict(frame='-'.join(f), length=k, slot=j + 1, n_members=len(m), n_passing=sum(1 for p in m if m[p][1]), total_texts=sum(v[0] for v in m.values()),
                     fillers=' '.join(f'{s}({n})' for s, n in sorted(fill.items(), key=lambda t: -t[1])), filler_classes='; '.join(f'{c} {n}' for c, n in classes.most_common()),
                     filler_pictures='; '.join(pic(s) for s in sorted(fill, key=lambda s: -fill[s])[:6]), one_class=oneclass, member_cosine=round(mcos, 3) if mcos == mcos else '',
                     control_q75=round(q75.get((k, typ), np.nan), 3), behave_alike=alike, paradigm=bool(oneclass and alike),
                     all_number_class=numeric, all_count_like=countlike_all, stroke_series=stroke_consec,
                     count_like_not_number=' '.join(likeother), number_fillers=' '.join(f'{s}({fill[s]})' for s in sorted(numf, key=lambda s: -fill[s])), n_number_fillers=len(numf), number_share_of_texts=round(share_num, 3),
                     P_number_fillers=round(p_num, 5),
                     numbered_series=bool((len(numf) >= 2 and share_num >= 0.5) or (alike and numeric))))
    for p in members: mrows.append(dict(frame='-'.join(f), member='-'.join(p), n_texts=m[p][0], passing=m[p][1]))
Fm = pd.DataFrame(rows).sort_values('total_texts', ascending=False)
Fm.to_csv(f'{OUTP}/families.csv', index=False); pd.DataFrame(mrows).to_csv(f'{OUTP}/family_members.csv', index=False)
say('families', len(Fm), ' paradigms', int(Fm.paradigm.sum()), ' numbered series', int(Fm.numbered_series.sum()), ' one-class', int(Fm.one_class.sum()), ' behave-alike', int(Fm.behave_alike.sum()))
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 60)
say(Fm[['frame', 'n_members', 'total_texts', 'fillers', 'member_cosine', 'control_q75', 'paradigm', 'n_number_fillers', 'numbered_series']].head(60).to_string())
say('numbered series:', Fm[Fm.numbered_series][['frame', 'fillers', 'number_fillers', 'number_share_of_texts', 'P_number_fillers', 'paradigm']].to_string())
say('paradigms:', Fm[Fm.paradigm][['frame', 'fillers', 'member_cosine', 'control_q75']].to_string())
