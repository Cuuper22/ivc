#!/usr/bin/env python3
"""PHRASES step 1: the list of fixed phrases. Fixed 2026-11-17 BEFORE any count was made.

RULE (every pair, triple and four-sign run in the first catalogue, Lipi, distinct texts):
  (1) COUNT   : the run occurs in at least 8 distinct texts;
  (2) ORDER   : in order at least 90% of the time: n(run) / (n(run) + n(run reversed)) >= 0.90
                (n = distinct texts; a run that reads the same backwards never passes);
  (3) MARGIN  : lift >= 5, lift = windows seen / windows expected if each place took a sign by sign frequency alone
                (expected = windows * product of the sign shares).
  (4) CONFIRM : on the new texts (second catalogue lines with no partner in the first catalogue; distinct strings; never used
                to build anything): predicted count = first-catalogue lift * expected count in the new texts.
                predicted < 2 -> 'untestable'. Otherwise 'confirmed' if seen >= 2 times, in order >= 90%, and new lift >= 3;
                else 'not confirmed'.
CONTROL: the same rule run on the first catalogue with sign order shuffled inside every run of every text (20 shuffles, seeds
  700-719). Count of runs passing (1)-(3) per shuffle.
NESTING: a run is 'nested' if a longer passing run contains it and has at least 90% of its count (same unit seen shorter).
  Nested runs are listed and counted but left out of the top 100 atlas.
GROUPS (frame v2 classes of the signs; fixed order of rules): front = holds a front word or slot sign (OPEN or SLOT class);
  count line = holds a short number, tall number, measure (NUM_SHORT, NUM_TALL, MEASURE);
  ending = a pair whose last sign is a closer or after-jar title (CLOSER, TITLE) and nothing counted;
  name = everything else (name front, name parts, tall two, counted things inside names, after-measure, name back,
  and any run of three or four that ends in a closer: a name with its ending).
PREDICTIONS (written before the run):
  P1 between 120 and 300 runs pass (1)-(3); pairs are the biggest group, then triples, then fours.
  P2 at least 75% of the testable ones are confirmed on the new texts.
  P3 the shuffled corpora pass fewer than 10% of the real number (mean).
  P4 names are the largest group; front, count line and ending each have at least 10.
Output: work_data/phrases/phrase_list.csv, phrase_shuffle_control.csv, log_1.txt
"""
from phrases_common import *
import random
LOG = open(f'{OUTP}/log_1.txt', 'w')
def say(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n'); LOG.flush()

NMIN, ORDER, LIFT = 8, 0.90, 5.0
KS = (2, 3, 4)

def passing(nt, win, uni, N):
    rows = {}
    for k in KS:
        for p, n in nt[k].items():
            if n < NMIN: continue
            rev = nt[k].get(p[::-1], 0) if p != p[::-1] else n
            order = n / (n + rev) if p != p[::-1] else 0.5
            if order < ORDER: continue
            e = expected(p, uni, N, win[k]); lift = n / e if e > 0 else np.inf
            if lift < LIFT: continue
            rows[p] = dict(n=n, rev=rev, order=order, expected=e, lift=lift)
    return rows

T = distinct_texts(); say('distinct first-catalogue texts', len(T))
nt, win, uni, N = count_phrases(T)
say('windows', win, 'sign tokens', N)
R = passing(nt, win, uni, N)
say('passing (1)-(3):', len(R), {k: sum(1 for p in R if len(p) == k) for k in KS})

# ---- control: order shuffled inside each run
def shuffled(texts, seed):
    rnd = random.Random(seed); out = []
    for x in texts:
        y = list(x)
        i = 0; n = len(y)
        while i < n:
            if not is_sign(y[i]): i += 1; continue
            j = i
            while j < n and is_sign(y[j]): j += 1
            seg = y[i:j]; rnd.shuffle(seg); y[i:j] = seg; i = j
        out.append(tuple(y))
    return out
ctl = []
for sd in range(700, 720):
    S = shuffled(T, sd); a, b, c_, N_ = count_phrases(S); Rs = passing(a, b, c_, N_)
    ctl.append(dict(seed=sd, passing=len(Rs), pairs=sum(1 for p in Rs if len(p) == 2), triples=sum(1 for p in Rs if len(p) == 3), fours=sum(1 for p in Rs if len(p) == 4),
                    max_count=max([r['n'] for r in Rs.values()] or [0])))
    say('shuffle', sd, ctl[-1])
pd.DataFrame(ctl).to_csv(f'{OUTP}/phrase_shuffle_control.csv', index=False)
say('shuffle mean passing', np.mean([c['passing'] for c in ctl]), 'max', max(c['passing'] for c in ctl))

# ---- confirmation on new texts
TN = new_distinct_texts(); say('distinct new texts', len(TN))
ntn, winn, unin, NN = count_phrases(TN)
rows = []
for p, r in R.items():
    k = len(p); n2 = ntn[k].get(p, 0); rev2 = ntn[k].get(p[::-1], 0) if p != p[::-1] else n2
    e2 = expected(p, unin, NN, winn[k]) if all(unin.get(s, 0) > 0 for s in p) else 0.0
    pred = r['lift'] * e2
    lift2 = n2 / e2 if e2 > 0 else np.nan
    order2 = n2 / (n2 + rev2) if (n2 + rev2) else np.nan
    if pred < 2: st = 'untestable'
    elif n2 >= 2 and order2 >= ORDER and lift2 >= 3: st = 'confirmed'
    else: st = 'not confirmed'
    rows.append(dict(phrase='-'.join(p), length=k, n_texts=r['n'], n_reversed=r['rev'], in_order=round(r['order'], 3), lift=round(r['lift'], 1),
                     expected=round(r['expected'], 2), new_n=n2, new_reversed=rev2, new_expected=round(e2, 2), new_predicted=round(pred, 2),
                     new_lift=round(lift2, 1) if lift2 == lift2 else '', new_status=st))
P = pd.DataFrame(rows)
# nesting
pset = {tuple(r.phrase.split('-')): r for r in P.itertuples()}
nested = []
for p, r in pset.items():
    host = ''
    for q, rq in pset.items():
        if len(q) > len(p) and any(q[i:i + len(p)] == p for i in range(len(q) - len(p) + 1)) and rq.n_texts >= 0.9 * r.n_texts:
            host = '-'.join(q) if not host or rq.n_texts > pset[tuple(host.split('-'))].n_texts else host
    nested.append(host)
P['nested_in'] = [nested[i] for i in range(len(P))]
# group by frame v2 classes
def group(p):
    cl = [v2c(s) for s in p]
    if any(c in ('OPEN', 'SLOT') for c in cl): return 'front'
    if any(c in ('NUM_SHORT', 'NUM_TALL', 'MEASURE') for c in cl): return 'count line'
    if len(p) == 2 and cl[-1] in ('CLOSER', 'TITLE'): return 'ending'
    return 'name'
P['classes'] = ['>'.join(v2c(s) for s in r.phrase.split('-')) for r in P.itertuples()]
P['group'] = [group(tuple(r.phrase.split('-'))) for r in P.itertuples()]
P = P.sort_values(['n_texts', 'lift'], ascending=False).reset_index(drop=True)
P.to_csv(f'{OUTP}/phrase_list.csv', index=False)
say('TOTAL passing', len(P), ' by length', P.length.value_counts().to_dict())
say('new-text status', P.new_status.value_counts().to_dict(), ' by length:'); say(P.groupby(['length', 'new_status']).size().unstack(fill_value=0).to_string())
say('groups (all)', P.group.value_counts().to_dict(), ' groups (non-nested)', P[P.nested_in == ''].group.value_counts().to_dict())
say('nested', int((P.nested_in != '').sum()), 'non-nested', int((P.nested_in == '').sum()))
tst = P[P.new_status != 'untestable']; say('testable', len(tst), 'confirmed share', round((tst.new_status == 'confirmed').mean(), 3))
say(P.head(30)[['phrase', 'n_texts', 'in_order', 'lift', 'new_n', 'new_status', 'group', 'nested_in']].to_string())
