#!/usr/bin/env python3
"""LUMPS step 2: stratum A (lumps proper), name stamp beside short stamp.  Predictions written before the numbers:
 P1 short tail sign = crest of the name stamp on the same lump: above chance (stamps.md guess).
 P2 short stamp shares a sign with the heading (field) of the name stamp: above chance (front word of both).
 P3 the same short stamp is not tied to one name stamp (free pairing); a name stamp keeps different short stamps.
 P4 order: name stamp first.  Roles mix: name+short on one lump above chance.
Chance = short-stamp sets dealt among eligible lumps of the same site, 20,000 deals; P_ge = share of deals >= real.
Output: work_data/lumps/log_2.txt
"""
import sys, os, collections
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from lump_common import *
rng = np.random.default_rng(2026)
NS = 20000
I, steps = load_lumps(); T = lump_table(I)
VAR = os.environ.get('LUMP_VARIANT', 'base')
fh = open(f'{OUT}/log_2_{VAR}.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); fh.write(s + '\n')
say('steps', steps)
A = T[T.stratum == 'A'].reset_index(drop=True)
say('stratum A lumps', len(A), 'by site', A.site.value_counts().to_dict(), 'by catalogue', A.cat.value_counts().to_dict())
say('lumps with name', (A.names.map(len) > 0).sum(), 'with short', (A.shorts.map(len) > 0).sum(),
    'with both', ((A.names.map(len) > 0) & (A.shorts.map(len) > 0)).sum())
E = A[(A.names.map(len) > 0) & (A.shorts.map(len) > 0)].reset_index(drop=True)
say('\nELIGIBLE name+short lumps:')
for r in E.itertuples():
    say(' ', r.label, r.site, '|', ' / '.join(s['text'] + '<' + s['role'][:2] + '>' for s in r.stamps))
CREST = {'140', '220', '222', '226', '231', '233', '235', '240', '243', '803', '806'}

def short_signs(sh):    # content signs of the short stamps
    return {x for s in sh for x in sset(s['tail'])}
def short_front(sh):
    out = set()
    for s in sh:
        for x in sset(s['text']):
            if x in OPEN: out.add(x)
    return out
def name_crest_cls(nm): return {x for n in nm for x in n['crest_cls'].split() }
def name_crest_first(nm): return {n['crest'] for n in nm if n['crest'] and not wild(n['crest'])}
def name_body(nm): return {x for n in nm for x in sset(n['body'])}
def name_field(nm): return {x for n in nm for x in sset(n['field']) if x not in SLOT}

def test(title, ok_short, ok_name, match):
    """eligible: lumps where both sides have something to compare; stat = lumps with a match."""
    el = [i for i, r in E.iterrows() if ok_short(r.shorts) and ok_name(r.names)]
    if not el: say(title, 'no eligible lumps'); return
    sub = E.loc[el].reset_index(drop=True)
    names = list(sub.names); shorts = list(sub.shorts); sites = list(sub.site)
    obs = sum(match(n, s) for n, s in zip(names, shorts))
    null = []
    for _ in range(NS):
        sh = deal(shorts, sites, rng)
        null.append(sum(match(n, s) for n, s in zip(names, sh)))
    p = pvals(obs, null)
    say(f'{title}: eligible lumps {len(sub)}; matches {obs}; chance {p["chance"]:.2f}; P_ge {p["p_ge"]:.4f}; P_le {p["p_le"]:.4f}')
    for n, s, l in zip(names, shorts, sub.label):
        m = match(n, s)
        say('    ', l, 'name', [x['text'] for x in n], 'short', [x['text'] for x in s], 'MATCH' if m else '')
    return p

say('\n=== ITEM 1: short stamp sign(s) vs crest of name stamp ===')
has_tail = lambda sh: len(short_signs(sh)) > 0
test('1a tail sign = crest-class sign of the name (frame v2 CREST class)', has_tail, lambda nm: len(name_crest_cls(nm)) > 0,
     lambda n, s: len(short_signs(s) & name_crest_cls(n)) > 0)
test('1b tail sign = first non-number sign of the name body (FRAME definition of crest)', has_tail, lambda nm: len(name_crest_first(nm)) > 0,
     lambda n, s: len(short_signs(s) & name_crest_first(n)) > 0)
test('1c tail sign = any sign of the name body (control, widest)', has_tail, lambda nm: len(name_body(nm)) > 0,
     lambda n, s: len(short_signs(s) & name_body(n)) > 0)

# class level: is the short tail itself a crest-class sign (fish-type), whichever fish
tails = [(r.site, x) for r in E.itertuples() for x in [sorted(short_signs(r.shorts))] if x]
k = sum(any(t in CREST for t in x) for _, x in tails)
pool = [(r.site, x) for r in A.itertuples() for n in r.names for x in sset(n['body'])] + [(r.site, x) for r in A.itertuples() for x in sorted(short_signs(r.shorts))]
rate = np.mean([x in CREST for _, x in pool])
null = []
for _ in range(NS):
    c = 0
    for st, x in tails:
        c += any(rng.choice([p[1] for p in pool if p[0] == st]) in CREST for _ in x)
    null.append(c)
say(f'1d short tails that are a CREST-class sign (any fish type): {k} of {len(tails)} stamps; chance {np.mean(null):.2f}; P_ge {pvals(k, null)["p_ge"]:.4f}  (draw: one sign from the pool of lump signs at the same site; pool rate of crest-class signs {rate:.3f})')

say('\n=== ITEM 2: short stamp vs heading (field) of name stamp ===')
has_sh = lambda sh: len(short_signs(sh) | short_front(sh)) > 0
test('2a short stamp front word or tail shares a sign with the name stamp field (slot signs left out)', has_sh, lambda nm: len(name_field(nm)) > 0,
     lambda n, s: len((short_signs(s) | short_front(s)) & name_field(n)) > 0)
test('2b same front word on both stamps', lambda sh: len(short_front(sh)) > 0, lambda nm: len(name_field(nm) & OPEN) > 0 or any(sset(x['front']) for x in nm),
     lambda n, s: len(short_front(s) & (name_field(n) | {y for x in n for y in sset(x['front']) if y in OPEN})) > 0)

say('\n=== ITEM 3: recurrence ===')
rows = [(r.site, r.label, [x['text'] for x in r.names], [x['text'] for x in r.shorts]) for r in E.itertuples()]
def recur(rows):
    nm = collections.defaultdict(set); nl = collections.Counter(); sm = collections.defaultdict(set); sl = collections.Counter()
    for _, _, ns, ss in rows:
        for n in ns:
            nl[n] += 1
            for s in ss: nm[n].add(s)
        for s in ss:
            sl[s] += 1
            for n in ns: sm[s].add(n)
    names2 = [n for n in nl if nl[n] >= 2]
    shorts2 = [s for s in sl if sl[s] >= 2]
    return (len(names2), sum(len(nm[n]) >= 2 for n in names2), len(shorts2), sum(len(sm[s]) >= 2 for s in shorts2),
            len({(n, s) for _, _, ns, ss in rows for n in ns for s in ss}), len(rows))
o = recur(rows)
say(f'name stamps on 2+ eligible lumps: {o[0]}; of them with 2+ different short stamps: {o[1]}')
say(f'short stamps on 2+ eligible lumps: {o[2]}; of them with 2+ different name stamps: {o[3]}')
say(f'distinct (name, short) pairs: {o[4]} on {o[5]} lumps')
sites = [r[0] for r in rows]; shl = [r[3] for r in rows]
nulls = collections.defaultdict(list)
for _ in range(NS):
    sh = deal(shl, sites, rng)
    rr = [(a[0], a[1], a[2], b) for a, b in zip(rows, sh)]
    q = recur(rr)
    nulls['names_diff'].append(q[1]); nulls['shorts_diff'].append(q[3]); nulls['pairs'].append(q[4]); nulls['names2'].append(q[0]); nulls['shorts2'].append(q[2])
for key, ob in (('names2', o[0]), ('names_diff', o[1]), ('shorts2', o[2]), ('shorts_diff', o[3]), ('pairs', o[4])):
    p = pvals(ob, nulls[key]); say(f'  {key}: real {ob}; chance {p["chance"]:.2f}; P_ge {p["p_ge"]:.4f}; P_le {p["p_le"]:.4f}')
say('  tables:')
bysh = collections.defaultdict(list)
for s_, l, ns, ss in rows:
    for s in ss: bysh[s].append((l, ns))
for s, v in sorted(bysh.items(), key=lambda kv: -len(kv[1])):
    if len(v) >= 2: say('   short', s, 'on', len(v), 'lumps with names', [(l, ns) for l, ns in v])
byn = collections.defaultdict(list)
for s_, l, ns, ss in rows:
    for n in ns: byn[n].append((l, ss))
for n, v in sorted(byn.items(), key=lambda kv: -len(kv[1])):
    if len(v) >= 2: say('   name', n, 'on', len(v), 'lumps with shorts', [(l, ss) for l, ss in v])

say('\n=== ITEM 4: order, mixing, picture field, find-spot ===')
# 4a order: lumps with exactly one name and one short (distinct texts)
one = [r for r in E.itertuples() if len(r.names) == 1 and len(r.shorts) == 1]
nf = sum(r.names[0]['imp'] < r.shorts[0]['imp'] for r in one)
null = rng.binomial(len(one), 0.5, NS)
p = pvals(nf, null)
say(f'4a lumps with one name and one short stamp: {len(one)}; name impression listed first {nf}; chance {len(one)/2:.1f}; P_ge {p["p_ge"]:.4f}; P_le {p["p_le"]:.4f} (order = catalogue impression order, not known to be stamping order)')
for cat in ('Lipi', 'Mah'):
    o2 = [r for r in one if r.cat == cat]
    say(f'   {cat}: {len(o2)} lumps, name first {sum(r.names[0]["imp"] < r.shorts[0]["imp"] for r in o2)}')
# 4b role mixing among all stratum A lumps
J = I[I.stratum == 'A'].copy()
def mixcount(roles, groups):
    return sum(('name' in set(roles[ix])) and ('short' in set(roles[ix])) for ix in groups)
J = J.reset_index(drop=True); roles = J.role.values.copy()
lump_ix = [np.where(J.lump.values == l)[0] for l in J.lump.unique()]
lump_site = J.groupby('lump', sort=False).site.first().values
obs = mixcount(roles, lump_ix)
null = []
site_ix = {s: np.where(J.site.values == s)[0] for s in np.unique(J.site.values)}
for _ in range(NS):
    r2 = roles.copy()
    for s, ix in site_ix.items(): r2[ix] = roles[rng.permutation(ix)]
    null.append(mixcount(r2, lump_ix))
p = pvals(obs, null)
say(f'4b lumps (A) carrying both a name stamp and a short stamp: {obs} of {len(lump_ix)}; chance {p["chance"]:.2f}; P_ge {p["p_ge"]:.4f}; P_le {p["p_le"]:.4f} (role labels dealt among impressions of the same site, lump sizes kept)')
# name+name and short+short
def pairs_same(roles, groups, role):
    return sum((roles[ix] == role).sum() >= 2 for ix in groups)
for role in ('name', 'short'):
    obs = pairs_same(roles, lump_ix, role); null = []
    for _ in range(NS // 4):
        r2 = roles.copy()
        for s, ix in site_ix.items(): r2[ix] = roles[rng.permutation(ix)]
        null.append(pairs_same(r2, lump_ix, role))
    p = pvals(obs, null); say(f'   lumps with 2+ {role} stamps: {obs}; chance {p["chance"]:.2f}; P_ge {p["p_ge"]:.4f}; P_le {p["p_le"]:.4f}')
# 4c picture field (second catalogue only: field symbol recorded for every impression)
M = J[J.cat == 'Mah'].reset_index(drop=True)
M = M[M.role.isin(['name', 'short'])].reset_index(drop=True)
has = (M.animal != '').values; rl = M.role.values
for role in ('name', 'short'):
    obs = int((has & (rl == role)).sum()); n = int((rl == role).sum())
    null = []
    for _ in range(NS):
        h2 = has.copy()
        for s in np.unique(M.site):
            ix = np.where(M.site.values == s)[0]; h2[ix] = has[rng.permutation(ix)]
        null.append((h2 & (rl == role)).sum())
    p = pvals(obs, null); say(f'4c second-catalogue {role} stamps with a picture field: {obs} of {n}; chance {p["chance"]:.2f}; P_ge {p["p_ge"]:.4f}; P_le {p["p_le"]:.4f}')
# 4d findspot: lumps sharing the same short (or name) text sit in the same spot more than chance (same catalogue and site)
def spot_pairs(L, key):
    d = collections.defaultdict(list)
    for r in L.itertuples():
        for s in getattr(r, key):
            if s['text'].count('000') < len(s['text'].split('-')) and r.spot: d[(r.cat, r.site, s['text'])].append(r.Index)
    return d
for key in ('shorts', 'names'):
    d = spot_pairs(A, key)
    groups = [v for v in d.values() if len(set(v)) >= 2]
    def cnt(spots):
        c = 0; n = 0
        for v in groups:
            v = sorted(set(v))
            for i in range(len(v)):
                for j in range(i + 1, len(v)):
                    n += 1; c += spots[v[i]] == spots[v[j]]
        return c, n
    spots = list(A.spot); obs, npairs = cnt(spots)
    # deal spots among lumps of the same catalogue and site
    cs = list(zip(A.cat, A.site)); null = []
    for _ in range(NS // 4):
        sp2 = deal(spots, cs, rng); null.append(cnt(sp2)[0])
    p = pvals(obs, null)
    say(f'4d lump pairs sharing the same {key[:-1]} stamp text and the same spot: {obs} of {npairs} pairs (spot named for both); chance {p["chance"]:.2f}; P_ge {p["p_ge"]:.4f}')
# 4e name ending class vs short front family
def end_class(nm):
    e = {x['ending'] for x in nm}
    if any('090' in x.split('-') for x in e): return 'jar+man'
    if any(x.startswith('740') for x in e): return 'jar'
    if any('520' in x.split('-') for x in e): return 'spear'
    return 'other'
def fam(sh):
    f = short_front(sh)
    return sorted(f)[0] if f else 'none'
ec = [end_class(n) for n in E.names]; fm = [fam(s) for s in E.shorts]
def chi(a, b):
    ta = collections.Counter(a); tb = collections.Counter(b); tab = collections.Counter(zip(a, b)); n = len(a)
    return sum((tab[(x, y)] - ta[x] * tb[y] / n) ** 2 / (ta[x] * tb[y] / n) for x in ta for y in tb)
obs = chi(ec, fm); null = [chi(ec, deal(fm, list(E.site), rng)) for _ in range(NS)]
p = pvals(obs, null)
say(f'4e name ending class vs short front word: chi-square {obs:.2f}; chance {p["chance"]:.2f}; P_ge {p["p_ge"]:.4f}  endings {collections.Counter(ec)} fronts {collections.Counter(fm)}')
