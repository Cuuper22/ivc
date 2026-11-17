#!/usr/bin/env python3
"""Job 2, one redesign for each rival word whose prediction did not come true, written before running.
Appends to work_data/sound_v6/job2_tests.csv (stage J2b)."""
from sound_v6_common import *
from sound_v6_job2 import frac_with, sites
T = [
 ('692', 'kūṭṭam "assembly"', 'an assembly sits in the great cities: faces with 692 are at Mohenjo-daro or Harappa more than faces overall', lambda: sites('692', {'Mohenjo-daro', 'Harappa'})),
 ('692', 'nāṭu "district"', 'a district is an agricultural tract: faces with 692 carry a crop word (produce 806/838, grain 413, threshed heap 416, sheaves 845, cotton 390, millet 831) more than faces overall', lambda: frac_with('692', {'806', '838', '413', '416', '845', '390', '831'})),
 ('838', 'viḷai "produce"', 'produce goes with crops: faces with 838 carry another crop word (grain 413, heap 416, sheaves 845, cotton 390, millet 831, produce 806) more than faces overall', lambda: frac_with('838', {'413', '416', '845', '390', '831', '806'})),
 ('838', 'eḷ "sesame"', 'sesame is oil, kept in jars: 838 is on pottery more than faces overall', lambda: on_kind('838', 'pot', 'LM')),
 ('407', 'kiḷai "kindred"', 'kindred is a name word: faces with 407 carry a fish crest (231, 233, 235, 240, 220) more than faces overall', lambda: frac_with('407', {'231', '233', '235', '240', '220'})),
 ('407', 'tuṇi "cloth"', 'cloth is sold and given: faces with 407 carry a trade verb (sale 892, given 890, received 440, price 824) more than faces overall', lambda: frac_with('407', {'892', '890', '440', '824'})),
]
if __name__ == '__main__':
    for s, w, p, f in T: print(f'[{s}] {w}: {p}', flush=True)
    print('---- computing ----', flush=True)
    out = [run('J2b', s, w, p, f) for s, w, p, f in T]
    old = pd.read_csv(f'{OUT6}/job2_tests.csv'); old = old[old.stage != 'J2b']
    pd.concat([old, pd.DataFrame(out)]).to_csv(f'{OUT6}/job2_tests.csv', index=False)
