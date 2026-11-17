#!/usr/bin/env python3
"""HANDS steps 2 and 3: build the pair lists and picture sheets. Written 2026-11-17. Predictions BEFORE any pair was judged.
HAND FEATURES (fixed in advance; each pair is judged on these and nothing else): (1) bull's eye: dot / ring / slit / not drawn;
(2) horn: shape and how it joins the head; (3) collar and shoulder mark: how many neck lines, whether a shoulder mark exists
and its form; (4) the stand or feeding trough in front of the animal: shape; (5) stroke depth and width of the signs, and
sign proportions (tall-thin / short-wide); (6) spacing between signs; (7) frame line: present or not. Calls: same (>=4 features
agree and no clear clash), near (3 agree, none clash), different (2+ clash), cannot tell (photo too poor / animal missing /
one stone a bar). Same-or-near is the 'alike' class.
DEFINITIONS. Text-sharing pair: two seals, each with a photo and an animal (not blank), square (SEAL:S), from DIFFERENT cities
(site names differ, 'Unknown' left out), sharing a contiguous run of 3+ signs (no 000/ALT inside the run); the 29 twin pairs
already looked at are left out; no seal is used more than twice; pairs are dealt round-robin over city pairs so that Lothal,
Kalibangan, Chanhu-daro and Banawali are in; seed 2101. Control pair: for each text pair, one pair from the same two cities,
same 'both unicorn' status, sharing no contiguous run of 2+ signs (and no run 3+); seed 2102. 120 pairs shuffled (seed 2103)
and shown with random labels only (no ids, no sites, no texts); the key sits in hands_pairs_key.csv and is not opened until
all 120 are judged.
Mohenjo-daro (step 3): seals with photo, animal (not blank), square. Building = the catalogue house (street/trench names such
as First Street, Trench E are NOT buildings and are left out). Area = first word of the catalogue area (DKG, VSA, HR ...,
'DKG. (N)' and 'DKG. (S)' count as DKG). 60 same-building pairs (max 3 pairs per building), 60 different-building pairs in
the same area, 60 pairs from different areas; no seal used more than twice; seed 2104; shuffled with seed 2105.
PREDICTIONS (written first): text-sharing pairs alike (same or near) 25-35 percent, control 10-18 percent. Mohenjo-daro
same-building alike about 25 percent, other buildings in the same area about 18 percent, different areas about 15 percent;
so a building does NOT get its seals from one cutter (gap under 10 points)."""
import sys; sys.path.insert(0, "/home/claude/ivc/work_scripts")
from hands_common import *
S = load(); S['n'] = S.n.astype(int)
tally = pd.read_csv(f'{ROOT}/work_data/twins/photo_tally.csv', dtype=str)
done = {frozenset([a, b]) for a, b in zip(tally.a, tally.b)}
# ---- twin re-look sheets
rl = tally[tally.hand != 'different']
items = []
for r in rl.itertuples():
    for lab, c, f in [('A', r.a, r.photo_a), ('B', r.b, r.photo_b)]:
        items.append((f'T{r.pair}{lab} {c} {r.site_a[:4] if lab=="A" else r.site_b[:4]}', f))
for k in range(0, len(items), 8): sheet(items[k:k+8], f'{OUT}/relook_sheet_{k//8+1}.jpg', cols=4, W=330, H=330)
# ---- eligible seals
E = S[(S.photo != '') & (~S.animal.isin(['none', ''])) & (S.type == 'SEAL:S') & (S.site != 'Unknown')].copy()
E = E[E.signs != ''].drop_duplicates('cisi')
def clean(s): return [t for t in s.split('-')]
def runs(s, k):
    x = clean(s); out = set()
    for i in range(len(x) - k + 1):
        w = x[i:i+k]
        if not any(t in ('000', 'ALT') for t in w): out.add(tuple(w))
    return out
