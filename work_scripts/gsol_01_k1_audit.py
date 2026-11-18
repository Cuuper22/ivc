#!/usr/bin/env python3
"""gsol_01_k1_audit.py -- Step 1: Audit & Retest the K=1 Primary-Sense Lift Lead.

Tests `values_master4.csv` (and pure-dictionary headword senses without human-authored label glosses)
at K=1 and K=2 across:
  1. Bag-of-signs (reproducing sense_onegloss.py) vs. Directional Adjacent-Bigrams (s_i -> s_{i+1}).
  2. Shuffle A (same v2_base class + Lipi face-count band) vs.
     Shuffle B_cat (same class + band + K-clipped category count) vs.
     Shuffle B_nsens (same class + band + full-dictionary sense count).
  3. Scoring metrics:
     - Category PMI (L learned strictly on Lipi; 2-fold CV on Lipi, zero-shot on unseen Mahadevan `new texts`).
     - BGE (`potion-base-32M`, 512d), M2V (`potion-multilingual-128M`, 256d), and Gemma (`senses_emb.npy`, 768d)
       direct cosine AND regularized directional vector bilinear PMI learned strictly on Lipi.
  4. Crucial Rival-Explanation Audit:
     - Fixed-Model (`L(real)` / `W(real)` fit on Lipi `real`, scored on `new texts` `real` vs shuffles `a`)
       VS. Refit-Per-Shuffle (`L(a)` / `W(a)` refit on Lipi for EACH shuffle `a` and scored on `new texts` `a`,
       testing whether cross-corpus recurring sign bigrams create self-consistency lift for ANY decoy assignment!)
       VS. External Non-Circular Prior (`L_ext` / `W_ext` fit on natural sentences `control_texts.json`).
  5. Per-sign & per-directional-bigram attribution on unseen `new texts`:
     identifies exact signs and bigrams driving positive vs. negative K=1 signal.
"""
import os
import sys
import json
import time
import collections
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "work_scripts"))

from sense_core import CATS, NEG, Prob
import sense_common as sc

OUT_DIR = os.path.join(ROOT, "work_data", "gsol")
os.makedirs(OUT_DIR, exist_ok=True)
SENSE_DIR = os.path.join(ROOT, "work_data", "sense")
DICT_EMB_DIR = "/tmp/dict_emb"

T0 = time.time()
def log(*a):
    print(f"[{time.time() - T0:6.1f}s] [gsol_01]", *a, flush=True)


def load_embeddings_for_phrases(target_phrases):
    """Map every phrase in target_phrases to centered+normalized BGE (512d) and M2V (256d) vectors."""
    with open(os.path.join(DICT_EMB_DIR, "phrases.json"), encoding="utf-8") as f:
        pdata = json.load(f)
    all_phrases = pdata["phrases"]
    p2i = {p: i for i, p in enumerate(all_phrases)}
    emb_bge_all = np.load(os.path.join(DICT_EMB_DIR, "emb_bge.npy"))
    emb_m2v_all = np.load(os.path.join(DICT_EMB_DIR, "emb_m2v.npy"))

    missing = sorted({p for p in target_phrases if p not in p2i})
    extra_bge, extra_m2v = {}, {}
    if missing:
        log(f"Encoding {len(missing)} label-only phrases not in /tmp/dict_emb/phrases.json...")
        from model2vec import StaticModel
        m_bge = StaticModel.from_pretrained("minishlab/potion-base-32M")
        m_m2v = StaticModel.from_pretrained("minishlab/potion-multilingual-128M")
        # Approximate global mean from a 20k subsample of raw encodes to match centering
        idx_sub = np.linspace(0, len(all_phrases) - 1, 10000, dtype=int)
        sub_phrases = [all_phrases[i] for i in idx_sub]
        mu_bge = m_bge.encode(sub_phrases).astype(np.float32).mean(axis=0, keepdims=True)
        mu_m2v = m_m2v.encode(sub_phrases).astype(np.float32).mean(axis=0, keepdims=True)

        vb = m_bge.encode(missing).astype(np.float32) - mu_bge
        vb /= (np.linalg.norm(vb, axis=1, keepdims=True) + 1e-8)
        vm = m_m2v.encode(missing).astype(np.float32) - mu_m2v
        vm /= (np.linalg.norm(vm, axis=1, keepdims=True) + 1e-8)
        for p, bvec, mvec in zip(missing, vb, vm):
            extra_bge[p] = bvec
            extra_m2v[p] = mvec

    out_bge = np.zeros((len(target_phrases), emb_bge_all.shape[1]), dtype=np.float32)
    out_m2v = np.zeros((len(target_phrases), emb_m2v_all.shape[1]), dtype=np.float32)
    for idx, p in enumerate(target_phrases):
        if p in p2i:
            out_bge[idx] = emb_bge_all[p2i[p]].astype(np.float32)
            out_m2v[idx] = emb_m2v_all[p2i[p]].astype(np.float32)
        else:
            out_bge[idx] = extra_bge[p]
            out_m2v[idx] = extra_m2v[p]
    return out_bge, out_m2v


