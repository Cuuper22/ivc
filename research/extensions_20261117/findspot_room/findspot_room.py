#!/usr/bin/env python3
"""findspot_room: do seals dug up in the same room share writing more than chance?

Run:  python3 research/extensions_20261117/findspot_room/findspot_room.py
      (numpy only, fixed seeds, several minutes, writes findspot_room_results.json next to this file)

Why this exists. Every earlier test in this repository used the catalogue's findspot columns only as
strata to control for. This script flips that: the findspot is the thing being explained. If seal texts
name people or households, seals found together should share uncommon signs; if texts are generic
formulas, they should not.

Data. Lipi metadata_filtered.csv, seals only (type starts with SEAL), faces of one object merged.
Columns used: site, area-section (excavation area), block-house (house), room-grid (room), depth, symbol
(the animal), text. Sign order is the stored Lipi order, which is the reverse of the conventional reading
order (see research/docs/reading_direction_note.md); "ends" = first and last stored sign, "middle" = the rest.

Four parts, each printed as it goes:
  A  first pass: same house, then same room, no depth condition; labels shuffled within excavation area
  B  depth-matched: only compare seals within 3 ft of depth; labels shuffled within area x 3-ft depth band
  C  grid: same-room sharing of an uncommon sign, over rarity cut-offs and depth windows, middle vs ends
  D  other sites that have a room/grid field

A "rare" or "uncommon" sign = a sign that occurs on at most N catalogue rows (N is the rarity cut-off).
P = share of label shuffles that give at least the observed value (one-sided), with the +1 correction.
"""
import csv, collections, math, os, random, re, sys, time
from json import JSONEncoder
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CSV_PATH = os.path.join(ROOT, "data/open_prototype/lipi/metadata_filtered.csv")
OUT_PATH = os.path.join(HERE, "findspot_room_results.json")
EMPTY = ("--", "-", "")
NEEDED = ["id", "site", "area-section", "block-house", "room-grid", "depth", "symbol", "type", "text", "cisi", "excavation-idno"]


def stop(msg):
    """Plain-English failure, raised the moment an input condition breaks."""
    print("STOPPING:", msg, flush=True)
    sys.exit(1)


def read_catalogue():
    if not os.path.exists(CSV_PATH):
        stop("catalogue file not found at " + CSV_PATH)
    rows = list(csv.DictReader(open(CSV_PATH, encoding="utf-8")))
    missing = [c for c in NEEDED if c not in rows[0]]
    if missing:
        stop("catalogue is missing columns: " + ", ".join(missing))
    if len(rows) != 5679:
        stop(f"expected 5679 catalogue rows, found {len(rows)}; the frozen file has changed")
    return rows


def signs_of(text):
    return re.findall(r"\d{3}", text)


def depth_ft(s):
    m = re.search(r"(-?\d+(\.\d+)?)\s*ft", s)
    return float(m.group(1)) if m else None


def merge_seal_objects(rows, site):
    """One record per seal object at a site (a seal with two inscribed faces is one object)."""
    objs = {}
    for x in rows:
        if x["site"] != site or not x["type"].startswith("SEAL"):
            continue
        k = x["id"].split(".")[0]
        o = objs.setdefault(k, dict(area=x["area-section"], house=x["block-house"], room=x["room-grid"],
                                    toks=[], sym=x["symbol"], depth=x["depth"], cisi=x["cisi"],
                                    exc=x["excavation-idno"]))
        o["toks"] += signs_of(x["text"])
    return objs


def pvalue(null, obs):
    null = np.asarray(null)
    return float((1 + np.sum(null >= obs)) / (len(null) + 1))


def progress(label, done, total, t0):
    print(f"    {label}: {done}/{total} shuffles ({100 * done // total}%), {time.time() - t0:.0f}s", flush=True)


