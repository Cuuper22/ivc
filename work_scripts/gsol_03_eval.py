#!/usr/bin/env python3
"""gsol_03_eval.py -- Step 3: Deep Evaluation, Fine-Frame Rival Test, Morpho-Phonetic Solver Redesign,
Equal-Lexicon Benchmark, and Unseen Mahadevan `new texts` Sign-by-Sign Readings.

Executes three decisive follow-ups / redesigns:
  1. Fine-Slot Rival Explanation & Cross-City Split Test on K=1 Primary-Sense Lift:
     - Tests whether K=1 directional category lift (`z=+3.45` Fixed / `z=+2.64` Refit under coarse 14-class `v2_base`,
       where 89 signs sit in one `PERSONAL` bucket) survives shuffling within finer WORD-FREE distributional classes
       (`v2_base + hmm10` and `v2_pushed` from `work_data/frame/classes_v2.csv`) + frequency band + category count!
     - Tests fresh Cross-City generalization: learn directional lift strictly on Mohenjo-daro Lipi -> score zero-shot
       on unseen Harappa/Lothal/Kalibangan `new texts`, and Lipi CV sign-pruning -> unseen `new texts`.
  2. Honest Solver Redesign (Morpho-Phonetic & Rebus-Locked Global QAP + Equal-Size Lexicon M=580):
     - Re-weights the Lipi QAP solver to prioritize language-specific phonetic locks (blind-picture rebus homophony +
       Lipi compound-base stem sharing + Lipi `C <-> A+B` splits + Lipi frame swaps, with semantic coherence as tie-breaker)
       on an EQUAL-SIZED candidate lexicon (`M=580`, matching the smallest lexicon `akkadian_wiktionary` across all 7 languages!)
       against 20 sign-permuted Lipi decoy solves and 1,000 unseen `new texts` shuffles.
  3. Concrete Sign-by-Sign Readings on Unseen Mahadevan `new texts`:
     - Glosses complete held-out `new texts` inscriptions sign-by-sign using the top Lipi-fitted global assignments.
"""
import os
import sys
import json
import time
import collections
import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "work_scripts"))

from sense_core import CATS
from gsol_01_k1_audit import (
    build_directional_corpus,
    pack_directional_edges,
    fit_dir_cat_lift,
    word_pair_matrix_from_cat_lift,
    score_assignments_dir,
    make_shuffles,
    summarize_vs_null,
)
from gsol_02_qap import (
    CANDIDATE_LANGS,
    build_sign_problem,
    build_external_m2v_priors,
    load_language_lexicon,
    make_sign_shuffles,
    eval_zeroshot_new,
    split_3body_bonus,
    eval_lipi_objective,
    save_word_table,
)

OUT_DIR = os.path.join(ROOT, "work_data", "gsol")
os.makedirs(OUT_DIR, exist_ok=True)
SENSE_DIR = os.path.join(ROOT, "work_data", "sense")
DICT_EMB_DIR = "/tmp/dict_emb"

T0 = time.time()
def log(*a):
    print(f"[{time.time() - T0:6.1f}s] [gsol_03]", *a, flush=True)


