#!/usr/bin/env python3
"""front_count: does the front inscription predict the cup + N-stroke count on two-sided miniature tablets?

Run from anywhere:  python3 research/extensions_20261001/front_count/front_count.py
Needs numpy only. Deterministic (fixed seeds). Writes front_count_results.json next to this file.

Parts
  a) Mahadevan 1977 paired objects (85): research/data/mahadevan_20260905/paired_objects.json
  b) Lipi two-sided tablets with a cup(700)+strokes(032/033/034 = 2/3/4) face, strict rules
  c) Held-out: fit lookup on Harappa H-1..H-1499, score on Harappa HARP-era objects (rule in REPORT.md)
"""
import csv, json, os, re, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))  # research/
NPERM = 20000
SEED = 20261001

# ---------------------------------------------------------------- statistics
def encode(keys):
    u = {k: i for i, k in enumerate(sorted(set(keys)))}
    return np.array([u[k] for k in keys]), len(u)

def table(f, c, nf, nc):
    return np.bincount(f * nc + c, minlength=nf * nc).reshape(nf, nc)

def stats_from(f, c, nf, nc):
    T = table(f, c, nf, nc)
    n = T.sum()
    rows, cols = T.sum(1, keepdims=True), T.sum(0, keepdims=True)
    E = rows * cols / n
    nz = E > 0
    chi2 = float((((T - E) ** 2)[nz] / E[nz]).sum())
    P = T / n
    with np.errstate(divide="ignore", invalid="ignore"):
        mi = np.nansum(np.where(T > 0, P * np.log2(P / (rows / n * cols / n)), 0.0))
    G = T.sum(0)
    # leave-one-out lookup accuracy
    oh = np.eye(nc, dtype=int)[c]
    M = T[f] - oh
    Gm = G[None, :] - oh
    fallback = M.sum(1) == 0
    M = np.where(fallback[:, None], Gm, M)
    pred = np.argmax(M + 1e-6 * Gm, axis=1)
    loo = float((pred == c).sum())
    return {
        "fronts_varying": int(((T > 0).sum(1) > 1).sum()),
        "fronts_all_counts": int(((T > 0).sum(1) == nc).sum()),
        "lookup_hits": int(T.max(1).sum()),
        "loo_hits": int(loo),
        "mi_bits": float(mi),
        "chi2": chi2,
    }

HIGH = ["lookup_hits", "loo_hits", "mi_bits", "chi2", "fronts_all_counts"]  # P(null >= obs)
LOW = ["fronts_varying"]                                                    # P(null <= obs)

def perm_test(fronts, counts, strata=None, nperm=NPERM, seed=SEED):
    """Permute counts across objects (unrestricted) or within `strata` labels."""
    f, nf = encode(fronts)
    cvals = sorted(set(counts))
    c = np.array([cvals.index(x) for x in counts])
    nc = len(cvals)
    obs = stats_from(f, c, nf, nc)
    rng = np.random.default_rng(seed)
    if strata is None:
        groups = [np.arange(len(c))]
    else:
        d = collections.defaultdict(list)
        for i, s in enumerate(strata):
            d[s].append(i)
        groups = [np.array(v) for v in d.values()]
    sims = {k: np.empty(nperm) for k in obs}
    for p in range(nperm):
        cp = c.copy()
        for g in groups:
            if len(g) > 1:
                cp[g] = c[g][rng.permutation(len(g))]
        s = stats_from(f, cp, nf, nc)
        for k in obs:
            sims[k][p] = s[k]
    out = {"n_objects": len(c), "n_fronts": nf, "n_strata": len(groups),
           "count_levels": cvals, "obs": obs, "null_mean": {}, "p": {}}
    for k in obs:
        out["null_mean"][k] = round(float(sims[k].mean()), 4)
        if k in LOW:
            out["p"][k] = round(float(((sims[k] <= obs[k] + 1e-9).sum() + 1) / (nperm + 1)), 4)
        else:
            out["p"][k] = round(float(((sims[k] >= obs[k] - 1e-9).sum() + 1) / (nperm + 1)), 4)
    out["obs"] = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in obs.items()}
    return out

