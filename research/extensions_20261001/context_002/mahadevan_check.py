"""Infer Lipi -> Mahadevan sign numbers by aligning texts, then repeat the 002 end-effect check in Mahadevan data.

Deterministic, no randomness. Run from the repo root: python3 research/extensions_20261001/context_002/mahadevan_check.py
Needs scipy (Fisher exact). Output: mahadevan_check_results.json next to this script.

Orientation: Lipi stored order = reverse of Mahadevan concordance slot order (S1..Sn). Checked on
H-306 = Mahadevan 5474: Lipi front +740-032-840+ vs Mahadevan slots 403,87,342; cup face +700-033+ vs 89,328.
Seeds: 700=328 (cup), 740=342 (jar, accepted exact crosswalk edge), 032/033/034 = 87/89/95 (2/3/4 strokes).
Propagation: a Lipi text of length n with >=1 seed sign and exactly one Mahadevan text of the same length consistent
with all mapped signs votes for the unmapped signs; a sign is mapped when >=3 votes and >=80% agree.
"""
import csv, collections, json, os, re
from scipy.stats import fisher_exact

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
D = os.path.join(ROOT, "research", "data")

M = []  # Mahadevan slot-order token tuples (no doubtful/illegible tokens, counts consistent)
for r in csv.DictReader(open(os.path.join(D, "mahadevan_20260905", "concordance_rows.csv"))):
    toks = [r["S%d" % i] for i in range(1, 15) if r["S%d" % i] != ""]
    if not toks or any(t.startswith("*") or t == "0" for t in toks):
        continue
    if int(r["posnum"] or 0) != len(toks) or int(r["signnum"] or 0) != len(toks):
        continue
    M.append(tuple(toks))
L = collections.defaultdict(int)  # Lipi complete texts, no 000
for r in csv.DictReader(open(os.path.join(D, "open_prototype", "lipi", "metadata_filtered.csv"))):
    t = r["text"]
    if not (t.startswith("+") and t.endswith("+")):
        continue
    toks = t.strip("+").split("-")
    if "000" in toks or any(not re.fullmatch(r"\d{3}", x) for x in toks):
        continue
    L[tuple(toks)] += 1

Mrev = collections.Counter(m[::-1] for m in M)
byLen = collections.defaultdict(list)
for m in Mrev:
    byLen[len(m)].append(m)
f = {"700": "328", "740": "342", "032": "87", "033": "89", "034": "95"}
for rnd in range(12):
    votes = collections.defaultdict(collections.Counter)
    for l, cnt in L.items():
        if len(l) < 2:
            continue
        known = [(i, f[s]) for i, s in enumerate(l) if s in f]
        unk = [i for i, s in enumerate(l) if s not in f]
        if not unk or not known:
            continue
        cands = [m for m in byLen[len(l)] if all(m[i] == v for i, v in known)]
        if len(cands) == 1:
            for i in unk:
                votes[l[i]][cands[0][i]] += cnt
    new = {}
    for l, v in votes.items():
        tot = sum(v.values()); m, n = v.most_common(1)[0]
        if n >= 3 and n / tot >= 0.8:
            new[l] = m
    if not new:
        break
    f.update(new)

# leave-target-out support: align on the other positions only, read the Mahadevan sign at the target position
support = {}
for target in ["002", "861", "817", "820"]:
    res = collections.Counter(); nstr = nrows = amb = 0
    for l, cnt in L.items():
        if target not in l or len(l) < 2:
            continue
        known = [(i, f[s]) for i, s in enumerate(l) if s in f and s != target]
        unk = [s for s in l if s not in f and s != target]
        if unk or not known:
            continue
        cands = [m for m in byLen[len(l)] if all(m[i] == v for i, v in known)]
        if len(cands) == 1:
            nstr += 1; nrows += cnt
            for i, s in enumerate(l):
                if s == target:
                    res[cands[0][i]] += cnt
        elif len(cands) > 1:
            amb += 1
    support[target] = {"mapped_to": f.get(target), "unique_alignment_strings": nstr, "rows": nrows,
                       "ambiguous_strings_skipped": amb, "mahadevan_sign_counts": dict(res.most_common(4))}

# Mahadevan replication of the end effect, in slot order: Y immediately before 99, Y is text-initial (slot 1).
# Conditioning mirrors context_002 (an occurrence needs a neighbour on the 002 side, here a successor).
def table(T):
    cnt = collections.Counter()
    for t in T:
        for i, s in enumerate(t[:-1]):
            cnt[(s, t[i + 1] == "99", i == 0)] += 1
    out = {}
    for Y in ["267", "391", "293", "59"]:
        a, b, c, d = cnt[(Y, True, True)], cnt[(Y, True, False)], cnt[(Y, False, True)], cnt[(Y, False, False)]
        out[Y] = {"before_99_initial": a, "before_99_n": a + b, "other_initial": c, "other_n": c + d,
                  "haldane_OR": round(((a + .5) * (d + .5)) / ((b + .5) * (c + .5)), 2),
                  "fisher_p": float("%.3g" % fisher_exact([[a, b], [c, d]])[1])}
    return out
rep = {"all_lines": table(M), "distinct_strings": table(list(set(M)))}
pairs = collections.Counter()
for t in M:
    for i in range(len(t) - 1):
        pairs[(t[i], t[i + 1])] += 1
res = {"mapped_signs": len(f), "mapping": {k: f[k] for k in ["700", "740", "032", "033", "034", "840", "002", "861", "817", "820"] if k in f},
       "support": support, "mahadevan_replication": rep,
       "slot_order_pair_counts": {"267,99": pairs[("267", "99")], "391,99": pairs[("391", "99")], "99,267": pairs[("99", "267")]}}
json.dump(res, open(os.path.join(os.path.dirname(__file__), "mahadevan_check_results.json"), "w"), indent=1)
print(json.dumps(res, indent=1))