def run_fine_slot_and_crosscity_k1_tests(n_shuf=1000):
    """Test whether K=1 directional category PMI lift comes from unmodelled word-free sub-slots inside PERSONAL
    or survives fine word-free machine classes (`v2_base x hmm10`) and cross-city splits."""
    log("Part A: Running Fine-Slot Rival Control & Cross-City Split on K=1...")
    S = pd.read_csv(os.path.join(SENSE_DIR, "signs.csv"), dtype={"sign": str}).fillna("")
    SS = pd.read_csv(os.path.join(SENSE_DIR, "senses.csv")).fillna("")
    cl_df = pd.read_csv(os.path.join(ROOT, "work_data", "frame", "classes_v2.csv"), dtype=str).fillna("")
    hmm_map = dict(zip(cl_df.sign, cl_df.hmm10))
    pushed_map = dict(zip(cl_df.sign, cl_df.v2_pushed))

    words = sorted(S.word.unique())
    widx = {w: i for i, w in enumerate(words)}
    W_cnt = len(words)
    real_w = np.array([widx[w] for w in S.word], dtype=np.int32)

    B_ws = np.zeros((W_cnt, 1, 13), dtype=bool)
    valid_ws = np.ones((W_cnt, 1), dtype=bool)
    for w, g in SS.groupby("word", sort=False):
        wi = widx[w]
        r = g.iloc[0]
        for c in str(r.cats).split("|"):
            if c in CATS:
                B_ws[wi, 0, CATS.index(c)] = True
    word_cats = B_ws[:, 0, :].astype(np.float32)
    cat_cnt = word_cats.sum(axis=1)

    events_lipi = json.load(open(os.path.join(SENSE_DIR, "events_lipi.json")))
    events_new = json.load(open(os.path.join(SENSE_DIR, "events_new.json")))
    sidx = {s: i for i, s in enumerate(S.sign)}

    dir_records = build_directional_corpus(events_lipi, events_new, sidx, seed=20261117)
    folds, tw, U1, U2, valid_edge = pack_directional_edges(dir_records, len(S))
    grp_lipi = (folds < 2)
    grp_new = (folds == 2)

    L_lipi = fit_dir_cat_lift(U1, U2, valid_edge, tw, grp_lipi, real_w, word_cats)
    M_lipi = {2: word_pair_matrix_from_cat_lift(B_ws, valid_ws, L_lipi),
              0: word_pair_matrix_from_cat_lift(B_ws, valid_ws, fit_dir_cat_lift(U1, U2, valid_edge, tw, folds == 1, real_w, word_cats)),
              1: word_pair_matrix_from_cat_lift(B_ws, valid_ws, fit_dir_cat_lift(U1, U2, valid_edge, tw, folds == 0, real_w, word_cats))}
    r_new = score_assignments_dir(M_lipi, folds, tw, U1, U2, valid_edge, real_w, grp_new)

    # Compare 3 word-free class granularities for Shuffle B (matching class + band + category count):
    # 1. `v2_base` (14 classes, 174 movable signs)
    # 2. `hmm10` alone (10 pure unsupervised HMM classes, ~180 movable signs)
    # 3. `v2_base_x_hmm10` (splits coarse 89-sign PERSONAL bucket by word-free HMM state!)
    cls_v2 = np.array(list(S.cls))
    cls_hmm = np.array([hmm_map.get(s, "H0") for s in S.sign])
    cls_joint = np.array([f"{c}|{h}" for c, h in zip(cls_v2, cls_hmm)])
    # Also check how many signs can move in each scheme
    band_arr = np.array(list(S.band))
    band_zero = np.zeros_like(band_arr)  # for fine joint classes, test both with band and across bands

    fine_controls = {}
    for label, c_arr, b_arr in (
        ("v2_base_band_cat", cls_v2, band_arr),
        ("hmm10_band_cat", cls_hmm, band_arr),
        ("v2_x_hmm10_cat", cls_joint, band_zero),
        ("v2_x_hmm10_band_cat", cls_joint, band_arr),
    ):
        cells = collections.Counter(zip(c_arr, b_arr))
        movable = sum(v for v in cells.values() if v >= 2)
        sh = make_shuffles(real_w, c_arr, b_arr, cat_cnt, n_shuf, seed=8181, matched=True)
        fixed_scores = score_assignments_dir(M_lipi, folds, tw, U1, U2, valid_edge, sh, grp_new)

        refit_scores = np.zeros(n_shuf, dtype=np.float64)
        for i in range(n_shuf):
            ai = sh[i]
            Li = fit_dir_cat_lift(U1, U2, valid_edge, tw, grp_lipi, ai, word_cats)
            refit_scores[i] = score_assignments_dir({2: word_pair_matrix_from_cat_lift(B_ws, valid_ws, Li)},
                                                    folds, tw, U1, U2, valid_edge, ai, grp_new)
        fine_controls[label] = {
            "movable_signs_of_184": int(movable),
            "n_cells_ge2": int(sum(1 for v in cells.values() if v >= 2)),
            "fixed_new": summarize_vs_null(r_new, fixed_scores),
            "refit_new": summarize_vs_null(r_new, refit_scores),
        }
        log(f"Fine control [{label:22s}] (movable={movable:3d}/184): "
            f"Fixed z={fine_controls[label]['fixed_new']['z']:+5.2f} (P={fine_controls[label]['fixed_new']['P']:.3f}) | "
            f"Refit z={fine_controls[label]['refit_new']['z']:+5.2f} (P={fine_controls[label]['refit_new']['P']:.3f})")

    # Fresh Cross-City Split: Train `Lm` strictly on Mohenjo-daro Lipi -> Test zero-shot on NON-Mohenjo-daro `new texts` (Harappa, Lothal, Kalibangan, Chanhu-daro, etc.)!
    md_lipi = [e for e in events_lipi if "Mohenjo" in str(e.get("site", ""))]
    non_md_new = [e for e in events_new if "Mohenjo" not in str(e.get("site", ""))]
    md_new = [e for e in events_new if "Mohenjo" in str(e.get("site", ""))]
    har_lipi = [e for e in events_lipi if "Harappa" in str(e.get("site", ""))]

    def cross_split_eval(train_evs, test_evs, tag):
        recs = build_directional_corpus(train_evs, test_evs, sidx, seed=99)
        fl, tw_s, u1_s, u2_s, ve_s = pack_directional_edges(recs, len(S))
        tr_m = (fl < 2)
        te_m = (fl == 2)
        L_tr = fit_dir_cat_lift(u1_s, u2_s, ve_s, tw_s, tr_m, real_w, word_cats)
        M_tr = {2: word_pair_matrix_from_cat_lift(B_ws, valid_ws, L_tr)}
        r_te = score_assignments_dir(M_tr, fl, tw_s, u1_s, u2_s, ve_s, real_w, te_m)
        sh_b = make_shuffles(real_w, cls_v2, band_arr, cat_cnt, n_shuf, seed=9191, matched=True)
        s_fix = score_assignments_dir(M_tr, fl, tw_s, u1_s, u2_s, ve_s, sh_b, te_m)
        s_ref = np.zeros(n_shuf, dtype=np.float64)
        for i in range(n_shuf):
            Li = fit_dir_cat_lift(u1_s, u2_s, ve_s, tw_s, tr_m, sh_b[i], word_cats)
            s_ref[i] = score_assignments_dir({2: word_pair_matrix_from_cat_lift(B_ws, valid_ws, Li)}, fl, tw_s, u1_s, u2_s, ve_s, sh_b[i], te_m)
        res = {"fixed_B_cat": summarize_vs_null(r_te, s_fix), "refit_B_cat": summarize_vs_null(r_te, s_ref)}
        log(f"Cross-City [{tag:32s}]: Fixed B_cat z={res['fixed_B_cat']['z']:+5.2f} (P={res['fixed_B_cat']['P']:.3f}) | "
            f"Refit B_cat z={res['refit_B_cat']['z']:+5.2f} (P={res['refit_B_cat']['P']:.3f})")
        return res

    cross_city = {
        "train_MD_lipi_test_NonMD_new": cross_split_eval(md_lipi, non_md_new, "MD Lipi -> Non-MD New"),
        "train_Harappa_lipi_test_MD_new": cross_split_eval(har_lipi, md_new, "Harappa Lipi -> MD New"),
    }
    return {"fine_slot_controls": fine_controls, "cross_city_splits": cross_city}