# ---------------------------------------------------------------------------------------------------
# Part A: first pass, no depth condition
# ---------------------------------------------------------------------------------------------------
def part_a(rows, freq, idf, level, nshuffle=2000):
    random.seed(7); np.random.seed(7)
    rare = {t for t, f in freq.items() if f <= 40}
    U = []
    for o in merge_seal_objects(rows, "Mohenjo-daro").values():
        if o["house"] in EMPTY:
            continue
        if level == "room" and o["room"] in EMPTY:
            continue
        st = o["toks"]; s = [t for t in st if t != "000"]
        if len(s) < 2:
            continue
        o["signs"] = set(s)
        o["bigr"] = {(a, b) for a, b in zip(st, st[1:]) if a != "000" and b != "000"}
        o["first"] = st[0] if st[0] != "000" else None      # stored-first = reading-final
        o["last"] = st[-1] if st[-1] != "000" else None     # stored-last  = reading-initial
        o["last2"] = tuple(st[-2:]) if "000" not in st[-2:] else None
        o["middle"] = set(t for t in st[1:-1] if t != "000")
        o["text"] = "-".join(st)
        o["unit"] = (o["area"], o["house"]) if level == "house" else (o["area"], o["house"], o["room"])
        U.append(o)

    def wj(a, b):  # overlap of two sign sets, uncommon signs weighted up (idf-weighted Jaccard)
        i = sum(idf[t] for t in a & b); u = sum(idf[t] for t in a | b)
        return i / u if u else 0.0

    def stats(labels):
        g = collections.defaultdict(list)
        for o, l in zip(U, labels):
            g[l].append(o)
        S = collections.Counter(); n = 0
        for mem in g.values():
            for i in range(len(mem)):
                for j in range(i + 1, len(mem)):
                    a, b = mem[i], mem[j]; n += 1
                    S["all_signs_overlap"] += wj(a["signs"], b["signs"])
                    S["shares_rare_sign"] += 1 if (a["signs"] & b["signs"] & rare) else 0
                    S["shares_sign_pair"] += 1 if (a["bigr"] & b["bigr"]) else 0
                    S["same_stored_last_sign"] += 1 if (a["last"] and a["last"] == b["last"]) else 0
                    S["same_stored_last_two"] += 1 if (a["last2"] and a["last2"] == b["last2"]) else 0
                    S["same_stored_first_sign"] += 1 if (a["first"] and a["first"] == b["first"]) else 0
                    S["middle_signs_overlap"] += wj(a["middle"], b["middle"])
                    S["identical_text"] += 1 if a["text"] == b["text"] else 0
                    S["same_animal"] += 1 if a["sym"] == b["sym"] else 0
        return {k: v / n for k, v in S.items()}, n

    lab = [o["unit"] for o in U]
    obs, npairs = stats(lab)
    units = collections.Counter(lab)
    print(f"  {level}: {len(U)} seals with a findspot, {sum(1 for v in units.values() if v >= 2)} "
          f"{level}s holding 2+ seals, {npairs} same-{level} pairs", flush=True)
    byarea = collections.defaultdict(list)
    for i, o in enumerate(U):
        byarea[o["area"]].append(i)
    null = collections.defaultdict(list); t0 = time.time()
    for t in range(nshuffle):
        p = lab[:]
        for idx in byarea.values():
            vals = [lab[i] for i in idx]; random.shuffle(vals)
            for i, v in zip(idx, vals):
                p[i] = v
        s, _ = stats(p)
        for k in obs:
            null[k].append(s.get(k, 0))
        if (t + 1) % 500 == 0:
            progress(f"part A {level}", t + 1, nshuffle, t0)
    out = {"seals": len(U), "pairs": npairs, "shuffles": nshuffle, "measures": {}}
    print(f"    {'measure':26s}{'observed':>10s}{'chance':>10s}{'ratio':>7s}{'P':>8s}")
    for k in ["all_signs_overlap", "shares_rare_sign", "shares_sign_pair", "same_stored_last_sign",
              "same_stored_last_two", "same_stored_first_sign", "middle_signs_overlap", "identical_text", "same_animal"]:
        a = np.array(null[k]); ch = float(a.mean())
        out["measures"][k] = {"observed": obs[k], "chance": ch, "ratio": (obs[k] / ch if ch else None), "p": pvalue(a, obs[k])}
        print(f"    {k:26s}{obs[k]:10.4f}{ch:10.4f}{(obs[k] / ch if ch else float('nan')):7.2f}{pvalue(a, obs[k]):8.4f}")
    return out