def build_directional_corpus(events_lipi, events_new, sidx, seed=20261117):
    """Extract directional adjacent sign bigrams (u -> v) per face, weighted 1 per physical object event."""
    rng = np.random.default_rng(seed)

    def extract(events, mode):
        # Returns list of faces: (fold, weight, [(u, v), ...])
        records = []
        n_ev = 0
        for e in events:
            fold = int(rng.integers(0, 2)) if mode == "cross" else 2
            valid_faces = []
            for f in e["faces"]:
                # Adjacent tokens in raw face `f` only (do NOT bridge across '000' or unlabelled signs!)
                pairs = []
                for a, b in zip(f, f[1:]):
                    if a in sidx and b in sidx and a != b:
                        pairs.append((sidx[a], sidx[b]))
                if pairs:
                    valid_faces.append(pairs)
            if not valid_faces:
                continue
            n_ev += 1
            w = 1.0 / len(valid_faces)
            for pairs in valid_faces:
                records.append((fold, w, pairs))
        return records, n_ev

    rec_lipi, nev_lipi = extract(events_lipi, "cross")
    rec_new, nev_new = extract(events_new, "new")
    log(f"Directional adjacent-bigram scorable events: Lipi={nev_lipi} ({len(rec_lipi)} faces), New={nev_new} ({len(rec_new)} faces)")
    return rec_lipi + rec_new


def make_shuffles(real_w, cls_arr, band_arr, aux_count_arr, n_shuf=1000, seed=4242, matched=False, block=3):
    """Generate N permutations of `real_w` within (cls, band), optionally matching `aux_count_arr`."""
    rng = np.random.default_rng(seed)
    U = len(real_w)
    cells = collections.defaultdict(list)
    for u in range(U):
        cells[(cls_arr[u], band_arr[u])].append(u)

    shufs = np.zeros((n_shuf, U), dtype=np.int32)
    for s in range(n_shuf):
        asg = real_w.copy()
        for _, us in cells.items():
            us = np.array(us, dtype=np.int32)
            if len(us) < 2:
                continue
            if not matched:
                asg[us] = real_w[us][rng.permutation(len(us))]
            else:
                key = aux_count_arr[real_w[us]] + rng.random(len(us)) * 0.25
                us_ord = us[np.argsort(key)]
                n = len(us_ord)
                off = int(rng.integers(0, block))
                bounds = [0] + list(range(off if off > 0 else block, n, block)) + [n]
                bounds = sorted(set(b for b in bounds if 0 <= b <= n))
                if len(bounds) > 2 and bounds[-1] - bounds[-2] < 2:
                    bounds.pop(-2)
                for a, b in zip(bounds[:-1], bounds[1:]):
                    blk = us_ord[a:b]
                    asg[blk] = real_w[blk][rng.permutation(len(blk))]
        shufs[s] = asg
    return shufs


def pack_directional_edges(records, U):
    """Aggregate directional bigrams per fold into a fast edge table + per-face normalization."""
    # Wait: in sense_core.py, text score is mean over valid pairs on the face, weighted by face event weight!
    # Notice: if a face has M valid pairs (with w_u != w_v), each pair on that face gets weight `w_face / M_valid`!
    # Because `w_u != w_v` rarely changes (almost all distinct signs have distinct words, except ~35 synonym pairs out of 16,800!),
    # let's compute exact face-level scores vectorized!
    max_p = max(len(r[2]) for r in records)
    T = len(records)
    folds = np.array([r[0] for r in records], dtype=np.int32)
    tw = np.array([r[1] for r in records], dtype=np.float64)
    U1 = np.full((T, max_p), -1, dtype=np.int32)
    U2 = np.full((T, max_p), -1, dtype=np.int32)
    for t, (_, _, pairs) in enumerate(records):
        for k, (u, v) in enumerate(pairs):
            U1[t, k] = u
            U2[t, k] = v
    valid_edge = (U1 >= 0)
    return folds, tw, U1, U2, valid_edge


def fit_dir_cat_lift(U1, U2, valid_edge, tw, sel_mask, asg, word_cats):
    """Fit directional 13x13 category log-lift matrix on `sel_mask` faces under assignment `asg`.
    `word_cats`: [W, 13] bool/float."""
    idx = np.where(sel_mask)[0]
    u1 = U1[idx]
    u2 = U2[idx]
    ve = valid_edge[idx]
    w_face = tw[idx]

    w1 = np.where(ve, asg[np.maximum(u1, 0)], -1)
    w2 = np.where(ve, asg[np.maximum(u2, 0)], -2)
    ok = ve & (w1 != w2)
    # Weight each valid bigram on a face equally so each face has total weight `w_face` (or raw bigram weight — let's match sense_core!)
    cnt = ok.sum(axis=1, keepdims=True)
    ew = np.where(ok, w_face[:, None] / np.maximum(cnt, 1), 0.0)

    flat_ok = ok.ravel()
    fw1 = w1.ravel()[flat_ok]
    fw2 = w2.ravel()[flat_ok]
    few = ew.ravel()[flat_ok]

    c1 = word_cats[fw1]  # [E, 13]
    c2 = word_cats[fw2]  # [E, 13]
    n_mat = (c1 * few[:, None]).T @ c2  # [13, 13]
    tot = float(few.sum())
    p1 = (c1 * few[:, None]).sum(axis=0) / max(tot, 1e-9)
    p2 = (c2 * few[:, None]).sum(axis=0) / max(tot, 1e-9)
    ex = tot * np.outer(p1, p2)
    return np.log((n_mat + 0.5) / (ex + 0.5)).astype(np.float32)


def word_pair_matrix_from_cat_lift(B_ws, valid_ws, Lm):
    """Given B_ws [W, S, 13] bool, valid_ws [W, S] bool, and directional Lm [13, 13],
    compute directional word-pair score M[w1, w2] = max_{s1, s2} max_{c1 in s1, c2 in s2} Lm[c1, c2]
    (symmetrized over s1/s2 sense choice for K<=2)."""
    W, S, _ = B_ws.shape
    Bf = B_ws.reshape(W * S, 13)
    A1 = np.full((W * S, 13), -np.inf, dtype=np.float32)
    for c1 in range(13):
        m = Bf[:, c1]
        if m.any():
            A1[m] = np.maximum(A1[m], Lm[c1][None, :])
    R = np.full((W * S, W * S), -np.inf, dtype=np.float32)
    for c2 in range(13):
        m = Bf[:, c2]
        if m.any():
            R[:, m] = np.maximum(R[:, m], A1[:, c2][:, None])
    R[~np.isfinite(R)] = 0.0
    R = R.reshape(W, S, W, S)
    R[~valid_ws, :, :] = NEG
    R[:, :, ~valid_ws] = NEG
    return R.max(axis=(1, 3))  # [W, W]


