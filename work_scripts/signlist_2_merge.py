#!/usr/bin/env python3
"""Sign list step 2: the merge rule and its controls. Rules written before this script's numbers.

MERGE RULE: two eligible signs (5+ uses) are one sign when at least two of the four evidence kinds (a) swaps, (b) neighbours,
(c) drawing, (d) other catalogue lumps them, fire (signlist_1_evidence.py), and neither veto holds:
  - co-occurrence veto: they share first-catalogue texts more than chance (Poisson P < 0.05, observed above expected);
  - numeral veto: different numerals. AMENDMENT, made after reading the evidence table and before any control or count
    in this script: the description-based numeral veto of step 1 missed 003/005 and 004/005 (the five is described in two
    rows, so the words differ beyond the number word). The veto now also holds when both signs are stroke numerals
    (frame-v2 class NUM_SHORT, NUM_TALL or NUM_NAME) with different shape codes. Same shape code (007 and 017, both
    "seven") is not vetoed.
GROUPS: pairs are linked strongest first (more kinds, then more swap frames, then higher similarity); a sign joins a group
  only if it has no veto with any sign already in it.
CONTROLS (1,000 deals each): the label each evidence kind is attached to is dealt at random, independently per kind:
  C1 within the 5 frequency bands (as asked: chance for "two kinds agree");
  C2 within frequency band x frame-v2 class (the strongest rival: two signs of the same job agree on corpus evidence
     because they do the same job, not because they are one sign).
  In a deal, pair (x, y) gets kind k's evidence of (pi_k x, pi_k y); vetoes stay with the real pair. Score = merged pairs.
REDESIGN (rule v2), written after the v1 controls below showed that merges resting only on (a)+(b) do not beat the
  same-job control C2 (5 against 2.17, P 0.074) and chain unrelated signs (176, 760, 773, 048, 222 ... into one group): a
  merge needs 2+ kinds AND at least one of them a form kind ((c) or (d)). (c) now includes the eye check of the glyphs
  (work_data/signlist/eye/eye_judgements.csv, made from the contact sheets of signlist_eye_sheets.py): (c) fires when the
  text rule fires and the eye does not call the drawings different, or when the eye calls them alike. Groups are built
  from rule v2. Both rules are reported with both controls.
RARE SIGNS (fewer than 5 uses, no corpus evidence possible): listed separately as FORM-ONLY merges when (c) and (d) both
  fire (same shape code or description overlap >= 0.6, and a shared Mahadevan number at share >= 0.25) and no numeral veto.
Outputs: work_data/signlist/merge_pairs.csv, merge_groups.csv, merge_controls.csv, log_merge.txt
"""
import itertools
from signlist_common import *

say = logger('merge')
P = pd.read_csv(f'{OUT}/pairs.csv', dtype={'a': str, 'b': str, 'mahadevan_shared': str}).fillna({'mahadevan_shared': ''})
S = pd.read_csv(f'{OUT}/signs.csv', dtype={'sign': str})
SH = shapes()
NUMC = {'NUM_SHORT', 'NUM_TALL', 'NUM_NAME'}
def code(s): return SH.get(s, ('', ''))[0]
P['numeral_veto2'] = P.numeral_veto | (P.class_a.isin(NUMC) & P.class_b.isin(NUMC) & (P.a.map(code) != P.b.map(code)))
P['veto'] = P.numeral_veto2 | P.cooc_veto
EYE = pd.read_csv(f'{OUT}/eye/eye_judgements.csv', dtype=str)
EYED = {}
for a, b, e in zip(EYE.a, EYE.b, EYE.eye): EYED[(a, b) if a < b else (b, a)] = e
P['eye'] = [EYED.get((a, b), '') for a, b in zip(P.a, P.b)]
P['c_final'] = (P.c_fire & (P.eye != 'different')) | (P.eye == 'alike')
P['n_kinds_v2'] = P.a_fire.astype(int) + P.b_fire.astype(int) + P.c_final.astype(int) + P.d_fire.astype(int)
P['merged_v2'] = (P.n_kinds_v2 >= 2) & (P.c_final | P.d_fire) & ~P.veto
P['merged'] = (P.n_kinds >= 2) & ~P.veto
KINDS = ['a_fire', 'b_fire', 'c_fire', 'd_fire']
real = int(P.merged.sum())
say(f'pairs with 2+ kinds: {int((P.n_kinds >= 2).sum())}; vetoed by co-occurrence {int(((P.n_kinds >= 2) & P.cooc_veto).sum())}, '
    f'by numeral {int(((P.n_kinds >= 2) & P.numeral_veto2).sum())}; MERGED PAIRS: {real}')
combo = P[P.merged].apply(lambda r: '+'.join(k[0] for k in KINDS if r[k]), axis=1)
say('merged pairs by which kinds agree:', combo.value_counts().to_dict())

