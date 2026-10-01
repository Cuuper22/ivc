#!/usr/bin/env python3
"""Study 4: are the proposed sign alternations more frequent than chance?

Support definition (reused from research/tools/semantic_transducer_search.py):
a rewrite A -> (B, C) is supported by an "exact-context pair" when a unique strict
line s contains A at position i and the line s[:i] + (B, C) + s[i+1:] is also an
observed unique strict line. "Shared context" = the unchanged signs, len(s) - 1.

Data: strict Mahadevan rows (concordance_rows.csv, strict == 1, S1..S14).
Everything is deterministic (fixed seeds, exhaustive enumeration where possible).
Run from anywhere:  python3 alternation_null.py
Outputs (next to this script): alternation_null_results.json, swap_table_summary.json
"""
import csv, json, math, random, sys
from collections import defaultdict, Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'research/tools'))
from semantic_transducer_search import TICK_PAIRS, ROOF_PAIRS, PARTS  # reuse repo's hypothesis lists

SEED = 20261001
K_MAIN = 25          # nearest-K pool for the exhaustive null
K_WIDE = 50          # wider pool (sensitivity), sampled
N_WIDE = 20000
N_FAMILY = 2000      # decoy families per family-level search null
VOCAB = range(1, 418)

PROPOSED = {          # name: (A, B, C)
    'roof 65 -> 87-59': (65, 87, 59),
    'marked fish 66 -> 87-60': (66, 87, 60),
    'surrounding marks 60 -> 59-211': (60, 59, 211),
    'non-fish 15 -> 149-342': (15, 149, 342),
}

# ---------------------------------------------------------------- data
by_seq = defaultdict(set)   # unique strict sequence -> set of object ids (textnum)
with open(ROOT / 'research/data/mahadevan_20260905/concordance_rows.csv') as f:
    for r in csv.DictReader(f):
        if r['strict'] == '1':
            s = tuple(int(r[f'S{i}']) for i in range(1, 15) if r[f'S{i}'])
            by_seq[s].add(r['textnum'])
SEQS = set(by_seq)
N_STRICT_ROWS = None

count = Counter(); ini = Counter(); fin = Counter(); multi = Counter()
for s in SEQS:
    for i, x in enumerate(s):
        count[x] += 1
        if len(s) > 1:
            multi[x] += 1
            ini[x] += (i == 0)
            fin[x] += (i == len(s) - 1)
# signs absent from the strict corpus (count 0) get a pseudo-count of 0.5 so they can be matched
profile = {x: (math.log2(count[x] or 0.5), ini[x] / multi[x] if multi[x] else 0.0,
               fin[x] / multi[x] if multi[x] else 0.0) for x in VOCAB}


def dist(x, y):
    """Frequency (octaves) + 2 x positional-share difference (initial, final)."""
    return (abs(profile[x][0] - profile[y][0])
            + 2 * (abs(profile[x][1] - profile[y][1]) + abs(profile[x][2] - profile[y][2])))


HYP_SIGNS = ({x for p in TICK_PAIRS + ROOF_PAIRS for x in p} | {x for p in PARTS for x in p}
             | {x for r in PROPOSED.values() for x in r})


def pool(x, k, reserved=HYP_SIGNS):
    cand = [y for y in count if y != x and y not in reserved]
    cand.sort(key=lambda y: (dist(x, y), y))
    return cand[:k]


# ---------------------------------------------------------------- full swap table
# hole index: (prefix, suffix) -> {A: s} for every unique line s with sign A at that slot
HOLE = defaultdict(list)
for s in SEQS:
    for i, a in enumerate(s):
        HOLE[(s[:i], s[i + 1:])].append((a, s))
SWAP = defaultdict(list)     # (A,B,C) -> list of (s, t, unchanged_len)
for t in SEQS:
    for j in range(len(t) - 1):
        key = (t[:j], t[j + 2:])
        for a, s in HOLE.get(key, ()):
            SWAP[(a, t[j], t[j + 1])].append((s, t, len(t) - 2, j))
BEST_BY_A = defaultdict(int)


def metrics(hits):
    h1 = [h for h in hits if h[2] >= 1]
    h2 = [h for h in hits if h[2] >= 2]
    ctx = {(t[:j], t[j + 2:]) for s, t, u, j in h1}
    objs = set()
    for s, t, u, j in h1:
        objs |= by_seq[s] | by_seq[t]
    return dict(pairs_ge1=len(h1), pairs_ge2=len(h2), contexts_ge1=len(ctx), objects=len(objs))


MET = {k: metrics(v) for k, v in SWAP.items()}
for (a, b, c), m in MET.items():
    BEST_BY_A[a] = max(BEST_BY_A[a], m['pairs_ge1'])


def met(k):
    return MET.get(k, dict(pairs_ge1=0, pairs_ge2=0, contexts_ge1=0, objects=0))


