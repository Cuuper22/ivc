#!/usr/bin/env python3
"""Recheck 8: count-line seal texts turn up on clay impressions: 22.7% against 5.7% for name seals (frame2_seals.py (d),
Lipi tags + second-catalogue sealings) and 24.5% against 4.3% length-matched (stamps_2_match.py, Lipi impressions).

Plain words: COUNT-LINE SEAL = a seal whose text is only a number and a counted thing (003-156 = three + porter).
IMPRESSION = a clay sealing or tag (or stamped pot) that carries a stamped text. A seal is "on an impression" when
some impression anywhere carries its exact text.

Checks: (1) is a seal ever matched to an impression that is the same physical object (same Lipi object, one stone in
two catalogue rows, same site + excavation number), or, in the second catalogue, a 'sealing' entry that is probably
the same object Lipi lists as a seal (same site, same text, and Lipi has no impression of that text at that site)?
(1b) seals counted once per face. (c) the count rests on a handful of impression texts: report distinct texts.
Run: python3 recheck_08_countline_impressions.py   (seconds)
"""
import sys, io, contextlib, collections
sys.path.insert(0, '/home/claude/ivc/work_scripts')
import numpy as np, pandas as pd
from scipy.stats import fisher_exact
from recheck_common import *
say = log_to(f'{OUT}/r08_log.txt')
rng = np.random.default_rng(9)
with contextlib.redirect_stdout(io.StringIO()):
    from frame2_common import d, M, UNK
f2s, _ = stone_map()
SK = pd.read_csv(f'{ROOT}/work_data/frame/seal_kinds.csv', dtype=str).fillna('')
SK['stone'] = SK.id.map(f2s)
say(f'(A) frame2_seals (d): seal_kinds.csv {len(SK)} rows = {SK.obj.nunique()} objects (longest face per object): fault 1 absent')
CL = SK[SK.seal_kind.isin(['opener count', 'bare count'])]; NM = SK[SK.seal_kind == 'name seal']
say(f'  old: count-line {(CL.on_sealing == "True").sum()} of {len(CL)}, name seals {(NM.on_sealing == "True").sum()} of {len(NM)}')
L = d[(d.kind == 'tag')].copy(); L['text'] = L.tok.map('-'.join); L = L[np.array([bool(x) and not set(x) & UNK for x in L.tok], dtype=bool)]
L['stone'] = L.id.map(f2s)
Mt = M[(M.kind == 'tag')].copy(); Mt['text'] = Mt.tok.map('-'.join); Mt = Mt[np.array([bool(x) and not set(x) & UNK for x in Mt.tok], dtype=bool)]
lipi_site_txt = set(zip(L.site, L.text))
seal_site_txt = collections.Counter(zip(SK.site, SK.text))
rows = []
for r in pd.concat([CL, NM]).itertuples():
    lt = L[L.text == r.text]; mt = Mt[Mt.text == r.text]
    if not len(lt) and not len(mt): continue
    same_stone = (lt.stone == r.stone).any()
    same_exc = any((s == r.site and e == ex and e not in EMPTY) for s, e, ex in
                   zip(lt.site, lt['excavation-idno'], [d.loc[d.id == r.id, 'excavation-idno'].iloc[0]] * len(lt)))
    # second-catalogue sealing at the seal's own site with no Lipi impression of that text there: possibly the seal itself
    m_only = mt[np.array([(s, r.text) not in lipi_site_txt for s in mt.site_l], dtype=bool)]
    poss_self = (m_only.site_l == r.site).any()
    rows.append(dict(id=r.id, cisi=r.cisi, site=r.site, text=r.text, kind='count line' if r.seal_kind != 'name seal' else 'name',
                     lipi_impressions=len(lt), lipi_imp_sites=','.join(sorted(set(lt.site))), m77_sealings=len(mt),
                     m77_sites=','.join(sorted(set(mt.site_l))), same_stone=same_stone, same_exc=same_exc, m77_only_at_own_site=poss_self))
H = pd.DataFrame(rows); H.to_csv(f'{OUT}/r08_hits.csv', index=False)
say(f'  matches where the impression is the same stone: {int(H.same_stone.sum())}; same site + excavation number: {int(H.same_exc.sum())}')
say(f'  matches resting only on a second-catalogue sealing at the seal\'s own site (possible double entry): '
    f'{int(H.m77_only_at_own_site.sum())} ({", ".join(H[H.m77_only_at_own_site].cisi)})')
