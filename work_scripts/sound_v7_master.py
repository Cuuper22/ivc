#!/usr/bin/env python3
"""ONE TABLE: work_data/values_master4.csv =
   values_master3.csv (sixth-pass sounds and status)  +  the slot words of values_master2.csv (odd-readings job)
   +  this pass's job-3 values (sound_v7_j3vals.py, when present).
Columns: sign, sound, english (default short word), english_name (inside a name), english_count (in a count line on goods),
english_final (text-final title), english_open (at the front), dedr, status, report, second_word.
Where the sound changed since values_master2 the old slot words are dropped (they belonged to the old word) unless listed in KEEP.
Run: python3 sound_v7_master.py"""
import os, sys
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = '/home/claude/ivc'
v3 = pd.read_csv(f'{ROOT}/work_data/values_master3.csv', dtype=str).fillna('').set_index('sign')
v2 = pd.read_csv(f'{ROOT}/work_data/values_master2.csv', dtype=str).fillna('').set_index('sign')

# short default words for signs that values_master2 did not have, or whose word changed in the sixth pass
SHORT = {'064': 'fork', '098': 'lady', '101': 'elder', '130': 'servant', '136': 'bondsman', '222': 'Shut-in-fish', '243': 'Scabbard-fish',
         '321': 'ration', '323': 'ration', '336': 'town', '341': 'stag', '406': 'kindred', '407': 'kindred', '408': 'herd', '405': 'thread',
         '421': 'field', '422': 'field', '423': 'field', '424': 'field', '554': 'paṟai measure', '592': 'hamlet', '603': 'door',
         '621': 'store', '642': 'many', '697': 'bundle', '703': 'cup measure', '772': 'child of', '773': 'child of', '776': 'flower',
         '792': 'gem', '804': 'crate', '821': 'betel', '844': 'sheaves', '927': 'two months', '060': 'of', '236': 'Bamboo-star',
         '645': 'gold weight', '611': 'Umbrella', '842': 'deputy', '711': 'vaḷḷam measure', '692': 'Assembly', '838': 'produce'}
SLOT_NEW = {   # slot words for signs new to the table (name / count / final / open)
    '406': ('Kindred', 'kindred', '', ''), '407': ('Kindred', 'kindred', '', ''), '772': ('', '', '', ''), '773': ('', '', '', ''),
    '927': ('Two-moons', 'two months', '', ''), '060': ('Inner', '', '', ''), '842': ('', '', 'deputy', ''),
}
KEEP = {'060'}     # 060: sound changed (uḷ -> -iṉ) but the Inner- name rule of the odd-readings job is kept
J3 = {}
try:
    from sound_v7_j3vals import J3                      # sign -> dict(sound, english, short, name, count, final, open, dedr, status, second)
except ImportError:
    pass
rows = []
for s in sorted(set(v3.index) | set(v2.index) | set(J3)):
    a = v3.loc[s] if s in v3.index else None
    b = v2.loc[s] if s in v2.index else None
    if a is not None:
        r = dict(sign=s, sound=a.sound, english_long=a.english, dedr=a.dedr, status=a.status, report=a.report, second_word=a.second_word)
    else:
        r = dict(sign=s, sound=b.sound, english_long=b.english, dedr=b.dedr, status=b.status, report=b.report, second_word=b.alt_sound)
    same = b is not None and (b.sound == r['sound'] or s in KEEP)
    r['english'] = SHORT.get(s) or (b.short if same and b.short else r['english_long'].split(' (')[0].split(';')[0].split(',')[0])
    if same:
        r['english_name'], r['english_count'], r['english_final'], r['english_open'] = b.short_name, b.short_count, b.short_final, b.short_open
    else:
        r['english_name'], r['english_count'], r['english_final'], r['english_open'] = SLOT_NEW.get(s, ('', '', '', ''))
    if s in SLOT_NEW:
        r['english_name'], r['english_count'], r['english_final'], r['english_open'] = SLOT_NEW[s]
    if s in J3:
        j = J3[s]
        for k in ('sound', 'dedr', 'status', 'second_word', 'english_name', 'english_count', 'english_final', 'english_open'):
            if j.get(k) is not None: r[k] = j[k]
        if j.get('english_long'): r['english_long'] = j['english_long']
        if j.get('english'): r['english'] = j['english']
        r['report'] = 'sound_list_v7.md'
    rows.append(r)
T = pd.DataFrame(rows)[['sign', 'sound', 'english', 'english_name', 'english_count', 'english_final', 'english_open', 'english_long', 'dedr', 'status', 'report', 'second_word']]
T.to_csv(f'{ROOT}/work_data/values_master4.csv', index=False)
print('values_master4.csv:', len(T), 'signs', T.status.value_counts().to_dict())