# ---------------------------------------------------------------- corpus-wide swap census
def census():
    types2 = defaultdict(list)       # swap type -> instances with >=2 shared signs
    for k, hits in SWAP.items():
        h2 = [h for h in hits if h[2] >= 2]
        if h2:
            types2[k] = h2
    inst2 = sum(len(v) for v in types2.values())

    def ctxs(hits):
        return {(t[:j], t[j + 2:]) for s, t, u, j in hits}
    recur = {k: ctxs(v) for k, v in types2.items()}
    # non-nested contexts: collapse contexts where one is a sub-context of another is hard to
    # define; also report the stricter count requiring >=2 contexts that share no sign position
    rec2 = {k: c for k, c in recur.items() if len(c) >= 2}
    # recurrence in >= 2 distinct *objects groups* not nested: contexts with disjoint token sets
    def disjoint_count(c):
        cs = [set(p) | set(q) for p, q in c]
        best = 1
        for a in range(len(cs)):
            chosen = [cs[a]]
            for b in range(len(cs)):
                if b != a and all(not (cs[b] & x) for x in chosen):
                    chosen.append(cs[b])
            best = max(best, len(chosen))
        return best
    rec_disj = {k for k, c in rec2.items() if disjoint_count(c) >= 2}
    all_types = len(SWAP)
    return dict(
        swap_instances_any_shared=sum(len(v) for v in SWAP.values()),
        swap_types_any_shared=all_types,
        swap_instances_ge2_shared=inst2,
        swap_types_ge2_shared=len(types2),
        swap_types_any_shared_with_ge2_contexts=sum(1 for v in MET.values() if v['contexts_ge1'] >= 2),
        swap_types_any_shared_with_ge2_pairs=sum(1 for v in MET.values() if v['pairs_ge1'] >= 2),
        instances_ge2_shared_distinct_line_pairs=len({(s, t) for v in types2.values() for s, t, u, j in v}),
        types_ge2_shared_recurring_ge2_contexts=len(rec2),
        types_ge2_shared_recurring_ge2_nonoverlapping_contexts=len(rec_disj),
        top_recurring=[dict(A=k[0], B=k[1], C=k[2], contexts=len(c))
                       for k, c in sorted(rec2.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:15]],
        proposed_in_recurring={n: (v in rec2) for n, v in PROPOSED.items()},
        proposed_context_counts_ge2={n: len(recur.get(v, ())) for n, v in PROPOSED.items()},
    )


# ---------------------------------------------------------------- matched decoys
def decoy_stats(obs, vals_by_metric):
    out = {}
    for m, vals in vals_by_metric.items():
        o = obs[m]; n = len(vals)
        lt = sum(v < o for v in vals); eq = sum(v == o for v in vals); ge = n - lt
        out[m] = dict(observed=o, n_decoys=n, decoys_ge_observed=ge, frac_ge=ge / n,
                      percentile_midrank=100 * (lt + 0.5 * eq) / n,
                      expected_ge_in_2000_draws=2000 * ge / n,
                      decoy_mean=sum(vals) / n, decoy_max=max(vals))
    return out