E['r3'] = E.signs.map(lambda s: runs(s, 3)); E['r2'] = E.signs.map(lambda s: runs(s, 2))
rows = E.to_dict('records')
by3 = collections.defaultdict(list)
for i, r in enumerate(rows):
    for g in r['r3']: by3[g].append(i)
cand = {}
for g, ids in by3.items():
    for a in range(len(ids)):
        for b in range(a + 1, len(ids)):
            i, j = ids[a], ids[b]
            if rows[i]['site'] == rows[j]['site']: continue
            if frozenset([rows[i]['cisi'], rows[j]['cisi']]) in done: continue
            cand[(min(i, j), max(i, j))] = g
print('text-sharing candidate pairs', len(cand))
cp = collections.defaultdict(list)
for (i, j), g in cand.items(): cp[tuple(sorted([rows[i]['site'], rows[j]['site']]))].append((i, j, g))
random.seed(2101)
for k in cp: random.shuffle(cp[k])
print({k: len(v) for k, v in cp.items()})
used = collections.Counter(); T = []; keys = sorted(cp); ptr = {k: 0 for k in keys}
while len(T) < 60 and any(ptr[k] < len(cp[k]) for k in keys):
    for k in keys:
        if len(T) >= 60: break
        while ptr[k] < len(cp[k]):
            i, j, g = cp[k][ptr[k]]; ptr[k] += 1
            if used[i] >= 2 or used[j] >= 2: continue
            # at most 3 pairs per run text
            if sum(1 for t in T if t[2] == g) >= 3: continue
            used[i] += 1; used[j] += 1; T.append((i, j, g)); break
print('text pairs', len(T), collections.Counter(tuple(sorted([rows[i]['site'], rows[j]['site']])) for i, j, g in T))
# controls
random.seed(2102); Cn = []; usedc = collections.Counter()
for (i, j, g) in T:
    si, sj = rows[i]['site'], rows[j]['site']; both_uni = rows[i]['animal'] == 'unicorn' and rows[j]['animal'] == 'unicorn'
    pool = [(a, b) for a in range(len(rows)) for b in range(len(rows)) if False]
    A_ = [k for k, r in enumerate(rows) if r['site'] == si]; B_ = [k for k, r in enumerate(rows) if r['site'] == sj]
    tries = 0
    while tries < 4000:
        tries += 1; a = random.choice(A_); b = random.choice(B_)
        if a == b or usedc[a] >= 2 or usedc[b] >= 2: continue
        if (rows[a]['animal'] == 'unicorn' and rows[b]['animal'] == 'unicorn') != both_uni: continue
        if rows[a]['r2'] & rows[b]['r2']: continue
        if any(a == x or a == y for x, y in [(i, j)] ) and False: continue
        usedc[a] += 1; usedc[b] += 1; Cn.append((a, b)); break
print('controls', len(Cn))
allp = [('text', i, j, ' '.join(g)) for i, j, g in T] + [('control', a, b, '') for a, b in Cn]
random.seed(2103); random.shuffle(allp)
K = []
for n_, (kind, i, j, g) in enumerate(allp, 1):
    K.append(dict(pid=f'X{n_:03d}', kind=kind, a=rows[i]['cisi'], b=rows[j]['cisi'], site_a=rows[i]['site'], site_b=rows[j]['site'],
                  animal_a=rows[i]['animal'], animal_b=rows[j]['animal'], signs_a=rows[i]['signs'], signs_b=rows[j]['signs'], shared_run=g,
                  shared_sign_count=len(set(clean(rows[i]['signs'])) & set(clean(rows[j]['signs']))), photo_a=rows[i]['photo'], photo_b=rows[j]['photo']))
