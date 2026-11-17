#!/usr/bin/env python3
"""PHRASES step 3: kinds of phrase by behaviour, each against its shuffle. Fixed 2026-11-17 before the run.

For each phrase, carriers = objects holding it (carriers.csv). Four flags, each with its own control. Controls draw random objects
(2,000 draws; seed 42) from the same pools; P = (draws at least as extreme + 1) / (draws + 1).
  HOUSE  (clustered in one building or block). Tests: REPEATS = carriers that share a building (or block, or area) with another carrier
         = k - distinct keys, summed over site x object-kind strata. Control: the same number of objects drawn at random from the same
         site and object kind with that key known (the shuffle within site). Flag: at least 8 carriers with building-or-block known,
         min(P_building, P_block) <= 0.005, and present in at least 2 of the 3 time bins (rule used only if 4+ carriers are dated).
  PLACE  (tied to one city or one mound). City tie: share of carriers in the top city vs the same share for random objects drawn with
         the same object-kind mix from the whole catalogue (sites known). Mound tie: Mohenjo-daro and Harappa carriers, top area share vs
         draws within the same site and kind. Flag: (top city share >= 0.8 and P_city <= 0.005) or (>= 8 carriers with area known at
         Mohenjo-daro/Harappa, top area share >= 0.6, P_area <= 0.005 against a draw within site and kind).
  GOODS  (sits on tags, pots, tablets; not seals). Non-seal share of carriers against the same share for random objects drawn at the
         same sites (the shuffle within site). Flag: at least 8 carriers, non-seal share >= 0.5, P <= 0.005.
  OFFICE (spread over many buildings and cities, holder different each time). Flag: at least 8 carriers, 4+ cities, P_building > 0.05 and
         P_block > 0.05 (not clustered) or fewer than 6 known, not PLACE, and holder variety >= 0.8: among distinct texts where something
         else stands beside the phrase (at least 8 such texts), distinct rest-of-text strings / such texts.
PRIMARY KIND: HOUSE if flagged; else the flagged ones of GOODS, PLACE joined (GOODS+PLACE); else OFFICE if flagged; else UNSORTED.
CLASSIFIER CONTROL: for every phrase, 10 random object sets of the same size and same kind mix from the whole catalogue go through the
  identical flags (300 draws each); report how often a random set gets each flag.
ADDED AFTER THE FIRST RUN (written before the second run; the first run's OFFICE flag was met by 76% of random sets; (iv) and (v) are computed from
  this script's table by phrases_3b_pooled.py: (iv) pooled excess of shared-building carriers over the null, summed over phrases,
  Z = sum(obs - mean) / sqrt(sum of null variances), by group, with and without copies; (v) PLACE and GOODS also on P alone (P <= 0.005, any share)):
  (i) classifier control also run on UNMATCHED random sets (same size, any objects); the kind-matched sets are circular for GOODS.
  (ii) SPREAD test for offices: P_spread = share of draws with AT MOST as many shared-building carriers as the phrase has (a phrase
       that avoids sharing a building more than chance = one holder per house). Flag SPREAD_WIDE if P_spread_building <= 0.05 with a null
       mean of at least 2 repeats (else the test has no power).
  (iii) HOUSE after removing copies: carriers with the identical full text in the same building count once; flag HOUSE_DEDUP needs the same
       rule (P <= 0.005, >= 8 carriers).
PREDICTIONS (before the run):
  H1 HOUSE flags: 3 to 15 of the top 100, mostly group 'name'. H2 OFFICE flags: the front phrases (920-060-741, 920-060, 692-060, 861-002)
  and several ending pairs; at least 10. H3 GOODS flags: count-line group and ending pairs on tablets (740-400 at Harappa); at least 8.
  H4 PLACE flags: at least 5. H5 random sets: each of HOUSE, PLACE, GOODS under 3% of sets; OFFICE high (it is the unclustered default).
Output: work_data/phrases/kinds.csv, kinds_control.csv, log_3.txt
"""
from phrases_common import *
LOG = open(f'{OUTP}/log_3.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n'); LOG.flush()
rng = np.random.default_rng(42)
DR, DC, NSET = 2000, 300, 10