# ---------------------------------------------------------------------------------------------------
# Part B: depth-matched comparison
# ---------------------------------------------------------------------------------------------------
def part_b(rows, freq, idf, band=3.0, dmax=3.0, nshuffle=2000):
    random.seed(11)
    rare = {t for t, f in freq.items() if f <= 40}
    U = []
    for o in merge_seal_objects(rows, "Mohenjo-daro").values():
        if o["house"] in EMPTY:
            continue
        st = o["toks"]; s = [t for t in st if t != "000"]
        if len(s) < 2:
            continue
        d = depth_ft(o["depth"])
        if d is None:
            continue
        o["d"] = d; o["signs"] = set(s); o["medial"] = set(st[1:-1]) - {"000"}
        o["ends"] = {st[0], st[-1]} - {"000"}
        o["bigr"] = {(a, b) for a, b in zip(st, st[1:]) if a != "000" and b != "000"}
        o["hk"] = (o["area"], o["house"])
        o["rk"] = (o["area"], o["house"], o["room"]) if o["room"] not in EMPTY else None
        U.append(o)

    def wj(a, b):
        i = sum(idf[t] for t in a & b); u = sum(idf[t] for t in a | b)
        return i / u if u else 0.0

    def stats(hk, rk):
        S = collections.defaultdict(float); n = collections.Counter()
        idx = collections.defaultdict(list)
        for i, h in enumerate(hk):
            idx[h].append(i)
        for mem in idx.values():
            for a_ in range(len(mem)):
                for b_ in range(a_ + 1, len(mem)):
                    i, j = mem[a_], mem[b_]; a, b = U[i], U[j]
                    if abs(a["d"] - b["d"]) > dmax:
                        continue
                    kind = "same_room" if (rk[i] is not None and rk[i] == rk[j]) else "same_house_other_room"
                    for kd in (kind, "same_house_any_room"):
                        n[kd] += 1
                        S[kd, "all_signs_overlap"] += wj(a["signs"], b["signs"])
                        S[kd, "middle_signs_overlap"] += wj(a["medial"], b["medial"])
                        S[kd, "end_signs_overlap"] += wj(a["ends"], b["ends"])
                        S[kd, "shares_rare_sign"] += 1 if a["signs"] & b["signs"] & rare else 0
                        S[kd, "shares_sign_pair"] += 1 if a["bigr"] & b["bigr"] else 0
                        S[kd, "same_animal"] += 1 if a["sym"] == b["sym"] else 0
        return {k: v / n[k[0]] for k, v in S.items()}, n

    hk = [o["hk"] for o in U]; rk = [o["rk"] for o in U]
    obs, n = stats(hk, rk)
    print(f"  {len(U)} seals with house + depth; pairs within {dmax:g} ft of depth: {dict(n)}", flush=True)
    strata = collections.defaultdict(list)
    for i, o in enumerate(U):
        strata[(o["area"], int(o["d"] // band))].append(i)
    null = collections.defaultdict(list); t0 = time.time()
    for t in range(nshuffle):
        ph = hk[:]; pr = rk[:]
        for idx in strata.values():
            sh = idx[:]; random.shuffle(sh)
            for i, j in zip(idx, sh):
                ph[i] = hk[j]; pr[i] = rk[j]
        s, _ = stats(ph, pr)
        for k in obs:
            null[k].append(s.get(k, 0.0))
        if (t + 1) % 500 == 0:
            progress("part B", t + 1, nshuffle, t0)
    out = {"seals": len(U), "pairs": dict(n), "depth_band_ft": band, "max_depth_gap_ft": dmax, "shuffles": nshuffle, "rows": []}
    print(f"    {'where':24s}{'what is shared':22s}{'observed':>9s}{'chance':>9s}{'ratio':>7s}{'P':>8s}")
    for kind in ("same_room", "same_house_other_room", "same_house_any_room"):
        for m in ("all_signs_overlap", "middle_signs_overlap", "end_signs_overlap", "shares_rare_sign", "shares_sign_pair", "same_animal"):
            a = np.array(null[(kind, m)]); o = obs[(kind, m)]; ch = float(a.mean())
            out["rows"].append({"where": kind, "measure": m, "observed": o, "chance": ch, "ratio": (o / ch if ch else None), "p": pvalue(a, o)})
            print(f"    {kind:24s}{m:22s}{o:9.4f}{ch:9.4f}{(o / ch if ch else float('nan')):7.2f}{pvalue(a, o):8.4f}")
    return out


# ---------------------------------------------------------------------------------------------------
# Part C: grid over rarity cut-off and depth window, middle signs vs end signs
# ---------------------------------------------------------------------------------------------------
def part_c(rows, freq, nshuffle=3000, band=3.0):
    random.seed(3)
    U = []
    for o in merge_seal_objects(rows, "Mohenjo-daro").values():
        if o["house"] in EMPTY or o["room"] in EMPTY:
            continue
        st = o["toks"]; s = [t for t in st if t != "000"]
        if len(s) < 2:
            continue
        d = depth_ft(o["depth"])
        if d is None:
            continue
        o["d"] = d; o["mid"] = set(st[1:-1]) - {"000"}; o["end"] = {st[0], st[-1]} - {"000"}
        o["rk"] = (o["area"], o["house"], o["room"])
        U.append(o)
    if len(U) != 845:
        stop(f"expected 845 Mohenjo-daro seals with room + depth, found {len(U)}")
    print(f"  {len(U)} Mohenjo-daro seals with room + depth", flush=True)

    def count(rk, cut, dmax, part, keep=None):
        idx = collections.defaultdict(list)
        for i, h in enumerate(rk):
            idx[h].append(i)
        c = 0; n = 0
        for mem in idx.values():
            for a_ in range(len(mem)):
                for b_ in range(a_ + 1, len(mem)):
                    a, b = U[mem[a_]], U[mem[b_]]
                    if abs(a["d"] - b["d"]) > dmax:
                        continue
                    n += 1
                    sh = [t for t in a[part] & b[part] if freq[t] <= cut]
                    if sh:
                        c += 1
                        if keep is not None:
                            keep.append({"room": " / ".join(a["rk"]), "seal_1": a["cisi"], "find_no_1": a["exc"], "depth_1": a["depth"],
                                         "text_1": "-".join(a["toks"]), "seal_2": b["cisi"], "find_no_2": b["exc"], "depth_2": b["depth"],
                                         "text_2": "-".join(b["toks"]), "shared": {t: freq[t] for t in sorted(sh)}})
        return c, n

    rk = [o["rk"] for o in U]
    strata = collections.defaultdict(list)
    for i, o in enumerate(U):
        strata[(o["area"], int(o["d"] // band))].append(i)
    out = {"seals": len(U), "shuffles": nshuffle, "depth_band_ft": band, "cells": []}
    cells = [(part, cut, dmax) for part in ("mid", "end") for cut in (20, 40, 80, 150) for dmax in (2, 3, 5, 99)]
    print(f"    {'part':8s}{'rarity<=':>9s}{'depth gap<=ft':>14s}{'pairs':>7s}{'observed':>9s}{'expected':>9s}{'ratio':>7s}{'P':>8s}")
    t0 = time.time()
    for ci, (part, cut, dmax) in enumerate(cells):
        obs, n = count(rk, cut, dmax, part)
        nl = []
        for t in range(nshuffle):
            p = rk[:]
            for idx in strata.values():
                sh = idx[:]; random.shuffle(sh)
                for i, j in zip(idx, sh):
                    p[i] = rk[j]
            nl.append(count(p, cut, dmax, part)[0])
        nl = np.array(nl); ex = float(nl.mean())
        out["cells"].append({"part": "middle" if part == "mid" else "ends", "rarity_cutoff": cut, "max_depth_gap_ft": dmax,
                             "pairs": n, "observed": obs, "expected": ex, "ratio": (obs / ex if ex else None), "p": pvalue(nl, obs)})
        print(f"    {('middle' if part == 'mid' else 'ends'):8s}{cut:9d}{dmax:14d}{n:7d}{obs:9d}{ex:9.2f}"
              f"{(obs / ex if ex else float('nan')):7.2f}{pvalue(nl, obs):8.4f}   [{ci + 1}/{len(cells)} cells, {time.time() - t0:.0f}s]", flush=True)
    pairs = []
    count(rk, 80, 3, "mid", keep=pairs)
    out["pairs_behind_headline_cell"] = pairs
    print("  the pairs behind the headline cell (middle signs, rarity <= 80, depth gap <= 3 ft):")
    for p in pairs:
        print(f"    {p['seal_1']} ({p['find_no_1']}, {p['depth_1']})  +  {p['seal_2']} ({p['find_no_2']}, {p['depth_2']})  share {p['shared']}")
    return out


# ---------------------------------------------------------------------------------------------------
# Part D: other sites with a room/grid field
# ---------------------------------------------------------------------------------------------------
def part_d(rows, freq, sites=("Harappa", "Kalibangan", "Chanhu-daro"), nshuffle=3000):
    random.seed(5)
    out = {}
    for site in sites:
        U = []
        for o in merge_seal_objects(rows, site).values():
            if o["room"] in EMPTY:
                continue
            st = o["toks"]
            if len([t for t in st if t != "000"]) < 2:
                continue
            o["mid"] = set(st[1:-1]) - {"000"}; o["all"] = set(st) - {"000"}
            o["u"] = (o["area"], o["house"], o["room"])
            U.append(o)
        lab = [o["u"] for o in U]

        def count(lab, cut, part):
            idx = collections.defaultdict(list)
            for i, h in enumerate(lab):
                idx[h].append(i)
            c = n = 0
            for mem in idx.values():
                for a in range(len(mem)):
                    for b in range(a + 1, len(mem)):
                        n += 1
                        if any(freq[t] <= cut for t in U[mem[a]][part] & U[mem[b]][part]):
                            c += 1
            return c, n

        byarea = collections.defaultdict(list)
        for i, o in enumerate(U):
            byarea[o["area"]].append(i)
        print(f"  {site}: {len(U)} seals with a room/grid findspot", flush=True)
        out[site] = {"seals": len(U), "shuffles": nshuffle, "cells": []}
        for part in ("mid", "all"):
            for cut in (40, 80, 150):
                obs, n = count(lab, cut, part); nl = []
                for t in range(nshuffle):
                    p = lab[:]
                    for idx in byarea.values():
                        sh = idx[:]; random.shuffle(sh)
                        for i, j in zip(idx, sh):
                            p[i] = lab[j]
                    nl.append(count(p, cut, part)[0])
                nl = np.array(nl); ex = float(nl.mean())
                out[site]["cells"].append({"part": "middle" if part == "mid" else "whole text", "rarity_cutoff": cut, "pairs": n,
                                           "observed": obs, "expected": ex, "p": pvalue(nl, obs)})
                print(f"    {('middle' if part == 'mid' else 'whole text'):11s} rarity<={cut:3d}: pairs {n}, observed {obs}, "
                      f"expected {ex:.2f}, P {pvalue(nl, obs):.4f}", flush=True)
    return out


def main():
    t0 = time.time()
    print("[1/5] reading the catalogue ...", flush=True)
    rows = read_catalogue()
    # how many catalogue rows each sign occurs on (a sign repeated inside one row counts once)
    freq = collections.Counter()
    for x in rows:
        for t in set(signs_of(x["text"])):
            if t != "000":
                freq[t] += 1
    idf = {t: math.log(len(rows) / f) for t, f in freq.items()}
    print(f"      {len(rows)} rows, {len(freq)} distinct signs", flush=True)
    res = {"seeds": {"A": 7, "B": 11, "C": 3, "D": 5}, "catalogue_rows": len(rows)}

    print("[2/5] part A: first pass, same house and same room, no depth condition", flush=True)
    res["A_first_pass"] = {lv: part_a(rows, freq, idf, lv) for lv in ("house", "room")}
    print("[3/5] part B: depth-matched (pairs within 3 ft; chance = labels shuffled within area x 3-ft band)", flush=True)
    res["B_depth_matched"] = part_b(rows, freq, idf)
    print("[4/5] part C: grid over rarity cut-off and depth window (the slow part)", flush=True)
    res["C_grid"] = part_c(rows, freq)
    print("[5/5] part D: other sites", flush=True)
    res["D_other_sites"] = part_d(rows, freq)

    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        fh.write(JSONEncoder(indent=1).encode(res) + "\n")
    head = next(c for c in res["C_grid"]["cells"] if c["part"] == "middle" and c["rarity_cutoff"] == 80 and c["max_depth_gap_ft"] == 3)
    print(f"done in {time.time() - t0:.0f}s. Headline: {head['observed']} same-room pairs share an uncommon middle sign, "
          f"{head['expected']:.2f} expected by chance, P {head['p']:.4f}. Results written to {OUT_PATH}", flush=True)


if __name__ == "__main__":
    main()