def fit_dir_vec_bilinear(U1, U2, valid_edge, tw, sel_mask, asg, W_emb_primary, ridge=0.25):
    """Fit regularized directional bilinear PMI matrix on primary sense embeddings `W_emb_primary` [W, D].
    Approximates RKHS log-density-ratio: (Sigma_L + ridge*I)^{-1} (E_pos[x y^T] - mu_L mu_R^T) (Sigma_R + ridge*I)^{-1}."""
    idx = np.where(sel_mask)[0]
    u1 = U1[idx]
    u2 = U2[idx]
    ve = valid_edge[idx]
    w_face = tw[idx]

    w1 = np.where(ve, asg[np.maximum(u1, 0)], -1)
    w2 = np.where(ve, asg[np.maximum(u2, 0)], -2)
    ok = ve & (w1 != w2)
    cnt = ok.sum(axis=1, keepdims=True)
    ew = np.where(ok, w_face[:, None] / np.maximum(cnt, 1), 0.0)

    flat_ok = ok.ravel()
    fw1 = w1.ravel()[flat_ok]
    fw2 = w2.ravel()[flat_ok]
    few = ew.ravel()[flat_ok]
    tot = float(few.sum())
    few_norm = few / max(tot, 1e-9)

    X = W_emb_primary[fw1]  # [E, D]
    Y = W_emb_primary[fw2]  # [E, D]
    mu_x = (X * few_norm[:, None]).sum(axis=0, keepdims=True)
    mu_y = (Y * few_norm[:, None]).sum(axis=0, keepdims=True)
    Xc = X - mu_x
    Yc = Y - mu_y

    C_xy = (Xc * few_norm[:, None]).T @ Yc  # [D, D]
    S_xx = (Xc * few_norm[:, None]).T @ Xc + ridge * np.eye(X.shape[1], dtype=np.float32)
    S_yy = (Yc * few_norm[:, None]).T @ Yc + ridge * np.eye(Y.shape[1], dtype=np.float32)
    B_mat = np.linalg.solve(S_xx, np.linalg.solve(S_yy, C_xy.T).T).astype(np.float32)
    return B_mat, mu_x.astype(np.float32), mu_y.astype(np.float32)


def word_pair_matrix_from_vec(E_ws, valid_ws, B_mat=None, mu_x=None, mu_y=None):
    """Compute [W, W] max_{s1, s2} score from sense embeddings E_ws [W, S, D].
    If B_mat is None: direct cosine similarity. Else: centered bilinear score."""
    W, S, D = E_ws.shape
    V = E_ws.reshape(W * S, D)
    if B_mat is None:
        R = V @ V.T
    else:
        Vx = V - mu_x
        Vy = V - mu_y
        R = (Vx @ B_mat) @ Vy.T
    R = R.reshape(W, S, W, S).astype(np.float32)
    R[~valid_ws, :, :] = NEG
    R[:, :, ~valid_ws] = NEG
    return R.max(axis=(1, 3))


def score_assignments_dir(M_by_fold, folds, tw, U1, U2, valid_edge, asgs, grp_mask):
    """Vectorized directional score for `asgs` ([N, U] or [U]) on faces where `grp_mask` is True."""
    single = (asgs.ndim == 1)
    if single:
        asgs = asgs[None, :]
    N = asgs.shape[0]
    T = len(tw)
    face_scores = np.zeros((N, T), dtype=np.float64)
    face_has = np.zeros((N, T), dtype=bool)

    active_folds = sorted(set(folds[grp_mask]))
    for f in active_folds:
        f_idx = np.where((folds == f) & grp_mask)[0]
        if len(f_idx) == 0:
            continue
        M = M_by_fold[f]
        u1 = U1[f_idx]       # [Tf, P]
        u2 = U2[f_idx]       # [Tf, P]
        ve = valid_edge[f_idx]  # [Tf, P]

        # Map [N, Tf, P]
        w1 = asgs[:, np.maximum(u1, 0)]
        w2 = asgs[:, np.maximum(u2, 0)]
        ok = ve[None, :, :] & (w1 != w2)
        vals = M[w1, w2]
        cnt = ok.sum(axis=2)
        fsc = np.where(cnt > 0, (vals * ok).sum(axis=2) / np.maximum(cnt, 1), 0.0)
        face_scores[:, f_idx] = fsc
        face_has[:, f_idx] = (cnt > 0)

    w = tw[None, :] * face_has * grp_mask[None, :]
    totals = (face_scores * w).sum(axis=1) / np.maximum(w.sum(axis=1), 1e-9)
    return float(totals[0]) if single else totals