def fish(a, n, b, m, lab):
    p = fisher_exact([[a, n - a], [b, m - b]], alternative='greater')[1]
    say(f'  {lab}: count-line {a} of {n} ({a / n:.1%}) against name seals {b} of {m} ({b / m:.1%}), one-sided Fisher P {p:.2g}')
    return a, n, b, m, p
hitL = set(H[H.lipi_impressions > 0].id)
hitC = set(H[(H.lipi_impressions > 0) | ((H.m77_sealings > 0) & ~H.m77_only_at_own_site)].id)
f_all = fish(int(CL.id.isin(set(H.id)).sum()), len(CL), int(NM.id.isin(set(H.id)).sum()), len(NM), 'as run (Lipi tags + second-catalogue sealings)')
f_c = fish(int(CL.id.isin(hitC).sum()), len(CL), int(NM.id.isin(hitC).sum()), len(NM), 'clean: possible double entries removed')
f_l = fish(int(CL.id.isin(hitL).sum()), len(CL), int(NM.id.isin(hitL).sum()), len(NM), 'Lipi impressions only')
say('  count-line hits: ' + ' | '.join(f'{r.cisi} {r.site} {r.text} (Lipi imp {r.lipi_impressions} at {r.lipi_imp_sites or "-"}; M77 {r.m77_sealings} at {r.m77_sites or "-"})'
                                         for r in H[H.kind == 'count line'].itertuples()))
say(f'  distinct impression texts behind the count-line hits: {H[H.kind == "count line"].text.nunique()}; behind name-seal hits: {H[H.kind == "name"].text.nunique()}')

say('\n(B) stamps_2_match: count line 12 of 49 (24.5%) against 4.3% length-matched')
O = pd.read_csv(f'{ROOT}/work_data/stamps/objects.csv', dtype=str).fillna('')
O['n'] = O.n.astype(int); O['lost'] = O.lost.astype(int); O['stone'] = O.face.map(f2s)
I = O[O.tier.isin(['sealing', 'stamped pot']) & (O.lost == 0) & (O.n >= 2)]
S = O[(O.tier == 'seal') & (O.lost == 0) & (O.n >= 2)].copy()
def kind_of(tk):
    if tk in ('bare count line', 'front word + count line'): return 'count line'
    return 'other'
S['ck'] = S.text_kind.map(kind_of)
both = set(S.stone) & set(I.stone)
say(f'  seal faces {len(S)} on {S.stone.nunique()} stones; impression faces {len(I)}; stones that are both a seal and an impression: {len(both)}')
exc = d.set_index('id')['excavation-idno']
S['exc'] = S.face.map(exc); I = I.assign(exc=I.face.map(exc))
same_num = sum(1 for r in S.itertuples() for q in I[(I.signs == r.signs) & (I.site == r.site)].itertuples() if r.exc == q.exc and r.exc not in EMPTY)
say(f'  seal-impression exact matches sharing site + excavation number: {same_num}')
def stamp_test(S, I, lab):
    S = S.copy(); S['on'] = S.signs.isin(set(I.signs))
    g = S[S.ck == 'count line']; o = S[S.ck != 'count line']; by_len = {L: gg.on.values for L, gg in o.groupby('n')}
    draws = []
    for rep in range(2000):
        v = 0
        for L_, c in g.n.value_counts().items():
            pool = by_len.get(L_)
            if pool is None or not len(pool): continue
            v += rng.choice(pool, c).sum()
        draws.append(v / len(g))
    draws = np.array(draws); sh = g.on.mean()
    say(f'  {lab}: count line {int(g.on.sum())} of {len(g)} ({sh:.1%}) against {draws.mean():.1%} length-matched other seals (P {pvalue_hi(draws, sh):.4f}); '
        f'distinct impression texts behind the hits {g[g.on].signs.nunique()}')
    return int(g.on.sum()), len(g), draws.mean(), pvalue_hi(draws, sh)
b0 = stamp_test(S, I, 'as run (seal faces)')
b1 = stamp_test(S.drop_duplicates('stone'), I[~I.stone.isin(set(S.stone))], 'clean (one row per seal stone, impressions that are not seals)')
import json
json.dump(dict(frame_run=f_all, frame_clean=f_c, frame_lipi=f_l, stamps_run=b0, stamps_clean=b1), open(f'{OUT}/r08.json', 'w'), default=float, indent=1)
