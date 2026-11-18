#!/usr/bin/env python3
"""gsol_02_qap.py -- Step 2: From-Scratch Global Dictionary Assignment Solver across 7 Candidate Languages.

Formulates decipherment of the top N=120 frequent Lipi signs as a constrained 1-to-1 global
Quadratic Assignment Problem (Frank-Wolfe Linear Sum Assignment + Blocked-Gibbs Simulated Annealing + 2-opt)
fit STRICTLY on Lipi training data (`events_lipi.json`), run head-to-head across 7 candidate lexicons:
  1. Dravidian (`dedr_tamil`)
  2. Munda (`mundari_bhadra` + `santali_campbell`)
  3. Indo-Aryan (`oia_turner`)
  4. Elamite (`elamite_hinzkoch`, German glosses via multilingual M2V + DE picture/category terms)
  5. Sumerian (`sumerian_halloran`)
  6. Akkadian (`akkadian_wiktionary`)
  7. Burushaski (`burushaski_lorimer`)

Two solver modes (covering both pure unsupervised QAP and Step 3 core-anchored redesign):
  - `free`: Joint objective uses ONLY (1) non-circular phrase/bigram semantic coherence (`emb_m2v` cosine +
            `control_texts.json` natural-sentence directional bilinear & category transitions),
            (2) Lipi-only compound splits (`C <-> A+B`), graphical compound-base (`C -> B`), and Lipi frame swaps,
            (3) same-language blind-agreed picture (`pictures_blind.csv`) homophone/rebus tie-breaker.
  - `anchored`: Locks the word-free closed grammatical/accounting core (`NUM_*`, `MEASURE`, `CLOSER`, `SLOT`,
                `TITLE`, `THING`, `PLACE`, `OPEN` from word-free `frame/classes_v2.csv`) first via role-category
                priors, then solves all 120 signs globally around that core.

Crucial Decoy-Proof Controls built in:
  (i) Zero-shot evaluation on unseen Mahadevan `new texts` (`events_new.json` directional bigrams AND
      Mahadevan-only frame swaps & compound splits never seen in Lipi!) vs. 1,000 same-class/same-band shuffles.
  (ii) Fitting the EXACT SAME QAP solver on `N_DECOY_SOLVES` sign-permuted Lipi decoy corpora per language
       (permuting signs within `(v2_base, band)` on Lipi so corpus bigrams/swaps are decoupled from sign pictures
       and graphical compound families) to measure whether any language achieves higher Lipi lock or out-of-sample
       held-out `new texts` coherence + held-out swap accuracy than decoy corpora!
"""
import os
import sys
import re
import csv
import json
import time
import itertools
import collections
import unicodedata
import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "work_scripts"))

from sense_core import CATS
from lang_m2_common import pic_terms_en, DE as DE_PIC_TERMS

OUT_DIR = os.path.join(ROOT, "work_data", "gsol")
os.makedirs(OUT_DIR, exist_ok=True)
SENSE_DIR = os.path.join(ROOT, "work_data", "sense")
DICT_EMB_DIR = "/tmp/dict_emb"
RAW_LEX_DIR = os.path.join(ROOT, "work_data", "lang_m", "lex")

T0 = time.time()
def log(*a):
    print(f"[{time.time() - T0:6.1f}s] [gsol_02]", *a, flush=True)


CANDIDATE_LANGS = collections.OrderedDict([
    ("dravidian", ["dedr_tamil"]),
    ("munda", ["mundari_bhadra", "santali_campbell"]),
    ("indo_aryan", ["oia_turner"]),
    ("elamite", ["elamite_hinzkoch"]),
    ("sumerian", ["sumerian_halloran"]),
    ("akkadian", ["akkadian_wiktionary"]),
    ("burushaski", ["burushaski_lorimer"]),
])

JUNK_NORMS = {
    "frequency", "archaic", "concatenates", "variants", "dialect", "cf", "todo",
    "theprospectivemodalprefix", "lianectgereay", "emesal", "unknown", "see", "ibid",
}

# Word-free structural class -> universal semantic categories (for `anchored` mode)
ROLE_TO_CATS = {
    "NUM_SHORT": ["number"],
    "NUM_TALL": ["number"],
    "NUM_NAME": ["number", "quality", "time"],
    "MEASURE": ["measure", "tool"],
    "THING": ["commodity", "plant", "animal", "tool"],
    "CLOSER": ["place", "kin", "person"],
    "TITLE": ["person", "action"],
    "SLOT": ["number", "measure", "place", "quality"],
    "OPEN": ["place", "time", "measure", "number"],
    "PLACE": ["place", "time"],
    "CREST": ["time", "animal", "person", "kin", "plant", "deity"],
    "NAME_BACK": ["kin", "person", "quality"],
    "PERSONAL": [],  # open lexical class
}


def is_valid_sign(s):
    return bool(s) and s not in ("000", "ALT") and str(s).isdigit()


def plain_ascii(t):
    t = unicodedata.normalize("NFD", str(t).lower())
    return "".join(c for c in t if not unicodedata.combining(c)).replace("ß", "ss")


def gloss_tokens(gl, n=4):
    return re.findall(r"[a-z]+", plain_ascii(gl))[:n]


