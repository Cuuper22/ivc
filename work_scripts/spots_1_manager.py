#!/usr/bin/env python3
"""SPOTS, lead 1: the house manager ("X's man", the seal form [crest X] jar 740 man 090).

Plain words:
- MANAGER (agent) = a seal whose text ends jar + man (090); the name before the jar belongs to the MASTER X, and the
  master's CREST (first name sign) is the house key. OWNER OBJECT = any undamaged object with a name closed by an
  ending other than jar+man, whose crest is X (seals, tablets, tags, pots; as in registry_tests2.py).
- FINDSPOT levels: building (area + house at Mohenjo-daro, area + grid square elsewhere), block (Mohenjo-daro block
  number, Harappa grid row), area (the catalogue's excavation area = trench), mound (Harappa only: the letter group
  of the area, F / E / ET / AB / D ...).
- SHUFFLE: the manager's findspot is swapped for the findspot of a seal drawn at random from the same city
  (the design of registry_tests2.py (a)); P = share of shuffles at least as strong as the real count.
- STAND LETTER = catalogue letter after the colon on unicorn seals (W, J, S, I, L): the household mark.

PREDICTIONS (written before any number below was computed):
 (a) The Mohenjo-daro result (5 of 24 against 2.10) repeats at Harappa at building, block and area (trench) level, at
     Lothal, and in the pooled set; ratio above 1 and P below 0.1 in the pooled set at building level.
     Dholavira and Kalibangan hold almost no manager seals (0 and 0-1 in the registry): reported as "no test".
 (b) MAIN HOUSE: the manager's building holds more of the master's crest objects than a random building of the same
     city would hold (sum over managers of the master-crest objects in the manager's building above the shuffle),
     and in the cases where he sits with them, his building is the one holding most of that crest in the city.
 (c) Managers' seals are bigger than other seals inside every site that has 4+ managers (Mohenjo-daro, Harappa), and
     pooled by within-site shuffle of the manager label.
 (d) A manager's stand letter matches the master-crest seals in his building (and in his area) more often than stand
     letters match between random seals of the city; the animal species does the same but weaker (species is not a
     household mark, stand letter is).
Writes work_data/spots/s1_*.csv and s1_log.txt.  Run: python3 spots_1_manager.py   (about 1-2 min; prints progress)
"""
import os, re, collections, random, sys
import numpy as np, pandas as pd
from scipy.stats import mannwhitneyu
random.seed(101); np.random.seed(101)
ROOT = '/home/antigravity/Cuuper22/ivc'; OUT = f'{ROOT}/work_data/spots'; os.makedirs(OUT, exist_ok=True)
LOG = open(f'{OUT}/s1_log.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n')
NSH = 5000

R = f'{ROOT}/work_data/registry'
P = pd.read_csv(f'{R}/people.csv', dtype=str).fillna('')
A = pd.read_csv(f'{R}/names_all.csv', dtype=str).fillna('')
A = A[(A.damaged == 'False') & (A.goods_line == 'False')].copy()
say('[s1] loaded people.csv', len(P), 'and names_all.csv (undamaged, no goods lines)', len(A))

def mound(area):
    m = re.match(r'^(AB|ET|EC|EB|EA|E|F|D|G|H|J)', area)
    return m.group(1) if m else (area or '')
for T in (P, A):
    T['mound'] = ['' if not (s == 'Harappa' and a) else f'Harappa|{mound(a)}' for s, a in zip(T.city if 'city' in T else T.site, T.area)]
P['site'] = P.city
P['hmm_n'] = pd.to_numeric(P.hmm, errors='coerce'); P['vmm_n'] = pd.to_numeric(P.vmm, errors='coerce'); P['mm2'] = P.hmm_n * P.vmm_n
A['mm2'] = pd.to_numeric(A.hmm, errors='coerce') * pd.to_numeric(A.vmm, errors='coerce')
A['is_agent'] = A.ending.str.startswith("X's man")
P['is_agent'] = P.master != ''

