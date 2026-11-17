#!/usr/bin/env python3
"""HEADS 6: Harappa heading faces against Mohenjo-daro's copper tablets (jobs/out/copper.md).  Predictions written 2026-11-17 BEFORE
these numbers:
  P1. No heading string (413-575..., 413-892..., 817-368-690, 415-578-...) occurs on any copper text face; the heading signs
      413, 575, 335, 711, 892, 824, 578 occur on 0 copper faces (copper texts have their own vocabulary: 134 of 162 copper tablets
      carry a sign pair found on no other kind of object).
  P2. The picture-replacing signs 777, 780, 781, 782, 753, 749, 841, 341 do not stand on Harappa heading faces and occur on at most
      3 Harappa objects in all; they are copper-picture signs.
  P3. The two systems have the same shape although they share no signs: on copper one text carries one picture (21 of 21 pairs of
      copies read by eye) and one picture covers several texts; at Harappa a name that stands under a heading keeps that heading
      (same-name pairs share the heading far above chance) and a heading covers many names (names per heading 4 to 12).
      Test for Harappa: among pairs of heading issues with the same name, the share with the same heading, against the heading
      label dealt at random among the heading issues (20,000 deals).
  P4. Count signs differ in the same direction: copper counts the big measure/tree, 413-575 (the heading with the big measure)
      is the Harappa heading that sits with big-measure names (copper 705/706 on 34 of 58 count faces against 6% at Harappa).
Outputs: work_data/heads/h6_copper.csv, h6_log.txt.   Run: python3 heads_6_copper.py (seconds)
"""
from heads_common import *
say = log_to(f'{HOUT}/h6_log.txt')
rng = np.random.default_rng(6)
with contextlib.redirect_stdout(io.StringIO()):
    O = load()
CU = O[O.kind == 'ctab']
say(f'copper tablets {len(CU)} (sites {fmt_counter(collections.Counter(CU.site))}); faces {int(CU.nfaces.sum())}')
HEAD = pd.read_csv(f'{HOUT}/h1_headings.csv', dtype=str)
HOB = pd.read_csv(f'{HOUT}/h1_objects.csv', dtype=str).fillna('')
heads_faces = sorted(set(HOB.face))
copper_faces = [(o, r.cisi, face_str(f)) for o, r in CU.iterrows() for f in r.faces]
def has(f, p):
    f = f.split('-'); p = p.split('-')
    return any(f[i:i + len(p)] == p for i in range(len(f) - len(p) + 1))
say('\n(1) heading strings and their 2-sign pieces on copper faces')
pieces = set()
for hf in heads_faces:
    t = hf.split('-')
    pieces.add(hf)
    for i in range(len(t) - 1): pieces.add('-'.join(t[i:i + 2]))
rows = []
for p in sorted(pieces):
    hits = [(c, f) for o, c, f in copper_faces if has(f, p)]
    rows.append(dict(piece=p, copper_faces=len(hits), examples='; '.join(f'{c} {f}' for c, f in hits[:4])))
CP = pd.DataFrame(rows); CP.to_csv(f'{HOUT}/h6_copper.csv', index=False)
say(f'  whole heading faces on copper: {sum(1 for hf in heads_faces for o, c, f in copper_faces if f == hf)}')
for _, r in CP[CP.copper_faces > 0].iterrows(): say(f'  piece {r.piece:14s} on {r.copper_faces} copper faces: {r.examples}')
say(f'  pieces with no copper face: {int((CP.copper_faces == 0).sum())} of {len(CP)}')
say('\n(2) single signs of the headings on copper:')
sgn = sorted({s for hf in heads_faces for s in hf.split('-')})
for s in sgn:
    n = sum(1 for o, c, f in copper_faces if s in f.split('-'))
    allu = sum(1 for f in O.faces for ff in f for x in ff if x == s)
    say(f'  sign {s} {pic(s)[:30]:30s}: copper faces {n}; all faces {allu}')
say('\n(3) the picture-replacing signs 777 780 781 782 753 749 841 341 (and 957) across the corpus')
PS = ['777', '780', '781', '782', '753', '749', '841', '341', '957']
for s in PS:
    m = [(r.site, r.kind, r.cisi, face_str(f)) for o, r in O.iterrows() for f in r.faces if s in f]
    kc = collections.Counter((a, b) for a, b, c, d in m)
    harap = [x for x in m if x[0] == 'Harappa']
    say(f'  {s}: faces {len(m)}; by (site, kind): {fmt_counter(kc, 6)}; Harappa {len(harap)}' + (': ' + '; '.join(f'{c} {k} {d}' for a, k, c, d in harap[:5]) if harap else ''))
hf_signs = set(sgn)
ps_on_heads = [s for s in PS if s in hf_signs]
say(f'  picture-replacing signs inside a heading string: {ps_on_heads or "none"}')
# partner faces of heading tablets
partner_has = []
for _, r in HOB.iterrows():
    for p in r.partners.split(' / '):
        for s in PS:
            if s in p.split('-'): partner_has.append((r.cisi, s, p))
