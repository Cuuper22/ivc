#!/usr/bin/env python3
"""met_02_multiface.py — Step 3A: Multi-Face Tablet, Copper Tablet, Sealing & Cross-Object Ledger Equations.

Tests multi-face arithmetic across 2-, 3-, 4-, 5-, and 7-face objects in Lipi and unseen Mahadevan new texts,
with 1,000 permutation controls, four honestly different rescues after the raw-sum null, and rival-explanation tests.

Outputs in work_data/met/:
  - multiface_records.csv
  - crew_kalam_equations.csv
  - recipient_ledgers.csv
  - cross_object_ledgers.csv
  - multiface_summary.json
  - log_02_multiface.txt
"""
import os
import sys
import json
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

LOG_PATH = os.path.join(OUT_DIR, 'log_02_multiface.txt')
log_fh = open(LOG_PATH, 'w')

def say(*args):
    s = ' '.join(str(a) for a in args)
    print(s, flush=True)
    log_fh.write(s + '\n')
    log_fh.flush()

def pval_ge(null_arr, obs):
    null_arr = np.asarray(null_arr, dtype=float)
    return float((1 + np.sum(null_arr >= obs - 1e-12)) / (len(null_arr) + 1))


def extract_multiface_table(ev_df, after_rate, before_rate):
    """Build one row per multi-face object/event with owned counts per face."""
    oc = extract_owned_counts(ev_df, after_rate, before_rate)
    by_stone = collections.defaultdict(list)
    for r in oc.itertuples(index=False):
        by_stone[r.stone_id].append(r)

    rows = []
    for r in ev_df[ev_df['nfaces'] >= 2].itertuples(index=False):
        c_list = by_stone.get(r.stone_id, [])
        face_counts = [
            dict(face=x.face_idx, val=int(x.val), series=x.series, unit=x.unit_group, owner=x.owner, side=x.side)
            for x in c_list
        ]
        rows.append(dict(
            cat=r.cat, stone_id=r.stone_id, cisi=r.cisi, site=r.site, area=r.area,
            kind=r.kind, type=r.type, nfaces=r.nfaces, symbol=r.symbol,
            faces_text=' | '.join(' '.join(f) for f in r.faces),
            ncounts=len(face_counts),
            nfaces_with_counts=len({x['face'] for x in face_counts}),
            counts=face_counts
        ))
    return pd.DataFrame(rows)


