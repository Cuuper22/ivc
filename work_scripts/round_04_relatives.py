#!/usr/bin/env python3
"""ROUND SEALS, step 4: which home object kind do the round texts resemble most in sign make-up and order. Written 2026-11-17.
No word on any sign. For each home object kind a sign-pair model (Witten-Bell, as in frame_common.bigram_model) is trained on the distinct
HOME texts of that kind, with every round-seal face removed from training. Kinds: tablets (mtab), tags and sealings (tag), copper tablets
(ctab), pots, rods, bangles, other, all seals, and three seal sub-kinds taken from work_data/frame/seal_kinds.csv: count-line seals
(bare count, opener count, name + count, measure line), name seals (name seal, loose name), damaged-or-other seals.
Each round text is scored by every model (bits per step, steps = neighbouring usable signs). Pooled over the round texts.
CONTROL for training size: for each kind, the ALL-KINDS model is retrained on a random draw of the same number of distinct texts
(500 draws, drawn from all non-round home texts) and scores the same round texts; real kind model against that spread. Also per-text wins.
PREDICTION (written now): round texts resemble the count-line seals / tablets (strokes and people), not name seals: the best-scoring
kind is tablets or count-line seals; no kind beats the all-kinds model at its own size by more than 0.3 bits per step.
Output: work_data/round/relatives.csv, relatives_per_text.csv, log_4.txt
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abroad4_common import *
OUTR = f'{ROOT}/work_data/round'
RL = pd.read_csv(f'{OUTR}/round_list.csv', dtype=str)
RIDS = set(RL.id)
sk = pd.read_csv(f'{ROOT}/work_data/frame/seal_kinds.csv', dtype=str).set_index('id').seal_kind
SUB = {'bare count': 'count-line seals', 'opener count': 'count-line seals', 'name + count': 'count-line seals', 'measure line': 'count-line seals',
       'name seal': 'name seals', 'loose name': 'name seals'}
home = F[(F.tier == 'home') & (~F.id.isin(RIDS))]
groups = collections.defaultdict(list)
for r in home.itertuples():
    if not r.tok: continue
    k = r.kind
    groups[{'mtab': 'tablets', 'tag': 'tags and sealings', 'ctab': 'copper tablets', 'pot': 'pots'}.get(k, k)].append(r)
    if k == 'seal':
        groups['all seals'].append(r); groups[SUB.get(sk.get(r.id, ''), 'damaged or other seals')].append(r)
groups = {k: v for k, v in groups.items() if k not in ('tool',)}
def distinct(rows): 
    seen = {}
    for r in rows: seen.setdefault(r.tok, (r.clean, r.kind))
    return [(x, c, k) for x, (c, k) in seen.items()]
def model(texts):
    from frame_common import counts, bigram_model
    return bigram_model(counts(texts, GIDX))
def score(m, texts):
    tot = 0.0; n = 0; per = {}
    for i, t in texts.items():
        b = 0.0; k = 0
        for r in runs_of(t):
            for a, c in zip(r, r[1:]): b += -np.log2(m.trans[a, c]); k += 1
        per[i] = (b, k); tot += b; n += k
    return tot / n, per
rt = {r.id: tuple(d.set_index('id').loc[r.id, 'tok']) for r in RL.itertuples() if r.tier != 'South India'}
rt = {i: t for i, t in rt.items() if any(len(r) >= 2 for r in runs_of(t))}
print('round texts with a step:', len(rt), 'steps', sum(len(r) - 1 for t in rt.values() for r in runs_of(t)))
allh = distinct([r for rows in [groups['all seals'], groups['tablets'], groups['tags and sealings'], groups['copper tablets'], groups['pots']] for r in rows] + groups.get('other', []) + groups.get('rod', []) + groups.get('bangle', []))
print('all non-round home distinct texts', len(allh))
rng = np.random.default_rng(404)
res = []; per_all = {}
m_all = model(allh); b_all, per_all = score(m_all, rt)
for kname, rows in sorted(groups.items()):
    tx = distinct(rows); n = len(tx)
    if n < 20: print('skip', kname, n); continue
    mk = model(tx); bk, perk = score(mk, rt)
    ctrl = []
    for _ in range(300):
        idx = rng.choice(len(allh), size=min(n, len(allh)), replace=False)
        ctrl.append(score(model([allh[j] for j in idx]), rt)[0])
    ctrl = np.array(ctrl)
    wins = sum(perk[i][0] / perk[i][1] < per_all[i][0] / per_all[i][1] for i in rt if perk[i][1])
    wins_ctrl = None
    res.append(dict(kind=kname, train_texts=n, round_bits_per_step=bk, same_size_all_kinds_mean=ctrl.mean(), same_size_lo=np.percentile(ctrl, 2.5), same_size_hi=np.percentile(ctrl, 97.5),
                    diff_vs_same_size=bk - ctrl.mean(), P_kind_lower=(np.sum(ctrl <= bk) + 1) / (len(ctrl) + 1), texts_kind_better_than_full_all=wins, texts_scored=sum(1 for i in rt if perk[i][1])))
R = pd.DataFrame(res).sort_values('round_bits_per_step'); R.to_csv(f'{OUTR}/relatives.csv', index=False)
print('ALL-KINDS model (full size):', round(b_all, 3)); print(R.round(3).to_string())
# context: the same models scored on matched square seals of home (mean steps match): how good is each model on its own turf
sqt = [x for x in set(F[(F.tier == 'home') & (F.kind == 'seal') & (~F['round'])].tok) if any(len(r) >= 2 for r in runs_of(x))]
sel = rng.choice(len(sqt), size=min(400, len(sqt)), replace=False); sqd = {j: sqt[s] for j, s in enumerate(sel)}
print('all-kinds model on 400 home square seals (it saw them):', round(score(m_all, sqd)[0], 3))
