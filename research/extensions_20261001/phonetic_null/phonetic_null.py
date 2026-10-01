#!/usr/bin/env python3
"""Study 5: chance baseline for whole-inscription Sanskrit-dictionary key fits.

IMPORTANT: the repo's own optimizer for decoding_followup_20260907.md section 1 is NOT in the
repository (neither in the tree nor in git history; the report says it lives in a "downloadable
research packet" that was not committed).  This script is therefore an INDEPENDENT RE-IMPLEMENTATION
of the method as described in that report, not the original code.  It is used only to compare real
vs control corpora under one identical optimizer, budget and seeds.  Numbers are not claimed to
reproduce 54/146 train, 4/56 held from the report.

Method (as described in the report, simplified where it was unspecified):
  * Dictionary: Monier-Williams headwords (SLP1), same extraction as
    campaigns/integrated_20260906/completion/route_d/run_completion_d.py (H1-H4 key1, [A-Za-z]+).
  * Chunks: split after each vowel, final consonant tail attached to the last chunk.
  * Eligible lines: distinct strict Mahadevan lines of length 2-10 made only of the 40 most frequent
    signs plus the fish family (59,60,65,66,67,68,70,71,72,73).
  * Key: injective sign -> chunk assignment.  A line "matches" if its chunk tuple is exactly the
    syllabified chunk tuple of some headword.
  * Objective per line: BONUS * match + mean chunk-bigram log-prob under the dictionary.
  * Search: simulated annealing, guided proposals (headword hole index) + random proposals.
    Key selected by TRAINING score only; held lines are scored once with the final key.
Controls (same size, same split indices, same optimizer, budget and seeds):
  within_line  : sign order permuted inside each line
  across_corpus: all sign tokens shuffled across lines, line lengths kept
  iid_matched  : each line = real length distribution, signs drawn i.i.d. from real sign frequencies
  markov1/2    : lines generated from an order-1 / order-2 Markov model of the real eligible lines (same
                 count; keeps local sign n-gram repetition, which the three controls above destroy)
Deterministic: fixed seeds; no timestamps in output.
"""
import csv, json, math, random, re, sys, time
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MW = ROOT / 'evidence/tmp/002390x_3335_yajnadevam_repo_trace_20260531/repo/dev-tools/ashtadhyayi/assets/mw.xml'
FISH = {59, 60, 65, 66, 67, 68, 70, 71, 72, 73}
SEEDS = list(range(101, 109))        # 8 seeds
RESTARTS = 6
PROPOSALS = 40000                    # per restart
BONUS = 8.0
T0, T1 = 2.0, 0.15
GUIDED = 0.7
HELD_FRAC = 0.2
VOWELS = set('aAiIuUfFxXeEoO')
CONDITIONS = ['real', 'within_line', 'across_corpus', 'iid_matched', 'markov1', 'markov2']


def chunks(w):
    out, cur = [], ''
    for ch in w:
        cur += ch
        if ch in VOWELS:
            out.append(cur); cur = ''
    if cur:
        if not out:
            return None
        out[-1] += cur
    return tuple(out)


def load_dictionary():
    words, entries = set(), 0
    for _, e in ET.iterparse(MW, events=['end']):
        if re.fullmatch(r'H[1-4][AB]?', e.tag):
            entries += 1
            w = e.findtext('./h/key1')
            if w and re.fullmatch('[A-Za-z]+', w):
                words.add(w)
            e.clear()
    return words, entries


def load_lines():
    rows = [r for r in csv.DictReader(open(ROOT / 'research/data/mahadevan_20260905/concordance_rows.csv'))
            if r['strict'] == '1']
    seqs = Counter()
    for r in rows:
        seqs[tuple(int(r[f'S{i}']) for i in range(1, 15) if r[f'S{i}'])] += 1
    sign_n = Counter(x for s, n in seqs.items() for x in s for _ in range(n))
    allowed = {x for x, _ in sign_n.most_common(40)} | FISH
    lines = sorted(s for s in seqs if 2 <= len(s) <= 10 and set(s) <= allowed)
    return lines, sorted(allowed)


# ----------------------------------------------------------------- global data (built once, shared by fork)
WORDS, N_ENTRIES = load_dictionary()
CH = [c for c in (chunks(w) for w in sorted(WORDS)) if c]
UNIT_ID = {u: i for i, u in enumerate(sorted({u for c in CH for u in c}))}
N_UNITS = len(UNIT_ID)
LINES, SIGNS = load_lines()
LENGTHS = sorted({len(s) for s in LINES})
HEAD = {n: set() for n in LENGTHS}                   # exact headword chunk tuples (unit ids) by length
HOLE = defaultdict(list)                             # (n, pos, rest) -> candidate unit ids
BG, CU, UNI = Counter(), Counter(), Counter()
for c in CH:
    ids = tuple(UNIT_ID[u] for u in c)
    for u in ids:
        UNI[u] += 1
    seq = (-1,) + ids + (-2,)
    for a, b in zip(seq, seq[1:]):
        BG[(a, b)] += 1; CU[a] += 1
    if len(ids) in HEAD:
        HEAD[len(ids)].add(ids)