def main():
    rng = np.random.default_rng(20261118)
    D = load_corpora()
    L_ev = D['L_events']
    Mn_ev = D['Mnew_clean_events']
    U_ev = pd.concat([L_ev, Mn_ev], ignore_index=True)

    after_rate, before_rate, _ = fit_ownership_rates(L_ev)
    mf_L = extract_multiface_table(L_ev, after_rate, before_rate)
    mf_Mn = extract_multiface_table(Mn_ev, after_rate, before_rate)
    mf_U = pd.concat([mf_L, mf_Mn], ignore_index=True)

    # Save readable CSV of multi-face records
    mf_export = mf_U.copy()
    mf_export['counts_summary'] = mf_export['counts'].apply(
        lambda cl: '; '.join(f"f{x['face']}:{x['val']}({x['series']},{x['unit']})" for x in cl)
    )
    mf_export.drop(columns=['counts']).to_csv(os.path.join(OUT_DIR, 'multiface_records.csv'), index=False)

    say("=== STEP 3A: MULTI-FACE OBJECT INVENTORY (DEDUPLICATED EVENTS) ===")
    say("Lipi multi-face events by face count:", mf_L['nfaces'].value_counts().sort_index().to_dict())
    say("Lipi multi-face events by kind:", mf_L['kind'].value_counts().to_dict())
    say("Held-out M_new_clean multi-face events by face count:", mf_Mn['nfaces'].value_counts().sort_index().to_dict())
    say("Held-out M_new_clean multi-face events by kind:", mf_Mn['kind'].value_counts().to_dict())

    # Inspect all >=4-face objects explicitly
    ge4 = mf_U[mf_U['nfaces'] >= 4]
    say(f"\nAll 4- to 7-face objects in deduplicated corpus (n={len(ge4)}):")
    for r in ge4.itertuples(index=False):
        cs = '; '.join(f"f{x['face']}:{x['val']}({x['series']},{x['unit']})" for x in r.counts)
        say(f"  {r.cisi:7s} ({r.cat}, {r.site}, {r.type}, {r.nfaces} faces): {cs or 'no pure counts'} | {r.faces_text[:95]}")

    # ==========================================================================
    # TEST E1: NAIVE RAW-NUMBER CROSS-FACE SUM (a + b = c) -> EXPECTED NULL
    # ==========================================================================
    say("\n=== TEST E1: NAIVE UNCONVERTED CROSS-FACE SUM (v_i = sum of other faces' counts) ===")
    acct_L = mf_L[mf_L['kind'].isin(['mtab', 'ctab', 'tag'])].copy()
    acct_Mn = mf_Mn[mf_Mn['kind'].isin(['mtab', 'ctab', 'tag'])].copy()

    def raw_sum_hits(df):
        sub = df[(df['ncounts'] >= 3) & (df['nfaces_with_counts'] >= 2)]
        hits = 0
        for cl in sub['counts']:
            vs = [x['val'] for x in cl]
            tot = sum(vs)
            if any(2 * v == tot for v in vs):
                hits += 1
        return hits, len(sub), sub

    h_sum_L, n_sum_L, sub_sum_L = raw_sum_hits(acct_L)
    pool_v = [x['val'] for cl in sub_sum_L['counts'] for x in cl]
    null_sum_L = []
    for _ in range(1000):
        pv = rng.permutation(pool_v)
        k = 0
        ht = 0
        for cl in sub_sum_L['counts']:
            vs = pv[k:k + len(cl)]
            k += len(cl)
            if any(2 * v == vs.sum() for v in vs):
                ht += 1
        null_sum_L.append(ht)
    say(f"Lipi account events with >=3 counts across >=2 faces: {h_sum_L}/{n_sum_L} hit raw sum "
        f"vs shuffle {np.mean(null_sum_L):.2f} (P={pval_ge(null_sum_L, h_sum_L):.4f}) -> NULL as expected (series differ across faces!).")
    say("Launching FOUR honestly different rescues: (R1) Cross-face parity / 12:1 annual-monthly rate, "
        "(R2) Crew x Cup = {6,12} kalam factorization, (R3) Recipient-level ledger invariance & roll-up, (R4) Block-027/Heading/Copper rate locks.")

    # ==========================================================================
    # RESCUE R1: CROSS-FACE PARITY (v_faceA == v_faceB) & KALAM-TO-CUP 12:1 MATCH
    # ==========================================================================
    say("\n=== RESCUE R1: CROSS-FACE PARITY (v_faceA == v_faceB) & 12:1 KALAM-CUP RATE ===")
    def cross_parity_test(df, label):
        sub = df[df['nfaces_with_counts'] >= 2].copy()
        if len(sub) == 0:
            say(f"  {label}: n=0")
            return 0, 0, 0.0, 1.0
        def is_par(cl):
            return any(cl[i]['val'] == cl[j]['val'] and cl[i]['face'] != cl[j]['face']
                       for i in range(len(cl)) for j in range(i + 1, len(cl)))
        obs = sum(is_par(cl) for cl in sub['counts'])
        # Control 1: permute all count values across slots
        vals = np.array([x['val'] for cl in sub['counts'] for x in cl])
        sers = [x['series'] for cl in sub['counts'] for x in cl]
        null_all = []
        for _ in range(1000):
            pv = rng.permutation(vals)
            k = 0
            ht = 0
            for cl in sub['counts']:
                m = len(cl)
                c2 = [dict(face=cl[j]['face'], val=int(pv[k + j])) for j in range(m)]
                k += m
                ht += is_par(c2)
            null_all.append(ht)
        # Control 2 (RIVAL): permute values STRICTLY WITHIN EACH NUMERAL SERIES (F with F, S with S, etc.)
        idx_by_s = collections.defaultdict(list)
        for i, sr in enumerate(sers):
            idx_by_s[sr].append(i)
        null_ser = []
        for _ in range(1000):
            pv = vals.copy()
            for ii in idx_by_s.values():
                if len(ii) > 1:
                    pv[ii] = rng.permutation(vals[ii])
            k = 0
            ht = 0
            for cl in sub['counts']:
                m = len(cl)
                c2 = [dict(face=cl[j]['face'], val=int(pv[k + j])) for j in range(m)]
                k += m
                ht += is_par(c2)
            null_ser.append(ht)
        z_ser = (obs - np.mean(null_ser)) / max(1e-9, np.std(null_ser))
        say(f"  {label} (n={len(sub)}): real={obs}/{len(sub)} ({100*obs/len(sub):.1f}%) "
            f"| global shuffle={np.mean(null_all):.1f} (P={pval_ge(null_all, obs):.4f}) "
            f"| series-matched shuffle={np.mean(null_ser):.1f} (z={z_ser:+.2f}, P={pval_ge(null_ser, obs):.4f})")
        return obs, len(sub), float(np.mean(null_ser)), pval_ge(null_ser, obs)

    par_obs_L, par_n_L, par_null_L, par_p_L = cross_parity_test(acct_L, "Lipi deduplicated account events")
    par_obs_Ld, par_n_Ld, _, par_p_Ld = cross_parity_test(acct_L.drop_duplicates('faces_text'), "Lipi distinct multi-face templates")
    par_obs_Mn, par_n_Mn, par_null_Mn, par_p_Mn = cross_parity_test(acct_Mn, "HELD-OUT M_new_clean account events")
    cross_parity_test(pd.concat([acct_L, acct_Mn], ignore_index=True), "Combined Lipi + M_new_clean account events")

    # Specific check: records carrying BOTH a kalam count (annual = 12 cups/kalam) and a cup count (monthly = 1 cup/mo)
    kc_rows = []
    for r in pd.concat([acct_L, acct_Mn], ignore_index=True).drop_duplicates('faces_text').itertuples(index=False):
        ka = [x['val'] for x in r.counts if x['unit'] == 'kalam']
        cu = [x['val'] for x in r.counts if x['unit'] == 'cup']
        if ka and cu:
            kc_rows.append((r.cisi, ka[0], cu[0], ka[0] == cu[0], r.faces_text))
    n_kc = len(kc_rows)
    h_kc = sum(x[3] for x in kc_rows)
    # Chance that a random kalam count and random cup count match
    all_ka = [x['val'] for r in acct_L['counts'] for x in r if x['unit'] == 'kalam'] or [3]
    all_cu = [x['val'] for r in acct_L['counts'] for x in r if x['unit'] == 'cup'] or [3]
    p_match_kc = float(np.mean([rng.choice(all_ka) == rng.choice(all_cu) for _ in range(10000)]))
    p_bin_kc = binomtest(h_kc, max(1, n_kc), p_match_kc, alternative='greater').pvalue if n_kc else 1.0
    say(f"  Annual-to-Monthly 12:1 Rate (distinct templates with kalam + cup): {h_kc}/{n_kc} have kalam_count == cup_count "
        f"(chance {100*p_match_kc:.1f}%, binom P={p_bin_kc:.4f}):")
    for cisi, k0, c0, eq, ft in kc_rows:
        say(f"    {cisi:7s}: {k0} kalam (= {12*k0} cups/yr) <-> {c0} cups/mo | match={eq} | {ft}")

    # ==========================================================================
    # RESCUE R2: CREW x CUP = {6, 12} (HALF OR WHOLE KALAM) & RIVAL SPLIT
    # ==========================================================================
    say("\n=== RESCUE R2: CREW / PERSON COUNT x CUP COUNT = {6, 12} (HALF OR WHOLE KALAM) ===")
    PERSON_UNITS = {'diamond_hand', 'porter', 'woman', 'staff_man', 'seated_man', 'bondsman', 'cultivator', 'man', 'twin_men'}

    def extract_crew_cup(ev_df):
        oc = extract_owned_counts(ev_df, after_rate, before_rate)
        by_st = collections.defaultdict(list)
        for r in oc.itertuples(index=False):
            by_st[r.stone_id].append(r)
        out = []
        for r in ev_df[ev_df['kind'].isin(['mtab', 'ctab', 'tag'])].itertuples(index=False):
            cl = by_st.get(r.stone_id, [])
            cups = [x for x in cl if x.unit_group == 'cup']
            ppls = []
            for f in r.faces:
                for run in parse_num_runs(f):
                    if run['role'] != 'count':
                        continue
                    a, b = run['start'], run['end']
                    left = f[a - 1] if a > 0 else '^'
                    right = f[b] if b < len(f) else '$'
                    if left in ('705', '706', '171', '711'):
                        continue
                    if right in CANDIDATE_UNITS and CANDIDATE_UNITS[right][0] in PERSON_UNITS:
                        if not (b + 1 < len(f) and f[b + 1] == '740'):
                            ppls.append((run['val'], CANDIDATE_UNITS[right][0], right))
                    elif right == '$' and left in CANDIDATE_UNITS and CANDIDATE_UNITS[left][0] in PERSON_UNITS:
                        if not (left in OPENER_SIGNS and a == 1):
                            ppls.append((run['val'], CANDIDATE_UNITS[left][0], left))
            if cups and ppls:
                c_val = int(cups[0].val)
                p_val, p_ug, p_sg = int(ppls[0][0]), ppls[0][1], ppls[0][2]
                out.append(dict(
                    cat=r.cat, stone_id=r.stone_id, cisi=r.cisi, site=r.site, area=r.area,
                    person_unit=p_ug, person_sign=p_sg,
                    person_count=p_val, cup_count=c_val, product=p_val * c_val,
                    hit_6_12=(p_val * c_val) in (6, 12),
                    is_gang_E11=('ETrench 11' in str(r.area)) or ('003 156' in ' | '.join(' '.join(f) for f in r.faces)),
                    faces_text=' | '.join(' '.join(f) for f in r.faces)
                ))
        return pd.DataFrame(out)

    crew_L = extract_crew_cup(L_ev)
    crew_Mn = extract_crew_cup(Mn_ev)
    crew_U = pd.concat([crew_L, crew_Mn], ignore_index=True)
    crew_U.to_csv(os.path.join(OUT_DIR, 'crew_kalam_equations.csv'), index=False)

    # Empirical Harappa cup distribution across all deduplicated cup events
    all_cup_vals = extract_owned_counts(U_ev, after_rate, before_rate)
    har_cup_pool = all_cup_vals[(all_cup_vals['unit_group'] == 'cup') & (all_cup_vals['site'] == 'Harappa')]['val'].values

    for label, sub_c in [
        ("All deduplicated crew+cup events (Lipi + M_new)", crew_U),
        ("Distinct crew+cup text templates", crew_U.drop_duplicates('faces_text')),
        ("RIVAL TEST — Excluding E-Trench-11 & 003-156 gang batch (distinct templates)",
         crew_U[~crew_U['is_gang_E11']].drop_duplicates('faces_text')),
        ("HELD-OUT M_new_clean crew+cup events", crew_Mn),
    ]:
        if len(sub_c) == 0:
            say(f"  {label}: n=0")
            continue
        obs_h = int(sub_c['hit_6_12'].sum())
        p_arr = sub_c['person_count'].values
        c_arr = sub_c['cup_count'].values
        null_perm = [int(np.isin(p_arr * rng.permutation(c_arr), [6, 12]).sum()) for _ in range(1000)]
        null_emp = [int(np.isin(p_arr * rng.choice(har_cup_pool, size=len(p_arr), replace=True), [6, 12]).sum()) for _ in range(1000)]
        say(f"  {label}: {obs_h}/{len(sub_c)} ({100*obs_h/len(sub_c):.1f}%) multiply to 6 or 12 "
            f"| within-set shuffle={np.mean(null_perm):.2f} (P={pval_ge(null_perm, obs_h):.4f}) "
            f"| Harappa cup-pool draw={np.mean(null_emp):.2f} (P={pval_ge(null_emp, obs_h):.4f})")
        for r in sub_c.itertuples(index=False):
            say(f"    {r.cisi:7s} ({r.area or 'no-area':11s}): {r.person_count} x {r.person_unit}({r.person_sign}) * {r.cup_count} cups = {r.product:2d} "
                f"[{'HIT' if r.hit_6_12 else 'miss'}] | {r.faces_text}")

    # ==========================================================================
    # RESCUE R3: RECIPIENT-LEVEL LEDGER INVARIANCE, CUMULATIVE SUMS & SEAL LINKS
    # ==========================================================================
    say("\n=== RESCUE R3: RECIPIENT-LEVEL LEDGER INVARIANCE & CUMULATIVE KALAM TOTALS ===")
    def get_jar_name(faces):
        """Extract canonical recipient face and stem before jar 740."""
        for f in faces:
            if '740' in f and '000' not in f and 'ALT' not in f:
                j = f.index('740')
                if j >= 1:
                    stem = f[:j]
                    if len(stem) >= 3 and stem[0] in OPENER_SIGNS and stem[1] in ('002', '060', '741', '742', '745', '368'):
                        stem = stem[2:]
                    if stem:
                        ending = ' '.join(f[j:])
                        return ' '.join(stem), ending, ' '.join(f)
        return None, None, None

    oc_all = extract_owned_counts(U_ev, after_rate, before_rate)
    cups_by_stone = {}
    kal_by_stone = {}
    for r in oc_all.itertuples(index=False):
        if r.unit_group == 'cup':
            cups_by_stone[r.stone_id] = int(r.val)
        elif r.unit_group == 'kalam':
            kal_by_stone[r.stone_id] = int(r.val)

    rec_rows = []
    for r in U_ev.itertuples(index=False):
        stem, ending, full_nface = get_jar_name(r.faces)
        if not stem:
            continue
        rec_rows.append(dict(
            cat=r.cat, stone_id=r.stone_id, cisi=r.cisi, site=r.site, area=r.area,
            kind=r.kind, stem=stem, ending=ending, name_face=full_nface,
            cup_val=cups_by_stone.get(r.stone_id, np.nan),
            kalam_val=kal_by_stone.get(r.stone_id, np.nan),
            faces_text=' | '.join(' '.join(f) for f in r.faces)
        ))
    df_rec = pd.DataFrame(rec_rows)

    # R3a: One unit per (name_face, cup_val, area) as in recheck_06_tablets.py!
    har_chits_raw = df_rec[(df_rec['site'] == 'Harappa') & (df_rec['kind'].isin(['mtab', 'tag'])) & df_rec['cup_val'].notna()].copy()
    har_chits_raw['cup_val'] = har_chits_raw['cup_val'].astype(int)
    har_chits = har_chits_raw.drop_duplicates(['name_face', 'cup_val', 'area']).reset_index(drop=True)

    def same_amount_pairs(stems, amounts):
        pairs_tot = 0
        pairs_eq = 0
        by_s = collections.defaultdict(list)
        for s, a in zip(stems, amounts):
            by_s[s].append(a)
        for s, al in by_s.items():
            if len(al) >= 2:
                for x, y in itertools.combinations(al, 2):
                    pairs_tot += 1
                    if x == y:
                        pairs_eq += 1
        return pairs_eq, pairs_tot

    eq_obs, tot_pairs = same_amount_pairs(har_chits['name_face'].values, har_chits['cup_val'].values)
    null_eq = [same_amount_pairs(har_chits['name_face'].values, rng.permutation(har_chits['cup_val'].values))[0] for _ in range(1000)]

    # Also excluding generic single-sign tax title '176' (which draws 2, 3, and 4 cups across 14 trenches)
    har_pers = har_chits[har_chits['stem'] != '176'].reset_index(drop=True)
    eq_p, tot_p = same_amount_pairs(har_pers['name_face'].values, har_pers['cup_val'].values)
    null_eq_p = [same_amount_pairs(har_pers['name_face'].values, rng.permutation(har_pers['cup_val'].values))[0] for _ in range(1000)]

    say(f"R3a. Recipient Ration Lock on Harappa deduplicated (name, cup, trench) units (n={len(har_chits)} units, {har_chits['name_face'].nunique()} names):")
    say(f"     All names: {eq_obs}/{tot_pairs} ({100*eq_obs/max(1,tot_pairs):.1f}%) same-amount pairs vs shuffle {np.mean(null_eq):.1f} (P={pval_ge(null_eq, eq_obs):.4f})")
    say(f"     Personal names (excluding generic title 176, n={len(har_pers)} units): {eq_p}/{tot_p} ({100*eq_p/max(1,tot_p):.1f}%) "
        f"vs shuffle {np.mean(null_eq_p):.1f} (ratio {eq_p/max(0.1,np.mean(null_eq_p)):.2f}x, P={pval_ge(null_eq_p, eq_p):.4f})")
    c_vals = har_chits['cup_val'].values
    s_vals = har_chits['stem'].values

    # R3b: Cumulative cup sum per multi-event recipient hitting {6, 12, 18, 24} (multiples of half-kalam = 6 cups!)
    multi_stems = [s for s, g in har_chits.groupby('stem') if 2 <= len(g) <= 6]
    obs_mod6 = sum((har_chits[har_chits['stem'] == s]['cup_val'].sum() % 6 == 0) for s in multi_stems)
    null_mod6 = []
    for _ in range(1000):
        pv = rng.permutation(c_vals)
        tmp = pd.DataFrame({'stem': s_vals, 'c': pv})
        sums = tmp.groupby('stem')['c'].sum()
        null_mod6.append(sum((sums[s] % 6 == 0) for s in multi_stems))
    say(f"R3b. Cumulative Recipient Totals (2-6 events per name, n={len(multi_stems)} names): "
        f"{obs_mod6}/{len(multi_stems)} ({100*obs_mod6/max(1,len(multi_stems)):.1f}%) sum to a multiple of 6 cups (half/whole kalam) "
        f"vs shuffle {np.mean(null_mod6):.1f} (P={pval_ge(null_mod6, obs_mod6):.4f})")

    # Export recipient ledger summary
    rec_summary = []
    for stem, g in har_chits.groupby('stem'):
        if len(g) >= 2:
            rec_summary.append(dict(
                recipient_stem=stem, n_events=len(g),
                n_trenches=g['area'].nunique(),
                cup_issues=','.join(str(x) for x in sorted(g['cup_val'].tolist())),
                total_cups=int(g['cup_val'].sum()),
                mod6_half_kalam=(int(g['cup_val'].sum()) % 6 == 0),
                constant_issue=(g['cup_val'].nunique() == 1),
                endings=';'.join(sorted(set(g['ending'])))
            ))
    pd.DataFrame(rec_summary).sort_values('n_events', ascending=False).to_csv(
        os.path.join(OUT_DIR, 'recipient_ledgers.csv'), index=False
    )

    # R3c: Cross-Object Seal <-> Tablet/Tag Ledger Matching
    cross_rows = []
    for stem, g in df_rec.groupby('stem'):
        kinds = set(g['kind'])
        if 'seal' in kinds and (kinds & {'mtab', 'ctab', 'tag'}):
            seals_g = g[g['kind'] == 'seal']
            tabs_g = g[g['kind'].isin(['mtab', 'ctab', 'tag'])]
            cross_rows.append(dict(
                recipient_stem=stem,
                n_seals=len(seals_g),
                n_tablets_tags=len(tabs_g),
                seal_sites=','.join(sorted(set(seals_g['site']))),
                tab_sites=','.join(sorted(set(tabs_g['site']))),
                seal_endings=','.join(sorted(set(seals_g['ending']))),
                tab_endings=','.join(sorted(set(tabs_g['ending']))),
                seal_kalam=','.join(str(int(x)) for x in seals_g['kalam_val'].dropna()),
                tab_cups=','.join(str(int(x)) for x in tabs_g['cup_val'].dropna()),
                tab_kalam=','.join(str(int(x)) for x in tabs_g['kalam_val'].dropna()),
            ))
    df_cross = pd.DataFrame(cross_rows)
    df_cross.to_csv(os.path.join(OUT_DIR, 'cross_object_ledgers.csv'), index=False)
    say(f"R3c. Cross-Object Recipient Matches (exact name stem on both Seal and Tablet/Sealing): {len(df_cross)} houses/persons saved to cross_object_ledgers.csv.")

    # ==========================================================================
    # RESCUE R4: BLOCK 025-028 TABLETS & COPPER TABLET ANIMAL-UNIT LOCK
    # ==========================================================================
    say("\n=== RESCUE R4: SLANTED-BLOCK (025-028/B119) TABLETS & COPPER ANIMAL-UNIT MATRIX ===")
    blk_tabs = []
    for r in U_ev.itertuples(index=False):
        flat = [s for f in r.faces for s in f]
        b_hits = [s for s in flat if s in ('025', '026', '027', '028', '029', 'B119')]
        if b_hits:
            blk_tabs.append((r.cisi, r.cat, r.site, r.kind, b_hits[0], cups_by_stone.get(r.stone_id, None), ' | '.join(' '.join(f) for f in r.faces)))
    say(f"Slanted 3-row block (025-029 / M119) deduplicated events (n={len(blk_tabs)}):")
    for cisi, cat, st, kd, bs, cv, ft in blk_tabs:
        say(f"  {cisi:7s} ({cat:10s}, {st:12s}, {kd:4s}): block={bs}, partner_cups={cv} | {ft}")

    # Mohenjo-daro Copper Tablets (TAB:C in Lipi): Animal symbol vs Metrological unit-value signature
    ctabs_L = L_ev[L_ev['type'] == 'TAB:C'].copy()
    oc_ctab = extract_owned_counts(ctabs_L, after_rate, before_rate)
    by_ct = collections.defaultdict(list)
    for r in oc_ctab.itertuples(index=False):
        by_ct[r.stone_id].append(f"{r.unit_group}:{r.val}")
    ctabs_L['anim'] = ctabs_L['symbol'].str.split(':').str[0]
    ctabs_L['met_sig'] = [';'.join(sorted(by_ct[st])) or 'uncounted' for st in ctabs_L['stone_id']]
    ct_valid = ctabs_L[~ctabs_L['anim'].isin(['-', '', 'None', 'unid', 'UID']) & (ctabs_L['met_sig'] != 'uncounted')].copy()
    if len(ct_valid) >= 10:
        nmi_ct = float(normalized_mutual_info_score(ct_valid['anim'], ct_valid['met_sig']))
        null_ct = [float(normalized_mutual_info_score(ct_valid['anim'], rng.permutation(ct_valid['met_sig'].values))) for _ in range(1000)]
        z_ct = (nmi_ct - np.mean(null_ct)) / max(1e-9, np.std(null_ct))
        say(f"\nMohenjo-daro Copper Tablets (deduplicated events with animal & count, n={len(ct_valid)}):")
        say(f"  NMI(Animal Emblem ; Metrological Unit:Count) = {nmi_ct:.4f} vs shuffle {np.mean(null_ct):.4f} +- {np.std(null_ct):.4f} "
            f"(z={z_ct:+.1f}, P={pval_ge(null_ct, nmi_ct):.4f})")
        for anim, g in ct_valid.groupby('anim'):
            if len(g) >= 2:
                say(f"    {anim:12s} (n={len(g):2d}): {g['met_sig'].value_counts().to_dict()}")

    summary = dict(
        multiface_lipi_events=len(mf_L),
        multiface_mnew_events=len(mf_Mn),
        raw_sum_lipi=f"{h_sum_L}/{n_sum_L} (null {np.mean(null_sum_L):.2f})",
        cross_parity_lipi=f"{par_obs_L}/{par_n_L} vs series-null {par_null_L:.1f} (P={par_p_L:.4f})",
        cross_parity_distinct=f"{par_obs_Ld}/{par_n_Ld} (P={par_p_Ld:.4f})",
        cross_parity_mnew=f"{par_obs_Mn}/{par_n_Mn} vs series-null {par_null_Mn:.1f} (P={par_p_Mn:.4f})",
        kalam_cup_12to1_templates=f"{h_kc}/{n_kc} (binom P={p_bin_kc:.4f})",
        recipient_ration_lock_all=f"{eq_obs}/{tot_pairs} vs null {np.mean(null_eq):.1f} (P={pval_ge(null_eq, eq_obs):.4f})",
        recipient_ration_lock_personal=f"{eq_p}/{tot_p} vs null {np.mean(null_eq_p):.1f} (P={pval_ge(null_eq_p, eq_p):.4f})",
        recipient_mod6_sums=f"{obs_mod6}/{len(multi_stems)} vs null {np.mean(null_mod6):.1f} (P={pval_ge(null_mod6, obs_mod6):.4f})",
        cross_object_houses=len(df_cross),
    )
    with open(os.path.join(OUT_DIR, 'multiface_summary.json'), 'w') as fh:
        json.dump(summary, fh, indent=2)
    say("\nSaved multiface_records.csv, crew_kalam_equations.csv, recipient_ledgers.csv, cross_object_ledgers.csv, and multiface_summary.json.")
    log_fh.close()


if __name__ == '__main__':
    main()