own = A[~A.is_agent]
LEVELS = ['building', 'block', 'area_key', 'mound']
homes = {lev: collections.defaultdict(collections.Counter) for lev in LEVELS}
for lev in LEVELS:
    for k, z in zip(own.house_key, own[lev]):
        if z: homes[lev][k][z] += 1

def test_a(S_all, agents, lev, label, site_filter=None, nsh=NSH):
    """agents/S_all: DataFrames with house_key, city/site and the level column. Returns obs, n, null mean, P."""
    sub = agents[agents[lev] != '']
    if site_filter: sub = sub[sub.site.isin(site_filter)]
    pool = S_all[S_all[lev] != '']
    if site_filter: pool = pool[pool.site.isin(site_filter)]
    if len(sub) == 0: return (0, 0, np.nan, np.nan)
    bycity = collections.defaultdict(list)
    for b, c in zip(pool[lev], pool.site): bycity[c].append(b)
    keys = list(sub.house_key); cities = list(sub.site); locs = list(sub[lev])
    obs = sum(homes[lev].get(k, {}).get(b, 0) > 0 for k, b in zip(keys, locs))
    nl = np.zeros(nsh)
    for t in range(nsh):
        nl[t] = sum(homes[lev].get(k, {}).get(random.choice(bycity[c]), 0) > 0 for k, c in zip(keys, cities))
    return (obs, len(sub), nl.mean(), (1 + (nl >= obs).sum()) / (nsh + 1))

# ---------------- (a) site by site ----------------
say('\n(a) Is the manager found where an owner object of his master crest was found?  (managers = seals jar+man; own objects any kind)')
Pseal = P.copy()
Aseal = A[A.kind == 'seal'].drop_duplicates('object_id').copy(); Aseal['site'] = Aseal.site
rows = []
SITES = [('Mohenjo-daro', ['Mohenjo-daro']), ('Harappa', ['Harappa']), ('Kalibangan', ['Kalibangan']), ('Lothal', ['Lothal']),
         ('Dholavira', ['Dholavira']), ('pooled (all cities)', None)]
for name, sf in SITES:
    for lev in LEVELS:
        if lev == 'mound' and name not in ('Harappa',): continue
        if lev == 'block' and name in ('Lothal', 'Dholavira'): pass
        ag = P[P.is_agent]; ob, n, mu, p = test_a(P, ag, lev, name, sf)
        # members as control (seals that are not managers), leave the seal itself out
        mem = P[~P.is_agent & (P[lev] != '')]
        if sf: mem = mem[mem.site.isin(sf)]
        mo = sum((homes[lev].get(k, {}).get(b, 0) - 1) > 0 for k, b in zip(mem.house_key, mem[lev]))
        # same test on every manager object of any kind (tags, tablets), names_all based
        aa = A[A.is_agent].drop_duplicates('object_id')
        ob2, n2, mu2, p2 = test_a(A.drop_duplicates('object_id'), aa, lev, name, sf, nsh=2000)
        rows.append(dict(site=name, level=lev, managers_seals=n, hit=ob, shuffle_mean=round(mu, 2) if n else np.nan,
                         ratio=round(ob / mu, 2) if n and mu else np.nan, P=round(p, 4) if n else np.nan,
                         members_n=len(mem), members_hit=mo,
                         managers_allkinds=n2, allkinds_hit=ob2, allkinds_shuffle=round(mu2, 2) if n2 else np.nan, allkinds_P=round(p2, 4) if n2 else np.nan))
        say(f'  {name:20s} {lev:8s} seals: {ob} of {n} in a building/area with a master-crest owner object; shuffle {mu:.2f}'
            + (f' (ratio {ob / mu:.2f}, P {p:.4f})' if n and mu else ' (no test)')
            + f' | family members {mo} of {len(mem)} | managers of any object kind: {ob2} of {n2}, shuffle {mu2:.2f}, P {p2:.4f}' if n2 else
            f'  {name:20s} {lev:8s} seals: {ob} of {n}; no test | members {mo} of {len(mem)}')
pd.DataFrame(rows).to_csv(f'{OUT}/s1_a_sites.csv', index=False)