def rule_null(name, rule):
    A, B, C = rule
    obs = met(rule)
    pa, pb, pc = pool(A, K_MAIN), pool(B, K_MAIN), pool(C, K_MAIN)
    vals = defaultdict(list); vals_bg = defaultdict(list)
    for a in pa:
        for b in pb:
            for c in pc:
                if len({a, b, c}) < 3:
                    continue
                m = met((a, b, c))
                bigram_ok = BIGRAM[(b, c)] >= 1
                for k, v in m.items():
                    vals[k].append(v)
                    if bigram_ok:
                        vals_bg[k].append(v)
    res = dict(rule=name, A=A, B=B, C=C, observed=obs,
               pools=dict(A=pa, B=pb, C=pc),
               null_main=decoy_stats(obs, vals),
               null_given_expansion_bigram_exists=decoy_stats(obs, vals_bg))
    # wider pool, random sample
    rng = random.Random(SEED + A)
    qa, qb, qc = pool(A, K_WIDE), pool(B, K_WIDE), pool(C, K_WIDE)
    wv = defaultdict(list)
    while len(wv['pairs_ge1']) < N_WIDE:
        a, b, c = rng.choice(qa), rng.choice(qb), rng.choice(qc)
        if len({a, b, c}) < 3:
            continue
        for k, v in met((a, b, c)).items():
            wv[k].append(v)
    res['null_wide_k50_sampled'] = decoy_stats(obs, wv)
    # selection-aware over (B, C): how many rewrites of the SAME A are at least this well supported
    ge = [k for k in MET if k[0] == A and MET[k]['pairs_ge1'] >= obs['pairs_ge1']]
    res['all_BC_for_same_A'] = dict(distinct_BC_rewrites_with_any_support=sum(1 for k in MET if k[0] == A),
        BC_rewrites_with_support_ge_observed=len(ge), of_possible_BC=417 * 417 - 417,
        best_support_for_A=BEST_BY_A[A])
    # selection-aware over (B, C) AND matched A': best rewrite of any form for matched A'
    bestvals = [BEST_BY_A[a] for a in pa]
    res['best_rewrite_of_matched_A'] = dict(
        observed=obs['pairs_ge1'], n_decoy_signs=len(pa),
        decoy_signs_whose_best_rewrite_ge_observed=sum(v >= obs['pairs_ge1'] for v in bestvals),
        decoy_best_values=sorted(bestvals))
    # selection-aware over the repo-style search: A and its graphical base fixed, the "extra" sign E
    # (both sides, 417 x 2 = 834 candidates) free.  Equal-sized search on matched decoy (A', base') pairs.
    base_pos = {'roof 65 -> 87-59': 'C', 'marked fish 66 -> 87-60': 'C',
                'surrounding marks 60 -> 59-211': 'B', 'non-fish 15 -> 149-342': 'C'}[name]
    base = C if base_pos == 'C' else B

    def best_extra(a, b):
        best1 = best2 = 0
        for e in VOCAB:
            for k in ((a, e, b), (a, b, e)):
                m = MET.get(k)
                if m:
                    best1 = max(best1, m['pairs_ge1']); best2 = max(best2, m['pairs_ge2'])
        return best1, best2
    ob1, ob2 = best_extra(A, base)
    dec = [best_extra(a, b) for a in pa for b in pool(base, K_MAIN) if a != b]
    res['search_over_extra'] = dict(
        base=base, observed_best_pairs_ge1=ob1, observed_best_pairs_ge2=ob2, proposed_rule_pairs_ge1=obs['pairs_ge1'],
        n_decoy_searches=len(dec),
        decoy_searches_with_best_pairs_ge1_ge_proposed=sum(d[0] >= obs['pairs_ge1'] for d in dec),
        frac_decoy_searches_ge_proposed=sum(d[0] >= obs['pairs_ge1'] for d in dec) / len(dec),
        decoy_searches_with_best_pairs_ge2_ge_proposed_ge2=sum(d[1] >= obs['pairs_ge2'] for d in dec) if obs['pairs_ge2'] else None,
        frac_decoy_searches_ge2=(sum(d[1] >= obs['pairs_ge2'] for d in dec) / len(dec)) if obs['pairs_ge2'] else None,
        decoy_best_pairs_ge1_mean=sum(d[0] for d in dec) / len(dec))
    return res


BIGRAM = Counter()
for s in SEQS:
    for j in range(len(s) - 1):
        BIGRAM[(s[j], s[j + 1])] += 1


# ---------------------------------------------------------------- family-level search null
OCC = defaultdict(list)       # sign -> list of (t, j)
for t in SEQS:
    for j, x in enumerate(t):
        OCC[x].append((t, j))


def family_search(pairs):
    """Repo's modifier search for a set of (base, modified) pairs, inverse enumeration.
    Returns ranking rows keyed (side, extra)."""
    hits = defaultdict(list)    # (side, extra) -> [(base, modified, s, t)]
    for base, mod in pairs:
        for t, j in OCC.get(base, ()):
            if j >= 1:                       # extra before base
                s = t[:j - 1] + (mod,) + t[j + 1:]
                if s in SEQS:
                    hits[('before', t[j - 1])].append((base, mod, s, t, j - 1))
            if j + 1 < len(t):               # extra after base
                s = t[:j] + (mod,) + t[j + 2:]
                if s in SEQS:
                    hits[('after', t[j + 1])].append((base, mod, s, t, j))
    rows = []
    for (side, extra), hh in hits.items():
        rows.append(dict(extra=extra, side=side, base_count=len({h[0] for h in hh}), pairs=len(hh),
                         pairs_with_two_unchanged_signs=sum(len(h[2]) - 1 >= 2 for h in hh),
                         distinct_contexts=len({(h[2][:h[4]], h[2][h[4] + 1:]) for h in hh})))
    rows.sort(key=lambda x: (-x['base_count'], -x['pairs_with_two_unchanged_signs'], -x['pairs'], x['extra'], x['side']))
    return rows


def family_summary(rows):
    if not rows:
        return dict(top=(0, 0, 0), max_pairs=0, max_pairs2=0, max_bases=0, max_contexts=0)
    t = rows[0]
    return dict(top=(t['base_count'], t['pairs_with_two_unchanged_signs'], t['pairs']),
                max_pairs=max(r['pairs'] for r in rows), max_pairs2=max(r['pairs_with_two_unchanged_signs'] for r in rows),
                max_bases=max(r['base_count'] for r in rows), max_contexts=max(r['distinct_contexts'] for r in rows))


