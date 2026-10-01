#!/usr/bin/env python3
"""context_002: is there a 002-specific end effect?

Run:  python3 research/extensions_20261001/context_002/context_002.py   (numpy + scipy, deterministic, writes context_002_results.json)

Data: Lipi metadata_filtered.csv, rows with dir. == R/L, STORED order. Under the conventional (Mahadevan) reading
direction stored-final = reading-INITIAL, and "002 immediately before Y in stored order" = "Y immediately before 002 in
reading order". Everything below is stated in stored terms; the reading-order translation is in REPORT.md.

Rules (strict): right end of the text intact (text ends with '+'); exact duplicate texts collapsed to one vote; an occurrence of
Y counts only if it has a known predecessor token (non-000, i.e. Y is not text-initial and the predecessor is legible).
Outcome: Y is the last token in stored order. Predictor: predecessor == 002.
Y set: signs that follow 002 at least MIN_AFTER times in that data.
Model: logit P(final) = alpha_Y + beta * pre002   (per-Y intercept). Per-Y: 2x2 table, Haldane-corrected odds ratio, Woolf CI,
Fisher exact p, Holm across Y. Pooled: stratified (per-Y intercept) logistic fit by Newton, Wald CI, permutation p
(pre002 flags shuffled within Y), Mantel-Haenszel OR. Sensitivity: row-length dummies; length>=3 only; placebo scan over
other predecessors.
"""
import csv, json, os, re, math, collections
import numpy as np
from scipy.stats import fisher_exact

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
MIN_AFTER = 5
NPERM = 20000
SEED = 20261003

def load_rows():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data/open_prototype/lipi/metadata_filtered.csv"))))
    seen, out = set(), []
    n_rl = n_intact = 0
    for x in rows:
        if x["dir."].strip() != "R/L":
            continue
        n_rl += 1
        t = x["text"].strip()
        if not t.endswith("+"):
            continue
        n_intact += 1
        if t in seen:
            continue
        seen.add(t)
        toks = [s for s in re.split(r"-", t.strip("+[]")) if s]
        out.append((toks, t.startswith("+")))
    return out, {"rows_total": len(rows), "rows_RL": n_rl, "rows_RL_right_end_intact": n_intact, "distinct_texts_used": len(out)}

def occurrences(texts, include_initial=False):
    """one record per Y occurrence with a legible predecessor: (Y, pred, is_final, text_length).
    include_initial=True also keeps text-initial tokens (predecessor "^", cannot be 002) -- sensitivity only."""
    occ = []
    for toks, left_intact in texts:
        L = len(toks)
        if include_initial and left_intact and toks[0] != "000":
            occ.append((toks[0], "^", int(L == 1), L))
        for i in range(1, L):
            y, p = toks[i], toks[i - 1]
            if y == "000" or p == "000":
                continue
            occ.append((y, p, int(i == L - 1), L))
    return occ

def sexp(x):
    return math.exp(max(-30.0, min(30.0, x)))

def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i])
    adj = [0.0] * len(ps); run = 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (len(ps) - r) * ps[i])); adj[i] = run
    return adj

def per_y(occ, X="002"):
    by = collections.defaultdict(lambda: [[0, 0], [0, 0]])  # [pre?][final?]
    for y, p, f, L in occ:
        by[y][int(p == X)][f] += 1
    ys = sorted(y for y, t in by.items() if t[1][0] + t[1][1] >= MIN_AFTER and t[0][0] + t[0][1] > 0)
    res = []
    for y in ys:
        (a0, b0), (a1, b1) = by[y]  # a=non-final, b=final ; row0 = not preceded, row1 = preceded
        orr, p = fisher_exact([[b1, a1], [b0, a0]])
        hb1, ha1, hb0, ha0 = b1 + .5, a1 + .5, b0 + .5, a0 + .5
        lor = math.log(hb1 * ha0 / (ha1 * hb0)); se = math.sqrt(1 / hb1 + 1 / ha1 + 1 / hb0 + 1 / ha0)
        res.append({"Y": y, "after_X_n": a1 + b1, "after_X_final": b1, "other_n": a0 + b0, "other_final": b0,
                    "P_final_after_X": round(b1 / (a1 + b1), 3), "P_final_otherwise": round(b0 / (a0 + b0), 3),
                    "odds_ratio_haldane": round(math.exp(lor), 2),
                    "ci95": [round(math.exp(lor - 1.96 * se), 2), round(math.exp(lor + 1.96 * se), 2)],
                    "fisher_p_two_sided": float(p)})
    adj = holm([r["fisher_p_two_sided"] for r in res])
    for r, a in zip(res, adj):
        r["holm_p"] = round(a, 5); r["fisher_p_two_sided"] = float(f"{r['fisher_p_two_sided']:.3g}")
    return res, ys