def solve_morphophonetic_qap(G_lipi, G_swap, G_base, splits, U_rebus, U_role, lex, seed=404, n_starts=8, n_sweeps=32):
    """Step 3 Redesign Solver: Morpho-Phonetic & Rebus-Locked Global QAP on Equal-Sized Lexicons (`M=580`).
    Prioritizes language-specific sound locks (picture-to-slot rebus + compound-base stem sharing +
    3-body `C <-> A+B` concatenation + Lipi frame swaps) with semantic coherence as tie-breaker!"""
    rng = np.random.default_rng(seed)
    N = G_lipi.shape[0]
    M = lex["M"]

    G_sem_n = (G_lipi / max(float(G_lipi.sum()), 1e-9)).astype(np.float32)
    G_swap_n = (G_swap / max(float(G_swap.sum()), 1e-9)).astype(np.float32)
    G_base_n = (G_base / max(float(G_base.sum()), 1e-9)).astype(np.float32)

    # Phonetic-first weights: sound-meaning locks lead, non-circular semantic transition breaks ties
    w_sem, w_swap, w_base, w_split = 0.35, 0.70, 0.85, 0.75
    U_tot = (0.95 * U_rebus + 0.45 * U_role).astype(np.float32)

    S_sem = lex["S_sem"]
    S_swap = lex["S_swap"]
    S_base = lex["S_base"]
    sks, nfs = lex["skels"], lex["norms"]

    splits_by_u = [[] for _ in range(N)]
    tot_split_w = max(sum(wt for _, _, _, wt in splits), 1e-9)
    for c, a, b, wt in splits:
        wn = wt / tot_split_w
        splits_by_u[c].append((0, c, a, b, wn))
        splits_by_u[a].append((1, c, a, b, wn))
        splits_by_u[b].append((2, c, a, b, wn))

    best_pi = None
    best_sc = -1e18

    for st in range(5):
        noise = rng.normal(0, 0.02 if st > 0 else 0.001, size=(N, M)).astype(np.float32)
        _, pi = linear_sum_assignment(-(U_tot / N + noise))
        pi = pi.astype(np.int32)
        for it in range(5):
            grad = (U_tot / N).copy()
            grad += w_sem * (G_sem_n @ S_sem[pi, :] + G_sem_n.T @ S_sem[:, pi].T)
            grad += w_swap * (2.0 * (G_swap_n @ S_swap[pi, :]))
            grad += w_base * (G_base_n @ S_base[pi, :] + G_base_n.T @ S_base[:, pi].T)
            if it < 3:
                grad += rng.normal(0, 0.005 * (3 - it), size=(N, M)).astype(np.float32)
            _, pi_cand = linear_sum_assignment(-grad)
            pi_cand = pi_cand.astype(np.int32)
            sc_cand, _ = eval_lipi_objective(pi_cand, G_sem_n, G_swap_n, G_base_n, splits, U_tot, lex, w_sem, w_swap, w_base, w_split)
            sc_curr, _ = eval_lipi_objective(pi, G_sem_n, G_swap_n, G_base_n, splits, U_tot, lex, w_sem, w_swap, w_base, w_split)
            if sc_cand > sc_curr or it == 0:
                pi = pi_cand
                sc_curr = sc_cand
            if sc_curr > best_sc:
                best_sc = sc_curr
                best_pi = pi.copy()

    pi = best_pi.copy()
    in_use = np.zeros(M, dtype=bool)
    in_use[pi] = True
    n_sw = 20

    for sw_idx, temp in enumerate(np.geomspace(0.015, 0.0002, n_sw)):
        greedy = (sw_idx >= n_sw - 5)
        for u in rng.permutation(N):
            w_old = pi[u]
            in_use[w_old] = False

            pot = (U_tot[u] / N).copy()
            pot += w_sem * (S_sem[:, pi] @ G_sem_n[u, :] + S_sem[pi, :].T @ G_sem_n[:, u])
            if G_swap_n[u].any():
                pot += w_swap * (2.0 * (S_swap[:, pi] @ G_swap_n[u, :]))
            if G_base_n[u].any() or G_base_n[:, u].any():
                pot += w_base * (S_base[:, pi] @ G_base_n[u, :] + S_base[pi, :].T @ G_base_n[:, u])
            pot[in_use] = -1e9

            if splits_by_u[u]:
                top20 = np.argpartition(pot, -20)[-20:]
                for w_c in top20:
                    if in_use[w_c]:
                        continue
                    b3 = 0.0
                    for role_idx, c, a, b, wn in splits_by_u[u]:
                        wc = w_c if role_idx == 0 else pi[c]
                        wa = w_c if role_idx == 1 else pi[a]
                        wb = w_c if role_idx == 2 else pi[b]
                        b3 += wn * split_3body_bonus(sks[wc], nfs[wc], sks[wa], nfs[wa], sks[wb], nfs[wb])
                    pot[w_c] += w_split * b3

            if greedy:
                w_new = int(np.argmax(pot))
            else:
                top16 = np.argpartition(pot, -16)[-16:]
                logits = (pot[top16] - pot[top16].max()) / temp
                probs = np.exp(np.clip(logits, -30.0, 0.0))
                probs /= probs.sum()
                w_new = int(rng.choice(top16, p=probs))
            pi[u] = w_new
            in_use[w_new] = True

        if (sw_idx + 1) % 5 == 0 or sw_idx == n_sw - 1:
            cur_sc, _ = eval_lipi_objective(pi, G_sem_n, G_swap_n, G_base_n, splits, U_tot, lex, w_sem, w_swap, w_base, w_split)
            for _ in range(80):
                u, v = rng.choice(N, 2, replace=False)
                pi[u], pi[v] = pi[v], pi[u]
                cand_sc, _ = eval_lipi_objective(pi, G_sem_n, G_swap_n, G_base_n, splits, U_tot, lex, w_sem, w_swap, w_base, w_split)
                if cand_sc > cur_sc + 1e-8:
                    cur_sc = cand_sc
                else:
                    pi[u], pi[v] = pi[v], pi[u]
            if cur_sc > best_sc:
                best_sc = cur_sc
                best_pi = pi.copy()
                in_use[:] = False
                in_use[pi] = True

    _, bd = eval_lipi_objective(best_pi, G_sem_n, G_swap_n, G_base_n, splits, U_tot, lex, w_sem, w_swap, w_base, w_split)
    return best_pi, bd