O = build_objects(); O['area_n'] = O.area.map(lambda a: re.sub(r'\s*\(.*\)|\.', '', a).strip())
O = O[O.site != 'Unknown'].copy()
O['kg'] = O.kind.where(O.kind.isin(['seal', 'mtab', 'tag', 'pot', 'ctab']), 'other')
O['nonseal'] = (O.kind != 'seal').astype(int)
oid = O.index.values; pos = {o: i for i, o in enumerate(oid)}
site = O.site.values; kg = O.kg.values; nonseal = O.nonseal.values
LV = {}
for lvl, col in (('building', 'building'), ('block', 'block'), ('area', 'area_n')):
    s = O[col].where(O[col] != '', None)
    codes = pd.factorize(s)[0]; LV[lvl] = codes       # -1 = unknown
bins = O.bin.values
# pools
def pool(mask_fn):
    return mask_fn
site_kind_pool = {}
for lvl in LV:
    known = LV[lvl] >= 0
    for s_ in np.unique(site):
        for k_ in np.unique(kg):
            ix = np.where((site == s_) & (kg == k_) & known)[0]
            if len(ix): site_kind_pool[(lvl, s_, k_)] = ix
site_pool = {s_: np.where(site == s_)[0] for s_ in np.unique(site)}
kind_pool = {k_: np.where(kg == k_)[0] for k_ in np.unique(kg)}

def repeats_obs_null(S, lvl, D, rg):
    """S: indices (into O arrays). returns (observed repeats, null array, n_known)."""
    codes = LV[lvl]; strata = collections.defaultdict(list)
    for i in S:
        if codes[i] >= 0: strata[(site[i], kg[i])].append(codes[i])
    obs = sum(len(v) - len(set(v)) for v in strata.values()); nk = sum(len(v) for v in strata.values())
    null = np.zeros(D)
    for (s_, k_), v in strata.items():
        pl = site_kind_pool.get((lvl, s_, k_))
        if pl is None or len(pl) < len(v): continue
        c = codes[pl]
        for t in range(D):
            null[t] += len(v) - len(set(rg.choice(c, len(v), replace=False).tolist()))
    return obs, null, nk

def pval(obs, null): return (np.sum(null >= obs - 1e-9) + 1) / (len(null) + 1)

def top_share(vals):
    c = collections.Counter(vals); return max(c.values()) / len(vals), c.most_common(1)[0][0]