def cross_group_test(fronts, counts, groups, perm_strata=None, nperm=NPERM, seed=SEED):
    """Cross-batch prediction. For each object, predict its count from the modal count of OBJECTS WITH THE SAME FRONT IN A
    DIFFERENT group (locus / area-section). Only objects that have such a partner are scored. Null: permute counts within
    `perm_strata` (default: within `groups`, so group-level count composition cannot create the signal)."""
    f, nf = encode(fronts)
    cvals = sorted(set(counts)); c = np.array([cvals.index(x) for x in counts]); nc = len(cvals)
    g, _ = encode(groups)
    n = len(c)
    A = ((f[:, None] == f[None, :]) & (g[:, None] != g[None, :])).astype(float)
    elig = A.sum(1) > 0
    G = np.bincount(c, minlength=nc).astype(float)
    def hits(cc):
        V = A @ np.eye(nc)[cc]
        pred = np.argmax(V + 1e-6 * G[None, :], axis=1)
        return int(((pred == cc) & elig).sum())
    obs = hits(c)
    strata = g if perm_strata is None else encode(perm_strata)[0]
    idx = [np.where(strata == s)[0] for s in np.unique(strata)]
    rng = np.random.default_rng(seed)
    sims = np.empty(nperm)
    for p in range(nperm):
        cp = c.copy()
        for gi in idx:
            if len(gi) > 1:
                cp[gi] = c[gi][rng.permutation(len(gi))]
        sims[p] = hits(cp)
    # baseline for the same eligible objects: always predict global mode
    base = int(((c == int(np.argmax(G))) & elig).sum())
    return {"eligible_objects": int(elig.sum()), "cross_group_hits": obs, "global_mode_hits_same_objects": base,
            "null_mean_hits": round(float(sims.mean()), 3),
            "P_ge_obs": round(float(((sims >= obs).sum() + 1) / (nperm + 1)), 4)}

# ---------------------------------------------------------------- (a) Mahadevan
def mahadevan():
    d = json.load(open(os.path.join(ROOT, "data/mahadevan_20260905/paired_objects.json")))
    fronts = [" ".join(o["front"]["tokens_raw"]) for o in d]
    counts = [o["long_stroke_count"] for o in d]
    locus = [o["front"]["locus"] for o in d]
    res = {"n": len(d), "locus_counts_top": collections.Counter(locus).most_common(5)}
    res["unrestricted"] = perm_test(fronts, counts, None, seed=SEED)
    res["within_locus"] = perm_test(fronts, counts, locus, seed=SEED + 1)
    idx = [i for i, l in enumerate(locus) if l == "42"]
    res["locus42_only_n"] = len(idx)
    res["locus42_only"] = perm_test([fronts[i] for i in idx], [counts[i] for i in idx], None, seed=SEED + 2)
    idx2 = [i for i, l in enumerate(locus) if l != "42"]
    res["not_locus42_n"] = len(idx2)
    res["not_locus42"] = perm_test([fronts[i] for i in idx2], [counts[i] for i in idx2], [locus[i] for i in idx2], seed=SEED + 4)
    bigf = collections.Counter(fronts).most_common(1)[0][0]
    idx3 = [i for i, x in enumerate(fronts) if x != bigf]
    res["largest_family"] = {"front": bigf, "n": len(fronts) - len(idx3)}
    res["without_largest_family_within_locus"] = perm_test([fronts[i] for i in idx3], [counts[i] for i in idx3], [locus[i] for i in idx3], seed=SEED + 5)
    res["cross_locus"] = cross_group_test(fronts, counts, locus, None, seed=SEED + 3)
    fam = collections.Counter(fronts)
    res["front_family_sizes"] = sorted(fam.values(), reverse=True)[:8]
    return res

# ---------------------------------------------------------------- (b) Lipi
CUP = re.compile(r"\+(700-(03[234])|(03[234])-700)\+")
CLEAN = re.compile(r"\+[0-9]{3}(-[0-9]{3})*\+")
STROKES = {"032": 2, "033": 3, "034": 4}
HARP_ID = re.compile(r"^H\d{2,4}-")

def load_lipi_objects():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data/open_prototype/lipi/metadata_filtered.csv"))))
    by = collections.defaultdict(list)
    for x in rows:
        by[x["id"].split(".")[0]].append(x)
    objs = []
    for k, v in by.items():
        if len(v) != 2 or not v[0]["type"].startswith("TAB") or v[0]["sides"] != "2":
            continue
        cs = [x for x in v if CUP.fullmatch(x["text"])]
        if len(cs) != 1:  # none, or cup+strokes on both faces (ambiguous front)
            continue
        cu = cs[0]
        fr = v[0] if v[1] is cu else v[1]
        m = CUP.fullmatch(cu["text"])
        count = STROKES[m.group(2) or m.group(3)]
        cisi = v[0]["cisi"]
        hnum = int(cisi[2:]) if re.fullmatch(r"H-\d+", cisi) else None
        idno = v[0]["excavation-idno"]
        if hnum is not None:
            era = "old" if hnum < 1500 else "harp"
        elif HARP_ID.match(idno):
            era = "harp"
        else:
            era = "unassigned"
        if hnum is None and era == "harp":
            pass
        objs.append({
            "id": k, "cisi": cisi, "site": v[0]["site"], "area": v[0]["area-section"], "era": era,
            "hnum": hnum, "count": count, "cup_order": "700_first" if m.group(2) else "700_last",
            "front": fr["text"], "front_complete": fr["complete"], "cup_complete": cu["complete"],
            "front_clean": bool(CLEAN.fullmatch(fr["text"])) and "000" not in fr["text"],
            "preservation": v[0]["preservation"], "condition": v[0]["condition"],
            "dir_front": fr["dir."], "type": v[0]["type"],
        })
    return objs