def decoy_family(pairs, rng, k=K_MAIN):
    """Injective sign relabelling of the real family; each sign -> a sign matched on frequency+position."""
    signs = sorted({x for p in pairs for x in p})
    rng.shuffle(signs)
    used, mp = set(), {}
    for x in signs:
        opts = [y for y in pool(x, k + 10) if y not in used][:k]
        y = rng.choice(opts); mp[x] = y; used.add(y)
    return [(mp[b], mp[m]) for b, m in pairs]


def family_null(name, pairs, ranking_file):
    # validate reproduction against the repo's stored ranking
    rows = family_search(pairs)
    stored = [r for r in json.load(open(ranking_file)) if r['family'] == name]
    stored_set = {(r['side'], r['extra']): (r['base_count'], r['pairs'], r['pairs_with_two_unchanged_signs'],
                                            r['distinct_contexts']) for r in stored}
    mine_set = {(r['side'], r['extra']): (r['base_count'], r['pairs'], r['pairs_with_two_unchanged_signs'],
                                          r['distinct_contexts']) for r in rows}
    reproduces = stored_set == mine_set
    obs = family_summary(rows)
    rng = random.Random(SEED + len(pairs))
    dec = []
    for _ in range(N_FAMILY):
        dec.append(family_summary(family_search(decoy_family(pairs, rng))))
    out = dict(family=name, n_pairs=len(pairs), n_candidate_extras=2 * 417,
               reproduces_repo_ranking_exactly=reproduces,
               observed=obs, top_rows=rows[:6], n_decoy_families=N_FAMILY)
    for m in ('max_pairs', 'max_pairs2', 'max_bases', 'max_contexts'):
        v = [d[m] for d in dec]; o = obs[m]
        out[m] = dict(observed=o, decoys_ge_observed=sum(x >= o for x in v), frac_ge=sum(x >= o for x in v) / len(v),
                      decoy_mean=sum(v) / len(v), decoy_max=max(v))
    v = [d['top'] for d in dec]; o = tuple(obs['top'])
    out['top_key_lexicographic'] = dict(observed=list(o), decoys_ge_observed=sum(tuple(x) >= o for x in v),
                                       frac_ge=sum(tuple(x) >= o for x in v) / len(v))
    return out


def main():
    res = dict(seed=SEED, k_main=K_MAIN, k_wide=K_WIDE, n_wide=N_WIDE, n_family_decoys=N_FAMILY,
               data=dict(unique_strict_lines=len(SEQS), distinct_signs=len(count)),
               matching=dict(distance='|log2 freq diff| + 2*(|d initial share| + |d final share|); shares over lines of length>=2; '
                                     'frequency = occurrences in unique strict lines',
                             excluded_from_decoy_pools='every sign in TICK_PAIRS, ROOF_PAIRS, PARTS or the four proposed rewrites'))
    res['proposed_rule_profiles'] = {n: {str(x): dict(count=count[x], p_initial=round(profile[x][1], 3), p_final=round(profile[x][2], 3))
                                         for x in r} for n, r in PROPOSED.items()}
    res['rules'] = {n: rule_null(n, r) for n, r in PROPOSED.items()}
    res['family_search_null'] = [
        family_null('four_surrounding_strokes', TICK_PAIRS, ROOT / 'research/data/semantic_search_20260906/modifier_ranking.json'),
        family_null('roof', ROOF_PAIRS, ROOT / 'research/data/semantic_search_20260906/modifier_ranking.json')]
    res['census'] = census()
    (HERE / 'alternation_null_results.json').write_text(json.dumps(res, indent=1, sort_keys=True) + '\n')
    # compact console summary
    for n, r in res['rules'].items():
        m = r['null_main']['pairs_ge1']; m2 = r['null_main']['pairs_ge2']
        print(f"{n}: obs pairs>=1 {r['observed']['pairs_ge1']} (>=2: {r['observed']['pairs_ge2']}); "
              f"decoys {m['n_decoys']}: P(>=obs)={m['frac_ge']:.4f}, pct={m['percentile_midrank']:.2f}; "
              f">=2-shared P={m2['frac_ge']:.4f}")
    for n, r in res['rules'].items():
        print(n, 'search over extra:', {k: v for k, v in r['search_over_extra'].items()})
    for f in res['family_search_null']:
        print(f['family'], f['reproduces_repo_ranking_exactly'], f['observed'], {k: f[k]['frac_ge'] for k in ('max_pairs', 'max_pairs2', 'max_bases', 'max_contexts')},
              f['top_key_lexicographic'])
    print(json.dumps({k: v for k, v in res['census'].items() if k != 'top_recurring'}, indent=1))


if __name__ == '__main__':
    main()