def classify(S, D, rg, rest_variety=None, full=True, S2=None):
    S = np.array(S); k = len(S); out = dict(n_obj=k)
    # time
    b = collections.Counter(x for x in bins[S] if x)
    out['bins'] = f"{b.get('early', 0)}/{b.get('middle', 0)}/{b.get('late', 0)}"; ndated = sum(b.values())
    nbins = sum(1 for v in b.values() if v > 0); out['n_bins'] = nbins
    # house
    ob, nb_, nkb = repeats_obs_null(S, 'building', D, rg); ok, nk_, nkk = repeats_obs_null(S, 'block', D, rg)
    out.update(n_bld_known=nkb, n_blk_known=nkk, rep_bld=ob, P_building=pval(ob, nb_) if nkb >= 4 else np.nan,
               rep_blk=ok, P_block=pval(ok, nk_) if nkk >= 4 else np.nan, null_rep_bld=float(nb_.mean()), null_rep_blk=float(nk_.mean()), null_sd_bld=float(nb_.std()), null_sd_blk=float(nk_.std()))
    pmin = np.nanmin([out['P_building'], out['P_block']]) if (nkb >= 4 or nkk >= 4) else np.nan
    out['P_house'] = pmin
    out['P_spread_building'] = (np.sum(nb_ <= ob + 1e-9) + 1) / (D + 1) if nkb >= 4 else np.nan
    out['spread_power'] = bool(nb_.mean() >= 2)
    out['HOUSE'] = bool(max(nkb, nkk) >= 8 and pmin == pmin and pmin <= 0.005 and (nbins >= 2 or ndated < 4))
    if S2 is not None:
        ob2, nb2, nk2 = repeats_obs_null(np.array(S2), 'building', D, rg); ok2, nk2_, nkk2 = repeats_obs_null(np.array(S2), 'block', D, rg)
        p2 = np.nanmin([pval(ob2, nb2) if nk2 >= 4 else np.nan, pval(ok2, nk2_) if nkk2 >= 4 else np.nan]) if (nk2 >= 4 or nkk2 >= 4) else np.nan
        out['n_dedup'] = len(S2); out['P_house_dedup'] = p2
        out.update(rep_bld_dd=ob2, null_bld_dd=float(nb2.mean()), null_sd_bld_dd=float(nb2.std()), rep_blk_dd=ok2, null_blk_dd=float(nk2_.mean()), null_sd_blk_dd=float(nk2_.std()), n_bld_known_dd=nk2, n_blk_known_dd=nkk2)
        out['HOUSE_DEDUP'] = bool(max(nk2, nkk2) >= 8 and p2 == p2 and p2 <= 0.005)
    # place
    sh, topc = top_share(site[S]); out['top_city'] = topc; out['top_city_share'] = round(sh, 3); out['n_cities'] = len(set(site[S]))
    cnt = collections.Counter(kg[S]); null = np.zeros(D)
    for t in range(D):
        sel = np.concatenate([rg.choice(kind_pool[k_], n_, replace=False) for k_, n_ in cnt.items()])
        null[t] = top_share(site[sel])[0]
    out['P_city'] = (np.sum(null >= sh - 1e-9) + 1) / (D + 1); out['null_city_share'] = float(null.mean())
    # mound
    SM = [i for i in S if site[i] in ('Mohenjo-daro', 'Harappa') and LV['area'][i] >= 0]
    out['n_area_known'] = len(SM); out['P_area'] = np.nan; out['top_area_share'] = np.nan; out['top_area'] = ''
    if len(SM) >= 4:
        ash, atop = top_share([(site[i], LV['area'][i]) for i in SM]); out['top_area_share'] = round(ash, 3)
        out['top_area'] = O.area_n.values[[i for i in SM if (site[i], LV['area'][i]) == atop][0]] + ' @ ' + atop[0]
        strata = collections.Counter((site[i], kg[i]) for i in SM); nl = np.zeros(D)
        for t in range(D):
            lab = []
            for (s_, k_), n_ in strata.items():
                pl = site_kind_pool.get(('area', s_, k_))
                if pl is None or len(pl) < n_: pl = site_kind_pool[('area', s_, k_)] if ('area', s_, k_) in site_kind_pool else None
                if pl is None: continue
                lab += [(s_, c) for c in rg.choice(LV['area'][pl], min(n_, len(pl)), replace=False)]
            nl[t] = top_share(lab)[0] if lab else 0
        out['P_area'] = (np.sum(nl >= ash - 1e-9) + 1) / (D + 1)
    out['PLACE'] = bool((sh >= 0.8 and out['P_city'] <= 0.005) or (len(SM) >= 8 and out['top_area_share'] >= 0.6 and out['P_area'] <= 0.005))
    out['PLACE_city'] = bool(sh >= 0.8 and out['P_city'] <= 0.005); out['PLACE_mound'] = bool(out['PLACE'] and not out['PLACE_city'])
    # goods
    ns = nonseal[S].sum(); strata = collections.Counter(site[S]); null = np.zeros(D)
    for t in range(D):
        null[t] = sum(nonseal[rg.choice(site_pool[s_], n_, replace=False)].sum() for s_, n_ in strata.items())
    out['nonseal_share'] = round(ns / k, 3); out['P_goods'] = (np.sum(null >= ns - 1e-9) + 1) / (D + 1); out['null_nonseal_share'] = float(null.mean() / k)
    out['GOODS'] = bool(k >= 8 and ns / k >= 0.5 and out['P_goods'] <= 0.005)
    # office
    if full:
        out['holder_variety'] = rest_variety if rest_variety is not None else np.nan
    return out

# ---- holder variety from distinct texts
P = pd.read_csv(f'{OUTP}/phrase_list.csv', dtype={'phrase': str}).fillna({'nested_in': ''})
Tt = distinct_texts()
def rest_of(x, p):
    k = len(p); rs = []
    for (i, st, en) in positions(x, p): rs.append(tuple(x[:i]) + ('|',) + tuple(x[i + k:]))
    return rs
