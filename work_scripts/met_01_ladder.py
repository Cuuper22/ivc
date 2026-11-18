#!/usr/bin/env python3
"""met_01_ladder.py — Step 1 & Step 2: Complete Numeral & Measure Inventory,
Proto-Cuneiform Numeral-System Split, and Exact Conversion Ladder (DAG + Ratios).

Outputs in work_data/met/:
  - numeral_inventory.csv
  - commodity_series.csv
  - unit_ladder.csv
  - ladder_order_pairs.csv
  - ladder_summary.json
  - log_01_ladder.txt
"""
import os
import sys
import json
import math
import collections
import itertools
import numpy as np
import pandas as pd
from scipy.stats import binomtest, fisher_exact, chi2_contingency
from sklearn.metrics import normalized_mutual_info_score

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from met_common import (
    ROOT, OUT_DIR, NUM_CATALOG, PURE_NUMS, CANDIDATE_UNITS, OPENER_SIGNS,
    load_corpora, parse_num_runs, fit_ownership_rates, extract_owned_counts
)

LOG_PATH = os.path.join(OUT_DIR, 'log_01_ladder.txt')
log_fh = open(LOG_PATH, 'w')

def say(*args):
    s = ' '.join(str(a) for a in args)
    print(s, flush=True)
    log_fh.write(s + '\n')
    log_fh.flush()

def pval_ge(null_arr, obs):
    null_arr = np.asarray(null_arr, dtype=float)
    return float((1 + np.sum(null_arr >= obs - 1e-12)) / (len(null_arr) + 1))

def pval_le(null_arr, obs):
    null_arr = np.asarray(null_arr, dtype=float)
    return float((1 + np.sum(null_arr <= obs + 1e-12)) / (len(null_arr) + 1))