# ---------------- controls ----------------
signs = list(S.sign); band = dict(zip(S.sign, S.band)); v2 = dict(zip(S.sign, S.v2))
EV = {k: {(a, b) for a, b, f in zip(P.a, P.b, P[k]) if f} for k in KINDS}
VETO = {(a, b) for a, b, f in zip(P.a, P.b, P.veto) if f}
def key(a, b): return (a, b) if a < b else (b, a)
def deal(strata, rng):
    perm = {}
    groups = collections.defaultdict(list)
    for s in signs: groups[strata(s)].append(s)
    for g in groups.values():
        sh = list(rng.permutation(g)); perm.update(zip(g, sh))
    return perm
inv_cache = {}
def run(strata, rng):
    # count pairs (x, y) whose dealt evidence has 2+ kinds and no real veto
    votes = collections.Counter()
    for k in KINDS:
        perm = deal(strata, rng); inv = {v: u for u, v in perm.items()}
        for (a, b) in EV[k]:
            x, y = inv[a], inv[b]            # the real pair that receives (a, b)'s evidence
            votes[key(x, y)] += 1
    return sum(1 for p, n in votes.items() if n >= 2 and p not in VETO), votes
out = []
for name, strata in (('C1 band', lambda s: band[s]), ('C2 band x class', lambda s: (band[s], v2[s]))):
    rng = np.random.default_rng(20261117)
    vals = []; combos = collections.Counter()
    for i in range(1000):
        bar(i, 1000, name, every=250)
        n, _ = run(strata, rng); vals.append(n)
    vals = np.array(vals)
    say(f'{name}: merged pairs mean {vals.mean():.2f}, 95th pct {np.quantile(vals, 0.95):.0f}, max {vals.max()}; real {real}; '
        f'P {pvalue_hi(vals, real):.4f}')
    out.append(dict(control=name, real=real, mean=round(vals.mean(), 2), p95=np.quantile(vals, 0.95), max=vals.max(), P=pvalue_hi(vals, real)))
# same controls for the merged pairs that rest on corpus + form (one of a/b and one of c/d)
cross = P.merged & (P.a_fire | P.b_fire) & (P.c_fire | P.d_fire)
say(f'merged pairs with corpus AND form evidence: {int(cross.sum())}; corpus only (a+b): {int((P.merged & ~(P.c_fire | P.d_fire)).sum())}; '
    f'form only (c+d): {int((P.merged & ~(P.a_fire | P.b_fire)).sum())}')
for name, strata in (('C1 band', lambda s: band[s]), ('C2 band x class', lambda s: (band[s], v2[s]))):
    rng = np.random.default_rng(7)
    vals = {'cross': [], 'ab': [], 'cd': []}
    for i in range(1000):
        votes = collections.defaultdict(set)
        for k in KINDS:
            perm = deal(strata, rng); inv = {v: u for u, v in perm.items()}
            for (a, b) in EV[k]: votes[key(inv[a], inv[b])].add(k[0])
        c1 = c2 = c3 = 0
        for p, ks in votes.items():
            if len(ks) < 2 or p in VETO: continue
            corp = bool(ks & {'a', 'b'}); form = bool(ks & {'c', 'd'})
            c1 += corp and form; c2 += corp and not form; c3 += form and not corp
        vals['cross'].append(c1); vals['ab'].append(c2); vals['cd'].append(c3)
    realv = {'cross': int(cross.sum()), 'ab': int((P.merged & ~(P.c_fire | P.d_fire)).sum()), 'cd': int((P.merged & ~(P.a_fire | P.b_fire)).sum())}
    for t in vals:
        v = np.array(vals[t])
        say(f'   {name}, {t}: real {realv[t]} against mean {v.mean():.2f} (max {v.max()}), P {pvalue_hi(v, realv[t]):.4f}')
        out.append(dict(control=f'{name} [{t}]', real=realv[t], mean=round(v.mean(), 2), p95=np.quantile(v, 0.95), max=v.max(), P=pvalue_hi(v, realv[t])))
pd.DataFrame(out).to_csv(f'{OUT}/merge_controls.csv', index=False)

