#!/usr/bin/env python3
"""lang_m: turns grid.csv and swap_grid.csv into the markdown tables of jobs/out/language_machine.md (work_data/lang_m/tables.md)."""
import csv
OUT = '/home/antigravity/Cuuper22/ivc/work_data/lang_m'
g = list(csv.DictReader(open(f'{OUT}/grid.csv'))); s = list(csv.DictReader(open(f'{OUT}/swap_grid.csv')))
L = []
def p(x): return f'{float(x):.3f}'.rstrip('0').rstrip('.') if float(x) < 1 else '1'
L.append('### Share score, every family, full grid\n')
L.append('| family | distance | keywords | units with a picture word | share | control 1 (jobs dealt) mean / P | control 2 (outside nouns) mean / P | control 3 (sounds dealt) mean / P |')
L.append('|---|---|---|---|---|---|---|---|')
for r in g:
    if r['unit'].startswith('FAMILY'):
        L.append(f"| {r['unit'][7:]} | {r['dist']} | {r['breadth']} | {r['covered']}/{r['units']} | {float(r['share']):.2f} | {float(r['share_c1_mean']):.2f} / {p(r['share_c1_P'])} | {float(r['share_c2_mean']):.2f} / {p(r['share_c2_P'])} | {float(r['share_c3_mean']):.2f} / {p(r['share_c3_P'])} |")
L.append('\n### Hit count, every family, full grid\n')
L.append('| family | distance | keywords | hits | control 1 mean (sd) / P | control 2 mean (sd) / P | control 3 mean (sd) / P |')
L.append('|---|---|---|---|---|---|---|')
for r in g:
    if r['unit'].startswith('FAMILY'):
        L.append(f"| {r['unit'][7:]} | {r['dist']} | {r['breadth']} | {r['hits']} | {float(r['hits_c1_mean']):.1f} ({float(r['hits_c1_sd']):.1f}) / {p(r['hits_c1_P'])} | {float(r['hits_c2_mean']):.1f} ({float(r['hits_c2_sd']):.1f}) / {p(r['hits_c2_P'])} | {float(r['hits_c3_mean']):.1f} ({float(r['hits_c3_sd']):.1f}) / {p(r['hits_c3_P'])} |")
L.append('\n### Every dictionary, share score (P against controls 1 / 2 / 3), cells: strict-narrow, strict-wide, medium-narrow, medium-wide, loose-narrow, loose-wide\n')
L.append('| dictionary | words / entries | units covered | s-n | s-w | m-n | m-w | l-n | l-w |')
L.append('|---|---|---|---|---|---|---|---|---|')
by = {}
for r in g:
    if not r['unit'].startswith('FAMILY'): by.setdefault(r['unit'], []).append(r)
for u, rs in by.items():
    cells = [f"{float(r['share']):.2f} ({p(r['share_c1_P'])}/{p(r['share_c2_P'])}/{p(r['share_c3_P'])})" for r in rs]
    L.append(f"| {u} | {rs[0]['words']} / {rs[0]['entries']} | {rs[0]['covered']} | " + ' | '.join(cells) + ' |')
L.append('\n### Swap pairs (65 pairs of differently drawn things), sound-alike picture names\n')
L.append('| family | distance | sound-alike pairs | random pairs mean (sd) / P | pictures dealt mean (sd) / P |')
L.append('|---|---|---|---|---|')
for r in s:
    if r['unit'].startswith('FAMILY'):
        L.append(f"| {r['unit'][7:]} | {r['dist']} | {r['soundalike']} | {r['R_mean']} ({r['R_sd']}) / {p(r['R_P'])} | {r['S_mean']} ({r['S_sd']}) / {p(r['S_P'])} |")
open(f'{OUT}/tables.md', 'w').write('\n'.join(L) + '\n'); print('[lang_m_tables] written tables.md')
