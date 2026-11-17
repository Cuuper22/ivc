#!/usr/bin/env python3
"""FRONT job 8: what does the front stand in place of?  2026-11-17.

front_7 found that names behind a front are about one sign SHORTER than frontless names (2.71 against 3.63 signs, seals),
so a fronted seal text is only about one sign longer in all though the front unit is two signs.  Idea (written before
these numbers): the front takes the place of the first part of the name, the crest / house element. A seal text is then
[house] [person] [closer] OR [front] [person] [closer]: the front is an institution standing where a house would stand.

Predictions:
 P1  the first sign of a fronted name is a crest-class sign (frame v2 CREST, fish and the other house emblems) LESS often
     than the first sign of a frontless name (seals, name + closer texts), beyond labels dealt within site and length.
 P2  fronted name n is found again as the TAIL of a longer frontless name (x + n) more often than as its HEAD (n + x),
     and more often than a frontless name of the same length is found as the tail of another frontless name.
 P3  the x in those (x + n) matches is a crest-class sign or a number + crest more often than chance.
"""
from front_common import *

say = make_logger('log_8_replace.txt')
rng = np.random.default_rng(8)
D = load(); F, *_ = front_set(D, say); D = add_parse(D, F)
S = copy_events(D[(D.kind == 'seal') & D.complete & (D.name.map(len) > 0) & D.has_closer]).copy()
S['hasf'] = S.front != ''
S['nlen'] = S.name.map(len)
CRESTISH = {s for s, c in V2.items() if c == 'CREST'}
S['c1'] = S.name.map(lambda n: V2.get(n[0], 'PERSONAL'))
say(f'seal name + closer texts: {len(S)}, fronted {int(S.hasf.sum())}')
say('class of the first name sign (share):')
say(pd.crosstab(S.c1, S.hasf, normalize='columns').round(3).rename(columns={False: 'no front', True: 'front'}).to_string())
say('name length (share):')
say(pd.crosstab(S.nlen.clip(upper=6), S.hasf, normalize='columns').round(3).rename(columns={False: 'no front', True: 'front'}).to_string())
# crest share by name length, fronted vs not
for L in (1, 2, 3, 4):
    a = S[(S.nlen == L) & S.hasf]; b = S[(S.nlen == L) & ~S.hasf]
    say(f'  name length {L}: crest-first fronted {(a.c1 == "CREST").mean():.3f} (n {len(a)}), frontless {(b.c1 == "CREST").mean():.3f} (n {len(b)})')
iscrest = (S.c1 == 'CREST').values.astype(float)
def st(lab): return iscrest[lab].mean() - iscrest[~lab].mean()
o = st(S.hasf.values)
grp = (S.site + '|' + S.nlen.astype(str)).values
null = [st(deal_within(S.hasf.values, grp, rng).astype(bool)) for _ in range(3000)]
say(f'P1 crest-first share, fronted minus frontless: {o:+.3f}; dealt within site and name length {np.mean(null):+.3f}; '
    f'P low {pval_lo(null, o):.4f}, P high {pval_hi(null, o):.4f}')
# numbers first in the name
isnum = S.name.map(lambda n: n[0] in NUMS).values.astype(float)
o2 = isnum[S.hasf.values].mean() - isnum[~S.hasf.values].mean()
null2 = [isnum[l].mean() - isnum[~l].mean() for l in (deal_within(S.hasf.values, grp, rng).astype(bool) for _ in range(3000))]
say(f'number-first share, fronted {isnum[S.hasf.values].mean():.3f} against frontless {isnum[~S.hasf.values].mean():.3f}; '
    f'difference {o2:+.3f}, dealt {np.mean(null2):+.3f}, P high {pval_hi(null2, o2):.4f}, P low {pval_lo(null2, o2):.4f}')

# ---------- P2 head / tail matching, all objects' frontless names as the reference pool
ALL = copy_events(D[D.complete & (D.name.map(len) > 0) & D.has_closer])
FL = set(ALL[ALL.front == ''].namestr)
FLt = [tuple(n.split('-')) for n in FL]
tails = collections.defaultdict(set); heads = collections.defaultdict(set)
for n in FLt:
    if len(n) >= 2:
        tails[n[1:]].add(n[0]); heads[n[:-1]].add(n[-1])
fn = set(tuple(n) for n in S[S.hasf].name)
fl_seal = set(tuple(n) for n in S[~S.hasf].name)
def rate(names):
    names = list(names)
    t = np.mean([len(tails.get(n, set()) - set()) > 0 for n in names]); h = np.mean([len(heads.get(n, set())) > 0 for n in names])
    return t, h
tf, hf = rate(fn)
# control: frontless seal names, excluding self-match (a name x+n where x+n is the name itself cannot happen since lengths differ)
tc, hc = rate(fl_seal)
# matched by length
def rate_len(names, L):
    nm = [n for n in names if len(n) == L]
    return (np.mean([len(tails.get(n, set())) > 0 for n in nm]) if nm else np.nan,
            np.mean([len(heads.get(n, set())) > 0 for n in nm]) if nm else np.nan, len(nm))
say(f'\nP2 distinct fronted seal names {len(fn)}: found as the TAIL of a longer frontless name {tf:.3f}, as the HEAD {hf:.3f}')
say(f'   distinct frontless seal names {len(fl_seal)}: as tail {tc:.3f}, as head {hc:.3f}')
rows = []
for L in (1, 2, 3, 4):
    a = rate_len(fn, L); b = rate_len(fl_seal, L)
    rows.append(dict(name_len=L, fronted_n=a[2], fronted_tail=round(a[0], 3), fronted_head=round(a[1], 3),
                     frontless_n=b[2], frontless_tail=round(b[0], 3), frontless_head=round(b[1], 3)))
HT = pd.DataFrame(rows); HT.to_csv(f'{OUTF}/f8_head_tail.csv', index=False); say(HT.to_string(index=False))
# P3: what the extra first sign x is
xs = collections.Counter()
for n in fn:
    for x in tails.get(n, ()): xs[x] += 1
cls = collections.Counter(V2.get(x, 'PERSONAL') for x in xs.elements())
xs_c = collections.Counter()
for n in fl_seal:
    for x in tails.get(n, ()): xs_c[x] += 1
cls_c = collections.Counter(V2.get(x, 'PERSONAL') for x in xs_c.elements())
say(f'\nP3 the extra first sign x where frontless x + n matches a fronted name n: {sum(xs.values())} matches; classes {dict(cls)}; '
    f'top {xs.most_common(12)}')
say(f'   same for frontless names as n: {sum(xs_c.values())} matches; classes {dict(cls_c)}; top {xs_c.most_common(12)}')
ex = [(n, sorted(tails[n])) for n in fn if n in tails][:30]
say('examples (fronted name n : signs x seen before it in frontless names): ' + '; '.join(f'{"-".join(n)}: {x}' for n, x in ex))