for n in LENGTHS:
    seen = set()
    for ids in HEAD[n]:
        for p in range(n):
            key = (n, p, ids[:p] + ids[p + 1:])
            HOLE[key].append(ids[p])
UNI_TOT = sum(UNI.values())
UNI_P = {u: UNI[u] / UNI_TOT for u in UNI}
UNIT_LIST = sorted(UNI)
UNIT_W = [UNI[u] ** 0.5 for u in UNIT_LIST]


def lp(a, b):
    return math.log(0.9 * BG.get((a, b), 0) / CU[a] + 0.1 * UNI_P.get(b, 1e-9)) if CU.get(a) else math.log(UNI_P.get(b, 1e-9))


LP_CACHE = {}


def line_score(ids):
    n = len(ids)
    seq = (-1,) + ids + (-2,)
    s = 0.0
    for a, b in zip(seq, seq[1:]):
        v = LP_CACHE.get((a, b))
        if v is None:
            v = LP_CACHE[(a, b)] = lp(a, b)
        s += v
    s /= (n + 1)
    return s + (BONUS if ids in HEAD[n] else 0.0)


def is_match(ids):
    return ids in HEAD[len(ids)]


def anneal(train, rng):
    signs = sorted({x for s in train for x in s})
    by_sign = defaultdict(list)
    for i, s in enumerate(train):
        for x in set(s):
            by_sign[x].append(i)
    chosen = rng.sample(UNIT_LIST, len(SIGNS))
    key = dict(zip(SIGNS, chosen))
    owner = {u: x for x, u in key.items()}

    def L(i):
        return tuple(key[x] for x in train[i])
    scores = [line_score(L(i)) for i in range(len(train))]
    total = sum(scores)
    best_total, best_key = total, dict(key)
    for step in range(PROPOSALS):
        T = T0 * (T1 / T0) ** (step / PROPOSALS)
        s = rng.choice(signs)
        old = key[s]
        new = None
        if rng.random() < GUIDED:
            i = rng.choice(by_sign[s])
            line = train[i]
            p = rng.choice([j for j, x in enumerate(line) if x == s])
            rest = tuple(key[x] for j, x in enumerate(line) if j != p)
            cand = HOLE.get((len(line), p, rest))
            if cand:
                new = rng.choice(cand)
        if new is None:
            new = rng.choices(UNIT_LIST, UNIT_W)[0]
        if new == old:
            continue
        t = owner.get(new)                       # injective: swap with current owner
        touched = set(by_sign[s]) | (set(by_sign[t]) if t is not None and t in by_sign else set())
        before = sum(scores[i] for i in touched)
        key[s] = new
        if t is not None:
            key[t] = old
        new_scores = {i: line_score(L(i)) for i in touched}
        delta = sum(new_scores.values()) - before
        if delta >= 0 or rng.random() < math.exp(delta / T):
            owner[new] = s
            owner[old] = t if t is not None else None
            if t is None:
                del owner[old]
            for i, v in new_scores.items():
                scores[i] = v
            total += delta
            if total > best_total:
                best_total, best_key = total, dict(key)
        else:
            key[s] = old
            if t is not None:
                key[t] = new
    return best_total, best_key


def make_condition(cond, rng):
    lines = [list(s) for s in LINES]
    if cond == 'real':
        out = [tuple(s) for s in lines]
    elif cond == 'within_line':
        out = []
        for s in lines:
            s = s[:]; rng.shuffle(s); out.append(tuple(s))
    elif cond == 'across_corpus':
        flat = [x for s in lines for x in s]; rng.shuffle(flat)
        out, k = [], 0
        for s in lines:
            out.append(tuple(flat[k:k + len(s)])); k += len(s)
    elif cond == 'iid_matched':
        freq = Counter(x for s in lines for x in s)
        pop, w = zip(*sorted(freq.items()))
        out = [tuple(rng.choices(pop, w, k=len(s))) for s in lines]
    elif cond in ('markov1', 'markov2'):
        order = int(cond[-1])
        nxt = defaultdict(Counter)
        for s in lines:
            seq = ['^'] * order + s + ['$']
            for k in range(order, len(seq)):
                nxt[tuple(seq[k - order:k])][seq[k]] += 1
                if order == 2:
                    nxt[(seq[k - 1],)][seq[k]] += 1          # backoff table
        out = []
        while len(out) < len(lines):
            seq = ['^'] * order
            while True:
                ctx = tuple(seq[-order:])
                tab = nxt.get(ctx) or nxt[(seq[-1],)]
                pop, w = zip(*sorted(tab.items(), key=lambda kv: str(kv[0])))
                x = rng.choices(pop, w)[0]
                if x == "$" or len(seq) - order >= max(LENGTHS):
                    break
                seq.append(x)
            body = tuple(seq[order:])
            if len(body) in LENGTHS:
                out.append(body)
    return out


