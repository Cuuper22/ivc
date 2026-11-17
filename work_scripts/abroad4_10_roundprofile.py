#!/usr/bin/env python3
"""STEP 10 of abroad4 (new idea): does the sign profile of the round seals found abroad explain the round seals found at home?
PREDICTION (written before running): a sign-frequency model that mixes half home-seal frequencies and half the round-seal
frequencies of the 25 foreign round seals (core + unknown site) predicts the tokens of the 15 home round seals better than the
home frequencies alone, by at least 0.3 bit per sign, and better than 97.5% of mixtures that use 25 random matched home seals
in place of the foreign round seals.
Unit: bits per sign over the signs of home round seals (every sign scored; unseen signs get the add-0.5 floor of both models).
Output: work_data/abroad4/roundprofile.csv
"""
from abroad4_common import *
pool = score_home_pool()
core = list(F[F.tier == 'core'].itertuples()); unk = list(F[F.tier == 'unk_round'].itertuples())
rr = [r for r in core + unk if r.kind == 'seal' and r.round]
home_round = F[(F.tier == 'home') & F['round']]
hr_keys = set(home_round.tok)
def rs(t): return [s for s in t if real(s)]
# home base frequencies: all home distinct texts EXCEPT the home round seals themselves
base = collections.Counter(s for x, v in home_distinct.items() if x not in hr_keys for s in rs(x))
signs = sorted(set(GV) | {s for r in rr for s in rs(r.tok)}); Vn = len(signs)
def probs(c):
    n = sum(c.values()); return {s: (c.get(s, 0) + 0.5) / (n + 0.5 * Vn) for s in signs}
pb = probs(base)
test = [s for x in hr_keys for s in rs(x)]
def bits(p): return -np.mean([np.log2(p[s]) for s in test])
def mix(c): q = probs(c); return {s: 0.5 * pb[s] + 0.5 * q[s] for s in signs}
b0 = bits(pb)
fc = collections.Counter(s for r in rr for s in rs(r.tok))
b1 = bits(mix(fc))
rng = np.random.default_rng(1010)
byn = collections.defaultdict(list)
for j, t in enumerate(pool):
    if t.intact and t.tok not in hr_keys: byn[(t.kind, t.ag, len(t.tok))].append(j)
def cand_n(kind, ag, m):
    c = byn.get((kind, ag, m), [])
    if len(c) >= 5: return c
    c = [j for k in (m - 1, m, m + 1) for j in byn.get((kind, ag, k), [])]
    if len(c) >= 5: return c
    return [j for (k2, a2, k), L in byn.items() if abs(k - m) <= 1 for j in L]
cs = [np.array(cand_n(r.kind, r.ag, max(1, len(rs(r.tok))))) for r in rr]
D = np.array([bits(mix(collections.Counter(s for k in range(len(cs)) for s in rs(pool[rng.choice(cs[k])].tok)))) for _ in range(1000)])
# the control must not reuse the home round seals: they are removed from candidates above
log(f'home round seals: {len(hr_keys)} distinct texts, {len(test)} signs')
log(f'home frequencies alone {b0:.3f} bits/sign; half foreign-round-seal profile {b1:.3f} (gain {b0 - b1:.3f}); with 25 random matched home seals instead: {D.mean():.3f} (gain {b0 - D.mean():.3f}, best {D.min():.3f}); P(random <= foreign) {(np.sum(D <= b1) + 1) / 1001:.4f}')
pd.DataFrame([dict(home_alone=b0, with_foreign_round_profile=b1, with_random_home_mean=D.mean(), with_random_home_min=D.min(), P=(np.sum(D <= b1) + 1) / 1001, signs=len(test), texts=len(hr_keys))]).to_csv(f'{OUT4}/roundprofile.csv', index=False)

# redesign after the profile test went against (prediction written before this block ran): home round seals do NOT carry the
# person + stroke make-up of foreign round seals (person signs under 5% of their signs, strokes under 25%).
PERSON = {'090', '091', '093', '095'}
STROKES = {s for s in GV if V2CLASS.get(s) in ('NUM_SHORT', 'NUM_TALL', 'NUM_NAME')} | {'001', '002', '003', '004', '005', '031', '032', '033', '055', '013'}
n = len(test)
log(f'home round seals: person signs {sum(s in PERSON for s in test)} of {n} = {sum(s in PERSON for s in test)/n:.3f}; stroke signs {sum(s in STROKES for s in test)} of {n} = {sum(s in STROKES for s in test)/n:.3f}')
log('home round seal texts: ' + '; '.join('-'.join(x) for x in hr_keys))