say(f'  picture-replacing signs on a partner face of a heading tablet: {partner_has or "none"}')

say('\n(4) the shape: does a name keep its heading, as a copper text keeps its picture?')
U = pd.read_csv(f'{HOUT}/h2_under.csv', dtype=str).fillna('')
U = U[U.name != ''].copy()
def strip_amount(n):
    t = n.split('-')
    for i, x in enumerate(t):
        if x in ('700', '705', '706') and i + 1 < len(t) and all(y in NUM or y in ('700', '705', '706') for y in t[:i + 1]): return '-'.join(t[i + 1:])
    return n
U['name1'] = [strip_amount(n.split('; ')[0]) for n in U.name]
HH = harappa_stones(); iss = dict(zip(HH.obj.astype(str), HH.issue))
U['issue'] = [iss.get(str(o), str(o)) for o in U.obj]
U = U.drop_duplicates(['family', 'issue', 'name1'])
def pairs_same(fams, names):
    same = tot = 0
    idx = collections.defaultdict(list)
    for i, n in enumerate(names): idx[n].append(i)
    for n, ii in idx.items():
        for a in range(len(ii)):
            for b in range(a + 1, len(ii)):
                tot += 1; same += fams[ii[a]] == fams[ii[b]]
    return same, tot
fams = U.family.values; names = U.name1.values
same, tot = pairs_same(fams, names)
nl = []
for _ in range(20000):
    s_, t_ = pairs_same(rng.permutation(fams), names); nl.append(s_)
nl = np.array(nl)
say(f'  pairs of heading issues with the same name: {tot}; same heading in {same}; chance {nl.mean():.2f}; P(>=) {pvalue_hi(nl, same):.4f}')
say(f'  names per heading (distinct, issues with a name partner): ' + '; '.join(f'{f} {U[U.family == f].name1.nunique()}' for f in HEAD.family))
say('  copper (from jobs/out/copper.md, rerun-able in work_scripts/copper_2_pairs.py): one text one picture, 21 of 21 pairs against 0.059 chance; 8 of 13 pictures cover 2+ text families')
say('  copper count faces: big measure on 20 (705) + 14 (706) of 58 against 6.4% of Harappa tablets; Harappa big measure sits under heading 413-575 (8 of 13 tablets) and nowhere else among headings')
# Count the Harappa-wide vocabulary overlap with copper at sign-pair level for the heading pieces (control): random 2-sign pieces
say('\n(5) control: share of Harappa 2-sign pieces from tablet faces (length 3+) that occur on a copper face')
allp = collections.Counter()
for o, r in O[(O.site == 'Harappa') & (O.kind == 'mtab')].iterrows():
    for f in r.faces:
        for a, b in set(zip(f, f[1:])):
            if '000' not in (a, b): allp[(a, b)] += 1
cp = {(a, b) for o, c, f in copper_faces for a, b in zip(f.split('-'), f.split('-')[1:])}
cands = [p for p, n in allp.items() if n >= 4]
hp = {(p.split('-')[i], p.split('-')[i + 1]) for p in pieces for i in range(len(p.split('-')) - 1)}
on_c = np.mean([p in cp for p in cands]); hon = np.mean([p in cp for p in hp])
say(f'  Harappa tablet pairs seen 4+ times: {len(cands)}; on copper {100 * on_c:.1f}%; heading pairs {len(hp)}; on copper {100 * hon:.1f}% ({sum(p in cp for p in hp)})')

say('\n(6) the big-measure line: faces with 705/706 then 033 (three big measures), where they stand')
def big3(f):
    t = f.split('-')
    return any(t[k] in ('705', '706') and t[k + 1] == '033' for k in range(len(t) - 1))
rows6 = []
for o, r in O.iterrows():
    for f in r.faces:
        fs = face_str(f)
        if big3(fs): rows6.append((r.site, r.kind, r.cisi, fs))
kc = collections.Counter((a, b) for a, b, c, d in rows6)
say(f'  faces with 705/706-033: {len(rows6)}; by (site, kind): {fmt_counter(kc, 8)}')
hp_ = HOB[HOB.family == '413-575']
hb = [r for _, r in hp_.iterrows() if any(big3(p) for p in r.partners.split(' / '))]
hb_h = int((H_ := harappa_stones()).shape[0])
tab_big = [(c, d) for a, b, c, d in rows6 if a == 'Harappa' and b == 'mtab']
tab_big_u = len(set(c for c, d in tab_big))
say(f'  Harappa clay-tablet objects with a 705/706-033 face: {tab_big_u}; of them beside the 413-575 heading: {len(hb)}')
say('  Harappa 705/706-033 tablet faces: ' + '; '.join(sorted(set(d for c, d in tab_big)))[:900])
say('  copper 705/706-033 faces: ' + '; '.join(sorted(set(d for a, b, c, d in rows6 if b == 'ctab')))[:900])
say('done')
