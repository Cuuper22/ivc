#!/usr/bin/env python3
"""STYLE step 2: self-agreement between the main pass and the blind second pass (40 stones).
Rule fixed first: per feature, agreement = share of stones read in both passes (neither '?') that got the same value;
readability = share of the 40 read in both passes. A feature is KEPT if agreement >= 0.75 and at least 15 stones were
read in both passes. Also reports chance agreement from the main-pass value mix (sum of squared shares)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_common import *
M = pd.read_csv(f'{OUT}/codes_main.csv', dtype=str).merge(pd.read_csv(f'{OUT}/key_main.csv', dtype=str)[['num', 'obj']], on='num')
R = pd.read_csv(f'{OUT}/codes_recode.csv', dtype=str).merge(pd.read_csv(f'{OUT}/key_recode.csv', dtype=str)[['num', 'obj']], on='num')
J = M.merge(R, on='obj', suffixes=('_1', '_2'))
rows = []
for f in FEATURES:
    a, b = J[f + '_1'], J[f + '_2']; both = (a != '?') & (b != '?')
    n = int(both.sum()); agree = float((a[both] == b[both]).mean()) if n else np.nan
    mix = M[f][M[f] != '?'].value_counts(normalize=True); chance = float((mix ** 2).sum())
    one = int(((a != '?') ^ (b != '?')).sum())
    rows.append(dict(feature=f, both_read=n, read_one_pass_only=one, agree=round(agree, 3), chance=round(chance, 3),
                     main_read=int((M[f] != '?').sum()), kept=bool(n >= 15 and agree >= 0.75)))
T = pd.DataFrame(rows); T.to_csv(f'{OUT}/agreement.csv', index=False); print(T.to_string(index=False))
J.to_csv(f'{OUT}/recode_joined.csv', index=False)