# ---------------- rule v2 and its controls ----------------
real2 = int(P.merged_v2.sum())
combo2 = P[P.merged_v2].apply(lambda r: '+'.join(k for k, c in (('a', 'a_fire'), ('b', 'b_fire'), ('c', 'c_final'), ('d', 'd_fire')) if r[c]), axis=1)
say(f'RULE v2 (needs a form kind; eye in c): merged pairs {real2}; by kinds: {combo2.value_counts().to_dict()}')
EV2 = {k: {(a, b) for a, b, f in zip(P.a, P.b, P[c]) if f} for k, c in (('a', 'a_fire'), ('b', 'b_fire'), ('c', 'c_final'), ('d', 'd_fire'))}
for name, strata in (('C1 band', lambda s: band[s]), ('C2 band x class', lambda s: (band[s], v2[s]))):
    rng = np.random.default_rng(99); vals = []
    for i in range(1000):
        votes = collections.defaultdict(set)
        for k in EV2:
            perm = deal(strata, rng); inv = {v: u for u, v in perm.items()}
            for (a, b) in EV2[k]: votes[key(inv[a], inv[b])].add(k)
        vals.append(sum(1 for p, ks in votes.items() if len(ks) >= 2 and ks & {'c', 'd'} and p not in VETO))
    vals = np.array(vals)
    say(f'   v2 {name}: real {real2} against mean {vals.mean():.2f} (95th pct {np.quantile(vals, 0.95):.0f}, max {vals.max()}), P {pvalue_hi(vals, real2):.4f}')
    out.append(dict(control=f'v2 {name}', real=real2, mean=round(vals.mean(), 2), p95=np.quantile(vals, 0.95), max=vals.max(), P=pvalue_hi(vals, real2)))
pd.DataFrame(out).to_csv(f'{OUT}/merge_controls.csv', index=False)

# ---------------- groups ----------------
M = P[P.merged_v2].copy()
M['combo'] = combo2
M = M.sort_values(['n_kinds_v2', 'swap_frames', 'sim_leaveout'], ascending=False)
M.to_csv(f'{OUT}/merge_pairs.csv', index=False)
grp = {}; members = collections.defaultdict(set)
def gid(s): return grp.get(s)
for r in M.itertuples():
    ga, gb = gid(r.a), gid(r.b)
    A = members[ga] if ga else {r.a}; B = members[gb] if gb else {r.b}
    if ga and ga == gb: continue
    if any(key(x, y) in VETO for x in A for y in B):
        say(f'   link {r.a}-{r.b} refused: a veto between the two groups'); continue
    new = ga or gb or r.a
    allm = A | B
    for x in allm: grp[x] = new
    if ga and ga != new: members.pop(ga, None)
    if gb and gb != new: members.pop(gb, None)
    members[new] = allm
U = dict(zip(S.sign, S.uses))
G = []
for g, ms in members.items():
    ms = sorted(ms, key=lambda s: -U[s])
    ev = M[M.a.isin(ms) & M.b.isin(ms)]
    G.append(dict(group=ms[0], members='|'.join(ms), n=len(ms), uses=sum(U[s] for s in ms),
                  links='; '.join(f'{a}-{b} [{c}; swaps {sf}]' for a, b, c, sf in zip(ev.a, ev.b, ev.combo, ev.swap_frames)),
                  shapes=' / '.join(f'{s}: {SH.get(s, ("", "no description"))[1][:70]}' for s in ms)))
G = pd.DataFrame(G).sort_values(['n', 'uses'], ascending=False)
G.to_csv(f'{OUT}/merge_groups.csv', index=False)
say(f'groups: {len(G)}, holding {G.n.sum()} eligible signs; signs removed by merging: {G.n.sum() - len(G)}')

# ---------------- rare signs: form-only ----------------
L = load_lipi(); Uall = uses(L)
X = crosswalk(); X = X[X.share >= 0.25]
L2M = collections.defaultdict(set)
for l, m in zip(X.lipi, X.mahadevan): L2M[l].add(m)
import importlib.util
rare = sorted(s for s in Uall if Uall[s] < 5)
def words(t): return {w for w in re.findall(r'[a-z]{3,}', t.lower())}
def numfree(t): return re.sub(r'\b(one|two|three|four|five|six|seven|eight|nine|ten|single|simple)\b', '#', t.lower())
R = []
allsigns = sorted(Uall)
for a in rare:
    for b in allsigns:
        if a == b or (b in rare and b < a): continue
        if a not in SH or b not in SH: continue
        dm = L2M[a] & L2M[b]
        if not dm: continue
        (ca, ta), (cb, tb) = SH[a], SH[b]
        if ta != tb and numfree(ta) == numfree(tb): continue
        j = len(words(ta) & words(tb)) / max(1, len(words(ta) | words(tb)))
        if ca == cb or j >= 0.6:
            R.append(dict(rare=a, uses_rare=Uall[a], partner=b, uses_partner=Uall[b], shape_code_rare=ca, shape_code_partner=cb, mahadevan='|'.join(sorted(dm))))
R = pd.DataFrame(R); R.to_csv(f'{OUT}/merge_rare_formonly.csv', index=False)
say(f'rare signs (<5 uses): {len(rare)}; form-only links (c and d both): {len(R)} pairs, {R.rare.nunique() if len(R) else 0} rare signs')