def build_sign_problem(n_signs=120):
    """Extract top `n_signs` frequent Lipi signs and build strictly separated Lipi vs Held-Out Mahadevan structures."""
    events_lipi = json.load(open(os.path.join(SENSE_DIR, "events_lipi.json")))
    events_new = json.load(open(os.path.join(SENSE_DIR, "events_new.json")))

    # Count physical event occurrences on Lipi
    ev_counts = collections.Counter()
    for e in events_lipi:
        seen = set()
        for f in e["faces"]:
            for s in f:
                if is_valid_sign(s):
                    seen.add(s)
        for s in seen:
            ev_counts[s] += 1

    top_signs = [s for s, _ in ev_counts.most_common(n_signs)]
    s2i = {s: i for i, s in enumerate(top_signs)}
    N = len(top_signs)

    # Word-free classes (`classes_v2.csv`) & frequency terciles
    cl_df = pd.read_csv(os.path.join(ROOT, "work_data", "frame", "classes_v2.csv"), dtype=str).fillna("")
    cmap = dict(zip(cl_df.sign, cl_df.v2_base))
    cls_list = [cmap.get(s, "PERSONAL") for s in top_signs]
    uses_arr = np.array([ev_counts[s] for s in top_signs], dtype=np.float64)
    q1, q2 = np.quantile(uses_arr, [1.0 / 3.0, 2.0 / 3.0])
    band_list = [0 if u < q1 else (1 if u < q2 else 2) for u in uses_arr]

    # Blind-agreed pictures (`work_data/lang_m2/signs.csv`, levels 3of3 and 2of3)
    pics_by_sign = {s: [] for s in top_signs}
    lm2_signs_path = os.path.join(ROOT, "work_data", "lang_m2", "signs.csv")
    for r in csv.DictReader(open(lm2_signs_path, encoding="utf-8")):
        if r["sign"] in pics_by_sign and r["level"] in ("3of3", "2of3") and r["nouns"]:
            pics_by_sign[r["sign"]] = [x for x in r["nouns"].split(";") if x]

    # 1. Directional adjacent-bigram matrices: Lipi vs New (strictly separated!)
    def build_adj_graph(events):
        G = np.zeros((N, N), dtype=np.float32)
        n_ev = 0
        for e in events:
            face_pairs = []
            for f in e["faces"]:
                ps = [(s2i[a], s2i[b]) for a, b in zip(f, f[1:]) if a in s2i and b in s2i and a != b]
                if ps:
                    face_pairs.append(ps)
            if not face_pairs:
                continue
            n_ev += 1
            wf = 1.0 / len(face_pairs)
            for ps in face_pairs:
                ew = wf / len(ps)
                for u, v in ps:
                    G[u, v] += ew
        return G, n_ev

    G_lipi, nev_lipi = build_adj_graph(events_lipi)
    G_new, nev_new = build_adj_graph(events_new)

    #Also keep face-level `new texts` edge list for exact per-shuffle evaluation
    new_faces = []
    for e in events_new:
        fps = []
        for f in e["faces"]:
            ps = [(s2i[a], s2i[b]) for a, b in zip(f, f[1:]) if a in s2i and b in s2i and a != b]
            if ps:
                fps.append(ps)
        if fps:
            wf = 1.0 / len(fps)
            for ps in fps:
                new_faces.append((wf, ps))

    # 2. Lipi-ONLY vs Held-Out Mahadevan-ONLY Frame Swaps & One-for-Two Splits
    # Check unbroken faces from corpus_jobs.csv (Lipi) vs events_new (unseen Mahadevan)
    cj = pd.read_csv(os.path.join(ROOT, "work_data", "frame", "corpus_jobs.csv"), dtype=str).fillna("")
    lipi_intact = set()
    for sig, br in zip(cj.signs, cj.broken_edge):
        if br != "True":
            tok = tuple(x for x in sig.split("-") if x)
            if len(tok) >= 2 and all(is_valid_sign(x) for x in tok):
                lipi_intact.add(tok)

    new_intact = set()
    for e in events_new:
        for f in e["faces"]:
            tok = tuple(f)
            if len(tok) >= 2 and all(is_valid_sign(x) for x in tok):
                new_intact.add(tok)

    def extract_swaps_and_splits(intact_set):
        # Swaps: P + [u] + S vs P + [v] + S on texts of length >= 3
        by_frame1 = collections.defaultdict(set)
        for f in intact_set:
            for idx in range(len(f)):
                by_frame1[(f[:idx], f[idx + 1:])].add(f[idx])
        swap_frames = collections.defaultdict(set)
        for key, ss in by_frame1.items():
            if len(key[0]) + len(key[1]) < 2:
                continue
            for a, b in itertools.combinations(sorted(ss), 2):
                if a in s2i and b in s2i:
                    swap_frames[(s2i[a], s2i[b])].add(key)

        # One-for-two splits: P + [C] + S vs P + [A, B] + S
        split_frames = collections.defaultdict(set)
        for f in intact_set:
            for idx in range(len(f) - 1):
                key = (f[:idx], f[idx + 2:])
                if not key[0] and not key[1]:
                    continue
                a, b = f[idx], f[idx + 1]
                if a not in s2i or b not in s2i:
                    continue
                for c in by_frame1.get(key, ()):
                    if c in s2i and c != a and c != b:
                        split_frames[(s2i[c], s2i[a], s2i[b])].add(key)
        return swap_frames, split_frames

    lipi_swaps_raw, lipi_splits_raw = extract_swaps_and_splits(lipi_intact)
    new_swaps_raw, new_splits_raw = extract_swaps_and_splits(new_intact)

    # Lipi swap graph (>= 2 Lipi frames; downweight same-picture variants to 0.25)
    G_swap_lipi = np.zeros((N, N), dtype=np.float32)
    n_lipi_swap_pairs = 0
    for (u, v), frs in lipi_swaps_raw.items():
        if len(frs) >= 2:
            pu, pv = set(pics_by_sign[top_signs[u]]), set(pics_by_sign[top_signs[v]])
            same_pic = bool(pu and pv and (pu & pv))
            wt = float(len(frs)) * (0.25 if same_pic else 1.0)
            G_swap_lipi[u, v] = G_swap_lipi[v, u] = wt
            n_lipi_swap_pairs += 1

    # Held-out unseen swaps: pairs that swap in `new_intact` (or Mahadevan-only in swap_pairs.csv) with <2 Lipi frames!
    heldout_swaps = []
    seen_ho = set()
    for (u, v), frs in new_swaps_raw.items():
        if len(lipi_swaps_raw.get((u, v), ())) == 0:
            pu, pv = set(pics_by_sign[top_signs[u]]), set(pics_by_sign[top_signs[v]])
            if not (pu and pv and (pu & pv)):
                heldout_swaps.append((u, v, len(frs)))
                seen_ho.add((u, v))
    # Also include Mahadevan-only swaps from `work_data/lang_m/swap_pairs.csv` (`lipi_frames == 0`, `mahadevan_frames >= 2`)
    sp_df = pd.read_csv(os.path.join(ROOT, "work_data", "lang_m", "swap_pairs.csv"), dtype=str).fillna("")
    for r in sp_df.itertuples():
        a, b = str(r.a).zfill(3), str(r.b).zfill(3)
        if a in s2i and b in s2i and int(r.lipi_frames) == 0 and int(r.mahadevan_frames) >= 1:
            u, v = min(s2i[a], s2i[b]), max(s2i[a], s2i[b])
            if (u, v) not in seen_ho and str(r.tested) == "True":
                heldout_swaps.append((u, v, int(r.mahadevan_frames)))
                seen_ho.add((u, v))

    # Graphical compound -> base relationships (`mark_families.csv`, excluding `joined object` per signlist.md)
    mf_df = pd.read_csv(os.path.join(ROOT, "work_data", "signlist", "mark_families.csv"), dtype=str).fillna("")
    G_base_raw = np.zeros((N, N), dtype=np.float32)  # G_base_raw[compound_u, base_v]
    comp_base_pairs = []
    for r in mf_df.itertuples():
        c, b, mtype = str(r.compound).zfill(3), str(r.base).zfill(3), str(r.mark_type)
        if c in s2i and b in s2i and c != b and mtype != "joined object":
            wt = 1.5 if mtype in ("strokes inside", "hat", "whiskers") else 0.6
            G_base_raw[s2i[c], s2i[b]] = wt
            comp_base_pairs.append((s2i[c], s2i[b], mtype, wt))

    def build_splits_and_base_graph(splits_dict, base_mat_raw):
        G_b = base_mat_raw.copy()
        out_splits = []
        for (c, a, b), frs in splits_dict.items():
            is_base_split = (base_mat_raw[c, a] > 0) or (base_mat_raw[c, b] > 0)
            # Exclude bare generic `-[ ]-740` single-sign frame when counting non-base multi-frame splits
            rich_frs = [k for k in frs if (len(k[0]) + len(k[1]) >= 2) or (k != ((), ("740",)))]
            if (is_base_split and len(frs) >= 1) or (len(rich_frs) >= 4):
                wt = float(len(frs)) * (2.0 if is_base_split else 0.75)
                out_splits.append((c, a, b, wt))
                G_b[c, a] += 0.35 * wt
                G_b[c, b] += 0.35 * wt
        return out_splits, G_b

    lipi_splits, G_base_lipi = build_splits_and_base_graph(lipi_splits_raw, G_base_raw)

    heldout_splits = [
        (c, a, b, len(frs)) for (c, a, b), frs in new_splits_raw.items()
        if (c, a, b) not in lipi_splits_raw and ((G_base_raw[c, a] > 0) or (G_base_raw[c, b] > 0) or len(frs) >= 2)
    ]

    log(f"Built top-{N} sign problem: Lipi events={nev_lipi} (edge sum={G_lipi.sum():.1f}), "
        f"New events={nev_new} (edge sum={G_new.sum():.1f}), pictured signs={sum(bool(pics_by_sign[s]) for s in top_signs)}, "
        f"Lipi swap pairs={n_lipi_swap_pairs}, Lipi compound-base={len(comp_base_pairs)}, Lipi splits={len(lipi_splits)}, "
        f"Held-out Mahadevan-only swaps={len(heldout_swaps)}, splits={len(heldout_splits)}")

    return {
        "N": N,
        "signs": top_signs,
        "s2i": s2i,
        "uses": uses_arr,
        "cls": np.array(cls_list),
        "band": np.array(band_list, dtype=np.int32),
        "pics": [pics_by_sign[s] for s in top_signs],
        "G_lipi": G_lipi,
        "G_new": G_new,
        "new_faces": new_faces,
        "G_swap_lipi": G_swap_lipi,
        "G_base_raw": G_base_raw,
        "G_base_lipi": G_base_lipi,
        "lipi_splits_raw": lipi_splits_raw,
        "build_splits_fn": build_splits_and_base_graph,
        "lipi_splits": lipi_splits,
        "heldout_swaps": heldout_swaps,
        "heldout_splits": heldout_splits,
    }