# Harappa/Kalibangan/Lothal/Dholavira manager counts, for the record
say('\n  managers available with a findspot (seals read whole/nearly whole): ' +
    '; '.join(f'{s} {int(((P.site == s) & P.is_agent).sum())} (with building {int(((P.site == s) & P.is_agent & (P.building != "")).sum())}, with area {int(((P.site == s) & P.is_agent & (P.area_key != "")).sum())})'
              for s in ('Mohenjo-daro', 'Harappa', 'Kalibangan', 'Lothal', 'Dholavira')))

# ---------------- (b) the main house ----------------
say('\n(b) MAIN HOUSE: does the manager sit in the building that holds MORE of the master crest than other buildings do?')
ag = P[P.is_agent & (P.building != '')]
rowsb = []
for lev in ('building', 'area_key'):
    ag = P[P.is_agent & (P[lev] != '')]
    pool = P[P[lev] != '']
    bycity = collections.defaultdict(list)
    for b, c in zip(pool[lev], pool.site): bycity[c].append(b)
    usable = [(r.cisi, r.site, r.house_key, r[lev]) for _, r in ag.iterrows()
              if any(z.split('|')[0] == r.site for z in homes[lev].get(r.house_key, {}))]
    obs = sum(homes[lev][k].get(b, 0) for _, c, k, b in usable)
    nl = np.zeros(NSH)
    for t in range(NSH):
        nl[t] = sum(homes[lev][k].get(random.choice(bycity[c]), 0) for _, c, k, b in usable)
    say(f'  level {lev:9s}: {len(usable)} managers whose master crest has owner objects in the same city: '
        f'master-crest objects in the manager\'s own {lev} total {obs}; shuffle {nl.mean():.2f} (ratio {obs / max(nl.mean(), 1e-9):.2f}, P {(1 + (nl >= obs).sum()) / (NSH + 1):.4f})')
    for cisi, c, k, b in usable:
        cnt = homes[lev][k]; sitecnt = {z: v for z, v in cnt.items() if z.split('|')[0] == c}
        rank = 1 + sum(v > cnt.get(b, 0) for v in sitecnt.values())
        rowsb.append(dict(level=lev, manager=cisi, city=c, master_crest=k, place=b, master_objects_there=cnt.get(b, 0),
                          crest_places_in_city=len(sitecnt), crest_objects_in_city=sum(sitecnt.values()),
                          max_objects_in_one_place=max(sitecnt.values()), rank_of_manager_place=rank if cnt.get(b, 0) else 0))
B = pd.DataFrame(rowsb); B.to_csv(f'{OUT}/s1_b_mainhouse.csv', index=False)
Bb = B[(B.level == 'building') & (B.master_objects_there > 0)]
say('  managers sitting with their master crest, and how that building ranks among all places holding the crest in the city:')
for _, r in Bb.iterrows():
    say(f'     {r.manager:9s} {r.place:34s} crest {r.master_crest}: {r.master_objects_there} of the crest\'s {r.crest_objects_in_city} objects in this city '
        f'sit here; the most any place holds {r.max_objects_in_one_place}; rank {r.rank_of_manager_place} of {r.crest_places_in_city} places')
# manager place vs the master's own seals: is the manager's building the crest's biggest holder? (all usable managers)
BB = B[B.level == 'building']
say(f'  all {len(BB)} usable managers: building is the single biggest holder of the crest in {int((BB.rank_of_manager_place == 1).sum())}; '
    f'holds any {int((BB.master_objects_there > 0).sum())}')
# benchmark: for ordinary owner seals of the same crest (not managers), how often is their building the crest's biggest holder?
def top_holder_rate(df, lev='building'):
    hit = n = 0
    for _, r in df.iterrows():
        cnt = {z: v for z, v in homes[lev].get(r.house_key, {}).items() if z.split('|')[0] == r.site}
        if not cnt or r[lev] not in cnt:
            if cnt: n += 1
            continue
        c2 = dict(cnt); c2[r[lev]] -= 1
        n += 1; hit += c2[r[lev]] >= max(c2.values()) and c2[r[lev]] > 0
    return hit, n
