#!/usr/bin/env python3
"""COPPER step 7 and 8: copper tablets at Mohenjo-daro against clay tablets at Harappa (same role, different material),
and the copper tablets in time.

Per city and object kind: objects, distinct complete texts, copies per text, share of objects with a count (a number
next to a counted thing or measure, or the cup), share with a jar name, distinct jar names, and how many of those names
also stand before a jar on a SEAL of the same city (with the seal's ending and size residual: log face area minus the
median for seals of the same city, length and format; 0 = typical, -0.69 = half size).
Control for the seal match: distinct jar names of length-matched random seal faces of the same city, matched against
the OTHER seals of that city (how often any seal name recurs on another seal), 2,000 draws.
TIME: bins early / middle / late from work_data/time/time_axis.csv. Copper bins against all other dated objects of the
same site and excavation area (expected = for each area, the copper count there times the area's bin shares).

Predictions written 2026-11-17 before the numbers:
 P7.1 Copper: copies per text over 2.0, count on under 30% of objects, a jar name on over half; Harappa clay tablets:
      copies about 1.45, count on about half, jar name on about half.
 P7.2 Copper jar names stand on Mohenjo-daro seals at least as often as Harappa chit names stand on Harappa seals
      (28%), with plain jar endings and ordinary size (residual near 0), not the comb's half-size seals.
 P8.1 Copper tablets are spread over the middle and late bins like everything else; no bin holds more than 1.5 times
      its expected share.
Writes work_data/copper/harappa_compare.csv, names_on_seals.csv, time.csv, log_7.txt.
"""
import sys; sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from copper_common import *
with contextlib.redirect_stdout(io.StringIO()):
    import chits_common as CC
say = say_to(f'{OUT}/log_7.txt')
say('loading objects (chits loader)')
O = CC.load()
NR = CC.name_rows(O)
SZ = CC.seal_sizes()
say('loaded')

def counted_any(fs):
    for f in fs:
        R = runs(list(f))
        for a, b, v, ser in R:
            for k in (b, a - 1):
                if 0 <= k < len(f) and (job(f[k]) in ('THING', 'MEASURE') or f[k] == '700'): return True
    return False
rows = []
groups = [('Mohenjo-daro', 'ctab', 'copper tablets'), ('Harappa', 'mtab', 'clay tablets'), ('Mohenjo-daro', 'mtab', 'clay tablets')]
seal_names = {}
for site in ('Mohenjo-daro', 'Harappa'):
    sn = NR[(NR.site == site) & (NR.kind == 'seal') & ~NR.lost]
    seal_names[site] = sn
rng = np.random.default_rng(13)
match_rows = []
for site, kind, lab in groups:
    g = O[(O.site == site) & (O.kind == kind)]
    full = [fs for fs in g.faces if all('000' not in f for f in fs)]
    texts = collections.Counter(' | '.join(sorted('-'.join(f) for f in fs)) for fs in full)
    nr = NR[(NR.site == site) & (NR.kind == kind) & ~NR.lost]
    names = sorted(set(nr.name))
    sn = seal_names[site]
    on = [n for n in names if n in set(sn.name)]
    ss = sn[sn.name.isin(on)]
    endings = collections.Counter(ss.ending)
    res = [SZ.res.get(o) for o in ss.obj if o in SZ.index]
    res = [x for x in res if x is not None and not np.isnan(x)]
    # control: distinct seal names of the same lengths as these names, how often they recur on another seal of the city
    lens = [len(n.split('-')) for n in names]
    pool = collections.defaultdict(list)
    for o, n in zip(sn.obj, sn.name): pool[len(n.split('-'))].append((o, n))
    _d = collections.defaultdict(set)
    for o, n in zip(sn.obj, sn.name): _d[n].add(o)
    cnt_by_name = {n: len(v) for n, v in _d.items()}
    sims = []
    for _ in range(2000):
        hit = 0
        for k in lens:
            c = pool.get(k) or pool[min(pool, key=lambda x: abs(x - k))]
            o, n = c[rng.integers(len(c))]
            hit += cnt_by_name[n] >= 2
        sims.append(hit / max(len(lens), 1))
    rows.append(dict(group=f'{site} {lab}', objects=len(g), complete_objects=len(full), distinct_texts=len(texts),
                     copies_per_text=round(len(full) / max(len(texts), 1), 2),
                     with_count=round(np.mean([counted_any(fs) for fs in g.faces]), 3),
                     with_jar_name=round(g.obj.isin(set(NR[NR.kind == kind].obj)).mean(), 3),
                     distinct_jar_names=len(names), names_on_city_seals=len(on), share_on_seals=round(len(on) / max(len(names), 1), 3),
                     seal_random_recur=round(float(np.mean(sims)), 3), seals_with_those_names=len(ss),
                     seal_endings=dict(endings), seal_size_residual_median=round(float(np.median(res)), 3) if res else None,
                     n_sizes=len(res)))
    for n in on:
        x = sn[sn.name == n]
        match_rows.append(dict(group=f'{site} {lab}', name=n, n_tablets=int((nr.name == n).sum()), n_seals=len(x),
                               seal_endings=dict(collections.Counter(x.ending)), seal_cisi=' '.join(x.cisi)))
