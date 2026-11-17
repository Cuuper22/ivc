#!/usr/bin/env python3
"""The 24 values whose first check used a fact already seen while choosing the word: rerun the same check on
second-catalogue texts with no Lipi partner (new texts). Writes work_data/sound_v2/seen_rerun.csv"""
from sound_v2_try2 import *
def nonseal(s): 
    rows = faces_all('Mu'); allm = [g != 'seal' for x, P, st, g in rows]; sub = [g != 'seal' for x, P, st, g in rows if s in x]
    return share(allm, sub, 'faces not on seals')
def le3(s):
    v = [VAL[a] for a in counts_beside(s, 'Mu')]
    if len(v) < 3: return None
    k = sum(x <= 3 for x in v); return res(k / len(v) >= .95, 0.0 if k / len(v) >= .95 else 1.0, f'counts beside it <= 3: {k} of {len(v)} (Mu)')
def ordinal():
    c = collections.Counter()
    for x, P, st, g in faces_all('Mu'):
        for i in range(len(x) - 1):
            if x[i] == '060' and x[i + 1] in ('741', '742', '745'): c[x[i + 1]] += 1
    ok = c['741'] > c['742'] > c['745']; return res(ok, 0.0 if ok else 1.0, f'after 060: jar+1 {c["741"]}, jar+2 {c["742"]}, jar+3 {c["745"]} (Mu)')
def prejar(s):
    return adjacent(s, {'740'}, 'next', 'Mu')
def noanim(s):
    m = M[~M.partnered & (M.cls == 'seal')]
    a = m.fs.isin(['0', '']); b = m[m.tok.apply(lambda t: s in t)].fs.isin(['0', ''])
    return share(a, b, 'second-catalogue seals with no field symbol')
R = {'798': ('right before the jar', lambda: prejar('798')), '407': ('short-stroke counts', lambda: count_series('407', 'short', 'Mu')),
     '892': ('not on seals', lambda: nonseal('892')), '850': ('not on seals', lambda: nonseal('850')), '845': ('not on seals', lambda: nonseal('845')),
     '790': ('not on seals', lambda: nonseal('790')), '335': ('not on seals', lambda: nonseal('335')), '630': ('not on seals', lambda: nonseal('630')),
     '095': ('not on seals', lambda: nonseal('095')), '645': ('not on seals', lambda: nonseal('645')), '540': ('not on seals', lambda: nonseal('540')),
     '636': ('not on seals', lambda: nonseal('636')), '711': ('not on seals', lambda: nonseal('711')), '824': ('not on seals', lambda: nonseal('824')),
     '167': ('not on seals', lambda: nonseal('167')), '820': ('counts <= 3', lambda: le3('820')), '061': ('counts <= 3', lambda: le3('061')),
     '920': ('ordinal fall after 060', ordinal), '742': ('ordinal fall', ordinal), '745': ('ordinal fall', ordinal),
     '055': ('no animal', lambda: noanim('055')), '838': ('no animal', lambda: noanim('838')), '615': ('not on seals', lambda: nonseal('615')),
     '500': ('not on seals', lambda: nonseal('500'))}
rows = []
for s, (t, fn) in R.items():
    r = fn()
    if r is None: rows.append(dict(sign=s, test=t, result='too few new texts', outcome='n/a', p='')); print(s, 'n/a'); continue
    ok, p, txt = r; rows.append(dict(sign=s, test=t, result=txt, outcome='yes' if ok and p <= .1 else 'direction only' if ok else 'no', p=f'{p:.3g}')); print(s, rows[-1]['outcome'], txt, f'P {p:.3g}')
pd.DataFrame(rows).to_csv(f'{OUT}/seen_rerun.csv', index=False)
