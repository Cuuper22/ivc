#!/usr/bin/env python3
"""Writes jobs/out/endings_heads.md from the tables in work_data/endings/ (run endings_build, A2-A6, B first)."""
import pandas as pd, ast
R='/home/claude/ivc'
m=pd.read_csv(f'{R}/work_data/endings/A4_mixed_names_clean.csv',dtype=str)
lines=[]
for r in m.itertuples():
    lines.append(f"| {r.name} | {r.n} | {r.endings} | {r.seals} |")
mixed='\n'.join(lines)
txt=open(f'{R}/work_scripts/endings_report_template.md').read().replace('@@MIXED@@',mixed)
open(f'{R}/jobs/out/endings_heads.md','w').write(txt)