CAR = pd.read_csv(f'{OUTP}/carriers.csv', dtype={'phrase': str}); cmap = CAR.groupby('phrase')['obj'].apply(list).to_dict()
TXT = d.groupby('obj').tok.first(); TXT.index = TXT.index.astype(str)
rows = []; ctl_rows = []
for r in P.itertuples():
    p = tuple(r.phrase.split('-'))
    rests = collections.Counter(); nonempty = 0
    for x in Tt:
        rr = rest_of(x, p)
        if rr:
            rest = rr[0]
            if len(rest) > 1 and not (rest[0] == '|' and len(rest) == 1) and (rest != ('|',)): nonempty += 1; rests[rest] += 1
    hv = len(rests) / nonempty if nonempty >= 8 else np.nan
    S = [pos[str(o)] for o in cmap[r.phrase] if str(o) in pos]
    seen_tb = set(); S2 = []
    for i in S:
        key = (TXT[oid[i]], O.building.values[i])
        if O.building.values[i] == '' or key not in seen_tb: S2.append(i); seen_tb.add(key)
    c = classify(S, DR, rng, rest_variety=hv, S2=S2)
    c['rest_texts'] = nonempty; c['holder_variety'] = hv
    unclustered = (not (c['P_building'] <= 0.05)) and (not (c['P_block'] <= 0.05))
    c['OFFICE'] = bool(len(S) >= 8 and c['n_cities'] >= 4 and unclustered and not c['PLACE'] and hv == hv and hv >= 0.8)
    flags = [f for f in ('GOODS', 'PLACE') if c[f]]
    c['primary'] = 'HOUSE' if c['HOUSE'] else ('+'.join(flags) if flags else ('OFFICE' if c['OFFICE'] else 'UNSORTED'))
    c.update(phrase=r.phrase, group=r.group, nested_in=r.nested_in, n_texts=r.n_texts)
    rows.append(c)
    # control sets
    kmix = collections.Counter(O.loc[[oid[i] for i in S], 'kg'])
    for j in range(NSET):
        sel = np.concatenate([rng.choice(kind_pool[k_], n_, replace=False) for k_, n_ in kmix.items()])
        cc = classify(sel, DC, rng, rest_variety=hv)
        unc = (not (cc['P_building'] <= 0.05)) and (not (cc['P_block'] <= 0.05))
        cc['OFFICE'] = bool(len(sel) >= 8 and cc['n_cities'] >= 4 and unc and not cc['PLACE'] and hv == hv and hv >= 0.8)
        ctl_rows.append(dict(phrase=r.phrase, set=j, matched='kind-matched', **{f: cc[f] for f in ('HOUSE', 'PLACE', 'GOODS', 'OFFICE')}))
        sel = rng.choice(len(oid), len(S), replace=False)
        cc = classify(sel, DC, rng, rest_variety=hv)
        unc = (not (cc['P_building'] <= 0.05)) and (not (cc['P_block'] <= 0.05))
        cc['OFFICE'] = bool(len(sel) >= 8 and cc['n_cities'] >= 4 and unc and not cc['PLACE'] and hv == hv and hv >= 0.8)
        ctl_rows.append(dict(phrase=r.phrase, set=j, matched='unmatched', **{f: cc[f] for f in ('HOUSE', 'PLACE', 'GOODS', 'OFFICE')}))
    log(f'{r.phrase:16s} {c["primary"]:12s} n={len(S):4d} P_house={c["P_house"]:.3f} P_city={c["P_city"]:.4f} P_goods={c["P_goods"]:.4f}')
K = pd.DataFrame(rows); K.to_csv(f'{OUTP}/kinds_all.csv', index=False)
Kc = pd.DataFrame(ctl_rows); Kc.to_csv(f'{OUTP}/kinds_control.csv', index=False)
A = pd.read_csv(f'{OUTP}/atlas.csv', dtype={'phrase': str})
top100 = K[K.phrase.isin(A.phrase)].copy(); top100['rank'] = top100.phrase.map(dict(zip(A.phrase, A['rank']))); top100 = top100.sort_values('rank')
top100.to_csv(f'{OUTP}/kinds.csv', index=False)
say('TOP 100 primary kinds', top100.primary.value_counts().to_dict())
say('flags (top 100):', {f: int(top100[f].sum()) for f in ('HOUSE', 'PLACE', 'GOODS', 'OFFICE')})
for mt in ('kind-matched', 'unmatched'):
    say('random sets', mt, 'flag rates on the top-100 phrases:', {f: round(Kc[(Kc.phrase.isin(A.phrase)) & (Kc.matched == mt)][f].mean(), 3) for f in ('HOUSE', 'PLACE', 'GOODS', 'OFFICE')})
say('HOUSE_DEDUP flags (top 100):', int(top100.HOUSE_DEDUP.sum()), top100[top100.HOUSE_DEDUP].phrase.tolist())
sw = top100[top100.spread_power & (top100.P_spread_building <= 0.05)]
say('SPREAD_WIDE (fewer shared buildings than chance, power ok):', len(sw), sw.phrase.tolist(), ' phrases with power:', int(top100.spread_power.sum()))
say(pd.crosstab(top100.group, top100.primary).to_string())
