#!/usr/bin/env python3
"""sense_report.py -- turns work_data/sense/results_*.json and the per-sign arrays into the tables of jobs/out/sense_test.md
(writes work_data/sense/tables.md; the prose of the report is written by hand around these tables).  Run: python3 sense_report.py"""
import json, numpy as np, pandas as pd
D = '/home/claude/ivc/work_data/sense'
VN = {'ov': 'category overlap', 'lift': 'category lift', 'cos': 'vector closeness'}
core = json.load(open(f'{D}/results_core.json')); N = core['N']
def pz(real, arr):
    a = np.array(arr); return (1 + (a >= real).sum()) / (len(a) + 1), (real - a.mean()) / (a.std() + 1e-12), a.mean(), a.std()
def verdict(p):
    return 'above chance' if p <= 0.05 else 'BELOW chance (against)' if p >= 0.95 else 'inside chance'
out = []
out.append('### Core table (real list against %d shuffles of each kind)\n' % N)
out.append('P = share of shuffles scoring at least as high as the real list (so P near 0 = real list ranks at the top; near 0.5 = it is a typical shuffle; near 1 = it ranks at the bottom). "chance" column = mean of the shuffles +- one spread.\n')
out.append('| score | texts | signs scored | real | A: chance (same class+band) | A: P | A: z | B: chance (sense count kept) | B: P | B: z | reading of B |')
out.append('|---|---|---|---|---|---|---|---|---|---|---|')
rows = []
for g, gl in (('new', 'new texts (main)'), ('lipi', 'Lipi (second)')):
    for sub, sl in (('all', 'all labelled'), ('sub', '30 strongest')):
        for v in ('ov', 'lift', 'cos'):
            k = f'{v}|{g}|{sub}'; r = core['real'][k]
            pa, za, ma, sa = pz(r, core['shuf']['A']['rec'][k]); pb, zb, mb, sb = pz(r, core['shuf']['B']['rec'][k])
            out.append(f'| {VN[v]} | {gl} | {sl} | {r:.4f} | {ma:.4f} +- {sa:.4f} | {pa:.3f} | {za:+.2f} | {mb:.4f} +- {sb:.4f} | {pb:.3f} | {zb:+.2f} | {verdict(pb)} |')
            rows.append((v, g, sub, r, ma, pa, za, mb, pb, zb))
out.append('')
# per sign
S = pd.read_csv(f'{D}/signs.csv', dtype={'sign': str}).fillna('')
um = np.load(f'{D}/unit_means_real.npy'); cnt = np.load(f'{D}/unit_counts_real.npy')
res = {}
for tag in ('A', 'B'):
    sh = np.load(f'{D}/unit_means_shuf_{tag}.npy')          # [3, N, U]
    z = (um[:, None, :] - sh).mean(1) / (sh.std(1) + 1e-9)
    frac = (um[:, None, :] > sh).mean(1)
    res[tag] = (z, frac)
S['events'] = cnt
for i, v in enumerate(('ov', 'lift', 'cos')):
    S[f'z_{v}_B'] = res['B'][0][i]; S[f'z_{v}_A'] = res['A'][0][i]; S[f'beat_{v}_B'] = res['B'][1][i]
S['zB'] = S[[f'z_{v}_B' for v in ('ov', 'lift', 'cos')]].mean(axis=1); S['zA'] = S[[f'z_{v}_A' for v in ('ov', 'lift', 'cos')]].mean(axis=1)
S['beatB'] = S[[f'beat_{v}_B' for v in ('ov', 'lift', 'cos')]].mean(axis=1)
S.to_csv(f'{D}/per_sign.csv', index=False)
ok = S[S.events >= 5].sort_values('zB', ascending=False)
out.append('### Per-sign: real word against that sign\'s own shuffles\n')
out.append(f'{len(ok)} of {len(S)} labelled signs sit in at least 5 weighted objects (Lipi + new texts pooled); the rest are too rare to rank. For each sign: its average fit (see method) under its real word, against the %d sense-count-keeping shuffles (where the sign carries other words of its class and band). z is averaged over the three score versions; "beaten" is the share of shuffles its real word beats, averaged over versions (0.5 = chance).\n' % N)
def tab(df):
    o = ['| sign | real word (gloss) | class | objects | senses | z (mean of 3 versions) | share of shuffles beaten |', '|---|---|---|---|---|---|---|']
    for r in df.itertuples():
        o.append(f'| {r.sign} | {r.sound} ({r.english}) | {r.cls} | {r.events:.0f} | {r.nsenses} | {r.zB:+.2f} | {r.beatB:.2f} |')
    return o