def render_sample_new_readings(sign_prob, lexicons, pi_by_lang, max_samples=15):
    """Render concrete sign-by-sign glosses on complete 3-to-6-sign unseen Mahadevan `new texts`."""
    events_new = json.load(open(os.path.join(SENSE_DIR, "events_new.json")))
    s2i = sign_prob["s2i"]
    samples = []
    seen_txt = set()
    for e in events_new:
        for f in e["faces"]:
            if 3 <= len(f) <= 6 and all(x in s2i for x in f):
                tkey = "-".join(f)
                if tkey in seen_txt:
                    continue
                seen_txt.add(tkey)
                readings = {}
                for lang, pi in pi_by_lang.items():
                    lex = lexicons[lang]
                    words_seq = [f"{lex['hws'][pi[s2i[x]]]} ('{lex['phrases'][pi[s2i[x]]]}')" for x in f]
                    readings[lang] = " · ".join(words_seq)
                samples.append({
                    "site": e.get("site", ""),
                    "kind": e.get("kind", ""),
                    "signs": tkey,
                    "classes": "-".join(sign_prob["cls"][s2i[x]] for x in f),
                    "readings": readings,
                })
                if len(samples) >= max_samples:
                    return samples
    return samples


def main():
    N_DECOY_SOLVES = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    M_EQUAL = 580  # Matches smallest dictionary (`akkadian_wiktionary` ~583 clean unique entries) across all 7 languages!

    part_a = run_fine_slot_and_crosscity_k1_tests(n_shuf=1000)

    log(f"Part B: Running Morpho-Phonetic & Rebus-Locked Redesign Solver across all 7 languages at EQUAL M={M_EQUAL} (N_DECOY={N_DECOY_SOLVES})...")
    with open(os.path.join(DICT_EMB_DIR, "phrases.json"), encoding="utf-8") as f:
        all_phrases = json.load(f)["phrases"]
    phrase_masks = np.load(os.path.join(DICT_EMB_DIR, "phrase_masks.npy"))
    emb_m2v_all = np.load(os.path.join(DICT_EMB_DIR, "emb_m2v.npy"))

    sign_prob = build_sign_problem(n_signs=120)
    ext_priors = build_external_m2v_priors(emb_m2v_all, phrase_masks, all_phrases)
    shuf_perms_1000 = make_sign_shuffles(sign_prob["N"], sign_prob["cls"], sign_prob["band"], n_shuf=1000, seed=9501)
    decoy_perms = make_sign_shuffles(sign_prob["N"], sign_prob["cls"], sign_prob["band"], n_shuf=N_DECOY_SOLVES, seed=8800)

    lexicons_eq = {}
    for lang, dnames in CANDIDATE_LANGS.items():
        lexicons_eq[lang] = load_language_lexicon(lang, dnames, sign_prob, all_phrases, phrase_masks, emb_m2v_all, ext_priors, m_cap=M_EQUAL)

    phon_res = {}
    pi_by_lang = {}
    for lang, lex in lexicons_eq.items():
        t_l = time.time()
        pi_real, bd_real = solve_morphophonetic_qap(
            sign_prob["G_lipi"], sign_prob["G_swap_lipi"], sign_prob["G_base_lipi"],
            sign_prob["lipi_splits"], lex["U_rebus"], lex["U_role"], lex, seed=5050
        )
        pi_by_lang[lang] = pi_real
        zs_real = eval_zeroshot_new(pi_real, sign_prob, lex, shuf_perms_1000)
        save_word_table(pi_real, sign_prob, lex, "morphophon_eq580", os.path.join(OUT_DIR, f"qap_words_{lang}_morphophon.csv"))

        dec_tot, dec_lock, dec_new_sem, dec_hoswap, dec_new_comb = [], [], [], [], []
        for d_i in range(N_DECOY_SOLVES):
            p = decoy_perms[d_i]
            inv_p = np.argsort(p)
            G_lipi_d = sign_prob["G_lipi"][np.ix_(p, p)]
            G_swap_d = sign_prob["G_swap_lipi"][np.ix_(p, p)]
            perm_raw_splits = {
                (int(inv_p[c]), int(inv_p[a]), int(inv_p[b])): frs
                for (c, a, b), frs in sign_prob["lipi_splits_raw"].items()
            }
            splits_d, G_base_d = sign_prob["build_splits_fn"](perm_raw_splits, sign_prob["G_base_raw"])
            pi_d, bd_d = solve_morphophonetic_qap(
                G_lipi_d, G_swap_d, G_base_d,
                splits_d, lex["U_rebus"], lex["U_role"], lex, seed=6000 + d_i
            )
            zs_d = eval_zeroshot_new(pi_d, sign_prob, lex, shuf_perms_1000[:200])
            dec_tot.append(bd_d["total"])
            dec_lock.append(bd_d["unary"] + 0.85 * bd_d["base"] + 0.75 * bd_d["split3"])
            dec_new_sem.append(zs_d["new_sem"]["real"])
            dec_hoswap.append(zs_d["heldout_mah_swaps"]["real"])
            dec_new_comb.append(zs_d["combined_zeroshot"]["real"])

        def cmp_d(rv, dl):
            arr = np.asarray(dl, dtype=np.float64)
            mu, sd = float(arr.mean()), float(arr.std())
            return {
                "real": round(float(rv), 5),
                "decoy_mean": round(mu, 5),
                "decoy_sd": round(sd, 5),
                "z": round(float((rv - mu) / max(sd, 1e-9)), 3),
                "P": round(float((1 + (arr >= rv).sum()) / (len(arr) + 1)), 4),
            }

        real_lock_val = bd_real["unary"] + 0.85 * bd_real["base"] + 0.75 * bd_real["split3"]
        phon_res[lang] = {
            "M_pool": lex["M"],
            "lipi_objective": {k: round(v, 5) for k, v in bd_real.items()},
            "zeroshot_vs_1000_shuffles": zs_real,
            "vs_decoy_lipi_solves": {
                "lipi_total": cmp_d(bd_real["total"], dec_tot),
                "rebus_compound_lock": cmp_d(real_lock_val, dec_lock),
                "zeroshot_new_sem": cmp_d(zs_real["new_sem"]["real"], dec_new_sem),
                "heldout_mah_swaps": cmp_d(zs_real["heldout_mah_swaps"]["real"], dec_hoswap),
                "zeroshot_combined": cmp_d(zs_real["combined_zeroshot"]["real"], dec_new_comb),
            },
            "elapsed_s": round(time.time() - t_l, 1),
        }
        r_lt = phon_res[lang]["vs_decoy_lipi_solves"]["lipi_total"]
        r_lk = phon_res[lang]["vs_decoy_lipi_solves"]["rebus_compound_lock"]
        r_ns = zs_real["new_sem"]
        r_hs = zs_real["heldout_mah_swaps"]
        log(f"[morphophon M={lex['M']}] {lang:11s} ({time.time()-t_l:4.1f}s) | "
            f"Lipi lock vs decoy z={r_lk['z']:+5.2f} (P={r_lk['P']:.3f}) | "
            f"Lipi tot z={r_lt['z']:+5.2f} | "
            f"New sem z={r_ns['z']:+5.2f} (P={r_ns['P']:.3f}) | "
            f"HO-swap z={r_hs['z']:+5.2f} (P={r_hs['P']:.3f})")

    samples = render_sample_new_readings(sign_prob, lexicons_eq, pi_by_lang, max_samples=15)

    out_payload = {
        "part_a_k1_fine_and_crosscity": part_a,
        "part_b_morphophonetic_equal_pool": phon_res,
        "part_c_sample_new_readings": samples,
    }
    with open(os.path.join(OUT_DIR, "eval_redesign_summary.json"), "w", encoding="utf-8") as f:
        json.dump(out_payload, f, indent=2, ensure_ascii=False)
    log("Saved eval_redesign_summary.json and all 7 qap_words_<lang>_morphophon.csv tables!")


if __name__ == "__main__":
    main()
