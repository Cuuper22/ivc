#!/usr/bin/env python3
"""ROUND SEALS, step 7: numbers for the four readings (a) outsiders' personal seals, (b) a tally of persons, (c) another language's signs, (d) a local Gulf product.
Written 2026-11-17. No word on any sign.
PREDICTIONS written now, one per reading, each with the observation that would count for it:
 (a) outsiders' names: the man sign should NOT sit in its home job (home: last sign of the text in ~75% of its uses, as the title after the closer); on round seals last in <= 40%.
 (b) tally of persons: a short stroke immediately BEFORE a person sign in >= 5 round texts, with several different stroke heights (1,2,3 ...), not one stroke.
 (c) other language: the round seals share a pair or a run in a fixed order across seals (leave-one-out pair gain > 0): found earlier -0.35 bits (against).
 (d) imitation: signs on round seals are the commonest and simplest ones, little order: rare-at-home share not higher, repeats of a sign inside a text more often than home.
Output: log_7.txt, work_data/round/verdict_numbers.csv
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from abroad4_common import *
from scipy.stats import fisher_exact
OUTR = f'{ROOT}/work_data/round'
RL = pd.read_csv(f'{OUTR}/round_list.csv', dtype=str); RIDS = set(RL.id)
rt = {r.id: tuple(d.set_index('id').loc[r.id, 'tok']) for r in RL.itertuples() if r.tier != 'South India'}
h = F[(F.tier == 'home') & (~F.id.isin(RIDS)) & (F.kind == 'seal')]
def pos(texts, s):
    c = collections.Counter()
    for x in texts:
        for i, t in enumerate(x):
            if t == s: c['first' if i == 0 else ('last' if i == len(x) - 1 else 'mid')] += 1
    return c
home_u = list(set(h.tok)); rows = []
for s in ['090', '091']:
    ch = pos(home_u, s); cr = pos(list(rt.values()), s)
    nh, nr = sum(ch.values()), sum(cr.values()); lh, lr = ch['last'], cr['last']
    p = fisher_exact([[lh, nh - lh], [lr, nr - lr]])[1]
    print(f'{s}: home last {lh}/{nh} ({100*lh/nh:.0f}%), round last {lr}/{nr} ({100*lr/max(nr,1):.0f}%), Fisher P {p:.4f}; round first/mid/last {cr["first"]}/{cr["mid"]}/{cr["last"]}; home {ch["first"]}/{ch["mid"]}/{ch["last"]}')
    rows.append(dict(sign=s, home_last=f'{lh}/{nh}', round_last=f'{lr}/{nr}', P=p))
# (b) short stroke before a person sign
PERSON = {'090', '091', '093', '095'}
SHORT = {'001', '002', '003', '004', '005', '055'}
cnt = collections.Counter(); hits = []
for i, t in rt.items():
    for a, b in zip(t, t[1:]):
        if a in SHORT and b in PERSON: cnt[a] += 1; hits.append((i, a, b))
print('short stroke immediately before a person sign:', len(set(i for i, _, _ in hits)), 'texts', hits)
# home reference: share of home seal texts with a short stroke before a person sign
hh = sum(any(a in SHORT and b in PERSON for a, b in zip(x, x[1:])) for x in home_u); print('home square-and-other seals (distinct texts):', hh, 'of', len(home_u), '= %.2f%%' % (100 * hh / len(home_u)))
nr = sum(1 for t in rt.values() if len(t) >= 2); print('round texts with 2+ tokens', nr, ' = %.1f%% have the unit' % (100 * len(set(i for i, _, _ in hits)) / nr))
print('stroke heights before a person (counts):', dict(cnt))
# tall stroke after twin men
tall = [(i, a, b) for i, t in rt.items() for a, b in zip(t, t[1:]) if a == '091' and b in {'031', '032', '033'}]
print('091 followed by a tall stroke:', tall)
pd.DataFrame(rows).to_csv(f'{OUTR}/verdict_numbers.csv', index=False)