def pooled(occ, ys, X="002", len_dummies=False, min_len=2, seed=SEED, nperm=NPERM):
    d = [(y, int(p == X), f, L) for y, p, f, L in occ if y in ys and L >= min_len]
    yi = {y: i for i, y in enumerate(ys)}
    Y = np.array([yi[r[0]] for r in d]); z = np.array([r[1] for r in d], float)
    f = np.array([r[2] for r in d], float); L = np.array([r[3] for r in d])
    cols = [(Y == i).astype(float) for i in range(len(ys))]
    cols.append(z)
    if len_dummies:
        for k in (3, 4, 5):
            cols.append((L == k).astype(float) if k < 5 else (L >= 5).astype(float))
    X_ = np.column_stack(cols)
    beta = np.zeros(X_.shape[1])
    for _ in range(100):
        eta = np.clip(X_ @ beta, -30, 30); mu = 1 / (1 + np.exp(-eta))
        W = mu * (1 - mu)
        H = X_.T @ (X_ * W[:, None]) + 1e-4 * np.eye(len(beta))
        step = np.linalg.solve(H, X_.T @ (f - mu))
        beta += step
        if np.abs(step).max() < 1e-9:
            break
    cov = np.linalg.inv(X_.T @ (X_ * W[:, None]) + 1e-4 * np.eye(len(beta)))
    j = len(ys); b = beta[j]; se = math.sqrt(cov[j, j])
    # Mantel-Haenszel and within-Y permutation of the pre-X flag
    def mh(zz):
        num = den = 0.0
        for i in range(len(ys)):
            m = Y == i
            n = m.sum()
            a = ((zz == 1) & (f == 1) & m).sum(); b_ = ((zz == 1) & (f == 0) & m).sum()
            c = ((zz == 0) & (f == 1) & m).sum(); d_ = ((zz == 0) & (f == 0) & m).sum()
            num += a * d_ / n; den += b_ * c / n
        return num / den if den else float("inf")
    stat = lambda zz: int(((zz == 1) & (f == 1)).sum())
    obs = stat(z)
    rng = np.random.default_rng(seed)
    idx = [np.where(Y == i)[0] for i in range(len(ys))]
    sims = np.empty(nperm)
    for k in range(nperm):
        zp = z.copy()
        for ix in idx:
            zp[ix] = z[ix][rng.permutation(len(ix))]
        sims[k] = stat(zp)
    return {"n_occurrences": len(d), "n_after_X": int(z.sum()), "n_after_X_final": int(((z == 1) & (f == 1)).sum()),
            "expected_final_after_X_under_per_Y_baseline": round(float(sims.mean()), 2),
            "logistic_beta": round(float(b), 3), "odds_ratio": round(sexp(b), 2) if abs(b) < 8 else None,
            "ci95": [round(sexp(b - 1.96 * se), 2), round(sexp(b + 1.96 * se), 2)] if abs(b) < 8 else None,
            "wald_z": round(float(b / se), 2), "mantel_haenszel_or": round(mh(z), 2),
            "perm_p_one_sided": round(float(((sims >= obs).sum() + 1) / (NPERM + 1)), 5)}

def placebo(occ, top=25):
    """Same pooled model for every frequent predecessor X (own Y set). Shows where 002 ranks."""
    cnt = collections.Counter(p for y, p, f, L in occ)
    out = []
    for X, n in cnt.most_common(top):
        if X == "000":
            continue
        res, ys = per_y(occ, X)
        if len(ys) < 2:
            continue
        pl = pooled(occ, ys, X, seed=SEED + 5, nperm=2000)
        out.append({"X": X, "n_Y": len(ys), "n_after_X": pl["n_after_X"], "odds_ratio": pl["odds_ratio"], "ci95": pl["ci95"],
                    "perm_p_one_sided": pl["perm_p_one_sided"]})
    return out

def crosswalk_check():
    p = os.path.join(ROOT, "data/sign_crosswalk/crosswalk_edges.csv")
    edges = list(csv.DictReader(open(p)))
    mine = [e for e in edges if e["from_sign_uid"] == "lipi_numeric:002"]
    to_mah = [e for e in edges if e["to_sign_uid"].startswith("mayig_mahadevan_m:") and e["from_sign_uid"].startswith("lipi_numeric:")]
    exact = [e for e in edges if e["mapping_state"] == "exact"]
    return {"edges_from_lipi_002": [{"edge_id": e["edge_id"], "to": e["to_sign_uid"], "mapping_state": e["mapping_state"],
                                     "accepted_for_analysis": e["accepted_for_analysis"], "review_status": e["review_status"]} for e in mine],
            "direct_edges_lipi_to_mahadevan_namespace": len(to_mah),
            "exact_edges_in_whole_crosswalk": [{"edge_id": e["edge_id"], "from": e["from_sign_uid"], "to": e["to_sign_uid"]} for e in exact],
            "verdict": "no exact Lipi 002 -> Mahadevan mapping; Mahadevan replication not run"}

def main():
    texts, meta = load_rows()
    occ = occurrences(texts)
    meta["occurrences_with_legible_predecessor"] = len(occ)
    meta["occurrences_after_002"] = sum(1 for o in occ if o[1] == "002")
    res, ys = per_y(occ)
    out = {"nperm": NPERM, "seed": SEED, "data": meta, "Y_set": ys, "min_after_002": MIN_AFTER}
    out["per_Y"] = sorted(res, key=lambda r: -r["after_X_n"])
    out["pooled_per_Y_intercept"] = pooled(occ, ys)
    out["pooled_plus_length_dummies"] = pooled(occ, ys, len_dummies=True, seed=SEED + 1)
    out["pooled_length_ge_3_only"] = pooled(occ, ys, min_len=3, seed=SEED + 2)
    nz = [y for y in ys]
    # leave-one-Y-out
    occ2 = occurrences(texts, include_initial=True)
    res2, ys2 = per_y(occ2)
    out["sensitivity_include_text_initial_tokens"] = {
        "per_Y": {r["Y"]: {"OR": r["odds_ratio_haldane"], "ci95": r["ci95"], "holm_p": r["holm_p"], "P_final_otherwise": r["P_final_otherwise"]} for r in res2},
        "pooled": pooled(occ2, ys2, seed=SEED + 4)}
    out["leave_one_Y_out_pooled_OR"] = {y: pooled(occ, [k for k in ys if k != y], seed=SEED + 3, nperm=200)["odds_ratio"] for y in ys}
    out["placebo_other_predecessors"] = placebo(occ)
    out["mahadevan_replication"] = crosswalk_check()
    path = os.path.join(HERE, "context_002_results.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True); fh.write("\n")
    print(json.dumps(out, indent=1, sort_keys=True))

if __name__ == "__main__":
    main()