def build_external_m2v_priors(emb_m2v_all, phrase_masks_all, all_phrases):
    """Learn non-circular directional category lift & M2V bilinear transition from `control_texts.json`."""
    p2i = {p: i for i, p in enumerate(all_phrases)}
    ctrl_words = pd.read_csv(os.path.join(SENSE_DIR, "control_words.csv")).fillna("")
    ctrl_senses = pd.read_csv(os.path.join(SENSE_DIR, "control_senses.csv")).fillna("")
    ctrl_texts = json.load(open(os.path.join(SENSE_DIR, "control_texts.json")))

    s0 = ctrl_senses[ctrl_senses.sense == 0]
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

    # Encode control phrases not in phrases.json
    missing = sorted({p for p in phrases if p and p not in p2i})
    extra = {}
    if missing:
        from model2vec import StaticModel
        m_m2v = StaticModel.from_pretrained("minishlab/potion-multilingual-128M")
        idx_sub = np.linspace(0, len(all_phrases) - 1, 8000, dtype=int)
        mu = m_m2v.encode([all_phrases[i] for i in idx_sub]).astype(np.float32).mean(axis=0, keepdims=True)
        vm = m_m2v.encode(missing).astype(np.float32) - mu
        vm /= (np.linalg.norm(vm, axis=1, keepdims=True) + 1e-8)
        for p, v in zip(missing, vm):
            extra[p] = v

    emb_c = np.zeros((W_c, emb_m2v_all.shape[1]), dtype=np.float32)
    for i, p in enumerate(phrases):
        if p in p2i:
            emb_c[i] = emb_m2v_all[p2i[p]].astype(np.float32)
        elif p in extra:
            emb_c[i] = extra[p]

    u1_l, u2_l = [], []
    for s in ctrl_texts:
        idxs = [x if isinstance(x, int) else w2idx.get(x, -1) for x in s]
        idxs = [x for x in idxs if 0 <= x < W_c]
        for a, b in zip(idxs, idxs[1:]):
            if a != b:
                u1_l.append(a)
                u2_l.append(b)
    u1, u2 = np.array(u1_l, dtype=np.int32), np.array(u2_l, dtype=np.int32)
    c1, c2 = wc[u1], wc[u2]
    tot = float(len(u1))
    L_ctrl = np.log((c1.T @ c2 + 0.5) / (tot * np.outer(c1.sum(0) / tot, c2.sum(0) / tot) + 0.5)).astype(np.float32)

    X, Y = emb_c[u1], emb_c[u2]
    mx, my = X.mean(0, keepdims=True), Y.mean(0, keepdims=True)
    Xc, Yc = X - mx, Y - my
    C = (Xc.T @ Yc) / tot
    D = emb_c.shape[1]
    Sx = (Xc.T @ Xc) / tot + 0.5 * np.eye(D, dtype=np.float32)
    Sy = (Yc.T @ Yc) / tot + 0.5 * np.eye(D, dtype=np.float32)
    B_ctrl = np.linalg.solve(Sx, np.linalg.solve(Sy, C.T).T).astype(np.float32)
    return L_ctrl, B_ctrl, mx.astype(np.float32), my.astype(np.float32)


def zscore_offdiag(M):
    """Standardize off-diagonal entries of [K, K] matrix to mean 0, std 1; set diagonal to 0."""
    K = M.shape[0]
    mask = ~np.eye(K, dtype=bool)
    vals = M[mask]
    mu = float(vals.mean())
    sd = float(vals.std())
    out = (M - mu) / max(sd, 1e-6)
    np.fill_diagonal(out, 0.0)
    return out.astype(np.float32)


def skel_dels(sk):
    if len(sk) < 2:
        return {("=", sk)}
    return {("=", sk)} | {("-", sk[:k] + sk[k + 1:]) for k in range(len(sk))}


