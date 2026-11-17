#!/usr/bin/env python3
"""ROUND SEALS, step 4b: redesign of the kind-relatives test after raw sign-pair models went against (kind models are small and noisy).
REDESIGN: use frame v2 (14 job classes; class-to-class rules learned PER OBJECT KIND, backed off to the pooled rules; frame2_common.class_model_kind)
trained on non-round home texts only. Score every round text under each kind's rules (seal, tag, tablet, copper tablet, pot) and under the pooled rules.
Because classes are few, small kinds are not starved. Control: the same score for matched home square seals under each kind's rules, so a kind that is
simply a good all-round grammar does not look like a relative; the number that matters is (round bits - matched-square bits) per kind: the smaller, the closer.
PREDICTION (written now): the 'pot' and 'tag' rules (short, loose texts) fit round seals better relative to squares than the seal rules do.
Output: work_data/round/relatives_classes.csv, log_4b.txt
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abroad4_common import *
OUTR = f'{ROOT}/work_data/round'
RL = pd.read_csv(f'{OUTR}/round_list.csv', dtype=str); RIDS = set(RL.id)
home = F[(F.tier == 'home') & (~F.id.isin(RIDS))]
seen = {}
for r in home.itertuples():
    if r.tok and r.tok not in seen: seen[r.tok] = (r.clean, r.kind)
train = [(x, c, k) for x, (c, k) in seen.items()]
C, CK = kind_counts(train, GIDX)
v2 = class_model_kind(C, CK, V2CLASS, 'frame v2', GV)
def bits_of(model, tok):
    b = 0.0; n = 0
    for r in runs_of(tok):
        for a, c in zip(r, r[1:]): b += -np.log2(model.trans[a, c]); n += 1
    return b, n
rt = {r.id: tuple(d.set_index('id').loc[r.id, 'tok']) for r in RL.itertuples() if r.tier != 'South India'}
rt = {i: t for i, t in rt.items() if any(len(r) >= 2 for r in runs_of(t))}
sq = [x for x in set(F[(F.tier == 'home') & (F.kind == 'seal') & (~F['round']) & (~F.id.isin(RIDS))].tok) if any(len(r) >= 2 for r in runs_of(x))]
rng = np.random.default_rng(55)
# length-matched square draws: for each round text, 400 random square texts with the same step count
def steps(t): return sum(len(r) - 1 for r in runs_of(t))
sqby = collections.defaultdict(list)
for x in sq: sqby[steps(x)].append(x)
rows = []
for kname, kk in [('pooled rules (all kinds)', 'other'), ('seal rules', 'seal'), ('tag and sealing rules', 'tag'), ('tablet rules', 'mtab'), ('copper tablet rules', 'ctab'), ('pot rules', 'pot')]:
    m = v2.per[kk]
    rb = sum(bits_of(m, t)[0] for t in rt.values()); rn = sum(bits_of(m, t)[1] for t in rt.values())
    ctrl = []
    for _ in range(500):
        tb = 0.0; tn = 0
        for t in rt.values():
            s = steps(t); c = sqby[min(max(s, 1), max(sqby))] if sqby.get(s) is None or len(sqby[s]) < 5 else sqby[s]
            x = c[rng.integers(len(c))]; b, n = bits_of(m, x); tb += b; tn += n
        ctrl.append(tb / tn)
    ctrl = np.array(ctrl)
    rows.append(dict(rules=kname, round_bits=rb / rn, matched_square_bits=ctrl.mean(), gap=rb / rn - ctrl.mean(), P_round_higher=(np.sum(ctrl >= rb / rn) + 1) / 501))
R = pd.DataFrame(rows); R.to_csv(f'{OUTR}/relatives_classes.csv', index=False); print(R.round(3).to_string())