K = pd.DataFrame(K); K.to_csv(f'{OUT}/hands_pairs_key.csv', index=False)
def pair_sheets(K, prefix, per=6):
    for s in range(0, len(K), per):
        part = K.iloc[s:s+per]; W = 245
        im = Image.new('RGB', (2 * (2 * W + 14) + 10, 3 * (W + 22)), 'white'); dr = ImageDraw.Draw(im); f = font(13)
        for k, r in enumerate(part.itertuples()):
            x0 = (k % 2) * (2 * W + 24); y0 = (k // 2) * (W + 22)
            dr.text((x0 + 3, y0 + 2), r.pid, fill='red', font=f)
            for c, fn in enumerate([r.photo_a, r.photo_b]):
                p = Image.open(f'{IMG}/{fn}').convert('RGB'); p.thumbnail((W, W)); im.paste(p, (x0 + c * (W + 4), y0 + 20))
        im.save(f'{OUT}/{prefix}_{s//per+1:02d}.jpg', quality=72)
pair_sheets(K[['pid', 'photo_a', 'photo_b']], 'xc_sheet')
print('xc sheets', (len(K) + 5) // 6)
# ---- Mohenjo-daro
M = E[E.site == 'Mohenjo-daro'].copy()
M['bld'] = M.house.where(~M.house.str.contains('Street|Trench|Lane', regex=True), '')
M['bld'] = np.where(M.bld != '', M.area_key + '|' + M.bld, '')
M['fam'] = M.area.map(lambda a: re.sub(r'[^A-Za-z]', '', a.split()[0].split('.')[0].split('(')[0]) if a else '')
M = M[M.fam != '']
Mb = M[M.bld != ''].copy()
print('MD seals', len(M), 'with building', len(Mb))
Mr = Mb.to_dict('records'); random.seed(2104)
def sample_pairs(kind, n):
    allp = []
    if kind == 'same_building':
        g = collections.defaultdict(list)
        for i, r in enumerate(Mr): g[r['bld']].append(i)
        for b, ids in g.items():
            ps = [(a, c) for x, a in enumerate(ids) for c in ids[x+1:]]; random.shuffle(ps)
            allp += [(a, c) for a, c in ps[:3]]
    else:
        ids = list(range(len(Mr)))
        for _ in range(400000):
            a, c = random.sample(ids, 2)
            ra, rc = Mr[a], Mr[c]
            if kind == 'diff_building_same_area' and ra['fam'] == rc['fam'] and ra['bld'] != rc['bld']: allp.append((a, c))
            if kind == 'diff_area' and ra['fam'] != rc['fam']: allp.append((a, c))
            if len(allp) > 3000: break
    random.shuffle(allp); out = []; u = collections.Counter(); seen = set()
    for a, c in allp:
        if u[a] >= 2 or u[c] >= 2 or (a, c) in seen: continue
        u[a] += 1; u[c] += 1; seen.add((a, c)); out.append((kind, a, c))
        if len(out) == n: break
    return out
MP = sample_pairs('same_building', 60) + sample_pairs('diff_building_same_area', 60) + sample_pairs('diff_area', 60)
print({k: sum(1 for p in MP if p[0] == k) for k in ['same_building', 'diff_building_same_area', 'diff_area']})
random.seed(2105); random.shuffle(MP)
K2 = []
for n_, (kind, a, c) in enumerate(MP, 1):
    ra, rc = Mr[a], Mr[c]
    K2.append(dict(pid=f'Y{n_:03d}', kind=kind, a=ra['cisi'], b=rc['cisi'], bld_a=ra['bld'], bld_b=rc['bld'], fam_a=ra['fam'], fam_b=rc['fam'],
                   animal_a=ra['animal'], animal_b=rc['animal'], signs_a=ra['signs'], signs_b=rc['signs'], same_text=ra['signs'] == rc['signs'],
                   photo_a=ra['photo'], photo_b=rc['photo']))
K2 = pd.DataFrame(K2); K2.to_csv(f'{OUT}/hands_md_key.csv', index=False)
pair_sheets(K2[['pid', 'photo_a', 'photo_b']], 'md_sheet')
print('md sheets', (len(K2) + 5) // 6)
