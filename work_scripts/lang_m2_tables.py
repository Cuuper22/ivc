#!/usr/bin/env python3
"""lang_m2: markdown tables from grid.csv, summary.csv, swap_grid.csv -> work_data/lang_m2/tables.md (pasted into the report)."""
import sys, os, csv, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lang_m2_common import *
G = list(csv.DictReader(open(f'{OUT}/grid.csv', encoding='utf-8')))
S = list(csv.DictReader(open(f'{OUT}/summary.csv', encoding='utf-8')))
W = list(csv.DictReader(open(f'{OUT}/swap_grid.csv', encoding='utf-8'))) if os.path.exists(f'{OUT}/swap_grid.csv') else []
L = []
def p(x): return f'{float(x):.3g}'
L.append('### Step 6 summary per family\n')
L.append('| variant | family | dictionaries | cells | cells beating all 4 controls (P<0.05) | expected by chance (bound) | cells beating C2 and C3 | Z3 (mean z vs C3) / P | Z1 (vs C1) / P | Z4 (vs C4) / P | clears bar |')
L.append('|---|---|---|---|---|---|---|---|---|---|---|')
for r in S:
    L.append(f"| {r['variant']} | {r['family']} | {r['dictionaries']} | {r['cells']} | {r['beat_all4']} | {r['expected_bound']} | {r['beat_c2_and_c3']} | "
             f"{r['Z3']} / {r['Z3_P']} | {r['Z1']} / {r['Z1_P']} | {r['Z4']} / {r['Z4_P']} | {'yes' if r['clears_bar'] == 'True' else 'no'} |")
for v in VARIANTS:
    for stat in ('share', 'hits'):
        L.append(f'\n### {v}: {stat}, every family and every dictionary, full grid\n')
        L.append(f'| dictionary / family | distance | keywords | units covered | {stat} | C1 classes dealt mean / P | C2 outside nouns mean / P | '
                 f'C3 sounds dealt by entry mean / P | C4 wrong class same picture mean / P | C3row mean / P |')
        L.append('|---|---|---|---|---|---|---|---|---|---|')
        order = [f'FAMILY {f}' for f in FAMILIES] + [n for ns in FAMILIES.values() for n in ns]
        for u in order:
            for r in [r for r in G if r['variant'] == v and r['unit'] == u]:
                mark = ' **all 4**' if r[f'{stat}_all4'] == 'True' else ''
                L.append(f"| {u} | {r['dist']} | {r['breadth']} | {r['covered']}/{r['units']} | {p(r[stat])}{mark} | "
                         + ' | '.join(f"{p(r[f'{stat}_{t}_mean'])} / {r[f'{stat}_{t}_P']}" for t in ('c1', 'c2', 'c3', 'c4', 'c3row')) + ' |')
if W:
    for v in VARIANTS:
        L.append(f'\n### Swap pairs, {v}\n')
        L.append('| dictionary / family | distance | sound-alike pairs / tested | random pairs mean (sd) / P | pictures dealt mean (sd) / P |')
        L.append('|---|---|---|---|---|')
        for r in [r for r in W if r['variant'] == v]:
            L.append(f"| {r['unit']} | {r['dist']} | {r['soundalike']}/{r['pairs']} | {r['R_mean']} ({r['R_sd']}) / {r['R_P']} | {r['S_mean']} ({r['S_sd']}) / {r['S_P']} |")
open(f'{OUT}/tables.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('written tables.md', len(L), 'lines')
