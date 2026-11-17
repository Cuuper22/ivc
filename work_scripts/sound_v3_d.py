#!/usr/bin/env python3
"""Stage D, a lead the sail reading opened: 705 (U-vessel with a stick standing in it) is a hull with a mast,
kalam "vessel, ship" (DEDR 1305: kalam vessel ... ship; kalavar navigators), and 705-500 is kalam pāy "ship, sail".
Predictions written before running.  Writes stage_d.csv."""
from sound_v3_common import *
D = {
 '705': ('kalam', 'a ship word: on new texts 705 sits at Lothal, the port, more than chance', 'fresh', lambda: site_share('705', 'Lothal', 'Mu')),
 '705b': ('kalam', 'shipped goods are sealed: on new texts 705 sits on sealings/tags more than chance', 'fresh', lambda: on_kind('705', 'tag')),
 '705c': ('kalam pāy', 'ship + sail: on new texts 500 follows 705 more than chance', 'fresh', lambda: adjacent('705', '500', 'next', 'Mu')),
}
if __name__ == '__main__':
    rows = []
    for i, (s, (w, pred, fr, fn)) in enumerate(D.items(), 1):
        print(f'({i}/{len(D)})', end=' '); r = run('D', s, w, pred, fn); r['fresh'] = fr; rows.append(r)
    pd.DataFrame(rows).to_csv(f'{OUT3}/stage_d.csv', index=False)
