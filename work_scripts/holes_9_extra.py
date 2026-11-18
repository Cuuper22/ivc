#!/usr/bin/env python3
"""Extra checks used in the report.  Predictions (fixed before running):
 X1  335 is part of the grain-record block: 70% or more of tablet lines carrying 335 also carry the grain header 413 (base: share of all tablet lines with 413).
 X2  842: probability of 3 or more of 5 texts holding a chief sign if the base rate is the seal rate (0.157): reported, no prediction (post hoc, see report).
 X3  645 fills the slot of the chief 255 in a fixed seal frame: in the Mahadevan table at least 2 lines with 645-partner (137) first, followed by the same 6 signs as the 255 frame.
 X4  the signboard's third phrase has a sibling: a wheel next to maru- (798) on another object (pot H-1402 820-798-740).
"""
import sys, math, collections
sys.path.insert(0, '/home/antigravity/Cuuper22/ivc/work_scripts')
from holes_common import *
ls = lines(True); out = []
def P(s): out.append(s); print(s)
tab = [L for L in ls if kind(L['type']) == 'TAB']
t335 = [L for L in tab if '335' in L['toks']]; k = sum('413' in L['toks'] for L in t335)
base = sum('413' in L['toks'] for L in tab) / len(tab)
pv = sum(math.comb(len(t335), i) * base ** i * (1 - base) ** (len(t335) - i) for i in range(k, len(t335) + 1))
P(f'X1  tablet lines with 335: {len(t335)}; with 413 as well: {k} ({k/len(t335):.2f}); base share of tablet lines with 413 {base:.3f}; one-sided binomial P {pv:.1e}')
pv2 = sum(math.comb(5, i) * 0.157 ** i * 0.843 ** (5 - i) for i in range(3, 6))
P(f'X2  P(3 or more of 5 | 0.157) = {pv2:.4f}')
M = mah_lines()
fr = [(r['textnum'], r['toks']) for r in M if r['toks'][:1] == (137,) and 155 in r['toks']]
fr255 = [(r['textnum'], r['toks']) for r in M if r['toks'][:2] == (51, 155)]
P(f'X3  Mahadevan lines starting 137 then 155: {fr}; lines starting with the 255-partner(51) then 155: {fr255}')
P('X4  wheel next to 798 elsewhere: ' + str([(L["cisi"], "-".join(L["toks"])) for L in ls if "820" in L["toks"] and "798" in L["toks"]]))
open(f'{HOLES}/tests_extra.txt', 'w').write('\n'.join(out))