def strict(o, level):
    base = o["front_complete"] == "Y" and o["cup_complete"] == "Y" and o["front_clean"]
    if level == "relaxed":
        return base
    ok = base and o["preservation"] not in ("fragment", "partly damaged")
    if level == "strict":
        return ok
    if level == "strict_fair_or_better":
        return ok and o["condition"] in ("Fair", "Good", "Fine")
    raise ValueError(level)

def lipi():
    objs = load_lipi_objects()
    res = {"two_sided_cup_stroke_tablets_before_filters": len(objs)}
    S = [o for o in objs if strict(o, "strict")]
    res["strict_n"] = len(S)
    res["strict_by_count"] = dict(collections.Counter(o["count"] for o in S))
    res["strict_by_site"] = dict(collections.Counter(o["site"] for o in S))
    res["strict_by_era"] = dict(collections.Counter(o["era"] for o in S))
    res["relaxed_n"] = sum(strict(o, "relaxed") for o in objs)
    fr = [o["front"] for o in S]; ct = [o["count"] for o in S]
    res["strict_unrestricted"] = perm_test(fr, ct, None, seed=SEED + 10)
    res["strict_within_site"] = perm_test(fr, ct, [o["site"] for o in S], seed=SEED + 11)
    res["strict_within_era"] = perm_test(fr, ct, [o["era"] for o in S], seed=SEED + 12)
    res["strict_within_area_section"] = perm_test(fr, ct, [o["site"] + "|" + o["area"] for o in S], seed=SEED + 13)
    res["strict_within_era_x_area"] = perm_test(fr, ct, [o["era"] + "|" + o["area"] for o in S], seed=SEED + 14)
    # sensitivity
    R = [o for o in objs if strict(o, "relaxed")]
    res["relaxed_unrestricted"] = perm_test([o["front"] for o in R], [o["count"] for o in R], None, seed=SEED + 15)
    res["relaxed_within_era_x_area"] = perm_test([o["front"] for o in R], [o["count"] for o in R], [o["era"] + "|" + o["area"] for o in R], seed=SEED + 16)
    F = [o for o in objs if strict(o, "strict_fair_or_better")]
    res["fair_or_better_n"] = len(F)
    res["fair_or_better_within_era"] = perm_test([o["front"] for o in F], [o["count"] for o in F], [o["era"] for o in F], seed=SEED + 17)
    O = [o for o in S if o["cup_order"] == "700_first"]
    res["cup_first_only_n"] = len(O)
    res["cup_first_only_within_era"] = perm_test([o["front"] for o in O], [o["count"] for o in O], [o["era"] for o in O], seed=SEED + 18)
    # cross-batch: predict from same-front objects in a DIFFERENT area-section (null: counts permuted within area-section)
    ga = [o["site"] + "|" + o["area"] for o in S]
    res["strict_cross_area_section"] = cross_group_test(fr, ct, ga, None, seed=SEED + 19)
    ge = [o["era"] + "|" + o["area"] for o in S]
    res["strict_cross_era_x_area"] = cross_group_test(fr, ct, ge, None, seed=SEED + 20)
    # same, leaving out the one 28-object formula family (400-740-176) to show it does not carry the result
    big = collections.Counter(fr).most_common(1)[0][0]
    keep = [i for i, x in enumerate(fr) if x != big]
    res["largest_front_family"] = {"front": big, "n": len(fr) - len(keep)}
    res["strict_without_largest_family_within_era_x_area"] = perm_test([fr[i] for i in keep], [ct[i] for i in keep], [ge[i] for i in keep], seed=SEED + 21)
    res["strict_without_largest_family_cross_area"] = cross_group_test([fr[i] for i in keep], [ct[i] for i in keep], [ga[i] for i in keep], None, seed=SEED + 22)
    return res, S

