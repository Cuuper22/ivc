#!/usr/bin/env python3
"""size_034: are cup+4-stroke (034) tablets smaller than 032/033 tablets of the same format?

Run:  python3 research/extensions_20261001/size_034/size_034.py      (numpy only, deterministic, writes size_034_results.json)

Objects: the 309 Harappa FRAME700 tablets with positive horizontal and vertical size and complete text on the short face,
from frame700_034_size_tier_heldout_20260712_predictions.csv, joined to Lipi metadata_filtered.csv by row id.
Unit of analysis: one vote per near-duplicate text family (source_group = identical longer text on the other face, or the
whole H-2218..H-2239 series) x format x group (034 vs 032/033): the cell mean of log(area). No single-object gate.
"""
import csv, json, os, collections, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
NPERM = 20000
NBOOT = 5000
SEED = 20261002

def load():
    pred = list(csv.DictReader(open(os.path.join(ROOT, "data/open_prototype/reports/frame700_034_size_tier_heldout_20260712_predictions.csv"))))
    lipi = {x["id"]: x for x in csv.DictReader(open(os.path.join(ROOT, "data/open_prototype/lipi/metadata_filtered.csv")))}
    objs = []
    for p in pred:
        l = lipi[p["row_id"]]
        h, v = float(l["horizontal(mm)"]), float(l["vertical(mm)"])
        assert h > 0 and v > 0 and l["cisi"] == p["cisi"]
        hn = int(p["cisi"][2:])
        mat = l["material"].strip().lower()
        objs.append({
            "cisi": p["cisi"], "sub": p["subtype"], "is034": int(p["subtype"] == "034"),
            "family": p["source_group"], "format": l["type"] + "|" + ("2" if l["sides"] == "2" else "3+"),
            "logA": math.log(h * v), "logH": math.log(h), "logV": math.log(v),
            "era": "harp" if hn >= 1500 else "old",
            "material": mat if mat in ("steatite", "faience") else "other",
            "area": l["area-section"], "period": l["period"], "phase": l["phase"],
            "preservation": l["preservation"], "order": p["order"],
        })
    return objs, lipi

def usable_counts(lipi):
    import re
    cup = re.compile(r"\+(700-03[234]|03[234]-700)\+")
    rows = [x for x in lipi.values() if cup.fullmatch(x["text"]) and x["type"].startswith("TAB")]
    cis = collections.defaultdict(list)
    for x in rows:
        cis[x["cisi"] if x["cisi"] != "-" else "id" + x["id"]].append(x)
    pos = [k for k, v in cis.items() if float(v[0]["horizontal(mm)"] or 0) > 0 and float(v[0]["vertical(mm)"] or 0) > 0]
    return {"lipi_tablet_objects_with_short_700_03x_face": len(cis), "with_positive_dimensions": len(pos),
            "of_which_in_frozen_309": None}

def cells(objs, key_group=lambda o: o["is034"]):
    d = collections.defaultdict(list)
    for o in objs:
        d[(o["family"], o["format"], key_group(o))].append(o)
    out = []
    for (fam, fmt, g), v in d.items():
        out.append({"family": fam, "format": fmt, "g": g, "n": len(v), "y": float(np.mean([o["logA"] for o in v])),
                    "era": collections.Counter(o["era"] for o in v).most_common(1)[0][0],
                    "material": collections.Counter(o["material"] for o in v).most_common(1)[0][0],
                    "area": collections.Counter(o["area"] for o in v).most_common(1)[0][0],
                    "phase": collections.Counter(o["phase"] for o in v).most_common(1)[0][0],
                    "period": collections.Counter(o["period"] for o in v).most_common(1)[0][0]})
    out.sort(key=lambda c: (c["family"], c["format"], c["g"]))
    return out

def strat_diff(y, g, s):
    """Weighted within-stratum mean difference (g=1 minus g=0); weight n1*n0/(n1+n0). Strata lacking a group drop out."""
    num = den = 0.0
    for lab in np.unique(s):
        m = s == lab
        a, b = y[m & (g == 1)], y[m & (g == 0)]
        if len(a) and len(b):
            w = len(a) * len(b) / (len(a) + len(b))
            num += w * (a.mean() - b.mean()); den += w
    return num / den if den else float("nan")

def perm_p(y, g, s, perm_strata, rng, nperm=NPERM):
    obs = strat_diff(y, g, s)
    ps = np.unique(perm_strata)
    idx = [np.where(perm_strata == q)[0] for q in ps]
    sims = np.empty(nperm)
    for k in range(nperm):
        gp = g.copy()
        for ix in idx:
            if len(ix) > 1:
                gp[ix] = g[ix][rng.permutation(len(ix))]
        sims[k] = strat_diff(y, gp, s)
    return obs, float(((sims <= obs + 1e-12).sum() + 1) / (nperm + 1)), float(((np.abs(sims) >= abs(obs) - 1e-12).sum() + 1) / (nperm + 1))

