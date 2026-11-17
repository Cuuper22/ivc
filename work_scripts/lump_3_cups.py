#!/usr/bin/env python3
"""LUMPS step 3: stratum B, objects that carry a name-type impression and a cup-count impression (cup sign 700 with a count).
Predictions written before the numbers:
 B1 the same cup-count stamp (e.g. 033-700) goes with many different names; a name keeps different counts (free pairing).
 B2 the count goes with the name's ending (comb 400 after the jar vs jar alone), as the Harappa cup tablets suggest.
 B3 the count follows the findspot (same trench, same count) more than chance.
 B4 the name impression is listed first.
Data 1: Lipi moulded and incised clay tablets (TAB:B, TAB:I) with exactly 2 faces, one name face and one cup-count face; these
  are the same kind of object that the second catalogue files as sealings at Harappa.  Identical batches (same site, trench,
  and pair of texts) count once.  Chance: counts (or trenches) dealt among objects of the same site and tablet type, 20,000 deals.
Data 2: the same test on the second-catalogue lumps of stratum B (lump_common), spot = locus.
Output: work_data/lumps/log_3.txt
"""
import sys, os, collections
sys.path.insert(0, '/home/claude/ivc/work_scripts')
from lump_common import *
from front_common import load, front_set, parse, CLOSERS
rng = np.random.default_rng(3030); NS = 20000
fh = open(f'{OUT}/log_3.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); fh.write(s + '\n')
D = load(); F, _, _, _ = front_set(D, say=lambda *a: None)
D = D[D.type.isin(['TAB:B', 'TAB:I'])].copy()
D['fn'] = D.face.str.split('.').str[1].astype(int)
rows = []
for st, g in D.groupby('stone'):
    g = g.sort_values('fn')
    if len(g) != 2: continue
    cups = [r for r in g.itertuples() if '700' in r.tok and len(r.tok) <= 3]
    names = [r for r in g.itertuples() if any(x in CLOSERS for x in r.tok) and '700' not in r.tok]
    if len(cups) != 1 or len(names) != 1: continue
    c, n = cups[0], names[0]
    count = [x for x in c.tok if x != '700']
    nm = parse(n.tok, F)
    rows.append(dict(stone=st, site=n.site, type=n.type, area=n.area, text_name=n.signs, cup=c.signs, count='-'.join(count),
                     name_first=n.fn < c.fn, ending='-'.join(nm['ending']), end_comb=('400' in nm['ending']), end_man=('090' in nm['ending']),
                     crest_cls=any(x in {'140','220','222','226','231','233','235','240','243','803','806'} for x in nm['name']),
                     front=nm['front'], bodykey='-'.join(nm['name']), lost=('000' in n.tok) or ('000' in c.tok)))
B = pd.DataFrame(rows)
say('Lipi two-face clay tablets with one name face and one cup-count face:', len(B), 'by site', B.site.value_counts().to_dict(), 'by type', B.type.value_counts().to_dict())
B['batch'] = B.site + '|' + B.area + '|' + B.text_name + '|' + B.cup
B = B.drop_duplicates('batch').reset_index(drop=True)
say('after counting identical batches once (same site, trench, both texts):', len(B))
B = B[(~B.lost) & B['count'].isin(['031', '032', '033', '034', '035', '036'])].reset_index(drop=True)
say('with no lost sign and a tall-stroke count 031-036:', len(B), 'counts', B['count'].value_counts().sort_index().to_dict())
grp = list(B.site + '|' + B.type)

def chi(a, b):
    ta = collections.Counter(a); tb = collections.Counter(b); tab = collections.Counter(zip(a, b)); n = len(a)
    return sum((tab[(x, y)] - ta[x] * tb[y] / n) ** 2 / (ta[x] * tb[y] / n) for x in ta for y in tb)
def run(title, a, b, groups, ns=NS):
    obs = chi(a, b); null = [chi(a, deal(b, groups, rng)) for _ in range(ns)]
    p = pvals(obs, null); say(f'{title}: chi-square {obs:.2f}; chance {p["chance"]:.2f}; P_ge {p["p_ge"]:.4f}')
    return p
def block(B, groups, spotcol, label):
    say(f'\n--- {label}: {len(B)} objects ---')
    cnt = list(B['count'])
    # item 3
    names = list(B.bodykey)
    nm = collections.defaultdict(set); nl = collections.Counter()
    for n, c in zip(names, cnt): nm[n].add(c); nl[n] += 1
    n2 = [n for n in nl if nl[n] >= 2]; real_names_diff = sum(len(nm[n]) >= 2 for n in n2)
    def namesdiff(cc):
        m = collections.defaultdict(set)
        for n, c in zip(names, cc): m[n].add(c)
        return sum(len(m[n]) >= 2 for n in n2)
    null = [namesdiff(deal(cnt, groups, rng)) for _ in range(NS)]
    p = pvals(real_names_diff, null)
    say(f'B1 names (signs before the ending) on 2+ objects: {len(n2)}; with 2+ different counts: {real_names_diff}; chance {p["chance"]:.2f}; P_ge {p["p_ge"]:.4f}; P_le {p["p_le"]:.4f}')
    say(f'   counts: {dict(collections.Counter(cnt))}; distinct names {len(nl)} on {len(B)} objects; the most-used count stamp goes with {max(collections.Counter(cnt).values())} objects and {len({n for n, c in zip(names, cnt) if c == collections.Counter(cnt).most_common(1)[0][0]})} different names')
    # B2
    ec = ['comb' if e else 'no comb' for e in B.end_comb]
    run('B2a count vs name ends in comb 400', cnt, ec, groups)
    run('B2b count vs fish-class crest sign in name', cnt, ['crest' if x else 'none' for x in B.crest_cls], groups)
    run('B2c count vs front word on the name', cnt, [f or 'none' for f in B.front], groups)
    run('B2d count vs name ends in man 090', cnt, ['man' if x else 'no' for x in B.end_man], groups)
    # B3 spot
    sp = list(B[spotcol])
    ok = [i for i, s in enumerate(sp) if s]
    def same(cc):
        by = collections.defaultdict(list)
        for i in ok: by[(groups[i], sp[i])].append(cc[i])
        return sum(sum(v[a] == v[b] for a in range(len(v)) for b in range(a + 1, len(v))) for v in by.values())
    _g = collections.Counter((groups[i], sp[i]) for i in ok); pairs = sum(v * (v - 1) // 2 for v in _g.values())
    obs = same(cnt); null = [same(deal(cnt, groups, rng)) for _ in range(NS)]
    p = pvals(obs, null)
    say(f'B3 pairs of objects in the same {spotcol} with the same count: {obs} of {pairs} same-spot pairs; chance {p["chance"]:.2f}; P_ge {p["p_ge"]:.4f}')
block(B, grp, 'area', 'Lipi clay tablets')
# B4 order
nf = int(B.name_first.sum()); null = rng.binomial(len(B), 0.5, NS); p = pvals(nf, null)
say(f'B4 name face is the first-listed face: {nf} of {len(B)}; chance {len(B)/2:.1f}; P_ge {p["p_ge"]:.4f}  (catalogue face order)')

# second-catalogue replicate
I, steps = load_lumps(); T = lump_table(I)
Tb = T[T.stratum == 'B']
rows = []
for r in Tb.itertuples():
    cups = [c for c in r.cups if c['text'].split('-')[0] in ('031', '032', '033', '034', '035', '036') or c['text'].split('-')[-1] in ('031','032','033','034','035','036')]
    if len(r.names) < 1 or len(cups) != 1: continue
    n = r.names[0]
    cnt = [x for x in cups[0]['text'].split('-') if x in ('031', '032', '033', '034', '035', '036')]
    if len(cnt) != 1 or '000' in n['text'].split('-'): continue
    rows.append(dict(lump=r.label, site=r.site, type='Mah', locus=r.spot, count=cnt[0], bodykey=n['name'], end_comb='400' in n['ending'].split('-'),
                     end_man='090' in n['ending'].split('-'), crest_cls=bool(n['crest_cls']), front=n['front'], name_first=n['imp'] < cups[0]['imp']))
M = pd.DataFrame(rows)
say('\nSecond catalogue, stratum B lumps with one readable name and one cup-count face:', len(M), M.site.value_counts().to_dict())
if len(M):
    M = M.rename(columns={'locus': 'area'})
    block(M, list(M.site), 'area', 'Second catalogue lumps (Harappa mostly; 34 of these match Lipi tablets, so this is not an independent sample)')
    nf = int(M.name_first.sum()); p = pvals(nf, rng.binomial(len(M), 0.5, NS))
    say(f'B4 name impression first: {nf} of {len(M)}; chance {len(M)/2:.1f}; P_ge {p["p_ge"]:.4f}')