def bigram_cov(train, held):
    seen = {(a, b) for s in train for a, b in zip(s, s[1:])}
    v = [sum((a, b) in seen for a, b in zip(s, s[1:])) / (len(s) - 1) for s in held]
    return sum(v) / len(v)


def run_one(args):
    cond, seed = args
    split_rng = random.Random(seed)                                 # identical train/held index split across conditions
    idx = list(range(len(LINES))); split_rng.shuffle(idx)
    n_held = round(HELD_FRAC * len(idx))
    held_idx, train_idx = set(idx[:n_held]), idx[n_held:]
    lines = make_condition(cond, random.Random(seed + 555))
    # distinct types per side (a control can create duplicates)
    train = sorted({lines[i] for i in train_idx})
    held = sorted({lines[i] for i in held_idx} - set(train))
    best = None
    for r in range(RESTARTS):
        rr = random.Random(seed * 1000 + r)                          # same optimizer seeds across conditions
        tot, key = anneal(train, rr)
        if best is None or tot > best[0]:
            best = (tot, key)
    key = best[1]
    tm = sum(is_match(tuple(key[x] for x in s)) for s in train)
    hm = sum(is_match(tuple(key[x] for x in s)) for s in held)
    return dict(condition=cond, seed=seed, n_train=len(train), train_matches=tm, n_held=len(held), held_matches=hm,
                train_rate=tm / len(train), held_rate=hm / len(held),
                held_sign_bigram_seen_in_train=bigram_cov(train, held), best_train_objective=round(best[0], 4))


def mean_sd(v):
    m = sum(v) / len(v)
    sd = (sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** 0.5 if len(v) > 1 else 0.0
    return m, sd


def main():
    print(f'entries {N_ENTRIES} headwords {len(WORDS)} units {N_UNITS} eligible lines {len(LINES)} signs {len(SIGNS)}', flush=True)
    jobs = [(c, s) for s in SEEDS for c in CONDITIONS]
    with Pool(4) as p:
        res = p.map(run_one, jobs, chunksize=1)
    summary = {}
    for c in CONDITIONS:
        rr = [r for r in res if r['condition'] == c]
        d = {}
        for k in ('train_matches', 'held_matches', 'train_rate', 'held_rate', 'held_sign_bigram_seen_in_train'):
            m, sd = mean_sd([r[k] for r in rr]); d[k] = dict(mean=round(m, 4), sd=round(sd, 4))
        d['mean_n_train'] = sum(r['n_train'] for r in rr) / len(rr)
        d['mean_n_held'] = sum(r['n_held'] for r in rr) / len(rr)
        summary[c] = d
    # paired by seed (same split indices, same optimizer seeds)
    paired = {}
    real = {r['seed']: r for r in res if r['condition'] == 'real'}
    for c in CONDITIONS[1:]:
        ctl = {r['seed']: r for r in res if r['condition'] == c}
        for k in ('train_rate', 'held_rate', 'held_matches', 'held_sign_bigram_seen_in_train'):
            diffs = [real[s][k] - ctl[s][k] for s in SEEDS]
            m, sd = mean_sd(diffs)
            paired[f'real_minus_{c}:{k}'] = dict(mean=round(m, 4), sd=round(sd, 4),
                                                seeds_real_greater=sum(d > 0 for d in diffs), seeds_equal=sum(d == 0 for d in diffs),
                                                seeds_real_smaller=sum(d < 0 for d in diffs))
    out = dict(
        implementation='independent re-implementation; the repo optimizer script is absent from tree and git history',
        dictionary=dict(entries_parsed=N_ENTRIES, distinct_headwords=len(WORDS), chunk_units=N_UNITS,
                        report_says=dict(entries=283809, headwords=192482, units=7236)),
        eligible_lines=len(LINES), eligible_signs=len(SIGNS), line_lengths=dict(sorted(Counter(len(s) for s in LINES).items())),
        budget=dict(seeds=SEEDS, restarts=RESTARTS, proposals_per_restart=PROPOSALS, bonus=BONUS, held_fraction=HELD_FRAC,
                    temperature=[T0, T1], guided_proposal_prob=GUIDED),
        summary=summary, paired_by_seed=paired, runs=res)
    (HERE / 'phonetic_null_results.json').write_text(json.dumps(out, indent=1, sort_keys=True) + '\n')
    print(json.dumps(dict(summary=summary, paired=paired), indent=1))


if __name__ == '__main__':
    t = time.time()
    main()
    print('wall seconds', round(time.time() - t), file=sys.stderr)