def build_external_priors(bge_model_or_none=None):
    """Build external category lift L_ext and BGE/M2V bilinear matrices from `control_texts.json`
    (1,519 real natural sentences, WordNet primary sense) so zero Lipi sign labels are touched!"""
    ctrl_words = pd.read_csv(os.path.join(SENSE_DIR, "control_words.csv")).fillna("")
    ctrl_senses = pd.read_csv(os.path.join(SENSE_DIR, "control_senses.csv")).fillna("")
    ctrl_texts = json.load(open(os.path.join(SENSE_DIR, "control_texts.json")))

    # Keep primary sense (sense == 0) of each control word
    s0 = ctrl_senses[ctrl_senses.sense == 0].copy()
    w2idx = {w: i for i, w in enumerate(ctrl_words.word)}
    W_c = len(ctrl_words)
    wc = np.zeros((W_c, 13), dtype=np.float32)
    phrases = [""] * W_c
    for r in s0.itertuples():
        if r.word in w2idx:
            i = w2idx[r.word]
            phrases[i] = r.phrase
            for c in str(r.cats).split("|"):
                if c in CATS:
                    wc[i, CATS.index(c)] = 1.0

    # Ordered adjacent content-word pairs in control sentences
    u1_list, u2_list = [], []
    for s in ctrl_texts:
        # control_texts.json stores integer word indices or strings? Let's handle both
        idxs = [x if isinstance(x, int) else w2idx.get(x, -1) for x in s]
        idxs = [x for x in idxs if 0 <= x < W_c]
        for a, b in zip(idxs, idxs[1:]):
            if a != b:
                u1_list.append(a)
                u2_list.append(b)
    u1 = np.array(u1_list, dtype=np.int32)
    u2 = np.array(u2_list, dtype=np.int32)
    c1 = wc[u1]
    c2 = wc[u2]
    n_mat = c1.T @ c2
    tot = float(len(u1))
    p1 = c1.sum(axis=0) / max(tot, 1e-9)
    p2 = c2.sum(axis=0) / max(tot, 1e-9)
    L_ext = np.log((n_mat + 0.5) / (tot * np.outer(p1, p2) + 0.5)).astype(np.float32)

    ebge, em2v = load_embeddings_for_phrases(phrases)
    def fit_bilin_pairs(emb, ridge=0.5):
        X, Y = emb[u1], emb[u2]
        mx, my = X.mean(0, keepdims=True), Y.mean(0, keepdims=True)
        Xc, Yc = X - mx, Y - my
        N = float(len(u1))
        C = (Xc.T @ Yc) / N
        Sx = (Xc.T @ Xc) / N + ridge * np.eye(emb.shape[1], dtype=np.float32)
        Sy = (Yc.T @ Yc) / N + ridge * np.eye(emb.shape[1], dtype=np.float32)
        B = np.linalg.solve(Sx, np.linalg.solve(Sy, C.T).T).astype(np.float32)
        return B, mx.astype(np.float32), my.astype(np.float32)

    B_bge_ext, mx_bge, my_bge = fit_bilin_pairs(ebge)
    B_m2v_ext, mx_m2v, my_m2v = fit_bilin_pairs(em2v)
    log(f"Built external priors from control_texts.json ({len(ctrl_texts)} sentences, {len(u1)} ordered bigrams)")
    return L_ext, (B_bge_ext, mx_bge, my_bge), (B_m2v_ext, mx_m2v, my_m2v)


def summarize_vs_null(real_val, null_arr):
    null_arr = np.asarray(null_arr, dtype=np.float64)
    mu = float(null_arr.mean())
    sd = float(null_arr.std())
    p = float((1 + (null_arr >= real_val).sum()) / (len(null_arr) + 1))
    z = float((real_val - mu) / max(sd, 1e-12))
    return {"real": round(float(real_val), 6), "mean": round(mu, 6), "sd": round(sd, 6), "z": round(z, 3), "P": round(p, 4)}


