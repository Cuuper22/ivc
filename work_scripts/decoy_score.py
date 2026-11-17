#!/usr/bin/env python3
"""Scores the decoy test. Seeds: none needed (exact tests, no randomness).
Reads work_data/decoy/results.csv (the tester's) and KEY_do_not_open.csv; for REAL and for DECOY items prints how many predictions came true /
right direction only / against, the real-versus-decoy difference with Fisher's exact test (came true vs not), and the same split by job class.
Run: python3 decoy_score.py [results.csv] [key.csv]"""
import sys, os, csv, collections
from scipy.stats import fisher_exact
D = '/home/claude/ivc/work_data/decoy'
rp = sys.argv[1] if len(sys.argv) > 1 else f'{D}/results.csv'
kp = sys.argv[2] if len(sys.argv) > 2 else f'{D}/KEY_do_not_open.csv'
def log(*a): print('[decoy_score]', *a, flush=True)
OUTS = ('came true', 'right direction only', 'against', 'too few')
def norm(o):
    o = o.strip().lower()
    if o.startswith('came') or o == 'yes': return 'came true'
    if o.startswith('right') or o.startswith('direction'): return 'right direction only'
    if o.startswith('against') or o == 'no': return 'against'
    if o.startswith('too') or o in ('n/a', ''): return 'too few'
    raise SystemExit(f'unknown outcome label: {o!r}')
log('reading key', kp); key = {r['item']: r for r in csv.DictReader(open(kp, newline=''))}
log('reading results', rp); res = {r['item']: r for r in csv.DictReader(open(rp, newline=''))}
missing = [i for i in key if i not in res]; extra = [i for i in res if i not in key]
if missing: log('items with no result:', missing)
if extra: log('results with no key row (ignored):', extra)
rows = [(key[i]['real_or_decoy'], key[i]['job_class'], norm(res[i]['outcome'])) for i in key if i in res]
log(f'{len(rows)} scored items')

def tally(sel):
    c = collections.Counter(o for k, cl, o in rows if sel(k, cl)); return c
def line(name, c):
    n = sum(c.values()); t = c['came true']
    return f"{name:8s} n={n:3d}  came true {c['came true']:3d} ({100 * t / max(n, 1):5.1f}%)  right direction only {c['right direction only']:3d}  against {c['against']:3d}  too few {c['too few']:3d}"
def compare(label, cr, cd):
    nr = sum(v for k, v in cr.items() if k != 'too few'); nd = sum(v for k, v in cd.items() if k != 'too few')
    a, b = cr['came true'], cd['came true']
    if nr == 0 or nd == 0: log(label, ': a group has no testable items, no comparison'); return
    odds, p = fisher_exact([[a, nr - a], [b, nd - b]])
    log(f'{label}: real {a}/{nr} = {100 * a / nr:.1f}% came true; decoy {b}/{nd} = {100 * b / nd:.1f}%; difference {100 * (a / nr - b / nd):+.1f} points; Fisher exact two-sided P {p:.4f} (odds ratio {odds:.2f}); one-sided real>decoy P {fisher_exact([[a, nr - a], [b, nd - b]], alternative="greater")[1]:.4f}')
    return p, a / nr - b / nd
log('=== all classes ===')
cr = tally(lambda k, c: k == 'real'); cd = tally(lambda k, c: k == 'decoy')
print(line('real', cr)); print(line('decoy', cd))
# "right direction" share too: came true + right direction only
for nm, c in (('real', cr), ('decoy', cd)):
    n = sum(v for k, v in c.items() if k != 'too few')
    if n: log(f'{nm}: right direction (came true or right direction only) {c["came true"] + c["right direction only"]}/{n} = {100 * (c["came true"] + c["right direction only"]) / n:.1f}%')
out = compare('came true, real vs decoy', cr, cd)
if out:
    p, diff = out
    if p < 0.05 and diff > 0:
        log('MEANING: real words pass clearly more often than decoys, so the word list carries information beyond the slot (the false-alarm rate of the method is the decoy rate above).')
    elif p < 0.05 and diff < 0:
        log('MEANING: decoys pass MORE often than real words; the predictions favour wrong words, so they cannot be read as support for the word list.')
    else:
        log(f'MEANING: no clear difference (P {p:.3f}). If real and decoy words pass about equally often, the predictions cannot tell a right word from a wrong one; the decoy pass rate is how often a wrong word passes the same test. (A small sample can hide a real gap: see the numbers above.)')
log('=== by job class ===')
for cl in sorted({c for k, c, o in rows}):
    r = tally(lambda k, c: k == 'real' and c == cl); dd = tally(lambda k, c: k == 'decoy' and c == cl)
    print(f'-- {cl}'); print(line('real', r)); print(line('decoy', dd)); compare(f'  {cl}', r, dd)