def load_language_lexicon(lang_name, dict_names, sign_prob, all_phrases, phrase_masks, emb_m2v_all, ext_priors, m_cap=1200):
    """Load candidate lexicon for `lang_name`:
    1. Index ALL raw rows in `<dict>.tsv` for full-coverage picture-word homophony (`U_rebus`).
    2. Build clean 1-to-1 candidate pool `W_L` (size <= `m_cap`, strictly unique `eid` AND unique `p1_id`!)
       and precompute standardized `S_sem`, `S_swap`, `S_base`, `U_rebus`, and `U_role`.
    """
    is_de = (lang_name == "elamite")
    # 1. Read raw TSVs for full picture-noun lookup across the entire language dictionary
    raw_rows = []
    for dname in dict_names:
        tsv_path = os.path.join(RAW_LEX_DIR, f"{dname}.tsv")
        with open(tsv_path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                parts = line.rstrip("\n").split("\t")
                if len(parts) < 5:
                    continue
                eid, hw, nf, sk, gl = parts[0], parts[1], parts[2], parts[3], parts[4]
                if not nf or len(nf) > 12 or nf in JUNK_NORMS:
                    continue
                raw_rows.append((f"{dname}:{eid}", hw, nf, sk, gl))

    # Index picture words in full raw dictionary
    inv3 = collections.defaultdict(set)
    for idx, (_, _, _, _, gl) in enumerate(raw_rows):
        for w in gloss_tokens(gl, 3):
            forms = {w} | ({w[:-1]} if w.endswith("s") and len(w) > 3 else set()) | ({w[:-2]} if w.endswith("es") and len(w) > 4 else set())
            for f_ in forms:
                inv3[f_].add(idx)

    all_blind_nouns = sorted({n for ns in sign_prob["pics"] for n in ns})
    pic_entries = {}  # noun -> list of (eid, nf, sk)
    for nn in all_blind_nouns:
        terms = set(DE_PIC_TERMS.get(nn, "").split()) if is_de else pic_terms_en(nn)
        hit_idxs = set().union(*[inv3.get(t, set()) for t in terms]) if terms else set()
        pic_entries[nn] = [(raw_rows[i][0], raw_rows[i][2], raw_rows[i][3]) for i in sorted(hit_idxs)]

    # 2. Read prebuilt `/tmp/dict_emb/<dict>.csv` and clean/deduplicate to unique `eid` and unique `p1_id`
    dfs = []
    for dname in dict_names:
        df = pd.read_csv(os.path.join(DICT_EMB_DIR, f"{dname}.csv"), dtype={"eid": str, "hw": str, "norm": str, "skel": str}).fillna("")
        df["eid_full"] = dname + ":" + df["eid"]
        dfs.append(df)
    cat_df = pd.concat(dfs, ignore_index=True)

    # Permutation-invariant set of all picture-word forms & consonant skeletons across the 87 blind pictures
    any_pic_nf = {pnf for entries in pic_entries.values() for _, pnf, _ in entries}
    any_pic_sk2 = {psk for entries in pic_entries.values() for _, _, psk in entries if len(psk) >= 2}

    # Filter junk rows
    valid_rows = []
    for r in cat_df.itertuples():
        nf = str(r.norm).strip()
        sk = str(r.skel).strip()
        pid = int(r.p1_id)
        ph = all_phrases[pid]
        if not (1 <= len(nf) <= 12) or nf in JUNK_NORMS or not re.search(r"[a-zA-Zäöüß]{2,}", ph):
            continue
        if re.match(r"^\d+", ph):
            continue
        cmask = int(phrase_masks[pid])
        has_cat = int(cmask > 0)
        is_hom = int((nf in any_pic_nf) or (len(sk) >= 2 and sk in any_pic_sk2))
        # Retain full-dictionary homophone/picture candidates + categorized core roots (100% permutation-invariant!)
        prio = (is_hom * 12) + (has_cat * 8) + int(len(sk) >= 1) * 4 - 0.35 * len(nf)
        valid_rows.append((prio, r.eid_full, r.hw, nf, sk, pid, cmask))

    # Sort descending by root quality priority and enforce STRICT unique `eid_full` AND unique `p1_id`
    valid_rows.sort(key=lambda x: -x[0])
    seen_eid = set()
    seen_pid = set()
    dedup = []
    for item in valid_rows:
        _, eid_f, hw, nf, sk, pid, cmask = item
        if eid_f in seen_eid or pid in seen_pid:
            continue
        seen_eid.add(eid_f)
        seen_pid.add(pid)
        dedup.append((eid_f, hw, nf, sk, pid, cmask))
        if len(dedup) >= m_cap:
            break

    M = len(dedup)
    eids = [x[0] for x in dedup]
    hws = [x[1] for x in dedup]
    norms = [x[2] for x in dedup]
    skels = [x[3] for x in dedup]
    pids = np.array([x[4] for x in dedup], dtype=np.int32)
    cmasks = np.array([x[5] for x in dedup], dtype=np.int32)

    # Build 13-cat binary matrix [M, 13] and M2V embedding matrix [M, 256]
    W_cats = np.zeros((M, 13), dtype=np.float32)
    for c_i in range(13):
        W_cats[:, c_i] = ((cmasks & (1 << c_i)) > 0).astype(np.float32)
    W_emb = emb_m2v_all[pids].astype(np.float32)

    # Precompute standardized non-circular semantic coherence matrix `S_sem` [M, M]
    L_ctrl, B_ctrl, mx_c, my_c = ext_priors
    S_cos = W_emb @ W_emb.T
    S_bilin = ((W_emb - mx_c) @ B_ctrl) @ (W_emb - my_c).T
    # Category max-lift matrix
    A1 = np.full((M, 13), -np.inf, dtype=np.float32)
    for c1 in range(13):
        m = W_cats[:, c1] > 0
        if m.any():
            A1[m] = np.maximum(A1[m], L_ctrl[c1][None, :])
    S_cat = np.full((M, M), -np.inf, dtype=np.float32)
    for c2 in range(13):
        m = W_cats[:, c2] > 0
        if m.any():
            S_cat[:, m] = np.maximum(S_cat[:, m], A1[:, c2][:, None])
    S_cat[~np.isfinite(S_cat)] = 0.0

    S_sem = zscore_offdiag(
        0.60 * zscore_offdiag(S_cos)
        + 0.20 * zscore_offdiag(S_bilin)
        + 0.20 * zscore_offdiag(S_cat)
    )
    S_cos_z = zscore_offdiag(S_cos)

    # Precompute standardized phonetic swap matrix `S_swap` [M, M] (consonant skeleton match)
    S_swap_raw = np.zeros((M, M), dtype=np.float32)
    by_sk = collections.defaultdict(list)
    by_del = collections.defaultdict(list)
    for i, sk in enumerate(skels):
        if sk:
            by_sk[sk].append(i)
            if len(sk) >= 2:
                for k in range(len(sk)):
                    by_del[sk[:k] + sk[k + 1:]].append(i)

    # Loose 1-edit skeleton match (0.35)
    for sub, idxs in by_del.items():
        if len(sub) >= 1 and len(idxs) > 1:
            arr = np.array(idxs, dtype=np.int32)
            S_swap_raw[np.ix_(arr, arr)] = np.maximum(S_swap_raw[np.ix_(arr, arr)], 0.35)
        if len(sub) >= 2 and sub in by_sk:
            arr1 = np.array(idxs, dtype=np.int32)
            arr2 = np.array(by_sk[sub], dtype=np.int32)
            S_swap_raw[np.ix_(arr1, arr2)] = np.maximum(S_swap_raw[np.ix_(arr1, arr2)], 0.35)
            S_swap_raw[np.ix_(arr2, arr1)] = np.maximum(S_swap_raw[np.ix_(arr2, arr1)], 0.35)

    # Exact skeleton match (1.0 if len>=2, 0.5 if len==1)
    for sk, idxs in by_sk.items():
        if len(idxs) > 1:
            arr = np.array(idxs, dtype=np.int32)
            val = 1.0 if len(sk) >= 2 else 0.5
            S_swap_raw[np.ix_(arr, arr)] = np.maximum(S_swap_raw[np.ix_(arr, arr)], val)
    np.fill_diagonal(S_swap_raw, 0.0)
    S_swap = zscore_offdiag(S_swap_raw)

    # Precompute standardized compound-base affix containment matrix `S_base` [M, M]
    # S_base[w_C, w_B] > 0 when w_C's consonant skeleton starts or ends with w_B's skeleton (and is longer!)
    S_base_raw = np.zeros((M, M), dtype=np.float32)
    for j, sk_b in enumerate(skels):
        if not sk_b:
            continue
        nf_b = norms[j]
        for i, sk_c in enumerate(skels):
            if i == j or len(sk_c) <= len(sk_b):
                continue
            if len(sk_b) >= 2 and (sk_c.startswith(sk_b) or sk_c.endswith(sk_b)):
                S_base_raw[i, j] = 1.0
            elif len(nf_b) >= 2 and len(norms[i]) > len(nf_b) and (norms[i].startswith(nf_b) or norms[i].endswith(nf_b)):
                S_base_raw[i, j] = 0.75
            elif len(sk_b) == 1 and len(sk_c) >= 2 and (sk_c.startswith(sk_b) or sk_c.endswith(sk_b)):
                S_base_raw[i, j] = 0.25
    S_base = zscore_offdiag(S_base_raw)

    # Precompute same-language blind-picture Rebus / Acrophony / Logogram unary matrix `U_rebus` [N, M]
    N = sign_prob["N"]
    U_rebus = np.zeros((N, M), dtype=np.float32)
    U_rebus_raw = np.zeros((N, M), dtype=np.float32)
    for u in range(N):
        p_nouns = sign_prob["pics"][u]
        if not p_nouns:
            continue
        # Gather picture words in this language
        pw_eids = set()
        pw_nfs = set()
        pw_sks2 = set()
        pw_dels = set()
        pw_acro = set()
        for nn in p_nouns:
            for peid, pnf, psk in pic_entries.get(nn, ()):
                pw_eids.add(peid)
                pw_nfs.add(pnf)
                if len(psk) >= 2:
                    pw_sks2.add(psk)
                    for k in range(len(psk)):
                        if len(psk) - 1 >= 2:
                            pw_dels.add(psk[:k] + psk[k + 1:])
                if len(pnf) >= 2:
                    pw_acro.add(pnf[:2])
        if not pw_eids:
            continue
        raw_u = np.zeros(M, dtype=np.float32)
        for w in range(M):
            if eids[w] in pw_eids:
                # Direct logogram reading
                raw_u[w] = 0.55
            else:
                nf_w, sk_w = norms[w], skels[w]
                sc_w = 0.0
                if nf_w in pw_nfs:
                    sc_w = 1.0  # strict homophone rebus pun!
                elif len(sk_w) >= 2 and sk_w in pw_sks2:
                    sc_w = 0.70  # consonant-skeleton rebus pun!
                elif len(sk_w) >= 2 and (sk_w in pw_dels or any((sk_w[:k] + sk_w[k + 1:]) in pw_sks2 for k in range(len(sk_w)))):
                    sc_w = 0.35  # near-skeleton rebus
                elif len(nf_w) >= 2 and nf_w[:2] in pw_acro:
                    sc_w = 0.20  # acrophonic CV match
                raw_u[w] = sc_w
        U_rebus_raw[u] = raw_u
        sd = float(raw_u.std())
        if sd > 1e-6:
            U_rebus[u] = (raw_u - float(raw_u.mean())) / sd

    # Precompute word-free structural role prior `U_role` [N, M] (used ONLY in `anchored` mode)
    U_role = np.zeros((N, M), dtype=np.float32)
    for u in range(N):
        rcats = ROLE_TO_CATS.get(sign_prob["cls"][u], [])
        if not rcats:
            continue
        c_idxs = [CATS.index(c) for c in rcats]
        hit = (W_cats[:, c_idxs].sum(axis=1) > 0).astype(np.float32)
        sd = float(hit.std())
        if sd > 1e-6:
            U_role[u] = (hit - float(hit.mean())) / sd

    log(f"Loaded lexicon {lang_name:12s}: raw={len(raw_rows):5d} | active 1-to-1 pool M={M:4d} | "
        f"pictured signs with L-nouns={int((U_rebus_raw.max(1) > 0).sum())}/{sum(bool(x) for x in sign_prob['pics'])}")

    return {
        "lang": lang_name,
        "M": M,
        "eids": eids,
        "hws": hws,
        "norms": norms,
        "skels": skels,
        "pids": pids,
        "phrases": [all_phrases[p] for p in pids],
        "W_cats": W_cats,
        "S_sem": S_sem,
        "S_cos_z": S_cos_z,
        "S_swap": S_swap,
        "S_swap_raw": S_swap_raw,
        "S_base": S_base,
        "S_base_raw": S_base_raw,
        "U_rebus": U_rebus,
        "U_rebus_raw": U_rebus_raw,
        "U_role": U_role,
    }


def split_3body_bonus(sk_c, nf_c, sk_a, nf_a, sk_b, nf_b):
    """Exact 3-body concatenation score for C <-> A + B (head-final or head-initial symmetric)."""
    if not sk_c:
        return 0.0
    for s1, s2 in ((sk_a, sk_b), (sk_b, sk_a)):
        if s1 and s2:
            comb = s1 + s2
            if sk_c == comb:
                return 2.0
            if len(comb) >= 3 and (sk_c.startswith(comb[:3]) or comb.startswith(sk_c)):
                return 1.0
    for n1, n2 in ((nf_a, nf_b), (nf_b, nf_a)):
        if len(n1) >= 2 and len(n2) >= 2 and (nf_c == n1 + n2):
            return 2.0
    return 0.0


def eval_lipi_objective(pi, G_sem_n, G_swap_n, G_base_n, splits, U_tot, lex, w_sem=1.0, w_swap=0.35, w_base=0.35, w_split=0.20):
    """Exact total Lipi QAP objective and breakdown for injective assignment `pi` [N]."""
    sem_val = float((G_sem_n * lex["S_sem"][np.ix_(pi, pi)]).sum())
    swap_val = float((G_swap_n * lex["S_swap"][np.ix_(pi, pi)]).sum())
    base_val = float((G_base_n * lex["S_base"][np.ix_(pi, pi)]).sum())
    u_val = float(U_tot[np.arange(len(pi)), pi].sum()) / len(pi)

    sp_val = 0.0
    if splits:
        sks, nfs = lex["skels"], lex["norms"]
        tot_sw = sum(wt for _, _, _, wt in splits)
        acc = 0.0
        for c, a, b, wt in splits:
            wc, wa, wb = pi[c], pi[a], pi[b]
            acc += wt * split_3body_bonus(sks[wc], nfs[wc], sks[wa], nfs[wa], sks[wb], nfs[wb])
        sp_val = acc / max(tot_sw, 1e-9)

    tot = w_sem * sem_val + w_swap * swap_val + w_base * base_val + w_split * sp_val + u_val
    return tot, {"total": tot, "sem": sem_val, "swap": swap_val, "base": base_val, "split3": sp_val, "unary": u_val}


def solve_qap_global(G_lipi, G_swap, G_base, splits, U_rebus, U_role, lex, mode="free", seed=101, n_starts=6, n_sweeps=28):
    """Solve 1-to-1 QAP strictly on Lipi data via Multi-Start Hungarian Frank-Wolfe + Blocked-Gibbs SA + 2-Opt."""
    rng = np.random.default_rng(seed)
    N = G_lipi.shape[0]
    M = lex["M"]

    # Normalize each Lipi graph so objective weights have clean interpretable unit scales
    G_sem_n = (G_lipi / max(float(G_lipi.sum()), 1e-9)).astype(np.float32)
    G_swap_n = (G_swap / max(float(G_swap.sum()), 1e-9)).astype(np.float32)
    G_base_n = (G_base / max(float(G_base.sum()), 1e-9)).astype(np.float32)

    w_sem, w_swap, w_base, w_split = 1.0, 0.35, 0.35, 0.20
    if mode == "free":
        U_tot = (0.45 * U_rebus).astype(np.float32)
    elif mode == "anchored":
        U_tot = (0.45 * U_rebus + 0.65 * U_role).astype(np.float32)
    else:
        raise ValueError(mode)

    S_sem = lex["S_sem"]
    S_swap = lex["S_swap"]
    S_base = lex["S_base"]

    # Build split incident adjacency for fast 3-body incremental updates
    splits_by_u = [[] for _ in range(N)]
    tot_split_w = max(sum(wt for _, _, _, wt in splits), 1e-9)
    for c, a, b, wt in splits:
        wn = wt / tot_split_w
        splits_by_u[c].append((0, c, a, b, wn))
        splits_by_u[a].append((1, c, a, b, wn))
        splits_by_u[b].append((2, c, a, b, wn))

    best_pi = None
    best_sc = -1e18

    # Phase 1: Multi-start Frank-Wolfe Linear Sum Assignment (Hungarian)
    for st in range(n_starts):
        if st == 0 and mode == "anchored":
            # Core-first initialization: lock closed grammatical/measure core first, then solve all 120!
            core_u = np.where(np.abs(U_role).max(axis=1) > 0)[0]
            _, col_ind_full = linear_sum_assignment(-(U_tot / N + rng.normal(0, 0.002, size=(N, M))))
            pi = col_ind_full.astype(np.int32)
            if len(core_u) >= 5:
                # 4 Hungarian linearization steps on the core subgraph first
                for _ in range(4):
                    grad_core = (U_tot[core_u] / N).copy()
                    pi_c = pi[core_u]
                    grad_core += w_sem * (G_sem_n[np.ix_(core_u, core_u)] @ S_sem[pi_c, :] + G_sem_n[np.ix_(core_u, core_u)].T @ S_sem[:, pi_c].T)
                    _, c_cols = linear_sum_assignment(-grad_core)
                    # Repair collisions with non-core signs
                    used_c = set(c_cols)
                    free_w = [w for w in range(M) if w not in used_c]
                    ptr = 0
                    pi[core_u] = c_cols
                    non_core = [u for u in range(N) if u not in set(core_u)]
                    for u in non_core:
                        if pi[u] in used_c:
                            pi[u] = free_w[ptr]
                            ptr += 1
        else:
            noise = rng.normal(0, 0.015 if st > 0 else 0.001, size=(N, M)).astype(np.float32)
            _, pi = linear_sum_assignment(-(U_tot / N + noise))
            pi = pi.astype(np.int32)

        # 5 Frank-Wolfe Hungarian iterations
        for it in range(5):
            grad = (U_tot / N).copy()
            grad += w_sem * (G_sem_n @ S_sem[pi, :] + G_sem_n.T @ S_sem[:, pi].T)
            grad += w_swap * (2.0 * (G_swap_n @ S_swap[pi, :]))
            grad += w_base * (G_base_n @ S_base[pi, :] + G_base_n.T @ S_base[:, pi].T)
            if it < 3:
                grad += rng.normal(0, 0.004 * (3 - it), size=(N, M)).astype(np.float32)
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

    # Phase 2: Blocked-Gibbs Simulated Annealing + Vectorized 2-Opt Polish from `best_pi`
    pi = best_pi.copy()
    in_use = np.zeros(M, dtype=bool)
    in_use[pi] = True
    sks, nfs = lex["skels"], lex["norms"]

    temps = np.geomspace(0.012, 0.0002, n_sweeps)
    for sw_idx, temp in enumerate(temps):
        order = rng.permutation(N)
        greedy = (sw_idx >= n_sweeps - 5)
        for u in order:
            w_old = pi[u]
            in_use[w_old] = False

            # Exact O(M*N) vectorized marginal potential over ALL M words simultaneously!
            pot = (U_tot[u] / N).copy()
            pot += w_sem * (S_sem[:, pi] @ G_sem_n[u, :] + S_sem[pi, :].T @ G_sem_n[:, u])
            if G_swap_n[u].any():
                pot += w_swap * (2.0 * (S_swap[:, pi] @ G_swap_n[u, :]))
            if G_base_n[u].any() or G_base_n[:, u].any():
                pot += w_base * (S_base[:, pi] @ G_base_n[u, :] + S_base[pi, :].T @ G_base_n[:, u])

            pot[in_use] = -1e9

            # Add exact 3-body split bonus on top-20 candidate words if u participates in Lipi splits
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

        # Every 6 sweeps, run greedy 2-opt swap pass among the 120 assigned signs!
        if (sw_idx + 1) % 6 == 0 or sw_idx == n_sweeps - 1:
            cur_sc, _ = eval_lipi_objective(pi, G_sem_n, G_swap_n, G_base_n, splits, U_tot, lex, w_sem, w_swap, w_base, w_split)
            for _ in range(70):
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

    final_sc, breakdown = eval_lipi_objective(best_pi, G_sem_n, G_swap_n, G_base_n, splits, U_tot, lex, w_sem, w_swap, w_base, w_split)
    return best_pi, breakdown


def make_sign_shuffles(N, cls_arr, band_arr, n_shuf=1000, seed=9001):
    """Generate same-class + same-band permutations over the N=120 signs."""
    rng = np.random.default_rng(seed)
    cells = collections.defaultdict(list)
    for u in range(N):
        cells[(cls_arr[u], int(band_arr[u]))].append(u)
    perms = np.zeros((n_shuf, N), dtype=np.int32)
    for i in range(n_shuf):
        p = np.arange(N, dtype=np.int32)
        for us in cells.values():
            if len(us) >= 2:
                us_arr = np.array(us, dtype=np.int32)
                p[us_arr] = us_arr[rng.permutation(len(us_arr))]
        perms[i] = p
    return perms


def eval_zeroshot_new(pi, sign_prob, lex, shuf_perms):
    """Evaluate Lipi-learned `pi` ZERO-SHOT on unseen Mahadevan `new texts` + unseen swaps/splits
    against `len(shuf_perms)` same-class/same-band decoy permutations!"""
    G_new = sign_prob["G_new"]
    G_new_n = (G_new / max(float(G_new.sum()), 1e-9)).astype(np.float32)

    S_sem = lex["S_sem"]
    S_cos = lex["S_cos_z"]
    S_swap = lex["S_swap"]
    S_swap_raw = lex["S_swap_raw"]

    # Assigned words under real `pi` vs shuffled `pi[shuf_perms]` ([N_SHUF, N])
    pi_shuf = pi[shuf_perms]

    # 1. Held-out `new texts` directional bigram semantic coherence (`S_sem` and pure `S_cos`)
    real_sem_new = float((G_new_n * S_sem[np.ix_(pi, pi)]).sum())
    real_cos_new = float((G_new_n * S_cos[np.ix_(pi, pi)]).sum())

    # Vectorized over all 1,000 shuffles via active edges!
    eu, ev = np.where(G_new_n > 0)
    ew = G_new_n[eu, ev]
    w1_s = pi_shuf[:, eu]  # [S, E]
    w2_s = pi_shuf[:, ev]  # [S, E]
    null_sem_new = (S_sem[w1_s, w2_s] * ew[None, :]).sum(axis=1)
    null_cos_new = (S_cos[w1_s, w2_s] * ew[None, :]).sum(axis=1)

    # 2. Held-out unseen Mahadevan-only swaps phonetic skeleton score
    ho_swaps = sign_prob["heldout_swaps"]
    if ho_swaps:
        su = np.array([x[0] for x in ho_swaps], dtype=np.int32)
        sv = np.array([x[1] for x in ho_swaps], dtype=np.int32)
        sw = np.array([x[2] for x in ho_swaps], dtype=np.float32)
        sw /= sw.sum()
        real_hoswap_z = float((S_swap[pi[su], pi[sv]] * sw).sum())
        real_hoswap_raw = float((S_swap_raw[pi[su], pi[sv]] * sw).sum())
        null_hoswap_z = (S_swap[pi_shuf[:, su], pi_shuf[:, sv]] * sw[None, :]).sum(axis=1)
    else:
        real_hoswap_z, real_hoswap_raw = 0.0, 0.0
        null_hoswap_z = np.zeros(len(shuf_perms))

    # Combined zero-shot unseen Mahadevan score
    real_comb = real_sem_new + 0.35 * real_hoswap_z
    null_comb = null_sem_new + 0.35 * null_hoswap_z

    def stat(r, arr):
        mu, sd = float(arr.mean()), float(arr.std())
        return {
            "real": round(float(r), 5),
            "shuf_mean": round(mu, 5),
            "shuf_sd": round(sd, 5),
            "z": round(float((r - mu) / max(sd, 1e-9)), 3),
            "P": round(float((1 + (arr >= r).sum()) / (len(arr) + 1)), 4),
        }

    return {
        "new_sem": stat(real_sem_new, null_sem_new),
        "new_cos": stat(real_cos_new, null_cos_new),
        "heldout_mah_swaps": {**stat(real_hoswap_z, null_hoswap_z), "raw_skel_rate": round(real_hoswap_raw, 4), "n_pairs": len(ho_swaps)},
        "combined_zeroshot": stat(real_comb, null_comb),
    }


def save_word_table(pi, sign_prob, lex, mode, out_path):
    N = sign_prob["N"]
    G_lipi_n = sign_prob["G_lipi"] / max(float(sign_prob["G_lipi"].sum()), 1e-9)
    G_new_n = sign_prob["G_new"] / max(float(sign_prob["G_new"].sum()), 1e-9)
    S_sem = lex["S_sem"]

    rows = []
    for u in range(N):
        w = int(pi[u])
        cats_str = "|".join(CATS[c] for c in range(13) if lex["W_cats"][w, c] > 0)
        sem_lipi_u = float(G_lipi_n[u] @ S_sem[w, pi] + G_lipi_n[:, u] @ S_sem[pi, w])
        sem_new_u = float(G_new_n[u] @ S_sem[w, pi] + G_new_n[:, u] @ S_sem[pi, w])
        rows.append({
            "rank": u + 1,
            "sign": sign_prob["signs"][u],
            "cls": sign_prob["cls"][u],
            "band": int(sign_prob["band"][u]),
            "lipi_events": int(sign_prob["uses"][u]),
            "blind_pics": ";".join(sign_prob["pics"][u]),
            "eid": lex["eids"][w],
            "headword": lex["hws"][w],
            "norm": lex["norms"][w],
            "skel": lex["skels"][w],
            "primary_gloss": lex["phrases"][w],
            "cats": cats_str,
            "rebus_raw": round(float(lex["U_rebus_raw"][u, w]), 3),
            "rebus_z": round(float(lex["U_rebus"][u, w]), 3),
            "role_z": round(float(lex["U_role"][u, w]), 3),
            "lipi_sem_contrib": round(sem_lipi_u, 5),
            "new_sem_contrib": round(sem_new_u, 5),
        })
    pd.DataFrame(rows).to_csv(out_path, index=False)


def main():
    N_DECOY_SOLVES = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    M_CAP = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
    log(f"Starting Global Dictionary QAP Solver: N=120 signs, 7 languages, N_DECOY_SOLVES={N_DECOY_SOLVES}, M_CAP={M_CAP}...")

    with open(os.path.join(DICT_EMB_DIR, "phrases.json"), encoding="utf-8") as f:
        all_phrases = json.load(f)["phrases"]
    phrase_masks = np.load(os.path.join(DICT_EMB_DIR, "phrase_masks.npy"))
    emb_m2v_all = np.load(os.path.join(DICT_EMB_DIR, "emb_m2v.npy"))

    sign_prob = build_sign_problem(n_signs=120)
    ext_priors = build_external_m2v_priors(emb_m2v_all, phrase_masks, all_phrases)
    shuf_perms_1000 = make_sign_shuffles(sign_prob["N"], sign_prob["cls"], sign_prob["band"], n_shuf=1000, seed=9001)
    decoy_corpus_perms = make_sign_shuffles(sign_prob["N"], sign_prob["cls"], sign_prob["band"], n_shuf=N_DECOY_SOLVES, seed=7700)

    lexicons = {}
    for lang, dnames in CANDIDATE_LANGS.items():
        lexicons[lang] = load_language_lexicon(lang, dnames, sign_prob, all_phrases, phrase_masks, emb_m2v_all, ext_priors, m_cap=M_CAP)

    summary = {"config": {"N_signs": 120, "N_decoy_solves": N_DECOY_SOLVES, "M_cap": M_CAP}, "modes": {}}

    for mode in ("free", "anchored"):
        log(f"================ SOLVER MODE: {mode.upper()} ================")
        mode_res = {}
        for lang, lex in lexicons.items():
            t_lang = time.time()
            # 1. Solve on REAL Lipi corpus
            pi_real, lipi_bd = solve_qap_global(
                sign_prob["G_lipi"], sign_prob["G_swap_lipi"], sign_prob["G_base_lipi"],
                sign_prob["lipi_splits"], lex["U_rebus"], lex["U_role"], lex,
                mode=mode, seed=2026, n_starts=4, n_sweeps=18
            )
            zs_real = eval_zeroshot_new(pi_real, sign_prob, lex, shuf_perms_1000)
            save_word_table(pi_real, sign_prob, lex, mode, os.path.join(OUT_DIR, f"qap_words_{lang}_{mode}.csv"))

            # 2. Control (ii): Fit EXACT SAME SOLVER on `N_DECOY_SOLVES` sign-permuted Lipi decoy corpora!
            # Sign `u` gets sign `p[u]`'s Lipi training occurrences/swaps/splits (within same class + band),
            # while keeping sign `u`'s REAL picture (`U_rebus`), REAL compound shape (`G_base_raw`), and REAL unseen `new texts`!
            decoy_lipi_totals = []
            decoy_lipi_rebus = []
            decoy_lipi_base = []
            decoy_new_sem = []
            decoy_new_comb = []
            for d_idx in range(N_DECOY_SOLVES):
                p = decoy_corpus_perms[d_idx]
                inv_p = np.argsort(p)
                G_lipi_dec = sign_prob["G_lipi"][np.ix_(p, p)]
                G_swap_dec = sign_prob["G_swap_lipi"][np.ix_(p, p)]
                perm_raw_splits = {
                    (int(inv_p[c]), int(inv_p[a]), int(inv_p[b])): frs
                    for (c, a, b), frs in sign_prob["lipi_splits_raw"].items()
                }
                splits_dec, G_base_dec = sign_prob["build_splits_fn"](perm_raw_splits, sign_prob["G_base_raw"])

                pi_dec, bd_dec = solve_qap_global(
                    G_lipi_dec, G_swap_dec, G_base_dec,
                    splits_dec, lex["U_rebus"], lex["U_role"], lex,
                    mode=mode, seed=3000 + d_idx, n_starts=4, n_sweeps=18
                )
                zs_dec = eval_zeroshot_new(pi_dec, sign_prob, lex, shuf_perms_1000[:200])
                decoy_lipi_totals.append(bd_dec["total"])
                decoy_lipi_rebus.append(bd_dec["unary"])
                decoy_lipi_base.append(bd_dec["base"] + 0.5 * bd_dec["split3"])
                decoy_new_sem.append(zs_dec["new_sem"]["real"])
                decoy_new_comb.append(zs_dec["combined_zeroshot"]["real"])

            def cmp_decoy(r_val, d_list):
                arr = np.asarray(d_list, dtype=np.float64)
                mu, sd = float(arr.mean()), float(arr.std())
                return {
                    "real": round(float(r_val), 5),
                    "decoy_mean": round(mu, 5),
                    "decoy_sd": round(sd, 5),
                    "z_vs_decoy_solves": round(float((r_val - mu) / max(sd, 1e-9)), 3),
                    "P_vs_decoy_solves": round(float((1 + (arr >= r_val).sum()) / (len(arr) + 1)), 4),
                }

            c2_lipi = cmp_decoy(lipi_bd["total"], decoy_lipi_totals)
            c2_lock = cmp_decoy(lipi_bd["unary"] + lipi_bd["base"] + 0.5 * lipi_bd["split3"],
                                np.array(decoy_lipi_rebus) + np.array(decoy_lipi_base))
            c2_new_sem = cmp_decoy(zs_real["new_sem"]["real"], decoy_new_sem)
            c2_new_comb = cmp_decoy(zs_real["combined_zeroshot"]["real"], decoy_new_comb)

            mode_res[lang] = {
                "M_pool": lex["M"],
                "lipi_objective": {k: round(v, 5) for k, v in lipi_bd.items()},
                "zeroshot_vs_1000_shuffles": zs_real,
                "vs_decoy_lipi_solves": {
                    "lipi_total": c2_lipi,
                    "rebus_compound_lock": c2_lock,
                    "zeroshot_new_sem": c2_new_sem,
                    "zeroshot_combined": c2_new_comb,
                },
                "elapsed_s": round(time.time() - t_lang, 1),
            }
            log(f"[{mode:8s}] {lang:11s} (M={lex['M']:4d}, {time.time()-t_lang:4.1f}s) | "
                f"Lipi tot={lipi_bd['total']:+.4f} (vs decoy-solve z={c2_lipi['z_vs_decoy_solves']:+5.2f} P={c2_lipi['P_vs_decoy_solves']:.3f}) | "
                f"New sem z={zs_real['new_sem']['z']:+5.2f} (P={zs_real['new_sem']['P']:.3f}) | "
                f"HO-swap z={zs_real['heldout_mah_swaps']['z']:+5.2f} | "
                f"New vs decoy-solve z={c2_new_comb['z_vs_decoy_solves']:+5.2f}")
        summary["modes"][mode] = mode_res

    with open(os.path.join(OUT_DIR, "qap_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    log("Saved qap_summary.json and all 14 qap_words_<lang>_<mode>.csv tables!")


if __name__ == "__main__":
    main()