out.append('**15 signs whose real word beats its shuffles by the most**\n'); out += tab(ok.head(15)); out.append('')
out.append('**15 signs whose real word beats its shuffles by the least (most negative)**\n'); out += tab(ok.tail(15).iloc[::-1]); out.append('')
out.append(f'Spread of z over the {len(ok)} signs: mean {ok.zB.mean():+.2f}, share with z above 0: {(ok.zB > 0).mean():.2f}, share with z above 2: {(ok.zB > 2).mean():.2f}, below -2: {(ok.zB < -2).mean():.2f}. A sign list with no signal would give a mean near 0 and about 2.5% beyond +2 and 2.5% beyond -2 by chance alone.\n')
# mass
mass = json.load(open(f'{D}/results_mass.json'))
out.append('### Mass run (every candidate word of the pool tried in place of each sign\'s label, new texts)\n')
out.append('rank percentile: 1.0 = the real label is the best candidate, 0.5 = middle (chance), 0.0 = worst. "scrambled" = the same search on new texts where which signs sit together has been destroyed (every sign occurrence dealt out again at random, same text lengths and sign totals; mean of 10 scrambles). Ties share places.\n')
out.append('| score | pool | candidates per sign | signs | real: mean percentile | scrambled: mean percentile | real: first place | chance first | scrambled first | real: top 10% | chance | scrambled top 10% |')
out.append('|---|---|---|---|---|---|---|---|---|---|---|---|')
for key, m in mass.items():
    v, pm = key.split('|')
    for sel, sl in (('all', 'all candidates'), ('matched', 'candidates within 3 senses of the real word')):
        if sel not in m['real']: continue
        r, s = m['real'][sel], m['scrambled'][sel]
        out.append(f"| {VN[v]} | {pm} | {r['mean_pool']:.0f} ({sl}) | {r['n_signs']} | {r['mean_pct']:.3f} | {s['mean_pct']:.3f} | {r['top1']:.3f} | {r['chance_top1']:.3f} | {s['top1']:.3f} | {r['top10']:.3f} | {r['chance_top10']:.3f} | {s['top10']:.3f} |")
out.append('')
# control
c = json.load(open(f'{D}/results_control.json'))
out.append('### Control (English sentences, WordNet senses)\n')
out.append(f"{c['n_texts']} sentences ({c['n_short']} with 4 or fewer content words), {c['n_words']} words, {c['N']} shuffles of each kind.\n")
out.append('| score | sentences | real | A: chance | A: P | A: z | B: chance | B: P | B: z |'); out.append('|---|---|---|---|---|---|---|---|---|')
for g, gl in (('all', 'all'), ('short', '4 words or fewer')):
    for v in ('ov', 'lift', 'cos'):
        k = f'{v}|{g}'; r = c['real'][k]; pa, za, ma, sa = pz(r, c['shuf']['A']['rec'][k]); pb, zb, mb, sb = pz(r, c['shuf']['B']['rec'][k])
        out.append(f'| {VN[v]} | {gl} | {r:.4f} | {ma:.4f} +- {sa:.4f} | {pa:.3f} | {za:+.2f} | {mb:.4f} +- {sb:.4f} | {pb:.3f} | {zb:+.2f} |')
open(f'{D}/tables.md', 'w').write('\n'.join(out)); print('\n'.join(out))
