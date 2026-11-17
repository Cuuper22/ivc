#!/usr/bin/env python3
"""STEP 9 of abroad4: what the round seals are made of (the redesign after the spelling test went against flatness).
PREDICTION (written before running): round seals reuse a small set of signs: the 8 most frequent signs inside the set cover a larger
share of tokens than the 8 most frequent signs inside matched home sets (spelling with a small set of signs would show it).
Also: the person signs (090 091 093 095) and the stroke signs together make up about half of all round-seal tokens against under
a fifth in matched home seals.
Output: work_data/abroad4/roundcomp.csv
"""
from abroad4_common import *
pool = score_home_pool()
core = list(F[F.tier == 'core'].itertuples()); unk = list(F[F.tier == 'unk_round'].itertuples())
rr = [r for r in core + unk if r.kind == 'seal' and r.round]
def rs(t): return [s for s in t if real(s)]
fc = collections.Counter(s for r in rr for s in rs(r.tok)); n = sum(fc.values())
shapes = pd.read_csv(f'{ROOT}/work_data/sign_shapes.csv', dtype=str).set_index('lipi_wells_number').shape_description.to_dict()
PERSON = {'090', '091', '093', '095'}
STROKES = {s for s in GV if V2CLASS.get(s) in ('NUM_SHORT', 'NUM_TALL', 'NUM_NAME')} | {'001', '002', '003', '004', '005', '031', '032', '033', '055', '013'}
byn = collections.defaultdict(list)
for j, t in enumerate(pool):
    if t.intact: byn[(t.kind, t.ag, len(t.tok))].append(j)
def cand_n(kind, ag, m):
    c = byn.get((kind, ag, m), [])
    if len(c) >= 5: return c
    c = [j for k in (m - 1, m, m + 1) for j in byn.get((kind, ag, k), [])]
    if len(c) >= 5: return c
    return [j for (k2, a2, k), L in byn.items() if abs(k - m) <= 1 for j in L]
rng = np.random.default_rng(909)
cs = [np.array(cand_n(r.kind, r.ag, max(1, len(rs(r.tok))))) for r in rr]
def top8(c): v = sorted(c.values(), reverse=True)[:8]; return sum(v) / sum(c.values())
def comp(c): t = sum(c.values()); return (sum(v for s, v in c.items() if s in PERSON) / t, sum(v for s, v in c.items() if s in STROKES) / t)
t8 = top8(fc); pc = comp(fc)
D = []
for _ in range(2000):
    c = collections.Counter(s for k in range(len(cs)) for s in rs(pool[rng.choice(cs[k])].tok)); D.append((top8(c),) + comp(c))
D = np.array(D)
log(f'round seals: {len(rr)} texts, {n} signs, {len(fc)} distinct signs')
log(f'top-8 signs cover {t8:.3f} of tokens; matched home sets {D[:,0].mean():.3f} (97.5th pct {np.percentile(D[:,0],97.5):.3f}), P home >= round {(np.sum(D[:,0] >= t8) + 1) / 2001:.4f}')
log(f'person signs share {pc[0]:.3f} vs home {D[:,1].mean():.3f} (P {(np.sum(D[:,1] >= pc[0]) + 1) / 2001:.4f}); stroke signs share {pc[1]:.3f} vs home {D[:,2].mean():.3f} (P {(np.sum(D[:,2] >= pc[1]) + 1) / 2001:.4f}); together {pc[0]+pc[1]:.3f} vs {(D[:,1]+D[:,2]).mean():.3f}')
rows = [dict(sign=s, count_round=c, texts_round=sum(s in r.tok for r in rr), home_uses=HOME_USE[s], v2_class=V2CLASS.get(s, '-'), shape=shapes.get(s, '')[:70]) for s, c in fc.most_common(20)]
R = pd.DataFrame(rows); R.to_csv(f'{OUT4}/roundcomp.csv', index=False); print(R.to_string())