Pm = P[(~P.is_agent) & (P.building != '') & (P.site == 'Mohenjo-daro')]
say(f'  benchmark, ordinary owner seals at Mohenjo-daro: their building (leaving the seal itself out) is a top holder of their own crest in {top_holder_rate(Pm)[0]} of {top_holder_rate(Pm)[1]}')

# ---------------- (c) sizes inside each site ----------------
say('\n(c) Are managers\' seals bigger inside each site?  (face area mm2; all named undamaged seals, not only the whole-read ones)')
S = A[(A.kind == 'seal') & (A.mm2 > 0)].drop_duplicates('object_id').copy()
S['logA'] = np.log(S.mm2)
rowsc = []
for site, g in S.groupby('site'):
    a = g[g.is_agent]; o = g[~g.is_agent]
    if len(a) < 1: continue
    pu = mannwhitneyu(a.mm2, o.mm2, alternative='greater').pvalue if len(a) >= 2 else np.nan
    same = o[o.house_key.isin(set(a.house_key))]
    ps = mannwhitneyu(a.mm2, same.mm2, alternative='greater').pvalue if len(a) >= 2 and len(same) >= 2 else np.nan
    rowsc.append(dict(site=site, managers=len(a), mgr_median=a.mm2.median(), others=len(o), others_median=o.mm2.median(), P=pu,
                      same_crest_owners=len(same), same_crest_median=same.mm2.median() if len(same) else np.nan, P_same_crest=ps))
    if len(a) >= 2:
        say(f'  {site:15s} managers {len(a):3d} median {a.mm2.median():.0f} | all other seals {len(o):4d} median {o.mm2.median():.0f} (P {pu:.4f}) | owners of the same crests {len(same):3d} median {same.mm2.median() if len(same) else float("nan"):.0f} (P {ps:.4f})')
    else:
        say(f'  {site:15s} managers {len(a)} ({a.mm2.iloc[0]:.0f} mm2) | others median {o.mm2.median():.0f}')
pd.DataFrame(rowsc).to_csv(f'{OUT}/s1_c_sizes.csv', index=False)
# pooled: percentile of each manager inside its own site, labels shuffled inside each site
S['pct'] = S.groupby('site').mm2.rank(pct=True)
sites_ok = [s for s, g in S.groupby('site') if g.is_agent.sum() >= 1 and len(g) >= 10]
Sx = S[S.site.isin(sites_ok)]
obs = Sx[Sx.is_agent].pct.mean()
groups = [np.where(Sx.site.values == s)[0] for s in sites_ok]
lab = Sx.is_agent.values.copy(); pct = Sx.pct.values
nl = np.zeros(NSH)
for t in range(NSH):
    tot = 0; cnt = 0
    for ix in groups:
        l = lab[ix]; k = l.sum()
        if k: tot += pct[ix][np.random.permutation(len(ix))[:k]].sum(); cnt += k
    nl[t] = tot / cnt
say(f'  pooled over {len(sites_ok)} sites ({int(Sx.is_agent.sum())} managers): a manager\'s seal sits at the {obs * 100:.1f}th percentile of its own site\'s seal sizes on average; '
    f'label shuffle inside site gives {nl.mean() * 100:.1f} (P {(1 + (nl >= obs).sum()) / (NSH + 1):.4f})')
# same, but compared only with seals of the same shape class (hmm/vmm ratio close) is skipped; instead: against seals with the same ending jar only
Sj = S[S.ending.isin(['house of'])]
say(f'  managers {S[S.is_agent].mm2.median():.0f} mm2 vs plain "house of" owner seals {Sj.mm2.median():.0f} mm2 (all sites pooled); '
    f'MWU P {mannwhitneyu(S[S.is_agent].mm2, Sj.mm2, alternative="greater").pvalue:.5f}')

