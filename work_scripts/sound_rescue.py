#!/usr/bin/env python3
"""Second tries for values whose first check went against them (one new prediction each).
717 aṭi read as 'base, origin, founder' [DEDR 72] -> house-mates share it; 803 il read as 'wife, mistress of the house'
[494] -> sits in one text with the woman sign 140; 900 tiṅkaḷ month -> counted with short strokes; 171 niṟai -> house-mates
share it (an office kept in one house); 233/231 fish crests -> shared in houses when read as the first name sign only."""
import sys, os
sys.argv = [sys.argv[0]]
import importlib.util
spec = importlib.util.spec_from_file_location('sc', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sound_checks.py'))
src = open(spec.origin).read().split("print('stage 2/3")[0]
exec(src)
from scipy.stats import fisher_exact
print('717 house:', t_house('717')); print('171 house:', t_house('171')); print('900 short counts:', t_short('900'))
a = objs.signs.apply(lambda z: '803' in z); b = objs.signs.apply(lambda z: '140' in z)
k = int((a & b).sum()); e = a.sum() * b.sum() / len(objs)
print(f'803 with 140 on one object: {k} against {e:.2f}; P', fisher_exact([[k, int((a & ~b).sum())], [int((~a & b).sum()), int((~a & ~b).sum())]], alternative='greater')[1])
