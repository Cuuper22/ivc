#!/usr/bin/env python3
"""Merged value table work_data/values_master3.csv = values_master.csv (merged before the fifth pass) + the fifth
pass (sound_v5_values) + this pass (sound_v6_values). Status: strict = building on a fact not seen while choosing (or a
base value); wide = building on a fact seen while choosing; testing; paused."""
from sound_v6_common import *
from sound_v6_values import V6, TIER6, STRICT6, ALT6, NOTE6, UPD
from sound_v6_j3vals import J3
from sound_v5_values import V5, UPD as UPD5, J1 as J15
from sound_v6_job3 import W as W3
from sound_v6_job3b import WC
old = pd.read_csv(f'{ROOT}/work_data/values_master.csv', dtype=str).fillna('').set_index('sign')
DEDR6 = {'711': '5315', '060': '', '692': '1882', '838': '5437', '407': '2018', '842': '3308', '611': '1663', '341': '4780', '923': '4720', '255': '4952'}
for s, v in W3.items(): DEDR6[s] = v[2]
for s, v in WC.items():
    if J3.get(s, ('',))[0] == v[0]: DEDR6[s] = v[2]
rows = []
for s in sorted(set(old.index) | set(V6)):
    o = old.loc[s] if s in old.index else None
    if s in V6:
        t, st = TIER6[s], STRICT6[s]
        status = 'strict' if t == 'base' or st == 'building' else 'wide' if t == 'building' else t
        rep = 'sound_list_v6.md' if (s in UPD or s in J3) else 'sound_list_v5.md' if (s in UPD5 or s in J15) else (o.report if o is not None and o.sound == V6[s][0] else 'sound_list_v5.md')
        dedr = DEDR6.get(s) or (o.dedr if o is not None and o.sound == V6[s][0] else '')
        second = ALT6.get(s, '') or (f'{o.alt_sound} "{o.alt_english}"' if o is not None and o.alt_sound and o.alt_sound != V6[s][0] else '')
        rows.append(dict(sign=s, sound=V6[s][0], english=V6[s][1], dedr=dedr, status=status, report=rep, second_word=second))
    else:
        rows.append(dict(sign=s, sound=o.sound, english=o.english, dedr=o.dedr, status=o.status, report=o.report, second_word=o.alt_sound))
T = pd.DataFrame(rows)
T.to_csv(f'{ROOT}/work_data/values_master3.csv', index=False)
print(len(T), T.status.value_counts().to_dict())