def main():
    rng = np.random.default_rng(20261117)
    D = load_corpora()
    L_ev = D['L_events']
    Mn_ev = D['Mnew_clean_events']
    Mn_std_ev = D['Mnew_events']
    U_ev = pd.concat([L_ev, Mn_ev], ignore_index=True)

    say("=== STEP 1: CORPUS & DEDUPLICATION SUMMARY ===")
    say(f"Lipi: {len(D['raw_L'])} faces -> {len(D['L_stones'])} physical stones -> {len(L_ev)} deduplicated copy events")
    say(f"Mahadevan unseen (standard ~partnered): {len(Mn_std_ev)} copy events ({len(D['Mnew_objs'])} objects)")
    say(f"Mahadevan unseen (decontaminated of 9 split 121-121=056 twins): {len(Mn_ev)} copy events ({len(D['Mnew_clean_objs'])} objects)")
    say(f"Combined deduplicated corpus (Lipi + M_new_clean): {len(U_ev)} copy events")

    # Fit EM ownership strictly on Lipi deduplicated events (zero leakage from M_new!)
    after_rate, before_rate, occ_L = fit_ownership_rates(L_ev)
    oc_L = extract_owned_counts(L_ev, after_rate, before_rate)
    oc_Mn = extract_owned_counts(Mn_ev, after_rate, before_rate)
    oc_Mn_std = extract_owned_counts(Mn_std_ev, after_rate, before_rate)
    oc_U = pd.concat([oc_L, oc_Mn], ignore_index=True)

    # Also compare naive cross-series parser vs series-aware parser
    naive_merges_L = 0
    clean_compounds_L = 0
    non_inc_compounds_L = 0
    for r in L_ev.itertuples(index=False):
        for f in r.faces:
            rn = parse_num_runs(f, naive_cross_series=True)
            rc = parse_num_runs(f, naive_cross_series=False)
            for x in rn:
                if len(x['tokens']) >= 2 and len(x['series']) >= 2:
                    naive_merges_L += 1
            for x in rc:
                if len(x['tokens']) >= 2:
                    clean_compounds_L += 1
                    vs = [PURE_NUMS[t][1] for t in x['tokens']]
                    if all(vs[k] >= vs[k + 1] for k in range(len(vs) - 1)):
                        non_inc_compounds_L += 1
    say(f"\nNumeral boundary audit (Lipi events): {naive_merges_L} cross-series false merges eliminated;")
    say(f"Within-series additive compounds: {clean_compounds_L}, of which {non_inc_compounds_L}/{clean_compounds_L} "
        f"({100.0 * non_inc_compounds_L / max(1, clean_compounds_L):.1f}%) obey non-increasing order (v1 >= v2).")

    # ==========================================================================
    # 1A. FULL NUMERAL INVENTORY
    # ==========================================================================
    tok_raw_L = collections.Counter(s for t in D['raw_L']['tok'] for s in t)
    tok_raw_Mall = collections.Counter(s for t in D['raw_M']['tok'] for s in t)
    tok_ev_L = collections.Counter(s for r in L_ev.itertuples() for f in r.faces for s in f)
    tok_ev_Mn = collections.Counter(s for r in Mn_ev.itertuples() for f in r.faces for s in f)
    tok_ev_Mn_std = collections.Counter(s for r in Mn_std_ev.itertuples() for f in r.faces for s in f)

    role_counts = collections.defaultdict(collections.Counter)
    for r in U_ev.itertuples(index=False):
        for f in r.faces:
            for run in parse_num_runs(f):
                for t in run['tokens']:
                    role_counts[t][run['role']] += 1
            for t in f:
                if t in NUM_CATALOG and NUM_CATALOG[t][0] == 'J':
                    role_counts[t]['infixed_jar'] += 1

    owner_by_num = collections.defaultdict(collections.Counter)
    for r in oc_U.itertuples(index=False):
        for t in r.num_tokens.split():
            owner_by_num[t][f"{r.owner}({r.unit_group})"] += 1

    num_rows = []
    for tok, (ser, val, lab, desc) in NUM_CATALOG.items():
        rc = role_counts[tok]
        dom_role = rc.most_common(1)[0][0] if rc else 'unattested'
        top_own = '; '.join(f"{k}:{v}" for k, v in owner_by_num[tok].most_common(3))
        num_rows.append(dict(
            sign=tok, series=ser, value=val, code=lab,
            lipi_raw=tok_raw_L[tok], mah_all_raw=tok_raw_Mall[tok],
            lipi_events=tok_ev_L[tok], mnew_clean_events=tok_ev_Mn[tok],
            mnew_std_events=tok_ev_Mn_std[tok],
            total_dedup_events=tok_ev_L[tok] + tok_ev_Mn[tok],
            primary_role=dom_role,
            role_breakdown='; '.join(f"{k}:{v}" for k, v in rc.most_common()),
            top_counted_owners=top_own,
            description=desc
        ))
    df_num_inv = pd.DataFrame(num_rows)
    df_num_inv.to_csv(os.path.join(OUT_DIR, 'numeral_inventory.csv'), index=False)
    say(f"\nSaved numeral_inventory.csv ({len(df_num_inv)} numeral signs across 6 series S, F, T, B, A, J).")
    for ser in ('S', 'F', 'T', 'B', 'A', 'J'):
        sub = df_num_inv[df_num_inv['series'] == ser]
        say(f"  Series {ser}: {int((sub['total_dedup_events'] > 0).sum())}/{len(sub)} signs attested, "
            f"Lipi events={int(sub['lipi_events'].sum())}, M_new_clean events={int(sub['mnew_clean_events'].sum())}")

    # ==========================================================================
    # 1B. PROTO-CUNEIFORM NUMERAL-SYSTEM SPLIT TESTS
    # ==========================================================================
    say("\n=== STEP 2A: NUMERAL-SYSTEM SPLIT (COMMODITY -> SERIES SELECTION) ===")
    # Filter to candidate units/commodities with >= 5 owned counts in Lipi (excluding BARE and 'other')
    grp_counts_L = oc_L[oc_L['unit_group'] != 'other'].copy()
    valid_grps = {g for g, c in grp_counts_L['unit_group'].value_counts().items() if c >= 5 and g != 'bare'}
    sub_L = oc_L[oc_L['unit_group'].isin(valid_grps)].copy()
    sub_Mn = oc_Mn[oc_Mn['unit_group'].isin(valid_grps)].copy()

    def calc_nmi(df):
        if len(df) < 5:
            return 0.0
        return float(normalized_mutual_info_score(df['unit_group'], df['series']))

    nmi_L = calc_nmi(sub_L)
    ct_L = pd.crosstab(sub_L['unit_group'], sub_L['series'])
    chi2_L, p_chi2_L, dof_L, _ = chi2_contingency(ct_L)

    # Control 1: 1,000 global permutations of series labels
    null_global = [
        float(normalized_mutual_info_score(sub_L['unit_group'], rng.permutation(sub_L['series'].values)))
        for _ in range(1000)
    ]
    # Control 2 (STRONGEST RIVAL): 1,000 permutations stratified within (site, kind)
    # Tests rival hypothesis: "Tablets at Harappa use tall strokes, seals at Mohenjo-daro use short strokes"
    strata = (sub_L['site'] + '|' + sub_L['kind']).values
    idx_by_stratum = collections.defaultdict(list)
    for idx, st in enumerate(strata):
        idx_by_stratum[st].append(idx)
    ser_arr = sub_L['series'].values
    grp_arr = sub_L['unit_group'].values
    null_strat = []
    for _ in range(1000):
        perm_s = ser_arr.copy()
        for ii in idx_by_stratum.values():
            if len(ii) > 1:
                perm_s[ii] = rng.permutation(ser_arr[ii])
        null_strat.append(float(normalized_mutual_info_score(grp_arr, perm_s)))

    z_strat = (nmi_L - np.mean(null_strat)) / max(1e-9, np.std(null_strat))
    say(f"Lipi deduplicated events (n={len(sub_L)} across {len(valid_grps)} unit/commodity groups):")
    say(f"  Real NMI(Commodity ; Series) = {nmi_L:.4f} (chi2={chi2_L:.1f}, dof={dof_L}, analytic P={p_chi2_L:.2e})")
    say(f"  Global shuffle (1,000x): mean={np.mean(null_global):.4f}, max={np.max(null_global):.4f}, P={pval_ge(null_global, nmi_L):.4f}")
    say(f"  RIVAL TEST — Stratified within (site x object_kind) (1,000x): mean={np.mean(null_strat):.4f} +- {np.std(null_strat):.4f}, "
        f"max={np.max(null_strat):.4f}, z={z_strat:+.1f}, P={pval_ge(null_strat, nmi_L):.4f}")

    # Within Seals ONLY and within Tablets ONLY
    for kname, kset in [('Seals only', {'seal'}), ('Tablets only (mtab+ctab)', {'mtab', 'ctab'})]:
        sk = sub_L[sub_L['kind'].isin(kset)]
        obs_k = calc_nmi(sk)
        nk = [float(normalized_mutual_info_score(sk['unit_group'], rng.permutation(sk['series'].values))) for _ in range(1000)]
        zk = (obs_k - np.mean(nk)) / max(1e-9, np.std(nk))
        say(f"  {kname} (n={len(sk)}): real NMI={obs_k:.4f} vs shuffle {np.mean(nk):.4f} (max {np.max(nk):.4f}), z={zk:+.1f}, P={pval_ge(nk, obs_k):.4f}")

    # Out-of-sample validation on unseen Mahadevan new texts (M_new_clean)!
    # Predict each group's dominant series on Lipi, test exact series match accuracy on M_new_clean!
    dom_ser_L = sub_L.groupby('unit_group')['series'].agg(lambda s: s.value_counts().index[0]).to_dict()
    if len(sub_Mn) > 0:
        nmi_Mn = calc_nmi(sub_Mn)
        null_Mn = [
            float(normalized_mutual_info_score(sub_Mn['unit_group'], rng.permutation(sub_Mn['series'].values)))
            for _ in range(1000)
        ]
        z_Mn = (nmi_Mn - np.mean(null_Mn)) / max(1e-9, np.std(null_Mn))
        pred_hits = np.array([sub_Mn.iloc[i]['series'] == dom_ser_L[sub_Mn.iloc[i]['unit_group']] for i in range(len(sub_Mn))])
        acc_Mn = float(pred_hits.mean())
        # Stratified shuffle of series on M_new_clean
        st_m = (sub_Mn['site'] + '|' + sub_Mn['kind']).values
        idx_m = collections.defaultdict(list)
        for idx, st in enumerate(st_m):
            idx_m[st].append(idx)
        m_ser = sub_Mn['series'].values
        m_ug = sub_Mn['unit_group'].values
        null_acc_Mn = []
        for _ in range(1000):
            ps = m_ser.copy()
            for ii in idx_m.values():
                if len(ii) > 1:
                    ps[ii] = rng.permutation(m_ser[ii])
            null_acc_Mn.append(float(np.mean([ps[i] == dom_ser_L[m_ug[i]] for i in range(len(sub_Mn))])))
        z_acc_Mn = (acc_Mn - np.mean(null_acc_Mn)) / max(1e-9, np.std(null_acc_Mn))
        say(f"  HELD-OUT M_new_clean (n={len(sub_Mn)}): NMI={nmi_Mn:.4f} vs shuffle {np.mean(null_Mn):.4f} (z={z_Mn:+.1f}, P={pval_ge(null_Mn, nmi_Mn):.4f})")
        say(f"  HELD-OUT Lipi->M_new_clean series prediction accuracy: {int(pred_hits.sum())}/{len(sub_Mn)} = {100*acc_Mn:.1f}% "
            f"vs (site x kind)-stratified shuffle {100*np.mean(null_acc_Mn):.1f}% (z={z_acc_Mn:+.1f}, P={pval_ge(null_acc_Mn, acc_Mn):.4f})")

    # Graphic Packing Law inside S / T / B (for non-F, non-A discrete counts)
    stb_U = oc_U[oc_U['series'].isin(['S', 'T', 'B'])].copy()
    say("\n--- Graphic Packing Transition (S -> T -> B) across deduplicated corpus ---")
    for band_label, vmin, vmax in [('Values 1-5', 1, 5), ('Values 6-8', 6, 8), ('Values 9-10', 9, 10), ('Value 12', 12, 12), ('Value 24', 24, 24)]:
        sb = stb_U[(stb_U['val'] >= vmin) & (stb_U['val'] <= vmax)]
        vc = sb['series'].value_counts().to_dict()
        say(f"  {band_label:12s} (n={len(sb):4d}): S={vc.get('S',0):4d} ({100*vc.get('S',0)/max(1,len(sb)):5.1f}%), "
            f"T={vc.get('T',0):4d} ({100*vc.get('T',0)/max(1,len(sb)):5.1f}%), "
            f"B={vc.get('B',0):4d} ({100*vc.get('B',0)/max(1,len(sb)):5.1f}%)")

    # Syntactic Direction Split: Abstract standards (kalam, nirai, vallam, kalancu) take count AFTER ('X n'),
    # while unit containers & discrete items (cup, porter, trees, crop, quarter, dozen) take count BEFORE ('n X').
    STANDARDS = {'kalam', 'nirai', 'vallam', 'kalancu'}
    ITEMS_CONTAINERS = {'cup', 'porter', 'tree_390', 'tree_405', 'tree_407', 'crop_806', 'crop_838',
                        'quarter', 'dozen', 'fish_plain', 'fish_marked', 'fish_crate', 'diamond_hand', 'woman', 'staff_man'}
    say("\n--- Syntactic Count-Direction Split ('UNIT n' vs 'n ITEM') ---")
    for cname, cdf in [('Lipi events', oc_L), ('Held-out M_new_clean', oc_Mn)]:
        d_sub = cdf[cdf['side'].isin(['before', 'after']) & cdf['unit_group'].isin(STANDARDS | ITEMS_CONTAINERS)].copy()
        s_std = d_sub[d_sub['unit_group'].isin(STANDARDS)]
        s_itm = d_sub[d_sub['unit_group'].isin(ITEMS_CONTAINERS)]
        p_after_std = (s_std['side'] == 'after').mean() if len(s_std) else 0.0
        p_after_itm = (s_itm['side'] == 'after').mean() if len(s_itm) else 0.0
        gap_obs = p_after_std - p_after_itm
        # 1,000 sign-group label permutations across unit_groups
        u_grps = list(set(d_sub['unit_group']))
        n_std_g = len(set(u_grps) & STANDARDS)
        null_gaps = []
        for _ in range(1000):
            fake_std = set(rng.choice(u_grps, size=n_std_g, replace=False))
            a1 = (d_sub[d_sub['unit_group'].isin(fake_std)]['side'] == 'after').mean()
            a2 = (d_sub[~d_sub['unit_group'].isin(fake_std)]['side'] == 'after').mean()
            null_gaps.append(float(a1 - a2))
        say(f"  {cname:20s}: Standards post-counted {int((s_std['side']=='after').sum())}/{len(s_std)} ({100*p_after_std:.1f}%) "
            f"vs Containers/Items {int((s_itm['side']=='after').sum())}/{len(s_itm)} ({100*p_after_itm:.1f}%); "
            f"gap={gap_obs:+.3f} vs group-shuffle {np.mean(null_gaps):+.3f} (P={pval_ge(null_gaps, gap_obs):.4f})")

    # ==========================================================================
    # 2B. DIRECTED CONVERSION LADDER DAG & ORDER TESTS
    # ==========================================================================
    say("\n=== STEP 2B: DIRECTED CONVERSION LADDER (PAIRWISE PRECEDENCE & DAG) ===")
    # Core metrological & container signs for the DAG (excluding jar 740 closer & diamond_hand opener, tested separately)
    DAG_MAP = {
        '413': 'grain_hdr',
        '575': 'kottai',
        '605': 'granary',
        '590': 'chest',
        '540': 'parai',
        '704': 'kalam', '705': 'kalam', '706': 'kalam', '707': 'kalam',
        '335': 'bin_town', '336': 'bin_town',
        '711': 'vallam',
        '700': 'cup', '701': 'cup', '703': 'cup',
        '320': 'pati', '321': 'pati', '323': 'pati',
        '061': 'quarter', '062': 'quarter', '063': 'quarter',
        '171': 'nirai',
        '056': 'two_dozen',
        '055': 'dozen',
        '048': 'seven_bkt', '049': 'seven_bkt',
    }

    def pair_counts_from_events(ev_df, umap):
        pc = collections.Counter()
        lines = []
        examples = collections.defaultdict(list)
        for r in ev_df.itertuples(index=False):
            for f in r.faces:
                seq = [umap[s] for s in f if s in umap]
                # Deduplicate repeated identical unit within one face while preserving first appearance order
                dedup_seq = []
                for u in seq:
                    if u not in dedup_seq:
                        dedup_seq.append(u)
                if len(dedup_seq) >= 2:
                    lines.append(dedup_seq)
                    for a, b in itertools.combinations(dedup_seq, 2):
                        pc[(a, b)] += 1
                        if len(examples[(a, b)]) < 3:
                            examples[(a, b)].append(f"{r.cisi}: {' '.join(f)}")
        return pc, lines, examples

    pc_L, lines_L, ex_L = pair_counts_from_events(L_ev, DAG_MAP)
    pc_Mn, lines_Mn, ex_Mn = pair_counts_from_events(Mn_ev, DAG_MAP)
    pc_U, lines_U, ex_U = pair_counts_from_events(U_ev, DAG_MAP)

    # Fit exact Slater / Minimum-Violation Ranking on Lipi events ONLY
    units_present = sorted({u for pair in pc_U for u in pair})
    # Initial score by smoothed net precedence rate on Lipi: (wins + 0.5) / (wins + losses + 1.0)
    def fit_slater_order(pc_dict, nodes):
        net = {}
        for u in nodes:
            w = sum(pc_dict[(u, v)] for v in nodes if v != u)
            l = sum(pc_dict[(v, u)] for v in nodes if v != u)
            net[u] = (w - l) / (w + l + 1.0)
        order = sorted(nodes, key=lambda u: (-net[u], u))
        # Local adjacent-swap hill climbing + 2-opt insertion to minimize Lipi backward edges
        def score_ord(ord_list):
            rk = {u: i for i, u in enumerate(ord_list)}
            return sum(c for (a, b), c in pc_dict.items() if rk[a] < rk[b])
        improved = True
        best_s = score_ord(order)
        while improved:
            improved = False
            for i in range(len(order)):
                u = order[i]
                rem = order[:i] + order[i + 1:]
                for j in range(len(order)):
                    cand = rem[:j] + [u] + rem[j:]
                    sc = score_ord(cand)
                    if sc > best_s:
                        order = cand
                        best_s = sc
                        improved = True
                        break
                if improved:
                    break
        return order

    dag_order = fit_slater_order(pc_L, units_present)
    dag_rank = {u: i + 1 for i, u in enumerate(dag_order)}
    say("Fitted Lipi topological rank order (1 = largest / earliest on line):")
    for u in dag_order:
        wL = sum(pc_L[(u, v)] for v in units_present if v != u)
        lL = sum(pc_L[(v, u)] for v in units_present if v != u)
        wM = sum(pc_Mn[(u, v)] for v in units_present if v != u)
        lM = sum(pc_Mn[(v, u)] for v in units_present if v != u)
        say(f"  Rank {dag_rank[u]:2d}: {u:12s} | Lipi first={wL:2d}, second={lL:2d} | M_new first={wM:2d}, second={lM:2d}")

    def dag_agreement(pc_dict, rk):
        tot = sum(pc_dict.values())
        fwd = sum(c for (a, b), c in pc_dict.items() if rk[a] < rk[b])
        return fwd, tot, (fwd / tot if tot else 0.0)

    fwd_L, tot_L, acc_dag_L = dag_agreement(pc_L, dag_rank)
    fwd_Mn, tot_Mn, acc_dag_Mn = dag_agreement(pc_Mn, dag_rank)
    fwd_U, tot_U, acc_dag_U = dag_agreement(pc_U, dag_rank)

    # Control A: 1,000 within-line unit-order shuffles (refitting Slater order each time on Lipi!)
    null_dag_L = []
    for _ in range(1000):
        shuf_pc = collections.Counter()
        for ln in lines_L:
            pl = list(rng.permutation(ln))
            for a, b in itertools.combinations(pl, 2):
                shuf_pc[(a, b)] += 1
        ord_s = fit_slater_order(shuf_pc, units_present)
        rk_s = {u: i + 1 for i, u in enumerate(ord_s)}
        _, _, sh_acc = dag_agreement(shuf_pc, rk_s)
        null_dag_L.append(sh_acc)

    # Control B: 1,000 frequency-matched DECOY sign sets (interior non-OPEN/SLOT/CLOSER signs of matching Lipi frequency)
    all_L_faces = [f for r in L_ev.itertuples(index=False) for f in r.faces]
    sign_freq_L = collections.Counter(s for f in all_L_faces for s in f)
    excluded_for_decoy = (
        set(DAG_MAP.keys()) | set(PURE_NUMS.keys()) | OPENER_SIGNS |
        {'740', '741', '742', '745', '400', '090', '520', '060', '368', '151', '154', '156', '158', '000', 'ALT'}
    )
    pool_signs = [s for s, c in sign_freq_L.items() if s not in excluded_for_decoy and c >= 3]

    decoy_accs = []
    decoy_fwd_vols = []
    decoy_mnew_fwds = []
    dag_signs_list = sorted(DAG_MAP.keys())
    peers_for = {}
    for s in dag_signs_list:
        f0 = max(3, sign_freq_L[s])
        ps = [p for p in pool_signs if 0.5 * f0 <= sign_freq_L[p] <= 2.0 * f0]
        if len(ps) < 5:
            ps = sorted(pool_signs, key=lambda p: abs(sign_freq_L[p] - f0))[:10]
        peers_for[s] = ps

    for _ in range(1000):
        dmap = {}
        used = set()
        for s in dag_signs_list:
            cands = [p for p in peers_for[s] if p not in used] or peers_for[s]
            pick = rng.choice(cands)
            used.add(pick)
            dmap[pick] = DAG_MAP[s]
        d_pc, _, _ = pair_counts_from_events(L_ev, dmap)
        d_nodes = sorted({u for pair in d_pc for u in pair})
        if d_nodes:
            d_ord = fit_slater_order(d_pc, d_nodes)
            d_rk = {u: i + 1 for i, u in enumerate(d_ord)}
            dfwd, dtot, dacc = dag_agreement(d_pc, d_rk)
            decoy_fwd_vols.append(dfwd)
            if dtot >= 10:
                decoy_accs.append(dacc)
            # Out-of-sample transfer to M_new_clean without refitting!
            d_pc_mn, _, _ = pair_counts_from_events(Mn_ev, dmap)
            mfwd = sum(c for (a, b), c in d_pc_mn.items() if a in d_rk and b in d_rk and d_rk[a] < d_rk[b])
            decoy_mnew_fwds.append(mfwd)
        else:
            decoy_fwd_vols.append(0)
            decoy_mnew_fwds.append(0)

    # Held-out M_new_clean within-line shuffle (applying frozen Lipi dag_rank!)
    null_dag_Mn = []
    for _ in range(1000):
        spc = collections.Counter()
        for ln in lines_Mn:
            pl = list(rng.permutation(ln))
            for a, b in itertools.combinations(pl, 2):
                spc[(a, b)] += 1
        null_dag_Mn.append(dag_agreement(spc, dag_rank)[2])

    say(f"\nGlobal DAG Order Consistency:")
    say(f"  Lipi deduplicated events: {fwd_L}/{tot_L} = {100*acc_dag_L:.1f}% vs refitted within-line shuffle "
        f"{100*np.mean(null_dag_L):.1f}% +- {100*np.std(null_dag_L):.1f}% (P={pval_ge(null_dag_L, acc_dag_L):.4f})")
    say(f"  Raw ratio vs 1,000 interior sign decoys: real {100*acc_dag_L:.1f}% vs sparse decoy mean {100*np.mean(decoy_accs):.1f}% (P={pval_ge(decoy_accs, acc_dag_L):.4f}; sparse decoys average only {np.mean(decoy_fwd_vols):.1f} ordered pairs!)")
    say(f"  RESCUE (Domain Co-Occurrence x Order Lock vs 1,000 interior decoys): Lipi ordered pairs={fwd_L} vs decoy mean={np.mean(decoy_fwd_vols):.1f} (max={np.max(decoy_fwd_vols)}, P={pval_ge(decoy_fwd_vols, fwd_L):.4f}); "
        f"Held-out M_new ordered pairs={fwd_Mn} vs decoy mean={np.mean(decoy_mnew_fwds):.1f} (max={np.max(decoy_mnew_fwds)}, P={pval_ge(decoy_mnew_fwds, fwd_Mn):.4f})")
    say(f"  HELD-OUT M_new_clean directional accuracy (frozen Lipi DAG rank!): {fwd_Mn}/{tot_Mn} = {100*acc_dag_Mn:.1f}% "
        f"vs shuffle {100*np.mean(null_dag_Mn):.1f}% (exact binom P={binomtest(fwd_Mn, max(1, tot_Mn), 0.5, alternative='greater').pvalue:.4g}, "
        f"perm P={pval_ge(null_dag_Mn, acc_dag_Mn):.4f})")

    # Export pairwise order table
    pair_rows = []
    for a, b in itertools.combinations(dag_order, 2):
        ab_L, ba_L = pc_L[(a, b)], pc_L[(b, a)]
        ab_M, ba_M = pc_Mn[(a, b)], pc_Mn[(b, a)]
        ab_U, ba_U = ab_L + ab_M, ba_L + ba_M
        if ab_U + ba_U == 0:
            continue
        p_bin = binomtest(ab_U, ab_U + ba_U, 0.5, alternative='greater').pvalue
        ex_str = (ex_U[(a, b)] or ex_U[(b, a)])[0]
        pair_rows.append(dict(
            higher_unit=a, lower_unit=b,
            fwd_lipi=ab_L, rev_lipi=ba_L,
            fwd_mnew=ab_M, rev_mnew=ba_M,
            fwd_total=ab_U, rev_total=ba_U,
            total_meetings=ab_U + ba_U,
            fwd_share=round(ab_U / (ab_U + ba_U), 3),
            binom_p_one_sided=round(p_bin, 5),
            example=ex_str
        ))
    pd.DataFrame(pair_rows).sort_values('total_meetings', ascending=False).to_csv(
        os.path.join(OUT_DIR, 'ladder_order_pairs.csv'), index=False
    )

    # ==========================================================================
    # 2C. EXACT CONVERSION RATIOS & COMPETING BASE TESTS
    # ==========================================================================
    say("\n=== STEP 2C: EXACT CONVERSION RATIOS & BASE FINGERPRINTS ===")

    # 1. Cup 700 -> R = 12 (Divisors of 12: {1, 2, 3, 4, 6} vs Base 8 {1,2,4}, Base 10 {1,2,5}, Binary {1,2,4,8})
    cup_L = oc_L[oc_L['unit_group'] == 'cup']['val'].values
    cup_Mn = oc_Mn[oc_Mn['unit_group'] == 'cup']['val'].values
    cup_U = oc_U[oc_U['unit_group'] == 'cup']['val'].values
    div12_L = np.isin(cup_L, [1, 2, 3, 4, 6]).mean()
    div12_Mn = np.isin(cup_Mn, [1, 2, 3, 4, 6]).mean() if len(cup_Mn) else np.nan
    bin_U = np.isin(cup_U, [1, 2, 4, 8]).mean()
    dec_U = np.isin(cup_U, [1, 2, 5, 10]).mean()

    # Pool of all non-cup owned counts on deduplicated events for 1,000-draw control
    non_cup_L = oc_L[(oc_L['unit_group'] != 'cup') & (oc_L['val'] <= 12)]['val'].values
    null_div12_L = [np.isin(rng.choice(non_cup_L, size=len(cup_L), replace=True), [1, 2, 3, 4, 6]).mean() for _ in range(1000)]
    non_cup_Mn = oc_Mn[(oc_Mn['unit_group'] != 'cup') & (oc_Mn['val'] <= 12)]['val'].values
    null_div12_Mn = [np.isin(rng.choice(non_cup_Mn, size=len(cup_Mn), replace=True), [1, 2, 3, 4, 6]).mean() for _ in range(1000)] if len(cup_Mn) else [0.0]

    # Missing-5 gap test on tall strokes (035 has 51 uses on non-cup signs in Lipi+M_new, 0 on cup 700!)
    f_all = oc_U[oc_U['series'] == 'F']
    f_cup = f_all[f_all['unit_group'] == 'cup']
    f_non = f_all[f_all['unit_group'] != 'cup']
    n5_cup = int((f_cup['val'] == 5).sum())
    n5_non = int((f_non['val'] == 5).sum())
    p_no5 = fisher_exact([[n5_cup, len(f_cup) - n5_cup], [n5_non, len(f_non) - n5_non]], alternative='less')[1]

    say(f"1. CUP 700 -> KALAM 705/706 (Ratio R = 12, Base-12 fractional shares {{1,2,3,4,6}}):")
    say(f"   Lipi deduplicated events (n={len(cup_L)}): hist={dict(sorted(collections.Counter(cup_L).items()))}")
    say(f"     Divisors of 12 {{1,2,3,4,6}}: {int(np.isin(cup_L, [1,2,3,4,6]).sum())}/{len(cup_L)} = {100*div12_L:.2f}% "
        f"vs non-cup draw {100*np.mean(null_div12_L):.1f}% (P={pval_ge(null_div12_L, div12_L):.4f})")
    say(f"   HELD-OUT M_new_clean (n={len(cup_Mn)}): hist={dict(sorted(collections.Counter(cup_Mn).items()))}")
    if len(cup_Mn):
        say(f"     Divisors of 12 {{1,2,3,4,6}}: {int(np.isin(cup_Mn, [1,2,3,4,6]).sum())}/{len(cup_Mn)} = {100*div12_Mn:.2f}% "
            f"vs non-cup draw {100*np.mean(null_div12_Mn):.1f}% (P={pval_ge(null_div12_Mn, div12_Mn):.4f})")
    say(f"   Competing bases on cup (n={len(cup_U)}): Base-12 divisors={100*np.isin(cup_U,[1,2,3,4,6]).mean():.2f}% | "
        f"Binary {{1,2,4,8}}={100*bin_U:.1f}% | Decimal {{1,2,5,10}}={100*dec_U:.1f}%")
    say(f"   Tall-5 exclusion on cup 700: {n5_cup}/{len(f_cup)} (0.0%) vs {n5_non}/{len(f_non)} ({100*n5_non/max(1,len(f_non)):.1f}%) on other tall-counted signs, Fisher P={p_no5:.3e}")

    # 2. Context-Conditional Ceiling on 711 (vallam = 4 cups = 1/3 kalam):
    # On faces where 711 precedes 700, cup count is capped at 3 (never >=4), whereas without 711 cup >=4 is ~28%!
    cup_rows_U = oc_U[oc_U['unit_group'] == 'cup'].copy()
    cup_rows_U['has_711'] = cup_rows_U['face_text'].apply(lambda s: '711' in s.split())
    c_with711 = cup_rows_U[cup_rows_U['has_711']]['val'].values
    c_no711 = cup_rows_U[~cup_rows_U['has_711']]['val'].values
    ge4_with = int((c_with711 >= 4).sum())
    ge4_no = int((c_no711 >= 4).sum())
    p_711_cap = fisher_exact([[ge4_with, len(c_with711) - ge4_with], [ge4_no, len(c_no711) - ge4_no]], alternative='less')[1]
    cup_dist = cup_rows_U.drop_duplicates('face_text')
    cd_with = cup_dist[cup_dist['has_711']]['val'].values
    cd_no = cup_dist[~cup_dist['has_711']]['val'].values
    p_711_dist = fisher_exact([[(cd_with >= 4).sum(), (cd_with < 4).sum()], [(cd_no >= 4).sum(), (cd_no < 4).sum()]], alternative='less')[1]
    say(f"\n2. VALLAM 711 -> CUP 700 (Ratio R = 4 cups = 1/3 kalam; conditional ceiling <= 3 cups when 711 precedes 700):")
    say(f"   Events with 711 + cup: {len(c_with711)} (hist={dict(collections.Counter(c_with711))}); >=4 cups: {ge4_with}/{len(c_with711)} (0.0%) "
        f"vs {ge4_no}/{len(c_no711)} ({100*ge4_no/max(1,len(c_no711)):.1f}%) without 711 (Fisher P={p_711_cap:.4g}; distinct templates {len(cd_with)}: 0/{len(cd_with)} vs {(cd_no>=4).sum()}/{len(cd_no)}, P={p_711_dist:.4g})")

    # 3. Kalam 705/706 -> Kottai 575 (Ratio R = 6, ceiling = 5 on tall capacity strokes)
    kal_df_L = oc_L[(oc_L['unit_group'] == 'kalam') & (oc_L['series'] == 'F')]
    kal_df_Mn = oc_Mn[(oc_Mn['unit_group'] == 'kalam') & (oc_Mn['series'] == 'F')]
    kal_L = kal_df_L['val'].values
    kal_Mn = kal_df_Mn['val'].values
    kal_U = np.concatenate([kal_L, kal_Mn])
    non_kal_U = oc_U[(oc_U['unit_group'] != 'kalam') & (oc_U['unit_group'] != 'cup')]['val'].values
    ge6_kal = int((kal_U >= 6).sum())
    ge6_non = int((non_kal_U >= 6).sum())
    p_kal_cap = fisher_exact([[ge6_kal, len(kal_U) - ge6_kal], [ge6_non, len(non_kal_U) - ge6_non]], alternative='less')[1]
    say(f"\n3. KALAM 705/706 -> KOTTAI 575 (Ratio R = 6 kalam = 72 cups, ceiling = 5 on tall counts):")
    say(f"   Lipi tall-counted events (n={len(kal_L)}): hist={dict(sorted(collections.Counter(kal_L).items()))}")
    say(f"   HELD-OUT M_new_clean tall-counted events (n={len(kal_Mn)}): hist={dict(sorted(collections.Counter(kal_Mn).items()))}")
    say(f"   Tall counts >= 6 on kalam: {ge6_kal}/{len(kal_U)} ({100*ge6_kal/max(1,len(kal_U)):.1f}%, max={int(kal_U.max()) if len(kal_U) else 0}) vs "
        f"{ge6_non}/{len(non_kal_U)} ({100*ge6_non/max(1,len(non_kal_U)):.1f}%) on non-kalam/cup signs (Fisher P={p_kal_cap:.3e})")

    # 4. Quarter 061/062/063 & Infixed Jar-Mouth 741/742/745/748 -> Ratio R = 4 (ceiling = 3)
    qtr_L = oc_L[oc_L['unit_group'] == 'quarter']['val'].values
    qtr_Mn = oc_Mn[oc_Mn['unit_group'] == 'quarter']['val'].values
    qtr_U = oc_U[oc_U['unit_group'] == 'quarter']['val'].values
    # Jar-mouth stroke distribution across deduplicated events
    jm_L = [NUM_CATALOG[s][1] for r in L_ev.itertuples() for f in r.faces for s in f if s in NUM_CATALOG and NUM_CATALOG[s][0] == 'J']
    jm_Mn = [NUM_CATALOG[s][1] for r in Mn_ev.itertuples() for f in r.faces for s in f if s in NUM_CATALOG and NUM_CATALOG[s][0] == 'J']
    say(f"\n4. QUARTER 061-063 & INFIXED JAR-MOUTH 741-748 (Ratio R = 4, ceiling = 3):")
    say(f"   Quarter 061-063 owned counts: Lipi={dict(sorted(collections.Counter(qtr_L).items()))}, "
        f"M_new_clean={dict(sorted(collections.Counter(qtr_Mn).items()))}; <=3 share={100*(qtr_U<=3).mean():.1f}% (n={len(qtr_U)})")
    say(f"   Infixed Jar-Mouth strokes (741=1, 742-4=2, 745-7=3, 748=4): Lipi={dict(sorted(collections.Counter(jm_L).items()))}, "
        f"M_new_clean={dict(sorted(collections.Counter(jm_Mn).items()))}; <=3 share={100*(np.array(jm_L+jm_Mn)<=3).mean():.2f}% (n={len(jm_L)+len(jm_Mn)})")

    # 5. Nirai 171 Weight Standard -> {3, 5} non-binary steps (including rescued M94 in M_new_clean!)
    nir_L = oc_L[oc_L['unit_group'] == 'nirai']['val'].values
    nir_Mn = oc_Mn[oc_Mn['unit_group'] == 'nirai']['val'].values
    nir_U = oc_U[oc_U['unit_group'] == 'nirai']['val'].values
    f_pool_L = oc_L[(oc_L['series'] == 'F') & (oc_L['unit_group'] != 'nirai')]['val'].values
    f_pool_Mn = oc_Mn[(oc_Mn['series'] == 'F') & (oc_Mn['unit_group'] != 'nirai')]['val'].values
    p35_L = np.isin(nir_L, [3, 5]).mean() if len(nir_L) else 0.0
    p35_Mn = np.isin(nir_Mn, [3, 5]).mean() if len(nir_Mn) else 0.0
    null_nir_L = [np.isin(rng.choice(f_pool_L, size=len(nir_L), replace=True), [3, 5]).mean() for _ in range(1000)]
    null_nir_Mn = [np.isin(rng.choice(f_pool_Mn, size=len(nir_Mn), replace=True), [3, 5]).mean() for _ in range(1000)] if len(nir_Mn) else [0.0]
    say(f"\n5. NIRAI 171 WEIGHT STANDARD (Non-binary stone-weight factors {{3, 5}} only):")
    say(f"   Lipi events (n={len(nir_L)}): hist={dict(sorted(collections.Counter(nir_L).items()))} -> {{3,5}} share={100*p35_L:.1f}% "
        f"vs other F-counts {100*np.mean(null_nir_L):.1f}% (perm P={pval_ge(null_nir_L, p35_L):.4f}, exact binom P={binomtest(int(np.isin(nir_L,[3,5]).sum()), len(nir_L), np.isin(f_pool_L,[3,5]).mean(), alternative='greater').pvalue:.3e})")
    say(f"   HELD-OUT M_new_clean (n={len(nir_Mn)}): hist={dict(sorted(collections.Counter(nir_Mn).items()))} -> {{3,5}} share={100*p35_Mn:.1f}% "
        f"vs other F-counts {100*np.mean(null_nir_Mn):.1f}% (perm P={pval_ge(null_nir_Mn, p35_Mn):.4f}, exact binom P={binomtest(int(np.isin(nir_Mn,[3,5]).sum()), max(1,len(nir_Mn)), np.isin(f_pool_Mn,[3,5]).mean(), alternative='greater').pvalue:.3e})")

    # ==========================================================================
    # EXPORT machine-readable unit_ladder.csv AND commodity_series.csv
    # ==========================================================================
    LADDER_SPECS = [
        # (rung, unit_group, signs, system, ratio_to_below, unit_below, cup_equiv, litres_or_grams, ceiling_obs, role_note)
        (1, 'grain_hdr', '413', 'capacity_grain', None, 'kottai', None, 'grain_domain_header', None, 'Tablet grain-office header preceding 575 or 892'),
        (2, 'kottai', '575', 'capacity_grain', 6, 'kalam', 72.0, '665.3 L (at 6 kalam)', 7, 'Great grain measure; takes stacked 7 before (017-575) or 1-3 after'),
        (3, 'granary', '605', 'container', None, 'kalam', None, 'granary_store', 3, 'Large storage granary container'),
        (4, 'chest', '590', 'container', None, 'kalam', None, 'chest_store', 4, 'Square storage chest / strongbox; precedes kalam on tablets'),
        (5, 'parai', '540', 'capacity_grain', None, 'kalam', None, 'drum/bowtie_measure', 4, 'Bowtie measure; stamped doubled (540-540) on Harappa goblets & rods'),
        (6, 'kalam', '704|705|706|707', 'capacity_grain', 3, 'vallam (12x cup)', 12.0, '110.9 L (~72 kg grain)', 5, 'Primary wholesale grain measure; post-counted in tall strokes 1-5'),
        (7, 'bin_town', '335|336', 'container', None, 'vallam', None, 'store_bin_or_town', 2, 'Stands between 575 and 711 in Harappa grain office formula'),
        (8, 'vallam', '711', 'capacity_grain', 4, 'cup', 4.0, '37.0 L (1/3 kalam)', 3, 'Sub-kalam measure (tuni/vallam = 4 cups); caps following cup 700 at 3'),
        (9, 'cup', '700|701|703', 'capacity_grain', 8, 'pati', 1.0, '9.24 L (~6 kg grain)', 6, 'Standard ration measure (marakkal); counts {1,2,3,4,6} = exact divisors of 12'),
        (10, 'pati', '320|321|323', 'capacity_grain', 4, 'quarter', 0.125, '1.16 L (~0.75 kg/day)', 5, 'Daily ration allowance (1/8 cup; 30 pati = 3.75 cups/month)'),
        (11, 'quarter', '061|062|063', 'fraction', None, None, 0.25, '1/4 fractional unit', 3, 'Quarter fraction; owned counts {1,2,3} (<4)'),
        (12, 'nirai', '171', 'weight', None, 'kalancu', None, 'weight_standard (takes 3,5)', 5, 'High stone-weight standard; post-counted exclusively in {3 (032+031/M94), 5 (035)}'),
        (13, 'kalancu', '645', 'weight', None, 'kunri', None, 'precious_metal_weight', 4, 'Small metal/gold weight unit on seals, bronze axes & multi-face prisms'),
        (14, 'two_dozen', '056', 'bundle_discrete', 2, 'dozen', 24.0, '24 discrete items (8x3)', 1, 'Double-dozen block (24 = 2x055); photo-verified 8x3 strokes & M 121-121'),
        (15, 'dozen', '055|057', 'bundle_discrete', 12, 'item', 12.0, '12 discrete items (4x3)', 2, 'Dozen block (12 = 4x3); multiplied by 1 or 2, precedes kalam & goods'),
        (16, 'block_slanted', '025|026|027|028|029|B119', 'bundle_discrete', None, 'item', 9.0, '6-10 slanted block', 10, '3-row slanted stroke block before 032-740 on Harappa steatite tablets'),
        (17, 'seven_bkt', '048|049', 'bundle_discrete', 7, 'item', 7.0, '7 bracketed unit', 2, 'Bracketed 7-unit after 861-002 or 741'),
    ]

    ladder_rows = []
    for rung, ugrp, signs_s, sys_name, rat, u_below, ceq, phys, ceil_theory, note in LADDER_SPECS:
        ug_L = oc_L[oc_L['unit_group'] == ugrp]
        ug_M = oc_Mn[oc_Mn['unit_group'] == ugrp]
        ug_U = oc_U[oc_U['unit_group'] == ugrp]
        vals_U = collections.Counter(ug_U['val'].tolist())
        ser_U = collections.Counter(ug_U['series'].tolist())
        side_U = collections.Counter(ug_U['side'].tolist())
        ladder_rows.append(dict(
            ladder_rung=rung,
            dag_rank=dag_rank.get(ugrp, ''),
            unit_group=ugrp,
            lipi_signs=signs_s,
            metrological_system=sys_name,
            ratio_to_lower=rat if rat is not None else '',
            lower_unit=u_below if u_below is not None else '',
            cup_equivalents=ceq if ceq is not None else '',
            physical_estimate=phys,
            owned_counts_lipi=len(ug_L),
            owned_counts_mnew=len(ug_M),
            owned_counts_total=len(ug_U),
            dominant_series=ser_U.most_common(1)[0][0] if ser_U else '',
            dominant_side=side_U.most_common(1)[0][0] if side_U else '',
            max_observed_count=max(vals_U) if vals_U else '',
            value_distribution=' '.join(f"{k}:{v}" for k, v in sorted(vals_U.items())),
            structural_constraint=note
        ))
    pd.DataFrame(ladder_rows).to_csv(os.path.join(OUT_DIR, 'unit_ladder.csv'), index=False)

    # Build commodity_series.csv across ALL candidate unit groups in CANDIDATE_UNITS
    comm_rows = []
    by_grp_signs = collections.defaultdict(list)
    by_grp_meta = {}
    for s, (ug, dom, desc) in CANDIDATE_UNITS.items():
        by_grp_signs[ug].append(s)
        if ug not in by_grp_meta:
            by_grp_meta[ug] = (dom, desc)

    for ug in sorted(by_grp_signs.keys()):
        s_list = sorted(by_grp_signs[ug])
        dom, desc = by_grp_meta[ug]
        ev_L_cnt = sum(any(any(x in s_list for x in f) for f in r.faces) for r in L_ev.itertuples(index=False))
        ev_M_cnt = sum(any(any(x in s_list for x in f) for f in r.faces) for r in Mn_ev.itertuples(index=False))
        ug_L = oc_L[oc_L['unit_group'] == ug]
        ug_M = oc_Mn[oc_Mn['unit_group'] == ug]
        ug_U = oc_U[oc_U['unit_group'] == ug]
        n_tot = len(ug_U)
        ser_c = collections.Counter(ug_U['series'].tolist())
        side_c = collections.Counter(ug_U['side'].tolist())
        val_c = collections.Counter(ug_U['val'].tolist())
        dom_ser = ser_c.most_common(1)[0][0] if ser_c else 'none'
        purity = round(ser_c[dom_ser] / n_tot, 3) if n_tot else np.nan
        n_dir = side_c['before'] + side_c['after']
        pct_after = round(side_c['after'] / n_dir, 3) if n_dir else np.nan
        dom_side = 'after' if (n_dir and side_c['after'] > side_c['before']) else ('before' if n_dir else 'none')

        # Generate concise machine-readable constraint for downstream sound/sense solvers
        if dom_ser == 'F' and dom_side == 'after':
            constraint = f"POST-COUNTED STANDARD ({dom}): takes tall strokes F ({100*(ser_c['F']/max(1,n_tot)):.0f}%) AFTER sign; max={max(val_c) if val_c else 'na'}"
        elif dom_ser == 'F' and dom_side == 'before':
            constraint = f"PRE-COUNTED CAPACITY/CONTAINER ({dom}): takes tall strokes F ({100*(ser_c['F']/max(1,n_tot)):.0f}%) BEFORE sign; max={max(val_c) if val_c else 'na'}"
        elif dom_ser == 'A':
            constraint = f"A-COMB LOAD COMMODITY ({dom}): takes A-comb ticks 465-475 ({100*(ser_c['A']/max(1,n_tot)):.0f}%) BEFORE sign + carrier 154/158"
        elif dom_ser in ('S', 'T', 'B'):
            constraint = f"DISCRETE/BUNDLE COUNTED ({dom}): takes short/stacked {dom_ser} ({dom_side}); values={dict(sorted(val_c.items()))}"
        else:
            constraint = f"UNCOUNTED / STRUCTURAL ({dom})"

        comm_rows.append(dict(
            unit_group=ug,
            signs='|'.join(s_list),
            domain=dom,
            lipi_events_present=ev_L_cnt,
            mnew_events_present=ev_M_cnt,
            owned_counts_lipi=len(ug_L),
            owned_counts_mnew=len(ug_M),
            owned_counts_total=n_tot,
            dominant_series=dom_ser,
            series_purity=purity,
            pct_F=round(ser_c['F'] / n_tot, 3) if n_tot else 0.0,
            pct_S=round(ser_c['S'] / n_tot, 3) if n_tot else 0.0,
            pct_T=round(ser_c['T'] / n_tot, 3) if n_tot else 0.0,
            pct_B=round(ser_c['B'] / n_tot, 3) if n_tot else 0.0,
            pct_A=round(ser_c['A'] / n_tot, 3) if n_tot else 0.0,
            dominant_side=dom_side,
            pct_after=pct_after,
            min_val=min(val_c) if val_c else '',
            max_val=max(val_c) if val_c else '',
            values_hist=' '.join(f"{k}:{v}" for k, v in sorted(val_c.items())),
            dag_rank=dag_rank.get(ug, ''),
            solver_constraint=constraint,
            description=desc
        ))
    pd.DataFrame(comm_rows).sort_values('owned_counts_total', ascending=False).to_csv(
        os.path.join(OUT_DIR, 'commodity_series.csv'), index=False
    )

    summary = dict(
        lipi_events=len(L_ev),
        mnew_clean_events=len(Mn_ev),
        false_cross_series_merges_eliminated=naive_merges_L,
        within_series_non_increasing_share=round(non_inc_compounds_L / max(1, clean_compounds_L), 4),
        nmi_lipi=round(nmi_L, 4),
        nmi_lipi_strat_null_mean=round(float(np.mean(null_strat)), 4),
        nmi_lipi_strat_z=round(float(z_strat), 2),
        nmi_lipi_strat_p=pval_ge(null_strat, nmi_L),
        mnew_series_pred_acc=round(acc_Mn, 4),
        mnew_series_pred_null=round(float(np.mean(null_acc_Mn)), 4),
        mnew_series_pred_p=pval_ge(null_acc_Mn, acc_Mn),
        dag_order_lipi=f"{fwd_L}/{tot_L} ({100*acc_dag_L:.1f}%)",
        dag_order_decoy_mean=round(float(np.mean(decoy_accs)), 4),
        dag_order_decoy_p=pval_ge(decoy_accs, acc_dag_L),
        dag_order_mnew=f"{fwd_Mn}/{tot_Mn} ({100*acc_dag_Mn:.1f}%)",
        dag_order_mnew_p=pval_ge(null_dag_Mn, acc_dag_Mn),
        cup_div12_lipi=f"{int(np.isin(cup_L,[1,2,3,4,6]).sum())}/{len(cup_L)} ({100*div12_L:.2f}%)",
        cup_div12_mnew=f"{int(np.isin(cup_Mn,[1,2,3,4,6]).sum())}/{len(cup_Mn)} ({100*div12_Mn:.2f}%)",
        vallam_711_cap_fisher_p=p_711_cap,
        kalam_cap5_fisher_p=p_kal_cap,
        nirai_35_lipi=f"{int(np.isin(nir_L,[3,5]).sum())}/{len(nir_L)}",
        nirai_35_mnew=f"{int(np.isin(nir_Mn,[3,5]).sum())}/{len(nir_Mn)}",
    )
    with open(os.path.join(OUT_DIR, 'ladder_summary.json'), 'w') as fh:
        json.dump(summary, fh, indent=2)
    say("\nSaved unit_ladder.csv, commodity_series.csv, ladder_order_pairs.csv, and ladder_summary.json.")
    log_fh.close()


if __name__ == '__main__':
    main()