# ---------------- (d) animal and stand letter ----------------
say('\n(d) Household mark: does the manager share the stand letter / animal with the master crest\'s seals?')
Sd = A[A.kind == 'seal'].drop_duplicates('object_id').copy().reset_index(drop=True)
Sd['stand'] = Sd.stand.where(Sd.stand.isin(['W', 'J', 'S', 'I', 'L']), '')
BADANIM = {'', 'none', 'Misc', 'bull (unspecified)', 'other'}
Sd['sp'] = Sd.animal.where(~Sd.animal.isin(BADANIM), '')
def pair_stat(pairs, col, sites_arr):
    """pairs: list of (i, j). observed matches among pairs where both have a value; null: shuffle the column inside site."""
    vals = Sd[col].values
    ok = [(i, j) for i, j in pairs if vals[i] != '' and vals[j] != '']
    if not ok: return 0, 0, np.nan, np.nan
    obs = sum(vals[i] == vals[j] for i, j in ok)
    groups = [np.where(sites_arr == s)[0] for s in pd.unique(sites_arr)]
    nl = np.zeros(2000)
    for t in range(2000):
        v2 = vals.copy()
        for ix in groups:
            sub = ix[vals[ix] != '']
            v2[sub] = vals[sub][np.random.permutation(len(sub))]
        nl[t] = sum(v2[i] == v2[j] for i, j in ok)
    return obs, len(ok), nl.mean(), (1 + (nl >= obs).sum()) / 2001
sites_arr = Sd.site.values
rowsd = []
for lev in ('building', 'area_key', 'site'):
    pairs = []
    for i, r in Sd[Sd.is_agent].iterrows():
        if lev != 'site' and r[lev] == '': continue
        mates = Sd[(Sd.house_key == r.house_key) & (~Sd.is_agent) & (Sd.site == r.site)]
        if lev != 'site': mates = mates[mates[lev] == r[lev]]
        pairs += [(i, j) for j in mates.index]
    for col in ('stand', 'sp'):
        o, n, mu, p = pair_stat(pairs, col, sites_arr)
        what = 'stand letter' if col == 'stand' else 'animal species'
        say(f'  manager vs master-crest owner seals in the same {lev:9s}: {what:14s} match {o} of {n} pairs; shuffle {mu:.2f} (P {p:.4f})')
        rowsd.append(dict(partners=f'master-crest owner seals, same {lev}', mark=what, matches=o, pairs=n, shuffle=mu, P=p))
# manager vs ANY non-manager seal in the same building / area (the household as a whole)
for lev in ('building', 'area_key'):
    pairs = []
    for i, r in Sd[Sd.is_agent].iterrows():
        if r[lev] == '': continue
        mates = Sd[(~Sd.is_agent) & (Sd[lev] == r[lev])]
        pairs += [(i, j) for j in mates.index]
    for col in ('stand', 'sp'):
        o, n, mu, p = pair_stat(pairs, col, sites_arr)
        what = 'stand letter' if col == 'stand' else 'animal species'
        say(f'  manager vs ALL other seals in the same {lev:9s}: {what:14s} match {o} of {n} pairs; shuffle {mu:.2f} (P {p:.4f})')
        rowsd.append(dict(partners=f'all non-manager seals, same {lev}', mark=what, matches=o, pairs=n, shuffle=mu, P=p))
pd.DataFrame(rowsd).to_csv(f'{OUT}/s1_d_marks.csv', index=False)
say('\n  the managers that sit with master-crest owner seals, with their marks:')
for i, r in Sd[Sd.is_agent & (Sd.building != '')].iterrows():
    m = Sd[(Sd.house_key == r.house_key) & (~Sd.is_agent) & (Sd.building == r.building)]
    if len(m):
        say(f'     {r.cisi:9s} {r.building:32s} animal {r.animal:18s} stand {r.stand or "-"} | master seals: ' +
            '; '.join(f'{x.cisi} {x.animal}/{x.stand or "-"}' for _, x in m.iterrows()))
# stand letter shared by crest overall (to see if the household mark rides on the crest in general)
say('\n  manager stand letter vs master-crest owner seals anywhere in the same city (not only the same building):')
LOG.close()