def boot_ci(cs, rng, nboot=NBOOT):
    fams = sorted(set(c["family"] for c in cs))
    by = collections.defaultdict(list)
    for c in cs:
        by[c["family"]].append(c)
    vals = []
    for _ in range(nboot):
        pick = rng.integers(0, len(fams), len(fams))
        sample = [c for i in pick for c in by[fams[i]]]
        y = np.array([c["y"] for c in sample]); g = np.array([c["g"] for c in sample])
        s = np.array([c["format"] for c in sample])
        d = strat_diff(y, g, s)
        if not np.isnan(d):
            vals.append(d)
    return np.percentile(vals, [2.5, 97.5])

def run_diff(objs, label, seed, which="pooled", perm_by=lambda c: c["format"]):
    if which == "034_vs_033":
        objs = [o for o in objs if o["sub"] in ("033", "034")]
    elif which == "034_vs_032":
        objs = [o for o in objs if o["sub"] in ("032", "034")]
    cs = cells(objs)
    y = np.array([c["y"] for c in cs]); g = np.array([c["g"] for c in cs]); s = np.array([c["format"] for c in cs])
    ps = np.array([perm_by(c) for c in cs])
    rng = np.random.default_rng(seed)
    obs, p1, p2 = perm_p(y, g, s, ps, rng)
    lo, hi = boot_ci(cs, np.random.default_rng(seed + 1))
    return {"label": label, "objects": len(objs), "families": len(set(c["family"] for c in cs)), "cells": len(cs),
            "cells_034": int(g.sum()), "cells_other": int((1 - g).sum()),
            "log_area_diff": round(float(obs), 4), "area_ratio": round(math.exp(obs), 3),
            "area_ratio_ci95_family_bootstrap": [round(math.exp(lo), 3), round(math.exp(hi), 3)],
            "perm_p_one_sided_034_smaller": round(p1, 4), "perm_p_two_sided": round(p2, 4),
            "permutation_strata": len(set(ps.tolist()))}

def ols_cluster(cs, covs):
    """cell-level OLS of y on is034 + dummies of `covs` (list of cell keys), cluster-robust (CR1) by family."""
    y = np.array([c["y"] for c in cs]); g = np.array([c["g"] for c in cs], float)
    cols = [np.ones(len(cs)), g]; names = ["const", "is034"]
    for k in covs:
        levels = sorted(set(c[k] for c in cs))
        for lv in levels[1:]:
            cols.append(np.array([1.0 if c[k] == lv else 0.0 for c in cs])); names.append(f"{k}={lv}")
    X = np.column_stack(cols)
    # drop all-zero / duplicate columns
    keep = [0, 1]
    for j in range(2, X.shape[1]):
        if X[:, j].sum() > 0 and np.linalg.matrix_rank(X[:, keep + [j]]) == len(keep) + 1:
            keep.append(j)
    X = X[:, keep]
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    fam = np.array([c["family"] for c in cs]); ufam = np.unique(fam)
    XtXi = np.linalg.pinv(X.T @ X)
    meat = np.zeros((X.shape[1], X.shape[1]))
    for f in ufam:
        m = fam == f
        sc = X[m].T @ res[m]
        meat += np.outer(sc, sc)
    G, n, k = len(ufam), len(y), X.shape[1]
    V = XtXi @ meat @ XtXi * (G / (G - 1)) * ((n - 1) / (n - k))
    se = math.sqrt(V[1, 1])
    return {"coef_is034": round(float(beta[1]), 4), "se_cluster_family": round(se, 4), "area_ratio": round(math.exp(beta[1]), 3),
            "ci95_ratio": [round(math.exp(beta[1] - 1.96 * se), 3), round(math.exp(beta[1] + 1.96 * se), 3)],
            "z": round(float(beta[1] / se), 2), "n_cells": n, "n_params": k, "n_families": G}

def within_family(objs, seed):
    """Families that contain both a 034 and a 032/033 object in the same format: sign test and label-flip permutation."""
    cs = cells(objs)
    by = collections.defaultdict(dict)
    for c in cs:
        by[(c["family"], c["format"])][c["g"]] = c["y"]
    diffs = [v[1] - v[0] for v in by.values() if 0 in v and 1 in v]
    d = np.array(diffs)
    rng = np.random.default_rng(seed)
    obs = d.mean()
    sims = np.array([(d * rng.choice([-1, 1], len(d))).mean() for _ in range(NPERM)])
    return {"family_format_pairs": len(d), "mean_log_diff": round(float(obs), 4), "area_ratio": round(math.exp(obs), 3),
            "n_034_smaller": int((d < 0).sum()), "n_034_larger": int((d > 0).sum()),
            "sign_flip_perm_p_034_smaller": round(float(((sims <= obs + 1e-12).sum() + 1) / (NPERM + 1)), 4)}