def main():
    N_SHUF = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    log(f"Starting Step 1 K=1 / K=2 Audit with N_SHUF={N_SHUF}...")

    S = pd.read_csv(os.path.join(SENSE_DIR, "signs.csv"), dtype={"sign": str}).fillna("")
    SS = pd.read_csv(os.path.join(SENSE_DIR, "senses.csv")).fillna("")
    EM_gemma = np.load(os.path.join(SENSE_DIR, "senses_emb.npy")).astype(np.float32)

    # Also build BGE and M2V embeddings for every row of SS
    SS_bge, SS_m2v = load_embeddings_for_phrases(list(SS.phrase))

    # Also build Pure-Dictionary senses (excluding values_master4 hand-written English glosses!)
    tam_df = pd.read_csv(os.path.join(DICT_EMB_DIR, "tamil_all_senses.csv"), dtype={"eid": str, "hw": str, "norm": str}).fillna("")
    with open(os.path.join(DICT_EMB_DIR, "phrases.json"), encoding="utf-8") as f:
        all_dict_phrases = json.load(f)["phrases"]
    phrase_masks = np.load(os.path.join(DICT_EMB_DIR, "phrase_masks.npy"))
    emb_bge_dict = np.load(os.path.join(DICT_EMB_DIR, "emb_bge.npy"))
    emb_m2v_dict = np.load(os.path.join(DICT_EMB_DIR, "emb_m2v.npy"))

    tam_df["wkey"] = tam_df["hw"].map(sc.word_key)
    tam_by_wk = tam_df.groupby("wkey")

    events_lipi = json.load(open(os.path.join(SENSE_DIR, "events_lipi.json")))
    events_new = json.load(open(os.path.join(SENSE_DIR, "events_new.json")))
    sidx = {s: i for i, s in enumerate(S.sign)}

    # Unordered bag-of-signs texts (exact sense_onegloss.py setup)
    rng0 = np.random.default_rng(20261117)
    def make_bag_texts(events, mode):
        agg = collections.defaultdict(float)
        for e in events:
            fold = int(rng0.integers(0, 2)) if mode == "cross" else 2
            faces = []
            for f in e["faces"]:
                us = list(dict.fromkeys(sidx[x] for x in f if x in sidx))
                if len(us) >= 2 and len({S.word.iloc[u] for u in us}) >= 2:
                    faces.append(us)
            if not faces:
                continue
            for us in faces:
                agg[(fold, tuple(sorted(us)))] += 1.0 / len(faces)
        return agg

    A1 = make_bag_texts(events_lipi, "cross")
    A2 = make_bag_texts(events_new, "new")
    bag_keys = list(A1) + list(A2)
    bag_texts = [list(k[1]) for k in bag_keys]
    bag_tw = [(A1.get(k) or A2.get(k)) for k in bag_keys]
    bag_tf = [k[0] for k in bag_keys]

    # Directional adjacent-bigram corpus
    dir_records = build_directional_corpus(events_lipi, events_new, sidx, seed=20261117)
    folds, tw, U1, U2, valid_edge = pack_directional_edges(dir_records, len(S))
    grp_lipi = (folds < 2)
    grp_new = (folds == 2)
    fold0 = (folds == 0)
    fold1 = (folds == 1)

    L_ext, ext_bge, ext_m2v = build_external_priors()

    words = sorted(S.word.unique())
    widx = {w: i for i, w in enumerate(words)}
    W_cnt = len(words)
    real_w = np.array([widx[w] for w in S.word], dtype=np.int32)
    cls_arr = np.array(list(S.cls))
    band_arr = np.array(list(S.band))
    full_nsens_by_w = np.zeros(W_cnt, dtype=np.float64)
    for w, g in SS.groupby("word", sort=False):
        full_nsens_by_w[widx[w]] = len(g)

    results = {"bag_of_signs": {}, "directional_bigrams": {}, "rival_refit_audit": {}, "pure_dict_senses": {}}

    for K in (1, 2):
        log(f"--- Evaluating K={K} (values_master4 + dict senses) ---")
        senses_k = {}
        emb_g_k, emb_b_k, emb_m_k = {}, {}, {}
        B_ws = np.zeros((W_cnt, K, 13), dtype=bool)
        valid_ws = np.zeros((W_cnt, K), dtype=bool)
        E_bge = np.zeros((W_cnt, K, SS_bge.shape[1]), dtype=np.float32)
        E_m2v = np.zeros((W_cnt, K, SS_m2v.shape[1]), dtype=np.float32)
        E_gem = np.zeros((W_cnt, K, EM_gemma.shape[1]), dtype=np.float32)

        for w, g in SS.groupby("word", sort=False):
            wi = widx[w]
            sub = g.iloc[:K]
            senses_k[w] = [(r.phrase, [c for c in r.cats.split("|") if c]) for r in sub.itertuples()]
            emb_g_k[w] = EM_gemma[sub.index.values]
            emb_b_k[w] = SS_bge[sub.index.values]
            emb_m_k[w] = SS_m2v[sub.index.values]
            for s_i, (_, cs) in enumerate(senses_k[w]):
                valid_ws[wi, s_i] = True
                for c in cs:
                    B_ws[wi, s_i, CATS.index(c)] = True
            E_bge[wi, :len(sub)] = emb_b_k[w]
            E_m2v[wi, :len(sub)] = emb_m_k[w]
            E_gem[wi, :len(sub)] = emb_g_k[w]

        # Center + renormalize E_gem on active senses (matching sense_core)
        gem_mu = E_gem[valid_ws].mean(axis=0)
        E_gem = E_gem - gem_mu
        E_gem /= (np.linalg.norm(E_gem, axis=2, keepdims=True) + 1e-9)
        E_gem[~valid_ws] = 0.0

        word_cats = B_ws.any(axis=1).astype(np.float32)  # [W, 13]
        cat_count_by_w = word_cats.sum(axis=1)  # number of categories triggered at cap K

        # Pre-generate 3 shuffle sets:
        # A: class + band
        # B_cat: class + band + K-sense category count (0 vs 1 vs 2+)
        # B_nsens: class + band + full-dictionary sense count
        shuf_A = make_shuffles(real_w, cls_arr, band_arr, cat_count_by_w, N_SHUF, seed=4242, matched=False)
        shuf_Bcat = make_shuffles(real_w, cls_arr, band_arr, cat_count_by_w, N_SHUF, seed=5252, matched=True)
        shuf_Bns = make_shuffles(real_w, cls_arr, band_arr, full_nsens_by_w, N_SHUF, seed=6262, matched=True)

        # 1. Bag-of-signs check (exact sense_onegloss.py + Shuffle B_cat + Shuffle B_nsens)
        P_bag = Prob(words, senses_k, emb_g_k, list(S.sign), list(S.word), list(S.cls), list(S.band),
                     bag_texts, bag_tw, bag_tf, lmax=10, name=f"bag_K{K}")
        P_bag.build(("ov", "lift", "cos"))
        grp_bag_new = (P_bag.tfold == 2).astype(float)
        grp_bag_lipi = (P_bag.tfold < 2).astype(float)

        bag_res = {}
        for ver in ("lift", "cos", "ov"):
            f_r, ok_r = P_bag.fits(P_bag.real, ver)
            r_new = P_bag.total(f_r, ok_r, grp_bag_new)["all"]
            r_lipi = P_bag.total(f_r, ok_r, grp_bag_lipi)["all"]
            rec = {}
            for sname, s_arr in (("A", shuf_A), ("B_cat", shuf_Bcat), ("B_nsens", shuf_Bns)):
                vals_new, vals_lipi = [], []
                for i in range(N_SHUF):
                    fi, oki = P_bag.fits(s_arr[i], ver)
                    vals_new.append(P_bag.total(fi, oki, grp_bag_new)["all"])
                    vals_lipi.append(P_bag.total(fi, oki, grp_bag_lipi)["all"])
                rec[f"{sname}_new"] = summarize_vs_null(r_new, vals_new)
                rec[f"{sname}_lipi"] = summarize_vs_null(r_lipi, vals_lipi)
            bag_res[ver] = rec
        results["bag_of_signs"][f"K={K}"] = bag_res
        log(f"Bag-of-signs K={K} lift new: A z={bag_res['lift']['A_new']['z']} | B_cat z={bag_res['lift']['B_cat_new']['z']} | B_nsens z={bag_res['lift']['B_nsens_new']['z']}")

        # 2. Directional Adjacent-Bigram Models (learned strictly on Lipi -> zero-shot on New, 2-fold CV on Lipi)
        L_f0 = fit_dir_cat_lift(U1, U2, valid_edge, tw, fold1, real_w, word_cats)
        L_f1 = fit_dir_cat_lift(U1, U2, valid_edge, tw, fold0, real_w, word_cats)
        L_all_lipi = fit_dir_cat_lift(U1, U2, valid_edge, tw, grp_lipi, real_w, word_cats)

        M_cat_dir = {
            0: word_pair_matrix_from_cat_lift(B_ws, valid_ws, L_f0),
            1: word_pair_matrix_from_cat_lift(B_ws, valid_ws, L_f1),
            2: word_pair_matrix_from_cat_lift(B_ws, valid_ws, L_all_lipi),
        }
        M_cat_ext = {f: word_pair_matrix_from_cat_lift(B_ws, valid_ws, L_ext) for f in (0, 1, 2)}

        # Vector bilinear & cosine models (BGE 512d, M2V 256d, Gemma 768d)
        vec_models = {}
        for vname, E_arr, ext_pack in (("bge", E_bge, ext_bge), ("m2v", E_m2v, ext_m2v), ("gemma", E_gem, None)):
            # Direct cosine
            M_cos_0 = word_pair_matrix_from_vec(E_arr, valid_ws, None)
            vec_models[f"{vname}_cos"] = {0: M_cos_0, 1: M_cos_0, 2: M_cos_0}

            # Bilinear PMI learned strictly on Lipi
            B0, mx0, my0 = fit_dir_vec_bilinear(U1, U2, valid_edge, tw, fold1, real_w, E_arr[:, 0, :], ridge=0.25)
            B1, mx1, my1 = fit_dir_vec_bilinear(U1, U2, valid_edge, tw, fold0, real_w, E_arr[:, 0, :], ridge=0.25)
            B2, mx2, my2 = fit_dir_vec_bilinear(U1, U2, valid_edge, tw, grp_lipi, real_w, E_arr[:, 0, :], ridge=0.25)
            vec_models[f"{vname}_bilin_lipi"] = {
                0: word_pair_matrix_from_vec(E_arr, valid_ws, B0, mx0, my0),
                1: word_pair_matrix_from_vec(E_arr, valid_ws, B1, mx1, my1),
                2: word_pair_matrix_from_vec(E_arr, valid_ws, B2, mx2, my2),
            }
            if ext_pack is not None:
                Be, mxe, mye = ext_pack
                Me = word_pair_matrix_from_vec(E_arr, valid_ws, Be, mxe, mye)
                vec_models[f"{vname}_bilin_ext"] = {0: Me, 1: Me, 2: Me}

        all_dir_models = {"dir_cat_pmi_lipi": M_cat_dir, "dir_cat_pmi_ext": M_cat_ext, **vec_models}
        dir_res = {}
        for mname, M_dict in all_dir_models.items():
            r_new = score_assignments_dir(M_dict, folds, tw, U1, U2, valid_edge, real_w, grp_new)
            r_lipi = score_assignments_dir(M_dict, folds, tw, U1, U2, valid_edge, real_w, grp_lipi)
            rec = {}
            for sname, s_arr in (("A", shuf_A), ("B_cat", shuf_Bcat), ("B_nsens", shuf_Bns)):
                s_new = score_assignments_dir(M_dict, folds, tw, U1, U2, valid_edge, s_arr, grp_new)
                s_lipi = score_assignments_dir(M_dict, folds, tw, U1, U2, valid_edge, s_arr, grp_lipi)
                rec[f"{sname}_new"] = summarize_vs_null(r_new, s_new)
                rec[f"{sname}_lipi"] = summarize_vs_null(r_lipi, s_lipi)
            dir_res[mname] = rec
            log(f"Dir K={K} {mname:20s} | New A z={rec['A_new']['z']:+6.2f} (P={rec['A_new']['P']:.3f}) | B_cat z={rec['B_cat_new']['z']:+6.2f} (P={rec['B_cat_new']['P']:.3f})")
        results["directional_bigrams"][f"K={K}"] = dir_res

        # 3. Crucial Rival-Explanation Audit (Refit L(a) and W(a) on Lipi for EVERY shuffle `a`, score `a` on New!)
        # Exact QR-subspace projection reduces 512x512 linear solve to rank-W (~119x119) with zero loss of precision!
        rival_res = {}
        r_cat_self = score_assignments_dir(M_cat_dir, folds, tw, U1, U2, valid_edge, real_w, grp_new)
        r_bge_self = score_assignments_dir(vec_models["bge_bilin_lipi"], folds, tw, U1, U2, valid_edge, real_w, grp_new)

        Q_sub, _ = np.linalg.qr(E_bge[:, 0, :].T, mode="reduced")  # [512, r], r <= 119
        E_bge_sub_p1 = (E_bge[:, 0, :] @ Q_sub).astype(np.float32)  # [W, r]
        E_bge_sub_ws = (E_bge.reshape(-1, E_bge.shape[2]) @ Q_sub).reshape(W_cnt, K, -1).astype(np.float32)

        for sname, s_arr in (("A", shuf_A), ("B_cat", shuf_Bcat)):
            refit_cat_new = np.zeros(N_SHUF, dtype=np.float64)
            refit_bge_new = np.zeros(N_SHUF, dtype=np.float64)
            for i in range(N_SHUF):
                ai = s_arr[i]
                Li = fit_dir_cat_lift(U1, U2, valid_edge, tw, grp_lipi, ai, word_cats)
                Mi = {2: word_pair_matrix_from_cat_lift(B_ws, valid_ws, Li)}
                refit_cat_new[i] = score_assignments_dir(Mi, folds, tw, U1, U2, valid_edge, ai, grp_new)

                Bi, mxi, myi = fit_dir_vec_bilinear(U1, U2, valid_edge, tw, grp_lipi, ai, E_bge_sub_p1, ridge=0.25)
                Mbi = {2: word_pair_matrix_from_vec(E_bge_sub_ws, valid_ws, Bi, mxi, myi)}
                refit_bge_new[i] = score_assignments_dir(Mbi, folds, tw, U1, U2, valid_edge, ai, grp_new)
            rival_res[f"dir_cat_pmi_refit_{sname}_new"] = summarize_vs_null(r_cat_self, refit_cat_new)
            rival_res[f"bge_bilin_refit_{sname}_new"] = summarize_vs_null(r_bge_self, refit_bge_new)
        results["rival_refit_audit"][f"K={K}"] = rival_res
        log(f"Rival Refit Audit K={K} (each decoy learns its own Lipi model -> New): "
            f"cat B_cat z={rival_res['dir_cat_pmi_refit_B_cat_new']['z']:+6.2f} (P={rival_res['dir_cat_pmi_refit_B_cat_new']['P']:.3f}) | "
            f"bge B_cat z={rival_res['bge_bilin_refit_B_cat_new']['z']:+6.2f} (P={rival_res['bge_bilin_refit_B_cat_new']['P']:.3f})")

        # 4. Pure-Dictionary Primary-Sense Check (dedr_tamil + tamil_wiktionary ONLY, dropping human-written values_master4 glosses)
        B_pd = np.zeros((W_cnt, K, 13), dtype=bool)
        val_pd = np.zeros((W_cnt, K), dtype=bool)
        E_pd = np.zeros((W_cnt, K, emb_bge_dict.shape[1]), dtype=np.float32)
        for w in words:
            wi = widx[w]
            if w in tam_by_wk.groups:
                pids = list(dict.fromkeys(tam_by_wk.get_group(w)["pid"].tolist()))[:K]
                for s_i, pid in enumerate(pids):
                    val_pd[wi, s_i] = True
                    msk = int(phrase_masks[pid])
                    for c_i in range(13):
                        if msk & (1 << c_i):
                            B_pd[wi, s_i, c_i] = True
                    E_pd[wi, s_i] = emb_bge_dict[pid].astype(np.float32)
            else:
                # Fallback to SS only for words absent from dict (~10 compound star words)
                val_pd[wi] = valid_ws[wi]
                B_pd[wi] = B_ws[wi]
                E_pd[wi] = E_bge[wi]
        wc_pd = B_pd.any(axis=1).astype(np.float32)
        L_pd = fit_dir_cat_lift(U1, U2, valid_edge, tw, grp_lipi, real_w, wc_pd)
        M_pd = {2: word_pair_matrix_from_cat_lift(B_pd, val_pd, L_pd)}
        r_pd = score_assignments_dir(M_pd, folds, tw, U1, U2, valid_edge, real_w, grp_new)
        s_pd_A = score_assignments_dir(M_pd, folds, tw, U1, U2, valid_edge, shuf_A, grp_new)
        shuf_pd_B = make_shuffles(real_w, cls_arr, band_arr, wc_pd.sum(axis=1), N_SHUF, seed=7272, matched=True)
        s_pd_B = score_assignments_dir(M_pd, folds, tw, U1, U2, valid_edge, shuf_pd_B, grp_new)
        # Also refit per shuffle for pure-dict
        refit_pd_B = np.zeros(N_SHUF, dtype=np.float64)
        for i in range(N_SHUF):
            ai = shuf_pd_B[i]
            Li = fit_dir_cat_lift(U1, U2, valid_edge, tw, grp_lipi, ai, wc_pd)
            refit_pd_B[i] = score_assignments_dir({2: word_pair_matrix_from_cat_lift(B_pd, val_pd, Li)}, folds, tw, U1, U2, valid_edge, ai, grp_new)
        results["pure_dict_senses"][f"K={K}"] = {
            "fixed_A_new": summarize_vs_null(r_pd, s_pd_A),
            "fixed_B_cat_new": summarize_vs_null(r_pd, s_pd_B),
            "refit_B_cat_new": summarize_vs_null(r_pd, refit_pd_B),
        }
        log(f"Pure-Dict K={K} New: fixed A z={results['pure_dict_senses'][f'K={K}']['fixed_A_new']['z']:+6.2f} | "
            f"fixed B_cat z={results['pure_dict_senses'][f'K={K}']['fixed_B_cat_new']['z']:+6.2f} | "
            f"refit B_cat z={results['pure_dict_senses'][f'K={K}']['refit_B_cat_new']['z']:+6.2f}")

        # 5. Step 1(b): Detailed Per-Sign & Per-Directional-Bigram Attribution at K=1 on unseen `new texts`
        if K == 1:
            log("Computing per-sign and per-bigram K=1 attribution on unseen Mahadevan `new texts`...")
            M_fix = M_cat_dir[2]
            M_ext_mat = M_cat_ext[2]
            M_bge_cos = vec_models["bge_cos"][2]

            # Gather all valid directional edges on `new texts` with their face-normalized weights
            new_idx = np.where(grp_new)[0]
            bg_weights = collections.defaultdict(float)
            for t in new_idx:
                pairs = [(int(U1[t, k]), int(U2[t, k])) for k in range(U1.shape[1])
                         if valid_edge[t, k] and real_w[U1[t, k]] != real_w[U2[t, k]]]
                if not pairs:
                    continue
                ew = float(tw[t]) / len(pairs)
                for u, v in pairs:
                    bg_weights[(u, v)] += ew

            tot_new_w = sum(bg_weights.values())
            bigram_rows = []
            sign_gain_fix = collections.defaultdict(float)
            sign_gain_ext = collections.defaultdict(float)
            sign_gain_cos = collections.defaultdict(float)
            sign_w = collections.defaultdict(float)

            for (u, v), bw in bg_weights.items():
                wu_r, wv_r = real_w[u], real_w[v]
                wu_s, wv_s = shuf_Bcat[:, u], shuf_Bcat[:, v]
                valid_s = (wu_s != wv_s)
                if not valid_s.any():
                    continue

                # Fixed Lipi category PMI
                r_fix = float(M_fix[wu_r, wv_r])
                s_fix = M_fix[wu_s[valid_s], wv_s[valid_s]]
                d_fix = bw * (r_fix - float(s_fix.mean()))

                # External natural-sentence category PMI
                r_ext = float(M_ext_mat[wu_r, wv_r])
                s_ext = M_ext_mat[wu_s[valid_s], wv_s[valid_s]]
                d_ext = bw * (r_ext - float(s_ext.mean()))

                # Direct BGE cosine
                r_cos = float(M_bge_cos[wu_r, wv_r])
                s_cos = M_bge_cos[wu_s[valid_s], wv_s[valid_s]]
                d_cos = bw * (r_cos - float(s_cos.mean()))

                bigram_rows.append({
                    "u_sign": S.sign.iloc[u],
                    "v_sign": S.sign.iloc[v],
                    "u_word": S.sound.iloc[u],
                    "v_word": S.sound.iloc[v],
                    "u_gloss": senses_k[S.word.iloc[u]][0][0],
                    "v_gloss": senses_k[S.word.iloc[v]][0][0],
                    "u_cats": "|".join(senses_k[S.word.iloc[u]][0][1]),
                    "v_cats": "|".join(senses_k[S.word.iloc[v]][0][1]),
                    "u_cls": S.cls.iloc[u],
                    "v_cls": S.cls.iloc[v],
                    "new_weight": round(bw, 4),
                    "lipi_cat_pmi_real": round(r_fix, 4),
                    "lipi_cat_pmi_shufB": round(float(s_fix.mean()), 4),
                    "contrib_lipi_cat_pmi": round(d_fix / max(tot_new_w, 1e-9), 6),
                    "ext_cat_pmi_real": round(r_ext, 4),
                    "ext_cat_pmi_shufB": round(float(s_ext.mean()), 4),
                    "contrib_ext_cat_pmi": round(d_ext / max(tot_new_w, 1e-9), 6),
                    "bge_cos_real": round(r_cos, 4),
                    "bge_cos_shufB": round(float(s_cos.mean()), 4),
                    "contrib_bge_cos": round(d_cos / max(tot_new_w, 1e-9), 6),
                })
                for s_id in (u, v):
                    sign_w[s_id] += 0.5 * bw
                    sign_gain_fix[s_id] += 0.5 * d_fix / max(tot_new_w, 1e-9)
                    sign_gain_ext[s_id] += 0.5 * d_ext / max(tot_new_w, 1e-9)
                    sign_gain_cos[s_id] += 0.5 * d_cos / max(tot_new_w, 1e-9)

            bg_df = pd.DataFrame(bigram_rows).sort_values("contrib_lipi_cat_pmi", ascending=False)
            bg_df.to_csv(os.path.join(OUT_DIR, "k1_bigram_drivers_new.csv"), index=False)

            sign_rows = []
            for u in range(len(S)):
                if sign_w[u] <= 0:
                    continue
                sign_rows.append({
                    "sign": S.sign.iloc[u],
                    "sound": S.sound.iloc[u],
                    "gloss1": senses_k[S.word.iloc[u]][0][0],
                    "cats1": "|".join(senses_k[S.word.iloc[u]][0][1]),
                    "cls": S.cls.iloc[u],
                    "band": int(S.band.iloc[u]),
                    "status": S.status.iloc[u],
                    "new_edge_weight": round(sign_w[u], 3),
                    "contrib_lipi_cat_pmi": round(sign_gain_fix[u], 6),
                    "contrib_ext_cat_pmi": round(sign_gain_ext[u], 6),
                    "contrib_bge_cos": round(sign_gain_cos[u], 6),
                })
            sg_df = pd.DataFrame(sign_rows).sort_values("contrib_lipi_cat_pmi", ascending=False)
            sg_df.to_csv(os.path.join(OUT_DIR, "k1_sign_drivers_new.csv"), index=False)

            # Save directional 13x13 category lift matrix learned on Lipi vs External control
            pd.DataFrame(L_all_lipi, index=CATS, columns=CATS).round(4).to_csv(
                os.path.join(OUT_DIR, "k1_dir_cat_pmi_matrix_lipi.csv")
            )
            pd.DataFrame(L_ext, index=CATS, columns=CATS).round(4).to_csv(
                os.path.join(OUT_DIR, "k1_dir_cat_pmi_matrix_ext.csv")
            )

    with open(os.path.join(OUT_DIR, "k1_audit_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    log("Saved k1_audit_results.json, k1_bigram_drivers_new.csv, k1_sign_drivers_new.csv.")


if __name__ == "__main__":
    main()