# ---------------------------------------------------------------- (c) held-out
def fit_lookup(train):
    by = collections.defaultdict(collections.Counter)
    G = collections.Counter()
    for o in train:
        by[o["front"]][o["count"]] += 1
        G[o["count"]] += 1
    gmode = sorted(G, key=lambda k: (-G[k], k))[0]
    table_ = {f: sorted(c, key=lambda k: (-c[k], -G[k], k))[0] for f, c in by.items()}
    return table_, gmode

def predict(table_, gmode, front):
    return table_.get(front, gmode), front in table_

def heldout(S):
    train = [o for o in S if o["era"] == "old"]
    test = [o for o in S if o["era"] == "harp"]
    tab, gmode = fit_lookup(train)
    pred = [predict(tab, gmode, o["front"]) for o in test]
    y = np.array([o["count"] for o in test])
    p = np.array([a for a, _ in pred]); cov = np.array([b for _, b in pred])
    res = {"train_n": len(train), "train_fronts": len(tab), "train_by_count": dict(collections.Counter(o["count"] for o in train)),
           "train_global_mode": gmode, "test_n": len(test), "test_by_count": dict(collections.Counter(int(v) for v in y)),
           "test_fronts_seen_in_train": int(cov.sum())}
    res["lookup_hits"] = int((p == y).sum())
    res["lookup_acc"] = round(float((p == y).mean()), 4)
    res["majority_hits"] = int((y == gmode).sum())
    res["majority_acc"] = round(float((y == gmode).mean()), 4)
    res["test_majority_class_acc_oracle"] = round(float(max(collections.Counter(y.tolist()).values()) / len(y)), 4)
    if cov.sum():
        res["covered_n"] = int(cov.sum())
        res["covered_lookup_hits"] = int((p[cov] == y[cov]).sum())
        res["covered_majority_hits"] = int((y[cov] == gmode).sum())
    # null 1: shuffle held-out counts (fixed predictions), overall and within area-section
    rng = np.random.default_rng(SEED + 30)
    sims = np.array([(p == rng.permutation(y)).sum() for _ in range(NPERM)])
    res["null_shuffle_test_counts"] = {"mean_hits": round(float(sims.mean()), 3),
                                       "P_ge_obs": round(float(((sims >= res["lookup_hits"]).sum() + 1) / (NPERM + 1)), 4)}
    strata = collections.defaultdict(list)
    for i, o in enumerate(test):
        strata[o["area"]].append(i)
    rng = np.random.default_rng(SEED + 31)
    sims2 = np.empty(NPERM)
    for k in range(NPERM):
        yy = y.copy()
        for g in strata.values():
            g = np.array(g)
            if len(g) > 1:
                yy[g] = y[g][rng.permutation(len(g))]
        sims2[k] = (p == yy).sum()
    res["null_shuffle_test_counts_within_area"] = {"n_strata": len(strata), "mean_hits": round(float(sims2.mean()), 3),
        "P_ge_obs": round(float(((sims2 >= res["lookup_hits"]).sum() + 1) / (NPERM + 1)), 4)}
    # null 2: shuffle TRAIN counts (breaks the learned front->count association), refit, score on the true held-out
    rng = np.random.default_rng(SEED + 32)
    tc = np.array([o["count"] for o in train])
    sims3 = np.empty(NPERM)
    for k in range(NPERM):
        tp = tc[rng.permutation(len(tc))]
        tr2 = [dict(o, count=int(c)) for o, c in zip(train, tp)]
        t2, g2 = fit_lookup(tr2)
        sims3[k] = sum(predict(t2, g2, o["front"])[0] == o["count"] for o in test)
    res["null_shuffle_train_counts"] = {"mean_hits": round(float(sims3.mean()), 3),
        "P_ge_obs": round(float(((sims3 >= res["lookup_hits"]).sum() + 1) / (NPERM + 1)), 4)}
    # honest side check: front-seen fronts' own repeat rate
    res["note_split_gap"] = {"max_old_hnum": max(o["hnum"] for o in S if o["era"] == "old" and o["hnum"]),
                             "min_harp_hnum": min(o["hnum"] for o in S if o["era"] == "harp" and o["hnum"])}
    return res

def main():
    out = {"nperm": NPERM, "seed": SEED}
    out["a_mahadevan"] = mahadevan()
    b, S = lipi()
    out["b_lipi"] = b
    out["c_heldout"] = heldout(S)
    path = os.path.join(HERE, "front_count_results.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps(out, indent=1, sort_keys=True))

if __name__ == "__main__":
    main()