H = pd.DataFrame(rows); H.to_csv(f'{OUT}/harappa_compare.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_colwidth', 60)
say('\n' + H.T.to_string())
MR = pd.DataFrame(match_rows); MR.to_csv(f'{OUT}/names_on_seals.csv', index=False)
say('copper names found on Mohenjo-daro seals:\n' + MR[MR.group.str.contains('copper')].to_string(index=False))

# ---------------- time
T = pd.read_csv(f'{ROOT}/work_data/time/time_axis.csv', dtype=str).fillna('')
T = T[(T.site == 'Mohenjo-daro') & (T.bin != '')]
cop = T[T.kind == 'ctab']
exp = collections.Counter(); obs = collections.Counter(cop.bin)
for st, g in cop.groupby('stratum'):
    allst = T[T.stratum == st]; sh = allst.bin.value_counts(normalize=True)
    for b in ('early', 'middle', 'late'): exp[b] += len(g) * sh.get(b, 0)
# shuffle: copper label dealt among dated objects within stratum
sims = []
strata = {st: T[T.stratum == st].bin.values for st in set(cop.stratum)}
ncop = cop.stratum.value_counts()
for _ in range(10000):
    c = collections.Counter()
    for st, n in ncop.items(): c.update(rng.choice(strata[st], n, replace=False))
    sims.append([c[b] for b in ('early', 'middle', 'late')])
sims = np.array(sims)
TM = pd.DataFrame([dict(bin=b, copper=obs[b], expected=round(exp[b], 2), P_high=round(float(np.mean(sims[:, i] >= obs[b])), 4),
                        P_low=round(float(np.mean(sims[:, i] <= obs[b])), 4)) for i, b in enumerate(('early', 'middle', 'late'))])
TM.to_csv(f'{OUT}/time.csv', index=False)
say(f'dated copper tablets {len(cop)} of {(O.kind == "ctab").sum()}; by period string: {dict(collections.Counter(cop.time))}')
say('copper by bin against other dated objects of the same areas:\n' + TM.to_string(index=False))
L = pd.read_csv(f'{OUT}/objects.csv', dtype=str).fillna('')
by = L[L.bin != ''].groupby('set_text').bin.agg(lambda s: dict(collections.Counter(s)))
say('sets with dated copies: ' + '; '.join(f'{t} {b}' for t, b in by.items() if sum(b.values()) >= 2))

# ---------------- redesign after P7.2 went against (written after the first run): (a) whole copper TEXTS (not only the
# signs before a jar) found inside any Mohenjo-daro seal face; (b) new idea: copper jar names on seals of ANY city.
cop = O[(O.site == 'Mohenjo-daro') & (O.kind == 'ctab')]
ctexts = sorted({'-'.join(f) for fs in cop.faces for f in fs if '000' not in f and len(f) >= 3})
mseal = ['-'.join(f) for fs in O[(O.site == 'Mohenjo-daro') & (O.kind == 'seal')].faces for f in fs]
inside = [t for t in ctexts if any(t in s for s in mseal)]
say(f'redesign (a): copper text faces of 3+ signs found whole inside a Mohenjo-daro seal face: {len(inside)} of {len(ctexts)}: {inside}')
mtexts = sorted({'-'.join(f) for fs in O[(O.site == 'Mohenjo-daro') & (O.kind == 'mtab')].faces for f in fs if '000' not in f and len(f) >= 3})
inside2 = [t for t in mtexts if any(t in s for s in mseal)]
say(f'   control: Mohenjo-daro clay tablet faces of 3+ signs found whole inside a Mohenjo-daro seal face: {len(inside2)} of {len(mtexts)}')
allseal = set(NR[(NR.kind == 'seal') & ~NR.lost].name)
cn = sorted(set(NR[(NR.site == 'Mohenjo-daro') & (NR.kind == 'ctab') & ~NR.lost].name))
say(f'new idea (b): copper jar names on a seal of any city: {sum(n in allseal for n in cn)} of {len(cn)}')