def main():
    objs, lipi = load()
    out = {"nperm": NPERM, "nboot": NBOOT, "seed": SEED}
    u = usable_counts(lipi)
    u["of_which_in_frozen_309"] = len(objs)
    u["frozen_309_by_subtype"] = dict(collections.Counter(o["sub"] for o in objs))
    u["frozen_309_by_era"] = dict(collections.Counter(o["era"] for o in objs))
    u["frozen_309_populated"] = {
        "area_section_not_dash": sum(o["area"] not in ("--", "-", "") for o in objs),
        "period_not_dash": sum(o["period"] not in ("-", "") for o in objs),
        "phase_not_dash": sum(o["phase"] not in ("-", "") for o in objs),
        "material_steatite_or_faience": sum(o["material"] != "other" for o in objs)}
    u["families_in_309"] = len(set(o["family"] for o in objs))
    out["data"] = u
    # naive object-level (many votes per family) for contrast
    ob = [dict(o, family=o["cisi"]) for o in objs]
    out["object_level_one_vote_per_object"] = run_diff(ob, "one vote per object (NOT family-collapsed)", SEED + 1)
    # headline: family-collapsed, stratified by format
    out["family_level_pooled_by_format"] = run_diff(objs, "034 vs 032/033, family-collapsed, strata=format", SEED + 2)
    out["family_level_034_vs_033"] = run_diff(objs, "034 vs 033 only", SEED + 3, "034_vs_033")
    out["family_level_034_vs_032"] = run_diff(objs, "034 vs 032 only", SEED + 4, "034_vs_032")
    # permutation strata with controls
    out["perm_within_format_x_era"] = run_diff(objs, "perm within format x era", SEED + 5, perm_by=lambda c: c["format"] + "|" + c["era"])
    out["perm_within_format_x_era_x_material"] = run_diff(objs, "perm within format x era x material", SEED + 6, perm_by=lambda c: c["format"] + "|" + c["era"] + "|" + c["material"])
    out["perm_within_format_x_area"] = run_diff(objs, "perm within format x area-section", SEED + 7, perm_by=lambda c: c["format"] + "|" + c["area"])
    out["perm_within_format_x_era_x_area"] = run_diff(objs, "perm within format x era x area-section", SEED + 8, perm_by=lambda c: c["format"] + "|" + c["era"] + "|" + c["area"])
    # restricted subsets
    out["harp_era_only"] = run_diff([o for o in objs if o["era"] == "harp"], "HARP era only", SEED + 9)
    out["old_era_only"] = run_diff([o for o in objs if o["era"] == "old"], "old (H<1500) era only", SEED + 10)
    pop = [o for o in objs if o["phase"] not in ("-", "")]
    out["phase_populated_only_perm_within_format_x_phase"] = run_diff(pop, "phase populated only, perm within format x phase", SEED + 11, perm_by=lambda c: c["format"] + "|" + c["phase"])
    out["complete_or_chipped_only"] = run_diff([o for o in objs if o["preservation"] in ("complete", "slightly chipped", "chipped")], "preservation complete/chipped only", SEED + 12)
    out["without_H2218_2239_series"] = run_diff([o for o in objs if o["family"] != "series:H-2218-H-2239"], "excluding the H-2218..H-2239 series family", SEED + 13)
    big = collections.Counter(o["family"] for o in objs).most_common(2)
    out["without_two_largest_families"] = run_diff([o for o in objs if o["family"] not in [b[0] for b in big]], "excluding two largest families " + str([b[0] for b in big]), SEED + 14)
    out["without_cup_last"] = run_diff([o for o in objs if o["order"] == "700_first"], "700-first order only", SEED + 15)
    out["within_family_pairs"] = within_family(objs, SEED + 16)
    # regression at the cell level with controls
    cs = cells(objs)
    out["ols_cell_level"] = {
        "format": ols_cluster(cs, ["format"]),
        "format+era": ols_cluster(cs, ["format", "era"]),
        "format+era+material": ols_cluster(cs, ["format", "era", "material"]),
        "format+era+material+area_section": ols_cluster(cs, ["format", "era", "material", "area"]),
        "format+era+material+area_section+phase": ols_cluster(cs, ["format", "era", "material", "area", "phase"]),
    }
    # each dimension separately (is the difference in length, width, or both?)
    for dim in ("logH", "logV"):
        c2 = []
        d = collections.defaultdict(list)
        for o in objs:
            d[(o["family"], o["format"], o["is034"])].append(o[dim])
        y = np.array([np.mean(v) for v in d.values()]); g = np.array([k[2] for k in d]); s = np.array([k[1] for k in d])
        out["dim_" + dim] = {"ratio": round(math.exp(strat_diff(y, g, s)), 3)}
    path = os.path.join(HERE, "size_034_results.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True); fh.write("\n")
    print(json.dumps(out, indent=1, sort_keys=True))

if __name__ == "__main__":
    main()
